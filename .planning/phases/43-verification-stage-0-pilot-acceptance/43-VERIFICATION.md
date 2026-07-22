---
phase: 43-verification-stage-0-pilot-acceptance
verified: 2026-07-22T13:01:06Z
status: gaps_found
score: 2/6 must-haves verified
behavior_unverified: 0
overrides_applied: 0
gaps:
  - truth: "ACC-01: the verify ladder and smoke-derived duration gate safely gate real long runs"
    status: failed
    reason: "CR-03 and CR-04 are reproducible authorization bypasses: the duration gate fingerprints the requested runtime before strict CPU/fp64 resolution, and a five-entry marker with arbitrary duplicate rung names is accepted as green."
    artifacts:
      - path: "pinn/train.py"
        issue: "_check_duration_gate uses config.run.precision/device at lines 448-450, while the effective strict-CPU RuntimeSpec is resolved later at lines 475-482 and 686-688."
      - path: "pinn/verify.py"
        issue: "ladder_is_green checks only record count and truthy passed values; marker freshness does not validate schema version, exact rung names, order, uniqueness, or boolean types."
    missing:
      - "Resolve the effective immutable RuntimeSpec before duration authorization and use it for calibration, marker, and model construction."
      - "Validate the complete verify-marker schema and exact ordered LADDER records before accepting freshness."
  - truth: "ACC-02: the real smoke contract is formally accepted and repository-compatible"
    status: failed
    reason: "Real smoke/resume/timing artifacts exist and focused artifact tests pass, but REQUIREMENTS.md still marks ACC-02 Pending; the repository-wide launch-fixture regression also remains disclosed and non-green."
    artifacts:
      - path: ".planning/REQUIREMENTS.md"
        issue: "ACC-02 is unchecked at line 88 and Pending in the traceability table at line 189."
      - path: "runs/stage0-smoke"
        issue: "The run proves 300 steps, resume, checkpoints, and timing, but does not close the formal requirement or the older Phase 41/42 fixture regressions."
    missing:
      - "Resolve the ACC-02 Pending state from verified evidence through the owning workflow."
      - "Restore repository-wide compatibility for fresh-launch fixtures without weakening the production duration gate."
  - truth: "ACC-03: one held-out evaluation is durably enforced and renders the acceptance gate"
    status: failed
    reason: "The final receipt correctly renders FAIL, but CR-01 and CR-02 show the once-only invariant is not enforced: alternate output directories bypass the receipt check, and no atomic run-level claim exists before held-out access."
    artifacts:
      - path: "pinn/evaluate.py"
        issue: "_validate_output_dir accepts any path beneath runs/, and the receipt is checked/written only in the caller-selected directory. The receipt is written after test-index access, all forward passes, and metric writes."
      - path: "runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json"
        issue: "The completed receipt is valid evidence of the final invocation, but it cannot prevent another output-path replay or account atomically for a crash/concurrent attempt."
    missing:
      - "Require the canonical <run>/evaluation output and a fixed run-owned attempt/receipt path."
      - "Claim the held-out budget atomically before first access and preserve failed/abandoned attempts."
  - truth: "ACC-04: the enriched end-of-run summary contract is formally accepted"
    status: failed
    reason: "The production seed-42 summary contains real final loss, validation, curriculum, held-out preview, comparison guidance, and honesty text, but REQUIREMENTS.md still marks ACC-04 Pending."
    artifacts:
      - path: ".planning/REQUIREMENTS.md"
        issue: "ACC-04 is unchecked at line 90 and Pending in the traceability table at line 191."
      - path: "runs/stage0-pilot-seed42/summary.md"
        issue: "The artifact is substantive and refreshed with the final FAIL metrics, but the requirement has not been closed by the owning requirements workflow."
    missing:
      - "Resolve the ACC-04 Pending state from the verified production summary evidence through the owning workflow."
  - truth: "The ACC-06 grounding backstop validates the cited receipt rather than only citation text"
    status: failed
    reason: "CR-05 is reproducible: the current test never opens the receipt. An in-memory verdict changed to gate PASS / verdict go / owner_decision go still passes while citing the actual FAIL receipt."
    artifacts:
      - path: "tests/phase43/test_verdict_grounding.py"
        issue: "Hand-written frontmatter parsing and string-presence checks do not compare receipt gate, metrics, digests, or a real calendar date with the verdict."
      - path: ".planning/phases/43-verification-stage-0-pilot-acceptance/43-VERDICT.md"
        issue: "The current document manually matches the receipt and records owner adjust, but its claimed parser-level protection is inadequate."
    missing:
      - "Parse typed YAML and an actual ISO date, load the cited receipt, and compare gate, metrics, digests, and allowed owner decision."
      - "Add receipt-mismatch, quoted-YAML, and invalid-date regressions."
---

