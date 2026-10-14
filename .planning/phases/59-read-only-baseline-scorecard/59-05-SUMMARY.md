---
phase: 59-read-only-baseline-scorecard
plan: 05
subsystem: verification
tags: [census, reader-acceptance, panel-rule, feas-02, scorecard-tolerance]

requires:
  - phase: 59-read-only-baseline-scorecard
    provides: Allowlisted reader, production reference trajectories, evidence writer, and the frozen scorecard
provides:
  - Stage-0 census functions and the frozen panel rule, tested on synthetic orbits and three real training systems
  - No audit or census evidence. The reader acceptance halted on the frozen IC13 tolerance.
affects: [59-06, 59-07, 59-08, 59-09, 59-10, 60]

actuals:
  tokens: 17036
  tasks: 1
  commits: 2
plan_head_before: 0f100e4c3bf48cdbf88df03e5ccd98a9ab0632fa

tech-stack:
  added: []
  patterns:
    - "N_in is the gold-grid unwrap of the inner separation about the t=0 normal, clipped to t <= 10"
    - "Validation census rows keep every difficulty field empty"
    - "Panels are selected only by the frozen scorecard rule"

key-files:
  created:
    - pinn/verification/stage0_census.py
    - tests/phase59/test_census.py
  modified: []

key-decisions:
  - "Reader acceptance halted. The monitor IC13 max abs is 1.1920928955078125e-07, above the frozen monitor_reproduction_ic13_abs of 1e-7. The tolerance was not changed and no audit file was written."
  - "The full census and the panels were not run, because the plan requires the reader acceptance before those numbers are committed."
  - "FEAS-02 stays pending."

patterns-established:
  - "CensusHalt prints CENSUS-HALT and writes nothing"

requirements-completed: []

coverage:
  - id: D1
    description: "Gold-grid revolution counts, gold-base agreement, and the frozen panel rule, with validation difficulty fields left empty"
    requirement: FEAS-02
    verification:
      - kind: unit
        ref: "tests/phase59/test_census.py#UnwrapTests,OuterRevolutionsTests,AssistedBaseTests,GoldBaseAgreementTests,PairTrackingTests,PanelRuleTests,PhaseAccuracyTests,ValidationRowTests,FreezeGuardCallTests"
        status: pass
      - kind: integration
        ref: "python -B -m pinn.verification.stage0_census --ids 1632,851,4658 --stdout"
        status: pass
    human_judgment: false
  - id: D2
    description: "Reader acceptance that the allowlisted reader matches generation 7's monitor batch"
    requirement: FEAS-02
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.stage0_census --acceptance"
        status: fail
    human_judgment: true
    rationale: "Targets, times, and masses match, but the IC13 residual is one float32 ulp over the frozen 1e-7 tolerance. Widening that tolerance is an owner decision."
  - id: D3
    description: "Difficulty census and the three frozen panels over the 1,812 Stage-0 training systems"
    requirement: FEAS-02
    verification: []
    human_judgment: true
    rationale: "Not run. The plan stops the census until the reader-acceptance halt is resolved."

duration: 90min
completed: 2026-10-14
status: halted
---

# Phase 59 Plan 05: Stage-0 Census Summary

**Census code is committed, but the reader acceptance halted because the monitor IC13 residual is one float32 ulp over the frozen 1e-7 tolerance**

## Performance

- **Duration:** about 90 min
- **Started:** 2026-10-14T02:40:00Z
- **Completed:** 2026-10-14T04:10:27Z
- **Tasks:** 1 of 3
- **Files modified:** 2

## Accomplishments

- The census module counts gold-grid inner and outer turns, checks gold-base agreement, and applies the frozen panel rule. Validation rows leave difficulty fields empty.
- Three real Stage-0 training systems (1632, 851, 4658) read through the allowlist give N_in 10.472, 18.612, and 39.349, each within 2% of the research preview, with pair tracking true, gold-base deviation at most 6.3e-10, and unwrap steps below pi.
- The reader acceptance did not pass, so the audit area and the full census were not written.

