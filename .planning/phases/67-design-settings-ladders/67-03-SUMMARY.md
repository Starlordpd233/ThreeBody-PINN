---
phase: 67-design-settings-ladders
plan: "03"
subsystem: testing
tags: [pytorch, unittest, census, signed-laps, window-prefixes, diagnostic-harness, tdd, frozen-scoring, two-kepler]

requires:
  - phase: 66-small-network-control
    provides: the frozen _comparison_rows baselines, score_trajectory/two_kepler_prediction and the exact inclusive loader window this plan reuses
  - phase: 67-design-settings-ladders (67-01)
    provides: the tests/phase67 synthetic fixture conventions and the per-phase module/ownership protocol this plan follows
provides:
  - first_lap_prefixes — the D-06 exact sampled signed-lap prefixes (1/2/5/10 laps) with full crossing brackets, exact float64 endpoints, exact inclusive retention, locked global tau hashes and the census aliasing guard
  - same_window_expectations — independently checked same-window window-mean-constant and two-Kepler baselines with prefix grid cross-checks, explicit formula nonapplicability and the GAP-59-08 note
  - WindowPrefixRefused / WindowExpectationRefused — the typed refusals for later registration and reading plans
affects: [67-05 (window registration/reader rules), 67-08..67-15 (EXP-05 execution and reading), Phase 68 energy adjudication]

actuals:
  tokens: 15461
  tasks: 2
  commits: 5

tech-stack:
  added: []
  patterns:
    - "First-crossing prefixes from existing samples only: the endpoint is the exact float64 gold timestamp of the earliest sample whose cumulative signed census-normal turns reach the lap count; no interpolation, no rescaled tau, no census t_max tolerance (D-06)"
    - "Dual-measure unwrap guard against the single census limit pi: the observed principal arctan2 step plus the increment predicted by the local angular rate about the same normal, because a true step beyond pi wraps invisibly to the principal measure alone"
    - "Baseline evidence is cross-checked, not trusted: same-window comparisons agree between the harness rows and an independent recomputation through the same frozen functions, and the retained grid's hashes/endpoint/count must match the selected prefix, so no window can borrow another's constants"

key-files:
  created:
    - pinn/verification/diagnostic_phase67_windows.py
    - tests/phase67/test_windows.py
  modified: []

key-decisions:
  - "The census angular-step guard is applied as one limit (scorecard census_rules unwrap_max_step_rad, pi) over two measures: the census's observed principal step and the increment predicted by the local angular rate about the same initial normal (trapezoid over the recorded separation and its derivative). The principal measure alone can never reach pi — a true increment beyond pi wraps silently — so the predicted increment is what actually exposes an aliased grid at the census limit, which is exactly what D-06's 'reject a grid that cannot distinguish' demands."
  - "Same-window baseline agreement is a serialization/consistency check (rtol 1e-8, atol 1e-10) over the frozen score_trajectory/two_kepler functions — not a new science bar; a formula refusal stays an explicit not_applicable/solver failure with its reason on both paths and can never become a manufactured finite score (D-13, T-67-09)."
  - "The prefix cross-check (physical_times_sha256, normalized_tau_sha256, endpoint, sample count) is what prevents borrowed evidence: a window loaded on another lap's grid, a tampered interior timestamp, or the full-window [0,10] EXP-01 grid all refuse before any scoring (T-67-08)."
  - "rough_planning_duration L*T/N_in is emitted only when census_n_in is supplied, carries an approximate/never-the-endpoint note, and plays no role in selection (D-06)."
  - "TDD resume: the interrupted prior executor's task-1 RED commit (5ed595e4) was re-verified at resume — the failing state reproduced (20 tests / 18 failures on the missing module) and a fresh RED evidence record was machine-checked RED_EVIDENCE_OK — before any GREEN work began."

patterns-established:
  - "Prefix-then-verify pairing: first_lap_prefixes selects and hashes the grid, same_window_expectations re-derives the baselines on exactly that grid — later registration plans record both as one window intervention"
  - "Applicability-truthful baselines: nonapplicability is recorded on every path it appears on, with agreement meaning 'same refusal, same reason', never a substituted score"

requirements-completed: []  # EXP-05 is declared here but the experiment runs in 67-08..67-15; the mark flips at the phase verification act (shared-ID gate: siblings also declare it), matching the 67-01/67-02 convention.

