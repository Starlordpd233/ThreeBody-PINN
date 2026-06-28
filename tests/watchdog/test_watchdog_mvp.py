#!/usr/bin/env python3
"""Tests for the cross-session watchdog MVP (Phase 2: same-worktree path).

Covers the channel resolver (wd-common.sh), the producer (wd-publish-done),
the consumer staleness gate (wd-check), and the consumer watcher + exactly-once
claim + dead-producer timeout (wd-arm). Every test isolates shared state in a
throwaway git repo, so the live channel under the real repo's
.git/live-monitor/channels/ is never touched.
"""
import os
import pathlib
import shlex
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
WD = ROOT / "tools" / "watchdog"
COMMON = WD / "lib" / "wd-common.sh"
PUBLISH = WD / "wd-publish-done"
CHECK = WD / "wd-check"
ARM = WD / "wd-arm"

# Git/agent vars that could leak the parent session's repo or identity into a
# temp-repo test are stripped from the inherited environment.
ISOLATED_KEYS = (
    "GIT_AGENT_ID",
    "GIT_AGENT_OWNED_PATHS",
    "GIT_AGENT_COMMIT",
    "GIT_DIR",
    "GIT_WORK_TREE",
)


def run(args, cwd, env=None):
    merged = os.environ.copy()
    for key in ISOLATED_KEYS:
        merged.pop(key, None)
    if env:
        merged.update(env)
    return subprocess.run(
        args,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        env=merged,
        check=False,
    )


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
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


class WatchdogMvpTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def publish(self, channel="demo", stage="smoke", scope="README.md"):
        return run(
            ["bash", str(PUBLISH), "--channel", channel, "--stage", stage, "--scope", scope],
            self.repo,
        )

    def check(self, channel="demo", *extra):
        return run(["bash", str(CHECK), "--channel", channel, *extra], self.repo)

    def arm(self, channel="demo", poll="1", timeout="5", *extra):
        return run(
            ["bash", str(ARM), "--channel", channel,
             "--poll-secs", poll, "--timeout-secs", timeout, *extra],
            self.repo,
        )

    # (f) resolver returns an absolute path under the shared common dir.
    def test_resolver_returns_absolute_path(self):
        result = run(["bash", "-c", f"source {shlex.quote(str(COMMON))}; wd_channel_root"], self.repo)
        self.assertEqual(result.returncode, 0, result.stderr)
        root = result.stdout.strip()
        self.assertTrue(root.startswith("/"), root)
        self.assertEqual(root, str(self.repo / ".git" / "live-monitor" / "channels"))

    # (a) publish -> check returns WAKE.
    def test_publish_then_check_wakes(self):
        pub = self.publish()
        self.assertEqual(pub.returncode, 0, pub.stderr)
        self.assertIn("published done @", pub.stdout)
        chk = self.check()
        self.assertEqual(chk.returncode, 0, chk.stderr)
        self.assertEqual(chk.stdout.strip(), "WAKE")

    # (b) producer advances past the marked head within scope -> STALE.
    def test_producer_advanced_is_stale(self):
        self.publish()
        (self.repo / "README.md").write_text("hello\nmore\n")
        git(self.repo, "commit", "-q", "-am", "advance")
        chk = self.check()
        self.assertEqual(chk.returncode, 20, chk.stderr)
        self.assertEqual(chk.stdout.strip(), "STALE:producer-advanced")

    # (c) dirty scope -> publish refused with exit 3.
    def test_dirty_scope_refuses_publish(self):
        (self.repo / "README.md").write_text("hello\ndirty\n")  # uncommitted
        pub = self.publish()
        self.assertEqual(pub.returncode, 3, pub.stdout)
        self.assertIn("refusing to publish", pub.stderr)

    # (d) exactly-once: a second wd-arm on the same head -> ALREADY-CLAIMED.
    def test_arm_claims_once(self):
        self.publish()
        first = self.arm()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertTrue(first.stdout.startswith("WAKE "), first.stdout)
        second = self.arm()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertTrue(second.stdout.startswith("ALREADY-CLAIMED "), second.stdout)

    # (e) dead-producer guard: no done marker within the timeout -> exit 42.
    def test_arm_timeout_producer_stalled(self):
        result = self.arm(channel="none", poll="1", timeout="1")
        self.assertEqual(result.returncode, 42, result.stderr)
        self.assertIn("PRODUCER-STALLED", result.stdout)

    # Bonus: --task-file persists the task to the channel at arm time.
    def test_arm_persists_task_file(self):
        (self.repo / "task.md").write_text("# B task\nDo the thing.\n")
        result = self.arm("tf", "1", "1", "--task-file", "task.md")
        self.assertEqual(result.returncode, 42, result.stderr)  # no done -> times out
        task = self.repo / ".git" / "live-monitor" / "channels" / "tf" / "consumer-task.md"
        self.assertTrue(task.is_file(), "consumer-task.md not written at arm time")
        self.assertEqual(task.read_text(), "# B task\nDo the thing.\n")

    # A missing --task-file must NOT kill the arm: it warns and arms anyway, so a
    # bad path can't silently prevent the watcher from running.
    def test_arm_missing_task_file_still_arms(self):
        result = self.arm("none2", "1", "1", "--task-file", "does-not-exist.md")
        self.assertEqual(result.returncode, 42, result.stderr)  # armed, then timed out
        self.assertIn("not found", result.stderr)
        self.assertIn("arming without", result.stderr)


if __name__ == "__main__":
    unittest.main()
