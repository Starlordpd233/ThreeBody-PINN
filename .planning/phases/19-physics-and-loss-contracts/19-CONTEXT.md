# Phase 19: Physics and Loss Contracts - Context

**Gathered:** 2026-05-22
**Status:** Ready for planning
**Mode:** `gsd-discuss-phase 19 --all ultrathink` (all 5 gray areas auto-selected; full interactive discussion per default mode). Resolution doc remains the default verdict source per milestone directive (2026-05-18); EVID-05 triggered for B-02, B-09, and M4 (M4 reclassified — see D-16). Issue Doc adjudication-annotation convention established this phase (see D-14).

---

> **GOVERNANCE NOTICE** — Produced under `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` **CRITICAL GOVERNANCE** rule (STOP protocol + math/engineering grounding requirement). No new `19-GAPS.md` entries were created at context-gathering time: every semantic and process-artifact decision below was either (a) directly answered by the user in the 2026-05-22 discussion, or (b) grounded in locked Phase 16/17/18 precedent. During the 2026-05-22 plan-repair pass, `GAP-19-01` was opened for the ungrounded numeric default `epsilon_H = 10^-8`; dependent P02 work must not choose a numeric `epsilon_H` default until the user resolves it. The Phase 16 ledger inconsistency on M4's `Sources Disagree?` flag was surfaced and corrected in the same discussion (D-16) rather than being recorded as a gap, because the user provided the corrective instruction inline. New gaps encountered during plan-phase or execute-phase MUST be appended to `19-GAPS.md` per the STOP protocol; the Decision Status Summary at the top of §"Implementation Decisions" below is the authoritative gate.
>
> **Live-code directive (2026-05-19):** Live code in `pinn/` is NOT a grounding source for any v1.4 decision; v1.3-era artifact rebuilt by FUT-01. References allowed only in forward-pointing `19-CODE-DIVERGENCE.md`.
>
> **simulation_data role (Phase 19 specific — see D-17):** Phase 18 D-10 made `simulation_data/` authoritative grounding for `sampling_method.md` / FRAME-03 (the spec describes data the code generated; code wins on conflict). Phase 19 uses `simulation_data/` differently: as **supporting evidence** in `evidence/B-09.md` §5 to verify a negative claim (no force-softening epsilon exists in simulation_data to "mismatch" against). The Phase 19 spec contract is grounded in resolution doc §7.1-7.2, not in `simulation_data/`. Both roles compose with pending SCOPE-05.

---

<domain>
## Phase Boundary

Phase 19 locks the **physics and loss contracts** across the two framework specs (`ctl_instruction.md` and `pinn_architecture.md`) by adjudicating five findings (B-02, B-07, B-08, B-09, M4) and editing the spec passages they govern. Three of the five are EVID-05 contested (B-02, B-09, M4 — see D-16 ledger reclassification); two are uncontested (B-07, B-08). It delivers six requirements (PHYS-01 through PHYS-06).

Phase 19 ships:

1. **PHYS-01** — Raw-mass nondimensionalization locked: `D = (G·T²)^(1/3)` retained; mass-fraction alternative `D = (G·M_tot·T²)^(1/3)` documented as a future rewrite only. EVID-05 packet `evidence/B-02.md` records the dimensional-analysis proof and assigns the issue doc's 6.694 claim as "correct only under an unstated mass-fraction framework rewrite the issue doc did not also propose."
2. **PHYS-02** — Componentwise normalized-time derivative contract: autograd leaf is `u = t/T` (canonical, no chain-rule factors); chain-rule factors `v' = 2·dr'/dτ`, `a' = 4·d²r'/dτ²` apply ONLY to a code path that differentiates directly w.r.t. `τ = 2u-1`. Anti-pattern named: `torch.autograd.grad(r.sum(), u, create_graph=True)` is forbidden as a substitute for componentwise derivatives. Worked synthetic-trajectory test `r'(u) = [sin(2πu), cos(2πu), u²]` documented with symbolic derivatives. Canonical home: `pinn_architecture.md` §5.x; `ctl_instruction.md:962` retargets to a cross-reference (no duplicate math).
3. **PHYS-03** — One softening functional form across the framework: Plummer everywhere (`r_safe = sqrt(||r||² + ε²)`); `ε_train = 10⁻⁵` for training-time matched residual + Hamiltonian pair (`pinn_architecture.md` §3.2-3.3); `ε_inv = 10⁻¹⁰` for offline static invariants (`ctl_instruction.md` Step 3); `s_min` unsoftened. Anti-pattern named: do NOT mix additive vs Plummer; do NOT mix unmatched `(||r||+ε)⁻³` force with `(||r||+ε)⁻¹` potential. EVID-05 packet `evidence/B-09.md` records the issue doc's "5 orders of magnitude mismatch" as a category error (compared PINN-internal static vs training ε; no `simulation_data/` quantity to mismatch against). `simulation_data/` is inspected as supporting evidence (no force-softening; only IC-rejection threshold 0.05); not grounding for the spec contract.
4. **PHYS-04** — Energy term is a **soft conservation regularizer** using the analytic matched-Plummer Hamiltonian `H_ε`. The model predicts positions; it does NOT parameterize a Hamiltonian, so it is NOT an HNN. All "HNN-style" framing in `pinn_architecture.md` is replaced; the term "Hamiltonian" is retained where it means the analytic energy function `H_ε`.
5. **PHYS-05** — ALM restructured: removed from default training (the current pseudo-ALM-on-physics-MSE `+λ_p L_phys + (μ_p/2) L_phys²` formulation is rejected because squaring a nonnegative MSE is not a standard equality-constrained augmented Lagrangian). Optional ALM is **P2 only**, **scalar conservation constraints only** (`c_E`, `c_{L,α}`), **never** on dense ODE residual, **never** dual updates during L-BFGS, updates only between Adam epochs or deterministic refinement passes.
6. **PHYS-06** — M4 constraint-counting replacement: `ctl_instruction.md:914-915` "13 constraints for an 8-dimensional reduced phase space ensure over-determination and uniqueness" is replaced with resolution §10.4 reconstructive-gauge-fixed-encoding prose. EVID-05 packet `evidence/M4.md` credits the issue doc's arithmetic correction (`18 − 3 COM − 3 P − 3 SO(3) = 9`) in §5/§9 while making the resolution doc's reframing the locked spec contract.
7. **Total-loss replacement** (PHYS-04/05 coupled): `L_total = L_data + λ_IC L_IC + λ_phys L_phys^causal + λ_E L_E + λ_L L_L`. Adds **L_IC** (resolution §8.3, mandatory IC anchor at `u=0` for position AND velocity, `β_v = 1`). Adds **L_L** (resolution §8.6, componentwise Huber on relative angular-momentum drift, numerical-stability scale `ε_L = 10⁻⁸` distinct from softening). Causal weighting for L_phys per resolution §8.4 (`w_n = exp(-η_c·Σ stopgrad(R_m))`, `η_c = 1` default, stopgrad in weights by default). §8.7 warmup schedule replaces the legacy `λ_E`-only schedule.
8. EVID evidence packets for all five findings, following Phase 16 D-06 12-section template. §5/§7/§8/§9 mandatory for EVID-05 contested (B-02, B-09, M4); `Not contested` markers for B-07/B-08.
9. **`19-CODE-DIVERGENCE.md`** — FUT-01 hand-off inventory mirroring `17-CODE-DIVERGENCE.md` / `18-CODE-DIVERGENCE.md` schema (D-13 from Phase 18). Documents where `pinn/basic_architecture.py` and `pinn/data-processing-pipeline-full.py` diverge from the new Phase 19 contracts (additive softening, pseudo-ALM, `grad_outputs=torch.ones_like` AD, HNN-branded language).
10. **Issue Doc adjudication annotations** for all five Phase 19 findings — one line each appended to `pinn_instruction/issues/01-architecture-and-physics-foundations.md` per D-14.
11. **Phase 16 ledger M4-row reclassification** (D-16) — `Sources Disagree? NO → YES — EVID-05 required` with audit-note.
12. **Acceptance-check names** `AC-PHYS-01..06` reserved (AC-PHYS-02 is the Phase 19 invention; AC-PHYS-01/03/04/05/06 were pre-reserved by Phase 16). Pass criteria are Phase 21 VER-01 scope.

Phase 19 does NOT:

- Edit any file in `pinn/` (SCOPE-01 — v1.3-era artifact; FUT-01 rewrites from v1.4 specs).
- Touch `sampling_method.md` (Phase 18 D-11 confined Phase 18's FRAME-03 edits; Phase 20.5 owns Sobol coordinate-allocation; Phase 19 has no `sampling_method.md` work).
- Touch SIREN frequency / init / LayerNorm / `I_3` / `I_norm` (Phase 20 ARCH-01..05).
- Define numeric AC pass criteria or execute disposable probes (Phase 21 VER-01 / VER-04).
- Back-fill Phase 17 / Phase 18 Issue Doc rows with adjudication annotations (would require separate user instruction — see D-15).
- Edit the `## Source Issues` sections of the framework specs (Phase 21 VER-06 retires `SI-CTL-*` / `SI-PINN-*` entries with back-references).
- Mark any finding `VERIFIED` until the corresponding `AC-PHYS-NN` structural check passes (VER-05 discipline preserved; see D-12 P04 closure rule).

</domain>

<decisions>
## Implementation Decisions

### Decision Status Summary

Per CRITICAL GOVERNANCE rule. Plan-phase and execute-phase agents MUST consult this table before acting on any decision below. All entries are `LOCKED` via user instruction in the 2026-05-22 discussion; no `OPEN` gaps remain at context-gathering time.

| Decision | Status | Anchor | Plan-phase / execute-phase action |
|----------|--------|--------|-----------------------------------|
| **D-01** B-02 / PHYS-01 verdict = `accept-resolution` | ✅ LOCKED | User 2026-05-22 | Actionable. Spec: keep `D=(GT²)^(1/3)`; add raw-mass governing-convention prose; explicit false-positive note in evidence §9. |
| **D-02** B-09 / PHYS-03 verdict = `accept-resolution`; Plummer everywhere; dual-context ε | ✅ LOCKED | User 2026-05-22 | Actionable. Spec: additive → Plummer in residual, Hamiltonian, static V; `ε_train = 1e-5`, `ε_inv = 1e-10`; `s_min` unsoftened. |
| **D-03** M4 / PHYS-06 verdict = `accept-resolution` | ✅ LOCKED | User 2026-05-22 | Actionable. Spec: replace `ctl_instruction.md:914-915` with resolution §10.4 reconstructive-gauge-fixed-encoding prose. |
| **D-04** B-07 / PHYS-04 verdict = `accept-resolution` | ✅ LOCKED | User 2026-05-22 | Actionable. Spec: replace HNN-style framing with soft conservation regularizer language; retain "Hamiltonian" for analytic `H_ε`. |
| **D-05** B-08 / PHYS-05 verdict = `accept-resolution` | ✅ LOCKED | User 2026-05-22 | Actionable. Spec: remove pseudo-ALM from default; add P2-ablation appendix limited to scalar conservation constraints. |
| **D-06** Softening unified to Plummer everywhere; context-specific ε values | ✅ LOCKED | User 2026-05-22 | Actionable. Spec edits in 4-6 locations across both files; cited line numbers are anchors, executor `rg`-driven for full edit set. |
| **D-07** Total-loss replacement contract | ✅ LOCKED | User 2026-05-22 | Actionable. `L_total = L_data + λ_IC L_IC + λ_phys L_phys^causal + λ_E L_E + λ_L L_L`; adds L_IC and L_L; removes ALM term from default. |
| **D-08** PHYS-02 AD contract: primary in `pinn_architecture.md`; ctl side cross-references | ✅ LOCKED | User 2026-05-22 | Actionable. Math + short illustrative Python listing. Canonical leaf = `u`; factors only on τ-leaf path. |
| **D-09** HNN reframing scope: full prose rewrite, not formula-only patch | ✅ LOCKED | User 2026-05-22 | Actionable. Affects title/intro, §1.x, §3 overview, §3.2 ALM block, §3.3 HNN section, §4.1, summary table, plus `ctl_instruction.md` total-loss block. |
| **D-10** Causal weighting + stopgrad as default L_phys contract | ✅ LOCKED | User 2026-05-22 | Actionable. Resolution §8.4: `w_n = exp(-η_c·Σ stopgrad(R_m))`, `η_c = 1`. PHYS-05's "or otherwise justified" wording leaves a future-flexibility note. |
| **D-11** M4 spec replacement prose includes cross-ref to Phase 17 IO-02 + Phase 18 FRAME-01 | ✅ LOCKED | Claude's discretion per user-approved precedent | Actionable. Resolution §10.4 prose + explicit "as locked by Phase 17 (IO-02) and Phase 18 (FRAME-01)" anchor. |
| **D-12** 4-plan decomposition (P01 ctl_instruction / P02 pinn_architecture formulas / P03 pinn_architecture prose / P04 evidence + ledger + divergence) | ✅ LOCKED | User 2026-05-22 | Actionable. P01 + P02 parallel (different files); P03 blocked on P02; P04 blocked on Waves 1–2. |
| **D-13** AC-PHYS-02 invented; pass criteria are Phase 21 VER-01 scope | ✅ LOCKED | User 2026-05-22 | Actionable. Phase 19 reserves the name; do NOT invent pass criteria. |
| **D-14** Issue Doc adjudication annotation convention (one-line, verdict-agnostic) | ✅ LOCKED | User 2026-05-22 | Actionable. Format: `**Adjudicated Phase 19:** `<verdict>`. See `evidence/<id>.md`.` — append to the relevant table row; original row text stays verbatim. |
| **D-15** D-14 annotation scope: forward-apply to all five Phase 19 findings (incl. uncontested); NO back-fill of Phase 17/18 | ✅ LOCKED | User 2026-05-22 | Actionable. B-07/B-08 get `Not contested` markers. Back-fill of earlier phases requires separate user instruction. |
| **D-16** Phase 16 ledger M4-row reclassification `NO → YES — EVID-05 required` with audit-note | ✅ LOCKED | User 2026-05-22 | Actionable. Single-row factual correction + per-finding subsection note. NOT a new-schema invention. |
| **D-17** `simulation_data/` role in `evidence/B-09.md` §5 = supporting evidence, NOT grounding for new spec decisions | ✅ LOCKED | User 2026-05-22 | Actionable. Cite inspected files + finding (no force-softening; only IC-rejection threshold 0.05) + implication (no quantity to mismatch). Differs from Phase 18 D-10 FRAME-03 grounding role. |
| **D-18** Symbol renames: `epsilon_soft → epsilon_train`; introduce `epsilon_inv`; matches resolution-doc convention | ✅ LOCKED | User 2026-05-22 | Actionable. Mechanical cleanup; reduces ambiguity. `η_gauge` (Phase 18 D-14) remains numerical-geometry guard — clean separation preserved. |
| **D-19** `19-CODE-DIVERGENCE.md` mirrors `17/18-CODE-DIVERGENCE.md` schema; row-level FUT-01 priority hints non-binding | ✅ LOCKED | Phase 17 D-14 / Phase 18 D-13 precedent | Actionable. Schema identical; content scope = Phase 19's divergences (see Specific Ideas). |

**Summary:** 19 context-gathering decisions are LOCKED. No OPEN gaps existed at context-gathering time; `GAP-19-01` was opened during the 2026-05-22 plan-repair pass for the ungrounded numeric `epsilon_H` default. Plans P01/P02 may proceed only on disjoint spec-file edits and must serialize shared lifecycle artifacts; any P02 step requiring a concrete `epsilon_H` value is blocked until user instruction resolves `GAP-19-01`.

---

### Tier A — Verdicts on the five Phase 19 findings

The resolution doc (`ctl_pinn_resolution.md`) is the **default verdict source** per the 2026-05-18 milestone directive: the agent transcribes its positions into framework-spec edits unless EVID-05 surfaces concrete evidence that the position fails physics, code, or spec verification. (Per directive 2026-05-19, live `pinn/` code is NOT part of the verification basis.)

#### D-01 (B-02 / PHYS-01 verdict — D-formula)

`accept-resolution`. Lock `D = (G·T²)^(1/3) ≈ 4.6416` with raw masses throughout the framework. The issue doc's `D = (G·M_tot·T²)^(1/3) = 6.694` is correct **only** under a mass-fraction convention rewrite that would require touching every residual, Hamiltonian, angular-momentum, COM, and invariant formula in the spec. The issue doc did not propose that downstream rewrite — it framed the change as a "formula error" when in fact it was an unstated convention change.

- **Why:** Resolution doc §3.1–3.2 (lines 137–207) gives a complete dimensional-analysis proof. Substituting `r = D·r'`, `t = T·u` into Newton's equation and demanding the dimensionless residual `d²r'/du² = Σ m_j (r_j'−r_i') / ||r_j'−r_i'||³` (with raw masses) forces `D³ = GT²`. Using 6.694 with raw masses inserts a phantom `1/M_tot` factor.
- **How to apply (P01):** Evidence packet `evidence/B-02.md` records the 4-source EVID-05 framing (resolution §3.1–3.2, issue doc B-02 row, framework specs, first-principles dimensional analysis). §9 (which source was correct): resolution doc correct on dimensional grounds; issue doc correct only conditionally on a framework rewrite it did not also propose. Spec edit adds an explicit "Governing Mathematical Convention" anchor in `ctl_instruction.md` Step 2.5 (per resolution §10.1 patch text) that names raw-mass as locked and derives D as a consequence.

#### D-02 (B-09 / PHYS-03 verdict — softening strategy)

`accept-resolution`. Lock the matched-Plummer-pair-within-training + separate static-invariant ε contract:
- `ε_train = 10⁻⁵` (training: residual + Hamiltonian, same `r_safe`).
- `ε_inv = 10⁻¹⁰` (offline static invariants — `V` in `ctl_instruction.md` Step 3).
- `s_min` **unsoftened** (resolution §7.2: "Softening never enters curriculum collision gates").

The issue doc's "5 orders of magnitude mismatch" framing is a category error — it compared PINN-internal static-invariant ε (1e-10) against PINN-internal training ε (1e-5), both PINN-side. There is no `simulation_data/` quantity to mismatch against (`simulation_data/` uses no force-softening; its `epsilon = 0.05` is an IC minimum-separation rejection threshold; Brutus is arbitrary-precision; metrics use unsoftened separations — see D-17).

- **Why:** Resolution doc §7.1–7.2 (lines 743–824) gives matched Plummer pairs for both training and static contexts. The two contexts (training vs static-invariant) are conceptually separate by purpose, not by hardware (issue doc's CPU/float64 vs GPU/float32 framing is a contingent justification, not the contract).
- **How to apply (P02):** Evidence packet `evidence/B-09.md` records the matched-pair structure + simulation_data verification subsection (D-17). §9: issue doc partly correct on separating static-invariant ε from training-time softening; wrong/overstated on the mismatch framing; incomplete on functional form. Resolution doc correct on the final contract.

#### D-03 (M4 / PHYS-06 verdict — constraint-counting replacement)

`accept-resolution`. Replace `ctl_instruction.md:914-915` with resolution §10.4 (lines 1160–1175) reconstructive-gauge-fixed-encoding prose: "The final IC13 is a redundant but reconstructive fixed-gauge initial-state encoding. It is not justified by constraint counting. Its validity comes from COM removal, zero-momentum boost, canonical ordering, canonical rotation, and retention of the independent Jacobi position/velocity degrees of freedom." (See D-11 for cross-reference polish to Phase 17/18.)

- **Why:** Under Phase 17 (D-01) Jacobi-state IC13, the validity of the IC vector has nothing to do with counting against a reduced phase space. It comes from being a reconstructive gauge-fixed encoding given the canonical preprocessing pipeline (Phase 18 FRAME-01). Counting against an "8-dimensional reduced phase space" is mathematically wrong (the correct count is 9, per issue doc M4) AND is a misframing — the IC13 design isn't derived from constraint counting at all.
- **Sources disagree:** Issue doc M4 (line 86) keeps the constraint-counting framing and only fixes the arithmetic ("9 constraints reduce 18-DOF to 9 dimensions"); resolution doc §10.4 rejects constraint counting altogether. EVID-05 adjudication required — see D-16 for the Phase 16 ledger reclassification.
- **How to apply (P01):** Evidence packet `evidence/M4.md` records all four EVID-05 sections (§5 first-principles dimension accounting credits the issue doc's `18 − 3 COM − 3 P − 3 SO(3) = 9` arithmetic; §7 root-cause ambiguity = pre-Phase-17 IC vector design treated as a DOF-reduction artifact; §8 locked convention = reconstructive gauge-fixed encoding; §9 per-claim correctness — issue doc arithmetically correct on counting but wrong on relevance under Jacobi-state IC13; resolution doc correct on the framing).

#### D-04 (B-07 / PHYS-04 verdict — energy regularizer / not HNN)

`accept-resolution`. The energy term is a **soft conservation regularizer** using the analytic matched-Plummer Hamiltonian `H_ε`. The network predicts positions; it does NOT parameterize a Hamiltonian, so it is NOT an HNN. The HNN-style framing in the current spec is misleading and gets replaced wholesale (see D-09 for scope).

- **Why:** PHYS-04 is explicit: "The energy term is described as a soft conservation regularizer rather than an HNN unless the model actually parameterizes a Hamiltonian." The model in this framework outputs 9D positions (Phase 17 D-02); the loss penalizes deviations of the analytic `H_ε(r_θ', v_θ')` from `H_0` via Huber. That is a soft constraint enforced via a penalty term, not an architectural HNN.
- **How to apply (P02, P03):** P02 lands the formula reframing (`L_E` definition references the matched-Plummer `H_ε`); P03 lands the prose reframing (HNN-style language replaced throughout — see D-09). Evidence packet `evidence/B-07.md` is uncontested → §5/§7/§8/§9 carry `Not contested` markers per Phase 17/18 precedent.

#### D-05 (B-08 / PHYS-05 verdict — ALM scope restriction)

`accept-resolution`. Remove pseudo-ALM from default training. The current `L_total = L_data + λ_p L_phys + (μ_p/2) L_phys² + λ_E(k) L_energy` formulation is rejected because squaring a nonnegative MSE (`L_phys²`) produces a quartic residual that does not represent a standard equality-constrained augmented Lagrangian (resolution doc §8.8 reasoning). Replace per resolution §10.8 patch text (see D-07).

Optional ALM is **P2 only**, **scalar conservation constraints only** (`c_E = RMS_n(ΔH_n)`, `c_{L,α} = RMS_n((L'_θ,α(u_n) − L_0,α') / L_scale)`):
- Never apply ALM to the dense ODE residual.
- Never update dual variables during L-BFGS.
- Update dual variables only between Adam epochs or between deterministic refinement passes.
- Log constraint values before and after each update.
- Lives in a dedicated `## 4.x Optional ALM ablation (P2)` subsection after the default-contract sections.

- **How to apply (P02, P03):** P02 lands the formula replacement; P03 lands the prose cleanup of the current ALM block (`pinn_architecture.md:483-532, 663-666`; `ctl_instruction.md:1090-1113`) and adds the P2-ablation appendix. Evidence packet `evidence/B-08.md` uncontested → `Not contested` markers.

### Tier B — Spec contract decisions (Plummer form, total loss, AD contract, M4 prose, HNN/ALM scope)

#### D-06 (One softening form across the framework; context-specific ε values)

Plummer-sqrt `r_safe = sqrt(||r||² + ε²)` everywhere a softened force/potential pair appears:
- `pinn_architecture.md:416` physics residual — additive → Plummer with `ε_train = 1e-5`.
- `pinn_architecture.md:549` energy regularizer — additive → Plummer with `ε_train = 1e-5` (same as residual; matched pair).
- `pinn_architecture.md:600, 613` Python `compute_initial_energy` listing — same.
- `ctl_instruction.md:664` static-invariant `V` — additive → Plummer with `ε_inv = 1e-10` (matches resolution §7.2 verbatim).

`s_min` (line 667) remains the unsoftened geometric quantity `min_{i<j} ||r_i' − r_j'||`. Anti-pattern enforcement (resolution §7.1, lines 772–784): "Do not mix `(||r||+ε)⁻³` with `(||r||+ε)⁻¹`. Do not mix additive vs Plummer forms. The chosen pair MUST appear identically in residual and Hamiltonian."

**Practical note (corrected by user):** At `ε_inv = 10⁻¹⁰` and IC-rejection floor `r ≥ 0.05`, additive's first-order relative bias from Newtonian is `≈ ε/r ≈ 2·10⁻⁹`; Plummer's bias is `≈ ε²/(2r²) ≈ 2·10⁻¹⁸`. Both negligible; Plummer is mathematically cleaner and matches resolution §7.2 verbatim.

**Clean separation from Phase 18 D-14:** `η_gauge = 10⁻⁸` is a dimensionless rotation-gauge degeneracy tolerance — NOT a physics softening parameter and NOT tied to `ε_train` or `ε_inv`. Phase 19's spec text should NOT introduce any cross-reference between them.

#### D-07 (Total-loss replacement contract)

Per resolution §8.1 + §10.8, the default training loss is:

```
L_total = L_data + λ_IC · L_IC + λ_phys · L_phys^causal + λ_E · L_E + λ_L · L_L
```

Replaces the current pseudo-ALM formulation `L_data + λ_p L_phys + (μ_p/2) L_phys² + λ_E(k) L_energy`.

| Term | Definition source | Mandatory additions vs current spec |
|---|---|---|
| `L_data` | Resolution §8.2 | Huber, `δ_r = 1` default (current `pinn_architecture.md` data-loss prose uses MAE/L1 — change to Huber). |
| `L_IC` | Resolution §8.3 | **NEW.** Position anchor `L_IC,r` + velocity anchor `L_IC,v` at `u = 0`; `L_IC = L_IC,r + β_v · L_IC,v`, `β_v = 1`. `λ_IC = 1` default, ablation range `[0.1, 10]`. |
| `L_phys^causal` | Resolution §8.4 | Causal weights `w_n = exp(-η_c · Σ_{m<n} stopgrad(R̄_m))`, `w_1 = 1`, `η_c = 1` default. **stopgrad in weights by default** to prevent the weight mechanism from becoming an adversarial term. |
| `L_E` | Resolution §8.5 + D-04 reframing | Huber on relative drift `ΔH_n = (H_ε(r_θ', v_θ') − H_ε(r_0', v_0')) / (|H_ε(r_0', v_0')| + ε_H)`, `δ = 1.0`. Soft conservation regularizer (NOT HNN). `ε_H` is symbolic until `GAP-19-01` is resolved; do not assign a numeric default in Phase 19 execution plans. |
| `L_L` | Resolution §8.6 | **NEW.** Componentwise Huber on relative angular-momentum drift, `L_scale = ‖L_0'‖ + ε_L`, `ε_L = 10⁻⁸` numerical-stability scale (distinct from softening — see D-06). |

**Warmup schedule** (resolution §8.7) replaces the legacy `λ_E(k) = 10^(k-3)`-only schedule:

- `I_warm = min(2000, 0.1 · N_Adam,k)`
- `λ_phys(k, i) = λ_phys^max(k) · min(1, i/I_warm)`, default `λ_phys^max(k) = 1`
- `λ_E^max(k) = λ_L^max(k) = {0 for k∈{0,1}; 10^(k-4) for k∈{2,3,4}; 1 for k∈{5,6}}`
- `λ_E(k, i)` and `λ_L(k, i)` warm-up linearly with `i/I_warm`
- `λ_IC = 1` default, ablation `[0.1, 10]`

**Optimizer-phase semantics** (PHYS-05 explicit requirement):
- During Adam epochs: hyperparameters (λ values) may be scheduled per the warmup schedule; no dual variables updated.
- During L-BFGS phase: λ values are frozen; no dual updates inside a line search.
- Stage-boundary transitions: re-warmup applies per the new stage's `λ_phys^max` / `λ_E^max` / `λ_L^max`.
- Optional ALM P2 ablation (D-05): dual updates only between Adam epochs or between deterministic refinement passes, never inside L-BFGS.

#### D-08 (PHYS-02 AD contract placement and format)

Canonical home: `pinn_architecture.md` §5.x (the area Phase 17 forward-referenced at line 826). `ctl_instruction.md:962` retargets to a cross-reference (`"see pinn_architecture.md §5.x (PHYS-02)"`) — single source of truth, no duplicate math.

Format: math + short illustrative Python listing (spec-level, not a FUT-01 implementation harness).

Content (resolution §3.3 + §6.4 + §10.6):

1. **Three-layer separation** `(t, r, v)_raw → (u, r', v')_physics → (τ, IC13)_network` with `u = t/T`, `τ = 2u − 1`.
2. **Canonical leaf = `u`.** If the code path differentiates w.r.t. `u`, then `v' = dr'/du` and `a' = d²r'/du²` directly (no chain-rule factors). The 2× / 4× chain-rule factors `v' = 2 · dr'/dτ`, `a' = 4 · d²r'/dτ²` apply **only** to a code path that differentiates directly w.r.t. `τ = 2u − 1`. *(Refines the resolution doc's contract — the factors are conditional on the leaf choice.)*
3. **Anti-pattern warning:**
   - **Forbidden:** `torch.autograd.grad(r.sum(), u, create_graph=True)` as a substitute for componentwise derivatives. This gives a vector-Jacobian product against an all-ones covector, not the nine derivatives the residual and Hamiltonian require.
   - **Acceptable:** `torch.func.jacrev` + `vmap`; explicit loop over the 9 projected output components; equivalent full-Jacobian/Hessian method.
4. **Worked synthetic-trajectory test:** Use the **exact PHYS-02 trajectory** `r'(u) = [sin(2πu), cos(2πu), u²]`. Do NOT substitute the resolution doc's simpler `τ³` smoke test. Symbolic derivatives stated in the spec:
   - `dr'/du = [2π cos(2πu), −2π sin(2πu), 2u]`
   - `d²r'/du² = [−4π² sin(2πu), −4π² cos(2πu), 2]`
   AD outputs must match symbolic to numerical tolerance. Executable tolerance and the disposable probe belong to Phase 21 VER-04 / `AC-PHYS-02`.

The short Python listing in the spec illustrates the accepted pattern (jacrev + vmap, OR explicit per-component loop). It is spec-illustrative, not an FUT-01 implementation; the listing's exact pattern choice is Claude's discretion (the planner picks whichever is cleaner against current spec style).

#### D-09 (HNN reframing scope — full prose rewrite)

The HNN-style framing in `pinn_architecture.md` is spread across title/intro, `§1.x` overview, `§3` loss-overview prose, `§3.2` ALM implementation block, `§3.3` HNN Energy section title and body, `§4.1` Adaptive Loss Balancing prose, the summary table (lines 866–870), plus the `ctl_instruction.md:1095, 1098-1113` total-loss block. Leaving any of these as active prose would contradict PHYS-04/05.

**Terminology nuance (user-stated):** Keep "Hamiltonian" where it means the analytic energy function `H_ε`. Remove "HNN-style" and any architectural-HNN claims (e.g., "borrowing the primary benefit of an HNN", "HNN architecture", "HNN-style loss term"). The replacement language is "soft conservation regularizer" + descriptions of the soft constraint mechanism (penalty term in the loss).

P02 lands the formula changes; P03 lands the prose cleanup. AC-PHYS-04 does not pass until the final coherent rewrite is in place across both files (P03 closure).

#### D-10 (Causal weighting + stopgrad as default L_phys contract)

Resolution §8.4 `w_n = exp(-η_c · Σ_{m<n} stopgrad(R̄_m))`, `w_1 = 1`, `η_c = 1` default, with clipping of the exponent to avoid underflow. `stopgrad` in weights by default — prevents the weight mechanism from becoming an unintended adversarial term.

PHYS-05's wording "dense ODE residuals use a causal **or otherwise justified** residual weighting contract" leaves room for future-flexibility alternatives, but the spec locks causal-with-stopgrad as the default. Alternatives may be documented as P2 ablations only.

#### D-11 (M4 spec replacement prose: cross-reference Phase 17/18)

The replacement prose for `ctl_instruction.md:914-915` (per D-03) uses resolution §10.4 verbatim base, polished with an explicit cross-reference: "...as locked by Phase 17 (IO-02) and Phase 18 (FRAME-01)..." — anchors the validity argument in the upstream contracts so future readers know where the gauge-fixing comes from. This is Claude's discretion under Phase 17/18 cross-reference precedent; planner finalizes exact wording.

### Tier C — Process decisions

#### D-12 (4-plan decomposition)

Phase 19 uses 4 plans for review safety. Treated as execution-plan decomposition, not a semantic physics decision. The accepted contract is still the unified Option 1 contract from the discussion; AC-PHYS-04/05 do not pass until the final coherent rewrite is in place across both `ctl_instruction.md` and `pinn_architecture.md` (P03 closure).

- **P01 (Wave 1, can parallel with P02 only for disjoint spec-file edits): `ctl_instruction.md` edits + EVID-05 ctl-side adjudications.**
  - Add raw-mass governing-convention prose to Step 2.5 (D-01, resolution §10.1 patch).
  - Static-invariant `V` (line 664) additive → Plummer with `ε_inv = 10⁻¹⁰` (D-02 / D-06).
  - Replace M4 constraint-counting sentence (line 914-915) with resolution §10.4 reconstructive-gauge-fixed-encoding prose, with Phase 17/18 cross-reference (D-03 / D-11).
  - Replace total-loss block (lines 1095, 1098-1113) with the new contract per D-07 — coordinate with P02 so both files land the same total-loss equation.
  - Evidence packets `evidence/B-02.md`, `evidence/M4.md` (both EVID-05 — full §5/§7/§8/§9 treatment).
  - Issue Doc annotations for B-02 and M4 per D-14, serialized with other Issue Doc annotations.
  - Phase 16 ledger M4-row reclassification per D-16 (`Sources Disagree? NO → YES — EVID-05 required`) + per-finding subsection audit note, serialized with all other ledger writes.
  - Ledger transitions: B-02 PENDING→IN_PROGRESS→FIX_APPLIED; M4 PENDING→IN_PROGRESS→FIX_APPLIED. Shared `16-ISSUE-LEDGER.md` and Issue Doc writes must be handled by a single coordination task or explicit serial order; P01/P02 parallelism applies only to disjoint spec-file edits.

- **P02 (Wave 1, parallel with P01 only for disjoint spec-file edits): `pinn_architecture.md` formula / contract changes.**
  - PHYS-02 AD contract + worked synthetic-trajectory test (D-08).
  - PHYS-03 Plummer-form change in residual (line 416), Hamiltonian (line 549), Python Listings (lines 583-616) — `ε_train = 10⁻⁵` (D-06).
  - PHYS-04 `L_E` formula reframed as soft conservation regularizer using matched-Plummer `H_ε`.
  - PHYS-05 total-loss replacement per D-07.
  - §8.7 warmup schedule (replaces legacy `λ_E`-only schedule).
  - Evidence packets `evidence/B-07.md`, `evidence/B-08.md` (`Not contested` markers), `evidence/B-09.md` (EVID-05 — full §5/§7/§8/§9 + structured `simulation_data` verification subsection per D-17).
  - Issue Doc annotations for B-07, B-08, B-09 per D-14, serialized with other Issue Doc annotations.
  - Ledger transitions: B-07, B-08, B-09 PENDING→IN_PROGRESS→FIX_APPLIED. Shared `16-ISSUE-LEDGER.md` and Issue Doc writes must be handled by a single coordination task or explicit serial order; P01/P02 parallelism applies only to disjoint spec-file edits.

- **P03 (Wave 2, blocked on P02): `pinn_architecture.md` prose cleanup + cross-reference validation.**
  - HNN reframing throughout (`§1.x` intro, `§3.3` title + body, `§4.1` prose, summary table) per D-09.
  - Optional ALM P2-ablation appendix per D-05.
  - Cross-references between `pinn_architecture.md` and `ctl_instruction.md` validated (forward-refs to Phase 19 satisfied; total-loss text matches across files).
  - `ctl_instruction.md:879-880` velocity-output legacy fragments swept (if any survive after Phase 17/18 cleanup — verify).
  - No new ledger transitions; this is prose cleanup that closes out PHYS-04/05 coherence.

- **P04 (Wave 3, blocked on Waves 1–2): `19-CODE-DIVERGENCE.md` + evidence-packet closure + ledger finalization + AC structural checks.**
  - Write `19-CODE-DIVERGENCE.md` mirroring `17/18-CODE-DIVERGENCE.md` schema (D-19). Content scope: pseudo-ALM machinery in live code (full restructure); additive softening in residual + energy + V (Plummer change); no `L_IC` anchor (addition); no `L_L` angular-momentum loss (addition); `grad_outputs=torch.ones_like` AD anti-pattern (PHYS-02); symbol rename `epsilon_soft → epsilon_train`; HNN-branded variable/method names (if any).
  - AC-PHYS-02 reservation appended to `16-ISSUE-LEDGER.md` lifecycle notes (or `pinn_instruction/issues/...` if Phase 16 reserved them there — verify; precedent says ledger reservation).
  - Final ledger transitions: B-02, B-07, B-08, B-09, M4 FIX_APPLIED → VERIFIED, gated on each finding's `AC-PHYS-NN` structural check passing in the Phase 19 verification step.
  - Phase 19 verification artifact (`19-VERIFICATION.md`) runs the AC-PHYS structural checks (text/structural; numeric is Phase 21 VER-04 scope).
  - Confirm no in-scope finding exits Phase 19 at IN_PROGRESS or FIX_APPLIED (Phase 16 D-12 exit gate).

#### D-13 (`AC-PHYS-02` invention; Phase 16 reservations preserved)

Phase 16 ledger reserved AC-PHYS-01, AC-PHYS-03, AC-PHYS-04, AC-PHYS-05, AC-PHYS-06 but not AC-PHYS-02. PHYS-02's worked synthetic-trajectory test naturally maps to `AC-PHYS-02`. Pattern mirrors Phase 17 GAP-17-02 (AC-IO-04 invention, RESOLVED-WITH-INSTRUCTION: approve invention).

Phase 19 reserves the name; pass criteria are Phase 21 VER-01 scope per Phase 16 D-13 — do NOT invent. Structural close criteria for Phase 19 verification: "PHYS-02 AD contract present in `pinn_architecture.md` §5.x; canonical leaf named as `u`; chain-rule factors stated conditionally for `τ`-leaf; anti-pattern warning present naming `torch.autograd.grad(r.sum(), u, ...)` as forbidden + acceptable patterns named; synthetic-trajectory `r'(u) = [sin(2πu), cos(2πu), u²]` and symbolic derivatives present; `ctl_instruction.md:962` retargeted to cross-reference, no duplicate math."

| AC name | Findings | Pass-criteria scope |
|---|---|---|
| AC-PHYS-01 | B-02 | Phase 21 VER-01 (numeric); Phase 19 structural = D-formula prose present, mass-fraction alternative documented as future-rewrite-only, no other formula in either spec. |
| AC-PHYS-02 | PHYS-02 (no finding ID — Phase 19 invention) | Phase 21 VER-01 (numeric AD test); Phase 19 structural = AD contract per D-08 present. |
| AC-PHYS-03 | B-09 | Phase 21 VER-01 (numeric); Phase 19 structural = Plummer in both files, `ε_train = 10⁻⁵` / `ε_inv = 10⁻¹⁰` named, `s_min` unsoftened, anti-pattern warning present. |
| AC-PHYS-04 | B-07 | Phase 21 VER-01 (numeric energy-drift probe); Phase 19 structural = HNN-style framing removed, `L_E` reframed as soft conservation regularizer, matched-Plummer `H_ε` retained. |
| AC-PHYS-05 | B-08 | Phase 21 VER-01 (numeric loss-stability dry run); Phase 19 structural = pseudo-ALM removed from default, P2-ablation appendix present with scalar-conservation-only scope, optimizer-phase semantics named. |
| AC-PHYS-06 | M4 | Phase 21 VER-01 (numeric — if any; M4 is largely prose); Phase 19 structural = `ctl_instruction.md:914-915` replaced with reconstructive-gauge-fixed-encoding prose with Phase 17/18 cross-references. |

#### D-14 (Issue Doc adjudication annotation convention — NEW milestone-wide pattern)

The agent does NOT rewrite Issue Doc content; Issue Docs are historical audit records. For each Phase 19 finding, append exactly ONE annotation inside the relevant existing GFM table row/cell in `pinn_instruction/issues/01-architecture-and-physics-foundations.md`:

```
**Adjudicated Phase 19:** `<verdict>`. See `evidence/<id>.md`.
```

Original row text stays verbatim and the table row's column count must remain unchanged; do not add a free-standing line that breaks the table. The evidence packet plus the resolution doc are the correction mechanism. This convention is established by user instruction 2026-05-22 and supersedes any prior pattern that may have rewritten issue-doc content. (Resolution doc remains the default verdict source per directive 2026-05-18; agent transcribes its positions into spec edits unless EVID-05 surfaces concrete evidence it fails.)

#### D-15 (D-14 annotation scope — forward-only for Phase 19, no back-fill)

Apply D-14 annotations forward to **all** five Phase 19 findings:
- B-02 → `**Adjudicated Phase 19:** \`accept-resolution\`. See \`evidence/B-02.md\`.`
- B-07 → same format, `accept-resolution`, with `Not contested` recorded in the evidence packet.
- B-08 → same format, `accept-resolution`, `Not contested` in packet.
- B-09 → same format, `accept-resolution`, EVID-05 packet.
- M4 → same format, `accept-resolution`, EVID-05 packet.

Do **NOT** retroactively back-fill Phase 17 (B-03, B-04, B-06, M1, M2) or Phase 18 (B-05, M3) issue-doc rows. Back-fill requires separate user instruction.

#### D-16 (Phase 16 ledger M4-row reclassification)

Phase 16 ledger `16-ISSUE-LEDGER.md` M4 row currently shows `Sources Disagree? = NO`. REQUIREMENTS.md PHYS-06 explicitly says EVID-05 adjudication required; the actual source positions disagree (issue doc keeps counting framing with arithmetic fix; resolution doc rejects counting altogether — see D-03). Phase 19 amends the row from `NO → YES — EVID-05 required` and appends to the M4 per-finding subsection:

```
Phase 19 reclassification (2026-05-22): Sources Disagree changed from NO to YES — EVID-05 required.
Phase 16 seed marked NO in error; the requirement language (PHYS-06) and actual source positions
both indicate EVID-05 is required. Adjudicated in Phase 19 P01 per `evidence/M4.md`.
```

This is a factual ledger correction after surfacing the discrepancy, NOT a new schema invention. Lifecycle rules (Phase 16 D-04, D-09 through D-12) are unchanged.

#### D-17 (`simulation_data/` role in Phase 19 = supporting evidence, NOT grounding)

For `evidence/B-09.md` §5 (first-principles physics check), use a structured `simulation_data` verification subsection:

```markdown
### simulation_data check (supporting evidence; not grounding for new spec)

Inspected files:
- `simulation_data/Scripts/ic_generation/ic_generation_utils.py:60-81, 223, 261, 572`
- `simulation_data/Scripts/ic_generation/generate_ics.py:40`
- `simulation_data/Scripts/metrics_calculation/calculate_metrics.py:193-207, 266-284`
- `simulation_data/Documentation/README.md:385`

Finding: simulation_data uses NO force-softening epsilon anywhere.
- Only "epsilon": `epsilon = 0.05` as an IC minimum-separation rejection threshold during
  sampling (rejects IC triangles with any pairwise distance ≤ 0.05 in G=1 natural units).
- Brutus integrator: arbitrary-precision GMP/MPFR with extrapolation; no Plummer or additive
  softening.
- Metrics calculation: pure `sqrt(dx²+dy²+dz²)` with no softening.

Implication: the issue doc's "5 orders of magnitude mismatch" framing compared PINN-internal
static-invariant ε (1e-10) against PINN-internal training ε (1e-5), both PINN-side. No
simulation_data quantity exists to "mismatch" against. The matched Plummer contract is
purely PINN-internal.

Role of this check: supporting evidence (verifying a negative claim), NOT grounding for new
v1.4 spec decisions. The PHYS-03 spec contract is grounded in resolution doc §7.1-7.2.
Distinct from Phase 18 D-10 where simulation_data IS grounding for sampling_method.md /
FRAME-03 (the spec describes data generated by the code; code wins on conflict).
```

#### D-18 (Symbol renames — mechanical cleanup matching resolution-doc convention)

- Current spec `\epsilon_{soft}` / `\varepsilon` (additive context) → `\epsilon_{train}` per resolution-doc convention. Affects every reference in the rewritten sections.
- Introduce `\epsilon_{inv}` as the symbol for the static-invariant softening (was bare `\varepsilon = 10^{-10}` in `ctl_instruction.md:669`).
- Preserve `\eta_{gauge}` (Phase 18 D-14) as the numerical rotation-gauge tolerance — distinct symbol family from physics softening. Spec text should NOT introduce any cross-reference between `\eta_{gauge}` and `\epsilon_{train}` / `\epsilon_{inv}`.
- `r_{safe}` symbol for the Plummer denominator `\sqrt{||r_j' - r_i'||^2 + \epsilon^2}` is recommended where the formula is reused (e.g., `r_{safe,ij} = \sqrt{||r_j' - r_i'||^2 + \epsilon_{train}^2}`).

Treat cited line numbers in P01/P02 as anchors, NOT the full edit set. The executor `rg`s for all old additive forms and old symbols (`epsilon_soft`, bare `\varepsilon`, `(||r|| + eps)`, `eps_soft`) and updates related prose / listings / numerical notes / anti-pattern wording.

#### D-19 (`19-CODE-DIVERGENCE.md` schema — mirrors Phase 17 D-14 / Phase 18 D-13)

5-column Markdown table: `Surface | Live code (file:line) | Spec target (Phase 19 decision) | FUT-01 item | FUT-01 priority`. Row-level `FUT-01 priority` values are non-binding FUT-01 hand-off hints; FUT-01 planning may revise after reading the accumulated Phase 17/18/19/20 divergence files and `pinn/STATUS.md` (added Phase 21). Live `pinn/` references in this artifact are FUT-01 hand-off coordinates only; they are not v1.4 grounding sources.

Phase 19's divergence rows (initial list; planner finalizes):

| Surface | Live code (file:line) | Spec target (Phase 19 decision) | FUT-01 item | FUT-01 priority |
|---|---|---|---|---|
| Force softening form (residual) | additive `1/(||r||+eps_soft)³` (`pinn/data-processing-pipeline-full.py`, `pinn/basic_architecture.py` if any; exact lines verified in FUT-01) | Plummer `1/r_safe³` with `r_safe = sqrt(||r||²+ε_train²)` | Replace training residual denominator with matched Plummer form. | high |
| Energy softening form | additive `1/(||r||+eps_soft)` (`pinn/data-processing-pipeline-full.py:H_0` calc; exact lines verified in FUT-01) | Plummer `1/r_safe` with same `ε_train` | Replace analytic energy denominator with matched Plummer potential. | high |
| Static-invariant V form | additive if present in metrics-generation code; exact lines verified in FUT-01 | Plummer with `ε_inv = 10⁻¹⁰` (offline only) | Align offline invariant computation with PHYS-03 static-invariant contract. | medium |
| AD method | `grad_outputs=torch.ones_like(positions)` (`pinn/basic_architecture.py` `compute_derivatives`; exact lines verified in FUT-01) | componentwise (jacrev+vmap or explicit per-component loop) | Replace all-ones VJP derivative shortcut with componentwise derivative contract. | high |
| Loss composition | `L_data + λ_p L_phys + (μ_p/2) L_phys² + λ_E(k) L_energy` | `L_data + λ_IC L_IC + λ_phys L_phys^causal + λ_E L_E + λ_L L_L` | Rewrite default loss composition and remove pseudo-ALM default. | high |
| L_IC anchor | absent | mandatory at `u=0` for both position and velocity | Add initial-condition anchor loss. | high |
| L_L angular-momentum loss | absent | componentwise Huber with `ε_L = 10⁻⁸` | Add angular-momentum conservation loss. | high |
| Causal weighting | absent | `w_n = exp(-η_c · Σ stopgrad(R̄_m))` with stopgrad | Add causal residual weighting. | medium |
| ALM machinery | `λ_p`, `μ_p` updates per step with RMSprop-stabilized `μ_p ← γ/sqrt(v_p+ε)` | removed from default; P2 ablation only, scalar conservation, no L-BFGS dual updates | Move any ALM logic out of baseline training and into optional ablation scope. | medium |
| Symbol naming | `epsilon_soft = 1e-5` everywhere | `ε_train = 10⁻⁵` (training matched pair); `ε_inv = 10⁻¹⁰` (static) | Rename softening symbols by context. | low |
| HNN-branded names | if any (`hnn_*` variable/method names) | renamed to soft-conservation-regularizer-aligned (`energy_*`, `conservation_*`) | Rename HNN-branded implementation identifiers where they survive. | low |
| Time input | raw `t` or `tau` as autograd leaf | `u = t/T` canonical leaf, model wrapper computes `τ = 2u−1` | Align time leaf and wrapper with PHYS-02. | high |

Lines/exact paths are non-binding — verified by FUT-01 against the post-rewrite codebase. Phase 19 records the divergence structure, not exact LOC counts.

### Claude's Discretion

- Exact section-break placement of the new "Governing Mathematical Convention" anchor in `ctl_instruction.md` Step 2.5 (per resolution §10.1).
- Exact wording of the M4 replacement prose's Phase 17/18 cross-reference clause (D-11).
- Markdown formatting choice for the Plummer formula table in `pinn_architecture.md` §3.2-3.3 (math display vs inline; current spec uses display blocks — keep).
- Whether the worked synthetic-trajectory Python listing uses `torch.func.jacrev + vmap` or an explicit per-component loop (D-08); either is acceptable, planner picks the cleaner diff.
- Exact placement of the "Optional ALM ablation (P2)" appendix within `pinn_architecture.md` §4 (after the default-contract sections; planner finalizes).
- Evidence-packet section ordering within the Phase 16 `_TEMPLATE.md` 12-section schema (Phase 17/18 precedent: follow template ordering).
- Whether `evidence/B-07.md` / `evidence/B-08.md` use a Markdown table or list for source-position quotes (both findings are non-EVID-05, so §5/§7/§8/§9 carry `Not contested` markers either way).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents (Phase 19 researcher, planners, executors) MUST read these before planning or implementing.**

### Primary sources (v1.4 policy: neither authoritative; resolution doc is default verdict source per directive 2026-05-18)

- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md` —
  - §1 decision matrix (lines 116–131: D formula, softening rows, ALM rows, energy/HNN rows).
  - §3.1–3.2 (lines 137–207: raw-mass nondimensionalization proof; rejected `D=(GM_tot T²)^(1/3)` alternative).
  - §3.3 (lines 209–250: τ semantics three-layer separation; autograd leaf = `u`; chain-rule factors).
  - §6.3–6.4 (lines 687–737: COM projection head + AD derivative implementation; componentwise rule; forbidden `r.sum()`).
  - §7.1–7.3 (lines 743–823: matched Plummer pair; static invariant softening; physics residual definition).
  - §8.1–8.8 (lines 827–1039: total loss; data/IC/causal-phys/energy/angular-momentum terms; warmup schedule; ALM policy).
  - §10.1–10.10 (lines 1106–1247: exact source patch requirements for every PHYS spec edit).

- `pinn_instruction/issues/01-architecture-and-physics-foundations.md` —
  - B-02 row (line 72: D formula claim).
  - B-07 row (energy/HNN; line 89 area, plus §"HNN-Style Energy Regularizer" cross-section).
  - B-08 row (ALM scheduling and loss balancing; line 90 area).
  - B-09 row (line 76: softening mismatch).
  - M4 row (line 86: constraint-counting error).
  - "Dual-Context Epsilon Strategy" section (lines 181–211).
  - "AD Chain-Rule Factor — Missing Derivative Conversion" section (lines 107–135).
  - "Explicit AD Implementation Requirement" section (lines 139–177; `grad_outputs=torch.ones_like` anti-pattern).
  - "Cross-Issue Interactions" (lines 316–328: D + ε + COM, D + stage assignment).

### Current framework specs (the target of Phase 19 edits)

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` —
  - Step 2.5 scaling block (lines 573-596; `D = (G*T**2)^(1/3)` already present; Phase 19 adds Governing Mathematical Convention prose per resolution §10.1).
  - Step 3 static-invariant `V` (lines 663-670; additive form with `ε = 10⁻¹⁰` — converts to Plummer with `ε_inv = 10⁻¹⁰`).
  - Step 4 Mathematical Guarantees block (lines 908-940; **M4 sentence at 914-915 is Phase 19's PHYS-06 target** — Phase 18 D-06 left it verbatim).
  - Step 4 Numerical Implementation Considerations (lines 927-940; mentions `ε = 10⁻¹⁰` — update symbol to `ε_inv`).
  - `ctl_instruction.md:962` Phase 19 PHYS-02 forward-reference (Phase 17 D-09 inserted; Phase 19 retargets to cross-reference).
  - Phase 2 total-loss block (lines 1087-1113; current pseudo-ALM `+λ_p L_phys + (μ_p/2) L_phys²` formulation — full replacement per D-07).

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` —
  - Title and §1.x overview (lines 6, 86-108: HNN-style framing — full rewrite per D-09).
  - §3 loss overview (lines 285-323: ALM Initialization + ε_soft references).
  - §3.2 Physics Residual (lines 405-532: residual formula at line 416 with additive `(||r||+ε_soft)³` — change to Plummer; ALM Implementation Details — remove from default per D-05; Listings 3, 4 retained/relocated/removed per planner discretion).
  - §3.3 HNN-Style Energy Regularizer (lines 534-655: title + body — wholesale rewrite per D-09; Hamiltonian formula at line 549 with additive `1/(||r||+ε_soft)` — change to Plummer; Listing 5 `compute_initial_energy` — Plummer + symbol rename).
  - §4.1 Adaptive Loss Balancing via ALM (lines 662-666: rename/restructure per D-09).
  - §5.3 AD prose (lines 815-826: Phase 17 D-09 forward-reference to Phase 19 PHYS-02 — Phase 19 lands the canonical AD contract here per D-08).
  - Summary table (lines 866-870: HNN-style language and ALM mentions — update per D-09).

### `simulation_data/` — supporting evidence for `evidence/B-09.md` §5 (NOT grounding for Phase 19 spec)

Distinct role from Phase 18 D-10's FRAME-03 grounding usage (see D-17 in this document).

- `simulation_data/Scripts/ic_generation/ic_generation_utils.py:60-81, 223, 261, 572` — `epsilon = 0.05` is the IC minimum-separation rejection threshold, NOT force softening.
- `simulation_data/Scripts/ic_generation/generate_ics.py:40` — entry point; same `epsilon = 0.05` plumbing.
- `simulation_data/Scripts/metrics_calculation/calculate_metrics.py:193-207, 266-284` — pure unsoftened separations.
- `simulation_data/Documentation/README.md:385, 488` — `epsilon (minimum separation): 0.05`; Brutus extrapolation sequence.
- Brutus C++ integrator (`brutus_Newton-main/`) — arbitrary-precision; no softening.

### Phase 16 / 17 / 18 inheritance (read before planning)

- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` — Status table (B-02, B-07, B-08, B-09, M4 rows — all currently PENDING); lifecycle rules (D-04, D-09 through D-12); phase-exit gate. **Phase 19 amends the M4 row per D-16.**
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md` — D-06 12-section evidence-packet schema; D-08 pre-flagged EVID-05 findings (B-02, B-09); D-13 AC naming policy; D-14 shared-AC annotation rule.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` — Mandatory packet schema. Phase 19 fills 5 packets here.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/README.md` — Protocol, EVID-05 trigger conditions, VER-05 lifecycle.
- `.planning/phases/17-input-and-output-contracts/17-CONTEXT.md` — D-01 (Jacobi-state IC₁₃ — referenced by M4 replacement prose per D-11); D-03 (τ semantics — references PHYS-02 contract); D-09 (PHYS-02 forward-reference Phase 19 owns); D-12 (3-plan precedent, Phase 19 extends to 4); D-14 (`17-CODE-DIVERGENCE.md` schema precedent).
- `.planning/phases/17-input-and-output-contracts/17-CODE-DIVERGENCE.md` — Schema precedent for `19-CODE-DIVERGENCE.md`.
- `.planning/phases/18-frame-and-gauge-contracts/18-CONTEXT.md` — D-06 (M4 sentence left untouched for Phase 19); D-10 (`simulation_data/` as FRAME-03 grounding — Phase 19 differentiates per D-17); D-13 (`18-CODE-DIVERGENCE.md` schema); D-14 (`η_gauge` rotation-gauge tolerance — distinct from Phase 19's softening ε values).
- `.planning/phases/18-frame-and-gauge-contracts/18-CODE-DIVERGENCE.md` — Schema precedent.

### Project planning context

- `.planning/PROJECT.md` — v1.4 milestone goal; Key Decisions (resolution-doc policy 2026-05-18; no-live-code directive 2026-05-19; `milestone/v1.4` branch; Phase 18 complete; Phase 20.5 design+plan locked but execution pending).
- `.planning/REQUIREMENTS.md` — PHYS-01 through PHYS-06 acceptance language (lines 36-41); VER-05 lifecycle (line 57); §Traceability (source of truth, 30/30 mapped).
- `.planning/ROADMAP.md` §"Phase 19: Physics and Loss Contracts" — Goal, dependencies (Phase 18), success criteria 1–6; v1.4 verification protocol.
- `CLAUDE.md` — CRITICAL GOVERNANCE block (STOP protocol + math/engineering grounding requirement; live-code directive 2026-05-19); Source of Truth section.

### Governance / gap registers

- `.planning/phases/19-physics-and-loss-contracts/19-GAPS.md` — Phase 19 gap register. Created during plan repair with `GAP-19-01` for the ungrounded numeric `epsilon_H` default. New gaps from plan-phase or execute-phase appended per STOP protocol.
- `.planning/milestones/v1.4-GAPS.md` — Milestone-wide gap index.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- **Phase 16 evidence-packet template** (`evidence/_TEMPLATE.md`) — Phase 19 fills `evidence/B-02.md`, `evidence/B-07.md`, `evidence/B-08.md`, `evidence/B-09.md`, `evidence/M4.md` into the same `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/` directory used by Phases 16–18. EVID-05 contested findings (B-02, B-09, M4) get §5/§7/§8/§9 fully written; uncontested (B-07, B-08) carry `Not contested` markers.
- **Phase 17 / Phase 18 spec-edit pattern** — 3-plan two-wave decomposition pattern with per-plan ledger-status-transition mechanic directly reusable; Phase 19 extends to 4 plans for review safety (D-12).
- **`17-CODE-DIVERGENCE.md` and `18-CODE-DIVERGENCE.md` schemas** — `19-CODE-DIVERGENCE.md` mirrors (D-19).
- **Phase 18 D-14 `η_gauge` precedent** — naming pattern for numerical tolerances that aren't physics softening; Phase 19's `ε_train` / `ε_inv` symbols follow the same clean-separation discipline.

### Established Patterns

- **Source of truth + verification, not duplication** — `REQUIREMENTS.md` §Traceability is the VER-02 source; the issue ledger is the per-finding source. Phase 19 emits status transitions and packet content, not copies.
- **Resolution doc as default verdict source** (2026-05-18 milestone directive) — transcribe positions into spec edits unless EVID-05 surfaces concrete evidence the position fails. Three Phase 19 findings (B-02, B-09, M4) triggered EVID-05; all three resolved to `accept-resolution` after the adjudication.
- **Issue Doc adjudication-annotation convention** (D-14, NEW this phase) — one-line annotation per row; Issue Doc content is historical audit, not source-of-truth for solutions.
- **Phase artifact naming** — `19-{ARTIFACT}.md` and `19-NN-{ARTIFACT}.md` (`19-CONTEXT.md`, `19-DISCUSSION-LOG.md`, `19-01-PLAN.md`, `19-CODE-DIVERGENCE.md`, etc.).
- **Commit convention** — `docs(19): <subject>` for phase-wide edits; `docs(19-NN): <subject>` for sub-plan commits; imperative mood, lowercase, no trailing period (`.planning/codebase/CONVENTIONS.md`).
- **Grounding-source asymmetry** — `pinn/` is NOT grounding (v1.4 directive); `simulation_data/` IS grounding for sampling/data-generation specs (Phase 18 D-10) but only supporting evidence for Phase 19 B-09 (D-17). Researcher and planner must apply the correct rule per artifact.

### Integration Points

- **`gsd-plan-phase` consumes `19-CONTEXT.md`** to generate `19-RESEARCH.md` (if research stage enabled) and the four `19-NN-PLAN.md` files. Each plan must include the evidence-packet write step before any spec edit (so EVID-01's source-position and spec-evidence sections are captured before the spec changes).
- **`gsd-execute-phase` consumes the plans wave-by-wave.** Wave 1 = P01 + P02 in parallel (different files); Wave 2 = P03 (blocked on P02); Wave 3 = P04 (blocked on Waves 1–2).
- **Phase 20 (ARCH-01..05) inherits clean spec text** — SIREN frequency/init, LayerNorm, `I_norm` cleanup all build on the Phase 19-cleaned `pinn_architecture.md`. Phase 20's ARCH-01 (SIREN omega0) is unaffected by the HNN reframing.
- **Phase 20.5 (Sobol coordinate allocation) is unaffected** by Phase 19 — Phase 19 does NOT touch `sampling_method.md` (Phase 18 D-11 already isolated).
- **Phase 21 VER-04 consumes** `AC-PHYS-01..06` names (D-13) and all five evidence packets; layers disposable numeric probes on top during VER-04 execution.
- **`19-CODE-DIVERGENCE.md` is FUT-01 input** alongside `17/18/20-CODE-DIVERGENCE.md` and the eventual `pinn/STATUS.md` (added Phase 21).
- **Phase 16 ledger receives an amendment** (D-16) — M4 row reclassified; per-finding subsection note appended. No other ledger structural changes.
- **Issue Doc receives 5 forward annotations** (D-14, D-15) — one line each for B-02, B-07, B-08, B-09, M4. Original row text preserved verbatim.

</code_context>

<specifics>
## Specific Ideas

- **The `pinn_architecture.md` rewrite is the largest single edit in v1.4 so far.** It touches the title/intro, `§1.x` framing, `§3` loss overview, `§3.2` Physics Residual + ALM block, `§3.3` HNN Energy Regularizer (title + body), `§4.1` Adaptive Loss Balancing, the summary table, and the AD contract section. The 4-plan decomposition (D-12) splits this into Wave-1 P02 (formula/contract) and Wave-2 P03 (prose cleanup) to keep diffs reviewable.
- **The softening-form change (additive → Plummer) is mechanical but pervasive.** Cited line numbers are anchors; the executor `rg`s for all old additive forms and old symbols (`epsilon_soft`, bare `\varepsilon`, `(||r|| + eps)`) and updates related prose, listings, numerical notes, and anti-pattern wording. Symbol rename `epsilon_soft → epsilon_train`, introduction of `epsilon_inv`, and consistent `r_safe` notation are all in scope (D-18).
- **The M4 replacement is small text but high-value** — `ctl_instruction.md:914-915` is two sentences becoming a paragraph with cross-references to Phase 17 IO-02 and Phase 18 FRAME-01 (D-11). The arithmetic correction (`18 − 3 COM − 3 P − 3 SO(3) = 9`) belongs in `evidence/M4.md` §5/§9, not in the spec replacement prose (the spec uses the resolution doc's framing, which sidesteps counting entirely).
- **The Phase 16 ledger M4-row reclassification (D-16) is a factual ledger correction, NOT a new-schema invention.** The audit-note format mirrors the precedent set by Phase 17/18 status-transition log entries. It is the only ledger row Phase 19 modifies structurally; status-transition logs for B-02/B-07/B-08/B-09/M4 are appended normally per Phase 16 D-04.
- **The L_IC and L_L additions (D-07) are structural new content** — they don't exist in the current spec. The planner must locate where they fit naturally in `pinn_architecture.md` (likely a new subsection between §3.2 Physics Residual and §3.3 Energy Regularizer for `L_IC`, and after §3.3 for `L_L` — or restructure §3 entirely into a "Loss term catalog" subsection per resolution §8.x organization).
- **The optional ALM P2-ablation appendix (D-05)** lives at the end of `pinn_architecture.md` §4 (after the default-contract sections). Planner picks exact placement.
- **The `simulation_data` verification subsection in `evidence/B-09.md` §5 (D-17) is structured prose** — inspected files cited with line ranges, finding stated, implication derived, role explicitly named as "supporting evidence, NOT grounding." This is distinct from Phase 18 D-10's grounding usage; the distinction is recorded in the packet so future readers don't conflate them.
- **The 4-plan decomposition (D-12) lets P01 and P02 run in parallel** because they touch different files (`ctl_instruction.md` vs `pinn_architecture.md`). The total-loss replacement (D-07) is the one coordination point: both files have a total-loss block (the `ctl_instruction.md:1095` `L_total` formula and the `pinn_architecture.md` §4.1 Adaptive Loss Balancing prose). Planner coordinates P01 and P02 to land the same final equation in both files. P03 then validates the cross-references in Wave 2.

</specifics>

<deferred>
## Deferred Ideas

- **Numerical execution of `AC-PHYS-01..06`** — Phase 21 VER-04. Phase 19 reserves names + writes structural pass criteria (D-13); Phase 21 layers disposable numeric probes (AD componentwise test, COM/momentum invariance with new loss, energy-drift dry run, loss-stability dry run).
- **`AC-PHYS-NN` numeric pass criteria** — Phase 21 VER-01 per Phase 16 D-13. Phase 19 reserves names only.
- **SCOPE-05 formalization in `REQUIREMENTS.md`** — Phase 20.5's job. Phase 19 relies on Phase 18 D-10 + the user-directive distinction (D-17) directly; it does not edit `REQUIREMENTS.md` to add SCOPE-05.
- **Phase 17 / Phase 18 Issue Doc retroactive annotation** — requires separate user instruction (D-15). When user authorizes, the back-fill applies D-14's one-line format to B-03, B-04, B-06, M1, M2 (Phase 17) and B-05, M3 (Phase 18) issue-doc rows.
- **`pinn/` code rebuild** — FUT-01. Phase 19 records the divergence in `19-CODE-DIVERGENCE.md` (D-19); v1.4 does not edit `pinn/` code.
- **SI-PINN-001 / SI-CTL-001 (and any SI-* entries Phase 19 touches) retirement** — Phase 21 VER-06 retires source-issue ledger entries with back-references to Phase 19's evidence packets. Phase 19 does NOT edit the `## Source Issues` sections of the framework specs.
- **Causal-weighting alternatives** — PHYS-05's "causal or otherwise justified" wording leaves room for alternatives. Phase 19 locks causal-with-stopgrad as default; alternatives may be documented as P2 ablations only (no further work this phase).
- **L_phys hyperparameter ablations** (η_c, lookahead fraction, replay fraction beyond defaults) — Phase 21 disposable probes or post-v1.4 training-tuning work. Phase 19 spec carries defaults only.
- **`pinn/STATUS.md` archival marker file** — Phase 21 handoff per Phase 17 D-15.

None — discussion stayed within phase scope. (Scope creep redirected once during the discussion: the Phase 17/18 Issue Doc retroactive back-fill question was surfaced and explicitly deferred per D-15.)

</deferred>

---

*Phase: 19-Physics and Loss Contracts*
*Context gathered: 2026-05-22*
*Mode: gsd-discuss-phase 19 --all ultrathink — default-mode interactive discussion across 5 auto-selected gray areas*
*Inherits: Phase 16 evidence framework + ledger (with D-16 amendment); Phase 17 D-01 (Jacobi-state IC13), D-03 (τ semantics), D-09 (PHYS-02 forward-ref); Phase 18 D-06 (M4 sentence left untouched), D-10 (simulation_data grounding for FRAME-03 — differentiated by D-17 here), D-13 (CODE-DIVERGENCE schema), D-14 (η_gauge — distinct from PHYS softening symbols)*
*Establishes: D-14 (Issue Doc adjudication-annotation convention — milestone-wide pattern going forward)*
*Next: gsd-plan-phase 19 (4-plan decomposition: P01 ctl_instruction / P02 pinn_architecture formulas / P03 pinn_architecture prose / P04 evidence + ledger + divergence)*
