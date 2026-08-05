---
phase: 49-conformance-gate
reviewed: 2026-08-05T06:22:08Z
depth: standard
files_reviewed: 22
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
  - pinn/training/checkpoint.py
  - pinn/training/config.py
  - pinn/training/config_yaml.py
  - pinn/training/controllers.py
  - pinn/training/guards.py
  - pinn/training/summary.py
  - tests/phase49/__init__.py
  - tests/phase49/test_gate01_table.py
  - tests/phase49/test_gate02_census.py
  - tests/phase49/test_gate03_invariants.py
  - tests/phase49/test_gate03_resume.py
  - tests/phase49/test_inst03_register.py
findings:
  critical: 11
  warning: 3
  info: 1
  total: 15
status: issues_found
---

# Phase 49: Code Review Report

**Reviewed:** 2026-08-05T06:22:08Z  
**Depth:** standard  
**Files Reviewed:** 22  
**Status:** issues_found

## Summary

The Phase 49 focused suites pass (86 tests), and the Phase 46 suite passes (151 tests plus 68 subtests), but the integrated implementation still has fail-closed and auditability defects. The shipped YAML examples cannot load, malformed instrumentation can suppress the causal-stall guard, preflight failures can escape without refusal evidence, forged artifacts can report eligibility, resume discards prior evidence, and the maintained Phase 41 launch suite remains red (16 failures). Wave 3 adds a summary crash for non-finite artifact values and a filesystem-path disclosure in Markdown rendering.

## Narrative Findings (AI reviewer)

## Critical Issues

### CR-01: Documented null invariant configuration cannot be loaded

**Severity:** BLOCKER  
**File:** `pinn/training/config_yaml.py:173-185`, `pinn/training/config.py:406-410`

**Issue:** A YAML nested dataclass field whose value is `null` is forwarded as `None` instead of being replaced by its default instance. The Phase 49 comments explicitly document absent or null `run.invariants` as the record-only state, but `RunConfig.__post_init__` rejects `None`. Both shipped `configs/stage0-example.yaml` and `configs/smoke.yaml` parse the comment-only mapping as `None` and fail before launch.

**Fix:** In `_map_section`, when a nested dataclass field is present with `None`, construct `nested_cls()` (or omit the key so the dataclass default applies). Add tests for omitted, `{}`, and explicit `null` values.

### CR-02: Malformed causal `front_idx` values bypass or crash invariant B

**Severity:** BLOCKER  
**File:** `pinn/training/guards.py:461-512`

**Issue:** The guard coerces `front_idx` with `int()` and rejects only `-1`. Values such as `-2`, `99`, and `1.9` are accepted; with `n_colloc=4`, `front_idx=99` makes `front_high_water >= n_colloc - 1`, so invariant B is permanently treated as saturated and never trips. `float('inf')` raises `OverflowError`, which is not converted into a HALT outcome or failure bundle. Persisted state has the same hole: `load_invariant_b_state` accepts any high-water value >= -1, and the next check can suppress the stall guard with an out-of-range value.

**Fix:** Require a finite, non-boolean integer `front_idx` and validate `-1` or `0 <= front_idx < n_colloc` before updating state. Reject/flag impossible restored high-water values when the first collocation length is known, and catch `OverflowError` alongside `TypeError`/`ValueError` into the invariant-A refusal path.

### CR-03: Non-`ValueError` metadata/census failures bypass refusal evidence

**Severity:** BLOCKER  
**File:** `pinn/conformance/preflight.py:239-273,305-365`, `pinn/conformance/census.py:125-199,264-266`, `pinn/train.py:972-977`

**Issue:** The run-start composition catches only `ValueError`. A syntactically valid list in `training_metadata.json` raises `AttributeError` at `raw.get`; permission/encoding/read failures raise `OSError`/`UnicodeError`; missing config attributes raise `AttributeError`; and a census probe can propagate import/runtime `TypeError` or `RuntimeError`. These paths never append the failed `run_start` event and escape the `main()` refusal handler, leaving an incomplete summary/audit trail (and potentially a traceback instead of a controlled non-zero exit).

**Fix:** Validate decoded metadata as a mapping and normalize expected setup/probe failures to one conformance exception. Catch that exception (or the complete `Exception` family for the setup boundary) in `run_start_preflight`, write the failed event first, then let `train.py` finish the run through its normal refusal path.

