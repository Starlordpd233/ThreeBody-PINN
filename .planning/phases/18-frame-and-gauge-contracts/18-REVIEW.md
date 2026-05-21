---
phase: 18-frame-and-gauge-contracts
status: clean
depth: standard
files_reviewed: 3
findings:
  critical: 0
  warning: 0
  info: 0
  total: 0
created: 2026-05-21T05:31:38Z
reviewer: codex-inline
scope:
  - pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
  - pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
  - pinn_instruction/markdown_conversion/framework-specs/sampling_method.md
---

# Phase 18 Code Review

Status: clean after one source-backed prose correction.

## Scope

- `ctl_instruction.md` - reviewed the unified preprocessing pipeline, canonical ordering, rotation gauge, global scaling, metadata, and FRAME-04 3D Cartesian guard.
- `pinn_architecture.md` - reviewed the FRAME-02 output-side mass-weighted COM projection cross-reference.
- `sampling_method.md` - reviewed the FRAME-03 hierarchical and quasi-random frame notes and the adjacent quasi-random momentum-conservation prose.

## Findings

None remaining.

## Review Notes

- The initial review found one grounded inconsistency: the inherited quasi-random momentum sentence said the sampler adjusted the velocity of a fixed particle, while `simulation_data/Scripts/ic_generation/ic_generation_utils.py` sets `v1_batch = -v2_batch / 2` and `v3_batch = -v2_batch / 2`.
- This did not require a new gap because `18-CONTEXT.md` D-10 and `18-GAPS.md` GAP-18-02 resolution explicitly make `simulation_data/` authoritative for FRAME-03 `sampling_method.md` edits.
- Commit `34cd746` corrected only that momentum-conservation sentence; the Phase 20.5 Sobol coordinate-allocation target text remains untouched.

## Self-Check: PASSED

- No `pinn/` implementation files were modified.
- No unresolved review findings remain in the reviewed framework-spec scope.
- The review artifact is advisory and does not define Phase 21 numeric acceptance-check pass criteria.
