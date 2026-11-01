---
phase: 66-small-network-control
plan: "05"
status: halted
requires:
  - phase: 66-small-network-control (plan 04)
    provides: "the three verified EXP-01 run records under evidence/exp01/ (main-1632-s42, repeat-851-s42, repeat-1632-s41), each 465,000 steps, check-run-clean, committed at a546016b / 3dc3646a / 277c25ce, with no score read in 66-04"
provides:
  - "66-RESULT.md (89045a7f): the EXP-01 branch derived mechanically by diagnostic_phase66 review over the three committed run directories — all three runs tier1, confirmation confirmed, route phase67-as-planned — in plain language with every number cited to a committed record by path and SHA-256, the frozen reading, the SCOPE-49 proposal (none), the identifiability limits, harness provenance and the evidence index; RESULT-PAGE-OK"
affects: [owner-checkpoint-1, 66-05-continuation, phase-67]
actuals:
  tokens: 8000
  tasks: 1
  commits: 3
tech-stack:
  added: []
  patterns:
    - "mechanical branch derivation: every label, the confirmation, the route and every number copied from read-run/review/check-run output over the committed directories; the only computed figures are the plan-mandated band edges (0.95/1.05 x the record's own E_const), the loss quarter change, wall times and machine hours, each scripted and cited"
key-files:
  created:
    - .planning/phases/66-small-network-control/66-RESULT.md
  modified: []
key-decisions:
  - "None - followed the plan as specified: the branch was derived mechanically from the review tool output only (all three runs tier1, confirmed, phase67-as-planned, which proposes no plan change); the owner checkpoint was not pre-answered and 66-CHECKPOINT-1-RULING.md was not written"
requirements-completed: [EXP-01]
coverage:
  - id: SC2
    description: "66-RESULT.md reports, per run, tier, E beside the record's own E_const and band edges, the two-Kepler E, eps_h with the GAP-59-08 sentence, the input and h1 traces at the registered cadence, and the improvement check beside the E-only band and the final label; every value from diagnostic_phase66 output over the committed directories; loss context only"
    requirement: EXP-01
    verification:
      - kind: cli
        ref: "RESULT-PAGE-OK confirmed phase67-as-planned (the plan's automated verify: seven headings, confirmation/route equal to a fresh review)"
        status: pass
    human_judgment: false
  - id: SC3
    description: "66-RESULT.md states each run's label (tier1 on all three), the confirmation (confirmed), the route (phase67-as-planned), the plain-language reading pre-registered for tier1, and the SCOPE-49 proposal the route implies (none; the owner still answers checkpoint 1)"
    requirement: EXP-01
    verification:
      - kind: cli
        ref: "RESULT-PAGE-OK (confirmation and route asserted against the review output); page section SCOPE-49 proposal"
        status: pass
    human_judgment: false
  - id: VERD01
    description: "Every number cites a committed record by path and SHA-256 (all 22 evidence-index digests re-checked equal to shasum -a 256), and the page lists the machine hours used on this Mac for the timing run and the three runs (5,750 s = 1.5972222 h, about 1.60)"
    requirement: EXP-01
    verification:
      - kind: cli
        ref: "scripted digest cross-check of the evidence index against shasum -a 256 (22 files, no missing, all agree)"
        status: pass
    human_judgment: false
  - id: CP1
    description: "Owner checkpoint 1 (D-01, D-12) is one blocking-human decision presented only after 66-RESULT.md was committed; it is never auto-selected. The plan is HALTED awaiting the owner's answer; 66-CHECKPOINT-1-RULING.md is not written and no ruling content was invented"
    requirement: EXP-01
    verification:
      - kind: judgment
        ref: "structured checkpoint returned to the orchestrator with the committed page's branch, reading, proposal, options and the awaited owner answer; task 66-05-03 outstanding for the continuation agent"
        status: pass
    human_judgment: true
duration: 20min
completed: 2026-11-01
---

