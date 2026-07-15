---
gsd_state_version: 1.0
milestone: v2.0
milestone_name: CTL-PINN Training Viability Slice
current_phase: 39
current_phase_name: data-ingestion-stage-0-population-scan
status: executing
stopped_at: Phase 39 Plan 01 complete (Wave 0 test-contract scaffold); ready for Plan 39-02
last_updated: "2026-07-15T01:56:07Z"
last_activity: 2026-07-15
last_activity_desc: Completed 39-01-PLAN.md (Wave 0 nine-file test contract)
progress:
  total_phases: 7
  completed_phases: 2
  total_plans: 18
  completed_plans: 12
  percent: 29
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-07-06)

**Core value:** A thin, Stage-0-first, end-to-end training run — built from the ratified trainex-r1a decisions and the locked framework specs — that proves the CTL-PINN pipeline trains a model on the M5 Pro Mac and reaches the acceptance gate, before any effort on the full multi-stage platform.
**Current focus:** Phase 39 — data-ingestion-stage-0-population-scan

## Current Position

Phase: 39 (data-ingestion-stage-0-population-scan) — EXECUTING
Plan: 2 of 7 (Plan 01 Wave-0 test contract complete)
Status: Executing Phase 39
Last activity: 2026-07-15 — Phase 39 Plan 01 complete (nine-file dataset-free test scaffold)

## Deferred Items

Items acknowledged and deferred at milestone close on 2026-07-02:

| Category | Item | Status |
|----------|------|--------|
| pending_todo | trainex-r1-research-handoff | Deferred to trainex track (FUT-01/FUT-04); not v1.6 specwork |

Closeout type: `override_closeout` — the only override is the acknowledged trainex-r1 todo above; all 7 v1.6 phases are verification-passed and 32/32 requirements Complete.

## Performance Metrics

**Velocity:**

- Total plans completed: 832 (v1.0: 10, v1.1: 5, v1.2: 3, v1.3: 21, v1.4: 26)
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
| Phase 32 P01 | 11 min | 3 tasks | 6 files |
| Phase 32 P02 | 9 min | 2 tasks | 5 files |
| Phase 32 P03 | 10 min | 3 tasks | 6 files |
| Phase 32 P04 | 7 min | 2 tasks | 4 files |
| 32 | 4 | - | - |
| 33 | 4 | - | - |
| Phase 34 P01 | 8min | 3 tasks | 8 files |
| Phase 35-loss-energy-weight-contracts P35-02 | 728 | 2 tasks | 2 files |
| Phase 35 P03 | 12 min | 3 tasks | 2 files |
| Phase 35 P04 | 11 min | 3 tasks | 3 files |
| 35 | 4 | - | - |
| 37 | 5 | - | - |
| Phase 38 P04 | 9min | 3 tasks | 6 files |
| Phase 39 P01 | 18min | 3 tasks | 9 files |

## Accumulated Context

### Roadmap Evolution

