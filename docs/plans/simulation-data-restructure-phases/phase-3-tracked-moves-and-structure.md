# Phase 3 — Tracked Moves + Structural Consolidation

## Goal
Move tracked code/docs with `git mv`, move ignored-but-needed scripts with `mv + git add`, and avoid destination-collision failures.

## 3.1 Create parent destinations only
```bash
mkdir -p simulation_data/Scripts/{ic_generation,brutus_runners,metrics_calculation,debug,archived}
mkdir -p simulation_data/Validation/{analysis/prescreening_analysis,audit_reports,prescreening}
mkdir -p simulation_data/Documentation

# Create namespace marker so `python -m Validation.dataset_readiness_checks` works in Phase 5
touch simulation_data/Validation/__init__.py
```

Do not pre-create:
- `simulation_data/Scripts/debug/renaming`
- `simulation_data/Validation/dataset_readiness_checks`
- `simulation_data/Validation/prescreening/utilities`

These are whole-directory `git mv` targets.

## 3.2 Move tracked files/directories with `git mv`
```bash
# Core scripts
git mv 3_Body_Problem/FINAL_ic_generator_enhanced.py simulation_data/Scripts/ic_generation/
git mv 3_Body_Problem/generate_enhanced_ics.py simulation_data/Scripts/ic_generation/
git mv 3_Body_Problem/run_brutus_both_type_simple.py simulation_data/Scripts/brutus_runners/
git mv 3_Body_Problem/run_brutus_hierarchical_only_mac_gold_standard.py simulation_data/Scripts/brutus_runners/

# Debug + archived
git mv 3_Body_Problem/debug_scripts/audit_and_backfill_brutus_result_footers.py simulation_data/Scripts/debug/
git mv 3_Body_Problem/debug_scripts/check_brutus_completeness.py simulation_data/Scripts/debug/
git mv 3_Body_Problem/debug_scripts/compare_folders.py simulation_data/Scripts/debug/
git mv 3_Body_Problem/debug_scripts/compare_ic_brutus_files.py simulation_data/Scripts/debug/
git mv 3_Body_Problem/debug_scripts/renaming simulation_data/Scripts/debug/
git mv 3_Body_Problem/scripts_not_using/manage_problematic_ics_notusing.py simulation_data/Scripts/archived/
git mv 3_Body_Problem/scripts_not_using/visualize_test_brutus.py simulation_data/Scripts/archived/

# Validation + analysis
git mv 3_Body_Problem/dataset_readiness_checks simulation_data/Validation/
git mv 3_Body_Problem/prescreen_stage2/stage2_prescreening_revised_auto.py simulation_data/Validation/prescreening/
git mv 3_Body_Problem/prescreen_stage2/prescreening_utils.py simulation_data/Validation/prescreening/
git mv 3_Body_Problem/prescreen_stage2/utilities simulation_data/Validation/prescreening/
git mv "3_Body_Problem/prescreen_stage2/analysis script/analyze.py" simulation_data/Validation/analysis/prescreening_analysis/
git mv "3_Body_Problem/prescreen_stage2/analysis script/analyze_prescreening.py" simulation_data/Validation/analysis/prescreening_analysis/
git mv "3_Body_Problem/prescreen_stage2/analysis script/analyze_prescreening_new.py" simulation_data/Validation/analysis/prescreening_analysis/
git mv "3_Body_Problem/prescreen_stage2/analysis script/analyze_prescreening_v2.py" simulation_data/Validation/analysis/prescreening_analysis/
git mv "3_Body_Problem/prescreen_stage2/analysis script/analyze_threshold_failures.py" simulation_data/Validation/analysis/prescreening_analysis/
git mv 3_Body_Problem/analyze_data_generation/metrics_analysis.py simulation_data/Validation/analysis/
git mv 3_Body_Problem/analyze_data_generation/particle_positions_viz.py simulation_data/Validation/analysis/
git mv 3_Body_Problem/analyze_data_generation/reference_plane_viz.py simulation_data/Validation/analysis/
git mv 3_Body_Problem/analyze_data_generation/utils.py simulation_data/Validation/analysis/

# Documentation
git mv 3_Body_Problem/data_documentation/DATASET_DOCUMENTATION.md simulation_data/Documentation/
git mv 3_Body_Problem/README.md simulation_data/Documentation/
```

## 3.3 Move ignored/untracked sources with `mv`, then stage

These sources are ignored by current `.gitignore`, so `git mv` fails.

```bash
# From ignored brutus_metrics/
mv 3_Body_Problem/brutus_metrics/calculate_metrics.py simulation_data/Scripts/metrics_calculation/
mv 3_Body_Problem/brutus_metrics/calculate_brutus_metrics.py simulation_data/Scripts/metrics_calculation/
mv 3_Body_Problem/brutus_metrics/analyze_metrics_not_sure_if_using.py simulation_data/Scripts/archived/

# From ignored brutus_output/check missing results line/
mv "3_Body_Problem/brutus_output/check missing results line/check_missing_results.py" simulation_data/Validation/audit_reports/
mv "3_Body_Problem/brutus_output/check missing results line/check_missing_results_detailed.py" simulation_data/Validation/audit_reports/
mv "3_Body_Problem/brutus_output/check missing results line/footer_audit_20251224_151949.md" simulation_data/Validation/audit_reports/
mv "3_Body_Problem/brutus_output/check missing results line/footer_audit_20251224_170141.md" simulation_data/Validation/audit_reports/
mv "3_Body_Problem/brutus_output/check missing results line/missing_results_20250716_230528.csv" simulation_data/Validation/audit_reports/
mv "3_Body_Problem/brutus_output/check missing results line/missing_results_report_20250716_230528.txt" simulation_data/Validation/audit_reports/
```

## 3.4 Handle tracked `analysis_output copy/` safely

This directory is tracked and must not be deleted with plain `rm -rf`.

```bash
git mv "3_Body_Problem/prescreen_stage2/analysis_output copy" simulation_data/Validation/analysis/figures/prescreening_copy_archive
```

Optional (if you want selected artifacts in primary output folder):
```bash
for f in comparison_distributions.png threshold_recommendation.png threshold_sensitivity.png property_correlations.png property_distributions.png; do
  src="simulation_data/Validation/analysis/figures/prescreening_copy_archive/$f"
  dst="simulation_data/Validation/analysis/figures/prescreening/$f"
  if [ -f "$src" ] && [ ! -f "$dst" ]; then
    git mv "$src" "$dst"
  fi
done
```

## 3.5 Move optional ignored IDE folder
```bash
if [ -d 3_Body_Problem/.vscode ]; then
  mv 3_Body_Problem/.vscode simulation_data/
fi
```

## 3.6 Commit
```bash
cd <home>/Desktop/cursor
git add -A
git commit -m "chore: move scripts, validation, and docs into simulation_data structure"
```

## Notes
- `missing_results_report_20250716_230528.txt` in `audit_reports/` will remain **untracked** at the new location because `simulation_data/**/*.txt` in `.gitignore` catches it. This is consistent with its previous gitignored status — acceptable.
- `Validation/__init__.py` created in 3.1 will be staged by `git add -A` in 3.6 and committed.

## Exit Criteria
- No failed `git mv` due to untracked sources.
- No destination-collision failures from pre-created directories.
- Tracked `analysis_output copy/` handled via Git-aware operations.
- `simulation_data/Validation/__init__.py` exists and is staged.
