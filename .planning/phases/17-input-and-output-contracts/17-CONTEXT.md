# Phase 17: Input and Output Contracts - Context

**Gathered:** 2026-05-18
**Status:** Ready for planning
**Mode:** `gsd-discuss-phase 17` with `superpowers:brainstorming` overlay; resolution doc adopted as default verdict source per user's milestone-level directive (2026-05-18) — *override only on EVID-05 evidence that the resolution-doc position fails physics, code, or spec verification*.

---

> ⚠️ **GOVERNANCE NOTICE** — This context document was audited 2026-05-19 under the `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` **CRITICAL GOVERNANCE** rule (strengthened 2026-05-19 with STOP protocol + math/engineering grounding requirement).
>
> **Live-code directive 2026-05-19:** Live code in `pinn/` is **NOT** a grounding source, evidence source, or source-of-truth for any v1.4 decision. The v1.3-era code is artifact, rebuilt in FUT-01 from v1.4 specs. Live-code references are permitted ONLY in forward-pointing FUT-01 hand-off documents (`17-CODE-DIVERGENCE.md`, eventual `pinn/STATUS.md`). This applies retroactively to every reference in this file.
>
> Of 16 implementation decisions (D-01 through D-16):
> - **6 are LOCKED** (user-approved + resolution-doc-grounded): D-01, D-02, D-03, D-12, D-15, D-16
> - **11 are RESOLVED-WITH-INSTRUCTION** (user instruction 2026-05-19): D-04, D-05, D-06, D-07, D-08, D-09, D-10, D-11, D-13, D-14 schema, D-14 row-level priorities
> - **0 are OPEN**
>
> **Mandate for plan-phase and execute-phase agents:** GAP-17-01 through GAP-17-11 are actionable because their linked entries now have `Status: RESOLVED-WITH-INSTRUCTION` in `17-GAPS.md`. For GAP-17-11 specifically, row-level `FUT-01 priority` values in `17-CODE-DIVERGENCE.md` are **non-binding FUT-01 hand-off hints**; FUT-01 planning may revise them after reading the accumulated Phase 17/18/19/20 divergence files and `pinn/STATUS.md`. If new gaps are discovered during plan-phase or execute-phase work, append them to `17-GAPS.md` per the STOP Protocol (see CRITICAL GOVERNANCE block in `CLAUDE.md` / `AGENTS.md` / `GEMINI.md`). The Decision Status Summary at the top of §"Implementation Decisions" below is the authoritative gate.

---

<domain>
## Phase Boundary

Phase 17 locks the **network input and output contracts** in the framework specs (`ctl_instruction.md` and `pinn_architecture.md`) so every downstream phase, and any FUT-01 code rewrite, has a single coherent target.

Phase 17 ships:

1. The canonical 14D input contract `[τ, IC₁₃]` with τ semantics fully locked.
2. The canonical 13-component IC vector composition and per-slot normalization rules.
3. The canonical 9D position output contract with a hard mass-weighted COM projection head and AD-derived velocities/accelerations.
4. Cleanup of all obsolete 11D / 12D / ambiguous 13D / 14D wording (or explicit historical-metadata labeling) across both spec files.
5. EVID-05 evidence packets for the in-scope findings (B-03, B-04, B-06, M1, M2) with verdicts, root-cause ambiguity notes, and locked conventions.
6. `17-CODE-DIVERGENCE.md` — a phase-local inventory of the gap between the new spec contracts and the v1.3-era code in `pinn/`, for FUT-01 to consume.

Phase 17 does NOT:

- Edit any file in `pinn/` (SCOPE-01 — `pinn/` is v1.3-era artifact; FUT-01 will rewrite).
- Lock frame, gauge, scaling order, or COM preprocessing (Phase 18, FRAME-*).
- Lock the autograd chain-rule contract or componentwise-derivative test (Phase 19, PHYS-02 — Phase 17 names the leaf `u`; Phase 19 wires the chain-rule).
- Lock `I_3` or `I_norm` normalization (Phase 20, ARCH-03 / ARCH-04 — these are metadata-only under the Jacobi-state IC, see D-06 below).
- Execute numerical acceptance probes (Phase 21, VER-04 — Phase 17 reserves AC-IO-01, AC-IO-02, AC-IO-03 and defines text/structural pass criteria; Phase 21 may layer disposable numeric probes on top).

</domain>

<decisions>
## Implementation Decisions

### Decision Status Summary (audit 2026-05-19)

Per CRITICAL GOVERNANCE rule (`CLAUDE.md` / `AGENTS.md` / `GEMINI.md`). The plan-phase and execute-phase agents MUST consult this table before acting on any decision below. A decision marked `⚠️ OPEN` MUST NOT be acted on until the linked gap is `RESOLVED-WITH-INSTRUCTION` in `17-GAPS.md`; as of the 2026-05-19 GAP-17-11 resolution, no Phase 17 gap remains open.

