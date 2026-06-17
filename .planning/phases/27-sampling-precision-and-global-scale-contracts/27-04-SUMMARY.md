---
phase: 27-sampling-precision-and-global-scale-contracts
plan: 04
type: execute-summary
executed_at: 2026-06-14
executed_by: gsd-executor-27-04
status: complete
requirements: [PIPE-09]
commits:
  - 731c795e spec(27-04): land PIPE-09 normative compute_globals contract in ctl §2.5
  - 95575fd9 docs(27-04): backfill SHA 731c795 into transition logs
---

# Plan 27-04 — PIPE-09 compute_globals — Execution Summary

## What was built

PIPE-09 normative `compute_globals` global-scale contract landed in `ctl_instruction.md §2.5`:
- Raw-mass `D = (G·T²)^(1/3) ≈ 4.6416` canonical (HC-6 / PHYS-01).
- Mass-fraction `D = (G·M_tot·T²)^(1/3) ≈ 6.694` and `M_tot_ref` rejected by name; **"No configuration parameter may select the mass-fraction form."**
- `E_scale` floor canonicalized `+1e-10 → +1e-8` (2-of-3 editable-spec majority; `pinn_architecture.md §5.2` already matched).
- Plummer-vs-additive-ε (PHYS-03) rule restated; `ε_inv = 1e-10` preserved.
- Admitted-set scope (post-Step-1A, post-blacklist, post-DATA-05-quarantine) per GAP-27-02 Option A.
- `evidence/compute-globals-D.md` cited by path; locked D value unchanged (D-03).
- SCS / Phase 28 untouched per D-14 dependents note.

## Artifacts produced

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` §2.5 — normative `compute_globals` contract paragraph + `E_scale = |median(E)| + 10^{-8}`.
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/compute-globals-D.md` — Status Transition Log advanced PENDING→IN_PROGRESS→FIX_APPLIED→VERIFIED.
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` — D=6.694 row (line 39) and per-finding transition log (line 444) at VERIFIED.
- `.planning/phases/27-sampling-precision-and-global-scale-contracts/ac-pipe-09.sh` — runnable AC-PIPE-09 (14 assertions: canonical-D + Plummer positive + 6.694/M_tot/E_scale/arch/SCS negative-controls + arch §5.2 consistency).
- `.planning/phases/27-sampling-precision-and-global-scale-contracts/27-VALIDATION.md` — flipped to `nyquist_compliant: true`, `wave_0_complete: true`, all rows green.

## Acceptance checks (full-suite re-run 2026-06-14)

| AC | Result | Notes |
|----|--------|-------|
| AC-PIPE-04 | PASS | `min(n_pts_cap, n_snapshots)` present; 50/50 replaced; DATA-06 medians cited |
| AC-PIPE-07 (inline) | PASS | float64 + Decimal + stale + DATA-05 rerun cited |
| AC-PIPE-08 | PASS | sample_replay/lookahead signatures + param_provenance preserved + doc-03/M16 forward ref |
| AC-PIPE-09 | PASS | All 14 assertions: raw-mass D=4.6416 + Plummer + admitted-set + 6.694/M_tot_ref/E_scale 1e-10 negative controls + arch §5.2 consistency + SCS untouched |
| AC-PIPE-01 (regression) | PASS | `## Step 1A — Trajectory Admission Gate` intact |
| AC-PIPE-06 (regression) | PASS | `param_provenance` preserved |
| AC-PIPE-10 (regression, conditional) | PASS | HDF5 canonical + schema_version present |

## Phase-exit gate (F-13/F-16)

All Phase 27 in-scope ledger rows at VERIFIED — no IN_PROGRESS/FIX_APPLIED:
- M12 (line 26) — VERIFIED
- G5 (line 33) — VERIFIED
- mass-drift (line 41) — VERIFIED
- footer (line 40) — VERIFIED
- D=6.694 (line 39) — VERIFIED

`27-GAPS.md` has no OPEN in-scope gap (GAP-27-02 RESOLVED-WITH-INSTRUCTION 2026-06-14, Option A).

## Deviations

None — locked D value unchanged; Plummer `ε_inv = 1e-10` preserved; arch §5.2 confirmed already canonical (no edit); SCS untouched.
