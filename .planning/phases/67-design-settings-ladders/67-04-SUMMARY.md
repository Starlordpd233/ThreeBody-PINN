---
phase: 67-design-settings-ladders
plan: "04"
subsystem: testing
tags: [pytorch, unittest, diagnostic-harness, tdd, checkpoint-schedule, timing, cost-only-budget, equal-updates]

requires:
  - phase: 67-design-settings-ladders (67-01)
    provides: the phase67 registry dispatch, the admission-door extension seam and the tests/phase67 synthetic fixtures
  - phase: 67-design-settings-ladders (67-02)
    provides: PHASE67_ARMS and the declared ladders the budget's expected identities enumerate
  - phase: 66-small-network-control
    provides: the bounded fit loop, the synchronized timing basis and the exp01_budget projection precedent this plan generalizes
provides:
  - phase67_cadence / phase67_score_cadence / phase67_loss_trace_stride and PHASE67_BUDGET_RULE — the registered five-event similarity schedule, three-event frozen-score schedule and the bounded loss trace at the 100-step quantum
  - The fit's timed science checkpoints — score_checkpoints with step, frozen score and elapsed seconds, the disjoint per-event logging/scoring/publication-I/O timing ledger, endpoint-score reuse without a fourth scoring call, and event-boundary deadline checks
  - The score_cadence admission gate (exact schedule validated before any data or model; phase67-only)
  - phase67_budget — the cost-only common-update budget over every declared timing row, with per-row/per-experiment projections, timing-evidence digests and the phase cost ledger (measured projections vs cap-based reservations)
affects: [67-05 (window registration/reader rules), 67-06 compatibility work, 67-07 prediction/registration pages, 67-08..67-15 (timing and science execution), Phase 68 energy adjudication]

actuals:
  tokens: 22862
  tasks: 2
  commits: 4

tech-stack:
  added: []
  patterns:
    - "Registered-schedule timing: the same normalized event grid (five similarity, three frozen-score) serves timing and science, so every projected cost is a measured cost of an event the science run actually performs"
    - "Per-event disjoint timing ledger: each logger/scorer/publication event is its own synchronized completed-work segment on the shared monotonic basis, provably disjoint from the synchronized optimizer durations by a segment-sum bound inside the loop wall"
    - "Cost-only budgets: identities plus measured durations and bytes decide N; scientific values are never read, never echoed, and an unmeasured experiment gets an explicitly labelled cap reservation, never a borrowed historical rate"

key-files:
  created:
    - pinn/verification/diagnostic_phase67.py
    - tests/phase67/test_checkpoints.py
    - tests/phase67/test_budget.py
  modified:
    - pinn/verification/diagnostic_fit.py

key-decisions:
  - "score_cadence is optional in settings: a phase67 registration without it keeps 67-01's tracer contract byte-for-byte, while one with it must pin the exact schedule (score cadence, normalized similarity cadence and bounded stride) before any data access; a non-phase67 registry declaring it refuses."
  - "The checkpoint's elapsed_seconds is the elapsed whole-run clock at checkpoint completion; the per-call durations live in timing.events.scoring (and logging/publication_io), so the record carries both when-in-run evidence and the disjoint cost ledger."
  - "The after-event deadline checks and the comparisons_seconds phase exist only on the schedule path; the historical path's checks, fields and behavior are unchanged (phase65 discovery 204 OK proves it)."
  - "phase67_budget takes an optional unmeasured run-count map so the phase ledger can carry explicitly labelled cap-based upper reservations for experiments without timing rows yet — the minimal mechanism the plan's ledger requirement implies; the default ledger covers the measured experiments only."
  - "Projection exactness is tested with dyadic-rational rows so the target equality (2655.0 s at N=17100) is exact floating-point arithmetic, proving <= semantics admit equality and the next 100-step candidate necessarily exceeds the target."

patterns-established:
  - "Schedule-first registration: timing and science registrations declare one schedule through the pure module functions, and admission re-derives it rather than trusting the document"
  - "Residual-plus-readdition projections: F retains every unitemized launch cost while the itemized costs are re-added at their measured maxima scaled to the candidate N — nothing measured is dropped and nothing scientific is read"

requirements-completed: []  # EXP-02..05 are declared here but the experiments run in 67-08..67-15; the marks flip at the phase verification act, per the 67-01/02/03 convention (shared-ID gate: siblings also declare them).

