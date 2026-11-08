---
phase: 67-design-settings-ladders
plan: "14"
subsystem: verification-diagnostics
tags: [pinn, exp05, window-ladder, pre-registration, metadata-capture, timing-rows, serial-launch, budget, science-registrations]

requires:
  - phase: 67-design-settings-ladders (67-13)
    provides: PHASE67-REVIEW-OK on the unsettled EXP-04 verdict admitting EXP-05 under its existing committed registration with no plan amendment
provides:
  - The committed EXP-05 signed-lap window-ladder scientific design (67-EXP05-TIMING-PREDICTION.md, design.json, metadata-registration.json): the locked depth12/width256/first-omega-30/raw14/rate-1e-4 setup at 1, 2, 5 and 10 inner laps on the three registered cases, each arm an exact physical prefix from zero whose endpoint is the first existing gold timestamp reaching its requested cumulative signed turns, lap10 the registered control, and the full prospective reading branches fixed before any real attempt
  - One guarded TRAIN-only metadata capture for both registered Stage0 systems (1632 and 851) with exact first-crossing window endpoints, retained sample counts, physical/tau-grid hashes and independently cross-checked same-window baselines (201db8e0), plus the committed 12-row timing matrix and every timing row registration before any launch (146153d2)
  - All 12 EXP-05 timing rows measured serially (each launched exactly once at N=1200 under the 900-second whole-launch cap, PHASE67-ROW-OK, committed as four artifacts before the next launch) — the experiment's own cost basis, no Phase65/66 rate borrowed
  - The derived cost-only Plan04 budget (common N=148700 optimizer steps; worst-row projection 2654.00 s against the 2655 s = 0.75 x 3540 s science cap; experiment projection 30305.5 s) with the frozen prediction page, the 12-row science matrix and every science registration committed BEFORE any science launch — no science run has started (79587171)
  - Three harness fixes restoring the exp05 flow end to end (8c6c201f, 54d3cb40, bbf492d4): the lap variants now materialize from the committed metadata record in every process that admits an exp05 registration, including the fit CLI's own spawned interpreter, each with regression tests and freeze-chain re-pins
affects: [67-15 (EXP-05 science run), 67-16, Phase 68 energy adjudication]

# Actuals (#2632) — pairs with the plan's `estimate` (10000 est / 20000 raw tokens, 3 tasks).
# Scale caveat: the realized diff is dominated by machine-written evidence
# (12 run records ~100-570 KB each plus the 24 registrations and the frozen
# pages); the three harness fixes each also re-pinned 100-112 live
# registrations (+ digest lines), and the weights binaries are excluded.
actuals:
  tokens: 712502     # chars/4 over the realized text diff b7b31072..HEAD (2,850,008 bytes; weights binaries excluded)
  tasks: 3           # 67-14-01, 67-14-02, 67-14-03 — all executed
  commits: 20        # 19 through the budget freeze + this docs close-out

tech-stack:
  added: []
  patterns:
    - "Registry state cannot cross a spawn boundary: the exp05 lap variants materialize from the committed metadata record inside the settings gate itself (validate_smoke_settings), the one admission contract every process re-executes — parent commands, the supervised launch child and the fixed-argv fit CLI/worker alike."
    - "Serial timing campaign at the registered N: per row, check-matrix -> AC/window/no-other-run eligibility -> previous row verified committed -> launch-row exactly once -> check-row (value-free) -> cost-only inspection -> commit the row's four files before the next launch, all inside a session-level caffeinate wake lock on top of the per-launch caffeinate."

key-files:
  created:
    - .planning/phases/67-design-settings-ladders/67-EXP05-TIMING-PREDICTION.md
    - .planning/phases/67-design-settings-ladders/67-EXP05-BUDGET.md
    - .planning/phases/67-design-settings-ladders/67-EXP05-PREDICTION.md
    - .planning/phases/67-design-settings-ladders/evidence/exp05/design.json, metadata-registration.json
    - .planning/phases/67-design-settings-ladders/evidence/exp05/metadata/{record.json,attempt.json,power-gate.json}
    - .planning/phases/67-design-settings-ladders/evidence/exp05/timing-matrix.json
    - .planning/phases/67-design-settings-ladders/evidence/exp05/timing/CASE/ARM/{registration.json,record.json,attempt.json,power-gate.json,diagnostic.weights} (12 rows)
    - .planning/phases/67-design-settings-ladders/evidence/exp05/budget.json
    - .planning/phases/67-design-settings-ladders/evidence/exp05/science-matrix.json
    - .planning/phases/67-design-settings-ladders/evidence/exp05/science/CASE/ARM/registration.json (12 rows)
  modified:
    - pinn/verification/diagnostic_phase67_execution.py (ordering fix + public materializer; 8c6c201f, bbf492d4)
    - pinn/verification/diagnostic_fit.py (lazy exp05 materialization in the settings gate; 54d3cb40)
    - tests/phase67/test_workflow.py (4 regression tests)
    - .planning/phases/67-design-settings-ladders/evidence/harness-freeze.json + 112 live registrations (three freeze-chain re-pins)
    - .planning/STATE.md, .planning/ROADMAP.md (plan tracking)

