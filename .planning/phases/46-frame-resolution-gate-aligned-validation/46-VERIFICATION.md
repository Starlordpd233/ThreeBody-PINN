---
phase: 46-frame-resolution-gate-aligned-validation
verified: 2026-07-29T13:19:23Z
status: gaps_found
score: 57/61 must-haves verified
behavior_unverified: 0
overrides_applied: 0
gaps:
  - truth: "EVAL-01 precondition (iii) is true only for the latest persisted gate record and its same-event, contained, semantically valid sidecar"
    status: failed
    reason: "The summary accepts a cross-run ../ sidecar, does not bind the JSONL step or compact fields to the sidecar, and relies on a validator that accepts test-split, failed-status, negative-step, empty-frame payloads."
    artifacts:
      - path: "pinn/training/summary.py"
        issue: "_eval01_precondition_iii joins an arbitrary JSONL path to the run directory and treats shallow validation as eligibility."
      - path: "pinn/training/validation_gate.py"
        issue: "validate_sidecar_payload omits semantic invariants; compact_validation_fields can join a validated sidecar to different in-memory metrics."
      - path: "tests/phase46/test_artifacts.py"
        issue: "The fail-closed suite covers missing keys, truncation, ordering, and metric encoding but not record/artifact identity or semantic invariants."
    missing:
      - "Require a contained, exact step-derived sidecar path and bind JSONL step/schema/metrics/verdict/counts to the validated payload."
      - "Validate the complete frame, split, status, step/stage, path, identity, threshold, count, aggregate, SCS, and verdict invariants."
      - "Derive compact fields from the validated payload or compare them exactly to the observation."
  - truth: "Every latest validation event fails closed and an older eligible record can never remain presented as current"
    status: failed
    reason: "A non-finite validation loss appends no contemporaneous gate record, and a malformed trailing JSONL line is skipped; both leave an older successful gate record reported as current and EVAL-01-eligible."
    artifacts:
      - path: "pinn/train.py"
        issue: "_append_validation_record returns before persisting the gate status when final_val_loss is non-finite."
      - path: "pinn/training/summary.py"
        issue: "_read_jsonl_mappings skips malformed lines and _validation_summary selects the last older parseable record."
      - path: "tests/phase46/test_validation_wiring.py"
        issue: "The test suite explicitly pins the unsafe non-finite early return and has no malformed-latest-line fail-closed case."
    missing:
      - "Persist every validation event with JSON-safe loss/trend representation and contemporaneous gate fields."
      - "Treat a malformed or torn latest JSONL event as ineligible instead of falling back to an older success."
      - "Reverse the non-finite early-return regression and add two-event stale-record tests."
deferred:
  - truth: "Training residency and IC13 share the full locked rotation-gauged, D/V-scaled canonical frame"
    addressed_in: "Phase 47"
    evidence: "CONF-09 and Phase 47 success criteria explicitly move residency to pre.r_gauge/pre.v_gauge and re-ratify the validation frame before CONF-02."
---

# Phase 46: Frame Resolution & Gate-Aligned Validation Verification Report

**Phase Goal:** The last remaining way the next run could be invalid is settled, and validation carries a conservation signal where none exists.
**Verified:** 2026-07-29T13:19:23Z
**Status:** gaps_found
**Re-verification:** No — initial goal verification

## Verdict

Phase 46 does not yet satisfy its complete goal. CONF-01 and CONF-08 are supported by committed evidence and owner rulings, but INST-01's conservation signal is not a fail-closed eligibility receipt. A stale, unrelated, or semantically malformed sidecar can unlock EVAL-01 precondition (iii), and a later invalid validation event can be hidden behind an older eligible record.

The passing UAT, security report, summaries, and 114-test Phase 46 suite were treated as claims to challenge, not proof. Targeted adversarial reproductions confirmed three critical review findings and the step-aliasing warning.

## Goal Achievement

### Roadmap Success Criteria

