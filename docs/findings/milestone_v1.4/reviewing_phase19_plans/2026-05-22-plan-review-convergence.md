# Plan Review Convergence: Phase 19 — Physics and Loss Contracts

**Date:** 2026-05-22
**Reviewer:** Plan-review-convergence (orthogonal physics + structural analysis)
**Plans Reviewed:** 19-01 (ctl_instruction), 19-02 (pinn_architecture formulas), 19-03 (pinn_architecture prose), 19-04 (divergence + verification + closure)
**Grounding Sources:** 19-CONTEXT.md (D-01..D-19), ctl_pinn_resolution.md (resolution doc), current spec files, Phase 17/18 locked decisions

---

## Executive Summary

Phase 19 plans are structurally well-organized and correctly decompose the work into 4 parallel-blocked plans. All 19 decisions from 19-CONTEXT.md are faithfully propagated. However, **5 findings** are identified across physics verification, factual accuracy, and structural verification quality. None are blockers to execution, but several should be addressed before plan execution begins.

| Severity | Count | Key Items |
|----------|-------|-----------|
| HIGH | 0 | — |
| MEDIUM | 4 | L_data factual error, warmup magnitude gap, verification regex fragility, L_L near-zero regime |
| LOW | 1 | s_min softening scope ambiguity |

---

## MEDIUM Findings

### M1: L_data "MSE" Factual Error in 19-02 Task 2

**Finding:** Plan 19-02 Task 2's warmup schedule table states: "L_data: Huber loss on position predictions, δ_r = 1 default (**resolution §8.2**). (Current spec uses MSE — change to Huber)."

The **current pinn_architecture.md:864** actually uses **MAE (L1 norm)**, not MSE:
> "Data Loss (L_data): Mean Absolute Error (MAE / L1 Norm) of the predicted positions"

The `ctl_instruction.md` text around line 332-337 also describes L1 norm usage. The plan's claim that the current spec uses MSE is **factually incorrect**.

**Impact:** The executor may become confused about which formulation to replace. The change to Huber is still valid and grounded in resolution §8.2, but the "before" description should be corrected to "MAE (L1)" to match the live spec.

**Suggested Fix:** Update 19-02 Task 2 text: "L_data: Huber loss on position predictions (current spec uses MAE/L1 — change to Huber per resolution §8.2)."

---

### M2: Warmup Schedule Magnitude Discrepancy Not Flagged

**Finding:** The new warmup schedule (19-02 Task 2, 19-CONTEXT.md D-07) caps all λ terms at 1.0 maximum:
```
λ_E^max(k) = λ_L^max(k) = {0 for k∈{0,1}; 10^(k-4) for k∈{2,3,4}; 1 for k∈{5,6}}
```

The **current** schedule (pinn_architecture.md:623) uses:
```
λ_E(k) = 10^(k-3)  → Stage 5: λ_E = 100, Stage 6: λ_E = 1000
```

This is a **3–4 order of magnitude reduction** for L_E at high curriculum stages. The plans correctly implement the resolution doc's new schedule but do not explicitly acknowledge the magnitude shift. While this is grounded in the resolution doc, the scale difference could affect training convergence and should be flagged for the user or Phase 21 verification awareness.

**Impact:** Plans are correct per resolution doc, but the magnitude shift should be explicitly noted in evidence packets or divergence inventory so Phase 21 VER-01 numeric probes understand the scale regime they're validating.

**Suggested Fix:** In 19-02 Task 2 (warmup schedule section) or 19-CODE-DIVERGENCE.md (19-04 Task 1), add a note: "New warmup caps λ_E/L_L at 1.0 vs current 100–1000 at late stages — magnitude shift documented for Phase 21 awareness."

---

### M3: Verification Regex Fragility in 19-04 Task 2

**Finding:** Plan 19-04 Task 2's AC-PHYS-02 structural check uses:
```bash
rg -n "u.*t/T" pinn_architecture.md
```
and
```bash
rg -n "sin.*2.*pi.*u.*cos.*2.*pi.*u" pinn_architecture.md
```

These regexes are extremely loose. `u.*t/T` matches any line containing both "u" and "t/T" anywhere, even in unrelated contexts. Conversely, if the spec uses LaTeX math notation (e.g., `$u = t/T$` or `\(u = t/T\)`), the regex may pass on a false match from prose text rather than the actual AD contract section.

