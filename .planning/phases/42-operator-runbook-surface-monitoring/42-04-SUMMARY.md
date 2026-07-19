---
phase: 42-operator-runbook-surface-monitoring
plan: 04
status: complete
completed: 2026-07-19
---

# Plan 42-04 Summary

## What was built

The canonical machine log (`JsonlStepHandler`) and its human mirror
(`HumanStepHandler`) as `logging.Handler` subclasses on the `pinn.training`
logger tree, consuming the widened `_log_step` record (42-01).

### 1. CTX-67 non-finite null-policy sanitizer

`_sanitize_step_record(record)` in `pinn/training/step_log.py`:
- Replaces every NaN/±Inf float with Python `None`
- Adds `finite: bool` (False iff any field was non-finite) and
  `nonfinite_keys: list[str]` (sorted affected field names)
- A fully-finite record gets `finite: True`, `nonfinite_keys: []`
- `json.dumps(sanitized, allow_nan=False)` never raises
- No string sentinels (`"NaN"`/`"Inf"`/`"-Inf"`) ever appear
- Independent of `pinn.training.guards._json_safe_scalar` (its
  string-sentinel policy is trip.json-local — Anti-Pattern #1)

### 2. JsonlStepHandler (append-only JSONL, OPS-03)

`JsonlStepHandler(logging.Handler)` writing to `runs/<name>/logs/train.log.jsonl`:
- Opens the file once in `"a"` mode; writes + `flush()` per step (no
  `os.fsync`, no `atomic_write_text` — Anti-Pattern #4)
- Filters the widened `extra=` record to the canonical `STEP_LOG_FIELDS`
  vocabulary — the `residuals_bin_*` family is EXCLUDED (TB-only, OPS-04b,
  cycle-2 review finding HIGH-1), so the registry-vs-JSONL parity assertion
  holds without a dynamic-key carve-out
- Passes the filtered dict through `_sanitize_step_record`, then
  `json.dumps(allow_nan=False)`
- Exposes `last_step_finite: Optional[bool]` (default None), updated to the
  sanitized record's `finite` value on each successful emit — read by the
  42-08 terminal-cause discriminator in-memory instead of re-parsing the
  JSONL from disk (cycle-2 review finding, agy MEDIUM)
- `emit` cannot raise into the step loop (standard `handleError` path)

### 3. HumanStepHandler (design §5.4 mirror)

`HumanStepHandler(logging.Handler)` writing to `runs/<name>/logs/train.log`:
- Step records render as the design §5.4 pipe-delimited line:
  `step N | stage k phase 2a | total=… data=… ic=… phys=… energy=… angmom=… | lr=… | … s/step | ETA …`
- Non-step events (run start, mem:, stage dispositions, guard trips) render
  as readable lines without crashing on records lacking step fields
- `emit` cannot raise into the step loop

## Verification

- `_sanitize_step_record` maps NaN/Inf → None, sets `finite`/`nonfinite_keys`;
  finite record gets `finite:true`, `nonfinite_keys:[]`;
  `json.dumps(allow_nan=False)` does not raise ✓
- `grep -c 'from pinn.training.guards import _json_safe_scalar' step_log.py`
  returns 0 (no string-sentinel import) ✓
- JsonlStepHandler writes one parseable JSON object per step; NaN field is
  `null` with `finite:false` ✓
- JSONL output carries canonical keys and EXCLUDES `residuals_bin_*` ✓
- Append mode (`open("a")`) confirmed; `grep -c 'atomic_write_text'` returns 0 ✓
- HumanStepHandler renders §5.4 line for steps; does not raise on non-step ✓
- `tests.phase42.test_step_log_jsonl`: 4/4 pass (happy-path field presence,
  registry parity + no-residuals-leak, E1 whole-file parseability under
  divergence, last_step_finite attribute) ✓
- Full `tests/phase42` discovery: 14 tests, 0 errors, 0 failures (10 skipped
  stubs, 4 OK) ✓

## Files modified

- `pinn/training/step_log.py` — `_sanitize_step_record`, `JsonlStepHandler`,
  `_format_step_line`, `HumanStepHandler`
- `tests/phase42/test_step_log_jsonl.py` — realized OPS-03 happy-path + E1
  whole-file non-finite coverage tests (4 test methods)
