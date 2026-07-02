# Milestones

## v1.6 Resolving 03 Curriculum and Training Loop (Shipped: 2026-07-02)

**Phases completed:** 7 phases, 30 plans, 49 tasks

**Key accomplishments:**

- Read-only PKG-08 characterization of both curriculum-relevant reports plus a provisional PKG-07 claims register (CLM-01..CLM-19) carrying the D-17 no-in-milestone-verification boundary and the D=6.694 vs D≈4.6416 seed-conflict, with content-SHA + source-commit provenance seeded for byte-fidelity.
- Authored the PKG-05 document-list + consolidation plan (`30-CONSOLIDATION-PLAN.md`), locked the MULTI-COMPANION package form, classified the framework specs NEVER consolidated (D-04), assigned the standalone verified-facts reference to 30-03 Task 2 (F11), posed the three open inclusion calls, and FILLED the D-09 APPROVED record under the user's pre-authorized approve-as-proposed waiver — each decision cross-checked against the 30-RESEARCH Consolidation Map with zero conflicts. Assembly (30-03) is now unlocked.
- Authored the four upload companions for the doc-03 ERW package: 19 neutrally-framed research questions in issue-03 section order (three named decisions + the D conflict posed unsettled with locked/open delineation), the verbatim SCOPE-12 hard-constraints preamble, a non-binding per-finding resolution-doc skeleton, and the uploaded PKG-07 claims register — with the claims seed extended after the full issue-03 read.
- Delivered the complete repo-blind doc-03 ERW package (single-entry-point master + paste-ready prompt + round-root delivery note over the existing companions/snapshots), passed the F12 self-containment cross-check both directions, and opened the external resolution-doc gate via gsd-tools handlers with STATE progress counters verified unchanged.
- Gate verdict READY-WITH-CAVEATS on the landed issue-03 resolution doc — all 18 selected findings covered, zero v1.5-verified-fact contradictions, zero SCOPE-12 violations; 12 non-blocking caveats routed to Phase 32 EVID-15 / Phases 33–35 / FUT.
- Issue-03 adjudication machinery with first-write baselines, fixed verdict/status protocol, packet template, seeded 18-row ledger, and verification inventory
- Final Phase 32 evidence-framework closeout with packet coverage, ledger coverage, protected-path guards, owner-decision discipline, and baseline preservation verified
- Multi-Stage Data Stratification by Difficulty section
- Stage Transition Criteria section
- 1. Combined dirty-doc SHA-256 mismatch (Wave 1-3 STATE.md tracking-write artifact)
- Captured the Phase 34 baseline, stood up the evidence workspace, authored the four packet-before-edit evidence packets (B-07, B-08, M16, ALM), and synchronized their Phase 32 ledger links so the downstream spec-edit plans can proceed without inventing evidence or process schema.
- Transcribed the LOOP-04 merged adaptive median-based gradient-clipping contract with a single canonical home per half: mechanism in `pinn_architecture.md` §4.4 and per-stage C-schedule `7-10 / 5 / 3` in `ctl_instruction.md`, linked by bidirectional `AC-LOOP-04` anchors.
- Landed the LOOP-01/02/03 provisional batch-construction contract, the LOOP-06 realized-as-deferred collocation-scaling body, the LOOP-07/08 provisional training-side metric roles, and the opaque total-loss ordering skeleton in `ctl_instruction.md`, and opened GAP-34-01 for the source-silent batch edge cases.
- Reconciled the pinn_architecture.md batch-construction inconsistency with ctl_instruction.md as canonical and transcribed the LOOP-05 optional/deferred ALM contract, leaving the default training loop ALM-free and the LOOP-04 cross-file invariants intact.
- Durable Phase 34 goal-backward verification report and five LOOP-related Phase-32 ledger rows closed VERIFIED, with Phase-34 completion explicitly gated on OPEN GAP-34-01.
- Transcribed the owner-ratified Option A batch edge-case policy into the `ctl_instruction.md` Mini-Batch Construction LOOP-01 contract (provisional) and cleared the Phase-34 closure gate recorded in `34-VERIFICATION.md`, with the LOOP-04 cross-file and locked-convention guards re-verified intact.
- 1. [Rule 3 - Blocking verification anchor] Restored the plan's stable multi-component loss anchor
- Phase 35 loss-contract verification with dual-register D-04 closure and five VERIFIED issue-ledger rows.
- Build the Phase 36 acceptance-check spine (contract manifest + probe suite)
- Run AC suite and record evidence
- Drive the Phase 32 issue ledger to terminal state by verifying D-05/D-06 transcription and promoting those two PENDING rows.
- Write the v1.6 milestone-closure handoff: classify every ledger finding, reconcile all four framework-spec SI entries, and route implementation-shaped findings to FUT-01/FUT-04.
- Phase 36 verification + reconciliation + final batch re-verify.

---

## v1.5 Resolving 02 Data Pipeline and Validation (Shipped: 2026-06-17)

**Delivered:** Evidence-verified data-pipeline and validation-metric design contracts for `ctl_instruction.md` / `pinn_architecture.md`, with every issue-02 finding adjudicated against the on-disk dataset and a user-produced resolution doc, plus a complete FUT-01 implementation handoff.

**Phases completed:** 8 phases, 27 plans

**Key accomplishments:**

