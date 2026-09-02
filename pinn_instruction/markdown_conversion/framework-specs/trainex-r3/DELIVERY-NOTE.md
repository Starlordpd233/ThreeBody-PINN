---
title: Trainex R3 Delivery Note (single sub-package)
package_for: trainex-r3 (single sub-package)
role: user-facing handoff and routing instructions — NOT part of any upload to external agents
status: active
created: 2026-08-20
access_mode: open-book
---

# Trainex R3 Delivery Note

**This file stays in the repository. Do NOT send it to external research agents.**

## Status: COMMISSIONED (checkpoint ①, 2026-08-21)

The owner selected **commission `trainex-r3`** at checkpoint ① on 2026-08-21. The ruling record is `.planning/phases/54-recalibration-decision-grounding/54-RULING.md`. Checkpoint ② — the recalibration ratification — remains open; this round exists to inform it.

Package root: `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/`.

## Handoff — what to attach, what to paste

Open `research_package/RESEARCH-AGENT-PROMPT.md`. Everything above its horizontal rule is routing for you; everything below it is the prompt to paste.

**Attach these three files individually** (no folders) — ERW Rule 15 caps a sub-package at five, and this round ships three:

| # | Attachment | What it is |
|---|---|---|
| 1 | `research_package/RESEARCH-CONTEXT-MASTER.md` | The agent's entry point: source tiering, the mechanism, the five decision surfaces plus item (e)'s fourth remedy family, the framed questions, the claims register, the gaps, the output contract. |
| 2 | `specs/framework-specs-bundle.md` | Verbatim locked framework-spec excerpts (10 extraction blocks, byte-verified against the pinned commit). |
| 3 | `research_package/v2.2-closure-evidence-bundle.md` | The 2026-08-17 conformance audit, the VER-20 routing handoff, and the DIAG-05 re-derivation — each reproduced in full. |

Not uploaded: this delivery note (routing only), the prompt (pasted, not attached), and `research_results/` (created at delivery).

**Fan out across several external agents.** Save each as `research_results/<agent>-resolution.md`.

## Rule-20 live-tree pin — stamped per engagement

**Restructuring note — 2026-09-02, by plan `54-08`.** This table was restructured after
delivery. Before the restructure it was a **single** five-row field table (`Worktree`,
`Branch`, `Commit at engagement`, `Access granted by`, `Date of engagement`) whose commit
cell held the short hash `11b4e0c1` with the annotation "the ERW-02 assembly commit, which
is the state of the tree as this package was completed. **Re-stamp with the actual `git
rev-parse HEAD` if the branch has moved before you grant access.**", and whose last two
cells were unfilled markers awaiting the owner. The branch had moved, so the commit cell is
re-derived below rather than copied; the short hash is retained only as a reading aid and
is nowhere used as the pin.

The single-row shape is replaced by **one block per returned report**. ERW Rule 20 pins
*the tree the agent saw*; two agents saw different things, and a single-row pin would
assert that both saw the same tree, which is false. It would also make the closed-book
report's anchors look re-derivable against a tree it never read.

Writing this record here costs no pin fidelity, because **this file is never uploaded**:
the ERW runbook's "Files every package round creates" lists `DELIVERY-NOTE.md` as
"user-facing routing — NEVER uploaded"
(`docs/runbooks/external-research/2026-06-11-external-research-workflow.md:100`), and Rule
15 repeats it — "Files that are never uploaded to the agent — `DELIVERY-NOTE.md` (user-only
routing), `research_results/` (created at delivery) … are routing / provenance / outputs"
(`…:193`–`:195`). Nothing learned after delivery is written back into a file the external
agents read (D-15); it lands here, or in
`.planning/phases/54-recalibration-decision-grounding/54-INTAKE.md`.

### The commit, re-derived

| Field | Value |
|---|---|
| Branch tip when the reports arrived, at full length | `efe8e590d6c6b2a77cc92abb0b93d625e2b92c49` |
| Author date | `2026-08-28T13:18:33+08:00` |
| Subject | `docs(54-07): certify trainex-r3 handoff readiness and halt` |
| Short form (reading aid only — **not** the pin) | `efe8e590` |
| Commits landing between that tip and the reports' arrival | none — `git rev-list efe8e590d6c6b2a77cc92abb0b93d625e2b92c49..HEAD --before='2026-08-30T23:59:59Z'` returns **empty output**, made explicit here rather than left as a silent absence. The next commit on the branch is `9f1ad245…` (2026-08-31), after both reports had landed |

