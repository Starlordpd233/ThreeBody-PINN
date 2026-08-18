# Phase 46: Frame Resolution & Gate-Aligned Validation - Context

**Gathered:** 2026-07-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 46 delivers exactly two v2.2 requirements, in dependency order:

1. **CONF-01 / RG-02:** settle whether the exact stored positions consumed as
   training targets are raw positions or the locked physics-frame targets
   `r' = r/D`, using a train-free residual-on-stored-targets check. The
   evidence and verdict are recorded; no training run is permitted for this
   decision.
2. **INST-01:** after CONF-01 establishes a coherent position/time frame, add
   per-trajectory validation `epsilon_H`/SCS observations by composing the
   existing `pinn.verification.gate_metrics` functions. The observations are
   persisted per run and establish EVAL-01 precondition (iii); they never
   influence optimization.

This is a conformance-and-instrumentation phase, not a recipe experiment. It
does not tune hyperparameters, change the validation cadence, edit framework
specs, run Stage-0 training to answer RG-02, inspect the held-out test split,
invoke `pinn.evaluate`, or spend the one authorized held-out evaluation.

The phase has a mandatory branch. If CONF-01 proves the target frame wrong, or
if the evidence cannot ground a unique verdict, all frame-dependent work stops.
The finding is recorded in `46-GAPS.md` and `.planning/milestones/v2.2-GAPS.md`,
and the roadmap's owner scope decision is surfaced. A target-frame repair or
other data-path repair must never be absorbed silently into Phase 46.

</domain>

<decisions>
## Implementation Decisions

Discussion ran with all areas enabled and owner-delegated automatic selection.
The recommended default was selected for every discussion area. The complete
question/alternative/answer record is in `46-DISCUSSION-LOG.md`.

### CONF-01: stored-target frame probe

- **D-01 — Probe the exact model-facing surface.** The primary operand is every
  trajectory exposed by the train/validation `StageIndex.snapshot_positions`
  seam that `pinn.data.batches.sample_data_points` samples into `targets`.
  Parsed corpus arrays and the output of `preprocess_trajectory` are provenance
  and positive-control arms; neither code inspection nor a raw-file-only check
  may substitute for the residual evidence over the resident target surface.

- **D-02 — Cover the complete eligible population deterministically.** Run the
  probe over every Stage-0 identity in the frozen train and validation split
  views, sorted by canonical `RecordKey`. Record split membership and counts.
  The test split is excluded absolutely. No random sample, undocumented panel,
  or held-out preview may decide RG-02.

- **D-03 — Use symmetric raw/scaled hypotheses.** Evaluate the same resident
  positions, times, identities, and mass metadata under both locked
  interpretations:
  - the target is already in physics coordinates `r'`, paired with normalized
    time `u=t/T`; and
  - the target is raw `r`, requiring the locked raw-to-physics transformation
    before the same dimensionless residual is evaluated.
  Report both arms without privileging one in code. The fully preprocessed
  ordered/gauged/scaled trajectory is the positive control; parsed raw
  positions with their matching raw metadata are the provenance control.
  Every arm must make its coordinate, time, mass-order, COM/boost, rotation,
  and scale convention explicit in the artifact.

- **D-04 — Distinguish scale from other data-path divergences.** Current code
  inspection shows that preprocessing computes ordered/gauged/scaled
  trajectories while adapter residency appears to retain parsed positions.
  This observation motivates the probe but is not the verdict. The probe must
  include controls that can distinguish a pure `D`-scaling mismatch from body
  permutation, COM/boost, rotation-gauge, or metadata-pairing mismatches. If a
  non-frame mismatch prevents a clean raw-versus-scaled conclusion, preserve
  it as a data-path finding and route it through the same owner branch; do not
  reinterpret it as noise or repair it inline.

- **D-05 — Evidence is population-level and re-derivable.** Commit a versioned
  machine-readable evidence artifact plus a concise Markdown rendering under
  the Phase 46 evidence tree. Record the repository commit, data/split
  identities and hashes, locked `D`/`T` values, dtype/device, arm definitions,
  trajectory counts, excluded-snapshot reasons, per-trajectory measures, and
  aggregate distributions. Stable key ordering and deterministic serialization
  are required.

