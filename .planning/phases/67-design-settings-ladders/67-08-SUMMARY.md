---
phase: 67-design-settings-ladders
plan: "08"
subsystem: verification-diagnostics
tags: [pinn, exp02, depth-ladder, prospective-registration, timing-rows, ac-gate]

# Dependency graph
requires:
  - phase: 67-design-settings-ladders (67-06, 67-07)
    provides: the thirteen diagnostic_phase67 commands, the bounded launch supervisor, the remaining-window power primitive, and the pinned 41-file harness freeze
provides:
  - Committed EXP-02 scientific design, metadata registration and one guarded TRAIN metadata capture (both Stage0 systems 1632 and 851, independently verified gold-grid hashes and same-window expectations)
  - Committed prospective timing matrix and all 15 arm/case timing registrations (3 cases x 5 depth arms, N1200/warmup200/measured1000, 900-second whole-launch cap) with every code dependency pinned to live bytes
  - Halt state: all 15 timing rows and the derived budget/science-registration work are deferred, unstarted, with zero burned directories
affects: [67-09, 67-10, 67-11, 67-12, 67-13, 67-14, 67-15, 67-16]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
actuals:
  tokens: 49083        # chars/4 over the realized diff 75424795^..c6dfb15c (196332 bytes)
  tasks: 2              # tasks 67-08-01 and 67-08-02 complete; 67-08-03 deferred unstarted
  commits: 7            # 75424795, 73bcbc74, 9106f40b, 41095975, c9c994eb, e2a3a380, c6dfb15c

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Re-pin convention for pre-launch spec changes: re-pin harness-freeze.json to the live file digests, re-pin the manifest digest in every registration that names it (harness_freeze and code_dependencies), commit, then re-run the check commands (mirrors 41095975)."
    - "Row declarations must carry the variant's nominal window length (window_length), never the observed gold grid's float64 endpoint."

key-files:
  created:
    - .planning/phases/67-design-settings-ladders/67-EXP02-TIMING-PREDICTION.md
    - .planning/phases/67-design-settings-ladders/evidence/exp02/design.json
    - .planning/phases/67-design-settings-ladders/evidence/exp02/metadata-registration.json
    - .planning/phases/67-design-settings-ladders/evidence/exp02/metadata/record.json
    - .planning/phases/67-design-settings-ladders/evidence/exp02/metadata/attempt.json
    - .planning/phases/67-design-settings-ladders/evidence/exp02/metadata/power-gate.json
    - .planning/phases/67-design-settings-ladders/evidence/exp02/timing-matrix.json
    - .planning/phases/67-design-settings-ladders/evidence/exp02/timing/CASE/ARM/registration.json (15 rows)
  modified:
    - pinn/verification/diagnostic_phase67_execution.py (t_end deviation fix)
    - tests/phase67/test_pages.py (regression test)
    - .planning/phases/67-design-settings-ladders/evidence/harness-freeze.json (re-pinned twice)
    - .planning/STATE.md, .planning/ROADMAP.md, .planning/WINDOWS.md

key-decisions:
  - "Timing/science rows declare the variant's nominal window length (float(declaration.window_length) = 10.0 for the full-window arms), never the observed gold-grid float64 endpoint 9.999999999999831; exp05 keeps the observed prefix endpoint because its variants are prefixes (deviation fix e2a3a380, regression test in tests/phase67/test_pages.py)."
  - "Pre-launch registration re-pins follow the 41095975 amendment convention: after a legitimate harness change with no launch yet, re-pin harness-freeze.json and every registration's harness_freeze/code_dependencies digests; register-timing's exclusive write refuses regeneration, so the hand re-pin is the sanctioned path (c6dfb15c)."
  - "The owner-authorized one-shot weekday amendment (73bcbc74) admits weekday launches only before 2026-11-04 07:30 America/Chicago, and that deadline is also the closing instant of the remaining-window check."
  - "Task 67-08-03 deferred at the designed AC-power admission gate: launch-row refused with 'the Mac is not on AC power; pmset reports Battery Power' before any protected work; the row is unstarted and nothing is burned; per the plan's deferral rule an unavailable power window defers an unstarted row without creating an attempt."

