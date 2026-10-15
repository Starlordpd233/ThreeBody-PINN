---
phase: 59-read-only-baseline-scorecard
plan: 07
subsystem: verification
tags: [diag07, jx-10, gate-g1, tolerance-boundary, generation-7]

requires:
  - phase: 59-read-only-baseline-scorecard
    provides: Frozen scorecard, allowlisted corpus doorway, and the evidence writer with the 6 GiB launch preflight
provides:
  - Unit-tested DIAG-07 driver library and JX-10 entry point, with a working float64 CPU cross-check
  - One complete but unaccepted JX-10 development run on MPS float32 and CPU float64 (53 of 54 frozen checks pass)
  - No accepted JX-10, JX-1, or Gate G1 evidence
affects: [59-09, 59-10, 61]

actuals:
  tokens: 15147
  tasks: 0
  commits: 5
plan_head_before: 1b31079c188380528161a6ff41ddc4e05a815a72

tech-stack:
  added: []
  patterns:
    - "DIAG-07 loads generation 7 from a blob-checked git archive and the five Phase 59 overlays from the repository"
    - "The shared launch lock is evidence/logs/launch.lock.log, taken after the freeze and before the vm_stat preflight"
    - "A float64 cross-check is built as the permitted (float64, cpu) runtime, demoted to float32 for the trainer's own restore checks, then promoted back"

key-files:
  created:
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/diag07_common.py
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx01_jx10.py
    - tests/phase59/test_diag07.py
  modified: []

key-decisions:
  - "The JX-10 acceptance run halted at the tracer gate on one frozen-tolerance boundary case. The comparison code and every frozen value were left as they were when the result was seen."
  - "Gate G1 was not computed. There is no physics-share outcome."
  - "DIAG-07 stays pending."

patterns-established:
  - "DIAG07-TOLERANCE-FAIL exits 3, records the launch failure, releases the lock, writes no completion marker, and keeps the unaccepted result files untracked"

requirements-completed: []

coverage:
  - id: D1
    description: "Snapshot identity, checkpoint registry, refusing store, monitor-field formulas, launch lock, and the runtime-pair regression"
    requirement: DIAG-07
    verification:
      - kind: unit
        ref: "tests/phase59/test_diag07.py#SnapshotIdentityTests,RegistryTests,RunBookkeepingTests,RefusingStoreTests,MonitorFieldsTests,ModuleProvenanceTests,RuntimePairTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "JX-10 re-score of the generation-7 frozen monitor on MPS float32 and CPU float64"
    requirement: DIAG-07
    verification:
      - kind: other
        ref: ".planning/phases/59-read-only-baseline-scorecard/evidence/diag07/logs/jx10.log"
        status: fail
    human_judgment: true
    rationale: "The run finished with EXIT=3. One of 54 frozen checks failed at the 1e-4 boundary of the rounded packet comparison (stage-0-init.pt, bin 2: 2.0539 against 2.0538, unrounded gap 5.78e-5). How the boundary is evaluated is an owner-routed reading of a frozen tolerance."
  - id: D3
    description: "JX-1 per-term gradients, Adam-preconditioned shares, and Gate G1"
    requirement: DIAG-07
    verification: []
    human_judgment: true
    rationale: "Not started. The tracer gate halts before any expansion task, and Gate G1 has no recorded outcome."

duration: 42min
completed: 2026-10-14
status: halted
---

# Phase 59 Plan 07: Read-Only Checkpoint Experiments Summary

**Gate G1 has no outcome: JX-10 re-scored all eight retained checkpoints on MPS float32 and CPU float64 (seed-42 fronts 0, 1, 2, 2, 2; smoke fronts 0, 0, 0), 53 of 54 frozen checks passed, and the run halted at the tracer gate on one 1e-4 boundary case, so JX-1 was not started**

## In plain language

The owner freed memory, so the run could start. It now reproduces the front positions recorded in Phase 58 on both the GPU (MPS) and the CPU cross-check, and the smoke run's front stays at 0 at steps 100, 200 and 300. One comparison of 54 failed for a reason that is not about the network. The recorded Phase 58 value is 2.0538. This run measures 2.05386, which rounds to 2.0539, one step in the fourth decimal away. Computer arithmetic evaluates the pair 2.0539 and 2.0538 as 0.00010000000000021, which is a hair above the 0.0001 limit. Four other comparisons are also one step apart and passed only because their arithmetic landed a hair below the limit. The plan says a tolerance miss goes to the owner, so the run stopped and nothing was changed after the result was seen. Gate G1 was not computed.

## Performance

