---
phase: 20
phase_name: "Architecture and Normalization Cleanup"
project: "3-body-problem"
generated: "2026-06-09"
counts:
  decisions: 15
  lessons: 7
  patterns: 6
  surprises: 3
missing_artifacts: []
---

# Phase 20 Learnings: Architecture and Normalization Cleanup

## Decisions

### Fixed omega0 SIREN Contract with No In-Run Scheduler
SIREN initialization locked to `first_omega_0=30`, `hidden_omega_0=1`, standard SIREN init, with no epochwise or optimizer-step omega0 scheduler. This resolves the v1.3-era dynamic-scheduling ambiguity.

**Rationale:** The resolution doc and issue doc both support a fixed contract. Dynamic scheduling introduced instability and was not grounded in either source.
**Source:** 20-01-SUMMARY.md

---

### Hidden-Layer Init Bounds Divided by hidden_omega_0
The hidden-layer initialization formula divides by `hidden_omega_0` (not multiplies). Only the prose description was corrected — no formula changed.

**Rationale:** The existing code already divided; the spec prose had the description backwards.
**Source:** 20-01-SUMMARY.md

---

### Stage-Boundary Omega0 Retuning Preserved as Ablation Only
Omega0 retuning is permitted only as a stage-boundary ablation with fresh re-initialization, not as an in-run scheduler adjustment.

**Rationale:** Preserves the research option of tuning omega0 between curriculum stages without reintroducing the in-run scheduling ambiguity.
**Source:** 20-01-SUMMARY.md

---

### Separate Evidence Packets Sharing One Acceptance Check (B-01 + B-10 / AC-ARCH-01)
B-01 (hidden-layer init) and B-10 (dynamic scheduling) remain separate evidence records with separate verdicts, sharing only the AC-ARCH-01 closure audit.

**Rationale:** They address distinct issues but touch the same spec surface; separating them keeps evidence records atomic while the shared AC avoids redundant audits.
**Source:** 20-01-SUMMARY.md

---

### LayerNorm as Project-Specific Attribution
LayerNorm is explicitly documented as an author addition for this project, layered on top of the SQR-SkipResNet formulation. This resolves the attribution ambiguity flagged in Issue 01.

**Rationale:** Neither source (resolution doc nor issue doc) attributes LayerNorm to the original SQR-SkipResNet paper; it was a project-specific addition that needed explicit labelling.
**Source:** 20-02-SUMMARY.md

---

### elementwise_affine=False Default for LayerNorm
Learnable affine parameters are disabled by default. Enabling them or removing LayerNorm entirely are optional future ablations, not the Phase 20 contract.

**Rationale:** Both cited sources agree on `elementwise_affine=False` as the default. The affine case and removal are left open as future experiments.
**Source:** 20-02-SUMMARY.md

---

### Raw I_3 ∈ [0, 1/3] (Not [-1, 1])
Triangle geometry bounds the ratio-form I_3 quantity to [0, 1/3]. The [-1, 1] range in the pre-Phase-20 spec was the mapped/input range misattributed as the raw range.

**Rationale:** First-principles triangle geometry: the ratio-form I_3 (derived from side lengths) cannot exceed 1/3 for any triangle.
**Source:** 20-03-SUMMARY.md

---

### Staging-Metadata Map I_3^in = 6·I_3 − 1
The linear map from [0, 1/3] to [-1, 1] preserves the equilateral/collinear ordering while keeping the mapped value in the standard network-input interval.

**Rationale:** Maps the raw physics range onto the standard [-1, 1] interval used by SIREN inputs, preserving the physical ordering (equilateral → 1, collinear → -1).
**Source:** 20-03-SUMMARY.md

---

### I_3 is Metadata-Only, Not a Network IC Slot
I_3 is not a network IC slot under the Phase 17 input contract (GAP-17-05). The staging map exists for metadata/diagnostic use, not as a live network input surface.

**Rationale:** Phase 17's input contract does not include I_3 among the final network IC slots. The map serves diagnostic/staging purposes only.
**Source:** 20-03-SUMMARY.md

---

### Separate M9/M10 Packets Sharing AC-ARCH-05
Energy (M9) and mass (M10) normalization remain separate evidence records with separate verdicts, sharing only the AC-ARCH-05 closure audit.

**Rationale:** Energy and mass normalization have distinct physics grounding and distinct dataset-support arguments, even though they share the same acceptance check pattern.
**Source:** 20-04-SUMMARY.md

---

### Dataset-Occupancy Framing (Not "Realized Support")
Spec prose uses plain descriptive wording ("dataset-occupied range", "acceptable for SIREN", "not a correctness failure") instead of the planning shorthand "realized support."

**Rationale:** The planning term "realized support" is internal jargon; the spec should use language that is self-contained and readable by future implementers.
**Source:** 20-04-SUMMARY.md

---

