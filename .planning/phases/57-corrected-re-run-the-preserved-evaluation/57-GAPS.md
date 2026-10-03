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

- **Status.** RESOLVED-WITH-INSTRUCTION (owner-delegated, 2026-09-09).

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

  **Status change — RESOLVED-WITH-INSTRUCTION (owner-delegated, 2026-09-09).**
  The owner delegated the adjudication expressly ("decide on the previous
  questions yourself; you have control and decision making over this"), the same
  mechanism that ratified the R-1 `loss_explosion_ceiling` on 2026-07-21 and
  discharged Phase 54's checkpoint (2) on 2026-09-04. The delegation is read
  narrowly: it covers engineering scope and conformance judgement, and expressly
  does **not** cover spending EVAL-02's single held-out look, the Phase-58
  verdict (checkpoint (5)), or any ratified scientific value.

  Ruled:

  - **(A) Memory-bounded microbatch execution is in-scope conformance.** The
    ratified spec writes the constraint microbatching must satisfy, twice, inside
    its acceptance criterion; GAP-57-01's authorized inventory names
    "microbatch-preserved aggregates"; and the delivered `index_add` aggregation
    was built microbatch-safe for exactly this purpose. Two passes — bin means
    then detached weights, then per-microbatch gradient accumulation — compute
    the same loss and change no recipe value, satisfying SCOPE-37. Default
    microbatch is 256 rows (one bin), configurable. The residual risk that
    "preserved aggregates" meant only a correctness property is recorded and
    accepted, mitigated by a **blocking** loss/gradient equivalence test against
    the monolithic path across multiple microbatch sizes including one that does
    not divide 4096 evenly. The guard stays at 0.7: this reduces the peak rather
    than moving the alarm, and a peak still above 0.7 afterwards is a new fact
    requiring a new decision.
  - **(B) Per-term gradient telemetry becomes periodic**, on the `run.log_every`
    cadence plus every guard trip and failure bundle. All ten `STEP_LOG_FIELDS`
    names are retained; non-cadence steps emit `null` with
    `grad_stats_complete: false` and an explicit skip provenance, reusing the
    schema's existing `Optional` fields rather than inventing new ones. This is a
    cadence ratification, not a contract reduction. Justified because the
    traversals cost 4.4x wall clock and are provably observation-only
    (bit-identical `grad_norm`), while remaining the instrument that shows which
    loss term drives the front — so they are kept, not deleted. Must be verified
    that the guard's `grad_norm` path (`clip_outcome.total_norm`, independent of
    `_build_gradient_stats`) keeps full per-step fidelity, and that no census,
    validation-gate, or TB consumer depends on per-step availability.
  - **(E) The resource preflight is in scope** — it is already required by
    `57-05-PLAN.md` Task 3 and simply does not exist.
  - **(C) Environment change is not taken**, and is preserved as the fallback if
    the equivalence test or the post-fix peak fails.

  Scope brief with the full reasoning, required shapes, constraints, and
  ordering:
  `docs/work/plans/milestone_v2.3/57-corrected-re-run-the-preserved-evaluation/2026-09-09-band-generation-2-scope.md`.

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

---

## GAP-57-04 — a governed pause is legal but has no run-ledger representation, and the closeout validator still rejects resumed launches

- **Decision point.** The 57-08 owner ruling makes a deliberate operator stop
  followed by `--stage-0-only --resume latest` "a governed pause of the same
  run". No source says how the run ledger records such a run: every v1 record
  field that describes an invocation is single-valued, and `run-window` still
  fails closed on any record whose `launch_kind` is `"resume"`.

- **Where in artifact.** `evidence/run-ledger.md` `records[]` (schema
  `phase57-run-ledger/v1`: single-valued `command`, `process_pid`, `exit_code`,
  `launch_started_utc`, `completion_utc`, `wall_clock_secs`);
  `evidence/verify_phase57_evidence.py:345-346` (`cmd_run_window`);
  `57-05-PLAN.md:98` (the 57-08 amendment).

- **Task context.** Pre-launch check for the band generation 2 calibration
  smoke (`configs/stage0-v23g2-smoke.yaml`), which the owner asked on
  2026-09-13 to start as a run that is interruptible at any time. Surfaced
  before `admit-run-window` because the phase directory is a fingerprinted
  input and cannot be edited once the window opens. Blocking is
  dependency-scoped: this blocks only the ledger record of a run that is
  actually paused, and the `run-window` closeout of a band that contains one.
  Launching the smoke or any graded run, and recording an uninterrupted run, do
  not depend on it.

- **Classification.** **Process-artifact schema** — it fixes the record format
  for a run that spans more than one process, and the pass criterion of the
  `run-window` closeout check.

- **Source silence.**
  - `57-05-PLAN.md:98` grounds four things: a deliberate stop is not an
    operational failure, it is "a governed pause of the same run", it writes no
    blocked-state, and it continues with `--stage-0-only --resume latest`. It is
    silent on the ledger.
  - `evidence/run-ledger.md` writes one record per run at its outcome (history:
    the scaffold in `0640347c`, then the generation-1 record in `9b4f6e05`, with
    no launch-only intermediate). No field holds a stop step, a boundary
    checkpoint, or a second command, PID, or exit code.
  - `verify_phase57_evidence.py:345` fails `launch_kind == "resume"` with "run
    window contains a resumed launch". The check predates 57-08 and was not
    amended with it; nothing says whether it now forbids a governed pause or
    only an unrecorded restart.
  - Phase 50 modelled invocations as a per-record `invocations[]` list with
    `launch_kind` `fresh`/`resume` (`tests/phase50/_evidence_fixtures.py:849`)
    and refused to build a band from a resumed invocation
    (`tests/phase50/test_band_record.py:101-110`) — the pre-57-08 rule. The
    Phase 57 v1 schema did not adopt `invocations[]`; its record-level
    `launch_kind` carries `smoke`, a different meaning of the same key.

