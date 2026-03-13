# 3_Body_Problem: Data Pipeline

## Overview

This folder contains the complete data pipeline for the three-body simulation project. It handles:
- **Stage 1**: Initial Condition (IC) generation
- **Stage 2**: Prescreening to filter unstable systems
- **Stage 3**: High-precision Brutus integration
- **Stage 4**: Metrics calculation

The pipeline produces training data for the PINN (Physics-Informed Neural Network) system in the parent `pinn/` directory.

---

## Pipeline Stages

### Stage 1: IC Generation

**Purpose:** Generate initial conditions for three-body systems.

**Key Scripts:**
- `generate_enhanced_ics.py` - Main entry point for IC generation
- `FINAL_ic_generator_enhanced.py` - Core IC generation logic

**Configuration (in generate_enhanced_ics.py):**
```python
GENERATE_STANDARD = True      # Standard quasi-random ICs
GENERATE_HIERARCHICAL = True  # Hierarchical triple systems
N_SAMPLES_STANDARD = 2500
N_SAMPLES_HIERARCHICAL = 1500
epsilon = 0.05                # Position perturbation
velocity_scale = 0.1          # Velocity magnitude
scale_range = (0.8, 1.2)      # Global scaling factor
```

**Output:** `ic_raw_datasets/`
- `ic_hierarchical/` - Hierarchical triple systems
- `ic_standard_quasi_random/` - Standard quasi-random configurations

**IC File Format:**
```
m1 x1 y1 z1 vx1 vy1 vz1
m2 x2 y2 z2 vx2 vy2 vz2
m3 x3 y3 z3 vx3 vy3 vz3
```
- Mass (m), position (x,y,z), velocity (vx,vy,vz) for each of 3 bodies
- Natural units with G=1, total mass ≈ 3

---

### Stage 2: Prescreening

**Purpose:** Filter unstable ICs using short-term leapfrog integration.

**Key Script:** `prescreen_stage2/stage2_prescreening_revised_auto.py`

**Parameters:**
```python
TMAX = 1.0                    # Integration time
DT = 0.0001                   # Time step
ENERGY_ERROR_THRESHOLD = 0.01 # 1% relative energy error
MIN_DISTANCE_THRESHOLD = 0.01 # Minimum separation
VIRIAL_RATIO_MIN = 0.001
VIRIAL_RATIO_MAX = 2.0
```

**Input:** `ic_raw_datasets/`

**Output:**
- `final_stage_ic_datasets/` - Prescreened ICs
  - `ic_hierarchical/`
  - `ic_hierarchical_for_gold_standard/`
  - `ic_standard_quasi_random/`
  - `ic_standard_quasi_random_for_gold_standard/`
- `processing_index_ic_hierarchical.json` - Tracking metadata
- `processing_index_ic_standard_quasi_random.json` - Tracking metadata

**Logic:** Uses JIT-compiled leapfrog integrator to reject ICs that:
- Have energy error > 1%
- Experience collisions (min separation < 0.01)
- Have extreme virial ratios

---

### Stage 3: Brutus Integration

**Purpose:** Run high-precision N-body simulations using the Brutus integrator.

**Algorithm:** Brutus uses the **Bulirsch-Stoer extrapolation method** with:
- **Base integrator:** Leapfrog (velocity Verlet) scheme
- **Extrapolation sequence:** n = 1, 2, 4, 6, 8, ..., 56 substeps
- **Precision:** GNU MPFR via `mpreal` wrapper; user-specified word length (MPFR digits ≈ Lw/log₂(10))
- **Adaptive stepping:** `dt = eta * (r/a)^0.25` where eta is tolerance-derived step-size controller

**Key Scripts:**
- `run_brutus_both_type_simple.py` - Main batch runner
- `run_brutus_hierarchical_only_mac_gold_standard.py` - Gold standard hierarchical

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

**⚠️ Parameter Heterogeneity Caveat:** The values above are defaults from runner scripts. Actual output files within each folder show heterogeneity (multiple `tol`/`Lw` values) due to reruns, script evolution, and manual interventions. See `DATASET_DOCUMENTATION.md` for detailed per-folder parameter breakdowns.

**Integration Contract:**
- **Timeout:** 3000 seconds (50 minutes) per simulation
- **Parallel execution:** `ProcessPoolExecutor` with `max(1, cpu_count - 1)` workers
- **Failure handling:**
  - Validates final timestep ≥ 9.5
  - Moves failed IC to `problematic_ics/{variant}/`
  - Deletes partial output file

