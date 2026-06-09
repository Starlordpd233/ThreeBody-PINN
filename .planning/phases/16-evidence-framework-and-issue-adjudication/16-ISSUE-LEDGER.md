---
phase: 16
slug: evidence-framework-and-issue-adjudication
status: draft
created: 2026-05-16
total_findings: 21
in_scope_findings: 19
deferred_findings: 2
traceability_verified: true
last_verified_traceability: "30/30 v1.4 requirements mapped exactly once - verified 2026-05-16 against REQUIREMENTS.md §Traceability"
---

# Phase 16 Issue Ledger

## Status Table

| ID | Title | Phase | Status | Verdict | Sources Disagree? | Evidence Packet | Acceptance Check | Spec Section | Dependents | Last Updated |
|----|-------|-------|--------|---------|-------------------|-----------------|------------------|--------------|------------|--------------|
| B-01 | SIREN hidden-layer initialization | 20 | VERIFIED | accept-resolution | NO | evidence/B-01.md | AC-ARCH-01 | pinn_architecture.md | B-10 | 2026-06-05 |
| B-02 | Characteristic length and mass scaling | 19 | VERIFIED | accept-resolution | YES - EVID-05 required | evidence/B-02.md | AC-PHYS-01 | ctl_instruction.md; pinn_architecture.md | B-09, M3 | 2026-05-30 |
| B-03 | Input dimensionality | 17 | VERIFIED | accept-resolution | NO | evidence/B-03.md | AC-IO-01 | ctl_instruction.md; pinn_architecture.md | B-04, M1, M2 | 2026-05-19 |
| B-04 | Input vector composition and orientation slots | 17 | VERIFIED | accept-resolution | YES - EVID-05 required | evidence/B-04.md | AC-IO-02 | ctl_instruction.md; pinn_architecture.md | B-03, M1, M2 | 2026-05-19 |
| B-05 | COM frame consistency | 18 | VERIFIED | accept-resolution | NO | evidence/B-05.md | AC-FRAME-01 | ctl_instruction.md; pinn_architecture.md; sampling_method.md | M3, B-11-folded-into-B-05 | 2026-05-21 |
| B-06 | 3D-vs-planar encoding and output contract | 17 | VERIFIED | accept-resolution | NO | evidence/B-06.md | AC-IO-03 | pinn_architecture.md; ctl_instruction.md | - | 2026-05-19 |
| B-07 | Energy/Hamiltonian regularizer | 19 | VERIFIED | accept-resolution | NO | evidence/B-07.md | AC-PHYS-04 | pinn_architecture.md | - | 2026-05-30 |
| B-08 | ALM scheduling and loss balancing | 19 | VERIFIED | accept-resolution | NO | evidence/B-08.md | AC-PHYS-05 | pinn_architecture.md | - | 2026-05-30 |
| B-09 | Softening mismatch | 19 | VERIFIED | accept-resolution | YES - EVID-05 required | evidence/B-09.md | AC-PHYS-03 | ctl_instruction.md; pinn_architecture.md | B-02, PHYS-04, PHYS-05 | 2026-05-30 |
| B-10 | Dynamic omega0 scheduling | 20 | VERIFIED | accept-resolution | NO | evidence/B-10.md | AC-ARCH-01 | pinn_architecture.md | - | 2026-06-05 |
| M1 | 11D IC versus 13D IC gap | 17 | VERIFIED | accept-resolution | NO | evidence/M1.md | AC-IO-02 | ctl_instruction.md; pinn_architecture.md | - | 2026-05-19 |
| M2 | Total dimension claims conflict | 17 | VERIFIED | accept-resolution | NO | evidence/M2.md | AC-IO-01 | ctl_instruction.md; pinn_architecture.md | - | 2026-05-19 |
| M3 | Scaling order and COM transform order | 18 | VERIFIED | accept-resolution | NO | evidence/M3.md | AC-FRAME-01 | ctl_instruction.md | - | 2026-05-21 |
| M4 | Constraint counting error | 19 | VERIFIED | accept-resolution | YES - EVID-05 required | evidence/M4.md | AC-PHYS-06 | ctl_instruction.md | - | 2026-05-30 |
| M5 | I_3 normalization map | 20 | VERIFIED | accept-resolution | YES - EVID-05 required | evidence/M5.md | AC-ARCH-03 | ctl_instruction.md; data-processing-pipeline-full.py *(pre-2026-05-19; now v1.3-era artifact, not spec)* | - | 2026-06-05 |
| M6 | Deferred finding M6 | 21 | DEFERRED | defer-with-blocker | NO | - | AC-VER-03 | - | - | 2026-05-16 |
| M7 | Deferred finding M7 | 21 | DEFERRED | defer-with-blocker | NO | - | AC-VER-03 | - | - | 2026-05-16 |
| M8 | LayerNorm attribution and affine default | 20 | VERIFIED | accept-resolution | NO | evidence/M8.md | AC-ARCH-02 | pinn_architecture.md | ARCH-02 | 2026-06-05 |
| M9 | Energy normalization realized support | 20 | VERIFIED | accept-resolution | NO | evidence/M9.md | AC-ARCH-05 | ctl_instruction.md | - | 2026-06-05 |
| M10 | Mass normalization realized support | 20 | VERIFIED | accept-resolution | NO | evidence/M10.md | AC-ARCH-05 | ctl_instruction.md | - | 2026-06-05 |
| D-02-NORM | Raw-vs-bounded I_norm naming (issue-doc D-02) | 20 | VERIFIED | accept-resolution | NO | evidence/D-02-NORM.md | AC-ARCH-04 | ctl_instruction.md | - | 2026-06-06 |

