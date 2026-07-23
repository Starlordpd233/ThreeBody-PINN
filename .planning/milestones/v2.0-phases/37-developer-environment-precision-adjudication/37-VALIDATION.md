---
phase: 37
slug: developer-environment-precision-adjudication
status: ready-for-execution
nyquist_compliant: true
wave_0_complete: false
created: 2026-07-11
---

# Phase 37 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python 3.11 standard-library `unittest`; shell syntax via `bash -n` |
| **Config file** | none — Wave 0 creates `tests/phase37/`; no project-wide Python test configuration is required |
| **Quick run command** | `conda run -n pinn-train python -m unittest discover -s tests/phase37 -p 'test_*.py'` |
| **Full suite command** | `bash -n setup.sh scripts/refresh-environment-lock.sh && conda run -n pinn-train python -m unittest discover -s tests/phase37 -p 'test_*.py' && conda run -n pinn-train python scripts/verify_environment.py --check-only` |
| **Estimated runtime** | quick suite: <30 seconds; full software-only suite: <120 seconds; fresh-Mac bootstrap and real MPS evidence are designated hardware gates |

---

## Sampling Rate

- **After every task commit:** Run the task's narrow `tests.phase37.test_*` module plus `git diff --check`.
- **After every plan wave:** Run `bash -n` for changed shell scripts and the complete `tests/phase37` discovery command.
- **After Wave 1:** Run the real environment verifier and `pip check`; inspect the fingerprint and committed lock hash; run `./setup.sh` twice and confirm the second invocation is a no-op validation pass.
- **After Wave 3:** Run the CPU worker and orchestrator failure-path suite; do not run the empirical MPS arm as incidental regression sampling.
- **Before `/gsd-verify-work`:** Run the full software suite, the setup first/second-run checks, and the designated Wave 4 dual-arm evidence command.
- **Max feedback latency:** 120 seconds for ordinary automated sampling; hardware/network gates are isolated to their named waves.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 37-01-01 | 01 | 0 | ENV-01, ENV-02 | T-37-01 | bootstrap tests use fake tools and temporary prefixes; no host mutation | contract/unit | `conda run -n pinn-train python -m unittest tests.phase37.test_setup_contract tests.phase37.test_environment_fingerprint` | ❌ W0 | ⬜ pending |
| 37-01-02 | 01 | 0 | ENV-03, ENV-04 | T-37-02 | probe tests sanitize child environments and never select a precision | scientific/unit | `conda run -n pinn-train python -m unittest tests.phase37.test_runtime tests.phase37.test_componentwise_ad tests.phase37.test_precision_orchestrator` | ❌ W0 | ⬜ pending |
| 37-02-01 | 02 | 1 | ENV-01 | T-37-03 | setup fails closed on incompatible hosts/prefixes and does not alter shell startup files | shell + integration | `bash -n setup.sh scripts/refresh-environment-lock.sh && conda run -n pinn-train python scripts/verify_environment.py --check-only` | ❌ W0 | ⬜ pending |
| 37-02-02 | 02 | 1 | ENV-02 | T-37-04 | normal setup cannot rewrite the pinned lock; fingerprint excludes secrets and hashes the lock | unit + integration | `conda run -n pinn-train python -m unittest tests.phase37.test_setup_contract.TestLockBoundary tests.phase37.test_environment_fingerprint` | ❌ W0 | ⬜ pending |
| 37-03-01 | 03 | 2 | ENV-04 | T-37-05 | unsupported or omitted precision/device pairs fail before tensor creation; global dtype is unchanged | unit | `conda run -n pinn-train python -m unittest tests.phase37.test_runtime` | ❌ W0 | ⬜ pending |
| 37-03-02 | 03 | 2 | ENV-03 | T-37-06 | both AD methods preserve the locked analytical fixture and reject non-finite/component errors | scientific/unit | `conda run -n pinn-train python -m unittest tests.phase37.test_componentwise_ad` | ❌ W0 | ⬜ pending |
| 37-04-01 | 04 | 3 | ENV-03 | T-37-07 | MPS fallback is removed before Torch import; child failures are recorded without fallback | subprocess integration | `conda run -n pinn-train python -m unittest tests.phase37.test_precision_orchestrator` | ❌ W0 | ⬜ pending |
| 37-04-02 | 04 | 3 | ENV-03 | evidence writes are atomic/non-overwriting and summaries are verdict-free and re-derivable | unit/schema | `conda run -n pinn-train python -m unittest tests.phase37.test_precision_orchestrator tests.phase37.test_componentwise_ad` | ❌ W0 | ⬜ pending |
| 37-05-01 | 05 | 4 | ENV-01, ENV-02, ENV-03, ENV-04 | T-37-08 | on-device run records actual devices/fallback state and stops for owner D1-p instruction | hardware + evidence validation | `conda run -n pinn-train python -m unittest discover -s tests/phase37 -p 'test_*.py'` plus the implemented dual-arm orchestration command | ❌ W0 | ⬜ pending |