coverage:
  - id: D1
    description: "The D-06 exact sampled signed-lap prefixes: earliest signed crossings on analytic uniform/variable-speed/reversing orbits, exact endpoint inclusion under nextafter both sides, crossing near the record end, full brackets with counts and hashes, locked global tau never rescaled, the census aliasing limit refusing and the just-under-limit grid admitted, distinguishability refusal, and every refusal class (duplicate/nonincreasing/nonfinite times, nonzero start, undefined normal, missing fields, fewer than two samples, unreached laps, bad lap inputs, bad census_n_in, endpoints beyond the loader window)"
    requirement: EXP-05
    verification:
      - kind: unit
        ref: "tests/phase67/test_windows.py#LapPrefixTests.test_a_uniform_circular_orbit_prefixes_end_at_the_earliest_signed_crossing"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_windows.py#LapPrefixTests.test_the_selected_endpoint_is_included_exactly_under_nextafter"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_windows.py#LapPrefixTests.test_signed_reversals_do_not_count_as_extra_turns"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_windows.py#LapPrefixTests.test_angular_aliasing_refuses_through_the_census_limit"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_windows.py#LapPrefixTests.test_a_grid_that_cannot_distinguish_requested_laps_refuses"
        status: pass
    human_judgment: false
  - id: D2
    description: "Same-window baseline verification on exactly the selected samples: constant and two-Kepler rows equal a third test-side recomputation, short-window means and formula scores differ from full-window values (no borrowed [0,10] constants), explicit formula nonapplicability on both paths never becomes a score, tampered windows/grid hashes and manufactured applicability refuse, and the GAP-59-08 note rides the evidence with no energy-threshold ruling"
    requirement: EXP-05
    verification:
      - kind: unit
        ref: "tests/phase67/test_windows.py#SameWindowExpectationTests.test_short_window_constant_and_kepler_match_independent_recomputation"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_windows.py#SameWindowExpectationTests.test_formula_nonapplicability_is_explicit_and_never_a_score"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_windows.py#SameWindowExpectationTests.test_a_tampered_window_against_the_prefix_refuses"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_windows.py#SameWindowExpectationTests.test_a_mismatched_grid_hash_refuses"
        status: pass
      - kind: unit
        ref: "tests/phase67/test_windows.py#SameWindowExpectationTests.test_tampered_harness_applicability_refuses"
        status: pass
    human_judgment: false

duration: 24 min
completed: 2026-11-02
status: complete
---

# Phase 67 Plan 03: Design & Settings Ladders — Signed-Lap Windows Summary

**D-06's exact sampled signed-lap prefixes (the earliest existing gold sample whose cumulative signed census-normal turns reach 1/2/5/10 laps, with exact inclusive retention and locked global tau) plus independently cross-checked same-window constant and two-Kepler baselines that refuse tampered windows, grids and manufactured applicability.**

## Performance

- **Duration:** 24 min resume session (18:42–19:06 UTC, 2026-11-02); the task-1 RED was committed by the interrupted prior executor earlier the same day
- **Started:** 2026-11-02T18:42:20Z (resume; plan RED commit 5ed595e4 predates it)
- **Completed:** 2026-11-02T19:06:39Z
- **Tasks:** 2 of 2
- **Files modified:** 2 (1 new diagnostic module, 1 new test module)

## Accomplishments

