# Phase 19 Plan Review: Physics and Loss Contracts

**Reviewed:** 2026-05-22
**Documents:** 19-CONTEXT.md, 19-DISCUSSION-LOG.md, 19-01-PLAN.md, 19-02-PLAN.md, 19-03-PLAN.md, 19-04-PLAN.md
**Method:** Multi-persona adversarial review (coherence, feasibility, adversarial physics/math, product-lens, scope-guardian)

---

## Executive Summary

The Phase 19 plans are **well-structured and mathematically sound at the physics level**. The 19 LOCKED decisions in 19-CONTEXT.md are properly grounded in the resolution doc, the dimensional analysis is correct, the Plummer softening argument is rigorous, and the AD contract is precise. The 4-plan decomposition (P01 ctl_instruction, P02 pinn_architecture formulas, P03 prose cleanup, P04 closure) is reasonable for review safety.

However, the review identified **2 BLOCKING issues**, **5 MAJOR issues**, and **7 MINOR issues / improvements**. The blocking issues concern missing gap-register infrastructure and a cross-plan coordination deadlock. The major issues include under-specified spec content, fragile verification commands, and a potential mathematical edge case in the angular momentum loss.

---

## Critical / BLOCKING Findings

### B1: No 19-GAPS.md gap register exists; plans don't create one

**Severity:** BLOCKING
**Persona:** feasibility-reviewer, coherence-reviewer
**Evidence:** 19-CONTEXT.md line 458 states: "Phase 19 gap register. Empty at context-gathering time; created by P01 if any gap surfaces during planning. New gaps from plan-phase or execute-phase appended per STOP protocol." But 19-GAPS.md does not exist, and no plan task creates it. P01 Task 1 writes evidence packets; Task 2 edits specs; Task 3 annotates the Issue Doc. None of them create the gap register file.

**Why this matters:** The CRITICAL GOVERNANCE STOP protocol (CLAUDE.md) requires that when a semantic, process-artifact, or cross-phase gap is encountered, the agent MUST record it in 19-GAPS.md and update the milestone-wide v1.4-GAPS.md index. If the gap register file doesn't exist, the executor has nowhere to log gaps and may either skip the STOP protocol or log to the wrong location.

**Suggested fix:** Add a Task 0 to P01 (or a pre-task) that creates `19-GAPS.md` with the standard gap-register header and confirms it's writable. The file should be created before any spec edits begin. Alternatively, add a note that the executor creates it on first gap encounter, with the exact path and format specified.

### B2: Cross-plan total-loss mismatch has no repair path for ctl_instruction.md

**Severity:** BLOCKING
**Persona:** coherence-reviewer, feasibility-reviewer
**Evidence:** P01 Task 2 writes the total-loss formula into `ctl_instruction.md`. P02 Task 2 writes it into `pinn_architecture.md`. P03 Task 2 (lines 176-183) validates they match and says: "If either file has a different formula, fix `pinn_architecture.md` to match (ctl_instruction.md is already committed in 19-01)." But if the mismatch is in `ctl_instruction.md` (P01 got it wrong), P03 has no authority to fix it — P01 already committed and closed. The plan explicitly says "do NOT edit ctl_instruction.md."

**Why this matters:** If P01's executor writes a subtly wrong total-loss formula (e.g., omits λ_IC, swaps term order, or uses wrong subscript), P03 will detect the mismatch but can only fix `pinn_architecture.md` to match the WRONG `ctl_instruction.md` text. The two files would be consistent but consistently wrong. The only repair would be an out-of-band edit to a committed file.

**Suggested fix:** Either (a) make P01 and P02 share a common include/literal for the total-loss formula (a small shared snippet both reference), or (b) give P03 explicit authority to amend ctl_instruction.md if the total-loss formula is wrong, with a new commit, or (c) add a pre-coordination step where both executors confirm the formula text before committing.

---

## MAJOR Findings

### M1: Causal-weight clipping threshold is mentioned but never specified

**Severity:** MAJOR
**Persona:** adversarial-document-reviewer
**Evidence:** 19-CONTEXT.md D-10 (line 211): "with clipping of the exponent to avoid underflow." But the spec edit text in P02 Task 2 (line 354) only says `w_n = exp(-η_c · Σ_{m<n} stopgrad(R̄_m))` — no clipping threshold, no clip range, no implementation guidance. The verification command in P02 Task 2 (line 453) checks for `w_n.*exp.*eta_c.*stopgrad` which passes without clipping. The resolution doc §8.4 may specify the clipping, but the plan doesn't transcribe it.

