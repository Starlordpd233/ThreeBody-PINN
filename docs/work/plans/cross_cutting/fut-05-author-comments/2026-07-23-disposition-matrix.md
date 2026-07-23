---
status: active
purpose: implementation-plan
created: 2026-07-23
milestone: untracked
phase: cross-cutting
retirement_trigger: All rows have final user_decision; FUT-05 closed; absorb summary into REQUIREMENTS/closeout
---

# FUT-05 Disposition Matrix (working ledger)

**Census basis:** `node tools/spec-render-check/detect.mjs --census` on `HEAD` `2cabd666` (2026-07-23).  
**Raw capture:** `2026-07-23-live-census.raw.txt`  
**Detector residual:** `2026-07-23-detector-all.raw.txt` (3 DEFINITE / 27 REVIEW)  
**Engine:** design §6 — intent → temporal grounding → referent check → basis → disposition.  
**Default:** SURFACE. Every `proposed_disposition` is a **recommendation**, not an applied verdict.

Legend for `status`:

| status | meaning |
|--------|---------|
| `OPEN` | No user decision yet |
| `PROPOSED` | Agent recommendation recorded; awaiting user |
| `DECIDED` | User decision recorded; edit not yet applied |
| `APPLIED` | Spec edit committed |
| `CLOSED-NO-EDIT` | Disposition needs no further edit (already gone / keep / false positive) |

---

## Drift summary (handoff 26 → live 25)

| Change | Handoff | Live | Notes |
|--------|---------|------|-------|
| H11 stage-transition author note | present | **ABSENT** | Body replaced by Phase 33 dual-path stage-transition contract prose; original "test train stage 0" note not found |
| H20 bold-bracket batch-construction flag in §3.1 | present | **ABSENT** | Removed by Phase 34 SI-PINN-003 (`b4325ff9`); §3.1 now points to ctl Mini-Batch Construction |
| Integrity-R2 clearance block | n/a | **extra census hit** | Line ~127 matches marker text `"author note above"` — **false positive**, not a new author comment |
| H26 SI-PINN-003 appendix | open investigation text | **rewritten RESOLVED** | Meta-doc already records Phase 34 reconciliation |
| H25 SI-PINN-002 description | listed 3 body comments incl. batch | **partially updated** | Item 3 text already notes Phase 34 resolution |

Net: 26 − 2 gone + 1 false positive = 25 census markers. Real open comments ≈ 24 (excluding false positive) of which 2–3 are pure meta-docs.

---

## Matrix

Columns: **H** = handoff id from `22-COMMENT-HANDOFF.md`. **Live** = present in 2026-07-23 census (line). Intent/basis/disposition use design §6 vocabulary.

### ctl_instruction.md

