#!/usr/bin/env bash
# AC-EVID-15-D05: s_min frame acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Owner Option A verification (geometric gate + matched-Plummer loss-side).

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-EVID-15-D05: s_min frame ==="

# Owner Option A (geometric gate)
grep -qiE 'Option.*A.*geometric|geometric.*Option.*A' "$CTL" && echo "[1] PASS: Owner Option A (geometric gate) cited" || { echo "[1] FAIL"; ERR=1; }

# Matched-Plummer loss-side
grep -qiE 'matched-Plummer|Plummer.*matched' "$CTL" && echo "[2] PASS: matched-Plummer loss-side reference" || { echo "[2] FAIL"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-EVID-15-D05: ALL CHECKS PASSED ===" || echo "=== AC-EVID-15-D05: SOME CHECKS FAILED ==="
exit $ERR