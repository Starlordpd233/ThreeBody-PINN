---
phase: 40-stage-0-curriculum-training-loop-fut-04
reviewed: 2026-07-17T00:00:00Z
depth: standard
files_reviewed: 21
files_reviewed_list:
  - pinn/training/__init__.py
  - pinn/training/scheduled_weights.py
  - pinn/training/grad_clip.py
  - pinn/training/collocation_sampler.py
  - pinn/training/slbfgs_preflight.py
  - pinn/training/stage_exit.py
  - pinn/training/config.py
  - pinn/training/checkpoint.py
  - pinn/training/controllers.py
  - tests/phase40/__init__.py
  - tests/phase40/_fixtures.py
  - tests/phase40/test_prohibitions.py
  - tests/phase40/test_scheduled_weights.py
  - tests/phase40/test_grad_clip.py
  - tests/phase40/test_collocation_sampler.py
  - tests/phase40/test_slbfgs_preflight.py
  - tests/phase40/test_stage_exit.py
  - tests/phase40/test_config.py
  - tests/phase40/test_checkpoint.py
  - tests/phase40/test_controllers.py
  - tests/phase40/test_optimizer_phase.py
findings:
  critical: 3
  warning: 5
  info: 2
  total: 10
status: issues_found
---

# Phase 40: Code Review Report

**Reviewed:** 2026-07-17T00:00:00Z
**Depth:** standard
**Files Reviewed:** 21
**Status:** issues_found

## Summary

Reviewed the Phase 40 training-driver layer (scheduled loss weights, Adam-only
grad clipper, collocation sampler, sL-BFGS typed refusal, stage-exit decision
machine, `TrainingConfig`, checkpoint seam, `RunController` / `CurriculumController`)
plus the full `tests/phase40` suite. The individual mechanism modules
(`scheduled_weights.py`, `grad_clip.py`, `collocation_sampler.py`,
`slbfgs_preflight.py`) are well-specified and their happy paths are correctly
implemented and thoroughly tested.

The wiring layer (`controllers.py`) is where the real defects live. Three
BLOCKER-level correctness gaps were found, all in code paths that the current
142-test suite does not exercise:

1. `CurriculumController`'s RECOVER branch calls `checkpoint_store.rollback()`
   but discards the returned state — the model is never actually restored to
   the "last well-formed checkpoint," contradicting both the module's own
   docstring and the `ctl_instruction.md` RECOVER contract.
2. `RunController.run_stage()` only ever polls the ADVANCE/RECOVER/HALT gate
   from inside the L-BFGS phase. A legally-constructible `StageConfig`
   (`n_adam == max_epochs`, explicitly tested as valid in `test_config.py`)
   gives the L-BFGS phase zero budget, so `StageExitMachine.evaluate()` is
   never called and ADVANCE becomes structurally unreachable for that stage.
3. `CurriculumController` holds one fixed `RunController` / `ScheduledWeights`
   / `TrainingConfig` triple across the whole curriculum. Multi-stage
   progression (stage 0 → 1 → 2) is an actively tested capability
   (`PreflightGateTests`), but nothing reconstructs per-stage lambda-max caps
   or per-stage thresholds when the stage index advances, despite the
   `ScheduledWeights` / `RunController` docstrings explicitly claiming this
   happens.

Several secondary WARNING-level gaps compound these: a config field
(`energy_floor_factor`) that is documented as the config-overridable source
for `eps_h`'s scale factor is silently ignored in favor of a hardcoded module
constant; the checkpoint `load_state_dict` round trip (`RunController` /
`GradClipper` / `ScheduledWeights`) has zero test coverage anywhere in the
suite, which is exactly why the rollback-discard bug above went undetected;
and one existing test (`test_recover_branch_catches_empty_checkpoint_store`)
only grep-checks for the string `"except EmptyCheckpointStore"` rather than
asserting the restore actually happens, so it cannot catch the bug it appears
to guard against.

## Critical Issues

### CR-01: RECOVER never restores the model from the rolled-back checkpoint

**File:** `pinn/training/controllers.py:849-865`
**Issue:** `CurriculumController.step()`'s RECOVER branch calls
`self._checkpoint_store.rollback()` purely to detect `EmptyCheckpointStore`;
the returned state (which includes `payload["run_controller"]`, exactly the
dict `RunController.load_state_dict()` expects) is discarded:

