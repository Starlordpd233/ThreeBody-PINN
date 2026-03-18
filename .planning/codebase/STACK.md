# Stack

## Languages

| Language | Usage | Version / Notes |
|----------|-------|-----------------|
| **C++** | Brutus N-body integrator | C++11 (`-std=c++11`), compiled with `g++` |
| **Python** | Simulation pipeline, PINN, data processing | 3.x (venv at `.venv/`) |
| **Julia** | Reference Lyapunov analysis | Notebooks + `.jl` scripts |

## C++ Dependencies (Brutus)

| Library | Purpose | Install |
|---------|---------|---------|
| **GMP** (`libgmpxx`, `libgmp`) | Arbitrary-precision integer/rational arithmetic | Homebrew (`/opt/homebrew`) |
| **MPFR** (`libmpfr`) | Arbitrary-precision floating-point | Homebrew |
| **mpreal** | C++ wrapper for MPFR | Source at `~/src/mpreal` |

Compiler flags: `-O3 -std=c++11 -DMPFR_USE_NO_MACRO -DMPFR_USE_INTMAX_T`

## Python Dependencies (Inferred)

| Library | Purpose |
|---------|---------|
| **NumPy** | Numerical computation, IC generation, data processing |
| **SciPy** | Sobol sequences (`scipy.stats.qmc`), scientific computation |
| **PyTorch** | PINN neural network (SIREN architecture) |
| **h5py** | HDF5 data storage for PINN training data |
| **matplotlib** | Visualization |
| **json** | Metrics and config handling |

> **Note:** No `requirements.txt` or `pyproject.toml` exists. Dependencies are inferred from imports.

## Build System

- **Brutus:** GNU Make (`brutus_Newton-main/makefile`), macOS M2-specific paths
- **Python:** No package manager; scripts run directly
- **No CI/CD pipeline**

## Configuration

- Brutus parameters passed as CLI args: `./brutus <tol> <Lw> <t_begin> <t_end> <dt_out> <N> <ic_file>`
- Python scripts use hardcoded paths and constants (some accept CLI args)
- `.vscode/` settings present in `simulation_data/` and `pinn/`
