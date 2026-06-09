# Phase 21: Validation Handoff

This handoff is the Phase 22 input for final framework-spec cleanup. It is grounded in the Phase 16 issue ledger, the current framework-spec SI metadata sections, and the repaired Phase 21 probe evidence.

## Evidence Used

- `21-PROBE-RESULTS.md` - hash-backed summary of fresh 2026-06-08 probe execution.
- `evidence/*.stdout.txt` - raw stdout for Python environment and all five probes.
- `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` - stable v1.4 issue ledger.
- `pinn_architecture.md:984-1009` - Section 10 acceptance checks.
- `ctl_instruction.md:1446-1448` and `stage_strat_revision.md:425-427` - retired SI entries.

## 1. Fixed

The following in-scope Issue 01 findings are `VERIFIED` in the Phase 16 issue ledger and are covered by prior phase evidence packets plus Phase 21 acceptance evidence where applicable:

- **B-01**: SIREN hidden-layer initialization
- **B-02**: Characteristic length and mass scaling
- **B-03**: Input dimensionality
- **B-04**: Input vector composition and orientation slots
- **B-05**: COM frame consistency
- **B-06**: 3D-vs-planar encoding and output contract
- **B-07**: Energy/Hamiltonian regularizer
- **B-08**: ALM scheduling and loss balancing
- **B-09**: Softening mismatch
- **B-10**: Dynamic omega0 scheduling
- **M1**: 11D IC versus 13D IC gap
- **M2**: Total dimension claims conflict
- **M3**: Scaling order and COM transform order
- **M4**: Constraint counting error
- **M5**: I_3 normalization map
- **M8**: LayerNorm attribution and affine default
- **M9**: Energy normalization realized support
- **M10**: Mass normalization realized support
- **D-02-NORM**: Raw-vs-bounded I_norm naming

## 2. Intentionally Unchanged

No in-scope Issue 01 finding is currently classified by the Phase 16 ledger as an intentionally unchanged valid existing convention. The ledger's non-fixed terminal state is `DEFERRED` for M6/M7 only.

## 3. Deferred

The following findings remain explicitly deferred:

- **M6**: Not adjudicable from supplied files. The accessible consolidation map does not expose standalone M6 or M7 semantic categories. Revisit only when source material is available.
- **M7**: Not adjudicable from supplied files. The accessible consolidation map does not expose standalone M6 or M7 semantic categories. Revisit only when source material is available.

## 4. SI Metadata Reconciliation

| Entry | Status | Evidence |
|---|---|---|
| `SI-CTL-001` | Retired with B-03 back-reference | `ctl_instruction.md:1446-1448` |
| `SI-SSR-001` | Retired with M5 back-reference | `stage_strat_revision.md:425-427` |
| `SI-PINN-001` | Not present in framework-spec SI sections; not synthesized | `git grep` at `v1.4-pre-phase-21` and current tree found planning references only |
| `SI-PINN-002` | Preserved untouched | `pinn_architecture.md:1017-1024` |
| `SI-PINN-003` | Preserved untouched | `pinn_architecture.md:1026-1030` |
| `SI-DQA-002` | Preserved untouched | `data_quality_assessment.md:318-322` |
| `SI-DQA-003` | Preserved untouched | `data_quality_assessment.md:324-327` |

## 5. Phase 22 Consumption Notes

- Phase 22 may clean presentation, rendering, author-comment disposition, and markdown/LaTeX formatting.
- Phase 22 must not reinterpret the v1.4 semantic decisions above unless it opens a new STOP-protocol gap and gets user instruction.
- Phase 22 should preserve the `.venv/bin/python` probe commands in Section 10 unless it also updates the evidence and validation artifacts.
- FUT-01 implementation work remains out of v1.4 scope; use `21-CODE-DIVERGENCE.md` for forward-pointing code-alignment hints.
