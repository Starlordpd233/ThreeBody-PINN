# Codebase Structure

**Analysis Date:** 2026-04-27

## Directory Layout

```
3_body_problem/                                 # Repository root
├── .claude/                                     # Claude Code agent config (skills, instructions)
│   └── skills/                                  # Project-specific skill definitions
├── .github/                                     # GitHub workflows and custom slash commands
│   ├── commands/                                # Custom slash command definitions
│   └── workflows/                               # CI/CD workflow YAML files
├── .planning/                                   # GSD project management (detailed below)
├── .tmp/                                        # Temporary files (not committed)
├── .venv/                                       # Python virtual environment (not committed)
│
├── brutus_Newton-main/                          # C++ high-precision N-body integrator
│   ├── main.cpp                                 # CLI entry point (331 lines)
│   ├── Brutus.{cpp,h}                           # Integrator orchestrator class
│   ├── Bulirsch_Stoer.{cpp,h}                   # Richardson extrapolation ODE integrator
│   ├── Cluster.{cpp,h}                          # N-body cluster container (extends Star)
│   ├── Star.{cpp,h}                             # Single body state representation
│   ├── test_libs.cpp                            # Test driver for libraries
│   ├── lib/                                     # Utility libraries
│   │   ├── Timer/                               # CPU timing (Timer.cpp, Timer.h)
│   │   └── Data_Handler/                        # File I/O formatting (Data_Handler.cpp, Data_Handler.h, test.cpp)
│   ├── mplib/                                   # Multi-precision library support
│   │   └── Data_Handler/                        # MP-aware Data_Handler variant (copied)
│   ├── input/                                   # Test input files and IC generator
│   │   ├── generate_ics.csh                     # TCShell IC generation script
│   │   ├── uniform_density_distribution.py      # Python uniform density IC generator
│   │   └── NBodyN{8,16,32,64,128,256,512,1024,2048}.Q05.IMF2_scaled.in  # N-body test inputs
│   ├── img/                                     # Documentation images
│   │   └── Brutus.jpg                           # Brutus logo
│   ├── makefile                                 # Build configuration (macOS M2 hardcoded paths)
│   ├── makefile.original                        # Original unmodified makefile backup
│   ├── brutus                                   # Compiled binary (build artifact)
│   ├── README.md                                # Brutus-specific documentation
│   ├── README_brutus.md                         # Additional Brutus documentation
│   └── LICENSE                                  # Software license
│
├── simulation_data/                             # Python pipeline + all simulation data
│   ├── Scripts/                                 # Active Python pipeline scripts
│   │   ├── ic_generation/                       # Stage 1: IC creation
│   │   │   ├── generate_ics.py                  # Entry point: generates both IC types
│   │   │   └── ic_generation_utils.py           # Core: Sobol sampling, hierarchical generation
│   │   ├── brutus_runners/                      # Stage 3: Batch Brutus simulation
│   │   │   ├── run_brutus_both_type_simple.py   # Main batch runner (hierarchical + standard)
│   │   │   └── run_brutus_hierarchical_only_mac_gold_standard.py  # Gold-standard hierarchical
│   │   ├── metrics_calculation/                 # Stage 4: Conservation metrics
│   │   │   ├── calculate_metrics.py             # Main metrics extractor (energy, momentum, AM)
│   │   │   └── calculate_brutus_metrics.py      # Alternative metrics calculator
│   │   ├── debug/                               # Debug and audit utilities
│   │   │   ├── audit_and_backfill_brutus_result_footers.py  # Footer audit/backfill
│   │   │   ├── check_brutus_completeness.py     # Completeness check utility
│   │   │   ├── compare_folders.py               # Directory comparison tool
│   │   │   ├── compare_ic_brutus_files.py       # IC-to-Brutus file matcher
│   │   │   └── renaming/                        # File renaming scripts (4 scripts)
│   │   └── archived/                            # Deprecated/archived scripts (3 files)
│   │       ├── analyze_metrics_not_sure_if_using.py
│   │       ├── manage_problematic_ics_notusing.py
│   │       └── visualize_test_brutus.py
│   │
│   ├── Validation/                              # Quality assurance and prescreening
│   │   ├── __init__.py                          # Package marker
│   │   ├── prescreening/                        # Stage 2: IC stability filtering
│   │   │   ├── stage2_prescreening_revised_auto.py  # Main prescreener (leapfrog short-run)
│   │   │   ├── prescreening_utils.py            # Prescreening helper functions
│   │   │   ├── prescreening_data/               # Prescreening run results (JSON indices)
│   │   │   └── utilities/                       # Prescreening tooling (threshold comparison, index migration)
│   │   ├── analysis/                            # Analysis and visualization scripts
│   │   │   ├── metrics_analysis.py              # Metrics statistical analysis
│   │   │   ├── particle_positions_viz.py        # Position visualization
│   │   │   ├── reference_plane_viz.py           # Reference plane analysis
│   │   │   ├── utils.py                         # Shared analysis utilities
│   │   │   ├── prescreening_analysis/           # Prescreening results analysis (5 scripts)
│   │   │   └── figures/                         # Generated figures (PNG)
│   │   │       ├── hierarchical_positions/
│   │   │       ├── metrics_analysis/
│   │   │       ├── prescreening/
│   │   │       │   ├── property_correlations/
│   │   │       │   └── property_distributions/
│   │   │       ├── prescreening_copy_archive/
│   │   │       └── reference_plane/
│   │   ├── audit_reports/                       # Data quality audit reports (Markdown)
│   │   │   ├── check_missing_results.py         # Missing output checker
│   │   │   └── check_missing_results_detailed.py  # Detailed audit version
│   │   └── dataset_readiness_checks/            # Pre-training data validation suite
│   │       ├── __init__.py                      # Package marker
│   │       ├── __main__.py                      # Entry point for `python -m` invocation
│   │       ├── config.py                        # Shared configuration
│   │       ├── datastructures.py                # Core data structures
│   │       ├── validator.py                     # Main validator orchestrator
│   │       ├── audit_naming.py                  # Naming consistency audit
│   │       ├── modules/                         # Validation modules (11 files)
│   │       │   ├── __init__.py
│   │       │   ├── blacklist.py                 # Blacklist validation
│   │       │   ├── completeness.py              # Output completeness checks
│   │       │   ├── correspondence.py            # IC-to-output mapping
│   │       │   ├── coverage.py                  # Dataset coverage analysis
│   │       │   ├── curriculum.py                # Curriculum stage validation
│   │       │   ├── file_format.py               # File format validation
│   │       │   ├── metadata.py                  # Metadata consistency
│   │       │   ├── metrics.py                   # Metrics validation
│   │       │   ├── parameters.py                # Parameter validation
│   │       │   ├── physics.py                   # Physics consistency checks
│   │       │   └── temporal.py                  # Temporal validation
│   │       ├── reports/                         # Generated reports
│   │       │   ├── csv/
│   │       │   ├── json/
│   │       │   └── markdown/
│   │       └── utils/                           # Shared utilities
│   │           ├── __init__.py
│   │           ├── logging.py
│   │           ├── naming.py
│   │           ├── parsers.py
│   │           └── physics_core.py
│   │
│   ├── Data/                                    # All simulation data (input + output)
│   │   ├── ic_final/                            # Final validated initial conditions
│   │   │   ├── ic_hierarchical/                 # 4,857 IC files (binary+outer, perturbed COM)
│   │   │   └── ic_standard_quasi_random/        # 2,749 IC files (Sobol, exact COM)
│   │   ├── brutus_output/                       # Brutus simulation trajectory outputs
│   │   │   ├── brutus_hierarchical/             # 4,857 files (tol=1e-15, Lw=130, dt=0.08)
│   │   │   ├── brutus_hierarchical_gold_standard/   # 4,857 files (tol=1e-13, Lw=130, dt=0.01)
│   │   │   ├── brutus_standard_quasi_random/    # 2,749 files (tol=1e-13, Lw=118, dt=0.17)
│   │   │   └── brutus_standard_quasi_random_gold_standard/  # 2,565 files (tol=1e-13, Lw=130, dt=0.01)
│   │   ├── metrics/                             # Computed conservation metrics
│   │   │   ├── sim_result_metric_hierarchical/   # ~4,857 JSON files
│   │   │   ├── sim_result_metric_hierarchical_gold_standard/  # ~4,857 JSON files
│   │   │   ├── sim_result_metric_standard/       # ~2,749 JSON files
│   │   │   └── sim_result_metric_standard_gold_standard/      # ~2,565 JSON files
│   │   └── testing_data/                        # Small test datasets for development
│   │       ├── brutus_output/
│   │       └── ic_final/
│   │           ├── ic_hierarchical/
│   │           ├── ic_standard_quasi_random/
│   │           └── ic_raw/
│   │               ├── ic_hierarchical/
│   │               └── ic_standard_quasi_random/
│   │
│   └── Documentation/                           # Dataset documentation
│       ├── README.md                            # Main dataset documentation (source of truth)
│       ├── problematic_ics_blacklist.json       # JSON blacklist of rejected ICs
│       ├── standard_quasi_random_ids_not_in_gold.md  # List of 184 IDs not in gold subset
│       └── problematic_ics/                     # Moved problematic IC files (backups)
│           ├── hierarchical/
│           ├── hierarchical_for_gold_standard/
│           └── standard/
│
├── pinn/                                        # CTL-PINN system (Physics-Informed Neural Network)
│   ├── basic_architecture.py                    # SQR-SkipResNet-SIREN model definition (308 lines)
│   ├── data-processing-pipeline-full.py          # Monolithic data pipeline (1,650 lines)
│   └── data-handling/                           # Modular pipeline refactor (10 Python files, 2,550 lines)
│       ├── __init__.py
│       ├── core/                                # Core data processing
│       │   ├── __init__.py
│       │   ├── data_structures.py               # Dataclass type definitions (123 lines)
│       │   ├── parsing.py                       # IC and Brutus file parsers (699 lines)
│       │   ├── scaling.py                       # Dimensionless scaling (241 lines)
│       │   ├── com_transform_ic.py              # COM recentering for ICs (143 lines)
│       │   ├── com_transform_brutus.py          # COM recentering for Brutus outputs (103 lines)
│       │   ├── parsing.txt                      # Parsing notes/errata (13 lines)
│       │   └── preprocessed-data/               # Preprocessed HDF5 sample files
│       │       └── parsed-data/
│       │           ├── brutus/brutus_hierarchical/  # 3 sample .h5 files
│       │           ├── ic/ic_hierarchical/          # 3 sample .h5 files
│       │           └── parsing_stats.json
│       ├── processing/                          # Physical quantity computation
│       │   ├── __init__.py
│       │   ├── invariants.py                    # E, Q, s_min, L_norm, I_norm computation (267 lines)
│       │   ├── input_vector.py                  # 13-component IC vector formulation (155 lines)
│       │   ├── stage_assignment.py              # Curriculum stage assignment (138 lines)
│       │   └── rosenstein_lyapunov.py           # Lyapunov exponent estimation (225 lines)
│       └── scripts/                             # Entry point scripts
│           ├── __init__.py
│           ├── preprocess_dataset.py            # Raw-to-HDF5 preprocessing (198 lines)
│           └── prepare_training_data.py         # HDF5-to-training-batches (258 lines)
│
├── pinn_instruction/                            # Research methodology documentation
│   ├── original_latex/                          # LaTeX source documents (5 document sets)
│   │   ├── ctl-instruction/                     # CTL methodology instruction
│   │   │   ├── main_CTL.tex                     # Main document
│   │   │   ├── preamble_CTL.tex                 # LaTeX preamble
│   │   │   ├── main_CTL.pdf                     # Compiled PDF
│   │   │   └── sections/                        # 7 content sections + appendix
│   │   ├── Data-quality-assessment/             # Data quality assessment methodology
│   │   │   ├── main-data-quality-assess.tex
│   │   │   ├── preamble.tex
│   │   │   ├── main-data-quality-assess.pdf
│   │   │   └── sections/                        # 7 content sections
│   │   ├── pinn-architecture/                   # PINN architecture design document
│   │   │   ├── main_pinn.tex
│   │   │   ├── preamble.tex
│   │   │   ├── main_pinn.pdf
│   │   │   └── sections/                        # 9 sections (3 marked inactive)
│   │   ├── review-of-framework/                 # CTL-PINN framework review (2 sub-documents)
│   │   │   ├── review_of_framework/
│   │   │   │   ├── review_of_framework.tex
│   │   │   │   ├── preamble.tex
│   │   │   │   ├── review_of_framework.pdf
│   │   │   │   └── sections/                    # 7 content sections
│   │   │   ├── stage_strat_revision/
│   │   │   │   ├── stage_strat_revision.tex
│   │   │   │   ├── preamble.tex
│   │   │   │   ├── stage_strat_revision.pdf
│   │   │   │   └── sections/                    # 6 content sections
│   │   │   └── issues/                          # Consolidated thematic issue docs
│   │   │       ├── 01-architecture-and-physics-foundations.md
│   │   │       ├── 02-data-pipeline-and-validation.md
│   │   │       ├── 03-curriculum-and-training-loop.md
│   │   │       ├── MIGRATION.md
│   │   │       ├── README.md
│   │   │       └── archive/                     # 8 original issue files
│   │   └── sampling-method/                     # Sampling methodology
│   │       ├── sampling_method_instruction.tex
│   │       └── sampling_method_instruction.pdf
│   │
│   └── markdown_conversion/                     # LaTeX -> Markdown conversions (for reference)
│       ├── ctl_instruction.md                   # Authoritative CTL conversion
│       ├── pinn_architecture.md                 # Authoritative PINN architecture conversion
│       ├── sampling_method.md                   # Authoritative sampling conversion
│       ├── assess_data_quality.md               # Authoritative data quality conversion
│       ├── review_of_framework.md               # Authoritative framework review conversion
│       ├── stage_strat_revision.md              # Authoritative stage strategy conversion
│       └── _archive/                            # Unselected candidates from v1.3
│
├── paper_templates/                             # Academic paper templates
│   └── mdpi_template/
│       ├── raw_template.tex                     # Empty MDPI template
│       ├── raw_template.pdf
│       ├── paper.tex                            # Working paper draft
│       ├── paper.pdf                            # Compiled draft
│       ├── refs.bib                             # Bibliography
│       └── Definitions/                         # MDPI journal definitions
│           ├── mdpi.cls                         # MDPI document class
│           ├── mdpi.bst / mdpi_apacite.bst / mdpi_chicago.bst  # Bibliography styles
│           ├── mdpi_apacite.sty                 # APA citation style
│           ├── journalnames.tex                 # Journal name definitions
│           └── logo-*.{eps,pdf}                 # MDPI branding logos
│
├── reference-code/                              # Vendored reference implementations
│   ├── lyapunov/                                # Julia-based Lyapunov analysis
│   │   ├── 3. Quantifying Chaos (Lyapunov Exponents).jl
│   │   ├── 3. Quantifying Chaos (Lyapunov Exponents).ipynb
│   │   ├── 6. Miscellaneous Algorithms.jl
│   │   └── lyapunovs.md
│   └── reference_NNs/                           # Reference NN implementations (~63,000 files)
│       ├── deepxde-master/                      # DeepXDE library (28 MB, ~multiple thousand files)
│       ├── PINA-master/                         # PINA (Physics-Informed Neural networks for Applications)
│       ├── siren/                               # SIREN (Sinusoidal Representation Networks)
│       ├── GravNN-master/                       # Gravity-field Neural Networks
│       ├── hamiltonian-nn-master/               # Hamiltonian Neural Networks
│       ├── neural-symplectic-integrator-main/   # Neural symplectic integrator
│       ├── [removed-vendored-example]/                         # Another PINN reference
│       ├── PyTorch-LBFGS-master/                # LBFGS optimizer for PyTorch
│       └── pytorch-main/                        # PyTorch source reference
│
├── docs/                                        # Additional documentation
│   └── findings/                                # Audit reports and verification findings

├── AGENTS.md                                    # Agent instructions (13,607 bytes)
├── ANTIGRAVITY.md                               # Agent instructions (12,848 bytes)
├── CLAUDE.md                                    # Agent instructions - source of truth for data formats (13,630 bytes)
├── GEMINI.md                                    # Agent instructions (13,631 bytes)
└── README.md                                    # Project README (10,361 bytes)
```

