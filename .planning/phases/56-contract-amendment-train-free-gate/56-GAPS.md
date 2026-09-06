---
phase: 56
milestone: v2.3
created: 2026-09-06
---

# Phase 56 Gap Register — Contract Amendment & Train-Free Gate

Phase-local record of owner-routed decisions and source-silent gaps surfaced
during Phase 56 work. The milestone-wide index is
`.planning/milestones/v2.3-GAPS.md`. Surfaced under the CLAUDE.md STOP protocol
(v2.3 adjudication milestone). The autonomous best-judgment directive
(2026-09-06) does **not** waive the semantic / process-artifact-schema
MUST-surface class — both entries below are acceptance-check-schema / spec-
convention decisions, not mechanical or test-design calls.

Both gaps were surfaced during the Phase 56 **discuss** step, before any plan or
edit, so they are visible to the researcher and planner rather than hit by the
executor. Blocking is **dependency-scoped**: the core §2.2/§3.2 amendment
(transcription of `54-RULING.md`) and the GATE-04 structural scaffolding
proceed; only the items named in each entry wait.

---

## GAP-56-01 — GATE-04 condition (ii): the operational definition of "differential information / non-degenerate" and the "controlled residual reduction" response test

- **Decision point.** GATE-04's fail-closed conditions are (i) no causal weight
  pinned at the dtype clamp floor, (ii) the weight vector carries "differential
  information" — "not all-floor, not degenerate", and (iii) `front_idx` able to
  advance. `54-RULING.md`'s re-issued AC-LOSS-04 additionally requires GATE-04
  to "fail closed on ... a degenerate weight vector, or a front that cannot
  respond to **controlled residual reduction**." Conditions (i) and (iii) and
  the non-finite checks are precise. Condition (ii)'s numeric/structural
  threshold, and the design of the controlled-reduction response test, are
  fixed by no source.

