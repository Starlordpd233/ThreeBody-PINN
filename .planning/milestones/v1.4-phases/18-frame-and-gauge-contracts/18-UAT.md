---
status: complete
phase: 18-frame-and-gauge-contracts
source:
  - 18-01-SUMMARY.md
  - 18-02-SUMMARY.md
  - 18-03-SUMMARY.md
  - 18-VERIFICATION.md
started: 2026-05-26T01:47:25Z
updated: 2026-05-26T01:47:25Z
mode: agent-audit
---

## Current Test

[testing complete]

## Tests

### 1. FRAME-01 Unified Preprocessing Contract
expected: `ctl_instruction.md` defines one preprocessing order for all IC/BRUTUS pairs: parse, mass-invariance check, COM recenter, zero-momentum boost, canonical ordering, canonical rotation gauge, global scaling, then assertions and stored metadata.
result: pass

### 2. FRAME-02 COM And Momentum Guarantees
expected: Framework specs state COM and total-momentum assertions for preprocessed samples and preserve the model-output hard mass-weighted COM projection contract.
result: pass

### 3. FRAME-03 Sampling-Frame Reconciliation
expected: `sampling_method.md` documents hierarchical post-perturbation COM/P offsets and standard quasi-random COM/P-by-construction behavior, while keeping the Phase 20.5 Sobol coordinate-allocation target untouched.
result: pass

### 4. FRAME-04 Full 3D Output Preservation
expected: The rotation gauge fixes only initial orientation; Jacobi velocities remain fully 3D and the model output remains 9D Cartesian positions, not planar or invariant-only.
result: pass

### 5. VER-05 Ledger And Gap Discipline
expected: B-05 and M3 are `VERIFIED` only under the authorized `AC-FRAME-01` structural closure; `AC-FRAME-02/03/04` remain reserved names with numeric criteria deferred to Phase 21; all Phase 18 gaps are `RESOLVED-WITH-INSTRUCTION`.
result: pass

### 6. Scope Boundaries And FUT-01 Handoff
expected: Phase 18 records FUT-01 frame/gauge code divergence without modifying `pinn/`, preserves the Phase 19 M4 text, and leaves Phase 21 numeric acceptance probes out of Phase 18 scope.
result: pass

## Summary

total: 6
passed: 6
issues: 0
pending: 0
skipped: 0
blocked: 0

## Audit Notes

- Parallel audit agents and local checks agreed that the core Phase 18 framework-spec work is complete and source-grounded.
- Initial verification found two process-artifact inaccuracies: stale B-05/M3 current-spec evidence citations and overbroad `AC-FRAME-01/02/03/04 structural checks passed` transition wording.
- The inaccuracies were corrected during this verification: B-05/M3 now cite current post-edit spec evidence, the B-05/ledger/18-03 plan transition wording now scopes structural closure to `AC-FRAME-01`, and `18-VALIDATION.md` frontmatter now matches its passed approval state.
- Fresh Phase 18 strict suite, GSD `audit-open`, and `git diff --check` passed after correction.

## Gaps

[none]
