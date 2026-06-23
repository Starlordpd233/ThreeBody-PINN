---
phase: 33-curriculum-stage-contracts
plan: 01
subsystem: planning
tags: [evidence, packet-first, curriculum, ledger-linkage]
requires:
  - .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md
  - .planning/phases/33-curriculum-stage-contracts/33-GAPS.md
  - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md
provides:
  - .planning/phases/33-curriculum-stage-contracts/33-BASELINE-CAPTURED
  - .planning/phases/33-curriculum-stage-contracts/evidence/README.md
  - .planning/phases/33-curriculum-stage-contracts/evidence/_TEMPLATE.md
  - .planning/phases/33-curriculum-stage-contracts/evidence/adaptive-stage-assignment.md
  - .planning/phases/33-curriculum-stage-contracts/evidence/l-max-tau-l.md
  - .planning/phases/33-curriculum-stage-contracts/evidence/m7-tau-l-ic13-exclusion.md
  - .planning/phases/33-curriculum-stage-contracts/evidence/d5-stage-transitions.md
  - .planning/phases/33-curriculum-stage-contracts/evidence/m6-l-norm-metadata.md
affects:
  - .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md
tech-stack:
  added: []
  patterns:
    - Phase 32 evidence-packet schema mirrored into Phase 33 with no new verdict enum, status lifecycle, package dependency, schema push, or UI artifact
    - Dynamic dirty-doc SHA-256 baseline capture (no hardcoded filename)
    - Post-task ledger freshness hash for Plan 33-04 concurrency check
key-files:
  created:
    - .planning/phases/33-curriculum-stage-contracts/33-BASELINE-CAPTURED
    - .planning/phases/33-curriculum-stage-contracts/evidence/README.md
    - .planning/phases/33-curriculum-stage-contracts/evidence/_TEMPLATE.md
    - .planning/phases/33-curriculum-stage-contracts/evidence/adaptive-stage-assignment.md
    - .planning/phases/33-curriculum-stage-contracts/evidence/l-max-tau-l.md
    - .planning/phases/33-curriculum-stage-contracts/evidence/m7-tau-l-ic13-exclusion.md
    - .planning/phases/33-curriculum-stage-contracts/evidence/d5-stage-transitions.md
    - .planning/phases/33-curriculum-stage-contracts/evidence/m6-l-norm-metadata.md
  modified:
    - .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md
decisions:
  - GAP-33-01 packet-first / defer-floor disposition carried into AC-CURR-01 packet
  - GAP-33-02 keep-Rosenstein-baseline / defer-estimator disposition carried into AC-CURR-02-LMAX and AC-CURR-02-M7 packets
  - GAP-33-03 raw-only / defer-clip disposition carried into AC-CURR-04 packet
  - D5 three-state ADVANCE/RECOVER/HALT-REVIEW contract grounded in resolution doc §1.11 / 33-SPEC R3 / 33-CONTEXT D-33-08
  - Phase 32 ledger AC ID convention reconciled (AC-CURR-02 -> AC-CURR-02-LMAX, AC-CURR-04-M6 -> AC-CURR-04)
metrics:
  duration: ~25 minutes
  completed: 2026-06-23
  tasks_completed: 3
  files_touched: 9
status: complete
---

# Phase 33 Plan 01: Evidence Baseline and Packet/Ledger Linkage Summary

Created the Phase 33 evidence baseline, the Phase 33 packet workspace, all five
Phase 33-owned evidence packets, and the synchronized Phase 32 ledger linkage
required before any curriculum-stage framework-spec edit. No framework spec,
frozen/read-only report, live `pinn/` code, generated data, package manifest, or
UI artifact was modified.

## What Was Built

- **`33-BASELINE-CAPTURED`** sentinel: records the `milestone/v1.6` branch, the
  resolution-doc SHA-256 (`4c5195b8...`), the empty `pinn/` working-tree
  snapshot, the dynamic per-file dirty-doc SHA-256 set (captured at baseline,
  not hardcoded), the combined `dirty_docs_sha256`, and the post-Task-3
  `ledger_post_33_01_sha256` freshness reference for Plan 33-04 Task 2.
- **`evidence/README.md`** + **`evidence/_TEMPLATE.md`**: Phase 33 packet
  protocol and template mirroring Phase 32 with Phase 33 paths. No new verdict
  enum, status lifecycle, package dependency, schema push, or UI artifact.
- **Five Phase 33-owned packets**:
  - `adaptive-stage-assignment.md` (CURR-01; D-33-01..03; AC-CURR-01; GAP-33-01)
  - `l-max-tau-l.md` (CURR-02; D-33-04/05/07; AC-CURR-02-LMAX; GAP-33-02)
  - `m7-tau-l-ic13-exclusion.md` (CURR-02; D-33-06; AC-CURR-02-M7; §1.7 accepted)
  - `d5-stage-transitions.md` (CURR-03; D-33-08/09; AC-CURR-03; §1.11 + R3 + D-33-08)
  - `m6-l-norm-metadata.md` (CURR-04; D-33-10/11/12; AC-CURR-04; GAP-33-03)