- **Mathematical / engineering grounding.** The ledger binds each run's outcome
  to its HEAD, config, command, process, and artifact hashes, so a later reader
  can re-derive that the evidence is the evidence. A governed pause splits one
  optimization trajectory across two OS processes. Numerically that is inert —
  57-08 verified the resumed trajectory bit-identical to an uninterrupted one —
  so no science is at stake. The defect is representational, and it fails in
  either direction. Recorded as a separate `launch_kind: "resume"` record, the
  pause makes `run-window` fail, so a band the owner ruled legitimate could not
  close as RUN-WINDOW-OK: a false blocked outcome. Folded silently into one
  record, the single-valued fields misstate provenance: the first process's
  exit code is the interrupt code 130 rather than the run's outcome,
  `wall_clock_secs` either counts or drops the paused interval, and the
  boundary checkpoint carrying `invariant_b_state` — the artifact whose
  correctness is what makes the pause governed — is addressed by no field.
  Either reading changes what the closeout validator certifies.

- **Agent was tempted to.** Record a paused run as one record with
  `launch_kind` unchanged: take the launch fields from the first invocation and
  the outcome fields from the last, and add a `pauses[]` list holding the stop
  step, boundary-checkpoint sha256, continuation command, PID, and UTC times.
  The reasoning was that "the same run" means one record, and that this keeps
  `run-window` passing with no validator edit. Not done: it adds fields to a
  versioned schema and decides what the single-valued fields describe.

- **What the user needs to decide.**
  - **(A)** One record per run plus a `pauses[]` list (stop step,
    boundary-checkpoint sha256, continuation command, PID, UTC times).
    Single-valued launch fields describe the first launch, outcome fields the
    final process, and `wall_clock_secs` counts active time only. `run-window`
    is unchanged.
  - **(B)** Adopt the Phase 50 `invocations[]` pattern (one entry per process,
    `launch_kind` `fresh`/`resume`), bump the schema to v2, and amend
    `run-window` to accept a resume invocation only when it continues from a
    boundary checkpoint carrying `invariant_b_state`. The validator edit
    touches a fingerprinted path, which the plan forbids mutating during the
    window, so it would land between the last run and closeout.
  - **(C)** One record with no schema change; describe the pause in free text.
  - **(D)** Defer until a pause actually occurs; nothing changes until then.

- **Confidence of impact.** **MEDIUM** — no effect on training or on any run's
  scientific validity. It bites only if a pause occurs, and in that branch it
  decides whether closeout certifies the band correctly (HIGH).

- **Status.** RESOLVED-WITH-INSTRUCTION (2026-09-27).

- **Resolution note.** The owner confirmed option B on 2026-09-27:
  represent each process of a governed pause as one entry in a version-2
  `invocations[]` ledger record. Each entry carries its own command, process,
  timing, exit status, and `fresh` or `resume` launch kind. Amend the verifier
  before admitting the next run window so that it accepts a resume only from a
  boundary checkpoint containing `invariant_b_state`, and verifies that
  checkpoint and the resumed invocation. The September 13 generation-2 smoke
  is historical and incomplete; this ruling does not make it a calibration
  for the final-HEAD generation-3 window. The owner recalled deliberately
  stopping it because they had to cut it off, while the retained log by itself
  establishes only an interrupted status.

---

## GAP-57-06 — the interrupted generation-2 smoke occupies the final-run target after the code HEAD changed

The GAP-57-05 identifier appears in commit 63cb8616 for the chunked-monitor
ruling and is not reused here.

- **Decision point.** How should the interrupted stage0-v23g2-smoke attempt be
  classified and preserved, and which run-name namespace should the final-HEAD
  smoke and band use? Its directory makes Plan 57-05 admission fail, while the
  attempt ran before the current code HEAD and cannot supply D-09's final-HEAD
  smoke.

- **Where in artifact.** 57-05-PLAN.md:24-44,64-73,94-103 (one unchanged HEAD,
  fresh target directories, and the smoke/band sequence);
  evidence/verify_phase57_evidence.py:252-279 (generation-2 target names and
  directory refusal); evidence/run-ledger.md:20-35 (only generation 1 is
  recorded); ignored runs/stage0-v23g2-smoke/status.json (interrupted at step
  30 on 2026-09-13).

- **Task context.** Plan 57-05 Task 1, run on 2026-09-27 from the data-bearing
  milestone/v2.3 worktree. The read-only admit-run-window command exited 1:
  "FAIL-CLOSED: target run directory already exists:
  .../runs/stage0-v23g2-smoke". No training or held-out evaluation was started
  in this attempt. Task 2's operator checkpoint was not reached.

- **Classification.** **Process-artifact schema** — the decision assigns a
  durable identity and provenance record to the prior run and fixes the target
  names and pass criteria for the next admitted window. It also affects Plan
  57-06's candidate and evaluation paths.

- **Source silence.**
  - 57-CONTEXT.md:220-235 and 57-05-PLAN.md:24-44,64-73 require a final-code
    smoke and one commit-free HEAD through the graded runs. Neither says how
    to handle an earlier smoke under the same target name after a fingerprinted
    code change. Commit 63cb8616 changed the frozen monitor and resource
    preflight after the September 13 smoke.
  - 57-GAPS.md:592-618 records the owner's paired decision to retain all
    generation-1 artifacts in place and use new generation-2 names. It fixes
    that collision only; it does not grant a standing policy for another
    generation or choose a retention location for this generation-2 attempt.
  - 57-GAPS.md:622-715 (GAP-57-04) leaves the paused-run ledger schema OPEN.
    It does not decide whether this particular "interrupted" status was a
    deliberate operator pause, how to classify an attempt that cannot join
    the current-HEAD band, or whether the next window uses generation 2 or 3.
  - evidence/README.md:18-19 requires a record for every attempted launch,
    with retries as new records. evidence/run-ledger.md:20-35 has only the
    blocked generation-1 entry. The generation-2 status and summary say
    "interrupted", but the retained log does not establish who requested the
    stop; no source supplies its ledger disposition.

