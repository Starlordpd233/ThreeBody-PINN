# Phase 54: Recalibration Decision Grounding - Context

**Gathered:** 2026-08-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 54 runs the **governed decision channel** for VER-20 item (e) — the
causal-weight / SIREN-scale calibration mismatch that halted v2.2's conformant
Stage-0 run. Two requirements:

| Req | Deliverable |
|---|---|
| ERW-01 | A **strictly non-recommending** decision packet, presented at a blocking owner gate (checkpoint ①) |
| ERW-02 | Discharge of whichever branch the owner takes — a recorded direct ruling, or the `trainex-r3` Route-B round — ending in **one** ratified recalibration decision (checkpoint ②) |

**Ungated.** Roadmap: *"Depends on: Nothing — ungated (ratified sequencing track
B). Runs in parallel with Phases 53 and 55; its ratified output hard-gates Phase
56."*

**The hard boundary that shapes every decision below.** SCOPE-34: *"The
recalibration decision is owner-ratified, never agent-decided. The agent
assembles and frames the decision packet and, if commissioned, the `trainex-r3`
round; it marks no default, ranks no option, and picks nothing."* The roadmap
strengthens this into a planning constraint: *"No phase may plan an agent-chosen
value… Plans carry the decision channel, the transcription of what was ratified,
and the verification — never the pick."*

So this phase's deliverable is a **question, framed well** — plus the machinery
that makes the framing verifiably neutral. It is not an analysis that arrives at
an answer.

**Not this phase.** The spec amendment itself is Phase 56 (SPEC-01 + SPEC-06,
ratified jointly under SCOPE-38). The characterization probe is Phase 55
(INST-04) and is independent. No framework spec file is edited in Phase 54.

**Phase 54 does not close in one execution pass** — see D-11. Checkpoint ① is
blocking and the roadmap states *"no work proceeds past the gate on an assumed
branch"* (SC-3).

</domain>

<decisions>
## Implementation Decisions

**Delegation of authority.** The owner instructed (2026-08-19): *"you can
automatically select the best option following your best judgement and reasoning,
no need to ask the user for their input unless the choice is absolutely impactful
and significant that must be made by the user."*

This is the same owner-delegated-resolution pattern used in Phase 53 (which
recorded the identical boundary), GAP-45-04, and GAP-46-01. **Its limit is
explicit and load-bearing here:** the delegation covers *how the packet is
assembled, structured, and verified*. It does **not** and cannot cover the
recalibration content — SCOPE-34 reserves that to the owner, and the owner's own
carve-out ("absolutely impactful and significant") points at exactly that class.
Every decision below is an assembly-mechanics decision. **None of them names,
defaults, ranks, or narrows a value of `η_c`, `R̄` normalization, `ω₀`, `N_t`,
or the clip semantics.**

Where the carve-out fired, the item is in **Open Items for Owner Visibility**
rather than decided silently.

### Packet identity, location, and branch neutrality

- **D-01: Author the packet in place at the ERW round root — `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-CONTEXT-MASTER.md`. Do not build it under `docs/work/designs/` and promote it later.**

  Three independent sources point the same way. `.claude/rules/repo-map.md`:
  *"Research packages for trainex decisions live at
  `pinn_instruction/markdown_conversion/framework-specs/trainex-<id>/`, numbered
  as research rounds."* ERW Rule 12 fixes the round name `<track>-rN`, and Rule
  14 makes the round root **the durable record**. Roadmap SC-1 and ERW-01's
  acceptance text both say the packet *"doubles as the `trainex-r3`
  `RESEARCH-CONTEXT-MASTER.md`… so neither gate branch wastes work"* — which is
  only literally true if it is written as that file, in that place, from the
  start. A build-then-promote path reintroduces exactly the rework the
  requirement was written to eliminate.
  — **Reversibility:** reversible — `git mv` plus a delivery-note path update.

