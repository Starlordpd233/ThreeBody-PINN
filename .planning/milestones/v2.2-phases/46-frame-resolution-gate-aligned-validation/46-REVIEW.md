---
phase: 46-frame-resolution-gate-aligned-validation
reviewed: 2026-07-30T03:43:53Z
depth: standard
files_reviewed: 13
files_reviewed_list:
  - pinn/data/adapter.py
  - pinn/data/preprocessing.py
  - pinn/train.py
  - pinn/training/summary.py
  - pinn/training/validation_gate.py
  - pinn/verification/target_frame_probe.py
  - tests/phase39/test_prohibitions.py
  - tests/phase43/test_summary_enrichment.py
  - tests/phase46/test_artifacts.py
  - tests/phase46/test_frame_probe_evidence.py
  - tests/phase46/test_isolation.py
  - tests/phase46/test_pairing_repair.py
  - tests/phase46/test_validation_wiring.py
findings:
  critical: 0
  warning: 1
  warning_resolved: 1
  info: 1
  total: 2
  deferred: 2
status: clean
resolved_in_run:
  - id: WR-46-10-01
    commit: bbc398b
---

# Phase 46: Code Review Report

**Reviewed:** 2026-07-30T03:43:53Z
**Depth:** standard
**Files Reviewed:** 13
**Status:** issues_found

## Summary

This is the `execute:post` re-review after plan 46-10 (commits `ad5331cd`,
`35c88d7f`) landed on top of the 2026-07-29T13:05:37Z review (preserved at git
commit `38add1d2`). Plan 46-10 touched exactly five files —
`pinn/training/validation_gate.py`, `pinn/train.py`,
`pinn/training/summary.py`, `tests/phase46/test_artifacts.py`,
`tests/phase46/test_validation_wiring.py` — and rewrote the EVAL-01
eligibility/sidecar-validation logic the prior review found four blockers and
one warning in.

I re-derived every prior finding from the diff, the current source, the
mutation-style test suite, and — because the prior review explicitly warned
that a green suite is not evidence of correctness — three independent
adversarial reproductions run directly against the fixed code (not just the
shipped tests): the exact CR-03 donor-path-traversal repro, a same-step
forged-donor-sidecar repro, and a corrupted-encoding repro against the new
`_read_latest_validation_event`. All findings below reflect that direct
verification, not test-suite trust.

**Verdict: CR-03, CR-04, CR-05, and WR-01 are genuinely CLOSED.** The rewrite
is a real fail-closed identity-binding and semantic-validation layer, not a
cosmetic patch. CR-01 and CR-02 are **DEFERRED-BY-OWNER** per the CONF-09
routing to Phase 47 (GAP-46-07, `RESOLVED-WITH-INSTRUCTION`, 2026-07-28) and
are reported here for completeness only — they do not block Phase 46 and are
excluded from the finding counts that drive `status`.

Adversarially, this pass surfaced one new, reproducible WARNING in code this
plan touched: `_read_latest_validation_event`'s `except OSError` around
`Path.read_text(encoding="utf-8")` does not catch `UnicodeDecodeError` (a
`ValueError` subclass), so a validation.jsonl file containing invalid UTF-8
bytes crashes the summary render instead of degrading to the documented
"present-but-invalid" state — undermining the module's own stated "presence
under every death mode" contract. It is a narrow, low-probability trigger
(the writer only ever emits pure-ASCII JSON) and it is an *inherited* pattern
(the pre-46-10 `_read_jsonl_mappings` had the identical gap), so it is
reported as a WARNING, not a blocker, but it sits in code this plan rewrote
and is one line to fix.

## Adjudication of Prior Findings

### CR-01 [BLOCKER, prior] — Resident targets and IC13 encode different coordinate frames — **DEFERRED (owner ruling, not a Phase 46 blocker)**

