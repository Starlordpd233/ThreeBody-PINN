---
phase: 60-single-system-learnability
plan: 08
subsystem: testing
tags: [learnability-harness, frozen-budget-rule, timing-run, adam-cosine, second-cosine, grad-clip, divergence, owner-stop]

requires:
  - phase: 60-single-system-learnability
    provides: "Plan 60-01's data-only arm runner and exclusive record writer, Plan 60-23's closed arm catalog and first_omega_0 routing, Plan 60-02's MPS-safe scorer"
  - phase: 59-read-only-baseline-scorecard
    provides: "the frozen scorecard functions steps_budget, scoring_cadence_ok, budget_outcome, polish_should_stop, better_state and tier_of"
provides:
  - "learnability_run: timing_steps_for, timing_run, budget_from_timing, reading_steps, drive_adam, make_adam, make_cosine, start_second_cosine, make_scheduled_weights, make_clipper, write_owner_stop; run_arm now runs real arms under the frozen budget rule and gains clip_enabled and fixture_timing_steps"
  - "Record fields timing, budget.{rule, frozen_budget_steps, outcome, extended, new_budget_steps, rate_per_step, diverged_at_step, diverged_by}, schedule.cosines, clip.{stage, multiplier, median_floor, enabled, clipped_steps} and wall.adam_seconds; evidence schema phase60-owner-stop/v1"
  - "tests/phase60/test_schedule.py (27 tests) and tests/phase60/test_budget_driver.py (51 tests)"
affects: [60-09, 60-10, 60-11, 60-12, 60-13, 60-14]

actuals:
  tokens: 23382
  tasks: 3
  commits: 5
plan_head_before: f1dcabf55880ff74b19ffeef0d6e3a106b140f63

tech-stack:
  added: []
  patterns:
    - "A pure budget driver (drive_adam) that takes the step, the reading and the extension as callables and branches only on the frozen budget_outcome and on a skipped step"
    - "One Adam step object shared by the timing run and the arm, so the timed configuration cannot drift from the trained one"
    - "A missing runner function fails as an assertion (a _fn lookup), which keeps RED honest without import errors"
    - "A mutation harness that applies one source change, runs the targeted tests, restores the file byte for byte and checks its SHA-256"

key-files:
  created:
    - tests/phase60/test_schedule.py
    - tests/phase60/test_budget_driver.py
  modified:
    - pinn/verification/learnability_run.py

key-decisions:
  - "A fixture arm follows the same driver as a real arm. It names its own small budget, keeps the frozen budget its timing run would have given beside it, and may extend like any arm; the existing fixture runs at 2, 3, 10 and 12 steps all end complete, so Plan 60-01's tests are unchanged"
  - "The fixture timing run defaults to the frozen minimum of 50 steps (a real arm always times 500 or 50 by timing_steps_for), under the keyword fixture_timing_steps that Plan 60-11 already names"
  - "A clipped step is one whose pre-clip total norm is strictly above the clip value that step applied; the count covers the arm's own steps and not the timing run's"
  - "With clipping off, the gradients themselves are checked for finiteness before optimizer.step(), because there is no clip outcome to read"
  - "owner-stop.json blocks a fresh run of the same arm exactly as record.json does, and records whether the arm had extended"

patterns-established:
  - "Authorize first, validate gating next, check the first-result files, and only then read data or time anything"
  - "Record the budget the frozen rule would have given even where a fixture overrides it"

requirements-completed: [INST-05, FEAS-03]

