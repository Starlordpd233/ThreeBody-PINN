---
phase: 17
slug: input-and-output-contracts
total_gaps: 10
open_gaps: 10
resolved_gaps: 0
deferred_gaps: 0
last_updated: 2026-05-19
governance: "Governed by CLAUDE.md/AGENTS.md/GEMINI.md 'CRITICAL GOVERNANCE' block (strengthened 2026-05-19 with STOP protocol + math/engineering grounding requirement). All entries below complete the required schema, including Task context and Mathematical / engineering grounding fields."
---

# Phase 17 Gap Register

This file records every Phase 17 decision where source materials (resolution doc, issue doc, live code under SCOPE-01, or prior user / roadmap / requirements decisions) did not explicitly answer the question. Per the CRITICAL GOVERNANCE rule, when an agent hits such a decision it MUST: (1) STOP, (2) verify it understands the math/physics/engineering at stake, (3) record the gap with all required fields, (4) update the milestone-wide index, (5) surface to the user and wait for instruction.

**Required fields per entry (per governance rule):**

- Decision point
- Where in artifact
- Task context (NEW — what the agent was doing when it hit the gap)
- Classification (semantic / operational coordination / process-artifact schema / cross-phase reframing)
- Source silence (citations with file:line)
- **Mathematical / engineering grounding (NEW — demonstrates the agent understands why the gap is consequential; if absent or vague, the gap was recorded out of ignorance and is invalid)**
- Agent was tempted to
- What the user needs to decide (options A/B/C/...)
- Confidence of impact (HIGH / MEDIUM / LOW)
- Status (`OPEN` | `RESOLVED-WITH-INSTRUCTION` | `DEFERRED`)
- Resolution note (filled after user instruction)

---

## High-impact gaps (HIGH confidence-of-impact)

### GAP-17-01: Mass slot encoding (raw vs fraction)

- **Decision point**: For the IC₁₃ mass slots m₁, m₂, m₃, is the pre-tanh input the raw ordered mass `m_i` or the mass fraction `m_i / Σ m`?
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-07
- **Task context**: Auditing `17-CONTEXT.md` during the 2026-05-19 governance-rule-driven audit of D-01 through D-16. Hit this gap when reviewing D-07's "ordered, raw" assertion against the resolution doc and live code.
- **Classification**: semantic
- **Source silence**:
  - `ctl_pinn_resolution.md:540, 547` — formula `tanh((m_i − μ_{m,i}) / (σ_{m,i} + 10⁻⁸))` uses variable `m_i` without explicitly stating raw vs fractional at the input layer. Mass channels use post-canonical-ordering statistics per the parallel-research read; the doc does not pin which form `m_i` is *before* the statistics are applied.
  - `.planning/REQUIREMENTS.md` PHYS-01 (Phase 19) — locks raw-mass nondimensionalization for the *physics-side* (Newtonian dynamics, `D=(G*T²)^(1/3)` family), but does not explicitly extend the convention to the input encoding.
  - `pinn/data-processing-pipeline-full.py:1114–1116` — live code uses mass fractions (`2 * (masses / m_total) - 1`), but is v1.3-era and explicitly NOT authoritative under the milestone's `resolution-doc-as-default-verdict` policy. Live-code position is evidence of the OLD convention, not evidence of the new one.
