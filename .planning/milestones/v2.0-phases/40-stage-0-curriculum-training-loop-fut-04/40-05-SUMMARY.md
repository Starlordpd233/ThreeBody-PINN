---
phase: 40-stage-0-curriculum-training-loop-fut-04
plan: 05
subsystem: training
tags: [train-02, train-06, adam, lbfgs, plateau-detector, gradient-clipping, curriculum, pinn-training-loop]

# Dependency graph
requires:
  - phase: 40-stage-0-curriculum-training-loop-fut-04 (plans 01-04)
    provides: dataset-free test contract + pinn/training package skeleton (40-01); ScheduledWeights + GradClipper (40-02); CollocationSampler + sL-BFGS preflight refusal (40-03); StageExitMachine + TrainingConfig + CheckpointStore (40-04)
provides:
  - "pinn.training.controllers.PlateauDetector -- CTX-46 50-consecutive-epoch flat-slope Adam->L-BFGS handoff detector, distinct from stage_exit.py's TotalLossPlateauSmoother"
  - "pinn.training.controllers.RunController -- run_stage(k) -> StageDisposition, the full inner two-phase Adam->L-BFGS optimization loop composing every 40-01..40-04 seam plus the Phase-38 model and Phase-39 build_stage_batch"
  - "pinn.training.controllers.HandoffEvent -- distinguishes trigger='plateau' vs trigger='budget-exhausted' (CTX-45)"
  - "pinn.training.controllers.accumulate_chunked_data_term -- standalone, independently-testable chunked-accumulation L_data backward for the L-BFGS closure"
  - "pinn.training.grad_clip.GradClipper.state_dict/load_state_dict -- deferred from 40-02, closes the CTX-44 checkpoint-composition seam"
affects: ["40-06 (CurriculumController wraps run_stage(k) into the outer curriculum loop)", "41 (checkpoint/config/guards -- RunController.state_dict() is the per-stage payload CTRL-02..04 will persist)", "43 (ACC-05 Stage-0 pilot calibrates the provisional C_stage/eps_h/lbfgs_max_iter/lbfgs_chunk_size values this plan reads from config)"]

# Tech tracking
tech-stack:
  added: []  # torch.optim.Adam / CosineAnnealingLR / LBFGS already in torch; no new deps
  patterns:
    - "mockable core seam (_compose_loss_terms) -- the shared Adam/validation forward+compose step is a single, well-named method so control-flow tests can inject a controlled loss/phys sequence without needing real physics to organically behave a particular way, while build_stage_batch/anchor-context/clipping/scheduling still run for real"
    - "single representative-identity anchor for L_IC/L_E/L_L (see controllers.py module docstring) -- pinn.loss_catalog's ic_anchor_loss/soft_energy_loss/angular_momentum_loss are single-trajectory-scoped by signature (matching the only existing reference Adam loop, overfit_probe.py); L_data uses the full multi-identity FixedBatch, the other three anchor on one deterministic identity per fixed batch with h0/l0 from that identity's ground-truth snapshot-0"
    - "accumulate-in-closure via a standalone module function (accumulate_chunked_data_term) rather than inlined in the closure, so the len(chunk)/N_total-weighted-equals-full-batch-mean-backward property is independently unit-testable"
    - "no-grad-in-the-loose-sense validation pass -- model.eval()/model.train() bracket a try/finally instead of torch.no_grad(), because the physics/IC/energy/angmom terms need live second-order autograd (componentwise_du); the pass just never calls .backward()/optimizer.step(), matching the overfit_probe.py diagnostics precedent"

key-files:
  created:
    - pinn/training/controllers.py
    - tests/phase40/test_optimizer_phase.py
  modified:
    - pinn/training/grad_clip.py

