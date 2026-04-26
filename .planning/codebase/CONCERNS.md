# Concerns

## Technical Debt

### No Dependency Management

- **Issue:** No `requirements.txt`, `pyproject.toml`, or `setup.py`
- **Impact:** Difficult to reproduce environment; hidden dependency conflicts
- **Severity:** Medium

### Hardcoded Paths

- **Issue:** `brutus_Newton-main/makefile` has Mac-specific paths (`/opt/homebrew`, `<home>`)
- **Impact:** Won't build on other machines without modification
- **Severity:** Low (single-developer project)

### No Formal Training Script

- **Issue:** `pinn/basic_architecture.py` defines the model but no training loop exists in repo
- **Impact:** PINN training workflow is incomplete in the codebase
- **Severity:** High — this is the primary gap to address

### Duplicate/Stale Data Pipeline

- **Issue:** Two data processing approaches exist:
  1. `pinn/data-processing-pipeline-full.py` (56KB monolith, source of truth)
  2. `pinn/data-handling/` (modular package, ~partial implementation)
- **Impact:** Potential divergence between the two; unclear which to use for training
- **Severity:** Medium

## Data Integrity Concerns

### Result Footer Schema Variation (resolved as of 2026-04-26)

- **Footer presence**: All 15,028 Brutus output files contain a `Result:` footer (verified 2026-04-26 via `grep -l "^Result:"` and tail-5 check across all 4 output folders).
- **Schema variance**: The footer schema is not uniform — some files omit `eta`, and a small subset (219 files in `brutus_standard_quasi_random_gold_standard/`) omit both `eta` and `tol`. When `tol` is absent, fall back to folder defaults.
- **History**: An audit on 2025-12-24 (`simulation_data/Validation/audit_reports/footer_audit_20251224_170141.md`) found 2,470 files missing footers and 3,273 with partial (energy-field-less) footers. These were backfilled by `simulation_data/Scripts/debug/audit_and_backfill_brutus_result_footers.py`.
- **Reference**: Per-folder schema counts are in `simulation_data/Documentation/README.md` "Brutus Parameters by Variant".

### Standard Quasi-Random Gold Provenance

- No runner script in repo for standard quasi-random gold outputs
- Mixed provenance (multiple parameter sets in same folder)
- Treat as partial provenance unless recovered from external logs

### Hierarchical COM Offset

- Post-perturbation COM and total momentum are not exactly zero
- Must recenter/reboost before analysis if exact COM frame required
- Documented but easy to forget

### ID Gaps in Datasets

- Intentional gaps from generation continuation, prescreen rejection, failed Brutus runs
- Not a bug — but code must handle non-contiguous IDs

## Performance Concerns

### Brutus Timeout

- 3000-second timeout per simulation in batch scripts
- Some ICs may take much longer (chaotic regimes)
- No mechanism to resume interrupted simulations

### Data Processing Pipeline Scale

- `data-processing-pipeline-full.py` is 56KB — large monolith
- Processes all data in memory; may not scale to very large datasets

## Security

- **No secrets detected** — project is entirely offline
- No API keys, tokens, or credentials in codebase
- `.gitignore` covers `.venv/`, `.tmp/`, data files appropriately

## Fragile Areas

### Brutus Output Parsing

- `pinn/data-handling/core/parsing.py` (31KB) — complex parser with many edge cases
- Must handle 30-40 digit precision strings, optional footers, OS-variant paths
- Changes here can break the entire downstream pipeline

### IC Generation Randomness

- `FINAL_ic_generator_enhanced.py` (28KB) — complex sampling logic
- Sobol sequences with scrambling, hemisphere constraints, global scaling
- Subtle changes to sampling can shift the entire dataset distribution
