---
phase: 57
milestone: v2.3
created: 2026-09-07
---

# Phase 57 Gap Register — Corrected Re-Run & the Preserved Evaluation

Phase-local record of owner-routed decisions and source-silent gaps surfaced
during Phase 57 work. The milestone-wide index is
`.planning/milestones/v2.3-GAPS.md`. Surfaced under the CLAUDE.md STOP protocol
(v2.3 adjudication milestone; the build-track analog per `.planning/ROADMAP.md`
"Gap discipline"). The autonomous best-judgment directive (2026-09-07) does
**not** waive the semantic / cross-phase-reframing MUST-surface class.

GAP-57-01 was surfaced during the Phase 57 **discuss** step, before any plan or
run, so it is visible to the researcher and planner rather than hit by an
executor. Its initial blocking was **dependency-scoped**: the checkpoint-③ and
checkpoint-④ owner packets, the EVAL-02 evaluator-pairing characterization
(GAP-46-01), and the evidence-contract design could proceed. The owner resolved
the implementation responsibility on 2026-09-07; RUN-04 still waits on the
separate verification and owner gates recorded in the resolution note.

---

## Inherited items resolved for Phase 57 (not new gaps — carried forward)

- **GAP-54-06** (`.planning/phases/54-recalibration-decision-grounding/54-GAPS.md`;
  `.planning/milestones/v2.3-GAPS.md`) — `RESOLVED-WITH-INSTRUCTION
  (2026-09-08)`. The owner fixed the L-BFGS behavior at checkpoint ③: freeze
  the segment's collocation samples and detached causal weights for the entire
  L-BFGS segment, including every line-search closure and outer call. Use one
  separate frozen training-only monitor for invariant B and explicitly
  re-ratify `N = 500`. Exact record: `57-RULING.md`.

- **GAP-56-01** (`.planning/phases/56-contract-amendment-train-free-gate/56-GAPS.md`;
  `.planning/milestones/v2.3-GAPS.md`) — `RESOLVED-WITH-INSTRUCTION
  (2026-09-08)`. The owner requires a `2:1` non-anchor spread and one uniform
  residual reduction with `alpha = log(2)/(2 * P_15)`, followed by
  `front_idx = 15` and every perturbed weight `>= 0.70`. Exact record:
  `57-RULING.md`. The current `PASS INCOMPLETE` remains historical; production
  implementation and a new complete GATE-04 PASS still block RUN-04.

---

## GAP-57-01 — the amended (SPEC-01/SPEC-06) recipe has no implementation home, and no source authorizes a `pinn/` code change to give it one

- **Decision point.** RUN-04 requires "Stage-0 runs end-to-end under the
  SPEC-01/SPEC-06-corrected recipe." The corrected recipe exists in
  `pinn_architecture.md` §3.2 (amended by Phase 56) but **not** in `pinn/` code:
  `pinn/train.py:1033` still hard-codes `collocation_count = 16`;
  `pinn/loss_catalog.py::causal_physics_loss` still forms a raw per-point
  16-term exclusive prefix over unnormalized `R̄`; there is no `R_ref`
  normalization of the causal exponent or of the outer training physics loss;
  there is no 16-bin bin-mean structure. The ratified v2.3 roadmap proposal put
  implementation in its Phase D scope; the roadmap as ratified and Phase 56 as
  executed did not. Who implements the amended recipe in code, whether Phase 57
  is authorized to, and how large a `pinn/` change is in-grant, is fixed by no
  source.

- **Where in artifact.** `57-CONTEXT.md` Section 1 (D-01, D-02) and "Open
  Decisions surfaced to the owner". Will surface again in `57-RESEARCH.md` /
  `57-PLAN.md` when the RUN-04 launch path is specified. Requirement text:
  `.planning/REQUIREMENTS.md:104` (RUN-04). Proposal text:
  `docs/work/designs/cross_cutting/v2.3-milestone-proposal/2026-08-17-v2.3-roadmap-proposal.md:267`
  ("Phase D | SPEC-01 + SPEC-06 amendment **and implementation**; GATE-04").

- **Task context.** Discuss-phase servicing of Phase 57's gray areas —
  specifically deciding how RUN-04 obtains an executable form of the amended
  recipe, so the planner can hand the executor a launch path.

