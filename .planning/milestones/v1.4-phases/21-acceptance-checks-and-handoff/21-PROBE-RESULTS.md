# Phase 21: Validation Probe Results

Fresh execution date: 2026-06-08

Interpreter: `.venv/bin/python`

Environment evidence:

- `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/evidence/python_environment.stdout.txt`
- SHA-256: `1f625a2554749e62dad7d2cbec64ccfb585623e6da9079e4325ef5ad9eae6cb6`

All five Phase 21 disposable validation probes executed with exit code 0. Each probe's raw stdout is captured in a committed evidence file; this document summarizes that captured output rather than replacing it.

## 10.1 Scaling Consistency

- **Status:** PASS
- **Command:** `.venv/bin/python .planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_scaling.py`
- **Raw stdout evidence:** `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/evidence/probe_scaling.stdout.txt`
- **SHA-256:** `329ad79f02aa22fbc93e510644bfe8af4a1972ddcc7ed14ab759665cc5825dfc`
- **Observed metric:** `max_relative_error = 2.22e-16` across 3 non-unit scaling cases.
- **Pass criterion:** `relative_error < 1e-10`

## 10.2 COM Invariance

- **Status:** PASS
- **Command:** `.venv/bin/python .planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_com.py`
- **Raw stdout evidence:** `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/evidence/probe_com.stdout.txt`
- **SHA-256:** `e61bc6d1792b2b3940a4b3ca4b2e5f33470700e1d41a813f6fd0b767385e1db4`
- **Observed metric:** `COM magnitude: 7.90e-17`
- **Pass criterion:** `abs(COM) < 1e-10`

## 10.3 Componentwise AD on Synthetic Trajectory

- **Status:** PASS
- **Command:** `.venv/bin/python .planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_ad.py`
- **Raw stdout evidence:** `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/evidence/probe_ad.stdout.txt`
- **SHA-256:** `e9673901e8b0577dc5fdc92041b51890382aff8f02c50554616c76be771ac13b`
- **Observed metric:** `relative_error: 0.00e+00`
- **Pass criterion:** `relative_error < 1e-6`

## 10.4 Force-Energy Consistency

- **Status:** PASS
- **Command:** `.venv/bin/python .planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_force_energy.py`
- **Raw stdout evidence:** `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/evidence/probe_force_energy.stdout.txt`
- **SHA-256:** `06353a62bc256f6c960c09e3bef2d7de91f98f042e4c3a12f41a97211097012a`
- **Observed metric:** `relative_error: 1.62e-16; H_epsilon: -2.695067658127e+00; eps_train: 1.0e-05`
- **Pass criterion:** finite matched-Plummer Hamiltonian and force-gradient `relative_error < 1e-5`

## 10.5 Loss Stability Dry Run

- **Status:** PASS
- **Command:** `.venv/bin/python .planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/probes/probe_loss_stability.py`
- **Raw stdout evidence:** `.planning/milestones/v1.4-phases/21-acceptance-checks-and-handoff/evidence/probe_loss_stability.stdout.txt`
- **SHA-256:** `5fbd8d3500e8b22c000b847647d20fde6ad740bd16348d9dca39066a7a4e7da1`
- **Observed metric:** `total_loss=2.004441042593e+08; data=6.372e-02; ic=7.712e+01; physics=2.004e+08; energy=1.692e-01; angular=1.483e-01`
- **Pass criterion:** finite forward pass and finite data, IC, physics, energy, and angular-momentum loss scalars; no NaN/Inf
