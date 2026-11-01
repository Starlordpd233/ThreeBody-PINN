---
phase: 66-small-network-control
plan: 04
subsystem: pinn-verification
tags: [exp01, ac-power-gate, detached-launch, repeat-runs, evidence-order, check-run, score-blind]
requires:
  - phase: 66-small-network-control (plan 03)
    provides: "measured rate 0.004238129693630617 s/step, budget N=465000 stride=47 cap=3300.0, three admitting registrations (main-1632-s42, repeat-851-s42, repeat-1632-s41) at 3f4d0a85"
provides:
  - "the three verified EXP-01 run records under evidence/exp01/ (record, diagnostic.weights, attempt, power-gate each), every run completing 465,000 steps under its 3,300 s cap through the AC gate, each VERIFY-RESULT-OK and EXP01-CHECK-OK, all three check-run-clean with no score ever read (branch reading is plan 66-05's)"
affects: [66-05]
actuals:
  tokens: 2950
  tasks: 3
  commits: 4
tech-stack:
  added: []
  patterns:
    - "score-blind run execution: verify-result plus check-run only (never read-run) so no E, tier, branch or similarity value is seen before all three runs exist (D-07); the value-free problem lists are the whole verification surface"
    - "detached gated runs at 41-minute scale: wrapper-launched (start_new_session), AC-power receipt precedes the attempt, supervised cap never needed (largest wall 2034 s of 3300 s)"
key-files:
  created:
    - .planning/phases/66-small-network-control/evidence/exp01/main-1632-s42/record.json
    - .planning/phases/66-small-network-control/evidence/exp01/main-1632-s42/diagnostic.weights
    - .planning/phases/66-small-network-control/evidence/exp01/main-1632-s42/attempt.json
    - .planning/phases/66-small-network-control/evidence/exp01/main-1632-s42/power-gate.json
    - .planning/phases/66-small-network-control/evidence/exp01/repeat-851-s42/record.json
    - .planning/phases/66-small-network-control/evidence/exp01/repeat-851-s42/diagnostic.weights
    - .planning/phases/66-small-network-control/evidence/exp01/repeat-851-s42/attempt.json
    - .planning/phases/66-small-network-control/evidence/exp01/repeat-851-s42/power-gate.json
    - .planning/phases/66-small-network-control/evidence/exp01/repeat-1632-s41/record.json
    - .planning/phases/66-small-network-control/evidence/exp01/repeat-1632-s41/diagnostic.weights
    - .planning/phases/66-small-network-control/evidence/exp01/repeat-1632-s41/attempt.json
    - .planning/phases/66-small-network-control/evidence/exp01/repeat-1632-s41/power-gate.json
  modified: []
key-decisions:
  - "None - followed the plan as specified: three launches in the pre-registered order through the AC gate, identical budget, single verification pass per run, no score read anywhere in this plan"
patterns-established: []
requirements-completed: [EXP-01]
coverage:
  - id: D1
    description: "The main EXP-01 run on system 1632 seed 42 ran once, detached, through the AC-power weekend gate, completed its registered 465,000 steps under the 3,300 s cap, and its evidence is committed and verified"
    requirement: EXP-01
    verification:
      - kind: integration
        ref: "diagnostic_power launch (POWER-OK, FIT-RUN-COMPLETE completed_steps=465000, LAUNCH-EXIT=0); verify-result VERIFY-RESULT-OK; check-run EXP01-CHECK-OK with empty problem lists"
        status: pass
    human_judgment: false
  - id: D2
    description: "The repeat on system 851 seed 42 ran under the same rule and order, whichever branch the main run landed in (D-07), and is committed and verified"
    requirement: EXP-01
    verification:
      - kind: integration
        ref: "diagnostic_power launch (POWER-OK, FIT-RUN-COMPLETE completed_steps=465000, LAUNCH-EXIT=0); verify-result VERIFY-RESULT-OK; check-run EXP01-CHECK-OK with empty problem lists"
        status: pass
    human_judgment: false
  - id: D3
    description: "The repeat on system 1632 seed 41 ran the same way; the evidence-order check proves each registration precedes its record (RUN-ORDER-OK), check-run is clean on all three (CHECK-RUNS-OK), and both test discoveries pass (phase65 204, phase66 99)"
    requirement: EXP-01
    verification:
      - kind: integration
        ref: "verify-result VERIFY-RESULT-OK; check-run on all three directories (CHECK-RUNS-OK); git merge-base --is-ancestor registration->record for all three (RUN-ORDER-OK); unittest discover tests/phase65 (204 OK) and tests/phase66 (99 OK)"
        status: pass
    human_judgment: false
