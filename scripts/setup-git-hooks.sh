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
  scripts/agent-commit \
  scripts/agent-claim \
  scripts/agent-release \
  scripts/git_policy/agent_claims.py \
  scripts/git_policy/claim_guard.py

git config core.hooksPath .githooks

actual="$(git config --get core.hooksPath)"
if [ "$actual" != ".githooks" ]; then
  echo "git policy: expected core.hooksPath=.githooks, got '$actual'" >&2
  exit 1
fi

echo "git policy: installed tracked hooks at .githooks"
