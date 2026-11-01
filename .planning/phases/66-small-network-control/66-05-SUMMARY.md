---
phase: 66-small-network-control
plan: "05"
status: complete
requires:
  - phase: 66-small-network-control (plan 04)
    provides: "the three verified EXP-01 run records under evidence/exp01/ (main-1632-s42, repeat-851-s42, repeat-1632-s41), each 465,000 steps, check-run-clean, committed at a546016b / 3dc3646a / 277c25ce, with no score read in 66-04"
provides:
  - "66-RESULT.md (89045a7f): the EXP-01 branch derived mechanically by diagnostic_phase66 review over the three committed run directories — all three runs tier1, confirmation confirmed, route phase67-as-planned — in plain language with every number cited to a committed record by path and SHA-256, the frozen reading, the SCOPE-49 proposal (none), the identifiability limits, harness provenance and the evidence index; RESULT-PAGE-OK"
  - "66-CHECKPOINT-1-RULING.md (e40ebca2): the owner's checkpoint 1 answer recorded verbatim (accept) beside the exact result page it answers by SHA-256, with the CP1-EXP01 row and the SCOPE-49 disposition (no plan change; Phase 67 runs as planned); RULING-OK"
affects: [phase-66-verification, phase-67]
actuals:
  tokens: 12000
  tasks: 3
  commits: 6
tech-stack:
  added: []
  patterns:
    - "mechanical branch derivation: every label, the confirmation, the route and every number copied from read-run/review/check-run output over the committed directories; the only computed figures are the plan-mandated band edges (0.95/1.05 x the record's own E_const), the loss quarter change, wall times and machine hours, each scripted and cited"
    - "owner ruling protocol: the checkpoint answer is held verbatim in one never-parsed owner-quote block, restated only as the chosen option in a Recorded answers row, and cited beside the reviewed page's SHA-256"
key-files:
  created:
    - .planning/phases/66-small-network-control/66-RESULT.md
    - .planning/phases/66-small-network-control/66-CHECKPOINT-1-RULING.md
  modified: []
key-decisions:
  - "Task 66-05-01: none - followed the plan as specified: the branch was derived mechanically from the review tool output only (all three runs tier1, confirmed, phase67-as-planned, which proposes no plan change); the owner checkpoint was not pre-answered and 66-CHECKPOINT-1-RULING.md was not written"
  - "Tasks 66-05-02/03: the owner's checkpoint 1 answer was recorded verbatim (accept) with no interpretation, and the accepted proposal proposes no plan change, so this plan edited no roadmap, requirement, spec or registration; ROADMAP.md, REQUIREMENTS.md, pinn/ and tests/ are unchanged from PLAN_START_SHA 2b5d0df7 (the plan's acceptance diff is empty)"
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
    description: "Owner checkpoint 1 (D-01, D-12) was one blocking-human decision presented only after 66-RESULT.md was committed and never auto-selected; the owner answered 2026-11-01 (America/Chicago) — verbatim: accept the recorded proposal — and the answer is recorded verbatim in 66-CHECKPOINT-1-RULING.md (one owner-quote block, the CP1-EXP01 row, the reviewed page's SHA-256 and the three record digests)"
    requirement: EXP-01
    verification:
      - kind: cli
        ref: "RULING-OK (the plan's automated verify: status ratified, the four sections, exactly one non-empty owner-quote block, the cited result digest, the CP1-EXP01 accept row)"
        status: pass
      - kind: cli
        ref: "acceptance diff: git diff --stat 2b5d0df7..HEAD -- .planning/ROADMAP.md .planning/REQUIREMENTS.md pinn tests prints nothing; git diff --check over the range clean"
        status: pass
    human_judgment: true
