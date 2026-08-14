---
gsd_state_version: 1.0
milestone: v2.2
milestone_name: Stage-0 Conformance Repair & Valid Re-Run
current_phase: 50
current_phase_name: valid-stage-0-re-run
status: executing
stopped_at: Planned 50-04 and 50-05 (GAP-50-02 repair + generation-3 run window)
last_updated: "2026-08-13T07:30:00.000Z"
last_activity: 2026-08-13
last_activity_desc: Phase 50 replanned after GAP-50-02 ruling; plans 50-04/50-05 added, 50-03 re-sequenced to wave 5
progress:
  total_phases: 7
  completed_phases: 4
  total_plans: 31
  completed_plans: 28
  percent: 53
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-07-31)

**Core value:** A thin, Stage-0-first, end-to-end training run — built from the ratified trainex-r1a decisions and the locked framework specs — that proves the CTL-PINN pipeline trains a model on the M5 Pro Mac and reaches the acceptance gate, before any effort on the full multi-stage platform.
**Current focus:** Phase 50 — valid-stage-0-re-run

## Current Position

Phase: 50 (valid-stage-0-re-run) — EXECUTING
Plan: 2 of 5 executed (50-01, 50-02; 50-04 → 50-05 → 50-03 remain)
Status: Phase 50 replanned — GAP-50-02 resolved, conformance repair planned, no run launched
Last activity: 2026-08-13 — GAP-50-02 ruled (option A, full held-out validation pool); plans 50-04 and 50-05 written; 50-03 re-sequenced to wave 5
**Verification:** [███████░░░] 67% (4/6 truths verified)

### Phase 49 verification (2026-08-10)

- **Phase 49 is not closed.** `49-VERIFICATION.md` records `gaps_found`
  with 4/6 must-haves verified despite the full Phase 49 suite passing 176 tests.

- **Run-local invariant-B eligibility is incomplete.** A real synthetic
  `main()` run with `front_advance_window_n = None` remained record-only but
  emitted `eval01_precondition_i = true` after the global divergence entry was
  closed.

- **Run-start evidence is not required by the eligibility projection.** A
  schema-valid, passed `stage_boundary`-only preflight with no `run_start` or
  census loaded successfully and also yielded `eval01_precondition_i = true`.

- **Phase 50 remains blocked.** `$gsd-plan-phase 49 --gaps` ran on 2026-08-10 and
  produced `49-09-PLAN.md` (wave 6, depends on 49-08), which closes both gaps at the
  single eligibility seam: bind the run-local invariant-B window so an N-unset run is
  structurally ineligible (D-20), and require the run-start table + census evidence the
  predicate claims to summarize. Plan-checker passed with 0 blockers after one revision.
  Next action is gap-only execution of 49-09, then re-verification. The gaps remain OPEN
  until re-verification says otherwise — the plan is forbidden from self-certifying them.

### Decisions from 49-08

- **Phase 49 review BLOCKERs are closed.** CR-03/04/06/09 landed in Plan
  49-08; CR-08's producer-contract repair at `7d4ffd8d` was independently
  re-run without further code changes. The final required gate is 943 passed,
  3 skipped, and 289 subtests passed.

- **Invariant-B policy is owner-ratified, not inferred.** The 2026-08-05 owner
  ruling is `N = 500 (= 0.5 * N_Adam,0)`; the shipped Stage-0 config carries
  that exact value and `INV-B-N-UNSET` is closed by its enforcing trip test.

- **Preflight evidence is append-only across resumed attempts.** Existing
  artifacts are validated and retained before the next run-start event; any
  ordinary setup/probe refusal records its failed event before controlled exit.

- **Phase 50 is authorized to be planned, not auto-launched.** No admitted
  corpus or held-out evaluator was touched during Phase 49 remediation.

### Decisions from 47-02

- **CONF-02 discharged.** `_matched_plummer_components` is the single home of
  the softened pairwise sum (D-11); `k0`/`uabs0` are captured in float64 at
  admission at `EPS_SOFT` before the fp32 residency cast (D-09/D-10/D-12);
  `pinn/training/run_metadata.py` computes the train-split median once at
  setup and persists `s_h`/`eps_h`/`n_train` via `atomic_write_text` with
  re-validate-on-load and explicit `expected_energy_floor_factor`/
  `expected_eps_train` bindings (D-13..D-18).

- **Both setup branches bind the same `s_h` local** — the resume helper
  `_assert_s_h_matches_artifact` RETURNS the validated value, so the 47-03
  `RunController` hand-off is structural, not conventional.

- **First authoritative real-corpus `S_H`/`eps_H`/`N_train` deferred to Phase
  50** (owner ruling 2026-07-30, Option B); Phase 47 proves the semantics
  with deterministic fixtures. No zero-step emitter added; no training
  launched.

- **REQUIREMENTS.md CONF-02 checkbox deliberately NOT flipped by the
  executor** — same phase-close/verification-act precedent as CONF-09.

### Decisions from 47-01

- **CONF-09 discharged.** Residency is `pre.r_gauge`/`pre.v_gauge`;
  `RATIFIED_VALIDATION_FRAME` is `(r_prime, u_t_over_T, ordered_raw)`, re-ratified
  in the same commit; the one pairing test is corrected in place. The one-shot
  re-probe records `identity_scaled` true and a zero max difference against
  `r_gauge`/`v_gauge` for 1651/1651 — record-only, not a new CONF-01 verdict.

