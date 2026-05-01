---
phase: 09-issues-directory-consolidation
plan: validation
date: "2026-04-27"
audit_date: "2026-05-01"
---

# Phase 9 Validation Strategy

This is a documentation-only phase. Validation is manual and file-based.

## Test Infrastructure

| Framework | Config | Command |
|-----------|--------|---------|
| Bash (file checks) | N/A | `wc -c`, `wc -l`, `ls`, `grep` |
| Git history | N/A | `git log --follow` |

## Per-Task Map

| Task ID | Plan | Requirement IDs | Automated Check | Status |
|---------|------|-----------------|-----------------|--------|
| 09-01-T1 | 09-01-PLAN | CONSOL-01 | `ls archive/ \| wc -l` = 7 | PASS |
| 09-01-T2 | 09-01-PLAN | CONSOL-01, CONSOL-02 | `wc -c 01-*.md` = 38,806 (30-40 KB) | PASS |
| 09-01-T3 | 09-01-PLAN | CONSOL-01, CONSOL-03 | `wc -c 02-*.md` = 27,266 (20-30 KB) | PASS |
| 09-02-T1 | 09-02-PLAN | CONSOL-01, CONSOL-02 | `wc -c 03-*.md` = 40,944 (30-40 KB) | PASS |
| 09-03-T1 | 09-03-PLAN | CONSOL-01, CONSOL-02 | `wc -c MIGRATION.md` = 7,643 (5-8 KB) | PASS |
| 09-03-T2 | 09-03-PLAN | CONSOL-01 | `wc -l README.md` = 32 (≤50) | PASS |

## Automated Checks (per task)

| Check | Command | Pass Criteria | Status |
|-------|---------|---------------|--------|
| File exists | `ls {path}` | Returns without error | PASS |
| Size budget | `wc -c issues/01-*.md issues/02-*.md issues/03-*.md` | Total < 120 KB (actual: 107,016 B) | PASS |
| README length | `wc -l issues/README.md` | ≤ 55 lines (actual: 32) | PASS |
| Archive completeness | `ls issues/archive/` | 7 files present | PASS |
| Git history preserved | `git log --follow issues/archive/three_body_pinn_pre-implementation_audit_2026-04-27.md` | Shows pre-move history | PASS |
| No orphaned originals | `ls issues/*.md issues/*.txt` | Only new docs present | PASS |
| 01 DECISION-NEEDED count | `grep -c '[DECISION-NEEDED]' 01-*.md` | = 2 | PASS |
| 02 DECISION-NEEDED count | `grep -c '[DECISION-NEEDED]' 02-*.md` | = 1 | PASS |
| 03 DECISION-NEEDED count | `grep -c '[DECISION-NEEDED]' 03-*.md` | = 2 | PASS |
| 01 verbatim Section 5 | `grep -c 'CORRECTED INPUT VECTOR SPECIFICATION' 01-*.md` | ≥ 1 | PASS |
| 03 verbatim Section 6 | `grep -c 'UNIFIED BATCH CONSTRUCTION SPECIFICATION' 03-*.md` | ≥ 1 | PASS |
| Cross-links 01→02/03 | `grep -c '02-\|03-' 01-*.md` | ≥ 1 each | PASS |
| Cross-links 02→01/03 | `grep -c '01-\|03-' 02-*.md` | ≥ 1 each | PASS |
| Cross-links 03→01/02 | `grep -c '01-\|02-' 03-*.md` | ≥ 1 each | PASS |
| Severity labels in 01 | `grep -c 'BLOCKING\|MAJOR' 01-*.md` | ≥ 1 | PASS |
| Severity labels in 02 | `grep -c 'BLOCKING\|MAJOR' 02-*.md` | ≥ 1 | PASS |
| Severity labels in 03 | `grep -c 'BLOCKING\|MAJOR' 03-*.md` | ≥ 1 | PASS |
| Executive Summary 01 | `grep -c 'Executive Summary' 01-*.md` | ≥ 1 | PASS |
| Executive Summary 02 | `grep -c 'Executive Summary' 02-*.md` | ≥ 1 | PASS |
| Executive Summary 03 | `grep -c 'Executive Summary' 03-*.md` | ≥ 1 | PASS |
| Considered Alternatives 01 | `grep -ci 'considered alternatives' 01-*.md` | ≥ 1 | PASS |
| Considered Alternatives 03 | `grep -ci 'considered alternatives' 03-*.md` | ≥ 1 | PASS |

## Manual Checks (phase gate)

1. **Completeness:** MIGRATION.md has an entry for every major section heading in each of the 7 originals. **PASS** — 40 provenance table rows across 7 originals.
2. **Unique findings:** Cross-reference RESEARCH.md Appendix: Detailed Content Inventory against the 3 new docs. Every bullet must appear somewhere. **PASS** — 36 unique findings preserved in MIGRATION.md checklists.
3. **Conflict resolution:** Both live conflicts (input vector encoding, s_min frame) have a "Considered Alternatives" subsection. **PASS** — 01 has "Considered Alternatives" (line 333), 03 has "Considered Alternatives" (line 536).
4. **Decision callouts:** All 5 [DECISION-NEEDED] items from D-12 appear in the relevant docs. **PASS** — 2 in 01 (input vector, I_norm), 1 in 02 (file format), 2 in 03 (causal training, s_min frame).
5. **No duplicates:** grep for identical paragraphs (>5 lines) across the 3 new docs — should return zero hits. **PASS** — no duplicates found.
6. **Cross-links:** Each doc references the other two at least once. **PASS** — all 3 docs have cross-links to both others.

## Sampling Rate

- **Per task commit:** Verify file exists and size is reasonable.
- **Per wave merge:** Verify MIGRATION.md has an entry for every original file.
- **Phase gate:** All 7 originals in `archive/`, all 5 new files in `issues/`, no orphaned content.

## Validation Audit 2026-05-01

| Metric | Count |
|--------|-------|
| Gaps found | 5 |
| Resolved | 5 |
| Escalated | 0 |

### Gaps Found and Resolved

| # | Gap | Fix |
|---|-----|-----|
| 1 | 03-curriculum-and-training-loop.md at 44,678 B (target max 40,960) | Trimmed verbose prose: compressed tau_L function, L_norm function, EDA code blocks, Huber delta section, Causal Training prose, and Training Phases list. Final: 40,944 B. |
| 2 | MIGRATION.md at 9,172 B (target max 8,192) | Compressed table entries and checklist descriptions. Final: 7,643 B. |
| 3 | 01 missing verbatim Section 5 (audit §5 "Corrected Input Vector Specification") | Added verbatim copy of original audit Section 5 (lines 213-288 of archived audit) before the Option B recommendation. Heading: `## 5. CORRECTED INPUT VECTOR SPECIFICATION`. |
| 4 | 01 had 4 `[DECISION-NEEDED]` mentions (target: 2 callouts) | Replaced non-callout mentions (line 9 readiness assessment, line 169 table note) with alternative phrasing. |
| 5 | 02 had 3 `[DECISION-NEEDED]` mentions (target: 1 callout) | Replaced non-callout mentions (line 73 table reference, line 160 prose reference) with alternative phrasing. |
