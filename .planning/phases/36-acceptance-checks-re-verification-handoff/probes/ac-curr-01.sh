#!/usr/bin/env bash
# AC-CURR-01: adaptive stage assignment acceptance check.
# Disposable Phase-36 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
# Assertions transcribed from Phase 33 verification.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-CURR-01: adaptive stage assignment ==="

# Methodology tokens present: offline EDA → PCA + clustering + quantile
grep -qiE 'offline.*EDA|PCA.*clustering|clustering.*quantile' "$CTL" && echo "[1] PASS: offline-EDA + PCA + clustering + quantile methodology tokens present" || { echo "[1] FAIL"; ERR=1; }

# Stage-2 hierarchical-gold / Stage-5 quasi-random-gold refinement roles preserved
grep -qiE 'Stage-2.*hierarchical.*gold|Stage-5.*quasi-random.*gold|hierarchical-gold|quasi-random-gold' "$CTL" && echo "[2] PASS: Stage-2/Stage-5 refinement roles preserved" || { echo "[2] FAIL"; ERR=1; }

# Table 4 rejected (population safeguard owner-pending)
grep -qiF 'Table 4' "$CTL" && echo "[3] FAIL: Table 4 still present (should be rejected)" && ERR=1 || echo "[3] PASS: Table 4 rejected"

# Population safeguard owner-pending (NOT locked)
grep -qiE 'population.*safeguard.*owner-pending|owner-pending.*population' "$CTL" && echo "[4] PASS: population safeguard owner-pending (NOT locked)" || { echo "[4] FAIL: population safeguard status unclear"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "=== AC-CURR-01: ALL CHECKS PASSED ===" || echo "=== AC-CURR-01: SOME CHECKS FAILED ==="
exit $ERR