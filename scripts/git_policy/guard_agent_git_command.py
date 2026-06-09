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
