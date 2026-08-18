# Phase 48: Loss-Math Conformance - Context

**Gathered:** 2026-07-31
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 48 makes the loss math executed by the Stage-0 trainer conform to the
locked framework contracts. It owns exactly CONF-04..07, INST-02, TEST-01, and
TEST-02:

- correct `Rbar` to `(1/3) sum_i ||f_i||^2` before causal weighting;
- add the mandatory causal-exponent underflow clip and record its bound;
- restore the locked Stage-0 `lambda_E^max = 0`;
- implement the owner-ratified scalar reduction for `L_data`;
- log per-term gradient statistics alongside the existing losses and weights;
- correct tests that defend divergent behavior in the same changes; and
- prove at the assembly boundary that the loss receives the locked `Rbar` and
  `eps_H` values.

This is a conformance phase, not a recipe experiment. It runs no training, does
not access held-out evaluation data, does not edit framework specs, does not
re-audit component math already recorded as verified clean, and does not tune or
automatically rebalance loss weights. Phase 49 owns full PHYS-05 table
enforcement, runtime invariant B, the placeholder census, and the known-
divergence register. Phases 50-51 own the Stage-0 re-run and the single
authorized held-out evaluation.

</domain>

<decisions>
## Implementation Decisions

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
  causal-loss mean. The conformance audit's verified-clean inventory is
  load-bearing.

### Governance and scope locks

- **D-24 [SCOPE-27..32]:** No training run, held-out evaluation, framework-spec
  edit, recipe tuning, automatic dominance reweighting, or trainex-r2 tuning-
  report consultation in Phase 48.

- **D-25 [ORDERING]:** Plan and implement CONF-04 before CONF-05. Phase 47's
  CONF-09 frame completion is already a hard predecessor. Gradient
  instrumentation and tests may be developed in parallel only where their
  assertions do not encode the pre-correction formula.

### Agent's Discretion

The planner may choose helper/module names, phase-scoped test-file organization,
the exact established run-record artifact and schema migration used for D-11,
and the graph-safe implementation used to collect D-16..D-20. Those choices
must preserve every decision above, add no dependency, keep JSONL as the durable
gradient-statistics record, and not introduce a cadence, threshold, tuning
signal, or evaluator path outside this phase.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and owner-ratified boundaries

- `.planning/ROADMAP.md` §"Phase 48: Loss-Math Conformance" — goal,
  requirements, blocking GAP-45-01 checkpoint, CONF-04-before-CONF-05 order,
  and success criteria.
- `.planning/REQUIREMENTS.md` — CONF-04..07, INST-02, TEST-01..02,
  SCOPE-27..32, and the binding evaluation policy.
- `.planning/PROJECT.md` — active v2.2 milestone and owner-ratified evaluation
  policy.
- `.planning/STATE.md` — current Phase 48 position, inherited rulings, and the
  Phase 47 predecessor state.
- `AGENTS.md` — gap/STOP protocol, source precedence, and Git policy.

### GAP-45-01 and inherited owner rulings

- `.planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-GAPS.md`
  §"GAP-45-01" — full decision space, mathematical grounding, initial deferral,
  retained-run condition, and final 2026-07-31 Option-A resolution.
- `.planning/milestones/v2.1-GAPS.md` — milestone-level record for GAP-45-01
  through GAP-45-04 and inherited obligations.
- `.planning/milestones/v2.2-GAPS.md` §"Coupling to inherited v2.1
  obligations" — v2.2 record that the Phase 48 checkpoint is resolved.
- `.planning/milestones/v2.1-phases/44-physics-gate-forensics/evidence/diag02/loss_decomposition.json`
  — retained-run loss values used to compute both `L_data` readings.

### Locked loss and training contracts

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
  §§3.1, 3.2, 4.1 — Huber data term, locked `Rbar`, causal weighting and
  mandatory underflow clip, and PHYS-05 schedule.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
  §"Loss Function Formulation" — total-loss assembly, Phase-35 logging
  precondition, optimizer-phase semantics, and component ownership.
- `.planning/milestones/v1.6-phases/35-loss-energy-weight-contracts/35-CONTEXT.md`
  — LOSS-01..04 decisions, including logging-before-reweighting and the
  deferred numeric clip bound.
- `.planning/phases/47-frame-completion-s-h-pipeline/47-CONTEXT.md` — completed
  frame and `S_H`/`eps_H` decisions that Phase 48 consumes.

### Verified conformance evidence

- `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-24-stage0-training-path-conformance-audit.md`
  — C-01..C-08 and the equally binding verified-clean inventory.
- `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-28-conformance-divergence-verification-report.md`
  — independent confirmation of `Rbar`, clip, energy-weight, and gradient-
  instrumentation defects plus the corrected-frame ordering constraint.

