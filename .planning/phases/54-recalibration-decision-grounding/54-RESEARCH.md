# Phase 54: Recalibration Decision Grounding - Research

**Researched:** 2026-08-20
**Domain:** ERW (External Research Workflow) governance-packet assembly — Markdown/YAML document authoring under a non-recommending constraint. No application code is written in this phase.
**Confidence:** HIGH

## Summary

Phase 54 is not a software-implementation phase — it is a **document-assembly** phase governed by SCOPE-34's hard neutrality bar. The deliverable (ERW-01) is a single Markdown file, authored in place at `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-CONTEXT-MASTER.md`, plus a `DELIVERY-NOTE.md`. Both must mirror an existing, already-audited precedent (`trainex-r2`) and a runbook (the ERW runbook) whose rules are prescriptive down to file names and attachment counts. Because the content itself (the recalibration values) is owner-reserved, the planning risk in this phase is entirely **mechanical**: getting the skeleton, the citations, and the greppable neutrality markers right — not deciding anything about `η_c`, `R̄` normalization, `ω₀`, `N_t`, or the clip.

Every one of the nine structural questions posed in this research's scope was independently re-verified this session by opening the source file and either running `grep`/`sed` against it or reading it with line numbers. Two findings materially change what the plan should cite:

1. **CONTEXT.md's "corrected anchors" in Canonical References are correct.** All eight `pinn_architecture.md` line numbers CONTEXT.md lists as corrected (§2.2:181, §2.4:267/:274, §3.2:435/:445/:454/:461, :669–:671, :692, §10.6:1064) were independently re-derived this session against the live tree and match exactly (one line-boundary nuance noted below). `.planning/REQUIREMENTS.md`'s `:424`, `:167`, `:433`, `:440` anchors are independently confirmed **stale** — the text at those lines is unrelated content, not the cited contract blocks.
2. **"`front_idx = 0` at step 501" is NOT a fact stated in the 2026-08-17 audit document.** A full-file `grep` for `501` in that file returns zero matches. The number lives in `52-DIAG-05-REDERIVATION.md:58` and `50-03-SUMMARY.md:84` instead. If a plan task instructs "transcribe `front_idx = 0` at step 501, citing the audit," the citation will be wrong on inspection. See Finding 5 below for the corrected citation.

**Primary recommendation (assembly mechanics only):** decompose ERW-01 following the Phase 45 precedent's four-wave shape (skeleton/evidence → intellectual core → routing artifacts → owner checkpoint + audit), adapted for the fact that D-02 removes the "author the prompt" step from this phase's scope and adds a D-04 self-audit section, a D-08 gate stub, and a D-09 ruling-record file that Phase 45 did not need. Every mechanical check the plan writes should be a `grep`/`diff`/file-existence assertion in the style of `45-AUDIT.md`'s ten checks and `53-VALIDATION.md`'s per-task map — this project has no pytest-style suite for Markdown-assembly phases and none should be introduced.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

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

#### Packet identity, location, and branch neutrality

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

#### Packet structure

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

#### Making "non-recommending" verifiable by inspection

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

#### The trainex-r2 premise qualification

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

#### Evidence depth

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

  > **Research note (verified this session, see Finding 5 below):** the halt fact
  > "`front_idx = 0` at step 501" is not stated in the 2026-08-17 audit document —
  > a full-file grep for `501` there returns zero matches. It is stated in
  > `52-DIAG-05-REDERIVATION.md:58` and `50-03-SUMMARY.md:84`. This does not change
  > D-07's requirement (the fact still belongs in the packet); it changes which
  > `file:line` the packet must cite for that specific number.

#### The gate presentation and the ruling record

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

#### Gap-register bookkeeping

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

#### Decomposition and the halt boundary

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

### Deferred Ideas (OUT OF SCOPE)

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

#### Reviewed Todos (not folded)

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

### Open Items for Owner Visibility (non-blocking, carried for planner awareness)

