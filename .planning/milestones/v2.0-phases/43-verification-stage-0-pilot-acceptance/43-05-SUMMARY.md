---
phase: 43-verification-stage-0-pilot-acceptance
plan: 05
subsystem: verification-acceptance
tags: [acc-04, summary, honesty, evaluation-refresh, persisted-artifacts]
status: complete
requires:
  - phase: 43-02
    provides: "one-time held-out evaluator, committed metrics.json, and evaluation receipt"
  - phase: 43-04
    provides: "production pinn.train composition root used by terminal summary finalization"
provides:
  - "single-source completed-run summary payload with validation, curriculum, test-preview, comparison, and honesty sections"
  - "persisted validation.jsonl observations and terminal train wiring"
  - "post-receipt evaluation refresh for finished runs only"
affects: [43-06, 43-07, 43-08, milestone-acceptance]
tech-stack:
  added: []
  patterns:
    - "operator-facing claims are projections of persisted artifacts, never recomputed substitutes"
    - "non-success summaries return after the run header with null metric payloads"
key-files:
  created:
    - tests/phase43/test_summary_enrichment.py
    - tests/phase43/test_summary_honesty.py
  modified:
    - pinn/training/summary.py
    - pinn/train.py
    - pinn/evaluate.py
key-decisions:
  - "Validation trend is recorded contemporaneously in validation.jsonl; the renderer selects the last persisted record and never derives a replacement trend."
  - "Evaluation refresh occurs only after metrics and the one-time receipt are committed, and is a no-op unless the existing summary disposition is finished."
  - "Missing or malformed persisted inputs render as unavailable; failed/interrupted summaries do not parse or render metric-bearing sections."
patterns-established:
  - "Completed-run refresh preserves the existing terminal header/final losses and adds only committed evaluation evidence."
requirements-completed: [ACC-04]
coverage:
  - id: D1
    description: "Finished summaries render the required sections in fixed order from one JSON/Markdown payload, including all three honesty statements."
    requirement: ACC-04
    verification:
      - kind: unit
        ref: "tests/phase43/test_summary_enrichment.py#SummaryEnrichmentTests.test_finished_summary_uses_one_payload_and_fixed_section_order"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_summary_honesty.py#SummaryHonestyTests.test_finished_summary_states_all_three_honesty_rules"
        status: pass
    human_judgment: false
  - id: D2
    description: "The real evaluator refreshes an actual completed-run summary from committed metrics after creating its receipt."
    requirement: ACC-04
    verification:
      - kind: integration
        ref: "tests/phase43/test_summary_enrichment.py#SummaryEnrichmentTests.test_actual_evaluate_flow_refreshes_the_completed_run_summary_once"
        status: pass
    human_judgment: false
  - id: D3
    description: "Failed and interrupted summaries retain null metrics and cannot gain a test preview through refresh."
    requirement: ACC-04
    verification:
      - kind: unit
        ref: "tests/phase43/test_summary_honesty.py#SummaryHonestyTests.test_failed_and_interrupted_summaries_are_null_only_and_skip_metric_sections"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_summary_enrichment.py#SummaryEnrichmentTests.test_refresh_does_not_overwrite_a_non_success_summary"
        status: pass
    human_judgment: false
duration: 9min
completed: 2026-07-21
status: complete
---

# Phase 43 Plan 05: Completed-Run Summary Enrichment Summary

**Completed-run summaries now project persisted validation, curriculum, held-out metrics, and prior-run evidence into one honest payload, with evaluation refreshing only an existing finished run after its one-time receipt is committed.**

## Performance

- **Duration:** 9 min
- **Started:** 2026-07-22T02:25:17Z
- **Completed:** 2026-07-22T02:34:19Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments

- Extended `summary.json`/`summary.md` with fixed-order Validation summary, Test-set preview, Comparison hint, and Honesty notes sections while preserving the existing header, losses, and recorded curriculum.
- Wired `pinn.train` to persist validation observations and pass the validation/curriculum artifact paths to terminal finalization.
- Added `refresh_completed_summary` and invoked it from `pinn.evaluate` only after metrics and receipt commits; absent, malformed, failed, and interrupted summaries remain unmodified.
- Added seven Plan 43-05 tests, including a real evaluator flow over an actual completed-run fixture.

