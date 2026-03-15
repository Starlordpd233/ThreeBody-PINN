# Phase 1 — Pre-existing Bug Fixes (No Directory Moves)

## Goal
Fix known runtime and filename-contract defects before migration, so later verification is meaningful.

## Files to Fix

### 1. `3_Body_Problem/dataset_readiness_checks/config.py` — filename patterns

Lines 65-66 and 73-74 have patterns that don't match actual on-disk filenames.

| Line | Old (broken) | New (matches on-disk files) |
|------|-------------|---------------------------|
| 65 | `"standard": "ic_standard_quasi_random_{num:04d}.txt"` | `"standard": "ic_standard_{num:04d}.txt"` |
| 66 | `"standard_gold": "ic_standard_quasi_random_gold_{num:04d}.txt"` | `"standard_gold": "ic_standard_gold_{num:04d}.txt"` |
| 73 | `"standard": "brutus_standard_quasi_random_{num:04d}.txt"` | `"standard": "brutus_standard_{num:04d}.txt"` |
| 74 | `"standard_gold": "brutus_standard_quasi_random_gold_{num:04d}.txt"` | `"standard_gold": "brutus_standard_gold_{num:04d}.txt"` |

### 2. `pinn/data-handling/core/parsing.py` — dataset-type detection (line 59)

The check looks for `quasirandom` or `quasi-random` in the filename stem, but actual stems are `ic_standard_XXXX` which contain neither substring.

| Line | Old (broken) | New |
|------|-------------|-----|
| 59 | `elif 'quasirandom' in ic_name or 'quasi-random' in ic_name:` | `elif 'standard' in ic_name:` |

### 3. `pinn/data-handling/core/parsing.txt` — mirror the same fix (line 61)

| Line | Old | New |
|------|-----|-----|
| 61 | `elif 'quasirandom' in ic_name or 'quasi-random' in ic_name:` | `elif 'standard' in ic_name:` |

### 4. `3_Body_Problem/dataset_readiness_checks/validator.py` — missing import (line 12)

`run_validation()` at line 346 calls `ValidationConfig()` but only `config` (the instance) is imported.

| Line | Old | New |
|------|-----|-----|
| 12 | `from .config import config` | `from .config import config, ValidationConfig` |

### 5. `3_Body_Problem/dataset_readiness_checks/utils/logging.py` — stale log dir (line 31)

Replace stale default log dir with path relative to the package (works both pre and post migration):

| Line | Old | New |
|------|-----|-----|
| 31 | `self.log_dir = base_dir / "validation_system" / "logs"` | `self.log_dir = Path(__file__).resolve().parent.parent / "logs"` |

### 6. `3_Body_Problem/prescreen_stage2/utilities/compare_thresholds.py` — nonexistent JSON (line 10)

Hardcodes `run_results_2025-06-16T21-27-29.065044.json` which does not exist on disk.

Replace with CLI argument:
```python
import sys
json_file = sys.argv[1] if len(sys.argv) > 1 else None
if not json_file or not os.path.exists(json_file):
    print("Usage: python compare_thresholds.py <path_to_run_results.json>")
    sys.exit(1)
```

### 7. `3_Body_Problem/prescreen_stage2/utilities/example_incremental_workflow.py` — broken paths (lines 84-85)

Scripts are referenced at the repo root, but they live inside `prescreen_stage2/`. Fix to current correct location (Phase 4 will update these again after migration):

| Line | Old (broken) | New (pre-migration correct) |
|------|-------------|---------------------------|
| ~84 | `".../3_Body_Problem/prescreening_utils.py"` | `".../3_Body_Problem/prescreen_stage2/prescreening_utils.py"` |
| ~85 | `".../3_Body_Problem/stage2_prescreening_incremental.py"` | `".../3_Body_Problem/prescreen_stage2/stage2_prescreening_revised_auto.py"` |

## Commit
```bash
cd <home>/Desktop/cursor
git add -A
git commit -m "fix: repair pre-existing parsing/validation/prescreening bugs before migration"
```

## Exit Criteria
- Bugfixes committed independently from migration mechanics.
- No filesystem move has occurred yet.
