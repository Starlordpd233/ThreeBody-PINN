# Phase 39 Gap Register

## GAP-39-01 — Authoritative `data_version_hash` producer

- **Decision point:** Define the authoritative producer, serialization location,
  and generation algorithm for `data_version_hash`. Phase 39 can compare an
  expected value with supplied metadata, but cannot manufacture authoritative
  metadata without this decision.
- **Where in artifact:** `39-SPEC.md` DATA-03 and `39-CONTEXT.md` D-05.
- **Task context:** Recording implementation decisions for the DATA-03
  compare-and-refuse seam.
- **Classification:** operational coordination.
- **Source silence:**
  - `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/trainex-r1a-resolution-doc.md:153`
    explicitly leaves the production mechanism open (U-12) while requiring the
    adapter to implement compare-and-refuse only.
  - `.planning/REQUIREMENTS.md` DATA-03 requires mismatch refusal but does not
    designate a producer, canonical payload, or metadata location.
  - `39-SPEC.md` DATA-03 locks a typed `DataVersionHashDeferred` outcome for an
    absent field; it deliberately does not invent the missing producer.
- **Mathematical / engineering grounding:** Version comparison is meaningful
  only when both sides derive from the same stable identity function over the
  same corpus/metadata scope. A locally chosen file-order or text-format hash
  could change for non-semantic formatting differences, or fail to change for a
  semantic change outside its chosen payload. A hard mismatch refusal therefore
  needs a ratified producer; the typed deferral keeps the unverified state
  observable without falsely claiming compatibility.
- **Agent was tempted to:** Generate a local manifest or file-content hash so
  the compare path always has a value. This would silently choose scope,
  ordering, normalization, and storage semantics that the sources reserve.
- **What the user needs to decide:**
  - **A.** Designate the authoritative data producer, canonical payload, and
    metadata location for `data_version_hash`.
  - **B.** Explicitly retain the typed absent-field deferral until the upstream
    PIPE contract is supplied.
  - **C.** Supply a specific owner-maintained sidecar/manifest contract to use
    as the canonical source.
- **Confidence of impact:** HIGH — an unratified hash can make the safety check
  either spuriously reject unchanged data or silently accept incompatible data.
- **Status:** DEFERRED — non-blocking for the locked compare/refuse plus typed
  deferral seam. It blocks a claim of mandatory version enforcement where the
  metadata field is absent.
- **Resolution note:** User instruction, 2026-07-13: “follow your best
  judgement.” Agent judgment chooses option B: retain the typed absent-field
  deferral and do not invent a producer, payload, or sidecar contract in Phase
  39. Revisit only when an upstream canonical producer is ratified.

## GAP-39-02 — DATA-01 single-reader rule versus Phase 38 fixture loader

- **Decision point:** Resolve whether DATA-01's requirement that the new
  adapter is the only `pinn/` component reading the on-disk `.txt` format
  includes the pre-existing Phase 38 verification fixture loader.
- **Where in artifact:** `39-SPEC.md:28-30` and `:89`; `39-CONTEXT.md` D-02.
- **Task context:** Validating the DATA-01 implementation boundary before
  planning the new adapter.
- **Classification:** cross-phase reframing.
- **Source silence:**
  - `39-SPEC.md:28-30` calls the new adapter the sole `.txt` importer, and
    `:89` makes that a grep-verified acceptance criterion; it does not name an
    exception or migration for `pinn/verification/fixture_loader.py`.
  - `pinn/verification/fixture_loader.py:12-16,235-237,300-323` resolves and
    parses Brutus/IC `.txt` files through direct reads, and its module contract
    says it is deliberately not the Phase 39 adapter.
  - `tests/phase38/test_prohibitions.py:48-60,158-160,254-258` treats that
    fixture loader as a Phase 38 module and actively consumes it in retained
    verification coverage. Neither the roadmap nor requirements specifies
    whether it must be exempted, migrated, or replaced.
- **Mathematical / engineering grounding:** The sole-reader rule prevents two
  production parsers from diverging on record identity, completeness, and
  numerical interpretation. The existing loader instead supplies evidence
  probes and has a separately tested read-only contract. Narrowing the rule to
  the production ingestion surface preserves the probe; migrating or delegating
  the probe changes its provenance and Phase 38 regression surface. These are
  materially different system boundaries and cannot be inferred from a grep
  phrase.
- **Agent was tempted to:** Exempt the loader by narrowing the grep to new
  Phase 39 modules. That is plausible but changes the universal requirement.
  Alternatively, making the loader delegate to the adapter would modify a
  completed Phase 38 artifact and expand Phase 39's scope.
- **What the user needs to decide:**
  - **A.** Narrow DATA-01 to the production ingestion surface and explicitly
    exempt the Phase 38 probe-local fixture loader from the single-reader grep.
  - **B.** Require the fixture loader to delegate parsing to the Phase 39
    adapter, with Phase 38 regression coverage included in scope.
  - **C.** Retire/replace the fixture loader and define a new verification
    boundary, accepting the corresponding Phase 38 scope change.
- **Confidence of impact:** HIGH — without a ruling, no implementation can both
  preserve the existing Phase 38 probe contract and satisfy the stated
  repository-wide grep criterion.
- **Status:** RESOLVED-WITH-INSTRUCTION — no longer blocks DATA-01 planning.
- **Resolution note:** User instruction, 2026-07-13: “follow your best
  judgement.” Agent judgment chooses option A: the DATA-01 single-reader rule
  applies to the production ingestion surface. Preserve
  `pinn/verification/fixture_loader.py` as the sole existing, probe-local Phase
  38 exception; it is neither the admitted-set adapter nor a reusable production
  parser. The Phase 39 reader audit must allow that exact module and fail on any
  other non-adapter on-disk reader.

