---
phase: 40-stage-0-curriculum-training-loop-fut-04
plan: 06
subsystem: training
tags: [train-01, curriculum-controller, stage-exit-dispatch, checkpoint-seam, curriculum-loop, pinn-training-loop]

# Dependency graph
requires:
  - phase: 40-stage-0-curriculum-training-loop-fut-04 (plans 01-05)
    provides: dataset-free test contract + pinn/training package skeleton (40-01); ScheduledWeights + GradClipper (40-02); CollocationSampler + sL-BFGS preflight refusal (40-03); StageExitMachine + TrainingConfig + CheckpointStore (40-04); RunController.run_stage(k) inner Adam->L-BFGS loop (40-05)
provides:
  - "pinn.training.controllers.CurriculumController -- the outer curriculum loop (TRAIN-01): dispatches on RunController.run_stage(k)'s StageDisposition into stage progression, with a forced-disposition injection seam and a run-start provisional-threshold log + stage-0-init checkpoint anchor"
  - "pinn.training.controllers.ForcedDispositionOnLiveRun -- typed T-40-09 construction-time guard (the ONE mechanism) refusing a forced disposition supplied alongside a live RunController"
  - "pinn.training (package barrel) -- full CTX-33 one-namespace re-export of TrainingConfig, CurriculumController, RunController, CheckpointStore"
affects: ["41 (config/checkpoint/guards -- CheckpointStore atomic/retention/promotion impl slots behind CurriculumController's checkpoint_store seam; TrainingConfig YAML mapping)", "42 (logging -- CTX-45 logger tree 'pinn.training.controllers' gets a JSONL handler)", "43 (ACC-05 Stage-0 pilot calibrates eps_plateau/eps_phys/eps_energy/MAX_EPOCHS against real data; the composed gate-earned ADVANCE test's permissive thresholds are explicitly NOT that calibration)"]

# Tech tracking
tech-stack:
  added: []  # stdlib logging only; no new deps
  patterns:
    - "injection-seam XOR pattern -- forced_disposition and run_controller are mutually exclusive constructor args guarded by a SINGLE typed-exception raise at construction (no parallel assert anywhere in the class), reusable for future single-mechanism-guard seams (T-40-09 precedent)"
    - "step() / run() split -- step() is the single-stage-iteration primitive tests call directly for isolated forced-disposition assertions (avoiding an infinite forced-ADVANCE loop); run() loops step() until a terminal HALT and owns the once-per-run anchor save + provisional-threshold log"

key-files:
  created:
    - tests/phase40/test_controllers.py
  modified:
    - pinn/training/controllers.py
    - pinn/training/__init__.py

key-decisions:
  - "CurriculumController requires exactly one of run_controller / forced_disposition at construction (raises ValueError if neither is supplied), in addition to the plan-mandated ForcedDispositionOnLiveRun raise when BOTH are supplied -- a controller built with neither could never produce a StageDisposition, an unusable object (Rule 2 defensive addition, not a plan-mandated AC)."
  - "step() is the single-stage-iteration primitive; run() loops step() until a terminal HALT. Isolated forced-disposition ACs (forced ADVANCE/HALT/RECOVER, the composed real-ADVANCE test) call step() directly; the run-start anchor/logging tests and the cold-start/preflight-gate tests call run() (which owns the once-per-run anchor save + provisional log before entering the loop)."
  - "CheckpointStore.save(state) generates its own checkpoint id and accepts no id parameter (per the 40-04 Protocol), so the stage-{k}-final / stage-{k+1}-init / stage-0-init tagging is carried INSIDE the saved payload dict's 'tag' key, not as a save() argument."
  - "The composed gate-earned ADVANCE test's permissive thresholds (eps_plateau/eps_phys/eps_energy) are 1e15, not the initially-tried 1e6 -- empirical probing showed an untrained SIREN (omega_0=30) network's real Stage-0 physics residual sits in the 1e9-1e10 range on random initialization (a mechanism-noise floor to clear, not a convergence signal); the test docstring records this and states the thresholds assert nothing about real-data convergence (Phase 43 / ACC-05)."
  - "CurriculumController logs stage-exit dispositions (ADVANCE/RECOVER/HALT) and, when a live RunController is present, its last_handoff_event -- both CTX-45-required event categories beyond the run-start provisional log the plan's ACs specifically test."

