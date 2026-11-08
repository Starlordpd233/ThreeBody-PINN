# Phase 68: Yardstick - Context

**Gathered:** 2026-11-08
**Status:** Ready for research and planning
**Decision source:** The owner's evidence-first direction in `68-SPEC.md` and
standing technical delegation in `.planning/PROJECT.md` (2026-10-28).

<domain>
## Phase boundary

Audit the Stage-0 yardsticks against Brutus's recorded answer and a constant
prediction on the fixed training panel. Commit the measurements before owner
checkpoint 2. The checkpoint uses those results to decide how to measure
energy drift and what counts as a successful proof of concept.

</domain>

<spec_lock>
## Requirements locked by SPEC.md

Three requirements are locked: YARD-01, YARD-02 and YARD-03. Read
`.planning/phases/68-yardstick/68-SPEC.md` for their full requirements,
boundaries, constraints and acceptance criteria. The audit uses existing
Stage-0 TRAIN records, the frozen FEAS-01 scorer and shared gate calculations.
The specification places training, new validation/test access, a graded
run, the preserved evaluation, metric repairs, new trajectory generation
and changes to locked values outside this phase. Phase 69 owns the final
findings and redesign choice. v2.6 owns authorized amendments.

</spec_lock>

<decisions>
## Implementation decisions

### Inputs and comparisons

- **D-01. Use the per-record TRAIN reader.** Reuse `Stage0TrainingReader`,
  the hash-checked split manifest and the process open attestation. Limit
  the audit to the hierarchical base/gold pairs for 1632, 851 and 4658. The
  base record supplies the physical orbit's Stage-0 label, so the gold
  sibling's own `UNASSIGNED` label does not exclude it. Require TRAIN and
  Stage 0 before resolving a corpus path. Record the keys admitted and
  the actual split opens. Use `load_reference` for the existing gauge,
  body permutation and ordered masses.
- **D-02. Compare matched samples within each grid.** Use the frozen
  scorecard's native gold window through `t = 10` for the primary score.
  Use the persisted base sibling for the coarse comparison. Within each
  grid and window, feed the reference positions and recorded velocities
  to `score_trajectory` for the correct answer. For the constant answer,
  repeat each body's mean position over the corresponding sampled window
  and supply analytic zero velocity. This is the existing diagnostic
  baseline. Keep the gold and base windows, sample counts and measured
  cadences explicit. Verify that the compared records have matching body
  order and use the existing grid agreement evidence.

### Measurement and evidence

- **D-03. Call the shared gate calculations on the same inputs.** For the
  finite-difference energy comparison, use `compute_trajectory_gate_metrics`
  and `aggregate_gate_verdict` from `gate_metrics`. Pair `r_prime` with
  `u = t/T` via `gate_time_coordinate`, using ordered raw masses. Use the
  same gold positions and times for the recorded-velocity reference and
  the finite-difference probe. Retain the production stencil, including
  its endpoints, and record the native base result separately. Map the
  shared calls to `compute_validation_gate` and `evaluate_run`, including
  any input dtype differences relevant to the reading. The audited
  aggregate is over the TRAIN panel. Exercise the calculation with
  in-memory inputs, outside the evaluator's attempt and receipt path.
- **D-04. Distinguish the verdict from the audit finding.** Report the
  existing bar and verdict alongside the expected known answer. A complete
  audit can expose a correct-answer failure or a constant-prediction pass.
  Preserve separate FEAS-01 tier, finite-difference gate and context-only
  results. A constant with finite nonzero initial energy conserves energy
  relative to its own initial state. The measured floor describes the drift on the
  sampled Brutus references. If it drives a decision, inspect the returned
  Hamiltonian series to explain whether the initial value or endpoint
  estimates contribute to the discrepancy. Publish provenance, a rerun
  command and results at the precision needed to reproduce verdicts. Use
  the edge checks in `68-SPEC.md` to verify the existing boundaries and
  record any refusal or missing row as such.

### Owner checkpoint and research handoff

- **D-05. Bring checkpoint 2 the committed audit first.** Present the
  charter's three C-7 choices with the measured base/gold comparisons and
  the consequences for production validation and evaluation. Ask for C-7
  explicitly. Then present C-2 and C-4 through C-6 with that disposition
  stated, including the C-5 dependency on C-7. Use the frozen comparison
  points and primary published evidence, explaining differences in tasks
  and metric definitions. Record each owner answer verbatim or record the
  row as open. C-6 and C-7 require individual answers. GAP-59-08 stays OPEN
  and YARD-02 stays unsatisfied until an explicit C-7 ruling. On instruction,
  close the original gap with a cross-reference to the verbatim ruling.
  Route resulting changes, including evaluation text under C-11, to v2.6.

