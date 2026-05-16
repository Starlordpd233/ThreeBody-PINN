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
| B-02 | Characteristic length and mass scaling | 19 | PENDING | - | YES - EVID-05 required | evidence/B-02.md | AC-PHYS-01 | ctl_instruction.md; pinn_architecture.md | B-09, M3 | 2026-05-16 |
| B-03 | Input dimensionality | 17 | PENDING | - | NO | evidence/B-03.md | AC-IO-01 | ctl_instruction.md; pinn_architecture.md | B-04, M1, M2 | 2026-05-16 |
| B-04 | Input vector composition and orientation slots | 17 | PENDING | - | YES - EVID-05 required | evidence/B-04.md | AC-IO-02 | ctl_instruction.md; pinn_architecture.md | B-03, M1, M2 | 2026-05-16 |
| B-05 | COM frame consistency | 18 | PENDING | - | NO | evidence/B-05.md | AC-FRAME-01 | ctl_instruction.md; pinn_architecture.md; sampling_method.md | M3, B-11-folded-into-B-05 | 2026-05-16 |
| B-06 | 3D-vs-planar encoding and output contract | 17 | PENDING | - | NO | evidence/B-06.md | AC-IO-03 | pinn_architecture.md | - | 2026-05-16 |
| B-07 | Energy/Hamiltonian regularizer | 19 | PENDING | - | NO | evidence/B-07.md | AC-PHYS-04 | pinn_architecture.md | - | 2026-05-16 |
| B-08 | ALM scheduling and loss balancing | 19 | PENDING | - | NO | evidence/B-08.md | AC-PHYS-05 | pinn_architecture.md | - | 2026-05-16 |
| B-09 | Softening mismatch | 19 | PENDING | - | YES - EVID-05 required | evidence/B-09.md | AC-PHYS-03 | ctl_instruction.md; pinn_architecture.md | B-02, PHYS-04, PHYS-05 | 2026-05-16 |
| B-10 | Dynamic omega0 scheduling | 20 | PENDING | - | NO | evidence/B-10.md | AC-ARCH-01 | pinn_architecture.md | - | 2026-05-16 |
| M1 | 11D IC versus 13D IC gap | 17 | PENDING | - | NO | evidence/M1.md | AC-IO-02 | ctl_instruction.md; pinn_architecture.md | - | 2026-05-16 |
| M2 | Total dimension claims conflict | 17 | PENDING | - | NO | evidence/M2.md | AC-IO-01 | ctl_instruction.md; pinn_architecture.md | - | 2026-05-16 |
| M3 | Scaling order and COM transform order | 18 | PENDING | - | NO | evidence/M3.md | AC-FRAME-01 | ctl_instruction.md | - | 2026-05-16 |
| M4 | Constraint counting error | 19 | PENDING | - | NO | evidence/M4.md | AC-PHYS-06 | ctl_instruction.md | - | 2026-05-16 |
| M5 | I_3 normalization map | 20 | PENDING | - | YES - EVID-05 required | evidence/M5.md | AC-ARCH-03 | ctl_instruction.md; data-processing-pipeline-full.py | - | 2026-05-16 |
| M6 | Deferred finding M6 | 21 | DEFERRED | defer-with-blocker | NO | - | AC-VER-03 | - | - | 2026-05-16 |
| M7 | Deferred finding M7 | 21 | DEFERRED | defer-with-blocker | NO | - | AC-VER-03 | - | - | 2026-05-16 |
| M8 | LayerNorm attribution and affine default | 20 | PENDING | - | NO | evidence/M8.md | AC-ARCH-02 | pinn_architecture.md | ARCH-02 | 2026-05-16 |
| M9 | Energy normalization realized support | 20 | PENDING | - | NO | evidence/M9.md | AC-ARCH-05 | ctl_instruction.md | - | 2026-05-16 |
| M10 | Mass normalization realized support | 20 | PENDING | - | NO | evidence/M10.md | AC-ARCH-05 | ctl_instruction.md | - | 2026-05-16 |