- **D-06 — Do not invent a new physics threshold.** A grounded verdict requires
  finite, reproducible, theory-consistent separation between the symmetric
  hypotheses and agreement with the appropriate control arm. Numerical
  comparison tolerances may be derived from the represented dtype/round-trip
  error and must be reported separately from any physics acceptance threshold.
  Do not promote Phase 38's one-fixture residual threshold, a lower mean, or an
  ad hoc ratio into a new target-frame lock. Ambiguous, non-finite, or
  train/validation-inconsistent evidence fails closed into the governed gap
  path.

### CONF-01 branch handling

- **D-07 — CONF-01 precedes INST-01.** First produce and record the target-frame
  verdict. Validation instrumentation may be planned alongside the probe, but
  no implementation detail may bake in a coordinate assumption until the
  verdict is grounded.

- **D-08 — Conformant branch.** If the exact target surface is confirmed to
  satisfy the locked ordered/gauged/scaled contract, record the clean verdict
  and evidence, make no data-path rewrite "for clarity," and proceed with
  INST-01 in the confirmed frame.

- **D-09 — Defect or ambiguity branch.** If the surface is confirmed wrong,
  record the sixth conformance divergence as a data-path defect and stop. If
  the evidence is ambiguous, record the unresolved semantic decision and stop.
  In either case, create the phase-local gap and the v2.2 milestone index entry
  with the full engineering grounding required by `AGENTS.md`, then surface
  the roadmap-mandated owner scope decision. Phase 47 and any dependent part of
  Phase 46 remain blocked until the owner resolves or defers it.

### INST-01: validation metric cadence and isolation

- **D-10 — Reuse the existing validation cadence.** Compute the conservation
  observation at each already-scheduled validation event. Add no new cadence
  option and do not alter the existing schedule. The loss-validation batch
  remains whatever the current controller uses; the conservation observation
  is a separate deterministic pass.

- **D-11 — Evaluate the complete current-stage validation pool.** For a
  validation event at stage `k`, traverse
  `validation_source.records_at_or_below(k)` in sorted `RecordKey` order.
  Do not reuse the random validation-loss batch and do not create an
  undocumented fixed panel. Preserve the canonical identity of every
  trajectory in the per-event artifact.

- **D-12 — Compose existing gate functions in a coherent frame.** Use a
  detached `model.eval()` / `torch.no_grad()` full-trajectory forward pass,
  restore the model's prior train/eval state, and pass the resulting position
  series, ordered raw masses, and matching monotone time coordinate to
  `pinn.verification.gate_metrics`. Under the locked scaled contract the
  coherent pair is `r'` with `u=t/T`, so finite-difference velocity is
  `dr'/du`; any alternate pair must be the explicit consequence of the
  CONF-01 owner-ratified branch. Do not duplicate Hamiltonian, finite
  difference, aggregation, SCS, or verdict formulas in training code.

- **D-13 — Keep component math closed.** Phase 46 integrates the already
  verified gate-metric functions; it does not re-audit or rewrite their
  component math. If planning exposes an actual conflict between an existing
  caller contract and the locked `r'`/`u` specification, surface that conflict
  as a governed gap rather than silently changing the held-out evaluator or
  redefining the metric.

- **D-14 — Persist per-trajectory metrics; headline the worst case.** Record
  `epsilon_H` and diagnostic SCS for every validation trajectory. Derive the
  aggregate headline from the owner-ratified worst-trajectory maximum and
  derive aggregate SCS from that single value. Means, medians, quantiles, and
  failure fractions may appear only as clearly labeled descriptive
  diagnostics; they never replace or compete with the maximum.

- **D-15 — Observation only.** Validation conservation metrics may not alter
  any loss or weight, stage-exit state, optimizer/scheduler state, replay
  selection, checkpoint rank, early stopping, recipe value, or control flow
  other than failing closed when the required instrumentation itself cannot
  produce durable evidence. A numeric PASS/FAIL is an honest observation, not
  a training-control signal.