- **Mathematical / engineering grounding**:

  The mass slot encoding determines what distribution is fed into the tanh nonlinearity of each input slot. The two candidate encodings have measurably different downstream behavior:

  **Option (a) — raw ordered masses `m_i`:** dataset support determined by IC generation. Per CLAUDE.md §5.2, standard quasi-random ICs have all three masses exactly equal to 1.0, while hierarchical ICs have variable masses normalized to total mass ≈ 3. Under raw encoding, the standard-quasi-random subset has `m_i = 1.0` constant, while hierarchical varies. The combined dataset's per-slot distribution is bimodal: a delta at 1.0 for SQR samples plus a continuous distribution for hierarchical samples.

  **Option (b) — mass fractions `m_i / Σ m`:** constrained by `m₁_frac + m₂_frac + m₃_frac = 1`. For SQR ICs (all raw masses 1.0), all three fractions equal exactly 1/3 — zero variance across that entire subset. For hierarchical ICs, fractions vary but live on a 2-simplex in R³, reducing the effective degrees of freedom from 3 (raw, unconstrained in R³₊) to 2 (constrained simplex).

  **Downstream consequences:**

  - *Input rank.* The mass section's effective rank is 3 (raw) or 2 (fractions). Under fractions, the three mass slots carry only 2 independent units of information; one slot is determined by the other two.
  - *Discriminability.* Can the network distinguish equal-mass (SQR) from unequal-mass (hierarchical) ICs from the mass slots alone? Raw: yes — `m_i = 1.0` vs varying values; the network sees the difference immediately. Fractions: only weakly — SQR fractions are exactly 1/3 for every body; hierarchical fractions vary. The network can detect SQR (low variance) but cannot use mass-magnitude information directly.
  - *Gradient flow through tanh.* `tanh((z − μ_z)/(σ_z + 10⁻⁸))` saturates as `|z − μ_z| ≫ σ_z`. The σ statistics differ by orders of magnitude between raw and fractional encoding. Under fractions, σ for SQR is essentially zero (forced offset by the 10⁻⁸ floor); under raw, σ for SQR is exactly zero. Both saturate, but in different regimes.
  - *Consistency with PHYS-01.* PHYS-01 locks raw-mass nondimensionalization for physics-side dynamics (Newton's law uses raw `m_i`). Choosing raw input encoding extends the same convention to the input; choosing fractions introduces a duality where physics-side and input-side use different mass conventions.

  **Engineering implication:** The data preprocessing pipeline (currently `pinn/data-processing-pipeline-full.py:1114–1116`, v1.3-era) will be rewritten in FUT-01 to compute the chosen encoding plus the new μ_{m,i}, σ_{m,i} statistics. The choice is not deferrable to runtime without forcing a stale-statistics regeneration loop on the dataset, because dataset-wide statistics must be computed once and frozen before training.

- **Agent was tempted to**: Pick **raw**, on PHYS-01 consistency reasoning.
- **What the user needs to decide**:
  - (a) Pre-tanh input is **raw ordered mass** `m_i` — extends PHYS-01 to the input encoding
  - (b) Pre-tanh input is **mass fraction** `m_i / Σ m` — keeps input encoding decoupled from physics-side raw convention
  - (c) Defer to a separate "input encoding vs physics nondimensionalization" pass that examines both options against the resolution doc + first-principles physics + a synthetic test
- **Confidence of impact**: **HIGH** — affects every IC vector ever computed; downstream FUT-01 code-rewrite scope depends on this; ripples into the per-slot statistics which would differ by orders of magnitude between options.
- **Status**: OPEN
- **Resolution note**: *(empty)*

### GAP-17-05: M5 reframe to metadata-only (Phase 20 scope change)

- **Decision point**: Does adopting the Jacobi-state IC₁₃ (D-01) automatically narrow Phase 20's M5 scope to "I₃ normalization map only matters for staging metadata, no longer for IC input"?
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-10 (forward reference to Phase 20 ARCH-03 / ARCH-04 with the reframe)
- **Task context**: Auditing `17-CONTEXT.md` D-10 during the 2026-05-19 governance audit. Hit this gap when reviewing whether Phase 17 is allowed to pre-empt Phase 20's M5 scope.
- **Classification**: cross-phase reframing
- **Source silence**:
  - `ctl_pinn_resolution.md §5.5–5.6` (lines 576–636) — relegates shape invariants `I₁, I₂, I₃` and direction cosines `c₁, c₂` to metadata for curriculum staging and diagnostics, with `I_3` mapped via `I_3^{in} = 6*I_3 − 1` (line 620). The doc does NOT explicitly say "this means M5's contested formula no longer matters for the IC input". That conclusion is the agent's downstream-phase reframing.
  - `16-ISSUE-LEDGER.md` M5 row — assigns M5 to Phase 20 ARCH-03 with `Sources Disagree? = YES — EVID-05 required`. Phase 16 did NOT pre-commit M5's scope to "metadata-only" or "IC-input".
  - `.planning/ROADMAP.md` Phase 20 Success Criteria 3 — "Reader can verify `I_3` maps the documented triangle-shape range to `[-1, 1]`." Currently agnostic on whether the `[-1, 1]` value is consumed as IC input or as metadata.
- **Mathematical / engineering grounding**:

  Under D-01 (Jacobi-state IC), the 13-component network input contains no `I₃` slot — orientation is encoded implicitly via the 6D Jacobi velocity scalars `(ρ̇_x, ρ̇_y, ρ̇_z, λ̇_x, λ̇_y, λ̇_z)`. Therefore the I₃ normalization map (M5's contested formula) does not affect any network input under the new contract.

  I₃ retains a role in curriculum staging metadata per resolution doc §5.5–5.6 — it informs which difficulty bucket a trajectory belongs to during stage assignment.

  **The contested M5 formulas, evaluated:**
  - Issue doc `I₃_norm = 2*I₃ − 1`. For input domain `I₃ ∈ [0, 1/3]`: maps `2*0 − 1 = −1` to `2*(1/3) − 1 = −1/3`. Image: `[−1, −1/3]` — does NOT cover the canonical `[−1, 1]` output range.
  - Resolution doc `I₃_norm = 6*I₃ − 1`. For input domain `I₃ ∈ [0, 1/3]`: maps `6*0 − 1 = −1` to `6*(1/3) − 1 = 1`. Image: `[−1, 1]` — covers the canonical range.

  Independent of the reframe question, the resolution doc's `6*I₃ − 1` is the correct affine map for `[0, 1/3] → [−1, 1]`; the issue doc's `2*I₃ − 1` misses the upper bound by a factor of 3. The M5 verdict appears mathematically determined toward the resolution doc.

  **Cross-phase implication:** if Phase 17 declares the reframe ("I₃ is now metadata-only under Jacobi IC"), Phase 20's M5 work narrows to "apply the correct affine map to staging metadata"; if Phase 17 doesn't reframe, Phase 20 must rediscover that I₃ no longer enters the IC vector and may waste effort re-adjudicating against the old IC contract. Either way, the verdict appears to be resolution-doc's formula.

- **Agent was tempted to**: Declare M5's scope narrowed to "metadata-only" under Jacobi IC, on the logical chain D-01 → I₃ not in IC → therefore M5's normalization affects only staging metadata.
- **What the user needs to decide**:
  - (a) Acknowledge the reframe explicitly: Phase 20 M5 scope is now "I₃ normalization for staging metadata only"; Phase 20 plans should reflect this
  - (b) Direct Phase 20 to re-adjudicate M5 independently — Phase 17 does NOT preempt Phase 20's scope, leaves M5 contested in the ledger, Phase 20 decides whether Jacobi-IC adoption affects M5 in its own EVID-05 step
  - (c) Defer the reframe decision until Phase 20 actually opens
- **Confidence of impact**: **HIGH** — directly changes Phase 20's work scope, the M5 verdict path, and possibly the `SI-SSR-001 ↔ M5` retirement in Phase 21 VER-06. If left implicit, Phase 20 may rediscover the same logical chain or contradict it.
- **Status**: OPEN
- **Resolution note**: *(empty)*

---

## Medium-impact gaps

### GAP-17-02: AC-IO-04 invention

- **Decision point**: Should IO-04 (obsolete-wording cleanup) have its own named acceptance check (`AC-IO-04`), or should the cleanup be enforced as a phase-exit gate without a named AC?
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-13
- **Task context**: Drafting `17-CONTEXT.md` D-13 (acceptance-check reservations) during discuss-phase write-up 2026-05-18. Hit this gap when realizing IO-04 has no finding ID, so the Phase 16 AC reservation list doesn't have a name for it.
- **Classification**: process-artifact schema
- **Source silence**:
  - `16-ISSUE-LEDGER.md` AC reservations — reserved `AC-IO-01` (B-03, M2), `AC-IO-02` (B-04, M1), `AC-IO-03` (B-06). Did NOT reserve `AC-IO-04`.
  - `.planning/REQUIREMENTS.md` IO-04 — "Any obsolete 11D, 12D, or ambiguous 13D/14D wording is removed or explicitly labeled as historical source-issue metadata." No finding ID tied to IO-04; it is a phase-wide cleanup requirement.
  - `16-CONTEXT.md` D-13 acceptance-check naming policy — "Reserve names `AC-{REQ-ID}[-{NN}]`". `AC-IO-04` would conform syntactically; Phase 16 did not pre-reserve it.
- **Mathematical / engineering grounding**:

  This is a verification-protocol design decision, not a physics/math question. Background: Phase 16 D-09 established `VERIFIED` status requires a NAMED acceptance check that passes. The transition `FIX_APPLIED → VERIFIED` is gated on the named AC. IO-04 is a phase-wide cleanup requirement with no corresponding finding ID in `16-ISSUE-LEDGER.md`, so it has no natural AC-ID slot under the current naming convention.

  **Two clean designs:**
  - (a) Extend AC-naming to cover requirement-level checks: `AC-IO-04` as Phase 17-local, no ledger row needed. Pass criterion: "no unqualified 11D/12D/ambiguous 13D mentions remain except where labeled historical".
  - (b) Cleanup verified as part of `17-VERIFICATION.md` phase-exit gate without a named AC. Cleanup still happens, but isn't bracketed by an AC-ID.

  Both preserve audit-trail soundness. (a) gives finer granularity at the cost of one extra AC name not in the Phase 16 reservation list; (b) keeps the AC list aligned with Phase 16 reservations but loses a named gate for the cleanup.

  **Engineering implication:** affects the verification protocol naming convention going forward. If we extend the convention here, Phases 18–20 may need similar requirement-level ACs for their own cleanup-style requirements.

- **Agent was tempted to**: Reserve `AC-IO-04` as a Phase 17-local check.
- **What the user needs to decide**:
  - (a) Approve `AC-IO-04` as a Phase 17-local AC (no Phase 16 ledger row; phase-exit gate)
  - (b) Skip the AC; treat IO-04 cleanup verification as part of standard `17-VERIFICATION.md` without a named AC
  - (c) Retroactively add an `AC-IO-04` row to `16-ISSUE-LEDGER.md`
- **Confidence of impact**: **MEDIUM** — affects only verification protocol naming; cleanup happens regardless.
- **Status**: OPEN
- **Resolution note**: *(empty)*

### GAP-17-03: AC-IO-01 / AC-IO-02 / AC-IO-03 pass-criteria wording

- **Decision point**: For each of `AC-IO-01`, `AC-IO-02`, `AC-IO-03` (names reserved by Phase 16 D-13), what is the *text/structural pass criterion* that gates the `VERIFIED` status transition for the underlying findings?
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-13 — the proposed criteria
- **Task context**: Drafting `17-CONTEXT.md` D-13 acceptance-check pass criteria for IO findings during discuss-phase write-up 2026-05-18.
- **Classification**: process-artifact schema
- **Source silence**:
  - `.planning/REQUIREMENTS.md` VER-01 — "numerically-defined acceptance checks ... names its pass criterion (e.g., `relative_error < 1e-10`), the data it runs on, and the command or function that executes it — not just prose descriptions." VER-01 enumerates checks for *PHYS/FRAME-side* findings (scaling, COM, AD, force-energy, loss). VER-01 does NOT define the pass-criterion format for IO-side ACs.
  - `16-CONTEXT.md` D-13 — "pass criteria, runnable command, and data fixture are defined in Phase 21 per VER-01." Implies Phase 17 reserves names, criteria are written elsewhere. But for IO findings (which Phase 21 may not numericize), there is no upstream source for the *text/structural* criteria the agent proposes.
- **Mathematical / engineering grounding**:

  IO contracts are linguistic-syntactic decisions about spec content, not numerical computations:
  - "Does the spec file contain exactly one canonical input-contract definition?"
  - "Does the input width claim in `ctl_instruction.md` match the claim in `pinn_architecture.md`?"
  - "Does the B-04 EVID-05 record exist with all four candidate analyses?"

  These cannot be expressed as `relative_error < threshold` style numerical checks (VER-01's format). They map naturally to **structural assertions** verifiable by:
  - grep-based existence/absence checks ("exactly one match for the canonical contract pattern")
  - cross-file consistency checks (text equality of two specific lines or values across files)
  - presence-of-required-element checks (the evidence packet contains the required §)

  Either prose pass criteria (declarative: "the spec must say X") or a small grep harness (procedural: `grep -c "..." file | should equal 1`) is a valid AC for IO findings. The engineering question is which form the user wants for IO-side verification — they're equivalent in soundness, but differ in mechanizability and audit clarity.

  **Engineering implication:** pass criteria gate the `FIX_APPLIED → VERIFIED` transition for B-03/B-04/B-06/M1/M2 — the entire Phase 17 in-scope finding set. Loose criteria let weak fixes pass; over-tight criteria force unnecessary re-work cycles.

- **Agent was tempted to**: Write specific text/structural pass criteria (already drafted in `17-CONTEXT.md` D-13): AC-IO-01 = "exactly one canonical input contract per spec, total width 14, no contradiction across files"; AC-IO-02 = "IC₁₃ ordering matches across files, per-slot normalization named, B-04 EVID-05 complete"; AC-IO-03 = "9D position output, COM head formula present, AD-derived v/a defined".
- **What the user needs to decide**:
  - (a) Approve agent-proposed text/structural criteria
  - (b) Defer all IO pass-criteria wording to Phase 21 VER-01 — Phase 17 cites AC-IDs only
  - (c) User writes the criteria directly; agent transcribes
- **Confidence of impact**: **MEDIUM** — gates VERIFIED transitions for all Phase 17 in-scope findings.
- **Status**: OPEN
- **Resolution note**: *(empty)*

### GAP-17-04: `17-CODE-DIVERGENCE.md` schema

- **Decision point**: What fields does `17-CODE-DIVERGENCE.md` contain per divergence entry, and how does it relate to the eventual `pinn/STATUS.md`?
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-14 (proposed 5-column schema with FUT-01 priority)
- **Task context**: Drafting `17-CONTEXT.md` D-14 (code-divergence handling) during discuss-phase write-up 2026-05-18. The mechanism was user-approved earlier; the schema is new.
- **Classification**: process-artifact schema
- **Source silence**:
  - No source document specifies the schema for a divergence-register file. Phase 16 did not define one.
  - `.planning/REQUIREMENTS.md` IO-02 success criterion 5 — "any discovered mismatch with existing `pinn/` implementation files is recorded as downstream code-alignment work" — establishes *that* divergences are recorded, but not the schema.
  - SCOPE-01 — establishes that divergences exist and a handoff record is needed; doesn't specify format.
- **Mathematical / engineering grounding**:

  The divergence record's job is to enable FUT-01 (the eventual post-v1.4 code-rewrite milestone) to consume spec-vs-code gaps efficiently. Engineering considerations:

  - **Localization:** each entry must specify both sides — current code at `file:line` (so FUT-01 can find the rewrite site) and target spec contract (so FUT-01 knows what to write).
  - **Ordering hints:** priority HIGH/MEDIUM/LOW helps FUT-01 sequence rewrites. IC composition and COM head are high-impact (every training/inference call uses them); docstring drift is low-impact (cosmetic).
  - **Estimation fields:** "estimated effort", "risk", "tests needed post-rewrite" would help FUT-01 plan, but require speculation Phase 17 can't currently ground (no FUT-01 dev velocity data exists yet).
  - **Format choice:** Markdown table is greppable and human-readable; YAML/JSON is machine-consumable but less readable. Per-divergence Markdown subsection (like the evidence-packet pattern) supports rich content per entry but resists tabular summaries.

  No mathematical content; the engineering question is *information density per row that best serves a future code-rewrite workflow*.

  **Failure mode if schema is suboptimal:** FUT-01 spends more time re-organizing the divergence list than reading it. Not catastrophic, but wasteful.

- **Agent was tempted to**: Use 5-column Markdown table — Surface / Live code (file:line) / Spec target (Phase 17 decision) / FUT-01 item / FUT-01 priority (HIGH/MEDIUM/LOW).
- **What the user needs to decide**:
  - (a) Approve agent-proposed 5-column schema
  - (b) Lighter schema — drop priority column; FUT-01 picks its own ordering
  - (c) Heavier schema — add fields for "estimated effort", "risk", "tests needed post-rewrite", "blocked by"
  - (d) Different format — YAML, JSON, or per-divergence Markdown subsection
- **Confidence of impact**: **MEDIUM** — schema affects FUT-01 ergonomics, not v1.4 correctness; locked here once and reused across Phases 18/19/20 divergence files.
- **Status**: OPEN
- **Resolution note**: *(empty)*

---

## Low-impact / operational gaps (promoted per user request 2026-05-19)

### GAP-17-06: Canonical-home topical split — specific topic→file assignment

- **Decision point**: User approved a topical split between `ctl_instruction.md` and `pinn_architecture.md`. The agent then assigned: IC₁₃ composition + per-slot normalization → `ctl_instruction.md` primary; network input width + τ semantics + 9D output + COM head → `pinn_architecture.md` primary. Is this the right assignment?
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-04 and D-05
- **Task context**: Drafting `17-CONTEXT.md` D-04/D-05 (canonical-home decisions) during discuss-phase write-up 2026-05-18 after the user approved the abstract "topical split" approach.
- **Classification**: operational coordination
- **Source silence**:
  - No source document specifies which spec file owns which content. The two current spec files happen to both define overlapping (and contradictory) IO content (per the discuss-phase parallel-research audit) — the natural topical split must be reasoned from the files' historical roles, not transcribed.
- **Mathematical / engineering grounding**:

  Information-architecture decision; no math content. Engineering considerations:

  - **Edit locality:** which file is modified for a given contract change? Concentrating IO contract in one file localizes future edits.
  - **Drift risk:** cross-file definitions can drift if one is edited and the other isn't. The current contradictions (12D vs 14D, 11 vs 13, positions+velocities vs positions-only) are the failure mode of unmanaged cross-file ownership.
  - **Ergonomics:** where does a reader look for the contract? Conventional separation in this repo: `ctl_instruction.md` is the data-preprocessing + curriculum-staging methodology (IC formulation has lived there since v1.0); `pinn_architecture.md` is the model architecture + AD contract (input/output dims and head architecture live there).

  The proposed split maps to these historical roles. Alternative single-file ownership of the full IO contract would concentrate the contract but break the data/model separation. Either approach is sound; trade-off is "preserve historical separation" vs "concentrate contract in one location".

- **Agent was tempted to**: Apply the split above; secondary file carries a one-line summary + back-reference.
- **What the user needs to decide**:
  - (a) Confirm the proposed assignment
  - (b) Different assignment (e.g., put everything in `pinn_architecture.md` since v1.4's IO-contract goal lives there)
  - (c) No back-references — each file is self-contained
- **Confidence of impact**: **LOW-MEDIUM** — affects spec edit locations; logically driven by current spec file roles.
- **Status**: OPEN
- **Resolution note**: *(empty)*

### GAP-17-07: "Symbolic μ, σ until Phase 18"

- **Decision point**: Does Phase 17 lock per-slot normalization statistics μ_z, σ_z numerically, or leave them as named symbols and let Phase 18 (FRAME-01 preprocessing) finalize them?
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-06 ("Phase 17 does NOT lock μ, σ numerical values — only the *form* of the normalization formula")
- **Task context**: Drafting `17-CONTEXT.md` D-06 (per-slot normalization table) during discuss-phase write-up 2026-05-18.
- **Classification**: operational coordination
- **Source silence**:
  - `ctl_pinn_resolution.md:533–572` — formula form is locked; numerical statistics are described as "dataset statistics computed after the full frame/gauge/scale pipeline". The doc does NOT compute or provide numerical values.
  - `.planning/ROADMAP.md` Phase 18 — FRAME-01 locks preprocessing order; does not explicitly say "Phase 18 also computes the IC normalization statistics".
- **Mathematical / engineering grounding**:

  μ_z, σ_z are dataset-wide statistics computed over the preprocessed Jacobi state for each slot. Their numerical values depend on:

  - which trajectories are in the training set (dataset composition);
  - the preprocessing pipeline (FRAME-01 in Phase 18 — COM recentering, momentum boost, canonical ordering, rotation gauge, scaling).

  Computing numerical μ, σ now would bond the framework spec to the v1.3-era preprocessing pipeline (since that's the only preprocessing currently implemented). When Phase 18 locks FRAME-01, the preprocessing may differ from v1.3, and the μ, σ values would shift. Symbolic placeholders in the spec (e.g., `tanh((z − μ_z) / (σ_z + 10⁻⁸))` without numerical μ_z, σ_z) preserve spec correctness across Phase 18 finalization.

  No mathematical correctness concern; this is a deferred-computation operational choice.

- **Agent was tempted to**: Leave μ, σ symbolic in `ctl_instruction.md`, with a forward reference to Phase 18 (or FUT-01) for the actual numbers.
- **What the user needs to decide**:
  - (a) Symbolic in Phase 17; concrete values populated downstream (Phase 18, or FUT-01 when the data pipeline is rebuilt)
  - (b) Concrete in Phase 17 — run a disposable probe to compute μ, σ over the existing dataset and lock them now (risks bonding the spec to v1.3-era preprocessing)
  - (c) Forward-ref language softer — "to be specified once dataset preprocessing is finalized" without naming a specific phase
- **Confidence of impact**: **LOW** — text-spec choice; doesn't change semantic content of IC₁₃.
- **Status**: OPEN
- **Resolution note**: *(empty)*

### GAP-17-08: Forward-reference wording — Phase 18 FRAME-01

- **Decision point**: Exact wording of `17-CONTEXT.md` D-08 forward reference, and of the corresponding sentence(s) inserted into `ctl_instruction.md` that say "IC₁₃ is computed from preprocessed (post-FRAME-01) trajectories".
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-08; future `ctl_instruction.md` Step 4 edit
- **Task context**: Drafting `17-CONTEXT.md` D-08 (forward references to downstream phases) during discuss-phase write-up 2026-05-18.
- **Classification**: operational coordination
- **Source silence**:
  - The coordination point ("IC₁₃ depends on preprocessing being applied first") is grounded by `ctl_pinn_resolution.md` §5.4. The specific *phrasing* of "Phase 18 FRAME-01" inside the framework spec is agent invention.
  - Framework spec docs (`ctl_instruction.md`, `pinn_architecture.md`) do NOT currently reference GSD phase numbers. Inserting "Phase 18 FRAME-01" inline couples the spec to the GSD planning structure.
- **Mathematical / engineering grounding**:

  Spec-coupling decision; no math content. Engineering considerations:

  - **Spec durability:** framework specs predate GSD planning. Coupling spec text to GSD phase IDs means the spec needs editing whenever phase numbering changes (e.g., if Phase 18 is split into 18a/18b, or if v1.5 renumbers).
  - **Reader navigation:** "Phase 18 (FRAME-01)" tells a downstream reader exactly which planning artifact authorizes the preprocessing order. Neutral phrasing ("the preprocessing order defined in the data-quality and frame-gauge spec sections") is more portable but less precise about decision authority.

  Trade-off is precision vs durability.

- **Agent was tempted to**: Use "Phase 18 (FRAME-01)" inline in both the planning artifact AND the framework spec edit.
- **What the user needs to decide**:
  - (a) Use "Phase 18 (FRAME-01)" inline everywhere (couples spec to GSD)
  - (b) Inline in planning artifacts only; framework spec text uses neutral phrasing without naming GSD phases
  - (c) No forward reference in the framework spec — just state "preprocessed trajectories" and leave the order to the reader
- **Confidence of impact**: **LOW** — wording choice only; doesn't change the contract.
- **Status**: OPEN
- **Resolution note**: *(empty)*

### GAP-17-09: Forward-reference wording — Phase 19 PHYS-02

- **Decision point**: Same as GAP-17-08 but for the τ / autograd-leaf / chain-rule contract → Phase 19 PHYS-02 forward reference. Where and how is it named?
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-09; future `pinn_architecture.md` §5.2 edit
- **Task context**: Drafting `17-CONTEXT.md` D-09 during discuss-phase write-up 2026-05-18.
- **Classification**: operational coordination
- **Source silence**:
  - `ctl_pinn_resolution.md:240–248` — chain-rule factors stated; resolution doc does not name "PHYS-02" or "Phase 19".
  - Same spec-coupling concern as GAP-17-08.
- **Mathematical / engineering grounding**: Same as GAP-17-08 (spec-coupling decision; precision vs durability trade-off). No math content beyond the GAP-17-08 framing.
- **Agent was tempted to**: Inline "Phase 19 (PHYS-02)" reference in `pinn_architecture.md` §5.2.
- **What the user needs to decide**: Same A/B/C options as GAP-17-08.
- **Confidence of impact**: **LOW**
- **Status**: OPEN
- **Resolution note**: *(empty)*

### GAP-17-10: Forward-reference wording — Phase 21 VER-04

- **Decision point**: Does Phase 17 mention VER-04 in the framework spec, or only in planning artifacts?
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-11
- **Task context**: Drafting `17-CONTEXT.md` D-11 during discuss-phase write-up 2026-05-18.
- **Classification**: operational coordination
- **Source silence**:
  - VER-04 in `.planning/REQUIREMENTS.md` is a planning artifact; framework spec docs do not currently reference VER-* numbering.
- **Mathematical / engineering grounding**: Same spec-coupling trade-off as GAP-17-08/09. The proposed default (planning artifacts name VER-04; framework specs do not) keeps framework specs decoupled from GSD's verification-protocol numbering.
- **Agent was tempted to**: Mention VER-04 only in planning artifacts (17-CONTEXT.md, 17-NN-PLAN.md), NOT in the framework spec edits.
- **What the user needs to decide**:
  - (a) Confirm the proposed split (planning artifacts name VER-04; framework specs do not)
  - (b) Mention in framework specs too
  - (c) Different split
- **Confidence of impact**: **LOW**
- **Status**: OPEN
- **Resolution note**: *(empty)*

---

## Operational choices NOT promoted to gaps (recorded here for audit)

The following are mechanical / presentation-only choices the agent is authorized to make without surfacing per the CRITICAL GOVERNANCE rule. They are recorded here for completeness:

| Choice | Decision the agent will make | Where in artifact |
|--------|------------------------------|-------------------|
| Section-break placement of IC₁₃ definition inside `ctl_instruction.md` Step 4 | Preserve existing section flow; IC₁₃ as natural sub-step | `17-CONTEXT.md` Claude's Discretion |
| Table vs enumerated list for per-slot normalization formula | Markdown table (matches `17-CONTEXT.md` D-06 style) | Future `ctl_instruction.md` edit |
| Evidence-packet subsection ordering for non-EVID-05 findings (B-03, B-06, M1, M2) | Per Phase 16 D-06 template; section 5/7/8/9 marked "Not contested" | `evidence/B-03.md` etc. |
| COM-projection-head placement in `pinn_architecture.md` §5.3 | Immediately after existing "Output Frame" subsection (lines 777–779) | Future `pinn_architecture.md` edit |

If any of these is actually a more substantial decision than I've classified it, promote it to a gap entry.

---

*Audit performed: 2026-05-19. Audit basis: `17-CONTEXT.md` decisions D-01 through D-16 classified against the CRITICAL GOVERNANCE rule.*
*Schema strengthened: 2026-05-19 — added `Task context` and `Mathematical / engineering grounding` fields per user directive that gap entries must demonstrate the agent understands the math/physics/engineering at stake before claiming a gap.*
