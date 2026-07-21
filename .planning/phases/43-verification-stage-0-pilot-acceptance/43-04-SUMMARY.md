---
phase: 43-verification-stage-0-pilot-acceptance
plan: 04
subsystem: verification-acceptance
tags: [acc-01, duration-gate, launch-preflight, fail-closed, timing-calibration]
status: complete
requires:
  - phase: 43-01 (verify ladder & fresh-marker fingerprint)
    provides: "current_fingerprint / read_verify_marker / marker_is_green_and_fresh — the fresh-green full-fingerprint predicate this gate consumes"
  - phase: 43-03 (real-data smoke composition & timing inputs)
    provides: "runs/.calibration/stage0-timing.json + forecast_from_calibration — the persisted measured s/step this gate forecasts from; run.smoke config flag"
provides:
  - "pinn.train._check_duration_gate — fail-closed >30-min launch duration gate, called from main() before run_dir.mkdir"
  - "pinn.train.DurationGateError — the typed refusal raised by the gate"
  - "tests/phase43/test_verify_gate.py — 16 tests over the full refusal/acceptance matrix against real persisted fixtures and a real subprocess launch"
affects:
  - "43-06 (the smoke run is now the only way to produce the calibration this gate requires before any subsequent non-smoke launch)"
  - "43-07 (Stage-0 pilot launches are long, non-smoke runs and now require a valid calibration, and a fresh green marker if forecast > 1800s)"
  - "43-08 (go/adjust/rethink verdict can cite ACC-01 as fully delivered — both the ladder (43-01) and its launch-time enforcement (43-04))"
tech-stack:
  added: []
  patterns:
    - "fail-closed pre-construction launch gate reusing a single shared runtime+code fingerprint (pinn.verify.current_fingerprint) across both a timing-calibration reader and a verify-marker predicate, so the two authorize the identical launch identity"
key-files:
  created:
    - tests/phase43/test_verify_gate.py
  modified:
    - pinn/train.py
key-decisions:
  - "Reconciled and kept the pre-existing uncommitted pinn/train.py work rather than rewriting it: independently verified it against 43-04-PLAN.md's must_haves/behavior/action, 43-SPEC.md prohibition 4 (R1/R2 edges), 43-CONTEXT.md CTX-71, and the 43-REVIEWS.md HIGH finding that specifically asked for this exact fail-closed contract (\"define fail-closed behavior when [the timing input] is absent\")."
  - "DurationGateError(ValueError) is the sole typed refusal; main() catches it and prints to stderr + returns 1, matching pinn.train's existing fail-closed CLI validation idiom (same pattern as RunFolderExistsError / HoldStageTargetError)."
  - "Exemptions (run.smoke, --resume) are applied at the call site in main() ('if not is_resume: _check_duration_gate(...)'), not baked into the gate itself for --resume — resume re-enters an already-authorized run and gating it again would lock an operator out of their own run past the marker's 24h window; run.smoke is checked as the gate's own first line since a smoke launch is the gate's calibration source."
  - "No new calibration/marker read paths invented — the gate consumes only the 43-01/43-03 public surface (verify.current_fingerprint, verify.read_verify_marker, verify.marker_is_green_and_fresh, timing.forecast_from_calibration) with one shared fingerprint object, so the calibration and the marker are checked against the identical device/dtype/torch/python/git-head identity."
