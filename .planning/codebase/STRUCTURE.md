# Codebase Structure

**Analysis Date:** 2026-06-10

## Directory Layout

```
3_body_problem/                                 # Repository root
├── .claude/                                     # Claude Code agent config
│   ├── rules/                                   # Path-scoped rules (repo-map.md, dataset-reference.md, pinn-reference.md)
│   ├── settings.json / settings.local.json     # Claude Code settings
│   └── scheduled_tasks.json                     # Scheduled-task config
├── .codex/                                      # Codex agent config (hooks.json)
├── .context/                                    # Compound-engineering agent context
│   └── compound-engineering/
├── .cursor/                                     # Cursor agent config
├── .github/                                     # GitHub workflows and custom slash commands
│   ├── commands/                                # Custom slash command definitions
│   └── workflows/                               # CI/CD workflow YAML files
├── .githooks/                                   # Git hooks (commit-msg, pre-commit, pre-push, post-commit, post-merge, post-checkout, pre-rebase)
├── .planning/                                   # GSD project management (detailed below)
├── .understand-anything/                        # Code-understanding tool cache (fingerprints.json, knowledge-graph.json, intermediate/)
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
│   │       ├── reports/                         # Generated reports (csv/, json/, markdown/)
│   │       └── utils/                           # Shared utilities (logging, naming, parsers, physics_core)
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
├── pinn/                                        # CTL-PINN system — v1.3-era code, NOT spec-authoritative, pending FUT-01 rewrite
│   ├── basic_architecture.py                    # SQR-SkipResNet-SIREN model (308 lines); design authority = pinn_architecture.md spec
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
│       │   ├── input_vector.py                  # IC vector formulation (155 lines)
│       │   ├── stage_assignment.py              # Curriculum stage assignment (138 lines)
│       │   └── rosenstein_lyapunov.py           # Lyapunov exponent estimation (225 lines)
│       └── scripts/                             # Entry point scripts
│           ├── __init__.py
│           ├── preprocess_dataset.py            # Raw-to-HDF5 preprocessing (198 lines)
│           └── prepare_training_data.py         # HDF5-to-training-batches (258 lines)
│
├── pinn_instruction/                            # Research methodology + AUTHORITATIVE framework specs (restructured 2026)
│   ├── markdown_conversion/                     # Markdown form of specs (AUTHORITATIVE specs live here)
│   │   ├── framework-specs/                     # ── AUTHORITATIVE framework specs ──
│   │   │   ├── ctl_instruction.md               # CTL methodology, input-vector, curriculum (spec-edit target)
│   │   │   ├── pinn_architecture.md             # Network architecture, AD contract, output head (spec-edit target)
│   │   │   └── sampling_method.md               # IC sampling (FROZEN historical record; SCOPE-08)
│   │   ├── framework-revisions/                 # Research reports (non-authoritative)
│   │   │   ├── data_quality_assessment.md       # Data-quality research report (read-only; SCOPE-09)
│   │   │   ├── review-of-framework/             # Framework review conversion
│   │   │   ├── stage-strat-revision/            # Stage-strategy revision conversion
│   │   │   └── research_reports/                # Per-issue external research + resolution docs
│   │   │       └── 01-architecture-and-physics-foundations/
│   │   │           ├── ctl_pinn_resolution.md   # v1.4 candidate verdict source (resolution doc)
│   │   │           ├── chatgpt_research_report.md
│   │   │           ├── claude_research_report.md
│   │   │           ├── claude_research_report_2.md
│   │   │           └── gemini_research_report.md
│   │   └── README.md
│   │
│   ├── original_latex/                          # LaTeX sources (mirrors the markdown split)
│   │   ├── framework-specs/                     # LaTeX sources for the authoritative specs
│   │   │   ├── ctl-instruction/                 # main_CTL.tex + preamble_CTL.tex + sections/
│   │   │   ├── pinn-architecture/               # main_pinn.tex + preamble + sections/
│   │   │   └── sampling-method/                 # sampling methodology LaTeX
│   │   └── framework-revisions/                 # LaTeX sources for revisions/research
│   │       ├── data-quality-assessment/
│   │       └── review-of-framework/             # review_of_framework/ + stage_strat_revision/
│   │
│   └── issues/                                  # Consolidated thematic issue docs (top-level)
│       ├── 01-architecture-and-physics-foundations.md  # v1.4 target (resolved)
│       ├── 02-data-pipeline-and-validation.md   # v1.5 target (non-authoritative; under adjudication)
│       ├── 03-curriculum-and-training-loop.md
│       ├── MIGRATION.md
│       ├── README.md
│       └── archive/                             # Original pre-consolidation issue files
│
├── paper_templates/                             # Academic paper templates
│   └── mdpi_template/
│       ├── raw_template.tex                     # Empty MDPI template
│       ├── raw_template.pdf
│       ├── paper.tex                            # Working paper draft
│       ├── paper.pdf                            # Compiled draft
│       ├── refs.bib                             # Bibliography
│       └── Definitions/                         # MDPI journal definitions (mdpi.cls, .bst, logos)
│
├── reference-code/                              # Vendored reference implementations (NOT dependencies)
│   ├── lyapunov/                                # Julia-based Lyapunov analysis (3 files)
│   └── reference_NNs/                           # 9 cloned NN repos (deepxde, PINA, siren, GravNN, HNN, etc.)
│
├── tools/                                       # Standalone tooling
│   └── spec-render-check/                       # Node spec-render/adjudication detector (v1.4 acceptance tooling)
│       ├── detect.mjs                           # Detector entry point
│       ├── adjudications/                       # Adjudication fixtures (22-02-pinn-architecture.json, 22-03-ctl-instruction.json)
│       ├── fixtures/                            # Test fixtures
│       ├── node_modules/                        # Node deps (not committed)
│       ├── package.json / package-lock.json
│       └── README.md
│
├── scripts/                                     # Git-policy + setup tooling
│   ├── agent-commit                             # Mandated agent commit wrapper (hooks enforced)
│   ├── setup-git-hooks.sh                       # Installs .githooks as core.hooksPath
│   └── git_policy/                              # Commit/staged-path validation
│       ├── __init__.py
│       ├── guard_agent_git_command.py
│       ├── validate_commit_msg.py
│       └── validate_staged_paths.py
│
├── tests/                                       # Pytest suites (governance + phase validation)
│   ├── test_phase12_validation.py               # Phase validation tests
│   └── git_policy/test_git_policy.py            # Git-policy guard tests
│
├── docs/                                        # Project documentation + governance
│   ├── README.md                                # Docs lifecycle policy
│   ├── git-guidelines.md                        # Full git commit policy
│   ├── findings/                                # Audit reports and verification findings (milestone_v1.4/)
│   ├── runbooks/                                # Operational runbooks
│   │   ├── migration/                           # exact-state-mac-migration.md (restore runbook)
│   │   └── EDL/                                 # Empirical Decision Loop runbooks
│   ├── user_plans/                              # User-authored plans
│   ├── work/                                    # designs/, plans/, reviews/ (docs plan lifecycle)
│   └── archive/                                 # Archived docs (work/)
│
├── docs_temp/                                   # Scratch/handoff docs (chat_history, agent-context bundle, phase verification notes)
│
├── AGENTS.md                                    # CANONICAL agent instructions (CLAUDE.md, GEMINI.md symlink here)
├── ANTIGRAVITY.md                               # Antigravity agent instructions (separate file)
├── CLAUDE.md -> AGENTS.md                        # Symlink to canonical instructions
├── GEMINI.md -> AGENTS.md                        # Symlink to canonical instructions
└── README.md                                    # Project README
```

