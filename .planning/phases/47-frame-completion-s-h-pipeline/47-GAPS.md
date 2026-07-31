# Phase 47 Gap Register — Frame Completion & `S_H` Pipeline

Phase-local STOP-protocol gap register for Phase 47 (milestone v2.2). Each entry
is a source-silent decision that this phase **surfaced** rather than decided, per
the CLAUDE.md / AGENTS.md STOP protocol. The milestone-wide index is
`.planning/milestones/v2.2-GAPS.md`.

This register is written by the Phase 47 orchestrator (parent session), not by a
subagent — per governance, the parent owns gap-register writes. The plan 47-01
executor surfaced the finding and correctly declined to resolve it.

## GAP-47-01 — The D-08 derived tolerance is exceeded on the validation-side reading for 9 of 50 sampled real trajectories, because its derivation omits the finite-difference cancellation term. Is the derivation completed, the claim narrowed, or the record accepted as-is?

- **Decision point:** Plan 47-01's Task-3 D-23 measurement compares gate metrics
  before and after the CONF-09 residency swap against the per-trajectory bound
  that the committed helper `frame_drift_tolerance` derives from inputs only. On
  the **loss-side** reading the measurement is inside the bound for 50/50 sampled
  trajectories (max ratio 0.6693). On the **validation-side** reading it is
  inside the bound for only **41/50** — 9 trajectories exceed it, max ratio
  **4.7611**. The underlying physics claim is nevertheless confirmed: the two
  arms' `eps_H` agree to ~13 significant digits (medians identical to all seven
  printed digits at `1.470877e-01`; absolute differences `1e-17 … 1e-14` on
  values of order `1e-1`). What falls short is the **certificate**, not the
  invariance. The decision is what to do about a pinned derivation now known to
  be incomplete, when the incompleteness was noticed only after the numbers were
  observed.

- **Where in artifact:**
  `.planning/phases/47-frame-completion-s-h-pipeline/evidence/frame-re-ratification/20260731T012304Z/re-ratification.md`
  §4.2 (the D-23 comparison table and the FINDING block beneath it); the
  derivation itself is `tests/phase47/test_conf09_frame_completion.py`
  `frame_drift_tolerance`, Step 4.

- **Task context:** Plan 47-01 Task 3 (the one-shot D-22 re-probe plus the D-23
  before/after comparison record), executed during Wave 1 of
  `/gsd-execute-phase 47`. Tasks 1 and 2 completed and committed cleanly
  (`2c84d161`, `1c68368d`); the finding arises only in Task 3's measurement
  against real Brutus sampling.

- **Classification:** **semantic** (a physics/numerics tolerance derivation), with
  a **process-artifact** component (whether extending a plan-pinned derivation
  after observing data is permissible under SCOPE-29 / D-26).

- **Source silence:**
  - `47-01-PLAN.md` Task 2 pins the four-step derivation and states the operation
    counts `4` (the `D` identity) and `8` (the `H` assembly) are "operation
    counts … not to be raised". It specifies fail-loud behaviour **only** for the
    `delta_total < |H_old(0)|` precondition — it is silent on what to do when the
    bound is satisfied as a formula but violated by real data.
  - `47-CONTEXT.md` D-08 asserts approximate invariance under the swap and
    requires a derived (not hand-chosen) bound, but does not quantify the
    float64 error budget or enumerate its error sources.
  - `47-CONTEXT.md` D-26 and `.planning/REQUIREMENTS.md` SCOPE-29 forbid an
    observed number steering the tolerance. They prohibit *fitting*; they do not
    say whether *completing an omitted first-principles term* counts as fitting.
    This is precisely the ambiguity that makes the decision non-mechanical.
  - `47-VALIDATION.md` sets the wave gate as `pytest tests/phase46/ tests/phase47/`
    green with zero skips — which is satisfied (155 passed, 0 skipped), because
    the unit fixture does not exercise the failing regime.

