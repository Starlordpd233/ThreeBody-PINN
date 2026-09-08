---
phase: 57-corrected-re-run-the-preserved-evaluation
plan: "04"
subsystem: verification
tags: [gate04, provenance, production-conformance, evaluator, evidence, unittest]

requires:
  - phase: 57-corrected-re-run-the-preserved-evaluation
    provides: "57-03's strict 4096-row/R_ref runtime binding, frozen monitor, L-BFGS segment, and v2.3 config band"
  - phase: 56-contract-amendment-train-free-gate
    provides: "The architecture probe, governed R_ref schema, and six-case Gate evidence lineage"
provides:
  - "A fresh complete six-case GATE-04 PASS with exact 2:1 spread, fixed alpha reduction, front 15, and perturbed weights at least 0.70"
  - "An independent CPU production-path conformance record bound to the final R_ref and Gate raw-evidence hashes"
  - "Canonical-frame evaluator enforcement, structural-only candidate selection, and Phase-57 append-only evidence tooling"
affects: [57-05, 57-06, RUN-04, RUN-05, EVAL-02]

actuals:
  tokens: 37728
  tasks: 3
  commits: 5
plan_head_before: daefd71a12b83b3aebefe97327f08f2cdd679b63
commits: 5

tech-stack:
  added: []
  patterns:
    - "GATE-04 refresh is fail-closed: only a fresh six-case complete PASS writes the governed R_ref artifact; scientific BLOCK and operational failure remain distinct outcomes."
    - "Independent production evidence validates the public controller/loss/checkpoint seams and records source, allocation, gradient, monitor, segment, resume, and provenance hashes without duplicating recipe arithmetic."
    - "Evaluator access starts with a dataset-free canonical-frame assertion; candidate selection recomputes only the four Phase-50 structural facts in fixed 42/41/43 order."

key-files:
  created:
    - pinn/verification/phase57_production_conformance.py
    - pinn/verification/candidate_eligibility.py
    - .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/production-conformance.json
    - .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/gate04/20260908T093626Z/raw.json
    - .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/build_phase57_evidence.py
    - .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/verify_phase57_evidence.py
    - .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/README.md
    - .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/run-ledger.md
  modified:
    - pinn/verification/gate04_train_free.py
    - pinn/verification/artifacts/r_ref_stage0.json
    - pinn/evaluate.py
    - .planning/phases/57-corrected-re-run-the-preserved-evaluation/deferred-items.md

key-decisions:
  - "The owner-ratified condition-(ii) rule is computed from raw bin means and frozen R_ref, not from a static weight vector: require non-anchor spread >=2, then recompute the all-residual alpha reduction through the production arithmetic."
  - "The fresh Gate raw evidence is the sole provenance source for the refreshed R_ref artifact; its path, digest, schema, six case labels, and complete PASS are all persisted and revalidated."
  - "The production verifier uses a deterministic synthetic training-only StageQuery and the actual RunController path on CPU, proving checkpoint/monitor/L-BFGS state without starting a training run."
  - "The evaluator now passes normalized u=t/T to gate metrics only after the canonical r_prime/u_t_over_T/ordered_raw frame assertion; no held-out materialization occurs before that assertion."

requirements-completed: []

coverage:
  - id: D1
    description: "Fresh exact GATE-04 evidence and governed R_ref satisfy all six-case D-05 facts with empty blocking and unratified arrays."
    requirement: RUN-04
    verification:
      - kind: other
        ref: "pinn/verification/gate04_train_free.py CLI + evidence/gate04/20260908T093626Z/raw.json"
        status: pass
      - kind: unit
        ref: "tests.phase57.test_gate_and_evaluation.Gate04RulingTests (5/5)"
        status: pass
    human_judgment: false
  - id: D2
    description: "Independent final-R_ref production conformance proves exact allocation, normalized loss, gradients, frozen monitor, immutable L-BFGS closure, and exact checkpoint resume."
    requirement: RUN-04
    verification:
      - kind: integration
        ref: "python -m pinn.verification.phase57_production_conformance ... (status=PASS)"
        status: pass
    human_judgment: false
  - id: D3
    description: "Canonical evaluator boundary and Phase-50-equivalent structural evidence surfaces are implemented without held-out access or metric-based fallback."
    requirement: EVAL-02
    verification:
      - kind: unit
        ref: "tests.phase57.test_gate_and_evaluation.EvaluationBoundaryTests + EvidenceSelectionTests + RunFailureClassificationTests (16/16)"
        status: pass
      - kind: other
        ref: "verify_phase57_evidence.py admit-run-window (ADMIT-RUN-WINDOW-OK)"
        status: pass
    human_judgment: false

duration: 45min
completed: 2026-09-08
status: complete
---

