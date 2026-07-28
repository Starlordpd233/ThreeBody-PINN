# Phase 46 Gap Register — Frame Resolution & Gate-Aligned Validation

Phase-local STOP-protocol gap register for Phase 46 (milestone v2.2). Each entry
is a source-silent decision that this phase **surfaced** rather than decided, per
the CLAUDE.md / AGENTS.md STOP protocol and `46-CONTEXT.md` D-09 / D-13. The
milestone-wide index is `.planning/milestones/v2.2-GAPS.md` (created on the first
v2.2 gap, standing trigger).

This register is written by the Phase 46 orchestrator (parent session), not by a
subagent — per governance, the parent owns gap-register writes.

## GAP-46-01 — The held-out evaluator pairs model-frame positions with raw native times; is its `eps_H` the gate quantity EVAL-01 will spend its single look on?

- **Decision point:** `pinn/evaluate.py` — the sole production consumer of
  `gate_metrics.compute_trajectory_gate_metrics` — finite-differences the model's
  predicted positions against **raw native snapshot times** rather than the locked
  normalized time `u = t/T`. Under the locked contract the model emits scaled
  positions `r'` whose coherent conjugate is `u`, which would make the evaluator's
  kinetic term smaller than the contract's by exactly `T² = 100` while leaving the
  potential term untouched — changing the T:V balance and therefore `eps_H`.
  Whether this is a defect is **conditional on CONF-01's own verdict** (see
  grounding below), so the question is not "fix it now" but "which of the two
  CONF-01 branches leaves the held-out evaluator computing the intended quantity,
  and what must Phase 50/51 do about it before EVAL-01 is spent?"

- **Where in artifact:**
  - `pinn/evaluate.py:407` — `times_native = test_index.snapshot_times(key)`
  - `pinn/evaluate.py:411-415` — the same `times_native` becomes `times_t` with no
    `/T` normalization (contrast `_build_tau_ic13`, which *does* normalize for the
    network leaf)
  - `pinn/evaluate.py:420-425` — `positions = predicted.reshape(-1,3,3)` (model
    output) passed with `times_t` into `gate_metrics.compute_trajectory_gate_metrics`
  - `pinn/verification/gate_metrics.py:116-121` — `finite_difference_velocity`
    divides by whatever units `times` carries
  - `pinn/verification/gate_metrics.py:162-163` — kinetic term `0.5 * m * ||v||²`
  - `pinn/constants.py:24,31` — `D = 100^(1/3) ≈ 4.6416`, `T = 10.0`
  - `.planning/phases/46-frame-resolution-gate-aligned-validation/46-CONTEXT.md`
    D-12 (coherent pair is `r'` with `u=t/T`) and D-13 (an actual caller-contract
    conflict is a governed gap, never a silent evaluator change)

- **Task context:** Surfaced during `/gsd-plan-phase 46` research (candidate C1 in
  `46-RESEARCH.md`), then independently verified by the orchestrator by direct read
  of `evaluate.py`, `gate_metrics.py`, `adapter.py`, and `constants.py` before being
  recorded. The finding arose while establishing the coherent position/time pair
  INST-01 must use (D-12) — i.e. exactly the "planning exposes a conflict between an
  existing caller contract and the locked `r'`/`u` specification" case D-13 names.

- **Classification:** cross-phase reframing — the finding is about `pinn/evaluate.py`,
  which Phase 46 may not modify, invoke, or import (D-16). Its consequence lands on
  Phases 50–51 (Stage-0 re-run + the single held-out evaluation), so it changes
  downstream phase scope and MUST be surfaced rather than absorbed.

- **Source silence:**
  - `pinn/evaluate.py:1-40` (module docstring) specifies checkpoint ownership,
    single-use, and split selection in detail; it says nothing about the time-leaf
    units handed to the gate pass.
  - `pinn/verification/gate_metrics.py:1-30` cites `ctl_instruction.md` §2.4.5
    clause 5 for the Hamiltonian, softening, and thresholds, and states velocity is
    obtained "by finite-differencing the predicted positions over the persisted
    monotone snapshot times" — but never states a required time-unit contract for
    its caller. The module deliberately imports no scale constants, so it cannot
    enforce coherence itself.
  - Phase 43 never adjudicated this. A grep of the full Phase 43 artifact set
    (`.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/`)
    for `u=t/T`, `normalized time`, `times_native`, `snapshot_times`, and `raw time`
    returns only two incidental API-listing mentions in `43-RESEARCH.md:218,434`.
    `43-VERIFICATION.md` verifies gate behavior against fixtures; it does not rule
    on the evaluator's position/time pairing.
  - The 2026-07-24 Stage-0 conformance audit does not cover `evaluate.py` at all —
    a grep for `evaluate.py`, `finite_difference_velocity`, and time/velocity
    pairing in
    `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-24-stage0-training-path-conformance-audit.md`
    returns nothing. This is therefore a NEW finding about the evaluator's
    assembly, not a re-litigation of the audit's verified-clean section (D-26).

- **Mathematical / engineering grounding:** `eps_H = max_t |(H(t) − H(0))/H(0)|` is
  invariant under a *uniform* rescaling of `H`, but **not** under a *differential*
  rescaling of the kinetic term relative to the potential term. `finite_difference_velocity`
  returns `d(pos)/d(t)` in the units of the supplied `t`. If the model emits `r'` and
  the supplied time is raw `t`, the resulting velocity is `dr'/dt`, whereas the locked
  contract's coherent velocity is `dr'/du = T · dr'/dt`. The kinetic term
  `0.5 Σ mᵢ‖vᵢ‖²` is therefore a factor `T² = 100` too small, while the potential
  `−Σ mᵢmⱼ / r'_safe,ij` (position-only) is unchanged. `H = T + V` is thus neither the
  raw-frame nor the scaled-frame Hamiltonian but a third, internally inconsistent
  quantity, and its relative drift is not the spec's `eps_H`.

  **The conditional is the crux.** Whether this is a defect depends on what the model
  actually emits, which is precisely CONF-01's question:
  - If CONF-01 finds the training targets are the locked `r'`, the model emits `r'`,
    the pairing is incoherent, and the Phase 43 held-out `eps_H = 237.21` is a
    mis-scaled quantity — with a knock-on to GAP-44-02's mandated re-derivation.
  - If CONF-01 finds the targets are raw `r` (which direct code reading favours:
    `adapter.py:863,925-926,938,1035` store `parsed_brutus.positions`), then the
    model was trained to emit raw positions, `evaluate.py`'s raw-`r`/raw-`t` pairing
    is internally *coherent*, and the defect lies in the training targets instead —
    but the moment Phases 47–48 repair the target frame to `r'`, `evaluate.py`
    silently becomes wrong unless it is changed in the same breath.

  Either branch therefore imposes an obligation on Phase 50/51. The severity is set
  by EVAL-01/SCOPE-28: exactly one held-out evaluation remains for the milestone, and
  a mis-scaled kinetic term can flip a genuine PASS to FAIL or the reverse in a way
  that is not recoverable after the fact without hand re-derivation.

