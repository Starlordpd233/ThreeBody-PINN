---
phase: 66-small-network-control
plan: 03
subsystem: pinn-verification
tags: [exp01, prediction-page, pre-registration, timing-calibration, budget, ac-power-gate, survival-test, evidence-order]
requires:
  - phase: 66-small-network-control (plans 01-02)
    provides: "the frozen harness at 734cb7da: EXP01_VARIANT, REGISTRIES, classify_exp01/improvement_check/readers, diagnostic_power launch/check with the weekend-window gate, exp01_budget/exp01_design, and the seven code digests every registration pins"
provides:
  - "66-TIMING-PREDICTION.md: the frozen EXP-01 design (exp01-design block equal to exp01_design()), the bandwidth case for first_omega_0 = 1000, the suspect table, the reading rule with the improvement check and setting-check table, repeats and confirmation, the budget rule with the 100,000-step sanity stop, the retry and setting-problem rules, and the harness provenance — committed before any Phase 66 run of any kind"
  - "the committed timing calibration evidence evidence/timing/1632-s42/ (record, weights, attempt, power-gate receipt): seconds_per_step 0.004238129693630617 measured through the AC gate in the owner's window; its score was recorded but never read"
  - "66-PREDICTION.md: the full prediction page — timing sections 1-5 and 7 verbatim, the budget from the measured rate (N = 465000, stride 47, cap 3300.0), the three-run table with exact launch commands, the record readout and the what-a-longer-run-would-need section"
  - "three admitting experiment registrations (main-1632-s42, repeat-851-s42, repeat-1632-s41) pinning the prediction page by SHA-256 and the seven frozen code digests, differing only in title, orbit_key, orbit_note and seed"
  - "tests/phase66/test_pages.py real-file classes TimingPageTests, PredictionPageTests and ExperimentRegistrationTests; the phase 66 discovery is 99 tests green and phase 65 stays at 204"
affects: [66-04, 66-05, phase-67]
actuals:
  tokens: 23638
  tasks: 3
  commits: 4
tech-stack:
  added: []
  patterns:
    - "prediction-before-run enforced by git ancestry: page commit -> registration commit -> record commit -> full-page commit -> experiment-registration commits, each an ancestor of the next (ORDER-OK)"
    - "score-blind calibration: check-run verifies the timing run with value-free problem lists only, so its E/tier/similarity/loss are recorded but never shown or read"
    - "verbatim page reuse by construction: the prediction page's frozen sections are spliced from the timing page's exact bytes, and the tests re-derive the splice"
key-files:
  created:
    - .planning/phases/66-small-network-control/66-TIMING-PREDICTION.md
    - .planning/phases/66-small-network-control/66-PREDICTION.md
    - .planning/phases/66-small-network-control/evidence/timing/timing-registration.json
    - .planning/phases/66-small-network-control/evidence/timing/1632-s42/record.json
    - .planning/phases/66-small-network-control/evidence/timing/1632-s42/diagnostic.weights
    - .planning/phases/66-small-network-control/evidence/timing/1632-s42/attempt.json
    - .planning/phases/66-small-network-control/evidence/timing/1632-s42/power-gate.json
    - .planning/phases/66-small-network-control/evidence/exp01/main-1632-s42-registration.json
    - .planning/phases/66-small-network-control/evidence/exp01/repeat-851-s42-registration.json
    - .planning/phases/66-small-network-control/evidence/exp01/repeat-1632-s41-registration.json
  modified:
    - tests/phase66/test_pages.py
key-decisions:
  - "The frozen design, reading rule, budget rule and sanity stop were committed on the timing page before the timing registration pinned them, and the timing registration pinned the page before the run — admission re-checks the page SHA-256, so the scientific rules provably precede every Phase 66 run"
  - "The timing run's score was never read: verification used verify-result and check-run (value-free problem lists) only, never read-run, per timing page section 6"
  - "The detached-launch survival test was run and passed before the launch; the launched child keeps its own session (PGID == own PID) and survived a SIGTERM to the subshell's process group"
  - "The budget is exactly exp01_budget's output from the committed timing evidence (N 465000, stride 47, cap 3300.0); N is far above the 100,000-step sanity stop, so nothing was re-sized or re-set"
patterns-established:
  - "Survival test for the detached wrapper: the simulated agent subshell runs under setsid (macOS has no setsid binary; the pinned interpreter does os.setsid()+exec), the group SIGTERM must kill the subshell but not the detached child, and the child's PGID must equal its own PID"
  - "Registration builder as a scratch script from the smoke-registration template with asserted digests (never committed), mirroring Phase 65's inline practice"