**Why this matters:** Without a specified clipping threshold, FUT-01 implementers will either guess, use a hardcoded value from the resolution doc that may not be in the spec, or omit clipping entirely. If cumulative residual accumulates large values for late time steps in deep curricula, unclipped exponent underflow could zero out physics loss for late collocation points, silently disabling the physics constraint.

**Suggested fix:** Add the clipping value to the spec edit text in P02 Task 2 and to the verification command. If the resolution doc §8.4 specifies a value (likely `clip(exp_argument, min=-20, max=20)` or similar), transcribe it. If it doesn't, surface as a gap in 19-GAPS.md.

### M2: Verification commands use fragile regex patterns that may silently pass on wrong content

**Severity:** MAJOR
**Persona:** feasibility-reviewer
**Evidence:** Multiple verification commands use patterns like:
- `rg -n "D.*G.*T.*2.*1/3"` — matches D=(G*T^2)^(1/3) but also D = G*T2/3 or any text with D, G, T, 2 in sequence
- `rg -n "L_total.*L_data.*L_IC.*L_phys.*L_E.*L_L"` — matches any line with these tokens in order, even if the formula is different
- `rg -n "lambda_p.*L_phys.*mu_p.*L_phys"` — for NEGATIVE check (should return 0 matches). If the text says "we used to have λ_p L_phys and μ_p L_phys²" in a history section, this would false-positive fail
- 19-04 Task 2 verification (line 343): complex alternation with `\|` escaping that may not work in all bash versions

**Why this matters:** Verification commands are the primary quality gate. If regexes are too loose, wrong spec text passes verification. If too tight, correct text fails. If negative checks have false positives, the plan incorrectly fails verification.

**Suggested fix:** Tighten critical regexes to include exact formula fragments (e.g., `rg -F "D = (G·T²)^(1/3)"` or `rg -F "D³ = G·T²"`). For negative checks, verify the matching lines aren't in a history/context section. Add a pre-verification step that confirms `rg` is available and the patterns match expected content.

### M3: L_L angular momentum loss has a potential division-by-near-zero edge case

**Severity:** MAJOR
**Persona:** adversarial-document-reviewer
**Evidence:** P02 Task 2 (lines 333-342) defines L_L with `L_scale = ||L_0'|| + ε_L` where ε_L = 10⁻⁸. For initial conditions with exactly zero angular momentum (e.g., collinear free-fall, or the collinear periodic figure-8 orbit), ||L_0'|| = 0 exactly. Then L_scale = 10⁻⁸, and the relative drift term (L_θ,α' / 10⁻⁸) amplifies small absolute errors by 10⁸. While Huber(δ=1.0) caps the per-component contribution at linear growth, the scaling means the loss is dominated by angular momentum noise rather than being proportional to physical drift.

**Why this matters:** For zero-angular-momentum ICs (which are common test cases), L_L becomes a large-magnitude noisy term that could destabilize training. The Huber cap limits damage but doesn't fix the root scaling issue.

**Suggested fix:** Consider a hybrid scale: `L_scale = max(||L_0'||, L_min) + ε_L` where `L_min` is a physically meaningful minimum angular momentum scale (e.g., the typical |L| of a random 3-body IC). Or document this edge case explicitly in the spec with a note that zero-L ICs should use an alternative normalization. If the resolution doc §8.6 already addresses this, transcribe the handling.

### M4: L_IC uses MSE while L_data uses Huber — loss-type inconsistency not justified

**Severity:** MAJOR
**Persona:** adversarial-document-reviewer, product-lens-reviewer
**Evidence:** P02 Task 2 defines L_IC as `MSE(r_θ'(0), r_0')` and `MSE(v_θ'(0), v_0')` (line 325), while L_data uses Huber with δ_r = 1 (line 352). This means the IC anchor loss has quadratic penalty for large errors while the data loss has linear penalty. For early training when IC predictions may be far from truth, the MSE IC loss could dominate and cause training instability — exactly the problem Huber is designed to solve.

