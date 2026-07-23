# Three-Body Problem + CTL-PINN Training Stack

## Project Overview

This repository contains the complete simulation pipeline, metrics analysis, and Neural Network training stack for a three-body physics problem. The ultimate goal is to produce high-precision N-body simulation data (using the Brutus C++ integrator) and use Curriculum-Trained Physics-Informed Neural Networks (CTL-PINN) to learn and predict system dynamics.

## Migration Handoff

If you are opening this repository on the new Mac as part of the workstation migration, start with [`docs/runbooks/migration/exact-state-mac-migration.md`](docs/runbooks/migration/exact-state-mac-migration.md). It is the canonical restore runbook for recreating the old Mac's local repo state; the bulky simulation payloads are intentionally restored separately outside Git.

### Current Status Snapshot

When the bulky simulation payloads are restored (they are gitignored and copied in separately per the migration runbook), the repository holds massive datasets generated from two main sampling variants, which then go through integration and validation pipelines. On a fresh checkout or an isolated worktree, expect fixture-scale data only.

**Current Dataset Scale:**
- **Hierarchical Variant**: ~4,857 Initial Conditions (ICs) and their corresponding Brutus integration outputs, plus a "Gold Standard" high-precision subset (same 4,857 files, higher resolution).
- **Standard Quasi-Random Variant**: ~2,749 ICs and corresponding Brutus outputs, plus a "Gold Standard" subset of ~2,565 files (184 IDs excluded from gold re-simulation).

**Note:** Gold-standard Brutus outputs exist. Gold IC input folders have been removed (they were duplicates of the base IC folders).

**Milestone history:** The v2.0 CTL-PINN Training Viability Slice (trainex track) shipped 2026-07-23: it rebuilt the PINN training code under `pinn/` from the locked framework specs (FUT-01) and ran a Stage-0-first training slice end-to-end (42/42 requirements complete), but the held-out physics-conservation gate came back FAIL and the owner signed an **`adjust`** verdict. The active milestone, **v2.1 (Physics-Gate Investigation & trainex-r2 Research Package)**, diagnoses that failure and assembles a research package for the owner's external research — see [`.planning/ROADMAP.md`](.planning/ROADMAP.md) for the current phase plan. The Stage-0 training operator runbook from v2.0 remains at [`docs/runbooks/training/2026-07-18-stage0-training-operator-runbook.md`](docs/runbooks/training/2026-07-18-stage0-training-operator-runbook.md).

**Key Outputs**:
- Generating Sobol-based and Hierarchical Initial Conditions.
- Prescreening unstable ICs via short leapfrog integration.
- Full high-precision integrations using arbitrary-precision math.
- Deep metric profiling (energy conservation, momentum drift, phase space).

---

## Architecture & Repository Map

### Core Systems

- **`simulation_data/`**: The main data pipeline. Contains IC generation (`Scripts/ic_generation/`), Stage 2 prescreening (`Validation/prescreening/`), batch running scripts (`Scripts/brutus_runners/`), and metrics generation (`Scripts/metrics_calculation/`). Houses the massive generated datasets in `Data/ic_final/` and `Data/brutus_output/`.
- **`pinn/`**: Code for Physics-Informed Neural Networks. As of v2.0 (FUT-01), this holds the rebuilt training stack generated from the framework specs (`network.py`, `train.py`, `evaluate.py`, `loss_catalog.py`, `com_projection.py`, and the `data/` and `training/` packages); the v1.3-era monofiles (`basic_architecture.py`, `data-processing-pipeline-full.py`) remain as peers.
- **`brutus_Newton-main/`**: The C++ arbitrary-precision N-body integrator "Brutus" source code. This is the integration engine.

### Ancillary Systems

- **`pinn_instruction/`**: Markdown conversions and reference documents describing sampling methodology, CTL routines, and PINN architecture plans.
- **`paper_templates/`**: LaTeX templates for documentation or papers (under `mdpi_template/`).
- **`reference-code/`**: Reference Python implementations of N-body integrators, lyapunov analysis, and other baselines.
- **`tools/`**: Verification tooling, e.g. `spec-render-check/`, the framework-spec render detector suite added in v1.4 Phase 22.

