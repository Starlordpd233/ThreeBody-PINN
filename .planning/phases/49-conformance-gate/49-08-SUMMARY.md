---
phase: 49-conformance-gate
plan: 08
subsystem: conformance
tags: [summary, conformance, blocker-remediation, preflight, phys05, resume]

requires:
  - phase: 49-conformance-gate
    provides: "Plans 49-01..49-07 and CR-08 producer-contract remediation at 7d4ffd8d"
provides:
  - "Controlled persisted refusals for ordinary run-start setup/probe failures"
  - "Type/domain-safe scheduler-state conformance checks before arithmetic or comparison"
  - "Validated append-only preflight history across resumed attempts"
  - "Independent CR-08 producer-contract re-verification"
affects: [phase-50-valid-stage0-rerun, phase-51-authorized-evaluation]

actuals:
  tasks: 5
  commits: 1

key-files:
  created:
    - .planning/phases/49-conformance-gate/49-08-PLAN.md
    - .planning/phases/49-conformance-gate/49-08-SUMMARY.md
    - .planning/phases/49-conformance-gate/49-06-SUMMARY.md
  modified:
    - pinn/conformance/preflight.py
    - pinn/conformance/table.py
    - tests/phase49/test_gate01_table.py
    - tests/phase49/test_inst03_register.py
    - .planning/REQUIREMENTS.md
    - .planning/ROADMAP.md
    - .planning/STATE.md

key-decisions:
  - "Normalize ordinary Exception subclasses only at the run-start composition boundary; BaseException remains untouched."
  - "A scheduler state_dict is a plain-Python scalar contract: caps are finite non-negative int/float values excluding bool; budgets/warmup are non-negative exact ints."
  - "PreflightRecorder validates and deep-copies any existing artifact at construction, making append-only preservation independent of a new resume flag."
  - "CR-08 required no additional code: the fixture-backed producer implementation at 7d4ffd8d passed its corruption/removal suite unchanged."

requirements-completed: [GATE-01, GATE-02, GATE-03, INST-03]

completed: 2026-08-07
status: complete
---

# Phase 49 Plan 08: Remaining Blocker Remediation Summary

**CR-03, CR-04, CR-06, and CR-09 are remediated, and CR-08 is independently
re-confirmed against `7d4ffd8d`. Phase 49's required gate is green.**

## Blocker closure

### CR-03 — setup/probe failures now leave refusal evidence

`run_start_preflight` now treats the complete metadata/census composition as one
controlled boundary. It validates decoded metadata and census report shapes,
records a failed `run_start` event first, then raises
`ConformancePreflightError` (a `ValueError` subtype) so `train.main()` returns a
controlled non-zero exit. Runtime producer exceptions, malformed metadata, and
non-mapping census returns are covered.

### CR-04 / CR-09 — scheduler corruption cannot coerce or escape

`assert_phys05_table` validates every required scalar before table comparison or
warmup arithmetic. Matching booleans no longer satisfy float rows; string or
infinite budgets no longer leak `TypeError`/`OverflowError`; negative budgets and
boolean/negative warmup values are refused as `ValueError`. The real entrypoint
test proves a corrupt infinite budget writes the failed artifact before exit.

### CR-06 — resume preserves append-only history

`PreflightRecorder` loads and validates an existing `preflight.json`, deep-copies
its assertions, and appends the new attempt. Tests retain the original event
order and canonical event bytes, and prove malformed existing history is
refused without replacement.

### CR-08 — producer-contract re-check

No further change was required. At exact HEAD/base `7d4ffd8d`,
`tests/phase49/test_gate02_census.py` passed **13/13**. The suite exercises real
resident-source, batch, model, collocation, anchor, and non-data-term producers,
including malformed shape, finiteness, body ordering, missing-field, and raised
producer cases. `pinn/conformance/census.py` remains unchanged in Plan 49-08.

## TDD and review evidence

- Initial blocker selection against unchanged production code: **15 failed, 1
  passed** for the intended coercion, exception-leak, and overwrite defects. The
  lone baseline-green negative-warmup case represented behavior already refused;
  the RED negative-budget pair is the case that previously matched and passed.
- Review-discovered non-mapping census result: **1 failed** with the expected
  uncaught `AttributeError`, then passed after the boundary was widened.
- Final modified-file suites: **77 passed**.
- Standards review: no hard or judgment findings.
- Spec review: one initial BLOCKER and three evidence gaps found, remediated, then
  re-reviewed with no remaining missing, partial, wrong, or scope-creep findings.

## Final verification

| Command | Result |
|---|---|
| `.venv/bin/python -m pytest -q tests/phase49/test_gate02_census.py` | **13 passed** |
| `.venv/bin/python -m pytest -q tests/phase49/test_gate01_table.py tests/phase49/test_inst03_register.py` | **77 passed** |
| `.venv/bin/python -m pytest -q tests/phase49` | **176 passed** |
| Required cross-phase gate from 49-08 | **943 passed, 3 skipped, 289 subtests passed** |
| `.venv/bin/python -m compileall -q pinn/conformance tests/phase49` | pass |
| `git diff --check` | pass |

The cross-phase run emitted two pre-existing warnings: the Phase 38 COM-offset
warning fixture and PyTorch's requires-grad scalar-conversion warning.

## Scope retained

- Owner-ratified `N = 500` and `INV-B-N-UNSET` closure are unchanged.
- No admitted-corpus run or held-out evaluation occurred.
- No framework specification changed.
- WR-01, WR-02, WR-03, and IN-01 remain advisory/out of this BLOCKER-only wave.

## Next-phase readiness

All Phase 49 BLOCKERs are closed with executable evidence. Phase 50 may now be
planned; this result authorizes planning, not an unreviewed real-corpus launch.

---
*Phase: 49-conformance-gate · Plan: 08 · Completed: 2026-08-07*
