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
- ✓ **MD-CONV-02**: ctl-instruction markdown matches LaTeX source with one-to-one injection fidelity — Phase 10
- ✓ **MD-CONV-01**: data-quality-assessment markdown matches LaTeX source with one-to-one injection fidelity — Phase 11
- ✓ **MD-CONV-03**: pinn-architecture markdown matches LaTeX source with one-to-one injection fidelity — Phase 12
- ✓ **MD-CONV-04**: review_of_framework markdown matches LaTeX source with one-to-one injection fidelity — Phase 13
- ✓ **MD-CONV-05**: stage_strat_revision markdown matches LaTeX source with one-to-one injection fidelity — Phase 14
- ✓ **MD-CONV-06**: sampling-method markdown matches LaTeX source with one-to-one injection fidelity — Phase 15
- ✓ Post-v1.3 SCS gate correction: data-quality-assessment now distinguishes raw Hamiltonian drift `\epsilon_H` from logarithmic `SCS`, and the gate is `\epsilon_H > 10^{-5}` / `SCS > -5`

### Active

<!-- Current scope. Building toward these. -->

- [ ] Critically examine each Issue 01 finding against BOTH `ctl_pinn_resolution.md` AND `01-architecture-and-physics-foundations.md` (neither treated as authoritative); for every conflict, identify the root-cause ambiguity in the framework specs and lock the convention explicitly before any spec edit
- [ ] Patch framework specs only after each issue has an evidence-backed verdict and a named acceptance check
- [ ] Preserve the SQR-SkipResNet-SIREN, CTL, and raw-mass framework decisions unless the evidence disproves them
- [ ] Record traceable evidence for every architecture and physics foundation correction
- [ ] Execute (not just document) acceptance checks via disposable validation probes: scaling consistency, COM invariance, componentwise AD correctness, force-energy consistency, loss-stability dry run — failing checks block milestone close-out, but do not authorize production framework implementation
- [ ] Close each finding through an iterative re-verification loop (`PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED`); "fix applied" is not closure, only a passing acceptance check is

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
- Broad cross-document reconciliation beyond the shipped SCS gate correction and active v1.4 Issue 01 scope
- Editing existing `pinn/` implementation files to match the revised framework specs — code alignment happens after v1.4

## Current Milestone: v1.4 Resolving 01 Architecture and Physics Foundations

**Goal:** Critically examine each Issue 01 finding against BOTH `ctl_pinn_resolution.md` AND `01-architecture-and-physics-foundations.md` — treating neither as authoritative — to identify the root-cause ambiguity in the current framework specs, lock the right convention, apply evidence-backed framework-spec edits, and **verify each fix with disposable acceptance checks** before closing the issue. v1.4 settles the framework documentation; it does not implement or update the production PINN/training code.

**Target features:**
- Evidence packets for each issue before edits: spec evidence, issue-report evidence, resolution-doc verdict, first-principles checks where required, and an explicit verdict from `{accept-resolution, accept-issue-doc, accept-third-position, reject-both-as-unsupported, defer-with-blocker}`. Live PINN-side code is not v1.4 evidence or grounding.
- For every contested finding (B-02, B-04, B-09, M5, and any further conflict discovered during the walkthrough), an EVID-05 record that names the underlying spec ambiguity and the convention now locked.
- Framework-spec revisions in `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`, `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`, and the narrow `sampling_method.md` sections needed for FRAME-03.
- Live code in `pinn/basic_architecture.py` and `pinn/data-processing-pipeline-full.py` is **NOT** used as evidence or grounding source for any v1.4 decision (directive 2026-05-19). It is v1.3-era artifact; FUT-01 will rebuild from the v1.4 specs. Live-code references are permitted only in forward-pointing FUT-01 hand-off documents (`NN-CODE-DIVERGENCE.md`, eventual `pinn/STATUS.md`).
- Disposable validation probes for scaling consistency, COM invariance, componentwise AD on the synthetic trajectory, force-energy consistency, and loss stability — failing probes loop back to the originating spec phase.
- Iterative re-verification: each finding moves through `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED` in `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md`; nothing closes on "fix applied," only on a passing acceptance check.
- Reconciled `SI-*` ledger: every v1.4-resolved finding retires its corresponding spec source-issue entry; `SI-DQA-002`/`SI-DQA-003`/`SI-PINN-002` are preserved untouched.
- Requirements and roadmap begin at Phase 16, after v1.3 ended at Phase 15.1 and the post-ship SCS gate correction shipped 2026-05-15. Phases 16, 17, and 18 are complete; the next logical workflow step is `$gsd-discuss-phase 19`.

