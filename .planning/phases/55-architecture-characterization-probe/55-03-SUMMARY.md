---
phase: 55-architecture-characterization-probe
plan: 03
subsystem: testing
tags: [pinn, verification, architecture-characterization, stratified-bins, d-03, inst-04]

requires:
  - phase: 55-architecture-characterization-probe
    provides: SweepCase, ArchitectureCharacterizationResult, DEFAULT_CASES, measure_case, run_sweep, main
  - phase: 54-recalibration-decision-grounding
    provides: 54-RULING.md batch allocation and bin policy
affects: [56-contract-amendment-train-free-gate, 55-04]

provides:
  - RATIFIED_N_BINS/PER_BIN/TOTAL transcribed from 54-RULING.md B2/D3
  - stratified_collocation_times and bin_mean_residuals as pure numpy helpers
  - synthetic-only unit tests for the 16-bin / 256-per-bin structure
  - AST call-graph and causal-point recorder tests enforcing D-03 containment

actuals:
  tokens: 3675
  tasks: 3
  commits: 2
plan_head_before: bee5871f50d8bee2be1dc9abb10c994ab2e28a45

tech-stack:
  added: []
  patterns:
    - D-03 capability-without-exercise: helpers exist, default path cannot reach them
    - CollocationSampler caller-owned Generator policy on stratified draws
    - AST call-graph closure with non-vacuity guard for mechanical prohibition

key-files:
  created: []
  modified:
    - pinn/verification/architecture_characterization_probe.py
    - tests/phase55/test_architecture_characterization.py
    - .planning/phases/55-architecture-characterization-probe/55-VALIDATION.md

key-decisions:
  - "Checkpoint Task 1: selected contain (CONTEXT.md D-03 locked)"
  - "Helpers are synthetic-only in Phase 55; Phase 56 owns real wiring and R_ref provenance"

patterns-established:
  - "Pattern: RATIFIED_* constants cite 54-RULING.md B2/D3; last bin is closed, others half-open"
  - "Pattern: containment is an AST closure from run_sweep/measure_case/main plus a DEFAULT_N_COL recorder"

requirements-completed: [INST-04]

coverage:
  - id: D1
    description: stratified_collocation_times returns 4096 ascending times with exactly 256 entries in each of 16 ratified bins
    requirement: INST-04
    verification:
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_stratified_bins_synthetic
        status: pass
    human_judgment: false
  - id: D2
    description: bin_mean_residuals returns 16 closed-form arithmetic means on a synthetic arange and rejects mismatch, OOR index, and empty bins
    requirement: INST-04
    verification:
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_bin_mean_residuals_synthetic
        status: pass
    human_judgment: false
  - id: D3
    description: AST call-graph closure from run_sweep/measure_case/main reaches neither new-structure helper
    requirement: INST-04
    verification:
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_new_structure_helpers_unreachable_from_default_sweep
        status: pass
    human_judgment: false
  - id: D4
    description: Every causal_physics_loss call in default run_sweep() and main([]) receives exactly DEFAULT_N_COL residuals
    requirement: INST-04
    verification:
      - kind: unit
        ref: tests/phase55/test_architecture_characterization.py#test_default_sweep_never_exceeds_sixteen_causal_points
        status: pass
    human_judgment: false
  - id: D5
    description: D-03 contain checkpoint recorded; Phase 55 produced no 4096-structure measurement and no R_ref
    requirement: INST-04
    verification:
      - kind: other
        ref: git status --short .planning/phases/55-architecture-characterization-probe/evidence/
        status: pass
    human_judgment: false

duration: 8min
completed: 2026-09-06
status: complete
---

# Phase 55 Plan 03: Contained 4096-Bin Stratified Helpers Summary

**Pure numpy 16-bin / 256-per-bin collocation helpers transcribed from 54-RULING.md, unit-tested on synthetic arrays, and proven unreachable from the default 16-point sweep**

## Performance

- **Duration:** 8 min
- **Started:** 2026-09-06T03:33:37Z
- **Completed:** 2026-09-06T03:41:30Z
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments

- Checkpoint Task 1 selected `contain` (CONTEXT.md D-03 locked; orchestrator `user_response: contain`). No `## CHECKPOINT REACHED` halt.
- `stratified_collocation_times` and `bin_mean_residuals` land with `RATIFIED_N_BINS=16`, `RATIFIED_PER_BIN=256`, `RATIFIED_TOTAL=4096`. Bin edges match 54-RULING.md: `[b/16,(b+1)/16)` for `b=0..14` and `[15/16,1]` for the last bin.
- Synthetic tests lock cardinality, per-bin count, membership, determinism, Generator-owned RNG, closed-form bin means `256*b+127.5`, and the three `ValueError` rejections.
- Two mechanical containment tests prove the helpers are absent from the `run_sweep`/`measure_case`/`main` call-graph and that every default-path `causal_physics_loss` call receives exactly `DEFAULT_N_COL=16` residuals.
- Phase 55 produced no 4096-point measurement, no `R_ref`, and no evidence artifact under `evidence/`.

