---
phase: 67-design-settings-ladders
plan: "09"
subsystem: verification-diagnostics
tags: [pinn, exp02, depth-ladder, science-rows, serial-launch, review, unsettled-branch]

# Dependency graph
requires:
  - phase: 67-design-settings-ladders (67-08)
    provides: the committed EXP-02 design, metadata, budget N=152900, science-matrix.json and all 15 science registrations
provides:
  - All 15 EXP-02 science rows measured, mechanically checked (PHASE67-ALL-ROWS-OK) and committed serially at the common N=152900 (record/attempt/power-gate/weights per row, one commit per row before the next launch)
  - The committed machine review (evidence/exp02/review.json, dependent_launch_allowed=true, scope49_disposition=none) and the complete result page 67-EXP02-RESULT.md with every endpoint E/tier, same-window comparison scores, per-cadence per-layer similarity traces, matched contrasts, costs and the prediction/roadmap comparison
  - The observed branch: the registered unsettled continue route — EXP-03 dependent work unblocked under D-01, no owner ruling required, no ruling file created
affects: [67-10, 67-11, 67-12, 67-13, 67-14, 67-15, 67-16]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
# Scale caveat: the realized diff is dominated by machine-written evidence
# (15 run records ~16.7-17k lines each, the 13.6k-line review.json and its
# byte-exact embed in the result page), not agent-authored text.
actuals:
  tokens: 1990317      # chars/4 over the realized text diff 79a624c3..HEAD (7,961,268 bytes; weights binaries excluded)
  tasks: 3             # 67-09-01, 67-09-02; 67-09-03 skipped by its own condition (continue route)
  commits: 18          # 15 row commits + review/result + embed fix + final docs commit

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Result-page embed contract: check-review requires the result page to contain the byte-exact json.dumps(review, indent=2, sort_keys=True) serialization of the committed review.json — reference-by-path alone refuses (fix 490ce41b)."
    - "Serial science campaign mirroring 67-08: per row, check-matrix -> AC/window/no-other-run eligibility -> previous row verified committed -> launch-row exactly once -> check-row (scores hidden) -> scoped cost-only inspection (attempt status, power source, wall, rate, bytes) -> commit the row's four files before the next launch."

key-files:
  created:
    - .planning/phases/67-design-settings-ladders/evidence/exp02/science/CASE/ARM/{record.json,attempt.json,power-gate.json,diagnostic.weights} (15 rows)
    - .planning/phases/67-design-settings-ladders/evidence/exp02/review.json
    - .planning/phases/67-design-settings-ladders/67-EXP02-RESULT.md
  modified:
    - .planning/STATE.md, .planning/ROADMAP.md

key-decisions:
  - "All 15 science rows ran inside the amendment window on AC power with zero gate refusals: launches 2026-11-03 20:45:54 through 2026-11-04 02:38:44 CST, each exactly once through diagnostic_power and the outer supervisor, every attempt published, measured walls 693.6-2135.6 s (total 19,750.2 s vs the 25,466.9 s projection; every row inside its 3540 s cap and per-row projection)."
  - "The observed EXP-02 branch is the registered unsettled continue route: every noncontrol arm's confirmation label is unsettled because at least one paired endpoint is unsettled — the d12 control's own main-case endpoint is unsettled (final-quarter improvement >5%), blocking confirmation for every arm of the main case; d2 worsens on all three cases (tier 0 vs control tier 1), d8 improves on all three but does not qualify on main (4.0% < 20%, no tier change), d4/d6 are mixed. The registered depth hypothesis is not supported on any arm at this budget and nothing is confirmed; dependent_launch_allowed=true, scope49_disposition=none, no proposed change."
  - "Task 67-09-03 (blocking-human checkpoint) was skipped exactly per its condition: it fires only when the committed review reads dependent_launch_allowed=false; the committed review reads true, so no ruling file exists, no owner question was asked, and check-review passed (PHASE67-REVIEW-OK) directly after the in-scope review."
  - "No scientific value was screened during the run loop: check-row's value-free mechanical audit was the only per-row verdict, per-row inspection touched cost fields only (attempt status, power source, wall/rate, bytes), and no row or repeat was selected, extended or reordered after any result."

