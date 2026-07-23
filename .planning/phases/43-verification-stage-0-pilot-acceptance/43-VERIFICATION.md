---
phase: 43-verification-stage-0-pilot-acceptance
verified: 2026-07-23T06:18:12Z
status: passed
score: 6/6 must-haves verified
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: 2/6
  gaps_closed:
    - "ACC-01: CR-03 effective strict-CPU runtime now fingerprints the duration gate and smoke calibration (pinn/train.py _effective_runtime_labels)."
    - "ACC-01: CR-04 verify marker now enforces schema version, exact ordered LADDER, strict booleans, and all six fingerprint keys (pinn/verify.py marker_is_green_and_fresh)."
    - "ACC-02: repository-wide launch fixtures (Phase 41/42) and the Phase 39 .txt detector are green; ACC-02 flipped to Complete in REQUIREMENTS.md."
    - "ACC-03: CR-01 output bound to <run_dir>/evaluation; CR-02 atomic O_CREAT|O_EXCL claim before corpus access (pinn/evaluate.py)."
    - "ACC-04: production seed-42 summary formally accepted; ACC-04 flipped to Complete in REQUIREMENTS.md."
    - "ACC-06: CR-05 verdict backstop now parses typed YAML and compares gate/eps_H/SCS/digests against the cited receipt (tests/phase43/test_verdict_grounding.py)."
    - "GAP-43-01 (RESOLVED-WITH-INSTRUCTION, Option A): device-sanity rung proves MPS by materialization, not an availability predicate; Phase 38 prohibition scan passes on pinn/verify.py."
  gaps_remaining: []
  regressions: []
---

# Phase 43: Verification, Stage-0 Pilot & Acceptance Verification Report

**Phase Goal:** The slice is proven: the verify ladder + smoke test gate real runs, the `evaluate` script renders the binary acceptance gate, the Stage-0 pilot calibrates the owner-carved thresholds, and the milestone closes with a go / adjust / rethink verdict on whether to build the full multi-stage platform.

**Verified:** 2026-07-23T06:18:12Z
**Status:** passed
**Re-verification:** Yes — after gap closure (plans 43-09..43-12 and GAP-43-01). The prior report was `gaps_found` (score 2/6, verified 2026-07-22T13:01Z) and PREDATED this closure work.

## Goal Achievement

The phase goal is achieved. All six acceptance requirements (ACC-01..06) are verified against the current code, and every code-review BLOCKER cited by the prior report (CR-01..CR-05) is independently confirmed CLOSED — not by trusting the gap-closure summaries, but by reading the hardened functions, running the exact read-only bypass probes the prior verifier used to demonstrate the bypasses, and running the CR regressions and the previously-red repository suites.

The prior verifier's three reproduced bypasses now REFUSE: `forged_marker_accepted=False` (CR-04), `receipt_mismatched_go_accepted=False` (CR-05), and the alternate-output / non-atomic-claim replay path is refused (CR-01/CR-02) by both code inspection and the named ClosedEvaluationFlow regressions. The device-sanity/Phase-38 conflict (GAP-43-01) is resolved by materialization proof, and the previously-red repository suites (Phase 38/39/41/42) are all green.

**The held-out evaluator was NOT re-run.** ACC-03 is verified by CITING the preserved final receipt at `runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json` and its recorded digests. The evaluator budget is exhausted; no held-out command was invoked during this verification.

