#!/usr/bin/env bash
# AC-PIPE-02 (B-11 / G2): ID-resolution contract (id != array index) acceptance check.
# Disposable Phase-29 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Assertions transcribed from the landed Step-1 item-7 ID-resolution contract.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-PIPE-02: ID-resolution contract (B-11/G2) ==="

grep -qF 'record_key = (variant, fidelity, id)' "$CTL" && echo "[1] PASS: record_key identity tuple" || { echo "[1] FAIL"; ERR=1; }
grep -qF 'id_to_path' "$CTL" && echo "[2] PASS: id_to_path scan-built mapping" || { echo "[2] FAIL"; ERR=1; }
grep -qF 'equal to an array index' "$CTL" && echo "[3] PASS: dense/index-equality prohibited" || { echo "[3] FAIL"; ERR=1; }
grep -qF 'range(n_files)' "$CTL" && echo "[4] PASS: range(n_files) iteration prohibited" || { echo "[4] FAIL"; ERR=1; }
grep -qF '3958' "$CTL" && echo "[5] PASS: non-dense ID-space fact (id 3958) cited" || { echo "[5] FAIL"; ERR=1; }

# Negative control: arithmetic path computation from id must be prohibited, never permitted.
grep -qF 'NO code path may compute a path' "$CTL" \
  && echo "[6] PASS: arithmetic path-from-id prohibited (ID != index)" \
  || { echo "[6] FAIL: arithmetic path prohibition absent"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-PIPE-02: ALL CHECKS PASSED ===" || echo "=== AC-PIPE-02: SOME CHECKS FAILED ==="
exit $ERR
