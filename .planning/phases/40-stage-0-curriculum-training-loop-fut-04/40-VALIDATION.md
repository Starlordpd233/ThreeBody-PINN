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

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (existing `pinn/tests/` suite, `pinn-train` conda env) |
| **Config file** | existing repo pytest conventions (deferred-import skip guards) |
| **Quick run command** | `pytest pinn/tests -k "phase40 or training or curriculum" -q` |
| **Full suite command** | `pytest pinn/tests -q` |
| **Estimated runtime** | ~60 seconds |

---

## Sampling Rate

- **After every task commit:** Run the quick run command
- **After every plan wave:** Run the full suite command
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 120 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| (filled by planner) | — | — | TRAIN-01..07 | — | N/A | unit | (per-plan) | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] Test stubs for TRAIN-01..07 behaviors in `pinn/tests/` (planner assigns exact files)
- [ ] Shared fixtures reusing Phase 38/39 test conventions (deferred-import skip guards, typed sentinel exceptions)

*Existing pytest infrastructure covers the framework; no new test framework is installed.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Full Stage-0 end-to-end pilot convergence | TRAIN-06 | Long-running training; thresholds are placeholders pending Stage-0-pilot calibration (Phase 43) | Deferred to Phase 43 smoke/pilot |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 120s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
