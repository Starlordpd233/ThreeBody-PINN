# Requirements: Three-Body Physics-Informed LLM v1.4

**Defined:** 2026-05-15
**Core Value:** The simulation dataset and data pipeline must be clean, well-validated, and correctly processed; framework specs must be physically coherent before implementation work depends on them.

**Current workflow state:** v1.3, Phase 15.1, the post-ship SCS gate correction, and v1.4 Phases 16 through 21 are complete. Phase 22 framework-spec cleanup is next and is the final v1.4 phase.

## v1.4 Requirements

### Evidence and Resolution Validation

Resolution-doc treatment policy: `ctl_pinn_resolution.md` is the most recent adjudication of Issue 01 and is the candidate set of fixes for v1.4. Per user directive 2026-05-18, it is adopted as the **default verdict source** — the agent transcribes its positions into framework-spec edits unless EVID-05 surfaces concrete evidence that the position fails. Every claim in it must survive critical examination against `01-architecture-and-physics-foundations.md`, the current framework specs (`ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`), and first-principles physics before any spec edit is applied. `master_consolidation_report.md` is supporting evidence consumed by the resolution doc, not a co-equal primary source. **Live code in `pinn/` is NOT part of the examination basis** (directive 2026-05-19) — the v1.3-era code is artifact, not authority, and will be rebuilt from the v1.4 specs in FUT-01. Live-code references are permitted only in forward-pointing FUT-01 hand-off documents.

Empirical Decision Loop support: when a source-silent decision is empirically consequential and the agent cannot decide whether theory/source material is enough, the agent records the decision in the phase-local gap register and may attach a central EDL research brief under `.planning/research/edl/`. The brief packages context for user-led external research; it is not itself grounding, does not resolve the gap, and does not authorize probe execution without user instruction. Phase-local gap registers remain the canonical blocking and resolution records.

- [x] **EVID-01**: For each Issue 01 finding selected for remediation, the agent records direct evidence from `ctl_pinn_resolution.md`, `01-architecture-and-physics-foundations.md`, and the current framework specs before editing. Evidence packets cite line ranges, not whole files. (Live code in `pinn/` is NOT a source of evidence per the 2026-05-19 directive — the v1.3-era code is non-authoritative artifact, rebuilt in FUT-01 from v1.4 specs.)
- [x] **EVID-02**: Each issue receives an explicit verdict drawn from a fixed set — `accept-resolution`, `accept-issue-doc`, `accept-third-position`, `reject-both-as-unsupported`, or `defer-with-blocker` — with the reasoning recorded in the evidence packet.
- [x] **EVID-03**: False positives in either source document are documented as intentional non-changes, including why the current framework convention remains valid and which source(s) misread it.
- [x] **EVID-04**: Every accepted issue has a before/after evidence note that names the changed spec section, the contract it now enforces, and the verification step that will confirm the fix.
- [x] **EVID-05**: When `ctl_pinn_resolution.md` and `01-architecture-and-physics-foundations.md` give different verdicts on the same finding (currently B-02 D formula, B-04 input-vector orientation slots, B-09 softening strategy, M5 `I_3` mapping — and any further conflicts discovered during the walkthrough), the agent (a) reads both positions in full, (b) verifies each claim against the current framework specs and first-principles physics (Newtonian N-body equations, dimensional analysis, SIREN initialization, ALM constraint theory), (c) identifies the root-cause ambiguity in the framework specs that produced the disagreement, (d) locks the underlying convention explicitly, and (e) records the adjudication — including which source was correct, which was wrong, and why — in the issue evidence packet before any spec edit is applied. (Live code in `pinn/` is NOT in the examination basis per the 2026-05-19 directive.)

### Input and Output Contracts

- [x] **IO-01**: Framework specs state one canonical network input contract: `14D = [tau, IC_13]`.
- [x] **IO-02**: Framework specs define the 13-component Jacobi-state IC vector in one consistent order, with ordered raw mass slots, retained Jacobi position slots, full Jacobi velocity slots, energy, and per-slot normalization rules. Shape invariants and orientation summaries are metadata only, not final network IC slots.
- [x] **IO-03**: Framework specs distinguish position outputs from velocities and accelerations derived by automatic differentiation, and require a mass-weighted COM projection on the raw 9D position head before any output is consumed by a loss term.
- [x] **IO-04**: Any obsolete 11D, 12D, or ambiguous 13D/14D wording is removed or explicitly labeled as historical source-issue metadata.

### Frame and Gauge Contracts

