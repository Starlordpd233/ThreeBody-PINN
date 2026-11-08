---
phase: 67-design-settings-ladders
reviewed: 2026-11-08T00:00:00Z
depth: standard
files_reviewed: 29
files_reviewed_list:
  - pinn/verification/diagnostic_phase67.py
  - pinn/verification/diagnostic_phase67_catalog.py
  - pinn/verification/diagnostic_phase67_records.py
  - pinn/verification/diagnostic_phase67_execution.py
  - pinn/verification/diagnostic_phase67_windows.py
  - pinn/verification/diagnostic_fit.py
  - pinn/verification/diagnostic_time_features.py
  - pinn/verification/diagnostic_variants.py
  - pinn/verification/diagnostic_similarity.py
  - pinn/verification/diagnostic_power.py
  - tests/phase67/__init__.py
  - tests/phase67/_fixtures.py
  - tests/phase67/test_tracer.py
  - tests/phase67/test_admission.py
  - tests/phase67/test_historical.py
  - tests/phase67/test_time_features.py
  - tests/phase67/test_catalog.py
  - tests/phase67/test_windows.py
  - tests/phase67/test_checkpoints.py
  - tests/phase67/test_budget.py
  - tests/phase67/test_records.py
  - tests/phase67/test_reading_rule.py
  - tests/phase67/test_pages.py
  - tests/phase67/test_workflow.py
  - tests/phase67/test_isolation.py
  - tests/phase65/test_fit_short.py
  - tests/phase66/test_historical.py
  - tests/phase66/test_pages.py
  - .planning/phases/67-design-settings-ladders/evidence/harness-freeze.json
findings:
  critical: 0
  warning: 5
  info: 7
  total: 12
status: issues_found
---

# Phase 67: Code Review Report

**Reviewed:** 2026-11-08
**Depth:** standard
**Files Reviewed:** 29 (plus the exp02–exp05 evidence JSON/MD artifacts, checked for internal consistency)
**Status:** issues_found

## Summary

The Phase 67 diagnostic harness (catalog, budget, cadence, windows, records reader, execution adapter, fit/power integration) and its 15 test modules were reviewed at standard depth, with the committed evidence artifacts cross-checked rather than line-read. The core machinery is sound: the budget arithmetic re-derives independently from the committed timing rows (exp02 N=152900, worst projection 2649.96 s ≤ 2655.0 s target, re-verified numerically), the cadence/score/stride outputs follow exactly from the frozen N, the harness freeze manifest's 41 pinned digests all match current bytes and are committed clean, every budget's timing-evidence digests are fresh, every result page embeds its committed review verbatim, the exp04 851 encoded rows carry the orbit-specific `-851` declarations at the correct census frequency, the exp05 rows carry per-orbit lap variants, and the exp03 `confirmed-worsening` → proposal-pending → authorized-ruling chain is digest-faithful end to end. The check-row command provably exposes no scientific values, and scores are gated behind a clean audit in both readers.

The findings below are all gaps in defense-in-depth enforcement, not failures on the normal path: four launch/admission gates verify less than their sibling audit commands or their module docstrings claim (WR-01..WR-03), the owner-ruling scope gate cannot selectively restrict downstream experiments (WR-04), and a narrow supervisor race can downgrade a published attempt claim (WR-05). Each is exploitable only through a committed tampering step the regime's own chronology audits would surface, and in every case the registration-bound readers refuse the produced evidence before any scientific value is exposed — but each burns a scarce compute window before that refusal, which under the no-retry policy is the real cost. The committed evidence itself shows no instance of any of these gaps having been hit.

The intentional fail-closed refusals named in the phase context (harness freeze re-pin convention, power gate compute window, check-row value hiding, pre-registered reading thresholds) were treated as design, not defects.

## Warnings

### WR-01: The T-67-04 census-agreement admission check is dead in the wired fit path

**File:** `pinn/verification/diagnostic_phase67_catalog.py:551-572`; `pinn/verification/diagnostic_fit.py:363-381, 424-451`

**Issue:** `phase67_registry` implements the documented T-67-04 protection — "rejects a settings block whose orbit's census row disagrees with the declaration the settings name" — but only when the settings mapping carries BOTH `variant` and `orbit_key`. The only production caller, `validate_smoke_settings` → `_named_registry`, always passes `{"variant_registry": name}` (a one-key mapping), so the census branch never executes at the settings door; it is reachable only from `tests/phase67/test_catalog.py:309-326`. Enforcement of "a 1632-pinned declaration never runs mis-encoded on 851" therefore rests entirely on matrix construction (`phase67_arm_variant`) and the post-hoc reader binding (`_matrix_row_problems`), both of which run after the registration is already committed — and a hand-written committed registration naming `exp04-locked-f1` with `orbit_key: hierarchical/gold/851` admits through `validate_smoke_settings` (variant found in registry, byte-agreement holds, window matches) and would run mis-encoded before any refusal.

