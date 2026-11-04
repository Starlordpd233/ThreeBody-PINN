---
phase: 67-design-settings-ladders
plan: "08"
subsystem: verification-diagnostics
tags: [pinn, exp02, depth-ladder, prospective-registration, timing-rows, ac-gate, cost-only-budget]

# Dependency graph
requires:
  - phase: 67-design-settings-ladders (67-06, 67-07)
    provides: the thirteen diagnostic_phase67 commands, the bounded launch supervisor, the remaining-window power primitive, and the pinned 41-file harness freeze
provides:
  - Committed EXP-02 scientific design, metadata registration and one guarded TRAIN metadata capture (both Stage0 systems 1632 and 851, independently verified gold-grid hashes and same-window expectations)
  - All 15 measured, checked and individually committed timing rows (3 cases x 5 depth arms at N1200/warmup200/measured1000 under the 900-second cap, zero retries, zero refusals)
  - The measured cost-only common science budget N=152900 (largest 100-step quantum with every projection <= 0.75*3540 s), the budget/prediction pages, science-matrix.json and all 15 science registrations — no science run started
affects: [67-09, 67-10, 67-11, 67-12, 67-13, 67-14, 67-15, 67-16]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
# Scale caveat: the realized diff is dominated by 15 machine-written timing records
# (~251k JSON insertions of loss-trace/similarity evidence), not agent-authored text.
# Agent-authored content (pages, receipts, registrations) is a small fraction of it.
actuals:
  tokens: 1801903       # chars/4 over the realized diff 75424795^..652d1a9d (7207612 bytes, text files only, weights binaries excluded)
  tasks: 3              # 67-08-01, 67-08-02 (predecessor) + 67-08-03 (this resume)
  commits: 25           # 8 predecessor (through e2ebda79) + 15 row commits + 1 budget commit + 1 final docs commit

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Re-pin convention for pre-launch spec changes: re-pin harness-freeze.json to the live file digests, re-pin the manifest digest in every registration that names it (harness_freeze and code_dependencies), commit, then re-run the check commands (mirrors 41095975)."
    - "Row declarations must carry the variant's nominal window length (window_length), never the observed gold grid's float64 endpoint."
    - "Resume-after-power-halt: a designed gate refusal leaves zero burned directories, so the resume replays the declared row order unchanged with a wake assertion (caffeinate -i) covering the inter-row gaps; every row is committed before the next launch."

key-files:
  created:
    - .planning/phases/67-design-settings-ladders/67-EXP02-TIMING-PREDICTION.md
    - .planning/phases/67-design-settings-ladders/evidence/exp02/design.json
    - .planning/phases/67-design-settings-ladders/evidence/exp02/metadata-registration.json
    - .planning/phases/67-design-settings-ladders/evidence/exp02/metadata/record.json
    - .planning/phases/67-design-settings-ladders/evidence/exp02/metadata/attempt.json
    - .planning/phases/67-design-settings-ladders/evidence/exp02/metadata/power-gate.json
    - .planning/phases/67-design-settings-ladders/evidence/exp02/timing-matrix.json
    - .planning/phases/67-design-settings-ladders/evidence/exp02/timing/CASE/ARM/{registration,record,attempt,power-gate}.json + diagnostic.weights (15 rows)
    - .planning/phases/67-design-settings-ladders/evidence/exp02/budget.json
    - .planning/phases/67-design-settings-ladders/67-EXP02-BUDGET.md
    - .planning/phases/67-design-settings-ladders/67-EXP02-PREDICTION.md
    - .planning/phases/67-design-settings-ladders/evidence/exp02/science-matrix.json
    - .planning/phases/67-design-settings-ladders/evidence/exp02/science/CASE/ARM/registration.json (15 rows)
  modified:
    - pinn/verification/diagnostic_phase67_execution.py (t_end deviation fix)
    - tests/phase67/test_pages.py (regression test)
    - .planning/phases/67-design-settings-ladders/evidence/harness-freeze.json (re-pinned twice)
    - .planning/STATE.md, .planning/ROADMAP.md, .planning/WINDOWS.md

