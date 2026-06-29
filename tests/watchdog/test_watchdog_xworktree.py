#!/usr/bin/env python3
"""Tests for the cross-session watchdog cross-worktree path (Phase 3).

Covers wd-integrate (B pulls A's done.head into its own branch) and the
wd-check --require-integration gate variant. Every test isolates shared state
in a throwaway git repo with two LINKED worktrees (main + a consumer worktree on
its own branch), so the live channel under the real repo's
.git/live-monitor/channels/ is never touched. The linked worktrees share one
object store and one git common dir, so both sides resolve the same channel root
— the same property Task 2.1 verified for the same-worktree resolver.
"""
import os
import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
WD = ROOT / "tools" / "watchdog"
PUBLISH = WD / "wd-publish-done"
CHECK = WD / "wd-check"
INTEGRATE = WD / "wd-integrate"

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


class WatchdogCrossWorktreeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        # Main worktree (producer A) and a linked worktree (consumer B) on its
        # own branch, placed as siblings so neither nests inside the other.
        self.main = init_repo(pathlib.Path(self.tmp.name) / "main")
        self.wt_b = pathlib.Path(self.tmp.name) / "wt_b"
        subprocess.run(
            ["git", "-C", str(self.main), "worktree", "add", "-q", "-b", "b-branch", str(self.wt_b)],
            check=True,
        )
        self.addCleanup(self.tmp.cleanup)

    def publish_from_main(self, channel="xwt", stage="smoke", scope="README.md"):
        return run(
            ["bash", str(PUBLISH), "--channel", channel, "--stage", stage, "--scope", scope],
            self.main,
        )

    def check_b(self, channel="xwt", *extra):
        return run(["bash", str(CHECK), "--channel", channel, *extra], self.wt_b)

    def integrate_b(self, channel="xwt"):
        return run(["bash", str(INTEGRATE), "--channel", channel], self.wt_b)

    def _a_advances_readme(self):
        (self.main / "README.md").write_text("hello\nA\n")
        git(self.main, "commit", "-q", "-am", "a-work")

    # (a) before integration, A's head is not in B's history -> STALE:not-integrated.
    def test_not_integrated_is_stale(self):
        self._a_advances_readme()
        pub = self.publish_from_main()
        self.assertEqual(pub.returncode, 0, pub.stderr)
        chk = self.check_b("xwt", "--require-integration")
        self.assertEqual(chk.returncode, 20, chk.stderr)
        self.assertEqual(chk.stdout.strip(), "STALE:not-integrated")

    # (b) wd-integrate merges A's head; the gate then returns WAKE.
    def test_integrate_then_wake(self):
        self._a_advances_readme()
        self.publish_from_main()
        # Pre-integration: stale.
        self.assertEqual(
            self.check_b("xwt", "--require-integration").stdout.strip(), "STALE:not-integrated"
        )
        integ = self.integrate_b()
        self.assertEqual(integ.returncode, 0, integ.stderr)
        self.assertIn("integrated", integ.stdout)
        # Post-integration: WAKE.
        chk = self.check_b("xwt", "--require-integration")
        self.assertEqual(chk.returncode, 0, chk.stderr)
        self.assertEqual(chk.stdout.strip(), "WAKE")

    # (c) a second integrate once A's head is already in B is a no-op.
    def test_already_integrated(self):
        self._a_advances_readme()
        self.publish_from_main()
        self.integrate_b()
        again = self.integrate_b()
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertIn("already-integrated", again.stdout)

    # (d) a conflicting B-side change -> wd-integrate aborts cleanly
    #     (exit 4, no half-merge: MERGE_HEAD absent, working tree clean).
    def test_conflict_aborts_cleanly(self):
        # B diverges with a conflicting edit to the same line.
        (self.wt_b / "README.md").write_text("hello\nB\n")
        git(self.wt_b, "commit", "-q", "-am", "b-work")
        # A diverges with a conflicting edit to the same line.
        self._a_advances_readme()
        self.publish_from_main()
        integ = self.integrate_b()
        self.assertEqual(integ.returncode, 4, integ.stdout + integ.stderr)
        self.assertIn("CONFLICT", integ.stderr)
        # No half-merge left behind: MERGE_HEAD must be absent.
        merge_head = git(self.wt_b, "rev-parse", "--verify", "-q", "MERGE_HEAD")
        self.assertNotEqual(merge_head.returncode, 0, "MERGE_HEAD still present after abort")
        # ...and the worktree must be clean.
        status = git(self.wt_b, "status", "--porcelain")
        self.assertEqual(status.stdout.strip(), "", f"worktree dirty after abort: {status.stdout}")


if __name__ == "__main__":
    unittest.main()