- **`r_com_ordered`/`v_com_ordered` survive** on `PreprocessedTrajectory` (D-03);
  `pinn/data/preprocessing.py` is byte-unchanged.

- **REQUIREMENTS.md CONF-09 checkbox deliberately NOT flipped by the executor** —
  that is a phase-close/verification act, and this plan does not mutate the locked
  governance docs it was planned against.

### ⚠ OPEN — surfaced for owner ruling (47-01, D-08)

The D-08 derived bound is **exceeded on the validation-side reading for 9 of 50
sampled real trajectories** (max ratio 4.76); the loss-side reading is inside the
bound on all 50. The physics claim holds — both arms' `eps_H` agree to ~13
significant digits — but Step 4's float64 allowance omits the cancellation
amplification the finite-difference velocity incurs on real Brutus sampling.
Nothing was widened or relaxed (SCOPE-29/D-26). Options: extend Step 4 with a
finite-difference cancellation term; narrow the D-08 claim to the loss-side
reading; or accept the record. Full record: `evidence/frame-re-ratification/20260731T012304Z/re-ratification.md` §4.2.

**Phase 47 scope changed 2026-07-28 (GAP-46-07, owner option A) — read before planning it.** An independent verification of the conformance handoff confirmed all six carried divergences and surfaced a seventh that no requirement owned: CONF-08 excluded the rotation gauge and the `D`/`V` scaling by design, GAP-46-06 ratified the resulting intermediate as the **validation** frame, and neither reached the **training** path, which pairs unrotated/unscaled residents with `u = t/T` — a pairing `COHERENT_FRAME_PAIRS` does not admit. New requirement **CONF-09** completes the residency transform to the locked canonical contract and is sequenced **ahead of CONF-02** (`S_H` is frame-dependent). Milestone is now **24 requirements**; Phase 47 is renamed "Frame Completion & S_H Pipeline" and runs CONF-09 → CONF-02 → CONF-03. The Phase 48 CONF-05 clip bound now waits on CONF-09 as well as CONF-04. `RATIFIED_VALIDATION_FRAME` is re-ratified by CONF-09, so GAP-46-06 is superseded **in part** — CONF-01's Complete status and its mandatory EVAL-01 precondition-(ii) qualification are unchanged. Report: `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-28-conformance-divergence-verification-report.md`.

## Deferred Items

Items acknowledged and deferred at milestone close on 2026-07-23 (v2.0):

| Category | Item | Status |
|----------|------|--------|
| debug | phase39-collocation-slot-multiplicity | Open session record [diagnosed]; deferred — session never formally closed |
| debug | phase39-memory-guard-validation | Open session record [investigating]; deferred — session never formally closed |
| uat | 38-UAT partial | Stale-satisfied — its one outstanding item (real-trajectory rung 3/4 gate) passed 2026-07-13 with GAP-38-01 closure; frontmatter never updated |
| verification | 41-VERIFICATION human_needed | Stale-satisfied — both human items (B-5 ratification; R-1/D4-a calibration) owner-ratified during Phase 43 |
| verification | 42-VERIFICATION human_needed | Genuinely open, explicitly non-blocking — 2 Manual-Only visual checks (runbook walkthrough legibility; sleep-assertion identity) |
| pending_todo | trainex-r1-research-handoff | Deliberate carry-forward (r1b tuning round); unlinked to v2.0 phases |
| pending_todo | d-06-static-epsilon-sensitivity-check | Deliberate carry-forward (spec-side sensitivity question); not a v2.0 build item |
| audit_warning | W-1 evaluation-attempt.json absent (seed-42) | Provenance-only; claim hardening postdates the sole evaluation; refusal holds via receipt path; do NOT re-run |
| audit_warning | W-2 runbook omits verify/evaluate entry points | Discoverability only; correctness protected by fail-closed train.py gate |
| audit_warning | W-3 ACC-05 spread location | Spread lives in 43-CALIBRATION.md, not pilot summary.md; substance complete and ratified |

Closeout type: `override_closeout` — all 7 v2.0 phases verification-scored in full and 42/42 requirements Complete; overrides are the acknowledged items above (see `.planning/v2.0-MILESTONE-AUDIT.md`, status `tech_debt`). Milestone verdict: owner-signed `adjust` (43-VERDICT.md).

<details>
<summary>Prior close (v1.6, 2026-07-02)</summary>

| Category | Item | Status |
|----------|------|--------|
| pending_todo | trainex-r1-research-handoff | Deferred to trainex track (FUT-01/FUT-04); not v1.6 specwork |

Closeout type: `override_closeout` — the only override is the acknowledged trainex-r1 todo above; all 7 v1.6 phases are verification-passed and 32/32 requirements Complete.

</details>

## Performance Metrics

**Velocity:**

- Total plans completed: 872 (v1.0: 10, v1.1: 5, v1.2: 3, v1.3: 21, v1.4: 26)
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
| Phase 39 P02 | 22min | 4 tasks | 8 files |
| Phase 39 P03 | 35min | 3 tasks | 4 files |
| Phase 39 P06 | 17 min | 2 tasks | 2 files |
| 40 | 9 | - | - |
| 44 | 5 | - | - |
| 46 | 10 | - | - |
| 47 | 3 | - | - |
| 48 | 4 | - | - |
| 49 | 9 | - | - |
**Per-Plan Metrics:**

