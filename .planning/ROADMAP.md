# Roadmap: 3-Body Problem Physics-Inspired LLM

## Milestones

- ✅ **v1.0 Codebase Cleanup** — Phases 1–4 (shipped 2026-03-20)
- ✅ **v1.1 LaTeX Modularization Verification** — Phases 5–8 (shipped 2026-03-22)
- ✅ **v1.2 PINN Implementation Readiness** — Phase 9 (shipped 2026-05-08)
- ✅ **v1.3 Markdown Conversion Verification & Correction** — Phases 10–15, 15.1 (shipped 2026-05-08; SCS gate correction verified 2026-05-15)
- 🚧 **v1.4 Resolving 01 Architecture and Physics Foundations** — Phases 16–21, with Phase 20.5 inserted before Phase 21 (Phases 16–18 complete; next: discuss Phase 19)

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
- [x] **Post-ship SCS Gate Correction** — Corrected data-quality-assessment raw drift/SCS semantics in LaTeX, regenerated PDF, aligned markdown, and closure audit row — verified 2026-05-15

Full details: `.planning/milestones/v1.3-ROADMAP.md`

</details>

### 🚧 v1.4 Resolving 01 Architecture and Physics Foundations (Initialized)

**Milestone Goal:** Critically examine each Issue 01 finding against BOTH `ctl_pinn_resolution.md` AND `01-architecture-and-physics-foundations.md` — treating neither as authoritative — to identify the root-cause ambiguity in the current framework specs, lock the right convention, apply evidence-backed framework-spec edits, and **verify each fix by executing disposable acceptance checks** before closing the issue. Preserve the SQR-SkipResNet-SIREN, CTL, and raw-mass decisions unless evidence requires otherwise. v1.4 settles documentation and validation evidence; it does not implement or update production PINN/training code.

**Granularity:** standard
**Coverage:** 30/30 v1.4 requirements mapped

#### Verification Protocol (applies to every phase)

Every issue and every edit in v1.4 follows this loop:

1. **Adjudicate** — for findings where the resolution doc and the issue doc disagree (currently B-02 D formula, B-04 input-vector orientation slots, B-09 softening strategy, M5 `I_3` mapping, plus any further conflicts discovered during the walkthrough), apply EVID-05: read both positions in full, verify each against the current framework specs and first-principles physics, and record the root-cause ambiguity in the issue evidence packet before editing. Per the 2026-05-19 directive, live PINN-side code is not v1.4 evidence or grounding.
2. **Fix** — apply the framework-spec edit. Existing `pinn/` implementation files are v1.3-era artifacts; code alignment belongs after this milestone and may be referenced only in forward-pointing FUT-01 hand-off documents.
3. **Verify** — run the acceptance check defined for that finding using disposable validation probes where execution is needed (per VER-01; full §10 suite executed in Phase 21 per VER-04; smaller phase-local checks may run earlier).
4. **Re-verify after every batch** — re-run the acceptance check on every previously `VERIFIED` finding the new batch could have regressed (same spec section, dependent contract, or shared formula). Any regression reverts that finding to `IN_PROGRESS`.
5. **Ledger discipline** — each finding's status (`PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED` or `DEFERRED`) lives in `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md`. No phase exits until every in-scope finding is `VERIFIED` or `DEFERRED` with a written blocker. "I applied the patch" is **not** a closure event; "the acceptance check passed" is.

**EDL research support:** If a source-silent decision is empirically consequential and cannot be settled from sources or short first-principles reasoning, record it in the phase-local gap register first. When useful, attach a central EDL research brief under `.planning/research/edl/` so the user can research the decision externally. EDL artifacts are non-canonical support unless promoted; the phase gap register owns blocking, deferral, and resolution.

This loop expects iteration. It is normal for a contested finding to cycle through `FIX_APPLIED → IN_PROGRESS → FIX_APPLIED` multiple times before reaching `VERIFIED` — especially when an initial fix treats the surface symptom rather than the root cause.

