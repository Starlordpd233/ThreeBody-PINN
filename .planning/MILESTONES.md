# Milestones

## v1.0 Codebase Cleanup (Shipped: 2026-03-20)

**Phases completed:** 4 phases, 10 plans, 9 tasks

**Key accomplishments:**

- (none recorded)

## v1.1 LaTeX Modularization Verification (Shipped: 2026-03-22)

**Phases completed:** 4 phases (5–8)

**Key accomplishments:**

- Verified content completeness across all 5 modular LaTeX structures (automated diff)
- Confirmed preamble parity (packages, macros, commands) between original and modular preambles
- Verified structure fidelity (section hierarchy, labels, references, citations, floats)
- Confirmed all 5 modular structures compile cleanly (0 errors, 0 new warnings)

## v1.2 PINN Implementation Readiness (Shipped: 2026-05-08)

**Phases completed:** 1 phase (9), 3 plans

**Key accomplishments:**

- Consolidated 7 scattered issue reports into 3 thematic documents (01-architecture, 02-data-pipeline, 03-curriculum)
- No unique findings lost; each thematic document has distinct, non-overlapping coverage
- Produced MIGRATION.md and README.md for migration tracking; VERIFICATION-REPORT.md (PASS) and VALIDATION.md (all checks PASS)

## v1.3 Markdown Conversion Verification & Correction (Shipped: 2026-05-08)

**Phases completed:** 7 phases (10–15, 15.1), 21 plans

**Key accomplishments:**

- Verified all 6 LaTeX→markdown conversions with one-to-one injection fidelity
- Corrected 7 critical, 19 major, and 17 minor conversion errors in Phase 15.1
- Archived unselected markdown candidates to `_archive/` directories
- Produced verification reports documenting all discrepancies and fixes
- Preserved inter-document inconsistencies faithfully (deferred reconciliation to v2)
- Cleaned up stale debug sessions and quick-task artifacts from prior milestones

## v1.4 Resolving 01 Architecture and Physics Foundations (In Progress)

**Phases planned:** 6 core phases (16–21), plus inserted Phase 20.5 before Phase 21. Phases 16–19 are complete and verified. Phase 20.5 (Sampling Coordinate Allocation) design and plan locked 2026-05-20 (commit b727b15), execution pending.

**Next workflow step:**

- Phases 16–19 are complete and verified; the next workflow step is Phase 20 (architecture and normalization cleanup) — plans authored (5: 4 executable + 1 blocked by GAP-20-01), ready to execute.
- Phase 20.5 (Sampling Coordinate Allocation) design+plan locked 2026-05-20 (commit b727b15) — resolves the `u_4` Sobol double-booking flagged in `docs/findings/addressing_sobol_sequence_suggestion.md`; locks Option A from `simulation_data/Scripts/ic_generation/ic_generation_utils.py`; introduces SCOPE-05 for data-spec alignment. Plan execution pending; will run after Phase 20 completes and before Phase 21 (acceptance checks).

---