## Notes

30/30 v1.4 requirements mapped exactly once - see REQUIREMENTS.md §Traceability. This ledger records the verification statement only; REQUIREMENTS.md remains the source of truth.

## Lifecycle Rules

The forward status path is exactly `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED`.

`DEFERRED` is an absorbing state and requires a written blocker. `FIX_APPLIED` is not closure. `VERIFIED` requires a passing acceptance check for the finding's AC-ID.

Audit string: FIX_APPLIED is not closure; VERIFIED requires a passing acceptance check.

A batch is one GSD plan (`NN-NN-PLAN.md`). After every batch of spec or code edits in Phases 17-22, including Phase 20.5, the executing agent re-runs each `VERIFIED` finding's acceptance check if that finding appears as a transitive dependent of any finding edited by the batch. Any regression returns the affected finding to `IN_PROGRESS` and blocks phase exit until re-fixed and re-verified.

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
- 2026-06-05 0c265ee PENDING -> IN_PROGRESS (Phase 20 P01 Task 1 by Phase 20 executor)
- 2026-06-05 2a9614a IN_PROGRESS -> FIX_APPLIED (Phase 20 P01 Task 2 by Phase 20 executor)
- 2026-06-05 51baaee FIX_APPLIED -> VERIFIED (Phase 20 P01 Task 3 by Phase 20 executor)

### B-02: Characteristic length and mass scaling

Evidence packet: evidence/B-02.md

Sources disagree: contested; EVID-05 required; no verdict assigned in Phase 16.

Acceptance check: AC-PHYS-01

Phase 19 reserved acceptance-check names for Phase 21:
- AC-PHYS-01 (B-02): D-formula prose present; mass-fraction alternative documented as future-rewrite-only.
- AC-PHYS-02 (PHYS-02): AD contract in pinn_architecture.md; canonical leaf u named; chain-rule factors; anti-pattern warning.
- AC-PHYS-03 (B-09): Plummer in both files; ε_train=10⁻⁵/ε_inv=10⁻¹⁰ named; s_min unsoftened.
- AC-PHYS-04 (B-07): HNN-style framing removed; L_E reframed as soft conservation regularizer.
- AC-PHYS-05 (B-08): Pseudo-ALM removed; P2-ablation appendix present.
- AC-PHYS-06 (M4): ctl_instruction.md constraint-counting passage replaced.