**Arrival date, and which evidence it rests on.** Two sources are available and they are
not the same thing. The open-book report records its own authoring date in its frontmatter
(`claude-resolution.md:5` — `created: 2026-08-30`) and its own reading date at `:7`
(`read-only, 2026-08-30`); the closed-book report carries no frontmatter and no
self-recorded date at all. The file modification times in this worktree are
`claude-resolution.md` 2026-08-30T10:28:01Z and `chatgpt-resolution.md`
2026-08-30T14:35:44Z (`date -u -r <file>`). **The modification times are what this stamp
relies on**, for two reasons: they are the only per-file arrival evidence that exists for
*both* reports, and the pin needs the moment the reports landed *in this tree* relative to
the branch, which is what a modification time records and what an authoring date does not.
The open-book report's self-recorded date corroborates them to the day.

### Engagement 1 — the open-book report

| Field | Value |
|---|---|
| Report file | `research_results/claude-resolution.md` |
| Worktree | `<home>/Desktop/3_body_problem/.worktrees/trainex` — recorded by the report itself at `claude-resolution.md:7` |
| Branch | `milestone/v2.3` |
| Commit at engagement | `LIVE-TREE-PIN=efe8e590d6c6b2a77cc92abb0b93d625e2b92c49` |
| How access was granted | read-only mount of the worktree. The report records the mount at `:7` and records at `G-10` (`:847`–`:851`) that the mount's `.git` file points outside it, so repository-level git metadata was unreachable and the agent could record no tree hash of its own. This stamp discharges that report's own instruction: "a Rule 20 pin should be attached by someone with repository-level git access before this report is filed" |
| Date of engagement | 2026-08-30 |

### Engagement 2 — the closed-book report

| Field | Value |
|---|---|
| Report file | `research_results/chatgpt-resolution.md` |
| Worktree | **not applicable** — the report states at `:7` that it worked "from the attachments and published literature without live repository verification", and at `:596` that "Repository inspection was waived" |
| Branch | **not applicable** — same reason: no tree was read, so no branch was seen |
| Commit at engagement | **no live-tree pin exists for this engagement**, and none may be invented for it. Its only baseline is the attachment baseline: `ATTACHMENT-BASELINE-PIN=6a4f9b9902ab62e1d1f57bba0e521f38120c416d` |
| How access was granted | attachments only, under a revised access instruction from the owner. The report declares this in its own third paragraph at `:7` |
| Date of engagement | 2026-08-30 |

Both markers are written by name rather than by position, because both values are real
commits and a check that selected "the first commit-typed hash in the file" would attest
whichever block happened to be written first — and would report the attachment baseline as
a Rule-20 live-tree pin. The two values differ, which is the distinction Rule 20 exists to
record: `source_baseline` pins the snapshots, the live-tree pin pins the tree.

### Identity of the pinned tree and the verifying tree — `PIN-TREE-IDENTICAL`

The **citable-path set** — the closed list of repository paths either report cites — was
extracted from the two reports and is recorded, with its derivation and its resolved
abbreviations, in
`.planning/phases/54-recalibration-decision-grounding/54-INTAKE.md` under the marker that
later checks paste verbatim. It holds **21** paths.

| Check | Command | Output |
|---|---|---|
| Pinned commit versus current tip, over the citable-path set | `git diff --stat efe8e590d6c6b2a77cc92abb0b93d625e2b92c49 HEAD -- $(cat <the recorded set>)` | empty — `PIN-TREE-IDENTICAL` |
| Working tree versus index and HEAD, over the same set | `git status --porcelain -- $(cat <the recorded set>)` | empty — `PIN-TREE-IDENTICAL` |

Success prints the marker rather than relying on the absence of output, because an empty
result and a mistyped path produce the same silence.

**The conclusion these two checks license, and no more than this:** a re-derivation
performed against the working tree is a re-derivation against the pinned tree, for every
path either report cites. The claim is not extended to any path outside the set; the set is
closed, and how it was derived is recorded in `54-INTAKE.md` so a later reader can re-open
it if a new citation appears.

The `source_baseline` pin below covers the attachments. It does **not** cover the live tree; that is what this section is for.

## Consolidation join points (ERW Rule 11)

When merging several agents' reports:

- **The per-surface menus** (master §5.1–§5.6) join on the surface. Disagreement between agents on a surface is a finding, not noise — carry both into the decision sheet.
- **The §5.7(a) capacity accounting** is the cross-check: two agents who disagree on a suggested default but agree on the scaling laws have a resolvable disagreement; two who disagree on the scaling laws have a physics dispute that must be settled before any menu is trusted.
- **The §5.7(c) source-method identification** should converge. If agents name different source methods, or one cannot find one, that is the single most important thing to resolve first — the whole calibration question is downstream of it.
- **Premise-challenge findings** (up-front sections) merge first, before any answers are read. A contradicted premise invalidates the answers built on it, however well argued.
- **The composed first-run recipes** are the coherence check across menus. Compare them directly; a recipe that no agent's own menus compose into is a signal that the menus interact in a way the per-question answers missed.