patterns-established:
  - "Deviation fix + mandatory re-pin chain: fix harness, add regression test, regenerate affected declarations, re-pin freeze manifest, re-pin manifest digests in registrations, commit, re-run check-design/check-metadata/check-matrix."

requirements-completed: []  # EXP-02 remains open: the depth-ladder measurement (15 timing rows) and the derived budget/science registrations are deferred; see Issues Encountered.

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "EXP-02 complete scientific design and metadata registration committed before any real metadata or timing access (depths 2/4/6/8/12 on width256/o30/raw14/lr1e-4/[0,10], contrasts, reading branches, 900-second metadata cap, frozen dependency digests)"
    requirement: EXP-02
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-design --experiment exp02 (PHASE67-DESIGN-OK at 75424795)"
        status: pass
    human_judgment: false
  - id: D2
    description: "One guarded TRAIN-only metadata capture for systems 1632 and 851 with independently verified full-window gold-grid hashes, sample counts, coordinates, window-mean constant and two-Kepler applicability; receipt committed before timing registration"
    requirement: EXP-02
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-metadata --experiment exp02 (PHASE67-METADATA-OK, re-verified 2026-11-03 after the deviation fix)"
        status: pass
    human_judgment: false
  - id: D3
    description: "Prospective timing matrix and all 15 case-major timing registrations committed before any timing launch, every code dependency pinned to live bytes, each row N1200/warmup200/measured1000/similarity 0-300-600-900-1200/score 600-900-1200/900-second cap"
    requirement: EXP-02
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-matrix --experiment exp02 --kind timing (PHASE67-MATRIX-OK, re-verified 2026-11-03 after the re-pin)"
        status: pass
    human_judgment: false
  - id: D4
    description: "15 serial timing rows measured and committed, then the cost-only common science budget, prediction page, science-matrix and 15 science registrations (no science launch)"
    requirement: EXP-02
    verification: []
    human_judgment: true
    rationale: "NOT DONE - deferred at the designed AC-power admission gate (battery power; refusal before any protected work, zero attempts created). Resume procedure in Next Phase Readiness; the halt is resolved and re-summarized when the rows complete."

# Metrics
duration: ~2h20m active execution (predecessor 12:00-14:00 continuation interrupted by provider limit; this session 14:05-16:25 America/Chicago, including ~2h of AC-power polling)
completed: 2026-11-03
status: halted
---

# Phase 67 Plan 08: EXP-02 Depth Ladder Pre-Registration, Calibration and Budget Summary

**EXP-02's complete scientific design, one clean TRAIN metadata capture and all 15 prospective timing registrations are committed with live-byte dependency pins; the 15-row measurement itself is deferred unstarted at the designed AC-power admission gate (Mac on battery, zero attempts created, window open until 2026-11-04 07:30 America/Chicago).**

## Performance

