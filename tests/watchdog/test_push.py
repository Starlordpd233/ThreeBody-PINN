#!/usr/bin/env python3
"""Tests for wd-push (Phase 5): the PUSH (tmux) accelerator.

The real tmux + claude-TUI interaction is NOT unittest-able. These tests
exercise wd-push's DETERMINISTIC SURFACE only — arg validation, the hard
preconditions (tmux-missing / pane-not-found), the two-call send-keys shim
construction, the exactly-once claim shared with wd-arm, and the disarm
lifecycle — via a STUB `tmux` placed on PATH. They do NOT drive a real tmux
session or a real claude TUI, and assert nothing about a live pane.

Channel state is isolated in a throwaway git repo so the real repo's
.git/live-monitor/channels/ is never touched.
"""
import os
import pathlib
import shutil
import subprocess
import tempfile
import time
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
WD = ROOT / "tools" / "watchdog"
PUBLISH = WD / "wd-publish-done"
PUSH = WD / "wd-push"
ARM = WD / "wd-arm"
DISARM = WD / "wd-disarm"
STATUS = WD / "wd-status"

# Git/agent vars that could leak the parent session's repo or identity into a
# temp-repo test are stripped from the inherited environment.
ISOLATED_KEYS = (
    "GIT_AGENT_ID",
    "GIT_AGENT_OWNED_PATHS",
    "GIT_AGENT_COMMIT",
    "GIT_DIR",
    "GIT_WORK_TREE",
)

# The fixed wake prompt (verbatim from the brief). The first send-keys
# injection must carry this text exactly.
WAKE_PROMPT = (
    "Watchdog: read `consumer-task.md` in this channel and the `wd-arm` result "
    "line; if WAKE, begin that task; if ALREADY-CLAIMED or PRODUCER-STALLED, "
    "stop and report."
)

# tmux stub. Logs every invocation (one line, args space-joined) to $TMUX_LOG.
# Exits 0 by default; exits 1 for has-session/list-panes when
# TMUX_STUB_NO_PANE=1 (simulating an unresolved pane target); exits 1 for
# send-keys when TMUX_STUB_SEND_KEYS_FAIL=1 (simulating a TOCTOU failure
# between has-session and injection — pane dies, tmux server restarts).
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
  *)
    exit 0
    ;;
