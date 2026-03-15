# Phase 4 — Path Rewrites + Documentation Updates

## Goal
Update hardcoded `3_Body_Problem` references after files are moved, then update documentation references.

## Safeguards
- Update code paths first, docs second.
- Keep filename-contract fixes from Phase 1 intact (do NOT revert `ic_patterns`/`brutus_patterns`).
- Confirm no accidental revert of Phase 1 bug fixes.
- After each file edit, verify the change makes sense at the new file location.

## Path Substitution Reference

| Old subpath | New subpath |
|-------------|-------------|
| `3_Body_Problem` | `simulation_data` |
| `final_stage_ic_datasets` | `Data/ic_final` |
| `ic_raw_datasets` | `Data/ic_raw` |
| `brutus_output` (data dirs) | `Data/brutus_output` |
| `brutus_metrics` (data dirs) | `Data/metrics` |
| `problematic_ics` | `Documentation/problematic_ics` |
| `problematic_ics_blacklist.json` | `Documentation/problematic_ics_blacklist.json` |
| `testing_data` | `Data/testing_data` |
| `prescreen_stage2` | `Validation/prescreening` |
| `dataset_readiness_checks` | `Validation/dataset_readiness_checks` |
| `analyze_data_generation` | `Validation/analysis` |
| `debug_scripts` | `Scripts/debug` |

---

## 4.1 CRITICAL — `config.py` (highest priority, most changes)

**File:** `simulation_data/Validation/dataset_readiness_checks/config.py`

This file moved from depth-2 (`3_Body_Problem/dataset_readiness_checks/config.py`) to depth-3 (`simulation_data/Validation/dataset_readiness_checks/config.py`). The `base_dir` derivation MUST add one more `.parent`.

| Line | Old | New | Why |
|------|-----|-----|-----|
| 16 | `base_dir: Path = Path(__file__).resolve().parent.parent` | `base_dir: Path = Path(__file__).resolve().parent.parent.parent` | Extra nesting level after move |
| 44 | `"ic_dir": "final_stage_ic_datasets/ic_hierarchical"` | `"ic_dir": "Data/ic_final/ic_hierarchical"` | Data subpath changed |
| 45 | `"brutus_dir": "brutus_output/brutus_hierarchical"` | `"brutus_dir": "Data/brutus_output/brutus_hierarchical"` | |
| 48 | `"ic_dir": "final_stage_ic_datasets/ic_hierarchical_for_gold_standard"` | `"ic_dir": "Data/ic_final/ic_hierarchical_for_gold_standard"` | |
| 49 | `"brutus_dir": "brutus_output/brutus_hierarchical_gold_standard"` | `"brutus_dir": "Data/brutus_output/brutus_hierarchical_gold_standard"` | |
| 52 | `"ic_dir": "final_stage_ic_datasets/ic_standard_quasi_random"` | `"ic_dir": "Data/ic_final/ic_standard_quasi_random"` | |
| 53 | `"brutus_dir": "brutus_output/brutus_standard_quasi_random"` | `"brutus_dir": "Data/brutus_output/brutus_standard_quasi_random"` | |
| 56 | `"ic_dir": "final_stage_ic_datasets/ic_standard_quasi_random_for_gold_standard"` | `"ic_dir": "Data/ic_final/ic_standard_quasi_random_for_gold_standard"` | |
| 57 | `"brutus_dir": "brutus_output/brutus_standard_quasi_random_gold_standard"` | `"brutus_dir": "Data/brutus_output/brutus_standard_quasi_random_gold_standard"` | |
| 94 | `self.base_dir / "dataset_readiness_checks" / "reports"` | `self.base_dir / "Validation" / "dataset_readiness_checks" / "reports"` | Relative path to reports changed |
| 134 | `self.base_dir / "brutus_metrics" / variant_to_metrics[variant]` | `self.base_dir / "Data" / "metrics" / variant_to_metrics[variant]` | Metrics data relocated |
| 139 | `self.base_dir / "problematic_ics_blacklist.json"` | `self.base_dir / "Documentation" / "problematic_ics_blacklist.json"` | Blacklist relocated |

