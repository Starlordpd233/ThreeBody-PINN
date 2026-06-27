#!/usr/bin/env bash
# wd-common.sh — shared helpers for the cross-session watchdog tools.
#
# Sourced by wd-publish-done, wd-check, and wd-arm. Resolves the watchdog
# channel root to an ABSOLUTE path under the shared git common dir, so a
# producer and consumer in the same repo (main worktree or any linked
# worktree) agree on one channel location. The relative-vs-absolute
# normalization mirrors scripts/agent-commit:16-21: the main worktree returns
# a relative ".git" from `git rev-parse --git-common-dir`, which must be
# anchored to the repo root; linked worktrees already return an absolute path.
set -euo pipefail

wd_channel_root() {
  local repo_root common_dir
  repo_root="$(git rev-parse --show-toplevel)"
  common_dir="$(git rev-parse --git-common-dir)"
  case "$common_dir" in /*) : ;; *) common_dir="$repo_root/$common_dir" ;; esac
  printf '%s/live-monitor/channels' "$common_dir"
}

wd_channel_dir() { printf '%s/%s' "$(wd_channel_root)" "$1"; }
