---
phase: 67-design-settings-ladders
plan: "12"
subsystem: verification-diagnostics
tags: [pinn, exp04, time-input-ladder, pre-registration, timing-rows, serial-launch, budget, science-registrations]

# Dependency graph
requires:
  - phase: 67-design-settings-ladders (67-11)
    provides: the owner's committed SCOPE-49 ruling (eab52f7d, authorize-recorded-proposal; PHASE67-REVIEW-OK) unblocking EXP-04 under its existing committed registration
provides:
  - The committed EXP-04 time-input-ladder scientific design (67-EXP04-TIMING-PREDICTION.md, design.json, metadata-registration.json): raw14 vs fundamental-encoding16 vs fundamental-plus-second-harmonic-encoding18 on both required backbones, exact contrasts/controls, five similarity events, three frozen-score events, no automatic continuation, and the confirmatory/unsettled/mechanical reading branches fixed prospectively (tasks 1-2 executed by the predecessor executor: ffd80b7b, d5d6f17c)
  - One guarded TRAIN-only metadata capture for both registered Stage0 systems (1632 and 851) with census N_in, f=N_in/10 cycles, phase2*pi*f*t identity and strictly-sub-pi maximum adjacent feature-phase increment, plus the committed 18-row timing matrix and every timing row registration before any launch (aaace25f)
  - All 18 EXP-04 timing rows measured serially (each launched exactly once at N=1200 under the 900-second whole-launch cap, PHASE67-ROW-OK, committed as four artifacts before the next launch) — the experiment's own cost basis, no Phase65/66 rate borrowed
  - The derived cost-only Plan04 budget (common N=112700 optimizer steps; worst-row projection 2653.94 s against the 2655 s = 0.75 x 3540 s science cap; experiment projection 25880.3 s) with the frozen prediction page, the 18-row science matrix and every science registration committed BEFORE any science launch — no science run has started (4c8b7b25)
affects: [67-13, 67-14, 67-15, 67-16]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
# Scale caveat: the realized diff is dominated by machine-written evidence
# (18 run records ~16k lines each plus the 18-row registrations and the two
# frozen pages), not agent-authored text; the two harness fixes each also
# re-pin the 81 live registrations (+161 digest lines).
actuals:
  tokens: 2197529     # chars/4 over the realized text diff 88d17045^..HEAD (8,790,114 bytes; weights binaries excluded)
  tasks: 3            # 67-12-01, 67-12-02, 67-12-03 — all executed (tasks 1-2 by the predecessor executor before its usage-cap death)
  commits: 27         # amendment 88d17045 + ffd80b7b, d5d6f17c, aaace25f, 04c50346, 478141c7, ee2cf509 (predecessor) + 20 this continuation (2 fixes, 17 rows, budget boundary)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Continuation resume over a usage-cap death: an on-disk complete-but-uncommitted row is never relaunched — check-row (value-free) first, then commit exactly as prior rows; the exclusive first-write evidence identity stays intact."
    - "Serial timing campaign: per row, check-matrix -> AC/window/no-other-run eligibility -> previous row verified committed -> launch-row exactly once -> check-row (scores hidden) -> cost-only inspection -> commit the row's four files before the next launch; the whole loop inside a session-level caffeinate wake lock on top of the per-launch caffeinate."
    - "Freeze-chain re-pin convention (now 7290bf58/ed93f359/88d17045/ee2cf509/3d640feb/4ea20b05): a harness fix moves its module digest and the manifest digest, and every live registration re-pins both digest fields in the same commit; run evidence keeps its as-captured citations and the reader verifies them against committed history."