# Phase 57 Plan 04: Gate, Production Proof, and Evaluator Boundary Summary

**A fresh complete GATE-04 PASS, final-R_ref-bound production proof, and fail-closed canonical evaluator/evidence boundaries are now committed; RUN-04 remains unspent pending the operator-authorized run window.**

## Performance

- **Duration:** approximately 45 minutes
- **Started:** 2026-09-08T08:45:00Z (execution window; exact gate launch began at 09:36:26Z)
- **Completed:** 2026-09-08T10:01:20Z
- **Tasks:** 3/3
- **Files modified or created:** 13 plan-owned paths, plus the broken-windows ledger entry

## Accomplishments

- Implemented the owner ruling in `gate04_train_free.py`: condition (ii) now requires the measured non-anchor `2:1` spread and recomputes the fixed `alpha = log(2)/(2*P_15)` all-residual reduction through `ratified_causal_weights`. Complete verdicts carry empty blocking and unratified arrays.
- Ran the exact mandated six-case CPU command. Fresh evidence at `evidence/gate04/20260908T093626Z/raw.json` records six cases (`41`, `42`, `43`, `0`, `7`, `41-variable-mass`), `PASS`, `R_ref = 19749775821.24417`, each `front_idx = 15`, `w'_15 ≈ 0.707106781187`, and minimum perturbed weight ≈ `0.707106781187`. The governed artifact records and matches the raw path and SHA-256 `f58ea8f5b60b9b650ec7c958fffb25b117a93cd67abe941dfcda4d1d07986507`.
- Added and ran the independent synthetic CPU production verifier. It exercises the actual `FixedBatch`/`RunController`/loss/checkpoint seams and records exact 4096/16/256 allocation, finite nonzero gradients, frozen training-only monitor with separate `N=500`, immutable L-BFGS segment hashes, exact monitor/segment restore, and final R_ref/Gate provenance.
- Added the canonical-frame assertion before evaluator split materialization and normalized gate-metric time coordinate, plus structural-only candidate selection and append-only Phase-57 evidence builder/verifier scaffolding. No training run, admitted corpus access, or held-out evaluation was launched.

## Task Commits

Each task was committed atomically:

1. **Task 1: Finalize, run, and persist the exact six-case GATE-04 ruling** — `0ccfe855` (`feat(57-04)`)
2. **Task 2: Verify the real production path against the final R_ref** — `73454817` (`feat(57-04)`)
3. **Task 3: Enforce canonical evaluation assembly and port governed evidence tooling** — `0640347c` (`feat(57-04)`)

Follow-up commits required to keep the committed evidence current and wording accurate:

4. **Align the resolved Gate diagnostic wording** — `dda7cf7c` (`fix(57-04)`)
5. **Refresh production evidence on the final code HEAD** — `87e50573` (`verify(57-04)`)

## Validation Evidence

- Exact Gate command under `pinn-train` — **PASS COMPLETE**; fresh raw evidence and governed R_ref provenance match.
- `python -m unittest tests.phase57.test_gate_and_evaluation.Gate04RulingTests -v` — **5/5 passed**.
- `python -m unittest tests.phase57.test_gate_and_evaluation.Gate04RulingTests.test_persisted_complete_pass_and_r_ref_provenance -v` — **1/1 passed**.
- `python -m unittest discover -s tests/phase57 -p 'test_*.py' -v` — **46/46 passed**.
- `python -m pinn.verification.phase57_production_conformance --r-ref-path ... --gate-evidence-root ... --output ...` — **PASS** on the final code state; output records `training_launched: false` and `held_out_evaluation_launched: false`.
- `python .../verify_phase57_evidence.py admit-run-window` — **ADMIT-RUN-WINDOW-OK**; current final HEAD and Gate/conformance/R_ref ancestry are coherent, and target v2.3 run directories are absent.
- Evaluator/selector subset (`EvaluationBoundaryTests`, `EvidenceSelectionTests`, `RunFailureClassificationTests`) — **16/16 passed**.
- The requested Phase-50 adjacent command was attempted. Its 14 tests fail before exercising Phase-50 behavior because this checkout intentionally lacks the old `.planning/phases/50-valid-stage-0-re-run/evidence/build_phase50_evidence.py` path; preserved implementation/evidence is archived under `.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/evidence/`. This pre-existing issue is recorded in `deferred-items.md` and the broken-windows ledger; no archived artifact was copied or changed.
- Evidence verifier commands `run-window`, `candidate`, `pre-evaluation`, and `final` correctly return nonzero while no smoke/band/evaluation exists. They preserve the fail-closed pre-run state and do not create run or held-out artifacts.

## Task-1 Gate Record