- **Agent was tempted to:** (a) treat this as an in-scope "while we're in the area"
  fix to `pinn/evaluate.py` — refused; D-16 forbids Phase 46 from invoking, importing,
  or modifying the held-out evaluator, and D-13 names exactly this case as a governed
  gap. (b) State flatly that the Phase 43 `eps_H = 237.21` is invalid — refused; that
  conclusion is downstream of CONF-01's unmeasured verdict, and asserting it now would
  be the invention the STOP protocol exists to prevent.

- **What the user needs to decide:**
  - **(A) Open now, act at Phase 50/51.** Accept the finding as a milestone-carried
    obligation: Phase 50/51 must assert the evaluator's position/time pair matches the
    CONF-01-ratified frame *before* EVAL-01 is spent, with a preflight assertion or
    test as the acceptance check. Phase 46 proceeds unchanged.
  - **(B) Defer to Phase 50/51 planning.** Record it, take no obligation now, and
    re-open the question when Phase 50/51 is planned. Risk: the coupling to the
    Phase 47–48 target-frame repair is exactly where it would be easiest to miss.
  - **(C) Out of v2.2 scope.** Treat the evaluator's assembly as outside the
    conformance-repair remit and carry it to v2.3. Risk: EVAL-01 gets spent first.
  - **(D) Widen Phase 46.** Add an evaluator-side conformance check to this phase.
    Note this contradicts D-16 and SCOPE-32 as currently written and would be a scope
    change, not a clarification.

  The orchestrator's assessment, for what it is worth: **(A)** — it costs nothing now,
  it binds the obligation to the phase that can actually discharge it, and it composes
  cleanly with the GAP-44-02 re-derivation mandate already inherited from v2.1.

- **Confidence of impact:** HIGH — bears directly on the correctness of the milestone's
  single unspendable-twice held-out evaluation (EVAL-01 / SCOPE-28), which is the point
  of v2.2, and couples to the inherited GAP-44-02 re-derivation obligation.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** User instruction 2026-07-26 explicitly delegated the option
  selection to Codex. **Refined Option A — bind the obligation now and discharge it
  before the Phase 51 held-out access.**
  1. EVAL-01 is authorized for the **corrected conformant implementation**. The locked
     output consumed by evaluation is therefore scaled position `r'`, and its coherent
     finite-difference time coordinate is `u = t/T`. The Phase 51 evaluator must pass
     predicted `r'` with `times_native / T_CHARACTERISTIC_TIME` to `gate_metrics`;
     passing raw native times with scaled predictions is prohibited.
  2. A CONF-01 `TARGETS_ARE_RAW` result diagnoses the historical resident target path
     and triggers D-09's owner-governed repair branch. It does **not** authorize a new
     raw-frame EVAL-01 run. The historical v2.0 evaluator pairing may have been coherent
     for a raw-output checkpoint, but its status remains conditional on the measured
     CONF-01 verdict and the GAP-44-02 re-derivation; this ruling does not pre-judge it.
  3. Phase 50/51 planning must make the evaluator's position/time assembly explicit,
     add a dataset-free regression proving the `r'`/`u` pair, and run a pre-invocation
     assertion before any test `StageIndex` or held-out trajectory is materialized.
     This is a RUN-03 implementation-correctness obligation, recorded separately from
     EVAL-01's already-ratified three eligibility preconditions.
  4. Phase 46 remains unchanged: D-16 still forbids it from importing, invoking, or
     modifying `pinn.evaluate`.

- **Blocking scope (resolved, dependency-scoped):** Never blocked Phase 46. The
  downstream obligation is now mapped to RUN-03 / Phase 51 and blocks the held-out
  invocation there until its regression and pre-access assertion pass.

---

## GAP-46-02 — Which frozen split manifest instantiates D-02's probe population?

- **Decision point:** D-02 requires the probe to run over "every Stage-0 identity in the
  frozen train and validation split views", with "the test split excluded absolutely".
  Three retained pilot manifests exist and they **differ pairwise**, so "the frozen split
  views" has no unique referent and the absolute-exclusion guarantee changes meaning
  depending on which manifest (or combination) is chosen.

- **Where in artifact:** `46-CONTEXT.md` D-02; `46-DISCUSSION-LOG.md:27` (singular
  phrasing, silent on multiplicity). Verified by the orchestrator:
  `runs/stage0-pilot-seed41/splits.json` sha256 `c25568a18f3c…`,
  `runs/stage0-pilot-seed42/splits.json` `5846ae5b5510…`,
  `runs/stage0-pilot-seed43/splits.json` `a8618b0c6d0f…`
  (`runs/stage0-smoke/splits.json` is byte-identical to seed-42). All three carry the
  same 7606 groups, so the difference is the seed-dependent train/validation/test
  **assignment**, not the population.

- **Task context:** Surfaced by the gsd-planner while planning 46-06 (the single
  real-corpus evidence run) — it needed a concrete eligible-key set and found no unique
  one. Returned as candidate CG-1; verified independently by the orchestrator before
  being recorded.

- **Classification:** semantic — it defines the probe population and, with it, the exact
  content of the held-out-exclusion guarantee that SCOPE-28 / EVAL-01 rest on.

- **Source silence:** `46-CONTEXT.md` D-02 names "the frozen train and validation split
  views" in the singular and never contemplates multiple retained manifests.
  `46-DISCUSSION-LOG.md:27` carries the same singular phrasing. `46-RESEARCH.md` assumes a
  single population (Assumption A2). `.planning/REQUIREMENTS.md` (CONF-01) and
  `.planning/ROADMAP.md` (Phase 46) name no manifest. No prior owner ruling selects one.

