---
gsd_state_version: 1.0
milestone: v1.6
milestone_name: Resolving 03 Curriculum and Training Loop
current_phase: 31
current_phase_name: resolution-doc-readiness-verification
status: executing
stopped_at: Phase 31 complete — resolution-doc readiness READY-WITH-CAVEATS; Phases 32-36 unblocked, proceeding to Phase 32 planning
last_updated: "2026-06-20T11:18:06.000Z"
last_activity: 2026-06-20
last_activity_desc: Phase 31 executed — resolution-doc readiness READY-WITH-CAVEATS (32-36 unblocked)
progress:
  total_phases: 7
  completed_phases: 2
  total_plans: 6
  completed_plans: 6
  percent: 29
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-06-20)

**Core value:** Curriculum-staging and training-loop framework contracts are evidence-backed, consistent with the locked v1.4/v1.5 conventions, and verified before any training-loop implementation depends on them
**Current focus:** Phase 31 complete (resolution-doc readiness READY-WITH-CAVEATS); Phase 32 unblocked — next: discuss/plan Phase 32

## Current Position

Phase: 31 (resolution-doc-readiness-verification) — COMPLETE (gate READY-WITH-CAVEATS; 31-01 executed, user-confirmed)
Plan: 31-01 executed + committed; 1 of 1 complete (Phase 30: 5/5 complete + verified)
Status: Phase 31 complete — resolution-doc readiness verdict READY-WITH-CAVEATS (31-READINESS-REPORT.md + 31-RESOLUTION-MAP.md committed). Pre-exec gate PASS; 18/18 findings covered (0 silent, 0 partial); 0 v1.5-verified-fact contradictions; 0 SCOPE-12 locked-convention violations. 12 non-blocking caveats routed downstream by design: D-04/D-05/D-06 + tau_L estimator + GAP-17 provenance → Phase 32 EVID-15; M16/NS-13/ALM defers → Phases 34/35; unverified figures → FUT calibration; §6 non-independence → provenance hygiene for EVID-11..15. Phases 32-36 UNBLOCKED. No STOP-protocol gap arose.
Last activity: 2026-06-20 — Phase 31 executed (Tasks 1-7 + user-confirmed gate decision); resolution-doc readiness READY-WITH-CAVEATS

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
| Phase 23 P04 | 12min | 2 tasks | 1 files |
| Phase 23 P05 | 15min | 2 tasks | 2 files |
| 23 | 5 | - | - |
| 24.5 | 1 | - | - |
| 25 | 2 | - | - |
| Phase 26 P26-02 | 28 | 2 tasks | 3 files |
| Phase 26 P26-05 | ~25 min | 3 tasks | 4 files |
| 26 | 5 | - | - |
| Phase 27 P01 | 15min | 3 tasks | 3 files |
| Phase 27 P02 | 15min | 3 tasks | 3 files |

## Accumulated Context

### Roadmap Evolution

- v1.0: Codebase Cleanup (Phases 1-4) — shipped 2026-03-20
- v1.1: LaTeX Modularization Verification (Phases 5-8) — shipped 2026-03-22
- v1.2: PINN Implementation Readiness (Phase 9) — complete; 3 thematic docs + MIGRATION.md + README.md written, verified and validated
- v1.3: Markdown Conversion Verification & Correction (Phases 10-15, 15.1) — shipped 2026-05-08; post-ship SCS gate correction verified 2026-05-15
- v1.4: Resolving 01 Architecture and Physics Foundations (Phases 16-22, plus inserted Phase 20.5) — shipped 2026-06-09. All phases closed; archived under `.planning/milestones/v1.4-*`. EDL support remains a non-canonical support workflow under `.planning/research/edl/`.
- v1.5: Resolving 02 Data Pipeline and Validation (Phases 23-29) — shipped 2026-06-17. 36/36 requirements mapped; standard granularity; 8 phases (incl. inserted 24.5). Phase 23 (research package) first; Phase 24 (verification + DATA-07 addendum) ran in parallel with the external-research gate; Phases 25-29 gated on the resolution doc AND Phase 24. Spec edits limited to `ctl_instruction.md` and `pinn_architecture.md` (SCOPE-08/09/10). Branch `milestone/v1.5` from master HEAD `b8b39a4`; `--no-ff` merged to master (fe9b3c92) and archived under `milestones/v1.5-*` 2026-06-17 (tag v1.5).
- v1.6: Resolving 03 Curriculum and Training Loop (Phases 30-36) — roadmap created 2026-06-17. 32/32 requirements mapped; standard granularity; 7 phases (no inserted decimal). Phase 30 (research package) first and ungated; its delivery opens the external resolution-doc gate. Phase 31 (resolution-doc readiness verification, operational, 0 IDs) gates Phases 32-36. Phase 32 stands up the evidence ledger and adjudicates the headline conflicts (D-04/D-05/D-06 + `D=6.694` + M14) before the contract phases transcribe verdicts: Phase 33 (CURR), Phase 34 (LOOP), Phase 35 (LOSS). Phase 36 (VER) executes acceptance checks + handoff. Specwork-only (SCOPE-13/14/15); `pinn/` never grounding (SCOPE-10). Branch `milestone/v1.6` (worktree) cut from the v1.5 deliverable tip `88aa1e4f`; rebased onto completed master 2026-06-17 once v1.5 shipped.
- Phase 15.1 inserted (URGENT) after Phase 15: Fix milestone v1.3 markdown conversion issues
- Phase 20.5 (Sampling Coordinate Allocation) design+plan locked (2026-05-20, commit b727b15); completed execution 2026-06-07.

