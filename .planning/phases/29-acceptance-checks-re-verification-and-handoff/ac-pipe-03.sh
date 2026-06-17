#!/usr/bin/env bash
# AC-PIPE-03 (M11 / G3): blacklist-exclusion contract acceptance check.
# Disposable Phase-29 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Assertions transcribed from the landed "Blacklist-exclusion contract" subsection.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-PIPE-03: blacklist-exclusion contract (M11/G3) ==="

grep -qF 'Blacklist-exclusion contract' "$CTL" && echo "[1] PASS: blacklist-exclusion contract subsection" || { echo "[1] FAIL"; ERR=1; }
grep -qF 'problematic_ics_blacklist.json' "$CTL" && echo "[2] PASS: blacklist config file named" || { echo "[2] FAIL"; ERR=1; }
grep -qF 'physical_key' "$CTL" && echo "[3] PASS: IC-level (physical_key) exclusion semantics" || { echo "[3] FAIL"; ERR=1; }
grep -qiE 'fail-closed|hard init failure' "$CTL" && echo "[4] PASS: fail-closed on missing/malformed file" || { echo "[4] FAIL"; ERR=1; }
grep -qF 'never against a hard-coded constant' "$CTL" && echo "[5] PASS: counts asserted vs parsed file, not hard-coded" || { echo "[5] FAIL"; ERR=1; }

# Negative control: the 65-IDs figure is a cross-check dataset fact, never a contract constant.
grep -qF 'not a contract constant' "$CTL" \
  && echo "[6] PASS: 65-IDs is a cross-check fact, not a contract constant" \
  || { echo "[6] FAIL: 65-IDs not framed as non-contract reference"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-PIPE-03: ALL CHECKS PASSED ===" || echo "=== AC-PIPE-03: SOME CHECKS FAILED ==="
exit $ERR