**Fix:** In `validate_smoke_settings`, resolve the registry through the full settings block once the variant name is known, e.g. after the byte-agreement loop call `phase67_registry(settings)` (which now carries `variant` and `orbit_key`) inside a `VariantRefused` → `DiagnosticFitRefused` translation, so the census check actually runs at admission. Note WR-01 interacts with IN-03 (the exp05 lookup inside the census branch resolves only from the static registry) — fix both together.

### WR-02: `launch_phase67_row` never verifies the committed registration against its matrix row

**File:** `pinn/verification/diagnostic_phase67_execution.py:2111-2203` (launch); contrast `pinn/verification/diagnostic_phase67_execution.py:2796-2831` (check-matrix)

**Issue:** `check_matrix` verifies each registration's `variant.name == row["variant_name"]`, orbit, seed, `physical_window`, cadences and cap against its matrix row. `launch_phase67_row` — the command that actually spends the compute window — checks only that the matrix is committed, the registration file exists and is committed clean, prerequisites exist, and the output is absent; it then delegates to `power.launch`, whose `check_fit_registration` admission validates the settings against the registry (byte-agreement, window-vs-variant, cap < 1 h) but never against the row. A committed registration that disagrees with its row (stale variant, wrong orbit/seed/cap, or for exp05 a lap variant whose window differs from the row's) launches unrefused; the mismatch is caught only post-hoc by `check_row`/`write_review` via `_matrix_row_problems`, after the window is burned. Under the no-retry policy that is a lost row slot.

**Fix:** In `launch_phase67_row`, after resolving `row`, load the registration JSON and require the same predicate check-matrix uses — at minimum `settings["variant"]["name"] == row["variant_name"]`, `settings["orbit_key"] == row["orbit_key"]`, `settings["seed"] == row["seed"]`, `settings["physical_window"] == row["physical_window"]`, and `settings["whole_run_cap_seconds"] == row["schedule"]["cap_seconds"]` — before the supervised launch.

### WR-03: Row launch, check-row and review skip the harness-freeze verification

**File:** `pinn/verification/diagnostic_phase67_execution.py:2111-2203` (launch), `2238-2276` (check-row), `2287-2391` (write-review); `verify_harness_freeze` call sites at lines 1342, 2013, 2528, 2585, 2647, 2708, 2832, 2897

**Issue:** `verify_harness_freeze` is enforced in metadata admission, budget, check-matrix, check-budget, design, check-metadata and audit — but not in `launch_phase67_row`, `check_row` or `write_review`. The freeze manifest's 41 pinned files include four production math modules that are NOT covered by the row registrations' `code_dependencies` (the 13 harness modules) or their copied `frozen` block (`feasibility_scorer.py`, `feasibility_scorecard.py` only): `pinn/network.py` (the model class), `pinn/architecture_spec.py`, `pinn/constants.py`, `pinn/verification/learnability_protocol.py`. A post-freeze edit to any of these admits at launch (registration admission checks only the enumerated artifacts), executes the row with modified model math, and is caught only post-hoc — the record's `source_sha256` (33 pinned modules, which do include these four) then disagrees with the changed modules and the reader refuses the evidence. The freeze manifest digest is pinned inside every registration but nothing on the launch path re-verifies the manifest's per-file contents. The module docstring's claim ("no phase67 registration or launch can precede the compatibility gate") overstates the wired enforcement for launches.

**Fix:** Call `verify_harness_freeze(root, phase)` in `launch_phase67_row` before the supervised launch (the freeze is already committed and clean by the time any row registration exists, so this adds one git-status + 41 digest reads per launch). Optionally also in `check_row`/`write_review` for symmetry.

### WR-04: The owner-ruling scope list cannot restrict which downstream experiments unblock

**File:** `pinn/verification/diagnostic_phase67_execution.py:2394-2471` (`_verify_ruling`), `2077-2108` (`phase67_prior_experiment_allowed`)

