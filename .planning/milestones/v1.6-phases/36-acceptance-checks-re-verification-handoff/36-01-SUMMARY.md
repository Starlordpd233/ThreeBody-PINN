# Plan 36-01 Execution Summary

**Plan:** Build the Phase 36 acceptance-check spine (contract manifest + probe suite)

**Executed:** 2026-07-02

## Task 1: 36-ACCEPTANCE-MANIFEST.md (contract inventory)

**Status:** ✅ COMPLETE

The manifest was authored with 26 contract rows sorted by requirement-family ID (CURR → LOOP → LOSS → EVID-15 → SI → PROTECTED-PATH-GUARD). Each row includes:
- Requirement ID
- Contract source (framework-spec section anchor)
- Pass criterion (sourced from spec + ledger + AC record, not stale prose)
- Data / expression
- Command / function (probe name)
- Expected evidence path
- Owning phase

**Manifest audit results:**
- Row count: 26 (meets >=26 requirement)
- Exact-set verification: PASS (all enumerated IDs appear exactly once in Requirement ID column)
- Pitfall-1 audit: PASS (rejected literals and bare rejected numeric values absent from pass-criteria cells)
- All required cells non-empty: PASS

## Task 2: probes/ suite + run-ac-suite.sh driver

**Status:** ✅ COMPLETE

**Probe count:** 26 probes (one per manifest row)

**Probe breakdown:**
- Formula-sanity probes (4): ac-curr-02-lmax.py, ac-loop-04.py, ac-loss-01-ad.py, ac-loss-02.py
- Spec-consistency probes (21): CURR-01/03/04/05, CURR-02-M7, LOOP-01/02/05/06/07/08, LOSS-01/03/04, EVID-15 headlines (3), SI rows (4)
- Protected-path guard (1): ac-protected-path-guard.sh

**Protected-path guard verification:**
- All probes/ scripts except ac-protected-path-guard.sh contain no pinn/ references: PASS
- run-ac-suite.sh parses clean (bash -n): PASS

## Verification

All acceptance criteria from Plan 36-01 met:
1. ✅ Manifest contains >=26 contract rows
2. ✅ All enumerated R1 contract IDs plus four SI IDs plus protected-path guard row present
3. ✅ Each enumerated ID appears exactly once (exact-set)
4. ✅ Every row has non-empty Requirement ID, Contract source, Pass criterion, Data/expression, Command/function
5. ✅ Rows sorted by requirement-family ID
6. ✅ LOOP-07/08 rows cite 34-VERIFICATION.md as evidence anchor
7. ✅ Manifest-layer Pitfall-1 audit passes (rejected literals absent)
8. ✅ probes/ contains >=26 disposable scripts
9. ✅ run-ac-suite.sh exists and parses clean
10. ✅ No script under probes/ (excluding guard) references pinn/
11. ✅ Every manifest row has corresponding probe

## Artifacts Created

| Artifact | Path |
|----------|------|
| Manifest | `.planning/phases/36-acceptance-checks-re-verification-handoff/36-ACCEPTANCE-MANIFEST.md` |
| Probe suite | `.planning/phases/36-acceptance-checks-re-verification-handoff/probes/` (26 scripts) |
| Driver | `.planning/phases/36-acceptance-checks-re-verification-handoff/run-ac-suite.sh` |
| Summary | `.planning/phases/36-acceptance-checks-re-verification-handoff/36-01-SUMMARY.md` |

## Next Steps

Proceed to **Plan 36-02**: Run the AC suite and record evidence. This will execute all 26 probes via run-ac-suite.sh, generate evidence/ output files, and create 36-PROBE-RESULTS.md with PASS/FAIL/SKIP outcomes.