# Milestones

## v1.0 Codebase Cleanup (Shipped: 2026-03-20)

**Phases completed:** 4 phases, 10 plans, 9 tasks

**Key accomplishments:**

- (none recorded)

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

**Phases planned:** 6 phases (16–21), Phase 16 complete and verified. Phase 20.5 (Sampling Coordinate Allocation) inserted 2026-05-19 between Phase 20 and Phase 21; design and plan locked (commit b727b15), execution pending.

**Next workflow step:**

- Phase 16 is complete and verified; the next workflow step is Phase 17 input and output contracts.
- Phase 20.5 (Sampling Coordinate Allocation) design+plan locked 2026-05-19 (commit b727b15) — resolves the `u_4` Sobol double-booking flagged in `docs/findings/addressing_sobol_sequence_suggestion.md`; locks Option A from `simulation_data/Scripts/ic_generation/ic_generation_utils.py`; introduces SCOPE-05 for data-spec alignment. Plan execution pending; will run after Phase 20 completes and before Phase 21 (acceptance checks).

---