Phase 21 defines numeric pass criteria and executes disposable probes; Phase 19 reserves
structural criteria only.

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)
- 2026-05-22 ff7a309 PENDING -> IN_PROGRESS (Phase 19 P01 Task 1)
- 2026-05-22 b470f9b IN_PROGRESS -> FIX_APPLIED (Phase 19 P01 Task 3; ctl_instruction spec edits applied)
- 2026-05-30 19-04-T2 FIX_APPLIED -> VERIFIED (Phase 19 P04 Task 2; AC-PHYS-01 structural checks passed)

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
- 2026-05-22 08140c4 PENDING -> IN_PROGRESS (Phase 19 P02 Task 1)
- 2026-05-22 84fe183 IN_PROGRESS -> FIX_APPLIED (Phase 19 P02 Task 3; pinn_architecture spec edits applied)
- 2026-05-30 19-04-T2 FIX_APPLIED -> VERIFIED (Phase 19 P04 Task 2; AC-PHYS-04 structural checks passed)

### B-08: ALM scheduling and loss balancing

Evidence packet: evidence/B-08.md

Acceptance check: AC-PHYS-05

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)
- 2026-05-22 08140c4 PENDING -> IN_PROGRESS (Phase 19 P02 Task 1)
- 2026-05-22 84fe183 IN_PROGRESS -> FIX_APPLIED (Phase 19 P02 Task 3; pinn_architecture spec edits applied)
- 2026-05-30 19-04-T2 FIX_APPLIED -> VERIFIED (Phase 19 P04 Task 2; AC-PHYS-05 structural checks passed)

### B-09: Softening mismatch

Evidence packet: evidence/B-09.md

Sources disagree: contested; EVID-05 required; no verdict assigned in Phase 16.

Acceptance check: AC-PHYS-03

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)
- 2026-05-22 08140c4 PENDING -> IN_PROGRESS (Phase 19 P02 Task 1)
- 2026-05-22 84fe183 IN_PROGRESS -> FIX_APPLIED (Phase 19 P02 Task 3; pinn_architecture spec edits applied)
- 2026-05-30 19-04-T2 FIX_APPLIED -> VERIFIED (Phase 19 P04 Task 2; AC-PHYS-03 structural checks passed)

### B-10: Dynamic omega0 scheduling

Evidence packet: evidence/B-10.md

Acceptance check: AC-ARCH-01

Shared acceptance check: AC-ARCH-01 also covers other IDs B-01 and B-10.

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)
- 2026-06-05 0c265ee PENDING -> IN_PROGRESS (Phase 20 P01 Task 1 by Phase 20 executor)
- 2026-06-05 2a9614a IN_PROGRESS -> FIX_APPLIED (Phase 20 P01 Task 2 by Phase 20 executor)
- 2026-06-05 51baaee FIX_APPLIED -> VERIFIED (Phase 20 P01 Task 3 by Phase 20 executor)

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
- 2026-05-22 ff7a309 PENDING -> IN_PROGRESS (Phase 19 P01 Task 1)
- 2026-05-22 b470f9b IN_PROGRESS -> FIX_APPLIED (Phase 19 P01 Task 3; ctl_instruction spec edits applied)
- 2026-05-30 19-04-T2 FIX_APPLIED -> VERIFIED (Phase 19 P04 Task 2; AC-PHYS-06 structural checks passed)

### M5: I_3 normalization map

Evidence packet: evidence/M5.md