- v1.0: Codebase Cleanup (Phases 1-4) — shipped 2026-03-20
- v1.1: LaTeX Modularization Verification (Phases 5-8) — shipped 2026-03-22
- v1.2: PINN Implementation Readiness (Phase 9) — complete; 3 thematic docs + MIGRATION.md + README.md written, verified and validated
- v1.3: Markdown Conversion Verification & Correction (Phases 10-15, 15.1) — shipped 2026-05-08; post-ship SCS gate correction verified 2026-05-15
- v1.4: Resolving 01 Architecture and Physics Foundations (Phases 16-22, plus inserted Phase 20.5) — shipped 2026-06-09. All phases closed; archived under `.planning/milestones/v1.4-*`. EDL support remains a non-canonical support workflow under `.planning/research/edl/`.
- v1.5: Resolving 02 Data Pipeline and Validation (Phases 23-29) — shipped 2026-06-17. 36/36 requirements mapped; standard granularity; 8 phases (incl. inserted 24.5). Phase 23 (research package) first; Phase 24 (verification + DATA-07 addendum) ran in parallel with the external-research gate; Phases 25-29 gated on the resolution doc AND Phase 24. Spec edits limited to `ctl_instruction.md` and `pinn_architecture.md` (SCOPE-08/09/10). Branch `milestone/v1.5` from master HEAD `b8b39a4`; `--no-ff` merged to master (fe9b3c92) and archived under `milestones/v1.5-*` 2026-06-17 (tag v1.5).
- v1.6: Resolving 03 Curriculum and Training Loop (Phases 30-36) — roadmap created 2026-06-17. 32/32 requirements mapped; standard granularity; 7 phases (no inserted decimal). Phase 30 (research package) first and ungated; its delivery opens the external resolution-doc gate. Phase 31 (resolution-doc readiness verification, operational, 0 IDs) gates Phases 32-36. Phase 32 stands up the evidence ledger and adjudicates the headline conflicts (D-04/D-05/D-06 + `D=6.694` + M14) before the contract phases transcribe verdicts: Phase 33 (CURR), Phase 34 (LOOP), Phase 35 (LOSS). Phase 36 (VER) executes acceptance checks + handoff. Specwork-only (SCOPE-13/14/15); `pinn/` never grounding (SCOPE-10). Branch `milestone/v1.6` (worktree) cut from the v1.5 deliverable tip `88aa1e4f`; rebased onto completed master 2026-06-17 once v1.5 shipped.
- v2.0: CTL-PINN Training Viability Slice (Phases 37–43) — roadmap created 2026-07-06. The project's first **build** milestone, opening the trainex track. 42 requirements mapped; standard granularity; 7 phases continuing from v1.6's Phase 36 (no reset). Dependency-ordered, no external gate: 37 ENV (dev env + D1-p probe) → 38 NET (`pinn/` rebuild, FUT-01) → 39 DATA (in-memory adapter + Stage-0 scan) → 40 TRAIN (Adam→L-BFGS Stage-0 loop, FUT-04) → 41 CTRL (config/checkpoint/guards/determinism) → 42 OPS (operator runbook + monitoring) → 43 ACC (verify + Stage-0 pilot + go/adjust/rethink verdict). Grounded in the ratified trainex-r1a decision set (2026-07-05); `pinn/` ban lifted; owner-carved decisions built as seams. Planning on `master`; build in `.worktrees/trainex`.
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