- **Classification.** Cross-phase reframing (it changes what Phase 57 builds
  and whether a `pinn/` implementation phase is needed) **with a semantic
  component** (the change restructures the causal loss and the outer physics
  loss — loss math the STOP protocol's semantic class covers) **and a scope
  component** (SCOPE-33 authorizes framework-spec edits only; a `pinn/` code
  change is not obviously in any v2.3 grant).

- **Source silence.**
  - `.planning/REQUIREMENTS.md:104` (RUN-04) — "Re-run Stage-0 under the
    SPEC-01/SPEC-06-corrected recipe … [SCOPE-36 authorizes Stage-0 training]".
    Says nothing about who makes the recipe executable or authorizes the code
    change.
  - `.planning/REQUIREMENTS.md` SCOPE-33 — "**Framework-spec edits ARE
    authorized**, narrowly: only … VER-20 items (a)–(e), plus the `n_col`/`N_t`
    disposition … No open-ended spec rewriting." Framework-spec edits only; no
    mention of `pinn/` production code.
  - `.planning/REQUIREMENTS.md` SCOPE-37 — "**Iteration after the spec edit
    lands is conformance-only again.** Once the new … values are locked, no
    further tuning against observed re-run results …" This **presumes** the code
    already implements the ratified recipe (it governs *tuning*, not initial
    implementation); it neither authorizes nor forbids the implementing change.
  - `.planning/PROJECT.md:344` — FUT-01 is **already shipped in v2.0**: the
    production `pinn/` package was rebuilt from the framework specs. This
    corrects the Phase-56 shorthand that points the new §3.2 divergence to a
    future FUT-01 rebuild, but it still does not assign the post-v2.0 amended
    recipe implementation to a v2.3 phase.
  - `.planning/REQUIREMENTS.md` "Future Requirements" — defers PLAT-01..07 and
    Stage-1+ work, not FUT-01. It neither authorizes a new wholesale trainer
    rebuild nor assigns the bounded §3.2 conformance patch.
  - `.planning/ROADMAP.md:59` (Phase 56 line) — maps Phase 56 to "SPEC-01,
    SPEC-06, GATE-04"; the word "implementation" from the proposal's Phase D is
    absent.
  - `.planning/ROADMAP.md:60` (Phase 57 line) — "Stage-0 re-runs end-to-end
    under the SPEC-01/SPEC-06-corrected recipe …"; does not say the recipe is
    implemented as part of Phase 57 or by whom.
  - `docs/work/designs/cross_cutting/v2.3-milestone-proposal/2026-08-17-v2.3-roadmap-proposal.md:267`
    — "Phase D | SPEC-01 + SPEC-06 amendment **and implementation**; GATE-04".
    The proposal *did* scope implementation into Phase D, but the roadmapper's
    one-to-one mapping (`ROADMAP.md:223` "no merges, splits, or reordering")
    dropped "and implementation" without recording where it went.
  - `.planning/phases/56-contract-amendment-train-free-gate/56-CONTEXT.md` D-03,
    `56-VERIFICATION.md` truth 3 — Phase 56 **actively declined** the
    implementation: "Do not edit `pinn/train.py` (SCOPE-33; live code is not a
    v2.3 grounding source or edit target)"; "the trainer rebuild is FUT-01";
    "`pinn/train.py` confirmed unedited. `git status --porcelain -- pinn/` =
    empty." The FUT-01 pointer conflicts with `.planning/PROJECT.md:344`'s
    shipped-v2.0 record, and these Phase-56 artifacts do not say which phase or
    requirement picks the new amendment's implementation back up.
  - `.planning/phases/54-recalibration-decision-grounding/54-RULING.md` — ratifies
    the recipe's *content*; is silent on code implementation (it explicitly
    scopes itself to framework-spec re-ratification and defers even the
    optimizer contract to GAP-54-06).

