#!/usr/bin/env python3
"""PostToolUse hook for Codex: heartbeat on every call; flush a staged announce.

Runs unsandboxed (Codex sandboxes only model-generated shell, not hooks), so it can
write the shared presence/claims board from any worktree. On every PostToolUse it
bumps the session heartbeat (keeping a live session on the roster through non-edit
work), then applies any announce the model staged via agent-codex-announce.

Advisory only: always exits 0.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import agent_presence  # noqa: E402


def staging_file(session_id):
    base = os.path.join(os.environ.get("TMPDIR", "/tmp"), "agent-presence-staging")
    return os.path.join(base, f"{session_id}.json")


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if not isinstance(payload, dict):
        return 0  # fail open: wrong-shaped payload
    session = payload.get("session_id")
    if not isinstance(session, str) or not session:
        return 0
    try:
        agent_presence.heartbeat(session)  # unconditional P0 heartbeat, first
    except Exception:
        pass
    path = staging_file(session)
    try:
        if os.path.exists(path):
            with open(path) as handle:
                staged = json.load(handle)
            agent_presence.announce(
                session, staged.get("summary"), staged.get("areas") or [])
            os.remove(path)  # consume; existence alone marks "not yet flushed"
    except Exception:
        return 0  # advisory: never fail the PostToolUse round-trip
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