`pinn/data/adapter.py` and `pinn/data/preprocessing.py` are **byte-for-byte
unchanged** between `0355cbbc` and `HEAD` (`git diff 0355cbbc..HEAD --stat --
pinn/data/adapter.py pinn/data/preprocessing.py` is empty), so the finding's
original file:line evidence (`adapter.py:861-872`, `preprocessing.py:68-74`)
still describes the code exactly. This is the CONF-09 canonical-training-frame
defect. GAP-46-07 (`.planning/phases/46-frame-resolution-gate-aligned-validation/46-GAPS.md:882-1124`)
records **owner ruling 2026-07-28, option A**: complete the residency
transform (`r_com_ordered`/`v_com_ordered` → `r_gauge`/`v_gauge`, re-ratify
`RATIFIED_VALIDATION_FRAME` to the scaled pair) as new requirement **CONF-09**,
sequenced in **Phase 47 ahead of CONF-02**. The resolution note is explicit:
*"Phase 46 verification and closure were never blocked by this gap; its three
requirements' evidence stands as recorded."* Per the task's owner ruling, this
is reported as deferred and is **not** re-litigated or re-proposed here.

### CR-02 [BLOCKER, prior] — Post-repair probe has no identity class for the repaired resident frame — **DEFERRED (owner ruling, not a Phase 46 blocker)**

`pinn/verification/target_frame_probe.py` is likewise byte-for-byte unchanged
(`target_frame_probe.py:632-695` and the rule-5 emission at `887-894` are
unmodified). GAP-46-07's same option-A ruling covers this: the same residency
completion that resolves CR-01 also gives the probe a reachable
ordered-COM/raw identity class; until CONF-09 lands in Phase 47, the
post-repair verdict `VERDICT_NON_FRAME_DIVERGENCE` recorded in
`46-VERDICT-POSTREPAIR.md` stands as the grounded, owner-accepted rule-5
result for the *current* (raw/native) `RATIFIED_VALIDATION_FRAME` — which is
itself the deliberately-scoped GAP-46-06 ratification, not an oversight.
Deferred to Phase 47; not a Phase 46 blocker.

### CR-03 [BLOCKER, prior] — EVAL-01 eligibility trusts arbitrary sidecar paths, never binds record to artifact — **CLOSED**

Closed by `compact_validation_fields_from_payload` (`pinn/training/validation_gate.py:691-722`),
whose three keyword parameters `expected_run_dir_name` / `expected_global_step`
/ `expected_sidecar_path` have **no defaults** — Python raises `TypeError` if a
caller omits any of them — and whose sole production callers
(`compact_validation_fields`, `pinn/training/validation_gate.py:725-762`, and
`summary._eval01_precondition_iii`, `pinn/training/summary.py:246-305`) always
supply all three, derived from the call's own context (the run directory's
own name, the record's own claimed step, and the step-derived canonical path)
— never from attacker-controlled payload content. `validate_sidecar_payload`
(`pinn/training/validation_gate.py:669-686`) then rejects any payload whose
`run_dir`/`global_step`/`sidecar_path` disagrees with those bindings.
Containment is proved via `Path.resolve()` + `relative_to()`
(`validation_gate.py:741-747`, `summary.py:287-289`), which is
symlink-and-`../`-safe (not a string-prefix check).

I independently reproduced both exploits from the prior report against the
current code (script run in-session, not committed):
- The exact CR-03 repro (a step-999 record whose `gate_sidecar` points via
  `../donor/...` at a real donor sidecar in a different run directory) →
  `_eval01_precondition_iii` returns `False`.
- A same-step forged-donor variant (donor sidecar copied to the victim run's
  *own* canonical `step-00000999.json` path, so the filename-derived check
  aligns) → also `False`, because the copied payload's internal `run_dir` and
  `sidecar_path` fields still name the donor run, and
  `expected_run_dir_name`/`expected_sidecar_path` reject the mismatch.

Test evidence: `tests/phase46/test_artifacts.py` `IdentityBindingTests` and
`PayloadDerivedCompactFieldsTests`; `tests/phase46/test_validation_wiring.py`
`Eval01IdentityBindingTests` (`test_cross_run_traversal_pointer_rejected`,
`test_wrong_step_pointer_with_renamed_donor_sidecar_rejected`,
`test_one_at_a_time_gate_field_mismatch_rejected`). All pass; all raise/return
`False` on the tampered path, not merely "don't crash."

### CR-04 [BLOCKER, prior] — Fail-closed sidecar validator accepts semantically invalid gate records — **CLOSED**

