---
phase: 09-issues-directory-consolidation
plan: validation
date: "2026-04-27"
---

# Phase 9 Validation Strategy

This is a documentation-only phase. Validation is manual and file-based.

## Automated Checks (per task)

| Check | Command | Pass Criteria |
|-------|---------|---------------|
| File exists | `ls {path}` | Returns without error |
| Size budget | `wc -c issues/01-*.md issues/02-*.md issues/03-*.md` | Total < 120 KB |
| README length | `wc -l issues/README.md` | ≤ 55 lines |
| Archive completeness | `ls issues/archive/` | 7 files present |
| Git history preserved | `git log --follow issues/archive/three_body_pinn_pre-implementation_audit_2026-04-27.md` | Shows pre-move history |
| No orphaned originals | `ls issues/*.md issues/*.txt 2>/dev/null` | Only new docs + next steps.txt (if not archived) |

## Manual Checks (phase gate)

1. **Completeness:** MIGRATION.md has an entry for every major section heading in each of the 7 originals.
2. **Unique findings:** Cross-reference RESEARCH.md Appendix: Detailed Content Inventory against the 3 new docs. Every bullet must appear somewhere.
3. **Conflict resolution:** Both live conflicts (input vector encoding, s_min frame) have a "Considered Alternatives" subsection.
4. **Decision callouts:** All 5 [DECISION-NEEDED] items from D-12 appear in the relevant docs.
5. **No duplicates:** grep for identical paragraphs (>5 lines) across the 3 new docs — should return zero hits.
6. **Cross-links:** Each doc references the other two at least once.

## Sampling Rate

- **Per task commit:** Verify file exists and size is reasonable.
- **Per wave merge:** Verify MIGRATION.md has an entry for every original file.
- **Phase gate:** All 7 originals in `archive/`, all 5 new files in `issues/`, no orphaned content.
