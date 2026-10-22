---
phase: 60-single-system-learnability
plan: 14
subsystem: verification
tags: [rung-1, supervised-ceiling, gate-g2, evidence, weights, detached-run, owner-waiver, seed-42, mps-float32]

requires:
  - phase: 60-single-system-learnability
    provides: "60-13 sealed run protocol, fail-closed evidence verifier and assigned-record preflight; 60-12 arm runner and detached launcher; 60-03 scope amendment"
  - phase: 59-read-only-baseline-scorecard
    provides: "the frozen scorecard f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b"
provides:
  - "evidence/arms/r1-1632, r1-851 and r1-4658: record.json, adam.weights and polish.weights of the first completed Rung-1 runs (seed 42, MPS float32, first_omega_0 30, trained and scored on hierarchical gold, sealed protocol cited)"
  - "evidence/g2/g2-outcome.json: Gate G2 fired on tiers 0 0 0; sweep system 1632, confirmation system 851, uncovered system 4658"
affects: [60-15 settings sweep on system 1632, later Phase 60 plans that read the G2 outcome, Phase 64 verdict inputs]

protocol_sha256: 93486d240f129bb5947cddb56d2eb18936ac0cbad7ac0bceeb0af0372b850383
g2_outcome_sha256: 3e71568fe6d243f16dc930c7b8d49d028967b625e134cf5ba52d4c48b579c529
g2_fired: true
rung1_tiers: [0, 0, 0]

owner_reply_verbatim:
  memory_waiver: "I'm fine with less memory avaialble than than 6GB expected. I don't know who came up with that number, but I don't think the PINn needs that much RAM and memory to run these tests for. go agead and proceed on the next wave"
  task_2_checkpoint: "start"
  task_4_go_ahead: "go ahead and check it now"

actuals:
  tokens: 15641   # chars/4 over the four text evidence files (62,563 bytes); the six binary weights files (19,151,826 bytes) and this SUMMARY are not counted
  tasks: 4
  commits: 2
  plan_head_before: a686d26e00f7c1e8ba54bb2d3e1cd730a3404a69

tech-stack:
  added: []
  patterns:
    - "Detached long run checked in a later session: the Task 1-3 record is carried in STATE.md and no SUMMARY draft exists until the run ends, because any SUMMARY marks a plan complete in GSD's plan index"
    - "Write-once G2 outcome written only after the records it reads are committed, then re-verified by the independent verifier and by a recomputation of the frozen g2_fires"

key-files:
  created:
    - .planning/phases/60-single-system-learnability/evidence/arms/r1-1632/record.json
    - .planning/phases/60-single-system-learnability/evidence/arms/r1-1632/adam.weights
    - .planning/phases/60-single-system-learnability/evidence/arms/r1-1632/polish.weights
    - .planning/phases/60-single-system-learnability/evidence/arms/r1-851/record.json
    - .planning/phases/60-single-system-learnability/evidence/arms/r1-851/adam.weights
    - .planning/phases/60-single-system-learnability/evidence/arms/r1-851/polish.weights
    - .planning/phases/60-single-system-learnability/evidence/arms/r1-4658/record.json
    - .planning/phases/60-single-system-learnability/evidence/arms/r1-4658/adam.weights
    - .planning/phases/60-single-system-learnability/evidence/arms/r1-4658/polish.weights
    - .planning/phases/60-single-system-learnability/evidence/g2/g2-outcome.json
  modified: []

key-decisions:
  - "Gate G2 fired: all three Rung-1 arms ended at Tier 0, so g2_fires is true (at least two of three below Tier 1). With all three failing, the pinned lap-count rule gives sweep system 1632, confirmation system 851 and uncovered system 4658. The next step is the four-setting sweep (plan 60-15); a G2 fire is a recorded branch, not an owner checkpoint by itself."
  - "The first completed run of each arm is the result: one launch invocation, no pause, stop or resume, seed 42, MPS float32. r1-4658 earned its one budget doubling (980,623 to 1,961,246 steps); r1-1632 and r1-851 did not."
  - "g2-outcome.json was written once, after the three records were committed, in its own commit; the record hashes inside it equal the committed blobs."
  - "The owner waived the 6 GiB free-memory figure for this wave. The arms ran with about 4 GiB advisory free and about 9.9 GB of swap in use, and all three exited 0."
  - "The owner's replies 'start' and 'go ahead and check it now' were taken as the plan's resume signals 'ready' and 'finished'; the sequence status itself (SEQUENCE-COMPLETE) was re-read before anything was verified or committed."

