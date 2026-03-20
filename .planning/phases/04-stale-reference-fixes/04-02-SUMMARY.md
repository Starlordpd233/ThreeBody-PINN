---
phase: 04-stale-reference-fixes
plan: 02
subsystem: documentation
tags: [docs, cleanup]
dependency_graph:
  requires: [04-01]
  provides: []
  affects: [AGENTS.md, CLAUDE.md, GEMINI.md, ANTIGRAVITY.md, REQUIREMENTS.md]
tech_stack:
  added: []
  patterns: [documentation cleanup, reference updates]
key_files:
  created:
    - .planning/phases/04-stale-reference-fixes/04-02-SUMMARY.md
  modified:
    - AGENTS.md
    - CLAUDE.md
    - GEMINI.md
    - ANTIGRAVITY.md
    - .planning/REQUIREMENTS.md
decisions:
  - "Updated AGENTS.md Section 3.2 to match canonical content from CLAUDE.md, reducing inconsistency across agent instruction files"
  - "Replaced all stale filenames in agent files: FINAL_ic_generator_enhanced.py -> ic_generation_utils.py, generate_enhanced_ics.py -> generate_ics.py"
  - "Marked PATH-06, DOCS-02, DOCS-04 as complete in REQUIREMENTS.md, closing all remaining gaps from previous phases"
metrics:
  duration: 15 minutes
  completed_date: 2026-03-20
---

# Phase 04 Plan 02: Update Agent Instruction Files and REQUIREMENTS.md

## One-liner
Fixed stale filenames and brought AGENTS.md Section 3.2 in line with other agent files, completed all v1 requirements in REQUIREMENTS.md

## Summary

Successfully updated all 4 agent instruction files to fix stale filename references and bring AGENTS.md Section 3.2 in line with the other 3 agent files. Updated REQUIREMENTS.md to mark all remaining v1 requirements as complete.

## Tasks Completed

| Task | Name | Commit | Files |
| ---- | ---- | ------ | ----- |
| 1 | Update AGENTS.md Section 3.2 and fix stale filenames in all 4 agent instruction files | 60865c5 | AGENTS.md, CLAUDE.md, GEMINI.md, ANTIGRAVITY.md |
| 2 | Update REQUIREMENTS.md checkboxes and DOCS-04 description | 3ac8a17 | .planning/REQUIREMENTS.md |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical Functionality] Updated AGENTS.md Section 3.2 to include missing gold IC removal note**
- **Found during:** Task 1
- **Issue:** AGENTS.md Section 3.2 was missing the note about gold IC folders being removed and the IC_RAW_DIR externalization
- **Fix:** Replaced entire Section 3.2 with canonical content from CLAUDE.md that includes all necessary notes
- **Files modified:** AGENTS.md
- **Commit:** 60865c5

**2. [Rule 1 - Bug] Fixed inconsistent dataset inventory between agent files**
- **Found during:** Task 1
- **Issue:** AGENTS.md listed 4 IC folders while other agent files listed 2, causing inconsistency
- **Fix:** Updated AGENTS.md to match the canonical 2-folder layout
- **Files modified:** AGENTS.md
- **Commit:** 60865c5

## Key Changes

### Agent Instruction Files Updates
- **AGENTS.md Section 3.2**: Completely replaced to match canonical content with 2 IC folders, IC_RAW_DIR externalization, and gold-standard subset note
- **All 4 agent files**: Replaced `FINAL_ic_generator_enhanced.py` with `ic_generation_utils.py` and `generate_enhanced_ics.py` with `generate_ics.py`
- **Consistency**: All agent files now have identical Section 3.2 content

### REQUIREMENTS.md Updates
- **PATH-06**: Marked complete (was previously pending due to stale references)
- **DOCS-02**: Marked complete (was previously pending due to stale filenames)
- **DOCS-04**: Marked complete (was previously pending due to AGENTS.md Section 3.2 inconsistency)
- **Traceability table**: Updated all three requirements to show "Complete" status
- **Total v1 requirements**: All 19 requirements now marked as [x] complete

## Impact

- **Documentation consistency**: All 4 agent instruction files now have identical dataset inventory sections
- **Stale reference cleanup**: Eliminated all references to old filename patterns in agent files
- **Requirement completion**: Closed the final gaps in v1 requirements, achieving 100% completion
- **Maintainability**: Future updates to agent instruction files will be consistent across all files

## Verification

- All 4 agent files contain zero references to `FINAL_ic_generator_enhanced` or `generate_enhanced_ics`
- AGENTS.md Section 3.2 matches CLAUDE.md Section 3.2 exactly
- All 19 v1 requirements in REQUIREMENTS.md are marked as [x] complete
- No functional changes to code - only documentation updates

## Next Steps

Phase 04 is now complete. All requirements have been satisfied and the codebase cleanup project milestone is achieved.