## .planning/ Directory (GSD Project Management)

```
.planning/
├── config.json                                  # Project configuration
├── ROADMAP.md                                   # Milestone tracking (v1.0–v1.5 + deferred LaTeX sync)
├── STATE.md                                     # Current project state snapshot
├── MILESTONES.md                                # Milestone definitions
├── PROJECT.md                                   # Project overview and scope
├── REQUIREMENTS.md                              # Active (v1.5) requirements + SCOPE rules
├── RETROSPECTIVE.md                             # Retrospective notes
├── TONIGHT.md                                   # Session working notes
├── codebase/                                    # Codebase mapping documents (this file's home)
│   ├── ARCHITECTURE.md  STRUCTURE.md  CONCERNS.md
│   ├── CONVENTIONS.md   TESTING.md
│   └── STACK.md         INTEGRATIONS.md
├── milestones/                                  # Per-milestone archives (requirements, roadmap, audit, gaps)
│   ├── v1.0-* v1.3-* v1.4-*                      # Shipped-milestone archives
│   ├── v1.4-GAPS.md                             # v1.4 milestone-wide gap index
│   └── v1.4-phases/                             # Archived v1.4 phase folders (16–22, incl. 20.5)
│       ├── 16-evidence-framework-and-issue-adjudication/
│       ├── 17-input-and-output-contracts/
│       ├── 18-frame-and-gauge-contracts/
│       ├── 19-physics-and-loss-contracts/
│       ├── 20-architecture-and-normalization-cleanup/
│       ├── 20.5-sampling-coordinate-allocation/
│       ├── 21-acceptance-checks-and-handoff/
│       └── 22-framework-spec-cleanup/
├── phases/                                      # ACTIVE phase folders (current milestone)
│   └── 23-research-package-assembly/            # v1.5 Phase 23 (CONTEXT, RESEARCH, PATTERNS, VALIDATION, DISCUSSION-LOG)
├── research/                                    # Cross-cutting research storage
│   ├── ARCHITECTURE.md FEATURES.md PITFALLS.md STACK.md SUMMARY.md  # Research notes
│   └── edl/                                     # Non-canonical Empirical Decision Loop briefs
│       ├── README.md INDEX.md
│       ├── EDL-19-01-epsilon-H.md               # EDL brief (Phase 19 epsilon_H)
│       └── EDL-19-01-resolution.md              # User-resolved EDL outcome
├── reports/                                     # Milestone summary reports (MILESTONE_SUMMARY-v1.4.md)
├── forensics/                                   # Forensic incident reports (report-YYYYMMDD-HHMMSS.md)
└── tmp/                                         # Planning scratch
```

