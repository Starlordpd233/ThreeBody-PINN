---
gsd_state_version: 1.0
milestone: v1.5
milestone_name: Resolving 02 Data Pipeline and Validation
status: verifying
last_updated: "2026-06-10T06:09:37.379Z"
last_activity: 2026-06-10 — v1.5 roadmap revised (`.planning/ROADMAP.md`); REQUIREMENTS.md traceability updated to 36/36
progress:
  total_phases: 7
  completed_phases: 0
  total_plans: 0
  completed_plans: 0
  percent: 0
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-06-10)

**Core value:** Simulation dataset and data pipeline are clean, validated, and correctly processed
**Current focus:** v1.5 roadmap revised (Phases 23–29; phase-order swap); next action is to plan Phase 23 (research package assembly + DQA characterization)

## Current Position

Phase: Phase 23 next (roadmap revised, not started)
Plan: —
Status: Roadmap revised — 36/36 requirements mapped across 7 phases (23–29); phase-order swap (research package first, verification + correction addendum second)
Last activity: 2026-06-10 — v1.5 roadmap revised (`.planning/ROADMAP.md`); REQUIREMENTS.md traceability updated to 36/36

**Gate awareness:** Phase 23 (research package assembly + DQA characterization) runs first with no gate; its delivery opens the external resolution-doc gate (user research starts). Phase 24 (empirical dataset verification + DATA-07 correction addendum) runs **in parallel** during the gate window — it depends on Phase 23's delivered claim list but gates on nothing external. Phases 25–29 (all adjudication / spec-edit work) gate on BOTH the resolution doc landing at `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/` AND Phase 24 completion.

## Performance Metrics

**Velocity:**

- Total plans completed: 65 (v1.0: 10, v1.1: 5, v1.2: 3, v1.3: 21, v1.4: 26)
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
| 21 | 2 | complete | 2026-06-08 |

## Accumulated Context

### Roadmap Evolution

- v1.0: Codebase Cleanup (Phases 1-4) — shipped 2026-03-20
- v1.1: LaTeX Modularization Verification (Phases 5-8) — shipped 2026-03-22
- v1.2: PINN Implementation Readiness (Phase 9) — complete; 3 thematic docs + MIGRATION.md + README.md written, verified and validated
- v1.3: Markdown Conversion Verification & Correction (Phases 10-15, 15.1) — shipped 2026-05-08; post-ship SCS gate correction verified 2026-05-15
- v1.4: Resolving 01 Architecture and Physics Foundations (Phases 16-22, plus inserted Phase 20.5) — shipped 2026-06-09. All phases closed; archived under `.planning/milestones/v1.4-*`. EDL support remains a non-canonical support workflow under `.planning/research/edl/`.
- v1.5: Resolving 02 Data Pipeline and Validation (Phases 23-29) — roadmap created 2026-06-10, revised same day (phase-order swap). 36/36 requirements mapped; standard granularity; 7 phases. Phase 23 (research package) first; Phase 24 (verification + DATA-07 addendum) runs in parallel with the external-research gate; Phases 25-29 gate on the resolution doc AND Phase 24. Spec edits limited to `ctl_instruction.md` and `pinn_architecture.md` (SCOPE-08/09/10). Branch `milestone/v1.5` from master HEAD `b8b39a4`.
- Phase 15.1 inserted (URGENT) after Phase 15: Fix milestone v1.3 markdown conversion issues
- Phase 20.5 (Sampling Coordinate Allocation) design+plan locked (2026-05-20, commit b727b15); completed execution 2026-06-07.

### v1.5 Phase Summary

