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
- ✓ Codebase cleanup: consolidated IC folders (removed gold IC duplicates) — Phase 1
- ✓ Codebase cleanup: externalized raw ICs via IC_RAW_DIR environment variable — Phase 1
- ✓ Codebase cleanup: 184-ID gold subset validation via exclusion file — Phase 1
- ✓ Documentation: all files updated for post-consolidation layout — Phase 2
- ✓ Codebase cleanup: deleted legacy folders and build artifacts — Phase 3
- ✓ Codebase cleanup: fixed all stale code imports and documentation filename references — Phase 4
- ✓ Verify modular LaTeX content completeness (automated diff script) — Phase 5
- ✓ Verify preamble parity (packages, macros, commands) across all 5 modular structures — Phase 6
- ✓ Verify document structure fidelity (sections, labels, refs, citations, floats) — Phase 7
- ✓ Verify compilability of all 5 modular structures (0 errors, 0 new warnings) — Phase 8

### Active

<!-- Current scope. Building toward these. -->

- None — v1.1 milestone complete

### Deferred

- [ ] Data pipeline: get PINN training loop working end-to-end (architecture exists, training does not)
- [ ] LLM fine-tuning: prepare simulation data for language model training format
- [ ] LLM fine-tuning: fine-tune Qwen 3.5 2B on three-body trajectory prediction

### Out of Scope

<!-- Explicit boundaries. Includes reasoning to prevent re-adding. -->

- Modifying Brutus C++ integrator — it works, no changes needed
- `.git/lfs/` pruning or repository size reduction — separate concern
- Real-time prediction API or web interface — research project, not a product
- Qualitative reasoning by the LLM — focus is on numerical trajectory prediction first

## Current Milestone: v1.1 LaTeX Modularization Verification — COMPLETE

**Goal:** Rigorously verify that 5 modular LaTeX structures faithfully preserve the content, style, format, and components of their original monolithic LaTeX files.

**Target features:**
- ✓ Automated Python diffing scripts comparing original vs concatenated modular sections
- ✓ Content completeness verification (no dropped text)
- ✓ Preamble parity checks (packages, macros, commands)
- ✓ Structure fidelity checks (section hierarchy, labels, refs, citations)
- ✓ Compilability verification (0 errors, 0 new warnings)

**Scope:** 5 structures in `pinn_instruction/original_latex/`:
1. Data-quality-assessment (`data_quality_assess.tex` → `data_quality_assess/`)
2. ctl-instruction (`CTL-instruction-final.tex` → `ctl-instruction/`)
3. pinn-architecture (`PINN_architecture_plan.tex` → `pinn-architecture/`)
4. review-of-framework (`review_of_ctl-pinn_framework.tex` → `review_of_framework/`)
5. review-of-framework (`stage-strat-revision.tex` → `stage_strat_revision/`)

**Excluded:** `sampling-method/` (no modular structure exists)

**Status:** All 4 phases complete, all 5 plans executed, all 13 requirements satisfied.

## Context

- Brutus generates trajectories with 30-40 significant digit precision, G=1 natural units
- Two IC types: standard quasi-random (equal masses, Sobol sampling) and hierarchical (variable masses, orbital elements)
- Four dataset variants per type: standard and gold-standard (higher-resolution output)
- Gold IC folders were removed (duplicates) — gold Brutus outputs remain
- Raw ICs externalized via IC_RAW_DIR environment variable
- Standard quasi-random gold subset excludes 184 IDs (see `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md`)
- Existing PINN approach (SQR-SkipResNet-SIREN) relationship to new LLM direction is TBD
- Qwen 3.5 2B 4-bit model already downloaded at `Qwen3.5-2B-4bit/`

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
| Clean up codebase before LLM work | Data integrity is the foundation; cleanup simplifies downstream pipeline | ✓ v1.0 shipped (Phases 1-4) |
| Verify LaTeX modularization before LLM work | Ensure documentation integrity for future reference | ✓ v1.1 shipped (Phases 5-8) |
| PINN vs LLM approach | PINN architecture exists but no training loop; LLM is the new direction | — Pending |
| Numerical trajectory output (not qualitative) | Core use case is trajectory prediction from ICs | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd:transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-22 after Phase 8 (Compilability Verification) completed*