**Why this matters:** Mixed loss types create unpredictable relative scaling during training. If the IC constraint is meant to be a hard constraint (exact match at u=0), MSE enforces this more strongly than Huber. But if it's a soft constraint like the others, consistency argues for Huber. The resolution doc §8.3 may justify this, but the plan doesn't capture the justification.

**Suggested fix:** Either (a) add a brief justification in the spec for why MSE is appropriate for IC anchor (e.g., "IC values are known exactly from data preprocessing, so large errors indicate a training fault, not an outlier"), or (b) consider making L_IC use Huber with its own δ_IC parameter, or (c) document this as a deliberate design choice in the evidence packet.

### M5: The AD contract Python listing is incomplete for batch-mode operation

**Severity:** MAJOR
**Persona:** feasibility-reviewer
**Evidence:** P02 Task 2 lines 416-434 show a Python listing with `model_single(u_scalar, ic13)` — single-sample only. The spec doesn't address how `jacrev` + `vmap` composes for batch-mode operation (batch_size × N_collocation inputs). The listing says `J = jacrev(model_single)(u, ic13)` with shape `(9, 1)`, but actual training requires shape `(batch, 9, 1+13)` or similar.

**Why this matters:** The jump from single-sample to batched operation is non-trivial for `torch.func.jacrev` + `vmap`. FUT-01 implementers reading this spec might implement the single-sample version and only discover the batching issue during integration testing. The anti-pattern warning about `r.sum()` is correct but doesn't address batching.

**Suggested fix:** Add a note that the listing is single-sample for clarity, and that batch-mode composition follows standard `vmap` semantics (vmap over batch dimension of both u and ic13). No need for full batch code, but the spec should acknowledge the gap.

---

## MINOR Findings / Improvements

### m1: Stale line-number references in read_first sections

**Persona:** feasibility-reviewer
**Evidence:** Plans reference specific line numbers from framework specs (e.g., `ctl_instruction.md:914-915`, `pinn_architecture.md:416`, `pinn_architecture.md:549`). Phase 17 and Phase 18 edited these same files, and their line numbers may have shifted. P01 acknowledges this ("Cited line numbers are anchors, not the full edit set") but some task `read_first` sections hardcode line ranges without the caveat.

**Suggested fix:** Add a pre-task that `rg`s for the anchor text to confirm current line positions before attempting edits. Or replace line numbers with search patterns in all `read_first` sections.

### m2: No explicit distinction between "Hamiltonian" (analytic function) vs "Hamiltonian" (HNN architecture) in spec prose

**Persona:** coherence-reviewer
**Evidence:** D-09 says "Keep 'Hamiltonian' where it means the analytic energy function H_ε." But the spec reader may not understand the distinction without explicit framing. The plan relies on surrounding prose to clarify, but the boundary between "acceptable Hamiltonian mention" and "removed HNN claim" is fuzzy.

**Suggested fix:** Add a one-sentence framing note in the spec: "Throughout this document, 'Hamiltonian' refers to the analytic energy function H_ε = T + V_ε, not to a neural-network-parameterized Hamiltonian or Hamiltonian Neural Network architecture."

### m3: The synthetic trajectory test uses 1-body/3-component but system is 3-body/9-component

**Persona:** adversarial-document-reviewer
**Evidence:** The PHYS-02 test trajectory `r'(u) = [sin(2πu), cos(2πu), u²]` is for one body with three position components. The actual system outputs 9 components (3 bodies × 3D). The test verifies per-component AD works but doesn't verify that the 9-output case has no cross-component leakage.

**Why this matters (minor):** The `torch.autograd.grad(r.sum(), u)` anti-pattern is specifically about cross-component summation. A 1-body test can't demonstrate the failure mode (summing 3 components vs summing 9). This is fine for a spec-level test (Phase 21 VER-04 does numeric validation) but worth noting.

### m4: ε_L = 10⁻⁸ magnitude justification is thin

**Persona:** adversarial-document-reviewer
**Evidence:** The plan says ε_L = 10⁻⁸ is "a numerical-stability scale distinct from softening ε_train / ε_inv" (P02 Task 2 line 340). The resolution doc §8.6 presumably justifies this value, but the plan doesn't capture the reasoning. Is 10⁻⁸ chosen because typical angular momentum values in dimensionless units are O(1)? Because float32 epsilon is ~10⁻⁷? Because it's small enough not to affect the loss scale but large enough to prevent division by zero?

