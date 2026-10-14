---
phase: 59-read-only-baseline-scorecard
plan: 07
subsystem: verification
tags: [diag07, jx-10, gate-g1, memory-preflight, generation-7]

requires:
  - phase: 59-read-only-baseline-scorecard
    provides: Frozen scorecard, allowlisted corpus doorway, and the evidence writer with the 6 GiB launch preflight
provides:
  - Unit-tested DIAG-07 driver library and the JX-10 entry point
  - No JX-10, JX-1, or Gate G1 evidence. The detached launch halted on the frozen memory preflight.
affects: [59-09, 59-10, 61]

actuals:
  tokens: 15318
  tasks: 0
  commits: 3
plan_head_before: 1b31079c188380528161a6ff41ddc4e05a815a72

tech-stack:
  added: []
  patterns:
    - "DIAG-07 loads generation 7 from a blob-checked git archive and the five Phase 59 overlays from the repository"
    - "The shared launch lock is evidence/logs/launch.lock.log, taken after the freeze and before the vm_stat preflight"
    - "A float64 cross-check loads the float32 checkpoint first, because the monitor hash is raw float32 bytes, then promotes"

key-files:
  created:
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/diag07_common.py
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx01_jx10.py
    - tests/phase59/test_diag07.py
  modified: []

key-decisions:
  - "The JX-10 launch halted. vm_stat reported 4899373056 available bytes against the required 6442450944. The 6 GiB bar was not lowered and no result JSON was written."
  - "Gate G1 was not computed. There is no physics-share outcome."
  - "DIAG-07 stays pending."

patterns-established:
  - "DIAG07-PREFLIGHT exits 4, records the launch failure, releases the lock, and writes no result"

requirements-completed: []

coverage:
  - id: D1
    description: "Snapshot identity, checkpoint registry, refusing store, monitor-field formulas, and the launch lock"
    requirement: DIAG-07
    verification:
      - kind: unit
        ref: "tests/phase59/test_diag07.py#SnapshotIdentityTests,RegistryTests,RunBookkeepingTests,RefusingStoreTests,MonitorFieldsTests,ModuleProvenanceTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "JX-10 re-score of the generation-7 frozen monitor on MPS and CPU"
    requirement: DIAG-07
    verification:
      - kind: other
        ref: ".planning/phases/59-read-only-baseline-scorecard/evidence/diag07/logs/jx10.log"
        status: fail
    human_judgment: true
    rationale: "The detached launch exited 4 with DIAG07-PREFLIGHT before any checkpoint was read. Available memory was 4899373056 bytes and the frozen requirement is 6442450944. No tolerance was changed."
  - id: D3
    description: "JX-1 per-term gradients, Adam-preconditioned shares, and Gate G1"
    requirement: DIAG-07
    verification: []
    human_judgment: true
    rationale: "Not run. The plan stops once the JX-10 launch is refused, and Gate G1 has no recorded outcome."

duration: 27min
completed: 2026-10-14
status: halted
---

# Phase 59 Plan 07: Read-Only Checkpoint Experiments Summary

**Gate G1 has no outcome: the JX-10 launch halted at the frozen 6 GiB preflight, with 4899373056 bytes available, and JX-1 was not started**

## Performance

- **Duration:** 27 min
- **Started:** 2026-10-14T04:10:27Z
- **Completed:** 2026-10-14T04:37:16Z
- **Tasks:** 0 of 3 completed
- **Files modified:** 3

## Accomplishments

- The driver library checks a generation-7 `git archive` blob-for-blob, loads the five overlay modules from the repository, and refuses a second pinn import.
- Unit tests cover the registry (including the real `best.pt` step of 900), the refusing store, monitor prefix formulas, and the shared launch lock.
- The detached JX-10 launch did not score a checkpoint. Gate G1 was not computed.

## Task Commits

1. **Task 1: JX-10 driver** - `16f5f0db` (test) and `12c5420d` (feat). The experiment itself halted before a result file existed.
2. **Task 2: JX-1 and Gate G1** - not started.
3. **Task 3: Committed combined run** - not started.

**Plan metadata:** this summary.

## Files Created/Modified

- `.planning/phases/59-read-only-baseline-scorecard/evidence/diag07/diag07_common.py` - Snapshot bootstrap, registry load, refusing store, monitor fields, and launch bookkeeping
- `.planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx01_jx10.py` - JX-10 entry point. JX-1 is not implemented in this revision.
- `tests/phase59/test_diag07.py` - Failing-then-passing tests for the task 1 behaviors

## Decisions Made

The preflight halt is owner-routed. The required 6 GiB (`6442450944` bytes) was not reduced. No scorecard byte, tolerance, or reading rule was changed. `optimizer_constructed` is true when no optimizer object exists, because the verifier treats that boolean as a passed check. A float64 runtime is loaded at float32 and promoted afterward, because the checkpoint's monitor hash is the raw float32 bytes. That path was not executed.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing critical] Float64 load promotes after the float32 restore**
- **Found during:** Task 1 (controller load)
- **Issue:** The generation-7 restore hashes monitor tensors as raw float32 bytes, so `load_state_dict` into a float64 model fails the trainer's own check.
- **Fix:** The float64 runtime builds and loads at float32, then promotes the model and the restored monitor batch to float64. The file SHA-256 check still happens on the original bytes.
- **Files modified:** `.planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx01_jx10.py`
- **Verification:** Not reached. The launch returned before any checkpoint load.
- **Committed in:** `12c5420d` (Task 1 feat)

---

**Total deviations:** 1 auto-fixed (1 missing critical)
**Impact on plan:** The promotion is unexercised. It does not change the preflight halt.

## Issues Encountered

- **Memory preflight halt.** `jx01_jx10.py --experiment jx10` exited 4 in well under a second. The log line is `DIAG07-PREFLIGHT: available 4899373056 bytes < required 6442450944 bytes`, then `EXIT=4`. The failure record is in `evidence/logs/launch-failures.log` (`run_id` `0cd0b6a77d2f49ae86141b503f7c472d`). The launch lock was released. No file was written under `evidence/diag07/` except the gitignored log. JX-1 and Gate G1 were not started.
- **Tests.** `tests.phase59.test_diag07` and `tests.phase59.test_static_guards` together: 23 tests, OK, after the feat commit.
- **TDD.** RED `16f5f0db` failed 8 tests on `diag07_common.py is required`. GREEN `12c5420d` passed those 8 tests. Task 2's RED/GREEN cycle did not start.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Blocked. DIAG-07 needs about 6 GiB of free, inactive, and speculative memory at the moment of launch (`vm_stat`, not the footprint reader). This machine reported 4899373056 bytes while Chrome, Claude, and Codex were resident. Free that memory and relaunch the same command. Do not lower `required_bytes`. Until `jx10.log` ends in `EXIT=0` and `jx10.done.json` exists, do not start JX-1, the combined run, or plan 59-09.

## Self-Check: FAILED

Task 1's unit tests passed. The JX-10 acceptance run failed the frozen preflight and wrote no `jx10.json`. Tasks 2 and 3 were not run. `ROADMAP.md` was not checked off. Gate G1 has no outcome.

---
*Phase: 59-read-only-baseline-scorecard*
*Completed: 2026-10-14*
