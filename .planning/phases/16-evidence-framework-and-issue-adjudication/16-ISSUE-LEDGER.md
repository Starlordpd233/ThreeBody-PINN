---
phase: 16
slug: evidence-framework-and-issue-adjudication
status: draft
created: 2026-05-16
total_findings: 20
in_scope_findings: 18
deferred_findings: 2
traceability_verified: true
last_verified_traceability: "30/30 v1.4 requirements mapped exactly once - verified 2026-05-16 against REQUIREMENTS.md §Traceability"
---

# Phase 16 Issue Ledger

## Status Table

| ID | Title | Phase | Status | Verdict | Sources Disagree? | Evidence Packet | Acceptance Check | Spec Section | Dependents | Last Updated |
|----|-------|-------|--------|---------|-------------------|-----------------|------------------|--------------|------------|--------------|
| B-01 | SIREN hidden-layer initialization | 20 | PENDING | - | NO | evidence/B-01.md | AC-ARCH-01 | pinn_architecture.md | B-10 | 2026-05-16 |
| B-02 | Characteristic length and mass scaling | 19 | IN_PROGRESS | accept-resolution | YES - EVID-05 required | evidence/B-02.md | AC-PHYS-01 | ctl_instruction.md; pinn_architecture.md | B-09, M3 | 2026-05-22 |
| B-03 | Input dimensionality | 17 | VERIFIED | accept-resolution | NO | evidence/B-03.md | AC-IO-01 | ctl_instruction.md; pinn_architecture.md | B-04, M1, M2 | 2026-05-19 |
| B-04 | Input vector composition and orientation slots | 17 | VERIFIED | accept-resolution | YES - EVID-05 required | evidence/B-04.md | AC-IO-02 | ctl_instruction.md; pinn_architecture.md | B-03, M1, M2 | 2026-05-19 |
| B-05 | COM frame consistency | 18 | VERIFIED | accept-resolution | NO | evidence/B-05.md | AC-FRAME-01 | ctl_instruction.md; pinn_architecture.md; sampling_method.md | M3, B-11-folded-into-B-05 | 2026-05-21 |
| B-06 | 3D-vs-planar encoding and output contract | 17 | VERIFIED | accept-resolution | NO | evidence/B-06.md | AC-IO-03 | pinn_architecture.md; ctl_instruction.md | - | 2026-05-19 |
| B-07 | Energy/Hamiltonian regularizer | 19 | PENDING | - | NO | evidence/B-07.md | AC-PHYS-04 | pinn_architecture.md | - | 2026-05-16 |
| B-08 | ALM scheduling and loss balancing | 19 | PENDING | - | NO | evidence/B-08.md | AC-PHYS-05 | pinn_architecture.md | - | 2026-05-16 |
| B-09 | Softening mismatch | 19 | PENDING | - | YES - EVID-05 required | evidence/B-09.md | AC-PHYS-03 | ctl_instruction.md; pinn_architecture.md | B-02, PHYS-04, PHYS-05 | 2026-05-16 |
| B-10 | Dynamic omega0 scheduling | 20 | PENDING | - | NO | evidence/B-10.md | AC-ARCH-01 | pinn_architecture.md | - | 2026-05-16 |
| M1 | 11D IC versus 13D IC gap | 17 | VERIFIED | accept-resolution | NO | evidence/M1.md | AC-IO-02 | ctl_instruction.md; pinn_architecture.md | - | 2026-05-19 |
| M2 | Total dimension claims conflict | 17 | VERIFIED | accept-resolution | NO | evidence/M2.md | AC-IO-01 | ctl_instruction.md; pinn_architecture.md | - | 2026-05-19 |
| M3 | Scaling order and COM transform order | 18 | VERIFIED | accept-resolution | NO | evidence/M3.md | AC-FRAME-01 | ctl_instruction.md | - | 2026-05-21 |
| M4 | Constraint counting error | 19 | IN_PROGRESS | accept-resolution | YES - EVID-05 required | evidence/M4.md | AC-PHYS-06 | ctl_instruction.md | - | 2026-05-22 |
| M5 | I_3 normalization map | 20 | PENDING | - | YES - EVID-05 required | evidence/M5.md | AC-ARCH-03 | ctl_instruction.md; data-processing-pipeline-full.py *(pre-2026-05-19; now v1.3-era artifact, not spec)* | - | 2026-05-16 |
| M6 | Deferred finding M6 | 21 | DEFERRED | defer-with-blocker | NO | - | AC-VER-03 | - | - | 2026-05-16 |
| M7 | Deferred finding M7 | 21 | DEFERRED | defer-with-blocker | NO | - | AC-VER-03 | - | - | 2026-05-16 |
| M8 | LayerNorm attribution and affine default | 20 | PENDING | - | NO | evidence/M8.md | AC-ARCH-02 | pinn_architecture.md | ARCH-02 | 2026-05-16 |
| M9 | Energy normalization realized support | 20 | PENDING | - | NO | evidence/M9.md | AC-ARCH-05 | ctl_instruction.md | - | 2026-05-16 |
| M10 | Mass normalization realized support | 20 | PENDING | - | NO | evidence/M10.md | AC-ARCH-05 | ctl_instruction.md | - | 2026-05-16 |