| # | Roadmap truth | Status | Evidence |
|---|---|---|---|
| 1 | RG-02 is settled by a train-free stored-target residual check with recorded evidence and verdict. | ✓ VERIFIED — QUALIFIED | Two committed runs exist. Pre-repair is `VERDICT_AMBIGUOUS`; post-repair is rule-5 `VERDICT_NON_FRAME_DIVERGENCE`. **RG-02 was owner-settled from measured evidence, not by a clean `VERDICT_TARGETS_ARE_RAW` token.** GAP-46-06 option B relies on scaled-arm median 0.989358 with 1605/1651 separated versus raw-arm median 0.0802249 against controls at 0.0802262, and ratifies `("r_raw", "t_native", "ordered_raw")`. This qualification must travel to Phase 51/EVAL-01 precondition (ii). |
| 2 | The sixth divergence is surfaced as an owner scope decision, never silently absorbed. | ✓ VERIFIED | GAP-46-04/05 route the minimum repair into CONF-08; GAP-46-06 preserves the non-clean machine verdict and records the owner frame ruling; GAP-46-07 routes the separate frame-completion issue to CONF-09/Phase 47. |
| 3 | Per-trajectory ε_H/SCS are computed on validation through `gate_metrics`, persisted per event, and projected fail-closed for EVAL-01 (iii). | ✗ FAILED | The normal data flow exists and focused tests pass, but targeted reproductions show cross-run/unbound sidecars, semantically invalid payloads, and stale older records can still render `eval01_precondition_iii: true`. |
| 4 | Resident series match `masses_ordered`, carry COM/boost gauge, and the unchanged 1,651-record probe is re-run once. | ✓ VERIFIED | `pre.r_com_ordered`/`v_com_ordered` feed adapter residency; Phase 46 pairing tests pass; post-repair evidence has `plus_permutation == 0.0` for 1651/1651, identical controls, matching instrument hash, and exactly one post-repair directory. |

**Roadmap score:** 3/4 criteria verified.

### Every PLAN Must-Have Truth

Truth IDs are their order under each plan's `must_haves.truths`.

| Plan | Truth audit | Result | Evidence / failure |
|---|---:|---|---|
| 46-01 | T1–T8 | 8/8 VERIFIED | Dataset-free fixtures, non-sorted stub, disjoint split pair, dual-frame/degenerate/confound fixtures; fixture and phase suites pass. |
| 46-02 | T1–T9 | 9/9 VERIFIED | Symmetric arms, shared mask, exact boundary/adjacency/empty/ordering/precision contracts, four-way fail-closed classifier; probe tests pass. |
| 46-03 | T1–T8 | 8/8 VERIFIED | Full-pool `gate_metrics` composition, coherent frame pairs, mode restore, ordering, sentinel handling, atomic publication, and truncation protection are present and exercised. Later semantic binding failures are counted under 46-05/07, whose truths make the stronger fail-closed claims. |
| 46-04 | T1–T6 | 6/6 VERIFIED | Manifest intersection/test exclusion, deterministic redacted evidence, sentinels, operational exit semantics, and population mismatch refusal are implemented and tested. |
| 46-05 | T1–T6 | 5/6 VERIFIED | T1–T4 and T6 pass. **T5 FAILED:** semantic corruption is accepted despite the truth that schema validation fails closed on corrupt sidecars. |
| 46-06 | T1–T5 | 5/5 VERIFIED — QUALIFIED | One pre-repair real-corpus run and D-09 routing are recorded. The final RG-02 settlement comes later from GAP-46-06 owner instruction on both measured runs; no clean verdict token is claimed. |
| 46-07 | T1–T7 | 4/7 VERIFIED | T1–T3 and T6 pass. **T4 FAILED:** non-finite validation loss can suppress the failure record. **T5 FAILED:** eligibility is not bound to the latest same-event sidecar. **T7 FAILED:** malformed trailing JSONL falls back to an older eligible record. |
| 46-08 | T1–T6 | 6/6 VERIFIED, with baseline note | Exact pairing/COM/boost repair and additive preprocessing fields are tested; no rotation or D/V scaling. No test was weakened. The repository-wide suite was not rerun here; execution recorded unrelated pre-existing failures, while the complete Phase 46 suite is green with zero skips. |
| 46-09 | T1–T6 | 6/6 VERIFIED | Probe hash matches `997c731b`; population/hashes/controls match; exactly one post-repair run exists; machine verdict and owner routing remain unrounded and separate from the original verdict. |

**Plan truth score:** 57/61 verified. The four failures are all within INST-01's fail-closed persistence/eligibility contract.

## Required Artifacts

All 22 unique PLAN artifacts exist and are substantive. None is a stub or orphan.

