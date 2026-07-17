---
phase: 40-stage-0-curriculum-training-loop-fut-04
verified: 2026-07-17T12:00:00Z
status: gaps_found
score: 3/5 roadmap success criteria verified (2 partially failed)
behavior_unverified: 0
overrides_applied: 0
gaps:
  - truth: "Roadmap SC1 / TRAIN-01: CurriculumController drives a real outer CURRICULUM loop (multiple stages), not only a single-stage dispatch."
    status: failed
    reason: "CurriculumController is constructed with exactly ONE fixed RunController / ScheduledWeights / TrainingConfig triple for its entire lifetime. On ADVANCE it only calls ScheduledWeights.rewarm() -- it never reconstructs ScheduledWeights with the new stage's lambda_e_max/lambda_l_max, and never swaps TrainingConfig (n_adam, max_epochs, beta, eps_phys, eps_energy stay pinned to stage 0's values for every later stage). The only test that drives multi-stage progression (PreflightGateTests.test_advancing_into_stage_three_raises_before_run_stage) uses forced_disposition=lambda k: ADVANCE with NO live RunController, so it proves only that the stage counter increments -- it cannot and does not exercise real per-stage reconfiguration."
    artifacts:
      - path: "pinn/training/controllers.py"
        issue: "CurriculumController.__init__ (lines ~699-734) takes one fixed run_controller/scheduled_weights pair; step()'s ADVANCE branch (lines ~837-847) never reconstructs either per new stage."
    missing:
      - "A stage_factory seam (or equivalent) that reconstructs RunController/ScheduledWeights/TrainingConfig with the new stage's parameters on ADVANCE, OR an explicit code comment + SPEC/CONTEXT amendment stating multi-stage per-stage reconfiguration is intentionally deferred beyond Phase 40 (SPEC.md already defers 'full multi-stage curriculum beyond the Stage 0-2 full-batch path' to PLAT-01, but the code does not reference this deferral anywhere, and the module's own docstrings claim the opposite behavior already happens)."
  - truth: "Roadmap SC4 / TRAIN-06: the stage-exit machine routes ADVANCE when all four gate criteria hold -- no silent dead end."
    status: failed
    reason: "StageExitMachine.evaluate() -- the only place ADVANCE can be produced -- is called exclusively from RunController._run_lbfgs_phase. When a stage's Adam phase consumes the entire budget (n_adam_k == max_epochs), run_stage() computes remaining_budget = 0 and returns StageDisposition.HALT directly, WITHOUT ever calling evaluate(). StageConfig.__post_init__ only rejects n_adam > max_epochs; equality is explicitly validated as legal (test_config.py::test_n_adam_eq_max_epochs_ok). So a configuration the codebase's own validator certifies as valid guarantees that stage can NEVER ADVANCE, regardless of how well the loss/physics/energy criteria are satisfied during Adam. No test in the suite constructs this scenario against a real (non-forced) RunController -- it is undetected by the 142/142 green suite."
    artifacts:
      - path: "pinn/training/controllers.py"
        issue: "run_stage() (lines ~598-640): 'remaining_budget = max(max_epochs - adam_epochs_used, 0); if remaining_budget == 0: return StageDisposition.HALT' -- returns before ever calling the stage-exit gate."
    missing:
      - "Poll StageExitMachine.evaluate() once more when the Adam budget is exhausted with zero L-BFGS remainder, before falling back to HALT; or tighten StageConfig validation to require n_adam < max_epochs (strict) so this configuration cannot be constructed."
  - truth: "Roadmap SC4 / TRAIN-06: RECOVER rolls back to the last well-formed checkpoint (NaN/Inf, bounded retry budget)."
    status: failed
    reason: "CurriculumController.step()'s RECOVER branch calls self._checkpoint_store.rollback() purely to detect EmptyCheckpointStore; the returned state (which includes payload['run_controller'], exactly the dict RunController.load_state_dict() expects and is fully implemented to consume) is discarded on every call. RunController.load_state_dict() exists (controllers.py:289-292) but is never invoked from CurriculumController. At the ratified default recover_retries=0 this is masked (RECOVER always falls straight to HALT with no retrain, so the discarded restore has no visible effect on THIS run), but for any recover_retries > 0 -- a value the constructor explicitly accepts and range-validates -- a retried stage would resume training from the SAME diverged/NaN-producing parameters that triggered the RECOVER, not from 'the last well-formed checkpoint' as both this module's own docstring and ctl_instruction.md's RECOVER contract require. The one existing 'rolls back' test (test_forced_recover_at_retries_zero_rolls_back_and_halts_with_no_retrain) only asserts rollback() was CALLED (a spy call-count) and the terminal disposition/stage -- it uses forced_disposition with no live RunController, so there is no state to restore in that test and it structurally cannot catch this gap. A second test (test_recover_branch_catches_empty_checkpoint_store) only greps source text for 'except EmptyCheckpointStore'."
    artifacts:
      - path: "pinn/training/controllers.py"
        issue: "step()'s RECOVER branch (lines ~849-865): 'self._checkpoint_store.rollback()' return value dropped; RunController.load_state_dict is never called anywhere in this file."
    missing:
      - "if self._run_controller is not None and 'run_controller' in restored: self._run_controller.load_state_dict(restored['run_controller']) inside the RECOVER branch, plus a behavioral test that seeds known checkpoint weights, mutates live model weights, forces RECOVER with recover_retries=1, and asserts the model matches the seeded checkpoint after the retry begins."
