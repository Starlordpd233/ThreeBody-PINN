# GEMINI.md: Enhanced Instructions for Gemini Code Agent

## Part 1: Core AI Assistant Guidelines

### 1.1 Core Behavior and Response Principles
- Be accurate, concise, and reliable; prioritize correctness over speed or flair.
- Use conversation context; resolve tasks fully and confirm assumptions when needed.
- If uncertain, use tools or ask for clarification; never fabricate.
- Plan before actions and large code edits; keep steps crisp and ordered.
- Communicate clearly with essential details and examples when they help.
- Admit unknowns directly; avoid filler or rote phrasing.
- Use markdown for structure and LaTeX for math when helpful.
- Distinguish facts from assumptions or speculation; cite sources or files.
- IMPORTANT: Use "Let's think step by step" for complex reasoning.

### 1.2 Code Style and Best Practices
- Follow existing style and patterns in the repo.
- Favor readability and correctness; handle edge cases and input validation.
- Add error handling where failure is plausible.
- Offer alternatives when tradeoffs exist; call out ambiguities.
- Provide tests or validation steps when feasible.

### 1.3 Workflow Guidelines
- Default flow: Explore -> Plan -> Implement -> Verify.
- For large tasks, create a checklist and work sequentially.
- Use test-driven development when it improves safety or clarity.
- For UI or visualization tasks, iterate visually and verify against targets.
- For codebase Q and A, search code before answering.
- Course correct quickly if assumptions are wrong; re-plan when needed.
- Use a quick second pass or verification sweep for critical changes.

### 1.4 Mathematics and Science
- Show steps with explicit assumptions and methodology.
- Double-check calculations and sanity-check results.
- Use LaTeX for formulas (for example: $$ \int_a^b f(x) \, dx $$).
- Provide confidence levels when uncertainty remains.

### 1.5 Writing and Essays
- Provide analytical, well-structured responses with clear reasoning.
- Match the user's tone and intent; prefer substance over fluff.

### 1.6 Document Analysis and Extraction
- Quote exact text with citations and preserve context.
- Cross-check sources and note contradictions.

### 1.7 Research and Information Gathering
- Use tools for current or external information; cite sources.
- Be specific in queries and include relevant paths or URLs.

### 1.8 Available Tools and Customization
- Use the tool interface and permissions provided by the runtime.
- Do not fabricate tool output; retrieve data before summarizing.
- Adapt responses to user preferences and local project conventions.

## Part 2: Three-Body Problem Project Architecture

### 2.1 Project Overview and Components
This repository implements a complete three-body simulation and CTL-PINN training stack:
- High-precision N-body integration with Brutus (C++).
- A Python data pipeline for IC generation, prescreening, simulation, and metrics.
- A CTL-PINN system with curriculum stages and HDF5-based datasets.
- Paper templates documenting the CTL-PINN methodology and architecture.
- Reference implementations for Lyapunov analysis and neural network baselines.

### 2.2 Brutus N-body Simulator (brutus_Newton-main/)
- Language: C++ with GMP and MPFR for arbitrary precision.
- Build config: brutus_Newton-main/makefile (Homebrew paths and mpreal include).
- Core files: Brutus.cpp, Bulirsch_Stoer.cpp, Cluster.cpp, Star.cpp, Data_Handler.cpp, Timer.cpp.
- CLI signature:
  ./brutus <tolerance> <word_length> <t_begin> <t_end> <dt_out> <N> <input_ic.txt>

### 2.3 Three-Body Problem Pipeline (3_Body_Problem/)
- IC generation: FINAL_ic_generator_enhanced.py and generate_enhanced_ics.py (Sobol-based sampling).
- Prescreening: prescreen_stage2/stage2_prescreening_revised_auto.py.
- Simulation: run_brutus_both_type_simple.py and run_brutus_hierarchical_only_mac_gold_standard.py.
- Metrics: brutus_metrics/calculate_metrics.py (energy, momentum, angular momentum, escape/collision flags).
- Key directories:
  - ic_raw_datasets/, prescreen_stage2/, final_stage_ic_datasets/
  - brutus_output/, brutus_metrics/, problematic_ics/