## Task Commits

1. **Task 1 RED: define summary payload and honesty behavior** — `706b0225` (test)
2. **Task 1 GREEN: implement persisted-artifact summary rendering** — `486c17b3` (feat)
3. **Task 2 RED: define production train/evaluator refresh behavior** — `318fed3c` (test)
4. **Task 2 GREEN: wire validation persistence and post-evaluation refresh** — `6a6f879e` (feat)

No refactor commit was needed; the GREEN implementations were already minimal and the focused/regression suites passed unchanged.

## Files Created/Modified

- `pinn/training/summary.py` — persisted-artifact readers, enriched single payload/renderer, non-success early return, and finished-run refresh.
- `pinn/train.py` — validation observation persistence plus terminal validation artifact wiring.
- `pinn/evaluate.py` — post-metrics/post-receipt completed-run summary refresh.
- `tests/phase43/test_summary_enrichment.py` — payload parity, section order, unavailable inputs, production caller, real evaluator refresh, and non-success refresh coverage.
- `tests/phase43/test_summary_honesty.py` — fixed honesty statements and failed/interrupted null-only backstops.

## Decisions Made

- Persist validation trend at the time each validation observation is recorded. Summary rendering reads the last valid JSONL record in order and never infers a trend from training data.
- Treat missing or malformed optional persisted artifacts as unavailable operator evidence, not as a reason to calculate a substitute or fabricate a value.
- Preserve failed/interrupted summaries byte-for-byte during evaluation refresh; only a pre-existing `disposition: finished` summary with readable committed metrics is eligible.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Added the assumed persisted validation artifact producer**

- **Found during:** Task 2 (terminal train wiring)
- **Issue:** The plan required the production caller to pass the run's persisted validation artifact, but no validation-history artifact existed; `_last_val_total` was runtime-only.
- **Fix:** Added append-only `validation.jsonl` observations at validation cadence, including step, final validation loss, and the contemporaneous trend consumed by the summary renderer.
- **Files modified:** `pinn/train.py`
- **Verification:** `test_terminal_train_caller_passes_persisted_validation_and_curriculum` plus the completed-run evaluator integration test pass.
- **Committed in:** `6a6f879e`

---

**Total deviations:** 1 auto-fixed (1 missing critical functionality).
**Impact on plan:** The addition supplies the persisted input the plan assumed and is required for an honest production Validation summary; no model, loss, data-selection, or evaluation behavior changed.

## Issues Encountered

- An optional Phase 42 redaction regression check remains blocked by the already-documented Phase 43-04 fail-closed duration gate: its synthetic fresh launch lacks the required persisted timing calibration. This is pre-existing, recorded as DI-43-04-02, and outside Plan 43-05 ownership. The exact Plan 43-05 suite and the prior evaluator suites pass.
- A closeout shell loop temporarily used zsh's special `path` variable, which removed commands from that one subprocess's lookup path; the stub scan and `git diff --check` were immediately rerun in a clean shell and passed. No files were affected.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- ACC-04 is production-wired and ready for the later smoke/pilot/verdict plans to consume.
- Plans 43-06 through 43-08 remain pending; this plan does not mark Phase 43 or milestone v2.0 complete.

## Known Stubs

None. The word `placeholder` appears only in existing honesty documentation that prohibits placeholder metrics; unavailable persisted inputs are explicitly represented as unavailable evidence.

## Self-Check: PASSED

- All five owned implementation/test files and this SUMMARY exist on disk.
- TDD commit order is present: `706b0225` → `486c17b3` → `318fed3c` → `6a6f879e`.
- `python -m unittest tests.phase43.test_summary_enrichment tests.phase43.test_summary_honesty -v` — 7/7 pass.
- `python -m unittest tests.phase43.test_evaluate_gate tests.phase43.test_evaluate_edge_cases tests.phase43.test_summary_enrichment tests.phase43.test_summary_honesty -v` — 24/24 pass.
- `python -m py_compile` over all five owned implementation/test files — pass.
- `git diff --check` — pass.

---
*Phase: 43-verification-stage-0-pilot-acceptance*
*Completed: 2026-07-21*
