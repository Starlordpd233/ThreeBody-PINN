---
phase: 20.5-sampling-coordinate-allocation
plan: "01"
subsystem: sampling-spec
tags:
  - SAMP-01
  - SAMP-02
  - SCOPE-05
  - AC-SAMP-01
key_files:
  created:
    - ".planning/phases/20.5-sampling-coordinate-allocation/20-5-DATA-ALIGNMENT.md"
    - ".planning/phases/20.5-sampling-coordinate-allocation/probes/verify_sobol_allocation.py"
  modified:
    - "pinn_instruction/markdown_conversion/framework-specs/sampling_method.md"
    - ".planning/REQUIREMENTS.md"
    - ".planning/ROADMAP.md"
    - "AGENTS.md"
    - "ANTIGRAVITY.md"
completed: 2026-06-07
---

# Phase 20.5 Summary: Sobol Coordinate Allocation

## Objective

Lock the Sobol coordinate allocation convention in `sampling_method.md` so it is
explicit, non-overlapping, and matches the data-generation code in
`simulation_data/Scripts/ic_generation/ic_generation_utils.py`, resolving the
`u_4` double-booking between scaling and velocity sampling.

## Execution Summary

Phase 20.5 executed 9 tasks across 3 stage files (`20-5-PART{1,2,3}.md`),
coordinated from the thin index (`20-5-PLAN.md`). All tasks completed
successfully.

### Tasks 1–4 (Governance scaffolding)

- **Task 1:** Added SAMP-01, SAMP-02 requirements and SCOPE-05 scope rule to
  `REQUIREMENTS.md`; bumped coverage from 30/30 to 32/32 in both REQUIREMENTS
  and ROADMAP.
- **Task 2:** Inserted Phase 20.5 details block in `ROADMAP.md` with
  dependencies on Phase 18 (FRAME) and Phase 19 (preprocessing-scaling).
- **Task 3:** Propagated SCOPE-05 governance rule to `AGENTS.md` and
  `ANTIGRAVITY.md`.
- **Task 4:** Verified pre-existing gap register (GAP-20-5-01/02/03 at
  `RESOLVED-WITH-INSTRUCTION`) — verification-only, no commit.

### Tasks 5–8 (Spec edits and verification)

- **Task 5:** Applied five spec edits to `sampling_method.md` locking the
  conditional `(δ_s, δ_v)` allocation convention ("Option A"); removed the
  obsolete double-booked velocity statement; ran FLAG-10 cross-reference check.
- **Task 6:** Created and ran the three-surface disposable verification probe
  (`verify_sobol_allocation.py`) — spec text, entrypoint AST, sampler behavior
  — all surfaces passed.
- **Task 7:** Created `20-5-DATA-ALIGNMENT.md` as a FUT-01 hand-off with the
  expanded AC-SAMP-01 acceptance check and scoped provenance claim.
- **Task 8:** Verified no separate velocity-momentum finding needed (Phase 18
  already reconciled it).

### Task 9 (Closure)

- Reran expanded AC-SAMP-01 probe — passed all three surfaces.
- Verified handoff contains both the scoped no-regeneration conclusion and the
  historical-provenance caveat.
- Final status synchronization in STATE.md, ROADMAP.md, PROJECT.md.

## Key Decisions

- **Locked convention:** Conditional `(δ_s, δ_v)` allocation — "Option A" — the
  convention the existing standard quasi-random dataset was generated under.
- **No regeneration:** Spec matches data-generator behavior; no dataset rebuild
  required.
- **Scoped provenance:** Alignment covers spec, documented configuration, and
  current sampler behavior — not a blanket historical-provenance certification.

## Commit Lineage

| Commit | Scope |
|--------|-------|
| `17ab288` | SAMP requirements + SCOPE-05 in REQUIREMENTS.md |
| `b235ef9` | ROADMAP details block |
| `916d3f8` | Spec edits locking Sobol convention |
| `3c06fca` | Disposable verification probe |
| `91408de` | Data-alignment hand-off + AC-SAMP-01 |
| `dc54738` | Phase 20.5 closure / status sync |

## Open Items

None. All three pre-existing gaps (GAP-20-5-01/02/03) resolved. No
outstanding blockers for FUT-01.