## .planning/ Directory (GSD Project Management)

```
.planning/
├── config.json                                  # Project configuration (282 bytes)
├── ROADMAP.md                                   # Milestone tracking (7,803 bytes)
├── STATE.md                                     # Current project state snapshot (4,697 bytes)
├── MILESTONES.md                                # Milestone definitions (162 bytes)
├── PROJECT.md                                   # Project overview and scope (6,927 bytes)
├── REQUIREMENTS.md                              # Requirements specification (3,134 bytes)
├── RETROSPECTIVE.md                             # Retrospective notes (3,094 bytes)
├── codebase/                                    # Codebase mapping documents
│   ├── ARCHITECTURE.md                          # Architecture analysis
│   ├── STRUCTURE.md                             # Directory structure analysis
│   ├── CONCERNS.md                              # Technical debt and issues
│   ├── CONVENTIONS.md                           # Coding conventions
│   ├── TESTING.md                               # Testing patterns
│   ├── STACK.md                                 # Technology stack
│   └── INTEGRATIONS.md                          # External integrations
├── milestones/                                  # Milestone state files
├── phases/                                      # Phase execution records
│   ├── 01-code-rewrites-and-validation/         # Phase 1: 3 plans, 3 summaries + context/research/validation/verification
│   ├── 02-documentation-updates/                # Phase 2: 3 plans, 3 summaries + context/research/validation/verification
│   ├── 03-data-deletion-and-legacy-cleanup/     # Phase 3: 2 plans, 2 summaries + research/validation/verification
│   ├── 04-stale-reference-fixes/                # Phase 4: 2 plans, 2 summaries + context/research/validation/verification
│   ├── 05-content-completeness-verification/    # Phase 5: 1 plan, 1 summary + context/research/validation/verification
│   ├── 06-preamble-parity-verification/         # Phase 6: 1 plan, 1 summary + research/validation/verification
│   ├── 07-structure-fidelity-verification/      # Phase 7: 2 plans, 2 summaries + context/research/validation/verification
│   ├── 08-compilability-verification/           # Phase 8: 1 plan, 1 summary + context/research/validation/verification
│   ├── 09-issues-directory-consolidation/       # Phase 9: 3 plans, 3 summaries + context/research/validation/verification/reviews (complete)
├── quick/                                       # Quick tasks (ad-hoc, single-session)
│   ├── 260320-rca-modularize-pinn-architecture-latex-templ/
│   ├── 260320-rxu-split-ctl-instruction-final-tex-into-mod/
│   ├── 260320-sh3-modularize-review-of-ctl-pinn-framework-/
│   ├── 260320-ssi-modularize-stage-strat-revision-tex-into/
│   ├── 20260426-merge-sim-docs/
│   └── 20260426-update-brutus-footer-docs/
└── research/                                    # Research storage
```