key-files:
  created:
    - .planning/phases/67-design-settings-ladders/evidence/exp04/timing/CASE/ARM/{record.json,attempt.json,power-gate.json,diagnostic.weights} (18 rows; row 1 by the predecessor, rows 2-18 this continuation)
    - .planning/phases/67-design-settings-ladders/evidence/exp04/budget.json
    - .planning/phases/67-design-settings-ladders/evidence/exp04/science-matrix.json
    - .planning/phases/67-design-settings-ladders/evidence/exp04/science/CASE/ARM/registration.json (18 rows)
    - .planning/phases/67-design-settings-ladders/67-EXP04-BUDGET.md
    - .planning/phases/67-design-settings-ladders/67-EXP04-PREDICTION.md
  modified:
    - pinn/verification/diagnostic_fit.py (as-captured citation admission; 3d640feb)
    - pinn/verification/diagnostic_phase67_records.py (orbit-aware matrix-row binding; 4ea20b05)
    - tests/phase67/test_records.py (6 regression tests)
    - .planning/phases/67-design-settings-ladders/evidence/harness-freeze.json + 81 live registrations (two freeze-chain re-pins)
    - .planning/STATE.md, .planning/ROADMAP.md, .planning/state.json, .planning/agent-history.json

key-decisions:
  - "Every real attempt stayed serial, single-use, TRAIN-only and supervised: 17 launches this continuation (rows 2-18) plus the predecessor's row-1 launch, each exactly once through the guarded launcher on AC power inside the weekend window (POWER-OK AC Power; row 2 on Friday 18:02 CST under the amendment bridge, rows 3-18 on Saturday 11:22-11:58 CST), each complete 1200-step attempt published under the 900-second cap; zero retries, zero reused directories, no timing E value ever screened (check-row's value-free audit was the only per-row verdict)."
  - "Two reader false-refusals on faithful evidence were fixed as harness defects under the dispatch's prescribed fix protocol, with the evidence bytes untouched: (1) the as-captured registration citation after the ee2cf509 re-pin made the citation check a catch-22 (the re-pinned bytes fail the record's citation, the as-captured bytes fail admission's live-digest check) — fixed by admitting the current sha or the registration's exact bytes at a commit in HEAD's history (3d640feb); (2) the static arm table could never bind exp04's orbit-specific 851 encoded declarations (D-09) — fixed by resolving the expected variant through phase67_arm_variant with the row's declared orbit, exactly as the launch gate does, keeping the static declaration as the base case for orbits with no materialized registration (4ea20b05). Both fixes carry regression tests, both re-pinned the freeze chain per convention, and no registered design, prediction, setting or pass bar changed."
  - "The cost-only budget is derived from this experiment's own 18 measured timing rows (Plan04 verbatim): the largest common N in 100-step quanta is 112700 optimizer steps (112500 measured + 200 warmup), where the worst row (locked-f12 on the 851 system, 0.018761 s/step) projects 2653.94 s — one 100-step quantum higher would breach the 2655 s science cap; the 18-run science experiment projects 25880.3 s. Every science row is registered prospectively at that one common N with the normalized cadence [0, 28175, 56350, 84525, 112700] and score cadence [56350, 84525, 112700], cap 3540 s, and the original full contrast/repeat rule; no admissible-N refusal occurred and no arm was rescued."

patterns-established:
  - "A freeze-chain re-pin between a run's capture and its commit boundary is survivable without touching evidence: the reader admits the as-captured citation against the registration's committed history, so the convention's 'verifiable at its introducing commit' invariant holds even when the introducing commit lands after a re-pin."

requirements-completed: []  # EXP-04 stays open until the phase verification act: every 67-0N plan declares EXP-02..05 and the marks flip only when all declaring plans finish (shared-ID gate, 67-04/67-08 convention).

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "The committed design, metadata capture and 18-row timing matrix precede every real attempt; all 18 timing rows launched exactly once, serially, at N=1200 under the 900-second whole-launch cap on AC power inside the owner's window, each mechanically checked with scores hidden and committed as four artifacts before the next launch"
    requirement: EXP-04
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-row per row (17x PHASE67-ROW-OK this continuation after the two reader fixes, row 1 PHASE67-ROW-OK under its predecessor) and check-matrix --kind timing (PHASE67-MATRIX-OK) before each launch"
        status: pass
    human_judgment: false
  - id: D2
    description: "The cost-only budget derived from all 18 committed timing rows (no Phase65/66 rate, no score influence), and all 18 science rows registered prospectively at the one common N with measured overhead before any science launch; no science run has started"
    requirement: EXP-04
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-budget --experiment exp04 (PHASE67-BUDGET-OK) and check-matrix --experiment exp04 --kind science (PHASE67-MATRIX-OK) at the committed boundary 4c8b7b25"
        status: pass
    human_judgment: false

