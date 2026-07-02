#!/usr/bin/env bash
# PROTECTED-PATH-GUARD: Phase 36 protected-path check.
# Verifies (a) no probes/ script references pinn code, and (b) git diff over pinn/ and frozen/read-only specs empty.
# Assembles forbidden tokens dynamically to avoid self-matching.

cd "$(git rev-parse --show-toplevel)" || exit 2

ERR=0
echo "=== PROTECTED-PATH-GUARD ==="

# Check (a): no probes/ script references pinn code
echo "[1] Checking probes/ for pinn references..."

PROBES_DIR=".planning/phases/36-acceptance-checks-re-verification-handoff/probes"
if [ ! -d "$PROBES_DIR" ]; then
  echo "[1] FAIL: probes directory not found"
  ERR=1
else
  # Dynamically assemble forbidden tokens (pinn/, import pinn, from pinn, Path(pinn))
  FORBIDDEN_TOKENS=""
  for token in "pinn/" "import pinn" "from pinn" "Path.*pinn"; do
    FORBIDDEN_TOKENS="$FORBIDDEN_TOKENS$token|"
  done
  FORBIDDEN_TOKENS="${FORBIDDEN_TOKENS%|}"  # Remove trailing pipe

  # Check for forbidden patterns (excluding comments)
  PATTERN_COUNT=$(find "$PROBES_DIR" -type f \( -name "*.sh" -o -name "*.py" \) -exec grep -vE '^[[:space:]]*#' {} \; | grep -cE "$FORBIDDEN_TOKENS" || echo "0")

  if [ "$PATTERN_COUNT" -eq 0 ]; then
    echo "[1] PASS: no pinn/ references in probes/ scripts"
  else
    echo "[1] FAIL: found $PATTERN_COUNT pinn/ reference(s) in probes/ scripts"
    # Show the matches
    find "$PROBES_DIR" -type f \( -name "*.sh" -o -name "*.py" \) -exec grep -vE '^[[:space:]]*#' {} + | grep -E "$FORBIDDEN_TOKENS"
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