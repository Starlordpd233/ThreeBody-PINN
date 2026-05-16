# Roadmap: 3-Body Problem Physics-Inspired LLM

## Milestones

- ✅ **v1.0 Codebase Cleanup** — Phases 1–4 (shipped 2026-03-20)
- ✅ **v1.1 LaTeX Modularization Verification** — Phases 5–8 (shipped 2026-03-22)
- ✅ **v1.2 PINN Implementation Readiness** — Phase 9 (shipped 2026-05-08)
- ✅ **v1.3 Markdown Conversion Verification & Correction** — Phases 10–15, 15.1 (shipped 2026-05-08)
- 🚧 **v1.4 Resolving 01 Architecture and Physics Foundations** — Phases 16–21 (planned)

## Phases

<details>
<summary>✅ v1.0 Codebase Cleanup (Phases 1–4) — SHIPPED 2026-03-20</summary>

- [x] Phase 1: Code Rewrites and Validation (3/3 plans) — completed 2026-03-18
- [x] Phase 2: Documentation Updates (3/3 plans) — completed 2026-03-19
- [x] Phase 3: Data Deletion and Legacy Cleanup (2/2 plans) — completed 2026-03-19
- [x] Phase 4: Stale Reference Fixes (2/2 plans) — completed 2026-03-20

Full details: `.planning/milestones/v1.0-ROADMAP.md`

</details>

<details>
<summary>✅ v1.1 LaTeX Modularization Verification (Phases 5–8) — SHIPPED 2026-03-22</summary>

- [x] **Phase 5: Content Completeness Verification** — Automated diff confirms no content lost across all 5 structures (completed 2026-03-21)
- [x] **Phase 6: Preamble Parity Verification** — Package, macro, and command declarations match between original and modular preambles (completed 2026-03-21)
- [x] **Phase 7: Structure Fidelity Verification** — Section hierarchy, labels, references, citations, and floats preserved (completed 2026-03-21)
- [x] **Phase 8: Compilability Verification** — All 5 modular structures compile cleanly with 0 errors and 0 new warnings (completed 2026-03-22)

</details>

<details>
<summary>✅ v1.2 PINN Implementation Readiness (Phase 9) — SHIPPED 2026-05-08</summary>

### Phase 9: Issues Directory Consolidation

**Goal:** Reorganize 7 scattered issue reports into 2–3 thematic documents eliminating duplication
**Depends on**: None
**Requirements**: CONSOL-01, CONSOL-02, CONSOL-03
**Success Criteria:**
  1. All 7 existing files merged into 2–3 new thematic files
  2. No unique findings lost in consolidation
  3. Each thematic document has distinct purpose with no overlapping coverage
  4. Original files archived or deleted with migration note

**Plans**: 3 plans
- [x] 09-01-PLAN.md
- [x] 09-02-PLAN.md
- [x] 09-03-PLAN.md

**Deliverables:**
- 3 thematic issue documents in `pinn_instruction/issues/`
- MIGRATION.md and README.md for migration tracking
- VERIFICATION-REPORT.md (PASS), VALIDATION.md (all checks PASS)

</details>

<details>
<summary>✅ v1.3 Markdown Conversion Verification & Correction (Phases 10–15, 15.1) — SHIPPED 2026-05-08</summary>

**Milestone Goal:** Verify every markdown conversion against its LaTeX source section-by-section, fix all errors to achieve one-to-one injection fidelity, and produce one authoritative `.md` file per source document.

- [x] **Phase 10: CTL-Instruction Verification** — 8 sections + appendix, 3 markdown candidates, heavy math — completed 2026-05-02
- [x] **Phase 11: Data-Quality-Assessment Verification** — 7 sections, 2 markdown candidates, cross-reference heavy — completed 2026-05-05
- [x] **Phase 12: PINN-Architecture Verification** — 7 active + 3 inactive sections, 3 markdown candidates, comment exclusion — completed 2026-05-05
- [x] **Phase 13: Review-of-Framework Verification** — 7 sections, 1 pandoc candidate, sub-document structure — completed 2026-05-05
- [x] **Phase 14: Stage-Strategy-Revision Verification** — 6 sections, 1 pandoc candidate, table normalization — completed 2026-05-05
- [x] **Phase 15: Sampling-Method Verification** — Monolithic source, 2 markdown candidates — completed 2026-05-06
- [x] **Phase 15.1: Markdown Conversion Correction** (INSERTED) — Resolve critical conversion errors and structural issues from v1.3 review reports (phases 10-15) to produce authoritative markdown files for handoff. New issues discovered after this scope are handled via GSD workflow, not this phase. — completed 2026-05-08

