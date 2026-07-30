---
phase: 46-frame-resolution-gate-aligned-validation
verified: 2026-07-30T05:10:00Z
status: passed
score: 70/70 must-haves verified
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: 57/61
  gaps_closed:
    - "EVAL-01 precondition (iii) is true only for the latest persisted gate record and its same-event, contained, semantically valid sidecar"
    - "Every latest validation event fails closed and an older eligible record can never remain presented as current"
  gaps_remaining: []
  regressions: []
deferred:
  - truth: "Training residency and IC13 share the full locked rotation-gauged, D/V-scaled canonical frame"
    addressed_in: "Phase 47"
    evidence: "CONF-09 and Phase 47 success criteria explicitly move residency to pre.r_gauge/pre.v_gauge and re-ratify the validation frame before CONF-02 (GAP-46-07, owner ruling 2026-07-28, option A)."
---

# Phase 46: Frame Resolution & Gate-Aligned Validation Verification Report

**Phase Goal:** The last remaining way the next run could be invalid is settled, and validation carries a conservation signal where none exists.
**Verified:** 2026-07-30T05:10:00Z
**Status:** passed
**Re-verification:** Yes — after gap closure (Plan 46-10)

## Verdict

Both INST-01 gaps recorded in the prior verification (2026-07-29T13:19:23Z, `gaps_found`, 57/61) are genuinely closed by Plan 46-10 (`ad5331cd`, `35c88d7f`, plus the same-run code-review fix `bbc398b`). This pass independently re-derived the closure from source, ran the specific test classes that exercise each previously-failing behavior (not the full suite blindly trusted), and hand-executed the exact adversarial scenarios the prior verifier used to prove the defects (cross-run traversal, semantic forgery, type-aliased equality, latest-event fallback). All reproduced as fixed. CONF-01 and CONF-08 are untouched by Plan 46-10 (byte-identical files, unchanged evidence directories) and their mandatory qualifications/exclusions travel forward unchanged. CONF-09 remains correctly deferred to Phase 47 per the standing owner ruling and is not re-litigated here.

## Goal Achievement

### Roadmap Success Criteria

| # | Roadmap truth | Status | Evidence |
|---|---|---|---|
| 1 | RG-02 is settled by a train-free stored-target residual check with recorded evidence and verdict. | ✓ VERIFIED — QUALIFIED (unchanged) | `pinn/data/adapter.py`, `pinn/data/preprocessing.py`, `pinn/verification/target_frame_probe.py` are byte-for-byte identical between the prior verification and HEAD (`git diff 0355cbbc..HEAD --stat` for these three files is empty). CONF-01 remains **owner-settled from measured arm evidence under GAP-46-06, not a clean machine verdict** — this qualification is preserved verbatim and must still travel to EVAL-01 precondition (ii). |
| 2 | The sixth divergence is surfaced as an owner scope decision, never silently absorbed. | ✓ VERIFIED (unchanged) | GAP-46-04/05/06/07 remain `RESOLVED-WITH-INSTRUCTION`; no new gap or re-litigation was introduced by Plan 46-10 (confirmed: no new `## GAP-46-` entry exists in `46-GAPS.md`). |
| 3 | Per-trajectory ε_H/SCS are computed on validation through `gate_metrics`, persisted per event, and projected fail-closed for EVAL-01 (iii). | ✓ VERIFIED | Both prior blockers are closed. (a) `validate_sidecar_payload` now recomputes every per-row/aggregate SCS, verdict, and nonfinite count through the same `gate_metrics.scs_from_eps_h`/`aggregate_gate_verdict` functions the sidecar was built from, and rejects any disagreement (confirmed by direct source read and by running `SemanticInvariantTests` — 23/23 pass). (b) `_eval01_precondition_iii` binds the JSONL record to its own exact same-run, same-step, fully-valid sidecar via `_json_scalar_equal` (type-AND-value equality) over all eight compact fields; I directly executed `_json_scalar_equal(False, 0) == False`, `_json_scalar_equal(True, 1) == False`, `_json_scalar_equal(1, 1.0) == False` against the live module to confirm bool/int/float aliasing is genuinely rejected, not just claimed. (c) Every validation event — including nonfinite loss and `failed:` gate status — now leaves exactly one JSON-safe JSONL line (the early-return-without-append bug is removed from `pinn/train.py::_append_validation_record`); the physical latest non-empty line is the sole eligibility source, confirmed by running `LatestEventMonotonicityTests` (7/7 pass, covering torn/non-mapping/blank-only/undecodable/failed/nonfinite-loss latest events). |
| 4 | Resident series match `masses_ordered`, carry COM/boost gauge, and the unchanged 1,651-record probe is re-run once. | ✓ VERIFIED (unchanged) | `pinn/data/adapter.py`/`preprocessing.py` untouched by Plan 46-10; `plus_permutation == 0.0` for 1651/1651 remains the recorded evidence; exactly one post-repair run exists (`evidence/target-frame/` unchanged — no new directory). |

