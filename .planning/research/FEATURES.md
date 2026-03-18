# Features Research: Physics-Informed LLM for Three-Body Prediction

## Table Stakes (Must Have)

### Codebase Cleanup
- **IC folder consolidation** — Remove duplicate gold IC folders (byte-identical)
- **Raw IC externalization** — Move `ic_raw/` out of repo, configurable path
- **Documentation updates** — All docs reflect post-cleanup layout
- **Subset-aware validation** — Handle 184-ID gap in standard-gold correspondence

### Data Pipeline
- **End-to-end preprocessing** — IC files → normalized training data (exists, needs verification)
- **Training data format conversion** — Simulation data → JSONL for LLM training (new)
- **Data validation** — Conservation metrics, completeness checks (exists)

### LLM Fine-Tuning
- **LoRA fine-tuning script** — Train Qwen 3.5 2B on trajectory data via mlx-lm
- **Training/validation split** — Proper held-out test set from simulation IDs
- **Loss monitoring** — Track training loss and convergence

## Differentiators (Competitive Advantage)

### Enhanced Prediction Quality
- **Physics-informed loss** — Add conservation law penalties to training loss
- **Curriculum training** — Start with simple (near-integrable) trajectories, progress to chaotic
- **Multi-resolution training** — Train on both standard and gold-standard (high-resolution) data

### Evaluation
- **Trajectory accuracy metrics** — MSE, energy conservation error on predicted trajectories
- **Comparison with PINN** — Benchmark LLM predictions against PINN architecture
- **Generalization testing** — Test on unseen IC configurations

## Anti-Features (Do NOT Build)

| Feature | Why Not |
|---------|---------|
| Web UI for predictions | Research project, not a product |
| Real-time inference API | Focus on training quality first |
| Multi-body (N>3) support | Out of scope; different dynamics |
| Qualitative physics reasoning | Numerical prediction is the core goal |

## Feature Dependencies

```
Codebase Cleanup (independent)
    ↓
Data Pipeline Verification → Training Data Format Conversion
    ↓
LoRA Fine-Tuning Script → Loss Monitoring
    ↓
Evaluation Metrics → Comparison with PINN
```
