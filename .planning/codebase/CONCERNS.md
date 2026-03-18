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

### Missing Result Footers

- Many Brutus output files lack the optional `Result:` footer
- Must rely on folder defaults for parameter metadata
- Audit scripts exist at `simulation_data/Data/brutus_output/check missing results line/`

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
