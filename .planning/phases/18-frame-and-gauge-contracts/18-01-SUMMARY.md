---
phase: 18-frame-and-gauge-contracts
plan: 01
subsystem: pinn-framework-spec
tags: [frame-contract, preprocessing-pipeline, com-boost, rotation-gauge, ac-frame-01]

# Dependency graph
requires:
  - phase: 16-evidence-framework-and-issue-adjudication
    provides: "Issue ledger, evidence packet template, VER-05 lifecycle, and AC-FRAME-01 reservation"
  - phase: 17-input-and-output-contracts
    provides: "Hard mass-weighted COM projection head in pinn_architecture.md Section 5.3"
provides:
  - "B-05 and M3 evidence packets opened with verdict accept-resolution"
  - "Unified Step 2 preprocessing pipeline in ctl_instruction.md"
  - "Canonical ordering relocated into Step 2.3 with original-file-order tie-break"
  - "Canonical rotation gauge with eta_gauge = 1e-8 dimensionless degeneracy guard"
  - "FRAME-02 output-side COM projection cross-reference in pinn_architecture.md"
  - "M3 advanced to VERIFIED under AC-FRAME-01 structural criteria; B-05 remains IN_PROGRESS for FRAME-03 sampling reconciliation"
affects: [18-02, 18-03, 19, 21, FUT-01]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Phase 18-local structural AC-FRAME-01 closure criteria are allowed only for M3 until FRAME-03 lands"
    - "FRAME-02 is split between preprocessed-sample assertions in ctl_instruction.md and output-side projection in pinn_architecture.md"
    - "M4 preservation uses a multiline rg check because the protected sentence is line-wrapped"

key-files:
  created:
    - ".planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-05.md - COM frame consistency evidence packet"
    - ".planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M3.md - Scaling-order evidence packet"
  modified:
    - ".planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md - B-05/M3 status rows and M3 VERIFIED transition"
    - "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md - Unified preprocessing pipeline, ordering relocation, rotation gauge, assertions, metadata"
    - "pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md - FRAME-02 output-side COM projection cross-reference"

key-decisions:
  - "Applied D-01/D-02: B-05 and M3 are uncontested accept-resolution findings; no EVID-05 adjudication was needed."
  - "Applied D-03/D-04: Step 2 and old Step 2.5 were consolidated, and canonical ordering moved from Step 4 to Step 2.3."
  - "Applied D-05/D-14: the rotation gauge fixes only initial orientation, preserves full 3D Cartesian trajectory semantics, and uses eta_gauge = 1e-8."
  - "Applied D-06: the Step 4 Mathematical Guarantees / M4 sentence remained untouched."
  - "Applied GAP-18-03: M3 may close against Phase 18-local AC-FRAME-01 structural criteria; B-05 waits for FRAME-03."

patterns-established:
  - "Frame/gauge spec edits must keep the live pinn/ implementation out of v1.4 evidence and reserve code divergence for FUT-01 hand-off artifacts."
  - "M3 closes against AC-FRAME-01 criteria 1, 2, 4, 5, 6, and 8; B-05 needs the full criteria set after sampling_method.md is updated."

requirements-completed:
  - FRAME-01
  - FRAME-02
  - FRAME-04
  - VER-05

# Metrics
duration: ~49min active execution, interrupted by GAP-18-05 resolution
completed: 2026-05-21T05:21:52Z
---

# Phase 18 P01: Unified Frame/Gauge Contract Summary

**The CTL spec now owns one ordered preprocessing pipeline, M3 is VERIFIED, and B-05 remains open only for the sampling-frame reconciliation planned in 18-02.**

## Performance

- **Duration:** ~49 min active execution, interrupted by GAP-18-05 resolution
- **Started:** 2026-05-21T04:31:41Z
- **Completed:** 2026-05-21T05:21:52Z
- **Tasks:** 3 plan tasks + plan summary
- **Files modified:** 5 plus this summary and state bookkeeping

## Accomplishments

- Created B-05 and M3 evidence packets with `accept-resolution` verdicts and AC-FRAME-01 structural criteria scoped by GAP-18-03.
- Rewrote `ctl_instruction.md` Step 2 into the unified pipeline: parser/mass check -> COM recenter -> zero-momentum boost -> canonical ordering -> rotation gauge -> global scaling -> assertions/metadata.
- Relocated canonical ordering from Step 4 to Step 2.3 and added the original-file-order final tie-break.
- Added the canonical rotation-gauge construction with `eta_gauge = 1e-8`, collinear fallback, deterministic sign handling, and full-3D output guard.
- Added the FRAME-02 architecture cross-reference and advanced M3 to `VERIFIED` while keeping B-05 `IN_PROGRESS` for plan 18-02.

## Task Commits

1. **Task 1: Write B-05 and M3 evidence packets** - `d31e82c` (docs: open frame evidence packets)
2. **Task 2: Replace Step 2/2.5 and relocate canonical ordering** - `83d6a0a` (docs: define unified preprocessing pipeline in ctl_instruction.md)
3. **Task 3: Reference output-side COM guarantee and verify Wave 1** - `26d9627` (docs: verify scaling order frame contract)

## Files Created/Modified

- `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-05.md` - New B-05 evidence packet; remains `IN_PROGRESS`.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M3.md` - New M3 evidence packet; advanced to `VERIFIED`.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` - B-05/M3 rows opened and M3 closure recorded.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` - Unified preprocessing pipeline and frame/gauge assertions.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` - FRAME-02 output-side COM projection guarantee cross-reference.

## Verification

- **Task 1 evidence gate:** PASS - B-05 and M3 packets exist, carry `accept-resolution`, and no live `pinn/` code is cited as v1.4 evidence.
- **Task 2 preprocessing gate:** PASS - unified Step 2, rotation-gauge markers, metadata keys, global scaling, and multiline M4-preservation checks all pass.
- **Task 3 wave gate:** PASS - FRAME-02 cross-reference exists, M3 is `VERIFIED`, B-05 remains `IN_PROGRESS`, M4 text is present, and there is no `pinn/` diff.
- **Formatting:** PASS - `git diff --check` is clean for the plan files and state bookkeeping.

## Deviations from Plan

None - plan scope and source boundaries were followed.

## Issues Encountered

- GAP-18-05 was already surfaced during Task 2 because the original single-line M4-preservation regex could not match the protected line-wrapped M4 sentence. The user resolved it by authorizing the multiline `rg -nU` check; M4 content remained untouched.

## Gap Handling

No new gaps were encountered after resuming Task 3. GAP-18-03, GAP-18-04, and GAP-18-05 were all `RESOLVED-WITH-INSTRUCTION` before M3 was moved to `VERIFIED`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plan 18-02 can proceed with FRAME-03. B-05 is intentionally still `IN_PROGRESS` until `sampling_method.md` reconciles hierarchical post-perturbation frame offsets and quasi-random COM/zero-momentum behavior.

## Self-Check: PASSED

- Key files created/modified by plan tasks exist.
- Task commits are present in git history.
- Task 3 automated verification passed after the final task commit.
- B-05 remains open for plan 18-02; M3 is verified under the authorized AC-FRAME-01 structural subset.

---
*Phase: 18-frame-and-gauge-contracts*
*Completed: 2026-05-21*