### v1.6 Phase Summary

| Phase | Focus | Requirements | Gate |
|-------|-------|--------------|------|
| 30 | Research package assembly (annotated doc list + framed questions, figures "claimed, unverified" unless v1.5-verified; D-04/D-05/D-06 + `D=6.694` posed neutrally) + read-only characterization of `review-of-framework.md` / `stage-strat-revision.md` | PKG-05..08 | None (first phase); delivery opens external gate |
| 31 | Resolution Doc Readiness Verification (v1.5 Phase 24.5 analog) | Operational (no new IDs) | Consolidated resolution doc landing |
| 32 | Evidence framework, issue ledger, root-cause conflict adjudication (D-04/D-05/D-06, M14, `D=6.694`) + re-verification ledger | EVID-11..15 | Phase 31 |
| 33 | Curriculum-stage contracts (adaptive assignment, `tau_L`/`L_max`, dual-path transitions, Stage 0–6 gating, s_min stage-gate frame) | CURR-01..05 | Phase 31 (via Phase 32 verdicts) |
| 34 | Training-loop & batch-construction contracts (replay/lookahead, two point sets, mixed sampling, merged clipping, ALM+`μ_p` clamp, `dt_out` collocation scaling, SASD/IPR/PSC training-side use) | LOOP-01..08 | Phase 31 (via Phase 32 verdicts) |
| 35 | Loss & energy-weight contracts (loss scaling, capped-hybrid `λ_E`, Huber-δ, D-04 causal-mode contract) | LOSS-01..04 | Phase 31 (via Phase 32 verdicts) |
| 36 | Acceptance checks executed, ledger close, SI-ledger reconcile, FUT-01/FUT-04 handoff, 32/32 traceability | VER-13..18 | Phases 32–35 |

**Execution order:** 30 → ⛔gate opens (user ERW research starts) → 31 readiness check → 32 (evidence + conflict adjudication) → 33 (curriculum) → 34 (training-loop) → 35 (loss) → 36 (acceptance + handoff).

**Verification protocol (applies to every adjudication phase 32–36):** adjudicate → fix → verify → re-verify after every batch → close only when the acceptance check passes. The issue ledger lives at a stable path under the Phase 32 (evidence-framework) directory. Spec edits limited to `ctl_instruction.md` / `pinn_architecture.md`; probes never touch `pinn/`. STOP protocol in full; phase-local `NN-GAPS.md` + milestone index `.planning/milestones/v1.6-GAPS.md`.

### v1.5 Phase Summary

