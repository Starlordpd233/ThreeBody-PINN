---
phase: 35-loss-energy-weight-contracts
plan: "35-02"
subsystem: pinn-framework-spec
status: complete
tags:
  - v1.6
  - loss
  - architecture-spec
  - energy-weighting
dependency_graph:
  requires:
    - Phase 35 plan 35-01 loss evidence packets
    - Phase 32 D-04 owner-ratified GAP-32-01 Option A
    - Phase 35 context/research/validation contract
  provides:
    - Phase 35 verdict-status callouts in pinn_architecture.md
    - Component-math source-precedence guard for loss-energy weighting
    - Traceability tags for AC-LOSS-01 through AC-LOSS-04
  affects:
    - Phase 35 plans 35-03 and 35-04
    - Phase 36 structural verification
tech_stack:
  added: []
  patterns:
    - Grounded Phase 35 verdict callouts inside the framework spec
    - Deferred/rejected issue-doc proposals marked inline with acceptance IDs
key_files:
  created:
    - .planning/phases/35-loss-energy-weight-contracts/35-02-SUMMARY.md
  modified:
    - pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
    - .planning/STATE.md
    - .planning/ROADMAP.md
key_decisions:
  - No new semantic/spec decision was invented; all verdict text follows Phase 35 evidence packets, the resolution doc, or owner-ratified D-04 Option A.
  - Component formulas remain in pinn_architecture.md while total-loss assembly remains in ctl_instruction.md.
requirements_completed:
  - LOSS-01
  - LOSS-02
  - LOSS-03
  - LOSS-04
coverage:
  - id: D1
    description: Phase 35 loss-scaling, componentwise-AD, energy-delta, energy-weight, and causal-mode callouts were added to pinn_architecture.md.
    verification:
      - kind: other
        ref: "python3 token/anchor checks from 35-02-PLAN.md"
        status: pass
      - kind: other
        ref: "python3 ctl anchor check from 35-02-PLAN.md"
        status: pass
    human_judgment: false
  - id: D2
    description: Source-precedence guard rejects or defers stale issue-doc loss constructs without introducing forbidden numeric defaults.
    verification:
      - kind: other
        ref: "python3 negative regex check from 35-02-PLAN.md"
        status: pass
      - kind: other
        ref: "git diff --check -- pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md"
        status: pass
    human_judgment: false
metrics:
  started_at: 2026-06-29T02:49:55Z
  completed_at: 2026-06-29T03:02:03Z
  duration_seconds: 728
  tasks_completed: 2
  files_created: 1
  files_modified: 1
---

# Phase 35 Plan 02: Loss Architecture Contract Summary

Phase 35 loss-energy verdicts are now embedded in `pinn_architecture.md` with acceptance tags, grounded evidence references, and explicit rejected/deferred guards for stale issue-doc proposals.

## Tasks Completed

| Task | Result | Commit |
|---|---|---|
| Task 1 - Add Phase 35 component-math callouts | Added grounded callouts for LOSS-01 through LOSS-04, NS-18, NS-12, M15, NS-13, and D-04; preserved PHYS-05 max weights, `delta_E = 1.0`, and D-04 Option A causal weighting. | `8c61eb16` |
| Task 2 - Guard source precedence and deferred values | Added a source-precedence guard that rejects/defer stale cap-table, dominance-reweighting, Huber-calibration, dense-ALM, and windowed-causal constructs while keeping CTL assembly as a pointer. | `583a010f` |

## Files Changed

Created:

- `.planning/phases/35-loss-energy-weight-contracts/35-02-SUMMARY.md`

Modified:

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
- `.planning/STATE.md`
- `.planning/ROADMAP.md`

## Decisions Made

- No new semantic/spec decision was made by the executor.
- D-04 text was grounded in the existing `RESOLVED-WITH-INSTRUCTION` owner-ratified Option A.
- NS-13 calibration remains deferred; this plan preserves `delta_E = 1.0` and does not choose a new Huber threshold.
- M15 cap-table/high-weight replacement remains rejected; this plan keeps PHYS-05 scheduled conservation weights at or below one.

## Verification

| Check | Result |
|---|---|
| Task 1 token check for AC-LOSS-01, AC-LOSS-01-AD, AC-LOSS-02, AC-LOSS-03, AC-LOSS-04, LOSS-01 through LOSS-04, NS-18, NS-12, M15, NS-13, D-04, and required formula tokens | PASS |
| Task 1 truncation/anchor check for `The Multi-Component Loss Function`, `Loss Balancing via Warmup Schedule (PHYS-05)`, and `Output Layer and Kinematic Consistency` | PASS |
| CTL anchor check for `Loss Function Formulation`, `Total Training Loss`, and `Data Flow During Training` | PASS |
| Task 2 forbidden/default negative regex check | PASS |
| Plan-level `git diff --check -- pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` | PASS |
| Stub scan for TODO/FIXME/placeholder/empty-data patterns in `pinn_architecture.md` | PASS - no matches |
| Commit existence check for `8c61eb16` and `583a010f` | PASS |
| Tracked deletion check after both task commits | PASS - no deletions |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking verification anchor] Restored the plan's stable multi-component loss anchor**
- **Found during:** Task 1 verification.
- **Issue:** The existing heading was `The Multi-Component, Physics-Constrained Loss Function`, but the plan's required anchor check expected `The Multi-Component Loss Function`.
- **Fix:** Renamed the heading to `The Multi-Component Loss Function (Physics-Constrained)`, preserving the qualifier while satisfying the stable anchor.
- **Files modified:** `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
- **Verification:** Task 1 truncation/anchor check passed.
- **Committed in:** `8c61eb16`

**Total deviations:** 1 auto-fixed blocking verification issue.
**Impact on plan:** Presentation-only anchor fix; no semantic/spec decision was added.

## Issues Encountered

- An initial patch application targeted the main checkout path instead of the active specwork checkout. The accidental main-checkout edit was reversed before any commit, the specwork absolute path was verified before re-applying, and `git diff -- pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` in the main checkout showed no remaining diff.
- `.planning/STATE.md` and `.planning/ROADMAP.md` were updated through GSD tracking commands after task commits. `.planning/REQUIREMENTS.md` was not touched because it was outside the owned write set; requirement completion is recorded in this summary frontmatter.

## Auth Gates

None.

## Known Stubs

None.

## Threat Flags

None. This plan edited framework-spec documentation only and introduced no network endpoint, authentication path, file-access path, schema change, or runtime trust-boundary surface.

## Self-Check: PASSED

- Found `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`.
- Found `.planning/phases/35-loss-energy-weight-contracts/35-02-SUMMARY.md`.
- Found updated `.planning/STATE.md` and `.planning/ROADMAP.md` tracking files.
- Found task commits `8c61eb16` and `583a010f` in git history.
- Verified no tracked deletions were introduced by either task commit.
