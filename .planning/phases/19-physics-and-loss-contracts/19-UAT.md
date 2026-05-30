---
status: complete
phase: 19-physics-and-loss-contracts
source: [19-01-SUMMARY.md, 19-02-SUMMARY.md, 19-03-SUMMARY.md, 19-04-SUMMARY.md]
started: 2026-05-30T19:34:18Z
updated: 2026-05-30T19:34:18Z
method: independent re-verification via 4 read-only subagents (auto-verified; spec phase has no interactive UI)
---

## Current Test

[testing complete]

## Tests

### 1. PHYS-01 — Raw-mass scaling locked
expected: ctl_instruction.md locks raw-mass nondimensionalization with retained scale D=(G*T^2)^(1/3); the mass-fraction alternative D=(G*M_tot*T^2)^(1/3) is documented as a FUTURE-REWRITE-ONLY path (not active in v1.4); EVID-05/B-02 adjudication recorded.
result: pass
evidence: ctl_instruction.md:591-602; mass-fraction confined to future-rewrite text at :597-601; evidence/B-02.md verdict accept-resolution; issue row annotated at 01-architecture-and-physics-foundations.md.

### 2. PHYS-02 — Normalized-time derivative contract
expected: autograd leaf named explicitly as canonical u=t/T; tau=2u-1 chain-rule factors (2x velocity, 4x acceleration) stated when leaf is tau; componentwise derivatives REQUIRED with explicit anti-pattern warning against grad_outputs=torch.ones_like / r.sum() aggregate; synthetic-trajectory worked example present; CTL cross-references architecture without duplicating the math.
result: pass
evidence: pinn_architecture.md:843-910; CTL cross-ref ctl_instruction.md:988-989; r.sum() appears only as a Forbidden anti-pattern (pinn_architecture.md:866). Worked example r'(u)=[sin(2πu),cos(2πu),u²] is spec-authored (resolution doc uses r(τ)=τ³); derivatives are correct first-principles calculus (permitted grounding).

### 3. PHYS-03 — Matched Plummer softening + epsilon split
expected: physics residual and energy regularizer use a MATCHED softened Plummer force/potential pair; epsilons separated (epsilon_train=1e-5, epsilon_inv=1e-10, unsoftened s_min) after B-09 adjudication; no stale additive softening as an active formula.
result: pass
evidence: pinn_architecture.md:377-409, 511-518 (shared r_safe across residual/V_ε/H_ε); ctl_instruction.md:677-695 (epsilon_inv=1e-10, unsoftened s_min); additive form appears only inside the PHYS-03 anti-pattern at ctl_instruction.md:690-695; evidence/B-09.md accept-resolution.

### 4. PHYS-04 — Energy as soft conservation regularizer (not HNN)
expected: energy term described as a soft conservation regularizer using analytic matched-Plummer Hamiltonian H_ε; NOT framed as an HNN / Hamiltonian Neural Network.
result: pass
evidence: pinn_architecture.md:496-548, 956 — explicit "soft conservation regularizer... not architecture-level conservation"; "'Hamiltonian' refers to the analytic energy function H_ε, not a neural-network-parameterized Hamiltonian." Negative checks for "HNN" / "Hamiltonian Neural Network" returned zero active matches.

### 5. PHYS-05 — Default loss / causal residual / P2-only ALM
expected: default physics loss is CAUSAL-weighted (L_phys^causal with stopgrad), NOT an unweighted N_col mean as default; ALM limited to optional P2 scalar-conservation constraints (E, L_x, L_y, L_z), pseudo-ALM absent from default loss; dual-variable update rules name the optimizer phase (Adam/L-BFGS).
result: pass
evidence: pinn_architecture.md:410-423 (causal weights + stopgrad; unweighted mean demoted to "diagnostic, not the default training loss"), 626-685 (total loss, warmup, optional P2 ALM only, Adam/L-BFGS update/freeze semantics); pseudo-ALM appears only in rejection sentence ctl_instruction.md:1144; evidence/B-08.md accept-resolution.

### 6. PHYS-06 — M4 constraint-counting replacement
expected: stale "13 constraints overdetermine an 8D reduced phase space" passage REMOVED; replaced with evidence-backed reconstructive gauge-fixed IC13 validity prose + Phase 17/18 cross-references.
result: pass
evidence: ctl_instruction.md:941 replacement prose with IO-02 (Phase 17) / FRAME-01 (Phase 18) cross-refs; stale "13 constraints ... 8-dimensional reduced phase" negative check returned no active matches; evidence/M4.md accept-resolution.

### 7. Execution completeness (plans vs summaries vs git)
expected: all four plans' tasks completed and summarized with no silently dropped task; all claimed spec edits landed in git; working tree clean; zero pinn/ implementation files modified by Phase 19; ROADMAP marks 4/4 complete.
result: pass
evidence: SA-1 confirmed all 4 plans→summaries cover every task; commit chain ff7a309..aa9324b maps to claimed outputs; `git status --porcelain` empty; `git log --name-only ff7a309^..aa9324b -- pinn/` empty; ROADMAP 4/4 complete (2026-05-30).