| Phase | Focus | Requirements | Gate |
|-------|-------|--------------|------|
| 23 | Research package assembly (annotated doc list + framed questions, figures "claimed, unverified") + DQA characterization | PKG-01..04 | None (first phase); delivery opens external gate |
| 24 | Empirical dataset verification + DATA-07 correction addendum (seeds the issue ledger) | DATA-01..07 | None external; runs in parallel with gate window; depends on Phase 23 |
| 24.5 | Resolution doc readiness verification (INSERTED) | Operational (no new IDs) | Consolidated resolution doc + Phase 24 |
| 25 | Evidence framework, verdicts, root-cause conflict adjudication, re-verification ledger | EVID-06..10, VER-10 | Phase 24.5 |
| 26 | DataLoader ingestion & selection contracts | PIPE-01, 02, 03, 05, 06, 10 | Phase 24.5 |
| 27 | Sampling, precision, dt_out/stage-query, global-scale contracts | PIPE-04, 07, 08, 09 | Phase 24.5 |
| 28 | Validation-metrics contracts (SCS, SASD, IPR, PSC) | VAL-01..04 | Phase 24.5 |
| 29 | Acceptance checks executed, ledger close, SI-ledger reconcile, handoff | VER-07, 08, 09, 11, 12 | Phase 24.5 |

**v1.5 execution order:** 23 → ⛔gate opens (user research starts) ‖ 24 runs in parallel → 24.5 readiness check → 25 → 26 → 27 → 28 → 29.

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

