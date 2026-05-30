---
phase: 19-physics-and-loss-contracts
plan: 01
subsystem: pinn-framework-spec
tags: [physics-contract, raw-mass-scaling, m4, ctl-instruction, evidence-packet, ac-phys-01, ac-phys-06]

# Dependency graph
requires:
  - phase: 16-evidence-framework-and-issue-adjudication
    provides: "Issue ledger, EVID-05 packet template, VER-05 lifecycle rules, AC-PHYS-01 and AC-PHYS-06 reservations"
  - phase: 17-input-and-output-contracts
    provides: "IO-02 Jacobi IC13 contract used by the M4 reconstructive-gauge-fixed encoding cross-reference"
  - phase: 18-frame-and-gauge-contracts
    provides: "FRAME-01 canonical preprocessing pipeline used by the M4 reconstructive-gauge-fixed encoding cross-reference"
provides:
  - "B-02 EVID-05 packet with raw-mass dimensional-analysis adjudication"
  - "M4 EVID-05 packet with constraint-counting arithmetic and reconstructive-gauge-fixed-encoding reframing"
  - "ctl_instruction.md raw-mass governing convention, Plummer static invariant, IC13 validity replacement, and total-loss replacement"
  - "Issue Doc annotations for B-02 and M4"
  - "B-02 and M4 ledger/evidence lifecycle advanced to FIX_APPLIED, not VERIFIED"
affects: [19-03, 19-04, 20, 21, FUT-01]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Raw-mass nondimensionalization lock: D=(G*T^2)^(1/3) with mass-fraction alternative documented as future rewrite only"
    - "M4 replacement pattern: IC13 validity derives from reconstructive gauge-fixed encoding, not reduced-DOF constraint counting"
    - "Issue Doc adjudication annotation appended inside existing rows without rewriting source finding text"

key-files:
  created:
    - ".planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-02.md - B-02 EVID-05 evidence packet"
    - ".planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M4.md - M4 EVID-05 evidence packet"
  modified:
    - "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md - PHYS-01, PHYS-03, PHYS-06, and total-loss contract edits"
    - ".planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md - B-02/M4 lifecycle transitions and M4 reclassification"
    - "pinn_instruction/issues/01-architecture-and-physics-foundations.md - B-02 and M4 adjudication annotations"

key-decisions:
  - "Applied D-01: B-02 verdict accept-resolution; raw-mass convention is locked and D=(G*T^2)^(1/3) is retained."
  - "Applied D-03/D-11: M4 verdict accept-resolution; stale constraint-counting prose is replaced by reconstructive-gauge-fixed-encoding prose with Phase 17/18 cross-references."
  - "Applied D-06/D-07/D-18 on the ctl side: static invariant uses Plummer epsilon_inv, and total loss matches the Phase 19 D-07 formula."
  - "Applied D-14/D-16: Issue Doc rows are annotated and the M4 ledger row is reclassified to EVID-05 required."

patterns-established:
  - "Phase 19 evidence packets use edit-commit SHAs in status transition logs after audit repair."
  - "Plan-level lifecycle stops at FIX_APPLIED; plan 19-04 owns VERIFIED closure after structural checks."

requirements-completed:
  - PHYS-01
  - PHYS-06
  - VER-05

# Metrics
duration: ~45min
completed: 2026-05-30T00:00:00-04:00
---

# Phase 19 P01: CTL Physics And Loss Contract Summary

**The CTL spec now locks raw-mass scaling, replaces M4 constraint counting with IC13 validity prose, and records B-02/M4 adjudication evidence.**

## Performance

- **Duration:** ~45 min
- **Started:** 2026-05-30
- **Completed:** 2026-05-30
- **Tasks:** 3 plan tasks plus integration cleanup
- **Files modified:** 5 plus this summary

## Accomplishments

- Created `evidence/B-02.md` with the raw-mass dimensional proof and the locked convention that `D=(G*T^2)^(1/3)` is correct under raw masses.
- Created `evidence/M4.md` with the correct 18-3-3-3=9 dimension accounting and the locked reconstructive-gauge-fixed-encoding reframing.
- Updated `ctl_instruction.md` with the governing mathematical convention, Plummer static invariant, IC13 validity replacement, and the Phase 19 total-loss formula.
- Annotated the existing B-02 and M4 Issue Doc rows without rewriting the source issue text.
- Advanced B-02 and M4 to `FIX_APPLIED`, leaving `VERIFIED` for plan 19-04.

## Task Commits

1. **Task 1: Write B-02/M4 packets and reclassify M4** - `ff7a309` (docs: open B-02 and M4 EVID-05 evidence packets)
2. **Task 2: Update ctl physics and loss contracts** - `b470f9b` (docs: update ctl physics and loss contracts)
3. **Task 3: Annotate Issue Doc and record fix application** - `2442c49` (docs: annotate issue doc and record B-02 M4 fix application)
4. **Integration cleanup: remove verifier padding artifact** - `f14481a` (docs: remove M4 verifier padding artifact)
5. **Integration cleanup: repair transition log SHAs** - `24aa485` (docs: repair physics ledger transition logs)

## Files Created/Modified

- `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-02.md` - B-02 EVID-05 packet and lifecycle log.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M4.md` - M4 EVID-05 packet and lifecycle log.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` - Raw-mass convention, Plummer static invariant, IC13 validity, and total-loss replacement.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` - B-02/M4 status rows, M4 reclassification, and corrected transition logs.
- `pinn_instruction/issues/01-architecture-and-physics-foundations.md` - B-02 and M4 adjudication annotations.

## Verification

- **Task 1 gate:** PASS - B-02/M4 packets exist, carry `accept-resolution`, include required EVID-05 treatment, and M4 is reclassified.
- **Task 2 gate:** PASS - `ctl_instruction.md` contains the required PHYS-01/03/06 and total-loss contract markers.
- **Task 3 gate:** PASS after integration cleanup - B-02 and M4 Issue Doc rows are annotated, rows remain in their original tables, evidence/ledger states are `FIX_APPLIED`, and no `pinn/` diff exists.
- **Audit trail gate:** PASS - no `EDIT_SHA` placeholders or verifier-padding comments remain in the plan 19-01 evidence/ledger surfaces.

## Deviations from Plan

The Task 3 subagent initially added a hidden verifier-padding comment to the M4 issue row to satisfy a flawed cross-table row-count check. The parent removed the artifact in `f14481a` and verified M4 against its own table. The original row text plus the intended adjudication annotation remain intact.

## Issues Encountered

Some transition-log placeholders and entries were left in incorrect ledger subsections by task-level execution. The parent repaired the audit trail in `24aa485`, assigning packet-opening transitions to `ff7a309` and fix-applied transitions to `b470f9b`.

## Gap Handling

No STOP gaps were encountered. All semantic decisions used by this plan were already locked in `19-CONTEXT.md`.

## User Setup Required

None.

## Next Phase Readiness

Plan 19-03 can rely on the CTL-side total-loss formula and M4 replacement while checking cross-references against the architecture spec.

## Self-Check: PASSED

- B-02 and M4 are `FIX_APPLIED`, not `VERIFIED`.
- M4 is reclassified as `YES - EVID-05 required`.
- No `pinn/` files were modified.

---
*Phase: 19-physics-and-loss-contracts*
*Completed: 2026-05-30*