- **Mathematical / engineering grounding.** D-09 makes the smoke a measurement
  of the exact code, configuration, environment, and data that the graded runs
  will use. Its timing calibration includes git_head, so a smoke under the
  pre-63cb8616 code cannot calibrate or validate graded runs under the current
  HEAD, even if a boundary checkpoint can reproduce its earlier trajectory.
  The 31 completed optimizer updates are also short of the 300-step smoke
  budget. Reusing the existing directory would risk overwriting the sole
  local bytes that could verify the interrupted attempt; merely retaining a
  hash in a ledger would not preserve the evidence. A new namespace changes
  the fingerprinted run configs, Plan 57-05 targets, and downstream candidate
  paths; relocating the old directory instead changes the location that a
  provenance record must address. Either choice must be fixed and committed
  before admission, then kept unchanged across the new smoke and band. The
  held-out evaluation remains unspent under every option.

- **Agent was tempted to.** Repeat the prior GAP-57-03 pattern: retain and
  record the interrupted generation-2 attempt in place, allocate generation-3
  names, amend the plan/config/verifier references, and rerun admission. That
  preserves bytes and avoids a name collision, but the owner authorized the
  prior pattern for generation 1 specifically. Applying it again would
  silently decide a new evidence schema and run identity.

- **What the user needs to decide.** First, say whether the September 13
  interruption was a deliberate operator stop under the 57-08 pause ruling,
  an unintended process loss, or unknown. A deliberate-pause record also
  requires a ruling on OPEN GAP-57-04. Then select one disposition:
  - **(A)** Preserve generation 2 in place, record the attempt with an
    owner-approved disposition, and allocate generation-3 names for a fresh
    final-HEAD smoke and band. Amend configs, plan, verifier, and downstream
    paths before readmission.
  - **(B)** Preserve generation 2 under an explicitly named durable archive
    location with a verified manifest, record its original and new locations,
    then reuse the generation-2 target names for a fresh final-HEAD smoke and
    band. Amend plan and verifier references before readmission.
  - **(C)** Stop Plan 57-05 incomplete. Preserve the existing directory and
    held-out evaluation without admitting another run window.

- **Confidence of impact.** **HIGH** — admission demonstrably exits 1, and
  choosing a run identity or moving evidence without a ruling would change
  what the later run-window validator claims to certify.

- **Status.** RESOLVED-WITH-INSTRUCTION (2026-09-27).

- **Resolution note.** The owner confirmed option A on 2026-09-27 and reported
  that the September 13 interruption was a deliberate operator stop, though
  the logs establish only that the process was interrupted. Treat the
  generation-2 smoke as an incomplete historical attempt, retain all 16 files
  at `runs/stage0-v23g2-smoke/`, and record its identity, hashes, and
  disposition. Do not resume that pre-final-HEAD attempt into the new window.
  Use `stage0-v23g3-{smoke,seed41,seed42,seed43}` for the next fresh smoke and
  band, and retarget the verifier, configs, Plan 57-05, and downstream Plan
  57-06 paths before admission. The owner also confirmed exact-path Git
  exceptions for those 16 preserved files and exact size exceptions for the
  two checkpoints above the repository's 10 MiB limit. These are limited to
  the preserved generation-2 attempt; no future run directory is authorized
  by that exception. The separate Plan 57-05 compute checkpoint and Plan
  57-06 one-look evaluation checkpoint remain in force.

---

## GAP-57-07 — a generation-3 operational block would overwrite generation-1 blocked evidence

- **Decision point.** Where should a generation-3 resource, guard, or
  operational blocked-state record be written if that branch occurs? Plan
  57-05 names the already-tracked singleton blocked-state.json, whose exact
  bytes are hash-bound as generation-1 evidence.

- **Where in artifact.** 57-05-PLAN.md:94-103 and its files_modified
  frontmatter (the failure branch writes evidence/blocked-state.json);
  evidence/README.md:22-25 (one blocked-state path);
  evidence/run-ledger.md:43,119-120 (generation-1 path and SHA-256);
  evidence/verify_phase57_evidence.py:_blocked_state (singleton reader).

- **Task context.** Pre-admission review of the owner-approved generation-3
  preparation on 2026-09-27. The historical blocked-state.json is tracked;
  its on-disk SHA-256 is
  2d0e43343f84bf18df571b8f1fd2e1e14b9cd7c8ee416ad6f50ae2bacea1260b,
  matching the generation-1 ledger. No generation-3 run or evaluation has
  begun. The failure branch must be decidable before D-09 freezes the HEAD.

- **Classification.** **Process-artifact schema** — this fixes the path and
  verification rule for a later generation's failure record without erasing
  an earlier generation's evidence.

- **Source silence.**
  - 57-05-PLAN.md:94-103 requires blocked-state.json on any operational
    failure but does not state how a second generation writes it when the
    singleton is already occupied.
  - evidence/run-ledger.md:43,119-120 binds generation 1 to the current
    blocked-state.json path and digest. evidence/README.md:18-25 requires
    append-only run history and a blocked-state record, but gives no
    generation-scoped naming or replacement rule.
  - 57-GAPS.md:592-618 (GAP-57-03) records the owner's instruction to retain
    generation-1 evidence. It does not authorize moving or overwriting its
    blocked-state file. The 2026-09-27 GAP-57-04/06 rulings cover invocation
    history and preservation of generation-2 run files, not blocked-state
    path reuse.
  - evidence/verify_phase57_evidence.py:_blocked_state reads only the
    singleton. It does not establish an alternative path or a rule for
    selecting the blocked record of the active generation.

- **Mathematical / engineering grounding.** The generation-1 ledger's
  SHA-256 claim is re-derivable only while the referenced bytes remain.
  Writing a generation-3 failure to the same path would invalidate that
  claim and erase the earlier failure record. Leaving the old file in place
  without another location would fail to record a generation-3 operational
  block, while treating the old file as the new block would misclassify the
  current run. A generation-scoped record can preserve both histories, but
  the plan and verifier must agree on its path before admission. D-09 forbids
  editing those fingerprinted inputs after the new smoke begins.

