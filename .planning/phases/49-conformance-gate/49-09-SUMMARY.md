---
phase: 49-conformance-gate
plan: 09
subsystem: conformance
tags: [summary, conformance, gap-closure, preflight, eval01, invariant-b]

requires:
  - phase: 49-conformance-gate
    provides: "Plans 49-01..49-08: the conformance gate — PHYS-05 table, census, divergence register, runtime guards, preflight evidence spine, summary projection"
provides:
  - "Run-local invariant-B window binding through the single _extract_invariant_window accessor (preflight.py:384 anti-pattern closed at its root)"
  - "The affirmative advisory invariant_b_window run-start check (D-16: affirmative evidence, not absence of a negative)"
  - "The run-local open INV-B-N-UNSET divergence projection, computed per run from that run's own config (D-20)"
  - "History-ordering enforcement at load AND write: an assertion history must begin with run_start"
  - "REQUIRED_RUN_START_CHECKS and the single evaluate_eval01_precondition_i predicate behind the pinn/conformance module boundary (D-32)"
  - "WR-02 read-error normalization: OSError/UnicodeError convert to ValueError in load_preflight"
affects: [phase-50-valid-stage0-rerun, phase-51-authorized-evaluation]

actuals:
  tokens: 16630
  tasks: 3
  commits: 1

key-files:
  created:
    - .planning/phases/49-conformance-gate/49-09-SUMMARY.md
  modified:
    - pinn/conformance/preflight.py
    - pinn/training/summary.py
    - tests/phase49/test_e2e_seam.py
    - tests/phase49/test_gate03_invariants.py
    - tests/phase49/test_inst03_register.py
    - tests/phase49/test_preflight_integrity.py
    - .planning/ROADMAP.md

key-decisions:
  - "Conformance is per run: the committed INV-B-N-UNSET register entry stays globally closed (the owner ruling of 2026-08-05) while each run's own config decides whether that run carries the divergence open — the 49-VERIFICATION-endorsed reconciliation of D-19 and D-20."
  - "Only the ORDERING rule is enforced at load; required-evidence rules live in the eligibility predicate. A refused run's incomplete run_start evidence must still LOAD because the artifact IS the caveat record (D-27)."
  - "The invariant_b_window check is advisory, not locked: _assert_status_consistency refuses a passed event carrying a failed LOCKED check, and D-20 requires an N-unset run to remain runnable and leave a passed run-start record."
  - "PREFLIGHT_SCHEMA_VERSION stays 1: the payload shape is unchanged — only its semantic validation and its consumer's requirements tightened — and no persisted real-corpus artifact exists to distinguish the two regimes (D-29)."
  - "Stale eligibility fixtures were repaired by binding the owner-ratified N = 500 — never by relaxing the predicate, the register filter, or the gate (the 49-07 CR-10 lesson)."

requirements-completed: []

duration: 29min
completed: 2026-08-11
status: complete
---

# Phase 49 Plan 09: Gap-Closure Summary — Run-Local Invariant-B Window Bound to the EVAL-01 Gate

**Both `49-VERIFICATION.md` blocking gaps are closed at their shared seam: an
N-unset run is now structurally ineligible (its own run record carries an open
run-local `INV-B-N-UNSET` divergence and a failed affirmative
`invariant_b_window` check), and `eval01_precondition_i` is true only when the
artifact PROVES the run-start table assertion, the passed census, and the
run-local window binding all actually happened.**

`requirements-completed` is deliberately empty: this plan does NOT certify the
gaps closed. `/gsd-verify-work` re-verification owns that adjudication, and
requirement status in `.planning/REQUIREMENTS.md` is therefore left unchanged.
Self-certifying the gaps closed is exactly the failure mode this remediation
exists to correct.

## GAP A (GATE-03, truth 3) — run-local N binding

