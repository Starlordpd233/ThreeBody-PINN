---
phase: 40
slug: stage-0-curriculum-training-loop-fut-04
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-07-16
---

# Phase 40 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Reconciled 2026-07-16 to the authoritative Validation Architecture in `40-RESEARCH.md`
> (stdlib `unittest`, `tests/phase40/`, Phase 38/39 conventions). The PLAN.md files are
> the authoritative per-task test contract.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | stdlib `unittest` (no pytest — Phase 37/38/39 convention) |
| **Config file** | none — `unittest discover` |
| **Quick run command** | `<home>/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase40 -p 'test_*.py' -v` |
| **Full suite command** | `<home>/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests -p 'test_*.py' -v` |
| **Estimated runtime** | ~60–120 seconds |

---

## Sampling Rate

- **After every task commit:** Run the task's targeted test module (see map) paired with `tests.phase40.test_prohibitions` (Phase 38/39 convention: every production-module change re-runs the prohibitions audit)
- **After every plan wave:** Run the phase-40 discover command (quick run command above)
- **Before `/gsd-verify-work`:** Full suite (`tests/` discover) must be green
- **Max feedback latency:** 120 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| (scaffold) | 01 | 1 | TRAIN-01..07 (test contract) | — | N/A | unit | `python -m unittest tests.phase40.test_prohibitions -v` | ❌ W0 | ⬜ pending |
| (weights) | 02 | 2 | TRAIN-03 | — | N/A | unit | `python -m unittest tests.phase40.test_scheduled_weights -v` | ❌ W0 | ⬜ pending |
| (clip) | 02 | 2 | TRAIN-05 | — | N/A | unit | `python -m unittest tests.phase40.test_grad_clip -v` | ❌ W0 | ⬜ pending |
| (sampler) | 03 | 2 | TRAIN-04 | — | N/A | unit | `python -m unittest tests.phase40.test_collocation_sampler -v` | ❌ W0 | ⬜ pending |
| (preflight) | 03 | 2 | TRAIN-07 | — | N/A | unit | `python -m unittest tests.phase40.test_slbfgs_preflight -v` | ❌ W0 | ⬜ pending |
| (stage-exit) | 04 | 2 | TRAIN-06 | T-40-02 | weights_only-clean `state_dict` composition (CTX-44) | unit | `python -m unittest tests.phase40.test_stage_exit -v` | ❌ W0 | ⬜ pending |
| (inner loop) | 05 | 3 | TRAIN-02 | — | N/A | unit | `python -m unittest tests.phase40.test_optimizer_phase -v` | ❌ W0 | ⬜ pending |
| (outer loop) | 06 | 4 | TRAIN-01 | — | N/A | unit | `python -m unittest tests.phase40.test_controllers -v` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky. Exact task IDs live in the PLAN.md files (authoritative).*

---

## Wave 0 Requirements

- [ ] `tests/phase40/__init__.py` — package marker
- [ ] `tests/phase40/_fixtures.py` — stub model + stub `StageQuery`/batch source, mirroring `tests/phase39/_fixtures.py` conventions (SimpleNamespace-backed stub, not on-disk corpus)
- [ ] Eight test modules per the RESEARCH Recommended Project Structure (`test_controllers`, `test_optimizer_phase`, `test_scheduled_weights`, `test_collocation_sampler`, `test_grad_clip`, `test_stage_exit`, `test_slbfgs_preflight`, `test_prohibitions`)
- [ ] `tests/phase40/test_prohibitions.py` — extend the Phase 38/39 AST/discovery audit to `pinn/training/*.py` (no v1.3 imports, no hardcoded precision/device, no corpus-path access)
- [ ] Framework install: none — `unittest` is stdlib

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Full Stage-0 end-to-end pilot convergence | TRAIN-06 | Long-running training; ADVANCE/HALT thresholds are safe placeholders pending Stage-0-pilot calibration | Deferred to Phase 43 smoke/pilot (ACC-05) |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 120s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