requirements-completed: [ACC-01]
coverage:
  - id: D1
    description: "A non-smoke fresh launch with no valid persisted Stage-0 timing calibration is refused before run-directory creation (SPEC edge R2 — never fabricate a forecast)."
    requirement: ACC-01
    verification:
      - kind: unit
        ref: "tests/phase43/test_verify_gate.py#DurationGateFunctionTests.test_no_calibration_is_refused"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_gate.py#DurationGateFunctionTests.test_fingerprint_mismatched_calibration_is_refused"
        status: pass
      - kind: integration
        ref: "tests/phase43/test_verify_gate.py#DurationGateLaunchTests.test_no_calibration_refused_before_run_dir"
        status: pass
    human_judgment: false
  - id: D2
    description: "Forecast (persisted s/step times this launch's own declared Stage-0 budget) strictly above 1800s requires a fresh green full-fingerprint verify marker; exactly 1800s passes without one (SPEC edge R1)."
    requirement: ACC-01
    verification:
      - kind: unit
        ref: "tests/phase43/test_verify_gate.py#DurationGateFunctionTests.test_forecast_exactly_1800_passes_without_marker"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_gate.py#DurationGateFunctionTests.test_forecast_just_above_1800_without_marker_is_refused"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_gate.py#DurationGateFunctionTests.test_over_limit_with_green_fresh_marker_passes"
        status: pass
      - kind: integration
        ref: "tests/phase43/test_verify_gate.py#DurationGateLaunchTests.test_forecast_exactly_1800_accepted_run_dir_created"
        status: pass
      - kind: integration
        ref: "tests/phase43/test_verify_gate.py#DurationGateLaunchTests.test_over_limit_with_green_marker_accepted_run_dir_created"
        status: pass
    human_judgment: false
  - id: D3
    description: "A stale, code-mismatched, runtime-mismatched, or Git-unavailable verify marker cannot authorize an over-limit launch."
    requirement: ACC-01
    verification:
      - kind: unit
        ref: "tests/phase43/test_verify_gate.py#DurationGateFunctionTests.test_over_limit_with_stale_marker_is_refused"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_gate.py#DurationGateFunctionTests.test_over_limit_with_code_mismatch_marker_is_refused"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_gate.py#DurationGateFunctionTests.test_over_limit_with_runtime_mismatch_marker_is_refused"
        status: pass
      - kind: unit
        ref: "tests/phase43/test_verify_gate.py#DurationGateFunctionTests.test_over_limit_with_git_unavailable_marker_is_refused"
        status: pass
      - kind: integration
        ref: "tests/phase43/test_verify_gate.py#DurationGateLaunchTests.test_over_limit_with_stale_marker_refused_before_run_dir"
        status: pass
      - kind: integration
        ref: "tests/phase43/test_verify_gate.py#DurationGateLaunchTests.test_over_limit_with_code_mismatch_marker_refused_before_run_dir"
        status: pass
    human_judgment: false
  - id: D4
    description: "run.smoke:true launches are exempt from the gate regardless of calibration state (the smoke IS the gate's own calibration source)."
    requirement: ACC-01
    verification:
      - kind: unit
        ref: "tests/phase43/test_verify_gate.py#DurationGateFunctionTests.test_smoke_is_exempt_with_no_calibration"
        status: pass
    human_judgment: false
duration: ~50min
completed: 2026-07-21
status: complete
---

# Phase 43 Plan 04: Launch-Time Duration Gate Summary

**`pinn.train._check_duration_gate` — wired into the launch preflight before any run-directory/checkpoint/optimizer construction, forecasting from the persisted 43-03 Stage-0 timing calibration times the launch's own declared budget, and refusing both an absent calibration (unconditional on duration) and a >1800s forecast lacking a fresh green 43-01 verify marker.**

## Performance

- **Duration:** ~50 min (includes an extended regression sweep of `tests/phase41`/`tests/phase42`, real subprocess-heavy MPS suites)
- **Completed:** 2026-07-21
- **Tasks:** 1 (reconciliation of pre-existing uncommitted work; no rewrite needed)
- **Files modified:** 1 created (`tests/phase43/test_verify_gate.py`), 1 modified (`pinn/train.py`)

## Accomplishments

