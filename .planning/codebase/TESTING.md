# Testing Patterns

**Analysis Date:** 2026-04-27

## Test Framework

**Runner:**
- No test runner configured. No `pytest`, `unittest`, or C++ test framework installed at the project level.
- No `conftest.py`, `pytest.ini`, `tox.ini`, or `setup.cfg` in project root.
- Python packages present in `.venv/` include `pytest`, `unittest`, and `numpy.testing` as transitive dependencies, but no project test configuration exists.

**Assertion Library:**
- No dedicated assertion library. The minimal test code uses manual checks with `print()` and `if` statements.

**Run Commands:**
```bash
# No standard test commands. The closest equivalents:
python simulation_data/Data/testing_data/test_pipeline.py        # Integration test
cd brutus_Newton-main && make && ./test_libs                      # Library test
```

## Test File Inventory

**Project-owned test files: 2**

| File | Type | What it tests |
|------|------|---------------|
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
- Co-located with source for C++: `test_libs.cpp` in `brutus_Newton-main/`, `test.cpp` in `lib/Data_Handler/`
- Separate test data directory for Python: `simulation_data/Data/testing_data/test_pipeline.py`
- One project test file: `tests/test_phase12_validation.py` (Phase 12 validation test)

**Naming:**
- C++: `test_*.cpp` or `test.cpp` (inconsistent)
- Python: `test_pipeline.py`

**Expected structure (not yet present):**
```
# What a testing directory would look like (none exist currently)
simulation_data/tests/
brutus_Newton-main/tests/
pinn/tests/
```

## Test Structure

**`test_libs.cpp` (`brutus_Newton-main/test_libs.cpp`):**

```cpp
#include <iostream>
#define MPFR_USE_NO_MACRO
#define MPFR_USE_INTMAX_T
#include <gmp.h>
#include <mpfr.h>
#include "mpreal.h"

using namespace mpfr;

int main() {
    std::cout << "GMP version: " << gmp_version << std::endl;
    std::cout << "MPFR version: " << mpfr_get_version() << std::endl;
    
    mpreal::set_default_prec(128);
    mpreal x = "1.234567890123456789";
    std::cout << "mpreal test: " << x << std::endl;
    std::cout << "Libraries are working correctly!" << std::endl;
    
    return 0;
}
```

Pattern: Compile-and-run sanity check, no assertions, relies on visual inspection of output.

**`test_pipeline.py` (`simulation_data/Data/testing_data/test_pipeline.py`):**

- Orchestrated as four sequential steps: `step1_generate_ics()`, `step2_prescreening()`, `step3_run_brutus()`, `step4_verify()`
- Manual assertions via `validate_brutus_output()` which checks final timestep >= 9.5
- Uses `subprocess.run()` to execute Brutus binary
- Hardcoded parameters for fast testing (lower tolerances, larger dt)
- Graceful fallback if Brutus binary not built
- Output: prints PASS/FAIL per simulation, summary at end

**What the pipeline validates:**
1. IC files can be generated and parsed
2. Prescreening can process ICs (optional, skippable)
3. Brutus binary exists and can be executed
4. Brutus output files contain valid timestep data
5. Final simulation time exceeds threshold (9.5)

## Mocking

**Framework:** None. No mocking library used, no mock objects or stubs.

**Patterns:** Not applicable. The test_pipeline.py tests against real Brutus binary execution.

## Fixtures and Factories

**Test Data:**
- `simulation_data/Data/testing_data/test_pipeline.py` generates its own test ICs using `continuation_enhanced_ic_generation()` from `ic_generation_utils.py`
- Parameters: `N_STANDARD = 3`, `N_HIERARCHICAL = 3` small sample sizes
- No fixture files exist; test data is generated and cleaned up in `Data/testing_data/ic_raw/`, `ic_final/`, `brutus_output/` subdirectories (git-ignored)

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
- **None exist.** No individual Python module or C++ function has a unit test.
- All computational functions in `simulation_data/Validation/prescreening/`, `simulation_data/Scripts/metrics_calculation/`, `pinn/data-handling/core/`, etc., are untested.

**Integration Tests:**
- `simulation_data/Data/testing_data/test_pipeline.py` (407 lines) -- end-to-end pipeline test exercising IC generation, prescreening, Brutus execution, and output validation.
- `brutus_Newton-main/test_libs.cpp` (20 lines) -- library linking verification (GMP, MPFR, mpreal).

**E2E Tests:**
- Not used. The test_pipeline.py is the closest approximation.

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

**Test-like qualities:**
- Deterministic pass/fail outcomes per IC file
- Reproducible with seeded random sampling
- Audit trail via processing index

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

## Common Testing Patterns (if tests existed)

**Async Testing:**
Not applicable -- no async Python code in project.

**Error Testing:**
The `validate_brutus_output()` function in `test_pipeline.py:267-296` is the only exemplar of a test-like validation function. It follows this pattern:
- Return `(False, error_message)` on failure
- Return `(True, success_message)` on success
- Catch generic `Exception` with `(False, f"Validation error: {e}")`

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

### Low Priority / Non-Critical

7. **LaTeX compilation testing is manual:**
   - `simulation_data/Validation/` has LaTeX verification scripts (`verify_compile.py`, `verify_structure.py`, `verify_preamble.py`, `verify_content.py`) that check document structure and compilability
   - These are run manually, not in CI

8. **Reference code tests exist but are not project tests:**
   - DeepXDE, PyTorch, PINA, etc. have their own test suites but these validate the reference implementations, not project code

## How to Add Tests (Recommended Pattern)

Based on the project's conventions, new tests should follow:

1. **Location:** Create `tests/` directories at appropriate levels:
   - `simulation_data/tests/` for simulation pipeline tests
   - `pinn/tests/` for PINN pipeline tests
   - `brutus_Newton-main/tests/` for C++ tests

2. **Framework:** Install `pytest` (already in .venv) and create `conftest.py` files

3. **Naming:** Use `test_*.py` for Python tests, following existing `test_pipeline.py` pattern

4. **Fixtures:** Use `simulation_data/Data/testing_data/` (already git-ignored) for test data

5. **Path handling:** Use `pathlib.Path` and relative-to-project-root resolution:
   ```python
   PROJECT_ROOT = Path(__file__).resolve().parent.parent
   ```
   Do not hardcode `<home>/` paths.

6. **Assertions:** Use `assert` statements with descriptive messages or `pytest.raises()` for exception testing

7. **Scientific validation:** For physics correctness tests, use `np.testing.assert_allclose()` with appropriate relative/absolute tolerances

---

*Testing analysis: 2026-04-27*
