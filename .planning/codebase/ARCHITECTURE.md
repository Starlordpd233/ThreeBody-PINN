# Architecture

**Analysis Date:** 2026-04-27

## System Overview

This codebase implements a complete three-body simulation and CTL-PINN (Curriculum-Trained Physics-Informed Neural Network) training stack. It is a **batch scientific computing system** with no servers, no APIs, and no databases. All inter-component communication occurs through the filesystem using text and HDF5 files. The system has two runtime personalities: a **C++ high-precision numerical integrator** invoked as a subprocess, and a **Python pipeline** that orchestrates, validates, and processes data across 6 stages.

```mermaid
graph TD
    subgraph "Stage 1: IC Generation"
        A1[ic_generation_utils.py] --> A2[generate_ics.py]
        A2 --> A3[IC .txt files<br/>ic_hierarchical: 4,857<br/>ic_standard_quasi_random: 2,749]
    end

    subgraph "Stage 2: Prescreening"
        B0[prescreening_utils.py] --> B1[stage2_prescreening_revised_auto.py]
        A3 --> B1
        B1 --> B2[Validated ICs]
        B1 --> B3[Blacklist JSON<br/>problematic_ics_blacklist.json]
        B1 --> B4[Processing Index JSONs]
    end

    subgraph "Stage 3: Brutus Integration"
        C1[run_brutus_both_type_simple.py] --> Csub[brutus subprocess]
        C5[run_brutus_hierarchical_only_mac_gold_standard.py] --> Csub
        Csub --> C2[C++ Components]
        C2 --> C3[Brutus output .txt<br/>hier: 4,857 | hier_gold: 4,857<br/>std: 2,749 | std_gold: 2,565]
    end

    subgraph "Stage 4: Metrics"
        D1[calculate_metrics.py] --> D2[Metrics JSON ~15,047 files]
        C3 --> D1
    end

    subgraph "Stage 5: PINN Data Processing"
        E1[data-processing-pipeline-full.py<br/>monolithic, 1,650 lines]
        E1mod[data-handling/ modular refactor<br/>2,550 lines across 10 files]
        A3 --> E1
        C3 --> E1
        E1 --> E2[HDF5 preprocessed data]
        E2 --> E3[Stage-based training .npz + .pkl]
    end

    subgraph "Stage 6: PINN Training"
        F1[basic_architecture.py]
        F2[SQRSkipResNetSIREN<br/>14→256×12→9<br/>with SIREN + skip + LayerNorm]
        E3 --> F2
        F2 --> F3[Physics loss + data loss]
    end

    subgraph "Cross-Cutting: Validation Layer"
        V1[Dataset Readiness Checks<br/>11 modules]
        V1 --> V1a[completeness.py]
        V1 --> V1b[correspondence.py]
        V1 --> V1c[physics.py]
        V1 --> V1d[curriculum.py]
        V1 --> V1e[... 7 more modules]
        V2[Audit Reports]
        V3[Footer Audit Scripts]
    end

    A3 --> V1
    C3 --> V1
    D2 --> V1
```

## Component Responsibilities