| Decision | Status | Linked gap(s) | Plan-phase / execute-phase action |
|----------|--------|---------------|-----------------------------------|
| **D-01** B-04 verdict = Option C (Jacobi-state IC₁₃) | ✅ LOCKED | — | Actionable. User-approved (Tier A1) + resolution-doc-grounded (`ctl_pinn_resolution.md:71–72, 459–465, 517–524`). |
| **D-02** IO-03 = hard COM projection head | ✅ LOCKED | — | Actionable. User-approved (Tier A2) + resolution-doc-grounded (`:687–720`). |
| **D-03** τ semantics fully locked: leaf=u, τ=2u−1 | ✅ LOCKED | — | Actionable. User-approved (Tier A3) + resolution-doc-grounded (`:209–250`). |
| **D-04** IC composition primary in `ctl_instruction.md` | ✅ RESOLVED-WITH-INSTRUCTION | GAP-17-06 | Actionable. User auto-advance instruction confirmed the proposed topical split. |
| **D-05** Network I/O width primary in `pinn_architecture.md` | ✅ RESOLVED-WITH-INSTRUCTION | GAP-17-06 | Actionable. User auto-advance instruction confirmed the proposed topical split. |
| **D-06** Per-slot tanh normalization form + symbolic μ/σ | ✅ RESOLVED-WITH-INSTRUCTION | GAP-17-07 | Actionable. Formula form is grounded; μ/σ values remain symbolic in Phase 17 and concrete values are deferred downstream. |
| **D-07** Mass slots: ordered, raw, pre-normalization | ✅ RESOLVED-WITH-INSTRUCTION | GAP-17-01 | Actionable. User auto-advance instruction selected raw ordered masses. |
| **D-08** Forward-ref to Phase 18 FRAME-01 | ✅ RESOLVED-WITH-INSTRUCTION | GAP-17-08 | Actionable. Use "Phase 18 (FRAME-01)" inline in planning artifacts and framework spec text. |
| **D-09** Forward-ref to Phase 19 PHYS-02 | ✅ RESOLVED-WITH-INSTRUCTION | GAP-17-09 | Actionable. Use "Phase 19 (PHYS-02)" inline in planning artifacts and framework spec text. |
| **D-10** M5 reframed to metadata-only under Jacobi IC | ✅ RESOLVED-WITH-INSTRUCTION | GAP-17-05 | Actionable. Phase 20 M5 scope is metadata-only under the Jacobi-state IC contract. |
| **D-11** Forward-ref to Phase 21 VER-04 | ✅ RESOLVED-WITH-INSTRUCTION | GAP-17-10 | Actionable. Mention VER-04 only in planning artifacts, not framework spec edits. |
| **D-12** 3-plan decomposition: P01 input / P02 output / P03 cleanup | ✅ LOCKED | — | Actionable. User-approved. |
| **D-13** AC-IO-01/02/03 pass criteria + AC-IO-04 invention | ✅ RESOLVED-WITH-INSTRUCTION | GAP-17-02, GAP-17-03 | Actionable. Use proposed text/structural criteria and approve `AC-IO-04` as Phase 17-local. |
| **D-14** `17-CODE-DIVERGENCE.md` schema | ✅ RESOLVED-WITH-INSTRUCTION | GAP-17-04, GAP-17-11 | Schema is actionable. Row-level `FUT-01 priority` values are non-binding FUT-01 hand-off hints; FUT-01 may revise. |
| **D-15** `pinn/STATUS.md` deferred to v1.4 ship; no physical move | ✅ LOCKED | — | Actionable. User-approved. |
| **D-16** Phase 16 amendment 2026-05-18 acknowledgement | ✅ LOCKED | — | Actionable. User-approved (amendment itself approved earlier). |

**Summary:** 6 LOCKED (D-01, D-02, D-03, D-12, D-15, D-16) + 11 RESOLVED-WITH-INSTRUCTION (D-04, D-05, D-06, D-07, D-08, D-09, D-10, D-11, D-13, D-14 schema, D-14 row-level priorities). Plans P01/P02 and P03 cleanup may proceed; P03 may keep the current `FUT-01 priority` values in `17-CODE-DIVERGENCE.md` as non-binding hand-off hints.

The decision content below (D-01..D-16) preserves the full audit trail — the agent's tempted-to reasoning is retained alongside the LOCKED items so the user can see the difference between grounded content and gated proposals.

### Tier A — Verdicts locked to the resolution doc (per user directive, 2026-05-18)

