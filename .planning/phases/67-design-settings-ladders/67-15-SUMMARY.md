---
phase: 67-design-settings-ladders
plan: "15"
subsystem: verification-diagnostics
tags: [pinn, exp05, window-ladder, science-rows, serial-launch, review, unsettled-branch]

requires:
  - phase: 67-design-settings-ladders (67-14)
    provides: the committed EXP-05 pre-registration (design trio, metadata capture, 12-row timing matrix, cost-only Plan04 budget common N=148700, prediction page, science matrix and all 12 science registrations frozen at 79587171 before any science launch)
provides:
  - All 12 EXP-05 signed-lap window-ladder science rows measured exactly once at the registered common N=148700 under the 3540-second whole-launch cap, serially in the case-major matrix order, each mechanically checked with scores hidden (PHASE67-ROW-OK) and committed as its four artifacts before the next launch (commits 678bf333..3479ef68); zero deferred rows, zero burned directories, no retry/resume/continuation, no post-result selection
  - The committed EXP-05 review and original result page (3b19801c): every arm's E/tier/endpoint-status on all three cases, the three matched lap1/lap2/lap5-vs-lap10 contrasts, the prediction/roadmap comparison and the SCOPE-49 disposition — all three contrasts unsettled (improvement direction on all nine case-contrast cells with every relative E effect qualifying, but unsettled endpoints block confirmation), confirmed empty, dependent_launch_allowed=true on the registered unsettled branch, no scope proposal
  - The phase verification gate for the EXP-05 experiment: check-review prints PHASE67-REVIEW-OK and admits 67-16 evidence closure with no owner ruling (67-EXP05-RULING.md intentionally absent on the in-scope continue route)
affects: [67-16 (phase audit/close-out), Phase 68 energy adjudication]

# Actuals (#2632) — pairs with the plan's `estimate` (9000 est / 18000 raw tokens, 3 tasks).
# Scale caveat: the realized diff is dominated by machine-written evidence
# (12 run records ~100-570 KB each plus the ~500 KB review pair); the weights
# binaries are excluded. No harness code changed in this plan.
actuals:
  tokens: 868598     # chars/4 over the realized text diff 4b8b9b82..HEAD (3,474,390 bytes; weights binaries excluded)
  tasks: 2           # 67-15-01 and 67-15-02 executed; 67-15-03 skipped by its own registered condition (dependent_launch_allowed=true)
  commits: 14        # 12 row commits + 1 review/result commit + this docs close-out

tech-stack:
  added: []
  patterns:
    - "Pre-registered ladder execution at the frozen common N: per row, check-matrix -> AC/window/no-other-run eligibility -> previous row verified committed -> launch-row exactly once through diagnostic_power and the outer supervisor -> check-row (value-free) -> cost-only inspection -> one commit of the row's four artifacts before the next launch, all inside a session-level caffeinate wake lock on top of the per-launch caffeinate."
    - "The registered review is the first and only score reader: the generated result page is committed verbatim and the executor's narrative cites it rather than replacing it, so the original review bytes stay what check-review digests."

key-files:
  created:
    - .planning/phases/67-design-settings-ladders/evidence/exp05/science/CASE/ARM/{record.json,attempt.json,power-gate.json,diagnostic.weights} (12 rows, beside their pre-committed registration.json)
    - .planning/phases/67-design-settings-ladders/evidence/exp05/review.json
    - .planning/phases/67-design-settings-ladders/67-EXP05-RESULT.md
  modified:
    - .planning/STATE.md, .planning/ROADMAP.md (plan tracking)

key-decisions:
  - "No scientific value was screened during the run loop: check-row's value-free mechanical audit was the only per-row verdict, per-row inspection touched cost fields only (attempt status, power source, wall/seconds-per-step), and the review command was the first and only score reader. The prospective design was never altered by any result."
  - "The review read the committed evidence under the unchanged prospective rule and recorded the unsettled branch: all three contrasts are unsettled because unsettled endpoints block confirmation regardless of direction — the main case's lap10 control and all three of its short arms were still improving by more than the registered five percent when their budgets ended, and the repeat-system case's lap10 control was likewise unsettled. Nothing is confirmed in either direction; no continuation, rescue or re-sizing ran (no-continuation policy); no scope change is proposed, so the conditional owner checkpoint is skipped without a ruling file."

