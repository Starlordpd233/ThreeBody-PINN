---
phase: 41-config-checkpointing-resume-determinism
plan: 05
subsystem: training-control
tags: [ctrl-01, ctrl-05, ctrl-08, resume, train-entrypoint, identity-digest, hold-stage, strict-cpu]

requires:
  - phase: 41-config-checkpointing-resume-determinism
    provides: TrainingConfig + config_yaml freeze (41-01); CheckpointStore save_rolling/save_best/save_anchor/load_checkpoint (41-02); StepGuards + determinism RNG/strict-CPU/honesty (41-03); RunController hooks + build_checkpoint_payload + resume_ctx epoch re-entry (41-04)
provides:
  - Multi-module identity payload + field-classified fail-safe resume_config_diff (CTRL-05)
  - load_resume_target exact-anchor FILE routing vs DIR/latest (CTRL-05)
  - validate_hold_stage_target non-final guard (SPEC Edge R5)
  - identity_coverage_check REPRESENTED vs DEFERRED-NOT-REPRESENTABLE (cycle-4 MEDIUM-3)
  - python -m pinn.train composition root with --config/--resume/--hold-stage (CTRL-01/05/08)
  - strict-CPU RuntimeSpec override into build_network (HIGH 4)
  - fail-closed run-folder collision + path-traversal hardening
  - checkpoint_hook/guard_hook closures capturing live curriculum_state + config_identity
affects:
  - Phase 42 logging/operator ergonomics (consumes frozen config + curriculum.jsonl + honesty string)
  - Stage-0 pilot / ACC runs via python -m pinn.train

tech-stack:
  added: []
  patterns:
    - "named field-level identity payload (not digest-only refuse)"
    - "unclassified→refuse fail-safe; operational whitelist only proceeds"
    - "RESUME_FIELD_REGISTRY is ⚖ provisional; rule is locked"
    - "strict_cpu_determinism → apply_strict_cpu_determinism RuntimeSpec handed to build_network"
    - "load_resume_target FILE→load_checkpoint; DIR/latest→load_latest"
    - "CurriculumController.run(resume_ctx=, from_resume=) one-shot mid-stage re-entry"

key-files:
  created:
    - pinn/training/resume.py
    - pinn/train.py
    - tests/phase41/test_resume.py
    - tests/phase41/test_train_entrypoint.py
  modified:
    - pinn/training/config.py
    - pinn/training/controllers.py

key-decisions:
  - "Seed fan-out: ArchitectureSpec(seed=config.run.seed) so one YAML seed drives weight init + data sampling"
  - "B-5 RESUME_FIELD_REGISTRY shipped as ⚖ provisional; unclassified→refuse locked"
  - "DEFERRED IDENTITY categories (dataset/split/loss-catalog) honest-absent in dataset-free floor; has_dataset=True refuses"
  - "Synthetic train/val sources default to n=240 to satisfy build_stage_batch Stage-0 floor"
  - "CurriculumController.run gains from_resume + one-shot resume_ctx (Rule 2 wiring gap from 41-04)"

patterns-established:
  - "config_identity envelope = {digest, identity_fields, resolved_config_snapshot, effective_runtime}"
  - "pinn.train owns hook closures; RunController does not own curriculum_state/config_identity"
  - "reproducibility_scope() honesty string emitted at run start (never bitwise)"

requirements-completed: [CTRL-05, CTRL-01, CTRL-08]

coverage:
  - id: D1
    description: Multi-module identity payload + field-level named resume refuse (identity/unclassified) with operational-only proceed; strict_cpu + effective_runtime explicit IDENTITY
    requirement: CTRL-05
    verification:
      - kind: unit
        ref: tests/phase41/test_resume.py#IdentityPayloadTests|NamedDiffFailSafeTests|StrictCpuIdentityClassificationTests|DefenseInDepthTests|ClassificationRegistryTests
        status: pass
    human_judgment: false
  - id: D2
    description: Exact-anchor load routing, hold-stage non-final guard, identity coverage check
    requirement: CTRL-05
    verification:
      - kind: unit
        ref: tests/phase41/test_resume.py#ResumeExactAnchorLoadingTests|HoldStageTargetTests|IdentityCoverageTests
        status: pass
    human_judgment: false
  - id: D3
    description: python -m pinn.train launches, freezes config, dual-trigger checkpoints, strict-CPU override, collision/path-traversal, resume refuse, hold-stage exact anchor
    requirement: CTRL-01
    verification:
      - kind: unit
        ref: tests/phase41/test_train_entrypoint.py#LaunchContractTests|StrictCpuOverrideTests|RunFolderCollisionTests|ResumeRefuseTests|HoldStageTests
        status: pass
    human_judgment: false
  - id: D4
    description: Mid-stage resume, four-stream RNG in every checkpoint, dual-trigger e2e, repro honesty, structural validity + fallback_scan
    requirement: CTRL-08
    verification:
      - kind: unit
        ref: tests/phase41/test_train_entrypoint.py#ExactContinuationTests|RngRecordedEverywhereTests|DualTriggerEndToEndTests|MidStageRollingStructuralValidityTests|ReproHonestyTests
        status: pass
    human_judgment: false

duration: 10min
completed: 2026-07-18
status: complete
---

# Phase 41 Plan 05: Resume/Rollback + pinn.train Driver Summary

