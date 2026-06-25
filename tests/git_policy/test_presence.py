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


class RegisterSweepTests(PresenceTestBase):
    def _load(self, sid):
        import agent_presence
        return agent_claims.load(agent_presence.presence_file(sid))

    def test_register_writes_schema_with_live_pid(self):
        import agent_presence
        agent_presence.register("sid-1", pid=os.getpid())
        entry = self._load("sid-1")
        self.assertEqual(entry["session_id"], "sid-1")
        self.assertEqual(entry["pid"], os.getpid())
        self.assertIsNone(entry["task_summary"])
        self.assertIn("start_time", entry)
        self.assertIn("last_heartbeat", entry)

    def test_register_is_idempotent_and_preserves_summary(self):
        import agent_presence
        agent_presence.register("sid-1", pid=os.getpid())
        path = agent_presence.presence_file("sid-1")
        entry = agent_claims.load(path)
        entry["task_summary"] = "do the thing"
        entry["start_time"] = 111
        agent_presence._atomic_write(path, entry)
        agent_presence.register("sid-1", pid=os.getpid())  # re-register (resume)
        again = self._load("sid-1")
        self.assertEqual(again["task_summary"], "do the thing")
        self.assertEqual(again["start_time"], 111)

    def test_sweep_keeps_live_pid_even_when_heartbeat_old(self):
        import agent_presence
        os.environ["AGENT_PRESENCE_STALE"] = "0"  # floor would reap if applied
        agent_presence.register("sid-live", pid=os.getpid())
        path = agent_presence.presence_file("sid-live")
        entry = agent_claims.load(path)
        entry["last_heartbeat"] = 0  # ancient
        agent_presence._atomic_write(path, entry)
        agent_presence.sweep_presence()
        self.assertIsNotNone(self._load("sid-live"))  # live pid => kept

    def test_sweep_reaps_dead_pid_past_floor_and_releases_claims(self):
        import agent_presence
        os.environ["AGENT_PRESENCE_STALE"] = "0"  # collapse the floor
        dead = subprocess.Popen([sys.executable, "-c", "pass"])
        dead.wait()  # pid now dead
        os.environ["AGENT_CLAIM_WHO"] = agent_presence.who_key("sid-dead")
        agent_claims.claim("sim/owned.py")
        os.environ.pop("AGENT_CLAIM_WHO", None)
        agent_presence.register("sid-dead", pid=dead.pid)
        path = agent_presence.presence_file("sid-dead")
        entry = agent_claims.load(path)
        entry["last_heartbeat"] = 0  # ancient -> past the (zero) floor
        agent_presence._atomic_write(path, entry)
        agent_presence.sweep_presence()
        self.assertIsNone(self._load("sid-dead"))                     # reaped
        self.assertEqual(agent_claims.claims_for_who(
            agent_presence.who_key("sid-dead")), [])                  # claims released

    def test_sweep_keeps_dead_pid_within_floor(self):
        # A transient SessionStart shell pid dies immediately; an actively
        # heartbeating session must survive (untrusted pid -> floor, not reap).
        import agent_presence
        dead = subprocess.Popen([sys.executable, "-c", "pass"])
        dead.wait()
        agent_presence.register("sid-untrusted", pid=dead.pid)  # dead nonzero pid
        # last_heartbeat is fresh (register set it); default 20-min floor applies
        agent_presence.sweep_presence()
        self.assertIsNotNone(self._load("sid-untrusted"))  # kept by the floor grace

    def test_sweep_reaps_pidless_entry_past_floor(self):
        import agent_presence
        os.environ["AGENT_PRESENCE_STALE"] = "0"
        agent_presence.register("sid-x", pid=os.getpid())
        path = agent_presence.presence_file("sid-x")
        entry = agent_claims.load(path)
        entry["pid"] = None          # untrusted/absent pid
        entry["last_heartbeat"] = 0  # past the (zero) floor
        agent_presence._atomic_write(path, entry)
        agent_presence.sweep_presence()
        self.assertIsNone(self._load("sid-x"))

    def test_register_without_identity_is_silent(self):
        import agent_presence
        self.assertEqual(agent_presence.register(None), "")  # no env, no arg


class FormattingTests(PresenceTestBase):
    def test_roster_formatting(self):
        import agent_presence
        agent_presence.register("sid-A", pid=100)
        os.environ["AGENT_CLAIM_WHO"] = agent_presence.who_key("sid-A")
        agent_claims.claim("sim/a.py")
        agent_claims.claim("pinn/c.py")
        agent_presence.register("sid-B", pid=101)  # no claims
        
        # Test roster format output
        out = agent_presence.format_roster()
        self.assertIn("sid-A", out)
        self.assertIn("sid-B", out)
        self.assertIn("pinn/c.py, sim/a.py", out)

    def test_task_summary_read_write(self):
        import agent_presence
        agent_presence.register("sid-1")
        agent_presence.set_task_summary("sid-1", "investigate test failures")
        
        path = agent_presence.presence_file("sid-1")
        entry = agent_claims.load(path)
        self.assertEqual(entry["task_summary"], "investigate test failures")
        
        out = agent_presence.format_roster()
        self.assertIn("investigate test failures", out)


if __name__ == "__main__":
    unittest.main()
