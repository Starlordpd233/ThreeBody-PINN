# Phase 2 — `.gitignore` Update + Gitignored Data Migration

## Goal
Protect `simulation_data/` before any data moves, then move gitignored datasets with plain filesystem operations.

## 2.1 Update `.gitignore` first

Edit `<home>/Desktop/cursor/.gitignore` and add a new block for `simulation_data/` while keeping current `3_Body_Problem/` rules during migration.

Minimum additions:
```gitignore
# Simulation Data Directories (new layout)
simulation_data/Data/ic_raw/
simulation_data/Data/ic_final/
simulation_data/Data/brutus_output/
simulation_data/Data/metrics/
simulation_data/Data/testing_data/
simulation_data/Documentation/problematic_ics/
simulation_data/Documentation/problematic_ics_blacklist.json
simulation_data/Validation/prescreening/prescreening_data/
simulation_data/Validation/analysis/figures/
simulation_data/Scripts/debug/*.txt
simulation_data/Scripts/debug/*.png
simulation_data/**/figures/**/*.html
simulation_data/**/*.txt
!simulation_data/**/README.txt
```

Commit immediately:
```bash
cd <home>/Desktop/cursor
git add .gitignore
git commit -m "chore: add simulation_data ignore rules before data migration"
```

## 2.2 Create only data-target directories

Do not pre-create directories intended as whole-directory `git mv` targets in later phases.

```bash
mkdir -p simulation_data/Data/{ic_raw,ic_final,brutus_output,metrics,testing_data}
mkdir -p simulation_data/Documentation/problematic_ics
mkdir -p simulation_data/Validation/prescreening/prescreening_data
mkdir -p simulation_data/Validation/analysis/figures/{hierarchical_positions,metrics_analysis,reference_plane,prescreening}
```

## 2.3 Move gitignored data with `mv`

```bash
# IC data
mv 3_Body_Problem/ic_raw_datasets/ic_hierarchical simulation_data/Data/ic_raw/
mv 3_Body_Problem/ic_raw_datasets/ic_standard_quasi_random simulation_data/Data/ic_raw/

# Final IC data
mv 3_Body_Problem/final_stage_ic_datasets/ic_hierarchical simulation_data/Data/ic_final/
mv 3_Body_Problem/final_stage_ic_datasets/ic_hierarchical_for_gold_standard simulation_data/Data/ic_final/
mv 3_Body_Problem/final_stage_ic_datasets/ic_standard_quasi_random simulation_data/Data/ic_final/
mv 3_Body_Problem/final_stage_ic_datasets/ic_standard_quasi_random_for_gold_standard simulation_data/Data/ic_final/

# Brutus outputs (data folders only)
mv 3_Body_Problem/brutus_output/brutus_hierarchical simulation_data/Data/brutus_output/
mv 3_Body_Problem/brutus_output/brutus_hierarchical_gold_standard simulation_data/Data/brutus_output/
mv 3_Body_Problem/brutus_output/brutus_standard_quasi_random simulation_data/Data/brutus_output/
mv 3_Body_Problem/brutus_output/brutus_standard_quasi_random_gold_standard simulation_data/Data/brutus_output/

# Metrics data folders
mv 3_Body_Problem/brutus_metrics/sim_result_metric_hierarchical simulation_data/Data/metrics/
mv 3_Body_Problem/brutus_metrics/sim_result_metric_hierarchical_gold_standard simulation_data/Data/metrics/
mv 3_Body_Problem/brutus_metrics/sim_result_metric_standard simulation_data/Data/metrics/
mv 3_Body_Problem/brutus_metrics/sim_result_metric_standard_gold_standard simulation_data/Data/metrics/

# Misc data
mv 3_Body_Problem/testing_data simulation_data/Data/
mv 3_Body_Problem/problematic_ics/* simulation_data/Documentation/problematic_ics/
mv 3_Body_Problem/problematic_ics_blacklist.json simulation_data/Documentation/
mv 3_Body_Problem/prescreen_stage2/processing_index_ic_hierarchical.json simulation_data/Validation/prescreening/prescreening_data/
mv 3_Body_Problem/prescreen_stage2/processing_index_ic_standard_quasi_random.json simulation_data/Validation/prescreening/prescreening_data/
mv 3_Body_Problem/prescreen_stage2/prescreen_run_results simulation_data/Validation/prescreening/prescreening_data/
```

Handle optional figure directories with explicit guards (no `2>/dev/null` suppression):
```bash
for d in \
  3_Body_Problem/prescreen_stage2/analysis_output \
  3_Body_Problem/analyze_data_generation/figures/hierarchical_positions \
  3_Body_Problem/analyze_data_generation/figures/metrics_analysis \
  3_Body_Problem/analyze_data_generation/figures/reference_plane
  do
  if [ -d "$d" ]; then
    case "$d" in
      *analysis_output)
        mv "$d"/* simulation_data/Validation/analysis/figures/prescreening/
        ;;
      *)
        mv "$d" simulation_data/Validation/analysis/figures/
        ;;
    esac
  fi
done
```

## 2.4 Verify ignore behavior
```bash
git status --short | rg "simulation_data/Data/|simulation_data/Validation/prescreening/prescreening_data/|simulation_data/Validation/analysis/figures/" || true
```

Expected: no untracked data flood from migrated ignored paths.

## Exit Criteria
- `.gitignore` new rules committed before data movement.
- Data directories moved successfully.
- No unexpected untracked explosion in `git status`.