coverage:
  - id: D1
    description: "Every declared science row launched exactly once at the registered common N=148700 (200 warmup) with the registered five similarity events and three score events, serially in the committed case-major matrix order, on AC power inside the weekend window, each mechanically checked with scores hidden and committed as four artifacts before the next launch"
    requirement: EXP-05
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-row per row (12x PHASE67-ROW-OK), check-matrix --experiment exp05 --kind science (PHASE67-MATRIX-OK) before each launch, check-budget (PHASE67-BUDGET-OK) at start, and the plan's all-rows verify (PHASE67-ALL-ROWS-OK)"
        status: pass
    human_judgment: false
  - id: D2
    description: "The result reviewed against the committed prediction and roadmap with matched contrasts, every declared arm published, and the conditional scope authority resolved by the registered branch itself (unsettled: dependent_launch_allowed=true, no proposal, no ruling)"
    requirement: EXP-05
    verification:
      - kind: other
        ref: "review --experiment exp05 (PHASE67-REVIEW-WRITTEN allowed=True); plan task-2 verify PHASE67-REVIEW-ARTIFACTS-OK; check-review PHASE67-REVIEW-OK"
        status: pass
    human_judgment: false

duration: ~9h19m wall (2026-11-07 20:08 - 2026-11-08 05:27 CST, single executor session; 12 supervised launches totalling 29246 s plus per-row checks/commits and the review)
completed: 2026-11-08
status: complete
---

# Phase 67 Plan 15: EXP-05 Science Run & Review — Summary

**All 12 EXP-05 window-ladder science rows ran exactly once at the registered common N=148700 under the 3540-second cap (each PHASE67-ROW-OK with scores hidden, committed as four artifacts before the next launch, zero deferred/burned rows), and the registered review read the committed evidence under the unchanged prospective rule: all three lap1/lap2/lap5-vs-lap10 contrasts unsettled — the improvement direction on all nine case-contrast cells with every relative E effect qualifying (0.14 to 0.88), but unsettled endpoints block confirmation — nothing confirmed in either direction, dependent_launch_allowed=true on the registered unsettled branch, no owner proposal, no ruling file (PHASE67-REVIEW-OK admits 67-16 evidence closure).**

## Performance

- **Duration:** 2026-11-07 20:08 - 2026-11-08 05:27 CST (~9 h 19 m; 12 serial supervised launches totalling 29246 s of whole-launch wall against the 3540 s cap each, plus per-row checks/commits and the review)
- **Tasks:** 2 of 3 executed (task 03 is the conditional owner checkpoint; its own registered condition — dependent_launch_allowed=true — skips it without a ruling)
- **Commits:** 12 row commits (678bf333..3479ef68) + 1 review commit (3b19801c) + this docs close-out

## Accomplishments

