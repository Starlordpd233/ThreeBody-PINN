# Requirements: Three-Body Physics-Informed LLM v1.4

**Defined:** 2026-05-15
**Core Value:** The simulation dataset and data pipeline must be clean, well-validated, and correctly processed; framework specs must be physically coherent before implementation work depends on them.

## v1.4 Requirements

### Evidence and Resolution Validation

- [ ] **EVID-01**: For each Issue 01 finding selected for remediation, the agent records direct evidence from `ctl_pinn_resolution.md`, `master_consolidation_report.md`, `01-architecture-and-physics-foundations.md`, and the current framework specs before editing.
- [ ] **EVID-02**: Each issue receives an explicit verdict: accept the resolution decision, reject it as unsupported, or defer it with a stated blocker.
- [ ] **EVID-03**: False positives from the original thematic issue report are documented as intentional non-changes, including why the current framework convention remains valid.
- [ ] **EVID-04**: Every accepted issue has a before/after evidence note that names the changed spec section and the contract it now enforces.

### Input and Output Contracts

- [ ] **IO-01**: Framework specs state one canonical network input contract: `14D = [tau, IC_13]`.
- [ ] **IO-02**: Framework specs define the 13-component IC vector in one consistent order with normalization rules for masses, energy, angular momentum, virial ratio, minimum separation, inertia, shape invariants, and velocity-orientation scalars.
- [ ] **IO-03**: Framework specs distinguish position outputs from velocities and accelerations derived by automatic differentiation.
- [ ] **IO-04**: Any obsolete 11D, 12D, or ambiguous 13D/14D wording is removed or explicitly labeled as historical source-issue metadata.

### Frame and Gauge Contracts

- [ ] **FRAME-01**: Framework specs define one preprocessing order for all ICs and Brutus snapshots: COM recentering, zero-momentum boost, canonical ordering, canonical rotation gauge, then scaling.
- [ ] **FRAME-02**: Framework specs state COM and total-momentum assertions for preprocessed samples and model outputs.
- [ ] **FRAME-03**: Hierarchical and standard quasi-random IC frame behavior is reconciled with the sampling spec, including the hierarchical post-perturbation COM offset.
- [ ] **FRAME-04**: The output contract preserves 3D Cartesian trajectories and does not collapse the framework into planar or invariant-only predictions.

### Physics and Loss Contracts

- [ ] **PHYS-01**: Framework specs lock the raw-mass nondimensionalization convention and retain `D=(G*T^2)^(1/3)` unless a full mass-fraction rewrite is explicitly chosen later.
- [ ] **PHYS-02**: Framework specs define the normalized-time derivative contract, including whether training differentiates with respect to `u=t/T` directly or applies the `tau` chain-rule factors.
- [ ] **PHYS-03**: Framework specs use a matched softened force/potential pair for physics residuals and energy regularization, with any offline invariant epsilon kept separate from training-time numerical softening.
- [ ] **PHYS-04**: The energy term is described as a soft conservation regularizer rather than an HNN unless the model actually parameterizes a Hamiltonian.
- [ ] **PHYS-05**: ALM is specified only for scalar conservation constraints, while dense ODE residuals use a causal or otherwise justified residual weighting contract.

### Architecture and Normalization Cleanup

- [ ] **ARCH-01**: SIREN initialization and frequency settings are stated consistently, with no epochwise `omega0` scheduler unless a reparameterized runtime mechanism is specified.
- [ ] **ARCH-02**: LayerNorm is documented as a project-specific stabilizer, and the affine/non-affine default is stated consistently.
- [ ] **ARCH-03**: `I_3` normalization maps the documented triangle-shape range to `[-1, 1]`.
- [ ] **ARCH-04**: `I_norm` uses separate names for the raw inertia descriptor and the tanh-squashed network input.
- [ ] **ARCH-05**: Energy and mass normalization support ranges are documented as realized dataset support, not treated as correctness failures when asymmetric or mostly negative.

### Verification and Handoff

- [ ] **VER-01**: The revised specs include enough acceptance checks for downstream implementation planning to verify scaling consistency, COM invariance, derivative correctness, force-energy consistency, and loss stability.
- [ ] **VER-02**: The roadmap maps every v1.4 requirement to exactly one phase beginning at Phase 16.
- [ ] **VER-03**: The final milestone handoff identifies which issues were fixed, which were intentionally left unchanged, and which require future empirical validation.

## Future Requirements

- **FUT-01**: Implement the corrected framework contracts in code after spec reconciliation is complete.
- **FUT-02**: Recompute curriculum statistics and stage thresholds after preprocessing and physics contracts are finalized.
- **FUT-03**: Add executable validation scripts for the corrected contracts if not completed during v1.4.
- **FUT-04**: Resume PINN training-loop implementation after the framework specs are coherent.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Brutus integrator changes | Issue 01 concerns framework architecture and physics contracts, not the validated C++ integrator. |
| LLM fine-tuning prep | Deferred until framework and data contracts are stable. |
| Broad rewrite of non-Issue-01 specs | This milestone is scoped to Architecture and Physics Foundations. |
| Empirical curriculum redesign beyond required evidence notes | Curriculum work belongs to later issue themes unless needed to validate an Issue 01 contract. |
| Replacing the SQR-SkipResNet-SIREN backbone wholesale | The resolution preserves the backbone unless contradicted by validated physics or architecture evidence. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| EVID-01 | Phase 16 | Pending |
| EVID-02 | Phase 16 | Pending |
| EVID-03 | Phase 16 | Pending |
| EVID-04 | Phase 16 | Pending |
| IO-01 | Phase 17 | Pending |
| IO-02 | Phase 17 | Pending |
| IO-03 | Phase 17 | Pending |
| IO-04 | Phase 17 | Pending |
| FRAME-01 | Phase 18 | Pending |
| FRAME-02 | Phase 18 | Pending |
| FRAME-03 | Phase 18 | Pending |
| FRAME-04 | Phase 18 | Pending |
| PHYS-01 | Phase 19 | Pending |
| PHYS-02 | Phase 19 | Pending |
| PHYS-03 | Phase 19 | Pending |
| PHYS-04 | Phase 19 | Pending |
| PHYS-05 | Phase 19 | Pending |
| ARCH-01 | Phase 20 | Pending |
| ARCH-02 | Phase 20 | Pending |
| ARCH-03 | Phase 20 | Pending |
| ARCH-04 | Phase 20 | Pending |
| ARCH-05 | Phase 20 | Pending |
| VER-01 | Phase 21 | Pending |
| VER-02 | Phase 16 | Pending |
| VER-03 | Phase 21 | Pending |

**Coverage:**
- v1.4 requirements: 25 total
- Mapped to phases: 25
- Unmapped: 0

---
*Requirements defined: 2026-05-15*
*Last updated: 2026-05-15 after milestone v1.4 roadmap creation*