- [v1.6-roadmap 2026-06-17]: 7 phases (30–36), standard granularity, continuing numbering from v1.5's Phase 29 (no reset). Phase 30 (research package, ungated) first; its delivery opens the external resolution-doc gate. Phase 31 (resolution-doc readiness verification) is operational (0 requirement IDs) and given the next whole number rather than a decimal because it is a planned milestone phase, not an urgent insertion (departs from the v1.5 inserted-Phase-24.5 convention). Phase 32 (EVID) stands up the ledger AND adjudicates the headline conflicts before the contract phases transcribe verdicts — there is intentionally NO standalone empirical-dataset-verification phase (doc-03's dataset facts were settled in v1.5; remaining empirical work is FUT/trainex). Contract phases 33/34/35 (CURR/LOOP/LOSS) follow the EVID verdicts; Phase 36 (VER) executes acceptance checks and writes the handoff. 32/32 mapped (VER-14).
- [v1.6-init]: v1.6 targets issue doc 03 (curriculum + training loop); specwork-only, ERW package-first. Resolution doc is NOT authoritative — candidate verdict source only, same standing `ctl_pinn_resolution.md` had in v1.4 and `02-resolution-doc.md` had in v1.5. Issue doc non-authoritative. Locked v1.4 + v1.5 outcomes are hard-constraint grounding (SCOPE-12), incl. raw-mass `D ≈ 4.6416` (doc-03's `D=6.694` must reconcile, EVID-15). `pinn/` never grounding (SCOPE-10). Spec edits limited to `ctl_instruction.md` / `pinn_architecture.md` (SCOPE-13); `sampling_method.md` frozen (SCOPE-08); `data_quality_assessment.md` / `review-of-framework.md` / `stage-strat-revision.md` read-only (SCOPE-09); training-loop code + EDA run + Stage-0 pilot are FUT-01/FUT-04 (SCOPE-14/15).
- [v1.6-init]: v1.6 initialized in an isolated worktree (`../3_body_problem-v1.6`, branch `milestone/v1.6`) cut from the v1.5 deliverable tip `88aa1e4f` — departs from the v1.4/v1.5 "no worktree" convention because v1.5 closure runs concurrently in the main tree. The branch is rebased onto the completed `master` once v1.5's `--no-ff` merge + `/gsd-complete-milestone` land. Tag `v1.6-pre-phase-NN` from branch HEAD before each phase; one atomic commit per plan via `scripts/agent-commit`; `--no-ff` merge to master at milestone end.
- [v1.5-roadmap-revision 2026-06-10]: Phase-order swap — **research package first (Phase 23)**, **empirical verification second (Phase 24)**. Rationale: the user's external multi-AI research is the milestone critical path (it gates all adjudication, Phases 25–29), so the package must ship first; figures in the package are marked "claimed, unverified" (PKG-03). PKG-04 (DQA characterization) moves to Phase 23 (read-only, fast, informs the document-list decision). DATA-07 added — a post-verification correction addendum forwarded to the in-flight external research; nil addendum if nothing contradicted. Phase 24 runs in parallel with the gate window and gates on nothing external.
- [v1.5-roadmap]: 7 phases (23–29; 8 incl. inserted 24.5), standard granularity, derived from issue-02's simpler shape (one issue doc, two spec-edit targets). Research package (Phase 23) precedes; verification + correction addendum (Phase 24) runs in parallel with the external resolution-doc gate; EVID/PIPE/VAL adjudication (Phases 25–28) and acceptance/handoff (Phase 29) follow the gate AND Phase 24.
- [v1.5-roadmap]: VER-10 (re-verification ledger) owned by Phase 25; the ledger file lives at a stable path under the **Phase 24 (empirical-dataset-verification)** directory, seeded with the finding inventory + DATA evidence by Phase 24 and operated through the protocol established in Phase 25.
- [v1.5-roadmap]: VER-08 satisfied by this roadmap (every requirement maps to exactly one phase, 36/36); confirmed again at Phase 29 closure.
- [v1.5-init]: Resolution doc is NOT authoritative — candidate verdict source only, same standing `ctl_pinn_resolution.md` had in v1.4. Issue doc non-authoritative. Every finding verified empirically before any fix.
- [v1.5-init]: Spec edits limited to `ctl_instruction.md` / `pinn_architecture.md`; `sampling_method.md` frozen (SCOPE-08); `data_quality_assessment.md` read-only/characterized (SCOPE-09); `pinn/` never touched and not grounding (SCOPE-10).
- [v1.5-init]: On-disk dataset (SCOPE-06) and `simulation_data/Scripts/` (SCOPE-07) are grounding for v1.5; extends the v1.4 SCOPE-05 carveout.
- [v1.5-workflow]: All v1.5 work on `milestone/v1.5` branch (cut from master HEAD `b8b39a4`). Tag `v1.5-pre-phase-NN` before each phase; one atomic commit per plan via `scripts/agent-commit`; `--no-ff` merge to master at milestone end.
- [v1.4-EDL]: Empirically consequential source-silent gaps may attach central EDL research briefs under `.planning/research/edl/`; phase-local gap registers remain authoritative.
- [Post-v1.3]: SCS gate — raw Hamiltonian drift is `\epsilon_H`, SCS is `\log_{10}(\epsilon_H)`, gate is `\epsilon_H > 10^{-5}` / `SCS > -5`. v1.5 Phase 25 EVID-10 locked the log-based gate and rejected issue-02 ratio thresholds; the raw-mass `D ≈ 4.6416` convention stands (`D = 6.694` rejected). v1.6 reconciles issue-03's `D = 6.694` against this hard constraint (EVID-15).
- [Phase 25 2026-06-12]: Four v1.5 EVID-10 verdicts locked: SCS `accept-resolution` (locked log-based gate `SCS > -5` stands); D=6.694 `accept-resolution` (raw-mass D ≈ 4.6416 stands; CLM-13 ratified `convention-rejected`); M12 `accept-third-position` (`n_pts = min(n_pts_cap, n_snapshots)`); M11 MAJOR→BLOCKING reclassification STANDS. These are SCOPE-12 hard constraints for v1.6.
- [Phase 30]: Phase 30 research package delivered; external resolution-doc gate OPEN, user multi-AI ERW research starts
- [Phase 31 2026-06-20]: Resolution-doc readiness verdict READY-WITH-CAVEATS. Pre-exec gate PASS (doc 48,049 B / 282 lines, byte-identical to commit `49fb7958`; Phase 30 `5/5 complete + verified`). 18/18 selected findings `covered` by identity (0 `silent`, 0 `partial`); 0 v1.5-verified-fact contradictions (CLM IDs cited as provenance anchors; `D ≈ 4.6416` exact-matches EVID-10); 0 SCOPE-12 violations (§1.16 read fresh — upholds `4.6416`, rejects `6.694`). 12 non-blocking caveats routed by design: D-04/D-05/D-06 + §1.17 `tau_L` + GAP-17 provenance → Phase 32 EVID-15; M16/NS-13/ALM defers → Phases 34/35; unverified figures → FUT; §6 non-independence → provenance hygiene. Phases 32-36 UNBLOCKED. The resolution doc is the candidate verdict source (not authoritative); Phase 31 adjudicated nothing. No STOP-protocol gap arose.

### Pending Todos

Phase 31 (resolution-doc readiness) PASSED — verdict READY-WITH-CAVEATS; Phases 32–36 are UNBLOCKED. The consolidated resolution doc landed at `research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` (commit `49fb7958`).

- [ ] Discuss/plan Phase 32 (Evidence Framework, Issue Ledger & Conflict Adjudication) with `/gsd-discuss-phase 32` or `/gsd-plan-phase 32`; carry the 12 routed caveats from `31-READINESS-REPORT.md` §4
- [ ] Tag `v1.6-pre-phase-32` from `milestone/v1.6` HEAD before Phase 32 begins
- [ ] **[Standing trigger]** Create `.planning/milestones/v1.6-GAPS.md` index when the first v1.6 phase opens a gap (none arose in Phases 30–31)
- [x] Plan + execute Phase 30 (Research Package Assembly); external resolution-doc gate opened on delivery (2026-06-18)
- [x] Execute Phase 31 (resolution-doc readiness verification) — READY-WITH-CAVEATS (2026-06-20)
- [x] Rebase `milestone/v1.6` onto the completed `master` (2026-06-17; recovery `backup/milestone-v1.6-pre-rebase` + tag `v1.6-pre-rebase`)
- [x] Define v1.6 requirements (32 requirements across PKG/EVID/CURR/LOOP/LOSS/VER)
- [x] Create v1.6 roadmap (Phases 30–36; 32/32 mapped)

### Prerequisites

**v1.4 shipped and merged to master; v1.5 closure-ready** — the framework specs carry the locked v1.4 architecture/physics conventions AND the v1.5 data-pipeline/validation contracts that v1.6 treats as hard constraints (14D input, Jacobi IC₁₃, COM projection head, PHYS-03 softening, PHYS-01 raw-mass D ≈ 4.6416, post-v1.3 SCS gate, PIPE-01..10, VAL-01..04). v1.6 rebases onto the completed `master` once v1.5's merge + completion land.

### Blockers/Concerns

- **Working branch is `milestone/v1.6`** (isolated worktree at `../3_body_problem-v1.6`, cut from the v1.5 deliverable tip `88aa1e4f`, 2026-06-17). Do NOT commit v1.6 work to master or to `milestone/v1.5`. Tag `v1.6-pre-phase-NN` before each phase; `--no-ff` merge at milestone end. Every session must surface `git status --short --branch` before any file mutation.
- **External gate (SATISFIED):** the consolidated resolution doc landed under `framework-revisions/research_reports/03-curriculum-and-training-loop/` and Phase 31 verified its readiness (READY-WITH-CAVEATS, 2026-06-20). The gate that blocked Phases 32–36 is now open.
- **v1.5 closure (DONE):** v1.5 shipped 2026-06-17 (`--no-ff` merge `fe9b3c92`; archived under `.planning/milestones/v1.5-*`); `milestone/v1.6` was rebased onto the completed `master` the same day, reconciling the forward-only PROJECT.md/STATE.md edits.
- **STOP protocol active:** v1.6 is a "similar adjudication milestone" per AGENTS.md governance — source-silent semantic / process-schema / cross-phase decisions must be surfaced as gaps, never invented.
- Phases 32-36 UNBLOCKED: the issue-03 resolution doc landed at `research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` (commit `49fb7958`) AND Phase 31 resolution-doc readiness PASSED (READY-WITH-CAVEATS, 2026-06-20). Phase 32 may now be planned/executed, carrying the 12 routed caveats.

## Session Continuity

**Resume file:** .planning/phases/31-resolution-doc-readiness-verification/31-01-SUMMARY.md

Last session: 2026-06-20T11:18:06.000Z
Stopped at: Phase 31 complete (resolution-doc readiness READY-WITH-CAVEATS)
Next action: Phase 32 (Evidence Framework, Issue Ledger & Conflict Adjudication) is UNBLOCKED. Run `/gsd-discuss-phase 32` (recommended) or `/gsd-plan-phase 32` to begin evidence-packet construction (EVID-11..15), adjudicating the headline conflicts (D-04/D-05/D-06, M14, `D = 6.694`) using `31-RESOLUTION-MAP.md` and carrying the 12 routed caveats from `31-READINESS-REPORT.md` §4.

## Operator Next Steps

- v1.6 roadmap, requirements traceability, and STATE are written. Phase 30 (research package) is the unblocked first phase.
- Phases 32–36 unblock once the consolidated resolution doc lands and Phase 31 readiness verification passes.
- v1.5 closure (`--no-ff` merge + `/gsd-complete-milestone`) remains user-owned in the main tree; rebase `milestone/v1.6` onto the completed `master` after it lands.
