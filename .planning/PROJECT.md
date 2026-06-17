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
- ✓ Evidence-backed Issue 01 adjudication with explicit STOP-gap handling and re-verification — v1.4
- ✓ Coherent 14D input, 13-component IC, raw 9D output, COM projection, frame, gauge, and sampling contracts — v1.4
- ✓ Physically consistent scaling, AD, softening, conservation, and loss contracts — v1.4
- ✓ Settled architecture and normalization contracts with downstream implementation divergences recorded — v1.4
- ✓ Executed five numerical acceptance probes and closed 32/32 requirements across 8/8 verified phases — v1.4
- ✓ Presentation-preserving framework-spec cleanup with complete author-comment preservation and FUT-05 handoff — v1.4
- ✓ Evidence-backed Issue 02 data-pipeline adjudication with empirical dataset verification and STOP-gap handling — v1.5
- ✓ Locked DataLoader ingestion/selection contracts (B-06 gate, B-11 ID-resolution, M11 blacklist, M13 gold-counterpart, D7 footers, D-03 HDF5) and sampling/precision/global-scale contracts — v1.5
- ✓ Canonical SCS/SASD/IPR/PSC validation-metric contracts, threshold-aligned to the locked gate; G1–G8 milestone-closure gate PASS — v1.5

### Active

<!-- Current scope. Building toward these. -->

- v1.6 (Issue-03 "Resolving CTL") requirement set being defined in the `milestone/v1.6` worktree — see `.planning/REQUIREMENTS.md` once the new milestone creates it.

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

## Current State

**Shipped:** v1.5 Resolving 02 Data Pipeline and Validation on 2026-06-17.

**In progress:** v1.6 (Issue-03 "Resolving CTL") initialization in the `milestone/v1.6` worktree — the next milestone starts fresh requirements. FUT-01 consumes the v1.5 dataset-finalization handoff (`29-HANDOFF.md` + `29-CODE-DIVERGENCE.md`): FO-1 promotes the 117 validated gold + the 184→67 cascade, then FO-2 runs PSC/SCR first-run sanity, SASD/IPR/PSC constant recalibration, and the AC-VAL-04 numeric check.

v1.5 closed 36/36 requirements across eight verified phases (23–29, including inserted 24.5) and 27 plans, with the G1–G8 milestone-closure gate PASS and 10/10 STOP-protocol gaps RESOLVED-WITH-INSTRUCTION. Its roadmap, requirements, audit, and phase execution history are archived under `.planning/milestones/v1.5-*`; the live `REQUIREMENTS.md` was removed at archive (fresh for v1.6).

<details>
<summary>Archived v1.4 planning context</summary>

### v1.4 Resolving 01 Architecture and Physics Foundations

**Goal:** Critically examine each Issue 01 finding against BOTH `ctl_pinn_resolution.md` AND `01-architecture-and-physics-foundations.md` — treating neither as authoritative — to identify the root-cause ambiguity in the current framework specs, lock the right convention, apply evidence-backed framework-spec edits, and **verify each fix with disposable acceptance checks** before closing the issue. v1.4 settles the framework documentation; it does not implement or update the production PINN/training code.