## GAP-39-03 — Reversed Stage-0 `s_min` predicate in the phase SPEC

- **Decision point:** Resolve the contradiction between the derived Phase 39
  SPEC, which assigns `s_min > s0` to Stage 1 and equality to Stage 0, and the
  authoritative CTL contract, which requires `s_min > s0` for Stage 0.
- **Where in artifact:** `39-SPEC.md:53-56,104-106`; `39-RESEARCH.md` DATA-06
  source-conflict finding.
- **Task context:** Researching the DATA-06 classifier and fatal Stage-0
  population count before generating executable plans.
- **Classification:** cross-phase reframing / build-discovered spec defect.
- **Source conflict:**
  - `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:138-150`
    defines Stage 0 with `s_min > s0`; its Stage 1a/1b criteria at `:155-184`
    also require `s_min > s0` alongside different energy/angular-momentum
    predicates.
  - `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/CLEARANCE.md:23`
    records the owner-ratified PB-1 repair as `s_min > s0`, with interim
    `s0 = 0.01` pending the DATA-06 scan.
  - `.planning/REQUIREMENTS.md:126` (SCOPE-18) makes the framework specs
    authoritative for the v2.0 build and requires a build-discovered spec
    defect to be surfaced rather than implemented.
  - `39-SPEC.md:53-56,104-106` reverses that predicate by labeling
    `s_min > s0` as Stage 1 and placing equality in Stage 0.
- **Mathematical / engineering grounding:** The Stage-0 count is the number of
  admitted trajectories satisfying the conjunction of the Stage-0 invariant
  predicates. Reversing one predicate changes set membership and can invert the
  below-240 fatal-class decision. At the exact boundary, strict `>` excludes
  equality from Stage 0; assigning equality to Stage 0 would violate the
  authoritative predicate and make the report disagree with the trainer's
  curriculum contract.
- **Agent was tempted to:** Preserve the phase SPEC literally so its acceptance
  wording and implementation matched. That would knowingly implement a
  derived-artifact defect against the read-only authoritative CTL contract.
- **What the user needs to decide:**
  - **A.** Follow the authoritative CTL predicate for planning and execution;
    record the derived phase-SPEC wording as a routed spec defect.
  - **B.** Override the CTL and integrity clearance with the reversed phase-SPEC
    predicate.
  - **C.** Block all DATA-06 planning until a separate spec milestone republishes
    the derived Phase 39 SPEC.
- **Confidence of impact:** HIGH — this predicate directly determines the
  Stage-0 population and whether Phase 39 emits a fatal-class signal.
- **Status:** RESOLVED-WITH-INSTRUCTION — no longer blocks DATA-06 planning.
- **Resolution note:** The user's 2026-07-13 full-autonomy instruction requires
  the work to continue without an interactive ruling. Source precedence makes
  option A the only SCOPE-18-compliant resolution: plans and implementation must
  use the CTL Stage-0 conjunction with strict `s_min > s0`; equality is not
  Stage 0. Do not edit the authoritative framework specs in v2.0. Keep the
  contradictory `39-SPEC.md` wording visible as the routed build-discovered
  spec defect, and make every DATA-06 plan cite this gap plus the CTL lines.

## GAP-39-04 — Numerically near-zero `H(0)` predicate

- **Decision point:** Define the numerical quarantine predicate for an initial
  energy that is too close to zero for the relative conservation drift to be
  meaningful, without adding a denominator floor.
- **Where in artifact:** `ctl_instruction.md:560-580`; `39-SPEC.md` DATA-02;
  `39-RESEARCH.md` Open Question 1.
- **Task context:** Converting Step-1A's qualitative near-zero-energy rule into
  an executable and boundary-testable admission plan.
- **Classification:** semantic implementation threshold.
- **Source silence:** The CTL requires float64 energy, Plummer softening
  `eps=1e-10`, quarantine of numerically near-zero `H(0)`, and no denominator
  floor, but no source gives an absolute, relative, or scale-aware threshold.
  The force-law softening constant is not an energy-zero tolerance.
- **Mathematical / engineering grounding:** Floating-point cancellation error in
  `H0 = K0 + V0` scales with `|K0| + |V0|`; an absolute threshold is unit
  dependent. A scale-aware comparison against float64 machine epsilon preserves
  uniform energy scaling while quarantining values whose sign and relative
  drift are not numerically resolved.
- **Agent was tempted to:** Reuse `1e-10` because it already appears in the
  energy formula. That would conflate a length softening with an energy
  cancellation tolerance.
- **What the user needs to decide:**
  - **A.** Use a scale-aware float64 cancellation predicate with an explicit
    reversible safety factor.
  - **B.** Choose an absolute energy threshold and its units.
  - **C.** Quarantine only exact zero and accept unresolved near-zero ratios.
- **Confidence of impact:** MEDIUM — the current corpus has a wide safety
  margin, but synthetic and future data need deterministic boundary behavior.
- **Status:** RESOLVED-WITH-INSTRUCTION — no longer blocks DATA-02 planning.
- **Resolution note:** Under the user's full-autonomy instruction, choose option
  A: quarantine when `H0 == 0.0` or, for `scale = |K0| + |V0| > 0`,
  `|H0| <= 64 * finfo(float64).eps * scale`. Treat `64` as a reversible
  implementation safety factor, not source authority. Tests must cover exact
  zero, the boundary, `nextafter` immediately above it, a small but resolved
  value, absence of denominator floors, and the real-corpus quarantine count.

## GAP-39-05 — Disposition after non-finite snapshot removal

- **Decision point:** Decide whether a trajectory containing a non-finite
  snapshot block may be admitted after that block is dropped and the remaining
  blocks still satisfy shape, finiteness, and monotonicity checks.