## Directory Purposes

### `brutus_Newton-main/`
- **Purpose:** High-precision N-body numerical integrator using the Bulirsch-Stoer extrapolation method
- **Contains:** C++ source files (.cpp, .h), compiled binary, utility libraries, test inputs, build system
- **Key files:** `main.cpp` (CLI entry point), `Brutus.cpp` (orchestrator), `Bulirsch_Stoer.cpp` (ODE integrator), `Cluster.cpp` (N-body container), `Star.cpp` (body state), `makefile` (build config)
- **Source lines:** ~11 .cpp files, ~7 .h files, ~2,000 lines of C++ total (estimated)
- **Build output:** Single `brutus` binary
- **Note:** Contains Mac-specific hardcoded Homebrew paths in `makefile`. Also contains `makefile.original` as a backup.

### `simulation_data/Scripts/`
- **Purpose:** Active Python pipeline scripts for IC generation, Brutus execution, and metrics
- **Contains:** 10 active Python files across 3 functional subdirectories, plus 3 archived and 7 debug scripts
- **Key files:** `ic_generation/generate_ics.py`, `brutus_runners/run_brutus_both_type_simple.py`, `metrics_calculation/calculate_metrics.py`
- **Archived:** `Scripts/archived/` contains 3 deprecated scripts clearly marked as unused

