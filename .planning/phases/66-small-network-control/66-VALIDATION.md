---
phase: "66"
slug: "small-network-control"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-10-31"
---

# Phase 66 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

Seeded by plan-phase from `66-RESEARCH.md`, section "Validation Architecture".
The requirement-level map below is bound to plan task IDs once the plans exist.
No planned test or real run has been executed during planning.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python standard-library `unittest` in the existing pinn-train environment |
| **Interpreter** | `<home>/miniforge3/envs/pinn-train/bin/python` |
| **Config file** | none (same convention as Phase 65; no framework installation) |
| **Quick run command** | `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase66 -t .` |
| **Full suite command** | `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase65 -t .` then the quick run command |
| **Estimated runtime** | Phase 65 suite: 204 tests, about 33 seconds (includes one MPS parity test). Phase 66 suite: unmeasured; keep it within 60 seconds. |

---

## Sampling Rate

- **After every task commit:** Run the closest `tests.phase66` module.
- **After every plan wave:** Run all of `tests/phase66` plus all of `tests/phase65`.
- **Before `/gsd-verify-work`:** Both suites green, `check-registration` and `verify-result` passing for every Phase 66 registration and record, and the page-then-registration-then-record ancestry check passing.
- **Max feedback latency:** 60 seconds for unit feedback. Real runs are separate, registered, AC-power-only evidence steps, not routine tests.

A synthetic test pass is not evidence that the small network fitted an orbit. Real
results come only from registered runs whose prediction page was committed first.

---

## Per-Task Verification Map

Requirement-level map from research. Task IDs are bound after planning.

| Requirement | Behavior | Test Type | Automated Command (after the interpreter `-B`) | File Exists | Status |
|-------------|----------|-----------|-------------------------------------------------|-------------|--------|
| EXP-01 / SC-1 | Variant registered through `register_variant` into a copy; sealed `REGISTRY` unchanged; duplicates refused | unit | `-m unittest tests.phase66.test_catalog` | ❌ W0 | ⬜ pending |
| EXP-01 / SC-1 | Page variant JSON and parameter count equal the production-class computation; timing page and main page agree on the design block; band numbers equal 0.95 and 1.05 times the constant-predictor E | static | `-m unittest tests.phase66.test_pages` | ❌ W0 | ⬜ pending |
| EXP-01 / SC-1 | Phase 66 registrations admit; every Phase 65 refusal still applies; unknown registry refuses; a cap at 3,600 s refuses | unit (fixture repos) | `-m unittest tests.phase66.test_admission` | ❌ W0 | ⬜ pending |
| EXP-01 / SC-1 | AC-power gate fails closed; launch order | unit (fakes) | `-m unittest tests.phase66.test_power` | ❌ W0 | ⬜ pending |
| EXP-01 / SC-2 | Record carries the registry, similarity rows, scores and both comparison rows; verify checks the registry | unit (synthetic corpus) | `-m unittest tests.phase66.test_records` | ❌ W0 | ⬜ pending |
| EXP-01 / SC-2, SC-3 | Branch classification and repeat confirmation at every boundary | unit | `-m unittest tests.phase66.test_reading_rule` | ❌ W0 | ⬜ pending |
| Phase 65 preserved | Unedited pins and evidence hashes unchanged; historical harness bytes recoverable at the introducing commit | unit (git) | `-m unittest tests.phase66.test_historical` | ❌ W0 | ⬜ pending |
| Phase 65 preserved | The Phase 65 tests still pass | regression | full suite command | ✅ | ⬜ pending |
| EXP-01 / SC-1 | Page, then registration, then record ancestry holds for the timing run and each experiment run | git verification | evidence-order check (executor-run after evidence exists) | executor-run | ⬜ pending |
| EXP-01 / SC-2 | Each record verifies against its registration | CLI | `-m pinn.verification.diagnostic_fit verify-result --registration R --result record.json` expecting `VERIFY-RESULT-OK`, exit 0 | executor-run | ⬜ pending |
| EXP-01 / SC-3 | `66-REVIEW.md` records the branch, a plain-language reading and any SCOPE-49 proposal with the owner's answer, citing record digests | structure check + manual | heading check; the owner's answer is manual-only | executor-run, manual | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/phase66/__init__.py`, `test_catalog.py`, `test_admission.py`, `test_records.py`, `test_reading_rule.py`, `test_power.py`, `test_pages.py`, `test_historical.py`
- [ ] New harness modules named by the plans are created test-first
- [ ] No framework install; no change to `tests/phase65`

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Owner's answer to any SCOPE-49 proposal at checkpoint ① | EXP-01 / SC-3 | A reserved owner decision (66-CONTEXT D-01, D-12) | Present the branch, the plain-language reading and the proposal; record the owner's verbatim answer in `66-REVIEW.md` |
| Mac on AC power for each training launch | EXP-01 / SC-2 | The owner's compute window (66-CONTEXT D-08): weekends, plugged in | The launch gate refuses on battery; the operator plugs in and relaunches |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