**Target features:**
- Evidence packets for each issue before edits: spec evidence, issue-report evidence, resolution-doc verdict, first-principles checks where required, and an explicit verdict from `{accept-resolution, accept-issue-doc, accept-third-position, reject-both-as-unsupported, defer-with-blocker}`. Live PINN-side code is not v1.4 evidence or grounding.
- For every contested finding (B-02, B-04, B-09, M5, and any further conflict discovered during the walkthrough), an EVID-05 record that names the underlying spec ambiguity and the convention now locked.
- Framework-spec revisions in `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`, `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`, and the narrow `sampling_method.md` sections needed for FRAME-03.
- Live code in `pinn/basic_architecture.py` and `pinn/data-processing-pipeline-full.py` is **NOT** used as evidence or grounding source for any v1.4 decision (directive 2026-05-19). It is v1.3-era artifact; FUT-01 will rebuild from the v1.4 specs. Live-code references are permitted only in forward-pointing FUT-01 hand-off documents (`NN-CODE-DIVERGENCE.md`, eventual `pinn/STATUS.md`).
- Disposable validation probes for scaling consistency, COM invariance, componentwise AD on the synthetic trajectory, force-energy consistency, and loss stability — failing probes loop back to the originating spec phase.
- Iterative re-verification: each finding moves through `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED` in `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md`; nothing closes on "fix applied," only on a passing acceptance check.
- Reconciled `SI-*` ledger: every v1.4-resolved finding retires its corresponding spec source-issue entry; `SI-DQA-002`/`SI-DQA-003`/`SI-PINN-002` are preserved untouched.
- Final presentation-preserving cleanup in Phase 22: repair rendering-breaking Markdown/LaTeX, normalize math representation, and defer author-comment adjudication to FUT-05 via a preserved handoff across the three framework specs.
- Requirements and roadmap begin at Phase 16, after v1.3 ended at Phase 15.1 and the post-ship SCS gate correction shipped 2026-05-15. Phases 16 through 22 are complete and verified 2026-06-09; v1.4 is ready for `--no-ff` merge to master.

**Primary sources:**
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md` — most recent candidate adjudication; not treated as authoritative
- `pinn_instruction/issues/01-architecture-and-physics-foundations.md` — thematic issue consolidation; not treated as authoritative

**Supporting evidence:**
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/master_consolidation_report.md` — earlier multi-AI consolidation already consumed by the resolution doc; **removed as obsolete (commit `a64c018`)**, so traceability now runs through `ctl_pinn_resolution.md` and the four individual model reports rather than this (now-deleted) file
- Individual model reports (`chatgpt_research_report.md`, `claude_research_report.md`, `claude_research_report_2.md`, `gemini_research_report.md`) — consult only when adjudicating a finding the consolidation map records as ambiguous (e.g., M6/M7)
- Brutus C++ integrator + IC generation / prescreening scripts: read-only reference for dataset / simulation-side first-principles checks. **The PINN-side live code (`pinn/basic_architecture.py`, `pinn/data-processing-pipeline-full.py`) is NOT in this supporting-evidence set** — per directive 2026-05-19 it is v1.3-era artifact, not used as evidence during v1.4.

**Scope:** Architecture and physics foundation corrections only. Data-pipeline, curriculum-stage, PINN implementation, and LLM fine-tuning work remain deferred. v1.4 may create or record disposable validation probes only to test risky framework contracts before the specs are locked. The SCS gate work that previously sat under data-quality-assessment is complete and out of v1.4 scope.

**EDL support:** Empirically consequential, source-silent decisions may use the non-canonical Empirical Decision Loop draft at `.planning/research/edl/README.md` for research support. Phase-local gap registers remain the authoritative blocking and resolution records; central EDL briefs package context for user-led external research and do not resolve gaps by themselves.

**Phase structure:** 7 core phases in `.planning/ROADMAP.md` (Phases 16–22), plus inserted Phase 20.5 for Sampling Coordinate Allocation before Phase 21. Phase 22 is the final presentation-preserving framework-spec cleanup after Phase 21. The 30 original v1.4 requirements retain their existing owning mappings in Phases 16–21; Phase 20.5 carries its own design/plan handoff; Phase 22 applies the existing cross-cutting VER-05 governance and is complete. The verification protocol and iterative re-verification loop are encoded as requirements (VER-04/05/06) and roadmap protocol rather than separate phases.

</details>

## Current Milestone: v1.6 Resolving CTL (Issue-03) — initializing

v1.6 starts fresh requirements for the curriculum-and-training-loop (CTL) issue (`pinn_instruction/issues/03-curriculum-and-training-loop.md`); see the `milestone/v1.6` branch/worktree and the forthcoming `.planning/REQUIREMENTS.md`. FUT-01 consumes the v1.5 dataset-finalization handoff (`29-HANDOFF.md` + `29-CODE-DIVERGENCE.md`).

