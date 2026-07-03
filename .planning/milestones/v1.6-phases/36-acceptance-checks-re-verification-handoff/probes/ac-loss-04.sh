#!/usr/bin/env bash
# AC-LOSS-04: causal mode acceptance check (D-04 Option A).
# Disposable Phase-36 spec-consistency probe. Reads both specs; no pinn execution.
# Assertions transcribed from Phase 35 verification.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
PINN="pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md"
ERR=0
echo "=== AC-LOSS-04: causal mode (D-04 Option A) ==="

# Per-time causal weighting w_n = exp(-η_c * Σ stopgrad(R̄_m))
grep -qiE 'w_n.*exp.*eta|per-time.*causal.*weighting' "$CTL" "$PINN" && echo "[1] PASS: per-time causal weighting present" || { echo "[1] FAIL"; ERR=1; }

# w_1 = 1
grep -qiE 'w_1.*=.*1|w_1.*=.*1.0' "$PINN" && echo "[2] PASS: w_1 = 1 present" || { echo "[2] FAIL"; ERR=1; }

# η_c = 1
grep -qiE 'eta_c.*=.*1|η_c.*=.*1' "$PINN" && echo "[3] PASS: η_c = 1 present" || { echo "[3] FAIL"; ERR=1; }

# Dense-residual pseudo-ALM rejected
grep -qiE 'dense-residual.*pseudo-ALM.*rejected|pseudo-ALM.*dense-residual.*rejected' "$CTL" "$PINN" && echo "[4] PASS: dense-residual pseudo-ALM rejected" || { echo "[4] FAIL"; ERR=1; }

# Scalar ALM deferred P2
grep -qiE 'scalar.*ALM.*deferred|deferred.*scalar.*ALM' "$CTL" "$PINN" && echo "[5] PASS: scalar ALM deferred P2" || { echo "[5] FAIL"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-LOSS-04: ALL CHECKS PASSED ===" || echo "=== AC-LOSS-04: SOME CHECKS FAILED ==="
exit $ERR