**Primary sources:**
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md` — most recent candidate adjudication; not treated as authoritative
- `pinn_instruction/issues/01-architecture-and-physics-foundations.md` — thematic issue consolidation; not treated as authoritative

**Supporting evidence:**
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/master_consolidation_report.md` — earlier multi-AI consolidation already consumed by the resolution doc; read for traceability and verification, not as a primary verdict source
- Individual model reports (`chatgpt_research_report.md`, `claude_research_report.md`, `claude_research_report_2.md`, `gemini_research_report.md`) — consult only when adjudicating a finding the consolidation map records as ambiguous (e.g., M6/M7)
- Brutus C++ integrator + IC generation / prescreening scripts: read-only reference for dataset / simulation-side first-principles checks. **The PINN-side live code (`pinn/basic_architecture.py`, `pinn/data-processing-pipeline-full.py`) is NOT in this supporting-evidence set** — per directive 2026-05-19 it is v1.3-era artifact, not used as evidence during v1.4.

**Scope:** Architecture and physics foundation corrections only. Data-pipeline, curriculum-stage, PINN implementation, and LLM fine-tuning work remain deferred. v1.4 may create or record disposable validation probes only to test risky framework contracts before the specs are locked. The SCS gate work that previously sat under data-quality-assessment is complete and out of v1.4 scope.

**Phase structure:** 6 core phases in `.planning/ROADMAP.md` (Phases 16–21), plus inserted Phase 20.5 for Sampling Coordinate Allocation before Phase 21. 30 original v1.4 requirements remain mapped 1:1 to phases; Phase 20.5 carries its own design/plan handoff. The verification protocol and iterative re-verification loop are encoded as requirements (VER-04/05/06) and roadmap protocol rather than separate phases.

### Previous Milestones

**v1.3 Markdown Conversion Verification & Correction** (complete — shipped 2026-05-08)
- Phases 10-15 and 15.1: Verified all six LaTeX-to-markdown conversions, corrected audit gaps, and preserved inter-document inconsistencies for later reconciliation.
- Post-ship SCS gate correction (verified 2026-05-15): corrected the data-quality-assessment source, regenerated the PDF, aligned markdown, and updated the stale closure-audit equation row.

**v1.2 PINN Implementation Readiness** (complete — shipped 2026-05-08)
- Phase 9: Issues Directory Consolidation — 3 thematic docs + MIGRATION.md + README.md written, verified and validated

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
- Qwen 3.5 2B 4-bit model download status needs verification (Qwen3.5-2B-4bit/ directory not found on disk)
- 5 of 6 LaTeX sources are modular (split into sections/); sampling-method is monolithic
- Markdown conversions exist in two locations: `markdown_conversion/` (top-level) and `markdown_conversion/pandoc_conversion/`
- Some sources have 2-3 competing markdown conversions; the best candidate was selected per phase during v1.3

## Constraints

- **Hardware**: M2 Mac development machine — limits model size and training speed
- **Model**: Qwen 3.5 2B 4-bit — chosen for local training feasibility on M2
- **Data format**: Brutus outputs are high-precision text files, not natively LLM-friendly
- **Dependencies**: No `requirements.txt` exists — environment management needed
- **One-to-one injection**: Markdown must match LaTeX source exactly; non-architecture inter-document inconsistencies remain preserved unless a v1.4 fix directly requires touching them
- **Commented-out content**: LaTeX `\begin{comment}...\end{comment}` blocks (not author comments) are excluded from markdown
- **Source critique mandatory for v1.4**: Neither `ctl_pinn_resolution.md` nor `01-architecture-and-physics-foundations.md` is treated as authoritative; every contested finding requires EVID-05 adjudication against the live framework specs and first-principles physics

## Key Decisions