### Observable Truths

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | ACC-01 — the ordered ladder and measured-duration gate safely authorize only verified long runs | ✓ VERIFIED | CR-03 CLOSED: `_effective_runtime_labels` (train.py:368-372) feeds both smoke calibration write (train.py:394) and the gate fingerprint (train.py:456-459); `forecast_from_calibration` enforces a full fingerprint match (timing.py:217). CR-04 CLOSED: `marker_is_green_and_fresh` (verify.py:483-536) requires schema version, exact ordered LADDER via `_marker_ladder_is_valid` (verify.py:329-340), strict `passed is True`, all six fingerprint keys + `git_head_available`, and the freshness window. Probes returned `forged/reordered/truthy_nonbool = False`, `genuine_green = True`. Named CR-03 tests pass. |
| 2 | ACC-02 — the real 32-trajectory/300-step smoke survives interruption/resume and supplies accepted timing evidence | ✓ VERIFIED | `runs/stage0-smoke` finished 300 steps with checkpoints at 100/158/200/300 (158 = resume evidence); `runs/.calibration/stage0-timing.json` is `valid`, `s_per_step=0.10190…`, `forecast_seconds=30.57`, full fingerprint. REQUIREMENTS.md ACC-02 is Complete (line 88, table line 189). Repository fixtures now green: phase41 193/193, phase42 38/38, phase39 264/264. |
| 3 | ACC-03 — the held-out set is evaluated once and the binary physics gate is rendered honestly | ✓ VERIFIED (receipt citation; evaluator NOT re-run) | Preserved receipt: `verdict=FAIL`, `eps_h=237.2086056078468`, `scs=2.3751304405952904`, 1,500 trajectories (metrics.json:5 / metrics.md:5), digests match VERDICT.md. CR-01 CLOSED: `evaluate_run` binds output to `<run_dir>/evaluation` and raises `OutputPathEscapeError` otherwise (evaluate.py:341-347). CR-02 CLOSED: `_claim_evaluation_attempt` uses `os.O_CREAT|os.O_EXCL` + fsync before adapter construction (evaluate.py:193-214, called at 364 before adapter at 373), never removed. Four named ClosedEvaluationFlow regressions pass. |
| 4 | ACC-04 — the production summary reports all required sections and is formally accepted | ✓ VERIFIED | `runs/stage0-pilot-seed42/summary.md` contains Validation summary, Curriculum progression, Test-set preview (eps_H 237.21, SCS 2.375, FAIL, 1500 trajectories), comparison hint, and the three honesty statements (lines 24-49). REQUIREMENTS.md ACC-04 is Complete (line 90, table line 191). |
| 5 | ACC-05 — 2–3 real seeds calibrate owner-carved guard/recovery values without dropping failures | ✓ VERIFIED | Seeds 41/42/43 each finished 300/300 steps with retained checkpoints; `43-CALIBRATION.md` records raw per-seed observations, exact spread, HIGH operational confidence (explicitly not a convergence claim), derived R-1/R-2 candidates + D4-a ceiling; owner values `1e11`, `0.05`, `0.7`, `0` load from `configs/stage0-example.yaml`. REQUIREMENTS.md ACC-05 Complete. |
| 6 | ACC-06 — the owner renders go/adjust/rethink and the handoff separates shipped/seam/deferred work | ✓ VERIFIED | `43-VERDICT.md` is owner-signed `adjust` (2026-07-22), grounded in the FAIL receipt; `pinn/STATUS.md` records shipped/seam/deferred inventory (PLAT-01..07 deferred). CR-05 CLOSED: `validate_verdict_grounding` (test_verdict_grounding.py:136-201) parses typed YAML, loads the cited receipt, and compares gate↔receipt-verdict, eps_H/SCS text, three SHA-256 digests, and an ISO date; probe `receipt_mismatched_go_accepted=False`, real verdict validates against real receipt. REQUIREMENTS.md ACC-06 Complete. |

**Score:** 6/6 truths verified (0 present-but-behavior-unverified)

The four ROADMAP Success Criteria inherit these results: criterion 1 (ACC-01/02) verified; criterion 2 (ACC-03/04) verified; criterion 3 (ACC-05) verified; criterion 4 (ACC-06) verified. The verdict remains the owner-signed `adjust` — a FAILing gate honestly rendered, not a "go".

### Per-CR Blocker Disposition

