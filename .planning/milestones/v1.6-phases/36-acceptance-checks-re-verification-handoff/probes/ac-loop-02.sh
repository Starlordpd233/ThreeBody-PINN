#!/usr/bin/env bash
# AC-LOOP-02: data vs collocation points acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Assertions transcribed from Phase 34 verification.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-LOOP-02: data vs collocation points ==="

# Two independent point sets (data-fidelity vs collocation)
grep -qiE 'independent.*point.*sets|data-fidelity.*collocation' "$CTL" && echo "[1] PASS: two independent point sets specified" || { echo "[1] FAIL"; ERR=1; }

# 8192/4096 provisional sizes
grep -qF '8192' "$CTL" && echo "[2] PASS: 8192 present (data-fidelity provisional)" || { echo "[2] FAIL"; ERR=1; }
grep -qF '4096' "$CTL" && echo "[3] PASS: 4096 present (collocation provisional)" || { echo "[3] FAIL"; ERR=1; }

# Data-fidelity 50/50 retained
grep -qiE 'data-fidelity.*50/50|50/50.*data-fidelity' "$CTL" && echo "[4] PASS: data-fidelity 50/50 retained" || { echo "[4] FAIL"; ERR=1; }

# Collocation 50/50 deferred (NOT mandated)
grep -qiE 'collocation.*50/50.*deferred|deferred.*collocation.*50/50' "$CTL" && echo "[5] PASS: collocation 50/50 deferred (NOT mandated)" || { echo "[5] FAIL"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-LOOP-02: ALL CHECKS PASSED ===" || echo "=== AC-LOOP-02: SOME CHECKS FAILED ==="
exit $ERR