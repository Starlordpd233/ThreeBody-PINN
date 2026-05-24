# Phase 19 Meta-Plan Completeness Audit

**Date**: 2026-05-23
**Auditor**: Claude (deepseek-v4-pro), multi-agent systematic cross-reference
**Scope**: Verify that `2026-05-22-phase19-plan-repair-meta-plan.md` completely and accurately synthesized all findings from 8 independent review documents, and that the repaired Phase 19 plans correctly implement all prescribed fixes.

## Executive Summary

**Verdict: The meta plan is sound and produced correctly repaired plans. Three higher-concern items and approximately ten lower-concern documentation enhancements were not fully addressed, but none require plan re-repair.**

The meta plan successfully deduplicated and addressed ~75 findings across 5 repair units. All critical physics errors (G' reintroduction, L_L normalization missing 1/3 factor, L_IC MSE ambiguity, epsilon_H silent invention) were correctly identified and repaired. All governance violations (no gap register, STOP-protocol "log and continue" wording, parallel shared-artifact write conflicts) were properly resolved. All verification defects (unescaped regex pipes, token-presence-only checks, ASCII-vs-LaTeX grep mismatches) were fixed with strict structural verification.

Agent verification of the 7 repaired planning files confirms **100% pass** on all repair-unit checks and all 6 meta-plan `rg` criteria.

Three higher-concern gaps in the meta plan's coverage were identified:
1. L_E energy denominator degeneracy at |H_0| → 0 (symmetric to the L_L near-zero case that was addressed)
2. η_c = 1 density scaling with N_t (causal weights vanish for large collocation counts)
3. AD bootstrapping detection mechanism (if AD is wrong, L_IC,v and L_L both train toward wrong physics with no guard)

None are blocking — all can be addressed as documentation addenda during execution or deferred to Phase 21.

---

## 1. Audit Methodology

### 1.1 Source Documents

**8 independent review documents** (all dated 2026-05-22):

| # | File | Reviewer | Severity Framework |
|---|------|----------|-------------------|
| R1 | `REVIEW.md` | Multi-persona adversarial | 2 BLOCKING, 5 MAJOR, 7 MINOR |
| R2 | `phase19-plans-review.md` | Physics/loss contracts | 3 CRITICAL, 2 MAJOR, 3 MINOR |
| R3 | `ce-doc-review-phase19-synthesis.md` | 5-persona synthesis | 1 P0→P1, 4 P1, 8 P2 |
| R4 | `2026-05-22-claude-ce-doc-review-phase-19-plans.md` | Claude Opus 4.7 | 8 MUST_FIX, 10 SHOULD_FIX, 7 CONSIDER, 6 FYI |
| R5 | `2026-05-22-codex-phase-19-plan-review.md` | Codex inline review | 6 HIGH, 2 MEDIUM, 1 LOW |
| R6 | `2026-05-22-glm-independent-phase-19-plan-review.md` | GLM-5.1 independent | 3 CRITICAL, 4 NOVEL, 3 FACTUAL_ERRORS |
| R7 | `2026-05-22-plan-review-convergence.md` | Orthogonal convergence | 0 HIGH, 4 MEDIUM, 1 LOW |
| R8 | `2026-05-22-ultrathink-phase19-grounding-verification.md` | Numerical grounding | 3 Execution Risks, 2 Cross-Ref Gaps |

**Meta plan**: `2026-05-22-phase19-plan-repair-meta-plan.md` (5 repair units)

**Repaired artifacts** (7 files in `.planning/phases/19-physics-and-loss-contracts/`):
`19-CONTEXT.md`, `19-GAPS.md`, `19-01-PLAN.md`, `19-02-PLAN.md`, `19-03-PLAN.md`, `19-04-PLAN.md`, `19-DISCUSSION-LOG.md`

### 1.2 Method

Five parallel agents each read their assigned review documents plus the meta plan, extracted every individual finding, and cross-referenced each finding against the meta plan's 5 repair units and Gap Handling / Rejected Findings sections. Findings were classified as ADDRESSED, EXPLICITLY_REJECTED, DUPLICATE, PARTIALLY_ADDRESSED, or POTENTIALLY_MISSED. A sixth agent verified the repaired plans contain every prescribed fix.

### 1.3 Classification Rules

- **ADDRESSED**: Finding has a corresponding repair in at least one meta-plan unit
- **EXPLICITLY_REJECTED**: Listed in Rejected Findings with justification
- **DUPLICATE**: Same issue independently found by multiple reviewers, addressed once
- **PARTIALLY_ADDRESSED**: Some aspect handled, another aspect missed
- **POTENTIALLY_MISSED**: No corresponding meta-plan unit or rejection addresses it

---

## 2. Complete Findings Inventory

### 2.1 Summary Statistics

| Source | Total Findings | ADDRESSED | REJECTED | PARTIAL | POTENTIALLY MISSED |
|--------|---------------|-----------|----------|---------|-------------------|
| R1: REVIEW.md | 19 | 13 | 2 | 1 | 3 |
| R2: phase19-plans-review.md | 8 | 7 | 0 | 0 | 0 |
| R3: ce-doc-review-synthesis | 18 | 12 | 0 | 0 | 0 |
| R4: claude-ce-doc-review | 32 | 20 | 2 | 1 | 9 |
| R5: codex review | 9 | 9 | 0 | 0 | 0 |
| R6: GLM independent | 17 | 12 | 3 | 1 | 0 |
| R7: plan-review-convergence | 22 | 16 | 3 | 0 | 3 |
| R8: ultrathink grounding | 16 | 10 | 1 | 1 | 1 |
| **Total (deduplicated)** | **~100** | **~75** | **~6** | **~4** | **~13** |

Note: Counts are approximate due to cross-review duplication. Many findings appear in 3-5 reviews.

### 2.2 Critical/Blocking Findings — All Resolved

| Finding | Reviews That Found It | Resolution |
|---------|----------------------|------------|
| epsilon_H = 10⁻⁸ silently invented (STOP violation) | R1, R3, R4, R6, R8 | GAP-19-01 created; epsilon_H symbolic in P02 |
| No 19-GAPS.md exists | R1, R3, R4 | Created with GAP-19-01; milestone index updated |
| Cross-plan total-loss deadlock (P03 can't fix ctl_instruction.md) | R1, R4, R5 | P03 uses closure-safe routing; D-07 is authority |
| P01/P02 parallel writes collide on shared files | R3, R4, R5, R6, R8 | Serialized; shared-artifact writes moved to coordination |
| Verification regex has unescaped pipes | R2, R4, R5 | Fixed to grouped pattern `^\| (B-02\|...)` |
| L_L normalization missing 1/3 factor | R2, R3, R6 | Fixed to 1/(3N_t) |
| L_IC uses ambiguous MSE() | R2, R3, R6 | Replaced with explicit (1/3) Σ formulas |
| G' reintroduced in Plummer force | R3, R5, R6 | Removed; raw-mass convention absorbs G |
| L_data §3.1 not rewritten MAE→Huber | R5, R7 | Explicit Huber rewrite with δ_r=1 added |
| Causal-weight clipping omitted | R4, R5 | Non-numeric clipping language added |

### 2.3 Convergence Review Error Corrected

R7 (`plan-review-convergence.md`) and R1 (`REVIEW.md` structural assessment) both claimed P01/P02 Wave-1 parallelism was safe ("different files, no conflict"). This was incorrect — both plans write to shared `16-ISSUE-LEDGER.md` and the Issue Doc. The meta plan explicitly corrected this error, adding serialization rules in Units 1, 2, and 3.

---

## 3. Potentially Missed Findings

### 3.1 Higher Concern (3 items)

#### PM-01: L_E Energy Denominator Degeneracy at |H_0| → 0

- **Source**: R4 (claude review S5), R8 (ultrathink)
- **Severity in original review**: SHOULD_FIX
- **Category**: physics edge case

The meta plan's Gap Handling Rules address the L_L near-zero angular momentum case:

> "Zero or near-zero L_0': do not change L_scale = ||L_0'|| + ε_L. Surface only if adding prescreening, formula changes, or Phase 21 low-L_0 probe scope."

But there is no parallel provision for the L_E energy denominator. Both losses share the same structure:

```
L_E:  ΔH_n = (H_θ'(u_n) - H_0') / max(ε_H, |H_0'|)
L_L:  ΔL_n = (L_θ'(u_n) - L_0') / (||L_0'|| + ε_L)
```

For marginally-bound ICs with |H_0| ≈ 0, the denominator collapses to ε_H ≈ 10⁻⁸, amplifying absolute drift by 10⁸ — symmetric to the L_L case. The L_L half was addressed; the L_E half was overlooked.

**Recommendation**: Add symmetric Gap Handling language for L_E during P02 execution, or note in 19-GAPS.md that both denominators share the same edge-case behavior and the Huber cap is the shared mitigation.

**Impact**: LOW. The Huber loss caps per-component contribution at linear growth for both terms. The edge case is symmetric, and the mitigation (Huber cap) is identical.

---

#### PM-02: η_c Density Scaling with N_t

- **Source**: R4 (claude review S6)
- **Severity in original review**: SHOULD_FIX
- **Category**: physics parameter scaling

The causal weight formula with η_c=1:

```
w_n = exp(-η_c · Σ_{m<n} stopgrad(R̄_m))
```

For N_t = 100 collocation points and typical residual magnitudes, the final weight is `w_N_t ≈ e^(-100) ≈ 10⁻⁴⁴` — effectively zero. The same η_c=1 with N_t=10 gives `w_N_t ≈ 4·10⁻⁵` — small but recoverable.

The meta plan added non-numeric clipping language ("the exponent must be clipped to avoid underflow") but does not address whether η_c=1 is the right value across different N_t densities. The routing section (D.16) recommended adding a scaling note, but no implementation unit mandates it.

**Recommendation**: During P02 execution, add a brief note that η_c=1 was chosen for the default curriculum (N_t ~ 50-100), and that different collocation densities may require adjusting η_c or the clipping threshold. Defer numeric tuning to Phase 21.

**Impact**: LOW-MEDIUM. The non-numeric clipping language provides partial mitigation. If clipping is implemented and η_c=1 causes all late-time weights to clip to the floor, the causal weighting becomes a step function rather than exponential decay — still functional but losing the intended gradual horizon.

---

#### PM-03: AD Bootstrapping Detection Gap

- **Source**: R6 (GLM N1)
- **Severity in original review**: HIGH (novel finding)
- **Category**: verification_defect (cross-contract failure mode)

GLM's most consequential novel finding: L_IC,v = MSE(v_θ'(0), v_0') and L_L both depend on AD-derived velocities from the PHYS-02 contract. If AD is implemented incorrectly (e.g., forbidden `r.sum()` anti-pattern), both loss terms compute wrong velocities:

1. L_IC,v trains the IC velocity anchor toward wrong target velocities
2. L_L penalizes deviations from wrong angular momentum
3. Both actively reinforce the AD error with no detection mechanism

The meta plan's Unit 3 adds a documentation note:

> "State that v'_theta used by L_IC,v and L_L comes from the PHYS-02 componentwise AD contract."

This documents the dependency but does not create a verification guard. The suggested Phase 21 VER-04 probe (checking L_IC,v convergence consistency with L_data convergence) was implicitly precluded by Unit 5's rule: "Do not invent Phase 21 numeric thresholds."

**Recommendation**: Document this as a known Phase 21 verification concern in 19-CODE-DIVERGENCE.md or 19-GAPS.md. The detection mechanism belongs in Phase 21 VER-04 (numeric validation), but the risk should be flagged for Phase 21 planners.

**Impact**: MEDIUM (latent, not active). If PHYS-02 AD is implemented correctly (as specified by the contract), this is moot. The risk is that Phase 19 specifies the contract correctly but Phase 21 implements it incorrectly — and the cross-contract dependency means a single AD bug poisons two loss terms instead of one.

---

### 3.2 Lower Concern — Documentation Enhancements

These CONSIDER/FYI/MINOR-severity items from the original reviews were not explicitly addressed by any meta-plan repair unit. The meta plan's routing section acknowledged many as "during execution" or "leave for Phase 21" items. None affect physics correctness.

| ID | Finding | Original Severity | Recommendation |
|----|---------|-------------------|----------------|
| PM-04 | L_IC MSE vs L_data Huber inconsistency justification missing | MAJOR (R1 M4), MINOR (R8 CR2) | Add one-line rationale: IC values are exact from deterministic preprocessing; MSE's quadratic penalty enforces hard IC match |
| PM-05 | Hamiltonian stay/go criteria for P03 HNN prose cleanup | MINOR (R1 m2), semantic gap (R1 GAP-19-03) | Add framing sentence: "Throughout this document, 'Hamiltonian' refers to the analytic energy function H_ε = T + V_ε, not to an HNN architecture" |
| PM-06 | 1-body/3-component AD test vs 3-body/9-component system | MINOR (R1 m3) | Note in AD listing: "The 1-body test verifies contract mechanics; Phase 21 VER-04 validates 3-body correctness" |
| PM-07 | 19-04-SUMMARY.md naming vs Phase 18 per-wave convention | MINOR (R1 m6) | Acceptable as-is; Phase 19 uses different plan structure (4 plans, 3 waves) |
| PM-08 | Warmup magnitude shift (3-4 OOM reduction) not flagged | MEDIUM (R7 M2) | Add one-line note in 19-CODE-DIVERGENCE.md or evidence packets |
| PM-09 | L_IC anchor at u=0 vs network input at τ=-1 implicit | LOW (R7 GG2) | Add explicit statement in L_IC subsection |
| PM-10 | "Or equivalent" hedge for M4 replacement text boundary | SHOULD_FIX (R4 S11) | Replace with exact match instruction during P01 execution |
| PM-11 | D ≈ 4.6416 assumes T=10 in natural units, never stated | CONSIDER (R4 Co1) | Document T=10 assumption in 19-CONTEXT.md or ctl_instruction.md |
| PM-12 | Linear momentum conservation absence not documented | CONSIDER (R4 Co2) | Add note: L_P enforced structurally by COM projection head, not via loss term |
| PM-13 | B-09 "category error" framing partially strawmans issue doc | CONSIDER (R4 Co4) | Soften language during P02 execution per routing recommendation |
| PM-14 | simulation_data anchor pre-flight check not enforced | CONSIDER (R4 Co6) | Add pre-task `rg` verification that cited line ranges exist |
| PM-15 | ε_L = 10⁻⁸ magnitude justification thin | MINOR (R1 m4) | Add one-line justification: "10⁻⁸ balances float32 epsilon (~10⁻⁷) safety margin against negligible perturbation to O(1) angular momenta" |
| PM-16 | Numerical defaults provenance table missing | SHOULD_FIX (R4 S8) | Add subsection to B-07/B-08/B-09 evidence packets |
| PM-17 | Title "Hamiltonian Regularization" fate undecided | FYI (R4 Fy1) | Keep with framing note from PM-05 |

---

## 4. Rejected Findings — Justification Review

The meta plan explicitly rejected 6 findings. Each rejection was reviewed for grounding quality.

| Rejected Finding | Meta Plan Justification | Assessment |
|-----------------|------------------------|------------|
| Re-open M4 with convention-dependence language | "Phase 19 already locks reconstructive gauge-fixed encoding while crediting the issue doc arithmetic" (D-03) | **Sound.** Both 8 and 9 are defensible; Phase 19 chose one and locked it. |
| Add k > 6 warmup behavior | "The grounded stage range is 0..6" (resolution doc §8.7) | **Sound.** Adding undefined-range behavior is scope creep. |
| Add η_gauge / ε_L cross-reference note | "The context already separates geometry tolerance from loss stability scale" | **Sound.** Distinct symbol families with different purposes. |
| Apply claim that B-09 additive-softening derivation is mathematically wrong | "At most clarify that the plan compares the current unmatched additive-cubic force with the current additive potential and then locks the Plummer matched pair" | **Debatable.** The strawman `r/(r+ε)³` genuinely doesn't exist in published softening literature. But the locked verdict (Plummer) is correct either way — the error is in the audit trail, not the outcome. |
| Treat L_IC or L_L formulas as semantic gaps | "Resolution §8.3 and §8.6 give the formulas" | **Sound.** The resolution doc is explicit. |
| Add live-code "not read" attestations | "Use 'not used as v1.4 grounding; no pinn/ edits' instruction instead" | **Reasonable.** Achieves same governance goal with less ceremony. |

**Conclusion**: All rejections are grounded in either the resolution doc or locked Phase 19 decisions. None are arbitrary. The B-09 derivation rejection is the most debatable — the meta plan chose a conservative clarification over a full rewrite — but the physics outcome is unaffected.

---

## 5. Repaired Plan Verification

A dedicated verification agent audited all 7 repaired planning files against every meta-plan prescription. **Result: 100% pass — zero failures, zero partials.**

### 5.1 Meta-Plan `rg` Criteria (6/6 PASS)

| # | Criterion | Result |
|---|-----------|--------|
| 1 | No unapproved numeric `epsilon_H` default in 19-02-PLAN.md | PASS |
| 2 | No `G'` or free gravitational coefficient in 19-02-PLAN.md | PASS |
| 3 | `L_L` normalization `1/(3N_t)` confirmed in 19-02-PLAN.md | PASS |
| 4 | `L_data` Huber rewrite explicit in 19-02-PLAN.md | PASS |
| 5 | Strict `PASS: AC-PHYS-01..06` markers required in 19-04-PLAN.md | PASS |
| 6 | No "log and continue" closure-unsafe wording in 19-03-PLAN.md | PASS |

### 5.2 Repair Unit Checks (5/5 units PASS)

| Unit | Scope | Key Verifications |
|------|-------|-------------------|
| **Unit 1** | Context/Governance | D-12 parallel-safety clarified; D-14 annotation mechanics precise; D-19 schema 5-column; live `pinn/` references restricted to handoff only; 19-GAPS.md exists with GAP-19-01 OPEN; v1.4-GAPS.md updated |
| **Unit 2** | P01 | Clean raw-mass proof (no M_scale); M_tot=3 corrected; non-numeric causal clipping added; parallel ledger writes serialized; verify-before-commit ordering |
| **Unit 3** | P02 | G' removed; L_data Huber rewrite explicit; L_IC uses (1/3) Σ formulas; L_L = 1/(3N_t); epsilon_H symbolic with explicit "do not preserve" instruction; AD listing clarified as illustrative; cross-contract velocity dependency documented |
| **Unit 4** | P03 | "Log and continue" replaced with closure-safe routing; CTL-side defects route to targeted repair tasks; D-07 is literal authority |
| **Unit 5** | P04 | Strict PASS: AC-PHYS-01..06 markers; scoped negative checks; exit-gate regex safe (grouped pipes); source files verified directly; pinn/ edits forbidden |

---

## 6. Cross-Review Discrepancies

Two review documents made claims that contradict the consensus of the other reviews:

### 6.1 P01/P02 Parallelism Safety

- **R7** (`plan-review-convergence.md`, line 142-144): "P01 + P02 (Wave 1, parallel): Different files (ctl vs pinn_arch), no conflict. Correct."
- **R1** (`REVIEW.md`, line 279): "P01/P02 parallelism is safe (different files)."

**Why this is wrong**: Both P01 and P02 write to `16-ISSUE-LEDGER.md` and `pinn_instruction/issues/01-architecture-and-physics-foundations.md`. Six other reviews (R3, R4, R5, R6, R8, plus R1's own B2 finding) flagged the shared-artifact write conflict.

**Resolution**: The meta plan correctly identified and repaired this. R7's claim should be disregarded by future readers.

**Recommendation**: Consider adding an errata note to `2026-05-22-plan-review-convergence.md` flagging that its structural assessment of Wave-1 parallelism is incorrect.

### 6.2 L_data Current State

- **R7** (`plan-review-convergence.md`, M1): Claimed the current spec uses "MSE" for L_data.

**Why this is wrong**: The actual `pinn_architecture.md` data loss uses MAE/L1, not MSE.

**Resolution**: The meta plan (Unit 1) corrected this: "Correct any 'current spec uses MSE' wording for L_data; the current pinn_architecture.md data loss is MAE/L1." R7 correctly identified the error in the plans (the plans said "MSE") but the review itself contains a factual inaccuracy about what the current spec uses.

---

## 7. Gap Register Status

### Phase 19 Gaps

| Gap | Description | Status | Blocking |
|-----|-------------|--------|----------|
| GAP-19-01 | Numerical default for epsilon_H in energy-drift denominator | OPEN | P02 work requiring numeric epsilon_H |

### Milestone v1.4 Gaps

| Phase | Total Gaps | Open | Resolved |
|-------|-----------|------|----------|
| Phase 17 | 11 | 0 | 11 |
| Phase 18 | 5 | 0 | 5 |
| Phase 19 | 1 | 1 | 0 |
| **Total** | **17** | **1** | **16** |

---

## 8. Recommendations

### Before Phase 19 Execution

1. **Resolve GAP-19-01** (epsilon_H numeric default). This is the only open gap blocking any Phase 19 work. All other issues can be addressed during or after execution.

2. **Add errata note to `2026-05-22-plan-review-convergence.md`**: Flag that its Wave-1 parallelism assessment ("no conflict") is incorrect per the consensus of 6 other reviews. Future readers should not be misled.

### During Phase 19 Execution (optional polish)

3. **PM-01**: Add symmetric L_E |H_0| degeneracy note during P02 execution.

4. **PM-02**: Add η_c density scaling note during P02 execution.

5. **PM-04 through PM-17**: Address documentation enhancements opportunistically during plan execution. None are blocking.

### For Phase 21 Planning

6. **PM-03**: Flag the AD bootstrapping dependency for Phase 21 VER-04 — if AD is wrong, L_IC,v and L_L both train toward wrong physics. A convergence-consistency probe between L_IC,v and L_data would detect this failure mode.

---

## 9. Conclusion

The Phase 19 multi-AI review and repair process was thorough and effective. Eight independent reviews produced a dense findings landscape. The meta plan successfully navigated this landscape — deduplicating, prioritizing, and routing findings into concrete plan edits. The repaired plans are internally consistent, physically grounded, and execution-ready (modulo GAP-19-01).

The meta plan's judgment calls on which findings to reject were consistently grounded in the resolution doc or locked Phase 19 decisions. Its judgment calls on which findings to defer (CONSIDER/FYI items) were reasonable prioritization, though a few items that the routing section recommended addressing during execution were not mandated by any implementation unit.

No finding of BLOCKING, CRITICAL, or MAJOR severity was missed. The three higher-concern missed items (PM-01 through PM-03) are edge cases or latent risks, not active defects in the repaired plans.

**The meta plan was good enough.** The Phase 19 plans are ready for execution once GAP-19-01 is resolved.

---

## 10. Verification Notes (added 2026-05-24)

Independent re-verification against the repaired plans and source documents (direct `rg` re-runs of all 6 meta-plan criteria, parallel Explore-agent grounding checks, and physics sanity checks) found three of this audit's "potentially missed" claims to be overstated or wrong. Preserved here so future readers don't act on incorrect recommendations:

- **PM-02 (η_c collocation-density scaling):** OVERSTATED. The meta-plan IS addressing this. `.planning/phases/19-physics-and-loss-contracts/19-02-PLAN.md:373-375` reads: *"Clip the causal exponent to avoid underflow, but do not choose a numeric clipping bound in Phase 19; surface a gap if one is needed."* This satisfies the v1.4 STOP-protocol grounding rule (non-numeric language with explicit surface-as-gap escape). The audit's claim that the meta-plan "never addresses η_c=1 choice" misreads the current plan text. No further action required for PM-02.

- **PM-03 (AD bootstrapping detection):** OVERSTATED. The PHYS-02 AD-contract dependency is explicitly documented in the repaired `19-02-PLAN.md`: line 346 for `L_IC,v` (*"The velocity v_θ'(0) comes from the PHYS-02 componentwise normalized-time AD contract"*); lines 359-360 for `L_L` (*"The velocity v_θ'(u_n) used to compute L_θ'(u_n) comes from the PHYS-02 componentwise normalized-time AD contract"*); line 431 for the Phase 21 verification route (*"the disposable probe belong to Phase 21 VER-04 / AC-PHYS-02"*). The "no verification mechanism" framing in the audit's PM-03 conflates Phase 19 (structural specification) with Phase 21 (numeric validation), which are intentionally separated by milestone design. Phase 21 VER-04 is the appropriate venue for the AD-correctness probe; the dependency is documented at the loss-term level so a Phase 21 planner cannot miss it.

- **PM-13 (B-09 "category error" framing softening):** FALSE ALARM. The framing is explicitly grounded in EVID-05 adjudication: `19-CONTEXT.md` D-02 (line 100) states *"The issue doc's '5 orders of magnitude mismatch' framing is a category error — it compared PINN-internal static-invariant ε (1e-10) against PINN-internal training ε (1e-5), both PINN-side"*; and the B-09 evidence-packet instructions in `19-02-PLAN.md` lines 199 and 221 require this same framing in `B-09.md` §1 and §5. The framing is the EVID-05 §9 verdict ("issue doc partly correct on separating static-invariant ε from training-time softening; wrong/overstated on the mismatch framing"), not a strawman. Softening this language would weaken a grounded position. **Do not soften.**

### Verified-real items addressed

In parallel with this verification-notes addendum, the 5 audit findings that were verified as real and actionable have been applied to the planning artifacts:

- **PM-01** → `19-GAPS.md` "Known Symmetric Edge Cases" section (KSE-19-01 documents the `L_E`/`L_L` denominator-collapse symmetry and the shared Huber mitigation).
- **PM-04** → `19-02-PLAN.md` L_IC subsection rationale paragraph (squared error for IC = deterministic preprocessing; Huber for L_data = noisier targets).
- **PM-08** → `19-CONTEXT.md` D-19 divergence table now has a dedicated `Loss-stage warmup schedule (energy term magnitude)` row capturing the ~3-4 OOM shift.
- **PM-11** → `19-CONTEXT.md` D-01 now includes the T=10 grounding sentence that produces D ≈ 4.6416.
- **PM-16** → `19-02-PLAN.md` Task 1 now mandates a §6.5 `Numerical Defaults Provenance` table in B-07/B-08/B-09 evidence packets.

The 10 unverified lower-concern items (PM-05, 06, 07, 09, 10, 12, 14, 15, 17) remain available for opportunistic execution-time handling.