# Metrics
duration: ~15h10m wall across two executor sessions (predecessor: design/metadata/matrix + row-1 launch 2026-11-06 afternoon, died on a provider usage cap 18:09 CST after the float32 reader fix ee2cf509; this continuation: 2026-11-07 ~10:50-12:05 CST — row-2 verify+commit, two reader fixes with suites, rows 3-18, budget, science freeze, close-out; ~7 min of it the 17 supervised launches)
completed: 2026-11-07
status: complete
---

# Phase 67 Plan 12: EXP-04 Time-Input Ladder Pre-Registration — Timing & Budget Summary

**All 18 EXP-04 timing rows ran serially at N=1200 under the 900-second cap (each launched exactly once, PHASE67-ROW-OK, committed before the next launch), the cost-only Plan04 budget is derived from those measured rows (common N=112700; worst-row projection 2653.94 s vs the 2655 s science cap; experiment projection 25880.3 s), and the science prediction page, science matrix and all 18 science registrations are committed before any science launch — no science run has started. Two reader false-refusals on faithful evidence (the as-captured citation after a re-pin; the static arm binding vs D-09's orbit-specific 851 variants) were fixed as harness defects with regression tests and freeze-chain re-pins, the evidence bytes untouched.**

## Performance

- **Duration:** predecessor executor 2026-11-06 ~09:00-18:09 CST (design ffd80b7b, metadata receipt d5d6f17c, 18-row timing matrix aaace25f, launch-admission ruling fix 04c50346, row-1 commit 478141c7, float32 reader fix ee2cf509; died on a provider usage cap with row 2 complete on disk but uncommitted); this continuation 2026-11-07 ~10:50-12:05 CST (row-2 verify+commit through budget/science-freeze/close-out)
- **Tasks:** 3 executed (tasks 1-2 by the predecessor, task 3 split across both sessions)
- **Files:** 74 evidence/page files created this continuation (68 row artifacts + budget.json + science-matrix.json + 18 science registrations + 2 pages) plus 6 regression tests, 2 reader fixes and 2 freeze-chain re-pins

## Accomplishments

- Row 2 (main-1632-s42/locked-f1) was recovered exactly as the continuation protocol requires: the predecessor's launch had completed on disk inside the window (POWER-OK AC Power isoweekday=5 at 18:02 CST, attempt published); this continuation verified it read-only and committed the four artifacts (14b4651c) without any relaunch — but only after fixing the reader defect that its mechanical check had tripped (below).
- Rows 3-18 ran with zero gate refusals: per row check-matrix (PHASE67-MATRIX-OK) -> AC/window admission (POWER-OK AC Power, isoweekday=6 Saturday 11:22-11:58 CST) -> launch-row exactly once -> check-row PHASE67-ROW-OK -> commit the row's four files before the next launch. Case-major order main-1632-s42 (rows 3-6), repeat-851-s42 (rows 7-12), repeat-1632-s41 (rows 13-18), arms in the declared order.
- The budget step froze the science state in one boundary (4c8b7b25): budget.json (common N=112700, per-row projections, phase ledger updated to 25880.3 s planned), the immutable 67-EXP04-PREDICTION.md, the cost page 67-EXP04-BUDGET.md, science-matrix.json and all 18 prospective science registrations. Task verifies: PHASE67-BUDGET-OK and PHASE67-MATRIX-OK (science), on top of the standing PHASE67-DESIGN-OK, PHASE67-METADATA-OK and PHASE67-MATRIX-OK (timing).
- A session-level caffeinate wake lock (caffeinate -i -s -t 40000) was held across the whole gated continuation on top of the per-launch caffeinate; the machine stayed on AC power throughout.

## Task Commits

1. **Task 67-12-01 design (predecessor executor)** - ffd80b7b (evidence) - 67-EXP04-TIMING-PREDICTION.md + design.json + metadata-registration.json; PHASE67-DESIGN-OK.
2. **Task 67-12-02 metadata + timing registrations (predecessor executor)** - d5d6f17c (guarded metadata capture receipt), aaace25f (18-row timing-matrix registrations); PHASE67-METADATA-OK, PHASE67-MATRIX-OK. Predecessor fixes en route: 04c50346 (dependent-launch admission per the committed owner ruling), ee2cf509 (float32 encoder cycles in the record reader, +2 regression tests, freeze re-pin).
3. **Row 1 (predecessor executor)** - 478141c7 (evidence) - main-1632-s42/locked-raw.
4. **As-captured citation fix (this continuation)** - 3d640feb (fix) - diagnostic_fit.py + 2 regression tests + freeze re-pin (fit digest 97c459b6->b336503d, manifest d7f7d9e1->76255d5c, 81 registrations).
5. **Rows 2-7 (this continuation)** - 14b4651c (locked-f1, the recovered on-disk row), df4cad80 (locked-f12), d1c8e169 (exp01-raw), a8de809e (exp01-f1), e70b5889 (exp01-f12), 75b57a65 (repeat-851-s42/locked-raw).
6. **Orbit-aware binding fix (this continuation)** - 4ea20b05 (fix) - diagnostic_phase67_records.py + 4 regression tests + freeze re-pin (records digest d13da3ba->920ad300, manifest 76255d5c->9dd440c7, 81 registrations).
7. **Rows 8-18 (this continuation)** - 08b9f358 (locked-f1-851), 7129d8cd (locked-f12-851), 98705924 (exp01-raw-851), 20005061 (exp01-f1-851), a5802c8f (exp01-f12-851), 61c6606a (repeat-1632-s41/locked-raw), d4f4a730 (locked-f1), ec7bd19c (locked-f12), 251c5a2d (exp01-raw), d272c7c1 (exp01-f1), 63f45c69 (exp01-f12, the final row).
8. **Budget + science freeze (this continuation)** - 4c8b7b25 (evidence) - budget.json, both pages, science-matrix.json, 18 science registrations; PHASE67-BUDGET-OK, PHASE67-MATRIX-OK (science).
9. **Plan close-out:** this docs commit (SUMMARY + STATE/ROADMAP/state.json/agent-history).

## Files Created/Modified

- `evidence/exp04/timing/{main-1632-s42,repeat-851-s42,repeat-1632-s41}/{locked-raw,locked-f1,locked-f12,exp01-raw,exp01-f1,exp01-f12}/` - 18 rows x (record.json, attempt.json, power-gate.json, diagnostic.weights)
- `evidence/exp04/budget.json`, `evidence/exp04/science-matrix.json`, `evidence/exp04/science/CASE/ARM/registration.json` (18), `67-EXP04-BUDGET.md`, `67-EXP04-PREDICTION.md` - the cost-only budget and the frozen prospective science state
- `pinn/verification/diagnostic_fit.py`, `pinn/verification/diagnostic_phase67_records.py`, `tests/phase67/test_records.py` - the two reader fixes with 6 regression tests
- `evidence/harness-freeze.json` + the 81 live exp02/exp03/exp04 registrations - two freeze-chain re-pins (digest fields only)
- `.planning/STATE.md`, `.planning/ROADMAP.md`, `.planning/state.json`, `.planning/agent-history.json` - plan tracking

## Decisions Made

- No scientific value was screened during the run loop: check-row's value-free mechanical audit was the only per-row verdict, per-row inspection touched cost fields only (attempt status, power source, wall/rate), and no row or repeat was selected, extended or reordered after any result.
- The two reader false-refusals were treated as harness defects under the dispatch's prescribed new-defect protocol (minimal fix + regression tests + freeze-chain re-pin + fix(67-12) commit), NOT as burned rows: in both cases the run was launched faithfully through the guarded gate and the record was content-clean against the committed registration in every respect but the refused binding — the sole failing checks were provably over-strict against evidence the committed convention explicitly protects ("run evidence keeps its as-captured citations"; the launch gate's own orbit-aware D-09 resolution). Row directories stayed untouched until their mechanical checks passed; relaunching was never considered.
- The budget derivation accepted the tool's Plan04 output verbatim (N=112700 with the worst row 1.06 s under the cap); no admissible-N refusal occurred, so no resource refusal needed reporting and no arm was rescued or cap relaxed.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] The registration citation check could not admit as-captured bytes after a freeze-chain re-pin**
- **Found during:** Task 67-12-03 (row 2's post-fix check-row)
- **Issue:** verify_fit_result compared the record's registration citation against the current on-disk bytes only; the ee2cf509 freeze-chain re-pin had moved the registration bytes between row 2's capture (18:03 CST) and its commit boundary, and the as-captured bytes could never re-admit either (their declared records.py digest predates the fix) — a catch-22 that made the row's mechanical check permanently unpassable and retroactively broke check-row for every pre-re-pin row of every experiment.
- **Fix:** _cites_registration_bytes admits the current sha or the registration file's exact bytes at a commit in HEAD's history; two regression tests (as-captured admits after a committed re-pin; another path's committed bytes refuse); freeze re-pin in the same commit.
- **Files modified:** pinn/verification/diagnostic_fit.py, tests/phase67/test_records.py, harness-freeze.json, 81 registrations
- **Commit:** 3d640feb

**2. [Rule 2 - Missing critical functionality] The matrix-row arm binding could not resolve D-09's orbit-specific 851 encoded variants**
- **Found during:** Task 67-12-03 (row 8's check-row)
- **Issue:** _matrix_row_problems resolved the expected variant through the static PHASE67_ARMS table, which only names the 1632 declarations; exp04's encoded arms are the first case-dependent variants (the launch gate resolves them orbit-aware through phase67_arm_variant, D-09), so every 851 encoded row's faithful run could never pass its mechanical check (the run's registered exp04-locked-f1-851 was refused as "not the matrix row's arm").
- **Fix:** the row binding resolves through phase67_arm_variant with the row's declared orbit, exactly as the launch gate does; an orbit with no materialized registration keeps the static declaration as the reader's base case (the launch gate still refuses such launches); four regression tests; freeze re-pin in the same commit.
- **Files modified:** pinn/verification/diagnostic_phase67_records.py, tests/phase67/test_records.py, harness-freeze.json, 81 registrations
- **Commit:** 4ea20b05

## Issues Encountered

- The predecessor executor died on a provider usage cap right after committing the float32 reader fix (ee2cf509, 18:09 CST) and before row 2's commit; state at this continuation's start was verified by the orchestrator (HEAD ee2cf509) and row 2 was recovered as described above.
- Row 3's commit body (df4cad80) says "row 4 of the declared matrix order" — a prose off-by-one; the subject, case/arm and artifacts are correct and the message was left unamended (history rewrite is forbidden).
- The torch requires_grad UserWarning at diagnostic_fit.py:831 appears in every launch log; it is pre-existing, informational and outside the harness freeze (also recorded by 67-11).

## Known Stubs

None - every row artifact, the budget, the science matrix and the registrations are complete machine-generated evidence; no placeholder or unwired value exists.

## Next Phase Readiness

- EXP-04's science campaign (67-13 and onward per the roadmap's wave order) launches against the committed science matrix: 18 rows at the common N=112700, cap 3540 s, experiment projection 25880.3 s, review and scope handling per the plan's registered reading branches.
- No held-out evaluation was spent, no source symbol/flag/scoring bar/package was added, and every historical byte (including both pre-fix registrations' as-captured citations) is preserved.

## Self-Check: PASSED

All created evidence/page files exist on disk (18 timing rows x 4 artifacts beside their committed registrations, budget.json, science-matrix.json, 18 science registrations, both pages, this SUMMARY); all 27 plan commits exist in history (88d17045, ffd80b7b, d5d6f17c, aaace25f, 04c50346, 478141c7, ee2cf509, 3d640feb, 14b4651c, df4cad80, d1c8e169, a8de809e, e70b5889, 75b57a65, 4ea20b05, 08b9f358, 7129d8cd, 98705924, 20005061, a5802c8f, 61c6606a, d4f4a730, ec7bd19c, 251c5a2d, d272c7c1, 63f45c69, 4c8b7b25); all five gates ran green at the committed state (PHASE67-DESIGN-OK, PHASE67-METADATA-OK, PHASE67-MATRIX-OK timing, PHASE67-BUDGET-OK, PHASE67-MATRIX-OK science); the three suites ran green at the settled bytes (phase65 204 OK, phase66 101 OK, phase67 256 OK).
