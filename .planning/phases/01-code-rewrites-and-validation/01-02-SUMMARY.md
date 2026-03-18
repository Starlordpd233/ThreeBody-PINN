---
phase: 01-code-rewrites-and-validation
plan: 02
subsystem: path-resolution
tags: [PATH-04, PATH-06, debug-scripts, ic-generation, prescreening]
requires:
  - 01-01
provides:
  - Base IC folder references in debug scripts
  - IC_RAW_DIR environment variable support in Stage 1/2 scripts
  - Renamed IC generation modules
affects:
  - simulation_data/Scripts/debug/
  - simulation_data/Scripts/ic_generation/
  - simulation_data/Validation/prescreening/
tech-stack:
  patterns:
    - Environment variable configuration pattern
    - Graceful error with usage example
key-files:
  created: []
  modified:
    - simulation_data/Scripts/debug/compare_ic_brutus_files.py
    - simulation_data/Scripts/debug/audit_and_backfill_brutus_result_footers.py
    - simulation_data/Scripts/debug/renaming/rename_ic_hierarchical_gold.py
    - simulation_data/Scripts/debug/renaming/rename_ic_standard_gold.py
    - simulation_data/Scripts/debug/compare_folders.py
    - simulation_data/Scripts/ic_generation/ic_generation_utils.py
    - simulation_data/Scripts/ic_generation/generate_ics.py
    - simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py
    - simulation_data/Validation/prescreening/prescreening_utils.py
    - simulation_data/Validation/prescreening/utilities/example_incremental_workflow.py
decisions:
  - Debug scripts updated to reference base IC folders instead of _for_gold_standard folders
  - IC_RAW_DIR raises RuntimeError with export example when not set (no fallback)
  - IC generation files renamed: FINAL_ic_generator_enhanced.py -> ic_generation_utils.py, generate_enhanced_ics.py -> generate_ics.py
metrics:
  started: 2026-03-18T21:30:00Z
  completed: 2026-03-18T22:00:00Z
  duration_minutes: 30
  tasks_completed: 4
  commits: 5
---

# Phase 01 Plan 02: Path Resolution Updates Summary

**One-liner:** Updated 5 debug scripts to reference base IC folders (PATH-04) and added IC_RAW_DIR environment variable support to Stage 1/2 scripts (PATH-06), plus renamed IC generation modules for clarity.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Update debug scripts IC paths (PATH-04) | c392d05 | 5 debug scripts |
| 2 | Add IC_RAW_DIR to IC generator (PATH-06) | 7bfee32 | ic_generation_utils.py |
| 3 | Add IC_RAW_DIR to prescreening scripts (PATH-06) | beae23e | 3 prescreening scripts |
| 4 | Rename IC generation files | 16d1b89 | 2 files renamed |
| - | Fix prescreening_utils.py fallback | 9c0fb95 | prescreening_utils.py |

## Implementation Details

### PATH-04: Debug Scripts Base Path Updates

All five debug scripts now reference base IC folders instead of `_for_gold_standard` folders:

1. **rename_ic_hierarchical_gold.py**: `ic_hierarchical` instead of `ic_hierarchical_for_gold_standard`
2. **rename_ic_standard_gold.py**: `ic_standard_quasi_random` instead of `ic_standard_quasi_random_for_gold_standard`
3. **compare_ic_brutus_files.py**: `ic_dir` points to `ic_hierarchical` base folder
4. **compare_folders.py**: `folder2` points to `problematic_ics/hierarchical`
5. **audit_and_backfill_brutus_result_footers.py**: `ic_dir_map` uses base folders for all variants

**Verification:** `grep -rn "_for_gold_standard" simulation_data/Scripts/debug/` returns zero matches.

### PATH-06: IC_RAW_DIR Environment Variable

Three script groups now use `IC_RAW_DIR` environment variable:

**IC Generation (ic_generation_utils.py):**
```python
IC_RAW_DIR = os.environ.get('IC_RAW_DIR')
if IC_RAW_DIR is None:
    raise RuntimeError(
        "IC_RAW_DIR environment variable not set. "
        "This script requires an external ic_raw directory with "
        "ic_hierarchical/ and ic_standard_quasi_random/ subdirectories.\n"
        "Example: export IC_RAW_DIR=/path/to/ic_raw"
    )
```

**Prescreening (stage2_prescreening_revised_auto.py):**
```python
DATASET_CONFIGS = [
    {
        'name': 'ic_hierarchical',
        'input_dir': os.path.join(IC_RAW_DIR, 'ic_hierarchical'),
        'output_dir': "simulation_data/Data/ic_final/ic_hierarchical",
    },
    ...
]
```

**Prescreening Utilities (prescreening_utils.py, example_incremental_workflow.py):**
- Same error handling pattern
- Uses `os.path.join(IC_RAW_DIR, 'ic_standard_quasi_random')`

**Verification:** `grep -rn "<home>/.*/ic_raw/"` returns zero matches in `.py` files.

### File Renaming

Per CONTEXT.md decision "IC Generation File Renaming":

| Old Name | New Name | Purpose |
|----------|----------|---------|
| `FINAL_ic_generator_enhanced.py` | `ic_generation_utils.py` | Core utilities/library |
| `generate_enhanced_ics.py` | `generate_ics.py` | Runner/entry point |

Import in `generate_ics.py` updated:
```python
from ic_generation_utils import continuation_enhanced_ic_generation
```

## Deviations from Plan

None - plan executed exactly as written.

## Verification Results

```bash
# PATH-04: Debug scripts use base paths
$ grep -rn "_for_gold_standard" simulation_data/Scripts/debug/
# Result: Zero matches (PASS)

# PATH-06: IC_RAW_DIR usage
$ grep -n "IC_RAW_DIR" simulation_data/Scripts/ic_generation/*.py simulation_data/Validation/prescreening/*.py
# Result: IC_RAW_DIR references in ic_generation_utils.py, stage2_prescreening_revised_auto.py, prescreening_utils.py, example_incremental_workflow.py (PASS)

# PATH-06: No hardcoded ic_raw paths
$ grep -rn "<home>/.*/ic_raw/" simulation_data/Scripts/ic_generation/ simulation_data/Validation/prescreening/
# Result: Zero matches in .py files (PASS)
```

## Commits

- `c392d05`: fix(01-02): update debug scripts to reference base IC folders (PATH-04)
- `7bfee32`: feat(01-02): add IC_RAW_DIR env var to IC generator (PATH-06)
- `beae23e`: feat(01-02): add IC_RAW_DIR env var to prescreening scripts (PATH-06)
- `16d1b89`: chore(01-02): rename IC generation files for clarity
- `9c0fb95`: fix(01-02): prescreening_utils.py should raise error if IC_RAW_DIR missing

## Self-Check

**Files modified exist:** All 10 files confirmed modified via git status.

**Commits exist:** All 5 commits verified via git log.

**Verification passed:** All grep commands return expected results.

**Self-Check: PASSED**