- [x] **Phase 16: Evidence Framework and Issue Adjudication** — Establish the issue ledger schema, evidence-packet template, EVID-05 conflict-adjudication protocol, and VER-05 re-verification cycle that every Issue 01 edit must follow. (completed 2026-05-16)
- [x] **Phase 17: Input and Output Contracts** — Resolve the 14D input, 13-entry IC schema, position-output (with mass-weighted COM projection head), and obsolete-dimension wording contracts across framework specs. (completed 2026-05-20)
- [x] **Phase 18: Frame and Gauge Contracts** — Reconcile COM, momentum, ordering, rotation gauge, scaling order, hierarchical offsets, and 3D Cartesian output guarantees. (completed 2026-05-21)
- [ ] **Phase 19: Physics and Loss Contracts** — Lock raw-mass scaling, componentwise normalized-time derivatives, matched softening (after dual-eps vs single-eps adjudication), energy-regularizer wording, loss-balancing semantics, and the M4 constraint-counting replacement.
- [ ] **Phase 20: Architecture and Normalization Cleanup** — Clean up SIREN frequency/init, LayerNorm attribution/defaults, inertia normalization, and realized dataset-support wording.
- [ ] **Phase 21: Acceptance Checks, Validation Execution, and Handoff** — Define the §10 acceptance checks (VER-01), **execute** them with disposable validation probes that test the v1.4 framework specs (VER-04), reconcile the `SI-*` ledger (VER-06), and produce the final fixed/non-change/deferred handoff (VER-03). Failing checks loop back to Phases 17–20 for spec correction.

## Phase Details

### Phase 16: Evidence Framework and Issue Adjudication

**Goal**: Reviewers can trace every Issue 01 decision to direct evidence — examined critically against both source documents, current framework specs, and first-principles physics — before any framework-spec edit is accepted, and every fix that follows has a defined re-verification pass.
**Depends on**: Phase 15.1 + post-ship SCS gate correction (both complete)
**Requirements**: EVID-01, EVID-02, EVID-03, EVID-04, EVID-05, VER-02, VER-05 (defined here; applied throughout Phases 17–21)
**Completion**: Phase 16 completed 2026-05-16; Phase 17 completed 2026-05-20. Next milestone workflow step is `$gsd-discuss-phase 18`.
**Success Criteria** (what must be TRUE):

  1. Reviewer can inspect issue-by-issue evidence packets with line-range citations to `ctl_pinn_resolution.md`, `01-architecture-and-physics-foundations.md`, and current framework specs. Live `pinn/` references, when present, are FUT-01 hand-off context only.
  2. Reviewer can see a verdict from the fixed set — `accept-resolution`, `accept-issue-doc`, `accept-third-position`, `reject-both-as-unsupported`, or `defer-with-blocker` — for every selected Issue 01 finding.
  3. Reviewer can identify false positives in either source document with the evidence-backed reason each current convention remains valid and which source(s) misread it.
  4. Reviewer can trace every accepted issue to a before/after spec-section note, the contract that section now enforces, and the named verification step that will confirm the fix.
  5. Reviewer can find an EVID-05 conflict-adjudication record for each contested finding (B-02 D formula, B-04 input-vector orientation slots, B-09 softening strategy, M5 `I_3` mapping, plus any further conflict discovered during the walkthrough) that identifies the root-cause ambiguity in the framework specs and the explicit convention now locked.
  6. Reviewer can find `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` containing every in-scope finding with a status (`PENDING`/`IN_PROGRESS`/`FIX_APPLIED`/`VERIFIED`/`DEFERRED`), the acceptance check that will close it, and an explicit rule that "fix applied" is not closure.
  7. Roadmap and requirements traceability show all 30 v1.4 requirements mapped exactly once, beginning at Phase 16.

**Plans**: 3 plans
Plans:
**Wave 1**

- [x] 16-01-PLAN.md — Evidence protocol and packet template
- [x] 16-02-PLAN.md — Issue ledger and lifecycle controls

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 16-03-PLAN.md — Ledger path reconciliation and traceability audit