### 2.4 PINN System (pinn/)
- Architecture: basic_architecture.py (SQR-SkipResNet-SIREN).
- Data pipeline: data-processing-pipeline-full.py (parsing, scaling, invariants, stages, IC vectors, HDF5, training batches).
- Input is time plus a 13-component IC vector; output is 3D positions for three bodies.

### 2.5 Paper Templates (paper_templates/)
- CTL instruction: paper_templates/pinn_instruction/CTL-instruction-final.tex.
- Architecture plan: paper_templates/pinn_instruction/markdown_conversions/PINN_architecture_plan.md.
- MDPI and review templates in paper_templates/mdpi_template/ and paper_templates/review-of-framework/.

### 2.6 Reference Code (reference-code/)
- Lyapunov analysis: reference-code/lyapunov/.
- Neural network baselines: reference-code/reference_NNs/.

## Part 3: Essential Development Commands

### 3.1 Building and Running Brutus Simulator
```bash
cd brutus_Newton-main
make clean
make
```

```bash
# Single run example (hierarchical parameters)
./brutus 1e-15 130 0 10 0.08 3 /abs/path/ic.txt > /abs/path/output.txt
```

### 3.2 Pipeline Execution Commands
```bash
# Generate ICs
python 3_Body_Problem/generate_enhanced_ics.py

# Stage 2 prescreening
python 3_Body_Problem/prescreen_stage2/stage2_prescreening_revised_auto.py

# Batch simulations (hierarchical + standard)
python 3_Body_Problem/run_brutus_both_type_simple.py

# Gold-standard hierarchical runs (dt_out=0.01)
python 3_Body_Problem/run_brutus_hierarchical_only_mac_gold_standard.py

# Metrics extraction
python 3_Body_Problem/brutus_metrics/calculate_metrics.py
```

### 3.3 PINN Development and Training
```bash
# Architecture sanity check
python pinn/basic_architecture.py

# Prepare CTL-PINN training data (stage batches)
python pinn/data-processing-pipeline-full.py --input /path/to/preprocessed.h5 --output_dir /path/to/stage_data
```
Note: pinn/data-processing-pipeline-full.py also contains a scripts/preprocess_dataset.py section that writes the preprocessed HDF5. Extract that section into a standalone script or rename the entry point when you need to run preprocessing.

## Part 4: Data Flow and Formats

### 4.1 Complete Pipeline Workflow
IC Generation -> Stage 2 Prescreen -> Brutus Simulation -> Metrics -> CTL-PINN Processing -> Stage Batches

Key flow notes:
- ICs live under 3_Body_Problem/final_stage_ic_datasets/.
- Outputs land in 3_Body_Problem/brutus_output/.
- Metrics JSON files land in 3_Body_Problem/brutus_metrics/.
- CTL-PINN preprocessing produces HDF5 plus per-stage batch files.
- Preprocessing logic lives in the scripts/preprocess_dataset.py section inside pinn/data-processing-pipeline-full.py.

### 4.2 Initial Condition File Format
```
mass1 x1 y1 z1 vx1 vy1 vz1
mass2 x2 y2 z2 vx2 vy2 vz2
mass3 x3 y3 z3 vx3 vy3 vz3
```

### 4.3 Brutus Output Format
```
# Each snapshot starts with: time N cpu_time
0.000 3 0.00123
m1 x1 y1 z1 vx1 vy1 vz1
m2 x2 y2 z2 vx2 vy2 vz2
m3 x3 y3 z3 vx3 vy3 vz3
```

### 4.4 PINN Input Vector (13 components)
The IC vector is normalized to [-1, 1] and concatenated with time t to form a 14D input.
Components (in order):
- m1, m2, m3 (mass fractions normalized)
- E (energy, normalized)
- L_norm (angular momentum, mapped to [-1, 1])
- Q (virial ratio, normalized)
- s_min (minimum separation, normalized)
- I1, I2, I3 (shape invariants)
- theta1, theta2 (velocity angles)
- I_norm (normalized moment of inertia)

## Part 5: Precision and Performance Settings

### 5.1 Brutus Simulator Parameters
- Hierarchical (run_brutus_both_type_simple.py): tol=1e-15, word_length=130, dt_out=0.08.
- Standard quasi-random: tol=1e-13, word_length=118, dt_out=0.17.
- Gold standard hierarchical: tol=1e-13, word_length=130, dt_out=0.01.
- Timeout per run: 3000 seconds.

