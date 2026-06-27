#!/usr/bin/env bash
# Branch-independent launcher for the advisory presence registry.
#
# The user-global Claude settings call this script by absolute path (master's
# copy), so it runs from any worktree. It forwards to its sibling
# agent_presence.py, which resolves the shared presence dir via the git
# common-dir -- so every worktree shares one roster regardless of which branch
# it has checked out. The hook payload (carrying the session id) is passed
# through on stdin. Advisory only: always exits 0, never blocks a hook.
#
# Usage (from a Claude hook): presence_hook.sh {register|heartbeat|deregister}
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$here/agent_presence.py" "$@" 2>/dev/null || true
exit 0
