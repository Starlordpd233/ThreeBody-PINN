---
phase: 38-pinn-model-rebuild-from-specs-fut-01
plan: "05"
subsystem: pinn
tags: [loss, huber, causal-physics, net-04, compose_total]
requires:
  - phase: 38-02
    provides: "network + COM projection head"
  - phase: 38-03
    provides: "PHYS-02 residual and batch-dimension contract"
provides:
  - "pinn/loss_catalog.py — five locked loss terms + LossWeights + compose_total"
  - "tests/phase38/test_loss_catalog.py — per-term δ / causal / finiteness / composer"
affects: [38-06, 40-training-loop, 42-ops-logging]
tech-stack:
  added: []
  patterns:
    - "frozen five-field LossWeights with construction-time validation"
    - "supplied-weights pure composer (no scheduling)"
    - "causal_physics_loss optional times ascending-order guard"
key-files:
  created:
    - pinn/loss_catalog.py
    - tests/phase38/test_loss_catalog.py
  modified: []
key-decisions:
  - "lambda_data enforced == 1.0 at LossWeights construction (§3.1 unweighted data)."
  - "soft_energy_loss consumes supplied eps_h metadata directly; does not recompute S_H."
  - "causal_physics_loss documents sorted-time precondition and raises ValueError on unordered times."
metrics:
  duration: "25 minutes"
  completed: "2026-07-13"
  tasks_completed: 3
  files_created: 2
status: complete
---

# Phase 38 Plan 05: Five-Term Loss Catalog Summary

Locked NET-04 loss catalog: data Huber, IC anchors, causal physics, soft-energy, angular-momentum, plus a pure supplied-weights composer.

## Performance

- **Duration:** ~25 minutes
- **Tasks:** 3/3
- **Files created:** 2

## Accomplishments

- Implemented `pinn/loss_catalog.py` with exactly five terms and no linear-momentum term.
- `LossWeights` is a frozen five-field container; rejects negative/NaN weights and `lambda_data != 1.0`.
- `compose_total` returns `LossTerms` (per-term scalars + weighted total) for Phase 42 logging.
- Contract suite green under `pinn-train` (11 tests).

## Task Commits

1. **Tasks 38-05-01..03 (tests + catalog)** — `9257928` (`feat`)

## Verification

```text
conda run -n pinn-train python -m unittest tests.phase38.test_loss_catalog -v
# Ran 11 tests — OK
```

## Decisions Made

- Data Huber operates on already-dimensionless COM-projected `r'`; `D_CHARACTERISTIC_LENGTH` is referenced so callers convert raw Brutus with `r' = r/D`.
- Causal weights use `Rbar.detach()` (stopgrad); optional `times` enforces ascending order.
- Soft-energy `eps_h` is operator/metadata-supplied (Phase 39/40); no in-term S_H.