coverage:
  - id: D1
    description: "Each arm's budget is the frozen 3-hour cap over its own timing run (500 steps data-only, 50 with a physics term, every step timed, MPS synchronized, network discarded, arm restarts from its seed-42 initialization), recorded with the timing wall time and step count (D-02, GAP-60-04)"
    requirement: "FEAS-03"
    verification:
      - kind: unit
        ref: "tests/phase60/test_budget_driver.py#FixtureBudgetTracerTests, TimingRunTests, RealArmBudgetTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "The ratified Adam schedule: LR_k from the trainer's OptConfig (k = 0 for every data-only arm, 4 and 6 for the probe Rung-2b arms), betas (0.9, 0.999), eps 1e-8, cosine to zero over exactly B (D-01, D-04, D-05)"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_schedule.py#LearningRateTests, CosineTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "The one extension is a second cosine of length B on the same optimizer: every group's rate reset to its initial rate, the rate trace over [B, 2B) equal to the trace over [0, B) exactly, Adam's moments and step count kept (D-03)"
    requirement: "FEAS-03"
    verification:
      - kind: unit
        ref: "tests/phase60/test_schedule.py#CosineTests, ExtensionRunTests"
        status: pass
    human_judgment: false
  - id: D4
    description: "make_scheduled_weights gives the PHYS-05 warmup min(2000, floor(0.1 B)) with the stage maxima and no re-ramp past B (used by physics arms in Plan 60-11)"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_schedule.py#WarmupTests"
        status: pass
    human_judgment: false
  - id: D5
    description: "Every Adam step of the timing run and the arm is clipped by the trainer's GradClipper at the arm's clip stage and never in the polish; the record holds stage, multiplier, median floor, enabled flag and clipped-step count (GAP-60-03)"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_schedule.py#ClipperTests"
        status: pass
    human_judgment: false
  - id: D6
    description: "Readings at step 0, every floor(0.05 B) steps and B, continuing to 2B after an extension, meeting scoring_cadence_ok; every branch is the frozen budget_outcome (complete, extend once, inconclusive with a rate); the Adam wall passed to the polish is steps plus readings (GAP-60-05)"
    requirement: "FEAS-03"
    verification:
      - kind: unit
        ref: "tests/phase60/test_budget_driver.py#ReadingStepTests, DriverBranchTests"
        status: pass
    human_judgment: false
  - id: D7
    description: "An OwnerRouted from budget_outcome writes owner-stop.json (phase60-owner-stop/v1) and the Adam weights, is re-raised as the same object, writes no record.json, and blocks a second launch (T-60-11)"
    requirement: "FEAS-03"
    verification:
      - kind: unit
        ref: "tests/phase60/test_budget_driver.py#OwnerStopTests"
        status: pass
    human_judgment: false
  - id: D8
    description: "A non-finite loss, clip outcome or (with clipping off) gradient skips optimizer.step(), ends Adam at the last finite state, records diverged_at_step and outcome diverged, never calls budget_outcome or invents a reading, scores the last finite state, and still polishes (GAP-60-06, T-60-07)"
    requirement: "FEAS-03"
    verification:
      - kind: unit
        ref: "tests/phase60/test_schedule.py#StepGuardTests"
        status: pass
      - kind: unit
        ref: "tests/phase60/test_budget_driver.py#DivergenceTests, DivergenceRunTests"
        status: pass
    human_judgment: false
  - id: D9
    description: "Tier edges come only from the frozen tier_of: E exactly 0.1 is Tier 1, a non-finite E is Tier 0, a non-finite eps_H caps at Tier 1 when E <= 0.1 and gives Tier 0 above it; the recorded result tier equals tier_of of the recorded result"
    requirement: "INST-05"
    verification:
      - kind: unit
        ref: "tests/phase60/test_budget_driver.py#TierEdgeTests"
        status: pass
    human_judgment: false
  - id: D10
    description: "Adam weights that are not finite after the driver returns (unreachable by construction) stop the arm with HarnessHalt and write nothing, because the plan is silent on a result for that case and the scorer refuses non-finite networks"
    verification: []
    human_judgment: true
    rationale: "The plan says the polish runs only if the weights are finite but does not say what the arm's result is when they are not; halting without a record is the only choice that invents no number, and the owner or verifier should confirm it"
  - id: D11
    description: "Mechanical definitions chosen where the sources name a field but not its rule: a clipped step is a pre-clip norm strictly above the clip value, and a fixture arm's timing run defaults to the frozen minimum"
    verification: []
    human_judgment: true
    rationale: "Neither the plan, 60-GAPS.md nor 60-RESEARCH.md defines the clipped-step count; the choice cannot change training, only the audit field"

