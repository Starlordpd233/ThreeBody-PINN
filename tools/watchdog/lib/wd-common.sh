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

# Channel naming lives here. Channel location stays owned by wd_channel_root /
# wd_channel_dir above; keep those helpers stable while naming evolves.
wd_slug() {
  local s
  s="$(printf '%s' "$1" | LC_ALL=C tr '[:upper:]' '[:lower:]' \
        | LC_ALL=C sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//')"
  [ -n "$s" ] || return 1
  printf '%s' "$s"
}

# wd_resolve_channel TOOL CHANNEL PHASE KEY -> prints resolved channel name.
# Exactly one of CHANNEL/PHASE/KEY must be non-empty.
wd_resolve_channel() {
  local tool channel phase key selected normalized slug
  tool=$1
  channel=$2
  phase=$3
  key=$4
  selected=0
  [ -n "$channel" ] && selected=$((selected + 1))
  [ -n "$phase" ] && selected=$((selected + 1))
  [ -n "$key" ] && selected=$((selected + 1))
  if [ "$selected" -ne 1 ]; then
    printf '%s: exactly one of --channel, --phase, --key is required\n' "$tool" >&2
    return 2
  fi
  if [ -n "$channel" ]; then
    printf '%s' "$channel"
    return 0
  fi
  if [ -n "$phase" ]; then
    case "$phase" in
      *[!0-9]*)
        printf '%s: --phase must be a positive integer\n' "$tool" >&2
        return 2
        ;;
    esac
    normalized=$((10#$phase))
    if [ "$normalized" -le 0 ]; then
      printf '%s: --phase must be a positive integer\n' "$tool" >&2
      return 2
    fi
    printf 'gsd-phase-%s' "$normalized"
    return 0
  fi
  slug="$(wd_slug "$key")" || {
    printf '%s: --key produced an empty channel slug\n' "$tool" >&2
    return 2
  }
  printf '%s' "$slug"
}
