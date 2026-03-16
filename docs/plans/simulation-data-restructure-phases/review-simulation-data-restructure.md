# Review Report: Simulation Data Restructure Phases

**Date:** March 16, 2026
**Target Architecture:** Moving `3_Body_Problem/` to `simulation_data/`
**Target Scripts Tested:** Data-Generation Pipeline (IC Generation, Brutus Output, Metrics, Prescreening, PINN Parsing)

**Note:** An initial review (Report 1) incorrectly found "zero critical errors" and was removed after Reports 2 and 3 demonstrated it missed 4 critical and 2 significant bugs. The reports below are the authoritative reviews.

---

# Review Report 1
**Findings**
- `[P1]` Phase 5’s “correspondence-only” verification does not work as written. The command in [phase-5-verification-and-cutover.md](<home>/Desktop/cursor/docs/plans/simulation-data-restructure-phases/phase-5-verification-and-cutover.md#L18) passes `--modules correspondence`, but [__main__.py](<home>/Desktop/cursor/3_Body_Problem/dataset_readiness_checks/__main__.py#L40) writes that into the global `config` and [validator.py](<home>/Desktop/cursor/3_Body_Problem/dataset_readiness_checks/validator.py#L346) immediately throws it away by creating a fresh `ValidationConfig()`. The phase therefore runs the full default validator set, not the narrow smoke test the plan claims.
- `[P1]` That same Phase 5 run then falls into an unfixed metrics-validation bug the plan never accounts for. [validator.py](<home>/Desktop/cursor/3_Body_Problem/dataset_readiness_checks/validator.py#L226) looks for files named like `standard_0000.json`, but the real files are `metrics_standard_0000.json` / `metrics_hierarchical_0000.json` in [sim_result_metric_standard](<home>/Desktop/cursor/3_Body_Problem/brutus_metrics/sim_result_metric_standard) and [sim_result_metric_hierarchical](<home>/Desktop/cursor/3_Body_Problem/brutus_metrics/sim_result_metric_hierarchical). Even if the filename bug were fixed, [modules/metrics.py](<home>/Desktop/cursor/3_Body_Problem/dataset_readiness_checks/modules/metrics.py#L22) expects keys like `final_energy_error` and `momentum_drift`, while actual metric JSONs such as [metrics_standard_0000.json](<home>/Desktop/cursor/3_Body_Problem/brutus_metrics/sim_result_metric_standard/metrics_standard_0000.json) expose `conservation`, `timing`, `file_info`, etc. Result: Phase 5 verification is not trustworthy after cutover.
- `[P1]` Phase 5’s stale-reference gate cannot satisfy its own expectation. The grep in [phase-5-verification-and-cutover.md](<home>/Desktop/cursor/docs/plans/simulation-data-restructure-phases/phase-5-verification-and-cutover.md#L6) scans all `.py`, `.md`, and `.tex` files, but the rewrite scope in [phase-4-path-rewrites-and-docs.md](<home>/Desktop/cursor/docs/plans/simulation-data-restructure-phases/phase-4-path-rewrites-and-docs.md#L346) does not include the phase bundle itself or older review docs. Those files intentionally contain `3_Body_Problem`, for example [phase-1-preexisting-bugfixes.md](<home>/Desktop/cursor/docs/plans/simulation-data-restructure-phases/phase-1-preexisting-bugfixes.md#L8) and [review.md](<home>/Desktop/cursor/docs/plans/review.md#L40). As written, 5.1 will keep reporting hits even when the migration is otherwise complete.
- `[P2]` Phase 1 step 6 introduces a new bug in the proposed fix. The snippet in [phase-1-preexisting-bugfixes.md](<home>/Desktop/cursor/docs/plans/simulation-data-restructure-phases/phase-1-preexisting-bugfixes.md#L53) calls `os.path.exists(...)` but never imports `os`, so `compare_thresholds.py` would still fail with `NameError`.
- `[P2]` The plan claims completeness checks for all rewrites, but both search gates ignore `.txt` companions. Phase 4 explicitly rewrites [parsing.txt](<home>/Desktop/cursor/docs/plans/simulation-data-restructure-phases/phase-4-path-rewrites-and-docs.md#L120), yet the scans in [phase-4-path-rewrites-and-docs.md](<home>/Desktop/cursor/docs/plans/simulation-data-restructure-phases/phase-4-path-rewrites-and-docs.md#L332) and [phase-5-verification-and-cutover.md](<home>/Desktop/cursor/docs/plans/simulation-data-restructure-phases/phase-5-verification-and-cutover.md#L6) only cover `.py`/`.md`/`.tex`. A stale `3_Body_Problem` reference can survive there without tripping the plan.

**Assumptions**
- I treated `docs/plans/**` as in-scope because Phase 5’s own grep includes them.
- I did not run the full dataset validator; the blocking issues above are visible directly from the current code, filenames, and JSON schema.

1. I can turn this into a patched version of the phase docs.
2. I can also patch `dataset_readiness_checks` so `--modules` works and metrics validation matches the real files.


# Review Report 2
  ---                                                                                                                                                                                                     
  Critical Analysis Report: Simulation Data Restructure Plan
                                                                                                                                                                                                          
  Executive Summary                                         

  After systematic verification against the actual codebase, I have identified 4 critical issues (P1) and 2 significant issues (P2) that would hinder successful execution of the plan. The review
  document already identified some of these, and I've confirmed them plus found additional problems.

  ---
  P1 Critical Issues (Would Block Migration)

  1. Phase 5 --modules correspondence Bug (CONFIRMED)

  Location: Phase 5.2 validation command

  Problem: The --modules correspondence CLI argument is parsed but then discarded:
  - __main__.py:40-41 writes to config.enabled_modules
  - __main__.py:47 calls run_validation() without passing modules
  - validator.py:346 creates a fresh ValidationConfig() that ignores the global config
  - Result: All 12 validation modules run instead of just "correspondence"

  Impact: Phase 5 verification will be slower than expected and may surface unrelated validation failures.

  Fix Required: Add a modules parameter to run_validation() and propagate it to ValidationConfig().

  ---
  2. Metrics Validation Filename/Key Mismatch (CONFIRMED)

  Location: 3_Body_Problem/dataset_readiness_checks/modules/metrics.py

  Problems:
  1. Filename mismatch: Expects standard_0000.json, actual files are metrics_standard_0000.json
  2. Key mismatch: Expects final_energy_error, momentum_drift, actual JSON has conservation, timing, file_info structure

  Impact: Phase 5 validation will fail with FileNotFoundError or KeyError.

  Fix Required: Update metrics.py to:
  - Use correct filename pattern
  - Parse the actual JSON schema

  ---
  3. Phase 5.1 False Positives from Plan Files (NEW DISCOVERY)

  Location: Phase 5.1 grep command

  Problem: The grep command:
  rg "3_Body_Problem" --type py --type tex --type md -l \
    --glob '!brutus_simulation_documentation/*' \
    --glob '!.git/*'

  Does NOT exclude docs/plans/. The plan files themselves contain 50+ references to 3_Body_Problem.

  Impact: Phase 5.1 will report false positives, making the "Expected: no actionable references" exit criterion impossible to satisfy.

  Fix Required: Add --glob '!docs/plans/*' to the grep command, or document that plan files intentionally retain old references.

  ---
  4. Phase 1 Step 6 Missing import os (CONFIRMED)

  Location: 3_Body_Problem/prescreen_stage2/utilities/compare_thresholds.py

  Problem: The Phase 1 fix adds code using os.path.exists() but the file only imports json and numpy. No import os is present.

  Impact: Would cause NameError: name 'os' is not defined when the script runs.

  Fix Required: Add import os to the imports section.

  ---
  P2 Significant Issues (Would Cause Problems)

  5. Completeness Scans Miss .txt Files (CONFIRMED)

  Location: Phase 4.12 and Phase 5.1

  Problem: 3 terminal output log files in brutus_simulation_documentation/ contain 3_Body_Problem references but are NOT covered by completeness scans:
  - 1st_run_terminal_output.txt
  - 2_run_terminal_output.txt
  - 3_run_terminal_output.txt

  Impact: Stale references can survive in these files after migration.

  Recommendation: Either add .txt to scan scope, explicitly list these files for rewriting, or document that they are historical logs that don't need updates.

  ---
  6. compare_thresholds.py References Nonexistent File

  Location: 3_Body_Problem/prescreen_stage2/utilities/compare_thresholds.py:10

  Problem: The script hardcodes:
  json_file = "<home>/Desktop/cursor/3_Body_Problem/run_results_2025-06-16T21-27-29.065044.json"
  This file does not exist on disk.

  Impact: The script is currently broken and would fail immediately if run.

  Note: Phase 1 fix addresses this by converting to CLI argument, but the missing os import bug must also be fixed.

  ---
  Verified Correct (No Issues)

  ┌────────────────────────────────────────────┬────────────────────────────────────────────┐
  │                    Item                    │                   Status                   │
  ├────────────────────────────────────────────┼────────────────────────────────────────────┤
  │ All Phase 2/3 source directories exist     │ ✅ Verified                                │
  ├────────────────────────────────────────────┼────────────────────────────────────────────┤
  │ Phase 1 filename pattern fixes             │ ✅ Correct (actual files use short naming) │
  ├────────────────────────────────────────────┼────────────────────────────────────────────┤
  │ Empty Validation/__init__.py is sufficient │ ✅ Confirmed                               │
  ├────────────────────────────────────────────┼────────────────────────────────────────────┤
  │ Analysis scripts covered in Phase 4.9      │ ✅ All 5 files listed                      │
  ├────────────────────────────────────────────┼────────────────────────────────────────────┤
  │ Phase 3 git mv commands                    │ ✅ No destination collision issues         │
  └────────────────────────────────────────────┴────────────────────────────────────────────┘

  ---

---

# Resolution Status

All P1 and P2 findings from Reviews 1 and 2 have been addressed in the updated phase documents:

| ID | Finding | Severity | Resolution | Updated File |
|----|---------|----------|------------|--------------|
| P1-1 | `--modules` CLI argument silently discarded | Critical | Added `modules` param to `run_validation()` | `phase-1-preexisting-bugfixes.md` Step 8, `master-plan-rewrite.md` #15 |
| P1-2 | Metrics filename pattern mismatch | Critical | Added `metrics_` prefix to filename construction | `phase-1-preexisting-bugfixes.md` Step 9, `master-plan-rewrite.md` #16 |
| P1-3 | Metrics JSON key schema mismatch | Critical | Replaced flat key checks with nested schema parsing | `phase-1-preexisting-bugfixes.md` Step 10, `master-plan-rewrite.md` #17 |
| P1-4 | Phase 5.1 grep false positives from plan files | Critical | Added `--glob '!docs/plans/*'` exclusion | `phase-5-verification-and-cutover.md` 5.1, `phase-4-path-rewrites-and-docs.md` 4.12, `master-plan-rewrite.md` #18 |
| P2-1 | Phase 1 Step 6 missing `import os` | Significant | Added `import os` to proposed code snippet | `phase-1-preexisting-bugfixes.md` Step 6, `master-plan-rewrite.md` #19 |
| P2-2 | Completeness scans miss `.txt` files | Significant | Added `--type txt` to Phase 4.12 and Phase 5.1 | `phase-4-path-rewrites-and-docs.md` 4.12, `phase-5-verification-and-cutover.md` 5.1, `master-plan-rewrite.md` #20 |
| P2-3 | `compare_thresholds.py` nonexistent JSON | Significant | Already covered by Phase 1 Step 6 (CLI arg conversion) + P2-1 fix | `phase-1-preexisting-bugfixes.md` Step 6 |
