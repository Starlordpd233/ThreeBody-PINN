#!/usr/bin/env bash
# AC-CURR-04: L_norm clamping acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Assertions transcribed from Phase 33 verification.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-CURR-04: L_norm clamping ==="

# Raw un-clipped L_norm metadata storage
grep -qiE 'raw.*un-clipped.*L_norm|L_norm.*raw.*un-clipped' "$CTL" && echo "[1] PASS: raw un-clipped L_norm metadata storage specified" || { echo "[1] FAIL"; ERR=1; }

# Mandatory nonfinite/near-degenerate L_max diagnostic guard
grep -qiE 'nonfinite.*near-degenerate.*L_max|L_max.*nonfinite.*near-degenerate' "$CTL" && echo "[2] PASS: mandatory nonfinite/near-degenerate L_max diagnostic guard" || { echo "[2] FAIL"; ERR=1; }

# "No global clamp is authorized"
grep -qF 'No global clamp is authorized' "$CTL" && echo "[3] PASS: global clamp explicitly NOT authorized" || { echo "[3] FAIL"; ERR=1; }

# np.clip gate NOT locked (owner-pending)
grep -qiE 'np.clip.*L_norm|L_norm.*np.clip' "$CTL" && echo "[4] FAIL: np.clip(L_norm) gate locked (should be owner-pending)" && ERR=1 || echo "[4] PASS: np.clip gate NOT locked (owner-pending)"

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-CURR-04: ALL CHECKS PASSED ===" || echo "=== AC-CURR-04: SOME CHECKS FAILED ==="
exit $ERR