### CR-04: Scheduler corruption can skip refusal evidence before validation

**Severity:** BLOCKER  
**File:** `pinn/conformance/table.py:150-183`, `pinn/conformance/preflight.py:325-365`, `pinn/train.py:985-1006`

**Issue:** `math.floor(PHYS05_I_WARM_FRACTION * n_adam_k)` runs before `n_adam_k` is type/domain checked. A string raises `TypeError`, infinity raises `OverflowError`, and malformed state can therefore escape the `ValueError`-only catches at both run-start and stage-boundary sites without a failed artifact. The same state path accepts booleans and negative scheduler values through Python coercive equality/comparison.

**Fix:** Validate scheduler fields first (finite real caps, non-boolean non-negative integer budgets/warmup) and raise a dedicated conformance error for all malformed states. Catch it at both assertion sites and append the failed event before propagating.

### CR-05: Preflight loader accepts semantically forged “passed” artifacts

**Severity:** BLOCKER  
**File:** `pinn/conformance/preflight.py:60-146`, `pinn/training/summary.py:362-394`

**Issue:** `_validate_payload` checks shape and enum membership only. It accepts an empty assertion list, a stream without a first `run_start`, arbitrary event ordering, and `preflight_status: "passed"` paired with failed checks or a failed locked check. `_eval01_precondition_i` then trusts the forged status/check stream and can return `True`; a hand-edited artifact can claim eligibility without a successful run-start gate.

**Fix:** Require a non-empty ordered stream beginning with `run_start`; derive the top-level status from event/check outcomes; reject status/check contradictions and any failed locked check under a passed status; validate stage-boundary ordering before returning from `load_preflight`.

### CR-06: Resume destroys append-only preflight history

**Severity:** BLOCKER  
**File:** `pinn/conformance/preflight.py:149-174`, `pinn/train.py:741-758,967-977`

**Issue:** Every `PreflightRecorder` starts with an empty event list. A `--resume` reuses the existing run directory but calls `run_start_preflight` again, whose first `_write()` replaces the old `preflight.json`. Prior stage-boundary and failure events are lost, contradicting the recorder’s append-only contract and making a resumed run’s conformance evidence non-reproducible.

**Fix:** On resume, load and validate the existing artifact and seed the recorder with its assertions before appending the new attempt, or write a distinct attempt log while retaining the canonical history. Add a resume test that asserts old event order and records remain present.

### CR-07: Closed divergence entries do not prove their proof tests exist or pass

**Severity:** BLOCKER  
**File:** `pinn/conformance/register.py:114-125,152-164`

**Issue:** The loader treats any non-empty string as a valid `proof_test`; it never resolves the module/node or verifies that the referenced test passes. A hand-edited register can mark a divergence closed with a nonexistent or failing proof, and preflight trusts that closed status. The separate test that scans the committed JSON is not runtime validation of future register edits.

**Fix:** Resolve every closed proof node against the repository and fail closed when its module or test node is absent; require the referenced proof to be executed by the verification path before accepting closure.

### CR-08: Census probes prove symbol existence instead of producer contracts

**Severity:** BLOCKER  
**File:** `pinn/conformance/census.py:39-68,114-133,250-314`

**Issue:** Pipeline quantities (`target_positions`, `masses_ordered`, `IC13`) and derived quantities are marked resolved when `importlib` can find a class or private method. No producer is instantiated, no admitted record is read, and no shape, ordering, finiteness, or value contract is checked. A stub or broken adapter therefore yields a passing census and lets the central gate claim quantities resolve.

**Fix:** Replace symbol-only pipeline/derived probes with fixture-backed producer calls that validate concrete fields, shapes, ordering, and finite values at the boundary. Add corruption/removal tests that require a blocked census.

### CR-09: Exact table comparison accepts boolean and negative scheduler state

**Severity:** BLOCKER  
**File:** `pinn/conformance/table.py:43-61,128-183`

**Issue:** `_check` uses untyped `==`, so `True == 1.0` and `False == 0.0` satisfy locked cap rows. Negative `n_adam_k` can also make a negative warmup appear conformant when the arithmetic happens to match, despite the scheduler contract rejecting negative budgets. Restored mutable scheduler state must not be trusted solely because Python coercion says it equals the expected literal.

