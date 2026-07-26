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

- **Status:** OPEN

- **Resolution note:** *(empty — awaiting owner instruction)*

- **Blocking scope (dependency-scoped):** Does **not** block Phase 46 planning or
  execution. Phase 46's INST-01 builds its own validation-side composition in the
  coherent frame per D-12, and D-12/D-13 already prescribe how to behave if the
  CONF-01 branch selects an alternate pair. Blocks nothing until Phase 50/51 planning,
  where it must be resolved before EVAL-01 is spent.

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

- **Status:** OPEN

- **Resolution note:** *(empty — awaiting owner instruction)*

- **Blocking scope (dependency-scoped):** Blocks **46-06** (the one real-corpus evidence
  run) and therefore 46-07. Waves 1–3 (46-01 through 46-05) are unaffected — they are
  synthetic/dataset-free and manifest-agnostic.

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

- **Status:** OPEN

- **Resolution note:** *(empty — awaiting owner instruction)*

- **Blocking scope (dependency-scoped):** Blocks the tolerance constant in **46-02** only.
  46-01 and the INST-01 strand (46-03, 46-05) are unaffected. Cheap to ratify; the planner
  supplied a complete rationale.

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