patterns-established:
  - "Injection-seam XOR guard: mutually exclusive constructor parameters enforced by ONE typed raise (ForcedDispositionOnLiveRun), with a structural test (`test_exactly_one_guard_mechanism_no_alternative_assert_unset`) asserting no parallel assert-based guard exists anywhere in the class -- a reusable pattern + test template for T-40-09-style single-mechanism contracts."

requirements-completed: [TRAIN-01, TRAIN-06]

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "CurriculumController outer curriculum loop (TRAIN-01): dispatches on StageDisposition -- ADVANCE checkpoints stage-{k}-final + stage-{k+1}-init, increments k, rewarms the schedule; HALT stops for owner review; no fallback advancement. The forced-disposition injection seam is a first-class constructor parameter, defaulting to None."
    requirement: "TRAIN-01"
    verification:
      - kind: unit
        ref: "tests/phase40/test_controllers.py#ForcedDispositionDispatchTests (3 tests: forced ADVANCE/HALT/RECOVER dispatch)"
        status: pass
      - kind: unit
        ref: "tests/phase40/test_controllers.py#PreflightGateTests (stage>=3 refused before run_stage)"
        status: pass
    human_judgment: false
  - id: D2
    description: "T-40-09 guard: ForcedDispositionOnLiveRun raised AT CONSTRUCTION when both a live run_controller and forced_disposition are supplied together; the injection parameter defaults to None/absent; exactly ONE guard mechanism exists (no alternative assert-unset path)."
    requirement: "TRAIN-01"
    verification:
      - kind: unit
        ref: "tests/phase40/test_controllers.py#CurriculumControllerConstructionTests (4 tests)"
        status: pass
    human_judgment: false
  - id: D3
    description: "Cold-start RECOVER backstop (cycle-2 H3 / T-40-10): a run-start stage-0-init checkpoint anchor is saved before the first stage is entered; RECOVER against a genuinely empty CheckpointStore is caught (except EmptyCheckpointStore), records the disposition, and run() returns normally with Δstage=0 and terminal state HALT."
    requirement: "TRAIN-01"
    verification:
      - kind: unit
        ref: "tests/phase40/test_controllers.py#ColdStartRecoverTests (2 tests, against a REAL TorchSaveCheckpointStore over an empty tmp dir)"
        status: pass
    human_judgment: false
  - id: D4
    description: "CTX-38/45 run-start logging: the full provisional-threshold set (name/value/provenance from TrainingConfig.provisional_fields()) is logged once via logging.getLogger('pinn.training.controllers') before the first stage; the run-start stage-0-init anchor is the FIRST CheckpointStore.save() call of a run (save-order spy)."
    requirement: "TRAIN-06"
    verification:
      - kind: unit
        ref: "tests/phase40/test_controllers.py#RunStartLoggingAndAnchorTests (2 tests: assertLogs provenance content + save-order spy)"
        status: pass
    human_judgment: false
  - id: D5
    description: "Composed gate-earned ADVANCE (cycle-2 M4): with TEST-LOCAL permissive thresholds and NO forced disposition, one real RunController.run_stage call (via CurriculumController.step()) produces ADVANCE through the real StageExitMachine and increments the outer-loop stage by exactly 1 -- the production-of-ADVANCE path, not only the dispatch-of-ADVANCE path. Test docstring records the thresholds are mechanism values, not calibrated pass levels; real-data convergence remains Phase 43 (ACC-05)."
    requirement: "TRAIN-01"
    verification:
      - kind: unit
        ref: "tests/phase40/test_controllers.py#ComposedGateEarnedAdvanceTests.test_real_run_stage_produces_advance_with_permissive_test_local_thresholds"
        status: pass
    human_judgment: false
  - id: D6
    description: "Package barrel (CTX-33): pinn/training/__init__.py re-exports TrainingConfig, CurriculumController, RunController, CheckpointStore from one namespace, preserving the 'importing binds names, performs NO discovery/init' docstring discipline; no model build / no dataset discovery at import time. The full dataset-free tests/phase40 suite is green with no remaining SKIPs for landed symbols."
    requirement: "TRAIN-06"
    verification:
      - kind: other
        ref: "python -c \"import pinn.training as t; assert all(hasattr(t,n) for n in ('TrainingConfig','CurriculumController','RunController','CheckpointStore'))\" -> barrel OK"
        status: pass
      - kind: unit
        ref: "unittest discover -s tests/phase40 -p 'test_*.py' (142/142 pass, 0 skips)"
        status: pass
    human_judgment: false