- **D-02: Make branch neutrality mechanical, not asserted. ERW-01 ships the master and `DELIVERY-NOTE.md` ONLY. `RESEARCH-AGENT-PROMPT.md` and the `specs/` snapshots are NOT written until the owner commissions the round.**

  The obvious objection to D-01 is that creating `trainex-r3/` before the gate
  looks like presuming the branch — which SCOPE-34 forbids. This decision answers
  it with a structural property rather than a disclaimer.

  ERW's own rule is used affirmatively: *"A package without its prompt is
  incomplete — always ship them together."* An assembled master with **no prompt
  and no snapshots** is therefore, by the runbook's own definition, a package
  that has not been commissioned. The prompt is the artifact that presupposes
  Route B — it is the thing a human pastes to an external agent — so withholding
  it is the mechanically visible proof that no branch was assumed.

  This also maps cleanly onto the requirement split: **ERW-01 = master +
  delivery note + gate; ERW-02 = everything that only exists if Route B fires**
  (prompt, snapshots bundle, Rule-20 tree pin at engagement time, results,
  Rule-19 verification, consolidated decision sheet).
  — **Reversibility:** reversible — the withheld files are additive.

### Packet structure

- **D-03: Mirror trainex-r2's master skeleton, with the Route-B additions the runbook mandates and two v2.3-specific sections.**

  Base skeleton, verbatim from
  `trainex-r2/research_package/RESEARCH-CONTEXT-MASTER.md`: §1 Orientation ·
  §2 Manifest · §3 Source tiering · §4 Questions · §5 Claims register ·
  §6 Provenance · §7 Output contract. Matching it means a commissioned r3 needs
  no restructuring, and a reader who has seen r2 can navigate r3 immediately.

  **Route-B additions (runbook-mandated, not chosen):**
  - `access_mode: open-book` declared in frontmatter, prompt body, and delivery
    note (Rule 16). Grounded in roadmap SC-4 — *"a Route-B (open-book)
    build-design round against the post-repair tree"* — so the mode is
    **transcribed, not selected**.
  - Rules 1–2 **invert** under Route B: repo paths in the master are *expected*,
    and the "attached files only" instruction must **not** appear.
  - The premise-challenge mandate as a **duty** with contradictions reported up
    front as first-class findings (Rule 17) — r2's *"source-verification findings
    that bear on multiple questions"* section is the named shape to request.
  - The read-only bars enumerated in the imperative (Rule 18): no file edited, no
    training run, no evaluation invoked, no commit — plus this project's standing
    bars (no held-out evaluation, no new training runs, no framework-spec edits,
    no remedy selection). Discriminating experiments are **proposed as
    owner-gated options**, never performed.
  - `source_baseline` commit pin (Rule 5) in the master; the Rule-20 **live-tree**
    pin (worktree, branch, commit at engagement) belongs in the delivery note and
    is filled at ERW-02, since it records the tree the agent actually saw.

  **Two v2.3-specific sections:**
  - **§0 Premise qualification** — the trainex-r2 standing block (D-06).
  - **A dedicated "what the assembled evidence cannot answer" section** —
    required by ERW-01's acceptance text (*"it names its own gaps"*) and roadmap
    SC-1. This is the section that makes the packet honest about its own limits,
    and it is the enumeration D-10 refuses to duplicate into the gap registers.
  — **Reversibility:** reversible.

### Making "non-recommending" verifiable by inspection

