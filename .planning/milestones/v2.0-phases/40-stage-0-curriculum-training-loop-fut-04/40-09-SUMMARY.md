---
phase: 40-stage-0-curriculum-training-loop-fut-04
plan: 09
subsystem: training
tags: [train-01, cr-03, gap-40-04, stage-factory, curriculum-controller, phys-05, gap-closure, live-objective]

# Dependency graph
requires:
  - phase: 40-stage-0-curriculum-training-loop-fut-04 (plans 01-08)
    provides: CurriculumController ADVANCE/RECOVER/HALT; RunController compose path; CR-01 recover restore; CR-02 boundary poll; WR-01..04 integrity
provides:
  - "CR-03 / TRAIN-01 (SC1) closed: stage_factory Option C swaps per-stage RunController on ADVANCE"
  - "Model-continuity invariant (StageFactoryModelMismatch) + T-40-09 guard extended to stage_factory"
  - "Live-objective AC: stage-1 compose receives stage-1 lambda_phys_max on real path"
  - "Docstring contract: factory-obtained per stage when injected; PLAT-01 single-stage when not"
affects: ["40 re-verification (SC1/SC4)", "41+ multi-stage callers supplying stage_factory", "43 ACC-05"]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "stage_factory: Callable[[int], RunController] | None — one seam carries ScheduledWeights+TrainingConfig+GradClipper"
    - "ADVANCE order: save stage-k-final (OLD) → stage+=1 → factory swap + model is-check → rebind → save stage-{k+1}-init (NEW) → rewarm"
    - "Option-B RED evidence: temporary schedule-only rebind fails live-objective on physics (lambda_phys=1.0 vs 7.0)"

key-files:
  created:
    - .planning/phases/40-stage-0-curriculum-training-loop-fut-04/40-09-SUMMARY.md
  modified:
    - pinn/training/controllers.py
    - pinn/training/scheduled_weights.py
    - tests/phase40/test_controllers.py
    - .planning/phases/40-stage-0-curriculum-training-loop-fut-04/40-09-PLAN.md

key-decisions:
  - "GAP-40-04 Option C BINDING: factory yields RunController (not the superseded GAP-40-03 tuple)"
  - "Model continuity is identity (is) check + typed StageFactoryModelMismatch; never assert statement"
  - "stage_factory=None default preserves single-stage PLAT-01 byte-for-byte; no built-in default factory (SCOPE-19)"
  - "stage-{k+1}-init saved AFTER swap from NEW controller (T-40-13 / composed RECOVER path)"

patterns-established:
  - "Per-stage collaborator swap via caller-supplied factory; owner supplies n_adam/max_epochs/eps/lambda^max — never invent tables in pinn/"
  - "Live-objective proof captures weights at _compose_loss_terms (wraps/call-through); factory call-count is not evidence"
  - "Meaningful RED for Option C vs B is a physics failure under schedule-only rebind, not a missing-kwarg TypeError"

requirements-completed: [TRAIN-01]

coverage:
  - id: D1
    description: "CR-03 / TRAIN-01: stage_factory seam swaps live RunController on ADVANCE; rebinds ScheduledWeights; T-40-09 mutual exclusion with forced_disposition"
    requirement: "TRAIN-01"
    verification:
      - kind: unit
        ref: "tests/phase40/test_controllers.py#StageFactorySeamTests + CurriculumControllerConstructionTests stage_factory cases"
        status: pass
    human_judgment: false
  - id: D2
    description: "Model continuity: same model identity across swap; foreign model raises StageFactoryModelMismatch with no partial rebind"
    requirement: "TRAIN-01"
    verification:
      - kind: unit
        ref: "tests/phase40/test_controllers.py#StageFactorySeamTests.test_model_continuity_preserved_across_factory_swap / test_foreign_model_from_factory_raises_and_does_not_partial_swap"
        status: pass
    human_judgment: false
  - id: D3
    description: "Anchor provenance + composed swap→RECOVER: stage-0-final carries old lambda_phys_max; stage-1-init carries new; RECOVER restore leaves stage-1 caps"
    requirement: "TRAIN-01"
    verification:
      - kind: unit
        ref: "tests/phase40/test_controllers.py#StageFactorySeamTests.test_anchor_provenance_final_from_old_init_from_new / test_composed_swap_anchor_recover_keeps_stage1_lambda_max"
        status: pass
    human_judgment: false
  - id: D4
    description: "Live-objective AC: after earned ADVANCE, weights at _compose_loss_terms equal stage-1 lambda_phys_max (not stage 0); Option-B RED recorded"
    requirement: "TRAIN-01"
    verification:
      - kind: unit
        ref: "tests/phase40/test_controllers.py#LiveObjectiveStageFactoryTests.test_stage1_compose_receives_stage1_lambda_phys_max"
        status: pass
    human_judgment: false
  - id: D5
    description: "Docstring contract: scheduled_weights module + rewarm state factory/PLAT-01; RunController Constructed-once docstring unchanged"
    requirement: "TRAIN-01"
    verification:
      - kind: other
        ref: "pinn/training/scheduled_weights.py module docstring + rewarm(); git diff docstring-only; tests.phase40.test_scheduled_weights OK"
        status: pass
    human_judgment: false

duration: 10min
completed: 2026-07-17
status: complete
---

# Phase 40 Plan 09: CR-03 stage_factory Option C Gap Closure Summary

**Per-stage RunController swap via caller-supplied stage_factory so ADVANCE trains stage k+1 against that stage's lambda^max (PHYS-05), not stage 0's**

## Performance

