---
phase: 67-design-settings-ladders
plan: "10"
subsystem: verification-diagnostics
tags: [pinn, exp03, rate-ladder, prospective-registration, timing-rows, ac-gate, cost-only-budget, deferral]

# Dependency graph
requires:
  - phase: 67-design-settings-ladders (67-08, 67-09)
    provides: the committed EXP-02 end-to-end pipeline (design -> metadata -> timing -> budget -> science -> review), the registered unsettled continue route (dependent_launch_allowed=true) that unblocks EXP-03, the frozen 41-file harness freeze and the phase67_control_arm convention
provides:
  - Committed EXP-03 scientific design (67-EXP03-TIMING-PREDICTION.md, design.json, metadata-registration.json): the learning-rate ladder (constant Adam rates 1e-3, 3e-4, 1e-4, 3e-5, 1e-5 on the locked depth12/width256/o30/h1/raw14/[0,10] network) with exact contrasts, control lr1e-4, confirmatory rule, reading branches and the single 900-second metadata cap, all frozen before any real access
  - One guarded TRAIN-only metadata capture for systems 1632 and 851 (attempt published 03:07:53 CST, independently verified gold-grid hashes and same-window expectations) and the committed 15-row timing-matrix registration (3 cases x 5 arms, case-major order)
  - All 15 measured, checked and individually committed timing rows (N1200/warmup200/measured1000, measured segments 13.21-13.66 s, zero retries, zero refusals, every row committed before the next launch)
  - The measured cost-only common science budget N=155100 (warmup 200, measured 154900; per-row projections 2567.88-2654.24 s, all <= the 2655 s = 0.75 x 3540 target; experiment projection 39055.09 s), the budget/prediction pages, science-matrix.json and all 15 prospective science registrations — no science run started
  - The deferral state: every science row is registered and waiting on the weekend admission window (Sat 2026-11-07 00:00 through Sun 2026-11-08 22:00 America/Chicago)
affects: [67-11, 67-12, 67-13, 67-14, 67-15, 67-16]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
# Scale caveat: the realized diff is dominated by machine-written evidence
# (15 timing records with full step-event traces, 15 science registrations,
# budget.json and its two pages), not agent-authored text.
actuals:
  tokens: 1814494      # chars/4 over the realized text diff 7290bf58^..1977d85d (7,257,978 bytes; weights binaries excluded)
  tasks: 3             # 67-10-01, 67-10-02, 67-10-03 (all complete; task-03 verify run by this continuation)
  commits: 22          # 21 evidence/fix commits (7290bf58..1977d85d) + 1 final docs commit (this SUMMARY)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Control-arm resolution is centralized: every site that reads a control row (design stamping, review contrasts, self-control arm identity) resolves through phase67_control_arm rather than arms[-1], which only coincided with the registered control for exp02/exp05 (fix 7290bf58)."
    - "Post-fix freeze-chain re-pin before any dependent registration exists: fix code, re-pin harness-freeze.json to the live digests, re-pin the manifest digest in every registration that names it, commit, re-run all checks (mirrors 41095975/c6dfb15c; applied in ed93f359)."

key-files:
  created:
    - .planning/phases/67-design-settings-ladders/67-EXP03-TIMING-PREDICTION.md
    - .planning/phases/67-design-settings-ladders/evidence/exp03/design.json
    - .planning/phases/67-design-settings-ladders/evidence/exp03/metadata-registration.json
    - .planning/phases/67-design-settings-ladders/evidence/exp03/metadata/{record.json,attempt.json,power-gate.json}
    - .planning/phases/67-design-settings-ladders/evidence/exp03/timing-matrix.json
    - .planning/phases/67-design-settings-ladders/evidence/exp03/timing/CASE/ARM/{registration,record,attempt,power-gate}.json + diagnostic.weights (15 rows)
    - .planning/phases/67-design-settings-ladders/evidence/exp03/budget.json
    - .planning/phases/67-design-settings-ladders/67-EXP03-BUDGET.md
    - .planning/phases/67-design-settings-ladders/67-EXP03-PREDICTION.md
    - .planning/phases/67-design-settings-ladders/evidence/exp03/science-matrix.json
    - .planning/phases/67-design-settings-ladders/evidence/exp03/science/CASE/ARM/registration.json (15 rows)
  modified:
    - .planning/phases/67-design-settings-ladders/evidence/harness-freeze.json (re-pinned in ed93f359)
    - 30 exp02 metadata/timing/science registrations (manifest + execution.py digest re-pins, digest fields only)

