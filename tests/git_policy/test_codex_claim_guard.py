#!/usr/bin/env python3
"""P1: codex_claim_guard parses apply_patch bodies and auto-declares write areas."""
import json, os, pathlib, subprocess, sys, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
GIT_POLICY = ROOT / "scripts" / "git_policy"
GUARD = GIT_POLICY / "codex_claim_guard.py"
CLAIMS = GIT_POLICY / "agent_claims.py"
ISOLATED = ("AGENT_CLAIM_WHO", "AGENT_CLAIM_EXPIRY", "GIT_AGENT_ID", "CODEX_THREAD_ID")


def run(args, cwd, stdin=None):
    env = os.environ.copy()
    for k in ISOLATED:
        env.pop(k, None)
    return subprocess.run(args, cwd=str(cwd), input=stdin, text=True,
                          capture_output=True, env=env, check=False)


def init_repo(path):
    path = pathlib.Path(path).resolve()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "t@e.com"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "T"], check=True)
    return path


def patch(*body_lines):
    return "*** Begin Patch\n" + "\n".join(body_lines) + "\n*** End Patch\n"


def edit(repo, command, session, cwd=None):
    payload = json.dumps({"session_id": session, "cwd": str(cwd or repo),
                          "tool_name": "apply_patch",
                          "tool_input": {"command": command}})
    return run([sys.executable, str(GUARD)], repo, stdin=payload)


def claimed_areas(repo, who):
    # Read the board directly via agent_claims to assert exact areas.
    out = run([sys.executable, "-c",
               f"import sys;sys.path.insert(0,{str(GIT_POLICY)!r});"
               "import agent_claims,os;print('\\n'.join(agent_claims.claims_for_who("
               f"{who!r})))"], repo).stdout
    return sorted(x for x in out.splitlines() if x)


class CodexClaimGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def test_add_file_is_claimed(self):
        r = edit(self.repo, patch("*** Add File: sim/foo.py", "+x"), "S-A")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(claimed_areas(self.repo, "session:S-A"), ["sim/foo.py"])

    def test_update_file_is_claimed(self):
        edit(self.repo, patch("*** Update File: sim/foo.py", "@@", "+x"), "S-A")
        self.assertEqual(claimed_areas(self.repo, "session:S-A"), ["sim/foo.py"])

    def test_delete_file_is_claimed(self):
        edit(self.repo, patch("*** Delete File: sim/foo.py"), "S-A")
        self.assertEqual(claimed_areas(self.repo, "session:S-A"), ["sim/foo.py"])

    def test_rename_claims_both_old_and_new(self):
        edit(self.repo, patch("*** Update File: a.py", "*** Move to: b.py", "@@", "+x"), "S-A")
        self.assertEqual(claimed_areas(self.repo, "session:S-A"), ["a.py", "b.py"])

    def test_multifile_patch_claims_all(self):
        edit(self.repo, patch("*** Add File: a.py", "+1",
                              "*** Update File: sub/b.py", "@@", "+2"), "S-A")
        self.assertEqual(claimed_areas(self.repo, "session:S-A"), ["a.py", "sub/b.py"])

    def test_cwd_relative_path_resolves_repo_relative(self):
        # cwd is a subdir; "foo.py" must resolve to "sub/foo.py" repo-relative.
        sub = self.repo / "sub"
        sub.mkdir()
        edit(self.repo, patch("*** Add File: foo.py", "+x"), "S-A", cwd=sub)
        self.assertEqual(claimed_areas(self.repo, "session:S-A"), ["sub/foo.py"])

    def test_foreign_overlap_warns_and_does_not_block(self):
        edit(self.repo, patch("*** Add File: sim/foo.py", "+x"), "S-A")
        r = edit(self.repo, patch("*** Update File: sim/foo.py", "@@", "+y"), "S-B")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("claim warning", r.stderr)

    def test_garbage_stdin_exits_zero(self):
        self.assertEqual(run([sys.executable, str(GUARD)], self.repo, stdin="nope").returncode, 0)

    def test_non_applypatch_payload_is_noop(self):
        payload = json.dumps({"session_id": "S", "cwd": str(self.repo),
                              "tool_name": "Bash", "tool_input": {"command": "ls"}})
        r = run([sys.executable, str(GUARD)], self.repo, stdin=payload)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(claimed_areas(self.repo, "session:S"), [])

    def test_valid_json_wrong_shape_exits_zero(self):
        # Fail-open: syntactically valid JSON that is not the documented payload
        # object shape must still exit 0 (plan constraint: hooks never block).
        for blob in ("[]", "null", "42", '"nope"',
                     '{"tool_input": [1, 2]}', '{"tool_input": "oops"}',
                     '{"tool_input": {"command": 123}}',
                     '{"tool_input": {"command": "*** Begin Patch\\n*** Add File: x.py\\n+1\\n*** End Patch\\n"}, "cwd": 12345}'):
            r = run([sys.executable, str(GUARD)], self.repo, stdin=blob)
            self.assertEqual(r.returncode, 0, f"{blob!r}: {r.stderr}")


if __name__ == "__main__":
    unittest.main()