1. **`trainex-r3/` is created before the round is commissioned** (D-01 + D-02). Deliberate; the missing prompt marks it uncommissioned by the runbook's own definition. If the owner rules directly at checkpoint ①, the directory persists as the durable provenance of the ruling, and the next ERW round takes `r4` rather than reusing `r3`.
2. **Gap-register granularity** (D-10). One anchor gap rather than one record per sub-question.
3. **Phase 54 will remain open after this execution pass** (D-11). ERW-02 is a post-gate replan; STATE shows Phase 54 in progress; Phase 56 stays closed until checkpoint ② is discharged.
4. **`54-RULING.md` is a new artifact name** (D-09), not in any template or prior phase.
5. **`.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` carry stale `pinn_architecture.md` line numbers**, written 2026-08-18 before Phase 53's `spec(53)` commits shifted the file 2026-08-19. Corrected anchors are in CONTEXT.md's Canonical References — **independently re-verified against the live tree this session; see Finding 7 below.** This is a live trap for Phase 56's SCOPE-38 amendment; not fixed in Phase 54 (out of scope).
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| ERW-01 | Assemble a strictly non-recommending decision packet for the causal-weight/SIREN-scale recalibration and present it at a blocking owner gate. Contents: confirmed mechanism, coupled remedy surfaces, what v2.2's evidence already settled from trainex-r2 Q3, and what the assembled evidence cannot answer. | Findings 1–8 below give the exact skeleton to mirror (Finding 1), the exact delivery-note shape and routing content (Finding 2), the exact runbook rules that bind the packet's construction (Finding 3), the Phase 45 four-wave decomposition precedent (Finding 4), the exact `file:line` citations for every D-07 mechanism fact including one corrected citation (Finding 5), the verified coupling arithmetic plus the previously-unmapped clip-semantics code location (Finding 6), independently re-verified canonical-reference line numbers (Finding 7), and confirmation of what does/does not exist yet on disk (Finding 8). |
| ERW-02 | Discharge the owner gate's branch and produce one ratified recalibration decision — direct ruling or commissioned `trainex-r3`. **Per CONTEXT.md D-11, this execution pass plans ERW-01 + gate presentation only; ERW-02 is a post-gate replan.** | Findings 3 (ERW runbook Rules 7/16/19/20, which govern ERW-02's eventual Route-B contract) and 4 (Phase 45's Rule-19 worked example) are pre-positioned for the future replan. This research does not investigate "how to run trainex-r3" beyond what ERW-01's packet must state as r3's output contract (Rule 7, transcribed not chosen), per the phase's own scope boundary. |
</phase_requirements>

## Architectural Responsibility Map

This phase has no browser/API/database tiers — it has a **governance-pipeline** shape. Mapping capability to tier is what prevents (for example) the packet-assembly tier from silently absorbing a decision that belongs to the owner-decision tier.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Mechanism transcription (`R̄≈10¹⁰`, underflow, saturated weights) | Source-evidence tier (2026-08-17 audit; `52-VER-20-ROUTING-HANDOFF.md`) | Packet-assembly tier (§0/mechanism section, D-07) | The mechanism is already established fact; the packet's job is citation-carrying transcription, not derivation. |
| Remedy-surface enumeration (`η_c`, `R̄` norm, `ω₀`, `N_t`/`n_col`, clip) | Packet-assembly tier (D-05 per-surface presentation) | — | SCOPE-34 forbids any tier from ranking; the packet states location + coupling only, never a menu. |
| trainex-r2 premise qualification | Packet-assembly tier (D-06 block + inline tag) | Source-evidence tier (r2 master §7 clause 3, verified verbatim — Finding 1) | The "travels with citation" requirement binds the packet's presentation layer, not the source document. |
| Branch selection (rule directly vs. commission `trainex-r3`) | Owner-decision tier (checkpoint ①) | — (never agent, never packet) | SCOPE-34 — the packet frames; only the owner selects. |
| Recalibration value pick (`η_c`, `R̄` norm, `ω₀`, `N_t`) | Owner-decision tier (checkpoint ②) | Route-B agent tier (`trainex-r3`, if commissioned — produces Rule-7 menus, never a pick) | SCOPE-34 — the value pick belongs to the owner or, at most, is narrowed to owner-ratified menu options by an *external* agent; never by the in-repo agent. |
| Ruling provenance record | Ruling-record tier (`54-RULING.md`, D-09) | — | Deliberately distinct from the gap register (a ruling is not a gap) and the delivery note (routing, not provenance). |
| Gap surfacing | Gap-register tier (`54-GAPS.md` + `.planning/milestones/v2.3-GAPS.md`, D-10) | Packet-assembly tier (the "what evidence cannot answer" section is the enumeration source) | One anchor gap, not per-sub-question, per D-10; the packet and the register must stay in sync by pointer, not by duplication. |
| Framework-spec amendment | Downstream tier (Phase 56) | — | No framework-spec file is opened for editing in Phase 54 — read-only citation only. |

## Standard Stack

**Not applicable in the conventional sense — this phase installs no packages, libraries, or runtimes.** The "stack" is:

| Component | Role | Verified location |
|---|---|---|
| Markdown + YAML frontmatter | Authoring format for the master, delivery note, ruling record, gap registers | `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_package/RESEARCH-CONTEXT-MASTER.md:1-9` (frontmatter keys: `title`, `package_for`, `role`, `status`, `created`, `source_baseline`, `self_contained`) — Finding 1 |
| Shell verification tooling (`grep`, `diff`, `git diff`, `shasum`, `wc`) | Mechanical acceptance checks, not a test framework | `.planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-AUDIT.md` (all ten checks); `.planning/phases/53-narrow-spec-codification/53-VALIDATION.md:24` (`Framework: none — grep/diff/render-oracle assertions (shell)`) — Findings 4, 9 |
| `scripts/agent-commit` | Git commit protocol (per CLAUDE.md) | See Project Constraints below |

No package installation, no `npm`/`pip`/`cargo` dependency. **Package Legitimacy Audit is not applicable to this phase** — skipped per the audit protocol's own trigger condition ("whenever this phase installs external packages"); this phase installs none.

## Finding 1 — The trainex-r2 master skeleton (verified against source, this session)

CONTEXT.md D-03 states the base skeleton is: *"§1 Orientation · §2 Manifest · §3 Source tiering · §4 Questions · §5 Claims register · §6 Provenance · §7 Output contract."* I opened `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_package/RESEARCH-CONTEXT-MASTER.md` (331 lines) directly this session. **The 7-section count, order, and topic are correct.** The exact heading text carries more detail than CONTEXT.md's shorthand:

| # | CONTEXT.md's shorthand | Exact heading text `[VERIFIED: pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_package/RESEARCH-CONTEXT-MASTER.md]` | Line |
|---|---|---|---|
| 1 | Orientation | `## 1. Orientation` | 19 |
| 2 | Manifest | `## 2. Manifest (the four attached files)` | 48 |
| 3 | Source tiering | `## 3. Source tiering (how to treat each kind of content)` | 57 |
| 4 | Questions | `## 4. The six research questions` | 74 |
| 5 | Claims register | `## 5. Claims register (folded in verbatim from CLAIMS-REGISTER.md)` | 254 |
| 6 | Provenance | `## 6. Provenance` | 297 |
| 7 | Output contract | `## 7. Output contract` | 308 |

Note "The six research questions" — r2 shipped with six questions (Q1–Q6) after the Q6 owner-add (D-13 in Phase 45); the r3 packet is not required to reuse "six," only the section's role and position.

**§7 clause 3, quoted VERBATIM (the D-06 premise-qualification anchor):**

```
3. **Do not recommend a remedy.** Remedy adjudication is owner-governed
   downstream. Your answers inform that decision; they do not make it.
```
`[VERIFIED: pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_package/RESEARCH-CONTEXT-MASTER.md:319-320]`

This matches CONTEXT.md D-06's quotation exactly, word for word. The full §7 output contract (lines 308-329) has six numbered clauses (evidence-citation, trade-off framing, the clause-3 no-remedy bar, gap-recording, claims-listing, and DIAG-04/discriminating-test labeling discipline) plus an opening paragraph specifying "per-question sections (Q1–Q6) plus a dedicated gaps section" as the required external-agent report structure, and a closing sentence: *"This master carries no repository paths. Companion files are referenced by bare filename only; you have no codebase access."* — this last line is the Route-A-only sentence that, per D-03's Route-B additions, **must NOT appear** in the r3 master (Rules 1–2 invert under Route B).

**Frontmatter keys observed** (r2, Route A, `access_mode` absent): `title`, `package_for`, `role`, `status`, `created`, `source_baseline`, `self_contained`. Per D-03/Rule 16, the r3 master adds `access_mode: open-book` to this list.

## Finding 2 — The trainex-r2 DELIVERY-NOTE.md shape (verified, 210 lines)

Section list, in order, as it exists on disk `[VERIFIED: pinn_instruction/markdown_conversion/framework-specs/trainex-r2/DELIVERY-NOTE.md]`:

1. Frontmatter (`title`, `package_for`, `role`, `status`, `created`) + opening warning paragraph ("This file stays in the repository. Do NOT send it to external research agents.")
2. `## The package` (lines 20-37) — sub-package count rationale, question-area list, purpose statement, package root path
3. `## What to send to each external research agent` (41-59) — numbered upload list (exact repo paths), attachment-cap arithmetic
4. `## Access mode — amended 2026-07-24 (ERW Rules 16, 20)` (61-95) — the Route-B override narrative, agent-identity note, access grant details, tree-state pin, consequence for package audits, Rule-19 verification-pass pointer
5. `## Provenance` (97-107) — `source_baseline` + complementary diagnosis evidence pin
6. `## Scope notes (the standing boundaries, in plain terms)` (121-136) — SCOPE-22..26 stated in prose
7. `## Result delivery conventions` (138-151) — result landing path, consolidation path, expected return format
8. `## Standing of the eventual resolution doc` (153-160) — candidate-verdict-source framing, milestone-close/gate-open relationship
9. `## Owner decisions to record at assembly (D-13)` (162-211) — two neutral A/B/C questions with a `**Owner's pick:**` field per question, populated with the verbatim owner answer and date

**Routing information that lives here and nowhere else** (per the file's own opening line and the ERW runbook's "Files every package round creates" list, Finding 3): all repository paths (both the package root and every individual attachment path), the access-mode grant details (worktree, branch, commit-at-engagement), result landing paths (`research_results/<agent>-resolution.md`), the consolidation output path (`<round>-resolution-doc.md`), and — specific to this round — the two owner A/B/C decision stubs with their pick fields. The authored uploads (master, prompt, bundles) are explicitly instructed to carry **zero** repo paths under Route A; the delivery note is "the ONLY file where repo routing lives" (runbook, Files-created list). Under D-08/D-09 for Phase 54, `54-RULING.md`'s existence and its path will need to be pointed at from the r3 delivery note once it exists (D-09: "The delivery note is updated to point at it").

## Finding 3 — ERW runbook: Rules 5, 7, 9, 12, 14, 15, 16, 17, 18, 19, 20, and the file-creation list

All quoted VERBATIM from `[VERIFIED: docs/runbooks/external-research/2026-06-11-external-research-workflow.md]` (265 lines, read in full this session).

**"Files every package round creates"** (lines 96-107):
```
<round-root>/                          e.g. trainex-r1/
  DELIVERY-NOTE.md                     user-facing routing — NEVER uploaded
  specs/                               ONE shared snapshot set for the whole round
  research_package[_a|_b]/             one per sub-package (split rounds) or just one
    RESEARCH-CONTEXT-MASTER.md         the uploaded entry point
    RESEARCH-AGENT-PROMPT.md           paste-ready prompt + user attach-list header
  research_results/[r1a|r1b/]<agent>-resolution.md     (created at delivery time)
  <round>-resolution-doc.md            consolidated output (lands later)
```
Plus (lines 109-122): `RESEARCH-CONTEXT-MASTER.md` carries declared `access_mode`, orientation, companion-file manifest, source-treatment tiering, framed questions, output contract (and under Route B, the premise-challenge mandate + read-only bars + repo-derived evidence label); `RESEARCH-AGENT-PROMPT.md` is "a user-facing header above a horizontal rule listing exactly which files to attach; below the rule, the verbatim prompt" and "**A package without its prompt is incomplete — always ship them together**"; `DELIVERY-NOTE.md` is user-only, carrying "all repo paths, gate context, result landing paths, consolidation join points, standing of the eventual report... the ONLY file where repo routing lives"; `specs/` snapshots are "verbatim copies of the grounding documents, pinned to a commit hash recorded in the master's frontmatter (`source_baseline`)."

**Rule 5** (line 152-154): *"Pin snapshots to a commit hash in the master frontmatter. If a source document is edited after packaging (e.g., a standing note is added), **refresh the snapshot** so the package stays internally consistent."*

**Rule 7** (lines 164-170): *"**Build-design packages** (user picks): options menus (2–4 options, mechanical-surface trade-offs, cross-decision interactions, suggested default clearly marked); a **one-way vs two-way door classification** on every suggested default and deviation; a fill-in **decision sheet** (decision | options | suggested default | door type | your pick); a **composed first-run recipe** as a cross-menu coherence check; "what the runbook inherits"; claims-and-uncertainty register. Prompt must say: *suggest defaults; never decide.*"*

**Rule 9** (lines 176-178): *"All packages: where attached materials are silent or ambiguous, the agent records the gap in the claims register — never invents. (STOP-protocol culture extends to external agents via the prompt.)"*

**Rule 12** (lines 238-241): *"Rounds: `<track>-rN` (e.g., `trainex-r1`, `trainex-r2`); sub-packages `research_package_a/_b`; results `<agent>-resolution.md` under `research_results/[rNa|rNb/]`; consolidated `<round>-resolution-doc.md`. Issue-doc rounds keep the `<NN-issue-slug>` convention."*

**Rule 14** (lines 248-249): *"The package directory is the durable record: keep master, prompt, delivery note, snapshots, results, and resolution together under the round root."*

**Rule 15** (lines 190-202): *"**Maximum 5 uploaded attachments per sub-package.** From 2026-07-07 onward, the package sent to each external research agent contains at most **5 attached files** per sub-package. This is a hard cap; exceeding it requires explicit user override. Files that are never uploaded to the agent — `DELIVERY-NOTE.md` (user-only routing), `research_results/` (created at delivery), the eventual `<round>-resolution-doc.md` (consolidated output) — are routing / provenance / outputs and do not count. **`specs/` snapshots DO count when uploaded**: bundle them into a single `framework-specs-bundle.md` so the bundle is 1 attachment, not N. If a round's input set would exceed 5, **bundle — do not split into more attachments**... The cap applies per sub-package..."*

**Rule 16** (lines 205-208): *"**Declare the mode explicitly** in the master frontmatter (`access_mode: closed-book` or `open-book`), in the prompt body, and in the delivery note. An undeclared mode is a package defect: the agent's behavior, the evidence labels, and the receiving-end verification burden all depend on it."*

**Rule 17** (lines 209-215): *"**Route B carries a premise-challenge mandate, and it is not optional.** The prompt must instruct the agent to test the package's own stated premises against the repository and to report contradictions as **first-class findings reported up front**, not as per-question footnotes. Phrase it as a duty, not a permission: an agent that finds a false premise and buries it has failed the round. The trainex-r2 report's "source-verification findings that bear on multiple questions" section, placed ahead of the per-question answers, is the shape to ask for."*

**Rule 18** (lines 216-222): *"**Route B is read-only, and the prompt must say so in the imperative.** No file edited, no training run, no evaluation invoked, no command with side effects, no commit. On this project the standing bars (no held-out evaluation without owner policy, no new training runs, no framework-spec edits, no remedy selection) apply to external agents exactly as they apply to in-repo agents, and the prompt must enumerate them. Discriminating experiments are **proposed** as owner-gated options, never performed."*

**Rule 19** (lines 223-230): *"**Every repo-derived claim is verified in-repo before use, and the verification is recorded.** A Route B report's repo claims arrive as checkable assertions, not as established facts — they carry a file:line citation precisely so they can be re-derived independently. Produce a verification report under `docs/work/reviews/` with a per-claim verdict before any claim informs a decision, a roadmap, or a spec edit. This is a required step of the round, not a discretionary extra."* — with the worked example `docs/work/reviews/milestone_v2.1/45-trainex-r2-erw-package-assembly/2026-07-24-trainex-r2-report-factw-verification.md` cited and **confirmed to exist on disk** (12,714 bytes) `[VERIFIED: file exists, this session]`.

**Rule 20** (lines 231-235): *"**Pin the tree the agent saw.** Record in the delivery note how access was granted (which worktree, which branch) and the commit the working tree was at during the engagement. Open-book file:line citations are only re-derivable against that state; without the pin they rot silently as the tree moves. The attachment `source_baseline` pin does not cover this — it pins the snapshots, not the live tree."*

Also load-bearing for D-03's Route-B posture (Rules 1-2 inversion, quoted verbatim, lines 136-142): *"Under Route B, Rules 1–2 invert: repo paths in the master are *expected*, since the agent can resolve them, and the "attached files only" instruction must NOT appear — it directly contradicts the mandate in Rule 17. A Route B master still ships the attachments and still pins them, because they frame the questions and fix the baseline; the repository is an additional evidence source, not a replacement for the package. Package audits that check "zero repo-path markers" apply to Route A packages only."*

## Finding 4 — Phase 45 precedent: plan decomposition and the 45-AUDIT ten-check structure

**Plan decomposition** `[VERIFIED: .planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/, directory listing + 4 SUMMARY.md files read this session]` — four plans, one per wave, strictly sequential:

| Plan | Wave | Requirement | What it built |
|---|---|---|---|
| 45-01 | 1 | PKG-09 | Package tree skeleton + PKG-09 commit-pinned snapshot substrate: byte-identical `44-DIAGNOSIS.md` snapshot, `specs/framework-specs-bundle.md`, `research_package/run-evidence-bundle.md`, `research_results/.gitkeep`. Pure assembly/curation. |
| 45-02 | 2 | PKG-10, PKG-11 | The "intellectual core": the standalone `CLAIMS-REGISTER.md` (16 F-rows / 8 H-rows) and `RESEARCH-CONTEXT-MASTER.md` itself — manifest, source tiering, the neutrally framed questions, the folded-in claims register, dual provenance pins, the neutral output contract. |
| 45-03 | 3 | PKG-10 | The two routing artifacts: paste-ready `RESEARCH-AGENT-PROMPT.md` and the `DELIVERY-NOTE.md` draft, including the two D-13 owner questions framed but explicitly marked `PENDING` (not pre-answered). |
| 45-04 | 4 | PKG-11 | The blocking owner checkpoint (both D-13 questions answered verbatim) + the package-wide amendments those answers triggered (Q6 added) + the final `45-AUDIT.md` ten-check audit. |

Phase 54 differs from this precedent in two structural ways worth flagging for plan-count discretion (owned by the planner per CONTEXT.md's Claude's Discretion): **(a)** D-02 removes the "author the prompt" step entirely from ERW-01's scope (no Wave-3-style prompt authoring this pass — the prompt is deferred to ERW-02), and **(b)** Phase 54 adds artifacts Phase 45 did not need: a D-04 self-audit section *inside* the master itself, a D-08 gate-decision stub, a D-09 `54-RULING.md` (only populated if the owner rules directly), and D-10's creation of `.planning/milestones/v2.3-GAPS.md`.

**45-AUDIT.md's ten-check structure** `[VERIFIED: .planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-AUDIT.md, read in full this session]`:

1. Tree completeness — `ls`/`find` over every expected artifact path
2. Upload count (4 of at most 5; prompt header == delivery note) — grep both lists, confirm identical
3. Self-containment (zero repo-path markers in authored uploads) — `grep -cE '(\.planning|runs/|pinn_instruction/|framework-specs/|markdown_conversion/|milestones/|evidence/diag|docs/runbooks)'` per file, expect 0 (Route-A-only check; N/A once r3 is Route B per the r2 delivery note's own "Consequence for package audits" note)
4. Snapshot fidelity (diagnosis byte-identical) — `diff -q` + `shasum -a 256` against the source
5. Drift check (no source changed since `source_baseline`) — `git diff <baseline>..HEAD -- <path> | wc -l` per snapshotted/excerpted source, expect 0
6. Pin consistency — `grep -c <pin>` per file, confirm the same `source_baseline` string appears everywhere it should
7. Neutrality re-audit (D-04 analog; SCOPE-26 in r2 / SCOPE-34 in r3) — automated `grep -ci 'suggest defaults'` = 0, plus a manual per-question attestation that each "what a complete answer specifies" block names no value
8. Claims-register sync (D-03 analog) — `grep -cE '^\| F-[0-9]+'` / `'^\| H-[0-9]+'` counts must match between the standalone register and the master's folded section
9. Boundary attestation (SCOPE-22..26 analog; SCOPE-33..38 for v2.3) — `git status --short` over every source tree touched, confirm empty; explicit per-scope-item attestation sentence
10. Requirement and success-criteria traceability — a table mapping each requirement/roadmap SC to the checks that certify it

D-04's self-audit section (inside the *packet itself*, not a separate audit file) is explicitly framed in CONTEXT.md as extending this structure with the neutrality checks roadmap SC-1 adds — the planner should treat 45-AUDIT.md as the check-library to draw from, not a template to copy wholesale (Phase 54's checks are partially internal to the packet, partially a separate phase-closing audit).

## Finding 5 — Where each D-07 mechanism fact actually lives (file:line, verified this session)

| Fact | Exact figure | Verified location | Note |
|---|---|---|---|
| Six-row seed/IC table | 6 data rows (seeds 41, 42, 43, 0, 7, and an alt-mass/random-IC 41 variant); columns `‖r′‖, ‖v′‖, ‖a′‖=‖d²r′/du²‖, ‖F_grav‖, min pairwise sep, R̄ median, front_idx` | `[VERIFIED: docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md:142-151]` (table header line 142; the six data rows are lines 144-149; the parenthetical note "(All six rows are the probe's printed output; medians over the 16 collocation points.)" is line 151) | Confirmed present exactly where CONTEXT.md says. |
| `first_omega_0=30` → `‖a′‖` ~O(10⁵) → `R̄~10¹⁰` | `‖a′‖` column values 1.94×10⁵–2.79×10⁵; `R̄` median column 1.25×10¹⁰–2.60×10¹⁰ | `[VERIFIED: same file, §6b table (142-151) for the numbers; §6c mechanism prose, lines 163-169, for the causal narrative]` | The exact phrase "`O(10⁵)`" for the second derivative also appears independently in `[VERIFIED: .planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md:37]`: *"an `ω₀=30` SIREN's second derivative is `O(10⁵)` in the network's own units, giving `R̄≈10¹⁰`"* — this is the "routing authority" document CONTEXT.md's Canonical References names as the source of the remedy-surface list; both documents corroborate the same chain independently. |
| Float32 underflow bound | `R̄ > 87.34` (rounds to the "87.3" CONTEXT.md/REQUIREMENTS.md use) | `[VERIFIED: docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md:127]`, table row: `"Point where \`exp(−η_c R̄)\` underflows float32 \| \`R̄ > 87.34\` → **8.46 decades below the median**"` | The rounded "87.3" form also appears at `52-VER-20-ROUTING-HANDOFF.md:40`. |
| 15-of-16 collocation weights on numerical floor | `w_2…w_16` pinned at the float32 tiny clamp; `w_mean = 0.0625 = 1/16` exactly | `[VERIFIED: docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md:121]`: *"`w_min` is pinned at the float32 tiny clamp on 502/502 steps and `w_mean = 0.0625 = 1/16` exactly on 502/502 steps, so `w_2…w_16` are all at the clamp floor..."* | `w_1 = 1` always (by construction, `pinn/loss_catalog.py:340`), so the 15 floored weights are `w_2` through `w_16` inclusive. |
| **`front_idx = 0` at step 501** | — | **NOT in the 2026-08-17 audit** — `grep -c "501" <that file>` returns `0` `[VERIFIED: grep run this session against the full file, zero matches]`. Correct citations: `[VERIFIED: .planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-DIAG-05-REDERIVATION.md:58]` — *"Invariant B (front-advance-within-N, `N=500`, Phase 49 GATE-03) HALTed at step 501: `front_idx=0` on all 502 logged steps (`trip.json`, `50-05-SUMMARY.md`)."* and `[VERIFIED: .planning/milestones/v2.2-phases/50-valid-stage-0-re-run/50-03-SUMMARY.md:84]` — *"**Terminal reason:** generation-3 seed 41 invariant-B HALT at step 501 (\`front_idx\` stayed 0 for the full \`N=500\` window; \`threshold_provisional=false\`)."* | **This is the one D-07 fact whose citation target must change.** The audit document itself only states "front_idx: 0 on 502/502 steps" (§6a, no single-step number, describing the whole retained log) and "front_idx: 0" in the six-row *initialization-only* table (§6b — that table has no step number at all, since it characterizes the architecture before any training step). "Step 501" is the run's terminal HALT step, a fact from a different, later document. |

**Planning implication (mechanics only, not a recalibration opinion):** if a plan task says "transcribe the five D-07 facts, citing the 2026-08-17 audit for all five," the task's acceptance check will fail on inspection for the fifth fact. The task should cite `52-DIAG-05-REDERIVATION.md:58` (or `50-03-SUMMARY.md:84`) for the step-501 HALT fact specifically, while the audit document remains the correct citation for the other four.

## Finding 6 — Coupling arithmetic, verified line-by-line, plus the previously unlocated clip-semantics code site

**`w_n` as an exclusive prefix sum** `[VERIFIED: pinn/loss_catalog.py:283-347, read in full this session]`:

```python
283:def causal_physics_loss(residuals_per_time, *, eta_c=CAUSAL_ETA_C, times=None,
284:                        dtype, device, return_details: bool = False):
...
326:    eta = torch.as_tensor(eta_c, dtype=dtype, device=device)
327:    # Prefix sum of stopgrad(Rbar) for the STRICTLY preceding points.
328:    # cumsum_excl[0] = 0; cumsum_excl[n] = sum_{m<n} Rbar_m.detach()
329:    detached = rbar.detach()
330:    cumsum = torch.cumsum(detached, dim=0)
331:    # Shift right by one: exclusive prefix.
332:    zeros = torch.zeros(1, dtype=dtype, device=device)
333:    cumsum_excl = torch.cat([zeros, cumsum[:-1]], dim=0)
334:    clip_facts = resolve_causal_clip_facts(dtype, device)
335:    exponent = -eta * cumsum_excl
336:    floor = torch.as_tensor(
337:        clip_facts["causal_clip_exponent_floor"], dtype=dtype, device=device,
338:    )
339:    weights = torch.exp(torch.clamp_min(exponent, floor))
340:    # w_1 is identically 1 by construction (cumsum_excl[0] = 0); pin via constant.
341:    _ = CAUSAL_W1
342:    loss = (weights * rbar).mean()
```

This confirms CONTEXT.md D-05's citation (`pinn/loss_catalog.py:328–:331`) sits inside the exact function and mechanism it describes — the "exclusive prefix sum" is implemented by right-shifting a `torch.cumsum` and prepending a zero (lines 330-333), matching the docstring's own restatement of the formula at lines 292-293 (`w_1 = 1`, `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`).

**`collocation_count = 16`** `[VERIFIED: pinn/train.py:1033]`:
```python
1032:    collocation_sampler = CollocationSampler(
1033:        collocation_count=16,
1034:        rng=np.random.default_rng(int(config.run.seed)),
```
Exact match to CONTEXT.md's citation.

**`n_col=4096`** `[VERIFIED: pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:454,461]`:
```python
454:def sample_collocation_points(u_min=0.0, u_max=1.0, n_col=4096, strategy='uniform',
...
461:        n_col: Number of collocation points (recommended: 2048-4096)
```
Exact match. `4096 / 16 = 256` exactly — the "roughly 256×" figure in D-05 is verifiable arithmetic on two already-fixed numbers (the code's actual `N_t` and the spec's stated `n_col`), not itself a recalibration pick.

**Previously unmapped: the causal-exponent clip's code location** (relevant because "the causal-exponent clip's declared semantics" is one of ERW-01's five named remedy surfaces, and D-05 requires stating "what the quantity is, where it is specified" for every surface — this was not explicitly asked for in the research scope but directly completes it):

`[VERIFIED: pinn/constants.py:71-72]`:
```python
71:CAUSAL_ETA_C = 1.0
72:CAUSAL_W1 = 1.0
```

`[VERIFIED: pinn/loss_catalog.py:73,77]`:
```python
73:CAUSAL_CLIP_FORMULA = "exp(clamp_min(x_n, causal_clip_exponent_floor))"
...
77:def resolve_causal_clip_facts(dtype, device) -> dict[str, object]:
```
(`causal_clip_exponent_floor` — the value consumed at `loss_catalog.py:337`, shown above — is derived dynamically per dtype/device, not a hardcoded literal; `resolve_causal_clip_facts` is the function that computes it.) This is the code-side implementation of the spec's `pinn_architecture.md:668-671` clip language ("required only to avoid underflow... do not choose a numeric [bound]," verified in Finding 7). Reporting this location is mechanism (where the quantity is currently specified in code), not a recommendation about what the clip semantics should become.

## Finding 7 — CONTEXT.md's "corrected anchors" verified against the live tree

Every anchor CONTEXT.md's Canonical References lists as corrected was independently re-derived this session by opening `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (1098 lines) at the cited offsets and reading with line numbers.

| Claim | CONTEXT.md's corrected anchor | Verified this session | Verdict |
|---|---|---|---|
| `"first_omega_0` is fixed at `30` and is not scheduled during training."` | §2.2 `:181` | `[VERIFIED: pinn_architecture.md:181]` — exact text present | **Correct** |
| `\| **Hyperparameter** \| **Recommended Value** \| ... \|` table header | §2.4 `:267` | `[VERIFIED: pinn_architecture.md:267]` — exact text present | **Correct** |
| `\| first_omega_0 \| 30 \| ... \|` row | §2.4 `:274` | `[VERIFIED: pinn_architecture.md:274]` — exact text present | **Correct** |
| `w_n = exp(-η_c Σ_{m=1}^{n-1} stopgrad(R̄_m))` formula | §3.2 `:435` | `[VERIFIED: pinn_architecture.md:435]` — `w_n = \exp\left(-\eta_c \sum_{m=1}^{n-1} \operatorname{stopgrad}(\bar R_m)\right),` — this exact LaTeX line | **Correct** |
| Phase-35 contract block fixing `eta_c = 1` | §3.2 `:445` | `[VERIFIED: pinn_architecture.md:445]` — `> **Phase 35 contract: causal-training mode (LOSS-04; D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A; AC-LOSS-04; ...)**` — exact match | **Correct** |
| `n_col=4096` in `sample_collocation_points` | §3.2 `:454` | `[VERIFIED: pinn_architecture.md:454]` — see Finding 6 | **Correct** |
| `"recommended: 2048-4096"` | §3.2 `:461` | `[VERIFIED: pinn_architecture.md:461]` — see Finding 6 | **Correct** |
| `"Clip the causal exponent to avoid underflow, but do not choose a numeric [bound]"` and `"The causal exponent clip is required only to avoid underflow."` | `:669`-`:671` | `[VERIFIED: pinn_architecture.md:668-671]` — see exact line-by-line breakdown below | **Correct, with a one-line nuance** |
| Phase-35 guard block (source precedence / deferred values) | `:692` | `[VERIFIED: pinn_architecture.md:692]` — `> **Phase 35 guard: source precedence and deferred values (LOSS-02 / LOSS-03 / LOSS-04; AC-LOSS-02 / AC-LOSS-03 / AC-LOSS-04).**` — exact match | **Correct** |
| §10.6 Held-Out Physics-Gate Aggregate Statistic | `:1064` | `[VERIFIED: pinn_architecture.md:1064]` — `### 10.6 Held-Out Physics-Gate Aggregate Statistic` — exact match | **Correct** |

**The one-line nuance:** the clip text actually reads, line by line:
```
668:  $\eta_c = 1$ default. Use `stopgrad` in weights by default. Clip the
669:  causal exponent to avoid underflow, but do not choose a numeric
670:  clipping bound in Phase 19; surface a gap if one is needed.
671:  The causal exponent clip is required only to avoid underflow.
```
The word "Clip the" (which opens the first quoted clause) is the last two words of line **668**, not 669 — the sentence spans 668-670. Line 671 (the second quoted sentence) is an exact, self-contained line. So `:669-671` is a very close but not maximally tight citation for the first sentence; `:668-671` is fully precise. This is a minor precision note, not an error that would mislead a reader to the wrong paragraph.

**Cross-check confirming REQUIREMENTS.md's anchors are genuinely stale** `[VERIFIED, this session]`: REQUIREMENTS.md:90 (SPEC-01) cites `pinn_architecture.md:424` for the η_c contract marker — line 424 of the live file is `- $\epsilon_{train} = 10^{-5}$ (\`10^-5\`) : Training-time Plummer softening parameter to prevent`, unrelated content. REQUIREMENTS.md's implicit `:167` for the `first_omega_0` fixed-at-30 sentence — line 167 of the live file is `cause the distribution of activations to either collapse to zero or`, unrelated. SPEC-06's `:433`/`:440` for `n_col`/"recommended" — line 433 is blank, line 440 is the `L_phys^causal` total-loss display-math line, neither is the `n_col` text. **All three stale anchors are confirmed to point at unrelated content in the live tree**, corroborating CONTEXT.md's Open Item 5 and DISCUSSION-LOG.md's "Incidental finding" with independent evidence gathered this session (not merely re-stating CONTEXT.md's own claim).

