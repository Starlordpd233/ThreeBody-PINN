#!/usr/bin/env python3
"""P2: announce shim stages summary+areas; flush consumes them (V5 round-trip)."""
import json, os, pathlib, subprocess, sys, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SHIM = ROOT / "scripts" / "agent-codex-announce"
GIT_POLICY = ROOT / "scripts" / "git_policy"
FLUSH = GIT_POLICY / "codex_presence_flush.py"
PRESENCE = GIT_POLICY / "agent_presence.py"
ISOLATED = ("AGENT_CLAIM_WHO", "CODEX_THREAD_ID", "CLAUDE_CODE_SESSION_ID", "GIT_AGENT_ID")


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


class AnnounceShimTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.tmpdir = pathlib.Path(self.tmp.name).resolve()
        self.env = {"TMPDIR": str(self.tmpdir), "CODEX_THREAD_ID": "S-Z"}
        self.staged = self.tmpdir / "agent-presence-staging" / "S-Z.json"

    def test_shim_writes_staging_payload(self):
        r = run(["bash", str(SHIM), "do the work", "--areas", "sim/a.py,sim/b.py"],
                self.repo, env=self.env)
        self.assertEqual(r.returncode, 0, r.stderr)
        body = json.loads(self.staged.read_text())
        self.assertEqual(body["session_id"], "S-Z")
        self.assertEqual(body["summary"], "do the work")
        self.assertEqual(body["areas"], ["sim/a.py", "sim/b.py"])

    def test_round_trip_announce_then_flush(self):
        # Register via the Python API (the CLI `register` ignores argv — see Task 3).
        run([sys.executable, "-c",
             "import sys;sys.path.insert(0,%r);import agent_presence,os;"
             "agent_presence.register('S-Z',pid=os.getpid())" % str(GIT_POLICY)],
            self.repo, env=self.env)
        run(["bash", str(SHIM), "round trip", "--areas", "sim/a.py"], self.repo, env=self.env)
        run([sys.executable, str(FLUSH)], self.repo,
            stdin=json.dumps({"session_id": "S-Z"}), env=self.env)
        self.assertFalse(self.staged.exists())  # consumed by flush
        # V5 lock: the announce actually landed on the roster entry (guards against
        # a vacuous pass where the shim never wrote and flush never applied anything).
        out = run([sys.executable, "-c",
                   "import sys,json;sys.path.insert(0,%r);import agent_presence,agent_claims;"
                   "print(json.dumps(agent_claims.load(agent_presence.presence_file('S-Z'))))"
                   % str(GIT_POLICY)], self.repo, env=self.env).stdout.strip()
        entry = json.loads(out)
        self.assertEqual(entry["task_summary"], "round trip")

    def test_missing_thread_id_exits_zero_no_file(self):
        r = run(["bash", str(SHIM), "x", "--areas", "a.py"], self.repo,
                env={"TMPDIR": str(self.tmpdir)})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(self.staged.exists())


if __name__ == "__main__":
    unittest.main()
