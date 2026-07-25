# Phase 45 Gap Register — trainex-r2 ERW Package Assembly

Phase-local STOP-protocol gap register for Phase 45 (milestone v2.1). Each entry
is a source-silent decision that this phase **surfaced** rather than decided, per
the CLAUDE.md STOP protocol and the ROADMAP "STOP-protocol spirit" clause. The
milestone-wide index is `.planning/milestones/v2.1-GAPS.md`.

All four gaps below surfaced **after** package delivery, during the mandatory
verification of the returned Route B (open-book) research report — ERW runbook
Rule 19. They are recorded here because Phase 45 owns the delivery and its
return path; several are *about* content owned elsewhere (the framework specs,
the v2.0 build phases) and are indexed as such.

Supporting evidence for all four:
- `docs/work/reviews/milestone_v2.1/45-trainex-r2-erw-package-assembly/2026-07-24-trainex-r2-report-factw-verification.md`
- `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-24-stage0-training-path-conformance-audit.md`

---

## GAP-45-01 — What is the component reduction in the locked `L_data` formula?

- **Decision point:** `pinn_architecture.md` §3.1 locks
  `L_data = (1/N_t) Σ_n Σ_i Huber_δr(r'_θ,i(u_n) − r'_i(u_n))`. The Huber argument
  is a 3-vector and the formula specifies no reduction over spatial components, so
  the expression is not scalar as written. Read as an implicit sum over components,
  the spec value is 9× the implemented value; read as a mean, the implementation
  matches. Which reduction does the locked formula intend?

- **Where in artifact:**
  `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` §3.1
  (the locked formula); `pinn/loss_catalog.py:173-188` (`data_huber_loss`, which
  applies `.mean()` over the full `(N_t, 3, 3)` tensor); conformance audit finding
  **C-07**.

- **Task context:** Bounded conformance audit of the executed Stage-0 training
  path against the locked specs, run to establish the full divergence inventory
  after the trainex-r2 report's spot-findings were confirmed. Every other loss
  term's reduction (`L_IC` (1/3)Σ, `L_L` (1/(3N_t))ΣΣ, `L_phys` (1/N_t)Σ, `L_E`
  (1/N)Σ) is stated unambiguously in spec and matches the implementation; `L_data`
  is the only term whose reduction is under-specified.

- **Classification:** semantic — a loss-term normalization that changes relative
  term weighting.

- **Source silence:**
  - `pinn_architecture.md` §3.1 states the sums over `n` and `i` and the Huber
    delta, and no reduction over the 3 spatial components.
  - The §3.1 Phase 35 LOSS-01 contract note specifies units, frames, and which
    file owns the component math; it does not state the reduction.
  - `ctl_instruction.md:1749` (total-loss assembly) treats `L_data` as an opaque
    scalar with implicit coefficient 1; it does not define the reduction.
  - The neighbouring terms' formulas each state their own normalizing factor
    explicitly, which makes `L_data`'s omission an ambiguity rather than an
    established convention that can be read across.

- **Mathematical / engineering grounding:** `L_data` is the only loss term whose
  coefficient is pinned at 1 (`ctl_instruction.md:1749`; `scheduled_weights.py`
  documents `lambda_data = 1.0 (fixed, §3.1 unweighted data term)`). Every other
  term carries a schedulable λ. A factor-9 ambiguity in the one unweighted term is
  therefore not a cosmetic scaling — it is a factor-9 change in the *relative*
  weight of data fidelity against physics, IC, energy, and angular-momentum terms,
  and it cannot be absorbed by any λ the spec allows to be tuned. Dimensionally
  both readings are consistent (Huber of a dimensionless quantity), so dimensional
  analysis cannot settle it. The mean reading makes `L_data` a per-coordinate
  average error, comparable in magnitude to a per-coordinate residual; the sum
  reading makes it a per-snapshot total, comparable to a whole-configuration error.
  Which is intended determines whether the pilot's observed data-term dominance
  (DIAG-02 F-07/F-09) reflects the specified balance or a 9× under-weighting of
  data relative to spec. First-principles physics does not select between them:
  this is a modelling convention, not a derivable fact.