- **Mathematical / engineering grounding.** The ratified causal weight is
  `w_1 = 1`, `w_n = exp(−η_c · Σ_{m<n} stopgrad(R̃_m))` with `η_c = 1`,
  `R̃_b = R̄_b / R_ref`, a **batch-global exclusive prefix over M = 16 fixed
  equal-`u` bin means** (`[b/16,(b+1)/16)` for `b = 0…14`, `[15/16,1]` for
  `b = 15`), with `n_col = 4096` total physics rows per training batch stratified
  256 per bin, and `R_ref` frozen (the finite positive median of the 96 raw bin
  means from the fixed six-case GATE-04 initialization probe). `54-RULING.md`
  `B2` (residual-wide) additionally applies `R̃_b = R̄_b / R_ref` to the **outer
  training physics loss**, not only the causal exponent.
  The shipped trainer instead: forms the prefix over **16 collocation points**
  (`collocation_count = 16`), over **unnormalized** raw per-point `R̄`, with no
  bin structure and no `R_ref`. Bringing the code to the ratified recipe is
  therefore a restructure of `causal_physics_loss` (bin aggregation + frozen
  normalization + the residual-wide application to `L_phys`) and of the
  collocation sampler (`n_col` 16 → 4096, stratified 256-per-bin draw, the
  240-slot replay-only construction, microbatch bin-aggregate preservation) —
  touching `pinn/train.py` and `pinn/loss_catalog.py` at multiple call sites.
  **Why the choice is consequential:**
  - **RUN-04's risk profile.** A 256× increase in collocation rows per batch
    multiplies the per-step forward/backward cost of the physics term and
    changes the wall-clock the duration gate calibrates against; the frozen
    `R_ref` normalization is precisely the mechanism `54-RULING.md` says makes
    the weights "sensitive to genuine residual descent" — a wrong implementation
    of it either re-saturates the front (GATE-04 should catch this) or divides
    real descent back out (GATE-04's condition (ii), currently unratified, is
    the guard). The size and correctness of the code change directly govern
    whether RUN-04's result is interpretable evidence about the design.
  - **Whether SCOPE-37 even applies.** SCOPE-37's "conformance-only iteration"
    clause presumes the code implements the ratified recipe. If no phase is
    authorized to make that implementation, the clause has no referent and the
    milestone cannot reach RUN-04.
  - **Milestone traceability (VER-21).** Options B and C change the phase count
    and the requirement→phase mapping VER-21 re-verifies at close; option A
    keeps the mapping but expands Phase 57's `pinn/`-edit surface beyond
    anything v2.3 has done, risking a "conformance patch" becoming an unscoped
    wholesale rebuild under a name that hides it.
  - **The v2.2 precedent cuts both ways.** v2.2 Phases 46–49 *were* exactly
    code-to-spec conformance work on `pinn/` (nine C-01..C-09 divergences
    repaired) — precedent for option A. But v2.2 did that under a milestone
    whose requirements *named* the conformance work (CONF-01..09); v2.3's
    requirements do not name a RUN-04 implementation task.

