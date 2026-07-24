# Phase 44 Evidence — Reproduction Boundary

This directory holds the read-only forensic analysis for Phase 44 (Physics-Gate
Forensics, milestone v2.1). Every number in `44-DIAGNOSIS.md` traces back to an
artifact here. **Nothing in this phase re-runs the evaluator (SCOPE-22), trains
(SCOPE-23), edits a spec (SCOPE-24), or selects a remedy (SCOPE-26).**

## Layout

| Path | Role |
|------|------|
| `diag01/eps_h_distribution.py` → `diag01/eps_h_distribution.json` | DIAG-01: per-trajectory ε_H distribution (1,500 trajectories) |
| `diag02/loss_decomposition.py` → `diag02/loss_decomposition.json` | DIAG-02: five-term loss decomposition (smoke + 3 pilot seeds) |
| `diag03/seed_band.py` → `diag03/seed_band.json` | DIAG-03: three-seed band + held-out-split divergence + Phase 38 citation |
| `build_manifest.py` → `manifest.json` | Pins every input file by SHA-256 + git HEAD |

## Exact reproduction commands

Use the pinned absolute interpreter — **never bare `python3`** (the repo `.venv`
and system Pythons have no `torch`/`numpy`; the pinn-train conda env is off-PATH):

```sh
cd <repo-root>/.planning/phases/44-physics-gate-forensics/evidence
~/miniforge3/envs/pinn-train/bin/python3 diag01/eps_h_distribution.py
~/miniforge3/envs/pinn-train/bin/python3 diag02/loss_decomposition.py
~/miniforge3/envs/pinn-train/bin/python3 diag03/seed_band.py
~/miniforge3/envs/pinn-train/bin/python3 build_manifest.py
```

Each script resolves the repo root from `__file__`, so it is cwd-independent.
Inputs are read-only from `runs/`, `.planning/milestones/v2.0-*`, and the
framework specs; nothing under those paths is written.

## Self-check assertions that gate each output (fail-closed — nothing is written on any failure)

- **DIAG-01** — `len(per_trajectory) == 1500`; `max(per_trajectory.eps_h) ==
  metrics.json.eps_h` (exact float equality, no tolerance); each entry's key set
  is exactly `{eps_h, fidelity, id, variant}`. The uniform-vs-tail criterion is
  pre-registered in source and stated before the verdict.
- **DIAG-02** — every step record carries all 26 required keys (5 loss + 5 λ +
  16 diagnostic); the step set is exactly `{1..300}` per run; `lambda_l == 0.0`
  at all 300 steps (asserted); no loss term is imputed as zero.
- **DIAG-03** — `median != 0` asserted before the relative-span division; no
  values rounded before calculation; the Phase 38 rung is a verbatim citation
  flagged `CITATION-NOT-COMPUTATION`.
- **build_manifest** — every `(path, sha256)` recorded in the three diag
  provenance blocks must match the live tree exactly; any mismatch is treated as
  tamper evidence and the manifest is not written.

## Determinism

Outputs use `sort_keys=True`, full-repr floats, and no generated timestamps, so
the three diag JSONs are byte-identical across consecutive runs at the same
commit (verified with `cmp`). Non-finite floats (none observed in the retained
artifacts) would be serialized as explicit `"Infinity"`/`"NaN"` tokens to keep
the JSON valid. `manifest.json` records `git_head`, so it is a deterministic
function of the tree at a given commit.

## Convention note (recorded choice)

The standalone `manifest.json` is a **new Phase 44 convention**, assembled from
`pinn/verify.py`'s `git_head`/`git_head_available` bounded `git rev-parse HEAD`
mechanics plus Phase 43's inline sha256-dict shape (`{repo-relative path: hex
digest}`). It is the phase's single pinning record. This divergence from prior
phases (which embedded provenance inline per artifact) is intentional, not an
accident: a single cross-checked manifest lets `build_manifest.py` assert that
every diag script's recorded inputs still match the tree.