Sources disagree: contested; EVID-05 required; no verdict assigned in Phase 16.

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)
- 2026-06-05 05f9dfc PENDING -> IN_PROGRESS (Phase 20 P03 Task 1; EVID-05 packet filled, verdict accept-resolution recorded)
- 2026-06-05 64f2ffc IN_PROGRESS -> FIX_APPLIED (Phase 20 P03 Task 2; ctl_instruction §3.4 I_3 range/mapping edits applied)
- 2026-06-05 8249172 FIX_APPLIED -> VERIFIED (Phase 20 P03 Task 3; surface + negative audits pass)

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
- 2026-06-05 aaaa1b3 PENDING -> IN_PROGRESS (Phase 20 P02 Task 1 by Phase 20 executor)
- 2026-06-05 47de1d6 IN_PROGRESS -> FIX_APPLIED (Phase 20 P02 Task 2 by Phase 20 executor)
- 2026-06-05 a5f52b4 FIX_APPLIED -> VERIFIED (Phase 20 P02 Task 3 by Phase 20 executor)

### M9: Energy normalization realized support

Evidence packet: evidence/M9.md

Acceptance check: AC-ARCH-05

Shared acceptance check: AC-ARCH-05 also covers other IDs M9 and M10.

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)
- 2026-06-05 69f9e2b PENDING -> IN_PROGRESS (Phase 20 P04 Task 1 by Phase 20 executor)
- 2026-06-05 a685bd0 IN_PROGRESS -> FIX_APPLIED (Phase 20 P04 Task 2 by Phase 20 executor)
- 2026-06-05 8259adf FIX_APPLIED -> VERIFIED (Phase 20 P04 Task 3 by Phase 20 executor)

### M10: Mass normalization realized support

Evidence packet: evidence/M10.md

Acceptance check: AC-ARCH-05

Shared acceptance check: AC-ARCH-05 also covers other IDs M9 and M10.

Status transition log:
- 2026-05-16 SEED_SHA PENDING -> PENDING (seeded by Phase 16 P02)
- 2026-06-05 69f9e2b PENDING -> IN_PROGRESS (Phase 20 P04 Task 1 by Phase 20 executor)
- 2026-06-05 a685bd0 IN_PROGRESS -> FIX_APPLIED (Phase 20 P04 Task 2 by Phase 20 executor)
- 2026-06-05 8259adf FIX_APPLIED -> VERIFIED (Phase 20 P04 Task 3 by Phase 20 executor)

### D-02-NORM: Raw-vs-bounded I_norm naming (issue-doc D-02)

Evidence packet: evidence/D-02-NORM.md

Acceptance check: AC-ARCH-04

Provenance: Added 2026-06-05 by GAP-20-01 resolution (option a, user instruction). Covers issue-doc D-02 / ARCH-04 raw-vs-bounded `I_norm` naming (`I_norm_raw` raw physics/metadata descriptor vs `I_norm_in = tanh(I_norm_raw)` bounded network-facing value). Distinct from M5 / AC-ARCH-03, which adjudicates the `I_3` range/mapping only — do not conflate, and do not treat AC-ARCH-03 as covering `I_norm`. Sources Disagree seeded NO; the Phase 20 executor (plan 20-05) confirmed this during packet review and would escalate to EVID-05 only if a concrete source conflict were found. No `pinn/` live code is a grounding source. Post-review remediation on 2026-06-06 added the missed Step 4 scope descriptor surface and strengthened the ASCII/LaTeX bare `I_norm` audit; D-02-NORM remains VERIFIED.

Status transition log:
- 2026-06-05 0c265ee PENDING -> PENDING (seeded by GAP-20-01 resolution, option a, by user instruction)
- 2026-06-05 f80326a PENDING -> IN_PROGRESS (Phase 20 P05 Task 1 by Phase 20 executor)
- 2026-06-05 774778b IN_PROGRESS -> FIX_APPLIED (Phase 20 P05 Task 2 by Phase 20 executor)
- 2026-06-05 03a6220 FIX_APPLIED -> VERIFIED (Phase 20 P05 Task 3 by Phase 20 executor)
- 2026-06-06 remediation-audit VERIFIED -> VERIFIED (post-review remediation: fixed missed Step 4 scope descriptor surface and strengthened bare I_norm audit)

## Phase 21 Acceptance Evidence Addendum

Added 2026-06-08 during Phase 21 recovery after the prior execution claim was found structurally incomplete. This addendum does not change existing terminal statuses; it records the VER-04 numerical acceptance evidence that supports Phase 21 closure.

