---
gsd_state_version: 1.0
milestone: v1.4
milestone_name: Resolving 01 Architecture and Physics Foundations
status: in_progress
last_updated: "2026-06-07"
last_activity: 2026-06-07
progress:
  total_phases: 8
  completed_phases: 6
  total_plans: 19
  completed_plans: 19
  percent: 75
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-06-07)

**Core value:** Simulation dataset and data pipeline are clean, validated, and correctly processed
**Current focus:** Phase 21 — Acceptance Checks, Validation Execution, and Handoff (Phase 20.5 complete)

## Current Position

Phase: 21
Plan: Next — Phase 21 acceptance checks and v1.4 final verification
Status: Phase 20.5 complete (1/1 plan executed). Phase 21 acceptance checks and v1.4 final verification are next; Phase 22 framework-spec cleanup remains the final v1.4 phase.
Last activity: 2026-06-07
Progress: [████████░░] 75%

## Performance Metrics

**Velocity:**

- Total plans completed: 58 (v1.0: 10, v1.1: 5, v1.2: 3, v1.3: 21, v1.4: 19)
- Average duration: ~10 minutes per plan (v1.1)

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. Code Rewrites | 3 | — | — |
| 2. Documentation | 3 | — | — |
| 3. Data Deletion | 2 | — | — |
| 4. Stale Refs | 2 | — | — |
| Phase 05 P01 | 4min | 2 tasks | 2 files |
| Phase 06 P01 | 4min | 2 tasks | 2 files |
| Phase 07-structure-fidelity-verification P01 | 15min | 2 tasks | 1 files |
| Phase 07-structure-fidelity-verification P02 | 38min | 3 tasks | 3 files |
| Phase 08-compilability-verification P01 | 10min | 2 tasks | 3 files |
| Phase 10 P01 | 3 min | 3 tasks | 1 files |
| Phase 10 P02 | 4 min | 2 tasks | 2 files |
| Phase 10 P03 | 4 min | 3 tasks | 6 files |
| Phase 11 P02 | 15min | 2 tasks | 2 files |
| 11 | 3 | - | - |
| 12 | 3 | - | - |
| 13 | 3 | 3 waves | 17 fixes |
| 14 | 3 | 3 waves | 14 fixes |
| 15 | 3 | - | - |
| 16 | 3 | - | - |
| 17 | 3 | - | - |
| 18 | 3 | - | - |
| 19 | 4 | - | - |
| 20 | 5 | - | - |
| 20.5 | 1 | - | - |

## Accumulated Context

### Roadmap Evolution

- v1.0: Codebase Cleanup (Phases 1-4) — shipped 2026-03-20
- v1.1: LaTeX Modularization Verification (Phases 5-8) — shipped 2026-03-22
- v1.2: PINN Implementation Readiness (Phase 9) — complete; 3 thematic docs + MIGRATION.md + README.md written, verified and validated
- v1.3: Markdown Conversion Verification & Correction (Phases 10-15, 15.1) — shipped 2026-05-08; post-ship SCS gate correction verified 2026-05-15
- v1.4: Resolving 01 Architecture and Physics Foundations (Phases 16-22, plus inserted Phase 20.5) — Phases 16–20.5 are complete and verified; Phase 21 validation/handoff is next, followed by final Phase 22 framework-spec cleanup. EDL support remains a non-canonical support workflow under `.planning/research/edl/`.
- Phase 15.1 inserted (URGENT) after Phase 15: Fix milestone v1.3 markdown conversion issues
- Phase 15.1 edited (2026-05-07): scope narrowed to v1.3 review report issues only; new issues handled via GSD workflow
- Phase 20.5 (Sampling Coordinate Allocation) design+plan locked (2026-05-20, commit b727b15), survived adversarial review (3 BLOCK + 7 FLAG fixes applied), and completed execution 2026-06-07. Inserts between Phase 20 and Phase 21; locks Option A (`u_4` scale, `u_5`–`u_7` velocity for standard config) matching `simulation_data/Scripts/ic_generation/ic_generation_utils.py`. Introduces SCOPE-05 (data-spec alignment carveout) — `.planning/PROJECT.md` already records the high-level status in commit a9ecd51, and completion artifacts now live under `.planning/phases/20-5-sampling-coordinate-allocation/`.
- Phase 22 added: Framework-Spec Cleanup

### v1.4 Phase Summary

| Phase | Focus | Requirements |
|-------|-------|--------------|
| 16 | Evidence framework, issue ledger, conflict adjudication | EVID-01..05, VER-02, VER-05 (defined) |
| 17 | Input and output contracts (incl. COM projection head) | IO-01..04 |
| 18 | Frame and gauge contracts | FRAME-01..04 |
| 19 | Physics and loss contracts (incl. M4 constraint counting) | PHYS-01..06 |
| 20 | Architecture and normalization cleanup | ARCH-01..05 |
| 20.5 | Sampling coordinate allocation | SAMP-01, SAMP-02; SCOPE-05 boundary; complete |
| 21 | Acceptance checks executed, SI-ledger reconciled, handoff | VER-01, VER-03, VER-04, VER-06 |
| 22 | Presentation-preserving framework-spec cleanup | TBD pending phase planning; VER-05 applies |

