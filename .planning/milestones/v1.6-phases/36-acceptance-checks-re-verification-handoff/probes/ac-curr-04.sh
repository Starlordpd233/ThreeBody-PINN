#!/usr/bin/env bash
# AC-CURR-04: L_norm clamping acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Assertions transcribed from Phase 33 verification.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-CURR-04: L_norm clamping ==="

# Raw un-clipped L_norm metadata storage. Spec uses phrase "Raw un-clipped
# $L_{\mathrm{norm}}$ storage" (line 1176) and "raw and un-clipped" continuation
# (line 1178). Accept either form paired with the L_norm token (plain or LaTeX).
if grep -qiE 'Raw un-clipped' "$CTL"; then
  echo "[1] PASS: raw un-clipped L_norm metadata storage specified (Raw un-clipped \$L_{\\mathrm{norm}}\$ storage)"
elif grep -qiE 'raw[[:space:]]+and[[:space:]]+un-clipped' "$CTL" && grep -qiE '(L_norm|L_\\\?\{?\\\?mathrm\{?norm\}?\}?)' "$CTL"; then
  echo "[1] PASS: raw un-clipped L_norm metadata storage specified (raw and un-clipped ... L_norm)"
else
  echo "[1] FAIL"
  ERR=1
fi

# Mandatory nonfinite/near-degenerate L_max diagnostic guard
grep -qiE 'nonfinite.*near-degenerate.*L_max|L_max.*nonfinite.*near-degenerate' "$CTL" && echo "[2] PASS: mandatory nonfinite/near-degenerate L_max diagnostic guard" || { echo "[2] FAIL"; ERR=1; }

# "No global clamp is authorized"
grep -qF 'No global clamp is authorized' "$CTL" && echo "[3] PASS: global clamp explicitly NOT authorized" || { echo "[3] FAIL"; ERR=1; }

# np.clip gate NOT locked (owner-pending). Spec may reference np.clip in non-locking
# context (e.g., "is NOT locked", "owner-pending"). Pass iff the np.clip mention
# carries a non-locking marker, OR np.clip is wholly absent.
if grep -qiE 'np\.clip\(' "$CTL"; then
  if grep -qiE 'np\.clip\([^)]*\).*(NOT locked|is NOT|owner-pending|deferred|defer|not adopted|reject)' "$CTL"; then
    echo "[4] PASS: np.clip mention carries non-locking (NOT locked/owner-pending) context"
  else
    echo "[4] FAIL: np.clip mentioned without non-locking marker"
    ERR=1
  fi
else
  echo "[4] PASS: np.clip gate not adopted"
fi

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-CURR-04: ALL CHECKS PASSED ===" || echo "=== AC-CURR-04: SOME CHECKS FAILED ==="
exit $ERR