`validate_sidecar_payload` (`pinn/training/validation_gate.py:541-688`) now
enforces the full v1 semantic contract: exact top/frame/row/record_key key
sets via `_require_exact_keys` (missing *and* unknown keys both reject);
`split == "validation"` and `gate_status == "ok"` exact-string checks;
non-negative strict-integral `global_step`/`stage`/`n_trajectories`/
`n_nonfinite`/record-key `id` via `_strict_nonnegative_integral` /
`_is_strict_nonnegative_json_int` (bool explicitly excluded at every one of
these sites); canonical (non-tamperable) reject thresholds via
`_validate_canonical_threshold`; unique, strictly-increasing record-key
triples (`triples[i] < triples[i+1]`, which proves both uniqueness and
order in one comparison); and — the core of the fix — every per-row `scs`,
`n_nonfinite`, `aggregate_eps_h`, `aggregate_scs`, and `verdict` is
**recomputed from `gate_metrics`** and compared bit-exact
(`_metrics_equal`/`_json_scalar_equal`-equivalent logic) against the
persisted value, so a payload can never advertise a value inconsistent with
its own rows.

I confirmed the prior report's exact repro values are individually rejected
by reading `test_cr04_repro_split_status_step_stage_frame_all_individually_rejected`
(`tests/phase46/test_artifacts.py:541-556`), which tests `frame={}`,
`split="test"`, `gate_status="failed"`, `global_step=-99`, `stage=-3` each in
isolation, and traced each through `validate_sidecar_payload` by hand to
confirm the specific check that fires (split/gate_status exact-string checks
fire before the frame/step checks are ever reached for those two fields;
`_strict_nonnegative_integral` fires for the negative step/stage; `_validate_frame`
fires for the empty frame dict). Ran the full `SemanticInvariantTests` class
(17 tests) — all pass, including bool-alias, duplicate-key, wrong-threshold,
wrong-scs, wrong-aggregate, and wrong-verdict mutation tests.

### CR-05 [BLOCKER, prior] — Later validation failures hidden behind a stale eligible record — **CLOSED**

Two independent defects are both fixed:

1. **The early-return-without-append bug.** `_append_validation_record`
   (`pinn/train.py:75-119`) no longer returns before appending on a
   non-finite `final_val_loss`; the removed branch (`if not
   math.isfinite(value): return value`) is gone (confirmed in the diff,
   `pinn/train.py` diff hunk at the old lines 92-98), and every call now
   reaches the single `path.open("a").write(...)` at the end of the
   function, encoding non-finite values as `json_safe_float` sentinels
   (`"NaN"`/`"Infinity"`/`"-Infinity"`) so `allow_nan=False` never raises.
2. **The stale-fallback JSONL reader.** `_read_jsonl_mappings` (which
   silently skipped malformed lines and let `_validation_summary` select an
   older valid record) is replaced by `_read_latest_validation_event`
   (`pinn/training/summary.py:192-230`), which reads only the **physical**
   last `splitlines()` entry and, if it is blank, malformed JSON, torn, or a
   non-mapping, returns `(True, None)` — the caller then renders the
   documented all-null / `eval01_precondition_iii=False` block rather than
   falling back to an older record. `_validation_summary`
   (`summary.py:308-342`) never iterates past the latest line.

Confirmed via `tests/phase46/test_validation_wiring.py`
`LatestEventMonotonicityTests` (torn line, non-mapping line, blank-only line,
a later `"failed:..."` gate event, and a later gate-`"ok"`-but-nonfinite-loss
event — all six scenarios assert the *latest* step is reported and
`eval01_precondition_iii` is `False`), and by direct execution
(`Ran 150 tests ... OK`, conda env `pinn-train`, 2026-07-30).

### WR-01 [WARNING, prior] — Fractional and string steps silently coerced into artifact-name collisions — **CLOSED**