# Metrics
duration: ~20min
completed: 2026-07-17
status: complete
---

# Phase 40 Plan 06: CurriculumController Outer Curriculum Loop Summary

**CurriculumController closes TRAIN-01 -- ADVANCE/RECOVER/HALT stage-progression dispatch over RunController.run_stage(k), a T-40-09-guarded forced-disposition injection seam, a cold-start RECOVER backstop against an empty CheckpointStore, CTX-38/45 run-start provisional-threshold logging, and the full pinn/training package barrel -- closing Phase 40 at 142/142 dataset-free tests.**

## Performance

- **Duration:** ~20 min (resumed once after a transient API interruption; no work was lost -- the interrupted append had not yet landed on disk)
- **Completed:** 2026-07-17T11:08:24Z
- **Tasks:** 2 (Task 1: CurriculumController + tests; Task 2: package barrel + phase-gate suite run)
- **Files modified:** 3 (1 created, 2 modified)

## Accomplishments

- **CurriculumController (TRAIN-01):** the outer curriculum loop. `step()` runs `check_stage_preflight(k)` (TRAIN-07 wiring) before obtaining a `StageDisposition` from either a live `RunController.run_stage(k)` or the forced-disposition injection seam, then dispatches exactly: ADVANCE saves the `stage-{k}-final` + `stage-{k+1}-init` checkpoint anchors, increments `k`, and calls `ScheduledWeights.rewarm()`; RECOVER calls `CheckpointStore.rollback()` (catching `EmptyCheckpointStore` as the H3 backstop) and, at the default `recover_retries=0`, transitions straight to HALT with no retrain attempt; HALT stops for owner review. There is no fallback advancement -- only ADVANCE ever changes the stage. `run()` wraps `step()` in a loop, saving the run-start `stage-0-init` anchor and logging the full CTX-38 provisional-threshold set exactly once before the first stage.
- **T-40-09 guard (`ForcedDispositionOnLiveRun`):** the forced-disposition injection parameter defaults to `None`; supplying it alongside a live `run_controller` raises the typed error AT CONSTRUCTION. This is the ONLY guard mechanism -- a structural test (`test_exactly_one_guard_mechanism_no_alternative_assert_unset`) proves no parallel "assert unset" code path exists anywhere in the class.
- **Cold-start RECOVER backstop (cycle-2 H3 / T-40-10):** verified against a REAL `TorchSaveCheckpointStore` over a genuinely empty tmp directory (not a spy) with the run-start anchor suppressed -- `run()` returns normally, no exception propagates, `Δstage == 0`, and the terminal state is HALT.
- **Composed gate-earned ADVANCE (cycle-2 M4):** a dedicated test drives ONE real `RunController.run_stage` call (via `CurriculumController.step()`, no forced disposition) with test-local permissive thresholds, and asserts the real `StageExitMachine` produces ADVANCE and the outer-loop stage increments by exactly 1 -- proving the production-of-ADVANCE path, not only the dispatch-of-ADVANCE path already covered by the forced-injection tests.
- **CTX-38/45 logging:** `logging.getLogger('pinn.training.controllers')` emits a run-start record enumerating every provisional-threshold field (name, value, provenance) once per run (`assertLogs`-verified), plus stage-exit-disposition and Adam→L-BFGS handoff-event records when a live `RunController` is present.
- **Package barrel (Task 2, CTX-33):** `pinn/training/__init__.py` now re-exports `TrainingConfig`, `CurriculumController`, `RunController`, and `CheckpointStore` from one namespace for Phase 41/42 to import against, preserving the "importing binds names, performs NO discovery/init" docstring discipline.
- **Phase gate:** the full dataset-free `tests/phase40` suite is 142/142 green (129 prior + 13 new), 0 skips, 0 failures -- Phase 40 is complete.

