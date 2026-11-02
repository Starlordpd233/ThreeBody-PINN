# Phase 67: Design & Settings Ladders - Research

**Researched:** 2026-11-01. **Domain:** diagnostic one-orbit fits, differentiable time features, controlled comparisons. **Confidence:** HIGH for repository contracts; MEDIUM for prospective scientific designs. No corpus reads, timing or training were performed.

<user_constraints>
## User Constraints (from CONTEXT.md)

The following decision, discretion and deferred text is copied verbatim from `67-CONTEXT.md:33-162,269-281`. [VERIFIED: .planning/phases/67-design-settings-ladders/67-CONTEXT.md:33-162]
<!-- DATA_8d3f17ac_START -->
### Locked Decisions

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

### Deferred ideas (OUT OF SCOPE)

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
<!-- DATA_8d3f17ac_END -->
</user_constraints>

## Summary

Implement four independent, prospectively specified contrasts through INST-08. Reuse production layer construction without changing production locks, keep feature transforms inside the diagnostic model, and use sampled signed-lap prefixes. Commit each experiment's design before timing, then derive equal-update budgets from its slowest measured arm. Predictions concern finite-budget fits; similarity remains associated evidence, not a demonstrated cause. [VERIFIED: .planning/phases/67-design-settings-ladders/67-CONTEXT.md:33-147]

## Architectural Responsibility Map

| Capability | Primary tier | Secondary tier | Implementation recommendation |
|---|---|---|---|
| Registration, budget, interpretation | Local diagnostic orchestration | Evidence storage | A Phase 67 catalog and reader own scientific settings; production training owns none. |
| Time encoding and derivatives | Diagnostic model | Frozen scorer | Keep the public raw input; encode inside the forward pass. |
| Prefix selection and comparisons | Diagnostic data adapter | Census algorithm | Select existing samples and recompute same-window comparisons. |
| Launch admission | Existing local power/access guards | Registration verifier | Validate metadata before data access or optimizer creation. |

These assignments implement D-05..13, rather than introduce application tiers. [VERIFIED: .planning/phases/67-design-settings-ladders/67-CONTEXT.md:66-147]

<phase_requirements>
## Phase Requirements

| ID | Description from requirements | Research support |
|---|---|---|
| EXP-02 | "The locked layer types at 2, 4, 6, 8 and 12 layers, with everything else locked, on orbit 1632." | Depth catalog, counts and every-layer logging. [VERIFIED: .planning/REQUIREMENTS.md:121-123] |
| EXP-03 | "The locked network at learning rates from 10⁻³ down to 10⁻⁵. The exact points are on the prediction page." | Five-point constant-Adam grid and common updates. [VERIFIED: .planning/REQUIREMENTS.md:124-126] |
| EXP-04 | "Time features matched to how fast the orbit moves, against the locked input, where time shares the first layer with 13 inputs that are constant on one orbit." | Two nested harmonic designs on both required backbones. [VERIFIED: .planning/REQUIREMENTS.md:127-129] |
| EXP-05 | "Windows of 1, 2, 5 and 10 inner laps." | First-crossing sampled prefixes and matched baselines. [VERIFIED: .planning/REQUIREMENTS.md:130-132] |
</phase_requirements>

## Project Constraints (from AGENTS.md)

Use Sequentialthinking for multistep work; orient to the task worktree; preserve unrelated work. Surface consequential ungrounded decisions; do not use legacy PINN code as physics authority. Keep framework specs and locked production values unchanged. For execution, declare disjoint ownership, stage explicit paths, use `scripts/agent-commit` with both required Git agent variables, inspect staged/unstaged diffs and run relevant checks plus `git diff --check`. No hook bypass or destructive Git operation without the prescribed approval/checkpoint. Read `docs/README.md` before creating any docs files and follow its placement/frontmatter rules. This research creates no docs file and no commit. [VERIFIED: AGENTS.md:9-14,61-93,144-212,223-254]

## Standard Stack

