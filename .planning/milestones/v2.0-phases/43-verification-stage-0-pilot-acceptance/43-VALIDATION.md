---
phase: 43
slug: verification-stage-0-pilot-acceptance
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-07-20
---

# Phase 43 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | stdlib `unittest` |
| **Config file** | none — activate the `pinn-train` conda environment |
| **Quick run command** | `python -m unittest tests.phase43.test_<module> -v` |
| **Full suite command** | `python -m unittest discover -s tests/phase43 -v` |
| **Estimated runtime** | under 60 seconds, excluding manual real-data smoke and pilot runs |

---

## Sampling Rate

- **After every task commit:** Run the targeted `python -m unittest tests.phase43.test_<module> -v` module suite.
- **After every plan wave:** Run `python -m unittest discover -s tests/phase43 -v`.
- **Before `$gsd-verify-work`:** The full Phase 43 suite must be green; real-data smoke and pilot evidence must be present.
- **Max feedback latency:** 60 seconds for automated checks.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 43-01 | 01 | 1 | ACC-01 | T-43-01 | Verify ladder reports the first failed rung and writes the fail-closed fresh-marker contract. | unit | `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_verify_ladder -v` | ❌ W0 | ⬜ pending |
| 43-02 | 02 | 3 | ACC-03 | T-43-02 | Evaluation refuses invalid paths or checkpoints, produces an honest binary gate result, and keeps output within the allowed run directory. | unit | `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_gate_boundary tests.phase43.test_evaluate_gate tests.phase43.test_evaluate_edge_cases -v` | ❌ W0 | ⬜ pending |
| 43-03 | 03 | 2 | ACC-02 | T-43-03 | Real-data smoke configuration is accepted only when its data source, split manifest, and timing calibration are explicit and valid. | unit | `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_real_data_smoke_config tests.phase43.test_timing_calibration -v` | ❌ W0 | ⬜ pending |
| 43-04 | 04 | 3 | ACC-01 | T-43-04 | A long-run launch is rejected when no valid timing forecast or verify marker exists; the 30-minute boundary remains permitted. | unit | `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_verify_gate -v` | ❌ W0 | ⬜ pending |
| 43-05 | 05 | 4 | ACC-04 | T-43-05 | Final summaries include completion evidence and remain explicit about unavailable, failed, or interrupted metrics. | unit | `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_summary_enrichment tests.phase43.test_summary_honesty -v` | ❌ W0 | ⬜ pending |
| 43-06 | 06 | 5 | ACC-02 | T-43-06 | The manual smoke evidence records checkpoints, resume behavior, measured seconds per step, and any honest failure disposition. | manual | `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_smoke -v` | ❌ W0 | ⬜ pending |
| 43-07 | 07 | 6 | ACC-05 | T-43-07 | Pilot evidence retains every seed outcome, computes the observed spread, and marks fewer than two completed seeds low-confidence. | unit + manual | `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_pilot_calibration -v` | ❌ W0 | ⬜ pending |
| 43-08 | 08 | 7 | ACC-06 | T-43-08 | A `go` verdict cannot be rendered from a failing acceptance gate; the handoff identifies shipped, placeholder, and deferred work. | unit + manual | `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_verdict_grounding -v` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/phase43/__init__.py` — shared Phase 43 test helpers and skip phrase.
- [ ] `tests/phase43/_fixtures.py` — small dataset-free fixtures for gate-boundary and honesty tests.
- [ ] No framework installation — the existing `pinn-train` environment supplies `unittest` dependencies.
- [ ] Fold the existing Phase 42 s/step TODO into the ACC-02 smoke test rather than adding a duplicate assertion.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| ~5-minute Stage-0 smoke, including Ctrl-C/resume | ACC-02 | Requires the real corpus and measured local timing. | Run the smoke command after the verify ladder passes; retain its run directory and record the measured seconds per step and checkpoint/resume evidence. |
| Two or three seeded Stage-0 pilot runs and threshold calibration | ACC-05 | Depends on observed variance and owner ratification, not deterministic unit-test input. | Run the approved pilot seeds, preserve every seed outcome, calculate the band from recorded results, and pause for R-1/R-2 owner ratification. |
| Go / adjust / rethink milestone verdict | ACC-06 | Requires owner judgment over real smoke/pilot evidence. | Review the acceptance gate, verification evidence, calibration note, and handoff; record the owner-approved verdict and rationale. |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies.
- [ ] Sampling continuity: no three consecutive tasks lack automated verification.
- [ ] Wave 0 covers all missing test references.
- [ ] No watch-mode flags.
- [ ] Feedback latency < 60 seconds for automated checks.
- [ ] `nyquist_compliant: true` set in frontmatter.

**Approval:** pending
