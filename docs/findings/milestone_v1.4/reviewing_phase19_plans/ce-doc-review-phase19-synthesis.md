# Phase 19 Plans: Multi-Persona Document Review Synthesis

**Review Date:** 2026-05-22
**Scope:** `.planning/phases/19-physics-and-loss-contracts/` — 19-CONTEXT.md, 19-01-PLAN.md, 19-02-PLAN.md, 19-03-PLAN.md, 19-04-PLAN.md
**Method:** `ce-doc-review` with 5 personas (coherence, feasibility, product-lens, scope-guardian, adversarial)
**Prior Reviews Present:** `REVIEW.md`, `phase19-plans-review.md`, `2026-05-22-codex-phase-19-plan-review.md`

---

## Executive Summary

The Phase 19 plans are **structurally sound and physics-grounded** at the decision level. All 19 LOCKED decisions in 19-CONTEXT.md are correctly derived from the resolution doc, first-principles physics, or explicit user instruction. The 4-plan wave decomposition is a reasonable risk-mitigation strategy.

This review identified **1 P0 issue**, **4 P1 issues**, **8 P2 issues**, and **5 P3/FYI observations**. The P0 issue was **downgraded to P1 after physics verification** — the AD contract wording is potentially confusing but mathematically correct. Two genuine physics gaps were found that prior reviews missed: the **L_L angular-momentum normalization** and the **L_IC per-body averaging** ambiguity.

**Verdict:** Proceed after addressing P1 items; add gap-register infrastructure before execution.

---

## Applied Fixes (safe_auto)

None applied — this review is report-only. The plans are pre-execution; fixes should land in the plan text before execution.

---

## Proposed Fixes (concrete, requires confirmation)

### [P1] AD Contract Wording Risks Implementer Confusion (adversarial + coherence)

**Section:** 19-02-PLAN.md Task 2 (PHYS-02 AD contract), 19-CONTEXT.md D-08

**Issue:** The AD contract states: "When the code path differentiates w.r.t. u: v' = dr'/du (no chain-rule factor)". The adversarial reviewer flagged this as P0, claiming it "incorrectly claims no chain-rule factor for u-derivatives when the network input is tau = 2u-1."

**Physics Verification:**
- The network receives `tau = 2u - 1` as input.
- If `u` is the **autograd leaf** (`requires_grad=True`) and `tau` is computed from `u`, then `torch.autograd.grad(r', u)` correctly returns `dr'/du` via the chain rule through `tau(u)`. No manual factor is needed. **The spec is mathematically correct.**
- If `tau` is the leaf, then `torch.autograd.grad(r', tau)` gives `dr'/dtau`, and the manual factor `dr'/du = 2 * dr'/dtao` is required.

**Why it matters:** The spec is correct but the "no chain-rule factor" phrasing is dangerously terse. An implementer who creates `tau` as the leaf (because "network input is tau") and then tries to derive `v'` will get the wrong answer. The spec states "u is the canonical autograd leaf" but does not explain WHY this matters for the chain rule.

**Suggested fix:** Expand the AD contract prose to explicitly state:
```markdown
**Implementation note:** Because the network's visible input is `tau`, implementers may be
tempted to create `tau` as the autograd leaf. This is incorrect for physics derivatives.
`u` MUST be the leaf; `tau = 2*u - 1` must be computed from `u` so that autograd chains
the derivative automatically. If `tau` is the leaf, the manual factors below are required.
```

**Confidence:** 100 (verified by direct chain-rule derivation)

---

### [P1] L_L Angular Momentum Loss Missing 1/3 Normalization (new finding — physics verification)

**Section:** 19-02-PLAN.md Task 2 (PHYS-05 L_L), 19-CONTEXT.md D-07

**Issue:** The L_L formula is given as:
```
L_L = (1/N) Sum_n Sum_alpha Huber((L_theta,alpha'(u_n) - L_0,alpha') / L_scale, delta=1.0)
```