# Phase 43: Verification, Stage-0 Pilot & Acceptance Verification Report

**Phase Goal:** The slice is proven: the verify ladder + smoke test gate real runs, the `evaluate` script renders the binary acceptance gate, the Stage-0 pilot calibrates the owner-carved thresholds, and the milestone closes with a go / adjust / rethink verdict on whether to build the full multi-stage platform.

**Verified:** 2026-07-22T13:01:06Z  
**Status:** gaps_found  
**Re-verification:** No — initial verification

## Goal Achievement

Phase 43 has strong execution evidence, but the phase goal is not achieved safely enough to close. The smoke, three-seed pilot, final FAIL receipt, owner `adjust` verdict, and forward handoff are real. However, five code-review BLOCKERs remain reproducible, ACC-02 and ACC-04 remain Pending, and the repository-wide suite is red. The focused green suites do not exercise the authorization bypasses.

### Observable Truths

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | ACC-01 — the ordered ladder and measured-duration gate safely authorize only verified long runs | ✗ FAILED | Ladder/gate artifacts are wired, but CR-03 fingerprints requested rather than effective strict-CPU runtime and CR-04 accepts a forged five-record marker. |
| 2 | ACC-02 — the real 32-trajectory/300-step smoke survives interruption/resume and supplies accepted timing evidence | ✗ FAILED | `runs/stage0-smoke` is real and the 4 smoke artifact checks pass, but ACC-02 remains Pending and shared launch-fixture compatibility remains red. |
| 3 | ACC-03 — the held-out set is evaluated once and the binary physics gate is rendered honestly | ✗ FAILED | Final receipt is `FAIL` at `eps_H=237.2086056078468`, `SCS=2.3751304405952904`, 1,500 trajectories; CR-01/CR-02 defeat the once-only guarantee. |
| 4 | ACC-04 — the production summary reports all required sections and is formally accepted | ✗ FAILED | Seed-42 `summary.md` contains all required real sections and honesty statements, but ACC-04 remains Pending. |
| 5 | ACC-05 — 2–3 real seeds calibrate owner-carved guard/recovery values without dropping failures | ✓ VERIFIED | Seeds 41/42/43 all finished 300 steps; raw spread and confidence are recorded; owner values `1e11`, `0.05`, `0.7`, and `0` load from supported config. |
| 6 | ACC-06 — the owner renders go/adjust/rethink and the handoff separates shipped/seam/deferred work | ✓ VERIFIED | Owner signed `adjust` on 2026-07-22: retain the mechanical Stage-0 slice, block full-platform expansion, investigate failed physics gate/nonconvergence. `pinn/STATUS.md` leaves PLAT-01..07 deferred. CR-05 remains a separate blocking weakness in the automated grounding backstop. |

**Score:** 2/6 truths verified (0 present-but-behavior-unverified)

The four ROADMAP success criteria inherit these results: criteria 1 and 2 fail; criterion 3 is verified; criterion 4 is verified as an owner decision and handoff, with CR-05 still blocking phase closure as an artifact-quality gap.

## Required Artifacts

| Artifact | Expected | Status | Details |
| --- | --- | --- | --- |
| `pinn/verify.py` | Five-rung ladder and fresh marker | ✗ UNSAFE | 583 substantive lines and production-wired, but marker validation is forgeable (CR-04). |
| `pinn/train.py` | Real-data smoke composition and duration gate | ✗ UNSAFE | Smoke/data/timing flow is wired; effective-runtime mismatch defeats the authorization contract (CR-03). |
| `pinn/evaluate.py` | One-time held-out evaluator | ✗ UNSAFE | Real final receipt exists, but output-path replay and pre-claim race/crash gaps violate the single-use contract (CR-01/02). |
| `pinn/verification/gate_metrics.py` | Binary eps_H/SCS metric | ✓ VERIFIED | Final artifacts use the strict gate and agree on FAIL; no metric-formula blocker was reported after the MPS-to-CPU repair. |
| `runs/stage0-smoke/` | Real smoke, resume, checkpoints, timing | ✓ PRESENT | Finished run, checkpoints 100/158/200/300, positive timing, valid calibration. Formal ACC-02 status is still Pending. |
| `runs/stage0-pilot-seed{41,42,43}/` | Three real pilot runs | ✓ VERIFIED | All finished 300/300 finite steps with checkpoints and retained evidence. |
| `runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json` | Final held-out receipt | ✓ VERIFIED | `FAIL`; exact metrics and input digests match `43-VERDICT.md`. No evaluator retry was performed during verification. |
| `runs/stage0-pilot-seed42/summary.md` | Enriched completed-run summary | ✓ PRESENT | Real final losses, validation, curriculum, FAIL preview, comparison hint, and three honesty notes. Formal ACC-04 status is still Pending. |
| `43-CALIBRATION.md` | Seed band and owner ratification | ✓ VERIFIED | Raw observations, exact spread math, confidence limits, candidates, and dated exact values are present. |
| `43-VERDICT.md` | Owner decision and evidence matrix | ✓ VERIFIED | Current content manually agrees with the final receipt and records `adjust`; its automated grounding test is inadequate (CR-05). |
| `pinn/STATUS.md` | FUT-01/FUT-04 handoff | ✓ VERIFIED | Shipped/seam/deferred inventory is explicit; Stage 1 and PLAT-01..07 remain blocked. |

