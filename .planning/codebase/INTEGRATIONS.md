# External Integrations

**Analysis Date:** 2026-04-27

## Integration Architecture Overview

This project has **no external network services, APIs, databases, or cloud integrations.** All integration is:
1. **File-based** between pipeline stages
2. **Subprocess-based** (Python spawns Brutus C++ binary)
3. **Environment-based** (`IC_RAW_DIR` variable for external raw IC storage)
4. **GitHub Actions** for Gemini AI assistant automation only

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                          PIPELINE DATA FLOW                              │
│                                                                          │
│  [External IC Raw Storage]                                               │
│     │ $IC_RAW_DIR                                                        │
│     ▼                                                                    │
│  ┌─────────────┐     ┌──────────────┐     ┌──────────────┐              │
│  │ Stage 1:    │────▶│ Stage 2:     │────▶│ Stage 3:     │              │
│  │ IC Gen      │     │ Prescreening │     │ Brutus Sim   │              │
│  │ generate_   │     │ stage2_      │     │ run_brutus_  │              │
│  │ ics.py      │     │ prescreening │     │ both_type_   │              │
│  │             │     │ _revised_    │     │ simple.py    │              │
│  │             │     │ auto.py      │     │              │              │
│  └──────┬──────┘     └──────┬───────┘     └──────┬───────┘              │
│         │ .txt              │ .txt               │ .txt                  │
│         ▼                   ▼                    ▼                       │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐              │
│  │ ic_raw/      │    │ ic_final/    │    │ brutus_      │              │
│  │ ic_hier/     │    │ ic_hier/     │    │ output/      │              │
│  │ ic_standard/ │    │ ic_standard/ │    │ brutus_hier/ │              │
│  └──────────────┘    └──────────────┘    │ brutus_std/  │              │
│                                          └──────┬───────┘              │
│                                                 │                       │
│                          ┌──────────────────────┘                       │
│                          ▼                                              │
│                   ┌──────────────┐                                      │
│                   │ Stage 4:     │                                      │
│                   │ Metrics      │                                      │
│                   │ calculate_   │                                      │
│                   │ metrics.py   │                                      │
│                   └──────┬───────┘                                      │
│                          │ .json                                        │
│                          ▼                                              │
│                   ┌──────────────┐                                      │
│                   │ metrics/     │                                      │
│                   │ sim_result_  │                                      │
│                   │ metric_*/    │                                      │
│                   └──────────────┘                                      │
│                                                                          │
│  IC files + Brutus outputs ──────────────▶ ┌──────────────────┐        │
│                                             │ PINN Preprocessing│        │
│                                             │ data-processing-  │        │
│                                             │ pipeline-full.py  │        │
│                                             └────────┬─────────┘        │
│                                                      │ .h5              │
│                                                      ▼                  │
│                                             ┌──────────────────┐        │
│                                             │ HDF5 Preprocessed │        │
│                                             │ Dataset           │        │
│                                             └────────┬─────────┘        │
│                                                      │                  │
│                                                      ▼                  │
│                                             ┌──────────────────┐        │
│                                             │ CTL-PINN Training │        │
│                                             │ (WIP)             │        │
│                                             └──────────────────┘        │
└──────────────────────────────────────────────────────────────────────────┘
```

## Pipeline Stage Integration Details

### Stage 1: Initial Condition Generation

**Entry Point:** `simulation_data/Scripts/ic_generation/generate_ics.py`
**Core Logic:** `simulation_data/Scripts/ic_generation/ic_generation_utils.py`

**Input:**
- Environment variable `IC_RAW_DIR` must point to external raw IC storage
- Configuration: epsilon=0.05, velocity_scale=0.1, scale_range=(0.8, 1.2)

**Output:** Text files written to `$IC_RAW_DIR/ic_hierarchical/` and `$IC_RAW_DIR/ic_standard_quasi_random/`

**File Format Contract (IC File):**
```
m1 x1 y1 z1 vx1 vy1 vz1
m2 x2 y2 z2 vx2 vy2 vz2
m3 x3 y3 z3 vx3 vy3 vz3
```
- 3 lines, 7 space-separated numeric values each
- Two sub-variants: standard quasi-random (masses exactly 1.0) and hierarchical (variable masses, normalized to total ~3)

**IC Type Distinctions:**

| Property | Standard Quasi-Random | Hierarchical |
|----------|----------------------|--------------|
| Masses | Exactly 1.0 each | Variable, normalized to total ~3 |
| COM/Momentum | Exactly 0 by construction | Perturbed with Gaussian noise (sigma=0.01) |
| Orientation | Full 3D, large \|z\| possible | Near-planar, small inclinations |
| Sampling method | Sobol quasi-random, p1 fixed at (1,0,0) | Stable hierarchical: binary + outer body |

### Stage 2: Prescreening

**Entry Point:** `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py`
**Core Logic:** `simulation_data/Validation/prescreening/prescreening_utils.py`

**Input:**
- IC files from `$IC_RAW_DIR/ic_hierarchical/` or `$IC_RAW_DIR/ic_standard_quasi_random/`
- Reads `IC_RAW_DIR` environment variable

**Output:**
- Accepted IC files copied to `simulation_data/Data/ic_final/ic_hierarchical/` and `simulation_data/Data/ic_final/ic_standard_quasi_random/`
- Prescreening logs at `simulation_data/Validation/prescreening/processing_index_ic_*.json`
- Rejected ICs are not moved (they stay in `ic_raw/`)

**Validation Logic** (from `stage2_prescreening_revised_auto.py`):
- Parameters: TMAX=1.0, DT=0.0001, ENERGY_ERROR_THRESHOLD=0.01, MIN_DISTANCE_THRESHOLD=0.01
- Short leapfrog integration; rejects unstable ICs based on energy conservation and minimum separation

**Contract:** Input and output files maintain identical format and naming. Prescreening is a filter, not a transformation.

### Stage 3: Brutus High-Precision Integration

**Brutus Binary:** `brutus_Newton-main/brutus` (C++ executable)

**Runner Scripts:**
- Standard batch: `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py`
- Gold-standard hierarchical: `simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py`

**CLI Interface:**
```bash
./brutus <tolerance> <word_length> <t_begin> <t_end> <dt_out> <n_particles> <input_file>
```

| Argument | Typical Hierarchical | Typical Standard | Description |
|----------|---------------------|------------------|-------------|
| tolerance | 1e-15 | 1e-13 | Bulirsch-Stoer tolerance |
| word_length | 130 | 118 | Working precision in bits |
| t_begin | 0 | 0 | Start time |
| t_end | 10 | 10 | End time |
| dt_out | 0.08 | 0.17 | Output sampling interval |
| n_particles | 3 | 3 | Number of bodies |
| input_file | (IC file) | (IC file) | Absolute path to IC |

**Gold-standard parameters:**
- Hierarchical gold: tol=1e-13, Lw=130, dt_out=0.01 (`run_brutus_hierarchical_only_mac_gold_standard.py:39-45`)
- Standard gold: tol=1e-13 or 1e-14, Lw=130, dt_out=0.01 (external runner, not in repo)

**Output Format (Brutus Trajectory File):**
```
0.000 3 0.00123
m1 x1 y1 z1 vx1 vy1 vz1
m2 x2 y2 z2 vx2 vy2 vz2
m3 x3 y3 z3 vx3 vy3 vz3