**Roadmap score:** 4/4 criteria verified (up from 3/4).

### Every PLAN Must-Have Truth

Truth IDs are their order under each plan's `must_haves.truths`. Plans 46-01 through 46-09 received a regression check (their source files are byte-identical to the prior verification pass — `git diff --exit-code HEAD -- .../46-0[1-9]-PLAN.md` and the equivalent source-file check both confirm no drift); the four previously-failed sub-truths and all nine of Plan 46-10's own truths received full re-verification.

| Plan | Truth audit | Result | Evidence / closure |
|---|---:|---|---|
| 46-01 | T1–T8 | 8/8 VERIFIED (regression) | Unchanged; fixtures still drive all Phase 46 suites (151 passed). |
| 46-02 | T1–T9 | 9/9 VERIFIED (regression) | Unchanged; `pinn/data/adapter.py`/`preprocessing.py`/`target_frame_probe.py` byte-identical. |
| 46-03 | T1–T8 | 8/8 VERIFIED (regression) | Unchanged gate-composition core; still exercised by the passing suite. |
| 46-04 | T1–T6 | 6/6 VERIFIED (regression) | Unchanged evidence-writer/CLI contract. |
| 46-05 | T1–T6 | **6/6 VERIFIED — T5 now CLOSED** | T5 ("schema validation fails closed on corrupt sidecars") previously failed because semantic corruption (`frame={}`, `split="test"`, `gate_status="failed"`, `global_step=-99`, `stage=-3`) was accepted. `validate_sidecar_payload` now rejects every one of these individually — confirmed by running `SemanticInvariantTests::test_cr04_repro_split_status_step_stage_frame_all_individually_rejected` directly (part of the 23/23 `SemanticInvariantTests` pass). |
| 46-06 | T1–T5 | 5/5 VERIFIED — QUALIFIED (regression) | Unchanged; owner ruling and evidence untouched. |
| 46-07 | T1–T7 | **7/7 VERIFIED — T4, T5, T7 now CLOSED** | T4 ("non-finite validation loss can suppress the failure record"): the early-return-without-append bug is removed from `_append_validation_record`; every event now reaches the single append (confirmed: `test_non_finite_final_val_loss_is_persisted_not_dropped`, `test_positive_and_negative_infinite_val_loss_persist_as_sentinels` pass). T5 ("eligibility not bound to the latest same-event sidecar"): closed by the full identity-binding contract in `_eval01_precondition_iii` (confirmed: `Eval01IdentityBindingTests` 3/3 pass, 8 subtests). T7 (backstop — "malformed trailing JSONL falls back to an older eligible record"): closed by `_read_latest_validation_event`'s physical-latest-line-only selection (confirmed: `LatestEventMonotonicityTests` 7/7 pass, including the undecodable-bytes fix `bbc398b`). |
| 46-08 | T1–T6 | 6/6 VERIFIED (regression) | Unchanged; `pinn/data/preprocessing.py`/`adapter.py` byte-identical since 0355cbbc. |
| 46-09 | T1–T6 | 6/6 VERIFIED (regression) | Unchanged; probe hash, population, controls, and owner routing untouched; no new probe run. |
| **46-10** | T1–T9 | **9/9 VERIFIED (new)** | See below. |