The automated artifact query reported `runs/<run>/splits.json` missing because the plan uses a placeholder path. Real non-empty manifests exist at all smoke/pilot run directories; manual inspection supersedes that placeholder-path false negative.

## Key Link Verification

| From | To | Via | Status | Details |
| --- | --- | --- | --- | --- |
| `pinn/verify.py` | `pinn/train.py` | fresh marker authorization | ✗ PARTIAL | Imported/used, but CR-03/04 make the authorization identity and marker schema unsafe. |
| `pinn/train.py` | `runs/.calibration/stage0-timing.json` | measured s/step forecast | ⚠ PARTIAL | Real calibration flows, but strict-CPU launches can consult the wrong requested-runtime fingerprint. |
| `pinn/train.py` | `pinn/data/adapter.py` / split manifests | admitted CPU/fp32 source | ✓ WIRED | Real smoke/pilot execution proves data reaches training. |
| `pinn/evaluate.py` | persisted `splits.json` | `StageIndex.from_split(..., "test")` | ⚠ PARTIAL | Real data reached the final receipt, but no canonical atomic one-use claim protects the link. |
| `pinn/evaluate.py` | `pinn/training/summary.py` | post-receipt refresh | ✓ WIRED | Seed-42 production summary contains the exact receipt metrics and FAIL verdict. |
| `configs/stage0-example.yaml` | `CurriculumController` | validated `recover_retries` | ✓ WIRED | Exact owner value `0` reaches the controller; config spot-check passed. |
| `43-VERDICT.md` | final receipt | cited receipt/digest/metric parity | ⚠ PARTIAL | Current values match manually, but the regression test checks only strings and can approve a mismatched go. |

## Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| --- | --- | --- | --- | --- |
| Smoke summary/timing | losses, validation, s/step | real admitted Stage-0 run | Yes | ✓ FLOWING |
| Pilot calibration | three per-seed observations and spread | real run summaries/log hashes | Yes | ✓ FLOWING |
| Evaluation metrics | per-trajectory `eps_H`, aggregate SCS/gate | frozen seed-42 split/checkpoint | Yes — 1,500 trajectories | ⚠ FLOWING BUT SINGLE-USE UNSAFE |
| Completed summary | final losses, validation, curriculum, test preview | persisted run + committed metrics | Yes | ✓ FLOWING |
| Verdict | gate, metrics, seed band, thresholds | receipt/calibration/smoke/handoff | Yes, manually matched | ⚠ TEST BACKSTOP INCOMPLETE |

## Final Held-Out Evaluation Boundary

No evaluator or held-out-data command was invoked during this verification.

| Attempt | Recorded result | Verification disposition |
| --- | --- | --- |
| 1 | Failed before held-out split access due missing blacklist wiring | Preserved in `43-VERDICT.md`; no receipt. |
| 2 | Failed during MPS float64 conversion after held-out records/predictions were likely processed | Preserved as a consumed attempt; no receipt, demonstrating CR-02's reachable gap. |
| 3 | Final authorized invocation completed | Receipt preserved at the canonical path; `FAIL`, `eps_H=237.2086056078468`, `SCS=2.3751304405952904`, 1,500 trajectories. |

The evaluator budget is exhausted. No retry is authorized.

## Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| --- | --- | --- | --- |
| Smoke/pilot/verdict artifact checks | `python -m unittest tests.phase43.test_smoke.RealSmokeArtifactTests tests.phase43.test_pilot_calibration tests.phase43.test_verdict_grounding -v` | 17 tests, OK | ✓ PASS, but CR-05 shows the verdict tests are insufficient |
| Alternate evaluator output path validation | Read-only Python call to `_validate_output_dir(runs/.../evaluation-alt)` | `alternate_output_accepted=True` | ✗ FAIL (CR-01) |
| Forged marker validation | Read-only Python call with five duplicate `not_a_rung` records | `forged_marker_accepted=True` | ✗ FAIL (CR-04) |
| Receipt-mismatched go validation | In-memory mutation to `gate: PASS`, `verdict: go`, `owner_decision: go` while retaining FAIL receipt citation | `receipt_mismatched_go_accepted=True` | ✗ FAIL (CR-05) |
| Final receipt parity | `jq` receipt fields + `shasum -a 256` over receipt/metrics/summaries | Exact verdict metrics and recorded hashes match | ✓ PASS |
| Phase 43 complete suite | Disclosed execution result; not rerun because it includes evaluator flow | 177/177 green | ✓ PHASE-LOCAL GREEN |
| Standard review focused slice | `43-REVIEW.md` / commit `014ae41` | 111 tests green | ✓ REVIEW SLICE GREEN |
| Repository-wide suite | Disclosed 1,010-test run; not rerun | 24 failures, 10 errors | ✗ REPOSITORY RED |

