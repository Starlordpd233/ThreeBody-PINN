# Independent Review: Phase 19 Plans — Physics and Loss Contracts

**Reviewer:** GLM-5.1 (independent from all prior reviews)
**Date:** 2026-05-22
**Branch:** `milestone/v1.4`
**Documents reviewed:** 19-CONTEXT.md, 19-DISCUSSION-LOG.md, 19-01-PLAN.md through 19-04-PLAN.md
**Prior reviews consulted:** 5 (REVIEW.md, ce-doc-review, codex, phase19-plans-review, plan-review-convergence)

---

## Executive Summary

The Phase 19 plans correctly transcribe the resolution doc's physics decisions at the conceptual level. The 19 LOCKED decisions in 19-CONTEXT.md are sound and well-grounded. However, the plans contain **3 physics errors in spec-edit text**, **1 STOP-protocol violation**, and **6 execution risks** that will cause silent failures if not fixed before Wave 1 starts. Additionally, this review identifies **4 novel findings** not captured by any of the 5 prior reviews.

**Minimum fix before execution:** Address the 3 physics errors, surface the ε_H gap, and fix the Wave-1 parallel-write collision. Everything else can be patched during execution.

---

## Physics/Math Verification (Independent)

All core physics claims were independently verified against first-principles calculations:

| Claim | Verdict | Notes |
|-------|---------|-------|
| D³=G·T² with raw masses (B-02) | CORRECT | Masses cancel identically on both sides; no M_scale |
| Plummer preserves F=-∇V matched pair (B-09) | CORRECT | F = -m_i·m_j·r/r_safe³ from V = -m_i·m_j/r_safe |
| Additive does NOT match (B-09) | CORRECT (inequality) but STRAWMAN RHS | r/(r+ε)³ is not a standard force law |
| 18-3-3-3=9 constraint count (M4) | CONVENTION-DEPENDENT | Both 8 and 9 are defensible; see §M4 below |
| v'=2·dr'/dτ, a'=4·d²r'/dτ² (PHYS-02) | CORRECT | Chain rule through τ=2u-1 |
| ALM rejection: quartic residual (B-08) | CORRECT | Squaring nonnegative MSE is not standard ALM |

---

## Critical Findings

### C1. G' in Plummer formulas contradicts PHYS-01

**Severity:** CRITICAL (physics error in spec-edit text)
**Location:** 19-02-PLAN.md Task 2 (lines 286-290)
**Prior coverage:** Codex HIGH-03

Plan 19-02 writes the Plummer force as:
```
F_ij = G' · m_j · (r_j' - r_i') / r_{safe,ij}³
where G' is the dimensionless gravitational constant in the scaled system.
```

The raw-mass nondimensionalization D³=G·T² was chosen precisely so the scaled residual has **unit coefficient with no gravitational constant**. After substitution, Newton's equation becomes:

d²r'/du² = Σ m_j·(r'_j - r'_i)/||r'_j - r'_i||³

There is no G'. Including G' as a named variable contradicts PHYS-01's dimensional analysis lock, invites implementers to tune it independently (wrong), and creates the appearance of a free parameter where none exists.

**Fix:** Remove G' from both the force and potential snippets, or explicitly state once that G'=1 after raw-mass nondimensionalization.

---

### C2. L_L missing 1/3 normalization — 3× overweight angular momentum

**Severity:** CRITICAL (math error)
**Location:** 19-02-PLAN.md Task 2 (line 337)
**Prior coverage:** phase19-plans-review C-01

Plan specifies:
```
L_L = (1/N) Σ_n Σ_α Huber((L_θ,α'(u_n) - L_0,α') / L_scale, δ=1.0)
```

Resolution doc §8.6 specifies `1/(3·N_t)` — the `3` averages over spatial components {x,y,z}. The plan omits this factor. Since λ_L^max(k) = λ_E^max(k) in the warmup schedule, angular momentum conservation will dominate energy conservation by 3× during training. The warmup schedule was calibrated with the 1/3 factor present.

**Fix:** Change `(1/N)` to `1/(3·N)` in the L_L formula block.

---

### C3. ε_H = 10⁻⁸ silently invented — STOP-protocol violation

**Severity:** CRITICAL (governance)
**Location:** 19-02-PLAN.md Task 2 (line 314)
**Prior coverage:** ce-doc-review M7

The resolution doc §8.5 defines ε_H symbolically as a denominator floor but **never assigns a numerical value**. The plan picks 10⁻⁸ by silent analogy with ε_L. Per CLAUDE.md CRITICAL GOVERNANCE:

> "**Semantic** (physics derivations the source hedged on): **MUST surface**, never invent."

This is the textbook case the STOP protocol exists to prevent.

**Fix:** Surface as a 19-GAPS.md entry. Options: (A) ε_H=10⁻⁸ by analogy with ε_L, (B) ε_H=10⁻⁶ as safety margin over ε_train², (C) absolute-drift fallback for |H₀|<threshold ICs, (D) dataset filtering.

---

## Novel Findings (not in any prior review)

### N1. L_IC,v and L_L depend on correct AD — circular bootstrapping risk

**Severity:** HIGH
**Location:** 19-02-PLAN.md Task 2 (L_IC and L_L sections)

L_IC,v = MSE(v_θ'(0), v_0') requires v_θ'(0) = dr'/du at u=0, computed via autograd per PHYS-02. L_L uses L' = Σ m_i r'_i × v'_i where v'_i = dr'_i/du from the same AD computation. If AD is implemented incorrectly (e.g., the forbidden `r.sum()` anti-pattern), both L_IC,v and L_L are computed from wrong velocities. The IC velocity anchor would then train the network toward wrong velocities, and L_L would penalize deviations from a wrong angular momentum — actively reinforcing the AD error.

This creates a **circular bootstrapping dependency**: PHYS-02 correctness gates L_IC,v and L_L training signal quality. No plan task or verification step detects this cross-contract failure mode.

**Fix:** Add a note in the L_IC and L_L spec sections: "The velocity v'_i = dr'_i/du and angular momentum L' = Σ m_i r'_i × v'_i both depend on correct componentwise AD per the PHYS-02 contract (§5.x). If AD is wrong, these terms train toward wrong physical quantities." Consider adding a Phase 21 VER-04 probe that checks L_IC,v convergence is consistent with L_data convergence (both should improve together; divergence indicates AD issues).

---

### N2. ε_L = η_gauge = 10⁻⁸ numerical coincidence undocumented

**Severity:** LOW
**Location:** Cross-reference between Phase 18 D-14 and 19-02 Task 2

Phase 18's η_gauge = 10⁻⁸ (rotation-gauge tolerance) and Phase 19's ε_L = 10⁻⁸ (angular-momentum stability scale) share the same numerical value but serve entirely different purposes. A future reader could confuse them, especially since both relate to angular quantities. The plan says they're "distinct symbol families" but doesn't note the coincidence.

**Fix:** Add one sentence in the L_L section: "Note: ε_L = 10⁻⁸ coincides numerically with η_gauge = 10⁻⁸ (Phase 18 D-14, rotation-gauge tolerance) but serves a different purpose — ε_L is a loss-term stability scale, η_gauge is a geometry tolerance."

---

### N3. Warmup schedule undefined for k > 6

**Severity:** LOW
**Location:** 19-02-PLAN.md Task 2 and 19-CONTEXT.md D-07

The warmup schedule λ_E^max(k) = λ_L^max(k) = {0 for k∈{0,1}; 10^(k-4) for k∈{2,3,4}; 1 for k∈{5,6}} is defined for exactly 7 curriculum stages. If the curriculum has more stages (k≥7), the schedule is undefined. The plan doesn't address extrapolation.

**Fix:** Add: "For k > 6, λ_E^max = λ_L^max = 1 (saturates at the k=5/6 value)."

---

### N4. L_L angular momentum cross-contract dependency should be explicit

**Severity:** MEDIUM
**Location:** 19-02-PLAN.md Task 2 (L_L section)

The angular momentum L' = Σ_i m_i r'_i × v'_i requires AD-derived velocities v'_i = dr'_i/du from the PHYS-02 contract. This cross-contract dependency is implicit but not stated. An executor implementing L_L without reading PHYS-02 might use wrong velocity computation.

**Fix:** Add to the L_L formula block: "where v'_i = dr'_i/du is computed via the componentwise AD contract in §5.x (PHYS-02)."

---

## Factual Errors in Evidence Packets

### F1. B-02 says M_tot=1 but 6.694 requires M_tot=3

**Prior coverage:** Codex HIGH-02

19-01 Task 1 line 163: "The issue doc's 6.694 value corresponds to M_tot=1 (in natural units) and mass fractions." This is factually wrong. D = (G·M_tot·T²)^(1/3) = 6.694 requires M_tot=3 with T≈10, G=1: (3·100)^(1/3) = 300^(1/3) ≈ 6.694. With M_tot=1, D = T^(2/3) = 4.6416 — same as raw mass.

**Fix:** Replace "M_tot=1" with "physical total mass M_tot=3 in natural units; the mass-fraction convention normalizes m_j' = m_j/M_tot."