**Plan truth score: 70/70 verified** (61 from 46-01..09, now fully closed, + 9 new from 46-10).

### Plan 46-10's Nine Truths (gap-closure plan)

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | EVAL-01 precondition (iii) true only for the physical latest event with finite loss, `gate_status ok`, and all eight compact fields exactly matching a valid same-run/same-step sidecar | ✓ VERIFIED | `_eval01_precondition_iii` (`summary.py:246-318`) implements every clause; `Eval01IdentityBindingTests` + `LatestEventMonotonicityTests` (10/10 combined) directly executed and pass. |
| 2 | Sidecar semantic validity requires exact v1 keys, frame tuple, split, strict integral identities/counts, unique ordered RecordKeys, canonical thresholds, and gate_metrics-recomputed per-row/aggregate/verdict agreement | ✓ VERIFIED | `validate_sidecar_payload` (`validation_gate.py:541-702`) recomputes via the *same* `gate_metrics.scs_from_eps_h`/`aggregate_gate_verdict` functions production uses to build the sidecar (line 275 vs line 648 — confirmed by direct source diff, not a divergent reimplementation); `SemanticInvariantTests` 23/23 pass. |
| 3 | `compact_validation_fields` derives every value from the validated durable payload, never the in-memory observation | ✓ VERIFIED | `compact_validation_fields_from_payload` projects exclusively from `validated[...]`; `PayloadDerivedCompactFieldsTests::test_compact_fields_reflect_disk_payload_not_a_differing_observation` passes. |
| 4 | Every event (incl. nonfinite loss, failed gate) leaves one JSON-safe line; latest malformed/torn/non-mapping/nonfinite/failed event is explicitly ineligible and can never reveal an older success | ✓ VERIFIED | Early-return bug removed from `train.py::_append_validation_record`; `_read_latest_validation_event` inspects only the physical last line (never falls back); `LatestEventMonotonicityTests` 7/7 pass, including the `UnicodeDecodeError` fix from `bbc398b`. |
| 5 | Boolean/fractional/string steps rejected before filename/record construction; equal integral steps share identity, adjacent differ (WR-01) | ✓ VERIFIED | `_strict_nonnegative_integral` rejects bool explicitly (bool is a `numbers.Integral` subclass in Python) before any `int()` conversion; `StrictStepIdentityTests` 3/3 pass. |
| 6 | CONF-01 remains owner-settled from measured evidence, not a clean verdict; this plan changes neither that evidence nor performs CONF-09 | ✓ VERIFIED | Diff scope is exactly `pinn/training/validation_gate.py`, `pinn/train.py`, `pinn/training/summary.py`, and the two named test files — no CONF-01/CONF-08/probe/evidence file touched; `RATIFIED_VALIDATION_FRAME`'s definition (`validation_gate.py:788`) is outside the diff. |
| 7 | (backstop) CONF-01 edge contracts (adjacency/empty/ordering/concurrency) remain covered | ✓ VERIFIED | `pinn/verification/target_frame_probe.py` byte-identical; the pre-existing CONF-01 test suites (46-02/46-04/46-06/46-09) are part of the 151-passed, 0-failed Phase 46 run with no test deleted or weakened in that area. |
| 8 | (backstop) CONF-08 edge contracts (idempotency, no second writer) remain covered | ✓ VERIFIED | `pinn/data/adapter.py`/`preprocessing.py` byte-identical; no new writer or parallel preprocessing path introduced (diff touches only the training/validation-gate/summary seam, never the data pipeline). |
| 9 | INST-01 adjacency/empty/ordering edges are executable regressions | ✓ VERIFIED | `StrictStepIdentityTests` (adjacency), `test_missing_and_empty_stream_retain_none_projection` (empty/absent), `LatestEventMonotonicityTests` (physical-latest authority, no sort/fallback) — all directly executed and pass. |