**Conclusion for the planner:** CONTEXT.md's Canonical References anchors are safe to use directly for any task that must cite `pinn_architecture.md`. Do not use the line numbers printed in `.planning/REQUIREMENTS.md` or `.planning/ROADMAP.md` for this file — both are confirmed stale as of the current tree (post-Phase-53).

## Finding 8 — Existing state on disk (verified this session)

| Path | Exists? | Verified |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/` | **No** | `ls` returned "No such file or directory" |
| `.planning/milestones/v2.3-GAPS.md` | **No** | `ls` returned "No such file or directory" |
| `.planning/phases/54-recalibration-decision-grounding/54-GAPS.md` | **No** | `ls` returned "No such file or directory" |
| `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/` (naming-convention precedent) | Yes | `ls -d` succeeded |
| `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/` and its 5 files (`DELIVERY-NOTE.md`, `specs/framework-specs-bundle.md`, `research_results/{.gitkeep, trainex-r2-research-report.md}`, `research_package/{44-DIAGNOSIS.md, run-evidence-bundle.md, CLAIMS-REGISTER.md, RESEARCH-CONTEXT-MASTER.md, RESEARCH-AGENT-PROMPT.md}`) | Yes | `find -type f` listing, this session |
| `docs/work/reviews/milestone_v2.1/45-trainex-r2-erw-package-assembly/2026-07-24-trainex-r2-report-factw-verification.md` (Rule-19 worked example) | Yes (12,714 bytes) | `ls -la` |
| `.planning/phases/54-recalibration-decision-grounding/54-CONTEXT.md`, `54-DISCUSSION-LOG.md` | Yes | Read this session |
| `.planning/phases/54-recalibration-decision-grounding/54-RULING.md`, `54-VALIDATION.md`, plan files | No — none yet exist; this is a fresh phase directory (only the two files above) | `ls -la` of the phase directory returned exactly these two files |

Since `trainex-r3/`, `v2.3-GAPS.md`, and `54-GAPS.md` do not exist, every plan task that creates them is a genuine creation task (no merge/patch logic needed), and D-10's "standing trigger" for `v2.3-GAPS.md` is confirmed live — the plan must include the file's creation, not assume it already exists from an earlier phase.

## Architecture Patterns

### System flow (governance pipeline, not a software architecture)

```
[Source-evidence tier]                    [Packet-assembly tier]                [Gate / owner-decision tier]
2026-08-17 audit ────────┐
52-VER-20-ROUTING-       │   file:line citations    RESEARCH-CONTEXT-MASTER.md   54-RULING.md (D-09, if
HANDOFF.md item (e) ─────┼──────────────────────►   (§0 premise-qual, mechanism, ─┐  owner rules directly)
trainex-r2 §7 clause 3 ──┤   D-06 inline tags        remedy surfaces w/ D-05      │
(premise-qualified,      │                           no-menu form, "what          │  OR
NOT authoritative) ──────┘                           evidence cannot answer",     │
                                                       D-04 self-audit) ───────────┼─► 54-GAPS.md / v2.3-GAPS.md
