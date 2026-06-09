---
phase: 18
phase_name: "Frame and Gauge Contracts"
project: "3-body-problem"
generated: "2026-06-09"
counts:
  decisions: 8
  lessons: 5
  patterns: 6
  surprises: 2
missing_artifacts: []
---

# Phase 18 Learnings: Frame and Gauge Contracts

## Decisions

### D-03: Consolidate Step 2 and Step 2.5 into One Unified Preprocessing Pipeline
The separate "Step 2: Preprocessing: Scaling to Dimensionless Units" and "Step 2.5: Verify Center-of-Mass (COM) Frame" were merged into a single "Step 2: Unified Preprocessing Pipeline" with substeps: 2.1 parser contract/mass-invariance check, 2.2 COM recenter/zero-momentum boost, 2.3 canonical ordering, 2.4 canonical rotation gauge, 2.5 global scaling, 2.6 assertions and stored metadata.

**Rationale:** A single ordered pipeline eliminates ambiguity about preprocessing sequence and ensures all frame/gauge operations are applied in a deterministic, auditable order.
**Source:** 18-01-PLAN.md

---

### D-04: Relocate Canonical Ordering from Step 4 to Step 2.3
Canonical ordering was moved from its original location in Step 4 to Step 2.3 within the unified preprocessing pipeline, using raw mass, COM-corrected position norm, COM-corrected velocity norm, then original file order as tie-break.

**Rationale:** Ordering must happen before scaling and gauge operations so that downstream steps receive bodies in a deterministic sequence; the original-file-order tie-break preserves reproducibility when all physical keys match.
**Source:** 18-01-PLAN.md

---

### D-05/D-14: Rotation Gauge Fixes Only Initial Orientation with eta_gauge = 1e-8
The canonical rotation gauge fixes only the initial orientation of the system, preserves full 3D Cartesian trajectory semantics (output remains 9D), and uses eta_gauge = 1e-8 as a dimensionless degeneracy threshold with collinear fallback and deterministic sign handling.

**Rationale:** The gauge must not reduce the physical dimensionality of the problem — Jacobi velocities remain fully 3D — while still providing a deterministic initial-frame convention; the 1e-8 dimensionless threshold guards against degenerate collinear configurations.
**Source:** 18-01-PLAN.md, 18-01-SUMMARY.md

---

### D-02: M3 Verdict Is accept-resolution; COM Transform First, Then Scale
The M3 finding (scaling order and COM transform order) was resolved with verdict `accept-resolution`, encoding the rule that the COM transform must be applied FIRST, then scaling.

**Rationale:** The order of COM recentering vs. scaling is physically consequential — scaling before COM recentering would produce different dimensionless coordinates. The resolution doc was explicit on this ordering.
**Source:** 18-01-PLAN.md

---

### D-09/D-10: FRAME-03 Sampling Frame Notes Grounded in simulation_data/
FRAME-03 documents that hierarchical generation perturbs after COM/P enforcement, while standard quasi-random generation constructs equal-mass COM/P exactly by construction. `simulation_data/` scripts (generate_ics.py, ic_generation_utils.py) are the authoritative source for these claims.

**Rationale:** The sampling spec must reflect what the actual IC generation code does, not stale prose. Reading the generation code before editing the spec prevents documentation drift.
**Source:** 18-02-PLAN.md, 18-02-SUMMARY.md

---

### D-11: Confine Phase 18 Edits Away from Sobol Coordinate-Allocation Formula
Phase 18 deliberately does not touch the Sobol velocity-coordinate allocation paragraph (`u_4, u_5, u_6`), preserving it for Phase 20.5 which owns that fix.

**Rationale:** The Sobol coordinate allocation is a known bug scoped to Phase 20.5; fixing it in Phase 18 would violate scope boundaries and create cross-phase coordination risk.
**Source:** 18-02-PLAN.md

---

### D-13: CODE-DIVERGENCE Inventory Follows Phase 17 Five-Column FUT-01 Hand-Off Schema
The `18-CODE-DIVERGENCE.md` file mirrors the Phase 17 schema, recording live `pinn/` implementation divergences only as FUT-01 handoff context — never as v1.4 evidence.

