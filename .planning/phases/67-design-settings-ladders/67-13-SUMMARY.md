---
phase: 67-design-settings-ladders
plan: "13"
subsystem: verification-diagnostics
tags: [pinn, exp04, time-input-ladder, science-rows, serial-launch, review, unsettled-branch]

requires:
  - phase: 67-design-settings-ladders (67-12)
    provides: the frozen EXP-04 pre-registration — committed design, budget (common N=112700), 18-row science matrix and all 18 science registrations before any science launch
provides:
  - All 18 EXP-04 science rows run exactly once at the registered common N=112700 (200 warmup) under the 3540-second whole-launch cap, each mechanically checked with scores hidden (PHASE67-ROW-OK) and committed as four artifacts beside its registration before the next launch (3517e1dc..c04bb428); zero deferred rows, zero burned directories, zero retries
  - The committed EXP-04 review and original result page (3af7a831): every declared arm's endpoint E/tier/endpoint-status on all three cases, the four matched encoded-vs-raw contrasts, the prediction/roadmap comparison and the SCOPE-49 disposition — all four contrasts unsettled, nothing confirmed in either direction, dependent_launch_allowed=true on the registered unsettled branch
  - The phase gate PHASE67-REVIEW-OK green, admitting the EXP-05 experiment under its existing committed registration
affects: [67-14 (EXP-05), 67-15, 67-16, Phase 68 energy adjudication]

# Actuals (#2632) — pairs with the plan's `estimate` (9000 est / 18000 raw tokens, 3 tasks).
# Scale caveat: the realized diff is dominated by machine-written evidence
# (18 run records ~450 KB each plus the ~375 KB review pair); no harness code
# changed in this plan.
actuals:
  tokens: 2213652     # chars/4 over the realized text diff 46e7ae0d..HEAD (8,854,608 bytes; weights binaries excluded)
  tasks: 3            # tasks 1-2 executed; task 3 skipped by its own registered condition (dependent_launch_allowed=true)
  commits: 20         # 18 row commits + 1 review/result commit + this docs close-out

tech-stack:
  added: []
  patterns:
    - "Serial science campaign at the registered N: per row, check-matrix -> AC/window/no-other-run eligibility -> previous row verified committed -> launch-row exactly once -> check-row (value-free) -> cost-only inspection -> commit the row's four files before the next launch, all inside a session-level caffeinate wake lock on top of the per-launch caffeinate."
    - "No-selection discipline held end to end: no row, repeat or arm was selected, extended or reordered after any result; per-row inspection touched cost fields only (attempt status, power source, wall/seconds-per-step); the review command was the first and only score reader."

key-files:
  created:
    - .planning/phases/67-design-settings-ladders/evidence/exp04/science/CASE/ARM/{record.json,attempt.json,power-gate.json,diagnostic.weights} (18 rows)
    - .planning/phases/67-design-settings-ladders/evidence/exp04/review.json
    - .planning/phases/67-design-settings-ladders/67-EXP04-RESULT.md
  modified:
    - .planning/STATE.md, .planning/ROADMAP.md, .planning/state.json, .planning/agent-history.json (plan tracking)

key-decisions:
  - "All 18 registered rows launched exactly once in the committed case-major matrix order (main-1632-s42, repeat-851-s42, repeat-1632-s41 x locked-raw/locked-f1/locked-f12/exp01-raw/exp01-f1/exp01-f12), each on AC power inside the Saturday weekend window (isoweekday 6, 12:13-18:22 CST), each a complete 112700-step attempt published under the 3540-second cap; measured walls 442-1987 s (total 19695 s vs the 25880.3 s projection). The 851 encoded arms launched through the orbit-aware variants (exp04-locked-f1-851 etc.) exactly as the registrations declare, and their check-rows read clean on the first try after 4ea20b05."
  - "The review read the committed evidence under the unchanged prospective rule and recorded the unsettled branch: all four encoded contrasts (each against its own backbone's raw control) are unsettled — several endpoints were still improving by more than the registered five percent when their budget ended, and unsettled endpoints block confirmation regardless of direction. Direction is worsening on the main case and the 851 repeat for all four arms, with an opposed improvement direction on the seed-41 repeat for both locked arms. Nothing is confirmed in either direction; no main-only or single-repeat reading is presented; no continuation, rescue or re-sizing ran (no-continuation policy)."
  - "scope49_disposition none and dependent_launch_allowed=true: the unsettled branch is registered and equally recorded, so the conditional task 3 owner checkpoint is skipped by its own condition with no ruling file created; EXP-05 proceeds under its existing committed registration after PHASE67-REVIEW-OK."

