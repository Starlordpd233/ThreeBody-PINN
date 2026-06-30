import os
import pathlib
import re
import shutil
import signal
import subprocess
import tempfile
import time
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
WD = ROOT / "tools" / "watchdog"
COMMON = WD / "lib" / "wd-common.sh"
PUBLISH = WD / "wd-publish-done"
CHECK = WD / "wd-check"
ARM = WD / "wd-arm"
PUSH = WD / "wd-push"
DISARM = WD / "wd-disarm"
STATUS = WD / "wd-status"
INTEGRATE = WD / "wd-integrate"
GSD_PUBLISH = WD / "wd-gsd-publish"

# Git/agent vars that could leak the parent session's repo or identity into a
# temp-repo test are stripped from the inherited environment.
ISOLATED_KEYS = (
    "GIT_AGENT_ID",
    "GIT_AGENT_OWNED_PATHS",
    "GIT_AGENT_COMMIT",
    "GIT_DIR",
    "GIT_WORK_TREE",
)


def _clean_env(extra=None):
    merged = os.environ.copy()
    for key in ISOLATED_KEYS:
        merged.pop(key, None)
    if extra:
        merged.update(extra)
    return merged


def run(args, cwd, env=None, timeout=60):
    return subprocess.run(
        [str(a) for a in args],
        cwd=str(cwd),
        text=True,
        capture_output=True,
        env=_clean_env(env),
        check=False,
        timeout=timeout,
    )


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, check=False,
    )


def init_repo(path):
    # .resolve() collapses the macOS /var -> /private/var symlink so cwd-based
    # paths and git's realpath toplevel agree.
    path = pathlib.Path(path).resolve()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    git(path, "config", "user.email", "test@example.com")
    git(path, "config", "user.name", "Test")
    (path / "README.md").write_text("hello\n")
    git(path, "add", "README.md")
    git(path, "commit", "-q", "-m", "init")
    return path


def first_token(proc):
    return proc.stdout.split()[0] if proc.stdout.strip() else ""


# tmux stub (identical contract to tests/watchdog/test_push.py): logs each call
# to $TMUX_LOG, exits 0, honors TMUX_STUB_NO_PANE / TMUX_STUB_SEND_KEYS_FAIL.
TMUX_STUB = """#!/bin/sh
log="${TMUX_LOG:-/dev/null}"
printf '%s\\n' "$*" >> "$log"
cmd="${1:-}"
case "$cmd" in
  has-session|list-panes)
    [ -n "${TMUX_STUB_NO_PANE:-}" ] && exit 1
    exit 0
    ;;
  send-keys)
    [ -n "${TMUX_STUB_SEND_KEYS_FAIL:-}" ] && exit 1
    exit 0
    ;;
  *) exit 0 ;;
esac
"""


def _stub_tmux_on_path(d):
    bindir = pathlib.Path(d) / "stubbin"
    bindir.mkdir()
    tmux = bindir / "tmux"
    tmux.write_text(TMUX_STUB)
    tmux.chmod(0o755)
    return f"{bindir}:{os.environ['PATH']}"


def _popen_arm(repo, channel, poll, timeout):
    return subprocess.Popen(
        [str(ARM), "--channel", channel, "--poll-secs", str(poll),
         "--timeout-secs", str(timeout)],
        cwd=str(repo), text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=_clean_env(),
    )