## Notes

30/30 v1.4 requirements mapped exactly once - see REQUIREMENTS.md §Traceability. This ledger records the verification statement only; REQUIREMENTS.md remains the source of truth.

## Lifecycle Rules

The forward status path is exactly `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED`.

`DEFERRED` is an absorbing state and requires a written blocker. `FIX_APPLIED` is not closure. `VERIFIED` requires a passing acceptance check for the finding's AC-ID.

Audit string: FIX_APPLIED is not closure; VERIFIED requires a passing acceptance check.

A batch is one GSD plan (`NN-NN-PLAN.md`). After every batch of spec or code edits in Phases 17-21, the executing agent re-runs each `VERIFIED` finding's acceptance check if that finding appears as a transitive dependent of any finding edited by the batch. Any regression returns the affected finding to `IN_PROGRESS` and blocks phase exit until re-fixed and re-verified.

The phase-exit gate permits only `VERIFIED` or `DEFERRED` for in-scope findings. No phase exits with any in-scope finding at `IN_PROGRESS` or `FIX_APPLIED`.

## Dependency Source Note

Initial Dependents values use the locked D-10 entries. The exact `## Cross-Issue Interactions` heading was verified in `pinn_instruction/issues/01-architecture-and-physics-foundations.md`, while `ctl_pinn_resolution.md` contributes supporting Verified Audit Matrix and dependency-ordered roadmap anchors.

## Per-Finding Notes

Status transition log entries must include date, commit short SHA, status transition, and actor / plan reference.

### B-01: SIREN hidden-layer initialization

Evidence packet: evidence/B-01.md

Acceptance check: AC-ARCH-01

Shared acceptance check: AC-ARCH-01 also covers other IDs B-01 and B-10.

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)
- 2026-05-22 EDIT_SHA PENDING -> IN_PROGRESS (Phase 19 P01 Task 1)

### B-02: Characteristic length and mass scaling

Evidence packet: evidence/B-02.md

Sources disagree: contested; EVID-05 required; no verdict assigned in Phase 16.

Acceptance check: AC-PHYS-01

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)

### B-03: Input dimensionality

Evidence packet: evidence/B-03.md

Acceptance check: AC-IO-01

Shared acceptance check: AC-IO-01 also covers other IDs B-03 and M2.

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)
- 2026-05-19 884efd3 PENDING -> IN_PROGRESS (Phase 17 P01 Task 1)
- 2026-05-19 50650a3 IN_PROGRESS -> FIX_APPLIED (Phase 17 P01 Task 3; input spec edits applied)
- 2026-05-19 50650a3 FIX_APPLIED -> VERIFIED (Phase 17 P01 Task 3; AC-IO-01/AC-IO-02 passed)

### B-04: Input vector composition and orientation slots

Evidence packet: evidence/B-04.md

Sources disagree: contested; EVID-05 required; no verdict assigned in Phase 16.

Acceptance check: AC-IO-02

