#!/usr/bin/env bash
# AC-LOOP-06: dt_out collocation scaling acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Assertions transcribed from Phase 34 verification.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-LOOP-06: dt_out collocation scaling ==="

# Realized-as-deferred
grep -qiE 'realized.*deferred|deferred.*realized' "$CTL" && echo "[1] PASS: realized-as-deferred marked" || { echo "[1] FAIL"; ERR=1; }

# Candidate direction only
grep -qiE 'candidate.*direction|direction.*candidate' "$CTL" && echo "[2] PASS: candidate direction only" || { echo "[2] FAIL"; ERR=1; }

# Negative check: no probe-able collocation-scaling formula assignment
# The n_col= pattern should be absent (inverse form NOT adopted)
grep -qE 'n_col\s*=' "$CTL" && echo "[3] FAIL: n_col= formula assignment present (should be absent)" && ERR=1 || echo "[3] PASS: no probe-able n_col= formula assignment"

# Inverse form NOT adopted
grep -qiE 'inverse.*form.*NOT.*adopted|NOT.*adopted.*inverse' "$CTL" && echo "[4] PASS: inverse form NOT adopted" || { echo "[4] FAIL"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-LOOP-06: ALL CHECKS PASSED ===" || echo "=== AC-LOOP-06: SOME CHECKS FAILED ==="
exit $ERR