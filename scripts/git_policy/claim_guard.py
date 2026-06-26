#!/usr/bin/env python3
"""PreToolUse hook for Edit/Write/MultiEdit: warn on a foreign claim, else auto-declare.

Advisory only: always exits 0 so it never blocks an edit. The hard guarantee
against silent overwrite is the commit-time owned-paths net, not this hook.
Identity is the Claude session id (stable across a session's edits), taken from
the hook payload.
"""
import json
import os
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import agent_claims  # noqa: E402
import agent_presence  # noqa: E402


def repo_relative(file_path):
    try:
        root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            text=True, capture_output=True, check=True,
        ).stdout.strip()
        return os.path.relpath(os.path.abspath(file_path), root)
    except Exception:
        return file_path


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    file_path = (payload.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0
    session = payload.get("session_id")
    if session:
        os.environ["AGENT_CLAIM_WHO"] = f"session:{session}"
        try:
            agent_presence.heartbeat(session)
        except Exception:
            pass   # advisory: heartbeat must never block an edit
    area = repo_relative(file_path)
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