**Note:** `ic_patterns` and `brutus_patterns` (lines 61-75) were already fixed in Phase 1. Do NOT touch those lines here.

---

## 4.2 CRITICAL — Brutus runner scripts

### `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py`

| Line | Old | New |
|------|-----|-----|
| 32 | `BASE_DIR = Path("<home>/Desktop/cursor/3_Body_Problem")` | `BASE_DIR = Path("<home>/Desktop/cursor/simulation_data")` |
| 37 | `BASE_DIR / "final_stage_ic_datasets" / "ic_hierarchical"` | `BASE_DIR / "Data" / "ic_final" / "ic_hierarchical"` |
| 38 | `BASE_DIR / "final_stage_ic_datasets" / "ic_standard_quasi_random"` | `BASE_DIR / "Data" / "ic_final" / "ic_standard_quasi_random"` |
| 41 | `BASE_DIR / "brutus_output" / "brutus_hierarchical"` | `BASE_DIR / "Data" / "brutus_output" / "brutus_hierarchical"` |
| 42 | `BASE_DIR / "brutus_output" / "brutus_standard_quasi_random"` | `BASE_DIR / "Data" / "brutus_output" / "brutus_standard_quasi_random"` |
| 47 | `BASE_DIR / "problematic_ics" / "hierarchical"` | `BASE_DIR / "Documentation" / "problematic_ics" / "hierarchical"` |
| 48 | `BASE_DIR / "problematic_ics" / "standard"` | `BASE_DIR / "Documentation" / "problematic_ics" / "standard"` |

### `simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py`

| Line | Old | New |
|------|-----|-----|
| 31 | `PROBLEM_DIR = BASE_DIR / "3_Body_Problem"` | `PROBLEM_DIR = BASE_DIR / "simulation_data"` |
| 34 | `PROBLEM_DIR / "final_stage_ic_datasets" / "ic_hierarchical_for_gold_standard"` | `PROBLEM_DIR / "Data" / "ic_final" / "ic_hierarchical_for_gold_standard"` |
| 35 | `PROBLEM_DIR / "brutus_output" / "brutus_hierarchical_gold_standard"` | `PROBLEM_DIR / "Data" / "brutus_output" / "brutus_hierarchical_gold_standard"` |
| 36 | `PROBLEM_DIR / "problematic_ics" / "hierarchical_for_gold_standard"` | `PROBLEM_DIR / "Documentation" / "problematic_ics" / "hierarchical_for_gold_standard"` |

---

## 4.3 CRITICAL — Metrics calculation scripts

### `simulation_data/Scripts/metrics_calculation/calculate_metrics.py`

| Line | Old | New |
|------|-----|-----|
| 17 | `PROBLEM_DIR = BASE_DIR / "3_Body_Problem"` | `PROBLEM_DIR = BASE_DIR / "simulation_data"` |
| 21 | `PROBLEM_DIR / "brutus_output" / "brutus_hierarchical"` | `PROBLEM_DIR / "Data" / "brutus_output" / "brutus_hierarchical"` |
| 22 | `PROBLEM_DIR / "brutus_output" / "brutus_hierarchical_gold_standard"` | `PROBLEM_DIR / "Data" / "brutus_output" / "brutus_hierarchical_gold_standard"` |
| 23 | `PROBLEM_DIR / "brutus_output" / "brutus_standard_quasi_random"` | `PROBLEM_DIR / "Data" / "brutus_output" / "brutus_standard_quasi_random"` |
| 24 | `PROBLEM_DIR / "brutus_output" / "brutus_standard_quasi_random_gold_standard"` | `PROBLEM_DIR / "Data" / "brutus_output" / "brutus_standard_quasi_random_gold_standard"` |
| 28 | `PROBLEM_DIR / "brutus_metrics" / "sim_result_metric_hierarchical"` | `PROBLEM_DIR / "Data" / "metrics" / "sim_result_metric_hierarchical"` |
| 29 | `PROBLEM_DIR / "brutus_metrics" / "sim_result_metric_hierarchical_gold_standard"` | `PROBLEM_DIR / "Data" / "metrics" / "sim_result_metric_hierarchical_gold_standard"` |
| 30 | `PROBLEM_DIR / "brutus_metrics" / "sim_result_metric_standard"` | `PROBLEM_DIR / "Data" / "metrics" / "sim_result_metric_standard"` |
| 31 | `PROBLEM_DIR / "brutus_metrics" / "sim_result_metric_standard_gold_standard"` | `PROBLEM_DIR / "Data" / "metrics" / "sim_result_metric_standard_gold_standard"` |