Retain the existing environment. The lockfile declares "torch==2.12.1", "numpy==2.4.6", "h5py==3.16.0"; the existing tests import "unittest". No package install, dependency upgrade or new testing framework is required, so the package-legitimacy installation gate does not apply. [VERIFIED: requirements-lock.txt:5-19; tests/phase66/test_budget.py:15-23] The read-only environment probe returned Python 3.11.15, those three package versions and `mps_available True` using the established pinn-train interpreter. [VERIFIED: environment probe, 2026-11-01]

## Architecture Patterns

The proposed flow is `committed design → registered timing → common budget → committed science registrations → guarded fits → frozen scoring → variant-aware reading → SCOPE-49 review → next experiment`. A refusal ends that branch before affected dependent work. This follows D-07..13. [VERIFIED: .planning/phases/67-design-settings-ladders/67-CONTEXT.md:90-147]

**EXP-02 and EXP-03 recommendation.** Use the exact locked depth set and width from D-03. Use rates `1e-3, 3e-4, 1e-4, 3e-5, 1e-5`; the intermediate factors give roughly half-decade spacing across the locked interval without adding an optimizer question. Compare each noncontrol arm with the experiment's freshly registered control at equal updates. This is a prospective technical choice under D-01/D-04, not a claim of an optimal rate. [VERIFIED: .planning/phases/67-design-settings-ladders/67-CONTEXT.md:33-65]

**EXP-04 recommendation.** Use raw input plus two deterministic nested Fourier designs: append one sine/cosine pair at the census mean inner frequency; append two pairs at its fundamental and second harmonic. Retain raw tau and all IC components in each design. The resulting input dimensions are 14, 16 and 18. Use `f=N_in/10` cycles per physical time unit and `phase=2*pi*f*t=pi*N_in*(tau+1)`; use the same physical frequencies on both backbones. Pin each system's frequencies before timing, including the repeat system. The census gives "N_in": 10.471994061054543, "id": 1632 and "N_in": 18.612048388702, "id": 851. [VERIFIED: .planning/phases/59-read-only-baseline-scorecard/evidence/census/panels.json:167-180] This deliberately tests a fundamental and one harmonic, not a claim that two harmonics suffice for an eccentric three-body trajectory. Register the maximum adjacent feature-phase increment from the existing grid and require it below pi before runs; do not silently revise frequencies if that check fails. These are prospective design choices under D-05. [VERIFIED: .planning/phases/67-design-settings-ladders/67-CONTEXT.md:66-75]

Keep the real EXP-01 backbone settings verbatim: "depth=1", "width=384", "learning_rate=1e-4", "window_length=10.0", "first_omega_0=1000.0". [VERIFIED: pinn/verification/diagnostic_phase66.py:82-90] Preserve the first-layer fan-in initialization when changing input dimension and report its changed bound and parameter count as part of the input-design intervention; do not claim a parameter-matched or bandwidth-only test. The constructor uses "bound = 1.0 / self.in_features". [VERIFIED: pinn/network.py:74-91]

