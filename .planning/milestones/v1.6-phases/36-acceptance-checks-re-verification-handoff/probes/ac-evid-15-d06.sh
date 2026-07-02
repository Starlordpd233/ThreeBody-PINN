#!/usr/bin/env bash
# AC-EVID-15-D06: epsilon strategy acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Owner dual-context verification.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-EVID-15-D06: epsilon strategy ==="

# Owner dual-context
grep -qiE 'dual-context|dual.*context' "$CTL" && echo "[1] PASS: owner dual-context cited" || { echo "[1] FAIL"; ERR=1; }

# epsilon_inv = 1e-10 (offline invariants/validation). Spec uses whitespace around "=".
grep -qiE 'epsilon_inv[[:space:]]*=[[:space:]]*1e-?10' "$CTL" && echo "[2] PASS: epsilon_inv = 1e-10 (offline) present" || { echo "[2] FAIL"; ERR=1; }

# epsilon_train = 1e-5 (training)
grep -qiE 'epsilon_train[[:space:]]*=[[:space:]]*1e-?5' "$CTL" && echo "[3] PASS: epsilon_train = 1e-5 (training) present" || { echo "[3] FAIL"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-EVID-15-D06: ALL CHECKS PASSED ===" || echo "=== AC-EVID-15-D06: SOME CHECKS FAILED ==="
exit $ERR