key-decisions:
  - "The control-arm fix (7290bf58) landed before the design commit: prepare-design had stamped control_arm=arms[-1], which for exp03's listed arm order is lr1e-5, while D-04 and phase67_control_arm name lr1e-4 (the locked rate); all three sites now resolve through phase67_control_arm, exp02's generated design stayed byte-identical, and a regression test asserts exp03 declares lr1e-4 with lr1e-5 keeping a hypothesis row (suites after the fix: phase65 204 OK, phase66 101 OK, phase67 245 OK)."
  - "The freeze-chain re-pin (ed93f359) followed the sanctioned pre-launch convention: the control-arm fix changed diagnostic_phase67_execution.py, moving the frozen harness digest 28896b3c -> 2c1ae0a8 and the manifest digest df16b296 -> dc916d2f; the manifest entry and all 30 exp02 registrations naming it were re-pinned (digest fields only) before any exp03 registration existed, and exp02's checks re-verified green."
  - "All 16 real launches of this plan (1 metadata + 15 timing rows) ran inside the owner amendment's weekday window on 2026-11-04 03:05-03:18 America/Chicago, strictly before its 07:30 closing instant, each exactly once through diagnostic_power and the outer supervisor; measured timing segments are 13.21-13.66 s per row (seconds_per_step 0.01321-0.01366), every attempt published under the 900-second whole-launch cap."
  - "The common science budget is N=155100 (warmup 200, measured 154900), the largest 100-step quantum with N>=300 whose every case/arm projection fits 0.75 x 3540 s: the slowest row repeat-1632-s41/lr3e-4 projects 2654.24 s against the 2655 s target, the fastest repeat-851-s42/lr3e-5 2567.88 s, the experiment 39055.09 s over 15 runs — measured costs only; no score, loss, tier or cosine value entered the projection."
  - "No science row was launched: the amendment window closed at 07:30 America/Chicago on 2026-11-04, the 15 science rows cannot fit inside a weekday window before that instant, and the next eligible admission is the weekend window (Sat 2026-11-07 00:00 through Sun 2026-11-08 22:00 America/Chicago); every science registration is committed and waiting, and deferral created no attempt and burned no directory."

patterns-established:
  - "Every declared arm is registered equally — all five rates including the control and the slowest arm carry identical registration structure; ties between timing costs do not merge identities."
  - "Prospective science staging completes before the compute window exists: budget, pages, matrix and all 15 registrations are committed while the machine is ineligible, so the weekend run starts at check-budget, not at design."

