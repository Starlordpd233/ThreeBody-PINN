---
phase: 59-read-only-baseline-scorecard
plan: 09
subsystem: verification
tags: [diag07, jx-2, jx-3, jx-4, jx-5, generation-7, batch-replay, gap-59-13]

requires:
  - phase: 59-read-only-baseline-scorecard
    provides: The DIAG-07 harness and the committed JX-10, JX-1 and Gate G1 results (59-07), the committed panels (59-05), and the frozen scorecard's diag07 rules
provides:
  - The DIAG-07 driver for JX-5, JX-2, JX-4 and JX-3 (evidence/diag07/jx02_jx05.py), with tests
  - Committed results for all six DIAG-07 experiments and Gate G1, under one manifest that supersedes the Plan-07 version
  - A replay of generation 7's batch random stream, proven against every retained checkpoint's numpy RNG state
affects: [59-10, 60, 61]

actuals:
  tokens: 0  # not measured: the plan ran interleaved with 59-08 in one session
  tasks: 3
  commits: 8
plan_head_before: 0d57e8f9

tech-stack:
  added: []
  patterns:
    - "On MPS, derivatives are taken in reverse mode only: forward mode promotes Python scalars to the float64 default, which MPS cannot hold"
    - "Network scores on MPS go through a CPU-first float64 widening (GAP-59-13), pinned equal to the scorer's own on CPU float64"

key-files:
  created:
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx02_jx05.py
    - tests/phase59/test_diag07_panels.py
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx05.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx02.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx04.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx03.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/files_opened_jx02_jx05.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/provenance_jx02_jx05.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx02_jx05.done.json
  modified:
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/summary.md
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/MANIFEST.json
    - .planning/phases/59-read-only-baseline-scorecard/59-GAPS.md
    - .planning/milestones/v2.4-GAPS.md

key-decisions:
  - "GAP-59-13 (delegation, option A): JX-4 scores through network_score, a copy of the scorer's network_trajectory that moves to the CPU before widening to float64. The shared scorer stays byte-unchanged because the committed Plan-07 results pin its SHA-256. Phase 60 must fix the scorer in place before it scores a network on MPS."
  - "JX-2 checkpoint 951 is step-000951.pt (D-29). The statistic bin is max(frozen front at 900, frozen front at 951) = 2."
  - "JX-4's fixture masses and IC13 come from the resident record, as the plan states; its reference positions come from the gold record."

patterns-established:
  - "When a memory wait blocks the development runs, finish the driver code first, so the development runs exercise the final code and no development result goes stale (compare GAP-59-12)"

requirements-completed: []

coverage:
  - id: D1
    description: "Subset rule, mixed derivative against a central difference, and the skip and SIREN branch split"
    requirement: DIAG-07
    verification:
      - kind: unit
        ref: "tests/phase59/test_diag07_panels.py#SubsetRuleTests,MixedDerivativeTests,SkipBranchTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "Fixture anchor context, the JX-2 and JX-4 reading rules, the physical front and scale, and the MPS-safe network score"
    requirement: DIAG-07
    verification:
      - kind: unit
        ref: "tests/phase59/test_diag07_panels.py#FixtureContextTests,Jx2ReadingTests,Jx4ReadingTests,PhysicalFrontTests,NetworkScoreTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "The batch-stream replay proven on the real generation-7 metadata, the JX-3 groups and the factor-of-two reading"
    requirement: DIAG-07
    verification:
      - kind: unit
        ref: "tests/phase59/test_diag07_panels.py#ReplayProofTests,Jx3GroupTests,Jx3ReadingTests"
        status: pass
    human_judgment: false
  - id: D4
    description: "All six DIAG-07 results and Gate G1 committed, hash-pinned and guarded"
    requirement: DIAG-07
    verification:
      - kind: integration
        ref: "python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py diag07 --require all --require-committed"
        status: pass
    human_judgment: true
    rationale: "The verifier checks hashes, markers, non-interference and commit order. What the readings mean for Phase 61 and the verdict is read in plan 59-10."

duration: 210min
completed: 2026-10-16
status: complete
---

# Phase 59 Plan 09: The Remaining Checkpoint Experiments Summary

**All six DIAG-07 experiments are now recorded on generation 7's saved checkpoints, without training a step. JX-2 reads "estimator noise not excluded". JX-4 reads "relative descent without useful accuracy". JX-3 reads "mixed: exposure-specific / global". JX-5 records that, at initialization, the network's acceleration is about 6,600 times the actual gravitational force.**

## In plain language

These experiments look inside generation 7's saved states to explain its stall.