# Phase 66: Small-Network Control — Plan 05 Summary

**The three committed EXP-01 runs were read mechanically against the pre-registered rule: all three landed tier1 (E 0.0114 / 0.0172 / 0.0790, each settled), the branch is confirmed and the pre-registered route is phase67-as-planned (no plan change proposed); the result page is committed and owner checkpoint ① is posed — this plan is HALTED at that blocking-human checkpoint with the ruling (task 66-05-03) outstanding.**

## Performance
- **Duration:** about 20 minutes (20:05Z–20:25Z)
- **Started:** 2026-11-01T20:05Z (PLAN_START_SHA `2b5d0df73dd9ae3f22d3ee4e1712979d1d67deec`)
- **Tasks:** 1 of 3 complete (66-05-01); 66-05-02 presented as the blocking checkpoint; 66-05-03 outstanding
- **Files modified:** 1 created (66-RESULT.md); this SUMMARY and the hand-maintained STATE.md update are the docs commits

## Accomplishments
- Task 66-05-01: ran the review once over the three committed run directories
  (`read-run` per directory, one `review`, and `check-run` on the timing
  directory for provenance only — its score stays unread). All three runs read
  **tier1** with empty mechanical and setting problem lists:
  - main 1632/seed 42: E 0.011431234453278821 (Tier 1 line 0.1; record's own
    E_const 1.1538408194255343, two-Kepler 0.9168487091299374), output
    movement 0.9999971356891447, still_improving false;
  - repeat-system 851/seed 42: E 0.01720558902801923 (E_const
    1.233696866477104, two-Kepler 0.4312597209593449), output movement
    1.000002590770897, still_improving false;
  - repeat-seed 1632/seed 41: E 0.07898485527313073 (E_const
    1.1538408194255343, two-Kepler 0.9168487091299374), output movement
    0.9994221674071753, still_improving false.
- The review printed `EXP01-REVIEW confirmation=confirmed route=phase67-as-planned` —
  confirmation requires all three runs to share tier1 or near, and all three
  share tier1. The pre-registered reading for tier1: a network one-fifth the
  size, with one hidden layer, fits the orbit, so size is not what stopped
  v2.4; the data and scoring path can produce a passing fit.
- `66-RESULT.md` written plain-language-first with the seven required
  sections, every number cited to a committed record by path and SHA-256, the
  GAP-59-08 sentence verbatim, the identifiability limits ("what this result
  does not say"), harness provenance (historical smoke registration, reuse
  conditions, the seven frozen digests, budget, record sizes, machine hours
  5,750 s = 1.5972222 h ≈ 1.60), and the evidence index (both pages, four
  registrations, 16 record/weights/attempt/receipt files). The plan's
  automated check printed `RESULT-PAGE-OK confirmed phase67-as-planned`.
- The SCOPE-49 proposal for this route is **none**: Phase 67 runs as planned
  once the owner answers checkpoint ①; Phases 67–69 stay provisional until
  this review (SCOPE-49), and Phase 68 does not depend on the experiments
  (D-12).

## Task Commits
1. **Task 66-05-01: derive the branch mechanically and commit the plain-language result page** - `89045a7f` (docs) — `.planning/phases/66-small-network-control/66-RESULT.md` only; RESULT-PAGE-OK.
2. **Task 66-05-02: owner checkpoint ① (blocking-human)** - presented, no commit; the owner answers in chat. **Awaiting the owner's answer.**
3. **Task 66-05-03: write and commit the checkpoint ① ruling** - **outstanding**; the continuation agent writes `66-CHECKPOINT-1-RULING.md` from the owner's verbatim words (owner-quote block, CP1-EXP01 row, the SHA-256 of the committed 66-RESULT.md) and passes RULING-OK.
4. Docs commits: this SUMMARY (status: halted) and a separate hand-maintained STATE.md update (the gsd-tools mutating verbs stay off this checkout, per the 66-03/66-04 precedent). ROADMAP.md is deliberately untouched: the plan's verification requires ROADMAP.md, REQUIREMENTS.md, `pinn/` and `tests/` unchanged between PLAN_START_SHA and HEAD, and any accepted SCOPE-49 change is applied by the orchestrator's separate command after the phase.