## Task Commits

Each task was committed atomically:

1. **Task 1: CurriculumController outer loop + dispatch + preflight + run-start log (TRAIN-01)** - `eaed7714` (feat)
2. **Task 2: Package barrel + full phase-40 suite gate** - `db8a855a` (feat)

**Plan metadata:** committed separately below (this SUMMARY + STATE/ROADMAP).

## Files Created/Modified

- `pinn/training/controllers.py` - adds `CurriculumController` (outer stage-progression loop) and `ForcedDispositionOnLiveRun` (typed T-40-09 guard) to the file that already held `RunController`/`PlateauDetector` (40-05).
- `pinn/training/__init__.py` - full barrel re-exporting `TrainingConfig`, `CurriculumController`, `RunController`, `CheckpointStore`.
- `tests/phase40/test_controllers.py` - 13 tests: construction/T-40-09 guard (4), forced-disposition dispatch (3), cold-start RECOVER (2), preflight gate (1), run-start logging/anchor ordering (2), composed gate-earned ADVANCE (1).

## Decisions Made

See frontmatter `key-decisions` for the full list. Headline decisions: (1) a defensive both-None construction guard beyond the plan-mandated both-supplied guard; (2) the `step()`/`run()` split so isolated forced-disposition tests avoid an infinite forced-ADVANCE loop; (3) checkpoint tagging lives inside the saved payload dict (`"tag"` key) since `CheckpointStore.save(state)` generates its own id; (4) the composed gate-earned test's permissive thresholds were widened to 1e15 after empirically observing an untrained SIREN network's Stage-0 physics-residual mechanism-noise floor sits in the 1e9-1e10 range; (5) stage-exit-disposition and handoff-event logging were added alongside the plan's explicitly-tested run-start log, completing CTX-45's stated event list.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Added a construction-time guard requiring exactly one of `run_controller` / `forced_disposition`**
- **Found during:** Task 1 (implementing the `CurriculumController` constructor)
- **Issue:** The plan mandates the T-40-09 guard for the case where BOTH `run_controller` and `forced_disposition` are supplied together, but is silent on the case where NEITHER is supplied. A controller constructed with neither could never obtain a `StageDisposition` -- an object that cannot function, discovered only at first `step()`/`run()` call rather than at construction.
- **Fix:** The constructor also raises `ValueError` when both are `None`, alongside the plan-mandated `ForcedDispositionOnLiveRun` raise when both are non-`None`. This is purely additive; it does not change or weaken the T-40-09 guard (which remains the ONE typed-exception mechanism for the both-supplied case).
- **Files modified:** `pinn/training/controllers.py`
- **Verification:** `test_forced_disposition_only_construction_does_not_raise` proves both sanctioned single-argument construction paths still work cleanly; the fail-closed both-None path is a straightforward defensive guard mirroring the `ArchitectureSpec`/`TrainingConfig` construction-time-validation idiom already established in this phase, not a plan-mandated AC.
- **Commit:** `eaed7714`

---

**Total deviations:** 1 auto-fixed (1 missing-critical). **Impact:** purely additive defensive validation at construction time; does not alter, weaken, or duplicate the plan-mandated T-40-09 `ForcedDispositionOnLiveRun` guard. No scope creep.

## Issues Encountered