- **Duration:** ~10 min wall (plus full cross-phase regression)
- **Started:** 2026-07-17T14:19:36Z
- **Completed:** 2026-07-17T14:29:47Z
- **Tasks:** 3 (TDD: RED+GREEN for Task 1; test-only Task 2; docs Task 3)
- **Files modified:** 3 code/test + SUMMARY/plan docs

## Accomplishments

- Closed CR-03 / TRAIN-01 (SC1): `CurriculumController` accepts optional `stage_factory: Callable[[int], RunController] | None` (GAP-40-04 Option C). On ADVANCE it replaces the live `RunController`, rebinds `self._scheduled_weights` to the new controller's schedule, and only then saves `stage-{k+1}-init`.
- Model continuity: factory must return a controller on the same model instance (`is`); mismatch raises `StageFactoryModelMismatch` with no partial rebind. T-40-09: `stage_factory` + `forced_disposition` raises `ForcedDispositionOnLiveRun` through the single existing guard (no `assert`).
- Live-objective AC proves the composed objective uses stage 1's `lambda_phys_max` on the real `:479 → :482` path. Option-B RED (schedule-only rebind) failed with `composed lambda_phys=1.0 must equal stage-1 max 7.0`.
- Docstrings in `scheduled_weights.py` state the real factory contract and PLAT-01 single-stage default; no executable line changed. `RunController`'s "Constructed once per stage" stays and is now true.

## Task Commits

Each task was committed atomically:

1. **Task 1 RED: stage_factory seam tests** - `805e8895` (test)
2. **Task 1 GREEN: stage_factory Option C implementation** - `8970bc4d` (feat)
3. **Task 2: live-objective AC** - `a6b3dade` (test)
4. **Task 3: scheduled_weights docstring correction** - `4cf27df5` (docs)

**Plan metadata:** (this commit)

## Files Created/Modified

- `pinn/training/controllers.py` — `stage_factory` param; ADVANCE swap; `StageFactoryModelMismatch`; `RunController.model` / `.scheduled_weights` accessors; T-40-09 guard extended; CurriculumController docstring
- `pinn/training/scheduled_weights.py` — module + `rewarm()` docstring only (factory contract + PLAT-01)
- `tests/phase40/test_controllers.py` — StageFactorySeamTests, LiveObjectiveStageFactoryTests, construction ACs

## Decisions Made

- Implemented GAP-40-04 Option C exactly (factory yields `RunController`); did not implement superseded GAP-40-03 `(ScheduledWeights, TrainingConfig)` tuple.
- No built-in default factory and no per-stage `n_adam`/`max_epochs`/`eps_*` table in `pinn/` (SCOPE-19). All per-stage values in tests arrive through the seam.
- Model-continuity check is `if ... is not ...: raise StageFactoryModelMismatch` — never an `assert` (enforced by `test_exactly_one_guard_mechanism_no_alternative_assert_unset`).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Seam-test stub population under StageZeroUnderpopulated floor**
- **Found during:** Task 1 GREEN (composed RECOVER path)
- **Issue:** `n_stage0=80` / `n_stage1=80` could not build a real stage-1 batch (`StageZeroUnderpopulated: 160 < 240`).
- **Fix:** Sized seam-test sources to 300/300 (matching existing earned-ADVANCE fixtures).
- **Files modified:** `tests/phase40/test_controllers.py`
- **Verification:** `StageFactorySeamTests` green
- **Committed in:** `8970bc4d`

None other — plan executed as written (Option C shape, ordering, ACs).

## Option-B RED Evidence (load-bearing)

Temporary ADVANCE stub rebinding only `self._scheduled_weights` (leaving `self._run_controller` on stage 0):

```
AssertionError: 6.0 not less than or equal to 1e-12 :
composed lambda_phys=1.0 must equal stage-1 max 7.0
```

A bare `TypeError` on missing `stage_factory` was **not** used as RED evidence. After restoring Option C, the same test passes with captured `lambda_phys == 7.0`.

## SCOPE-19 Evidence

`rg -n stage_factory pinn/` shows only:
- parameter / storage / `None` guard / ADVANCE call site in `controllers.py`
- docstring mentions in `scheduled_weights.py`

No built-in default factory; no literal per-stage `n_adam`/`max_epochs`/`eps_*` values in `pinn/`.  
`rg` for `def set_|def reconfigure|@.*setter` in `controllers.py`: empty (Option A stays rejected).

## Test Results

| Suite | Count | Result |
|-------|-------|--------|
| tests/phase40 | 163 | OK |
| tests/phase37 | 55 | OK |
| tests/phase38 | 128 | OK |
| tests/phase39 | 264 | OK |

Pre-plan phase40 baseline was ~156; +7 from 40-09 seam + live-objective coverage. CR-01/CR-02/WR-01..04 not regressed (`RecoverRestoreBehavioralTests`, `ComposedGateEarnedAdvanceTests`, grad-clip/energy/stagnation suites still green via full phase40 run).

## Known Stubs

None. `stage_factory=None` is the intentional PLAT-01 single-stage default, not a stub preventing the plan goal.

## Self-Check: PASSED

- `pinn/training/controllers.py` — FOUND (stage_factory, StageFactoryModelMismatch, model/scheduled_weights properties)
- `pinn/training/scheduled_weights.py` — FOUND (docstring-only factory/PLAT-01 wording)
- `tests/phase40/test_controllers.py` — FOUND (StageFactorySeamTests, LiveObjectiveStageFactoryTests)
- Commits `805e8895`, `8970bc4d`, `a6b3dade`, `4cf27df5` — FOUND on `milestone/v2.0`