patterns-established:
  - "Sustained-run bookkeeping: each status reading, launch file and owner reply is recorded verbatim in the SUMMARY; the launch files under runs/ stay ignored and are never staged."

requirements-completed: [FEAS-03]

coverage:
  - id: D1
    description: "Rung 1 recorded on systems 1632, 851 and 4658: three record.json files and six weights files committed in plain git and verified fail-closed"
    requirement: "FEAS-03"
    verification:
      - kind: other
        ref: "verify_phase60_evidence.py records --arm r1-1632, --arm r1-851 and --arm r1-4658 each print RECORDS-OK; verify_phase60_evidence.py records prints RECORDS-OK"
        status: pass
    human_judgment: false
  - id: D2
    description: "Gate G2 outcome written once from the committed records and committed: fired on tiers 0 0 0, sweep system 1632, confirmation system 851, uncovered system 4658"
    requirement: "FEAS-03"
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.learnability_g2 outcome prints G2-OUTCOME-WRITTEN; verify_phase60_evidence.py g2 --require outcome prints G2-OK"
        status: pass
    human_judgment: false
  - id: D3
    description: "Run window admitted, owner released the machine (6 GiB figure waived) and the sequence launched detached on the sealed protocol (Tasks 1 to 3)"
    requirement: "FEAS-03"
    verification:
      - kind: other
        ref: "verify_phase60_evidence.py protocol prints PROTOCOL-OK; launch_phase60_arm.py --sequence rung1 --dry-run prints three ADMIT-OK lines; launch_phase60_arm.py --sequence rung1 --status prints SEQUENCE-RUNNING"
        status: pass
    human_judgment: true
    rationale: "The machine being freed and the protocol being reviewed are owner decisions recorded verbatim; no command can confirm them"
  - id: D4
    description: "Reading of the result: three Tier-0 arms mean G2 fired and the settings sweep comes next; whether the failure comes from capacity or from optimization is not decided here"
    verification: []
    human_judgment: true
    rationale: "What three Tier-0 results mean for the project belongs to the owner and the later verdict stage; this plan reports only the pre-registered branch"

duration: 13h 42m   # calendar time; the detached sequence itself took 11h 07m of it
completed: 2026-10-22
status: complete
---

# Phase 60 Plan 14: Rung 1 on the Panel Systems and Gate G2 Summary

**Rung 1 ran to completion on systems 1632, 851 and 4658 under the sealed protocol: all three networks ended at Tier 0 (worst position error 1.14 to 1.24 against the 0.10 Tier-1 line, valid horizon 0.0), so Gate G2 fired on tiers 0 0 0 and the settings sweep on system 1632 is the pre-registered next step.**

In plain language: the network was shown each of three real orbits together with the answer and trained for hours to copy it. It did not manage to copy any of them. At its worst moment the predicted position was off by about 114% to 124%, more than ten times the 10% that Tier 1 allows. The pre-registered rule says that when at least two of the three fail, the next step is a sweep of the first-layer frequency setting on the failing system with the fewest orbital laps. All three failed, so Gate G2 fired. That is a recorded branch of the plan, not an owner checkpoint by itself.

## Performance

- **Duration:** 13h 42m of calendar time from plan start to this SUMMARY. The detached sequence took 11h 07m of it (39,997 s). The Task 4 work in this session took about 15 minutes.
- **Plan started:** 2026-10-22T02:13:55Z (2026-10-21 21:13:55 CDT)
- **Sequence launched:** 2026-10-22T02:29:01Z; **sequence ended:** 2026-10-22T13:35:40Z (08:35:40 CDT)
- **Task 4 session started:** 2026-10-22T15:43:19Z; **completed:** 2026-10-22T15:57Z
- **Tasks:** 4 (Tasks 1 to 3 by earlier executors, Task 4 here)
- **Files committed:** 10 evidence files (9 in the first commit, `g2-outcome.json` in the second) plus this SUMMARY

## Accomplishments

