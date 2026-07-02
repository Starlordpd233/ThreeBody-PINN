#!/usr/bin/env bash
# AC-LOOP-05: ALM mu_p clamp acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads pinn_architecture.md only; no pinn execution.
# Assertions transcribed from Phase 34 verification.

PINN="pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md"
ERR=0
echo "=== AC-LOOP-05: ALM mu_p clamp ==="

# ALM deferred/optional
grep -qiE 'ALM.*deferred|deferred.*ALM|ALM.*optional' "$PINN" && echo "[1] PASS: ALM marked deferred/optional" || { echo "[1] FAIL"; ERR=1; }

# Dense-residual ALM rejected from default loss
grep -qiE 'dense-residual.*ALM.*rejected|ALM.*dense-residual.*rejected' "$PINN" && echo "[2] PASS: dense-residual ALM rejected from default loss" || { echo "[2] FAIL"; ERR=1; }

# [1e-4, 100] clamp conditional only. Spec uses "[1e-4, 100]" (space after comma).
grep -qiE '\[1e-?4,[[:space:]]+100\]|1e-?4.*100.*clamp' "$PINN" && echo "[3] PASS: [1e-4, 100] clamp conditional present" || { echo "[3] FAIL"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-LOOP-05: ALL CHECKS PASSED ===" || echo "=== AC-LOOP-05: SOME CHECKS FAILED ==="
exit $ERR