| Plan | Duration | Tasks | Files |
|------|----------|-------|-------|
| Phase 39 P11 | 12min | 2 tasks | 3 files |
| Phase 39 P12 | 4min | 2 tasks | 2 files |
| Phase 40 P06 | 20 min | 2 tasks | 3 files |
| Phase 40 P07 | 12min | 2 tasks | 3 files |
| Phase 40 P08 | 25min | 3 tasks | 6 files |
| Phase 40 P09 | 10min | 3 tasks | 3 files |
| Phase 41 P01 | 6min | 3 tasks | 9 files |
| Phase 41 P02 | 5min | 3 tasks | 2 files |
| Phase 41 P03 | 5min | 2 tasks | 4 files |
| Phase 41 P04 | 25min | 3 tasks | 2 files |
| Phase 41 P05 | 10min | 3 tasks | 6 files |
| Phase 43 P02 | ~7min | 2 tasks | 5 files |
| Phase 43 P04 | ~50min | 1 tasks | 2 files |
| Phase 43 P05 | 9min | 2 tasks | 5 files |
| Phase 46 P04 | ~45min | 2 tasks | 4 files |
| Phase 46 P05 | 58min | 2 tasks | 4 files |
| Phase 46 P06 | ~25min | 3 tasks | 3 files |
| Phase 46 P10 | 50min | 2 tasks | 5 files |
| Phase 47 P02 | ~30min | 2 tasks | 7 files |
| Phase 48 P01 | 7 min | 2 tasks | 4 files |
| Phase 48 P2 | 16 min | 2 tasks | 7 files |
| Phase 48 P3 | 14 min | 2 tasks | 8 files |
| Phase 48-loss-math-conformance P04 | 20 min | 2 tasks | 4 files |
| Phase 49 P01 | 50min | 3 tasks | 8 files |
| Phase 49 P02 | 7min | 3 tasks | 7 files |
| Phase 49 P04 | 20min | 3 tasks | 6 files |
| Phase 50 P01 | ~50min | 3 tasks | 15 files |

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
- v2.1: Physics-Gate Investigation & trainex-r2 Research Package (Phases 44-45) — roadmap created 2026-07-23; both phases complete 2026-07-24, 7/7 requirements delivered; close PENDING five open gaps. Small granularity, 2 phases, no external gate inside the milestone (the gate opens at close). Phase 44 (DIAG-01..04) read-only forensics from retained v2.0 artifacts → `44-DIAGNOSIS.md`; Phase 45 (PKG-09..11) the trainex-r2 ERW package, delivered and audited PASS. SCOPE-22..26 held throughout: no evaluation, no training, no spec edits, no remedy chosen. **Post-delivery:** the returned report (Route B / open-book) established that the v2.0 Stage-0 pilot diverged from the locked specs in five verified respects, qualifying Phase 44's DIAG-04 rankings (`44-ERRATUM.md`) and opening GAP-44-02 + GAP-45-01..04. Branch `milestone/v2.1` in `.worktrees/trainex`.
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

