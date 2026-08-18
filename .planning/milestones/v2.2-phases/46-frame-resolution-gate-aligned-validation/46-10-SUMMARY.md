---
phase: 46-frame-resolution-gate-aligned-validation
plan: "10"
subsystem: training
tags: [inst-01, validation-gate, eval01-precondition, fail-closed, gap-closure]

requires:
  - phase: 46-frame-resolution-gate-aligned-validation
    provides: 46-07 validation frame ratification and gate-aligned validation wiring
provides:
  - "A strict semantic/contextual sidecar validator (validate_sidecar_payload) that recomputes every per-row and aggregate gate value through gate_metrics and rejects any payload that disagrees with its own rows"
  - "compact_validation_fields_from_payload: the eight compact gate_* fields derived exclusively from a validated persisted payload, never from a caller's in-memory observation"
  - "Every validation event (finite, NaN, +Inf, -Inf loss; ok or failed gate) leaves exactly one JSON-safe validation.jsonl line -- no early-return drop"
  - "The physical latest non-empty validation.jsonl line is the sole eligibility source; a later malformed/torn/blank/non-mapping/nonfinite/failed event can never expose an older eligible record"
  - "eval01_precondition_iii binds the JSONL record to its own exact same-run, same-step, fully-valid sidecar via type-and-value-sensitive equality of all eight compact fields"
affects: [INST-01 complete, 46-VERIFICATION.md gaps 1 and 2 closed, Phase 47 frame-completion work inherits a hardened receipt/eligibility contract]

tech-stack:
  added: []
  patterns:
    - "Strict numbers.Integral identity check (bool explicitly excluded) before any filename/record conversion"
    - "Validate-then-derive: compact fields are computed as a pure projection of an already-fully-validated payload, never independently"
    - "Physical-latest-line JSONL selection (no skip-and-fallback) for fail-closed eligibility"
    - "Type-AND-value equality (not bare ==) for JSON-decoded scalars to reject bool/int/float/string aliasing"

key-files:
  created: []
  modified:
    - pinn/training/validation_gate.py
    - pinn/train.py
    - pinn/training/summary.py
    - tests/phase46/test_artifacts.py
    - tests/phase46/test_validation_wiring.py

key-decisions:
  - "NonFiniteRetentionTests' _non_finite_observation fixture (test_artifacts.py) was rebuilt from a dataclasses.replace override to a plain make_observation([nan, inf, 0.0]) call, because the old override forced an aggregate_eps_h=Infinity that gate_metrics.aggregate_test_eps_h can never itself produce (any non-finite row poisons the aggregate to NaN, never +Inf) -- the new strict recomputation invariant (AC-46-10-02) cannot coexist with a hand-forced, non-recomputable aggregate. Mechanical/presentational fix, not a semantic one: the exact same three sentinel classes (NaN/Infinity/-Infinity) still appear in the payload, just at self-consistent field positions."
  - "_read_latest_validation_event treats a purely blank/whitespace physical last line as present-but-invalid (True, None), distinct from a missing/zero-length file (False, None) -- a defensive-only branch never exercised by the production writer (which always writes one complete JSON line), documented as a mechanical edge-case choice."
  - "eval01_precondition_iii's validation_gate import stays function-local (not moved to module scope), preserving the pre-existing stdlib-only honesty-layer contract that keeps the terminal summary renderable under torch-import failure."

requirements-completed: [INST-01]
completed: 2026-07-30
status: complete
---

# Phase 46 Plan 46-10: Fail-Closed Validation Gap Closure Summary

**Closed both remaining INST-01 verifier failures: the sidecar validator now recomputes every gate value through `gate_metrics` and binds compact fields to one validated payload (CR-03/CR-04), and every validation event -- including non-finite loss and gate failure -- is durably persisted so a later invalid event can never expose an older eligible record (CR-05); WR-01's step-aliasing warning is closed via a strict `numbers.Integral` identity check.**

## Performance

- **Duration:** ~50 min (including a 6m51s phase41+42 run and a 5m50s phase41+42+43 run)
- **Completed:** 2026-07-30T03:24:00Z
- **Tasks:** 2 completed
- **Files modified:** 5