- [x] **FRAME-01**: Framework specs define one preprocessing order for all ICs and Brutus snapshots: COM recentering, zero-momentum boost, canonical ordering, canonical rotation gauge, then scaling.
- [x] **FRAME-02**: Framework specs state COM and total-momentum assertions for preprocessed samples and model outputs.
- [x] **FRAME-03**: Hierarchical and standard quasi-random IC frame behavior is reconciled with the sampling spec, including the hierarchical post-perturbation COM offset.
- [x] **FRAME-04**: The output contract preserves 3D Cartesian trajectories and does not collapse the framework into planar or invariant-only predictions.

### Physics and Loss Contracts

- [x] **PHYS-01**: Framework specs lock the raw-mass nondimensionalization convention and retain `D=(G*T^2)^(1/3)` unless a full mass-fraction rewrite is explicitly chosen later.
- [x] **PHYS-02**: Framework specs define the normalized-time derivative contract, naming the autograd leaf explicitly (`u=t/T` or `tau=2u-1`) and specifying the chain-rule factors when the leaf differs from `u`. The contract requires componentwise derivatives per output coordinate — not a `grad_outputs=torch.ones_like(...)` aggregate — and includes the synthetic-trajectory test `r'(u) = [sin(2πu), cos(2πu), u²]` as a worked example whose AD outputs must match symbolic derivatives.
- [x] **PHYS-03**: Framework specs use a matched softened force/potential pair for physics residuals and energy regularization, with any offline invariant epsilon kept separate from training-time numerical softening. The chosen softening value (single matched `r_safe` vs. dual-context `eps_inv`/`eps_soft`) is locked only after EVID-05 adjudication against the current `simulation_data` epsilon usage and the close-encounter analysis in `01-architecture-and-physics-foundations.md`.
- [x] **PHYS-04**: The energy term is described as a soft conservation regularizer rather than an HNN unless the model actually parameterizes a Hamiltonian.
- [x] **PHYS-05**: ALM is specified only for scalar conservation constraints (E, L_x, L_y, L_z by default), while dense ODE residuals use a causal or otherwise justified residual weighting contract. Dual-variable update rules name which optimizer phase (Adam/L-BFGS) updates or freezes them.
- [x] **PHYS-06**: The constraint-counting passage in `ctl_instruction.md` ("13 constraints overdetermine an 8D reduced phase space") is replaced with an evidence-backed statement of how many constraints v1.4 actually enforces and over what reduced phase space. The replacement text is locked only after EVID-05 adjudication of M4 against the gauge-fixing logic in the resolution doc and the dimension accounting in `01-architecture-and-physics-foundations.md`.

### Architecture and Normalization Cleanup

- [x] **ARCH-01**: SIREN initialization and frequency settings are stated consistently, with no epochwise `omega0` scheduler unless a reparameterized runtime mechanism is specified.
- [x] **ARCH-02**: LayerNorm is documented as a project-specific stabilizer, and the affine/non-affine default is stated consistently.
- [x] **ARCH-03**: `I_3` normalization maps the documented triangle-shape range to `[-1, 1]`.
- [x] **ARCH-04**: `I_norm` uses separate names for the raw inertia descriptor and the tanh-squashed network input.
- [x] **ARCH-05**: Energy and mass normalization support ranges are documented as realized dataset support, not treated as correctness failures when asymmetric or mostly negative.

### Sampling Coordinate Allocation

- [x] **SAMP-01**: `sampling_method.md` documents an explicit Sobol coordinate allocation convention with no coordinate reused for two independent physical quantities. Allocation order: position → optional scale → optional velocity. Dimension formula `d = 3 + δ_s + 3δ_v`, where `δ_s = 1` iff sampling-time scaling is enabled and `δ_v = 1` iff velocity sampling is enabled.
- [x] **SAMP-02**: The §1.1 dimension claim, the "Sampling-Time Size Variability" prose, and the "Velocity Sampling" prose/formula in `sampling_method.md` are mutually consistent and agree with the locked allocation and with the documented and current behavior of `simulation_data/Scripts/ic_generation/` under its standard configuration (`scale_range=(0.8, 1.2)`, `velocity_scale=0.1`, `rotate=False`). The Phase 20.5 spec/code alignment does not depend on asserting an exact script revision for every stored file; it depends on the documented generator identity and its current, observable behavior under the standard configuration.

### Verification and Handoff