### `simulation_data/Scripts/metrics_calculation/calculate_brutus_metrics.py`

| Line | Old | New |
|------|-----|-----|
| 18 | `PROBLEM_DIR = BASE_DIR / "3_Body_Problem"` | `PROBLEM_DIR = BASE_DIR / "simulation_data"` |
| 22 | `PROBLEM_DIR / "brutus_output" / "brutus_hierarchical"` | `PROBLEM_DIR / "Data" / "brutus_output" / "brutus_hierarchical"` |
| 23 | `PROBLEM_DIR / "brutus_output" / "brutus_standard_quasi_random"` | `PROBLEM_DIR / "Data" / "brutus_output" / "brutus_standard_quasi_random"` |
| 27 | `PROBLEM_DIR / "sim_result_metric_hierarchical"` | `PROBLEM_DIR / "Data" / "metrics" / "sim_result_metric_hierarchical"` |
| 28 | `PROBLEM_DIR / "sim_result_metric_standard"` | `PROBLEM_DIR / "Data" / "metrics" / "sim_result_metric_standard"` |

---

## 4.4 HIGH — PINN parser (external, outside simulation_data/)

### `pinn/data-handling/core/parsing.py` (absolute paths)

| Line | Old | New |
|------|-----|-----|
| 38 | `Path("<home>/Desktop/cursor/3_Body_Problem/final_stage_ic_datasets/ic_hierarchical")` | `Path("<home>/Desktop/cursor/simulation_data/Data/ic_final/ic_hierarchical")` |
| 39 | `Path("<home>/Desktop/cursor/3_Body_Problem/brutus_output/brutus_hierarchical")` | `Path("<home>/Desktop/cursor/simulation_data/Data/brutus_output/brutus_hierarchical")` |

**Note:** The `detect_simulation_metadata` dataset-type detection was already fixed in Phase 1. Do NOT touch lines 57-62 here.

### `pinn/data-handling/core/parsing.txt` (relative paths)

| Line | Old | New |
|------|-----|-----|
| 41 | `Path("../../../3_Body_Problem/final_stage_ic_datasets/ic_hierarchical")` | `Path("../../../simulation_data/Data/ic_final/ic_hierarchical")` |
| 42 | `Path("../../../3_Body_Problem/brutus_output/brutus_hierarchical")` | `Path("../../../simulation_data/Data/brutus_output/brutus_hierarchical")` |

---

## 4.5 HIGH — Prescreening scripts

### `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py`

| Line | Old | New |
|------|-----|-----|
| 42 | `'input_dir': ".../3_Body_Problem/ic_raw_datasets/ic_hierarchical"` | `'input_dir': ".../simulation_data/Data/ic_raw/ic_hierarchical"` |
| 43 | `'output_dir': ".../3_Body_Problem/final_stage_ic_datasets/ic_hierarchical"` | `'output_dir': ".../simulation_data/Data/ic_final/ic_hierarchical"` |
| 47 | `'input_dir': ".../3_Body_Problem/ic_raw_datasets/ic_standard_quasi_random"` | `'input_dir': ".../simulation_data/Data/ic_raw/ic_standard_quasi_random"` |
| 48 | `'output_dir': ".../3_Body_Problem/final_stage_ic_datasets/ic_standard_quasi_random"` | `'output_dir': ".../simulation_data/Data/ic_final/ic_standard_quasi_random"` |
| 422 | `os.path.join(".../3_Body_Problem/prescreen_stage2", ...)` | `os.path.join(".../simulation_data/Validation/prescreening/prescreening_data", ...)` |
| 649 | `".../3_Body_Problem/prescreen_stage2/prescreen_run_results"` | `".../simulation_data/Validation/prescreening/prescreening_data/prescreen_run_results"` |