## Accomplishments

- `pinn/training/validation_gate.py`: `sidecar_relative_path` now requires a strict `numbers.Integral` step (bool explicitly excluded) via a new `_strict_nonnegative_integral` helper; `validate_sidecar_payload` gained keyword-only `expected_run_dir_name`/`expected_global_step`/`expected_sidecar_path` bindings and enforces the complete v1 semantic contract (exact key sets everywhere, exact `split`/`gate_status` strings, coherent frame pairs with `ordered_raw` mass and a non-empty evidence ref, strict non-negative integer identities/counts, unique strictly increasing `record_key` triples, canonical thresholds, and per-row/aggregate SCS/verdict recomputed through `gate_metrics`); the new public `compact_validation_fields_from_payload` derives the eight compact fields exclusively from a validated payload, and `compact_validation_fields` now resolves/contains the candidate path and delegates to it.
- `pinn/train.py`: `_append_validation_record` no longer drops a non-finite `final_val_loss` -- every event leaves one JSON-safe line, with the step validated through `sidecar_relative_path` first, the loss encoded via `json_safe_float`, and trend `"unavailable"` whenever either loss is non-finite.
- `pinn/training/summary.py`: replaced the parse-all-and-skip-invalid `_read_jsonl_mappings` selection with `_read_latest_validation_event`, which inspects only the physical latest JSONL line and distinguishes missing/empty from present-but-invalid, so a later malformed event is never skipped in favor of an older good one. Hardened `_eval01_precondition_iii` to require a finite non-bool loss, a strict non-negative integer step, `gate_status == "ok"`, a same-run resolved-and-contained sidecar at the exact step-derived path, and type-and-value equality (`_json_scalar_equal`) of all eight persisted `gate_*` fields against `compact_validation_fields_from_payload`.
- `tests/phase46/test_artifacts.py`: added `StrictStepIdentityTests`, `SemanticInvariantTests`, `IdentityBindingTests`, and `PayloadDerivedCompactFieldsTests` covering AC-46-10-01 through -04.
- `tests/phase46/test_validation_wiring.py`: replaced the regression that pinned the unsafe early-return with a positive persistence assertion; added `LatestEventMonotonicityTests` (CR-05 stale-record fallback, torn/non-mapping/blank-only trailing lines, adjacent-step distinctness) and `Eval01IdentityBindingTests` (cross-run traversal, wrong-step/renamed-donor pointer, one-at-a-time mismatch for all eight compact gate fields).

## Task Commits

Each task was committed atomically:

1. **Task 1: Bind compact gate receipts to one fully validated sidecar** - `ad5331cd` (feat)
2. **Task 2: Make latest validation failure persistent and non-fallback** - `35c88d7f` (fix)

_Both tasks were TDD (`tdd="true"`); tests were written before/alongside the implementation and are folded into each single task commit per this plan's file-ownership boundaries (only two existing test modules are touched, no new test files permitted)._

## Files Created/Modified

- `pinn/training/validation_gate.py` - strict step identity, full v1 semantic validator, payload-derived compact fields
- `pinn/train.py` - persists every validation event, including non-finite/failed
- `pinn/training/summary.py` - physical-latest-event selection, hardened same-event eligibility binding
- `tests/phase46/test_artifacts.py` - Task 1 regressions (AC-46-10-01..04) plus a fixed non-finite-observation fixture
- `tests/phase46/test_validation_wiring.py` - Task 2 regressions (AC-46-10-05..09)

## Decisions Made

- The `NonFiniteRetentionTests` fixture in `test_artifacts.py` was rebuilt to be self-consistent under strict recomputation (see key-decisions above) -- a Rule 1 auto-fix, since the old fixture pinned a payload shape `gate_metrics` itself could never produce.
- `_read_latest_validation_event`'s blank-only-vs-missing distinction is a mechanical edge-case choice for a defensive branch the production writer never exercises; documented rather than treated as ambiguous, since it does not affect any physics/spec outcome.
- No STOP-protocol gap was raised: this plan's decision space (receipt identity, eligibility binding, persistence contract) is fully specified by the plan text, `46-VERIFICATION.md`'s two gap descriptions, and `46-REVIEW.md`'s five CR findings, none of which are physics/spec adjudications.

