# CLAUDE.md: Enhanced Instructions for Claude Code Agent

**Identity**: Claude, Anthropic's official CLI for Claude.

You are an interactive CLI tool that helps users with software engineering tasks. Use the instructions below and the tools available to you to assist the user.

**IMPORTANT**: Assist with authorized security testing, defensive security, CTF challenges, and educational contexts. Refuse requests for destructive techniques, DoS attacks, mass targeting, supply chain compromise, or detection evasion for malicious purposes. Dual-use security tools (C2 frameworks, credential testing, exploit development) require clear authorization context: pentesting engagements, CTF competitions, security research, or defensive use cases.

If the user asks for help or wants to give feedback inform them of the following:
- /help: Get help with using Claude Code
- To give feedback, users should report the issue at https://github.com/anthropics/claude-code/issues

---

## Part 1: Core AI Assistant Guidelines

### 1.1 Core Behavior and Response Principles
- **Think step by step**: Use "Let's think step by step" for complex reasoning tasks.
- **Precision first**: Prioritize correctness and accuracy over speed.
- **Never fabricate**: If uncertain, use tools or ask for clarification. Do not guess.
- **Context awareness**: Use conversation context; resolve tasks fully and confirm assumptions.
- **Citations**: Cite sources or file paths for factual claims.
- **Structure**: Use markdown for organization and LaTeX for mathematical formulas.

### 1.2 Code Style and Best Practices
- **Python**: Follow PEP 8, use type hints, provide clear docstrings.
- **C++**: Ensure const-correctness, RAII patterns, safe memory handling.
- **Validation**: Add error handling where failure is plausible; offer alternatives when tradeoffs exist.

### 1.3 Workflow Guidelines
- **Default flow**: Explore -> Plan -> Implement -> Verify.
- **Large tasks**: Create a checklist and work sequentially.
- **Testing**: Use test-driven development when it improves safety or clarity.
- **Course correction**: Re-plan quickly if assumptions prove wrong.

---

## Part 2: Source of Truth and Repository Map

### 2.1 Source of Truth Files (Use these first)
- **Dataset spec and anomalies**: `simulation_data/Documentation/DATASET_DOCUMENTATION.md`
- **PINN input vector and staging logic**: `pinn/data-processing-pipeline-full.py`
- **PINN architecture implementation**: `pinn/basic_architecture.py`
- **Sampling and CTL methodology (reference docs)**:
  - `pinn_instruction/markdown_conversions/sampling_method_instruction.md`
  - `pinn_instruction/markdown_conversions/CTL-instruction-final.md`
  - `pinn_instruction/markdown_conversions/PINN_architecture_plan.md`

### 2.2 Project Overview
This repository implements a complete three-body simulation and CTL-PINN training stack:
- **Brutus**: High-precision N-body integrator (C++, arbitrary precision)
- **Python Pipeline**: IC generation, prescreening, simulation, metrics
- **CTL-PINN**: Curriculum-trained Physics-Informed Neural Network
- **Reference Code**: Lyapunov analysis and neural network baselines

### 2.3 Key Directories
```
<home>/Desktop/3_body_problem/
├── brutus_Newton-main/          # C++ N-body integrator
├── simulation_data/             # Simulation pipeline and datasets
├── pinn/                        # PINN system and data processing
├── pinn_instruction/            # Instruction and methodology docs
├── paper_templates/             # Documentation templates
├── reference-code/              # Reference implementations
└── ANTIGRAVITY.md               # This file - agent instructions
```

---

## Part 3: Data Pipeline and Dataset Inventory

### 3.1 Pipeline Stages
1. **Stage 1 IC generation**
   - Standard quasi-random (Sobol) and hierarchical ICs.
   - Scripts: `simulation_data/Scripts/ic_generation/FINAL_ic_generator_enhanced.py`, `simulation_data/Scripts/ic_generation/generate_enhanced_ics.py`.
   - Defaults: epsilon=0.05, velocity_scale=0.1, Sobol scrambling enabled.
2. **Stage 2 prescreening**
   - Short leapfrog integration to reject unstable ICs.
   - Script: `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py`.
   - Defaults: TMAX=1.0, DT=0.0001, ENERGY_ERROR_THRESHOLD=0.01, MIN_DISTANCE_THRESHOLD=0.01.
3. **Stage 3 Brutus integration**
   - Main runner: `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py`.
   - Gold-standard hierarchical runner: `simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py`.
   - No in-repo runner for standard quasi-random gold outputs.
   - Timeout: 3000 seconds per simulation in batch scripts.
4. **Metrics**
   - Script: `simulation_data/Scripts/metrics_calculation/calculate_metrics.py`.