| H | Live | Section (anchor) | Intent | Basis (proposed) | Proposed disposition | Evidence / notes | user_decision | status |
|---|------|------------------|--------|------------------|----------------------|------------------|---------------|--------|
| H1 | L111 | multi-stage-data-stratification… | suggestion | GROUNDED-LIVE / JUDGMENT | **SURFACE** — consider REVISE to short "superseded by data-derived $s_0$" note or REMOVE if Integrity-R2 is enough | Integrity-R2 clearance (2026-07-11) already adopts data-first staging from this note; suggestion partially answered, not formally closed | | PROPOSED |
| — | L127 | same section | *(false positive)* | FALSE-POSITIVE | **CLOSED-NO-EDIT** (do not treat as comment); optional detector harden | Census matched Integrity-R2 prose: "proposed in the **author note** above" | | PROPOSED |
| H2 | L425 | phase-1-data-preparation… | syntax-flag + content-stale | JUDGMENT-REQUIRED | **SURFACE** (two claims: conversion syntax *and* "statement outdated / code unusable") | Dual-intent; content half is semantic — not autonomous | | PROPOSED |
| H3 | L1033 | 2-5-global-scaling | syntax-flag | JUDGMENT-REQUIRED | **SURFACE** → likely REMOVE after local render check | Surrounding math is largely `$…$` (v1.5/v1.4 revisions). Comment text still claims backtick math. Confirm Cursor preview; if clean → GROUNDED-STALE | | PROPOSED |
| H4 | L1164 | outputs-of-this-step | syntax-flag | GROUNDED-LIVE | **SURFACE** — fix residual DEFINITE first, then re-classify | Detector still has **DEFINITE** `\lVert` / `\epsilon` outside math at L1354–1355 in this section. Comment not fully stale | | PROPOSED |
| H5 | L1441 | outputs-of-this-step | todo-gap | JUDGMENT-REQUIRED | **SURFACE** | "We need the code snippets here" — product/spec choice | | PROPOSED |
| H6 | L1443 | outputs-of-this-step | open-question | JUDGMENT-REQUIRED | **SURFACE** | "Two paragraphs below are suspicious" — needs human content review | | PROPOSED |
| H7 | L1487 | scope | retained-historical | EXPLICIT-RETENTION | **SURFACE per-note** (keep / archive / answer) | Prefixed "retained as non-normative question"; IC ∈ [-1,1] / final form | | PROPOSED |
| H8 | L1532 | scope | retained-historical | EXPLICIT-RETENTION | **SURFACE per-note** | Math guarantees + "add time t → 14D" — largely answered by v1.4 14D contract; still formal retention | | PROPOSED |
| H9 | L1598 | network-input-contract | syntax-flag | JUDGMENT-REQUIRED | **SURFACE** → likely REMOVE if preview clean | Same family as H3; re-check local math | | PROPOSED |
| H10 | L1669 | phase-2-the-definitive-ctl-pinn-training-loop | retained-historical | EXPLICIT-RETENTION | **SURFACE per-note** | Long training-loop I/O / "replacement for Brutus?" question; partially answered by later contracts + FUT-01 build, not formally closed | | PROPOSED |
| H11 | **ABSENT** | stage-transition-criteria (handoff) | open-question | GROUNDED-STALE (referent superseded) | **ALREADY-GONE** — record only; no delete needed | Live body uses Phase 33 dual-path ADVANCE/RECOVER/HALT contract; original author note text gone | | PROPOSED |
| H12 | L2068 | evaluation-metrics-and-validation | open-question | JUDGMENT-REQUIRED | **SURFACE** | Lyapunov definition cross-ref to §2.3 — yes/no/defer | | PROPOSED |
| H13 | L2136 | reproducibility-note… | syntax-flag | GROUNDED-LIVE | **Wave 2:** fix trailing `\` then **REMOVE** comment (user confirm) | Live line still has `indices\` before the author comment — defect real | | PROPOSED |

### pinn_architecture.md

| H | Live | Section (anchor) | Intent | Basis (proposed) | Proposed disposition | Evidence / notes | user_decision | status |
|---|------|------------------|--------|------------------|----------------------|------------------|---------------|--------|
| H14 | L103 | 1-foundational… | syntax-flag | JUDGMENT-REQUIRED | **SURFACE** → likely REMOVE if superscripts render | Phase 22 math normalization; confirm preview | | PROPOSED |
| H15 | L188 | 2-2-siren-init | syntax-flag | JUDGMENT-REQUIRED | **SURFACE** | Detector has ADJUDICATED code-identifier keeps for `\text{xxx}` / omega names nearby — may be intentional identifiers, not broken math | | PROPOSED |
| H16 | L249 | 2-4-hyperparameters | syntax-flag | JUDGMENT-REQUIRED | **SURFACE** | Table formatting; Phase 22 may have fixed; confirm preview | | PROPOSED |
| H17 | L282 | 3-multi-component-loss… | syntax-flag | JUDGMENT-REQUIRED | **SURFACE** → likely REMOVE if formula renders | Adjacent display math present; re-check | | PROPOSED |
| H18 | L286 | 3-multi-component-loss… | syntax-flag | JUDGMENT-REQUIRED | **SURFACE** | "canonical text form" raw in preview — may be intentional plaintext twin; design treated redundant math carefully | | PROPOSED |
| H19 | L305 | 3-1-data-fidelity | syntax-flag | JUDGMENT-REQUIRED | **SURFACE** → likely REMOVE if $L_{data}$ renders | Live formula above is proper `$$…$$`; comment may be stale | | PROPOSED |
| H20 | **ABSENT** | 3-1-data-fidelity (bold-bracket) | inconsistency-flag | GROUNDED-STALE | **ALREADY-GONE** (Phase 34 SI-PINN-003) | `b4325ff9`; §3.1 PIPE-04 pointer to ctl Mini-Batch Construction | | PROPOSED |
| H21 | L542 | 3-4-energy regularizer | syntax-flag / redundant-math | GROUNDED-STALE (clause) | **Wave 2 candidate REMOVE** (user confirm) | D-05 already normalized surrounding `10^-5` → `$10^{-5}$`; comment still complains about duplicate plaintext | | PROPOSED |
| H22 | L602 | 3-4 Softening Parameter | syntax-flag / redundant-math | GROUNDED-STALE (clause) | **Wave 2 candidate REMOVE** (user confirm) | Same family as H21; parenthetical "again duplicate number" | | PROPOSED |
| H23 | L699 | 4-2 optional ALM | syntax-flag | JUDGMENT-REQUIRED | **SURFACE** | Constraints now LaTeX; nearby REVIEW findings are mostly `mu_p` / code identifiers | | PROPOSED |
| H24 | L1047 | SI-PINN-002 heading | meta-doc | META-DOC | **KEEP** (census completeness) | Negative control / inventory heading — not a defect | | PROPOSED |
| H25 | L1050 | SI-PINN-002 description | meta-doc | META-DOC | **KEEP + co-update** after Waves 2–3 | Still lists omega_0 / hidden-layer todos; item 3 already notes Phase 34 | | PROPOSED |
| H26 | L1060 | SI-PINN-003 description | meta-doc (resolved) | META-DOC | **KEEP** as resolution record (or REVISE for brevity) | Status already RESOLVED by Phase 34; not an open inconsistency | | PROPOSED |

### sampling_method.md

| H | Live | Notes | status |
|---|------|-------|--------|
| — | 0 | Negative control confirmed | CLOSED-NO-EDIT |

### SI-PINN-002 body todos (referenced by H25, not separate handoff rows)

These `\authcomment` themes may still need Wave 3 SURFACE even though they are only listed inside the meta-doc today:

1. "Need more detail on this dynamic scheduling for omega_0" (Section 2)
2. "Need confirmation on this hidden layer's detail" (Section 2)
3. Batch construction — **resolved** under SI-PINN-003 / Phase 34

---

## Recommended Wave 2 package (for your approval)

Do **not** apply until you confirm. Small, mechanical, high-confidence:

| ID | Action | Why |
|----|--------|-----|
| H13 | Remove trailing `\` on `indices\` **and** remove the author comment clause | Defect still live; comment becomes stale only after fix |
| H21 | Remove parenthetical author-comment clause about duplicate `10^-5` | Surrounding math already normalized; comment is the leftover flag |
| H22 | Remove parenthetical "author comment: again duplicate number" | Same |
| H11, H20 | Matrix only — already gone | Close rows without edits |

Optional same-wave if preview-confirmed clean (still SURFACE until you say yes):

| ID | Action |
|----|--------|
| H19 | Remove "again, the syntax is broken" under $L_{data}$ |
| H3, H9, H14, H17 | Remove pure preview-syntax flags after local clean check |

**Not** in Wave 2 (need interactive adjudication): H1–H2, H5–H8, H10, H12, H15–H16, H18, H23–H26, omega_0/hidden-layer depth todos.

---

## Residual detector work (coupled to Wave 2)

At track start (`detect.mjs --all`):

| Severity | Count | Action in FUT-05 |
|----------|-------|------------------|
| DEFINITE | 3 | Fix if blocking a syntax-flag disposition (ctl `outputs-of-this-step` ×2, `phase-2-total-training-loss` ×1) |
| REVIEW | 27 | Do not mass-convert; only touch loci tied to a dispositioned comment |
| ADJUDICATED | 7 | Leave (Phase 22 allowlist) |
| SUPPRESSED | 20 | Leave |

Fixing DEFINITE findings is **presentation-preserving** only (same math meaning), consistent with Phase 22 rules.

---

## Decision log

| Date | Decision | By |
|------|----------|-----|
| 2026-07-23 | Track started; branch repointed to master; no GSD milestone; lightweight plan + matrix | agent + user direction |
| 2026-07-23 | No autonomous removals; Wave 2 package proposed only | agent |

_(Append user decisions here as they land.)_
