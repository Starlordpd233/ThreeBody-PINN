#!/usr/bin/env bash
# AC-CURR-02-M7: tau_L exclusion from IC13 acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Assertions transcribed from Phase 33 verification.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-CURR-02-M7: tau_L exclusion from IC13 ==="

# tau_L is staging/eval metadata, outside IC13 by design
grep -qiE 'tau_L.*staging.*metadata|staging.*metadata.*tau_L' "$CTL" && echo "[1] PASS: tau_L marked as staging/evaluation metadata" || { echo "[1] FAIL"; ERR=1; }

# tau_L explicitly excluded from IC13
grep -qiE 'tau_L.*outside.*IC13|IC13.*does.*not.*include.*tau_L' "$CTL" && echo "[2] PASS: tau_L excluded from IC13 by design" || { echo "[2] FAIL"; ERR=1; }

# No tau_L in the IC13 vector definition
grep -A 20 'IC13.*=.*\[' "$CTL" | grep -q 'tau_L' && echo "[3] FAIL: tau_L found in IC13 vector (should be excluded)" && ERR=1 || echo "[3] PASS: tau_L absent from IC13 vector definition"

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-CURR-02-M7: ALL CHECKS PASSED ===" || echo "=== AC-CURR-02-M7: SOME CHECKS FAILED ==="
exit $ERR