deferred: []
human_verification: []
---

# Phase 40: Stage-0 Curriculum Training Loop (FUT-04) Verification Report

**Phase Goal:** The trainer runs Stage 0 end-to-end -- the two-phase Adam→L-BFGS closure loop with PHYS-05 scheduled weights, the collocation sampler, merged gradient clipping, and the ADVANCE/RECOVER/HALT stage-exit machine -- implementing the `ctl_instruction.md` Stage-0 contract without re-deciding it.
**Verified:** 2026-07-17
**Status:** gaps_found
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths (mapped 1:1 to ROADMAP Success Criteria)

| # | Truth (ROADMAP SC) | Status | Evidence |
|---|---|---|---|
| 1 | SC1: CurriculumController/RunController drive an outer curriculum + inner optimization loop that trains Stage 0 (TRAIN-01), running the two-phase Adam→L-BFGS closure (TRAIN-02) | ⚠️ **FAILED (partial)** | Single-stage dispatch (ADVANCE/RECOVER/HALT), checkpoint anchors, and the closure mechanics (accumulate-in-closure, frozen-λ, no-clip-during-L-BFGS, fresh-optimizer-per-boundary) are correctly implemented and test-verified (`ComposedGateEarnedAdvanceTests`, `test_optimizer_phase.py`). **But** the "outer curriculum loop" framing of TRAIN-01 is not actually multi-stage correct: `CurriculumController` never reconstructs per-stage `ScheduledWeights`/`TrainingConfig` on ADVANCE (CR-03, see gaps), and `RunController.run_stage`'s ADVANCE path is structurally unreachable for a valid, tested `n_adam == max_epochs` config (CR-02, see below). |
| 2 | SC2: PHYS-05 scheduled-weight module (warmup, per-stage λ^max ≤1, frozen/re-warm, checkpoint-serialized state) (TRAIN-03); collocation sampler (uniform + adaptive hook) (TRAIN-04) | ✓ **VERIFIED** | `scheduled_weights.py` + `test_scheduled_weights.py` (warmup formula, λ_E≤1 across the per-stage table, freeze/re-warm, `state_dict`/`load_state_dict` round-trip); `collocation_sampler.py` + `test_collocation_sampler.py` (uniform bounds/count, adaptive hook signature, caller-owned RNG). No findings against either module in the committed code review. |
| 3 | SC3: Merged gradient clipping `clip_value = C_stage · median(grad_norm_history)`, per-stage C-table, rolling window, none during L-BFGS (TRAIN-05) | ✓ **VERIFIED** | `grad_clip.py` + `test_grad_clip.py`: clip formula, `torch.median` (not numpy/statistics, even-length semantics), partial-window bootstrap, non-finite-returns-flag-not-raise contract, window-integrity (non-finite never appended). **WARNING** (not a truth failure): `GradClipper.load_state_dict` hardcodes the restored window's dtype to `float64` regardless of the run's actual dtype (WR-01) -- untested, zero round-trip test exists; relevant to Phase 41 resume correctness, not to the clip formula itself. |
| 4 | SC4: Stage-exit machine routes ADVANCE (plateau+validation+ε_phys/ε_energy) / RECOVER (NaN/Inf, default `recover.retries: 0`) / HALT-REVIEW (max-epoch/stagnation), no fallback advancement (TRAIN-06) | ✗ **FAILED** | The four-criterion gate FORM is correctly implemented and tested in isolation (`stage_exit.py` + `test_stage_exit.py`: all-four-required, NaN/Inf→RECOVER regardless of phase, max-epoch→HALT, no fallback ADVANCE). But the **wiring** in `controllers.py` breaks two of the three named dispositions in ways the 142/142 suite does not catch: (a) ADVANCE is structurally unreachable when a stage's Adam phase consumes its entire budget (`n_adam == max_epochs`, explicitly validated as legal by `test_config.py::test_n_adam_eq_max_epochs_ok`) -- `StageExitMachine.evaluate()` is simply never called in that path; (b) RECOVER's "rollback to the last well-formed checkpoint" is not wired -- `CheckpointStore.rollback()`'s returned state is discarded and `RunController.load_state_dict()` is never invoked, masked only because the ratified default `recover_retries=0` never re-enters a retry loop. Both are confirmed by direct code reading (not merely absent tests) -- see gaps below. |
| 5 | SC5: A preflight refuses stages 3-6 with a typed stop until sL-BFGS exists (TRAIN-07) | ✓ **VERIFIED** | `slbfgs_preflight.py` + `test_slbfgs_preflight.py`: stage≥3 raises `StochasticLBFGSNotImplemented` (non-empty message, `.stage` field); stages {0,1,2} do not raise. Wired into `CurriculumController.step()` via `check_stage_preflight(k)` before any disposition is obtained, confirmed by `PreflightGateTests`. |

