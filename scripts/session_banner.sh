#!/usr/bin/env bash
# SessionStart banner: states which worktree + branch this session is in, so an
# agent (and the user) can see at a glance which tab/worktree they are working
# in. Advisory only; always exits 0.
set -uo pipefail
root="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
[ -n "$root" ] || exit 0
branch="$(git -C "$root" symbolic-ref --short HEAD 2>/dev/null || echo 'DETACHED')"
echo "worktree $(basename "$root") -> branch ${branch}  ($root)"
# Advisory presence. Identity is the Claude session id, which arrives on the
# SessionStart hook payload (stdin). Read it (guarded so we never block on a
# tty), seed CLAUDE_CODE_SESSION_ID into CLAUDE_ENV_FILE so later agent
# Bash-tool calls (announce/list) can read it, then register for this call.
# Everything here is advisory; failures are ignored.
sid=""
if [ ! -t 0 ]; then
  payload="$(cat 2>/dev/null || true)"
  sid="$(printf '%s' "$payload" | python3 -c 'import sys, json
try:
    print(json.load(sys.stdin).get("session_id", "") or "")
except Exception:
    pass' 2>/dev/null || true)"
fi
if [ -n "$sid" ] && [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  printf 'export CLAUDE_CODE_SESSION_ID=%s\n' "$sid" >> "$CLAUDE_ENV_FILE"
fi
CLAUDE_CODE_SESSION_ID="${sid:-${CLAUDE_CODE_SESSION_ID:-}}" \
  python3 "$root/scripts/git_policy/agent_presence.py" register 2>/dev/null || true

# Nudge the agent to announce its task so peers can see intent (the core datum).
echo 'presence: run  scripts/agent-presence announce "<your task>" --areas <paths>  so peers can see your work.'

exit 0
