---
phase: 49-conformance-gate
reviewed: 2026-08-05T03:55:28Z
depth: standard
files_reviewed: 8
files_reviewed_list:
  - pinn/constants.py
  - pinn/conformance/__init__.py
  - pinn/conformance/table.py
  - pinn/conformance/preflight.py
  - pinn/train.py
  - pinn/training/controllers.py
  - tests/phase49/__init__.py
  - tests/phase49/test_gate01_table.py
findings:
  critical: 5
  warning: 2
  info: 0
  total: 7
status: issues_found
---

# Phase 49: Code Review Report

**Reviewed:** 2026-08-05T03:55:28Z  
**Depth:** standard  
**Files Reviewed:** 8  
**Status:** issues_found

## Summary

The focused Phase 49 suite passes (20 tests), but the gate is not fail-closed for malformed or tampered state and its artifact loader accepts semantically contradictory records. Resume launches erase prior preflight history, and the new Stage-0 lock leaves the existing Phase 41 launch suite red (16 failures). These issues affect correctness and auditability and should be fixed before shipping.

## Narrative Findings (AI reviewer)

## Critical Issues

### CR-01: Preflight loader accepts a forged passed status

**Severity:** BLOCKER  
**File:** `pinn/conformance/preflight.py:44-110,171-182`

**Issue:** `_validate_payload` checks only JSON shape, enum membership, and `passed`'s boolean type. It never checks that `preflight_status` agrees with event statuses/checks, that the assertions array is non-empty, or that the event sequence starts with `run_start` and then follows entered stage boundaries. For example, a payload with `preflight_status: "passed"` and a failed `run_start` event is accepted by `load_preflight`. The persisted artifact is the trust boundary used by later summary/evaluation code, so a tampered file can report a failed run as conformant.

**Fix:** Add semantic validation before returning: require a non-empty ordered event list, enforce the `run_start`/`stage_boundary` sequence, derive top-level status from locked-check failures (advisory failures remain non-blocking), and reject contradictions between event status and its checks. Validate check names and scalar values sufficiently for the downstream projection as well.

### CR-02: Invalid scheduler state can pass the exact table gate

**Severity:** BLOCKER  
**File:** `pinn/conformance/table.py:43-61,150-168`

**Issue:** `_check` relies on Python `==` without validating scalar types or domains. Consequently `True == 1.0` and `False == 0.0`, so a state dictionary containing boolean caps passes all Stage-0 locked rows. A tampered state with `n_adam_k = -1` and `warmup_length = -1` also satisfies the computed formula, despite `ScheduledWeights` rejecting negative budgets at construction. Checkpoint state is persisted input and can be loaded after construction; this lets invalid schedule state bypass the conformance claim.

**Fix:** Validate every state value before comparison: reject booleans, require finite real caps/IC values with the scheduler's non-negative domain, and require non-negative integer `n_adam_k`/`warmup_length`. Normalize only after validation and then perform the exact comparisons.

### CR-03: Non-ValueError gate failures skip refusal evidence

**Severity:** BLOCKER  
**File:** `pinn/conformance/table.py:150-154`, `pinn/conformance/preflight.py:195-214`, `pinn/train.py:927-962`

**Issue:** Malformed values are not normalized to `ValueError`: for example `n_adam_k = float("inf")` makes `math.floor(...)` raise `OverflowError`, and a string budget raises `TypeError`. `run_start_preflight` and the run-start call site catch only `ValueError`, so the exception escapes before `_failure_check` writes `preflight.json` (and before the normal `finish_run` path). At the stage hook, only `ValueError` is recorded; other gate failures reach the broad training catch without a failed stage-boundary record. This violates D-27 for malformed persisted state.

**Fix:** Make table input validation convert all expected malformed-state failures into a dedicated conformance exception (or `ValueError`) carrying the failing check. Catch that gate exception at both call sites, append the structured failed event, and only then re-raise through the existing non-zero finish path. Do not let `TypeError`/`OverflowError` escape the gate.

### CR-04: Resume launches overwrite append-only preflight history

**Severity:** BLOCKER  
**File:** `pinn/conformance/preflight.py:114-163,195-214`, `pinn/train.py:697-714`

**Issue:** `PreflightRecorder` always initializes `self._events` to an empty list. `main()` reuses the same run directory for `--resume`, so the next `run_start_preflight` writes a new one-event payload over the previous run's `stage_boundary` and failure records. This contradicts the recorder's append-only contract and destroys the evidence needed to explain an earlier attempt.

**Fix:** On construction, load and validate an existing `preflight.json` and seed `_events` before appending the new run-start event (or use a separately versioned attempt log while preserving the canonical history). Add a resume test proving prior events remain in order.

### CR-05: Existing launch contract is broken by the new gate

**Severity:** BLOCKER  
**File:** `pinn/train.py:918-933`

**Issue:** The new run-start assertion refuses `lambda_e_max: 1.0` for Stage 0, which is the value hard-coded by the existing Phase 41 launch fixture. Running `.venv/bin/python -m pytest -q tests/phase41/test_train_entrypoint.py` now produces **16 failed, 5 passed**, all failures occurring before training with `PHYS-05 ... lambda_e_max expected 0.0, actual 1.0`. This is a shipped regression in the composition root, not merely a new negative test.

**Fix:** Update all launch fixtures and user-facing Stage-0 examples that are intended to train to the locked Stage-0 row (`lambda_e_max: 0.0`), and add explicit refusal coverage for non-conformant values. If the old nonzero fixture is intentional, reconcile the stage/cap contract before enabling the gate; do not leave the baseline suite red.

## Warnings

### WR-01: Two locked cap checks have no independent trip coverage

**Severity:** WARNING  
**File:** `tests/phase49/test_gate01_table.py:148-157`

**Issue:** The only one-ULP cap trip mutates `lambda_e_max`. Stage-2 refusal also fails on that same first row, so there is no test that independently proves `lambda_phys_max` or `lambda_l_max` violations reach `_raise_locked`. This falls short of D-16's requirement that every added check be driven to failure.

**Fix:** Parameterize the adjacency/trip test over all three locked cap keys and assert each field name in the raised error (plus retain the existing Stage-2 integration test).

### WR-02: Loader file-read errors are not normalized to the promised ValueError

**Severity:** WARNING  
**File:** `pinn/conformance/preflight.py:171-182`

**Issue:** `load_preflight` catches only `FileNotFoundError` and `JSONDecodeError`. Permission errors, directory paths, and invalid UTF-8 propagate as `PermissionError`, `IsADirectoryError`, or `UnicodeDecodeError`, so the documented fail-closed loader does not provide a typed failure for all file-read cases.

**Fix:** Catch the relevant `OSError`/`UnicodeError` cases and raise a path-specific `ValueError` while preserving the original exception as the cause; add malformed-file tests for each class.

---

_Reviewed: 2026-08-05T03:55:28Z_  
_Reviewer: the agent (gsd-code-reviewer)_  
_Depth: standard_