| CR | Prior finding | Current disposition | Evidence personally checked |
| --- | --- | --- | --- |
| CR-01 | Evaluation receipt written in a caller-selected output dir → replay bypass | ✓ CLOSED | `evaluate.py:341-347` computes `canonical_output = <run_dir>/evaluation` and raises `OutputPathEscapeError` when `resolved_output != canonical_output`, before any config/manifest/corpus access. Named test `test_second_evaluation_cannot_redirect_to_an_alternate_output` → OK. |
| CR-02 | Receipt written after held-out access with no atomic claim | ✓ CLOSED | `_claim_evaluation_attempt` (`evaluate.py:179-214`) creates `evaluation-attempt.json` with `os.O_CREAT|os.O_EXCL|os.O_WRONLY`, fsyncs file + dir, and is called (line 364) BEFORE `AdmittedSetAdapter` (373) and `StageIndex.from_split` (379); claim is never removed (`_finalize` rewrites in place, line 241). Named tests `test_attempt_is_claimed_before_test_split_materialization`, `test_post_claim_failure_preserves_attempt_and_refuses_retry`, `test_preexisting_attempt_refuses_a_concurrent_claim` → OK. |
| CR-03 | Duration gate fingerprinted the requested runtime, not the effective strict-CPU runtime | ✓ CLOSED | `_effective_runtime_labels` (`train.py:368-372`) returns `(float64, cpu)` under `strict_cpu_determinism`; used for both smoke calibration write (`train.py:394`) and the gate fingerprint (`train.py:456-459`). Read path `forecast_from_calibration`→`calibration_is_valid` enforces full fingerprint match incl. `git_head_available` (`timing.py:180-192`). Named tests `test_strict_cpu_gate_uses_effective_float64_cpu_fingerprint`, `test_strict_cpu_smoke_calibration_uses_effective_runtime_labels` → OK. |
| CR-04 | Verify marker accepted a forged five-record marker | ✓ CLOSED | `marker_is_green_and_fresh` (`verify.py:483-536`) + `_marker_ladder_is_valid` (`verify.py:329-340`) require the exact ordered `LADDER`, `passed is True` (strict bool), schema version, freshness, and all six `_FINGERPRINT_KEYS`. Read-only probe: forged (5× `not_a_rung`), reordered, and truthy-non-bool markers all → `False`; genuine green → `True`. |
| CR-05 | Verdict-grounding test checked citation text, not the receipt | ✓ CLOSED | `validate_verdict_grounding` (`test_verdict_grounding.py:136-201`) uses `yaml.safe_load`, loads the cited receipt JSON, and raises unless `gate == receipt.verdict`, `eps_h`/`scs`/`checkpoint_sha256`/`config_sha256`/`splits_sha256` all appear in the text, and `owner_decision_date` is a valid ISO date. Read-only probe: PASS/go verdict citing FAIL receipt → rejected ("frontmatter gate PASS does not match receipt verdict FAIL"); real verdict validates against real receipt. |

## Required Artifacts

| Artifact | Expected | Status | Details |
| --- | --- | --- | --- |
| `pinn/verify.py` | Five-rung ladder + fail-closed fresh marker | ✓ VERIFIED | 638 lines; `marker_is_green_and_fresh` enforces the full schema (CR-04 closed); device-sanity rung uses MPS materialization proof, no availability predicate (GAP-43-01). |
| `pinn/train.py` | Real-data smoke composition + duration gate | ✓ VERIFIED | `_effective_runtime_labels` binds calibration + gate to the executed runtime (CR-03 closed); `_check_duration_gate` fail-closed before run-dir creation; strict `> 1800 s` boundary. |
| `pinn/evaluate.py` | One-time held-out evaluator | ✓ VERIFIED | Canonical `<run_dir>/evaluation` output (CR-01) + atomic O_EXCL pre-access claim (CR-02); manifest-only empty-split refusal before claim. |
| `pinn/verification/gate_metrics.py` | Binary eps_H/SCS metric | ✓ VERIFIED | Final artifacts render the strict gate; receipt + summary agree on FAIL. |
| `runs/stage0-smoke/` | Real smoke, resume, checkpoints, timing | ✓ VERIFIED | Checkpoints 100/158/200/300; persisted valid calibration; ACC-02 formally Complete. |
| `runs/stage0-pilot-seed{41,42,43}/` | Three real pilot runs | ✓ VERIFIED | All finished 300/300 with retained checkpoints and evidence. |
| `runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json` | Final held-out receipt | ✓ VERIFIED (cited) | `FAIL`; `eps_h=237.2086…`; `scs=2.3751…`; digests match VERDICT.md. Evaluator NOT re-run. |
| `runs/stage0-pilot-seed42/summary.md` | Enriched completed-run summary | ✓ VERIFIED | All required sections + three honesty statements + FAIL preview; ACC-04 formally Complete. |
| `43-CALIBRATION.md` | Seed band + owner ratification | ✓ VERIFIED | Raw observations, spread math, confidence, candidates, dated exact values. |
| `43-VERDICT.md` | Owner decision + evidence matrix | ✓ VERIFIED | Owner-signed `adjust`; receipt-grounded; CR-05 backstop now adequate. |
| `pinn/STATUS.md` | FUT-01/FUT-04 handoff | ✓ VERIFIED | Shipped/seam/deferred inventory; PLAT-01..07 deferred; GAP-38-01 disposition reflected. |
| `tests/phase43/test_verdict_grounding.py` | Receipt-grounded verdict backstop | ✓ VERIFIED | Typed YAML + receipt-content comparison (CR-05 closed). |

## Key Link Verification

