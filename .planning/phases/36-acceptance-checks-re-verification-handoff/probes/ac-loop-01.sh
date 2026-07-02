#!/usr/bin/env bash
# AC-LOOP-01: replay/lookahead batching acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Assertions transcribed from Phase 34 verification.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-LOOP-01: replay/lookahead batching ==="

# B_replay=240, B_lookahead=16
grep -qF 'B_replay=240' "$CTL" && echo "[1] PASS: B_replay=240 present" || { echo "[1] FAIL"; ERR=1; }
grep -qF 'B_lookahead=16' "$CTL" && echo "[2] PASS: B_lookahead=16 present" || { echo "[2] FAIL"; ERR=1; }

# has_stage(k+1) guard
grep -qiE 'has_stage.*k.*1|k.*1.*has_stage' "$CTL" && echo "[3] PASS: has_stage(k+1) guard present" || { echo "[3] FAIL"; ERR=1; }

# Provisional status
grep -qiE 'provisional.*LOOP-01|LOOP-01.*provisional' "$CTL" && echo "[4] PASS: LOOP-01 marked provisional" || { echo "[4] FAIL"; ERR=1; }

# Edge-case policy (GAP-34-01 Option A) transcribed
grep -qiE 'GAP-34-01.*Option.*A|edge.*case.*policy.*transcribed' "$CTL" && echo "[5] PASS: edge-case policy (GAP-34-01 Option A) transcribed" || { echo "[5] FAIL"; ERR=1; }

# SI-PINN-003 citation (canonical in ctl)
grep -qF 'SI-PINN-003' "$CTL" && echo "[6] PASS: SI-PINN-003 citation present (canonical in ctl)" || { echo "[6] FAIL"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-LOOP-01: ALL CHECKS PASSED ===" || echo "=== AC-LOOP-01: SOME CHECKS FAILED ==="
exit $ERR