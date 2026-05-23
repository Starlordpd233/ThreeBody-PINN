# Phase 19 Plans Review: Physics and Loss Contracts

**Reviewed:** 2026-05-22
**Documents reviewed:**
- `19-CONTEXT.md` (19 locked decisions, 5 findings, 6 requirements)
- `19-01-PLAN.md` (ctl_instruction.md edits, B-02/M4 evidence packets)
- `19-02-PLAN.md` (pinn_architecture.md formula edits, B-07/B-08/B-09 evidence packets)
- `19-03-PLAN.md` (HNN prose cleanup, P2 ALM appendix, cross-reference validation)
- `19-04-PLAN.md` (code divergence inventory, structural verification, closure)

**Reviewers:** coherence-reviewer, feasibility-reviewer, adversarial-document-reviewer (physics/math grounding)

---

## Executive Summary

The Phase 19 plans are well-structured, internally consistent, and correctly adjudicate all five findings against the resolution doc. The wave decomposition (P01+P02 parallel, P03 blocked on P02, P04 blocked on all) is sound. However, **three critical issues** were found that would silently corrupt the framework specs if executed as written:

1. The L_L angular-momentum loss formula is missing a `1/3` normalization factor (3x overweighting vs resolution doc)
2. The L_IC anchor loss uses ambiguous `MSE()` instead of the resolution doc's explicit `1/3` per-body average
3. P04's verification regex has unescaped pipe characters that will cause the verify command to always fail

---

## Critical Findings

### C-01: L_L normalization factor missing -- 3x overweighting angular momentum

**Severity:** Critical (physics/math error)
**Location:** `19-02-PLAN.md` Task 2, "Add L_L term" (line 337)
**Confidence:** HIGH

The plan specifies:
```
L_L = (1/N) Σ_n Σ_α Huber((L_θ,α'(u_n) - L_0,α') / L_scale, δ=1.0)
```

The resolution doc §8.6 (lines 958-961) specifies:
```
L_L = 1/(3·N_t) Σ_n Σ_{α∈{x,y,z}} Huber_1.0((L_θ,α'(u_n) - L_0,α') / L_scale)
```

The plan writes `(1/N)` where the resolution doc writes `1/(3·N_t)`. The `3` in the denominator averages over the three spatial components {x, y, z}. The plan omits this factor.

**Consequence:** L_L is 3x larger than the resolution doc intends. Since the warmup schedule (§8.7) applies identical `λ_L^max(k)` to L_L as to L_E, angular momentum conservation will dominate energy conservation during training. The warmup schedule was calibrated with the 1/3 factor present.

**Fix:** Change `(1/N)` to `1/(3·N)` in the L_L formula block.

---

### C-02: L_IC anchor uses ambiguous MSE -- potential 3x deviation from resolution doc

**Severity:** Critical (physics/math ambiguity)
**Location:** `19-02-PLAN.md` Task 2, "Add L_IC term" (line 327)
**Confidence:** MEDIUM

The plan specifies:
```
L_IC,r = MSE(r_θ'(0), r_0')
```

The resolution doc §8.3 (lines 869-870) specifies:
```
L_IC,r = (1/3) Σ_{i=1}^{3} ||r_θ,i'(0) - r_i'(0)||_2^2
```

The resolution doc uses an explicit `1/3` factor averaging over 3 bodies, where each term is a 3D squared norm. The plan's `MSE()` is ambiguous:
- PyTorch's `F.mse_loss` with default `reduction='mean'` on a `(3,3)` tensor divides by 9 (total elements), yielding `(1/9) Σ ||...||²`
- The resolution doc divides by 3 (number of bodies), yielding `(1/3) Σ ||...||²`
- These differ by a factor of 3

**Consequence:** If implemented naively with PyTorch's default MSE, the IC anchor is 3x weaker than intended. Since `λ_IC = 1` with ablation range `[0.1, 10]`, this is recoverable via tuning, but out-of-the-box behavior will differ from the resolution doc's design.

**Fix:** Replace `MSE(r_θ'(0), r_0')` with the explicit formula: `(1/3) Σ_{i=1}^{3} ||r_θ,i'(0) - r_i'(0)||_2^2`. Same for the velocity anchor.

---

### C-03: P04 Task 2 verification regex has unescaped pipes -- command always fails

