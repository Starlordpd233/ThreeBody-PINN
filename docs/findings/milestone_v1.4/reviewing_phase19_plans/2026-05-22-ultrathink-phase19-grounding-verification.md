# Phase 19 Plans Deep Review: Physics Grounding Verification and Execution Risks

**Reviewed:** 2026-05-22
**Reviewer Mode:** ultrathink — maximum depth, recall-first
**Documents:** 19-CONTEXT.md, 19-DISCUSSION-LOG.md, 19-01-PLAN.md, 19-02-PLAN.md, 19-03-PLAN.md, 19-04-PLAN.md
**Reference:** ctl_pinn_resolution.md §8.1-8.8 (numerical parameter grounding)
**Pre-existing Review:** REVIEW.md in same directory (2 blocking, 5 major, 7 minor)

---

## Executive Summary

This review performs **ultrathink-level physics/math grounding verification** for Phase 19 numerical parameters and identifies execution risks beyond the existing REVIEW.md. 

**Key findings:**
1. **All numerical parameters ARE grounded in resolution doc §8.1-8.8** — no semantic gaps for default values
2. **3 EXECUTION RISKS** not covered in prior review
3. **2 cross-reference consistency gaps** in plan task instructions
4. **1 subtle physics edge case** for Plummer softening at collision proximity

The prior REVIEW.md's blocking issues (B1, B2) and major issues (M1-M5) remain valid. This report supplements with additional analysis and verifies grounding claims.

---

## Numerical Parameter Grounding Verification

### Resolution Doc §8.1-8.8 Verification Table

| Parameter | Value | Resolution Doc Line | Grounding Status |
|-----------|-------|---------------------|------------------|
| δ_r (L_data Huber) | 1.0 | §8.2 line 860 | ✓ GROUNDED |
| β_v (L_IC velocity weight) | 1 | §8.3 line 883 | ✓ GROUNDED |
| η_c (causal weighting) | 1 | §8.4 line 918 | ✓ GROUNDED |
| ε_L (L_L numerical stability) | 10^-8 | §8.6 line 952 | ✓ GROUNDED |
| L_E Huber δ | 1.0 | §8.5 line 934 | ✓ GROUNDED |
| L_L Huber δ | 1.0 | §8.6 line 960-961 | ✓ GROUNDED |
| λ_IC default | 1 | §8.7 line 1006 | ✓ GROUNDED |
| λ_IC ablation range | [0.1, 10] | §8.7 line 1009 | ✓ GROUNDED |
| λ_phys^max(k) default | 1 | §8.7 line 978-979 | ✓ GROUNDED |
| λ_E^max(k) schedule | {0, 10^(k-4), 1} | §8.7 line 985-991 | ✓ GROUNDED |
| I_warm formula | min(2000, 0.1·N_Adam,k) | §8.7 line 969 | ✓ GROUNDED |
| ε_H (energy denominator stability) | 10^-8 | §8.5 line 928-929 | ✓ GROUNDED (implied from formula) |

**Conclusion:** The plans correctly transcribe all numerical defaults from resolution doc. No semantic gaps exist for these parameters. The 19-CONTEXT.md D-07 citations are accurate.

---

## Additional Execution Risks (Not in Prior Review)

### ER1: Parallel Execution Race Condition for Total-Loss Formula

**Severity:** HIGH (Execution Risk)
**Location:** P01 Task 2 + P02 Task 2 coordination

**Finding:** P01 and P02 are marked as "Wave 1, parallel" but both must land the SAME total-loss formula. The plans acknowledge coordination via D-07 formula, but:

- If P01 executor and P02 executor are different agents running concurrently
- Both read D-07 formula and independently transcribe
- One may introduce a typo or formatting variation
- Race condition: whichever commits first becomes the "reference"

**Why prior review missed it:** REVIEW.md B2 addresses mismatch repair, but not the prevention mechanism. The race condition itself is an execution risk.

**Mitigation:** Before Wave 1 execution, confirm both executors use the EXACT formula string from D-07. Consider a pre-flight check:

```bash
# Both executors verify before commit
echo "L_total = L_data + λ_IC · L_IC + λ_phys · L_phys^causal + λ_E · L_E + λ_L · L_L"
```

If running on same agent context (sequential parallel), no race. If truly concurrent agents, add mutex/coordination.

---