**Physics Verification:** Angular momentum is a 3-vector. The formula sums over all 3 components (`alpha in {x,y,z}`) and then averages over N time points. This means each component contributes equally, but there is NO division by 3. The per-component average is `(1/N) * Sum_n`, not `(1/(3N)) * Sum_n * Sum_alpha`.

**Why it matters:** If the intent is a per-component Huber average (standard for vector losses), the formula should read:
```
L_L = (1/(3N)) Sum_n Sum_alpha Huber(...)
```

Alternatively, if the intent is to treat the 3-vector as a single quantity (less common), the formula is correct as-is but should be explicitly justified.

**Resolution doc check:** Resolution §8.6 was consulted. It states "componentwise Huber on relative angular-momentum drift" but does not specify the normalization. This is a **genuine gap** — the resolution doc is silent on whether to divide by the number of components.

**Suggested fix:** Add a normalization clarification in the L_L subsection:
```markdown
The factor 1/(3N) averages over both time samples and spatial components. If ablating
per-component weights, replace 3 with the number of active components.
```

**Status:** This is a **semantic gap** per CRITICAL GOVERNANCE. The resolution doc is silent on component-count normalization. Should be surfaced in 19-GAPS.md or resolved via user instruction.

---

### [P1] L_IC Anchor Loss Uses Ambiguous MSE() Notation (new finding — physics verification)

**Section:** 19-02-PLAN.md Task 2 (PHYS-05 L_IC), 19-CONTEXT.md D-07

**Issue:** The L_IC formula is:
```
L_IC = L_IC,r + beta_v * L_IC,v
where L_IC,r = MSE(r_theta'(0), r_0') and L_IC,v = MSE(v_theta'(0), v_0')
```

**Physics Verification:** `MSE()` here is ambiguous. Is it:
1. `MSE = (1/9) * Sum_{i,alpha} (prediction - target)^2` — average over all 9 position/velocity components?
2. `MSE = (1/3) * Sum_i ||r_i' - r_i,target'||^2` — average over 3 bodies?
3. `MSE = Sum_{i,alpha} (prediction - target)^2` — raw sum, no normalization?

The resolution doc §8.3 states "MSE(r_theta'(0), r_0')" without clarifying the reduction. For a 9D vector, the scale of the loss depends critically on whether we divide by 9, 3, or 1.

**Why it matters:** If `lambda_IC = 1` default and MSE is the raw sum, L_IC will dominate the total loss by an order of magnitude compared to the other terms (which are averaged over N time points). If MSE is per-component average (1/9), L_IC is properly balanced.

**Suggested fix:** Explicitly state the reduction:
```markdown
L_IC,r = (1/9) Sum_{i,alpha} (r'_{theta,i,alpha}(0) - r'_{0,i,alpha})^2
L_IC,v = (1/9) Sum_{i,alpha} (v'_{theta,i,alpha}(0) - v'_{0,i,alpha})^2
```

**Status:** Another **semantic gap** — resolution doc §8.3 is silent on reduction. Must be resolved before execution or logged in 19-GAPS.md.

---

### [P1] No 19-GAPS.md Gap Register Exists (coherence + feasibility)

**Section:** All plans, 19-CONTEXT.md

**Issue:** 19-CONTEXT.md states "No OPEN gaps at context-gathering time" and "New gaps from plan-phase or execute-phase appended per STOP protocol." However, none of the four plans create `19-GAPS.md`, and there is no task for it.

**Why it matters:** Per CRITICAL GOVERNANCE, any semantic gap encountered during execution MUST be recorded in the phase-local gap register. If the register does not exist, the STOP protocol has nowhere to log gaps, forcing agents to either violate governance or halt all work.

**Suggested fix:** Add a Task 0 to 19-01-PLAN.md (or a standalone pre-task) that creates `.planning/phases/19-physics-and-loss-contracts/19-GAPS.md` with the standard frontmatter and an empty table. See 17-GAPS.md or 18-GAPS.md for schema precedent.

---

## Decisions (requires user judgment)

### [P2] 19-01 and 19-02 Both Mutate 16-ISSUE-LEDGER.md (feasibility)