key-decisions:
  - "Timing/science rows declare the variant's nominal window length (float(declaration.window_length) = 10.0 for the full-window arms), never the observed gold-grid float64 endpoint 9.999999999999831; exp05 keeps the observed prefix endpoint because its variants are prefixes (deviation fix e2a3a380, regression test in tests/phase67/test_pages.py)."
  - "Pre-launch registration re-pins follow the 41095975 amendment convention: after a legitimate harness change with no launch yet, re-pin harness-freeze.json and every registration's harness_freeze/code_dependencies digests; register-timing's exclusive write refuses regeneration, so the hand re-pin is the sanctioned path (c6dfb15c)."
  - "The owner-authorized one-shot weekday amendment (73bcbc74) admits weekday launches only before 2026-11-04 07:30 America/Chicago, and that deadline is also the closing instant of the remaining-window check; all 16 real launches of this plan (metadata + 15 rows) ran inside that window on AC power."
  - "The AC-power halt resolved exactly as designed: the refusal fired before any protected work, the resume changed nothing (no code edit, no re-registration, no re-pin), and the 15 rows replayed in the declared case-major order with each row committed before the next launch — zero retries, zero reused directories, zero gate refusals."
  - "The common science budget is N=152900 (warmup 200, measured 152700), the largest 100-step quantum with N>=300 whose every case/arm projection fits 0.75*3540 s: the slowest row repeat-1632-s41/d12 projects 2654.31 s against the 2655 s target, the fastest 854.81 s, the experiment 25466.89 s over 15 runs — measured costs only, no score, loss, tier or cosine value entered the projection."

patterns-established:
  - "Deviation fix + mandatory re-pin chain: fix harness, add regression test, regenerate affected declarations, re-pin freeze manifest, re-pin manifest digests in registrations, commit, re-run check-design/check-metadata/check-matrix."
  - "Serial row campaign with per-row prospective commits: check-matrix -> eligibility -> verify earlier rows committed -> launch-row once -> check-row -> inspect scoped cost evidence only -> commit the row's record/attempt/power-gate/weights before the next launch."

requirements-completed: []  # EXP-02 stays open until the phase verification act: every 67-0N plan declares EXP-02..05 and the marks flip only when all declaring plans finish (shared-ID gate, 67-04/67-06 convention).

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
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-matrix --experiment exp02 --kind timing (PHASE67-MATRIX-OK, re-verified before every launch of this plan)"
        status: pass
    human_judgment: false
  - id: D4
    description: "15 serial timing rows measured, checked (each PHASE67-ROW-OK) and individually committed before the next launch, then the cost-only common budget N=152900, both budget/prediction pages, science-matrix.json and all 15 science registrations committed before any science launch (no science run started)"
    requirement: EXP-02
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-budget --experiment exp02 (PHASE67-BUDGET-OK at 652d1a9d)"
        status: pass
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-matrix --experiment exp02 --kind science (PHASE67-MATRIX-OK at 652d1a9d)"
        status: pass
    human_judgment: false

# Metrics
duration: ~3h55m total across sessions (predecessor 12:00-14:00 + 14:05-16:25 including ~2h AC polling; resume 20:02-20:45 America/Chicago, ~35 min of it the 15 rows + budget)
completed: 2026-11-03
status: complete
---

# Phase 67 Plan 08: EXP-02 Depth Ladder Pre-Registration, Calibration and Budget Summary

**EXP-02 is fully pre-registered and measured: the committed design and metadata capture, all 15 case-major timing rows (N1200/warmup200/measured1000 under the 900-second cap, 5.9-19.2 s walls each, every row PHASE67-ROW-OK and committed before the next launch), and the derived cost-only common science budget N=152900 with both pages, the science matrix and all 15 science registrations — no science run started.**

## Performance

