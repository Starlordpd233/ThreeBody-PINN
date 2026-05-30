# Phase 19 Structural Verification

This file records the Phase 19 structural acceptance checks for `AC-PHYS-01` through
`AC-PHYS-06`. Phase 19 records structural criteria only; Phase 21 owns numeric pass
criteria and disposable probe execution.

Notation note: the current specs use Unicode notation in two places covered by the plan
probes (`T²` for the mass-fraction alternative and `2πu` for the synthetic trajectory).
The structural suite checked those existing notations with equivalent `rg` patterns
without editing the framework specs.

| AC ID | Command or manual check | Expected result | Actual result | Result |
|---|---|---|---|---|
| AC-PHYS-01 | `rg` checks for `Governing Mathematical Convention`, raw-mass nondimensionalization, future-rewrite-only mass-fraction alternative, `D=(G*T**2)^(1/3)`, and the alternative `D=(G*M_tot*T²)^(1/3)` only in that alternative context. | CTL spec locks raw-mass scaling and documents the mass-fraction path as future rewrite only. | Lines 591-600 of `ctl_instruction.md` match the required structural anchors. PASS: AC-PHYS-01 | PASS |
| AC-PHYS-02 | `rg` checks for the normalized-time derivative contract, canonical `u=t/T` leaf, conditional `tau` chain-rule factors, componentwise derivative requirement, forbidden all-ones vector-Jacobian product, `2πu` synthetic trajectory, and CTL cross-reference. | Architecture spec owns PHYS-02 and CTL cross-references it without duplicating the contract. | `pinn_architecture.md` lines 828-870 and `ctl_instruction.md` line 989 match the required structural anchors. PASS: AC-PHYS-02 | PASS |
| AC-PHYS-03 | `rg` checks for Plummer `r_safe` in both specs, `epsilon_train=10^-5`, `epsilon_inv=10^-10`, unsoftened `s_min`, anti-pattern warnings, and stale additive-softening negative checks. | Both specs use the matched Plummer form and no stale softening symbols remain. | `ctl_instruction.md` lines 678-695 and `pinn_architecture.md` lines 380-584 match required anchors; stale softening negative checks returned no matches. PASS: AC-PHYS-03 | PASS |
| AC-PHYS-04 | Negative `rg` checks for HNN-style architecture claims, plus positive checks for soft conservation regularizer, Energy Conservation Regularizer, matched-Plummer Hamiltonian, and `H_ε`. | HNN-style framing is removed and energy is framed as a soft conservation regularizer. | HNN negative checks returned no matches; `pinn_architecture.md` lines 489-507 and 941 match required anchors. PASS: AC-PHYS-04 | PASS |
| AC-PHYS-05 | Negative `rg` checks for pseudo-ALM default-loss terms, plus positive checks for Optional ALM Ablation, P2, scalar conservation constraints only, and optimizer-phase semantics for Adam/L-BFGS. | Default loss excludes pseudo-ALM and optional ALM is P2 scalar-conservation-only. | Pseudo-ALM default negative checks returned no matches; `pinn_architecture.md` lines 649-672 and 945 match required anchors. PASS: AC-PHYS-05 | PASS |
| AC-PHYS-06 | `rg` checks for IC13 Validity, reconstructive fixed-gauge / gauge-fixed prose, no constraint-counting justification, Phase 17/18 cross-reference, and absence of the stale 8D passage. | CTL M4 text uses reconstructive gauge-fixed encoding and removes the old constraint-counting claim. | `ctl_instruction.md` line 941 matches required anchors; stale M4 text negative check returned no matches. PASS: AC-PHYS-06 | PASS |

## Closure Guards

- All six exact markers are present: `PASS: AC-PHYS-01`, `PASS: AC-PHYS-02`, `PASS: AC-PHYS-03`, `PASS: AC-PHYS-04`, `PASS: AC-PHYS-05`, `PASS: AC-PHYS-06`.
- No `pinn/` diff is present in staged or unstaged changes.
- `GAP-19-01` is resolved: `19-GAPS.md`, `v1.4-GAPS.md`, and `19-CONTEXT.md` carry the canonical D-20 decision.
- Phase 21 handoff validates denominator activation behavior only: `Pr(|H0| < epsilon_H)` and quantiles of `|H0| / S_H`.
- Phase 21 does not reopen epsilon selection unless a new user-instruction gap is created.
- The final acceptance guards use the resolved numeric contract `epsilon_H = 1e-4 * S_H`, not a symbolic placeholder.
- The closure plan no longer treats `GAP-19-01` as open or blocking.
