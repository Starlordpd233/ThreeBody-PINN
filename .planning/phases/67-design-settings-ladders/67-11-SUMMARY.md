---
phase: 67-design-settings-ladders
plan: "11"
subsystem: verification-diagnostics
tags: [pinn, exp03, rate-ladder, science-rows, serial-launch, review, refuted-lead, scope49-pending]

# Dependency graph
requires:
  - phase: 67-design-settings-ladders (67-10)
    provides: the committed EXP-03 design, metadata, budget N=155100, science-matrix.json and all 15 science registrations
provides:
  - All 15 EXP-03 science rows measured, mechanically checked (PHASE67-ALL-ROWS-OK) and committed serially at the common N=155100 (record/attempt/power-gate/weights per row, one commit per row before the next launch)
  - The committed machine review (evidence/exp03/review.json, dependent_launch_allowed=false, scope49_disposition=proposal-pending) and the complete result page 67-EXP03-RESULT.md with every endpoint E/tier, same-window comparison scores, per-cadence per-layer similarity traces, matched contrasts, costs and the prediction/roadmap comparison
  - The reserved branch: a refuted lead was observed (lr1e-3 confirmed-worsening), so task 67-11-03's blocking-human checkpoint is OPEN awaiting the owner's SCOPE-49 instruction; EXP-04 (67-12) dependent work is blocked until the actual ruling; no ruling file exists yet
affects: [67-12 (blocked by the pending SCOPE-49 proposal), 67-13, 67-14, 67-15, 67-16]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
# Scale caveat: the realized diff is dominated by machine-written evidence
# (15 run records ~16.9k lines each, the 17.7k-line review.json and its
# byte-exact embed in the result page), not agent-authored text.
actuals:
  tokens: 1995664     # chars/4 over the realized text diff ddd241bf^..bfd85916 (7,982,656 bytes; weights binaries excluded)
  tasks: 2            # 67-11-01, 67-11-02 executed; 67-11-03 HALTED at its blocking-human owner checkpoint
  commits: 17         # 15 row commits + review/result + this docs commit (4 rows by the predecessor executor)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Continuation resume over a usage-cap death: an on-disk complete-but-uncommitted row is never relaunched — check-row (value-free) first, then commit exactly as prior rows; the exclusive first-write evidence identity stays intact."
    - "Serial science campaign identical to 67-08/67-09: per row, check-matrix -> AC/window/no-other-run eligibility -> previous row verified committed -> launch-row exactly once -> check-row (scores hidden) -> scoped cost-only inspection (attempt status, power source, wall, rate) -> commit the row's four files before the next launch."

key-files:
  created:
    - .planning/phases/67-design-settings-ladders/evidence/exp03/science/CASE/ARM/{record.json,attempt.json,power-gate.json,diagnostic.weights} (15 rows)
    - .planning/phases/67-design-settings-ladders/evidence/exp03/review.json
    - .planning/phases/67-design-settings-ladders/67-EXP03-RESULT.md
  modified:
    - .planning/STATE.md, .planning/ROADMAP.md, .planning/WINDOWS.md

