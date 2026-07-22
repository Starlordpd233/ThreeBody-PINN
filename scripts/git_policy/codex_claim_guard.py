#!/usr/bin/env python3
"""PreToolUse hook for Codex apply_patch: warn on a foreign claim, else auto-declare.

Mirrors claim_guard.py but parses the apply_patch *patch body* (tool_input.command)
for affected paths instead of reading tool_input.file_path. Codex emits cwd-relative
paths, so each is resolved against the payload's cwd before being made repo-relative.

Advisory only: always exits 0; never blocks an edit. The hard guarantee against
silent overwrite is the commit-time owned-paths net, not this hook.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import agent_claims  # noqa: E402
import agent_presence  # noqa: E402

# "*** Add File: <p>", "*** Update File: <p>", "*** Delete File: <p>", "*** Move to: <p>"
_MARKER = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+?)\s*$")
_MOVE = re.compile(r"^\*\*\* Move to: (.+?)\s*$")


def extract_paths(command):
    paths = []
    for line in (command or "").splitlines():
        m = _MARKER.match(line) or _MOVE.match(line)
        if m:
            paths.append(m.group(1))
    return paths


def repo_relative(path, cwd):
    base = path if os.path.isabs(path) else os.path.join(cwd, path)
    try:
        root = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--show-toplevel"],
            text=True, capture_output=True, check=True,
        ).stdout.strip()
        return os.path.relpath(os.path.abspath(base), root)
    except Exception:
        return path


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if not isinstance(payload, dict):
        return 0  # fail open: wrong-shaped payload
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return 0  # fail open: wrong-shaped tool_input
    command = tool_input.get("command")
    if not isinstance(command, str) or not command:
        return 0  # not an apply_patch-shaped payload; nothing to claim
    cwd = payload.get("cwd") or os.getcwd()
    if not isinstance(cwd, str):
        cwd = os.getcwd()  # fail open: contract says cwd is a string
    session = payload.get("session_id")
    if session:
        os.environ["AGENT_CLAIM_WHO"] = agent_presence.who_key(session)
        try:
            agent_presence.heartbeat(session)
        except Exception:
            pass  # advisory: heartbeat must never block an edit
    seen = set()
    for raw in extract_paths(command):
        area = repo_relative(raw, cwd)
        if area in seen:
            continue
        seen.add(area)
        try:
            other = agent_claims.find_conflict(area)
            if other is not None:
                print(
                    f"claim warning: '{area}' overlaps a claim held by {other.get('who')} "
                    f"(area: {other.get('area')}, reason: {other.get('why') or 'n/a'}). "
                    f"Coordinate before overlapping.",
                    file=sys.stderr,
                )
            else:
                agent_claims.claim(area, why="auto-declared on edit")
        except Exception:
            return 0  # fail open: advisory must never block
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
