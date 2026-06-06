---
phase: 20-architecture-and-normalization-cleanup
plan: 05
subsystem: spec-adjudication
tags: [I_norm, naming-convention, ARCH-04, evidence-packet, D-02-NORM]

# Dependency graph
requires:
  - phase: 20-03
    provides: I_3 range/mapping edits landed before I_norm naming work
  - phase: 20-04
    provides: energy/mass support edits landed before I_norm naming work
provides:
  - D-02-NORM evidence packet with verdict and Locked Convention for I_norm naming
  - ctl_instruction.md with all live I_norm framework-spec surfaces raw-qualified as I_norm_raw
  - AC-ARCH-04 closure proof with positive and negative audits
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "I_norm_raw for raw physics/metadata inertia descriptor"
    - "I_norm_in = tanh(I_norm_raw) for the conditional widened-input ablation convention"
    - "I_norm (bare) is metadata only, not a final network IC slot"

key-files:
  created:
    - ".planning/phases/16-evidence-framework-and-issue-adjudication/evidence/D-02-NORM.md"
  modified:
    - ".planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md"
    - "pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"

key-decisions:
  - "Sources agree on raw-vs-bounded I_norm distinction; verdict accept-resolution"
  - "LaTeX surfaces (lines 671, 722, 728, 1433) needed _raw suffix beyond plan's initial enumeration"
  - "Error message string (line 753) updated to I_norm_raw for full consistency"

patterns-established:
  - "I_norm_raw: raw descriptor = trace(I_tensor) / (M_total * r_char^2 + eps)"
  - "I_norm_in: conditional widened-input ablation convention = tanh(I_norm_raw)"

requirements-completed:
  - ARCH-04

# Metrics
duration: 6min
completed: 2026-06-05
---

# Phase 20 Plan 05: Raw-vs-Bounded I_norm Naming Summary

**ARCH-04 closed: D-02-NORM evidence packet records accept-resolution verdict with I_norm_raw / I_norm_in = tanh(I_norm_raw) Locked Convention; post-review remediation verifies all 12 ctl_instruction.md I_norm surfaces are consistently named**

## Performance

- **Duration:** 6 min
- **Started:** 2026-06-05T14:41:00+08:00
- **Completed:** 2026-06-05T14:48:00+08:00
- **Tasks:** 3/3
- **Files modified:** 3

## Accomplishments

- Created evidence/D-02-NORM.md with both primary sources cited side by side, source agreement confirmed, verdict accept-resolution, and Locked Convention
- Aligned 7 ctl_instruction.md surfaces (6 LaTeX + 1 error message) to use I_norm_raw consistently; 5 other surfaces already correct
- Completed positive audit (12 surfaces all pass) and strengthened negative audit (0 ASCII or LaTeX bare I_norm naming surfaces remain)

## Task Commits

Each task was committed atomically:

1. **Task 1: Fill D-02-NORM packet** - `f80326a` (evidence)
2. **Task 2: Align I_norm naming in ctl_instruction.md** - `774778b` (spec)
3. **Task 3: Closure audit and AC-ARCH-04 verification** - `03a6220` (verify)

## Files Created/Modified

- `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/D-02-NORM.md` - Raw-vs-bounded I_norm adjudication packet with verdict, Locked Convention, closure proof audit
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` - D-02-NORM row advanced PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` - 7 I_norm surfaces updated to I_norm_raw (6 LaTeX + 1 error message), with `I_norm_in = tanh(I_norm_raw)` retained in D-02-NORM as the conditional ablation convention rather than a live framework-spec input surface

## Decisions Made

- **Sources agree:** Both `ctl_pinn_resolution.md` (lines 623-628, 1435-1443) and `01-architecture-and-physics-foundations.md` (lines 42-62) explicitly agree on the raw-vs-bounded distinction. No EVID-05 escalation needed.
- **Additional LaTeX surfaces found via rg:** The plan's initial enumeration listed 4 surfaces; post-review remediation found 6 LaTeX surfaces (lines 667, 671, 722, 728, 917, 1433) plus 1 error message string (line 753) that needed alignment. All are within the same spec sections and within scope.
- **Locked Convention:** I_norm_raw for the raw physics/metadata descriptor; I_norm_in = tanh(I_norm_raw) for the conditional widened-input ablation convention; I_norm (bare) is metadata only and not a live framework-spec input surface.

## Post-Review Remediation

- 2026-06-06: Corrected the missed Step 4 scope descriptor list surface from `I_{\text{norm}}` to `I_{\text{norm,raw}}`.
- Strengthened the negative audit to check both ASCII bare `I_norm` and LaTeX bare `I_{\text{norm}}` / `I_{\mathrm{norm}}`.

## Deviations from Plan

None - plan executed exactly as written. The plan instructed to "re-locate every I_norm surface by rg" which discovered additional surfaces beyond the initial enumeration. This is expected behavior, not a deviation.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- ARCH-04 / AC-ARCH-04 closed. D-02-NORM VERIFIED.
- All five Phase 20 architecture requirements (ARCH-01 through ARCH-05) now have VERIFIED findings in the Phase 16 ledger.
- Phase 20 closure is complete pending any final plan-level wrap-up.

---
*Phase: 20-architecture-and-normalization-cleanup*
*Completed: 2026-06-05*