- **D-04: Two-layer enforcement — a scoped lexical prohibition plus an explicit carve-out for the output-contract section. Record both in a self-audit section inside the packet.**

  Roadmap SC-1 requires that *"a reader can verify **by inspection** that it marks
  no default, ranks no option, and recommends no remedy."* Inspection needs a
  stated criterion, or two readers disagree.

  *Layer 1 — scoped ban.* Recommendation and ranking vocabulary (recommend,
  suggest, prefer, best, most likely, primary candidate, default to, should use,
  ranked, leading option, and ordinal framing of the surfaces) is prohibited in
  the packet's **orientation, mechanism, remedy-surfaces, settled-evidence, and
  question** sections. The self-audit section records the check and its result,
  so the criterion travels with the artifact.

  *Layer 2 — the carve-out that makes Layer 1 coherent.* ERW Rule 7 **requires**
  a build-design round to produce *"suggested default clearly marked"*, door-type
  classification, and a decision sheet — and roadmap SC-4 requires the packet to
  specify exactly that contract for `trainex-r3`. Read naively, SC-1 and Rule 7
  contradict each other. They do not: **the prohibition binds the packet's own
  voice, never its specification of the external agent's deliverable.** §7 must
  use those words; §1–§6 must not. Stating this boundary explicitly is what stops
  a later audit from either flagging §7 as a violation or gutting the Rule-7
  contract to satisfy a lexical sweep.

  This mirrors Phase 53's D-02 reasoning — choose the form a mechanical check can
  actually assert, and name its scope.
  — **Reversibility:** reversible — an audit convention, not a spec contract.

- **D-05: Present each remedy surface as a surface with its mechanical couplings. Do NOT enumerate comparable alternatives per surface.**

  The subtler failure mode is structural rather than lexical: a packet that lists
  "for `η_c`: A, B, C" has already done the framing work that produces a ranking,
  even with every recommendation word stripped. A menu of comparable options **is**
  the ranking substrate, and Rule 7 assigns menu construction to the commissioned
  round (or the ruling to the owner) — not to the packet.

  So each surface states: what the quantity is, where it is specified (`file:line`),
  what contract marker it carries, what it is mechanically coupled to, and what
  the assembled evidence does and does not pin about it. Anything that reads as
  "the choices are…" belongs to trainex-r3's Rule-7 menus or the owner.

  **The one coupling that must be unmissable** is `η_c` ↔ `N_t`/`n_col`: `w_n` is
  an **exclusive prefix sum** over collocation points, so the exponent at point
  *n* grows with the count of preceding points, and calibrating at
  `collocation_count = 16` (`pinn/train.py:1033`) while §3.2 specifies
  `n_col = 4096` moves the exponent by roughly **256×**. Stating a coupling is
  mechanism, not recommendation — and SC-5 makes it consequential (see D-08).
  — **Reversibility:** reversible.

### The trainex-r2 premise qualification

- **D-06: One full qualification block plus a short greppable inline tag on every `trainex-r2` citation.**

  Roadmap SC-2 requires that *"every citation of trainex-r2 in the packet travels
  with its premise qualification."* Repeating a paragraph at every citation site
  is unreadable; a single distant footnote is missable. The inline tag satisfies
  "travels with" while a mechanical check can assert that **no bare `trainex-r2`
  mention exists** — the same greppability argument that decided Phase 53's D-02.

  The block states, at minimum: r2's output contract
  (`trainex-r2/research_package/RESEARCH-CONTEXT-MASTER.md` §7, clause 3) reads
  verbatim *"Do not recommend a remedy. Remedy adjudication is owner-governed
  downstream. Your answers inform that decision; they do not make it."*; the
  consequent **absence list** — no decision sheet, no options menu, no suggested
  defaults, no one-way/two-way door classification; and the **vintage** — the
  round was packaged 2026-07-24 and delivered 2026-07-25, predating the v2.2
  conformance repairs, so its observations describe the pre-repair tree.

  Q3's standing is stated precisely: it framed the diagnosis and independently
  derived the `ω₀=30` mechanism **as a hypothesis** (since confirmed by the
  2026-08-17 audit); it does not contain the answer.
  — **Reversibility:** reversible.

### Evidence depth

