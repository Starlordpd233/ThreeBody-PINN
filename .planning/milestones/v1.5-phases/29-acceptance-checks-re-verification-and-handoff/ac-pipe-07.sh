#!/usr/bin/env bash
# AC-PIPE-07 (footer / mass-drift): precision contract acceptance check.
# Disposable Phase-29 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Assertions transcribed from section 2.1 parser/mass-invariance + PIPE-07 precision note.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-PIPE-07: precision contract (footer / mass-drift) ==="

grep -qiE 'mass-invariance|mass invariance' "$CTL" && echo "[1] PASS: mass-invariance gate present" || { echo "[1] FAIL"; ERR=1; }
grep -qF '1e-15' "$CTL" && echo "[2] PASS: mass-invariance tolerance 1e-15" || { echo "[2] FAIL"; ERR=1; }
grep -qF 'float64` is the data-side precision contract' "$CTL" && echo "[3] PASS: float64 is the precision contract" || { echo "[3] FAIL"; ERR=1; }
grep -qF 'Precision note (PIPE-07' "$CTL" && echo "[4] PASS: PIPE-07 precision note (DATA-05 rerun validated)" || { echo "[4] FAIL"; ERR=1; }

# Negative control: decimal.Decimal is NOT the routine parsing / metric path.
grep -qF 'never as the routine parsing or metric-computation path' "$CTL" \
  && echo "[5] PASS: Decimal confined to mass-gate classifier, not routine path" \
  || { echo "[5] FAIL: Decimal-routine-path prohibition absent"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-PIPE-07: ALL CHECKS PASSED ===" || echo "=== AC-PIPE-07: SOME CHECKS FAILED ==="
exit $ERR
