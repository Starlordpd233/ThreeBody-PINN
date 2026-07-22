#!/usr/bin/env python3
"""P3: _session_from_env() prefers CODEX_THREAD_ID over CLAUDE_CODE_SESSION_ID."""
import importlib, os, pathlib, sys, unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "git_policy"))
import agent_presence  # noqa: E402

KEYS = ("CODEX_THREAD_ID", "CLAUDE_CODE_SESSION_ID")


class SessionFromEnvTests(unittest.TestCase):
    def setUp(self):
        self._saved = {k: os.environ.get(k) for k in KEYS}
        for k in KEYS:
            os.environ.pop(k, None)
        self.addCleanup(self._restore)
        importlib.reload(agent_presence)

    def _restore(self):
        for k, v in self._saved.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)

    def test_codex_id_wins_when_both_set(self):
        os.environ["CODEX_THREAD_ID"] = "codex-1"
        os.environ["CLAUDE_CODE_SESSION_ID"] = "claude-1"
        self.assertEqual(agent_presence._session_from_env(), "codex-1")

    def test_claude_id_used_when_codex_absent(self):
        os.environ["CLAUDE_CODE_SESSION_ID"] = "claude-1"
        self.assertEqual(agent_presence._session_from_env(), "claude-1")

    def test_uuid_codex_id_passes_safe_filter(self):
        os.environ["CODEX_THREAD_ID"] = "019f13c1-cfbc-7b73-a8b5-9f67d910532b"
        self.assertEqual(agent_presence._session_from_env(),
                         "019f13c1-cfbc-7b73-a8b5-9f67d910532b")

    def test_none_when_neither_set(self):
        self.assertIsNone(agent_presence._session_from_env())


if __name__ == "__main__":
    unittest.main()
