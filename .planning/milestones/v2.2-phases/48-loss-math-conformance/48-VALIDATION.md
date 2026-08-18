---
phase: 48
slug: loss-math-conformance
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-01
---

# Phase 48 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

Seeded by `/gsd-plan-phase 48` from `48-RESEARCH.md` §Validation Architecture
and bound to the four-plan execution set after planner/checker iteration 1.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.1.1 over the repository's existing unittest- and pytest-style modules |
| **Config file** | none dedicated — run from the repository root with explicit paths and `-q` |
| **Quick run command** | `.venv/bin/python -m pytest -q tests/phase48` |
| **Full suite command** | `.venv/bin/python -m pytest -q tests/phase38 tests/phase40 tests/phase41 tests/phase42 tests/phase46 tests/phase47 tests/phase48` |
| **Estimated runtime** | ~120 seconds (dataset-free synthetic fixtures plus the local MPS regression; no training or held-out access) |

**Known green baseline from research:**

- `tests/phase38/test_loss_catalog.py`, `tests/phase40/test_scheduled_weights.py`, and `tests/phase47/test_conf03_eps_h_wiring.py` → `32 passed, 89 subtests passed`.
- `tests/phase42/test_step_log_jsonl.py`, `tests/phase47/test_conf02_s_h_pipeline.py`, `tests/phase40/test_config.py`, and `tests/phase41/test_config_yaml.py` → `61 passed`.

The causal-floor proof must exercise a real MPS float32 tensor under the locked
`pinn-train` torch 2.12.1 environment. A CPU-only result is not evidence for
CONF-05 because the literal nearest-rounded `log(tiny)` result is positive on
CPU but flushes to exact zero on MPS.

**Locked target-backend probe (dependency-free because `pinn-train` has no
pytest):**

```bash
<home>/miniforge3/bin/conda run -n pinn-train python -c 'import torch; from pinn.loss_catalog import causal_physics_loss; assert torch.__version__.split("+", 1)[0] == "2.12.1", torch.__version__; assert torch.backends.mps.is_built() and torch.backends.mps.is_available(); device = torch.device("mps"); dtype = torch.float32; rbar = torch.tensor([1000.0, 1000.0], dtype=dtype, device=device); loss, details = causal_physics_loss(rbar, dtype=dtype, device=device, return_details=True); w = details["w_n"]; torch.mps.synchronize(); assert rbar.device.type == "mps" and w.device.type == "mps"; assert bool(torch.isfinite(loss).item()); assert bool(torch.all((w > 0) & (w <= 1)).item()); print(torch.__version__, w.tolist())'
```

---

## Sampling Rate

- **After every task commit:** Run the directly named Phase-48 test file plus the closest impacted existing module.
- **After every plan wave:** Run `.venv/bin/python -m pytest -q tests/phase38 tests/phase40 tests/phase41 tests/phase42 tests/phase46 tests/phase47 tests/phase48`.
- **Before `/gsd-verify-work`:** Run the full suite command above and `git diff --check`; all new Phase-48 tests and the existing `eps_H` assembly proof must be green; the locked MPS probe is a named, separately recorded, non-waivable gate at phase close.
- **Max feedback latency:** 120 seconds for the quick/targeted loop; the locked-environment MPS probe is additionally required at the CONF-05 task and phase gates.

---

## Per-Task Verification Map

Every row resolves to a task `<verify>` or `<automated>` block in the finalized
PLAN set.