**Rationale:** v1.4 constructs framework specs; FUT-01 rewrites code from those specs. Live-code references are permitted only in forward-pointing hand-off documents per the governance directive.
**Source:** 18-03-PLAN.md, 18-03-SUMMARY.md

---

### D-08: Reserve AC-FRAME-01..04 Names; Phase 21 Owns Numeric Pass Criteria
Phase 18 reserves the acceptance check names AC-FRAME-01 through AC-FRAME-04 but defers definition of numeric pass criteria to Phase 21.

**Rationale:** Phase 18 establishes structural/spec-level contracts; numeric thresholds for automated acceptance testing are owned by the acceptance-checks phase to avoid premature commitment.
**Source:** 18-01-PLAN.md, 18-03-SUMMARY.md

---

## Lessons

### Evidence Packets Must Precede Spec Edits
Phase 18 established that B-05 and M3 evidence packets are opened and their verdicts recorded BEFORE any framework-spec modifications are made. This ensures the evidentiary basis is locked before changes are applied.

**Context:** Task 1 (write evidence packets) was sequenced before Task 2 (rewrite spec). This ordering prevents the spec from being changed on the basis of evidence that was never formally recorded.
**Source:** 18-01-PLAN.md, 18-01-SUMMARY.md

---

### B-05 Requires Multi-Plan Lifecycle; Cannot Close in a Single Plan
B-05 could not be fully VERIFIED in plan 18-01 because FRAME-03 (sampling reconciliation) had not yet landed. It transitioned: PENDING → IN_PROGRESS (P01) → FIX_APPLIED (P02) → VERIFIED (P03). This staged lifecycle was intentional.

**Context:** The sampling-frame reconciliation (FRAME-03) was a prerequisite for B-05 closure, requiring a separate plan (18-02) to edit `sampling_method.md` before the full structural suite could pass.
**Source:** 18-01-SUMMARY.md, 18-02-SUMMARY.md, 18-03-SUMMARY.md

---

### M4 Preservation Requires Multiline Regex Because the Protected Sentence Is Line-Wrapped
The Step 4 Mathematical Guarantees sentence containing "13 constraints for an 8-dimensional reduced phase space" is line-wrapped in the markdown, so a single-line regex cannot reliably verify its presence. A multiline `rg -nU` check was required.

**Context:** GAP-18-05 was surfaced during P01 Task 2 when the original single-line M4-preservation regex failed. The user authorized the multiline approach.
**Source:** 18-01-SUMMARY.md

---

### Live pinn/ Code Is Excluded from v1.4 Evidence but Tracked for FUT-01 Handoff
Phase 18 reinforced that `pinn/` live code must not be cited as v1.4 evidence, but divergences between spec and live code are recorded in `18-CODE-DIVERGENCE.md` as forward-pointing handoff for the FUT-01 rewrite.

**Context:** This is a governance directive (2026-05-19) that Phase 18 operationalized through the CODE-DIVERGENCE inventory pattern established in Phase 17.
**Source:** 18-01-PLAN.md, 18-03-PLAN.md, 18-03-SUMMARY.md

---

### Post-Review Correction Applied to Quasi-Random Momentum-Conservation Prose
After initial FRAME-03 edits, a post-review correction aligned the adjacent quasi-random momentum-conservation sentence with authoritative generator behavior (`v1 = v3 = -v2/2`) without touching the Sobol coordinate-allocation target.

**Context:** This correction was documented in P02's tech tracking as an application of D-10 — the spec must match what the code actually does.
**Source:** 18-02-SUMMARY.md

---

## Patterns

### Split-Frame Contract: Input-Side Assertions in ctl_instruction.md, Output-Side Projection in pinn_architecture.md
FRAME-02 is implemented as a split contract: preprocessed-sample COM/momentum assertions live in `ctl_instruction.md` (input side), while the hard mass-weighted COM projection for model outputs lives in `pinn_architecture.md` (output side). The two are cross-referenced.

