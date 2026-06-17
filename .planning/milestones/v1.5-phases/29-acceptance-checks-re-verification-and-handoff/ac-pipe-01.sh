#!/usr/bin/env bash
# AC-PIPE-01 (B-06 / G1): Step-1A trajectory-admission-gate contract acceptance check.
# Disposable Phase-29 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Assertions transcribed from the landed Step-1A clause (ctl_instruction.md Step 1A).

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-PIPE-01: Step-1A admission gate (B-06/G1) ==="

grep -qF 'Trajectory Admission Gate' "$CTL" && echo "[1] PASS: admission-gate heading present" || { echo "[1] FAIL"; ERR=1; }
grep -qF 'runs at DataLoader init' "$CTL" && echo "[2] PASS: gate runs at DataLoader init" || { echo "[2] FAIL"; ERR=1; }
grep -qF 'Structural integrity' "$CTL" && echo "[3] PASS: structural-integrity condition" || { echo "[3] FAIL"; ERR=1; }
grep -qF 'final_timestep >= 9.5' "$CTL" && echo "[4] PASS: completeness final_timestep >= 9.5" || { echo "[4] FAIL"; ERR=1; }
grep -qF 'Conservation gate' "$CTL" && echo "[5] PASS: conservation gate (SCS) condition" || { echo "[5] FAIL"; ERR=1; }

# Negative control: the issue-doc >= 200 snapshot floor appears only in rejection context.
NL=$(grep -nE '>= ?200' "$CTL" 2>/dev/null)
if [ -n "$NL" ] && [ -z "$(echo "$NL" | grep -vE 'reject|incompatible|floor')" ]; then
  echo "[6] PASS: >= 200 snapshot floor only in rejection context"
else
  echo "[6] FAIL: >= 200 floor outside rejection context"; ERR=1
fi

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-PIPE-01: ALL CHECKS PASSED ===" || echo "=== AC-PIPE-01: SOME CHECKS FAILED ==="
exit $ERR