```python
if disposition is StageDisposition.RECOVER:
    empty_store = False
    try:
        self._checkpoint_store.rollback()          # <-- return value dropped
    except EmptyCheckpointStore:
        empty_store = True
    ...
    if self._recover_attempts < self._recover_retries:
        self._recover_attempts += 1
        return StageDisposition.RECOVER              # retries WITHOUT restoring state
```

`RunController.load_state_dict()` exists and is fully implemented
(`controllers.py:289-292`) but is never called from `CurriculumController`.
With the ratified default `recover_retries=0` this is masked (RECOVER always
falls straight through to HALT), but for any `recover_retries > 0` — a value
the constructor explicitly accepts and validates
(`controllers.py:717-725`) — a retried stage resumes training from the
*same diverged/NaN-producing parameters* that triggered the RECOVER, not from
"the last well-formed checkpoint" as both this module's docstring
(`controllers.py:681-685`) and `ctl_instruction.md`'s RECOVER contract
("rolls back to the last well-formed checkpoint and retries") require. No
test in `tests/phase40/test_controllers.py` exercises `recover_retries > 0`,
so this gap is currently invisible to the suite.
**Fix:**
```python
if disposition is StageDisposition.RECOVER:
    empty_store = False
    try:
        restored = self._checkpoint_store.rollback()
        if self._run_controller is not None and "run_controller" in restored:
            self._run_controller.load_state_dict(restored["run_controller"])
    except EmptyCheckpointStore:
        empty_store = True
    ...
```

### CR-02: ADVANCE is structurally unreachable when `n_adam == max_epochs`

**File:** `pinn/training/controllers.py:598-640` (`RunController.run_stage`)
**Issue:** `StageExitMachine.evaluate()` — the only place ADVANCE can be
produced — is called exclusively from `_run_lbfgs_phase` (line 580). If the
Adam phase consumes the entire stage budget (`n_adam_k == max_epochs`, or the
plateau detector fires exactly at `max_epochs`), `run_stage()` computes
`remaining_budget = 0` and returns `HALT` directly without ever entering
`_run_lbfgs_phase`:

```python
remaining_budget = max(max_epochs - adam_epochs_used, 0)
if remaining_budget == 0:
    return StageDisposition.HALT       # ADVANCE never evaluated
```

`StageConfig.__post_init__` (`config.py:125-129`) only rejects `n_adam >
max_epochs`; equality is explicitly validated as legal
(`test_config.py::test_n_adam_eq_max_epochs_ok`). So a configuration the
codebase itself certifies as valid guarantees that stage can *never* ADVANCE,
regardless of how well the loss/physics/energy criteria are actually
satisfied during Adam — a silent, undiagnosed dead end that violates this
codebase's own "no silent fallback / no silent deviation" governance
principle. No test constructs this scenario against a real (non-forced)
`RunController`.
**Fix:** Either poll the gate once more on Adam-budget exhaustion before
deciding HALT:
```python
remaining_budget = max(max_epochs - adam_epochs_used, 0)
if remaining_budget == 0:
    outcome = self._stage_exit_machine.evaluate(
        train_loss_history, val_loss_history,
        state["val_phys"], state["val_energy"], False, state["epoch_count"],
    )
    return outcome.disposition if outcome.disposition is not None else StageDisposition.HALT
```
or tighten `StageConfig` validation to require `n_adam < max_epochs` (strict)
so this configuration cannot be constructed at all.

### CR-03: Per-stage `ScheduledWeights` / `TrainingConfig` are never swapped across curriculum stages

