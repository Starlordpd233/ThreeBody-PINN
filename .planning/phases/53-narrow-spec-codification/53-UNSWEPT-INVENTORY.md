# Phase 53 — Un-Swept Default/Recommended Wordings (D-01 routed inventory)

Records the `default` / `recommended` wordings in
`pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` that
Phase 53 deliberately left **unmarked** under the locked-vs-default convention,
with the reasoning for each.

Phase 53 declares the convention and applies it at exactly one site (§4.1's
PHYS-05 per-stage λ^max(k) values). It does **not** sweep the file: GAP-45-03's
ruling ends with *"Generalization to other spec tables NOT decided"* — an
explicit owner withholding, so a sweep would reverse a standing ruling. This
inventory **records** the un-swept items; it marks nothing.

All line anchors below are **pre-edit** anchors verified 2026-08-19 (against
worktree HEAD `08e04176`, before Phase 53's own insertions shifted the file).

| # | Location | Text | Why un-swept |
|---|---|---|---|
| 1 | `:253` + `:260` | §2.4 Table 1 header "**Recommended Value**"; row `first_omega_0 \| 30` | **Routed to Phase 56** (first item of this inventory). The value is locked at §2.2 `:167` ("fixed at 30 and is not scheduled during training") yet labelled "Recommended Value", and it is SCOPE-38-amendable — Phase 56 may amend it under the recalibration decision. Marking it in Phase 53 would couple this phase to that outcome and destroy the independence that is Phase 53's reason to exist. |
| 2 | `:307` | §3.1 "where `$\delta_r = 1$` is the default Huber transition" | Adjacent to the §3.1 `L_data` edit site but not a VER-20 routing item; rewording it while editing §3.1 is a listed anti-pattern (minimal diff). |
| 3 | `:641`-`:644` | §4.1 where-block `$\delta_r = 1$` default; `$\lambda_{IC} = 1$` default | D-01 scopes the convention's application to the PHYS-05 per-stage values only; these are different values in the same subsection. |
| 4 | `:647` | §4.1 `$\eta_c = 1$` default wording | SCOPE-38 contract-marked and Phase-56-coupled. Touching it would be a SCOPE-38 amendment without re-ratification. |
| 5 | `:433`, `:440` | §3.2 `n_col = 4096` / "recommended: 2048-4096" | SPEC-06 territory (Phase 56); not covered by any ruling Phase 53 transcribes. |
| 6 | `:976`-`:992` | **Table 2** "Definitive Specification" — mixes locked values (`epsilon_train = 1e-5`, PHYS-03) with explicit defaults (`δ_r = 1`, `λ_IC = 1`) | Marking it would require roughly fifteen fresh status adjudications that no owner ruling covers. Cited here as "Table 2": sections 6-9 do not exist as headers in this file, so a "§9" citation would not resolve. |
| 7 | `:357`-`:360` | §3.1 Loss Integration Note "unweighted in the default objective" | Here "default" modifies the objective *formulation*, not a tabulated value, so the value-attached convention does not apply. |

## Disposition

Item 1 is routed to **Phase 56**, which is already editing §2.2/§2.4 territory
under the recalibration decision. Items 2-7 remain open with no assigned phase;
extending the sweep is additive and reversible — a later phase adds markers, and
nothing here has to be undone.