- **Agent was tempted to:** accept the implementation's mean reading, on the
  grounds that it matches `torch.nn.functional.huber_loss` default behavior, that
  `tests/phase38/test_loss_catalog.py:58` already asserts that equivalence, and
  that a per-coordinate average is the more common convention in PINN
  implementations. That is an argument from convention and from live code, and
  live code is not a grounding source for spec intent.

- **What the user needs to decide:**
  - **(A)** Mean over all components — the implementation is correct as written;
    the spec formula gains an explicit `1/(3·3)` or a stated per-component-mean
    convention.
  - **(B)** Sum over components (mean over time only) — the implementation is a
    9× under-weighting of the data term and must be corrected; the spec formula
    gains an explicit component sum.
  - **(C)** Defer to the next milestone's conformance-fix phase, bundled with the
    other divergence corrections so all loss-term scalings are ruled on together.

- **Confidence of impact:** MEDIUM-HIGH — no effect on whether the gate failed
  (the failure margin is ~7 orders of magnitude), but a direct effect on term
  balance in any re-run, and it is the one loss scaling that no λ can compensate.

- **Status:** DEFERRED

- **Resolution note:** Owner instruction 2026-07-24 (interactive session,
  AskUserQuestion): **Option C — defer to the next milestone's conformance-fix
  phase**, bundled with the other divergence corrections so every loss-term scaling
  is ruled on together with the term-balance consequences visible side by side.
  Conditions carried with the deferral:
  1. **This gap must be resolved before any Stage-0 re-run**, not merely before the
     milestone closes. A re-run under an unresolved 9× ambiguity in the one
     unweighted loss term would produce another result that cannot be interpreted —
     the exact failure mode this whole investigation exists to prevent.
  2. The conformance-fix phase must present both readings **with computed term
     magnitudes** from the retained runs, so the choice is made against numbers
     rather than convention.
  3. **Live code remains non-grounding.** That the implementation chose the mean,
     and that a passing test asserts equivalence with `torch.nn.functional.huber_loss`,
     are facts about the implementation — not evidence of spec intent. The deferral
     must not decay into ratifying the status quo by default.
  4. Whichever reading wins, the spec formula gains an explicit reduction — a spec
     edit, routed to a spec-editing milestone (out of scope for v2.1, SCOPE-24).

---

## GAP-45-02 — Was `λ_E^max = 1.0` at Stage 0 an authorized calibration choice or unratified drift?

- **Decision point:** The locked PHYS-05 schedule sets `λ_E^max(k) = 0` for
  `k ∈ {0,1}`. All four executed run configs set `loss.lambda_e_max: 1.0` — the
  Stage-6 value — and the per-step logs confirm λ_E ramping to 1.0 and holding for
  the whole run. `scheduled_weights.py`'s own defaults are the locked Stage-0
  values, so the divergence entered via config override. Whether that override was
  owner-sanctioned is not recorded anywhere.

- **Where in artifact:**
  `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:663`
  (locked schedule); `runs/stage0-pilot-seed{41,42,43}/config.yaml:6` and
  `runs/stage0-smoke/config.yaml:6`;
  `runs/stage0-pilot-seed42/logs/train.log.jsonl` (`lambda_e` field);
  `pinn/training/scheduled_weights.py` (spec-faithful defaults); conformance audit
  finding **C-05**; trainex-r2 report gap RG-01.

- **Task context:** Verification of the trainex-r2 report's SV-1 claim, then the
  conformance audit. The *fact* of the divergence is established beyond doubt; its
  authorization is what cannot be determined.

- **Classification:** process — a ratification-record question, with semantic
  consequences for how the pilot's failure is interpreted.

- **Source silence:**
  - `runs/*/config.yaml` records the value, never its provenance or authorization.
  - `43-CALIBRATION.md`'s ratification record covers the guards, the RECOVER
    retry budget, and the checkpoint wall-clock ceiling (R-1, R-2, D4-a, B-5). It
    does not mention λ_E or the PHYS-05 schedule.
  - `43-VERDICT.md` reports the gate outcome; it does not enumerate the executed
    weight vector against the locked schedule.
  - `.planning/STATE.md` "Decisions" records five owner-carved v2.0 seams
    (D1-p precision, D4-a ceiling, R-1/R-2 thresholds, B-5 resume fields). λ_E is
    not among them.
  - `pinn/training/scheduled_weights.py` describes the per-stage caps as
    "provisional seams (CTX-38) … awaiting pilot calibration" — the code's own
    reading, not an owner ratification.
  - Chat history is not available to this session as a searchable record for
    2026-07-21/22 (the smoke and pilot window).

