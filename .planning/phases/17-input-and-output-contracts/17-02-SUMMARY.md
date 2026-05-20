---
phase: 17-input-and-output-contracts
plan: 02
subsystem: pinn-framework-spec
tags: [output-contract, com-projection, ad-derived-kinematics, evidence-packet, ac-io-03]

# Dependency graph
requires:
  - phase: 17-input-and-output-contracts
    provides: "17-01 input contract: canonical 14D [tau, IC_13], ordered raw mass slots, Phase 18/19 forward references"
provides:
  - "B-06 evidence packet with verdict accept-resolution"
  - "Hard mass-weighted COM projection formula in pinn_architecture.md Section 5.3"
  - "Position-only CTL training-flow wording with AD-derived velocities and accelerations"
  - "B-06 ledger and evidence status advanced PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED"
affects: [17-03, 18, 19, 21, FUT-01]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Output contract: raw 9D position head followed by hard mass-weighted COM projection before any consumer"
    - "Velocity/acceleration contract: AD-derived from projected positions; Phase 19 owns componentwise derivative tests"
    - "Two-commit audit-SHA pattern for evidence-packet transition logs"

key-files:
  created:
    - ".planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-06.md - Output contract evidence packet"
  modified:
    - "pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md - Hard COM projection formula and projected-output consumption rule"
    - "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md - Training-flow network prediction wording"
    - ".planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md - B-06 status row and transition log"

key-decisions:
  - "Accepted D-02 / B-06 resolution: network emits raw 9D positions only, then applies a hard mass-weighted COM projection before losses, residuals, diagnostics, metrics, or evaluation."
  - "Preserved Phase 19 boundary: 17-02 names AD-derived velocities/accelerations and chain-rule responsibility but does not define the componentwise derivative test."
  - "Used ordered raw pre-tanh mass metadata as the COM projection weight source per Phase 17 D-02 and 17-01 D-07."

patterns-established:
  - "B-06 uses the non-contested packet pattern: EVID-05-only sections are marked `Not contested` because source direction is aligned after D-02."
  - "AC-IO-03 closure requires both spec edits and regression checks for 17-01 input contracts before ledger status reaches VERIFIED."

requirements-completed:
  - IO-03
  - VER-05

# Metrics
duration: ~50min
completed: 2026-05-19T23:05:00Z
---

# Phase 17 P02: Output Contract Implementation Summary

**Raw 9D position output now flows through a hard mass-weighted COM projection before consumers, with velocities and accelerations defined as AD-derived quantities.**

## Performance

- **Duration:** ~50 min
- **Started:** 2026-05-19T22:15:00Z
- **Completed:** 2026-05-19T23:05:00Z
- **Tasks:** 3 plan tasks + plan summary
- **Files modified:** 4

## Accomplishments

- Created `evidence/B-06.md` with side-by-side primary-source citations, `accept-resolution` verdict, AC-IO-03 pass text, and no live-code-as-evidence citation.
- Added the hard mass-weighted COM projection formula to `pinn_architecture.md` immediately after the output reference-frame bullets, including the raw pre-tanh mass metadata rule and projected-output consumption rule.
- Replaced the CTL training-flow claim that the network outputs positions and velocities with position-only output wording aligned to the architecture spec.
- Advanced B-06 through `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED` only after AC-IO-03 and 17-01 regression checks passed.

## Task Commits

1. **Task 1: Write B-06 evidence packet and open ledger status** - `a052e35` (docs: open output contract evidence packet)
   - Audit SHA recording - `796668a`
2. **Task 2: Add COM projection formula and output consumption rule** - `44c3f15` (docs: add hard com projection contract)
3. **Task 3: Replace CTL direct-velocity wording and verify B-06** - `55c1805` (docs: verify output contract)
   - Audit SHA recording - `2a5b6fd`

## Files Created/Modified

- `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-06.md` - New B-06 evidence packet and AC-IO-03 status log.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` - B-06 row and per-finding transition log.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` - Hard mass-weighted COM projection formula and projected-output consumer rule.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` - CTL training-flow network prediction bullet aligned to position-only output.

## Verification

- **AC-IO-03:** PASS - B-06 packet exists, both specs contain 9D/COM/AD-derived wording, and B-06 is `VERIFIED`.
- **17-01 regression checks:** PASS - B-03, B-04, M1, and M2 evidence packets still exist; IO-01/IO-02 strings remain present; ledger rows remain `VERIFIED`.
- **Negative output wording scan:** PASS - before Source Issues metadata, neither spec contains `outputs.*velocities` or `network outputs.*velocities`.

## Deviations from Plan

None - the plan scope and source boundaries were followed.

## Issues Encountered

- The Task 2 verification regex for the LaTeX literal `R_{\mathrm{COM}}` failed because the regex engine treated `\mathrm` as an invalid escape sequence. Re-ran the same content check with fixed literal matching for `R_{\mathrm{COM}}`; the verification passed.

## Gap Handling

No STOP gaps were encountered. Sidecar grounding confirmed the core B-06 contract is explicitly grounded. The only boundary noted is that Phase 19, not Phase 17, owns componentwise derivative-test details.

## Next Phase Readiness

17-03 can now run the cleanup and divergence inventory: AC-IO-03 is green, B-06 is verified, and output-side spec wording is aligned without editing `pinn/` implementation files.

---
*Phase: 17-input-and-output-contracts*
*Completed: 2026-05-19*