**Gap.** A real `main()` run with `run.invariants = {}` exited 0, ran invariant
B record-only, reported `INV-B-N-UNSET open=False`, and still emitted
`eval01_precondition_i=True`. The divergence lived GLOBALLY in
`divergence_register.json` — where the owner's 2026-08-05 ruling (D-19, N = 500)
correctly closed it — while enforcement is configured PER RUN. The same root
cause produced the verifier's `preflight.py:384` anti-pattern:
`_consistency_finding` read `config.invariants` instead of
`config.run.invariants`, so even the shipped N = 500 config reported
`config_value: None`.

**Fix.**

1. **One reader for N.** `_run_local_invariant_window(config)` delegates to
   `_extract_invariant_window` imported from `pinn.training.guards` — the ONE
   accessor — and converts its `ValueError` into a non-null `error_text` so a
   malformed or duck-typed config stays fail-closed evidence. Import-cycle
   safety verified directly: `guards.py` imports only
   `pinn.training.atomic_io` and `pinn.training.stage_exit`, neither of which
   imports `pinn.conformance`. `_consistency_finding` now resolves the window
   through this helper; its `config_value` is the resolved run-local window.
2. **Affirmative evidence (D-16).** `INVARIANT_B_WINDOW_CHECK_NAME` plus
   `_invariant_b_window_check(window, error_text)` build the five-key advisory
   check: `passed` is true only when a window is bound and no error text was
   produced. Advisory, not locked, so an N-unset run still leaves a `passed`
   run-start record (D-20) without tripping `_assert_status_consistency`. The
   check is inserted immediately after `checks = list(result["checks"])` and
   BEFORE the census append in BOTH the passing and census-failure branches, so
   `checks[-1]["name"] == "census"` stays true (three existing refusal tests
   assert that terminal position — see the sentinel inventory below).
3. **Run-local divergence (D-20).** `INV_B_N_UNSET_ID` plus
   `_run_local_n_unset_divergence(register_payload)` copy the canonical
   entry's `id`/`kind`/`title`/`spec_citation`/`authority`/`rationale`/
   `what_it_would_take` verbatim with `status` forced to `open`, `proof_test`
   null (the closure proof does not hold for a run that omits the window), and
   `waiver` null. When the canonical entry is absent, the same ten-key record
   is constructed locally with literal text naming D-20 as the source.
   `run_start_preflight` computes the window once, immediately after
   `open_entries` is built from the register and BEFORE the table assertion,
   and appends the run-local record there — so table-failure, census-failure,
   and success branches all carry the caveat.
4. **One predicate, behind the module boundary (D-32).**
   `evaluate_eval01_precondition_i(payload)` in `pinn/conformance/preflight.py`
   is the single eligibility predicate; `summary.py::_eval01_precondition_i`
   now only null-checks the path, then loads fail-closed and delegates inside
   its existing broad boundary. The divergence-vs-qualification filter
   rationale moved onto the predicate verbatim (D-23/D-26: open qualifications
   keep travelling without stranding a run).

**RED evidence (observed against the pre-fix tree, baseline 176 passed in
13.27s):**

- `test_real_main_with_n_unset_is_structurally_ineligible` (the verifier's
  N-unset real-main heredoc probe promoted to a named case): FAILED with
  `assert 0 == 1` at `len(run_local) == 1` — the run-local `INV-B-N-UNSET`
  record was absent. The earlier assertions in the same test (exit code 0,
  `run_start` status `passed`, census verdict `passed`) all held, so the ONLY
  missing piece was the run-local record and the flag — exactly the plan's
  recorded reason ("the run-local record is absent and the flag is True").
- `test_consistency_finding_reads_run_scoped_window_from_real_config`: FAILED
  with `assert None is not None` — no consistency finding could fire because
  the accessor read the wrong path and the owner-ratified 500 read as unset.
- `test_preflight_appends_run_local_n_unset_divergence_when_window_absent`:
  FAILED on the exact-equality assertion — no run-local record was appended.
- `test_preflight_omits_run_local_divergence_when_window_is_bound`: FAILED with
  `assert 0 == 1` — no `invariant_b_window` check existed.