- **Mathematical / engineering grounding:** λ_E multiplies the soft-energy
  conservation term. Setting it to zero at Stage 0 is a deliberate curriculum
  choice: the earliest stage teaches trajectory fidelity and the physics residual,
  and defers explicit conservation regularization until later stages when the
  network already tracks the dynamics — the schedule ramps λ_E in only from k=2
  (`10^(k-4)`, i.e. 0.01) and reaches 1 only at k=5. Running Stage 0 with λ_E = 1
  therefore imposes the *final-stage* conservation pressure on an untrained
  network, which is a materially different optimization problem: the energy term
  competes with data fidelity from the first warmup step. Whether that is harmful
  is genuinely open — one could argue conservation pressure early is beneficial —
  but it is not the specified experiment. The consequence for interpretation is
  concrete: the trainex-r2 question set (Q3) asks how to weight losses in a Stage 0
  where "conservation weights are zero by design," and no retained run instantiates
  that configuration, so Q3's premise describes no executed run. The answer also
  determines the classification of C-05: an authorized calibration is a *choice*
  whose consequences are a legitimate research question, while unratified drift is
  a *defect* whose correction is mandatory before the design can be tested.

- **Agent was tempted to:** classify it as unratified drift, since no ratification
  record mentions it and the code's own comments call the caps provisional. But
  absence of a record in the artifacts this session can read is not proof of
  absence of an owner decision, and the classification changes whether the next
  milestone treats this as a bug fix or as a live experimental variable.

- **What the user needs to decide:**
  - **(A)** It was unratified drift. C-05 is a defect; the config is corrected to
    the locked Stage-0 value (0) before any re-run.
  - **(B)** It was an authorized calibration choice. Record the authorization
    retroactively with its rationale; λ_E at Stage 0 becomes an explicit
    experimental variable rather than a conformance defect, and GAP-45-03's lock
    boundary must then permit it.
  - **(C)** Cannot recall / unknown. Treat as drift for correctness purposes
    (revert to the locked 0) while noting the provenance is unrecoverable.

- **Confidence of impact:** HIGH — determines whether the pilot's conservation
  pressure was intended, which loss-balance questions are live for the next
  milestone, and whether C-05 is filed as a defect or a variable.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** Owner instruction 2026-07-24 (interactive session,
  AskUserQuestion): **Option C — provenance unknown / not recalled; treat as
  drift.** The owner does not recall authorizing `λ_E^max = 1.0` at Stage 0, and no
  retained artifact records an authorization. Rulings:
  1. **Treated as unratified drift for correctness purposes.** The config reverts
     to the locked Stage-0 value `λ_E^max = 0` before any Stage-0 re-run.
  2. **Provenance is recorded as unrecoverable**, not as proven-absent. Absence of
     a record in the readable artifacts is not proof no decision was made; this
     entry states what could and could not be established.
  3. Combined with GAP-45-03 Option A (per-stage values locked), conformance audit
     finding **C-05 is a defect**, not an experimental variable. It carries no
     experimental-variable status and needs no waiver.
  4. Whether Stage-0 conservation pressure is *worth* studying deliberately later
     is untouched by this ruling — it would be a new, explicitly-authorized
     experiment against a conformant baseline, not a reinterpretation of the v2.0
     pilot.
  5. Follow-on hygiene, noted not decided: the run-record format does not capture
     *why* a config value deviates from spec. The verification charter's preflight
     placeholder-census and waiver policy (§5 layer 1, §6) is where that gets
     fixed; this gap is the concrete motivating case.

---

## GAP-45-03 — Where is the PHYS-05 lock boundary: the per-stage λ values, or only the schedule form plus the ≤1 cap?

