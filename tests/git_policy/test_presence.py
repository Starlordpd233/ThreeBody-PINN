#!/usr/bin/env python3
"""Tests for the advisory presence registry (agent_presence.py) and the
claims-board helpers it relies on (claims_for_who / release_by_who).

Every test isolates shared state in a throwaway git repo (cwd is chdir'd into
it), so the live presence registry and claims board under the real repo's .git/
are never touched. Identity/floor env vars are stripped per-test so the parent
session never leaks into a temp-repo assertion.
"""
import importlib
import os
import pathlib
import subprocess
import sys
import tempfile
import time
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
GIT_POLICY = ROOT / "scripts" / "git_policy"

ISOLATED_KEYS = (
    "AGENT_CLAIM_WHO",
    "AGENT_CLAIM_EXPIRY",
    "AGENT_PRESENCE_STALE",
    "CLAUDE_CODE_SESSION_ID",
    "CLAUDE_CODE_CHILD_SESSION",
    "GIT_AGENT_ID",
)

sys.path.insert(0, str(GIT_POLICY))
import agent_claims  # noqa: E402


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, check=False)


def init_repo(path):
    # .resolve() collapses the macOS /var -> /private/var symlink so cwd-based
    # abspath() and git's realpath toplevel agree.
    path = pathlib.Path(path).resolve()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    git(path, "config", "user.email", "test@example.com")
    git(path, "config", "user.name", "Test")
    return path


class PresenceTestBase(unittest.TestCase):
    """Temp git repo + cwd + env isolation, shared by all in-process tests."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        prev = os.getcwd()
        os.chdir(self.repo)
        self.addCleanup(lambda: os.chdir(prev))
        saved = {k: os.environ.get(k) for k in ISOLATED_KEYS}
        for k in ISOLATED_KEYS:
            os.environ.pop(k, None)

        def restore():
            for k, v in saved.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v

        self.addCleanup(restore)


class ClaimsByWhoTests(PresenceTestBase):
    def test_claims_for_who_returns_only_that_whos_areas(self):
        os.environ["AGENT_CLAIM_WHO"] = "session:A"
        agent_claims.claim("sim/a.py")
        agent_claims.claim("sim/b.py")
        os.environ["AGENT_CLAIM_WHO"] = "session:B"
        agent_claims.claim("pinn/c.py")
        self.assertEqual(agent_claims.claims_for_who("session:A"),
                         ["sim/a.py", "sim/b.py"])
        self.assertEqual(agent_claims.claims_for_who("session:B"), ["pinn/c.py"])

    def test_release_by_who_removes_only_that_whos_claims(self):
        os.environ["AGENT_CLAIM_WHO"] = "session:A"
        agent_claims.claim("sim/a.py")
        os.environ["AGENT_CLAIM_WHO"] = "session:B"
        agent_claims.claim("pinn/c.py")
        removed = agent_claims.release_by_who("session:A")
        self.assertEqual(removed, 1)
        self.assertEqual(agent_claims.claims_for_who("session:A"), [])
        self.assertEqual(agent_claims.claims_for_who("session:B"), ["pinn/c.py"])


if __name__ == "__main__":
    unittest.main()
