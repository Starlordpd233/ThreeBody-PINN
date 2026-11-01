---
phase: 66-small-network-control
reviewed: 2026-11-01T21:08:48Z
depth: standard
files_reviewed: 13
files_reviewed_list:
  - pinn/verification/diagnostic_phase66.py
  - pinn/verification/diagnostic_power.py
  - pinn/verification/diagnostic_fit.py
  - tests/phase66/__init__.py
  - tests/phase66/test_admission.py
  - tests/phase66/test_budget.py
  - tests/phase66/test_catalog.py
  - tests/phase66/test_historical.py
  - tests/phase66/test_pages.py
  - tests/phase66/test_power.py
  - tests/phase66/test_reading_rule.py
  - tests/phase66/test_records.py
  - tests/phase66/test_tracer.py
findings:
  critical: 2
  blocker: 0
  warning: 4
  info: 4
  total: 10
status: findings
---

# Phase 66: Code Review Report

**Reviewed:** 2026-11-01T21:08:48Z
**Depth:** standard
**Files Reviewed:** 13
**Status:** findings

## Summary

Reviewed the three Phase 66 harness modules (`diagnostic_phase66.py`, `diagnostic_power.py`, `diagnostic_fit.py`) and their nine unittest suites at standard depth. The harness is frozen at commit 734cb7da, so every finding below is advisory; no file was modified.

**Verified clean** (traced, no defect found):

- **Subprocess argv and injection safety.** `pmset` is invoked with a fixed 3-element argv, no shell, `stdin=DEVNULL`, `capture_output`, and a 10 s timeout (`diagnostic_power.py:90-97`); the fit child is a fixed argv list under `caffeinate -is` with paths as separate argv elements, no shell, and `cwd` pinned to the repository root (`diagnostic_power.py:257-270`). Output/registration paths are resolved and refused outside the repo (`diagnostic_power.py:196-209`). The `git` subprocesses in `diagnostic_fit.py` use fixed argv; the one rev built by interpolation (`diagnostic_fit.py:557`) begins with a validated 40-hex commit, so it cannot be option-parsed.
- **Exclusive-receipt launch path.** `write_record_exclusive` uses `O_CREAT|O_EXCL`, raises `FirstResultExists`, creates parent directories, and fsyncs file and directory (`learnability_arms.py:435-465`); the gate's order (power, window, containment, output-exists, metadata-only admission, receipt, then child) is enforced in `launch` and the child re-checks the record and claims `attempt.json` exclusively before any data access. A partial/crashed write burns the directory rather than allowing a retry — consistent with the stated design.
- **Weekend window boundaries.** Saturday all day, Sunday strictly before 22:00 America/Chicago wall-clock (`hour < 22`), naive datetimes refused, unloadable zone refused, UTC instants converted before the check; DST is handled by construction because the check runs on Chicago local wall time. Boundary tests pin 21:59/22:00 exactly.
- **Budget arithmetic.** The exponential-then-binary search preserves the invariant `wall(low) <= target < wall(high)`, so the returned N always satisfies the 0.75-of-cap bound; `exp01_cadence` never exceeds 14 entries at any length; the record-size ceiling is genuinely N-independent (10,001-entry trace bound + 14-entry cadence bound) and therefore can refuse but never shorten a run; the "no score, similarity value or loss value in the budget output" property holds and is pinned by tests.
- **Test isolation.** The suites never touch real corpus data or weights: `subprocess` in `diagnostic_power` is replaced by a tripwire shim, pmset/window-clock/runner are injected, the data seam is patched on both harness modules, and all writes land in throwaway fixture repositories under temp directories. Real-file reads are limited to the frozen scorecard, the 33 pinned sources, and committed evidence — all read-only and by design.

