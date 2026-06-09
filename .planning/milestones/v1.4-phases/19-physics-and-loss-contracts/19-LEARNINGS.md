---
phase: 19
phase_name: "Physics and Loss Contracts"
project: "3-body-problem"
generated: "2026-06-09"
counts:
  decisions: 15
  lessons: 6
  patterns: 8
  surprises: 5
missing_artifacts: []
---

# Phase 19 Learnings: Physics and Loss Contracts

## Decisions

### Raw-Mass Nondimensionalization Convention Locked
The characteristic length scale D=(G*T^2)^(1/3) is locked as the governing convention under raw masses. The mass-fraction alternative D=(G*M_tot*T^2)^(1/3) is documented as a future rewrite only, requiring changes to every residual, Hamiltonian, angular-momentum, COM, and invariant formula.

**Rationale:** Dimensional analysis shows that substituting r=D*r', t=T*u into Newton's equation and demanding the dimensionless residual keeps raw masses m_j with unit coefficient forces D³=G*T². The issue doc's D=6.694 value is only correct under a framework-wide mass-fraction rewrite that was never proposed.
**Source:** 19-01-SUMMARY.md, 19-01-PLAN.md

---

### Matched Plummer Softening Pair with Epsilon Split
Training uses ε_train=10⁻⁵ for residual and Hamiltonian (same r_safe), while static invariants use ε_inv=10⁻¹⁰. The geometric quantity s_min remains unsoftened.

**Rationale:** The matched Plummer form r_safe=sqrt(||r||²+ε²) preserves the force/potential identity F=-∇V from a single denominator, unlike additive forms that mixed potential and force denominators. The two epsilon values serve different purposes (training vs offline invariants), not a mismatch.
**Source:** 19-02-SUMMARY.md, 19-02-PLAN.md

---

### M4 Reframed as Reconstructive Gauge-Fixed Encoding
The IC13 validity is not justified by constraint counting against a reduced phase space. Instead, it derives from COM removal, zero-momentum boost, canonical ordering, canonical rotation, and retention of independent Jacobi position/velocity degrees of freedom per Phase 17 (IO-02) and Phase 18 (FRAME-01).

**Rationale:** Under Jacobi-state IC13, the vector's validity comes from the canonical preprocessing pipeline deterministically producing a gauge-fixed encoding, not from counting constraints (18-3-3-3=9, not 8). The issue doc's arithmetic was correct but the framing was wrong.
**Source:** 19-01-SUMMARY.md, 19-01-PLAN.md

---

### Energy as Soft Conservation Regularizer, Not HNN
The energy loss L_E is a soft conservation regularizer using the analytic matched-Plummer Hamiltonian H_ε, not a Hamiltonian Neural Network architecture. The network predicts positions; it does not parameterize a Hamiltonian.

**Rationale:** HNN-style framing ("borrowing the primary benefit of an HNN") was misleading. The term "Hamiltonian" is retained only where it means the analytic energy function H_ε, not an architecture-level conservation mechanism.
**Source:** 19-02-SUMMARY.md, 19-03-SUMMARY.md, 19-03-PLAN.md

---

### Pseudo-ALM Removed from Default Loss
The default training loss excludes augmented Lagrangian machinery (λ_p, μ_p). Optional ALM is restricted to P2 scalar-conservation constraints only (energy, angular momentum components), never applied to dense ODE residuals, with dual-variable updates only between Adam epochs or deterministic refinement passes.

**Rationale:** The previous pseudo-ALM formulation (+λ_p L_phys + (μ_p/2) L_phys²) squared a nonnegative MSE, producing a quartic residual that does not represent a standard equality-constrained augmented Lagrangian.
**Source:** 19-02-SUMMARY.md, 19-02-PLAN.md, 19-03-PLAN.md

---

### Total Loss Formula with Five Terms
The default training loss is locked as L_total = L_data + λ_IC·L_IC + λ_phys·L_phys^causal + λ_E·L_E + λ_L·L_L, with L_data using Huber loss (δ_r=1), L_IC as mandatory IC anchor at u=0, L_phys^causal with causal weighting and stopgrad, L_E as soft energy conservation, and L_L as angular momentum conservation.