Full details: `.planning/milestones/v1.3-ROADMAP.md`

</details>

### 🚧 v1.4 Resolving 01 Architecture and Physics Foundations (Planned)

**Milestone Goal:** Validate `ctl_pinn_resolution.md` issue-by-issue against the current framework specs and thematic issue report, then make evidence-backed framework-spec edits without changing the SQR-SkipResNet-SIREN, CTL, or raw-mass decisions unless evidence requires it.

**Granularity:** standard
**Coverage:** 25/25 v1.4 requirements mapped

- [ ] **Phase 16: Evidence Framework and Issue Adjudication** — Establish the evidence packet, verdict, false-positive, and traceability structure that every Issue 01 edit must follow.
- [ ] **Phase 17: Input and Output Contracts** — Resolve the 14D input, 13-entry IC schema, position-output, and obsolete-dimension wording contracts across framework specs.
- [ ] **Phase 18: Frame and Gauge Contracts** — Reconcile COM, momentum, ordering, rotation gauge, scaling order, hierarchical offsets, and 3D Cartesian output guarantees.
- [ ] **Phase 19: Physics and Loss Contracts** — Lock raw-mass scaling, normalized-time derivatives, matched softening, energy-regularizer wording, and loss-balancing semantics.
- [ ] **Phase 20: Architecture and Normalization Cleanup** — Clean up SIREN frequency/init, LayerNorm attribution/defaults, inertia normalization, and realized dataset-support wording.
- [ ] **Phase 21: Acceptance Checks and Handoff** — Add verification checks and produce the final fixed/non-change/deferred handoff for downstream implementation planning.

## Phase Details

### Phase 16: Evidence Framework and Issue Adjudication
**Goal**: Reviewers can trace every Issue 01 decision to direct evidence before any framework-spec edit is accepted.
**Depends on**: Phase 15.1
**Requirements**: EVID-01, EVID-02, EVID-03, EVID-04, VER-02
**Success Criteria** (what must be TRUE):
  1. Reviewer can inspect issue-by-issue evidence packets with citations to `ctl_pinn_resolution.md`, `master_consolidation_report.md`, `01-architecture-and-physics-foundations.md`, and current framework specs.
  2. Reviewer can see an explicit accept, reject, or defer verdict for every selected Issue 01 finding.
  3. Reviewer can identify false positives and intentional non-changes with the evidence-backed reason each current convention remains valid.
  4. Reviewer can trace every accepted issue to a before/after spec-section note and the contract that section now enforces.
  5. Roadmap and requirements traceability show all 25 v1.4 requirements mapped exactly once, beginning at Phase 16.
**Plans**: TBD

### Phase 17: Input and Output Contracts
**Goal**: Framework specs expose one coherent network input and output contract for downstream implementation.
**Depends on**: Phase 16
**Requirements**: IO-01, IO-02, IO-03, IO-04
**Success Criteria** (what must be TRUE):
  1. Reader can find one canonical network input contract: `14D = [tau, IC_13]`.
  2. Reader can inspect one ordered 13-entry IC vector with normalization rules for masses, energy, angular momentum, virial ratio, minimum separation, inertia, shape invariants, and velocity-orientation scalars.
  3. Reader can distinguish 9D position predictions from velocities and accelerations derived by automatic differentiation.
  4. Reader no longer encounters unqualified 11D, 12D, or ambiguous 13D/14D wording except where it is explicitly labeled as historical source-issue metadata.
**Plans**: TBD

### Phase 18: Frame and Gauge Contracts
**Goal**: Framework specs define one frame, gauge, and output-space convention for ICs, Brutus snapshots, and model predictions.
**Depends on**: Phase 17
**Requirements**: FRAME-01, FRAME-02, FRAME-03, FRAME-04
**Success Criteria** (what must be TRUE):
  1. Reader can follow one preprocessing order: COM recentering, zero-momentum boost, canonical ordering, canonical rotation gauge, then scaling.
  2. Reader can find explicit COM and total-momentum assertions for preprocessed samples and model outputs.
  3. Reader can see how hierarchical post-perturbation COM offsets and standard quasi-random COM behavior are reconciled with the sampling spec.
  4. Reader can verify the output contract remains 3D Cartesian trajectories and is not replaced by planar or invariant-only predictions.
**Plans**: TBD