No truth in this phase is left ⚠️ PRESENT_BEHAVIOR_UNVERIFIED. Every state-transition/ordering-invariant truth (latest-event monotonicity, identity binding, semantic recomputation) was confirmed by directly running its specific test class — not inferred from a green full-suite count alone — and, for the type-aliasing claim specifically, by hand-executing `_json_scalar_equal` against the live module.

## Required Artifacts

All 22 unique PLAN artifacts across the phase exist, are substantive, and are now functionally complete (the three previously DEFECTIVE artifacts are fixed; no new unique artifact paths were introduced by Plan 46-10 since its five declared files were already in the 22-artifact set from earlier plans).

| Artifact group | Level 1–3 | Level 4 / functional status |
|---|---|---|
| `tests/phase46/__init__.py`, `_fixtures.py`, `test_fixtures_selfcheck.py` | ✓ exists, substantive, used | ✓ dataset-free fixture data flows into all Phase 46 suites |
| `pinn/verification/target_frame_probe.py`, probe/evidence tests | ✓ exists, substantive, CLI/tests wired | ✓ unchanged; owner-qualified evidence stands |
| `pinn/data/preprocessing.py` fields, `pinn/data/adapter.py`, pairing tests | ✓ exists, substantive, wired | ✓ unchanged; 1651/1651 pairing evidence stands |
| Pre/post `raw.json`, `summary.md`, `46-VERDICT*.md` | ✓ present, non-empty | ✓ unchanged |
| `pinn/training/validation_gate.py` | ✓ exists, substantive, called from training hook | ✓ **FIXED**: full semantic/contextual validator, payload-derived compact fields |
| `pinn/train.py` | ✓ gate seam called at existing cadence | ✓ **FIXED**: every validation event persists, including nonfinite/failed |
| `pinn/training/summary.py` | ✓ persisted fields projected | ✓ **FIXED**: physical-latest-event selection, hardened identity-bound eligibility |
| `test_artifacts.py`, `test_validation_wiring.py` | ✓ substantive and runnable | ✓ **STRENGTHENED**: `StrictStepIdentityTests`, `SemanticInvariantTests`, `IdentityBindingTests`, `PayloadDerivedCompactFieldsTests`, `LatestEventMonotonicityTests`, `Eval01IdentityBindingTests` added; one prior fixture (`NonFiniteRetentionTests._non_finite_observation`) was rebuilt from a hand-forced impossible payload shape to a genuinely `gate_metrics`-derivable one (a necessary consequence of the new strict-recomputation validator, verified as a strengthening not a weakening by reading the before/after assertions) |

## Key Link Verification

All 25 declared links across the phase are now WIRED and functionally complete (the three previously PARTIAL/FAILED links are fixed by Plan 46-10; `gsd-tools query verify.key-links` returns 0/0 for this plan because its frontmatter uses freeform prose link descriptions rather than the structured `from/to/via` schema — links were verified manually against source).

| From | To | Status | Details |
|---|---|---|---|
| `validation_gate.compact_validation_fields` | published sidecar | ✓ WIRED (fixed) | Now resolves/proves containment (`Path.resolve()` + `relative_to()`), loads the payload, and delegates to `compact_validation_fields_from_payload` with the call's own run/step/path as the expected identity — payload-derived, never the caller's differing observation. |
| `summary._eval01_precondition_iii` | sidecar validator | ✓ WIRED (fixed) | Resolves the run-relative candidate under `Path(path).resolve().parent`, proves containment, loads and validates the payload, and compares all eight `gate_*` fields to the payload projection with `_json_scalar_equal` (type-AND-value). |
| `train._append_validation_record` | same `validation.jsonl` stream | ✓ WIRED (fixed) | The early-return-without-append branch is removed; every event (finite, NaN, ±Inf, failed) reaches the single terminal append. |
| All remaining PLAN links | declared consumers | ✓ WIRED | Unchanged; confirmed by source inspection and the passing regression suite. |