**Suggested fix:** Add a one-line justification: "ε_L = 10⁻⁸ provides ~8 decimal orders of headroom below O(1) dimensionless angular momentum while preventing division by zero."

### m5: P03 Task 2 can't fix cross-reference gaps found in ctl_instruction.md

**Persona:** coherence-reviewer
**Evidence:** P03 Task 2 line 195: "if any cross-reference is wrong or missing, note it but do NOT edit ctl_instruction.md (it was committed in 19-01). Instead, log any cross-reference gap found and continue." This means a ctl_instruction.md cross-reference error found late (Wave 2) has no repair path within Phase 19. The gap gets logged but not fixed.

**Suggested fix:** Either (a) run cross-reference validation during P01 execution (before commit), or (b) give P03 authority to make a targeted cross-reference fix commit to ctl_instruction.md with a `docs(19-03): fix cross-reference` message.

### m6: 19-04-SUMMARY.md naming may conflict if Phase 19 is re-executed

**Persona:** feasibility-reviewer
**Evidence:** P04 Task 3 creates `19-04-SUMMARY.md`. Phase 18 created `18-01-SUMMARY.md`, `18-02-SUMMARY.md`, `18-03-SUMMARY.md`. The naming convention differs: Phase 19 uses `19-04-SUMMARY.md` (matching the plan number), while Phase 18 used per-wave summaries. This is inconsistent but not incorrect. The real risk is if Phase 19 needs re-execution and the summary gets overwritten.

**Suggested fix:** Either align with Phase 18's per-wave convention (`19-01-SUMMARY.md`, `19-02-SUMMARY.md`, etc.) or document that Phase 19 uses a single terminal summary by design.

### m7: Missing explicit declaration that live pinn/ code was not read during execution

**Persona:** project-standards-reviewer
**Evidence:** All plans include "No `pinn/*.py` file is modified" in acceptance criteria, and the threat models warn against treating live code as evidence. But no task explicitly verifies "no `pinn/` file was read during execution." This is hard to verify mechanically, but a self-attestation in the summary would help.

**Suggested fix:** Add a self-attestation line to each plan summary: "Confirmed: no `pinn/` file was read or used as v1.4 evidence during this plan's execution."

---

## Missed Gaps (should have been documented in 19-GAPS.md)

### GAP-19-01: Causal-weight clipping threshold is under-specified

**Classification:** semantic
**Where:** P02 Task 2 spec edit (total-loss section, causal weighting line)
**Context:** The spec says `w_n = exp(-η_c · Σ stopgrad(R̄_m))` but 19-CONTEXT.md D-10 says "with clipping of the exponent to avoid underflow." No clipping threshold is specified in either the plan or the spec edit.
**Impact:** MEDIUM — FUT-01 implementers need the clipping value; without it, underflow could silently zero out physics loss.
**Options:**
- A: Clip exponent to `[-20, 0]` (standard exp clipping; prevents underflow below e⁻²⁰ ≈ 2×10⁻⁹)
- B: Clip weights directly to `[10⁻⁶, 1]` (post-exp clipping; simpler)
- C: Defer to resolution doc §8.4; transcribe whatever value it specifies

### GAP-19-02: L_L angular momentum loss behavior for zero-L initial conditions

**Classification:** semantic
**Where:** P02 Task 2 §3.x Angular Momentum Conservation Loss
**Context:** For zero-angular-momentum ICs, L_scale = ε_L = 10⁻⁸, causing the relative drift to amplify small absolute errors by 10⁸.
**Impact:** LOW — Huber caps damage; zero-L ICs are a subset of all ICs; most random ICs have nonzero L.
**Options:**
- A: Use `L_scale = max(||L_0'||, L_min) + ε_L` with a physical L_min
- B: Document as known edge case; FUT-01 handles with IC-specific normalization
- C: Accept current formulation; Huber cap is sufficient mitigation

### GAP-19-03: No formal specification of which "Hamiltonian" mentions stay vs go

