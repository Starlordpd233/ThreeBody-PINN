# Phase 54: Recalibration Decision Grounding - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-08-19
**Phase:** 54-recalibration-decision-grounding
**Mode:** `--all` (all gray areas auto-selected) + owner-delegated resolution
**Areas discussed:** Packet location & branch neutrality, Packet structure, Non-recommendation enforcement, trainex-r2 premise qualification, Evidence depth, Gate presentation & ruling record, Gap-register bookkeeping, Decomposition & halt boundary

---

## Owner instruction governing this session

> *"you can automatically select the best option following your best judgement and
> reasoning, no need to ask the user for their input unless the choice is absolutely
> impactful and significant that must be made by the user."*

Applied to **assembly mechanics only**. SCOPE-34 reserves the recalibration content
itself to the owner, and the instruction's own carve-out points at that same class.
No question below names, defaults, ranks, or narrows a value of `η_c`, `R̄`
normalization, `ω₀`, `N_t`, or the clip semantics. Nothing was escalated as blocking;
five items were routed to **Open Items for Owner Visibility** in CONTEXT.md.

---

## Packet location and branch neutrality

| Option | Description | Selected |
|--------|-------------|----------|
| Round root in place | Author as `trainex-r3/research_package/RESEARCH-CONTEXT-MASTER.md` from the start | ✓ (D-01) |
| Build-then-promote | Author under `docs/work/designs/milestone_v2.3/54-.../`, `git mv` into `trainex-r3/` only if commissioned | |
| Phase-local | Author as `.planning/phases/54-.../54-DECISION-PACKET.md` | |

**Selected:** round root in place.
**Notes:** Three sources converge — `.claude/rules/repo-map.md` fixes the
`framework-specs/trainex-<id>/` home; ERW Rule 12 fixes the round name and Rule 14
makes the round root the durable record; ERW-01's own acceptance text says the packet
*"doubles as the `trainex-r3` `RESEARCH-CONTEXT-MASTER.md`… so neither gate branch
wastes work"*, which is only literally true if it is written as that file, there,
now. Build-then-promote reintroduces exactly the rework the requirement removes.

**Follow-up — the objection this raises, and how it was answered.** Creating
`trainex-r3/` before the gate could read as presuming the Route-B branch, which
SCOPE-34 forbids. Rather than answer with a disclaimer, D-02 answers with a
structural property: **ERW-01 ships the master and delivery note only**; the prompt
and `specs/` snapshots are withheld until the owner commissions the round. ERW's own
rule — *"A package without its prompt is incomplete"* — is used affirmatively, so the
missing prompt is the runbook-defined proof that no round exists yet. It also splits
the requirements cleanly: ERW-01 = master + note + gate; ERW-02 = everything that only
exists under Route B.

---

## Packet structure

| Option | Description | Selected |
|--------|-------------|----------|
| Mirror trainex-r2's master skeleton | §1 Orientation / §2 Manifest / §3 Source tiering / §4 Questions / §5 Claims register / §6 Provenance / §7 Output contract, plus Route-B additions and two v2.3 sections | ✓ (D-03) |
| Fresh structure for a gate document | Optimize purely for the owner's read at checkpoint ① | |
| Minimal master + separate gate brief | Two documents, one for the agent and one for the owner | |

**Selected:** mirror r2, extended.
**Notes:** A commissioned r3 then needs no restructuring, and a reader who has seen r2
navigates r3 immediately. Route-B additions are **transcribed from the runbook, not
chosen**: `access_mode: open-book` (Rule 16, and roadmap SC-4 already fixes the route);
the Rules 1–2 inversion (repo paths expected; the "attached files only" instruction
must *not* appear); the premise-challenge mandate as a duty with contradictions
reported up front (Rule 17, r2's "source-verification findings" section named as the
shape); the read-only bars in the imperative (Rule 18); `source_baseline` pin (Rule 5)
in the master with the Rule-20 live-tree pin deferred to the delivery note at ERW-02,
since it records the tree the agent actually saw. Two v2.3-specific sections added:
the §0 premise-qualification block, and a dedicated *"what the assembled evidence
cannot answer"* section required by ERW-01's *"it names its own gaps"*.

---

## Making "non-recommending" verifiable by inspection

| Option | Description | Selected |
|--------|-------------|----------|
| Scoped lexical ban + explicit §7 carve-out + self-audit section | Prohibition binds §1–§6; §7 must use Rule-7 vocabulary; both recorded in-packet | ✓ (D-04) |
| Prose assertion only | State that the packet is non-recommending and rely on careful drafting | |
| Unscoped banned-word sweep | Ban the vocabulary everywhere in the file | |