*Task IDs are the validation contract expected by the research-derived five-plan decomposition; the planner must keep these mappings synchronized if it changes plan/task numbering.*

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/phase37/__init__.py` — package marker for targeted module commands.
- [ ] `tests/phase37/test_setup_contract.py` — fake-conda/fake-installer and bootstrap state-transition tests for ENV-01/02.
- [ ] `tests/phase37/test_environment_fingerprint.py` — canonical JSON, Markdown derivation, secret exclusion, and lock-hash tests for ENV-02.
- [ ] `tests/phase37/test_runtime.py` — precision/device pair and no-global-default tests for ENV-04.
- [ ] `tests/phase37/test_componentwise_ad.py` — locked fixture, analytical derivatives, method parity, timing-sample, and error-threshold tests for ENV-03.
- [ ] `tests/phase37/test_precision_orchestrator.py` — subprocess isolation, environment sanitation, structured failure, non-overwrite, and verdict-free report tests for ENV-03.
- [ ] Shared fake executable/temp-prefix fixtures — destructive-path-free bootstrap coverage.
- [ ] Canonical environment-fingerprint and precision-evidence schema assertions.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Fresh-Mac Miniforge/Python/Torch bootstrap and second-run idempotence | ENV-01, ENV-02 | Requires the target M5 Pro, network access, and an initially absent environment; cannot be made cheap or hermetic | Run `./setup.sh` on the target host, validate `pinn-train`, capture environment state, run `./setup.sh` again, and prove no environment or repository mutation except a deliberately new non-overwriting fingerprint if configured. |
| Real fp32-MPS and fp64-CPU dual-arm evidence | ENV-03, ENV-04 | Requires real MPS hardware and synchronized kernel timing | After Waves 0–3 are green, run the implemented orchestration command once; validate raw JSON, re-derive the Markdown summary, confirm actual/requested devices and fallback state, and preserve the timestamped evidence. |
| D1-p precision selection | ENV-03 | Owner-carved semantic decision; automation must not infer or recommend it | Present both validated arms and their correctness/failure/timing evidence. Stop until the owner records `fp32-MPS` or `fp64-CPU`; do not set a production default beforehand. |

---

## Required Negative Coverage

- Incompatible occupied install prefix fails without deletion or update.
- Non-arm64 or non-macOS host fails before network access.
- Drifted `pinn-train` fails with explicit instructions rather than auto-rebuild.
- Missing lock or implicit lock refresh fails; ordinary setup cannot change lock bytes.
- MPS unavailable fails ENV-01 verification.
- Missing, partial, or unsupported precision/device pairs fail before tensor creation.
- MPS child retaining `PYTORCH_ENABLE_MPS_FALLBACK` fails and records the violation.
- Requested and actual devices differing fails the evidence criterion.
- Child timeout, signal, malformed JSON, or Torch exception becomes a structured record with no fallback child.
- Aggregate error `>= 1e-6`, non-finite components, or vector mismatch fails correctness.
- Evidence path collision fails without overwriting.
- Evidence summaries that recommend, rank, choose, or assert a production default fail the verdict-free contract.

---

## Validation Sign-Off

- [x] Every executable task has an automated verify or Wave 0 dependency; the terminal D1-p checkpoint is explicitly manual-only.
- [x] Sampling continuity: no 3 consecutive executable tasks without automated verify.
- [x] Wave 0 plans cover all MISSING test/schema references; `wave_0_complete` remains false until execution creates them.
- [x] No watch-mode flags.
- [x] Ordinary automated feedback latency < 120 seconds.
- [x] Hardware/network checks are isolated to explicit Wave 1 and Wave 4 gates.
- [x] D1-p remains owner-selected and no production precision default is introduced.
- [x] `nyquist_compliant: true` set after task IDs `37-01-01` through `37-05-01` were synchronized with all five plans.

**Approval:** approved 2026-07-11 for planning coverage; Wave 0 and target-hardware execution remain pending.
