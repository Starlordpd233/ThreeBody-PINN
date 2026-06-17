# Testing Patterns

**Analysis Date:** 2026-06-10

## Test Framework

**Runner:**
- No project-wide test runner configured. No `pytest.ini`, `tox.ini`, or `setup.cfg` in project root.
- `tests/git_policy/test_git_policy.py` uses `unittest` (standard library).
- `tests/test_phase12_validation.py` uses a hand-rolled check/result accumulator (no framework dependency).
- `simulation_data/Data/testing_data/test_pipeline.py` uses `subprocess` and manual assertions.
- Python packages present in `.venv/` include `pytest` as a transitive dependency, but no project test configuration uses it.

**Assertion Library:**
- `unittest.TestCase` assertions in `tests/git_policy/test_git_policy.py` (`assertEqual`, `assertNotEqual`, `assertIn`, `assertTrue`, `assertFalse`)
- Manual `check(name, condition, detail)` accumulator pattern in `tests/test_phase12_validation.py`
- Manual `print()` + `if` checks in older test files

**Run Commands:**
```bash
# Phase 12 content-integrity tests
python3 tests/test_phase12_validation.py

# Git policy unit tests
python3 -m unittest tests/git_policy/test_git_policy.py

# Legacy pipeline integration test
python simulation_data/Data/testing_data/test_pipeline.py

# C++ library link test
cd brutus_Newton-main && make && ./test_libs
```

## Test File Inventory

**Project-owned test files: 4**

| File | Type | What it tests |
|------|------|---------------|
| `tests/test_phase12_validation.py` | Content-integrity test | Structural properties of `pinn_architecture.md` against Phase 12 plan requirements: section order, inactive-content absence, source-issues metadata, bibliography, index entry |
| `tests/git_policy/test_git_policy.py` | Unit tests (unittest) | Git policy enforcement scripts: `validate_commit_msg.py`, `validate_staged_paths.py`, `guard_agent_git_command.py` |
| `brutus_Newton-main/test_libs.cpp` | C++ compilation test | Verifies GMP, MPFR, and mpreal libraries link correctly |
| `simulation_data/Data/testing_data/test_pipeline.py` | Python integration test | End-to-end: IC generation -> prescreening -> Brutus execution -> output validation |

**C++ library-level tests (included but minimal):**
| File | Purpose |
|------|---------|
| `brutus_Newton-main/lib/Data_Handler/test.cpp` | Data_Handler unit (standalone test executable for parsing) |
| `brutus_Newton-main/mplib/Data_Handler/test.cpp` | mpreal Data_Handler variant unit |

**Third-party reference tests (not project tests):**
- `reference-code/reference_NNs/` contains test suites for DeepXDE, PyTorch, PINA, GravNN, etc. These are reference implementations, not project code.

## Test File Organization

**Location:**
- `tests/` at repo root -- primary test directory (Phase 12 content validation, git-policy unit tests)
- Co-located with source for C++: `test_libs.cpp` in `brutus_Newton-main/`, `test.cpp` in `lib/Data_Handler/`
- Separate test data directory for Python: `simulation_data/Data/testing_data/test_pipeline.py`

**Naming:**
- Python: `test_*.py` (consistent across both `tests/` and data testing)
- C++: `test_*.cpp` or `test.cpp`

**Package structure:**
```
tests/
├── __pycache__/
├── git_policy/
│   ├── __init__.py
│   └── test_git_policy.py
└── test_phase12_validation.py
```

## Test Structure

### `tests/test_phase12_validation.py` (280 lines)

Content-integrity detector pattern — verifies that converted markdown artifacts satisfy structural requirements from the Phase 12 plan. Uses a module-level accumulator:

```python
results = {"pass": 0, "fail": 0, "errors": []}

def check(name, condition, detail=""):
    if condition:
        results["pass"] += 1
        print(f"  PASS: {name}")
    else:
        results["fail"] += 1
        msg = f"  FAIL: {name}"
        if detail:
            msg += f" ({detail})"
        print(msg)
        results["errors"].append(msg)
```