- **Mathematical / engineering grounding:** The CONF-01 verdict is a property of the data
  **pipeline** — every admitted trajectory traverses the same
  `preprocess_trajectory` → residency → `sample_data_points` path — so the raw-vs-`r'`
  answer is population-invariant in substance. What the choice does change is (i) the
  formal guarantee "no identity that is held out was read", and (ii) the recorded
  trajectory counts and per-trajectory evidence rows that make the verdict re-derivable
  under D-05. Because the assignments differ by seed, an identity that is train/validation
  under seed 42 may be **test** under seed 41 or 43. Reading it therefore satisfies D-02
  under one manifest while violating "the test split is excluded absolutely" under another.
  The options are not equivalent in what they guarantee:
  - **(A) Conservative intersection** — supply all three manifests; eligible = train-or-validation
    under *every* seed; excluded = test under *any* seed. Satisfies every reading of
    absolute exclusion. Cost: under-covers roughly a quarter of any single manifest's
    train+validation population, so the recorded counts are smaller than any one view.
  - **(B) Seed-42 only** — the evaluated seed of record. Full coverage of that view; but it
    reads identities that are held out under seeds 41 and 43.
  - **(C) Probe all three views separately** — three evidence sets, ~3× cost, and it reads
    every identity that is non-test under at least one seed (the union), which is the
    weakest exclusion guarantee of the three.

- **Agent was tempted to:** adopt (A) silently as "obviously the safe one". The planner in
  fact encoded (A) as the plan default with recorded provenance. The orchestrator is
  **not** letting that stand as a decision: (A) is defensible but it is a semantic choice
  about the exclusion guarantee, and D-02's silence is exactly the kind the STOP protocol
  says must be owner-ratified rather than defaulted.

- **What the user needs to decide:** (A), (B), or (C) above — or name a different manifest
  basis. The 46-04 machinery is manifest-set-parametric either way, so the ruling is a
  configuration input, not a redesign.

- **Confidence of impact:** MEDIUM — the verdict itself is expected to be invariant, but
  the ruling determines the formal held-out-isolation claim and the recorded evidence
  counts, and held-out isolation is the discipline the whole milestone is protecting.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** User instruction 2026-07-26 explicitly delegated the option
  selection to Codex. **Option A — conservative intersection across the three retained
  pilot manifests**, content-pinned as:
  - `runs/stage0-pilot-seed41/splits.json` —
    `c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86`
  - `runs/stage0-pilot-seed42/splits.json` —
    `5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903`
  - `runs/stage0-pilot-seed43/splits.json` —
    `a8618b0c6d0f0f1487fe4e3f8c0409a3e3398c7e8cb8bee2b4d3d7962a576172`

  `runs/stage0-smoke/splits.json` is omitted because it is byte-identical to the
  seed-42 manifest and adds no independent exclusion constraint. An identity is
  eligible only when it is Stage 0 and train-or-validation under **all three** pilot
  manifests; test under **any one** excludes it. Direct manifest arithmetic records
  2,265 Stage-0 physical identities, 2,039 non-test identities per individual seed,
  and a 1,651-identity all-three intersection — 388 (19.0%) fewer than one seed's
  train+validation view. Those are manifest-level provenance counts; adapter
  admission/quarantine and snapshot exclusions remain separately reported in D-05
  evidence. The retained 1,651-identity population is ample for a pipeline-wide frame
  property, while this is the only listed basis that makes D-02's absolute test
  exclusion true across the full three-seed protocol.

- **Blocking scope (resolved, dependency-scoped):** The 46-06 population gate and
  therefore 46-07 are unblocked as of 2026-07-26. Plan 46-06 must pass exactly the
  three content-pinned pilot manifests above and quote this resolution as provenance.

---

## GAP-46-03 — Is a measured finite-difference floor admissible in D-06's tolerance basis?

- **Decision point:** D-06 permits numerical comparison tolerances "derived from the
  represented dtype/round-trip error". The planner's 46-02 design derives the
  per-trajectory tolerance as **measured control-arm finite-difference floor + measured
  fp32 round-trip term**. The FD floor is a *truncation*-error term, not a dtype term. Is
  widening the basis this way inside D-06's delegation, or does D-06 mean dtype/round-trip
  only?

- **Where in artifact:** `46-CONTEXT.md` D-06; planner candidate CG-2; the tolerance
  derivation in `46-02-PLAN.md`.

- **Task context:** Surfaced by the gsd-planner while writing 46-02's tolerance derivation;
  it explicitly requested a veto opportunity before 46-02 executes.

- **Classification:** semantic — it sets what counts as "agreement" between a hypothesis
  arm and its control, which is the operative comparison the CONF-01 verdict rests on.

- **Source silence:** D-06 authorizes a dtype/round-trip-derived tolerance and forbids
  promoting Phase 38's one-fixture threshold, a lower mean, or an ad hoc ratio into a
  target-frame lock. It does not say whether a *measured* truncation floor may enter the
  tolerance, nor does it rule it out. `46-RESEARCH.md` does not settle it.

- **Mathematical / engineering grounding:** A centered finite difference carries truncation
  error `O(h²)·|r'''|`, which for these trajectories dominates fp32 round-off
  (eps ≈ 1.19e-7) by orders of magnitude. A dtype-only tolerance would therefore be far
  tighter than the numerical method's own noise floor, so **every** arm — including the
  positive control — would read as "differs", and D-06's fail-closed clause would trigger
  unconditionally. That makes the dtype-only reading self-defeating in practice, which is
  the planner's motivation. The counter-consideration is that a measured floor is derived
  from the data rather than from the representation, so it is one step closer to the ad hoc
  ratio D-06 forbids, and it must not become a de facto physics threshold.

- **Agent was tempted to:** ratify the planner's derivation inline as "short uncontroversial
  numerics". Declined: D-06 is the specific guard rail against threshold construction in
  this phase, and the planner itself asked for a veto — deciding it silently would defeat
  the decision's purpose.

- **What the user needs to decide:** (A) Ratify the planner's two-term derivation
  (measured FD floor + measured fp32 round-trip), reported separately from any physics
  acceptance threshold and with the theory-predicted arm separations (~21× / ~99×) shown
  as diagnostics only. (B) Require a strict dtype/round-trip-only tolerance and accept that
  the fail-closed path may trigger. (C) Specify a different admissible basis.