- **D-07: Transcribe the confirmed mechanism inline, with its numbers, each carrying a `file:line` citation. Not citation-only.**

  SC-1 requires the packet to **state** the mechanism. The owner reads it at the
  gate as a standalone document; a packet that says "see the audit" has moved the
  work rather than done it. Route B's repo access is an *additional* evidence
  source for the external agent — the runbook is explicit that *"the repository is
  an additional evidence source, not a replacement for the package"* — so
  open-book access is not a licence to thin the packet.

  Minimum inline content: the 2026-08-17 audit's six-row seed/IC table reproduced;
  the chain `first_omega_0 = 30` → second derivative `O(10⁵)` in network units →
  `R̄ ≈ 10¹⁰`; the float32 underflow bound `R̄ > 87.3` for `η_c = 1` on
  unnormalized `R̄`; 15 of 16 collocation weights on the numerical floor; and the
  halt fact `front_idx = 0` at step 501. Each with its citation, so every number
  is re-derivable and Rule-19-checkable later.
  — **Reversibility:** reversible.

### The gate presentation and the ruling record

- **D-08: Present checkpoint ① as a structured decision-record stub the owner fills, not a free-text ask — and pre-declare the `N_t` completeness rule inside it.**

  Fields: **the branch** (rule directly / commission `trainex-r3`); and, if ruling
  directly, one line per surface — `η_c`, `R̄` normalization *and its reference
  scale*, `ω₀` / `first_omega_0`, `N_t` / `n_col`, the causal-exponent clip's
  declared semantics — plus a **SCOPE-38 re-ratification line** for each locked
  contract the pick amends (naming the superseded ruling and carrying a re-issued
  acceptance criterion).

  The stub states up front that **a ruling which does not dispose of `N_t` is
  incomplete and routes back to the owner as a gap, never completed by an agent
  choice.** This is transcribed from roadmap SC-5 and SPEC-06's joint-ratification
  requirement, not invented — and putting it *in the stub* is what turns it from a
  post-hoc rejection into a visible requirement at the moment of ruling.

  The stub is empty of candidate values. It is a form, not a menu.
  — **Reversibility:** reversible.

- **D-09: Record the branch and any direct ruling in a dedicated `54-RULING.md` under the phase directory, with provenance. Do not record a ruling in the gap register.**

  A ruling is not a gap. `54-RULING.md` carries: the date, the exact owner
  instruction as quoted data, the branch taken, the filled stub, and the
  `file:line` of every contract the ruling amends. The delivery note is updated to
  point at it, so the ERW round root stays the durable record (Rule 14). Phase 56
  reads `54-RULING.md` as its authorizing source.
  — **Reversibility:** reversible.

### Gap-register bookkeeping

- **D-10: One anchor gap covering checkpoints ① and ②, in `54-GAPS.md` and the new `.planning/milestones/v2.3-GAPS.md`. Not one gap per recalibration sub-question.**

  The roadmap's gap discipline says *"under SCOPE-34 every recalibration
  sub-question is MUST-surface by construction."* Read as bookkeeping that would
  mean a gap record per surface per sub-question — duplicating the packet into two
  registers and making all three unreadable.

  The coherent reading: **the packet is the surfacing instrument** — that is
  precisely what ERW-01 exists to be — and the registers carry one anchor entry
  that names the decision, classifies it `semantic`, and points at the packet and
  its "what the evidence cannot answer" section as the enumeration. The anchor
  stays `OPEN` until checkpoint ② is discharged.

  `.planning/milestones/v2.3-GAPS.md` does not exist yet; this is the standing
  trigger that creates it. Any **new** source-silent question discovered during
  assembly that the packet's own scope does not cover gets its own full record
  with all required fields.

  Flagged as **Open Item 2** — it is a bookkeeping-granularity call, and the owner
  may prefer the exhaustive form.
  — **Reversibility:** reversible — an anchor can be expanded into per-surface
  records without rework.

### Decomposition and the halt boundary