- **D-16 — Enforce held-out isolation structurally.** The instrumentation
  receives only the validation `StageIndex`, never constructs or reads a test
  `StageIndex`, and never calls or imports `pinn.evaluate`. Tests must prove
  these prohibitions. No Phase 46 command may create a held-out evaluation
  receipt or consume the EVAL-01 budget.

### Persistence and failure semantics

- **D-17 — Sidecar plus compact event record.** At each validation event, write
  one atomic, versioned sidecar containing the complete per-trajectory
  evidence. Append only compact aggregate fields and a run-relative sidecar
  pointer to the existing `validation.jsonl` event. Never inline the full
  population into JSONL and never persist aggregates without their identity-
  preserving sidecar.

- **D-18 — Required sidecar schema.** Each sidecar records at least: schema
  version, run-relative identity, global step, stage, `split="validation"`,
  confirmed frame and CONF-01 evidence reference, position/time convention,
  trajectory count, sorted `RecordKey` identity plus `epsilon_H` and SCS for
  every trajectory, non-finite count, gate thresholds, worst-case aggregate
  `epsilon_H`, aggregate SCS, and diagnostic PASS/FAIL. JSON must represent
  non-finite values safely and unambiguously rather than emitting non-standard
  numeric tokens or dropping records.

- **D-19 — Make EVAL-01 precondition (iii) inspectable.** Project the latest
  successfully persisted validation aggregate and its run-relative sidecar
  pointer into the terminal run summary, tied to the exact validation step and
  model state. A run with no durable, schema-valid validation-gate record is
  explicitly ineligible for held-out evaluation; console output or the mere
  existence of `validation.jsonl` is insufficient.

- **D-20 — Fail closed without turning metrics into tuning.** An empty eligible
  pool, computation error, schema error, or sidecar/JSONL persistence failure
  makes the required instrumentation incomplete and the run ineligible; it
  must not silently fall back to loss-only validation. A genuinely computed
  non-finite `epsilon_H` is instead retained as numeric evidence with FAIL
  status. It remains observation-only and does not authorize recipe changes.

### Regression coverage

- **D-21 — Frame-probe tests.** Use synthetic trajectories encoded once as raw
  positions and once as locked processed/scaled targets with the same `D`/`T`.
  Assert that the symmetric analysis identifies the corresponding arm and that
  canonical preprocessing is the positive control. Separately test stable key
  ordering, train/validation inclusion, test exclusion, mismatched
  body-order/metadata controls, and ambiguous/non-finite fail-closed behavior.

- **D-22 — Gate composition tests.** Extend the established Phase 43
  boundary/non-finite fixtures and add a small multi-trajectory validation
  integration seam. Assert per-trajectory `epsilon_H`/SCS, strict threshold
  direction, worst-case aggregation, aggregate SCS derivation, sorted identity,
  the coherent position/time pair, and reuse of the existing gate functions.

- **D-23 — Isolation and non-interference tests.** Prove that the helper sees
  validation only, never imports/calls the held-out evaluator, restores the
  prior model mode even on error, and leaves the loss, optimizer, scheduler,
  curriculum/stage-exit, replay, checkpoint, and early-stop decisions
  unchanged.

- **D-24 — Artifact tests stay dataset-free.** Test atomic sidecar publication,
  schema validation, JSON-safe non-finite encoding, compact
  `validation.jsonl` linkage, terminal-summary projection, and fail-closed
  empty/missing/corrupt cases using synthetic sources. The real corpus is used
  once for the committed CONF-01 evidence run, not as a standing test-suite
  dependency.

### Governance and scope locks

- **D-25 — v2.2 boundaries remain hard.** SCOPE-27..32 apply throughout:
  Stage-0-only authorization does not authorize a probe training run; exactly
  one held-out evaluation remains unspent; iteration is conformance-only; no
  framework-spec file is edited; the trainex-r2 report is not grounding; and
  Phase 46 implements only the minimum validation instrumentation it owns.

- **D-26 — Verified-clean math is not reopened.** The conformance audit's
  verified-clean component section is load-bearing. Phase 46 investigates the
  assembly/data-frame seam and adds validation wiring; it does not use that
  scope to re-litigate force, Hamiltonian, projection, AD, or gate formula
  math.

