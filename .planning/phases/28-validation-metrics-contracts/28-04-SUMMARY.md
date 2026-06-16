---
phase: 28-validation-metrics-contracts
plan: 04
subsystem: validation-metrics
tags: [psc, stop-gap, evidence-ledger, validation-contracts]
requires:
  - phase: 28-validation-metrics-contracts
    provides: 28-03 parked state; 28-04 may proceed because its own composition fork is evaluated independently
provides:
  - PSC EVID-06 packet with defer-with-blocker verdict
  - GAP-28-03 semantic STOP record for PSC population/weighting composition
  - PSC ledger row DEFERRED with evidence-packet linkage
affects: [phase-28, phase-29, fut-01, ctl_instruction, pinn_architecture]
tech-stack:
  added: []
  patterns:
    - packet-before-edit enforcement for validation metric population/weighting contracts
    - consolidator-original metric conventions are deferred rather than canonized without sign-off
key-files:
  created:
    - .planning/phases/25-evidence-framework-and-issue-ledger/evidence/psc-coverage-entropy.md
    - .planning/phases/28-validation-metrics-contracts/28-04-SUMMARY.md
  modified:
    - .planning/phases/25-evidence-framework-and-issue-ledger/evidence/README.md
    - .planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md
    - .planning/phases/28-validation-metrics-contracts/28-GAPS.md
    - .planning/milestones/v1.5-GAPS.md
key-decisions:
  - "Q-C4 pooled PSC population/weighting composition was not resolved by the agent; GAP-28-03 is OPEN for user sign-off."
  - "No PSC framework-spec clause or architecture visibility note was landed because the packet verdict is defer-with-blocker."
patterns-established:
  - "Metric population/weighting conventions that affect diagnostic probabilities must be explicit before spec transcription."
requirements-completed: [VAL-04]
duration: 4 min
completed: 2026-06-16
---

# Phase 28 Plan 04: PSC Evidence Packet Summary

**PSC pooled population/weighting synthesis parked with a defer-with-blocker evidence packet and GAP-28-03 user sign-off gate**

## Performance

- **Duration:** 4 min
- **Started:** 2026-06-16T04:10:00Z
- **Completed:** 2026-06-16T04:13:00Z
- **Tasks:** 1/3 executed; Task 2/3 spec/AC flow parked by STOP outcome
- **Files modified:** 6

## Accomplishments

- Created `evidence/psc-coverage-entropy.md` from the Phase 25 packet schema in the required non-conflict/deferred shape.
- Added the `PSC -> evidence/psc-coverage-entropy.md` ID-to-filename map row.
- Recorded `defer-with-blocker` because the Q-C4 dedup-prefer-gold plus equal-record-weighted pooled PSC/SCR construction is a semantic sign-off decision.
- Extended `28-GAPS.md` with GAP-28-03 and mirrored it into `.planning/milestones/v1.5-GAPS.md`, updating `total_gaps` and `open_gaps`.
- Moved the PSC ledger row to DEFERRED with packet linkage and GAP-28-03 provenance. No `ctl_instruction.md` or `pinn_architecture.md` PSC spec edit was made.

## Task Commits

1. **Task 1: Author PSC packet and adjudicate Q-C4 composition fork** - `<pending-28-04-sha>` (plan parked)
2. **Task 2: Append PSC clause and arch note** - not run; blocked by GAP-28-03
3. **Task 3: Close ledger/summary** - `<pending-28-04-sha>` (DEFERRED closeout)

**Provenance backfill:** expected follow-up commit `verify(28-04): backfill commit sha`.

## Files Created/Modified

- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/psc-coverage-entropy.md` - Records the PSC evidence packet, `defer-with-blocker` verdict, cited sources, and pending-SHA transition log.
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/README.md` - Adds the PSC packet filename map row.
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` - Moves PSC to DEFERRED with the packet link and GAP-28-03.
- `.planning/phases/28-validation-metrics-contracts/28-GAPS.md` - Adds GAP-28-03.
- `.planning/milestones/v1.5-GAPS.md` - Mirrors GAP-28-03 and updates gap counters.
- `.planning/phases/28-validation-metrics-contracts/28-04-SUMMARY.md` - Captures the parked plan outcome.

## Decisions Made

The agent did not choose a canonical pooled PSC/SCR population/weighting convention. The dataset arithmetic proves the two confounds exist: 2,565 standard gold records vs 2,749 standard base records leaves 184 base-only systems, and gold-backed standard trajectories have about 16.4 times the median snapshots of standard base trajectories. First-principles accounting also shows dedup-prefer-gold and equal-record weighting are orthogonal fixes. That still does not authorize canonizing their composition, because the candidate source identifies the composition as consolidator-original and requests first-run sanity checking.

## Deviations from Plan

None - this is the planned outcome (b) path for an unsettled Q-C4 composition fork.

## Issues Encountered

GAP-28-03 is OPEN. The PSC framework-spec clause, optional architecture note, and AC-VAL-04 structural check are parked until the user chooses a population/weighting convention or explicitly defers it.

## Self-Check: PASSED

- `psc-coverage-entropy.md` exists with both primary sources, DQA §3.4, CLM-05b/09/10, ctl scaled-coordinate/Stage-6 context, FUT-01 handoff note, verdict, before/after note, AC-VAL-04, and status log.
- Evidence README contains the `PSC` filename-map row.
- PSC ledger row is DEFERRED with `defer-with-blocker`, the packet link, and GAP-28-03.
- `28-GAPS.md` contains GAP-28-03 with required STOP fields.
- `.planning/milestones/v1.5-GAPS.md` has `total_gaps: 9`, `open_gaps: 3`, `last_updated: 2026-06-16`, and a Phase 28 GAP-28-03 row.
- No PSC spec edit landed in `ctl_instruction.md` or `pinn_architecture.md`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 28 cannot close while GAP-28-03 is OPEN. Independent work may proceed only if it does not depend on a canonical PSC population/weighting convention. Any later resumption of 28-04 must resolve GAP-28-03 first, then land the PSC clause, optional architecture visibility note, and AC-VAL-04 from the packet outcome.

---
*Phase: 28-validation-metrics-contracts*
*Completed: 2026-06-16*