requirements-completed: []  # EXP-03 stays open until the phase verification act: every 67-0N plan declares EXP-02..05 and the marks flip only when all declaring plans finish (shared-ID gate, 67-04/67-08/67-09 convention).

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "EXP-03 complete scientific design and metadata registration committed before any real metadata or timing access (rate ladder 1e-3..1e-5 on the locked network, cases main-1632-s42/repeat-851-s42/repeat-1632-s41, control lr1e-4, confirmatory rule, ties/small-effects/opposed-repeats/unsettled/mechanical branches, 900-second metadata cap, frozen dependency digests)"
    requirement: EXP-03
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-design --experiment exp03 (PHASE67-DESIGN-OK, exit 0, re-run at final evidence HEAD 1977d85d)"
        status: pass
    human_judgment: false
  - id: D2
    description: "One guarded TRAIN-only metadata capture for systems 1632 and 851 (independently verified full-window gold-grid hashes, sample counts, coordinates and same-window constant/two-Kepler expectations) with the receipt committed before timing registration"
    requirement: EXP-03
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-metadata --experiment exp03 (PHASE67-METADATA-OK, exit 0, re-run at final evidence HEAD 1977d85d)"
        status: pass
    human_judgment: false
  - id: D3
    description: "All 15 declared timing rows (3 cases x 5 rate arms, case-major serial order) each launched exactly once at N1200/warmup200/measured1000 under the 900-second cap, mechanically checked with scores hidden, and committed as record/attempt/power-gate/weights before the next launch"
    requirement: EXP-03
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-matrix --experiment exp03 --kind timing (PHASE67-MATRIX-OK, exit 0, re-run at final evidence HEAD 1977d85d)"
        status: pass
    human_judgment: false
  - id: D4
    description: "The measured cost-only common budget (N=155100, per-row projections 2567.88-2654.24 s <= 2655 s, experiment 39055.09 s), both budget/prediction pages, science-matrix.json and all 15 prospective science registrations committed with no science run started; every row deferred to the weekend admission window"
    requirement: EXP-03
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-budget --experiment exp03 (PHASE67-BUDGET-OK, exit 0, run at 1977d85d)"
        status: pass
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-matrix --experiment exp03 --kind science (PHASE67-MATRIX-OK, exit 0, run at 1977d85d)"
        status: pass
    human_judgment: false

# Metrics
duration: ~13 min of executor evidence work (2026-11-04 03:05:55-03:18:49 CST) + ~10 min continuation verification/close-out (12:10-12:20 CST)
completed: 2026-11-04
status: complete
---

# Phase 67 Plan 10: EXP-03 Rate Ladder Pre-registration, Timing and Budget — Execution Summary

**The learning-rate ladder (1e-3/3e-4/1e-4/3e-5/1e-5 on the locked network, 3 cases) is fully pre-registered: committed design -> one guarded TRAIN metadata capture -> 15 measured and serially committed timing rows -> the cost-only common budget N=155100 (per-row 2567.88-2654.24 s, experiment 39055.09 s) -> all 15 prospective science registrations, with no science row launched and every row waiting on the weekend window (Sat 2026-11-07 00:00 - Sun 22:00 America/Chicago).**

## Performance

- **Duration:** ~13 min of evidence work (design fixes 03:05:55 CST through the final evidence commit 03:18:49 CST 2026-11-04) + ~10 min continuation verification and close-out (12:10-12:20 CST)
- **Started:** 2026-11-04T03:05:55-06:00 (evidence work; predecessor executor)
- **Completed:** 2026-11-04 (evidence HEAD 1977d85d at 03:18:49-06:00; SUMMARY committed by the continuation executor)
- **Tasks:** 3 of 3 complete
- **Files:** 98 evidence/page files created or re-pinned (75 timing artifacts + 15 science registrations + design/metadata/matrix/budget/pages)

## Accomplishments

