<!-- refreshed: 2026-06-10 -->
# Architecture

**Analysis Date:** 2026-06-10

> **Governance note (read first).** This repo is a heavily-governed scientific
> spec-engineering project. The **authoritative** sources for PINN methodology,
> architecture, physics, and curriculum are the framework specs ONLY:
> `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`,
> `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`,
> `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`
> (frozen historical record). The live code in `pinn/`
> (`basic_architecture.py`, `data-processing-pipeline-full.py`,
> `data-handling/`) is **v1.3-era, pending FUT-01 rewrite, and is NOT
> spec-authoritative**. Where this document describes the model / AD contract /
> output head / curriculum, it is sourced from the framework specs; where the
> v1.3 code diverges from the specs, that is flagged as a known **code↔spec
> divergence** (the specs win). This document does not adjudicate any
> physics/spec question; unsettled items are reported as "tracked; see
> <artifact>" against `.planning/` and the framework specs only.

**Milestone context** (code analysis dated 2026-06-10; milestone status refreshed
2026-06-20): v1.4 ("Resolving 01 Architecture and Physics Foundations", Phases
16–22 incl. 20.5) shipped 2026-06-09 and constructed/repaired the framework specs.
v1.5 ("Resolving 02 Data Pipeline and Validation", Phases 23–29) **shipped
2026-06-17** (merged to `master`, archived under `.planning/milestones/v1.5-*`).
v1.6 ("Resolving 03 Curriculum and Training Loop", Phases 30–36) is **IN PROGRESS**
on branch `milestone/v1.6` (Phases 30–31 complete; Phase 32 next); it is
specwork-only and edits no runtime code. The architecture documented here reflects
the v1.4/v1.5 framework-spec state, with `pinn/` noted as the not-yet-rewritten
v1.3 code (FUT-01).

## System Overview

This codebase implements a complete three-body simulation and CTL-PINN
(Curriculum-Trained Physics-Informed Neural Network) training stack. It is a
**batch scientific computing system** with no servers, no APIs, and no
databases. All inter-component communication occurs through the filesystem
using text and HDF5 files. The system has two runtime personalities: a **C++
high-precision numerical integrator** invoked as a subprocess, and a **Python
pipeline** that orchestrates, validates, and processes data across 6 stages.

Alongside the runtime stack sits a large **spec-engineering / governance
subsystem** (`pinn_instruction/`, `.planning/`, `docs/`, `tools/`, `scripts/`,
`.githooks/`, `tests/`) where the framework specs, adjudication artifacts, and
GSD project management live. For the current milestones (v1.4 and v1.5 shipped,
v1.6 in progress) the spec-engineering subsystem — not the runtime code — is
where design work happens; `pinn/` is frozen v1.3 code awaiting FUT-01.

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

    subgraph "Stage 5: PINN Data Processing (v1.3 code, pending FUT-01)"
        E1[data-processing-pipeline-full.py<br/>monolithic, 1,650 lines]
        E1mod[data-handling/ modular refactor<br/>2,550 lines across 10 files]
        A3 --> E1
        C3 --> E1
        E1 --> E2[HDF5 preprocessed data]
        E2 --> E3[Stage-based training .npz + .pkl]
    end

    subgraph "Stage 6: PINN Training (design in specs; code is v1.3)"
        F1[basic_architecture.py]
        F2[SQR-SkipResNet-SIREN<br/>spec: 14-dim input -> 9-dim positions]
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
| PINN Data Pipeline (monolithic, **v1.3, pending FUT-01**) | Parse raw files, scale, compute invariants, assign stages, create training batches | `pinn/data-processing-pipeline-full.py` (1,650 lines) |
| PINN Data Pipeline (modular, **v1.3, pending FUT-01**) | Refactored modular version: core/, processing/, scripts/ subpackages | `pinn/data-handling/` (2,550 lines across 10 files) |
| PINN Architecture (**v1.3 code; design authority is the spec**) | SQR-SkipResNet-SIREN network; spec authority is `pinn_architecture.md` | `pinn/basic_architecture.py` (308 lines) |
| COM Transformation | Center-of-mass recentering for hierarchical ICs and Brutus outputs | `pinn/data-handling/core/com_transform_ic.py`, `com_transform_brutus.py` |
| **Framework Specs (AUTHORITATIVE)** | CTL methodology, PINN architecture/AD contract, IC sampling | `pinn_instruction/markdown_conversion/framework-specs/{ctl_instruction,pinn_architecture,sampling_method}.md` |
| Framework Revisions (research reports, non-authoritative) | Data-quality assessment, framework review, stage-strategy revision, per-issue research reports | `pinn_instruction/markdown_conversion/framework-revisions/` |
| LaTeX Source Specs | Modular LaTeX sources for the framework specs + revisions | `pinn_instruction/original_latex/framework-specs/`, `.../framework-revisions/` |
| Spec-Render Detector Tooling | Node detector that checks spec rendering / adjudication fixtures (v1.4 acceptance tooling) | `tools/spec-render-check/detect.mjs` |
| Git-Policy Guard Tooling | Commit-message / staged-path validation enforced by `.githooks/` and `scripts/agent-commit` | `scripts/git_policy/`, `.githooks/`, `tests/git_policy/` |
| GSD Project Management | Phase-based plan tracking, milestones, gap registers, adjudication records | `.planning/` (milestones, phases, research/edl, codebase, reports, forensics) |