requirements-completed: []
coverage:
  - id: D1
    description: "The frozen EXP-01 design and reading rule are committed on the timing page and pinned by the admitting timing registration before any Phase 66 run"
    requirement: EXP-01
    verification:
      - kind: unit
        ref: "tests/phase66/test_pages.py#TimingPageTests"
        status: pass
      - kind: cli
        ref: "diagnostic_fit check-registration --registration evidence/timing/timing-registration.json (CHECK-REGISTRATION-OK registration-commit=4eab280b)"
        status: pass
    human_judgment: false
  - id: D2
    description: "The timing calibration ran once through the AC-power weekend gate, detached after a passing survival test; verify-result and check-run pass and the score was never read"
    requirement: EXP-01
    verification:
      - kind: integration
        ref: "diagnostic_power launch (POWER-OK, FIT-RUN-COMPLETE completed_steps=5200, LAUNCH-EXIT=0); verify-result VERIFY-RESULT-OK; check-run EXP01-CHECK-OK with empty problem lists"
        status: pass
    human_judgment: false
  - id: D3
    description: "The full prediction page with the measured budget and the three experiment registrations are committed after the timing record, in a git-verifiable order, and all three registrations admit"
    requirement: EXP-01
    verification:
      - kind: unit
        ref: "tests/phase66/test_pages.py#PredictionPageTests and #ExperimentRegistrationTests"
        status: pass
      - kind: integration
        ref: "check-registration on all three (CHECK-ALL-OK); evidence-order ancestry check (ORDER-OK)"
        status: pass
    human_judgment: false
duration: 41min
completed: 2026-11-01
status: complete
---

# Phase 66: Small-Network Control — Plan 03 Summary

**EXP-01's scientific rules were frozen and committed before any run, the timing calibration measured this network's own rate through the AC gate (0.004238129693630617 s/step, score never read), and the measured budget (N = 465000, stride 47, cap 3300 s) and three admitting experiment registrations were committed in a git-verifiable prediction-before-run order.**

## Performance
- **Duration:** about 41 minutes (17:47Z–18:28Z)
- **Started:** 2026-11-01T17:46:39Z (PLAN_START_SHA `7ca90a140e708a7618172803f21a2de526db5be1`)
- **Completed:** 2026-11-01T18:28Z
- **Tasks:** 3 of 3
- **Files modified:** 10 (9 created, 1 modified); actuals.tokens is chars/4 over the authored pages, registrations and tests only (94,554 bytes); the harness-written timing record (564,082 B) and weights (631,881 B) are machine evidence

## Accomplishments
- `66-TIMING-PREDICTION.md` (commit `4eab280b`): the nine frozen sections — the `exp01-design` block exactly equal to `exp01_design()`, the architecture and 157,065-parameter breakdown, the first_omega_0 = 1000 bandwidth case from the census lap counts (460.6/818.6 needed; 1.22x and 2.17x margins), the suspect table with the under-training row, the reading rule with the 0.01-over-the-last-quarter output-movement improvement check, the unsettled label, the setting-check table and no extension rule, repeats and confirmation with the owner-registered near wording, the timing run and its budget rule with the 100,000-step sanity stop, the retry/setting-problem rules, and the harness provenance.
- `evidence/timing/timing-registration.json` (same commit): schema `phase65-fit-registration/v1`, `variant_registry` phase66, seed 42, orbit hierarchical/gold/1632, 5200 steps (200 warmup, 5000 measured), cadence [0, 1300, 2600, 3900, 5200], loss_trace_stride 1, cap 600 s, page SHA-256 pinned, the seven frozen code digests, and the smoke registration's `logger_parity`/`context`/`frozen`/`pinned` blocks verbatim. `TimingPageTests` (7 tests) ties page, registration and live files together.
- The timing calibration (commit `a564ea35`): one run, launched detached through `diagnostic_power launch` after the survival test passed; `POWER-OK source=AC Power isoweekday=7`, `FIT-RUN-COMPLETE status=complete completed_steps=5200 seconds_per_step=0.004238129693630617`, `LAUNCH-EXIT=0`; `VERIFY-RESULT-OK`; `EXP01-CHECK-OK` with empty mechanical and setting problem lists. The record (564,082 bytes, loss_trace_stride 1 with 5,200 entries) is committed with its weights, attempt and receipt, and its score was never read.
- `66-PREDICTION.md` and the three experiment registrations (commit `3f4d0a85`): the prediction page repeats the timing page's sections 1-5 and 7 verbatim and adds the budget from the measured rate — `EXP01-BUDGET steps=465000 loss_trace_stride=47 cap=3300.0`, projected wall 2470.1995211585886 s of the 2475 s target, projected record 1,304,114 bytes against the 1,307,538-byte N-independent ceiling — plus the three-run table with exact launch commands, the record readout and the what-a-longer-run-would-need section. The registrations pin the page SHA-256 `7ec16fe9…`, carry `branch_rule` naming `classify_exp01` (admission ignores it), and differ only in title, orbit_key, orbit_note and seed. `PredictionPageTests` and `ExperimentRegistrationTests` (8 tests) re-derive the splice, the budget and the digest pins from the committed files.