coverage:
  - id: D1
    description: "The pure registered schedule and its admission gate: the five normalized similarity events and three frozen-score checkpoints at the 100-step quantum, the bounded ceil(N/1000) loss trace with at most 1001 retained entries, the PHASE67_BUDGET_RULE numbers (science and timing scales), and admission validating the exact schedule (wrong score cadence, foreign similarity cadence, unbounded stride, non-phase67 registry, off-quantum step counts all refusing) before any data access"
    requirement: EXP-02
    verification:
      - kind: unit
        ref: "tests/phase67/test_checkpoints.py#CadenceTests.test_similarity_cadence_is_the_five_normalized_events"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_checkpoints.py#CadenceTests.test_loss_trace_stride_is_ceil_n_over_1000_with_at_most_1001_entries"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_checkpoints.py#ScoreCadenceAdmissionTests.test_the_registered_schedule_admits_before_any_data_access"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_checkpoints.py#ScoreCadenceAdmissionTests.test_score_cadence_on_a_non_phase67_registration_refuses"
        status: pass
    human_judgment: false
  - id: D2
    description: "The timed science checkpoints in the fit: exactly three scorer and five logger events at the right steps (spy-proven), individually synchronized and disjoint from the optimizer durations, checkpoints recorded with step/frozen score/elapsed seconds after the complete-finite guard, the endpoint score reused from the final checkpoint without a fourth call, event-boundary deadline expiry refusing with nothing published, clean registration-bound verification with tamper refusals, and the historical no-schedule path unchanged"
    requirement: EXP-02
    verification:
      - kind: integration
        ref: "tests/phase67/test_checkpoints.py#RegisteredScheduleRunTests.test_exactly_five_logger_and_three_scorer_events_fire"
        status: pass
      - kind: integration
        ref: "tests/phase67/test_checkpoints.py#RegisteredScheduleRunTests.test_event_costs_are_disjoint_from_the_optimizer_durations"
        status: pass
      - kind: integration
        ref: "tests/phase67/test_checkpoints.py#RegisteredScheduleRunTests.test_the_final_checkpoint_supplies_the_endpoint_score"
        status: pass
      - kind: integration
        ref: "tests/phase67/test_checkpoints.py#ScheduleDeadlineTests.test_a_deadline_expiry_at_a_checkpoint_refuses_and_publishes_nothing"
        status: pass
      - kind: integration
        ref: "tests/phase67/test_checkpoints.py#HistoricalPathControls.test_the_run_completes_with_the_historical_shape"
        status: pass
    human_judgment: false
  - id: D3
    description: "The cost-only common update budget from every registered timing row: largest common multiple-of-100 N at or above 300 within 0.75*3540 s for every row (exact target equality admitted, next quantum beyond), slow repeats constraining N, permutation and changed-scientific-score invariance, the 5*max logger and 3*max scorer and byte-scaled publication terms, the 1e-9 s residual tolerance, the unsafe-size refusal, the explicit no-admissible-N resource refusal, malformed/missing/duplicate/non-finite/boolean row refusals (seed 41 included), the ten cost-only output fields and the ledger separating measured projections from cap-based reservations"
    requirement: EXP-03
    verification:
      - kind: unit
        ref: "tests/phase67/test_budget.py#CommonBudgetTests.test_the_budget_picks_the_largest_common_n_for_every_row"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_budget.py#CommonBudgetTests.test_target_equality_is_admitted_and_the_next_quantum_exceeds_it"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_budget.py#CommonBudgetTests.test_row_permutation_and_changed_scientific_scores_change_nothing"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_budget.py#BudgetValidationTests.test_a_missing_declared_row_refuses_including_seed41"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_budget.py#BudgetOutputTests.test_the_ledger_separates_measured_projections_from_cap_reservations"
        status: pass
    human_judgment: false

duration: 26 min
completed: 2026-11-02
status: complete
---

# Phase 67 Plan 04: Design & Settings Ladders — Checkpoint Schedule & Common Budget Summary

**The registered science checkpoint schedule (five normalized similarity events, three frozen-score checkpoints at N/2, 3N/4, N) is timed event-by-event inside the fit with the endpoint score reused, and a cost-only common-update budget derives the largest fair N for every declared timing row within 75% of the 3,540-second cap — no score, loss or cosine value anywhere in a projection or output.**

## Performance

- **Duration:** 26 min (19:20–19:46 UTC, 2026-11-02)
- **Started:** 2026-11-02T19:20:19Z
- **Completed:** 2026-11-02T19:46:11Z
- **Tasks:** 2 of 2
- **Files modified:** 4 (1 new pure module, 1 harness edit, 2 new test modules)