- **Decision point:** `pinn_architecture.md` §4.1 presents the warmup schedule
  including explicit per-stage `λ^max(k)` values, while the same section calls
  `λ_phys^max(k) = 1` a "default"; the Phase 35 LOSS-02 contract says "Retain the
  PHYS-05 warmup schedule above with `lambda_E^max <= 1`"; and the implementation
  treats the per-stage values as config-overridable provisional defaults while
  enforcing only the ≤1 cap. Is the locked object (i) the schedule *form* plus the
  ≤1 cap, with per-stage values calibration-open, or (ii) the per-stage values
  themselves?

- **Where in artifact:**
  `pinn_architecture.md:657-667` (schedule, "default" wording, Phase 35 LOSS-02
  contract note); `ctl_instruction.md:1759` (the restated contract);
  `pinn/training/scheduled_weights.py:37-81` ("provisional seams (CTX-38)… the
  `lambda_E^max <= 1` invariant is the one hard cap");
  `tests/phase40/test_scheduled_weights.py:81`
  (`test_lambda_e_max_cap_enforced_at_construction` — asserts the cap, not the
  per-stage table); conformance audit finding **C-08**; trainex-r2 report gap RG-09.

- **Task context:** The conformance audit found that the test suite encodes the ≤1
  cap and leaves the per-stage table unguarded — the ambiguity materialized as a
  test-coverage asymmetry. This gap is the governance question underneath
  GAP-45-02: whether λ_E = 1.0 at Stage 0 is even *capable* of being a violation
  depends on which object is locked.

- **Classification:** process-artifact schema — defines what "locked" means for a
  spec table, and therefore what a conformance check may assert.

- **Source silence:**
  - §4.1 presents the per-stage values in the same bulleted block as the warmup
    formula, with no marker distinguishing locked values from defaults, while
    calling one adjacent quantity a "default."
  - The Phase 35 LOSS-02 note says "retain the schedule above **with**
    `lambda_E^max <= 1`" — grammatically the cap is an additional constraint on a
    retained schedule, but it does not say whether the retained per-stage values
    are themselves binding.
  - `.planning/milestones/v1.6-phases/35-loss-energy-weight-contracts/` evidence
    (`m15-energy-weight-schedule.md`) rejects the issue-doc replacement table; it
    does not state the lock granularity of the surviving one.
  - No spec convention is stated anywhere for how to mark a value locked vs
    default within a table.

- **Mathematical / engineering grounding:** The two readings license different
  engineering behavior, and the difference is not cosmetic. Under (i), a run may
  set any `λ_E^max ≤ 1` at any stage, the curriculum's conservation-deferral
  structure is advisory, and a preflight conformance check can assert only the
  cap — meaning C-05 is not a violation at all and the only enforceable invariant
  is a bound. Under (ii), the per-stage values are the contract, the deferral
  structure (zero at k∈{0,1}, `10^(k-4)` ramp at k∈{2,3,4}, unity at k∈{5,6}) is
  itself a locked scientific decision about how conservation pressure should enter
  the curriculum, and a preflight check must assert the whole table. The scientific
  content of the schedule favors (ii): the specific form `10^(k-4)` encodes a
  three-decade geometric ramp tied to stage index, which is a designed statement
  about how fast conservation pressure should grow, not an arbitrary default. But
  the "default" wording on the adjacent `λ_phys^max` line and the Phase 35 cap
  framing genuinely support (i). This also determines what the verification
  regime's layer-1 preflight gate is allowed to block on, so it must be settled
  before that gate is built.

- **Agent was tempted to:** read (ii) — the per-stage values are locked — because
  the geometric ramp carries evident design intent and because reading the values
  as free makes the table nearly contentless. But this defines what "locked" means
  for framework-spec tables generally, which is a process-artifact schema decision
  the agent must not invent.

- **What the user needs to decide:**
  - **(A)** The per-stage values are locked. Overriding any of them is a
    conformance violation; preflight asserts the full table; C-05 is a defect.
  - **(B)** Only the schedule form and the ≤1 cap are locked. Per-stage values are
    calibration-open; preflight asserts only the cap and the form; C-05 is a
    legitimate configuration choice (though still one worth recording).
  - **(C)** Locked with an explicit waiver mechanism — values are binding, but a
    run may deviate if the deviation is recorded and owner-approved in the run
    record, which preflight then verifies.

- **Confidence of impact:** HIGH — determines whether C-05 is a defect, what the
  planned preflight conformance gate may enforce, and how future spec tables
  declare lock granularity.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** Owner instruction 2026-07-24 (interactive session,
  AskUserQuestion): **Option A — the per-stage `λ^max(k)` values are locked.**
  The full PHYS-05 table binds, not merely the warmup form plus the `≤1` cap; the
  `10^(k−4)` ramp is a designed decision about how conservation pressure enters the
  curriculum, not a placeholder default. Consequences, all owner-authorized by this
  ruling:
  1. Overriding **any** per-stage value is a conformance violation, not a
     configuration choice. This makes conformance audit finding **C-05** a defect
     (see GAP-45-02, resolved consistently).
  2. The planned preflight conformance gate (verification charter layer 1) asserts
     the **entire** per-stage table at run start and at every stage boundary — not
     just the `≤1` ceiling.
  3. `tests/phase40/test_scheduled_weights.py` is under-specified as written: it
     asserts the cap fails closed at 1.5 but never asserts the locked Stage-0 value
     of 0. Adding per-stage table assertions is part of the conformance fix.
  4. The "default" wording on the adjacent `λ_phys^max(k) = 1` line in
     `pinn_architecture.md` §4.1 is now known to be misleading relative to this
     ruling. Correcting that wording is a **spec edit** and therefore out of scope
     here (SCOPE-24, and v2.1 edits no spec); it is routed to a spec-editing
     milestone. Recorded so the ambiguity is not re-litigated.
  5. Generalization beyond PHYS-05 was **not** decided: this ruling settles the
     PHYS-05 table's lock granularity. Whether framework-spec tables carry locked
     per-row values *by default* remains unstated, and a spec convention for
     marking locked-vs-default within a table is still absent. Flagged for the
     spec-editing milestone rather than assumed.

---

## GAP-45-04 — What numeric bound clips the causal exponent?

- **Decision point:** Both specs mandate clipping the causal exponent and defer
  the numeric bound: "Clip the causal exponent to avoid underflow, but do not
  choose a numeric clipping bound in Phase 19; **surface a gap if one is needed**"
  (`pinn_architecture.md` §4.1) and "The exponent must be clipped to avoid
  underflow, but no numeric clipping bound is selected in Phase 35; the bound
  remains deferred to FUT" (`ctl_instruction.md:1773`). The implementation applies
  no clip, and the pilot demonstrated total underflow — the spec's own
  gap-surfacing condition was met and never acted on. A bound is now needed.

- **Where in artifact:**
  `pinn_architecture.md:648-650` and `:414` (the mandate and the weight formula);
  `ctl_instruction.md:1773`; `pinn/loss_catalog.py:228-229, 258` (unclipped
  `torch.exp`); `runs/stage0-*/logs/train.log.jsonl` (`front_idx`, `w_min`,
  `w_mean`, `w_max`); conformance audit findings **C-01/C-02**; trainex-r2 report
  gap RG-11.

- **Task context:** The conformance audit established that `front_idx = 0` across
  1500 of 1500 logged steps in 5 of 5 runs, with `w_mean = 0.0625 = 1/16` exactly,
  `w_max = 1.0`, `w_min = 0.0` — arithmetically consistent only with `w₁ = 1` and
  `w₂…w₁₆` underflowed to exactly zero, given `collocation_count=16`.

- **Classification:** semantic — a numeric contract in a locked spec, explicitly
  deferred to a gap by the spec itself.

- **Source silence:** the two spec passages above *name* the deferral and instruct
  that a gap be surfaced if a bound is needed. No source proposes a value, a
  selection method, or an acceptance criterion for one. `pinn/constants.py` — the
  home for every spec-cited numeric constant — has no entry, correctly, because
  none was ever specified.

- **Mathematical / engineering grounding:** The causal weight is
  `w_n = exp(−η_c Σ_{m<n} stopgrad(R̄_m))` with `η_c = 1`. In float32 the
  exponential underflows to exactly 0.0 once the argument falls below about −103
  (`log(2^-149) ≈ −103.3` at the subnormal limit; below roughly −87 the result is
  subnormal and loses precision). With early-training residuals of order 1 or
  larger and 16 collocation points, the cumulative sum for later points reaches
  that threshold immediately, which is precisely what the logs show. Once a weight
  is exactly zero it contributes no gradient, so physics supervision at that
  collocation time vanishes entirely rather than merely being down-weighted — the
  mechanism's intended behavior (a soft time-ordered curriculum) degrades into a
  hard one-point mask. Clipping the exponent at some floor `−C` bounds the smallest
  weight at `e^(−C)`, preserving a non-zero gradient path at every collocation
  time. The trade-off in choosing `C` is direct: too small (aggressive clip) and
  the causal ordering is weakened toward uniform weighting, defeating the
  mechanism's purpose; too large and underflow returns. The choice interacts with
  `η_c`, with the residual scale (hence with GAP-45-01's normalization and the R̄
  factor finding C-03, since a corrected R̄ is 3× larger and reaches the underflow
  threshold sooner), and with `N_t`. Because the value trades off two failure modes
  the spec deliberately declined to arbitrate, and because it is a locked-spec
  numeric contract, it is not the agent's call.

- **Agent was tempted to:** propose a conventional floor such as clamping the
  exponent to `≥ −30` (smallest weight ~9e-14, safely above float32 underflow while
  still expressing four decades of causal ordering), or equivalently clamping the
  weights themselves to a small positive floor. The reasoning is sound as an
  engineering starting point, but it selects a numeric value inside a locked spec
  contract that the spec explicitly reserved.

- **What the user needs to decide:** the bound, or the process for setting it —
  - **(A)** Owner selects a value now (e.g. an exponent floor `−C`, or a weight
    floor `w_min`), recorded as a spec amendment in a spec-editing milestone.
  - **(B)** Owner authorizes a provisional implementation value for the next
    milestone's conformance fix, explicitly marked provisional and revisited after
    a conformant run produces evidence on how fast the front advances.
  - **(C)** Defer the value but mandate the *invariant* now — e.g. "no causal
    weight may be exactly zero" and "the front must advance within N steps" —
    letting the implementation pick any bound that satisfies it, with a runtime
    guard asserting the invariant (this is layer 2 of the verification charter).

- **Confidence of impact:** HIGH — this is the mechanism behind the most severe
  confirmed divergence, and no re-run of Stage 0 is meaningful until it is fixed.
  Note also that C-01 cannot be closed as a routine code fix, precisely because it
  needs this decision.

- **Status:** RESOLVED-WITH-INSTRUCTION

- **Resolution note:** Owner instruction 2026-07-24 (interactive session,
  AskUserQuestion): **Option C — mandate the invariant, defer the numeric bound.**
  The contract is the *behavior*, not a value:
  1. **Locked invariant A (fully specified, self-executing):** no causal weight
     `w_n` may be exactly zero. This is checkable without any further decision and
     is sufficient to close conformance finding **C-01** — the implementation may
     select any clip that satisfies it.
  2. **Locked invariant B (threshold still owner-owned):** the causal front must
     advance within N steps. **N is deliberately not set here.** It is already
     tracked as an owner-owned runtime-invariant threshold in the verification
     charter §6, alongside the dominance ratio and persistence window. Invariant B
     is therefore *stated* but not yet *enforceable*; invariant A alone unblocks
     the C-01 fix, so this does not gate the conformance work.
  3. **The implementer chooses the bound, and must record it.** The chosen clip
     (exponent floor, weight floor, or equivalent) is an authorized implementation
     decision — not a spec value and not a silent default. It is recorded in the
     conformance-fix plan and in the run record, and marked revisitable once a
     conformant run shows how fast the front actually advances.
  4. **No spec amendment is made.** The specs' deferral of the numeric bound to FUT
     stands; this ruling supplies the invariant the specs left implicit
     ("clip to avoid underflow") in a form an implementation can be held to.
  5. **Interaction flagged, not resolved:** fixing C-03 (R̄ from (1/9) to the locked
     (1/3)) makes R̄ three times larger, so the un-clipped exponent would underflow
     *sooner*. Whatever clip satisfies invariant A must be chosen against the
     corrected R̄, not the current one — otherwise the fix to C-03 reintroduces the
     collapse. This is an ordering constraint on the conformance-fix phase.
  6. The spec's own "surface a gap if one is needed" condition (`pinn_architecture.md`
     §4.1) is hereby satisfied — belatedly. The gap was surfaced, and answered.