pinn/loss_catalog.py,                                        │                    │  (D-10 anchor gap,
pinn/train.py,                     mechanism-only             │  DELIVERY-NOTE.md │   OPEN until checkpoint ②)
pinn_architecture.md ───────────►  (coupling arithmetic,       │  (D-08 gate stub,
(code + spec, read-only)           clip location)              │   routing only) ──► Owner reads packet at
                                                                │                     checkpoint ① → branch:
                                                                └────────────────────►  rule directly (→ 54-RULING.md)
                                                                                        OR commission trainex-r3
                                                                                        (→ ERW-02 replan, D-11)
```

The primary use case traced end to end: an owner opens `RESEARCH-CONTEXT-MASTER.md` at the gate; every fact in it traces back to an already-published, already-cited source document (never to agent inference); the packet frames but does not narrow the remedy surfaces; the owner's branch choice at checkpoint ① routes either to a same-phase `54-RULING.md` (direct ruling) or to a deferred ERW-02 replan (commission) — no path in this diagram lets the packet-assembly tier reach a value pick on its own.

### Recommended Project Structure (ERW-01 scope only — per D-02, this is deliberately incomplete)

```
pinn_instruction/markdown_conversion/framework-specs/trainex-r3/
├── DELIVERY-NOTE.md                          # NEW — Finding 2 shape, adapted for D-08/D-09 pointers
└── research_package/
    └── RESEARCH-CONTEXT-MASTER.md            # NEW — Finding 1 skeleton + D-03's two v2.3 sections + D-04 self-audit