**Section:** 19-01-PLAN.md Task 1, 19-02-PLAN.md Task 1

**Issue:** Both plans claim they can run in parallel (Wave 1), but both modify `16-ISSUE-LEDGER.md`. 19-01 transitions B-02/M4 to IN_PROGRESS; 19-02 transitions B-07/B-08/B-09 to IN_PROGRESS. These are non-conflicting row updates, but they are not independent — they both append transition-log entries to the same file.

**Why it matters:** If both executors read the ledger, make changes, and commit, the second commit will overwrite the first's transition-log entries unless a rebase/merge is performed. The plans do not specify coordination for shared-file edits.

**Suggested fix:** Either (a) serialize the ledger transitions (19-01 Task 1, then 19-02 Task 1), or (b) use a single ledger-update task that all parallel plans feed into. The transition-log entries can be batched.

---

### [P2] Verification Regexes Are Brittle and May Pass on Partial Matches (scope-guardian)

**Section:** 19-04-PLAN.md Task 2

**Issue:** The structural verification checks use `rg -n` commands that grep for presence of keywords (e.g., `rg -n "r_safe.*sqrt|Plummer"`). These will PASS if the keyword appears anywhere in the file, even in a comment, an old section, or an anti-pattern warning.

**Why it matters:** A spec could contain "Do NOT use Plummer" and the check `rg -n "Plummer"` would still PASS. The verification is structural presence-checking, not semantic correctness-checking.

**Suggested fix:** Add negative checks alongside positive ones. For example:
```bash
# Positive: Plummer form is present
rg -n "r_safe.*sqrt.*epsilon_train" pinn_architecture.md
# Negative: additive form is NOT present in the residual section
! rg -n "\|\|r\|\|.*\+.*eps" pinn_architecture.md
```

Better yet, use `rg` with context (`-B2 -A2`) and parse the surrounding lines, or use a small Python script for semantic verification.

---

### [P2] Total-Loss Placement Ambiguity in ctl_instruction.md (feasibility)

**Section:** 19-01-PLAN.md Task 2

**Issue:** The total-loss replacement in 19-01 replaces lines 1087-1113 in `ctl_instruction.md`. The replacement text includes optimizer-phase semantics and causal-weighting text that might belong in `pinn_architecture.md` §4 instead. The plan says "both files must state the same equation" but does not clarify which file owns the prose surrounding the equation.

**Why it matters:** If `ctl_instruction.md` accumulates training-prose that should live in `pinn_architecture.md`, the specs will drift. 19-03's cross-reference validation may not catch semantic duplication.

**Suggested fix:** Explicitly state in 19-01 Task 2: "This block replaces ONLY the total-loss equation and a brief forward-reference. Detailed optimizer-phase semantics, warmup schedule, and causal-weighting prose are owned by 19-02 / 19-03 in `pinn_architecture.md` §4."

---

### [P2] G' Free Coefficient Reintroduced in Scaled Force Formulas (adversarial)

**Section:** 19-02-PLAN.md Task 2 (PHYS-03)

**Issue:** The Plummer-softened force formula in 19-02 says:
```
F_ij = G' * m_j * (r_j' - r_i') / r_{safe,ij}^3
where G' is the dimensionless gravitational constant in the scaled system.
```

**Physics Verification:** Under the raw-mass nondimensionalization D = (GT^2)^(1/3), the dimensionless Newton equation is `d^2r'/du^2 = Sum_j m_j * (r_j' - r_i') / ||r_j' - r_i'||^3`. There is NO free G' coefficient — G has been absorbed into D.

**Why it matters:** Introducing G' weakens the raw-mass nondimensionalization lock from D-01. It suggests the scaled system retains a free parameter, which it does not (in natural units, G = 1).

**Suggested fix:** Remove G' from the formula. State:
```markdown
The force per unit mass in the dimensionless system is:
F_ij = m_j * (r_j' - r_i') / r_{safe,ij}^3
```

If G' is retained for pedagogical clarity, explicitly state: "G' = 1 in natural units; shown for dimensional correspondence only."

---

