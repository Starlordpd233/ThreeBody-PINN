#!/usr/bin/env bash
# AC-LOSS-03: energy Huber delta acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads both specs; no pinn execution.
# Assertions transcribed from Phase 35 verification.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
PINN="pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md"
ERR=0
echo "=== AC-LOSS-03: energy Huber delta ==="

# delta_E = 1.0 baseline retained
grep -qF 'delta_E=1.0' "$PINN" && echo "[1] PASS: delta_E=1.0 baseline retained" || { echo "[1] FAIL"; ERR=1; }

# Empirical/median-scaled calibration deferred
grep -qiE 'empirical.*median-scaled.*deferred|median-scaled.*empirical.*deferred' "$CTL" "$PINN" && echo "[2] PASS: empirical/median-scaled calibration deferred" || { echo "[2] FAIL"; ERR=1; }

# No per-stage delta table locked
grep -qiE 'per-stage.*delta.*table|delta.*table.*per-stage' "$CTL" "$PINN" && echo "[3] FAIL: per-stage delta table present (should be absent)" && ERR=1 || echo "[3] PASS: no per-stage delta table locked"

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-LOSS-03: ALL CHECKS PASSED ===" || echo "=== AC-LOSS-03: SOME CHECKS FAILED ==="
exit $ERR