### `simulation_data/Validation/`
- **Purpose:** Quality assurance: prescreening, analysis, audit, and dataset readiness validation
- **Contains:** 27 Python files across 5 subdirectories, plus generated figures and reports
- **Key subsystems:**
  - Prescreening: Leapfrog short-run filtering of unstable ICs
  - Analysis: Statistical analysis and visualization of simulation results
  - Audit reports: Data quality audit scripts and Markdown reports
  - Dataset readiness checks: 11-module automated validation suite with multiformat reporting

### `simulation_data/Data/`
- **Purpose:** All simulation input and output data
- **Contains:** ~38,399 text files (IC + Brutus output), ~15,047 JSON files (metrics), organized by dataset variant
- **Variant organization:** Folder name defines the variant ("gold" is in folder name, not file name)
- **File counts by variant:**
  - `ic_hierarchical/`: 4,857 files
  - `ic_standard_quasi_random/`: 2,749 files
  - `brutus_hierarchical/`: 4,857 files
  - `brutus_hierarchical_gold_standard/`: 4,857 files
  - `brutus_standard_quasi_random/`: 2,749 files
  - `brutus_standard_quasi_random_gold_standard/`: 2,565 files (184 fewer — documented in `standard_quasi_random_ids_not_in_gold.md`)
- **Testing data:** Small subsets for development (in `testing_data/`)
- **External:** IC raw storage is external to repo (set via `IC_RAW_DIR` env var)

