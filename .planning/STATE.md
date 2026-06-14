---
gsd_state_version: 1.0
milestone: v1.5
milestone_name: Resolving 02 Data Pipeline and Validation
status: Executed
stopped_at: context exhaustion at 90% (2026-06-13)
last_updated: "2026-06-14T04:01:52.343Z"
last_activity: 2026-06-14 -- Phase 27 Plan 03 (PIPE-08 stage-query) complete
progress:
  total_phases: 8
  completed_phases: 4
  total_plans: 22
  completed_plans: 20
  percent: 50
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-06-12)

**Core value:** Simulation dataset and data pipeline are clean, validated, and correctly processed
**Current focus:** Phase 27 - sampling-precision-and-global-scale-contracts

## Current Position

Phase: 27
Plan: 03 complete
Status: Executed
Next: Plan 04 (PIPE-09 compute_globals)
Last activity: 2026-06-14 -- Phase 27 Plan 03 (PIPE-08 stage-query) complete

**Gate awareness:** Phase 23 (research package assembly + DQA characterization) completed 2026-06-10; its delivery opened the external resolution-doc gate (user research started). Phase 24 (empirical dataset verification + DATA-07 correction addendum) completed 2026-06-11 — ran **in parallel** during the gate window. 8 individual AI research results have landed. **Phase 24.5** (INSERTED 2026-06-11) verifies the consolidated resolution doc is ready for use before adjudication begins. Phases 25–29 (all adjudication / spec-edit work) gate on Phase 24.5 passing.

## Performance Metrics

**Velocity:**

- Total plans completed: 78 (v1.0: 10, v1.1: 5, v1.2: 3, v1.3: 21, v1.4: 26)
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
- v1.5: Resolving 02 Data Pipeline and Validation (Phases 23-29) — roadmap created 2026-06-10, revised same day (phase-order swap). 36/36 requirements mapped; standard granularity; 7 phases. Phase 23 (research package) first; Phase 24 (verification + DATA-07 addendum) runs in parallel with the external-research gate; Phases 25-29 gate on the resolution doc AND Phase 24. Spec edits limited to `ctl_instruction.md` and `pinn_architecture.md` (SCOPE-08/09/10). Branch `milestone/v1.5` from master HEAD `b8b39a4`.
- Phase 15.1 inserted (URGENT) after Phase 15: Fix milestone v1.3 markdown conversion issues
- Phase 20.5 (Sampling Coordinate Allocation) design+plan locked (2026-05-20, commit b727b15); completed execution 2026-06-07.

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

