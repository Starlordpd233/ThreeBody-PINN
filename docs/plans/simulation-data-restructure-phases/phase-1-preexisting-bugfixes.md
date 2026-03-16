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
import os
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

### 8. `3_Body_Problem/dataset_readiness_checks/validator.py` — `run_validation()` ignores `--modules`

`run_validation()` creates a fresh `ValidationConfig()` at line 346, discarding any `enabled_modules` set via CLI. Add a `modules` parameter and propagate it.

**Changes to `run_validation()` signature (line ~331):**

| Change | Details |
|--------|---------|
| Add parameter | `modules: Optional[List[str]] = None` |
| After `validation_config = ValidationConfig()` | Add: `if modules: validation_config.enabled_modules = modules` |

**Changes to `__main__.py` (line 47):**

| Line | Old | New |
|------|-----|-----|
| 47 | `run_validation(variants=args.variants, output_dir=output_dir, threshold=args.threshold)` | `run_validation(variants=args.variants, output_dir=output_dir, threshold=args.threshold, modules=config.enabled_modules if args.modules else None)` |

### 9. `3_Body_Problem/dataset_readiness_checks/validator.py` — metrics filename pattern (line 226)

| Line | Old | New |
|------|-----|-----|
| 226 | `metrics_file = self.config.get_metrics_dir(variant) / f"{variant}_{file_number:04d}.json"` | `metrics_file = self.config.get_metrics_dir(variant) / f"metrics_{variant}_{file_number:04d}.json"` |

### 10. `3_Body_Problem/dataset_readiness_checks/modules/metrics.py` — key schema mismatch (lines 22-38)

The actual metrics JSON has this structure (verified from `metrics_standard_0000.json`):
```json
{
  "conservation": {
    "energy": {
      "initial": ..., "final": ...,
      "absolute_error": ..., "relative_error": ...,
      "conservation_quality": "excellent"
    },
    "linear_momentum": {
      "initial_magnitude": ..., "final_magnitude": ...,
      "absolute_error": ..., "relative_error": ...,
      "conservation_quality": "excellent"
    },
    "angular_momentum": { "...same pattern..." }
  },
  "timing": { "simulation_time": ..., "cpu_time_seconds": ..., "..." },
  "detection": { "possible_escape": ..., "possible_collision": ..., "..." },
  "..."
}
```

Replace the flat key checks (lines 22-38) with:
```python
# Check required nested keys
conservation = data.get('conservation', {})
energy = conservation.get('energy', {})
momentum = conservation.get('linear_momentum', {})

if not energy:
    issues.append(create_issue(
        "missing_metric_key", ValidationStatus.WARNING, "metrics",
        "Missing conservation.energy section", str(metrics_path)
    ))
if not momentum:
    issues.append(create_issue(
        "missing_metric_key", ValidationStatus.WARNING, "metrics",
        "Missing conservation.linear_momentum section", str(metrics_path)
    ))

# Basic sanity check on energy conservation
if 'relative_error' in energy:
    rel_err = abs(energy['relative_error'])
    if rel_err > 1.0:
        issues.append(create_issue(
            "extreme_energy_drift", ValidationStatus.WARNING, "metrics",
            f"Extreme energy relative error: {rel_err:.4e}", str(metrics_path)
        ))
```

## Commit
```bash
cd <home>/Desktop/cursor
git add -A
git commit -m "fix: repair pre-existing parsing/validation/prescreening bugs before migration"
```

## Exit Criteria
- Bugfixes committed independently from migration mechanics.
- No filesystem move has occurred yet.
