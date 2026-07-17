---
phase: 40-stage-0-curriculum-training-loop-fut-04
plan: 07
subsystem: training
tags: [train-02, train-06, cr-01, cr-02, recover-restore, stage-exit-boundary, gap-closure, pinn-training-loop]

# Dependency graph
requires:
  - phase: 40-stage-0-curriculum-training-loop-fut-04 (plans 01-06)
    provides: RunController + CurriculumController composition layer; CheckpointStore.rollback payload with run_controller; StageExitMachine.evaluate precedence; ratified GAP-40-01/02 rulings
provides:
  - "CR-01 closed: CurriculumController.step() RECOVER branch restores RunController state from CheckpointStore.rollback() payload before retry decision"
  - "CR-02 closed: RunController.run_stage polls StageExitMachine at n_adam==max_epochs zero-L-BFGS-headroom boundary (ADVANCE reachable when gate holds)"
  - "WR-05 closed: source-text grep test deleted; replaced by parameter-level behavioral RECOVER-restore tests"
affects: ["40-08/40-09 gap plans", "41 (resume/checkpoint)", "43 (Stage-0 pilot inherits RECOVER restore + boundary ADVANCE)"]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "RECOVER restore inside existing EmptyCheckpointStore try — dual guard (live run_controller AND payload key) so forced-disposition and seed-without-run_controller paths stay safe"
    - "Zero-headroom boundary polls the SAME StageExitMachine.evaluate (no second ADVANCE path); HALT/None fallback preserves non-Optional run_stage return"
    - "TDD red-commit-then-green-commit for gap closures that shipped under a green suite (red commit is the proof the defect was real)"

key-files:
  created:
    - .planning/phases/40-stage-0-curriculum-training-loop-fut-04/40-07-SUMMARY.md
  modified:
    - pinn/training/controllers.py
    - tests/phase40/test_controllers.py
    - tests/phase40/test_optimizer_phase.py

key-decisions:
  - "Followed GAP-40-01 → B and GAP-40-02 → A as already adjudicated; did not re-decide, did not tighten StageConfig to n_adam < max_epochs"
  - "CR-03 / stage_factory deliberately out of scope (owned by 40-09); no scheduled_weights docstring edits"
  - "Boundary poll does not rewarm ScheduledWeights (freeze never ran on zero-headroom path)"

patterns-established:
  - "Gap-closure TDD for controller wiring: behavioral RED test against live objects first (parameter tensors / returned dispositions), then minimal composition-layer fix — never spy call_count or inspect.getsource for restore/ADVANCE claims"

requirements-completed: [TRAIN-02, TRAIN-06]

coverage:
  - id: D1
    description: "CR-01 / TRAIN-06: RECOVER restores model (+ schedule + clipper via RunController.load_state_dict) from rolled-back checkpoint payload before retry decision; recover_retries=0 still HALTs with no retrain; empty-store backstop preserved"
    requirement: "TRAIN-06"
    verification:
      - kind: unit
        ref: "tests/phase40/test_controllers.py#RecoverRestoreBehavioralTests (3 tests: retries=1 restore+RECOVER; retries=0 restore+HALT; live empty-store no crash)"
        status: pass
      - kind: unit
        ref: "tests/phase40/test_controllers.py#ForcedDispositionDispatchTests.test_forced_recover_at_retries_zero_rolls_back_and_halts_with_no_retrain (unmodified)"
        status: pass
    human_judgment: false
  - id: D2
    description: "CR-02 / TRAIN-02+TRAIN-06: at n_adam==max_epochs zero L-BFGS headroom, run_stage polls StageExitMachine once — ADVANCE when all four gate criteria hold, HALT when unmet; StageConfig equality still legal"
    requirement: "TRAIN-02"
    verification:
      - kind: unit
        ref: "tests/phase40/test_optimizer_phase.py#test_zero_lbfgs_headroom_boundary_advances_when_gate_satisfied"
        status: pass
      - kind: unit
        ref: "tests/phase40/test_optimizer_phase.py#test_zero_lbfgs_headroom_boundary_halts_when_gate_unmet"
        status: pass
      - kind: unit
        ref: "tests/phase40/test_config.py#test_n_adam_eq_max_epochs_ok"
        status: pass
    human_judgment: false
  - id: D3
    description: "WR-05: deleted source-text grep test_recover_branch_catches_empty_checkpoint_store; RECOVER coverage is behavioral only"
    requirement: "TRAIN-06"
    verification:
      - kind: unit
        ref: "tests/phase40/test_controllers.py (no inspect.getsource in RECOVER tests; only T-40-09 guard test keeps getsource)"
        status: pass
    human_judgment: false

duration: 12min
completed: 2026-07-17
status: complete
---

# Phase 40 Plan 07: CR-01/CR-02 Gap Closure Summary