**Key concerns.** The two critical findings are both in the frozen reading-rule reader: (1) the constant-predictor cross-check — the mechanism that makes a run's orbit identity verifiable — is silently skipped for any orbit key outside the two-entry `E_CONST_PREDICTED` table, so a foreign-orbit record either crashes the reader or reads as a clean branch; and (2) malformed evidence (a valid-JSON receipt that is not an object, a JSON-array record, non-dict similarity entries, mixed naive/aware timestamps) crashes the reader with unhandled exceptions and exit code 1 instead of producing the documented value-free mechanical problem and exit 2. Both were confirmed empirically with a read-only probe against the live modules. The remaining findings are audit-integrity warnings (self-declared weekday in the window audit, unaudited budget CLI, missing-attestation asymmetry) and robustness/info items.

## Critical Issues

### CR-01: E_CONST cross-check is silently skipped for orbit keys outside `E_CONST_PREDICTED`, so a foreign-orbit record reads as a clean branch (or crashes the reader)

**File:** `pinn/verification/diagnostic_phase66.py:640-651` (guard), `:728-735` (unguarded classify), `:217` (band math)

**Issue:** The module's D-10 contract is that a branch is "never read from a run that did not test the registered network on the registered orbit." The orbit half of that guarantee rests entirely on the `E_CONST_PREDICTED` lookup:

```python
predicted = (
    E_CONST_PREDICTED.get(orbit_key) if isinstance(orbit_key, str) else None
)
if predicted is not None:
    ...
```

For any orbit key not in the two-entry table, `predicted` is `None` and the entire constant-predictor cross-check — the only mechanical check that ties the record to the registered orbit's window — is skipped without flagging anything. Two manifestations, both confirmed with a read-only probe:

1. **Unsound clean reading.** A complete record for `hierarchical/gold/4658` (a structurally valid corpus orbit; `validate_smoke_settings` admits any `variant/fidelity/<int>` key) with a self-attested numeric `E_const` produces `mechanical_problems=[]` and a live branch label (`branch='near'`/`'other'`), i.e. exactly the run the rule was designed to refuse reads as clean. The single-run `read-run`/`check-run` CLIs expose this verdict directly; only `_cmd_review`'s role check catches the foreign orbit downstream.
2. **Crash.** With the comparison row missing (or non-numeric), the `e_band` computation is guarded by `isinstance(e_const, (int, float))` at line 720, but the `branch` computation at line 733 calls `classify_exp01(e, e_const, ...)` unguarded; `(1.0 - band) * None` raises `TypeError`, which escapes `main`'s `except (OSError, ValueError)` — traceback, exit 1.

Additionally, the `isinstance(e_const, (int, float))` guards that do exist admit `bool` (a `json` `true` in the score row), inconsistent with the bool-excluding check at lines 644-649; a boolean `E_const` on a foreign orbit classifies against 1.0 without complaint.

**Fix:**

```python
predicted = (
    E_CONST_PREDICTED.get(orbit_key) if isinstance(orbit_key, str) else None
)
if predicted is None:
    problems.append(_PROBLEM_ORBIT_UNREGISTERED)  # new value-free string
elif not const_ok:
    problems.append(_PROBLEM_E_CONST)
```

and mirror the `e_band` guard on the branch path:

```python
branch = (
    classify_exp01(e, e_const, tier1_max=tier1_max, still_improving=still)
    if e_is_number and isinstance(e_const, (int, float)) and not isinstance(e_const, bool)
    else None  # or keep out-of-branch via the new problem
)
```

With the new mechanical problem, a foreign-orbit record can never produce a live branch, and the crash path disappears with it.

### CR-02: Reader crashes on malformed evidence instead of recording a value-free mechanical problem; undocumented exit code 1

**File:** `pinn/verification/diagnostic_phase66.py:809-836` (receipt), `:606` (record), `:654-657`, `:659-668`, `:677-684`, `:700` (entries/access), `:925-938` (review identity), `:404-420` (budget inputs)

**Issue:** `read_run_directory`'s contract is that every failure short of a missing `record.json` becomes a value-free mechanical problem and the CLI returns 0 or 2. Multiple malformed-evidence shapes instead raise uncaught exceptions (all confirmed empirically against the live modules):