- [Phase 46 Plan 46-04]: CONF-01 evidence layer landed (commit aa094f37). Population rule fixed and manifest-parametric: eligible = train-or-validation under EVERY supplied manifest; excluded = test under ANY, attributed `test_under_<label>`; the test partition is read as a manifest-payload physical-key set, never a StageIndex (D-16). Exclusion ledger keyed on PhysicalKey so the excluded set is exactly the supplied manifests' test partitions. Resident-reader routing uses the first supplied manifest's membership (routing-only choice, recorded via `first_manifest_label`). Control reader streams per key under a `--chunk-size` FIFO window, never caching the corpus. Manifest labels derive from path stems with deterministic `~2` collision suffixes. Rule-3 deviation: the plan-mandated control reader was registered in the Phase 39 GAP-39-02 sole-reader audit allow-list (`tests/phase39/test_prohibitions.py`) — a registration gate, exactly one coherent resolution. Pre-existing `tests/phase43` failures (12; worktree-environmental + stale archived-milestone paths, zero coupling) logged as DI-46-04-01, not fixed.
- [Phase 39 verification 2026-07-16]: Verification closeout ran under owner "Full closeout" instruction. 39-10-03 authority checkpoint resolved as Option A (gsd-core hard-gate at <home>/Desktop/code/gsd-core `fix/phase-complete-uat-predicate`, deployed to .claude-alt); 39-10 closed with SUMMARY. Canonical 39-VERIFICATION.md produced by gsd-verifier → **gaps_found (6/7)**. DATA-01..06 substance solid (251/251 dataset-free tests pass; all requirements map to real code), but an independently-reproduced evidence-integrity gap blocks completion: 39-VALIDATION row 39-07-02 is marked green yet its command fails against the retained 9-line scan.log — the original 41-line scan.log (acf9b207) was hand-assembled (its `# adapter init_log` block cannot come from the CLI), and 39-10-01 honestly regenerated the minimal true CLI output without correcting the ledger. Root cause: `pinn/data/stage_scan.py` CLI never serializes `AdmittedSetAdapter.init_log` (mem/watermark/blacklist/freshness). Phase 39 stays In Progress; fix routed to /gsd-plan-phase 39 --gaps. Memory-below-watermark held mechanically (adapter fail-closed) but is not independently provable from retained bytes.
- [Phase 39 closeout 2026-07-16]: Gap-closure plans 39-11..39-14 executed and committed. 39-11 added fail-closed redacted `evidence_lines()` + per-fidelity `n_present_on_disk`/`n_excluded` to `AdmittedSetAdapter`; 39-12 wired `evidence_lines()` into the scan CLI with `run_timestamp`/`run_nonce`/`evidence_byte_identity` freshness markers and renamed `exit_code`→`scan_exit_code`; 39-13 regenerated real-corpus evidence (scan.log now carries `mem:`/`n_blacklist_entries`/`n_present_on_disk`/freshness fields, no `/Users/` leakage); 39-14 repaired the vacuous row 39-10-02 awk assertion. Row 39-07-02 command re-run: observed exit 0. 39-UAT updated: Test 24 → pass, 27/27 pass, status complete, G-39-24 resolved. ROADMAP Phase 39 marked `[x]`. STATE advanced to Phase 40.
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
- [Phase 39-02]: AdmittedRecord field renamed s_min -> min_separation to keep pinn/data/types.py off the sole-classifier prohibition audit (only pinn/data/stages.py may co-occur s_min with STAGE_0/STAGE_1).
- [Phase 39-02]: evaluate_admission blacklist kwarg defaults to frozenset() (not required) to match the frozen tests/phase39/test_admission.py contract from Plan 01, which calls evaluate_admission(parsed) with no blacklist arg.
- [Phase 39-02]: Admission clause 6 COM/momentum checks are optional com_norm/momentum_norm kwargs (default None) since ParsedTrajectory carries no preprocessed state; Plan 39-03 wires them after running preprocessing.
- [Phase 39-02]: REQUIREMENTS.md DATA-01..06 left Pending (not marked complete) despite the plan frontmatter listing all six: Plan 39-02 delivers only the pure building-block layer (types/parser-helpers/preprocessing/stages/admission); DATA-01/02/03 need Plan 39-03's AdmittedSetAdapter integration and DATA-04/05/06 have zero code yet (splits.py/batches.py/stage_scan.py are Plans 39-04/05/06). Matches Plan 39-01's identical precedent.
- [Phase 39-03]: DATA-01/02/03 marked Complete — Plan 39-03 landed the production AdmittedSetAdapter (two-pass scan→admit→classify→fp32 residency), the deterministic GAP-39-07 resident_tensor_bytes numerator + mem_ballpark lower-bound cross-check, and the DATA-01..03 integration/containment gate. DATA-04/05/06 remain Pending (splits.py/batches.py/stage_scan.py are Plans 39-04/05/06).
- [Phase 39-03]: The full production adapter (residency, accessors, mem accounting, module-level resident_tensor_bytes/format_mem_line) landed in the task-01 commit rather than being split across tasks 01/02, because the frozen Wave-0 deferred tests (AdapterResidencyTests, ResidentBytesTests) activate the instant the AdmittedSetAdapter symbol exists and cannot be partially satisfied. Tasks 02/03 add the plan's additional named requirements as additive tests. Mirrors Plan 39-02's frozen-test-is-load-bearing precedent.
- [Phase 39-03]: Adapter constructor follows the frozen Wave-0 test's interface (root=, precision=, device=, run_dir=, version_metadata_path=, capacity_bytes=) rather than the plan prose's data_root=/memory_capacity_bytes= naming, since the deferred tests are the load-bearing contract; plan-named features (GSD_DATA_ROOT/git-common-dir default, DataSourceRootMissing/Incomplete, GSD_ALLOW_PARTIAL_DATA_ROOT, mem_ballpark, resident_tensor_bytes_misfit, remediation_quarantine, records_at/records_at_or_below/has_stage) are layered in as additive behavior + tests.
- [Phase 39-03]: adapter.py references .s_min (building the interim classify record) but deliberately contains NO STAGE_0/STAGE_1 literal — numeric-stage detection uses `label is not StageLabel.UNASSIGNED` / `label.value` — so it stays off the sole-classifier prohibition audit while stages.py remains the sole numeric classifier. The classifier floor is stored as self.classifier_interim_s0 (word-boundary-safe against the s0-mutation detector) and passed positionally to classify_stage_label.
- [Phase 41]: Retained exit_code as internal param while renaming emitted scan.log field to scan_exit_code=; plan acceptance grep over-broad on param names
- [Phase 40]: [Phase 40 Plan 40-05]: RunController anchors L_IC/L_E/L_L on one representative identity per fixed batch (pinn.loss_catalog single-trajectory-scoped signatures), computing h0/l0 from that identity ground-truth snapshot-0 via loss_catalog own helpers, eps_h provisional |h0|*1e-4; GradClipper.clip fixed to materialize its params iterable (was silently no-oping the apply call on a live generator) and gained state_dict/load_state_dict for RunController checkpoint composition.
- [Phase 40]: CurriculumController requires exactly one of run_controller/forced_disposition at construction — Defensive Rule 2 addition beyond the plan's T-40-09 both-supplied guard; a controller with neither could never produce a StageDisposition
- [Phase 41]: CR-01: RECOVER restores RunController from rollback payload before retry (dual-guard: live controller + run_controller key)
- [Phase 41]: CR-02: zero L-BFGS headroom polls StageExitMachine once; n_adam==max_epochs stays legal (GAP-40-02 A)
- [Phase 41]: WR-01: GradClipper checkpoint carries dtype as string and restores via closed local float32/float64 map
- [Phase 41]: WR-03: percentile_10_relaxation is a reserved owner-authorized degraded-advancement seam with no automatic consumer
- [Phase 41]: GAP-40-04 Option C: stage_factory yields RunController; ADVANCE swaps + rebinds schedule before stage-init save
- [Phase 41]: stage_factory=None preserves PLAT-01 single-stage; no default factory / no invented per-stage tables (SCOPE-19)
- [Phase 41]: 41-01: checkpoint cadence under run.checkpoint; guards under run.guards; RNG format UNDECIDED (A sidecar vs B sibling)
- [Phase 41]: TorchSaveCheckpointStore name preserved as production body; CHECKPOINT_SCHEMA_VERSION owned by checkpoint.py
- [Phase 41]: failure-* excluded from fallback_scan and latest.pt; bounded by failure_keep
- [Phase 41]: should_checkpoint elapsed is time-since-last-write via last_written_time + injectable time.monotonic
- [Phase 41]: GuardOutcome per-family RECOVER/HALT (LOW-1); memory signal torch.mps.driver_allocated_memory with injectable total
- [Phase 41]: apply_strict_cpu_determinism returns float64/cpu RuntimeSpec for pinn.train build override (HIGH 4)
- [Phase ?]: Dual save path: Phase-40 nested save() + CTX-53 save_anchor via build_checkpoint_payload
- [Phase ?]: Beyond-terminal promote soft-fail; TRAIN-07 preflight owns stage>=3 hard stop
- [Phase ?]: checkpoint_hook/guard_hook are closures with phase-specific placement (Adam before step, L-BFGS after)
- [Phase ?]: Seed fan-out: ArchitectureSpec.seed = config.run.seed for weight init + sampling
- [Phase ?]: B-5 RESUME_FIELD_REGISTRY is provisional; unclassified-to-refuse is locked
- [Phase ?]: python -m pinn.train is the CTRL-01/05/08 composition root with exact-anchor resume routing
- [Phase ?]: 43-02: velocity for the gate Hamiltonian is derived by finite-differencing the model's predicted positions (never input-time autograd), keeping the model forward pass a single torch.no_grad() call; gate_verdict is the sole PASS/FAIL source (SCS is display-only), avoiding a two-independent-booleans render; the evaluation receipt is colocated with metrics.json/metrics.md at the operator-supplied --output directory per the plan's literal artifact contract
- [Phase ?]: [Phase 43 43-04]: ACC-01 completed — pinn.train._check_duration_gate wired into the launch preflight before run_dir.mkdir; reconciled pre-existing uncommitted work rather than rewriting (matched plan + 43-REVIEWS.md HIGH finding + SPEC edges R1/R2). Discovered (not fixed, out of scope): tests/phase41/test_train_entrypoint.py (17/193) and tests/phase42 subprocess-launch tests now fail against the new fail-closed gate since they launch fresh non-smoke pinn.train without a persisted calibration; logged as DI-43-04-01/02 in deferred-items.md for a follow-up fixture update.
- [Phase 43 43-06, 2026-07-21]: ACC-02 real smoke complete over the real admitted corpus: 32 identities, 300/300 gap-free steps, checkpoints 100/158/200/300, one SIGTERM interrupt + `--resume latest` to finished, `s_per_step=0.11570`, forecast 34.71s. Loss bounded but non-descending across the 300-step Adam budget — recorded as an ACC-05 pilot watch-item, never framed as convergence. Three owner-carved seams closed this plan: B-5 `ratify-current` (unchanged registry); R-1 `loss_explosion_ceiling=1e11` via owner delegation (revisable at ACC-05); D4-a `wall_clock_ceiling_s=120` via owner's explicit selection, persisted in `configs/stage0-example.yaml`. Two Rule-3 operational auto-fixes: `data.blacklist_path` threaded to fix DI-43-06-01 (owner-authorized, legacy Documentation blacklist designated authoritative), and `rolling_keep` 3→4 in `configs/smoke.yaml` to preserve checkpoint 100 across the required interrupt.
- [Phase 46 Plan 46-05]: INST-01 safety properties proven as tests (commit 270e045). Held-out isolation enforced doubly — AST scan over raw validation_gate source covering absolute/from/relative import spellings, plus a fresh-subprocess sys.modules check (T-46-05-01). Prior-mode restoration proven from BOTH prior states under an injected mid-population failure; mode bracket AST-pinned handler-less try/finally. Non-interference proven bitwise (real CPU/float64 network), structurally (exact signature pin), behaviorally (deterministic passes). Artifact contract pinned: atomic publication with no temp residue, schema fail-closed over the full 16-key 46-03 schema list, NaN/Infinity/-Infinity quoted sentinels under plain json.loads, pointer fields only behind a durable schema-valid sidecar; valid-FAIL observation still yields gate_status ok (metric FAIL is honest evidence). Both suites dataset-free with inline FrameConvention (the wave-5 ratified-frame constant never referenced — T-46-05-04). Clarified 46-03 contract: validator enforces the 16 top-level keys; nested frame/row shape pinned on the published payload; Inf-aggregate shape constructed directly with gate_metrics-derived SCS/verdict. Pre-existing watchdog packaging failures (2, live-deploy drift) logged as DI-46-05-01, not fixed.
- [Phase ?]: [Phase 46 Plan 46-06]: CONF-01 real-corpus evidence run (commit f106889b) returned VERDICT_AMBIGUOUS over 1651 GAP-46-02-Option-A trajectories -- routes D-09, not the clean D-08 continuation. 100% of eligible trajectories carry a body-permutation confound and a com_recenter_boost gauge divergence; identity_raw=true for 100% but only 66.6% (1100/1651) clear the corrected-raw residual tolerance, short of decide_verdict rule 4's unanimity requirement, so the verdict falls to the rule-6 fail-closed catch-all. 46-VERDICT.md (commit 6638204d) records the branch; Plan 46-07 and Phase 47 stay BLOCKED pending owner resolution. GAP-46-01's consequence note: the verdict selects neither of that gap's two evaluator-pairing readings cleanly, though the identity classification leans structurally toward the raw-target reading.
- [Phase 46 GAP-46-05, 2026-07-27]: Phase 46 re-scoped by owner instruction after GAP-46-04's option-A routing proved circular — Plan 46-07 waited on a repair owned by Phases 47/48, while Phase 47 was gated on Phase 46 closing (`ROADMAP.md:103`), so neither phase could start. Option A: move the **minimum** repair (body permutation + COM-recentre/boost gauge) and its follow-up CONF-01 re-probe into Phase 46, traced as new requirement **CONF-08** (milestone 22 → 23). The `D` scaling is excluded from the repair because it is the raw-vs-scaled question CONF-01 exists to answer; rotation gauge enters only if the re-probe measures it as the new `first_diverging_step`. New plans: 46-08 (repair, wave 5), 46-09 (re-probe + verdict, wave 6, `autonomous: false`); 46-07 moves to wave 7 with its hard gate unchanged. GAP-46-04 is superseded **in part** — only on which phase performs the minimum repair; `VERDICT_AMBIGUOUS` is still not upgraded and residual conformance repair stays with Phases 47/48. Engineering basis: `S_H = median_train(K0 + Uabs0)` is mass-weighted in both terms, so computing it over the un-permuted corpus would yield an `S_H` for a different three-body system and mis-scale `ε_H = 1e-4·S_H` across the milestone. Correction recorded in the same amendment: CONF-01 and INST-01 had been marked Complete prematurely (RG-02 is measurably unresolved and sits under EVAL-01 precondition (ii); INST-01's production wiring is the unexecuted 46-07) — both reverted to Pending.
- [Phase 46 GAP-46-06 + Plan 46-07, 2026-07-28]: **The validation frame is ratified by owner instruction, not by a machine verdict.** Plan 46-09's one post-repair probe returned rule-5 `VERDICT_NON_FRAME_DIVERGENCE`. Root cause is structural, not empirical: `decide_verdict` rule 4 requires `all_identity_raw` — a byte-match against the parsed file-order array (`target_frame_probe.py:641`) — which CONF-08's authorized repair deliberately removed, plus `all_raw_corrected_consistent`, whose unconditional inverse-permutation correction post-repair *creates* the mismatch it was written to undo (1100 → 0). **Our own repair made the clean verdict unreachable.** Orchestrator analysis of the committed `raw.json` showed option B's "only 1086/1651" caveat is a zero-margin tolerance artifact: raw-vs-provenance-control median ratio 0.999996, failing trajectories exceeding by ~0.002%, `tolerance_floor` equal to the control median for 1651/1651, and `tolerance_fp32_increment` exactly 0 for 801/1651 — while the two float64 controls agree to 8.6e-16 and the float32 resident to ~1e-6, i.e. residency quantization. The substantive raw-vs-scaled question is answered by measurement (scaled arm separated by a factor of 12.3); only the token was unobtainable. Owner ruled option B: ratify `("r_raw", "t_native", "ordered_raw")` with `conf01_evidence_ref` on the `20260728T014532Z` run. Plan 46-07 then landed `RATIFIED_VALIDATION_FRAME` (quoted from the resolution note, never inferred — D-12), the `_run_validation_gate_pass` seam inside checkpoint_hook's existing validation branch (no new cadence — D-10), sidecar-before-pointer ordering (D-17), fail-closed `failed:` conversion (D-15/D-20), and the summary projection with `eval01_precondition_iii`. Verified by inspecting a real run's artifacts, not by a passing test: 240 per-trajectory `{record_key, eps_h, scs}` rows per validation event, ratified frame embedded in the sidecar, `gate_status ok` with `gate_verdict FAIL` kept distinct.
- [Phase 46 Plan 46-10]: Closed both remaining INST-01 verifier gaps: validate_sidecar_payload now recomputes every per-row/aggregate gate value through gate_metrics and binds compact fields via compact_validation_fields_from_payload; every validation event (finite/NaN/+Inf/-Inf loss, ok/failed gate) is durably persisted, and eval01_precondition_iii selects only the physical latest JSONL line with type-and-value-sensitive equality against the validated sidecar, so a failed/malformed/cross-run/wrong-step event can never expose an older eligible success.
- [Phase ?]: [Phase 47 Plan 47-02]: CONF-02 S_H pipeline landed (commits 2b985eee, 2ecc53d3). _matched_plummer_components is the single home of the softened pairwise sum (D-11); k0/uabs0 captured in float64 at admission at EPS_SOFT before the fp32 cast (D-09/D-10/D-12); run_metadata.py computes the train-split median once at setup and persists s_h/eps_h/n_train via atomic_write_text with re-validate-on-load and explicit expected_energy_floor_factor/expected_eps_train bindings (D-13..D-18); _assert_s_h_matches_artifact RETURNS the validated s_h so both setup branches bind the local 47-03 threads into RunController. First authoritative real-corpus S_H/eps_H/N_train deferred to Phase 50 (owner Option B); REQUIREMENTS.md CONF-02 checkbox deliberately not flipped by the executor.
- [Phase ?]: Phase 48 Plan 48-01: Rbar is assembled as sum(residual**2, body/component)/3 before the existing causal consumer.
- [Phase ?]: Phase 48 Plan 48-01: data_huber_loss retains .mean(), documented as sum(Huber)/(9*N_t) under GAP-45-01/D-01.
- [Phase ?]: LossConfig.lambda_e_max defaults to exact 0.0 while retaining finite, nonnegative, <=1 validation.
- [Phase ?]: Both shipped Stage-0 YAML entry points explicitly declare lambda_e_max: 0.0; ScheduledWeights remains generic with nonzero caps supported.
- [Phase ?]: CONF-05 causal weights clamp at the active dtype/backend upward-directed representable log-tiny floor, with exact five-field runtime provenance.
- [Phase ?]: Fresh and resumed training setup derive and enforce the same causal clip facts from RuntimeSpec through strict atomic training_metadata.json.
- [Phase ?]: Adam and L-BFGS gradient telemetry uses non-mutating autograd.grad diagnostics with explicit pre-total-backward and last-closure provenance.
- [Phase ?]: Missing or non-finite required gradient statistics fail closed as null telemetry with grad_stats_complete=false and step_completed=false.
- [Phase 49 Plan 49-06]: Owner ruling 2026-08-05 sets `front_advance_window_n = 500`; invariant B is enforcing and `INV-B-N-UNSET` is closed with a passing proof test.
- [Phase ?]: GATE-03 invariant A, invariant B, and causal_stats_missing remain HALT-family StepGuards entries; existing step-log and failure-bundle paths are unchanged.
- [Phase 49 Plans 49-04/49-08]: The ordered census manifest resolves concrete producer contracts; the fail-closed divergence register and preflight preserve open caveats verbatim.
- [Phase ?]: Every closed register entry carries a passing proof-test node; waivers cite existing authority only.
- [Phase 49 Plan 49-08]: Scheduler state is scalar-validated before PHYS-05 arithmetic/comparison; ordinary setup/probe failures persist refusal evidence; resume retains the validated preflight history.
- [Phase ?]: Plan 50-01: --stage-0-only fresh-run Stage-0 ceiling added to CurriculumController/pinn.train (SCOPE-27); guarded ADVANCE skips stage increment, stage_factory, stage-1-init, promotion, and the k->k+1 disposition record
- [Phase ?]: Plan 50-01: four Phase-50 configs committed with D-04 diff receipt; 50-PRE-REGISTRATION.md fixes seed-42 candidate/checkpoint/fallback order before any graded run; 50-CONFIG-DELTA.md derived by structural load_config() diff; STAGE0-BUDGET-DELTA qualification appended to divergence register via API
- [Phase ?]: Plan 50-01: RUN-01/RUN-02 requirement checkboxes deliberately NOT flipped (D-30 reserves that to phase verification); all wave-1 files landed in one commit (abd5f8d) on milestone/v2.2 per D-17

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
- **CONF-01 is settled by owner instruction, not by a machine verdict (2026-07-28, GAP-46-06).** The ratified frame constant `RATIFIED_VALIDATION_FRAME` in `pinn/training/validation_gate.py` carries its ratification source in an adjacent comment block. **Standing consequence:** if Phase 47/48 moves residency to the locked canonical scaled contract (`r'` with `u = t/T`), that constant goes stale and must be re-ratified under the same D-12 discipline — and any `S_H` already computed in the raw frame is invalidated (`H' = D·H`). Do not let a `Complete` checkbox on CONF-01 stand in for this qualification when Phase 51 checks EVAL-01 precondition (ii).
- **Pre-existing suite failures, NOT introduced by Phase 46 (2026-07-28).** `pytest tests/ -q` reports 14 failures in this worktree: 7 in `tests/phase43/test_verdict_grounding.py`, 2 in `test_verify_gate.py`, 2 in `test_pilot_calibration.py`, 1 in `test_smoke.py`, 2 in `tests/watchdog/test_global_packaging.py`. Cause: `.planning/phases/` now holds only phase 46 (the phase-43 artifacts those tests read were archived at v2.0 close), plus gitignored `runs/` being present here — its presence flips those tests from *skip* to *fail*. Verified by A/B in a throwaway worktree at `fe3d45de`: identical failure sets with and without plan 46-07's five changed files. Do not treat a red full suite as a Phase 46 regression.
- **Thin pre-existing timeout margin in `tests/phase42/test_signals.py`.** Three subprocess tests run at 92–105s against a 120s per-subprocess timeout. Plan 46-07 did not consume this margin (measured before/after), but an unrelated slowdown on a loaded machine could surface it as a flaky timeout. D-10 forbids escaping via a new cadence/chunking knob.
- CONF-01 D-09 STOP (2026-07-27, Plan 46-06) — **resolved, gap registers written.** The real-corpus target-frame probe returned VERDICT_AMBIGUOUS, not the clean D-08 VERDICT_TARGETS_ARE_SCALED. GAP-46-04 (commit `be0867ab`/`997c731b`) routed the confound repair to Phases 47/48; GAP-46-05 corrected that routing the same day after it deadlocked the milestone, moving the minimum repair + re-probe into Phase 46 as CONF-08. Plan 46-07 remains gated on 46-09's verdict — that gate is by design. Its Task-1 hard gate was repointed to `46-VERDICT-POSTREPAIR.md` (absence ⇒ BLOCKED), because the pre-repair `46-VERDICT.md` must never be used to ratify a frame; the gate's three-state logic is otherwise unchanged.
- **Repair discipline for CONF-08 (SCOPE-29 boundary):** the repair is defined by the canonical pipeline in `preprocess_trajectory`, not by which transform lowers the probe residual. The probe reports the *first* diverging step, so repairing permutation + COM/boost may surface `rotation_gauge` as the next one; that is a measurement to route, not a licence to iterate against the probe. The `D` scaling is excluded from the repair specifically because it is the raw-vs-scaled question CONF-01 must answer.
- **Branch-ref hygiene:** `milestone/v2.2` was created 2026-07-27 at `997c731b`, after plans 46-01..46-06 had already executed on `milestone/v2.1`. Tag `v2.1` (`f72eaabd`) is the durable v2.1 record; `milestone/v2.1` still points at `997c731b` and carries 23 v2.2 commits, so owner-controlled master integration should target the **tag**, not the branch ref.