## Files Created/Modified
- `.planning/phases/66-small-network-control/66-RESULT.md` - the EXP-01 result page presented to the owner (new; commit `89045a7f`)

## Decisions Made
- None - followed the plan as specified. The branch derivation was mechanical
  (review tool output only); no number was re-derived by hand. The only
  computed figures are the plan-mandated ones (band edges as 0.95/1.05 x the
  record's own E_const, the loss quarter change, wall times from the attempt
  timestamps, machine hours), each scripted and cited. No ruling content was
  invented; `66-CHECKPOINT-1-RULING.md` was not written.

## Deviations from Plan
- None - plan executed exactly as written through the checkpoint. No retry
  directory replaced any role (66-04 recorded none), so the review received
  the first-launch directories as registered.

## Issues Encountered
- None. All three read-run outputs were clean (`EXP01-RUN-OK`, exit 0, empty
  problem lists), the review exited 0, and the timing check-run printed
  `EXP01-CHECK-OK` without showing any score.

## Checkpoint state (owner checkpoint ①, blocking-human)
- **What the owner is asked (D-01, D-12, SCOPE-49):** having seen the EXP-01
  result, accept the proposal recorded on 66-RESULT.md (here: proceed — no
  plan change; Phase 67 runs as planned), direct a different plan change (an
  inserted phase, a dropped phase, re-aimed later phases, a new requirement,
  or proceeding unchanged, in the owner's own words), or hold.
- **Awaited:** the owner's answer in their own words. A question, a compute
  go-ahead, or a restatement of the D-08 budget answer is not a checkpoint ①
  answer; an item the reply does not address is recorded as not answered.
- **Next step:** a continuation agent records `66-CHECKPOINT-1-RULING.md`
  (status ratified, one owner-quote block, the CP1-EXP01 row, the SHA-256 of
  the committed 66-RESULT.md — `shasum -a 256` at ruling time), passes
  RULING-OK, and re-summarizes this plan as `status: complete`. The
  orchestrator handles any SCOPE-49 follow-up command and the hand-maintained
  STATE.md entry after the ruling.
- **Boundary:** this plan edits no roadmap, requirement, spec or registration;
  the held-out evaluation is unspent; nothing graded ran.

## Next Phase Readiness
- The result page the owner reviews is
  `.planning/phases/66-small-network-control/66-RESULT.md` (commit `89045a7f`;
  its SHA-256 is computed from the committed bytes at ruling time and cited by
  the ruling).
- If the owner accepts the recorded proposal, Phase 67 (the ladders) is set up
  as planned — the branch refutes "too small" for one orbit, so EXP-02..05 run
  as planned to find which part of the locked design fails.
- The held-out evaluation remains unspent; nothing beyond the three runs'
  Stage-0 TRAIN-only access was opened.

## Self-Check: PASSED

`66-RESULT.md` exists on disk and is committed at `89045a7f` (366 insertions,
that path only); RESULT-PAGE-OK re-printed against a fresh review; all 22
evidence-index digests equal `shasum -a 256` of the committed files;
`66-CHECKPOINT-1-RULING.md` correctly does not exist (the ruling awaits the
owner). The working tree after the plan's commits shows only the pre-existing
user-owned changes (`.planning/config.json`, the milestone_v2.2 brief, and the
untracked `.agents/`, `.gsd/`, `.planning/agent-history.json`,
`.planning/milestone.lock`, `.planning/state.json`, `.planning/tmp/`,
cross_cutting docs, `phase-40-plan-04-grok.md`), identical to the start
status.

---
*Phase: 66-small-network-control*
*Completed: 2026-11-01 (halted at owner checkpoint ①; the continuation agent closes the plan)*
