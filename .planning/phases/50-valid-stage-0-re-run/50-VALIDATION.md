---
phase: 50
slug: valid-stage-0-re-run
status: planned
nyquist_compliant: true
wave_0_complete: false
created: 2026-08-14
---

# Phase 50 — Validation Strategy

> Per-phase validation contract for closing RUN-01 and RUN-02 without spending the held-out evaluation look or tuning against observed results.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python 3.11 `unittest` |
| **Config file** | none — module/discovery invocation |
| **Quick run command** | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest tests.phase46.test_gate_composition tests.phase46.test_validation_wiring tests.phase50.test_causal_telemetry tests.phase50.test_evidence_verifier -v` |
| **Full suite command** | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest discover -s tests -p 'test_*.py' -v` |
| **Estimated runtime** | quick modules under 30 seconds; full suite measured before preregistration |

---

## Fixture-Tested Verifier Command Contract

All commands below are implemented and positive/negative fixture-tested by Plan 50-07 before Plan 50-09 may open a registration or Plan 50-11 may launch a process.

| Mode | Production command shape | Success marker | First-use gate |
|------|--------------------------|----------------|----------------|
| Pre-append identity baseline | `python evidence/verify_phase50_evidence.py identity-baseline --repo-root ROOT --ledger evidence/run-ledger.md --output evidence/identity-baseline-generation-4.json` | `IDENTITY-BASELINE-OK` | Plan 50-09 before any generation-4 append |
| Committed preregistration authorization | `python evidence/verify_phase50_evidence.py identity --state authorization --repo-root ROOT --authorization-summary 50-08-SUMMARY.md` | `IDENTITY-OK` | Plan 50-09 precondition; reads the ancestor blob, not working-tree text |
| Exact preregistered/run-window identity | `python evidence/verify_phase50_evidence.py identity --state preregistered\|run-window --repo-root ROOT --authorization-summary 50-08-SUMMARY.md [--smoke-authorization-summary 50-10-SUMMARY.md] --baseline evidence/identity-baseline-generation-4.json --pre-registration 50-PRE-REGISTRATION.md --config-delta 50-CONFIG-DELTA.md --ledger evidence/run-ledger.md` | `IDENTITY-OK` | Plans 50-09/50-10 and before each Plan 50-11 spawn; rejects scoped tracked and untracked drift |
| Smoke/graded semantic attempt | `python evidence/verify_phase50_evidence.py attempt --repo-root ROOT --generation 4 --kind smoke\|graded [--seed 41\|42\|43] --attempt-root PATH --ledger evidence/run-ledger.md --pre-registration 50-PRE-REGISTRATION.md` | `ATTEMPT-OK` | Plan 50-11 after smoke and after each seed before checkpoint/next seed/final-band state |

The concrete plans use absolute Phase-50 paths. Plan 50-12 verifier `all` repeats identity and attempt semantics only as defense in depth; it is not the first-detection gate.

---

## Sampling Rate