- **`32-ISSUE-LEDGER.md`**: all five Phase 33-owned rows now link to their
  packet paths, carry the reconciled AC IDs, and have `accept-resolution`
  verdicts with `IN_PROGRESS` status. Per-row transition logs document the
  rename `AC-CURR-02 -> AC-CURR-02-LMAX` and `AC-CURR-04-M6 -> AC-CURR-04` and
  cite the resolved gap and the resolution-doc section.

## Packet-First Constraint Compliance

All five packets preserve the owner-pending constraints from the resolved
Phase 33 gaps and from the v1.6 spec:

- **Population safeguard (CURR-01):** packet states explicitly that the
  5% / `>10%` / adaptive value is owner-pending the FUT admitted-set EDA
  (SCOPE-15) per `GAP-33-01`; the roadmap / `CURR-01` `>10%` phrasing is
  superseded and is not transcribed as a locked floor.
- **tau_L estimator (CURR-02):** packet retains the Rosenstein-style estimator
  as the revisable baseline and routes the final estimator / time-unit
  convention / fit parameters / uncertainty handling / thresholds to the owner
  per `GAP-33-02`; the issue-doc shadow-trajectory method, its `epsilon_pert`
  / `epsilon_soft` shadow parameters, and the unspecified PCA+Rosenstein
  shortcut are NOT normatively adopted (TAUL-02, TAUL-05 rejected). Active
  scale stays raw-mass `D ~= 4.6416` (Phase 32 D packet; SCOPE-12).
- **tau_L exclusion (M7):** packet records `tau_L` as staging/evaluation
  metadata excluded from `IC13` by design (§1.7 `accepted`).
- **Stage transitions (CURR-03):** packet locks the ADVANCE / RECOVER /
  HALT-REVIEW state machine grounded in §1.11 / R3 / D-33-08 and keeps all
  numeric thresholds, epoch tables, stagnation windows, retry limits, and
  percentile relaxations provisional pending FUT Stage-0 pilot calibration
  (D-33-09; SCOPE-14).
- **L_norm metadata (CURR-04):** packet locks raw un-clipped `L_norm` storage
  + the mandatory nonfinite / near-degenerate `L_max` diagnostic guard and
  states that no global clamp is authorized; the `np.clip(L_norm, 0, 1)`
  stage-gate is owner-pending admitted-set evidence per `GAP-33-03`.

## Deviations from Plan

None - plan executed exactly as written. The Task 2 verify check required
literal `D-33-01` through `D-33-07` decision IDs in the packet text; I added
explicit "Phase 33 Decisions Covered" header rows and cited the decision IDs
inline in the "Locked Convention or Owner Route" sections. This is a citation
completeness adjustment, not a plan deviation. The M7 transition-log section
was missing from the original Phase 32 ledger (only the row existed); I added
the `### M7` transition-log section to host the Phase 33 entry, which is the
synchronization the plan's Task 3 action requires.

## Self-Check: PASSED

Created files (all FOUND):

- `.planning/phases/33-curriculum-stage-contracts/33-BASELINE-CAPTURED`
- `.planning/phases/33-curriculum-stage-contracts/evidence/README.md`
- `.planning/phases/33-curriculum-stage-contracts/evidence/_TEMPLATE.md`
- `.planning/phases/33-curriculum-stage-contracts/evidence/adaptive-stage-assignment.md`
- `.planning/phases/33-curriculum-stage-contracts/evidence/l-max-tau-l.md`
- `.planning/phases/33-curriculum-stage-contracts/evidence/m7-tau-l-ic13-exclusion.md`
- `.planning/phases/33-curriculum-stage-contracts/evidence/d5-stage-transitions.md`
- `.planning/phases/33-curriculum-stage-contracts/evidence/m6-l-norm-metadata.md`

Modified files (FOUND): `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md`.

All plan-level `<automated>` verify checks pass:

- Task 1 checks 1-4 (file existence, baseline tokens, dynamic dirty-doc hash, template tokens): PASS
- Task 2 checks 1-3 (packet tokens, Stage-2/Stage-5/owner-pending, gap+AC citations): PASS
- Task 3 checks 1-6 (D5/M6 tokens, D5 grounding qualification, ledger paths+AC IDs, ledger hash matches baseline, dirty-doc preservation, closed-set changed files): PASS

Commits:

- `0113f86` plan(33): capture phase 33 baseline and evidence workspace
- `699b849` plan(33): author curr-01 and curr-02 evidence packets
- `f2c8a9b` plan(33): author curr-03/curr-04 packets and link phase 32 ledger (this commit)

No framework spec, frozen/read-only report, live `pinn/` code, generated data,
package manifest, or UI artifact was modified by Plan 33-01. The dirty-doc set
captured at baseline (`.planning/STATE.md`, the cross-cutting review-resilience
plan) is preserved unchanged. The packet-before-edit prerequisite is now
complete; Plans 33-02 and 33-03 may transcribe the curriculum-stage contracts
into `ctl_instruction.md`, and Plan 33-04 will verify the linkage, dirty-doc
preservation, and protected-path guard.