## Task Commits
1. **Task 66-03-01: freeze the exp01 design and register the timing run** - `4eab280b` (evidence) — 66-TIMING-PREDICTION.md (page sha256 `ec54a05e0c98e6b92d303516c4d19ec466064c296ad6227df0efab7ab3e2aaed`), timing-registration.json (sha256 `794daa6e334e44c0f3c0c5a040c635614de20d8143629b9f020e71ac998421c6`), TimingPageTests. check-registration: `CHECK-REGISTRATION-OK registration-commit=4eab280b9a47596b7153e75641c6c95db044e86a`.
2. **Task 66-03-02: record the exp01 timing calibration run** - `a564ea35` (evidence) — the four files of `evidence/timing/1632-s42/`.
3. **Task 66-03-03: register the three exp01 runs with the measured budget** - `3f4d0a85` (evidence) — 66-PREDICTION.md (sha256 `7ec16fe90c34cd01406fe227217916754128a283bc6409ed77f4e1811058d8be`), the three registrations (main `b0d79585131c198a4c09f9dea4f1667b57eed8e38fb0d0fd3b11e5071964dcce`, repeat-851 `40754fb93ac4b8a4aa70c580ec233b6fbf7f15fb95dad002a969215062646f36`, repeat-1632 `48a15ad60f4a018c17eab10211153a48df577a292f9853d68eccd4e38592a8f1`), PredictionPageTests + ExperimentRegistrationTests.
4. **Docs: record the executed plan in state and roadmap** - (hand-maintained STATE.md/ROADMAP.md update; the gsd-tools mutating verbs stay off this checkout).

## The detached-launch survival test (before the launch)

