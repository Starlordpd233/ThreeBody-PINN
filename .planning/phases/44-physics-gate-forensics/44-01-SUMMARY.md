---
phase: 44-physics-gate-forensics
plan: 01
wave: 1
requirements: [DIAG-01, DIAG-04]
status: complete
---

# 44-01 Summary — DIAG-01 ε_H distribution + D-07 surfaced

## Objective
Characterize the per-trajectory `eps_H` distribution over all 1,500 held-out
test trajectories from the preserved `metrics.json` ONLY (evaluator NOT invoked,
SCOPE-22), and surface the D-07 gate-statistic question as a STOP-protocol gap.

## What was built
- `evidence/diag01/eps_h_distribution.py` — deterministic, fail-closed analyzer
  (stdlib + numpy). Pre-registered uniform-vs-tail criterion stated BEFORE the
  verdict; asserts `len==1500`, exact `max==top-level eps_h`, exact per-entry
  key set; full-repr floats, `sort_keys`, cwd-independent.
- `evidence/diag01/eps_h_distribution.json` — the distribution output (5,114 B).
- `44-GAPS.md` — phase register with GAP-44-01 (11-field STOP schema).
- `v2.1-GAPS.md` — milestone index created (standing trigger), GAP-44-01 row.

## Key results (verified fact, cited to the JSON)
- **Uniform failure:** min `0.974125…` > `1e-5` → 1500/1500 trajectories
  exceed the reject threshold (`frac_exceeding_threshold = 1.0`); the *best*
  trajectory misses by ~5 orders of magnitude. Heavy right tail
  (max/median ≈ 106×, p99/median ≈ 24.7×).
- Distribution: min 0.9741, p50 2.2327, mean 5.6222, p99 56.1, max 237.2086.
- **No attribute separates the population:** by_variant (hierarchical 970 /
  standard 530) and by_fidelity (base 759 / gold 741) both span the full range
  with no ≥10× median gap.
- Worst trajectory: `id 1414`, `standard`, `base`, `eps_h = 237.2086…`.
- **D-07 confirmed & surfaced, not decided:** top-level `eps_h = 237.2086…` is
  EXACTLY `max(per_trajectory.eps_h)` (mean 5.6222, median 2.2327). Whether a
  worst-case max is the spec-intended gate statistic is GAP-44-01 (OPEN).

## Verification
- Byte-identical on re-run (`cmp` of two consecutive runs at the same commit).
- All fail-closed assertions pass; output is a deterministic function of the
  pinned input (SHA-256 recorded in `provenance.inputs`).

## Deviations
None. The plan executed as specified; all `must_haves` satisfied.