> **Note:** v1.0–v1.4 phase folders (Phases 1–22) are archived under
> `.planning/milestones/<version>-phases/` or their milestone archives. `.planning/phases/`
> now holds only the active milestone's phases (currently v1.5 Phase 23). The milestone-wide
> gap index for v1.5 will be `.planning/milestones/v1.5-GAPS.md` once it lands.

## Directory Purposes

### `brutus_Newton-main/`
- **Purpose:** High-precision N-body numerical integrator using the Bulirsch-Stoer extrapolation method
- **Contains:** C++ source files (.cpp, .h), compiled binary, utility libraries, test inputs, build system
- **Key files:** `main.cpp` (CLI entry point), `Brutus.cpp` (orchestrator), `Bulirsch_Stoer.cpp` (ODE integrator), `Cluster.cpp` (N-body container), `Star.cpp` (body state), `makefile` (build config)
- **Note:** Contains Mac-specific hardcoded Homebrew paths in `makefile`; `makefile.original` is a backup.

### `simulation_data/Scripts/`
- **Purpose:** Active Python pipeline scripts for IC generation, Brutus execution, and metrics
- **Contains:** 10 active Python files across 3 functional subdirectories, plus 3 archived and debug scripts
- **Key files:** `ic_generation/generate_ics.py`, `brutus_runners/run_brutus_both_type_simple.py`, `metrics_calculation/calculate_metrics.py`
- **SCOPE-05:** `ic_generation/` is a permitted grounding source for `sampling_method.md`.

### `simulation_data/Validation/`
- **Purpose:** Quality assurance: prescreening, analysis, audit, and dataset readiness validation
- **Contains:** ~27 Python files across 5 subdirectories, plus generated figures and reports
- **Key subsystems:** prescreening (leapfrog short-run filtering), analysis (stats + viz), audit reports, dataset readiness checks (11-module suite, multiformat reporting)

### `simulation_data/Data/`
- **Purpose:** All simulation input and output data
- **Variant organization:** Folder name defines the variant ("gold" is in the folder name, not the file name)
- **File counts by variant:** `ic_hierarchical/` 4,857; `ic_standard_quasi_random/` 2,749; `brutus_hierarchical/` 4,857; `brutus_hierarchical_gold_standard/` 4,857; `brutus_standard_quasi_random/` 2,749; `brutus_standard_quasi_random_gold_standard/` 2,565 (184 fewer — see `standard_quasi_random_ids_not_in_gold.md`)
- **External:** IC raw storage is external to repo (set via `IC_RAW_DIR` env var)
- **SCOPE-06/07:** This on-disk dataset and `simulation_data/Scripts/` are v1.5 empirical grounding sources.