### ER2: Verification Regex Negative Pattern May False-Positive on Historical Context

**Severity:** MEDIUM (Execution Risk)
**Location:** Multiple task verification commands

**Finding:** Negative checks like:
```bash
! rg -n "lambda_p.*L_phys.*mu_p.*L_phys" pinn_architecture.md
```

If the spec includes a "History" or "Why we rejected this" section explaining the old formulation, the regex matches historical prose and verification fails incorrectly.

**Why this matters:** Plans use negative regex checks extensively. A spec section explaining "Previous pseudo-ALM formulation +λ_p L_phys + (μ_p/2) L_phys² was rejected" would trigger false-positive failure.

**Mitigation:** Add context exclusion to negative checks:
```bash
! rg -n "lambda_p.*L_phys.*mu_p.*L_phys" pinn_architecture.md | grep -v "rejected|previous|History|Why"
```

Or verify matches are NOT in explanatory prose sections.

---

### ER3: Batch-Mode AD Contract Implementation Gap

**Severity:** MEDIUM (Execution Risk)
**Location:** P02 Task 2 PHYS-02 Python listing

**Finding:** The Python listing shows single-sample operation:

```python
def model_single(u_scalar, ic13):
    """Single-trajectory forward pass."""
    return net(torch.cat([2*u_scalar - 1, ic13]))  # tau = 2u-1

J = jacrev(model_single)(u, ic13)  # shape (9, 1)
```

Actual training requires batch-mode: `[batch_size, N_collocation]` inputs. The spec doesn't address:

1. How `jacrev` + `vmap` compose for batched inputs
2. Whether the batch dimension is the FIRST or LAST axis
3. Memory implications of full-Jacobian for batch_size × N_collocation × 9 outputs

**Why prior review addressed it:** REVIEW.md M5 covers this but as "MAJOR." I downgrade to "Execution Risk" because FUT-01 will discover this during implementation, not during spec validation.

**Mitigation:** Add batch-mode note to spec:

```markdown
**Batch-mode composition:** The single-sample listing above illustrates the derivative contract.
For batched training, apply `vmap` over both the u-batch and ic13-batch dimensions:
`J_batch = vmap(vmap(jacrev(model_single), in_dims=(0, None)), in_dims=(None, 0))(u_batch, ic13_batch)`
Memory cost: O(batch × N × 9 × hidden) per forward+backward pass. Batch size tuning is Phase 20 scope.
```

---

## Cross-Reference Consistency Gaps

### CR1: s_min Unsoftened Citation Missing in Spec Edit

**Severity:** MINOR (Documentation Gap)
**Location:** P02 Task 2 PHYS-03 Plummer conversion

**Finding:** 19-CONTEXT.md D-02 states: "s_min unsoftened (resolution §7.2: 'Softening never enters curriculum collision gates')"

But P02 Task 2 doesn't include explicit citation of §7.2 in the spec edit. The executor may omit the anti-pattern warning for s_min.

**Mitigation:** Add to spec text:
```markdown
**Collision gate invariant:** s_min = min_{i<j} ||r_i' − r_j'|| remains unsoftened.
Softening ε_train / ε_inv applies to force/potential pair, NOT to curriculum collision detection
(resolution §7.2: softening never enters collision gates).
```

---

### CR2: L_IC MSE vs L_data Huber Justification Missing

**Severity:** MINOR (Documentation Gap)
**Location:** P02 Task 2 L_IC definition

**Finding:** REVIEW.md M4 correctly identifies that L_IC uses MSE while L_data uses Huber. The resolution doc §8.3 defines L_IC with MSE (lines 869-877), but doesn't justify WHY.

**Physics reasoning:** IC values are known EXACTLY from preprocessing (COM-removed, gauge-fixed Jacobi state). There's no measurement uncertainty. Large IC errors indicate a training failure, not outlier data. MSE penalizes large errors quadratically, enforcing hard IC match.

**Mitigation:** Add justification note:
```markdown
**MSE for IC anchor:** Initial conditions are exact outputs of deterministic preprocessing
(Phase 17/18 canonical pipeline). No measurement noise or outlier risk. MSE's quadratic penalty
enforces hard IC match at u=0, whereas Huber would allow linear-tolerance drift.
```

---

## Subtle Physics Edge Cases

### PE1: Plummer Softening Bias at r ≈ ε