| Artifact group | Level 1–3 | Level 4 / functional status |
|---|---|---|
| `tests/phase46/__init__.py`, `_fixtures.py`, `test_fixtures_selfcheck.py` | ✓ exists, substantive, used | ✓ dataset-free fixture data flows into all Phase 46 suites |
| `pinn/verification/target_frame_probe.py`, probe/evidence tests | ✓ exists, substantive, CLI and tests wired | ✓ real corpus flowed into two immutable evidence directories; post-repair token limitation is owner-resolved and qualified |
| `pinn/data/preprocessing.py` fields, `pinn/data/adapter.py`, pairing tests | ✓ exists, substantive, adapter consumes preprocessing fields | ✓ resident arrays flow to materialized tensors/accessors; 1651/1651 evidence confirms pairing |
| Pre/post `raw.json`, `summary.md`, `46-VERDICT*.md` | ✓ all present and non-empty | ✓ hashes, population, controls, and verdict fields independently parsed |
| `pinn/training/validation_gate.py` | ✓ exists, substantive, called from training hook | ✗ DEFECTIVE: semantic validation and record/artifact binding are incomplete |
| `pinn/train.py` | ✓ gate seam called at existing cadence | ✗ DEFECTIVE: non-finite loss can suppress the contemporaneous gate event |
| `pinn/training/summary.py` | ✓ persisted fields projected; validator imported locally | ✗ DEFECTIVE: arbitrary/stale sidecars and malformed latest lines can produce eligibility |
| `test_artifacts.py`, `test_validation_wiring.py` | ✓ substantive and runnable | ⚠ INCOMPLETE: adversarial cases above are absent; one test pins the unsafe early return |

## Key Link Verification

All 25 declared links were located. Twenty-two are functionally complete; three are wired but defective:

| From | To | Status | Details |
|---|---|---|---|
| `validation_gate.compact_validation_fields` | published sidecar | ⚠ PARTIAL | Re-reads and calls the validator, but returns independent observation values and does not bind them to payload identity. |
| `summary._eval01_precondition_iii` | sidecar validator | ✗ FAILED | Imports and calls the validator, but accepts uncontained/cross-run paths and does not compare record to payload. |
| `train._append_validation_record` | same `validation.jsonl` stream | ✗ FAILED on latest invalid event | Normal finite events merge correctly; non-finite loss suppresses the entire contemporaneous record. |
| All remaining PLAN links | declared consumers | ✓ WIRED | Imports/calls/accessor flow were confirmed by source inspection and focused tests. |

## Data-Flow Trace

| Artifact | Data | Source | Status |
|---|---|---|---|
| CONF-01 evidence | 1,651 trajectory arm/control rows | three-manifest train/validation intersection plus adapter/preprocessing control readers | ✓ FLOWING |
| CONF-08 residents | ordered COM/boost positions and velocities | `preprocess_trajectory` → adapter candidate → resident tensors/accessors | ✓ FLOWING |
| Validation sidecar | per-trajectory `{record_key, eps_h, scs}` | validation `StageIndex` → model → existing `gate_metrics` | ✓ FLOWING |
| `validation.jsonl` compact fields | aggregate/pointer fields | sidecar publication → `compact_validation_fields` | ⚠ UNBOUND |
| `summary.json` eligibility | latest record plus sidecar | JSONL reader → sidecar validator | ✗ STALE/UNCONTAINED ACCEPTANCE |

## Prohibitions

All 47 PLAN prohibition statements were audited against source, tests, evidence, and phase history. Forty-six are satisfied. The observable violation is 46-07's prohibition that instrumentation failure always marks the run ineligible: the non-finite/malformed-latest reproductions leave an older eligible record current.

Confirmed negative boundaries include: no training or held-out evaluation run for CONF-01; no `pinn.evaluate` import/invocation/modification; no test-split `StageIndex`; no framework-spec edits; no cadence/config/threshold change; no rotation or D/V scaling in CONF-08; no probe retuning; no extra probe directory; and no host path in committed evidence.

Historical mental-state clauses such as “was not read for behavior selection” cannot be proven from code bytes; the authoritative observable checks show no prohibited edits, imports, citations, or outputs.

## Requirements Coverage

| Requirement | Source plans | Status | Evidence |
|---|---|---|---|
| CONF-01 | 46-01, 02, 04, 06, 09 | ✓ SATISFIED — QUALIFIED | RG-02 is settled by GAP-46-06 owner instruction on measured evidence. Neither evidence run contains a clean raw/scaled machine token. This qualification is mandatory wherever CONF-01 is used for EVAL-01 (ii). |
| CONF-08 | 46-08, 09 | ✓ SATISFIED | Exact resident pairing and COM/boost repair; no rotation/D/V scale; unchanged probe/population re-run once; 1651/1651 `plus_permutation=0.0`. |
| INST-01 | 46-01, 03, 05, 07 | ✗ BLOCKED | Metric computation and normal persistence exist, but fail-closed durable identity/latest-event eligibility does not. |

No orphaned Phase 46 requirement exists. CONF-09 is mapped to Phase 47 and must not be folded back into this verdict.

## Independent Review-Finding Adjudication