- [x] **VER-01**: The revised specs include numerically-defined acceptance checks for scaling consistency, COM invariance, derivative correctness, force-energy consistency, and loss stability. Each check names its pass criterion (e.g., `relative_error < 1e-10`), the data it runs on, and the command or function that executes it — not just prose descriptions.
- [x] **VER-02**: The roadmap maps every v1.4 requirement to exactly one phase beginning at Phase 16.
- [x] **VER-03**: The Phase 21 validation handoff identifies which issues were fixed, which were intentionally left unchanged (with the M6/M7 "not adjudicable from supplied files" deferral made explicit), and which require future empirical validation; Phase 22 consumes this handoff while performing final presentation cleanup.
- [x] **VER-04**: The acceptance checks defined in VER-01 are **executed** during Phase 21 — not just documented — using disposable validation probes that **implement what the v1.4 framework specs say** (directive 2026-05-19; the probes test the specs, not the v1.3-era code). Each test (§10.1 scaling, §10.2 COM, §10.3 componentwise AD on the synthetic trajectory, §10.4 force-energy consistency, §10.5 loss stability dry run) produces a recorded pass/fail with numerical evidence. A failing test blocks phase completion and routes back to the originating phase (17–20.5) for spec re-fix; v1.4 does not ship while any required test fails. The validation probes are disposable: their job is to confirm the framework specs are self-consistent and implementable. Passing or failing VER-04 does NOT touch the v1.3-era `pinn/` implementation — code alignment is FUT-01.
- [x] **VER-05**: Every fix is closed through an iterative re-verification loop. The issue ledger tracks each finding through `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED`. A finding only advances to `VERIFIED` after the corresponding acceptance check passes; an applied edit that fails re-verification stays at `IN_PROGRESS` and is re-fixed before any phase exits. After each batch of edits the agent re-runs verification on every previously `VERIFIED` finding the batch could have regressed (same spec section, dependent contract, or shared formula) and reverts the status to `IN_PROGRESS` on any regression. The ledger lives at a stable path (recommended: `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md`) and every phase appends to it; nothing in v1.4 closes until all in-scope findings are `VERIFIED` or explicitly `DEFERRED` with a written blocker.
- [x] **VER-06**: The framework-spec Source-Issue (`SI-*`) ledger is reconciled: every v1.4-resolved finding retires its corresponding `SI-*` entry with a back-reference to the resolving phase/commit (candidates: `SI-CTL-001` ↔ B-03, `SI-PINN-001` ↔ B-04, `SI-SSR-001` ↔ M5). Entries unrelated to Issue 01 are preserved untouched (`SI-PINN-002`, `SI-DQA-002`, `SI-DQA-003`).

## Future Requirements

- **FUT-01**: Update existing `pinn/` implementation code and build the broader PINN training loop after framework-spec reconciliation is complete.
- **FUT-02**: Recompute curriculum statistics and stage thresholds after preprocessing and physics contracts are finalized.
- **FUT-03**: Repurposed — package any useful VER-04 disposable validation probes into reusable executable scripts under `pinn/validation/` once v1.4 ships, so CI or later milestones can re-run them.
- **FUT-04**: Resume PINN training-loop implementation after the framework specs are coherent.
- **FUT-05**: Adjudicate the author comments preserved by Phase 22. Phase 22 censuses and preserves every author-flagged comment (any form/format) verbatim and hands them off via `.planning/phases/22-framework-spec-cleanup/22-COMMENT-HANDOFF.md`. A dedicated post-v1.4 phase performs the per-comment basis classification and disposition (keep / remove / revise / resurface) under human adjudication, per the WS-B disposition engine in `docs/work/designs/milestone_v1.4/framework-spec-cleanup/2026-06-07-framework-spec-cleanup-design.md` §6. Origin: GAP-22-01 (user decision 2026-06-08 to defer adjudication out of Phase 22).

## Scope Boundaries

| Scope | Status |
|-------|--------|
| **SCOPE-01** Existing `pinn/` implementation files (`pinn/basic_architecture.py`, `pinn/data-processing-pipeline-full.py`) | **Out of scope and NOT used as evidence** — per directive 2026-05-19, v1.4 does NOT inspect these files as evidence, grounding source, or source-of-truth for any spec decision. They are v1.3-era artifact, rebuilt in FUT-01 from v1.4 specs. Live-code references are permitted only in forward-pointing FUT-01 hand-off documents (`NN-CODE-DIVERGENCE.md`, eventual `pinn/STATUS.md`). |
| **SCOPE-02** `sampling_method.md` revisions | **In scope, limited to (a) FRAME-03** — hierarchical post-perturbation COM offset wording and any cross-reference needed for the unified preprocessing contract — **AND (b) SAMP-01/SAMP-02** — the Sobol coordinate allocation convention (Phase 20.5). No sampling-method content unrelated to (a) or (b) is rewritten. Any other sampling-method discrepancy noticed during Phase 20.5 (for example, the §2.1 enhancement framing) is out of Phase 20.5 scope and handled separately if needed, not silently fixed. |
| **SCOPE-03** Data-quality-assessment and SCS gate work | **Out of scope — already completed** on branch `codex/scs-gate-correction`. v1.4 does not re-open `SI-DQA-002`/`SI-DQA-003`. |
| **SCOPE-04** Disposable validation probes | **In scope, limited** — probes may be created, recorded, or run only to test risky framework contracts and produce evidence for VER-04. They are not production framework code and are not packaged as reusable `pinn/` validation infrastructure during v1.4. |
| **SCOPE-05** Data-spec alignment for sampling-method edits | When v1.4 framework-spec edits describe the data-generation pipeline, they MUST match the actual behavior of `simulation_data/Scripts/ic_generation/`. The no-live-code directive (2026-05-19) targets `pinn/` only; `simulation_data/Scripts/ic_generation/` is a permitted grounding source for data-generation specs because the existing dataset is fixed and the framework must remain compatible with it. Spec divergences from data must be (i) reconciled to match data, (ii) flagged in `docs/findings/` for separate handling, or (iii) explicitly authorized by the user as a data-regeneration directive for FUT-01. |
| **EDL support artifacts** | **Non-canonical support workflow** — `.planning/research/edl/README.md`, `.planning/research/edl/INDEX.md`, and central EDL briefs prepare user research for empirically consequential source-silent decisions. They support, but do not replace, phase gap registers and milestone requirements. |

