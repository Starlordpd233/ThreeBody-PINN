#!/usr/bin/env bash
# AC-EVID-15-D-CONFLICT: D=6.694 conflict acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads both specs; no pinn execution.
# Assertions transcribed from Phase 32 verification.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
PINN="pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md"
ERR=0
echo "=== AC-EVID-15-D-CONFLICT: D=6.694 conflict ==="

# D ≈ 4.6416 active
grep -qF 'D ≈ 4.6416' "$CTL" && echo "[1] PASS: D ≈ 4.6416 active in ctl" || { echo "[1] FAIL"; ERR=1; }

# 6.694 absent from pinn (rejected provenance only)
grep -qF '6.694' "$PINN" && echo "[2] FAIL: D = 6.694 present in pinn (should be absent)" && ERR=1 || echo "[2] PASS: D = 6.694 absent from pinn (rejected provenance only)"

# 6.694 absent from ctl (rejected provenance only)
grep -qF '6.694' "$CTL" && echo "[3] FAIL: D = 6.694 present in ctl (should be absent)" && ERR=1 || echo "[3] PASS: D = 6.694 absent from ctl (rejected provenance only)"

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-EVID-15-D-CONFLICT: ALL CHECKS PASSED ===" || echo "=== AC-EVID-15-D-CONFLICT: SOME CHECKS FAILED ==="
exit $ERR