| Req / Decision | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---|---|---|---|---|---|---|---|---|---|
| D-05/D-07 | 48-01 Task 1 | 1 | CONF-04 / TEST-02 | T-48-01 | Controller-to-catalog assembly rejects the obsolete `/9` value. | assembly unit | `.venv/bin/python -m pytest -q tests/phase48/test_loss_math_conformance.py -k rbar` | ❌ W0 | ⬜ pending |
| D-01..D-03 | 48-01 Task 2 | 1 | CONF-07 | T-48-03 | N/A | unit + regression | `.venv/bin/python -m pytest -q tests/phase48/test_loss_math_conformance.py tests/phase40/test_optimizer_phase.py -k 'data_huber or chunked_accumulation'` | ✅ existing chunk proof + ❌ W0 | ⬜ pending |
| D-13..D-15 | 48-02 Tasks 1-2 | 2 | CONF-06 / TEST-01 | T-48-04..06 | Resolved defaults and shipped inputs cannot silently activate Stage-0 energy supervision. | config + integration | `.venv/bin/python -m pytest -q tests/phase40/test_config.py tests/phase40/test_scheduled_weights.py tests/phase41/test_config_yaml.py tests/phase48/test_stage0_energy_config.py -k 'lambda_e or stage0'` | ✅ impacted existing + ❌ W0 | ⬜ pending |
| D-08..D-10 | 48-03 Tasks 1-2 | 2 | CONF-05 | T-48-07/T-48-09 | Backend underflow cannot erase later-time physics supervision. | unit + backend integration | `.venv/bin/python -m pytest -q tests/phase48/test_loss_math_conformance.py -k causal_clip` plus the locked dependency-free torch-2.12.1 MPS probe above | ❌ W0 | ⬜ pending |
| D-11 | 48-03 Tasks 1-2 | 2 | CONF-05 / TEST-01 | T-48-08/T-48-10 | Clip precision, upward-rounded exponent bound, and minimum weight are atomically persisted and fail closed on mismatch. | metadata integration | `.venv/bin/python -m pytest -q tests/phase48/test_clip_metadata.py` | ❌ W0 | ⬜ pending |
| D-16..D-19 | 48-04 Tasks 1-2 | 2 | INST-02 | T-48-11/T-48-13/T-48-14 | Diagnostic VJPs do not mutate `.grad`, clipping, optimizer updates, or graph lifetime. | unit + controller integration | `.venv/bin/python -m pytest -q tests/phase48/test_gradient_observability.py` | ❌ W0 | ⬜ pending |
| D-20 | 48-04 Task 2 | 2 | INST-02 | T-48-12 | Missing/non-finite statistics never serialize as a complete step. | JSONL integration | `.venv/bin/python -m pytest -q tests/phase48/test_gradient_observability.py tests/phase42/test_step_log_jsonl.py -k 'missing or nonfinite or complete or step_completed'` | ✅ impacted existing + ❌ W0 | ⬜ pending |
| D-21 | 48-02 Task 2; 48-03 Task 2 | 2 | TEST-01 | T-48-06/T-48-08 | Divergence-defending expectations are corrected atomically with their owner behavior. | regression | `.venv/bin/python -m pytest -q tests/phase40/test_config.py tests/phase41/test_config_yaml.py tests/phase38/test_loss_catalog.py tests/phase48/test_stage0_energy_config.py tests/phase48/test_clip_metadata.py` | ✅ impacted existing + ❌ W0 | ⬜ pending |
| D-22 | 48-01 Task 1; 48-03 Task 2 | 1/2 | TEST-02 | T-48-01/T-48-07 | Tests defend locked assembly inputs and focused clip behavior rather than divergent behavior. | assembly regression | `.venv/bin/python -m pytest -q tests/phase48/test_loss_math_conformance.py tests/phase47/test_conf03_eps_h_wiring.py -k 'rbar or eps_h_assembly_value or causal_clip'` | ✅ existing `eps_H` + ❌ W0 | ⬜ pending |
| D-23 | 48-01 Task 1; 48-04 Task 2 | 1/2 | CONF-04 / INST-02 | T-48-02/T-48-11 | Heavily edited controller/optimizer seams keep their existing regression suites green. | regression | .venv/bin/python -m pytest -q tests/phase40/test_controllers.py tests/phase41/test_controllers_ext.py tests/phase40/test_optimizer_phase.py | ✅ existing | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/phase48/__init__.py` — phase package marker if required by the chosen imports.
- [ ] `tests/phase48/test_loss_math_conformance.py` — CONF-04/05/07 and TEST-02 boundary proofs, including the real-MPS float32 arm.
- [ ] `tests/phase48/test_stage0_energy_config.py` — default and shipped-YAML Stage-0 exact-zero proof.
- [ ] `tests/phase48/test_clip_metadata.py` — strict fresh/resume clip-fact metadata and refusal behavior.
- [ ] `tests/phase48/test_gradient_observability.py` — Adam/L-BFGS non-contamination, raw/applied semantics, last-closure provenance, and validation-stash isolation.

Framework install: none needed — pytest, NumPy, PyYAML, and torch already exist in the repository environments.

---

## Manual-Only Verifications

All Phase-48 behaviors have automated verification. The target-version MPS probe
is an automated command run on the local supported backend; it is not waivable
as a manual inspection and must not be replaced with a CPU-only test.

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 120s for targeted checks
- [ ] Real-MPS float32 probe passes under locked torch 2.12.1 with `0 < w_n <= 1`
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
