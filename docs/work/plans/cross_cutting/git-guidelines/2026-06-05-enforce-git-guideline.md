---
status: consumed
purpose: other
created: 2026-06-05
milestone: untracked
phase: git-guidelines
retirement_trigger: milestone complete; superseded by subsequent work
---

# Enforce Git Guideline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Install repo-local instructions and enforcement so Claude Code, Codex, Gemini, and human collaborators follow the project Git guideline whenever work may require a later commit.

**Architecture:** Enforcement is layered. `AGENTS.md` remains the compact cross-agent bootstrap, `docs/git-guidelines.md` becomes the full canonical reference, Python validators provide shared policy logic, tracked `.githooks/` scripts enforce commit-time behavior, setup scripts make hook installation repeatable, and Claude/Codex lifecycle hooks block agent attempts to bypass or destructively mutate Git state.

**Tech Stack:** Markdown governance docs, Git hooks, shell scripts, Python 3 standard library, JSON agent hook configuration, `unittest`, `rg`, and `git`.

---

## Source Inputs

Read these before implementing:

- `docs/work/reviews/cross_cutting/git-guidelines/final-git-guideline-review.md`
- `AGENTS.md`
- `.claude/settings.json`
- `<home>/Desktop/3_body_problem/.planning/codebase/CONVENTIONS.md`

Preserve this existing project state:

- `<home>/Desktop/3_body_problem/CLAUDE.md` is a symlink to `AGENTS.md`.
- `<home>/Desktop/3_body_problem/GEMINI.md` is a symlink to `AGENTS.md`.
- `<home>/Desktop/3_body_problem/.claude/settings.json` currently contains `enabledPlugins`; merge hook settings into it without replacing that array.
- Current local Git LFS hooks exist in `.git/hooks/post-checkout`, `.git/hooks/post-commit`, `.git/hooks/post-merge`, and `.git/hooks/pre-push`. Tracked hooks must preserve those LFS calls after `core.hooksPath` is set.

## Review-Identified Corrections

This plan was reviewed before execution and these corrections are already incorporated:

- Claude Code policy hooks must exit `2` to block a `PreToolUse` command; exit `1` is not enough for enforcement.
- Codex project-local hooks must use a top-level `hooks` object and depend on the project `.codex/` layer being trusted.
- The tracked `pre-push` hook must inspect pushed destination refs and replay stdin to `git lfs pre-push`; reading stdin once and then calling Git LFS would starve the LFS hook.
- Early commits made before `scripts/agent-commit` exists must still include explicit `Agent-Assisted-By:` trailers.
- Hook-bypass detection must block `git config core.hooksPath ...` mutations while allowing read-only `git config --get core.hooksPath`.

## Gray Areas For User Decision

The plan uses these default decisions. Change them before execution if the project owner wants different behavior:

- Agent attribution is required for agent-authored or materially agent-assisted commits, not for purely human commits.
- `ALLOW_DESTRUCTIVE_GIT=1` is the required machine-readable marker after explicit user approval for destructive Git commands; the marker does not replace the chat confirmation requirement in `AGENTS.md`.
- Pushes to protected remote refs `master`, `main`, and `milestone/*` are blocked locally. Maintainer emergency pushes should use an explicit, documented bypass outside normal agent workflow.
- Local Git hooks and agent lifecycle hooks are defense-in-depth, not absolute security controls. Repository-hosted CI and branch protection are still recommended if GitHub policy enforcement is available.

## File Structure

Create:

- `docs/git-guidelines.md` - full canonical Git guideline reference, derived from the consolidated final draft.
- `scripts/git_policy/__init__.py` - package marker for tests.
- `scripts/git_policy/validate_commit_msg.py` - commit-message validator used by `.githooks/commit-msg`.
- `scripts/git_policy/validate_staged_paths.py` - staged-file validator used by `.githooks/pre-commit`.
- `scripts/git_policy/guard_agent_git_command.py` - agent lifecycle hook guard for Git bypass and destructive commands.
- `scripts/agent-commit` - agent-only commit wrapper that sets `GIT_AGENT_COMMIT=1`.
- `scripts/setup-git-hooks.sh` - installs tracked hooks by setting `core.hooksPath=.githooks` and checking executability.
- `.githooks/commit-msg` - invokes the commit-message validator.
- `.githooks/pre-commit` - invokes the staged-file validator.
- `.githooks/pre-push` - blocks direct pushes to protected branches and preserves Git LFS `pre-push`.
- `.githooks/pre-rebase` - blocks rebases unless the user explicitly approved a bypass marker.
- `.githooks/post-checkout` - preserves Git LFS `post-checkout`.
- `.githooks/post-commit` - preserves Git LFS `post-commit`.
- `.githooks/post-merge` - preserves Git LFS `post-merge`.
- `.codex/hooks.json` - Codex project-local lifecycle hook configuration.
- `tests/git_policy/test_git_policy.py` - validator tests.

Modify:

- `AGENTS.md` - add the compact mandatory Git Commit Protocol after the existing Git Branch Awareness and Destructive Operations section.
- `.claude/settings.json` - add Claude Code `PreToolUse` hook configuration while preserving `enabledPlugins`.

## Execution Identity Prerequisite

Before the first commit command in Task 1, set an agent identity for the active implementation session:

```bash
export GIT_AGENT_ID="Codex GPT-5"
```

If execution is performed by Claude Code or Gemini instead of Codex, set `GIT_AGENT_ID` to that active tool and model before committing. Tasks 1-4 use explicit trailers because the wrapper is not available yet; Tasks 5-8 use `scripts/agent-commit`.

## Enforcement Rules To Implement

Hard failures:

- Reject `git commit --no-verify`, `git -c core.hooksPath=/dev/null`, and other hook-bypass attempts from agents.
- Agent lifecycle guard failures must exit with status `2`, because Claude Code only blocks `PreToolUse` on exit code `2`; Codex also supports exit code `2` for blocking hooks.
- Reject raw agent `git commit` commands; require `scripts/agent-commit`.
- Reject destructive agent commands unless the current chat has explicit user approval and the command sets `ALLOW_DESTRUCTIVE_GIT=1`.
- Reject commit subjects that do not match `<type>(<scope>): <lowercase imperative subject>`.
- Reject commit messages with disallowed types, disallowed scopes, empty subjects, uppercase subject starts, trailing periods, markdown/backticks/quotes, semicolon chains, or throwaway subjects such as `wip`, `update`, `misc`, and `changes`.
- Require a body for `spec`, `evidence`, `verify`, and `plan` commits; commits staging more than one file; commits touching `pinn_instruction/`, `.planning/`, framework spec paths, or `AGENTS.md`.
- When `GIT_AGENT_COMMIT=1`, require an `Agent-Assisted-By:` or valid `Co-Authored-By:` trailer.
- Reject staged bulky/generated/scratch artifacts such as `.DS_Store`, `__pycache__`, `*.pyc`, `tmp/`, `scratch/`, `runs/`, `outputs/`, `wandb/`, and staged blobs over 10 MiB unless the path is explicitly allowlisted in the validator.
- Block pushes from protected branches: `master`, `main`, and `milestone/*`.

Allowed commit types:

- `spec`
- `evidence`
- `verify`
- `plan`
- `docs`
- `feat`
- `fix`
- `refactor`
- `test`
- `chore`

Allowed scope forms:

- Phase scope: two digits, for example `20`
- Task scope: two digits, hyphen, two digits, for example `20-05`
- Fixed domain scopes: `governance`, `planning`, `pinn`, `brutus`, `pipeline`, `spec`, `docs`, `ref`

---

### Task 1: Add Policy Test Harness

**Files:**
- Create: `tests/git_policy/test_git_policy.py`

- [ ] **Step 1: Create the failing test file**

Use `apply_patch` to create `tests/git_policy/test_git_policy.py` with this exact content:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail before implementation**

Run:

```bash
python3 tests/git_policy/test_git_policy.py
```

Expected: FAIL because the validator scripts do not exist yet.

- [ ] **Step 3: Commit the failing test harness**

Run:

```bash
git add tests/git_policy/test_git_policy.py
git commit -m "test(governance): add git policy enforcement tests" -m "Add the test harness that defines the expected Git policy validation behavior before installing the validators and hooks." -m "Agent-Assisted-By: ${GIT_AGENT_ID}"
```

---

### Task 2: Implement Commit Message Validator

**Files:**
- Create: `scripts/git_policy/__init__.py`
- Create: `scripts/git_policy/validate_commit_msg.py`
- Test: `tests/git_policy/test_git_policy.py`

- [ ] **Step 1: Create package marker**

Use `apply_patch` to create `scripts/git_policy/__init__.py` as an empty file.

- [ ] **Step 2: Create commit message validator**

Use `apply_patch` to create `scripts/git_policy/validate_commit_msg.py` with this exact content:

```python
#!/usr/bin/env python3
import os
import re
import subprocess
import sys
from pathlib import Path


ALLOWED_TYPES = {
    "spec",
    "evidence",
    "verify",
    "plan",
    "docs",
    "feat",
    "fix",
    "refactor",
    "test",
    "chore",
}

FIXED_SCOPES = {
    "governance",
    "planning",
    "pinn",
    "brutus",
    "pipeline",
    "spec",
    "docs",
    "ref",
}

BODY_REQUIRED_TYPES = {"spec", "evidence", "verify", "plan"}
THROWAWAY_SUBJECTS = {"wip", "update", "updates", "misc", "changes", "work", "checkpoint"}
HEADER_RE = re.compile(r"^(?P<type>[a-z]+)\((?P<scope>[A-Za-z0-9_-]+)\): (?P<subject>.+)$")
PHASE_SCOPE_RE = re.compile(r"^\d{2}$")
TASK_SCOPE_RE = re.compile(r"^\d{2}-\d{2}$")
COAUTHOR_RE = re.compile(r"^Co-Authored-By: .+ <[^<>@\s]+@[^<>@\s]+>$")
AGENT_TRAILER_RE = re.compile(r"^Agent-Assisted-By: .+")


def fail(message):
    print(f"git policy: {message}", file=sys.stderr)
    return 1


def non_comment_lines(text):
    return [line.rstrip() for line in text.splitlines() if not line.startswith("#")]


def split_message(text):
    lines = non_comment_lines(text)
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        return "", [], []
    header = lines[0].strip()
    rest = lines[1:]
    body_lines = []
    trailer_lines = []
    in_trailers = False
    for line in rest:
        stripped = line.strip()
        if stripped.startswith("Co-Authored-By:") or stripped.startswith("Agent-Assisted-By:"):
            in_trailers = True
        if in_trailers:
            trailer_lines.append(stripped)
        else:
            body_lines.append(line)
    body = [line for line in body_lines if line.strip()]
    trailers = [line for line in trailer_lines if line.strip()]
    return header, body, trailers


def staged_files():
    override = os.environ.get("GIT_POLICY_STAGED_FILES")
    if override is not None:
        return [line.strip() for line in override.splitlines() if line.strip()]
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def valid_scope(scope):
    return scope in FIXED_SCOPES or PHASE_SCOPE_RE.match(scope) or TASK_SCOPE_RE.match(scope)


def touches_body_required_path(paths):
    prefixes = (
        "pinn_instruction/",
        ".planning/",
        "pinn_instruction/markdown_conversion/framework-specs/",
    )
    exact = {"AGENTS.md", "CLAUDE.md", "GEMINI.md", "docs/git-guidelines.md"}
    for path in paths:
        if path in exact:
            return True
        if path.endswith(".tex") and "framework" in path:
            return True
        if path.startswith(prefixes):
            return True
    return False


def validate_header(header):
    match = HEADER_RE.match(header)
    if not match:
        return None, None, None, fail("header must match '<type>(<scope>): <lowercase imperative subject>'")

    commit_type = match.group("type")
    scope = match.group("scope")
    subject = match.group("subject").strip()

    if commit_type not in ALLOWED_TYPES:
        return None, None, None, fail(f"type '{commit_type}' is not allowed")
    if not valid_scope(scope):
        return None, None, None, fail(f"scope '{scope}' is not allowed")
    if not subject:
        return None, None, None, fail("subject must not be empty")
    if len(subject) > 80:
        return None, None, None, fail("subject must be 80 characters or fewer")
    if subject.endswith("."):
        return None, None, None, fail("subject must not end with a period")
    if subject.lower() in THROWAWAY_SUBJECTS:
        return None, None, None, fail("subject is throwaway; describe the concrete change")
    if subject[0].isalpha() and subject[0] != subject[0].lower():
        return None, None, None, fail("subject must start lowercase")
    if any(ch in subject for ch in "`\"'"):
        return None, None, None, fail("subject must not contain markdown ticks or quotes")
    if ";" in subject:
        return None, None, None, fail("subject must not chain multiple changes with semicolons")

    return commit_type, scope, subject, 0


def has_agent_trailer(trailers):
    return any(AGENT_TRAILER_RE.match(line) or COAUTHOR_RE.match(line) for line in trailers)


def main(argv):
    if len(argv) != 2:
        return fail("usage: validate_commit_msg.py <commit-msg-file>")
    message_path = Path(argv[1])
    header, body, trailers = split_message(message_path.read_text())

    commit_type, _scope, _subject, status = validate_header(header)
    if status:
        return status

    paths = staged_files()
    body_required = (
        commit_type in BODY_REQUIRED_TYPES
        or len(paths) > 1
        or touches_body_required_path(paths)
    )
    if body_required and not body:
        return fail("commit body is required for this commit")

    if os.environ.get("GIT_AGENT_COMMIT") == "1" and not has_agent_trailer(trailers):
        return fail("agent commits must include Agent-Assisted-By or Co-Authored-By trailer")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

- [ ] **Step 3: Run commit validator tests**

Run:

```bash
python3 tests/git_policy/test_git_policy.py
```

Expected: Some tests still fail because the staged-path validator and command guard are not implemented yet. All `CommitMessagePolicyTests` should pass.

- [ ] **Step 4: Commit commit-message validator**

Run:

```bash
git add scripts/git_policy/__init__.py scripts/git_policy/validate_commit_msg.py tests/git_policy/test_git_policy.py
git commit -m "feat(governance): add commit message policy validator" -m "Add the shared validator that enforces the project Git commit format, required bodies, and agent attribution trailers." -m "Agent-Assisted-By: ${GIT_AGENT_ID}"
```

---

### Task 3: Implement Staged Path Validator

**Files:**
- Create: `scripts/git_policy/validate_staged_paths.py`
- Test: `tests/git_policy/test_git_policy.py`

- [ ] **Step 1: Create staged path validator**

Use `apply_patch` to create `scripts/git_policy/validate_staged_paths.py` with this exact content:

```python
#!/usr/bin/env python3
import fnmatch
import json
import os
import subprocess
import sys


MAX_BLOB_BYTES = 10 * 1024 * 1024

BLOCKED_PATTERNS = (
    ".DS_Store",
    "*/.DS_Store",
    "__pycache__/*",
    "*/__pycache__/*",
    "*.pyc",
    "tmp/*",
    "*/tmp/*",
    "scratch/*",
    "*/scratch/*",
    "runs/*",
    "*/runs/*",
    "outputs/*",
    "*/outputs/*",
    "wandb/*",
    "*/wandb/*",
)

ALLOW_LARGE_PATTERNS = (
    "simulation_data/Documentation/*",
)


def fail(message):
    print(f"git policy: {message}", file=sys.stderr)
    return 1


def staged_files():
    override = os.environ.get("GIT_POLICY_STAGED_FILES")
    if override is not None:
        return [line.strip() for line in override.splitlines() if line.strip()]
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def staged_sizes():
    override = os.environ.get("GIT_POLICY_STAGED_SIZES")
    if override:
        return {str(key): int(value) for key, value in json.loads(override).items()}
    sizes = {}
    for path in staged_files():
        result = subprocess.run(
            ["git", "cat-file", "-s", f":{path}"],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip().isdigit():
            sizes[path] = int(result.stdout.strip())
    return sizes


def matches_any(path, patterns):
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def main():
    paths = staged_files()
    errors = []

    for path in paths:
        if matches_any(path, BLOCKED_PATTERNS):
            errors.append(f"generated or scratch artifact is staged: {path}")

    sizes = staged_sizes()
    for path, size in sizes.items():
        if size > MAX_BLOB_BYTES and not matches_any(path, ALLOW_LARGE_PATTERNS):
            errors.append(f"staged blob exceeds 10 MiB: {path}")

    if errors:
        for error in errors:
            print(f"git policy: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run staged path tests**

Run:

```bash
python3 tests/git_policy/test_git_policy.py
```

Expected: `CommitMessagePolicyTests` and `StagedPathPolicyTests` pass. `AgentCommandGuardTests` still fail because the command guard is not implemented yet.

- [ ] **Step 3: Commit staged path validator**

Run:

```bash
git add scripts/git_policy/validate_staged_paths.py tests/git_policy/test_git_policy.py
git commit -m "feat(governance): add staged path policy validator" -m "Block generated, scratch, and oversized staged artifacts before project commits are created." -m "Agent-Assisted-By: ${GIT_AGENT_ID}"
```

---

### Task 4: Implement Agent Command Guard And Commit Wrapper

**Files:**
- Create: `scripts/git_policy/guard_agent_git_command.py`
- Create: `scripts/agent-commit`
- Test: `tests/git_policy/test_git_policy.py`

- [ ] **Step 1: Create agent command guard**

Use `apply_patch` to create `scripts/git_policy/guard_agent_git_command.py` with this exact content:

```python
#!/usr/bin/env python3
import json
import os
import re
import shlex
import sys


DESTRUCTIVE_PATTERNS = (
    (re.compile(r"\bgit\s+reset\s+--hard\b"), "git reset --hard"),
    (re.compile(r"\bgit\s+clean\s+-[^\n]*f"), "git clean -f"),
    (re.compile(r"\bgit\s+branch\s+-D\b"), "git branch -D"),
    (re.compile(r"\bgit\s+rebase\b"), "git rebase"),
    (re.compile(r"\bgit\s+push\s+[^\n]*--force(?:-with-lease)?\b"), "git push --force"),
    (re.compile(r"\bgit\s+stash\s+drop\b"), "git stash drop"),
)

BYPASS_PATTERNS = (
    (re.compile(r"--no-verify\b"), "no-verify"),
    (re.compile(r"core\.hooksPath\s*=\s*/dev/null"), "core.hooksPath=/dev/null"),
    (re.compile(r"-c\s+core\.hooksPath=/dev/null"), "core.hooksPath=/dev/null"),
)


def fail(message):
    print(f"git policy: {message}", file=sys.stderr)
    return 2


def collect_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from collect_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from collect_strings(item)


def read_payload():
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}


def shell_words(command):
    try:
        return shlex.split(command)
    except ValueError:
        return command.split()


def command_invokes_agent_commit(command):
    words = shell_words(command)
    return any(word.endswith("scripts/agent-commit") or word == "agent-commit" for word in words)


def command_invokes_raw_git_commit(command):
    if command_invokes_agent_commit(command):
        return False
    words = shell_words(command)
    git_options_with_values = {"-c", "-C", "--git-dir", "--work-tree", "--namespace", "--config-env"}
    for index, word in enumerate(words):
        if word != "git" and not word.endswith("/git"):
            continue
        cursor = index + 1
        while cursor < len(words):
            token = words[cursor]
            if token in git_options_with_values:
                cursor += 2
                continue
            if any(token.startswith(f"{option}=") for option in git_options_with_values if option.startswith("--")):
                cursor += 1
                continue
            if token.startswith("-"):
                cursor += 1
                continue
            return token == "commit"
    return False


def mutates_core_hooks_path(command):
    if "core.hooksPath" not in command or not re.search(r"\bgit\s+config\b", command):
        return False
    words = shell_words(command)
    read_flags = {"--get", "get", "--get-regexp", "--list", "-l"}
    return not any(flag in words for flag in read_flags)


def command_has_destructive_bypass(command):
    return "ALLOW_DESTRUCTIVE_GIT=1" in command or os.environ.get("ALLOW_DESTRUCTIVE_GIT") == "1"


def main():
    payload = read_payload()
    commands = [text for text in collect_strings(payload) if "git" in text or "agent-commit" in text]

    for command in commands:
        for pattern, label in BYPASS_PATTERNS:
            if pattern.search(command):
                return fail(f"agent command attempted to bypass Git hooks with {label}")

        if mutates_core_hooks_path(command):
            return fail("agent command attempted to mutate core.hooksPath")

        if command_invokes_raw_git_commit(command):
            return fail("agents must use scripts/agent-commit so attribution and hook policy are enforced")

        for pattern, label in DESTRUCTIVE_PATTERNS:
            if pattern.search(command) and not command_has_destructive_bypass(command):
                return fail(
                    f"agent command attempted destructive Git operation '{label}' without explicit user approval marker"
                )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Create agent commit wrapper**

