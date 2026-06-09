---
phase: 22
plan: 04
wave: 2
status: completed
executed_at: 2026-06-09
execution_status: completed
review_status: pending
depends_on: ["22-01", "22-02", "22-03"]
artifacts_produced:
  - .planning/phases/22-framework-spec-cleanup/22-COMMENT-CENSUS-POST.md
  - .planning/phases/22-framework-spec-cleanup/22-COMMENT-DIFF.md
  - .planning/phases/22-framework-spec-cleanup/22-COMMENT-HANDOFF.md
---

# Plan 22-04 Summary — Author-Comment Preservation + FUT-05 Handoff

**Objective:** Census every author-flagged comment (all forms/formats) across the three framework
specs in the POST-WS-A state, verify all survived WS-A edits verbatim (0 lost, 0 semantically
changed) by diffing against the pre-WS-A census from Wave 0, and produce the
`22-COMMENT-HANDOFF.md` handoff artifact that FUT-05 consumes for later adjudication. Phase 22
performs NO basis classification, NO adjudication, NO deletion (GAP-22-01 deferral honored).

## Tasks executed

### Task 1: Census + Preservation Diff
- **Pre-condition check:** `22-COMMENT-CENSUS-PRE.md` exists, is tracked (`faa73d0` snapshot) ✓
- **POST capture:** `node tools/spec-render-check/detect.mjs --census` over live HEAD (7fe572e)
  returns 26 (13 ctl + 13 pinn + 0 sampling) — matches PRE union count
- **D-05-aware diff (22-COMMENT-DIFF.md):**
  - 0 comments lost (26 PRE stable-ids = 26 POST stable-ids)
  - 0 comments gained
  - 23/26 text hashes byte-identical
  - 3/26 hash changes documented as mechanical D-05 wrapper repairs (see below)

### Task 2: FUT-05 Handoff
- Wrote `22-COMMENT-HANDOFF.md` per RESEARCH § schema: census-basis header, per-file counts,
  one row per comment with form/file/section/anchor/verbatim/preservation-verified flag,
  negative-control note (SI-PINN-002 meta-doc excluded from defect findings), FUT-05 ownership
  boundary, reconciliation against PRE/POST/DIFF/live census.
- Verified: no disposition / basis-class / keep-remove verdict on any row.

## D-05 wrapper repairs (3 comments)

All 3 are in `pinn_architecture.md`. In each case, 22-02 math normalization repaired
render-breaking syntax in the **prose surrounding** the author-comment clause. The author-comment
clause itself is byte-identical between PRE and POST.

| # | Stable id | Wrapper change | Comment clause preserved |
|---|-----------|----------------|--------------------------|
| 21 | pinn::3-4-soft-energy…::1 | `` `10^-5` ``→`$10^{-5}$`; `epsilon_H`→`$\epsilon_H$`; `<=`→`$\leq$` | byte-identical |
| 22 | pinn::3-4-soft-energy…::2 | `` `10^-5` ``→`$10^{-5}$` | byte-identical |
| 23 | pinn::4-2-optional-alm-ablation…::1 | raw-subscript math → LaTeX `$c_E = \mathrm{RMS}_n(\Delta H_n)$, …` | byte-identical |

## Reconciliation

| Source | Total | ctl | pinn | sampling |
|--------|-------|-----|------|----------|
| 22-COMMENT-CENSUS-PRE.md | 26 | 13 | 13 | 0 |
| 22-COMMENT-CENSUS-POST.md | 26 | 13 | 13 | 0 |
| 22-COMMENT-HANDOFF.md | 26 | 13 | 13 | 0 |
| Live detect.mjs --census | 26 | 13 | 13 | 0 |

All four sources agree: **26 comments, 0 lost, 0 semantically changed.**

## Verification gates satisfied

- **G3 (comment-preservation half):** before/after census diff shows 0 lost, 0 semantically changed;
  pre and post snapshots recorded in committed state.
- **ROADMAP Phase 22 SC 6:** census + verbatim preservation + FUT-05 handoff produced; no
  adjudication/deletion performed (deferral honored).
- **Plan 22-04 acceptance criteria:** all 4 acceptance criteria met.

## STOP gaps encountered

None. No new comment forms discovered beyond the marker set the PRE census already recognized.

## Commits

| SHA | Subject |
|-----|---------|
| `e7204d2` | `evidence(22-04): capture post-WS-A author-comment census + pre/post diff` |
| `99b15f3` | `spec(22-04): produce FUT-05 author-comment handoff (inventory only, no adjudication)` |

## Output locations

- **POST census:** `.planning/phases/22-framework-spec-cleanup/22-COMMENT-CENSUS-POST.md`
- **DIFF:** `.planning/phases/22-framework-spec-cleanup/22-COMMENT-DIFF.md`
- **Handoff:** `.planning/phases/22-framework-spec-cleanup/22-COMMENT-HANDOFF.md`
- **Summary:** `.planning/phases/22-framework-spec-cleanup/22-04-SUMMARY.md` (this file)
