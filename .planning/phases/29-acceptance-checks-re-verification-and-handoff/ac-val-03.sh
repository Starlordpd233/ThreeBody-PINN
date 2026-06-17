#!/usr/bin/env bash
# AC-VAL-03 (IPR): interpolation-physics-residual raw-G=1 + dual-epsilon contract check.
# Disposable Phase-29 spec-consistency probe. Reads ctl_instruction.md + pinn_architecture.md
# (read-only); no pinn touch. Assertions transcribed from the landed IPR clause + arch 3.4 note.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ARCH="pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md"
ERR=0
echo "=== AC-VAL-03: IPR raw-G=1 + dual-epsilon contract ==="

grep -qF 'Interpolation Physics Residual' "$CTL" && echo "[1] PASS: IPR clause present" || { echo "[1] FAIL"; ERR=1; }
grep -qF 'raw `G = 1` units' "$CTL" && echo "[2] PASS: raw G=1 units convention" || { echo "[2] FAIL"; ERR=1; }
grep -qF 'GAP-28-02 RESOLVED-WITH-INSTRUCTION' "$CTL" && echo "[3] PASS: GAP-28-02 user sign-off cited" || { echo "[3] FAIL"; ERR=1; }
grep -qF 'CubicHermiteSpline' "$CTL" && grep -qF 'PchipInterpolator' "$CTL" && echo "[4] PASS: velocity-carrying Hermite spline (Pchip prohibited)" || { echo "[4] FAIL"; ERR=1; }
grep -qF 'eps_inv = 1e-10' "$CTL" && echo "[5] PASS: validation softening eps_inv = 1e-10" || { echo "[5] FAIL"; ERR=1; }

# Dual-epsilon (PHYS-03): data-side eps_inv distinct from training epsilon_train (arch 3.4).
grep -qF 'epsilon_train = 1e-5' "$CTL" && echo "[6] PASS: dual-epsilon note distinguishes epsilon_train = 1e-5" || { echo "[6] FAIL"; ERR=1; }
if grep -qF 'epsilon_train' "$ARCH"; then
  echo "[7] PASS: pinn_architecture 3.4 dual-epsilon note present (read-only cross-check)"
else
  echo "[7] FAIL: arch 3.4 epsilon_train note absent"; ERR=1
fi

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-VAL-03: ALL CHECKS PASSED ===" || echo "=== AC-VAL-03: SOME CHECKS FAILED ==="
exit $ERR
