---
phase: 19
slug: physics-and-loss-contracts
total_gaps: 1
open_gaps: 1
resolved_gaps: 0
deferred_gaps: 0
last_updated: 2026-05-24
governance: "Governed by CLAUDE.md/AGENTS.md/GEMINI.md 'CRITICAL GOVERNANCE' block (STOP protocol + math/engineering grounding requirement + no-live-code directive). GAP-19-01 is OPEN; dependent Phase 19 P02 work must not assign a numeric epsilon_H default until user instruction resolves it."
---

# Phase 19 Gap Register

This file records every Phase 19 decision where source materials (resolution doc, issue doc, prior user / roadmap / requirements decisions, framework specs revised in v1.4, or first-principles physics) did not explicitly answer the question. Per the CRITICAL GOVERNANCE rule, when an agent hits such a decision it MUST: (1) STOP, (2) verify it understands the math/physics/engineering at stake, (3) record the gap with all required fields, (4) update the milestone-wide index, (5) surface to the user and wait for instruction.

**Live-code directive (2026-05-19):** Live code in `pinn/` is NOT a grounding source for any v1.4 decision. Live-code references are permitted only in forward-pointing FUT-01 hand-off documents such as `19-CODE-DIVERGENCE.md`.

**Required fields per entry (per governance rule):** Decision point - Where in artifact - Task context - Classification - Source silence (file:line) - Mathematical / engineering grounding - Agent was tempted to - What the user needs to decide - Confidence of impact - Status - Resolution note.

---

## GAP-19-01: Numerical default for `epsilon_H` in the energy-drift denominator

- **Decision point:** The Phase 19 energy-conservation loss uses `epsilon_H` in the relative energy-drift denominator. Should Phase 19 assign a numeric default to `epsilon_H`, and if so what value and scope should it have?
- **Where in artifact:** `.planning/phases/19-physics-and-loss-contracts/19-02-PLAN.md` Task 2 `L_E` formula block; the draft currently says `epsilon_H = 10^-8`.
- **Task context:** Repairing the Phase 19 execution plans from `docs/findings/milestone_v1.4/reviewing_phase19_plans/2026-05-22-phase19-plan-repair-meta-plan.md`. The review convergence found that `epsilon_H = 10^-8` was invented by the plan; the resolution document names only the symbol.
- **Classification:** semantic.
- **Source silence:**
  - `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:928` defines `Delta H_n` with denominator `|H_epsilon(r_0',v_0')| + epsilon_H`, but does not assign a numeric value to `epsilon_H`.
  - `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:934` defines `L_E` as a Huber average over `Delta H_n`; it does not bind `epsilon_H`.
  - `pinn_instruction/issues/01-architecture-and-physics-foundations.md:76` discusses softening values for static invariants and training loss, not the energy-drift denominator stability scale `epsilon_H`.
  - `.planning/phases/19-physics-and-loss-contracts/19-CONTEXT.md:164` transcribes the `L_E` denominator with symbolic `epsilon_H`, but does not record a user decision assigning a numeric value.
- **Mathematical / engineering grounding:** `epsilon_H` stabilizes division by the initial matched-Plummer Hamiltonian magnitude when computing relative drift. Its value controls how strongly trajectories with small `|H_0|` are penalized: a smaller value preserves a stricter relative normalization but risks exploding `Delta H_n` near zero-energy cases, while a larger value floors the denominator and changes the effective weighting of low-energy trajectories. This is distinct from `epsilon_train` and `epsilon_inv` softening, and distinct from `epsilon_L`, because it normalizes a scalar conservation-drift term rather than regularizing a force/potential denominator or angular-momentum scale. Reusing `10^-8` may be reasonable by analogy to other numerical-stability floors, but that analogy is not a grounding source under the v1.4 STOP protocol.
- **Agent was tempted to:** Set `epsilon_H = 10^-8`, matching the draft plan and common numerical-floor convention, while labeling it as a stability scale distinct from softening.
- **What the user needs to decide:**
  - (a) Leave `epsilon_H` symbolic in Phase 19 and require FUT-01 or Phase 21 to bind it with explicit validation.
  - (b) Bind `epsilon_H = 10^-8` now as a Phase 19 loss-contract default.
  - (c) Provide a different numeric value and explain whether it is absolute, dimensionless, or tied to an energy scale.
  - (d) User writes the exact `epsilon_H` contract directly.
- **Confidence of impact:** **HIGH** - affects the default energy-drift loss weighting and may change both Phase 19 spec text and Phase 21 loss-stability validation design.
- **Status:** **OPEN**
- **Resolution note:**

---

## Notes

GAP-19-01 was surfaced during Phase 19 plan repair before Phase 19 execution. Until resolved, plan text must not preserve or rely on a numeric `epsilon_H` default; dependent P02 work is blocked at the point where a concrete default would be required.

---

## Known Symmetric Edge Cases (non-blocking)

This section documents edge cases that are mathematically symmetric between two loss terms and share a single mitigation. They are not STOP-protocol gaps — they do not require user instruction — but they are recorded here so future audits and Phase 21 numeric-validation planners do not treat them as missed.

### KSE-19-01: `L_E` and `L_L` denominator-collapse symmetry near zero conserved quantity

- **Loss terms:** `L_E` uses `H_scale = |H_0'| + ε_H`; `L_L` uses `L_scale = ||L_0'|| + ε_L` (see `19-CONTEXT.md` decisions D-06 and the L_E formula context).
- **Edge case:** For marginally-bound trajectories with `|H_0'| → 0`, the `L_E` denominator collapses to `ε_H`, amplifying relative-drift magnitudes. The mathematically symmetric `L_L` case occurs for IC samples with near-coplanar / near-collinear configurations where `||L_0'|| → 0`.
- **Shared mitigation:** Both losses apply Huber (δ=1.0) around the per-sample relative-drift term. The Huber cap bounds per-sample contribution to linear growth past `δ`, so denominator-driven amplification cannot drive unbounded loss for either term.
- **Phase 21 follow-up:** Phase 21 numeric validation (AC-PHYS-04 for `L_E`, AC-PHYS-05/06 for `L_L`) should include low-`|H_0|` and low-`||L_0||` IC subsets in the disposable probes so the Huber-cap mitigation is exercised, not assumed. Surface a NEW gap only if either Phase 21 probe reveals the Huber cap is insufficient and prescreening, formula changes, or a denominator floor change become necessary.
- **Why not a STOP-protocol gap:** No user instruction is needed; the contract is grounded (resolution §8.5 for `L_E`, §8.6 for `L_L`); the mitigation is symmetric; the residual risk is empirical and properly belongs in Phase 21 numeric validation, not Phase 19 structural specification.