key-decisions:
  - "All 15 science rows ran inside the owner amendment window (weekday launches through 2026-11-05 07:30 America/Chicago) on AC power with zero gate refusals: launches 2026-11-04 15:40:08 CST through 2026-11-05 02:24:15 CST, each exactly once through diagnostic_power and the outer supervisor, every attempt published, measured walls 2069-2385 s, total 32,185 s vs the 39,055.09 s experiment projection; every row inside its 3540 s cap."
  - "The observed EXP-03 branch is the REFUTED-LEAD reserved route: lr1e-3 is confirmed-worsening (worsening in all three cases with matching tier change and >=20% relative E effect in each, all six endpoints settled — main case E 1.4552 tier 0 vs control E 0.04069 tier 1, relative effect 34.76), so the registered rate-sensitivity-improves hypothesis is refuted at confirmation grade. lr3e-4 and lr3e-5 are direction-mixed (worsening/improvement/worsening; lr3e-4's repeat-seed arm endpoint unsettled). lr1e-5 worsens on all three cases but its repeat-seed endpoint is unsettled, so unsettled. Nothing is confirmed-improving; no favourable-main selection was made."
  - "Task 67-11-03 (blocking-human checkpoint) is OPEN by its own condition: the committed review reads dependent_launch_allowed=false with scope49_disposition=proposal-pending because a refuted lead was observed. No ruling file exists, no owner answer has been received, check-review is intentionally NOT run (it requires resolution of the pending proposal), and EXP-04 (67-12) dependent launches stay blocked until the actual owner instruction."
  - "No scientific value was screened during the run loop: check-row's value-free mechanical audit was the only per-row verdict, per-row inspection touched cost fields only (attempt status, power source, wall/rate), and no row or repeat was selected, extended or reordered after any result. Row 5 (completed on disk by the dying predecessor executor at 18:26 CST inside the amendment window) was verified read-only and committed as-is; it was never relaunched."

patterns-established:
  - "A refuted lead at confirmation grade is published as loudly as a confirmation: every declared arm appears in the result page (ties, small effects, mixed directions, unsettled and failed outcomes included) and the reserved SCOPE-49 question goes to the owner with the committed evidence."

requirements-completed: []  # EXP-03 stays open until the phase verification act: every 67-0N plan declares EXP-02..05 and the marks flip only when all declaring plans finish (shared-ID gate, 67-04/67-08 convention).

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "All 15 declared EXP-03 science rows (3 cases x 5 rate arms, case-major serial order) each launched exactly once at the common N=155100, mechanically checked with scores hidden, and committed as four artifacts per row before the next launch"
    requirement: EXP-03
    verification:
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-row per row (15x PHASE67-ROW-OK) and the plan's task-1 aggregate verify command (PHASE67-ALL-ROWS-OK)"
        status: pass
    human_judgment: false
  - id: D2
    description: "The committed review (review.json, dependent_launch_allowed=false, scope49 proposal-pending) and the complete result page exposing all 15 outcomes, every prospective contrast, convergence statuses, machine costs and the prediction/roadmap comparison, with the byte-exact review embedded; the conditional owner gate carried to task 67-11-03"
    requirement: EXP-03
    verification:
      - kind: other
        ref: "plan task-2 verify (PHASE67-REVIEW-ARTIFACTS-OK: both files committed at HEAD with byte-identical content, all six review fields present)"
        status: pass
      - kind: other
        ref: "python -B -m pinn.verification.diagnostic_phase67 check-review --experiment exp03 — DELIBERATELY UNRUN: requires the owner's ruling on the recorded proposal first (task 67-11-03, blocking-human; WINDOWS entry 5)"
        status: pending-owner
    human_judgment: true

# Metrics
duration: ~11h20m wall (2026-11-04 15:40 CST to 2026-11-05 03:05 CST; predecessor rows 1-5, continuation rows 5-commit through review; ~8h56m of it the 15 supervised launches)
completed: 2026-11-05
status: halted
---

# Phase 67 Plan 11: EXP-03 Rate Ladder Science Matrix — Execution & Review Summary

**All 15 EXP-03 science rows ran serially at the common N=155100 (each launched once, PHASE67-ROW-OK, committed before the next launch; total measured wall 32,185 s inside every cap), and the committed review reads the REFUTED-LEAD reserved route: lr1e-3 is confirmed-worsening — the registered rate-sensitivity-improves hypothesis is refuted at confirmation grade — so scope49_disposition=proposal-pending, dependent_launch_allowed=false, and the plan is HALTED at task 67-11-03 awaiting the owner's actual SCOPE-49 instruction. EXP-04 (67-12) is blocked until that ruling.**

## Performance

