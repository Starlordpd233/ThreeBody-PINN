# Three-Body Problem Simulation and CTL-PINN Training Stack

A complete software stack for simulating three-body gravitational systems and training Curriculum-Trained Physics-Informed Neural Networks (CTL-PINNs) to predict their trajectories.

## Overview

This repository implements a full pipeline from initial condition generation through high-precision N-body integration to neural network training:

- **Brutus**: A C++ N-body integrator with arbitrary-precision arithmetic (GMP/MPFR)
- **Python Pipeline**: IC generation, dynamic prescreening, batch simulation, and metrics extraction
- **CTL-PINN**: A SQR-SkipResNet-SIREN architecture trained with curriculum learning

The system produces and processes ~15,000 high-fidelity three-body trajectories suitable for training machine learning models.

## Repository Layout

```
<home>/Desktop/cursor/
├── 3_Body_Problem/              # Simulation pipeline, datasets, and utilities
│   ├── final_stage_ic_datasets/ # Prescreened initial conditions
│   ├── brutus_output/           # High-precision trajectory outputs
│   ├── prescreen_stage2/        # Dynamic stability filtering
│   ├── brutus_metrics/          # Energy/momentum conservation analysis
│   └── data_documentation/      # Dataset specifications
├── brutus_Newton-main/          # C++ N-body integrator (Bulirsch-Stoer)
├── pinn/                        # PINN architecture and data processing
├── pinn_instruction/            # Architecture plans and CTL methodology docs
├── paper_templates/             # LaTeX templates (MDPI)
├── reference-code/              # Lyapunov analysis and NN baselines
└── brutus_simulation_documentation/  # Additional documentation
```

## Pipeline Summary

The data processing pipeline consists of five stages:

```
Stage 1: IC Generation → Stage 2: Prescreening → Stage 3: Brutus Integration → Stage 4: Metrics → Stage 5: PINN Preprocessing
```

### Stage 1: Initial Condition Generation

- **Scripts**: `FINAL_ic_generator_enhanced.py`, `generate_enhanced_ics.py`
- **Hierarchical**: Stable configurations (inner binary + outer third body)
- **Standard**: Sobol quasi-random sampling across configuration space

### Stage 2: Dynamic Prescreening

- **Script**: `prescreen_stage2/stage2_prescreening_revised_auto.py`
- Rejects unstable ICs using short leapfrog integration
- Filters by: energy error < 1%, minimum separation > 0.01, virial ratio [0.001, 2.0]

### Stage 3: Brutus Integration

- **Scripts**: `run_brutus_both_type_simple.py`, `run_brutus_hierarchical_only_mac_gold_standard.py`
- Produces high-precision trajectory snapshots (30-40 significant digits)

### Stage 4: Metrics Extraction

- **Script**: `brutus_metrics/calculate_metrics.py`
- Computes energy conservation, momentum drift, angular momentum

### Stage 5: PINN Preprocessing

- **Script**: `pinn/data-processing-pipeline-full.py`
- Computes physical invariants, normalizes data, assigns curriculum stages

## Brutus Simulator (C++)

Brutus implements a Bulirsch-Stoer integrator with arbitrary-precision arithmetic.

### Dependencies

- GMP: https://gmplib.org/
- MPFR: http://www.mpfr.org/
- MPFR C++: http://www.holoborodko.com/pavel/mpfr/
- MPREAL: https://github.com/advanpix/mpreal/

### Build

```bash
cd brutus_Newton-main
make clean
make
```

### Run

```bash
./brutus tolerance word_length t_begin t_end dt_out N ic_file > output.txt
```

Example: `./brutus 1e-15 130 0 10 0.08 3 ic.txt > trajectory.txt`

## PINN System

### Architecture: SQR-SkipResNet-SIREN

A physics-informed network designed for chaotic N-body dynamics:

| Hyperparameter | Value |
|----------------|-------|
| Input dimension | 14 (t + 13-component IC vector) |
| Output dimension | 9 (3D positions for 3 bodies) |
| Hidden layers | 12 |
| Hidden dimension | 256 |
| Activation | SIREN (sinusoidal) |
| Skip connections | Power-enhanced (p=2), LayerNorm on odd layers |
| first_omega_0 | 30.0 |
| hidden_omega_0 | 1.0 |

### IC Vector (13 components)

The network conditions on a normalized 13-dimensional initial condition vector:
- Masses (m1, m2, m3) - normalized mass fractions
- Total energy (E) - normalized
- Angular momentum (L_norm) - normalized
- Virial ratio (Q) - normalized
- Minimum separation (s_min) - normalized
- Shape invariants (I1, I2, I3)
- Velocity angles (theta1, theta2)
- Moment of inertia (I_norm) - normalized

### Curriculum Training (CTL)

Trains progressively through difficulty stages:

- **Stage 0-1**: Stable hierarchical systems (high binding energy, high angular momentum)
- **Stage 2**: High-resolution stable orbits
- **Stage 3-4**: Chaotic quasi-random systems (progressively harder)
- **Stage 5**: High-resolution chaotic trajectories
- **Stage 6**: Near-collision and extreme cases

Each stage includes replay of all previous stages.

## Datasets and Formats

### Initial Condition Format

```
m1 x1 y1 z1 vx1 vy1 vz1
m2 x2 y2 z2 vx2 vy2 vz2
m3 x3 y3 z3 vx3 vy3 vz3
```

### Brutus Output Format

```
t N t_cpu
m1 x1 y1 z1 vx1 vy1 vz1
m2 x2 y2 z2 vx2 vy2 vz2
m3 x3 y3 z3 vx3 vy3 vz3

[t_next N t_cpu_next]
...

[optional] Result: filename=... N=... t_begin=... t_end=... dt=... tol=... Lw=... t_cpu=... E_initial=... E_final=... dE/E=...
```

### Dataset Variants

| Folder | Type | Files |
|--------|------|-------|
| `ic_hierarchical/` | IC | 4,857 |
| `ic_hierarchical_for_gold_standard/` | IC | 4,857 |
| `ic_standard_quasi_random/` | IC | 2,749 |
| `ic_standard_quasi_random_for_gold_standard/` | IC | 2,565 |
| `brutus_hierarchical/` | Trajectory | 4,857 |
| `brutus_hierarchical_gold_standard/` | Trajectory | 4,857 |
| `brutus_standard_quasi_random/` | Trajectory | 2,749 |
| `brutus_standard_quasi_random_gold_standard/` | Trajectory | 2,565 |

**Note**: The folder determines the dataset variant (gold vs. standard). File names do not encode "gold".

### Brutus Parameters by Variant

| Variant | Tolerance | Word Length | dt_out |
|---------|-----------|-------------|--------|
| Hierarchical | 1e-15 | 130 | 0.08 |
| Standard quasi-random | 1e-13 | 118 | 0.17 |
| Hierarchical gold | 1e-13 | 130 | 0.01 |
| Standard gold | 1e-13 / 1e-14 | 130 | 0.01 |

## Physical Conventions

- **Units**: Natural units with G = 1, total mass ≈ 3
- **Time range**: 0 to 10 code units
- **Dimensionality**: Full 3D (not planar)
- **Standard ICs**: Masses = 1.0 each, COM = 0, momentum = 0
- **Hierarchical ICs**: Varying masses, COM/momentum perturbed (σ=0.01)

## Running the Pipeline

```bash
# Generate initial conditions
python 3_Body_Problem/generate_enhanced_ics.py

# Stage 2 prescreening
python 3_Body_Problem/prescreen_stage2/stage2_prescreening_revised_auto.py

# Batch simulations (both types)
python 3_Body_Problem/run_brutus_both_type_simple.py

# Gold-standard hierarchical runs
python 3_Body_Problem/run_brutus_hierarchical_only_mac_gold_standard.py

# Extract metrics
python 3_Body_Problem/brutus_metrics/calculate_metrics.py

# Preprocess for PINN training
python pinn/data-processing-pipeline-full.py --input /path/to/preprocessed.h5 --output_dir /path/to/stage_data

# Verify architecture
python pinn/basic_architecture.py
```

## Key Files

| Purpose | Location |
|---------|----------|
| IC Generator | `3_Body_Problem/FINAL_ic_generator_enhanced.py` |
| Prescreening | `3_Body_Problem/prescreen_stage2/stage2_prescreening_revised_auto.py` |
| Brutus Runner | `3_Body_Problem/run_brutus_both_type_simple.py` |
| Gold Runner | `3_Body_Problem/run_brutus_hierarchical_only_mac_gold_standard.py` |
| Metrics | `3_Body_Problem/brutus_metrics/calculate_metrics.py` |
| Architecture | `pinn/basic_architecture.py` |
| Data Pipeline | `pinn/data-processing-pipeline-full.py` |
| Dataset Docs | `3_Body_Problem/data_documentation/DATASET_DOCUMENTATION.md` |

## Known Caveats

1. **Result footers are optional**: ~32% of files lack the `Result:` footer. Use final timestep ≥ 9.5 for completeness checks.

2. **ID gaps exist**: Caused by prescreen rejection, generation continuation, and failed simulations.

3. **Parameter heterogeneity**: Multiple tolerance/word-length combinations exist within folders.

4. **OS path variance**: Result footers may contain macOS or Windows paths—do not use for mapping.

5. **Hierarchical COM offset**: Post-perturbation COM/momentum are not exactly zero; recenter if needed.

## References

- **Brutus**: PhD thesis by Tjarda Boekholt (Leiden Observatory)
- **SIREN**: [Sinusoidal Representation Networks](https://arxiv.org/abs/2008.02265)
- **CTL-PINN**: Curriculum training methodology documented in `pinn_instruction/`

## License

See individual components for their respective licenses.