- **Where in artifact.** `56-CONTEXT.md` "Open Decisions surfaced to the owner";
  will surface again in `56-RESEARCH.md` / `56-PLAN.md` when GATE-04's verdict
  logic is specified. The requirement text: `.planning/REQUIREMENTS.md:100`
  (GATE-04); `.planning/ROADMAP.md:158` (SC-4);
  `.planning/phases/54-recalibration-decision-grounding/54-RULING.md:207`
  (re-issued AC-LOSS-04, "a front that cannot respond to controlled residual
  reduction").

- **Task context.** Discuss-phase servicing of Phase 56's gray areas —
  specifically deciding what GATE-04's pass/fail logic asserts for condition
  (ii), so the planner can hand the executor a concrete threshold.

- **Classification.** Process-artifact schema (an acceptance-check pass
  criterion). Borders on semantic: the threshold encodes a judgement about what
  "healthy causal weighting at initialization" means physically.

- **Source silence.**
  - `.planning/REQUIREMENTS.md:100` — gives (ii) as "a weight vector carrying
    **differential information** (not all-floor, not degenerate)"; no numeric
    or structural test.
  - `.planning/ROADMAP.md:158` (SC-4) — repeats "not all-floor, not
    degenerate"; no test.
  - `54-RULING.md:207` — "a degenerate weight vector" and "a front that cannot
    respond to controlled residual reduction" are named as fail conditions; the
    magnitude of the reduction, the response metric, and the pass margin are
    not stated. `54-RULING.md:124-130` gives an **illustrative** flat-profile
    calculation (endpoint exponent ≈ 15, endpoint weight `exp(-15) ≈ 3.06e-7`,
    float32 normal-floor margin `87.34 / 15 ≈ 5.82`) but explicitly labels it
    "illustrative, not a guarantee; GATE-04 evaluates every actual 16-term
    probe vector and its maximum unclipped prefix" — a reference point, not a
    threshold.
  - `docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/2026-09-02-trainex-r3-rule19-claim-verification.md:345`
    (CC-2) — confirms the three conditions verbatim; does not operationalize
    them.
  - `.planning/phases/55-architecture-characterization-probe/55-CONTEXT.md`
    D-01 — the Phase 55 tier-1 invariant suite asserts `w_2..w_16` **pinned at
    the clamp floor** (the pre-amendment degenerate case); it has no assertion
    for the *healthy* (post-amendment) weight vector, because that was out of
    Phase 55 scope (D-03).

- **Mathematical / engineering grounding.** The causal weight is
  `w_n = exp(-η_c Σ_{m<n} stopgrad(R̃_m))` with `R̃_b = R̄_b / R_ref`,
  `η_c = 1`, a batch-global exclusive prefix over 16 bin-mean residuals. Under
  the ratified recipe `R̃_b ≈ 1` on a flat profile, so the exponent grows
  roughly linearly `0, 1, 2, ..., 15` across the 16 bins and `w_n` spans
  `[exp(-15), 1] ≈ [3e-7, 1]` — a smooth, monotone, ~6.5-decade range. The gate
  must distinguish this from three failure shapes:
  1. **All-floor** — every `w_n` at `causal_clip_min_weight` (the pre-amendment
     state: `R̄` unnormalized ≈ 10¹⁰, exponent argument ≫ 87, immediate
     underflow). Covered by condition (i).
  2. **All-equal / constant** — `w_n` numerically identical across bins (e.g.
     `R̃_b` ≈ 0 everywhere, or `R_ref` mis-scaled so the exponent is
     negligible). The weights carry no ordering information; the causal
     mechanism is inert. **This is the "degenerate" case (i) does not catch.**
  3. **Non-monotone / noise-dominated** — `w_n` varies but not in a way that
     tracks residual accumulation, so `front_idx` (the largest `n` with
     `w_n > 0.5`) is not a meaningful "how far the network has learned"
     pointer.
  Why the choice is consequential: the gate is the SCOPE-35 single-look
  protection. A threshold too loose (e.g. "any variation at all") passes shape
  2 with a hair of float noise and wastes the one preserved Stage-0 run on a
  recipe whose causal weighting is still effectively off. A threshold too tight
  (e.g. "range ≥ 6 decades", keyed to the flat-profile ideal) false-blocks a
  legitimate recipe whose real residual profile is not flat — the six audit
  cases have genuinely different dynamics. The "controlled residual reduction"
  test is the ruling's own construction for separating shape 2/3 from a healthy
  vector: perturb the bin residuals by a known amount and confirm the weight
  vector / `front_idx` responds in the expected direction and magnitude — but
  "known amount", "expected direction and magnitude", and the pass margin are
  all unspecified.

- **Agent was tempted to.** Define (ii) as: `w_2..w_16` (the non-`w_1`
  entries) have coefficient of variation `> 0.1` **and** at least 8 distinct
  non-floor values **and** the sequence is monotone non-increasing **and** the
  max-to-min ratio spans `≥ 2` decades; plus a controlled-reduction test
  applying `R̃_b ← 0.5·R̃_b` uniformly and requiring `front_idx` to increase by
  `≥ 1` or `max(w_n) − min(w_n)` to change by `≥ 10%`. Rationale: this catches
  shapes 1–3 while tolerating non-flat real profiles. **Not recorded as a
  decision** — every constant in it (0.1, 8, 2 decades, 0.5, ≥ 1, 10%) is an
  invented acceptance threshold on the milestone's single-look gate.

- **What the user needs to decide.** The condition-(ii) pass criterion and the
  controlled-reduction test design. Concrete options for the owner (the
  gsd-phase-researcher should flesh these out with the audit's six real weight
  vectors under the amended recipe):
  - **A — dispersion floor.** A coefficient-of-variation (or Gini, or
    distinct-value count) floor on `w_2..w_16`, plus monotonicity, plus a
    minimum dynamic-range span. Owner sets the constants.
  - **B — controlled-reduction only.** No static shape threshold; the gate
    passes iff a `−δ` perturbation of the bin residuals moves `front_idx` (or a
    named weight-vector statistic) by a ratified minimum. Owner sets `δ` and the
    minimum response.
  - **C — both A and B** (recommended by the tempted-to reasoning: A rules out
    the static degenerate shapes cheaply, B confirms live sensitivity).
  - **D — defer the numeric bound to Phase 57 checkpoint ③** alongside the
    invariant-B window, and have Phase 56 ship GATE-04 with conditions (i) and
    (iii) wired and condition (ii) as a logged-but-non-blocking diagnostic
    until ③. (Trades single-look protection completeness for not front-loading
    a threshold decision; the owner may prefer to see real post-amendment
    vectors first.)

- **Confidence of impact.** HIGH — this threshold directly governs whether the
  one preserved held-out evaluation is spent; a mis-set bound either wastes it
  (too loose) or produces a false `rethink` terminal state (too tight).

- **Status.** OPEN.

- **Resolution note.** _(empty — awaiting owner instruction)_

---

## GAP-56-02 — Scope and mechanism of the §2.4 Table 1 locked-vs-default treatment

- **Decision point.** 53-UNSWEPT-INVENTORY item 1 routed §2.4 Table 1's
  "**Recommended Value**" column header and its `first_omega_0 | 30` row to
  Phase 56. `first_omega_0` is ratified NOT AMENDED (`54-RULING.md` `C1`/`D3-A`,
  Block 2), so the value is not in question — but the header calls a §2.2-locked
  constant "Recommended", which is misleading. Marking the row with Phase 53's
  `**[LOCKED]**` / `**[DEFAULT]**` convention would generalize that convention
  beyond its single §4.1 application site, and GAP-45-03 consequence 5
  explicitly left convention generalization undecided.

- **Where in artifact.** `56-CONTEXT.md` D-11 / "Open Decisions"; the target is
  `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
  §2.4 Table 1 (the "Recommended Value" header and the `first_omega_0` row —
  anchors line-drifted, re-derive by content).

- **Task context.** Discuss-phase servicing of Phase 56's gray areas; deciding
  whether the §2.4 cosmetic reconciliation is in Phase 56's grant and, if so,
  by what mechanism.

- **Classification.** Process-artifact schema (a spec-convention decision —
  whether/how the locked-vs-default table convention generalizes).

- **Source silence.**
  - `.planning/phases/53-narrow-spec-codification/53-UNSWEPT-INVENTORY.md:19,29`
    — routes the item to Phase 56 as an owner-visible open item; states marking
    it in Phase 53 would "destroy the independence that is Phase 53's reason to
    exist"; does not instruct Phase 56 to mark it or say how.
  - `pinn_architecture.md` §4.1 Phase 53 contract block — "This site is the
    locked-vs-default convention's first and only application in this phase ...
    Generalization of the convention to other spec tables was explicitly NOT
    decided by this ruling (consequence 5), and remains open."
  - `.planning/REQUIREMENTS.md` SCOPE-33 — authorizes VER-20 items (a)–(e) +
    the `n_col`/`N_t` disposition; the §2.4 header is not obviously any of
    those (SPEC-03 is "add a convention", done in Phase 53; whether *applying*
    it to §2.4 is (e)-adjacent or its own thing is unstated).
  - `54-RULING.md:233` — notes §2.4's `first_omega_0` row "is already routed to
    Phase 56 by Phase 53's unswept inventory and is outside this file's four
    blocks" — confirms the routing, adds no instruction.

- **Mathematical / engineering grounding.** Not a physics decision — a
  documentation-integrity one. The engineering stake: a spec table that labels
  a locked constant "Recommended" invites a future implementer to treat it as
  tunable, which is the exact class of ambiguity SPEC-02/SPEC-03 were created to
  remove. But retro-marking one row in one table, without a ruling on whether
  the convention applies table-wide, creates a *new* inconsistency (why is this
  row marked and the nine others in the same table not?). The three candidate
  mechanisms differ in how much un-ratified convention-generalization they
  commit: (a) per-row markers = most generalization; (b) a header footnote
  pointing to the §2.2 lock = minimal, no convention change; (c) leave as-is =
  none, but the misleading header persists.

- **Agent was tempted to.** Apply option (b): add a one-line note under §2.4
  Table 1 — "Values in this table marked or described elsewhere as locked (e.g.
  `first_omega_0`, §2.2) bind; 'Recommended Value' is the column's historical
  title." — and not touch the convention. Rationale: fixes the integrity issue,
  avoids generalizing the convention Phase 53 left open. **Not recorded as a
  decision** — whether Phase 56 may touch §2.4 at all, and by which mechanism,
  is the owner's scope call.

- **What the user needs to decide.** Whether Phase 56 (A) applies `[LOCKED]`
  markers to the `first_omega_0` row (and, by consistency, audits the rest of
  §2.4 Table 1) — i.e. generalizes the convention; (B) adds a minimal header /
  footnote clarification without touching the convention (recommended); (C)
  leaves §2.4 untouched and the item is re-routed to a future
  documentation-convention pass. Under (A), a follow-on question: does the
  convention then also apply to §2.4 Table 2 and the §3.2 `n_col` recommendation
  wording (unswept item 5)?

- **Confidence of impact.** MEDIUM — low functional risk (`first_omega_0` is
  not changing and everyone agrees it is locked), but it sets precedent for how
  the locked-vs-default convention propagates through the framework spec, which
  is a cross-cutting documentation-governance question.

- **Status.** OPEN.

- **Resolution note.** _(empty — awaiting owner instruction)_