**Execution order:** 23 → ⛔gate opens (user research starts) ‖ 24 runs in parallel → 24.5 readiness check → 25 → 26 → 27 → 28 → 29.

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
- [Phase ?]: [23-04 PKG-02] Framed-research-questions.md authored: six locked v1.4 conventions as verbatim hard constraints (SCS gate cited only to read-only DQA, never editable spec); every in-scope finding posed as a neutral CLM-referenced question in three clusters; both known conflicts (SCS thresholds, D=6.694) and M13 fallback posed without settling; doc-03 items deferred. No STOP gap surfaced.
- [Phase 23]: Phase 23 research package delivered; external resolution-doc gate OPEN (user multi-AI research starts). Resolution doc lands at research_reports/02-data-pipeline-and-validation/.
- [Phase 23]: Doc-integrity audit F-08/F-09 contradict two claims carried in the delivered Phase 23 package: gold output filenames carry no gold token (folder-only), and ~2,470 files (1,550+701+219) have NO Result: footer rather than partial footers. CLM-07 claim text affected; CLM-09 values re-verified correct. Package stays byte-stable - audit workstream issues an erratum beside the package; Phase 24 DATA-07 CLM-keyed correction addendum is the authoritative follow-up and must fold these in.
- [Phase 23→24]: Phase 23 review (`23-REVIEW.md:115-173`) identified four non-blocking warnings (WR-01..04) routed to Phase 24's DATA-07 correction pass: WR-01 (Q-B2 sample-size conflict 1000 vs 100), WR-02 (Hard Constraint 3 wrong line cite 972→967), WR-03 (Q-B1 dangling "§5.3.2" cite, spec says example not contract), WR-04 (CLM-05 dual-observable ambiguity — IC vs Brutus folder counts). Two schema questions (CLM-05 split, new CLM row for WR-01) and one channel question (WR-02/03 citation-fix channel) are surfaced as open decisions in `24-DISCUSSION-LOG.md` — NOT pre-decided. WR-04 shapes DATA-03/04 probe design (count both observables separately). All corrections travel through the correction channel; package byte-stability preserved.
- [Phase 24.5 2026-06-11]: Resolution-doc readiness verification complete. Gate verdict **READY-WITH-CAVEATS**. All four checks pass: structure citable; 19/19 issue-02 findings covered (0 silent, 0 partial); 0 DATA-xx contradictions across CLM-01..13 + DATA-05; 0 locked-convention violations (HC-1..HC-6 upheld; issue-doc SCS ratio thresholds and D=6.694 rejected). Caveats are deferred-by-design open items the resolution doc registers (OI-3 calibration constants, OI-6 no-footer probe gap, OI-7 Q-A4 label-semantics STOP-gap defeater + gold-rerun residue, OI-8 M11 live-loader outside grounding, OI-11 CLM-13 → EVID-10/PIPE-09, OI-12 optional addendum erratum). Phases 25-29 unblocked. Deliverables: `24.5-READINESS-REPORT.md`, `24.5-RESOLUTION-MAP.md`. No STOP-gap opened.
- [Phase 24 2026-06-11]: GAP-24-01 (DATA-05 base-hier mass mismatch) resolved with user instruction. Current IC files are canonical; the 70 affected base-hier outputs (`0005`-`0059`, `0061`-`0075`) are invalid/stale artifacts requiring targeted rerun from current ICs; old artifacts are quarantined from training, metrics, and PIPE-07 until rerun validation passes. Remediation boundary recorded in `24-DATA05-RERUN-REMEDIATION.md`; the milestone gap index now has 0 open gaps.
- [Phase 25 2026-06-12]: Adjudication machinery stood up (`evidence/_TEMPLATE.md` 12-section + §3b Dataset Evidence; protocol README with EVID-10 trigger table, D-03 downstream enforcement, GAP-25-02 adjudicated-but-unfixed legend; `24-ISSUE-LEDGER.md` Lifecycle Rules re-issued to Phases 26–28). Four EVID-10 verdicts locked: SCS `accept-resolution` (locked log-based gate `SCS > -5` stands; ratio thresholds rejected); D=6.694 `accept-resolution` (raw-mass D ≈ 4.6416 stands; CLM-13 ratified `convention-rejected`, OI-11); M12 `accept-third-position` (`n_pts = min(n_pts_cap, n_snapshots)` locked; 0.5× factor rejected); M11 MAJOR→BLOCKING reclassification STANDS (data-integrity grounds; OI-8 carried to Phase 26 PIPE-03/FUT-01). G3/G5 close with parents (D-12). Remaining packets authored by owning phases 26–28 immediately before their spec edits (GAP-25-01 split reading); ledger rows stay PENDING (adjudicated-but-unfixed) until fixes verify.

### Pending Todos

v1.5 Phases 23–24 complete; Phase 24.5 inserted and planned; Phases 25–29 gated on Phase 24.5 (consolidated resolution doc + readiness check).

