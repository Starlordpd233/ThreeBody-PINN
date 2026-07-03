#!/usr/bin/env bash
# AC-SI-DQA-003: conservation gate inline citation acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Inline citation on conservation/SCS gate (locked post-v1.3).

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-SI-DQA-003: conservation gate inline citation ==="

# SI-DQA-003 inline citation present
grep -qF 'SI-DQA-003' "$CTL" && echo "[1] PASS: SI-DQA-003 inline citation present" || { echo "[1] FAIL"; ERR=1; }

# Conservation gate (locked post-v1.3)
grep -qiE 'conservation.*gate|gate.*conservation' "$CTL" && echo "[2] PASS: conservation gate cited" || { echo "[2] FAIL"; ERR=1; }

# Locked post-v1.3
grep -qF 'locked post-v1.3' "$CTL" && echo "[3] PASS: locked post-v1.3 status" || { echo "[3] FAIL"; ERR=1; }

# SCS = log10(eps_H), REJECT if SCS > -5
grep -qiE 'SCS.*=.*log10.*eps_H|REJECT.*SCS.*>-5' "$CTL" && echo "[4] PASS: SCS gate formula present" || { echo "[4] FAIL"; ERR=1; }

# Plummer eps=1e-10 in V
grep -qF 'eps=1e-10' "$CTL" && echo "[5] PASS: Plummer eps=1e-10 in V" || { echo "[5] FAIL"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-SI-DQA-003: ALL CHECKS PASSED ===" || echo "=== AC-SI-DQA-003: SOME CHECKS FAILED ==="
exit $ERR