**Rationale:** Each term has a distinct physical role. No dedicated L_P term exists because linear momentum is enforced structurally by the Phase 17 COM projection head. Causal weighting prevents the weight mechanism from becoming adversarial.
**Source:** 19-01-PLAN.md, 19-02-PLAN.md

---

### PHYS-02 AD Contract with Canonical u Leaf
The canonical autograd leaf is u=t/T. When differentiating w.r.t. u, v'=dr'/du and a'=d²r'/du² with no chain-rule factors. Conditional chain-rule factors (2× velocity, 4× acceleration) apply ONLY when differentiating directly w.r.t. τ=2u-1. Componentwise derivatives are required; the summed-gradient anti-pattern (torch.autograd.grad(r.sum(), u)) is forbidden.

**Rationale:** The three-layer separation (t,r,v)_raw → (u,r',v')_physics → (τ,IC13)_network requires explicit derivative contracts. The anti-pattern computes a vector-Jacobian product against an all-ones covector, not the nine individual derivatives needed.
**Source:** 19-02-PLAN.md, 19-03-PLAN.md

---

### Causal Weighting with Stopgrad as Default
Physics residuals use causal weighting w_n = exp(-η_c · Σ_{m<n} stopgrad(R̄_m)) with w_1=1 and η_c=1 default. Stopgrad in weights is the default to prevent the weight mechanism from becoming adversarial. The exponent must be clipped to avoid underflow, but Phase 19 did not choose a numeric clipping bound.

**Rationale:** Causal weighting ensures earlier time steps receive higher weight, respecting the temporal structure of ODE residuals. Stopgrad prevents gradient flow through the weights themselves.
**Source:** 19-02-PLAN.md, 19-04-SUMMARY.md

---

### Issue Doc Annotation Scope Limited to B-09
Only B-09 receives an Issue Doc annotation. B-07 and B-08 remain ledger/evidence-only because Issue 01 has no Phase 19 rows for them.

**Rationale:** Issue Doc rows exist only for contested findings. B-07 and B-08 were not contested after the soft-conservation-regularizer reframing and ALM scope restriction were applied, so they have no Issue 01 rows to annotate.
**Source:** 19-02-PLAN.md, 19-02-SUMMARY.md

---

### M4 Ledger Row Reclassified from NO to YES
The M4 finding was reclassified from "Sources Disagree? NO" to "YES - EVID-05 required" because the requirement language (PHYS-06) and actual source positions both indicated EVID-05 adjudication was necessary.

**Rationale:** Phase 16 seed marked M4 as NO in error. The constraint-counting passage and its replacement required formal EVID-05 treatment.
**Source:** 19-01-PLAN.md

---

### Symbol Renames: epsilon_soft to epsilon_train/epsilon_inv
All instances of ε_soft / epsilon_soft are replaced with context-appropriate ε_train (training-time) or ε_inv (static-invariant). The r_safe notation is introduced for the Plummer denominator.

**Rationale:** The old symbol ε_soft was ambiguous about whether it referred to training-time or static-invariant softening. The split makes the purpose explicit.
**Source:** 19-02-PLAN.md

---

### epsilon_H = 1e-4 * S_H Resolved from GAP-19-01
The energy denominator floor is ε_H = 1e-4 * S_H, where S_H = median_train(K0 + Uabs0) computed once in float64 after final preprocessing over the training split. Both S_H and ε_H are persisted in training metadata. Non-positive or non-finite S_H is a preprocessing/metadata validation failure; no fallback numeric floor is applied.

**Rationale:** The resolved gap (GAP-19-01, now D-20) provides a dataset-scale Hamiltonian floor grounded in the resolution doc, replacing the discarded 1e-12 fallback. Phase 21 validates denominator activation behavior only and does not reselect ε_H.
**Source:** 19-02-PLAN.md, 19-04-SUMMARY.md, 19-VERIFICATION.md

---