- **Duration:** 42 min (27 min in the first session, 15 min in this resume)
- **Started:** 2026-10-14T04:10:27Z; resumed 2026-10-15T02:43:43Z
- **Completed:** 2026-10-15T02:56:07Z (resume record written)
- **Tasks:** 0 of 3 accepted. Task 1's code is committed and unit-tested; its acceptance run is halted. Tasks 2 and 3 were not started.
- **Files modified:** 3 (the same three files as before; `jx01_jx10.py` and the test file changed again)
- **JX-10 run:** 112.6 s wall, MPS then CPU, `ru_maxrss` 3611295744 bytes (3.36 GiB)

## Accomplishments

- The memory halt cleared. After the owner freed memory, `vm_stat` showed 7335460864 available bytes and the frozen 6 GiB preflight (`required_bytes` 6442450944, unchanged) passed at both relaunches.
- The first real execution of the driver found and fixed a CPU-only bug (below). MPS float32 had already run end to end.
- JX-10 measured, with no checkpoint written and no optimizer built:
  - Seed-42 fronts, MPS and CPU alike: `stage-0-init.pt` 0, `best.pt` 1, `step-000931.pt` 2, `step-000941.pt` 2, `step-000951.pt` 2. These equal the Phase 58 packet.
  - Smoke fronts at steps 100, 200 and 300: 0, 0, 0 on both runtimes.
  - Largest unrounded gap between the MPS re-score and any packet value: 6.67e-5 (`step-000941.pt`), against the 1e-4 bound.
  - Largest `raw_rbar_bin0` relative gap: 1.21e-5 (`step-000941.pt`), against 1e-4.
  - All 19 CPU-versus-MPS agreement checks pass (front exact; scaled residual and prefix within 1e-3 relative).
  - Non-interference: parameters bitwise unchanged, every `.grad` None, no optimizer constructed, 0 checkpoint writes, run-file hashes unchanged.
  - Corpus access: 4142 train and 486 validation files opened; test split 0, blocked attempts 0, refused before open 0. The normalizer was recovered from the checkpoint (residual 1.192e-7, no fallback).

## Task Commits

1. **Task 1: JX-10 driver** - `16f5f0db` (test), `12c5420d` (feat), `a0fc5edf` (fix). The acceptance run is halted.
2. **Task 2: JX-1 and Gate G1** - not started.
3. **Task 3: Committed combined run** - not started.

**Plan metadata:** `384c2112` (first halt record, memory preflight) and the commit that carries this summary. `commits: 5` in the frontmatter is the four measured with `git rev-list --count` at write time (RED, GREEN, first halt record, fix) plus the commit carrying this summary.

## Files Created/Modified

- `.planning/phases/59-read-only-baseline-scorecard/evidence/diag07/diag07_common.py` - Snapshot bootstrap, registry load, refusing store, monitor fields, and launch bookkeeping (unchanged in this resume)
- `.planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx01_jx10.py` - JX-10 entry point; the CPU cross-check now builds with the permitted pair. JX-1 is not implemented in this revision.
- `tests/phase59/test_diag07.py` - Task 1 behaviors plus `RuntimePairTests`
- Untracked and not accepted, left in place: `evidence/diag07/{jx10.json, files_opened_jx01_jx10.json, provenance_jx01_jx10.json, summary.md}` from the EXIT=3 run. Its `summary.md` says "falsifies"; do not cite it. The next run overwrites all four. No `*.done.json` marker exists.

## Decisions Made

The boundary case is owner-routed. The plan and the orchestrator both say a frozen-tolerance miss stops the run. Choosing now how "within 1e-4" is evaluated at its boundary, after seeing which comparison it affects, is the post-result choice the pre-registered scorecard exists to prevent (SCOPE-42). So the comparison code, `phase58_packet_rounded_abs` (1e-4), and every other frozen value are exactly as they were.

`optimizer_constructed` in `non_interference` is true when no optimizer object exists, because the verifier treats that flag as a passed check. A reader should take `true` there to mean "the no-optimizer check passed".

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] The CPU float64 cross-check built its controller with a pair that generation 7 refuses**
- **Found during:** Task 1 (acceptance run, attempt 1)
- **Issue:** `_run_jx10` built the CPU controller as `("float32", "cpu")`. Generation 7's `resolve_runtime` permits only `("float32", "mps")` and `("float64", "cpu")`, so the run stopped with `ValueError` (EXIT=1) after the MPS pass finished.
- **Fix:** Build the CPU controller as `("float64", "cpu")`. The existing step in `_load_into` demotes it to float32 for the trainer's own restore checks (the monitor hash is the raw float32 bytes), restores the checkpoint, then promotes to float64. That step ran for the first time in attempt 2 and the CPU fronts matched MPS.
- **Files modified:** `jx01_jx10.py`, `tests/phase59/test_diag07.py`
- **Verification:** The new test failed first on `[('float32', 'mps'), ('float32', 'cpu')] != [('float32', 'mps'), ('float64', 'cpu')]`, then passed. `test_diag07` plus `test_static_guards`: 24 tests OK. The relaunch ran past the CPU build.
- **Commit:** `a0fc5edf`