- **Agent was tempted to.** Read option A into RUN-04 by implication ("re-run
  under the corrected recipe" presupposes the recipe is implemented) and scope a
  bounded conformance patch to `causal_physics_loss` + the collocation sampler
  as Phase 57's first wave, citing the v2.2 Phases 46–49 precedent and SCOPE-37's
  "conformance" language. **Not recorded as a decision** — the proposal-vs-roadmap
  discrepancy, the SCOPE-33 spec-edits-only boundary, and the magnitude of the
  change (loss-math restructure, 256× compute, `R_ref` plumbing, residual-wide
  `L_phys` normalization) put this squarely in the class `.planning/ROADMAP.md`
  "Gap discipline" says is "MUST-surface by construction" and the class v2.2
  Phase 50's CONTEXT required be surfaced ("change nothing that enters a loss
  term, an optimizer, the data path, or a gate").

- **What the user needs to decide.** How RUN-04 obtains an executable form of
  the amended §3.2 recipe:
  - **A — Phase 57 makes a bounded `pinn/` conformance patch** to the
    causal-loss (`pinn/loss_catalog.py`) and collocation-sampler
    (`pinn/train.py`) path, and the residual-wide `L_phys` normalization,
    honouring `pinn_architecture.md` §3.2 exactly, as an explicit first wave —
    read as code-to-spec conformance (v2.2 Phases 46–49 precedent; SCOPE-37
    "conformance" language). The owner fixes the boundary: what may change and
    what may not.
  - **B — Insert a dedicated implementation phase** (e.g. Phase 56.5 or 57) for
    the amended-recipe code, before RUN-04, with its own requirement, plan, and
    verification; RUN-04/05/EVAL-02 shift to a later phase number. Updates the
    requirement→phase mapping (VER-21).
  - **C — Commission a new wholesale trainer rebuild in v2.3** as an explicit
    requirement. The originally surfaced "pull FUT-01" description was
    factually incorrect: `.planning/PROJECT.md:344` records FUT-01 as shipped in
    v2.0. A new rebuild would therefore require its own concrete justification.
  - **D — The milestone blocks** pending a separate owner scope decision (e.g.
    an ERW round on the implementation approach, or a new milestone).

- **Confidence of impact.** HIGH — RUN-04, RUN-05, and EVAL-02 are all gated on
  the amended recipe running; the decision sets whether v2.3 can reach its
  terminal state at all, and the authorized code-change size is RUN-04's primary
  risk lever.

- **Status.** RESOLVED-WITH-INSTRUCTION (2026-09-07).

- **Resolution note.** Owner selected **Option A** on 2026-09-07: Phase 57 owns
  a bounded code-to-spec conformance patch as an explicit first implementation
  wave, followed by a **separate verification step that must pass before
  RUN-04**. This instruction repairs the proposal-to-roadmap omission and
  expressly supersedes the earlier Phase-56 / `pinn_architecture.md:458`
  implementation deferral and "no production Python file" statement **only for
  this bounded amended-recipe path**.

  The patch inventory is defined by the ratified behavior, not by the two
  example files named in Option A. It includes every necessary production-path
  change in the causal loss, collocation allocation/sampler, controller, and
  configuration wiring—including replacing the current one-anchor physics-loss
  execution with contributions from all selected slots—plus focused tests and
  verification evidence. The implementation must reproduce §3.2 exactly:
  `4096` physics rows per batch; `16` fixed equal-`u` bins with `256` rows each;
  one batch-global exclusive prefix over the bin means; the detached, frozen
  `R_ref` applied to both the exponent and residual-wide outer `L_phys`; the
  ratified full-batch and replay-only allocation; energy-set reuse;
  microbatch-preserved bin aggregates; valid gradient behavior; and raw plus
  normalized diagnostics. Verification must exercise the actual production
  training path and demonstrate the allocation, normalization, gradients, and
  diagnostics before RUN-04 is eligible.

  This is **not** authorization for retuning, architecture redesign, a data-policy
  change, Stage-1+, PLAT-01..07, or a new wholesale trainer rebuild. Any required
  expansion stops for a new owner decision. A resource failure at the exact
  ratified `4096`-row batch is fail-closed evidence; it never permits silently
  reducing the sample count. FUT-01 itself shipped in v2.0
  (`.planning/PROJECT.md:344`), correcting the gap's original option-C
  characterization.

  This resolution authorizes implementation only. The owner subsequently
  resolved GAP-56-01, checkpoint ③/GAP-54-06, and checkpoint ④ on 2026-09-08;
  `57-RULING.md` is the exact governing record. RUN-04 remains blocked until
  the bounded production wiring, separate verification, and a new complete
  GATE-04 PASS are finished.

---

## GAP-57-02 — the ratified 4096-row recipe exceeds this machine's memory and throughput, and no source authorizes any of the available remedies

- **Decision point.** Band generation 1 halted on the Tier-2 `memory_watermark`
  guard at stage 0 / step 0 / phase `2a`, before any optimizer update. The
  ratified 4096-row batch cannot be executed to completion on the current
  machine under the current guard configuration and instrumentation contract.
  Four mutually non-exclusive remedies exist (recalibrate the guard, reduce the
  in-step transient peak, change the execution environment, or accept the
  observed schedule). No source selects among them, and every one of them
  changes either an owner-carved threshold, a declared telemetry contract, the
  execution environment, or the phase's cost basis.

- **Where in artifact.**
  `.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/blocked-state.json`
  (`failure.guard = memory_watermark`, `failure.value = 0.968756357828776`);
  `runs/stage0-v23-smoke/failure/trip.json`; ledger record
  `evidence/run-ledger.md` `band_generations[0].status = "blocked"`.

- **Task context.** Post-Wave-6 preparation for a band generation 2 run window.
  Wave 5 attempted the smoke and blocked; Wave 6 correctly refused to run,
  because plan `57-06` Task 1 forbids candidate selection on an operational
  block. Preparing re-admission requires knowing which remedy is authorized.

- **Classification.** **Semantic** for the guard threshold and the
  transient-peak remedy (both change values or contracts the sources reserve to
  the owner); **operational coordination** for the environment choice. Not
  mechanical under any reading.

- **Source silence.**
  - `pinn/training/config.py:291-297` — `memory_watermark_fraction` is
    `_PROVISIONAL_MEMORY_WATERMARK_FRACTION = 0.7`, with the in-code comment
    stating that `disk_floor_fraction / memory_watermark_fraction` "remain
    owner-carved and uncalibrated". The value is a placeholder, never
    calibrated; the run-start log line repeats this as
    "owner-calibrate-at-Phase-43-pilot".
  - `57-GAPS.md` GAP-57-01 resolution note — "A resource failure at the exact
    ratified `4096`-row batch is fail-closed evidence; it never permits
    silently reducing the sample count." This forecloses the row-count remedy
    but selects none of the others.
  - `57-05-PLAN.md` Task 3 — requires an "exact-4096 resource preflight" before
    optimization and instructs the executor to "abort rather than reduce it if
    resource preflight fails". No such preflight exists:
    `pinn/conformance/preflight.py` contains no memory/resource/watermark
    reference, and `evidence/verify_phase57_evidence.py:247` mentions "resource"
    only when classifying a failure after the fact.
  - `pinn/training/step_log.py:164-234` and `pinn/conformance/census.py:75-79`
    — the ten per-term raw/applied gradient-norm fields are a declared
    contract; the run-start log flags `step_log_fields_registry='PROVISIONAL'`
    with "Owner-ratify the final list before run #1". No source says whether
    that telemetry may be reduced, deferred, or made conditional.
  - No `.planning/REQUIREMENTS.md` requirement, `57-RULING.md` clause, or
    framework-spec section addresses per-step wall-clock cost or the total
    compute budget for the graded band.

- **Mathematical / engineering grounding.** The physics residual compares a
  predicted acceleration against Newtonian force, so it requires a
  *second-order* autograd graph — the graph is constructed with
  `create_graph=True` (`pinn/physics_residual.py:174,176`) so that the first
  derivative is itself differentiable. That graph is built over 4096
  collocation rows in 16 equal-`u` bins. Its memory cost is not the model's
  parameters but the retained intermediate activations needed to differentiate
  a derivative, which scale with rows × depth.

  The decisive measurement is that the two memory signals disagree by a factor
  of ~2,700. The run logged `driver_bytes = 24,964,661,248` (23.25 GiB, the
  Metal allocator's reserved high-water pool) against
  `current_bytes = 9,193,984` (8.8 MiB of live tensors). Live state — the
  parameters, their gradients, and the optimizer moments — is therefore
  negligible, and nothing is retained between steps. The entire 23.25 GiB is
  transient allocation *inside one step*.

  The reason that transient peak is so large is that the graph is traversed six
  times before a single parameter update.
  `_build_gradient_stats` (`pinn/training/controllers.py:482-496`) calls
  `_global_parameter_grad_norm(..., retain_graph=True)` once per loss term to
  produce the five `grad_norm_raw_*` diagnostics, and only then does
  `loss_terms.total.backward()` run (`controllers.py:1706`). Because every
  diagnostic pass sets `retain_graph=True`, no part of the second-order graph
  can be freed until the last traversal completes, so the allocator's pool grows
  to approximately the union of all six working sets rather than the maximum of
  any one. This is a property of the instrumentation schedule, not of the
  physics.

  A related observation sharpens the consequence: at step 0 the physics weight
  is `lambda_phys = 0.0` (PHYS-05 warm-up, `I_warm = floor(0.1 · n_adam) = 30`).
  The physics term therefore contributes nothing to the loss actually optimized
  at this step, yet its full 4096-row second-order graph is constructed and
  traversed twice — once for the `grad_norm_raw_phys` telemetry value (recorded
  as 440.33) and once inside `total.backward()`.

  The guard's denominator is `_DEFAULT_MEMORY_TOTAL_BYTES = 24 * (1024 ** 3)`
  (`pinn/training/guards.py:41`), a hard-coded constant that coincidentally
  equals this machine's `hw.memsize` exactly (25,769,803,776 bytes, Apple M5
  Pro). Because the ratio is measured against *physical* RAM rather than a GPU
  working-set budget, 0.969 means the process was within ~800 MiB of the
  machine's total, and macOS would have been paging. Raising the threshold
  therefore does not release headroom that exists — it permits the run to
  proceed into swap. This is corroborated by the throughput measurement: file
  mtimes split the 852 s run into 181 s of preflight and **671 s for the single
  Adam step**. At that observed rate the three-seed graded band
  (3 × 1000 steps) projects to ~559 h ≈ 23 days. That figure is an upper bound
  measured under paging, not a prediction for a memory-repaired run; but it
  establishes that a guard-threshold change alone does not yield a usable band,
  which is what makes this a genuine multi-option decision rather than a
  one-line recalibration.

- **Agent was tempted to.** Raise `memory_watermark_fraction` from its
  self-declared placeholder 0.7 to something above the observed 0.969 and
  re-launch, on the reasoning that the threshold is explicitly uncalibrated,
  that Phase 57 is the pilot at which the sources say to calibrate it, and that
  the guard is the only thing standing between the run and a completed band.
  This was not done. It would have selected a semantic value the sources
  reserve to the owner, and — on the throughput evidence — would have converted
  a clean 14-minute block into a multi-week paging run with no better prospect
  of completing.

- **What the user needs to decide.** Which remedy (or combination) authorizes a
  band generation 2 window:
  - **(A) Recalibrate the guard only.** Set `memory_watermark_fraction` to an
    owner-chosen value above 0.969 and re-launch unchanged. Cheapest; contradicted
    by the throughput evidence and runs into physical-RAM paging.
  - **(B) Reduce the in-step transient peak.** Make the five per-term
    `retain_graph=True` diagnostic traversals conditional, batched, or
    deferred, and/or skip the physics graph while `lambda_phys == 0`. Preserves
    the 4096-row recipe and the guard exactly. Requires owner ratification
    because `STEP_LOG_FIELDS` / INST-02 / the conformance census declare those
    ten fields, and the registry is flagged owner-ratify-before-run-#1.
  - **(C) Change the execution environment.** A machine with materially more
    memory, or a CUDA device. Also requires deciding what `guards.py:41`'s
    hard-coded 24 GiB denominator becomes, and re-establishing the
    environment fingerprint that the run window admits.
  - **(D) Accept the observed cost** and authorize a multi-week band on the
    current machine with an owner-chosen threshold.
  - **(E) Build the missing resource preflight first** (orthogonal, combinable
    with any of A–D): implement the "exact-4096 resource preflight" that
    `57-05-PLAN.md` Task 3 already requires, so the next window predicts the
    ceiling in seconds instead of discovering it in 14 minutes.

- **Confidence of impact.** **HIGH** — RUN-04, RUN-05, and EVAL-02 are all
  gated on obtaining a completed band or an authorized terminal closure. No
  generation 2 window can be admitted until this is resolved, and options B, C,
  and E each change what the next wave's plan must contain.

- **Status.** OPEN.

- **Resolution note.** _Interim direction (owner, 2026-09-09):_ option **(A)
  recalibrate-only is rejected** and the **probe-first** path is selected —
  measure the memory attribution before committing to a remedy, then implement
  the smallest change that clears the guard, together with **(E)** the resource
  preflight that `57-05-PLAN.md` Task 3 already requires. The measurement is
  bounded, writes no Phase-57 evidence, and touches no admitted config: it holds
  every scientific input identical to generation 1 and varies only the
  instrumentation, by routing the production `_build_gradient_stats` through its
  existing `raw_overrides` parameter so the five `retain_graph=True` traversals
  are not performed. Condition A is already measured by generation 1
  (`driver_bytes` = 24,964,661,248). **The final remedy remains OPEN**: if
  condition B falls well below the 0.7 watermark the cause is the instrumentation
  schedule and a telemetry-contract ratification suffices; if it stays high, the
  single second-order backward over 4096 rows is itself the ceiling and the
  decision moves to option (C) environment. Nothing is ratified until that number
  exists.

  _Probe result (2026-09-09) — the second branch obtained._ Condition B measured
  `driver_bytes = 22,812,983,296` (21.25 GiB), `memory_fraction = 0.8853`, which
  **still trips** the 0.7 watermark. Removing five of the six traversals recovered
  2.00 GiB (8.6%). Two controls confirm the measurement isolated one variable:
  the step record carries
  `grad_stats_provenance = "pre_total_backward|PROBE-B-no-per-term-traversal"`,
  and `grad_norm` is bit-identical to generation 1 (627404864.0), so the
  diagnostic traversals are observation-only exactly as designed.

  **The section-4 instrumentation hypothesis is therefore refuted.** The peak is
  set by the single `total.backward()` over the 4096-row second-order graph,
  which alone needs ~21.25 GiB on this machine. Ratifying the telemetry-contract
  change on its own would not have cleared the guard — which is what the
  probe-first direction was for.

  The probe did return a large **throughput** result: step 0 took **153 s** under
  condition B versus **671 s** in generation 1, a 4.4x speedup, revising the
  three-seed band projection from ~23.3 days to ~5.3 days (both still measured
  under memory pressure, so both remain upper bounds). Memory and throughput
  therefore have different causes and different remedies.

  _Narrowed decision._ The ratified spec already contemplates the memory
  mechanism: `pinn_architecture.md:456` states verbatim, twice, "Microbatching
  preserves complete bin aggregates and never resets the prefix", the GAP-57-01
  resolution names "microbatch-preserved aggregates" among what the authorized
  bounded patch must implement, and `57-02-SUMMARY.md` records that the built
  `index_add` aggregation is microbatch-safe by construction
  (`controllers.py:233-234`). The measurement says the path is microbatch-safe
  but not microbatch-**executed** — 4096 rows enter one graph. Bounding the peak
  requires two passes (compute bin means and hence weights, then walk
  microbatches with those weights fixed and accumulate gradients), which is exact
  only because the causal weights are detached; the codebase already implements
  that pattern for the data term (`accumulate_chunked_data_term`,
  `controllers.py:567`).

  **Whether "microbatch-preserved aggregates" — a correctness property the code
  already satisfies — also authorizes memory-bounded microbatch execution, a
  change to how the step runs, is an inference the agent will not make.** That is
  now the open question, against option (C) environment as the alternative.
  Options (A) recalibrate-only and (B) telemetry-only are both closed by the
  measurement. Option (E), the missing resource preflight, remains open and
  combinable with either. Full working:
  `docs/work/reviews/milestone_v2.3/57-corrected-re-run-the-preserved-evaluation/2026-09-09-stage0-4096-row-resource-diagnosis.md`
  sections 11-14.

---

## GAP-57-03 — generation-1 evidence is single-copy and gitignored, and clearing the re-admission blocker is the action that would destroy it

- **Decision point.** `verify_phase57_evidence.py admit-run-window` fails closed
  on exactly one condition: the target run directory already exists. The
  simplest way to clear it — removing `runs/stage0-v23-smoke/` — is also the
  only way to permanently destroy the generation-1 evidence, because `runs/` is
  covered by a blanket `.gitignore` rule. Where that evidence goes, and whether
  any of it enters git, is not specified by any source.

- **Where in artifact.** `.gitignore:339` (`runs/`); read-only output of
  `evidence/verify_phase57_evidence.py admit-run-window`; the 18 hashed paths in
  `evidence/run-ledger.md` `records[0].artifact_hashes`, every one of which is
  relative to `runs/stage0-v23-smoke/`.

- **Task context.** Post-Wave-6 preparation. Establishing what must happen
  before a generation 2 window can be admitted.

- **Classification.** **Process-artifact schema** — it decides the retention
  location and tracking status of terminal-adjacent run evidence, and the
  run-name namespace for subsequent band generations. Governance reserves this
  class to the owner.

- **Source silence.**
  - `.gitignore:337-339` — `runs/<name>/` is described as "produced at runtime";
    the rule makes no exception for a run whose artifacts are hashed into a
    committed ledger.
  - `git ls-files runs/stage0-v23-smoke` returns 0 against 18 files on disk
    (23 MB), so no precedent exists in-tree: no prior generation's run directory
    was ever tracked.
  - `evidence/README.md` and `57-05-PLAN.md` specify what the ledger and
    blocked state must contain, but neither says where the run directory itself
    is retained, nor whether a blocked generation's directory may be moved.
  - No source assigns run names for a second band generation;
    `57-CONFIG-DELTA.md` fixes the four v2.3 names for generation 1 only and
    notes only that they "do not overwrite the preserved v2.2
    `stage0-rerun-seed4X` directories".

- **Mathematical / engineering grounding.** The integrity argument for this
  phase rests on content addressing: the ledger records a sha256 for each of the
  18 artifacts, so any later reader can re-derive that the evidence is the
  evidence. That guarantee is only as durable as the bytes it addresses. A
  sha256 of a deleted file is not evidence of anything — it is an unfalsifiable
  claim. Because the ledger is now committed and the referenced bytes are not,
  the phase is currently in a state where its own integrity claim can silently
  become unverifiable through an ordinary housekeeping action.

  Verification performed during this preparation: all 18 files were re-hashed
  and compared against both `run-ledger.md` and `blocked-state.json`. 17 of 18
  matched on first check. The exception was
  `artifact_hashes["config.yaml"]`, recorded as a **62-character** string — two
  characters dropped from the middle of a sha256. The correct 64-character value
  was independently attested in `blocked-state.json` `config.resolved_sha256`
  and matched recomputation from disk, so the ledger was corrected to the
  dual-attested value before commit; all 18 now match. That defect is noted here
  because it demonstrates the failure mode concretely: had the bytes been
  deleted first, the truncated hash could never have been adjudicated against
  anything, and the entire generation-1 record would have been permanently
  suspect.

  The run-name question is coupled to this and cannot be settled independently.
  `run.run_name` is a field of the fingerprinted config, so choosing new names
  for generation 2 is a config change that alters the admitted identity; keeping
  the names requires relocating the generation-1 directory, which requires
  deciding where it goes.

- **Agent was tempted to.** Force-add the small non-checkpoint artifacts
  (JSON, logs, `summary.md` — well under 1 MB in total) into the tracked phase
  evidence tree with `git add -f`, leaving the 23 MB of `.pt` checkpoints on
  disk, on the reasoning that this is mechanical preservation of bytes the
  ledger already addresses rather than an invention. This was not done. It would
  select a retention location, a tracking policy, and a partial-preservation
  boundary, all of which are process-artifact schema decisions; and the split
  would silently make four of the eighteen hashed artifacts unverifiable, which
  is the precise failure this gap exists to prevent.

- **What the user needs to decide.** Both parts, together:
  1. *Preservation:* **(A)** force-add all 18 artifacts (23 MB, includes four
     `.pt` checkpoints) into the tracked phase evidence tree; **(B)** force-add
     only the non-checkpoint artifacts and accept that four hashes become
     unverifiable; **(C)** relocate the whole directory to an untracked but
     durable archive path outside `runs/`; **(D)** leave it exactly where it is.
  2. *Namespace:* **(E)** generation 2 uses new run names (e.g. a `g2` suffix),
     which leaves generation 1 untouched and clears the blocker without moving
     anything, at the cost of a fingerprinted config edit; or **(F)**
     generation 2 reuses the existing names, which requires the directory to be
     moved first per the preservation choice.

- **Confidence of impact.** **HIGH** for irreversibility — option D combined
  with any later cleanup destroys the only copy, and the loss is silent and
  permanent. **MEDIUM** for schedule — it blocks the next window but any of the
  listed choices unblocks it quickly once selected.

- **Status.** RESOLVED-WITH-INSTRUCTION (2026-09-09).

- **Resolution note.** Owner selected **preservation option (A) with namespace
  option (E)**: track all 18 generation-1 artifacts, and give band generation 2
  new run names so nothing has to move.

  Executed 2026-09-09. The 18 artifacts are force-added **in place** under
  `runs/stage0-v23-smoke/` rather than copied into `.planning/`, because the
  committed ledger records `artifact_dir = runs/stage0-v23-smoke` with 18 paths
  relative to it; tracking them where they already are keeps the committed
  ledger literally correct and requires no amendment of committed evidence,
  whereas copying would duplicate 23 MB and invalidate the recorded relative
  paths. All 18 re-hash to their ledger values.

  The staged-path policy blocks `runs/*` by design, so the 18 **exact** paths
  were added to `ALLOWED_BLOCKED_PATHS` in
  `scripts/git_policy/validate_staged_paths.py`, which already carried per-path
  precedent. No wildcard was introduced — `runs/` remains blocked for ordinary
  runtime output and any future run directory is still refused. The largest
  blob is 4.86 MB, within the 10 MiB cap, so `ALLOW_LARGE_PATTERNS` is
  unchanged.

  Generation 2 will use `stage0-v23g2-{smoke,seed41,seed42,seed43}`. This
  clears the sole `admit-run-window` fail-closed condition (the existing target
  directory) without touching preserved evidence. `run.run_name` is a
  fingerprinted config field, so the four new configs are a config change that
  belongs to the next wave's plan, not to this preparation.