- **Duration:** rows 1-5 by the predecessor executor 2026-11-04 15:40-19:02 CST (died on a provider usage cap right after row 5's on-disk completion, before its commit); this continuation 2026-11-04 20:58 CST through 2026-11-05 03:05 CST (row-5 verify+commit, rows 6-15, review, close-out)
- **Tasks:** 2 executed; task 3 (conditional blocking-human checkpoint) OPEN awaiting the owner
- **Files:** 62 evidence/page files created (60 row artifacts + review.json + 67-EXP03-RESULT.md)

## Accomplishments

- Row 5 (main-1632-s42/lr1e-5) was recovered exactly as the continuation protocol requires: the predecessor's dying launch had completed on disk inside the amendment window (POWER-OK AC Power isoweekday=3 at 18:26:37 CST, attempt published, 155100 steps, wall 2158 s); this continuation ran check-row (PHASE67-ROW-OK, scores hidden) and committed the four artifacts (948e7951) without any relaunch — the exclusive evidence identity stayed single-use.
- Rows 6-15 ran with zero gate refusals: per row check-matrix (PHASE67-MATRIX-OK) -> AC/window admission inside the amendment window (POWER-OK AC Power; isoweekday=3 for rows 6-10, isoweekday=4 for rows 11-15) -> launch-row exactly once through the outer supervisor -> check-row PHASE67-ROW-OK -> commit the row's four files before the next launch. Task-1 aggregate verify: PHASE67-ALL-ROWS-OK.
- Task 67-11-02: review --experiment exp03 committed (PHASE67-REVIEW-WRITTEN allowed=False) with the complete result page 67-EXP03-RESULT.md (every endpoint E/tier/status for all 15 rows, same-window comparisons, per-cadence per-layer adjacent-time cosine traces, all four matched contrasts against each case's freshly registered lr1e-4 control, measured machine costs against projections, prediction-table and roadmap comparison, GAP-59-08 energy limitation explicit, byte-exact embedded review). Plan task-2 verify: PHASE67-REVIEW-ARTIFACTS-OK.
- The observed branch: lr1e-3 confirmed-worsening (refutes the registered improvement hypothesis at confirmation grade — worsening in all three cases, matching tier change and >=20% relative E effect in each, all endpoints settled); lr3e-4/lr3e-5 direction-mixed; lr1e-5 worsening but repeat-seed-unsettled. A refuted lead is a result-driven reserved decision under SCOPE-49: scope49_disposition=proposal-pending, dependent_launch_allowed=false. Task 67-11-03's blocking-human checkpoint is therefore OPEN; check-review was deliberately not run and EXP-04 (67-12) stays blocked.
- A backstop wake lock (caffeinate -i -s, 10 h) was held alongside the still-alive 67-08 assertion through the overnight rows; the launch machinery's own caffeinate/fit descendants were untouched.

## Task Commits

1. **Rows 1-4 (predecessor executor, 2026-11-04 16:27-18:26 CST)** - ddd241bf (r1 main-1632-s42/lr1e-3), 1d665848 (r2 lr3e-4), df40671e (r3 lr1e-4), 4c7c8d24 (r4 lr3e-5).
2. **Row 5 recovery (this continuation)** - 948e7951 (evidence) - inherited on-disk artifacts checked read-only and committed; never relaunched.
3. **Rows 6-10 (repeat-851-s42)** - 892b728f (lr1e-3), 8575358c (lr3e-4), 23df087c (lr1e-4), 7c9918a3 (lr3e-5), abaed679 (lr1e-5).
4. **Rows 11-15 (repeat-1632-s41)** - d6929b08 (lr1e-3), 52624dae (lr3e-4), 623f8df6 (lr1e-4), 93d631cf (lr3e-5), 517475e1 (lr1e-5).
5. **Task 67-11-02 review** - bfd85916 (evidence) - review.json + 67-EXP03-RESULT.md; PHASE67-REVIEW-ARTIFACTS-OK.
6. **Plan metadata:** this docs commit (SUMMARY + STATE/ROADMAP hand-edits + WINDOWS entry 5).

## Files Created/Modified

- `evidence/exp03/science/{main-1632-s42,repeat-851-s42,repeat-1632-s41}/{lr1e-3,lr3e-4,lr1e-4,lr3e-5,lr1e-5}/` - 15 rows x (record.json, attempt.json, power-gate.json, diagnostic.weights)
- `evidence/exp03/review.json`, `67-EXP03-RESULT.md` - the committed review and its embedding result page
- `.planning/STATE.md`, `.planning/ROADMAP.md` - plan tracking hand-edits (also correcting 67-10's completion, which its minimal close-out had not recorded)
- `.planning/WINDOWS.md` - entry 5 (unrun check-review pending the owner ruling)

## Decisions Made

- The continuation treated the predecessor's completed-but-uncommitted row 5 as evidence to verify and commit, never as a burned or re-runnable directory: the attempt identity is exclusive and single-use, and check-row's value-free audit confirmed mechanical validity before the commit.
- The reserved route is presented, not papered over: the refuted lead is published with every other arm's outcome, the proposal is recorded in the committed review, and the owner question is carried to the checkpoint with the evidence — no scheduler, extension, rescue or scope change was invented to avoid the ask.
- Row-cost provenance for commit messages used only attempt.json/fit-telemetry cost fields (steps, ms/step, whole-launch wall, power source, weekday); no score, loss, tier or cosine value was read during the run loop.

## Deviations from Plan

None — the plan executed exactly as written across the two executor sessions. (The predecessor's usage-cap death and the row-5 recovery were a continuation of the plan's own serial protocol, not a deviation; the plan's reversibility contract explicitly preserves completed attempts.)

## Issues Encountered

- The predecessor executor died on a provider usage cap after row 5's on-disk completion (18:26-19:02 CST) but before its commit; state at this continuation's start was verified by the orchestrator (HEAD 4c7c8d24, clean tree) and row 5 was recovered as described above.
- 67-10's minimal close-out (5642f869) committed only its SUMMARY, leaving STATE.md/ROADMAP.md stale at "67-09 complete"; this plan's docs commit corrects that drift (67-10 marked complete).
- The torch UserWarning at diagnostic_fit.py:795 (requires_grad tensor to float) appears in every launch log; it is pre-existing, informational, and outside the harness freeze — recorded here only for the record.

## Known Stubs

None - every row artifact, the review and the result page are complete machine-generated evidence; no placeholder or unwired value exists.

## User Setup Required

**The owner ruling on the recorded EXP-03 SCOPE-49 proposal (task 67-11-03, blocking-human).** The committed review reads: "a refuted lead or an out-of-rule result was observed; the owner decides under SCOPE-49 whether the remaining experiments run, change or stop." The checkpoint presents the committed evidence and the agent's plain-language recommendation; only an actual owner instruction (authorize / direct-different / hold) resumes the affected work. No response means the task stays paused.

## Next Phase Readiness

- Wave 11 (67-12, EXP-04) is BLOCKED by the pending SCOPE-49 proposal exactly as designed (a pending proposal blocks only the dependent experiment); 67-13..67-15 depend on their predecessors; 67-16's audit will verify the resolved state.
- Phase 68 (Yardstick) depends on nothing in v2.5's experiments and may proceed independently of this halt.
- The held-out evaluation remains unspent; no source symbol, flag, setting, registration or pass bar changed in this plan.

## Self-Check: PASSED

All 62 created evidence/page files exist on disk (15 rows x 4 artifacts beside their committed registrations, review.json, 67-EXP03-RESULT.md, this SUMMARY); all 16 evidence commits exist in history (ddd241bf, 1d665848, df40671e, 4c7c8d24, 948e7951, 892b728f, 8575358c, 23df087c, 7c9918a3, abaed679, d6929b08, 52624dae, 623f8df6, 93d631cf, 517475e1, bfd85916); both task verifies re-ran green at bfd85916 (PHASE67-ALL-ROWS-OK, PHASE67-REVIEW-ARTIFACTS-OK); check-review remains intentionally unrun pending the owner ruling (WINDOWS entry 5).
