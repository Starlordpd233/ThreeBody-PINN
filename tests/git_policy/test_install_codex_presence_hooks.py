#!/usr/bin/env python3
"""Installer merges guarded presence hooks into ~/.codex/hooks.json idempotently."""
import json, os, pathlib, subprocess, sys, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
INSTALLER = ROOT / "scripts" / "git_policy" / "install_codex_presence_hooks.py"


def run(target, args=()):
    env = os.environ.copy()
    env["CODEX_HOOKS_FILE"] = str(target)
    return subprocess.run([sys.executable, str(INSTALLER), *args],
                          text=True, capture_output=True, env=env, check=False)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.target = pathlib.Path(self.tmp.name) / ".codex" / "hooks.json"

    def _events(self):
        return json.loads(self.target.read_text())["hooks"]

    def test_creates_file_with_four_events(self):
        self.assertEqual(run(self.target).returncode, 0)
        ev = self._events()
        for name in ("SessionStart", "PreToolUse", "PostToolUse", "Stop"):
            self.assertIn(name, ev)

    def test_commands_are_guarded_and_path_free(self):
        run(self.target)
        blob = self.target.read_text()
        # Assert against the decoded command strings, not the raw JSON text —
        # json.dump escapes inner double quotes, so a raw-text substring match
        # on '[ -f "$s" ]' can never succeed.
        doc = json.loads(blob)
        ours = [h["command"]
                for groups in doc["hooks"].values()
                for g in groups
                for h in g["hooks"]
                if h.get("statusMessage", "").startswith("aps:")]
        self.assertEqual(len(ours), 4)
        for cmd in ours:
            self.assertIn("git rev-parse --path-format=absolute --git-common-dir", cmd)
            self.assertIn('[ -f "$s" ] || exit 0', cmd)
        self.assertNotIn("/Users/", blob)  # no hardcoded absolute paths

    def test_preserves_existing_foreign_handler(self):
        self.target.parent.mkdir(parents=True)
        self.target.write_text(json.dumps({"hooks": {"PostToolUse": [
            {"matcher": ".*", "hooks": [{"type": "command", "command": "echo claude-mem",
                                         "statusMessage": "claude-mem"}]}]}}))
        run(self.target)
        post = self._events()["PostToolUse"]
        msgs = [h["statusMessage"] for g in post for h in g["hooks"]]
        self.assertIn("claude-mem", msgs)          # foreign handler kept
        self.assertTrue(any(m.startswith("aps:") for m in msgs))  # ours added

    def test_idempotent_no_duplicate_groups(self):
        run(self.target)
        run(self.target)
        post = self._events()["PostToolUse"]
        aps_groups = [g for g in post
                      if any(h.get("statusMessage", "").startswith("aps:") for h in g["hooks"])]
        self.assertEqual(len(aps_groups), 1)

    def test_sessionstart_stop_postooluse_omit_matcher(self):
        # Real Codex global hooks (~/.codex/hooks.json, verified 2026-06-30) carry no
        # matcher for these events. A "startup|resume" value is Claude-Code vocabulary
        # and would never match Codex SessionStart, silently breaking roster registration.
        run(self.target)
        ev = self._events()
        for event in ("SessionStart", "Stop", "PostToolUse"):
            for g in ev[event]:
                self.assertNotIn("matcher", g, f"{event} group must omit matcher")
        # PreToolUse is the only event that must restrict firing, and only to apply_patch.
        self.assertEqual([g.get("matcher") for g in ev["PreToolUse"]], ["apply_patch"])

    def test_pretooluse_narrowed_to_apply_patch(self):
        # Edit/Write are not Codex tool names (probe F4) and codex_claim_guard only
        # parses tool_input.command (apply_patch bodies); the matcher must not advertise
        # broader coverage than the guard can deliver.
        run(self.target)
        blob = self.target.read_text()
        self.assertIn('"apply_patch"', blob)
        self.assertNotIn("Edit|Write", blob)


if __name__ == "__main__":
    unittest.main()
