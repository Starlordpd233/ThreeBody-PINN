#!/usr/bin/env bash
# AC-SI-PINN-002: author comments preserved acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads pinn_architecture.md only; no pinn execution.
# Author comments documented for future reconciliation.

PINN="pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md"
ERR=0
echo "=== AC-SI-PINN-002: author comments preserved ==="

# SI-PINN-002 block present
grep -qF 'SI-PINN-002' "$PINN" && echo "[1] PASS: SI-PINN-002 block present" || { echo "[1] FAIL"; ERR=1; }

# Author comments documented for future reconciliation
grep -qiE 'documented.*for.*future.*reconciliation|future.*reconciliation.*documented' "$PINN" && echo "[2] PASS: documented for future reconciliation" || { echo "[2] FAIL"; ERR=1; }

# Batch-construction comment resolved under SI-PINN-003
grep -qiE 'batch-construction.*resolved.*SI-PINN-003|SI-PINN-003.*batch-construction' "$PINN" && echo "[3] PASS: batch-construction comment resolved under SI-PINN-003" || { echo "[3] FAIL"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-SI-PINN-002: ALL CHECKS PASSED ===" || echo "=== AC-SI-PINN-002: SOME CHECKS FAILED ==="
exit $ERR