- **Agent was tempted to.** Keep the generation-1 singleton untouched and
  add evidence/blocked-state-g3.json for a generation-3 failure, with the
  Plan 57-05 failure path and verifier updated before admission. This is the
  smallest additive change, but choosing a new evidence-file name and
  closeout criterion is an owner-routed schema decision.

- **What the user needs to decide.**
  - **(A)** Retain generation-1 blocked-state.json at its current path; use
    blocked-state-g3.json only if generation 3 has an operational block.
    Amend Plan 57-05, README, and verifier before admission to select the
    current generation's block while preserving the historical digest.
  - **(B)** Preserve generation-1 blocked-state.json under a new durable
    generation-specific path with verified identical bytes, amend the ledger
    reference, then reuse the singleton path for a possible generation-3
    block. This changes a historical path before admission.
  - **(C)** Do not admit generation 3 until a failure-record path is chosen.

- **Confidence of impact.** **HIGH** if generation 3 blocks, because the
  current plan would either invalidate a committed SHA-256 or fail to record
  the new failure. The branch is conditional, but the path choice must
  precede the immutable run window.

- **Status.** RESOLVED-WITH-INSTRUCTION (2026-09-27).

- **Resolution note.** Owner selected **Option A** on 2026-09-27: preserve the
  generation-1 `evidence/blocked-state.json` at its current path and verify its
  ledger-bound SHA-256 before admission. Generation-3 operational/resource/
  guard failures use the additive `evidence/blocked-state-g3.json` path with
  `band_generation=3`, the affected generation-3 `run_name`,
  `evaluation=preserved-unspent`, and `terminal=false`. Plan 57-05, the
  evidence README/ledger contract, verifier, and focused tests were amended
  before admission. The historical singleton is never overwritten.

---

## GAP-57-08 — the sandbox-blocked generation-3 smoke needs a retry identity

- **Decision point.** How should an elevated-host retry be represented after the
  admitted generation-3 smoke directory already exists from a sandboxed
  process that failed before optimization? The failed attempt and its hashes
  must remain append-only while the host-level MPS probe now passes.

- **Where in artifact.** `57-05-PLAN.md` generation-3 target names and fresh
  directory precondition; `evidence/run-ledger.md` generation-3 blocked header
  and smoke record; `evidence/blocked-state-g3.json`.

- **Task context.** Post-run diagnosis on 2026-09-27. The exact generation-3
  smoke command failed in the sandbox because Metal exposed zero devices to
  the process. The same `torch 2.12.1` MPS allocation succeeds with host-level
  access (`mps_available=True`, `device_count=1`). The existing
  `runs/stage0-v23g3-smoke/` directory is therefore a real, recorded
  pre-optimization attempt and cannot be silently reused as a fresh launch.

- **Classification.** **Process-artifact schema** — this chooses how a retry
  after an execution-context failure is named and linked without overwriting a
  governed run record.

- **Source silence.**
  - `57-05-PLAN.md` requires fresh generation-3 target directories but says
    nothing about retrying after a launch-context failure has materialized one.
  - `57-GAPS.md` GAP-57-06 fixes generation-2 preservation and fresh
    generation-3 names, but does not define a same-generation retry identity.
  - `57-GAPS.md` GAP-57-07 fixes generation-scoped blocked-state paths, but
    does not authorize overwriting a current generation's run directory or
    changing its recorded process identity.
  - `evidence/README.md` and `run-ledger.md` require append-only per-process
    provenance and do not define an elevated-context retry generation.

- **Mathematical / engineering grounding.** The run directory contains the
  frozen config, process timestamps, PID, status, and artifact hashes for the
  sandbox attempt. Overwriting it would erase the evidence needed to explain
  why that process did not reach an optimizer step. Reusing the same name for a
  host-level process would make two distinct launches appear to be one run and
  would break the one-record/one-config/process provenance invariant. A fresh
  generation preserves the failed attempt and gives the successful-context
  retry a unique immutable identity.

- **Agent was tempted to.** Preserve the generation-3 block in the ledger,
  increment the final admissible generation to 4, create fresh
  `stage0-v23g4-{smoke,seed41,seed42,seed43}` configs, and rerun only after a
  new admission check under elevated host access. This is the cleanest
  append-only repair, but the generation increment is an owner-routed schema
  decision.

- **What the user needs to decide.**
  - **(A)** Preserve generation 3 as the sandbox-blocked attempt and admit a
    fresh generation 4 for the host-level retry. Amend the plan, configs,
    ledger, verifier, and tests before launching.
  - **(B)** Keep generation 3 as the active identity by relocating the failed
    run directory under a verified archival path, updating all hashes and
    ledger links, then recreate the generation-3 target. This changes the
    current evidence paths before retry.
  - **(C)** Stop without retrying; the MPS host-access diagnosis remains
    recorded and evaluation stays unspent.

- **Confidence of impact.** **HIGH** — silently replacing the existing run
  directory would destroy process provenance, while a new generation changes
  the final-band admission contract.

- **Status.** RESOLVED-WITH-INSTRUCTION (2026-09-27).

- **Resolution note.** Owner selected **Option A** on 2026-09-27: preserve the
  generation-3 sandbox-blocked attempt and admit a fresh generation-4 retry
  with `stage0-v23g4-{smoke,seed41,seed42,seed43}` names. The plan, configs,
  config delta, validation table, README, verifier, and focused tests now
  treat generation 4 as the only admissible final band. The retry must execute
  with host-level Metal access; no recipe, precision, row-count, or data-policy
  change is authorized.

---

## GAP-57-09 — the operator stop did not produce a resumable boundary checkpoint

- **Decision point.** How should the interrupted generation-4 smoke be handled
  after the operator requested a pause but the outer `conda` wrapper received
  `KeyboardInterrupt` before the trainer wrote its required boundary
  checkpoint? The run reached step 40, but `latest.pt` remains the initial
  checkpoint at global step 0 and cannot resume that trajectory.

- **Where in artifact.** `evidence/blocked-state-g4.json`, the generation-4
  record in `evidence/run-ledger.md`, and `runs/stage0-v23g4-smoke/status.json`.