The resolution doc (`ctl_pinn_resolution.md`) is treated as the **default candidate set of fixes** for every Phase 17 finding. EVID-05 still applies: each verdict is justified against the issue doc AND a first-principles physics check, but the working presumption is `accept-resolution`. Overrides require explicit EVID-05 evidence that the resolution-doc position fails one of those checks. (Per directive 2026-05-19, live code in `pinn/` is NOT part of the verification basis.)

- **D-01 (B-04 verdict — Jacobi-state IC₁₃):** Accept the resolution doc. Lock
  ```
  IC₁₃ = [m₁, m₂, m₃, ρ_x, λ_x, λ_y, ρ̇_x, ρ̇_y, ρ̇_z, λ̇_x, λ̇_y, λ̇_z, E]
  ```
  per `ctl_pinn_resolution.md:517–524`. Shape invariants `I₁, I₂, I₃` and direction cosines `c₁, c₂` are demoted to **metadata for curriculum staging and diagnostics only** (resolution doc §5.5–5.6). The issue doc's Option A (5 trig values for 3 angles) and Option B (shape invariants + direction cosines) are both **explicitly rejected** in the EVID-05 record — verdict on the EVID-02 enum is `accept-resolution`.

  - **Why:** Jacobi coordinates are the mathematically clean reduction for 3-body dynamics — relative motion separates from COM motion exactly, and orientation is carried implicitly by the 6D velocity scalars without requiring permutation-asymmetric angle definitions. Invariant-only IC vectors (Option B) lose information needed to reconstruct the initial state up to symmetry; trig-encoded angles (Option A) impose body-label-dependent conventions that the resolution doc argues are unnecessary once canonical ordering (Phase 18) is enforced.
  - **How to apply:** Phase 17 P01 writes `evidence/B-04.md` with the full 4-candidate framing from the 16-CONTEXT 2026-05-18 amendment (A, B, C, D = status-quo live code), the physics check above, and the verdict `accept-resolution`. Spec edit lands in `ctl_instruction.md` Step 4.

- **D-02 (IO-03 / B-06 verdict — hard COM projection head):** Accept the resolution doc. Lock the COM projection as a **hard architectural component** applied to the raw 9D position head **before** any data loss, physics residual, IC loss, conservation loss, or evaluation metric, per `ctl_pinn_resolution.md:687–720`:
  ```
  R_θ' = (1/M) Σᵢ mᵢ r̃_θ,i'        (mass-weighted COM of raw output)
  r_θ,i' = r̃_θ,i' − R_θ'             (project before every loss/metric)
  ```
  Because masses are constant metadata, AD through the projection automatically yields `Σᵢ mᵢ v_θ,i' = 0` and `Σᵢ mᵢ a_θ,i' = 0` — a free guarantee that downstream conservation regularizers and metrics can rely on.

  - **Why:** A loss-only correction would let the network learn to drift in the COM direction and rely on the loss to clean it up; that turns COM conservation into a soft constraint when the dataset is in the COM frame by construction (FRAME-01, FRAME-02). The hard layer makes COM conservation a **structural invariant** of every forward pass, which then composes correctly with FRAME-* in Phase 18 and PHYS-04 in Phase 19.
  - **How to apply:** P02 edits `pinn_architecture.md` §5.2 to add the projection head between the final linear layer and any output consumer. The network output dim is 9, the projection is purely arithmetic (no learnable parameters), and the mass vector is threaded through as inference-time metadata (forward signature change recorded for FUT-01 in `17-CODE-DIVERGENCE.md`).

- **D-03 (τ semantics — fully locked, not deferred):** Accept the resolution doc's three-layer separation per `ctl_pinn_resolution.md:209–250`:
  - Raw layer: `(t, r, v)` from Brutus output
  - Physics-scaled layer: `(u, r', v')` with `u = t/T`
  - Network layer: `(τ, IC₁₃)` with `τ = 2u − 1`
  - **Autograd leaf = `u`** (line 231). The model wrapper computes `τ = 2u − 1` internally; the leaf the optimizer sees during AD is `u`, not `τ`.
  - **Chain-rule factors are part of the contract** (lines 240–248): if differentiating w.r.t. τ directly, `v' = 2 (dr'/dτ)` and `a' = 4 (d²r'/dτ²)`; if w.r.t. u, `v' = dr'/du` and `a' = d²r'/du²`. Phase 17 names this contract; **Phase 19 PHYS-02** writes the componentwise-derivative test that exercises it.

  - **Why:** Phase 16's framing (D-03 there) suggested τ semantics might be deferred to Phase 19. The resolution doc actually locks this in its P0 decisions; deferring would leave Phase 17 with a vague "tau (TBD)" entry in the input contract, which contradicts IO-01's "one coherent network input contract" goal.
  - **How to apply:** P01 edits `pinn_architecture.md` §5.2 to define the three-layer separation, the leaf identification, and a *forward reference* to Phase 19 PHYS-02 for the componentwise chain-rule test (Phase 17 does not write the test).

