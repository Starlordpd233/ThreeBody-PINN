---
phase: 27-sampling-precision-and-global-scale-contracts
plan: 01
subsystem: data-pipeline
wave: 1
requirement: PIPE-04
status: complete
completed: 2026-06-14
---

# Phase 27 Plan 01: M12 Points-per-Trajectory Data-Loss Sampling Contract (PIPE-04) Summary

**One-liner:** Landed the locked M12 `min(n_pts_cap, n_snapshots)` without-replacement sampling contract into `ctl_instruction.md` Mini-Batch Construction, advanced M12 and G5 ledger rows to VERIFIED, and authored AC-PIPE-04 runnable acceptance check.

## Files Changed

| File | Action | Description |
|------|--------|-------------|
| `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` | Modified | Mini-Batch Construction (~1417): replaced stale "50% uniform / 50% weighted" prose with locked M12 contract blockquote |
| `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` | Modified | §3.1 (~351): added code-default note pointing `points_per_trajectory=32` to ctl contract |
| `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` | Modified | M12 row: PENDING -> VERIFIED; G5 row: PENDING -> VERIFIED (closes-with-M12); transition logs backfilled with SHA 6e81d14f |
| `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/m11-m12-severity.md` | Modified | M12 status transition log: IN_PROGRESS -> FIX_APPLIED -> VERIFIED; SHA backfilled |
| `.planning/phases/27-sampling-precision-and-global-scale-contracts/ac-pipe-04.sh` | Created | Runnable AC-PIPE-04 acceptance check with 8 region-scoped assertions |

## Commits

| SHA | Type | Message |
|-----|------|---------|
| `6e81d14f` | `spec(27-01)` | Land M12 points-per-trajectory data-loss sampling contract (PIPE-04) |
| `da2149d` | `verify(27-01)` | Backfill commit sha 6e81d14f into M12 and G5 transition logs |

## Verification Results

### AC-PIPE-04 (Post-Edit)
All 8 assertions PASS:
1. `min(n_pts_cap, n_snapshots)` present in Mini-Batch region
2. `without replacement` present
3. Cap 32 flagged as example/non-evidence-based
4. 0.5 factor appears ONLY in rejection context (vacuous per F-22)
5. DATA-06 medians (61/127/1003) cited
6. `m11-m12-severity.md` packet cited
7. `n_snapshots`/`dt_out` metadata + M16/doc-03 deferral present
8. Stale 50/50 prose replaced; curriculum table (Replay set / Look-ahead set) preserved

### AC-PIPE-01 Regression (B-06)
B-06 region byte-stable; no shared text touched. `## Step 1A`, `final_timestep >= 9.5`, `SCS > -5` all present. B-06 stays VERIFIED.

## Deviations from Plan

None. Plan executed exactly as written.

## Threat Register

| Threat | Status | Mitigation |
|--------|--------|------------|
| T-27-SPEC-DRIFT | Mitigated | Verbatim transcription from m11-m12-severity.md:107; AC-PIPE-04 asserts packet citation + DATA-06 medians |
| T-27-REGRESS | Mitigated | B-06 region byte-stable; no AC-PIPE-01 regression re-check required |

## Next-Wave Readiness

- Wave 2 (PIPE-07 precision) can proceed independently.
- Wave 3 (PIPE-08 stage-query) depends on PIPE-04 metadata exposure (`n_snapshots`, `dt_out`) now landed.
- Wave 4 (PIPE-09 compute_globals) is fully independent.

## Self-Check: PASSED

- [x] All created files exist on disk
- [x] Commit 6e81d14f exists in git log
- [x] Commit da2149d exists in git log
- [x] AC-PIPE-04 check runs and passes against edited ctl_instruction.md
- [x] M12 row shows VERIFIED in ledger
- [x] G5 row shows VERIFIED in ledger
- [x] No `0.5 * n_snapshots` operative rule anywhere in spec (the only `0.5` token in Mini-Batch region is the explicit rejection line "No `0.5 x n_snapshots` factor is imposed", per F-22 vacuous negative control)
