# Testing

## Testing Framework

**No formal test framework in place.** No pytest, unittest, or any testing infrastructure detected.

## Validation Approach

Instead of traditional unit/integration tests, this project uses **data validation scripts**:

### Prescreening (Stage 2 Validation)

- `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py`
- Short leapfrog integration to reject unstable ICs
- Criteria: energy error < 0.01, minimum distance > 0.01
- Outputs: processing index JSON files per IC type

### Dataset Readiness Checks

- `simulation_data/Validation/dataset_readiness_checks/` — Pre-training validation
- Verifies dataset completeness and quality before PINN training

### Audit Reports

- `simulation_data/Validation/audit_reports/` — Post-hoc data quality audits
- Detects Result-footer schema variation (eta/tol presence) and incomplete simulations; current state: all files have footers — see `.planning/codebase/CONCERNS.md` "Result Footer Schema Variation"

### Analysis Scripts

- `simulation_data/Validation/analysis/` — Analytical validation
- Conservation metric analysis, trajectory quality assessment

## Conservation Metrics

- `simulation_data/Scripts/metrics_calculation/calculate_metrics.py`
- Computes energy, momentum, angular momentum drift per simulation
- Outputs JSON metrics to `simulation_data/Data/metrics/`

## Architecture Sanity Check

- `pinn/basic_architecture.py` can be run standalone as a sanity check
- Verifies model dimensions and forward pass succeed

## Known Test Artifacts

- `brutus_Newton-main/testcase.txt` — Brutus test input
- `brutus_Newton-main/test_output.txt` — Expected output reference
- `simulation_data/Data/testing_data/` — Test dataset samples

## Coverage

No code coverage measurement. Validation is by physical correctness (conservation laws, trajectory completeness) rather than code-level testing.