duration: 122min
completed: 2026-11-01
status: complete
---

# Phase 66: Small-Network Control — Plan 04 Summary

**All three pre-registered EXP-01 runs (main 1632/s42, repeat 851/s42, repeat 1632/s41) each ran once, detached, through the AC-power gate in the owner's Sunday window, each completing its registered 465,000 steps under the 3,300 s cap; each record is verified against its registration and committed with its three sibling files, and no score, tier, branch or similarity value was read anywhere in this plan.**

## Performance
- **Duration:** about 122 minutes (18:12Z–20:14Z; ~85 min of that is the three runs' supervised wall time, polled per the run-state table)
- **Started:** 2026-11-01T18:12:24Z
- **Completed:** 2026-11-01T20:14Z
- **Tasks:** 3 of 3
- **Files modified:** 12 created (the harness-written evidence, four files per run); actuals.tokens is chars/4 over the authored SUMMARY/STATE/ROADMAP text only — the 5.6 MB of machine-written evidence is excluded, as in 66-03

## Accomplishments
- The main EXP-01 run on `hierarchical/gold/1632` seed 42 (commit `a546016b`): launched once, detached, through the AC gate; 465,000 steps (200 warmup, 464,800 measured), 14-entry cadence at the registered steps, loss trace 9,894 entries at stride 47; Stage-0 TRAIN-only access verified mechanically by check-run (one train open, zero validation opens, `test_split_opened` 0); `VERIFY-RESULT-OK`, `EXP01-CHECK-OK` with empty mechanical and setting problem lists.
- The repeat on `hierarchical/gold/851` seed 42 (commit `3dc3646a`): same rule and order, run regardless of the main run's branch (D-07); verified and committed the same way.
- The repeat on `hierarchical/gold/1632` seed 41 (commit `277c25ce`): shares the main run's `run_id` by design; told apart by seed 41, its registration SHA-256 and its directory; verified and committed the same way.
- All-three checks (no run in progress): `RUN-ORDER-OK` (each registration's introducing commit `3f4d0a85` is an ancestor of its record's introducing commit), `CHECK-RUNS-OK` (check-run's final line exactly `EXP01-CHECK-OK` on all three directories), and the wave gate — `tests/phase65` discovery **204 tests OK** (35.4 s, matching 65-CLOSEOUT.md line 105) and `tests/phase66` discovery **99 tests OK** (19.4 s).
- The harness freeze held: no code, page, test or registration changed in this plan; every file created is harness-written evidence.

## Task Commits
1. **Task 66-04-01: run the main EXP-01 run on system 1632, seed 42** - `a546016b` (evidence) — the four files of `evidence/exp01/main-1632-s42/`.
2. **Task 66-04-02: run the second-panel-system repeat on system 851, seed 42** - `3dc3646a` (evidence) — the four files of `evidence/exp01/repeat-851-s42/`.
3. **Task 66-04-03: run the second-seed repeat on system 1632, seed 41, and check the evidence order for all three** - `277c25ce` (evidence) — the four files of `evidence/exp01/repeat-1632-s41/`; then RUN-ORDER-OK, CHECK-RUNS-OK, and both test discoveries.
4. **Docs: complete the three-run execution plan** - SUMMARY commit (this file), then a separate hand-maintained STATE.md/ROADMAP.md update commit (the gsd-tools mutating verbs stay off this checkout, per 66-03 precedent).

## Files Created/Modified
- `.planning/phases/66-small-network-control/evidence/exp01/main-1632-s42/{record.json,diagnostic.weights,attempt.json,power-gate.json}` - the main run's harness-written evidence (new)
- `.planning/phases/66-small-network-control/evidence/exp01/repeat-851-s42/{record.json,diagnostic.weights,attempt.json,power-gate.json}` - the 851 repeat's evidence (new)
- `.planning/phases/66-small-network-control/evidence/exp01/repeat-1632-s41/{record.json,diagnostic.weights,attempt.json,power-gate.json}` - the seed-41 repeat's evidence (new)

## Decisions Made
- None - followed the plan as specified. Every launch command, order, wait rule, verify command and commit subject came from 66-04-PLAN.md and the 66-03 run-state table; nothing was re-sized, retried or substituted.

## Deviations from Plan
- None - plan executed exactly as written. No retry was used (all three roles completed on their first launch), no cap expired, no setting or mechanical problem was reported by any check-run.

## Issues Encountered
- None beyond the pre-existing PyTorch `float(loss)` UserWarning in each launch log (`diagnostic_fit.py:681`), recorded in 65-CLOSEOUT.md and unchanged since.

## Mechanical facts recorded (plan step 7: RECORD ONLY MECHANICAL FACTS)

Each run's launch log (session scratch `/tmp/gsd-66-04/<role>-launch.log`, outside the repository; cwd the trainex root; start time inside each header line). In every log the `FIT-RUN-COMPLETE` line prints before `POWER-OK` because the launcher's POWER-OK line is written by the parent after the child's output; both lines are verbatim below.

**main-1632-s42** (wrapper child PID 87462; log start 18:12Z):
```
FIT-RUN-COMPLETE status=complete completed_steps=465000 seconds_per_step=0.004202254948933541 record=...exp01/main-1632-s42/record.json
POWER-OK source=AC Power isoweekday=7 receipt=...exp01/main-1632-s42/power-gate.json
LAUNCH-EXIT=0
```
- steps completed 465,000 (200 warmup, 464,800 measured); similarity cadence 14 entries at the registered steps; loss trace 9,894 entries at stride 47
- access: one train open, zero validation opens, `access.attestation.test_split_opened` 0 (check-run-verified)
- timing: seconds_per_step 0.004202254948933541; warmup 0.9436903615132906 s; measured 1953.20810026431 s; phases setup 0.6021513750310987 / logging 0.2946966248564422 / scoring 0.42608883301727474 / publish 0.03898108296561986 / data_load 0.29147441702662036
- receipt checked_utc 2026-11-01T18:12:49+00:00 (AC Power, Sunday, inside the window), load average [2.9189453125, 2.580078125, 3.0966796875]; attempt started 18:12:51Z, ended 18:45:28Z, status published, wall 1957 s
- record.json 1,250,910 bytes; SHA-256 `774a5a451bda97c79e39e3e10d146bcde8a5a5551b19a0d3cf59022b4b301007`; weights `bdf95cc1…afc0ce31c6`; attempt `a3b9d57b…962205a8`; receipt `e39b87ca…d5c80de218ba`

**repeat-851-s42** (wrapper child PID 8801; log start 18:50Z):
```
FIT-RUN-COMPLETE status=complete completed_steps=465000 seconds_per_step=0.003724428295332197 record=...exp01/repeat-851-s42/record.json
POWER-OK source=AC Power isoweekday=7 receipt=...exp01/repeat-851-s42/power-gate.json
LAUNCH-EXIT=0
```
- steps completed 465,000; cadence 14 entries; loss trace 9,894 entries at stride 47
- access: one train open, zero validation opens, `test_split_opened` 0 (check-run-verified)
- timing: seconds_per_step 0.003724428295332197; warmup 0.8279038324253634 s; measured 1731.1142716704053 s
- receipt checked_utc 2026-11-01T18:51:15+00:00 (AC Power, Sunday), load average [1.51318359375, 1.54736328125, 2.14453125]; attempt started 18:51:17Z, ended 19:20:11Z, status published, wall 1734 s
- record.json 1,251,193 bytes; SHA-256 `9166311284ea857ea835813ea74b5ea6a30323d0cb4036341b722dcf56add05b`; weights `f73519df…22c62c`; attempt `9175c53c…8a4f0d`; receipt `5e2cdbac…24954990`

**repeat-1632-s41** (wrapper child PID 26775; log start 19:29Z):
```
FIT-RUN-COMPLETE status=complete completed_steps=465000 seconds_per_step=0.004365704157405605 record=...exp01/repeat-1632-s41/record.json
POWER-OK source=AC Power isoweekday=7 receipt=...exp01/repeat-1632-s41/power-gate.json
LAUNCH-EXIT=0
```
- steps completed 465,000; cadence 14 entries; loss trace 9,894 entries at stride 47; seed 41, orbit.train.record_key hierarchical/gold/1632, registration SHA-256 differs from the main run's (`48a15ad6…` vs `b0d79585…`)
- access: one train open, zero validation opens, `test_split_opened` 0 (check-run-verified)
- timing: seconds_per_step 0.004365704157405605; warmup 1.4274682897957973 s; measured 2029.1792923621251 s
- receipt checked_utc 2026-11-01T19:30:38+00:00 (AC Power, Sunday), load average [6.00244140625, 4.0849609375, 3.14208984375]; attempt started 19:30:40Z, ended 20:04:34Z, status published, wall 2034 s
- record.json 1,251,013 bytes; SHA-256 `4146675b56990ca145fa9db777f7922476b1d64ab4cf8f708acb1acec2137c2a`; weights `957af465…f8530aabb`; attempt `f4c17dfc…8fbe1a233`; receipt `4464c41d…b4528d2c`

**Retry:** none — all three roles completed on their first launch, so no `<role>-retry1-registration.json` or `<role>-retry1/` directory exists.

**Record sizes:** 1,250,910 / 1,251,193 / 1,251,013 bytes — each below 10,485,760 (checked by `stat` before staging).

**Machine time:** 1957 + 1734 + 2034 s (the three attempts) + 25 s (the 66-03 timing attempt, 17:57:04–17:57:29Z) = **5,750 s ≈ 1.60 machine-hours** on this Mac.

## Verification (measured)
- `verify-result` on each of the three registrations/records: `VERIFY-RESULT-OK`, exit 0, no FIT-REFUSED on stderr.
- `check-run` on each of the three directories: `EXP01-CHECK-OK` with empty `mechanical_problems` and `setting_problems` and no score value; `CHECK-RUNS-OK` on the all-three loop.
- Evidence order: `RUN-ORDER-OK` (each registration commit `3f4d0a85` is an ancestor of its record commit `a546016b`/`3dc3646a`/`277c25ce` via `git merge-base --is-ancestor`).
- `tests/phase65` discovery: 204 tests, OK (35.371 s). `tests/phase66` discovery: 99 tests, OK (19.363 s).
- `git diff --check a546016b^..a546016b`, `3dc3646a^..3dc3646a`, `277c25ce^..277c25ce`: clean.
- No score, E, tier, similarity, output-movement or loss value was opened, printed or interpreted anywhere in this plan; only whitelisted mechanical fields were extracted from the records. `read-run` was never issued. Branch reading belongs to plan 66-05.

## Next Phase Readiness
- Plan 66-05 reads the three results: record paths `evidence/exp01/main-1632-s42/record.json` (sha256 `774a5a45…b301007`), `evidence/exp01/repeat-851-s42/record.json` (sha256 `91663112…6add05b`), `evidence/exp01/repeat-1632-s41/record.json` (sha256 `4146675b…c2137c2a`), each committed after its registration in `RUN-ORDER-OK` order, all three check-run-clean, so `read-run`/`review`/`confirm`/`route` can now be exercised (checkpoint ① for the owner).
- No retry directories exist; the first-launch directories are the canonical ones for 66-05's readers.
- Machine time consumed by EXP-01 end to end: 5,750 s ≈ 1.60 h (timing run 25 s + the three 465,000-step runs 5,725 s). The owner's weekend AC window was used for about 2 h 12 min wall (18:12Z–20:14Z ≈ 12:12–15:14 America/Chicago, inside the Sunday-before-22:00 window).
- The held-out evaluation remains unspent; nothing beyond each run's registered Stage-0 training gold record was opened.

## Self-Check: PASSED

All 12 created evidence files exist on disk (four per run directory); all five plan commits (`a546016b`, `3dc3646a`, `277c25ce`, `8fd1b131`, `6722b794`) are in `git log`. The working tree afterwards shows only the pre-existing user-owned changes (`.planning/config.json`, the milestone_v2.2 brief, and the untracked `.agents/`, `.gsd/`, `.planning/agent-history.json`, `.planning/milestone.lock`, `.planning/state.json`, `.planning/tmp/`, cross_cutting docs, `phase-40-plan-04-grok.md`), identical to the start status.

---
*Phase: 66-small-network-control*
*Completed: 2026-11-01*