- **Duration:** ~3h55m across three sessions (predecessor 12:00-14:00 interrupted by a provider limit; halted session 14:05-16:25 including ~2h of AC-power polling; this resume 20:02-20:45 America/Chicago)
- **Started:** 2026-11-03 ~12:00 America/Chicago (predecessor)
- **Completed:** 2026-11-03 20:45 America/Chicago (this resume: rows 20:04-20:33, budget 20:34)
- **Tasks:** 3 of 3 complete
- **Files:** 80 evidence/page files on disk across the plan's commits; this resume committed 15 rows x 4 files + 19 budget/science files

## Accomplishments

- Task 67-08-01 (predecessor): the complete EXP-02 design, metadata registration and 67-EXP02-TIMING-PREDICTION.md committed at 75424795 (check-design PHASE67-DESIGN-OK).
- Task 67-08-02 (predecessor): the guarded TRAIN metadata capture receipt at 9106f40b, the amended receipt-window audits at 41095975, the timing matrix and all 15 registrations at c9c994eb; the t_end deviation fixed and the freeze chain re-pinned (e2a3a380, c6dfb15c).
- Task 67-08-03 (this resume): all 15 declared timing rows launched serially, case-major with arms in the listed order — main-1632-s42, repeat-851-s42, repeat-1632-s41 x d2, d4, d6, d8, d12. Each row: check-matrix re-run, eligibility verified (AC power + amendment window + no other diagnostic run), earlier rows verified committed, launch-row exactly once, check-row (each PHASE67-ROW-OK), scoped cost evidence inspected (no timing E screened), then the row's record/attempt/power-gate/weights committed before the next launch. Zero retries, zero gate refusals, zero reused directories.
- The Plan04 budget applied verbatim over the 15 committed rows: common science N=152900 (measured 152700, warmup 200), per-row projections 854.81-2654.31 s against the 2655 s = 0.75*3540 target, experiment projection 25466.89 s over 15 declared runs in the phase cost ledger (measured_projection basis). budget.json, 67-EXP02-BUDGET.md, 67-EXP02-PREDICTION.md, science-matrix.json and all 15 science registrations committed at 652d1a9d before any science launch.
- Verify gates on the committed state: check-budget PHASE67-BUDGET-OK and check-matrix --kind science PHASE67-MATRIX-OK (both at 652d1a9d); check-matrix --kind timing re-verified PHASE67-MATRIX-OK.
- The halt is resolved in the tracking artifacts: WINDOWS entries 3 (t_end deviation) and 4 (unrun task-3 gates) marked fixed; STATE.md/ROADMAP.md brought to the completed position.

## Task Commits

1. **Task 67-08-01: design** - `75424795` (evidence)
2. **Owner-authorized amendment: weekday deadline** - `73bcbc74` (spec)
3. **Task 67-08-02: metadata receipt** - `9106f40b` (evidence)
4. **Task 67-08-02: receipt-window audits** - `41095975` (spec)
5. **Task 67-08-02: timing matrix + registrations** - `c9c994eb` (evidence)
6. **Deviation fix: declared window = variant length** - `e2a3a380` (fix)
7. **Re-pin: registrations to the amended harness** - `c6dfb15c` (fix)
8. **Halted close-out (superseded by this SUMMARY)** - `e2ebda79` (docs)
9. **Task 67-08-03: row 1 main-1632-s42/d2** - `a05542df` (evidence, 5.571 ms/step, 8.56 s wall)
10. **Task 67-08-03: row 2 main-1632-s42/d4** - `42b27794` (evidence, 7.065 ms/step, 9.98 s wall)
11. **Task 67-08-03: row 3 main-1632-s42/d6** - `f35d15dc` (evidence, 8.752 ms/step, 12.11 s wall)
12. **Task 67-08-03: row 4 main-1632-s42/d8** - `50ae90e6` (evidence, 10.184 ms/step, 14.05 s wall)
13. **Task 67-08-03: row 5 main-1632-s42/d12** - `d1feec48` (evidence, 13.344 ms/step, 18.62 s wall)
14. **Task 67-08-03: row 6 repeat-851-s42/d2** - `a27fad10` (evidence, 4.447 ms/step, 5.91 s wall)
15. **Task 67-08-03: row 7 repeat-851-s42/d4** - `b2eb4a11` (evidence, 6.616 ms/step, 9.00 s wall)
16. **Task 67-08-03: row 8 repeat-851-s42/d6** - `1f4382a0` (evidence, 8.284 ms/step, 11.42 s wall)
17. **Task 67-08-03: row 9 repeat-851-s42/d8** - `10c1b9e1` (evidence, 10.319 ms/step, 14.04 s wall)
18. **Task 67-08-03: row 10 repeat-851-s42/d12** - `69818423` (evidence, 13.682 ms/step, 18.95 s wall)
19. **Task 67-08-03: row 11 repeat-1632-s41/d2** - `3e59865f` (evidence, 5.392 ms/step, 7.28 s wall)
20. **Task 67-08-03: row 12 repeat-1632-s41/d4** - `f7b0da1e` (evidence, 6.786 ms/step, 9.27 s wall)
21. **Task 67-08-03: row 13 repeat-1632-s41/d6** - `5a8335f0` (evidence, 8.296 ms/step, 11.48 s wall)
22. **Task 67-08-03: row 14 repeat-1632-s41/d8** - `401876e4` (evidence, 10.108 ms/step, 13.91 s wall)
23. **Task 67-08-03: row 15 repeat-1632-s41/d12** - `288d81df` (evidence, 13.844 ms/step, 19.25 s wall)
24. **Task 67-08-03: budget + science registrations (N=152900)** - `652d1a9d` (evidence)
25. **Plan metadata: this SUMMARY + STATE/ROADMAP/WINDOWS** - final docs commit