## Data-Flow Trace

| Artifact | Data | Source | Status |
|---|---|---|---|
| CONF-01 evidence | 1,651 trajectory arm/control rows | unchanged manifest/adapter/preprocessing readers | ✓ FLOWING (unchanged) |
| CONF-08 residents | ordered COM/boost positions and velocities | unchanged `preprocess_trajectory` → adapter → resident tensors | ✓ FLOWING (unchanged) |
| Validation sidecar | per-trajectory `{record_key, eps_h, scs}` | `StageIndex` → model → `gate_metrics` (unchanged computation) | ✓ FLOWING |
| `validation.jsonl` compact fields | aggregate/pointer fields | sidecar publication → `compact_validation_fields_from_payload` | ✓ **BOUND** (previously ⚠️ UNBOUND) — every field is now proved to originate from the validated payload at the exact expected identity |
| `summary.json` eligibility | latest physical record + its bound sidecar | `_read_latest_validation_event` → `_eval01_precondition_iii` | ✓ **FAIL-CLOSED** (previously ✗ STALE/UNCONTAINED ACCEPTANCE) — cross-run, wrong-step, forged, malformed, torn, undecodable, and stale-fallback paths all reproducibly return `False`/ineligible |

## Prohibitions

All prohibition statements across the phase (46 previously satisfied + 3 new from Plan 46-10) are satisfied. The one previously-observed violation — 46-07's "instrumentation failure always marks the run ineligible" — is closed: the non-finite/malformed-latest reproductions now leave the failure current, never an older success.

Plan 46-10's three prohibitions:

| Statement | Verification tier | Disposition |
|---|---|---|
| No held-out evaluator invoked/modified/imported into training | test | ✓ RESOLVED — `tests/phase46/test_isolation.py` (unchanged AST-scan + fresh-subprocess enforcement) passes 12/12, directly executed this pass. |
| No training run, validation probe, real-corpus access, probe rewrite, extra probe directory, tuning, cadence/framework-spec change, or new owner verdict | judgment | ✓ RESOLVED (agent judgment, corroborated by objective evidence) — `git diff ea8cd213..HEAD --name-only` (unfiltered) lists exactly 9 files: two plan/summary docs, `46-REVIEW.md`, `ROADMAP.md`, `STATE.md`, and the 5 plan-owned source/test files. No `pinn_instruction/`, dependency/lockfile, or evidence-directory file appears. This is an objective diff check, not a subjective call, but per the judgment-tier protocol it is flagged here for the record rather than silently absorbed into a passed status. |
| No CONF-09 rotation/scaling or broader canonical-frame repair pulled forward | judgment | ✓ RESOLVED (agent judgment, corroborated by objective evidence) — `pinn/data/adapter.py`, `pinn/data/preprocessing.py` are byte-identical to the prior verification pass; `RATIFIED_VALIDATION_FRAME`'s assignment is outside the diff. Flagged here for the record per the judgment-tier protocol. |

Confirmed negative boundaries (unchanged from the prior pass, re-checked): no dependency/lockfile change; no framework-spec edit under `pinn_instruction/`; no new probe run or probe directory; no host path in evidence.

## Requirements Coverage