coverage:
  - id: D1
    description: "Every EXP-04 arm on all three registered cases has complete committed science evidence at the prospective common N, with frozen scorer, pass bars and production settings unchanged"
    requirement: EXP-04
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-row per row (18x PHASE67-ROW-OK) and the plan's all-18 verify (PHASE67-ALL-ROWS-OK); check-budget PHASE67-BUDGET-OK and check-matrix --kind science PHASE67-MATRIX-OK re-verified before every launch"
        status: pass
    human_judgment: false
  - id: D2
    description: "The result is reviewed against the committed prediction and roadmap with matched contrasts, all outcomes published, and the conditional scope authority resolved by the registered branch itself (no reserved proposal, no ruling needed)"
    requirement: EXP-04
    verification:
      - kind: other
        ref: "review --experiment exp04 (PHASE67-REVIEW-WRITTEN allowed=True); plan task-2 verify PHASE67-REVIEW-ARTIFACTS-OK; check-review PHASE67-REVIEW-OK"
        status: pass
    human_judgment: false

duration: ~6.5 h wall (2026-11-07 12:11-18:40 CST, single executor session; 18 supervised launches totalling 19695 s plus per-row checks/commits and the review)
completed: 2026-11-07
status: complete
---

# Phase 67 Plan 13: EXP-04 Science Run & Review Summary

**All 18 EXP-04 time-input-ladder science rows ran exactly once at the registered common N=112700 under the 3540-second cap (each PHASE67-ROW-OK with scores hidden, committed as four artifacts before the next launch, zero deferred/burned rows), and the registered review read the committed evidence under the unchanged prospective rule: all four encoded-vs-raw contrasts unsettled, nothing confirmed in either direction, dependent_launch_allowed=true on the registered unsettled branch — PHASE67-REVIEW-OK admits EXP-05 with no owner proposal.**

## Performance

- **Duration:** 2026-11-07 12:11-18:40 CST (~6.5 h; 18 serial supervised launches totalling 19695 s, rows 442-1987 s each against the 3540 s cap, experiment projection was 25880.3 s)
- **Tasks:** 2 executed + 1 conditional skipped by its own registered condition
- **Commits:** 18 row commits (3517e1dc..c04bb428) + 1 review commit (3af7a831) + this docs close-out

## Accomplishments

- Task 67-13-01: all 18 registered science rows launched exactly once in the committed case-major matrix order, one row at a time, never in parallel, no retry/resume/continuation. Per row: check-matrix (PHASE67-MATRIX-OK), AC-power and weekend-window eligibility (POWER-OK AC Power, isoweekday 6 Saturday), absence of any other run, previous row verified committed, launch-row through diagnostic_power and the outer supervisor, check-row (PHASE67-ROW-OK, the only per-row verdict — its audit hides scores), cost-only inspection, then one commit of exactly the row's four artifacts before the next launch. The plan's all-18 verify prints PHASE67-ALL-ROWS-OK. The session-level caffeinate wake lock held from before row 1 to after the review; the machine stayed on AC power at 100% throughout.
- Task 67-13-02: with all rows committed, the registered review command read every row through its registration-bound reader and wrote the original result page and review.json (PHASE67-REVIEW-WRITTEN allowed=True). Both artifacts committed (3af7a831); the plan's verify prints PHASE67-REVIEW-ARTIFACTS-OK.
- Task 67-13-03 (conditional checkpoint): its condition — dependent_launch_allowed=false on a reserved SCOPE-47/49 or resource decision — does not hold (scope49_disposition none, dependent_launch_allowed=true), so the checkpoint is skipped exactly as its resume-signal specifies, without requesting an answer and without creating 67-EXP04-RULING.md.
- Phase verification gate: check-review --experiment exp04 prints PHASE67-REVIEW-OK; the EXP-05 experiment is admitted under its existing committed registration.

## Result Reading (summary; exact values live in review.json / 67-EXP04-RESULT.md)

- Under the unchanged prospective rule (direction in all three cases + matching tier change or >=20 percent relative E effect in each, all six endpoints settled and clean; final-quarter relative E improvement strictly above five percent leaves an endpoint unsettled), every one of the four registered encoded contrasts reads **unsettled**: unsettled endpoints block confirmation in both directions.
- Direction pattern across cases: worsening on the main case and the 851 system repeat for all four encoded arms; the two locked arms show an opposed improvement direction on the seed-41 repeat (an opposed repeat is exactly what the registered rule refuses to confirm on). The exp01-backbone arms show worsening on all three cases with relative effects far above the twenty-percent line — recorded as observed fit, not confirmation, because confirmation requires settled, clean endpoints in the improving direction.
- Nothing is presented as confirmation: no main-only result, no tie, no opposed repeat, no unsettled endpoint and no small effect is promoted. Loss stays context; adjacent-time hidden-state cosine stays associated evidence only. GAP-59-08's energy limitation (E is the frozen scorecard's position-error score; no energy bar adjudicated here) and the one-orbit no-new-IC generalization limitation stay explicit.
- scope49_disposition none / dependent_launch_allowed=true: the unsettled branch is registered and equally recorded; the no-continuation policy extended nothing; no scope, pass-bar, registration or roadmap change is proposed. The frozen scorer, pass bars, production settings and all historical evidence remain unchanged (D-11/D-12).