- **Task context.** Operator-requested stop on 2026-09-28. `caffeinate` and the
  outer `conda run` wrapper were launched as the shell command; Ctrl-C caused
  `CondaError: KeyboardInterrupt`, the trainer process exited, and no
  `invariant_b_state` boundary checkpoint was produced.

- **Classification.** **Process-artifact schema** — this determines whether a
  non-boundary operator stop is a resumable invocation or an incomplete
  operational block, and which fresh identity is authorized for later work.

- **Source silence.**
  - `57-05-PLAN.md` permits a deliberate stop only when the in-flight step
    completes and a boundary checkpoint carrying `invariant_b_state` is
    written; it does not define the disposition when the wrapper intercepts
    the signal first.
  - `evidence/README.md` and the v2 invocation verifier require a resume to
    reference a verified boundary checkpoint; they do not authorize synthesizing
    one from the initial checkpoint or from status/log rows.
  - GAP-57-08 resolves the generation identity for the sandbox failure but does
    not cover a later failed pause inside the host-level retry.

- **Mathematical / engineering grounding.** A resume checkpoint is the state
  vector for the optimizer, model, RNG, frozen monitor, and invariant-B
  high-water mark at one completed boundary. The initial checkpoint has
  `global_step=0`; substituting it for the step-40 state would replay a
  different optimization trajectory while claiming same-run continuation.
  Without a boundary checkpoint, the only provenance-safe disposition is an
  incomplete block; a later attempt needs a fresh run identity and admission.

- **Agent was tempted to.** Treat the operator's intent alone as sufficient,
  mark generation 4 paused, and resume with `--resume latest`. That would make
  the verifier accept a checkpoint that does not describe the interrupted
  process, so it is not authorized.

- **What the user needs to decide.**
  - **(A)** Keep generation 4 as an incomplete operational block and create a
    fresh generation-5 identity after fixing signal delivery so the trainer
    receives the interrupt and writes its boundary checkpoint.
  - **(B)** Stop without retrying; preserve generation 4 and the evaluation
    budget with no further run.
  - **(C)** Authorize a fresh generation-5 run but do not attempt interruption;
    let the smoke finish before any pause decision.

- **Confidence of impact.** **HIGH** — the missing checkpoint makes same-run
  resume unverifiable and controls whether a later attempt can share the
  generation-4 provenance.

- **Status.** RESOLVED-WITH-INSTRUCTION (2026-09-28).

- **Resolution note.** Owner selected **Option C** on 2026-09-28: preserve
  generation 4 as the incomplete operator-stop attempt and admit a fresh
  generation-5 smoke without attempting interruption. Generation 5 must use
  the direct pinned environment interpreter under `caffeinate -is` so signals
  reach the trainer if an unexpected stop occurs. No recipe, precision,
  row-count, data-policy, or held-out evaluation change is authorized.

---

## GAP-57-10 — D-10 produced-artifact comparison conflicts with graded launch order

- **Decision point.** When must the seed-42 smoke/graded split-byte, `s_h`, and
  `n_train` equality be asserted? Plan 57-05 requires the produced-artifact
  comparison before *any* graded seed and also launches seed 41 before seed 42.
  The seed-42 graded artifacts do not exist before its run setup.

- **Where in artifact.** `57-05-PLAN.md:26-27,100`; `57-CONTEXT.md:237-245`;
  `pinn/training/run_metadata.py:158-204`.

- **Task context.** The generation-5 seed-42 calibration smoke finished on
  2026-09-28 at admitted HEAD `b151e02d25bd954409ab0dec6a0fda6d9a5d3cb3`.
  It produced `splits.json` SHA-256
  `5846ae5b55104e55a85d644875c3d521f52a9298876d656c6d8903`,
  `s_h=22.321729071058996`, and `n_train=1812`. Its timing calibration is
  valid and the five-rung verify marker is fresh and green. No generation-5
  graded run has launched, so the required graded artifacts do not exist.

- **Classification.** **Process-artifact schema** — this determines the
  timing and pass criterion of a hard prelaunch evidence check. It also affects
  the execution order of the graded band if seed 42 must run first.

- **Source silence.**
  - `57-CONTEXT.md:237-245` requires the smoke and graded seed-42 *runs* to
    produce byte-identical `splits.json` and exactly equal `s_h`/`n_train`, but
    does not say how to prove that result before the graded run exists.
  - `57-05-PLAN.md:26-27,100` requires the comparison before seeds 41/42/43
    are graded while prescribing launch order 41, 42, 43; the two instructions
    are in conflict for produced artifacts.
  - `57-RULING.md:126-138` fixes **evaluation candidate** order 42, 41, 43,
    not the timing of this prelaunch check or the graded training launch order.
  - `pinn/training/run_metadata.py:158-204` checks persisted split bytes and
    metadata scalars; it does not authorize a prospective config-only check
    as a substitute. `pinn/train.py` has no setup-only CLI mode that writes
    graded seed-42 artifacts before training.

- **Mathematical / engineering grounding.** The smoke and graded configs have
  the same seed and admitted-data inputs, so deterministic split construction
  predicts equality. A prediction is weaker than comparing the actual bytes
  produced by both runs. The exact `S_H` and `n_train` values depend on the
  realized train split and admitted corpus. Starting seed 41 first spends a
  long graded run before the mandated seed-42 equality can be observed.
  Changing the plan or verifier after this smoke also changes the fingerprinted
  HEAD, which invalidates the current timing calibration and requires a fresh
  admission and smoke under D-09.

- **Agent was tempted to.** Treat matching seed/data config fields as a pass
  and launch seed 41. That would replace a byte/value assertion with an
  inference and silently relax the prelaunch gate.

- **What the user needs to decide.**
  - **(A)** Keep graded launch order 41, 42, 43. Treat matching config/data
    inputs as the prelaunch check, then assert actual produced-artifact equality
    as soon as seed 42 writes both files; do not launch seed 43 on mismatch.
  - **(B)** Launch graded seed 42 first, assert actual equality immediately
    after its setup artifacts exist, then launch seeds 41 and 43 only if it
    passes. This changes the training launch order but preserves the fixed
    evaluation-candidate order.
  - **(C)** Stop the graded band; preserve the smoke and evaluation budget
    while the plan's timing requirement is adjudicated separately.