## Deviations from Plan

None beyond the one documented fixture rebuild above (already covered under Decisions Made, not a separate auto-fix against running code).

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Verification

| Check | Command | Result |
|---|---|---|
| Task 1 verify | `pytest tests/phase46/test_artifacts.py -x -q -rs` | 41 passed, 55 subtests passed, 0 skipped |
| Task 2 verify (part 1) | `pytest tests/phase46/test_validation_wiring.py tests/phase43/test_summary_enrichment.py -x -q -rs` | 30 passed, 13 subtests passed, 0 skipped |
| Task 2 verify (part 2) | `pytest tests/phase41/ tests/phase42/ -q` | 228 passed, 3 skipped (pre-existing), 4 subtests passed |
| Plan verification 1 | closure suites (`test_artifacts.py test_validation_wiring.py test_summary_enrichment.py`) | all pass, 0 skipped |
| Plan verification 2 | `pytest tests/phase46/ -q -rs` | 150 passed, 68 subtests passed, 0 failed, 0 skipped (up from the 114 baseline) |
| Plan verification 3 | `pytest tests/phase41/ tests/phase42/ tests/phase43/ -q` | 414 passed, 3 skipped, 26 subtests passed, **exactly 12 failed** -- all 12 match the orchestrator's pre-existing/environmental baseline list verbatim (`test_pilot_calibration.py` x2, `test_smoke.py` x1, `test_verdict_grounding.py` x7, `test_verify_gate.py` x2); none are new |
| Plan verification 4 | `git diff --name-only -- pinn/ tests/phase46 tests/phase43` (vs. pre-plan HEAD `ea8cd213`) | exactly the 5 plan-owned files; no dependency manifest, framework spec, probe artifact, or Phase 47 file touched |
| Plan verification 5 | `git diff --exit-code HEAD -- .../46-0[1-9]-PLAN.md` | exit 0 -- plans 46-01..09 byte-identical to HEAD |

The 12 pre-existing phase43 failures (environmental, unrelated to this plan's files) enumerated verbatim:

- `test_pilot_calibration.py::PilotCalibrationEvidenceTests::test_candidates_are_observation_linked_and_await_owner_ratification`
- `test_pilot_calibration.py::PilotCalibrationEvidenceTests::test_manifest_has_traceable_completed_seed_band_and_required_schema`
- `test_smoke.py::HonestyGuardTests::test_evidence_readme_documents_the_findings`
- `test_verdict_grounding.py::VerdictGroundingTests` (7 tests)
- `test_verify_gate.py::DurationGateLaunchTests::test_forecast_exactly_1800_accepted_run_dir_created`
- `test_verify_gate.py::DurationGateLaunchTests::test_over_limit_with_green_marker_accepted_run_dir_created`

## Next Phase Readiness

- INST-01 is complete: both `46-VERIFICATION.md` gaps (unbound/semantically-unvalidated sidecar; non-monotonic latest-event eligibility) are closed with executable regressions and root-cause fixes, not test-only patches.
- CONF-01 and CONF-08 are untouched by this plan (no files under their ownership were modified); the mandatory CONF-01 EVAL-01-precondition-(ii) qualification from GAP-46-06 travels forward unchanged.
- Phase 47's CONF-09 canonical-frame/rotation-scaling repair is explicitly out of this plan's scope and was not pulled forward; `RATIFIED_VALIDATION_FRAME` is unchanged.
- No held-out evaluator was invoked, imported, or modified; no training run, validation probe, real-corpus access, or dependency/lockfile change occurred.

## Self-Check: PASSED

All 5 modified/created source files confirmed present on disk; all 3 commit
hashes (`ad5331cd`, `35c88d7f`, `0ea7ead`) confirmed present in `git log --all`.

---
*Phase: 46-frame-resolution-gate-aligned-validation*
*Plan: 46-10*
*Completed: 2026-07-30*