---

## Prerequisites & Environment Setup

### 1. C++ Dependencies (For Brutus)
Brutus is a high-precision arbitrary math integrator. To build and run it, ensure you have:
- `g++` or another C++11 compliant compiler.
- `make` utility.
- [GMP (GNU Multiple Precision Arithmetic Library)](https://gmplib.org/)
- [MPFR (GNU Multiple Precision Floating-Point Reliable Library)](https://www.mpfr.org/)

To compile Brutus, run:
```bash
cd "$REPO_ROOT/brutus_Newton-main"
make clean
make
```

### 2. Python Dependencies
The data generation and PINN processing scripts are built with Python 3. Standard data-science and ML libraries are required. At a minimum, ensure you have installed:
```bash
pip install numpy pandas scipy h5py torch
```

*Note:* Use `python3` explicitly when executing pipeline scripts.

---

## Quickstart Runbook

The typical data pipeline flows from Stage 1 (Generation) to Stage 5 (PINN Pre-processing).

*(Note: Ensure `$REPO_ROOT` is exported and you run these from the root directory).*

**1. Generate Initial Conditions (Stage 1)**  
Generates raw `.txt` IC files into `$IC_RAW_DIR/ic_<variant>/`. Stage 2 prescreening later copies the passers into `simulation_data/Data/ic_final/`.
```bash
cd "$REPO_ROOT"
python3 simulation_data/Scripts/ic_generation/generate_ics.py
```

**2. Prescreen Unstable ICs (Stage 2)**  
Uses a fast leapfrog integration to filter out colliding/escaping systems early.
```bash
python3 simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py
```

**3. Run High-Precision Integration (Stage 3)**  
Feeds valid ICs into compiled Brutus. *(Warning: Make sure you compile Brutus first!)*
```bash
python3 simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py
```

*(For Gold Standard Hierarchical data only)*:
```bash
python3 simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py
```

**4. Calculate Run Metrics (Stage 4)**  
Evaluates output quality, calculating energy/momentum drift and collision flags.
```bash
python3 simulation_data/Scripts/metrics_calculation/calculate_metrics.py
```

**5. PINN Pre-processing (Stage 5)**  
Consolidates and normalizes outputs for NN training.
```bash
python3 pinn/data-processing-pipeline-full.py --input /path/to/preprocessed.h5 --output_dir /path/to/stage_data
```

---

## Dataset Layout and Naming Conventions

After the bulky payloads are restored, the datasets live inside the pipeline directory, split between `ic_final/` (inputs) and `brutus_output/` (outputs). The **folder name** rigidly defines the variant—files inside do *not* contain special text strings delineating "gold standard".

### Valid Output Folders (Inside `brutus_output/`)
- `brutus_hierarchical/`
- `brutus_hierarchical_gold_standard/`
- `brutus_standard_quasi_random/`
- `brutus_standard_quasi_random_gold_standard/`

**ID Mapping Rules:**
- Each file carries its variant prefix and a 4-digit zero-padded numeric ID (e.g., `ic_standard_0000.txt`, `brutus_hierarchical_0085.txt`).
- The numeric ID maps perfectly between the matching `ic_<variant>_<ID>.txt` and `brutus_<variant>_<ID>.txt` files.
- Gaps in ID sequencing are entirely normal and expected. They result from IC generation restarts, prescreen rejections, and occasional Brutus timeout failures (limit: 3000 sec).

**IC Folders (2 folders):**
- `ic_hierarchical/`
- `ic_standard_quasi_random/`

The `*_for_gold_standard` IC folders have been removed (they were duplicates). Gold-standard Brutus runs now read from the base IC folders.

---

## Data Quality and Readiness Checks

Due to integration complexity, a successful return code does not guarantee a scientifically valid result. Apply the following checks rigorously:

1. **Completeness Rule:** Ensure the final recorded timestep is `>= 9.5` before depending on a `brutus_output` file. Do not rely heavily on the file's footer note starting with `Result:`, as many valid outputs omit it.
2. **Metrics Audit:** Output folders are processed by the Stage 4 metrics scripts (`calculate_metrics.py` / `calculate_brutus_metrics.py`), which calculate metrics on structural integrity and accuracy. Any severe deviation should disqualify a run.
3. **Provenance Validation:** Check the Stage 2 processing-index JSON logs written under `simulation_data/Validation/prescreening/` for index mapping and logic trails, and `simulation_data/Documentation/problematic_ics_blacklist.json` (gitignored; present only after restore) for specific failed IDs.

---

## Script Status Matrix

| Entrypoint / Module                                   | Category       | Status          | Note                                                                                           |
|-------------------------------------------------------|----------------|-----------------|------------------------------------------------------------------------------------------------|
| `brutus` (C++ Makefile)                               | Integration    | Working         | Requires GMP/MPFR.                                                                             |
| `generate_ics.py`                            | Stage 1        | Config-driven   | Requires manual adjustment of target quantities limits before running.                         |
| `stage2_prescreening_revised_auto.py`                 | Stage 2        | Working         | Scans IC datasets directly.                                                                    |
| `run_brutus_both_type_simple.py`                      | Stage 3        | Working         | Typical timeout ~3000s per simulation instance.                                                |
| `calculate_metrics.py`                                | Stage 4        | Working         | Generates `.json` metric counterparts across outputs.                                          |
| **`dataset_readiness_checks` (Various scripts)**      | Validation     | **Unverified**  | The old `ValidationConfig` NameError etiology is stale — the class is defined in `config.py` and imported in `validator.py`. Other failure modes (missing restored data, gold filename-pattern mismatch) may remain; not re-run in the project env. |
| **`pinn/data-processing-pipeline-full.py`**           | Stage 5 / PINN | **Known-Broken**| Imports currently fail as structured; absolute path or `PYTHONPATH` fixes actively required.     |

---

## Known Limitations and Workarounds

Because this repository aggregates many rapidly evolving research scripts, expect some tooling inconsistencies.

- **`dataset_readiness_checks`:** The previously documented `NameError: name 'ValidationConfig' is not defined` no longer reflects the sources — `ValidationConfig` is defined in `config.py` and imported in `validator.py`. Treat these scripts as unverified rather than known-broken, and rely on the Stage 4 metrics scripts (`calculate_metrics.py` / `calculate_brutus_metrics.py`) until they are re-run in the project environment.
- **Naming Mismatches:** Inside legacy readiness check scripts, standard variant names are hardcoded with varying string literals that mismatch the actual folder schemas on disk (e.g. `brutus_standard_quasi_random`).
- **PINN Script Imports:** The legacy `pinn/data-processing-pipeline-full.py` monofile throws import errors due to internal `from core...` / `from processing...` cross-references. **Workaround:** add the repo root to the script's `sys.path` before importing. (The hyphenated filename is not a valid Python module name, so `python3 -m pinn.data-processing-pipeline-full` does **not** work.)
- **Missing "Gold Standard" Standard-Random Runner:** There is no exact runnable script to natively reproduce `brutus_standard_quasi_random_gold_standard/` outputs. These were generated partly from previous pipeline versions. Furthermore, naming documentation in older guides regarding what constitutes "gold" conflicts with the on-disk directory split.
- **Hierarchical Center of Mass (COM):** Hierarchical setups enforce a ~0 total momentum but perturb it by `sigma=0.01` noise immediately after. Consequently, COM runs slightly adrift. Re-center manually prior to running translationally-invariant networks.

---

## Further Reading

- [Dataset Specifications & Anomalies](simulation_data/Documentation/README.md)
- [Sampling Methodology Instruction](pinn_instruction/markdown_conversion/framework-specs/sampling_method.md)
- [CTL Curriculum Instruction](pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md)
- [PINN Architecture Plan](pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md)
- See `brutus_Newton-main/README.md` for Brutus usage arguments.
