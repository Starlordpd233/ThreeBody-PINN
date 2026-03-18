---
phase: 01-code-rewrites-and-validation
plan: 01
subsystem: path-configuration
tags:
  - PATH-02
  - PATH-03
  - PATH-05
  - gold-standard
  - ic-paths
dependency_graph:
  requires: []
  provides:
    - Updated gold IC directory paths in config.py
    - Legacy path comments in naming.py
    - Updated IC_DIR and PROBLEMATIC_DIR in Brutus runner
  affects:
    - simulation_data/Validation/dataset_readiness_checks/
    - simulation_data/Scripts/brutus_runners/
tech_stack:
  added: []
  patterns:
    - Centralized path configuration via config.py
    - Directory-to-variant mapping via naming.py
key_files:
  created: []
  modified:
    - path: simulation_data/Validation/dataset_readiness_checks/config.py
      change: Updated hierarchical_gold and standard_gold ic_dir from _for_gold_standard to base folders
    - path: simulation_data/Validation/dataset_readiness_checks/utils/naming.py
      change: Added legacy path comments to _for_gold_standard directory mappings
    - path: simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py
      change: Updated IC_DIR and PROBLEMATIC_DIR to base folder paths
decisions:
  - "Retained legacy _for_gold_standard mappings in naming.py with Phase 3 deletion comments for backwards compatibility"
  - "Preserved IC and Brutus filename patterns with _gold_ suffix (verified as correct per actual file naming)"
  - "Preserved brutus_dir values (still point to gold_standard output folders)"
metrics:
  duration_seconds: 214
  completed: "2026-03-18T13:30:45Z"
  tasks_completed: 3
  files_modified: 3
  commits_created: 3
---

# Phase 01 Plan 01: Path Configuration Update Summary

## One-liner

Updated gold IC directory paths in config.py, naming.py, and Brutus runner to point to base folders (ic_hierarchical/, ic_standard_quasi_random/) while preserving _gold_ filename patterns and gold Brutus output directories.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Update config.py gold IC directory paths | 8a9d304 | simulation_data/Validation/dataset_readiness_checks/config.py |
| 2 | Update naming.py directory mapping | 6fbd269 | simulation_data/Validation/dataset_readiness_checks/utils/naming.py |
| 3 | Update Brutus runner IC_DIR | 34bf8db | simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py |

## Changes Made

### Task 1: config.py Gold IC Directory Paths

**File:** `simulation_data/Validation/dataset_readiness_checks/config.py`

Changed lines 47-49 (hierarchical_gold):
```python
# Before:
"hierarchical_gold": {
    "ic_dir": "Data/ic_final/ic_hierarchical_for_gold_standard",
    "brutus_dir": "Data/brutus_output/brutus_hierarchical_gold_standard"
}

# After:
"hierarchical_gold": {
    "ic_dir": "Data/ic_final/ic_hierarchical",
    "brutus_dir": "Data/brutus_output/brutus_hierarchical_gold_standard"
}
```

Changed lines 55-57 (standard_gold):
```python
# Before:
"standard_gold": {
    "ic_dir": "Data/ic_final/ic_standard_quasi_random_for_gold_standard",
    "brutus_dir": "Data/brutus_output/brutus_standard_quasi_random_gold_standard"
}

# After:
"standard_gold": {
    "ic_dir": "Data/ic_final/ic_standard_quasi_random",
    "brutus_dir": "Data/brutus_output/brutus_standard_quasi_random_gold_standard"
}
```

**Preserved:**
- IC filename patterns: `ic_hierarchical_gold_{num:04d}.txt` and `ic_standard_gold_{num:04d}.txt`
- Brutus filename patterns: `brutus_hierarchical_gold_{num:04d}.txt` and `brutus_standard_gold_{num:04d}.txt`
- Brutus output directories (still contain "gold_standard")

### Task 2: naming.py Directory Mapping

**File:** `simulation_data/Validation/dataset_readiness_checks/utils/naming.py`

Added legacy path comments to lines 172 and 174:
```python
'ic_hierarchical_for_gold_standard': 'hierarchical_gold',  # Legacy path - Phase 3 deletion
'ic_standard_quasi_random_for_gold_standard': 'standard_gold',  # Legacy path - Phase 3 deletion
```

**Rationale:** Retained for backwards compatibility during transition. Directories exist until Phase 3 deletion.

### Task 3: Brutus Runner Update

**File:** `simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py`

Changed lines 34-36:
```python
# Before:
IC_DIR = PROBLEM_DIR / "Data" / "ic_final" / "ic_hierarchical_for_gold_standard"
OUTPUT_DIR = PROBLEM_DIR / "Data" / "brutus_output" / "brutus_hierarchical_gold_standard"
PROBLEMATIC_DIR = PROBLEM_DIR / "Documentation" / "problematic_ics" / "hierarchical_for_gold_standard"

# After:
IC_DIR = PROBLEM_DIR / "Data" / "ic_final" / "ic_hierarchical"
OUTPUT_DIR = PROBLEM_DIR / "Data" / "brutus_output" / "brutus_hierarchical_gold_standard"
PROBLEMATIC_DIR = PROBLEM_DIR / "Documentation" / "problematic_ics" / "hierarchical"
```

## Verification Results

### PATH-02: config.py gold ic_dir entries updated
```bash
grep -n "ic_dir.*_for_gold_standard" config.py
# Result: Zero matches (PASS)
```

### PATH-03: naming.py mappings
```bash
grep -n "_for_gold_standard" naming.py
# Result: Lines 172, 174 with legacy comments (expected)
```

### PATH-05: Filename patterns retain _gold_
```bash
grep -n "ic_.*_gold_" config.py
# Result: Lines 64, 66 contain _gold_ patterns (PASS)
```

## Deviations from Plan

None - plan executed exactly as written.

## Requirements Progress

This plan addresses:
- **PATH-02**: config.py ic_dir entries for gold variants now point to base folders
- **PATH-03**: naming.py folder-to-name mappings updated with legacy comments
- **PATH-05**: Gold IC filename patterns verified as correct (retain _gold_ suffix)

## Self-Check

### Files Modified Check
- [x] config.py modified and committed (8a9d304)
- [x] naming.py modified and committed (6fbd269)
- [x] run_brutus_hierarchical_only_mac_gold_standard.py modified and committed (34bf8db)

### Verification Commands Check
- [x] config.py has zero _for_gold_standard references in ic_dir values
- [x] naming.py retains _for_gold_standard mappings with Phase 3 deletion comments
- [x] config.py IC patterns still contain _gold_ suffix
- [x] Brutus runner IC_DIR points to base folder

### Git Commits Check
- [x] 8a9d304 exists: feat(01-01): update config.py gold IC directory paths
- [x] 6fbd269 exists: feat(01-01): add legacy path comments to naming.py
- [x] 34bf8db exists: feat(01-01): update gold Brutus runner IC and problematic directory paths

## Self-Check: PASSED