### Canonical spec-home split (topical, not file-monopolistic)

- **D-04:** **IC₁₃ composition + per-slot normalization** — primary in `ctl_instruction.md` Step 4 (preprocessing/curriculum side, where the data pipeline naturally lives). `pinn_architecture.md` §5.2 carries a one-line summary plus a back-reference. Drift-prevention rule: any future edit to the IC composition must touch `ctl_instruction.md` first; the `pinn_architecture.md` summary is regenerated from it.

- **D-05:** **Network input width (14D = [τ, IC₁₃]), τ semantics, output width (9D), COM projection head, AD-derived v/a contract** — primary in `pinn_architecture.md` §5.2–5.3 (model-architecture side). `ctl_instruction.md` carries a one-line summary plus a back-reference. The current `ctl_instruction.md:879–880` claim "network outputs positions and velocities" is **wrong** under D-02 and must be replaced with the position-only + AD-derived wording (handled in P02).

### Per-slot normalization for IC₁₃

- **D-06:** Each of the 13 slots normalizes via the resolution doc's `tanh((z − μ_z) / (σ_z + 10⁻⁸))` pattern with dataset-wide statistics computed **after the full frame/gauge/scale pipeline** (resolution doc lines 533–572). Specifically:

  | Slots | Component | Formula | Statistics |
  |-------|-----------|---------|------------|
  | 1–3 | Ordered masses m_i | `tanh((m_i − μ_{m,i}) / (σ_{m,i} + 10⁻⁸))` | μ, σ per ordered mass slot computed *after* canonical ordering |
  | 4–6 | Jacobi positions (ρ_x, λ_x, λ_y) | `tanh((z − μ_z) / (σ_z + 10⁻⁸))` per slot | μ, σ per slot computed *after* full preprocessing |
  | 7–12 | Jacobi velocities (ρ̇_x, ρ̇_y, ρ̇_z, λ̇_x, λ̇_y, λ̇_z) | Same `tanh` formula as positions | Same |
  | 13 | Energy E | `tanh(E / E_scale)`, `E_scale = |median(E)| + 10⁻⁸` | Computed once over the full preprocessed dataset |

  - **Phase 17 does NOT lock μ, σ numerical values** — only the *form* of the normalization formula. The dataset statistics depend on FRAME-01 preprocessing order (Phase 18) being finalized first. Phase 17 leaves μ, σ as named symbols.

- **D-07:** **Mass slots: ordered, raw, before normalization.** RESOLVED-WITH-INSTRUCTION 2026-05-19 (option (a) per GAP-17-01). The resolution doc treats `m₁, m₂, m₃` as **ordered masses** (canonical-ordering per Phase 18 FRAME-01 puts mass-descending body 1 first), not mass fractions. PHYS-01 in Phase 19 confirms raw-mass nondimensionalization. The `tanh((m_i − μ_{m,i}) / σ_{m,i})` map produces a `[-1, 1]` slot value driven by where this trajectory's body-i mass falls in the dataset distribution — encoding *which* body this is, not its fraction of total mass. The mass-fraction encoding present in v1.3-era code is recorded in `17-CODE-DIVERGENCE.md` as a forward-pointing FUT-01 hand-off note only (per directive 2026-05-19) — it is NOT cited as evidence here.

### Forward references (Phase 17 does not over-lock)

- **D-08:** **Frame, gauge, scaling order** → Phase 18 FRAME-01/02/03/04. Phase 17's IC₁₃ assumes the input trajectory has been preprocessed (COM-recentered, momentum-zeroed, canonical-ordered, canonical-rotation-gauged, scaled) — but Phase 17 does NOT write the preprocessing-order spec. Phase 17 says "IC₁₃ is computed from preprocessed (post-FRAME-01) trajectories" and refers to Phase 18 for the order definition.
- **D-09:** **Componentwise AD chain rule + synthetic-trajectory test `r'(u) = [sin(2πu), cos(2πu), u²]`** → Phase 19 PHYS-02. Phase 17 names the leaf `u` and the chain-rule factors; PHYS-02 writes the test.
- **D-10:** **`I_3` normalization map and `I_norm` (raw vs tanh-squashed)** → Phase 20 ARCH-03 / ARCH-04. Under D-01 (Jacobi-state IC), `I_3` and `I_norm` are **metadata only**, not IC slots — so M5's contested `I3_norm = 6*I3 − 1` vs `I3_norm = 2*I3 − 1` debate now applies only to staging metadata, which simplifies Phase 20. Phase 17 records this re-scope but does not lock the metadata formula.
- **D-11:** **Numerically-defined acceptance checks** → Phase 21 VER-01 / VER-04. Phase 17 reserves AC-IO-01, AC-IO-02, AC-IO-03 with text/structural pass criteria (see D-13). Phase 21 may layer disposable numerical probes on top during VER-04.