- **After every task commit:** Run the closest affected module tests plus `git diff --check`.
- **After every implementation wave:** Run the full `unittest` discovery command.
- **Before immutable preregistration:** Require the full suite, normal builder/verifier fixture suite, exact config diffs, and clean runtime/head identity checks.
- **After smoke:** Run verifier `attempt --kind smoke`; any nonzero result closes generation 4 terminally before the graded-run authorization checkpoint.
- **After each graded seed:** Run verifier `attempt --kind graded --seed N`; any nonzero result closes generation 4 terminally before launching the next seed or setting final-band state.
- **Before `$gsd-verify-work`:** The normal evidence verifier and all four Phase 50 roadmap truths must pass.
- **Max feedback latency:** under 30 seconds for unit-task feedback; expensive smoke and graded jobs are explicit owner-gated checks.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 50-06-01 | 50-06 | 6 | RUN-01 | T-50-06-01, T-50-06-02 | MPS prediction data detaches, moves to CPU, then casts float64 without changing metric semantics | MPS unit/integration | `python -m unittest tests.phase46.test_gate_composition tests.phase46.test_validation_wiring -v` on canonical MPS | ⚠️ tests exist; regression added during execution | planned |
| 50-06-02 | 50-06 | 6 | RUN-01 | T-50-06-03 | Training-owned causal telemetry survives an intervening validation pass | deterministic unit | `python -m unittest tests.phase50.test_causal_telemetry -v` | ❌ execution creates | planned |
| 50-06-03 | 50-06 | 6 | RUN-01 | T-50-06-04 | Diagnosis records whether overwrite was proven and makes no ungrounded dynamics claim | regression + artifact check | Plan 50-06 combined unittest and clean-commit gate | ❌ execution creates | planned |
| 50-07-01 | 50-07 | 6 | RUN-01, RUN-02 | T-50-07-01, T-50-07-02, T-50-07-07 | Identity baseline/authorization/preregistered/run-window modes recompute all locked identities, preserve generations 1-3, and reject malformed state plus scoped tracked/untracked drift | positive/negative fixture integration | `python -m unittest tests.phase50.test_evidence_builder tests.phase50.test_evidence_verifier -v` | ❌ execution creates/extends | planned |
| 50-07-02 | 50-07 | 6 | RUN-01, RUN-02 | T-50-07-03, T-50-07-04, T-50-07-08 | Attempt mode parses smoke/graded source artifacts and predecessor eligibility; only three complete same-generation seeds produce a D-24 band | positive/negative fixture integration | `python -m unittest tests.phase50.test_band_record tests.phase50.test_evidence_verifier -v` | ❌ execution creates/extends | planned |
| 50-07-03 | 50-07 | 6 | RUN-01, RUN-02 | T-50-07-05, T-50-07-06 | Candidate/finalize/all use structural policy, reject held-out paths, and preserve terminal behavior | positive/negative fixture integration | `python -m unittest tests.phase50.test_candidate_finalization tests.phase50.test_evidence_verifier -v` | ❌ execution creates | planned |
| 50-08-01 | 50-08 | 7 | RUN-01, RUN-02 | T-50-08-03..05 | Conformance results resolve to an owner-ready, non-predictive decision brief with no new generation | automated readiness | Plan 50-08 combined suite, terminal verifier, and generation-4 absence gate | ✅ artifact specified | planned |
| 50-08-02 | 50-08 | 7 | RUN-01, RUN-02 | T-50-08-01..05 | Owner decision is verbatim, scope-bounded, and atomically committed with blob-SHA-256 trailer; only exact authorize-preregistration continues | owner decision + committed-blob gate | Exact option checkpoint, scripts/agent-commit, then verifier `identity --state authorization` | ✅ checkpoint and commit specified | planned |
| 50-09-01 | 50-09 | 8 | RUN-01, RUN-02 | T-50-09-01..05, T-50-09-07 | Committed authorization passes; baseline precedes append; generation 4 is immutable, policy-identical, unopened, and identity-bound | preregistration integration | verifier `identity --state authorization`, then `identity-baseline`; scaffold JSON check | ✅ verifier implemented in 50-07; generation-4 append pending | planned |
| 50-09-02 | 50-09 | 8 | RUN-01, RUN-02 | T-50-09-01..07 | Preregistration lands in one explicit-path governed commit and exact identity re-proves authorization/baseline/ancestry/cleanliness | suite + exact identity + commit gate | Phase-50 discovery tests, verifier `identity --state preregistered`, `git diff --check`, scripts/agent-commit | ✅ mechanism exists | planned |
| 50-10-01 | 50-10 | 9 | RUN-01, RUN-02 | T-50-10-01, T-50-10-02, T-50-10-05 | Immutable preregistration resolves to one exact smoke identity; tracked/untracked drift, prior-generation mutation, or authorization-blob mismatch blocks | identity gate | verifier `identity --state preregistered` plus Phase-50 tests | ✅ verifier implemented in 50-07 | planned |
| 50-10-02 | 50-10 | 9 | RUN-01, RUN-02 | T-50-10-01..05 | One exact source identity receives durable smoke-only authority in a committed read-only summary | owner decision + exact run-window identity | scripts/agent-commit, then verifier `identity --state run-window --smoke-authorization-summary ...` | ✅ checkpoint specified | planned |
| 50-11-01 | 50-11 | 10 | RUN-01, RUN-02 | T-50-11-01, T-50-11-03..05 | Exact-authorized smoke finishes and passes source-parsing semantic verification before graded authority is requested | real-corpus smoke integration | verifier `identity --state run-window`, launch/copy, then verifier `attempt --kind smoke` | ✅ runtime path; execution pending authorization | planned |
| 50-11-02 | 50-11 | 10 | RUN-01, RUN-02 | T-50-11-02, T-50-11-07 | Owner sees only smoke facts already accepted by the semantic verifier and authorizes/holds/closes the graded spend | automated semantic smoke gate + owner decision | Repeat verifier `attempt --kind smoke`, then exact decision checkpoint | ✅ checkpoint specified | planned |
| 50-11-03 | 50-11 | 10 | RUN-01, RUN-02 | T-50-11-01..08 | Seeds 41→42→43 finish sequentially; each passes source-parsing attempt/predecessor semantics before the next launch/finalization | real-corpus graded integration | verifier `attempt --kind graded --seed 41`, then 42, then 43; terminal verifier on first failure | ✅ runtime path; execution pending authorization | planned |
| 50-12-01 | 50-12 | 11 | RUN-01, RUN-02 | T-50-12-01, T-50-12-02, T-50-12-04, T-50-12-06 | Complete generation extracts to a descriptive D-24 band; terminal generation emits no normal artifact | normal/terminal evidence verification | verifier `manifest` + `band`, or terminal verifier branch | ❌ normal artifacts require completed runs | planned |
| 50-12-02 | 50-12 | 11 | RUN-01, RUN-02 | T-50-12-03, T-50-12-05, T-50-12-07 | Structural candidate/final manifest pass verifier `all` without held-out access | evidence verification | verifier `candidate` then `all` | ❌ normal artifacts require completed runs | planned |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky. The planner replaces provisional `TBD`/`W0` identifiers with final plan/task IDs.*

