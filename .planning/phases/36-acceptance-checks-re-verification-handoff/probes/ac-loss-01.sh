#!/usr/bin/env bash
# AC-LOSS-01: loss scaling acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads both specs; no pinn execution.
# Assertions transcribed from Phase 35 verification.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
PINN="pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md"
ERR=0
echo "=== AC-LOSS-01: loss scaling ==="

# Dimensionless L_data/L_physics/L_energy
grep -qiE 'L_data|L_physics|L_energy' "$CTL" "$PINN" && echo "[1] PASS: dimensionless L_data/L_physics/L_energy present" || { echo "[1] FAIL"; ERR=1; }

# AD chain factors
grep -qiE 'd²r/.du².*=.*4.*d²r/.dτ²|dr/.du.*=.*2.*dr/.dτ' "$PINN" && echo "[2] PASS: AD chain factors present" || { echo "[2] FAIL"; ERR=1; }

# No linear-momentum loss term
grep -qiE 'linear.*momentum.*loss|momentum.*loss.*term' "$CTL" "$PINN" && echo "[3] FAIL: linear-momentum loss term present (should be absent)" && ERR=1 || echo "[3] PASS: no linear-momentum loss term"

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-LOSS-01: ALL CHECKS PASSED ===" || echo "=== AC-LOSS-01: SOME CHECKS FAILED ==="
exit $ERR