Shared acceptance check: AC-IO-02 also covers other IDs B-04 and M1.

EVID-05 candidate set (corrected 2026-05-18; see 16-CONTEXT.md Amendment 2026-05-18):
- Option A: trig encoding for 3 angles (issue doc §5.3 / recommended-A path)
- Option B: shape invariants + direction cosines (issue doc "Recommended Option B")
- Option C: reconstructive Jacobi-state IC₁₃ (resolution doc §5.2–5.4; rejects A and B)
- Option D: codify status quo — live code's `I₁, I₂, I₃ + θ₁, θ₂` hybrid (pinn/data-processing-pipeline-full.py:1062–1146) *(pre-2026-05-19; now v1.3-era artifact only, not a v1.4 candidate)*

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)
- 2026-05-18 AMEND_REC PENDING -> PENDING (candidate set corrected from 2-option to 4-option framing; no status change; recorded in 16-CONTEXT.md Amendment)
- 2026-05-19 884efd3 PENDING -> IN_PROGRESS (Phase 17 P01 Task 1)
- 2026-05-19 50650a3 IN_PROGRESS -> FIX_APPLIED (Phase 17 P01 Task 3; input spec edits applied)
- 2026-05-19 50650a3 FIX_APPLIED -> VERIFIED (Phase 17 P01 Task 3; AC-IO-01/AC-IO-02 passed)

### B-05: COM frame consistency

Evidence packet: evidence/B-05.md

B-11 folded into B-05 because both concern COM/mass consistency.

Acceptance check: AC-FRAME-01

Shared acceptance check: AC-FRAME-01 also covers other IDs B-05 and M3.

Phase 18 reserved sibling acceptance-check names for Phase 21:
- AC-FRAME-02: COM/momentum assertions for preprocessed samples and model outputs.
- AC-FRAME-03: hierarchical / quasi-random sampling-frame reconciliation.
- AC-FRAME-04: 3D Cartesian output preserved.

Phase 21 defines numeric pass criteria and executes disposable probes; Phase 18 reserves names only.

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)
- 2026-05-21 d31e82c PENDING -> IN_PROGRESS (Phase 18 P01 Task 1)
- 2026-05-21 a940474 IN_PROGRESS -> FIX_APPLIED (Phase 18 P02 Task 3; sampling-frame spec edit applied)
- 2026-05-21 98bc955 FIX_APPLIED -> VERIFIED (Phase 18 P03 Task 2; AC-FRAME-01 structural closure passed; FRAME-02/03/04 markers verified with numeric criteria deferred to Phase 21)

### B-06: 3D-vs-planar encoding and output contract

Evidence packet: evidence/B-06.md

Acceptance check: AC-IO-03

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)
- 2026-05-19 a052e35 PENDING -> IN_PROGRESS (Phase 17 P02 Task 1)
- 2026-05-19 55c1805 IN_PROGRESS -> FIX_APPLIED (Phase 17 P02 Task 3; output spec edits applied)
- 2026-05-19 55c1805 FIX_APPLIED -> VERIFIED (Phase 17 P02 Task 3; AC-IO-03 passed)

### B-07: Energy/Hamiltonian regularizer

Evidence packet: evidence/B-07.md

Acceptance check: AC-PHYS-04

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)

### B-08: ALM scheduling and loss balancing

Evidence packet: evidence/B-08.md

Acceptance check: AC-PHYS-05

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)

### B-09: Softening mismatch

Evidence packet: evidence/B-09.md

Sources disagree: contested; EVID-05 required; no verdict assigned in Phase 16.

Acceptance check: AC-PHYS-03

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)

### B-10: Dynamic omega0 scheduling

Evidence packet: evidence/B-10.md

Acceptance check: AC-ARCH-01

Shared acceptance check: AC-ARCH-01 also covers other IDs B-01 and B-10.

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)

### M1: 11D IC versus 13D IC gap

Evidence packet: evidence/M1.md

Acceptance check: AC-IO-02

