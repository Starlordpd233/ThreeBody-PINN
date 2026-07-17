---
phase: 40
slug: stage-0-curriculum-training-loop-fut-04
status: validated
nyquist_compliant: true
wave_0_complete: true
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
| (scaffold) | 01 | 1 | TRAIN-01..07 (test contract) | — | N/A | unit | `python -m unittest tests.phase40.test_prohibitions -v` | ✅ W0 | ✅ green |
| (weights) | 02 | 2 | TRAIN-03 | — | N/A | unit | `python -m unittest tests.phase40.test_scheduled_weights -v` | ✅ W0 | ✅ green |
| (clip) | 02 | 2 | TRAIN-05 | — | N/A | unit | `python -m unittest tests.phase40.test_grad_clip -v` | ✅ W0 | ✅ green |
| (sampler) | 03 | 2 | TRAIN-04 | — | N/A | unit | `python -m unittest tests.phase40.test_collocation_sampler -v` | ✅ W0 | ✅ green |
| (preflight) | 03 | 2 | TRAIN-07 | — | N/A | unit | `python -m unittest tests.phase40.test_slbfgs_preflight -v` | ✅ W0 | ✅ green |
| (stage-exit) | 04 | 2 | TRAIN-06 | T-40-02 | weights_only-clean `state_dict` composition (CTX-44) | unit | `python -m unittest tests.phase40.test_stage_exit -v` | ✅ W0 | ✅ green |
| (inner loop) | 05 | 3 | TRAIN-02 | — | N/A | unit | `python -m unittest tests.phase40.test_optimizer_phase -v` | ✅ W0 | ✅ green |
| (outer loop) | 06 | 4 | TRAIN-01 | — | N/A | unit | `python -m unittest tests.phase40.test_controllers -v` | ✅ W0 | ✅ green |
| (config) | 02–05 | 2–3 | CTX-39/42 (TrainingConfig nested frozen dataclasses) | — | N/A | unit | `python -m unittest tests.phase40.test_config -v` | ✅ W0 | ✅ green |
| (checkpoint) | 04–07 | 2–3 | CTX-43/44 (CheckpointStore protocol + naive torch.save) | T-40-02 | weights_only=True on every load/rollback | unit | `python -m unittest tests.phase40.test_checkpoint -v` | ✅ W0 | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky. Exact task IDs live in the PLAN.md files (authoritative).*

---

## Wave 0 Requirements

- [x] `tests/phase40/__init__.py` — package marker
- [x] `tests/phase40/_fixtures.py` — stub model + stub `StageQuery`/batch source, mirroring `tests/phase39/_fixtures.py` conventions (SimpleNamespace-backed stub, not on-disk corpus)
- [x] Ten test modules (8 per RESEARCH Recommended Project Structure + `test_config` CTX-39/42 + `test_checkpoint` CTX-43/44): `test_controllers`, `test_optimizer_phase`, `test_scheduled_weights`, `test_collocation_sampler`, `test_grad_clip`, `test_stage_exit`, `test_slbfgs_preflight`, `test_prohibitions`, `test_config`, `test_checkpoint`
- [x] `tests/phase40/test_prohibitions.py` — extend the Phase 38/39 AST/discovery audit to `pinn/training/*.py` (no v1.3 imports, no hardcoded precision/device, no corpus-path access)
- [x] Framework install: none — `unittest` is stdlib

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Full Stage-0 end-to-end pilot convergence | TRAIN-06 | Long-running training; ADVANCE/HALT thresholds are safe placeholders pending Stage-0-pilot calibration | Deferred to Phase 43 smoke/pilot (ACC-05) |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 120s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved (2026-07-17 Nyquist validation audit; 163/163 tests green)

---

## Validation Audit 2026-07-17

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

**Method:** State-A audit of existing `40-VALIDATION.md`. Read all 40-01..09 PLAN/SUMMARY artifacts; built requirement-to-task map for TRAIN-01..07 plus CTX-39/42/43/44. Ran `conda run -n pinn-train python -m unittest discover -s tests/phase40 -p 'test_*.py' -v`: **163/163 OK (32.1 s)**. All 10 test modules (8 planned + `test_config` + `test_checkpoint`) classified COVERED; no auditor spawn required. Per-task map updated to ✅ green; frontmatter set `status: validated` / `nyquist_compliant: true` / `wave_0_complete: true`.

**Coverage summary:**

| Requirement | Test module(s) | Tests | Status |
|-------------|---------------|-------|--------|
| TRAIN-01 (outer loop) | `test_controllers` | 14 | COVERED |
| TRAIN-02 (inner loop) | `test_optimizer_phase` | 20 | COVERED |
| TRAIN-03 (scheduled weights) | `test_scheduled_weights` | 12 | COVERED |
| TRAIN-04 (collocation sampler) | `test_collocation_sampler` | 14 | COVERED |
| TRAIN-05 (grad clip) | `test_grad_clip` | 14 + prohibitions M1 | COVERED |
| TRAIN-06 (stage exit + wiring) | `test_stage_exit`, controllers/optimizer wiring | 22+ | COVERED |
| TRAIN-07 (sL-BFGS preflight) | `test_slbfgs_preflight` | 8 | COVERED |
| CTX-39/42 (config dataclasses) | `test_config` | 23 | COVERED |
| CTX-43/44 (checkpoint protocol) | `test_checkpoint` | 11 | COVERED |
| Prohibitions audit | `test_prohibitions` | 11 | COVERED |