| Component | Responsibility | Key File |
|-----------|----------------|----------|
| Brutus C++ Integrator | High-precision N-body integration via Bulirsch-Stoer extrapolation method | `brutus_Newton-main/Brutus.cpp` (11 lines of header, ~150 lines impl) |
| Star / Cluster | Single-body state representation and N-body container with acceleration calculation | `brutus_Newton-main/Star.h`, `brutus_Newton-main/Cluster.h` |
| Bulirsch-Stoer Integrator | Richardson extrapolation-based adaptive ODE integrator | `brutus_Newton-main/Bulirsch_Stoer.cpp` |
| IC Generation | Create hierarchical (binary+outer) and standard quasi-random (Sobol) initial conditions | `simulation_data/Scripts/ic_generation/generate_ics.py` |
| IC Generation Utils | Core sampling logic: Sobol sequences, hierarchical parameter sampling | `simulation_data/Scripts/ic_generation/ic_generation_utils.py` |
| Prescreening | Filter unstable ICs via short leapfrog integration with energy/distance thresholds | `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py` |
| Batch Runner | Orchestrate parallel Brutus simulations with timeout, validation, and failure handling | `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py` |
| Gold Standard Runner | Batch runner for hierarchical gold-standard higher-fidelity re-simulations | `simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py` |
| Metrics Calculator | Extract conservation metrics (energy, momentum, angular momentum) from all Brutus outputs | `simulation_data/Scripts/metrics_calculation/calculate_metrics.py` |
| Brutus Metrics Calculator | Alternative metrics extractor with validation logic | `simulation_data/Scripts/metrics_calculation/calculate_brutus_metrics.py` |
| Dataset Readiness Validator | 11-module validation suite for production data quality assurance | `simulation_data/Validation/dataset_readiness_checks/` |
| PINN Data Pipeline (monolithic) | Parse raw files, scale, compute invariants, assign stages, create training batches | `pinn/data-processing-pipeline-full.py` (1,650 lines) |
| PINN Data Pipeline (modular) | Refactored modular version: core/, processing/, scripts/ subpackages | `pinn/data-handling/` (2,550 lines across 10 files) |
| PINN Architecture | SQR-SkipResNet-SIREN neural network with DeepXDE API compatibility layer | `pinn/basic_architecture.py` (308 lines) |
| COM Transformation | Center-of-mass recentering for hierarchical ICs and Brutus outputs | `pinn/data-handling/core/com_transform_ic.py`, `com_transform_brutus.py` |
| LaTeX Research Docs | Technical methodology for CTL, PINN architecture, sampling, data quality | `pinn_instruction/original_latex/` (5 document sets, modular sections) |
| Reference Code | Vendored reference implementations for research comparison | `reference-code/` (10+ cloned repos: DeepXDE, SIREN, PINA, GravNN, HNN, etc.) |
| GSD Project Management | Phase-based project plan tracking and execution records | `.planning/` (9 phases, milestones, context sessions) |

## Pattern Overview

**Overall:** Filesystem-based Pipeline Architecture with GSD (Goal-Structured Development) project management

**Key Characteristics:**
- **Linear pipeline with modular stages**: Each stage reads from and writes to the filesystem with zero runtime coupling to upstream/downstream stages
- **C++ subprocess invocation**: The Brutus binary is compiled separately and invoked via `subprocess.run()` with CLI arguments; Python wrappers handle timeout, validation, and output management
- **File-based data interchange**: IC files (*.txt) -> Brutus output (*.txt) -> Metrics (*.json) -> Preprocessed data (*.h5) -> Training batches (*.npz, *.pkl)
- **Folder-defines-variant pattern**: "Gold" vs "standard" data quality is encoded in directory names, not file names. The same file naming convention is used across all variant folders
- **Dataclass-based data structures**: Python `@dataclass` classes (RawTrajectoryData, ScaledTrajectoryData, PhysicalInvariants, ProcessedTrajectory) form a type-safe pipeline chain
- **Plug-in validation modules**: The dataset readiness checker uses an 11-module plugin pattern with shared configuration
- **Curriculum learning stages**: 7 stages (0-6) of increasing difficulty based on physical invariants (E, Q, L_norm, s_min, tau_L)
- **DeepXDE API compatibility**: The PINN model inherits from an NN base class that mirrors DeepXDE transform patterns

## Layers

### C++ Simulation Layer
- **Purpose:** High-precision N-body numerical integration using the Bulirsch-Stoer extrapolation method
- **Location:** `brutus_Newton-main/`
- **Contains:** C++ source files (.cpp, .h), compiled binary (`brutus`), utility libraries (Timer, Data_Handler), test inputs, test output
- **Depends on:** MPFR (arbitrary-precision floating point), GMP (arbitrary-precision integers), libgmpxx (C++ bindings), Homebrew-installed libraries on macOS
- **Used by:** Python batch runners via `subprocess.run()`
- **Class hierarchy:** `Star` (individual body) -> `Cluster` (N-body container with acceleration) -> `Bulirsch_Stoer` (ODE integrator) -> `Brutus` (orchestrator)
- **Build system:** Hand-written Makefile with hardcoded macOS Homebrew paths, g++ with `-O3 -std=c++11`

### Python Simulation Pipeline Layer
- **Purpose:** IC generation, prescreening, batch orchestration, metrics extraction
- **Location:** `simulation_data/Scripts/` (active scripts), `simulation_data/Validation/` (validation and prescreening)
- **Contains:** Python scripts organized by function: `ic_generation/`, `brutus_runners/`, `metrics_calculation/`, `debug/`, `archived/`
- **Depends on:** numpy, scipy, subprocess (Brutus binary), pathlib, concurrent.futures (ProcessPoolExecutor)
- **Used by:** Direct command-line invocation, no programmatic import dependency between scripts
- **Concurrency:** ProcessPoolExecutor with max_workers = cpu_count - 1

