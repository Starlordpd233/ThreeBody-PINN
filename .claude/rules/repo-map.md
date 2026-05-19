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
- `.planning/` — GSD planning artifacts and phases

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
