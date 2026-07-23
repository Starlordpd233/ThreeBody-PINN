---
phase: 39-data-ingestion-stage-0-population-scan
plan: "05"
subsystem: data
tags: [replay, lookahead, gumbel-top-k, collocation, stage-index, provenance]

# Dependency graph
requires:
  - phase: 39-04
    provides: "Immutable persisted-label StageIndex, train-restricted StageIndex.from_split seam, and deterministic physical-group split manifest"
provides:
  - "Deterministic cumulative replay and adjacent-stage lookahead selection with fail-closed StageQuery validation"
  - "Model-ready observed data-fidelity points with mixed acceleration-weighted/uniform snapshot sampling and auditable provenance"
  - "Independent fixed physics-collocation points with exact seeded quotient/remainder identity balance"
affects: [39-06, 39-07, 40-training-loop]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Caller-owned NumPy Generator supplies every selection and point-sampling draw without global RNG mutation"
    - "Train-restricted StageIndex delegates resident snapshot access to its admitted adapter"
    - "Global T_CHARACTERISTIC_TIME normalizes both observed and continuous physics times"

key-files:
  created:
    - pinn/data/batches.py
  modified:
    - pinn/data/adapter.py
    - pinn/data/splits.py
    - pinn/data/types.py
    - tests/phase39/test_batches.py

key-decisions:
  - "Replay samples 240 identities without replacement from D<=k; present adjacent stages contribute exactly 16 identities, padding only nonempty undersized pools with replacement."
  - "Each selected trajectory contributes min(32,n_snapshots) unique observed points, split between floor(n/2) acceleration-weighted Gumbel top-k draws and uniform draws from the remainder."
  - "Collocation count is fixed exactly by GAP-39-12 Option C q/r quotas, with seeded remainder recipients and continuous Uniform[0,10] times; adaptive density remains Phase 40 ownership."

patterns-established:
  - "FixedBatch contains two independent typed point sets and explicit replay/lookahead identity provenance; it has no per-record T field."
  - "Every candidate and emitted identity is revalidated as original/base hierarchical Set 1a, non-blacklisted, and never numerically gold."

requirements-completed: [DATA-05]

coverage:
  - id: D1
    description: "Cumulative replay, adjacent-stage lookahead, replacement padding, missing-stage behavior, local RNG, and fail-closed identity selection"
    requirement: DATA-05
    verification:
      - kind: unit
        ref: "tests/phase39/test_batches.py#SelectionContract"
        status: pass
    human_judgment: false
  - id: D2
    description: "Mixed unique data-fidelity snapshot sampling with global-T model inputs, aligned targets/masses, provenance, and network-compatible shapes"
    requirement: DATA-05
    verification:
      - kind: unit
        ref: "tests/phase39/test_batches.py#FullBatchContract"
        status: pass
      - kind: integration
        ref: "tests/phase39/test_batches.py#FullBatchContract.test_real_network_accepts_model_facing_batch_shapes"
        status: pass
    human_judgment: false
  - id: D3
    description: "Exact deterministic GAP-39-12 balanced collocation quotas and train-restricted StageIndex-to-FixedBatch integration"
    requirement: DATA-05
    verification:
      - kind: unit
        ref: "tests/phase39/test_batches.py#CollocationQuotaTests"
        status: pass
      - kind: integration
        ref: "tests/phase39/test_batches.py#FullBatchContract.test_train_restricted_stage_index_emits_only_train_keys"
        status: pass
    human_judgment: false

# Metrics
duration: 8min
completed: 2026-07-15
status: complete
---

# Phase 39 Plan 05: Fixed Two-Point-Set Batch Construction Summary

**The DATA-04 train-restricted `StageIndex` now builds deterministic replay/lookahead batches containing aligned observed snapshots and an independent, exactly balanced continuous physics-collocation set.**

## Performance

- **Duration:** 8 min
- **Started:** 2026-07-15T10:45:42Z
- **Completed:** 2026-07-15T10:53:06Z
- **Tasks:** 2
- **Files modified:** 5 production/test files (plus this summary and the DATA-05 requirement status)

## Accomplishments

- Implemented the canonical `select_stage_records` selector: 240 seeded replay identities from cumulative `D<=k`, 16 adjacent-stage lookahead identities when present, replacement padding only for nonempty pools below 16, and a typed Stage-0 underpopulation failure.
- Built observed data-fidelity points with `min(32,n_snapshots)` unique indices per identity, half acceleration-weighted Gumbel top-k and half uniform from the remaining snapshots, aligned raw masses/position targets/provenance, and global `T=10` normalization to `(N,14)` `[tau,IC13]` inputs.
- Built exactly 4,096 independent continuous physics-collocation points by seeded near-even quotient/remainder quotas over selected identities; returned model-ready dtype/device tensors without adaptive density, epoch ownership, or per-record `T` state.
- Completed the production integration path `StageIndex.from_split(adapter, manifest, "train") -> build_stage_batch(...)`, preserving split restriction while accessing the adapter's resident trajectories.

## Task Commits

Both tasks followed RED -> GREEN TDD and were committed atomically through `scripts/agent-commit`:

1. **Task 39-05-01 RED: replay/lookahead selection contract** — `842445b0` (test)
2. **Task 39-05-01 GREEN: deterministic trajectory selection** — `46b22441` (feat)
3. **Task 39-05-02 RED: independent two-point-set contract** — `0a1877cb` (test)
4. **Task 39-05-02 GREEN: observed data and balanced collocation assembly** — `56c223c9` (feat)

**Plan metadata:** this SUMMARY plus `.planning/REQUIREMENTS.md` (docs commit)

## Files Created/Modified

- `pinn/data/batches.py` — replay/lookahead selection, data-fidelity snapshot sampling, balanced continuous collocation sampling, and fixed batch assembly.
- `pinn/data/adapter.py` — resident snapshot accessors and finite-difference acceleration magnitudes for DATA-05 sampling.
- `pinn/data/splits.py` — train-restricted source retention and snapshot delegation through `StageIndex.from_split`.
- `pinn/data/types.py` — aligned target, time, identity, snapshot, sampling-kind, replay, and lookahead provenance fields.
- `tests/phase39/test_batches.py` — activated and extended DATA-05 selection, quota, point-set, alignment, network-shape, hard-failure, and production split-integration coverage.

## Decisions Made

- **Keep all stochasticity caller-owned and local.** Selection, Gumbel ranking, uniform snapshot choice, quota remainder assignment, and continuous time draws consume only the supplied `numpy.random.Generator`.
- **Use observed resident velocities for acceleration weights.** The adapter computes one finite-difference acceleration norm per resident snapshot; the weighting affects only the observed data set and does not define physics-collocation density.
- **Canonicalize collocation output after quota assignment.** Record keys and times are sorted after seeded draws so equal inputs and seeds produce identical tensors and metadata while quota recipients remain seeded.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking cross-plan interface gap] Preserved resident snapshot access through train-restricted StageIndex**
- **Found during:** Task 39-05-02 production integration
- **Issue:** Plan 39-04's `StageIndex.from_split(adapter, manifest, split_name)` retained immutable record metadata but discarded the adapter reference, so the required DATA-05 path could select train identities but could not read their resident times, positions, velocities, or acceleration inputs.
- **Fix:** Train-restricted `StageIndex` instances retain the admitted source privately and delegate checked snapshot/acceleration accessors for keys present in the split. Direct `StageIndex(records)` remains metadata-only unless its records explicitly provide those surfaces.
- **Files modified:** `pinn/data/splits.py`, `tests/phase39/test_batches.py`
- **Verification:** `FullBatchContract.test_train_restricted_stage_index_emits_only_train_keys`
- **Committed in:** `56c223c9`

**2. [Rule 3 - Blocking frozen-type completeness] Added DATA-05 targets and provenance to point-set types**
- **Found during:** Task 39-05-02 model-ready assembly
- **Issue:** The frozen Wave-0 point-set dataclasses contained only model inputs/masses (and collocation times), but the plan requires observed position targets, sample provenance, collocation identity provenance, and explicit replay/lookahead identities.
- **Fix:** Extended the existing frozen dataclasses with exactly the required aligned fields. No per-record `T`, optimizer state, epoch state, or Phase-40 adaptive state was introduced.
- **Files modified:** `pinn/data/types.py`, `pinn/data/batches.py`, `tests/phase39/test_batches.py`
- **Verification:** `FullBatchContract.test_batch_emits_two_distinct_point_sets_with_aligned_shapes`; `test_fixture_ic13_masses_targets_and_provenance_stay_aligned`
- **Committed in:** `56c223c9`

---

**Total deviations:** 2 auto-fixed blocking interface/type gaps. **Impact:** both fixes make the already-required DATA-04 -> DATA-05 production path executable without changing its public signature or entering Phase-40 adaptive/training ownership.

## Issues Encountered

None beyond the two blocking interface/type gaps recorded above.

## Known Stubs

None. No placeholder values, TODO/FIXME markers, global RNG mutation, or adaptive collocation policy exists in the files changed by this plan.

## User Setup Required

None. Real-corpus scan execution and artifact production remain Plan 39-06/39-07 responsibilities.

## Next Phase Readiness

- Plan 39-06 may consume the completed adapter, manifest, and StageIndex surfaces for scan orchestration; this plan did not create or modify any Plan-39-06 source, test, summary, or artifact.
- Phase 40 may consume `FixedBatch` and may later replace only the fixed collocation-density policy under TRAIN-04; DATA-05 owns no epoch or adaptive state.
- DATA-06 remains pending.

## Self-Check: PASSED

- `pinn/data/batches.py`, `tests/phase39/test_batches.py`, and this SUMMARY exist on disk.
- TDD commits `842445b0`, `46b22441`, `0a1877cb`, and `56c223c9` exist in `milestone/v2.0` history.
- Focused batch suite: 27 tests, 0 failures, 0 skips.
- Full Phase-39 discovery: 211 tests, 0 failures, 9 intentional future Plan-39-06 skips.
- DATA-05 is complete in both REQUIREMENTS checklist and traceability table; DATA-06 remains pending.
- `git diff --check` passes; Plan-39-06 files and artifacts remain untouched.

---
*Phase: 39-data-ingestion-stage-0-population-scan*
*Completed: 2026-07-15*
