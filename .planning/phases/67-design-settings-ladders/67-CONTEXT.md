# Phase 67: Design & Settings Ladders - Context

**Gathered:** 2026-11-01
**Status:** Ready for research and planning
**Decision source:** The owner's standing technical and scientific delegation
in `.planning/PROJECT.md`, Context, dated 2026-10-28. The owner accepted
Phase 66's `phase67-as-planned` route on 2026-11-01. Technical choices below
are agent decisions within that direction, not new owner answers.

<domain>
## Phase boundary

Deliver EXP-02, EXP-03, EXP-04 and EXP-05 through four diagnostic experiments:
depth, learning rate, time-input design and window length. Establish which
changes affect the locked setup's one-orbit fit and its per-layer response
to neighbouring times. Each experiment has committed predictions, settings,
measured budgets and a reading rule before it runs. Confirming claims repeat
on a second panel system and a second seed.

Phase 66 and its owner checkpoint are complete. Initially keep the roadmap's
experiment order. Review each result before dependent work continues; an
insertion, omission or re-aiming still requires the owner's SCOPE-49 decision.
The yardstick is Phase 68, and the final redesign decision is Phase 69.
SCOPE-45..49 remain binding. This context does not launch training.

</domain>

<decisions>
## Implementation decisions

### Decision ownership and existing evidence

- **D-01:** Carry forward Phase 65 D-01 and Phase 66 D-01. Agents research
  technical alternatives, make defensible choices inside scope, and record
  evidence, rationale and uncertainty. Do not ask the owner to supply the
  scientific design. Ask for scope changes, resource changes and other
  expressly reserved decisions, with a plain-language recommendation.
- **D-02:** Use Phase 66 as a positive control, not a depth-only experiment.
  Its variant has depth 1, width 384 and `first_omega_0 = 1000`; the locked
  variant has depth 12, width 256 and `first_omega_0 = 30`. Its confirmed
  Tier-1 result refutes "too small" for the tested one-orbit task, but does
  not identify which changed setting enabled the fit. Low neighbour cosine
  remains an association to investigate, not proof of information loss or a
  causal mechanism. Neither high cosine nor output movement alone proves an
  accurate fit.

### Controlled ladders

All four experiments remain data-only fits with constant-rate Adam on MPS
float32. The full physical window is `[0, 10]` except in EXP-05. Keep the
locked `1e-4` rate except in EXP-03, and change only the declared factor
within each matched comparison.

- **D-03:** EXP-02 uses the locked layer types at depths 2, 4, 6, 8 and 12,
  with width, input, frequency settings, optimizer, learning rate, physical
  window and data treatment otherwise locked. In particular, do not import
  Phase 66's width or frequency into this ladder. Record parameter counts so
  the report states the size change that accompanies depth. No width sweep
  or additional architecture family is added.
- **D-04:** EXP-03 changes learning rate on the locked 12-layer network,
  spanning `1e-3` through `1e-5` and including the locked `1e-4` control.
  Research selects a small, justified set of intermediate points; the
  prediction page fixes them before runs. Keep the optimizer family and
  other settings fixed. A scheduler, optimizer swap or post-result rescue
  would answer a different question and is not silently added.
- **D-05:** EXP-04 compares the raw `[tau, IC13]` input against a small set
  of time-feature designs whose bandwidth is justified from training-system
  orbital timescales. Compare each design with its raw-input control on both
  the locked network and the actual EXP-01 network, retaining each network's
  other settings. Research determines the exact feature families, frequency
  units and conditioning arrangement before implementation. Record feature
  dimensions and parameter counts, and distinguish an input-design change
  from a mere change of `first_omega_0`. Do not choose features after seeing
  a scored result or treat an orbit-specific diagnostic fit as evidence of
  generalization to new initial conditions.
- **D-06:** EXP-05 uses the locked-depth setup at 1, 2, 5 and 10 inner laps.
  Define each physical duration prospectively from the Phase 59 census for
  that system, with the same definition on repeats. Use prefixes beginning
  at physical time zero and the existing exact inclusive gold-grid mask;
  record the requested endpoint, last retained timestamp, sample count and
  actual lap coverage. Keep the locked global time normalization rather
  than stretching every prefix to `[-1, 1]`. This preserves the existing
  `diagnostic_data.py` contract and avoids also changing the first layer's
  physical frequency scale. Do not interpolate new gold samples. Recompute
  the window-mean constant and two-Kepler comparisons on each same window.
  Report shorter-window fits as such, not as full-window success.

### Budgets, repetitions and readings

- **D-07:** Carry forward the owner's compute direction in Phase 66 D-08:
  "as long as you need. this mac will be plugged into power for the weekend
  only. not weekdays. i have classes weekdays". Keep training on this Mac,
  on AC power in the established weekend window. Research, code and tests
  may proceed on weekdays. Prefer individual runs below one hour. Runs at
  or above an hour remain refused until governed pause, resume and power
  compatibility is proved. Do not infer a total Phase 67 duration from the
  Phase 65 or Phase 66 rates; measure each variant's cost and report
  the resulting experiment and phase estimates before execution.
