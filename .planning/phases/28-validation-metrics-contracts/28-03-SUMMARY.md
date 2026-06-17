---
phase: 28-validation-metrics-contracts
plan: 03
subsystem: validation-metrics
tags: [ipr, stop-gap, evidence-ledger, validation-contracts]
requires:
  - phase: 28-validation-metrics-contracts
    provides: 28-02 parked state; 28-03 may proceed via locate-or-create only if its own units fork is settled
provides:
  - IPR EVID-06 packet with defer-with-blocker verdict
  - GAP-28-02 semantic STOP record for raw-vs-scaled unit convention
  - IPR ledger row DEFERRED with evidence-packet linkage
affects: [phase-28, phase-29, fut-01, ctl_instruction, pinn_architecture]
tech-stack:
  added: []
  patterns:
    - packet-before-edit enforcement for unit-bound validation metric gates
    - high-impact unit convention forks are deferred rather than inferred
key-files:
  created:
    - .planning/phases/25-evidence-framework-and-issue-ledger/evidence/ipr-physics-residual.md
    - .planning/phases/28-validation-metrics-contracts/28-03-SUMMARY.md
  modified:
    - .planning/phases/25-evidence-framework-and-issue-ledger/evidence/README.md
    - .planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md
    - .planning/phases/28-validation-metrics-contracts/28-GAPS.md
    - .planning/milestones/v1.5-GAPS.md
key-decisions:
  - "Q-C3 raw-vs-scaled unit convention was not resolved by the agent; GAP-28-02 is OPEN for user sign-off."
  - "No IPR framework-spec clause or architecture dual-epsilon note was landed because the packet verdict is defer-with-blocker."
  - "[SUPERSEDED 2026-06-16, UAT Pass 2] GAP-28-02 RESOLVED-WITH-INSTRUCTION (raw G=1 units); IPR clause landed in ctl_instruction.md Step-1A + pinn_architecture.md §3.4 dual-epsilon note; AC-VAL-03 PASS; ledger VERIFIED. The parked-state body sections below (Issues Encountered, Self-Check, Next Phase Readiness) are the historical first-park STOP record — their 'GAP-28-02 is OPEN', counters 8/2, 'DEFERRED / No spec edit landed', and 'Phase 28 cannot close' lines are NOT current state. See 28-UAT.md Pass 2."
patterns-established:
  - "Dimensionful validation metrics must bind threshold values to explicit units before spec transcription."
requirements-completed: [VAL-03]
duration: 4 min
completed: 2026-06-16
---

# Phase 28 Plan 03: IPR Evidence Packet Summary

**IPR raw-vs-scaled unit fork parked with a defer-with-blocker evidence packet and GAP-28-02 user sign-off gate**

> **RESUMED 2026-06-16 — GAP-28-02 RESOLVED-WITH-INSTRUCTION (raw G=1 units).** The EDL gold-flag-rate
> tripwire was inconclusive (both raw and scaled saturate the admitted-set proxy), so the user selected
> Option A (raw) on grounded convention-consistency — the pipeline computes conservation in raw G=1
> units. Plan 03 Task 2/3 executed: the IPR clause (raw units, Hermite/PCHIP-prohibited, eps_inv=1e-10,
> dual-epsilon IPR_train separation) landed in `ctl_instruction.md` Step-1A `Data-side quality-metric
> contracts`, plus a `pinn_architecture.md` §3.4 dual-epsilon visibility note; AC-VAL-03 PASS; IPR ledger
> row → VERIFIED. The `1e-3` threshold is provisional (mis-calibrated in both conventions per EDL;
> doc-03/FUT-01 recalibration). The parked-state narrative below is retained as the original record.

## Performance

- **Duration:** 4 min
- **Started:** 2026-06-16T04:03:00Z
- **Completed:** 2026-06-16T04:06:00Z
- **Tasks:** 1/3 executed; Task 2/3 spec/AC flow parked by STOP outcome
- **Files modified:** 6

## Accomplishments

- Created `evidence/ipr-physics-residual.md` from the Phase 25 packet schema in the required non-conflict/deferred shape.
- Added the `IPR -> evidence/ipr-physics-residual.md` ID-to-filename map row.
- Recorded `defer-with-blocker` because the Q-C3 raw-vs-scaled unit fork remains a semantic sign-off decision with ~464x gate impact.
- Extended `28-GAPS.md` with GAP-28-02 and mirrored it into `.planning/milestones/v1.5-GAPS.md`, updating `total_gaps` and `open_gaps`.
- Moved the IPR ledger row to DEFERRED with packet linkage and GAP-28-02 provenance. No `ctl_instruction.md` or `pinn_architecture.md` IPR spec edit was made.

## Task Commits

1. **Task 1: Author IPR packet and adjudicate Q-C3 units fork** - `aea6747` (plan parked)
2. **Task 2: Append IPR clause and arch note** - not run; blocked by GAP-28-02
3. **Task 3: Close ledger/summary** - `aea6747` (DEFERRED closeout)

**Provenance backfill:** expected follow-up commit `verify(28-03): backfill commit sha`.

## Files Created/Modified

- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/ipr-physics-residual.md` - Records the IPR evidence packet, `defer-with-blocker` verdict, cited sources, and pending-SHA transition log.
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/README.md` - Adds the IPR packet filename map row.
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` - Moves IPR to DEFERRED with the packet link and GAP-28-02.
- `.planning/phases/28-validation-metrics-contracts/28-GAPS.md` - Adds GAP-28-02.
- `.planning/milestones/v1.5-GAPS.md` - Mirrors GAP-28-02 and updates gap counters.
- `.planning/phases/28-validation-metrics-contracts/28-03-SUMMARY.md` - Captures the parked plan outcome.

## Decisions Made

The agent did not choose a raw or scaled unit convention. The dimension analysis is clear that IPR is acceleration-squared and that raw/scaled readings differ by about 464x against the same `1e-3` flag. The cited sources do not prove which unit convention authored the threshold: DQA gives the metric and gate but no unit pin, and its "Load and Normalize" wording prevents treating on-load placement as raw-units proof. The resolution doc's raw-units candidate remains a candidate, not authority.

## Deviations from Plan

None - this is the planned outcome (b) path for an unsettled Q-C3 units fork.

## Issues Encountered

GAP-28-02 is OPEN. The IPR framework-spec clause, architecture dual-epsilon note, and AC-VAL-03 structural check are parked until the user chooses a unit convention or explicitly defers it.

## Self-Check: PASSED

- `ipr-physics-residual.md` exists with both primary sources, DQA §3.3, CLM-09/CLM-10, ctl/architecture dual-epsilon context, FUT-01 handoff note, verdict, before/after note, AC-VAL-03, and status log.
- Evidence README contains the `IPR` filename-map row.
- IPR ledger row is DEFERRED with `defer-with-blocker`, the packet link, and GAP-28-02.
- `28-GAPS.md` contains GAP-28-02 with required STOP fields.
- `.planning/milestones/v1.5-GAPS.md` has `total_gaps: 8`, `open_gaps: 2`, `last_updated: 2026-06-16`, and a Phase 28 GAP-28-02 row.
- No IPR spec edit landed in `ctl_instruction.md` or `pinn_architecture.md`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 28 cannot close while GAP-28-02 is OPEN. Independent work may proceed only if it does not depend on a canonical IPR unit convention. Any later resumption of 28-03 must resolve GAP-28-02 first, then land the IPR clause, architecture disambiguation note, and AC-VAL-03 from the packet outcome.

---
*Phase: 28-validation-metrics-contracts*
*Completed: 2026-06-16*
