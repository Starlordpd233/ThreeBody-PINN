# Phase 48: Loss-Math Conformance - Research

**Researched:** 2026-08-01
**Domain:** PyTorch loss assembly, numerical stability, autograd diagnostics, and durable training telemetry
**Confidence:** HIGH; the float32/MPS causal-floor implementation question is resolved by the existing GAP-45-04 delegation and remains subject to a target-lock backend regression

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

### `L_data` scalar reduction — GAP-45-01 owner ruling

- **D-01 [OWNER-RATIFIED — GAP-45-01, 2026-07-31]:** Use the mean Huber loss
  over time, bodies, and spatial components:
  `mean(Huber(predicted - target), axes=(time, body, component))`. For the
  resident `(N_t, 3, 3)` tensor this is `1/(9*N_t)` times the elementwise Huber
  sum. This is Option A from the original GAP-45-01 decision space.

- **D-02 [GROUNDED EVIDENCE, NOT THE SOURCE OF INTENT]:** Both readings were
  presented at the blocking checkpoint using the four retained Stage-0 traces.
  Per-run mean `L_data` was `0.1539..0.1630`; summing components while averaging
  only over time would have produced `1.3852..1.4673`, exactly 9x larger. The
  retained runs were non-conformant and did not contain per-term gradient
  statistics, so the numbers did not adjudicate intent. They document impact
  only. The owner ratified the recommended per-coordinate convention by
  replying `proceed` after the explicit recommendation and ratification request.

- **D-03 [CONFORMANCE CONSEQUENCE]:** `pinn.loss_catalog.data_huber_loss`
  already computes the D-01 value. CONF-07 therefore preserves its numerical
  reduction, replaces ambiguity/provisional wording with GAP-45-01 provenance,
  and adds or updates focused conformance coverage. Do not introduce a
  multiply-by-9 correction merely to make code move.

- **D-04 [SCOPE-30 / VER-20]:** The framework formula remains textually
  ambiguous. Phase 48 does not edit it. Preserve the explicit-reduction
  amendment as a VER-20 routing item for a later spec-editing milestone.

### Correct `Rbar` before causal weighting

- **D-05 [GROUNDED — CONF-04 / locked loss contract]:** Construct each
  per-time residual energy at the controller assembly seam as
  `(residual ** 2).sum(dim=(-2, -1)) / 3`, exactly
  `(1/3) sum_i ||f_i||^2`. The current mean over the `(3,3)` block divides by
  9 and is exactly one third of the locked value.

- **D-06 [GROUNDED — conformance audit verified-clean boundary]:** Keep
  `causal_physics_loss` as the consumer of an already-assembled one-dimensional
  `Rbar` sequence. Its downstream `(weights * Rbar).mean()` is verified clean.
  Do not compensate through `lambda_phys`, rescale supplied test vectors, or
  duplicate residual construction inside the component function.

- **D-07 [TEST-02]:** Add an assembly-boundary test that intercepts the actual
  `Rbar` passed from `RunController._non_data_terms` to
  `causal_physics_loss`, using a synthetic residual whose divide-by-3 and
  divide-by-9 values differ. Supplying an already-built `Rbar` directly to a
  component unit test is insufficient because that is how C-03 escaped the
  existing suite.

### Causal-exponent clip — invariant A

- **D-08 [IMPLEMENTER-DELEGATED — GAP-45-04 option C]:** Clip the exponent,
  not the residual and not the final physics loss. Given
  `x_n = -eta_c * exclusive_prefix_sum(stopgrad(Rbar))`, use the active torch
  dtype's smallest-normal logarithm as the lower exponent bound:
  `x_clipped = clamp_min(x_n, log(torch.finfo(dtype).tiny))`, then
  `w_n = exp(x_clipped)`. This yields a finite, strictly positive minimum
  normal weight on both supported precision arms and changes the formula only
  in the numerical-underflow regime, as the spec requires.

- **D-09 [NO TUNING]:** The bound is dtype-derived, not fitted to an observed
  run, residual percentile, front position, or validation result. Approximate
  resolved values are `-87.3365` for float32 and `-708.3964` for float64; the
  implementation derives rather than hard-codes them. This choice remains
  valid after CONF-04 makes `Rbar` 3x larger and after Phase 47 removed the
  incoherent-frame residual floor.

- **D-10 [INVARIANTS]:** Preserve `w_1 = 1`, ascending-time validation,
  stop-gradient prefix semantics, and `0 < w_n <= 1` for every finite
  non-negative input. Tests cover both float32 and float64, a prefix large
  enough to have produced exact zero before the fix, and the no-op region where
  the unclipped exponential is already normal and positive.

- **D-11 [RECORDING OBLIGATION]:** Persist the resolved precision, exponent
  lower bound, and resulting minimum causal weight in the run record before
  step 1, and include the same formula/bound in the implementation plan. Reuse
  an established run-record artifact and its atomic/fail-closed pattern; do not
  create a second competing metadata source. Exact field placement and schema
  migration are planner discretion.

- **D-12 [PHASE BOUNDARY]:** This clip closes invariant A only: no causal
  weight may be exactly zero. It must not invent or pre-empt invariant B's
  owner-owned `N`-step front-advance threshold, which remains Phase 49 scope.

### Restore the locked Stage-0 energy weight

- **D-13 [OWNER-RATIFIED — GAP-45-02/03; CONF-06]:** Set the Stage-0 resolved
  configuration and every shipped Stage-0/smoke config to
  `lambda_e_max = 0`. The existing `ScheduledWeights` ramp implementation is
  retained; a zero cap naturally produces zero throughout Stage 0.

- **D-14 [SCOPE CONTROL]:** Do not hard-code zero inside the generic scheduler,
  multiply the energy term by a shadow zero downstream, or redesign the
  per-stage schedule. Later stages require non-zero values under the same
  PHYS-05 table. Phase 49 owns general table enforcement at run start and stage
  boundaries.

- **D-15 [TEST-01]:** Correct the weak test boundary in the same change: retain
  the generic `<= 1` construction guard, but add explicit Stage-0 assertions
  that the resolved configuration and scheduled values are exactly zero at all
  sampled warmup steps. Update existing fixtures/config round-trip expectations
  that encode `1.0` for Stage 0.

### Per-term gradient observability

- **D-16 [INST-02 / Phase-35 logging precondition]:** At each canonical
  completed optimizer-step record, log a global parameter-gradient L2 norm for
  each unweighted term: data, IC, physics, energy, and angular momentum. Keep
  the existing total pre-clip `grad_norm`; it answers a different question.

- **D-17 [INTERPRETABILITY]:** Also log the applied norm for each term, derived
  from the non-negative scalar schedule as
  `grad_norm_applied_term = lambda_term * grad_norm_raw_term`. Raw norms remain
  observable when a scheduled lambda is zero; applied norms state what actually
  entered the optimizer. Together with the already-logged raw losses and lambda
  vector, this is the evidence Phase 35 required before any future reweighting
  decision.

- **D-18 [NO GRADIENT CONTAMINATION]:** Diagnostic per-term gradients must not
  accumulate into parameter `.grad`, change the total backward result, change
  clipping, or retain graphs beyond the step. Parameters unused by a term
  contribute zero to that term's global norm. A completed step must not silently
  substitute a missing statistic with numeric zero.