**Plan metadata:** the final `docs(67-08)` commit carries this SUMMARY, STATE.md, ROADMAP.md and WINDOWS.md (it rewrites the halted close-out e2ebda79).

## Files Created/Modified
- `evidence/exp02/timing/{main-1632-s42,repeat-851-s42,repeat-1632-s41}/{d2,d4,d6,d8,d12}/` - each row's registration.json (predecessor) plus this resume's record.json, attempt.json (status published), power-gate.json (AC Power, isoweekday 2) and diagnostic.weights
- `evidence/exp02/budget.json` - the cost-only budget document (N=152900, per-row projections, timing-evidence digests, phase cost ledger)
- `67-EXP02-BUDGET.md` / `67-EXP02-PREDICTION.md` - the budget and immutable science prediction pages
- `evidence/exp02/science-matrix.json` + `evidence/exp02/science/{CASE}/{ARM}/registration.json` (15) - the prospective science registrations at the common N with normalized cadence
- `pinn/verification/diagnostic_phase67_execution.py`, `tests/phase67/test_pages.py`, `evidence/harness-freeze.json` - the predecessor's deviation fix and re-pin chain (unchanged this resume)

## Decisions Made
- The resume made no changes to code, registrations or pins: the halt left zero burned directories, so the declared row order replayed unchanged. The only addition before the first launch was the wake assertion (`caffeinate -i -t 41400`) covering the inter-row gaps through the 07:30 America/Chicago amendment deadline, so the Mac could not idle-sleep mid-campaign.
- check-budget and check-matrix --kind science intentionally run AFTER the budget commit, not before: the dependency chronology requires the committed budget before the checks admit (the pre-commit run refused with "the budget is untracked or dirty", exactly the designed gate).
- EXP-02's requirement mark stays open until the phase verification act (shared-ID gate: every 67-0N plan declares EXP-02..05).
- No scientific value was screened at any point: check-row's value-free reading was the only per-row verdict, and only cost fields (walls, rates, phase ledgers, access attestations) were inspected.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Rows declared the observed grid endpoint instead of the variant's window length**
- **Found during:** Task 67-08-02 (predecessor, mid-flight at interruption; verified and committed in the halted session)
- **Issue:** phase67_run_matrix stamped t_end 9.999999999999831 (the observed gold-grid float64 endpoint) into the timing rows and registrations; the settings door requires the declared endpoint to equal the variant's window length (10.0, as Phase 66's committed real registrations declare), so admission would refuse every row.
- **Fix:** declared_t_end = float(declaration.window_length) for full-window experiments (exp05 keeps the observed prefix endpoint); regression test added; matrix and all 15 registrations regenerated to t_end 10.0; harness freeze re-pinned (7c8a4f09.. -> 28896b3c..) and the metadata registration's manifest digest re-pinned (884bf217.. -> df16b296..), mirroring the 41095975 chain.
- **Files modified:** pinn/verification/diagnostic_phase67_execution.py, tests/phase67/test_pages.py, timing-matrix.json, 15 timing registration.json files, harness-freeze.json, metadata-registration.json
- **Verification:** new regression test passes; phase65 204 OK, phase66 101 OK, phase67 244 OK; check-metadata PHASE67-METADATA-OK
- **Committed in:** e2a3a380

