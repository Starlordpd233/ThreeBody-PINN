#!/usr/bin/env bash
# PROTECTED-PATH-GUARD: Phase 36 protected-path check.
# Verifies (a) no probes/ script imports / references pinn code, and
# (b) git diff over pinn/ and frozen/read-only specs is empty.
# Self-matching is excluded: this script (and its own echo / git-diff lines)
# legitimately contains "pinn/" tokens describing what is forbidden.

cd "$(git rev-parse --show-toplevel)" || exit 2

ERR=0
echo "=== PROTECTED-PATH-GUARD ==="

# Check (a): no probes/ script references pinn code
echo "[1] Checking probes/ for pinn references..."

PROBES_DIR=".planning/phases/36-acceptance-checks-re-verification-handoff/probes"
SELF_FILE=".planning/phases/36-acceptance-checks-re-verification-handoff/probes/ac-protected-path-guard.sh"

if [ ! -d "$PROBES_DIR" ]; then
  echo "[1] FAIL: probes directory not found"
  ERR=1
else
  # Forbidden patterns indicate ACTIVE references to pinn/ code:
  #   - Importing: `import pinn` / `from pinn`
  #   - Path() argument: `Path("pinn/...")` / `Path('pinn/...')` etc.
  # We deliberately do NOT match the bare string "pinn/" because it appears
  # legitimately in echo messages describing forbidden tokens.
  ACTIVE_PATTERNS='import[[:space:]]+pinn|from[[:space:]]+pinn[[:space:]]+import|Path[[:space:]]*\([[:space:]]*["\x27]pinn/'

  PATTERN_COUNT=0
  PATTERN_OUTPUT=""
  while IFS= read -r f; do
    # Skip this guard script itself (legitimately mentions pinn/ in its own check).
    [ "$f" = "$SELF_FILE" ] && continue
    # Read non-comment, non-blank lines and grep for ACTIVE patterns.
    MATCHES=$(grep -vE '^[[:space:]]*#|^[[:space:]]*$' "$f" 2>/dev/null | grep -nE "$ACTIVE_PATTERNS" || true)
    if [ -n "$MATCHES" ]; then
      PATTERN_COUNT=$((PATTERN_COUNT + $(echo "$MATCHES" | wc -l)))
      PATTERN_OUTPUT="${PATTERN_OUTPUT}${f}: ${MATCHES}\n"
    fi
  done < <(find "$PROBES_DIR" -type f \( -name "*.sh" -o -name "*.py" \))

  if [ "$PATTERN_COUNT" -eq 0 ]; then
    echo "[1] PASS: no active pinn code references in probes/ scripts"
  else
    echo "[1] FAIL: found $PATTERN_COUNT active pinn code reference(s) in probes/ scripts"
    echo -e "$PATTERN_OUTPUT"
    ERR=1
  fi
fi

# Check (b): git diff over pinn/ and frozen/read-only specs empty
echo "[2] Checking git diff for pinn/ and frozen specs changes..."

# Check pinn/ diff
PINN_DIFF=$(git diff --name-only pinn/ 2>/dev/null)
if [ -z "$PINN_DIFF" ]; then
  echo "[2a] PASS: no pinn/ changes detected"
else
  echo "[2a] FAIL: pinn/ has uncommitted changes:"
  echo "$PINN_DIFF"
  ERR=1
fi

# Check frozen/read-only spec diffs
FROZEN_SPECS="pinn_instruction/markdown_conversion/framework-specs/sampling_method.md pinn_instruction/markdown_conversion/research_reports/data_quality_assessment.md pinn_instruction/markdown_conversion/research_reports/review-of-framework.md pinn_instruction/markdown_conversion/research_reports/stage-strat-revision.md"
FROZEN_DIFF=""
for spec in $FROZEN_SPECS; do
  if [ -f "$spec" ]; then
    SPEC_DIFF=$(git diff --name-only "$spec" 2>/dev/null)
    if [ -n "$SPEC_DIFF" ]; then
      FROZEN_DIFF="$FROZEN_DIFF$SPEC_DIFF\n"
    fi
  fi
done

if [ -z "$FROZEN_DIFF" ]; then
  echo "[2b] PASS: no frozen/read-only spec changes detected"
else
  echo "[2b] FAIL: frozen/read-only specs have uncommitted changes:"
  echo -e "$FROZEN_DIFF"
  ERR=1
fi

echo ""
if [ "$ERR" -eq 0 ]; then
  echo "=== PROTECTED-PATH-GUARD: ALL CHECKS PASSED ==="
else
  echo "=== PROTECTED-PATH-GUARD: SOME CHECKS FAILED ==="
fi

exit $ERR