| Requirement | Source plans | Status | Evidence |
|---|---|---|---|
| CONF-01 | 46-01, 02, 04, 06, 09 | ✓ SATISFIED — QUALIFIED (unchanged) | RG-02 settled by GAP-46-06 owner instruction on measured evidence; the mandatory qualification is preserved and confirmed untouched by Plan 46-10. |
| CONF-08 | 46-08, 09 | ✓ SATISFIED (unchanged) | Exact resident pairing and COM/boost repair; `plus_permutation=0.0` for 1651/1651; files byte-identical since the repair landed. |
| INST-01 | 46-01, 03, 05, 07, 10 | ✓ SATISFIED | Both previously-blocking receipt/eligibility defects are closed with root-cause fixes and executable regressions (not test-only patches): semantic recomputation validation, payload-bound compact fields, persistent non-finite/failed events, and physical-latest-line eligibility with no older-record fallback. |

No orphaned Phase 46 requirement exists. CONF-09 remains correctly mapped to Phase 47 (GAP-46-07, `RESOLVED-WITH-INSTRUCTION`) and is not folded back into this verdict.

## Independent Adversarial Reproduction (this verification pass)

Beyond re-reading the code and the code-reviewer's own adjudication, this pass independently executed the following against the live module (not merely reading assertions):

