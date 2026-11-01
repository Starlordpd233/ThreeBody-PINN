---
phase: 66-small-network-control
plan: 02
subsystem: pinn-verification
tags: [exp01, ac-power-gate, weekend-window, reading-rule, improvement-check, budget, design-block, harness-freeze, tdd]
requires:
  - phase: 65-probe-on-the-record-fit-harness
    provides: "the INST-08 fit harness and its committed-registration admission (check_fit_registration), write_record_exclusive, the Site F stride contract and the 204-test phase65 suite"
  - phase: 66-small-network-control (plan 01)
    provides: "EXP01_VARIANT, PHASE66_REGISTRY/REGISTRIES, tier1_e_max, classify_exp01, the fail-closed AC gate with the exclusive power-gate.json receipt, and the tests/phase66 helpers (phase66_fixture_registration, fake_pmset)"
provides:
  - "diagnostic_power.py: the America/Chicago weekend window (Saturday, Sunday before 22:00) enforced in code, the output-exists and metadata-only admission prechecks before the receipt, the window block in the receipt, the POWER-OK stdout token, and the read-only check subcommand"
  - "diagnostic_phase66.py: the reading rule with the unsettled label, the output-movement improvement check (0.75 reference fraction, strict 0.01 growth), read_exp01_record/read_run_directory with every mechanical and setting problem, confirm/route, the read-run/check-run/review CLI, the time-bound exp01_budget, the bounded exp01_cadence/stride, launch_wall_seconds, the frozen exp01_design block and the design/budget CLI"
  - "tests/phase66: test_power (22), test_reading_rule (20), test_budget (9), test_pages (3, with the extract_block/has_number helpers for 66-03) — the discovery is 84 tests green"
  - "the frozen seven-file digest set every Phase 66 registration pins"
affects: [66-03, 66-04, 66-05, phase-67]
actuals:
  tokens: 27700
  tasks: 3
  commits: 8
tech-stack:
  added: []
  patterns:
    - "fail-closed environmental gate composed of two independent checks (power source, then weekend window) with the clock injectable end to end"
    - "value-free problem strings: the mechanical/setting readers name failures without embedding any score value, so one reader serves both the owner (read-run) and the score-blind timing check (check-run)"
    - "record size bounded at its source (14-entry cadence, ceil-to-10000 stride) so the run length is set by time alone and the commit limit appears only in an N-independent ceiling guard"
key-files:
  created:
    - tests/phase66/test_power.py
    - tests/phase66/test_reading_rule.py
    - tests/phase66/test_budget.py
    - tests/phase66/test_pages.py
  modified:
    - pinn/verification/diagnostic_power.py
    - pinn/verification/diagnostic_phase66.py
    - tests/phase66/test_tracer.py
key-decisions:
  - "The launch order is fixed exactly as the plan writes it: AC power, weekend window, repository resolution, output-exists precheck, the metadata-only check_fit_registration precheck, the exclusive receipt, POWER-OK, then the caffeinate child; every refusal before the child prints POWER-REFUSED and creates nothing"
  - "The improvement check reads only the DIAG-09 logger's output movement (never the loss) with the reference at or before 0.75 of the final step and a strict 0.01 growth bar (about three times the settled v2.4 movement); a still-improving non-Tier-1 run reads unsettled, is never confirmed and routes to the owner"
  - "check-run prints only the directory and value-free problem lists, so the timing run's score is never shown; review keys runs by the (orbit_key, seed, registration_sha256) triple and refuses duplicates and wrong roles with exit 2"
  - "Time alone sets N (0.75 of the 3,300 s cap at a 25 percent margin); the record-size ceiling does not depend on N and can refuse a broken input but never shorten a run; MAX_BLOB_BYTES and the commit policy are unchanged"
  - "The harness is frozen at 734cb7da: diagnostic_fit.py, diagnostic_phase66.py and diagnostic_power.py do not change for the rest of Phase 66; a later fix retires every registration that pins them and forces fresh pages and registrations"