**RECOVER restores rolled-back RunController state; zero-L-BFGS-headroom boundary polls stage-exit so ADVANCE is reachable when the gate holds**

## Performance

- **Duration:** 12 min
- **Started:** 2026-07-17T14:01:39Z
- **Completed:** 2026-07-17T14:14:00Z
- **Tasks:** 2
- **Files modified:** 3 code + SUMMARY/plan docs

## Accomplishments

- Closed **CR-01** (🛑 Blocker): `CurriculumController.step()` RECOVER branch now captures `rollback()` return and calls `RunController.load_state_dict(restored["run_controller"])` inside the existing `EmptyCheckpointStore` try, guarded by live run controller + payload key presence.
- Closed **CR-02** (🛑 Blocker): `RunController.run_stage` replaces `remaining_budget == 0 → HALT` shortcut with a single `StageExitMachine.evaluate` poll (ADVANCE when gate holds; HALT/None → HALT).
- Closed **WR-05**: deleted source-text grep test; added parameter-level behavioral RECOVER-restore tests that failed on pre-fix code.
- Full regression green: phase40 **146**, phase37 **55**, phase38 **128**, phase39 **264**.

## Task Commits

Each task was committed atomically under TDD (RED then GREEN):

1. **Task 1 RED: CR-01 behavioral tests** - `39112594` (test)
2. **Task 1 GREEN: RECOVER restore** - `47992574` (fix)
3. **Task 2 RED: zero-headroom boundary tests** - `2fa0d779` (test)
4. **Task 2 GREEN: boundary stage-exit poll** - `89711545` (fix)

**Plan metadata:** (this SUMMARY commit)

## Observed RED output (pre-fix failure proof)

### CR-01 (Task 1 RED)

```
FAIL: test_recover_with_retries_restores_model_params_from_checkpoint
  AssertionError: False is not true : RECOVER must restore model parameters
    from the rolled-back checkpoint (CR-01)
FAIL: test_recover_at_retries_zero_restores_then_halts_with_no_retrain
  AssertionError: False is not true : recover_retries=0 still restores,
    then HALTs with no retrain
OK: test_live_run_controller_recover_against_empty_store_does_not_crash
Ran 3 tests in 1.072s — FAILED (failures=2)
```

### CR-02 (Task 2 RED)

```
FAIL: test_zero_lbfgs_headroom_boundary_advances_when_gate_satisfied
  AssertionError: <StageDisposition.HALT: 'HALT'> !=
    <StageDisposition.ADVANCE: 'ADVANCE'>
OK: test_zero_lbfgs_headroom_boundary_halts_when_gate_unmet
Ran 2 tests in 2.393s — FAILED (failures=1)
```

## Files Created/Modified

- `pinn/training/controllers.py` — RECOVER restore + zero-headroom gate poll
- `tests/phase40/test_controllers.py` — RecoverRestoreBehavioralTests; deleted WR-05 grep
- `tests/phase40/test_optimizer_phase.py` — boundary ADVANCE + HALT-mirror tests

## Decisions Made

- Implemented only the adjudicated fixes (GAP-40-01 → B, GAP-40-02 → A). Did **not** take verification's alternative of tightening `StageConfig` to strict `n_adam < max_epochs`.
- Did **not** implement `stage_factory` / CR-03 / scheduled_weights docstring work (40-09 scope).
- Boundary path does not call `rewarm()` (schedule never frozen there).

## Deviations from Plan

None - plan executed exactly as written.

## Scope explicitly not done (per plan)

- CR-03 / SC1 / TRAIN-01 per-stage reconfiguration → `40-09-PLAN.md`
- No edits to `pinn/training/config.py` or `pinn/training/scheduled_weights.py` (`git diff --stat` empty for both)

## Verification counts (post-fix)

| Suite | Count | Result |
|-------|-------|--------|
| tests/phase40 | 146 | OK |
| tests/phase37 | 55 | OK |
| tests/phase38 | 128 | OK |
| tests/phase39 | 264 | OK |

Phase-40 arithmetic: 142 baseline − 1 deleted WR-05 grep + 3 RECOVER behavioral + 2 boundary = **146**.

## Known Stubs

None introduced.

## Threat Flags

None new. T-40-02 remains mitigated by existing `weights_only=True` load; T-40-09 single-mechanism guard unchanged; T-40-10 boundary poll uses the same four-criterion machine (mirror test asserts no fallback ADVANCE).

## Self-Check: PASSED

- [x] `pinn/training/controllers.py` exists and contains restore + boundary poll
- [x] Commits `39112594`, `47992574`, `2fa0d779`, `89711545` present on `milestone/v2.0`
- [x] No `stage_factory` in controllers.py
- [x] SUMMARY written at plan path
