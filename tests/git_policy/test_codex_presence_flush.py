#!/usr/bin/env python3
"""P0/P2: heartbeat on every PostToolUse; flush a staged announce when present."""
import json, os, pathlib, subprocess, sys, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
GIT_POLICY = ROOT / "scripts" / "git_policy"
FLUSH = GIT_POLICY / "codex_presence_flush.py"
PRESENCE = GIT_POLICY / "agent_presence.py"
ISOLATED = ("AGENT_CLAIM_WHO", "AGENT_PRESENCE_STALE", "CODEX_THREAD_ID",
            "CLAUDE_CODE_SESSION_ID", "GIT_AGENT_ID")


def run(args, cwd, stdin=None, env=None):
    merged = os.environ.copy()
    for k in ISOLATED:
        merged.pop(k, None)
    if env:
        merged.update(env)
    return subprocess.run(args, cwd=str(cwd), input=stdin, text=True,
                          capture_output=True, env=merged, check=False)


def init_repo(path):
    path = pathlib.Path(path).resolve()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "t@e.com"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "T"], check=True)
    return path


def presence_entry(repo, sid, env):
    out = run([sys.executable, "-c",
               f"import sys;sys.path.insert(0,{str(GIT_POLICY)!r});import agent_presence,"
               f"agent_claims,json;print(json.dumps(agent_claims.load("
               f"agent_presence.presence_file({sid!r}))))"], repo, env=env).stdout.strip()
    return json.loads(out) if out and out != "null" else None


class FlushTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.staging = pathlib.Path(self.tmp.name).resolve() / "stg"
        self.staging.mkdir()
        self.env = {"TMPDIR": str(self.staging.parent)}  # staging dir = $TMPDIR/agent-presence-staging
        self.sdir = self.staging.parent / "agent-presence-staging"

    def _register(self, sid):
        # The CLI `register` ignores argv — main() resolves identity from env/stdin,
        # so `agent-presence register <sid>` drops <sid> and registers nothing. Call
        # the Python API with the explicit sid (mirrors tests/git_policy/test_presence.py).
        # env still carries TMPDIR so the shared presence dir resolves inside the temp repo.
        run([sys.executable, "-c",
             f"import sys;sys.path.insert(0,{str(GIT_POLICY)!r});"
             f"import agent_presence,os;agent_presence.register({sid!r},pid=os.getpid())"],
            self.repo, env=self.env)

    def _flush(self, sid):
        return run([sys.executable, str(FLUSH)], self.repo,
                   stdin=json.dumps({"session_id": sid, "tool_name": "Bash"}), env=self.env)

    def test_heartbeat_bumps_when_registered(self):
        self._register("S1")
        before = presence_entry(self.repo, "S1", self.env)["last_heartbeat"]
        import time
        time.sleep(1)
        self.assertEqual(self._flush("S1").returncode, 0)
        after = presence_entry(self.repo, "S1", self.env)["last_heartbeat"]
        self.assertGreater(after, before)

    def test_noop_when_not_registered(self):
        r = self._flush("ghost")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIsNone(presence_entry(self.repo, "ghost", self.env))

    def test_flush_applies_staged_announce_and_deletes_file(self):
        self._register("S2")
        self.sdir.mkdir(parents=True, exist_ok=True)
        (self.sdir / "S2.json").write_text(json.dumps(
            {"session_id": "S2", "summary": "build the thing", "areas": ["sim/x.py"]}))
        self.assertEqual(self._flush("S2").returncode, 0)
        entry = presence_entry(self.repo, "S2", self.env)
        self.assertEqual(entry["task_summary"], "build the thing")
        self.assertFalse((self.sdir / "S2.json").exists())

    def test_double_flush_is_idempotent(self):
        self._register("S3")
        self.sdir.mkdir(parents=True, exist_ok=True)
        (self.sdir / "S3.json").write_text(json.dumps(
            {"session_id": "S3", "summary": "x", "areas": ["a.py"]}))
        self.assertEqual(self._flush("S3").returncode, 0)
        self.assertEqual(self._flush("S3").returncode, 0)  # Stop fired twice → no error

    def test_garbage_stdin_exits_zero(self):
        self.assertEqual(run([sys.executable, str(FLUSH)], self.repo, stdin="nope",
                             env=self.env).returncode, 0)

    def test_valid_json_wrong_shape_exits_zero(self):
        # Fail-open: valid JSON that is not the documented payload object shape
        # must still exit 0 (plan constraint: hooks never block).
        for blob in ("[]", "null", "42", '"nope"', '{"session_id": 123}'):
            r = run([sys.executable, str(FLUSH)], self.repo, stdin=blob, env=self.env)
            self.assertEqual(r.returncode, 0, f"{blob!r}: {r.stderr}")


if __name__ == "__main__":
    unittest.main()