- **JX-2: was the monitor measuring real progress?** Between steps 900 and 951 the monitor's value moved by 0.155. Redrawing its random sample times 20 times spreads that value by 0.17 at step 900 and 0.14 at step 951. The movement is no larger than the monitor's own noise, so it cannot be called progress. The position of the front, though, came out the same in all 20 redraws.
- **JX-4: did the run's own progress signal come with real accuracy?** No. The run's front advanced from 0 to 2, but on the three panel systems and the monitor's own system the predicted orbits are off by 13 to 62 times the system's size at step 951 (all Tier 0). Measured against each system's real physical force, the front never left 0.
- **JX-3: did the network improve everywhere, or only on what it kept seeing?** The run trained its starting-point and physics terms on 40 different systems, mostly the lowest-numbered few. On the 7 systems it saw most, the starting-point error fell about 200-fold. On 7 systems it never trained on, and on 6 validation systems, it fell only about 3-fold. So that part of the learning was specific to what it saw. The physics residual fell by a similar amount in all three groups (about 2- to 3-fold), so that part was global. The frozen rule reads this as mixed.
- **JX-5: where do the large derivatives come from at the start?** At initialization the network's second derivative (its acceleration) is about 290,000, against a true gravitational force of about 44. The physics residual starts out as almost pure network noise. This is a structural observation only, not a decision input.

The run's batch random stream was replayed and matched every saved checkpoint exactly, so the list of which systems the run trained on is proven, not assumed.

## Performance

- **Duration:** about 3.5 hours, of which about 70 minutes was waiting for free memory
- **Tasks:** 3 of 3
- **Long runs (all detached, one at a time under the launch lock, bar 6442450944 bytes unchanged):**

| Run | Launched (UTC) | Exit | Elapsed | Note |
|---|---|---|---|---|
| JX-5 development | 2026-10-17T03:57:08Z | 0 | 28 s | Task 1 verify: DIAG07-OK |
| JX-2 development | 2026-10-17T03:57:37Z | 0 | 361 s | |
| JX-4 development | 2026-10-17T04:03:39Z | 0 | 77 s | Task 2 verify: DIAG07-OK |
| Committed run, `--experiment all` | 2026-10-17T04:05:58Z | 0 | 576.5 s | `ru_maxrss` 513 MB, preflight 7.09 GB |

- Logs retained at `/private/tmp/claude-501/-Users-<user>-Desktop-3-body-problem--worktrees-trainex/beea9c78-634d-42db-a091-86fa23b14af1/scratchpad/59-09/` (jx05.log, jx02.log, jx04.log, jx02_jx05.log); the in-repo copies are gitignored.
- **Broad test run:** `unittest discover -s tests/phase59 -p 'test_*.py'` at `ce1e6104`, 319 tests OK in 175.4 s.

## Accomplishments

- **JX-5** (`jx05.json` `c74ab3cb`), at `stage-0-init.pt` on anchor 28 over 4,096 rows:
  - RMS sizes: a' 2.90e5, softened force 44.1, residual 2.90e5, v' 352, r' 1.04.
  - IC errors: position 0.82, velocity 211.
  - Mixed-derivative norm on every 16th row: median 2.9e5.
  - In the six skip blocks, the skip branch's du-derivative exceeds the SIREN branch's in every block. It roughly doubles per block: 3.4, 7.9, 18.2, 40.7, 91.4 and 206.5 at hidden layers 1, 3, 5, 7, 9 and 11.
- **JX-2** (`jx02.json` `1853be89`):
  - Frozen fronts 0, 1, 2, 2, 2 at steps 0, 900, 931, 941 and 951; statistic bin 2.
  - The frozen change from 900 to 951 is 0.155. The draw ranges are 0.172 at 900 and 0.141 at 951.
  - All 20 draws give the frozen front at every checkpoint.
- **JX-4** (`jx04.json` `c3baae24`, `panels_sha256` `56ad5185` equal to the committed panels):
  - The monitor front is 0, 1 and 2 at steps 0, 900 and 951. The physical front is 0 at every checkpoint, on every fixture.
  - Fixture E at step 951: anchor 28 61.7, p10 13.5, p50 19.9, p90 29.1. All Tier 0.
- **JX-3** (`jx03.json` `ec529371`):
  - Every replay proof holds: `stage-0-init.pt` after the monitor draw, `best.pt` at 900, 931, 941 and 951, `latest.pt`, and the failure checkpoint after the step-952 draw.
  - The monitor batch begins [28, 90, 104, 147, 167]. There are 40 distinct anchors over 951 steps.
  - Groups: high exposure [0, 1, 3, 9, 5, 8, 11]; never anchored [1772, 2336, 2471, 3088, 3903, 4030, 4209]; validation [216, 295, 414, 889, 2930, 4848].
  - Median ratios of value(951)/value(0): L_IC 0.0052, 0.331 and 0.274; residual sum 0.369, 0.448 and 0.335.
- **Non-interference:** in every result no optimizer was built, there were 0 checkpoint writes, the parameters stayed bitwise unchanged, every `.grad` was None, and the run-file hashes were unchanged. The test split was not opened (4,146 training and 486 validation opens).

## Task Commits

