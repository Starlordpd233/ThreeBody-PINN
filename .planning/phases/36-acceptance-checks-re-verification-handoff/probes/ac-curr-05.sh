#!/usr/bin/env bash
# AC-CURR-05: s_min gate acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Assertions transcribed from Phase 33 verification.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-CURR-05: s_min gate ==="

# Unsoftened geometric s_min stage gate
grep -qiE 'geometric.*s_min.*stage.*gate|s_min.*geometric.*stage.*gate' "$CTL" && echo "[1] PASS: unsoftened geometric s_min stage gate present" || { echo "[1] FAIL"; ERR=1; }

# max(s_min, eps) rejected per PHYS-03
grep -qF 'max(s_min, eps)' "$CTL" && echo "[2] FAIL: max(s_min, eps) still present (should be rejected)" && ERR=1 || echo "[2] PASS: max(s_min, eps) rejected per PHYS-03"

# Matched-Plummer loss-side owned by Phase 35
grep -qiE 'matched-Plummer|Plummer.*matched' "$CTL" && echo "[3] PASS: matched-Plummer loss-side reference present" || { echo "[3] FAIL"; ERR=1; }

# epsilon_inv=1e-10 / epsilon_train=1e-5 dual context
grep -qF 'epsilon_inv=1e-10' "$CTL" && echo "[4] PASS: epsilon_inv=1e-10 (offline invariants) present" || { echo "[4] FAIL"; ERR=1; }
grep -qF 'epsilon_train=1e-5' "$CTL" && echo "[5] PASS: epsilon_train=1e-5 (training) present" || { echo "[5] FAIL"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-CURR-05: ALL CHECKS PASSED ===" || echo "=== AC-CURR-05: SOME CHECKS FAILED ==="
exit $ERR