5. **PINN preprocessing and stage batching**
   - Script: `pinn/data-processing-pipeline-full.py`.

### 3.2 Dataset Variants (Folder Defines Variant)
- ICs (2 base folders):
  - `simulation_data/Data/ic_final/ic_hierarchical/`
  - `simulation_data/Data/ic_final/ic_standard_quasi_random/`
- Brutus outputs:
  - `simulation_data/Data/brutus_output/brutus_hierarchical/`
  - `simulation_data/Data/brutus_output/brutus_hierarchical_gold_standard/`
  - `simulation_data/Data/brutus_output/brutus_standard_quasi_random/`
  - `simulation_data/Data/brutus_output/brutus_standard_quasi_random_gold_standard/`

**Note:** Gold-standard Brutus output folders exist, but gold IC input folders have been removed. Gold runs read from the base IC folders. The `*_for_gold_standard` IC folders were duplicates and have been deleted.

**ic_raw externalization:** Raw IC storage is external to the repository. Set `IC_RAW_DIR` environment variable before running Stage 1/2 scripts:
```bash
export IC_RAW_DIR=/path/to/ic_raw  # Expected subdirs: ic_hierarchical/, ic_standard_quasi_random/
```

**Mapping rule**: The numeric ID maps IC to Brutus output. File names do **not** encode "gold"; the folder defines the variant.

**Gold-standard subset note**: Standard quasi-random gold Brutus outputs contain 2,565 files while the base IC folder contains 2,749. 184 IDs were not selected for gold-standard re-simulation - see `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` for the complete list.

**ID gaps**: Intentional and caused by generation continuation, prescreen rejection, and failed Brutus runs.

### 3.3 Typical Brutus Parameter Sets (Verify with Result: when present)
- Hierarchical: tol=1e-15, Lw=130, dt_out=0.08.
- Standard quasi-random: tol=1e-13, Lw=118, dt_out=0.17.
- Hierarchical gold: tol=1e-13, Lw=130, dt_out=0.01.
- Standard gold: most commonly tol=1e-13 or 1e-14, Lw=130, dt_out=0.01.

**Note**: Folders can contain multiple parameter sets. Treat these as defaults only. `dt_out` is the output sampling interval, not the internal adaptive step size.

---

## Part 4: Data Formats and Parsing Rules

### 4.1 Initial Condition (IC) File Format
```
m1 x1 y1 z1 vx1 vy1 vz1
m2 x2 y2 z2 vx2 vy2 vz2
m3 x3 y3 z3 vx3 vy3 vz3
```

### 4.2 Brutus Output Format
```
# Snapshot header: t N t_cpu
0.000 3 0.00123
m1 x1 y1 z1 vx1 vy1 vz1
m2 x2 y2 z2 vx2 vy2 vz2
m3 x3 y3 z3 vx3 vy3 vz3

[optional] Result: filename=... N=... t_begin=... t_end=... dt=... eta=... tol=... Lw=... t_cpu=... E_initial=... E_final=... dE/E=...
```
Body lines can contain 30-40 significant digits. Parse as strings or Decimal when exact precision matters.

### 4.3 Mandatory Parsing Rules
1. **Completeness check**: Use final timestamp >= 9.5. Do not rely on `Result:`.
2. **Result footer is optional**: Many files omit it. Treat it as metadata only.
3. **OS-dependent paths**: `Result: filename=` may be macOS or Windows style and can reference multiple IC folders.
4. **t_end varies**: Some runs end at 10.01 or 10.03 when `dt_out` does not divide 10 exactly.

---

## Part 5: Physical Conventions and Key Properties

### 5.1 Units and Dimensionality
- Natural units with **G = 1** and total mass approximately **3**.
- Data is **3D**, not planar.
  - Standard quasi-random can have large |z|.
  - Hierarchical tends to be near-planar due to small inclinations.

### 5.2 Mass and COM Properties
- **Standard quasi-random**: masses are exactly 1.0, COM and total momentum are exactly 0 by construction.
- **Hierarchical**: masses vary but are normalized to total mass ~3. COM and momentum are enforced then **perturbed** with Gaussian noise (sigma=0.01), so COM and total momentum are **not** exactly 0.
  - Recommendation: recenter/reboost before analysis if exact COM frame is required.

### 5.3 Sampling Notes (Standard Quasi-Random)
- p1 fixed at (1, 0, 0); p2 sampled on hemisphere with x <= 0; p3 = -(p1 + p2).
- Velocity components sampled from Normal(0, velocity_scale) via Sobol inverse CDF.
- Global scaling is enabled in `generate_enhanced_ics.py` with `scale_range=(0.8, 1.2)`.
  - Both positions and velocities scale by s.
  - Virial ratio scales as Q ~ s^3.