# Deliberately ABSENT until ERW-02 (D-02 — the absence IS the branch-neutrality proof):
#   research_package/RESEARCH-AGENT-PROMPT.md
#   specs/  (snapshot bundle)
#   research_results/

.planning/phases/54-recalibration-decision-grounding/
├── 54-CONTEXT.md              # exists already
├── 54-DISCUSSION-LOG.md       # exists already
├── 54-GAPS.md                 # NEW — D-10 anchor gap entry
├── 54-RULING.md               # NEW, populated ONLY if owner rules directly at checkpoint ① (D-09)
└── (plan/summary files per planner's wave decomposition)

.planning/milestones/
└── v2.3-GAPS.md                # NEW — D-10 standing trigger; first v2.3 gap entry
```

### Pattern: greppable neutrality markers over prose promises (Phase 53 precedent, directly reusable)

Phase 53's `53-VALIDATION.md` (the immediately-prior, same-milestone phase, also a pure Markdown-editing phase) established the exact mechanical-check idiom this phase should reuse:

```
| Task ID | ... | Automated Command |
|---------|-----|--------------------|
| 53-01-05 | ... | `git diff -U0 -- pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md | grep -E '^[+-]' | grep -E 'eta_c|first_omega_0|underflow'` → **empty** |
```
`[VERIFIED: .planning/phases/53-narrow-spec-codification/53-VALIDATION.md:49]` — a negative-diff assertion proving no contract-marked value changed. Phase 54's analog (mechanics only): a negative-diff assertion over `pinn_architecture.md` and `pinn/` proving **nothing was edited in either** during ERW-01 (both are cited-but-read-only per D-03's Route-B read-only bars and per this phase's own scope — no framework spec file is opened for editing in Phase 54).

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Packet section structure | A fresh outline optimized for "what reads best at a gate" | Mirror trainex-r2's 7-section skeleton exactly (Finding 1), per D-03 | A commissioned r3 then needs no restructuring; a reader who has seen r2 navigates r3 immediately (CONTEXT.md's own stated reason). |
| Neutrality-enforcement wording | Ad hoc "we promise this is neutral" prose | The two-layer scoped-lexical-ban + explicit-§7-carve-out pattern (D-04), using ERW Rule 7's own vocabulary for the carve-out | Roadmap SC-1 requires verification **by inspection** — an unstated criterion is unauditable; Rule 7's existing vocabulary is what the carve-out must match against, not a paraphrase of it. |
| Package audit checklist | A new audit shape from scratch | Extend `45-AUDIT.md`'s ten-check structure (Finding 4) with the D-04 neutrality-by-inspection additions | 45-AUDIT.md is an already-PASSed, already-battle-tested check library for this exact artifact type (ERW master + delivery note); reinventing it risks missing a check category (e.g., pin consistency, drift check) that has already caused problems once. |
| Mechanical verification tooling | A pytest-style test suite for the Markdown packet | Shell (`grep`/`diff`/`git diff`/`shasum`) assertions in the `53-VALIDATION.md` / `45-AUDIT.md` style | This project's established pattern for Markdown-only phases is shell-based structural assertions, not a code test framework — introducing pytest here would be inconsistent with the immediately-prior sibling phase and would test nothing pytest is suited for (there is no code under test). |
| trainex-r2 citation qualification | Restating the premise-qualification paragraph at every citation site, or a single unlinked footnote | D-06's block-plus-short-inline-tag pattern, checked by a "no bare `trainex-r2` mention" grep | Roadmap SC-2 requires qualification to "travel with" every citation; a repeated paragraph is unreadable, a distant footnote is missable, and only the tag pattern is grep-checkable. |

**Key insight:** every "don't hand-roll" item in this phase is really the same insight restated: **this project already ran this exact kind of phase once (Phase 45) and audited it to PASS.** The correct default is "what did Phase 45 do, and does D-01..D-11 change it" — never "what would a well-structured decision document look like in the abstract."

## Common Pitfalls

### Pitfall 1: Citing the wrong document for the step-501 halt fact
**What goes wrong:** A task instructs "transcribe D-07's five mechanism facts, citing the 2026-08-17 audit," and the executor writes a citation to that audit for "front_idx = 0 at step 501" — which is not literally in that document (Finding 5).
**Why it happens:** CONTEXT.md's own D-07 prose lists all five facts together in one sentence without breaking out per-fact citations, and the research-focus brief that seeded this research made the same assumption.
**How to avoid:** Cite `52-DIAG-05-REDERIVATION.md:58` or `50-03-SUMMARY.md:84` specifically for the step-501 HALT fact; keep the audit document as the citation for the other four D-07 facts.
**Warning signs:** A `grep` for the cited number against the cited file returns nothing — exactly the check that surfaced this pitfall.

### Pitfall 2: A per-surface menu reads as a ranking even without ranking words
**What goes wrong:** A remedy-surface section lists candidate values or forms for `η_c`/`R̄` normalization/`ω₀`/`N_t`/the clip "for completeness," believing that omitting words like "recommend" or "best" keeps it neutral.
**Why it happens:** Structuring information as a list of options is a natural drafting instinct, and the lexical-ban layer (D-04 Layer 1) does not catch it — the words are clean, but the structure itself is the violation (D-05).
**How to avoid:** Each surface states only: the quantity, where it's specified (`file:line`), its contract marker (if any), what it's mechanically coupled to, and what the evidence pins/doesn't pin. No "the choices are..." framing anywhere in §0–§6.
**Warning signs:** Any sentence in the mechanism/remedy-surfaces sections that could be read aloud as "you could do A, B, or C."

### Pitfall 3: Treating `pinn/` as a grounding source rather than "the divergence being disposed of"
**What goes wrong:** Citing `pinn/loss_catalog.py` or `pinn/train.py` as authoritative evidence for what the *spec* should say, rather than as the *current, possibly-to-be-amended* implementation.
**Why it happens:** The coupling arithmetic (Finding 6) is genuinely in `pinn/`, and it's tempting to treat "what the code does" as settled truth the same way the locked spec sections are.
**How to avoid:** CONTEXT.md's own Canonical References make this explicit: *"Note: `pinn/` is **not** a grounding source for spec decisions; it is cited here as the divergence being disposed of, per SPEC-06's own text."* Cite `pinn/` only to state the current numeric divergence (`collocation_count = 16` vs. `n_col = 4096`), never as authority for what either number *should* be.
**Warning signs:** A sentence that treats a `pinn/` value as if it were spec-locked in the SCOPE-38 sense (only `pinn_architecture.md` contract markers carry that status).

### Pitfall 4: Assuming the attachment cap applies to ERW-01's files
**What goes wrong:** Applying Rule 15's 5-attachment cap logic to files created in this phase, when ERW-01 uploads nothing (no external agent is engaged this pass — D-02 withholds the prompt).
**Why it happens:** The cap is heavily discussed in the r2 precedent and the runbook, making it feel load-bearing everywhere.
**How to avoid:** The cap becomes relevant only once ERW-02 authors `RESEARCH-AGENT-PROMPT.md` and the `specs/` bundle (branch-conditional, out of this phase's scope per D-11). ERW-01's plan should not budget or reason about attachment counts.
**Warning signs:** A Phase 54 task referencing "the 5-attachment cap" for artifacts this phase actually creates.

### Pitfall 5: Reading D-01/D-02's `trainex-r3/` creation as presuming the branch
**What goes wrong:** A reviewer (human or agent) flags the mere existence of `trainex-r3/research_package/RESEARCH-CONTEXT-MASTER.md` before the gate as having "chosen Route B."
**Why it happens:** Creating the round-root directory looks, on its face, like commissioning the round.
**How to avoid:** The packet's own D-02 structural property is the answer: a round with no `RESEARCH-AGENT-PROMPT.md` and no `specs/` snapshots is, by the runbook's own Rule ("A package without its prompt is incomplete"), *not yet commissioned*. This is already flagged as **Open Item 1** for owner visibility in CONTEXT.md — the plan does not need to re-litigate it, only implement D-02's file-withholding faithfully.
**Warning signs:** A task that creates `RESEARCH-AGENT-PROMPT.md` or `specs/` during ERW-01 — this would be a direct D-02 violation, not merely a style issue.

## Code Examples

Verified patterns from the actual, on-disk precedent files (not synthesized):

### The D-06 premise-qualification anchor (quote this verbatim in the r3 packet)
```
Source: pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_package/RESEARCH-CONTEXT-MASTER.md:319-320 (§7, clause 3)

3. **Do not recommend a remedy.** Remedy adjudication is owner-governed
   downstream. Your answers inform that decision; they do not make it.
```

### Frontmatter shape to extend (r2 base + D-03's `access_mode` addition)
```yaml
Source: pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_package/RESEARCH-CONTEXT-MASTER.md:1-9 (base keys, Route A)
---
title: Trainex R2 Research Context Master — Stage-0 Physics-Gate Training-Recipe Questions
package_for: trainex-r2 (single sub-package)
role: the external research agent's single entry point — orientation, manifest, source tiering, five neutrally framed questions, claims register, provenance, and the neutral output contract
status: active
created: 2026-07-24
source_baseline: 9b1f0e7a4735df1c54867530cfd1f13b390e1514
self_contained: true
---
```
Per D-03/Rule 16, the r3 master's frontmatter must additionally declare `access_mode: open-book`.

### The causal-weight exclusive-prefix-sum mechanism (cite, do not reproduce as an editable spec — it is `pinn/`, not grounding, per Pitfall 3)
```python
Source: pinn/loss_catalog.py:326-342

    eta = torch.as_tensor(eta_c, dtype=dtype, device=device)
    # Prefix sum of stopgrad(Rbar) for the STRICTLY preceding points.
    # cumsum_excl[0] = 0; cumsum_excl[n] = sum_{m<n} Rbar_m.detach()
    detached = rbar.detach()
    cumsum = torch.cumsum(detached, dim=0)
    # Shift right by one: exclusive prefix.
    zeros = torch.zeros(1, dtype=dtype, device=device)
    cumsum_excl = torch.cat([zeros, cumsum[:-1]], dim=0)
    clip_facts = resolve_causal_clip_facts(dtype, device)
    exponent = -eta * cumsum_excl
    floor = torch.as_tensor(
        clip_facts["causal_clip_exponent_floor"], dtype=dtype, device=device,
    )
    weights = torch.exp(torch.clamp_min(exponent, floor))
    # w_1 is identically 1 by construction (cumsum_excl[0] = 0); pin via constant.
    _ = CAUSAL_W1
    loss = (weights * rbar).mean()
```

### The Phase 53 negative-diff scope guard (directly reusable pattern for Phase 54's own boundary attestation)
```
Source: .planning/phases/53-narrow-spec-codification/53-VALIDATION.md:49

git diff -U0 -- pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md | grep -E '^[+-]' | grep -E 'eta_c|first_omega_0|underflow'
→ expected: empty
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|---------------|--------|
| ERW packages assumed closed-book (Route A) — "you have no codebase access" | Two declared access modes; Route B (open-book) is the **default** whenever a question references a project artifact | 2026-07-24, after the trainex-r2 lesson `[VERIFIED: docs/runbooks/external-research/2026-06-11-external-research-workflow.md:25-27, 47-83]` | Directly relevant here: Phase 54's own packet is Route B by roadmap SC-4 fiat (not a fresh choice — "transcribed, not selected," per D-03), and its master must carry the Route-B-only premise-challenge mandate, read-only bars, and repo-derived evidence label that a Route-A master would omit. |
| No attachment limit on ERW packages | Hard cap of 5 uploaded attachments per sub-package; bundle, don't split | 2026-07-07 `[VERIFIED: docs/runbooks/external-research/2026-06-11-external-research-workflow.md:189-202, Rule 15]` | Not load-bearing for ERW-01 itself (no upload happens this pass), but will bind ERW-02 if `trainex-r3` is commissioned. |
| Self-containment check ("zero repo-path markers") applied uniformly | Explicitly Route-A-only; does not apply to Route-B packages | 2026-07-24, alongside the access-mode split `[VERIFIED: trainex-r2/DELIVERY-NOTE.md:86-88]` — *"`45-AUDIT.md` Check 3 (zero repo-path markers in authored uploads) was a correct Route A check at the time it ran. It does not apply to a Route B package"* | If the D-04 self-audit / any Phase-54-closing audit reuses `45-AUDIT.md`'s Check 3 verbatim, it must be dropped or inverted for the r3 master, which is Route B from the start and is *expected* to carry repo paths per Rules 1-2's inversion. |

**Deprecated/outdated:** the "attached files only" sentence that closes r2's master (`...you have no codebase access`) is a Route-A-only sentence and must not appear in the r3 master (Finding 1, Finding 3).

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The planner will decompose ERW-01 into roughly a Phase-45-shaped sequence (skeleton/evidence → core master → routing/self-audit → owner checkpoint), adapted for D-02's prompt-withholding and D-04/D-08/D-09's additions. This is presented as a precedent, not a prescription — plan count and decomposition are explicitly Claude's Discretion per CONTEXT.md. | Finding 4, Architecture Patterns | Low — if the planner chooses a different decomposition, nothing in this research depends on the specific plan count; only the *content* findings (1, 2, 3, 5, 6, 7, 8) are load-bearing for correctness. |
| A2 | The D-04 self-audit section belongs *inside* `RESEARCH-CONTEXT-MASTER.md` itself (per CONTEXT.md's own phrasing, "Record both in a self-audit section inside the packet"), while the phase-closing package-wide audit (the Phase-45-style `45-AUDIT.md` analog) is a separate file. This split is inferred from CONTEXT.md's wording, not independently re-confirmed against a second source. | Finding 4, Don't Hand-Roll | Low-Medium — if the planner instead puts the self-audit as a wholly separate file, D-04's letter ("inside the packet") would not be honored; worth a one-line confirmation at plan-check time. |
| A3 | `54-RULING.md`'s exact internal shape (beyond D-09's field list: date, quoted instruction, branch, filled stub, file:line of amended contracts) has no existing precedent to mirror — Open Item 4 in CONTEXT.md itself confirms this ("not in any template or prior phase... rename freely"). This research did not invent a template for it, consistent with the neutrality bars (a ruling record's *shape* is assembly mechanics, but its population is entirely gated on an owner action that has not happened yet). | User Constraints (Open Item 4), Recommended Project Structure | Low — CONTEXT.md already flags this as freely renameable/shapeable; no downstream phase depends on a specific internal structure beyond the D-08 field list, which is fixed. |

**If this table is empty:** N/A — three low-risk assumptions are logged above; none touches a recalibration value, and all three are either explicitly delegated to the planner by CONTEXT.md or explicitly flagged as open by CONTEXT.md itself.

## Open Questions

1. **Does any other in-repo document besides `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` carry a stale `pinn_architecture.md` line-number citation that a Phase-54 or Phase-56 task might inherit?**
   - What we know: CONTEXT.md's DISCUSSION-LOG.md flags exactly four stale citations (REQUIREMENTS.md's `:424`, implicit `:167`, `:433`, `:440`), all independently re-confirmed stale this session (Finding 7). ROADMAP.md's Phase 56 detail block (line 122) also quotes `pinn_architecture.md:424` for the same η_c marker, inheriting the same staleness.
   - What's unclear: whether `53-UNSWEPT-INVENTORY.md`, `52-VER-20-ROUTING-HANDOFF.md`, or other cross-referenced documents carry their own independent stale citations not yet flagged.
   - Recommendation: out of scope for Phase 54 to fix (CONTEXT.md is explicit that editing REQUIREMENTS.md is out of this phase's scope), but the planner may want a task that greps for `pinn_architecture.md:` followed by a 3-digit number across `.planning/` as a cheap, mechanical pre-flight check before Phase 56 opens, so any newly-discovered stale anchor is caught before it causes a Phase-56 mis-edit. This is a suggestion about *process*, not about any recalibration content.

2. **Should the D-04 self-audit section reuse `45-AUDIT.md`'s exact ten-check numbering, or a renumbered subset?**
   - What we know: `45-AUDIT.md`'s Check 3 (self-containment) is explicitly Route-A-only and does not apply to r3 (State of the Art table above); several other checks (snapshot fidelity, pin consistency) presuppose a `specs/` snapshot bundle that D-02 withholds from ERW-01.
   - What's unclear: whether the planner should therefore write a *smaller* internal self-audit (only the checks that apply to a master + delivery note with no snapshots yet) and defer the full ten-check-style audit to ERW-02 when the snapshot bundle exists, or run a differently-scoped audit now.
   - Recommendation: this is a planning-mechanics choice within Claude's Discretion (CONTEXT.md explicitly delegates "exact section numbering and prose"); flagged here only so the planner is aware the two audits (r2's ten-check precedent vs. what's actually assertable this phase) are not a 1:1 match.

## Environment Availability

Not applicable. This phase makes no external tool, service, or runtime calls beyond the standard Unix utilities (`grep`, `diff`, `git`, `shasum`, `wc`) already used and confirmed working throughout Phase 45 and Phase 53's identical-genre phases, plus the `scripts/agent-commit` wrapper this repository's Git protocol requires for all commits (see Project Constraints below). No package installation, no network calls, no database, no new CLI dependency.

## Validation Architecture

Modeled directly on the immediately-prior, same-milestone, same-genre sibling phase's validation doc `[VERIFIED: .planning/phases/53-narrow-spec-codification/53-VALIDATION.md, read in full this session]`, which itself states: *"This phase's validation is **textual**, not runtime — the phase edits one framework-spec Markdown file and writes no code."* Phase 54's validation is one further step removed from code (it doesn't even edit the framework spec — it only cites it), so the same "textual, shell-assertion, no framework" pattern applies with an even lighter footprint.

### Test Framework

| Property | Value |
|----------|-------|
| Framework | none — grep/diff/file-existence shell assertions, per the Phase 45 (`45-AUDIT.md`) and Phase 53 (`53-VALIDATION.md`) precedent |
| Config file | none |
| Quick run command | per-task `grep -c`/`diff -q`/`ls`/`git diff --stat` assertions scoped to the file(s) that task's wave touched |
| Full suite command | the full `45-AUDIT.md`-style check battery, scoped to what ERW-01 actually creates this phase (see Open Question 2 re: which checks apply pre-snapshot) |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command (illustrative — planner fixes exact form) | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| ERW-01 | Packet uses the mirrored 7-section skeleton (Finding 1) | textual assertion | `grep -c '^## [1-7]\.'` against the master → 7 (or the D-03-extended count including §0 and the "cannot answer" section) | ✅ post-write |
| ERW-01 | No bare `trainex-r2` mention (D-06) | textual assertion | `grep -n 'trainex-r2' <master>` — every hit must also match the D-06 inline-tag pattern within the same line or immediate vicinity; a hit with no tag fails | ✅ post-write |
| ERW-01 | Lexical ban holds in §0–§6, carve-out holds in §7 (D-04) | scoped textual assertion | `sed -n '/^## §0/,/^## 7\./p' <master> \| grep -Eiv '^## 7\.' \| grep -Ei 'recommend\|suggest\|prefer\|best\|default to\|should use\|ranked\|leading option'` → empty | ✅ post-write |
| ERW-01 | Branch neutrality: prompt and `specs/` absent (D-02) | file-existence assertion | `! test -f research_package/RESEARCH-AGENT-PROMPT.md && ! test -d specs/` | ✅ post-write |
| ERW-01 | No framework-spec or `pinn/` file edited (read-only bar) | negative-diff assertion | `git diff --stat -- pinn_instruction/markdown_conversion/framework-specs/ pinn/` → empty | ✅ |
| ERW-01 | Every D-07 mechanism fact carries a correct `file:line` citation | manual + textual | grep each cited path for the quoted figure (as done in Finding 5 this session) — the "step 501" fact specifically must NOT cite the 2026-08-17 audit alone | ✅ (spot-checkable) |
| ERW-01 | Gate stub pre-declares the `N_t` completeness rule (D-08) | textual assertion | `grep -c 'does not dispose of' <gate stub>` ≥ 1; `grep -c` for a bare candidate-value table row (would indicate a menu, not a stub) → 0 | ✅ post-write |
| D-10 | `54-GAPS.md` and `.planning/milestones/v2.3-GAPS.md` both exist with the one anchor entry | file-existence + textual assertion | `test -f` both; `grep -c 'OPEN'` in each ≥ 1 | ✅ post-write |

### Sampling Rate

- **Per task commit:** the grep/diff/existence assertions scoped to that task's own edit (mirrors 53-VALIDATION.md's "After every task commit" row)
- **Per wave merge:** the full assertion set for everything touched in the wave
- **Phase gate (before checkpoint ① is presented):** every assertion above green, plus the D-04 self-audit section's own recorded result reviewed manually

### Wave 0 Gaps

None — existing shell tooling (`grep`, `diff`, `git`, standard Unix utilities) covers every mechanical check this phase needs; no fixtures, no framework install, no config file to write. This mirrors Phase 53's identical Wave-0 conclusion (*"Existing infrastructure covers all phase requirements — no test framework, fixtures, or config are introduced"*).

## Security Domain

This phase has no traditional application attack surface (no auth, no session, no network-facing input, no crypto, no user-supplied data at runtime) — it is Markdown document authoring. The one genuinely applicable concern is **content-provenance / instruction-injection hygiene** when citing an externally-authored document into a new document that will itself later be handed to another external agent:

### Applicable ASVS-adjacent categories

| Category (adapted) | Applies | Standard Control |
|---|---|---|
| V5 Input Validation (adapted: treat cited external content as data, not instructions) | Yes | The trainex-r2 research report (`trainex-r2-research-report.md`) is an externally-authored document that D-06 requires citing extensively. Per this project's own standing untrusted-input-boundary discipline (which this researcher session itself operates under), any content quoted from it into the r3 packet must be treated and presented as **data to cite**, never as an instruction to follow — the D-06 block-plus-tag pattern already achieves this by construction, since it quotes specific, bounded claims (the §7 clause 3 text, the absence list, the vintage) rather than importing the report wholesale. |
| Traditional ASVS categories (V2 Auth, V3 Session, V6 Crypto) | No | Not applicable — no code, no runtime, no user session exists in this phase's deliverable. |

### Known risk pattern for this phase's genre

| Pattern | Analogous STRIDE category | Standard Mitigation (already in place via D-01..D-11) |
|---|---|---|
| A second-order prompt-injection surface: if `trainex-r2-research-report.md` (external-agent-authored) contained any embedded adversarial instruction text, and the r3 packet quoted it verbatim without bounding, that text could propagate into whatever gets pasted to the *next* external agent under Route B. | Tampering (of the downstream agent's context) | D-06 already bounds every trainex-r2 citation to specific, named claims (the §7 clause-3 quote, the absence list, the vintage) rather than bulk-including the report; the master's own §7 output contract (once r3 is commissioned) additionally instructs the receiving agent per Rule 18's read-only bars. No task in this phase needs to add anything further — this is a confirmation that the existing D-06 design already avoids the pattern, not a new requirement. |

## Sources

### Primary (HIGH confidence — opened and read/grepped directly this session)
- `.planning/phases/54-recalibration-decision-grounding/54-CONTEXT.md` (499 lines, read in full)
- `.planning/phases/54-recalibration-decision-grounding/54-DISCUSSION-LOG.md` (265 lines, read in full)
- `.planning/REQUIREMENTS.md` (195 lines, read in full)
- `.planning/STATE.md` (lines 1-342 of 488, read)
- `.planning/ROADMAP.md` (171 lines, read in full)
- `.planning/config.json` (read in full)
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_package/RESEARCH-CONTEXT-MASTER.md` (331 lines, read in full)
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/DELIVERY-NOTE.md` (210 lines, read in full)
- `docs/runbooks/external-research/2026-06-11-external-research-workflow.md` (265 lines, read in full)
- `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md` (221 lines, read in full)
- `.planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-AUDIT.md` (207 lines, read in full)
- `.planning/milestones/v2.1-phases/45-trainex-r2-erw-package-assembly/45-{01,02,03,04}-SUMMARY.md` (all four, read in full)
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — targeted reads at offsets 165-304, 420-509, 655-704, 1055-1074 (all cited anchors independently verified)
- `pinn/loss_catalog.py` — grepped and read in full at lines 283-347
- `pinn/train.py` — read at lines 1025-1040
- `pinn/constants.py` — grepped for `CAUSAL_ETA_C`/`CAUSAL_W1`
- `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-DIAG-05-REDERIVATION.md` — grepped/read line 58 and surrounding
- `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md` — read in full (66 lines)
- `.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/{50-03-SUMMARY.md,50-08-SUMMARY.md,50-CONTEXT.md}` — grepped for "501"/"front_idx"
- `.planning/phases/53-narrow-spec-codification/53-VALIDATION.md` (83 lines, read in full)
- File-existence checks via `ls`/`find` for `trainex-r3/`, `v2.3-GAPS.md`, `54-GAPS.md`, `trainex-r1/`, the Rule-19 worked-example verification report, and the full `trainex-r2/` tree

### Secondary (MEDIUM confidence)
- None — every claim in this document traces to a primary source opened this session; no WebSearch or external documentation was needed (this is a pure in-repo governance/documentation phase with no external library or framework dependency).

### Tertiary (LOW confidence)
- None.

## Project Constraints (from CLAUDE.md)

Extracted directives that bind Phase 54's plan and execution:

- **STOP protocol applies.** REQUIREMENTS.md's own SCOPE-34 text invokes it explicitly ("The STOP protocol's semantic / MUST-surface class governs every sub-question"). Any decision Phase 54's execution encounters that is source-silent and semantic (touches `η_c`, `R̄` normalization, `ω₀`, `N_t`, or the clip) must STOP and route to the gap register — never be decided inline, "reasonable default" or not.
- **`pinn/` is not a grounding source** for spec decisions (v1.3-era-code directive, generalized) — reinforced specifically for this phase by CONTEXT.md's own note on the SPEC-06 divergence citation (Pitfall 3 above).
- **Git commit protocol:** all commits must go through `scripts/agent-commit` (never raw `git commit`), with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS` set; no blanket staging (`git add .`/`-A`/`-u`); commit messages follow `<type>(<scope>): <lowercase imperative subject>` — for this phase, type is most likely `docs` (packet/delivery-note authoring) or `plan`, scope `54`; a body is required for any commit touching `.planning/` or `pinn_instruction/` (which every commit in this phase will).
- **Docs placement + frontmatter rules apply** if ERW-02's later Rule-19 verification report is ever written (it lands under `docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/` per the Phase 45 precedent and CONTEXT.md's own Deferred Ideas) — out of this phase's scope but worth the planner noting for the eventual ERW-02 replan.
- **Never rewrite history, force-push, or run destructive git operations** without explicit approval and a recovery checkpoint — not expected to arise in this phase (pure file creation, no history rewrites).
- **Worktree awareness:** this research was conducted from `.worktrees/trainex` on branch `milestone/v2.3`, confirmed as the correct location per the repo's own CLAUDE.md routing note and `git status --short --branch` at session start.

## Metadata

**Confidence breakdown:**
- Structural facts (Findings 1-8): HIGH — every claim opened and verified directly this session with file:line citations; two corrections found and documented (step-501 citation, minor clip-line boundary).
- Architecture patterns / Don't Hand-Roll / Pitfalls: HIGH — derived entirely from verified precedent artifacts (Phase 45, Phase 53), not invented.
- Validation Architecture: HIGH — modeled directly on the immediately-prior sibling phase's own validation doc, same milestone, same document genre.
- Recalibration content itself: **N/A — out of scope by design (SCOPE-34).** This research contains zero claims, opinions, or leanings about `η_c`, `R̄` normalization, `ω₀`, `N_t`, or the clip's numeric semantics.

**Research date:** 2026-08-20
**Valid until:** Until `pinn_architecture.md`, `pinn/loss_catalog.py`, `pinn/train.py`, or `pinn/constants.py` are next edited (Phase 56 is the next scheduled edit to `pinn_architecture.md` — re-verify all Finding 7 anchors after Phase 56 lands, exactly as this session re-verified them after Phase 53). Until then, the file:line citations in this document are load-bearing and should be treated as current.