**Classification:** semantic
**Where:** P03 Task 1 (HNN prose rewrite)
**Context:** D-09 says keep "Hamiltonian" where it means analytic H_ε. P03 Task 1 sweep command (line 133) removes all HNN variants but keeps "Hamiltonian." Without explicit criteria, the executor may keep or remove borderline cases inconsistently.
**Impact:** LOW — prose-level; AC-PHYS-04 structural check catches gross errors.
**Options:**
- A: Keep "Hamiltonian" only when immediately followed by "H_ε" or preceded by "analytic"/"matched-Plummer"
- B: Replace ALL instances of "Hamiltonian" with "energy function" except in the formal definition of H_ε
- C: Executor discretion; AC-PHYS-04 structural check is the gate

---

## Physics and Mathematics Verification

### Dimensional analysis (B-02 / PHYS-01): ✓ CORRECT

Newton's equation: m_i · d²r_i/dt² = G · Σ_j m_i · m_j · (r_j − r_i) / ||r_j − r_i||³

Substituting r = D·r', t = T·u, m_i = M_scale·m_i':
- LHS: m_i · d²r_i/dt² = M_scale·m_i' · (D/T²) · d²r_i'/du²
- RHS: G · Σ_j (M_scale·m_i') · (M_scale·m_j') · D·(r_j' − r_i') / (D³·||r_j' − r_i'||³)
       = G · M_scale²/D² · m_i' · Σ_j m_j'·(r_j' − r_i') / ||r_j' − r_i'||³

Cancel m_i': M_scale·(D/T²) · d²r_i'/du² = G·M_scale²/D² · Σ_j m_j'·(r_j' − r_i') / ||r_j' − r_i'||³

Divide by M_scale: (D/T²) · d²r_i'/du² = G·M_scale/D² · Σ_j m_j'·(r_j' − r_i') / ||r_j' − r_i'||³

For the dimensionless residual to have unit coefficient: D³/(G·M_scale·T²) = 1 → D³ = G·M_scale·T²