### Data Layer
- **Purpose:** Persistent storage for all simulation inputs, outputs, and derived products
- **Location:** `simulation_data/Data/`
- **Contains:**
  - `ic_final/`: IC text files (2 variant folders, 7,606 total)
  - `brutus_output/`: Brutus trajectory text files (4 variant folders, 15,028 total)
  - `metrics/`: Conservation metrics JSON files (4 variant folders, ~15,047 total)
  - `testing_data/`: Small test subsets for development
- **Depends on:** Nothing (passive filesystem storage)
- **Used by:** All pipeline stages read from and write to this layer
- **Size:** ~63,000 files total, dominated by .txt and .json files

### PINN Data Processing Layer
- **Purpose:** Parse raw simulation data, normalize to dimensionless units, compute physical invariants, assign curriculum learning stages, prepare training batches
- **Location:** `pinn/data-processing-pipeline-full.py` (monolithic 1,650-line script), `pinn/data-handling/` (modular refactor: core/, processing/, scripts/)
- **Contains:**
  - `core/`: data_structures.py (123 lines), parsing.py (699 lines), scaling.py (241 lines), com_transform_*.py
  - `processing/`: invariants.py (267 lines), input_vector.py (155 lines), stage_assignment.py (138 lines), rosenstein_lyapunov.py (225 lines)
  - `scripts/`: preprocess_dataset.py (198 lines), prepare_training_data.py (258 lines)
- **Depends on:** numpy, scipy, h5py, sklearn (PCA), tqdm
- **Used by:** PINN training scripts (external, not yet in repo), command-line invocation
- **Key anomaly:** Both monolithic (`data-processing-pipeline-full.py`) and modular (`data-handling/`) versions exist. The monolithic file contains the same code inline as the modular package files. This represents a refactoring-in-progress.

### PINN Model Layer
- **Purpose:** Neural network architecture definition with physics-informed capabilities
- **Location:** `pinn/basic_architecture.py` (308 lines)
- **Contains:** PyTorch nn.Module implementations:
  - `SineLayer` (42 lines): SIREN activation layer with specialized weight initialization
  - `NN` (34 lines): DeepXDE-compatible base class with input/output transforms, auxiliary variables, regularizer
  - `SQRSkipResNetSIREN` (113 lines): Main architecture - 14-dim input, 256-neuron 12-layer ResNet, 9-dim output
- **Depends on:** PyTorch, numpy
- **Used by:** PINN training scripts (external), sanity-check invocation

### Documentation Layer
- **Purpose:** Research methodology, architecture specifications, pre-implementation reviews, paper templates
- **Location:** `pinn_instruction/`, `simulation_data/Documentation/`, `paper_templates/`
- **Contains:**
  - 5 modular LaTeX document sets with section-based structure (`main_*.tex` + `preamble.tex` + `sections/*.tex`)
  - Markdown conversions for reference (`pinn_instruction/markdown_conversion/framework-specs/` and `framework-revisions/`)
  - Research issues and pre-implementation audits (`pinn_instruction/original_latex/framework-revisions/review-of-framework/issues/`)
  - Dataset documentation and blacklists (`simulation_data/Documentation/`)
  - MDPI paper templates (`paper_templates/mdpi_template/`)
- **Depends on:** LaTeX toolchain (pdflatex/latexmk), pandoc (for markdown conversion)
- **Used by:** Researchers and developers for reference

## Data Flow

### Primary Simulation Path (Production Pipeline)

1. **IC Generation** (`simulation_data/Scripts/ic_generation/generate_ics.py` -> `ic_generation_utils.py`)
   - Generates two IC types: hierarchical (binary+outer, perturbed COM) and standard quasi-random (Sobol sampling, exact COM)
   - Writes 3-body IC files (7 fields per body: mass + 3D position + 3D velocity) to `simulation_data/Data/ic_final/`
   - Hierarchical: binary a~0.1-0.3, outer 3-10x separation, Gaussian perturbations sigma=0.01
   - Standard quasi-random: masses=1.0, Sobol sampling, global scaling factor 0.8-1.2

2. **Prescreening** (`simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py`)
   - Short leapfrog integration (TMAX=1.0, DT=0.0001) to detect unstable ICs
   - Rejects ICs exceeding ENERGY_ERROR_THRESHOLD=0.01 or below MIN_DISTANCE_THRESHOLD=0.01
   - Records processing index as JSON, writes blacklist