Similarly, `rg -n "lambda_p.*L_phys.*mu_p"` for AC-PHYS-05 checks that the pseudo-ALM formula should NOT appear, but the regex could match explanatory text about why it was rejected (which contains those terms as a negative example).

**Impact:** Verification checks may pass on false positives or fail on false negatives, giving misleading PASS/FAIL results for the structural verification suite.

**Suggested Fix:** Tighten critical regexes to anchor on distinctive markers:
- Use `rg -n "Canonical autograd leaf"` instead of `rg -n "u.*t/T"` for the AD contract check
- Use `rg -n "\\lambda_p.*L_phys.*\\mu_p.*L_phys" --count` with `!` for the negative check (ensuring it matches zero times in the actual formula context)
- Add `--context` flags to verification commands so failures show surrounding text

---

### M4: L_L Angular Momentum Stability Scale Near-Zero Regime

**Finding:** Plan 19-02 Task 2 defines:
```
L_scale = ||L_0'|| + ε_L, ε_L = 10⁻⁸
```

For trajectories that start with near-zero total angular momentum (e.g., nearly collinear or near-head-on IC configurations), `||L_0'||` could be comparable to or smaller than `ε_L = 10⁻⁸`. In this regime, the normalization `L_scale ≈ ε_L` would amplify tiny angular-momentum drifts into large loss values, creating an artificially strong gradient signal for what is physically a degenerate case.

**Impact:** The plan doesn't address this edge case. While the relative-drift formulation is standard practice, the numerical-stability scale should be reviewed against the IC distribution to ensure it doesn't create pathological gradients for low-L_0 ICs.

**Suggested Fix:** This is not a blocker — the plan correctly implements resolution §8.6. However, add a note in the L_L subsection: "For ICs with ||L_0'|| ≈ 0, L_scale bottoms out at ε_L = 10⁻⁸. Consider whether the IC prescreening (Phase 18 / Stage 1) already rejects such configurations, or whether Phase 21 VER-01 probes should specifically validate low-L_0 behavior."

---

## LOW Findings

### L1: s_min Unsoftened Scope Ambiguity

**Finding:** Both 19-01 and 19-02 state that `s_min` remains the unsoftened geometric quantity `min_{i<j} ||r_i' − r_j'||`. The 19-CONTEXT.md D-06 says: "s_min (line 667) remains the unsoftened geometric quantity."

However, `s_min` appears in multiple places in the framework:
1. `ctl_instruction.md` Step 3 static-invariant V calculation (line 667 area)
2. `ctl_instruction.md` Step 2.5 scaling (`s_min_scale = median({r_char,j})`, line 594 area)
3. Potentially in curriculum staging gates or input-vector formulation references

The plans clearly state `s_min` stays unsoftened in the static-invariant V context (ctl_instruction.md Step 3), but do not explicitly address whether `s_min` references in other sections (Step 2.5, curriculum gates) need the same anti-pattern warning or cross-reference to the unsoftened guarantee.

**Impact:** Minor. The anti-pattern note in 19-01 Task 2 only covers the Step 3 context. Other `s_min` references in the spec remain unaddressed.

**Suggested Fix:** In 19-01 Task 2 (symbol renames), add: "Verify ALL s_min references across ctl_instruction.md — each should be either the unsoftened geometric quantity or explicitly noted as such. No s_min reference should imply softening."

---

## Gap Analysis: Missed Gaps

### GG1: No Gap Registered for M4 Ledger Pre-Phase-16 State

Plan 19-01 Task 1 reclassifies M4 from `NO` to `YES — EVID-05 required` with the note: "Phase 16 seed marked NO in error." This is a factual correction to a prior phase's ledger state. The plans handle this correctly by appending an audit note, but they do not discuss whether this correction should propagate to Phase 16's own documentation or whether the Phase 16 issue ledger itself should have a cross-reference back to this correction.

**Assessment:** The plans handle this adequately — the audit note in the ledger provides traceability. No additional gap needed.

### GG2: No Gap for L_IC Anchor at u=0 vs Network Input at τ=-1

The L_IC formula in Plan 19-02 Task 2 uses `r_θ'(0)` and `v_θ'(0)` — evaluated at `u = 0`. But the network input is `τ = 2u - 1`, so at `u = 0`, the network receives `τ = -1`. The plan does not explicitly state that L_IC evaluation requires the network forward pass at `τ = -1` (the first collocation point).