- **Rung 1 is recorded on all three panel systems.** Each arm trained on the hierarchical gold record and was scored on that same gold grid (1,001 times), with the base-grid scores (126 times) beside it, at `first_omega_0 = 30`, seed 42, MPS float32, under the frozen budget rule and polish. All three records name the sealed protocol SHA-256, and the independent verifier printed `RECORDS-OK` for each.
- **Gate G2 is recorded and committed.** `g2-outcome.json` says fired, failing systems 1632, 851 and 4658, sweep system 1632, confirmation system 851, uncovered system 4658. Its `g2_fired` equals the frozen `g2_fires` recomputed on the committed tiers in panel order.
- **The launch discipline held.** One invocation, no pause, no governed stop, no resume, no restart. The first completed run of each arm is the result.

## Run window, owner gates and status readings (Tasks 1 to 3)

No SUMMARY draft existed during the wait (see Deviations); the Task 1 to 3 record was carried in STATE.md (committed in `a686d26e`) and is reproduced here.

**Task 1 (tracer, 2026-10-22T02:14Z = 21:14 CDT, HEAD `768ade36`).** From the project root with `<home>/miniforge3/envs/pinn-train/bin/python -B`, each command took 1 to 3 s and exited 0:

| Time (UTC) | Output |
|---|---|
| 02:14:20Z | `PROTOCOL-OK` |
| 02:14:21Z | `PREFLIGHT-OK` |
| 02:14:22Z | `SCORECARD-FROZEN-OK` |
| 02:14:24Z | `SEQUENCE-NOT-LAUNCHED` |
| 02:14:32Z | `ADMIT-OK r1-1632`, `ADMIT-OK r1-851`, `ADMIT-OK r1-4658` |

No competing jobs were running. The advisory available-memory reading (not a gate) was 3.891 GiB at 21:14:36 CDT and 4.051 GiB at 21:17:55 CDT. At 21:21 CDT the orchestrator measured 9.8 GB of swap in use and 10.5 GiB in the compressor.

**Task 2 (owner checkpoint).** The checkpoint quoted the "In plain language" section of `60-RUN-PROTOCOL.md` verbatim with the protocol SHA-256 `93486d240f129bb5947cddb56d2eb18936ac0cbad7ac0bceeb0af0372b850383`, and stated that GAP-60-03 and GAP-60-09 were settled in Plan 60-13 and are not reopened here. The owner's words, verbatim:

- Waiver of the 6 GiB free-memory figure (2026-10-21, about 21:05 CDT): "I'm fine with less memory avaialble than than 6GB expected. I don't know who came up with that number, but I don't think the PINn needs that much RAM and memory to run these tests for. go agead and proceed on the next wave"
- Reply to the Task 2 checkpoint (about 21:26 CDT): "start" (taken as "ready")
- Memory after the reply: 4.084 GiB advisory free at 21:28:20 CDT and about 9.95 GB of swap in use. Gemini.app spiked to 98.7% CPU at 21:28:20 and was gone by 21:28:53.

The 6 GiB figure was an agent-chosen value from `60-CONTEXT.md` "Claude's Discretion" and is not enforced in code.

**Task 3 (launch).** `LAUNCHED rung1 invocation-1` at 21:29:01 CDT (02:29:01Z). `--status` at 21:29:07 CDT printed `SEQUENCE-RUNNING` and `ARM-PID 2179`, with supervisor pid 2178 and caffeinate pid 2180. The power guard started at 21:29:11 CDT as pid 2553; its log line reads "[2026-10-21 21:29:11] power guard started (pid 2553)". The sealed protocol files were clean in git.

**The wait.** Every status reading, all read-only:

| When | Reading |
|---|---|
| 2026-10-21 21:29:07 CDT | `SEQUENCE-RUNNING`, `ARM-PID 2179` (Task 3) |
| 2026-10-21 23:50:58 CDT | `SEQUENCE-RUNNING`, `ARM-PID 2179` (r1-1632, 2:21:57 elapsed); guard running (pid 2553); on AC power |
| 2026-10-22 08:27:08 CDT | `SEQUENCE-RUNNING`, `ARM-PID 18649` (r1-4658); arms 1 and 2 had ended with exit 0; guard running; on AC power |
| 2026-10-22 10:09:35 CDT | `SEQUENCE-COMPLETE`; guard not running (its log reads "[2026-10-22 08:46:04] nothing is running; the power guard exits"); no learnability_run process left; on AC power |
| 2026-10-22 10:44:26 CDT (15:44:26Z) | `SEQUENCE-COMPLETE` (this session's re-read, the status of record at resume; exit 0, 1 s) |

The guard log holds only its start line and its idle-exit line. There was no pause, governed stop or resume, so there is no governed-resume `LAUNCHED` line to record. The ignored launch files (`runs/.launch/phase60/rung1/invocation-1/`, never staged) say: `exit.json` has `completed_arms` 3, `signal` null, `stopped_arm` null, `stopped_code` null and `wall_clock_secs` 39997.39. `output.log` holds three `ADMIT-OK` lines and, once per arm, the known harmless `UserWarning` from `pinn/verification/learnability_run.py:453` (`float(loss)` on a tensor that requires grad).

**Task 4 resume signal.** After the orchestrator reported `SEQUENCE-COMPLETE` and asked for "finished", the owner replied (2026-10-22, about 10:12 CDT), verbatim: "go ahead and check it now" (taken as "finished").

## Results

Every record shows `run_kind` real, seed 42, runtime float32 on mps, `first_omega_0` 30, loss arm `data_only`, and the sealed protocol SHA-256. Table A is the official result: the better of the two optimizer states by the frozen lexicographic rule, scored on the gold grid. E is the worst position error (relative, so 0.1 is 10%; for all three arms the inner-pair error is the worst one). Tier 1 needs E at most 0.1. eps_H is the largest relative energy drift along the predicted path (Tier 2 needs at most 0.001).

Table A: official result per arm

| Arm | System | Inner laps | Tier | E | eps_H | Valid horizon at 1% / 10% | Better state | Budget trail | Counts | Wall hours |
|---|---|---|---|---|---|---|---|---|---|---|
| r1-1632 | 1632 | 10.47 | 0 | 1.1574 | 705.69 | 0.0 / 0.0 | polish | B = 794,350; complete, not extended (1 cosine) | no (formula 0.9168) | 2.573 |
| r1-851 | 851 | 18.61 | 0 | 1.2375 | 165.5 | 0.0 / 0.0 | adam | B = 980,523; complete, not extended (1 cosine) | no (formula 0.4312) | 2.842 |
| r1-4658 | 4658 | 39.35 | 0 | 1.1432 | 13128 | 0.0 / 0.0 | adam | B = 980,623; still improving, so doubled once to 1,961,246; complete (2 cosines) | no (formula 1.9697) | 5.693 |

Table B: both optimizer states, and the base-grid score beside the gold-grid score

| Arm | Adam, gold grid: tier / E / eps_H | Polish, gold grid: tier / E / eps_H | Base grid beside, better state: tier / E / eps_H | Polish outer calls | CPU float64 cross-check |
|---|---|---|---|---|---|
| r1-1632 | 0 / 1.1606 / 30.295 | 0 / 1.1574 / 705.69 | 0 / 1.1519 / 272.34 (polish) | 6 | agrees on tier and counts, both states |
| r1-851 | 0 / 1.2375 / 165.5 | 0 / 1.2384 / 176.65 | 0 / 1.2340 / 44.266 (adam) | 7 | agrees on tier and counts, both states |
| r1-4658 | 0 / 1.1432 / 13128 | 0 / 1.1439 / 362.02 | 0 / 1.1400 / 4872.6 (adam) | 6 | agrees on tier and counts, both states |

Table C: the runs themselves (launcher times; the record's own wall time is Adam seconds plus polish seconds)

| Arm | PID | Started (UTC) | Ended (UTC) | Exit | Launcher wall (s) | Adam + polish seconds | Timed s/step | Sustained s/step | Clipped steps |
|---|---|---|---|---|---|---|---|---|---|
| r1-1632 | 2179 | 2026-10-22T02:29:02Z | 2026-10-22T05:03:29Z | 0 | 9266.45 | 9244.82 + 4.44 | 0.01360 | 0.01164 | 66 |
| r1-851 | 63958 | 2026-10-22T05:03:29Z | 2026-10-22T07:54:04Z | 0 | 10234.94 | 10215.56 + 4.79 | 0.01101 | 0.01042 | 93 |
| r1-4658 | 18649 | 2026-10-22T07:54:04Z | 2026-10-22T13:35:40Z | 0 | 20495.99 | 20475.93 + 4.50 | 0.01101 | 0.01044 | 85 |

What the tables say, in words:

- All three arms are Tier 0 on the gold grid and on the base grid beside it. The valid horizon is 0.0 at both 1% and 10% on every arm: the rule returns the first scored time at which the error exceeds the threshold, divided by T, so 0.0 means the error was already above both thresholds at the first scored time.
- No arm counts against the two-Kepler formula. Counting needs Tier 1 or better as well as an error strictly below the formula's. For r1-4658 the error (1.1432) is numerically below its formula error (1.9697), yet at Tier 0 it still does not count.
- Polish moved little. It was the better state only for r1-1632 (E 1.1574 against Adam's 1.1606). Each polish ended on the frozen stop "5 outer calls in a row without a lower objective", after 6, 7 and 6 outer calls, in 4.4 to 4.8 seconds.
- The doubling bought nothing for r1-4658: E was 1.14272 at step 980,623 and 1.14319 at step 1,961,246.
- The CPU float64 cross-check agreed with the MPS tier and counts for both states of every arm, so no arm was stopped for the owner. The attestation counters (test split opened, blocked attempts, refused before open) are all 0.
- The attempts at fitting are alike across systems that differ in difficulty: E sits in a narrow 1.14 to 1.24 band although the inner-lap counts are 10.47, 18.61 and 39.35. This is a measured fact only; what it implies is not decided here.

## Gate G2 in plain language

**What G2 asks.** Whether the network can even represent a Stage-0 orbit when it is shown the answer. The rule (frozen in the Phase 59 scorecard) fires when at least two of the three Rung-1 systems end below Tier 1, that is, with a worst position error above 0.1.

**What happened.** The tiers in panel order (1632, 851, 4658) are 0, 0, 0. Three systems are below Tier 1, and the rule needs two, so `g2_fires` is true. The recorded outcome is that value, and a recomputation of the frozen function on the committed tiers gives the same answer.

**What follows, by the pre-registered rule.** With all three failing, the lap-count rule picks the sweep system, the confirmation system and the uncovered system:

- Sweep system 1632 (the failing system with the fewest inner laps, 10.47). Plan 60-15 runs it at `first_omega_0` 60, 120, 240 and 480, all four, in that order, even after a success.
- Confirmation system 851 (the next failing system). The highest setting that reached Tier 1 is confirmed there in one run.
- Uncovered system 4658. Only if the owner continues after a confirmed rescue does it get one data-only Rung 1 at the approved setting.

**What it is not.** A G2 fire is not an owner checkpoint by itself. The owner is asked only at the frozen stops: a confirmed rescue (checkpoint 4), a confirmation that ends below Tier 1 (no pre-answer was given, GAP-60-09), an unreadable assigned record, a CPU cross-check disagreement or an undeterminable improvement rate. If no sweep setting reaches Tier 1 there is no confirmation and no rescue: the ladder stops at G2 with RETHINK-REPRESENTATION, Rung 2 and the probes are recorded as skipped (not failed), and Phases 61 to 63 are marked skipped by G2. One seed per arm is a stated limit of the verdict, not a reason to add seeds.

## Task Commits

1. **Tasks 1 to 3** - no commits by design: Task 1 is read-only, Task 2 is an owner reply, Task 3's launch files stay in the ignored `runs/` tree.
2. **Task 4, records** - `0a135eca` (evidence): `evidence(60-14): record rung 1 on the panel systems`. Nine files: three `record.json`, three `adam.weights`, three `polish.weights`.
3. **Task 4, Gate G2** - `ee739e64` (evidence): `evidence(60-14): record gate g2`. One file: `g2-outcome.json`. It is a separate commit, a stated exception to one atomic commit per task, because its writer reads only committed records.

**Plan metadata:** the `docs(60-14)` commit that adds this file.

## Files Created/Modified

- `evidence/arms/r1-1632/{record.json, adam.weights, polish.weights}` - Rung 1 on the 10th-percentile panel system
- `evidence/arms/r1-851/{record.json, adam.weights, polish.weights}` - Rung 1 on the median panel system
- `evidence/arms/r1-4658/{record.json, adam.weights, polish.weights}` - Rung 1 on the 90th-percentile panel system
- `evidence/g2/g2-outcome.json` - Gate G2's recorded outcome (`phase60-g2-outcome/v1`)

All paths are under `.planning/phases/60-single-system-learnability/`. The six weights files are the first `.weights` files tracked in this repository (about 3.2 MB each, under the 10 MiB blob limit). Nothing under `runs/`, no launch file and no resume checkpoint was staged. `.planning/config.json`, the v2.2 design brief and the other untracked owner files were not touched.

## Decisions Made

- G2 fired on tiers 0 0 0; the sweep, confirmation and uncovered systems are 1632, 851 and 4658 (see Gate G2 above).
- The first completed run of each arm is the result: no restart, no second seed.
- The G2 outcome was written once, in its own commit after the records, so that the outcome reads only committed inputs.
- The 6 GiB waiver and the two reply wordings below were accepted as given.

## Deviations from Plan

### Owner waiver

**1. [Owner waiver] The 6 GiB free-memory figure.**
- **Found during:** Task 2 (and the plan's third truth).
- **Issue:** The plan has the owner confirm at least 6 GiB free before the first arm. The advisory reading was 3.891, 4.051 and 4.084 GiB, with about 9.9 GB of swap in use.
- **Action:** The owner waived the figure in the words quoted above and asked to go on. The protocol was not amended.
- **Outcome:** No stop, no slowdown that shows in the records, three exits of 0. The other mitigations of T-60-09 held: one arm at a time, the advisory reading recorded, no competing job at admission. Whether swap use slowed the runs was not measured.

### Wording of the resume signals

**2. [Resume signal] "start" for "ready", and "go ahead and check it now" for "finished".**
- **Found during:** Task 2 and Task 4.
- **Issue:** The plan names the signals "ready" and "finished"; the owner used other words.
- **Action:** Both were taken as plain go-aheads. For Task 4 the sequence's own status (`SEQUENCE-COMPLETE`) was re-read before anything was verified or committed, so the owner's phrase was not the only evidence that the run had ended.

### Process

**3. [Process] No SUMMARY draft existed during the wait.** Task 4's `read_first` names a SUMMARY draft holding the launch time and ARM-PID. Any `*-SUMMARY.md` marks a plan complete in GSD's plan index, which would have shown 60-14 as done while Rung 1 was running. The Task 1 to 3 record was carried in STATE.md instead (`a686d26e`), and this SUMMARY was built from it.

**4. [Process] The Co-Authored-By trailer names Claude Sonnet 5.5**, the model that did this work, in place of the plan's Opus 5.5, as in earlier waves.

**5. [Process] The generic agent-branch allow-list was not applied.** The executor's pre-commit check that HEAD sits on an `agent-*` branch assumes a per-agent worktree. This plan ran sequentially on the milestone worktree's own branch (`milestone/v2.4`), as every earlier wave did. The checks that do apply passed: HEAD attached, not a protected branch by the GSD query, and no cwd drift from the spawn-time toplevel.

**6. [Process] The plan commit ledger was created late.** Tasks 1 to 3 made no commits, so the ledger `gsd-plan-head-before-60-14` was created just before the first evidence commit and holds `a686d26e`. The orchestrator's `docs(planning)` commit `a686d26e` sits at that point and touches only STATE.md and ROADMAP.md. `commits: 2` counts the two evidence commits, the way 60-13 counted its three task commits and not its SUMMARY.

---

**Total deviations:** 0 auto-fixed under Rules 1 to 4; 1 owner waiver, 1 resume-signal wording, 4 process notes.
**Impact on plan:** None on the results. The run, the records and G2 are what the plan specified.

## Issues Encountered

- One verifier call of mine was aborted before it ran, because an `echo` of a row of equals signs was expanded by zsh as a command lookup. It created no evidence entry. The verifier was re-run cleanly (`RECORDS-OK`, exit 0), and nothing in the records or the commits was affected.
- The body of commit `0a135eca` prints E beside the formula error for r1-4658 without saying that counting also needs Tier 1. The line is accurate; the counting rule is spelled out above.

## Observations

- **Time against the plan.** The plan expected about 3.75 hours per arm (3 hours of Adam plus up to 45 minutes of polish) and 11 to 12 hours in all. Actual wall hours were 2.573, 2.842 and 5.693, 11.11 hours for the sequence. Two reasons: each Adam budget is sized from a 500-step timing run, and the sustained rate came out 14.4%, 5.4% and 5.2% faster than the timed rate, so Adam finished under the 3-hour cap; and each polish stopped after about 4.5 seconds on its five-calls-without-improvement rule instead of running up to 45 minutes. The third arm's 5.69 hours is its single doubling.
- **The 09:00 power-guard pause never triggered.** The third arm ended at 08:35:40 CDT, 25 minutes before it.
- **Code head in the records.** Every record names `git_head` `a686d26e`, while `launch.json` names `768ade36`. The only commit between them changed `STATE.md` and `ROADMAP.md`. Each record's `dirty_pinn_paths` is empty and the verifier's pinned module digests passed.

## Verification Results

Full stdout, stderr, exit codes and timings of the Task 4 commands were retained in a session evidence file outside the repository (its path is in the executor's return).

| Command | Result |
|---|---|
| `launch_phase60_arm.py --sequence rung1 --status` (10:44:26 CDT) | `SEQUENCE-COMPLETE`, exit 0 |
| `verify_phase60_evidence.py records --arm r1-1632` | `RECORDS-OK`, exit 0 |
| `verify_phase60_evidence.py records --arm r1-851` | `RECORDS-OK`, exit 0 |
| `verify_phase60_evidence.py records --arm r1-4658` | `RECORDS-OK`, exit 0 |
| `python -B -m pinn.verification.learnability_g2 outcome` (10:48:46 CDT, run once) | `G2-OUTCOME-WRITTEN: .planning/phases/60-single-system-learnability/evidence/g2/g2-outcome.json (g2_fired true; tiers 0 0 0)`, exit 0 |
| `verify_phase60_evidence.py g2 --require outcome` | `G2-OK`, exit 0 |
| Plan check 1: `records` then `g2 --require outcome` | `RECORDS-OK`, `G2-OK`, exit 0 |
| Plan check 2: tracked-file count | `TRACKED 10`, exit 0 |
| Independent acceptance check (49 checks) | all pass: run_kind real, seed 42, float32 on mps, protocol/scorecard/scorer hashes, gold and base grids, both weights hashes against the files, attestation 0, `g2_fires` recomputed from the frozen scorecard |
| Record hashes inside `g2-outcome.json` against the committed blobs | all three match |
| Files under `runs/` touched by this plan's commits | 0 |

## Fingerprints

- Run protocol SHA-256 (cited by every record): `93486d240f129bb5947cddb56d2eb18936ac0cbad7ac0bceeb0af0372b850383`
- `r1-1632/record.json`: `a87273674785128714f5eae4981dcee31fe4c2332dbd84213b7aeaa0098da0b7`
- `r1-851/record.json`: `3152470de1b34f8e1aa4fe3c0a7f825c32da385eb7636db56a92da50a88baa8a`
- `r1-4658/record.json`: `dbba558ab41b9b1ba080b8346fc4834dcd0987e046d151a4d443a8e5d94f1ab8`
- `g2-outcome.json`: `3e71568fe6d243f16dc930c7b8d49d028967b625e134cf5ba52d4c48b579c529`
- The SHA-256 of each scored state's weights is in its record (`states.adam.weights.sha256` and `states.polish.weights.sha256`) and was checked against the files on disk.

## Threat model check

- T-60-09 (memory): mitigated as far as the owner allowed; the figure was waived (Deviation 1) and the arms ran one at a time.
- T-60-07 (restarts): no restart happened; one invocation, no stops.
- T-60-11 (owner-routed arm results): none occurred; no owner stop was needed.
- T-60-06 (disclosure): `runs/` and launch files were never staged; the verifier's redaction checks passed.

## Known Stubs

None. This plan added no code.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Plan 60-15 (wave 15) is next.** Its Task 1 runs `learnability_g2 branch sweep` and, with `g2_fired` true, should record BRANCH-TAKEN, then admit the four sweep arms on system 1632.
- **Its owner checkpoint repeats the 6 GiB request** and says the sweep takes about 15 hours. The waiver here was given for this wave, so the orchestrator should put the request to the owner again rather than assume the waiver carries over.
- **Use `scripts/phase60-resume.sh` for any resume.** Plans 60-15, 60-16, 60-20 and 60-21 still describe a launcher-direct `--resume` (see the STATE.md note from 60-13).
- **Nothing is running** and the machine is free. Rung 2 and the probes are neither run nor skipped until the G2 branch resolves.

---
*Phase: 60-single-system-learnability*
*Completed: 2026-10-22*

## Self-Check: PASSED

- All ten key files exist on disk (three `record.json`, six `.weights`, `g2-outcome.json`).
- Commits `0a135eca` and `ee739e64` exist, and `git rev-list --count a686d26e..HEAD` was 2 when the frontmatter was written.
- Every Task 4 acceptance criterion was re-run and passed (see Verification Results); the records, the weights hashes and `g2_fires` were checked independently of the writer.