**2. [Rule 2 - Missing critical] Float64 load promotes after the float32 restore** (first session, `12c5420d`). Now exercised: the CPU pass completed on it. No change.

### Tracer gate

Task 1 is `type="tracer"`, `workflow.human_verify_mode` is the default end-of-phase, and its `<verify>` is automated-only. The acceptance run failed, so the gate halts and expansion to Task 2 does not start.

## Issues Encountered

- **Run history.**
  - First session: launch refused at the preflight, exit 4, 4899373056 bytes available (see `384c2112`).
  - Resume attempt 1, 02:45:44Z: EXIT=1 after 46 s, the CPU pair bug above (`launch-failures.log` run_id `6aa1f644986f4adaa6efefef4c2cb22f`).
  - Resume attempt 2, 02:49:54Z: EXIT=3 after 112.6 s, `DIAG07-TOLERANCE-FAIL: phase58.stage-0-init.pt.rtilde_bins_0_5` (run_id `061eb7a1782e4fdba7b1ae3e3bc18282`). The lock was released and no marker was written. Logs are gitignored; copies and exit statuses are in the session scratchpad.
- **The failing check.** The 4-decimal copies of the MPS re-score are compared with the Phase 58 packet and must lie within 1e-4 absolute. Evaluated in IEEE doubles, five comparisons that are exactly one decimal step apart came out as follows:

| Checkpoint | Quantity | Measured (4 dp) | Packet | Float difference | Passes `<= 1e-4` | Unrounded measured |
|---|---|---|---|---|---|---|
| `best.pt` | bin 2 | 0.6165 | 0.6166 | 9.999999999998899e-05 | yes | 0.61654913 |
| `stage-0-init.pt` | bin 2 | 2.0539 | 2.0538 | 1.0000000000021103e-04 | **no** | 2.05385780 |
| `step-000941.pt` | prefix through front | 1.1816 | 1.1815 | 9.999999999998899e-05 | yes | 1.18155803 |
| `step-000941.pt` | bin 2 | 0.633 | 0.6329 | 9.999999999998899e-05 | yes | 0.63296670 |
| `step-000951.pt` | median over bins | 0.6579 | 0.6578 | 9.999999999998899e-05 | yes | 0.65785024 |

  CPU float64 gives 2.0538364 for the failing quantity, which rounds to the packet's 2.0538. The result of the check turns on how a decimal pair round-trips in binary, not on the network.

## Authentication Gates

None.

## Known Stubs

None.

## Threat Flags

None. No new network endpoint, auth path, or file-access pattern was added.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Blocked on one owner-routed reading. How is the frozen bound `phase58_packet_rounded_abs = 1e-4` evaluated at its boundary? Three options:

- **A (plan-literal; recommended).** The rounded copies are compared in exact decimal units. A difference of one unit in the fourth decimal is within 1e-4, tested on integers (`round(x * 1e4)`), so binary representation never decides. Verdict on the data: all 54 checks pass.
- **B.** Compare the unrounded measured value with the packet value within 1e-4. This avoids rounding twice. Largest gap 6.67e-5, so all 54 checks pass.
- **C.** Treat a one-unit difference as a miss. Applied consistently, five checks fail and the JX-10 reading is "falsifies", though CPU float64 and every unrounded gap sit inside 1e-4. Applied to only the one case that happened to fail, it would be arbitrary.

A and B give the same verdict and neither changes a frozen value. After a ruling: edit the packet comparison in `_compare_packet` (about 10 lines in `jx01_jx10.py`), add a regression test using the observed pair 2.0539 against 2.0538, rerun JX-10 detached (about 2 minutes), run the Task 1 verify chain, then Tasks 2 and 3.

Two plan-level facts for the executor who resumes (no action taken here):

1. `verify_phase59_evidence.py diag07` checks the `producer_sha256` of every result JSON present against the current files. Task 2 edits both driver files, so `jx10.json` from Task 1's development run will fail Task 2's second verify command unless JX-10 is rerun after Task 2's code lands. Run the Task 1 verify before touching the driver files, and after Task 2's GREEN commit run `--experiment jx1` and then `--experiment jx10` before the Task 2 verify chain.
2. The launch lock is free. Do not lower `required_bytes`; the preflight needs about 6 GiB of free, inactive and speculative memory at launch.

## Self-Check: PASSED

Every file and commit named in this summary exists: `16f5f0db`, `12c5420d`, `384c2112`, `a0fc5edf`, and the three driver and test files. `COMMITS_ACTUAL` was 4 at write time. This is a check of the claims only. The plan's acceptance criteria are not met (`status: halted`), `ROADMAP.md` was not checked off, and `REQUIREMENTS.md` still lists DIAG-07 as pending.

---
*Phase: 59-read-only-baseline-scorecard*
*Completed: 2026-10-14*
