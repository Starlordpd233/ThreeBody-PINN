---
phase: 38-pinn-model-rebuild-from-specs-fut-01
plan: "06"
subsystem: verification
tags: [overfit, net-05, prohibitions, evidence, adam]
requires:
  - phase: 38-04
    provides: "gradcheck + residual probe grammar and evidence dirs"
  - phase: 38-05
    provides: "five-term loss catalog"
provides:
  - "pinn/verification/overfit_probe.py — rung-4 data-path overfit CLI"
  - "tests/phase38/test_overfit_probe.py — >=1e3x, fail-loud, diagnostics"
  - "tests/phase38/test_prohibitions.py — endpoint+history spec identity, write spy, AST"
affects: [39-dataset-adapter, 40-training-loop, 43-training-pilot]
tech-stack:
  added: []
  patterns:
    - "fixed zeros(13) IC13 placeholder for Phase-38 overfit smoke"
    - "input-available full-stack diagnostics finiteness-gated"
    - "glob-discovered Phase-38 module AST prohibition checks"
key-files:
  created:
    - pinn/verification/overfit_probe.py
    - tests/phase38/test_overfit_probe.py
    - tests/phase38/test_prohibitions.py
  modified: []
key-decisions:
  - "IC13_placeholder = zeros(13); physically-normalized IC13 deferred to Phase 39."
  - "Soft-energy recorded 'not evaluated — requires Phase 39/40 metadata' unless --eps-h."
  - "Pass-gate calibration on synthetic 2-snapshot fixture: Adam lr=1e-4 reaches >=1e3x in ~74 steps; CLI defaults remain max-steps=3000 / lr=1e-3 (uncalibrated build knobs)."
  - "Real-trajectory rung 3/4 phase-close DEFERRED (no Brutus payload in worktree)."
metrics:
  duration: "45 minutes"
  completed: "2026-07-13"
  tasks_completed: 3
  files_created: 3
status: complete
---

# Phase 38 Plan 06: Overfit Probe + Prohibitions Summary

Rung-4 data-path overfit and phase-wide mechanical prohibition checks close NET-05 and CTX-32.

## Performance

- **Duration:** ~45 minutes
- **Tasks:** 3/3
- **Files created:** 3 (+ SUMMARY, GAPS)

## Accomplishments

- Shipped `pinn/verification/overfit_probe.py`: Adam DATA-Huber overfit through real model + COM head; `tau_ic13 = [2u-1, zeros(13)]`; fail-loud on NaN/cap/non-finite diagnostics; evidence with ratio/LR/ic13_placeholder/COM offset.
- Contract suite covers PASS (>=1e3x), soft-energy disposition, COM warning, CLI arms, AST no-precision-default.
- Prohibitions: endpoint sha256 + history-aware git-log for both framework specs; write spy over I/O entry points; AST precision/v1.3 checks over glob-discovered `pinn/**/*.py`.
- Full `tests/phase38` discover: **128 tests OK** under `pinn-train`.
- Dual CLI launches on synthetic fixture: both exit 0, ratio ≈ 1691.

## Task Commits

(See git log for plan-06 feat/test/docs commits under this summary.)

## Verification

```text
conda run -n pinn-train python -m unittest tests.phase38.test_overfit_probe -v   # 10 OK
conda run -n pinn-train python -m unittest tests.phase38.test_prohibitions -v   # 6 OK
conda run -n pinn-train python -m unittest discover -s tests/phase38 -p 'test_*.py' -v  # 128 OK
python -m pinn.verification.overfit_probe --precision float64 --device cpu \
  --path <tmp synthetic> --max-steps 5000 --lr 1e-4 --evidence-root <tmp>  # PASS x2
```

## Phase-close gate

Real Brutus trajectory rung 3/4 evidence was **DEFERRED** at plan-06 completion (payload absent) — and **closed 2026-07-13 via decision B**: the admitted `standard_quasi_random_gold_standard/0000` trajectory was copied into the worktree and both rungs re-run PASS (residual Gate A 1.5e-15 / Gate B median 0.00647; overfit ratio 1097.6). See `38-GAPS.md` (GAP-38-01 RESOLVED-WITH-INSTRUCTION), `v2.0-GAPS.md`, and `38-VERIFICATION.md`.