### 8. D-20 / epsilon_H cross-artifact consistency
expected: epsilon_H = 1e-4 * S_H (S_H = median_train(K0+|U0|)) stated consistently across specs + gap registers + context + plans/summaries + STATE/INDEX + evidence packets; no residual 1e-12 energy-floor fallback; GAP-19-01 not OPEN; Phase 21 scope limited to denominator-activation reporting.
result: pass
evidence: SA-3 enumerated 30+ locations all matching the canonical form; the only 1e-12 survivals are FRAME-02 COM/momentum thresholds (correct, Phase 18 D-07) and banner-fenced non-canonical EDL history; Phase 21 scope correctly limited to Pr(|H0|<epsilon_H) + quantiles of |H0|/S_H.

### 9. Code-review fixes present in live specs
expected: all resolved review findings present — CR-01 causal default loss; CR-02 u∈[0,1] collocation/inference with leaf u=t/T; CR-03 epsilon_H stage gate; WR-01 loss.yaml wording; WR-03 Python class indentation; WR-04 adaptive collocation traj_data['u'].
result: pass
evidence: SA-3 independently located each fix in the live specs — pinn_architecture.md:411-423 (CR-01), :432-465 + :739-754 (CR-02), :555-588 (WR-03), :460-461 (WR-04); ctl_instruction.md:1266-1268 (CR-03), :1301-1302/:1408-1409 (WR-01).

### 10. Evidence / ledger / governance integrity
expected: B-02/B-07/B-08/B-09/M4 all VERIFIED + accept-resolution with FIX_APPLIED→VERIFIED transitions; ledger rows VERIFIED with no in-scope finding left IN_PROGRESS/FIX_APPLIED; CODE-DIVERGENCE schema + live-code-not-evidence statement present; no forbidden live-code-as-grounding usage; no silent invention; no OPEN gap.
result: pass
evidence: SA-4 confirmed all 5 packets VERIFIED/accept-resolution; ledger rows VERIFIED; 19-CODE-DIVERGENCE.md uses the 5-column schema and states live pinn/ code is not v1.4 evidence; every pinn/ reference is a FUT-01 handoff coordinate or governance guard; GAP-19-01 RESOLVED-WITH-INSTRUCTION; KSE-19-01 explicitly non-blocking; no other OPEN gap.

## Summary

total: 10
passed: 10
issues: 0
pending: 0
skipped: 0
blocked: 0

## Minor Observations (non-blocking — not criterion failures, not governance gaps)

These do NOT fail any Phase 19 success criterion and do NOT require user instruction under the v1.4 STOP protocol (no ungrounded semantic invention). Recorded for awareness; candidates for Phase 20/21 cleanup at the user's discretion. No spec edit was made by this verification.

1. **Token collision: `epsilon_train` used for two unrelated quantities in `ctl_instruction.md`.**
   - PHYS-03 Plummer softening parameter `epsilon_train = 10^-5` (ctl_instruction.md:695; defined in pinn_architecture.md).
   - Loss-plateau stage-transition convergence threshold `\epsilon_{\text{train}} = 10^{-5}` (ctl_instruction.md:1248, 1251).
   - Same symbol AND same value, different physics. No numeric contradiction, but an ambiguity/readability hazard. Pre-existing stage-transition machinery; Phase 19 introduced the softening name. Suggested home: Phase 20 (Architecture and Normalization Cleanup) rename.

2. **Broken relative evidence-link paths in specs.** Specs cite `evidence/B-02.md` (ctl_instruction.md:601) and `evidence/M4.md` (ctl_instruction.md:941); the packets actually live at `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/`. Labels are unambiguous but the relative paths don't resolve from the spec's own location. Citation hygiene.

3. **Plan `files_modified` header metadata incompleteness.** 19-03-PLAN.md header lists only pinn_architecture.md but execution also touched ctl_instruction.md (commit 656fce4, mechanical anchor repair); 19-04-PLAN.md header omits 19-REVIEW.md, 19-04-SUMMARY.md, and the post-review spec re-edits. All are disclosed in the corresponding SUMMARY "Deviations" sections; the plan headers were simply not retroactively updated.

4. **`D-20` vs `GAP-19-01` label drift.** Specs label the energy-floor decision "PHYS-04/D-20"; planning artifacts call it "GAP-19-01" / decision "n". Identical, grounded content; only the internal decision label differs. Traceability cosmetic.

## Gaps

[none — 0 criterion failures; GAP-19-01 already RESOLVED-WITH-INSTRUCTION; no new STOP-protocol gap surfaced by this verification]
