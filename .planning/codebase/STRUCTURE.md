# Structure

## Directory Layout

```
3_body_problem/
├── brutus_Newton-main/             # C++ N-body integrator
│   ├── main.cpp                    # CLI entry point
│   ├── Brutus.{cpp,h}             # Integrator orchestrator
│   ├── Bulirsch_Stoer.{cpp,h}     # BS extrapolation method
│   ├── Cluster.{cpp,h}            # N-body cluster container
│   ├── Star.{cpp,h}               # Individual body representation
│   ├── makefile                    # Build config (M2 Mac paths)
│   ├── lib/                        # Timer, Data_Handler utilities
│   ├── mplib/                      # Multi-precision support
│   └── input/                      # Test inputs
│
├── simulation_data/                # Python pipeline + datasets
│   ├── Scripts/
│   │   ├── ic_generation/          # Stage 1: IC generators
│   │   ├── brutus_runners/         # Stage 3: Batch simulation runners
│   │   ├── metrics_calculation/    # Stage 4: Conservation metrics
│   │   ├── archived/              # Old/unused scripts
│   │   └── debug/                  # Debug utilities
│   ├── Data/
│   │   ├── ic_final/               # Final ICs (2 variant folders)
│   │   ├── brutus_output/          # Simulation results (4 variant folders)
│   │   ├── metrics/                # Computed conservation metrics
│   │   └── testing_data/           # Test datasets
│   ├── Validation/
│   │   ├── prescreening/           # Stage 2: IC prescreening
│   │   ├── analysis/               # Analysis scripts
│   │   ├── audit_reports/          # Data quality audits
│   │   └── dataset_readiness_checks/ # Pre-training validation
│   └── Documentation/              # Dataset docs, blacklists
│
├── pinn/                           # PINN system
│   ├── basic_architecture.py       # Model architecture definition
│   ├── data-processing-pipeline-full.py  # Full data pipeline
│   └── data-handling/              # Modular data handling package
│       ├── core/                   # Parsing, scaling, data structures
│       ├── processing/             # IC vector, invariants, stages
│       └── scripts/                # Preprocessing entry points
│
├── pinn_instruction/               # Methodology documentation
│   ├── markdown_conversions/       # Key reference docs (CTL, architecture, sampling)
│   ├── ctl-instruction/            # CTL methodology source
│   ├── pinn-architecture/          # Architecture design source
│   └── sampling-method/            # Sampling methodology source
│
├── reference-code/                 # External reference implementations
│   ├── lyapunov/                   # Julia Lyapunov analysis
│   └── reference_NNs/             # 9 NN reference repos
│
├── paper_templates/                # Paper/documentation templates
├── docs/                           # Additional docs and plans
├── Qwen3.5-2B-4bit/               # Downloaded ML model (separate)
│
├── AGENTS.md                       # Agent instructions
├── ANTIGRAVITY.md                  # Agent instructions (Antigravity)
├── CLAUDE.md                       # Agent instructions (Claude)
├── GEMINI.md                       # Agent instructions (Gemini)
├── QWEN.md                         # Agent instructions (Qwen)
└── README.md                       # Project README
```

## Naming Conventions

### Data Files

- **IC files:** `ic_<type>_<id>.txt` (e.g., `ic_hierarchical_0001.txt`)
- **Brutus output:** `brutus_<type>_<id>.txt` (e.g., `brutus_hierarchical_0001.txt`)
- **Folder defines variant** — "gold" is not in the filename, only in the parent folder name
- **Numeric ID** maps IC to corresponding Brutus output

### Dataset Variant Folders

| Folder | IC Type | Quality |
|--------|---------|---------|
| `ic_hierarchical/` | Hierarchical | Standard |
| `ic_standard_quasi_random/` | Standard quasi-random | Standard |

Gold-standard distinction lives only in the Brutus output folders (`brutus_output/brutus_hierarchical_gold_standard/` and `brutus_output/brutus_standard_quasi_random_gold_standard/`), not in the IC folders.

## Key Locations

| What | Where |
|------|-------|
| Brutus binary | `brutus_Newton-main/brutus` |
| IC generator core | `simulation_data/Scripts/ic_generation/ic_generation_utils.py` |
| Prescreener | `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py` |
| Dataset documentation | `simulation_data/Documentation/DATASET_DOCUMENTATION.md` |
| PINN architecture | `pinn/basic_architecture.py` |
| PINN data pipeline (source of truth) | `pinn/data-processing-pipeline-full.py` |
| CTL instruction | `pinn_instruction/markdown_conversions/CTL-instruction-final.md` |
| Blacklisted ICs | `simulation_data/Documentation/problematic_ics_blacklist.json` |
