---
phase: 49-conformance-gate
reviewed: 2026-08-11T06:40:17Z
depth: standard
files_reviewed: 6
files_reviewed_list:
  - pinn/conformance/preflight.py
  - pinn/training/summary.py
  - tests/phase49/test_e2e_seam.py
  - tests/phase49/test_gate03_invariants.py
  - tests/phase49/test_inst03_register.py
  - tests/phase49/test_preflight_integrity.py
findings:
  critical: 0
  warning: 1
  info: 2
  total: 3
status: issues_found
---

# Phase 49 (Plan 09): Code Review Report

**Reviewed:** 2026-08-11T06:40:17Z
**Depth:** standard
**Files Reviewed:** 6
**Review unit:** commit 93bdac47 (diff base 8727d1a3) — the 49-09 gap-closure wave
**Status:** issues_found

## Summary

The 49-09 change binds the run-local invariant-B window to the EVAL-01 precondition-(i) gate and makes eligibility require the run-start evidence it summarizes. The review unit was assessed against the 49-09-PLAN must_haves and prohibitions, with independent behavioral probes run against the shipped tree. Earlier phase-49 waves were reviewed separately (prior revisions of this file, latest d044b3de); only 49-09 interactions with pre-existing code were re-examined.

What was verified sound:

1. **Eligibility predicate (`evaluate_eval01_precondition_i`, preflight.py:549-602).** Fail-closed on every probed edge: empty-mapping census, case-variant verdict (`"Passed"`), non-string verdict (`True`), an incomplete second `run_start` in a resume history, and an open divergence riding a `stage_boundary` event — all deny eligibility; an open qualification travels without stranding the run (D-23/D-26). Every occurrence of every `REQUIRED_RUN_START_CHECKS` name must pass (preflight.py:591-598); census verdict compares by exact equality against `"passed"` (preflight.py:600); the open-`divergence` scan covers every event's `open_divergences` (preflight.py:578-583); the first event must be `run_start` (preflight.py:574).
2. **Single-accessor contract.** No attribute read of `front_advance_window_n` remains in preflight.py outside `_run_local_invariant_window` (preflight.py:460-473), which delegates to `guards._extract_invariant_window`; all other occurrences are string literals in evidence text. The `preflight.py:384` anti-pattern (reading `config.invariants` instead of `config.run.invariants`) is removed at its root, not patched around. No import cycle: `guards.py` imports only `pinn.training.atomic_io` and `pinn.training.stage_exit`.
3. **History-ordering placement.** `_assert_history_ordering` runs at load (preflight.py:376) and at write (preflight.py:309), and is deliberately absent from `append_event`'s single-record shape validation (preflight.py:338-344) — matching the plan's load-bearing D-27 separation. Append-only resume histories stay legal; `test_second_run_start_preserves_history_and_eligibility_verdict` pins second-`run_start` idempotency.
4. **Fixture-repair honesty.** The three census-terminal refusal tests are byte-identical between 8727d1a3 and 93bdac47 (verified by function-body hash, 15/22/20 lines respectively). The happy-path `summary["eval01_precondition_i"] is True` assertion in `test_real_main_orders_preflight_table_boundary_and_first_guard` carries zero diff lines. Pre-existing negatives in test_preflight_integrity.py still fail or pass for their originally encoded reasons: the forgery refusals still trip `_assert_status_consistency` at load, the advisory acceptance still loads, and `test_open_divergence_under_passed_status_loads_but_is_not_eligible` is denied solely by its open divergence — the upgraded `_event` baseline is proven genuinely eligible by the new control `test_complete_run_start_artifact_is_eligible`. The one collateral assertion change (`"INV-B-N-UNSET"` → `"CONF-01-QUALIFICATION"` in markdown, test_inst03_register.py:640) is honest: with the repaired bound fixture the consistency finding no longer fires, so the old substring is honestly absent; the replacement preserves equal-strength projection evidence, and it was disclosed as a deviation in the summary.
5. **Prohibition compliance.** `configs/`, `pinn/conformance/divergence_register.json`, `pinn/conformance/table.py`, `.planning/REQUIREMENTS.md`, and `.planning/STATE.md` carry zero diff lines in the review unit. No `gate_*` key is introduced (the recursive collision test stays green). `PREFLIGHT_SCHEMA_VERSION` is unchanged at 1 with the reasoning recorded. `load_preflight` normalizes `(OSError, UnicodeError)` → `ValueError` with the `FileNotFoundError` clause first (preflight.py:360-367). No N value is invented, defaulted, or proxied anywhere in the production diff; fixtures bind the owner-ratified 500, which the plan explicitly sanctions.
6. **Independent suite verification.** `.venv/bin/python -m pytest -q tests/phase49` → **190 passed in 13.52s** on the review tree, matching the summary's claim of 176 baseline + 14 new.

