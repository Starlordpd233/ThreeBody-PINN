---
phase: 65-probe-on-the-record-fit-harness
reviewed: 2026-10-29T22:09:25Z
depth: standard
runtime: general-purpose (gsd-code-reviewer role definition loaded)
files_reviewed: 15
files_reviewed_list:
  - pinn/evaluate.py
  - pinn/train.py
  - pinn/training/checkpoint.py
  - pinn/training/resume.py
  - pinn/verification/diagnostic_data.py
  - pinn/verification/diagnostic_fit.py
  - pinn/verification/diagnostic_guard.py
  - pinn/verification/diagnostic_probe.py
  - pinn/verification/diagnostic_similarity.py
  - pinn/verification/diagnostic_variants.py
  - tests/phase65/__init__.py
  - tests/phase65/test_contracts.py
  - tests/phase65/test_fit_short.py
  - tests/phase65/test_isolation.py
  - tests/phase65/test_probe.py
findings:
  critical: 0
  warning: 6
  info: 7
  total: 13
status: issues_found
---

# Phase 65: Code Review Report

**Reviewed:** 2026-10-29T22:09:25Z
**Depth:** standard
**Files Reviewed:** 15
**Status:** issues_found

## Summary

All 15 submitted files were read in full and reviewed at standard depth (per-file
analysis with Python-specific checks: bare excepts, mutable default arguments,
eval/exec, untyped exception paths, path-traversal handling, unbounded loops,
test-reliability patterns), with the Phase 65 diff (`be7c2af8^..HEAD`) used to
attribute findings to this phase's changes versus pre-existing behavior.

High-level assessment: the phase's stated security invariants hold as
implemented. Every `torch.load` site in the reviewed set passes
`weights_only=True` (diagnostic_guard.py:127,197; diagnostic_probe.py:519;
evaluate.py:463; checkpoint.py:295,322,588); the diagnostic refusal is raised
outside every corrupt-file handler so a marked payload can never be silently
skipped over (checkpoint.py `peek_latest_selection` / `_scan_first_valid`);
evaluate.py and train.py both refuse diagnostic content before the evaluation
claim / run-directory creation respectively; all subprocess invocations use
argument lists (no shell injection); the committed-registration gate validates
repo-relative paths and hash-checks every enumerated artifact before any corpus
or weight access; and the optimizer interlock correctly refuses construction
through `Optimizer.__init__` with correct restore in `finally`.

No critical (blocker) defects were found. Six warnings and seven info items
were found — concentrated in input-validation and typed-refusal coverage of the
new probe/fit tooling (a hang on degenerate registration tokens, unhandled
exceptions on the verify-result CLI paths, and two spots where record-supplied
paths or malformed registration content bypass the otherwise-strict typed
refusal conventions), plus one defense-in-depth gap in the marker predicate
itself (list-nested markers evade content detection).

Excluded as known owner-routed items (documented in 65-FINDINGS.md §7 and the
plan SUMMARYs; not re-counted): the 65-05 probe registration digest drift for
`diagnostic_fit.py`/`diagnostic_guard.py` and the resulting single failing test
(`RegistrationContentTests.test_the_recorded_dependency_and_source_digests_match_disk`);
the `diagnostic_probe._render_stdout` KeyError on `preserved_only` verdicts; the
empty `reading_rule.new_measurements` field; the missing standalone
logger-parity subcommand; and the stdout-rendering suite gap.

## Warnings

### WR-01: Diagnostic-marker predicate does not recurse into lists — a list-nested marker evades every content check

