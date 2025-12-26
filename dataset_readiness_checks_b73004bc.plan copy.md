---
name: Dataset readiness checks
overview: Rename and harden your current validation scripts into a runnable, read-only dataset readiness screening suite with comprehensive validation checks for PINN training suitability.
todos:
  - id: rename-and-package
    content: Rename `validation_system` → `dataset_readiness_checks`, add `__init__.py`/`__main__.py` for `python -m` execution.
    status: pending
  - id: fix-core-plumbing
    content: Fix config portability + filename patterns, repair naming glob bug, harden Brutus/footer parsing, and make logging API consistent.
    status: pending
  - id: implement-missing-modules
    content: Add the missing validation modules (completeness/metadata/physics/parameters/metrics/blacklist) and wire them into the orchestrator.
    status: pending
    dependencies:
      - fix-core-plumbing
  - id: implement-enhanced-checks
    content: Implement enhanced validation modules for coverage analysis, duplicate detection, and temporal consistency checks.
    status: pending
    dependencies:
      - implement-missing-modules
  - id: reporting-and-cli
    content: Add CLI entrypoint and report writers (Markdown/JSON/optional CSV) with clear exit codes and configurable strictness.
    status: pending
    dependencies:
      - implement-enhanced-checks
  - id: doc-sync
    content: (Optional) Update dataset documentation naming section to match current `*_gold_####.txt` filenames.
    status: pending
    dependencies:
      - rename-and-package
---

# Upgrade `validation_system` into `dataset_readiness_checks`

## What I found (current state and gaps)

The existing `validation_system` has a solid foundation but lacks the comprehensive validation needed to assess dataset readiness for PINN training. Key findings:

- **Import graph is broken**: `modules/__init__.py` imports several modules that do not exist, causing `Validator._load_modules()` to fail immediately.
- **Logger API mismatch**: `validator.py` calls `self.logger.info/error/warning`, but `get_logger()` returns a `ValidationLogger` wrapper that only exposes `log_info/log_error/...`.
- **Filename scanning bug**: `utils/naming.py` builds glob patterns with an extra underscore, which can silently make correspondence/inventory checks miss files.
- **Result footer parsing bug**: `utils/parsers.parse_result_footer()` cannot parse `dE/E` (only matches `\w+` keys), making footer energy fields unreliable.
- **Gold naming drift vs config/docs**: Current dataset folders contain `*_gold_####.txt` filenames (IC + Brutus), but config/docs still assume some non-gold filename patterns. I changed the gold IC + Brutus files yesterday using the rename scripts at <home>/Desktop/cursor/3_Body_Problem/debug_scripts/renaming, so there might be other existing files/documentations still using the original names. 
- **Metrics integration mismatch**: Validator expects metrics files named like `{variant}_{####}.json`, but your generator writes `metrics_{hierarchical|standard}_{####}.json`. Because of the recent name change, there are changes to other scripts necessary so that the naming patterns will be consistent: including the Brutus batch scripts that generates the files as well as other scripts that use the Brutus output files as inputs. These files should all be identified and flagged and reported.
- **Missing high-signal validation**: Current checks only cover correspondence and file format. No validation of:
- Physical plausibility (positive masses, finite values, no collisions/escapes)
- Parameter consistency (tol, Lw, dt_out distributions)
- Conservation metrics (energy/momentum/angular momentum drift)
- Dataset coverage (feature space distribution, outliers, gaps)
- Duplicate IC detection
- Temporal consistency (snapshot intervals, monotonic timestamps)
- Metrics integrity (cross-validation between JSON and Brutus files)
- PINN input vector computability. We need to figure out the specific formula or definition for the computation of the input vector here. 

## End state you'll get

A comprehensive, read-only dataset readiness screening suite with:

### Core Validation Modules

1. **Inventory & Correspondence** - 1:1 IC↔Brutus mapping with blacklist awareness
2. **Format Validation** - Robust parsing of IC and Brutus files with NaN/inf detection
3. **Completeness Checks** - Final timestep ≥ threshold + minimum snapshot count + monotonic timestamps
4. **Metadata Validation** - Footer presence analysis + parameter distribution histograms + path format consistency
5. **Physics Sanity Checks** - Energy, COM, momentum, virial ratio + hierarchical perturbation bounds
6. **Parameter Consistency** - Expected tol/Lw/dt_out sets per variant + warning for outliers
7. **Metrics Integration** - JSON schema validation + cross-check with Brutus snapshots + conservation quality assessment
8. **Blacklist Verification** - Confirmation that blacklisted IDs are correctly missing

### Enhanced Training-Focused Validation

9. **Coverage Analysis** - Statistical analysis of 13-component IC vector across dataset:

- Min/max/mean/std for each component
- Percentile distributions (5th, 25th, 50th, 75th, 95th)
- Outlier detection (beyond 3σ)
- Gap analysis in feature space
- Sobol sequence uniformity verification (for standard ICs)

10. **Duplicate Detection** - Pairwise distance analysis to flag near-identical ICs (risk of data leakage)
11. **Temporal Consistency** - Verification of consistent dt_out intervals + monotonic CPU times
12. **Cross-Variant Validation** - Gold vs non-gold subset verification + parameter set comparisons

### Reporting and Integration

