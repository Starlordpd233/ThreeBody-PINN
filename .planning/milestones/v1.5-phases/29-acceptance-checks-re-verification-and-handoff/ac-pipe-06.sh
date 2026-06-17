#!/usr/bin/env bash
# AC-PIPE-06 (D7): footer / parameter-provenance contract acceptance check.
# Disposable Phase-29 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Assertions transcribed from Step-1 item-3 footer-handling contract + section 2.6.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-PIPE-06: footer / param-provenance contract (D7) ==="

grep -qF 'param_provenance' "$CTL" && echo "[1] PASS: param_provenance record present" || { echo "[1] FAIL"; ERR=1; }
grep -qF "'direct'" "$CTL" && grep -qF "'inferred'" "$CTL" && echo "[2] PASS: direct/inferred provenance values" || { echo "[2] FAIL"; ERR=1; }
grep -qF "'absent'" "$CTL" && grep -qF "'measured'" "$CTL" && echo "[3] PASS: absent/measured provenance values" || { echo "[3] FAIL"; ERR=1; }
grep -qE 'Footer present|footer-handling contract' "$CTL" && echo "[4] PASS: footer-handling contract (Step-1 item 3)" || { echo "[4] FAIL"; ERR=1; }
grep -qF 'Assertions and stored metadata' "$CTL" && echo "[5] PASS: section 2.6 stored-metadata record" || { echo "[5] FAIL"; ERR=1; }

# Negative control: footers must NOT be used as completeness signals.
NL=$(grep -nE 'Footers? MUST NOT be used as completeness|MUST NOT be\s*used as completeness' "$CTL" 2>/dev/null)
[ -n "$NL" ] && echo "[6] PASS: footers prohibited as completeness signals" || { echo "[6] FAIL: footer-completeness prohibition absent"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-PIPE-06: ALL CHECKS PASSED ===" || echo "=== AC-PIPE-06: SOME CHECKS FAILED ==="
exit $ERR
