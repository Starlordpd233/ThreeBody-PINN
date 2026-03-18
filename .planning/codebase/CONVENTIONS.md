# Conventions

## Code Style

### Python

- **No formal linter/formatter** configured (no `pyproject.toml`, `.flake8`, etc.)
- Generally follows PEP 8 with some deviations
- Type hints not used consistently
- Docstrings present in some files, absent in others
- Scripts tend to use `if __name__ == "__main__"` pattern

### C++

- C++11 standard
- Class-based design pattern (header + implementation pairs)
- Public member access for data classes (`Star`, `Cluster`)
- No namespaces used
- MPFR type aliases for numerical precision

## Naming Patterns

| Context | Pattern | Examples |
|---------|---------|----------|
| Python scripts | `snake_case` | `calculate_metrics.py`, `run_brutus_both_type_simple.py` |
| Python functions | `snake_case` | `parse_brutus_output()`, `compute_energy()` |
| Python classes | `PascalCase` | `SimulationResult`, `TrajectoryData` |
| C++ classes | `PascalCase` | `Brutus`, `Bulirsch_Stoer`, `Cluster`, `Star` |
| C++ files | `PascalCase` | `Brutus.cpp`, `Bulirsch_Stoer.cpp` |
| Data folders | `snake_case` | `ic_hierarchical`, `brutus_standard_quasi_random` |
| Data files | `snake_case_{id}` | `ic_hierarchical_0001.txt` |

## Error Handling

- **Brutus C++:** Writes `Result:` footer with error metrics; no structured error codes
- **Python scripts:** Mix of `try/except`, print statements, and graceful degradation
- **Prescreening:** Explicit rejection criteria (energy error, minimum distance) with JSON logging
- **No centralized error handling or logging framework**

## Constants and Configuration

- **Physical constants:** `G = 1` (natural units), hardcoded
- **Brutus parameters:** Passed as CLI arguments, no config file
- **Pipeline defaults:** Hardcoded in each script (epsilon, velocity_scale, thresholds)
- **PINN architecture:** Hardcoded hyperparameters in `basic_architecture.py`

## File Parsing Patterns

- **Brutus output parsing:** Custom parser in `pinn/data-handling/core/parsing.py`
- **High-precision values:** Parsed as strings or `Decimal` when exact precision matters
- **Completeness check:** `final_timestamp >= 9.5` (mandatory rule)
- **Result footer:** Treated as optional metadata, never relied upon for logic