Check IDs match plan acceptance criteria: `CLEAN-01`, `FIDEL-05`, `FIDEL-06`, `CROSS-01`, `CROSS-02`, `FIDEL-03`.

Several checks are marked SKIP (report artifact retired after v1.3 closure): `CLEAN-03`, `CAND-01`, `AUDIT-01`, `AUDIT-02`, `AUDIT-03`.

**What it validates:**
- `pinn_architecture.md` exists and exceeds 200 lines (`CLEAN-01`)
- Numbered sections appear in correct order: `# 1.` through `# 10.` (`FIDEL-05`)
- Inactive terms absent from faithful body (`FIDEL-06`): `"Input Vector Formulation"`, `"14-dimensional injective"`, `"Advanced Training Dynamics"`, `"Curriculum-Aware Energy Regularization"`
- Source Issues metadata section present (`CROSS-01`)
- Bibliography section present with entries (`FIDEL-03`)
- Conversion index (`pinn_instruction/markdown_conversion/README.md`) has Phase 12 entry (`CROSS-02`)

### `tests/git_policy/test_git_policy.py` (179 lines)

Standard `unittest.TestCase` tests for git policy enforcement scripts. Uses subprocess to invoke the validator scripts with controlled inputs and environment variables:

```python
def validate_message(message, env=None):
    with tempfile.NamedTemporaryFile("w", delete=False) as handle:
        handle.write(message)
        path = handle.name
    return run_python(COMMIT_VALIDATOR, [path], env=env)
```

Tests cover: valid agent commit acceptance, uppercase subject rejection, throwaway subject rejection, scope validation, body requirements, and attribution trailer enforcement.

### `brutus_Newton-main/test_libs.cpp` (20 lines)

Compile-and-run sanity check. No assertions; relies on visual inspection of output. Verifies GMP, MPFR, and mpreal link correctly and can perform arbitrary-precision arithmetic.

### `simulation_data/Data/testing_data/test_pipeline.py` (407 lines)

Four sequential steps: `step1_generate_ics()`, `step2_prescreening()`, `step3_run_brutus()`, `step4_verify()`. Manual assertions via `validate_brutus_output()` which checks final timestep >= 9.5. Uses `subprocess.run()` to execute Brutus binary. Graceful fallback if Brutus binary not built.

## Mocking

**`tests/git_policy/test_git_policy.py`:**
- No mock objects. Tests invoke the real validator scripts via `subprocess.run()` with controlled `env` dicts.
- `GIT_AGENT_COMMIT`, `GIT_POLICY_STAGED_FILES` environment variables injected per test to simulate different commit contexts.

**`simulation_data/Data/testing_data/test_pipeline.py`:**
- No mocking. Tests against real Brutus binary execution.

## Fixtures and Factories

**Test Data:**
- `simulation_data/Data/testing_data/test_pipeline.py` generates its own test ICs using `continuation_enhanced_ic_generation()` from `ic_generation_utils.py`
- Parameters: `N_STANDARD = 3`, `N_HIERARCHICAL = 3` small sample sizes
- No fixture files; test data is generated and cleaned up in `Data/testing_data/ic_raw/`, `ic_final/`, `brutus_output/` subdirectories (git-ignored)
- `tests/test_phase12_validation.py` reads live project artifacts directly (no fixtures)
- `tests/git_policy/test_git_policy.py` uses `tempfile.NamedTemporaryFile` for commit message inputs (no persistent fixtures)

**Location:**
- `simulation_data/Data/testing_data/` -- git-ignored, regenerated on each test run

## Coverage

**Requirements:** None enforced. No `.coveragerc`, no coverage tool configured.

**View Coverage:**
```bash
# No coverage tooling set up. To add:
pip install pytest pytest-cov
# Then: pytest --cov=simulation_data --cov=pinn --cov-report=html
```

## Test Types

**Unit Tests:**
- `tests/git_policy/test_git_policy.py` -- unit tests for git policy scripts (`validate_commit_msg.py`, `validate_staged_paths.py`, `guard_agent_git_command.py`)
- `brutus_Newton-main/lib/Data_Handler/test.cpp` -- Data_Handler parsing unit (compile and run manually)
- All computational functions in `simulation_data/Validation/prescreening/`, `simulation_data/Scripts/metrics_calculation/`, `pinn/data-handling/core/` remain untested.