key-decisions:
  - "Every real attempt stayed serial, single-use, TRAIN-only and supervised: 12 launches (rows 1-12, 19:52-20:00 CST window Saturday) each exactly once through the guarded launcher on AC power inside the weekend window (POWER-OK AC Power, isoweekday 6), each a complete 1200-step attempt published under the 900-second cap; zero retries, zero reused directories, no timing E value ever screened (check-row's value-free audit was the only per-row verdict)."
  - "The exp05 window variants were never reachable in the admitting processes until this plan's fixes: register-timing refused on row 1 of the matrix (the materialization ran only after the registrations were written — an ordering inversion no synthetic test covered because the workflow chain exercises register-timing only for exp02), and the first real launch then refused inside the fit CLI's spawned interpreter, which re-executes the settings gate in a process nothing had loaded the capture into. Both were fixed under the dispatch's new-defect protocol with the evidence bytes untouched: the variants now materialize from the committed capture at the one choke point (the committed-record load) and lazily inside validate_smoke_settings itself; three regression tests and three freeze-chain re-pins; no registered design, prediction, setting or pass bar changed."
  - "The cost-only budget is derived from this experiment's own 12 measured timing rows (Plan04 verbatim): the largest common N in 100-step quanta is 148700 optimizer steps (148500 measured + 200 warmup), where the worst row (lap10 on the seed-41 repeat case, 0.014240 s/step) projects 2654.00 s — one 100-step quantum higher would breach the 2655 s science cap; the 12-run science experiment projects 30305.5 s. Every science row is registered prospectively at that one common N with the normalized cadence [0, 37175, 74350, 111525, 148700] and score cadence [74350, 111525, 148700], cap 3540 s, and the original full contrast/repeat rule (every shorter prefix against the lap10 control, confirmation requires all three cases); no admissible-N refusal occurred and no arm was rescued."

coverage:
  - id: D1
    description: "The committed design, metadata capture and 12-row timing matrix precede every real attempt; all 12 timing rows launched exactly once, serially, at N=1200 under the 900-second whole-launch cap on AC power inside the owner's window, each mechanically checked with scores hidden and committed as four artifacts before the next launch"
    requirement: EXP-05
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-row per row (12x PHASE67-ROW-OK) and check-matrix --kind timing (PHASE67-MATRIX-OK) before each launch"
        status: pass
    human_judgment: false
  - id: D2
    description: "The cost-only budget derived from all 12 committed timing rows (no Phase65/66 rate, no score influence), and all 12 science rows registered prospectively at the one common N with measured overhead before any science launch; no science run has started"
    requirement: EXP-05
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-budget --experiment exp05 (PHASE67-BUDGET-OK) and check-matrix --experiment exp05 --kind science (PHASE67-MATRIX-OK) at the committed boundary 79587171"
        status: pass
    human_judgment: false

duration: ~1h25m wall (2026-11-07 18:46-20:11 CST, single executor session; 12 supervised launches totalling ~167 s plus the metadata capture, per-row checks/commits, three harness fixes with suites and re-pins, budget and science freeze)
completed: 2026-11-07
status: complete
---

# Phase 67 Plan 14: EXP-05 Window-Ladder Pre-Registration — Timing & Budget Summary

**The EXP-05 signed-lap window ladder is pre-registered end to end with NO science launch: the committed design (locked setup at 1/2/5/10 inner laps against the lap10 control, exact first-crossing endpoints, no interpolation, no tau stretching), one clean guarded metadata capture for both TRAIN systems, all 12 timing rows measured serially at N=1200 under the 900-second cap (each PHASE67-ROW-OK, committed before the next launch), and the cost-only Plan04 budget (common N=148700, worst-row projection 2654.00 s vs the 2655 s cap, experiment projection 30305.5 s) with the prediction page, 12-row science matrix and all 12 science registrations frozen at 79587171 — all five gates green (PHASE67-DESIGN-OK, PHASE67-METADATA-OK, PHASE67-MATRIX-OK timing and science, PHASE67-BUDGET-OK).**