- **Where in artifact:** `ctl_instruction.md:539-561`; `.planning/REQUIREMENTS.md`
  DATA-02; `39-SPEC.md` DATA-02; `39-RESEARCH.md` Open Question 2.
- **Task context:** Making dropped-sample accounting and trajectory disposition
  mutually consistent in the admission plan.
- **Classification:** semantic admission policy.
- **Source silence:** Requirements demand both an all-finite structural gate
  and logged dropping/counting of NaN/Inf samples, but no source explicitly
  authorizes or forbids trajectory salvage after removal.
- **Mathematical / engineering grounding:** Removing a corrupt snapshot can
  delete the worst conservation event and make a damaged trajectory appear
  admissible. Counting the dropped block separately preserves diagnostics;
  quarantining the trajectory preserves the fail-closed all-finite contract.
- **Agent was tempted to:** Admit the remaining blocks whenever at least two
  finite monotone snapshots survive. That optimizes retention at the cost of a
  silent scientific-selection bias.
- **What the user needs to decide:**
  - **A.** Count/drop the corrupt block but quarantine the whole trajectory.
  - **B.** Salvage and admit after the remaining blocks pass every gate.
  - **C.** Reject the trajectory without retaining dropped-sample accounting.
- **Confidence of impact:** HIGH — salvage can alter conservation and stage
  statistics even though the verified corpus currently contains no NaN/Inf
  numeric tokens.
- **Status:** RESOLVED-WITH-INSTRUCTION — no longer blocks DATA-02 planning.
- **Resolution note:** Under the user's full-autonomy instruction, choose option
  A. Record each dropped non-finite block in `dropped_samples`, then quarantine
  the trajectory with reason `non_finite_snapshot`; never admit a partially
  salvaged trajectory. Keep trajectory and sample accounting as separate
  identities and test both an interior-corruption case and an all-finite control.

## GAP-39-06 — Grouped stage-stratification objective

- **Decision point:** Define what the deterministic 80/10/10 splitter balances
  after `physical_key` groups become indivisible, including base/gold siblings
  that legitimately carry different record-level stage labels.
- **Where in artifact:** `.planning/REQUIREMENTS.md` DATA-04;
  `ctl_instruction.md:515-530,1600-1665,1928-1942`; `39-SPEC.md` DATA-04;
  `39-RESEARCH.md` Open Question 3.
- **Task context:** Turning the no-leakage and stage-stratified split invariants
  into a byte-deterministic manifest algorithm.
- **Classification:** semantic partitioning objective.
- **Source silence:** Sources lock grouping, approximate fractions,
  determinism, and held-out validation but do not choose a group-, record-, or
  multi-label optimization rule. Fidelity-specific base/gold records may have
  different stages.
- **Mathematical / engineering grounding:** Treating records independently
  leaks physical siblings; collapsing a group to one label discards real
  fidelity-stage information. A complete group signature preserves all labels,
  and integer apportionment is required because groups cannot be fractionally
  assigned.
- **Agent was tempted to:** Greedily minimize global record-count error. That is
  sensitive to traversal order and can obscure rare cross-fidelity signatures.
- **What the user needs to decide:**
  - **A.** Stratify indivisible groups by complete fidelity-stage signature and
    use deterministic Hamilton largest-remainder apportionment per signature.
  - **B.** Optimize record-count deviations across stages globally.
  - **C.** Balance only the number of physical groups, ignoring stage labels.
- **Confidence of impact:** HIGH — this choice controls leakage, reproducibility,
  and whether held-out stage populations reflect cross-fidelity structure.
- **Status:** RESOLVED-WITH-INSTRUCTION — no longer blocks DATA-04 planning.
- **Resolution note:** Under the user's full-autonomy instruction, choose option
  A. Use signature `(regime, base_stage, gold_stage_or_missing)`, canonicalize
  keys, apply a local seeded permutation per signature, apportion group counts
  with Hamilton largest remainder for 0.8/0.1/0.1, break equal remainders in
  fixed `train -> validation -> test` order, and expand records only afterward.
  Report unavoidable rare-signature deviations; never infer or recalibrate
  stages in the splitter. The signature consumes the Phase 39 Stage-0/1 seam
  resolved in GAP-39-08: record labels are `0`, collapsed `1` (CTL Stage 1a or
  1b), or `UNASSIGNED`; no Stage 2–6 label is invented.

## GAP-39-07 — `mem:` byte numerator

- **Decision point:** Define whether DATA-01's required `mem: <bytes>` value is
  deterministic resident dataset payload or whole-process RSS/MPS allocation.
- **Where in artifact:** `.planning/REQUIREMENTS.md` DATA-01; `39-SPEC.md`
  DATA-01; `39-CONTEXT.md` D-03; integrity-r2 `CLEARANCE.md:31`;
  `39-RESEARCH.md` Open Question 4.
- **Task context:** Planning an auditable 0.7 memory-watermark assertion.
- **Classification:** operational metric semantics.
- **Source silence:** The sources lock the log shape, 24 GB capacity, 0.7
  watermark, and expected fp32 payload but do not explicitly name the numerator.
  Operational materials observe RSS/swap separately from dataset residency.
- **Mathematical / engineering grounding:** RSS includes interpreter state,
  temporary parse arrays, allocator caches, and unrelated allocations, so it is
  nondeterministic across runs. Summing unique owned fp32 tensor storages gives
  a reproducible dataset-residency metric; views must not double-count storage.
- **Agent was tempted to:** Use RSS because it is directly visible to the
  operating system. That would make a deterministic acceptance test sensitive
  to unrelated process state.
- **What the user needs to decide:**
  - **A.** Define the required numerator as deduplicated owned resident fp32
    tensor-storage bytes; report RSS/MPS separately if desired.
  - **B.** Use whole-process RSS.
  - **C.** Use MPS allocator bytes even though the admitted set is CPU-resident.