**Severity:** MINOR (Physics Edge Case)
**Location:** PHYS-03 Plummer conversion

**Finding:** At ε_train = 10^-5 and collision proximity r ≈ 0.05 (IC rejection floor), the Plummer softening introduces bias:

- Newtonian force: F_N = 1/r³ = 1/(0.05)³ = 8000
- Plummer force: F_P = 1/(r² + ε²)^(3/2) = 1/(0.05² + 10^-10)^(3/2) ≈ 1/(0.0025)^(3/2) ≈ 8000

At r ≈ ε (r ≈ 10^-5, physically impossible for training data but mathematically possible for residual computation):
- Newtonian: F_N = 1/(10^-5)³ = 10^15
- Plummer: F_P = 1/(10^-10 + 10^-10)^(3/2) = 1/(2×10^-10)^(3/2) ≈ 10^14.5

The Plummer form caps force growth at r < ε, preventing numerical overflow. This is INTENTIONAL — softening exists to regularize close encounters.

**Why this matters:** For normal training data (r ≥ 0.05), Plummer ≈ Newtonian to high precision. The softening only affects force computation when predicted positions approach artificial close encounter (training instability case).

**No gap:** Resolution doc §7.1-7.2 correctly explains matched Plummer pair. The capping behavior is implicit in the form.

---

## Verification of Prior Review's Physics Claims

### REVIEW.md Dimensional Analysis Verification

Prior review's dimensional analysis (lines 189-222) is **CORRECT**. I verified:

- Raw-mass D = (G·T²)^(1/3) ≈ 4.6416 ✓
- Mass-fraction D would be (G·M_tot·T²)^(1/3) with M_tot = 3 giving 6.694 ✓
- Issue doc's 6.694 was proposing formula change, not just different M_tot ✓

### REVIEW.md Plummer Matched-Pair Verification

Prior review's matched-pair analysis (lines 223-236) is **CORRECT**:

- Plummer: F ∝ 1/r_safe³, V ∝ 1/r_safe → matched ✓
- Additive: F_add ≠ -∇V_add → NOT matched ✓

### REVIEW.md AD Chain-Rule Verification

Prior review's AD analysis (lines 249-256) is **CORRECT**:

- Chain rule: ∂r/∂u = 2·∂r/∂τ, ∂²r/∂u² = 4·∂²r/∂τ² ✓
- If u is leaf, factors automatic via autograd ✓

---

## Summary of All Findings

| ID | Severity | Category | Description |
|----|----------|----------|-------------|
| ER1 | HIGH | Execution Risk | Parallel P01/P02 race condition for total-loss |
| ER2 | MEDIUM | Execution Risk | Negative regex may false-positive on historical prose |
| ER3 | MEDIUM | Execution Risk | Batch-mode AD composition gap in spec listing |
| CR1 | MINOR | Cross-Reference | s_min unsoftened §7.2 citation missing in spec edit |
| CR2 | MINOR | Cross-Reference | L_IC MSE vs Huber justification missing |
| PE1 | MINOR | Physics Edge | Plummer bias at r ≈ ε is intentional regularization |

**Prior review findings remain valid:** B1, B2 (BLOCKING), M1-M5 (MAJOR), m1-m7 (MINOR)

---

## Recommendations

1. **Before execution:** Fix B1 (create 19-GAPS.md) and B2 (cross-plan repair path)
2. **During execution:** Add race-condition prevention for P01/P02 total-loss
3. **During execution:** Add context-exclusion filters to negative regex checks
4. **After spec edits:** Verify s_min §7.2 citation and L_IC MSE justification present
5. **FUT-01 handoff:** Add batch-mode AD composition note to spec

---

## Verification Commands for This Review

```bash
# Verify resolution doc grounding for key parameters
rg -n "delta_r.*1|delta_r=1" ctl_pinn_resolution.md
rg -n "beta_v.*1|beta_v=1" ctl_pinn_resolution.md
rg -n "eta_c.*1|eta_c=1" ctl_pinn_resolution.md
rg -n "epsilon_L.*10.*-8" ctl_pinn_resolution.md
rg -n "lambda_IC.*1|lambda_IC=1" ctl_pinn_resolution.md

# Verify all exit 0 (parameters ARE grounded)
```

---

*Review completed: 2026-05-22*
*Mode: ultrathink — maximum depth*
*Supplements: REVIEW.md (prior adversarial review)*