**Assessment:** This is implicit in the AD contract (three-layer separation), but should be made explicit in the L_IC subsection to avoid ambiguity for FUT-01 implementation. **Low severity** — the mathematical relationship is straightforward.

### GG3: No Coverage for η_gauge vs ε Cross-Reference

The 19-CONTEXT.md D-06 explicitly states: "η_gauge = 10⁻⁸ is a dimensionless rotation-gauge degeneracy tolerance — NOT a physics softening parameter and NOT tied to ε_train or ε_inv." The plans include this guard in 19-01 Task 2 and 19-02 Task 2 ("Verify η_gauge is NOT cross-referenced with ε_train or ε_inv").

**Assessment:** This is correctly covered. No gap.

---

## Structural Assessment

### Plan Decomposition (D-12)
The 4-plan decomposition is sound:
- **P01 + P02 (Wave 1, parallel):** Different files (ctl vs pinn_arch), no conflict. Correct.
- **P03 (Wave 2, blocked on P02):** Edits pinn_architecture.md prose, depends on formula skeleton from P02. Correct.
- **P04 (Wave 3, blocked on all):** Verification, divergence, closure. Correct.

### Dependency Graph
```
19-01 (Wave 1) ──┐
                  ├──→ 19-03 (Wave 2) ──→ 19-04 (Wave 3)
19-02 (Wave 1) ──┘
```
Dependencies are correctly specified. No circular dependencies.

### File Ownership
- ctl_instruction.md → 19-01 only ✓
- pinn_architecture.md → 19-02 (formulas) + 19-03 (prose) ✓
- Evidence packets → 19-01 (B-02, M4) + 19-02 (B-07, B-08, B-09) ✓
- Issue ledger → 19-01 + 19-02 + 19-04 ✓
- No pinn/*.py modified in any plan ✓

### Threat Models
All plans have threat models with appropriate mitigations. The HIGH threats are correctly identified and mitigated.

---

## Physics Verification Assessment

### B-02 Dimensional Analysis (19-01 Task 1)
The dimensional analysis proof is correct:
- Raw masses: D³ = G·T² (M_scale = 1)
- Mass fractions: D³ = G·M_tot·T² (M_scale = M_tot)
- The spec uses raw masses, so D = (G·T²)^(1/3) ≈ 4.6416 is correct.
- The issue doc's 6.694 corresponds to M_tot = 1 in natural units with mass fractions.
- **Verdict: Physics-correct.**

### B-09 Plummer Softening (19-02 Task 1)
- Plummer preserves ∇(1/r_safe) = r/r_safe³ — force/potential matched pair. ✓
- Additive does NOT: -∇(1/(||r||+ε)) = r/(||r||·(||r||+ε)²) ≠ r/(||r||+ε)³. ✓
- simulation_data check confirms no force-softening exists upstream. ✓
- **Verdict: Physics-correct.**

### M4 Constraint Counting (19-01 Task 1)
- 18 DOF (3 bodies × 3 pos × 2 for pos+vel). ✓
- 9 constraints (3 COM pos + 3 COM momentum + 3 SO(3)). ✓
- 9-dimensional reduced phase space (not 8). ✓
- Reframing as reconstructive gauge-fixed encoding is grounded in resolution §10.4. ✓
- **Verdict: Physics-correct.**

### ALM Rejection (19-02 Task 2)
- L_phys² on a nonnegative MSE produces a quartic residual. ✓
- This is NOT a standard equality-constrained augmented Lagrangian. ✓
- **Verdict: Physics-correct.**

### AD Contract (19-02 Task 2)
- Canonical leaf = u (no chain-rule factors). ✓
- τ-leaf path: v' = 2·dr'/dτ, a' = 4·d²r'/dτ². ✓
- Anti-pattern (r.sum()) correctly identified as VJP against all-ones covector. ✓
- Synthetic trajectory derivatives are symbolically correct. ✓
- **Verdict: Physics-correct.**

---

## Convergence Decision

**Result: 0 HIGH concerns, 4 MEDIUM, 1 LOW.**

The plans are structurally sound and physics-correct. The MEDIUM findings are factual inaccuracies, missing contextual notes, and verification quality issues — none of which block execution. No replan cycle is required.

**Recommended actions before execution:**
1. Fix L_data factual description (M1) — quick text edit
2. Add warmup magnitude note (M2) — one-line addition
3. Tighten verification regexes (M3) — improves reliability
4. Add L_L near-zero note (M4) — documentation only
5. Verify s_min scope (L1) — quick grep + confirm