### `simulation_data/Validation/prescreening/prescreening_utils.py`

| Line | Old | New |
|------|-----|-----|
| ~209 | `default_output_dir = ".../3_Body_Problem/ic_prescreened"` | `default_output_dir = ".../simulation_data/Data/ic_final"` |
| ~211 | `default_input_dir = ".../3_Body_Problem/ic_raw_datasets/ic_standard_quasi_random"` | `default_input_dir = ".../simulation_data/Data/ic_raw/ic_standard_quasi_random"` |

---

## 4.6 HIGH — IC generation scripts

### `simulation_data/Scripts/ic_generation/generate_enhanced_ics.py`

| Line | Old | New |
|------|-----|-----|
| 8 | `sys.path.append('<home>/Desktop/cursor/3_Body_Problem')` | **DELETE this line** — both files are now in the same directory (`Scripts/ic_generation/`), so no sys.path hack is needed |

### `simulation_data/Scripts/ic_generation/FINAL_ic_generator_enhanced.py`

| Line | Old | New |
|------|-----|-----|
| 11 | Docstring: `.../3_Body_Problem/testing_data/single_ic.txt > .../3_Body_Problem/testing_data/test_output.txt` | Update to `.../simulation_data/Data/testing_data/...` |
| 14 | Docstring: (same pattern) | (same substitution) |
| 290 | `output_dir: str = "3_Body_Problem/ic_raw_datasets/ic_hierarchical"` | `output_dir: str = "simulation_data/Data/ic_raw/ic_hierarchical"` |
| 596 | `directory = "<home>/Desktop/cursor/3_Body_Problem/ic_raw_datasets/ic_hierarchical"` | `directory = "<home>/Desktop/cursor/simulation_data/Data/ic_raw/ic_hierarchical"` |
| 599 | `directory = "<home>/Desktop/cursor/3_Body_Problem/ic_raw_datasets/ic_standard_quasi_random"` | `directory = "<home>/Desktop/cursor/simulation_data/Data/ic_raw/ic_standard_quasi_random"` |

---

## 4.7 MEDIUM — Debug scripts

### `simulation_data/Scripts/debug/audit_and_backfill_brutus_result_footers.py`

| Line | Old | New |
|------|-----|-----|
| 247 | `base_dir = Path('<home>/Desktop/cursor/3_Body_Problem/final_stage_ic_datasets')` | `base_dir = Path('<home>/Desktop/cursor/simulation_data/Data/ic_final')` |
| 667 | `base_dir = '<home>/Desktop/cursor/3_Body_Problem/brutus_output'` | `base_dir = '<home>/Desktop/cursor/simulation_data/Data/brutus_output'` |
| ~699 | `output_dir = Path(base_dir) / 'check missing results line'` | `output_dir = Path('<home>/Desktop/cursor/simulation_data/Validation/audit_reports')` |

### `simulation_data/Scripts/debug/compare_ic_brutus_files.py`

| Line | Old | New |
|------|-----|-----|
| 32 | `ic_dir = "<home>/Desktop/cursor/3_Body_Problem/final_stage_ic_datasets/ic_hierarchical_for_gold_standard"` | `ic_dir = "<home>/Desktop/cursor/simulation_data/Data/ic_final/ic_hierarchical_for_gold_standard"` |
| 33 | `brutus_dir = "<home>/Desktop/cursor/3_Body_Problem/brutus_output/brutus_hierarchical_gold_standard"` | `brutus_dir = "<home>/Desktop/cursor/simulation_data/Data/brutus_output/brutus_hierarchical_gold_standard"` |

### `simulation_data/Scripts/debug/check_brutus_completeness.py`

| Line | Old | New |
|------|-----|-----|
| 94 | `BRUTUS_OUTPUT_DIR = "<home>/Desktop/cursor/3_Body_Problem/brutus_output/brutus_standard_quasi_random"` | `BRUTUS_OUTPUT_DIR = "<home>/Desktop/cursor/simulation_data/Data/brutus_output/brutus_standard_quasi_random"` |