## Pattern Overview

**Overall:** Filesystem-based Pipeline Architecture (runtime) wrapped by a
GSD (Goal-Structured Development) spec-engineering and governance subsystem.

**Key Characteristics:**
- **Linear pipeline with modular stages**: Each stage reads from and writes to the filesystem with zero runtime coupling to upstream/downstream stages
- **C++ subprocess invocation**: The Brutus binary is compiled separately and invoked via `subprocess.run()` with CLI arguments; Python wrappers handle timeout, validation, and output management
- **File-based data interchange**: IC files (*.txt) -> Brutus output (*.txt) -> Metrics (*.json) -> Preprocessed data (*.h5) -> Training batches (*.npz, *.pkl)
- **Folder-defines-variant pattern**: "Gold" vs "standard" data quality is encoded in directory names, not file names. The same file naming convention is used across all variant folders
- **Dataclass-based data structures**: Python `@dataclass` classes (RawTrajectoryData, ScaledTrajectoryData, PhysicalInvariants, ProcessedTrajectory) form a type-safe pipeline chain (in the **v1.3** PINN code)
- **Plug-in validation modules**: The dataset readiness checker uses an 11-module plugin pattern with shared configuration
- **Spec-as-source-of-truth**: Network/curriculum/physics design lives in the markdown framework specs; code is generated from specs (FUT-01), never the reverse. Live code is explicitly barred as a grounding source for spec decisions.
- **Curriculum learning stages**: Curriculum staging is defined authoritatively in `ctl_instruction.md`. (The v1.3 code's 7-stage 0–6 quantile assignment is an implementation that must be reconciled against the spec in FUT-01; treat the spec as authority.)
- **DeepXDE API compatibility**: The v1.3 PINN model inherits from an NN base class that mirrors DeepXDE transform patterns (code-level only).

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
- **SCOPE note:** `simulation_data/Scripts/ic_generation/` is a permitted grounding source for `sampling_method.md` (SCOPE-05 carveout); the on-disk `simulation_data/` dataset and its generation scripts are v1.5 grounding sources (SCOPE-06/07).

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

### PINN Data Processing Layer (v1.3 code, pending FUT-01 rewrite)
- **Purpose:** Parse raw simulation data, normalize to dimensionless units, compute physical invariants, assign curriculum learning stages, prepare training batches
- **Status:** **v1.3-era, NOT spec-authoritative.** Slated for FUT-01 rewrite from the framework specs. May be described as the existing implementation, but design questions are answered by the specs, not this code.
- **Location:** `pinn/data-processing-pipeline-full.py` (monolithic 1,650-line script), `pinn/data-handling/` (modular refactor: core/, processing/, scripts/)
- **Contains:**
  - `core/`: data_structures.py (123 lines), parsing.py (699 lines), scaling.py (241 lines), com_transform_*.py
  - `processing/`: invariants.py (267 lines), input_vector.py (155 lines), stage_assignment.py (138 lines), rosenstein_lyapunov.py (225 lines)
  - `scripts/`: preprocess_dataset.py (198 lines), prepare_training_data.py (258 lines)
- **Depends on:** numpy, scipy, h5py, sklearn (PCA), tqdm
- **Used by:** PINN training scripts (external, not yet in repo), command-line invocation
- **Known divergence:** Both monolithic (`data-processing-pipeline-full.py`) and modular (`data-handling/`) versions exist with duplicated code (refactoring-in-progress). Both are v1.3; both must be reconciled against the specs in FUT-01.

### PINN Model Layer (design authority = framework spec)
- **Purpose:** Physics-informed neural-network architecture for 3-body trajectory prediction.
- **Authoritative spec:** `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (revised/repaired during v1.4).
- **Spec contract (sourced from `pinn_architecture.md`):**
  - **Input Vector:** a 14-dimensional vector `[τ, IC_13]`, where `u = t/T` is the autograd leaf and `τ = 2u − 1` is the bounded network-time coordinate; `IC_13` is the ordered **Jacobi-state** initial-condition vector defined canonically in `ctl_instruction.md` Step 4 (`pinn_architecture.md` §5.2, lines ~753, ~930).
  - **Output head:** 9 projected position components (three bodies × 3D positions), linear (no) output activation; velocities/accelerations are AD-derived, not separate outputs (`pinn_architecture.md` lines ~266, ~866).
  - **AD contract:** physics loss uses autograd derivatives of position w.r.t. the time leaf `u`; an explicit per-component loop over the 9 outputs is specified (`pinn_architecture.md` §~866–891).
  - **Architecture family:** hybrid SQR-SkipResNet-SIREN with soft conservation regularization (spec title; SIREN sine activations, power-enhanced residual/skip terms).
- **Live code (v1.3, NOT authoritative):** `pinn/basic_architecture.py` (308 lines) implements `SineLayer`, a DeepXDE-style `NN` base class, and `SQRSkipResNetSIREN` (14→256×12→9). The 14→9 shape matches the spec contract, but the bounded `τ = 2u − 1` network-time coordinate and the Jacobi-state `IC_13` ordering are **v1.4 spec contracts** — verify against `pinn_architecture.md` / `ctl_instruction.md` rather than against this file. Any difference is a code↔spec divergence to be resolved in FUT-01.

### Spec-Engineering & Documentation Layer
- **Purpose:** Authoritative framework specs, research/revision reports, issue adjudication, and project methodology.
- **Location & structure:**
  - `pinn_instruction/markdown_conversion/framework-specs/` — **AUTHORITATIVE** markdown specs (`ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`).
  - `pinn_instruction/markdown_conversion/framework-revisions/` — research reports (non-authoritative): `data_quality_assessment.md`, `review-of-framework/`, `stage-strat-revision/`, and `research_reports/01-architecture-and-physics-foundations/` (the v1.4 resolution doc `ctl_pinn_resolution.md` plus external research reports).
  - `pinn_instruction/original_latex/framework-specs/` and `.../framework-revisions/` — modular LaTeX sources for the above (kebab-case doc dirs: `ctl-instruction/`, `pinn-architecture/`, `sampling-method/`, `data-quality-assessment/`, `review-of-framework/`).
  - `pinn_instruction/issues/` — consolidated thematic issue docs (`01-…`, `02-…`, `03-…`) + `MIGRATION.md`, `README.md`, `archive/`. Issue `02-data-pipeline-and-validation.md` was the (non-authoritative) target of v1.5; issue `03-curriculum-and-training-loop.md` is the (non-authoritative) target of v1.6.
- **Depends on:** LaTeX toolchain (LaTeX sources), pandoc (markdown conversion), Node (`tools/spec-render-check`).
- **Used by:** GSD planning/adjudication; FUT-01 will generate code from the specs.

### Governance / Tooling Layer
- **Purpose:** Enforce commit policy, spec-render checks, and migration runbooks.
- **Location:** `scripts/` (`agent-commit`, `setup-git-hooks.sh`, `git_policy/`), `.githooks/` (commit-msg, pre-commit, pre-push, post-*, pre-rebase), `tools/spec-render-check/` (Node detector + `adjudications/` fixtures), `tests/` (`test_phase12_validation.py`, `git_policy/`), `docs/` (`git-guidelines.md`, `README.md`, `runbooks/migration/`, `runbooks/EDL/`).
- **Used by:** Agents and CI; `scripts/agent-commit` is the mandated commit path (raw `git commit` is disallowed for agents).

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

6. **PINN Data Preprocessing** (`pinn/data-processing-pipeline-full.py` — **v1.3 code**)
   - Parses IC+Brutus file pairs, detects metadata from filenames
   - Computes global scaling constants across entire dataset
   - Scales to dimensionless units, applies canonical ordering
   - Computes physical invariants (E, Q, s_min, L_norm, I_norm, tau_L)
   - Computes normalized IC vectors and assigns curriculum stages
   - Saves to HDF5
   - **Note:** the exact invariant set, IC-vector formulation, and stage-assignment logic are governed by the framework specs (`ctl_instruction.md`); the v1.3 implementation must be reconciled to those specs in FUT-01.

7. **Training Data Preparation** (`pinn/data-handling/scripts/prepare_training_data.py` — **v1.3 code**)
   - Loads preprocessed HDF5
   - Time-samples trajectories (uniform, acceleration-weighted, or mixed)
   - Creates curriculum stage-based training batches with replay
   - Saves .npz and .pkl files per stage

### Secondary Data Quality Path

- **Dataset Readiness Checks** (`simulation_data/Validation/dataset_readiness_checks/`): 11-module suite validating completeness, correspondence, physics consistency, curriculum coverage, file format, metadata integrity, and more
- **Footer Audit** (`simulation_data/Scripts/debug/audit_and_backfill_brutus_result_footers.py`): Audits and backfills missing Brutus `Result:` footer lines
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

### Trajectory Data Classes (v1.3 code)
- **Purpose:** Typed containers for data flowing through the v1.3 PINN preprocessing pipeline
- **Classes (from** `pinn/data-processing-pipeline-full.py` lines 28-144):
  - `SimulationMetadata`, `RawTrajectoryData`, `ScaledTrajectoryData`, `PhysicalInvariants`, `ProcessedTrajectory`, `GlobalScales`
- **Pattern:** Immutable-like dataclasses with numpy arrays; pipeline transforms one type to the next. (Implementation detail of the v1.3 code; not a spec contract.)

### Network Input/Output Contract (framework spec — AUTHORITATIVE)
- **Source:** `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` §5.2 + summary table; `ctl_instruction.md` Step 4.
- **Input:** 14-dim `[τ, IC_13]`; `u = t/T` is the autograd leaf, `τ = 2u − 1` bounded network time; `IC_13` is the ordered Jacobi-state IC vector.
- **Output:** 9 position components (3 bodies × 3D), linear output activation; velocities/accelerations via AD.
- **Architecture family:** hybrid SQR-SkipResNet-SIREN with soft conservation regularization.
- **Note:** This is the design authority. The v1.3 `SQRSkipResNetSIREN` in `pinn/basic_architecture.py` is an existing implementation, not the contract.

### Dataset Readiness Checker Plugin System
- **Purpose:** Extensible data validation across multiple quality dimensions
- **Location:** `simulation_data/Validation/dataset_readiness_checks/`
- **Modules (11):** blacklist, completeness, correspondence, coverage, curriculum, file_format, metadata, metrics, parameters, physics, temporal
- **Pattern:** Each module is a separate `.py` file in `modules/`; shared config in `config.py`; reports generated in JSON, Markdown, and CSV formats

### GSD Adjudication & Gap-Register Pattern
- **Purpose:** Block on source-silent spec decisions rather than inventing content (governance STOP protocol).
- **Artifacts:** phase-local gap registers `.planning/phases/NN-*/NN-GAPS.md`; milestone gap indexes `.planning/milestones/v1.4-GAPS.md` and `v1.5-GAPS.md` (and `v1.6-GAPS.md`, created on the first v1.6 gap); EDL research-support briefs `.planning/research/edl/`; spec-render adjudication fixtures `tools/spec-render-check/adjudications/`.
- **Pattern:** A decision is "grounded" only if explicitly answered by a designated source (resolution doc, issue doc, prior user decision, planning artifact, or a v1.4-revised spec section). Otherwise STOP and surface. See `AGENTS.md` "CRITICAL GOVERNANCE" for the full test.

## Entry Points

| Entry Point | Location | Type | Purpose | Invocation |
|-------------|----------|------|---------|------------|
| Brutus binary | `brutus_Newton-main/brutus` | C++ executable | N-body integration | `./brutus tol Lw t_begin t_end dt N file_in` |
| IC Generator | `simulation_data/Scripts/ic_generation/generate_ics.py` | Python script | Generate both IC types | `python generate_ics.py` |
| Prescreener | `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py` | Python script | Filter unstable ICs | `python stage2_prescreening_revised_auto.py` |
| Batch Runner | `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py` | Python script | Parallel Brutus execution | `python run_brutus_both_type_simple.py` |
| Gold Runner | `simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py` | Python script | Gold-standard hierarchical runs | `python run_brutus_hierarchical_only_mac_gold_standard.py` |
| Metrics Calculator | `simulation_data/Scripts/metrics_calculation/calculate_metrics.py` | Python script | Extract conservation metrics | `python calculate_metrics.py` |
| PINN Preprocessor (v1.3) | `pinn/data-processing-pipeline-full.py` | Python script | Full data preprocessing to HDF5 | `python data-processing-pipeline-full.py --ic_dir ... --brutus_dir ... --output ...` |
| PINN Training Prep (v1.3) | `pinn/data-handling/scripts/prepare_training_data.py` | Python script | Create stage-based training batches | `python prepare_training_data.py --input ... --output_dir ...` |
| PINN Architecture Test (v1.3) | `pinn/basic_architecture.py` | Python script | Architecture sanity check | `python basic_architecture.py` |
| Dataset Validator | `simulation_data/Validation/dataset_readiness_checks/__main__.py` | Python package | Run data validation suite | `python -m simulation_data.Validation.dataset_readiness_checks` |
| Spec-Render Detector | `tools/spec-render-check/detect.mjs` | Node script | Spec-render / adjudication checks | `node tools/spec-render-check/detect.mjs` |
| Agent Commit | `scripts/agent-commit` | Shell script | Mandated commit path for agents (hooks enforced) | `scripts/agent-commit ...` |
| Git-Policy / Phase Tests | `tests/test_phase12_validation.py`, `tests/git_policy/test_git_policy.py` | Pytest | Validate phase artifacts and git policy | `pytest tests/` |

## Architectural Constraints

- **Threading:** C++ Brutus is single-threaded. Python pipelines use ProcessPoolExecutor for parallel simulation (max_workers = cpu_count - 1). No threading within individual pipeline stages.
- **Global state:** No shared mutable state between pipeline stages. Each script is stateless aside from filesystem reads/writes.
- **Circular imports:** None detected. Pipeline is strictly unidirectional (Stage 1 -> 2 -> 3 -> 4 -> 5).
- **Memory:** Brutus output files can be large (high precision, many timesteps). Processing is file-at-a-time to bound memory.
- **Platform:** macOS-specific. Hardcoded `<home>/` paths in batch runner, metrics calculator, and Makefile.
- **Precision:** Brutus uses MPFR arbitrary precision (Lw=118-130 bits, ~35-39 decimal digits). Python uses float64 except when exact parsing requires string/Decimal.
- **Data locality:** All simulation data in `simulation_data/Data/`. IC raw storage external to repo (set via `IC_RAW_DIR` env var).
- **Code duplication:** The `pinn/data-processing-pipeline-full.py` (1,650 lines) and `pinn/data-handling/` package (2,550 lines) contain duplicate code (refactoring-in-progress, both v1.3).
- **Spec-engineering constraint (governance):** Live code in `pinn/` is **not** a grounding source for any spec/physics decision. Spec edits in the active milestones are restricted to `ctl_instruction.md` and `pinn_architecture.md`; `sampling_method.md` is frozen by default; `data_quality_assessment.md` is read-only research material. Source-silent semantic decisions must STOP and surface per `AGENTS.md`.
- **Commit constraint:** Agents must use `scripts/agent-commit`; `.githooks/` enforce commit-message and staged-path policy; `--no-verify` / hook bypass requires explicit user approval.

## Error Handling

**Strategy:** Fail-soft with filesystem-based error tracking. Individual file failures do not halt batch processing.

**Patterns by layer:**

- **Brutus C++:** Returns non-zero exit codes on error. The `Result:` footer on stderr captures energy conservation metrics. Python wrapper catches subprocess.TimeoutExpired and subprocess.CalledProcessError.
- **Batch Runner:** Validates each output file after simulation. Failed ICs moved to `Documentation/problematic_ics/`. Partial output files deleted. Processing continues to next file.
- **IC Generation:** Configurable parameters with defaults. Errors bubble up as Python exceptions.
- **Metrics Calculator:** Processes every file regardless of completeness. Writes partial metrics for incomplete files. Logs errors per-file.
- **PINN Preprocessing (v1.3):** Per-file try/except with tqdm progress. Malformed files logged and skipped. Continues processing remaining files.
- **Dataset Readiness Checks:** Each module returns structured results with pass/fail and detailed messages. Aggregated into multiformat reports (JSON, Markdown, CSV).
- **Governance / spec work:** "Fail-loud-and-stop" — on a source-silent semantic decision, the agent halts and records a gap rather than inventing content.

## Cross-Cutting Concerns

**Logging:** Print statements to stdout with progress indicators (tqdm progress bars, status icons). No structured logging framework. Error messages written inline.

**Validation:** Four-layer runtime validation strategy:
1. **Output completeness:** Final timestamp >= 9.5 (mandatory before use)
2. **Conservation metrics:** Energy, momentum, angular momentum drift
3. **Dataset readiness:** 11-module automated validation suite
4. **Footer audit:** Brutus `Result:` line presence and content validation

Plus a governance validation layer: spec-render checks (`tools/spec-render-check`), git-policy guards (`scripts/git_policy/`, `.githooks/`), and phase-artifact tests (`tests/`).

**Authentication:** None. Local research codebase.

**Configuration:** Hardcoded in script-level dictionaries and constants. Brutus parameters per-variant in runner scripts. No external config files (except `dataset_readiness_checks/config.py` and `.planning/config.json`).

**Build dependencies:** Homebrew-installed MPFR/GMP libraries. C++ compiled with g++. Python dependencies: numpy, scipy, torch, h5py, sklearn, tqdm. Node (for `tools/spec-render-check`).

## Anti-Patterns

### Hardcoded Absolute Paths

**What happens:** Multiple scripts contain hardcoded `<home>/Desktop/3_body_problem/` paths (e.g., `run_brutus_both_type_simple.py`, `calculate_metrics.py`).
**Why it's wrong:** Repository cannot be used on another machine or by another user without path edits.
**Do this instead:** Use `pathlib.Path(__file__).resolve().parent.parent` or environment variables for repo root discovery.

### Monolithic + Modular Duplication (v1.3 code)

**What happens:** `pinn/data-processing-pipeline-full.py` (1,650 lines) contains all pipeline logic inline; the same code also exists as separate files in `pinn/data-handling/`.
**Why it's wrong:** Two sources of truth for the same logic in the v1.3 code.
**Do this instead:** Do not extend either; both are superseded by the FUT-01 rewrite generated from the framework specs. Do not treat either as the design contract.

### Treating Live Code as Spec Authority

**What happens:** A reader infers the "intended" network architecture, IC vector, curriculum, or physics from `pinn/basic_architecture.py` or `pinn/data-processing-pipeline-full.py`.
**Why it's wrong:** That code is v1.3-era and explicitly barred as a grounding source; the v1.4 specs may differ (e.g., bounded `τ = 2u − 1` network time, Jacobi-state IC ordering).
**Do this instead:** Read the design from `pinn_instruction/markdown_conversion/framework-specs/`. Treat code/spec differences as code↔spec divergences to resolve in FUT-01; do not silently adopt the code's version.

---

*Architecture analysis: 2026-06-10*