duration: 24min
completed: 2026-10-20
status: complete
---

# Phase 60 Plan 08: Frozen budget rule and ratified schedule Summary

**Real arms now size themselves from their own timing run under the frozen 3-hour cap and run the ratified Adam cosine over exactly that budget, with the one granted extension as a second cosine, the trainer's clipper on every Adam step, divergence ending Adam at the last finite state, and an undeterminable improvement rate written down for the owner and re-raised unhandled.**

## Performance

- **Duration:** about 24 min of execution after context loading
- **Started:** 2026-10-20T09:25:00Z
- **Completed:** 2026-10-20T09:49:35Z
- **Tasks:** 3 (Task 1 tracer, Tasks 2 and 3 test-first)
- **Files:** 1 modified (`pinn/verification/learnability_run.py`), 2 created (`tests/phase60/test_schedule.py`, `tests/phase60/test_budget_driver.py`); 78 new tests

## Accomplishments

- **Timing and budget.** `timing_run` builds a fresh network, optimizer, cosine and clipper of the arm's exact configuration, times every step including the first with MPS synchronized around the clock, and drops everything. `timing_steps_for` gives 500 steps for a data-only arm and 50 for an arm with a physics term, and refuses a count below the frozen minimum. `budget_from_timing` is `steps_budget` at the scorecard's `cap_hours_single_system`, read from the scorecard and never written into the runner. The arm then starts from its own seed-42 initialization (a test compares the step-0 reading with a freshly built network).
- **Budget driver.** `drive_adam` takes the step, the reading and the extension as callables. Its branches are the three values `budget_outcome` can return and a skipped step, and a test reads its source to prove it holds no numeric literal other than 0 and 1. It sums Adam's wall over every step and every reading and hands that to the polish (GAP-60-05). `reading_steps` reads the 5% fraction from the scorecard and meets `scoring_cadence_ok` for B and for 2B.
- **Schedule.** `make_adam`, `make_cosine`, `start_second_cosine`, `make_scheduled_weights` and `make_clipper` are thin wrappers over the trainer's own `OptConfig`, `CosineAnnealingLR`, `ScheduledWeights` and `GradClipper`. The second cosine reproduces the first rate trace exactly (maximum difference 0.0) and keeps the optimizer object, its moment tensors and its step count.
- **Clipping and divergence.** Every Adam step clips at the arm's clip stage when clipping is on and never in the polish. The loss and the clip outcome (or, with clipping off, the gradients) are checked before `optimizer.step()`. A skipped step records `diverged_at_step` and `diverged_by`, calls neither `budget_outcome` nor the scorer for an invented reading, scores the last finite state if no reading covered it, and lets the polish and `better_state` run.
- **Owner path.** The `except OwnerRouted` clause in `run_arm` is the only handler for it, writes `adam.weights` and `owner-stop.json`, and ends in a bare `raise`. A test proves the same exception object comes back, `record.json` is never written, and a second launch is refused before any read, build or step.

## Task Commits

1. **Task 1: Tracer, the frozen budget rule end to end on a fixture arm** - `37a76a90` (feat)
2. **Task 2 RED: failing schedule and clipper tests** - `9b18d8da` (test)
3. **Task 2 GREEN: ratified Adam schedule, second cosine, warmup helper, clipper and step guard** - `c1909e77` (feat)
4. **Task 3 RED: failing owner stop and divergence guard tests** - `ad15d86b` (test)
5. **Task 3 GREEN, the plan-named commit: owner-stop blocking, stop record detail and non-finite-weights guard** - `2c23f4b9` (feat, subject `add the frozen budget rule and schedule to the runner`)

**Plan metadata:** the SUMMARY commit that follows this file (docs).

The plan asks for one commit of Tasks 1 to 3. The tracer gate and the test-first flow for Tasks 2 and 3 need earlier commits, so there are five production commits and the plan-named subject is on the last one. Its body names D-01 to D-05 and GAP-60-03 to GAP-60-06.