0.080 3 0.00234
...
[blank line between snapshots]

Result: filename=... N=3 t_begin=... t_end=... dt=... eta=... tol=... Lw=... t_cpu=... E_initial=... E_final=... dE/E=...
```
- Body data lines contain 30-40 significant digits (arbitrary precision)
- `Result:` footer is **optional** (some files omit it). When present, schema varies: some omit `eta`, a subset of standard gold files omit both `eta` and `tol`.
- `Result:` paths can be macOS or Windows format

**Output Directories:**
- `simulation_data/Data/brutus_output/brutus_hierarchical/`
- `simulation_data/Data/brutus_output/brutus_hierarchical_gold_standard/`
- `simulation_data/Data/brutus_output/brutus_standard_quasi_random/`
- `simulation_data/Data/brutus_output/brutus_standard_quasi_random_gold_standard/`

**Python-to-Brutus Integration:**
- `subprocess.run()` with `stdout` redirected to output file
- `stderr` merged into stdout (`stderr=subprocess.STDOUT`)
- Timeout: 3000 seconds per simulation (set in `run_brutus_both_type_simple.py:29`)
- Parallel execution: `ProcessPoolExecutor` with `cpu_count() - 1` workers each spawning a separate `brutus` process

**Completeness Validation:**
- Final timestamp must be >= 9.5 (validated by regex `r'^(\d+\.?\d*)\s+3\s+\d+'` matching timestep headers)
- Incomplete results trigger IC file relocation to `Documentation/problematic_ics/`
- Blacklist at `simulation_data/Documentation/problematic_ics_blacklist.json` tracks persistently failing ICs

### Stage 4: Metrics Calculation

**Entry Point:** `simulation_data/Scripts/metrics_calculation/calculate_metrics.py`

**Input:** Brutus output files from `simulation_data/Data/brutus_output/`

**Output:** JSON metrics files at matching paths under `simulation_data/Data/metrics/`

**Output Directories:**
- `simulation_data/Data/metrics/sim_result_metric_hierarchical/`
- `simulation_data/Data/metrics/sim_result_metric_hierarchical_gold_standard/`
- `simulation_data/Data/metrics/sim_result_metric_standard/`
- `simulation_data/Data/metrics/sim_result_metric_standard_gold_standard/`

**Metric quantities:** Energy drift, momentum drift, angular momentum drift, ejection flags (max separation > 100), collision flags (min separation < 0.01), integration duration.

**File naming contract:** The numeric ID in the filename maps IC to Brutus output to metrics. The folder defines the variant (hierarchical/standard, regular/gold), NOT the filename.

### Stage 5: PINN Data Preprocessing

**Primary Script:** `pinn/data-processing-pipeline-full.py`

**Modular Libraries (in `pinn/data-handling/`):**
- `core/data_structures.py` - Dataclasses: `SimulationMetadata`, `RawTrajectoryData`, `ScaledTrajectoryData`, `PhysicalInvariants`, `ProcessedTrajectory`, `GlobalScales`
- `core/parsing.py` - File parsers for IC and Brutus formats
- `core/scaling.py` - Dimensionless scaling via characteristic length/velocity/time
- `processing/invariants.py` - Physical invariants: E, Q, s_min, L_norm, I_norm, tau_L
- `processing/stage_assignment.py` - 7-stage curriculum (0-6) based on invariants
- `processing/input_vector.py` - 13-component normalized IC vector formulation
- `scripts/preprocess_dataset.py` - CLI pipeline for batch preprocessing
- `scripts/prepare_training_data.py` - Stage-based training data preparation

**Input:**
- IC files from `simulation_data/Data/ic_final/`
- Brutus output files from `simulation_data/Data/brutus_output/`

**Processing Flow:**
1. Parse IC + Brutus file pairs → `RawTrajectoryData`
2. Compute global scales (D, V) across entire dataset
3. Scale trajectories to dimensionless units → `ScaledTrajectoryData`
4. Compute physical invariants (E, Q, s_min, L_norm, I_norm, tau_L via Rosenstein Lyapunov)
5. Assign curriculum stage (0-6)
6. Formulate 13-component normalized IC vector
7. Save to HDF5 format

**Output:** Single HDF5 file containing all preprocessed trajectories, global scales, dataset statistics, stage assignments, and IC vectors.

**PINN Input Vector Contract (13 components, all normalized to [-1, 1]):**
| Index | Component | Source |
|-------|-----------|--------|
| 0-2 | m1, m2, m3 (mass fractions) | `m_norm = 2*(m_i/m_total) - 1` |
| 3 | E (normalized) | `tanh(E / E_scale)` |
| 4 | L_norm (normalized) | `2*L_norm - 1` |
| 5 | Q (normalized) | `tanh((Q-1) / Q_scale)` |
| 6 | s_min (normalized) | `tanh(s_min / smin_scale)` |
| 7-9 | I1, I2, I3 (shape invariants) | Pairwise distance ratios |
| 10-11 | theta1, theta2 (velocity angles) | `2*(angle/pi) - 1` |
| 12 | I_norm (normalized) | `tanh(I_norm)` |

**Training Data Preparation** (from `prepares_training_data.py`):
- Loads per-stage data from HDF5
- Creates batches organized by curriculum stage with replay (previous stages included in current)
- Time sampling strategies: uniform, acceleration-weighted, or mixed
- Outputs per-stage: `training_data.npz`, `batches.pkl`, `summary.json`

### Stage 6: PINN Training (Work in Progress)

**Architecture:** `pinn/basic_architecture.py`

**Model:** SQRSkipResNetSIREN
- Input: 14 dimensions (t + 13-component IC vector)
- Output: 9 dimensions (3D positions of 3 bodies)
- 12 hidden layers, 256 neurons each
- SIREN activation (first_omega_0=30.0, hidden_omega_0=1.0)
- Skip connections with power term p=2 on odd layers
- LayerNorm (elementwise_affine=True, eps=1e-5) on odd layers
- Final linear layer (no activation, weights U[-0.01, 0.01])
- Second-order autodiff for velocity and acceleration via `torch.autograd.grad`

**Training status:** Architecture implemented and verified (forward pass + gradient computation tested). Full training loop, physics loss, and CTL (Curriculum Training) logic are not yet in the committed code.

## Data Storage and File Formats

### Directory Layout (Committed to Git)

```
simulation_data/
├── Scripts/                          # Pipeline scripts (committed)
│   ├── ic_generation/                # Stage 1: IC generation
│   ├── brutus_runners/              # Stage 3: Brutus orchestration
│   ├── metrics_calculation/         # Stage 4: Metrics extraction
│   └── debug/                       # Audit and diagnostic tools
├── Validation/                       # Quality assurance (committed)
│   ├── prescreening/                # Stage 2: Prescreening logic
│   ├── audit_reports/               # Footer audit reports
│   ├── analysis/                    # Metrics analysis and viz
│   └── dataset_readiness_checks/    # Dataset validation framework
├── Documentation/                    # Documentation (committed)
│   ├── README.md                    # Dataset specification
│   └── problematic_ics_blacklist.json
└── Data/                             # Data directories (in .gitignore)
    ├── ic_final/                    # Prescreened ICs
    ├── brutus_output/               # Brutus simulation results
    ├── metrics/                     # JSON metrics files
    └── testing_data/                # Test pipeline artifacts