- **Confidence of impact:** MEDIUM — all candidates fit current RAM, but only a
  deterministic numerator supports byte-exact testing and regression.
- **Status:** RESOLVED-WITH-INSTRUCTION — no longer blocks DATA-01 planning.
- **Resolution note:** Under the user's full-autonomy instruction, choose option
  A. Name the structured metric `resident_tensor_bytes`, count each underlying
  owned storage once, divide by the explicit 24 GB configured capacity, and emit
  `mem: <bytes> (<fraction>) watermark=0.7`. Optional `process_rss_bytes` or MPS
  metrics may be additional fields but cannot replace the DATA-01 assertion.

## GAP-39-08 — Production Stage-0/1 label seam

- **Decision point:** Define how authoritative stage membership reaches the
  in-memory split/query/batch pipeline when Phase 39 owns the Stage-0 scan and
  DATA-05 requires Stage-1 lookahead, while full Stage 2–6 recalibration is
  deferred.
- **Where in artifact:** `39-03-PLAN.md` supplied-stage references;
  `39-04-PLAN.md` `stage_by_record`; `39-05-PLAN.md` `StageQuery`;
  `39-06-PLAN.md` Stage-0 classification; checker revision iteration 1.
- **Task context:** Closing the production key link from admitted invariants to
  grouped stratification and real replay/lookahead batches.
- **Classification:** cross-plan data-contract seam.
- **Source grounding and boundary:**
  - `ctl_instruction.md:23-28,138-198` defines Stage 0, Stage 1a, and Stage 1b
    over original hierarchical Set 1a records and reserves high-resolution Set
    2a records for Stage 2 refinement; the Stage-0/1 predicates include strict
    `s_min > s0`.
  - DATA-05 requires `D_<=k` plus guarded `D_{k+1}` lookahead; for the Stage-0
    slice this requires observable Stage 0 and Stage 1 pools.
  - Phase 39 defers full Stage 1–6 threshold recalibration and must not invent
    Stage 2–6 labels.
  - GAP-39-03 makes the CTL Stage-0 predicate authoritative over the reversed
    derived-SPEC wording.
- **Mathematical / engineering grounding:** A split or batch query cannot be
  stage-aware if labels exist only inside a later report. Computing the Stage 0
  and Stage 1 predicates from the same admitted original/base Set 1a invariant
  record makes the report, splitter, and batch pools share one source of truth.
  Collapsing the mutually named Stage 1a/1b predicates to query label `1`
  supplies `D_1` without claiming later-stage calibration. Applying those
  predicates to gold Set 2a records would erase the fidelity progression by
  admitting Stage-2 refinement data into the Stage-0/1 pools.
- **Agent was tempted to:** Label only Stage 0 and mark every other record
  `UNASSIGNED`. That would force `has_stage(1)=false` on real data and could
  satisfy tests without exercising the locked lookahead path.
- **What the user needs to decide:**
  - **A.** Compute CTL Stage 0 and Stage 1a/1b only for admitted original/base
    hierarchical Set 1a records, collapse 1a/1b to query label `1`, and mark
    gold Set 2a plus every other record `UNASSIGNED`.
  - **B.** Compute Stage 0 only and disable real Stage-1 lookahead.
  - **C.** Implement provisional Stage 2–6 labels in Phase 39.
- **Confidence of impact:** HIGH — without this seam, DATA-04/05 can pass
  synthetic tests while real Stage-0 split and lookahead batches are unusable.
- **Status:** RESOLVED-WITH-INSTRUCTION — no longer blocks plan revision.
- **Resolution note:** Under the user's full-autonomy instruction, choose option
  A. Create one pure authoritative classifier before adapter residency; persist
  `stage_label` on every admitted record as `0`, `1`, or `UNASSIGNED`. Evaluate
  Stage 0 first and Stage 1a/1b second only when the record is original/base
  hierarchical Set 1a; collapse 1a/1b to `1`. Hierarchical gold Set 2a and all
  other records remain `UNASSIGNED`; do not assign Stage 2–6. The adapter,
  grouped splitter, `StageQuery`, batch constructor, and Thrust-A report must
  all consume that same field. Real-corpus Wave 5 evidence must show Stage-0
  replay and Stage-1 lookahead pools from Set 1a when `has_stage(1)` is true,
  and zero gold records labeled Stage 0 or 1.

## GAP-39-09 — Measured-vs-reference `dt_out` warning threshold

- **Decision point:** Define the relative-disagreement threshold at which the
  adapter warns that the independently measured `dt_out` disagrees with the
  footer/default reference value. The threshold is diagnostic only (it never
  gates admission), but it decides whether the real-corpus scan emits a wall of
  warnings or stays quiet.