### No Numeric v1.4 Mass Range Stated
The exact m_norm range under the v1.4 tanh formula depends on dataset-wide μ and σ per slot, so no specific numeric range is stated in the spec.

**Rationale:** The mass normalization formula `tanh((m_i - mu)/(sigma + 1e-8))` produces a range that varies with dataset statistics. Stating a fixed number would be incorrect or misleading.
**Source:** 20-04-SUMMARY.md

---

### Energy Occupancy Grounded in Physics: E_norm ∈ [-1, 0) for Bound Systems
Bound gravitational systems have E < 0, which maps through tanh to [-1, 0). The positive tanh range is unused; this is acceptable for SIREN.

**Rationale:** This is a direct consequence of the physics (bound systems have negative total energy) and dataset selection (prescreening for bound systems), not a normalizer design choice.
**Source:** 20-04-SUMMARY.md

---

### Locked I_norm Naming Convention: I_norm_raw / I_norm_in / I_norm (Metadata Only)
I_norm_raw for the raw physics/metadata descriptor; I_norm_in = tanh(I_norm_raw) for the conditional widened-input ablation convention; I_norm (bare) is metadata only and not a live framework-spec input surface.

**Rationale:** Both `ctl_pinn_resolution.md` and `01-architecture-and-physics-foundations.md` explicitly agree on the raw-vs-bounded distinction. The naming convention eliminates ambiguity across all spec surfaces.
**Source:** 20-05-SUMMARY.md

---

### Wave 2 Dependency Ordering to Avoid Concurrent-Edit Conflicts
20-02 depends on 20-01 (both edit pinn_architecture.md); 20-04 and 20-05 depend on 20-03 (all edit ctl_instruction.md). Wave-based ordering prevents concurrent-edit conflicts.

**Rationale:** Multiple plans editing the same spec file must be sequenced so each plan's read-only audit sees the final surfaces from prior plans.
**Source:** 20-02-SUMMARY.md, 20-05-PLAN.md

---

## Lessons

### EVID-05 Adjudication Can Resolve Without Escalation When Sources Actually Agree
The M5/I_3 adjudication was flagged `Sources Disagree: YES — EVID-05 required`, but the full EVID-05 protocol revealed both sources use the same ratio-form I_3 quantity, so the first-principles triangle-geometry lemma applied directly and grounded an `accept-resolution` verdict without needing `defer-with-blocker`.

**Context:** ARCH-03 (20-03-PLAN) was the only non-autonomous plan in Phase 20 due to the EVID-05 flag. The STOP protocol was followed, but the outcome was a clean resolution.
**Source:** 20-03-SUMMARY.md

---

### Pre-Phase-20 Spec Misattributed Mapped Range as Raw Range
The I_3 range was stated as [-1, 1] in the pre-Phase-20 spec, but this was the mapped/input range, not the raw physics range. The raw range [0, 1/3] comes from triangle geometry.

**Context:** This was discovered during the EVID-05 first-principles physics check in ARCH-03.
**Source:** 20-03-SUMMARY.md

---

### LayerNorm Attribution Was Ambiguous Between Sources
Neither the resolution doc nor the issue doc attributed LayerNorm to the original SQR-SkipResNet paper. The attribution ambiguity was a genuine issue that needed explicit documentation as a project-specific addition.

**Context:** ARCH-02 (20-02-PLAN) was created specifically to resolve this attribution question.
**Source:** 20-02-SUMMARY.md

---

### Plan Enumerations of Spec Surfaces Are Often Incomplete — rg Audit Finds More
The 20-05 plan initially enumerated 4 I_norm surfaces; the post-review remediation found 6 LaTeX surfaces plus 1 error message string (7 additional surfaces) that needed alignment.

**Context:** This is a recurring pattern — initial surface enumerations in plans tend to undercount because they miss LaTeX-rendered forms and error strings.
**Source:** 20-05-SUMMARY.md

---

### v1.3 Live Code Had a Dynamic omega0 Scheduler That the Spec Must Now Explicitly Prohibit
The v1.3 codebase used an epochwise/optimizer-step omega0 scheduler. The Phase 20 spec must explicitly state this is NOT part of the contract, and any historical discussion must be labelled non-normative.

**Context:** This was a key motivation for ARCH-01 — removing the ambiguity between what v1.3 did and what the spec now requires.
**Source:** 20-01-PLAN.md

---

### Dataset Documentation Serves as Evidence for Normalization Support Ranges
The M9/M10 evidence packets cite dataset documentation (not just the resolution/issue docs) as evidence for the realized regimes. Dataset occupancy is a valid evidence type for normalization support claims.

**Context:** ARCH-05 (20-04-PLAN) explicitly includes dataset documentation in its evidence chain.
**Source:** 20-04-PLAN.md

---

### Phase 20 Produced Seven Evidence Packets Across Five Plans
The phase created B-01, B-10, M5, M8, M9, M10, and D-02-NORM — all VERIFIED in the Phase 16 ledger. The "separate packets, shared AC" pattern scales: five plans produced seven evidence records while only requiring five acceptance checks.