## Accomplishments

- `pinn/verification/diagnostic_phase67.py` (new, stdlib-only, no harness imports) owns the registered schedule as pure functions — `phase67_cadence` (0, N/4, N/2, 3N/4, N at multiples of the 100-step quantum), `phase67_score_cadence` (N/2, 3N/4, N riding the cadence grid), `phase67_loss_trace_stride` (ceil(N/1000), at most 1001 retained entries with the final loss kept) — and `PHASE67_BUDGET_RULE` pinning the science numbers (cap 3540 s, 0.75 fraction, 0.25 rate margin, warmup 200, quantum 100, floor 300) and the registered timing run (1200/200/1000 under a 900 s cap).
- The fit harness now runs the registered schedule when a phase67 registration declares `score_cadence`: the three frozen `score_network` calls and five logger calls are timed individually as synchronized completed-work segments (same monotonic basis, disjoint from the optimizer durations — proven by the segment-sum bound inside the loop wall), deadline-checked before and after each event and after publication before the exclusive write, recorded into `score_checkpoints` (step, frozen score, elapsed seconds) only after the complete-finite-score guard, and the final checkpoint supplies `scores.network` with no fourth scoring call; `timing.events` keeps the disjoint logging/scoring/publication-I/O ledger.
- Admission validates the exact schedule before any data or model exists (score cadence, normalized similarity cadence and bounded stride all pinned to the module functions; non-phase67 registries cannot declare it), `run_registered_smoke` passes the admitted schedule through, and `verify_fit_result` checks it in both directions — missing, extra or tampered checkpoints, and un-declared event ledgers, all refuse.
- `phase67_budget(cost_rows, *, expected_identities, unmeasured=None)` derives the fair common update count from every declared timing row (main, repeat-system, seed-41 repeat — all required, unique, well-formed, finite, at the registered 1200/200/1000 scale with all actual checkpoint costs and the full-launch wall): the projection is the launch residual F (retaining comparison/data-load/power/admission/supervision costs) plus measured warmup, (N−200)·rate·1.25, five max logger-event seconds, three max scorer-event seconds and byte-scaled publication I/O; N is the largest multiple of 100 at or above 300 within 0.75·3540 s by integer exponential bracketing plus binary search (equality admitted, next quantum necessarily beyond, every value finite); unsafe predicted sizes refuse rather than shortening science; no admissible N is an explicit resource refusal.
- The budget output is cost-only (the ten required fields, per-row and per-experiment projections, timing-evidence digests) with a phase cost ledger that separates measured planned seconds from explicitly labelled cap-based upper reservations for unmeasured experiments — never a borrowed historical rate. Row permutation and changed scientific scores leave it byte-identical.

## Task Commits

1. **Task 67-04-01 RED: failing checkpoint schedule tests** - `534bd9e5` (test) — machine-verified `RED_EVIDENCE_OK` (23 tests, 18 failing on the planned behavior, 5 regression controls passing; target `test_similarity_cadence_is_the_five_normalized_events`).
2. **Task 67-04-01 GREEN: timed registered schedule** - `fafffa33` (feat) — the new pure module, the admission gate, the fit's per-event timing/checkpoint path, the verify checks and the run-through pass.
3. **Task 67-04-02 RED: failing budget tests** - `8665f3f2` (test) — machine-verified `RED_EVIDENCE_OK` (18 tests, 17 failing on the missing `phase67_budget`, the rule-numbers control passing).
4. **Task 67-04-02 GREEN: the common budget** - `b89e04d3` (feat) — `phase67_budget` with row validation, the F+events+bytes projection, the bracketing search and the cost-only ledger output.

**Plan metadata:** this SUMMARY's commit (docs).

## Files Created/Modified

- `pinn/verification/diagnostic_phase67.py` - the pure schedule functions, `phase67_loss_trace_entries` and `PHASE67_BUDGET_RULE` (task 1) plus the validated cost-row parser and `phase67_budget` with the projection, search, refusal surface and ledger output (task 2)
- `pinn/verification/diagnostic_fit.py` - the `score_cadence` admission gate in `validate_smoke_settings`; the schedule path in `fit_diagnostic` (per-event timing, checkpoints, deadline before/after events and publication, endpoint reuse, `timing.events`, `comparisons_seconds`); `_require_finite_checkpoint`; the `run_registered_smoke` pass-through; the two-directional schedule checks in `verify_fit_result`
- `tests/phase67/test_checkpoints.py` - CadenceTests, ScoreCadenceAdmissionTests, one 100-step registered end-to-end run with spies, the checkpoint-boundary deadline test and the historical controls (23 tests)
- `tests/phase67/test_budget.py` - BudgetRuleTests, CommonBudgetTests (incl. the exact-arithmetic target-equality row), BudgetValidationTests and BudgetOutputTests (18 tests)