### `simulation_data/Scripts/debug/compare_folders.py`

| Line | Old | New |
|------|-----|-----|
| 142 | `folder1 = "<home>/Desktop/cursor/3_Body_Problem/problematic_ics/hierarchical"` | `folder1 = "<home>/Desktop/cursor/simulation_data/Documentation/problematic_ics/hierarchical"` |
| 143 | `folder2 = "<home>/Desktop/cursor/3_Body_Problem/problematic_ics/hierarchical_for_gold_standard"` | `folder2 = "<home>/Desktop/cursor/simulation_data/Documentation/problematic_ics/hierarchical_for_gold_standard"` |

### `simulation_data/Scripts/debug/renaming/` (4 files — same pattern)

Each renaming script has a `folder_path` variable at line 5:

| File | Old | New |
|------|-----|-----|
| `rename_ic_hierarchical_gold.py:5` | `"<home>/Desktop/cursor/3_Body_Problem/final_stage_ic_datasets/ic_hierarchical_for_gold_standard"` | `"<home>/Desktop/cursor/simulation_data/Data/ic_final/ic_hierarchical_for_gold_standard"` |
| `rename_ic_standard_gold.py:5` | `"<home>/Desktop/cursor/3_Body_Problem/final_stage_ic_datasets/ic_standard_quasi_random_for_gold_standard"` | `"<home>/Desktop/cursor/simulation_data/Data/ic_final/ic_standard_quasi_random_for_gold_standard"` |
| `rename_brutus_hierarchical_gold.py:5` | `"<home>/Desktop/cursor/3_Body_Problem/brutus_output/brutus_hierarchical_gold_standard"` | `"<home>/Desktop/cursor/simulation_data/Data/brutus_output/brutus_hierarchical_gold_standard"` |
| `rename_brutus_standard_gold.py:5` | `"<home>/Desktop/cursor/3_Body_Problem/brutus_output/brutus_standard_quasi_random_gold_standard"` | `"<home>/Desktop/cursor/simulation_data/Data/brutus_output/brutus_standard_quasi_random_gold_standard"` |

---

## 4.8 MEDIUM — Prescreening utilities

### `simulation_data/Validation/prescreening/utilities/create_initial_indices.py`

| Line | Old | New |
|------|-----|-----|
| 14 | `base_dir = "<home>/Desktop/cursor/3_Body_Problem/prescreen_stage2"` | `base_dir = "<home>/Desktop/cursor/simulation_data/Validation/prescreening/prescreening_data"` |

### `simulation_data/Validation/prescreening/utilities/migrate_processing_index.py`

| Line | Old | New |
|------|-----|-----|
| 15 | `existing_index_path = ".../3_Body_Problem/prescreen_stage2/processing_index.json"` | `existing_index_path = ".../simulation_data/Validation/prescreening/prescreening_data/processing_index.json"` |
| 51 | `hierarchical_output = ".../3_Body_Problem/final_stage_ic_datasets/ic_hierarchical"` | `hierarchical_output = ".../simulation_data/Data/ic_final/ic_hierarchical"` |
| 52 | `standard_output = ".../3_Body_Problem/final_stage_ic_datasets/ic_standard_quasi_random"` | `standard_output = ".../simulation_data/Data/ic_final/ic_standard_quasi_random"` |
| 92 | `hierarchical_path = ".../3_Body_Problem/prescreen_stage2/processing_index_ic_hierarchical.json"` | `hierarchical_path = ".../simulation_data/Validation/prescreening/prescreening_data/processing_index_ic_hierarchical.json"` |
| 93 | `standard_path = ".../3_Body_Problem/prescreen_stage2/processing_index_ic_standard_quasi_random.json"` | `standard_path = ".../simulation_data/Validation/prescreening/prescreening_data/processing_index_ic_standard_quasi_random.json"` |

### `simulation_data/Validation/prescreening/utilities/example_incremental_workflow.py`