**Context:** This demonstrates the evidence-packet pattern's scalability for complex multi-issue cleanup phases.
**Source:** 20-VERIFICATION.md

---

## Patterns

### Evidence-First Spec Cleanup with Separate Packets Sharing One AC
Create/fill evidence packets first (citing sources side by side, recording verdicts), then edit only verdict-supported spec surfaces, then prove closure with a combined audit. Multiple evidence packets can share a single acceptance check.

**When to use:** When a phase addresses multiple related spec issues that touch overlapping files. Each issue gets its own atomic evidence record, but the closure audit is consolidated.
**Source:** 20-01-SUMMARY.md, 20-04-SUMMARY.md

---

### Negative Scheduler Audit
After locking a fixed contract (e.g., "no omega0 scheduler"), run a negative audit (`rg` for scheduler patterns) to confirm no active/normative scheduler guidance remains in the spec. Historical discussion is allowed only if explicitly labelled non-normative.

**When to use:** When removing a previously-existing dynamic behavior from a spec. Verify the removal by searching for remnants.
**Source:** 20-01-PLAN.md

---

### Wave-Based Plan Dependency Ordering for Same-File Edits
When multiple plans edit the same spec file, order them in waves so each plan's read-only audit sees the final surfaces from prior plans. 20-01 → 20-02 (both edit pinn_architecture.md); 20-03 → 20-04 → 20-05 (all edit ctl_instruction.md).

**When to use:** When a phase has multiple plans that edit the same files. Prevents stale-surface audits and merge conflicts.
**Source:** 20-05-PLAN.md, 20-02-SUMMARY.md

---

### Dataset-Occupancy Framing for Normalization Support Ranges
Frame normalization ranges as "dataset-occupied support" using plain descriptive wording, not as universal physics bounds or normalizer defects. Asymmetric or mostly-negative ranges are expected consequences of physics and dataset selection, not bugs.

**When to use:** When a normalization's effective range is narrower than the formula's mathematical range, and the asymmetry has a physical or dataset-selection explanation.
**Source:** 20-04-SUMMARY.md, 20-04-PLAN.md

---

### Verdict-Gated Spec Edits
No spec wording is touched until the evidence packet records a verdict. The plan instructs the executor to create the packet, fill it with source citations, record exactly one enum verdict, and only then edit the spec — and only as the verdict supports.

**When to use:** Any spec cleanup governed by the Phase 16 evidence ledger. Prevents premature edits and ensures every spec change is source-grounded.
**Source:** 20-05-PLAN.md, 20-03-PLAN.md

---

### Strengthened Bare-Name Audit for Naming Conventions
When establishing a naming convention (e.g., I_norm_raw vs I_norm_in vs bare I_norm), the closure audit must check not only the ASCII form but also LaTeX-rendered forms (I_{\text{norm}}, I_{\mathrm{norm}}) and error message strings.

**When to use:** After establishing any naming convention that has both code and LaTeX representations. Search for all rendering forms, not just the ASCII one.
**Source:** 20-VERIFICATION.md

---

## Surprises

### ARCH-03 EVID-05 Flag Was Resolvable Without User Escalation
The M5/I_3 issue was flagged `Sources Disagree: YES — EVID-05 required` in the Phase 16 ledger, making 20-03 the only non-autonomous plan. However, the full EVID-05 protocol revealed the sources actually agree — both use the same ratio-form I_3 quantity. The adjudication completed with an `accept-resolution` verdict without needing to surface to the user.

**Impact:** The non-autonomous flag was a precaution that turned out to be unnecessary. The STOP protocol was followed correctly but did not need to halt work.
**Source:** 20-03-SUMMARY.md

---

### Plan 20-05 Found 7 Additional Surfaces Beyond Initial Enumeration
The plan initially listed 4 I_norm surfaces to edit. Post-review remediation discovered 6 LaTeX surfaces (lines 667, 671, 722, 728, 917, 1433) plus 1 error message string (line 753) that also needed alignment — 7 additional surfaces beyond the original 4.

**Impact:** All were within the same spec sections and within scope, so no plan expansion was needed. But it demonstrates that initial surface enumerations systematically undercount LaTeX-rendered and string-literal forms.
**Source:** 20-05-SUMMARY.md

---

### All Five Phase 20 Requirements Closed with All Seven Findings VERIFIED
The phase completed with all automated checks passing: all five plan summaries exist, the strict validation suite passes, zero `pending-commit` markers remain, no `pinn/` diff exists, the CODE-DIVERGENCE handoff is present, and all seven evidence findings are VERIFIED.

**Impact:** Phase 20 was fully self-contained and did not require any GAP entries or user escalations. All five ARCH requirements (ARCH-01 through ARCH-05) closed cleanly.
**Source:** 20-VERIFICATION.md
