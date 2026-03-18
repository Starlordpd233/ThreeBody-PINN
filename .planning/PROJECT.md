# Three-Body Physics-Informed LLM

## What This Is

A research project that generates high-precision three-body gravitational simulation data using the Brutus N-body integrator, and uses that data to fine-tune a language model (Qwen 3.5 2B) that can predict three-body trajectories numerically given initial conditions. The project spans the full pipeline from simulation data generation through to LLM training.

## Core Value

The simulation dataset and data pipeline must be clean, well-validated, and correctly processed — everything downstream (PINN or LLM training) depends on data integrity.

## Requirements

### Validated

<!-- Shipped and confirmed valuable. -->

- ✓ Brutus N-body integrator compiles and runs on macOS (C++, GMP/MPFR) — existing
- ✓ IC generation for standard quasi-random and hierarchical configurations (Sobol + orbital elements) — existing
- ✓ Stage 2 prescreening rejects unstable ICs via short leapfrog integration — existing
- ✓ Batch Brutus runners for both IC types with timeout handling — existing
- ✓ Conservation metrics extraction (energy, momentum, angular momentum) — existing
- ✓ Dataset documentation with completeness checks and provenance tracking — existing
- ✓ PINN architecture defined (SQR-SkipResNet-SIREN, 14→256×12→9) — existing
- ✓ Data processing pipeline computes 13-component IC vector with normalization — existing

### Active

<!-- Current scope. Building toward these. -->

- [ ] Codebase cleanup: consolidate duplicate IC folders (gold → non-gold)
- [ ] Codebase cleanup: remove in-repo raw ICs, externalize raw IC paths
- [ ] Codebase cleanup: add subset-aware standard-gold validation (184-ID gap)
- [ ] Codebase cleanup: update all documentation to reflect post-cleanup layout
- [ ] Codebase cleanup: delete legacy folders and build artifacts
- [ ] Data pipeline: get PINN training loop working end-to-end (architecture exists, training does not)
- [ ] LLM fine-tuning: prepare simulation data for language model training format
- [ ] LLM fine-tuning: fine-tune Qwen 3.5 2B on three-body trajectory prediction

### Out of Scope

<!-- Explicit boundaries. Includes reasoning to prevent re-adding. -->

- Modifying Brutus C++ integrator — it works, no changes needed
- `.git/lfs/` pruning or repository size reduction — separate concern
- Real-time prediction API or web interface — research project, not a product
- Qualitative reasoning by the LLM — focus is on numerical trajectory prediction first

## Context

- Brutus generates trajectories with 30-40 significant digit precision, G=1 natural units
- Two IC types: standard quasi-random (equal masses, Sobol sampling) and hierarchical (variable masses, orbital elements)
- Four dataset variants per type: standard and gold-standard (higher-resolution output)
- Gold IC folders are byte-identical duplicates/subsets of standard IC folders → cleanup target
- Existing PINN approach (SQR-SkipResNet-SIREN) relationship to new LLM direction is TBD
- Qwen 3.5 2B 4-bit model already downloaded at `Qwen3.5-2B-4bit/`
- Revised cleanup plan exists at `docs/plans/cleaning-3-body.md`

## Constraints

- **Hardware**: M2 Mac development machine — limits model size and training speed
- **Model**: Qwen 3.5 2B 4-bit — chosen for local training feasibility on M2
- **Data format**: Brutus outputs are high-precision text files, not natively LLM-friendly
- **Dependencies**: No `requirements.txt` exists — environment management needed

## Key Decisions

<!-- Decisions that constrain future work. Add throughout project lifecycle. -->

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Fine-tune Qwen 3.5 2B for trajectory prediction | Small enough to train locally on M2 Mac | — Pending |
| Clean up codebase before LLM work | Data integrity is the foundation; cleanup simplifies downstream pipeline | — Pending |
| PINN vs LLM approach | PINN architecture exists but no training loop; LLM is the new direction | — Pending |
| Numerical trajectory output (not qualitative) | Core use case is trajectory prediction from ICs | — Pending |

---
*Last updated: 2026-03-18 after initialization*