| Probe | Related contracts/findings | Evidence | Result |
|---|---|---|---|
| 10.1 Scaling Consistency | B-02 / AC-PHYS-01; M3 scaling order context | `.planning/phases/21-acceptance-checks-and-handoff/evidence/probe_scaling.stdout.txt` | PASS: `max_relative_error = 2.22e-16` |
| 10.2 COM Invariance | B-05 / AC-FRAME-01 sibling numeric check; output projection contract | `.planning/phases/21-acceptance-checks-and-handoff/evidence/probe_com.stdout.txt` | PASS: `COM magnitude: 7.90e-17` |
| 10.3 Componentwise AD | PHYS-02 derivative contract; B-07/B-09 downstream force/loss dependence | `.planning/phases/21-acceptance-checks-and-handoff/evidence/probe_ad.stdout.txt` | PASS: `relative_error: 0.00e+00` |
| 10.4 Force-Energy Consistency | B-07 / AC-PHYS-04; B-09 / AC-PHYS-03 | `.planning/phases/21-acceptance-checks-and-handoff/evidence/probe_force_energy.stdout.txt` | PASS: `relative_error: 1.62e-16`, finite `H_epsilon` |
| 10.5 Loss Stability Dry Run | B-01/B-10/M8 architecture contracts; B-07/B-08/B-09 loss contracts | `.planning/phases/21-acceptance-checks-and-handoff/evidence/probe_loss_stability.stdout.txt` | PASS: finite total/data/IC/physics/energy/angular losses |

Environment evidence: `.planning/phases/21-acceptance-checks-and-handoff/evidence/python_environment.stdout.txt` records `.venv/bin/python`, Python 3.12.13, NumPy 2.2.0, and Torch 2.12.0.

## Phase 21 SI-Ledger Reconciliation Addendum

Recorded 2026-06-08 for VER-06:

- `SI-CTL-001` is retired in `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` with "Resolved by v1.4 finding B-03. See Phase 17 input contract."
- `SI-SSR-001` is retired in `pinn_instruction/markdown_conversion/framework-revisions/stage-strat-revision/stage_strat_revision.md` with "Resolved by v1.4 finding M5. See Phase 20 architecture and normalization cleanup."
- `SI-PINN-001` is not present in the current framework-spec SI metadata sections and was not present there at `v1.4-pre-phase-21`; it appears only in planning references. No synthetic retired entry was created.
- `SI-PINN-002`, `SI-PINN-003`, `SI-DQA-002`, and `SI-DQA-003` are preserved untouched because they are unrelated to Issue 01 retirement candidates.

## Phase 22 Acceptance & VER-05 Reconciliation Addendum

Recorded 2026-06-09 by plan 22-05 (Wave 3 — phase gate). Phase 22 is the
framework-spec-cleanup phase; its findings are render-defect findings (Pandoc/multiline
tables, raw/backtick ASCII-math, fenced-div/caption/attribute survivors) in the three
framework specs, not Issue-01 content findings. The existing Phase 16 lifecycle columns
(`PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED`, with `DEFERRED` for written blockers)
are reused.

**Baseline ref:** git tag `v1.4-pre-phase-22` (commit `faa73d0`).
**Detector:** `tools/spec-render-check/detect.mjs` (commit faa73d0 baseline + 22-02/22-03
adjudication layer). Adjudication allowlists: `tools/spec-render-check/adjudications/22-02-pinn-architecture.json`
(7 entries) and `tools/spec-render-check/adjudications/22-03-ctl-instruction.json` (10 entries).

### Phase 22 render findings