- **D-08:** Research must define a fair budget for each contrast, including
  how update counts, logging overhead and convergence evidence are compared.
  Equal wall time alone does not give different depths equal training, and
  a low learning rate can still be improving when a fixed budget ends.
  Pre-register any bounded continuation and inconclusive/under-trained
  branches. Do not label a budget-limited result a representation failure,
  or lengthen only a disappointing arm after reading its score.
- **D-09:** Use system 1632, seed 42 for the main comparisons. Carry forward
  system 851, seed 42 and system 1632, seed 41 for confirmation. The prediction
  page specifies the contrasts to repeat and any selection rule before
  results, so "confirming" means the same claimed effect repeats on both,
  not that a favourable variant was selected afterwards. Do not claim
  confirmation from the main run alone. Define disagreement and ambiguous
  results prospectively and route them under SCOPE-47/49.
- **D-10:** Commit the scientific design and reading rule before any real
  timing or experiment run for that experiment. A timing step may then
  establish the measured budget for the science registrations without
  changing that design. Freeze exact variants, cadence, budget, repeat rule
  and interpretation thresholds before the affected runs. Preserve the
  lightweight SCOPE-47 approach; do not recreate the full sealed v2.4
  protocol. Review each experiment against its predictions and roadmap
  before moving to work that its result could invalidate.

### Scoring and harness reuse

- **D-11:** Use the frozen FEAS-01 scorer and scorecard directly. Record `E`,
  tier, per-layer neighbour similarity and its training trace, plus the
  existing output-movement and first-layer-frequency diagnostics where
  applicable. Call neighbour similarity the comparison of centred hidden
  states at adjacent times, not similarity between adjacent hidden units.
  Record actual physical and normalized time coordinates, especially on
  short windows and changed inputs. Loss is context only. Keep GAP-59-08's
  energy limitation explicit; no energy bar or scorer definition changes
  here.
- **D-12:** Extend INST-08 only inside the diagnostic harness, with fresh
  named variants and committed registrations for Phase 67. Preserve locked
  production values, historical pages, registrations and run evidence.
  A changed pinned dependency requires new registration digests, not edited
  historical evidence. Test the new variant, input, window and scoring paths
  before relying on them. Retain Stage-0 TRAIN-only, pre-open refusals and
  rejection of diagnostic records by graded-run/evaluator entry points.
- **D-13:** Apply the reuse conditions in `65-CLOSEOUT.md` before affected
  new use. `66-REVIEW.md` also records accepted, unfixed reader limitations.
  Do not assume its EXP-01 orbit constants, full-window baseline checks,
  bandwidth checks or branch table apply to the new ladders. The Phase 67
  reader must validate the registered orbit, window, settings and evidence,
  and handle its admitted record shapes. Scope any hardening to the paths
  Phase 67 actually uses; do not turn this phase into an unrelated repair
  of every historical CLI.

### Agent discretion for research and planning

- Exact intermediate learning rates and the smallest informative set of
  time-feature designs, with source-grounded bandwidth and unit checks.
- Exact lap-to-time conversion and baseline verification for each window.
- Timing-run lengths, run budgets, cadence, fair-comparison policy,
  interpretation thresholds and prospective repeat-selection rules.
- The minimal harness, registration, reader and test changes that implement
  those decisions while preserving historical evidence and isolation.

These are prospective research and prediction-page tasks, not permission to
choose settings or reading rules after observing their results. No new
owner-only decision or source-silent scope change was identified in this
context capture.

</decisions>

<canonical_refs>
## Canonical references

Downstream agents must read these before planning or implementing.

### Scope, delegation and prerequisite

- `.planning/ROADMAP.md`: Phase 67 and the SCOPE-49 review sequence.
- `.planning/REQUIREMENTS.md`: EXP-02..05, shared experiment acceptance,
  SCOPE-45..49 and reserved owner checkpoints.
- `.planning/PROJECT.md`: Current Milestone, Context standing delegation,
  and Constraints.
- `AGENTS.md` and `docs/git-guidelines.md`: applicable grounding, ownership
  and commit rules.
- `.planning/phases/66-small-network-control/66-CONTEXT.md`: inherited
  decision ownership, compute direction, controls and repeat identities.
- `.planning/phases/66-small-network-control/66-CHECKPOINT-1-RULING.md`:
  owner acceptance of proceeding with Phase 67 unchanged.
- `.planning/phases/66-small-network-control/66-RESULT.md`: confirmed result
  and its limits.
- `.planning/phases/66-small-network-control/66-PREDICTION.md` and
  `.planning/phases/66-small-network-control/66-TIMING-PREDICTION.md`:
  exact positive-control design and prospective-registration precedent.

