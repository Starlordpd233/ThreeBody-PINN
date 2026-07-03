#!/usr/bin/env bash
# LOOP-07: IPR/PSC training-side provisional carry-forward.
# Disposable Phase-36 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Provisional tokens check per 34-VERIFICATION.md truth 6.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== LOOP-07: IPR/PSC training-side provisional ==="

# Provisional carry-forward tokens
grep -qiF 'provisional' "$CTL" && echo "[1] PASS: provisional token present" || { echo "[1] FAIL"; ERR=1; }

# IPR token
grep -qiF 'IPR' "$CTL" && echo "[2] PASS: IPR token present" || { echo "[2] FAIL"; ERR=1; }

# PSC token
grep -qiF 'PSC' "$CTL" && echo "[3] PASS: PSC token present" || { echo "[3] FAIL"; ERR=1; }

# VAL-03 token
grep -qiF 'VAL-03' "$CTL" && echo "[4] PASS: VAL-03 token present" || { echo "[4] FAIL"; ERR=1; }

# VAL-04 token
grep -qiF 'VAL-04' "$CTL" && echo "[5] PASS: VAL-04 token present" || { echo "[5] FAIL"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== LOOP-07: ALL CHECKS PASSED ===" || echo "=== LOOP-07: SOME CHECKS FAILED ==="
exit $ERR