**Input:** `final_stage_ic_datasets/`

**Output:** `brutus_output/`
- `brutus_hierarchical/`
- `brutus_hierarchical_gold_standard/`
- `brutus_standard_quasi_random/`
- `brutus_standard_quasi_random_gold_standard/`

**Brutus Output Format:**
```
t N t_cpu
m1 x1 y1 z1 vx1 vy1 vz1
m2 x2 y2 z2 vx2 vy2 vz2
m3 x3 y3 z3 vx3 vy3 vz3

[timestamp repeats with blank line between snapshots]
Result: filename=... N=... t_begin=... t_end=... dt=... [eta=...] [tol=...] Lw=... t_cpu=... E_initial=... E_final=... dE/E=...
```

- **Snapshot header:** timestamp, body count, CPU time
- **Body lines:** mass and state for each body (30-40 significant digits)
- **Blank line separator:** Between snapshots (critical for parsing)
- **Result footer:** Appended to stderr, schema varies (see below)

**Result Footer Schemas:**

All files contain a `Result:` footer, but schema varies by Brutus build:

| Schema | Fields | Example |
|--------|--------|---------|
| Full | filename, N, t_begin, t_end, dt, **eta**, **tol**, Lw, t_cpu, E_initial, E_final, dE/E | `Result: filename=... dt=0.08 eta=0.263027 tol=1e-15 Lw=130 ...` |
| Partial | filename, N, t_begin, t_end, dt, **tol** (no eta), Lw, t_cpu, E_initial, E_final, dE/E | `Result: filename=... dt=0.08 tol=1e-15 Lw=130 ...` |
| Minimal | filename, N, t_begin, t_end, dt, Lw, t_cpu, E_initial, E_final, dE/E (no eta/tol) | `Result: filename=... dt=0.01 Lw=130 ...` |

**Per-folder distribution:**
- `brutus_hierarchical/`: 3,307 full-schema, 1,550 partial (no eta)
- `brutus_hierarchical_gold_standard/`: 4,857 full-schema
- `brutus_standard_quasi_random/`: 2,048 full-schema, 701 partial
- `brutus_standard_quasi_random_gold_standard/`: 2,346 full-schema, 219 minimal

**Parsing note:** Treat `eta` and `tol` as optional fields. Use final timestep ≥ 9.5 as primary completeness check.

**Validation:**
- **Completeness check:** final timestamp ≥ 9.5
- **Do NOT use:** line count thresholds (variable due to dynamics), specific Result footer schema (varies)

---

### Stage 4: Metrics Calculation

**Purpose:** Calculate conservation metrics and quality indicators.

**Key Script:** `brutus_metrics/calculate_metrics.py`

**Metrics Calculated:**
- Energy conservation (relative drift)
- Linear momentum conservation
- Angular momentum conservation
- Escape detection (max separation > 100)
- Collision detection (min separation < 0.01)

**Input:** `brutus_output/`

**Output:** `brutus_metrics/sim_result_metric_*/`
- JSON files with metrics for each simulation ID

---

## Dataset Inventory

### IC Datasets (final_stage_ic_datasets/)

| Folder | Type | Files | ID Range |
|--------|------|-------|----------|
| `ic_hierarchical/` | IC | ~4,857 | 0000-4999 |
| `ic_hierarchical_for_gold_standard/` | IC | ~4,857 | 0000-4999 |
| `ic_standard_quasi_random/` | IC | ~2,749 | 0000-3998 |
| `ic_standard_quasi_random_for_gold_standard/` | IC | ~2,565 | 0000-3998 |

### Brutus Output Datasets (brutus_output/)

| Folder | Type | Files | Disk Usage |
|--------|------|-------|------------|
| `brutus_hierarchical/` | Trajectory | ~4,857 | ~531 MB |
| `brutus_hierarchical_gold_standard/` | Trajectory | ~4,857 | ~2.4 GB |
| `brutus_standard_quasi_random/` | Trajectory | ~2,749 | ~122 MB |
| `brutus_standard_quasi_random_gold_standard/` | Trajectory | ~2,565 | ~1.7 GB |

**Total Dataset Size:** ~4.86 GB

---

## Data Variants

### Hierarchical Systems
- Stable triple systems with inner binary + outer third body
- Inner binary semi-major axis: a ~ 0.1-0.3
- Outer body: 3-10× inner separation
- Near-planar (small inclinations)
- Masses normalized to total ~3, then perturbed with sigma=0.01