---

## Wave 0 Requirements

- [ ] Add an MPS float32 conversion regression to the existing Phase 46 composition and wiring tests; on the canonical host, an MPS skip is a failed verification.
- [ ] Add a deterministic causal-telemetry ownership regression; change runtime behavior only if the regression proves an implementation overwrite.
- [ ] Implement and positive/negative-test verifier `identity-baseline` plus `identity` authorization/preregistered/run-window states, including committed decision blobs, every locked identity, generations 1-3 preservation, malformed/open-generation state, and scoped tracked/untracked rejection.
- [ ] Implement and positive/negative-test verifier `attempt` for smoke and seeds 41/42/43, covering hashes/containment, exact identities, fresh/no-resume/Stage-0/1000-step semantics, invariants/front window, validation cadence/sidecars, held-out absence, and predecessor order.
- [ ] Implement and test normal `extract`, `band`, `candidate`, `finalize`, and verifier `all` paths while preserving terminal-mode behavior.
- [ ] Add the positive and negative three-seed fixture matrix specified in `50-RESEARCH.md`; no training job or real corpus is required for these tests.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Owner authorizes later-generation preregistration, then exact smoke and graded launches | RUN-01, RUN-02 | Authorization scope and compute spend are owner decisions, not automatable tests | Preserve GAP-50-03 as read-only history; commit the exact preregistration decision blob; separately commit the smoke decision blob; request graded authority only after semantic smoke verification |
| Causal front advances within 500 steps and invariants hold through a finished 1000-step seed | RUN-01 | Requires the expensive real-corpus Stage-0 experiment | Launch only the authorized immutable seed configuration; independently inspect terminal status, trip state, causal telemetry, validation events, and ledger before the next seed |
| Three-seed validation band and candidate record are complete | RUN-02 | Requires sequential finished runs for seeds 41, 42, and 43 | Run the normal builder and independent verifier after all three seeds; confirm D-24 band, structural candidate policy, manifests, and absence of held-out evaluation materialization |

---

## Threat References

| Ref | Threat | Required control |
|-----|--------|------------------|
| T-50-01 | An instrumentation exception or device-conversion failure appears as a usable validation metric | Keep `gate_status` distinct from verdict; any non-healthy status or missing sidecar is terminal |
| T-50-02 | Evidence paths escape the run/phase root or source copies are changed | Canonical path containment, source/copy SHA-256, symlink/escape rejection |
| T-50-03 | A partial or mixed generation is characterized as the three-seed band | Require one finalized generation, three finished seeds, common identities, and independent normal verification |
| T-50-04 | Observed metrics influence recipe or candidate selection | Immutable preregistration, SCOPE-29 conformance-only boundary, eligibility-only candidate fallback |
| T-50-05 | Held-out evaluation is spent during Phase 50 | Reject evaluation directories, attempts, and test-materialization artifacts; Phase 51 alone owns the look |

---

## Validation Sign-Off

- [x] All final plan tasks have an automated check or an explicit owner-gated/manual verification dependency.
- [x] Sampling continuity: no three consecutive implementation tasks without automated verification.
- [x] Wave-6 readiness plans cover every missing regression and normal evidence-tool mode; `wave_0_complete` remains false until implementation executes.
- [x] Identity and semantic attempt modes have explicit executable command contracts and Plan 50-07 fixture coverage before first production use.
- [x] No watch-mode flags.
- [x] Unit feedback latency remains under 30 seconds for the targeted suites; real-corpus jobs are separately owner-gated.
- [x] Validation repair preserves frame, population, formula, threshold, cadence, and gate-failure semantics.
- [x] No training or validation job launches before the required owner checkpoint.
- [x] `nyquist_compliant: true` and final plan/task IDs are set.

**Approval:** planned and mapped; implementation and owner-gated execution pending
