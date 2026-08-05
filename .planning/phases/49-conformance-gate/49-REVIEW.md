---
phase: 49-conformance-gate
reviewed: 2026-08-05T05:51:16Z
depth: standard
files_reviewed: 19
files_reviewed_list:
  - configs/smoke.yaml
  - configs/stage0-example.yaml
  - pinn/conformance/__init__.py
  - pinn/conformance/census.py
  - pinn/conformance/divergence_register.json
  - pinn/conformance/preflight.py
  - pinn/conformance/register.py
  - pinn/conformance/table.py
  - pinn/constants.py
  - pinn/train.py
  - pinn/training/config.py
  - pinn/training/config_yaml.py
  - pinn/training/controllers.py
  - pinn/training/guards.py
  - tests/phase49/__init__.py
  - tests/phase49/test_gate01_table.py
  - tests/phase49/test_gate02_census.py
  - tests/phase49/test_gate03_invariants.py
  - tests/phase49/test_inst03_register.py
findings:
  critical: 10
  warning: 2
  info: 0
  total: 12
status: issues_found
---

# Phase 49: Code Review Report

**Reviewed:** 2026-08-05T05:51:16Z  
**Depth:** standard  
**Files Reviewed:** 19  
**Status:** issues_found

## Summary

The focused Phase 49 suite passes (70 tests), but the integrated gate has fail-closed, auditability, and configuration defects. Both shipped YAML examples fail to load, malformed inputs can escape without refusal evidence, and invalid causal statistics can suppress invariant-B enforcement. The new Stage-0 lock also leaves the existing Phase 41 launch suite at 16 failures.

## Narrative Findings (AI reviewer)

## Critical Issues

### CR-01: Documented null invariant configuration cannot be loaded

**Severity:** BLOCKER  
**File:** `pinn/training/config_yaml.py:173-185`, `pinn/training/config.py:406-410`

**Issue:** The shipped YAML comments promise that an absent or explicit `null` `run.invariants` value means record-only mode, but the YAML mapper forwards `None` instead of constructing the nested dataclass. `RunConfig.__post_init__` then raises `TypeError`. Both `configs/stage0-example.yaml` and `configs/smoke.yaml` use the documented empty value and fail immediately at launch.

**Fix:** Treat a `None` value for a nested dataclass field as its default instance (or omit it before construction), while retaining strict type checks for non-null values. Add tests for both omitted and explicit `invariants: null` configurations.

### CR-02: Malformed `front_idx` values bypass or crash the invariant gate

**Severity:** BLOCKER  
**File:** `pinn/training/guards.py:461-512`

**Issue:** The guard converts `front_idx` with `int()` and rejects only the `-1` sentinel. Values such as `-2`, `99`, and `1.9` are accepted; an out-of-range high-water mark (`99` with `n_colloc=4`) makes `saturated` true and permanently suppresses invariant B. `float("inf")` raises `OverflowError`, so the step has no HALT outcome or failure bundle. This allows malformed instrumentation to defeat the stall guard.

**Fix:** Validate the raw value as a finite, non-boolean integer and enforce the valid range/sentinel (`-1` or `0 <= front_idx < n_colloc`) before updating high-water state. Catch `OverflowError` and route every malformed value through the invariant-A refusal path. Use the contract's exact saturation condition after validation.

### CR-03: Malformed metadata can escape without a failed preflight artifact

**Severity:** BLOCKER  
**File:** `pinn/conformance/preflight.py:239-273,305-365`, `pinn/train.py:950-955`

**Issue:** `_metadata_for_census` calls `.get()` on parsed JSON without first requiring a mapping. A syntactically valid `training_metadata.json` containing a list raises `AttributeError`, while read/encoding/backend failures can raise other exception types. `run_start_preflight` and the launch call site catch only `ValueError`, so no `preflight.json` failed event is persisted and the normal refusal path is skipped. This violates the documented “write evidence before raising” contract for malformed setup artifacts.

**Fix:** Validate the decoded metadata type and normalize expected file, encoding, device, and metadata errors to a dedicated conformance exception. Catch that exception around the complete census composition, append the failed run-start event first, then propagate through the normal non-zero finish path.

### CR-04: Non-`ValueError` scheduler corruption skips refusal evidence

**Severity:** BLOCKER  
**File:** `pinn/conformance/table.py:150-154`, `pinn/conformance/preflight.py:325-365`, `pinn/train.py:963-984`

**Issue:** The warmup calculation performs `math.floor()` before validating `n_adam_k`; strings raise `TypeError` and infinities raise `OverflowError`. The preflight and stage-boundary callers record failures only for `ValueError`, so these malformed schedule states escape without a failed event. The same gate accepts booleans and out-of-domain negative values because comparisons use Python `==` without scalar/domain validation.

**Fix:** Validate all scheduler fields (finite numeric caps, non-negative integer counts, and non-boolean values) before arithmetic/comparison. Convert expected malformed state to one conformance exception and catch it at both preflight sites so evidence is written before propagation.

### CR-05: Preflight loader accepts semantically forged “passed” artifacts

**Severity:** BLOCKER  
**File:** `pinn/conformance/preflight.py:60-146,213-224`