| Finding | Independent result | Phase 46 disposition |
|---|---|---|
| CR-01: resident targets and IC13 use different full frames | CONFIRMED by `adapter.py`/`preprocessing.py` | **Deferred, not a Phase 46 defect.** CONF-08 intentionally stops before rotation/D/V; GAP-46-07 owner-routed the remaining training-frame completion to CONF-09/Phase 47. |
| CR-02: post-repair probe lacks the repaired intermediate identity | CONFIRMED by source and post-repair evidence | **Owner-resolved/qualified.** The rule-5 token is preserved. CONF-01 closes through GAP-46-06 option B on arm evidence, not by pretending the token is clean. No probe rewrite/re-run is authorized. |
| CR-03: arbitrary/unbound sidecar can unlock eligibility | CONFIRMED | **BLOCKER — INST-01.** Reproduction: step 999 plus `../donor/...step-00000007.json` returns `True`; compact fields joined sidecar `2e-06` to observation `9.0/FAIL`. |
| CR-04: semantic-invalid sidecar passes validator | CONFIRMED | **BLOCKER — INST-01.** `frame={}`, `split="test"`, `gate_status="failed"`, `global_step=-99`, `stage=-3` is accepted. |
| CR-05: later failures hidden by stale eligible record | CONFIRMED | **BLOCKER — INST-01.** A valid step 7 plus non-finite step 8 leaves one line, reports step 7, and remains eligible; malformed trailing step 9 behaves the same. |
| WR-01: fractional/string steps alias integer artifact names | CONFIRMED | **WARNING.** `1`, `1.9`, and `"1"` all map to `step-00000001.json`. Current training passes integers, but the helper violates its declared contract and weakens evidence identity. |

## Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| Phase 46 focused suite | `"$PY" -m pytest tests/phase46/ -q -rs` | `114 passed, 27 subtests passed in 2.21s`, zero skips | ✓ PASS |
| Existing summary regression suite | `"$PY" -m pytest tests/phase43/test_summary_enrichment.py -q -rs` | `5 passed in 0.89s` | ✓ PASS |
| Review adversarial reproductions | Inline Python using `publish_gate_sidecar`, `compact_validation_fields`, `_append_validation_record`, `_validation_summary`, and `_eval01_precondition_iii` | Cross-run eligible `True`; invalid payload accepted; stale step 7 eligible after invalid steps 8/9; step aliases confirmed | ✗ FAIL |
| Evidence integrity | SHA-256 + JSON parse of both committed `raw.json` files | hashes `3fa8251b…` / `11b6690a…`; verdicts/population/controls match; 1651/1651 repair exact | ✓ PASS |
| Probe identity | current blob vs `git show 997c731b:...` SHA-256 | both `828ed22c…` | ✓ PASS |
| Diff hygiene | `git diff --check` | exit 0 | ✓ PASS |

No training run, evaluation run, server, or stateful production command was executed.

## Probe Execution

| Probe | Command | Status | Reason |
|---|---|---|---|
| CONF-01 real-corpus target-frame probe | not re-run | SKIPPED BY CONTRACT | Plan 46-09 and SCOPE-29 permit exactly one completed post-repair measurement. Re-running it during verification would violate the phase contract. Committed artifacts were independently hash/schema/content checked instead. |

## Anti-Patterns

No unreferenced `TBD`, `FIXME`, or `XXX` marker was found in the Phase 46 implementation/test files. Placeholder-word matches are explanatory docstrings, not stubs. No empty implementation or orphan artifact was found.

The disconfirmation pass found the important anti-pattern instead: tests prove the happy path and selected corruptions but do not prove the stronger eligibility claims; one test explicitly preserves the unsafe non-finite early-return behavior.

## Deferred Item Boundary

Phase 47 owns CONF-09: move residency to `pre.r_gauge`/`pre.v_gauge` and re-ratify the scaled/normalized validation frame before computing `S_H`. This is a real, high-impact issue, but the Phase 46 roadmap and GAP-46-07 explicitly route it forward. It is not one of the Phase 46 blocking gaps.

## Gaps Summary

Two related INST-01 gaps block Phase 46:

1. The sidecar receipt is neither semantically validated nor cryptographically/structurally bound to the JSONL record and run.
2. Latest-event failure is not monotonic: non-finite or malformed latest evidence can expose an older success as current.

Until both close, validation does carry ε_H/SCS data on the normal path, but it does not provide the fail-closed conservation eligibility signal Phase 46 promises.

---

_Verified: 2026-07-29T13:19:23Z_
_Verifier: the agent (gsd-verifier)_