key-decisions:
  - "PlateauDetector counts CONSECUTIVE QUALIFYING EPOCHS starting from the second update() call (the first call has no prior value, hence no slope, hence is not itself a qualifying epoch); fires() therefore becomes true on the 51st update() call for a maximally-flat curve -- the '50th consecutive qualifying epoch' language in the plan is satisfied by this counting (verified directly in PlateauDetectorTests, and integration-verified through RunController.run_stage at exactly adam_epochs_used==51)."
  - "RunController is constructed per-stage (mirrors TrainingConfig/ScheduledWeights being single-stage-scoped as landed by 40-04/40-02); run_stage(k) is callable repeatedly on one instance (each call builds a fresh Adam optimizer + fresh CosineAnnealingLR, verified by a spy test), matching how 40-06's CurriculumController is expected to drive it."
  - "Loss-term composition: L_data uses the full multi-identity FixedBatch.data_points (direct forward, no AD). L_IC/L_E/L_L anchor on ONE deterministic representative identity per fixed batch (first replay key, falling back to the first data-point identity) because pinn.loss_catalog's ic_anchor_loss/soft_energy_loss/angular_momentum_loss are single-trajectory-scoped by signature (angular_momentum_loss's l0 argument is reshaped to (3,), which structurally rejects a per-row batch) -- this is the ONLY existing reference Adam loop's (overfit_probe.py) convention, extended minimally to Phase 40's multi-identity batch. h0/l0 for the anchor identity are computed from its ground-truth snapshot-0 position/velocity via pinn.loss_catalog's own matched-Plummer/angular-momentum helpers (reused, not duplicated, to avoid a divergent second formula copy). eps_h is a provisional |h0|*1e-4 scale (mirrors the documented eps_h = 1e-4*S_H form; no S_H pipeline exists upstream of this plan) with a tiny additive floor."
  - "L_phys/L_E/L_L draw their interior evaluation TIMES from CollocationSampler.uniform() only; FixedBatch.collocation_points is never read for these terms (proven by a poisoned-NaN test on batch.collocation_points.times that still returns a finite loss)."
  - "L-BFGS chunking targets ONLY the L_data term (accumulate_chunked_data_term), not the causal physics loss: causal_physics_loss's prefix-cumsum causal weight has a cross-element dependency on the FULL ordered sequence, so chunking it independently would silently break the causal weighting (the accepted 'equals a full-batch mean backward' equality only holds for a plain independent-row mean, which L_data is and L_phys is not)."
  - "The L-BFGS phase's non-finite-gradient check is an explicit post-closure torch.isfinite over model.parameters() grads (self._grads_finite()), NOT the GradClipper flag -- GradClipper has no L-BFGS call site by construction, so the Adam-only clipper signal cannot cover this phase; this is the second half of the two-checks-total non-finite contract (loss isfinite before backward in both phases; gradient-flag in Adam, explicit grad-isfinite in L-BFGS)."
  - "Adam epoch and L-BFGS epoch share ONE running epoch_count and ONE train_loss_history/val_loss_history across both phases, so validation_every and StageExitMachine.evaluate see a single continuous stage timeline rather than two disjoint per-phase counters."
  - "StageExitMachine.evaluate is polled only during the L-BFGS phase, never during Adam -- the Adam phase's only internal exit signal is PlateauDetector.fires() (handoff) or budget exhaustion (also a handoff); this matches the plan's explicit design ('the stage falls through to StageExitMachine.evaluate' only after the Adam->L-BFGS transition) and keeps ADVANCE reachable only from a state where the held-out validation gate has actually been evaluated post-handoff."

patterns-established:
  - "Params-iterable-consumed-twice caller discipline: GradClipper.clip materializes its params argument into a list internally (Rule 1 fix, see Deviations) so any future caller may pass a live generator (model.parameters()) safely."