- Task 67-10-01: the complete EXP-03 scientific design was committed (952f4dcb) after two in-scope executor fixes: the control-arm resolver fix (7290bf58 — prepare-design and the review loop had stamped the control as arms[-1], which is lr1e-5 in exp03's listed order, instead of the registered lr1e-4; all sites now resolve through phase67_control_arm, exp02's design stayed byte-identical, regression test added) and the freeze-chain re-pin (ed93f359 — the fix moved the frozen harness digest 28896b3c -> 2c1ae0a8 and manifest digest df16b296 -> dc916d2f; manifest entry and all 30 exp02 registrations re-pinned, digest fields only, exp02 checks re-verified green). The design declares every case/arm row, the confirmatory rule (same E direction in all three cases plus a matching frozen-tier change or >=20% E effect in each; final-quarter E decrease >5% is unsettled), ties/small-effects/opposed-repeats/unsettled/mechanical branches, the single 900-second whole-attempt metadata cap over both systems, no automatic continuation, and frozen code/settings dependency digests.
- Task 67-10-02: one guarded TRAIN-only metadata capture ran exactly once (attempt published 03:07:53 CST, cap 900 s) and its record/attempt/power-gate receipt was committed (ceb5ff7d) before the 15-row timing-matrix registration (c52e81f5). All five rates remain separate registered identities.
- Task 67-10-03: all 15 timing rows ran serially in the declared case-major order (main-1632-s42, repeat-851-s42, repeat-1632-s41 x lr1e-3, lr3e-4, lr1e-4, lr3e-5, lr1e-5), each launched exactly once through diagnostic_power, mechanically checked with scores hidden, and committed (record, attempt, power-gate, diagnostic.weights) before the next launch. Measured optimizer segments: 13.21-13.66 s per row (seconds_per_step 0.01321-0.01366), every attempt published under the 900-second whole-launch cap. Zero retries, zero refusals, zero reused directories. Then the Plan04 budget was computed from measured costs only (1977d85d): common N=155100 (warmup 200, measured 154900), similarity cadence [0, 38775, 77550, 116325, 155100], frozen-score cadence [77550, 116325, 155100], loss-trace stride 156, per-row projections 2567.88-2654.24 s all inside the 2655 s target, experiment projection 39055.09 s. The budget page, prediction page, science-matrix.json and all 15 science registrations were committed before any science access.
- Continuation close-out (this session): both required task-03 verification gates were run for the first time (the predecessor executor died on a provider usage limit immediately after 1977d85d, before verification) — check-budget (PHASE67-BUDGET-OK) and check-matrix --kind science (PHASE67-MATRIX-OK), both exit 0 at the final evidence HEAD; the three earlier gates were re-run for confidence (check-design, check-metadata, check-matrix --kind timing — all OK).

## Task Commits

1. **Fix: control arm through the registered resolver** - `7290bf58` (fix, 03:05:55 CST)
2. **Fix: freeze-chain re-pin to the corrected harness** - `ed93f359` (fix, 03:06:35 CST)
3. **Task 67-10-01: complete exp03 scientific design** - `952f4dcb` (evidence, 03:07:35 CST)
4. **Task 67-10-02: guarded metadata capture receipt** - `ceb5ff7d` (evidence, 03:08:20 CST)
5. **Task 67-10-02: 15-row timing-matrix registration** - `c52e81f5` (evidence, 03:08:54 CST)
6. **Task 67-10-03: timing row 1 main-1632-s42/lr1e-3** - `bab3eab1` (evidence, 03:10:05 CST)
7. **Task 67-10-03: timing row 2 main-1632-s42/lr3e-4** - `130082d0` (evidence, 03:10:49 CST)
8. **Task 67-10-03: timing row 3 main-1632-s42/lr1e-4** - `15111235` (evidence, 03:11:19 CST)
9. **Task 67-10-03: timing row 4 main-1632-s42/lr3e-5** - `c0814b96` (evidence, 03:11:49 CST)
10. **Task 67-10-03: timing row 5 main-1632-s42/lr1e-5** - `acec95e5` (evidence, 03:12:20 CST)
11. **Task 67-10-03: timing row 6 repeat-851-s42/lr1e-3** - `5513300f` (evidence, 03:13:02 CST)
12. **Task 67-10-03: timing row 7 repeat-851-s42/lr3e-4** - `f575a678` (evidence, 03:13:33 CST)
13. **Task 67-10-03: timing row 8 repeat-851-s42/lr1e-4** - `02530da5` (evidence, 03:14:03 CST)
14. **Task 67-10-03: timing row 9 repeat-851-s42/lr3e-5** - `964a72e2` (evidence, 03:14:34 CST)
15. **Task 67-10-03: timing row 10 repeat-851-s42/lr1e-5** - `7cde69d7` (evidence, 03:15:04 CST)
16. **Task 67-10-03: timing row 11 repeat-1632-s41/lr1e-3** - `f43c0141` (evidence, 03:15:49 CST)
17. **Task 67-10-03: timing row 12 repeat-1632-s41/lr3e-4** - `866c26d9` (evidence, 03:16:19 CST)
18. **Task 67-10-03: timing row 13 repeat-1632-s41/lr1e-4** - `0490feaa` (evidence, 03:16:50 CST)
19. **Task 67-10-03: timing row 14 repeat-1632-s41/lr3e-5** - `6d0af660` (evidence, 03:17:21 CST)
20. **Task 67-10-03: timing row 15 repeat-1632-s41/lr1e-5** - `f925cdcc` (evidence, 03:17:51 CST)
21. **Task 67-10-03: exp03 budget and all science registrations** - `1977d85d` (evidence, 03:18:49 CST)
22. **Plan metadata: this SUMMARY** - final docs commit

