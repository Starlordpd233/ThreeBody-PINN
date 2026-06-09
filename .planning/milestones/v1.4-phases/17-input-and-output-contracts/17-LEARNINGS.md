---
phase: 17
phase_name: "Input and Output Contracts"
project: "3-body-problem"
generated: "2026-06-09"
counts:
  decisions: 14
  lessons: 4
  patterns: 9
  surprises: 2
missing_artifacts: []
---

# Phase 17 Learnings: Input and Output Contracts

## Decisions

### Decision 1: Raw 9D Position Head with Hard COM Projection
The network emits raw 9D positions only, then applies a hard mass-weighted center-of-mass (COM) projection before any data loss, physics residual, IC loss, conservation loss, or evaluation metric.

**Rationale:** Accepted D-02 / B-06 resolution — provides a single, unambiguous output surface for all downstream consumers (losses, metrics, AD-derived quantities).
**Source:** 17-02-SUMMARY.md

---

### Decision 2: Time Input Semantics and AD Derivation Chain
`u = t/T` is the autograd leaf and `tau = 2u - 1` is the bounded network input; velocities and accelerations are AD-derived from the projected positions, not directly output.

**Rationale:** Accepted D-03 — separates the autograd leaf (which enables chain-rule differentiation) from the bounded input the network sees, and defers componentwise derivative tests to Phase 19.
**Source:** 17-02-SUMMARY.md

---

### Decision 3: Per-Slot Tanh Normalization with Symbolic Statistics
Per-slot normalization uses `tanh((z - mu_z) / (sigma_z + 10^-8))` with symbolic mu/sigma placeholders; concrete dataset-wide statistic values are deferred to Phase 18.

**Rationale:** Accepted D-06 — establishes the normalization contract without locking values that depend on dataset preprocessing not yet finalized.
**Source:** 17-01-SUMMARY.md

---

### Decision 4: Ordered Raw Masses, Not Mass Fractions
Mass slots are ordered raw masses before `tanh` normalization (not mass fractions); v1.3-era mass-fraction encoding is FUT-01 handoff context only.

**Rationale:** Accepted D-07 (RESOLVED-WITH-INSTRUCTION, GAP-17-01) — raw masses provide a clearer physical contract and avoid ambiguity about reference body.
**Source:** 17-01-SUMMARY.md

---

### Decision 5: Inline Forward Reference Format (Phase 18)
Forward references use the format "Phase 18 (FRAME-01)" inline in both planning artifacts and framework spec text for preprocessing order.

**Rationale:** Accepted D-08 — provides traceable cross-phase links without requiring formal external-document pointers at this stage.
**Source:** 17-01-SUMMARY.md

---

### Decision 6: Inline Forward Reference Format (Phase 19)
Forward references use "Phase 19 (PHYS-02)" inline for componentwise AD chain-rule responsibility.

**Rationale:** Accepted D-09 — Phase 17 names the chain-rule factors and AD-derived velocity/acceleration contract but explicitly does not define the componentwise derivative tests; that boundary belongs to Phase 19.
**Source:** 17-01-SUMMARY.md and 17-02-SUMMARY.md

---

### Decision 7: Metadata-Only Status for Invariant Descriptors
Invariant-heavy descriptors (`Q`, `s_min`, `L_vec`, `L_norm`, `I_norm_raw`, `I1`, `I2`, `I3`, `tau_L`) and orientation summaries are metadata only under the Jacobi-state IC contract, not final network IC slots.

**Rationale:** Applied D-10 — these quantities serve curriculum staging, diagnostics, loss scaling, and reporting but do not enter the network input vector.
**Source:** 17-03-SUMMARY.md

---

### Decision 8: VER-04 Placement Boundary
VER-04 is named only in planning artifacts, not in framework spec edits.

**Rationale:** Accepted D-11 — separates verification planning from normative spec content.
**Source:** 17-01-SUMMARY.md (implied from tech tracking key-decisions)

---

### Decision 9: Three-Plan Decomposition (P01/P02/P03)
Phase 17 uses a locked P01 input / P02 output / P03 cleanup decomposition; P03 runs after P02.