**Issue:** `phase67_prior_experiment_allowed(experiment)` verifies a prior experiment's pending-proposal ruling via `_verify_ruling(prior, ...)`, and `_verify_ruling`'s coverage predicate is `any(experiment in item or item.endswith("*") for item in allowed)` where `experiment` is the BLOCKED (prior) experiment. The dependent experiment's name is never matched against `allowed_dependent_work`. Consequently, once a prior's ruling verifies, every downstream experiment unblocks: the committed exp03 ruling names `EXP-04` (uppercase, so `"exp04" not in item`) yet `phase67_prior_experiment_allowed("exp04")` and `("exp05")` both return True today — the exp03 item passes because it happens to contain the substring "exp03". The fixture suite codifies this (`test_workflow.py:734-745` asserts exp04 is allowed under a ruling whose scope item names only exp03). The refusal message "the ruling's allowed dependent work does not cover {experiment!r}" and the check-review docstring's "scope-matching" therefore promise a per-dependent restriction the implementation cannot deliver; a ruling authorizing only exp03 still admits exp04/exp05 launches.

**Fix:** Thread the dependent experiment into the ruling verification — e.g. `_verify_ruling(prior, review, ..., dependent=experiment)` with the coverage predicate testing the dependent's name (exact token or an explicit glob convention, not a bare substring) — or, if unblocking the whole chain is the registered intent, fix the refusal message and docstrings to say so and stop implying per-dependent scoping.

### WR-05: The supervisor timeout path can overwrite a published attempt claim

**File:** `pinn/verification/diagnostic_phase67_execution.py:1485-1507` (`_ensure_incomplete_attempt`); `pinn/verification/diagnostic_fit.py:1473-1498` (`_mark_attempt` / `_ensure_incomplete_attempt`)

**Issue:** `_ensure_incomplete_attempt` rewrites an existing `attempt.json` unconditionally to `status: "incomplete"`. In `launch_phase67_row` (execution lines 2186-2194) and `_cmd_run` (fit lines 1962-1974), the parent marks incomplete whenever `process.join(timeout)` reports the child still alive — but a child that publishes its record and flips its attempt to `published` in the microseconds between the join expiry and the SIGTERM landing produces a completed run whose attempt claim is then downgraded to `incomplete` by the parent. Under this phase's own adversarial-reading rules the flipped claim makes the row refuse (`_PROBLEM_ATTEMPT_STATUS`), the record survives but now contradicts its claim, and nothing in the evidence records that a downgrade happened — evidence corruption, not just a refusal. The race window is narrow (the publication-vs-join boundary) but the fix is cheap.

**Fix:** In both `_ensure_incomplete_attempt` variants, refuse to downgrade a claim already in `status: "published"` (leave it, or append a `downgraded_by_supervisor` side field with the reason and timestamp instead of replacing `status`). The exclusive-write and no-retry semantics are unaffected.

## Info

### IN-01: Vacuous census-mutation subtest in test_catalog.py

**File:** `tests/phase67/test_catalog.py:358-377`

**Issue:** The "non-numeric N_in" case appends `{"id": 700, "N_in": "fast"}` to the singles but then queries `census_n_in(701 ...)`; the appended row is never consulted and the refusal comes from "the committed census holds no row for orbit 701". The non-numeric-`N_in` branch of `census_n_in` is exercised only by the NaN case (id 701), which does hit its row. The suite still passes, but one of the four claimed mutation paths is not actually under test.

**Fix:** Query `700` for the non-numeric case (or append the mutated row with id 701).

### IN-02: `_score_agreement` raises a bare KeyError instead of a typed refusal

**File:** `pinn/verification/diagnostic_phase67_windows.py:341-367` (`left[key]` indexing at lines 356-357)

**Issue:** `_score_agreement` indexes `left[key]`/`right[key]` directly for `E`, `e_sys_max`, `e_in_max`, `eps_h`, `R_sys`. A score dict missing any of these keys raises `KeyError`, which escapes `same_window_expectations` as an unhandled exception rather than a `WindowExpectationRefused`; in the metadata capture this surfaces only as a generic "incomplete" attempt reason instead of a named refusal. Currently unreachable with the frozen scorer's `to_json_dict`, but it is the one path in the module that fails untyped.

**Fix:** Use `.get(key, _MISSING)` with a sentinel and return `(False, inf, inf)` on a missing key.

### IN-03: The census branch of `phase67_registry` resolves exp05 names only from the static registry

**File:** `pinn/verification/diagnostic_phase67_catalog.py:557`

**Issue:** The variant+orbit census branch looks up `PHASE67_REGISTRY.get(variant_block["name"])`, so a settings block naming a materialized exp05 lap variant WITH an orbit_key would refuse "unknown diagnostic variant" even though the merged table returned at the end of the same function contains it. Unreachable today (the fit door always passes a one-key mapping, so the branch never runs), but it is a latent trap the moment WR-01's fix wires full settings through this function — the exp05 lap registrations would then refuse admission.