| Line | Old | New |
|------|-----|-----|
| 13 | `raw_dir = "<home>/Desktop/cursor/3_Body_Problem/ic_raw_datasets/ic_standard_quasi_random"` | `raw_dir = "<home>/Desktop/cursor/simulation_data/Data/ic_raw/ic_standard_quasi_random"` |
| 84 | (fixed in Phase 1 to `prescreen_stage2/prescreening_utils.py`) | `"<home>/Desktop/cursor/simulation_data/Validation/prescreening/prescreening_utils.py"` |
| 85 | (fixed in Phase 1 to `prescreen_stage2/stage2_prescreening_revised_auto.py`) | `"<home>/Desktop/cursor/simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py"` |

---

## 4.9 MEDIUM — Analysis scripts

### `simulation_data/Validation/analysis/prescreening_analysis/` (5 files)

All 5 files follow the same pattern. Update in each:

| File | Lines | Old | New |
|------|-------|-----|-----|
| `analyze.py` | ~525-526 | `results_dir = "3_Body_Problem/prescreen_stage2/prescreen_run_results"` | `results_dir = "simulation_data/Validation/prescreening/prescreening_data/prescreen_run_results"` |
| | | `output_dir = "3_Body_Problem/prescreen_stage2/analysis_output"` | `output_dir = "simulation_data/Validation/analysis/figures/prescreening"` |
| `analyze_prescreening.py` | ~230-231 | (same pattern) | (same substitution) |
| `analyze_prescreening_new.py` | ~342-343 | (same pattern) | (same substitution) |
| `analyze_prescreening_v2.py` | ~308-309 | (same pattern) | (same substitution) |
| `analyze_threshold_failures.py` | ~157-158 | (same pattern) | (same substitution) |

### `simulation_data/Validation/analysis/metrics_analysis.py`

| Line | Old | New |
|------|-----|-----|
| ~5-8 | Docstring: `3_Body_Problem/analyze_data_generation/metrics_analysis.py` | `simulation_data/Validation/analysis/metrics_analysis.py` |
| ~40 | `output_path = '.../3_Body_Problem/analyze_data_generation/figures/metrics_analysis/...'` | `output_path = '.../simulation_data/Validation/analysis/figures/metrics_analysis/...'` |
| ~74 | (same pattern for pos2 heatmap) | (same substitution) |
| ~106 | (same pattern for scatter) | (same substitution) |
| ~120 | `folder default = '.../3_Body_Problem/sim_result_metric_hierarchical'` | `folder default = '.../simulation_data/Data/metrics/sim_result_metric_hierarchical'` |

### `simulation_data/Validation/analysis/particle_positions_viz.py`

| Line | Old | New |
|------|-----|-----|
| ~367 | `ic_dir = ".../3_Body_Problem/final_stage_ic_datasets/ic_hierarchical"` | `ic_dir = ".../simulation_data/Data/ic_final/ic_hierarchical"` |
| ~368 | `output_dir = ".../3_Body_Problem/analyze_data_generation/figures/hierarchical_positions"` | `output_dir = ".../simulation_data/Validation/analysis/figures/hierarchical_positions"` |

### `simulation_data/Validation/analysis/reference_plane_viz.py`

| Line | Old | New |
|------|-----|-----|
| ~454 | `output_dir = ".../3_Body_Problem/analyze_data_generation/figures/reference_plane"` | `output_dir = ".../simulation_data/Validation/analysis/figures/reference_plane"` |

### `simulation_data/Validation/analysis/utils.py`

| Line | Old | New |
|------|-----|-----|
| ~158 | Comment referencing `3_Body_Problem/{sim_result_metric_..., ic_raw_datasets}/` | Update to `.../simulation_data/{Data/metrics/..., Data/ic_raw/}` |
| ~169 | `'ic_raw_datasets'` in `os.path.join(...)` | `os.path.join(base_project_path, 'Data', 'ic_raw', ic_dir, ic_filename)` |
| ~501 | `ic_base_dir: str = '.../3_Body_Problem/ic_raw_datasets/ic_hierarchical/'` | `ic_base_dir: str = '.../simulation_data/Data/ic_raw/ic_hierarchical/'` |

---

## 4.10 MEDIUM — Audit report scripts