## Out of Scope

| Feature | Reason |
|---------|--------|
| Brutus integrator changes | Issue 01 concerns framework architecture and physics contracts, not the validated C++ integrator. |
| LLM fine-tuning prep | Deferred until framework and data contracts are stable. |
| Broad rewrite of non-Issue-01 specs | This milestone is scoped to Architecture and Physics Foundations. Non-architecture specs (data quality, curriculum, sampling) are preserved unless a fix here directly requires touching them. |
| Empirical curriculum redesign beyond required evidence notes | Curriculum work belongs to later issue themes unless needed to validate an Issue 01 contract. |
| Replacing the SQR-SkipResNet-SIREN backbone wholesale | Both source documents preserve the backbone unless contradicted by validated physics or architecture evidence. |
| M6 and M7 from the resolution doc | The resolution doc declares these "not adjudicable from supplied files." v1.4 records them as explicit deferrals under VER-03 rather than guessing. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| EVID-01 | Phase 16 | Complete |
| EVID-02 | Phase 16 | Complete |
| EVID-03 | Phase 16 | Complete |
| EVID-04 | Phase 16 | Complete |
| EVID-05 | Phase 16 | Complete |
| IO-01 | Phase 17 | Complete |
| IO-02 | Phase 17 | Complete |
| IO-03 | Phase 17 | Complete |
| IO-04 | Phase 17 | Complete |
| FRAME-01 | Phase 18 | Complete |
| FRAME-02 | Phase 18 | Complete |
| FRAME-03 | Phase 18 | Complete |
| FRAME-04 | Phase 18 | Complete |
| PHYS-01 | Phase 19 | Complete |
| PHYS-02 | Phase 19 | Complete |
| PHYS-03 | Phase 19 | Complete |
| PHYS-04 | Phase 19 | Complete |
| PHYS-05 | Phase 19 | Complete |
| PHYS-06 | Phase 19 | Complete |
| ARCH-01 | Phase 20 | Complete |
| ARCH-02 | Phase 20 | Complete |
| ARCH-03 | Phase 20 | Complete |
| ARCH-04 | Phase 20 | Complete |
| ARCH-05 | Phase 20 | Complete |
| SAMP-01 | Phase 20.5 | Complete |
| SAMP-02 | Phase 20.5 | Complete |
| VER-01 | Phase 21 | Pending |
| VER-02 | Phase 16 | Complete |
| VER-03 | Phase 21 | Pending |
| VER-04 | Phase 21 | Pending |
| VER-05 | Phase 16 (defined) / Phases 17–22, including Phase 20.5 (applied) | Complete |
| VER-06 | Phase 21 | Pending |

**Coverage:**
- v1.4 requirements: 32 total (5 EVID + 4 IO + 4 FRAME + 6 PHYS + 5 ARCH + 2 SAMP + 6 VER)
- Mapped to phases: 32
- Unmapped: 0
- SCOPE-01 through SCOPE-05 are scope-boundary annotations (see "Scope Boundaries" table above), not numbered requirements.
- Phase 22 is added as the final presentation-preserving framework-spec cleanup; Phase 22-specific requirement mapping remains TBD pending phase planning, while existing cross-cutting VER-05 governance applies.

---
*Requirements defined: 2026-05-15*
*Last updated: 2026-06-08 after Phase 21 repair completion — all 32 v1.4 requirements are mapped; SAMP-01/SAMP-02 and VER-01/03/04/06 are complete; Phase 22-specific requirements remain TBD.*