**Fix:** Build the merged table (`PHASE67_REGISTRY` + `_EXP05_WINDOW_VARIANTS`) before the census branch and resolve the variant from it.

### IN-04: The basic reader `read_phase67_record` lacks the science reader's containment guards

**File:** `pinn/verification/diagnostic_phase67_records.py:409-602` (contrast with the science reader's guards at lines 975-1008)

**Issue:** `read_phase67_run_directory` checks the record's weights reference for path traversal and symlinks BEFORE calling `verify_fit_result` (T-67-13). The basic `read_phase67_record` does not, so a hostile record naming an outside weights path gets that file opened and hashed by `verify_fit_result` before refusal. No content is disclosed (the digest/marker checks fail and the reader only reports `_PROBLEM_FIT_AUDIT`), and the basic reader's only production caller is the tracer test path, but the containment guarantee is inconsistently applied across the two readers of the same evidence shape. The basic reader also does not de-duplicate its mechanical list (the science reader does, line 1184).

**Fix:** Factor the `_PROBLEM_UNSAFE_PATH`/`_PROBLEM_SYMLINK` pre-check into a helper shared by both readers, or restrict `read_phase67_record` to fixture/phase-65-shaped use and say so in its docstring.

### IN-05: `census_n_in` silently skips non-mapping census rows

**File:** `pinn/verification/diagnostic_phase67_catalog.py:475-477`

**Issue:** `for row in singles: if not isinstance(row, Mapping) or row.get("id") != orbit_id: continue` — a census row that is not an object is skipped rather than refused, so a malformed committed census produces the misleading "holds no row for orbit X" refusal instead of naming the malformed document. Overall behavior stays fail-closed (no frequency is manufactured).

**Fix:** Refuse with a named problem when a `singles` entry is not a Mapping.

### IN-06: CLI cosmetics in `diagnostic_phase67.main`

**File:** `pinn/verification/diagnostic_phase67.py:1160-1165, 1246`

**Issue:** The `SystemExit` handler prints `PHASE67-REFUSED: unknown or missing option` even when argparse exits 0 (e.g. `--help`), mislabeling a successful help render as a refusal on stderr while still returning 0. Line 1164's f-string carries no placeholders, and line 1246 uses an inline `__import__("json")` where a local import beside `argparse` would read normally.

**Fix:** Only print the refused line when `exc.code` is not 0/None; import `json` alongside `argparse` inside `main`.

### IN-07: `phase67_cost_rows` silently defaults a missing weights byte count to 1

**File:** `pinn/verification/diagnostic_phase67_execution.py:1866`

**Issue:** `weights_bytes = entry[5] if len(entry) > 5 else 1` — a caller passing 5-tuples gets a synthetic 1-byte weight count folded into the budget's byte bound instead of a refusal. Both current callers pass 6-tuples, so no live effect, but every other missing field in this extractor is a hard `_require` refusal; the one silent default is a foot-gun for future callers and skews the byte bound imperceptibly.

**Fix:** Make the sixth element required (raise `Phase67CommandRefused` on a short tuple), matching the extractor's fail-closed contract.

---

## Verification performed during this review

- Harness freeze: all 41 pinned digests recomputed against current bytes — 0 mismatches; manifest committed clean.
- exp02–exp05 evidence: timing-matrix rows all have committed records; every budget's `timing_evidence` digests fresh; science matrices frozen at the budget's exact N (exp02 152900, exp03 155100, exp04 112700, exp05 148700); result pages embed their committed reviews byte-exactly; contrast labels map correctly to dispositions (exp03 `confirmed-worsening` → proposal-pending; ruling digests — review, result page, proposal — all match).
- Budget arithmetic independently recomputed for exp02 from `inputs.rows` (residual + warmup + margin-scaled measured steps): 2649.96 s ≤ 2655.0 s target; cadence `[0, 38225, 76450, 114675, 152900]`, score cadence, and stride 153 (⇒ 1000 trace entries) all derive from N exactly.
- Orbit-aware bindings in the committed registrations verified (exp04 851 rows carry the `-851` variants at `FEATURE_FREQUENCY_851`; exp05 rows carry `exp05-lap<L>-<orbit>` variants).
- `phase67_prior_experiment_allowed` executed against the committed evidence (exp03/exp04/exp05 → True), which is how WR-04's scope-matching gap was confirmed.
- Static scans: no secrets, no debug artifacts, no bare excepts; broad `except Exception` uses are bounded and fail closed.

_Reviewed: 2026-11-08_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