### Phase 17: Input and Output Contracts

**Goal**: Framework specs expose one coherent network input and output contract for downstream implementation.
**Depends on**: Phase 16
**Requirements**: IO-01, IO-02, IO-03, IO-04 (+ VER-05 applied throughout)
**Success Criteria** (what must be TRUE):

  1. Reader can find one canonical network input contract: `14D = [tau, IC_13]`.
  2. Reader can inspect one ordered 13-entry Jacobi-state IC vector with normalization rules for ordered raw masses, retained Jacobi position slots (`rho_x`, `lambda_x`, `lambda_y`), full Jacobi velocity slots, and energy. Shape invariants and orientation summaries are metadata only, not final network IC slots.
  3. Reader can distinguish 9D position predictions from velocities and accelerations derived by automatic differentiation, and can locate the mass-weighted COM projection head requirement on the raw output.
  4. Reader no longer encounters unqualified 11D, 12D, or ambiguous 13D/14D wording except where it is explicitly labeled as historical source-issue metadata.
  5. Every B-/M- finding in scope has its issue-ledger status updated, and any discovered mismatch with existing `pinn/` implementation files is recorded as downstream code-alignment work rather than patched in v1.4.

**Plans**: 3/3 complete (`17-01-PLAN.md`, `17-02-PLAN.md`, `17-03-PLAN.md`)

### Phase 18: Frame and Gauge Contracts

**Goal**: Framework specs define one frame, gauge, and output-space convention for ICs, Brutus snapshots, and model predictions.
**Depends on**: Phase 17
**Requirements**: FRAME-01, FRAME-02, FRAME-03, FRAME-04
**Success Criteria** (what must be TRUE):

  1. Reader can follow one preprocessing order: COM recentering, zero-momentum boost, canonical ordering, canonical rotation gauge, then scaling.
  2. Reader can find explicit COM and total-momentum assertions for preprocessed samples and model outputs.
  3. Reader can see how hierarchical post-perturbation COM offsets and standard quasi-random COM behavior are reconciled with the sampling spec.
  4. Reader can verify the output contract remains 3D Cartesian trajectories and is not replaced by planar or invariant-only predictions.

**Completion**: Phase 18 completed 2026-05-21; Phase 19 is next.

**Plans**: 3/3 complete (`18-01-PLAN.md`, `18-02-PLAN.md`, `18-03-PLAN.md`)

**Wave 1**
- [x] `18-01-PLAN.md` — Create B-05/M3 evidence packets and define the unified CTL preprocessing, ordering, rotation-gauge, COM/momentum assertion, and FRAME-04 3D guard contract.

**Wave 2** *(blocked on Wave 1 completion)*
- [x] `18-02-PLAN.md` — Reconcile hierarchical and standard quasi-random sampling-frame behavior in `sampling_method.md` using `simulation_data/` as the FRAME-03 source of truth.

**Wave 3** *(blocked on Waves 1-2 completion)*
- [x] `18-03-PLAN.md` — Record FUT-01 frame/gauge code divergence and run full Phase 18 verification before closing B-05/M3 ledger state.

**Cross-cutting constraints:**
- No `pinn/` implementation files are edited during Phase 18.
- `ctl_instruction.md` Step 4 M4 constraint-counting prose remains untouched for Phase 19.
- `sampling_method.md` Sobol coordinate-allocation prose remains untouched for Phase 20.5.

### Phase 19: Physics and Loss Contracts