```

### File Formats Summary

| Format | Extension | Stage | Consumer | Notes |
|--------|-----------|-------|----------|-------|
| Plain text (space-separated) | `.txt` | IC Gen, Brutus out | All stages | 30-40 sig digits for high-precision values |
| JSON | `.json` | Metrics, prescreening, validation | Humans, analysis scripts | Key-value configs, result reports |
| HDF5 | `.h5`, `.hdf5` | PINN preprocessing | PINN training | Structured hierarchical data |
| NumPy archive | `.npz` | PINN training prep | PINN training | IC vectors, metadata, invariants |
| Pickle | `.pkl` | PINN training prep | PINN training | Serialized training batches |
| Markdown | `.md` | Documentation | Humans, AI | Methodological instructions |
| LaTeX | `.tex` | Research docs | pdflatex | Methodology papers |
| PDF | `.pdf` | Compiled LaTeX | Humans | Final instruction documents |

## Environment Variable Dependencies

### Required

| Variable | Set By | Purpose | Failure Mode |
|----------|--------|---------|--------------|
| `IC_RAW_DIR` | User (shell) | External raw IC storage path | Scripts exit with `SystemExit(1)` and error message |

### Access Pattern

The `IC_RAW_DIR` variable is read at runtime, not build time:
```python
# ic_generation_utils.py:595-607
IC_RAW_DIR = os.environ.get('IC_RAW_DIR')
if IC_RAW_DIR is None:
    raise SystemExit(
        "IC_RAW_DIR environment variable not set. "
        "This script requires an external ic_raw directory with "
        "subdirs: ic_hierarchical/ and ic_standard_quasi_random/\n"
        "Example: export IC_RAW_DIR=/path/to/ic_raw"
    )
