# Three-Body Problem Simulation Data: Dataset Documentation

**Generated:** 2025-12-23 | **Last Updated:** 2026-04-26
**Dataset Location:** `<home>/Desktop/3_body_problem/simulation_data/`
**Path Convention:** Unless otherwise specified, paths in this document are relative to the repo root (e.g., start with `simulation_data/`).

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Overview](#overview)
3. [Folder Structure](#folder-structure)
4. [Dataset Variants and Inventory](#dataset-variants-and-inventory)
5. [File Naming Conventions and Mapping](#file-naming-conventions-and-mapping)
6. [File Schemas](#file-schemas)
7. [Physical Conventions and Units](#physical-conventions-and-units)
8. [Pipeline and Provenance](#pipeline-and-provenance)
9. [Brutus Parameters by Variant](#brutus-parameters-by-variant)
10. [Quality Control and Validation](#quality-control-and-validation)
11. [Known Anomalies and Gotchas](#known-anomalies-and-gotchas)
12. [Minimal Parsing Examples](#minimal-parsing-examples)
13. [References](#references)
14. [Changelog](#changelog)

---

## Quick Start

### Running the Pipeline

```bash
# Stage 1: Generate ICs
python3 simulation_data/Scripts/ic_generation/generate_ics.py

# Stage 2: Prescreen
python3 simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py

# Stage 3: Run Brutus (requires compiled brutus binary)
python3 simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py

# Stage 4: Calculate metrics
python3 simulation_data/Scripts/metrics_calculation/calculate_metrics.py
```

### Environment Setup

Raw IC storage is external to the repository. Set the `IC_RAW_DIR` environment variable before running Stage 1 or Stage 2 scripts:

```bash
export IC_RAW_DIR=/path/to/ic_raw  # Expected subdirs: ic_hierarchical/, ic_standard_quasi_random/
```

### Related Documentation

- [Root README](../README.md) - Project overview and architecture
- [PINN Pipeline](../pinn/data-processing-pipeline-full.py) - ML data preprocessing

---

## Overview

This folder contains the complete data pipeline for the three-body simulation project. It handles:
- **Stage 1**: Initial Condition (IC) generation
- **Stage 2**: Prescreening to filter unstable systems
- **Stage 3**: High-precision Brutus integration
- **Stage 4**: Metrics calculation

The pipeline produces training data for the PINN (Physics-Informed Neural Network) system in the parent `pinn/` directory.

This dataset contains initial conditions (ICs) and corresponding high-precision N-body integration outputs for the **three-dimensional (3D) three-body problem** in natural units. The data was generated using:

- **IC Generation:** Enhanced Sobol-based quasi-random sampling with hierarchical system generation
- **Prescreening:** Stage 2 dynamic stability filtering with adaptive thresholds
- **Integration:** Brutus N-body simulator (Bulirsch-Stoer with GMP/MPFR arbitrary precision)

The dataset is organized into two main categories:
- **Hierarchical systems:** Stable configurations with inner binary + outer third body
- **Standard quasi-random:** Uniformly sampled configuration space

### Dataset Sizes

| Category | Size |
|----------|------|
| Final-stage IC datasets | ~59 MB |
| Brutus output datasets | ~4.8 GB |
| **Total** | **~4.86 GB** |

---

## Folder Structure

```
simulation_data/
├── Data/
│   ├── ic_raw/                        # Raw ICs (EXTERNALIZED - set IC_RAW_DIR env var)
│   ├── ic_final/                      # Prescreened ICs (Stage 2 output, 2 folders)
│   │   ├── ic_hierarchical/
│   │   └── ic_standard_quasi_random/
│   ├── brutus_output/                 # Integrated trajectories (Stage 3 output)
│   │   ├── brutus_hierarchical/
│   │   ├── brutus_hierarchical_gold_standard/
│   │   ├── brutus_standard_quasi_random/
│   │   └── brutus_standard_quasi_random_gold_standard/
│   ├── metrics/                       # Stage 4 metrics
│   │   └── sim_result_metric_*/
│   └── testing_data/                  # Test ICs/outputs
├── Scripts/
│   ├── ic_generation/                 # Stage 1 scripts
│   │   ├── ic_generation_utils.py
│   │   └── generate_ics.py
│   ├── brutus_runners/                # Stage 3 scripts
│   │   ├── run_brutus_both_type_simple.py
│   │   └── run_brutus_hierarchical_only_mac_gold_standard.py
│   ├── metrics_calculation/           # Stage 4 scripts
│   │   ├── calculate_metrics.py
│   │   └── calculate_brutus_metrics.py
│   ├── debug/                         # Debug utilities
│   └── archived/                      # Deprecated scripts
├── Validation/
│   ├── dataset_readiness_checks/      # Validation framework
│   ├── prescreening/                  # Stage 2 scripts
│   │   ├── stage2_prescreening_revised_auto.py
│   │   ├── prescreening_utils.py
│   │   └── prescreening_data/         # Prescreen output data
│   │       ├── processing_index_*.json
│   │       └── prescreen_run_results/
│   ├── analysis/                      # Data analysis scripts
│   └── audit_reports/                 # Historical audits
├── Documentation/
│   ├── README.md                      # This file
│   ├── problematic_ics/               # Failed ICs
│   │   ├── hierarchical/
│   │   ├── hierarchical_for_gold_standard/
│   │   └── standard/
│   ├── problematic_ics_blacklist.json # Failed ID list
│   └── standard_quasi_random_ids_not_in_gold.md  # 184 IDs with no gold counterpart
```

---

## Dataset Variants and Inventory

### Primary Dataset Folders

| Folder | Type | File Count | ID Range | Gaps | Disk Usage |
|--------|------|------------|----------|------|------------|
| `simulation_data/Data/ic_final/ic_hierarchical/` | IC | 4,857 | 0000-4999 | 143 gaps | ~19 MB |
| `simulation_data/Data/ic_final/ic_standard_quasi_random/` | IC | 2,749 | 0000-3998 | 1,250 gaps | ~11 MB |
| `simulation_data/Data/brutus_output/brutus_hierarchical/` | Trajectory | 4,857 | 0000-4999 | 143 gaps | ~531 MB |
| `simulation_data/Data/brutus_output/brutus_hierarchical_gold_standard/` | Trajectory | 4,857 | 0000-4999 | 143 gaps | ~2.4 GB |
| `simulation_data/Data/brutus_output/brutus_standard_quasi_random/` | Trajectory | 2,749 | 0000-3998 | 1,250 gaps | ~122 MB |
| `simulation_data/Data/brutus_output/brutus_standard_quasi_random_gold_standard/` | Trajectory | 2,565 | 0000-3998 | 1,434 gaps | ~1.7 GB |

**Note:** Gold-standard Brutus output folders (`brutus_hierarchical_gold_standard/`, `brutus_standard_quasi_random_gold_standard/`) still exist. Only the gold IC input folders (`ic_hierarchical_for_gold_standard/`, `ic_standard_quasi_random_for_gold_standard/`) were duplicates and have been removed. Gold runs now read from the base IC folders.

### Dataset Relationships

```
$IC_RAW_DIR                   [Stage 1 output - raw generated ICs, externalized]
    |
    v
Validation/prescreening/  -->  Data/ic_final/       [Stage 2 - prescreened ICs]
    |                               |
    |                               v
    |                   Scripts/brutus_runners/  -->  Data/brutus_output/   [Stage 3]
    |                                       |
    |                                       v
    +------------------------------>  Data/metrics/     [Stage 4 - metrics]
```

**IC-to-Brutus Mapping:**
- Each IC file has a corresponding Brutus output file with the same numeric ID
- Non-gold: `ic_hierarchical_XXXX.txt` ↔ `brutus_hierarchical_XXXX.txt`
- Non-gold: `ic_standard_XXXX.txt` ↔ `brutus_standard_XXXX.txt`
- Gold hierarchical (in `brutus_hierarchical_gold_standard/`): `ic_hierarchical_XXXX.txt` ↔ `brutus_hierarchical_XXXX.txt`
- Gold standard (in `brutus_standard_quasi_random_gold_standard/`): `ic_standard_XXXX.txt` ↔ `brutus_standard_XXXX.txt`

**Gold Standard Subsets:**
- `*_gold_standard` Brutus output folders contain higher-resolution outputs (dt_out=0.01)
- For hierarchical ICs: gold standard is a complete copy (same 4,857 files)
- For standard quasi-random: gold standard excludes 184 IDs (2,749 base → 2,565 gold)
- The `*_for_gold_standard` IC folders were duplicates of the base IC folders and have been removed; gold runs now read from `ic_hierarchical/` and `ic_standard_quasi_random/`

**ID Gaps:**
- Gaps exist due to:
  1. Continuation of generation runs (non-contiguous ID allocation)
  2. Stage 2 prescreen rejection
  3. Problematic IC moves (failed during Brutus execution)

---

## File Naming Conventions and Mapping

### IC Files

Non-gold folders use:
```
ic_hierarchical_XXXX.txt
ic_standard_XXXX.txt
```

**Historical note (2026-06-10):** the gold-standard IC folders were documented as using a `_gold_` infix (`ic_hierarchical_gold_XXXX.txt`, `ic_standard_gold_XXXX.txt`). Those folders have since been removed, so this naming is no longer verifiable on disk; no current IC file uses a `_gold_` infix.

Where `XXXX` is a 4-digit zero-padded integer (e.g., `0000`, `0427`, `3998`).

### Brutus Output Files

All four folders use the **base filename prefixes**; gold-standard folders do **not** add a `_gold_` infix (verified against the on-disk tree 2026-06-10):

```
simulation_data/Data/brutus_output/brutus_hierarchical/brutus_hierarchical_XXXX.txt
simulation_data/Data/brutus_output/brutus_hierarchical_gold_standard/brutus_hierarchical_XXXX.txt
simulation_data/Data/brutus_output/brutus_standard_quasi_random/brutus_standard_XXXX.txt
simulation_data/Data/brutus_output/brutus_standard_quasi_random_gold_standard/brutus_standard_XXXX.txt
```

Gold-standard status is encoded **only** in the folder name; filenames do not encode it. When parsing, the folder is the authoritative (and only) variant identifier.

**Note:** The mapping between IC and Brutus files is always by numeric ID, within the corresponding folder pair:
- `ic_hierarchical_0427.txt` → `brutus_hierarchical_0427.txt` (same filename in the base and gold-standard Brutus folders)
- `ic_standard_0427.txt` → `brutus_standard_0427.txt` (same filename in the base and gold-standard Brutus folders)

---

## File Schemas

### Initial Condition File Format (`ic_*.txt`)

**Structure:** 3 lines, one per body

```
mass1 x1 y1 z1 vx1 vy1 vz1
mass2 x2 y2 z2 vx2 vy2 vz2
mass3 x3 y3 z3 vx3 vy3 vz3
```

**Fields:**
- `mass` - body mass (float64). Standard ICs use exactly `1.0` for all bodies; hierarchical ICs vary but are normalized so total mass ≈ 3.
- `x, y, z` - position components (float64)
- `vx, vy, vz` - velocity components (float64)

**Units:** All quantities are in natural units (G = 1, total mass ≈ 3)

**Example:**
```
1.3490330328149076 -0.9689510833073296 0.007710980988132066 -0.015155493143494857 0.003082579960339502 -0.9723812422861391 0.01317780514703599
0.3068019185652623 -0.6619848581497906 -0.005365500630046534 0.0070754473066994734 0.002840479118371817 1.3293141254107488 -0.013692746386640507
1.3441650486198304 1.1354206743022845 -0.0016313630906544987 0.002882937931195984 0.00441920746565285 0.6549777259648452 0.001846566609351255
```

### Brutus Output File Format (`brutus_*.txt`)

**Structure:** Repeating snapshots

```
t N t_cpu
m1 x1 y1 z1 vx1 vy1 vz1
m2 x2 y2 z2 vx2 vy2 vz2
m3 x3 y3 z3 vx3 vy3 vz3

t N t_cpu
m1 x1 y1 z1 vx1 vy1 vz1
m2 x2 y2 z2 vx2 vy2 vz2
m3 x3 y3 z3 vx3 vy3 vz3
...
Result: filename=... N=... t_begin=... t_end=... dt=... [eta=...] [tol=...] Lw=... t_cpu=... E_initial=... E_final=... dE/E=...
```

**Snapshot Header Line:**
- `t` - simulation time (float)
- `N` - number of bodies (always 3)
- `t_cpu` - accumulated CPU time for this snapshot (float)

**Body Data Lines:**
- High-precision arbitrary-precision floats (typically 30-40 significant digits)
- Same format as IC files: `m x y z vx vy vz`

**Snapshot Separator:** Blank line between snapshots

**Result Footer:**

All current Brutus output files contain a `Result:` footer line, but the **schema varies** across files. Three schemas are observed:

Full schema (with `eta` and `tol`):
```
Result: filename= /absolute/path/to/ic_XXXX.txt N= 3 t_begin= 0 t_end= 10 dt= 0.08 eta= 0.263027 tol= 1e-15 Lw= 130 t_cpu= 11.2667 E_initial= -1.23733 E_final= -1.23733 dE/E= 1.49235e-14
```

Partial schema (with `tol` but no `eta`):
```
Result: filename= /absolute/path/to/ic_XXXX.txt N= 3 t_begin= 0.0 t_end= 10.000000000000007 dt= 0.08 tol= 1e-15 Lw= 130 t_cpu= 8.5887 E_initial= -3.11082 E_final= -3.11082 dE/E= 1.97004e-14
```

Minimal schema (no `eta` or `tol`):
```
Result: filename= /absolute/path/to/ic_XXXX.txt N= 3 t_begin= 0.0 t_end= 10.009999999999831 dt= 0.01 Lw= 130 t_cpu= 431.969 E_initial= -2.10843 E_final= -2.10843 dE/E= 1.44300e-12
```

**Critical Note:** The `Result:` footer schema is **heterogeneous**. See [Known Anomalies](#known-anomalies-and-gotchas) for per-folder breakdown. Parsers must treat `eta` and `tol` as optional fields.

---

## Physical Conventions and Units

### Units and Constants

| Quantity | Value | Notes |
|----------|-------|-------|
| G (gravitational constant) | 1.0 | Natural units |
| Total mass | ~3.0 | Normalized across ICs |
| Time range | 0 to 10 | Integration interval |

### Mass Normalization

All systems have total mass M ≈ 3:
- **Standard quasi-random:** masses are exactly `1.0, 1.0, 1.0` (so total mass is exactly `3.0`).
- **Hierarchical:** masses vary (observed sample: min ≈ 0.105, median ≈ 0.897, max ≈ 2.377) but are normalized so total mass ≈ 3.

### Center of Mass and Momentum

**Standard Quasi-Random ICs:**
- Exact COM = 0 by construction
- Exact total momentum = 0 by construction

**Hierarchical ICs:**
- Small Gaussian perturbations (σ=0.01) applied to both positions and velocities after COM/P=0 enforcement
- Observed offsets are **not** tiny: in a 500-file sample, `|COM|` median ≈ 9e-3 (95th ≈ 1.8e-2) and `|P|` median ≈ 3e-2 (95th ≈ 5.5e-2)
- **Downstream consumers may want to recenter/reboost to COM frame**

### Dimensionality (Not Planar)

This dataset is **3D**:
- Standard quasi-random ICs can have large `|z|` (sample p95 ≈ 0.81, max ≈ 1.06).
- Hierarchical ICs tend to be near-planar because `inc_inner` is small and `z` is mostly introduced by small inclination + perturbations (sample p95 ≈ 0.023).

### Hierarchical System Characteristics

Hierarchical systems are configured with:
- Inner binary separation: a ~ 0.1-0.3
- Outer third body: 3-10× inner binary separation
- COM and total momentum are enforced to be ~0, **then** small Gaussian perturbations (σ=0.01) are applied to all positions/velocities (so COM/P are not exactly 0 in final files)

This configuration promotes stability and well-defined orbital motion.

### Standard Quasi-Random (Sobol) System Characteristics

Standard quasi-random IC generation in `simulation_data/Scripts/ic_generation/ic_generation_utils.py` uses a symmetry-reduced canonicalization:
- Particle 1 is fixed at `p1 = (1, 0, 0)` (then optionally globally scaled).
- Particle 2 is sampled by a Sobol sequence mapped to a uniform direction on the sphere and a radius `r = u^(1/3)`.
- A mirror constraint enforces `x ≤ 0` for the sampled direction (by shifting `phi` by π when needed).
- Particle 3 is set to `p3 = -(p1 + p2)` to enforce COM = 0 for equal masses.

Velocities for standard ICs:
- Particle 2 velocity components are sampled from `Normal(0, velocity_scale)` via inverse-CDF on Sobol draws.
- For equal masses, total momentum is enforced by setting `v1 = v3 = -v2/2`.

Global scaling:
- In the standard generator, `scale_range=(0.8, 1.2)` is enabled (see `simulation_data/Scripts/ic_generation/generate_ics.py`), and the implementation scales **both positions and velocities** by the same factor `s`.
- This changes the virial ratio by approximately `Q ∝ s^3` (because `T ∝ s^2` and `|U| ∝ 1/s`).

### Virial Ratio

- Virial ratio used in Stage 2 prescreening is `Q = 2T/|U|` (as implemented in `stage2_prescreening_revised_auto.py`)
- Stable systems typically have Q ≈ 1
- Fixed fallback range: Q ∈ [0.001, 2.0] (but actual cutoffs are data-derived when adaptive percentile thresholds are enabled, which is the default)

---

## Pipeline and Provenance

### Stage 1: IC Generation

**Script:** `ic_generation_utils.py`

**Method:** Sobol-based quasi-random sampling with scrambling

**Parameters:**
- `epsilon` (minimum separation): 0.05
- `velocity_scale` (velocity std): 0.1
- Sobol dimension: 7 (3 position + 3 velocity + 1 scaling)
- Scramble: enabled
- Standard generator scaling (enabled in `generate_ics.py`): `scale_range=(0.8, 1.2)`

**Specialized Generation for Hierarchical Systems:**
- Enforces hierarchical mass/separation structure
- Inner binary + outer third body configuration
- Enforces COM/P≈0 via a COM shift and velocity boost, then applies a small Gaussian perturbation (σ=0.01) to all positions/velocities

**Output:** Raw IC storage has been externalized from the repository. Set the `IC_RAW_DIR` environment variable before running Stage 1 or Stage 2 scripts:

```bash
export IC_RAW_DIR=/path/to/ic_raw  # Expected subdirs: ic_hierarchical/, ic_standard_quasi_random/
```

The directory pointed to by `IC_RAW_DIR` must contain:
- `ic_hierarchical/` - Raw hierarchical IC files
- `ic_standard_quasi_random/` - Raw standard quasi-random IC files

**Why externalized:** Raw IC files are large (multi-GB) and user-managed. Externalizing allows users to store raw ICs separately from the tracked repository while maintaining the same script interfaces.

**Error handling:** Stage 1/2 scripts raise a clear `RuntimeError` if `IC_RAW_DIR` is not set, including the expected export command and directory structure.

After prescreening, valid ICs are copied to `simulation_data/Data/ic_final/` which remains in the repository.

### Stage 2: Prescreening

**Script:** `Validation/prescreening/stage2_prescreening_revised_auto.py`

**Purpose:** Filter out unstable or pathological configurations before expensive Brutus integration

**Parameters:**
```python
TMAX = 1.0                    # Integration time for prescreen
DT = 0.0001                   # Leapfrog timestep
G = 1.0                       # Gravitational constant
ENERGY_ERROR_THRESHOLD = 0.01 # 1% relative energy error
MIN_DISTANCE_THRESHOLD = 0.01 # Minimum separation
```

**Static Check Thresholds:**
```python
VIRIAL_RATIO_MIN = 0.001      # Accept cold systems
VIRIAL_RATIO_MAX = 2.0        # Upper bound
MIN_ANGULAR_MOMENTUM = 0.0    # No minimum
```

**Adaptive Percentile Thresholds (enabled by default; `USE_PERCENTILE_THRESHOLDS = True`):**
```python
VIRIAL_PERCENTILE_MIN = 1     # Keep top 99%
VIRIAL_PERCENTILE_MAX = 99.5  # Remove top 0.5% outliers
```

When adaptive thresholds are enabled, the fixed virial range above serves only as a fallback. The actual virial cutoffs are computed per-batch from the data-derived percentiles.

**Logic:** Uses JIT-compiled leapfrog integrator to reject ICs that:
- Have energy error > 1%
- Experience collisions (min separation < 0.01)
- Have extreme virial ratios

**Provenance Tracking:**
- `simulation_data/Validation/prescreening/prescreening_data/processing_index_ic_hierarchical.json` - hierarchical pass/fail records (cumulative: 5,000 entries, 4,860 passed, 140 failed)
- `simulation_data/Validation/prescreening/prescreening_data/processing_index_ic_standard_quasi_random.json` - standard pass/fail records (cumulative: 4,000 entries, 3,007 passed, 993 failed)
- `simulation_data/Validation/prescreening/prescreening_data/prescreen_run_results/` - per-run summary JSON outputs (15 files; 10 older schema with `run_info`/`detailed_results`, 5 newer schema with `run_id`/`datasets`)

**Note:** The processing indices are **cumulative history** across all prescreen runs, not exact manifests of the current `final_stage_ic_datasets/` folders. The on-disk IC counts may differ from the index "passed" counts because the final-stage folders also include ICs that were promoted before the index existed or that were manually added.

**Processing Index Format:**
```json
{
  "processed_files": {
    "ic_hierarchical_0248.txt": {
      "hash": "0e16b5e265fdc8926046d71f62b0ba07551611282c790763b7b95d7f0f887b03",
      "passed": true,
      "last_processed": "2025-06-18T10:06:30.776840",
      "results": {
        "filename": "ic_hierarchical_0248.txt",
        "passed": true,
        "stage": "dynamic_check",
        "reason": "passed",
        "max_energy_error": 4.21e-07,
        "min_separation": 0.166,
        "integration_time": 1.0,
        "virial_ratio": 0.952,
        "angular_momentum": 1.12,
        "kinetic_energy": 3.655,
        "potential_energy": -7.679
      }
    }
  }
}
```

**Output:** `simulation_data/Data/ic_final/` (passed ICs only)

### Stage 3: Brutus Integration

**Purpose:** Run high-precision N-body simulations using the Brutus integrator.

**Algorithm:** Brutus uses the **Bulirsch-Stoer extrapolation method** with:
- **Base integrator:** Leapfrog (velocity Verlet) scheme
- **Extrapolation sequence:** n = 1, 2, 4, 6, 8, ..., 56 substeps
- **Precision:** GNU MPFR via `mpreal` wrapper; user-specified word length (MPFR digits ≈ Lw/log₂(10))
- **Adaptive stepping:** `dt = eta * (r/a)^0.25` where eta is tolerance-derived step-size controller

**Key Scripts:**
- `Scripts/brutus_runners/run_brutus_both_type_simple.py` - Main batch runner
- `Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py` - Gold standard hierarchical

**CLI Contract:**
```bash
./brutus <tolerance> <word_length> <t_begin> <t_end> <dt_out> <n_particles> <input_file>
```

Example:
```bash
./brutus 1e-15 130 0 10 0.08 3 /path/to/ic_hierarchical_0000.txt
```

| Argument | Description |
|----------|-------------|
| tolerance | Convergence tolerance (e.g., 1e-15) |
| word_length | MPFR precision in bits (recommended: 100-200) |
| t_begin | Start time (typically 0) |
| t_end | End time (typically 10) |
| dt_out | **Output sampling interval** (NOT internal step size) |
| n_particles | Number of bodies (3) |
| input_file | Path to IC file |

**Note:** `dt_out` is the output sampling interval, not the internal adaptive step size. The integrator uses adaptive stepping internally based on tolerance.

**Parameters (defaults from runner scripts):**
| Variant | Tolerance | Word Length | dt_out | Notes |
|---------|-----------|-------------|--------|-------|
| Hierarchical | 1e-15 | 130 | 0.08 | Default parameters |
| Standard | 1e-13 | 118 | 0.17 | Default parameters |
| Hierarchical Gold | 1e-13 | 130 | 0.01 | Higher resolution |
| Standard Gold | 1e-13 | 130 | 0.01 | Higher resolution |

**⚠️ Parameter Heterogeneity Caveat:** The values above are defaults from runner scripts. Actual output files within each folder show heterogeneity (multiple `tol`/`Lw` values) due to reruns, script evolution, and manual interventions. See [Brutus Parameters by Variant](#brutus-parameters-by-variant) for detailed per-folder parameter breakdowns.

**Integration Contract:**
- **Timeout:** 3000 seconds (50 minutes) per simulation
- **Parallel execution:** `ProcessPoolExecutor` with `max(1, cpu_count - 1)` workers
- **Failure handling:**
  - Validates final timestep ≥ 9.5
  - Moves failed IC to `Documentation/problematic_ics/{variant}/`
  - Deletes partial output file

**Input:** `Data/ic_final/`

**Output:** `Data/brutus_output/`
- `brutus_hierarchical/`
- `brutus_hierarchical_gold_standard/`
- `brutus_standard_quasi_random/`
- `brutus_standard_quasi_random_gold_standard/`

**Scripts:**
- `run_brutus_both_type_simple.py` - Main runner for hierarchical and standard (but see note below)
- `run_brutus_hierarchical_only_mac_gold_standard.py` - Gold standard hierarchical runner

**Current runner defaults:**
- `run_brutus_both_type_simple.py` currently has `STANDARD_ICS_PER_RUN = 0`, so by default it only processes hierarchical ICs. To process standard quasi-random ICs, increase this constant before running.
- `run_brutus_hierarchical_only_mac_gold_standard.py` processes up to `ICS_PER_RUN = 1000` hierarchical gold ICs per invocation.

**Standard Gold provenance note:** There is no runner script in this repo that explicitly targets `brutus_output/brutus_standard_quasi_random_gold_standard/`. For this folder, treat the `Result:` footers as the most direct evidence of parameters and input paths, and document provenance as "partially unknown / external machine" unless you locate the missing runner history elsewhere.

**Integration Method:** Bulirsch-Stoer with variable timestep and arbitrary precision (GMP/MPFR)

**Parameters:** See [Brutus Parameters by Variant](#brutus-parameters-by-variant)

**Validation:**
- Final timestep must reach ≥ 9.5
- Failed ICs moved to `problematic_ics/` directories

**Output:** `simulation_data/Data/brutus_output/`

### Stage 4: Metrics Calculation

**Purpose:** Calculate conservation metrics and quality indicators.

**Key Script:** `Scripts/metrics_calculation/calculate_metrics.py`

**Metrics Calculated:**
- Energy conservation (relative drift)
- Linear momentum conservation
- Angular momentum conservation
- Escape detection (max separation > 100)
- Collision detection (min separation < 0.01)

**Input:** `Data/brutus_output/`

**Output:** `Data/metrics/sim_result_metric_*/`
- JSON files with metrics for each simulation ID

---

## Brutus Parameters by Variant

Important distinction:
- `dt_out` in Brutus outputs is the **output sampling interval**, not the internal Bulirsch–Stoer step size (which is adaptive and not directly stored in these text files).

### Observed Parameter Sets (from `Result:` footers)

Most Brutus output files end with a `Result:` footer; a subset has no footer at all (counts below; verified 2026-06-10, matching the missing-footer counts in `Validation/audit_reports/footer_audit_20251224_170141.md`, except `brutus_hierarchical`, re-verified 2026-06-11 after the DATA-05 remediation rerun of 70 files — see note under that folder). Footers that are present carry the full schema, including `eta` and `tol`. Files without a footer cannot be assigned a parameter set from the file alone; for those, assume the folder-level defaults.

Each entry below is `(tol, Lw, dt_out, t_end, eta) → count`. Files with no footer are listed separately.

#### `simulation_data/Data/brutus_output/brutus_hierarchical/` (4,857 files; 3,377 with footer, 1,480 without)

Footers (full schema, with `eta`):
- `(1e-15, 130, 0.08, 10, 0.263027) → 3,377`

No `Result:` footer:
- `→ 1,480` (no parameters recorded in-file; assume folder defaults: tol=1e-15, Lw=130, dt_out=0.08)

> Counts updated 2026-06-11 (previously 3,307 / 1,550): the GAP-24-01 DATA-05 remediation
> rerun replaced 70 stale base-hierarchical files (IDs `0005`-`0059`, `0061`-`0075`); all
> 70 old files were footer-less, all 70 replacements carry full-schema footers with the
> same parameter tuple. This folder now intentionally differs from
> `footer_audit_20251224_170141.md` by −70 missing footers. Evidence:
> `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-DATA05-RERUN-REMEDIATION.md`.

#### `simulation_data/Data/brutus_output/brutus_hierarchical_gold_standard/` (4,857 files; all full-schema)

- `(1e-13, 130, 0.01, 10.01, 0.277971) → 4,146`
- `(1e-13, 124, 0.01, 10.01, 0.277971) → 649`
- `(1e-14, 118, 0.01, 10.01, 0.270396) → 34`
- `(1e-14, 112, 0.01, 10.01, 0.270396) → 27`
- `(1e-14, 124, 0.01, 10.01, 0.270396) → 1`

#### `simulation_data/Data/brutus_output/brutus_standard_quasi_random/` (2,749 files; 2,048 with footer, 701 without)

Footers (full schema, with `eta`):
- `(1e-13, 118, 0.17, 10.03, 0.277971) → 1,126`
- `(1e-13, 130, 0.17, 10.03, 0.277971) → 922`

No `Result:` footer:
- `→ 701` (no parameters recorded in-file; assume folder defaults: tol=1e-13, Lw=118, dt_out=0.17)

#### `simulation_data/Data/brutus_output/brutus_standard_quasi_random_gold_standard/` (2,565 files; 2,346 with footer, 219 without)

Footers (full schema, with `eta` and `tol`):
- `(1e-13, 130, 0.01, 10.01, 0.277971) → 1,754`
- `(1e-14, 130, 0.01, 10.01, 0.270396) → 592`

No `Result:` footer:
- `→ 219` (no parameters recorded in-file; assume folder defaults: tol=1e-13, Lw=130, dt_out=0.01)

### Snapshot Count Note

Avoid hard-coding exact expected snapshot counts:
- `t_end` can be slightly larger than 10 (e.g., 10.01 or 10.03) when `dt_out` does not evenly divide the nominal stop time.
- Some runs may have been re-executed with different parameters, especially in gold folders.

---

## Quality Control and Validation

### Completeness Checks

**Primary Check:** Final timestep ≥ 9.5

```python
# Validation pattern used in run scripts
timestep_pattern = re.compile(r'^(\d+\.?\d*)\s+3\s+\d+')
final_timestep = max([float(t) for t in timesteps])
if final_timestep < 9.5:
    # Mark as incomplete
```

**Do NOT rely on:**
- Parsing a specific `Result:` footer schema (the footer is present in all files but its fields vary; see [Known Anomalies](#known-anomalies-and-gotchas))
- Line count thresholds (variable due to integration dynamics)

### Conservation Metrics

**Energy Conservation:**
- Expected: dE/E < 10⁻¹² for high-precision runs
- Actual: varies by tolerance setting (check `Result:` footer when present)

**Momentum Conservation:**
- Exact for standard quasi-random (by construction)
- Approximate for hierarchical (small perturbations applied)

### Metrics Location

**Energy, momentum, angular momentum drift:** `Data/metrics/sim_result_metric_*/` directories (four subdirectories, one per variant)

**Collision Detection:**
- Minimum separation threshold: 0.01
- Flagged in metrics when violated

**Escape Detection:**
- Maximum separation threshold: 100
- Flagged in metrics when violated

**Important:** `calculate_metrics.py` does **not** enforce completeness; it generates a metrics JSON for every Brutus output file, including partial or errored runs. Consumers must apply their own final-timestep check before trusting a metric file.

---

## Known Anomalies and Gotchas

### 1. Missing `Result:` Footers

Most Brutus output files end with a `Result:` footer line, but a subset has none at all (verified 2026-06-10; matches the missing-footer counts in `Validation/audit_reports/footer_audit_20251224_170141.md`, except `brutus_hierarchical`, re-verified 2026-06-11 after the DATA-05 remediation rerun — see Section "Observed Parameter Sets"). Footers that are present carry the full field set, including `eta` and `tol`:

| Folder | Total Files | With Footer (full schema) | No Footer |
|--------|-------------|---------------------------|-----------|
| brutus_hierarchical | 4,857 | 3,377 | 1,480 |
| brutus_hierarchical_gold_standard | 4,857 | 4,857 | 0 |
| brutus_standard_quasi_random | 2,749 | 2,048 | 701 |
| brutus_standard_quasi_random_gold_standard | 2,565 | 2,346 | 219 |

**Implications:**
- A `Result:` footer may be absent; do not treat its absence as a failure mode
- Parsers must treat the entire footer as optional
- For files with no footer, assume the folder-level defaults
- Use timestep coverage (final timestep ≥ 9.5) as primary completeness check, not footer presence

### 2. `Result: filename=` Path and IC-Folder Ambiguity

All current `Result: filename=` paths use macOS-style absolute paths (`<home>/Desktop/3_body_problem/...`).

**Implication:** Treat `Result: filename=` as an informational hint only, not an authoritative IC-to-output mapping.

**IC-folder references inside `Result: filename=`:**

Gold-standard output folders reference **both** the gold and non-gold IC directories in their footers, because some runs were executed against one IC copy and some against the other:
- `brutus_hierarchical_gold_standard/`: `ic_hierarchical_for_gold_standard` 3,440, `ic_hierarchical` 1,417
- `brutus_standard_quasi_random_gold_standard/`: `ic_standard_quasi_random` 2,086, `ic_standard_quasi_random_for_gold_standard` 479

Non-gold output folders consistently reference their matching IC folder:
- `brutus_hierarchical/`: `ic_hierarchical` 4,857
- `brutus_standard_quasi_random/`: `ic_standard_quasi_random` 2,749

Do not use `Result: filename=` as a unique source of truth for which IC folder was used.

### 3. Hierarchical ICs Have Non-Zero COM/Momentum

The hierarchical generator applies Gaussian perturbations (σ=0.01) to both positions and velocities **after** COM=0 and P=0 enforcement. This reintroduces small offsets.

**Impact:**
- Offsets are typically ~1e-2 to 1e-1 in these units (sample-based): `|COM|` median ≈ 9e-3 (95th ≈ 1.8e-2) and `|P|` median ≈ 3e-2 (95th ≈ 5.5e-2)
- Downstream consumers should recenter/reboost if exact COM frame is required

### 4. Parameter Heterogeneity Within Folders

Parsing `Result:` lines shows multiple parameter sets within the same folder. This occurs due to:
- Reruns with different tolerances
- Script parameter evolution over time
- Manual intervention for edge cases

**Where heterogeneity is actually observed (from `Result:` footers):**
- `brutus_hierarchical_gold_standard/`: multiple `tol` and `Lw` values
- `brutus_standard_quasi_random/`: both `Lw=118` and `Lw=130`
- `brutus_standard_quasi_random_gold_standard/`: both `tol=1e-13` and `tol=1e-14`

### 5. Gold Standard Subset is Not Simply a Filter

**For hierarchical ICs:** Gold standard = complete copy (same 4,857 files). The `ic_hierarchical_for_gold_standard/` folder was a duplicate of `ic_hierarchical/` and has been removed.

**For standard quasi-random:** Gold standard excludes 184 IDs (2,749 base → 2,565 gold). The `ic_standard_quasi_random_for_gold_standard/` folder contained only the subset and has been removed. Gold runs now read from the base `ic_standard_quasi_random/` folder.

**184-ID exclusion list:** The complete list of standard quasi-random IDs that have no gold-standard counterpart is documented at `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md`. This file is used by `correspondence.py` to skip validation for these IDs when checking standard gold outputs.

**Note:** Gold-standard Brutus outputs (`brutus_hierarchical_gold_standard/`, `brutus_standard_quasi_random_gold_standard/`) still exist with higher temporal resolution (dt_out=0.01). Only the gold IC input folders were duplicates and have been removed.

### 6. ID Gaps Have Multiple Causes

Gaps in the ID sequence (e.g., hierarchical: 0000-4999 has 143 gaps; standard: 0000-3998 has 1,250 gaps) are due to:
1. Generation continuation (non-contiguous Sobol sequence allocation)
2. Stage 2 prescreen rejection
3. Moves to `problematic_ics/` during Brutus execution

**Gaps are intentional** and reflect the filtering process.

### 7. No Runner for Standard Quasi-Random Gold Standard

There is no in-repo runner script that reproduces `brutus_standard_quasi_random_gold_standard/` outputs. Gold Brutus outputs exist, but provenance is partially unknown unless recovered from external logs.

### 8. Naming Inconsistencies

Some legacy scripts use hardcoded variant names that differ from actual folder schemas. Consumers should rely on the folder structure documented above rather than script-internal naming.

---

## Minimal Parsing Examples

### Reading an IC File

```python
import numpy as np

def read_ic_file(filepath):
    """
    Read a 3-body initial condition file.

    Returns:
        masses: (3,) array
        positions: (3, 3) array
        velocities: (3, 3) array
    """
    data = np.loadtxt(filepath, dtype=np.float64)
    masses = data[:, 0]
    positions = data[:, 1:4]
    velocities = data[:, 4:7]
    return masses, positions, velocities

# Example usage
masses, pos, vel = read_ic_file('simulation_data/Data/ic_final/ic_hierarchical/ic_hierarchical_0000.txt')
```

### Reading a Brutus Output File (Robust)

```python
import re
import numpy as np

def read_brutus_output(filepath):
    """
    Read a Brutus trajectory file, handling heterogeneous Result: footer schemas.

    Returns:
        times: list of float timestamps
        trajectories: list of (3, 7) arrays [mass, x, y, z, vx, vy, vz]
        metadata: dict with Result: fields (fields vary by footer schema)
    """
    times = []
    trajectories = []
    metadata = None

    # Pattern for timestep headers: "t N t_cpu"
    timestep_pattern = re.compile(r'^(\d+\.?\d*)\s+3\s+\d+')
    # Pattern for Result footer
    result_pattern = re.compile(r'^Result:\s+filename=')

    current_snapshot = []

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()

            # Check for Result: footer
            if result_pattern.match(line):
                metadata = parse_result_footer(line)
                continue

            # Check for timestep header
            match = timestep_pattern.match(line)
            if match:
                # Save previous snapshot if exists
                if current_snapshot:
                    trajectories.append(np.array(current_snapshot))
                    current_snapshot = []

                times.append(float(match.group(1)))
                continue

            # Skip empty lines
            if not line:
                continue

            # Parse body data line
            # NOTE: converting to float will lose arbitrary-precision detail from Brutus.
            # If you need exact precision, parse with `decimal.Decimal` or keep strings.
            body_data = np.array([float(x) for x in line.split()])
            if len(body_data) == 7:
                current_snapshot.append(body_data)

    # Don't forget the last snapshot
    if current_snapshot:
        trajectories.append(np.array(current_snapshot))

    return times, trajectories, metadata

def parse_result_footer(line):
    """Parse a Result: footer line into a dictionary.

    Handles three observed footer schemas:
      - Full:    filename, N, t_begin, t_end, dt, eta, tol, Lw, t_cpu, E_initial, E_final, dE/E
      - Partial: filename, N, t_begin, t_end, dt, tol, Lw, t_cpu, E_initial, E_final, dE/E (no eta)
      - Minimal: filename, N, t_begin, t_end, dt, Lw, t_cpu, E_initial, E_final, dE/E (no eta/tol)
    """
    import re

    md = {}

    # Extract filename (terminated by " N=")
    m_file = re.search(r"^Result:\s+filename=\s+(?P<filename>.+?)\s+N=\s+(?P<N>\d+)", line)
    if not m_file:
        return {"raw": line}
    md.update(m_file.groupdict())

    # Extract each known field individually (all are optional)
    for field, pattern in [
        ("t_begin", r"t_begin=\s+(?P<t_begin>[-+\deE\.]+)"),
        ("t_end",   r"t_end=\s+(?P<t_end>[-+\deE\.]+)"),
        ("dt",      r"dt=\s+(?P<dt>[-+\deE\.]+)"),
        ("eta",     r"eta=\s+(?P<eta>[-+\deE\.]+)"),
        ("tol",     r"tol=\s+(?P<tol>[-+\deE\.]+)"),
        ("Lw",      r"Lw=\s+(?P<Lw>\d+)"),
        ("t_cpu",   r"t_cpu=\s+(?P<t_cpu>[-+\deE\.]+)"),
        ("E_initial", r"E_initial=\s+(?P<E_initial>[-+\deE\.]+)"),
        ("E_final",   r"E_final=\s+(?P<E_final>[-+\deE\.]+)"),
        ("dE_over_E", r"dE/E=\s+(?P<dE_over_E>[-+\deE\.]+)"),
    ]:
        m = re.search(pattern, line)
        if m:
            md.update(m.groupdict())

    return md

# Example usage
times, trajectories, metadata = read_brutus_output(
    'simulation_data/Data/brutus_output/brutus_hierarchical/brutus_hierarchical_0000.txt'
)
print(f"Read {len(times)} snapshots from t={times[0]:.3f} to t={times[-1]:.3f}")
if metadata:
    print(f"Metadata: {metadata}")
```

### Validating Brutus Output Completeness

```python
import re

def validate_brutus_output(filepath, time_threshold=9.5):
    """
    Validate Brutus output by checking final timestep.

    Returns:
        (is_valid, message)
    """
    timestep_pattern = re.compile(r'^(\d+\.?\d*)\s+3\s+\d+')

    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()

        timestep_values = []
        for line in lines:
            match = timestep_pattern.match(line.strip())
            if match:
                timestep_values.append(float(match.group(1)))

        if not timestep_values:
            return False, "No timestep lines found"

        final_timestep = timestep_values[-1]

        if final_timestep < time_threshold:
            return False, f"Incomplete (final t={final_timestep:.3f} < {time_threshold})"

        return True, f"Valid (final t={final_timestep:.3f})"

    except Exception as e:
        return False, f"Error: {e}"

# Example usage
is_valid, msg = validate_brutus_output(
    'simulation_data/Data/brutus_output/brutus_hierarchical/brutus_hierarchical_0000.txt'
)
print(f"Validation: {msg}")
```

### Computing Center of Mass

```python
import numpy as np

def compute_com(masses, positions):
    """
    Compute center of mass for a system.

    Args:
        masses: (N,) array
        positions: (N, 3) array

    Returns:
        com: (3,) array
    """
    total_mass = np.sum(masses)
    com = np.sum(masses[:, np.newaxis] * positions, axis=0) / total_mass
    return com

def recenter_to_com_frame(masses, positions, velocities):
    """
    Recenter system to COM frame (for hierarchical ICs).
    """
    com = compute_com(masses, positions)
    total_mass = np.sum(masses)
    com_velocity = np.sum(masses[:, np.newaxis] * velocities, axis=0) / total_mass

    positions_centered = positions - com
    velocities_centered = velocities - com_velocity

    return positions_centered, velocities_centered

# Example usage
masses, pos, vel = read_ic_file('simulation_data/Data/ic_final/ic_hierarchical/ic_hierarchical_0000.txt')
com = compute_com(masses, pos)
print(f"COM offset magnitude: {np.linalg.norm(com):.6e}")
pos_centered, vel_centered = recenter_to_com_frame(masses, pos, vel)
```

---

## References

### Code Locations

| Component | Location |
|-----------|----------|
| IC Generator (core) | `simulation_data/Scripts/ic_generation/ic_generation_utils.py` |
| IC Generator (entrypoint) | `simulation_data/Scripts/ic_generation/generate_ics.py` |
| Stage 2 Prescreening | `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py` |
| Brutus Runner (Main) | `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py` |
| Brutus Runner (Gold) | `simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py` |
| Metrics Calculator | `simulation_data/Scripts/metrics_calculation/calculate_metrics.py` |
| Brutus Simulator | `brutus_Newton-main/` (C++ with GMP/MPFR) |

### Provenance Files

| File | Content |
|------|---------|
| `simulation_data/Validation/prescreening/prescreening_data/processing_index_ic_hierarchical.json` | Hierarchical prescreen pass/fail records (cumulative history) |
| `simulation_data/Validation/prescreening/prescreening_data/processing_index_ic_standard_quasi_random.json` | Standard prescreen pass/fail records (cumulative history) |
| `simulation_data/Validation/prescreening/prescreening_data/prescreen_run_results/` | Per-run prescreen result summaries (`run_results_*.json`; two JSON schemas) |
| `simulation_data/Validation/audit_reports/` | Historical footer audit scripts and reports (`check_missing_results*.py`, CSV/MD reports) |
| `simulation_data/Documentation/problematic_ics/` | Directories of ICs moved during Brutus execution (hierarchical: 3, hierarchical_for_gold_standard: 3, standard: 695) |
| `simulation_data/Documentation/problematic_ics_blacklist.json` | Legacy blacklist (2 hierarchical, 63 standard IDs); **not** used by current runners |

### Additional Documentation

- [Root README](../README.md) - Project overview and architecture
- [PINN Pipeline](../pinn/data-processing-pipeline-full.py) - ML data preprocessing

---

## Changelog

| Date | Change |
|------|--------|
| 2025-12-23 | Initial documentation creation |
| 2026-03-09 | Audit update: corrected gap counts (143/1250/1434), documented gold `_gold_` filename infix, rewrote Result footer section (all files have footers; schema varies by eta/tol presence), updated OS-path and IC-folder reference counts, added adaptive-threshold and runner-default notes, replaced stale blacklist/missing-footer claims with current provenance |
| 2026-03-19 | Consolidated IC layout: removed gold IC folders (ic_hierarchical_for_gold_standard/, ic_standard_quasi_random_for_gold_standard/), externalized ic_raw via IC_RAW_DIR environment variable, documented 184-ID standard quasi-random gold subset exclusion |
| 2026-04-26 | Merged DATASET_DOCUMENTATION.md and README.md into single unified README.md; corrected blacklist standard ID count (63 not 64); added Quick Start, Folder Structure, and additional known anomalies from README.md |
| 2026-04-26 | Audit fix: corrected 6 stale file paths (Stage 2 script, processing index JSONs, prescreen results, metrics locations, missing-results provenance); removed stale Anomaly #7 (validation framework no longer broken); fixed folder structure tree to reflect prescreening_data/ subdirectory |

---

*End of Documentation*