The tracer feedback gate ran after `37a76a90`: not auto mode (`_auto_chain_active` false, `workflow.auto_advance` unset), mode `end-of-phase`, verify has only `<automated>`. The verify was re-run on the committed tree (47 tests OK) and expansion continued.

## drive_adam review (acceptance criterion)

`drive_adam` is `pinn/verification/learnability_run.py` lines 378-461. Its control flow is one loop: when the step equals the current horizon it calls `budget_outcome(readings, horizon, extended=..., scorecard=...)` and branches on `"extend"` (take `new_budget_steps` from the result, call `on_extend`, widen the reading plan) or anything else (that is the final outcome, with `rate_per_step` when present); otherwise it takes a step and branches on whether `step_fn` reported a skip. The only literals are the initial `0` and the increments `1`. `FixtureBudgetTracerTests.test_drive_adam_has_no_numeric_literal_but_zero_and_one` walks its AST, and a mutation that adds `0.75 * budget` is caught.

## Files Created/Modified

- `pinn/verification/learnability_run.py` - timing run, budget, reading plan, `drive_adam`, `write_owner_stop`, the schedule and clipper helpers, the shared Adam step, and the reworked `run_arm` (+521 lines, -48)
- `tests/phase60/test_schedule.py` - LR_k, cosine, second cosine, warmup, clipper, step guard, extension in a run, timing parity (27 tests)
- `tests/phase60/test_budget_driver.py` - tracer, timing run, real-arm budget, reading steps, driver branches with fakes, divergence, owner stop, tier edges (51 tests)

## Decisions Made

