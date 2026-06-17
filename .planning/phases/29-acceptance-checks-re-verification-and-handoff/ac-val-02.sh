#!/usr/bin/env bash
# AC-VAL-02 (SASD): stiffness-aware sampling-density both-endpoint contract acceptance check.
# Disposable Phase-29 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Assertions transcribed from the landed Data-side quality-metric contracts SASD clause.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-VAL-02: SASD both-endpoint contract ==="

grep -qF 'Stiffness-Aware Sampling Density' "$CTL" && echo "[1] PASS: SASD clause present" || { echo "[1] FAIL"; ERR=1; }
grep -qF 'Both-endpoint evaluation' "$CTL" && echo "[2] PASS: both-endpoint evaluation convention" || { echo "[2] FAIL"; ERR=1; }
grep -qF 'GAP-28-01 RESOLVED-WITH-INSTRUCTION' "$CTL" && echo "[3] PASS: GAP-28-01 user sign-off cited" || { echo "[3] FAIL"; ERR=1; }
grep -qiE 'flag.*resampling|not.*auto-reject' "$CTL" && echo "[4] PASS: flag-for-resampling (not auto-reject) semantics" || { echo "[4] FAIL"; ERR=1; }

# Negative control: perpendicular-component and stacked-9-component variants are rejected.
grep -qF 'perpendicular-component variant is rejected' "$CTL" && echo "[5] PASS: perpendicular-component variant rejected" || { echo "[5] FAIL"; ERR=1; }
grep -qF '9-component aggregation is rejected' "$CTL" && echo "[6] PASS: stacked 9-component aggregation rejected (negative control)" || { echo "[6] FAIL: stacked-variant rejection absent"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-VAL-02: ALL CHECKS PASSED ===" || echo "=== AC-VAL-02: SOME CHECKS FAILED ==="
exit $ERR