### F2. B-09 §5 additive-force derivation uses a strawman

**Prior coverage:** ce-doc-review M8

The plan rejects additive softening by showing -∇(1/(r+ε)) ≠ r/(r+ε)³. The LHS is correct (the actual gradient of the additive potential). The RHS r/(r+ε)³ is a strawman — no published softening method produces this cubic-denominator force. The real issue is that the pre-Phase-19 spec paired additive potential with unsoftened Newtonian force (or a mismatched force expression), breaking F=-∇V.

**Fix:** Rewrite B-09 §5 to state: the additive potential V=-1/(r+ε) yields valid force F=-r̂/(r+ε)², but the pre-Phase-19 spec paired this with a different force expression, breaking the matched pair. Plummer is preferred because the matched pair is automatic from a single r_safe definition.

### F3. M4 §5/§9 overclaims "9 is uniquely correct"

**Prior coverage:** ce-doc-review S7

The plan asserts "9 constraints, yielding a 9-dimensional reduced phase space (not 8). The issue doc's arithmetic is correct." Both 8 and 9 are defensible under different conventions (see §M4 analysis above). The resolution doc's key insight — constraint counting is irrelevant under Jacobi IC13 — is the correct framing.

**Fix:** Rewrite M4 §5 to acknowledge convention dependence and reframe §9: "Both source positions are partially correct depending on convention; both are wrong on relevance under Jacobi-state IC13."

---

## Execution Risks (confirming prior reviews)

These were identified by prior reviews and confirmed by independent analysis:

| Risk | Source | Impact if unfixed |
|------|--------|-------------------|
| Wave-1 parallel ledger writes collide | ce-doc M5, codex HIGH-01 | Git conflicts corrupt ledger |
| Cross-ref §-numbers unstable across waves | ce-doc M1, M6 | Broken cross-refs at phase exit |
| D-14 Markdown table annotation breaks table | ce-doc M2 | Issue Doc format corruption |
| Verification regexes non-functional | ce-doc M3/M4/S4, REVIEW M2 | Wrong specs pass verification |
| P04 verification too permissive | codex HIGH-06 | VERIFIED on non-passing checks |
| L_data §3.1 not rewritten (MAE→Huber) | codex HIGH-04, convergence M1 | Spec self-contradicts after execution |
| Causal-weight clipping omitted | codex HIGH-05, REVIEW M1 | Silent underflow zeroes physics loss |

---

## Recommended Actions

### Must fix before Wave 1 starts:

1. **C1:** Remove G' from Plummer formulas (or pin G'=1)
2. **C2:** Fix L_L formula: (1/N) → 1/(3·N)
3. **C3:** Surface ε_H as 19-GAPS.md entry per STOP protocol
4. **F1:** Fix B-02 M_tot=1 → M_tot=3
5. **Serialize Wave-1 ledger writes** (or use delta-file strategy)

### Should fix before execution:

6. **F2:** Rewrite B-09 §5 additive-force derivation
7. **F3:** Soften M4 §5/§9 convention-dependent claims
8. **Fix verification regexes** to be LaTeX-aware and non-tautological
9. **Lock D-14 annotation format** (HTML comment recommended)
10. **Add L_data §3.1 rewrite** to P02 Task 2
11. **Add causal-weight clipping clause**
12. **Use section-agnostic cross-references** in P01 (avoid §3.1/3.2/3.3 numbering)

### Can fix during execution:

13. **N1:** Add AD-dependency note to L_IC,v and L_L sections
14. **N2:** Document ε_L/η_gauge numerical coincidence
15. **N3:** Add warmup schedule extrapolation for k>6
16. **N4:** Add L_L cross-contract AD dependency note
17. **Tighten P04 verification** to require per-AC PASS markers

---

## Physics Verdict

The resolution doc's physics decisions — raw-mass scaling, Plummer matched pair, pseudo-ALM rejection, AD leaf semantics, constraint-counting reframing — are **mathematically sound**. The 19 LOCKED decisions in 19-CONTEXT.md are correctly grounded. The problems in the plans are in the **transcription details** (G' ghost variable, missing 1/3 factor, invented numerical defaults) and **process mechanics** (regex bugs, parallel-write collisions, dangling cross-references). None of these require re-litigating the physics.

---

*Reviewed by GLM-5.1, independent from all prior review agents.*
*Resolution doc verified against: ctl_pinn_resolution.md §3.1-3.2, §7.1-7.3, §8.1-8.8, §10.4*
*All dimensional analyses and force derivations independently recomputed.*