**Severity:** Critical (execution blocker)
**Location:** `19-04-PLAN.md` Task 2 verify section (line ~343)
**Confidence:** HIGH

The negation pattern in P04's Task 2 verify command:
```
! rg -n "^| B-02 .*IN_PROGRESS|^| B-02 .*FIX_APPLIED|..."
```

In `rg` (ERE mode), `|` is the alternation operator. The pattern `^| B-02 .*IN_PROGRESS` parses as: alternation between `^` (matches every line) and ` B-02 .*IN_PROGRESS`. Since `^` matches every line, the pattern always matches, and `! rg` always fails.

**Contrast:** P01/P02 correctly use `^\\|` (escaped pipe) for the same kind of table-row matching.

**Fix:** Replace all `^| ` with `^\\| ` in the negation pattern:
```
! rg -n "^\\| B-02 .*IN_PROGRESS|^\\| B-02 .*FIX_APPLIED|..."
```

---

## Major Findings

### M-01: B-02 evidence packet uses misleading "M_scale" reasoning

**Severity:** Major (mathematical reasoning error in evidence packet)
**Location:** `19-01-PLAN.md` Task 1, B-02.md §5 instructions (line 163)
**Confidence:** HIGH

The plan instructs the evidence packet to state:
> "the dimensionless form requires D^3/(G·T^2·M_scale) = 1 where M_scale is whatever mass unit appears in the dimensionless masses"

This is incorrect. With raw masses, the masses cancel identically on both sides of Newton's equation. There is no M_scale. The clean derivation (from resolution doc §3.1) is:
1. Substitute r=D·r', t=T·u into m_i d²r_i/dt² = G Σ m_j(r_j-r_i)/||r_j-r_i||³
2. Left side: m_i (D/T²) d²r_i'/du²
3. Right side: G Σ m_j D(r_j'-r_i') / (D³||r_j'-r_i'||³) = (G/D²) Σ m_j(r_j'-r_i')/||r_j'-r_i'||³
4. Divide both sides by m_i D/T²: d²r_i'/du² = (GT²/D³) Σ m_j(r_j'-r_i')/||r_j'-r_i'||³
5. For coefficient 1: D³ = GT²

The final conclusion is correct, but the intermediate reasoning introduces a nonexistent quantity. The M_scale concept only applies under the mass-fraction convention, which is the alternative being rejected.

**Fix:** Replace the §5 instructions with the resolution doc's clean derivation (no M_scale). The mass-fraction alternative can be explained as a separate "what-if" paragraph.

---

### M-02: Bare `ε` sweep instructions risk false-positive renames

**Severity:** Major (potential spec corruption)
**Location:** `19-01-PLAN.md` Task 2 action (line ~303), `19-02-PLAN.md` Task 2 action (line ~436)
**Confidence:** MEDIUM

The plans instruct the executor to "replace all `ε_soft` / `epsilon_soft` / bare `ε` (in softening contexts) with `ε_inv` or `ε_train`." The bare `ε` sweep is a manual judgment call. In `ctl_instruction.md`:
- Line 669: `ε = 10⁻¹⁰` in softening context → should become `ε_inv` ✓
- Line 933: `ε = 10⁻¹⁰` in "Numerical Implementation" → same softening epsilon, should rename ✓
- Line 994: `σ_z + 10⁻⁸` in normalization → NOT softening, do NOT rename
- Line 1109: `ε = 1e-8` in ALM context → NOT softening, do NOT rename

The verification commands only check for `epsilon_soft|eps_soft` (the old explicit name), not bare `ε`, so the risk is in the action instructions, not verification.

**Fix:** Clarify that line-number-anchored edits are primary and the `rg` sweep is supplementary. The executor should not blindly rename every bare `ε`.

---

## Minor Findings

### m-01: Cross-plan total-loss coordination is implicit

**Location:** P01 line 49, P02 line 55
Both plans reference "the exact formula from 19-CONTEXT.md D-07" but provide slightly different presentation formats (P01: prose block with optimizer semantics; P02: structured list with warmup details). P03 Task 2 validates cross-references reactively. The mechanism is adequate but could be stronger with a shared canonical markdown block.

### m-02: P02 Task 1 and Task 2 are independent but sequenced

P02 Task 1 (evidence packets) and Task 2 (spec edits) touch different files. They could theoretically run in parallel, but sequential execution is a conservative choice that avoids confusion.