3. **Brutus Integration** (`simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py`)
   - Invokes `brutus` binary: `./brutus tol Lw t_begin t_end dt_out N file_in`
   - Hierarchical: tol=1e-15, Lw=130, dt_out=0.08
   - Standard quasi-random: tol=1e-13, Lw=118, dt_out=0.17
   - Timeout: 3000s per simulation
   - Validates output: final timestamp >= 9.5
   - Failed ICs moved to `Documentation/problematic_ics/`

4. **Gold Standard Re-simulation** (`simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py`)
   - Higher-fidelity re-runs of hierarchical ICs: tol=1e-13, Lw=130, dt_out=0.01
   - Standard quasi-random gold: tol=1e-13 or 1e-14, Lw=130, dt_out=0.01
   - 2,565 of 2,749 standard ICs selected for gold re-simulation
   - Output stored in `*_gold_standard/` folders

5. **Metrics Extraction** (`simulation_data/Scripts/metrics_calculation/calculate_metrics.py`)
   - Parses all Brutus output files (no completeness pre-filtering)
   - Calculates energy, momentum, and angular momentum conservation errors
   - Writes per-file JSON metrics to `simulation_data/Data/metrics/`

6. **PINN Data Preprocessing** (`pinn/data-processing-pipeline-full.py`)
   - Parses IC+Brutus file pairs, detects metadata from filenames
   - Computes global scaling constants across entire dataset
   - Scales to dimensionless units, applies canonical ordering
   - Computes physical invariants (E, Q, s_min, L_norm, I_norm, tau_L)
   - Computes 13-component normalized IC vectors
   - Assigns curriculum stages (0-6) based on invariants and dataset quantiles
   - Saves to HDF5

7. **Training Data Preparation** (`pinn/data-handling/scripts/prepare_training_data.py`)
   - Loads preprocessed HDF5
   - Time-samples trajectories (uniform, acceleration-weighted, or mixed)
   - Creates curriculum stage-based training batches with replay
   - Saves .npz and .pkl files per stage

### Secondary Data Quality Path

- **Dataset Readiness Checks** (`simulation_data/Validation/dataset_readiness_checks/`): 11-module suite validating completeness, correspondence, physics consistency, curriculum coverage, file format, metadata integrity, and more
- **Footer Audit** (`simulation_data/Scripts/debug/audit_and_backfill_brutus_result_footers.py`): Audits and backfills missing Brutus Result: footer lines
- **Completeness Checks** (`simulation_data/Scripts/debug/check_brutus_completeness.py`): Validates all output files have final timestamps >= 9.5

**State Management:**
- File-based: processing indices (JSON), blacklists (JSON), audit reports (Markdown)
- No in-memory caching between stages; each script is independently invocable
- Idempotent processing: scripts skip already-valid output files

## Key Abstractions

### Pipeline Stage Pattern
- **Purpose:** Each pipeline stage is an independently-invocable Python script with well-defined input/output directories
- **Examples:** `generate_ics.py`, `stage2_prescreening_revised_auto.py`, `run_brutus_both_type_simple.py`, `calculate_metrics.py`
- **Pattern:** Command-line script with hardcoded paths and configuration dictionaries, idempotent (skips existing valid outputs), writes status to stdout

### Brutus C++ Class Hierarchy
- **Purpose:** Encapsulate N-body integration with arbitrary precision
- **Classes:**
  - `Star`: Single body state (mass, position, velocity) with perturbation methods
  - `Cluster`: extends Star - N-body container, acceleration calculation, position/velocity updates
  - `Bulirsch_Stoer`: Richardson extrapolation ODE integrator with error control
  - `Brutus`: High-level orchestrator, manages time stepping and output
  - `Timer`: CPU time measurement utility
  - `Data_Handler`: File I/O formatting utilities
- **Located in:** `brutus_Newton-main/Brutus.h`, `Bulirsch_Stoer.h`, `Cluster.h`, `Star.h`

