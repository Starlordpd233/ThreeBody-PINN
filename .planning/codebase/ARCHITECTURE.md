# Architecture

## System Overview

This project implements a **three-body gravitational simulation and machine learning pipeline** with three major subsystems:

1. **Brutus Integrator** — High-precision N-body solver (C++)
2. **Simulation Pipeline** — End-to-end data generation and validation (Python)
3. **CTL-PINN System** — Physics-Informed Neural Network for trajectory prediction (Python/PyTorch)

## Architecture Pattern

**Pipeline architecture** — Sequential stages with file-based handoff. No server, no API. Each stage reads files from previous stages and writes output files.

```
┌─────────────┐    ┌──────────────┐    ┌─────────┐    ┌─────────┐    ┌──────────┐
│ IC Generator │───▶│ Prescreening │───▶│ Brutus  │───▶│ Metrics │───▶│ PINN     │
│   (Python)   │    │   (Python)   │    │  (C++)  │    │(Python) │    │(PyTorch) │
└─────────────┘    └──────────────┘    └─────────┘    └─────────┘    └──────────┘
     Stage 1            Stage 2          Stage 3        Stage 4       Stage 5
```

## Component Details

### 1. Brutus N-Body Integrator (`brutus_Newton-main/`)

- **Pattern:** Numerical integrator with Bulirsch-Stoer extrapolation
- **Key classes:** `Brutus`, `Bulirsch_Stoer`, `Cluster`, `Star`
- **Entry point:** `main.cpp` — CLI program, reads IC file, integrates, writes trajectory
- **Precision:** Arbitrary (GMP/MPFR), controlled by `tol` and `Lw` (word length)
- **Output:** Sequential snapshots at `dt_out` intervals

### 2. Simulation Pipeline (`simulation_data/`)

- **Stage 1 — IC Generation** (`Scripts/ic_generation/`)
  - `FINAL_ic_generator_enhanced.py` — Core IC generation (standard quasi-random + hierarchical)
  - `generate_enhanced_ics.py` — Entry point wrapper
- **Stage 2 — Prescreening** (`Validation/prescreening/`)
  - `stage2_prescreening_revised_auto.py` — Short leapfrog integration to reject unstable ICs
- **Stage 3 — Brutus Runners** (`Scripts/brutus_runners/`)
  - `run_brutus_both_type_simple.py` — Batch runner for both IC types
  - `run_brutus_hierarchical_only_mac_gold_standard.py` — Gold-standard hierarchical runs
- **Stage 4 — Metrics** (`Scripts/metrics_calculation/`)
  - `calculate_metrics.py` — Energy/momentum/angular momentum conservation metrics

### 3. CTL-PINN System (`pinn/`)

- **Architecture:** SQR-SkipResNet-SIREN (14 → 256×12 → 9)
  - `basic_architecture.py` — Model definition with SIREN activation, skip connections, LayerNorm
- **Data Pipeline:** `data-processing-pipeline-full.py` — IC vector computation (13 components), normalization, stage assignment
- **Data Handling Package:** `data-handling/`
  - `core/parsing.py` — Brutus/IC file parsers
  - `core/scaling.py` — Position/velocity scaling
  - `core/data_structures.py` — Data classes
  - `processing/input_vector.py` — IC vector computation
  - `processing/invariants.py` — Shape and velocity invariants
  - `processing/stage_assignment.py` — CTL curriculum stage assignment
  - `processing/rosenstein_lyapunov.py` — Lyapunov exponent estimation

### 4. Reference Code (`reference-code/`)

- `lyapunov/` — Julia-based Lyapunov exponent analysis
- `reference_NNs/` — 9 reference NN implementations (SIREN, DeepXDE, PINA, GravNN, HNN, etc.)

## Data Flow

```
IC files (.txt, 3 bodies × 7 fields)
    ↓ prescreening filter
Validated ICs
    ↓ Brutus integration
Trajectory files (.txt, timestamped snapshots, 30-40 digit precision)
    ↓ metrics extraction
Conservation metrics (JSON)
    ↓ data processing pipeline
IC vector (13 components) + trajectory → HDF5
    ↓ CTL stage assignment
Staged training data → PINN
```

## Entry Points

| Entry Point | Type | Purpose |
|-------------|------|---------|
| `brutus_Newton-main/brutus` | Binary | N-body integration |
| `simulation_data/Scripts/ic_generation/generate_enhanced_ics.py` | Script | Generate ICs |
| `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py` | Script | Prescreen ICs |
| `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py` | Script | Batch Brutus runs |
| `simulation_data/Scripts/metrics_calculation/calculate_metrics.py` | Script | Compute metrics |
| `pinn/data-processing-pipeline-full.py` | Script | PINN data preprocessing |
| `pinn/basic_architecture.py` | Script | PINN architecture (sanity check) |
