#!/usr/bin/env bash
# AC-SI-PINN-003: batch construction inconsistency acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads both specs; no pinn execution.
# RESOLVED by Phase 34; ctl canonical.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
PINN="pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md"
ERR=0
echo "=== AC-SI-PINN-003: batch construction inconsistency ==="

# SI-PINN-003 block present in both specs
grep -qF 'SI-PINN-003' "$CTL" && echo "[1] PASS: SI-PINN-003 cited in ctl" || { echo "[1] FAIL"; ERR=1; }
grep -qF 'SI-PINN-003' "$PINN" && echo "[2] PASS: SI-PINN-003 cited in pinn" || { echo "[2] FAIL"; ERR=1; }

# RESOLVED by Phase 34
grep -qiE 'RESOLVED.*Phase.*34|Phase.*34.*RESOLVED' "$PINN" && echo "[3] PASS: RESOLVED by Phase 34" || { echo "[3] FAIL"; ERR=1; }

# ctl Mini-Batch Construction is canonical
grep -qF 'Mini-Batch Construction' "$CTL" && echo "[4] PASS: ctl Mini-Batch Construction is canonical" || { echo "[4] FAIL"; ERR=1; }

# pinn points to ctl
grep -qiE 'points.*to.*ctl|canonical.*ctl|ctl.*canonical' "$PINN" && echo "[5] PASS: pinn points to ctl (canonical)" || { echo "[5] FAIL"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-SI-PINN-003: ALL CHECKS PASSED ===" || echo "=== AC-SI-PINN-003: SOME CHECKS FAILED ==="
exit $ERR