- `power-gate.json` containing valid JSON that is not an object (array, string, number): lines 809-810 explicitly classify this as `_PROBLEM_RECEIPT_UNREADABLE`, but `receipt` is then dereferenced unconditionally at line 830 (`receipt.get("checked_utc")`) because the guard is `if receipt is not None:` — `AttributeError: 'list' object has no attribute 'get'`.
- `record.json` containing a JSON array: `record.get("status")` at line 606 raises `AttributeError`.
- `similarity.entries` containing a non-dict element (line 654-657) or not being a list (line 700 `entries[-1]`): `AttributeError`/`TypeError`.
- `access.reads`/`attestation`/`opened` being a list instead of a dict (lines 663-668): `AttributeError`.
- `h1_cosine_trace`'s `int(entry.get("step"))`/`float(layer.get("adjacent_cosine_mean"))` (lines 677-684): `ValueError`/`TypeError` on string or missing values.
- `_cmd_review`'s duplicate-identity check (lines 925-938): a record with an unhashable `seed` (a JSON list) makes `identity in seen` raise `TypeError`.
- `exp01_budget` with non-dict `timing`/`similarity` blocks (lines 404-420): `AttributeError` where the docstring promises `ValueError`.

All of these escape `main`'s `except (OSError, ValueError)` handler (`diagnostic_phase66.py:1044`), producing a raw traceback and exit code 1 — breaking the documented exit-code contract for exactly the garbage-input scenario this audit reader exists to process. The authors already defend against this hazard class in one place — `improvement_check` is wrapped in `except (TypeError, ValueError)` at line 675 — which shows the intent; the same defense is missing everywhere else. Note these failures are fail-closed (no wrong branch is ever produced), but a three-run review dies entirely on one malformed directory and any automation keyed on exit codes sees 1 instead of 2.

**Fix:** Validate shapes at the entry points and convert to problems. Minimal form for the receipt bug (the only case where the code already classified the condition and then contradicted itself):

```python
        if isinstance(receipt, dict):
            ...
        elif receipt is not None:
            problems.append(_PROBLEM_RECEIPT_UNREADABLE)
            receipt = None          # <-- prevents the .get crash at line 830
```

For the rest, either coerce with explicit type checks (`isinstance(record, dict)`, `isinstance(entries, list)`, `all(isinstance(e, dict) for e in entries)`, ...), each appending the appropriate value-free problem string, or wrap the per-directory read in a helper that converts `TypeError`/`AttributeError`/`ValueError`/`ArithmeticError` into a generic `_PROBLEM_RECORD_MALFORMED` before the reading is assembled. `main`'s handler should also catch the conversion result so the CLI exits 2 with `EXP01-REFUSED`/`EXP01-CHECK-PROBLEMS` rather than a traceback.

## Warnings

### WR-01: Window audit trusts the receipt's self-declared `isoweekday` instead of deriving the weekday from `local_time`

**File:** `pinn/verification/diagnostic_phase66.py:793-808`

**Issue:** The window check validates `timezone` as a string, takes the weekday from the receipt's own `isoweekday` field, and takes only the hour from the parsed `local_time`:

```python
local = datetime.fromisoformat(str(window.get("local_time")))
weekday = window.get("isoweekday")
window_ok = (
    window.get("timezone") == _WINDOW_TIMEZONE
    and (weekday == 6 or (weekday == 7 and local.hour < _WINDOW_SUNDAY_LAST_HOUR))
)
```