**Rationale:** Accepted D-12 — separates concerns and allows regression checks to accumulate without re-running prior work.
**Source:** 17-03-PLAN.md

---

### Decision 10: AC-IO-04 as Phase-17-Local Cleanup Check
AC-IO-04 is approved as a Phase 17-local cleanup check, not a Phase 16 ledger row.

**Rationale:** Applied D-13 — keeps phase-local validation scoped and avoids polluting the Phase 16 acceptance-check namespace.
**Source:** 17-03-SUMMARY.md

---

### Decision 11: Five-Column Markdown Schema for Divergence Inventory
`17-CODE-DIVERGENCE.md` uses a five-column Markdown schema recording live code file:line, spec target, FUT-01 item, and FUT-01 priority.

**Rationale:** Applied D-14 — provides a structured, forward-pointing handoff artifact without editing live code.
**Source:** 17-03-SUMMARY.md and 17-03-PLAN.md

---

### Decision 12: No pinn/STATUS.md During Phase 17
`pinn/STATUS.md` is not created during Phase 17; deferred to Phase 21 handoff.

**Rationale:** Applied D-15 — Phase 17 records divergence for FUT-01 only, and does not claim ownership of live-code status.
**Source:** 17-03-SUMMARY.md

---

### Decision 13: Spec Heading Layout (Sub-Section, Not Rename)
Added `### Network Input Contract` as a sub-section at the start of `pinn_architecture.md` §5.2 rather than renaming §5.2 itself.

**Rationale:** Preserves cross-references that already point to §5.2 while letting the D-05 directive ("primary in §5.2") read naturally; section title still says "Output Layer and Kinematic Consistency via Automatic Differentiation."
**Source:** 17-01-SUMMARY.md

---

### Decision 14: Status Transitions with Same Commit SHA
Status transitions IN_PROGRESS → FIX_APPLIED → VERIFIED in a single commit share the same edit-commit SHA because the AC checks ran against the same edited state.

**Rationale:** Both transitions are logged with the same SHA; the transition log records both events in chronological order; no information is lost.
**Source:** 17-01-SUMMARY.md

---

## Lessons

### Lesson 1: Sidecar Grounding Confirms Explicit Grounding
Sidecar grounding confirmed the core B-06 output contract is explicitly grounded in source materials after D-02 resolution.

**Context:** P02 gap handling found no STOP gaps because the output contract direction was aligned; the only boundary noted was that Phase 19, not Phase 17, owns componentwise derivative-test details.
**Source:** 17-02-SUMMARY.md

---

### Lesson 2: Sidecar Agent Timeout Risk
Three read-only sidecar agents were dispatched for stale-wording, verification, and divergence grounding but did not return before local verification completed, so they were closed without using their output.

**Context:** P03 cleanup encountered race conditions between parallel sidecar validation and local verification; local verification finished first.
**Source:** 17-03-SUMMARY.md

---

### Lesson 3: AC-IO-03 Closure Requires Both Spec Edits and Regression Checks
AC-IO-03 closure requires both spec edits and regression checks for 17-01 input contracts before ledger status reaches VERIFIED.

**Context:** Output contract verification cannot proceed in isolation; it depends on input contract stability.
**Source:** 17-02-SUMMARY.md

---

### Lesson 4: Phase Boundary Ownership for AD Derivatives
Phase 17 names AD-derived velocities/accelerations and chain-rule responsibility but does not define the componentwise derivative test; that boundary belongs to Phase 19.

**Context:** Preserved Phase 19 ownership prevents premature specification of derivative-test details before physics residual contracts are finalized.
**Source:** 17-02-SUMMARY.md

---

## Patterns

### Pattern 1: Raw 9D Position Head with Hard COM Projection
Network emits raw 9D positions only, then applies a hard mass-weighted COM projection before any consumer (losses, residuals, diagnostics, metrics, evaluation).