<!-- Decisions that constrain future work. Add throughout project lifecycle. -->

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Fine-tune Qwen 3.5 2B for trajectory prediction | Small enough to train locally on M2 Mac | — Pending |
| Clean up codebase before LLM work | Data integrity is the foundation; cleanup simplifies downstream pipeline | ✓ v1.0 shipped (Phases 1-4) |
| Verify LaTeX modularization before LLM work | Ensure documentation integrity for future reference | ✓ v1.1 shipped (Phases 5-8) |
| PINN vs LLM approach | PINN architecture exists but no training loop; LLM is the new direction | — Pending |
| Numerical trajectory output (not qualitative) | Core use case is trajectory prediction from ICs | — Pending |
| Verify markdown conversions before cross-document reconciliation | Must first ensure each markdown is a faithful copy of its LaTeX source; find inconsistencies later | ✓ v1.3 shipped (Phases 10-15) |
| One phase per LaTeX source (6 phases) | Keeps each phase scoped to one document; avoids context-switching across different content | ✓ v1.3 shipped |
| Preserve source-level CTL dimensionality inconsistency as metadata | Phase 10 found source alternates between 11/12D and 13/14D input-vector descriptions; conversion body must remain faithful | ✓ Phase 10 |
| v1.3 milestone complete | All 6 markdown conversions verified; all audit gaps remediated | ✓ 2026-05-08 |
| Correct SCS/raw-drift gate after v1.3 | User ratified the gate-led policy: keep SCS as a base-10 log score, introduce raw drift `\epsilon_H`, and reject at `\epsilon_H > 10^{-5}` / `SCS > -5` | ✓ 2026-05-15 |
| Resolution doc is NOT authoritative in v1.4 | The consolidated multi-AI resolution may contain errors that were never checked against current framework specs and first-principles physics; treating it as truth would silently bake in those errors. EVID-05 mandates critical examination of BOTH the resolution doc and the thematic issue doc, identifying the root-cause framework ambiguity behind each contested finding. Live PINN-side code is not v1.4 grounding or evidence. | — Active (v1.4) |
| Iterative re-verification protocol for v1.4 | Architecture/physics fixes will routinely need multiple attempts before a finding actually resolves. The ledger pattern (`PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED` with regression revert) prevents "fix applied" being mistaken for "issue closed." VER-04/VER-05 codify execute-then-re-verify using disposable validation probes, not production code edits; the loop is expected, not a failure mode. | — Active (v1.4) |
| `master_consolidation_report.md` demoted to supporting evidence | The resolution doc already consumed it; treating both as co-equal primary sources triples re-adjudication work without adding signal. | — Active (v1.4) |
| Agent must surface gaps, not invent (v1.4 and similar adjudication milestones) | User does not trust the executing agent to make decisions where source materials are silent or ambiguous; cost of asking is small, cost of silent invention is irreparable spec drift across phases. | — Active (v1.4) and standing rule for future adjudication milestones; see `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` "CRITICAL GOVERNANCE" block and per-phase `NN-GAPS.md` mechanism |
| Live code in `pinn/` is NOT a grounding source during v1.4 (directive 2026-05-19) | The v1.3-era code reflects a previous framework version; relying on it as evidence would silently propagate v1.3-era assumptions into v1.4 spec edits. The framework specs are the source of truth being constructed; the code will be rebuilt from them in FUT-01. | — Active (v1.4); see `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` "CRITICAL GOVERNANCE" block. Live-code references permitted only in forward-pointing FUT-01 hand-off documents. |
| v1.4 spec work isolated on `milestone/v1.4` branch (2026-05-19) | Master must remain a known-good checkpoint untouched by in-progress v1.4 spec edits, so it can serve as the pre-milestone baseline for selective or full revert. Per-phase atomic commits on the branch preserve selective revertibility (`git revert <phase-commit>` after merge); pre-phase checkpoint tags (`v1.4-pre-phase-NN`) provide named recovery points without log spelunking; `--no-ff` merge at milestone end preserves per-phase commits on master for post-merge granular revert. Worktree isolation rejected (no parallel-work need; interacts badly with non-primary-path STOP protocol). Squash-merge rejected (collapses per-phase commit boundaries, defeats selective-revert goal). | — Active (v1.4); branch cut from master HEAD 2026-05-19 with `v1.4-pre-phase-17` tag at the same point. Standard branch-awareness governance (CLAUDE.md / AGENTS.md) applies — every session must surface the working branch before any file mutation. |
| Phase 20.5 (Sampling Coordinate Allocation) design and plan locked (2026-05-19, commit b727b15) | `sampling_method.md` double-booked Sobol coordinate `u_4` between the sampling-time scale factor and the first velocity component — flagged in `docs/findings/addressing_sobol_sequence_suggestion.md`. User locked **Option A**: when scaling is enabled, velocity coordinates shift to `u_5, u_6, u_7`; dimension formula `d = 3 + δ_s + 3δ_v` (rotate=False). Option A matches `simulation_data/Scripts/ic_generation/ic_generation_utils.py` — the code that generated the existing standard quasi-random dataset — so the v1.4 spec describes the data that already exists, with no framework-data mismatch. SCOPE-05 is introduced to carve out `simulation_data/Scripts/ic_generation/` as a permitted grounding source for data-generation specs, distinct from the `pinn/` no-live-code directive. Phase 20.5 is inserted between Phase 20 and Phase 21 (precedent: v1.3 "Phase 15.1"). | — Active (v1.4); design and plan committed but Phase 20.5 execution (ROADMAP/REQUIREMENTS edits, `sampling_method.md` edits, gap register, SCOPE-05 propagation) is pending. See `docs/superpowers/specs/2026-05-19-sobol-allocation-ambiguity-design.md` and `docs/superpowers/plans/2026-05-19-phase-20-5-sampling-coordinate-allocation.md`. |
| Phase 18 frame and gauge contracts complete (2026-05-21, verification `18aacde`) | The framework specs now define the unified preprocessing order, COM/momentum frame assertions, canonical ordering, canonical rotation gauge, global scaling order, FRAME-03 sampling-frame reconciliation, and 3D Cartesian output guard. B-05 and M3 are `VERIFIED`; FUT-01 code divergence is recorded without editing `pinn/`. | ✓ Phase 18 complete; Phase 19 physics/loss contracts are next. |

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
*Last updated: 2026-05-21 — Phase 18 complete and verified; Phase 19 physics/loss contracts are next. Phase 20.5 execution remains pending before Phase 21.*