class MultiProcessTests(unittest.TestCase):

    # C1 — N real consumer processes race one publish; exactly one wins.
    def test_c1_n_consumers_exactly_one(self):
        import concurrent.futures
        with tempfile.TemporaryDirectory() as d:
            repo = init_repo(pathlib.Path(d) / "proj")
            run([PUBLISH, "--channel", "c", "--stage", "s", "--scope", "README.md"], cwd=repo)
            N = 6

            def arm_once():
                return run([ARM, "--channel", "c", "--poll-secs", "1", "--timeout-secs", "20"],
                           cwd=repo, timeout=40)

            with concurrent.futures.ThreadPoolExecutor(max_workers=N) as ex:
                res = [f.result() for f in [ex.submit(arm_once) for _ in range(N)]]
            v = [first_token(r) for r in res]
            self.assertEqual(v.count("WAKE"), 1, f"not exactly one WAKE: {v}")
            self.assertEqual(len(list((repo / ".git/live-monitor/channels/c").glob("claimed.*"))), 1)

    # C2 — mixed wake paths (2 wd-arm + 1 wd-push) race one head; exactly one of
    # {WAKE, PUSHED}, the rest ALREADY-CLAIMED, exactly one claim dir.
    def test_c2_mixed_arm_push_exactly_one(self):
        import concurrent.futures
        with tempfile.TemporaryDirectory() as d:
            repo = init_repo(pathlib.Path(d) / "proj")
            run([PUBLISH, "--channel", "c", "--stage", "s", "--scope", "README.md"], cwd=repo)
            stub_path = _stub_tmux_on_path(d)
            log = pathlib.Path(d) / "tmux.log"

            def arm_once():
                return run([ARM, "--channel", "c", "--poll-secs", "1", "--timeout-secs", "20"],
                           cwd=repo, timeout=40)

            def push_once():
                return run([PUSH, "--channel", "c", "--pane", "fake:0.0",
                            "--poll-secs", "1", "--timeout-secs", "20"],
                           cwd=repo, env={"PATH": stub_path, "TMUX_LOG": str(log)}, timeout=40)

            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
                fs = [ex.submit(arm_once), ex.submit(arm_once), ex.submit(push_once)]
                res = [f.result() for f in fs]
            v = [first_token(r) for r in res]
            winners = v.count("WAKE") + v.count("PUSHED")
            self.assertEqual(winners, 1, f"not exactly one winner: {v}")
            self.assertEqual(v.count("ALREADY-CLAIMED"), 2, f"{v}")
            self.assertEqual(len(list((repo / ".git/live-monitor/channels/c").glob("claimed.*"))), 1)

    # C3 — disarm sentinel dropped mid-poll stands down a RUNNING watcher within a
    # couple of poll intervals (process-fidelity timing).
    def test_c3_disarm_sentinel_timing(self):
        with tempfile.TemporaryDirectory() as d:
            repo = init_repo(pathlib.Path(d) / "proj")
            chan = repo / ".git/live-monitor/channels/c"
            proc = _popen_arm(repo, "c", poll=1, timeout=30)
            try:
                time.sleep(2)  # let it arm + enter the poll loop
                self.assertTrue((chan / "armed.json").exists(), "watcher did not arm")
                (chan / "disarm").write_text("")
                out, err = proc.communicate(timeout=10)
            finally:
                if proc.poll() is None:
                    proc.kill()
            self.assertEqual(proc.returncode, 0, err)
            self.assertEqual(out.strip(), "DISARMED", f"out={out!r} err={err!r}")

    # C4 — SIGTERM during the poll sleep stands down via the TERM trap (DISARMED,
    # exit 0), not a silent kill.
    def test_c4_sigterm_during_sleep_disarms(self):
        with tempfile.TemporaryDirectory() as d:
            repo = init_repo(pathlib.Path(d) / "proj")
            proc = _popen_arm(repo, "c", poll=5, timeout=30)
            try:
                time.sleep(2)  # now inside `sleep 5`
                proc.send_signal(signal.SIGTERM)
                out, err = proc.communicate(timeout=10)
            finally:
                if proc.poll() is None:
                    proc.kill()
            self.assertEqual(out.strip(), "DISARMED", f"out={out!r} err={err!r}")
            self.assertEqual(proc.returncode, 0)

    # C5 — cross-worktree with REAL linked worktrees: not-integrated -> STALE,
    # integrate -> WAKE; and conflict -> abort with a clean tree.
    # NOTE: tests/watchdog/test_watchdog_xworktree.py already uses real
    # `git worktree add` for all four sub-cases. Mark C5 ⏭️ covered-elsewhere.

    # C6 — channel isolation across two repos: a publish in repo-Y is invisible in
    # repo-Z (no cross-talk). Satisfies design T4.3 automatically.
    def test_c6_cross_repo_isolation(self):
        with tempfile.TemporaryDirectory() as d:
            y = init_repo(pathlib.Path(d) / "Y")
            z = init_repo(pathlib.Path(d) / "Z")
            run([PUBLISH, "--channel", "shared", "--stage", "s", "--scope", "README.md"], cwd=y)
            in_y = run([CHECK, "--channel", "shared"], cwd=y)
            in_z = run([CHECK, "--channel", "shared"], cwd=z)
            self.assertEqual(first_token(in_y), "WAKE", f"Y should WAKE: {in_y.stdout!r}")
            self.assertNotEqual(first_token(in_z), "WAKE",
                                f"Z must NOT see Y's publish (cross-talk): {in_z.stdout!r}")