## Performance

- **Duration:** 2026-11-07 18:46-20:11 CST (~1 h 25 m; one metadata capture + 12 serial supervised launches totalling ~167 s wall against the 900 s cap each, plus per-row checks/commits, three harness fixes with suites and freeze re-pins, budget and science freeze)
- **Tasks:** 3 of 3 executed
- **Commits:** 19 through the science freeze + this docs close-out

## Accomplishments

- Task 67-14-01: prepare-design froze the complete EXP-05 scientific design trio (072abd88): the locked depth12/width256/first-omega-30/hidden-omega-1/raw14/rate-1e-4 setup at 1, 2, 5 and 10 inner laps on main-1632-s42, repeat-851-s42 and repeat-1632-s41 (12 case-major rows), each arm an exact physical prefix from zero whose endpoint is the first existing gold timestamp reaching its requested cumulative signed turns, the global T normalization and exact inclusive mask preserved, no interpolation and no per-window tau stretching (D-06); lap10 the registered control with every shorter prefix contrasted against it; the confirmatory rule (same E direction in all three cases plus a matching frozen-tier change or >=20% E effect in each; final-quarter E decrease >5% unsettled), the flat/opposite/unsettled/mechanical branches, five similarity events, three frozen-score events, no automatic continuation, the single 900-second whole-attempt metadata cap over both systems with no optimizer, and the frozen dependency digests all declared; D-02 control limits, adjacent-time similarity terminology and GAP-59-08 carried forward. check-design prints PHASE67-DESIGN-OK.
- Task 67-14-02: one guarded TRAIN-only metadata capture (201db8e0, 2 TRAIN reads, no optimizer, status complete under the 900-second cap; power receipt AC Power isoweekday 6, closing 2026-11-09T04:00Z) pins both systems' census N_in (1632: 10.472, 851: 18.612), f=N_in/10 frequencies with strictly-sub-pi phase increments, and each system's exact first-crossing window endpoints of 1, 2, 5 and 10 cumulative signed turns with retained counts, last timestamps and physical/tau-grid hashes (1632: lap1 0.95/96, lap2 1.89/190, lap5 4.76/477, lap10 9.51/952; 851: lap1 55, lap2 109, lap5 269, lap10 5.37/538), with the window-mean constant and two-Kepler baselines independently recomputed per window and GAP-59-08 carried. check-metadata prints PHASE67-METADATA-OK. register-timing then wrote the exact 12-row timing matrix and every row registration (146153d2), each binding the committed capture and immutable design at N1200/warmup200/measured1000, similarity [0, 300, 600, 900, 1200], score [600, 900, 1200], 900-second cap; check-matrix --kind timing prints PHASE67-MATRIX-OK.
- Task 67-14-03: all 12 timing rows launched serially, one at a time, each exactly once (check-matrix -> AC/window eligibility -> earlier rows verified committed -> launch-row -> check-row PHASE67-ROW-OK -> commit the row's four artifacts before the next launch; rows 1-12 across 19:52-20:00 CST Saturday on AC power, measured walls ~16-17 s each). The budget step then froze the science state in one boundary (79587171): budget.json (common N=148700, per-row projections 2421.89-2654.00 s, experiment projection 30305.5 s, phase ledger distinguishing measured experiments from cap reservations), the immutable 67-EXP05-PREDICTION.md, the cost page 67-EXP05-BUDGET.md, science-matrix.json and all 12 prospective science registrations. check-budget prints PHASE67-BUDGET-OK and check-matrix --kind science prints PHASE67-MATRIX-OK. No science run has started.
- A session-level caffeinate wake lock was held across all gated work (restarted once mid-run when the background task was killed); the machine stayed on AC power at 100% throughout.

## Task Commits

1. **Task 67-14-01 design** - 072abd88 (evidence) - 67-EXP05-TIMING-PREDICTION.md + design.json + metadata-registration.json; PHASE67-DESIGN-OK.
2. **Task 67-14-02 metadata** - 201db8e0 (evidence) - metadata record/attempt/power-gate; PHASE67-METADATA-OK.
3. **Harness fix 1** - 8c6c201f (fix) - the lap variants materialize at the committed-record choke point before any registration write; +1 regression test; freeze re-pin (execution 4d7ef837->6bef604a, manifest 9dd440c7->1d55cd4e, 100 registrations).
4. **Task 67-14-02 matrix** - 146153d2 (evidence) - timing-matrix.json + 12 timing registrations; PHASE67-MATRIX-OK (timing).
5. **Harness fix 2** - 54d3cb40 (fix) - lazy exp05 materialization inside validate_smoke_settings (the fit CLI's spawned interpreter); +3 regression tests; freeze re-pin (fit b336503d->2917de34, manifest 1d55cd4e->aa5ef613, 112 registrations).
6. **Harness fix 2b** - bbf492d4 (fix) - the public materialize_phase67_exp05_variants wrapper the hook calls was left unstaged by the previous commit; landed with its re-pin (execution 6bef604a->d5446f27, manifest aa5ef613->a84c93ba, 112 registrations).
7. **Timing rows 1-12** - 7a630074 (main/lap1), bb361a96 (main/lap2), 0a4d2591 (main/lap5), 2243eb44 (main/lap10), 41b101a5 (851/lap1), 0cfdcefa (851/lap2), 33e751e1 (851/lap5), 64e2d502 (851/lap10), 13736321 (s41/lap1), bd99c336 (s41/lap2), f611f7f9 (s41/lap5), 6bb3af7e (s41/lap10, final) — each the row's record.json, attempt.json, power-gate.json and diagnostic.weights.
8. **Budget + science freeze** - 79587171 (evidence) - budget.json, both pages, science-matrix.json, 12 science registrations; PHASE67-BUDGET-OK, PHASE67-MATRIX-OK (science).
9. **Plan close-out:** this docs commit (SUMMARY + STATE.md/ROADMAP.md; on-disk state files removed).

## Files Created/Modified

- `67-EXP05-TIMING-PREDICTION.md`, `67-EXP05-BUDGET.md`, `67-EXP05-PREDICTION.md` — the three frozen pages
- `evidence/exp05/design.json`, `metadata-registration.json`, `metadata/*`, `timing-matrix.json`, `timing/CASE/ARM/*` (12 rows x 5 artifacts beside their registrations), `budget.json`, `science-matrix.json`, `science/CASE/ARM/registration.json` (12)
- `pinn/verification/diagnostic_phase67_execution.py`, `pinn/verification/diagnostic_fit.py` — the two exp05 materialization fixes (ordering + lazy fit-door hook)
- `tests/phase67/test_workflow.py` — 4 regression tests
- `evidence/harness-freeze.json` + 112 live exp02/exp03/exp04/exp05 registrations — three freeze-chain re-pins (digest fields only)
- `.planning/STATE.md`, `.planning/ROADMAP.md` — plan tracking

## Decisions Made

- No scientific value was screened during the run loop: check-row's value-free mechanical audit was the only per-row verdict, per-row inspection touched cost fields only (attempt status, power source, wall/seconds-per-step), and no arm was selected, extended or reordered after any result.
- The budget derivation accepted the tool's Plan04 output verbatim (N=148700 with the worst row 1.00 s under the cap); no admissible-N refusal occurred, so no resource refusal needed reporting and no arm was rescued or cap relaxed.
- The first real launch's refusal (unknown diagnostic variant inside the fit CLI) was treated as a harness defect under the dispatch's prescribed new-defect protocol, NOT as a burned row: the run never claimed an attempt (no attempt.json, no data access, no optimizer — only the launcher's power-gate receipt existed, written before the refusal because check_fit_registration is committed-identity only and does not resolve variants). The uncommitted orphaned receipt was removed (its bytes never committed; the refusal documented in the fix commits) so the row's first real attempt could claim the directory, exactly as the launch gate's exclusive-first-write convention intends.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] The exp05 lap variants materialized only after the registrations that need them**
- **Found during:** Task 67-14-02 (register-timing refused on the first row)
- **Issue:** _materialize_exp05_variants ran at the END of _write_row_registrations, but each row registration's settings block resolves its variant through phase67_arm_variant while being written — every exp05 register-timing refused; no synthetic test covered it because the workflow chain exercises register-timing only for exp02.
- **Fix:** the materialization moved to the committed-metadata-record choke point (_committed_metadata_record), made idempotent within a process; the late call removed; coverage extended to the commands that admit exp05 registrations without loading the record (launch science branch, check-row, write_review); one regression test proves register-timing writes all 12 rows from a cleared registry.
- **Files modified:** pinn/verification/diagnostic_phase67_execution.py, tests/phase67/test_workflow.py, harness-freeze.json, 100 registrations
- **Commit:** 8c6c201f

**2. [Rule 3 - Blocking] The fit CLI's spawned interpreter could not resolve the materialized variants**
- **Found during:** Task 67-14-03 (row 1's launch refused post-receipt, pre-attempt)
- **Issue:** the supervised launch spawns the fixed-argv fit CLI (and its worker), which re-executes the settings gate in a fresh process where nothing has loaded the capture — registry state cannot cross the spawn boundary (the same principle as 67-06's rule-patch boundary) — so the fit admission refused "unknown diagnostic variant exp05-lap1-1632" after the gate receipt was written.
- **Fix:** validate_smoke_settings materializes the lap set once when a settings block names an unloaded exp05 window variant (through the execution module's public hook), keeping the original refusal for every other unknown name and for a missing/incomplete record; three regression tests; freeze re-pin.
- **Files modified:** pinn/verification/diagnostic_fit.py, tests/phase67/test_workflow.py, harness-freeze.json, 112 registrations
- **Commit:** 54d3cb40

**3. [Rule 3 - Blocking] The fix-2 commit left the hook's public wrapper unstaged**
- **Found during:** Task 67-14-03 (post-commit gate verification)
- **Issue:** diagnostic_phase67_execution.py's materialize_phase67_exp05_variants wrapper was omitted from fix 2's staging, so the committed tree's lazy admission could only refuse and the manifest still pinned the pre-wrapper execution digest.
- **Fix:** landed the wrapper with its own freeze-chain re-pin (execution 6bef604a->d5446f27, manifest aa5ef613->a84c93ba, 112 registrations).
- **Files modified:** pinn/verification/diagnostic_phase67_execution.py, harness-freeze.json, 112 registrations
- **Commit:** bbf492d4

---

**Total deviations:** 3 auto-fixed (all blocking harness defects; the exp05 flow was never exercised end to end in a real or synthetic process before this plan)
**Impact on plan:** all three were the minimal changes needed to make the plan's own registered commands work for exp05's shape; no registered design, prediction, setting, pass bar or evidence byte changed; each fix carries regression tests and a freeze-chain re-pin per the established convention.

## Issues Encountered

- The pre-fix register-timing attempt wrote timing-matrix.json before refusing at the row settings; the orphaned file was verified byte-identical to the fixed command's output (12 rows, same metadata sha) before being removed so the guarded command could complete its exclusive first write. The refused first launch's power-gate receipt was likewise removed uncommitted (documented above).
- The torch requires_grad UserWarning at diagnostic_fit.py:876 appears in every launch log; pre-existing, informational, outside the harness freeze (also recorded by 67-11/67-12).
- The session-level caffeinate background task was killed once mid-run (between rows 1 and 2); it was restarted immediately with a fresh 4-hour lock before any further launch.

## Known Stubs

None — every artifact (design trio, metadata capture, 12 timing rows x 5 files, budget, both pages, science matrix, 12 science registrations) is complete machine-generated evidence; no placeholder or unwired value exists.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- EXP-05's science campaign (67-15) launches against the committed science matrix: 12 rows at the common N=148700, cap 3540 s, experiment projection 30305.5 s (~8.4 h), review and scope handling per the plan's registered reading branches. The weekend window closes Sunday 2026-11-08 22:00 America/Chicago; the experiment projection fits inside the remaining allowance only if the campaign starts promptly.
- No held-out evaluation was spent, no source symbol/flag/scoring bar/package was added, and every historical byte (including all as-captured citations) is preserved.

## Self-Check: PASSED

All created evidence/page files exist on disk (design trio, metadata trio, 12 timing rows x 5 artifacts beside their committed registrations, budget.json, science-matrix.json, 12 science registrations, both new pages, this SUMMARY); all 19 pre-close-out commits exist in history (072abd88, 201db8e0, 8c6c201f, 146153d2, 54d3cb40, bbf492d4, 7a630074, bb361a96, 0a4d2591, 2243eb44, 41b101a5, 0cfdcefa, 33e751e1, 64e2d502, 13736321, bd99c336, f611f7f9, 6bb3af7e, 79587171); all five gates ran green at the settled bytes (PHASE67-DESIGN-OK, PHASE67-METADATA-OK, PHASE67-MATRIX-OK timing, PHASE67-BUDGET-OK, PHASE67-MATRIX-OK science); the three suites ran green at the settled bytes (phase65 204 OK, phase66 101 OK, phase67 260 OK).

---

*Phase: 67-design-settings-ladders*
*Completed: 2026-11-07*