**Verification protocol (applies to every phase):** adjudicate → fix → verify → re-verify after every batch → close only when the acceptance check passes. Defined in detail in `.planning/ROADMAP.md` under v1.4.

### v1.3 Phase Summary

| Phase | Source | Sections | Candidates | Key Challenge | Status |
|-------|--------|----------|------------|---------------|--------|
| 10 | ctl-instruction | 8 | 3 (.md, _v2.md, pandoc) | Heavy math, stage criteria formulas | COMPLETE |
| 11 | Data-quality-assessment | 7 | 2 (.md, pandoc) | Cross-references, HTML table corruption | COMPLETE |
| 12 | pinn-architecture | 7 active + 3 inactive | 3 (.md, _v2.md, pandoc) | Comment block exclusion, inactive sections | COMPLETE |
| 13 | review_of_framework | 7 | 1 (pandoc only) | Sub-document structure | COMPLETE |
| 14 | stage_strat_revision | 6 | 1 (pandoc only) | Table normalization, bibliography reconstruction | COMPLETE |
| 15 | sampling-method | monolithic | 2 (.md, pandoc) | Monolithic source (no sections/ dir) | COMPLETE |

### Decisions

Recent decisions affecting current work:

- [v1.3]: One phase per LaTeX source (6 phases, Phases 10-15)
- [v1.3]: Phases ordered hardest-first: CTL (Phase 10) validates the approach before proceeding
- [v1.3]: Each phase follows: pick best candidate -> audit section-by-section -> fix -> verify -> archive -> report
- [v1.3]: One-to-one injection fidelity required — markdown must match LaTeX source exactly
- [v1.3]: Inter-document inconsistencies preserved, not resolved (separate future task)
- [v1.3]: Commented-out LaTeX sections (\begin{comment}...\end{comment}) excluded from markdown
- [v1.3]: Best markdown candidate selected per source; unselected duplicates archived to _archive/
- [v1.3]: Manual comparison only — no automated verification scripts this milestone (deferred to v2)
- [v1.3]: Milestone complete 2026-05-08 — all 6 markdown conversions verified and archived
- [Post-v1.3]: SCS gate correction shipped — raw Hamiltonian drift is `\epsilon_H`, SCS is `\log_{10}(\epsilon_H)`, and the data-ingestion gate is `\epsilon_H > 10^{-5}` / `SCS > -5`
- [v1.4-init]: Resolution doc is NOT authoritative; EVID-05 mandates critical examination of both `ctl_pinn_resolution.md` and `01-architecture-and-physics-foundations.md` against current framework specs and first-principles physics for every contested finding (B-02, B-04, B-09, M5)
- [v1.4-init]: Iterative re-verification loop (`PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED`) codified in VER-05; "fix applied" is not closure — only a passing acceptance check is. Loop expected to iterate; phases do not exit on regressed findings.
- [v1.4-scope]: Validation suite execution is VER-04 (in Phase 21) — not deferred to FUT — but execution uses disposable validation probes against the v1.4 framework specs. Existing `pinn/` implementation edits are deferred until after the framework specs are settled and live PINN-side code is not v1.4 evidence.
- [v1.4-init]: M4 (constraint counting) elevated to PHYS-06 — was missing from initial requirement coverage.
- [v1.4-init]: `master_consolidation_report.md` demoted from co-equal primary source to supporting evidence.
- [v1.4-workflow]: All Phases 17–22 spec work, including Phase 20.5, happens on `milestone/v1.4` branch; master frozen at branch-root commit until milestone acceptance. One atomic commit per plan completion; tag `v1.4-pre-phase-NN` before each phase begins; `--no-ff` merge to master at milestone end (preserves per-phase commits for granular post-merge revert). Worktree + squash-merge rejected. See PROJECT.md Key Decisions (2026-05-19) for full rationale.
- [v1.4-EDL]: Empirically consequential source-silent gaps may attach central EDL research briefs under `.planning/research/edl/`; phase-local gap registers remain authoritative, the user performs external research, and EDL artifacts do not resolve gaps or authorize probes/defaults/spec edits without user instruction. GAP-19-01 resolved by user instruction: epsilon_H = 1e-4 * S_H, with S_H = median_train(K0 + Uabs0). Phase 21 validates activation behavior only.
- [v1.2]: Phase 9 consolidated 7 issues files into 3 thematic docs: 01-architecture, 02-data-pipeline, 03-curriculum
- [v1.1]: Automated Python diffing approach chosen for verification
- [v1.1]: 4 verification dimensions: content completeness, preamble parity, structure fidelity, compilability
- [v1.1]: 5 modular structures across 4 directories (sampling-method excluded — no modular structure exists)
- [Phase 05]: D-01: Full recursive reassembly - resolve all input/include to produce flat file
- [Phase 06]: D-01: Inline preamble extraction for Data-quality-assessment (no input directive)
- [Phase 06]: D-02: Brace-depth tracking for multi-line config block extraction
- [Phase 06]: D-03: Whitespace normalization before comparison (strip trailing, collapse blanks)
- [Phase 07]: Exclude inactive sections from original comparison (not modular) for correct structural verification
- [Phase 07]: Section ordering must match original document structure exactly, including commented sections
- [Phase 07]: Float content formatting (line breaks) must match original exactly for structural fidelity
- [Phase 08]: D-04: Use latexmk -pdf for compilation (handles multi-pass automatically)
- [Phase 08]: D-10: PASS = 0 fatal errors in compilation log (lines matching ^!)
- [Phase 08]: D-15: Normalize warnings by stripping line numbers before comparison