requirements-completed: [TRAIN-02]

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "PlateauDetector (CTX-46): 50-consecutive-flat-slope-epoch Adam->L-BFGS handoff detector, resetting on any violating epoch, structurally distinct from stage_exit.py's TotalLossPlateauSmoother."
    requirement: "TRAIN-02"
    verification:
      - kind: unit
        ref: "tests/phase40/test_optimizer_phase.py#PlateauDetectorTests (4 tests)"
        status: pass
    human_judgment: false
  - id: D2
    description: "RunController.run_stage(k): fresh Adam+CosineAnnealingLR per stage, per-epoch resampled batches via build_stage_batch, Adam-only GradClipper.clip after backward before step, plateau-or-budget-exhaustion handoff to a frozen-lambda no-clip fixed-batch L-BFGS phase with accumulate-in-closure chunking, polling StageExitMachine.evaluate every L-BFGS epoch until a non-None disposition."
    requirement: "TRAIN-02"
    verification:
      - kind: unit
        ref: "tests/phase40/test_optimizer_phase.py#RunControllerControlFlowTests (10 tests: plateau handoff timing, budget-exhaustion handoff, fresh-optimizer-per-stage, NaN/Inf and non-finite-gradient RECOVER in both phases, finite-stall-not-RECOVER, clip-spy 1/0 counts, build_stage_batch-not-in-closure, lambda-frozen-across-lbfgs)"
        status: pass
    human_judgment: false
  - id: D3
    description: "TRAIN-06 wiring: a real (non-injected) no-parameter-update validation pass at validation_every cadence against the dedicated validation_source, populating val_loss_history (criterion 2) and exposing val_phys/val_energy as the .phys/.energy of the same compose_total return (criteria 3/4), with the model always restored to .train() even on a raising forward."
    requirement: "TRAIN-02"
    verification:
      - kind: unit
        ref: "tests/phase40/test_optimizer_phase.py#RunControllerValidationWiringTests (3 tests: real-wiring identity vs direct recompute, train-mode restoration on raise, single-collocation-source guarantee)"
        status: pass
    human_judgment: false
  - id: D4
    description: "Chunked-accumulation correctness: accumulate_chunked_data_term's len(chunk)/N_total-weighted per-chunk backward equals a single full-batch mean-reduction backward to allclose, on a real model; chunk size is read from TrainingConfig.opt.lbfgs_chunk_size."
    requirement: "TRAIN-02"
    verification:
      - kind: unit
        ref: "tests/phase40/test_optimizer_phase.py#ChunkedAccumulationTests (2 tests)"
        status: pass
    human_judgment: false
  - id: D5
    description: "Cross-plan M1 non-finite contract consumer half: controllers.py never wraps GradClipper.clip in try/except; branches on the returned GradClipOutcome.non_finite flag."
    requirement: "TRAIN-02"
    verification:
      - kind: unit
        ref: "tests/phase40/test_prohibitions.py#NonFiniteContractTests.test_controllers_does_not_catch_around_clip"
        status: pass
    human_judgment: false

# Metrics
duration: ~50min
completed: 2026-07-17
status: complete
---

# Phase 40 Plan 05: RunController Adam->L-BFGS Optimizer Phase Summary

**RunController.run_stage(k) — the real Adam→L-BFGS two-phase closure loop with per-epoch resampled batches, Adam-only median gradient clipping, the CTX-46 50-epoch plateau handoff (or budget-exhaustion fallback), a frozen-λ fixed-batch L-BFGS phase with chunked-accumulation gradients, and a real held-out validation pass wiring StageExitMachine's ADVANCE criteria 2–4.**

## Performance

- **Duration:** ~50 min
- **Started:** 2026-07-17 (session start)
- **Completed:** 2026-07-17T10:48:04Z
- **Tasks:** 2 (PlateauDetector; RunController), committed as one atomic unit — both land in the same file with Task 2 directly depending on Task 1's class, matching the 40-02 precedent for tightly-coupled same-file tasks
- **Files modified:** 3 (2 created, 1 modified)

## Accomplishments

- **PlateauDetector (CTX-46):** transcribes the 50-consecutive-flat-slope-epoch Adam→L-BFGS handoff rule exactly — `update(l_phys)` tracks the per-epoch finite difference of `log10(L_phys)`, incrementing a consecutive-qualifying-epoch counter while the slope exceeds `-5e-3` and resetting on any violation (or the unavoidable first call, which has no prior value). `fires()` becomes true on the 51st call for a maximally flat curve (the "50th consecutive qualifying epoch," since the first call establishes the baseline rather than counting as qualifying itself). Holds no reference to `stage_exit.py`'s `TotalLossPlateauSmoother`.
- **RunController (TRAIN-02):** the full inner two-phase loop. Adam phase: fresh `torch.optim.Adam` + fresh `CosineAnnealingLR` per stage, per-epoch `build_stage_batch` resampling with a freshly-advancing seeded `Generator`, `GradClipper.clip` (Adam-only) between backward and step, and the two pinned non-finite checks (`torch.isfinite` on the loss before backward; branch on `GradClipOutcome.non_finite` after clip) — both routing to `StageDisposition.RECOVER` with no raise and no try/except. The Adam loop is hard-bounded by `N_Adam,k`; a plateau fire breaks early (`trigger="plateau"`), while exhausting the budget without firing still hands off to L-BFGS (`trigger="budget-exhausted"`) per the GAP-40-02 → A ruling. L-BFGS phase: `ScheduledWeights.freeze()` (queried once, reused for every closure call — entry≡exit by construction), one fixed batch and one fixed set of `CollocationSampler`-drawn times drawn once at handoff, `torch.optim.LBFGS` with a closure that chunks `L_data` via `accumulate_chunked_data_term` (weighted `len(chunk)/N_total`, proven equal to a full-batch mean backward) and computes the other four terms once per closure call, with no clip call, no λ update, and no batch resample inside it. `StageExitMachine.evaluate` is polled every L-BFGS epoch until a non-None disposition; `run_stage` always returns a non-Optional `StageDisposition` (HALT at `MAX_EPOCHS` by construction).
- **TRAIN-06 wiring:** a real, non-injected validation pass runs at the `validation_every` cadence against the dedicated `validation_source` (never a slice of the training batch), populating `val_loss_history` (criterion 2, min-tracked) and exposing `val_phys`/`val_energy` as the `.phys`/`.energy` fields of the same `compose_total` return `StageExitMachine.evaluate` consumes for criteria 3/4 — verified by capturing the actual (batch, anchor context, weights) the pass used and directly recomputing `compose_total` on them for an allclose match. The model is always restored to `.train()` in a `finally`, even when the forward raises.
- **Single collocation-point source:** `L_phys`/`L_E`/`L_L` draw their evaluation times exclusively from `CollocationSampler`; `FixedBatch.collocation_points` is never read for these terms, proven by poisoning `batch.collocation_points.times` with NaN and confirming the loss stays finite.
- **Chunked-accumulation correctness:** `accumulate_chunked_data_term`, a standalone module function, is independently verified against a real model: chunked, `len(chunk)/N_total`-weighted per-chunk backward matches a single full-batch mean-reduction backward to `allclose` on every parameter's gradient.