- `test_missing_canonical_register_entry_still_yields_open_run_local_divergence`:
  FAILED with `assert 0 == 1` — no run-local record existed.

**GREEN evidence:** `.venv/bin/python -m pytest -q
tests/phase49/test_e2e_seam.py tests/phase49/test_inst03_register.py
tests/phase49/test_gate03_invariants.py` → **86 passed in 11.71s**. The
GAP-A probe now observes: exit 0, exactly one open `INV-B-N-UNSET` divergence
record in the run-start event, `summary["eval01_precondition_i"] is False`.

## GAP B (truth 6) — eligibility requires the evidence it summarizes

**Gap.** A schema-valid, `passed`, `stage_boundary`-only artifact with
`census=null` loaded successfully and `_eval01_precondition_i` returned `True`.
The predicate trusted the SHAPE of the assertion list without proving it
contains the mandatory run-start table assertion and census event.

**Fix.**

1. **Loader/predicate separation (the load-bearing design call, D-27).** Only
   the ORDERING rule is enforced at load: `_assert_history_ordering` refuses a
   non-empty history whose first event is not `run_start`, called from
   `load_preflight` AND `PreflightRecorder._write` (the same second-belt
   discipline the `allow_nan=False` writer comment records — the codebase can
   neither CREATE nor READ a hollow history). It is deliberately NOT called
   from `append_event`'s single-record shape validation, which validates one
   `stage_boundary` record in isolation. Required-evidence rules live in the
   predicate, so a refused run's incomplete `run_start` evidence still LOADS —
   the artifact IS the caveat record. Append-only resume histories
   (`run_start`, `stage_boundary`, …, `run_start`, …) stay legal (D-17/CR-06).
2. **WR-02 read-error normalization.** `load_preflight` gains an
   `(OSError, UnicodeError)` clause AFTER the existing `FileNotFoundError`
   clause (order matters — `FileNotFoundError` is an `OSError` subclass and
   its more specific message must win), mirroring the wording already used in
   `_metadata_for_census`. No native I/O exception escapes the fail-closed
   loader.
3. **Required run-start evidence.** `REQUIRED_RUN_START_CHECKS` =
   `("lambda_phys_max", "lambda_e_max", "lambda_l_max", "warmup_length",
   "lambda_data", "census", "invariant_b_window")`. The predicate additionally
   requires: the first event is a `run_start`; at least one `run_start`
   exists; for EVERY `run_start` event, each required name appears at least
   once and EVERY occurrence carries `passed` true; and the event's `census`
   is a mapping whose `verdict` compares exactly equal to `"passed"`. Anything
   unrecognized, absent, null, or non-mapping denies eligibility.

**RED evidence (observed against the post-Task-1, pre-GAP-B-fix tree):**

- `test_stage_boundary_only_history_is_refused_at_load` (the verifier's second
  heredoc probe promoted to a named case): FAILED with
  `Failed: DID NOT RAISE ValueError` — the artifact loaded, and the predicate
  returned true. Exactly the plan's recorded reason.
- `test_run_start_missing_required_check_is_not_eligible`: FAILED — the
  predicate returned `True` for a run_start missing one required check.
- `test_run_start_with_null_census_is_not_eligible`: FAILED with
  `assert True is False` — a null census still reported eligible.
- `test_run_start_with_blocked_census_verdict_is_not_eligible`: FAILED — a
  `blocked` verdict still reported eligible.
- `test_unreadable_preflight_artifact_raises_value_error`: FAILED with
  `AssertionError: Regex pattern did not match` — the native
  `UnicodeDecodeError` escaped with its own message instead of the normalized
  `could not be read` wording (and the directory case let a native `OSError`
  escape entirely).
- `test_second_run_start_preserves_history_and_eligibility_verdict`: FAILED
  with `AttributeError: module 'pinn.conformance.preflight' has no attribute
  'REQUIRED_RUN_START_CHECKS'` — the contract the test asserts did not exist
  yet.

