---
phase: 60-single-system-learnability
plan: 15
subsystem: verification
tags: [gate-g2, settings-sweep, first-omega-0, no-rescue, evidence, weights, detached-run, owner-waiver, seed-42, mps-float32, verifier-fix]

requires:
  - phase: 60-single-system-learnability
    provides: "60-14 Rung 1 records and g2-outcome.json (Gate G2 fired on tiers 0 0 0; sweep system 1632, confirmation system 851); 60-13 sealed run protocol and fail-closed evidence verifier; 60-12 arm runner and detached launcher; the pause, resume and power-guard scripts"
provides:
  - "evidence/arms/g2s-1632-w060, -w120, -w240 and -w480: record.json, adam.weights and polish.weights of the four sweep arms (first_omega_0 60, 120, 240 and 480, omega_provenance g2_sweep_override, seed 42, MPS float32, trained and scored on hierarchical gold, sealed protocol cited)"
  - "evidence/g2/sweep-curve.json: the four-setting curve and the confirmation choice (outcome no_rescue: all four settings below Tier 1, so no confirmation and no rescue)"
  - "verify_phase60_evidence.py g2: the sweep-curve check now runs on a real curve (confirmed_omega called with row mappings and the scorecard), with three regression tests"
affects: [the stop path that follows a no-rescue sweep (this plan's Task 1 text places its records in Plan 60-18), Phase 64 verdict inputs]

protocol_sha256: 93486d240f129bb5947cddb56d2eb18936ac0cbad7ac0bceeb0af0372b850383
g2_outcome_sha256: 3e71568fe6d243f16dc930c7b8d49d028967b625e134cf5ba52d4c48b579c529
sweep_curve_sha256: 946c0bb9a658f287f074c8768c4cd4a54333df9c7303445fd5d64a5a347706bc
sweep_system: 1632
sweep_tiers: [0, 0, 0, 0]
sweep_outcome: no_rescue
confirmed_first_omega_0: null

owner_reply_verbatim:
  memory_waiver_2026_10_21: "I'm fine with less memory avaialble than than 6GB expected. I don't know who came up with that number, but I don't think the PINn needs that much RAM and memory to run these tests for. go agead and proceed on the next wave"
  task_2_checkpoint: "okay let's run that wave 15 now"
  task_4_go_ahead: "should be done now?"

actuals:
  tokens: 19890   # chars/4 over the five text evidence files (77,244 chars) plus the lines added by the verifier fix and its tests (2,317 chars); the eight binary weights files and this SUMMARY are not counted
  tasks: 4
  commits: 3
  plan_head_before: 6873f25a988a3710e549649a1a83982caf3a0d65

tech-stack:
  added: []
  patterns:
    - "Detached long run checked in a later session: the Task 1-3 record is carried in STATE.md and no SUMMARY draft exists until the run ends, because any SUMMARY marks a plan complete in GSD's plan index"
    - "Write-once sweep curve written only after the records it reads are committed, then re-verified by the independent verifier and by a separate recomputation from the committed blobs"
    - "A verifier branch that only runs on a real artifact needs a test that builds that artifact: three tests now build four sweep records and a curve"

key-files:
  created:
    - .planning/phases/60-single-system-learnability/evidence/arms/g2s-1632-w060/record.json
    - .planning/phases/60-single-system-learnability/evidence/arms/g2s-1632-w060/adam.weights
    - .planning/phases/60-single-system-learnability/evidence/arms/g2s-1632-w060/polish.weights
    - .planning/phases/60-single-system-learnability/evidence/arms/g2s-1632-w120/record.json
    - .planning/phases/60-single-system-learnability/evidence/arms/g2s-1632-w120/adam.weights
    - .planning/phases/60-single-system-learnability/evidence/arms/g2s-1632-w120/polish.weights
    - .planning/phases/60-single-system-learnability/evidence/arms/g2s-1632-w240/record.json
    - .planning/phases/60-single-system-learnability/evidence/arms/g2s-1632-w240/adam.weights
    - .planning/phases/60-single-system-learnability/evidence/arms/g2s-1632-w240/polish.weights
    - .planning/phases/60-single-system-learnability/evidence/arms/g2s-1632-w480/record.json
    - .planning/phases/60-single-system-learnability/evidence/arms/g2s-1632-w480/adam.weights
    - .planning/phases/60-single-system-learnability/evidence/arms/g2s-1632-w480/polish.weights
    - .planning/phases/60-single-system-learnability/evidence/g2/sweep-curve.json
  modified:
    - .planning/phases/60-single-system-learnability/evidence/verify_phase60_evidence.py
    - tests/phase60/test_verifier_phase60.py

key-decisions:
  - "No sweep setting reached Tier 1: all four arms ended at Tier 0, so sweep-curve.json records outcome no_rescue with confirmation_arm and confirmed_first_omega_0 null. The single confirmation run on system 851 is not run and there is no rescue. The plan says the stop path follows."
  - "The first completed run of each arm is the result: one launch invocation, no pause, stop or resume, seed 42, MPS float32. No arm earned a budget doubling."
  - "sweep-curve.json was written once, after the four records were committed, and was committed only after the verifier itself printed G2-OK. The writer was not re-run when the verifier first failed."
  - "The verifier's confirmed_omega call was fixed rather than bypassed (Rule 1, authorized by the orchestrator, commit e3841c73), because the verifier is not pinned or sealed and the intended check was unambiguous."
  - "The owner's 2026-10-21 waiver of the 6 GiB free-memory figure was taken to cover this run; the arms ran with about 5.3 GiB advisory free."

patterns-established:
  - "Sustained-run bookkeeping: each status reading, launch file and owner reply is recorded verbatim in the SUMMARY; the launch files under runs/ stay ignored and are never staged."
  - "When an independent verifier fails on a new artifact, first establish whether the data or the instrument is wrong (a separate recomputation and an in-memory patch that touches nothing), then stop and report before editing the instrument."

requirements-completed: [FEAS-03]

coverage:
  - id: D1
    description: "The settings sweep recorded on system 1632 at first_omega_0 60, 120, 240 and 480: four record.json files and eight weights files committed in plain git and verified fail-closed"
    requirement: "FEAS-03"
    verification:
      - kind: other
        ref: "verify_phase60_evidence.py records --arm g2s-1632-w060, -w120, -w240 and -w480 each print RECORDS-OK; verify_phase60_evidence.py records prints RECORDS-OK"
        status: pass
    human_judgment: false
  - id: D2
    description: "The sweep curve written once from the committed records and committed: all four settings below Tier 1, outcome no_rescue, no confirmation and no rescue"
    requirement: "FEAS-03"
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.learnability_g2 sweep-curve prints SWEEP-CURVE-WRITTEN (outcome no_rescue); verify_phase60_evidence.py g2 --require outcome,sweep-curve prints G2-OK"
        status: pass
    human_judgment: false
  - id: D3
    description: "The evidence verifier's sweep-curve check runs on a real curve: confirmed_omega is called with row mappings and the scorecard, with three regression tests"
    verification:
      - kind: unit
        ref: "tests/phase60/test_verifier_phase60.py#G2CheckTests (7 tests, 3 of them new); python -B -m unittest tests.phase60.test_verifier_phase60 tests.phase60.test_g2 (175 tests, OK)"
        status: pass
    human_judgment: false
  - id: D4
    description: "Run window admitted, owner released the machine (6 GiB figure waived) and the sequence launched detached on the sealed protocol (Tasks 1 to 3)"
    requirement: "FEAS-03"
    verification:
      - kind: other
        ref: "learnability_g2 branch sweep prints BRANCH-TAKEN; launch_phase60_arm.py --sequence sweep-1632 --dry-run prints four ADMIT-OK lines; --status prints SEQUENCE-RUNNING"
        status: pass
    human_judgment: true
    rationale: "The machine being freed and the memory waiver are owner decisions recorded verbatim; no command can confirm them"
  - id: D5
    description: "Reading of the result: four Tier-0 settings across a 16-fold range of first_omega_0 (30 to 480) mean no rescue and the stop path follows; whether the failure comes from capacity, optimization or something else is not decided here"
    verification: []
    human_judgment: true
    rationale: "What a flat result across the whole first_omega_0 range means for the project belongs to the owner and the later verdict stage; this plan reports only the pre-registered branch"

duration: 21h 50m   # calendar time; the detached sequence itself took 11h 16m of it
completed: 2026-10-23
status: complete
---

# Phase 60 Plan 15: The Gate G2 Settings Sweep on System 1632 Summary

**The four-setting first-layer-frequency sweep (first_omega_0 60, 120, 240 and 480) on system 1632 ran to completion under the sealed protocol and every setting stayed at Tier 0 (worst position error 1.154 to 1.158 against the 0.10 Tier-1 line, valid horizon 0.0), so the sweep curve records no confirmation and no rescue; the verifier's never-exercised sweep-curve check also had to be fixed (Rule 1) before it could pass the curve.**

In plain language: the network was shown one real orbit (system 1632) together with the answer, as in Rung 1, but at four other values of its first-layer frequency setting (60, 120, 240 and 480, against the locked 30), and trained for hours at each to copy the orbit. None of the four managed it. At its worst moment the prediction was off by about 115% to 116%, more than eleven times the 10% that Tier 1 allows, and no better than the locked setting 30 gave on the same orbit (about 116%). The pre-registered rule would have taken the highest setting that reached Tier 1 and tried it once on a second failing orbit (system 851). No setting reached Tier 1, so that confirmation is not run and there is no rescue. The plan says the stop path follows.

## Performance

- **Duration:** 21h 50m of calendar time from plan start to this SUMMARY. The detached sequence took 11h 16m of it (40,584 s). This session's Task 4 work took about 25 minutes: the checks and the records commit, a stop at step 6, and, after the orchestrator authorized the verifier fix, the fix, the curve commit and this SUMMARY.
- **Plan started:** 2026-10-22T16:59:53Z (11:59:53 CDT, Task 1's first command)
- **Sequence launched:** 2026-10-22T17:01:51Z; **sequence ended:** 2026-10-23T04:18:16Z (2026-10-22 23:18:16 CDT)
- **Task 4 session started:** 2026-10-23T14:27:32Z (09:27:32 CDT); **completed:** about 2026-10-23T14:50Z (09:50 CDT)
- **Tasks:** 4 (Tasks 1 to 3 by earlier executors, Task 4 here)
- **Files committed:** 13 evidence files (12 in the first commit, `sweep-curve.json` in the third), 2 code files in the fix commit, plus this SUMMARY

## Accomplishments

- **The sweep is recorded on all four settings.** Each arm trained on the hierarchical gold record of system 1632 and was scored on that same gold grid (1,001 times), with the base-grid scores (126 times) beside it, at its own `first_omega_0` (60, 120, 240, 480), seed 42, MPS float32, under the frozen budget rule and polish. Every record states its `first_omega_0` and `omega_provenance` `g2_sweep_override`, names the sealed protocol SHA-256, and the independent verifier printed `RECORDS-OK` for each.
- **The sweep curve is recorded and committed.** `sweep-curve.json` says outcome `no_rescue`, `confirmation_arm` null and `confirmed_first_omega_0` null, with every row labelled "below Tier 1". It was written once, from the committed records, and the verifier printed `G2-OK` on it before it was committed.
- **The launch discipline held.** One invocation, no pause, no governed stop, no resume, no restart. The first completed run of each arm is the result.
- **The evidence verifier can now check a real sweep curve.** Its sweep-curve branch had never run on four real records and crashed on this one (see Issues Encountered). It is fixed in its own commit with three regression tests.

## Run window, owner gates and status readings (Tasks 1 to 3)

No SUMMARY draft existed during the wait (see Deviations); the Task 1 to 3 record was carried in STATE.md (committed in `6873f25a`) and is reproduced here.

**Task 1 (tracer, 2026-10-22, HEAD `c9f96a38`, all times CDT).** From the project root with `<home>/miniforge3/envs/pinn-train/bin/python -B`:

| Time (CDT) | Output |
|---|---|
| 11:59:53 | `BRANCH-TAKEN: sweep (g2 fired; sweep system 1632)` |
| 12:00:04 | `SEQUENCE-NOT-LAUNCHED` |
| 12:00:05 | dry run: `ADMIT-OK` for g2s-1632-w060, g2s-1632-w120, g2s-1632-w240 and g2s-1632-w480, in that order |

No competing jobs were running and the Mac was on AC power at 100%. The advisory available-memory reading (not a gate) was 5.345 GiB at 12:00:30 and 5.287 GiB at 12:01:35, with 5.16 GB of 6 GB swap in use. Chrome was open but light (its renderer at about 10% of one core).

**Task 2 (owner checkpoint).** The orchestrator's wave-14 report gave Task 2's presentation (the G2 tiers, the four settings on 1632, the duration and the pause, guard and resume steps) and asked whether the 2026-10-21 6 GiB waiver also covers this run. The owner's words, verbatim:

- The 2026-10-21 waiver of the 6 GiB free-memory figure (about 21:05 CDT): "I'm fine with less memory avaialble than than 6GB expected. I don't know who came up with that number, but I don't think the PINn needs that much RAM and memory to run these tests for. go agead and proceed on the next wave"
- Reply to the wave-14 report and Task 2 (2026-10-22, about 11:52 CDT): "okay let's run that wave 15 now" (taken as "ready", and as carrying the waiver over)

The 6 GiB figure was an agent-chosen value from `60-CONTEXT.md` "Claude's Discretion" and is not enforced in code.

**Task 3 (launch).** `LAUNCHED sweep-1632 invocation-1` at 12:01:51 CDT (17:01:51Z). `--status` at 12:01:57 CDT printed `SEQUENCE-RUNNING` and `ARM-PID 50359`, with supervisor pid 50358 and caffeinate pid 50360. The power guard started at 12:02:10 CDT as pid 50836; its log line reads "[2026-10-22 12:02:10] power guard started (pid 50836)". The sealed protocol files were clean in git, and `launch.json` names git_head `c9f96a38` with a fresh launch. The orchestrator re-checked the supervisor, the arm, caffeinate and the guard from its own shell at 12:04:22 and 12:06:07; all were alive, on AC power.

**The wait.** Every status reading, all read-only:

| When | Reading |
|---|---|
| 2026-10-22 12:01:57 CDT | `SEQUENCE-RUNNING`, `ARM-PID 50359` (Task 3) |
| 2026-10-22 16:23:33 CDT | `SEQUENCE-RUNNING`, `ARM-PID 16896` (g2s-1632-w120); arm 1 had ended with exit 0; guard running (pid 50836); AC power, 100% charged |
| 2026-10-22 19:46:39 CDT | `SEQUENCE-RUNNING`, `ARM-PID 98339` (g2s-1632-w240); arms 1 and 2 had ended with exit 0; guard running; AC power |
| 2026-10-22 21:39:25 CDT | `SEQUENCE-RUNNING`, `ARM-PID 83219` (g2s-1632-w480); arms 1 to 3 had ended with exit 0; guard running; AC power |
| 2026-10-23 09:23:16 CDT | `SEQUENCE-COMPLETE`; guard not running (its log reads "[2026-10-22 23:28:33] nothing is running; the power guard exits"); no learnability_run, launcher or run-control process left; the Mac was on battery by then (100%, discharging) with nothing training |
| 2026-10-23 09:28:15 CDT (14:28:15Z) | `SEQUENCE-COMPLETE` (this session's re-read, the status of record at resume; exit 0, 0.8 s) |

The guard log holds only its start line and its idle-exit line. There was no pause, governed stop or resume, so there is no governed-resume `LAUNCHED` line to record. The ignored launch files (`runs/.launch/phase60/sweep-1632/invocation-1/`, never staged) say: `exit.json` has `completed_arms` 4, `signal` null, `stopped_arm` null, `stopped_code` null and `wall_clock_secs` 40584.39. `output.log` holds four `ADMIT-OK` lines and, once per arm, the known harmless `UserWarning` from `pinn/verification/learnability_run.py:453` (`float(loss)` on a tensor that requires grad).

**Task 4 resume signal.** At 21:39 CDT on 2026-10-22 the orchestrator told the owner: when you're up, ask "done?" or say "finished", and the results will be checked and recorded. The owner replied (2026-10-23, about 09:23 CDT), verbatim: "should be done now?" (taken as "finished"). The sequence status was re-read (`SEQUENCE-COMPLETE`, 09:28:15 CDT) before anything was verified or committed.

## Results

Every record shows `run_kind` real, seed 42, runtime float32 on mps, loss arm `data_only`, system 1632, the keys `hierarchical/gold/1632` (train and score) and `hierarchical/base/1632` (beside), and the sealed protocol SHA-256. Table A is the official result: the better of the two optimizer states by the frozen lexicographic rule, scored on the gold grid. E is the worst position error (relative, so 0.1 is 10%; for all four arms the inner-pair error is the worst one). Tier 1 needs E at most 0.1. eps_H is the largest relative energy drift along the predicted path (Tier 2 needs at most 0.001). For comparison, the locked setting 30 on this system (r1-1632, plan 60-14) ended at tier 0, E 1.1574 (polish), not extended (794,350 steps), 2.573 h.

Table A: official result per arm

| Arm | first_omega_0 | Tier | E | eps_H | Valid horizon at 1% / 10% | Better state | Budget trail | Counts | Wall hours |
|---|---|---|---|---|---|---|---|---|---|
| g2s-1632-w060 | 60 | 0 | 1.1569 | 4052.3 | 0.0 / 0.0 | adam | B = 908,063; complete, not extended (1 cosine) | no (formula 0.9168) | 2.730 |
| g2s-1632-w120 | 120 | 0 | 1.1561 | 1342.9 | 0.0 / 0.0 | adam | B = 955,466; complete, not extended (1 cosine) | no (formula 0.9168) | 2.903 |
| g2s-1632-w240 | 240 | 0 | 1.1539 | 123.62 | 0.0 / 0.0 | adam | B = 994,807; complete, not extended (1 cosine) | no (formula 0.9168) | 3.046 |
| g2s-1632-w480 | 480 | 0 | 1.1575 | 4170.1 | 0.0 / 0.0 | adam | B = 842,770; complete, not extended (1 cosine) | no (formula 0.9168) | 2.591 |

Table B: both optimizer states, and the base-grid score beside the gold-grid score

| Arm | Adam, gold grid: tier / E / eps_H | Polish, gold grid: tier / E / eps_H | Base grid beside, better state: tier / E / eps_H | Polish outer calls | CPU float64 cross-check |
|---|---|---|---|---|---|
| g2s-1632-w060 | 0 / 1.1569 / 4052.3 | 0 / 1.1587 / 293.17 | 0 / 1.1513 / 4052.3 (adam) | 7 | agrees on tier and counts, both states |
| g2s-1632-w120 | 0 / 1.1561 / 1342.9 | 0 / 1.1580 / 2452.9 | 0 / 1.1514 / 541.35 (adam) | 6 | agrees on tier and counts, both states |
| g2s-1632-w240 | 0 / 1.1539 / 123.62 | 0 / 1.1588 / 117.99 | 0 / 1.1524 / 30.166 (adam) | 6 | agrees on tier and counts, both states |
| g2s-1632-w480 | 0 / 1.1575 / 4170.1 | 0 / 1.1576 / 431.61 | 0 / 1.1575 / 794.85 (adam) | 6 | agrees on tier and counts, both states |

Table C: the runs themselves (launcher times; the record's own wall time is Adam seconds plus polish seconds)

| Arm | PID | Started (UTC) | Ended (UTC) | Exit | Launcher wall (s) | Adam + polish seconds | Timed s/step | Sustained s/step | Clipped steps |
|---|---|---|---|---|---|---|---|---|---|
| g2s-1632-w060 | 50359 | 2026-10-22T17:01:51Z | 2026-10-22T19:45:41Z | 0 | 9829.22 | 9808.86 + 4.96 | 0.01189 | 0.01080 | 82 |
| g2s-1632-w120 | 16896 | 2026-10-22T19:45:41Z | 2026-10-22T22:39:56Z | 0 | 10455.28 | 10435.62 + 4.40 | 0.01130 | 0.01092 | 0 |
| g2s-1632-w240 | 98339 | 2026-10-22T22:39:56Z | 2026-10-23T01:42:44Z | 0 | 10967.99 | 10946.28 + 5.44 | 0.01086 | 0.01100 | 0 |
| g2s-1632-w480 | 83219 | 2026-10-23T01:42:44Z | 2026-10-23T04:18:16Z | 0 | 9331.89 | 9311.03 + 4.49 | 0.01282 | 0.01105 | 0 |

What the tables say, in words:

- All four arms are Tier 0 on the gold grid and on the base grid beside it, for both optimizer states. The valid horizon is 0.0 at both 1% and 10% on every arm: the rule returns the first scored time at which the error exceeds the threshold, divided by T, so 0.0 means the error was already above both thresholds at the first scored time.
- No arm counts against the two-Kepler formula. Counting needs Tier 1 or better as well as an error strictly below the formula's, and all four errors (1.154 to 1.158) are above the formula's 0.9168 for this system.
- The setting did not move the error. E sits between 1.1539 and 1.1575 across 60, 120, 240 and 480, a spread of 0.0036, and the locked setting 30 gave 1.1574 on the same system. This is a measured fact only; what it implies is not decided here.
- Energy drift differs by more than a factor of 30 between settings (123.6 at 240, 4170 at 480) but is above the Tier-2 line (0.001) by five orders of magnitude or more in every arm.
- Adam was the better state on all four arms (at the locked setting 30, polish was the better state). Polish moved little: its E was within 0.005 of Adam's on every arm. Each polish ended on the frozen stop "5 outer calls in a row without a lower objective", after 7, 6, 6 and 6 outer calls, in 4.4 to 5.4 seconds.
- The CPU float64 cross-check agreed with the MPS tier and counts for both states of every arm, so no arm was stopped for the owner. The attestation counters (test split opened, blocked attempts, refused before open) are all 0.
- The median clip bound on 82 Adam steps in the first arm and on none in the other three. No arm diverged and none earned a budget doubling.

## The sweep in plain language

**What the sweep asks.** Whether one locked setting, rather than the network's design, is the bottleneck. When Gate G2 fires, the rule tries four fixed values of the first-layer frequency on one failing orbit and counts a setting only if its arm reaches Tier 1 (worst position error at most 0.1).

**What happened.** The tiers in grid order (60, 120, 240, 480) are 0, 0, 0, 0. No setting reached Tier 1, so there is no highest Tier-1 setting to confirm. `sweep-curve.json` records outcome `no_rescue`, `confirmation_arm` null and `confirmed_first_omega_0` null, and labels all four rows "below Tier 1". None of the settings is therefore "reached Tier 1, not confirmed (one-confirmation budget)": that label applies only to a setting that reached Tier 1 and lost the confirmation slot to a higher one.

**What follows, by the plan and the roadmap.** The plan says that when no setting reached Tier 1 there is no confirmation and no rescue, and that the stop path follows; its Task 1 text places the stop path's records in Plan 60-18. The ROADMAP says Gate G2 can end the training phases with RETHINK-REPRESENTATION, but only after a settings sweep finds no rescue. This SUMMARY does not describe that plan's content. GAP-60-09 (a confirmation that ends below Tier 1) does not arise, because no confirmation was run; no owner stop occurred in this plan. One seed per arm is a stated limit of the verdict, not a reason to add seeds.

## Task Commits

1. **Tasks 1 to 3** - no commits by design: Task 1 is read-only, Task 2 is an owner reply, Task 3's launch files stay in the ignored `runs/` tree.
2. **Task 4, records** - `003009a3` (evidence): `evidence(60-15): record the four sweep arms`. Twelve files: four `record.json`, four `adam.weights`, four `polish.weights`.
3. **Task 4, verifier fix** - `e3841c73` (fix): `fix(60-15): call confirmed_omega with row mappings and the scorecard`. Two files: the verifier and its test file. A Rule 1 deviation, authorized by the orchestrator (see Deviations).
4. **Task 4, sweep curve** - `e091916a` (evidence): `evidence(60-15): record the g2 sweep curve`. One file, `sweep-curve.json`. It is a separate commit, a stated exception to one atomic commit per task, because its writer reads only committed records.

**Plan metadata:** the `docs(60-15)` commit that adds this file.

## Files Created/Modified

- `evidence/arms/g2s-1632-w060/{record.json, adam.weights, polish.weights}` - first_omega_0 60
- `evidence/arms/g2s-1632-w120/{record.json, adam.weights, polish.weights}` - first_omega_0 120
- `evidence/arms/g2s-1632-w240/{record.json, adam.weights, polish.weights}` - first_omega_0 240
- `evidence/arms/g2s-1632-w480/{record.json, adam.weights, polish.weights}` - first_omega_0 480
- `evidence/g2/sweep-curve.json` - the sweep curve and the confirmation choice (`phase60-sweep-curve/v1`)
- `evidence/verify_phase60_evidence.py` (modified) - the sweep-curve block of `cmd_g2`: three lines in place of one
- `tests/phase60/test_verifier_phase60.py` (modified) - a helper and three tests in `G2CheckTests` (38 added lines)

All evidence paths are under `.planning/phases/60-single-system-learnability/`. The eight sweep weights files are tracked in plain git (about 3.2 MB each, under the 10 MiB blob limit). Nothing under `runs/`, no launch file and no resume checkpoint was staged. `.planning/config.json`, the v2.2 design brief and the other untracked owner files were not touched. No pinned module and no protocol file was edited.

## Decisions Made

- No sweep setting reached Tier 1; the curve records `no_rescue` (see "The sweep in plain language").
- The first completed run of each arm is the result: no restart, no second seed.
- The curve was written once, in its own commit after the records, and was committed only after the verifier itself printed `G2-OK`.
- The verifier defect was fixed at the orchestrator's direction rather than bypassed (Deviation 3).
- The 6 GiB waiver and the two reply wordings below were accepted as given.

## Deviations from Plan

### Owner waiver

**1. [Owner waiver] The 6 GiB free-memory figure.**
- **Found during:** Task 2 (and the plan's third truth).
- **Issue:** The plan has the owner confirm at least 6 GiB free before the first arm. The advisory readings were 5.345 and 5.287 GiB, with 5.16 GB of 6 GB swap in use.
- **Action:** The owner's 2026-10-21 waiver (quoted above) was put to the owner again for this run, and "okay let's run that wave 15 now" was taken as carrying it over. The protocol was not amended.
- **Outcome:** No stop, and no slowdown that shows in the records; four exits of 0. The other mitigations of T-60-09 held: one arm at a time, the advisory reading recorded, no competing job at admission. Whether swap use slowed the runs was not measured.

### Wording of the resume signals

**2. [Resume signal] "okay let's run that wave 15 now" for "ready", and "should be done now?" for "finished".**
- **Found during:** Task 2 and Task 4.
- **Issue:** The plan names the signals "ready" and "finished"; the owner used other words, and the first reply also answered the waiver question.
- **Action:** Both were taken as plain go-aheads. For Task 4 the sequence's own status (`SEQUENCE-COMPLETE`) was re-read before anything was verified or committed, so the owner's phrase was not the only evidence that the run had ended.

### Rule 1 fix, outside the plan's files

**3. [Rule 1 - Bug] The evidence verifier's sweep-curve check could not run on a real curve.**
- **Found during:** Task 4, step 6 (`verify_phase60_evidence.py g2 --require outcome,sweep-curve`).
- **Issue:** `cmd_g2` called `confirmed_omega(curve_points)` with a list of `(omega, tier)` tuples and no scorecard. The pinned function takes rows that are mappings holding `first_omega_0` and `tier`, and a keyword-only `scorecard`. The first defect crashed the check (`confirmed_omega() missing 1 required keyword-only argument: 'scorecard'`, exit 1, no `G2-OK`); the second would have raised a `ValueError` once the first was fixed. The branch runs only when all four sweep records are committed, and no test had built four.
- **Fix:** In the sweep-curve block only: load the scorecard with `load_scorecard()`, as the file does elsewhere, build rows of `first_omega_0` and `tier`, and call `confirmed_omega(rows, scorecard=card)`, mirroring `learnability_g2._build_sweep_curve`. The hard-coded grid and every other check are unchanged, and no check was added. Three regression tests were added to `G2CheckTests`: tiers 0 0 0 0 with `confirmed_first_omega_0` null gives `G2-OK`; the same tiers with 240.0 fails with "confirmed_first_omega_0 mismatch" (negative control); tiers 0 1 1 0 with 240.0 gives `G2-OK`.
- **Authorization:** This was outside the plan's `files_modified` list and outside the six owned paths I had been given, so my first return stopped at step 6 with nothing further committed. The orchestrator checked the diagnosis, confirmed that the verifier is not one of the 33 pinned modules and is not sealed by the protocol, and authorized the fix as a Rule 1 correction in its own commit.
- **Files modified:** `.planning/phases/60-single-system-learnability/evidence/verify_phase60_evidence.py`, `tests/phase60/test_verifier_phase60.py`
- **Verification:** Red then green. Before the fix `G2CheckTests` ran 7 tests, 4 passing and the 3 new ones failing with the TypeError text (0.611 s). After it all 7 pass (0.606 s). `tests.phase60.test_verifier_phase60` with `tests.phase60.test_g2` ran 175 tests (29 and 146) in 61.5 s, all OK. `verify_phase60_evidence.py protocol` printed `PROTOCOL-OK` and `git diff --check` was clean. On the real tree the fixed verifier then printed `G2-OK`.
- **Committed in:** `e3841c73`

### Process

**4. [Process] No SUMMARY draft existed during the wait.** Task 4's `read_first` names a SUMMARY draft holding the launch line and ARM-PID. Any `*-SUMMARY.md` marks a plan complete in GSD's plan index, which would have shown 60-15 as done while the sweep was running. The Task 1 to 3 record was carried in STATE.md instead (`6873f25a`), and this SUMMARY was built from it.

**5. [Process] Task 2's presentation came before Task 1.** The wave-14 report put the question to the owner before Task 1 had taken the advisory memory reading, so the presentation could not quote it. The reading (5.3 GiB) was recorded afterwards.

**6. [Process] The pause, resume and guard scripts replaced the plan's hand steps** (`c9f96a38`, mirroring `768ade36` in 60-14). No pause was needed.

**7. [Process] The Co-Authored-By trailer names Claude Sonnet 5.5**, the model that did this work, in place of the plan's Opus 5.5, as in earlier waves.

**8. [Process] The generic agent-branch allow-list was not applied.** The executor's pre-commit check that HEAD sits on an `agent-*` branch assumes a per-agent worktree. This plan ran sequentially on the milestone worktree's own branch (`milestone/v2.4`), as every earlier wave did. The checks that do apply passed: HEAD attached, not a protected branch by the GSD query, and no cwd drift from the spawn-time toplevel.

**9. [Process] The plan commit ledger was created late, and Task 4 made three commits, not two.** Tasks 1 to 3 made no commits, so the ledger `gsd-plan-head-before-60-15` was created just before the first evidence commit and holds `6873f25a`, a `docs(planning)` commit that touches only STATE.md. `commits: 3` counts the two evidence commits and the fix commit, and not this SUMMARY. The plan states two commits for Task 4 (records and curve); the third is Deviation 3.

---

**Total deviations:** 1 auto-fixed under Rule 1 (orchestrator-authorized, outside the plan's files); 1 owner waiver, 1 resume-signal wording, 6 process notes.
**Impact on plan:** None on the results. The run, the records and the curve are what the plan specified. The fix changed no recorded number: it let the plan's own verification run on the curve.

## Issues Encountered

- **The verifier crashed on the first real sweep curve (2026-10-23 09:31:49 CDT).** `verify_phase60_evidence.py g2 --require outcome,sweep-curve` exited 1 and printed only `confirmed_omega() missing 1 required keyword-only argument: 'scorecard'`, with no `G2-OK`. The curve had just been written by the write-once writer (`SWEEP-CURVE-WRITTEN ... (outcome no_rescue)`), so before touching anything I checked whether the data or the instrument was wrong:
  - **Independent cross-check (`CROSSCHECK-OK`).** A scratchpad script, run with `python -I`, confirmed that the curve cites the committed `g2-outcome.json` by SHA-256; that each row's `record_sha256` equals the SHA-256 of that record's blob at HEAD; that each row's tier, E, eps_H, valid horizons and `first_omega_0` equal the record's; and that the confirmed setting recomputes to none. It printed `CROSSCHECK-OK`.
  - **In-memory diagnostic.** A second scratchpad script ran the unchanged verifier with only the one bad call replaced in memory (correct keyword, mapping rows). It printed `G2-OK` and wrote nothing to the repository (the working tree showed only the owner's two modifications). This was a diagnostic and not a pass.
  - **Stop, then fix.** I stopped at step 6 and returned to the orchestrator without committing the curve or writing this SUMMARY. The curve, being write-once, stayed in the working tree uncommitted, with SHA-256 `946c0bb9...06bc` before and after. After the orchestrator authorized the fix, it was made in `e3841c73`, and the curve was committed only after the fixed verifier printed `G2-OK`.
  - **Related check.** The verifier's other calls into pinned functions (`g2_fires`, `sweep_plan`, `counts`, `decision_verdict`) were compared with their signatures and match.
- **Two slips of mine, neither touching the evidence.** A `grep` with `--include=*.py` was expanded by zsh and refused to run ("no matches found"); I re-ran it with `git grep`. A tracked-path count that printed 13 was wrong, because I had piped my own logging helper's header line into `wc -l`; a plain recount printed 12, and 13 only after the curve was committed.

## Observations

- **Time against the plan.** The plan expected about 3.75 hours per arm (3 hours of Adam plus up to 45 minutes of polish) and about 15 hours in all (up to about 30 if every arm earned its doubling). Actual wall hours were 2.730, 2.903, 3.046 and 2.591, 11.27 hours for the sequence, and no arm doubled. Two reasons: each Adam budget is sized from a 500-step timing run, and the sustained rate came out 9.2% faster, 3.4% faster, 1.4% slower and 13.8% faster than the timed rate; and each polish stopped after 4.4 to 5.4 seconds on its five-calls-without-improvement rule instead of running up to 45 minutes.
- **One arm ran slightly over the 3-hour sizing target.** The Adam phase of g2s-1632-w240 took 10,946 s (3.04 h), 1.4% over 3 hours, because its sustained rate was 1.4% slower than its timing run. The budget rule sizes the step count from the timing run and does not enforce wall time, so this is not a breach of the rule.
- **Code head in the records.** Every record names `git_head` `6873f25a`, while `launch.json` names `c9f96a38`. The only commit between them changed `STATE.md` (the record of the launch). Each record's `dirty_pinn_paths` is empty and the verifier's pinned module digests passed. Rung 1 showed the same pattern (records `a686d26e`, launch `768ade36`).
- **The 09:00 power-guard pause never triggered.** The sequence ran from 12:01 to 23:18 CDT, and the guard exited on its own at 23:28:33.

## Verification Results

Full stdout, stderr, exit codes and timings of the Task 4 commands were retained in a session evidence file outside the repository (its path is in the executor's return).

| Command | Result |
|---|---|
| `launch_phase60_arm.py --sequence sweep-1632 --status` (09:28:15 CDT) | `SEQUENCE-COMPLETE`, exit 0 |
| `verify_phase60_evidence.py records --arm g2s-1632-w060` | `RECORDS-OK`, exit 0 |
| `verify_phase60_evidence.py records --arm g2s-1632-w120` | `RECORDS-OK`, exit 0 |
| `verify_phase60_evidence.py records --arm g2s-1632-w240` | `RECORDS-OK`, exit 0 |
| `verify_phase60_evidence.py records --arm g2s-1632-w480` | `RECORDS-OK`, exit 0 |
| Acceptance script: `first_omega_0` exactly 60, 120, 240, 480; `omega_provenance` `g2_sweep_override`; path, rung, run kind, seed, runtime, loss arm, system, gold and base keys, protocol and scorecard hashes, attestation 0, one invocation with no stops, no dirty pinn paths | all pass, on the records and again on the committed blobs |
| `python -B -m pinn.verification.learnability_g2 sweep-curve` (09:31:24 CDT, run once) | `SWEEP-CURVE-WRITTEN: .planning/phases/60-single-system-learnability/evidence/g2/sweep-curve.json (outcome no_rescue)`, exit 0 |
| `verify_phase60_evidence.py g2 --require outcome,sweep-curve` on the unfixed verifier (09:31:49 CDT) | exit 1, no `G2-OK`; stderr `confirmed_omega() missing 1 required keyword-only argument: 'scorecard'` |
| Independent cross-check of the curve against the committed blobs | `CROSSCHECK-OK` |
| `G2CheckTests` before the fix (3 new tests) | 7 tests, 3 failures, all with the TypeError text (0.611 s) |
| `G2CheckTests` after the fix | 7 tests, OK (0.606 s) |
| `python -B -m unittest tests.phase60.test_verifier_phase60 tests.phase60.test_g2 -v` | `Ran 175 tests in 61.547s`, `OK` (29 in the verifier module, 146 in test_g2) |
| `verify_phase60_evidence.py protocol`; `git diff --check` | `PROTOCOL-OK`; clean |
| Curve file hash before the curve commit | `946c0bb9a658f287f074c8768c4cd4a54333df9c7303445fd5d64a5a347706bc`, unchanged since the writer |
| `verify_phase60_evidence.py g2 --require outcome,sweep-curve` on the fixed verifier (09:44:17 CDT) | `G2-OK`, exit 0 |
| Plan check: `records` then `g2 --require outcome,sweep-curve` (09:44:49 CDT, and again at the final state) | `RECORDS-OK`, `G2-OK`, exit 0 |
| Tracked-file count of the four directories plus `sweep-curve.json` | 13 |
| Files under `runs/`, `.planning/config.json`, the v2.2 brief, STATE.md, ROADMAP.md or REQUIREMENTS.md touched by this plan's commits | 0 |

## Fingerprints

- Run protocol SHA-256 (cited by every record): `93486d240f129bb5947cddb56d2eb18936ac0cbad7ac0bceeb0af0372b850383`
- `g2s-1632-w060/record.json`: `cf1bc1fac780c21e26c917f4573c4845ccd36ed88136e23658f5a0eb5c960c42`
- `g2s-1632-w120/record.json`: `893cbcefbda4c8cb061071c6d12044620112750644d68987a3b57d55ea245900`
- `g2s-1632-w240/record.json`: `391e3f1728b3de287849ca4a7e48ae17da92e8ca48c8f77562caf377d56e4ca1`
- `g2s-1632-w480/record.json`: `b75905c954728001c27a4f9c649281feb7f404358d88a2cdd58822d94909639e`
- `g2-outcome.json`: `3e71568fe6d243f16dc930c7b8d49d028967b625e134cf5ba52d4c48b579c529`
- `sweep-curve.json`: `946c0bb9a658f287f074c8768c4cd4a54333df9c7303445fd5d64a5a347706bc`
- The SHA-256 of each scored state's weights is in its record (`states.adam.weights.sha256` and `states.polish.weights.sha256`) and was checked against the files on disk.

## Threat model check

- T-60-16 (branch selection): mitigated. `learnability_g2 branch sweep` printed `BRANCH-TAKEN` first, and admission accepted only the four `g2s-1632` arms.
- T-60-09 (memory): mitigated as far as the owner allowed; the figure was waived (Deviation 1) and the arms ran one at a time.
- T-60-07 (restarts): no restart happened; one invocation, no stops.
- T-60-SC (package installs): none; this plan installed nothing.

## Known Stubs

None. The fix and its tests are real code, and the evidence files are data.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **The committed curve and the plan say the stop path follows.** `sweep-curve.json` records `no_rescue`; the plan's words are "no confirmation and no rescue (the stop path follows)", and its Task 1 text places the stop path's records in Plan 60-18. This SUMMARY does not describe that plan's content.
- **Nothing is running** and the machine is free.
- STATE.md, ROADMAP.md and REQUIREMENTS.md are not touched here; the orchestrator updates them by hand.

---
*Phase: 60-single-system-learnability*
*Completed: 2026-10-23*

## Self-Check: PASSED

- All 15 key files exist on disk (twelve sweep files, `sweep-curve.json`, the verifier and its test file).
- Commits `003009a3`, `e3841c73` and `e091916a` exist, and `git rev-list --count 6873f25a..HEAD` was 3 when the frontmatter was written (this SUMMARY's own commit is not counted).
- Every Task 4 acceptance criterion was re-run on the committed blobs and passed; the plan-level verification re-run at the final state printed `RECORDS-OK` and `G2-OK`, and the protocol check printed `PROTOCOL-OK`.
- A path audit of everything committed since `6873f25a` found 15 paths and none under `runs/`, none of `.planning/config.json`, the v2.2 brief, STATE.md, ROADMAP.md or REQUIREMENTS.md; the lines added to the verifier and its tests hold no stub patterns.