- [D1-p RESOLVED 2026-07-12]: Owner recorded **fp32-MPS** (Option A) for D1-p, resolving GAP-37-01 and retiring the same-day deferral below. Verbatim ruling (*"...we will remain with the entire training happening on the MacBook Pro with M5 chip. Let's carry on with that choice and decision for now."*) plus an explicit branch-naming confirmation (owner selected "fp32-MPS" from {fp32-MPS, fp64-CPU, keep deferred}) are recorded in the gap register, including the R-6 dual-arm tolerance ratification (fp64-CPU reference arm; fp32-MPS within ~1e-4). Production default: `precision=float32, device=mps`; fp64-CPU remains the in-framework escape hatch (ENV-04). **Phase 38 (NET) UNBLOCKED**; ENV-03 closable. Single-machine M5 Pro training reaffirmed — a Lenovo/multi-machine split is a later cost-benefit question outside v2.0. No code changed (CTX-14): `pinn/runtime.py` encodes no default; the Phase 40/41 training config consumes the recorded value.
- [D1-p DEFERRED 2026-07-12]: Owner recorded an explicit DEFERRED verdict for D1-p (precision branch, fp32-MPS vs fp64-CPU) at the Plan 37-05 blocking checkpoint. Verbatim: *"i picked the wrong option. let's defer that and we'll decide on this later."* The owner retracted an initial fp32-MPS selection. **Phase 38 (NET) is blocked at the D1-p seam until the owner records a branch.** The agent did NOT choose, recommend, or apply a precision default. The retained dual-arm evidence (`evidence/precision/20260712T150406Z/`) is reusable; no re-run required when the owner records a branch. Full gap record: GAP-37-01 (`.planning/phases/37-developer-environment-precision-adjudication/37-GAPS.md`); milestone index: `.planning/milestones/v2.0-GAPS.md`.
- [integrity-r2-clearance 2026-07-11]: Owner disposed the integrity-r2 pre-build audit punch-list (MASTER-FINAL-RESOLUTION, status candidate/owner-disposes, verdict NO-GO): **PB-1 Option A + interim floor** (Stage-0/1a/1b `s_min` criterion becomes data-derived `s₀` ratified at the Phase 39 DATA-06 scan; interim `s₀ = 0.01`), **PB-2/PB-3/PB-4/PB-5 all Option A** (five-term Huber loss catalog; corrected replay/lookahead data/collocation contract; `physical_key` grouped-split invariant; Tier-1 dataset-count correction — corpus arithmetic becomes ≈8.23M snapshots ≈0.72 GB fp32, no ratified decision changes). Owner authorized a bounded spec micro-pass on `ctl_instruction.md` now (departing from the delivery-note "future spec milestone" routing): `s_min` repair, Set 1b/2a count swap, `compute_L_norm` degenerate-branch fix (IR2-007), DATA-05 quarantine historical note (IR2-008). v2.0 REQUIREMENTS/ROADMAP patched accordingly (NET-04, DATA-02, DATA-04, DATA-05, DATA-06 + Phase 38/39 criteria). **Phase-37 pre-build gate: CLEARED** (nothing waived). Clearance record: `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/CLEARANCE.md` (trainex worktree, `milestone/v1.7` commit `09c972c6`).
- [v2.0-init 2026-07-06]: v2.0 is the first **build** milestone (trainex track), scoped as the postspec-r1 **viability slice** (Stage-0 first); the full multi-stage platform is deferred pending an ACC-06 go/adjust/rethink verdict. Owner chose a major bump (v1.7 → v2.0) marking the spec→implementation inflection. Grounding is authoritative, not a candidate verdict source: the ratified trainex-r1a decision set (2026-07-05; D1–D7 / B-1–B-11 + §5 first-run recipe) for build-engineering, and the locked v1.4/v1.5/v1.6 specs for the science. The `pinn/` live-code ban is **LIFTED** (FUT-01 rebuilds from specs). Five owner-carved decisions (D1-p precision, D4-a checkpoint ceiling, RECOVER budget + HALT/guard thresholds R-1/R-2, B-5 resume-field list) are built as seams with safe defaults and calibrated/ratified by the owner at their designed moments — the build analog of the STOP protocol; the agent surfaces evidence, it does not pick the values.
- [v2.0-roadmap 2026-07-06]: 7 phases (37–43), standard granularity, continuing numbering from v1.6's Phase 36. 42/42 requirements mapped 1:1 by category (ENV=4, NET=5, DATA=6, TRAIN=7, CTRL=8, OPS=6, ACC=6). Straight dependency order 37→43, no external research gate (unlike v1.4–v1.6 — the research is already delivered and ratified). Planning artifacts committed on `master`; build execution in `.worktrees/trainex` on `milestone/v2.0` (renamed/created from the stale anticipatory `milestone/v1.7` at first phase execution).
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
- [Phase 32 Plan 32-01]: Created first-write baselines plus issue-03 evidence protocol/template/ledger machinery; the resolution doc remains a candidate verdict source, not authority, and live `pinn/` code remains NOT grounding.
- [Phase 32 Plan 32-01]: D-04, D-05, and D-06 remain owner-routed decisions; Plan 32-01 seeded routing without selecting causal mode, `s_min` gate frame, or static epsilon strategy.
- [Phase 32 Plan 32-01]: Every non-headline row must get an evidence packet and ledger update before downstream spec edits; `FIX_APPLIED` is not terminal.
- [Phase 32]: Plan 32-03: D-04 remains defer-with-blocker; no causal-training Option A/B/C selected without explicit owner instruction. — The issue doc and candidate verdict source preserve D-04 as owner-routed, and Phase 32 must not select a semantic default.
- [Phase 32]: Plan 32-03: D-05 remains defer-with-blocker; no final s_min stage-gate frame selected without explicit owner instruction. — Matched-Plummer loss-side evidence is recorded, but the curriculum stage-gate frame remains owner-routed.
- [Phase 32]: Plan 32-03: D-06 remains defer-with-blocker; loss-side epsilon_train = 1e-5 stays locked while static/invariant epsilon remains owner-routed. — The resolution doc narrows the open decision to static/invariant context; no sensitivity study or explicit owner instruction resolves it.
- [Phase 32]: Plan 32-04 closed Phase 32 structural verification; closeout remediation subsequently registered the known D-04/D-05/D-06 owner-route blockers as GAP-32-01/02/03 with `DEFERRED` status per user instruction. D-04, D-05, and D-06 remain defer-with-blocker owner-routed decisions; all final structural and closeout guards passed.
- [Phase 32]: Plan 32-04 protected-path and baseline guards passed before closeout — Framework specs, frozen/read-only reports, final resolution doc, .planning/STATE.md, and pinn/ remained untouched during task verification; the unrelated dirty docs patch, gap-file state, untracked pinn state, and resolution-doc identity matched the Phase 32 baseline.
- [Phase 32 closeout 2026-06-21]: Created `32-GAPS.md` and `.planning/milestones/v1.6-GAPS.md` for GAP-32-01/02/03; added the ledger `Owner Phase` legend without changing owner values; reconciled Phase 32 complete -> Phase 33 next state.
- [Phase 34]: B-07 (LOOP-01): consume resolution-doc §1.4 modified verdict; keep 240/16 and n_pts_cap=32 as provisional defaults; route source-silent edge cases to 34-GAPS.md by Plan 34-03
- [Phase 34]: B-08 (LOOP-02/03): consume resolution-doc §1.5 modified verdict; formalize two independent point sets; carry 8192/4096 as provisional; defer mandatory collocation 50/50
- [Phase 34]: M16 (LOOP-06): consume resolution-doc §1.10 defer; record dt_out scaling as realized-as-deferred with no transcribed formula and no probe
- [Phase 34]: ALM mu_p clamp (LOOP-05): consume resolution-doc §1.18 defer; reject dense-residual ALM from default loss; clamp conditional on optional scalar-conservation ablation
- [Phase 34]: LOOP-04 reuses existing Phase 32 M14 packet; no new M14 packet authored
- [Phase 34]: LOOP-07 and LOOP-08 are v1.5 carry-forwards with no ledger row and no packet
- [Phase 34]: Phase 34 evidence packets mirror Phase 32 template/schema without reinvention
- [Phase 35]: No new semantic/spec decision was invented in 35-02; loss contract text follows Phase 35 evidence packets and owner-ratified D-04 Option A.