- **Markdown summary** - Human-readable report with executive summary and detailed findings
- **JSON report** - Machine-readable structured data for programmatic analysis
- **CSV per-file table** - Optional detailed spreadsheet of validation results
- **CLI with configurable strictness** - Exit codes indicate overall readiness (0=ready, non-zero=issues)
- **Configurable thresholds** - Adjustable parameters for different validation scenarios

## Implementation steps (what I will change)

### 1. Rename + packaging

- Rename `3_Body_Problem/validation_system/` → `3_Body_Problem/dataset_readiness_checks/`
- Add `__init__.py` and `__main__.py` for `python -m dataset_readiness_checks` execution
- Update all internal imports to reflect new package name

### 2. Fix core plumbing (config, naming, parsing, logging)

- **config.py**: Make `base_dir` relative by default (derived from `__file__`), update IC/brutus patterns for gold folders, fix metrics lookup to match `calculate_metrics.py` naming
- **naming.py**: Fix glob pattern construction (remove extra underscore), make extraction robust to gold/non-gold prefixes
- **parsers.py**: Replace footer parsing with robust regex supporting `dE/E` and OS path variants, add fast Brutus scan helper for last timestep + snapshot sampling
- **logging.py**: Expose standard `.info/.warning/.error/.debug` methods for compatibility

### 3. Implement the missing core modules

#### `completeness.py`

- Check final timestep ≥ threshold (default 9.5)
- Verify minimum snapshot count (default 10)
- Validate monotonic increasing timestamps
- Detect and report incomplete simulations

#### `metadata.py`

- Analyze footer presence/absence (optional but noted)
- Parse footer fields with robust regex
- Validate footer consistency (t_end matches final timestamp, N=3)
- Check OS path format (macOS/Windows) and IC folder references
- Generate parameter distribution histograms (tol, Lw, dt_out)

#### `physics.py`

- Validate IC energy computation matches reference implementation
- Check COM offset: strict zero for standard, within perturbation bounds for hierarchical
- Verify total momentum: strict zero for standard, within bounds for hierarchical
- Compute virial ratio and validate within prescreening thresholds [0.001, 2.0]
- Detect collisions (min separation < 0.01) and escapes (max separation > 100)
- Flag negative masses or infinite/NaN values

#### `parameters.py`

- Define expected parameter sets per variant (from DATASET_DOCUMENTATION.md)
- Validate each file's parameters against expected sets
- Generate warnings for unexpected combinations
- Report parameter heterogeneity statistics

#### `metrics.py`

- Validate metrics JSON schema (required fields, data types)
- Cross-check energy values: compute from snapshots vs JSON values (within tolerance)
- Verify momentum and angular momentum consistency
- Assess conservation quality classification logic
- Flag missing or malformed metrics files

#### `blacklist.py`

- Load blacklist from `problematic_ics_blacklist.json`
- Verify blacklisted ICs are indeed missing Brutus outputs
- Generate explanations for expected gaps
- Report any inconsistencies (blacklisted ICs with outputs, non-blacklisted missing outputs)

### 4. Implement enhanced validation modules

#### `coverage.py`

- Compute 13-component IC vector for each IC (using `input_vector` logic from pipeline)
- Generate dataset-wide statistics: min, max, mean, std, percentiles for each component
- Identify outliers (beyond 3σ) and flag for review
- Check Sobol sequence uniformity for standard ICs (discrepancy analysis)
- Visualize feature space distributions (histograms, correlation matrices)
- Detect gaps in parameter coverage (clustering analysis)

#### `duplicates.py`

- Compute pairwise distances between IC vectors (Euclidean or cosine similarity)
- Flag potential duplicates (distance < epsilon, default 1e-6)
- Consider mass permutation invariance for hierarchical systems
- Generate warnings for near-identical ICs that could cause data leakage

#### `temporal.py`

- Verify consistent snapshot intervals (dt_out) across file
- Check for missing timestamps (gaps in expected sequence)
- Validate monotonic CPU times
- Assess temporal sampling adequacy for PINN training

### 5. Reporting + CLI

- **reporting.py**: Generate Markdown, JSON, and optional CSV reports with:
- Executive summary (ready/not ready determination)
- Module-level results with severity counts
- Detailed issue listings with file references
- Statistical summaries and distribution visualizations
- **cli.py**: Command-line interface with:
- `--variants` flag to select dataset variants (default: all)
- `--threshold` for completeness check (default: 9.5)
- `--modules` to enable/disable specific validation modules
- `--sample` for spot-checking subsets
- Clear exit codes: 0=ready, 1=warnings, 2=errors/failures

### 6. Optional documentation sync

- Update `DATASET_DOCUMENTATION.md` naming section to match current `*_gold_####.txt` reality
- Add validation methodology section referencing the new readiness suite

## Notes on severity defaults (read-only)

- **FAIL/ERROR**: Missing/invalid files/directories, parse failures, incomplete simulations (< threshold), collisions, escapes, negative masses, infinite/NaN values, parameter mismatch beyond tolerance
- **WARNING**: Missing `Result:` footer (known inconsistency), minor parameter variations, conservation quality degradation, moderate outliers
- **PASS**: All checks satisfied, parameters within expected ranges, conservation quality excellent
- **SKIPPED**: Blacklisted ICs (expected missing), user-disabled modules

## Success criteria

The dataset readiness suite will be considered successful when:

1. **Comprehensive coverage**: All 12 validation modules implemented and functional
2. **Actionable reports**: Markdown and JSON outputs provide clear readiness determination and specific issues
3. **Configurable**: CLI allows selection of variants, modules, and threshold adjustments