- `first_lap_prefixes` implements D-06 end to end on analytic references with no corpus read: the census's ordered inner-pair separation and initial normal, signed `atan2` steps accumulated from zero on the first sample, the earliest existing crossing per requested count, the exact float64 gold timestamp as the endpoint, the loader's exact inclusive `physical_window` retention, locked-global-tau hashes, the full preceding/current bracket with actual coverage, and refusals for every malformed input class.
- The census aliasing guard is applied as one limit (pi from the frozen scorecard's census_rules) over both the observed principal step and the increment predicted by the local angular rate about the same normal — the measure that actually exposes a 1.5-pi-per-step aliased grid, which the principal measure alone can never see — while a 0.99-pi-per-step grid is admitted.
- `same_window_expectations` reuses the harness `_comparison_rows` and independently reconstructs the same-window mean-position constant (zero velocities) and the direct frozen `two_kepler_prediction` call before frozen scoring, agreeing at rtol 1e-8/atol 1e-10; nonapplicability stays explicit on both paths; prefix grid hashes, endpoint and sample count are cross-checked so different windows cannot borrow baselines or the [0,10] EXP-01 constants; the GAP-59-08 note rides every evidence mapping with no energy-threshold ruling.
- 26 synthetic tests (20 prefix + 6 expectation) prove the contract, both RED gates machine-verified `RED_EVIDENCE_OK`, and the Phase 67 discovery is 98 tests OK with the loader regression controls unchanged.

## Task Commits

1. **Task 67-03-01 RED: failing signed-lap prefix tests** - `5ed595e4` (test, prior executor) — 20 tests / 18 failures on the missing module; RED evidence re-verified `RED_EVIDENCE_OK` at resume.
2. **Task 67-03-01 GREEN: exact prefixes** - `fbc991af` (feat) — `first_lap_prefixes` with the dual-measure census guard, exact retention and hashes; 20 tests OK.
3. **Task 67-03-02 RED: failing same-window expectation tests** - `cf5d9919` (test) — target `test_short_window_constant_and_kepler_match_independent_recomputation`; machine-verified `RED_EVIDENCE_OK` (25 tests / 5 planned failures).
4. **Task 67-03-02 GREEN: verified baselines** - `aa65b781` (feat) — `same_window_expectations` with prefix cross-checks and the applicability-tampering control; 26 tests OK.
5. **REFACTOR: style alignment** - `d9b3a035` (refactor) — import order and docstring markup; no behavior change; 26 tests OK.

**Plan metadata:** this SUMMARY's commit (docs).

## Files Created/Modified

- `pinn/verification/diagnostic_phase67_windows.py` - `first_lap_prefixes`, `same_window_expectations`, `WindowPrefixRefused`, `WindowExpectationRefused`, the dual-measure unwrap guard, independent baseline rows and the prefix grid cross-check; reads no corpus
- `tests/phase67/test_windows.py` - analytic planar-reference fixtures, loader regression controls, 20 LapPrefixTests and 6 SameWindowExpectationTests

## Decisions Made

- The unwrap guard keeps the census's single exact threshold (pi) but measures the predicted local increment beside the observed principal step; this is the only way the guard can trip on a genuinely aliased grid, and it preserves the census admission semantics rather than inventing a new limit.
- Baseline agreement is deliberately a serialization/consistency tolerance, not a science bar: both paths run the same frozen functions on the same arrays, so the tolerance guards drift, and any applicability/reason mismatch refuses outright.
- `rough_planning_duration` exists only when `census_n_in` is supplied (labelled approximate, never the endpoint), keeping the planning cost estimate opt-in and separate from selection.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Aliasing-guard measure corrected during task-1 GREEN**
- **Found during:** Task 67-03-01 GREEN
- **Issue:** Reusing the census guard as the observed principal-step maximum alone can never trip at the limit — `arctan2` returns principal values strictly inside (-pi, pi], so a true 1.5-pi-per-step grid wraps to 0.5-pi steps and the cumulative turns silently run backwards (the RED test demanded the limit string `3.141592653589793` in the refusal, which that measure cannot produce).
- **Fix:** The guard now compares both the observed principal step and the increment predicted by the local angular rate about the same census normal (trapezoid over the recorded separation and derivative) against the single frozen scorecard limit; the aliased grid refuses naming the limit and the 0.99-pi grid is admitted.
- **Files modified:** pinn/verification/diagnostic_phase67_windows.py
- **Verification:** `test_angular_aliasing_refuses_through_the_census_limit` and `test_steps_just_under_the_census_limit_are_admitted` both pass; the full module is 26 tests OK.
- **Committed in:** fbc991af

**2. [Rule 2 - Missing critical] Tampered-applicability control added during task-2 GREEN**
- **Found during:** Task 67-03-02 acceptance-criteria verification
- **Issue:** The acceptance criterion "tampered window/grid/applicability evidence is rejected by the helper tests" had no test driving the helper's applicability-disagreement refusal — the RED set covered window and grid tampering but not a manufactured applicable row.
- **Fix:** Added `test_tampered_harness_applicability_refuses`, which injects a manufactured applicable two-Kepler row (finite score, refusal fields removed) over the `_comparison_rows` seam on the nonapplicable fixture and asserts the helper refuses naming applicability.
- **Files modified:** tests/phase67/test_windows.py
- **Verification:** 26 tests OK; phase67 discovery 98 OK.
- **Committed in:** aa65b781

---

**Total deviations:** 2 auto-fixed (1 bug, 1 missing critical coverage)
**Impact on plan:** Both fixes tighten the plan's own acceptance criteria; no scope creep.

## Issues Encountered

None beyond the deviations above. No file pinned by a Phase 65/66 registration was edited (both files are new), so the known phase66 live-pin transition state is unchanged from 67-02's record; no real corpus, timing or training ran, and the held-out evaluation remains unspent.

## Known Stubs

None - both symbols are fully implemented and independently tested; no placeholder values or unwired paths were introduced.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Wave 2 is complete (67-02 and 67-03 done), unblocking Wave 3 (67-04).
- 67-05 (window registration/reader rules) and the EXP-05 execution plans (67-08..67-15) can register prefixes through `first_lap_prefixes` and record baseline evidence through `same_window_expectations`, with `WindowPrefixRefused`/`WindowExpectationRefused` as the typed refusal surface.
- The lap-to-time conversion is now an exact sampled selection on real gold grids at execution time (the analytic tests prove the algorithm); no real metadata has been read yet, so census_n_in wiring per system belongs to the registration plans exactly as their plans direct.

## Self-Check: PASSED

Both created files exist on disk; all five production commits (`5ed595e4`, `fbc991af`, `cf5d9919`, `aa65b781`, `d9b3a035`) exist in history; both TDD gate sequences are present and ordered (test -> feat per task, plus one refactor); the task verify command re-ran green at final HEAD (26 tests OK) and the Phase 67 discovery is 98 tests OK; `git diff --check` clean over the plan range `5ed595e4^..HEAD`.

---
*Phase: 67-design-settings-ladders*
*Completed: 2026-11-02*