The public model contract is "forward(self, tau_ic13, masses)". The scorer constructs "torch.cat([tau, ic13_t], dim=0).unsqueeze(0)" and computes "torch.func.vmap(torch.func.jacrev(flat_traj))(u_chunk)". [VERIFIED: pinn/network.py:210-228; pinn/verification/feasibility_scorer.py:355-369,407-420] Implement the transform with tensor operations inside a diagnostic subclass or adapter, persistent constant buffers and unchanged COM projection. Keep "input_layer" and "hidden_layers" observable so the existing hooks still capture every layer. [VERIFIED: pinn/network.py:168-196; pinn/verification/diagnostic_similarity.py:208-222] PyTorch supports persistent buffers as nonparameter state and composable function transforms. [CITED: https://docs.pytorch.org/docs/2.12/generated/torch.nn.Module.html#torch.nn.Module.register_buffer] [CITED: https://docs.pytorch.org/docs/2.12/func.html]

**EXP-05 recommendation.** Reuse the census definition, summing signed `atan2(normal·cross(r[j-1],r[j]), dot(r[j-1],r[j]))/(2*pi)` about the initial inner-orbit normal. Its exact source operations are "return np.arctan2(triple, dots)" and "steps.sum() / _TWO_PI". [VERIFIED: pinn/verification/stage0_census.py:131-146,174-181] After registration authorizes metadata capture, choose the first EXISTING gold sample whose cumulative signed turns reaches each requested lap count; record the preceding/current timestamps and turns, exact chosen endpoint, retained count and actual coverage. Refuse if unreached, nonfinite or the census angular-step guard fails. Do not substitute total absolute turning or interpolate. Use `L*10/N_in` only as an approximate cost estimate, never the endpoint rule. Preserve the loader mask "return (t >= 0.0) & (t <= window)" and normalization "tau = 2.0 * (times_t / T_CHARACTERISTIC_TIME) - 1.0". [VERIFIED: pinn/verification/diagnostic_data.py:446-459,550-555] Persist and independently recheck same-window constant/formula expectations before science; retain a formula's explicit nonapplicability rather than manufacturing a score. [VERIFIED: pinn/verification/diagnostic_fit.py:699-778]

**Budget and interpretation recommendation.** Register warmup plus a bounded timing interval for every variant/system, with identical normalized logging cadence and explicit launch, scoring, comparison and write overhead measurements. Start with 200 warmup and 1,000 measured updates, a 900-second whole-run cap and early mechanical refusal if it cannot finish. Timing results set costs only. For science, choose the largest common update count in multiples of 100 for which every arm's projected whole-run wall, including 25% optimizer-rate margin and measured overhead, is at most 75% of a 3,540-second cap. Use the slowest projected arm across that experiment and its repeats. Freeze cadence at start, quarters and end; include frozen scorer checkpoints at half, three-quarters and end so improving E can be distinguished from loss/movement alone. Time this exact cadence before assigning budgets. Do not use past phases' rates or equal wall time as equal training. These numbers are prospective choices implementing D-07/D-08/D-10. [VERIFIED: .planning/phases/67-design-settings-ladders/67-CONTEXT.md:90-120]

Pre-register no automatic continuation. If final-quarter E improves by more than 5% relative to its three-quarter value, mark the endpoint unsettled; a failed fit at the cap is inconclusive about representational impossibility even when its trace appears flat. A successful endpoint remains an observed fit. Compare each depth/rate/input arm with its declared raw/locked control, and each shorter prefix with the ten-lap prefix. Repeat every declared contrast on both confirmation cases, keeping both arms matched; this avoids post-result winner selection. A replicated finite-budget accuracy effect requires the same direction in all three cases and either a frozen tier change in that direction or at least a 20% E change in each case. Smaller effects, ties, nonfinite evidence, unsettled endpoints and opposite directions are explicitly ambiguous or inconclusive, not confirmation. Similarity traces describe whether accuracy and adjacent-time hidden-state response change together; they do not prove causation. Report per-arm wall projections and the complete experiment/phase cost before execution. Review EXP-02, then EXP-03, then EXP-04, then EXP-05; owner decisions gate any SCOPE-49 re-aiming. These are prospective thresholds and repeat rules under D-08..10, not revised FEAS pass bars. [VERIFIED: .planning/phases/67-design-settings-ladders/67-CONTEXT.md:99-132; .planning/REQUIREMENTS.md:180-194]

### Minimal files and new symbol sketch

Proposed additions, not claims of existing paths: `pinn/verification/diagnostic_phase67.py` owns `PHASE67_REGISTRY`, `phase67_budget`, `read_phase67_record` and experiment review; `pinn/verification/diagnostic_time_features.py` owns `DiagnosticTimeFeatures` and its diagnostic model; `tests/phase67/` owns synthetic contract tests. Keep the census-prefix helper in the Phase 67 module unless the planner needs a separate cohesive module. Store new predictions, registrations and evidence under this phase directory using the existing exclusive-write convention. Do not change historical files.

Targeted extension points: "SUPPORTED_TIME_FEATURES = (\"raw_tau_ic13\",)" and "def build_variant(variant, *, seed, dtype, device)" need explicit tested feature declarations; "def _named_registry(name)" needs a separate Phase 67 registry dispatch without editing the Phase 66 catalog. [VERIFIED: pinn/verification/diagnostic_variants.py:52-56,203-223; pinn/verification/diagnostic_fit.py:317-330] Extend the fit/logging path only for Phase 67 checkpoint scoring and feature applicability. The current frequency formula is "model.input_layer.weight[:, 0].detach().abs() * omega / math.pi"; for encoded inputs emit an explicit not-applicable reason and the registered feature-frequency metadata, rather than a misleading overall bandwidth. Preserve raw historical record shapes. [VERIFIED: pinn/verification/diagnostic_similarity.py:224-227]

The new reader must validate exact registered orbit/seed/window/settings, all expected layer rows, finite numbers excluding booleans, cadence/steps, power/access evidence, weights and registration digests. Independently verify each registered same-window baseline. Phase 66's reader hardcodes "[\"input\", \"h1\"]" and full-window "E_CONST_PREDICTED" values, so do not reuse its scientific reader for ladders. [VERIFIED: pinn/verification/diagnostic_phase66.py:111-115,640-658] Apply the affected-use conditions for malformed evidence, contained paths, time monotonicity and endpoint types; preserve recorded historical bytes while pinning changed dependencies in new registrations. [VERIFIED: .planning/phases/65-probe-on-the-record-fit-harness/65-CLOSEOUT.md:68-91; .planning/phases/66-small-network-control/66-REVIEW.md:48-111]

## Don't Hand-Roll

Use the frozen scorer and comparison functions, current SIREN/COM layer construction, shared similarity measurement, retained normalizer, TRAIN-only reader, committed-registration guard and power launcher. Do not duplicate these contracts or introduce a trainer, scoring implementation, normalizer or Fourier library. [VERIFIED: pinn/verification/diagnostic_fit.py:72-99; pinn/verification/diagnostic_variants.py:203-223; .planning/phases/67-design-settings-ladders/67-CONTEXT.md:124-147]

## Common Pitfalls

The implementation risks are external preprocessing that breaks the scorer's raw-input derivatives, frequency numbers that describe only the raw tau column, average-period endpoints mislabeled as actual laps, global time rescaling on prefixes, unchanged EXP-01 layer/baseline assumptions, and score-dependent budget extensions. The corresponding safeguards are specified above. [VERIFIED: pinn/verification/feasibility_scorer.py:355-420; pinn/verification/diagnostic_similarity.py:224-227; pinn/verification/stage0_census.py:131-181; pinn/verification/diagnostic_data.py:446-459,550-555; pinn/verification/diagnostic_phase66.py:640-658; .planning/phases/67-design-settings-ladders/67-CONTEXT.md:99-120]

## Code Examples

Proposed transform pseudocode: `phase = pi * registered_N_in * (raw_tau + 1); encoded = concatenate(raw_tau, raw_IC13, sin(k*phase), cos(k*phase) for k in registered_harmonics); return unchanged_COM_projection(backbone(encoded), raw_masses)`. Keep constants as persistent buffers. This is a design sketch under D-05, not an existing API or verified implementation. Verify analytic first/second time derivatives and the frozen scorer path on synthetic data before real use. [VERIFIED: .planning/phases/67-design-settings-ladders/67-CONTEXT.md:66-75,133-139] [CITED: https://docs.pytorch.org/docs/2.12/generated/torch.nn.Module.html#torch.nn.Module.register_buffer]

## Validation Architecture

Use existing standard-library unittest infrastructure, not pytest. The established interpreter is documented as "<home>/miniforge3/envs/pinn-train/bin/python -B". [VERIFIED: tests/phase66/test_budget.py:15-23; .planning/phases/65-probe-on-the-record-fit-harness/65-CLOSEOUT.md:93-105] In the proposed commands below, `P` denotes that interpreter with `-B`.

| Requirement | Proposed synthetic coverage | Proposed quick command |
|---|---|---|
| EXP-02 | Exact depth catalog, locked parity, parameter counts and all layer rows | `P -m unittest tests.phase67.test_catalog` |
| EXP-03 | Exact rates, equal-update cost-only budget, refused unregistered continuation | `P -m unittest tests.phase67.test_budget` |
| EXP-04 | Encoded dimensions, persistent buffers, raw signature, analytic/Jacobian derivatives, COM, hook cleanup and applicability | `P -m unittest tests.phase67.test_time_features` |
| EXP-05 | Signed first-crossing brackets, exact inclusion, unreached-lap refusal, retained tau and recomputed same-window scores | `P -m unittest tests.phase67.test_windows` |
| Shared scope | Pre-open TRAIN-only refusal, diagnostic isolation, malformed reader evidence, registration/power/deadline and historical bytes | `P -m unittest tests.phase67.test_records tests.phase67.test_isolation` |

Wave 0 must create these proposed tests and shared synthetic fixtures before reliance on the new paths. Keep targeted checks below 30 seconds where practical; split expensive numerical cases. Per task run its targeted module; per wave run `P -m unittest discover -s tests/phase67 -t .`; at the phase gate also run the existing Phase 65 and Phase 66 discovery suites, check frozen artifact/history digests and `git diff --check`. Those suites use fixtures rather than authorize corpus work. Existing precedent is explicit about synthetic isolation. [VERIFIED: .planning/phases/66-small-network-control/66-REVIEW.md:42-46] Real timing/science acceptance is a separate registered weekend execution task, never part of ordinary unit tests.

## Environment Availability

The existing pinn-train interpreter imports the locked scientific packages and reports MPS available; no install is needed. This import-only probe did not execute a training or corpus operation. AC/weekend eligibility was not probed and must be checked at execution. Existing power constants are "AC Power", "America/Chicago", and "WINDOW_SUNDAY_LAST_HOUR = 22"; reuse that launcher. [VERIFIED: environment probe, 2026-11-01; pinn/verification/diagnostic_power.py:56-70] Under-hour execution needs no unproved resume compatibility; keep the current refusal until that separate work is authorized. [VERIFIED: pinn/verification/diagnostic_fit.py:132-134]

## Security Domain

For this local diagnostic phase, the template's authentication/session categories V2/V3 are inapplicable; V4 access control and V5 input validation apply to TRAIN-only admission, contained artifact paths and hostile/malformed JSON; V6 cryptography applies only to existing digest provenance, with no new cryptographic design. Preserve fixed-argv subprocesses, exclusive evidence creation and diagnostic-marker rejection. This is a threat-applicability assessment, not an ASVS compliance certification. [VERIFIED: .planning/REQUIREMENTS.md:180-184; .planning/phases/66-small-network-control/66-REVIEW.md:42-48; .planning/phases/65-probe-on-the-record-fit-harness/65-CLOSEOUT.md:72-78]

## Assumptions Log

No unverified compatibility or optimality claim is required. Harmonic sufficiency, improved fit and similarity/accuracy association remain hypotheses to test. The prospective numerical design choices above are made under D-01/D-04..10 and must be committed before timing; they are not owner facts or locked FEAS bars. [VERIFIED: .planning/phases/67-design-settings-ladders/67-CONTEXT.md:33-37,60-120]

## Open Questions

Exact per-arm durations, common update counts, sampled lap endpoints and complete machine-hour estimates remain execution-time measurements under the stated registered algorithms. They do not block implementation planning. No new owner-only decision was identified; an unexpected scientific branch or scope/resource change must return through SCOPE-47/49. [VERIFIED: .planning/REQUIREMENTS.md:182-194]

## Sources and Metadata

Primary sources are the opened, line-cited context, requirements, harness/scorer/census sources and Phase 65/66 reuse records above. The only external API checks used version-matched official [PyTorch Module](https://docs.pytorch.org/docs/2.12/generated/torch.nn.Module.html#torch.nn.Module.register_buffer) and [torch.func](https://docs.pytorch.org/docs/2.12/func.html) documentation. The research-plan seam requested Context7; neither its MCP tool nor CLI was available, so official web documentation was the fallback. `classify-confidence --provider websearch --verified` returned MEDIUM, and its digest was cached. [VERIFIED: research-plan/classify-confidence/research-store tool results, 2026-11-01]

Repository contracts have HIGH confidence; prospective designs and external API guidance have MEDIUM confidence pending synthetic verification. Recheck after any harness change. No new package recommendations, production redesign, corpus probe, real timing or training are included.