### `simulation_data/Documentation/`
- **Purpose:** Dataset-level documentation, blacklists, and known issues
- **Contains:** README.md (source of truth for dataset specification), blacklist JSON, gold subset notes, problematic IC backups
- **Key files:** `README.md` (authoritative dataset docs), `problematic_ics_blacklist.json`, `standard_quasi_random_ids_not_in_gold.md`

### `pinn/`
- **Purpose:** CTL-PINN implementation: model architecture + data processing pipeline
- **Contains:** 2 main scripts + 1 modular package with 10 Python files, 6 sample HDF5 files
- **Key files:** `basic_architecture.py` (308 lines, model definition), `data-processing-pipeline-full.py` (1,650 lines, monolithic pipeline)
- **Modular refactor:** `data-handling/` (2,550 lines across 10 files: core/, processing/, scripts/)
- **Status:** Both monolithic and modular versions coexist (refactoring in progress)

### `pinn_instruction/`
- **Purpose:** Research methodology documentation: CTL methodology, PINN architecture, sampling methods, data quality assessment, framework reviews
- **Contains:** 49 LaTeX files across 5 document sets, 16 Markdown conversion files, research issues
- **Document sets:**
  1. `ctl-instruction/`: CTL curriculum training methodology (7 sections + appendix)
  2. `Data-quality-assessment/`: Data quality metrics and assessment protocol (7 sections)
  3. `pinn-architecture/`: PINN architecture design blueprint (9 sections, 3 inactive)
  4. `review-of-framework/review_of_framework/`: CTL-PINN framework review (7 sections)
  5. `review-of-framework/stage_strat_revision/`: Stage strategy revision (6 sections)
  6. `sampling-method/`: Standalone sampling methodology document