**Fix:** Enforce exact scalar types and domains before comparison: reject booleans, require finite non-negative real caps, and require non-negative integer budget/warmup fields. Compare only after those checks pass.

### CR-10: New Stage-0 gate leaves the maintained launch suite red

**Severity:** BLOCKER  
**File:** `pinn/train.py:962-977`; affected fixture `tests/phase41/test_train_entrypoint.py:75`

**Issue:** The launch gate now refuses `lambda_e_max: 1.0`, while the maintained Phase 41 launch fixture still creates that value. `.venv/bin/python -m pytest -q tests/phase41/test_train_entrypoint.py` currently reports **16 failed, 5 passed**, with every failure occurring at the PHYS-05 refusal before training. Shipping with the integrated launch contract red prevents regression validation and normal entrypoint behavior.

**Fix:** Update launch fixtures and runnable examples to the locked Stage-0 row (`lambda_e_max: 0.0`), retaining explicit negative tests for non-conformant caps. If the old fixture is intentional, reconcile the stage/cap contract before enabling the gate.

### CR-11: Non-finite preflight values crash terminal summary finalization

**Severity:** BLOCKER  
**File:** `pinn/conformance/preflight.py:104-126,160-174`, `pinn/training/summary.py:344-359,547-559,681-684`

**Issue:** `json.loads` accepts `NaN`/`Infinity`, and `_validate_payload` never rejects non-finite values in check fields or nested evidence. The loader returns that payload as valid, but `summary.json` is written with `allow_nan=False`; finalizing a failed run then raises `ValueError: Out of range float values are not JSON compliant`, so the terminal summary is not produced. A malformed/tampered evidence artifact can therefore break the death-mode honesty guarantee.

**Fix:** Parse with a `parse_constant` hook that rejects non-standard JSON numbers and recursively validate finite numeric leaves before accepting a payload; also use `allow_nan=False` in the preflight recorder writer so invalid evidence cannot be created.

## Warnings

### WR-01: Locked-cap trip coverage does not cover every independent check

**Severity:** WARNING  
**File:** `tests/phase49/test_gate01_table.py:148-157`

**Issue:** The one-ULP refusal test mutates only `lambda_e_max`; the Stage-2 test also fails on that first locked row. There is no independent assertion that `lambda_phys_max` or `lambda_l_max` mismatches reach the locked refusal path.

**Fix:** Parameterize the trip test over all three locked cap fields and assert the reported field name for each.

### WR-02: Preflight file-read failures are not consistently normalized

**Severity:** WARNING  
**File:** `pinn/conformance/preflight.py:213-224`

**Issue:** `load_preflight` catches only a missing file and JSON syntax errors. Permission errors, directory targets, and invalid UTF-8 propagate as unrelated exception types, despite the loader’s documented fail-closed `ValueError` contract and the summary’s broad exception fallback.

**Fix:** Catch relevant `OSError`/`UnicodeError` cases and raise a path-specific `ValueError` with the original exception as the cause; add coverage for each class.

### WR-03: Conformance Markdown can disclose absolute filesystem paths

**Severity:** WARNING  
**File:** `pinn/training/summary.py:539-559`

**Issue:** The Markdown renderer dumps the entire `assertions` list, including exception strings from preflight. Metadata/read failures embed absolute `run_dir` paths (for example, `/tmp/.../training_metadata.json`), violating the module’s no-absolute-path redaction invariant even though `summary.md` is intended to be safe for human sharing.

**Fix:** Keep the verbatim evidence only in `summary.json`; redact or reduce path-bearing error strings for Markdown (for example, render event/status/check names and a relative artifact name rather than raw `actual` text).

## Info

### IN-01: `_CONFORMANCE_KEYS` is unused and can drift from the loader schema

**Severity:** INFO  
**File:** `pinn/training/summary.py:90-99`

**Issue:** The tuple documents the nested artifact keys but is never referenced by composition or rendering; future schema changes can update it without affecting behavior.

**Fix:** Use it to assert/project the expected keys, or remove the dead constant and keep the loader as the single schema authority.

---

_Reviewed: 2026-08-05T06:22:08Z_  
_Reviewer: the agent (gsd-code-reviewer)  
_Depth: standard_