**Multi-module field-classified resume refuse + exact-anchor hold-stage routing + minimal runnable `python -m pinn.train` composition root delivering CTRL-01/05/08 end-to-end on the dataset-free Stage-0 floor**

## Performance

- **Duration:** ~10 min (wall clock)
- **Started:** 2026-07-18T08:34:58Z
- **Completed:** 2026-07-18T08:44:39Z
- **Tasks:** 3/3
- **Files modified:** 6

## Accomplishments

- Built `pinn/training/resume.py` with named multi-module identity payload, sha256 fast-path digest, field-classified fail-safe `resume_config_diff`, exact-anchor `load_resume_target`, `--hold-stage` non-final guard, and identity coverage check
- Built `pinn/train.py` composition root wiring config → freeze → strict-CPU/runtime → network (seed fan-out) → store + guards → hook closures → CurriculumController
- Extended CurriculumController for `run(resume_ctx=, from_resume=)` mid-stage epoch re-entry and registered ⚖ `resume_field_classification_registry` in provisional_fields
- Full `tests/phase41` suite green (192 tests) including exact-anchor hold-stage, dual-trigger e2e, and four-stream RNG recording

## Task Commits

Each task was committed atomically:

1. **Task 1: resume.py multi-module identity + fail-safe diff** - `91723553` (feat)
2. **Tasks 2–3: pinn.train composition root + e2e falsifiability** - `d4c7dbe3` (feat)

**Plan metadata:** (docs commit after this summary)

_Note: Tasks 2 and 3 share `pinn/train.py` / `test_train_entrypoint.py`; shipped as one feat commit after full green._

## Files Created/Modified

- `pinn/training/resume.py` — identity payload, digest, registry, resume_config_diff, load_resume_target, validate_hold_stage_target, identity_coverage_check, typed errors
- `pinn/train.py` — `python -m pinn.train` CLI composition root
- `tests/phase41/test_resume.py` — 30 unit tests for CTRL-05 resume surface
- `tests/phase41/test_train_entrypoint.py` — 21 unit/integration tests for CTRL-01/05/08 driver
- `pinn/training/config.py` — provisional_fields registers resume_field_classification_registry
- `pinn/training/controllers.py` — `_active_phase/_active_epoch`; `run(resume_ctx=, from_resume=)` one-shot re-entry

## Decisions Made

- Seed fan-out: single YAML `run.seed` seeds both `ArchitectureSpec` weight init and the RunController numpy Generator
- B-5 field lists are ⚖ provisional; unclassified→refuse is locked
- DEFERRED IDENTITY categories remain honest blind spots until a real data source lands; `has_dataset=True` refuses startup
- Synthetic sources use n=240 train+val to satisfy `build_stage_batch` Stage-0 floor without a corpus
- CurriculumController resume wiring (from_resume + resume_ctx) added as Rule 2 — required for CTRL-05 mid-stage re-entry that 41-04 exposed on `run_stage` but not on `run()`

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing critical functionality] CurriculumController.run resume surface**
- **Found during:** Task 2 resume_ctx threading
- **Issue:** `run_stage` accepted `resume_ctx` but `CurriculumController.run()` had no parameter and always wrote stage-0-init (would clobber resume)
- **Fix:** Added `run(*, resume_ctx=None, from_resume=False)` with one-shot pending ctx and skip of cold-start anchor on resume; track `_active_phase/_active_epoch` for curriculum_state_accessor
- **Files modified:** `pinn/training/controllers.py`
- **Commit:** `d4c7dbe3`

**2. [Rule 2 - Missing critical functionality] provisional_fields registry seam**
- **Found during:** Task 1 ClassificationRegistryTests
- **Issue:** Plan requires `resume_field_classification_registry` in `TrainingConfig.provisional_fields()`
- **Fix:** Append provisional entry (lazy-import from resume.py with fallback)
- **Files modified:** `pinn/training/config.py`
- **Commit:** `91723553`

**3. [Rule 3 - Blocking issue] Stage-0 population floor on synthetic sources**
- **Found during:** Task 2 LaunchContractTests
- **Issue:** Default n_train=8 / n_validation=32 raised `StageZeroUnderpopulated` (required 240)
- **Fix:** Default synthetic sources to 240/240 so the composition root is runnable dataset-free
- **Files modified:** `pinn/train.py`
- **Commit:** `d4c7dbe3`

## Known Stubs

- Dataset-free synthetic StageQuery sources inside `pinn/train.py` (intentional v2.0 floor; real data wiring is future)
- DEFERRED-NOT-REPRESENTABLE IDENTITY categories (dataset version/hash, split policy, loss-catalog structure, curriculum.stage_definitions beyond max_epochs) — honest blind spots until config sources exist
- ⚖ `frozen_config_rng_recording_format` remains UNDECIDED (41-01); checkpoints carry four RNG streams unconditionally

## Threat Flags

None beyond the plan's mitigated register (T-41-18..22A). No new bare `torch.load` sites; resume loads exclusively via store `weights_only=True` paths.

## Self-Check: PASSED

- FOUND: `pinn/training/resume.py`
- FOUND: `pinn/train.py`
- FOUND: `tests/phase41/test_resume.py`
- FOUND: `tests/phase41/test_train_entrypoint.py`
- FOUND: commit `91723553`
- FOUND: commit `d4c7dbe3`
- FOUND: 192/192 phase41 tests pass