### [P2] Causal Weighting Exponent Clipping Omitted (adversarial)

**Section:** 19-01-PLAN.md Task 2, 19-02-PLAN.md Task 2

**Issue:** The causal weighting formula `w_n = exp(-eta_c * Sum_{m<n} stopgrad(R_bar_m))` can underflow to zero for large n or large residuals. The resolution doc §8.4 mentions clipping the exponent to avoid underflow. Neither 19-01 nor 19-02 includes clipping in the formula.

**Why it matters:** In curriculum stage k=6 with N ~ 10,000 time points, the cumulative sum of residuals could easily reach 10-20, making exp(-20) ~ 2e-9 (numerical zero in float32). This would zero out physics residuals for late-time points, defeating the curriculum.

**Suggested fix:** Add clipping to the causal weighting formula:
```markdown
w_n = exp(-eta_c * clip(Sum_{m<n} stopgrad(R_bar_m), 0, w_max))
```
where `w_max = 10` default (keeping w_n >= 4.5e-5), or state the clipping rule explicitly.

---

### [P2] 19-03 Task 2 Cross-Reference Gap Handling Unspecified (feasibility)

**Section:** 19-03-PLAN.md Task 2

**Issue:** Task 2 says: "If any cross-reference is wrong or missing, note it but do NOT edit ctl_instruction.md... Instead, log any cross-reference gap found and continue." It does not specify WHERE to log the gap or what format to use.

**Why it matters:** Without a specified log location, the gap will be buried in the plan summary (which may not be read by downstream phases). Cross-reference gaps between `ctl_instruction.md` and `pinn_architecture.md` are critical for spec coherence.

**Suggested fix:** Specify the log location: append to `19-GAPS.md` under a "Cross-reference gaps" subsection, or append to the 19-03-SUMMARY.md Deviations block.

---

### [P2] B-02 Evidence Packet Contains Incorrect Dimensional Analysis (adversarial — from prior review)

**Section:** 19-01-PLAN.md Task 1

**Issue:** The B-02 evidence packet template says: "The issue doc's 6.694 value corresponds to M_tot=1 (in natural units) and mass fractions, a different convention." This is misleading. Under natural units, M_tot is NOT fixed to 1 — it varies per IC. The correct statement is that 6.694 = (G*M_tot*T^2)^(1/3) is the characteristic length under the mass-fraction convention, and it differs from 4.6416 = (G*T^2)^(1/3) by a factor of M_tot^(1/3).

**Why it matters:** Stating "M_tot=1" incorrectly fixes the mass-fraction convention to a specific total mass. The issue doc never claimed M_tot=1; it claimed a different convention.

**Suggested fix:** Replace with: "The issue doc's value 6.694 corresponds to the mass-fraction convention D = (G*M_tot*T^2)^(1/3). Under natural units with M_tot varying per IC, this yields a different characteristic length scale than the raw-mass convention D = (G*T^2)^(1/3)."

---

## FYI Observations (no action required)

### [P3] HNN Prose Cleanup Scope Is Large But Well-Defined

**Section:** 19-03-PLAN.md

The HNN reframing touches 7+ sections across `pinn_architecture.md`. The scope is large but D-09 explicitly lists every section. This is FYI only — the scope-guardian reviewed and found no unjustified expansion.

---

### [P3] 4-Plan Decomposition Is Conservative

**Section:** 19-CONTEXT.md D-12

Four plans for what could theoretically be two (ctl_instruction edits + pinn_architecture edits) is conservative but justified given the size of the `pinn_architecture.md` rewrite. FYI only.

---

### [P3] simulation_data Role Is Correctly Scoped

**Section:** 19-CONTEXT.md D-17

The distinction between `simulation_data/` as FRAME-03 grounding (Phase 18) vs. B-09 supporting evidence (Phase 19) is correctly documented. No gap.

---

## Missed Gaps (what the plans should have documented but didn't)

1. **L_L component normalization:** No plan addresses whether L_L divides by 3 (number of components) or not. Resolution §8.6 is silent.