`_strict_nonnegative_integral` (`pinn/training/validation_gate.py:320-335`)
requires `numbers.Integral` with `bool` explicitly excluded, and rejects
before any `int()` conversion. `sidecar_relative_path` (`:338-349`) is its
only production caller for step→filename mapping, and I traced every other
`int(...)` conversion of a step/global_step in the file
(`_observation_payload:365-366`, `compute_validation_gate:279-280`) back to a
value that was already produced by `int(global_step)` inside
`compute_validation_gate` itself (never a raw external value re-parsed).
`pinn/train.py:93` (`_append_validation_record`) now calls
`validation_gate.sidecar_relative_path(step)` for its "strict identity check
only" side effect **before** any record field is built, closing the
train.py-side gap the prior WR-01 was actually about. Confirmed via
`StrictStepIdentityTests` (`test_artifacts.py:470-487`, bool/float/string/
negative all raise) and `test_hostile_step_rejected_before_any_write`
(`test_validation_wiring.py:223-231`, asserts the JSONL file is never created).

## Warnings

### WR-46-10-01: `_read_latest_validation_event` does not catch `UnicodeDecodeError`, risking an uncaught crash of the "every death mode" summary writer

**File:** `pinn/training/summary.py:210-215` (also present in the sibling
readers `_read_json_mapping:181-189` and `_render_curriculum:152-178`, all in
the same file, pre-existing pattern)

**Issue:** `_read_latest_validation_event` wraps `Path(path).read_text(encoding="utf-8")`
in `try: ... except OSError: return False, None`. `UnicodeDecodeError` is a
subclass of `ValueError`, not `OSError`, so it is **not** caught. I
reproduced this directly (script, not committed):

```
$ python - <<'EOF'
# validation.jsonl: one valid line, then a line with invalid UTF-8 bytes
with open(p, "wb") as f:
    f.write(b'{"step": 7, "final_val_loss": 1.0, "trend": "improving"}\n')
    f.write(b'\xff\xfe\x00bad-bytes-not-utf8\n')
summary_mod._read_latest_validation_event(p)
EOF
EXCEPTION RAISED: UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 57: invalid start byte
```

This exception is uncaught all the way up the call chain:
`_validation_summary` → `_compose` → `finalize_summary`/`stub_summary`, and
`pinn/train.py`'s `finish_run` (`pinn/train.py:704-732`) wraps the
`finalize_summary` call in a bare `try/finally` with **no `except`**, so the
exception propagates out of `finish_run` and out of `main()` — i.e. the exact
death mode this module's docstring says it must survive ("Presence is thereby
guaranteed under every death mode including SIGKILL — a write-at-exit-only
design cannot satisfy E4's presence invariant") is not actually survived if
`validation.jsonl`'s tail is ever non-UTF-8.

The practical trigger is narrow: `_append_validation_record` always writes via
`json.dumps(..., allow_nan=False)` with the default `ensure_ascii=True`, so
the trusted writer can only ever produce pure-ASCII bytes, and any truncation
of pure ASCII is still valid UTF-8. A genuinely non-UTF-8 tail requires
external corruption (disk error, a future non-ASCII-emitting writer, or
direct tampering) — but the CR-05 threat model this exact function was
rewritten to close is precisely "the file can be corrupted/torn," and this is
one corruption mode the rewrite didn't cover. It is inherited from the
pre-46-10 `_read_jsonl_mappings` (identical `except OSError` gap), so it is
not a regression introduced by 46-10, but it lives in the function this plan
rewrote to make CR-05's fail-closed guarantee, so I am flagging it here rather
than silently carrying it forward.

**Fix:** Broaden the catch to include the decode failure, degrading to the
already-designed "present but invalid" state instead of raising:

```python
try:
    text = Path(path).read_text(encoding="utf-8")
except (OSError, UnicodeDecodeError):
    return False, None
```

(Note: this specific fallback returns `(False, None)` — "missing" — which is
slightly less precise than the "present but invalid" `(True, None)` state the
rest of the function uses for a readable-but-malformed latest line; consider
reading bytes and decoding with `errors="replace"` or explicitly returning
`(True, None)` for a decode failure so it renders identically to a torn/
malformed line rather than a missing file. Either resolution restores fail-closed
behavior; the current uncaught-exception state does not.) The same broadening
should be applied to `_read_json_mapping` and `_render_curriculum` for
consistency, though those are out of this plan's specific CR-05 mandate.

**Status: RESOLVED** — fixed in commit `bbc398b` during the same execute-phase
run that produced this report. The orchestrator independently reproduced the
uncaught `UnicodeDecodeError` and confirmed `finish_run`'s bare `try/finally`
(`pinn/train.py:710-726`) lets it escape with no `summary.json` written.