### Standard Quasi-Random
- Sobol-based sampling with scrambling
- p1 fixed at (1, 0, 0), p2 on hemisphere (x ≤ 0), p3 = -(p1 + p2)
- Masses exactly 1.0 each
- COM and momentum exactly zero by construction

### Gold Standard
- Finer timestep (dt_out=0.01) for higher temporal resolution
- Stricter tolerance parameters
- Higher precision outputs (more significant digits)

---

## Problematic ICs

**Tracking:** `problematic_ics_blacklist.json`

Failed ICs are moved to:
- `problematic_ics/hierarchical/`
- `problematic_ics/hierarchical_for_gold_standard/`
- `problematic_ics/standard/`

**Known failed IDs:**
- Hierarchical: 123, 253 (partial list)
- Standard: 21, 30, 52, 89, 121, ... (extensive list)

---

## Interaction Diagram

```
ic_raw_datasets/           [Stage 1 output - raw generated ICs]
    |
    v
prescreen_stage2/  -->  final_stage_ic_datasets/   [Stage 2 - prescreened ICs]
    |                           |
    |                           v
    |                   run_brutus_*.py  -->  brutus_output/   [Stage 3 - trajectories]
    |                               |
    |                               v
    +--------------------->  brutus_metrics/     [Stage 4 - metrics]
```

---

## Known Issues

1. **dataset_readiness_checks/ is broken**
   - Throws `NameError: name 'ValidationConfig' is not defined`
   - Use `brutus_metrics/` instead for validation

2. **Gold standard standard-quasi-random has no runner**
   - Cannot natively reproduce `ic_standard_quasi_random_for_gold_standard` outputs

3. **Hierarchical COM offset**
   - COM and momentum are perturbed with sigma=0.01 after construction
   - Re-center manually if translationally-invariant networks require exact COM frame

4. **Naming inconsistencies**
   - Some legacy scripts use hardcoded variant names that differ from actual folder schemas

---

## Running the Pipeline

```bash
# Stage 1: Generate ICs
python3 3_Body_Problem/generate_enhanced_ics.py

# Stage 2: Prescreen
python3 3_Body_Problem/prescreen_stage2/stage2_prescreening_revised_auto.py

# Stage 3: Run Brutus (requires compiled brutus binary)
python3 3_Body_Problem/run_brutus_both_type_simple.py

# Stage 4: Calculate metrics
python3 3_Body_Problem/brutus_metrics/calculate_metrics.py
```

---

## Related Documentation

- [Dataset Documentation](./data_documentation/DATASET_DOCUMENTATION.md) - Detailed specs and anomalies
- [Root README](../README.md) - Project overview and architecture
- [PINN Pipeline](../pinn/data-processing-pipeline-full.py) - ML data preprocessing

---

## Folder Structure

```
3_Body_Problem/
├── FINAL_ic_generator_enhanced.py    # Core IC generator
├── generate_enhanced_ics.py           # Stage 1 entry point
├── run_brutus_both_type_simple.py     # Stage 3 main runner
├── run_brutus_hierarchical_only_mac_gold_standard.py  # Gold runner
├── brutus_progress.json               # Run tracking
├── ic_raw_datasets/                   # Raw ICs (Stage 1 output)
│   ├── ic_hierarchical/
│   └── ic_standard_quasi_random/
├── final_stage_ic_datasets/           # Prescreened ICs (Stage 2 output)
│   ├── ic_hierarchical/
│   ├── ic_hierarchical_for_gold_standard/
│   ├── ic_standard_quasi_random/
│   └── ic_standard_quasi_random_for_gold_standard/
├── brutus_output/                      # Integrated trajectories (Stage 3 output)
│   ├── brutus_hierarchical/
│   ├── brutus_hierarchical_gold_standard/
│   ├── brutus_standard_quasi_random/
│   └── brutus_standard_quasi_random_gold_standard/
├── prescreen_stage2/                   # Stage 2 scripts
│   ├── stage2_prescreening_revised_auto.py
│   ├── processing_index_*.json
│   └── prescreening_utils.py
├── brutus_metrics/                      # Stage 4 scripts
│   ├── calculate_metrics.py
│   └── sim_result_metric_*/
├── dataset_readiness_checks/           # Validation (broken)
├── data_documentation/                 # Dataset docs
│   └── DATASET_DOCUMENTATION.md
├── problematic_ics/                     # Failed ICs
│   ├── hierarchical/
│   ├── hierarchical_for_gold_standard/
│   └── standard/
├── problematic_ics_blacklist.json       # Failed ID list
└── testing_data/                        # Test ICs/outputs
```