### Trajectory Data Classes
- **Purpose:** Typed containers for data flowing through the PINN preprocessing pipeline
- **Classes (from** `pinn/data-processing-pipeline-full.py` lines 28-144):
  - `SimulationMetadata`: Trajectory identification (type, fidelity, dt_out, set_name)
  - `RawTrajectoryData`: Parsed raw data from IC + Brutus files
  - `ScaledTrajectoryData`: Dimensionless scaled data with scaling factors
  - `PhysicalInvariants`: Computed physical quantities (E, Q, s_min, L_norm, I_norm, tau_L)
  - `ProcessedTrajectory`: Union of all above plus IC vector and curriculum stage
  - `GlobalScales`: Dataset-wide normalization constants
- **Pattern:** Immutable-like dataclasses with numpy arrays; pipeline transforms one type to the next

### SQRSkipResNetSIREN
- **Purpose:** Physics-informed neural network for 3-body trajectory prediction
- **File:** `pinn/basic_architecture.py` lines 80-193
- **Specs:** Input 14 dims (t + 13-component IC vector) -> 12 hidden layers of 256 neurons -> Output 9 dims (3D positions)
- **Architecture details:**
  - SIREN activation: sin(omega_0 * (Wx + b)), first_omega_0=30.0, hidden_omega_0=1.0
  - SQR-SkipResNet: odd layers have skip connection with power term p=2 after LayerNorm
  - LayerNorm: eps=1e-5, elementwise_affine=True, applied only to odd layers
  - Final linear layer with no activation, initialized to U(-0.01, 0.01)
- **Key methods:** forward() for standard pass, compute_derivatives() for physics loss (uses autograd for first and second time derivatives)

### Dataset Readiness Checker Plugin System
- **Purpose:** Extensible data validation across multiple quality dimensions
- **Location:** `simulation_data/Validation/dataset_readiness_checks/`
- **Modules (11):** blacklist, completeness, correspondence, coverage, curriculum, file_format, metadata, metrics, parameters, physics, temporal
- **Pattern:** Each module is a separate `.py` file in `modules/`; shared config in `config.py`; reports generated in JSON, Markdown, and CSV formats

### DeepXDE API Compatibility
- **Purpose:** Mirror DeepXDE neural network module patterns for future framework integration
- **File:** `pinn/basic_architecture.py` class NN, lines 44-77
- **Features:** input_transform, output_transform, auxiliary_vars, regularizer, num_trainable_parameters()
- **Note:** Compatibility layer only; actual DeepXDE integration is not yet implemented

## Entry Points

| Entry Point | Location | Type | Purpose | Invocation |
|-------------|----------|------|---------|------------|
| Brutus binary | `brutus_Newton-main/brutus` | C++ executable | N-body integration | `./brutus tol Lw t_begin t_end dt N file_in` |
| IC Generator | `simulation_data/Scripts/ic_generation/generate_ics.py` | Python script | Generate both IC types | `python generate_ics.py` |
| Prescreener | `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py` | Python script | Filter unstable ICs | `python stage2_prescreening_revised_auto.py` |
| Batch Runner | `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py` | Python script | Parallel Brutus execution | `python run_brutus_both_type_simple.py` |
| Gold Runner | `simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py` | Python script | Gold-standard hierarchical runs | `python run_brutus_hierarchical_only_mac_gold_standard.py` |
| Metrics Calculator | `simulation_data/Scripts/metrics_calculation/calculate_metrics.py` | Python script | Extract conservation metrics | `python calculate_metrics.py` |
| PINN Preprocessor | `pinn/data-processing-pipeline-full.py` | Python script | Full data preprocessing to HDF5 | `python data-processing-pipeline-full.py --ic_dir ... --brutus_dir ... --output ...` |
| PINN Training Prep | `pinn/data-handling/scripts/prepare_training_data.py` | Python script | Create stage-based training batches | `python prepare_training_data.py --input ... --output_dir ...` |
| PINN Architecture Test | `pinn/basic_architecture.py` | Python script | Architecture sanity check | `python basic_architecture.py` |
| Dataset Validator | `simulation_data/Validation/dataset_readiness_checks/__main__.py` | Python package | Run data validation suite | `python -m simulation_data.Validation.dataset_readiness_checks` |

## Architectural Constraints

