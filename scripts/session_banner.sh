#!/usr/bin/env bash
# SessionStart banner: states which worktree + branch this session is in, so an
# agent (and the user) can see at a glance which tab/worktree they are working
# in. Advisory only; always exits 0.
set -uo pipefail
root="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
[ -n "$root" ] || exit 0
branch="$(git -C "$root" symbolic-ref --short HEAD 2>/dev/null || echo 'DETACHED')"
echo "worktree $(basename "$root") -> branch ${branch}  ($root)"
exit 0