**File:** `pinn/training/controllers.py:242-277` (`RunController.__init__`), `pinn/training/controllers.py:699-734` (`CurriculumController.__init__`)
**Issue:** `RunController`'s own docstring states: "at a stage boundary the
RunController resets its per-stage epoch counter to 0 (and, if the new
stage's `lambda^max` differs, constructs a new `ScheduledWeights` for that
stage)" (`scheduled_weights.py:26-31`, echoed at `controllers.py:236-240`).
In the actual implementation, `CurriculumController` is constructed with
exactly one `scheduled_weights` and one `run_controller` for its entire
lifetime; on ADVANCE it only calls `self._scheduled_weights.rewarm()`
(`controllers.py:844`) — it never reconstructs `ScheduledWeights` with the
new stage's `lambda_e_max`/`lambda_l_max`, nor does it swap the injected
`TrainingConfig` (so `n_adam`, `max_epochs`, `beta`, `eps_phys`, `eps_energy`,
etc. also stay pinned to whatever was used for stage 0). Multi-stage
progression through one `CurriculumController` is an actively tested
capability — `PreflightGateTests.test_advancing_into_stage_three_raises_before_run_stage`
drives stages 0→1→2→3 through the same controller — so this is not a
theoretical path. Per the PHYS-05 per-stage table exercised in
`test_scheduled_weights.py::test_lambda_e_le_one_across_schedule_for_each_stage_table`
(stage 0/1: `lambda_e_max=0`; stage 2+: nonzero), a real multi-stage run would
silently keep stage 0's caps and thresholds active for every later stage.
**Fix:** Give `CurriculumController` a way to obtain a stage-specific
`RunController`/`ScheduledWeights` (e.g. a `stage_factory: Callable[[int],
tuple[RunController, ScheduledWeights]]` invoked on stage entry) instead of a
single fixed pair, or document/gate this explicitly as an intentional
Phase-40-stage-0-only limitation if the multi-stage wiring is deliberately
deferred to a later phase — the current code does neither.

## Warnings

### WR-01: `GradClipper.load_state_dict` hardcodes the window's tensor dtype to float64

