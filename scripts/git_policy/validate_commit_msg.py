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