**File:** `pinn/verification/diagnostic_guard.py:87-94`
**Issue:** `_carries_marker` recurses only into `Mapping` values
(`any(_carries_marker(value) for value in payload.values() if isinstance(value, Mapping))`).
A payload that hides the marker inside a list or tuple — e.g. a
production-complete CTX-53 envelope with `"notes": [{"diagnostic": True,
"artifact_kind": "diagnostic"}]` — passes `require_not_diagnostic` (and therefore
the evaluate.py/train.py entry-point refusals), passes
`carries_diagnostic_marker` in every checkpoint load route, and passes
`_is_structurally_valid` (checkpoint.py:197-233), so it would enter a graded run
or the one-time evaluation. Every diagnostic writer in this repository emits the
marker at the top level, so all *existing* artifacts are caught; this is a
defense-in-depth gap in the phase's core laundering refusal, reachable only by a
hand-crafted artifact, but the guard's own docstring claims content-based
detection independent of how the marker is wrapped ("an envelope with all
production-required keys added around the marker is still refused").
**Fix:** recurse into list/tuple containers as well:

```python
def _carries_marker(payload) -> bool:
    if not isinstance(payload, Mapping):
        if isinstance(payload, (list, tuple)):
            return any(_carries_marker(item) for item in payload)
        return False
    if payload.get("diagnostic") is True or payload.get("artifact_kind") == ARTIFACT_KIND:
        return True
    return any(
        _carries_marker(value) for value in payload.values()
        if isinstance(value, (Mapping, list, tuple))
    )
```

### WR-02: `derive_cell` hangs forever on non-finite registration tokens ("inf", "-inf", "nan")

**File:** `pinn/verification/diagnostic_probe.py:124-180`
**Issue:** `derive_cell` validates only that `render(float(token), formatter) ==
token`. For a committed registration naming token `"inf"` (or `"-inf"`) under
any formatter where `format(inf, fmt)` is `"inf"` (e.g. `.3f`, `.3g`), the
`boundary` exponential search loops forever because `outside == known_inside`
stays true (`inf - k == inf`). For token `"nan"`, `boundary` returns `(nan,
nan)` and the bisection loop never terminates: all comparisons with NaN are
False, so neither the `break` condition nor the low/high update can make
progress. `compare_field` calls `derive_cell` for every registered field, so one
such token hangs `run_probe` indefinitely (no deadline interlock on the probe
path) instead of raising the typed `RegistrationError`. The historical tokens
are finite, so the committed registration is unaffected; this is an unbounded
loop reachable through a degenerate or malicious registration document.
**Fix:** refuse non-finite tokens before the search:

```python
token = str(token)
anchor = float(token)
if not math.isfinite(anchor):
    raise RegistrationError(
        f"a registered token must be finite; got {token!r}"
    )
if render(anchor, formatter) != token:
    raise RegistrationError(...)
```

### WR-03: verify-result CLIs crash with unhandled exceptions instead of the documented typed exit 2

**File:** `pinn/verification/diagnostic_fit.py:1296-1301,1418-1429,1561-1566` and `pinn/verification/diagnostic_probe.py:986-995,1115-1124`
**Issue:** both `main()` implementations document "exit codes: 0 ok, 2 refused",
but the caught-tuples omit several refusals the verify paths can raise:
`read_diagnostic_record` raises `json.JSONDecodeError` (a bare `ValueError`) on a
garbage result file and `DiagnosticArtifactRefused` on a non-diagnostic one;
`read_diagnostic_weights` raises `DiagnosticArtifactRefused`; a missing
`--result` file raises bare `FileNotFoundError` in both modules. None of these
are in `(DiagnosticFitRefused, DiagnosticRegistrationRefused, FirstResultExists)`
(diagnostic_fit.py:1564) or `(ProbeRefused, DiagnosticRegistrationRefused,
RegistrationError)` (diagnostic_probe.py:1122), so the operator gets a traceback
and exit 1 rather than the typed refusal. A tampered result — exactly the input
verify-result exists to adjudicate — is the most likely trigger.
**Fix:** either catch `DiagnosticArtifactRefused`, `ValueError`, and
`OSError` in the verify branch and re-raise as the module's typed refusal, or
wrap the `verify_*` call:

```python
try:
    verify_fit_result(args.registration, args.result, repo_root=repo_root)
except (DiagnosticFitRefused, DiagnosticRegistrationRefused,
        FirstResultExists, DiagnosticArtifactRefused, ValueError, OSError) as exc:
    print(f"FIT-REFUSED: {exc}", file=sys.stderr)
    return 2
```

### WR-04: Result-record-supplied paths are joined without the repo-relative validation used everywhere else

**File:** `pinn/verification/diagnostic_probe.py:1007-1013` and `pinn/verification/diagnostic_fit.py:1417-1429`
**Issue:** `verify_result` builds `registration_file = root /
registration_relative` straight from the result JSON. `pathlib` discards the
left operand when the right side is absolute, and `".."` segments are not
rejected, so a tampered result can point the digest check (and
`load_registration`) at any file inside or outside the repository — a hash
oracle inconsistent with `_one_entry`'s strict refusal of absolute/`..` paths
(diagnostic_guard.py:277-288). The same class applies to
`verify_fit_result`'s weights lookup, `result_file.parent /
weights_block.get("file", "")`, where the file name comes from the record being
verified. Both are read-only paths and the recorded digests still have to match,
so impact is low, but the inconsistency undercuts the gate's own convention.
**Fix:** route both through a shared repo-relative resolver before joining, e.g.
reuse `_one_entry` (or an equivalent check) on the record-supplied path:

```python
relative_path, _ = _one_entry({"path": registration_relative, "sha256": ""}, "result.registration")
registration_file = root / relative_path
```

### WR-05: Malformed probe-section registration content raises untyped KeyError / raw ValueError instead of a typed refusal

**File:** `pinn/verification/diagnostic_probe.py:708-719,772-797,849-860,199-205`
**Issue:** the shared committed-registration gate validates the artifact
enumeration but treats the `probe` section as opaque, and `run_probe` then
indexes it unguarded: `entry["rows"]`, `row["state"]`, `row["fields"]`,
`parity_spec["arm_id"]`, `parity_spec["state"]` raise raw `KeyError`, and
`compare_field`'s `float.fromhex(str(recorded[key]))` (line 201) raises a bare
`ValueError` on a malformed recorded cell hex. `main` catches only
`(ProbeRefused, DiagnosticRegistrationRefused, RegistrationError)`, so a
committed registration with a malformed probe section crashes the CLI with a
traceback and exit 1 instead of the module's typed refusal convention — the same
contract gap as WR-03 but on the admission/measurement side.
**Fix:** validate the probe section's shape up front in `_validate_probe_spec`
(rows/state/fields present per row, logger_parity keys present, cell hex
well-formed) and raise `RegistrationError` there; or convert these access sites
to `.get(...)` + explicit `RegistrationError` raises.

### WR-06: `measure_time_signal` validates `times_physical` monotonicity but not the tau column it actually differentiates against

**File:** `pinn/verification/diagnostic_similarity.py:177-193`
**Issue:** the shared measurement refuses non-increasing `times_physical`
("non-increasing times are refused, never sorted"), but the gold rate comparator
is computed as `torch.gradient(flat_targets, spacing=(tau,), dim=0)` where
`tau = X[:, 0]` — a column that is never checked for monotonicity. A caller
supplying samples whose tau column is non-monotonic (while physical times
happen to increase) gets a silently meaningless `rms_gold` denominator and hence
a wrong `output_rate_ratio` — the exact quantity the DIAG-09 registration
reproduces and the fit logger records. Today's loader derives tau from the
validated times, so the committed results are sound; the single shared
implementation (D-05) does not enforce its own documented contract.
**Fix:** add the same strict-increase refusal for the tau column before the
gradient computation:

```python
if not bool((tau[1:] > tau[:-1]).all()):
    raise MeasurementRefused(
        "tau_ic13's normalized-time column must be strictly increasing; "
        "non-monotonic tau is refused, never sorted"
    )
```

## Info

### IN-01: `validate_smoke_settings` accepts a numeric-string `t_start` while strictly type-checking `t_end`

**File:** `pinn/verification/diagnostic_fit.py:368-376`
**Issue:** `float(window.get("t_start", float("nan"))) != 0.0` coerces before
comparison, so `"0.0"` (a string) or other float-coercible junk passes the
window-start gate, while `t_end` three lines later is explicitly
type-checked against `(int, float)`. Inconsistent input validation in the
pre-data admission gate.
**Fix:** apply the same bool/type guard to `t_start` as `t_end` uses.

### IN-02: `measure_time_signal` — duplicated reshape and a dead branch

**File:** `pinn/verification/diagnostic_similarity.py:144,184,246`
**Issue:** `Y = targets.reshape(count, -1)` (line 144) is immediately repeated
as `flat_targets = Y.reshape(count, -1)` (line 184); and
`times[:-1].diff() if count > 1 else torch.zeros(0, ...)` (line 246) can never
take the else branch because `count >= 2` is enforced at line 141.
**Fix:** drop the duplicate reshape and the dead conditional.

### IN-03: probe CLI prints `result=None` when `--result` is omitted

**File:** `pinn/verification/diagnostic_probe.py:1110-1113`
**Issue:** on `run`, the completion line prints `result={args.result}`, but
`args.result` is `None` when the default `reproduction.json` path was used, so
the operator-facing summary names a path that was not written.
**Fix:** resolve `result_path` first (or print `result["attempt"]`-derived
actual path).

### IN-04: Dead `except BaseException: raise` wrapper in `run_probe`

**File:** `pinn/verification/diagnostic_probe.py:881-883`
**Issue:** the try/except around the interlock block re-raises unconditionally
and does nothing — unlike the fit module's corresponding handler, which marks
the attempt. Harmless (the exclusive attempt already records incompleteness by
existing), but misleading to readers.
**Fix:** delete the wrapper or make it do the documented "attempt stays
incomplete" bookkeeping explicitly.

### IN-05: `Stage0TrainingReader._admit` reaches into the private `split_allowlist._ATTESTATION` global

**File:** `pinn/verification/diagnostic_data.py:211-214`
**Issue:** the guarded reader manually increments another module's private
`_ATTESTATION.refused_before_open` to mirror bookkeeping its hook would
normally provide. If the parent's refusal accounting changes, this silently
double-counts or under-counts attested refusals. (Confirmed against
split_allowlist.py:259-264 that the counts currently agree; tests only assert
`>= 1`.)
**Fix:** expose a small public hook on `AllowlistedCorpusReader` (e.g. an
overridable `_note_refusal()`) that the subclass calls instead of the private
global.

### IN-06: Optimizer interlock's subclass snapshot misses optimizers defined after it starts

**File:** `pinn/verification/diagnostic_probe.py:302-312`
**Issue:** `optimizer_interlock` enumerates `Optimizer.__subclasses__()`
transitively at entry. An optimizer subclass imported/defined during the probe
body would escape the `step` patch (its `__init__` is still refused via
`Optimizer.__init__`, so the practical path stays closed; the module docstring's
"every loaded subclass" claim is snapshot-scoped).
**Fix:** none required for correctness; optionally note the snapshot semantics
in the docstring.

### IN-07: Tight flakiness bound in the supervised-timeout test

**File:** `tests/phase65/test_fit_short.py:1140-1155`
**Issue:** `test_a_supervised_worker_is_terminated_at_the_timeout` asserts
`elapsed < 15.0`, while `_run_supervised`'s worst case is
`join(timeout) + join(terminate_grace=10) + join(kill_grace=5)` = 15.5 s plus
process teardown. With `fork` and a plain sleeping worker SIGTERM terminates
immediately, so the bound holds in practice, but a loaded machine could
transiently exceed it.
**Fix:** raise the assertion bound above the supervisor's worst case (e.g.
`< 20.0`) or assert only on the status/payload.

---

_Reviewed: 2026-10-29T22:09:25Z_
_Reviewer: Claude (gsd-code-reviewer, general-purpose runtime)_
_Depth: standard_
