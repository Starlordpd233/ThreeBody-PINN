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
| 2 | `specs/framework-specs-bundle.md` | Verbatim locked framework-spec excerpts (13 extraction blocks, byte-verified against the pinned commit). |
| 3 | `research_package/v2.2-closure-evidence-bundle.md` | The 2026-08-17 conformance audit, the VER-20 routing handoff, and the DIAG-05 re-derivation — each reproduced in full. |

Not uploaded: this delivery note (routing only), the prompt (pasted, not attached), and `research_results/` (created at delivery).

**Fan out across several external agents.** Save each as `research_results/<agent>-resolution.md`.

## Rule-20 live-tree pin — fill this at engagement

Open-book `file:line` citations are only re-derivable against the tree the agent actually saw. Record it here **before** pasting:

| Field | Value |
|---|---|
| Worktree | `<home>/Desktop/3_body_problem/.worktrees/trainex` |
| Branch | `milestone/v2.3` |
| Commit at engagement | `11b4e0c1` — the ERW-02 assembly commit, which is the state of the tree as this package was completed. **Re-stamp with the actual `git rev-parse HEAD` if the branch has moved before you grant access.** |
| Access granted by | `PENDING — how access was granted (read-only mount, clone, editor access)` |
| Date of engagement | `PENDING` |

The `source_baseline` pin below covers the attachments. It does **not** cover the live tree; that is what this table is for.

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

Rule-20 live-tree pin: see the **Rule-20 live-tree pin** table above. The worktree and branch are recorded; the engagement commit and access method are stamped by the user at handoff, because the pin records the tree the agent actually saw.

## ERW-02 obligations — what is done and what remains

| Obligation | State |
|---|---|
| `research_package/RESEARCH-AGENT-PROMPT.md` (Rule 7 output contract, Rule 17 premise-challenge, Rule 18 read-only bars) | **done** |
| `specs/framework-specs-bundle.md` (Rule 15 single-file bundle) | **done** — 10 verbatim excerpts, byte-verified |
| `research_package/v2.2-closure-evidence-bundle.md` | **done** — 3 documents reproduced in full, byte-verified |
| Master accuracy-and-faithfulness pass | **done** — see master §11 for the amendment record and audit results |
| Rule-20 live-tree pin | **user, at engagement** — the table above |
| `research_results/<agent>-resolution.md` | at delivery |
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
