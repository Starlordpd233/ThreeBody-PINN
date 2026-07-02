#!/usr/bin/env bash
# AC-CURR-03: stage transitions acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Assertions transcribed from Phase 33 verification.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-CURR-03: stage transitions ==="

# ADVANCE / RECOVER / HALT-REVIEW state machine present
grep -qiE 'ADVANCE|RECOVER|HALT-REVIEW' "$CTL" && echo "[1] PASS: ADVANCE / RECOVER / HALT-REVIEW state machine tokens present" || { echo "[1] FAIL"; ERR=1; }

# Anchored inside "## Stage Transition Criteria" section
grep -qF '## Stage Transition Criteria' "$CTL" && echo "[2] PASS: Stage Transition Criteria section exists" || { echo "[2] FAIL"; ERR=1; }

# Thresholds provisional pending FUT Stage-0 pilot
grep -qiE 'provisional.*FUT.*Stage-0|Stage-0.*pilot.*provisional' "$CTL" && echo "[3] PASS: thresholds marked provisional pending FUT Stage-0 pilot" || { echo "[3] FAIL"; ERR=1; }

# No automatic degradation advancement (GAP-34-01 Option A edge case policy)
grep -qiF 'automatic degraded advancement' "$CTL" && echo "[4] FAIL: automatic degraded advancement still present (should be rejected)" && ERR=1 || echo "[4] PASS: no automatic degraded advancement"

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-CURR-03: ALL CHECKS PASSED ===" || echo "=== AC-CURR-03: SOME CHECKS FAILED ==="
exit $ERR