**Selected:** two-layer, scoped.
**Notes:** Roadmap SC-1 requires that *"a reader can verify **by inspection**"* — which
needs a stated criterion, or two readers disagree. The unscoped sweep is actively
wrong: ERW Rule 7 **requires** trainex-r3 to produce *"suggested default clearly
marked"*, door-type classification, and a decision sheet, and SC-4 requires the packet
to specify that contract. Read naively, SC-1 and Rule 7 contradict. They do not — **the
prohibition binds the packet's own voice, never its specification of the external
agent's deliverable.** Naming that boundary is what stops a later audit from either
flagging §7 as a violation or gutting the Rule-7 contract to pass a grep. Same
reasoning as Phase 53's D-02: pick the form a mechanical check can actually assert,
then name its scope.

**Follow-up — the structural failure mode (D-05).** A packet listing "for `η_c`: A, B,
C" has already done the framing work that produces a ranking, even with every
recommendation word stripped. A menu of comparable options *is* the ranking substrate,
and Rule 7 assigns menu construction to the commissioned round or the ruling to the
owner. So each surface states what the quantity is, where it is specified, what
contract marker it carries, what it is coupled to, and what the evidence does and does
not pin — never "the choices are…". The one coupling made unmissable is `η_c` ↔
`N_t`/`n_col` (`w_n` is an exclusive prefix sum, verified at `pinn/loss_catalog.py:328`–`:331`;
`collocation_count = 16` at `pinn/train.py:1033` vs §3.2's `n_col = 4096` ⇒ ~256×).
Stating a coupling is mechanism, not recommendation.

---

## trainex-r2 premise qualification

| Option | Description | Selected |
|--------|-------------|----------|
| Full block + greppable inline tag at every citation | One qualification block; every `trainex-r2` mention carries a short bracketed tag pointing at it | ✓ (D-06) |
| Single block, cited once | One qualification section near the top | |
| Full paragraph repeated at each citation | Maximum locality | |

**Selected:** block + inline tag.
**Notes:** SC-2 requires the qualification to *"travel with"* every citation. Repeating
a paragraph is unreadable; a single distant block is missable. The tag satisfies
"travels with" while letting a check assert **no bare `trainex-r2` mention exists** —
the same greppability argument as Phase 53's D-02. Block contents fixed: r2's §7
clause 3 verbatim (*"Do not recommend a remedy. Remedy adjudication is owner-governed
downstream…"*, located at `trainex-r2/research_package/RESEARCH-CONTEXT-MASTER.md`);
the consequent absence list (no decision sheet, no options menu, no suggested defaults,
no door classification); and the vintage (packaged 2026-07-24, delivered 2026-07-25 —
predating the v2.2 conformance repairs). Q3's standing stated precisely: it derived the
`ω₀=30` mechanism **as a hypothesis**, since confirmed; it does not contain the answer.

---

## Evidence depth

| Option | Description | Selected |
|--------|-------------|----------|
| Inline transcription with `file:line` citations | Reproduce the six-row table and the numeric chain in the packet | ✓ (D-07) |
| Citation-only | Point at the audit; Route B lets the agent read it | |

**Selected:** inline with citations.
**Notes:** SC-1 requires the packet to **state** the mechanism, and the owner reads it
at the gate as a standalone document — "see the audit" moves the work rather than doing
it. Open-book access is not a licence to thin the packet; the runbook is explicit that
*"the repository is an additional evidence source, not a replacement for the package."*
Minimum inline content fixed: the 2026-08-17 audit's six-row seed/IC table; the chain
`first_omega_0 = 30` → second derivative `O(10⁵)` → `R̄ ≈ 10¹⁰`; the float32 underflow
bound `R̄ > 87.3`; 15 of 16 collocation weights on the floor; `front_idx = 0` at step
501 — each cited so every number stays re-derivable and Rule-19-checkable.

---

## Gate presentation and ruling record

| Option | Description | Selected |
|--------|-------------|----------|
| Structured decision-record stub with the `N_t` rule pre-declared | Owner fills branch + one line per surface + SCOPE-38 re-ratification lines | ✓ (D-08) |
| Free-text ask | Present the packet and ask for a ruling | |
| Stub with candidate values pre-filled | Faster for the owner | ✗ — SCOPE-34 violation |

**Selected:** structured stub, empty of candidates.
**Notes:** It is a form, not a menu. The stub states up front that **a ruling which
does not dispose of `N_t` is incomplete and routes back as a gap, never completed by an
agent choice** — transcribed from roadmap SC-5 and SPEC-06's joint-ratification
requirement. Putting it *in the stub* converts it from a post-hoc rejection into a
visible requirement at the moment of ruling.

**Follow-up (D-09).** The branch and any direct ruling land in a dedicated
`54-RULING.md` with provenance — date, the owner instruction quoted as data, the branch
taken, the filled stub, and the `file:line` of every contract amended. Not in the gap
register: a ruling is not a gap. The delivery note points at it so the round root stays
the durable record. Phase 56 reads it as its authorizing source.

---

## Gap-register bookkeeping

| Option | Description | Selected |
|--------|-------------|----------|
| One anchor gap covering checkpoints ①/② | Points at the packet as the surfacing instrument | ✓ (D-10) |
| One gap per recalibration sub-question | Literal reading of *"every recalibration sub-question is MUST-surface"* | |
| No gap entry | The packet is the record | |

**Selected:** one anchor, flagged to the owner.
**Notes:** The exhaustive reading would duplicate the packet into two registers and make
all three unreadable. The coherent reading is that **the packet is the surfacing
instrument** — that is what ERW-01 exists to be — with one anchor entry naming the
decision, classifying it `semantic`, and pointing at the packet's "what the evidence
cannot answer" section as the enumeration. Anchor stays `OPEN` until checkpoint ② is
discharged. This creates `.planning/milestones/v2.3-GAPS.md` (standing trigger; first
v2.3 gap). Any **new** source-silent question found during assembly and not covered by
the packet's scope gets its own full record. Routed as **Open Item 2** — it is a
bookkeeping-granularity call and the owner may prefer the exhaustive form.

---

## Decomposition and the halt boundary

| Option | Description | Selected |
|--------|-------------|----------|
| Plan ERW-01 + gate, stop; ERW-02 is a post-gate replan | No branch plan written | ✓ (D-11) |
| Plan both branches now | Neither branch waits on planning | |
| Plan the likelier branch | Fastest path | ✗ — SCOPE-34 violation |

**Selected:** stop at the gate.
**Notes:** Roadmap SC-3 — *"no work proceeds past the gate on an assumed branch"* —
and authoring a plan for either branch is work proceeding on an assumption. Concretely:
execution ends with the packet committed and the gate presented; STATE shows Phase 54
**in progress, not complete**; Phase 56 stays closed. Permitted and useful: a purely
factual branch-routing note listing which artifacts each branch would require (file
lists and ERW rule references). Not permitted: effort estimates, timelines, or
difficulty comparisons — cost framing at a gate is steering.

---

## Cross-referenced todos

| Todo | Score | Disposition |
|---|---|---|
| `d-06-static-epsilon-sensitivity-check.md` | 0.6 | **Not folded** — matched the literal string "D-06", which in this milestone is the *DIAG-06 verdict* (Phase 58), not the v1.6 Phase-32 epsilon-strategy decision the todo concerns. |
| `trainex-r1-research-handoff.md` | 0.6 | **Not folded** — matched "trainex"/"research". Concerns the r1a/r1b sub-package handoff, dated 2026-06-11; r1 was delivered and r2 shipped after it, so it is stale as well as out of scope. |

Both are keyword false positives. `--auto` would have folded them (score ≥ 0.4);
both were rejected on inspection and recorded in CONTEXT.md's Reviewed Todos.

---

## Incidental finding (not a gray area)

While verifying canonical refs, the `pinn_architecture.md` line numbers quoted inside
`.planning/REQUIREMENTS.md` (SPEC-01, SPEC-06) and `.planning/ROADMAP.md` were found
**stale** — they were written 2026-08-18 and Phase 53's three `spec(53)` commits
shifted the file on 2026-08-19. SPEC-01's `:424` (the `η_c` contract marker it must
name as superseded) is now `:445`; SPEC-06's `:433`/`:440` are now `:454`/`:461`;
`first_omega_0`'s `:167` is now `:181`; §2.4's `:253` is now `:267`. Corrected anchors
are in CONTEXT.md's Canonical References; the drift is routed as **Open Item 5**
because it is a live trap for Phase 56's SCOPE-38 amendment. Not fixed here — editing
`REQUIREMENTS.md` is outside Phase 54's scope.

---

## Claude's Discretion

Delegated onward to planner/executor; none changes a ratified quantity or the
neutrality of the packet:

- Plan count and task decomposition within ERW-01 scope (Phase 45, the direct
  precedent, used four plans for a comparable assembly).
- Commit granularity within `scripts/agent-commit` discipline.
- Exact section numbering and prose, provided every citation carries its `file:line`,
  every `trainex-r2` mention carries its D-06 tag, and the D-04 self-audit is present.
- Whether "what the evidence cannot answer" is a top-level section or a subsection of
  the claims register — provided it is findable by heading.

## Deferred Ideas

- The `trainex-r3` prompt, `specs/` bundle, and Rule-20 tree pin — ERW-02,
  branch-conditional; withheld deliberately by D-02.
- The Rule-19 per-claim in-repo verification report — Route B only; lands under
  `docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/`.
- The consolidated `trainex-r3-resolution-doc.md` and its decision sheet — Route B only.
- The SPEC-01 / SPEC-06 framework-spec amendment — Phase 56.
- Reconciling §2.4's "Recommended Value" header for `first_omega_0` — already routed to
  Phase 56 by Phase 53's unswept inventory.
- Multi-AI fan-out for r3 (ERW Rules 10–11 consolidation join points) — arises only if
  the round is commissioned.
