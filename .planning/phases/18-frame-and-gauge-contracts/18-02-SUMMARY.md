---
phase: 18-frame-and-gauge-contracts
plan: 02
subsystem: pinn-framework-spec
tags: [sampling-method, frame-reconciliation, simulation-data, ac-frame-01, phase-20-5-boundary]

# Dependency graph
requires:
  - phase: 18-frame-and-gauge-contracts
    provides: "18-01 unified FRAME-01 preprocessing pipeline and B-05/M3 evidence packets"
provides:
  - "FRAME-03 sampling-frame notes in sampling_method.md for hierarchical and standard quasi-random ICs"
  - "Verification that simulation_data/Scripts/ic_generation remains the authoritative source for sampling-frame claims"
  - "B-05 advanced to FIX_APPLIED, explicitly not VERIFIED, pending 18-03 full structural closure"
  - "Phase 20.5 Sobol coordinate-allocation text preserved for later section-anchor relocation"
affects: [18-03, 20.5, 21, FUT-01]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "simulation_data/ is authoritative only for FRAME-03 sampling_method.md claims"
    - "Phase 18 sampling edits avoid the Sobol coordinate-allocation paragraph reserved for Phase 20.5"

key-files:
  created: []
  modified:
    - "pinn_instruction/markdown_conversion/framework-specs/sampling_method.md - FRAME-03 hierarchical and quasi-random frame notes"
    - ".planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-05.md - Sampling before/after note and FIX_APPLIED status"
    - ".planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md - B-05 FIX_APPLIED ledger transition"

key-decisions:
  - "Applied D-09: hierarchical and quasi-random frame behavior is documented, but unrelated sampling prose is left alone."
  - "Applied D-10: FRAME-03 claims were checked against generate_ics.py, ic_generation_utils.py, and the dataset README before editing."
  - "Applied D-11/GAP-18-02: the Phase 20.5 Sobol coordinate-allocation target remains untouched."
  - "Post-review correction: aligned the adjacent quasi-random momentum-conservation sentence with D-10's authoritative generator behavior (`v1 = -v2/2`, `v3 = -v2/2`) without touching the Sobol coordinate-allocation target."

patterns-established:
  - "B-05 can move to FIX_APPLIED after the FRAME-03 spec edit, but it remains lifecycle-gated until 18-03 verifies the full AC-FRAME-01 structural set."

requirements-completed:
  - FRAME-03
  - VER-05

# Metrics
duration: ~3min
completed: 2026-05-21T05:24:43Z
---

# Phase 18 P02: Sampling Frame Reconciliation Summary

**The sampling spec now records hierarchical post-perturbation offsets and quasi-random COM/P-by-construction behavior, with B-05 held at FIX_APPLIED for final verification.**

## Performance

- **Duration:** ~3 min
- **Started:** 2026-05-21T05:21Z
- **Completed:** 2026-05-21T05:24:43Z
- **Tasks:** 3 plan tasks + plan summary
- **Files modified:** 3 plus this summary and state bookkeeping

## Accomplishments

- Verified the standard quasi-random generator uses `p3_batch = -(p1_scaled + p2_batch)`, `v1_batch = -v2_batch / 2`, `v3_batch = -v2_batch / 2`, and `scale_range=(0.8, 1.2)`.
- Verified the hierarchical generator applies COM/P adjustment before `perturbation = 0.01` and applies `np.random.normal(0, perturbation, 3)` to all positions and velocities.
- Added FRAME-03 frame notes to `sampling_method.md` for hierarchical offsets and quasi-random COM/P behavior.
- Confirmed the Phase 20.5 Sobol coordinate-allocation target text remains untouched.
- Updated B-05 to `FIX_APPLIED`, not `VERIFIED`, pending 18-03 full verification.

## Task Commits

1. **Task 1: Confirm authoritative sampling-frame facts** - no mutation; verification passed against `simulation_data/`.
2. **Task 2: Patch sampling_method.md frame behavior** - `a940474` (docs: reconcile sampling frame behavior)
3. **Task 3: Record B-05 sampling fix application** - `783c5a5` (docs: record sampling frame fix)
4. **Post-review correction: Align quasi-random momentum prose** - `34cd746` (docs: align quasi-random momentum prose)

## Files Created/Modified

- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` - Added hierarchical and quasi-random FRAME-03 frame notes.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-05.md` - Added sampling-method before/after note and changed status to `FIX_APPLIED`.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` - Updated B-05 row and transition log to `FIX_APPLIED`.

## Verification

- **Task 1 source gate:** PASS - all required sampling facts are present in `simulation_data/` scripts and README.
- **Task 2 sampling gate:** PASS - both FRAME-03 notes exist, the `u_4/u_5/u_6` Sobol text remains, and the Phase 20.5 heads-up remains in the milestone gap index.
- **Task 3 lifecycle gate:** PASS - B-05 is `FIX_APPLIED`, no B-05 ledger row is `VERIFIED`, and the sampling-frame transition is recorded.
- **Post-review prose gate:** PASS - the quasi-random momentum sentence now matches `ic_generation_utils.py` (`v1_batch = -v2_batch / 2`, `v3_batch = -v2_batch / 2`) and the Phase 20.5 `u_4/u_5/u_6` target text remains.

## Deviations from Plan

Post-review correction only: the mandatory review gate found that the adjacent inherited quasi-random momentum sentence conflicted with the D-10-authoritative generator behavior. The fix is source-backed FRAME-03 prose and does not touch the Phase 20.5 Sobol coordinate-allocation target.

## Issues Encountered

None.

## Gap Handling

No new gaps were encountered. GAP-18-02 remained resolved and governed the boundary around the Phase 20.5 Sobol coordinate-allocation target; D-10 explicitly grounded the post-review momentum-prose correction in `simulation_data/`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plan 18-03 can proceed with `18-CODE-DIVERGENCE.md`, final AC-FRAME-01 structural verification, and B-05 closure if the full criteria set passes.

## Self-Check: PASSED

- No file under `pinn/` was modified.
- Task commits are present in git history.
- B-05 is `FIX_APPLIED`, not `VERIFIED`.
- `sampling_method.md` preserves the Phase 20.5 Sobol coordinate-allocation target text.

---
*Phase: 18-frame-and-gauge-contracts*
*Completed: 2026-05-21*