### `simulation_data/Documentation/`
- **Purpose:** Dataset-level documentation, blacklists, known issues
- **Key files:** `README.md` (authoritative dataset spec), `problematic_ics_blacklist.json`, `standard_quasi_random_ids_not_in_gold.md`

### `pinn/`
- **Purpose:** CTL-PINN implementation: model architecture + data processing pipeline
- **Status:** **v1.3-era code, NOT spec-authoritative; slated for FUT-01 rewrite from the framework specs.** Both monolithic (`data-processing-pipeline-full.py`) and modular (`data-handling/`) versions coexist (duplicate code, refactoring in progress).
- **Design authority:** `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` and `ctl_instruction.md` — read design from there, not from this code.

### `pinn_instruction/`
- **Purpose:** AUTHORITATIVE framework specs + research methodology + issue adjudication.
- **Restructured (2026):** `original_latex/` and `markdown_conversion/` are each split into `framework-specs/` (authoritative) and `framework-revisions/` (non-authoritative research reports). The earlier flat list of LaTeX doc sets (ctl-instruction, Data-quality-assessment, pinn-architecture, review-of-framework, sampling-method directly under `original_latex/`) no longer applies — those now live under `framework-specs/` and `framework-revisions/`.
- **AUTHORITATIVE specs:** `markdown_conversion/framework-specs/{ctl_instruction,pinn_architecture,sampling_method}.md`. `ctl_instruction.md` and `pinn_architecture.md` are the only spec-edit targets in active milestones; `sampling_method.md` is frozen (SCOPE-08).
- **Issues:** `pinn_instruction/issues/` (TOP-LEVEL, not nested) — `01`/`02`/`03` thematic docs + MIGRATION.md + README.md + archive/. `02-data-pipeline-and-validation.md` is the v1.5 (non-authoritative) target.
- **Research reports:** `markdown_conversion/framework-revisions/research_reports/01-.../ctl_pinn_resolution.md` is the v1.4 candidate verdict source plus external research reports.

### `reference-code/`
- **Purpose:** Vendored reference implementations for comparison; NOT dependencies, NOT imported by project code.
- **Subdirectories:** `lyapunov/` (Julia, 3 files), `reference_NNs/` (9 cloned repos incl. deepxde, PINA, siren, GravNN, HNN, neural-symplectic-integrator, PINN-1, PyTorch-LBFGS, pytorch).

### `tools/`
- **Purpose:** Standalone tooling. Currently `spec-render-check/` — a Node detector (`detect.mjs`) that validates spec rendering/adjudication using fixtures in `adjudications/` and `fixtures/` (v1.4 acceptance tooling).

### `scripts/`
- **Purpose:** Git-policy enforcement and hook setup. `agent-commit` is the mandated commit path for agents; `setup-git-hooks.sh` installs `.githooks`; `git_policy/` holds commit-message / staged-path validators.

### `tests/`
- **Purpose:** Pytest suites for governance and phase-artifact validation (`test_phase12_validation.py`, `git_policy/test_git_policy.py`). The cached `__pycache__/test_v1_4_acceptance.cpython-312.pyc` indicates a v1.4 acceptance test ran here.

### `.githooks/`
- **Purpose:** Git hooks (commit-msg, pre-commit, pre-push, post-commit, post-merge, post-checkout, pre-rebase) enforcing the commit protocol. Activated via `scripts/setup-git-hooks.sh` (sets `core.hooksPath=.githooks`).

### `docs/`
- **Purpose:** Project documentation + governance policy. Key files: `README.md` (docs lifecycle), `git-guidelines.md` (commit policy). Subdirs: `findings/` (verification findings, `milestone_v1.4/`), `runbooks/` (`migration/exact-state-mac-migration.md`, `EDL/`), `user_plans/`, `work/` (designs/plans/reviews — docs plan lifecycle), `archive/`.

### `docs_temp/`
- **Purpose:** Scratch / handoff material (chat history, external-agent context bundle, phase verification notes, `work/`). Not part of the canonical docs lifecycle.

### `.planning/`
- **Purpose:** GSD (Goal-Structured Development) project management framework.
- **Milestone state:** v1.0–v1.4 shipped (Phases 1–22, incl. 20.5); v1.5 (Phases 23–29) in progress on branch `milestone/v1.5`, currently Phase 23. Active phase folders live in `phases/`; shipped phases are archived under `milestones/<version>-phases/`.
- **codebase/:** Codebase mapping documents consumed by GSD orchestrator (ARCHITECTURE, STRUCTURE, CONVENTIONS, TESTING, STACK, INTEGRATIONS, CONCERNS).