### 5.4 Sampling Notes (Hierarchical)
- Inner binary semi-major axis: a ~ 0.1-0.3.
- Outer body separation: 3-10x the inner binary separation.
- Small inner inclination; Gaussian perturbations applied to positions and velocities (sigma=0.01).

---

## Part 6: PINN Architecture and Input Vector

### 6.1 Architecture (SQR-SkipResNet-SIREN)
- **Input**: 14 dims (t + 13-component IC vector).
- **Output**: 9 dims (3D positions for 3 bodies).
- **Hidden**: 12 layers, 256 neurons each.
- **SIREN**: first_omega_0=30.0, hidden_omega_0=1.0.
- **Skip**: power p=2, LayerNorm on odd layers (eps=1e-5, elementwise_affine=True).

### 6.2 IC Vector (13 components)
Defined in `pinn/data-processing-pipeline-full.py` as the canonical source of truth:
- m1, m2, m3 (mass fractions, normalized)
- E (normalized)
- L_norm (mapped to [-1, 1])
- Q (normalized)
- s_min (normalized)
- I1, I2, I3 (shape invariants)
- theta1, theta2 (velocity angles)
- I_norm (normalized moment of inertia)

All components are normalized to [-1, 1] prior to training.

**Note**: If comments in `pinn/basic_architecture.py` differ, follow the input-vector logic in `pinn/data-processing-pipeline-full.py`.

---

## Part 7: Command Reference

### 7.1 Build and Run Brutus
```bash
cd brutus_Newton-main
make clean
make

./brutus 1e-15 130 0 10 0.08 3 /abs/path/ic.txt > /abs/path/output.txt
```

### 7.2 Pipeline Execution
```bash
# Generate ICs
python simulation_data/Scripts/ic_generation/generate_enhanced_ics.py

# Stage 2 prescreening
python simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py

# Batch simulations (hierarchical + standard)
python simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py

# Gold-standard hierarchical runs
python simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py

# Metrics extraction
python simulation_data/Scripts/metrics_calculation/calculate_metrics.py
```

### 7.3 PINN Development
```bash
# Architecture sanity check
python pinn/basic_architecture.py

# Data processing (preprocessing + stage batches)
python pinn/data-processing-pipeline-full.py --input /path/to/preprocessed.h5 --output_dir /path/to/stage_data
```

---

## Part 8: Validation and Quality Assurance

### 8.1 Completeness Check
- **Mandatory rule**: final_timestamp >= 9.5.
- Use this before processing any Brutus output.

### 8.2 Conservation Metrics
- `simulation_data/Data/metrics/` contains energy, momentum, and angular momentum drift.
- Escape: max separation > 100.
- Collision: min separation < 0.01.

### 8.3 Provenance and Audit Files
- Prescreening logs:
  - `simulation_data/Validation/prescreening/processing_index_ic_hierarchical.json`
  - `simulation_data/Validation/prescreening/processing_index_ic_standard_quasi_random.json`
- Missing footer audits:
  - `simulation_data/Data/brutus_output/check missing results line/`
- Failed ICs:
  - `simulation_data/Documentation/problematic_ics_blacklist.json`

---

## Part 9: Known Issues and Gotchas

- **Result footer inconsistency**: Optional, missing in many files. Treat as metadata only.
- **Parameter heterogeneity**: Multiple tol, Lw values exist within the same folder. Prefer actual `Result:` values when present, otherwise fallback to folder defaults.
- **Standard gold provenance**: No runner script in repo; treat provenance as partial unless recovered from external logs.
- **OS path variance**: Result footer paths can be macOS or Windows; do not use them as an authoritative mapping.
- **Hierarchical COM offset**: Post-perturbation COM and momentum are not zero; recenter if needed.

---

## Part 10: Quick Reference

### Key Files
- IC Generator: `simulation_data/Scripts/ic_generation/FINAL_ic_generator_enhanced.py`
- Prescreening: `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py`
- Metrics: `simulation_data/Scripts/metrics_calculation/calculate_metrics.py`
- Architecture: `pinn/basic_architecture.py`
- Data Pipeline: `pinn/data-processing-pipeline-full.py`

### Validation Checklist
- [ ] Final timestep >= 9.5
- [ ] Result footer handled (or fallback used)
- [ ] IC file format validated
- [ ] Metrics JSON produced for each output
- [ ] COM/momentum handling chosen explicitly for hierarchical ICs