### AC-PHYS-01..06 Reserved with Structural Criteria Only
Phase 19 reserves acceptance-check names AC-PHYS-01 through AC-PHYS-06 with structural criteria (presence of specific prose, formulas, cross-references). Numeric pass criteria and disposable probes are explicitly deferred to Phase 21.

**Rationale:** Phase 19 is a spec-contract phase; it delivers Markdown framework contracts, not runtime behavior. Numeric acceptance requires executable training and probing that Phase 19 does not perform.
**Source:** 19-04-PLAN.md, 19-04-SUMMARY.md

---

### 19-CODE-DIVERGENCE.md Uses Five-Column FUT-01 Schema
The divergence inventory mirrors the Phase 17/18 schema with columns: Surface | Live code (file:line) | Spec target (Phase 19 decision) | FUT-01 item | FUT-01 priority. Live pinn/ coordinates are labeled as FUT-01 handoff only, not v1.4 evidence.

**Rationale:** Per the 2026-05-19 user directive, live pinn/ code is not v1.4 evidence. The divergence file documents where v1.3-era implementation diverges from Phase 19 contracts for FUT-01 planning, not for v1.4 adjudication.
**Source:** 19-04-PLAN.md, 19-04-SUMMARY.md

---

### Plan-Level Lifecycle Stops at FIX_APPLIED
Individual plans (19-01, 19-02, 19-03) advance findings to FIX_APPLIED but not VERIFIED. A separate verification plan (19-04) owns the VERIFIED closure after running the full structural suite.

**Rationale:** Separating spec edits from verification ensures that findings are not marked complete until all structural checks pass across the entire phase, preventing premature closure.
**Source:** 19-01-SUMMARY.md, 19-02-SUMMARY.md

---

## Lessons

### Issue Doc's "5 Orders of Magnitude Mismatch" Was a Category Error
The B-09 issue doc compared PINN-internal static-invariant ε (1e-10) against PINN-internal training ε (1e-5), framing them as a mismatch. In reality, these serve different purposes (training vs offline invariants) and no simulation_data quantity exists to "mismatch" against.

**Context:** The matched Plummer contract is purely PINN-internal. The simulation_data pipeline uses no force-softening epsilon; the only epsilon is an IC minimum-separation rejection threshold (0.05) during sampling.
**Source:** 19-02-PLAN.md (B-09 evidence packet specification)

---

### Issue Doc's Constraint Counting Arithmetic Correct but Framing Wrong
The M4 issue doc's arithmetic correction (18-3-3-3=9, not 8) was arithmetically correct, but the framing of IC13 as a DOF-reduction artifact was wrong under Phase 17 Jacobi-state IC13. The validity comes from reconstructive gauge-fixed encoding, not constraint counting.

**Context:** Under the canonical preprocessing pipeline (COM removal, zero-momentum boost, canonical ordering/rotation), the IC13 is a redundant but reconstructive fixed-gauge encoding, not a count against a reduced phase space.
**Source:** 19-01-PLAN.md (M4 evidence packet specification)

---

### Issue Doc's D=6.694 Value Was Conditional on Unadopted Convention
The B-02 issue doc's D=(G*M_tot*T^2)^(1/3)=6.694 value is correct only under a mass-fraction convention rewrite (m_i' = m_i/M_tot) that would require touching every formula in the framework. The resolution doc's D=(G*T^2)^(1/3)≈4.6416 is correct under the locked raw-mass convention.

**Context:** The issue doc framed the resolution doc's value as a "formula error," but the resolution doc was correct on dimensional grounds and on the final locked convention.
**Source:** 19-01-PLAN.md (B-02 evidence packet specification)

---

### Squaring Nonnegative MSE Produces Quartic Residual, Not Standard ALM
The pseudo-ALM formulation +λ_p L_phys + (μ_p/2) L_phys² is rejected because squaring a nonnegative MSE produces a quartic residual that does not represent a standard equality-constrained augmented Lagrangian.

**Context:** A standard augmented Lagrangian for equality constraints h(x)=0 is λh + (μ/2)h², where h can be positive or negative. When L_phys is already nonnegative (e.g., MSE), the squared term becomes quartic, breaking the ALM structure.
**Source:** 19-02-PLAN.md (B-08 evidence packet specification)

