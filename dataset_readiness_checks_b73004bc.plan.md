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
    content: Implement enhanced validation modules for coverage analysis (PINN input vector), duplicate detection, and temporal consistency.
    status: pending
    dependencies:
      - implement-missing-modules
  - id: implement-curriculum-checks
    content: Implement curriculum readiness checks to classify trajectories into Stages 0-6 and report distribution/coverage.
    status: pending
    dependencies:
      - implement-enhanced-checks
  - id: reporting-and-cli
    content: Add CLI entrypoint and report writers (Markdown/JSON/optional CSV) with clear exit codes and configurable strictness.
    status: pending
    dependencies:
      - implement-curriculum-checks
  - id: audit-scripts-naming
    content: Audit and flag scripts (batch runners, metric calculators) that use outdated filename patterns to ensure full pipeline consistency.
    status: pending
    dependencies:
      - rename-and-package
---

# Upgrade `validation_system` into `dataset_readiness_checks`

## What I found (current state and gaps)

The existing `validation_system` has a solid foundation but lacks the comprehensive validation needed to assess dataset readiness for PINN training, particularly regarding the specific input vector requirements and curriculum stages.

- **Import graph is broken**: `modules/__init__.py` imports missing modules.
- **Filename scanning bug**: `utils/naming.py` has glob pattern issues (extra underscore).
- **Gold naming drift**: The dataset now uses `*_gold_####.txt` naming for gold-standard folders, but config/docs/scripts often assume older patterns. The dataset has 4 distinct pairs of folders (Hierarchical/Standard * Normal/Gold).
- **Metrics integration mismatch**: Generator produces `metrics_{type}_{id}.json`, validator expects `{type}_{id}.json`.
- **PINN Input Vector**: The specific 13-component vector logic exists in `pinn/data-processing-pipeline-full.py` but is not checked by the current validator.
- **Curriculum Stages**: The dataset is intended for staged training (Stages 0-6), but there is no check to verify that the dataset actually populates these stages adequately.
- **Missing Validations**:
  - **Physics**: Energy conservation, COM frame (critical for Hierarchical vs Standard differences), Virial ratio.
  - **Parameters**: `dt_out` consistency (0.01 for Gold/High-Fidelity vs 0.08/0.17 for Low-Fidelity).
  - **Architecture Compatibility**: Ensuring 13-component input computability for every IC.

## End state you'll get

A comprehensive, read-only dataset readiness screening suite with:

### Core Validation Modules

1. **Inventory & Correspondence** - 1:1 IC↔Brutus mapping across all 4 folder pairs, handling blacklist.
2. **Format Validation** - Robust parsing with NaN/inf detection.
3. **Completeness Checks** - Final timestep ≥ 9.5 (or threshold), snapshot count, monotonic time.
4. **Metadata Validation** - Footer analysis, OS path consistency, parameter histograms.
5. **Physics Sanity Checks** - Energy computation, **COM frame verification** (Hierarchical requires perturbation check, Standard requires strict zero), Momentum check.
6. **Parameter Consistency** - Validate `dt_out` (0.01 vs 0.08/0.17), `tolerance` (1e-13 vs 1e-15), `word_length`.
7. **Metrics Integration** - JSON schema validation, cross-check values against Brutus output.
8. **Blacklist Verification** - Confirm blacklisted IDs have no outputs.

### Enhanced Training-Focused Validation

9. **Coverage Analysis (PINN Input Vector)**
   - Compute the exact **13-component vector** for every IC:
     - `[m1, m2, m3]` (normalized)
     - `E` (normalized)
     - `L_norm` (normalized)
     - `Q` (normalized)
     - `s_min` (normalized)
     - `[I1, I2, I3]` (shape invariants)
     - `[theta1, theta2]` (velocity angles)
     - `I_norm` (bounded)
   - Report statistics (min/max/mean/std) and outliers (>3σ) for each component.
   - **Crucial**: Verify no NaNs in these computed features.

10. **Curriculum Readiness**
    - Classify each trajectory into **Stages 0-6** based on `CTL-instruction-final.md` criteria ($E, Q, s_{min}, L_{norm}, \tau_L$).
    - Report distribution (e.g., "Stage 0: 500 files", "Stage 6: 20 files").
    - Warn if any stage is under-represented.

11. **Duplicate Detection** - Flag near-identical ICs (distance < 1e-6).
12. **Temporal Consistency** - Check `dt_out` uniformity (vital for fixed-step training data).

### Reporting and Integration

- **Markdown/JSON Reports** - Executive summary, detailed issues, feature distribution plots (ASCII/links).
- **CLI** - Configurable strictness, variant selection (`--variants all`, `--variants gold`), specific module toggle.
- **Script Audit** - A special report listing external scripts (batch runners, metric calculators) that appear to use outdated filename patterns.

## Implementation steps

### 1. Rename + packaging

- Rename `3_Body_Problem/validation_system/` → `3_Body_Problem/dataset_readiness_checks/`.
- Add `__init__.py`, `__main__.py`.

### 2. Fix core plumbing

- **config.py**: Define the 4 folder pairs explicitly. Update regex to handle `*_gold_####.txt`.
- **parsers.py**: Robust regex for `dE/E`, handling `Result:` line variations.
- **naming.py**: Fix glob patterns.

### 3. Implement Core Modules

- **`completeness.py`**: Check $t_{final} \approx 10.0$.
- **`physics.py`**:
  - Implement `compute_energy`, `check_com`.
  - **Note**: Hierarchical ICs have Gaussian perturbations, so COM $\neq 0$ exactly (but close). Standard ICs should be strictly 0.
- **`parameters.py`**:
  - Check `dt_out`:
    - Hierarchical (Standard): ~0.08
    - Quasi-Random (Standard): ~0.17
    - Gold (Both): ~0.01
- **`metrics.py`**: Match JSON names to new file patterns.

### 4. Implement Enhanced Modules

- **`coverage.py`**:
  - Import or re-implement `processing.input_vector` logic.
  - Compute 13 components for all valid ICs.
  - Fail if any component is undefined/NaN.
- **`curriculum.py`**:
  - Implement stage classification logic (Stage 0: $E<-0.5, L>0.5...$, etc.).
  - Calculate `tau_L` (Lyapunov time) if missing from metrics (or warn if expensive). *Optimization: Use pre-calculated metrics if available.*
- **`duplicates.py`**: Pairwise distance check on 13-component vectors.

### 5. Reporting + CLI

- **reporting.py**: Generate `READINESS_REPORT.md`.
- **cli.py**: Flags for `--check-curriculum`, `--check-vectors`.

### 6. Script Audit (New)

- Scan `3_Body_Problem/` for python scripts containing strings like `brutus_hierarchical_` or old glob patterns.
- Report which scripts might need updates to match the new `_gold_` naming convention.

## Severity Levels

- **FAIL**: Corrupt files, missing 1:1 correspondence (outside blacklist), NaN in Input Vector, physically impossible values ($m<0$).
- **WARNING**: Stage imbalance (e.g., "0 files in Stage 2"), outdated script patterns found, minor energy drift.
- **PASS**: Ready for training.