## Files Created/Modified

- `evidence/exp03/design.json`, `evidence/exp03/metadata-registration.json`, `67-EXP03-TIMING-PREDICTION.md` - the frozen design, metadata registration and committed design page
- `evidence/exp03/metadata/{record.json,attempt.json,power-gate.json}` - the single TRAIN-only metadata capture and its receipt
- `evidence/exp03/timing-matrix.json` + `evidence/exp03/timing/CASE/ARM/{registration,record,attempt,power-gate}.json + diagnostic.weights` - the 15-row timing matrix and each row's five artifacts
- `evidence/exp03/budget.json`, `67-EXP03-BUDGET.md`, `67-EXP03-PREDICTION.md` - the measured common budget, its page and the prospective prediction page
- `evidence/exp03/science-matrix.json` + `evidence/exp03/science/CASE/ARM/registration.json` (15 rows) - the prospective science matrix, registrations only (no run artifacts exist)
- `evidence/harness-freeze.json` + 30 exp02 registrations - digest-only re-pins from ed93f359

## Decisions Made

- The two executor fixes were applied before the design commit so no registration ever existed against the stale resolver or the stale freeze digests: the control arm is resolved through phase67_control_arm everywhere, and the freeze chain was re-pinned per the 41095975/c6dfb15c convention (re-pinning is the sanctioned path because register-timing's exclusive write refuses regeneration).
- Timing and science identities: all five rates stay separate registered identities even where measured timing costs tie; timing rows measure cost only and no timing accuracy value was screened, read or used in any selection.
- The deferral was recorded, not worked around: the science rows were not squeezed toward the weekday deadline and no admission gate was relaxed; the committed registrations carry the weekend window as their next eligible admission.

## Deviations from Plan

### Auto-fixed Issues (handled earlier in the run, before the design commit)

**1. [Rule 1 - Bug] Control arm was stamped as arms[-1] instead of the registered lr1e-4**
- **Found during:** Task 67-10-01 (design preparation, pre-commit)
- **Issue:** prepare-design stamped control_arm=arms[-1] and the review loop read the control row as arms[-1]; that equals the registered control only for exp02/exp05, so the fresh exp03 design would have declared lr1e-5 as the control and contrasted every exp03 arm against lr1e-5 in review, while D-04 and phase67_control_arm name lr1e-4 (the locked rate) as the exp03 control.
- **Fix:** all three sites resolve through phase67_control_arm (an arm carries the control row when it is its own registered control; the design's control_arm scalar names the single control; review contrasts read each arm's registered control row). exp02's generated design verified byte-identical; regression test asserts exp03 declares lr1e-4 as control with lr1e-5 keeping a hypothesis row; suites phase65 204 OK, phase66 101 OK, phase67 245 OK.
- **Files modified:** pinn/verification/diagnostic_phase67_execution.py (resolver sites), tests/phase67 suite
- **Verification:** committed design.json declares lr1e-4 as control; check-design PHASE67-DESIGN-OK at every subsequent gate
- **Committed in:** 7290bf58

**2. [Rule 3 - Blocking] Freeze-chain digests moved after the control-arm fix**
- **Found during:** Task 67-10-01 (between the resolver fix and the design commit)
- **Issue:** the fix changed diagnostic_phase67_execution.py, so the frozen harness digest moved 28896b3c -> 2c1ae0a8 and the freeze-manifest digest df16b296 -> dc916d2f; any registration created against the stale pins would refuse at launch (dependency drift stops admission).
- **Fix:** re-pinned harness-freeze.json to the live file digests and re-pinned the manifest/execution.py digests in every registration that names them (the exp02 metadata registration and all 30 exp02 timing/science row registrations), digest fields only, before any exp03 registration existed; exp02's checks re-verified green afterwards.
- **Files modified:** evidence/harness-freeze.json, 30 exp02 registrations
- **Verification:** check-design/check-metadata/check-matrix (timing+science) all OK for exp02 after the re-pin; exp03 gates green at final HEAD
- **Committed in:** ed93f359

---

**Total deviations:** 2 auto-fixed (1 bug, 1 blocking).
**Impact on plan:** both fixes were prerequisites for a correct, admissible exp03 design; neither changed any committed exp02 run evidence and neither touched a scientific value.

## Issues Encountered

- The predecessor executor (agent_c60021a2) died on a provider usage limit immediately after the final evidence commit 1977d85d (03:18:49 CST), so the task-03 verification commands and this SUMMARY were left undone. The continuation executor ran both required gates read-only at the committed HEAD; both passed, and nothing was regenerated, re-pinned or relaunched.
- The amendment window closed at 07:30 America/Chicago on 2026-11-04 (the evidence work ran 03:05-03:18, inside it); the science rows therefore deferred to the weekend window. No attempt, burned directory or partial record exists for any science row.

## Known Stubs

None - no stubs, placeholders or unwired data paths; all 15 timing rows are measured publications, the budget is fully measured, and all 15 science registrations are complete prospective registrations awaiting their admission window (deferral by design, not an unwired path).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- EXP-03 is fully staged: the next eligible compute window is the weekend (Sat 2026-11-07 00:00 through Sun 2026-11-08 22:00 America/Chicago); the launching plan starts at check-budget/check-matrix (both green at 1977d85d) and proceeds row-by-row at the common N=155100 exactly as registered — no re-planning, no re-registration, no re-pinning needed.
- The experiment projection is 39055.09 s (~10h51m) over 15 serial supervised rows, inside the Sunday 22:00 close only if the weekend window is used broadly; the launching executor should sequence rows case-major as registered and defer unstarted rows rather than compress.
- EXP-03's requirement mark stays open until the phase verification act (shared-ID gate: every 67-0N plan declares EXP-02..05).

## Self-Check: PASSED

All five gates pass at the final evidence HEAD 1977d85d: check-design PHASE67-DESIGN-OK, check-metadata PHASE67-METADATA-OK, check-matrix timing PHASE67-MATRIX-OK, check-budget PHASE67-BUDGET-OK, check-matrix science PHASE67-MATRIX-OK (all exit 0). All 98 exp03 evidence/page files are tracked (75 timing files = 15 rows x 5 artifacts; 15 science registration.json files; design/metadata/matrix/budget/pages) with zero untracked exp03 paths; science directories contain registration.json only, confirming no science run started; all 21 evidence commits (7290bf58..1977d85d) exist in history in execution order with author = committer dates; the working tree holds only the pre-existing user-owned unrelated changes (.planning/config.json, the stage0 brief, cross_cutting docs, .agents/.gsd/planning temporaries), which were never staged or modified; `git diff --check` clean for the SUMMARY commit.

---
*Phase: 67-design-settings-ladders*
*Completed: 2026-11-04*