**Content-Integrity Tests:**
- `tests/test_phase12_validation.py` -- verifies structural properties of generated markdown artifacts against plan acceptance criteria. Pattern introduced in Phase 12 for v1.4 milestone work.

**Integration Tests:**
- `simulation_data/Data/testing_data/test_pipeline.py` (407 lines) -- end-to-end pipeline test exercising IC generation, prescreening, Brutus execution, and output validation.
- `brutus_Newton-main/test_libs.cpp` (20 lines) -- library linking verification (GMP, MPFR, mpreal).

**E2E Tests:**
- Not used. `test_pipeline.py` is the closest approximation.

**Scientific Validation Tests (domain-specific correctness, not software testing):**
- `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py` -- leapfrog N-body integration to validate IC stability (680 lines)
- `simulation_data/Validation/dataset_readiness_checks/` -- comprehensive data validation system with 13 modules (across ~20 Python files)
- `simulation_data/Scripts/debug/check_brutus_completeness.py` -- data completeness checker
- `simulation_data/Scripts/debug/audit_and_backfill_brutus_result_footers.py` -- Brutus output metadata audit and backfill

## Validation System (Scientific Correctness)

This is the primary quality assurance mechanism in the project, distinct from software testing.

### Prescreening Validation

**File:** `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py`

**What it validates:**
1. **Static criteria** (fast pre-filter):
   - Virial ratio within percentile-based thresholds (default: 1st to 99.5th percentile)
   - Angular momentum magnitude
2. **Dynamic criteria** (leapfrog integration):
   - Minimum pairwise separation during integration > `MIN_DISTANCE_THRESHOLD = 0.01`
   - Energy conservation: relative error < `ENERGY_ERROR_THRESHOLD = 0.01` (1%)
3. **Integration parameters:** `TMAX = 1.0`, `DT = 0.0001`

**Key design patterns:**
- Numba JIT-compiled computational kernels (`compute_forces`, `leapfrog_step`, `integrate_and_check`)
- Processing index with SHA256 hashing for incremental reprocessing
- Adaptive threshold computation from data percentiles
- Failure categorization: `min_separation`, `energy_conservation`, `static_check`
- Results serialized to JSON processing index files: `processing_index_ic_hierarchical.json`, `processing_index_ic_standard_quasi_random.json`

### Dataset Readiness Checks

**Location:** `simulation_data/Validation/dataset_readiness_checks/`

**Architecture:**
- `validator.py` -- orchestrator class, loads all modules, validates per-variant
- `config.py` -- `ValidationConfig` dataclass with thresholds, paths, enabled modules
- `modules/` -- 13 validation modules:
  - `correspondence.py` -- IC-to-Brutus file pairing
  - `file_format.py` -- IC and Brutus format validation
  - `completeness.py` -- final timestep >= threshold (9.5)
  - `metadata.py` -- Result footer parsing
  - `physics.py` -- COM, momentum conservation checks
  - `parameters.py` -- Brutus parameter consistency
  - `metrics.py` -- conservation metric validation
  - `blacklist.py` -- known problematic IC filtering
  - `coverage.py` -- parameter space coverage analysis
  - `curriculum.py` -- stage assignment validation
  - `temporal.py` -- time series structure validation
  - `duplicates` -- (registered but not yet implemented)

**Output:**
- JSON reports per run
- Markdown reports via `reports/markdown.py`
- CSV exports
- Audit files in `Validation/audit_reports/`

### Brutus Output Validation

**Embedded in `test_pipeline.py:267-296`:**

```python
def validate_brutus_output(output_path: Path, time_threshold: float = 9.5) -> tuple:
    """Validate Brutus output file."""
    # Checks: file existence, timestep line parsing, final timestep >= threshold
    # Returns: (bool, message_string)
```

Pattern: manual file parsing with regex, float comparison, boolean-plus-message return tuple.

## CI/CD Testing Setup

**Status: No testing CI/CD.**