patterns-established:
  - "Injected clock keyword (now=None) through launch/main so the AC gate is testable on every weekday; tests inject reader, clock and runner and the real pmset/caffeinate are never reached (guarded subprocess shim)"
  - "Page-helper contract for 66-03: extract_block (single-fence, last-token info match) and has_number (digit-boundary) in tests/phase66/test_pages.py"
requirements-completed: []
coverage:
  - id: D1
    description: "The launch gate is fail-closed on every power reading it does not fully recognize, outside the owner's weekend window, on a spent directory, on an inadmissible registration and on outside-repo paths, never reuses a run folder, writes the exact receipt contract with the window block, and has a read-only live check"
    requirement: EXP-01
    verification:
      - kind: unit
        ref: "tests/phase66/test_power.py#Phase66PowerTests"
        status: pass
      - kind: cli
        ref: "pinn.verification.diagnostic_power check (live verdict agrees with pmset and the America/Chicago window; POWER-OK source=AC Power isoweekday=7, exit 0)"
        status: pass
    human_judgment: false
  - id: D2
    description: "The reading rule is unambiguous at its edges (inclusive 0.1, both band edges, non-finite other), labels a still-improving non-Tier-1 run unsettled, and confirm/route follow the pre-registered tables; the improvement check is the tested output-movement rule"
    requirement: EXP-01
    verification:
      - kind: unit
        ref: "tests/phase66/test_reading_rule.py#ReadingRuleTests and #ImprovementTests"
        status: pass
      - kind: cli
        ref: "the inline reading-rule assertion (READING-RULE-OK)"
        status: pass
    human_judgment: false
  - id: D3
    description: "The record and run-directory readers refuse to read a branch from any run with a mechanical problem (status, tier-vs-E, E_const prediction, similarity rows, improvement evaluability, registry fields, split opens, receipt, attempt digest) or a setting problem on a Tier-1 fit, and check-run prints no score value"
    requirement: EXP-01
    verification:
      - kind: unit
        ref: "tests/phase66/test_reading_rule.py#RecordReaderTests"
        status: pass
    human_judgment: false
  - id: D4
    description: "Runs are identified by the (orbit_key, seed, registration_sha256) triple and the three-run review computes the pre-registered confirmation and route, refusing duplicates and wrong roles"
    requirement: EXP-01
    verification:
      - kind: unit
        ref: "tests/phase66/test_reading_rule.py#RunIdentityTests"
        status: pass
    human_judgment: false
  - id: D5
    description: "The time-bound budget, the bounded cadence and stride, the launch-wall margin, the frozen JSON-normal design block and the page helpers are tested, and the harness is frozen with its seven digests recorded"
    requirement: EXP-01
    verification:
      - kind: unit
        ref: "tests/phase66/test_budget.py#Phase66BudgetTests and tests/phase66/test_pages.py#PageHelperTests"
        status: pass
      - kind: cli
        ref: "design round trip (DESIGN-OK) and load_protocol (PROTOCOL-OK)"
        status: pass
    human_judgment: false
duration: 40min
completed: 2026-11-01
status: complete
---

# Phase 66: Small-Network Control — Plan 02 Summary

**The Phase 66 harness is finished and frozen: the launch gate now enforces the owner's verbatim weekend window and refuses spent directories and inadmissible registrations before writing anything, the reading rule (with the unsettled label, the output-movement improvement check and the three-run review) and the time-bound budget are tested deterministic functions, and the seven code dependencies' digests are recorded for the registrations.**

## Performance
- **Duration:** about 40 minutes (17:06Z–17:46Z)
- **Started:** 2026-11-01T17:06:32Z (PLAN_START_SHA `7baba3b139c9842bbdd9985ad6a0ec2f8ba85527`)
- **Completed:** 2026-11-01T17:46Z
- **Tasks:** 3 of 3 (each RED + GREEN, all three RED evidence records machine-verified `RED_EVIDENCE_OK`)
- **Files modified:** 7 (4 created, 3 modified); 2,748 insertions, 22 deletions