Shared acceptance check: AC-IO-02 also covers other IDs B-04 and M1.

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)
- 2026-05-19 884efd3 PENDING -> IN_PROGRESS (Phase 17 P01 Task 1)
- 2026-05-19 50650a3 IN_PROGRESS -> FIX_APPLIED (Phase 17 P01 Task 3; input spec edits applied)
- 2026-05-19 50650a3 FIX_APPLIED -> VERIFIED (Phase 17 P01 Task 3; AC-IO-01/AC-IO-02 passed)

### M2: Total dimension claims conflict

Evidence packet: evidence/M2.md

Acceptance check: AC-IO-01

Shared acceptance check: AC-IO-01 also covers other IDs B-03 and M2.

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)
- 2026-05-19 884efd3 PENDING -> IN_PROGRESS (Phase 17 P01 Task 1)
- 2026-05-19 50650a3 IN_PROGRESS -> FIX_APPLIED (Phase 17 P01 Task 3; input spec edits applied)
- 2026-05-19 50650a3 FIX_APPLIED -> VERIFIED (Phase 17 P01 Task 3; AC-IO-01/AC-IO-02 passed)

### M3: Scaling order and COM transform order

Evidence packet: evidence/M3.md

Acceptance check: AC-FRAME-01

Shared acceptance check: AC-FRAME-01 also covers other IDs B-05 and M3.

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)
- 2026-05-21 d31e82c PENDING -> IN_PROGRESS (Phase 18 P01 Task 1)
- 2026-05-21 83d6a0a IN_PROGRESS -> FIX_APPLIED (Phase 18 P01 Task 2; scaling-order spec edit applied)
- 2026-05-21 26d9627 FIX_APPLIED -> VERIFIED (Phase 18 P01 Task 3; AC-FRAME-01 scaling-order checks passed)

### M4: Constraint counting error

Evidence packet: evidence/M4.md

Phase 19 reclassification (2026-05-22): Sources Disagree changed from NO to YES - EVID-05 required.
Phase 16 seed marked NO in error; the requirement language (PHYS-06) and actual source positions
both indicate EVID-05 is required. Adjudicated in Phase 19 P01 per `evidence/M4.md`.

Acceptance check: AC-PHYS-06

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)
- 2026-05-22 EDIT_SHA PENDING -> IN_PROGRESS (Phase 19 P01 Task 1)

### M5: I_3 normalization map

Evidence packet: evidence/M5.md

Sources disagree: contested; EVID-05 required; no verdict assigned in Phase 16.

Acceptance check: AC-ARCH-03

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)

### M6: Deferred finding M6

Status: DEFERRED

Verdict: defer-with-blocker

Acceptance check: AC-VER-03

Shared acceptance check: AC-VER-03 also covers other IDs M6 and M7.

Blocker: Not adjudicable from supplied files. The accessible consolidation map does not expose standalone M6 or M7 semantic categories (per ctl_pinn_resolution.md §M6 and M7). v1.4 records as explicit deferral; revisit when source material is available.

Status transition log:
- 2026-05-16 SEED_SHA DEFERRED -> DEFERRED (seeded by Phase 16 P02)

### M7: Deferred finding M7

Status: DEFERRED

Verdict: defer-with-blocker

Acceptance check: AC-VER-03

Shared acceptance check: AC-VER-03 also covers other IDs M6 and M7.

Blocker: Not adjudicable from supplied files. The accessible consolidation map does not expose standalone M6 or M7 semantic categories (per ctl_pinn_resolution.md §M6 and M7). v1.4 records as explicit deferral; revisit when source material is available.

Status transition log:
- 2026-05-16 SEED_SHA DEFERRED -> DEFERRED (seeded by Phase 16 P02)

### M8: LayerNorm attribution and affine default

Evidence packet: evidence/M8.md

Acceptance check: AC-ARCH-02

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)

### M9: Energy normalization realized support

Evidence packet: evidence/M9.md

Acceptance check: AC-ARCH-05

Shared acceptance check: AC-ARCH-05 also covers other IDs M9 and M10.

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)

### M10: Mass normalization realized support

Evidence packet: evidence/M10.md

Acceptance check: AC-ARCH-05

Shared acceptance check: AC-ARCH-05 also covers other IDs M9 and M10.

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)