- **Where in artifact:** `39-02-PLAN.md` task 39-02-01 behavior/action ("warn
  only when finite relative disagreement exceeds 1%"); `39-SPEC.md` DATA-01
  measured/reference dt_out provenance.
- **Task context:** Recording the reversible implementation default surfaced by
  cross-AI review (claude MEDIUM-2) for consistency with how GAP-39-04 handled
  its `64` safety factor.
- **Classification:** semantic implementation threshold (reversible default).
- **Source silence:**
  - `simulation_data/Documentation/README.md:580-628` documents folder-specific
    reference/default `dt_out` values but gives no measured-vs-reference
    disagreement tolerance.
  - `ctl_instruction.md` does not mention a measured/reference `dt_out`
    comparison or warning at all; `dt_out` provenance is a Phase 39 diagnostic
    addition.
  - `39-SPEC.md` DATA-01 requires measured and reference `dt_out` provenance to
    be retained and warns on disagreement, but does not name a threshold.
- **Mathematical / engineering grounding:** The measured value is
  `median(diff(times))` and the reference is a documented cadence; their
  relative disagreement is `|measured - reference| / max(|reference|, tiny)`.
  A 1% relative threshold is large enough to tolerate float cadence jitter and
  small enough to flag a genuine folder/default mismatch. It is a warning only:
  it never changes completeness (clause 4 uses `times[-1] >= 9.5`) or admission.
- **Agent was tempted to:** Leave the 1% value inline as if it were source
  authority. That would repeat the unregistered-default drift the gap register
  exists to prevent.
- **What the user needs to decide:**
  - **A.** Retain 1% as a reversible, clearly-labeled diagnostic warning
    threshold (consistent with how GAP-39-04 labels `64`).
  - **B.** Choose a different relative/absolute threshold and its units.
  - **C.** Suppress the warning entirely and retain only raw provenance.
- **Confidence of impact:** LOW — the threshold is diagnostic only and never
  gates admission or completeness; it affects log noise, not scientific
  selection.
- **Status:** RESOLVED-WITH-INSTRUCTION — non-blocking for DATA-01 planning.
- **Resolution note:** Under the user's 2026-07-13 full-autonomy instruction,
  choose option A: retain the 1% relative measured-vs-reference `dt_out`
  disagreement threshold as a reversible implementation safety factor, not
  source authority. Plans and tests must label it reversible and test the exact
  1% no-warning and greater-than-1% warning boundaries. Revisit only if
  real-corpus logs show the threshold is miscalibrated.

---

## GAP-39-10 — Characteristic-time `T` in `τ = 2(t/T)−1` and the collocation bound `[0,T]`

- **Decision point:** Choose the characteristic time `T` used by the
  replay/lookahead batch constructor for `τ = 2(t/T)−1` and the collocation
  bound `[0,T]` (DATA-05). The plans (cycle-2 M2/HIGH-5) introduced a per-record
  `T = times[-1]`, but the locked non-dimensionalization pairs a global `T`.
- **Where in artifact:** `39-02-PLAN.md` task 39-02-01 `FixedBatch.T` field and
  the DATA-01 `T` accessor; `39-05-PLAN.md` task 39-05-02 (`T = times[-1]` for
  `tau` and `[0,T]`); `pinn/constants.py:24,31`; `39-RESEARCH.md` τ/collocation
  text.
- **Task context:** Cross-AI review cycle 4 (claude HIGH-1), verified against the
  live `pinn/constants.py`.
- **Classification:** semantic — touches a v1.5-locked convention
  (`D ≈ 4.6416`); cross-phase (affects every emitted τ, the collocation bound,
  Phase 40's derivative rescaling `u = t/T`, and Phase 38's `T=10` gradcheck
  probe).
- **Source silence:**
  - `pinn/constants.py:24` — `D_CHARACTERISTIC_LENGTH = 100^(1/3) ≈ 4.6416`,
    comment "cbrt(T²) with T = 10 (PIPE-09 identity D³ = G·T²)."
  - `pinn/constants.py:31` — `T_CHARACTERISTIC_TIME = 10.0`, comment
    "T = t_max; dataset horizon t_end = 10 fixes t_max = 10."
  - `.planning/REQUIREMENTS.md:13` locks "the raw-mass `D ≈ 4.6416` convention"
    (v1.5 outcome); NET-04 (`.planning/REQUIREMENTS.md:43`) evaluates the loss
    in the *shared* dimensionless system `t_τ ∈ [-1,1]`, `r' = r/D`.
  - None of `ctl_instruction.md`, `pinn_architecture.md`, or `39-SPEC.md`
    states whether `τ`'s `T` is the global `T_CHARACTERISTIC_TIME = 10.0` or a
    per-record `times[-1]`; the existing code locks the global `T` for
    `u = t/T`.
- **Mathematical / engineering grounding:** PIPE-09 ties `(T, D)` together by
  `D³ = G·T²`. The locked `D ≈ 4.6416` is derived from the global `T = 10`. If
  `τ = 2(t/T)−1` scales time by a per-record `T = times[-1]` while
  `r' = r/D` keeps the global `D` (from `T = 10`), the single
  non-dimensionalization splits across two inconsistent `(T, D)` pairs; every
  emitted `τ`, the collocation bound, and Phase 40's `u = t/T` derivative
  rescaling inherit the discrepancy, and Phase 38's `T = 10` gradcheck probe
  would disagree with the loader. The split is invisible to dataset-free tests
  (fixtures with `T ≈ 10` pass).
- **Agent was tempted to:** Silently pick the per-record `T` (cycle-2's choice)
  or silently pick the global `T`. Either is a physics-adjudication call on a
  locked convention; STOP protocol forbids inventing it.
- **What the user needs to decide:**
  - **A.** Global `T = T_CHARACTERISTIC_TIME = 10.0` for both `τ` and the
    `[0,T]` collocation bound — keeps `(T, D)` coherent with PIPE-09 and
    matches Phase 38's `T = 10` gradcheck probe.
  - **B.** Per-record `T = times[-1]` with a per-record `D` re-derivation
    (`D = ∛(G·T²)`) — keeps PIPE-09 per-record but changes the v1.5-locked
    global `D` convention.
  - **C.** Hybrid — global `T = 10` for `τ`, per-record `times[-1]` only for
    the collocation `[0,T]` bound.
- **Confidence of impact:** HIGH — affects every emitted `τ`, the collocation
  bound, and the Phase 40 cross-phase seam; one option (B) revises a v1.5 lock.
- **Status:** RESOLVED-WITH-INSTRUCTION (non-blocking for DATA-05 planning).
- **Resolution note:** Under the user's 2026-07-13 instruction, choose option A:
  Phase 39 uses the global `T = T_CHARACTERISTIC_TIME = 10.0` (from
  `pinn/constants.py`) for BOTH `τ = 2(t/T)−1` and the `[0,T]` collocation
  bound. The per-record `FixedBatch.T` field introduced cycle 2 is REMOVED; the
  DATA-01 `T` accessor is removed (no per-record `T` is exposed). This keeps
  `(T, D)` coherent with PIPE-09 and aligns with Phase 38's `T = 10` gradcheck
  probe. The admission guarantee `times[-1] >= 9.5` (clause 4) remains a
  completeness gate but is NOT the `τ`/collocation `T`. Apply in `39-02-PLAN.md`
  and `39-05-PLAN.md` before execution.

## GAP-39-11 — Missing-base sentinel in the DATA-04 split signature

- **Decision point:** The DATA-04 split signature
  `(variant, base_stage_label, gold_stage_or_missing)` defines a missing-gold
  sentinel (GAP-39-06) but no value for a missing *base* record. Base and gold
  are independent Brutus runs at different tolerance/word-length and receive
  independent admission outcomes, so a base record rejected by admission
  clause-5 while its gold sibling is admitted leaves a `physical_key` group in
  the admitted set containing only a gold record with no defined
  `base_stage_label`. Decide how the split/partition represents a
  missing/admitted-without-base group.
- **Where in artifact:** `39-04-PLAN.md` task 39-04-02 (split signature
  `(variant, base_stage_label, gold_stage_or_missing)`); the partition function
  that forms that signature.
- **Task context:** Cross-AI review cycle 4 (claude HIGH-2).
- **Classification:** semantic — defines a new sentinel value in the DATA-04
  contract; the silent-coercion failure mode would conflate "base rejected"
  with "base admitted-but-unlabeled."
- **Source silence:**
  - `ctl_instruction.md` / `pinn_architecture.md` do not address base-vs-gold
    asymmetric admission outcomes within a `physical_key` group.
  - `39-SPEC.md` DATA-04 specifies the `physical_key` grouping and the
    no-spanning-splits invariant but not a missing-base representation.
  - GAP-39-06 (the gold side) is resolved; the base side is not.
- **Mathematical / engineering grounding:** The signature is the partition key
  for the Hamilton stratified split. Every `physical_key` group must receive
  exactly one split. A group present in the admitted set with gold only (base
  rejected) has a well-defined `variant` and `gold_stage_or_missing` but no
  `base_stage_label`; an undefined slot is a `KeyError`/`None` hazard at
  partition time, and silently coercing it to `UNASSIGNED` conflates "base
  rejected" with "base admitted but UNASSIGNED." The reviewer notes all 4,857
  hierarchical IDs have both base+gold files, so the affected population is the
  whole hierarchical set (any clause-5 base rejection creates it).
- **Agent was tempted to:** Silently add a `MISSING_BASE` sentinel symmetric to
  missing-gold. That is a DATA-04 contract change the source materials do not
  authorize; STOP protocol forbids inventing it.
- **What the user needs to decide:**
  - **A.** Add a `MISSING_BASE` sentinel symmetric to `MISSING_GOLD`
    (GAP-39-06); a base-rejected/gold-admitted group partitions as a distinct
    signature, with a fixture asserting it still receives exactly one split.
  - **B.** Treat a missing base as `UNASSIGNED` for the base slot, but record an
    explicit `base_admission_status=rejected` side-channel so the partition
    keeps the distinction without a new label.
  - **C.** Exclude base-rejected/gold-admitted groups from numeric pools
    entirely (they cannot contribute a numeric `base_stage_label`), documenting
    the exclusion.
- **Confidence of impact:** MEDIUM — affects a contract value used at Wave-4
  split time; the failure mode is a KeyError/silent coercion at the real-corpus
  Wave-5 gate, not at dataset-free test time.
- **Status:** RESOLVED-WITH-INSTRUCTION — no longer blocks the missing-base
  path of DATA-04 planning.
- **Resolution note:** Under the user's 2026-07-14 instruction to resolve this
  gap carefully, choose option A. Add a canonical `MISSING_BASE` sentinel
  symmetric to `MISSING_GOLD`. The sentinel belongs only to the DATA-04 split
  signature and manifest metadata; it is not a persisted record `stage_label`
  and never enters a numeric stage pool. A base-rejected/gold-admitted group
  therefore has a total, distinct signature (for example,
  `(variant, MISSING_BASE, UNASSIGNED)`), remains distinguishable from a group
  whose base was admitted with `stage_label=UNASSIGNED`, and still receives
  exactly one split like every other admitted `physical_key`. Replace the
  `MissingBaseSentinelUndefined` deferral in `39-04-PLAN.md` during the cycle-4
  replan, and add a fixture where base is rejected, gold is admitted, and the
  group partitions exactly once without entering numeric pools.

## GAP-39-12 — Collocation-point allocation across selected trajectories

- **Decision point:** Define how DATA-05 allocates the provisional total of
  4,096 continuous collocation points across the 240 replay-only or 256
  replay-plus-lookahead trajectory identities selected for a batch. The total
  point budget and uniform time domain are grounded, but the per-trajectory
  integer counts are not.
- **Where in artifact:** `39-05-PLAN.md:19,103,109,114`, task 39-05-02
  (`sample_collocation_points` and its tests); future
  `pinn/data/batches.py` implementation.
- **Task context:** `$gsd-plan-phase 39 --reviews`, checker pass after the
  cycle-4 replan. The replan rejected the review's near-even suggestion and
  selected a global multinomial trajectory-identity draw without an owner
  ruling.
- **Classification:** semantic — changes how physics-residual samples weight
  selected trajectories within every Stage-0 batch and therefore changes the
  training distribution seen by Phase 40.
- **Source silence:**
  - `39-SPEC.md:48-51` fixes independent data/collocation point sets, continuous
    uniform collocation times, and the provisional total near 4,096, but does
    not assign those points to trajectory identities.
  - `ctl_instruction.md:1833-1853` separates the two loss roles, fixes the
    continuous `[0,T]` time domain, and labels 4,096 a provisional/example
    budget; it does not specify per-trajectory collocation counts or an
    identity-sampling distribution. Its word "independent" distinguishes the
    data and collocation point sets, not independent trajectory-identity draws.
  - `39-CONTEXT.md:85-94` (D-07/D-08) fixes the 240/16 trajectory pools, point-set
    separation, input shape, and sub-240 fatal signal, but leaves collocation
    allocation unstated.
  - `39-RESEARCH.md:420-423` repeats the provisional global count and continuous
    time domain without defining identity allocation.
  - `39-REVIEWS.md:73-75` explicitly states that CTL is silent and contrasts a
    global multinomial draw with an even per-trajectory allocation; review
    advice is not a grounding source.
- **Mathematical / engineering grounding:** For `M` selected trajectories and
  total collocation budget `C = 4096`, the implementation must choose integer
  counts `n_i >= 0` satisfying `sum_i n_i = C`. A uniform multinomial draw
  preserves i.i.d. identity sampling and an exact total but allows uneven
  gradient weight and `n_i = 0`; at `M = 256`, the zero-count probability for
  one trajectory is `(255/256)^4096 ~= e^-16 ~= 1.1e-7` (so zero coverage is
  possible but rare, not a "nontrivial fraction"). A guaranteed-minimum draw
  removes zero coverage but changes the identity distribution through the
  forced allocation. A near-even quota minimizes per-batch variance and
  guarantees coverage, but it abandons i.i.d. identity draws; for the 240-only
  case it also needs a deterministic or seeded rule for the 16-point remainder
  because `4096 = 17*240 + 16`. All choices preserve tensor cardinality but
  produce different physics-loss weighting, reproducibility tests, and Phase
  40 sampler seams.
- **Agent was tempted to:** Keep option A because it is simple and uses the
  existing local RNG, or choose option C because `4096 = 16*256` makes the
  populated-lookahead batch exactly balanced. Neither follows from the cited
  sources, and `TRAIN-04`'s later adaptive sampler ownership does not authorize
  Phase 39 to choose the initial identity allocation silently.
- **What the user needs to decide:**
  - **A.** Global i.i.d. draw — independently choose each of the 4,096
    trajectory identities uniformly with replacement from the selected pool;
    exact total and i.i.d. semantics, with uneven counts and rare zero-count
    trajectories allowed.
  - **B.** Guaranteed-one plus random remainder — give every selected
    trajectory one collocation point, then allocate the remaining `4096-M`
    identities by uniform multinomial draw; exact total and guaranteed
    coverage, with random unevenness after the minimum.
  - **C.** Near-even quota — allocate each selected trajectory either
    `floor(4096/M)` or `ceil(4096/M)` points, distributing any remainder by a
    canonical seeded order; exact total, guaranteed balanced coverage, and no
    i.i.d. trajectory-identity draw.
- **Confidence of impact:** HIGH — this is the per-batch sampling distribution
  for every physics/energy residual and becomes an executable test contract at
  the Phase 39 to Phase 40 seam.
- **Status:** RESOLVED-WITH-INSTRUCTION — no longer blocks DATA-05 plan
  verification.
- **Resolution note:** Under the user's 2026-07-14 delegation to use best
  mathematical and physics judgment, choose option C: near-even quotas. For
  `M` canonically sorted selected trajectory identities and total budget
  `C = 4096`, assign `q = floor(C/M)` points to every identity, compute
  `r = C mod M`, and give one additional point to `r` identities selected by a
  canonical permutation from the task's local seeded RNG. Thus a 256-trajectory
  batch receives exactly 16 points per identity; a 240-trajectory replay-only
  batch receives 17 points per identity plus one extra point for 16 seeded
  identities. Draw every assigned time independently and continuously from the
  global `[0, T_CHARACTERISTIC_TIME] = [0, 10.0]` interval, and keep energy on
  the same physics set. This stratifies the discrete identity dimension,
  guarantees every selected trajectory contributes a physics residual, and
  minimizes avoidable per-batch identity-weight variance without changing the
  fixed budget or introducing Phase 40 adaptive/residual-aware sampling.

## GAP-39-13 — Inert prohibited-content assertion in the validation ledger

- **Decision point:** Decide how the `39-VALIDATION.md` ledger should express a
  "prohibited content is absent" assertion, given that the current
  `! rg -q "<pattern>" "$v"` form cannot fail. This is the ledger's assertion
  schema, not a single row's content.
- **Where in artifact:** `39-VALIDATION.md:65` (row 39-10-02) and
  `39-VALIDATION.md:71` (row 39-13-02), both in the clause
  `! rg -q "\*\*R[u]n:\*\*|simulation_data/Data>" "$v"`.
- **Task context:** Surfaced as finding #2 of `39-13-SUMMARY.md`; re-confirmed
  by the 2026-07-16 re-verification (`39-VERIFICATION.md`, FINDING-2) after
  gap-closure plan 39-14 repaired the adjacent awk defect in row 39-10-02.
- **Classification:** process-artifact schema — this is the ledger's
  pass-criteria format, which the governance instructions reserve to the owner.
- **Source silence:**
  - `39-10-PLAN.md:115` supplies the authoritative text for row 39-10-02's awk
    clause but carries the same `! rg -q` form, so the plan reproduces the
    defect rather than resolving it.
  - `39-13-PLAN.md:137` explicitly forbids widening a historical row's
    exclusion set, but does not address the inverted-assertion form.
  - `.planning/REQUIREMENTS.md` DATA-01..06 constrain scan behavior and
    evidence content; no requirement specifies ledger assertion syntax.
- **Mathematical / engineering grounding:** Two independent defects compound so
  that the clause is inert in both directions, each empirically reproduced
  2026-07-16.
  1. **The needle self-matches.** `$v` is `39-VALIDATION.md` itself, and the
     literal string `simulation_data/Data>` occurs twice in that file — inside
     the two rows' own command text. `rg -c '\*\*R[u]n:\*\*|simulation_data/Data>'`
     returns 2. The author defended the first alternative against exactly this
     (`R[u]n` is a character-class evasion; searching for the literal `**Run:**`
     returns 0) but did not apply the same device to the second alternative.
     So `rg -q` always exits 0 and the inverted clause always evaluates to false.
  2. **`!`-inversion is exempt from `errexit`.** POSIX specifies that `set -e`
     does not abort when the failing command is the operand of `!`. Verified:
     `bash -c 'set -euo pipefail; ! true; echo REACHED'` prints `REACHED`.
     So the false clause is discarded and the script proceeds.
  The two cancel: the assertion always "fails" and the failure is always
  ignored. It therefore carries no information — it would stay silent if a
  hand-pasted terminal transcript were present, which is the precise thing it
  was written to prohibit. Note this is the same defect class as the row
  39-10-02 awk brace (`test -z "$(cmd)"` discards the inner exit status) that
  39-14 repaired: a check that cannot fail. Fixing defect 1 alone would make
  the clause fire spuriously on its own text; fixing defect 2 alone would make
  it abort on that spurious match. Both must move together.
- **Agent was tempted to:** Rewrite both rows to the `assert_absent()` helper
  already defined in rows 39-07-02/39-10-01 (`39-VALIDATION.md:59,60,70`),
  which handles the rc distinction correctly, and add a `[u]`-style evasion to
  the second alternative. This edits the recorded commands of two historical
  green rows — the exact move `39-13-PLAN.md:137` prohibits — and silently
  chooses a self-match evasion the sources never ratified.
- **What the user needs to decide:**
  - **A.** Leave both rows as recorded and accept the clause as inert,
    documenting it here as a known no-op. Preserves the historical rows byte-
    for-byte; the criterion stays enforced only by the independent audit.
  - **B.** Repair both rows in place to the existing `assert_absent()` form
    with a self-match evasion on both alternatives, and re-run them. Restores
    a real check at the cost of editing two historical rows' commands.
  - **C.** Leave the historical rows untouched and add one new ledger row that
    asserts the prohibition correctly going forward. Preserves history and
    restores enforcement, at the cost of a row whose scope overlaps two others.
- **Confidence of impact:** LOW for Phase 39's verdict — the underlying
  criterion is independently satisfied (the 2 matches are the assertion's own
  pattern text, not pasted transcript; 0 real violations, confirmed by the
  2026-07-16 re-verification, which scored the phase 7/7 with this finding
  recorded as non-blocking). MEDIUM going forward — the form is copyable, and
  this phase has now produced three separate "check that cannot fail" defects.
- **Status:** RESOLVED-WITH-INSTRUCTION (2026-07-16) — Option B (repair both
  rows in place).
- **Resolution note:** Under the user's 2026-07-16 delegation to use best
  judgment and resolve the gap, **Option B** was chosen over the initially
  recommended Option C. The decisive ground is the **Plan 39-14 precedent**
  (owner-accepted at Phase 39 closure): 39-14 fixed the identical defect class —
  a vacuous "cannot fail" assertion — in row 39-10-02's awk **in place**, and
  established that `39-13-PLAN.md:137`'s prohibition is an *anti-weakening* rule
  (do not widen a historical row's exclusion set), so *strengthening* a vacuous
  assertion is not barred. De-self-matching the second alternative to parity
  with the already-evaded first alternative (`R[u]n`) completes the author's
  evident intent and adds real enforcement — a strengthening, not a weakening.
  Option B also yields the cleanest end state: both broken rows become live, with
  no permanently-inert assertion, no overlapping duplicate row, and no invented
  non-plan row identity (39-14-01 being already taken would have forced Option C
  to mint a fresh row-identity schema — the invention the STOP protocol avoids).
  The fix, applied to rows 39-10-02 (`39-VALIDATION.md:65`) and 39-13-02
  (`39-VALIDATION.md:71`), replaces the inert `! rg -q "…|simulation_data/Data>"`
  clause with the ledger's already-ratified `assert_absent()` helper (as used in
  rows 39-07-01/02 and 39-13-01), split into two line-anchored, de-self-matched
  calls: `^[[:space:]]*\*\*R[u]n:\*\*` and `^[[:space:]]*simulation_data/Data[>]`.
  Anchoring targets a pasted transcript prompt at (indented) line start — the
  real prohibited artifact — while the mid-line pattern text in every command
  cell is not a line start, so it cannot self-match; the char-class evasion is
  belt-and-suspenders. Verified exactly as 39-14 did: (1) literal
  `simulation_data/Data>` count in the ledger dropped 2 → **0**; (2) both full
  row commands, extracted verbatim from the edited ledger and `eval`'d, observed
  **exit 0**; (3) liveness proven — the assertions **exit 1** on a scratch copy
  with injected `simulation_data/Data> …` and `**Run:** …` transcript lines
  (scratch written outside the repo, deleted after; no red status ever written
  to the real ledger); (4) the row→status pair list is byte-identical pre/post
  (SHA-256 `b940c5e5…`, 29 rows, all `✅ green`), so both rows' `✅ green` is
  retained from a fresh observed exit, not carried forward on the prior
  worthless record. The `assert_absent()` form is now the canonical
  prohibited-content schema for the Phase 40 `40-VALIDATION.md` ledger, closing
  the "MEDIUM going forward / copyable" risk this gap flagged.

---

**Milestone-index status:** `.planning/milestones/v2.0-GAPS.md` synchronized on
2026-07-16: GAP-39-01 is deferred, GAP-39-02 through GAP-39-13 are resolved.