### Plan decomposition (3 plans, Wave 1 → Wave 2 sequential)

- **D-12:** Three plans, two waves. Each plan is one VER-05 batch.

  - **Wave 1**
    - **P01 — Input contract.** Evidence packets for B-04, B-03, M1, M2. Spec edits: `ctl_instruction.md` Step 4 (rewrite IC vector definition to Jacobi-state form per D-01/D-06/D-07); `pinn_architecture.md` §5.2 (lock 14D input width per D-05, three-layer τ semantics per D-03). Reconcile the 12D-vs-14D / 11-vs-13 contradiction between the two specs.
  - **Wave 2** (sequential; P02 before P03 so cleanup audits the final state)
    - **P02 — Output contract.** Evidence packet for B-06. Spec edits: `pinn_architecture.md` §5.2–5.3 (9D position-only output + hard COM projection head per D-02 + AD-derived v/a wording); `ctl_instruction.md:879–880` (replace the wrong "positions and velocities" line with position-only + AD-derived).
    - **P03 — Cleanup + divergence inventory.** Grep-driven audit of all 11D / 12D / 13D / 14D mentions across `ctl_instruction.md` and `pinn_architecture.md`; classify each as authoritative (the new contract) / historical-labeled (preserved with `(historical, see SI-CTL-001)` annotation) / removed. Produce `17-CODE-DIVERGENCE.md` consolidating the Phase 17 spec↔live-code gaps for FUT-01.

- **D-13:** **Acceptance checks for IO findings are text/structural, not numerical** (numerical executions happen in Phase 21 VER-04 for PHYS/FRAME findings). Reserved names + pass criteria:
  - `AC-IO-01`: exactly one canonical input-contract definition in each spec; no contradiction between the two; total width is 14 in both. Covers B-03, M2.
  - `AC-IO-02`: IC₁₃ ordering and slot definitions match across both spec files; per-slot normalization formula is named (μ, σ may be symbolic); the four candidates from B-04 EVID-05 are all addressed in `evidence/B-04.md`. Covers B-04, M1.
  - `AC-IO-03`: output is 9D positions; COM projection head defined with formula in `pinn_architecture.md`; AD-derived velocities and accelerations defined; `ctl_instruction.md:879–880` no longer claims direct velocity output. Covers B-06.
  - `AC-IO-04` (Phase 17-local): no unqualified 11D / 12D / ambiguous 13D mentions remain in normative framework-spec prose before Source Issues metadata except where labeled historical; `17-CODE-DIVERGENCE.md` exists and enumerates all known P01/P02 spec↔code gaps from D-14. Covers IO-04.

### Code-divergence handling (SCOPE-01 compliance)

- **D-14:** **No edits to `pinn/*.py` in Phase 17.** All v1.3-era code in `pinn/` remains in place. Per directive 2026-05-19, Phase 17 does NOT cite live code as evidence — the `17-CODE-DIVERGENCE.md` table below is a forward-pointing FUT-01 hand-off only. The known divergences are:

  | Surface | Live code (`pinn/`) | Spec target (Phase 17) | FUT-01 item |
  |---------|----------------------|------------------------|-------------|
  | IC vector composition | `(m_frac, E_norm, L_norm, Q_norm, s_min_norm, I₁_norm, I₂_norm, I₃, θ₁_norm, θ₂_norm, I_norm)` | Jacobi state (D-01/D-06) | Full rewrite of `pinn/data-processing-pipeline-full.py` IC-formulation block (lines 1062–1146) |
  | Mass encoding | mass *fractions* (`2 m_i/m_total − 1`) | ordered raw masses, `tanh` over dataset statistics (D-07) | Replace mass-fraction logic in same block |
  | Orientation slots | `θ₁, θ₂` (angles between r and v for bodies 1, 2) | implicit via Jacobi velocities | Remove `compute_velocity_angles` helper |
  | COM projection head | absent (`pinn/basic_architecture.py:185–192` forward pass returns raw output) | hard layer applied before every loss/metric (D-02) | Add COM-subtraction step; thread mass metadata through forward signature |
  | Time input | raw `t` fed to network | model wrapper computes `τ = 2u − 1` from `u = t/T`; autograd leaf `u` (D-03) | Add wrapper layer; update training-loop time inputs and AD calls |
  | Docstring drift | `pinn/basic_architecture.py:154–159` claims Keplerian elements | Jacobi-state IC₁₃ | Docstring rewrite (small) |

  P03 writes this into `17-CODE-DIVERGENCE.md` with exact file:line citations.