### Agent discretion for research and planning

Research should confirm the native record and caller-input conventions,
the smallest reproducible audit entry point, and the evidence needed to
distinguish an inaccurate prediction from a measurement error. Planning
chooses file layout, result encoding and focused checks using existing
repository patterns. The accepted specification defines coverage and
verdict semantics. Any source-silent semantic choice or proposal to
change scope follows the applicable STOP and SCOPE-49 rules.

</decisions>

<canonical_refs>
## Canonical references

Read these before planning or implementing the relevant work.

### Scope and decision authority

- `.planning/phases/68-yardstick/68-SPEC.md` (locked requirements, must read
  before planning).
- `.planning/ROADMAP.md` (Phase 68 and the v2.5 diagnosis discipline).
- `.planning/REQUIREMENTS.md` (YARD-01 through YARD-03, SCOPE-45 through
  SCOPE-49 and owner checkpoint 2).
- `.planning/PROJECT.md` (v2.5 governance and standing GSD delegation).
- `.planning/phases/64-feasibility-verdict/64-CHARTER.md` (C-1, C-2,
  C-4 through C-7, C-11 and the reply rule).
- `.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md` (GAP-59-08
  and its owner-routed disposition).

### Scoring and comparison evidence

- `.planning/phases/59-read-only-baseline-scorecard/59-CONTEXT.md` (D-30,
  D-31 and D-35 for velocity, grid and corpus contracts).
- `.planning/phases/59-read-only-baseline-scorecard/evidence/census/panels.json`
  (fixed panel selection).
- `.planning/phases/59-read-only-baseline-scorecard/evidence/baselines/baselines.json`
  (frozen comparison points for the decision packet).
- `.planning/phases/66-small-network-control/66-VERIFICATION.md` (replicated
  Tier-1 one-orbit fit).
- `.planning/phases/67-design-settings-ladders/67-CLOSEOUT.md` (registered
  outcomes, scientific limits and the yardstick handoff).
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
  (§10.6 held-out gate contract).
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
  (Step 1A energy drift and the C-11 evaluation text).
- `.planning/milestones/v2.2-phases/47-frame-completion-s-h-pipeline/evidence/frame-re-ratification/20260731T012304Z/re-ratification.md`
  (ratified position, time and mass pairing used by the production callers).

</canonical_refs>

<code_context>
## Existing code insights

- `pinn/verification/diagnostic_data.py` has the pre-open Stage-0 TRAIN
  reader. Its `open_diagnostic_context` shows how to wire the manifest
  and attestation in `pinn/verification/split_allowlist.py`. Reuse the
  reader with `pinn/verification/production_reference.py` for matched
  positions, velocities and metadata.
- `pinn/verification/diagnostic_fit.py` defines the sampled window-mean
  constant row. `pinn/verification/feasibility_scorer.py` scores explicit
  velocities and `pinn/verification/feasibility_scorecard.py` loads the
  thresholds from `pinn/verification/artifacts/feasibility_scorecard_v1.json`.
- `pinn/verification/gate_metrics.py` supplies the finite-difference
  measurement and worst-trajectory verdict. `pinn/training/validation_gate.py`
  supplies the ratified frame and time conversion used by both the
  validation path and `pinn/evaluate.py`.
- `tests/phase59/test_scorer_known_errors.py`,
  `tests/phase59/test_split_allowlist.py` and `tests/phase43/test_gate_boundary.py`
  are precedents for known answers, pre-open refusals and gate boundaries.

</code_context>

<specifics>
## Prior results to carry forward

Phase 66 established a replicated Tier-1 data fit to individual TRAIN
orbits with a smaller network. Several settings changed together. Phase 67
confirmed worsening at its highest learning rate, with the depth,
time-input and window contrasts unsettled under their registered rules.
Use these results for the task they tested. Generalization to unseen
initial conditions remains an open question. GAP-59-08 supplies the
historical coarse-grid concern; Phase 68 measures the native gold result.

</specifics>

<deferred>
## Deferred ideas

- The v2.6 direction and commissioning of `trainex-r5` go to Phase 69.
- Framework and production changes follow the owner's instructions into v2.6.

### Reviewed todos, outside scope

- `.planning/todos/pending/d-06-static-epsilon-sensitivity-check.md`
  concerns the effect of changing softening on corpus admission and stage
  labels. It remains a separate check. The yardstick holds softening fixed
  while comparing velocity measurements.

</deferred>

---

*Phase: 68-yardstick*
*Context gathered: 2026-11-08*