- **D-19 [CADENCE AND OPTIMIZER SEMANTICS]:** Emit statistics at the same
  canonical per-step event as losses and scheduled weights. Adam statistics
  describe the pre-total-backward graph. L-BFGS statistics follow the existing
  last-closure-evaluation convention already documented for its per-term loss
  breakdown; label that provenance rather than claiming the last closure is
  necessarily the accepted line-search point. Planner research may choose the
  least expensive graph-safe computation that preserves these semantics.

- **D-20 [FAILURE HONESTY]:** Non-finite statistics flow through the existing
  JSONL null/non-finite policy and make the record ineligible as complete
  instrumentation. Guard-tripped/incomplete steps may carry nulls with
  `step_completed = false`; a normal completed step carries all five finite raw
  and applied norms. TensorBoard may mirror these fields, but JSONL remains the
  canonical durable record.

### Test correction and assembly-boundary coverage

- **D-21 [TEST-01]:** Correct a divergence-defending test in the same atomic
  change as its code/config correction. Do not weaken assertions merely to make
  a corrected implementation pass. The Phase 47 CONF-03 change already
  corrected the former per-anchor `eps_H` test; Phase 48 verifies it remains
  correct rather than reopening or duplicating that work.

- **D-22 [TEST-02]:** Treat
  `tests/phase47/test_conf03_eps_h_wiring.py::test_eps_h_assembly_value` as the
  existing `eps_H` assembly-boundary proof. Extend it only if research finds a
  real missing assertion. Add the new `Rbar` interception test from D-07 and
  focused causal-clip, Stage-0 energy-weight, `L_data` reduction, and per-term
  gradient-log tests.

- **D-23 [VERIFIED-CLEAN BOUNDARY]:** Do not re-audit or rewrite force,
  Hamiltonian, IC anchor, angular-momentum, projection, AD, or the downstream
  causal-loss mean. The conformance audit's verified-clean inventory is load-
  bearing.

### Governance and scope locks

- **D-24 [SCOPE-27..32]:** No training run, held-out evaluation, framework-spec
  edit, recipe tuning, automatic dominance reweighting, or trainex-r2 tuning-
  report consultation in Phase 48.

- **D-25 [ORDERING]:** Plan and implement CONF-04 before CONF-05. Phase 47's
  CONF-09 frame completion is already a hard predecessor. Gradient
  instrumentation and tests may be developed in parallel only where their
  assertions do not encode the pre-correction formula.

### the agent's Discretion

The planner may choose helper/module names, phase-scoped test-file organization,
the exact established run-record artifact and schema migration used for D-11,
and the graph-safe implementation used to collect D-16..D-20. Those choices
must preserve every decision above, add no dependency, keep JSONL as the durable
gradient-statistics record, and not introduce a cadence, threshold, tuning
signal, or evaluator path outside this phase.

### Deferred Ideas (OUT OF SCOPE)

- Invariant B's owner-ratified front-advance window `N`, full PHYS-05 table
  enforcement, placeholder census, and known-divergence register — Phase 49.
- Stage-0 training and the three-seed conformant re-run — Phase 50.
- The single authorized held-out evaluation — Phase 51.
- Explicit `L_data` formula amendment and other spec wording fixes — Phase 52
  VER-20 routing to a later spec-editing milestone.
- Recipe tuning, automatic dominance reweighting, and trainex-r2 remedy
  adjudication — v2.3.

### Reviewed Todos (not folded)

- **`d-06-static-epsilon-sensitivity-check`** — a sensitivity study would be
  tuning-shaped work prohibited by SCOPE-29 and is unrelated to the fixed loss-
  math corrections.
- **`trainex-r1-research-handoff`** — research-administration work unrelated to
  Phase 48. The todo match was lexical, not semantic.
</user_constraints>

## Summary

Phase 48 should be planned as a conformance repair across five existing seams, with no new package or parallel loss path: correct `Rbar` where the controller reduces the `(N_t,3,3)` residual; clip the causal exponent inside `causal_physics_loss`; persist the resolved clip facts in the existing strict `training_metadata.json`; resolve Stage-0 energy weight to zero through configuration; and extend the canonical step event with ten raw/applied per-term gradient fields. `data_huber_loss` already performs the owner-ratified all-element mean and needs provenance plus a hand-oracle regression, not a numerical change. [VERIFIED: `.planning/phases/48-loss-math-conformance/48-CONTEXT.md`; VERIFIED: codebase grep]