- Raw evidence: `.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/gate04/20260908T093626Z/raw.json`
- Raw SHA-256: `f58ea8f5b60b9b650ec7c958fffb25b117a93cd67abe941dfcda4d1d07986507`
- Governed artifact: `pinn/verification/artifacts/r_ref_stage0.json`
- Governed artifact SHA-256: `c3a14924524ec94ad633d7dabe1027d277ba2c1c94d74ad01af2c448b50d73ff`
- Gate verdict: `PASS`, empty `blocking_reasons`, empty `unratified_conditions`
- Evaluation state: `preserved-unspent`

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Documentation mismatch] Updated a stale Gate diagnostic comment after resolving GAP-56-01**

- **Found during:** Task 1 post-commit audit
- **Issue:** The condition-iii diagnostic comment still said GAP-56-01 was OPEN after the owner-ratified rule had landed and the diagnostic status changed to descriptive.
- **Fix:** Updated the comment to identify the sensitivity series as a descriptive companion to the fixed all-residual reduction.
- **Files modified:** `pinn/verification/gate04_train_free.py`
- **Verification:** `git diff --check`; Gate/Phase-57 tests remained green.
- **Committed in:** `dda7cf7c`

**2. [Rule 3 - Out-of-scope blocking issue] Recorded the unavailable archived Phase-50 adjacent regression path**

- **Found during:** Task 3 plan-level verification
- **Issue:** Phase-50 test fixtures invoke `.planning/phases/50-valid-stage-0-re-run/evidence/build_phase50_evidence.py`, which is absent because the completed phase was archived under `.planning/milestones/v2.2-phases/`.
- **Fix:** Added a deferred-items record and a broken-windows `unrun-verify` entry; left archived implementation, tests, and evidence untouched.
- **Files modified:** `.planning/phases/57-corrected-re-run-the-preserved-evaluation/deferred-items.md`, `.planning/WINDOWS.md`
- **Verification:** Phase-57 suite and new evaluator/evidence checks pass; the failure is reproducible before Phase-50 logic runs.
- **Committed in:** deferred to the final metadata commit

**3. [Rule 1 - Evidence freshness] Re-ran the production verifier after Task 3 code landed**

- **Found during:** final plan-level verification
- **Issue:** The first successful conformance record was captured before the evaluator/evidence-boundary commit, so its `git_head` did not identify the final code state.
- **Fix:** Re-ran the exact independent verifier and committed the refreshed record; Gate/R_ref digests and all scientific facts remained identical.
- **Files modified:** `.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/production-conformance.json`
- **Verification:** verifier returned `status=PASS`; admission verifier returned `ADMIT-RUN-WINDOW-OK`.
- **Committed in:** `87e50573`

---

**Total deviations:** 3 (one wording correction, one deferred out-of-scope path issue, one evidence-freshness rerun)
**Impact on plan:** No recipe value was retuned, no dependency was installed, no training was launched, and no held-out data was touched. RUN-04 remains gated on the separate operator-authorized Wave-5 window.

## Auth Gates

None.

## TDD Gate Compliance

The task markers carry `tdd="true"`, but `.planning/config.json` has `workflow.tdd_mode: false`. Plan 57-01 already committed the intentional RED contracts; this plan drove those contracts to green and added the required runtime/artifact checks. No separate RED commit was required for the already-landed tests, and no test framework or package was installed.

## Known Stubs

The empty `run-ledger.md` (`band_generations: []`, `records: []`) is an intentional pre-run scaffold, not a missing implementation: Plan 57-05 owns the operator-authorized smoke/band append. No stub blocks the completed Plan-57-04 gate/conformance/evaluator-boundary objective.

## Next Phase Readiness

- **RUN-04 status:** still blocked from spending compute until Plan 57-05's `admit-run-window` check and explicit operator authorization; this plan did not launch the smoke or band.
- **GATE-04 status:** fresh complete PASS; the governed R_ref artifact is valid and bound to the raw evidence path/hash.
- **Production conformance:** PASS on final code state; its evidence remains training-only and held-out-free.
- **RUN-05/EVAL-02:** not started. The candidate/evidence tooling is ready, and the evaluator fails closed before test-split materialization.
- **Wave 5:** do not start automatically; Plan 57-05 remains the next operator-gated plan.

---
*Phase: 57-corrected-re-run-the-preserved-evaluation*
*Completed: 2026-09-08*

## Self-Check: PASSED

- All plan-owned source, evidence, and summary files exist.
- Task commits `0ccfe855`, `73454817`, `dda7cf7c`, `0640347c`, and `87e50573` are present in git history.
- Fresh Gate raw evidence and the governed R_ref artifact paths/digests match; the independent verifier output is `PASS`.
- `git diff --check` reports no whitespace errors in the committed plan-owned changes.
- Re-checked file existence, all five commit hashes, Gate/R_ref provenance, and production-conformance provenance after writing this summary — all checks passed.