### `simulation_data/Validation/audit_reports/check_missing_results.py`

Uses relative directory names assuming CWD is `brutus_output/`. After moving to `audit_reports/`, it needs an absolute base_dir.

**Add** at top of `main()`:
```python
base_dir = "<home>/Desktop/cursor/simulation_data/Data/brutus_output"
```
Then update glob patterns: `pattern = os.path.join(base_dir, folder, '*.txt')`

### `simulation_data/Validation/audit_reports/check_missing_results_detailed.py`

Same fix as above. Add `base_dir` and update glob patterns.

---

## 4.11 LOW — Archived scripts (not in active use)

### `simulation_data/Scripts/archived/manage_problematic_ics_notusing.py`

| Line | Old | New |
|------|-----|-----|
| ~20 | `BASE_DIR = Path(".../3_Body_Problem")` | `BASE_DIR = Path(".../simulation_data")` |
| + | All `final_stage_ic_datasets`, `brutus_output`, `problematic_ics` refs | Update per substitution table |

### `simulation_data/Scripts/archived/visualize_test_brutus.py`

| Line | Old | New |
|------|-----|-----|
| ~310 | `filename = '.../3_Body_Problem/brutus_output/brutus_hierarchical_gold_standard/brutus_hierarchical_4951.txt'` | `filename = '.../simulation_data/Data/brutus_output/brutus_hierarchical_gold_standard/brutus_hierarchical_4951.txt'` |

### `simulation_data/Scripts/archived/analyze_metrics_not_sure_if_using.py`

| Line | Old | New |
|------|-----|-----|
| (check) | `BASE_DIR = Path(".../3_Body_Problem")` | `BASE_DIR = Path(".../simulation_data")` |
| + | Internal refs to `brutus_metrics` data dirs | Update per substitution table |

---

## 4.12 Completeness check

After all edits, run a quick scan to catch any missed references:
```bash
cd <home>/Desktop/cursor
rg "3_Body_Problem" --type py -l \
  --glob '!.git/*' \
  --glob '!brutus_simulation_documentation/*'
```

If any files appear, update them before committing.

---

## 4.13 Documentation update scope

Update existing files only (exclude deleted files):
- `simulation_data/Documentation/README.md`
- `simulation_data/Documentation/DATASET_DOCUMENTATION.md`
- `<home>/Desktop/cursor/README.md`
- `<home>/Desktop/cursor/CLAUDE.md`
- `<home>/Desktop/cursor/ANTIGRAVITY.md`
- `<home>/Desktop/cursor/GEMINI.md`
- `<home>/Desktop/cursor/QWEN.md`
- `<home>/Desktop/cursor/docs/plans/2026-03-09-data-documentation-readme.md`
- `<home>/Desktop/cursor/paper_templates/mdpi_template/paper.tex` — figure paths (e.g., `3_Body_Problem/analyze_data_generation/figures/...` → `simulation_data/Validation/analysis/figures/...`)
- `<home>/Desktop/cursor/paper_templates/old_templates/temp_v2.tex` — same figure path pattern

Do **not** include currently deleted paths:
- `<home>/Desktop/cursor/plan.md` (deleted)
- `<home>/Desktop/cursor/dataset_readiness_checks_b73004bc.plan.md` (deleted)

---

## 4.14 Commit code rewrites
```bash
cd <home>/Desktop/cursor
git add -A
git commit -m "fix: update hardcoded paths from 3_Body_Problem to simulation_data"
```

## 4.15 Commit docs rewrites
```bash
cd <home>/Desktop/cursor
git add -A
git commit -m "docs: update path references for simulation_data migration"
```

---

## Exit Criteria
- All Python path rewrites committed with explicit staging.
- `config.py` `base_dir` uses `parent.parent.parent` (verified).
- `config.py` `output_dir`, `get_metrics_dir`, and `get_blacklist_ids` point to new subpaths.
- Phase 1 filename-contract fixes (`ic_patterns`, `brutus_patterns`, parsing.py detection) are intact.
- Doc updates committed with explicit staging.
- Completeness scan (4.12) returns zero actionable results.