- **Confidence of impact.** **HIGH** — the current plan cannot establish its
  literal produced-artifact precondition before seed 41, and either change to
  that rule must be committed before a new immutable run window.

- **Status.** RESOLVED-WITH-INSTRUCTION (2026-09-28).

- **Resolution note.** Owner selected **Option B** on 2026-09-28: launch
  graded seed 42 first, assert its actual `splits.json` bytes and exact
  `s_h`/`n_train` against the smoke as soon as those setup artifacts exist,
  and launch 41 and 43 only after that comparison passes. The evaluation
  candidate order remains 42, 41, 43 and cannot use metric values for
  fallback. The owner also approved repairing the validation-step telemetry
  defect before a fresh immutable run window; the changed HEAD requires a new
  smoke. No scientific recipe tuning or held-out evaluation is authorized by
  this ruling.

---

## GAP-57-11 — preserving completed generation-5 smoke requires new run-artifact policy

- **Decision point.** How should the completed generation-5 smoke be retained
  before the next immutable run window? Its run directory has 23 ignored files
  totaling 71,532,678 bytes, including five checkpoints above the repository's
  10 MiB staged-blob limit. Its timing calibration (455 bytes) and green verify
  marker (863 bytes) are separate ignored singleton files that a new smoke and
  verifier invocation can overwrite. Full retention covers 25 files totaling
  71,533,996 bytes. The exact Git exceptions approved for generations 1 and 2
  do not cover this generation.

- **Where in artifact.** `runs/stage0-v23g5-smoke/` (23 files),
  `runs/.calibration/stage0-timing.json`, and
  `runs/.verify/latest-marker.json`; `evidence/run-ledger.md` (append-only
  generations); `scripts/git_policy/validate_staged_paths.py:9,29-81` (exact
  allowed paths and blob-size exceptions); `.gitignore:339` (`runs/`).

- **Task context.** After the owner selected GAP-57-10 Option B and approved a
  conformance repair, the generation-5 smoke must become historical evidence
  for the future generation-6 admission. It finished at HEAD
  `b151e02d25bd954409ab0dec6a0fda6d9a5d3cb3`, with valid calibration,
  a recorded validation gate FAIL, and the held-out evaluation unspent. A code
  commit will change the HEAD, so that smoke cannot calibrate the new window.

- **Classification.** **Process-artifact schema** — the retention location,
  exact path exceptions, and future verifier hash contract determine whether
  the historical run remains independently re-derivable.

- **Source silence.**
  - `57-GAPS.md` GAP-57-06 Resolution note expressly limits its 16 exact Git
    path exceptions and two size exceptions to the generation-2 attempt;
    future run directories are not covered.
  - `57-GAPS.md` GAP-57-08/09 authorize fresh run identities and preserving
    earlier attempts, but do not select Git tracking or a durable external
    archive for a completed generation-5 run.
  - `57-05-PLAN.md` and `evidence/README.md` require append-only history but
    do not grant a new large-file policy exception for 23 generated artifacts.
  - `scripts/git_policy/validate_staged_paths.py` rejects `runs/*` and files
    over 10 MiB absent exact exceptions.

- **Mathematical / engineering grounding.** A SHA-256 claim is verifiable only
  while the referenced bytes remain available. The run is gitignored, so a
  ledger entry or manifest alone cannot preserve its checkpoint, split,
  validation, and process evidence across worktree cleanup or migration. The
  current calibration and verify marker both bind to the generation-5 HEAD;
  their singleton paths are overwritten by the next successful smoke/verify.
  Tracking every file in Git makes the claim self-contained but adds about
  71.5 MB of immutable blobs to repository history; a separate durable archive
  requires a specified location and a hash-verified restore path before the
  next admission can claim retention.

- **Agent was tempted to.** Follow the generation-2 precedent: add 23 exact
  run-path exceptions, five exact large-checkpoint exceptions, make two
  byte-identical governed snapshots of the timing calibration and verify
  marker, commit a SHA-256/size manifest, and track all 25 files before
  generation-6 admission. The prior ruling's explicit generation-2 limit
  prevents treating that as standing authorization.

- **What the user needs to decide.**
  - **(A)** Track all 23 run-directory files in place, with exact path and
    five checkpoint size exceptions, and commit byte-identical snapshots of
    the calibration and verify marker at governed generation-specific paths.
    Commit a hash/size manifest. This adds 71,533,996 artifact bytes to Git
    history before the new smoke.
  - **(B)** Preserve all 25 files in a specified durable external archive and
    commit a manifest plus restore/verification instructions; identify the
    archive destination before admission.
  - **(C)** Stop generation-6 admission until a retention location is chosen.

- **Confidence of impact.** **HIGH** — without retained bytes, the completed
  smoke's scientific and provenance claims become unverifiable after cleanup;
  with Git tracking, repository history grows by the exact artifact size.

- **Status.** RESOLVED-WITH-INSTRUCTION (2026-09-28).

- **Resolution note.** Owner selected **Option A** on 2026-09-28: track the
  23 exact `runs/stage0-v23g5-smoke/` files in place, add five exact large
  checkpoint exceptions, and commit byte-identical generation-specific
  snapshots of `runs/.calibration/stage0-timing.json` and
  `runs/.verify/latest-marker.json`. The committed
  `evidence/generation-5-retention.json` lists all 25 exact paths, byte sizes,
  and SHA-256 digests. No wildcard exception extends to future runs.

---

## GAP-57-12 — the generation-6 graded seed-42 process was lost without a boundary checkpoint or a retained cause

- **Decision point.** What follows the generation-6 operational block? The
  graded `stage0-v23g6-seed42` process died silently after logging step 513 of
  1000. Its newest checkpoint is the rolling step-510 `latest.pt`, not a
  governed stop-boundary checkpoint. The cause cannot be determined from any
  retained artifact. Three linked choices are open: how the attempt continues
  (same-run resume, fresh generation, or stop), how the next process is
  launched, and how the generation-6 run directories are retained.