**File:** `pinn/training/grad_clip.py:288-293`
**Issue:**
```python
def load_state_dict(self, state: dict[str, Any]) -> None:
    ...
    self._window = [torch.tensor(v, dtype=torch.float64) for v in state["window"]]
```
The window's tensors are otherwise whatever dtype `clip_grad_norm_` returns
(the model's working dtype, e.g. `float32` in a non-float64 run). After a
checkpoint restore, every window entry silently becomes `float64` regardless
of the run's actual dtype; the next `clip()` call appends a fresh
`total_norm` in the run's real dtype and calls `torch.stack(self._window)`
over a dtype-mixed list. This is entirely untested: there is no
`state_dict`/`load_state_dict` test anywhere in `test_grad_clip.py`, and
`RunController.load_state_dict()` (which delegates to this method) is never
called by any test in `test_controllers.py` or `test_optimizer_phase.py`.
**Fix:** Preserve dtype through the round trip (e.g. serialize dtype as a
string in `state_dict()` and restore with it), or reuse the dtype of an
existing window entry / the caller's runtime dtype instead of hardcoding
`torch.float64`. Add a dedicated round-trip test that resumes with a
non-float64 runtime and calls `clip()` again afterward.

### WR-02: `energy_floor_factor` config field is documented as config-overridable but is never read

**File:** `pinn/training/controllers.py:230,338`; `pinn/training/config.py:69,110,263-264`
**Issue:** `TrainingConfig.stage.energy_floor_factor` (default `1e-4`) is
registered in the `_PROVISIONAL` table with provenance `"ctl_instruction.md
CURR-03 ε_H=1e-4·S_H (CTX-38)"` and described as "config-overridable...
surfaced for ACC-05 pilot calibration" (`config.py:1-10`) — i.e. it exists
specifically to parametrize the `1e-4` scale factor in `eps_h = 1e-4 * S_H`
(`pinn/loss_catalog.py:264-271` confirms `soft_energy_loss` expects exactly
this upstream-computed scalar). `RunController._build_anchor_context`,
however, computes it from an independent, hardcoded module constant:
```python
_EPS_H_SCALE_FACTOR = 1e-4  # mirrors the documented eps_h = 1e-4 * S_H form
...
eps_h = abs(h0) * _EPS_H_SCALE_FACTOR + 1e-12
```
`self._config.stage.energy_floor_factor` / `self._config.energy_floor` is
never referenced anywhere in `controllers.py`. Overriding
`energy_floor_factor` in a `StageConfig` for ACC-05 calibration has zero
effect on the actual value used in training.
**Fix:** `eps_h = abs(h0) * float(self._config.stage.energy_floor_factor) + 1e-12`, and drop (or repurpose) the now-redundant module constant.

### WR-03: `percentile_10_relaxation` is a required config field with no consumer

**File:** `pinn/training/config.py:99-123`
**Issue:** `StageConfig.percentile_10_relaxation` is CTX-39-"required"
(`ConfigRequiredError` on unset) and range-validated (`[0, 1]`), and
`ctl_instruction.md`'s HALT/REVIEW section names "the percentile-10
relaxation" as one of the provisional knobs governing degraded-advancement
authorization. It is never read anywhere in `stage_exit.py` or
`controllers.py` — grep across the reviewed modules shows zero uses outside
`config.py` and its own tests. A required-and-validated field that nothing
consumes is either dead code or an incomplete wiring gap; either way it is
worth an explicit note (e.g. a comment pointing at the owning future phase)
rather than silently sitting unused.
**Fix:** Either wire it into the relaxation/HALT-authorization path it is
named for, or mark it explicitly as reserved-for-a-later-phase in the
docstring so a reader doesn't assume it currently does something.

### WR-04: `stage_exit.py`'s spec-grounded stagnation-window HALT branch has zero test coverage

**File:** `pinn/training/stage_exit.py:195-213`; `tests/phase40/test_stage_exit.py`
**Issue:** The extra HALT branch —
```python
stag = getattr(cfg, "stagnation_window", None)
if stag is not None and int(stag) > 0 and len(val_loss_history) >= int(stag) and not val_stable:
    window = list(val_loss_history)[-int(stag):]
    running_min = min(val_loss_history)
    if all(v > running_min for v in window):
        return StageExitOutcome(disposition=StageDisposition.HALT, ...)
```
is grounded by `ctl_instruction.md`'s HALT/REVIEW criterion ("...or if
validation loss stagnates above the ADVANCE threshold for the stagnation
window, the loop halts..."), so it is not an invented mechanism. However,
every test in `test_stage_exit.py::HaltAndMidFlightTests` uses histories
shorter than `stagnation_window` (default 50), so `len(val_loss_history) >=
stag` is never true and this branch is never exercised by any test in the
suite — it is currently unverified code in a module explicitly described as
"the SINGLE binding, executable encoding" of a pinned decision machine.
**Fix:** Add a test with `stagnation_window` small (e.g. 5), a
`val_loss_history` that reaches its minimum early and then holds flat above
it for `stagnation_window` further entries, asserting
`disposition == StageDisposition.HALT`; and a companion test where the
window *does* re-touch the running min, asserting the branch does not fire.

### WR-05: Existing "RECOVER" regression test only greps for a string, not behavior

**File:** `tests/phase40/test_controllers.py:224-227`
**Issue:**
```python
def test_recover_branch_catches_empty_checkpoint_store(self):
    CurriculumController = _require("CurriculumController")
    source = inspect.getsource(CurriculumController)
    self.assertIn("except EmptyCheckpointStore", source)
```
This asserts only that the literal text exists in source, not that a
rollback state is actually restored on RECOVER — it cannot detect CR-01
above, and its name ("catches empty checkpoint store") suggests more
behavioral coverage than it provides.
**Fix:** Replace/augment with a behavioral test: seed the checkpoint store
with known model weights, mutate the live model's weights, force a RECOVER
with `recover_retries=1`, and assert the model's weights match the seeded
checkpoint after the retry begins (this test would currently fail and
demonstrate CR-01).

## Info

### IN-01: `RunController.__init__` has an 11-parameter constructor

**File:** `pinn/training/controllers.py:242-256`
**Issue:** `model, train_source, validation_source, config, scheduled_weights,
grad_clipper, collocation_sampler, stage_exit_machine, checkpoint_store,
runtime` (plus keyword-only `rng`) is a long positional parameter list,
typical of dependency-injection style but worth a groupable
collaborators-object if this constructor grows further in Phase 41/42.
**Fix:** Consider bundling the collaborator objects into a small
`RunControllerDeps`/dataclass if additional seams are added later; not
urgent as-is.

### IN-02: `_run_lbfgs_phase` and `_build_anchor_context` mix several responsibilities in one method

**File:** `pinn/training/controllers.py:307-356` (`_build_anchor_context`, ~50 lines), `pinn/training/controllers.py:537-593` (`_run_lbfgs_phase`, ~57 lines)
**Issue:** Both methods exceed ~50 lines and interleave several distinct
concerns (batch/anchor construction, optimizer construction, per-epoch
validation cadence, stage-exit polling, rewarm bookkeeping). Not a
correctness problem today, but a maintainability note for whoever extends
this file in Phase 41/42.
**Fix:** Consider extracting the per-epoch validation-and-gate-check block
into a small helper shared between the (currently gate-less) Adam phase and
the L-BFGS phase, which would also make CR-02 easier to fix cleanly.

---

_Reviewed: 2026-07-17T00:00:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
