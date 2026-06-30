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


class UnitGapTests(unittest.TestCase):

    # T1-a — concurrent claim race at unit fidelity. The exactly-once claim is a
    # single atomic `mkdir claimed.<head>` shared by every wake path (identical
    # line in wd-arm and wd-push), so N racing wd-arm processes prove the primitive.
    def test_b1_concurrent_claim_exactly_once(self):
        import concurrent.futures
        with tempfile.TemporaryDirectory() as d:
            repo = init_repo(pathlib.Path(d) / "proj")
            self.assertEqual(
                run([PUBLISH, "--channel", "c", "--stage", "s", "--scope", "README.md"],
                    cwd=repo).returncode, 0)
            N = 4

            def arm_once():
                return run([ARM, "--channel", "c", "--poll-secs", "1", "--timeout-secs", "15"],
                           cwd=repo, timeout=30)

            with concurrent.futures.ThreadPoolExecutor(max_workers=N) as ex:
                results = [f.result() for f in [ex.submit(arm_once) for _ in range(N)]]
            verdicts = [first_token(r) for r in results]
            self.assertEqual(verdicts.count("WAKE"), 1, f"not exactly one WAKE: {verdicts}")
            self.assertEqual(verdicts.count("ALREADY-CLAIMED"), N - 1, f"{verdicts}")
            claims = list((repo / ".git/live-monitor/channels/c").glob("claimed.*"))
            self.assertEqual(len(claims), 1, f"expected one claim dir: {claims}")

    # T1-b — non-git CWD must fail safely (defined non-zero exit + a diagnostic),
    # not hang or dump a confusing trace. wd-check is one-shot (cannot hang).
    def test_b2_non_git_cwd_fails_safely(self):
        with tempfile.TemporaryDirectory() as d:
            proc = run([CHECK, "--channel", "x"], cwd=d, timeout=20)
            self.assertNotEqual(proc.returncode, 0,
                                "wd-check unexpectedly succeeded outside a git repo")
            self.assertTrue((proc.stderr or proc.stdout).strip(),
                            "no diagnostic emitted outside a git repo")
            # FINDING gate (design T1-b / T4.4): a watchdog-identifiable message is
            # preferred over git's bare 'fatal: not a git repository'. If only the
            # bare git message appears, record a LOW-severity UX finding. PASS here
            # requires only: non-zero exit + some diagnostic + no hang.

    # T1-c — the resolver keys the channel to the CWD's repo, even when the tool is
    # invoked by absolute path from a different repo (the global-install case).
    def test_b3_resolver_uses_cwd_not_tool_home(self):
        with tempfile.TemporaryDirectory() as d:
            repo = init_repo(pathlib.Path(d) / "proj")
            pub = run([PUBLISH, "--channel", "c", "--stage", "s", "--scope", "README.md"], cwd=repo)
            self.assertEqual(pub.returncode, 0, pub.stderr)
            chan = repo / ".git" / "live-monitor" / "channels" / "c"
            self.assertTrue((chan / "done.json").exists(),
                            "done.json not under CWD repo's .git; resolver used tool home")
            chk = run([CHECK, "--channel", "c"], cwd=repo)
            self.assertEqual(first_token(chk), "WAKE",
                             f"rc={chk.returncode} out={chk.stdout!r} err={chk.stderr!r}")

    # T1-d — claim dirs accumulate one-per-distinct-head; a NEW head still wakes
    # despite prior claims (claims never block a future head). Documents the
    # housekeeping contract grounded in the per-head claim mechanism.
    def test_b4_claim_dirs_accumulate_and_rewake(self):
        with tempfile.TemporaryDirectory() as d:
            repo = init_repo(pathlib.Path(d) / "proj")
            chan = repo / ".git/live-monitor/channels/c"
            seen = []
            for i in range(3):
                (repo / f"f{i}.txt").write_text("x\n")
                git(repo, "add", f"f{i}.txt")
                git(repo, "commit", "-q", "-m", f"c{i}")
                head = git(repo, "rev-parse", "HEAD").stdout.strip()
                run([PUBLISH, "--channel", "c", "--stage", "s", "--scope", f"f{i}.txt"], cwd=repo)
                arm = run([ARM, "--channel", "c", "--poll-secs", "1", "--timeout-secs", "10"],
                          cwd=repo, timeout=20)
                self.assertEqual(first_token(arm), "WAKE",
                                 f"head {i}: out={arm.stdout!r} err={arm.stderr!r}")
                seen.append(head)
            dirs = sorted(p.name for p in chan.glob("claimed.*"))
            self.assertEqual(dirs, sorted(f"claimed.{h}" for h in seen),
                             "expected exactly one claimed.<head> per distinct head")

    # T1-e — disarm tolerates a dead pid (best-effort kill of a gone process) with
    # exit 0 and removes the record. The reused-pid hazard (kill could signal an
    # unrelated reborn pid) is a documented LOW nit, not exercised destructively.
    def test_b5_disarm_tolerates_dead_pid(self):
        with tempfile.TemporaryDirectory() as d:
            repo = init_repo(pathlib.Path(d) / "proj")
            chan = repo / ".git/live-monitor/channels/c"
            chan.mkdir(parents=True)
            dead = 2**31 - 1  # out-of-range pid; kill -0 fails cleanly
            (chan / "armed.json").write_text(
                '{"kind":"watcher","channel":"c","armed_at":0,"ttl":null,'
                f'"armed_by":"x","pid":{dead}}}\n')
            dis = run([DISARM, "--channel", "c"], cwd=repo)
            self.assertEqual(dis.returncode, 0, dis.stderr)
            self.assertFalse((chan / "armed.json").exists(), "armed.json not removed")