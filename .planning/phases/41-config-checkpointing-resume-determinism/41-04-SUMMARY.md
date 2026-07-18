---
phase: 41-config-checkpointing-resume-determinism
plan: 04
subsystem: training-control
tags: [ctrl-02, ctrl-03, ctrl-04, ctrl-06, ctrl-07, ctrl-08, controllers, mid-stage-checkpoint, guard-hook, adam-reset]

requires:
  - phase: 41-config-checkpointing-resume-determinism
    provides: CheckpointStore save_rolling/save_best/save_anchor/promote/record_disposition + CHECKPOINT_SCHEMA_VERSION (41-02); StepGuards + write_failure_bundle + capture/restore_rng_state (41-03)
provides:
  - RunController live optimizer + four-stream rng + global step in state_dict (CTRL-08)
  - build_checkpoint_payload single CTX-53 composer (HIGH 1)
  - pending-optimizer build-then-load + resume_ctx epoch re-entry (MEDIUM-5)
  - Optional checkpoint_hook / guard_hook mid-stage call sites (CTRL-02/03/07)
  - CurriculumController promote + curriculum.jsonl disposition ledger (CTRL-04)
  - stage-init anchor with reset Adam (CTRL-06 composition)
affects:
  - 41-05 pinn.train composition root (constructs hook closures, drives end-to-end)

tech-stack:
  added: []
  patterns:
    - "single build_checkpoint_payload composer; every production save routes through it"
    - "checkpoint_hook/guard_hook are closures (not controller methods) capturing live curriculum_state_accessor + config_identity"
    - "phase-specific guard placement: Adam before optimizer.step; L-BFGS after step at non_finite check"
    - "per-family GuardOutcome.disposition propagated verbatim (RECOVER vs HALT never flattened)"
    - "optimizer deferred into _pending_optimizer_state until fresh Adam is built"
    - "dual save path: Phase-40 nested save() for regression spies + CTX-53 save_anchor for production"

key-files:
  created:
    - tests/phase41/test_controllers_ext.py
  modified:
    - pinn/training/controllers.py

key-decisions:
  - "Keep Phase-40 nested {tag,stage,run_controller} save() payloads so phase40 spies stay green; also write CTX-53 save_anchor via build_checkpoint_payload"
  - "Beyond-terminal PromotionRefused is soft (TRAIN-07 preflight owns stage>=3); skip/regress still hard-raises"
  - "load_state_dict accepts both clipper (Phase-40) and grad_clip (CTX-53) keys"
  - "Validation runs before checkpoint_hook so _last_val_total is live for best.pt producer"

patterns-established:
  - "RunController hooks default None → byte-for-byte Phase-40 when uninjected"
  - "CurriculumController disposition calls unconditional (store no-op defaults — HIGH 5)"
  - "CTRL-06: entered controller._optimizer = None before stage-{k+1}-init serialize"

requirements-completed: [CTRL-02, CTRL-04, CTRL-06, CTRL-08]

coverage:
  - id: D1
    description: RunController state_dict exposes optimizer + four-stream rng + counters; build_checkpoint_payload assembles full CTX-53 envelope; pending-optimizer build-then-load restores mid-stage moments
    requirement: CTRL-08
    verification:
      - kind: unit
        ref: tests/phase41/test_controllers_ext.py#StateDictExposureTests|CheckpointPayloadComposerTests|RngRestoreExactTests|OptimizerRestoreOrderingTests|BackwardCompatTests
        status: pass
    human_judgment: false
  - id: D2
    description: Per-step checkpoint_hook + guard_hook fire mid-stage with phase-specific placement; best.pt on strict val improvement; family disposition RECOVER/HALT
    requirement: CTRL-02
    verification:
      - kind: unit
        ref: tests/phase41/test_controllers_ext.py#CheckpointHookTests|BestProducerTests|AdamGuardHookTests|LbfgsGuardHookTests|GuardHaltFamilyTests
        status: pass
    human_judgment: false
  - id: D3
    description: CurriculumController curriculum.jsonl ledger + ordered promote + stage-init Adam reset composition
    requirement: CTRL-04
    verification:
      - kind: unit
        ref: tests/phase41/test_controllers_ext.py#LedgerAndPromotionTests|AdamResetCompositionTests
        status: pass
    human_judgment: false
  - id: D4
    description: CTRL-06 Adam reset across boundary — stage-init anchor optimizer key is None; restore yields reset Adam
    requirement: CTRL-06
    verification:
      - kind: unit
        ref: tests/phase41/test_controllers_ext.py#AdamResetCompositionTests
        status: pass
    human_judgment: false

duration: 25min
completed: 2026-07-18
status: complete
---

# Phase 41 Plan 04: Controllers Mid-Stage Checkpoint + Guard Hooks Summary