- **D-11: Phase 54 does not close in this execution pass. Plan for ERW-01 + gate presentation, then stop. Write no branch plan for ERW-02.**

  Roadmap SC-3: *"The agent does not select the branch, and **no work proceeds
  past the gate on an assumed branch**."* Authoring a plan for either branch is
  work proceeding on an assumption, so ERW-02 is a **post-gate replan** once the
  branch is known. Concretely: this phase's execution ends with the packet
  committed and the gate presented; STATE shows Phase 54 in progress, not
  complete; Phase 56 stays closed (SCOPE-34 admits no substitute).

  **Permitted, and useful:** a purely factual **branch-routing note** in the plan
  listing which artifacts each branch would require — file lists and ERW rule
  references only. **Not permitted:** effort estimates, timelines, difficulty
  comparisons, or any framing that implies one branch is cheaper. Cost framing at
  a gate is steering.
  — **Reversibility:** reversible.

### Claude's Discretion

Delegated onward to planner/executor — none changes a ratified quantity or the
neutrality of the packet:

- Plan count and task decomposition within the ERW-01 scope (Phase 45, the direct
  precedent, used four plans for a comparable package assembly).
- Commit granularity within `scripts/agent-commit` discipline.
- Exact section numbering and prose, provided every citation carries its
  `file:line`, every `trainex-r2` mention carries its D-06 tag, and the D-04
  self-audit is present.
- Whether the "what the evidence cannot answer" content sits as its own top-level
  section or as a subsection of §5's claims register — provided it is findable by
  heading.

### Reviewed Todos

Both `todo.match-phase 54` matches (score 0.6 each) are keyword false positives
and are **not folded**. See Deferred Ideas.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### The ERW method (drives the entire deliverable)
- `docs/runbooks/external-research/2026-06-11-external-research-workflow.md` — the canonical runbook. Load-bearing here: the workflow's step 4b, "Files every package round creates", Rule 5 (`source_baseline` pin), Rule 7 (build-design output contract), Rule 9 (gaps never invented), Rule 12 (round naming), Rule 14 (round root is the durable record), Rule 15 (5-attachment cap, bundle don't split), Rule 16 (declare `access_mode`), Rule 17 (Route-B premise-challenge mandate), Rule 18 (read-only bars, imperative), Rule 19 (mandatory per-claim in-repo verification), Rule 20 (pin the tree the agent saw).
- `.claude/rules/repo-map.md` — the trainex/specwork track aliases and the `framework-specs/trainex-<id>/` round-root convention.

### Structural precedent (mirror this)
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_package/RESEARCH-CONTEXT-MASTER.md` — the master skeleton D-03 mirrors; **§7 clause 3 is the premise-qualification anchor** for D-06.
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/DELIVERY-NOTE.md` — delivery-note shape (user-only routing; the ONLY file where repo routing lives under Route A).
- `.planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-CONTEXT.md` — the direct precedent phase (D-01..D-13 assembly decisions, incl. D-04 neutral framing and D-09 claims-register construction).
- `.planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-AUDIT.md` — the ten-check package audit; the model for D-04's self-audit section.
- `docs/work/reviews/milestone_v2.1/45-trainex-r2-erw-package-assembly/2026-07-24-trainex-r2-report-factw-verification.md` — the Rule-19 worked example ERW-02 would follow if Route B fires.