- **Fixture arms use the same driver.** Plan 60-01's fixture runs end complete at 2, 3, 10 and 12 steps (I applied the frozen `budget_outcome` to their recorded readings on the Plan 60-01 code before changing anything), and the unchanged `test_run_short.py` still passes, so it is untouched. A fixture whose readings keep improving would extend like a real arm; the 20-step fixture readings do give `extend` to 40, which is why the new fixture tests read their expectations from the record and the frozen function instead of fixing an outcome.
- **`fixture_timing_steps` and its default.** The tracer needs a 50-step timing run on a fixture and the plan names no knob. I used `fixture_timing_steps`, the name Plan 60-11 already uses, defaulting to the frozen minimum. Both fixture knobs are refused for a real arm, and a real arm on a fixture context (or the reverse) is refused.
- **Cadence is enforced for real arms only.** A budget below 20 steps cannot meet a 5% gap with whole steps, so `reading_steps` and `drive_adam` take `enforce_cadence` (True by default) and a fixture passes False. This continues Plan 60-01's recorded deviation.
- **Clipped-step count.** A step counts as clipped when its pre-clip total norm is strictly above that step's clip value. The timing run's steps are not counted.
- **Clipping off.** `clip_enabled=False` turns the clipper off in the timing run and the arm. The record still reports the stage and the table's multiplier with `enabled: false` and `clipped_steps: 0`.
- **Owner-stop details.** The stop record also says whether the arm had extended, and its readings are the trace up to the stop.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing critical] Gradient finiteness check when clipping is off**
- **Found during:** Task 2 (GAP-60-06 wiring)
- **Issue:** The plan checks "the loss and the clip outcome" before `optimizer.step()`. A data-only arm may run unclipped (the owner's veto of GAP-60-03), and then there is no clip outcome, so a finite loss with a non-finite gradient would reach Adam and turn the weights to NaN.
- **Fix:** With no clipper, the step checks every gradient for finiteness and returns `non_finite_gradient`. The clipped path is unchanged.
- **Files modified:** `pinn/verification/learnability_run.py`
- **Verification:** `StepGuardTests.test_with_the_clipper_off_a_non_finite_gradient_still_skips_the_step`
- **Committed in:** `c1909e77`

**2. [Rule 3 - Blocking] `fixture_timing_steps` keyword, `enforce_cadence` keyword and a `data` keyword on `timing_run`**
- **Found during:** Task 1
- **Issue:** The tracer test needs a 50-step timing run on a fixture and a fixture cannot meet the 5% cadence below 20 steps; the plan's signatures name neither. Without `data`, the timing run would read the record a second time.
- **Fix:** `run_arm(..., fixture_timing_steps=None)`, `reading_steps(..., enforce_cadence=True)` and `drive_adam(..., enforce_cadence=True)`, and `timing_run(..., data=None, clock=time.monotonic)` (`clip_enabled` defaults to True). Every plan-named export and keyword is present.
- **Files modified:** `pinn/verification/learnability_run.py`
- **Verification:** `FixtureBudgetTracerTests`, `RealArmBudgetTests`, `ReadingStepTests`
- **Committed in:** `37a76a90`

---

**Total deviations:** 2 auto-fixed (1 Rule 2, 1 Rule 3)
**Impact on plan:** Both are additive. No frozen value, threshold or catalog entry changed.

### Plan-coverage items

- **An all-non-finite reference window does not give OwnerRouted.** Task 3's behavior list says a sequence whose reference window is all non-finite gives `OwnerRouted`. Through the frozen `budget_outcome` it does not: with a finite final window the first call returns `extend`, and the reference window of the second call (steps up to 1.5 B) then contains the first budget's final-window readings, so it is finite. The form that is reachable is a reference-window minimum of exactly 0.0 after the extension. Tests cover that form with the real frozen function (once in `DriverBranchTests` and once through `run_arm` with a scorer that reports E = 0.0), cover propagation as the same exception object with a scripted `budget_outcome`, and characterize the NaN case as extend-then-complete.
- **Real-arm record placeholders.** `record.formula` still holds Plan 60-01's fixture placeholder for any `run_kind: real` record, and there is no real-arm command line yet. Counting, the formula comparison, the complete real-record fields and `wall.hours` belong to Plan 60-11; the launcher and resume belong to Plan 60-12.

## TDD Gate Compliance

- **Task 1** is a tracer (not test-first). Its tests landed with its code in `37a76a90`.
- **Task 2:** RED `9b18d8da`, GREEN `c1909e77`. RED run: `python -B -m unittest tests.phase60.test_schedule` exited 1 with `Ran 27 tests`, `FAILED (failures=27)`: 26 tests failed (25 with one failure each and one with two failing sub-tests, which unittest counts as 27 failures) and the catalog characterization test passed by design (the RED commit message `9b18d8da` words this loosely as "27 failures in 27 tests"; these are the exact counts). Every failure was an assertion that a named runner function is missing (`make_adam`, `make_clipper`, `make_scheduled_weights`, `start_second_cosine`). GREEN run: 27 tests, OK.
- **Task 3:** RED `ad15d86b`, GREEN `2c23f4b9`. RED run: 50 tests, 1 failure and 2 errors, for the three behaviors Task 3 adds (the stop record's `extended` field, the second-launch refusal, the non-finite-weights halt). The other 47 already passed because Tasks 1 and 2 delivered the driver and the step guard as the plan's action text assigns them, so they are characterization tests. Each of those was proven by mutation instead (below).
- **Mutation evidence.** 28 single-line source mutations were applied one at a time, each followed by the targeted tests and a byte-for-byte restore checked by SHA-256: 10 for Task 2 (no lr reset, literal rate, no clip call, fixed clip stage, fixed warmup, no loss check, no second cosine, no unread-state score, clip at equality, timing ignoring the veto) and 18 for Tasks 1 and 3 (driver never extends, `on_extend` dropped, skip ignored, reading time left out of the Adam wall, reading plan not widened, `B` left out of the readings, owner-stop handler swallowing, wrong schema string, owner-stop not blocking, no weights guard, off-by-one `diverged_at_step`, `steps_taken` counting the skipped step, physics timed at 500, a literal cadence fraction, a literal in `drive_adam`, the arm reusing the timed network, a changed timing step count, a literal cap). All 28 were caught.
- `gsd_run check tdd-red-evidence` parses Node TAP output and does not apply to Python `unittest` output, so the RED evidence is recorded here from the retained logs.

## Verification Results

Logs are retained outside the repository under the session scratchpad `/private/tmp/claude-501/-Users-<user>-Desktop-3-body-problem--worktrees-trainex/10794de1-0511-4472-97f9-694399233015/scratchpad/`.

| Command | Result |
|---|---|
| `python -B -m unittest tests.phase60.test_budget_driver.FixtureBudgetTracerTests tests.phase60.test_run_short -v` | Ran 47 tests in 10.505 s, OK, exit 0 (`final_cmd1.log`) |
| `python -B -m unittest tests.phase60.test_schedule -v` | Ran 27 tests in 21.673 s, OK, exit 0 (`final_cmd2.log`) |
| `python -B -m unittest discover -s tests/phase60 -t . -v` | Ran 657 tests in 256.231 s, OK (skipped=1, the opt-in `PHASE60_PLATFORM_PROBES` probe), exit 0, 258 s elapsed (`phase60_full_discovery.log`) |
| `python -B -m unittest tests.phase39.test_prohibitions` plus the four named `tests.phase38.test_prohibitions.ProhibitionTests` tests `-v` | Ran 35 tests in 1.677 s, OK, exit 0 (`final_cmd4.log`) |
| `git diff --quiet f1dcabf5 HEAD -- <scorecard module and JSON, pinn/training, network, architecture spec, evaluator, trainer entry, arms, data and losses modules, test_run_short, both prohibition suites>` | exit 0 (unchanged) |

The full discovery ran once, on the three changed files at the digests committed in `2c23f4b9` (verified by `sha256sum -c` after the run), and was not repeated; its elapsed time was 258 s, so it is the one expensive command and its complete output is retained. Commands 1, 2 and 4 each took under 25 s and were run on that same tree. Earlier runs during development were narrower targeted runs.

## Known Stubs

- `record.formula` for a `run_kind: real` record is still the fixture placeholder (`not applicable: fixture record`); Plan 60-11 writes the real formula and counting fields.
- `make_scheduled_weights` has no caller in `run_arm` yet because arms with a physics term are still refused here; Plan 60-11 wires it. It is covered by unit tests.
- There is no real-arm command line or resume yet (Plan 60-12). `.planning/WINDOWS.md` was not appended: these are planned hand-offs to named plans, and the file is outside this plan's owned paths.

## Issues Encountered

None that blocked work. The first draft of two tests compared `id()` values of objects that can be freed and reused, and used a `wraps` mock that cannot return the objects it creates; both were corrected before the RED run. Plan-level discovery takes about 4 minutes, almost all of it in `tests/phase60/test_g2.py`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 60-09 can proceed. Plan 60-11 can call `make_scheduled_weights(B, spec.lr_stage)` and reuse `drive_adam`, `timing_run` and `write_owner_stop`; it should add its own keyword for the fixture slot count and keep `fixture_timing_steps` as defined here.
- Open for the owner or verifier: coverage items D10 and D11 above, and the two GAP-60-05 readings still open from Plan 60-01.
- The footprint and no-concurrent-job conditions for the timing run (T-60-18) are enforced at launch by Plan 60-13 and the execution plans; this plan records the timing fields they will check.

---
*Phase: 60-single-system-learnability*
*Completed: 2026-10-20*

## Self-Check: PASSED

- All three owned files exist (`learnability_run.py`, `test_schedule.py`, `test_budget_driver.py`); commits `37a76a90`, `9b18d8da`, `c1909e77`, `ad15d86b` and `2c23f4b9` exist; `git rev-list --count f1dcabf5..HEAD` is 5 before this file.
- Every task's acceptance criteria were re-run against the committed code (commands 1 and 2 above, the full discovery, and the prohibition suites); all pass.
- `STATE.md`, `ROADMAP.md`, `REQUIREMENTS.md` and `.planning/config.json` were not touched by this plan; `git status --short` for the three owned source paths is empty.
