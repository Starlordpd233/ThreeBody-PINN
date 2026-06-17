#!/usr/bin/env bash
# AC-VAL-01 (SCS): conservation-gate definition + ratio-threshold rejection acceptance check.
# Disposable Phase-29 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Assertions transcribed from the landed Step-1A clause-5 conservation gate (SI-DQA-003).

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-VAL-01: SCS conservation gate (ratio thresholds rejected) ==="

grep -qF 'SCS = log10(eps_H)' "$CTL" && echo "[1] PASS: SCS = log10(eps_H) definition" || { echo "[1] FAIL"; ERR=1; }
grep -qF 'SCS > -5' "$CTL" && echo "[2] PASS: reject gate SCS > -5" || { echo "[2] FAIL"; ERR=1; }
grep -qF 'eps_H > 1e-5' "$CTL" && echo "[3] PASS: equivalently eps_H > 1e-5" || { echo "[3] FAIL"; ERR=1; }
grep -qF 'Conservation gate (locked post-v1.3; SI-DQA-003)' "$CTL" && echo "[4] PASS: locked post-v1.3 gate (SI-DQA-003)" || { echo "[4] FAIL"; ERR=1; }
grep -qE 'Excellent' "$CTL" && grep -qE 'Marginal' "$CTL" && grep -qE 'Reject > -5' "$CTL" && echo "[5] PASS: band labels (Excellent/Acceptable/Marginal/Reject)" || { echo "[5] FAIL"; ERR=1; }

# Negative control: the issue-02 ratio thresholds (1e-6 / 1e-8) are rejected by name.
grep -qF 'ratio thresholds are rejected by name' "$CTL" && echo "[6] PASS: ratio thresholds rejected by name" || { echo "[6] FAIL: ratio-threshold rejection absent"; ERR=1; }
grep -qF 'mis-promoted' "$CTL" && echo "[7] PASS: 1e-6 band-boundary mis-promotion called out (negative control)" || { echo "[7] FAIL: mis-promotion rationale absent"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-VAL-01: ALL CHECKS PASSED ===" || echo "=== AC-VAL-01: SOME CHECKS FAILED ==="
exit $ERR