<details>
<summary>Archived v1.5 planning context (shipped 2026-06-17)</summary>

**Goal:** Critically examine each finding in `pinn_instruction/issues/02-data-pipeline-and-validation.md` — treating the issue doc as non-authoritative — verify every claim empirically against the on-disk dataset, the `simulation_data/` scripts that generated it, the v1.4-revised framework specs, and first principles; adjudicate against the user-produced external resolution doc once it lands; apply evidence-backed framework-spec edits; and verify each fix with disposable acceptance probes before closing. v1.5 settles the data-pipeline/validation design contracts; it does not implement production DataLoader/training code (that remains FUT-01).

**Target features:**
- Research package for user-led external multi-AI research: a curated document list (consolidating scattered fragments into a single context file if the list would exceed ~5 files; framework specs passed intact) plus the questions to pose. The resulting resolution doc is expected at `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/`; adjudication phases gate on its arrival. The resolution doc is the candidate verdict source, NOT authoritative — same standing as `ctl_pinn_resolution.md` in v1.4.
- Evidence framework and issue ledger covering the issue-02 findings: B-06, B-11, M11, M12, M13, D7, G1–G5, D-03 (training-data format), validation-metrics-as-live-parameters claims (SCS/SASD/IPR/PSC), `compute_globals` D=6.694 correction, footer/mass-drift protocol, and precision handling — with v1.4-style verdicts and iterative re-verification (`PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED`).
- Disposable empirical probes against the on-disk dataset: file counts, ID gaps (claimed 1,250/4,000 standard; 143/5,000 hierarchical), blacklist contents (claimed 65 IDs), gold-counterpart gaps (claimed 184 standard IDs), footer schema variance, mass-drift check, global-scale recomputation.
- Spec edits limited to `ctl_instruction.md` and `pinn_architecture.md`. `sampling_method.md` is frozen by default (completed generation-instruction doc — see Key Decisions); `data_quality_assessment.md` is untouched but characterized early, with findings reported to the user.
- Doc-03 boundary: data-side contracts only (dt_out metadata exposure, stage/replay query interface). M16 collocation-scaling policy and the G6 causal-training decision stay with the future doc-03 milestone.
- STOP protocol in full (v1.5 is a "similar adjudication milestone" per AGENTS.md governance): phase-local `NN-GAPS.md` registers, milestone index `.planning/milestones/v1.5-GAPS.md`, no inventing where sources are silent. Governance docs updated with the v1.5 phase list once the roadmap is approved.
- Known tension to adjudicate in-milestone: issue 02's ratio-based SCS thresholds (`SCS > 1e-6` reject, `< 1e-8` Stage 5) conflict with the locked post-v1.3 gate (`\epsilon_H > 10^{-5}` / log-based `SCS > -5`).

**Primary sources (neither authoritative):**
- `pinn_instruction/issues/02-data-pipeline-and-validation.md` — thematic issue consolidation
- Forthcoming resolution doc under `framework-revisions/research_reports/02-data-pipeline-and-validation/` — candidate verdict source, produced by user-led external research in two stages (process recorded 2026-06-10, mirroring v1.4): multiple independent research agents each produce an individual report from the Phase 23 package; one final consolidation agent then produces the final resolution doc. Only the final consolidated doc is the candidate verdict source; the Stage-1 individual reports are retained beside it as supporting evidence, consulted when the final doc's consolidation provenance records ambiguity (v1.4 precedent: `ctl_pinn_resolution.md` beside the four model reports). Operator prompts for both stages: `docs/work/plans/milestone_v1.5/23-research-package-assembly/`.

**Grounding sources for v1.5:** dataset documentation (`simulation_data/Documentation/README.md`), the on-disk dataset itself (empirical facts), `simulation_data/Scripts/` (metrics calculation, prescreening, runners, ic_generation — extends the SCOPE-05 carveout), v1.4-revised framework specs, prior user decisions, and short uncontroversial first-principles derivations. **`pinn/` live code remains banned as grounding** — issue 02's "Canonical" citation of `data-processing-pipeline-full.py` is overridden; live-code references stay confined to forward-pointing FUT-01 hand-off documents.

