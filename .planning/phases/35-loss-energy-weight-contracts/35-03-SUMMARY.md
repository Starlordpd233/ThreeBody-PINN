---
phase: 35-loss-energy-weight-contracts
plan: "35-03"
subsystem: pinn-framework-spec
status: complete
tags:
  - v1.6
  - loss
  - ctl-instruction
  - total-loss-assembly
dependency_graph:
  requires:
    - Phase 35 plan 35-01 loss evidence packets
    - Phase 35 plan 35-02 component-math anchors in pinn_architecture.md
    - Phase 32 GAP-32-01 owner-ratified D-04 Option A
  provides:
    - Phase 35 total-loss assembly callouts in ctl_instruction.md
    - D-04 owner-ratified causal-mode transcription in ctl_instruction.md
    - Source-precedence guard for deferred and rejected loss constructs
  affects:
    - Phase 35 plan 35-04
    - Phase 36 structural verification
tech_stack:
  added: []
  patterns:
    - Verdict-status callouts in framework specs
    - Stable section-heading plus AC-ID cross-references
    - Single canonical home split: ctl assembly, pinn component math
key_files:
  created:
    - .planning/phases/35-loss-energy-weight-contracts/35-03-SUMMARY.md
  modified:
    - pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
key_decisions:
  - No new semantic/spec decision was invented; all text follows Phase 35 evidence packets, 35-SPEC.md, and owner-ratified GAP-32-01 Option A.
  - ctl_instruction.md owns total-loss methodology and assembly while pinn_architecture.md remains the component-math home.
requirements_completed:
  - LOSS-01
  - LOSS-02
  - LOSS-03
  - LOSS-04
coverage:
  - id: D1
    description: ctl_instruction.md now carries LOSS-01 through LOSS-03 total-loss assembly callouts and points to pinn_architecture.md for component math.
    verification:
      - kind: other
        ref: "python3 token and anchor checks from 35-03-PLAN.md Task 1"
        status: pass
      - kind: other
        ref: "python3 pinn_architecture.md AC-LOSS anchor check from 35-03-PLAN.md Task 1"
        status: pass
    human_judgment: false
  - id: D2
    description: ctl_instruction.md records D-04 as RESOLVED-WITH-INSTRUCTION Option A and removes owner-pending Phase 35 causal-mode wording.
    verification:
      - kind: other
        ref: "python3 D-04 owner-resolution check from 35-03-PLAN.md Task 2"
        status: pass
    human_judgment: false
  - id: D3
    description: ctl_instruction.md guards against stale loss schedules, Huber tables, causal clip bounds, dominance controllers, default dense-residual ALM, and duplicated canonical homes.
    verification:
      - kind: other
        ref: "python3 negative regex guard from 35-03-PLAN.md Task 3"
        status: pass
      - kind: other
        ref: "git diff --check -- pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
        status: pass
    human_judgment: false
metrics:
  started_at: 2026-06-29T03:10:00Z
  completed_at: 2026-06-29T03:21:51Z
  duration_seconds: 711
  tasks_completed: 3
  files_created: 1
  files_modified: 1
---

# Phase 35 Plan 03: Loss Assembly Contract Summary

`ctl_instruction.md` now carries Phase 35 total-loss assembly callouts for LOSS-01 through LOSS-04, with stable pointers to `pinn_architecture.md` for component math and no new semantic choices beyond the grounded evidence packets and owner-ratified D-04 Option A.

## Performance

- **Duration:** ~12 min
- **Started:** 2026-06-29T03:10:00Z
- **Completed:** 2026-06-29T03:21:51Z
- **Tasks:** 3
- **Files modified:** 1 framework spec + this summary

## Accomplishments

- Added `ctl_instruction.md` Phase 35 assembly callouts for LOSS-01, LOSS-02, and LOSS-03, including `AC-LOSS-01`, `AC-LOSS-01-AD`, `AC-LOSS-02`, and `AC-LOSS-03`.
- Transcribed D-04 / LOSS-04 as `RESOLVED-WITH-INSTRUCTION` owner-ratified Option A and removed the Phase 35 owner-pending causal-mode forward reference.
- Added a source-precedence guard that rejects or defers stale issue-doc constructs while preserving the canonical split: ctl owns assembly, `pinn_architecture.md` owns component formulas.