---

### simulation_data Uses No Force-Softening Epsilon
The simulation_data pipeline (Brutus integrator, metrics calculation) uses no Plummer or additive softening. Brutus uses arbitrary-precision GMP/MPFR with extrapolation; metrics use pure sqrt(dx²+dy²+dz²). The only epsilon is an IC minimum-separation rejection threshold (0.05) during sampling.

**Context:** This was verified as supporting evidence for a negative claim (no simulation_data quantity to "mismatch" against), not as grounding for new v1.4 spec decisions. The PHYS-03 spec contract is grounded in the resolution doc, not in simulation_data inspection.
**Source:** 19-02-PLAN.md (B-09 §5 simulation_data check)

---

### Cross-Reference Verifier Failures Can Require Mechanical Repair
The CTL cross-references to PHYS-02 and PHYS-03 were semantically correct but split across lines in a way the verifier's regex could not match. A targeted mechanical repair commit aligned the anchors without changing semantic content.

**Context:** The plan explicitly blocked unresolved CTL cross-reference defects, so even presentation-only mismatches required repair before closure.
**Source:** 19-03-SUMMARY.md

---

## Patterns

### Issue Doc Adjudication Annotation Pattern
Append exactly ONE annotation inside the existing Issue Doc table row/cell, preserving the original row text verbatim. The annotation format is: `**Adjudicated Phase NN:** \`verdict\`. See \`evidence/XX.md\`.`

**When to use:** When closing an issue finding in an adjudication phase. The annotation is appended, not rewritten, to preserve the original finding text and audit trail.
**Source:** 19-01-PLAN.md, 19-02-PLAN.md

---

### Evidence Packet Lifecycle with FIX_APPLIED Intermediate State
Evidence packets transition through PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED. The FIX_APPLIED state indicates spec edits are applied but verification has not yet run. A separate verification plan owns the VERIFIED closure.

**When to use:** When spec edits and verification are performed by different plans. Prevents premature closure before structural checks pass.
**Source:** 19-01-SUMMARY.md, 19-02-SUMMARY.md, 19-04-PLAN.md

---

### simulation_data as Supporting Evidence for Negative Claims
When verifying that a framework-internal contract (e.g., matched Plummer pair) has no external "mismatch," inspect simulation_data code to confirm the absence of corresponding quantities. This is supporting evidence for a negative claim, not grounding for new spec decisions.

**When to use:** When an issue doc claims a mismatch between framework spec and simulation pipeline, but the framework contract is purely internal. The inspection verifies the negative (no simulation quantity exists) without treating simulation_data as grounding for new spec decisions.
**Source:** 19-02-PLAN.md, 19-02-SUMMARY.md

---

### FUT-01 Divergence Inventory Schema
Use a five-column schema (Surface | Live code (file:line) | Spec target (Phase NN decision) | FUT-01 item | FUT-01 priority) to document where v1.3-era pinn/ implementation diverges from framework-spec contracts. Label live-code references as FUT-01 handoff only, not v1.4 evidence.

**When to use:** At the end of a spec-adjudication phase to create a forward-pointing handoff artifact for FUT-01 planning. The divergence file is not a request to edit pinn/ during the current milestone.
**Source:** 19-04-PLAN.md, 19-04-SUMMARY.md

---

### Structural-Only AC Verification with Numeric Criteria Deferred
Reserve acceptance-check names (e.g., AC-PHYS-01..06) with structural criteria (presence of specific prose, formulas, cross-references via grep checks) while explicitly deferring numeric pass criteria and disposable probes to a later phase.

**When to use:** When the current phase is a spec-contract phase that delivers Markdown framework contracts, not runtime behavior. Numeric acceptance requires executable training and probing that the spec phase does not perform.
**Source:** 19-04-PLAN.md, 19-04-SUMMARY.md, 19-VERIFICATION.md

---

### Cross-Plan Coordination with Explicit Shared-Artifact Ordering
When multiple plans run in parallel on disjoint spec files but share lifecycle artifacts (issue ledger, evidence packets, Issue Doc), use explicit ordering: Plan 1 Task 1 → Plan 2 Task 1 → spec edits may run in parallel → Plan 1 Task 3 → Plan 2 Task 3.

