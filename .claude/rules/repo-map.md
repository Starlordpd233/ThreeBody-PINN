## Project Overview

This repository implements a complete three-body simulation and CTL-PINN training stack:
- **Brutus**: High-precision N-body integrator (C++, arbitrary precision)
- **Python Pipeline**: IC generation, prescreening, simulation, metrics
- **CTL-PINN**: Curriculum-trained Physics-Informed Neural Network
- **Reference Code**: Lyapunov analysis and neural network baselines

## Key Directories

- `brutus_Newton-main/` — C++ N-body integrator
- `simulation_data/` — Simulation pipeline and datasets
- `pinn/` — PINN system and data processing
- `pinn_instruction/` — Instruction and methodology docs
- `paper_templates/` — Documentation templates
- `reference-code/` — Reference implementations
- `docs/` — Lifecycle-managed project docs: conventions (`docs/README.md`), runbooks, work artifacts
- `tools/` — Verification tooling (`tools/spec-render-check/` render detector suite)
- `.planning/` — GSD planning artifacts and phases
- `.planning/research/edl/` — Non-canonical EDL research-support briefs for empirically consequential source-silent gaps

## Track Aliases (user-defined shorthand, 2026-06-11)

- **specwork** — the framework-specs design/editing stage: authoring and adjudicating
  `ctl_instruction.md` / `pinn_architecture.md` (the v1.4/v1.5-style adjudication
  milestones and the future doc-03 milestone). The scientific backbone track.
- **trainex** — the training-execution development (the "reality pipeline"): the user
  runbook, the PH-1..PH-10 research placeholders, and the future build of the training
  pipeline + PINN code (FUT-01/FUT-04). Reference design:
  `docs/work/designs/cross_cutting/training-execution/2026-06-10-training-execution-design.md`.
  Research packages for trainex decisions live at
  `pinn_instruction/markdown_conversion/framework-specs/trainex-<id>/`, numbered as
  research rounds (e.g. `trainex-r1/` = the foundational round; `trainex-r2/` = the
  post-framework tuning round).

When the user says "specwork" or "trainex", they mean these tracks.

Both tracks delegate research-grade decisions via the **External Research Workflow
(ERW)** — canonical runbook:
`docs/runbooks/external-research/2026-06-11-external-research-workflow.md`. Read it
before assembling any external research package.

## Key Scripts

| Purpose | Script |
|---|---|
| IC generation | `simulation_data/Scripts/ic_generation/generate_ics.py` |
| Stage 2 prescreening | `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py` |
| Brutus batch runner | `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py` |
| Gold hierarchical runner | `simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py` |
| Metrics calculation | `simulation_data/Scripts/metrics_calculation/calculate_metrics.py` |
| PINN architecture | `pinn/basic_architecture.py` |
| Data pipeline | `pinn/data-processing-pipeline-full.py` |
| IC utility functions | `simulation_data/Scripts/ic_generation/ic_generation_utils.py` |