### Agent's Discretion

The planner may choose focused helper/module names, evidence filenames,
sidecar directory layout, batching/chunking used to keep the deterministic
full-validation pass practical, and which descriptive distribution fields to
include. Those choices must preserve every decision above, add no dependency,
and not create a new cadence, threshold, tuning signal, or evaluator path.

</decisions>

<canonical_refs>
## Canonical References

**Downstream researchers, planners, executors, and reviewers MUST read these
before planning or implementing.**

### Phase scope and owner-ratified boundaries

- `.planning/ROADMAP.md` — Phase 46 goal, success criteria, strict dependency
  order, and the frame-defect owner checkpoint.
- `.planning/REQUIREMENTS.md` — CONF-01, INST-01, EVAL-01, the grounding-source
  hierarchy, and SCOPE-27..32.
- `.planning/PROJECT.md` — active v2.2 milestone, evaluation policy, branch
  timing, and inherited v2.1 obligations.
- `docs/work/designs/cross_cutting/v2.2-milestone-proposal/2026-07-25-v2.2-roadmap-proposal.md`
  — owner-ratified source consumed by milestone initialization.
- `AGENTS.md` — STOP/gap protocol, Git policy, and source-of-truth rules.

### Grounding and inherited diagnosis

- `.planning/milestones/v2.1-GAPS.md` — v2.1 owner rulings and obligations
  inherited by v2.2.
- `.planning/milestones/v2.1-phases/44-physics-gate-forensics/44-ERRATUM.md`
  — qualification of the earlier diagnosis after the conformance audit.
- `.planning/milestones/v2.1-phases/44-physics-gate-forensics/44-DIAGNOSIS.md`
  — retained evidence context only, subject to the erratum and v2.2 source
  precedence.
- `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-24-stage0-training-path-conformance-audit.md`
  — C-01..C-08 inventory plus the equally binding verified-clean section.