## Probe Execution

No Phase 43 shell probe is declared. Step 7c is not applicable. The final evaluator is an acceptance boundary, not a verifier probe, and was deliberately not rerun.

## Requirements Coverage

| Requirement | Source Plans | Description | Status | Evidence |
| --- | --- | --- | --- | --- |
| ACC-01 | 43-01, 43-04 | Verify ladder and >30-minute gate | ✗ BLOCKED | CR-03/04 defeat safe authorization despite focused tests. |
| ACC-02 | 43-03, 43-06 | Real smoke/resume/timing | ✗ BLOCKED | Real artifacts pass spot-checks, but REQUIREMENTS status remains Pending and repo compatibility is red. |
| ACC-03 | 43-02 | One-time held-out gate | ✗ BLOCKED | Correct final FAIL rendering; CR-01/02 defeat one-time enforcement. |
| ACC-04 | 43-05 | Enriched honest summary | ✗ BLOCKED | Production artifact is present, but REQUIREMENTS status remains Pending. |
| ACC-05 | 43-07 | Three-seed calibration and owner thresholds | ✓ SATISFIED | Three retained seeds, exact spreads, exact active values, dated owner ratification. |
| ACC-06 | 43-08 | Owner verdict and forward handoff | ✓ SATISFIED | Signed `adjust` and complete handoff are real; CR-05 remains a blocker in the claimed automated grounding protection. |

No orphaned Phase 43 requirements were found: ACC-01..06 appear in plan frontmatter and REQUIREMENTS mapping.

## Anti-Patterns and Review Findings

| ID | File | Pattern | Severity | Impact |
| --- | --- | --- | --- | --- |
| CR-01 | `pinn/evaluate.py` | Caller-selected receipt directory | BLOCKER | Single-evaluation replay bypass. |
| CR-02 | `pinn/evaluate.py` | Receipt written after access/work | BLOCKER | Crashes and concurrent attempts can consume held-out access without durable claim. |
| CR-03 | `pinn/train.py` | Requested/effective runtime mismatch | BLOCKER | Wrong calibration/marker can authorize a strict CPU/fp64 run. |
| CR-04 | `pinn/verify.py` | Weak marker schema validation | BLOCKER | Forged ladder records authorize long runs. |
| CR-05 | `tests/phase43/test_verdict_grounding.py` | Citation text treated as receipt validation | BLOCKER | A receipt-mismatched go passes the test. |
| WR-01 | `pinn/verify.py` | Git HEAD ignores dirty source | WARNING | Marker code identity can be stale under uncommitted relevant edits. |
| WR-02 | config/train/evaluate data-root flow | Relative root depends on process CWD | WARNING | Frozen run can resolve a different/missing corpus across working directories. |
| WR-03 | shared launch fixtures | Phase-local green masks repository regression | WARNING | 1,010-test suite has 24 failures and 10 errors. |

No unreferenced `TBD`, `FIXME`, or `XXX` debt marker was found in the Phase 43 implementation/test/evidence surfaces scanned. Empty-list matches in summary/evaluator code are guarded runtime accumulators/read-failure fallbacks, not user-visible stubs. The `PROVISIONAL` constants in `pinn/training/config.py` are overridden by exact active owner values in `configs/stage0-example.yaml`, but remain a reporting/maintenance warning.

## Human Verification Required

None for this report. The owner judgment already occurred and is recorded as `adjust`. The outstanding items are reproducible engineering gaps, not visual or experiential uncertainties.

## Deferred Items

None. `roadmap.analyze` reports no phase after Phase 43 in the current milestone, so none of these gaps can be reassigned to a later milestone phase. PLAT-01..07 remain future work and do not resolve Phase 43's acceptance-safety gaps.

## Gaps Summary

Five grouped gaps block goal achievement: unsafe long-run authorization (CR-03/04), unresolved formal smoke acceptance (ACC-02 Pending), unsafe one-time held-out enforcement (CR-01/02), unresolved formal summary acceptance (ACC-04 Pending), and an inadequate receipt-grounding backstop (CR-05). The owner verdict remains `adjust`: retain the mechanical Stage-0 slice, block full-platform expansion, and investigate the failed physics gate/nonconvergence. This verification does not authorize another held-out evaluation or any full-platform work.

---

_Verified: 2026-07-22T13:01:06Z_  
_Verifier: the agent (gsd-verifier)_
