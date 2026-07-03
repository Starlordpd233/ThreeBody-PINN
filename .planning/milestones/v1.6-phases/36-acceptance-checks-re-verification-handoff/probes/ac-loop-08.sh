#!/usr/bin/env bash
# LOOP-08: SASD training-side provisional carry-forward.
# Disposable Phase-36 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Provisional tokens check per 34-VERIFICATION.md truth 7.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== LOOP-08: SASD training-side provisional ==="

# Provisional carry-forward tokens
grep -qiF 'provisional' "$CTL" && echo "[1] PASS: provisional token present" || { echo "[1] FAIL"; ERR=1; }

# SASD token
grep -qiF 'SASD' "$CTL" && echo "[2] PASS: SASD token present" || { echo "[2] FAIL"; ERR=1; }

# VAL-02 token
grep -qiF 'VAL-02' "$CTL" && echo "[3] PASS: VAL-02 token present" || { echo "[3] FAIL"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== LOOP-08: ALL CHECKS PASSED ===" || echo "=== LOOP-08: SOME CHECKS FAILED ==="
exit $ERR