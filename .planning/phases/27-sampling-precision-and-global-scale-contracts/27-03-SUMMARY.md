---
phase: 27
plan: 03
wave: 3
subsystem: framework-specs / data-pipeline
status: complete
completed: 2026-06-14
---

# Phase 27 Plan 03: PIPE-08 Stage-Query Interface Summary

**One-liner:** Landed the locked data-side stage-query contract (`sample_replay`/`sample_lookahead`) into `ctl_instruction.md` §2.6, confirmed `dt_out`/`n_snapshots` metadata, added FUT-01 arch visibility note, and recorded G5/PIPE-08 consistency — all with AC-PIPE-08 passing and D7 regression verified.

## Tasks Completed

| Task | Name | Status | Commit |
|------|------|--------|--------|
| 1 | A1 guard + author AC-PIPE-08 | Complete | (part of c647fc3) |
| 2 | Add stage-query sub-section + confirm §2.6 metadata + arch note | Complete | c647fc3 |
| 3 | Run AC-PIPE-08, record G5 consistency, D7 regression, same-commit close | Complete | c647fc3 + 8fb87fa |

## Files Changed

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — §2.6 metadata schema now explicitly names `n_snapshots`; net-new `#### Data-side stage-query interface` sub-section with locked signatures `sample_replay(n, max_stage)` and `sample_lookahead(n, stage)`; data-side semantics (cumulative $D_{\leq k}$ / next-stage $D_{k+1}$); SCOPE-11 blockquote deferral to doc-03 for M16 collocation-scaling and training-loop policy.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — §3.1 one-line visibility note that data-side loader exposes `sample_replay`/`sample_lookahead` (FUT-01 visibility).
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` — G5 per-finding note appended with PIPE-08 metadata-consistency line (G5 stays VERIFIED, not reopened).
- `.planning/phases/27-sampling-precision-and-global-scale-contracts/ac-pipe-08.sh` — runnable acceptance check (AC-PIPE-08) with positive assertions + blockquote-scoped negative control.

## Deviations from Plan

**None.** Plan executed exactly as written. No return-type/ordering/seeding invented (A1 guard satisfied at grounded level). No new gap surfaced.

## Verification Results

- **AC-PIPE-08:** ALL CHECKS PASSED (7/7)
  - [PASS] `sample_replay(n, max_stage)` signature present
  - [PASS] `sample_lookahead(n, stage)` signature present
  - [PASS] `dt_out` in metadata schema
  - [PASS] `n_snapshots` in metadata schema
  - [PASS] `param_provenance` preserved (PIPE-06 regression check)
  - [PASS] doc-03 / M16 forward-reference present
  - [PASS] No forbidden training-loop/collocation-density policy in stage-query sub-section (deferral note correctly blockquoted)
- **D7 regression (AC-PIPE-06):** `param_provenance` footer/default provenance text byte-identical to pre-edit state; D7 stays VERIFIED.
- **AC-PIPE-10:** Not triggered — stage-query text placed under §2.6, not near Step-1 item 6 (HDF5 region).

## Decisions Made

- **Placement (F-02):** Stage-query sub-section placed under §2.6 (metadata schema section) rather than co-located near Mini-Batch Construction (~1417), avoiding region-collision risk with Plan 27-01 edits and keeping the interface adjacent to the metadata fields it references.
- **A1 guard outcome:** Grounded at signature + data-side-semantics level; no return-type/ordering/seeding invented. Proceed signal recorded.
- **Negative control scope:** Blockquote-scoped — the SCOPE-11 boundary note is a blockquote, and the negative control filters blockquote lines before checking for forbidden policy text.

## Metrics

- Duration: ~12 minutes (3 tasks, 2 commits)
- Files modified: 4
- Acceptance checks: 1 authored, 1 passing
- Regression checks: 1 (D7/AC-PIPE-06), passing

## Known Stubs

None. All signatures and metadata fields are fully wired to grounded sources.

## Threat Flags

None. No new network endpoints, auth paths, file access patterns, or schema changes at trust boundaries introduced.

## Self-Check

- [x] `ctl_instruction.md` contains exact signatures
- [x] `pinn_architecture.md` visibility note present
- [x] `24-ISSUE-LEDGER.md` G5 note appended
- [x] `ac-pipe-08.sh` runnable and passing
- [x] Commit `c647fc3` exists on `milestone/v1.5`
- [x] Provenance commit `8fb87fa` exists on `milestone/v1.5`

**Self-Check: PASSED**
