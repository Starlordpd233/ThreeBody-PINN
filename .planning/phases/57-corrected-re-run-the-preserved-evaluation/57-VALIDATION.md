---
phase: "57"
slug: corrected-re-run-the-preserved-evaluation
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-09-08"
---

# Phase 57 — Validation Strategy

> Per-phase Nyquist contract. Plan 57-01 supplies Wave-0 tests before production edits; `validate-phase` promotes this draft only after those tests and all mapped commands are green.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python stdlib `unittest` only |
| **Environment** | `<home>/miniforge3/bin/conda run -n pinn-train` |
| **Config file** | none dedicated |
| **Quick run command** | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest discover -s tests/phase57 -p 'test_*.py' -v` |
| **Adjacent regression command** | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest tests.phase39.test_batches.CollocationQuotaTests tests.phase39.test_batches.FullBatchContract tests.phase50.test_causal_telemetry.CausalTelemetryOwnershipTests tests.phase50.test_validation_full_pool.ValidationFullPoolTests tests.phase50.test_candidate_finalization.CandidateFinalizationTests tests.phase50.test_evidence_builder.ExtractManifestTests tests.phase50.test_band_record.BandRecordTests tests.phase50.test_evidence_verifier.AttemptVerifierTests -v` |
| **Full validation command** | `/bin/bash -lc 'set -e; <home>/miniforge3/bin/conda run -n pinn-train python -m unittest discover -s tests/phase57 -p "test_*.py" -v; <home>/miniforge3/bin/conda run -n pinn-train python -m unittest tests.phase39.test_batches.CollocationQuotaTests tests.phase39.test_batches.FullBatchContract tests.phase50.test_causal_telemetry.CausalTelemetryOwnershipTests tests.phase50.test_validation_full_pool.ValidationFullPoolTests tests.phase50.test_candidate_finalization.CandidateFinalizationTests tests.phase50.test_evidence_builder.ExtractManifestTests tests.phase50.test_band_record.BandRecordTests tests.phase50.test_evidence_verifier.AttemptVerifierTests -v'` |
| **Feedback target** | targeted tests and artifact verifiers under 60 seconds; measure during execution |
| **Long-running gates** | the fresh six-case GATE-04 CLI, smoke, graded runs, and sole evaluation are explicit pre-run/runtime gates, not quick feedback tests |

No package installation is required.

## Stdlib Adjacent-Suite Applicability

| Phase | Existing module | Disposition |
|-------|-----------------|-------------|
| 39 | `tests.phase39.test_batches` | Run `CollocationQuotaTests` and `FullBatchContract` after batch/allocation changes. |
| 48 | Existing loss modules import/use pytest-style fixtures or function discovery | Not runnable as honest stdlib-unittest regressions; Phase-57 `LossNormalizationTests` ports the applicable causal-loss/value/gradient assertions without importing pytest. |
| 49 | Checkpoint/guard modules are pytest-style; `test_e2e_seam.py` has function tests that stdlib unittest discovers as zero tests | Not invoked; Phase-57 `WindowContractTests`, `MonitorContractTests`, and `LbfgsFreezeTests` cover the changed checkpoint/train seams through unittest. |
| 50 | `test_causal_telemetry`, `test_validation_full_pool`, `test_candidate_finalization`, `test_evidence_builder`, `test_band_record`, and `test_evidence_verifier` expose `unittest.TestCase` suites without pytest imports | Run the targeted classes named below. |

## Sampling Rate and Latency

- **After each Plan-01 task:** run its intentional-RED wrapper; it succeeds only when the named tests are collected and fail for missing Phase-57 behavior rather than import/environment errors.
- **After every production task:** run the task's focused Phase-57 class plus the mapped Phase-39/50 adjacent class.
- **After each implementation wave:** run the quick Phase-57 discovery command; after Waves 2-4 also run the adjacent regression command.
- **Before RUN-04:** run the full validation command, the fresh exact GATE-04 CLI and persisted-artifact check, then the final-R_ref-bound production verifier.
- **Before EVAL-02:** rerun the pre-evaluation artifact verifier immediately before the one evaluator invocation.
- **Feedback expectation:** C01-C19 are designed for under-60-second feedback except the once-per-phase six-case Gate execution named in the runtime table. Record measured times during execution; no watch mode is permitted.

## Command Catalog