- **Raw masses** (m_i' = m_i, M_scale = 1 in natural units G=1): D³ = 1·T² → D = T^(2/3) ≈ 4.6416 ✓
- **Mass fractions** (m_i' = m_i/M_tot, M_scale = M_tot = 1 in natural units): D³ = 1·T² → same D ✓ (wait...)

Actually, let me re-examine. If we use mass fractions m_i' = m_i/M_tot where M_tot = Σ m_i, then in natural units M_tot = 1. But the M_scale in the dimensionless equation is M_tot = 1 (since masses are fractions of M_tot). So D³ = G·M_scale·T² = 1·1·T² = T². D = T^(2/3) ≈ 4.6416. Same D!

Hmm, but the CONTEXT says the issue doc's D = 6.694 comes from M_tot = 1. Let me reconsider...

Wait. If M_tot = 1 in natural units, and we use mass fractions m_i' = m_i/M_tot = m_i (since M_tot = 1), then raw masses and mass fractions give the same D. The difference only matters when M_tot ≠ 1 (which it isn't in natural units, but the FORMULA differs).

Actually, the key insight is: the issue doc proposed D = (G·M_tot·T²)^(1/3) as the FORMULA, not a specific numeric value for a specific M_tot. If M_tot = 1, both formulas give D = T^(2/3) = 4.6416. The difference is conceptual: raw-mass convention says D depends only on G and T; mass-fraction convention says D also depends on M_tot. In natural units (G=1, M_tot=1), the numeric values coincide for the standard normalization.

But wait, the CONTEXT says D = 6.694 for the mass-fraction approach. Where does 6.694 come from? If D = (G·M_tot·T²)^(1/3) and the training uses specific values of M_tot and T, then... The training T is chosen so that T^(2/3) = 4.6416. If the issue doc used M_tot = 3 (three bodies of mass ~1 each), then D = (1·3·T²)^(1/3) = 3^(1/3) · T^(2/3) = 1.442 · 4.6416 ≈ 6.694. So 6.694 = 3^(1/3) · 4.6416, meaning the "mass-fraction" D is 3^(1/3) times the raw-mass D when M_tot = 3.

This is correct: the issue doc's formula D = (G·M_tot·T²)^(1/3) with M_tot = 3 (three bodies) gives D = 3^(1/3) · (G·T²)^(1/3) ≈ 1.442 · 4.6416 ≈ 6.694.

The dimensional analysis is CORRECT. ✓

### Plummer matched-pair argument (B-09 / PHYS-03): ✓ CORRECT

Plummer potential: V ∝ -1/√(r² + ε²)
Force: F = -∇V = -∂V/∂r · r̂ = -[r/(r² + ε²)^(3/2)] · r̂ = -r/r_safe³

So F ∝ 1/r_safe³ and V ∝ 1/r_safe — both use the same r_safe = √(r² + ε²), giving a matched pair. ✓

Additive "potential": V_add ∝ -1/(r + ε)
Force: F_add = -∇V_add = -1/(r + ε)² · r̂ = -r/(r·(r+ε)²)

Additive "force" used in spec: F_spec ∝ 1/(r + ε)³

These are NOT a matched pair: -∇(-1/(r+ε)) ≠ -1/(r+ε)³. The additive forms in the current spec ARE inconsistent. ✓

### M4 constraint counting: ✓ CORRECT

3 bodies in 3D: 18 DOF (3 bodies × 3 position coords × 2 for position + velocity)
Constraints (all vector, 3 components each):
- COM position: Σ m_i r_i = 0 → 3 scalar constraints
- COM momentum: Σ m_i v_i = 0 → 3 scalar constraints  
- Angular momentum: Σ m_i r_i × v_i = 0 → 3 scalar constraints
Total constraints: 9
Reduced phase space: 18 − 9 = 9

The issue doc's arithmetic (9, not 8) is correct. The resolution doc's reframing (constraint counting is irrelevant; validity comes from gauge-fixed encoding) is the correct framing under Jacobi IC13. ✓

### PHYS-02 AD contract: ✓ CORRECT

If u is the autograd leaf and the network computes τ = 2u − 1 internally:
- PyTorch autograd chain rule: ∂r/∂u = ∂r/∂τ · ∂τ/∂u = ∂r/∂τ · 2
- Second derivative: ∂²r/∂u² = ∂/∂u(∂r/∂τ · 2) = ∂/∂τ(∂r/∂τ · 2) · ∂τ/∂u = ∂²r/∂τ² · 2 · 2 = 4 · ∂²r/∂τ²

So if the code puts u on the autograd graph and lets autograd handle τ internally, the chain-rule factors are automatic. The plan's "conditional" framing (factors apply only to τ-leaf path) is technically correct but potentially confusing — in practice, using u as leaf means you NEVER manually apply the 2×/4× factors because autograd handles them.

The anti-pattern warning about `r.sum()` is the essential correctness guard. ✓

---

## Cross-Document Consistency

| Check | Status | Notes |
|-------|--------|-------|
| D-01 through D-19 map to plan tasks | ✓ PASS | All 19 decisions have clear plan-task coverage |
| Total-loss formula consistent across all 6 docs | ✓ PASS | `L_total = L_data + λ_IC·L_IC + λ_phys·L_phys^causal + λ_E·L_E + λ_L·L_L` matches everywhere |
| AC-PHYS-01..06 across CONTEXT and P04 | ✓ PASS | Same structural criteria in both |
| Evidence packet headers match CONTEXT | ✓ PASS | B-02/B-07/B-08/B-09/M4 headers consistent |
| Phase 16/17/18 cross-references valid | ⚠️ FLAG | Line numbers may be stale post-Phase-17/18 execution |
| 19-DISCUSSION-LOG marked "audit trail only" | ✓ PASS | Not used as input by any plan |
| 19-CONTEXT.md GOVERNANCE NOTICE vs plan content | ⚠️ FLAG | CONTEXT says "No new 19-GAPS.md entries are created at context-gathering time" but plans don't create it either (see B1) |

---

## Summary

**Physics/mathematics:** All core claims verified correct. The dimensional analysis, Plummer matched-pair argument, constraint counting, and AD contract are mathematically sound.

**Plan structure:** The 4-plan decomposition is reasonable. P01/P02 parallelism is safe (different files). P03 blocker on P02 is correct. P04 closure gating on Waves 1-2 is correct.

**Key risks:**
1. No gap register file exists (B1 — BLOCKING)
2. Cross-plan total-loss repair deadlock (B2 — BLOCKING)
3. Causal-weight clipping unspecified (M1 — MAJOR)
4. Fragile verification regexes (M2 — MAJOR)
5. L_L zero-L edge case (M3 — MAJOR)

**Recommendation:** Fix B1 and B2 before execution. Address M1-M5 during execution. The three missed gaps (GAP-19-01 through GAP-19-03) should be pre-registered in 19-GAPS.md with the resolution options documented, so the executor can handle them without stopping.