Use `apply_patch` to create `scripts/agent-commit` with this exact content:

```bash
#!/usr/bin/env bash
set -euo pipefail

if [ -z "${GIT_AGENT_ID:-}" ]; then
  echo "git policy: set GIT_AGENT_ID to the active agent, tool, and model before committing" >&2
  exit 1
fi

export GIT_AGENT_COMMIT=1

for arg in "$@"; do
  case "$arg" in
    Agent-Assisted-By:*|Co-Authored-By:*)
      exec git commit "$@"
      ;;
  esac
done

exec git commit "$@" -m "Agent-Assisted-By: $GIT_AGENT_ID"
```

- [ ] **Step 3: Make scripts executable**

Run:

```bash
chmod +x scripts/git_policy/validate_commit_msg.py scripts/git_policy/validate_staged_paths.py scripts/git_policy/guard_agent_git_command.py scripts/agent-commit
```

Expected: command exits 0.

- [ ] **Step 4: Run all policy tests**

Run:

```bash
python3 tests/git_policy/test_git_policy.py
```

Expected: all tests pass.

- [ ] **Step 5: Commit guard and wrapper**

Run:

```bash
git add scripts/git_policy/guard_agent_git_command.py scripts/agent-commit tests/git_policy/test_git_policy.py
git commit -m "feat(governance): add agent git command guard" -m "Block raw agent commits, hook bypass attempts, and unapproved destructive Git commands before they reach the shell." -m "Agent-Assisted-By: ${GIT_AGENT_ID}"
```

---

### Task 5: Add Tracked Git Hooks And Setup Script

**Files:**
- Create: `.githooks/commit-msg`
- Create: `.githooks/pre-commit`
- Create: `.githooks/pre-push`
- Create: `.githooks/pre-rebase`
- Create: `.githooks/post-checkout`
- Create: `.githooks/post-commit`
- Create: `.githooks/post-merge`
- Create: `scripts/setup-git-hooks.sh`
- Test: `tests/git_policy/test_git_policy.py`

- [ ] **Step 1: Create commit-msg hook**

Use `apply_patch` to create `.githooks/commit-msg` with this exact content:

```bash
#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
exec python3 "$repo_root/scripts/git_policy/validate_commit_msg.py" "$1"
```

- [ ] **Step 2: Create pre-commit hook**

Use `apply_patch` to create `.githooks/pre-commit` with this exact content:

```bash
#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
exec python3 "$repo_root/scripts/git_policy/validate_staged_paths.py"
```

- [ ] **Step 3: Create pre-push hook preserving Git LFS**

Use `apply_patch` to create `.githooks/pre-push` with this exact content:

```bash
#!/usr/bin/env bash
set -euo pipefail

stdin_file="$(mktemp)"
trap 'rm -f "$stdin_file"' EXIT
cat > "$stdin_file"

while read -r local_ref _local_sha remote_ref _remote_sha; do
  case "$remote_ref" in
    refs/heads/master|refs/heads/main|refs/heads/milestone/*)
      echo "git policy: direct pushes to protected ref '$remote_ref' are blocked" >&2
      exit 1
      ;;
  esac
done < "$stdin_file"

if git lfs version >/dev/null 2>&1; then
  git lfs pre-push "$@" < "$stdin_file"
fi
```

- [ ] **Step 4: Create pre-rebase hook**

Use `apply_patch` to create `.githooks/pre-rebase` with this exact content:

```bash
#!/usr/bin/env bash
set -euo pipefail

if [ "${ALLOW_DESTRUCTIVE_GIT:-}" != "1" ]; then
  echo "git policy: rebase is blocked unless the user explicitly approved it and ALLOW_DESTRUCTIVE_GIT=1 is set" >&2
  exit 1
fi
```

- [ ] **Step 5: Create Git LFS preservation hooks**

Use `apply_patch` to create `.githooks/post-checkout` with this exact content:

```bash
#!/usr/bin/env bash
set -euo pipefail

if git lfs version >/dev/null 2>&1; then
  git lfs post-checkout "$@"
fi
```

Use `apply_patch` to create `.githooks/post-commit` with this exact content:

```bash
#!/usr/bin/env bash
set -euo pipefail

if git lfs version >/dev/null 2>&1; then
  git lfs post-commit "$@"
fi
```

Use `apply_patch` to create `.githooks/post-merge` with this exact content:

```bash
#!/usr/bin/env bash
set -euo pipefail

if git lfs version >/dev/null 2>&1; then
  git lfs post-merge "$@"
fi
```

- [ ] **Step 6: Create hook setup script**

Use `apply_patch` to create `scripts/setup-git-hooks.sh` with this exact content:

```bash
#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

chmod +x .githooks/commit-msg \
  .githooks/pre-commit \
  .githooks/pre-push \
  .githooks/pre-rebase \
  .githooks/post-checkout \
  .githooks/post-commit \
  .githooks/post-merge \
  scripts/git_policy/validate_commit_msg.py \
  scripts/git_policy/validate_staged_paths.py \
  scripts/git_policy/guard_agent_git_command.py \
  scripts/agent-commit

git config core.hooksPath .githooks

actual="$(git config --get core.hooksPath)"
if [ "$actual" != ".githooks" ]; then
  echo "git policy: expected core.hooksPath=.githooks, got '$actual'" >&2
  exit 1
fi

echo "git policy: installed tracked hooks at .githooks"
```

- [ ] **Step 7: Make hooks and setup script executable**

Run:

```bash
chmod +x .githooks/commit-msg .githooks/pre-commit .githooks/pre-push .githooks/pre-rebase .githooks/post-checkout .githooks/post-commit .githooks/post-merge scripts/setup-git-hooks.sh
```

Expected: command exits 0.

- [ ] **Step 8: Run policy tests**

Run:

```bash
python3 tests/git_policy/test_git_policy.py
```

Expected: all tests pass.

- [ ] **Step 9: Install tracked hooks locally**

Run:

```bash
scripts/setup-git-hooks.sh
git config --get core.hooksPath
```

Expected output includes:

```text
.githooks
```

- [ ] **Step 10: Commit hooks and setup script**

Run:

```bash
git add .githooks scripts/setup-git-hooks.sh tests/git_policy/test_git_policy.py
scripts/agent-commit -m "feat(governance): install tracked git policy hooks" -m "Set up repo-local Git hooks that enforce commit policy, preserve Git LFS behavior, and block protected branch pushes."
```

---

### Task 6: Add Canonical Git Guideline Docs

**Files:**
- Create: `docs/git-guidelines.md`
- Modify: `AGENTS.md`

- [ ] **Step 1: Create full Git guideline reference**

Use `apply_patch` to create `docs/git-guidelines.md`. The document must contain these sections, in this order, using the consolidated final draft as source material:

```markdown
# Git Guidelines

Date adopted: 2026-06-05
Status: Canonical project Git policy

## Purpose

This guideline prevents hidden branch drift, destructive Git loss, low-signal commits, and agent bypass of project commit policy.

## Trigger

Follow this guideline whenever a task may require a later Git commit, even if the commit is not created in the current session.

## Session Start And Branch Awareness

At session start and before committing, run `git status --short --branch` and surface the branch, ahead/behind state, and existing worktree changes. Treat existing changes as user-owned unless you created them in the current task.

## Destructive Operations

Do not run destructive Git operations without explicit user confirmation after explaining what will be affected. This includes `git reset --hard`, `git clean -f`, `git branch -D`, `git rebase`, `git push --force`, `git stash drop`, and disabling hooks.

## Commit Cadence

Commit at logical task boundaries. Keep commits atomic, reversible, and reviewable. Avoid mixed commits that combine planning, implementation, verification, and unrelated cleanup.

## Pre-Commit Review Protocol

Before committing, inspect `git status --short`, `git diff --cached`, and the unstaged diff for touched files. Stage only intended files. Run relevant verification and `git diff --check`.

## Commit Message Format

Use `<type>(<scope>): <lowercase imperative subject>`.

Allowed types: `spec`, `evidence`, `verify`, `plan`, `docs`, `feat`, `fix`, `refactor`, `test`, `chore`.

Allowed scopes: two-digit phase scopes such as `20`, task scopes such as `20-05`, and fixed domain scopes `governance`, `planning`, `pinn`, `brutus`, `pipeline`, `spec`, `docs`, `ref`.

The subject starts lowercase, uses imperative voice, is 80 characters or fewer, has no trailing period, and does not contain markdown ticks, quotes, or semicolon-chained changes.

## Required Bodies

A body is required for `spec`, `evidence`, `verify`, and `plan` commits; commits touching multiple files; commits touching `pinn_instruction/`, `.planning/`, framework specs, or governance instructions.

## Agent Attribution

Agent-authored or materially agent-assisted commits must include `Agent-Assisted-By: <agent/tool/model>` or a valid `Co-Authored-By:` trailer. Agents must use `scripts/agent-commit`; raw agent `git commit` commands are blocked by lifecycle hooks.

## Hook Enforcement

Run `scripts/setup-git-hooks.sh` after cloning or after changing hook files. Do not use `--no-verify`, `core.hooksPath=/dev/null`, or equivalent bypasses without explicit user approval.

## Branches, Tags, And PRs

Do not push directly from protected branches `master`, `main`, or `milestone/*`. Prefer feature branches for PR work. Create recovery branches or tags before destructive operations when loss is possible.

## Recovery

If work appears lost, perform read-only forensics first: `git reflog`, `git fsck`, `git stash list`, and `git worktree list`. Present recovery options before changing state.
```

- [ ] **Step 2: Insert compact protocol into `AGENTS.md`**

Insert this section immediately after the existing `CRITICAL GOVERNANCE: Git Branch Awareness & Destructive Operations` section and before `Source of Truth`:

```markdown
---

## CRITICAL GOVERNANCE: Git Commit Protocol

Follow this protocol whenever a task may require a later Git commit, even if the commit is not created in the current session. The full policy lives in `docs/git-guidelines.md`.

### Mandatory start and pre-commit checks

- At session start and before committing, run `git status --short --branch` and surface branch, ahead/behind state, and existing worktree changes.
- Treat existing changes as user-owned unless you created them in the current task.
- Before committing, inspect `git diff --cached`, check unstaged changes for touched files, and run relevant verification plus `git diff --check`.
- Stage only intended files. Do not include unrelated user changes.

### Hook and bypass policy

- Run `scripts/setup-git-hooks.sh` if `git config --get core.hooksPath` is not `.githooks`.
- Agents must use `scripts/agent-commit`; do not run raw `git commit`.
- Do not use `--no-verify`, `core.hooksPath=/dev/null`, or equivalent bypasses without explicit user approval.

### Commit message policy

Use `<type>(<scope>): <lowercase imperative subject>`.

Allowed types: `spec`, `evidence`, `verify`, `plan`, `docs`, `feat`, `fix`, `refactor`, `test`, `chore`.

Allowed scopes: two-digit phase scopes such as `20`, task scopes such as `20-05`, and fixed domain scopes `governance`, `planning`, `pinn`, `brutus`, `pipeline`, `spec`, `docs`, `ref`.

The subject starts lowercase, uses imperative voice, is 80 characters or fewer, has no trailing period, and contains no markdown ticks, quotes, or semicolon-chained changes.

A body is required for `spec`, `evidence`, `verify`, and `plan` commits; commits touching multiple files; commits touching `pinn_instruction/`, `.planning/`, framework specs, or governance instructions.

Agent-authored or materially agent-assisted commits must include `Agent-Assisted-By: <agent/tool/model>` or a valid `Co-Authored-By:` trailer.
```

- [ ] **Step 3: Verify docs mention the enforcement hooks**

Run:

```bash
rg -n "scripts/setup-git-hooks|scripts/agent-commit|Git Commit Protocol|core.hooksPath" AGENTS.md docs/git-guidelines.md
git diff --check AGENTS.md docs/git-guidelines.md
```

Expected: `rg` finds all four terms; `git diff --check` exits 0.

- [ ] **Step 4: Commit guideline docs**

Run:

```bash
git add AGENTS.md docs/git-guidelines.md
scripts/agent-commit -m "docs(governance): publish canonical git guidelines" -m "Add the full Git policy reference and compact cross-agent instructions in the root agent file."
```

---

### Task 7: Add Claude And Codex Lifecycle Enforcement

**Files:**
- Modify: `.claude/settings.json`
- Create: `.codex/hooks.json`
- Test: `scripts/git_policy/guard_agent_git_command.py`

- [ ] **Step 1: Merge Claude Code PreToolUse hook**

Modify `.claude/settings.json` by preserving the existing `enabledPlugins` array exactly and adding this top-level `hooks` entry:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(git rev-parse --show-toplevel)/scripts/git_policy/guard_agent_git_command.py\"",
            "timeout": 30,
            "statusMessage": "Checking Git command policy"
          }
        ]
      }
    ]
  }
}
```

The resulting file must have top-level keys `enabledPlugins` and `hooks`.

- [ ] **Step 2: Create Codex project hook configuration**

Use `apply_patch` to create `.codex/hooks.json` with this exact content:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "^(Bash|shell_command|exec_command|functions\\.exec_command)$",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(git rev-parse --show-toplevel)/scripts/git_policy/guard_agent_git_command.py\"",
            "timeout": 30,
            "statusMessage": "Checking Git command policy"
          }
        ]
      }
    ]
  }
}
```

- [ ] **Step 3: Validate JSON syntax**

Run:

```bash
python3 -m json.tool .claude/settings.json >/dev/null
python3 -m json.tool .codex/hooks.json >/dev/null
```

Expected: both commands exit 0.

- [ ] **Step 4: Verify Codex project-hook trust requirement**

Run:

```bash
python3 - <<'PY'
import json
from pathlib import Path

data = json.loads(Path(".codex/hooks.json").read_text())
assert "hooks" in data, "Codex hooks.json must have top-level hooks object"
assert "PreToolUse" in data["hooks"], "Codex hooks.json must define hooks.PreToolUse"
print("codex hook shape ok")
PY
```

Expected output:

```text
codex hook shape ok
```

Manual verification: start a fresh Codex session in this repository after the hook configuration is committed. If Codex prompts to trust the project `.codex/` layer, approve it only after reviewing this plan and the generated hook script. If the execution environment cannot verify Codex project trust, record `Codex project hook trust not verified` in the final handoff.

- [ ] **Step 5: Smoke-test guard payload behavior**

Run:

```bash
printf '{"tool_name":"Bash","tool_input":{"command":"git commit -m '\''fix(pinn): repair drift'\''"}}' | python3 scripts/git_policy/guard_agent_git_command.py
```

Expected: command exits 2 and prints a message requiring `scripts/agent-commit`.

Run:

```bash
printf '{"tool_name":"Bash","tool_input":{"command":"scripts/agent-commit -m '\''fix(pinn): repair drift'\''"}}' | python3 scripts/git_policy/guard_agent_git_command.py
```

Expected: command exits 0.

- [ ] **Step 6: Commit lifecycle hook configuration**

Run:

```bash
git add .claude/settings.json .codex/hooks.json
scripts/agent-commit -m "feat(governance): add agent git lifecycle guards" -m "Configure Claude Code and Codex project hooks to block agent Git bypasses and unapproved destructive commands."
```

---

### Task 8: End-To-End Enforcement Verification

**Files:**
- Verify: all enforcement files created or modified by Tasks 1-7

- [ ] **Step 1: Run unit tests**

Run:

```bash
python3 tests/git_policy/test_git_policy.py
```

Expected: all tests pass.

- [ ] **Step 2: Verify hook installation**

Run:

```bash
scripts/setup-git-hooks.sh
git config --get core.hooksPath
```

Expected output includes:

```text
.githooks
```

- [ ] **Step 3: Verify bad commit messages fail**

Run:

```bash
tmp_msg="$(mktemp)"
printf 'docs(docs): update\n' > "$tmp_msg"
python3 scripts/git_policy/validate_commit_msg.py "$tmp_msg"
rm -f "$tmp_msg"
```

Expected: validator exits nonzero and reports a throwaway subject.

- [ ] **Step 4: Verify good agent commit messages pass**

Run:

```bash
tmp_msg="$(mktemp)"
printf 'fix(pinn): repair parser drift\n\nExplain the parser drift and the intended behavior.\n\nAgent-Assisted-By: Codex GPT-5\n' > "$tmp_msg"
GIT_AGENT_COMMIT=1 GIT_POLICY_STAGED_FILES='pinn/parser.py' python3 scripts/git_policy/validate_commit_msg.py "$tmp_msg"
rm -f "$tmp_msg"
```

Expected: validator exits 0.

- [ ] **Step 5: Verify hook bypass guard fails**

Run:

```bash
printf '{"tool_name":"Bash","tool_input":{"command":"git commit --no-verify -m '\''fix(pinn): repair drift'\''"}}' | python3 scripts/git_policy/guard_agent_git_command.py
```

Expected: command exits 2 and reports `no-verify`.

- [ ] **Step 6: Verify destructive command guard fails without approval marker**

Run:

```bash
printf '{"tool_name":"Bash","tool_input":{"command":"git rebase master"}}' | python3 scripts/git_policy/guard_agent_git_command.py
```

Expected: command exits 2 and reports a destructive Git operation.

- [ ] **Step 7: Verify protected ref pre-push blocking**

Run:

```bash
printf 'refs/heads/topic 1111111111111111111111111111111111111111 refs/heads/milestone/v1.4 2222222222222222222222222222222222222222\n' | .githooks/pre-push origin git@example.com:owner/repo.git
```

Expected: command exits nonzero and reports that direct pushes to `refs/heads/milestone/v1.4` are blocked.

- [ ] **Step 8: Verify documentation and config references**

Run:

```bash
rg -n "Git Commit Protocol|docs/git-guidelines.md|scripts/setup-git-hooks.sh|scripts/agent-commit|guard_agent_git_command" AGENTS.md docs/git-guidelines.md .claude/settings.json .codex/hooks.json
git diff --check
```

Expected: `rg` finds all required references; `git diff --check` exits 0.

- [ ] **Step 9: Inspect final staged diff**

Run:

```bash
git status --short --branch
git diff --stat
git diff -- AGENTS.md docs/git-guidelines.md scripts/git_policy scripts/agent-commit scripts/setup-git-hooks.sh .githooks .claude/settings.json .codex/hooks.json tests/git_policy/test_git_policy.py
```

Expected: only enforcement-related files appear in the diff.

- [ ] **Step 10: Commit final verification if any verification-only file changed**

If Task 8 changed tracked files, commit those changes with:

```bash
git add AGENTS.md docs/git-guidelines.md scripts/git_policy scripts/agent-commit scripts/setup-git-hooks.sh .githooks .claude/settings.json .codex/hooks.json tests/git_policy/test_git_policy.py
scripts/agent-commit -m "verify(governance): validate git policy enforcement" -m "Record final verification updates for the project Git policy enforcement layer."
```

If Task 8 did not change tracked files, skip this commit.

---

## Self-Review Checklist

- [ ] Every enforcement layer from the consolidated draft is represented: instructions, full docs, tracked hooks, setup script, agent lifecycle hooks, tests, and verification.
- [ ] `AGENTS.md` stays compact and points to `docs/git-guidelines.md`.
- [ ] `CLAUDE.md` and `GEMINI.md` remain symlinks to `AGENTS.md`.
- [ ] `.claude/settings.json` keeps its existing `enabledPlugins` values.
- [ ] `.codex/hooks.json` uses project-local Codex hook structure and no inline `.codex/config.toml` hook table is added.
- [ ] Tracked `.githooks/` preserve Git LFS `post-checkout`, `post-commit`, `post-merge`, and `pre-push`.
- [ ] Agents cannot use raw `git commit`, `--no-verify`, or hook-path bypass commands through lifecycle hooks.
- [ ] Git hooks enforce commit-message shape even for non-agent commits.
- [ ] The implementation does not stage unrelated existing user changes.

## Execution Handoff

Plan complete and saved to `docs/work/plans/cross_cutting/git-guidelines/2026-06-05-enforce-git-guideline.md`. Two execution options:

1. Subagent-Driven (recommended) - dispatch a fresh subagent per task, review between tasks, fast iteration.
2. Inline Execution - execute tasks in this session using executing-plans, batch execution with checkpoints.