## Access mode — open-book (ERW Rules 16, 20)

`access_mode: open-book` — transcribed from roadmap Phase 54 Success Criterion 4, which already fixes the route as a Route-B open-book build-design round against the post-repair tree. The mode is transcribed, not selected.

Under Route B, ERW Rules 1–2 invert: repository paths in the master are expected, and the "attached files only" instruction must not appear.

Rule-20 live-tree pin: see the **Rule-20 live-tree pin — stamped per engagement** section above, which now carries one block per returned report because the pin records the tree the agent actually saw and the two agents did not see the same thing.

**Qualification recorded after delivery (2026-09-02, plan `54-08`).** The declaration above is the round's declared mode and it is left exactly as declared — it is the historical record of what the package said, and `54-HANDOFF-READINESS.md` check H2 certified it correctly against the package as it stood. One of the two engagements did not run under it: the closed-book report states in its own opening (`research_results/chatgpt-resolution.md:7`) that it worked from the attachments and published literature without live repository verification. The finding, the evidence for it, and the per-report verification burdens it implies are recorded under the marker `RULE-16-DIVERGENCE` in `.planning/phases/54-recalibration-decision-grounding/54-INTAKE.md`. The defect is in the round's declaration, not in either agent's conduct — both declared their own access up front.

## ERW-02 obligations — what is done and what remains

| Obligation | State |
|---|---|
| `research_package/RESEARCH-AGENT-PROMPT.md` (Rule 7 output contract, Rule 17 premise-challenge, Rule 18 read-only bars) | **done** |
| `specs/framework-specs-bundle.md` (Rule 15 single-file bundle) | **done** — 10 verbatim excerpts, byte-verified |
| `research_package/v2.2-closure-evidence-bundle.md` | **done** — 3 documents reproduced in full, byte-verified |
| Master accuracy-and-faithfulness pass | **done** — see master §11 for the amendment record and audit results |
| Rule-20 live-tree pin | **stamped** — per engagement, by plan `54-08` on 2026-09-02; see the Rule-20 section above |
| `research_results/<agent>-resolution.md` | **landed** — 2 returned reports; the count is derived, not assumed, at `.planning/phases/54-recalibration-decision-grounding/54-INTAKE.md` check I1 |
| Rule-19 per-claim in-repo verification report under `docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/` | after delivery, **before** any claim informs a decision |
| Consolidated `trainex-r3-resolution-doc.md` (Rule 12) | after verification |
| Checkpoint ② ratification in `54-RULING.md` | owner, after consolidation |

## The gate and the ruling record

Checkpoint ① is blocking. The ruling record is `.planning/phases/54-recalibration-decision-grounding/54-RULING.md` — created by plan 54-03 and filled by the owner. A ruling is recorded there rather than in the gap register, because a ruling is not a gap (D-09).

The gap anchor `GAP-54-01` in `.planning/phases/54-recalibration-decision-grounding/54-GAPS.md` and `.planning/milestones/v2.3-GAPS.md` stays `OPEN` until checkpoint ② is discharged.

## Provenance

`source_baseline`: `6a4f9b9902ab62e1d1f57bba0e521f38120c416d` — the repository commit at package assembly, and the ERW Rule-5 baseline pin every `file:line` citation in the master is re-derivable against. Byte-identical to the master's frontmatter value.

## Scope notes (the standing boundaries, in plain terms)

- **SCOPE-33** — Framework-spec edits are authorized, narrowly: only the items in `52-VER-20-ROUTING-HANDOFF.md` (a)–(e), plus the `n_col`/`N_t` disposition coupled to item (e) per SPEC-06. No open-ended spec rewriting.
- **SCOPE-34** — The recalibration decision is owner-ratified, never agent-decided. The agent assembles and frames the decision packet (ERW-01) and, if commissioned, the `trainex-r3` round (ERW-02); it marks no default, ranks no option, and picks nothing.
- **SCOPE-35** — Exactly one held-out evaluation — the one preserved unspent from v2.2. It may be spent only on a run passing its preconditions, only after the recalibrated recipe actually trains, and only on a seed pre-registered before RUN-04/05 execute.
- **SCOPE-36** — Stage-0 only. No Stage-1+, no PLAT-01..07 platform work.
- **SCOPE-37** — After the spec edit lands, iteration is conformance-only again: no further tuning against observed re-run results without a new owner decision.
- **SCOPE-38** — Amending a locked contract requires explicit re-ratification: recorded provenance, the superseded ruling named, and a re-issued acceptance criterion. A changed number without a re-ratified contract is not a legal v2.3 edit.

## Standing of the eventual resolution doc

If the round is commissioned, the consolidated resolution document is a candidate verdict source presented for owner ratification at checkpoint ② — not an authority. Phase 56 may not open until checkpoint ② is discharged.