**When to use:** When defining output contracts for physics-informed neural networks where conservation laws (momentum) must be enforced by construction rather than loss penalty.
**Source:** 17-02-SUMMARY.md

---

### Pattern 2: AD-Derived Velocities/Accelerations from Projected Positions
Velocities and accelerations are AD-derived from the projected positions; the componentwise derivative test is owned by the physics phase (Phase 19).

**When to use:** When the network output head is position-only and derivatives must be computed via automatic differentiation to ensure chain-rule consistency.
**Source:** 17-02-SUMMARY.md

---

### Pattern 3: Two-Commit Audit-SHA Pattern for Evidence Packets
Evidence-packet transition logs use a two-commit audit-SHA pattern: one commit for the edit, one for the audit SHA recording.

**When to use:** When tracking evidence-packet status transitions (PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED) in issue ledgers with full traceability.
**Source:** 17-01-SUMMARY.md and 17-02-SUMMARY.md

---

### Pattern 4: Non-Contested Evidence Packet Pattern
Evidence packets with EVID-05-only sections are marked "Not contested" when source direction is aligned after resolution decisions.

**When to use:** When evidence packets do not require adversarial testing because all candidate verdict sources agree on the resolution direction.
**Source:** 17-02-SUMMARY.md

---

### Pattern 5: Five-Column Divergence Inventory Schema
Code divergence inventory uses a five-column Markdown table: Surface | Live code (file:line) | Spec target (Phase 17 decision) | FUT-01 item | FUT-01 priority.

**When to use:** When creating forward-pointing handoff artifacts for downstream implementation phases (FUT-01) that need to know where live code diverges from finalized specs.
**Source:** 17-03-SUMMARY.md and 17-03-PLAN.md

---

### Pattern 6: Non-Binding FUT-01 Priority Hints
Row-level FUT-01 priority values in divergence inventories are non-binding handoff hints; FUT-01 planning may revise them after reading accumulated divergence files.

**When to use:** When providing implementation priority guidance in handoff artifacts without locking downstream planning decisions.
**Source:** 17-03-SUMMARY.md and 17-03-PLAN.md

---

### Pattern 7: Source Issues Metadata Preservation
Source Issues metadata remains untouched until Phase 21 VER-06; historical author-note wording can remain in normative files only when explicitly labeled non-normative and outside stale negative-grep terms.

**When to use:** When cleaning normative spec content but preserving historical context for future reconciliation.
**Source:** 17-03-SUMMARY.md

---

### Pattern 8: Code Divergence Rows Reference Live Code as Handoff Context Only
Code divergence rows list live code file:line references only as FUT-01 handoff context, not v1.4 evidence.

**When to use:** When documenting spec-vs-code divergences under governance rules that prohibit live code as grounding source.
**Source:** 17-03-SUMMARY.md

---

### Pattern 9: AC Closure Requires Regression Across Prior Contracts
Acceptance-check closure for a new contract (e.g., AC-IO-03) requires regression checks that prior contracts (e.g., 17-01 input contracts) remain green.

**When to use:** When phase plans have dependencies and later plans must not break earlier verified work.
**Source:** 17-02-SUMMARY.md

---

## Surprises

### Surprise 1: Sidecar Agents Did Not Return Before Local Verification
Three read-only sidecar agents were dispatched for parallel validation but did not return before local verification completed, so they were closed without using their output.

**Impact:** Operational inefficiency — sidecar dispatch added overhead without contributing to the final verification; future plans may need to synchronize sidecar completion or rely on local verification only.
**Source:** 17-03-SUMMARY.md

---

### Surprise 2: No New STOP Gaps in P02 or P03
No new STOP protocol gaps were encountered in P02 or P03; all decisions used by these plans were already LOCKED or RESOLVED-WITH-INSTRUCTION in `17-CONTEXT.md` / `17-GAPS.md`.

**Impact:** Positive — indicates that Phase 16 adjudication and P01 groundwork had already resolved all source-silent semantic/process decisions, allowing P02 and P03 to execute without governance halts.
**Source:** 17-02-SUMMARY.md and 17-03-SUMMARY.md
