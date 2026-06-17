#!/usr/bin/env bash
# AC-VAL-04 (PSC): STRUCTURAL phase-space-coverage-entropy clause probe.
# Disposable Phase-29 spec-consistency probe. Reads ctl_instruction.md only; no pinn touch.
#
# Two-axis status (Phase 29 D-04 / D-06):
#   STRUCTURAL axis -> executes here: the PSC clause is landed, well-formed, names the
#                      Shannon-entropy coverage diagnostic + SCR, states the ratified
#                      dedup-prefer-gold + 1/N_t composition, and cites its evidence packet.
#   NUMERIC    axis -> DEFERRED to the FUT-01 dataset-finalization gate (FO-2): this probe
#                      computes NO PSC value and asserts NO numeric constant (the grid,
#                      H/ln K normalization, SCR anchor, and first-run sanity are provisional
#                      pending the post-promotion pool).
#
# Composition transcribed (NOT invented) from the landed clause (GAP-28-03 ratified):
# one record per physical_key, dedup-prefer-gold; each trajectory weighted by 1/N_t.

CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
ERR=0
echo "=== AC-VAL-04: PSC structural clause probe ==="

# Structural assertions (no numeric value computed).
grep -qF 'Phase-Space Coverage Entropy' "$CTL" && echo "[1] PASS: PSC clause present" || { echo "[1] FAIL"; ERR=1; }
grep -qiE 'Shannon entropy' "$CTL" && grep -qiE 'report-only coverage diagnostic' "$CTL" && echo "[2] PASS: Shannon-entropy report-only coverage diagnostic" || { echo "[2] FAIL"; ERR=1; }
grep -qiE 'close-encounter coverage ratio|\bSCR\b' "$CTL" && echo "[3] PASS: companion close-encounter coverage ratio (SCR)" || { echo "[3] FAIL"; ERR=1; }
grep -qF 'dedup-prefer-gold' "$CTL" && echo "[4] PASS: dedup-prefer-gold pooled composition" || { echo "[4] FAIL"; ERR=1; }
grep -qF '1 / N_t' "$CTL" && echo "[5] PASS: trajectory-equal 1/N_t weighting" || { echo "[5] FAIL"; ERR=1; }
grep -qF 'GAP-28-03 RESOLVED-WITH-INSTRUCTION' "$CTL" && echo "[6] PASS: composition ratified (GAP-28-03 user sign-off)" || { echo "[6] FAIL"; ERR=1; }
grep -qF 'psc-coverage-entropy' "$CTL" && echo "[7] PASS: cites psc-coverage-entropy.md evidence packet" || { echo "[7] FAIL"; ERR=1; }

echo ""
[ "$ERR" -eq 0 ] && echo "AC-VAL-04 STRUCTURAL: PASS" || echo "AC-VAL-04 STRUCTURAL: FAIL"
# Numeric axis is explicitly NOT executed in Phase 29 (no PSC value computed here).
echo "AC-VAL-04 NUMERIC: DEFERRED (FUT-01 FO-2)"
exit $ERR
