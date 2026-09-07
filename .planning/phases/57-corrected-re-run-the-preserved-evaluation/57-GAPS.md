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
executor. Blocking is **dependency-scoped**: the checkpoint-③ and checkpoint-④
owner packets, the EVAL-02 evaluator-pairing characterization (GAP-46-01), and
the evidence-contract design all proceed; only the RUN-04 implementation and
everything gated on the amended recipe actually running wait.

---

## Inherited items due in Phase 57 (not new gaps — carried forward)

- **GAP-54-06** (`.planning/phases/54-recalibration-decision-grounding/54-GAPS.md`;
  `.planning/milestones/v2.3-GAPS.md`) — `DEFERRED (2026-09-04; must resolve at
  checkpoint ③ before RUN-04)`. The L-BFGS second-optimizer-phase semantics:
  whether the detached causal weights are recomputed inside the second phase's
  line searches, and how the second phase re-draws collocation points.
  `54-RULING.md` "Optimizer-phase boundary — explicitly deferred": Phase 56 "may
  not silently choose either second-optimizer-phase behavior." **Due at Phase 57
  checkpoint ③, before any RUN-04 execution.** Routed to the owner as part of
  the checkpoint-③ packet (`57-CONTEXT.md` D-03.3). Not re-adjudicated here.

- **GAP-56-01** (`.planning/phases/56-contract-amendment-train-free-gate/56-GAPS.md`;
  `.planning/milestones/v2.3-GAPS.md`) — `OPEN`. GATE-04 condition (ii)'s pass
  criterion and the controlled-reduction test design. GATE-04 currently renders
  `PASS (INCOMPLETE, unratified: ii)`; RUN-04 may not spend a run on an
  `INCOMPLETE` verdict (`57-CONTEXT.md` D-05). **Must be owner-ratified and
  GATE-04 re-run to a complete PASS before RUN-04.** If the owner takes GAP-56-01
  option D, the condition-(ii) numeric bound joins the checkpoint-③ agenda.
  Phase-56-local; not re-adjudicated here.

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
  - `.planning/REQUIREMENTS.md` "Future Requirements" — "**PLAT-01..07 …**" and
    "**Carried-forward todos**"; FUT-01 (trainer rebuild) is treated as
    post-v2.3 throughout v1.4/v1.6 governance and is not listed as a v2.3
    requirement.
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
    empty." It does not say which phase or requirement picks the implementation
    back up.
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
    anything v2.3 has done, risking a "conformance patch" becoming a de-facto
    partial FUT-01 rebuild under a name that hides it.
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
  - **C — Pull the full FUT-01 trainer rebuild into v2.3** as an explicit
    requirement, since the amended recipe is one of the specs FUT-01 was always
    going to build from.
  - **D — The milestone blocks** pending a separate owner scope decision (e.g.
    an ERW round on the implementation approach, or a new milestone).

- **Confidence of impact.** HIGH — RUN-04, RUN-05, and EVAL-02 are all gated on
  the amended recipe running; the decision sets whether v2.3 can reach its
  terminal state at all, and the authorized code-change size is RUN-04's primary
  risk lever.

- **Status.** OPEN.

- **Resolution note.** _(empty — awaiting owner instruction)_