### Pending Todos

v2.0 CTL-PINN Training Viability Slice initialized 2026-07-06. Next: `/gsd-plan-phase 37` (or `/gsd-discuss-phase 37`) from the `.worktrees/trainex` worktree once its branch is aligned to `milestone/v2.0`.

- [x] Update PROJECT.md with the v2.0 Current Milestone (goal, target features, grounding, git workflow); archive v1.6 context
- [x] Reset STATE.md for v2.0 (`gsd-tools state.milestone-switch`)
- [x] Define v2.0 requirements (42 across ENV/NET/DATA/TRAIN/CTRL/OPS/ACC)
- [x] Create v2.0 roadmap (Phases 37–43; 42/42 mapped)
- [ ] At first phase execution: align the `.worktrees/trainex` branch to `milestone/v2.0` (currently the stale `milestone/v1.7`); tag a pre-phase recovery point
- [ ] Carried-forward: `trainex-r1-research-handoff` (r1a ratified 2026-07-05; r1b tuning round pending — a Future item) and `d-06-static-epsilon-sensitivity-check` (spec-side sensitivity question, not a v2.0 build phase) remain in `.planning/todos/pending/`, unlinked to v2.0 phases

### Prerequisites

**v1.4/v1.5/v1.6 shipped and merged to master** — the framework specs (`ctl_instruction.md`, `pinn_architecture.md`) are complete and authoritative: 14D input `[τ, IC₁₃]`, Jacobi IC₁₃, mass-weighted COM projection head, PHYS-02 AD contract, PHYS-03 softening, PHYS-05 scheduled weights, the post-v1.3 SCS gate (`ε_H > 10⁻⁵` / `SCS > −5`), raw-mass `D ≈ 4.6416`, the Stage 0–6 curriculum + CURR-03 stage-exit machine, LOOP-01..08 batch/loop contracts, LOSS-01..04 loss contracts. **Trainex-r1a decision set ratified 2026-07-05** (D1–D7 / B-1–B-11 + §5 first-run recipe). Both are v2.0's authoritative grounding. The on-disk `simulation_data/` admitted set + v1.5-verified dataset facts are the training data. **Hardware confirmed** (R-3 CLOSED): Apple M5 Pro, 24 GB unified memory, 15-core CPU.

