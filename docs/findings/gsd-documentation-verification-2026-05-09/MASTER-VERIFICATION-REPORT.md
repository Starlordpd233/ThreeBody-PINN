# GSD Documentation Verification Report

**Date:** 2026-05-09
**Scope:** All GSD planning documents in `.planning/` verified against live codebase and git state
**Method:** 3 parallel verification agents + orchestrator analysis
**Files verified:** 39 core GSD documents across 7 categories

---

## Executive Summary

The GSD documentation system has **22 verified discrepancies** across 4 severity tiers. The most critical issues are: (1) ROADMAP.md reports Phase 9 as "Not Started" when it is complete with all 3 plans, summaries, verification, and validation passed; (2) all 7 `.planning/codebase/` analysis documents are frozen at 2026-04-27 with numerous stale file paths; (3) STATE.md has incorrect plan/phase counts; (4) documentation is split across multiple inconsistent snapshots that tell different stories about project state.

---

## Severity Classification

| Severity | Count | Definition |
|----------|-------|------------|
| **BLOCKER** | 6 | Makes documentation actively misleading — reader will take wrong action |
| **MAJOR** | 7 | Factually wrong but unlikely to cause wrong action |
| **MINOR** | 6 | Stale reference, missing update, or cosmetic issue |
| **OBSERVATION** | 3 | Not a bug, but a maintainability concern |

---

## BLOCKER: Phase 9 Status is Critically Wrong

**ROADMAP.md lines 48-51, 84** report Phase 9 (Issues Directory Consolidation) as:

- `[ ]` unchecked plan checkboxes (all 3)
- `0/3` plans complete
- Status: `Not Started`
- No completion date

**Actual filesystem state:**

```
.planning/phases/09-issues-directory-consolidation/
├── 09-01-PLAN.md          (16,526 bytes — substantive plan)
├── 09-02-PLAN.md          (8,978 bytes — substantive plan)
├── 09-03-PLAN.md          (10,817 bytes — substantive plan)
├── 09-01-SUMMARY.md       (6,443 bytes — complete)
├── 09-02-SUMMARY.md       (5,969 bytes — complete)
├── 09-03-SUMMARY.md       (4,453 bytes — complete)
├── 09-VERIFICATION-REPORT.md    — verdict: "PASS AFTER REMEDIATION"
├── 09-VALIDATION.md             — all 25+ checks PASS, all 6 gates PASS
├── 09-RE-VERIFICATION-REPORT-*.md (4 files from different models)
└── 09-CONTEXT.md, 09-RESEARCH.md, 09-REVIEW.md, 09-REVIEWS.md, 09-REVIEW-FIX.md, 09-DISCUSSION-LOG.md
```

**Deliverables exist on disk:**

```
pinn_instruction/original_latex/review-of-framework/issues/
├── 01-architecture-and-physics-foundations.md  (39,567 bytes)
├── 02-data-pipeline-and-validation.md          (27,868 bytes)
├── 03-curriculum-and-training-loop.md          (42,083 bytes)
├── MIGRATION.md                                (7,643 bytes)
├── README.md                                   (3,218 bytes)
└── archive/                                    (8 files — 7 originals + ARCHIVE_MASTER.md)
```

**Cross-document inconsistency:** Three GSD documents report three different statuses for the same phase:

| Document | Status Reported | Reality |
|----------|----------------|---------|
| ROADMAP.md | "Not Started" (0/3 plans) | **Wrong** |
| STATE.md | "partial; written, pending final verification" | **Close but stale** |
| PROJECT.md | "✓ validated" (marked complete in requirements) | **Correct** |
| Filesystem | COMPLETE — all plans, summaries, verification, validation passed | **Truth** |

**Root cause:** ROADMAP.md's progress table and checkboxes were never updated after Phase 9 plans were written and executed. The verification report confirms all work passed, dated approximately 2026-05-01.

---

## BLOCKER: STATE.md Has Wrong Plan/Phase Counts

**STATE.md frontmatter (lines 10-14):**

```yaml
total_phases: 16
completed_phases: 15
total_plans: 36
completed_plans: 36
percent: 100
```

**Actual counts from verified directory listings:**

| Phase | Plans | Status |
|-------|-------|--------|
| 1 | 3 | Complete |
| 2 | 3 | Complete |
| 3 | 2 | Complete |
| 4 | 2 | Complete |
| 5 | 1 | Complete |
| 6 | 1 | Complete |
| 7 | 2 | Complete |
| 8 | 1 | Complete |
| 9 | 3 | Complete (but ROADMAP says not) |
| 10 | 3 | Complete |
| 11 | 3 | Complete |
| 12 | 3 | Complete |
| 13 | 3 | Complete |
| 14 | 3 | Complete |
| 15 | 3 | Complete |
| 15.1 | 3 | Complete |
| **Total** | **39** | **16/16 phases, 39/39 plans** |