- **Threading:** C++ Brutus is single-threaded. Python pipelines use ProcessPoolExecutor for parallel simulation (max_workers = cpu_count - 1). No threading within individual pipeline stages.
- **Global state:** No shared mutable state between pipeline stages. Each script is stateless aside from filesystem reads/writes.
- **Circular imports:** None detected. Pipeline is strictly unidirectional (Stage 1 -> 2 -> 3 -> 4 -> 5).
- **Memory:** Brutus output files can be large (high precision, many timesteps). Processing is file-at-a-time to bound memory.
- **Platform:** macOS-specific. Hardcoded `<home>/` paths in batch runner, metrics calculator, and Makefile.
- **Precision:** Brutus uses MPFR arbitrary precision (Lw=118-130 bits, ~35-39 decimal digits). Python uses float64 except when exact parsing requires string/Decimal.
- **Data locality:** All simulation data in `simulation_data/Data/` (committed to git via Git LFS or .gitignore). IC raw storage external to repo (set via `IC_RAW_DIR` env var).
- **Code duplication:** The `pinn/data-processing-pipeline-full.py` (1,650 lines) and `pinn/data-handling/` package (2,550 lines) contain duplicate code. The monolithic file has inline versions of the same modules found in the package. This is a refactoring-in-progress where both versions coexist.

## Error Handling

**Strategy:** Fail-soft with filesystem-based error tracking. Individual file failures do not halt batch processing.

**Patterns by layer:**

- **Brutus C++:** Returns non-zero exit codes on error. The Result: footer on stderr captures energy conservation metrics. Python wrapper catches subprocess.TimeoutExpired and subprocess.CalledProcessError.
- **Batch Runner:** Validates each output file after simulation. Failed ICs moved to `Documentation/problematic_ics/`. Partial output files deleted. Processing continues to next file.
- **IC Generation:** Configurable parameters with defaults. Errors bubble up as Python exceptions.
- **Metrics Calculator:** Processes every file regardless of completeness. Writes partial metrics for incomplete files. Logs errors per-file.
- **PINN Preprocessing:** Per-file try/except with tqdm progress. Malformed files logged with error message and skipped. Continues processing remaining files.
- **Dataset Readiness Checks:** Each module returns structured results with pass/fail and detailed messages. Aggregated into multiformat reports (JSON, Markdown, CSV).

## Cross-Cutting Concerns

**Logging:** Print statements to stdout with progress indicators (tqdm progress bars, status icons). No structured logging framework. Error messages written inline.

**Validation:** Four-layer validation strategy:
1. **Output completeness:** Final timestamp >= 9.5 (mandatory before use)
2. **Conservation metrics:** Energy, momentum, angular momentum drift
3. **Dataset readiness:** 11-module automated validation suite
4. **Footer audit:** Brutus Result: line presence and content validation

**Authentication:** None. Local research codebase.

**Configuration:** Hardcoded in script-level dictionaries and constants. Brutus parameters (tolerance, word length, dt_out) defined per-variant in runner scripts. No external config files (except dataset_readiness_checks/config.py).

**Build dependencies:** Homebrew-installed MPFR/GMP libraries. C++ compiled with g++. Python dependencies: numpy, scipy, torch, h5py, sklearn, tqdm.

## Anti-Patterns

### Hardcoded Absolute Paths

**What happens:** Multiple scripts contain hardcoded `<home>/Desktop/3_body_problem/` paths (e.g., `run_brutus_both_type_simple.py` line 32, `calculate_metrics.py` line 17).
**Why it's wrong:** Repository cannot be used on another machine or by another user without path edits.
**Do this instead:** Use `pathlib.Path(__file__).resolve().parent.parent` or environment variables for repo root discovery.

### Monolithic + Modular Duplication

**What happens:** `pinn/data-processing-pipeline-full.py` (1,650 lines) contains all pipeline logic inline as sequential code sections (`# FILE: core/data_structures.py`, `# FILE: core/parsing.py`, etc.). The same code also exists as separate files in `pinn/data-handling/`.
**Why it's wrong:** Two sources of truth for the same logic. Changes to one are not reflected in the other. Confusion about canonical implementation.
**Do this instead:** Delete the monolithic file or convert it to an orchestrator that imports from `data-handling/`. The monolithic version should be the canonical reference per CLAUDE.md.

### Inconsistent IC Generator File Names

**What happens:** CLAUDE.md references `generate_ics.py` and `ic_generation_utils.py`, but the previous architecture doc referenced `FINAL_ic_generator_enhanced.py` and `generate_enhanced_ics.py`. These enhanced files no longer exist.
**Why it's wrong:** Documentation rot. Stale references cause confusion about which scripts to run.
**Do this instead:** Keep CLAUDE.md as the source of truth (it was updated). The architecture document has been corrected in this version.

---

*Architecture analysis: 2026-04-27*
