---
phase: 02-documentation-updates
plan: 03
subsystem: agent-instructions
tags: [documentation, dataset-inventory, consistency]
dependency_graph:
  requires: [02-01]
  provides: [DOCS-04]
  affects: [CLAUDE.md, GEMINI.md, QWEN.md, ANTIGRAVITY.md]
tech_stack:
  added: []
  patterns: [identical-section-synchronization]
key_files:
  created: []
  modified:
    - CLAUDE.md
    - GEMINI.md
    - QWEN.md
    - ANTIGRAVITY.md
decisions:
  - Update Section 3.2 to list only 2 base IC folders (removed *_for_gold_standard references)
  - Add ic_raw externalization note with IC_RAW_DIR environment variable
  - Reference 184-ID exclusion file for gold-standard subset documentation
metrics:
  duration_minutes: 5
  completed_date: "2026-03-19"
  task_count: 4
  file_count: 4
---

# Phase 02 Plan 03: Agent Instruction Section 3.2 Update Summary

## One-liner

Updated all 4 agent instruction files with identical Section 3.2 dataset inventory reflecting IC folder consolidation and ic_raw externalization.

## Changes Made

### Task 1: CLAUDE.md Section 3.2 Update
- Replaced 4 IC folder listings with 2 base folders
- Added note explaining gold IC folder removal
- Added ic_raw externalization with IC_RAW_DIR example
- Added reference to 184-ID exclusion file
- Commit: 3fdebe3

### Task 2: GEMINI.md Section 3.2 Update
- Applied identical content as CLAUDE.md
- Verified diff returns empty
- Commit: c0ecca2

### Task 3: QWEN.md Section 3.2 Update
- Applied identical content as CLAUDE.md
- Verified diff returns empty
- Commit: dd69c35

### Task 4: ANTIGRAVITY.md Section 3.2 Update
- Applied identical content as CLAUDE.md
- Verified diff returns empty
- Commit: 8cf8589

## Verification Results

All verification checks passed:

| Check | Result |
|-------|--------|
| CLAUDE.md == GEMINI.md Section 3.2 | PASS (no diff) |
| CLAUDE.md == QWEN.md Section 3.2 | PASS (no diff) |
| CLAUDE.md == ANTIGRAVITY.md Section 3.2 | PASS (no diff) |
| IC_RAW_DIR in all 4 files | PASS (2 occurrences each) |
| Exclusion file reference in all 4 files | PASS (1 occurrence each) |

## Deviations from Plan

None - plan executed exactly as written.

## Files Modified

| File | Lines Changed | Purpose |
|------|---------------|---------|
| CLAUDE.md | +9, -4 | Update Section 3.2 with consolidated dataset inventory |
| GEMINI.md | +9, -4 | Synchronize Section 3.2 with CLAUDE.md |
| QWEN.md | +9, -4 | Synchronize Section 3.2 with CLAUDE.md |
| ANTIGRAVITY.md | +9, -4 | Synchronize Section 3.2 with CLAUDE.md |

## Key Decisions

1. **Section 3.2 consolidation**: All 4 agent instruction files now have identical Section 3.2 content, ensuring consistent dataset inventory information across all AI agents.

2. **IC folder simplification**: Removed references to `*_for_gold_standard` IC folders, reflecting the actual state where gold IC folders have been deleted.

3. **ic_raw externalization documentation**: Added environment variable setup instructions for Stage 1/2 scripts that require external IC storage.

## Self-Check: PASSED

- [x] All 4 files exist at expected paths
- [x] All 4 commits exist in git history
- [x] Section 3.2 content is identical across all files
- [x] IC_RAW_DIR present in all files
- [x] Exclusion file reference present in all files