## Decisions Made

- `score_cadence` stays optional so 67-01's tracer registration contract is preserved byte-for-byte; when present it pins the exact schedule (score cadence, similarity cadence, stride) at admission — the only schedule a phase67 registration may declare.
- The checkpoint's `elapsed_seconds` is the elapsed whole-run clock at completion (when-in-run evidence); the per-call costs live in `timing.events`, so the record carries both without duplication of meaning.
- The after-event deadline checks, `timing.events` and `comparisons_seconds` exist only on the schedule path — the historical path's fields, checks and behavior are unchanged (phase65 discovery 204 OK).
- `phase67_budget`'s optional `unmeasured` run-count map is the minimal mechanism the ledger requirement implies: unmeasured experiments get explicitly labelled cap-based upper reservations, and the default ledger covers the measured experiments only.
- Projection exactness is tested with dyadic-rational rows so target equality at N=17100 is exact floating-point arithmetic — `<=` semantics provably admit equality and reject the next quantum.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Two test-authoring defects corrected during GREEN**
- **Found during:** Tasks 67-04-01 and 67-04-02 GREEN
- **Issue:** (a) the admission test read `orbit_key.record_id`, but `RecordKey`'s field is `id`; (b) the unknown-identity refusal assertion expected the fragment "not declared" while the implemented refusal reads "is not a declared identity".
- **Fix:** corrected the test to `orbit_key.id` and to the implemented refusal fragment; no implementation change was needed for either.
- **Files modified:** tests/phase67/test_checkpoints.py, tests/phase67/test_budget.py
- **Verification:** the task verify commands moved from 1 error/1 failure to 25 tests OK and 18 tests OK respectively.
- **Committed in:** fafffa33, b89e04d3 (test-only portions of the GREEN commits)

---

**Total deviations:** 1 auto-fixed (bug — two test-authoring defects, corrected in the GREEN commits)
**Impact on plan:** No scope creep; both fixes were test-side corrections that tightened the RED tests' agreement with the implemented refusals.

## Issues Encountered

- phase66 discovery remains at its known D-12 live-pin transition state — 99 tests, 6 failures (the four `test_pages` live-digest tests plus the Phase 65 smoke pins on `diagnostic_variants.py`/`diagnostic_similarity.py`) — unchanged by this plan's `diagnostic_fit.py` edit and still routed to 67-06 per the 67-01 convention. phase65 discovery is 204 OK and phase67 discovery is 139 OK at final HEAD.

## Known Stubs

None - the schedule and budget are fully implemented and tested; the real timing calibration run that feeds measured rows into `phase67_budget` is the registered weekend execution work of the later plans (67-07 onward), exactly as this plan's verification states ("no real timing is performed here").

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Wave 3 is complete, unblocking Wave 4 (67-05, window registration/reader rules). 67-07's prediction/registration pages can embed `PHASE67_BUDGET_RULE` and the schedule functions directly, and the timing/science execution plans (67-08..67-15) register `score_cadence = phase67_score_cadence(N)` with `loss_trace_stride = phase67_loss_trace_stride(N)`, then hand the measured cost rows (from the records' `timing.events`, `phases` and byte counts) to `phase67_budget`.
- The `unmeasured` ledger map lets each experiment's page carry honest phase cost bounds before its timing rows exist, updated with measured projections before each science launch as the plan directs.
- No real timing, corpus read or training ran in this plan; the held-out evaluation remains unspent.

## Self-Check: PASSED

All 3 created files exist on disk; all 4 production commits (`534bd9e5`, `fafffa33`, `8665f3f2`, `b89e04d3`) exist in history with both TDD gate sequences ordered (test → feat per task); both task verify commands re-ran green at final HEAD (25 and 18 tests OK), the Phase 67 discovery is 139 tests OK, phase65 is 204 OK and phase66 shows only its six known D-12 transition failures; `git diff --check` is clean over the plan range `534bd9e5^..HEAD`.

---
*Phase: 67-design-settings-ladders*
*Completed: 2026-11-02*