### Phase 19: Physics and Loss Contracts
**Goal**: Framework specs state physically consistent scaling, derivative, softening, energy, and loss-balancing contracts.
**Depends on**: Phase 18
**Requirements**: PHYS-01, PHYS-02, PHYS-03, PHYS-04, PHYS-05
**Success Criteria** (what must be TRUE):
  1. Reader can identify the raw-mass nondimensionalization convention and retained `D=(G*T^2)^(1/3)` scale, with the mass-fraction alternative documented as a future rewrite only.
  2. Reader can trace the normalized-time derivative contract, including whether training differentiates with respect to `u=t/T` or applies `tau` chain-rule factors.
  3. Reader can verify the physics residual and energy regularizer use a matched softened force/potential pair while offline invariant epsilon remains separate.
  4. Reader sees the energy term described as a soft conservation regularizer, not an HNN.
  5. Reader can confirm ALM is limited to scalar conservation constraints and dense ODE residuals use a causal or otherwise justified weighting contract.
**Plans**: TBD

### Phase 20: Architecture and Normalization Cleanup
**Goal**: Framework specs remove architecture and normalization ambiguity without changing the preserved backbone unnecessarily.
**Depends on**: Phase 19
**Requirements**: ARCH-01, ARCH-02, ARCH-03, ARCH-04, ARCH-05
**Success Criteria** (what must be TRUE):
  1. Reader can find consistent SIREN initialization and frequency settings, with no epochwise `omega0` scheduler unless a reparameterized runtime mechanism is specified.
  2. Reader can see LayerNorm documented as a project-specific stabilizer with one consistent affine/non-affine default.
  3. Reader can verify `I_3` maps the documented triangle-shape range to `[-1, 1]`.
  4. Reader can distinguish the raw inertia descriptor from the tanh-squashed network input value.
  5. Reader can see energy and mass normalization support ranges documented as realized dataset support rather than correctness failures.
**Plans**: TBD

### Phase 21: Acceptance Checks and Handoff
**Goal**: Downstream planning has acceptance checks and a clear fixed/non-change/deferred issue ledger.
**Depends on**: Phase 20
**Requirements**: VER-01, VER-03
**Success Criteria** (what must be TRUE):
  1. Reader can inspect acceptance checks for scaling consistency, COM invariance, derivative correctness, force-energy consistency, and loss stability.
  2. Reader can identify which Issue 01 findings were fixed, intentionally left unchanged, or deferred for future empirical validation.
  3. `$gsd-plan-phase` can derive implementation plans from evidence packets, changed spec sections, and verification checks without redoing the conceptual audit.
**Plans**: TBD

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Code Rewrites and Validation | v1.0 | 3/3 | Complete | 2026-03-18 |
| 2. Documentation Updates | v1.0 | 3/3 | Complete | 2026-03-19 |
| 3. Data Deletion and Legacy Cleanup | v1.0 | 2/2 | Complete | 2026-03-19 |
| 4. Stale Reference Fixes | v1.0 | 2/2 | Complete | 2026-03-20 |
| 5. Content Completeness Verification | v1.1 | 1/1 | Complete | 2026-03-21 |
| 6. Preamble Parity Verification | v1.1 | 1/1 | Complete | 2026-03-21 |
| 7. Structure Fidelity Verification | v1.1 | 2/2 | Complete | 2026-03-21 |
| 8. Compilability Verification | v1.1 | 1/1 | Complete | 2026-03-22 |
| 9. Issues Directory Consolidation | v1.2 | 3/3 | Complete | 2026-05-08 |
| 10. CTL-Instruction Verification | v1.3 | 3/3 | Complete | 2026-05-02 |
| 11. Data-Quality-Assessment Verification | v1.3 | 3/3 | Complete | 2026-05-05 |
| 12. PINN-Architecture Verification | v1.3 | 3/3 | Complete | 2026-05-05 |
| 13. Review-of-Framework Verification | v1.3 | 3/3 | Complete | 2026-05-05 |
| 14. Stage-Strategy-Revision Verification | v1.3 | 3/3 | Complete | 2026-05-05 |
| 15. Sampling-Method Verification | v1.3 | 3/3 | Complete | 2026-05-06 |
| 15.1 Markdown Conversion Correction | v1.3 | 3/3 | Complete | 2026-05-08 |
| 16. Evidence Framework and Issue Adjudication | v1.4 | 0/TBD | Not started | - |
| 17. Input and Output Contracts | v1.4 | 0/TBD | Not started | - |
| 18. Frame and Gauge Contracts | v1.4 | 0/TBD | Not started | - |
| 19. Physics and Loss Contracts | v1.4 | 0/TBD | Not started | - |
| 20. Architecture and Normalization Cleanup | v1.4 | 0/TBD | Not started | - |
| 21. Acceptance Checks and Handoff | v1.4 | 0/TBD | Not started | - |

---
*Last updated: 2026-05-15 — v1.4 roadmap created*