### Blockers/Concerns

- **Build execution branch:** v2.0 code work happens in `.worktrees/trainex` on `milestone/v2.0`. Alignment completed at merge commit `89daf842`, preserving the trainex-only history and the master planning/spec updates. Do NOT commit v2.0 build code to `master`. Every session surfaces `git status --short --branch` before any file mutation.
- **Owner-carved decisions are NOT invented:** D1-p (precision), D4-a (checkpoint ceiling), the RECOVER retry budget + HALT/guard thresholds (R-1/R-2), and the B-5 resume-field list are built as seams with safe defaults and calibrated/ratified by the owner at their designed moments (probe / smoke test / Stage-0 pilot / before run #1). The agent surfaces evidence; it does not pick these values.
- **`pinn/` ban lifted for v2.0:** FUT-01 rebuilds `pinn/` FROM the specs; v2.0 is the first milestone to write production `pinn/` code. The v1.3-era `basic_architecture.py` / `data-processing-pipeline-full.py` are reference-only and replaced wholesale.
- **Spec inputs are read-only in v2.0:** a build-discovered spec defect is surfaced as a gap and routed to a spec milestone; v2.0 implements the specs, it does not edit them.
- **No external research gate:** unlike v1.4–v1.6, v2.0 has no candidate-verdict-source gate — the research (trainex-r1a) is already delivered and ratified. Phases run in straight dependency order 37 → 43.

## Session Continuity

**Resume file:** .planning/phases/38-pinn-model-rebuild-from-specs-fut-01/38-CONTEXT.md

Last session: 2026-07-13T12:15:50.268Z
Stopped at: Phase 38 Plan 04 complete; Plans 38-05 and 38-06 pending
Next action: Execute Phase 38 Plan 05, then Plan 06; the NET rebuild consumes the recorded fp32-MPS default (`precision=float32, device=mps`), with fp64-CPU for the gradcheck rung.

## Operator Next Steps

- **Phase 38 is unblocked:** D1-p recorded as **fp32-MPS** in GAP-37-01 (`RESOLVED-WITH-INSTRUCTION`, verbatim quote filled). Production default `precision=float32, device=mps`; fp64-CPU escape hatch stands (ENV-04); no code changed (CTX-14).
- Continue Phase 38 with Plans 38-05 then 38-06; Plans 38-01..38-04 are complete. Note for rungs 3–4: no Brutus trajectory file exists in this worktree — probes are path-parameterized (CTX-26); point them at the real dataset location at execution time.
- Phase 37's verification surface: ENV-01/02/04 GREEN; ENV-03 evidence retained and validated + owner verdict recorded; all 55 tests/phase37 tests pass; the committed environment substrate is re-derivable on the M5 Pro.
