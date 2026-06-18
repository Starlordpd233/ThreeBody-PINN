# Phase 30: Document-List & Consolidation Plan (PKG-05)

**Purpose:** Enumerate the candidate research-package deliverables for issue-03
(`03-curriculum-and-training-loop.md`), classify each as **standalone** (byte-for-byte intact
snapshot) or **consolidated** (one shared context file), LOCK the package form
(MULTI-COMPANION) up front, and pose the open inclusion calls for the D-09 hard user gate. This
document is surfaced to the user **before any package assembly** — assembly is 30-03+, gated on
the D-09 approval recorded at the bottom of this file. No package directory, snapshot, or
companion file is created in this plan.

**Prepared:** 2026-06-18
**Phase:** 30-research-package-assembly · Plan 30-02 · Wave 2
**Governance:** v1.6 adjudication-milestone STOP protocol applies (CLAUDE.md). Mechanical /
presentation choices are noted in-artifact. No source-silent semantic, process-artifact-schema,
or cross-phase decision arose in preparing this plan — the package-form lock and the three
inclusion calls are operational package-structure choices already covered by CONTEXT D-09
discretion and the 30-RESEARCH Consolidation Map, NOT STOP-protocol gaps. This is the v1.5 D-07
analog (`23-CONSOLIDATION-PLAN.md`).

---

## Final Candidate Document List

Populated from the D-07 locked input set, the 30-RESEARCH "Consolidation Map (PKG-05)", and the
confirmed shipping annotations from 30-01 (`30-REPORTS-CHARACTERIZATION.md`). Role annotations
live in the manifest / this list, NEVER inside the copied files (reconciles D-04 byte-for-byte
with the manifest-annotation convention).

| # | Document | Role annotation | Treatment | Recommendation |
|---|----------|-----------------|-----------|----------------|
| 1 | `03-curriculum-and-training-loop.md` | Adjudication subject — NON-authoritative; may contain errors (including its own "Recommended Resolutions"); carries the `D = 6.694` claim | Intact, byte-for-byte snapshot | Required |
| 2 | `ctl_instruction.md` | Spec-edit target (SCOPE-13); carries curriculum staging, `τ_L`/`L_max`, s_min gate, loss scaling, PHYS-01 `D ≈ 4.6416` | Intact, byte-for-byte snapshot (D-04) | Required |
| 3 | `pinn_architecture.md` | Spec-edit target (SCOPE-13); carries gradient-clipping / training-strategy / output-head contracts | Intact, byte-for-byte snapshot (D-04) | Required |
| 4 | `sampling_method.md` | **FROZEN** (SCOPE-08); historical record of dataset generation; NOT a revision target | Intact, byte-for-byte snapshot | Required |
| 5 | `review_of_framework.md` | **baseline design intent** (ERW rule 6) + **baseline-critique mandate**; curriculum-relevant research report (SCOPE-09, non-authoritative); challengeable ONLY via explicit option-vs-baseline proposals; **locked-within-baseline hard constraints exempt (F10)** | Intact, byte-for-byte snapshot | Required |
| 6 | `stage_strat_revision.md` | **baseline design intent** (ERW rule 6) + **baseline-critique mandate**; data-driven stage-assignment research report (SCOPE-09, non-authoritative); methodology challengeable via option-vs-baseline only | Intact, byte-for-byte snapshot | Required |
| 7 | Consolidated context file (one file) | Scattered minimal `simulation_data` / v1.5 excerpts, each fragment source-labeled internally (D-10) | Consolidation (D-09) | Required |
| 8 | `verified-facts-reference.md` | **STANDALONE** v1.5-verified-facts reference; reused by the claims register + the SCOPE-12 preamble; **produced and owned by 30-03 Task 2 (single owner; F11)** | Standalone companion (snapshot-class) | Required |
| 9 | `framed-research-questions.md` | PKG-06 framed questions, issue-03 section order; D-04/D-05/D-06 + `D` conflict posed UNSETTLED | Authored companion (multi-companion form) | Required |
| 10 | `scope-12-hard-constraints.md` | SCOPE-12 hard-constraints preamble, verbatim locked v1.4 + v1.5 outcomes (D-13) | Authored companion (multi-companion form) | Required |
| 11 | `resolution-doc-skeleton.md` | Non-binding per-finding resolution-doc skeleton (D-14); carries finding → adjudication-phase (32–36) mapping | Authored companion (multi-companion form) | Required |
| 12 | `claims-register.md` | PKG-07 claimed-vs-verified figure register (uploaded form of `30-CLAIMS-INVENTORY.md`); states the D-17 no-in-milestone-verification boundary | Authored companion (multi-companion form) | Required |