| Phase | Focus | Requirements | Gate |
|-------|-------|--------------|------|
| 23 | Research package assembly (annotated doc list + framed questions, figures "claimed, unverified") + DQA characterization | PKG-01..04 | None (first phase); delivery opens external gate |
| 24 | Empirical dataset verification + DATA-07 correction addendum (seeds the issue ledger) | DATA-01..07 | None external; runs in parallel with gate window; depends on Phase 23 |
| 25 | Evidence framework, verdicts, root-cause conflict adjudication, re-verification ledger | EVID-06..10, VER-10 | Resolution doc + Phase 24 |
| 26 | DataLoader ingestion & selection contracts | PIPE-01, 02, 03, 05, 06, 10 | Resolution doc + Phase 24 |
| 27 | Sampling, precision, dt_out/stage-query, global-scale contracts | PIPE-04, 07, 08, 09 | Resolution doc + Phase 24 |
| 28 | Validation-metrics contracts (SCS, SASD, IPR, PSC) | VAL-01..04 | Resolution doc + Phase 24 |
| 29 | Acceptance checks executed, ledger close, SI-ledger reconcile, handoff | VER-07, 08, 09, 11, 12 | Resolution doc + Phase 24 |

**Execution order:** 23 → ⛔gate opens (user research starts) ‖ 24 runs in parallel → 25 → 26 → 27 → 28 → 29.

**Verification protocol (applies to every adjudication phase 25–29):** adjudicate → fix → verify → re-verify after every batch → close only when the acceptance check passes. The issue ledger lives at a stable path under the Phase 24 (empirical-dataset-verification) directory, seeded by Phase 24 and operated through the protocol established in Phase 25. Spec edits limited to `ctl_instruction.md` / `pinn_architecture.md`; probes never touch `pinn/`. STOP protocol in full; phase-local `NN-GAPS.md` + milestone index `.planning/milestones/v1.5-GAPS.md`.

### v1.4 Phase Summary

| Phase | Focus | Requirements |
|-------|-------|--------------|
| 16 | Evidence framework, issue ledger, conflict adjudication | EVID-01..05, VER-02, VER-05 (defined) |
| 17 | Input and output contracts (incl. COM projection head) | IO-01..04 |
| 18 | Frame and gauge contracts | FRAME-01..04 |
| 19 | Physics and loss contracts (incl. M4 constraint counting) | PHYS-01..06 |
| 20 | Architecture and normalization cleanup | ARCH-01..05 |
| 20.5 | Sampling coordinate allocation | SAMP-01, SAMP-02; SCOPE-05 boundary; complete |
| 21 | Acceptance checks executed, SI-ledger reconciled, handoff | VER-01, VER-03, VER-04, VER-06 — complete |
| 22 | Presentation-preserving framework-spec cleanup | Complete; G1-G4 and VER-05 passed |

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

- [v1.5-roadmap-revision 2026-06-10]: Phase-order swap — **research package first (Phase 23)**, **empirical verification second (Phase 24)**. Rationale: the user's external multi-AI research is the milestone critical path (it gates all adjudication, Phases 25–29), so the package must ship first; figures in the package are marked "claimed, unverified" (PKG-03). PKG-04 (DQA characterization) moves to Phase 23 (read-only, fast, informs the document-list decision). DATA-07 added — a post-verification correction addendum forwarded to the in-flight external research; nil addendum if nothing contradicted. Phase 24 runs in parallel with the gate window and gates on nothing external.
- [v1.5-roadmap]: 7 phases (23–29), standard granularity, derived from issue-02's simpler shape (one issue doc, two spec-edit targets). Research package (Phase 23) precedes; verification + correction addendum (Phase 24) runs in parallel with the external resolution-doc gate; EVID/PIPE/VAL adjudication (Phases 25–28) and acceptance/handoff (Phase 29) follow the gate AND Phase 24.
- [v1.5-roadmap]: VER-10 (re-verification ledger) owned by Phase 25; the ledger file lives at a stable path under the **Phase 24 (empirical-dataset-verification)** directory, seeded with the finding inventory + DATA evidence by Phase 24 and operated through the protocol established in Phase 25.
- [v1.5-roadmap]: VER-08 satisfied by this roadmap (every requirement maps to exactly one phase, 36/36); confirmed again at Phase 29 closure.
- [v1.5-init]: Resolution doc is NOT authoritative — candidate verdict source only, same standing `ctl_pinn_resolution.md` had in v1.4. Issue doc non-authoritative. Every finding verified empirically before any fix.
- [v1.5-init]: Spec edits limited to `ctl_instruction.md` / `pinn_architecture.md`; `sampling_method.md` frozen (SCOPE-08); `data_quality_assessment.md` read-only/characterized (SCOPE-09); `pinn/` never touched and not grounding (SCOPE-10).
- [v1.5-init]: On-disk dataset (SCOPE-06) and `simulation_data/Scripts/` (SCOPE-07) are grounding for v1.5; extends the v1.4 SCOPE-05 carveout.
- [v1.5-workflow]: All v1.5 work on `milestone/v1.5` branch (cut from master HEAD `b8b39a4`). Tag `v1.5-pre-phase-NN` before each phase; one atomic commit per plan via `scripts/agent-commit`; `--no-ff` merge to master at milestone end.
- [v1.4-EDL]: Empirically consequential source-silent gaps may attach central EDL research briefs under `.planning/research/edl/`; phase-local gap registers remain authoritative.
- [Post-v1.3]: SCS gate — raw Hamiltonian drift is `\epsilon_H`, SCS is `\log_{10}(\epsilon_H)`, gate is `\epsilon_H > 10^{-5}` / `SCS > -5`. Known v1.5 tension: issue-02 ratio-based SCS thresholds (`> 1e-6` / `< 1e-8`) conflict with this gate — adjudicated via EVID-10 in Phase 25, edited in Phase 28 (VAL-01).

