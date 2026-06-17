#!/usr/bin/env bash
# AC-PIPE-10 (D-03): processed-training-data format (HDF5 canonical) acceptance check.
# Disposable Phase-29 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Assertions transcribed from the landed Step-1 item-6 HDF5-canonical decision.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-PIPE-10: HDF5-canonical training-data format (D-03) ==="

grep -qF 'HDF5' "$CTL" && echo "[1] PASS: HDF5 named as storage format" || { echo "[1] FAIL"; ERR=1; }
grep -qF 'single source of truth' "$CTL" && echo "[2] PASS: HDF5 = canonical single source of truth" || { echo "[2] FAIL"; ERR=1; }
grep -qF 'user-locked 2026-06-13' "$CTL" && echo "[3] PASS: decision user-locked 2026-06-13" || { echo "[3] FAIL"; ERR=1; }
grep -qiE 'round-trip' "$CTL" && echo "[4] PASS: bit-identical round-trip acceptance test" || { echo "[4] FAIL"; ERR=1; }

# Negative control: JSON/text exports must NEVER be a training input path.
grep -qF 'MUST NEVER be a training input' "$CTL" \
  && echo "[5] PASS: JSON/text exports barred from training input path" \
  || { echo "[5] FAIL: JSON/text training-input prohibition absent"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-PIPE-10: ALL CHECKS PASSED ===" || echo "=== AC-PIPE-10: SOME CHECKS FAILED ==="
exit $ERR