**Issue:** `_validate_payload` checks only JSON shape and enum/type membership. It accepts an empty assertions list, a top-level `preflight_status: "passed"` paired with failed events/checks, and arbitrary event ordering. A hand-edited artifact can therefore claim conformance without a successful run-start assertion or with a failed locked check.

**Fix:** Require a non-empty ordered event stream beginning with `run_start`; derive the top-level status from event/check outcomes; reject status/check contradictions and failed locked checks under a passed status; validate the required stage-boundary ordering before returning from `load_preflight`.

### CR-06: Resume destroys append-only preflight history

**Severity:** BLOCKER  
**File:** `pinn/conformance/preflight.py:149-174`, `pinn/train.py:719-739,945-955`

**Issue:** Every `PreflightRecorder` starts with an empty event list. `--resume` reuses the existing run directory but calls `run_start_preflight` before loading the checkpoint, so the new `_write()` replaces the prior `preflight.json` and loses earlier stage-boundary and failure records. This contradicts the recorder’s append-only contract and makes an attempted run’s audit trail non-reproducible.

**Fix:** On resume, load and validate the existing artifact and seed the recorder with its assertions before appending the new event, or write a separate attempt log while retaining the canonical history. Add a resume test that checks event order and preservation.

### CR-07: Closed divergence entries do not prove their proof tests exist or pass

**Severity:** BLOCKER  
**File:** `pinn/conformance/register.py:114-125,152-164`

**Issue:** The loader treats any non-empty string as a valid `proof_test` for a `closed` entry; it never resolves the module/node or executes the referenced test. A committed register entry can therefore be marked closed with a nonexistent or failing proof, and `run_start_preflight` will trust that closed status. The separate test that scans the current JSON is not a runtime validation of future edits.

**Fix:** Resolve each closed proof node against the repository and fail closed when the module or test node is missing; require the verification/CI command to execute the resolved proof and record its passing result before accepting a closed status.

### CR-08: Census pipeline probes prove only symbol existence

**Severity:** BLOCKER  
**File:** `pinn/conformance/census.py:39-56,114-133,250-314`

**Issue:** Pipeline quantities such as `target_positions` and `masses_ordered` are declared resolved when `importlib` can find the `AdmittedSetAdapter` class. The same is true for derived quantities when a private method name exists. No producer is instantiated, no admitted record is read, and no shape, ordering, or value contract is checked. A stub or broken adapter therefore yields a passing census and allows the central gate to claim all quantities resolve.

**Fix:** Replace symbol-only pipeline/derived probes with fixture-backed calls that validate concrete fields, shapes, ordering, and finite values at the producer boundary. Add tests that remove or corrupt the actual quantity and require a blocked census.

### CR-09: Exact table comparison accepts boolean and negative scheduler state

**Severity:** BLOCKER  
**File:** `pinn/conformance/table.py:43-61,128-168`

**Issue:** `_check` uses untyped `==`, so `True == 1.0` and `False == 0.0` satisfy locked cap rows. `n_adam_k=-1` can also make the computed warmup and a negative `warmup_length` appear conformant, even though the scheduler constructor rejects negative budgets. A restored schedule is mutable state and must not be trusted merely because its values compare equal after Python coercion.

**Fix:** Enforce exact scalar types and scheduler domains before comparison: reject booleans, require finite non-negative real caps, and require non-negative integer budget/warmup fields. Only then perform the locked-row comparisons.

### CR-10: The new Stage-0 gate leaves the maintained launch suite red

**Severity:** BLOCKER  
**File:** `pinn/train.py:945-955`; affected fixture `tests/phase41/test_train_entrypoint.py:75`

**Issue:** The run-start gate now refuses `lambda_e_max: 1.0`, while the maintained Phase 41 launch fixture still creates that value. Running `.venv/bin/python -m pytest -q tests/phase41/test_train_entrypoint.py` produces **16 failed, 5 passed**, with every failure occurring before training at the PHYS-05 refusal. Shipping with the integrated launch contract red prevents regression validation and blocks normal entrypoint behavior.

**Fix:** Update launch fixtures and any training examples intended to run to the locked Stage-0 row (`lambda_e_max: 0.0`), while retaining explicit negative tests for non-conformant caps. If the old fixture is intentional, reconcile the stage/cap contract before enabling the gate.

## Warnings

### WR-01: Locked-cap trip coverage does not cover every independent check

**Severity:** WARNING  
**File:** `tests/phase49/test_gate01_table.py:148-157`

**Issue:** The one-ULP refusal test mutates only `lambda_e_max`; the Stage-2 test also fails on that first locked row. There is no independent assertion that `lambda_phys_max` or `lambda_l_max` mismatches reach the locked refusal path.

**Fix:** Parameterize the trip test over all three locked cap fields and assert the reported field name for each.

### WR-02: Preflight file-read failures are not consistently normalized

**Severity:** WARNING  
**File:** `pinn/conformance/preflight.py:213-224`

**Issue:** `load_preflight` catches only missing files and JSON syntax errors. Permission errors, directory targets, and invalid UTF-8 propagate as unrelated exception types, despite the loader’s fail-closed `ValueError` contract.

**Fix:** Catch the relevant `OSError`/`UnicodeError` cases and raise a path-specific `ValueError` with the original exception as its cause; add coverage for each class.

---

_Reviewed: 2026-08-05T05:51:16Z_  
_Reviewer: the agent (gsd-code-reviewer)_  
_Depth: standard_