| From | To | Via | Status | Details |
| --- | --- | --- | --- | --- |
| `pinn/verify.py` | `pinn/train.py` | fresh-marker authorization | ✓ WIRED | Gate consumes `read_verify_marker` + `marker_is_green_and_fresh` with the effective-runtime fingerprint; forged/stale markers refused. |
| `pinn/train.py` | `runs/.calibration/stage0-timing.json` | effective s/step forecast | ✓ WIRED | Write and read both keyed on `_effective_runtime_labels`; read enforces full fingerprint match (fail-closed None on mismatch). |
| `pinn/train.py` | `pinn/data/adapter.py` / split manifests | admitted CPU/fp32 source | ✓ WIRED | Real smoke/pilot execution proves data reaches training. |
| `pinn/evaluate.py` | persisted `splits.json` | `StageIndex.from_split(..., "test")` | ✓ WIRED | Canonical output + atomic single-use claim protect the once-only link; manifest empty-split refusal precedes the claim. |
| `pinn/evaluate.py` | `pinn/training/summary.py` | post-receipt refresh | ✓ WIRED | Seed-42 summary carries the exact receipt metrics and FAIL verdict. |
| `configs/stage0-example.yaml` | `CurriculumController` | validated `recover_retries` | ✓ WIRED | Owner value `0` reaches the controller. |
| `43-VERDICT.md` | final receipt | receipt/digest/metric parity | ✓ WIRED | `validate_verdict_grounding` compares gate, eps_H/SCS, and all three digests against the cited receipt. |

## Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| --- | --- | --- | --- | --- |
| Smoke summary/timing | losses, validation, s/step | real admitted Stage-0 run | Yes | ✓ FLOWING |
| Pilot calibration | three per-seed observations + spread | real run summaries | Yes | ✓ FLOWING |
| Evaluation metrics | per-trajectory eps_H, aggregate SCS/gate | frozen seed-42 split/checkpoint | Yes — 1,500 trajectories | ✓ FLOWING (single-use enforced) |
| Completed summary | final losses, validation, curriculum, test preview | persisted run + committed metrics | Yes | ✓ FLOWING |
| Verdict | gate, metrics, seed band, thresholds | receipt/calibration/smoke/handoff | Yes; receipt-grounded backstop | ✓ FLOWING |

## Final Held-Out Evaluation Boundary

No evaluator or held-out-data command was invoked during this verification. ACC-03 was verified by receipt citation and code inspection only.

| Attempt | Recorded result | Verification disposition |
| --- | --- | --- |
| 1 | Failed before held-out split access (missing blacklist wiring) | Preserved in `43-VERDICT.md`; no receipt. |
| 2 | Failed during MPS float64 conversion | Preserved as a consumed attempt; no receipt. |
| 3 | Final authorized invocation completed | Receipt preserved: `FAIL`, `eps_H=237.2086056078468`, `SCS=2.3751304405952904`, 1,500 trajectories. |

The evaluator budget is exhausted. No retry is authorized, and none was performed. (Note: the preserved receipt predates the 43-10 attempt-file hardening, so no `evaluation-attempt.json` exists for that run; the receipt itself is now the single-use guard, since `_assert_evaluation_unclaimed` refuses on an existing receipt.)

## Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| --- | --- | --- | --- |
| Forged/reordered/truthy marker refusal (CR-04) | read-only `marker_is_green_and_fresh` probe | forged/reordered/truthy = False; genuine green = True | ✓ PASS |
| Receipt-mismatched go refusal (CR-05) | read-only `validate_verdict_grounding` probe | rejected: "gate PASS does not match receipt verdict FAIL"; real verdict validates | ✓ PASS |
| CR-03 strict-CPU effective-runtime tests | `unittest ...DurationGateFunctionTests.test_strict_cpu_*` | 2/2 OK | ✓ PASS |
| CR-01/CR-02 once-only enforcement | `unittest ...ClosedEvaluationFlowTests.<4 named>` | 4/4 OK | ✓ PASS |
| Phase 43 focused suite | `unittest discover -s tests/phase43 -p 'test_*.py'` | 198/198 OK (8.9s) | ✓ PASS |
| GAP-43-01 Phase-38 prohibition scan on verify.py | `unittest ...test_no_precision_default_in_discovered_modules` | OK | ✓ PASS |
| Final receipt parity | `cat` receipt + metrics vs VERDICT.md digests | FAIL, 237.21/2.375, 1500, digests match | ✓ PASS |
| Previously-red repository suites | `unittest discover -s tests/phase{38,39,41,42}` | phase38 128, phase39 264, phase41 193, phase42 38 — all OK | ✓ PASS |

## Probe Execution

No Phase 43 shell probe (`scripts/*/tests/probe-*.sh`) is declared for this phase; Step 7c is not applicable. The final evaluator is an acceptance boundary, not a verifier probe, and was deliberately not re-run.

