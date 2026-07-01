#!/usr/bin/env bash
# install-global.sh — deploy the cross-session-watchdog toolchain globally.
#
# Source of truth: this repo's tools/watchdog/ + .claude/skills/cross-session-watchdog/SKILL.md.
# Targets: a real canonical at $HOME/.claude/skills/cross-session-watchdog/ and absolute
# symlinks under each alternate CCP profile's skills/ (alt, free, max). Re-runs are
# idempotent and self-healing — a profile reset or drifted canonical is restored by
# simply re-running this script. See docs/work/plans/cross_cutting/cross-session-watchdog/
# for design intent (path-rewrite, symlink scheme) and the project's git-guidelines.

set -euo pipefail

# --- repo-root resolution (CWD-independent) --------------------------------
# script lives at <repo>/tools/watchdog/install-global.sh
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

SRC_TOOLS_DIR="$REPO_ROOT/tools/watchdog"
SRC_LIB="$SRC_TOOLS_DIR/lib/wd-common.sh"
SRC_SKILL="$REPO_ROOT/.claude/skills/cross-session-watchdog/SKILL.md"

CANONICAL="$HOME/.claude/skills/cross-session-watchdog"
CANONICAL_BIN="$CANONICAL/bin"
CANONICAL_LIB="$CANONICAL_BIN/lib"

# --- preflight -------------------------------------------------------------
fail() { printf 'install-global.sh: %s\n' "$*" >&2; exit 1; }

[ -d "$SRC_TOOLS_DIR" ] || fail "missing source tools dir: $SRC_TOOLS_DIR"
[ -f "$SRC_LIB" ] || fail "missing source lib: $SRC_LIB"
[ -f "$SRC_SKILL" ] || fail "missing source SKILL.md: $SRC_SKILL"

# Locate the eight wd-* scripts the script will deploy.
scripts=()
for s in "$SRC_TOOLS_DIR"/wd-*; do
  [ -f "$s" ] || continue
  scripts+=("$(basename "$s")")
done
[ "${#scripts[@]}" -eq 8 ] || fail "expected 8 wd-* scripts in $SRC_TOOLS_DIR, found ${#scripts[@]}: ${scripts[*]}"

# --- refresh canonical bin/ -------------------------------------------------
mkdir -p "$HOME/.claude/skills" "$CANONICAL_BIN/lib"

for s in "${scripts[@]}"; do
  cp -f "$SRC_TOOLS_DIR/$s" "$CANONICAL_BIN/$s"
done

cp -f "$SRC_LIB" "$CANONICAL_LIB/wd-common.sh"
chmod 0755 "$CANONICAL_BIN"/wd-* || fail "chmod 0755 on $CANONICAL_BIN/wd-* failed"

# --- regenerate SKILL.md with absolute, profile-and-machine-independent paths
# The git repo stays the version-controlled dev/test source; this generated
# SKILL.md is what Claude Code loads when the skill is referenced from a profile.
# Source prefix is repo-relative `tools/watchdog/`; rewrite to absolute bin/.
SKILL_DEST="$CANONICAL/SKILL.md"
SKILL_PREFIX='tools/watchdog/'
# Single-quoted: keep '$HOME' literal in the deployed SKILL.md so the doc
# stays profile- and machine-independent (user shells expand $HOME at run time).
SKILL_TARGET='$HOME/.claude/skills/cross-session-watchdog/bin/'

# Count occurrences in source BEFORE rewriting — fails loud if source drifts
# away from the repo-relative tools/watchdog/ convention. -F treats the prefix
# literally (no regex); -o | wc -l counts occurrences, not just matching lines.
src_count=$(grep -Fo -- "$SKILL_PREFIX" "$SRC_SKILL" | wc -l | tr -d ' ' || true)
[ "$src_count" -gt 0 ] || fail "source SKILL.md has 0 occurrences of '$SKILL_PREFIX' (drift?); refusing to deploy an unrewritten SKILL.md"

sed "s|${SKILL_PREFIX}|${SKILL_TARGET}|g" "$SRC_SKILL" > "$SKILL_DEST"

# --- link alternate profiles ------------------------------------------------
PROFILES=(alt free max)

linked=()
skipped=()
errors=()

link_one() {
  local profile="$1"
  local profile_skills="$HOME/.claude-${profile}/skills"
  local target_link="$profile_skills/cross-session-watchdog"

  mkdir -p "$profile_skills"

  if [ -L "$target_link" ]; then
    ln -sfn "$CANONICAL" "$target_link" || { errors+=("$profile: ln -sfn failed"); return 1; }
  elif [ -e "$target_link" ]; then
    printf 'install-global.sh: WARNING: %s is a real directory; skipping (never clobber hand-installed skills)\n' "$target_link" >&2
    skipped+=("$profile (real dir)")
    return 0
  else
    ln -s "$CANONICAL" "$target_link" || { errors+=("$profile: ln -s failed"); return 1; }
  fi

  # Verify the link now points where intended.
  local resolved
  resolved="$(readlink "$target_link")"
  if [ "$resolved" != "$CANONICAL" ]; then
    errors+=("$profile: readlink -> '$resolved' (expected '$CANONICAL')")
    return 1
  fi
  linked+=("$profile")
}

for profile in "${PROFILES[@]}"; do
  link_one "$profile" || errors+=("$profile: link step failed")
done

# --- summary ----------------------------------------------------------------
printf '\n=== cross-session-watchdog global install ===\n'
printf 'canonical:    %s\n' "$CANONICAL"
printf 'bin scripts:  %s (chmod 0755)\n' "${#scripts[@]}"
printf 'SKILL.md:     %s  (rewrote %d paths)\n' "$SKILL_DEST" "$src_count"
if [ "${#linked[@]}" -gt 0 ]; then
  printf 'linked:       %s\n' "${linked[*]}"
fi
if [ "${#skipped[@]}" -gt 0 ]; then
  printf 'skipped:      %s\n' "${skipped[*]}"
fi

if [ "${#errors[@]}" -gt 0 ]; then
  printf 'errors:\n' >&2
  for e in "${errors[@]}"; do printf '  - %s\n' "$e" >&2; done
  exit 1
fi

cat <<'VERIFY'

verify:
  ls -l ~/.claude/skills/cross-session-watchdog/bin/                       # 8 + lib, scripts 0755
  ls -ld ~/.claude-{alt,free,max}/skills/cross-session-watchdog             # all -> canonical
  ~/.claude/skills/cross-session-watchdog/bin/wd-status                    # exit 0
  ~/.claude-alt/skills/cross-session-watchdog/bin/wd-status                # exit 0 (via symlink)
VERIFY