- Task 67-15-01: all 12 registered science rows launched exactly once in the committed case-major matrix order (main-1632-s42, repeat-851-s42, repeat-1632-s41 x lap1/lap2/lap5/lap10), one row at a time, never in parallel, no retry/resume/continuation. Per row: check-budget at the very start, then check-matrix (PHASE67-MATRIX-OK), AC-power and weekend-window eligibility (POWER-OK AC Power; Saturday isoweekday 6 for rows 1-6, Sunday isoweekday 7 for rows 7-12), absence of any other run, previous row verified committed, launch-row through diagnostic_power and the outer supervisor, check-row (PHASE67-ROW-OK, the only per-row verdict — its audit hides scores), cost-only inspection, then one commit of exactly the row's four artifacts before the next launch. Every row ran the full 148700 optimizer steps (200 warmup) with the registered five similarity events [0, 37175, 74350, 111525, 148700] and three score events [74350, 111525, 148700]. The plan's all-rows verify prints PHASE67-ALL-ROWS-OK. A session-level caffeinate wake lock was held across the whole ladder (restarted seven times when the harness killed the background task; every launch's own per-launch caffeinate was never interrupted and no launch was affected).
- Task 67-15-02: with all rows committed, the registered review command read every row through its registration-bound reader and wrote the original result page and review.json (PHASE67-REVIEW-WRITTEN allowed=True). Both artifacts committed verbatim (3b19801c); the plan's verify prints PHASE67-REVIEW-ARTIFACTS-OK. check-review prints PHASE67-REVIEW-OK — the EXP-05 phase verification gate is green and 67-16 evidence closure is admitted.
- Task 67-15-03: skipped by its own registered condition. The committed review's dependent_launch_allowed=true routes through the registered unsettled branch (equally recorded, no continuation runs, no scope change proposed: scope49_disposition none, proposed_change none), so no owner question was raised and 67-EXP05-RULING.md was intentionally not created.

## Result Reading (summary; exact values live in review.json / 67-EXP05-RESULT.md)

- **Confirmed: nothing.** All three declared contrasts (lap1, lap2, lap5 against their case's lap10 control) read unsettled under the unchanged prospective rule; `confirmed` is empty and the confirmation label is unsettled for every contrast.
- **Direction is uniform and hypothesis-aligned:** improvement on all nine case-contrast cells (each short arm's endpoint E below its case's lap10 control). Every relative E effect qualifies (all above the exact 20 percent line; they range from ~0.14 to ~0.88), and the frozen tier improves only on the seed-41 repeat (tier_direction improved for all three arms there; unchanged elsewhere). But qualification of the effect side is not confirmation: confirmation requires the same direction in all three cases with all paired endpoints settled and clean.
- **Unsettled endpoints are what blocks confirmation.** On the main case, every endpoint — the three short arms and the lap10 control — was still improving by more than the registered five percent when its budget ended (all six unsettled). On the repeat-system case, the three short arms settled but their lap10 control did not. Only the seed-41 repeat case is fully settled (all arms and its control), with tier improvements on the short arms. Because the main and repeat-system controls are unsettled, no contrast can confirm, and the no-continuation policy extends nothing.
- **What this says about the windows, carefully:** a short prefix reaching its exact first-crossing endpoint is an observed fit, never a full-window success — the ten-lap arm uses its actual signed first-crossing endpoint on each system (0.95/1.89/4.76/9.51 on 1632; 0.54/1.08/2.68/5.37 on 851), not an exact [0, 10] window. On the main case, ten laps did not settle within the budget and neither did the short windows (all still improving) — so the ladder shows the direction of the window effect at the frozen budget, not a settled endpoint anywhere on that case. The census mean period remains only a labelled rough planning estimate; the exact per-window baselines were recomputed by the committed metadata. Adjacent-time hidden-state similarity stays associated evidence only (no cosine threshold, no causal claim); loss stays context; GAP-59-08 stays explicit (E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here).
- **Costs:** 12 whole-launch walls 2012/1957/2006/2226/2203/2629/2791/2874/2593/2699/2899/2357 s (total 29246 s ≈ 8.12 h), every row inside the 3540 s cap and inside the remaining-window allowance at its launch (window closes Sunday 2026-11-08 22:00 America/Chicago). Overnight rows ran up to ~13 percent above the timing projection (seconds_per_step up to 0.019464 vs the 0.0131-0.0142 timing basis) yet kept comfortable cap margin; the metadata capture and timing rows were spent in 67-14 and are recorded there. No failed attempts.

## Task Commits

1. **Rows 1-4 (main case)** - 678bf333 (lap1), 3e98c341 (lap2), 75629a49 (lap5), 5b708f7e (lap10 control) — each the row's record.json, attempt.json, power-gate.json and diagnostic.weights; PHASE67-ROW-OK per row with scores hidden.
2. **Rows 5-8 (851 repeat case)** - aee42c43 (lap1), 6f769edd (lap2), 884d3862 (lap5), 58662492 (lap10 control).
3. **Rows 9-12 (seed-41 repeat case)** - 249946a3 (lap1), 0bab7d77 (lap2), 89a5fd82 (lap5), 3479ef68 (lap10 control, final row).
4. **Review + result** - 3b19801c (evidence) - 67-EXP05-RESULT.md + evidence/exp05/review.json; PHASE67-REVIEW-ARTIFACTS-OK, PHASE67-REVIEW-OK.
5. **Plan close-out:** this docs commit (SUMMARY + STATE.md/ROADMAP.md).

**Plan metadata:** the task-03 checkpoint was skipped by its own registered condition (no commit: a skipped conditional creates no artifact).

## Files Created/Modified

- `evidence/exp05/science/CASE/ARM/` — 12 rows x 4 new artifacts (record.json, attempt.json, power-gate.json, diagnostic.weights) beside their pre-committed registration.json
- `evidence/exp05/review.json`, `67-EXP05-RESULT.md` — the original generated review and result page
- `.planning/STATE.md`, `.planning/ROADMAP.md` — plan tracking

## Decisions Made

- No scientific value was screened during the run loop: check-row's value-free mechanical audit was the only per-row verdict, per-row inspection touched cost fields only, and the review command was the first and only score reader. The prospective design was never altered by any result; no arm was selected, extended, reordered or rescued.
- The review was committed with the generated page preserved verbatim (the original review bytes are what check-review digests); the narrative reading above cites it rather than replacing it.
- The task-03 owner checkpoint was skipped because the committed review itself resolves the conditional: dependent_launch_allowed=true on the registered unsettled branch. No ruling file was created, per the plan's explicit resume-signal contract.

## Deviations from Plan

None — plan executed exactly as written. No harness defect surfaced (the 67-14 materialization fixes held end to end across all 12 real launches); no gate refused; no row failed, deferred or burned; no registered design, prediction, setting or pass bar changed.

## Issues Encountered

- The session-level caffeinate background task was killed seven times by the harness during the ladder (between rows and during waits); each kill was detected from the task notification and the wake lock was restarted immediately, always while the in-flight launch's own per-launch caffeinate still held. No launch was interrupted and no machine sleep occurred (every attempt completed under its cap).
- Overnight rows ran measurably slower than the timing projection (row 6: 2629 s vs 2489 s projected; rows 7/8/11 up to 2899 s), keeping every row inside the cap with margin and the experiment inside the weekend window; the committed per-row projections were never edited in response.
- The known pre-existing torch requires_grad UserWarning at diagnostic_fit.py:876 appears in every launch log; informational, pre-existing (recorded by 67-11/67-12/67-14), outside the harness freeze.

## Known Stubs

None — every artifact (12 rows x 4 files, review.json, RESULT.md) is complete machine-generated evidence; no placeholder or unwired value exists.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- 67-16 (evidence closure/phase audit) is admitted: check-review --experiment exp05 prints PHASE67-REVIEW-OK, the review is committed with dependent_launch_allowed=true, no pending proposal exists, and 67-EXP05-RULING.md is intentionally absent on the in-scope continue route.
- EXP-05's outcome for the phase narrative: the window ladder is directionally consistent with the pre-registered hypothesis (shorter window improves the fit at the locked settings) on all three cases with large qualifying effects, but the registered confirmation rule is not met — unsettled endpoints block it on two of three cases, so the honest reading is "directionally supportive, unsettled at this budget, nothing confirmed". That is the registered unsettled branch: equally recorded, no continuation, no scope change. Phase 68 energy adjudication inherits this context; EXP-05 does not by itself establish a production window change.
- The EXP requirement marks (EXP-01..05) stay Pending until the phase verification act per the shared-ID gate convention recorded in 67-05/67-06.
- No held-out evaluation was spent, no source symbol/flag/scoring bar/package was added, and every historical byte is preserved.

## Self-Check: PASSED

All created evidence/page files exist on disk (12 rows x 4 artifacts beside their committed registrations, review.json, 67-EXP05-RESULT.md, this SUMMARY); all 13 pre-close-out commits exist in history (678bf333, 3e98c341, 75629a49, 5b708f7e, aee42c43, 6f769edd, 884d3862, 58662492, 249946a3, 0bab7d77, 89a5fd82, 3479ef68, 3b19801c); all gates ran green at the settled bytes (PHASE67-BUDGET-OK and PHASE67-MATRIX-OK science at start and before each launch, PHASE67-ROW-OK x12, PHASE67-ALL-ROWS-OK, PHASE67-REVIEW-WRITTEN allowed=True, PHASE67-REVIEW-ARTIFACTS-OK, PHASE67-REVIEW-OK).

---

*Phase: 67-design-settings-ladders*
*Completed: 2026-11-08*