| ID | Automated command | Expected direction |
|----|-------------------|--------------------|
| C01 | `<home>/miniforge3/bin/conda run -n pinn-train python -c "import subprocess,sys; p=subprocess.run([sys.executable,'-m','unittest','tests.phase57.test_recipe_production_path','-v'],capture_output=True,text=True); print(p.stdout+p.stderr); assert p.returncode != 0; assert 'test_controller_uses_complete_amended_recipe' in p.stdout+p.stderr; assert 'ImportError' not in p.stdout+p.stderr"` | Wrapper 0 with intentional target RED. |
| C02 | `<home>/miniforge3/bin/conda run -n pinn-train python -c "import subprocess,sys; mods=['tests.phase57.test_recipe_production_path.LossNormalizationTests','tests.phase57.test_runtime_freeze','tests.phase57.test_gate_and_evaluation.Gate04RulingTests']; p=subprocess.run([sys.executable,'-m','unittest','-v',*mods],capture_output=True,text=True); print(p.stdout+p.stderr); assert p.returncode != 0; assert 'test_segment_state_restores_exactly' in p.stdout+p.stderr; assert 'ImportError' not in p.stdout+p.stderr"` | Wrapper 0 with intentional target RED. |
| C03 | `<home>/miniforge3/bin/conda run -n pinn-train python -c "import subprocess,sys; p=subprocess.run([sys.executable,'-m','unittest','tests.phase57.test_runtime_freeze.ConfigProtocolTests','tests.phase57.test_gate_and_evaluation.EvaluationBoundaryTests','tests.phase57.test_gate_and_evaluation.EvidenceSelectionTests','tests.phase57.test_gate_and_evaluation.RunFailureClassificationTests','-v'],capture_output=True,text=True); print(p.stdout+p.stderr); assert p.returncode != 0; assert 'test_frame_assertion_precedes_test_materialization' in p.stdout+p.stderr; assert 'ImportError' not in p.stdout+p.stderr"` | Wrapper 0 with intentional target RED. |
| C04 | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest tests.phase57.test_recipe_production_path.AllocationContractTests tests.phase39.test_batches.CollocationQuotaTests tests.phase39.test_batches.FullBatchContract -v` | Exit 0. |
| C05 | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest tests.phase57.test_recipe_production_path.ProductionPathContractTests tests.phase57.test_recipe_production_path.LossNormalizationTests tests.phase50.test_causal_telemetry.CausalTelemetryOwnershipTests -v` | Exit 0. |
| C06 | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest tests.phase57.test_recipe_production_path.ProductionPathContractTests -v` | Exit 0. |
| C07 | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest tests.phase57.test_runtime_freeze.ConfigProtocolTests tests.phase57.test_recipe_production_path.ProductionPathContractTests -v` | Exit 0. |
| C08 | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest tests.phase57.test_runtime_freeze.MonitorContractTests tests.phase57.test_runtime_freeze.WindowContractTests tests.phase57.test_runtime_freeze.LbfgsFreezeTests tests.phase50.test_causal_telemetry.CausalTelemetryOwnershipTests -v` | Exit 0. |
| C09 | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest tests.phase57.test_runtime_freeze.ConfigProtocolTests tests.phase50.test_validation_full_pool.ValidationFullPoolTests -v` | Exit 0. |
| C10 | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest tests.phase57.test_gate_and_evaluation.Gate04RulingTests -v` | Exit 0; CLI status alone is not Gate acceptance. |
| C11 | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest tests.phase57.test_gate_and_evaluation.Gate04RulingTests.test_persisted_complete_pass_and_r_ref_provenance -v` | Exit 0 over the persisted Phase-57 Gate/R_ref pair. |
| C12 | `<home>/miniforge3/bin/conda run -n pinn-train python -m pinn.verification.phase57_production_conformance --r-ref-path pinn/verification/artifacts/r_ref_stage0.json --gate-evidence-root .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/gate04 --output .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/production-conformance.json` | Exit 0 with final R_ref/Gate provenance. |
| C13 | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest tests.phase57.test_gate_and_evaluation.EvaluationBoundaryTests tests.phase57.test_gate_and_evaluation.EvidenceSelectionTests tests.phase50.test_candidate_finalization.CandidateFinalizationTests tests.phase50.test_evidence_builder.ExtractManifestTests tests.phase50.test_band_record.BandRecordTests -v` | Exit 0. |
| C14 | `<home>/miniforge3/bin/conda run -n pinn-train python .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/verify_phase57_evidence.py admit-run-window` | Exit 0 only for immutable generation-4 inputs, preserved blocked generations 1–3, absent target directories, the version-2 historical ledger, and all retained artifact hashes; governed outputs remain writable. |
| C15 | `<home>/miniforge3/bin/conda run -n pinn-train python .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/verify_phase57_evidence.py run-window` | Exit 0 only for a complete generation-4 band or invariant-B-no-advance authorized terminal; every resumed invocation must match a hashed boundary checkpoint carrying invariant_b_state, while operational blocks remain nonzero/incomplete. |
| C16 | `<home>/miniforge3/bin/conda run -n pinn-train python .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/verify_phase57_evidence.py candidate` | Exit 0 for structural candidate or authorized unspent outcome, never an operational block. |
| C17 | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest tests.phase57.test_gate_and_evaluation.EvidenceSelectionTests tests.phase50.test_candidate_finalization.CandidateFinalizationTests tests.phase50.test_evidence_verifier.AttemptVerifierTests -v` | Exit 0. |
| C18 | `<home>/miniforge3/bin/conda run -n pinn-train python .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/verify_phase57_evidence.py pre-evaluation` | Exit 0 immediately before evaluation. |
| C19 | `<home>/miniforge3/bin/conda run -n pinn-train python .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/verify_phase57_evidence.py final` | Exit 0 for exactly one selected evaluation receipt or authorized unspent branch. |

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Behavior | Test Type | Commands | File Exists | Status |
|---------|------|------|-------------|------------|----------|-----------|----------|-------------|--------|
| 57-01-01 | 57-01 | 1/W0 | RUN-04 | T-57-01/02 | Real-path allocation tracer contracts | intentional RED | C01 | ❌ W0 | ⬜ pending |
| 57-01-02 | 57-01 | 1/W0 | RUN-04 | T-57-01 | Normalization, gradients, distinct monitor/window, L-BFGS, Gate contracts | intentional RED | C02 | ❌ W0 | ⬜ pending |
| 57-01-03 | 57-01 | 1/W0 | RUN-05, EVAL-02 | T-57-02 | Immutable band, terminal taxonomy, structural selection, pre-access/one-look | intentional RED | C03 | ❌ W0 | ⬜ pending |
| 57-02-01 | 57-02 | 2 | RUN-04 | T-57-03/04 | Exact binned allocation and Phase-39 batch continuity | unit/regression | C04 | ❌ W0 | ⬜ pending |
| 57-02-02 | 57-02 | 2 | RUN-04 | T-57-04 | Normalized loss/all-slot gradients and telemetry ownership | unit/integration | C05 | ❌ W0 | ⬜ pending |
| 57-02-03 | 57-02 | 2 | RUN-04 | T-57-05 | Raw/normalized diagnostics | integration | C06 | ❌ W0 | ⬜ pending |
| 57-03-01 | 57-03 | 3 | RUN-04 | T-57-06 | Strict 4096/R_ref construction | integration | C07 | ❌ W0 | ⬜ pending |
| 57-03-02 | 57-03 | 3 | RUN-04 | T-57-07 | Frozen monitor, separate 500-step deadline, segment, resume | integration/regression | C08 | ❌ W0 | ⬜ pending |
| 57-03-03 | 57-03 | 3 | RUN-05 | T-57-08 | Config comparability and validation-pool continuity | unit/regression | C09 | ❌ W0 | ⬜ pending |
| 57-04-01 | 57-04 | 4 | RUN-04 | T-57-10 | Exact Gate implementation plus persisted six-case PASS/R_ref provenance | unit/artifact | C10, C11 | ❌ W0 | ⬜ pending |
| 57-04-02 | 57-04 | 4 | RUN-04 | T-57-09 | Real production path bound to final R_ref | integration/e2e | C12 | ❌ W0 | ⬜ pending |
| 57-04-03 | 57-04 | 4 | RUN-05, EVAL-02 | T-57-11/12 | Evaluator pre-access and Phase-50 evidence semantics | integration/regression | C13 | ❌ W0 | ⬜ pending |
| 57-05-01 | 57-05 | 5 | RUN-04, RUN-05 | T-57-13/15 | Immutable run-window admission | artifact/preflight | C14 | ❌ W0 | ⬜ pending |
| 57-05-02 | 57-05 | 5 | RUN-04, RUN-05 | T-57-13 | Recheck unchanged admission at operator checkpoint | artifact/preflight | C14 | ❌ W0 | ⬜ pending |
| 57-05-03 | 57-05 | 5 | RUN-04, RUN-05 | T-57-13..16 | Complete band versus authorized terminal versus incomplete block | runtime/artifact | C15 | ❌ W0 | ⬜ pending |
| 57-06-01 | 57-06 | 6 | EVAL-02 | T-57-17 | Four-fact 42/41/43 selection and block refusal | artifact/regression | C16, C17 | ❌ W0 | ⬜ pending |
| 57-06-02 | 57-06 | 6 | EVAL-02 | T-57-18/20 | Three preconditions and canonical frame immediately before spend | artifact/preflight | C18 | ❌ W0 | ⬜ pending |
| 57-06-03 | 57-06 | 6 | EVAL-02 | T-57-18..20 | Exactly one selected-best.pt receipt | artifact | C19 | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

