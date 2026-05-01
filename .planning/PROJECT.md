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
- ✓ Consolidate 7 issue reports into 3 thematic documents with migration tracking — Phase 9

### Active

<!-- Current scope. Building toward these. -->

- [ ] **MD-CONV-01**: Data-quality-assessment markdown matches LaTeX source with one-to-one injection fidelity
- [ ] **MD-CONV-02**: ctl-instruction markdown matches LaTeX source with one-to-one injection fidelity
- [ ] **MD-CONV-03**: pinn-architecture markdown matches LaTeX source with one-to-one injection fidelity
- [ ] **MD-CONV-04**: review_of_framework markdown matches LaTeX source with one-to-one injection fidelity
- [ ] **MD-CONV-05**: stage_strat_revision markdown matches LaTeX source with one-to-one injection fidelity
- [ ] **MD-CONV-06**: sampling-method markdown matches LaTeX source with one-to-one injection fidelity

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
- Resolving inconsistencies between LaTeX instruction documents — this milestone preserves them faithfully; cross-document reconciliation is a separate future task

## Current Milestone: v1.3 Markdown Conversion Verification & Correction

**Goal:** Verify every markdown conversion against its LaTeX source section-by-section (leveraging the modular split), fix all errors to achieve one-to-one injection fidelity, and produce one authoritative `.md` file per source document.

**Target features:**
- 6 authoritative markdown files, one per LaTeX source, with exact content match
- Mathematical formulas faithfully converted (LaTeX → markdown math notation)
- All cross-references, citations, figure/table references preserved correctly
- Commented-out LaTeX sections excluded from markdown
- Duplicate/unselected markdown files identified and handled
- Inter-document inconsistencies preserved (not resolved — that's a separate task)

**Scope:** 6 LaTeX sources in `pinn_instruction/original_latex/`:
1. `Data-quality-assessment/` (7 sections)
2. `ctl-instruction/` (8 sections)
3. `pinn-architecture/` (7 active + 3 inactive sections)
4. `review-of-framework/review_of_framework/` (7 sections)
5. `review-of-framework/stage_strat_revision/` (6 sections)
6. `sampling-method/` (monolithic — 1 file)

**Phase structure:** 6 phases (one per source), each doing: pick best candidate → audit section-by-section → fix discrepancies → verify one-to-one match.

**Prerequisite:** Complete v1.2 Phase 9 (Issues Directory Consolidation) before executing v1.3 phases.

### Previous Milestones

**v1.2 PINN Implementation Readiness** (in progress)
- Phase 9: Issues Directory Consolidation — 3 thematic docs + MIGRATION.md + README.md written, pending final verification

**v1.1 LaTeX Modularization Verification** (shipped 2026-03-22)
- Phases 5-8: Content completeness, preamble parity, structure fidelity, compilability — all passed

**v1.0 Codebase Cleanup** (shipped 2026-03-20)
- Phases 1-4: Code rewrites, documentation, data deletion, stale references

## Context

- Brutus generates trajectories with 30-40 significant digit precision, G=1 natural units
- Two IC types: standard quasi-random (equal masses, Sobol sampling) and hierarchical (variable masses, orbital elements)
- Four dataset variants per type: standard and gold-standard (higher-resolution output)
- Gold IC folders were removed (duplicates) — gold Brutus outputs remain
- Raw ICs externalized via IC_RAW_DIR environment variable
- Standard quasi-random gold subset excludes 184 IDs (see `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md`)
- Existing PINN approach (SQR-SkipResNet-SIREN) relationship to new LLM direction is TBD
- Qwen 3.5 2B 4-bit model already downloaded at `Qwen3.5-2B-4bit/`
- 5 of 6 LaTeX sources are modular (split into sections/); sampling-method is monolithic
- Markdown conversions exist in two locations: `markdown_conversion/` (top-level) and `markdown_conversion/pandoc_conversion/`
- Some sources have 2-3 competing markdown conversions; the best candidate must be selected before editing

## Constraints

- **Hardware**: M2 Mac development machine — limits model size and training speed
- **Model**: Qwen 3.5 2B 4-bit — chosen for local training feasibility on M2
- **Data format**: Brutus outputs are high-precision text files, not natively LLM-friendly
- **Dependencies**: No `requirements.txt` exists — environment management needed
- **One-to-one injection**: Markdown must match LaTeX source exactly; inter-document inconsistencies are preserved, not resolved
- **Commented-out content**: LaTeX `\begin{comment}...\end{comment}` blocks (not author comments) are excluded from markdown

## Key Decisions

<!-- Decisions that constrain future work. Add throughout project lifecycle. -->

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Fine-tune Qwen 3.5 2B for trajectory prediction | Small enough to train locally on M2 Mac | — Pending |
| Clean up codebase before LLM work | Data integrity is the foundation; cleanup simplifies downstream pipeline | ✓ v1.0 shipped (Phases 1-4) |
| Verify LaTeX modularization before LLM work | Ensure documentation integrity for future reference | ✓ v1.1 shipped (Phases 5-8) |
| PINN vs LLM approach | PINN architecture exists but no training loop; LLM is the new direction | — Pending |
| Numerical trajectory output (not qualitative) | Core use case is trajectory prediction from ICs | — Pending |
| Verify markdown conversions before cross-document reconciliation | Must first ensure each markdown is a faithful copy of its LaTeX source; find inconsistencies later | ✓ v1.3 defined |
| One phase per LaTeX source (6 phases) | Keeps each phase scoped to one document; avoids context-switching across different content | ✓ v1.3 defined |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-30 — v1.3 milestone defined*