### Code and test seams

- `pinn/loss_catalog.py` — `data_huber_loss`, `causal_physics_loss`, and the
  verified-clean downstream causal-loss consumer.
- `pinn/training/controllers.py` — `RunController._non_data_terms`,
  `_compose_loss_terms`, Adam/L-BFGS gradient paths, and the canonical step-log
  emission point.
- `pinn/training/config.py` — current divergent `LossConfig.lambda_e_max`
  default.
- `pinn/training/scheduled_weights.py` — reusable PHYS-05 ramp with a correct
  zero Stage-0 default.
- `pinn/training/step_log.py` — canonical JSONL field registry and non-finite
  policy.
- `configs/stage0-example.yaml` and `configs/smoke.yaml` — shipped Stage-0
  configs that currently override `lambda_e_max` to `1.0`.
- `tests/phase38/test_loss_catalog.py` — existing component tests, including
  the now-ratified mean `L_data` reduction and supplied-`Rbar` causal tests.
- `tests/phase40/test_scheduled_weights.py` — generic cap/table tests requiring
  explicit Stage-0 zero coverage.
- `tests/phase47/test_conf03_eps_h_wiring.py` — existing `eps_H` assembly-
  boundary proof required by TEST-02.

### Explicitly excluded source

- `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/` is not a
  Phase 48 grounding source under SCOPE-31. Do not consult its tuning analysis.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `data_huber_loss` already implements the owner-ratified D-01 mean. The work is
  provenance and conformance coverage, not a numerical rewrite.
- `causal_physics_loss` already centralizes sorted-time validation, exclusive
  stop-gradient prefix sums, causal weights, and detached detail reporting. The
  clip belongs at its exponent seam.
- `RunController._non_data_terms` is the single assembly point where the
  `(N_t,3,3)` residual becomes `Rbar`; correcting it reaches Adam, validation,
  and the L-BFGS non-data path together.
- `_compose_loss_terms` and `compose_total` expose the five named term tensors
  and the applied `LossWeights`, the inputs needed for per-term gradient
  diagnostics without inventing a parallel loss catalog.
- `_log_step` is the single emission point shared by JSONL, human logs, and
  TensorBoard. `STEP_LOG_FIELDS` and `_sanitize_step_record` already provide a
  durable vocabulary and non-finite policy.
- `ScheduledWeights` already defaults `lambda_e_max` to zero and implements the
  generic warmup correctly; the divergence is the resolved config/default and
  shipped Stage-0 overrides.

### Established Patterns

- Assembly-boundary interception is preferred over duplicating component
  formulas in tests. Phase 47's `test_eps_h_assembly_value` is the direct
  precedent.
- Phase-scoped tests are dataset-free and use synthetic sources/controllers;
  no Stage-0 run is needed to prove these repairs.
- Run metadata and summaries use strict schemas, atomic writes, and fail-closed
  re-validation. Any clip-bound persistence follows those patterns rather than
  introducing an informal sidecar.
- Step logs preserve one canonical JSONL event and fan out to optional sinks.
  New gradient fields extend that event; they do not create a second log.

### Integration Points

- **Residual assembly -> causal loss:** `controllers.py` constructs corrected
  `Rbar`; `loss_catalog.py` clips its causal exponent and consumes the values.
- **Resolved config -> scheduler:** `LossConfig` and shipped YAML resolve
  Stage-0 zero; `ScheduledWeights.current()` applies the existing ramp.
- **Term graph -> instrumentation:** five term tensors plus the current lambda
  vector produce raw/applied gradient norms before the optimizer mutates state.
- **Instrumentation -> durable evidence:** `_log_step` -> `STEP_LOG_FIELDS` ->
  JSONL sanitizer/handler; optional TensorBoard mirrors the same source.
- **Existing energy metadata -> TEST-02:** the Phase 47 `eps_H` assembly test
  remains the proof that the loss receives the real dataset statistic.

</code_context>

<specifics>
## Specific Ideas

- Keep the distinction between **mathematical residual scale** and **numeric
  exponent range** visible. CONF-04 fixes the former; the dtype-derived clip
  protects the latter. Neither is a tunable loss weight.
- Record every conformance constant with provenance and resolved runtime dtype
  so a later run can prove what happened without reverse-engineering code.
- Per-term gradients are evidence, not a control loop. Phase 48 observes them;
  v2.2 never uses them to change the recipe.
- A test that supplies a correct component input proves only the component. A
  test that intercepts what assembly actually supplies protects the seam where
  every verified divergence in this phase occurred.

</specifics>

<deferred>
## Deferred Ideas

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

</deferred>

---

*Phase: 48-loss-math-conformance*
*Context gathered: 2026-07-31*