## Wave 0 Requirements

- [ ] `tests/phase57/__init__.py` — stdlib discovery marker.
- [ ] `tests/phase57/_fixtures.py` — deterministic CPU/training-only/held-out-sentinel fixtures.
- [ ] `tests/phase57/test_recipe_production_path.py` — allocation, normalized loss, gradients, diagnostics, energy reuse, microbatch equivalence, 4096 fail-closed.
- [ ] `tests/phase57/test_runtime_freeze.py` — frozen monitor identity, separate `front_advance_window_n = 500`, L-BFGS closure/outer-call freeze, checkpoint/resume, configs.
- [ ] `tests/phase57/test_gate_and_evaluation.py` — exact Gate persisted evidence, terminal/block taxonomy, canonical pre-access, structural fallback, sole evaluation.
- [ ] All three intentional-RED wrappers prove target failures rather than collection/import/environment failures.

Wave 0 is complete only when Plan 57-01 has created these tests and recorded its expected RED evidence. No pytest installation or invocation is permitted.

## Pre-Run and Runtime Gates

| Gate | Runnable action | Passing state | Failure disposition |
|------|-----------------|---------------|---------------------|
| Exact GATE-04 | `<home>/miniforge3/bin/conda run -n pinn-train python -m pinn.verification.gate04_train_free --precision float64 --device cpu --evidence-root .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/gate04 --r-ref-path pinn/verification/artifacts/r_ref_stage0.json` then C11 | Six cases; PASS; empty blocking/unratified; exact 2:1, alpha, 1/sqrt2, front15, all weights >=0.70; matching R_ref provenance | Completed scientific BLOCK is authorized terminal/unspent; execution/write/schema failure blocks incomplete/unspent. |
| Production conformance | C12 | Actual controller path and final R_ref/Gate hashes pass | Block incomplete; evaluation preserved. |
| Resource preflight | Plan 57-05 exact-4096 allocation probe | Exact 4096 rows allocate | Block incomplete; never reduce count; evaluation preserved. |
| Invariant B | Frozen training-only monitor plus separate `front_advance_window_n = 500` | Front advances inside 500 accepted steps | No-advance is authorized terminal/unspent; other guard failures block incomplete/unspent. |
| Run fingerprint | C14 before smoke and operator authorization | No commit or fingerprinted input/environment mutation; governed run/evidence outputs allowed | Block incomplete/unspent. |
| Evaluation readiness | C18 immediately before evaluator | Exact three preconditions, canonical frame, selected best.pt hash, no prior claim | Block/unspent. |
| Sole evaluation | One direct `python -m pinn.evaluate` command, then C19 | Exactly one selected-run claim/directory/receipt | Once claimed, no retry/fallback; record attempted/spent failure. |