## Naming Conventions

**Files:**
- **IC files:** `ic_<type>_<id>.txt` — e.g., `ic_hierarchical_0001.txt`, `ic_standard_quasi_random_0423.txt`
- **Brutus output:** `brutus_<type>_<id>.txt`
- **Metrics JSON:** `sim_result_metric_<variant>_<id>.json`
- **Pipeline scripts:** snake_case with descriptive prefixes — `generate_ics.py`, `run_brutus_both_type_simple.py`, `calculate_metrics.py`
- **Framework specs (markdown):** snake_case — `ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`
- **LaTeX sections:** numbered `NN_descriptive_name.tex`; mains `main_<document>.tex` with matching `preamble.tex`
- **GSD plans/summaries/context:** `NN-NN-PLAN.md`, `NN-NN-SUMMARY.md`, `NN-CONTEXT.md`, `NN-RESEARCH.md`, `NN-VALIDATION.md`, `NN-VERIFICATION.md`, `NN-GAPS.md`, `NN-PATTERNS.md`, `NN-DISCUSSION-LOG.md`
- **Adjudication fixtures:** `NN-NN-<spec-name>.json` (e.g., `22-02-pinn-architecture.json`)
- **EDL briefs:** `EDL-NN-NN-<slug>.md` (+ `-resolution.md`)
- **Forensics:** `report-YYYYMMDD-HHMMSS.md`

**Directories:**
- **Functional grouping:** `ic_generation/`, `brutus_runners/`, `metrics_calculation/` (verb/noun-first)
- **Data variant folders:** `brutus_hierarchical/`, `brutus_hierarchical_gold_standard/` (type_quality)
- **GSD phases:** `NN-short-description/` — e.g., `23-research-package-assembly/`
- **Milestone archives:** `vX.Y-phases/`, `vX.Y-<artifact>.md`
- **LaTeX / spec doc dirs:** kebab-case — `ctl-instruction/`, `pinn-architecture/`, `data-quality-assessment/`, `review-of-framework/`

## Key File Locations

**Entry Points:**
- `brutus_Newton-main/brutus`: Compiled Brutus binary (N-body integration)
- `simulation_data/Scripts/ic_generation/generate_ics.py`: IC generation entry point
- `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py`: Prescreening entry point
- `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py`: Batch simulation entry point
- `simulation_data/Scripts/metrics_calculation/calculate_metrics.py`: Metrics extraction entry point
- `pinn/data-processing-pipeline-full.py` (v1.3): PINN data preprocessing entry point (monolithic)
- `pinn/data-handling/scripts/preprocess_dataset.py` (v1.3): PINN preprocessing entry point (modular)
- `pinn/data-handling/scripts/prepare_training_data.py` (v1.3): Training batch preparation entry point
- `pinn/basic_architecture.py` (v1.3): PINN architecture definition + sanity check
- `simulation_data/Validation/dataset_readiness_checks/__main__.py`: Data validation suite entry point
- `tools/spec-render-check/detect.mjs`: Spec-render detector
- `scripts/agent-commit`: Mandated agent commit path

**Configuration:**
- `brutus_Newton-main/makefile`: C++ build configuration (macOS-specific paths)
- `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py`: Brutus parameters
- `simulation_data/Scripts/metrics_calculation/calculate_metrics.py`: Metrics parameters
- `simulation_data/Validation/dataset_readiness_checks/config.py`: Validation suite config
- `.planning/config.json`: Project configuration
- `.claude/settings.json`, `.codex/hooks.json`, `.githooks/`: Agent/git tooling config

**Core Logic:**
- `simulation_data/Scripts/ic_generation/ic_generation_utils.py`: IC sampling algorithms
- `brutus_Newton-main/Bulirsch_Stoer.cpp`, `Brutus.cpp`: BS extrapolation integrator + orchestrator
- `pinn/basic_architecture.py` (v1.3): SQRSkipResNetSIREN model (design authority = spec)
- `pinn/data-handling/core/parsing.py`: File parsing (699 lines, largest PINN module)