**Score:** 3/5 roadmap success criteria fully verified; 2/5 (SC1, SC4) contain code-proven wiring defects in `controllers.py` that a passing 142/142 test suite does not exercise.

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `pinn/training/__init__.py` | Barrel re-exporting TrainingConfig/CurriculumController/RunController/CheckpointStore, side-effect-free import | ✓ VERIFIED | Confirmed by direct import: `dir(pinn.training)` contains all 4 names; docstring discipline matches `pinn/data`/`pinn/verification`. |
| `pinn/training/scheduled_weights.py` | PHYS-05 schedule module | ✓ VERIFIED | 262 lines, well-specified per code review, no findings. |
| `pinn/training/grad_clip.py` | Adam-only merged clipper | ✓ VERIFIED (core); ⚠️ WARNING (checkpoint dtype, WR-01) | 293 lines. |
| `pinn/training/collocation_sampler.py` | Uniform + adaptive sampler | ✓ VERIFIED | 143 lines, no findings. |
| `pinn/training/slbfgs_preflight.py` | Typed refusal for stages 3-6 | ✓ VERIFIED | 49 lines, no findings. |
| `pinn/training/stage_exit.py` | StageExitMachine (ADVANCE/RECOVER/HALT form) | ✓ VERIFIED (form); ⚠️ WARNING (stagnation-window branch untested, WR-04) | 230 lines. |
| `pinn/training/config.py` | TrainingConfig nested frozen dataclasses | ✓ VERIFIED (core); ⚠️ WARNING (`energy_floor_factor` silently unused, WR-02) | 299 lines. |
| `pinn/training/checkpoint.py` | CheckpointStore Protocol + naive impl | ✓ VERIFIED | 95 lines; `weights_only=True` on load/rollback confirmed; `EmptyCheckpointStore` raised on empty store. |
| `pinn/training/controllers.py` | RunController + CurriculumController (the two driver classes) | ⚠️ **STUB-ADJACENT WIRING DEFECTS** | 892 lines; exists, substantive, imported/used by tests and the package barrel -- but contains the 3 code-proven defects (CR-01, CR-02, CR-03) detailed in Gaps below. Not a stub (extensive real logic), but the wiring that connects the well-tested unit modules together is incomplete on 2 of 3 stage-exit dispositions and on multi-stage reconfiguration. |

### Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| `CurriculumController.step()` | `RunController.run_stage(k)` / forced-disposition seam | `_get_disposition()` | ✓ WIRED | Confirmed exactly-one-of guard (`ForcedDispositionOnLiveRun` at construction) and dispatch tests pass. |
| `RunController.run_stage(k)` | `StageExitMachine.evaluate(...)` | called from `_run_lbfgs_phase` only | ⚠️ **PARTIAL** | Wired for the case where an L-BFGS phase actually runs; **NOT WIRED** for the `remaining_budget == 0` case (CR-02) -- the gate is bypassed entirely, defaulting to HALT. |
| `CurriculumController.step()` (RECOVER) | `CheckpointStore.rollback()` → `RunController.load_state_dict()` | intended per module docstring | ✗ **NOT WIRED** | `rollback()` is called and its return value is discarded; `load_state_dict()` exists on `RunController` (confirmed at controllers.py:289-292, composing `model.load_state_dict` + `scheduled_weights.load_state_dict` + `grad_clipper.load_state_dict`) but is never called from `CurriculumController` (CR-01). |
| `CurriculumController` (ADVANCE) | fresh per-stage `ScheduledWeights`/`TrainingConfig` | intended per module docstring ("constructs a new ScheduledWeights for that stage") | ✗ **NOT WIRED** | Only `ScheduledWeights.rewarm()` is called; no reconstruction of either object occurs on stage advance (CR-03). |
| `pinn.training` barrel | `CurriculumController`, `RunController`, `TrainingConfig`, `CheckpointStore` | `__init__.py` re-export | ✓ WIRED | Confirmed by direct `import pinn.training` + `dir()` check; no model build / dataset discovery at import time. |
| `ScheduledWeights.current(epoch)` | `pinn.loss_catalog.LossWeights` / `compose_total` | direct construction, fed to `compose_total` | ✓ WIRED (per 40-02 tests; not independently re-derived here beyond the passing suite). |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| Full dataset-free `tests/phase40` suite | `python -m unittest discover -s tests/phase40 -p 'test_*.py'` (pinn-train env) | `Ran 142 tests ... OK` | ✓ PASS (independently re-run, not just trusted from SUMMARY) |
| Regression: phase37 | `python -m unittest discover -s tests/phase37 -p 'test_*.py'` | `Ran 55 tests ... OK` | ✓ PASS |
| Regression: phase38 | `python -m unittest discover -s tests/phase38 -p 'test_*.py'` | `Ran 128 tests ... OK` | ✓ PASS |
| Regression: phase39 | `python -m unittest discover -s tests/phase39 -p 'test_*.py'` | `Ran 264 tests ... OK` | ✓ PASS -- note: the task brief cited "104 OK" for phase39; the independently re-run count is 264/264 passing (sum of all `test_phase39/test_*.py` files' `def test_` counts also totals 264). This is a discrepancy in the cited figure, not a regression -- more tests pass than claimed, none fail. Flagged for accuracy only. |
| Package barrel import side-effect-free | `python -c "import pinn.training as t; assert all(hasattr(t,n) for n in (...))"` | 4/4 names present, no exception | ✓ PASS |
| Anti-pattern scan (TBD/FIXME/XXX/TODO/HACK/PLACEHOLDER/"not yet implemented") | `grep` across `pinn/training/*.py` + `tests/phase40/*.py` | zero matches | ✓ PASS (no unresolved debt markers) |
| CR-01/CR-02/CR-03 direct code inspection | `Read` of `controllers.py` lines ~242-292, ~570-640, ~675-870; `Read` of `tests/phase40/test_controllers.py` lines 181-248 | All 3 findings independently confirmed against the actual source, not merely trusted from 40-REVIEW.md | Confirms 40-REVIEW.md's 3 critical findings are accurate, not overstated. |

### Requirements Coverage

| Requirement | Source Plan | Description | Verifier Status | Evidence |
|---|---|---|---|---|
| TRAIN-01 | 40-01 (frontmatter), 40-06 (delivers) | CurriculumController + RunController outer/inner loop | **PARTIAL** | Single-stage dispatch VERIFIED; real multi-stage reconfiguration BLOCKED (CR-03). |
| TRAIN-02 | 40-01, 40-05 (delivers) | Two-phase Adam→L-BFGS closure | **PARTIAL** | Closure mechanics (accumulate-in-closure, frozen-λ, no-clip, fresh-optimizer) VERIFIED; ADVANCE-reachability boundary at `n_adam==max_epochs` BLOCKED (CR-02). |
| TRAIN-03 | 40-01, 40-02 (delivers) | PHYS-05 scheduled-weight module | **SATISFIED** | `scheduled_weights.py` fully tested, no findings. REQUIREMENTS.md currently shows this `Pending` -- **stale**; code+test evidence supports `Complete`. |
| TRAIN-04 | 40-01, 40-03 (delivers) | Collocation sampler interface | **SATISFIED** | `collocation_sampler.py` fully tested, no findings. REQUIREMENTS.md shows `Pending` -- **stale**; should be `Complete`. |
| TRAIN-05 | 40-01, 40-02 (delivers) | Merged gradient clipping | **SATISFIED** (core formula); WARNING on checkpoint round-trip (WR-01, not literally required by TRAIN-05's text) | REQUIREMENTS.md shows `Pending` -- **stale**; should be `Complete`. |
| TRAIN-06 | 40-01, 40-04 (delivers) | Stage-exit ADVANCE/RECOVER/HALT machine | **BLOCKED** | Gate *form* correctly implemented in `stage_exit.py`; wiring in `controllers.py` breaks ADVANCE-reachability (CR-02) and RECOVER-rollback (CR-01). REQUIREMENTS.md currently marks this `[x] Complete` -- **should be reopened** pending the CR-01/CR-02 fixes. |
| TRAIN-07 | 40-01, 40-03 (delivers) | sL-BFGS preflight typed refusal | **SATISFIED** | `slbfgs_preflight.py` fully tested, wired into `CurriculumController.step()`. REQUIREMENTS.md shows `Pending` -- **stale**; should be `Complete`. |

**Requirements ledger reconciliation (task-directed):** All 7 requirement IDs are claimed across the 6 plans' `requirements:` frontmatter (40-01: all 7 as foundation scaffolding; 40-02: TRAIN-03/05; 40-03: TRAIN-04/07; 40-04: TRAIN-06; 40-05: TRAIN-02; 40-06: TRAIN-01/06) -- no orphaned requirements. `.planning/REQUIREMENTS.md`'s checklist is inaccurate in **both directions**: TRAIN-03/04/05/07 are marked `Pending` but are fully delivered and tested (should flip to `Complete`); TRAIN-01/02/06 are marked `[x] Complete` but this verification finds real, code-proven wiring defects in each (should be reopened, not simply left checked). This is not a case of "trust the code over stale docs" uniformly -- the docs are wrong on the Pending items AND the phase's own self-assessment was too optimistic on the Complete items.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---|---|---|---|
| `pinn/training/controllers.py` | ~849-852 (RECOVER branch) | Discarded return value from a state-restoring call (`self._checkpoint_store.rollback()`) | 🛑 Blocker | CR-01: rollback-to-checkpoint never actually restores model state; masked only by the default `recover_retries=0`. |
| `pinn/training/controllers.py` | ~634-636 (`run_stage`) | Early return bypassing the only gate-evaluation call site | 🛑 Blocker | CR-02: ADVANCE structurally unreachable for a legally-constructible config. |
| `pinn/training/controllers.py` | ~699-734, ~837-847 | Fixed single collaborator instances never refreshed across a loop that is supposed to iterate them | ⚠️ Warning | CR-03: multi-stage curriculum progression silently reuses stage-0 parameters; SPEC.md defers "full multi-stage curriculum beyond Stage 0-2" to PLAT-01, but the code does not document this as an intentional limitation, and the module's own docstrings claim the opposite already happens. |
| `pinn/training/grad_clip.py` | ~288-293 | Hardcoded `dtype=torch.float64` on checkpoint restore | ⚠️ Warning | WR-01: silently corrupts window dtype after resume in a non-float64 run; zero test coverage. |
| `pinn/training/controllers.py` + `config.py` | 230, 338 vs. 69/110/263-264 | Documented config-overridable field silently shadowed by a hardcoded module constant | ⚠️ Warning | WR-02: `energy_floor_factor` override has zero effect; blocks the field's stated ACC-05 (Phase 43) calibration purpose. |
| `pinn/training/config.py` | 99-123 | Required, validated config field with zero consumers | ⚠️ Warning | WR-03: `percentile_10_relaxation` is dead weight or an incomplete HALT/REVIEW wiring gap. |
| `pinn/training/stage_exit.py` | 195-213 | Spec-grounded branch with zero test coverage | ⚠️ Warning | WR-04: stagnation-window HALT path unverified in a module described as "the SINGLE binding, executable encoding" of the decision machine. |
| `tests/phase40/test_controllers.py` | 224-227 | Test asserts source-text substring presence, not behavior | ⚠️ Warning | WR-05: `test_recover_branch_catches_empty_checkpoint_store` cannot detect CR-01; its name overstates its coverage. |

No `TBD`/`FIXME`/`XXX`/`TODO`/`HACK`/`PLACEHOLDER` debt markers found in any Phase-40 file (mechanical grep, zero matches) -- the defects above are logic/wiring gaps, not flagged debt.

### Human Verification Required

None. All findings above are resolved by direct static-code inspection (return-value tracing, call-site enumeration, config-validation reading) rather than runtime behavior that only a human or a live run could observe. CR-01, CR-02, and CR-03 are not "untested but might work" -- each is a code path that provably cannot execute the claimed behavior regardless of any test, confirmed by reading the actual source independently of `40-REVIEW.md`'s narrative.

### Gaps Summary

The five well-isolated numeric/interface modules this phase built first -- `scheduled_weights.py` (TRAIN-03), `collocation_sampler.py` + `slbfgs_preflight.py` (TRAIN-04/07), `grad_clip.py` (TRAIN-05 core), and `stage_exit.py`'s gate *form* (TRAIN-06 core) -- are correctly implemented and thoroughly tested; none of the 3 critical findings originate there. All 3 critical findings live in `controllers.py`, the wiring layer that composes those modules into `RunController`/`CurriculumController` (TRAIN-01/TRAIN-02/TRAIN-06's dispatch), and all 3 are on code paths the current 142/142-passing suite does not exercise:

1. **RECOVER never restores model state from the rollback** (CR-01) -- `CheckpointStore.rollback()`'s return value is discarded; `RunController.load_state_dict()` exists and is fully wired to consume it, but `CurriculumController` never calls it. Masked at the shipped default (`recover_retries=0`), but the constructor accepts and validates `recover_retries > 0`, and the requirement text ("RECOVER... rollback... with a bounded retry budget") names this behavior directly.
2. **ADVANCE is structurally unreachable when `n_adam == max_epochs`** (CR-02) -- a configuration the codebase's own validator certifies as legal. `StageExitMachine.evaluate()` is simply never called on this path; the stage HALTs unconditionally regardless of how well training actually did.
3. **Per-stage `ScheduledWeights`/`TrainingConfig` are never swapped across curriculum stages** (CR-03) -- `CurriculumController` holds one fixed collaborator triple for its whole lifetime; only `rewarm()` fires on ADVANCE. `SPEC.md` explicitly defers "full multi-stage curriculum beyond the Stage 0-2 full-batch path" to PLAT-01, which provides a plausible scope argument for deferring the FIX, but the code does not document this as an intentional limitation anywhere, and the module's own docstrings assert the opposite already happens -- an override/documentation decision this report defers to the maintainer rather than deciding unilaterally.

**This looks like it could be partially intentional (CR-03).** To accept CR-03 as an explicitly deferred limitation rather than a defect requiring a fix in this phase, add to this file's frontmatter:

```yaml
overrides:
  - must_have: "CurriculumController reconstructs per-stage ScheduledWeights/TrainingConfig on ADVANCE"
    reason: "SPEC.md Boundaries explicitly defers 'full multi-stage curriculum beyond the Stage 0-2 full-batch path' to PLAT-01; Phase 40's targeted deliverable is Stage 0 end-to-end, and the ADVANCE dispatch mechanism itself (checkpoint anchors, stage counter, rewarm) is correctly wired and tested."
    accepted_by: "<owner>"
    accepted_at: "<ISO timestamp>"
```

CR-01 and CR-02 do not have an equivalent scope argument: CR-02 can manifest within pure single-stage (Stage-0-only) operation for a config the codebase itself certifies as valid, and CR-01 breaks a mechanism (bounded-retry RECOVER) that the requirement text names directly and the constructor actively supports. Both should be fixed (the review's proposed fixes are small and localized) before this phase is considered closed, or explicitly overridden with equally clear reasoning if the maintainer judges the shipped default (`recover_retries=0`, and a not-yet-calibrated `n_adam`/`max_epochs` pair) makes both unreachable in practice for the Phase-43 pilot's actual usage.

---

_Verified: 2026-07-17_
_Verifier: Claude (gsd-verifier)_