**2. [Rule 3 - Blocking] Stale harness pins inside the committed timing registrations refused check-matrix**
- **Found during:** Task 67-08-02 close-out (halted session)
- **Issue:** the 15 registrations were stamped by register-timing while the harness was at 7c8a4f09..; after the deviation fix the fit door refuses each row ("registration artifact changed since it was committed"). register-timing cannot be re-run because _exclusive_json_write refuses existing artifacts.
- **Fix:** re-pinned each registration's diagnostic_phase67_execution.py code_dependency to the live 28896b3c.. and harness_freeze to df16b296..; all 13 code dependencies per registration verified against live bytes; no other field touched.
- **Files modified:** the 15 timing registration.json files
- **Verification:** check-matrix --experiment exp02 --kind timing = PHASE67-MATRIX-OK; check-metadata = PHASE67-METADATA-OK
- **Committed in:** c6dfb15c

---

**Total deviations:** 2 auto-fixed (1 bug, 1 blocking), both in the predecessor sessions and carried forward from the halted SUMMARY; this resume executed its task with zero new deviations.
**Impact on plan:** both fixes were required for the settings door to admit any row; all 15 rows then admitted and published cleanly through the corrected declarations.

## Issues Encountered

- **The designed AC-power halt and its resolution.** The predecessor session's launch refused at row 1 on battery power before any protected work (zero attempts created); this resume verified AC power live (POWER-OK source=AC Power isoweekday=2), started the wake assertion, and ran the full 15-row campaign plus budget inside the amendment window (~31 minutes of launches). Nothing was retried, interpolated or modified to bypass the gate; the halt and resolution are the designed behavior of the power primitive, not a defect.
- check-budget/check-matrix --kind science refused with "untracked or dirty" when run before the budget commit — the designed commit-chronology gate, satisfied by committing the budget artifacts first (see Decisions Made).

## Known Stubs
None - no stubs, placeholders or unwired data paths. All 15 timing rows are measured publications and all 15 science registrations name the committed common budget.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- **EXP-02 is launch-ready for its science rows but no science run may or did start in this plan.** The science registrations at N=152900 are committed; the science launches belong to the phase's later execution sequence per their own plans and the review gates (the prior-experiment review chain gates dependent experiments).
- Wave 7 is complete, unblocking Wave 8 (67-09 onward: the EXP-03 rate ladder follows the same prepare-design -> capture -> register -> launch -> budget -> review chain against the same frozen harness).
- A `caffeinate -i -t 41400` wake assertion (started 20:03 America/Chicago) remains running through ~07:30 America/Chicago; it is benign (idle-sleep guard only, display may sleep) and self-expires. If later plans launch tonight inside the amendment window, it keeps the Mac awake between their rows.
- The remaining phase-67 WINDOWS ledger entries (1 and 2) belong to Phase 57 and predate this plan.

## Self-Check: PASSED

All 80 task-3 evidence files exist on disk (15 rows x 4 evidence files + registration check, budget.json, both pages, science-matrix.json, 15 science registrations); all 16 new commits (a05542df..652d1a9d) exist in history; check-budget PHASE67-BUDGET-OK, check-matrix science PHASE67-MATRIX-OK and check-matrix timing PHASE67-MATRIX-OK all pass at 652d1a9d; `git diff --check` clean at every commit; the working tree holds no uncommitted phase-67 evidence.

---
*Phase: 67-design-settings-ladders*
*Completed: 2026-11-03*