### Locked coordinate, preprocessing, and metric contracts

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` —
  one shared COM/boost/order/gauge/scale convention for ICs, BRUTUS targets,
  and model references; `r_true_prime_ordered_gauge`; `u=t/T`; target and
  evaluation contracts.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
  — Huber data loss on projected scaled positions, the normalized-time AD
  contract, and Hamiltonian/conservation component contracts.
- `simulation_data/Documentation/README.md` — canonical dataset layout and
  anomaly record used to resolve real-corpus identities.

### Verified implementation precedent

- `.planning/milestones/v2.0-phases/38-pinn-model-rebuild-from-specs-fut-01/38-VERIFICATION.md`
  — the existing residual-probe evidence precedent; not authority for a new
  CONF-01 threshold.
- `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-CONTEXT.md`
  — locked gate direction, split isolation, evidence, and summary patterns.
- `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-VERIFICATION.md`
  — verified gate-metric and held-out-evaluator behavior to reuse without
  reopening component math.

### Explicitly excluded source

- `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/` is **not**
  a Phase 46 grounding source (SCOPE-31). Do not consult its tuning analysis or
  use its returned report to select behavior.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable assets

- `pinn/data/preprocessing.py::preprocess_trajectory` already implements the
  full raw-to-physics transform and returns ordered/gauged/scaled `r_gauge`,
  `v_gauge`, ordered masses, and the locked `D`/`T`. It is the positive-control
  transform for CONF-01, not a substitute for probing the resident targets.
- `pinn/verification/residual_probe.py` already establishes the dimensionless
  residual-evidence pattern (`r/D`, `u=t/T`, `v*T/D`), deterministic evidence
  serialization, and the force-versus-finite-difference seam. Phase 46 should
  extract/reuse the smallest suitable computation seam rather than duplicate
  physics formulas, while avoiding promotion of its one-fixture threshold.
- `pinn/verification/gate_metrics.py` already owns finite-difference velocity,
  matched-Plummer Hamiltonian, per-trajectory `epsilon_H`, worst-case
  aggregation, SCS derivation, and strict-boundary PASS/FAIL. INST-01 composes
  these functions.
- `pinn/data/splits.py::StageIndex` provides split-restricted, deterministically
  ordered records and the full-trajectory accessors needed by both strands.
- `pinn/training/summary.py` and the existing `validation.jsonl` producer in
  `pinn/train.py` provide the render-don't-recompute and terminal-summary
  projection patterns.

### Load-bearing seams

- In `pinn/data/adapter.py`, admission calls `preprocess_trajectory` and builds
  IC13/ordered mass metadata from the processed result, while the current
  candidate/residency path stores `parsed_brutus.positions` and
  `parsed_brutus.velocities` in `_trajectory_tensors`.
- In `pinn/data/batches.py`, `sample_data_points` reads
  `snapshot_positions` and copies selected values directly into model-facing
  `targets`, while time is separately normalized into the network coordinate.
  This exact boundary is why CONF-01 must use measured evidence rather than a
  code-only conclusion.
- `pinn/training/controllers.py::_run_validation` currently samples a loss
  batch and restores model mode in `finally`. Conservation observation should
  be a separate deterministic full-validation pass at the same event boundary,
  preserving that restoration guarantee.
- `pinn/train.py` currently appends only `step`, `final_val_loss`, and `trend`
  to `validation.jsonl`; `pinn/training/summary.py` projects the latest record.
  INST-01 extends this persistence chain with compact aggregate/pointer fields,
  not a parallel summary source.
- `pinn/evaluate.py` is held-out-only and out of bounds for Phase 46. It may be
  read for artifact-pattern precedent but must not be invoked, imported by the
  validation path, or modified opportunistically.

### Established test style

- Phase-scoped tests use stdlib `unittest`, synthetic duck-typed
  `StageIndex`-like sources, and dataset-free fixtures.
- Phase 43 gate tests already cover non-finite handling, worst-case
  aggregation, SCS derivation, and the exact strict reject boundary; extend
  those fixtures instead of creating a competing metric oracle.
- Existing controller tests assert model-mode restoration after validation
  failure; preserve and extend that behavior.

</code_context>

<specifics>
## Specific Ideas

- The CONF-01 artifact should make the two hypothesis columns visually
  symmetric and render the raw/preprocessed controls beside them. The report
  should lead with what was measured and the resulting branch, not with the
  source-code suspicion.
- Record an explicit coordinate tuple for every calculation, for example
  `{position: r_prime, time: u, velocity: dr_prime_du, masses: ordered_raw}`.
  This prevents a numerically plausible result assembled from incoherent units.
- Keep the validation JSONL line small enough to remain a useful event stream:
  headline aggregate, count/status, schema version, and sidecar pointer belong
  inline; the sorted per-trajectory table belongs in the sidecar.
- Sidecar publication must be atomic before its pointer is appended. A JSONL
  record must never advertise a sidecar that was not durably published.
- Preserve a distinction between **instrumentation failure** (missing/invalid
  evidence; run ineligible) and **metric FAIL** (valid evidence whose
  `epsilon_H` misses the gate; run still honestly characterized, with no
  automatic tuning response).

</specifics>

<deferred>
## Deferred Ideas

- Any target/data-path repair identified by CONF-01 — mandatory owner scope
  branch before implementation.
- `S_H`, `epsilon_H = 1e-4 * S_H`, and the loss-math repairs — Phases 47–48,
  after the frame is settled.
- General conformance-enforcement regime, placeholder census, known-divergence
  register, and runtime invariants — Phase 49 / concurrent charter workstream.
- Stage-0 training, three-seed rerun, and the single held-out evaluation —
  Phases 50–51.
- Recipe tuning or trainex-r2 remedy adjudication — v2.3 (SCOPE-29/31).
- Framework-spec prose amendments — VER-20 handoff, not a v2.2 edit.

### Reviewed Todo (not folded)

- **`d-06-static-epsilon-sensitivity-check`** matched the phase scout, but
  `.planning/REQUIREMENTS.md` explicitly leaves both carried-forward todos
  unlinked to v2.2. It remains pending and is not folded into CONF-01 or
  INST-01; doing so would expand the owner-ratified scope and introduce a
  separate sensitivity question.

</deferred>

---

*Phase: 46-frame-resolution-gate-aligned-validation*
*Context gathered: 2026-07-25*