- **Where in artifact.** `evidence/blocked-state-g6.json` and the
  generation-6 header and records in `evidence/run-ledger.md` (both written by
  the prior session and still uncommitted at HEAD
  `ef4764f92d9ad23fa90c936166137944dc5e4aea`);
  `runs/stage0-v23g6-seed42/{status.json,logs/train.log,checkpoints/latest.pt}`;
  `evidence/verify_phase57_evidence.py:705-725,733-753,786` (resume
  admission); `evidence/README.md` "Version-2 invocation contract".

- **Task context.** Session resume on 2026-10-02. The prior session recorded
  the block (`blocked_reason: unexpected-process-loss`) on 2026-09-29 and
  stopped without committing. This session gathered read-only forensics only.
  No run was launched, resumed, moved, or deleted.

- **Observed facts (read-only, 2026-10-02).**
  - The process was launched at `2026-09-29T03:46:14Z` (trainer PID 25061,
    `caffeinate` PID 25062). The last heartbeat was at `05:33:21.58Z`
    (`state: running`, step 512, epoch 513). The last logged row is step 513
    and has no traceback. `runs/stage0-v23g6-seed42/failure/` is empty.
  - `pmset -g log` records `PID 25062(caffeinate) ClientDied` at
    `2026-09-29 00:33:25 -0500` (= `05:33:25Z`), with an assertion age of
    `01:47:12`. That entry is not a failure signature. The generation-6 smoke's
    normal exit also logged `ClientDied`, at `22:44:26 -0500` (= `03:44:26Z`),
    matching its ledger `completion_utc`. The entry therefore fixes the end
    time within seconds (active wall time about 6,431 s) but not the cause. No
    sleep, wake, or shutdown entry appears in that minute.
  - The macOS unified log for `00:33:20–00:33:30 -0500` has rotated out (no
    entries returned).
  - The trainer's stdout/stderr were attached to the launching agent exec
    session, which no longer exists (`blocked-state-g6.json` `failure.reason`).
    No session transcript in `~/.codex*/sessions` contains the launch: the two
    files that mention `v23g6-seed42` are 2026-09-28 planning sessions that end
    at `02:29Z`, before the launch.
  - The last `status.json` memory reading is 265 MB current and 361 MB driver
    on MPS. Nothing points to memory pressure.
  - `latest.pt` (sha256 `27c537a1…20917de0`) has kind
    `rolling-not-governed-stop-boundary`, `global_step` 510, and
    `invariant_b_state {front_high_water: 2, last_advance_step: 353}`.
  - Run-directory sizes: `stage0-v23g6-smoke` has 23 files, 71,532,876 bytes,
    5 over 10 MiB. `stage0-v23g6-seed42` has 24 files, 72,433,219 bytes, 5 over
    10 MiB. Both are gitignored, single-copy, and finished/lost respectively.

- **Classification.** **Process-artifact schema.** The choice decides whether
  a process loss without a boundary checkpoint can be a resumable invocation,
  which identity a retry uses, how launch provenance is captured, and how
  historical run bytes are kept re-derivable.

- **Source silence.**
  - `57-05-PLAN.md` Task 3 sends a process interruption to a blocked state with
    Phase 57 incomplete (done). It does not say what may follow.
  - GAP-57-04's Resolution note and the verifier (`:786` "resume does not
    follow a governed interrupted process"; `:705-725` boundary checkpoint
    with `invariant_b_state`) admit a resume only after a governed stop that
    wrote a boundary checkpoint. A `process-lost` invocation with
    `boundary_checkpoint: null` is outside that rule.
  - The 2026-09-12 Stage-0 resume ruling covers deliberate operator stops. In
    those, `train.py` writes a fresh checkpoint at the stop step. Its
    bit-identical proof (8 steps, SIGINT at step 6) used that stop checkpoint,
    not a rolling one.
  - GAP-57-08 and GAP-57-09 authorize fresh generations 4 and 5 for their own
    failures only. GAP-57-09 fixes the launch command (direct pinned
    interpreter under `caffeinate -is`) but not the parent session or where
    stdout/stderr are retained.
  - GAP-57-11 limits its Git retention exceptions to generation 5 and states
    that no wildcard exception extends to future runs.

- **Mathematical / engineering grounding.**
  - *Resume fidelity.* A resume checkpoint is the full state at one completed
    step: model, optimizer moments, RNG streams, frozen monitor, and the
    invariant-B high-water mark. If the rolling step-510 payload carries all of
    them, replaying steps 511-513 on the same HEAD and device should be
    deterministic. That holds for the governed-stop payload and has not been
    shown for the rolling one. Rows 511-513 already exist in `train.log` and
    `train.log.jsonl`, so a resume would give those steps two telemetry
    sources.
  - *Invariant B timing.* The front last advanced at step 353 with
    `front_advance_window_n = 500`, so the no-advance deadline would fall at
    step 853. A resume from step 510 does not move that deadline.
  - *HEAD binding.* Every invocation of a run must share the band HEAD and
    config digest (`:733-753`), and the seed-42 setup check compares against
    the current HEAD (`:610`). Committing the generation-6 evidence moves
    HEAD. A same-run resume would therefore need that evidence to stay
    uncommitted for the rest of the band, about 9 more hours. The verifier
    change it needs is on a fingerprinted path, which may not change inside the
    window, so the change could only land between the last run and closeout,
    as GAP-57-04 option B already anticipated.
  - *Launch robustness.* `caffeinate -is` only blocks sleep. The trainer's life
    and its error stream were both tied to the agent session that launched it,
    so a session ending can kill the run and leave no trace, which is what
    happened. A launch in its own session (detached from the launching shell or
    agent), with stdout/stderr written to a retained file, removes that failure
    path and makes any future crash diagnosable. Signalling the Python PID
    still delivers a deliberate stop.
  - *Retention.* Without retained bytes, the SHA-256 claims in
    `blocked-state-g6.json` and the ledger cannot be re-derived once the
    worktree is cleaned. Git tracking would add about 144 MB to history, with
    10 files over the 10 MiB staged-blob limit.