- **Each document set** follows the pattern: `main_*.tex` + `preamble.tex` + `sections/*.tex` + compiled PDF
- **Markdown conversions:** Located in `markdown_conversion/`, one authoritative file per source from v1.3 verification
- **Research issues:** Located in `pinn_instruction/issues/` — 3 consolidated thematic docs + MIGRATION.md + README.md + archive/

### `reference-code/`
- **Purpose:** Vendored reference implementations for research comparison and code reference
- **Contains:** ~63,000+ files (nearly the entire repo)
- **Subdirectories:**
  - `lyapunov/`: Julia scripts for Lyapunov analysis (3 files)
  - `reference_NNs/`: 9 cloned repositories (DeepXDE, SIREN, PINA, GravNN, HNN, Neural Symplectic Integrator, PINN-1, PyTorch-LBFGS, PyTorch source)
- **Size:** Dominated by `deepxde-master/` (28 MB), `pytorch-main/`, and other full cloned repos
- **Note:** These are NOT dependencies; they are reference implementations for comparison. The project's own PINN does not import from them.

### `paper_templates/`
- **Purpose:** Academic paper writing templates and working paper draft
- **Contains:** MDPI journal LaTeX template with definitions, bibliography, and working paper draft
- **Key files:** `mdpi_template/paper.tex` (working draft), `mdpi_template/mdpi.cls` (document class)

### `docs/`
- **Purpose:** Audit reports and verification findings
- **Contains:** `findings/milestone_v1.4/` (current v1.4 milestone reviews and gap-closure documents) and other current verification findings
- **Note:** Previously contained historical plans (`plans/`, `superpowers/`) — those have been removed. The earlier `findings/fixing_gaps/` directory was renamed to `findings/milestone_v1.4/`.

### `.planning/`
- **Purpose:** GSD (Goal-Structured Development) project management framework
- **Contains:** ROADMAP.md (milestones), STATE.md (current state), PROJECT.md (overview), REQUIREMENTS.md (spec), RETROSPECTIVE.md (lessons), 9 phases with plans/summaries/research/validation/verification, quick single-session tasks, research storage
- **Phases 1-9:** Completed (v1.0, v1.1, and v1.2 milestones)
- **codebase/:** Codebase mapping documents consumed by GSD orchestrator (ARCHITECTURE.md, STRUCTURE.md, CONVENTIONS.md, TESTING.md, STACK.md, INTEGRATIONS.md, CONCERNS.md)