```

The same pattern is used in `stage2_prescreening_revised_auto.py:38-44` and `prescreening_utils.py:212-214`.

## GitHub Actions Integration (Gemini AI Assistant)

The project uses GitHub Actions exclusively for Gemini AI automation, not for CI/CD:

| Workflow | File | Trigger | Function |
|----------|------|---------|----------|
| Gemini Dispatch | `gemini-dispatch.yml` | PR open, issue open, `@gemini-cli` comment | Routes user requests to review/triage/invoke |
| Gemini Review | `gemini-review.yml` | Called by dispatch | AI-powered PR review using Google Gemini |
| Gemini Triage | `gemini-triage.yml` | Called by dispatch | AI-powered issue triage |
| Gemini Invoke | `gemini-invoke.yml` | Called by dispatch | General Gemini invocation |
| Scheduled Triage | `gemini-scheduled-triage.yml` | Schedule | Periodic issue triage |

**External dependencies:**
- Google Cloud Platform (Vertex AI) for Gemini API
- Google Cloud service account (workload identity federation)
- GitHub Container Registry (`ghcr.io/github/github-mcp-server:v0.18.0`) for MCP tool access
- Required GitHub Secrets: `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `APP_PRIVATE_KEY`, `GITHUB_TOKEN`
- Required GitHub Variables: `GOOGLE_CLOUD_LOCATION`, `GOOGLE_CLOUD_PROJECT`, `SERVICE_ACCOUNT_EMAIL`, `GCP_WIF_PROVIDER`

