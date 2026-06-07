# Phase 21: Validation Handoff

This document provides a definitive list of spec changes to clean up in Phase 22, based on the reconciliation of Issue 01 findings.

## 1. Fixed
The following findings resulted in an explicit spec change and are marked as `VERIFIED` in the issue ledger:

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
Findings that were false positives or valid existing conventions:
- *None identified during v1.4 resolution that were kept in scope.*

## 3. Deferred
Findings that require future empirical validation or were not adjudicable from supplied files:

- **M6**: Not adjudicable from supplied files. The accessible consolidation map does not expose standalone M6 or M7 semantic categories. Revisit when source material is available.
- **M7**: Not adjudicable from supplied files. The accessible consolidation map does not expose standalone M6 or M7 semantic categories. Revisit when source material is available.

---
*Next Step: Phase 22 consumes this handoff while performing final presentation cleanup.*