**RunController/CurriculumController additive mid-stage checkpoint + guard wiring — live Adam/RNG/global-step state, single CTX-53 composer, phase-specific guard placement, disposition ledger, and CTRL-06 Adam-reset init anchors — composition seam ready for 41-05 pinn.train**

## Performance

- **Duration:** ~25 min
- **Started:** 2026-07-18T08:23:55Z
- **Completed:** 2026-07-18T08:55:00Z
- **Tasks:** 3/3
- **Files modified:** 2

## Accomplishments

- Extended `RunController` with live optimizer exposure, four-stream RNG capture/restore, global cross-stage step counter, deferred optimizer restore (`_pending_optimizer_state`), `resume_ctx` epoch re-entry, and `_last_val_total` for best.pt
- Added module-level `build_checkpoint_payload` as the single CTX-53 envelope composer (`CHECKPOINT_SCHEMA_VERSION` imported from `checkpoint.py`, never redefined)
- Wired optional `checkpoint_hook` / `guard_hook` closures with phase-specific placement (Adam before `optimizer.step`; L-BFGS after `optimizer.step(closure)` at the non_finite check) and per-family disposition propagation
- Extended `CurriculumController` with unconditional `promote` + `record_disposition` ledger rows and CTRL-06 Adam-reset composition on stage-init anchors

## Task Commits

Each task was committed atomically (implementation landed as one intertwined commit across all three tasks because they share `controllers.py`):

1. **Tasks 1–3: state exposure + hooks + curriculum ledger** - `92dabc98` (feat)

**Plan metadata:** (pending docs commit)

_Note: TDD tasks share production file; RED/GREEN were executed in-session with final green suite before the single feat commit._

## Files Created/Modified

- `pinn/training/controllers.py` — RunController + CurriculumController Phase-41 extensions + `build_checkpoint_payload`
- `tests/phase41/test_controllers_ext.py` — 22 unit tests covering CTRL-02/03/04/06/07/08 controller surface

## Decisions Made

- Dual save path preserves Phase-40 nested `save({tag, stage, run_controller})` for regression spies while production CTX-53 anchors go through `save_anchor(build_checkpoint_payload(...))`
- Beyond-terminal `PromotionRefused` is soft so TRAIN-07 preflight remains the stage≥3 hard stop; skip/regress still raise
- `load_state_dict` accepts both `clipper` and `grad_clip` keys for Phase-40 vs CTX-53 payloads
- Validation precedes the checkpoint hook so `_last_val_total` is current for the best.pt producer

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing critical functionality] Beyond-terminal promote soft-fail**
- **Found during:** Task 3 / phase40 PreflightGateTests
- **Issue:** Unconditional `promote(2, 3)` raised `PromotionRefused` before TRAIN-07 preflight could refuse stage 3
- **Fix:** Catch beyond-terminal `PromotionRefused` and continue; skip/regress still hard-raise
- **Files modified:** `pinn/training/controllers.py`
- **Commit:** `92dabc98`

**2. [Rule 1 - Bug] load_state_dict KeyError on CTX-53 `grad_clip`**
- **Found during:** Task 3 AdamResetCompositionTests
- **Issue:** Flat CTX-53 payloads use `grad_clip`; Phase-40 nested uses `clipper`
- **Fix:** Accept either key on load
- **Files modified:** `pinn/training/controllers.py`
- **Commit:** `92dabc98`

**3. [Rule 2 - Missing critical functionality] Validation before checkpoint_hook**
- **Found during:** Task 2 BestProducerTests design
- **Issue:** Hook fired before `_last_val_total` was updated
- **Fix:** Reorder Adam/L-BFGS epoch body so validation updates `_last_val_total` before the checkpoint hook
- **Files modified:** `pinn/training/controllers.py`
- **Commit:** `92dabc98`

## Known Stubs

None — no placeholder empty data paths; hooks default to None intentionally (Phase-40 compat), and production closures are constructed by 41-05.

## Threat Flags

None beyond the plan's `<threat_model>` mitigations (T-41-14..17C), all of which are covered by unit tests in `test_controllers_ext.py`.

## TDD Gate Compliance

- Plan `type: execute` with per-task `tdd="true"`. RED tests and GREEN implementation were developed in-session; final landing is a single feat commit (`92dabc98`) because all three tasks modify the same production file and test module. No separate `test(...)` RED commit was retained.

## Self-Check: PASSED

- `FOUND: pinn/training/controllers.py`
- `FOUND: tests/phase41/test_controllers_ext.py`
- `FOUND: 92dabc98` (feat commit)
- Phase-41 full suite: 141/141 OK
- Phase-40 `test_controllers` + `test_optimizer_phase`: green
- Phase-40 full suite: 162/163 green; pre-existing fail in `test_prohibitions` against `determinism.py` (41-03, out of scope for this plan)