The `.github/workflows/` directory contains only Gemini AI agent dispatch/review/triage workflows:
- `gemini-dispatch.yml` -- route issues to Gemini
- `gemini-invoke.yml` -- invoke Gemini agent
- `gemini-review.yml` -- Gemini PR review
- `gemini-triage.yml` -- issue triage
- `gemini-scheduled-triage.yml` -- periodic triage

None of these execute tests, build code, or run validation scripts.

## Known Test Gaps

### Critical Gaps (High Priority)

1. **No unit tests for any computational kernel:**
   - `simulation_data/Validation/prescreening/` -- `compute_forces()`, `leapfrog_step()`, `integrate_and_check()` -- all JIT-compiled with no test harness
   - `simulation_data/Scripts/metrics_calculation/calculate_metrics.py` -- energy, momentum, angular momentum computation untested
   - `simulation_data/Scripts/ic_generation/ic_generation_utils.py` -- `EnhancedThreeBodySampler` class with 1000+ lines, no tests
   - `pinn/data-handling/core/parsing.py` -- IC and Brutus file parsing, no tests
   - `pinn/data-handling/core/scaling.py` -- trajectory scaling, no tests
   - `pinn/data-handling/processing/invariants.py` -- physical invariant computation, no tests
   - `pinn/data-handling/processing/input_vector.py` -- 13-component IC vector construction, no tests
   - `pinn/data-handling/core/com_transform_brutus.py` -- COM frame transformation, no tests

2. **No regression tests for data pipeline:**
   - `pinn/data-processing-pipeline-full.py` -- monolithic pipeline, no test
   - `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py` -- no test
   - No golden-data comparison tests exist

3. **No PINN architecture tests:**
   - `pinn/basic_architecture.py` -- `SQRSkipResNetSIREN` model has an `if __name__ == "__main__"` block for interactive testing but no automated assertions
   - Forward pass shape validation is done via `print()` only
   - No gradient correctness tests
   - No loss function tests

### Moderate Gaps

4. **Validation system not itself tested:**
   - `simulation_data/Validation/dataset_readiness_checks/validator.py` orchestrates 13 modules but has no tests for the orchestrator itself
   - Module-level functions have no unit tests

5. **Brutus build not verified in CI:**
   - `brutus_Newton-main/Makefile` has no `test` target
   - `test_libs.cpp` must be manually compiled and run

6. **No test data fixtures:**
   - No known-answer IC files with expected Brutus outputs
   - No canonical test dataset for deterministic comparison

7. **Content-integrity test pattern not applied to `ctl_instruction.md`:**
   - `tests/test_phase12_validation.py` pattern covers `pinn_architecture.md` only
   - `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` has no equivalent structural test

### Low Priority / Non-Critical

8. **LaTeX compilation testing is manual:**
   - `simulation_data/Validation/` has LaTeX verification scripts (`verify_compile.py`, `verify_structure.py`, `verify_preamble.py`, `verify_content.py`) that check document structure and compilability
   - These are run manually, not in CI

9. **Reference code tests exist but are not project tests:**
   - DeepXDE, PyTorch, PINA, etc. have their own test suites but these validate the reference implementations, not project code

## How to Add Tests (Recommended Patterns)

**Content-integrity tests (follow `tests/test_phase12_validation.py` pattern):**
- Place in `tests/` at repo root
- Use the `check(name, condition, detail)` accumulator pattern
- Name checks after acceptance-criteria IDs from the relevant phase plan
- Read live project artifacts directly; no fixtures needed for structural checks
- Include a `main()` that prints pass/fail summary and exits non-zero on failure

**Git-policy / tooling unit tests (follow `tests/git_policy/test_git_policy.py` pattern):**
- Use `unittest.TestCase`
- Invoke scripts via `subprocess.run()` with controlled environment variables
- Place in `tests/<domain>/` subdirectory with `__init__.py`

**Path handling in all new tests:**
```python
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[N]
```
Never hardcode `<home>/` paths.

**Scientific validation tests:**
- For physics correctness, use `np.testing.assert_allclose()` with appropriate relative/absolute tolerances
- Place in `simulation_data/tests/` when created

---

*Testing analysis: 2026-06-10*