## Task Commits

| Task | Result | Commit |
|---|---|---|
| Task 1 - Add total-loss assembly callouts and component pointers | Added LOSS-01 through LOSS-03 assembly/status callouts and stable component-math pointers. | `50cc9ddf` |
| Task 2 - Transcribe D-04 owner-ratified causal mode in ctl assembly | Replaced owner-pending D-04 text with owner-ratified Option A, preserving dense-residual ALM rejection and deferred clip/scalar-ALM boundaries. | `83f82219` |
| Task 3 - Guard ctl source precedence and assembly ownership | Added the Phase 35 source-precedence and assembly-ownership guard. | `dce21ded` |

## Files Created/Modified

Created:

- `.planning/phases/35-loss-energy-weight-contracts/35-03-SUMMARY.md`

Modified:

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`

## Decisions Made

- No new semantic/spec decision was made by the executor.
- D-04 was transcribed from the existing GAP-32-01 `RESOLVED-WITH-INSTRUCTION` owner resolution, not re-decided.
- M15 replacement scheduling and dominance control remain rejected/deferred; NS-13 calibration remains deferred with `delta_E = 1.0` baseline.

## Verification

| Check | Result |
|---|---|
| Task 1 token check for `AC-LOSS-01`, `AC-LOSS-01-AD`, `AC-LOSS-02`, `AC-LOSS-03`, LOSS IDs, finding IDs, and `pinn_architecture.md` pointer | PASS |
| Task 1 `pinn_architecture.md` anchor check for `AC-LOSS-01` through `AC-LOSS-04` and component headings | PASS |
| Task 1/2/3 truncation and anchor guard for `Loss Function Formulation`, `The Definitive CTL-PINN Training Loop`, and `Data Flow During Training` | PASS |
| Task 2 D-04 owner-resolution check for `AC-LOSS-04`, `LOSS-04`, `D-04`, `RESOLVED-WITH-INSTRUCTION`, `w_1 = 1`, `eta_c = 1`, `dense-residual`, and `deferred` | PASS |
| Task 3 forbidden/default negative regex check | PASS |
| Phase 35 full suite token check across `ctl_instruction.md` and `pinn_architecture.md` | PASS |
| `git diff --check -- pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` | PASS |
| Commit deletion checks for `50cc9ddf`, `83f82219`, and `dce21ded` | PASS - no tracked deletions |

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- A first `apply_patch` attempt used a relative path and resolved against the main checkout, but the patch failed before changing any file. Both the main checkout and specwork `ctl_instruction.md` were verified to have no diff before reapplying with the specwork-rooted absolute path.
- Partial staging used an index-blob staging step for Task 2 so the D-04 hunk could be committed separately from the Task 3 guard without discarding owned working-tree edits.

## Auth Gates

None.

## Known Stubs

None. Stub scan found the pre-existing phrase `The placeholder L_total names the assembled scalar loss`; this is intentional spec wording, not an unwired UI/data stub.

## Threat Flags

None. This plan edited framework-spec documentation only and introduced no network endpoint, authentication path, file-access path, schema change, or runtime trust-boundary surface.

## Next Phase Readiness

Plan 35-04 can consume the Phase 35 ctl and pinn framework-spec callouts, then close ledger/verification state for LOSS-01 through LOSS-04.

## Self-Check: PASSED

- Found `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`.
- Found `.planning/phases/35-loss-energy-weight-contracts/35-03-SUMMARY.md`.
- Found task commits `50cc9ddf`, `83f82219`, and `dce21ded` in git history.
- Verified no tracked deletions were introduced by the task commits.

---
*Phase: 35-loss-energy-weight-contracts*
*Plan: 35-03*
*Completed: 2026-06-29*