### 5.2 PINN Architecture Specifications
- Model: SQR-SkipResNet-SIREN.
- Input dim: 14 (t + 13 IC components).
- Output dim: 9 (3D positions for 3 bodies).
- Hidden layers: 12 layers, 256 neurons each.
- SIREN omega_0: first=30.0, hidden=1.0.
- Skip power: p=2, LayerNorm on odd layers (eps=1e-5, elementwise_affine=True).

### 5.3 Memory and Performance Considerations
- Brutus outputs can be large; monitor brutus_output/ sizes.
- Parallel runs use CPU count minus one (see ProcessPoolExecutor usage).
- HDF5 datasets and per-stage batches can be large; ensure disk headroom.

## Part 6: Critical Implementation Details

### 6.1 Brutus Integration Method
- Bulirsch-Stoer integration with variable timestep and arbitrary precision.
- GMP/MPFR required; paths configured in brutus_Newton-main/makefile.

### 6.2 IC Generation Details
- Sobol sampling with scrambling (scipy.stats.qmc.Sobol).
- Epsilon default: 0.05, velocity_scale default: 0.1.
- Velocity sampling uses inverse CDF of a normal distribution.
- Hierarchical ICs enforce inner binary a ~ 0.1-0.3 and outer body at 3-10x separation.
- Momentum conservation via symmetric velocity assignment (v1 = -v2/2, v3 = -v2/2).

### 6.3 Curriculum Learning Implementation
Stages 0-6 are assigned from physical invariants in pinn/data-processing-pipeline-full.py:
- Stage 0: easiest hierarchical (E < -0.5, L_norm > 0.5, 0.7 <= Q <= 1.3, s_min > 2).
- Stage 1: relaxed hierarchical (energy or angular momentum relaxed).
- Stage 2: all high-fidelity hierarchical data.
- Stage 3: moderately chaotic low-fidelity (based on dataset quantiles E_25 and L_75).
- Stage 4: chaotic low-fidelity (tau_L thresholds).
- Stage 5: high-fidelity chaotic.
- Stage 6: extreme cases (s_min < 0.5 or |E| < 0.01).

## Part 7: Common Issues and Solutions

### 7.1 Brutus Compilation Issues
- Ensure BREW_PREFIX and MPRLIB are correct in brutus_Newton-main/makefile.
- Required libs: gmp, gmpxx, mpfr.

### 7.2 Simulation Timeouts and Failures
- TIMEOUT_SECONDS is 3000; failures move ICs to problematic_ics/.
- Validate output by checking final timestep >= 9.5 in batch scripts.

### 7.3 Data and File Layout Issues
- Ensure IC names follow ic_<type>_NNNN.txt conventions.
- Ensure brutus output naming matches expected patterns in calculate_metrics.py.

### 7.4 PINN Training Instability
- Check normalization scales and IC vector ranges.
- Reduce batch size or adjust curriculum progression if NaNs occur.

## Part 8: Validation and Quality Assurance

### 8.1 Conservation Metrics
- Use 3_Body_Problem/brutus_metrics/calculate_metrics.py to compute energy, linear momentum, and angular momentum drift.
- Escape/collision heuristics: max separation > 100 or min separation < 0.01.

### 8.2 Code Quality Standards
- C++: const-correctness, RAII, and safe memory handling.
- Python: PEP 8, type hints where feasible, clear docstrings.

### 8.3 Testing Strategy
- Validate Brutus outputs with timestep checks.
- Run small IC subsets before large batches.
- For CTL-PINN, verify stage counts and dataset stats after preprocessing.

## Part 9: Development Workflow Best Practices

### 9.1 Setup and Environment
```bash
brew install gmp mpfr
# Ensure mpreal is available at <home>/src/mpreal
```

### 9.2 Iterative Development
- Use small, frequent runs (see HIERARCHICAL_ICS_PER_RUN and STANDARD_ICS_PER_RUN).
- Confirm outputs before expanding batch sizes.

