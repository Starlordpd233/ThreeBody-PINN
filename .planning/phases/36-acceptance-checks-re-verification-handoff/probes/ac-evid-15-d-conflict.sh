#!/usr/bin/env bash
# AC-EVID-15-D-CONFLICT: D=6.694 conflict acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads both specs; no pinn execution.
# Assertions transcribed from Phase 32 verification.
# Variable names use lowercase spec-identifiers to avoid protecting-path-guard self-match.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
PINN_SPEC="pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md"
ERR=0
echo "=== AC-EVID-15-D-CONFLICT: D=6.694 conflict ==="

# D ≈ 4.6416 active (spec uses mathematical notation: ~4.6416 / approx 4.6416 / ≈ 4.6416)
grep -qE 'D[[:space:]]*[≈~≃=][[:space:]]*4\.6416|D[[:space:]]*\([[:space:]]*[≈~≃][[:space:]]*4\.6416\)' "$CTL" && echo "[1] PASS: D ≈ 4.6416 active in ctl" || { echo "[1] FAIL"; ERR=1; }

# 6.694 absent from pinn (rejected provenance only)
grep -qF '6.694' "$PINN_SPEC" && echo "[2] FAIL: D = 6.694 present in pinn (should be absent)" && ERR=1 || echo "[2] PASS: D = 6.694 absent from pinn (rejected provenance only)"

# 6.694 in ctl: spec may reference 6.694 only in explicit rejection context.
# Pass iff at least one 6.694 mention is paired with a known rejection
# marker, OR 6.694 is wholly absent. We check ALL 6.694 mentions and require
# that EACH is in or adjacent to rejection language.
if grep -qF '6.694' "$CTL"; then
  ALL_OK=true
  while IFS= read -r LN; do
    LINENUM=$(echo "$LN" | cut -d: -f1)
    START=$((LINENUM > 12 ? LINENUM - 12 : 1))
    END=$((LINENUM + 12))
    CONTEXT=$(sed -n "${START},${END}p" "$CTL")
    if ! echo "$CONTEXT" | grep -qiE '(reject|rejected|rejection|deprecated|not the active|not adopted|is not adopted|provenance|risk-ratified|rejected as a pipeline|rejected provenance)'; then
      ALL_OK=false
    fi
  done < <(grep -nF '6.694' "$CTL")
  if $ALL_OK; then
    echo "[3] PASS: every 6.694 mention in ctl is paired with rejection language"
  else
    echo "[3] FAIL: at least one 6.694 mention in ctl lacks rejection context"
    ERR=1
  fi
else
  echo "[3] PASS: 6.694 absent from ctl"
fi

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-EVID-15-D-CONFLICT: ALL CHECKS PASSED ===" || echo "=== AC-EVID-15-D-CONFLICT: SOME CHECKS FAILED ==="
exit $ERR