- [x] Plan Phase 23 (Research Package Assembly + DQA Characterization) with `/gsd-plan-phase 23`
- [x] Tag `v1.5-pre-phase-23` from `milestone/v1.5` HEAD before Phase 23 begins
- [x] **[Standing trigger]** Create `.planning/milestones/v1.5-GAPS.md` index when the first v1.5 phase opens a gap (created 2026-06-11; GAP-24-01 now RESOLVED-WITH-INSTRUCTION)
- [x] Continue Phase 24 DATA-07 addendum assembly and ledger/facts cleanup with `GAP-24-01` resolved (Phase 24 closed 2026-06-11; do not claim the 70 files are fixed until the rerun remediation gates pass — tracked under `24-DATA05-RERUN-REMEDIATION.md` as a separate operation).
- [x] (Separate remediation) DATA-05 70-file base-hier rerun from current canonical ICs: preserve old artifacts, run in staging, validate against DATA-05 gates, then replace and regenerate dependent metrics. Recorded under `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-DATA05-RERUN-REMEDIATION.md`. Not a Phase 24 closure prerequisite. (Executed and validated 2026-06-11: 70/70 reruns passed all gates, swap approved, old artifacts archived under `simulation_data/Data/forensic/data05_gap24-01_old_outputs/`; see GAP-24-01 in `.planning/milestones/v1.5-GAPS.md`.)
- [x] Define v1.5 requirements (36 requirements committed 2026-06-10, incl. DATA-07)
- [x] Create v1.5 roadmap (Phases 23–29; 36/36 mapped)
- [x] Revise v1.5 roadmap — phase-order swap, research package first (2026-06-10)

### Prerequisites

**v1.4 shipped and merged to master** — framework specs carry the locked v1.4 architecture/physics conventions that v1.5 treats as hard constraints (14D input, Jacobi IC₁₃, COM projection head, PHYS-03 softening, PHYS-01 D convention, post-v1.3 SCS gate).

### Blockers/Concerns

- **Working branch is `milestone/v1.5`** (cut from master HEAD `b8b39a4`, 2026-06-10). Do NOT commit v1.5 work to master. Tag `v1.5-pre-phase-NN` before each phase; `--no-ff` merge at milestone end. Every session must surface `git status --short --branch` before any file mutation.
- **External gate:** opens on Phase 23 (research package) delivery. Phase 24.5 verifies the consolidated resolution doc before adjudication begins. Phases 25–29 cannot start until Phase 24.5 passes (which requires BOTH the consolidated resolution doc landing AND Phase 24 completion). Phase 23 is unblocked; Phase 24 is unblocked and runs in parallel with the gate window (gates on nothing external).
- **DATA-05 remediation boundary:** GAP-24-01 is resolved as a decision, not as completed data repair. The old 70 base-hier outputs (`0005`-`0059`, `0061`-`0075`) are quarantined from training, metrics, and PIPE-07 until targeted rerun from current ICs passes validation (`24-DATA05-RERUN-REMEDIATION.md`).
- **STOP protocol active:** v1.5 is a "similar adjudication milestone" per AGENTS.md governance — source-silent semantic / process-schema / cross-phase decisions must be surfaced as gaps, never invented.
- Phase 24.5 passed 2026-06-11 (READY-WITH-CAVEATS) and Phase 25 closed 2026-06-12 — Phases 26–28 proceed under the Phase 25 machinery: evidence packet before any spec edit (EVID-06), same-commit ledger wiring (D-06), phase-exit only at VERIFIED/DEFERRED; carry the resolution-doc OI caveats (OI-3/6/7/8/11/12) forward.

## Session Continuity

Last session: 2026-06-14T03:52:05.307Z
Stopped at: context exhaustion at 90% (2026-06-13)
Next action: Plan Phase 27 with `$gsd-plan-phase 27 --auto` when ready; start from .planning/phases/27-sampling-precision-and-global-scale-contracts/27-CONTEXT.md and 27-SPEC.md.

## Operator Next Steps

- Phases 23 and 24 are closed; the issue-02 consolidation input package (bundles + manifest + originals) is committed and hash-verified.
- DATA-05 70-file rerun remediation executed and validated 2026-06-11 (all eight gates closed); old artifacts archived under `simulation_data/Data/forensic/data05_gap24-01_old_outputs/`.
- Phases 25–29 unblock once the consolidated resolution doc lands and Phase 24.5 readiness verification passes (Phase 24 completion side of the gate is already met).
