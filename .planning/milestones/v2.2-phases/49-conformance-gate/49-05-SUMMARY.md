---
phase: 49-conformance-gate
plan: 05
subsystem: testing
tags: [summary, conformance, preflight, fail-closed, eval01]

# Dependency graph
requires:
  - phase: 49-conformance-gate
    provides: "Validated preflight.json and the INST-03 divergence register from plans 49-01 and 49-04"
provides:
  - "Verbatim conformance projection and fail-closed EVAL-01 precondition-(i) flag in run summaries"
  - "Conformance markdown rendering for successful and refused/death-mode summaries"
  - "Trip-tested divergence-kind filtering, owner-N regression, and malformed/absent artifacts"
affects: [phase-50-real-corpus-run, phase-51-evaluation]

# Actuals (#2632)
actuals:
  tokens: 4111
  tasks: 2
  commits: 3

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Deferred conformance-loader imports with fail-closed summary rendering"
    - "Verbatim persisted-artifact projection paired with fixed markdown render order"

key-files:
  created:
    - .planning/phases/49-conformance-gate/49-05-SUMMARY.md
  modified:
    - pinn/training/summary.py
    - tests/phase49/test_inst03_register.py

key-decisions:
  - "EVAL-01 precondition-(i) blocks only open entries with kind divergence and status open; qualifications remain visible caveats but do not gate eligibility."
  - "The conformance payload is loaded through the validated preflight reader and passed through unchanged at every run disposition."
  - "Conformance renders before the non-success early return so refused and interrupted runs retain their evidence without re-enabling metric sections."

patterns-established:
  - "Summary projections keep persisted evidence separate from recomputed eligibility predicates."
  - "Malformed or absent conformance artifacts never raise during terminal summary composition."

requirements-completed: [INST-03]

coverage:
  - id: D1
    description: "summary.json carries the validated preflight payload verbatim and reports the kind-filtered eval01_precondition_i flag."
    requirement: INST-03
    verification:
      - kind: integration
        ref: "tests/phase49/test_inst03_register.py -k surfaces_in_run_record"
        status: pass
    human_judgment: false
  - id: D2
    description: "summary.md renders a Conformance section for valid, malformed, absent, finished, and failed/refused run states."
    requirement: INST-03
    verification:
      - kind: integration
        ref: "tests/phase49/test_inst03_register.py::test_surfaces_in_run_record_malformed_preflight_fails_closed_and_still_renders_conformance"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_summary_honesty.py tests/phase43/test_summary_enrichment.py"
        status: pass
    human_judgment: false

# Metrics
duration: 18min
completed: 2026-08-04
status: complete
---

# Phase 49 Plan 05: Conformance Projection Summary

**Run summaries now carry the validated preflight record verbatim and expose a fail-closed, divergence-kind-filtered EVAL-01 precondition-(i) status.**

## Performance

- **Duration:** 18 minutes
- **Started:** 2026-08-04T22:52:00-07:00
- **Completed:** 2026-08-04T23:10:01-07:00
- **Tasks:** 2
- **Files modified:** 2 (plus this summary)

## Accomplishments

- Added `_CONFORMANCE_KEYS`/`_CONFORMANCE_MD_ORDER`, validated preflight passthrough, and `_eval01_precondition_i` to `pinn/training/summary.py`.
- Kept conformance evidence available for failed/refused runs while preserving the existing success-gated metric sections and null policy.
- Added the `surfaces_in_run_record` suite covering open divergences, open qualifications, the owner-N closure branch, malformed artifacts, absent artifacts, and both eligibility truth directions.

## Task Commits

TDD gates were committed atomically:

1. **Task 1/2 RED: conformance summary projection tests** - `7eee7103` (test)
2. **Task 1 GREEN: preflight projection and EVAL-01 predicate** - `995fcab4` (feat)

**Plan metadata:** pending summary commit.

## Files Created/Modified

- `pinn/training/summary.py` - Loads the preflight artifact verbatim, computes fail-closed `eval01_precondition_i`, and renders the Conformance section for every disposition.
- `tests/phase49/test_inst03_register.py` - Exercises the projection and filter contract through the real preflight writer.
- `.planning/phases/49-conformance-gate/49-05-SUMMARY.md` - Records execution, verification, and plan metrics.

## Decisions Made

- The EVAL-01 precondition-(i) scope is exactly open `kind == "divergence"` plus `status == "open"`; qualification rows travel as caveats and do not block.
- A preflight refusal's persisted evidence is projected independently of run disposition; summary metrics remain success-gated.
- The helper revalidates through the conformance loader inside a deferred import and returns `False` for every import/read/parse/schema failure.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- The prescribed adjacent regression selection passed 272 tests and 70 subtests but had one unrelated pre-existing failure: `tests/phase43/test_real_data_smoke_config.py::SmokeYamlTests::test_smoke_yaml_loads_supported_fields` receives `run.invariants=None` while the already-landed Phase-49 config change now requires `InvariantsConfig`. This is outside the two files owned by this plan and was not changed.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Phase 50 can consume `summary.json.conformance` and the structural `eval01_precondition_i` flag without reverse-engineering preflight logs.
- The committed register still leaves `INV-B-N-UNSET` open; owner-controlled `N` remains the intended condition for a true precondition-(i) result on a real run.

---
*Phase: 49-conformance-gate*
*Plan: 05*
*Completed: 2026-08-04*

## Self-Check: PASSED

- Summary file exists at the canonical phase path.
- RED commit `7eee7103` and GREEN commit `995fcab4` are present in git history.
- No unintentional generated files or placeholder stubs were introduced in the owned source/test files.