These workflows are non-essential for the core research pipeline and serve as an AI productivity augmentation layer.

## Git-Based Integration

**No submodules.** The `.gitmodules` file does not exist. All reference code is directly committed (or excluded via `.gitignore`).

**Git hooks:**
- `.github/commands/` directory contains Gemini command definitions (TOML files). These are not standard git hooks.
- No pre-commit, post-commit, or pre-push hooks detected.

## Missing Integrations

The following integration points do NOT currently exist:

1. **No CI/CD for core pipeline.** No automated build/test for Brutus, no automated prescreening validation, no automated metrics extraction.
2. **No experiment tracking.** No MLflow, Weights & Biases, TensorBoard, or custom logging for PINN training runs.
3. **No data versioning.** No DVC, Git LFS, or artifact registry for simulation data or trained models.
4. **No dependency management.** No Python lockfile, no conda environment file, no Docker image for reproducible environments.
5. **No model registry.** No system for tracking trained PINN checkpoints (`.gitignore` excludes `.pt`, `.pth`, `.ckpt` files).
6. **No Docker/Container setup.** Brutus compilation requires manual dependency installation (GMP, MPFR, mpreal).
7. **No MPS/GPU acceleration for PINN.** Training runs on CPU only on macOS. No ROCm, CUDA, or MPS detection.

---

*Integration audit: 2026-04-27*
