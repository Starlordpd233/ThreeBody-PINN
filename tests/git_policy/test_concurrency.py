#!/usr/bin/env python3
"""Tests for the parallel-agent concurrency tooling.

Covers the advisory claims board (agent_claims.py), the warn-on-edit auto-declare
hook (claim_guard.py), the agent-commit lock reclaim paths, and the session
banner. Every test isolates shared state in a throwaway git repo, so the live
claims board under the real repo's .git/agent-claims/ is never touched.
"""
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import time
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
GIT_POLICY = ROOT / "scripts" / "git_policy"
CLAIMS = GIT_POLICY / "agent_claims.py"
CLAIM_GUARD = GIT_POLICY / "claim_guard.py"
AGENT_COMMIT = ROOT / "scripts" / "agent-commit"
SESSION_BANNER = ROOT / "scripts" / "session_banner.sh"

# Agent identity / lock vars are stripped from the inherited environment so the
# parent session's identity never leaks into a temp-repo test.
ISOLATED_KEYS = (
    "AGENT_CLAIM_WHO",
    "AGENT_CLAIM_EXPIRY",
    "GIT_AGENT_ID",
    "GIT_AGENT_OWNED_PATHS",
    "GIT_AGENT_COMMIT",
    "AGENT_COMMIT_LOCK_TIMEOUT",
    "AGENT_COMMIT_LOCK_STALE",
)


def run(args, cwd, stdin=None, env=None):
    merged = os.environ.copy()
    for key in ISOLATED_KEYS:
        merged.pop(key, None)
    if env:
        merged.update(env)
    return subprocess.run(
        args,
        cwd=str(cwd),
        input=stdin,
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
    # abspath() and git's realpath toplevel agree (claim_guard relies on this).
    path = pathlib.Path(path).resolve()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    git(path, "config", "user.email", "test@example.com")
    git(path, "config", "user.name", "Test")
    return path


def claims(cwd, *args, env=None):
    return run([sys.executable, str(CLAIMS), *args], cwd, env=env)


def guard(cwd, file_path, session, env=None):
    payload = json.dumps({"session_id": session, "tool_input": {"file_path": file_path}})
    return run([sys.executable, str(CLAIM_GUARD)], cwd, stdin=payload, env=env)


class ClaimsBoardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def test_foreign_claim_conflicts(self):
        claims(self.repo, "claim", "sim/foo.py", "edit foo", env={"GIT_AGENT_ID": "A"})
        result = claims(self.repo, "check", "sim/foo.py", env={"GIT_AGENT_ID": "B"})
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertIn("held by A", result.stderr)

    def test_self_claim_does_not_conflict(self):
        claims(self.repo, "claim", "sim/foo.py", env={"GIT_AGENT_ID": "A"})
        result = claims(self.repo, "check", "sim/foo.py", env={"GIT_AGENT_ID": "A"})
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_release_clears_claim(self):
        claims(self.repo, "claim", "sim/foo.py", env={"GIT_AGENT_ID": "A"})
        claims(self.repo, "release", "sim/foo.py", env={"GIT_AGENT_ID": "A"})
        result = claims(self.repo, "check", "sim/foo.py", env={"GIT_AGENT_ID": "B"})
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_expired_claim_is_ignored(self):
        claims(self.repo, "claim", "sim/foo.py", env={"GIT_AGENT_ID": "A", "AGENT_CLAIM_EXPIRY": "0"})
        time.sleep(1)
        result = claims(self.repo, "check", "sim/foo.py", env={"GIT_AGENT_ID": "B", "AGENT_CLAIM_EXPIRY": "0"})
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_folder_claim_covers_inner_file(self):
        claims(self.repo, "claim", "sim", "own the folder", env={"GIT_AGENT_ID": "A"})
        result = claims(self.repo, "check", "sim/foo.py", env={"GIT_AGENT_ID": "B"})
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertIn("held by A", result.stderr)


class ClaimGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def test_auto_declare_then_foreign_warn(self):
        first = guard(self.repo, "sim/foo.py", "sess-A")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertNotIn("claim warning", first.stderr)
        second = guard(self.repo, "sim/foo.py", "sess-B")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("claim warning", second.stderr)

    def test_same_session_repeat_edit_no_warning(self):
        guard(self.repo, "sim/foo.py", "sess-A")
        again = guard(self.repo, "sim/foo.py", "sess-A")
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertNotIn("claim warning", again.stderr)

    def test_garbage_payload_exits_zero(self):
        result = run([sys.executable, str(CLAIM_GUARD)], self.repo, stdin="not json")
        self.assertEqual(result.returncode, 0, result.stderr)


class CommitLockTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        (self.repo / "file.txt").write_text("hello\n")
        git(self.repo, "add", "file.txt")
        self.lock = self.repo / ".git" / "agent-commit.lock"
        # Temp repo has no hooks, so the commit message is not policy-checked;
        # a bounded timeout keeps a wrongly-held lock from hanging the suite.
        self.env = {
            "GIT_AGENT_ID": "Tester",
            "GIT_AGENT_OWNED_PATHS": "file.txt",
            "AGENT_COMMIT_LOCK_TIMEOUT": "30",
        }

    def commit(self):
        return run(
            [
                "bash",
                str(AGENT_COMMIT),
                "-m",
                "chore(ref): add file",
                "-m",
                "Body line.",
                "-m",
                "Agent-Assisted-By: Tester",
            ],
            self.repo,
            env=self.env,
        )

    def test_reclaims_dead_holder_lock(self):
        # A lock left by a process that no longer exists must be reclaimed.
        dead = subprocess.Popen([sys.executable, "-c", "pass"])
        dead.wait()
        self.lock.mkdir(parents=True)
        (self.lock / "pid").write_text(f"{dead.pid}\n")
        (self.lock / "started").write_text(f"{int(time.time())}\n")
        result = self.commit()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("add file", git(self.repo, "log", "--oneline").stdout)

    def test_reclaims_stale_lock(self):
        # A lock older than the stale floor is reclaimed even if its pid is alive.
        self.lock.mkdir(parents=True)
        (self.lock / "pid").write_text(f"{os.getpid()}\n")  # this process: alive
        (self.lock / "started").write_text("0\n")  # epoch => far past the stale floor
        result = self.commit()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("add file", git(self.repo, "log", "--oneline").stdout)


class SessionBannerTests(unittest.TestCase):
    def test_reports_worktree_and_branch_in_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(tmp)
            (repo / "f").write_text("x\n")
            git(repo, "add", "f")
            git(repo, "commit", "-q", "-m", "init")
            result = run(["bash", str(SESSION_BANNER)], repo, stdin="")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertRegex(result.stdout.strip(), r"^worktree \S+ -> branch \S+")

    def test_silent_outside_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run(["bash", str(SESSION_BANNER)], tmp, stdin="")
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