### `pinn/` archival approach (deferred to v1.4 ship)

- **D-15:** Phase 17 does NOT add `pinn/STATUS.md`. The lightweight `pinn/STATUS.md` marker file is added at **v1.4 ship time** (Phase 21 handoff) and indexes the accumulated `NN-CODE-DIVERGENCE.md` files from Phases 17–20. Rationale: deferring the marker until ship time lets it accurately reflect the full v1.4 divergence picture, not just Phase 17's slice. No physical move of `pinn/` during v1.4.

### Phase 16 amendment (already applied 2026-05-18)

- **D-16:** The Phase 16 `16-CONTEXT.md` D-08 description of B-04 was corrected by amendment 2026-05-18 to reflect that the resolution doc proposes Option C (Jacobi state), not "Option B = shape invariants + direction cosines / velocity scalars c_1/c_2". The B-04 row in `16-ISSUE-LEDGER.md` per-finding subsection now carries the 4-candidate framing. Phase 17 inherits the corrected ledger.

### Claude's Discretion

- Exact section-break placement of the IC₁₃ definition inside `ctl_instruction.md` Step 4 — preserve the existing section's flow; the IC vector is the natural sub-step.
- Exact wording of forward references to Phases 18/19/20 — must be unambiguous about which downstream phase locks the deferred concept, but specific phrasing is flexible.
- Whether to use a Markdown table or an enumerated list for the per-slot normalization formula in `ctl_instruction.md` — pick whichever reads cleaner in context.
- Exact ordering of evidence-packet sections (within the 12 required from `16-CONTEXT.md` D-06 of Phase 16) for B-03, B-06, M1, M2 (non-EVID-05 findings, so sections 5/7/8/9 of the template are skipped with `Not contested` markers).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents (P01, P02, P03 planners and executors) MUST read these before planning or implementing.**