| Check | Method | Result |
|---|---|---|
| Type-AND-value equality on the eight compact fields | Direct call: `_json_scalar_equal(False, 0)`, `(True, 1)`, `(1, 1.0)`, `("1", 1)` | All `False` (correctly rejected); `_json_scalar_equal(1.0, 1.0)` is `True` (correctly accepted) |
| Cross-run/traversal pointer rejection | Ran `Eval01IdentityBindingTests::test_cross_run_traversal_pointer_rejected` and `test_wrong_step_pointer_with_renamed_donor_sidecar_rejected` directly | Both pass — `eval01_precondition_iii` is `False` even when the donor payload is copied to the victim's own canonical path (its internal `run_dir`/`sidecar_path` fields still name the donor run) |
| One-at-a-time compact-field tamper detection | Ran `test_one_at_a_time_gate_field_mismatch_rejected` (8 subtests, one per `gate_*` key) | All 8 pass |
| Latest-event non-fallback (torn/non-mapping/blank/undecodable/failed/nonfinite) | Ran `LatestEventMonotonicityTests` (7 tests) directly | All pass, including the `bbc398b` `UnicodeDecodeError` fix |
| Semantic recomputation (frame/split/status/step/stage all individually rejected) | Ran `SemanticInvariantTests` (23 tests, incl. bool-alias/duplicate-key/wrong-scs/wrong-aggregate/wrong-verdict mutations) directly | All pass |
| Strict step identity (WR-01) | Ran `StrictStepIdentityTests` directly | All pass — bool/float/string/negative steps raise before filename conversion |
| Evaluator-import isolation unaffected | Ran `test_isolation.py` directly | 12/12 pass |
| Containment uses resolved paths, not string prefixes | Read `validation_gate.py:741-747`/`summary.py:287-289` | Confirmed: both sites use `Path.resolve()` then `relative_to()`, which is symlink-and-`../`-safe |
| Full Phase 46 regression | `pytest tests/phase46/ -q -rs` (run once, per Step 7b's single-full-run constraint) | 151 passed, 68 subtests passed, 0 failed, 0 skipped — matches the independently-measured orchestrator baseline exactly (up from 114 pre-46-10) |
| Diff scope / no dependency or framework-spec drift | `git diff ea8cd213..HEAD --name-only`, `git status --short` | Exactly the 9 expected files; clean tree for the phase's owned paths |

No check that "cannot fail" was found in the 46-10 diff — every test class exercised above operates on a freshly published real payload/record via the actual production functions (`compute_validation_gate`, `publish_gate_sidecar`, `compact_validation_fields`, `_append_validation_record`, `finalize_summary`) and asserts a specific rejection, not a vacuous non-crash.

## Anti-Patterns

No unreferenced `TBD`, `FIXME`, or `XXX` marker was found in the files this plan touched. No empty implementation, hardcoded stub-return, or orphan artifact was found. One informational finding from the code review (`IN-46-10-01`, duplicated but behaviorally-equivalent narrower type-check in `summary.py` vs. `validation_gate.py`'s shared helper) is low-priority maintainability debt, not a defect — `record` is always `json.loads` output, which only ever produces `int`/`float`/`bool`, so the narrower check is exactly equivalent at this call site.

## Documentation Staleness (informational, non-blocking)

`ROADMAP.md`'s Phase 46 success-criterion #3 prose still reads "Plan 46-10 is pending" — the "Plans:" progress line and phase-status table were updated by commit `156943f3` to `10/10`, but the success-criteria narrative text under criterion 3 was not refreshed to describe the closure. This is stale documentation, not a functional gap; it does not affect any of the 70 verified must-haves and is not modified by this verification per its scope (VERIFICATION.md only). Flagged for the orchestrator's awareness.

## Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| Phase 46 focused suite (full, run once) | `"$PY" -m pytest tests/phase46/ -q -rs` | `151 passed, 68 subtests passed`, zero skips, zero fails | ✓ PASS |
| `Eval01IdentityBindingTests` | `"$PY" -m pytest tests/phase46/test_validation_wiring.py::Eval01IdentityBindingTests -q -rs` | `3 passed, 8 subtests passed` | ✓ PASS |
| `LatestEventMonotonicityTests` | `"$PY" -m pytest tests/phase46/test_validation_wiring.py::LatestEventMonotonicityTests -q -rs` | `7 passed` | ✓ PASS |
| `SemanticInvariantTests` + `StrictStepIdentityTests` + `IdentityBindingTests` + `PayloadDerivedCompactFieldsTests` | `"$PY" -m pytest tests/phase46/test_artifacts.py::SemanticInvariantTests tests/phase46/test_artifacts.py::StrictStepIdentityTests tests/phase46/test_artifacts.py::IdentityBindingTests tests/phase46/test_artifacts.py::PayloadDerivedCompactFieldsTests -q -rs` | `23 passed, 28 subtests passed` | ✓ PASS |
| `test_isolation.py` | `"$PY" -m pytest tests/phase46/test_isolation.py -q -rs` | `12 passed` | ✓ PASS |
| Type-sensitive equality direct execution | `_json_scalar_equal(False, 0)` etc. via `python -c` against the live module | `False`/`False`/`False`/`False`/`True` as expected (see table above) | ✓ PASS |
| Diff hygiene | `git diff ea8cd213..HEAD --name-only` (unfiltered) + `git status --short` | Exactly 9 expected files; clean owned-path tree | ✓ PASS |

No training run, evaluation run, server, or stateful production command was executed. `tests/phase41/`, `tests/phase42/`, and `tests/phase43/test_summary_enrichment.py` were not re-run in this pass (per the orchestrator's independently-measured, unchanged baseline: 228 passed/3 skipped and 5 passed respectively); `tests/phase43/`'s other 12 failures are pre-existing/environmental (`test_pilot_calibration.py` x2, `test_smoke.py` x1, `test_verdict_grounding.py` x7, `test_verify_gate.py` x2) and are not Phase 46 defects.

## Probe Execution

| Probe | Command | Status | Reason |
|---|---|---|---|
| CONF-01 real-corpus target-frame probe | not re-run | SKIPPED BY CONTRACT | Plan 46-09/SCOPE-29 permit exactly one completed post-repair measurement; Plan 46-10 touched no probe file and created no new evidence directory (confirmed: `git status --short` on `evidence/` is empty). Re-running would violate the phase contract. |

## Gaps Summary

None. Both gaps from the prior verification pass are closed with root-cause fixes and directly-executed adversarial regressions, not test-only patches or documentation claims. No regression was found in the previously-passing 57 truths, 22 artifacts, or 25 key links (files outside Plan 46-10's five owned source/test files are byte-identical to the prior pass). One informational documentation-staleness item and one low-priority maintainability note are recorded above for completeness; neither blocks the phase goal.

---

_Verified: 2026-07-30T05:10:00Z_
_Verifier: the agent (gsd-verifier)_