- **Mathematical / engineering grounding:**
  `preprocess_trajectory` applies an orthogonal rotation `R0` (preserving pairwise
  distances and speeds exactly), then scales `r' = r/D` and `v' = v/V` with
  `V = D/T`. With `G = 1`, `T = 10`, `D = cbrt(G·T²)`, the PIPE-09 identity gives
  `D³ = T²`, hence `T²/D² = D`. Therefore `K_new = D·K_old` exactly, and
  `V_new_at_eps = −Σ mᵢmⱼ/sqrt((sᵢⱼ/D)² + eps²) = D·V_old_at_(D·eps)`, so
  `H_new(t) = D·(K_old(t) + V_old_at_(D·eps)(t))` exactly. The uniform factor `D`
  cancels identically in the relative drift `eps_H = maxₜ|(H(t) − H(0))/H(0)|`.
  The two arms can therefore differ **only** through the softening floor: the same
  numeric `eps` acts as an effective `D·eps ≈ 4.64·eps` in old-frame units. That
  is the entire content of D-08, and the derivation bounds it correctly.

  What Step 4 omits is a *floating-point* error source specific to one reading.
  The validation-side reading does not consume stored velocities; it reconstructs
  them as a central divided difference of positions,
  `v[k] ≈ (pos[k+1] − pos[k−1]) / (t[k+1] − t[k−1])`
  (`gate_metrics.py:84-123`). In exact arithmetic that operator is linear in
  positions and scales exactly as the stored velocities do — which is what Step 1
  correctly argues. In floating point the numerator is a **cancelling
  subtraction** of two `O(1)` operands whose difference is `O(Δr)`, so the
  relative error of the reconstructed velocity is amplified by the condition
  number `|r|/|Δr|`. On real Brutus sampling (`dt_out ≈ 0.01 … 0.08` over
  `t ∈ [0, 10]`) that factor is roughly `10² … 10³` unit round-offs — a term the
  bound does not contain. Three independent facts corroborate this diagnosis
  rather than a physics defect:
  1. the loss-side reading consumes **stored** velocities, incurs no cancellation,
     and stays inside its bound on 50/50 trajectories;
  2. the tiny-corpus unit fixture samples 12–24 snapshots over the same horizon,
     so `h ≈ 0.9` produces almost no cancellation and
     `test_gate_metric_near_invariance` passes on its own fixtures — i.e. the unit
     test is not wrong, it simply never enters the failing regime;
  3. the exceedances are `O(1e-14)` absolute against a bound of `O(1e-15)` on a
     metric of magnitude `1e-1`, i.e. both sides are at the noise floor of
     float64 — the ratio is large only because the bound is very small.

  Consequence of getting this wrong in each direction: if the bound is extended
  when it should not be, Phase 47 sets a precedent that a pinned derivation may be
  widened after seeing data, which is the exact failure mode SCOPE-29 exists to
  prevent. If the claim is narrowed when the bound was merely incomplete, CONF-09
  ships a weaker certificate than the physics supports, and Phase 50/51's
  validation-side gate inherits an unquantified error budget.

- **Agent was tempted to:** add the missing finite-difference cancellation term
  (`≈ |r|/|Δr| · unit round-off`, derivable from the trajectory's own `u` spacings
  and geometry without reference to any observed metric) to `delta_round` in
  Step 4, which would have brought all 50/50 validation-side trajectories inside
  the bound. Rationale: the term is derived from inputs, not fitted to output, so
  it is arguably admissible under SCOPE-29. **Not done** — the *decision to add a
  term at all* was prompted by observing the exceedance, and the plan pins the
  derivation explicitly. Nothing was widened, no operation count was raised, and
  no test was relaxed.

- **What the user needs to decide:**
  - **(A) Extend the derivation.** Add a finite-difference cancellation term to
    Step 4, derived from inputs only (per-node `h` spacings and trajectory
    geometry), and re-record the D-23 comparison against the corrected bound.
    Strongest certificate; requires ruling that completing an omitted
    first-principles term is not "steering by observation" under SCOPE-29/D-26.
  - **(B) Narrow the D-08 claim to the loss-side reading.** Certify near-invariance
    for the reading that CONF-02/CONF-03 actually consume, and record the
    validation-side agreement descriptively (~13 significant digits) without a
    bound claim. Touches no pinned derivation; leaves the validation-side gate's
    error budget unquantified for Phase 50/51.
  - **(C) Accept the record as-is.** Retain the 41/50 result with its written
    diagnosis. Cheapest; leaves a known-incomplete certificate in committed
    evidence.

- **Confidence of impact:** **MEDIUM.** The physics conclusion CONF-09 depends on
  is confirmed independently of this decision, and the reading that Waves 2–3
  consume is inside its bound — so the choice does not change any code Phase 47
  ships. It is HIGH for the integrity of the evidence record and for the
  precedent it sets on amending pinned derivations, and it gates Phase 47's
  close-out sign-off on CONF-09.

- **Dependency-scoped blocking (orchestrator assessment — for owner confirmation,
  not a ruling):** Wave 1's committed work is unaffected under all three options;
  none of A/B/C changes `pinn/data/adapter.py` or
  `pinn/training/validation_gate.py`. Waves 2 (CONF-02 `S_H`) and 3 (CONF-03
  `ε_H = 1e-4·S_H` wiring) build on the **loss-side** reading
  (`_matched_plummer_hamiltonian` at `EPS_SOFT = 1e-5`), which is inside its
  derived bound on 50/50 trajectories; the disputed certificate belongs to the
  **validation-side** gate reading (`EPS_INV = 1e-10`). On that basis Waves 2–3
  appear safe to proceed while this gap is open. **Phase 47 must not close** with
  it unresolved.