patterns-established:
  - "Every declared arm is published equally — ties, small effects, mixed directions and unsettled endpoints included; no favourable-main selection."

requirements-completed: []  # EXP-02 stays open until the phase verification act: every 67-0N plan declares EXP-02..05 and the marks flip only when all declaring plans finish (shared-ID gate, 67-04/67-08 convention).

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "All 15 declared EXP-02 science rows (3 cases x 5 depth arms, case-major serial order) each launched exactly once at the common N=152900, mechanically checked with scores hidden, and committed as four artifacts per row before the next launch"
    requirement: EXP-02
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-row per row (15x PHASE67-ROW-OK) and the plan's task-1 aggregate verify command (PHASE67-ALL-ROWS-OK)"
        status: pass
    human_judgment: false
  - id: D2
    description: "The committed review (review.json, dependent_launch_allowed=true, scope49 none) and the complete result page exposing all 15 outcomes, every prospective contrast, convergence statuses, machine costs and the prediction/roadmap comparison, with the byte-exact review embedded"
    requirement: EXP-02
    verification:
      - kind: other
        ref: "plan task-2 verify (PHASE67-REVIEW-ARTIFACTS-OK: both files committed at HEAD with byte-identical content, all six review fields present)"
        status: pass
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-review --experiment exp02 (PHASE67-REVIEW-OK after the embed fix 490ce41b)"
        status: pass
    human_judgment: false

# Metrics
duration: ~6h10m wall (2026-11-03 20:42 CST to 2026-11-04 02:52 CST; ~5h33m of it the 15 supervised launches)
completed: 2026-11-04
status: complete
---

# Phase 67 Plan 09: EXP-02 Depth Ladder Science Matrix — Execution & Review Summary

**All 15 EXP-02 science rows ran serially at the common N=152900 (each launched once, PHASE67-ROW-OK, committed before the next launch; total measured wall 19,750.2 s inside every cap), and the committed review reads the registered unsettled continue route: no arm is confirmable (the main-case d12 control endpoint is itself unsettled), d2 worsens on all three cases, d8 improves on all three without qualifying on main — dependent_launch_allowed=true, no owner ruling, EXP-03 unblocked.**

## Performance

- **Duration:** ~6h10m wall (start 2026-11-03 20:42 CST; launches 20:45:54 -> 02:38:44 CST; review/close-out to ~02:52 CST 2026-11-04)
- **Started:** 2026-11-03T20:42:00-06:00
- **Completed:** 2026-11-04T02:52:00-06:00
- **Tasks:** 2 executed + 1 conditional checkpoint skipped by its own condition (plan complete)
- **Files:** 62 evidence/page files created (60 row artifacts + review.json + 67-EXP02-RESULT.md)

## Accomplishments

- Task 67-09-01: all 15 declared science rows executed in the exact case-major order (main-1632-s42, repeat-851-s42, repeat-1632-s41 x d2,d4,d6,d8,d12). Per row: check-matrix re-run, AC/window eligibility and no-other-run verified, the previous row verified committed, launch-row exactly once through diagnostic_power and the outer supervisor (every admission POWER-OK source=AC Power isoweekday=2), check-row PHASE67-ROW-OK with scores hidden, cost-only inspection, then the row's record/attempt/power-gate/weights committed before the next launch. Zero retries, zero refusals, zero reused directories, all attempts published, TRAIN-only access attestations throughout. Plan task-1 verify: PHASE67-ALL-ROWS-OK.
- Task 67-09-02: review --experiment exp02 committed (PHASE67-REVIEW-WRITTEN allowed=True) with the complete result page. The page reports endpoint E/tier/status for all 15 rows, same-window comparison scores per case, parameter counts, input..hd adjacent-time cosine at every one of the five cadence points for every depth in every case, all four matched contrasts against each case's freshly registered d12 control, measured machine costs against projections, the prediction-table and roadmap comparison, and the byte-exact embedded review. Plan task-2 verify: PHASE67-REVIEW-ARTIFACTS-OK.
- Task 67-09-03: skipped by its own condition (dependent_launch_allowed=true) — no ruling file, no owner question; check-review passed directly: PHASE67-REVIEW-OK.
- The wake assertion (caffeinate -i -t 41400, pid 98878 from 67-08) was verified alive before row 1 and never duplicated; the harness's own transient caffeinate processes (a -t 300 admission assertion and the caffeinate -is fit wrapper) belong to the launch machinery and were left alone. It self-expires ~07:32 CST.