### The decision being framed (ERW-01 content inputs)
- `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md` §"Item (e)" — the routing authority; states the mechanism, names the remedy surfaces, and declares the calibration a research question rather than an engineering default.
- `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md` — the confirmed mechanism and the **six-row seed/IC table** D-07 transcribes. Also the audit Phase 55's INST-04 probe must reproduce.
- `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-DIAG-05-REDERIVATION.md` §3 — the operative diagnosis; supersedes `44-DIAGNOSIS.md` / `44-ERRATUM.md`, treated as **settled, not re-litigated**.
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_results/trainex-r2-research-report.md` — Q3 frames the diagnosis and derived the `ω₀=30` mechanism as a hypothesis. **Every citation carries the D-06 premise qualification.**
- `.planning/milestones/v2.2-GAPS.md` §"Milestone close" — v2.2's inherited obligations.

### Governing scope (hard constraints on what the packet may say)
- `.planning/REQUIREMENTS.md` — ERW-01 (`:85`), ERW-02 (`:86`), SPEC-01 (`:90`), SPEC-06 (`:95`); SCOPE-33 (`:118`), **SCOPE-34** (`:119`, never-agent-decided), SCOPE-35 (`:120`), SCOPE-37 (`:122`), **SCOPE-38** (`:123`, contract re-ratification).
- `.planning/ROADMAP.md` — Phase 54 detail block (`:84`–`:98`): goal, ungated dependency, and the **five Success Criteria** the plans must satisfy; plus the milestone-level "Adjudication discipline" block (`:44`–`:50`) carrying the grounding list, the five owner checkpoints, and the gap discipline.
- `CLAUDE.md` — the STOP protocol and its required gap-register fields; the Git commit protocol (`scripts/agent-commit`, `GIT_AGENT_ID`, `GIT_AGENT_OWNED_PATHS`, no blanket staging); `docs/` placement and frontmatter rules.

### The locked contracts the recalibration would amend (read-only in Phase 54)

> **Line numbers below were re-derived 2026-08-19, after Phase 53's three
> `spec(53)` commits shifted this file.** The line numbers quoted inside
> `.planning/REQUIREMENTS.md` (SPEC-01, SPEC-06) and `.planning/ROADMAP.md` were
> written 2026-08-18 and are now **stale** — see Open Item 5. Use the anchors
> below, and re-derive by content match rather than trusting any line number.

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — **cited, never edited, in this phase**:
  - §2.2 `:181` — *"`first_omega_0` is fixed at `30` and is not scheduled during training."* (the SCOPE-38 contract marker; REQUIREMENTS.md still says `:167`).
  - §2.4 `:267` — the `| **Hyperparameter** | **Recommended Value** | ... |` table header; `:274` — the `| first_omega_0 | 30 | ... |` row (REQUIREMENTS.md still says `:253`). Routed to Phase 56 by Phase 53's unswept inventory.
  - §3.2 `:435` — the `w_n = exp(-η_c Σ_{m=1}^{n-1} stopgrad(R̄_m))` formula; `:445` — the **`> **Phase 35 contract: causal-training mode (LOSS-04; D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A; AC-LOSS-04; ...)**` block fixing `eta_c = 1` (REQUIREMENTS.md still says `:424`). **This is the ruling SPEC-01 must name as superseded if `η_c` changes.**
  - §3.2 `:454` — `n_col=4096` in `sample_collocation_points`; `:461` — *"recommended: 2048-4096"* (REQUIREMENTS.md still says `:433`, `:440`).
  - `:669`–`:671` — *"Clip the causal exponent to avoid underflow, but do not choose a numeric [bound]"* and *"The causal exponent clip is required only to avoid underflow."* — the third SCOPE-38 contract marker.
  - `:692` — the `> **Phase 35 guard: source precedence and deferred values (LOSS-02 / LOSS-03 / LOSS-04; ...)**` block, which defers the numeric clip bound to FUT.
  - §10.6 `:1064` — *Held-Out Physics-Gate Aggregate Statistic*, landed by Phase 53's D-04. Present in the tree; confirms Phase 53 executed.
- `pinn/loss_catalog.py` — `w_n` as an **exclusive prefix sum** over collocation points; the mechanical basis of the `η_c` ↔ `N_t` coupling in D-05.
- `pinn/train.py:1033` — `collocation_count = 16`, the other half of the ~256× coupling. Note: `pinn/` is **not a grounding source** for spec decisions; it is cited here as the divergence being disposed of, per SPEC-06's own text.

### Sibling-phase boundaries
- `.planning/phases/53-narrow-spec-codification/53-CONTEXT.md` — the delegation-boundary precedent and the house CONTEXT/decision format.
- `.planning/phases/53-narrow-spec-codification/53-UNSWEPT-INVENTORY.md` — routes §2.4's "Recommended Value" header to Phase 56; Phase 54 does not touch it.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **The trainex-r2 package as a working template.** `research_package/` contains a master, a prompt, a standalone `CLAIMS-REGISTER.md`, and evidence bundles; `specs/framework-specs-bundle.md` is the Rule-15 bundling pattern (N spec files → 1 attachment). r3 reuses the shapes wholesale.
- **`45-AUDIT.md`'s ten-check structure** — an existing, passed package audit. D-04's self-audit section extends it with the neutrality checks SC-1 adds.
- **Phase 45's four-plan decomposition** — package assembly at this scale has a precedent that did not fit in one plan.

### Established Patterns
- **The round root is the durable record** (ERW Rule 14): master, prompt, delivery note, snapshots, results, and resolution live together. D-01/D-02 keep that invariant while splitting the round root's *population* across ERW-01 and ERW-02.
- **Delivery note is user-only routing.** All repo paths, gate context, and result landing paths live there and nowhere else. Under Route B the master may also carry repo paths (Rules 1–2 invert), but the routing role stays the delivery note's.
- **Claims are tagged `[FACT]` / `[HYP]` and lifted into a claims register** (Phase 45 D-09). Phase 54's mechanism section is now largely `[FACT]` — the 2026-08-17 audit confirmed what r2's Q3 could only hypothesize — and the register should show that transition rather than silently upgrade the rows.
- **Greppable ASCII markers over prose promises** (Phase 53 D-02). D-04 and D-06 both apply it: a convention a `grep` can assert beats a convention a reader must remember.

### Integration Points
- **Phase 56** consumes `54-RULING.md` as its authorizing source and may not open without it (SCOPE-34; roadmap "Depends on: Phase 54 **and** Phase 55").
- **Phase 55 (INST-04)** is independent and runs in parallel, but its probe reproduces the same six-row audit table D-07 transcribes. The packet should cite the audit, **not** Phase 55's output — Phase 55 may not exist yet, and a dependency would break the roadmap's declared independence.
- **`.planning/milestones/v2.3-GAPS.md`** is created by this phase (D-10) — first v2.3 gap, standing trigger.
- **The `54-` phase directory** did not exist before this discussion; it is created here.

</code_context>

<specifics>
## Specific Ideas

- Owner instruction, 2026-08-19: *"you can automatically select the best option
  following your best judgement and reasoning, no need to ask the user for their
  input unless the choice is absolutely impactful and significant that must be
  made by the user."* Recorded as data. It is the authority for D-01..D-11 and,
  by SCOPE-34, **cannot** extend to the recalibration content itself — the same
  boundary Phase 53's context recorded for the identical instruction.
- The sharpest framing risk in this phase is not vocabulary but **structure**:
  a neutral-sounding sentence that enumerates comparable options has already
  ranked them. D-05 is the guard, and it is the decision most likely to be
  eroded during drafting.
- The `~256×` coupling number is worth stating explicitly rather than deriving in
  the reader's head — SPEC-06 states it, SC-5 makes an `N_t`-silent ruling
  incomplete, and it is the single fact most likely to be skipped at a gate.
- ERW Rule 7's "suggested default clearly marked" and roadmap SC-1's "marks no
  default" describe **different documents**. Anyone auditing this packet will hit
  that apparent contradiction; D-04's carve-out exists so they resolve it the
  right way.

</specifics>

<deferred>
## Deferred Ideas

- **The `trainex-r3` prompt, `specs/` bundle, and Rule-20 tree pin** — ERW-02,
  branch-conditional. Deliberately withheld by D-02; withholding them is the
  proof of branch neutrality, not an omission.
- **The Rule-19 per-claim in-repo verification report** — required only if Route B
  fires. Lands under `docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/`
  per the Phase 45 precedent.
- **The consolidated `trainex-r3-resolution-doc.md` and its decision sheet** —
  ERW-02, Route-B branch only.
- **The SPEC-01 / SPEC-06 framework-spec amendment** — Phase 56. No spec file is
  edited in Phase 54.
- **Reconciling §2.4's "Recommended Value" header for `first_omega_0`** — already
  routed to Phase 56 by Phase 53's D-01 inventory. Not re-routed here.
- **Multi-AI fan-out for r3** (ERW Rule 10/11 consolidation join points) — a
  scoping decision that only arises if the round is commissioned.

### Reviewed Todos (not folded)

- **`d-06-static-epsilon-sensitivity-check.md`** (score 0.6) — matched on the
  literal string "D-06", which in this milestone is the *DIAG-06 verdict* (Phase
  58), not the v1.6 Phase-32 epsilon-strategy decision the todo concerns. That
  todo confirms a locked epsilon choice is safe on the admitted set; unrelated to
  the causal-weight/SIREN-scale calibration. **Not folded.**
- **`trainex-r1-research-handoff.md`** (score 0.6) — matched on "trainex" and
  "research". Concerns handing off the r1a/r1b sub-packages, dated 2026-06-11;
  r1 results were delivered and r2 shipped after it, so the todo is stale as
  well as out of scope. **Not folded** — flagged as a candidate for closure
  outside this phase.

</deferred>

<open_items>
## Open Items for Owner Visibility (non-blocking)

Recorded per the owner's escalation carve-out. None blocks planning.

1. **`trainex-r3/` is created before the round is commissioned** (D-01 + D-02).
   Deliberate, and the missing prompt marks it uncommissioned by the runbook's
   own definition. Consequence if the owner rules directly at checkpoint ①: the
   directory persists as the durable provenance of the ruling, and the next ERW
   round takes `r4` rather than reusing `r3`. Flagged because it is the one
   structural choice a reader might read as presuming the branch.

2. **Gap-register granularity** (D-10). One anchor gap for checkpoints ①/② rather
   than one record per recalibration sub-question. The roadmap's *"every
   recalibration sub-question is MUST-surface by construction"* could be read
   exhaustively; the packet is treated as the surfacing instrument instead. Say
   the word and it expands to per-surface records.

3. **Phase 54 will remain open after this execution pass** (D-11). The chain
   delivers ERW-01 and presents the gate; ERW-02 is a post-gate replan. STATE will
   show Phase 54 in progress, and Phase 56 stays closed until checkpoint ② is
   discharged. This is roadmap SC-3 working as designed, not a stall.

4. **`54-RULING.md` is a new artifact name** (D-09). It is not in any template or
   prior phase. Chosen over folding the ruling into the gap register (a ruling is
   not a gap) or into the delivery note (which is ERW routing). Rename freely.

5. **`.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` carry stale
   `pinn_architecture.md` line numbers.** Written 2026-08-18; Phase 53's
   `spec(53)` commits landed 2026-08-19 and shifted the file. SPEC-01's
   `pinn_architecture.md:424` (the `η_c` contract marker it must name as
   superseded) is now `:445`; SPEC-06's `:433`/`:440` are now `:454`/`:461`;
   `first_omega_0`'s `:167` is now `:181`; §2.4's `:253` is now `:267`.
   **This is a trap for Phase 56**, which reads those requirement texts to
   execute a SCOPE-38 amendment and would land at the wrong lines. Corrected
   anchors are in Canonical References above. Not fixed here — editing
   `REQUIREMENTS.md` is outside Phase 54's scope and belongs to the owner or the
   Phase 56 plan.

</open_items>

---

*Phase: 54-recalibration-decision-grounding*
*Context gathered: 2026-08-19*