### Pending Todos

v1.5 roadmap is revised (phase-order swap); phases not yet started.

- [ ] Plan Phase 23 (Research Package Assembly + DQA Characterization) with `/gsd-plan-phase 23`
- [ ] Tag `v1.5-pre-phase-23` from `milestone/v1.5` HEAD before Phase 23 begins
- [ ] Create `.planning/milestones/v1.5-GAPS.md` index when the first phase opens a gap
- [x] Define v1.5 requirements (36 requirements committed 2026-06-10, incl. DATA-07)
- [x] Create v1.5 roadmap (Phases 23–29; 36/36 mapped)
- [x] Revise v1.5 roadmap — phase-order swap, research package first (2026-06-10)

### Prerequisites

**v1.4 shipped and merged to master** — framework specs carry the locked v1.4 architecture/physics conventions that v1.5 treats as hard constraints (14D input, Jacobi IC₁₃, COM projection head, PHYS-03 softening, PHYS-01 D convention, post-v1.3 SCS gate).

### Blockers/Concerns

- **Working branch is `milestone/v1.5`** (cut from master HEAD `b8b39a4`, 2026-06-10). Do NOT commit v1.5 work to master. Tag `v1.5-pre-phase-NN` before each phase; `--no-ff` merge at milestone end. Every session must surface `git status --short --branch` before any file mutation.
- **External gate:** opens on Phase 23 (research package) delivery. Phases 25–29 cannot start until BOTH the user delivers the resolution doc to `framework-revisions/research_reports/02-data-pipeline-and-validation/` AND Phase 24 completes. Phase 23 is unblocked; Phase 24 is unblocked and runs in parallel with the gate window (gates on nothing external).
- **STOP protocol active:** v1.5 is a "similar adjudication milestone" per AGENTS.md governance — source-silent semantic / process-schema / cross-phase decisions must be surfaced as gaps, never invented.

## Session Continuity

Last session: 2026-06-10T06:09:37.375Z
Next action: Plan Phase 23 with `/gsd-plan-phase 23` (no gate); ensure `v1.5-pre-phase-23` tag is cut from `milestone/v1.5` HEAD first.

## Operator Next Steps

- Plan Phase 23 with `/gsd-plan-phase 23` (Research Package Assembly + DQA Characterization) — first phase, no gate; its delivery opens the external resolution-doc gate.
- After Phase 23 delivers the research package, run external multi-AI research and place the resolution doc under `framework-revisions/research_reports/02-data-pipeline-and-validation/`. Phase 24 (Empirical Dataset Verification + DATA-07 correction addendum) runs in parallel during that gate window; its DATA-07 addendum is forwarded to the in-flight research.
- Phases 25–29 unblock once BOTH the resolution doc lands AND Phase 24 completes.