esac
"""


def _path_without_tmux():
    """A PATH that has git/bash and core utils but NO tmux anywhere.

    Used only for the tmux-missing precondition test (which exits before any git
    call). Builds a dir list from git/bash locations plus /usr/bin:/bin, de-dupes,
    and drops any dir that contains a `tmux` executable. Deterministic on any host.
    """
    dirs = []
    for tool in ("git", "bash"):
        p = shutil.which(tool)
        if p:
            d = os.path.dirname(p)
            if d not in dirs:
                dirs.append(d)
    for d in ("/usr/bin", "/bin"):
        if d not in dirs:
            dirs.append(d)
    out = []
    for d in dirs:
        if os.path.exists(os.path.join(d, "tmux")):
            continue
        out.append(d)
    return os.pathsep.join(out)


def run(args, cwd, env=None, timeout=30):
    merged = os.environ.copy()
    for key in ISOLATED_KEYS:
        merged.pop(key, None)
    if env:
        merged.update(env)
    return subprocess.run(
        args, cwd=str(cwd), text=True,
        capture_output=True, env=merged, check=False, timeout=timeout,
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


class WdPushTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self._spawned = []
        # A throwaway bin for the stub tmux + the invocation log path.
        self.stub_dir = pathlib.Path(self.tmp.name) / "stubbin"
        self.stub_dir.mkdir()
        self.tmux_bin = self.stub_dir / "tmux"
        self.tmux_bin.write_text(TMUX_STUB)
        self.tmux_bin.chmod(0o755)
        self.log = pathlib.Path(self.tmp.name) / "tmux.log"
        self.addCleanup(self._reap_spawned)
        self.addCleanup(self.tmp.cleanup)

    # ----- helpers ---------------------------------------------------------
    def _reap_spawned(self):
        """Disarm + kill any watcher left running if a test failed mid-flight."""
        try:
            run(["bash", str(DISARM), "--all"], self.repo, timeout=10)
        except Exception:
            pass
        for proc in self._spawned:
            if proc.poll() is None:
                proc.kill()
            try:
                proc.communicate(timeout=5)
            except Exception:
                try:
                    proc.communicate()
                except Exception:
                    pass

    def channel_dir(self, channel):
        return self.repo / ".git" / "live-monitor" / "channels" / channel

    def _stub_env(self, no_pane=False, send_keys_fail=False):
        # Stub dir FIRST so the stub shadows any real tmux further down PATH;
        # the real PATH is kept so git/dirname/etc. remain available.
        env = {
            "TMUX_LOG": str(self.log),
            "PATH": f"{self.stub_dir}:{os.environ.get('PATH', '')}",
        }
        if no_pane:
            env["TMUX_STUB_NO_PANE"] = "1"
        if send_keys_fail:
            env["TMUX_STUB_SEND_KEYS_FAIL"] = "1"
        return env

    def publish(self, channel="demo", stage="smoke", scope="README.md"):
        return run(
            ["bash", str(PUBLISH), "--channel", channel,
             "--stage", stage, "--scope", scope],
            self.repo,
        )

    def push(self, channel, pane, env=None, poll="1", timeout="10"):
        return run(
            ["bash", str(PUSH), "--channel", channel, "--pane", pane,
             "--poll-secs", str(poll), "--timeout-secs", str(timeout)],
            self.repo, env=env, timeout=30,
        )

    def status(self):
        return run(["bash", str(STATUS)], self.repo)

    def disarm(self, *extra):
        return run(["bash", str(DISARM), *extra], self.repo)

    def wait_for(self, fn, timeout_s=8.0, interval=0.2):
        """Poll fn() until it returns truthy or timeout_s elapses."""
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            if fn():
                return True
            time.sleep(interval)
        return False

    def _send_keys_lines(self):
        """All stub invocations whose arg-vector starts with `send-keys `."""
        if not self.log.exists():
            return []
        return [l for l in self.log.read_text().splitlines()
                if l.startswith("send-keys ")]

    # ----- 1. arg validation ----------------------------------------------
    def test_missing_args_exit_2(self):
        # Missing --pane.
        r = run(["bash", str(PUSH), "--channel", "demo"], self.repo,
                env={"PATH": _path_without_tmux()}, timeout=10)
        self.assertEqual(r.returncode, 2, r.stderr)
        # Missing --channel.
        r2 = run(["bash", str(PUSH), "--pane", "p:0.0"], self.repo,
                 env={"PATH": _path_without_tmux()}, timeout=10)
        self.assertEqual(r2.returncode, 2, r2.stderr)

    # ----- 2. tmux-missing precondition -----------------------------------
    def test_tmux_missing_exits_5(self):
        # PATH with no tmux anywhere (stub dir NOT included). The script exits at
        # the tmux precondition before any git call, so git's absence from this
        # trimmed PATH is fine.
        r = run(
            ["bash", str(PUSH), "--channel", "demo", "--pane", "p:0.0"],
            self.repo, env={"PATH": _path_without_tmux()}, timeout=10,
        )
        self.assertEqual(r.returncode, 5, r.stderr)
        self.assertIn("tmux not found", r.stderr)
        # No PATH-induced crash before the intended exit (the intended exit 5 +
        # message is itself evidence the precondition fired cleanly).

    # ----- 3. pane-not-found precondition ---------------------------------
    def test_pane_not_found_exits_6_no_injection(self):
        r = self.push("demo", "missing:0.0",
                      env=self._stub_env(no_pane=True), timeout=15)
        self.assertEqual(r.returncode, 6, r.stderr)
        self.assertIn("pane not found", r.stderr)
        self.assertIn("missing:0.0", r.stderr)
        # No send-keys injection occurred (the pane check failed first).
        self.assertEqual(self._send_keys_lines(), [])

    # ----- 4. WAKE -> two-call shim, exactly once --------------------------
    def test_wake_two_call_shim_exactly_once(self):
        pub = self.publish(channel="wake4", stage="smoke", scope="README.md")
        self.assertEqual(pub.returncode, 0, pub.stderr)
        head = git(self.repo, "rev-parse", "HEAD").stdout.strip()
        r = self.push("wake4", "sess:0.1", env=self._stub_env(), timeout=20)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.strip(), f"PUSHED {head}")
        # Exactly TWO send-keys calls.
        sk = self._send_keys_lines()
        self.assertEqual(len(sk), 2, sk)
        # First carries the fixed wake prompt (verbatim), addressed to the pane.
        self.assertTrue(sk[0].startswith("send-keys -t sess:0.1 "), sk[0])
        self.assertIn(WAKE_PROMPT, sk[0])
        # Second is exactly `send-keys -t <pane> Enter` — the trailing-Enter
        # half of the two-call shim.
        self.assertEqual(sk[1], "send-keys -t sess:0.1 Enter")
        # armed.json removed on the PUSHED exit path; wd-status shows no arm.
        self.assertFalse((self.channel_dir("wake4") / "armed.json").exists())
        st = self.status()
        self.assertNotIn("wake4 kind=", st.stdout)

    # ----- 5. exactly-once vs wd-arm (shared claim) -----------------------
    def test_second_push_already_claimed(self):
        self.publish(channel="once5", stage="smoke", scope="README.md")
        head = git(self.repo, "rev-parse", "HEAD").stdout.strip()
        first = self.push("once5", "s:0.0", env=self._stub_env(), timeout=20)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout.strip(), f"PUSHED {head}")
        sk_after_first = self._send_keys_lines()
        self.assertEqual(len(sk_after_first), 2, sk_after_first)
        # A second wd-push on the same head -> ALREADY-CLAIMED, no new injection.
        second = self.push("once5", "s:0.0", env=self._stub_env(), timeout=20)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(second.stdout.strip(), f"ALREADY-CLAIMED {head}")
        self.assertEqual(self._send_keys_lines(), sk_after_first)
        # Bonus: a wd-arm on the same already-claimed head also sees
        # ALREADY-CLAIMED — the atomic mkdir claim is shared across wake paths.
        arm = run(
            ["bash", str(ARM), "--channel", "once5",
             "--poll-secs", "1", "--timeout-secs", "5"],
            self.repo, timeout=15,
        )
        self.assertEqual(arm.returncode, 0, arm.stderr)
        self.assertEqual(arm.stdout.strip(), f"ALREADY-CLAIMED {head}")

    # ----- 6. disarm stands a push-watcher down ---------------------------
    def test_disarm_stands_down_push_watcher(self):
        merged = os.environ.copy()
        for k in ISOLATED_KEYS:
            merged.pop(k, None)
        merged.update(self._stub_env())
        proc = subprocess.Popen(
            ["bash", str(PUSH), "--channel", "disarm6", "--pane", "s:0.0",
             "--poll-secs", "1", "--timeout-secs", "60"],
            cwd=str(self.repo), text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=merged,
        )
        self._spawned.append(proc)
        armed = self.channel_dir("disarm6") / "armed.json"
        self.assertTrue(self.wait_for(lambda: armed.is_file(), timeout_s=6),
                        "push-watcher did not write armed.json in time")
        st = self.status()
        self.assertEqual(st.returncode, 0, st.stderr)
        self.assertIn("disarm6 kind=push-watcher", st.stdout)
        # Disarm writes the sentinel + best-effort kill; the loop (or TERM trap)
        # stands the watcher down.
        d = self.disarm("--channel", "disarm6")
        self.assertEqual(d.returncode, 0, d.stderr)
        self.assertIn("disarmed disarm6", d.stdout)
        try:
            out, _ = proc.communicate(timeout=8)
        except subprocess.TimeoutExpired:
            proc.kill()
            out, _ = proc.communicate()
            self.fail("wd-push did not exit after disarm")
        self.assertEqual(proc.returncode, 0, f"rc={proc.returncode} out={out!r}")
        self.assertIn("DISARMED", out)
        self.assertFalse(armed.exists(), "armed.json not removed on standdown")
        st2 = self.status()
        self.assertNotIn("disarm6 kind=", st2.stdout)

    # ----- 7. send-keys failure releases claim, exits 7 --------------------
    def test_send_keys_failure_releases_claim_exits_7(self):
        # On a won claim, if either tmux send-keys call returns non-zero
        # (reachable via TOCTOU between the has-session precondition and
        # injection — pane dies, tmux server restarts), wd-push must NOT print
        # PUSHED. It must RELEASE the shared exactly-once claim and exit 7 so
        # the default PULL wake path (wd-arm) can still fire on this head.
        # The loop runs under `set +e`, so this also proves send-keys exit codes
        # are captured explicitly rather than swallowed.
        self.publish(channel="fail7", stage="smoke", scope="README.md")
        head = git(self.repo, "rev-parse", "HEAD").stdout.strip()
        r = self.push("fail7", "sess:0.1",
                      env=self._stub_env(send_keys_fail=True), timeout=20)
        # Exit 7, no PUSHED on stdout, send-keys-failed diagnostic on stderr.
        self.assertEqual(r.returncode, 7, r.stderr)
        self.assertNotIn("PUSHED", r.stdout)
        self.assertIn("send-keys failed", r.stderr)
        # The shared exactly-once claim was released — claimed.<head> is gone.
        claimed = self.channel_dir("fail7") / f"claimed.{head}"
        self.assertFalse(claimed.exists(), "claim not released on send-keys failure")
        # The failed PUSH's armed record was cleaned up.
        self.assertFalse((self.channel_dir("fail7") / "armed.json").exists())
        # LOAD-BEARING consequence: a subsequent wd-arm (the default PULL wake
        # path) on the same channel/head now claims successfully and prints
        # WAKE — proving the failed PUSH did not poison the shared guard.
        arm = run(
            ["bash", str(ARM), "--channel", "fail7",
             "--poll-secs", "1", "--timeout-secs", "10"],
            self.repo, timeout=25,
        )
        self.assertEqual(arm.returncode, 0, arm.stderr)
        self.assertEqual(arm.stdout.strip(), f"WAKE {head}")


if __name__ == "__main__":
    unittest.main()