## Accomplishments
- `diagnostic_power.py` (task 66-02-01): `WINDOW_TIMEZONE` ("America/Chicago"), `WINDOW_SUNDAY_LAST_HOUR` (22) and `require_weekend_window(now=None)` — the owner's verbatim compute window (D-08, "for the weekend only. not weekdays") enforced in code, converting any aware instant to the window zone and refusing a naive clock or an unloadable zone; `launch` now runs the fixed order (AC power → window → repository resolution → output-exists precheck → the metadata-only `check_fit_registration` precheck → the exclusive receipt → `POWER-OK source=AC Power isoweekday=<d> receipt=<path>` → the caffeinate child) and refuses with `POWER-REFUSED` and exit 2, creating nothing, on every other path; the receipt gains the `window` block (`timezone`, `local_time`, `isoweekday`) and renames `launch` to `launched`; `main` gains the read-only `check` subcommand and the injectable clock.
- `diagnostic_phase66.py` (task 66-02-02): the reading rule gains `unsettled` (a finite non-Tier-1 run still improving when its steps ran out); `improvement_check` reads only the DIAG-09 logger's output movement with the reference at or before 0.75 of the final step and a strict 0.01 growth bar; `read_exp01_record`/`read_run_directory` produce the identity, scores, similarity context, improvement, value-free mechanical/setting problems, `e_band` and `branch` (out-of-branch on any mechanical problem, or a setting problem on a Tier-1 fit); `confirm`/`route` implement the pre-registered tables; the `read-run`, `check-run` and `review` CLI (missing flags exit 2; check-run prints only the directory and value-free problems; review refuses duplicates and wrong roles by the run-identity triple).
- `diagnostic_phase66.py` (task 66-02-03): the one `BUDGET_RULE`; `exp01_cadence` (at most 14 entries), `exp01_loss_trace_stride` (ceil(n/10,000)), `loss_trace_entries` (exactly Site F's length), `launch_wall_seconds` (ended − checked + 2 s), `exp01_budget` (N set by time alone at 0.75 of the 3,300 s cap with a 25 percent margin; the N-independent record-size ceiling guard against 0.9 of 10 MiB), the frozen JSON-normal `exp01_design()` block, and the `design`/`budget --timing-dir` CLI (the budget prints no score, similarity or loss value).
- `tests/phase66/test_power.py` (22 tests), `test_reading_rule.py` (20 tests, four classes), `test_budget.py` (9 tests), `test_pages.py` (3 tests plus the `extract_block`/`has_number` helpers 66-03's real-file classes reuse); the tracer's two cases inject a Saturday clock through the new `fake_clock` helper, so the harness stays green on every weekday.

## Task Commits
1. **Task 66-02-01 RED: failing launch gate matrix** - `24bad2ae` (test) — tests/phase66/test_power.py; 14 of 22 tests error on the missing window constants/function/`now` keyword/`check` subcommand; RED verdict `RED_EVIDENCE_OK` (target: `test_launch_refuses_outside_the_weekend_window`).
2. **Task 66-02-01 GREEN: the launch gate** - `9c8e28dc` (feat) — the weekend window, the launch order with both prechecks, the receipt window block, the check subcommand, and the tracer's injected Saturday clock. 22 module tests OK; phase 66 discovery 52 tests OK in 15.211 s.
3. **Task 66-02-02 RED: failing reading rule and run reader tests** - `86a35ec8` (test) — tests/phase66/test_reading_rule.py; 19 of 20 tests error on the missing constants/functions/CLI; RED verdict `RED_EVIDENCE_OK`.
4. **Task 66-02-02 GREEN: reading rule, improvement check, readers, review** - `3fbba72d` (feat) — 20 module tests OK; READING-RULE-OK; discovery 72 tests OK in 17.582 s.
5. **Task 66-02-03 RED: failing budget, cadence and page helper tests** - `9fbac07d` (test) — tests/phase66/test_budget.py + test_pages.py; 10 of 12 tests fail on the missing functions/CLI; RED verdict `RED_EVIDENCE_OK`.
6. **Task 66-02-03 GREEN: time-bound budget and the freeze** - `734cb7da` (feat) — 12 module tests OK; the freeze commit.

## The live power-check line

Run after task 66-02-01 and again at the freeze (both agreed with the first line of `/usr/bin/pmset -g batt` and the America/Chicago weekday and hour; Sunday 11:00, inside the window):

```
pmset_first_line=Now drawing from 'AC Power'
chicago_dow=7 hour=11
check_output=POWER-OK source=AC Power isoweekday=7
check_exit=0
```

## The seven frozen code-dependency digests (at `734cb7da`, `shasum -a 256`)

| Module | SHA-256 |
|---|---|
| `pinn/verification/diagnostic_fit.py` | `4884a1a5a2d0f0356ff142b5bb2ba6b438bdf5e11dd8425f1ec73493c4e7b273` |
| `pinn/verification/diagnostic_guard.py` | `8dd577a263c28bf7886a0795336ac613fe3fde7c8ebf424fcd6eaf2e80fef540` |
| `pinn/verification/diagnostic_data.py` | `47b9d99dd991c2a899cb8a4308273643c1d98ea591b851546373e44bcf429836` |
| `pinn/verification/diagnostic_variants.py` | `ad8ed66c43a8d6edbef15e794f4f06af194a99729acd103428c25bd6cd0c5dfb` |
| `pinn/verification/diagnostic_similarity.py` | `e80079b62485f04c7c42a513913ef392d7201eea625ff496bae432d0c440d4b7` |
| `pinn/verification/diagnostic_phase66.py` | `cb0577fe6e976f3ed75ecf95e01f235e0c3cc94289ce316c731fe42581bc4ec7` |
| `pinn/verification/diagnostic_power.py` | `7e2f00e2c275bc6897bb971af06538ee561635bbabbf1b79c8b7bedfb05f4200` |

**Freeze rule:** these seven files do not change for the rest of Phase 66. Every registration written next pins them by digest; a later fix retires every registration that pins them, and forces fresh pages and registrations. The four Phase 65 smoke-pinned modules (guard, data, variants, similarity) remain byte-identical to their recorded digests.

## Verification (measured)
- `tests.phase66.test_power -v`: 22 tests OK.
- `tests.phase66.test_reading_rule -v`: 20 tests OK; the inline reading-rule assertion printed `READING-RULE-OK`; `read-run`/`check-run` with no `--dir` and `review` with a missing role flag each exit 2.
- `tests.phase66.test_budget tests.phase66.test_pages -v`: 12 tests OK.
- `unittest discover -s tests/phase65 -t .`: **204 tests, OK in 29.227 s** (the 204 of `65-CLOSEOUT.md` line 105) at the freeze.
- `unittest discover -s tests/phase66 -t .`: 84 tests, OK — 52 in 15.211 s after task 1, 72 in 17.582 s after task 2, **84 in 16.116 s** at the freeze (under the 30 s expectation).
- `design` round trip: `DESIGN-OK`; `load_protocol()`: `PROTOCOL-OK` (all 33 pinned digests unchanged).
- `git diff --check` clean at every commit and over the whole plan range (`7baba3b1..HEAD`); `git status --porcelain -- pinn/verification tests/phase66` prints nothing after the final commit.

## Decisions Made
- The window check converts any aware instant to America/Chicago before the check (a UTC instant reads as its Chicago local time), and the zone lookup itself is inside the refusal path, so an unloadable zone refuses even with an injected clock.
- `check_fit_registration` is imported inside `launch` (deferred), keeping the gate module light and the spy-patching surface honest; the refusal names the admission failure.
- The mechanical problem strings are value-free by construction (module constants), so check-run can print any of them; the plan-mandated string "the improvement check cannot be evaluated" is kept verbatim.
- The review's refusal token is `EXP01-REFUSED:` on stderr (mirroring the `FIT-REFUSED` convention) while the plan's stdout tokens (`EXP01-RUN-OK`, `EXP01-CHECK-OK`, `EXP01-REVIEW ...`) stay on stdout, including the `*-PROBLEMS:` variants, which are reports with exit 2 rather than stderr refusals.
- `exp01_cadence` uses integer floor math for the tail entries (`100000 + k*(n-100000)//6`), which reproduces the plan's 268,000 and 637,000 schedules exactly and always ends at n.
- The `has_number` page helper treats a trailing sentence period as punctuation (digit-boundary only), and `extract_block` matches the fence's final whitespace-separated token, so ` ```json exp01-design ` blocks are addressable by name.

## Deviations from Plan
- **[Rule 1 - Test bug] Two reading-rule test defects fixed during task 66-02-02 GREEN** — **Found during:** Task 66-02-02 GREEN. **Issue:** (a) the boundary/confirm/route assertions used `assertIs` on string labels, which is over-pinning (one interned literal compared unequal-by-identity); (b) the unevaluable-improvement test deleted the output movement at `CADENCE[9]` (step 156,000) instead of the reference entry (step 184,000). **Fix:** (a) `assertEqual` for label values (`assertIs` kept for booleans only); (b) `CADENCE.index(184000)`. **Files modified:** tests/phase66/test_reading_rule.py. **Verification:** 20 tests OK. **Committed-in:** `3fbba72d`.
- **[Rule 3 - Blocking] The `diagnostic_phase66` module lacked its `if __name__ == "__main__"` entry** — **Found during:** Task 66-02-02 GREEN acceptance check. **Issue:** `python -m pinn.verification.diagnostic_phase66 read-run` exited 0 for missing flags because the module never called `main`. **Fix:** added the `sys.exit(main())` guard. **Files modified:** pinn/verification/diagnostic_phase66.py. **Verification:** read-run/check-run/review with missing flags exit 2. **Committed-in:** `3fbba72d`.
- **[Rule 1 - Test bug] Two budget test defects fixed during task 66-02-03 GREEN** — **Found during:** Task 66-02-03 GREEN. **Issue:** (a) the maximality assertion compared the headroom with the wrong direction (`assertGreater` instead of `assertLess` — the implementation was maximal, the check was inverted); (b) the design's `budget_rule` comparison used `dict(BUDGET_RULE)`, whose cadence tuples are intentionally JSON-normalized to lists in the design block. **Fix:** (a) assert the headroom is smaller than one quantum's measured cost; (b) compare against the tuple→list-normalized expected rule. **Files modified:** tests/phase66/test_budget.py. **Verification:** 12 tests OK. **Committed-in:** `734cb7da`.

No harness site changed after its RED commit beyond the plan's own task scope; no Phase 65 refusal was weakened (204 tests OK at the freeze), and no Phase 65 artifact was touched.

## Issues Encountered
- The tracer's AC case now prints `POWER-OK ...` to the test runner's stdout (the tracer does not capture the launcher's success token, exactly as its injected supervisor's `FIT-RUN-COMPLETE` line already leaked); harmless, and the assertion set is unchanged.
- The `route()` identity-vs-equality surprise above was a Python string-interning artifact; the contract is value equality and the tests now say so.

## TDD Gate Compliance
All three tasks ran RED → GREEN with a `test(66-02)` commit preceding each `feat(66-02)` commit (`24bad2ae`→`9c8e28dc`, `86a35ec8`→`3fbba72d`, `9fbac07d`→`734cb7da`), and each RED evidence record was machine-verified `RED_EVIDENCE_OK` via `check tdd-red-evidence` before GREEN. No REFACTOR commits were needed.

## Next Phase Readiness
- Plan 66-03 can commit the pages and registrations against the frozen bytes: `exp01_design()` is the exact design-block text (`design` CLI, DESIGN-OK), `extract_block`/`has_number` in `tests/phase66/test_pages.py` are the page-test helpers, `exp01_budget`/`launch_wall_seconds`/`budget --timing-dir` are the measured-rate path, and the seven digests above are what every registration's `code_dependencies` records.
- The `EXP01_RUNS` triple, `read-run`/`check-run`/`review` are the reading path for 66-04/66-05; a launch before Sunday 22:00 America/Chicago on AC power is the only admitted compute window.
- No blockers. The held-out evaluation remains unspent; nothing opened Stage-0 data, used MPS, or launched any real run in this plan.

---
*Phase: 66-small-network-control*
*Completed: 2026-11-01*
