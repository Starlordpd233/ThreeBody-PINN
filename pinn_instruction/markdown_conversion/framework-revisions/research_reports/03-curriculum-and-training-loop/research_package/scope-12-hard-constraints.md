# Hard Constraints — Locked v1.4 + v1.5 Outcomes (the SCOPE-12 set)

> **Treatment class:** AUTHORED upload companion. Reference any other companion or
> snapshot by **bare filename** only. This preamble is a hard-constraints contract for
> the external research: the items below are **already decided and locked**. They are
> NOT open questions, NOT part of this adjudication, and may NOT be re-opened by the
> research. The contested/open questions live in `framed-research-questions.md`; the
> figure-grounding table lives in `claims-register.md`; the verified dataset anchors
> live in `verified-facts-reference.md`.

The doc-03 (curriculum + training loop) adjudication runs **on top of** two prior locked
milestones: doc-01 (architecture + physics foundations) and doc-02 (data pipeline +
validation). Their outcomes are settled framework conventions. The research must treat
every item in this file as a fixed boundary condition and reconcile its answers **to**
these constraints — never against them.

---

## 1. Locked v1.4 + v1.5 outcomes (verbatim — hard constraints)

These are stated verbatim as the locked grounding set. Respect them; do not re-derive,
re-open, or contradict any of them.

1. **14D network input `[τ, IC₁₃]`.** The network input is exactly 14 dimensions:
   the normalized time `τ = 2u − 1` (autograd leaf `u = t/T`) concatenated with the
   13-component initial-condition vector `IC₁₃`.

2. **Jacobi-state `IC₁₃`.** `IC₁₃` is the fixed-gauge Jacobi-state initial-condition
   encoding (raw ordered masses + Jacobi position/velocity scalars + energy), produced
   by the locked preprocessing pipeline (COM removal, zero-momentum boost, canonical
   ordering, canonical rotation gauge). It is redundant-but-reconstructive and is not
   justified by constraint counting (locked Phase 19, PHYS-06).

3. **Mass-weighted COM projection head.** A hard mass-weighted center-of-mass
   projection head is applied to the 9D position output **before** any loss or metric is
   evaluated; linear momentum is enforced structurally by this head, so no separate
   linear-momentum loss term exists.

4. **PHYS-03 training-time softening `eps_soft = 1e-5`.** The training-time Plummer
   softening parameter is `ε_train = 1e-5`, applied identically in the physics-residual
   force term and the energy regularizer (matched-Plummer form
   `r_safe = sqrt(‖Δr′‖² + ε_train²)`). Additive `(‖r‖ + ε)` softening on the distance
   norm is the PHYS-03 anti-pattern and is prohibited.

5. **Post-v1.3 SCS gate `ε_H > 10⁻⁵` / `SCS > −5`.** The self-consistency / energy-gate
   thresholds adopted post-v1.3 are locked: the energy-denominator floor regime
   `ε_H > 10⁻⁵` and the screening gate `SCS > −5`.

6. **PHYS-01 raw-mass `D ≈ 4.6416`.** The characteristic length scale is
   `D = (G·T²)^(1/3) ≈ 4.6416` (with `G = 1`), derived from **raw-mass**
   non-dimensionalization (raw masses `mᵢ`, not mass fractions). The alternative
   total-mass form `D = (G·M_tot·T²)^(1/3) ≈ 6.694` (with `M_tot = 3`) was **rejected**
   by v1.5 Phase 25 (EVID-10) and is documented as a future-only framework-wide rewrite,
   never adopted. **`D ≈ 4.6416` is locked; `D = 6.694` is not selectable.**

7. **v1.5 data-side contracts PIPE-01..10 / VAL-01..04.** The v1.5 DataLoader,
   stage-query, and validation-metric contracts are locked: the stage-query interface
   (`sample_replay(n, max_stage)`, `sample_lookahead(n, stage)`, `has_stage(k)`), the
   trajectory-admission gate, the blacklist-exclusion and quality-metric (SASD / IPR /
   PSC) contracts, and the validation-metric definitions. The research consumes these as
   fixed inputs.

---

## 2. Live-code citations are OVERRIDDEN (the source-of-truth override)

issue-03 carries "Canonical" citations of two live implementation files —
`data-processing-pipeline-full.py` and `basic_architecture.py`. **These citations are
overridden and carry no authority for this adjudication.** The live implementation code
is **not** a grounding source. Where issue-03 cites those two files as canonical
(for IC-vector assembly, stage assignment, `get_batch()`, the SIREN implementation, or
any other contract), the **framework specs are the source of truth** — specifically the
two spec-edit targets `ctl_instruction.md` and `pinn_architecture.md`, plus the locked
conventions in items 1–7 above. Any divergence between the live code and the specs is
resolved in favor of the specs; the code is reconciled later, outside this adjudication.

---

## 3. Locked hard constraints vs. revisable baseline (read this carefully)

Two different categories of spec content travel in this package, and the research must
NOT conflate them:

- **Locked hard constraints (items 1–7 above).** Fixed. Not in scope. Not re-openable.
  These are the SCOPE-12-locked v1.4 + v1.5 outcomes.

- **Revisable current doc-03 design state (the baseline).** The **current positions** in
  `ctl_instruction.md` and `pinn_architecture.md` on the doc-03 training-loop contracts —
  curriculum staging, batch construction (replay/lookahead, data-fidelity vs.
  collocation), stage-transition criteria, loss scaling and the loss-weight schedule,
  the `τ_L` / `L_max` formulas, and gradient clipping — are the **baseline / current
  design state**. They are the genuinely-open spec-edit targets of this adjudication and
  **may be revised** by the resolution the research informs. Treat them as the current
  baseline to critique against, not as locked law.

The research's job is to reconcile the revisable baseline **under** the locked hard
constraints. A proposed change to a revisable contract is in scope; a proposed change to
a locked hard constraint is out of scope and must be surfaced as a conflict, not adopted.

**Worked example of the distinction (the `D` case).** The *value* `D ≈ 4.6416` is a
locked hard constraint (item 6) — not open. What *is* open is how issue-03's `τ_L` /
`L_max` derivation re-derives **given** that locked `D`. So "which `D` is correct" is
settled (it is `4.6416`); "how the `τ_L` formula reconciles under `D ≈ 4.6416`" is the
open reconciliation question (see `framed-research-questions.md`). The same locked-vs-open
split applies to the softening parameter: the loss-side `eps_soft = 1e-5` (item 4) is
locked, while whether a distinct static-context softening coexists with it is open.

---

## 4. Findings out of scope for this adjudication (declined at the consolidation gate)

**None.** No candidate finding was declined at the consolidation gate; in particular the
ALM `μ_p`-clamp finding is **included** as its own framed question, so it retains a
resolution path. (This slot exists so that any finding declined in a future revision is
recorded here as "out of scope for this adjudication," with the downstream consequence
noted. At present there are no such declined findings.)