| ID | Title | Spec | Status | Verdict | Evidence | Acceptor plan | Last Updated |
|----|-------|------|--------|---------|----------|---------------|--------------|
| P22-R1 | Pandoc multiline tables (pinn hyperparameter + architecture blueprint) | pinn_architecture.md | VERIFIED | accept-resolution | 22-02-SUMMARY.md §Task 1; 22-02-DETECTOR-BASELINE.txt | 22-02 | 2026-06-09 |
| P22-R2 | Raw / backtick ASCII-math in prose and tables (both specs) | pinn_architecture.md, ctl_instruction.md | VERIFIED | accept-resolution | 22-02-SUMMARY.md §Task 2; 22-03-SUMMARY.md §Task 2; 22-02-DETECTOR-BASELINE.txt; 22-03-DETECTOR-BASELINE.txt | 22-02, 22-03 | 2026-06-09 |
| P22-R3 | Pandoc fenced-div, caption, section-attribute survivors | pinn_architecture.md, ctl_instruction.md | VERIFIED | accept-resolution | 22-02-SUMMARY.md §Task 1 (table divs); 22-03-SUMMARY.md §Task 2 (Pandoc attribute); adjudication allowlists | 22-02, 22-03 | 2026-06-09 |

### Phase 22 status transition log

| Date | Plan | Finding | Transition | Notes |
|------|------|---------|------------|-------|
| 2026-06-09 | 22-01 | P22-R1, P22-R2, P22-R3 | PENDING (seeded) | Detector + census + footnote probe completed; defect inventory captured from design §4. |
| 2026-06-09 | 22-02 | P22-R1, P22-R2, P22-R3 (pinn half) | PENDING → IN_PROGRESS → FIX_APPLIED | Pandoc multiline tables → GFM; math normalization; footnote form `[^n]` → `[n]` (Stage-0 probe confirmed `unsupported`). |
| 2026-06-09 | 22-02 | P22-R1, P22-R2 (pinn half) | FIX_APPLIED → VERIFIED | Post-adjudication detector: 0 DEFINITE + 0 REVIEW, 7 ADJUDICATED (GAP-22-03 RESOLVED-WITH-INSTRUCTION). |
| 2026-06-09 | 22-03 | P22-R2, P22-R3 (ctl half) | PENDING → IN_PROGRESS → FIX_APPLIED | Mid-list `$$\begin{aligned}` moved to own lines; raw ASCII-math → LaTeX `$…$`; Pandoc attribute removed. |
| 2026-06-09 | 22-03 | P22-R2, P22-R3 (ctl half) | FIX_APPLIED → VERIFIED | Post-adjudication detector: 0 DEFINITE + 0 REVIEW, 10 ADJUDICATED. |
| 2026-06-09 | 22-04 | (author-comment preservation) | — | PRE/POST census + diff + FUT-05 handoff. 26 PRE = 26 POST; 0 lost, 0 semantically changed; 3 D-05 wrapper repairs documented in 22-COMMENT-DIFF.md. |
| 2026-06-09 | 22-05 | (phase gate) | — | Full detector suite re-run: exit 0 per file. 0 DEFINITE + 0 REVIEW across all 3 specs. `sampling_method.md` negative control unchanged (0 findings + 1 SUPPRESSED). |

### Phase 22 re-verification of previously-VERIFIED Phase 16/20/21 findings