### Pending Todos

All v1.3 tasks, the post-ship SCS gate correction, and v1.4 Phases 16-20.5 are complete. Phase 21 acceptance checks and v1.4 final verification are next.

- [x] Complete v1.2 Phase 9 verification (deferred — outside v1.3 scope)
- [x] Execute v1.3 Phases 11-15 (complete)
- [x] Fix all audit gaps from MILESTONE-AUDIT-v1.3.md (complete — Task #3)
- [x] Correct and verify SCS/raw-drift gate across LaTeX, PDF, markdown, and closure audit

### Prerequisites

**v1.2 Phase 9 completion** — Phase 9 has 3 thematic docs + MIGRATION.md + README.md written in `pinn_instruction/issues/`. Verification complete. Markdown conversion reorganization also complete (framework-specs/ vs framework-revisions/ taxonomy).

### Blockers/Concerns

One dependency-scoped blocker plus three operational notes apply to v1.4 execution:

- GAP-19-01 resolved by user instruction: epsilon_H = 1e-4 * S_H, with S_H = median_train(K0 + Uabs0). Phase 21 validates activation behavior only.
- **Working branch is `milestone/v1.4`** (cut from master 2026-05-19). Do NOT commit v1.4 spec edits to master. Before each phase begins, tag `v1.4-pre-phase-NN` from the branch HEAD as a named checkpoint. At milestone end, merge to master with `git merge --no-ff milestone/v1.4`. Standard branch-awareness governance (CLAUDE.md / AGENTS.md "CRITICAL GOVERNANCE: Git Branch Awareness") applies — every session must surface `git status --short --branch`, `git branch --show-current`, and `git worktree list` before any file mutation.
- Phase 16 produced the issue ledger at `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` and the EVID-05 adjudication template used by Phase 17 and later v1.4 spec phases.
- Phase 20.5 execution complete (2026-06-07). Phase 21 re-runs the full §10 acceptance suite using disposable validation probes. Plan budget should anticipate fix-verify-refix cycles in the framework specs, especially for B-04, M5, and the Phase 20.5 SAMP checks.

## Quick Tasks Completed

| Task ID | Description | Result | Files |
|---------|-------------|--------|-------|
| 260320-rca | Modularize PINN_architecture_plan.tex | 12 files, 13-page PDF, 0 errors/warnings | main.tex, preamble.tex, 6 active + 3 inactive sections, blueprint_summary.tex, bibliography.tex |
| 260320-rxu | Split CTL-instruction-final.tex | 12 files, 22-page PDF, 0 errors | main_CTL.tex, preamble_CTL.tex, 8 section files |
| 260320-sh3 | Modularize review_of_ctl-pinn_framework.tex | 9 files, 16-page PDF, 0 errors/warnings | main.tex, preamble.tex, 7 section files |
| 260320-ssi | Modularize stage-strat-revision.tex | 8 files, 17-page PDF, 0 errors/warnings | main.tex, preamble.tex, 6 section files |
| 260321-g5d | Modularize data_quality_assess.tex | 9 files, 11-page PDF, 0 errors/warnings | main.tex, preamble.tex, 7 section files |
| 260322-c01 | Create verify_compile.py | All 5 structures compile with 0 errors, 0 new warnings | verify_compile.py, compile_verification_report.md, tmp/.gitkeep |
| 260426-bfd | Update Brutus footer docs (resolved missing-footer claims) | 6 files updated; historical audit reports preserved | CLAUDE.md, AGENTS.md, GEMINI.md, ANTIGRAVITY.md, .planning/codebase/CONCERNS.md, .planning/codebase/TESTING.md |

## Session Continuity

Last session: 2026-06-07
Next action: Execute Phase 21 (Acceptance Checks & v1.4 Final Verification)