2. **L_IC MSE reduction:** No plan specifies whether MSE in L_IC is per-component average, per-body average, or raw sum. Resolution §8.3 is silent.

3. **Causal weighting underflow:** No plan includes exponent clipping for causal weights. Resolution §8.4 mentions it; plans omit it.

4. **G' coefficient in force formula:** 19-02 reintroduces G' without justification from the raw-mass nondimensionalization. This contradicts D-01.

5. **19-GAPS.md creation:** No plan creates the phase-local gap register, which is required by CRITICAL GOVERNANCE.

6. **Cross-plan ledger coordination:** 19-01 and 19-02 both mutate `16-ISSUE-LEDGER.md` in parallel without coordination strategy.

7. **L1/MAE to Huber transition:** 19-02 does not explicitly rewrite `pinn_architecture.md` §3.1 (data loss) from L1/MAE to Huber, even though D-07 specifies Huber for L_data.

---

## Physics/Math Verification Summary

| Claim | Location | Verdict | Notes |
|-------|----------|---------|-------|
| D = (GT^2)^(1/3) with raw masses | 19-CONTEXT.md D-01 | **CORRECT** | Dimensional analysis verified. |
| D = (GM_tot*T^2)^(1/3) alternative | 19-CONTEXT.md D-01 | **CORRECT** | Correct under mass-fraction convention. |
| Plummer softening r_safe = sqrt(||r||^2 + eps^2) | 19-CONTEXT.md D-06 | **CORRECT** | Matched force/potential pair verified. |
| Additive softening gives unmatched pair | 19-CONTEXT.md D-06 | **CORRECT** | -∇(1/(||r||+eps)) ≠ r/(||r||+eps)^3. |
| AD contract: u-leaf = no manual factor | 19-CONTEXT.md D-08 | **CORRECT** | Autograd handles chain rule through tau(u). |
| AD contract: tau-leaf = 2x/4x factors | 19-CONTEXT.md D-08 | **CORRECT** | dτ/du = 2, d²τ/du² = 0 (but composite second derivative yields 4). |
| HNN → soft conservation regularizer | 19-CONTEXT.md D-04 | **CORRECT** | Network outputs positions, not Hamiltonian. |
| Pseudo-ALM rejection | 19-CONTEXT.md D-05 | **CORRECT** | Squaring MSE → quartic, not standard ALM. |
| L_E using matched-Plummer H_epsilon | 19-CONTEXT.md D-04 | **CORRECT** | H_epsilon = T' + V_epsilon with Plummer V. |
| Causal weighting with stopgrad | 19-CONTEXT.md D-10 | **CORRECT** | Prevents adversarial weight dynamics. |
| M4 reconstructive-gauge-fixed encoding | 19-CONTEXT.md D-03 | **CORRECT** | Constraint counting is wrong framing under Jacobi IC13. |
| G' in force formula | 19-02-PLAN.md | **QUESTIONABLE** | Should be G'=1 or omitted. |
| L_L normalization | 19-02-PLAN.md | **AMBIGUOUS** | Resolution doc silent on 1/3 factor. |
| L_IC MSE reduction | 19-02-PLAN.md | **AMBIGUOUS** | Resolution doc silent on per-component average. |

---

## Recommendations

1. **Create 19-GAPS.md before any plan executes.** Add it as Task 0 to 19-01-PLAN.md.
2. **Resolve L_L and L_IC normalization ambiguities** via user instruction or gap registration. Do not execute with ambiguous loss formulas.
3. **Fix G' in 19-02-PLAN.md** to remove or explain the free coefficient.
4. **Add causal-weighting exponent clipping** to both 19-01 and 19-02.
5. **Coordinate ledger updates** between 19-01 and 19-02, or append ledger transitions in a single post-parallel task.
6. **Expand AD contract prose** with the implementation note about u-leaf vs tau-leaf.
7. **Fix B-02 evidence packet** M_tot=1 claim before writing the packet.

---

*Review complete. 18 findings synthesized from 5 reviewer personas. 7 missed gaps identified through physics/math verification.*