**First-run-green disclosures (honesty, not hidden REDs):**

- `test_complete_run_start_artifact_is_eligible` is the CONTROL: green by
  construction on the upgraded helper. It exists so every negative in the file
  is discriminating against a genuinely eligible baseline (D-16).
- `test_duplicate_required_check_with_one_failure_is_not_eligible` was green on
  its first run: Task 1's all-occurrences-passed window-check rule already
  denied the duplicate-with-one-failure shape. Retained as the named
  GATE-01-adjacency regression.
- `test_run_local_divergence_position_is_deterministic` was green on its first
  run: the deterministic terminal-position append is Task 1's mechanism (whose
  absence pre-Task-1 is proven by the RED of
  `test_preflight_appends_run_local_n_unset_divergence_when_window_absent`).
  Retained as the named INST-03-ordering regression.

**GREEN evidence:** `.venv/bin/python -m pytest -q
tests/phase49/test_preflight_integrity.py tests/phase49/test_inst03_register.py
tests/phase49/test_gate01_table.py` → **107 passed in 11.88s**, including the
D-27 evidence-trail survivors
(`test_failed_status_with_a_failed_locked_check_still_loads`,
`test_failed_advisory_check_under_passed_status_is_accepted`,
`test_open_divergence_under_passed_status_loads_but_is_not_eligible`) and the
legal-boundary-ordering survivor
(`test_controller_stage_boundary_events_follow_entered_order`).

## Affected-existing-test inventory (fixture repair — never the gate)

Task 1 step 5: these tests asserted eligibility for a run whose fixture left
the window unset — precisely the state that must now be ineligible. The
FIXTURE was stale in each case; the gate is what is correct now. Binding 500
in a fixture reads the owner's ratified value from `configs/stage0-example.yaml`;
it selects nothing (D-21).

| Test | Repair | Why the fixture was stale |
|---|---|---|
| `test_preflight_composes_census_and_every_open_register_entry` | `_preflight_config()` → `_preflight_config(500)` | Its exact-equality assertion against the register's open entries is only honest for a bound run; an unbound run now carries the run-local record. The unbound counterpart is the new `..._appends_run_local_n_unset_divergence...` test. |
| `test_surfaces_in_run_record` | `_write_real_preflight(run_dir)` → `n=500` | Asserted `eval01_precondition_i is True` for an N-unset run. |
| `test_surfaces_in_run_record_true_with_no_open_divergence` | added `n=500` | Same. |
| `test_surfaces_in_run_record_committed_register_owner_n_branch_ignores_open_qualifications` | added `n=500` | Same. |
| `test_surfaces_in_run_record_open_qualification_travels_without_blocking` | added `n=500` | Same. |
| `_write_real_preflight` | gained keyword `n=None` threaded into `_preflight_config(n)` | The default stays UNBOUND so the N-unset tests keep exercising that state. |

One collateral assertion adjustment inside `test_surfaces_in_run_record`
(recorded as a deviation for transparency): `assert "INV-B-N-UNSET" in markdown`
was replaced with `assert "CONF-01-QUALIFICATION" in markdown`. Pre-repair, the
`INV-B-N-UNSET` string reached the markdown only via the consistency finding
that fired for the (unbound config, closed register) disagreement; with the
repaired bound fixture, config and register AGREE, so no finding fires and the
string is honestly absent. The replacement preserves equal-strength evidence
that an open register entry's id projects verbatim into `summary.md`. The
predicate, the register filter, and every eligibility assertion are untouched.

Task 2 step 5: `_event` in `tests/phase49/test_preflight_integrity.py` was
upgraded so its DEFAULT is a complete honest run_start (all seven required
check names present and passing, census verdict `passed`), keeping its keyword
surface so each negative perturbs exactly one thing. The pre-existing negatives
were re-run after the upgrade and each still fails or passes for its ORIGINAL
encoded reason: the forgery refusals still refuse at load
(`test_forged_passed_status_over_a_failed_locked_check_is_refused`,
`test_forged_passed_status_over_a_failed_event_is_refused`,
`test_forged_artifact_cannot_report_eval01_eligibility`), the advisory
acceptance still loads
(`test_failed_advisory_check_under_passed_status_is_accepted`), and
`test_open_divergence_under_passed_status_loads_but_is_not_eligible` is still
denied SOLELY by its open divergence (the upgraded baseline is otherwise fully
eligible — proven by the new control).