## Requirements Coverage

| Requirement | Source Plans | Description | Status | Evidence |
| --- | --- | --- | --- | --- |
| ACC-01 | 43-01, 43-04, 43-09 | Verify ladder + >30-min gate | ✓ SATISFIED | CR-03/04 closed; effective-runtime gate + full marker schema; REQUIREMENTS Complete. |
| ACC-02 | 43-03, 43-06, 43-12 | Real smoke/resume/timing | ✓ SATISFIED | Smoke 300 steps + resume + valid calibration; repo fixtures green; REQUIREMENTS Complete. |
| ACC-03 | 43-02, 43-10 | One-time held-out gate | ✓ SATISFIED | Canonical output + atomic claim (CR-01/02 closed); FAIL receipt cited; REQUIREMENTS Complete. |
| ACC-04 | 43-05, 43-12 | Enriched honest summary | ✓ SATISFIED | All sections + honesty statements in seed-42 summary; REQUIREMENTS Complete. |
| ACC-05 | 43-07 | Three-seed calibration + owner thresholds | ✓ SATISFIED | Three retained seeds, exact spreads, dated owner ratification. |
| ACC-06 | 43-08, 43-11 | Owner verdict + forward handoff | ✓ SATISFIED | Signed `adjust`; receipt-grounded backstop (CR-05 closed); STATUS.md handoff. |

No orphaned Phase 43 requirements: ACC-01..06 appear in plan frontmatter and the REQUIREMENTS.md traceability mapping (all rows Complete).

## Anti-Patterns and Review Findings

| ID | File | Pattern | Severity | Impact |
| --- | --- | --- | --- | --- |
| CR-01..CR-05 | evaluate.py / train.py / verify.py / test_verdict_grounding.py | (all prior BLOCKERs) | RESOLVED | Confirmed closed by code + probes + regressions (see per-CR table). |
| WR-01 | `pinn/verify.py` | Marker git HEAD ignores a dirty working tree | WARNING (non-blocking) | Documented; the fingerprint + 24 h freshness window is the primary control. Does not defeat any must-have; not a goal blocker. |
| WR-02 | config/train/evaluate data-root flow | Relative data root depends on process CWD | WARNING (non-blocking) | Receipt records the absolute run_dir; fail-closed refusal on a missing corpus rather than a silent wrong-corpus pass. Not a goal blocker. |

No unreferenced `TBD`/`FIXME`/`XXX` debt markers were found in the Phase 43 implementation/test surfaces. `_effective_runtime_labels`, the O_EXCL claim, and the marker schema checks are substantive (not stubs). Empty-container matches are guarded runtime accumulators or synthetic test inputs, not user-visible stubs. The prior WR-03 (repository-red) is resolved: the four previously-red suites are green.

## Human Verification Required

None. The two owner-owned judgment gates for this phase already occurred and are recorded: the R-1/R-2 threshold ratification (`43-CALIBRATION.md`, dated owner values in `configs/stage0-example.yaml`) and the ACC-06 verdict (`43-VERDICT.md`, owner-signed `adjust` 2026-07-22). The SPEC judgment-tier prohibitions (owner ratification, verdict grounded in the gate, assembly-only scope, single-eval discipline) are all satisfied. The remaining items are mechanical engineering checks that were verified programmatically, not visual/experiential uncertainties.

## Deferred Items

None. `roadmap.analyze` reports no phase after Phase 43 in milestone v2.0; no gap can be reassigned to a later phase. PLAT-01..07 remain future work gated on the `adjust` verdict and are correctly recorded as deferred seams in `pinn/STATUS.md`.

## Gaps Summary

No gaps. All six acceptance requirements are verified against the current code; all five prior code-review BLOCKERs (CR-01..CR-05) are independently confirmed CLOSED via code inspection, the exact read-only bypass probes (now refusing), and the named regressions; GAP-43-01 is resolved by MPS materialization proof; and the previously-red repository suites (Phase 38/39/41/42) are green. ACC-03 was verified by citing the preserved FAIL receipt without re-running the exhausted held-out evaluator. The milestone-closing owner verdict remains `adjust`: retain the mechanical Stage-0 slice, block full-platform expansion, and route a separately governed investigation of the failed physics gate and non-convergent pilot behavior. This verification does not authorize another held-out evaluation or any full-platform work.

---

_Verified: 2026-07-23T06:18:12Z_
_Verifier: the agent (gsd-verifier), re-verification after gap closure_