- **ACC-01 is now fully delivered end-to-end.** 43-01 built the `verify` ladder + marker; this plan wires the launch-time enforcement half — every fresh, non-smoke, non-resume `pinn.train` launch must present a valid persisted Stage-0 timing calibration, and any forecast strictly above 1800s (30 min) additionally needs a fresh green full-fingerprint verify marker.
- **The gate is fail-closed on both axes.** No calibration → refused, unconditionally on duration (SPEC edge R2: never invent a forecast from a step count or a default estimate). A forecast of exactly 1800s passes without a marker (SPEC edge R1); anything strictly above it needs the marker, and a stale/code-mismatched/runtime-mismatched/Git-unavailable marker is refused just like an absent one.
- **The gate runs before any construction.** `_check_duration_gate` is called in `main()` immediately after the run-folder collision check and before `run_dir.mkdir` — a refused launch leaves no run-dir, no checkpoint dir, and no model/optimizer behind. Verified directly by a real `python -m pinn.train` subprocess launch asserting the run-dir does not exist after a refusal.
- **One shared fingerprint authorizes both inputs.** The calibration read and the marker predicate both consume `verify.current_fingerprint(precision=, device=)`, so a calibration measured on one device/dtype/Torch/Python/Git-head combination can never silently authorize a launch on another.
- **Reconciliation, not a rewrite.** The prior session's uncommitted `pinn/train.py` changes (the `_DURATION_GATE_LIMIT_S` constant, `DurationGateError`, and `_check_duration_gate`) and the untracked `tests/phase43/test_verify_gate.py` already matched the plan's contract exactly on independent verification against `43-04-PLAN.md`, `43-SPEC.md` prohibition 4, `43-CONTEXT.md` CTX-71, and the 43-REVIEWS.md HIGH finding this plan addresses — nothing needed to change.

## Task Commits

1. **Task 1: Wire the persisted-calibration launch preflight** — `cae7f72f` (test) → `8538fec0` (feat)

_No refactor commit was needed — the reconciled implementation was already clean._

## Files Created/Modified

- `pinn/train.py` — `_DURATION_GATE_LIMIT_S = 1800.0`, `DurationGateError(ValueError)`, `_check_duration_gate(config, *, runs_root)`; called from `main()` before `run_dir.mkdir` for every non-resume launch.
- `tests/phase43/test_verify_gate.py` — `DurationGateFunctionTests` (10 tests, in-process against real calibration/marker fixture files) + `DurationGateLaunchTests` (6 tests, real `python -m pinn.train` subprocess launches proving pre-directory refusal).

## Decisions Made

- Kept the pre-existing implementation as-is after independent verification (see `key-decisions` in frontmatter) rather than re-deriving it — it already matched the plan, the SPEC edges, and the review finding it addresses.
- `DurationGateError` is a typed `ValueError`; `main()` prints its message to stderr and returns 1, following the same idiom as the file's other fail-closed CLI validation errors.
- Exemptions (`run.smoke`, `--resume`) are applied where the plan's own docstring specifies: `run.smoke` inside `_check_duration_gate` itself (first line, before any import); `--resume` at the call site in `main()` (the gate is skipped entirely, not passed a bypass flag).

## Deviations from Plan

None from the plan's own contract — the reconciled implementation satisfies every `must_haves.truths`/`behavior`/`action` clause in `43-04-PLAN.md` without modification, and all 16 of this plan's own tests plus the full `tests/phase43` regression suite pass.

### Discovery (not a plan deviation — an out-of-scope cross-plan regression, logged and NOT fixed here)

Wiring the gate into `main()` — exactly as the plan specifies — causes previously-green subprocess-launch tests in **other plans' owned files** to now fail, because none of them pre-write a persisted `runs/.calibration/stage0-timing.json` before a fresh non-smoke launch:

- **`tests/phase41/test_train_entrypoint.py`: 17/193 phase41 tests fail** (full list + root-cause analysis in `deferred-items.md` DI-43-04-01). All 17 are real `python -m pinn.train` subprocess launches; `tests/phase41/test_resume.py` (pure unit-level, no subprocess launches — the file 43-06-PLAN.md's own verify step targets) stays green, 30/30.
- **`tests/phase42` (operator runbook/monitoring): the same refusal confirmed** in `test_honesty_layer`, `test_redaction`, and `test_runs_contract` subprocess-launch tests (DI-43-04-02); config/unit-only tests in the same suite stay green. A full-suite enumeration was not completed in this session — several `test_runs_contract` "sigkill mid-<phase>" tests now poll for a status transition a gate-refused launch can never produce, paying out their full timeout before failing and materially inflating the suite's wall-clock time versus its pre-43-04 baseline.

This is **not a bug in this plan** — it is the plan's literal, review-requested contract (`43-REVIEWS.md` HIGH: "define fail-closed behavior when [the timing input] is absent"; `43-04-PLAN.md must_haves.truths`: "A non-smoke run with no valid persisted timing measurement is refused before construction" — unconditional on duration). It is **out of scope to fix here**: this plan's `files_modified` is `[pinn/train.py, tests/phase43/test_verify_gate.py]` only, and the executing task's instructions explicitly restrict owned/stageable paths to those two files plus the SUMMARY and tracking docs — `tests/phase41/*` and `tests/phase42/*` are other plans' owned files. Logged in full at `.planning/phases/43-verification-stage-0-pilot-acceptance/deferred-items.md` (DI-43-04-01, DI-43-04-02) rather than silently expanded into this plan's scope.

---

**Total deviations:** 0 (plan executed exactly as written; the pre-existing work was correct on arrival).
**Out-of-scope discoveries logged (not fixed):** 2 — DI-43-04-01, DI-43-04-02 (`deferred-items.md`).

## Issues Encountered

- The `tests/phase41`/`tests/phase42` regression sweep (beyond this plan's own required `tests/phase43` verification) took materially longer than expected because several affected tests now wait out a full polling timeout before failing rather than failing fast — see the Discovery section above. This did not block or change this plan's own completion; it is documented for whichever follow-up plan updates those fixtures.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- **ACC-01 complete.** Both halves — the `verify` ladder (43-01) and its launch-time enforcement (43-04) — are implemented, tested, and committed. `.planning/REQUIREMENTS.md` ACC-01 is marked complete by this plan's closeout.
- **43-06 (real smoke run) is now the load-bearing prerequisite for any subsequent non-smoke Stage-0 launch**, including the 43-07 pilot: without a real smoke run persisting `runs/.calibration/stage0-timing.json`, every non-smoke launch is refused by construction, not just by convention.
- **Follow-up needed (non-blocking):** `tests/phase41/test_train_entrypoint.py`'s and `tests/phase42`'s fresh-launch fixtures need a pre-launch calibration write (or a `run.smoke: true` config override where duration timing is not the point of the test) to stay green under the now-live production gate. Tracked in `deferred-items.md` (DI-43-04-01, DI-43-04-02); not part of this plan's scope.

## Known Stubs

None. `_check_duration_gate` is fully wired and exercised; nothing it returns or raises is a placeholder.

## Threat Flags

None beyond the plan's own register (`T-43-04-01`, `T-43-04-02`), which is mitigated as planned: both the missing-calibration path and the non-green-marker path return non-zero before any construction, and the marker predicate reuses 43-01's full runtime+code fingerprint.

---
*Phase: 43-verification-stage-0-pilot-acceptance*
*Completed: 2026-07-21*

## Self-Check: PASSED

- `pinn/train.py`, `tests/phase43/test_verify_gate.py`, this SUMMARY, and `deferred-items.md` all found on disk.
- Both task commits resolve in `git log`: `cae7f72f` (test), `8538fec0` (feat).
- `python -m unittest tests.phase43.test_verify_gate -v` — 16/16 pass.
- `python -m unittest discover -s tests/phase43 -v` — 136/136 pass.
