#!/usr/bin/env python3
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
COMMIT_VALIDATOR = ROOT / "scripts" / "git_policy" / "validate_commit_msg.py"
STAGED_VALIDATOR = ROOT / "scripts" / "git_policy" / "validate_staged_paths.py"
COMMAND_GUARD = ROOT / "scripts" / "git_policy" / "guard_agent_git_command.py"


def run_python(script, args=None, stdin=None, env=None):
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        [sys.executable, str(script), *(args or [])],
        cwd=ROOT,
        input=stdin,
        text=True,
        capture_output=True,
        env=merged_env,
        check=False,
    )


def validate_message(message, env=None):
    with tempfile.NamedTemporaryFile("w", delete=False) as handle:
        handle.write(message)
        path = handle.name
    try:
        return run_python(COMMIT_VALIDATOR, [path], env=env)
    finally:
        pathlib.Path(path).unlink(missing_ok=True)


class CommitMessagePolicyTests(unittest.TestCase):
    def test_accepts_valid_agent_commit_with_body_and_trailer(self):
        result = validate_message(
            "fix(pinn): repair parser drift\n"
            "\n"
            "Explain the behavioral change and why the parser drift occurred.\n"
            "\n"
            "Agent-Assisted-By: Codex GPT-5\n",
            env={"GIT_AGENT_COMMIT": "1", "GIT_POLICY_STAGED_FILES": "pinn/parser.py\n"},
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_uppercase_subject_start(self):
        result = validate_message(
            "fix(pinn): Repair parser drift\n",
            env={"GIT_POLICY_STAGED_FILES": "pinn/parser.py\n"},
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("lowercase", result.stderr)

    def test_rejects_throwaway_subject(self):
        result = validate_message(
            "docs(docs): update\n",
            env={"GIT_POLICY_STAGED_FILES": "docs/readme.md\n"},
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("throwaway", result.stderr)

    def test_requires_body_for_spec_type(self):
        result = validate_message(
            "spec(20): revise control objective\n",
            env={"GIT_POLICY_STAGED_FILES": "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md\n"},
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("body", result.stderr)

    def test_requires_agent_trailer_for_agent_commit(self):
        result = validate_message(
            "fix(pinn): repair parser drift\n"
            "\n"
            "Explain the behavioral change and why the parser drift occurred.\n",
            env={"GIT_AGENT_COMMIT": "1", "GIT_POLICY_STAGED_FILES": "pinn/parser.py\n"},
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Agent-Assisted-By", result.stderr)


class StagedPathPolicyTests(unittest.TestCase):
    def test_rejects_generated_artifacts(self):
        result = run_python(
            STAGED_VALIDATOR,
            env={"GIT_POLICY_STAGED_FILES": "pinn/__pycache__/model.cpython-312.pyc\n"},
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("generated", result.stderr)

    def test_rejects_large_unallowlisted_blob(self):
        result = run_python(
            STAGED_VALIDATOR,
            env={
                "GIT_POLICY_STAGED_FILES": "analysis/output.bin\n",
                "GIT_POLICY_STAGED_SIZES": json.dumps({"analysis/output.bin": 12 * 1024 * 1024}),
            },
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("10 MiB", result.stderr)


class AgentCommandGuardTests(unittest.TestCase):
    def guard(self, command, env=None):
        payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
        return run_python(COMMAND_GUARD, stdin=payload, env=env)

    def test_rejects_raw_agent_commit(self):
        result = self.guard("git commit -m 'fix(pinn): repair parser drift'")
        self.assertEqual(result.returncode, 2)
        self.assertIn("scripts/agent-commit", result.stderr)

    def test_rejects_raw_agent_commit_with_git_options(self):
        result = self.guard("git -c user.name=Agent commit -m 'fix(pinn): repair parser drift'")
        self.assertEqual(result.returncode, 2)
        self.assertIn("scripts/agent-commit", result.stderr)

    def test_rejects_raw_agent_commit_with_absolute_git_path(self):
        result = self.guard("/usr/bin/git commit -m 'fix(pinn): repair parser drift'")
        self.assertEqual(result.returncode, 2)
        self.assertIn("scripts/agent-commit", result.stderr)

    def test_allows_agent_commit_wrapper(self):
        result = self.guard("scripts/agent-commit -m 'fix(pinn): repair parser drift'")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_no_verify(self):
        result = self.guard("scripts/agent-commit --no-verify -m 'fix(pinn): repair parser drift'")
        self.assertEqual(result.returncode, 2)
        self.assertIn("no-verify", result.stderr)

    def test_rejects_hook_path_mutation(self):
        result = self.guard("git config core.hooksPath /dev/null")
        self.assertEqual(result.returncode, 2)
        self.assertIn("core.hooksPath", result.stderr)

    def test_allows_hook_path_read(self):
        result = self.guard("git config --get core.hooksPath")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_destructive_git_without_bypass_marker(self):
        result = self.guard("git reset --hard HEAD")
        self.assertEqual(result.returncode, 2)
        self.assertIn("destructive", result.stderr)

    def test_allows_destructive_git_with_bypass_marker(self):
        result = self.guard("ALLOW_DESTRUCTIVE_GIT=1 git reset --hard HEAD")
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