**Total deliverable files:** 12 candidate documents (6 intact standalone snapshots + 1
consolidated context file + 1 standalone verified-facts reference + 4 authored upload
companions). This far exceeds the ~5-file threshold → the consolidation rule fires (D-09).

> **Manifest note.** The uploaded `RESEARCH-CONTEXT-MASTER.md` references companions #8–#12 by
> **bare filename** only (ERW rule 1 / D-05); the intact spec/issue/report snapshots #1–#6 and the
> consolidated context file #7 live in `specs/`. All repo source paths live ONLY in the
> never-uploaded `DELIVERY-NOTE.md`. The role-annotation column above carries the
> baseline-design-intent + baseline-critique-mandate annotation confirmed by 30-01 for the two
> reports.

---

## Package Form (LOCKED)

**The package form is LOCKED as MULTI-COMPANION.** This is the CONTEXT-recommended default
(30-CONTEXT.md "Claude's Discretion", lines 81–83; 30-RESEARCH Open Question 2) and is fixed
**here, up front**, so 30-04 authors its companions against a settled architecture and 30-05
references them by bare filename — never orphaning or duplicating them (F3). The package form is
**not re-litigated** at the D-09 gate; only the document list and the three inclusion calls are
ratified there.

Under the multi-companion form:

- `framed-research-questions.md`, `scope-12-hard-constraints.md`, `resolution-doc-skeleton.md`,
  and `claims-register.md` ship as **named companion files**, each a clean attachable unit,
  referenced by **bare filename** from a manifest table in `RESEARCH-CONTEXT-MASTER.md` — NOT
  folded into the master (F3). The master is a thin orientation + manifest entry point that
  points at the companions.
- `verified-facts-reference.md` is a **standalone** companion (inclusion call (b), resolved
  standalone below), **produced and solely owned by 30-03 Task 2** (single owner; F11) — no other
  plan authors or duplicates it.
- The `RESEARCH-AGENT-PROMPT.md` attach-list header enumerates exactly which companions + specs
  to attach, by bare filename (a package without its prompt is incomplete, ERW rule / D-03).

> **Why locked now, not at the gate:** if the form were left open until assembly, 30-04 could
> author companions that 30-05 then folds into the master (or vice versa), orphaning files or
> duplicating content (F3). Locking the form here gives every downstream plan one settled target.

---

## What Is Consolidated vs Standalone

### Standalone — byte-for-byte intact snapshots (NEVER consolidated, D-04)

The framework specs are **NEVER consolidated** (D-04 / PKG-05 hard rule). `ctl_instruction.md`,
`pinn_architecture.md`, and `sampling_method.md` ship as **byte-for-byte intact** copies; their
hashes in `30-SNAPSHOT-HASHES.txt` must match source. The issue doc and the two reports likewise
ship intact. All role / FROZEN / non-authoritative / baseline-critique annotations live in the
manifest column, **never inside the copied files**.

- Documents #1–#6: each becomes a standalone intact snapshot in `specs/`.
- Document #8 (`verified-facts-reference.md`): a standalone companion (reused by the claims
  register + the SCOPE-12 preamble).
- Documents #9–#12: authored companions (the multi-companion form), each a standalone attachable
  file.

**Framework specs are NEVER consolidated, excerpted, or summarized — this is the dominant
landmine for this round (large specs + an active consolidation rule). Any `specs/` framework-spec
file whose hash differs from source is a defect.**

### Consolidated — one context file (D-09 / D-10)