- **Duration:** ~2h20m active (this continuation session 14:05-16:25 America/Chicago; the predecessor's 12:00-14:00 session was interrupted by a provider concurrency limit)
- **Started:** 2026-11-03 ~12:00 America/Chicago (predecessor), resumed 14:05
- **Completed:** 2026-11-03 16:25 America/Chicago (halted close-out)
- **Tasks:** 2 of 3 complete; task 67-08-03 deferred unstarted
- **Files modified:** 31 across the plan's commits (+~4612 lines, mostly the machine-written matrix and registrations)

## Accomplishments

- Task 67-08-01: the complete EXP-02 design, metadata registration and 67-EXP02-TIMING-PREDICTION.md committed at 75424795 (check-design PHASE67-DESIGN-OK).
- Owner-authorized one-shot weekday amendment committed at 73bcbc74: weekday launches admitted only before 2026-11-04 07:30 America/Chicago; that deadline is also the closing instant of the remaining-window check.
- Task 67-08-02: the guarded TRAIN metadata capture receipt committed at 9106f40b; the receipt-window audits single-sourced the amended rule at 41095975; the timing matrix and all 15 timing registrations committed at c9c994eb.
- Deviation fix (this session): rows now declare the variant's nominal window length, with regression test, regenerated matrix/registrations, and the full freeze re-pin chain (e2a3a380); the 15 registrations' stale harness pins re-pinned (c6dfb15c).
- Both task-2 verify gates re-verified clean after the fix: PHASE67-METADATA-OK and PHASE67-MATRIX-OK.
- Suites at the final code commit: phase65 204 OK, phase66 101 OK, phase67 244 OK.

## Task Commits

1. **Task 67-08-01 (predecessor): design** - `75424795` (evidence)
2. **Amendment (predecessor, owner-authorized): weekday deadline** - `73bcbc74` (spec)
3. **Task 67-08-02 (predecessor): metadata receipt** - `9106f40b` (evidence)
4. **Task 67-08-02 (predecessor): receipt-window audits** - `41095975` (spec)
5. **Task 67-08-02 (predecessor): timing matrix + registrations** - `c9c994eb` (evidence)
6. **Deviation fix (this session): declared window = variant length** - `e2a3a380` (fix)
7. **Re-pin (this session): registrations to the amended harness** - `c6dfb15c` (fix)

**Plan metadata:** the final `docs(67-08)` commit carries this SUMMARY, STATE.md, ROADMAP.md and WINDOWS.md.

## Files Created/Modified
- `.planning/phases/67-design-settings-ladders/67-EXP02-TIMING-PREDICTION.md` - committed scientific design, exact contrast identities and reading branches
- `.planning/phases/67-design-settings-ladders/evidence/exp02/design.json` - the frozen design document
- `.planning/phases/67-design-settings-ladders/evidence/exp02/metadata-registration.json` + `metadata/{record,attempt,power-gate}.json` - the registered and captured TRAIN metadata
- `.planning/phases/67-design-settings-ladders/evidence/exp02/timing-matrix.json` + `timing/{main-1632-s42,repeat-851-s42,repeat-1632-s41}/{d2,d4,d6,d8,d12}/registration.json` - the 15 prospective row registrations (t_end 10.0, live-byte pins)
- `pinn/verification/diagnostic_phase67_execution.py` - declared_t_end = float(declaration.window_length) for full-window experiments; exp05 keeps the observed prefix endpoint
- `tests/phase67/test_pages.py` - test_the_declared_window_is_the_variant_length_not_the_grid_endpoint
- `.planning/phases/67-design-settings-ladders/evidence/harness-freeze.json` - re-pinned to the amended harness (28896b3c...) in e2a3a380; manifest digest df16b296...

## Decisions Made
- The declared row window is the variant's nominal window length (the locked [0,10] = 10.0), never the observed grid's float64 endpoint: the settings door requires declared endpoint == variant window length, matching Phase 66's committed real registrations. exp05 is exempt because its variants are exact prefixes.
- Pre-launch re-pins follow the 41095975 convention (register-timing's exclusive write refuses replacement once files exist, so the hand re-pin plus commit is the sanctioned path while no launch has occurred).
- The deferral follows the plan's own rule: "an unavailable weekend defers an unstarted row" — extended here to the AC-power unavailability that gates every launch; nothing was retried, no directory created, no code modified to bypass the gate.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Rows declared the observed grid endpoint instead of the variant's window length**
- **Found during:** Task 67-08-02 (predecessor, mid-flight at interruption; verified and committed this session)
- **Issue:** phase67_run_matrix stamped t_end 9.999999999999831 (the observed gold-grid float64 endpoint) into the timing rows and registrations; the settings door requires the declared endpoint to equal the variant's window length (10.0, as Phase 66's committed real registrations declare), so admission would refuse every row.
- **Fix:** declared_t_end = float(declaration.window_length) for full-window experiments (exp05 keeps the observed prefix endpoint); regression test added; matrix and all 15 registrations regenerated to t_end 10.0; harness freeze re-pinned (7c8a4f09.. -> 28896b3c..) and the metadata registration's manifest digest re-pinned (884bf217.. -> df16b296..), mirroring the 41095975 chain.
- **Files modified:** pinn/verification/diagnostic_phase67_execution.py, tests/phase67/test_pages.py, timing-matrix.json, 15 timing registration.json files, harness-freeze.json, metadata-registration.json
- **Verification:** new regression test passes; phase65 204 OK, phase66 101 OK, phase67 244 OK; check-metadata PHASE67-METADATA-OK
- **Committed in:** e2a3a380

**2. [Rule 3 - Blocking] Stale harness pins inside the committed timing registrations refused check-matrix**
- **Found during:** Task 67-08-02 close-out (this session)
- **Issue:** the 15 registrations were stamped by register-timing while the harness was at 7c8a4f09..; after the deviation fix the fit door refuses each row ("registration artifact changed since it was committed"). register-timing cannot be re-run because _exclusive_json_write refuses existing artifacts.
- **Fix:** re-pinned each registration's diagnostic_phase67_execution.py code_dependency to the live 28896b3c.. and harness_freeze to df16b296..; all 13 code dependencies per registration verified against live bytes; no other field touched.
- **Files modified:** the 15 timing registration.json files
- **Verification:** check-matrix --experiment exp02 --kind timing = PHASE67-MATRIX-OK; check-metadata = PHASE67-METADATA-OK
- **Committed in:** c6dfb15c

---

**Total deviations:** 2 auto-fixed (1 bug, 1 blocking)
**Impact on plan:** both fixes were required for the settings door to admit any row; the declarations now match the settings door exactly, with the freeze chain consistent end to end.

## Issues Encountered

- **AC-power admission refusal halted task 67-08-03 at row 1.** launch-row main-1632-s42/d2 refused with "the Mac is not on AC power; pmset reports 'Battery Power'" (100%, discharging) before any protected work. pmset was polled from 14:17 to 16:20 America/Chicago (~2 hours): no AC return; the Mac also idled to sleep during the wait. Per the plan's deferral rule the row is unstarted and deferred without an attempt; nothing was burned, and no code was modified to bypass the gate. The amendment window (weekday launches before 2026-11-04 07:30 America/Chicago) remains open, so a resume after the Mac is plugged in can still run all 15 rows.
- A stray `caffeinate -i -t 300` timer from the predecessor self-expired; no diagnostic process was left running (verified with ps).

## Known Stubs
None - no stubs, placeholders or unwired data paths were introduced. The deferred rows are registered prospective artifacts awaiting launch, not stubs.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- **Resume procedure for task 67-08-03 (unchanged plan text):** with the Mac on AC power, resume the 15-row serial sequence exactly per the plan - for each row in case-major order (main-1632-s42, repeat-851-s42, repeat-1632-s41 x d2, d4, d6, d8, d12): check-matrix --kind timing, launch-row (once), check-row, inspect scoped evidence, commit that row's record/attempt/power-gate/diagnostic.weights before the next launch. Then budget (Plan04 algorithm verbatim), commit budget.json + 67-EXP02-BUDGET.md + 67-EXP02-PREDICTION.md + science-matrix.json + all 15 science registrations, and require check-budget PHASE67-BUDGET-OK and check-matrix --kind science PHASE67-MATRIX-OK. No science run may start.
- **State:** all completed boundaries are committed; the working tree holds no phase-67 evidence in flight; the halt is machine-read via this SUMMARY's `status: halted` and the WINDOWS ledger (entries 3 and 4).
- **Concern:** if AC is not restored before 2026-11-04 07:30 America/Chicago, the amendment deadline closes the weekday window; the rows then wait for the next weekend AC window (Sunday 22:00 America/Chicago closing rule) and this plan's halt persists until the rows complete.

---
*Phase: 67-design-settings-ladders*
*Completed: 2026-11-03 (halted at the AC gate; tasks 1-2 complete)*