- **Agent was tempted to.** Commit the generation-6 block as evidence. Retain
  both generation-6 run directories the GAP-57-11 option-A way. Admit a fresh
  generation 7 (`stage0-v23g7-{smoke,seed41,seed42,seed43}`) with the same
  recipe. Launch every process in its own session with stdout/stderr redirected
  to a retained file. This mirrors the GAP-57-08/09 precedent and needs no
  verifier rule for resuming after a process loss. However, the identity,
  launch-mode, and retention choices are owner-routed.

- **What the user needs to decide.**
  - **Continuation.**
    - **(A)** Preserve generation 6 as blocked and admit a fresh generation 7:
      smoke, then 42, then 41/43 after the D-10 check.
    - **(B)** Resume `stage0-v23g6-seed42` from the rolling step-510 checkpoint
      as invocation 2. This needs a new verifier rule for a process-lost
      invocation followed by a resume from a rolling checkpoint, a
      rolling-checkpoint equivalence check, and the generation-6 evidence kept
      uncommitted until the band ends.
    - **(C)** Stop. Preserve generation 6 and the unspent evaluation, with no
      further run.
  - **Launch mode** (A or B). **(L1)** Own session plus stdout/stderr to a
    retained file. **(L2)** The operator launches interactively in a terminal
    with the same command. **(L3)** Unchanged from generation 6.
  - **Retention of the generation-6 run directories.** **(R1)** Git-track in
    place with exact path and size exceptions plus a manifest (GAP-57-11 A
    pattern). **(R2)** External archive plus a committed manifest. **(R3)**
    Leave them ignored in place.

- **Confidence of impact.** **HIGH.** Option B changes the resume-admission
  contract, the launch mode decides whether the next loss can be diagnosed,
  and retention decides whether generation 6's hashed claims stay verifiable.

- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-02).

- **Resolution note.** On 2026-10-02 the owner selected three options.
  - **Continuation (A).** Preserve generation 6 as the blocked attempt and
    admit a fresh generation-7 band with the same recipe: smoke, then seed 42,
    then seeds 41 and 43 once the D-10 setup comparison passes.
  - **Launch mode (L1).** Launch each process detached in its own session,
    using the same trainer command, with stdout/stderr written to a retained
    file. Any verifier or test update this requires lands before admission.
  - **Retention (R1).** Track the generation-6 run directories in Git with
    exact path and size exceptions plus a size/SHA-256 manifest, following the
    GAP-57-11 option-A pattern.

  No same-run resume, recipe change, or held-out evaluation is authorized.

---

## GAP-57-13 — the generation-7 terminal band needs a retention policy before its evidence is committed

- **Decision point.** How should the generation-7 run evidence be retained now
  that the band closed on the authorized invariant-B terminal branch? The
  ledger and `terminal-state.json` address the run files by SHA-256, but those
  files are gitignored and single-copy.

- **Where in artifact.** `runs/stage0-v23g7-smoke/` (23 files, 71,532,415
  bytes, 5 over 10 MiB); `runs/stage0-v23g7-seed42/` (32 files, 85,648,371
  bytes, 6 over 10 MiB, including `failure/trip.json` and
  `checkpoints/failure-stage-0-step-951.pt`); `runs/.launch/stage0-v23g7-*/`
  (10 small files); singletons `runs/.calibration/stage0-timing.json` and
  `runs/.verify/latest-marker.json` (both bound to HEAD `629b1a6c`);
  `evidence/run-ledger.md` and `evidence/terminal-state.json` (uncommitted);
  `scripts/git_policy/validate_staged_paths.py`.

- **Task context.** 57-05 Task 3 on 2026-10-03. The smoke finished. Graded seed
  42 tripped the invariant-B guard at step 951: high-water 2 from step 450, 501
  steps without an advance against N=500. `run-window` returns
  `RUN-WINDOW-TERMINAL-OK`. Seeds 41 and 43 were not launched.

- **Classification.** **Process-artifact schema.** This sets the retention
  location and exact Git exceptions for the run bytes that the terminal
  closure's hashes point at.

- **Source silence.** GAP-57-11 and GAP-57-12 R1 authorized exact retention
  for generations 5 and 6 only and said that no wildcard extends to future runs.
  57-05 and 57-06 require append-only evidence but grant no new path or size
  exception. The staged-path validator rejects `runs/*` and blobs over 10 MiB
  unless an exact exception covers them.

- **Mathematical / engineering grounding.** A SHA-256 claim can be re-derived
  only while the bytes still exist. The terminal closure is now Phase 57's
  scientific result. Its trip record, failure checkpoint, and launcher exit
  record are what let a later reader verify the invariant-B halt. Git tracking
  makes that self-contained at a cost of about 157 MB of history. An external
  archive keeps history small but depends on the archive surviving.

- **Agent was tempted to.** Apply the GAP-57-11/12 R1 pattern: track all 65
  run and launch files in place with exact path and size exceptions, snapshot
  the two singletons, and commit a generation-7 retention manifest.

- **What the user needs to decide.**
  - **(A)** Git-track in place with exact exceptions, singleton snapshots, and
    a size/SHA-256 manifest, as for generations 5 and 6.
  - **(B)** Keep them in a named external archive and commit a manifest with
    restore instructions.
  - **(C)** Commit only the ledger and terminal state now and decide retention
    later. The run bytes stay single-copy until then.

- **Confidence of impact.** **HIGH.** These bytes back the phase's terminal
  scientific outcome.

- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-03).

- **Resolution note.** On 2026-10-03 the owner selected **Option A**:
  Git-track the generation-7 run and launch files in place with exact path
  and size exceptions, snapshot the timing calibration and verify marker,
  and commit a size/SHA-256 retention manifest, as for generations 5 and 6.
  The owner also approved closing Phase 57 on the terminal result: 57-06
  Task 1 writes `no-candidate.json` and stops before any evaluation step.