One Warning and two Info findings follow; none blocks the gap-closure intent.

## Warnings

### WR-01: `append_event` mutates in-memory history before the write-time ordering check can reject it

**File:** `pinn/conformance/preflight.py:345-346` (interacting with the new `_write`-time check at 309)
**Issue:** `append_event` appends to `self._events` and only then calls `_write()`. Plan 49-09 added `_assert_history_ordering(payload)` to `_write()` — the first write-time-only failure mode reachable through normal `append_event` use (single-record shape validation deliberately stays ordering-free per the plan's D-27 separation). Probe-confirmed consequence: appending a `stage_boundary` as the first event on a fresh recorder raises `ValueError` from `_write`, but the rejected record stays in `self._events` — `recorder.events` reports 1 event while no artifact exists on disk, and the recorder instance is permanently poisoned: every subsequent `append_event` re-trips ordering on the phantom first event, so the instance can never recover within that process. The class docstring contract ("Append-only assertion events persisted after every event") is silently violated in memory after a raised append. Unreachable from production today (`run_start_preflight` always writes `run_start` first, and train.py:986/1001 append stage boundaries through that same recorder), which is why this is a robustness Warning rather than Critical — but `PreflightRecorder` is a public export and the failure mode is exactly the misuse the new ordering rule exists to reject, so the rejection path should not corrupt the rejector.
**Fix:** Validate the full would-be payload before mutating state, keeping the single-record shape validation ordering-free as the plan requires:

```python
def append_event(self, *, event, stage, status, checks, census=None,
                 open_divergences=None, findings=None):
    record = { ... }
    _validate_payload({...single record...})               # unchanged: shape only
    _assert_history_ordering({"assertions": self._events + [record]})
    self._events.append(record)
    self._write()
    return record
```

This keeps `test_recorder_cannot_write_a_non_finite_value` (`recorder.events == ()`) green and extends the same never-retain-what-you-refuse discipline to the ordering rule.

## Info

### IN-01: Run-local open record carries the canonical entry's closure-language rationale verbatim

**File:** `pinn/conformance/preflight.py:521-526`
**Issue:** When the canonical `INV-B-N-UNSET` register entry is present, `_run_local_n_unset_divergence` copies `rationale` and `what_it_would_take` verbatim — and those canonical texts describe the global closure ("The owner selected N = 500 …", "Closed by the owner ruling …"). The run-local record therefore pairs `status: "open"` with rationale prose explaining why the entry is closed; the run-local explanation ("This run's own config omits …") exists only in the absent-canonical fallback path (527-546). This is the plan-sanctioned verbatim copy and the machine-readable verdict (`status`/`proof_test`/`waiver`) is correct, so eligibility logic is unaffected — but a human reading an N-unset run's `preflight.json` sees an open divergence whose prose argues for closure.
**Fix:** In a future wave, append one run-local sentence to the copied `rationale` (e.g. "Open for this run: the run's own config does not bind the window") or carry the run-local note in a dedicated field, so the human-readable caveat matches the forced-open status.

### IN-02: Fallback divergence rationale says "omits" for the malformed-window case

**File:** `pinn/conformance/preflight.py:534-539` (wording), trigger at 637-638
**Issue:** `run_start_preflight` appends the run-local record when `window is None`, which covers both the unbound case (`(None, None)`) and the malformed case (`(None, error_text)`) — plan-sanctioned ("unbound or malformed"). The locally constructed fallback rationale, however, states "This run's own config omits run.invariants.front_advance_window_n", which is inaccurate for a malformed window (the config supplied a bad value; it did not omit). No evidence is lost — the `invariant_b_window` check's `actual` carries the malformed error text (preflight.py:494) — and the case is unreachable for real configs because `InvariantsConfig` validates at construction; only duck-typed configs can produce it.
**Fix:** When `window_error` is not None, vary the rationale/what_it_would_take wording to "malformed" rather than "omits", or pass the error text into `_run_local_n_unset_divergence` for inclusion in the record.

---

_Reviewed: 2026-08-11T06:40:17Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