- **Status:** `OPEN` — owner ruled option A on 2026-07-30 and it was applied in
  full (`562084e8`); the ruling **narrowed but did not close** the shortfall, and a
  second, distinct omitted source has since been identified. A follow-on decision
  is required. See "Resolution progress" below.

- **Resolution note (progress, 2026-07-30):** Owner ruled **option A** — extend the
  derivation with an inputs-only finite-difference cancellation term. Implemented
  as ratified in `562084e8`: `frame_drift_tolerance` gained keyword-only
  `times`/`fd_velocities`, a new Step 5 adds
  `delta_fd = max_k Σᵢ mᵢ·‖vᵢ[k]‖·δvᵢ[k]` with
  `δvᵢ[k] = 2u·R_max/Δt_k + 2u·‖vᵢ[k]‖` and `Δt_k` read per interior node from the
  actual times, and `delta_total = delta_max + delta_round + delta_fd`. Steps 1–3
  unchanged; Step 4's operation counts `4` and `8` unchanged; no test relaxed.
  `delta_fd` is exactly zero for the loss-side reading, whose 50 rows are
  byte-identical before and after — the mechanical proof the term is
  reading-specific.

  **Result: validation-side 41/50 → 45/50 within bound; max ratio 4.7611 → 1.7044.
  Loss-side unchanged at 50/50 (max 0.6693).** Five trajectories (ids 0661, 1089,
  1611, 1888, 3703) still exceed. Two residual sources, both identified from the
  derivation rather than from the numbers, neither implemented:

  1. **Node coverage inside Step 5 itself.** Step 5 maxes over *interior* nodes,
     but `eps_H` is evaluated at every node, and `finite_difference_velocity` fills
     both endpoints with *one-sided* differences over `t[1]−t[0]`
     (`gate_metrics.py:117-118`) — about half the interior span on this corpus
     (0.08 vs 0.16), so endpoint error is roughly 2× the interior max. Node 0
     matters structurally, not just numerically: Step 3's `e = delta(0)` is the
     perturbation at node 0, an endpoint the interior max never sees. This reads
     as an incompleteness in Step 5's own wording rather than a new effect.
  2. **A genuinely second omitted source.** Step 5 prices the numerator at
     `2u·R_max` — two operands × one representation round-off — which is right for
     the OLD arm, whose positions *are* the stored array. The NEW arm's positions
     are computed: `r' = fl((R0 @ r_bar)/D)` (`preprocessing.py:200,204`), a
     three-term `einsum` (~3u) plus a divide (~1u), so ~`4u·|r|` per component,
     amplified by the same `1/Δt` factor and present on the new arm only, so it
     does not cancel between arms.

  Measured for scale only, explicitly **not** applied: endpoint coverage alone
  leaves 1/50 outside (id 0661 at 1.0402); endpoints plus the analytic
  `2 operands × 4u = 8u` leaves 0/50 outside (worst 0.3887). Both are a-priori
  operation counts in Step 4's style rather than fits, but adopting either extends
  the derivation beyond what the owner ratified, so neither was taken.

  **Orchestrator note on method risk.** This is now the second round in which the
  derivation proved incomplete. Each added term is individually a-priori, but an
  open-ended sequence of "add another term until the data fits" converges on the
  behaviour SCOPE-29 exists to prevent, even when no single step is a fit. The
  underlying difficulty is real: the bound is `O(1e-15)` on a metric of `O(1e-1)`,
  so it is certifying agreement at the float64 noise floor, where an exhaustive
  term-by-term operation count over a rotate → scale → difference → assemble →
  ratio pipeline is a brittle instrument. A single conservative whole-pipeline
  round-off model with one stated operation-count budget may be the terminating
  form. Recorded as an observation for the owner, not a proposal adopted.

## Not recorded as gaps

- **Three Rule-3 deviations in plan 47-01**, all documented in `47-01-SUMMARY.md`
  and resolved within the plan's own latitude: (i) the plan's `rtol=1e-10` for the
  independent body-order oracle cannot hold against an **fp32** resident, so the
  bound is derived from `finfo(float32).eps` using the `32.0` allowance already
  present in that file; (ii) the tiny-corpus fixture is collinear at `t = 0`, so
  the inline oracle implements all three §2.4 gauge branches; (iii)
  `--evidence-root` was required because the probe defaults to Phase 46's evidence
  tree, and writing there would contaminate retained Phase 46 evidence and breach
  this plan's one-directory cap. None of these is source-silent: each has a
  determinate answer from the plan's own constraints.
- **The REQUIREMENTS.md CONF-09 checkbox was deliberately not flipped** by the
  executor. That is a phase-close/verification act, not a plan-execution act, and
  plan 47-01 does not mutate the locked governance docs it was planned against.
