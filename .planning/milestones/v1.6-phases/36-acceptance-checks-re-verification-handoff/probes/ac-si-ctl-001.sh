#!/usr/bin/env bash
# AC-SI-CTL-001: input-vector dimensionality inconsistency acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Resolved by v1.4 finding B-03 / Phase 17.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-SI-CTL-001: input-vector dimensionality inconsistency ==="

# SI-CTL-001 block present
grep -qF 'SI-CTL-001' "$CTL" && echo "[1] PASS: SI-CTL-001 block present" || { echo "[1] FAIL"; ERR=1; }

# Resolved by v1.4 finding B-03
grep -qF 'B-03' "$CTL" && echo "[2] PASS: v1.4 finding B-03 cited" || { echo "[2] FAIL"; ERR=1; }

# Phase 17 back-reference
grep -qF 'Phase 17' "$CTL" && echo "[3] PASS: Phase 17 back-reference present" || { echo "[3] FAIL"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-SI-CTL-001: ALL CHECKS PASSED ===" || echo "=== AC-SI-CTL-001: SOME CHECKS FAILED ==="
exit $ERR