**Git workflow:** main repo directory (no worktree); branch `milestone/v1.5` cut from master HEAD (`b8b39a4`) before any v1.5 commits; tag `v1.5-pre-phase-NN` from branch HEAD before each phase begins; one atomic commit per plan via `scripts/agent-commit`; `--no-ff` merge to master at milestone end.

</details>

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
- **One-to-one injection** (historical v1.3 policy; superseded 2026-06-09): During v1.3, markdown was required to match LaTeX source exactly with one-to-one injection fidelity, and non-architecture inter-document inconsistencies remained preserved. Under the current v1.4+ policy, markdown framework specs (`pinn_instruction/markdown_conversion/framework-specs/*.md`) are the authoritative framework design documents during active revision, implementation, training, and research-result iteration; LaTeX sources are publication/archive derivatives refreshed only at the final publication/archive stage.
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
| Resolution doc is NOT authoritative in v1.4 | The consolidated multi-AI resolution may contain errors that were never checked against current framework specs and first-principles physics; treating it as truth would silently bake in those errors. EVID-05 mandates critical examination of BOTH the resolution doc and the thematic issue doc, identifying the root-cause framework ambiguity behind each contested finding. Live PINN-side code is not v1.4 grounding or evidence. | ✓ v1.4 shipped; retained as standing adjudication guidance |
| Iterative re-verification protocol for v1.4 | Architecture/physics fixes will routinely need multiple attempts before a finding actually resolves. The ledger pattern (`PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED` with regression revert) prevents "fix applied" being mistaken for "issue closed." VER-04/VER-05 codify execute-then-re-verify using disposable validation probes, not production code edits; the loop is expected, not a failure mode. | ✓ v1.4 shipped; all acceptance gates passed |
| `master_consolidation_report.md` demoted to supporting evidence | The resolution doc already consumed it; treating both as co-equal primary sources triples re-adjudication work without adding signal. | ✓ v1.4 shipped |
| Agent must surface gaps, not invent (v1.4 and similar adjudication milestones) | User does not trust the executing agent to make decisions where source materials are silent or ambiguous; cost of asking is small, cost of silent invention is irreparable spec drift across phases. | — Active (v1.4) and standing rule for future adjudication milestones; see `AGENTS.md` plus symlinks `CLAUDE.md` / `GEMINI.md`, supplemental `ANTIGRAVITY.md`, and per-phase `NN-GAPS.md` mechanism |
| Empirical Decision Loop support remains non-canonical until promoted (2026-05-24) | Some source-silent decisions are empirically consequential: theory can identify the formula shape but not the practical value, threshold, or stability default. The EDL draft provides a research-support workflow so agents package the context for user-led research and later EDL probes without inventing conclusions. Phase gap registers remain the authoritative blocking records. | — Draft support workflow at `.planning/research/edl/README.md`; first central brief is `EDL-19-01` for `GAP-19-01` `epsilon_H`. |
| Live code in `pinn/` is NOT a grounding source during v1.4 (directive 2026-05-19) | The v1.3-era code reflects a previous framework version; relying on it as evidence would silently propagate v1.3-era assumptions into v1.4 spec edits. The framework specs are the source of truth being constructed; the code will be rebuilt from them in FUT-01. | — Active (v1.4); see `AGENTS.md` plus symlinks `CLAUDE.md` / `GEMINI.md` and supplemental `ANTIGRAVITY.md` governance notes. Live-code references permitted only in forward-pointing FUT-01 hand-off documents. |
| v1.4 spec work isolated on `milestone/v1.4` branch (2026-05-19) | Master must remain a known-good checkpoint untouched by in-progress v1.4 spec edits, so it can serve as the pre-milestone baseline for selective or full revert. Per-phase atomic commits on the branch preserve selective revertibility (`git revert <phase-commit>` after merge); pre-phase checkpoint tags (`v1.4-pre-phase-NN`) provide named recovery points without log spelunking; `--no-ff` merge at milestone end preserves per-phase commits on master for post-merge granular revert. Worktree isolation rejected (no parallel-work need; interacts badly with non-primary-path STOP protocol). Squash-merge rejected (collapses per-phase commit boundaries, defeats selective-revert goal). | — Active (v1.4); branch cut from master HEAD 2026-05-19 with `v1.4-pre-phase-17` tag at the same point. Standard branch-awareness governance (CLAUDE.md / AGENTS.md) applies — every session must surface the working branch before any file mutation. |
| Phase 20.5 (Sampling Coordinate Allocation) design and plan locked (2026-05-20, commit b727b15) | `sampling_method.md` double-booked Sobol coordinate `u_4` between the sampling-time scale factor and the first velocity component — flagged in `docs/findings/addressing_sobol_sequence_suggestion.md`. User locked **Option A**: when scaling is enabled, velocity coordinates shift to `u_5, u_6, u_7`; dimension formula `d = 3 + δ_s + 3δ_v` (rotate=False). Option A matches `simulation_data/Scripts/ic_generation/ic_generation_utils.py` — the code that generated the existing standard quasi-random dataset — so the v1.4 spec describes the data that already exists, with no framework-data mismatch. SCOPE-05 is introduced to carve out `simulation_data/Scripts/ic_generation/` as a permitted grounding source for data-generation specs, distinct from the `pinn/` no-live-code directive. Phase 20.5 is inserted between Phase 20 and Phase 21 (precedent: v1.3 "Phase 15.1"). | ✓ Phase 20.5 execution complete (2026-06-07); design/plan lock remains anchored at commit b727b15 and the initial status anchor remains commit a9ecd51. See `.planning/milestones/v1.4-phases/20.5-sampling-coordinate-allocation/` for GSD planning artifacts, probe evidence, and data-alignment hand-off. |
| Phase 22 is the final framework-spec cleanup (2026-06-07) | Phase 22 runs after Phase 21 so it can catch rendering defects introduced by the remaining spec work. Its scope is presentation-preserving: normalize math rendering and preserve/defer author comments without autonomous semantic changes or deletions. | ✓ Phase 22 complete 2026-06-09; G1/G2/G3/VER-05 green; G4 user visual backstop approved; F1 corruption fixed in `bf841f6`; F2–F6 accepted as authorized cleanup; all 4 STOP-protocol gaps RESOLVED-WITH-INSTRUCTION. |
| Phase 18 frame and gauge contracts complete (2026-05-21, verification `18aacde`) | The framework specs now define the unified preprocessing order, COM/momentum frame assertions, canonical ordering, canonical rotation gauge, global scaling order, FRAME-03 sampling-frame reconciliation, and 3D Cartesian output guard. B-05 and M3 are `VERIFIED`; FUT-01 code divergence is recorded without editing `pinn/`. | ✓ Phase 18 complete; Phase 19 physics/loss contracts are next. |
| Markdown framework specs authoritative; LaTeX source refresh is final-stage only (2026-06-09) | Markdown framework specs (`pinn_instruction/markdown_conversion/framework-specs/*.md`) will continue changing during implementation, training, and research-result iteration; syncing LaTeX sources earlier creates churn and false stability. LaTeX sources (`pinn_instruction/original_latex/framework-specs/**/*.tex`) are publication/archive derivatives, not active design sources. | — Active (cross-project); LaTeX is deferred until final publication/archive stage. Supersedes the draft v1.6.5 timing from `docs/work/designs/cross_cutting/latex-sync/2026-05-24-latex-markdown-sync-strategy-design.md`. |
| `master` is a personal working line on a private repo (2026-06-10) | The GitHub remote (`github.com/Starlordpd233/ThreeBodyProblem`) is **private** (verified via `gh repo view` 2026-06-10); no public audience exists for this history. User directive: master is for the owner's personal use and may freely contain scratch and personal artifacts (e.g., `docs_temp/` chat transcripts, agent context bundles, workspace captures). | — Active (cross-project). Any future public release must be a separately sanitized export — never a direct push of this repository's history, which contains personal chat transcripts. |
| v1.5 targets issue doc 02 with v1.4-style adjudication; user-produced resolution doc is the candidate verdict source (2026-06-10) | No resolution doc existed for issue 02 at milestone start. The user runs external multi-AI research from an agent-prepared research package (document list; scattered fragments consolidated into one context file if >~5 files; framework specs passed intact); adjudication phases gate on the doc landing. The issue doc remains non-authoritative — every finding is verified empirically before any fix. | — Active (v1.5). Resolution doc expected at `framework-revisions/research_reports/02-data-pipeline-and-validation/`. |
| `sampling_method.md` frozen by default (user directive 2026-06-10) | It is the completed instruction file that generated the now-finished `simulation_data/` dataset; the generation work will not be re-run, so design-revision of this file is futile. It remains the authoritative historical record of how the existing training data was produced. Only verified data-feasibility issues (dataset ↔ framework incompatibilities blocking training) plus explicit user instruction may touch it. No dedicated phase/milestone has yet verified dataset ↔ framework compatibility; `data_quality_assessment.md` may cover parts of that ground and is characterized (not edited) during v1.5. | — Active (cross-project). Recorded in AGENTS.md Source of Truth section. |
| v1.5 grounding extensions: on-disk dataset + `simulation_data/Scripts/` (2026-06-10) | Issue 02's claims are largely empirical dataset facts (counts, gaps, footers, blacklist); verify-then-fix requires the dataset itself and the scripts that generated it as provenance. Extends the SCOPE-05 precedent beyond `ic_generation/`. The `pinn/` live-code ban persists — issue 02's "Canonical" citation of `data-processing-pipeline-full.py` is overridden. | — Active (v1.5); to be codified as SCOPE requirements in `.planning/REQUIREMENTS.md`. |
| v1.5 git workflow replicates v1.4 (2026-06-10) | Same rationale as the v1.4 decision: master stays a known-good baseline; per-plan atomic commits preserve selective revertibility; pre-phase tags give named recovery points; `--no-ff` merge preserves per-phase commits on master. Worktree isolation again rejected (no parallel-work need; interacts badly with STOP protocol). | — Active (v1.5); branch `milestone/v1.5` cut from master HEAD `b8b39a4` 2026-06-10, before any v1.5 planning commits. |
| Phase 25 EVID-10 verdicts locked (2026-06-12) | Root-cause adjudication of the three known cross-source conflicts, grounded in first principles + locked specs + verified dataset facts (D-09), not the resolution doc's recommendation: SCS — locked log-based gate `SCS > -5` stands, issue-doc ratio thresholds rejected (`accept-resolution`); `compute_globals` D — raw-mass `D = (G·T²)^(1/3) ≈ 4.6416` stands, 6.694 mass-fraction form rejected, CLM-13 ratified `convention-rejected` (OI-11); M12 — BLOCKING-infeasibility falsified on corrected CLM-10 medians, `n_pts = min(n_pts_cap, n_snapshots)` locked (`accept-third-position`); M11 — MAJOR→BLOCKING reclassification STANDS on data-integrity grounds (OI-8 carried to Phase 26 PIPE-03/FUT-01). | — Active (v1.5). Spec transcription owned by Phases 26–28 citing the EVID-10 records by path; ledger rows stay PENDING (adjudicated-but-unfixed per GAP-25-02) until fixes land and verify. |

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
*Last updated: 2026-06-17 after v1.5 milestone archive (v1.5 shipped 2026-06-17: 36/36 requirements, 8/8 phases, G1–G8 closure gate PASS; roadmap/requirements/audit/phase history archived under `milestones/v1.5-*`; live `REQUIREMENTS.md` removed for v1.6). Next: v1.6 (Issue-03 Resolving CTL) initialization.*