The safest gradient design is a small graph-local diagnostic helper based on `torch.autograd.grad(..., create_graph=False, retain_graph=True, allow_unused=True, materialize_grads=False)`. It returns gradients without accumulating parameter `.grad`; `None` entries represent parameters unused by that term and contribute zero to the aggregate. Adam can inspect all five live term graphs immediately before the ordinary total backward. L-BFGS must collect diagnostics inside every closure evaluation and overwrite detached floats in `closure_state`, because the closure may be evaluated multiple times and the existing log intentionally reports its last evaluation. [CITED: https://docs.pytorch.org/docs/2.12/generated/torch.autograd.grad.html; CITED: https://docs.pytorch.org/docs/2.12/optim.html; VERIFIED: `pinn/training/controllers.py`]

One literal expression does not survive the production runtime. On the repository `.venv` (`torch 2.12.0`, MPS available), float32 `exp(log(torch.finfo(torch.float32).tiny))` is exactly `0.0` on MPS; moving the representable exponent floor one ULP toward `+inf` gives `1.1754998158862984e-38`, which is positive and above `tiny`. CPU float32 returns a positive subnormal for the literal floor, and CPU float64 remains positive. The parent workflow adjudicated this against the already resolved GAP-45-04 delegation: the owner locked invariant A (`w_n` may never be exactly zero), expressly delegated the implementation bound, and required it to be recorded. D-08 then narrows that delegation to an exponent clip at the active dtype's mathematical `log(finfo.tiny)` bound. Upward-directed rounding to the nearest representable active-dtype value satisfying that lower bound is therefore an authorized implementation detail, not a new semantic default or tuned value. Acceptance still requires a real-MPS torch-2.12.1 regression; do not replace exponent clipping with a final-weight clamp. [VERIFIED: repository runtime probe; VERIFIED: `.planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md` GAP-45-04 resolution; VERIFIED: `.planning/phases/48-loss-math-conformance/48-CONTEXT.md` D-08/D-10]

**Primary recommendation:** Implement the conformance work in the dependency order `Rbar` assembly → upward-rounded dtype clip and metadata → Stage-0 configuration and `L_data` proof → Adam/L-BFGS diagnostics → canonical JSONL and regression gate, with the locked-environment MPS probe as a non-waivable CONF-05 acceptance check. [VERIFIED: `48-CONTEXT.md` D-25; VERIFIED: GAP-45-04 delegation; VERIFIED: repository runtime probe]

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CONF-04 | Correct `Rbar` to `(1/3) Σ_i ||f_i||²`. | The single reduction seam is `RunController._non_data_terms`; use `.sum(dim=(-2,-1)) / 3` and intercept the actual component argument in a dataset-free test. [VERIFIED: `.planning/REQUIREMENTS.md`; VERIFIED: `pinn/training/controllers.py`] |
| CONF-05 | Add causal-exponent clipping that makes every weight nonzero and record its bound. | The exponent seam is centralized in `causal_physics_loss`; `training_metadata.json` is the established pre-step-1 atomic artifact. GAP-45-04 delegates the bound, and D-08 narrows it to the active-dtype mathematical log-tiny exponent floor; upward-directed representable rounding preserves that lower-bound invariant on MPS. [VERIFIED: `.planning/REQUIREMENTS.md`; VERIFIED: `.planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md`; VERIFIED: repository runtime probe; VERIFIED: `pinn/loss_catalog.py`; VERIFIED: `pinn/training/run_metadata.py`] |
| CONF-06 | Restore Stage-0 `lambda_e_max = 0`. | Change `LossConfig`'s resolved default and both shipped Stage-0 YAML files; retain the generic scheduler, whose own default and zero-cap ramp already conform. [VERIFIED: `.planning/REQUIREMENTS.md`; VERIFIED: codebase grep] |
| CONF-07 | Apply the owner-ratified mean `L_data` reduction. | Preserve `data_huber_loss(...).mean()` and prove `sum(Huber)/(9*N_t)` against an independent hand oracle; retain the existing chunk/full gradient-equivalence test. [VERIFIED: `.planning/REQUIREMENTS.md`; VERIFIED: `pinn/loss_catalog.py`; VERIFIED: `tests/phase40/test_optimizer_phase.py`] |
| INST-02 | Log raw per-term gradient statistics. | Add five raw and five applied global L2 norms to the single canonical step event; use graph-local VJPs for Adam and closure-local detached state for L-BFGS. [VERIFIED: `.planning/REQUIREMENTS.md`; CITED: https://docs.pytorch.org/docs/2.12/generated/torch.autograd.grad.html; VERIFIED: `pinn/training/controllers.py`] |
| TEST-01 | Correct tests that defend divergent behavior in the same change. | Update config defaults, YAML expectations, fixtures, and Stage-0 schedule assertions atomically with CONF-06; do not weaken generic cap tests. [VERIFIED: `.planning/REQUIREMENTS.md`; VERIFIED: codebase grep] |
| TEST-02 | Prove `Rbar` and `eps_H` at the assembly boundary. | Add the new `Rbar` interception test and preserve the already-passing Phase-47 `test_eps_h_assembly_value`; no duplicate `eps_H` proof is needed. [VERIFIED: `.planning/REQUIREMENTS.md`; VERIFIED: `tests/phase47/test_conf03_eps_h_wiring.py`] |
</phase_requirements>

## Project Constraints (from AGENTS.md)

- Work only in the milestone worktree that owns the phase; this research verified branch `milestone/v2.2` in `.worktrees/trainex`. Existing modified and untracked files are user-owned and must remain untouched. [VERIFIED: `AGENTS.md`; VERIFIED: `git status --short --branch`; VERIFIED: `git worktree list --porcelain`]
- Use Sequentialthinking for multi-step work. It was used for this research. [VERIFIED: `AGENTS.md`; VERIFIED: research tool trace]
- For adjudication work, do not invent source-silent semantic decisions. Subagents surface findings to the parent and do not write gap registers. The parent checked the float32/MPS finding against GAP-45-04 and D-08/D-10: the bound is already implementer-delegated, while strict positivity is owner-locked, so no new STOP gap is opened. [VERIFIED: `AGENTS.md` STOP protocol; VERIFIED: `.planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md`]
- `ctl_instruction.md` and `pinn_architecture.md` are authoritative framework specs; Phase 48 may read but must not edit them. The v1.3 `pinn/` implementation is not a grounding source for spec intent, though the live Phase-48 code is the implementation target audited for conformance. [VERIFIED: `AGENTS.md`; VERIFIED: `48-CONTEXT.md` D-24]
- Do not consult `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/`; no source in this research came from that directory. [VERIFIED: `.planning/REQUIREMENTS.md` SCOPE-31; VERIFIED: research access log]
- Do not run training, access held-out evaluation data, tune weights, add automatic reweighting, or edit framework specs in this phase. [VERIFIED: `.planning/REQUIREMENTS.md` SCOPE-27..31; VERIFIED: `48-CONTEXT.md` D-24]
- If the research artifact is committed, use `scripts/agent-commit` with explicit `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS`, stage only this owned path, inspect staged/unstaged diffs, run relevant verification and `git diff --check`, and use a policy-conforming `docs(48): ...` message with the required body/trailer. [VERIFIED: `AGENTS.md` Git Commit Protocol]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Residual-to-`Rbar` reduction | API / Backend (training controller) | — | The controller owns construction of component input; the loss catalog intentionally consumes an already-built 1D sequence. [VERIFIED: `pinn/training/controllers.py`; VERIFIED: `48-CONTEXT.md` D-05/D-06] |
| Causal exponent stability | API / Backend (loss catalog) | Runtime backend (CPU/MPS) | The loss component owns exponent construction, while representable `exp` behavior is device/dtype dependent. [VERIFIED: `pinn/loss_catalog.py`; VERIFIED: repository runtime probe] |
| Clip provenance | Database / Storage (run artifact) | API / Backend (run setup) | Run setup resolves the active dtype/device and writes the strict artifact before step 1; the loader revalidates it on resume. [VERIFIED: `pinn/train.py`; VERIFIED: `pinn/training/run_metadata.py`] |
| Stage-0 energy cap | API / Backend (configuration) | API / Backend (scheduler) | The resolved config supplies the cap and the generic scheduler applies its existing ramp without Stage-specific branching. [VERIFIED: `pinn/training/config.py`; VERIFIED: `pinn/training/scheduled_weights.py`] |
| `L_data` scalar reduction | API / Backend (loss catalog) | API / Backend (L-BFGS chunk accumulator) | The catalog defines the all-element mean; the chunk path preserves it by weighting chunks by sample count. [VERIFIED: `pinn/loss_catalog.py`; VERIFIED: `pinn/training/controllers.py`] |
| Per-term gradient norms | API / Backend (optimizer controller) | Runtime backend (autograd) | Only the controller has all live term graphs, parameters, current weights, optimizer ordering, and closure semantics. [VERIFIED: `pinn/training/controllers.py`; CITED: https://docs.pytorch.org/docs/2.12/generated/torch.autograd.grad.html] |
| Durable gradient evidence | Database / Storage (JSONL) | Monitoring (TensorBoard, optional) | The JSONL handler filters to its field registry and is canonical; TensorBoard is explicitly secondary. [VERIFIED: `pinn/training/step_log.py`; VERIFIED: `pinn/training/tb_sink.py`; VERIFIED: `48-CONTEXT.md` D-20] |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.12.13 in repository `.venv` | Trainer, test runner, metadata validation | This is the restored repository runtime documented by the project and available in the current worktree. [VERIFIED: `.venv/bin/python --version`; VERIFIED: `docs/GETTING-STARTED.md`] |
| PyTorch | 2.12.1 target lock; 2.12.0 in repository `.venv` | Tensor math, MPS execution, autograd, Adam, L-BFGS | It is the existing trainer framework. The patch-version mismatch is material to the MPS clip and must be included in validation, not resolved by adding another framework. [VERIFIED: `requirements-lock.txt`; VERIFIED: `.venv` runtime probe] |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pytest | 9.1.1 in repository `.venv` | Phase-scoped tests, fixtures, monkeypatching, subtests | Use for all Phase-48 validation and impacted existing tests. [VERIFIED: `.venv` runtime probe; VERIFIED: existing test imports] |
| PyYAML | 6.0.3 in repository `.venv` | Strict configuration round trips | Use only through the existing config loader and existing tests. [VERIFIED: `.venv` runtime probe; VERIFIED: `pinn/training/config_yaml.py`] |
| Python `json` + existing atomic writer | standard library | Strict metadata and canonical JSONL | Reuse `training_metadata.json`, `_sanitize_step_record`, and `atomic_write_text`; no sidecar or serializer is needed. [VERIFIED: `pinn/training/run_metadata.py`; VERIFIED: `pinn/training/step_log.py`] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `torch.autograd.grad` diagnostics | Repeated `.backward()` | Repeated backward would accumulate into `.grad` unless carefully cleared and would violate D-18; do not use it. [CITED: https://docs.pytorch.org/docs/2.12/generated/torch.autograd.grad.html; VERIFIED: `48-CONTEXT.md` D-18] |
| Exponent clipping | Clamp the final `w_n` | Final-weight clamping is explicitly rejected by D-08 and hides backend behavior at the wrong seam. [VERIFIED: `48-CONTEXT.md` D-08] |
| Extend `training_metadata.json` | Create a new clip sidecar | A sidecar would create a competing source and violate D-11. [VERIFIED: `48-CONTEXT.md` D-11] |
| Resolve Stage-0 zero in config | Hard-code zero in scheduler or total loss | That breaks the reusable PHYS-05 schedule and later-stage behavior. [VERIFIED: `48-CONTEXT.md` D-13/D-14] |

**Installation:**

```bash
# No installation: Phase 48 adds no dependency.
```

**Version verification:** The repository `.venv` reports Python 3.12.13, torch 2.12.0, pytest 9.1.1, PyYAML 6.0.3, and NumPy 2.2.0; `requirements-lock.txt` targets torch 2.12.1. Re-run the clip probe under the exact target lock before accepting CONF-05. [VERIFIED: `.venv` runtime probe; VERIFIED: `requirements-lock.txt`]

## Package Legitimacy Audit

Not applicable: the phase installs no external package, so the Package Legitimacy Gate is not triggered. [VERIFIED: `48-CONTEXT.md` Agent's Discretion]

## Architecture Patterns

### System Architecture Diagram

```text
Stage-0 YAML / runtime dtype+device
              |
              +----> run setup ----> strict training_metadata.json
              |          |             (atomic write, fail-closed reload)
              |          v
data + IC ----+----> RunController
                         |
model outputs ------------+
                         |
                         +--> residual (Nt,3,3)
                         |       |
                         |       v
                         |   Rbar = sum(residual^2)/3
                         |       |
                         |       v
                         |   exclusive detached prefix
                         |       |
                         |       v
                         |   exponent floor --> exp --> causal L_phys
                         |
                         +--> five unweighted live term graphs
                         |       |
                         |       +--> graph-safe raw norms
                         |       +--> lambda * raw = applied norms
                         |       +--> weighted total.backward()
                         |
                         +--> optimizer step
                                 |
                                 v
                       one canonical step event
                          /                \
                         v                  v
                JSONL registry/sanitizer   TensorBoard (optional mirror)
                  |              |
         all 10 finite       missing/nonfinite
                  |              |
       step_completed=true   null + incomplete record
```

Every arrow above corresponds to an existing production seam; Phase 48 extends those seams rather than introducing a parallel loss, metadata, or logging subsystem. [VERIFIED: codebase grep; VERIFIED: `48-CONTEXT.md`]

### Recommended Project Structure

```text
pinn/
├── loss_catalog.py                 # L_data provenance + causal floor helper/use
├── train.py                        # bind live clip facts into pre-step metadata
└── training/
    ├── controllers.py              # Rbar fix; Adam/L-BFGS diagnostics; one log event
    ├── config.py                   # Stage-0 lambda_e_max resolved default
    ├── run_metadata.py             # strict schema extension and revalidation
    ├── scheduled_weights.py        # retained unchanged except documentation/tests if needed
    └── step_log.py                 # ten canonical JSONL fields + failure honesty
configs/
├── smoke.yaml                      # Stage-0 lambda_e_max: 0
└── stage0-example.yaml             # Stage-0 lambda_e_max: 0
tests/phase48/
├── __init__.py                     # package marker
├── test_loss_math_conformance.py   # Rbar interception, clip, L_data oracle
├── test_stage0_energy_config.py    # config/YAML-to-scheduler exact-zero proof
├── test_clip_metadata.py           # strict causal-floor metadata lifecycle
└── test_gradient_observability.py  # Adam/L-BFGS norms and JSONL honesty
```

The exact Phase-48 test filenames are planner discretion; production ownership should remain in the existing modules shown. [VERIFIED: `48-CONTEXT.md` Agent's Discretion; VERIFIED: codebase layout]

### Pattern 1: Correct the producer seam, not the verified consumer

**What:** Reduce the physical residual exactly once in `_non_data_terms`, then pass the one-dimensional result to the unchanged causal component. [VERIFIED: `48-CONTEXT.md` D-05/D-06]

**When to use:** Apply to CONF-04 and protect it with an interception test at the controller-to-loss call boundary. [VERIFIED: `48-CONTEXT.md` D-07]

**Example:**

```python
# Source: 48-CONTEXT.md D-05 and pinn/training/controllers.py
residual = accel - force
rbar = (residual ** 2).sum(dim=(-2, -1)) / 3
phys_term = causal_physics_loss(rbar, times=times_tensor, ...)
```

### Pattern 2: Inspect gradients without mutating optimizer state

**What:** Compute a global norm from the VJPs returned by `torch.autograd.grad`, discard those tensors after converting the norm to a detached scalar, and let the ordinary total backward own `.grad`. [CITED: https://docs.pytorch.org/docs/2.12/generated/torch.autograd.grad.html]

**When to use:** Adam's five live terms before total backward and the four live non-data terms inside each L-BFGS closure. The L-BFGS data norm can read the already-accumulated data-only `.grad` immediately after chunked data backward because `LossWeights.lambda_data` is structurally fixed to `1.0`; reading it adds no diagnostic gradient. [VERIFIED: `pinn/loss_catalog.py`; VERIFIED: `pinn/training/controllers.py`]

### Pattern 3: Persist resolved numerical facts in the established artifact

**What:** Centralize dtype floor derivation in one helper used by both the loss and run setup; persist precision, resolved exponent bound, minimum weight, and a formula identifier in `training_metadata.json`; bump its strict schema and rederive/revalidate on resume. [VERIFIED: `48-CONTEXT.md` D-11; VERIFIED: `pinn/training/run_metadata.py`]

**When to use:** Fresh run setup after runtime resolution and before step 1. A pre-Phase-48 schema cannot prove clip conformance and should fail closed on resume rather than be silently upgraded. [VERIFIED: `pinn/train.py`; VERIFIED: `pinn/training/run_metadata.py`; VERIFIED: planner-discretion analysis]

### Pattern 4: One explicit step-local telemetry carrier

**What:** Pass a detached gradient-statistics mapping explicitly to `_log_step`, add every key to `STEP_LOG_FIELDS`, and derive record completeness from presence and finiteness of all ten fields. [VERIFIED: `pinn/training/controllers.py`; VERIFIED: `pinn/training/step_log.py`; VERIFIED: `48-CONTEXT.md` D-18/D-20]

**When to use:** Both Adam and L-BFGS. Do not use `_last_widened_details` for gradient statistics: validation occurs before normal logging and can overwrite that shared stash with validation values. [VERIFIED: `pinn/training/controllers.py`]

### Anti-Patterns to Avoid

- **Literal float32 floor accepted from CPU-only tests:** CPU returns a subnormal while MPS returns zero; require the production MPS arm. [VERIFIED: repository runtime probe]
- **Per-chunk root-sum-square for L-BFGS data:** Norms do not add across chunks because gradient vectors can cancel; the global norm must be taken after vector accumulation. Reading the final data-only `.grad` is exact under the fixed unit data weight. [VERIFIED: first-principles linear algebra; VERIFIED: `LossWeights.lambda_data`]
- **Gradient telemetry in `_last_widened_details`:** A validation call can overwrite the training closure's stash before logging. Use step-local or closure-local state. [VERIFIED: `pinn/training/controllers.py`]
- **Missing fields treated as zero:** An unused parameter contributes zero inside a legitimate term norm, but a missing whole statistic remains `None` and makes the record incomplete. [VERIFIED: `48-CONTEXT.md` D-18/D-20]
- **Adding log keys only to `_log_step`:** `JsonlStepHandler` serializes only registry keys, so unregistered telemetry is silently discarded. [VERIFIED: `pinn/training/step_log.py`]
- **Reopening verified-clean component math:** Force, Hamiltonian, anchors, projection, AD, angular momentum, and the downstream causal mean are out of bounds. [VERIFIED: `48-CONTEXT.md` D-23]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Per-term reverse-mode differentiation | Manual parameter hooks or finite differences | `torch.autograd.grad` | It provides graph-local VJPs without accumulating `.grad` and already handles the active backend. [CITED: https://docs.pytorch.org/docs/2.12/generated/torch.autograd.grad.html] |
| Non-finite JSON encoding | A second sanitizer or string sentinels | `_sanitize_step_record` | The existing policy emits JSON `null`, `finite:false`, and `nonfinite_keys` with `allow_nan=False`. [VERIFIED: `pinn/training/step_log.py`] |
| Crash-safe metadata | Direct `open().write()` or a second sidecar | `atomic_write_text` + strict loader | The existing artifact is atomic and fail-closed, and D-11 prohibits a competing source. [VERIFIED: `pinn/training/run_metadata.py`; VERIFIED: `48-CONTEXT.md` D-11] |
| Stage-specific ramp logic | A new Stage-0 scheduler | Existing `ScheduledWeights` | A zero cap already yields zero at every warmup point while retaining later-stage generality. [VERIFIED: `pinn/training/scheduled_weights.py`] |
| Duplicate `eps_H` proof | A new parallel assembly harness | Existing Phase-47 assembly test | D-22 names the existing test as sufficient unless a concrete assertion gap appears; none was found. [VERIFIED: `48-CONTEXT.md` D-22; VERIFIED: targeted test run] |

**Key insight:** Nearly every Phase-48 defect escaped because the component-level code or tests were locally reasonable while the assembly, runtime backend, or logging boundary changed the meaning. The plan should protect boundaries and provenance, not add alternative implementations. [VERIFIED: conformance audit; VERIFIED: code/test audit]

## Common Pitfalls

### Pitfall 1: `log(tiny)` rounds the wrong way on float32 MPS

**What goes wrong:** The literal lower bound exponentiates to exact zero on MPS, violating invariant A, even though the same value appears positive in a CPU-only test. [VERIFIED: repository runtime probe]

**Why it happens:** The nearest float32 representation of the mathematical logarithm is slightly more negative; CPU emits a subnormal, while MPS flushes this result to zero. One representable step toward `+inf` yielded a value above the minimum normal in the tested runtime. [VERIFIED: repository runtime probe; CITED: https://docs.pytorch.org/docs/2.12/type_info.html]

**How to avoid:** Apply the resolved GAP-45-04/D-08 delegation, derive the upward-rounded bound rather than hard-code it, and test `0 < w <= 1` on real MPS under the target torch 2.12.1 lock as well as CPU float32/float64. [VERIFIED: `.planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md`; VERIFIED: `48-CONTEXT.md` D-09/D-10; VERIFIED: `requirements-lock.txt`]

**Warning signs:** `w_min == 0`, a CPU result smaller than `torch.finfo(dtype).tiny`, or a test that never exercises `device="mps"`. [VERIFIED: repository runtime probe]

### Pitfall 2: Testing the causal component while missing bad assembly

**What goes wrong:** A unit test supplies a correct `Rbar` directly, so it passes while the controller still divides residual energy by nine. [VERIFIED: `tests/phase38/test_loss_catalog.py`; VERIFIED: `pinn/training/controllers.py`]

**Why it happens:** The component and its tests start downstream of the defective reduction seam. [VERIFIED: conformance audit C-03]

**How to avoid:** Intercept the actual value passed by `_non_data_terms`, using an all-ones `(N_t,3,3)` residual for which the locked value is `3` and the divergent mean is `1`. [VERIFIED: first-principles arithmetic; VERIFIED: `48-CONTEXT.md` D-07]

**Warning signs:** A new test calls `causal_physics_loss(rbar, ...)` directly and never constructs a controller residual. [VERIFIED: code/test audit]

### Pitfall 3: Diagnostic gradients contaminate `.grad` or clipping

**What goes wrong:** Repeated diagnostic `.backward()` calls alter the total optimizer gradient, clipping outcome, or guard behavior. [VERIFIED: first-principles autograd semantics; VERIFIED: `48-CONTEXT.md` D-18]

**Why it happens:** `.backward()` accumulates leaf gradients by default, while the requirement is observational. [CITED: https://docs.pytorch.org/docs/2.12/generated/torch.Tensor.backward.html]

**How to avoid:** Use `autograd.grad`, snapshot actual `.grad` before/after in tests, compare optimizer updates with diagnostics enabled/disabled, and never store live graph tensors in log or closure state. [CITED: https://docs.pytorch.org/docs/2.12/generated/torch.autograd.grad.html; VERIFIED: `48-CONTEXT.md` D-18]

**Warning signs:** `.grad` becomes non-`None` before total backward in Adam, `retain_graph` tensors are stored on the controller, or clipping tests change after telemetry is enabled. [VERIFIED: code-path analysis]

### Pitfall 4: Claiming an L-BFGS accepted-point diagnostic

**What goes wrong:** A log labels the last closure's terms or norms as the accepted line-search point, or computes diagnostics only on the first closure. [VERIFIED: `pinn/training/controllers.py`; CITED: https://docs.pytorch.org/docs/2.12/optim.html]

**Why it happens:** L-BFGS may reevaluate its closure multiple times, and there is no prospective “this is the last closure” flag. [CITED: https://docs.pytorch.org/docs/2.12/generated/torch.optim.LBFGS.html; CITED: https://docs.pytorch.org/docs/2.12/optim.html]

**How to avoid:** Compute closure-local diagnostics on every invocation, overwrite detached `closure_state` values, and emit explicit `last_closure_evaluation` provenance. [VERIFIED: `48-CONTEXT.md` D-19; VERIFIED: code-path analysis]

**Warning signs:** Diagnostics run after `optimizer.step(closure)` from detached loss carriers, or a test assumes exactly one closure call. [VERIFIED: `pinn/training/controllers.py`]

### Pitfall 5: Stale validation data leaks into a training step

**What goes wrong:** Gradient or loss details stored in `_last_widened_details` are overwritten by validation before the completed step is logged. [VERIFIED: `pinn/training/controllers.py` ordering]

**Why it happens:** The normal Adam and L-BFGS paths can run validation before `_log_step`, while `_non_data_terms` writes the shared stash. [VERIFIED: `pinn/training/controllers.py`]

**How to avoid:** Carry gradient stats explicitly in a step-local mapping; keep L-BFGS values in detached closure state and pass the frozen weights to every L-BFGS log call. [VERIFIED: code-path analysis]

**Warning signs:** `validation_every=1` changes training-step telemetry, or L-BFGS lambda fields remain JSON null. [VERIFIED: code-path analysis]

### Pitfall 6: Canonical JSONL silently drops or misclassifies fields

**What goes wrong:** A field emitted by `_log_step` is absent from disk because it was not registered; alternatively, `None` serializes as null while `finite:true`, making missing instrumentation look complete. [VERIFIED: `pinn/training/step_log.py`]

**Why it happens:** `JsonlStepHandler` filters strictly through `STEP_LOG_FIELDS`, and `_sanitize_step_record` marks numeric NaN/Inf but does not classify `None` as non-finite. [VERIFIED: `pinn/training/step_log.py`]

**How to avoid:** Register all ten fields, explicitly derive `step_completed` from their presence and finiteness, preserve the sanitizer for actual non-finite numbers, and add JSONL parity tests for Adam and L-BFGS. [VERIFIED: `48-CONTEXT.md` D-18/D-20; VERIFIED: code-path analysis]

**Warning signs:** A normal record has `step_completed:true` with any gradient field null, or new fields appear in the logger `extra` dict but not `STEP_LOG_FIELDS`. [VERIFIED: `48-CONTEXT.md` D-20; VERIFIED: `pinn/training/step_log.py`]

### Pitfall 7: Schema extension is written but not revalidated

**What goes wrong:** Fresh runs record clip facts, but resumes accept a different dtype/bound or an old schema that cannot prove conformance. [VERIFIED: D-11 obligation and current strict loader analysis]

**Why it happens:** `training_metadata.json` currently enforces an exact schema-v1 key set; adding fields at only the writer or only the loader breaks the round trip. [VERIFIED: `pinn/training/run_metadata.py`]

**How to avoid:** Bump the schema, update writer/loader/setup/tests together, recompute expected clip facts from the live runtime, and fail closed on mismatch before step 1. [VERIFIED: established Phase-47 metadata pattern]

**Warning signs:** Unknown keys are ignored, old metadata is silently mutated, or the recorded precision is derived from config text rather than the resolved runtime dtype. [VERIFIED: `pinn/training/run_metadata.py`; VERIFIED: `pinn/train.py`]

### Pitfall 8: Only the scheduler default changes

**What goes wrong:** Stage-0 still resolves `lambda_e_max=1.0` from `LossConfig`, `configs/smoke.yaml`, or `configs/stage0-example.yaml`. [VERIFIED: codebase grep]

**Why it happens:** The generic scheduler already defaults to zero, but upstream resolved configuration overrides it. [VERIFIED: `pinn/training/config.py`; VERIFIED: `pinn/training/scheduled_weights.py`; VERIFIED: shipped YAML]

**How to avoid:** Change every Stage-0 resolution source and update round-trip fixtures while retaining generic nonzero cap tests. [VERIFIED: `48-CONTEXT.md` D-13/D-15]

**Warning signs:** Any shipped Stage-0 YAML or default `LossConfig()` still reports `1.0`. [VERIFIED: `48-CONTEXT.md` D-13]

## Code Examples

Verified patterns from official sources and repository seams follow.

### Global raw norm without `.grad` accumulation

```python
# Source: https://docs.pytorch.org/docs/2.12/generated/torch.autograd.grad.html
def raw_global_grad_norm(term, params):
    grads = torch.autograd.grad(
        term,
        params,
        retain_graph=True,       # ordinary total backward still follows
        create_graph=False,
        allow_unused=True,
        materialize_grads=False,
    )
    squared = term.new_zeros(())
    for grad in grads:
        if grad is not None:     # unused parameter contributes zero
            squared = squared + grad.detach().square().sum()
    return float(torch.sqrt(squared).detach())
```

The helper must receive a fixed tuple of trainable parameters, return a detached scalar, and let computation errors propagate rather than substitute zero. [VERIFIED: `48-CONTEXT.md` D-18]

### Raw and applied mapping

```python
# Source: 48-CONTEXT.md D-16/D-17; LossWeights enforces non-negative lambdas.
raw = {
    "data": raw_global_grad_norm(terms.data, params),
    "ic": raw_global_grad_norm(terms.ic, params),
    "phys": raw_global_grad_norm(terms.phys, params),
    "energy": raw_global_grad_norm(terms.energy, params),
    "angmom": raw_global_grad_norm(terms.angmom, params),
}
applied = {
    name: getattr(weights, weight_field[name]) * value
    for name, value in raw.items()
}
```

This keeps a zero-weight energy term observable as a nonzero raw norm with an applied norm of exactly zero. [VERIFIED: `48-CONTEXT.md` D-17; VERIFIED: `pinn/loss_catalog.py`]

### Resolved directed-up exponent floor

```python
# Source: GAP-45-04 implementer delegation + D-08/D-10 + repository MPS probe.
# The nearest active-dtype value that is not below the mathematical bound is
# the authorized representable implementation; it is derived, not tuned.
target = math.log(torch.finfo(dtype).tiny)
floor = torch.tensor(target, dtype=dtype, device=device)
if float(floor.detach().cpu()) < target:
    floor = torch.nextafter(
        floor,
        torch.tensor(math.inf, dtype=dtype, device=device),
    )
x_clipped = torch.clamp_min(x, floor)
w_n = torch.exp(x_clipped)
```

The comparison implements upward-directed representable rounding instead of a tuned constant. Its acceptance still requires the real-MPS test under the target lock because backend exponential behavior is the failure surface. [VERIFIED: repository runtime probe; CITED: https://docs.pytorch.org/docs/2.12/type_info.html]

### Honest canonical-record completeness

```python
# Source: 48-CONTEXT.md D-18/D-20 and pinn/training/step_log.py.
all_stats = [*raw.values(), *applied.values()]
instrumentation_complete = (
    len(all_stats) == 10
    and all(value is not None and math.isfinite(value) for value in all_stats)
)
resolved_step_completed = bool(step_completed and instrumentation_complete)
```

Keep original non-finite values in the emitted numeric fields so `_sanitize_step_record` can turn them into JSON null and name them in `nonfinite_keys`; only the completeness flag is derived before emission. [VERIFIED: `pinn/training/step_log.py`; VERIFIED: `48-CONTEXT.md` D-20]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Component-only causal-loss tests | Assembly-boundary interception of the producer's actual `Rbar` | Phase 48 locked TEST-02 | Protects the reduction seam where C-03 escaped. [VERIFIED: `48-CONTEXT.md` D-07] |
| Literal unbounded `exp(-prefix)` | Dtype-derived exponent floor with production-backend proof | Phase 48 CONF-05 | Prevents exact-zero causal weights without tuning residuals or loss weights. [VERIFIED: `.planning/REQUIREMENTS.md`; blocker caveat documented above] |
| Total pre-clip norm only | Five raw plus five schedule-applied term norms alongside total norm | Phase 48 INST-02 | Provides the Phase-35 evidence prerequisite without creating a control loop. [VERIFIED: `48-CONTEXT.md` D-16/D-17] |
| Detached last-closure loss breakdown | Detached last-closure loss plus explicitly labeled gradient breakdown | Existing convention extended in Phase 48 | Preserves honest L-BFGS provenance instead of claiming an accepted line-search point. [VERIFIED: `pinn/training/controllers.py`; VERIFIED: `48-CONTEXT.md` D-19] |
| Informal runtime reconstruction | Strict pre-step metadata for numerical constants | Phase 47 pattern extended in Phase 48 | Makes the dtype and actual clip facts re-derivable and resume-checkable. [VERIFIED: `pinn/training/run_metadata.py`; VERIFIED: `48-CONTEXT.md` D-11] |

**Deprecated/outdated:**

- The `causal_physics_loss` documentation that calls underflow-to-zero correct is stale and must be replaced with the invariant-A provenance. [VERIFIED: `pinn/loss_catalog.py`; VERIFIED: `48-CONTEXT.md` D-08/D-10]
- Stage-0 `lambda_e_max: 1.0` in the resolved default and shipped YAML is owner-classified drift. [VERIFIED: `48-CONTEXT.md` D-13; VERIFIED: codebase grep]
- Any provisional wording around the existing all-element `L_data` mean is superseded by GAP-45-01's owner ruling. [VERIFIED: `48-CONTEXT.md` D-01/D-03]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| — | None. The MPS finding is resolved by the existing GAP-45-04 implementer delegation plus D-08/D-10; exact metadata placement remains planner discretion under D-11. | — | — |

All other claims in this research were verified from canonical project sources, live code/tests, the repository runtimes, or cited official PyTorch documentation. [VERIFIED: research source log]

## Resolved Research Question

1. **Does D-08 authorize upward-directed representable rounding of `log(tiny)` on float32 MPS? — RESOLVED: YES**
   - What we know: In the repository `.venv` with torch 2.12.0 and MPS available, `torch.exp(torch.log(torch.tensor(torch.finfo(torch.float32).tiny, device="mps")))` returns `0.0`; its exponent is `-87.3365478515625`. `torch.nextafter(bound, +inf)` yields `-87.33654022216797`, and MPS `exp` then yields `1.1754998158862984e-38`, above `tiny=1.1754943508222875e-38`. CPU float32 returns `1.1754907074462803e-38`, a positive subnormal, for the literal bound; CPU float64 remains positive. [VERIFIED: repository runtime probe]
   - Reproduction command: `.venv/bin/python -c 'import torch; d=torch.float32; z=torch.tensor(torch.finfo(d).tiny,dtype=d,device="mps"); b=torch.log(z); u=torch.nextafter(b,torch.tensor(float("inf"),dtype=d,device="mps")); print(torch.finfo(d).tiny,b.item(),torch.exp(b).item(),u.item(),torch.exp(u).item())'`. [VERIFIED: repository runtime probe]
   - Resolution: GAP-45-04 already makes invariant A self-executing, delegates the clip bound to the implementer, and requires the selected bound to be recorded. D-08 narrows that discretion to exponent clipping at the active dtype's mathematical `log(finfo.tiny)` lower bound. The nearest active-dtype representation that is not below that mathematical bound is upward-directed rounding; advancing one ULP only when nearest rounding falls below the target introduces neither a tuned constant nor a user-selectable setting. [VERIFIED: `.planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md` GAP-45-04; VERIFIED: `48-CONTEXT.md` D-08/D-10]
   - Required backstop: Repeat the strict `0 < w_n <= 1` former-underflow probe on a real MPS device under locked torch 2.12.1. A CPU-only or mocked-device result is insufficient. [VERIFIED: repository runtime probe; VERIFIED: `requirements-lock.txt`]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Repository `.venv` Python | Tests and MPS reproduction | ✓ | Python 3.12.13 | — [VERIFIED: runtime probe] |
| PyTorch in `.venv` | Unit tests and MPS probe | ✓ | 2.12.0 | Re-run final backend proof in locked `pinn-train` torch 2.12.1. [VERIFIED: runtime probe; VERIFIED: `requirements-lock.txt`] |
| pytest in `.venv` | Phase-scoped validation | ✓ | 9.1.1 | — [VERIFIED: runtime probe] |
| `pinn-train` conda environment | Locked trainer dependency arm | ✓ | Python 3.11.15, torch 2.12.1 | Use `.venv` for pytest; `pinn-train` currently lacks pytest but can run a dependency-free MPS probe. [VERIFIED: conda runtime probe] |
| MPS backend | Production float32 invariant-A proof | ✓ | built and available in both probed torch environments | CPU-only tests are insufficient. [VERIFIED: runtime probe] |
| System Python | None; must not be used | ✗ for torch | Python 3.14.6, torch absent | Use repository `.venv`. [VERIFIED: runtime probe] |
| Dataset / held-out evaluator | Not required by Phase 48 | Not accessed | — | Synthetic fixtures only. [VERIFIED: `48-CONTEXT.md` D-24] |

**Missing dependencies with no fallback:** None. [VERIFIED: environment audit]

**Missing dependencies with fallback:** `pytest` is absent from `pinn-train`; use the repository `.venv` for the test suite and the locked environment for a standalone target-version MPS probe. [VERIFIED: environment audit]

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 9.1.1 over existing unittest- and pytest-style modules [VERIFIED: `.venv` runtime probe; VERIFIED: test tree] |
| Config file | None found; run from repository root with explicit paths and `-q`. [VERIFIED: codebase scan] |
| Quick run command | `.venv/bin/python -m pytest -q tests/phase48` [VERIFIED: project runtime convention] |
| Full impacted suite command | `.venv/bin/python -m pytest -q tests/phase38 tests/phase40 tests/phase41 tests/phase42 tests/phase46 tests/phase47 tests/phase48` [VERIFIED: code ownership/test map] |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CONF-04 | Controller passes `(residual²).sum((-2,-1))/3`, not `/9` | assembly unit | `.venv/bin/python -m pytest -q tests/phase48/test_loss_math_conformance.py -k rbar_assembly` | ❌ Wave 0 |
| CONF-05 | Float32/float64 weights stay in `(0,1]`, preserve `w1`, stopgrad, sorting, and no-op region; real MPS underflow arm passes | unit + backend integration | `.venv/bin/python -m pytest -q tests/phase48/test_loss_math_conformance.py -k causal_clip` | ❌ Wave 0 |
| CONF-06 | Resolved default and shipped Stage-0 configs produce energy cap/value zero throughout sampled warmup | config + unit | `.venv/bin/python -m pytest -q tests/phase48/test_stage0_energy_config.py -k lambda_e` | ❌ Wave 0 |
| CONF-07 | `L_data == sum(elementwise Huber)/(9*N_t)` across both Huber branches; chunk/full gradient equivalence remains | unit | `.venv/bin/python -m pytest -q tests/phase48/test_loss_math_conformance.py tests/phase40/test_optimizer_phase.py -k 'data_huber or chunked_accumulation'` | ❌ Wave 0 + ✅ existing chunk proof |
| INST-02 | Adam and L-BFGS emit five finite raw and five applied norms without changing `.grad`, clipping, or updates; lambda-zero and unused-parameter cases are distinguished | unit + controller integration | `.venv/bin/python -m pytest -q tests/phase48/test_gradient_observability.py` | ❌ Wave 0 |
| TEST-01 | Divergence-defending config/fixture expectations are corrected atomically | regression | `.venv/bin/python -m pytest -q tests/phase40/test_config.py tests/phase41/test_config_yaml.py tests/phase48/test_stage0_energy_config.py -k lambda_e` plus strict clip metadata/refusal tests in `tests/phase48/test_clip_metadata.py` | ✅ impacted existing + ❌ Wave 0 |
| TEST-02 | Actual `Rbar` and `eps_H` assembly inputs equal locked values | assembly regression | `.venv/bin/python -m pytest -q tests/phase48/test_loss_math_conformance.py tests/phase47/test_conf03_eps_h_wiring.py -k 'rbar_assembly or eps_h_assembly_value'` | ❌ new `Rbar`; ✅ existing `eps_H` |

### Sampling Rate

- **Per task commit:** Run the directly named Phase-48 test file plus the closest existing impacted module. [VERIFIED: project validation policy]
- **Per wave merge:** `.venv/bin/python -m pytest -q tests/phase38 tests/phase40 tests/phase41 tests/phase42 tests/phase47 tests/phase48`. [VERIFIED: dependency/test map]
- **Phase gate:** Run the full impacted suite including Phase 46, then `git diff --check`; require every new Phase-48 test and the existing `eps_H` assembly proof green before `$gsd-verify-work`. [VERIFIED: `AGENTS.md`; VERIFIED: `48-CONTEXT.md` D-22]

### Wave 0 Gaps

- [ ] `tests/phase48/__init__.py` — phase package marker if the chosen test invocation requires module imports. [VERIFIED: existing phase test layout]
- [ ] `tests/phase48/test_loss_math_conformance.py` — CONF-04/05/07 and TEST-02 boundary proofs. [VERIFIED: requirement map]
- [ ] `tests/phase48/test_stage0_energy_config.py` — default and shipped-YAML Stage-0 exact-zero proof. [VERIFIED: requirement map]
- [ ] `tests/phase48/test_clip_metadata.py` — strict fresh/resume clip-fact metadata and refusal behavior. [VERIFIED: requirement map]
- [ ] `tests/phase48/test_gradient_observability.py` — Adam/L-BFGS non-contamination, last-closure provenance, raw/applied completeness, and validation-stash isolation. [VERIFIED: requirement map]

Baseline validation completed during research:

- `.venv/bin/python -m pytest -q tests/phase38/test_loss_catalog.py tests/phase40/test_scheduled_weights.py tests/phase47/test_conf03_eps_h_wiring.py` → `32 passed, 89 subtests passed`. [VERIFIED: test run]
- `.venv/bin/python -m pytest -q tests/phase42/test_step_log_jsonl.py tests/phase47/test_conf02_s_h_pipeline.py tests/phase40/test_config.py tests/phase41/test_config_yaml.py` → `61 passed`. [VERIFIED: test run]
- A conda `python -m unittest` attempt ran 22 relevant tests but failed importing the Phase-47 pytest module because `pinn-train` lacks pytest; this is an environment mismatch, not a product-test failure. [VERIFIED: test run]

## Security Domain

Security enforcement is enabled because `.planning/config.json` does not explicitly disable it. This phase adds no network endpoint, authentication surface, secret, or cryptographic operation; its relevant security properties are strict input validation, artifact integrity, and failure honesty for untrusted/corrupt persisted state. [VERIFIED: `.planning/config.json`; VERIFIED: codebase scope]

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | no | No authentication boundary exists in this local trainer phase. [VERIFIED: codebase scope] |
| V3 Session Management | no | No user session exists. [VERIFIED: codebase scope] |
| V4 Access Control | no | No multi-principal resource or authorization decision is introduced. [VERIFIED: codebase scope] |
| V5 Input Validation | yes | Existing dataclass/YAML validation, exact metadata key/type checks, finite/range predicates, and fail-closed resume checks. [VERIFIED: `pinn/training/config.py`; VERIFIED: `pinn/training/run_metadata.py`] |
| V6 Cryptography | no | No cryptographic primitive is required or introduced. [VERIFIED: codebase scope] |

### Known Threat Patterns for PyTorch training telemetry

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Corrupt or mismatched run metadata changes claimed clip provenance | Tampering | Exact schema, expected-runtime rederivation, atomic write, and fail-closed resume before step 1. [VERIFIED: established metadata pattern; VERIFIED: D-11] |
| NaN/Inf diagnostic values produce invalid JSON or falsely complete evidence | Tampering / Denial of Service | Existing `allow_nan=False` sanitizer plus explicit completeness predicate and named nonfinite keys. [VERIFIED: `pinn/training/step_log.py`; VERIFIED: D-20] |
| Backend-specific underflow hides all later causal bins | Denial of Service (training correctness) | Dtype/device-bound floor provenance and production-MPS invariant tests. [VERIFIED: repository runtime probe] |
| Telemetry backward mutates optimizer gradients | Tampering (model update) | `autograd.grad`, before/after `.grad` and update-equivalence tests, no live graph in persisted state. [CITED: https://docs.pytorch.org/docs/2.12/generated/torch.autograd.grad.html; VERIFIED: D-18] |

## Sources

### Primary (HIGH confidence)

- `.planning/phases/48-loss-math-conformance/48-CONTEXT.md` — all locked decisions, scope, discretion, canonical references, and test boundaries. [VERIFIED: direct read]
- `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` — requirement text, phase order, and success criteria. [VERIFIED: direct read]
- `AGENTS.md` — STOP protocol, source precedence, worktree and commit policy. [VERIFIED: direct read]
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` §§3.1, 3.2, 4.1 and `ctl_instruction.md` loss formulation — locked loss/schedule contracts. [VERIFIED: direct read]
- `pinn/loss_catalog.py`, `pinn/training/controllers.py`, `config.py`, `scheduled_weights.py`, `run_metadata.py`, `step_log.py`, `tb_sink.py`, and `pinn/train.py` — live implementation seams and ordering. [VERIFIED: direct read and grep]
- Phase 38/40/41/42/47 tests and the two Stage-0 conformance audit reports — current coverage and defect escape routes. [VERIFIED: direct read and targeted execution]
- Repository `.venv` and `pinn-train` runtime probes — versions, MPS availability, and exact exponent results. [VERIFIED: direct execution]

### Secondary (MEDIUM confidence)

- https://docs.pytorch.org/docs/2.12/generated/torch.autograd.grad.html — returned-vs-accumulated gradients, unused gradients, and graph flags. [CITED: official PyTorch documentation; confidence classified MEDIUM by research seam]
- https://docs.pytorch.org/docs/2.12/type_info.html — `finfo.tiny` / smallest-normal definition. [CITED: official PyTorch documentation; confidence classified MEDIUM by research seam]
- https://docs.pytorch.org/docs/2.12/generated/torch.optim.LBFGS.html and https://docs.pytorch.org/docs/2.12/optim.html — closure reevaluation semantics. [CITED: official PyTorch documentation; confidence classified MEDIUM by research seam]

### Tertiary (LOW confidence)

- None. [VERIFIED: research source log]

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH — repository runtimes and target lock were directly inspected; the 2.12.0/2.12.1 mismatch is explicit. [VERIFIED: environment audit]
- Architecture: HIGH — every responsibility maps to an existing code seam and locked decision. [VERIFIED: code/context audit]
- Pitfalls: HIGH — assembly/logging pitfalls are directly visible in code, and the numerical blocker was reproduced on actual MPS. [VERIFIED: code audit and runtime probe]
- External API semantics: MEDIUM — sourced from official versioned PyTorch documentation and classified MEDIUM by the research seam. [CITED: official PyTorch documentation]

**Research date:** 2026-08-01

**Valid until:** 2026-08-31 for code architecture; revalidate the MPS exponent result immediately after any torch/backend version change. [VERIFIED: fast-moving numerical backend risk]