**When to use:** When a single invariant spans both preprocessing and model output, split the contract at the natural boundary (preprocessing vs. architecture) and cross-reference rather than duplicating.
**Source:** 18-01-SUMMARY.md, 18-03-SUMMARY.md

---

### Evidence Lifecycle Gating: Partial Closure Allowed When Dependencies Are Sequenced
M3 was closed to VERIFIED under a Phase 18-local structural subset of AC-FRAME-01 while B-05 waited for FRAME-03. This "partial closure with explicit dependency tracking" pattern allows progress without premature full closure.

**When to use:** When an evidence packet depends on multiple FRAME requirements that land in different plans, allow partial structural closure for the requirements that have landed, with explicit documentation of what remains.
**Source:** 18-01-SUMMARY.md, 18-03-SUMMARY.md

---

### Negative Acceptance Checks Protect Untouched Content
Phase 18 used negative acceptance checks (e.g., verifying "13 constraints for an 8-dimensional reduced phase space" still appears after edits; verifying no `pinn/` diff exists) to ensure that content NOT targeted by the plan remained untouched.

**When to use:** Whenever a plan modifies a file that also contains content owned by other phases or future work, add explicit negative checks that verify the untouched content survives.
**Source:** 18-01-PLAN.md, 18-VERIFICATION.md

---

### CODE-DIVERGENCE.md as a Reusable FUT-01 Handoff Schema
Phase 18 adopted the Phase 17 five-column CODE-DIVERGENCE schema (recording file:line divergences between spec and live code) as a standard handoff artifact. Each phase that touches spec content adjacent to live code produces its own divergence inventory.

**When to use:** At the end of any spec-writing phase that has awareness of live-code implementations, produce a CODE-DIVERGENCE.md to hand off known gaps to the FUT-01 rewrite without polluting the current phase's evidence.
**Source:** 18-03-PLAN.md, 18-03-SUMMARY.md

---

### Structural Pre-Closure Checks Before Lifecycle Mutation
Before changing an evidence packet's status (e.g., B-05 from FIX_APPLIED to VERIFIED), run the structural pre-closure checks first, then run the exact strict suite after closure to confirm nothing regressed.

**When to use:** When evidence lifecycle transitions depend on structural verification, run checks both before and after the mutation to catch ordering-dependent failures.
**Source:** 18-03-SUMMARY.md

---

### Scope-Carveout with Explicit Boundary: simulation_data/ Authoritative Only for FRAME-03
The `simulation_data/` directory was permitted as a grounding source for `sampling_method.md` edits (FRAME-03 only), with an explicit carve-out that this authority does not generalize beyond that scope.

**When to use:** When a spec edit requires grounding in implementation code, grant a narrow scope-limited carve-out rather than a blanket exception to the live-code exclusion rule.
**Source:** 18-02-PLAN.md, 18-02-SUMMARY.md

---

## Surprises

### GAP-18-05: Single-Line Regex Cannot Match Line-Wrapped M4 Sentence
The original M4-preservation check used a single-line regex that failed because the protected sentence "13 constraints for an 8-dimensional reduced phase space" was line-wrapped across multiple lines in the markdown source. This was not anticipated during planning.

**Impact:** Required user authorization for a multiline `rg -nU` check approach. The gap was surfaced, resolved, and documented without delaying the plan, but it revealed that protected-content checks must account for markdown line-wrapping.
**Source:** 18-01-SUMMARY.md

---

### Post-Review Correction Needed for Quasi-Random Momentum-Conservation Sentence
After the initial FRAME-03 sampling edits were applied, a post-review step discovered that the adjacent quasi-random momentum-conservation prose did not match the authoritative generator behavior (`v1 = v3 = -v2/2`). This required a correction that was not part of the original plan.

**Impact:** The correction was applied within P02 scope without deviating from the plan's intent, but it revealed that spec edits adjacent to code-grounded claims require their own code-verification pass — not just the targeted edit area.
**Source:** 18-02-SUMMARY.md