### 9.3 Data Processing Pipeline
- Generate ICs -> Prescreen -> Simulate -> Metrics -> Preprocess -> Stage batches.
- Maintain separation between hierarchical and quasi-random datasets.

### 9.4 Performance Optimization
- Tune tolerance and dt_out per dataset type.
- Use parallel processing for Brutus runs.
- Monitor disk usage and rotate outputs if needed.

## Part 10: File Organization Patterns

```
brutus_Newton-main/
  makefile
  Brutus.cpp
  Bulirsch_Stoer.cpp
  Cluster.cpp
  Star.cpp
  lib/Timer/
  lib/Data_Handler/

3_Body_Problem/
  FINAL_ic_generator_enhanced.py
  generate_enhanced_ics.py
  prescreen_stage2/
  final_stage_ic_datasets/
  brutus_output/
  brutus_metrics/
  problematic_ics/
  debug_scripts/

pinn/
  basic_architecture.py
  data-processing-pipeline-full.py
  data-handling/

paper_templates/
  pinn_instruction/
  mdpi_template/
  review-of-framework/

reference-code/
  lyapunov/
  reference_NNs/
```

## Part 11: Debugging and Troubleshooting

### 11.1 Common Error Patterns
- Missing libraries or include paths during Brutus builds.
- Partial or missing Brutus outputs from timeouts.
- Mismatched dataset types between ICs and outputs.

### 11.2 Diagnostic Commands
```bash
# Brutus build log
cd brutus_Newton-main && make clean && make 2>&1 | tee build.log

# Check brute-force output completeness
python 3_Body_Problem/debug_scripts/check_brutus_completeness.py
```

### 11.3 Validation Procedures
- Confirm final timestep >= 9.5 for completed runs.
- Verify metrics JSON files are produced for each output.

## Part 12: Advanced Features and Extensions

### 12.1 Parallel Processing
- run_brutus_both_type_simple.py uses ProcessPoolExecutor with (cpu_count - 1) workers.

### 12.2 Curriculum Learning Details
- Curriculum replay is supported in stage batch preparation (include_previous default).
- Stage thresholds are adjustable in processing/stage_assignment.py sections inside data-processing-pipeline-full.py.

### 12.3 High-Performance Computing
- Use batch scheduling where available and keep outputs staged by dataset type.
- Consider HDF5 chunking or compression for large datasets.

## Part 13: Security and Safety Considerations

### 13.1 Input Validation
- Validate IC file formats before simulation.
- Sanitize paths when moving or archiving outputs.

### 13.2 Numerical Stability
- Monitor conservation metrics for drift.
- Use gold-standard runs for spot checks when needed.

## Part 14: Collaboration and Version Control

### 14.1 Git Workflow
- Use feature branches and descriptive commits.
- Keep data generation and large outputs out of version control.

### 14.2 Code Review Standards
- Review for numerical correctness and performance regressions.
- Verify pipeline steps and dataset naming conventions.

## Part 15: Performance Monitoring

### 15.1 Key Metrics
- Simulation throughput (trajectories per hour).
- Energy and angular momentum drift.
- Data processing throughput and dataset sizes.

### 15.2 Profiling Tools
- Use cProfile for Python scripts and build logs for Brutus.

## Part 16: Emergency Procedures

### 16.1 Data Recovery
- Backup ic_raw_datasets/, final_stage_ic_datasets/, brutus_output/.
- Keep problematic_ics/ and blacklist JSON for reruns.

### 16.2 System Failure Recovery
- Resume with start_from_last=True for IC generation.
- Re-run batch scripts on remaining ICs.

## Part 17: Customization Notes

### 17.1 Environment-Specific Settings
- macOS paths are baked into makefile and scripts; update if moving hosts.
- Adjust BRUTUS_EXEC and BASE_DIR in scripts if paths change.

### 17.2 User Preferences
- Keep commands and outputs reproducible; document any local overrides.

## Part 18: Research and Reproducibility

### 18.1 Experiment Tracking
- Track seeds for Sobol sampling and IC generation.
- Record Brutus parameters and dataset identifiers per run.

### 18.2 Computational Experiments
- Use curriculum stages to structure experiments and comparisons.
- Preserve HDF5 datasets and stage batch summaries for reproducibility.