The Phase 22 edits touched `pinn_architecture.md` and `ctl_instruction.md`, which are the
primary Spec Section for many earlier findings. Per the ledger's Lifecycle Rules
("After every batch of spec edits in Phases 17-22, the executing agent re-runs each VERIFIED
finding's acceptance check if that finding appears as a transitive dependent of any finding
edited by the batch"), plan 22-05 re-ran the full detector suite after WS-A completed. The
Phase 22 edits are **presentation-only** (math delimiter/brace normalization, Pandoc table →
GFM preserving cell content, whitespace for block rendering, footnote form conversion, D-05
wrapper repairs). No mathematical content was changed (G3 content-preservation audit). The
re-run shows 0 DEFINITE + 0 REVIEW per file, so no Phase 16/20/21 finding's acceptance check
regresses. Specifically:

- **B-02 (AC-PHYS-01):** Governing Mathematical Convention block in `ctl_instruction.md` was
  ASCII-math → LaTeX-normalized (P22-R2). The D-form prose and mass-fraction alternative
  documentation remain present; the conversion is equivalence-verified per 22-03 Task 2.
  No regression.
- **B-09 (AC-PHYS-03):** Plummer softening forms in both files were math-normalized
  (P22-R2). `ε_train=10⁻⁵` and `ε_inv=10⁻¹⁰` naming is preserved in the LaTeX-normalized
  forms. No regression.
- **B-01 / B-10 / M8 (AC-ARCH-01/02):** SIREN `ω_0` forms and LayerNorm references in
  `pinn_architecture.md` were math-normalized (P22-R2). `first_omega_0` / `hidden_omega_0` /
  `elementwise_affine` PyTorch identifiers were correctly preserved as code (GAP-22-03
  adjudication). No regression.
- **M5 / M9 / M10 / D-02-NORM (AC-ARCH-03/04/05):** `ctl_instruction.md` normalization did
  not touch the I_3 normalization, energy normalization, or mass normalization passages.
  No regression.
- **B-03 / B-04 / B-05 / B-06 / M1 / M2 / M3 / M4 / B-07 / B-08:** These findings' content
  was not edited by Phase 22. No regression.

All Phase 16/20/21 VERIFIED findings remain VERIFIED. No finding reverted to IN_PROGRESS.

### Phase 22 gaps

| Gap ID | Classification | Status | Resolution note |
|--------|----------------|--------|-----------------|
| GAP-22-01 | semantic (author-comment adjudication scope) | RESOLVED-WITH-INSTRUCTION | User instruction: Phase 22 preserves; FUT-05 adjudicates. Recorded in 22-GAPS.md; implemented by 22-04. |
| GAP-22-02 | semantic (28 vs. 26 author-comment census) | RESOLVED-WITH-INSTRUCTION | User instruction: use live corpus count (26). Recorded in 22-GAPS.md; 22-01 captured the 26-comment PRE census. |
| GAP-22-03 | semantic (detector oracle conflicts with D-02/D-07 code-identifier exclusion) | RESOLVED-WITH-INSTRUCTION | User instruction (Option A): accept REVIEW findings on code identifiers as false positives; G2 redefined as 0 DEFINITE + every REVIEW adjudicated or absent. Adjudication allowlists committed. |

No OPEN STOP gaps remain. No finding blocks closure.

### Phase 22 deferred findings (design §12 — OUT of scope)

The following are recorded content inconsistencies that the design doc explicitly defers
to their owning tracks / FUT-01. They are **not Phase 22 render findings** and are not
entered in the Phase 22 findings table; they are recorded here for traceability only:

- **SI-PINN-002** (batch-construction inconsistency between `pinn_architecture.md` and
  `ctl_instruction.md`) — content issue; deferred to owning track (not Phase 22 scope).
- **IC-dimension reconciliation note** — content issue; deferred to FUT-01.
- **Outdated code-folder references in `ctl_instruction.md`** — content issue; deferred to
  owning track.

### Phase 22 acceptance verdict

**PASS.** All automated gates and the G4 visual backstop are complete.

- G1 (selftest): exit 0, regression reproduced, negative controls clean.
- G2 (all 3 specs 0-residual): exit 0 per file with `--adjudications` where applicable;
  `sampling_method.md` negative control unchanged (0 findings + 1 SUPPRESSED).
- G3 (content preservation): every changed hunk classified into allowed categories with
  per-hunk evidence; 0 comments lost, 0 semantically changed.
- G4 (automated proxy): PASS. Visual backstop: PENDING-USER-REVIEW
  (see `22-RENDER-REVIEW.md` for the user-facing checklist).
- VER-05 (ledger): PASS. All Phase-22 findings VERIFIED; 0 OPEN STOP gaps; no
  user-deferred Phase-22 findings (the 3 deferred items are design-§12 content issues,
  explicitly OUT of Phase 22 scope).
- G4 (visual backstop): PASS. User approved the checklist in `22-RENDER-REVIEW.md`
  on 2026-06-09.