- Assembled the framed research package (annotated document list, "claimed, unverified" dataset figures, read-only DQA characterization) that opened the external resolution-doc gate.
- Verified every empirical dataset claim (ID gaps, blacklist, gold-counterpart gap, footer variance, mass drift, snapshot/`dt_out` distributions) against `simulation_data/` with re-derivable probes; closed DATA-05 via a 70-file base-hierarchical rerun.
- Stood up the evidence-packet / EVID-10 root-cause adjudication machinery and the re-verification issue ledger; adjudicated the SCS-threshold, `D=6.694`, and M11/M12 conflicts at root cause.
- Locked the DataLoader ingestion/selection contracts (B-06 gate, B-11 ID-resolution, M11 blacklist, M13 gold-counterpart, D7 footer heterogeneity, D-03 HDF5 format) and the sampling/precision/global-scale contracts (M12 points, float64/Decimal, `dt_out`/stage-query, `compute_globals`).
- Defined canonical SCS/SASD/IPR/PSC validation-metric contracts threshold-aligned to the locked gate, with training-loop usage deferred to doc-03.
- Executed the 13-check acceptance suite (G1–G8 milestone-closure gate PASS), closed the 19-row ledger (18 VERIFIED + 1 DEFERRED), reconciled 3 SI dispositions, and produced the two-artifact FUT-01 handoff (gold: 117 validatable + 67 permanent-absent).

**Stats:**

- 36/36 requirements satisfied; 8/8 phases verified; 10/10 STOP-protocol gaps RESOLVED-WITH-INSTRUCTION, 0 open.
- G1–G8 milestone-closure gate PASS (2026-06-17); milestone audit verdict `tech_debt` with 3 non-blocking items closed at archive.
- `milestone/v1.5` merged to master `--no-ff` as `fe9b3c92` (2026-06-17); branch tip `b8b39a4` preserved at tag `v1.5-pre-merge-backup`.

**What's next:** v1.6 (Issue-03 "Resolving CTL") starts fresh requirements; FUT-01 consumes the dataset-finalization handoff (FO-1: promote 117 validated gold + 184→67 cascade; then FO-2: PSC/SCR first-run sanity, SASD/IPR/PSC constant recalibration, AC-VAL-04 numeric run).

---

## v1.4 Resolving 01 Architecture and Physics Foundations (Shipped: 2026-06-09)

**Delivered:** Evidence-backed, physically coherent framework specifications with executable acceptance checks and a complete downstream implementation handoff.

**Phases completed:** 8 phases, 26 plans, 65 tasks

**Key accomplishments:**

- Established the evidence-packet, EVID-05 adjudication, STOP-gap, and re-verification protocols used across all eight phases.
- Locked coherent 14D input, 13-component IC, raw 9D position-output, COM projection, frame, gauge, and sampling-coordinate contracts.
- Defined physically consistent scaling, componentwise AD, matched softening, conservation regularizers, and loss-balancing semantics.
- Settled SIREN, LayerNorm, inertia, energy, mass, and normalization contracts while preserving explicit FUT-01 implementation divergences.
- Executed all five numerical acceptance probes and closed 32/32 requirements, 8/8 phase verifications, and all 25 STOP-protocol gaps.
- Completed presentation-preserving cleanup and archived the full phase history, including the FUT-05 author-comment handoff.

**Stats:**

- 258 files changed across the milestone branch range
- 40,357 additions and 5,177 deletions
- 8 phases, 26 plans, 65 tasks
- 22 days from branch baseline to ship

**Git range:** `dffc7a5` → `833930f`

**What's next:** Define the next milestone and fresh requirements; production PINN alignment remains a documented candidate rather than an assumed scope.

---

## v1.0 Codebase Cleanup (Shipped: 2026-03-20)

**Phases completed:** 4 phases, 10 plans, 9 tasks

**Key accomplishments:**

- (none recorded)

## v1.1 LaTeX Modularization Verification (Shipped: 2026-03-22)

**Phases completed:** 4 phases (5–8)

**Key accomplishments:**

- Verified content completeness across all 5 modular LaTeX structures (automated diff)
- Confirmed preamble parity (packages, macros, commands) between original and modular preambles
- Verified structure fidelity (section hierarchy, labels, references, citations, floats)
- Confirmed all 5 modular structures compile cleanly (0 errors, 0 new warnings)

## v1.2 PINN Implementation Readiness (Shipped: 2026-05-08)

**Phases completed:** 1 phase (9), 3 plans

**Key accomplishments:**

- Consolidated 7 scattered issue reports into 3 thematic documents (01-architecture, 02-data-pipeline, 03-curriculum)
- No unique findings lost; each thematic document has distinct, non-overlapping coverage
- Produced MIGRATION.md and README.md for migration tracking; VERIFICATION-REPORT.md (PASS) and VALIDATION.md (all checks PASS)

## v1.3 Markdown Conversion Verification & Correction (Shipped: 2026-05-08)

**Phases completed:** 7 phases (10–15, 15.1), 21 plans

**Key accomplishments:**

- Verified all 6 LaTeX→markdown conversions with one-to-one injection fidelity
- Corrected 7 critical, 19 major, and 17 minor conversion errors in Phase 15.1
- Archived unselected markdown candidates to `_archive/` directories
- Produced verification reports documenting all discrepancies and fixes
- Preserved inter-document inconsistencies faithfully (deferred reconciliation to v2)
- Cleaned up stale debug sessions and quick-task artifacts from prior milestones