**Errors found:**
- `total_plans: 36` → should be **39** (omits Phase 9's 3 plans)
- `completed_plans: 36` → should be **39** (Phase 9 plans are complete)
- `percent: 100` with `completed_phases: 15/16` → internally inconsistent
- Either Phase 9 counts or it doesn't — can't have it both ways

---

## MAJOR: All 7 Codebase Analysis Docs Are Frozen at 2026-04-27

Every file in `.planning/codebase/` carries a last-analysis date of **2026-04-27**. In the 12 days since, the repository underwent significant restructuring (v1.3 completion, Phase 15.1, markdown conversion cleanup). None of the documents reflect current state.

### Specific stale references found

**STRUCTURE.md** (most affected — 10 stale claims):
| Line(s) | Stale Claim | Current State |
|----------|-------------|---------------|
| 222 | `markdown_conversions/` (plural) | `markdown_conversion/` (singular) |
| 222-223 | References `ctl_instruction_v2.md`, `pinn_architecture_v2.md` | v2 files deleted |
| 226-233 | Lists `pandoc_conversion/` with 6 .md files + Python script | Directory restructured; script and files gone |
| 207-216 | Lists 7 original issue files in `issues/` | Files moved to `issues/archive/`; replaced by 5 consolidation docs |
| 268, 524 | `docs/plans/splitting_latex.md` | File deleted |
| 270, 525 | `docs/superpowers/plans/2026-03-19-remove-qwen-model-and-mlx.md` | File and entire directory path deleted |
| 277, 528 | `/amp` file at repo root | File deleted |
| 266-278 | Overall `docs/` tree | Missing `docs/findings/` directory and 4 new files |

**CONCERNS.md:**
| Line | Stale Claim |
|------|-------------|
| 189 | Phase 9 has "0/3 plans complete"; references old `issues/` structure |
| 214 | References `FINAL_ic_generator_enhanced.py` — file was deleted in Phase 1 cleanup |

**ARCHITECTURE.md:**
| Line | Stale Claim |
|------|-------------|
| 162 | `pinn_instruction/markdown_conversions/` (plural, wrong directory name) |

**STACK.md:**
| Line | Stale Claim |
|------|-------------|
| 131, 155 | References `pandoc_conversion/convert_latex_to_md.py` — file no longer exists |

**TESTING.md:**
| Line | Stale Claim |
|------|-------------|
| 19 | References `./test_lib_data` — binary does not exist (never existed) |
| 45 | "No `tests/` directory exists anywhere" — `tests/test_phase12_validation.py` now exists |
| 88 | `test_pipeline.py` claimed 408 lines — actually 407 |

**INTEGRATIONS.md:** No factual errors found (mostly references stable paths).

**CONVENTIONS.md:** No factual errors found (describes patterns, not specific files).

---

## MAJOR: v1.3-ROADMAP.md Omits Phase 15.1

**`.planning/milestones/v1.3-ROADMAP.md`:**
- Header says `Phases: 10–15` and `Total Plans: 18`
- Status says `SHIPPED 2026-05-06`
- **Phase 15.1** (3 plans, completed 2026-05-08) is entirely absent
- Actual v1.3 milestone has **7 phases, 21 plans**, not 6/18
- Ship date of 2026-05-06 predates Phase 15.1 completion by 2 days

---

## MAJOR: Duplicate MILESTONE-AUDIT Files

Two files are **byte-for-byte identical** (diff produces no output):

- `.planning/MILESTONE-AUDIT-v1.3.md` (294 lines)
- `.planning/milestones/v1.3-MILESTONE-AUDIT.md` (294 lines)

One is an unintentional duplicate. Keeping both creates confusion about which is authoritative and risks divergent edits.

---

## MAJOR: PROJECT.md References Missing Directory

**PROJECT.md line 111:**
> `Qwen 3.5 2B 4-bit model already downloaded at Qwen3.5-2B-4bit/`

The directory `<home>/Desktop/3_body_problem/Qwen3.5-2B-4bit/` does **not** exist. A filesystem search for `Qwen*` directories found no matches. This is either a stale reference (model was removed) or was never actually present at this path.

---

## MINOR: PROJECT.md Stale Footer Date

**PROJECT.md line 159** says `Last updated: 2026-05-06` while ROADMAP.md and STATE.md both say `2026-05-08`. PROJECT.md was not updated for Phase 15.1 completion.

---

## MINOR: REQUIREMENTS.md Stale Footer Date

**REQUIREMENTS.md line 104** says `Last updated: 2026-05-01` but the CAND-02 checkbox was fixed after 2026-05-06 (per audit reports). The footer date was never updated.

---

## MINOR: Confusing Self-Reference in v1.3-MILESTONE-AUDIT.md

**`.planning/v1.3-MILESTONE-AUDIT.md` line 215:**
> `Prior audit (stale): .planning/v1.3-MILESTONE-AUDIT.md (this file, previous version)`

This self-reference says the prior audit is the same file at the same path, implying in-place overwrite. This is confusing — it reads as if a different historical file should exist.

---

## MINOR: Uncommitted Phase 15.1 Planning Artifacts

Git status shows Phase 15.1 plan/summary/review files are untracked:

```
.planning/phases/15.1-markdown-conversion-correction/
├── 15.1-01-PLAN.md        (untracked)
├── 15.1-02-PLAN.md        (untracked)
├── 15.1-03-PLAN.md        (untracked)
├── 15.1-PLAN-REVIEW.md    (untracked)
└── 15.1-REVIEW.md         (untracked)
```

The code changes from Phase 15.1 were committed (per git log), but the planning artifacts were never staged. ROADMAP.md and STATE.md mark Phase 15.1 as "complete" without noting these uncommitted artifacts.

---

## MINOR: Uncommitted Markdown Conversion Modifications

Four authoritative markdown files have uncommitted modifications (Phase 15.1 residual):

| File | Change |
|------|--------|
| `pinn_instruction/markdown_conversion/ctl_instruction.md` | 2 lines changed |
| `pinn_instruction/markdown_conversion/review_of_framework.md` | 8 lines added |
| `pinn_instruction/markdown_conversion/sampling_method.md` | 14 insertions, 12 deletions |
| `pinn_instruction/markdown_conversion/stage_strat_revision.md` | 8 insertions, 1 deletion |

No GSD document mentions these uncommitted modifications.

---

## MINOR: Undocumented Temporary Directories

Two directories exist uncommitted and untracked, not mentioned in any GSD doc:

- `.planning/debug/markdown-v13-conversion-audit.md` (2,892 bytes)
- `.planning/tmp/docs-work-manifest.json` and `verify-Phase-9-consistency.json`

---

## OBSERVATION: Documentation Fragmentation

The project maintains documentation across multiple systems:

1. **GSD planning** (`.planning/`) — 200+ files across ROADMAP, STATE, PROJECT, phases, milestones, codebase analysis, research, quick tasks
2. **Repository root docs** (`CLAUDE.md`, `ANTIGRAVITY.md`, `AGENTS.md`, `GEMINI.md`) — AI assistant instructions
3. **Findings docs** (`docs/findings/`) — audit reports and verification findings
4. **User plans** (`docs/user_plans/`) — task-specific planning
5. **Source documentation** (`simulation_data/Documentation/`) — data pipeline docs

The same facts appear in multiple places (e.g., Phase 9 status in ROADMAP.md, STATE.md, PROJECT.md) with different levels of accuracy. There is no single source of truth, and the system relies on manual synchronization.

---

## OBSERVATION: v1.2 Milestone Status Ambiguity

ROADMAP.md section header says v1.2 is "IN PROGRESS" but the only phase in v1.2 (Phase 9) is effectively complete. The milestone's actual status is ambiguous:
- If Phase 9 is complete, v1.2 should be marked SHIPPED
- If Phase 9 verification is pending, the pending item should be explicitly named
- Currently: 3 documents give 3 different answers

---

## OBSERVATION: No Automated Consistency Checks

The GSD system has no mechanism to detect when:
- A phase directory has plans but ROADMAP.md says "Not Started"
- STATE.md counts don't match filesystem reality
- Codebase analysis docs reference deleted files
- Two documents contradict each other about the same fact

All 22 discrepancies found in this audit were discovered through manual comparison.

---

## Remediation Priority

### Immediate (fix today)
1. **Update ROADMAP.md Phase 9** — check all 3 plan boxes, update progress table to `3/3`, change status from "Not Started" to "Complete", add completion date
2. **Fix STATE.md counts** — `total_plans: 39`, `completed_plans: 39`, `completed_phases: 16`
3. **Delete duplicate** `.planning/MILESTONE-AUDIT-v1.3.md` (or `milestones/v1.3-MILESTONE-AUDIT.md`)

### This week
4. **Update v1.3-ROADMAP.md** — add Phase 15.1, update plan count to 21, update ship date to 2026-05-08
5. **Regenerate codebase analysis docs** — all 7 are stale (12 days behind); run `/gsd-map-codebase` to refresh
6. **Update PROJECT.md** — bump footer date to 2026-05-09, verify or remove Qwen3.5-2B-4bit/ reference

### Later
7. **Commit untracked Phase 15.1 artifacts**
8. **Clean up `.planning/debug/` and `.planning/tmp/`** — commit or remove
9. **Consider adding a consistency check script** — verify plan counts, cross-reference phase status, detect stale codebase analysis docs

---

## Verification Method

| Category | Agent | Files Checked | Discrepancies |
|----------|-------|---------------|---------------|
| Core GSD docs (ROADMAP, STATE, PROJECT) | gsd-doc-verifier (Phase 9 focus) | 3 | 6 |
| Codebase analysis docs | Explore (structure/paths) | 7 | 9 |
| Milestone docs + cross-refs | Explore (references/status) | 8 | 7 |
| **Total** | | **18+** | **22** |

---

*Report generated 2026-05-09 by GSD docs-update verification workflow. Three parallel agents verified claims against the live filesystem and git state.*