Confirmed empirically: a receipt with `local_time` on a Wednesday and `isoweekday: 6` passes the audit with no window problem. `local_time` — the ground truth — is parsed and then only its hour is used; the weekday actually encoded in it is never compared to the declared `isoweekday`. A sloppy or future gate writer that sets the two fields inconsistently reads as window-compliant, and the `power-gate.json` file is not digest-protected by anything else in the directory (the attempt pins only `record.json`'s digest). Against a deliberate forger this adds little (they would write a consistent Saturday receipt), but the audit's purpose is to catch exactly the inconsistency it currently ignores.

**Fix:**

```python
window_ok = (
    window.get("timezone") == _WINDOW_TIMEZONE
    and isinstance(weekday, int) and not isinstance(weekday, bool)
    and local.isoweekday() == weekday
    and (weekday == 6 or (weekday == 7 and local.hour < _WINDOW_SUNDAY_LAST_HOUR))
)
```

### WR-02: `launch_wall_seconds` accepts naive ISO timestamps — silently wrong wall for naive pairs, unhandled `TypeError` for mixed pairs

**File:** `pinn/verification/diagnostic_phase66.py:376-383`; same defect in the late-receipt check at `:828-836`

**Issue:** The docstring promises `ValueError` "when a timestamp is missing or not ISO 8601", but a naive timestamp (no UTC offset) is valid ISO 8601 and passes. Two behaviors, both confirmed by probe:

- Both timestamps naive: `(ended - checked).total_seconds()` silently computes a wall that is wrong by the (unknown) offset — the +2 s margin does not cover a zone error.
- One naive, one aware: `checked > started` raises `TypeError: can't compare offset-naive and offset-aware datetimes`, which escapes `main`'s `except (OSError, ValueError)` in the `budget` command (traceback, exit 1) and, in `read_run_directory`'s late-receipt check (line 835), escapes the reader entirely.

The gate always writes aware `+00:00` timestamps, so the honest path is unaffected; the defect is that the auditors accept (or crash on) evidence the honest path never produces, without the promised typed refusal.

**Fix:** After each `fromisoformat`, reject naive values:

```python
def _aware(text):
    value = datetime.fromisoformat(str(text))
    if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
        raise ValueError(f"timestamp is not timezone-aware: {text!r}")
    return value
```

Use it in `launch_wall_seconds` and in the late-receipt check; both then raise the documented `ValueError`/append `_PROBLEM_RECEIPT_LATE` as designed.

### WR-03: `budget` CLI computes from an unaudited timing directory

**File:** `pinn/verification/diagnostic_phase66.py:891-906`

**Issue:** `_cmd_budget` reads `record.json`, `power-gate.json` and `attempt.json` with bare `json.loads` and computes the wall, applying none of the admission checks that `read_run_directory` enforces for the same three files: receipt schema, AC-power source, weekend window, attempt `published` status, `record_sha256` digest, receipt-not-after-attempt. A timing directory that would read `out-of-branch` (battery receipt, unpublished attempt, digest mismatch — i.e., not the gate's output at all) still yields a budget, and every number the budget produces flows into the committed experiment registrations and pages. The committed evidence is digest-pinned by `test_pages.py` today, which contains the damage, but the CLI's own contract ("the timing directory's budget") is that it sizes the gate's timing run, and it does not verify that.

**Fix:** Either run the same receipt/attempt checks (they are value-free and cheap) before computing the wall, or state in the docstring/help that `budget` trusts the directory and must only be pointed at digest-pinned evidence.

### WR-04: A record with a missing or null access attestation reads clean, while `verify_fit_result` refuses the same record

**File:** `pinn/verification/diagnostic_phase66.py:659-670`; contrast `pinn/verification/diagnostic_fit.py:1503`

**Issue:** The split-open audit sums `validation`/`test`/`test_split_opened` over `reads`, `attestation` and `attestation.opened`, but a record whose `access.attestation` is `null` (or absent) contributes nothing and passes with no problem. `fit_diagnostic` itself can publish `attestation: null` (`diagnostic_fit.py:1073-1075`, when `context.attestation is None`), and `verify_fit_result` explicitly refuses such a record ("the result carries no access attestation", line 1503). The reading rule is therefore strictly weaker than the verifier on the same evidence: missing attestation is fail-open at the point where a branch label is read. Fail-closed auditing should treat missing evidence as a problem, not as absence of wrongdoing.

**Fix:** In `read_exp01_record`, append a value-free problem (e.g. `"the record carries no access attestation"`) when `attestation` is not a dict, mirroring `verify_fit_result`'s requirement.

## Info

### IN-01: Gate-side exception boundary covers only `PowerRefused`/`FirstResultExists`; other failure modes exit 1 with a traceback

**File:** `pinn/verification/diagnostic_power.py:249-251`, `:114-127`, `:150-154`

**Issue:** `launch`'s `except (PowerRefused, FirstResultExists)` does not cover `OSError` from `write_record_exclusive` (e.g. disk-full mid-write, which also leaves a truncated receipt that then burns the directory for the next launch) — the contract "any refusal before step 8 prints POWER-REFUSED ... returns 2" is broken in that case. Likewise `require_ac_power` crashes with `AttributeError` if an injected reader returns a non-string (its contract says any reader failure raises `PowerRefused`), and `require_weekend_window` crashes on a non-datetime clock return. All production paths return correct types, so these are robustness-only.

**Fix:** Add `OSError` to `launch`'s except tuple; in `require_ac_power`, move the `power_source(text)` call inside the guarded region (or type-check `text`); in `require_weekend_window`, wrap `now()` in the existing fail-closed `try`.

### IN-02: Window semantics duplicated between the gate and the auditor

**File:** `pinn/verification/diagnostic_power.py:65-70, 157` and `pinn/verification/diagnostic_phase66.py:584-586, 797-804`

**Issue:** The window definition — `America/Chicago`, the Sunday last hour 22, the Saturday/Sunday predicate — is implemented twice: once in `diagnostic_power` (the gate) and again, independently, in `diagnostic_phase66` (the auditor, which also re-declares the receipt schema as `_RECEIPT_SCHEMA`). The two must agree for the audit to be meaningful; a future edit to one (e.g. moving the Sunday boundary) silently desynchronizes gate and auditor, and the catalog test that forbids harness imports from `diagnostic_phase66` prevents the obvious shared-constant fix from being expressed as an import.

**Fix:** At minimum, add a test asserting the two modules' window constants and predicates agree (e.g. `diagnostic_phase66._WINDOW_TIMEZONE == diagnostic_power.WINDOW_TIMEZONE` and the boundary hours match), so drift fails loudly instead of silently.

### IN-03: `exp01_loss_trace_stride(0)` returns 0

**File:** `pinn/verification/diagnostic_phase66.py:348-351`

**Issue:** For `n = 0` the ceil formula yields stride `0`, which would `ZeroDivisionError` in `loss_trace_entries` and violates `validate_smoke_settings`' "integer from 1 to optimizer_steps" contract if ever fed downstream. Unreachable through the budget path (steps are positive multiples of `step_quantum`), but the function is public and unguarded.

**Fix:** Raise `ValueError` for `n < 1`, matching the budget function's refusal style.

### IN-04: `exp01_budget` never cross-checks the timing record's warmup against the rule's `warmup_steps`

**File:** `pinn/verification/diagnostic_phase66.py:424-446`

**Issue:** `fixed_wall` subtracts the record's own `warmup_seconds` and `projected_wall` adds it back while subtracting the rule's `warmup_steps` (200) from `steps`. This bookkeeping is only coherent when the timing run's warmup step count equals `rule["warmup_steps"]`; nothing verifies `timing_record["steps"]["warmup"] == rule["warmup_steps"]`. A future timing run with a different warmup would silently mis-project (today the mismatch is small and the committed evidence pins 200, so this is latent).

**Fix:** Add `if int((timing_record.get("steps") or {}).get("warmup", -1)) != warmup_steps: raise ValueError(...)` alongside the existing record-completeness checks.

---

_No source files were modified. Findings are advisory: the diagnostic harness is frozen at commit 734cb7da (user directive); the two critical findings and the warnings concern the frozen readers and are recorded for the owner to triage, not for in-place fixes._

_Empirical basis: every crash/audit-gap claim in CR-01, CR-02, WR-01 and WR-02 was reproduced against the live modules with a read-only probe (temp-directory fixtures only; probe scripts deleted after use)._

_Reviewed: 2026-11-01T21:08:48Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