**Deliberately unchanged sentinels** (ordering assertions, not eligibility
assertions; zero edits, still green):
`test_malformed_metadata_object_writes_refusal_before_raise`,
`test_runtime_census_failure_is_normalized_after_refusal_is_written`,
`test_non_mapping_census_result_is_normalized_after_refusal_is_written` — all
three assert `checks[-1]["name"] == "census"`, which held because the window
check was inserted BEFORE the census append in both branches.

**Untouched happy path:** `test_real_main_orders_preflight_table_boundary_and_first_guard`
keeps its `summary["eval01_precondition_i"] is True` assertion byte-identical
(zero removed diff lines in `tests/phase49/test_e2e_seam.py`), and the
owner-ratified N = 500 run remains eligible.

## `PREFLIGHT_SCHEMA_VERSION` stays 1

The payload SHAPE is unchanged: no top-level key was added, renamed, or
removed; the new evidence rides inside the existing `checks` and
`open_divergences` arrays under the existing five-key check contract and
ten-key register-entry shape. Only the payload's semantic validation (history
ordering, read-error normalization) and its consumer's requirements (the
eligibility predicate) tightened. No persisted real-corpus artifact exists to
distinguish the two validation regimes (D-29 — the gate's first real-corpus
contact is Phase 50), so there is nothing a bumped version would disambiguate.
A future consumer that needs to tell the regimes apart may bump it then.

## Untouched findings