Applied the more precise of the two options this finding offered: a dedicated
`except UnicodeDecodeError: return True, None` branch, so undecodable bytes
render identically to a torn JSON line (present-but-invalid, 12-key block,
`eval01_precondition_iii` false) rather than masquerading as a missing stream.
Decoding with `errors="replace"` was rejected — it would let a torn line
silently become parseable-looking text, which is the opposite of fail-closed.

Regression `LatestEventMonotonicityTests::test_valid_event_followed_by_undecodable_bytes_never_falls_back`
was verified red-then-green (raises `UnicodeDecodeError` with the branch
removed, passes with it restored), so it is not an inert check.
`tests/phase46/` 151 passed; `tests/phase43/test_summary_enrichment.py` 5 passed.

The sibling `_read_json_mapping` / `_render_curriculum` readers were left
untouched: same pattern, but pre-existing and outside this plan's declared
files and CR-05 mandate. Carried forward as known debt, not silently fixed.

## Info

### IN-46-10-01: Duplicated, narrower-than-necessary integer/float validation in `summary._eval01_precondition_iii` instead of reusing `validation_gate`'s shared check

**File:** `pinn/training/summary.py:270-278`

**Issue:** `_eval01_precondition_iii` re-implements ad hoc type checks —
`isinstance(final_val_loss, bool) or not isinstance(final_val_loss, (int, float))`
and `isinstance(step, bool) or not isinstance(step, int) or step < 0` — that
duplicate, in narrower form, `validation_gate._strict_nonnegative_integral`'s
`numbers.Integral`-based check. This is not a bug for the current call site
(`record` always comes from `json.loads`, which only ever produces `int`,
never a `numpy` integer or other `numbers.Integral` subtype, so the narrower
`isinstance(step, int)` check is behaviorally equivalent here), but it is
duplicated logic that could silently diverge from the canonical helper if
either is edited independently, and `numbers` is stdlib (no torch
dependency), so summary.py could import it at module level without breaking
the "stdlib-only honesty layer" contract this file documents for itself.

**Fix:** Either import `numbers` in `summary.py` and reuse the same
`isinstance(x, bool) or not isinstance(x, numbers.Integral)` predicate as a
small shared stdlib-only helper, or leave as-is with a comment noting the
narrower check is intentionally JSON-domain-scoped (only `int`/`float`/`bool`
are reachable from `json.loads`). Low priority; noted for maintainability
only.

---

## Test State (independently verified this session)

- `tests/phase46/`: ran `python -m unittest discover -s tests/phase46 -p
  "test_*.py"` in the `pinn-train` conda env → **150 passed, 0 failed** —
  matches the orchestrator's independent count (up from 114 pre-46-10).
- `tests/phase39/test_prohibitions.py` + `tests/phase43/test_summary_enrichment.py`
  (both in this review's file scope but untouched by 46-10): ran directly →
  **36 passed, 0 failed** — no regression from the `summary.py` rewrite.
- `tests/phase43/`'s other 12 pre-existing failures (`pilot_calibration` x2,
  `smoke` x1, `verdict_grounding` x7, `verify_gate` x2) were not re-run in
  full here; per the task's environment note these are pre-existing and
  environmental, unrelated to this diff, and are not re-litigated.
- Test-suite quality: `test_artifacts.py`'s `SchemaFailClosedTests` and
  `SemanticInvariantTests` and `test_validation_wiring.py`'s
  `Eval01IdentityBindingTests`/`LatestEventMonotonicityTests` are genuine
  mutation tests — each mutates exactly one field on an otherwise-valid,
  freshly-published real payload/record and asserts the specific violation is
  caught; none of them would pass against a reverted (pre-46-10)
  implementation, and I confirmed this by hand-tracing three of them against
  the pre-46-10 code shape rather than only reading the assertions. No
  "checks that cannot fail" were found in the 46-10 diff. `test_isolation.py`
  (unchanged by 46-10) still performs genuine AST-scan-plus-fresh-subprocess
  enforcement of the D-16 evaluator-import ban, not a vacuous check.

---

_Reviewed: 2026-07-30T03:43:53Z_
_Reviewer: the agent (gsd-code-reviewer)_
_Depth: standard_