## Task Commits

Both tasks land in one atomic commit (same file, Task 2 depends directly on Task 1's `PlateauDetector` class; splitting would require an intermediate broken/partial file state):

1. **Task 1: PlateauDetector (CTX-46)** + **Task 2: RunController (TRAIN-02 part b)** — `2e80131` (feat)

**Plan metadata:** committed separately below (this SUMMARY + STATE/ROADMAP).

## Files Created/Modified

- `pinn/training/controllers.py` — `PlateauDetector`, `HandoffEvent`, `accumulate_chunked_data_term`, `RunController` (the inner Adam→L-BFGS loop; `CurriculumController` is added by 40-06 in the same file).
- `tests/phase40/test_optimizer_phase.py` — 21 tests across `PlateauDetectorTests`, `RunControllerConstructionTests`, `RunControllerControlFlowTests`, `RunControllerValidationWiringTests`, `ChunkedAccumulationTests`.
- `pinn/training/grad_clip.py` — adds `GradClipper.state_dict()`/`load_state_dict()` (deferred from 40-02); fixes the params-generator-consumed-twice bug (see Deviations).

## Decisions Made

See frontmatter `key-decisions` for the full list. Headline decisions: (1) PlateauDetector's counting semantics (first call is baseline, not a qualifying epoch — fires on the 51st call for a maximally flat curve); (2) RunController is per-stage-constructed with `run_stage(k)` callable repeatedly; (3) `L_data` batches over the full multi-identity `FixedBatch` while `L_IC`/`L_E`/`L_L` anchor on one representative identity per batch (forced by `pinn.loss_catalog`'s single-trajectory-scoped signatures); (4) chunking targets only `L_data` (not the causal physics loss, whose prefix-cumsum weight has cross-element dependencies that chunking would silently break); (5) the L-BFGS phase's gradient non-finite check is an explicit post-closure `isfinite`, not the (Adam-only) clipper flag.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] `GradClipper.clip` silently no-oped its apply call when passed a live generator**
- **Found during:** Task 2 (first real `run_stage` execution against the stub model) — a `UserWarning: 'parameters' is an empty generator, no gradient clipping will occur` surfaced from `torch.nn.utils.clip_grad_norm_` inside `grad_clip.py`.
- **Issue:** `GradClipper.clip(params, *, stage)` (landed in 40-02) calls `torch.nn.utils.clip_grad_norm_(params, ...)` TWICE internally (measure, then apply). `RunController` calls it with `self._model.parameters()` — a fresh generator per call, but ONE-SHOT: the measure call fully consumes it, leaving the apply call an empty iterable. The clip was silently never applied (no exception, no test failure — just a swallowed warning), which would have been a correctness bug (unbounded gradients) in any real training run.
- **Fix:** `GradClipper.clip` now materializes `params = list(params)` at its own top, before either internal call, so any caller (including one passing a one-shot generator) gets correct behavior. This is the more robust fix than only changing the call site in `controllers.py`, since it protects every future caller of the same public entry point.
- **Files modified:** `pinn/training/grad_clip.py` (outside this plan's stated `files_modified`, but directly caused by this plan's first real integration of the two modules, and the smallest correct fix).
- **Verification:** Re-ran the full `tests/phase40` suite (129/129 pass) with the warning gone; `tests/phase40/test_grad_clip.py` (14/14) and `tests/phase40/test_prohibitions.py` (both halves of the M1 audit) still pass unchanged.
- **Commit:** `2e80131` (same commit as the rest of this plan's work).

**2. [Rule 2 - Missing Critical] Added `GradClipper.state_dict()`/`load_state_dict()`**
- **Found during:** Task 2 (implementing `RunController.state_dict()`, which the plan's action text requires to compose "the model + schedule + clipper + optimizer-relevant state").
- **Issue:** 40-02 explicitly deferred this to 40-05 (see 40-02-SUMMARY.md "Next Phase Readiness": "GradClipper does not yet expose `state_dict()`/`load_state_dict()`; 40-05 (or Phase 41) adds it when composing the RunController's checkpoint dict"). Without it, `RunController.state_dict()` could not honestly compose the clipper's rolling-window state.
- **Fix:** Added a minimal `state_dict()`/`load_state_dict()` pair serializing the rolling window as plain python floats (weights_only-clean, CTX-44) plus the `C_stage` table/median floor/window length for round-trip fidelity.
- **Files modified:** `pinn/training/grad_clip.py`.
- **Verification:** `tests/phase40/test_grad_clip.py` unchanged and passing (no new AC in this plan tests state_dict round-trip explicitly, so this is additive, untested-beyond-import surface, exactly as 40-02 anticipated).
- **Commit:** `2e80131`.

---

**Total deviations:** 2 auto-fixed (1 bug, 1 missing-critical). Both are minimal, targeted, and necessary for `RunController` to actually function correctly / honestly implement the plan's stated checkpoint contract. No scope creep beyond `pinn/training/grad_clip.py`, which both deviations touch for good reason (the plan's own upstream summary forecast exactly the second one).

## Issues Encountered

- **`pinn.loss_catalog`'s energy/angular-momentum loss functions are single-trajectory-scoped**, not designed for Phase 40's multi-identity `FixedBatch`. Resolved by anchoring `L_IC`/`L_E`/`L_L` on one deterministic representative identity per fixed batch (documented at length in `controllers.py`'s module docstring and in this SUMMARY's key-decisions) rather than inventing a new multi-trajectory batched loss variant outside this plan's scope. This is a genuine architecture gap between Phase 38's loss catalog and Phase 40's multi-identity batch contract; it is not one of the five v2.0 owner-carved seam decisions (D1-p, D4-a, R-1/R-2, B-5), so it was resolved as a pragmatic, documented engineering choice rather than escalated as a STOP-protocol gap (v2.0 is a build milestone, not a specwork adjudication milestone — the STOP protocol in `CLAUDE.md` scopes to v1.4–v1.6-style adjudication).
- **`h0`/`l0`/`eps_h`** (needed for the soft-energy and angular-momentum loss terms) have no dedicated upstream computation pipeline yet (`AdmittedRecord.E`/`l_ratio` exist but are not exposed by the dataset-free stub source, and are normalized/scaled differently from the raw `H(u=0)` the loss function expects). Resolved by computing them directly from the anchor identity's ground-truth snapshot-0 position/velocity via `pinn.loss_catalog`'s own (reused, not duplicated) matched-Plummer/angular-momentum helpers, with `eps_h` as a provisional `|h0|*1e-4` scale. Flagged here for Phase 41/43 (ACC-05) calibration, consistent with every other provisional constant in this phase (`C_stage`, `median_floor`, `lbfgs_max_iter`, `lbfgs_chunk_size`).

## User Setup Required

None — dataset-free, no external service configuration.

## Next Phase Readiness

- **Ready for 40-06 (CurriculumController):** `RunController.run_stage(k) -> StageDisposition` is the pinned entry point; `RunController.state_dict()`/`load_state_dict()` compose model + schedule + clipper state for CurriculumController/Phase 41 to persist at stage boundaries via the injected `CheckpointStore`.
- **Provisional values surfaced for ACC-05 (Phase 43 pilot) calibration:** the anchor-identity `eps_h` scale factor (`1e-4 * |h0|`), alongside the already-provisional `C_stage`/`median_floor`/`lbfgs_max_iter`/`lbfgs_chunk_size` from 40-02/40-04.
- **No blockers.**

---
*Phase: 40-stage-0-curriculum-training-loop-fut-04 (plan 05)*
*Completed: 2026-07-17*