- **GATE-03 unclassified edge row — still UNRESOLVED, as planned.** The
  deterministic edge probe could not classify GATE-03's requirement text, and
  this plan proceeded on the flagged assumption that GATE-03's remaining edge
  surface is exactly the run-local N binding named in D-20. Nothing about
  invariant A, the HALT disposition, or resume continuity was newly at issue
  (those are VERIFIED in `49-VERIFICATION.md` truth 3's supporting evidence).
  If a reviewer disagrees, the correct response is to widen `must_haves`, not
  the code.
- **INST-03 concurrency (torn-write survivability)** remains a backstop
  disposition: `atomic_write_text` rename semantics plus append-only history
  mean a torn write leaves either the prior complete artifact or none. No test
  added; none required by the plan.
- **Informational anti-pattern row (debt markers):** the verifier's third
  Anti-Patterns row found no `TBD`/`FIXME`/`XXX` debt markers (severity None).
  Nothing to fix; a fresh scan of this plan's added lines finds none either.
- The verifier's two WARNING anti-patterns are both FIXED here:
  `preflight.py:384` (wrong config path) by the single-accessor repair, and
  `preflight.py:305` (partial read-error normalization, WR-02) by the
  `(OSError, UnicodeError)` clause.
- Plans `49-01`…`49-08` and their summaries are untouched;
  `configs/stage0-example.yaml` (still carries the owner-ratified 500),
  `configs/smoke.yaml` (still leaves the slot unset),
  `pinn/conformance/divergence_register.json` (INV-B-N-UNSET stays globally
  `closed`), and `pinn/conformance/table.py` are byte-for-byte unchanged
  (`git diff --stat -- configs/ pinn/conformance/divergence_register.json`
  empty; `table.py` not in this plan's `files_modified` at all).
- `.planning/STATE.md` and `.planning/REQUIREMENTS.md` are deliberately
  untouched: re-verification owns requirement status.

## Verification results

| Gate | Command | Result |
|---|---|---|
| Pre-fix baseline (Task 1 precondition) | `.venv/bin/python -m pytest -q tests/phase49` | **176 passed in 13.27s** on the unmodified tree |
| Task 1 verify (tracer gate) | `… pytest -q tests/phase49/test_e2e_seam.py tests/phase49/test_inst03_register.py tests/phase49/test_gate03_invariants.py` | **86 passed in 11.71s** |
| Task 2 verify | `… pytest -q tests/phase49/test_preflight_integrity.py tests/phase49/test_inst03_register.py tests/phase49/test_gate01_table.py` | **107 passed in 11.88s** |
| Full Phase-49 suite (final tree) | `… pytest -q tests/phase49` | **190 passed in 13.61s** — 176 baseline + 14 new, 0 failed, count ≥ 176 |
| Cross-phase suite (49-VALIDATION full command, final tree) | `… pytest -q tests/phase38 tests/phase40 tests/phase41 tests/phase42 tests/phase43/test_summary_enrichment.py tests/phase43/test_summary_honesty.py tests/phase43/test_real_data_smoke_config.py tests/phase46 tests/phase47 tests/phase48 tests/phase49` | **957 passed, 3 skipped, 289 subtests passed in 414.11s**, exit status 0 |
| D-28 preservation probe | `… test_inst03_register.py::test_no_gate_collision_in_preflight_and_register_payload` | passed |
| D-06 preservation probe | `… test_gate01_table.py::test_stage2_fails_without_rebound_scheduler` | passed |
| Owner-ratified config pin | `grep -v '^[[:space:]]*#' configs/stage0-example.yaml \| grep -c 'front_advance_window_n: 500'` | `1` |

The cross-phase run's complete stdout, stderr, exit status, command, working
directory, HEAD, and start/end timestamps are retained in the session-scoped
evidence file `$TMPDIR/49-09-cross-phase-evidence.log` (outside the
repository; run once at 2026-08-11T06:03:28Z–06:10:22Z against the final
tree). The 957 = 943 prior + 14 new accounting matches the phase-49 delta
exactly; the 3 skips are the pre-existing curated phase-43 skips.

New named test node IDs (14): the two promoted disconfirmation probes
(`test_real_main_with_n_unset_is_structurally_ineligible`,
`test_stage_boundary_only_history_is_refused_at_load`), the
consistency-finding path repair
(`test_consistency_finding_reads_run_scoped_window_from_real_config`), the
three run-local divergence composition tests, the eligible-baseline control,
the four required-evidence negatives, the duplicate-occurrence adjacency test,
the WR-02 normalization test, and the two INST-03 ordering/idempotency tests —
exactly the plan's "New test node IDs" list.

## Deviations from Plan

**1. [Rule 2 — missing critical functionality] Equal-strength replacement of
one collateral assertion in `test_surfaces_in_run_record`.**
- **Found during:** Task 1 step 5 fixture repair.
- **Issue:** the repaired (bound) fixture legitimately stops producing the
  consistency finding whose render had supplied the `INV-B-N-UNSET` substring
  to `summary.md`; the pre-repair assertion encoded the stale fixture state.
- **Fix:** `assert "CONF-01-QUALIFICATION" in markdown` replaces it, preserving
  the projection evidence at equal strength for a fixture state the test
  honestly produces. The gate, the predicate, and the register filter are
  untouched — this is the fixture-repair side the plan sanctions, not a
  relaxation.
- **Files modified:** `tests/phase49/test_inst03_register.py`.

No other deviations. Everything else executed exactly as written.

## Self-Check: PASSED

- `.planning/phases/49-conformance-gate/49-09-SUMMARY.md` — exists (this file).
- All seven `files_modified` code/test/planning paths verified present in the
  working tree and in the atomic commit (hash recorded in the execution
  report; single commit by design — the plan's Task 3 step 5 overrides the
  per-task-commit convention).
- `git diff --check` clean; `configs/`, `divergence_register.json`,
  `table.py`, `.planning/STATE.md`, and `.planning/REQUIREMENTS.md` confirmed
  absent from the change set.
</content>
