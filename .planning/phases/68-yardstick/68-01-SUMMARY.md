---
phase: 68-yardstick
plan: 01
subsystem: pinn-verification
tags: [yardstick-audit, feasibility-scorecard, validation-gate, brutus-floor, gap-59-08, known-answer]
requires:
  - phase: 59-read-only-baseline-scorecard
    provides: "FEAS-01 scorecard (frozen in feasibility_scorecard_v1.json), scoring functions, census panels.json"
provides:
  - "pinn/verification/yardstick_audit.py: Complete fixed-panel audit runner and replay checker (--check)"
  - "tests/phase68: Full unit and synthetic tracer test suite (tests/phase68/test_yardstick_audit.py)"
  - "evidence/yardstick-audit.json: Committed audit results for 12 prediction/grid groups and 8 aggregates"
  - "68-AUDIT.md: Full known-answer audit report and analysis"
affects: [68-02, phase-69, milestone-v2.6]
actuals:
  tasks: 3
  commits: 4
tech-stack:
  added: []
  patterns:
    - "Guarded Stage0TrainingReader with require_stage0_training and process-level open attestation"
    - "Array digests via little-endian float64 SHA-256 for bitwise preservation"
    - "Strict reproducibility replay checker verifying commit in history, producer hashes, and canonical JSON equality"
key-files:
  created:
    - pinn/verification/yardstick_audit.py
    - tests/phase68/__init__.py
    - tests/phase68/test_yardstick_audit.py
    - .planning/phases/68-yardstick/evidence/yardstick-audit.json
    - .planning/phases/68-yardstick/68-AUDIT.md
key-decisions:
  - "Under FEAS-01 with Brutus explicit velocities, Brutus achieves Tier 3 on all systems (pos_E = 0.0 exact, eps_H <= 2.2e-11)."
  - "Under the production validation gate (centered finite-difference velocity), Brutus fails the 1e-5 gate across all panel systems (gold panel eps_H = 0.0238, base panel eps_H = 0.379), confirming GAP-59-08 empirically."
  - "Constant predictors conserve their own energy perfectly (eps_H = 0, SCS = -Infinity, verdict PASS) despite failing position completely (E > 1.14, Tier 0)."
  - "Strict physical_window (t <= 10.0) retains 125 samples for base systems (t in [0.0, 9.92]) dropping the 126th sample at t = 10.000000000000007 (+7.1e-15 float roundoff), whereas Phase 59 census retained 126 via t <= 10.0 + 1e-9; preserved as keyed evidence."
  - "Input precision rounding (float32 positions/times/masses) has negligible impact on gate error (<0.012% shift on gold Brutus); truncation error of finite differences dominates."
requirements-completed: [YARD-01]
verification:
  - kind: unit
    command: "<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest tests.phase68.test_yardstick_audit tests.phase59.test_scorecard tests.phase59.test_scorer_known_errors tests.phase59.test_split_allowlist tests.phase43.test_gate_boundary"
    status: pass
  - kind: replay
    command: "<home>/miniforge3/envs/pinn-train/bin/python -B -m pinn.verification.yardstick_audit --check .planning/phases/68-yardstick/evidence/yardstick-audit.json"
    status: pass
---

# Plan 68-01 Summary: The Yardstick Audit

Executed Plan 68-01 to audit every judging metric and gate on Brutus ground truth and the constant baseline predictor across Stage-0 training panel systems (1632, 851, 4658).

## 1. Tasks Completed

- **Task 68-01-01 (Tracer):** Implemented `pinn/verification/yardstick_audit.py` with `audit_pair`, `compute_fd_metrics`, `compute_fd_metrics_float32_input`, and `array_digest`. Added `tests/phase68/test_yardstick_audit.py` exercising synthetic pairs through `Stage0TrainingReader` with pre-open admission and strict data isolation.
  - Commit: `541849a9` (`feat(68-01): implement pair calculation and synthetic audit tracer`)
- **Task 68-01-02 (Fixed-Panel Capture & Replay):** Added `run_fixed_panel_audit` and `replay_check` CLI. Added comprehensive helper unit tests for array digests, constant motion FD metrics, SCS $-\infty$ vs NaN, gate and tier boundaries, strict horizon crossings, and replay failure cases.
  - Commits:
    - `e7763838` (`feat(68-01): complete fixed-panel audit and replay test coverage`)
    - `e95f0b84` (`fix(68-01): pass paths first to module_hashes in yardstick audit`)
    - `3d60908a` (`feat(68-01): refine census comparison and completeness checks in yardstick audit`)
- **Task 68-01-03 (Full Known-Answer Audit Capture & Report):** Captured full 12-row by 8-aggregate audit on Stage-0 training panel systems. Verified complete reproducibility via `--check`. Documented findings, caller map, and full tables in `68-AUDIT.md`.
  - Evidence Commit: `605d7ad6` (`evidence(68): record known-answer yardstick audit and report`)
  - Evidence SHA-256: `4b82c21918ba578c9f889cc21f1a93494d12aaa60940b2dac5ef073318922fe4`

## 2. Access Attestation

```json
{
  "schema": "phase59-files-opened/v1",
  "tool": "yardstick_audit",
  "data_root_source": "git_common_dir_default",
  "opened": {
    "train": 6,
    "validation": 0,
    "other_under_root": 0
  },
  "blocked_attempts": 0,
  "refused_before_open": 0,
  "test_split_opened": 0
}
```

Only the six admitted Stage-0 training records (`1632`, `851`, `4658` base and gold) were opened. Validation and test data remained untouched.

## 3. Handoff to Wave 2 (Plan 68-02)

Plan 68-01 provides the committed empirical foundation required for Owner Checkpoint 2 in Plan 68-02:
1. `68-CHECKPOINT-2.md` will present the committed audit packet, detailing the three C-7 velocity options (Option A: autograd velocity; Option B: finite-difference velocity; Option C: dual reporting).
2. The owner's explicit decision will resolve `GAP-59-08` and establish the proof-of-concept targets (C-2, C-4, C-5, C-6) in `68-CHECKPOINT-2-RULING.md`, routing any required scorecard amendments to milestone `v2.6`.