## Naming Conventions

**Files:**
- **IC files:** `ic_<type>_<id>.txt` — e.g., `ic_hierarchical_0001.txt`, `ic_standard_quasi_random_0423.txt`
- **Brutus output:** `brutus_<type>_<id>.txt` — e.g., `brutus_hierarchical_0001.txt`, `brutus_standard_quasi_random_0423.txt`
- **Metrics JSON:** `sim_result_metric_<variant>_<id>.json`
- **Pipeline scripts:** snake_case with descriptive prefixes — `generate_ics.py`, `run_brutus_both_type_simple.py`, `calculate_metrics.py`
- **LaTeX sections:** numbered `NN_descriptive_name.tex` — e.g., `01_intro.tex`, `02_data_characterization.tex`
- **LaTeX mains:** `main_<document>.tex` with matching `preamble.tex`
- **GSD plans:** `NN-NN-PLAN.md` (phase-plan) — e.g., `01-01-PLAN.md`
- **GSD summaries:** `NN-NN-SUMMARY.md`
- **GSD context:** `NN-CONTEXT.md`, `NN-RESEARCH.md`, `NN-VALIDATION.md`, `NN-VERIFICATION.md`

**Directories:**
- **Functional grouping:** `ic_generation/`, `brutus_runners/`, `metrics_calculation/` (verb-first)
- **Data variant folders:** `brutus_hierarchical/`, `brutus_hierarchical_gold_standard/` (type_quality)
- **GSD phases:** `NN-short-description/` — e.g., `01-code-rewrites-and-validation/`
- **GSD quick tasks:** `YYMMDD-short-slug/` — e.g., `260320-rca-modularize-pinn-architecture-latex-templ/`
- **LaTeX documents:** kebab-case with hyphens — `ctl-instruction/`, `Data-quality-assessment/`, `review-of-framework/`

## Key File Locations

**Entry Points:**
- `brutus_Newton-main/brutus`: Compiled Brutus binary (N-body integration)
- `simulation_data/Scripts/ic_generation/generate_ics.py`: IC generation entry point
- `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py`: Prescreening entry point
- `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py`: Batch simulation entry point
- `simulation_data/Scripts/metrics_calculation/calculate_metrics.py`: Metrics extraction entry point
- `pinn/data-processing-pipeline-full.py`: PINN data preprocessing entry point (monolithic)
- `pinn/data-handling/scripts/preprocess_dataset.py`: PINN preprocessing entry point (modular)
- `pinn/data-handling/scripts/prepare_training_data.py`: Training batch preparation entry point
- `pinn/basic_architecture.py`: PINN architecture definition + sanity check
- `simulation_data/Validation/dataset_readiness_checks/__main__.py`: Data validation suite entry point

**Configuration:**
- `brutus_Newton-main/makefile`: C++ build configuration (macOS-specific paths)
- `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py`: Brutus parameters (lines 52-69)
- `simulation_data/Scripts/metrics_calculation/calculate_metrics.py`: Metrics parameters (lines 52-80)
- `simulation_data/Validation/dataset_readiness_checks/config.py`: Validation suite config
- `.planning/config.json`: Project configuration

**Core Logic:**
- `simulation_data/Scripts/ic_generation/ic_generation_utils.py`: IC sampling algorithms
- `brutus_Newton-main/Bulirsch_Stoer.cpp`: BS extrapolation ODE integrator
- `brutus_Newton-main/Brutus.cpp`: Integration orchestrator
- `pinn/basic_architecture.py`: SQRSkipResNetSIREN model
- `pinn/data-processing-pipeline-full.py`: Full data pipeline (source of truth per CLAUDE.md)
- `pinn/data-handling/core/parsing.py`: File parsing (699 lines, largest PINN module)

**Documentation (Source of Truth):**
- `CLAUDE.md`: Agent instructions with data format specs and pipeline docs
- `simulation_data/Documentation/README.md`: Dataset specification and anomalies
- `pinn_instruction/original_latex/framework-specs/ctl-instruction/`: CTL methodology
- `pinn_instruction/original_latex/framework-specs/pinn-architecture/`: Architecture design blueprint

**Testing:**
- `pinn/basic_architecture.py`: Self-contained test in `if __name__ == "__main__"` block
- `brutus_Newton-main/test_libs.cpp`: C++ library test driver
- `simulation_data/Data/testing_data/`: Small test datasets
- No dedicated test directory or test framework exists in this codebase