## Task Commits

Each task was committed atomically:

1. **Task 1: Confirm the D-03 containment contract** - no commit (checkpoint recorded as `contain`)
2. **Task 2: Ratified 16-bin stratified sampling and bin-mean reduction** - `c20691f9` (feat)
3. **Task 3: Mechanical containment tests and validation-row flip** - `b599444f` (test)

**Plan metadata:** pending this SUMMARY commit

## Files Created/Modified

- `pinn/verification/architecture_characterization_probe.py` - `RATIFIED_*` constants, `stratified_collocation_times`, `bin_mean_residuals`; default sweep unwired
- `tests/phase55/test_architecture_characterization.py` - synthetic bin tests plus AST/recorder containment tests
- `.planning/phases/55-architecture-characterization-probe/55-VALIDATION.md` - `55-03-T2` and `55-03-T3` Status rows flipped green

## Decisions Made

- Checkpoint Task 1: selected `contain` (CONTEXT.md D-03 locked). `defer` would contradict D-03.
- Helpers take no `dtype`/`device` argument and construct no tensor. Phase 56 owns wiring them into a real measurement and the reference-scale provenance record.

## Deviations from Plan

None - plan executed exactly as written.

### Execution notes (non-blocking)

**1. [process] Task 1 checkpoint auto-resolved as contain**
- **Found during:** Task 1
- **Issue:** Plan emits `checkpoint:decision` gate=blocking. Orchestrator already resolved it to `contain`.
- **Fix:** Recorded the selection in this SUMMARY and continued to Tasks 2 and 3 without emitting `## CHECKPOINT REACHED`.
- **Impact:** Required by the executor prompt; matches locked D-03.

**2. [process] Negative-control edits were applied then reverted**
- **Found during:** Task 3
- **Issue:** Acceptance requires demonstrated fail-first behavior with the tree left unchanged.
- **Fix:** Temporary `bin_mean_residuals(...)` inside `run_sweep` made `test_new_structure_helpers_unreachable_from_default_sweep` fail (`leaked ['bin_mean_residuals']`). Temporary `run_sweep(n_col=32)` made `test_default_sweep_never_exceeds_sixteen_causal_points` fail with residual counts `[32, 32, 32, 32, 32, 32, 16, 16, 16, 16, 16, 16]`. Both edits reverted; `git diff` on the probe vs Task 2 was empty before the Task 3 commit.
- **Impact:** Required by the plan; no residual production change.

---

**Total deviations:** 0 auto-fixed. 2 documented process notes.
**Impact on plan:** None on shipped behavior.

## Issues Encountered

- `.planning/phases/55-architecture-characterization-probe/evidence/` does not exist; `git status --short` on that path reported the directory absent. No measurement artifact was produced.
- Plan-level `pytest tests/ -q` failure-set diff was not re-run. Required gate `.venv/bin/python -m pytest tests/phase55/ -q` passed 43 tests. The 55-01 full-suite record (pre-existing archive failures outside `tests/phase55/`) is unchanged by these pure-numpy helpers.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Ready for 55-04: Tier-2 exact-value fixture and the one committed 16-point evidence run.
- Do not wire the new-structure helpers into `run_sweep`/`measure_case`/`main` in 55-04.
- Do not present any output as `R_ref` or GATE-04 evidence. That measurement remains Phase 56.

## Self-Check: PASSED

- FOUND: `pinn/verification/architecture_characterization_probe.py`
- FOUND: `tests/phase55/test_architecture_characterization.py`
- FOUND: `.planning/phases/55-architecture-characterization-probe/55-VALIDATION.md`
- FOUND: `.planning/phases/55-architecture-characterization-probe/55-03-SUMMARY.md`
- FOUND: commit `c20691f9` feat(55-03): add ratified stratified bin helpers
- FOUND: commit `b599444f` test(55-03): enforce new-structure helper containment
- FOUND: `.venv/bin/python -m pytest tests/phase55/ -q` — 43 passed
- FOUND: Checkpoint Task 1 recorded as `contain`

---
*Phase: 55-architecture-characterization-probe*
*Completed: 2026-09-06*