### Measurement and reuse conditions

- `.planning/phases/65-probe-on-the-record-fit-harness/65-CONTEXT.md`
- `.planning/phases/65-probe-on-the-record-fit-harness/65-FINDINGS.md`
- `.planning/phases/65-probe-on-the-record-fit-harness/65-CLOSEOUT.md`
- `.planning/phases/66-small-network-control/66-RESEARCH.md`: prior
  bandwidth reasoning to verify, not a replacement for Phase 67 research.
- `.planning/phases/66-small-network-control/66-REVIEW.md` and
  `.planning/phases/66-small-network-control/66-VERIFICATION.md`: accepted
  limitations and the boundary of the historical verification.
- `.planning/phases/59-read-only-baseline-scorecard/evidence/census/panels.json`
  and `.planning/phases/59-read-only-baseline-scorecard/evidence/census/census.json`:
  panel identities and orbital timescales.
- `.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md`: GAP-59-08.
- `pinn/verification/artifacts/feasibility_scorecard_v1.json` and
  `pinn/verification/feasibility_scorer.py`: frozen scoring.

### Diagnostic integration

- `pinn/verification/diagnostic_variants.py`
- `pinn/verification/diagnostic_fit.py`
- `pinn/verification/diagnostic_data.py`
- `pinn/verification/diagnostic_similarity.py`
- `pinn/verification/diagnostic_guard.py`
- `pinn/verification/diagnostic_phase66.py`
- `pinn/verification/diagnostic_power.py`
- `pinn/verification/two_kepler.py`
- `pinn/network.py` and `pinn/architecture_spec.py`: production parity and
  locked setup; no production redesign is authorized here.
- `tests/phase65/` and `tests/phase66/`: existing contracts and fixtures.
- `scripts/phase60_run_control.py`, `scripts/phase60-pause.sh`,
  `scripts/phase60-resume.sh` and `scripts/phase60-power-guard.sh`: mandatory
  compatibility work if a run at or above one hour is proposed.

</canonical_refs>

<code_context>
## Existing code insights

- `diagnostic_variants.py` has named depth, width, frequency, learning-rate
  and window fields, a sealed `locked-12` catalog and copy-on-registration.
  Its existing supported input declaration is `raw_tau_ic13`; time-feature
  variants need an explicit, tested extension.
- `diagnostic_data.py` already applies an exact physical prefix and retains
  the global `T_CHARACTERISTIC_TIME` normalization. Reuse its Stage-0 TRAIN
  reader and recorded normalizer rather than refitting statistics.
- `diagnostic_fit.py` supplies registration admission, timing, fixed-cadence
  similarity logging, same-window comparisons and exclusive run evidence.
  Its current admission path is not blanket support for new Phase 67 variants.
- `diagnostic_similarity.py` supplies the shared DIAG-09 measurement. Input
  and window changes must keep its time coordinates valid and explicit.
  Its frequency diagnostic currently reads input-weight column zero; an
  encoded input must not inherit that interpretation without verification.
- The frozen scorer constructs raw `[tau, IC13]` and differentiates the
  model for velocities. EXP-04's diagnostic model must accept that public
  input and keep its feature transform differentiable inside the model,
  rather than require an edit to the frozen scorer.
- `diagnostic_phase66.py` supplies a precedent for measured budgets and
  reading rules, but its scientific constants are specific to EXP-01.
- `diagnostic_power.py` supplies the established AC/weekend launch gate.
  Longer-run pause/resume compatibility remains unproved.

</code_context>

<specifics>
## Prior result carried forward

Phase 66's recorded main and repeat results are Tier 1: `E = 0.0114312` on
1632/42, `0.0172056` on 851/42 and `0.0789849` on 1632/41. These rounded
figures summarize `66-RESULT.md`; downstream result claims must cite its
committed records. They establish a working positive control, not a result
for any Phase 67 ladder. No training or new real-data experiment ran during
this discussion workflow.

</specifics>

<deferred>
## Deferred ideas

- Energy-metric adjudication and pass bars, Phase 68.
- Final cause findings, v2.6 direction and commissioning `trainex-r5`, Phase 69.
- Framework amendments, production redesign and physics-term repairs, v2.6.
- Any result-driven change to these four experiments, an owner decision
  under SCOPE-49 rather than an automatic consequence of this context.

### Reviewed todos, not folded

- `.planning/todos/pending/d-06-static-epsilon-sensitivity-check.md`:
  stage-label and validation-gate work outside these data-only experiments.
- `.planning/todos/pending/trainex-r1-research-handoff.md`: stale research
  handoff housekeeping outside Phase 67. Both retain the Phase 65/66
  disposition; neither todo is changed.

</deferred>

---

*Phase: 67-design-settings-ladders*
*Context gathered: 2026-11-01*