## Task Commits

1. **Task 67-09-01: row 1 main-1632-s42/d2** - `09a60d00` (evidence, wall 777.8 s)
2. **Task 67-09-01: row 2 main-1632-s42/d4** - `9c3aecab` (evidence, 1043.9 s)
3. **Task 67-09-01: row 3 main-1632-s42/d6** - `a04e50fc` (evidence, 1277.3 s)
4. **Task 67-09-01: row 4 main-1632-s42/d8** - `9b2d7ba2` (evidence, 1518.1 s)
5. **Task 67-09-01: row 5 main-1632-s42/d12** - `9d2957b3` (evidence, 2135.6 s)
6. **Task 67-09-01: row 6 repeat-851-s42/d2** - `6a19af45` (evidence, 743.4 s)
7. **Task 67-09-01: row 7 repeat-851-s42/d4** - `6a4c7f2c` (evidence, 1005.5 s)
8. **Task 67-09-01: row 8 repeat-851-s42/d6** - `2756362d` (evidence, 1229.2 s)
9. **Task 67-09-01: row 9 repeat-851-s42/d8** - `eb3b113c` (evidence, 1481.8 s)
10. **Task 67-09-01: row 10 repeat-851-s42/d12** - `97d52264` (evidence, 2018.8 s)
11. **Task 67-09-01: row 11 repeat-1632-s41/d2** - `c322c48e` (evidence, 693.6 s)
12. **Task 67-09-01: row 12 repeat-1632-s41/d4** - `5d190697` (evidence, 984.4 s)
13. **Task 67-09-01: row 13 repeat-1632-s41/d6** - `ffd98e41` (evidence, 1287.7 s)
14. **Task 67-09-01: row 14 repeat-1632-s41/d8** - `4aed8511` (evidence, 1517.2 s)
15. **Task 67-09-01: row 15 repeat-1632-s41/d12** - `c9b68e6e` (evidence, 2035.7 s)
16. **Task 67-09-02: review.json + 67-EXP02-RESULT.md** - `94c121c1` (evidence)
17. **Rule-3 fix: embed the committed review in the result page** - `490ce41b` (evidence)
18. **Plan metadata: this SUMMARY + STATE/ROADMAP** - final docs commit

## Files Created/Modified

- `evidence/exp02/science/{main-1632-s42,repeat-851-s42,repeat-1632-s41}/{d2,d4,d6,d8,d12}/` - each row's record.json, attempt.json (status=published), power-gate.json (AC Power receipts) and diagnostic.weights beside its previously committed registration.json
- `evidence/exp02/review.json` - the generated machine review (phase67-review/v1)
- `67-EXP02-RESULT.md` - the complete reviewed result page with the embedded review
- `.planning/STATE.md`, `.planning/ROADMAP.md` - position updates (hand-edit convention)

## Decisions Made