**Goal**: Framework specs state physically consistent scaling, derivative, softening, energy, and loss-balancing contracts — each one adjudicated against both source documents and locked at the root cause.
**Depends on**: Phase 18
**Requirements**: PHYS-01, PHYS-02, PHYS-03, PHYS-04, PHYS-05, PHYS-06 (+ VER-05 applied throughout)
**Success Criteria** (what must be TRUE):

  1. Reader can identify the raw-mass nondimensionalization convention and retained `D=(G*T^2)^(1/3)` scale, with the mass-fraction alternative documented as a future rewrite only and the EVID-05 adjudication of B-02 recorded.
  2. Reader can trace the normalized-time derivative contract, finding the autograd leaf named explicitly, the chain-rule factors stated when the leaf is `tau`, the requirement for componentwise derivatives (no `grad_outputs=torch.ones_like` aggregate), and the synthetic-trajectory test `r'(u) = [sin(2πu), cos(2πu), u²]` documented as a worked AD example.
  3. Reader can verify the physics residual and energy regularizer use a matched softened force/potential pair, with the chosen softening value (single matched `r_safe` vs. dual-context `eps_inv`/`eps_soft`) locked only after EVID-05 adjudication of B-09 against current epsilon usage in `simulation_data` and the close-encounter analysis in `01-architecture-and-physics-foundations.md`.
  4. Reader sees the energy term described as a soft conservation regularizer, not an HNN.
  5. Reader can confirm ALM is limited to scalar conservation constraints (default: E, L_x, L_y, L_z) and dense ODE residuals use a causal or otherwise justified weighting contract, with dual-variable update rules naming the optimizer phase that updates or freezes them.
  6. Reader can find the M4 constraint-counting replacement: the stale "13 constraints overdetermine an 8D reduced phase space" passage is removed and replaced with an evidence-backed statement of how many constraints v1.4 actually enforces and over what reduced phase space, after EVID-05 adjudication.

**Plans**: 4 plans (`19-01-PLAN.md`, `19-02-PLAN.md`, `19-03-PLAN.md`, `19-04-PLAN.md`)

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

### Phase 21: Acceptance Checks, Validation Execution, and Handoff

**Goal**: Acceptance checks are not only defined but **executed** with disposable validation probes against the v1.4 framework specs; the source-issue ledger is reconciled; and the final handoff records what shipped, what was deferred, and why.
**Depends on**: Phase 20 (or whichever phase last touched a contested finding)
**Requirements**: VER-01, VER-03, VER-04, VER-06 (+ VER-05 closing loop)
**Success Criteria** (what must be TRUE):

  1. Reader can inspect numerically-defined acceptance checks for scaling consistency, COM invariance, componentwise AD correctness, force-energy consistency, and loss stability — each named with its pass criterion, data, and executing command or disposable probe.
  2. The acceptance checks have **executed**, with pass/fail evidence recorded for each. Failing checks routed the work back to Phases 17–20 for spec correction (no v1.4 ships with a failing test); the iterative loop is visible in the ledger history.
  3. Reader can identify which Issue 01 findings were fixed, which are intentionally unchanged (including the M6/M7 "not adjudicable" deferral and any "accept-issue-doc" or "reject-both" verdicts from EVID-02), and which require future empirical validation.
  4. Reader can find the reconciled `SI-*` ledger entries in the framework specs: every v1.4-resolved finding retires its corresponding `SI-*` with a back-reference; entries outside Issue 01 (e.g., `SI-DQA-002`, `SI-DQA-003`, `SI-PINN-002`) are preserved untouched.
  5. `$gsd-plan-phase` for any downstream milestone can derive implementation plans from evidence packets, changed spec sections, and verification artifacts without redoing the conceptual audit.

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
| 16. Evidence Framework and Issue Adjudication | v1.4 | 3/3 | Complete    | 2026-05-16 |
| 17. Input and Output Contracts | v1.4 | 3/3 | Complete    | 2026-05-20 |
| 18. Frame and Gauge Contracts | v1.4 | 3/3 | Complete    | 2026-05-21 |
| 19. Physics and Loss Contracts | v1.4 | 2/4 | In Progress|  |
| 20. Architecture and Normalization Cleanup | v1.4 | 0/TBD | Not started | - |
| 21. Acceptance Checks and Handoff | v1.4 | 0/TBD | Not started | - |

---
*Last updated: 2026-05-21 — Phase 18 complete; next step is Phase 19 discussion.*