**Documentation (Source of Truth):**
- `AGENTS.md`: Canonical agent instructions with data-format specs (CLAUDE.md/GEMINI.md symlink here)
- `simulation_data/Documentation/README.md`: Dataset specification and anomalies
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`: CTL methodology (AUTHORITATIVE)
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`: Architecture/AD contract (AUTHORITATIVE)
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`: IC sampling (AUTHORITATIVE, frozen)

**Testing:**
- `tests/test_phase12_validation.py`, `tests/git_policy/test_git_policy.py`: Pytest suites
- `pinn/basic_architecture.py`: Self-contained test in `if __name__ == "__main__"` block (v1.3)
- `brutus_Newton-main/test_libs.cpp`: C++ library test driver
- `tools/spec-render-check/`: Node detector with fixtures
- `simulation_data/Data/testing_data/`: Small test datasets

## Where to Add New Code

**New Feature (simulation pipeline stage):**
- Script: `simulation_data/Scripts/<new_stage_name>/<script_name>.py`
- Follow pattern: self-contained script with hardcoded config, CLI entry point

**New PINN Component (neural network variant):**
- NOTE: Do not extend `pinn/` as if it were the design — it is v1.3 code pending FUT-01. New PINN code is generated from the framework specs during FUT-01, not added ad hoc here.

**New Validation Module:**
- Module: `simulation_data/Validation/dataset_readiness_checks/modules/<module_name>.py`
- Follow pattern: implement `check()` function, register in `__main__.py`

**New Framework-Spec Edit (active milestones):**
- Edit ONLY `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` or `pinn_architecture.md`. `sampling_method.md` is frozen (SCOPE-08); `framework-revisions/` is read-only research material. Surface source-silent semantic decisions per the STOP protocol in `AGENTS.md`.

**New Test:**
- Add to `tests/` (pytest). Git-policy tests live in `tests/git_policy/`.

**New Governance/Tooling:**
- Git-policy helpers: `scripts/git_policy/`. Hooks: `.githooks/`. Detectors: `tools/<tool-name>/`.

**New GSD Phase:**
- Create: `.planning/phases/NN-description/` with `NN-CONTEXT.md`, `NN-RESEARCH.md`, `NN-NN-PLAN.md`, `NN-GAPS.md`; `NN-NN-SUMMARY.md` after completion.

**Utilities / Helpers:**
- Shared simulation utils: `simulation_data/Validation/analysis/utils.py`
- Shared validation utils: `simulation_data/Validation/dataset_readiness_checks/utils/`

**Do NOT add new code to:**
- `simulation_data/Scripts/archived/` (deprecated scripts only)
- `reference-code/` (vendored references, not project code)
- `pinn/` as a design target (v1.3 code, pending FUT-01 rewrite from specs)
- `pinn_instruction/` framework-revisions or `sampling_method.md` (read-only / frozen)

## Special Directories

### Generated Files (Not Committed)
- `brutus_Newton-main/*.o`, `brutus_Newton-main/brutus`: C++ build artifacts
- `pinn_instruction/original_latex/**/*.{aux,log,out,fls,fdb_latexmk,toc}`: LaTeX artifacts
- `tools/spec-render-check/node_modules/`: Node deps
- `.tmp/`, `.venv/`, `**/__pycache__/`, `.understand-anything/intermediate/`: caches/temp

### Stale / Deprecated / Scratch
- `simulation_data/Scripts/archived/`: 3 archived, unused scripts
- `simulation_data/Validation/analysis/figures/prescreening_copy_archive/`: Duplicate figure archive
- `brutus_Newton-main/makefile.original`: Backup of original makefile
- `pinn/data-handling/core/parsing.txt`: 13-line notes/errata file in a code directory
- `docs_temp/`: Scratch handoff docs (not canonical)
- `pinn_instruction/issues/archive/`, `pinn_instruction/markdown_conversion/framework-revisions/...`: archived/research material

### Size Statistics (approximate; reference-code dominates raw counts)

| Category | Count | Notes |
|----------|-------|-------|
| Total tracked files | ~63,000+ | Excluding .git, node_modules, __pycache__ |
| Brutus output (.txt) | ~15,028 | Across 4 variant folders |
| Metrics (.json) | ~15,047 | Roughly one per Brutus output |
| Project Python (.py) | ~130 | Excluding reference-code/ |
| Project C++ | ~25 .cpp/.h | Brutus core + library utilities |
| Markdown (.md) | hundreds | Specs, planning, docs |
| LaTeX (.tex) | ~50+ | Framework-spec + revision sources |

---

*Structure analysis: 2026-06-10*