- Followed the plan exactly on the continue route: the conditional checkpoint was skipped by its own condition, no ruling file was created, and check-review was run directly after the in-scope review (PHASE67-REVIEW-OK) as the plan's verification block directs.
- The result page was generated programmatically from the committed review/records (every scientific value machine-copied), not hand-transcribed; the only hand-typed figures were the commit-message cost summaries (see Issues Encountered).
- EXP-02's requirement mark stays open until the phase verification act (shared-ID gate: every 67-0N plan declares EXP-02..05).
- The caffeinate wake assertion was left to self-expire (~07:32 CST) per the 67-08 hand-off; it covers the remaining amendment window for any later plan's rows tonight.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] check-review refused the committed result page: review not embedded**
- **Found during:** Task 67-09-02 close-out (running the plan-level verification)
- **Issue:** check-review requires the result page to contain the byte-exact `json.dumps(review, indent=2, sort_keys=True)` serialization of the committed review.json; the first version of 67-EXP02-RESULT.md cited review.json by path only, so check-review refused with "the committed result page does not embed the committed review" (exit 2).
- **Fix:** appended the exact serialization as a fenced `phase67-review` block at the page foot; review.json itself unchanged.
- **Files modified:** .planning/phases/67-design-settings-ladders/67-EXP02-RESULT.md
- **Verification:** task-2 verify PHASE67-REVIEW-ARTIFACTS-OK and check-review PHASE67-REVIEW-OK, both at the fixed HEAD.
- **Committed in:** 490ce41b

---

**Total deviations:** 1 auto-fixed (1 blocking).
**Impact on plan:** minimal — a page-format requirement of the check-review gate; no evidence, rule, registration or scientific value changed.

## Issues Encountered

- **Commit-message cost figures were hand-summarized before the machine extraction on rows 3, 7 and 9, so those three bodies carry slightly off wall/rate figures** (row 3: body said 1275.8 s, record says 1277.3 s; row 7: body said 986.0 s / 6.449 ms, record says 1005.5 s / 6.556 ms; row 9: body said 1547.1 s / 10.114 ms, record says 1481.8 s / 9.668 ms). The committed record.json files are the authoritative cost evidence and the exact values are carried in the SUMMARY table above, in 67-EXP02-RESULT.md's tables and in review.json; no evidence file is affected. Rows 1, 2, 4, 5, 6, 8 and 10-15 bodies match their records.
- The transient extra `caffeinate` processes observed during row 6's preflight (a `-t 300` admission assertion and the `caffeinate -is` fit wrapper) belong to the harness's own launch machinery; the inter-row wake assertion was never duplicated.

## Known Stubs

None - no stubs, placeholders or unwired data paths; all 15 rows are measured publications and the review/result pages are complete.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- EXP-02 is complete end to end (design -> metadata -> timing -> budget -> 15 science rows -> review) on the registered continue route: **the EXP-03 rate ladder (67-10) is unblocked** under D-01 with check-review PHASE67-REVIEW-OK committed at 490ce41b.
- The observed unsettled endpoints (including the d12 control's own main-case endpoint at N=152900) are recorded, not acted on: the no-continuation policy forbids extending, retrying or re-sizing any run, and no scope change was proposed.
- The remaining amendment window closes 2026-11-04 07:30 America/Chicago; any later plan launching tonight must still pass its own per-launch admission arithmetic.

## Self-Check: PASSED

All 60 row evidence files exist on disk and are tracked (75 tracked files under evidence/exp02/science including the 15 registrations); all 17 evidence commits (09a60d00..490ce41b) exist in history in launch order; PHASE67-ALL-ROWS-OK, PHASE67-REVIEW-ARTIFACTS-OK and PHASE67-REVIEW-OK all pass at the final evidence HEAD; `git diff --check` clean at every commit; the working tree holds no uncommitted phase-67 evidence; the two user-owned dirty files (.planning/config.json, docs/work/designs/milestone_v2.2/50-valid-stage-0-re-run/2026-08-16-stage0-causal-front-halt-brief.md) were never staged or modified.

---
*Phase: 67-design-settings-ladders*
*Completed: 2026-11-04*