## Task Commits

1. **Task 1: Census rows, revolution counters, and the panel rule** - `f54eded0` (feat)
2. **Task 2: Reader acceptance** - not committed. Halted before any audit file was written.
3. **Task 3: Full census and panels** - not started.

**Plan metadata:** this summary.

## Files Created/Modified

- `pinn/verification/stage0_census.py` - Stage-0 census, reader acceptance, and panel rule
- `tests/phase59/test_census.py` - Synthetic tests for the nine required classes

## Decisions Made

The acceptance halt is owner-routed. No tolerance, panel rule, or scorecard byte was changed.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Coarse-orbit test compares against the float just below pi**
- **Found during:** Task 1 (revolution counters)
- **Issue:** An exact half-turn sampled at 0.4 samples per turn makes `atan2` return `3.1415926535897927`, one ulp under `pi`. `>= pi` failed even though the step is the alias bound.
- **Fix:** The test uses `np.nextafter(pi, 0)`. The counter itself is unchanged.
- **Files modified:** `tests/phase59/test_census.py`
- **Verification:** `tests.phase59.test_census` passes, 15 tests.
- **Committed in:** `f54eded0` (Task 1 commit)

**2. [Rule 2 - Missing critical] Acceptance and census modes were written with the tracer**
- **Found during:** Task 1 (one CLI module)
- **Issue:** The plan adds `--acceptance` and the default census in tasks 2 and 3. The freeze test already calls those modes, and the row builder is the same module.
- **Fix:** Both modes are in the task 1 module. Task 2 was still the first real acceptance run, and it halted before writing evidence. The census mode was not executed on the full population.
- **Files modified:** `pinn/verification/stage0_census.py`
- **Verification:** Freeze-guard tests return non-zero before the reader is built. The acceptance run halted with `CENSUS-HALT` and created no audit directory.
- **Committed in:** `f54eded0` (Task 1 commit)

---

**Total deviations:** 2 auto-fixed (1 bug, 1 missing critical)
**Impact on plan:** The test change does not move the alias bound. Landing the later CLI modes early did not write evidence and did not change the halt.

## Issues Encountered

- **Reader acceptance halt.** `stage0_census --acceptance` exited 2 in 2.626 s wall (`WALL-SECONDS 2.6260334579856135`). `monitor_batch_reproduction` reported rows 8192, identities 256, and zero mismatches of targets, times, and masses. `ic13_max_abs` and the normalizer recovery residual are both `1.1920928955078125e-07`. The frozen `monitor_reproduction_ic13_abs` is `1e-7`, so `passed` is false (over by `1.9209289550781255e-08`). The recovery residual is inside `normalizer_recovery_max_abs` of `1e-6`, so the GAP-59-06 fallback was not used. No file was written under `evidence/audit/`. The full census was not started.
- **Tracer (task 1), for the record.** `WALL-SECONDS 0.5377122499921825`. N_in was 10.471994061054543, 18.612048388702, and 39.34922738660542.
- **Probe.** `split_allowlist --probe-split test` printed `FREEZE-OK` and `"outcome": "refused_before_path"`.
- **Guards.** Phase 38/39 prohibition scans and `tests.phase59.test_static_guards` — 48 tests, OK.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Blocked. The owner needs to decide what to do with an IC13 difference of one float32 ulp (`2**-23`) against the frozen `1e-7` monitor tolerance. Options are to widen that frozen tolerance, or to record this result as an accepted deviation. This run did not choose either. Until that decision, plans that need the panels should not start.

## Self-Check: FAILED

Task 1's tests and the three-system tracer passed. Task 2's acceptance criterion (`passed: true` and `ic13_max_abs` at most `1e-7`) failed. Task 3 was not run. `ROADMAP.md` was not checked off.

---
*Phase: 59-read-only-baseline-scorecard*
*Completed: 2026-10-14*