- **Cross-plan REQUIREMENTS.md staleness (out of this plan's scope, flagged for the verifier):** running `requirements.mark-complete` for this plan's own frontmatter list (`[TRAIN-01, TRAIN-06]`) surfaced that `.planning/REQUIREMENTS.md` still shows TRAIN-03, TRAIN-04, TRAIN-05, and TRAIN-07 as `Pending` even though 40-02/40-03/40-04's own SUMMARY frontmatter (`requirements-completed`) already claims TRAIN-03/TRAIN-05 (40-02) and TRAIN-04/TRAIN-07 wiring (40-03) as delivered, and all four are covered by passing tests in the current 142/142 suite. This plan did not call `mark-complete` for those IDs (they are not in 40-06's own `requirements:` frontmatter) to stay within scope; flagging here so Phase 40 verification (`/gsd-verify-work 40`) reconciles the ledger against the actual test coverage rather than trusting the `Pending` label.
- **Composed gate-earned ADVANCE test initially failed with `eps_phys`/`eps_energy` at 1e6.** Root cause: an untrained SIREN network (`omega_0=30`) produces a physics-residual magnitude in the 1e9-1e10 range on random initialization (confirmed by tracing `StageExitMachine.evaluate`'s inputs directly). Resolved by widening the test-local thresholds to 1e15, which is still explicitly documented in the test docstring as a mechanism value clearing an untrained-network noise floor, not a calibrated pass level or a config-default change. No production code was touched to resolve this -- it is purely a test-fixture-tuning issue in a new test this plan wrote.
- **Mid-execution interruption:** a transient API server error interrupted the session after the `controllers.py` import/`__all__` edit had applied but before the `CurriculumController`/`ForcedDispositionOnLiveRun` class bodies were appended. On resume, the on-disk state was re-verified (`git diff`, `tail -n 20`) before continuing -- no work was lost or duplicated.

## User Setup Required

None - dataset-free, no external service configuration.

## Next Phase Readiness

- **Phase 40 is complete.** All 7 requirements (TRAIN-01..07) are implemented across 6 plans; the full dataset-free `tests/phase40` suite is 142/142 green.
- **Ready for Phase 41 (CTRL):** `CurriculumController`'s `checkpoint_store` seam is the exact `CheckpointStore` Protocol Phase 41 swaps behind an atomic/retention/promotion implementation without touching controller code; `TrainingConfig` is the exact nested-dataclass shape Phase 41 maps YAML sections onto field-for-field; the `recover_retries` constructor parameter (currently a simple counter, default 0) is the seam Phase 41/43 calibrates via the D4-c/R-2 owner-carved decision.
- **Ready for Phase 42 (OPS):** the `logging.getLogger('pinn.training.controllers')` tree already emits the CTX-45-mandated run-start provisional-threshold, stage-exit-disposition, and Adam→L-BFGS handoff-event records; Phase 42 attaches a JSONL/TensorBoard handler to the same logger tree.
- **Provisional values surfaced for ACC-05 (Phase 43 pilot) calibration:** unchanged from prior plans (`C_stage`, `median_floor`, `lbfgs_max_iter`, `lbfgs_chunk_size`, the anchor-identity `eps_h` scale, and all CTX-38 stage-exit thresholds `eps_plateau`/`eps_phys`/`eps_energy`/`beta`/`patience`). This plan adds no new provisional science constant -- it is pure control-flow/dispatch logic over the values already surfaced.
- **No blockers.**

---
*Phase: 40-stage-0-curriculum-training-loop-fut-04 (plan 06)*
*Completed: 2026-07-17*

## Self-Check: PASSED

- FOUND: `pinn/training/controllers.py`
- FOUND: `pinn/training/__init__.py`
- FOUND: `tests/phase40/test_controllers.py` (13 test functions)
- FOUND: `.planning/phases/40-stage-0-curriculum-training-loop-fut-04/40-06-SUMMARY.md`
- FOUND commit `eaed7714` (feat(40-06): add CurriculumController outer curriculum loop)
- FOUND commit `db8a855a` (feat(40-06): export CurriculumController/RunController/TrainingConfig barrel)
- Re-ran `tests.phase40.test_controllers` + `tests.phase40.test_prohibitions`: 29/29 pass
- Re-ran `unittest discover -s tests/phase40 -p 'test_*.py'`: 142/142 pass, 0 skips, 0 errors