Only **scattered minimal dataset fragments** consolidate, into the single consolidated context
file (Document #7). Per D-10 this consolidated file MAY retain internal per-fragment
source-path provenance labels (it is a snapshot-class grounding companion); the master and prompt
carry zero repo paths and reference it by bare filename (D-05). Per D-22, doc-03 is less
dataset-centric than v1.5, so the excerpts are **minimal** — only the v1.5-verified facts the
curriculum / training-loop contracts depend on. Candidate fragments (final selection resolved by
inclusion call (a) below):

| Fragment | What it contributes |
|----------|---------------------|
| Per-variant snapshot / `dt_out` distributions | grounds the stage `dt_out` figures (0.08 / 0.01 / 0.17) and bounds `τ_L` / `L_max` / collocation scaling |
| Stage-assignment-relevant counts | per-stage population context for the stage-assignment finding cluster |
| Gold-gap record (184 IDs; ~2,565 gold) | the 184 standard IDs without gold; 2,749 base / 2,565 gold counts |
| EVID-10 D-rejection anchor | the committed v1.5 verdict that `D = 6.694` was rejected vs raw-mass `D ≈ 4.6416` — anchors the `D`-conflict framing |

### Excluded from consolidation

- `pinn/` live code — EXCLUDED (SCOPE-10 / D-08); the package states issue-03's "Canonical"
  `pinn/` citations are overridden (directive 2026-05-19).
- Framework specs — NEVER consolidated (D-04); shipped intact.
- Issue-01 / issue-02 docs — resolved; their outcomes travel as the SCOPE-12 block + the intact
  specs (D-08).

---

## Why The Consolidation Rule Fires

The candidate list is **12 deliverable documents** (6 intact snapshots + 1 consolidated context
file + 1 standalone verified-facts reference + 4 authored companions). PKG-05's consolidation
criterion is "consolidate if the list would exceed ~5 files or the context is scattered across
fragments." With 12 documents and dataset facts scattered across multiple v1.5 sources, the rule
fires.

The scattered dataset fragments (per-variant `dt_out` / snapshot distributions, gold-gap record,
EVID-10 D-rejection) are consolidated into **one** context file rather than shipped as separate
fragment files, keeping the attachable count manageable for external researchers. Surfacing this
plan to the user before assembly is a **PKG-05 requirement (D-09), not a courtesy** — the user's
approval at the D-09 gate locks the final document list and resolves the three inclusion calls.

---

## Open Inclusion Calls (D-09 User Gate)

These are the three decisions the D-09 gate asks the user to ratify. The package FORM
(multi-companion) is already locked above and is NOT among them.

### Inclusion Call (a): exact `simulation_data` / v1.5 excerpt selection for the consolidated file

**Recommendation: the MINIMAL research-recommended set** (per 30-RESEARCH "Consolidation Map" +
D-22). Include only: per-variant snapshot / `dt_out` distributions; stage-assignment counts; the
184-gap; the ~2,565 gold count; and the EVID-10 `D`-rejection anchor — and nothing more. doc-03 is
less dataset-centric than v1.5, so the footprint stays minimal.

### Inclusion Call (b): standalone-vs-folded for the v1.5-verified-facts reference

**Recommendation: STANDALONE** (30-RESEARCH line 248 + CONTEXT line 83). Kept standalone because
it is reused by BOTH the claims register and the SCOPE-12 preamble; folding it into the
consolidated context file would force those two companions to re-cite a buried fragment. The
standalone `verified-facts-reference.md` is produced and solely owned by 30-03 Task 2 (single
owner; F11).

### Inclusion Call (c): does the MINOR ALM-`μ_p`-clamp finding get its own framed question?

**Recommendation: INCLUDE it.** The ALM-`μ_p`-clamp finding (issue-03 line 117, 489–505;
`mu_p = np.clip(mu_p, 1e-4, 100)`) is a MINOR/INFO item that feeds LOOP-05. It is not in the
SPEC-locked selected set (which is an "at least" set), so this is a coverage-breadth call.
Including it preserves training-loop-contract coverage and avoids the F13 consequence — if dropped,
LOOP-05 has no resolution-doc verdict path. Default = include.

> **F13 (declined-findings consequence).** Any finding the user DECLINES at this gate must be
> recorded in the "Declined findings" slot of the D-09 record below so 30-04 lists it in the
> SCOPE-12 preamble as **"out of scope for this adjudication"**. For the ALM-clamp question
> specifically: dropping it means LOOP-05 has **no resolution-doc verdict path** — record that
> consequence alongside the decline.

---

## What This Plan Does NOT Do

- **No package directory is created.** Assembly (`specs/`, the round directory) is 30-03+, gated
  on the D-09 approval below.
- **No snapshots are taken.** Byte-for-byte copies happen during assembly (30-03).
- **No companion files are authored.** `framed-research-questions.md`,
  `scope-12-hard-constraints.md`, `resolution-doc-skeleton.md`, `claims-register.md`, and
  `verified-facts-reference.md` are authored in later waves (30-03/30-04), not here.
- **No framework specs are edited.** D-04 / SCOPE-08 / SCOPE-09 / SCOPE-13 — specs and reports are
  read-only; this plan only classifies and lists them.
- **No empirical probes are run.** v1.6 has no Phase-24 analog (D-17); all figures remain at their
  CLM-registered status (`claimed-unverified` or `verified`). No figure is verified here.
- **No STATE.md / ROADMAP.md edits.** Those are owned by the orchestrator.

---

*This document is surfaced at the D-09 user gate. The user's decision on the three inclusion
calls locks the final package contents for assembly (30-03+). The package form is already locked
MULTI-COMPANION and is not re-litigated here.*

---

## D-09 APPROVED Record

**Date:** 2026-06-18
**Decision authority:** User (pre-authorized 2026-06-18 — approvals waived; approve-as-proposed)
**Status:** APPROVED

> **Provenance:** The user waived per-step approvals for this run and instructed the orchestrator
> to finish Wave 2 autonomously, pre-authorizing "approve-as-proposed" with the
> research-recommended SAFE defaults. This record transcribes those orchestrator-authorized
> decisions; each aligns with the 30-RESEARCH "Consolidation Map" recommendations (no conflict).
> This is reversible: no assembly runs until 30-03 (a later wave), so the user may revise the
> inclusion calls before assembly begins.

### Approved Document List (12 documents)

| # | Document | Role annotation | Treatment |
|---|----------|-----------------|-----------|
| 1 | `03-curriculum-and-training-loop.md` | Adjudication subject — NON-authoritative; carries `D = 6.694` | Intact snapshot |
| 2 | `ctl_instruction.md` | Spec-edit target (SCOPE-13); PHYS-01 `D ≈ 4.6416` | Intact, byte-for-byte (D-04) |
| 3 | `pinn_architecture.md` | Spec-edit target (SCOPE-13); training-strategy / output-head contracts | Intact, byte-for-byte (D-04) |
| 4 | `sampling_method.md` | FROZEN (SCOPE-08); historical record | Intact, byte-for-byte |
| 5 | `review_of_framework.md` | baseline design intent + baseline-critique mandate (locked-within-baseline values exempt, F10) | Intact snapshot |
| 6 | `stage_strat_revision.md` | baseline design intent + baseline-critique mandate | Intact snapshot |
| 7 | Consolidated context file | Minimal `simulation_data` / v1.5 excerpts, source-labeled internally (D-10) | Consolidation (D-09) |
| 8 | `verified-facts-reference.md` | STANDALONE v1.5-verified-facts reference; owned by 30-03 Task 2 (F11) | Standalone companion |
| 9 | `framed-research-questions.md` | PKG-06 framed questions; D-04/D-05/D-06 + `D` conflict UNSETTLED | Authored companion (multi-companion) |
| 10 | `scope-12-hard-constraints.md` | SCOPE-12 hard-constraints preamble, verbatim (D-13) | Authored companion (multi-companion) |
| 11 | `resolution-doc-skeleton.md` | Non-binding per-finding skeleton (D-14); finding → phase 32–36 map | Authored companion (multi-companion) |
| 12 | `claims-register.md` | PKG-07 claimed-vs-verified register; D-17 boundary | Authored companion (multi-companion) |

**Package form:** MULTI-COMPANION (LOCKED in Task 1; not re-litigated).

### Inclusion Decisions

- **Inclusion Call (a) — sim_data excerpt selection:** APPROVED — the MINIMAL
  research-recommended set per the 30-RESEARCH Consolidation Map + D-22: per-variant snapshot /
  `dt_out` distributions; stage-assignment counts; the 184-gap; the ~2,565 gold count; the EVID-10
  `D`-rejection anchor. Nothing beyond this minimal set.
- **Inclusion Call (b) — standalone-vs-folded verified-facts reference:** APPROVED — **STANDALONE**
  (the research-recommended default; reused by the claims register + the SCOPE-12 preamble;
  produced and solely owned by 30-03 Task 2 per F11).
- **Inclusion Call (c) — ALM-`μ_p`-clamp own framed question:** APPROVED — **INCLUDE** (preserves
  LOOP-05 coverage; avoids the F13 no-verdict-path consequence). Matches the 30-RESEARCH
  recommendation to surface-and-include; 30-RESEARCH does not recommend exclusion.

### Declined findings

**None.** No finding was declined at this gate; the ALM-`μ_p`-clamp question is INCLUDED, so
LOOP-05 retains its resolution-doc verdict path. (Slot retained per F13 for any future revision —
if a finding is later declined, 30-04 must list it in the SCOPE-12 preamble as "out of scope for
this adjudication," with the downstream consequence noted.)

**Assembly unlocked.** 30-03 may proceed with snapshot assembly against this approved document
list and the resolved inclusion calls.