The simulated agent subshell was started in its own session (macOS has no `setsid` binary, so the pinned interpreter ran `os.setsid()` then exec'd bash; the first attempt without a separate group killed the harness script itself and was discarded — its detached pair survived, and the pair was stopped before the clean re-run):

- Subshell (simulated agent session): PID 69274, PGID 69274
- Launched wrapper child (`/bin/sh -c "/bin/sleep 120; echo LAUNCH-EXIT=$?"`): PID 69280, PGID 69280
- Step 2: `kill -TERM -- -69274` (the subshell's process group)
- Step 3: `kill -0 69280` succeeded (`SLEEP-STILL-RUNS`); `ps -o pid=,pgid=` shows 69280/69280 — PGID equals its own PID and differs from the subshell's 69274 (`PGID-CHECK-OK`); the subshell was gone as expected
- Step 4: the sleep and the launch tree were stopped (`LAUNCH-TREE-STOPPED`)

## The timing launch (mechanical facts only)

Session scratch log `/tmp/gsd-66-03/timing-launch.log` (outside the repository; cwd the trainex root; start 2026-11-01T17:56Z), complete lines:

```
POWER-OK source=AC Power isoweekday=7 receipt=.planning/phases/66-small-network-control/evidence/timing/1632-s42/power-gate.json
FIT-RUN-COMPLETE status=complete completed_steps=5200 seconds_per_step=0.004238129693630617 record=...evidence/timing/1632-s42/record.json
LAUNCH-EXIT=0
```

(The FIT-RUN-COMPLETE line prints first in the log because the launcher's POWER-OK line is written by the parent after the child's output; both are verbatim above. The launch child PID was 69455, PGID 69455.)

- steps.completed 5200 (200 warmup, 5000 measured); cadence entries at steps 0, 1300, 2600, 3900, 5200 (5 entries); loss_trace_stride 1 with 5,200 entries
- access: one train open, zero validation opens, `access.attestation.test_split_opened` 0
- `timing.seconds_per_step` 0.004238129693630617; warmup_seconds 1.3444102415814996; measured_seconds 21.190648468153086; phases setup 0.6462582080275752 / logging 0.5760097929742187 / scoring 0.5543462500208989 / publish 0.01299187500262633
- receipt checked_utc 2026-11-01T17:57:03+00:00 (AC Power, Sunday 2026-11-01T11:57:02-06:00 America/Chicago, inside the window), load average [3.37158203125, 3.90869140625, 3.646484375]; attempt started_utc 2026-11-01T17:57:04+00:00, ended_utc 2026-11-01T17:57:29+00:00, status published, its `record_sha256` equal to the record bytes
- record.json 564,082 bytes (well under 1 MiB); SHA-256 `128fe093dac017e1b9c0da900d07db8d768ccfacb9d8f22088b97a938859d671`; weights `68b6ac60…f1712dcc7`; attempt `767b1b15…7bf81fd6`; receipt `4b0d1505…7684a757c`
- launch wall: 26 s receipt-to-attempt-end plus the 2 s margin = 28.0 s (`launch_wall_seconds`)
- No E, tier, similarity, output-movement or loss value was opened, printed or interpreted.

## The budget (from the committed timing evidence)

`-m pinn.verification.diagnostic_phase66 budget --timing-dir .planning/phases/66-small-network-control/evidence/timing/1632-s42` printed `EXP01-BUDGET steps=465000 loss_trace_stride=47 cap=3300.0` (exit 0). N = 465000 (200 warmup, 464800 measured), cadence [0, 100, 300, 1000, 3000, 10000, 30000, 100000, 160833, 221666, 282500, 343333, 404166, 465000] (14 entries), loss_trace_stride 47, projected worker wall 2470.1995211585886 s (target 2475 s = 0.75 x 3300.0), projected record 1,304,114 bytes, record-size ceiling 1,307,538 bytes against 0.9 of the 10,485,760-byte limit of `scripts/git_policy/validate_staged_paths.py`. N is far above the 100,000-step sanity stop, so the stop did not trip, the ceiling did not refuse, and nothing was re-sized.

## check-registration and evidence-order outputs

- Timing: `CHECK-REGISTRATION-OK registration-commit=4eab280b9a47596b7153e75641c6c95db044e86a` (the evidence(66-03) page/registration commit).
- All three experiment registrations: `CHECK-REGISTRATION-OK registration-commit=3f4d0a85232e617fe2146429d223e683e82fe07e` each (`CHECK-ALL-OK`); their page digest is the prediction page's `7ec16fe9…`.
- Evidence order (`git merge-base --is-ancestor` chain, `--diff-filter=A` first commits): timing page `4eab280b` -> timing registration `4eab280b` -> timing record `a564ea35` -> prediction page `3f4d0a85` -> each experiment registration `3f4d0a85` — **ORDER-OK**.

## Verification (measured)
- `tests.phase66.test_pages -v`: 18 tests, OK (TimingPageTests 7, PredictionPageTests 4, ExperimentRegistrationTests 4, PageHelperTests 3).
- `unittest discover -s tests/phase66 -t .`: **99 tests, OK in 17.159 s** (84 before this plan + 15 new).
- `unittest discover -s tests/phase65 -t .`: **204 tests, OK in 31.883 s** (unchanged; no harness file was touched).
- `verify-result` on the timing registration/record: `VERIFY-RESULT-OK`, exit 0 (run twice: after the run and at plan end).
- `check-run` on `evidence/timing/1632-s42`: `EXP01-CHECK-OK` with empty `mechanical_problems` and `setting_problems` and no score value.
- `check-registration` on the timing registration and all three experiment registrations: CHECK-REGISTRATION-OK each.
- Evidence-order check: ORDER-OK (chain above).
- `git diff --check 7ca90a14..HEAD`: clean. No file under `.planning/phases/65-probe-on-the-record-fit-harness` changed; `git show --stat` of each task commit lists exactly its owned paths.

## Files Created/Modified
- `.planning/phases/66-small-network-control/66-TIMING-PREDICTION.md` - the frozen EXP-01 design and timing-run registration page (new)
- `.planning/phases/66-small-network-control/evidence/timing/timing-registration.json` - the immutable timing settings, page digest and seven code digests (new)
- `.planning/phases/66-small-network-control/evidence/timing/1632-s42/{record.json,diagnostic.weights,attempt.json,power-gate.json}` - the harness-written timing evidence (new)
- `.planning/phases/66-small-network-control/66-PREDICTION.md` - the full prediction page with the measured budget (new)
- `.planning/phases/66-small-network-control/evidence/exp01/{main-1632-s42,repeat-851-s42,repeat-1632-s41}-registration.json` - the three experiment registrations (new)
- `tests/phase66/test_pages.py` - TimingPageTests, PredictionPageTests, ExperimentRegistrationTests (modified)

## Decisions Made
- None beyond the plan's explicit text. The survival test needed one mechanical adaptation, recorded below; the scientific content (design block, reading rule, budget rule, sanity stop, retry policy) was transcribed from the plan without invention, and the band edges, thresholds and budget numbers are the plan's or the budget tool's exact outputs.

## Deviations from Plan
- **[Mechanical, Rule 3] The survival test's simulated-agent subshell needed its own session via `os.setsid()`** — **Found during:** Task 66-03-02. **Issue:** macOS has no `setsid` binary, and the first attempt's `set -m` subshell did not get its own process group, so the step-2 group SIGTERM killed the test harness itself (the detached sleep survived, proving the property, but the test did not record cleanly). **Fix:** the subshell body runs through a pinned-interpreter helper that calls `os.setsid()` then execs bash; the stray first-attempt pair was stopped, and the clean re-run recorded all four steps (PIDs/PGIDs above). **Files modified:** none in the repository (scratch scripts in `/tmp/gsd-66-03/` only). **Verification:** `PGID-CHECK-OK`, `SUBSHELL-GONE-AS-EXPECTED`, `LAUNCH-TREE-STOPPED`. **Committed-in:** n/a (scratch only; recorded here per the plan).
- **[Page/test agreement] Two page sentences were reflowed so the tests can match them verbatim** — **Found during:** Task 66-03-01 and 66-03-03 test runs. **Issue:** "This does not show where the fault is" and the GAP-59-08 sentence were line-wrapped in the Markdown, so the literal-string assertions failed; likewise the budget cadence list. **Fix:** reflowed those passages onto single lines (and re-pinned the registration/page digests accordingly); no content changed. **Files modified:** the two pages. **Verification:** 18 tests OK. **Committed-in:** `4eab280b` and `3f4d0a85`.

## Issues Encountered
- The first survival-test attempt killed its own harness script (see deviation above); no repository state was affected and no launch happened before the test passed.
- The pre-existing PyTorch `float(loss)` UserWarning appeared in the launch log (`diagnostic_fit.py:681`), as recorded in 65-CLOSEOUT.md and 66-01-SUMMARY.md; pre-existing, untouched.

## Next Phase Readiness
- Plan 66-04 runs the three pre-registered experiments with everything staged: the page `66-PREDICTION.md` (sha256 `7ec16fe9…`) states each run's exact launch command, output directory and order (main 1632/42, repeat-system 851/42, repeat-seed 1632/41), the registrations admit (`CHECK-ALL-OK`), and the measured budget is N = 465000 steps, warmup 200, cadence 14 entries ending at 465000, loss_trace_stride 47, cap 3300.0 s (about 41 minutes projected, 2,470 s of the 2,475 s target) — each launch still gated on AC power inside the weekend window (Sunday before 22:00 America/Chicago today).
- The timing record's rate (0.004238129693630617 s/step measured) sits inside 66-RESEARCH.md A2's 3-6 ms projection; the sanity stop did not trip.
- Reading path for 66-04/66-05 is unchanged: `read-run`/`check-run`/`review` on the three run directories, `confirm`/`route` for the pre-registered branches, checkpoint ① for the owner. The held-out evaluation remains unspent; no experiment run has started in this plan.

## Self-Check: PASSED

All 11 created/modified plan files exist on disk; all five commits (`4eab280b`, `a564ea35`, `3f4d0a85`, `2e20360c`, `f6de4aa1`) are in `git log`; the working tree afterwards shows only the pre-existing user-owned changes (`.planning/config.json`, the milestone_v2.2 brief, and the untracked `.agents/`, `.gsd/`, `.planning/state.json`, `.planning/milestone.lock`, `.planning/tmp/`, cross_cutting docs, `phase-40-plan-04-grok.md`), identical to the start status.

---
*Phase: 66-small-network-control*
*Completed: 2026-11-01*