- **Confidence of impact:** LOW–MEDIUM — the two hypothesis arms are expected to separate
  by ~1–2 orders of magnitude, far above either candidate tolerance, so the verdict is
  unlikely to turn on this. It matters for whether the evidence artifact's agreement claim
  is well-founded and for whether the fail-closed path behaves as D-06 intends.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** User instruction 2026-07-26 explicitly delegated the option
  selection to Codex. **Option A — ratify the measured two-term numerical comparison
  tolerance**, with these binding guardrails:
  1. Per trajectory and under the same qualifying-snapshot mask, the finite-difference
     floor is `max(positive_control_median_residual,
     provenance_control_median_residual)`.
  2. The fp32 term is the measured, nonnegative residual increase caused by
     fp32-cast-then-float64-restored copies of the same control inputs. The tolerance
     is `finite_difference_floor + fp32_roundtrip_increment`.
  3. Persist the floor, round-trip increment, and sum separately. No safety multiplier,
     population-fitted percentile, imported physics threshold, Phase 38 threshold, or
     theory-predicted `~21x` / `~99x` separation may enter the tolerance; those
     separations remain diagnostics only.
  4. This tolerance answers only whether two measurements agree within the numerical
     resolution of the finite-difference operator. It is not a physics-acceptance,
     target-quality, Hamiltonian, or training threshold.
  5. Non-finite controls, a non-positive/non-finite tolerance, simultaneous consistency
     of both hypotheses, or failure of the opposing arm to lie strictly above the
     tolerance remains fail-closed as `VERDICT_AMBIGUOUS`.

  A dtype-only basis was rejected because it omits the discretization error of the
  measurement operator and would test the coherent controls against a bound below that
  operator's own resolution. A Richardson-extrapolation or fitted global error model
  would add assumptions and machinery without improving this binary, control-anchored
  frame decision.

- **Blocking scope (resolved, dependency-scoped):** The tolerance gate in 46-02 is
  unblocked as of 2026-07-26. The implementation and Test 6 must reproduce the
  two-term provenance and guardrails above exactly.

---

## GAP-46-04 — CONF-01's real-corpus verdict is `VERDICT_AMBIGUOUS`: a 100%-prevalent body-permutation + COM/boost confound prevents a unanimous raw-vs-scaled verdict. How should the owner route this?

- **Decision point:** The single sanctioned real-corpus CONF-01 evidence run
  (Plan 46-06, over the GAP-46-02 Option A 1651-trajectory intersection
  population) returned machine verdict `VERDICT_AMBIGUOUS`
  (`decide_verdict` rule 6, the fail-closed catch-all) — neither the clean
  `VERDICT_TARGETS_ARE_SCALED` that would unblock 46-07 under D-08, nor a
  clean `VERDICT_TARGETS_ARE_RAW`. Per D-09 this is an unresolved ambiguity,
  not a confirmed defect and not a confirmed-conformant frame, and it must be
  resolved or deferred by the owner before any frame-dependent work resumes.

- **Where in artifact:**
  `.planning/phases/46-frame-resolution-gate-aligned-validation/46-VERDICT.md`
  §§ "Branch: D-09", "Confound register", "Population and exclusion
  accounting"; measured fields cited from
  `.planning/phases/46-frame-resolution-gate-aligned-validation/evidence/target-frame/20260727T070221Z/raw.json`
  (SHA-256 `3fa8251b464600fd2e99f5745bdfb1c315fb0073051de009d2b60a13a7dfcf08`,
  committed `f106889b90b84dcc4889427a8e0272dc76f6e59b`): `verdict`,
  `aggregates.{raw_hypothesis,scaled_hypothesis}.count_consistent`,
  `confound_register` (3302 entries), and the per-trajectory
  `confounds.{identity_raw,identity_scaled,raw_residual_corrected}` fields.