1. **Task 1: JX-5**: `6768db48` (feat)
2. **Task 2: JX-2 and JX-4**: `626c4400` (test, failing first), `6b498021` (feat), `ec2853b0` (plan, GAP-59-13)
3. **Task 3: JX-3 and the area close**: `88b477f4` (test, failing first), `f101c36e` (feat), `ce1e6104` (evidence)

**Plan metadata:** the docs commit that carries this summary.

**Manifest supersession (I-2):** the Plan 59-07 diag07 `MANIFEST.json`, SHA-256 `a2e8d488296af0aecb3c01bd3ca9e8569ae07e717f1ea597b6190d70381311bb`, is superseded by the manifest in `ce1e6104`. The eight Plan-07 files keep their committed SHA-256. Among Plan-07 paths, only `summary.md` and the manifest changed.

## Files Created/Modified

- `evidence/diag07/jx02_jx05.py`: the driver (JX-5, JX-2, JX-4, JX-3, the replay, the reading rules, the MPS-safe network score)
- `tests/phase59/test_diag07_panels.py`: 16 tests
- `evidence/diag07/{jx05, jx02, jx04, jx03}.json`, `files_opened_jx02_jx05.json`, `provenance_jx02_jx05.json`, `jx02_jx05.done.json`: one committed run
- `evidence/diag07/summary.md`, `MANIFEST.json`: regenerated to cover all six experiments
- `59-GAPS.md`, `.planning/milestones/v2.4-GAPS.md`: GAP-59-13

## Decisions Made

See `key-decisions` above.

## Deviations from Plan

### Auto-fixed issues

**1. [Rule 3 - Blocking] The scorer's network_trajectory crashes on MPS (GAP-59-13).**
- **Found during:** Task 2, before any run, by a one-line probe of the scorer's widening call on an MPS tensor.
- **Fix:** `network_score` in the driver, a line-for-line copy of `score_network` that moves to the CPU before widening. `NetworkScoreTests` pins it equal field for field to `score_network` on CPU float64. It is recorded in the gap register under the delegation.
- **Commits:** `6b498021`, `ec2853b0`

**2. [Rule 1 - Bug] Forward-mode derivatives fail on MPS.**
- **Found during:** Task 1, in an MPS smoke of `branch_scales` before any run.
- **Issue:** `jacfwd`, and `jvp` too, promote Python scalars such as `2.0 * u` to float64 duals, which MPS refuses.
- **Fix:** the branch du-derivatives use reverse over reverse. The pullback v -> J^T v is linear in v, so its gradient is J. The tests on CPU float64 pin the derivative against a central difference.
- **Commit:** `6768db48`

### Order of work (not a deviation in substance)

- Free memory stayed below the 6 GiB bar for about 70 minutes. During that wait all three tasks' code was written and committed, so the development runs (Tasks 1 and 2) ran on the final driver, and neither development result went stale. Each task's verify chain then ran exactly as written, on its development run.

**Total deviations:** 2 auto-fixed (1 blocking scorer defect, 1 MPS bug in this plan's own code). No frozen value, tolerance or scorecard byte changed.

## Issues Encountered

- **Memory headroom.** `vm_stat` showed 4.2 to 4.9 GB available, against the 6.44 GB bar plus a 0.5 GB margin, for about 70 minutes, mostly held by browser processes. The bar was not lowered; the runs started when memory freed.
- **The completion marker records the data root as `~/...`.** This matches the committed Plan-07 marker, because `write_completion_marker` redacts the home directory, while result files use `<DATA_ROOT>`.

## Authentication Gates

None.

## Known Stubs

None.

## Threat Flags

None. Every checkpoint, the start RNG state and the step log are SHA-256-checked against `generation-7-retention.json` before use, with `weights_only=True`.

## User Setup Required

None.

## Next Phase Readiness

- Plan 59-10 can read all six DIAG-07 results and Gate G1 (outcome `proceed`, from 59-07). JX-2 to JX-4 are diagnostic readings from single-anchor checkpoints and must not set a recipe value (R-2).
- Phase 60 inherits GAP-59-13's forward item: fix `feasibility_scorer.network_trajectory` in place, with an MPS regression test, before scoring a network on MPS.
- DIAG-07 stays pending in `REQUIREMENTS.md` until Plan 59-10's final check.

## Self-Check: PASSED

Every file and commit named here exists. Before the evidence commit, the Task 3 chain passed: JX-MARKERS-OK, MANIFEST-DIAG07-OK, DIAG07-OK with `--require all`, GUARDRAILS-OK and SCORECARD-FROZEN-OK. After it, `diag07 --require all --require-committed` printed DIAG07-OK and `scorecard-frozen` printed SCORECARD-FROZEN-OK. The area's only markers are `jx01_jx10.done.json` and `jx02_jx05.done.json`.

---
*Phase: 59-read-only-baseline-scorecard*
*Completed: 2026-10-16*