### Primary sources (per v1.4 policy: neither is authoritative; user directive 2026-05-18 makes resolution doc the default verdict source for `accept-resolution` cases)
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md` — Sections §3.3 (τ semantics, lines 209–250), §5.2–5.4 (IC₁₃ composition and normalization, lines 459–572), §5.5–5.6 (metadata/staging features, lines 576–636), §6.3 (output contract + COM head, lines 687–720), §1 decision matrix (lines 117–118).
- `pinn_instruction/issues/01-architecture-and-physics-foundations.md` — §5.3 / lines 270–289 + 422–468 (Option A trig encoding); lines 499–579 ("Recommended Option B": shape invariants + direction cosines).

### v1.3-era live code (NOT v1.4 evidence; FUT-01 hand-off reference only, per directive 2026-05-19)
- `pinn/data-processing-pipeline-full.py` — v1.3-era IC pipeline. NOT cited as evidence in v1.4 spec decisions. The following line ranges are recorded here only to seed the `17-CODE-DIVERGENCE.md` FUT-01 hand-off: lines 1036–1059 (shape invariants), 1062–1085 (velocity angles `θ₁, θ₂`), 1114–1116 (mass fractions), 1119–1142 (IC vector assembly), 1149–1184 (canonical ordering wrapper).
- `pinn/basic_architecture.py` — v1.3-era architecture. NOT cited as evidence. FUT-01 hand-off line ranges: 98–99 (input/output dims `(14, 9)`), 154–159 (drifted docstring), 185–192 (forward pass without COM head), 213–214 (raw time input).
- These line ranges are FUT-01 reference only — they document where the v1.3 code currently sits so the rewrite knows what to touch. They are **not** evidence for any v1.4 verdict.

### Current framework specs (the target of Phase 17 edits)
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — Step 4 (lines 790–809; current 11-component IC definition to be rewritten), §"Phase 2" (lines 876–880; wrong velocity-output claim to be replaced), §"Source Issues" (line 1218; SI-CTL-001 to be retired or back-referenced under VER-06 in Phase 21).
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — §5.2 (lines 812–815; current 14D = 1+13 + "5 trig values for 3 angles" claim — width is right, composition is wrong); §5.3 (lines 750–779; output side, currently correct on 9D position-only + AD; COM-head clause to add); §"Source Issues" (SI-PINN-001 to retire or back-ref under VER-06 in Phase 21).

### Phase 16 inheritance (read before P01 starts)
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md` — Decisions D-01 through D-19, plus the 2026-05-18 amendment.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` — Status table, B-04 corrected candidate set in per-finding subsection.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/_TEMPLATE.md` — Mandatory packet schema.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/README.md` — Protocol, EVID-05 trigger conditions, lifecycle rules.

### Project planning context
- `.planning/PROJECT.md` — Resolution-doc policy ("not authoritative"; v1.4 directive 2026-05-18 layered: default to it, override only on EVID-05 evidence).
- `.planning/REQUIREMENTS.md` — IO-01, IO-02, IO-03, IO-04 acceptance language; VER-05 (applied throughout Phase 17); §Traceability (source of truth).
- `.planning/ROADMAP.md` §"Phase 17: Input and Output Contracts" — Success criteria 1–5.
- `CLAUDE.md` Part 6 — Updated 2026-05-19: framework specs (`ctl_instruction.md`, `pinn_architecture.md`) are authoritative during v1.4. The v1.3-era `pinn/` code is NOT authoritative; pre-2026-05-19 pinning about input-vector logic overriding comments is obsolete. v1.4 specs supersede the entire v1.3 codebase.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable assets (across phases)
- **Phase 16 evidence packet template** (`evidence/_TEMPLATE.md`) — Phase 17 fills one per in-scope finding. Sections 5/7/8/9 (first-principles physics check, root-cause ambiguity, locked convention, source-correctness assignment) are MANDATORY for B-04 (EVID-05 contested) and OPTIONAL with `Not contested` markers for B-03, B-06, M1, M2.
- **Phase 16 evidence-directory convention** (`evidence/{id}.md`) — Phase 17 writes `evidence/B-03.md`, `evidence/B-04.md`, `evidence/B-06.md`, `evidence/M1.md`, `evidence/M2.md` into the SAME directory used by Phase 16, so the per-finding files accumulate one place across phases.
- **Phase 16 ledger update mechanic** — every spec edit commit also updates the corresponding row's status (PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED) and appends a status-transition log entry with date + commit short SHA in the per-finding subsection.

### Established patterns
- **Source of truth + verification, not duplication.** REQUIREMENTS.md §Traceability is the source for VER-02; PROJECT.md "Validated" section moves items post-phase. Phase 17's per-slot normalization spec lives in `ctl_instruction.md` only (D-04); `pinn_architecture.md` references it.
- **Phase artifact naming.** `17-{ARTIFACT}.md` and `17-NN-{ARTIFACT}.md` (e.g., `17-CONTEXT.md`, `17-01-PLAN.md`, `17-01-SUMMARY.md`, `17-VERIFICATION.md`, `17-VALIDATION.md`, `17-CODE-DIVERGENCE.md`).
- **Commit message convention** — `docs(17): <subject>` for phase-wide edits; `docs(17-01): <subject>` for sub-plan commits; `docs(17): amend evidence/B-04.md verdict` style for ledger transitions. Use imperative mood, lowercase, no trailing period (matches `.planning/codebase/CONVENTIONS.md`).

### Integration points
- **`gsd-plan-phase` consumes `17-CONTEXT.md`** to generate `17-RESEARCH.md` (if research stage on) and the three `17-NN-PLAN.md` files. Each plan must include the evidence-packet write step before any spec edit (so EVID-01's source-position and spec-evidence sections are captured before the spec changes). Per directive 2026-05-19, evidence packets do NOT cite live code — the §4 "FUT-01 Hand-off Note" carries forward-pointing references only.
- **`gsd-execute-phase` consumes the plans wave-by-wave.** Wave 1 = P01; Wave 2 = P02 then P03 sequential (per D-12).
- **Phase 18 inherits `17-CONTEXT.md` D-08** (forward reference to FRAME-01). Phase 18 must lock the preprocessing order before any data pipeline rebuild (FUT-01) can begin.
- **Phase 21 VER-04 consumes** `evidence/B-04.md`, `17-CODE-DIVERGENCE.md`, and the AC-IO-* names; layers disposable probes on top during execution.
- **`17-CODE-DIVERGENCE.md` is FUT-01 input.** When FUT-01 starts (post-v1.4 ship), it reads this file plus the analogous `18/19/20-CODE-DIVERGENCE.md` files plus `pinn/STATUS.md` (added Phase 21) and proceeds with the rewrite.

</code_context>

<specifics>
## Specific Ideas

- **The four-candidate B-04 framing belongs in `evidence/B-04.md` §2 (Source positions).** Quote Option A from `01-architecture-and-physics-foundations.md:270–289` + lines 422–468; quote Option B from same file lines 499–579; quote Option C from `ctl_pinn_resolution.md:71–72, 459–465, 517–524`; quote Option D (status quo) from `pinn/data-processing-pipeline-full.py:1062–1085, 1114–1146`. The §5 (first-principles physics check) section then argues why Jacobi-state Option C wins on (i) information completeness, (ii) clean separation of relative vs COM motion, (iii) avoidance of body-label-dependent angle conventions. The §9 (which source was correct) assignment notes: resolution doc was correct on rejecting invariant-only IC; issue doc was correct on flagging the original 11D underspecification; both were silent on why the live code's pos-v angles diverge from either proposal.
- **The ctl_instruction.md Step 4 rewrite is the largest single spec edit in Phase 17.** Replace the current 11-component definition (lines 790–809) with the 13-component Jacobi-state spec, the per-slot normalization formula table (D-06), the mass-ordering rule (D-07), and a one-line forward reference to Phase 18 FRAME-01 for the preprocessing order. The existing normalization-formula lines (715–738) need cross-checking — if any current formula matches the new Jacobi-slot pattern, reuse it; if it's specific to the old shape-invariant slots, remove or relocate to a "metadata diagnostics" sub-section.
- **The pinn_architecture.md §5.3 COM-projection-head addition** is one paragraph plus a formula block. Place it immediately after the existing "Output Frame" subsection (current lines 777–779), since it operationalizes the COM-frame guarantee that subsection currently states as an *assumption*.
- **The `ctl_instruction.md:879–880` velocity-output line** has been wrong for at least one milestone (Agent B's audit caught it). P02's edit just replaces it with the correct position-only + AD-derived wording — short, but high-value because it removes a direct contradiction with `pinn_architecture.md`.
- **For P03 cleanup**, the audit candidates Agent B already located: `ctl_instruction.md` lines 676 ("12D input vector"), 790–809 (the 11-component IC block to be replaced wholesale), 811 ("12-dimensional input vector"), 876 ("12-dimensional input vector"), 879–880 (velocity-output line). P03 runs after P01/P02 lands the new contract, so the audit confirms the cleanup is correct end-to-end.
- **The `17-CODE-DIVERGENCE.md` schema** mirrors the D-14 table above but adds a column for "FUT-01 priority" (high / medium / low) so the eventual code rewrite has a sequencing hint. Per GAP-17-11, these row-level values are **non-binding FUT-01 hand-off hints**; FUT-01 planning may revise them after reading the full Phase 17/18/19/20 divergence picture. Mass-encoding and IC composition are HIGH (they cascade through training); docstring drift is LOW (cosmetic).

</specifics>

<deferred>
## Deferred Ideas

- **Numerical acceptance probes for IO findings** — Phase 17 reserves AC-IO-01/02/03/04 with text/structural pass criteria (D-13). Phase 21 VER-04 may add disposable numeric probes (e.g., load a synthetic IC, compute the Jacobi state, verify the slot ordering and tanh normalization closes round-trip to ±1e-10). Out of Phase 17 scope.
- **`pinn/STATUS.md` archival marker file** — added at Phase 21 handoff per D-15, not during Phase 17. The accumulated `NN-CODE-DIVERGENCE.md` files from Phases 17/18/19/20 are its inputs.
- **Mass-fraction-vs-raw-mass rewrite of `pinn/data-processing-pipeline-full.py`** — FUT-01 work; Phase 17 records the divergence and the verdict (raw masses ordered with `tanh` normalization, not fractions). v1.4 does not edit code.
- **SI-CTL-001 / SI-PINN-001 retirement** — Phase 21 VER-06 retires these source-issue ledger entries with back-references to Phase 17's evidence packets. Phase 17 does NOT edit the `## Source Issues` sections of the framework specs (those edits happen in Phase 21's reconciliation step).
- **`I_3` and `I_norm` normalization-map adjudication (M5)** — Phase 20 ARCH-03 / ARCH-04, but now re-scoped per D-10: under Jacobi-state IC, these are metadata-only features; the contested formulas matter for curriculum-staging diagnostics, not network input.
- **Permutation-invariance discussion in `evidence/B-04.md` §5** — note that Jacobi coordinates impose a hierarchical body labeling that canonical ordering (Phase 18) makes deterministic. The body-label-asymmetry concern from sequentialthinking thought #9 is mentioned in the evidence packet but not resolved further in Phase 17 — Phase 18's canonical-ordering rule is the resolution.
- **Energy regularizer / HNN wording reconciliation (PHYS-04)** — Phase 19. The COM projection head locked here (D-02) automatically gives `Σ mᵢ vᵢ = 0` and `Σ mᵢ aᵢ = 0` for free; PHYS-04 in Phase 19 can rely on this when defining the energy-conservation regularizer rather than soft-enforcing momentum.

</deferred>

---

*Phase: 17 - Input and Output Contracts*
*Context gathered: 2026-05-18*
*Mode: gsd-discuss-phase 17 with superpowers:brainstorming overlay; resolution doc adopted as default verdict source per user directive (2026-05-18)*
*Inherits: Phase 16 evidence framework, ledger, EVID-05 protocol*
*Next: gsd-plan-phase 17 (or skip-research mode if research stage off)*