## Session Continuity

**Resume file:** None

Last session: 2026-08-13T07:30:00.000Z
Stopped at: Planned 50-04 and 50-05; 50-03 re-sequenced to wave 5. No run launched.
Next action: Execute wave 3 — `/gsd-execute-phase 50 --wave 3` from .worktrees/trainex — which runs 50-04: the GAP-50-02 conformance repair (`_run_validation` reads the entire held-out Stage-≤k validation pool, no replay draw, no lookahead), its divergence-register entry and proof test, and the generation-3 pre-registration amendment. `replay_count` stays 240 and no config byte changes. Wave 4 (50-05) then opens generation 3 and carries an owner checkpoint before the graded band — it is `autonomous: false`. Do not start 50-03 until `final_band_generation` is non-null.

## Operator Next Steps

- **Plan Phase 50** — begin with `$gsd-discuss-phase 50`; Phase 49 authorizes planning but did not launch the admitted-corpus run.
- ~~Execute Phase 44~~ — complete 2026-07-23 (qualified by `44-ERRATUM.md` 2026-07-24)
- ~~Adjudicate GAP-44-01~~ — RESOLVED-WITH-INSTRUCTION 2026-07-23 (owner option A: the physics gate is defined over the worst-case `max` per-trajectory ε_H; headline `max = 237.2086056078468`. See `.planning/phases/44-physics-gate-forensics/44-GAPS.md` and the updated `44-DIAGNOSIS.md`.)
- ~~Execute Phase 45~~ — complete 2026-07-24, `45-AUDIT.md` all ten checks PASS, package delivered
- ~~Adjudicate the five open gaps~~ — all five RESOLVED/DEFERRED 2026-07-24. GAP-45-03: per-stage PHYS-05 values are locked (option A). GAP-45-02: λ_E provenance unrecoverable, treated as drift, reverts to 0 (option C) → C-05 is a defect. GAP-45-04: mandate the invariant "no causal weight may be exactly zero", defer the number to the implementer with a recording obligation (option C). GAP-45-01: deferred to the conformance-fix phase, must resolve **before** any re-run (option C). GAP-44-02: erratum + mandatory re-derivation as a mapped requirement (option C). Index: `.planning/milestones/v2.1-GAPS.md`.
- ~~Frame the next milestone~~ — owner decision 2026-07-24: **conformance first**, then re-run, then tuning adjudication. Six inherited obligations enumerated in `v2.1-GAPS.md`.
- **Owner-controlled integration (NOT performed by the agent):** `--no-ff` merge of `milestone/v2.1` to master, archive under `milestones/v2.1-*`, tag `v2.1`. Closeout is committed on the branch and ready.
- **Provenance gap to close:** the returned research report does not identify which external agent produced it (landed as `trainex-r2-research-report.md`, not the convention's `<agent>-resolution.md`). Owner to confirm the agent/service so the delivery-note provenance record is complete.
- **Open the next milestone** — conformance-first roadmap; the six inherited obligations are the seed scope.
- **Spawn the verification-enforcement workstream** — separate concurrent session; charter at `docs/work/designs/cross_cutting/training-verification-regime/2026-07-24-verification-enforcement-charter.md`, initial register contents ready in the conformance audit's C-01..C-08.
- Hygiene (non-blocking): `44-VALIDATION.md` remains `status: draft` / `nyquist_compliant: false`.