duration: about 35 min across two sessions (execution 20:05Z-20:25Z; continuation after the owner's answer 20:31Z-20:45Z)
completed: 2026-11-01
---

# Phase 66: Small-Network Control — Plan 05 Summary

**The three committed EXP-01 runs were read mechanically against the pre-registered rule — all three landed tier1 (E 0.0114 / 0.0172 / 0.0790, each settled), the branch is confirmed and the pre-registered route is phase67-as-planned — the result page was committed, the owner answered checkpoint ① with accept (no plan change; Phase 67 runs as planned), and the answer is recorded verbatim in the ruling page beside the exact result page it answers.**

## Performance
- **Duration:** about 35 minutes across two sessions (task 66-05-01 20:05Z–20:25Z; the continuation after the owner's answer 20:31Z–20:45Z)
- **Started:** 2026-11-01T20:05Z (PLAN_START_SHA `2b5d0df73dd9ae3f22d3ee4e1712979d1d67deec`)
- **Tasks:** 3 of 3 complete (66-05-01; 66-05-02 checkpoint presented and answered; 66-05-03 ruling committed)
- **Files modified:** 2 created (66-RESULT.md, 66-CHECKPOINT-1-RULING.md); this SUMMARY and the hand-maintained STATE.md update are the docs commits

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
- Task 66-05-02: the checkpoint was presented after the result page was
  committed (plain-language reading, branch table, proposal and what it
  blocks, machine hours, that nothing graded ran and the held-out evaluation
  is unspent, the page path), with the three options accept / change / hold.
  The owner answered the same day, 2026-11-01 (America/Chicago), verbatim:
  **"Accept the recorded proposal"**.
- Task 66-05-03: `66-CHECKPOINT-1-RULING.md` written in the plan's format
  (frontmatter `status: ratified`, "Authority and boundary", one never-parsed
  `owner-quote` block with the owner's message verbatim, the Recorded answers
  row `CP1-EXP01 | accept`, and "The result reviewed" citing the committed
  page's SHA-256 `bf143995…8d26a9` at `89045a7f` plus the three record
  digests, re-verified with `shasum -a 256`). The plan's automated check
  printed `RULING-OK`.

## Task Commits
1. **Task 66-05-01: derive the branch mechanically and commit the plain-language result page** - `89045a7f` (docs) — `.planning/phases/66-small-network-control/66-RESULT.md` only; RESULT-PAGE-OK.
2. **Task 66-05-02: owner checkpoint ① (blocking-human)** - presented and answered in chat; no commit by design (the answer is recorded by task 66-05-03). **Answered: "Accept the recorded proposal" (2026-11-01, America/Chicago).**
3. **Task 66-05-03: write and commit the checkpoint ① ruling** - `e40ebca2` (evidence) — `.planning/phases/66-small-network-control/66-CHECKPOINT-1-RULING.md` only; RULING-OK; recorded answer CP1-EXP01: accept.
4. Docs commits: this SUMMARY (status: complete) and a separate hand-maintained STATE.md update (the gsd-tools mutating verbs stay off this checkout, per the 66-03/66-04 precedent). ROADMAP.md is deliberately untouched: the plan's verification requires ROADMAP.md, REQUIREMENTS.md, `pinn/` and `tests/` unchanged between PLAN_START_SHA and HEAD (the acceptance diff is empty), and the accepted proposal itself proposes no roadmap change — Phase 67 runs as planned, with any follow-up bookkeeping applied by the orchestrator's separate command after the phase.

## Files Created/Modified
- `.planning/phases/66-small-network-control/66-RESULT.md` - the EXP-01 result page presented to the owner (new; commit `89045a7f`)
- `.planning/phases/66-small-network-control/66-CHECKPOINT-1-RULING.md` - the owner's checkpoint ① answer, verbatim, ratified (new; commit `e40ebca2`)

## Decisions Made
- Task 66-05-01: none - followed the plan as specified. The branch derivation
  was mechanical (review tool output only); no number was re-derived by hand.
  The only computed figures are the plan-mandated ones (band edges as
  0.95/1.05 x the record's own E_const, the loss quarter change, wall times
  from the attempt timestamps, machine hours), each scripted and cited.
- Tasks 66-05-02/03: the owner's words were held verbatim and never parsed;
  the table restates only the chosen option (accept). No ruling content was
  invented, and nothing was applied on the answer's strength inside this
  plan — the accepted proposal is the recorded one for route
  `phase67-as-planned`: no plan change; Phase 67 runs as planned.

## Deviations from Plan
- None - plan executed exactly as written. No retry directory replaced any
  role (66-04 recorded none), so the review received the first-launch
  directories as registered; the checkpoint was presented and answered per
  the plan; the ruling follows the plan's format and commit protocol.

## Issues Encountered
- None. All three read-run outputs were clean (`EXP01-RUN-OK`, exit 0, empty
  problem lists), the review exited 0, the timing check-run printed
  `EXP01-CHECK-OK` without showing any score, and both page checks
  (RESULT-PAGE-OK, RULING-OK) passed.

## Checkpoint resolution (owner checkpoint ①)
- **Asked (2026-11-01, America/Chicago, after `66-RESULT.md` was committed):**
  "having seen the EXP-01 result (confirmed Tier 1, route
  phase67-as-planned), do you accept the recorded proposal, direct a
  different plan change, or hold?"
- **Owner's answer, verbatim:** "Accept the recorded proposal".
- **Recorded answer:** CP1-EXP01 — accept — applied by the separate step named
  in the ruling (here: no plan change to apply; Phase 67 runs as planned).
  The owner's message made no further request, so the ruling's table has one
  row and nothing is listed as not acted on in Phase 66.
- **Boundary held:** the plan edited no roadmap, requirement, spec or
  registration; ROADMAP.md, REQUIREMENTS.md, `pinn/` and `tests/` are
  unchanged from PLAN_START_SHA `2b5d0df7`; the held-out evaluation is
  unspent and nothing graded ran.

## Next Phase Readiness
- The owner accepted the recorded proposal, and it proposes no plan change:
  Phase 67 (the ladders, EXP-02..05) runs as planned. Setting it up is the
  orchestrator's separate step after this phase — this plan writes no
  roadmap.
- The SCOPE-49 review after EXP-01 is done and accepted; Phases 67–69 are no
  longer blocked on this phase's review. Phase 68 (the yardstick) never
  depended on the experiments (D-12).
- The EXP-01 requirement mark follows the phase verification act, as in
  Phase 65; the held-out evaluation remains unspent, machine time stands at
  5,750 s ≈ 1.60 h, and the harness freeze at `734cb7da` held throughout.

## Self-Check: PASSED

`66-RESULT.md` exists on disk and is committed at `89045a7f` (366 insertions,
that path only), unchanged since (working-tree `shasum -a 256`
`bf143995410ae48a57845b5cf7f5500dc059c4fd0af96486a1b43801b88d26a9`).
`66-CHECKPOINT-1-RULING.md` exists on disk and is committed at `e40ebca2`
(69 insertions, that path only); RESULT-PAGE-OK and RULING-OK both printed;
the three record digests cited by the ruling equal `shasum -a 256` of the
committed files; `git diff --stat 2b5d0df7..HEAD -- .planning/ROADMAP.md
.planning/REQUIREMENTS.md pinn tests` prints nothing and `git diff --check`
over the range is clean. The working tree after the plan's commits shows only
the pre-existing user-owned changes (`.planning/config.json`, the
milestone_v2.2 brief, and the untracked `.agents/`, `.gsd/`,
`.planning/agent-history.json`, `.planning/milestone.lock`,
`.planning/state.json`, `.planning/tmp/`, cross_cutting docs,
`phase-40-plan-04-grok.md`), identical to the start status.

---
*Phase: 66-small-network-control*
*Completed: 2026-11-01*
