# Resolution-Doc Skeleton (NON-BINDING) — doc-03 Curriculum and Training Loop

> **NON-BINDING.** The resolution doc remains the framework owner's product. This skeleton
> is a **suggestion only** — it exists to ease coverage-checking (so every framed question
> has a visible verdict slot) and to carry the downstream finding → adjudication-phase
> mapping. **No schema is mandated.** You may structure the resolution doc however you
> prefer; the v1.4 and v1.5 resolution docs are offered only as **format precedents**, not
> as a required template.
>
> **Treatment class:** AUTHORED upload companion. Reference companions by **bare filename**
> only. The questions this skeleton mirrors live in `framed-research-questions.md`; the hard
> constraints in `scope-12-hard-constraints.md`; the figure register in `claims-register.md`.

## Format precedents (suggestion only — no schema required)

- **v1.4 resolution doc:** `ctl_pinn_resolution.md` — the doc-01 (architecture + physics
  foundations) resolution doc. A workable per-finding verdict format.
- **v1.5 resolution doc:** `02-resolution-doc.md` — the doc-02 (data pipeline + validation)
  resolution doc. The most recent precedent; same package family.

Either is a fine model. Adopt, adapt, or ignore the structure below as you see fit.

## Downstream adjudication-phase map (where each verdict lands)

Each resolved finding feeds a later v1.6 adjudication phase. The mapping below is a guide so
the verdict is written with its destination spec contract in mind. Spec-edit targets are
`ctl_instruction.md` and `pinn_architecture.md` only.

| Finding cluster | Adjudication phase | Primary spec-edit target |
|-----------------|--------------------|--------------------------|
| Cross-milestone / cross-source conflicts (root-cause adjudication) — the `D` conflict; the three named decisions | **Phase 32** (root-cause adjudication / evidence) | both targets, as adjudicated |
| Curriculum / staging / `τ_L` / `L_max` / stage transitions (CURR cluster) | **Phase 33** | `ctl_instruction.md` |
| Training-loop mechanics: batch construction, loss composition, causal mode (LOOP cluster) | **Phase 34** | `ctl_instruction.md` + `pinn_architecture.md` |
| Loss scaling / weights / gradient clipping / softening (LOSS cluster) | **Phase 35** | `pinn_architecture.md` |
| Source-issue / cross-reference reconciliation | **Phase 36** (FUT hand-off) | both targets / FUT |

---

## Per-finding verdict slots (one per framed question)

> Fill each slot with the adjudicated verdict, the evidence, and the resulting spec edit.
> Leave the locked sub-parts marked LOCKED (do not re-open). Slots are ordered as in
> `framed-research-questions.md` (issue-03 section order).

### The causal-training-mode decision  → Phase 32 / Phase 34
- **Verdict:** _(per-time-step A / global+ALM B / time-windowed hybrid C — owner's choice)_
- **Reconciliation note:** how the choice relates to the existing PHYS-05 causal-weighting
  default and the rejection of dense-residual ALM.

### The s_min-frame decision  → Phase 32 / Phase 33
- **Verdict:** _(unsoftened gate + softened loss / softened everywhere)_
- **Note:** distinct from the D5 stage-transition finding.

### The epsilon-strategy decision  → Phase 32 / Phase 35
- **LOCKED:** loss-side `eps_soft = 1e-5` (not re-openable; `claims-register.md` CLM-19 /
  PHYS-03).
- **Verdict (OPEN part only):** static/invariant-softening reconciliation under the locked
  loss-side value — dual-context `1e-10` / collapse to `1e-5` / unify at `1e-10`.

### B-07 — replay/lookahead batch construction  → Phase 34
- **Verdict / spec edit:** _(replay/lookahead counts, per-trajectory points, 50/50)_

### B-08 — data-fidelity vs collocation point separation  → Phase 34
- **Verdict / spec edit:** _(two independent point sets contract)_

### M6 — `L_norm` clamping  → Phase 33
- **Verdict / spec edit:** _(clamp discipline given `L_norm` is now metadata)_

### M7 — `τ_L` excluded from IC vector  → Phase 33
- **Verdict / spec edit:** _(confirm exclusion by design under the locked 14D contract)_

### M14 — merged gradient clipping  → Phase 35
- **Verdict / spec edit:** _(`C_stage · median(·)`; reconcile `5.0` factor vs `C` schedule)_

### M15 — energy-loss weight schedule  → Phase 35
- **Verdict / spec edit:** _(capped-hybrid `cap_table` vs PHYS-05 warmup `λ_E^max(k)`)_

### M16 — `dt_out`-aware collocation scaling  → Phase 33 / Phase 35
- **Verdict / spec edit:** _(`n_col ∝ dt_base/dt_out`; verified `dt_out` from CLM-17)_

### D5 — stage-transition dual-path  → Phase 33
- **Verdict / spec edit:** _(strict + fallback; per-stage thresholds CLM-08 / max-epochs CLM-09)_

### NS-12 — componentwise AD  → Phase 34
- **Verdict / spec edit:** _(confirm PHYS-02 componentwise AD satisfies NS-12)_

### NS-13 — Huber energy δ  → Phase 35
- **Verdict / spec edit:** _(δ = 1.0 baseline vs quantile-tuned 0.01–0.1)_

### NS-18 — loss-component scaling contract  → Phase 35
- **Verdict / spec edit:** _(units contract across L_data / L_physics / L_energy)_

### Data-driven adaptive stage assignment  → Phase 33
- **Verdict / spec edit:** _(adaptive methodology vs threshold-based Step 5; population safeguards)_

### `D = 6.694` vs `D ≈ 4.6416` (the worked conflict)  → Phase 32
- **LOCKED:** `D ≈ 4.6416` (not re-openable; CLM-19 / PHYS-01; `6.694` rejected by EVID-10).
- **Verdict (OPEN part only):** `τ_L` / `L_max` re-derivation under the locked `D`.

### `τ_L` / `L_max` computation formulas  → Phase 33
- **Verdict / spec edit:** _(L_max formula; shadow-trajectory τ_L with split
  `epsilon_pert = 1e-8` / `epsilon_soft = 1e-10`; PCA+Rosenstein approximation)_

### ALM `μ_p` clamp  → Phase 34 / Phase 35
- **Verdict / spec edit:** _(clamp `[1e-4, 100.0]` placement given dense-residual ALM is
  rejected; applies to the P2 scalar-constraint ablation if anywhere)_

---

*This skeleton is non-binding and prescribes no schema; the v1.4 `ctl_pinn_resolution.md`
and v1.5 `02-resolution-doc.md` are format precedents only. Adapt freely.*