- **Task context:** Plan 46-06, Task 3 ("Author 46-VERDICT.md and route the
  D-08/D-09 branch"), executed by the gsd-executor subagent in
  `.worktrees/trainex` on `milestone/v2.1`, 2026-07-27. Recorded by the Phase
  46 orchestrator (parent session) per governance — the executor returned the
  full STOP block in its completion message without writing this register
  itself.

- **Classification:** cross-phase reframing (the measured outcome bears on
  Phase 47's scope and the Phase 46→47 dependency) with a semantic-ambiguity
  component (the raw-vs-scaled target-frame question itself is not decidably
  answered by this evidence).

- **Source silence:** `46-CONTEXT.md` D-08/D-09 name exactly two routes (a
  clean scaled-verdict continuation, or "defect or ambiguity → stop and
  surface") but do not, and structurally cannot, pre-decide which of the four
  machine verdicts a real run would return. This register's own "Not recorded
  as gaps" § (below) anticipated the body-permutation confound as a probe
  design input — it correctly routed the *measurement* to the planner rather
  than treating prevalence as a gap in advance — but it did not and could not
  anticipate the specific outcome that 100% confound prevalence would push
  33.4% of corrected-raw residuals over tolerance, short of rule 4's
  unanimity requirement. GAP-46-04 is the first phase artifact to record this
  specific ambiguity; no prior owner ruling addresses what to do when the
  verdict is `VERDICT_AMBIGUOUS` with universal confound prevalence but a
  near-miss corrected-raw-consistency rate.

- **Mathematical / engineering grounding:** Every one of the 1651 eligible
  trajectories (100%) carries two confounds simultaneously: (1) a
  non-identity body-permutation between the resident position array and its
  paired mass vector (`(2,0,1)` for 1547 trajectories, `(0,2,1)` for 104;
  zero show the identity permutation), and (2) a `com_recenter_boost` gauge
  divergence (the resident trajectory's first point of departure from the
  canonical ordered/gauged/scaled pipeline). Structurally, `identity_raw =
  true` for 100% of trajectories and `identity_scaled = false` for 100% —
  every trajectory classifies as "raw-shaped," never "scaled-shaped." Yet
  after correcting for the measured permutation, the raw residual clears the
  numerical tolerance (GAP-46-03 Option A two-term floor) for only 1100/1651
  (66.6%) of trajectories — short of the unanimity `decide_verdict` rule 4
  requires for a clean `VERDICT_TARGETS_ARE_RAW`. This 33.4% shortfall,
  universally attributable to the same two confounds present in 100% of
  trajectories, means the "raw-vs-scaled" question and the "is there a
  permutation/gauge defect" question are entangled in this population in a
  way the probe's own symmetric-hypothesis design (correctly, per D-04)
  refuses to silently resolve. Additionally, all 1651 eligible identities are
  `variant=hierarchical, fidelity=base` — no `standard` or `gold_standard`
  identity survives the three-manifold GAP-46-02 intersection at Stage 0, a
  previously unmeasured population fact whose implication (curriculum design
  vs. labeling artifact) is undecidable from this evidence alone.

- **Agent was tempted to:** (a) round the near-miss 66.6% raw-corrected
  consistency up to a "practically raw" verdict and route the clean-raw
  branch of D-09 — refused; the machine's own unanimity rule (rule 4) exists
  precisely to prevent an executor from making that judgment call, and D-06
  forbids inventing an alternate threshold. (b) Repair the identified
  body-permutation confound inline (it is a well-characterized, mechanically
  simple fix — reorder positions to match `masses_ordered`) — refused; D-09
  and the plan's explicit prohibition forbid any `pinn/` modification under
  any branch, verified clean by `git status --short -- pinn/`. (c) Treat the
  all-hierarchical population composition as either "expected" or "a bug" —
  refused; neither reading is decidable from this evidence alone, so it is
  reported as a measured fact only.

- **What the user needs to decide:**
  - **(A) Treat the confound as the sixth conformance divergence.** Route the
    100%-prevalent permutation + COM/boost confound into Phase 47/48's scope
    alongside the existing `S_H`/loss-math repairs, since the repair
    transform (reorder positions to match `masses_ordered`) is well-
    characterized by this evidence even though probe rule 4 could not
    unanimously confirm it.
  - **(B) Insert a dedicated repair phase between 46 and 47** specifically
    for the permutation/gauge confound, re-run this exact probe post-repair,
    and gate Phase 47 on a clean D-08/D-09-raw verdict from that re-run.
  - **(C) Defer with a recorded risk acceptance** — proceed to Phase 47
    assuming the raw-target reading (supported by the 100% `identity_raw`
    signal) without a unanimous machine verdict, explicitly accepting that
    33.4% of the population remains unexplained.
  - **(D) Request a widened or corrected probe** (e.g. a permutation-
    corrected symmetric-hypothesis re-run) before any scope decision, to
    determine whether correcting the confound analytically would also
    resolve rule 4's unanimity requirement.

- **Confidence of impact:** HIGH — Phases 47-52 and the single EVAL-01 look
  all depend on the frame this branch settles; GAP-46-01's evaluator-pairing
  resolution (already RESOLVED-WITH-INSTRUCTION, binding Phase 50/51) is also
  directly downstream of which reading ultimately prevails.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** User instruction 2026-07-27 selected **Option A —
  treat the confound as the sixth conformance divergence.** The
  100%-prevalent body-permutation (masses paired against un-permuted
  positions) and `com_recenter_boost` gauge divergence are routed into
  Phase 47/48's scope alongside the already-planned `S_H`/loss-math repairs,
  using the repair transform this evidence already characterizes (reorder
  the resident position array to match `masses_ordered`) even though probe
  rule 4 could not unanimously confirm the raw-vs-scaled question on its own.
  This ruling decides **where the repair work happens**, not the CONF-01
  verdict itself: `VERDICT_AMBIGUOUS` stands as measured evidence and is not
  retroactively upgraded to `VERDICT_TARGETS_ARE_SCALED`. Plan 46-07 remains
  gated on a clean D-08 verdict, which this run did not produce and cannot
  retroactively produce — 46-07 is unblocked only by a future clean
  conformance verdict (expected as an output of Phase 47/48's repair plus a
  follow-up re-verification, which Phase 47/48's own planning must specify;
  not invented here).

- **Blocking scope (resolved, dependency-scoped):** Plan 46-07 (INST-01
  production wiring) remains BLOCKED — this resolution routes the repair, it
  does not supply a clean verdict. Phase 47's scope now explicitly includes
  the body-permutation + COM/boost repair alongside the pre-existing
  `S_H`/loss-math work. The frame-independent INST-01 deliverables already
  shipped in Waves 1-3 (46-01, 46-02, 46-03, 46-05 — fixtures, probe core,
  gate-composition module, isolation/artifact test suites) are complete and
  unaffected. Position 3 of the `phase-46-execution` watchdog chain has this
  gap's resolution recorded but its done marker remains withheld, since
  46-07 — the task literally bound to that chain position — is still not
  executable.

- **SUPERSEDED IN PART by GAP-46-05 (2026-07-27, same day).** This ruling's
  routing of the repair to "Phase 47/48" proved circular: Phase 47 is gated on
  Phase 46, and 46-07 was gated on Phase 47/48's repair, so neither phase could
  start. GAP-46-05 (owner instruction, option A) moves the **minimum** repair —
  body permutation + COM-recentre/boost gauge — and its follow-up CONF-01 re-probe
  into Phase 46 as new requirement CONF-08, restoring a satisfiable order. Every
  other element of this ruling stands unchanged: `VERDICT_AMBIGUOUS` is still not
  retroactively upgraded, 46-07 is still unblocked only by a clean verdict, and
  conformance repair beyond the minimum remains routed to Phases 47/48.

---

## GAP-46-05 — GAP-46-04's Option-A routing leaves Phase 46 and Phase 47 mutually blocking: Plan 46-07 waits on a repair that Phase 47 may not begin until Phase 46 closes. Where does the minimum repair live?

- **Decision point:** GAP-46-04's resolution (option A, 2026-07-27) routes the
  body-permutation + COM/boost repair into Phase 47/48 while explicitly holding
  Plan 46-07 blocked until that repair produces a clean conformance verdict. But
  Phase 47 is itself gated on Phase 46. The two conditions cannot both be
  satisfied: Phase 46 cannot close without a repair only Phase 47 may perform,
  and Phase 47 may not start until Phase 46 closes. The milestone is deadlocked
  at its first phase, and the deadlock is structural rather than evidentiary — no
  additional measurement resolves it.

- **Where in artifact:**
  - `.planning/milestones/v2.2-GAPS.md` § "Open gaps" — "Plan 46-07 stays BLOCKED
    regardless … Phase 47/48 planning must carry both the pre-existing `S_H`/loss-math
    repair and this body-permutation + COM/boost repair, and must specify the
    follow-up conformance re-verification that would actually unblock 46-07-equivalent
    wiring."
  - `.planning/ROADMAP.md:103` — Phase 47 "**Depends on**: Phase 46 — `K0`/`Uabs0`
    are frame-dependent (`H' = D·H`), so the frame must be settled before the median
    is computed."
  - `.planning/ROADMAP.md:92` — Plan 46-07 "blocked until D-08 or owner-resolved D-09".
  - `.planning/ROADMAP.md:177` — "Execution Order: 46 → 47 → 48 … strict dependency order".
  - `46-GAPS.md` § GAP-46-04 "Blocking scope (resolved, dependency-scoped)".

- **Task context:** Phase 46 orchestration review, 2026-07-27, immediately after
  GAP-46-04 was resolved and committed (`997c731b`). The deadlock was surfaced by
  the owner while assessing whether Phase 46 could proceed to UAT. No plan was
  executing at the time.

- **Classification:** cross-phase reframing. Resolving it moves scope between
  phases and changes Phase 46's requirement set, Phase 47's entry condition, and
  the milestone's requirement count — none of which a planner or executor may
  decide inline.

- **Source silence:** `46-CONTEXT.md` D-08/D-09 define the branch routing but
  presume the D-09 "stop and surface" ends in an owner ruling that either supplies
  a frame or defers the phase; neither anticipates a ruling that routes repair
  downstream while holding the current phase open. ROADMAP Phase 46 success
  criterion 2 pre-authorized "Phases 47–48 grow accordingly" on a frame defect,
  but was written on the assumption that Phase 46 would still be *closable* once
  the branch was surfaced — it does not address a defect whose repair is itself a
  precondition of Phase 46's own last plan. GAP-46-04's option menu listed both
  (B) "insert a dedicated repair phase between 46 and 47 … and gate Phase 47 on a
  clean verdict from that re-run" and (D) "request a … permutation-corrected
  symmetric-hypothesis re-run before any scope decision"; the selected option A
  named neither, and no source states which phase owns the repair when A's routing
  proves circular.

- **Mathematical / engineering grounding:** The confound is a mass↔position index
  mismatch, verified in code: `pinn/data/preprocessing.py:186` computes the
  COM-recentred, boost-removed series via `_com_recenter_and_boost`, and `:188-189`
  computes `permutation = _canonical_order(...)` then `masses_ordered = masses[permutation]`;
  `pinn/data/adapter.py:865` stores `pre.masses_ordered` (permuted, gauged basis)
  beside `:863` `parsed_brutus.positions` (neither permuted nor gauged). Measured
  prevalence is 1651/1651, with permutation `(2,0,1)` for 1547 trajectories and
  `(0,2,1)` for 104 — the identity permutation never occurs.

  Every downstream quantity Phase 47 computes is mass-weighted and therefore
  invalid under this mismatch. `S_H = median_train(K₀ + U_abs,0)` is built from
  `K = ½ Σᵢ mᵢ‖vᵢ‖²` and `U = Σ_{i<j} G mᵢmⱼ/‖rᵢ−rⱼ‖`: pairing mass index *i* with
  position index *σ(i)* computes both terms for a different three-body system than
  the trajectory came from. Since `ε_H = 1e-4 · S_H` is the energy-residual
  normalizer for the whole loss, a permuted `S_H` silently mis-scales every
  energy term in the milestone. The same mismatch corrupts the Newtonian residual
  `f_i = Σ_{j≠i} G m_j (r_j − r_i)/(‖r_j−r_i‖² + ε)^{3/2}` that CONF-04's `R̄`
  aggregates, and the locked mass-weighted COM projection head (v1.4 D-02), which
  projects on `Σ mᵢ rᵢ / Σ mᵢ`. Computing `S_H` before the repair therefore does not
  merely risk a wrong number — it guarantees one, and Phase 47's sole deliverable
  would have to be discarded and recomputed. This is the engineering reason the
  repair cannot follow the phase that consumes it.

  A second-order consequence bounds the repair's scope honestly: the probe reports
  `first_diverging_step`, and it reports `com_recenter_boost` for 100% of
  trajectories. "First" means the canonical-pipeline walk halts there, so the
  conformance of the *later* steps — `_canonical_order` ordering of the position
  series, `_rotation_gauge` (preprocessing.py:195), and the `D` scaling — is
  unmeasured, not established. Repairing permutation + COM/boost may therefore
  move `first_diverging_step` to `rotation_gauge` rather than clearing it. That is
  an expected outcome of walking a pipeline in order, not a failed repair, and it
  does not license iterating against the probe's output: each repair step is
  defined by the canonical pipeline in `preprocess_trajectory`, never by which
  transform makes the residual fall below tolerance (SCOPE-29).

- **Agent was tempted to:** (a) Close Phase 46 with Plan 46-07 descoped to Phase
  47 or a new phase, treating the deadlock as a plan-sequencing detail — refused;
  that silently marks CONF-01 ("Resolve RG-02") complete while RG-02 is measurably
  unresolved, and EVAL-01 precondition (ii) is literally "RG-02 resolved", so the
  falsehood would propagate to the single authorized evaluation. (b) Perform the
  repair inline under GAP-46-04's existing option-A authority, on the reading that
  "Phase 47/48 scope" loosely means "downstream repair work" — refused; option A
  names the phases explicitly, and reallocating scope between phases is the
  cross-phase-reframing class this protocol reserves for the owner. (c) Insert a
  decimal Phase 46.5 rather than extending Phase 46 — not refused on principle
  (it is GAP-46-04's own option B, and ROADMAP:52 reserves decimals for urgent
  insertions), but not selected: the owner directed the work into Phase 46.

- **What the user needs to decide:**
  - **(A) Move the minimum repair and the follow-up probe into Phase 46.** Phase 46
    grows by two plans (repair, re-probe); Phase 47 keeps its existing entry
    condition and receives a corrected corpus. Phase 46 closes on a clean verdict.
  - **(B) Insert a decimal Phase 46.5** owning the repair + re-probe, close Phase 46
    with 46-07 moved into 46.5, and gate Phase 47 on 46.5 (GAP-46-04 option B).
  - **(C) Descope Plan 46-07 to Phase 49** and let Phase 47 open on the permuted
    corpus, accepting that `S_H` is recomputed after the repair lands.

- **Confidence of impact:** HIGH — this decides whether the milestone can advance at
  all, and it governs whether Phase 47's `S_H` is computed on a corrected or a
  corrupted corpus.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** Owner instruction 2026-07-27 selected **Option A — move the
  minimum permutation/gauge repair and the follow-up frame probe into Phase 46.**
  Verbatim: *"Resolve it by moving the minimum permutation/gauge repair and follow-up
  frame probe into Phase 46… Re-plan Phase 46 so the execution order becomes:
  data-path repair → repeat CONF-01 probe → clean frame verdict → Plan 46-07 wiring."*
  The owner further ruled (2026-07-27, in the same instruction round) that this scope
  is traced as a **new requirement CONF-08 owned by Phase 46**, rather than absorbed
  into CONF-01's branch-point clause — matching the convention by which each earlier
  conformance divergence received its own CONF identifier, and giving INST-03's
  known-divergence register and the VER-20 handoff a stable ID to cite. The milestone
  moves from 22 to 23 requirements.

  **Minimum is defined by the evidence, not by convenience.** The repair covers the
  body permutation and the COM-recentre/boost gauge — the two transforms the confound
  register actually measured — applied to the resident position and velocity series so
  they share `masses_ordered`' basis. It explicitly does **not** apply the `D` scaling,
  because that is the raw-vs-scaled question CONF-01 exists to answer and pre-applying
  it would decide the verdict by construction. Rotation gauge is out of the minimum
  repair unless the re-probe measures it as the new `first_diverging_step`.

- **Blocking scope (resolved):** Phase 46 gains plans 46-08 (repair, wave 5) and
  46-09 (re-probe + verdict, wave 6, `autonomous: false` — owner branch point);
  Plan 46-07 moves to wave 7 and stays gated on 46-09 producing a clean verdict. Its
  Task-1 hard gate required one repoint — it read `46-VERDICT.md`, which after the repair
  is the superseded pre-repair measurement, so it now reads `46-VERDICT-POSTREPAIR.md` and
  treats that file's absence as state (c) BLOCKED. The gate's three-state logic, its
  prohibition on inferring a frame, and its BLOCKED reporting path are otherwise unchanged. Phase 47's stated dependency on
  Phase 46 is unchanged and is now satisfiable. CONF-01 and INST-01 revert from
  Complete to Pending (both were marked Complete prematurely — see the
  correction note below). GAP-46-04's option-A routing is **superseded in part**:
  the minimum repair moves to Phase 46; any residual conformance repair beyond the
  minimum remains routed to Phases 47/48 as that ruling directed.

- **Correction recorded with this gap:** `REQUIREMENTS.md` marked **CONF-01** and
  **INST-01** `Complete` before either was true. CONF-01 reads "Resolve RG-02"; RG-02
  is measurably unresolved (`VERDICT_AMBIGUOUS`), and EVAL-01 precondition (ii) is
  "RG-02 resolved", so the false marking sat directly on the gate protecting the single
  authorized evaluation. INST-01's production wiring is Plan 46-07, which has never
  executed. Both revert to Pending under this resolution. This is a factual repair of
  the traceability record, not a scope change.

---

## GAP-46-06 — The successful minimum repair leaves residency at an ordered COM/boost-gauged raw-scale intermediate that the unchanged v1 probe classifies as `VERDICT_NON_FRAME_DIVERGENCE`. What contract or frame does Phase 46 use next?

- **Decision point:** The one authorized post-repair probe returned
  `VERDICT_NON_FRAME_DIVERGENCE` (rule 5, D-09), not a clean raw or scaled
  verdict. CONF-08's repair is nevertheless exact:
  `stepwise_attribution.plus_permutation = 0.0` for 1651/1651 trajectories, so
  resident positions and `masses_ordered` now address the same canonical
  bodies in the COM/boost gauge. The owner must decide whether Phase 46 should
  revise the post-repair probe contract, ratify an operational frame by
  instruction, authorize a further canonical transform and measurement, or
  defer the phase.

- **Where in artifact:**
  - `evidence/target-frame/20260728T014532Z/raw.json`:
    `.verdict`, `.rationale`, `.aggregates`, and
    `.trajectories[].confounds.stepwise_attribution`
  - `46-VERDICT-POSTREPAIR.md` §§ "Pre/post comparison", "Confound register",
    and "Branch: D-09"
  - `pinn/verification/target_frame_probe.py:620-643` — identity and canonical
    permutation booleans
  - `pinn/verification/target_frame_probe.py:658-695` — stepwise attribution and
    unconditional inverse-permutation correction
  - `pinn/verification/target_frame_probe.py:887-893` — rule-5 D-09 classifier
  - `pinn/data/adapter.py:861-875` — the repaired resident surface

- **Task context:** Surfaced during Plan 46-09 Task 3 after all four pre-run
  gates passed and the single permitted measurement completed. The unchanged
  instrument and population reproduced both controls exactly. The hypothesis
  arms moved, but the machine returned its grounded non-frame route. Per
  fable-mode's truth and failure-visibility gates, the result is preserved
  without retuning, rerunning, or self-ratifying.

- **Classification:** cross-phase reframing (+ semantic probe-contract
  ambiguity) — the ruling determines what Phase 46 calls the resident frame,
  whether a new evidence instrument/run is authorized, and whether Phase 47
  may begin. It also changes the acceptance meaning of CONF-01 and therefore
  the roadmap's frame-first dependency.

- **Source silence:**
  - `46-CONTEXT.md:60-68` requires two symmetric hypotheses and explicit
    coordinate conventions but does not specify how to classify an intentionally
    resident, ordered COM/boost-gauged raw-scale intermediate.
  - `46-CONTEXT.md:70-78` requires non-frame divergences to be preserved and
    owner-routed; it supplies no resolution for one found after the authorized
    minimum repair.
  - `46-CONTEXT.md:105-116` supplies D-08/D-09 routing and requires this gap,
    but deliberately reserves the branch resolution to the owner.
  - `46-02-SUMMARY.md:85-100` fixes rule 5 as a D-09
    `VERDICT_NON_FRAME_DIVERGENCE` route; it does not define a postrepair-aware
    third identity arm.
  - `46-09-PLAN.md:60-72` enumerates clean raw, clean scaled, and repeated
    ambiguity, anticipating that the first divergence might move to rotation
    or scaling. It does not anticipate rule 5 remaining stable because the
    unchanged attribution algorithm compares the ordered resident against the
    earlier unpermuted intermediate first.
  - `46-09-PLAN.md:153-169` requires pre/post confound comparison and owner
    routing, but only spells out creation of GAP-46-06 for a repeated
    `VERDICT_AMBIGUOUS`; it does not authorize self-resolving the equally
    explicit D-09 non-frame outcome.
  - `46-08-SUMMARY.md:72-110` proves the intended repair boundary and that no
    rotation or global scaling was applied. It does not choose which resulting
    coordinate convention validation should ratify.

- **Mathematical / engineering grounding:** The repaired resident is
  `r_bar_perm = P(r - R_COM0 - V_COM t)`: raw dimensional length, zero-COM and
  zero-COM-velocity gauge, canonical body order, no rotation gauge, and no
  division by `D`. Translation, uniform boost, and simultaneous body
  permutation are symmetries/relabelings of Newtonian three-body dynamics when
  positions, velocities, and masses transform together. They do not select the
  dimensionless scaled frame `r' = R0 r_bar_perm / D`, nor do they make
  `r_bar_perm` byte-identical to parsed file-order raw `r`.

  The probe's two identity tests admit only those endpoints:
  file-order parsed raw (`positions_vs_parsed`) and fully
  ordered/rotated/scaled (`positions_vs_r_gauge`). The repaired intermediate is
  therefore `identity_neither` by construction. Its stepwise loop tests
  `r_bar` before `r_bar_perm`, so an ordered resident first differs at the
  label `com_recenter_boost` even though it exactly equals the very next
  intermediate. Finally, the "corrected raw" arm applies the inverse canonical
  permutation to stored masses unconditionally. That operation repaired the
  old file-order-position/ordered-mass mismatch; after CONF-08 it creates the
  mismatch, which is why corrected-raw consistency moves from 1100/1651 to
  0/1651 while the direct raw hypothesis moves from 0/1651 to 1086/1651.

  A validation frame must still pair positions and time coherently. The locked
  future contract is canonical scaled `r'` with `u=t/T`, while the historical
  raw reading is parsed raw `r` with native `t`. Treating `r_bar_perm` as
  either endpoint without an explicit gauge/frame ruling changes target
  semantics and downstream validation assembly. Conversely, applying rotation
  and `D/V` scaling now would establish the scaled endpoint by construction,
  not independently measure raw-versus-scaled residency. The options therefore
  have materially different scientific and engineering consequences.

- **Agent was tempted to:** (a) call the 1086/1651 uncorrected-raw consistency
  a "raw verdict" — refused because rule 4 requires unanimity and identity-raw,
  neither of which holds. (b) infer that rotation is the next divergence from
  `plus_permutation = 0.0` and apply it — refused because the single measured
  result does not authorize another transform. (c) patch the probe's
  discriminators and re-run — refused because Plan 46-09 permits exactly one
  completed measurement with the unchanged instrument. (d) treat rule 5 as a
  tool bug and proceed to 46-07 — refused because rule 5 is explicitly a
  grounded D-09 route.

- **What the user needs to decide:**
  - **(A) Authorize a postrepair-aware probe revision and one new measurement.**
    Add an explicit ordered COM/boost-gauged raw intermediate identity arm;
    define pairing status by resident/mass alignment rather than whether the
    canonical permutation is identity; make the inverse-mass correction
    conditional on the resident convention; and make stepwise attribution
    report the matching/latest canonical intermediate. Keep Phase 46 stalled
    and author a new plan before changing the instrument.
  - **(B) Ratify an operational raw/native validation frame by instruction.**
    Treat the repaired order and COM/boost gauge as symmetry-equivalent to raw
    positions for conservation validation, explicitly accept that the current
    raw arm clears tolerance for only 1086/1651 trajectories, and authorize
    46-07 to wire that named pair. This is an owner override of the machine
    verdict, not a clean CONF-01 measurement.
  - **(C) Authorize the remaining canonical transform to the locked scaled
    contract, then create new evidence.** Apply rotation plus `D/V` scaling in
    a separately planned repair and remeasure. This makes future residency
    conformant but establishes scaled targets by specified transformation
    rather than by the original symmetric raw-vs-scaled diagnosis.
  - **(D) Defer Phase 46.** Leave GAP-46-06 open/deferred and carry the
    probe-contract/frame adjudication into a later milestone. Phase 46,
    46-07, Phase 47, and downstream frame-dependent work remain blocked.

- **Confidence of impact:** HIGH — this ruling controls the frame named by
  INST-01, the input to Phase 47's mass-weighted `S_H`, and whether the
  milestone's single held-out evaluation is ever eligible to run.

- **Status:** OPEN

- **Resolution note:**

- **Blocking scope:** Plan 46-07, Phase 46 closure, Phase 47, and all
  frame-dependent downstream work. Independent evidence review may continue;
  no further repair, probe run, or frame ratification is authorized.

---

## Not recorded as gaps

Recorded here so the reasoning is re-derivable and the same candidates are not
re-litigated later.

- **Body-permutation prevalence in the real corpus** (research candidate C2). The
  masses stored beside the resident positions are `pre.masses_ordered`
  (`pinn/data/adapter.py:865`), i.e. canonically reordered by
  `preprocessing._canonical_order`, while the positions are the un-permuted
  `parsed_brutus.positions` (`adapter.py:863`). How often that permutation is
  non-identity is unmeasured. This is **not** a gap: `46-CONTEXT.md` D-04 already
  requires CONF-01's probe to carry controls that distinguish a pure `D`-scaling
  mismatch from body-permutation, COM/boost, rotation-gauge, and metadata-pairing
  mismatches. The question is the phase's own deliverable, not a source silence.
  It is routed to the planner as a design input: the permutation-identity check is a
  pure per-trajectory boolean with no tolerance judgement, so it belongs among the
  first and cheapest discriminators.