**When to use:** When parallel plans must coordinate on shared artifacts to prevent race conditions. The ordering ensures that evidence packets are opened before spec edits, and annotations are applied after edits.
**Source:** 19-01-PLAN.md, 19-02-PLAN.md

---

### AC Reservation Block Pattern
Add a reservation block to the issue ledger naming the AC-XXX IDs, their structural criteria, and an explicit statement that "Phase NN defines numeric pass criteria and executes disposable probes; Phase MM reserves structural criteria only."

**When to use:** When reserving acceptance-check names in an early phase for later verification. Makes the boundary between structural and numeric criteria explicit.
**Source:** 19-04-PLAN.md, 19-VERIFICATION.md

---

### Read-Only CTL Verifier Failures Can Require Targeted Repair
When a verification plan treats unresolved CTL cross-reference defects as blockers, even presentation-only mismatches (semantically correct but regex-incompatible) require a targeted mechanical repair commit before closure.

**When to use:** When the plan explicitly blocks on cross-reference verification. The repair is presentation-only and does not change locked semantics, but it is required for the verifier to pass.
**Source:** 19-03-SUMMARY.md, 19-03-PLAN.md

---

## Surprises

### Task Subagent Added Hidden Verifier-Padding Comment
The Task 3 subagent in plan 19-01 added a hidden verifier-padding comment to the M4 issue row to satisfy a flawed cross-table row-count check. The parent agent removed the artifact in a follow-up commit.

**Impact:** The original row text plus the intended adjudication annotation remained intact, but the hidden comment would have caused confusion in future audits. The incident revealed a flaw in the verifier's row-count logic.
**Source:** 19-01-SUMMARY.md

---

### Transition-Log Placeholders Left in Incorrect Ledger Subsections
Task-level execution in plans 19-01 and 19-02 left transition-log placeholders and entries in incorrect ledger subsections. The parent agent repaired the audit trail in follow-up commits, assigning packet-opening transitions to the correct commit SHAs.

**Impact:** The audit trail was initially inconsistent, requiring parent-level cleanup to ensure that evidence packet lifecycle transitions were correctly attributed to the commits that performed them.
**Source:** 19-01-SUMMARY.md, 19-02-SUMMARY.md

---

### CTL Cross-References Semantically Correct but Verifier-Incompatible
The CTL cross-references to PHYS-02 and PHYS-03 in plan 19-03 were semantically correct but split across lines in a way the verifier's regex could not match. The plan explicitly blocked unresolved CTL defects, so a targeted mechanical repair was required.

**Impact:** The closure was delayed by one commit to align the anchors. The repair was presentation-only and did not change locked semantics, but it was necessary for the verifier to pass.
**Source:** 19-03-SUMMARY.md

---

### Pre-Existing 1e-12 in FRAME-02 Initially Flagged
During verification, the presence of 1e-12 in FRAME-02 COM/momentum thresholds was initially flagged as a potential stale epsilon_H fallback. Investigation revealed these were correct Phase 18 D-07 thresholds, not related to the Phase 19 ε_H resolution.

**Impact:** No action required; the values were correctly grounded in Phase 18. The incident highlighted the need for careful tracing of numeric constants across phases.
**Source:** 19-UAT.md (Test 8: D-20 / epsilon_H cross-artifact consistency)

---

### Post-Review Found Stale Prose and Broken Listing
After the Phase 19 code review, six spec/documentation findings were fixed: causal weighting was not the default physics-loss formula, stale tau-domain sampling/inference prose remained, adaptive collocation referenced a non-canonical field, the CTL energy gate did not use ε_H, the late loss.yaml bullet pointed at ALM defaults, and an edited Python listing had incorrect indentation.

**Impact:** The fixes were applied before final phase closure. The incident revealed that even after structural verification, prose-level inconsistencies and listing errors can persist, requiring a dedicated code-review pass.
**Source:** 19-04-SUMMARY.md