## Task Commits

1. **Rows 1-6, main-1632-s42** - 3517e1dc (locked-raw), 599206d9 (locked-f1), d99e9042 (locked-f12), add4fe72 (exp01-raw), 31351774 (exp01-f1), 8597e580 (exp01-f12).
2. **Rows 7-12, repeat-851-s42** - e560e309 (locked-raw), 2e0bc7eb (locked-f1), ffbbf3f4 (locked-f12), a5719fbb (exp01-raw), 279a5266 (exp01-f1), 646f43c5 (exp01-f12); the encoded rows launched through the orbit-aware 851 variants exactly as registered.
3. **Rows 13-18, repeat-1632-s41** - 23a95327 (locked-raw), 241f70e9 (locked-f1), 7dc72f11 (locked-f12), 114f5d43 (exp01-raw), 5cdffcaa (exp01-f1), c04bb428 (exp01-f12, final).
4. **Review + result** - 3af7a831 (evidence) - 67-EXP04-RESULT.md + evidence/exp04/review.json; PHASE67-REVIEW-ARTIFACTS-OK, PHASE67-REVIEW-OK.
5. **Plan close-out:** this docs commit (SUMMARY + STATE.md/ROADMAP.md + on-disk state files).

## Files Created

- `evidence/exp04/science/{main-1632-s42,repeat-851-s42,repeat-1632-s41}/{locked-raw,locked-f1,locked-f12,exp01-raw,exp01-f1,exp01-f12}/` - 18 rows x (record.json, attempt.json, power-gate.json, diagnostic.weights) beside their committed registrations
- `evidence/exp04/review.json`, `67-EXP04-RESULT.md` - the original generated review and result page

## Decisions Made

- No scientific value was screened during the run loop: check-row's value-free mechanical audit was the only per-row verdict, per-row inspection touched cost fields only, and the review command was the first and only score reader. The prospective design was never altered by any result.
- The review was committed with the generated page preserved verbatim (original review bytes are what check-review digests); the narrative reading above cites it rather than replacing it.

## Deviations from Plan

None - the plan executed exactly as written. No harness defect surfaced (the 67-12 reader fixes 3d640feb/4ea20b05 were committed precedent and were neither redone nor reverted; the 851 orbit-aware rows checked clean on their first check-row). No POWER-REFUSED, no battery event, no burned directory, no auth gate.

## Issues Encountered

- The known pre-existing informational UserWarning at diagnostic_fit.py:831 appeared in every launch log (recorded by 67-11/67-12; outside the harness freeze; informational only).
- Rows ran faster than the timing-based projections (measured total 19695 s vs 25880.3 s projected; the worst-projected row, repeat-851-s42/locked-f12, measured 1587.0 s vs 2653.94 s projected). All recorded costs are per-row measured values in the committed attempt records; the registered N and cadences were untouched.

## Known Stubs

None - every row artifact, the review and the result page are complete machine-generated evidence; no placeholder or unwired value exists.

## Next Phase Readiness

- EXP-05 (67-14) is unblocked: PHASE67-REVIEW-OK is green at 3af7a831 and the dependent-launch admission verifies the committed review with no pending proposal.
- The EXP-04 verdict carried into dependent work: the encoded harmonic input is NOT a confirmed improvement on either backbone within the registered finite budget — the unsettled endpoints and the opposed seed-41 repeat for the locked arms mean no input-design change is justified by this evidence, and the registered unsettled branch records that equally.

## Self-Check: PASSED

All 18 row directories contain their four committed artifacts beside their registrations; review.json and 67-EXP04-RESULT.md exist and are byte-identical to HEAD (task-2 verify re-run green); all 20 plan commits exist in history (3517e1dc, 599206d9, d99e9042, add4fe72, 31351774, 8597e580, e560e309, 2e0bc7eb, ffbbf3f4, a5719fbb, 279a5266, 646f43c5, 23a95327, 241f70e9, 7dc72f11, 114f5d43, 5cdffcaa, c04bb428, 3af7a831, this docs commit); PHASE67-ALL-ROWS-OK, PHASE67-REVIEW-ARTIFACTS-OK and PHASE67-REVIEW-OK all green at final HEAD; the phase67 suite re-ran 256 tests OK at the settled bytes; `git diff --check` clean at every commit.

---
*Phase: 67-design-settings-ladders*
*Completed: 2026-11-07*