## Manual Checkpoints

| Behavior | Requirement | Why Manual | Verification |
|----------|-------------|------------|--------------|
| Authorize expensive smoke/band window | RUN-04, RUN-05 | Operator compute authorization only; scientific/config decisions are already fixed | Review C14 receipt and exact four commands; reply `proceed` or `stop`. |
| Authorize sole evaluation spend | EVAL-02 | The protected one-look action is irreversible once claimed | Review C18 receipt and pinned best.pt; reply `approved` only if every machine fact passes. |

## Validation Sign-Off

- [ ] All 18 tasks have runnable `<automated>` verification and `<fails_when>` direction.
- [ ] Sampling continuity has no unverified implementation task.
- [ ] Wave 0 exists and intentional-RED evidence is target-specific.
- [ ] Phase-39/50 adjacent stdlib regressions pass; Phase-48/49 pytest-coupled modules are not silently reported as unittest coverage.
- [ ] Quick and adjacent suites meet the under-60-second feedback target or measured exceptions are recorded.
- [ ] Fresh GATE-04 persisted evidence and final-R_ref production conformance pass before training.
- [ ] Terminal versus blocked-incomplete dispositions pass their trip tests.
- [ ] No watch mode, pytest command, reduced-row fallback, held-out pre-access, or second evaluation exists.
- [ ] `nyquist_compliant: true` and `wave_0_complete: true` are set only by post-execution validation.

**Approval:** pending execution and `$gsd-validate-phase 57`.