## Where to Add New Code

**New Feature (simulation pipeline stage):**
- Script: `simulation_data/Scripts/<new_stage_name>/<script_name>.py`
- Follow pattern: self-contained script with hardcoded config, CLI entry point

**New PINN Component (neural network variant):**
- Model definition: `pinn/<new_architecture>.py`
- Follow pattern: inherit from NN base class, implement forward(), add `if __name__` block for sanity check

**New PINN Data Processing Feature:**
- Core logic: `pinn/data-handling/core/<module_name>.py` or `pinn/data-handling/processing/<module_name>.py`
- Entry point: `pinn/data-handling/scripts/<script_name>.py`
- Use `@dataclass` for data structures, follow existing module patterns

**New Validation Module:**
- Module: `simulation_data/Validation/dataset_readiness_checks/modules/<module_name>.py`
- Follow pattern: implement `check()` function, register in `__main__.py`

**New LaTeX Document:**
- Structure: `pinn_instruction/original_latex/<doc-name>/main_<doc>.tex` + `preamble.tex` + `sections/*.tex`
- Follow pattern: modular sections, matching preamble structure

**New GSD Phase:**
- Create: `.planning/phases/NN-description/NN-01-PLAN.md`
- Follow pattern: phase-CONTEXT.md, phase-RESEARCH.md, PLAN.md with checklist, SUMMARY.md after completion

**Utilities / Helpers:**
- Shared simulation utils: `simulation_data/Validation/analysis/utils.py`
- Shared PINN utils: `pinn/data-handling/core/` (core) or `pinn/data-handling/processing/` (domain-specific)
- Shared validation utils: `simulation_data/Validation/dataset_readiness_checks/utils/`

**Do NOT add new code to:**
- `simulation_data/Scripts/archived/` (deprecated scripts only)
- `reference-code/` (vendored references, not project code)
- `pinn_instruction/` (documentation, not code)

## Special Directories

### Generated Files (Not Committed)
- `brutus_Newton-main/*.o`: C++ object files (build artifacts)
- `brutus_Newton-main/brutus`: Compiled binary (build artifact)
- `pinn_instruction/original_latex/**/*.aux, *.log, *.out, *.fls, *.fdb_latexmk, *.toc`: LaTeX compilation artifacts
- `.tmp/`: Temporary files
- `.venv/`: Python virtual environment
- `simulation_data/Scripts/ic_generation/__pycache__/`: Python bytecode cache
- `simulation_data/Validation/dataset_readiness_checks/__pycache__/`: Python bytecode cache

### Stale / Deprecated
- `simulation_data/Scripts/archived/`: 3 scripts explicitly archived and unused
- `simulation_data/Validation/analysis/figures/prescreening_copy_archive/`: Duplicate figure archive
- `brutus_Newton-main/makefile.original`: Backup of original makefile
- `pinn/data-handling/core/parsing.txt`: 13-line text file in code directory — seems to be notes/errata

### Unrecognized
- `pinn/data-handling/core/parsing.txt`: 13-line text file in code directory — seems to be notes/errata

### Size Statistics

| Category | Count | Notes |
|----------|-------|-------|
| Total tracked files | ~63,689 | Excluding .git, node_modules, __pycache__ |
| Brutus output (.txt) | ~23,354 | Dominates file count |
| Metrics (.json) | ~15,081 | One per Brutus output |
| Python (.py) | ~7,670 | Mostly in reference-code/ (vendored repos) |
| Project Python (.py) | ~130 | Excluding reference-code/ |
| C++ headers (.h) | ~2,183 | Mostly in reference-code/ |
| C++ source (.cpp) | ~1,950 | Mostly in reference-code/ |
| Brutus C++ | ~11 .cpp, ~7 .h | Core integrator |
| Project C++ | ~25 .cpp/.h | Including library utilities |
| Markdown (.md) | ~429 | Across all directories |
| LaTeX (.tex) | ~52 | PINN instruction documents |
| HDF5 (.h5) | ~6 | Sample preprocessed data |

**Project code (excluding reference-code/):**
- Python: ~130 files (~15,000-20,000 lines estimated)
- C++: ~25 files (~2,500-3,000 lines estimated)
- LaTeX: ~52 files across 6 document sets
- Data: ~38,000+ text files + ~15,000+ JSON files

---

*Structure analysis: 2026-04-27*