### m-03: P03 Task 2 cross-reference gap handling is read-only

P03 Task 2 verifies ctl_instruction.md cross-references but says "if any cross-reference is wrong or missing, note it but do NOT edit ctl_instruction.md." This means cross-reference errors found in Wave 2 cannot be fixed without re-running P01 or opening a new task.

---

## Verified Claims (No Issues)

All of the following physics/math claims were verified against the resolution doc and first-principles calculations:

| Claim | Verdict | Source |
|-------|---------|--------|
| D=(GT²)^(1/3) dimensional analysis with raw masses | VERIFIED | Resolution §3.1-3.2 |
| Plummer softening: V = -m_i m_j / r_safe gives F = m_i m_j · r / r_safe³ | VERIFIED | Resolution §7.1 |
| Additive softening: V = -m_i m_j / (r+ε) does NOT give F = r/(r+ε)³ | VERIFIED | Resolution §7.1 |
| Causal weighting w_n = exp(-η_c Σ stopgrad(R̄_m)) prevents adversarial dynamics | VERIFIED | Resolution §8.4 |
| M4 arithmetic: 18 - 3 COM - 3 P - 3 SO(3) = 9 | VERIFIED | Resolution §10.4 |
| ALM rejection: squaring nonnegative MSE produces quartic, not standard ALM | VERIFIED | Resolution §8.8 |
| Warmup schedule: I_warm, λ_E^max(k), λ_L^max(k), linear warmup | VERIFIED | Resolution §8.7 |
| η_gauge (Phase 18) is distinct from ε_train/ε_inv | VERIFIED | Phase 19 D-06 |

---

## Structural/Process Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Wave dependencies (P01∥P02, P03→P02, P04→all) | CORRECT | Different-file parallelism confirmed |
| File ownership (P01=ctl, P02/P03=pinn) | CORRECT | No cross-ownership conflicts |
| Evidence-packet-first ordering | CORRECT | Task 1 (packets) before Task 2 (spec edits) in both P01 and P02 |
| Ledger transitions (PENDING→IN_PROGRESS→FIX_APPLIED→VERIFIED) | CORRECT | Consistent across all 4 plans |
| Line number anchors | STABLE | All 13 cited line numbers verified against current spec files |
| D-14 Issue Doc annotation format | CONSISTENT | Same one-line format across all 5 findings |
| D-16 M4 ledger reclassification | CORRECT | Factual correction, not schema invention |
| P04 AC-PHYS structural checks | COMPREHENSIVE | All 6 AC checks cover the required markers |

---

## Recommendations

**Must-fix before execution (Critical):**
1. Fix L_L formula: `(1/N)` → `1/(3·N)` in 19-02-PLAN.md Task 2
2. Fix L_IC formula: `MSE(...)` → explicit `(1/3) Σ ||...||²` in 19-02-PLAN.md Task 2
3. Fix P04 regex: `^|` → `^\\|` in 19-04-PLAN.md Task 2 verify

**Should-fix before execution (Major):**
4. Fix B-02 evidence packet §5: remove M_scale, use clean derivation from resolution §3.1 in 19-01-PLAN.md Task 1
5. Clarify bare `ε` sweep: line-number anchors are primary, rg is supplementary in 19-01/19-02 Task 2

**Nice-to-have (Minor):**
6. Consider a shared canonical total-loss markdown block for P01/P02 coordination
7. Note that P03 Task 2 cross-reference gaps in ctl_instruction.md require a new task to fix

---

## Gap Register Check

Per the CRITICAL GOVERNANCE STOP protocol: no new gaps were identified that require user instruction. All findings above are either:
- Math/physics errors in the plan text that can be mechanically corrected (C-01, C-02, M-01)
- Execution bugs in regex commands that can be mechanically fixed (C-03)
- Clarification needs in action instructions (M-02)

None of these require semantic, schema, or cross-phase reframing decisions. The 19 locked decisions (D-01 through D-19) remain sound and correctly grounded in the resolution doc.

---

*Reviewed by: ce-coherence-reviewer, ce-feasibility-reviewer, ce-adversarial-document-reviewer*
*Resolution doc verified against: `ctl_pinn_resolution.md` §3.1-3.2, §7.1-7.2, §8.1-8.8, §10.4*
