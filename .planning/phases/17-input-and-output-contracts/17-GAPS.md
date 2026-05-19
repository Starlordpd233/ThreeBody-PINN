---
phase: 17
slug: input-and-output-contracts
total_gaps: 10
open_gaps: 0
resolved_gaps: 10
deferred_gaps: 0
last_updated: 2026-05-19
governance: "Governed by CLAUDE.md/AGENTS.md/GEMINI.md 'CRITICAL GOVERNANCE' block (strengthened 2026-05-19 with STOP protocol + math/engineering grounding requirement + no-live-code directive). All 10 Phase 17 gaps are RESOLVED-WITH-INSTRUCTION per user auto-advance authorization 2026-05-19."
---

# Phase 17 Gap Register

This file records every Phase 17 decision where source materials (resolution doc, issue doc, prior user / roadmap / requirements decisions, framework specs revised in v1.4, or first-principles physics) did not explicitly answer the question. Per the CRITICAL GOVERNANCE rule, when an agent hits such a decision it MUST: (1) STOP, (2) verify it understands the math/physics/engineering at stake, (3) record the gap with all required fields, (4) update the milestone-wide index, (5) surface to the user and wait for instruction.

**Live-code directive (2026-05-19):** Live code in `pinn/` is **NOT** a grounding source, evidence source, or source-of-truth for any v1.4 decision. The "Documents to review" sections below do NOT include `pinn/` files. Live-code references are permitted only in forward-pointing FUT-01 hand-off documents (`17-CODE-DIVERGENCE.md`, eventual `pinn/STATUS.md`).

**Resolution batch:** On 2026-05-19, after the gaps were surfaced, the user instructed: *"auto advance now yourself without having to ask for my user input."* This register treats that as authorization to apply each entry's agent-recommended / "Agent was tempted to" option and continue Phase 17 planning without further gap prompts. Each entry's `Status` is therefore `RESOLVED-WITH-INSTRUCTION` and `Resolution note` records the applied option.

**Required fields per entry (per governance rule):**

- Decision point
- Where in artifact
- Task context — what the agent was doing when it hit the gap
- Classification (semantic / operational coordination / process-artifact schema / cross-phase reframing)
- Source silence (citations with file:line)
- **Mathematical / engineering grounding** — demonstrates the agent understands why the gap is consequential; if absent or vague, the gap was recorded out of ignorance and is invalid
- Agent was tempted to
- What the user needs to decide (options A/B/C/...)
- Confidence of impact (HIGH / MEDIUM / LOW)
- **Documents to review** (NEW 2026-05-19) — curated reading list. Option C (grouped by purpose) for HIGH/MEDIUM-impact gaps; Option A (simple list) for LOW-impact ones. Live code in `pinn/` is NEVER listed here per the no-live-code directive.
- Status (`OPEN` | `RESOLVED-WITH-INSTRUCTION` | `DEFERRED`)
- Resolution note (filled after user instruction)

---

## High-impact gaps (HIGH confidence-of-impact)

### GAP-17-01: Mass slot encoding (raw vs fraction)

- **Decision point**: For the IC₁₃ mass slots m₁, m₂, m₃, is the pre-tanh input the raw ordered mass `m_i` or the mass fraction `m_i / Σ m`?
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-07
- **Task context**: Auditing `17-CONTEXT.md` during the 2026-05-19 governance-rule-driven audit of D-01 through D-16. Hit this gap when reviewing D-07's "ordered, raw" assertion against the resolution doc.
- **Classification**: semantic
- **Source silence**:
  - `ctl_pinn_resolution.md:540, 547` — formula `tanh((m_i − μ_{m,i}) / (σ_{m,i} + 10⁻⁸))` uses variable `m_i` without explicitly stating raw vs fractional at the input layer. Mass channels use post-canonical-ordering statistics; the doc does not pin which form `m_i` is *before* the statistics are applied.
  - `.planning/REQUIREMENTS.md` PHYS-01 (Phase 19) — locks raw-mass nondimensionalization for the *physics-side* (Newtonian dynamics, `D=(G*T²)^(1/3)` family), but does not explicitly extend the convention to the input encoding.
- **Mathematical / engineering grounding**:

  The mass slot encoding determines what distribution is fed into the tanh nonlinearity of each input slot. The two candidate encodings have measurably different downstream behavior:

  **Option (a) — raw ordered masses `m_i`:** dataset support determined by IC generation. Per CLAUDE.md §5.2, standard quasi-random ICs have all three masses exactly equal to 1.0, while hierarchical ICs have variable masses normalized to total mass ≈ 3. Under raw encoding, the standard-quasi-random subset has `m_i = 1.0` constant, while hierarchical varies. The combined dataset's per-slot distribution is bimodal: a delta at 1.0 for SQR samples plus a continuous distribution for hierarchical samples.

  **Option (b) — mass fractions `m_i / Σ m`:** constrained by `m₁_frac + m₂_frac + m₃_frac = 1`. For SQR ICs (all raw masses 1.0), all three fractions equal exactly 1/3 — zero variance across that entire subset. For hierarchical ICs, fractions vary but live on a 2-simplex in R³, reducing the effective degrees of freedom from 3 (raw, unconstrained in R³₊) to 2 (constrained simplex).

  **Downstream consequences:**

  - *Input rank.* The mass section's effective rank is 3 (raw) or 2 (fractions). Under fractions, the three mass slots carry only 2 independent units of information; one slot is determined by the other two.
  - *Discriminability.* Can the network distinguish equal-mass (SQR) from unequal-mass (hierarchical) ICs from the mass slots alone? Raw: yes — `m_i = 1.0` vs varying values; the network sees the difference immediately. Fractions: only weakly — SQR fractions are exactly 1/3 for every body; hierarchical fractions vary. The network can detect SQR (low variance) but cannot use mass-magnitude information directly.
  - *Gradient flow through tanh.* `tanh((z − μ_z)/(σ_z + 10⁻⁸))` saturates as `|z − μ_z| ≫ σ_z`. The σ statistics differ by orders of magnitude between raw and fractional encoding. Under fractions, σ for SQR is essentially zero (forced offset by the 10⁻⁸ floor); under raw, σ for SQR is exactly zero. Both saturate, but in different regimes.
  - *Consistency with PHYS-01.* PHYS-01 locks raw-mass nondimensionalization for physics-side dynamics (Newton's law uses raw `m_i`). Choosing raw input encoding extends the same convention to the input; choosing fractions introduces a duality where physics-side and input-side use different mass conventions.

  **Engineering implication:** The data preprocessing pipeline (v1.3-era) will be rewritten in FUT-01 to compute the chosen encoding plus the new μ_{m,i}, σ_{m,i} statistics. The choice is not deferrable to runtime without forcing a stale-statistics regeneration loop on the dataset.

- **Agent was tempted to**: Pick **raw**, on PHYS-01 consistency reasoning.
- **What the user needs to decide**:
  - (a) Pre-tanh input is **raw ordered mass** `m_i` — extends PHYS-01 to the input encoding
  - (b) Pre-tanh input is **mass fraction** `m_i / Σ m` — keeps input encoding decoupled from physics-side raw convention
  - (c) Defer to a separate pass that examines both options against the resolution doc + first-principles physics + a synthetic test
- **Confidence of impact**: **HIGH** — affects every IC vector ever computed; downstream FUT-01 code-rewrite scope depends on this; ripples into the per-slot statistics which would differ by orders of magnitude between options.
- **Documents to review** (Option C — grouped by purpose):
  - **Candidate verdict position (resolution doc):**
    - `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md` §5.3–5.4 (lines 514–572) — locked IC₁₃ formula and normalization. Line 540 (mass channel statistics) and line 547 (mass tanh formula) carry the ambiguity.
  - **Candidate counter-position (issue doc, EVID-05 cross-check):**
    - `pinn_instruction/issues/01-architecture-and-physics-foundations.md` §5.3 — IC vector framing (Options A/B); neither explicitly resolves raw-vs-fraction at the input layer.
  - **Current framework spec being changed:**
    - `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` Step 4 — current 11-component IC definition (will be replaced).
  - **Physics-side convention dependency:**
    - `.planning/REQUIREMENTS.md` PHYS-01 — raw-mass nondimensionalization rule.
  - **Project-level scope and directive context:**
    - `.planning/PROJECT.md` Key Decisions — "Resolution doc is NOT authoritative in v1.4" + "Live code in `pinn/` is NOT a grounding source during v1.4 (directive 2026-05-19)".
  - **Dataset support context:**
    - `CLAUDE.md` §5.2 / `simulation_data/Documentation/README.md` — mass conventions (SQR = exactly 1.0; hierarchical = variable, normalized to total mass ≈ 3).
- **Status**: **RESOLVED-WITH-INSTRUCTION**
- **Resolution note**: User-authorized 2026-05-19. Applied option (a): pre-tanh mass slots are **raw ordered masses** `m_i`, extending PHYS-01's raw-mass convention to the input encoding. Resolved content now sits in `17-CONTEXT.md` D-07. v1.3-era mass-fraction implementation is recorded in `17-CODE-DIVERGENCE.md` as forward-pointing FUT-01 hand-off only.

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

  Independent of the reframe question, the resolution doc's `6*I₃ − 1` is the correct affine map; the issue doc's `2*I₃ − 1` misses the upper bound by a factor of 3. The M5 verdict appears mathematically determined toward the resolution doc.

  **Cross-phase implication:** if Phase 17 declares the reframe, Phase 20's M5 work narrows to "apply the correct affine map to staging metadata"; if Phase 17 doesn't reframe, Phase 20 may waste effort re-adjudicating against the old IC contract.

- **Agent was tempted to**: Declare M5's scope narrowed to "metadata-only" under Jacobi IC.
- **What the user needs to decide**:
  - (a) Acknowledge the reframe explicitly: Phase 20 M5 scope is now "I₃ normalization for staging metadata only"
  - (b) Direct Phase 20 to re-adjudicate M5 independently
  - (c) Defer the reframe decision until Phase 20 actually opens
- **Confidence of impact**: **HIGH** — directly changes Phase 20's work scope, the M5 verdict path, and possibly the `SI-SSR-001 ↔ M5` retirement in Phase 21 VER-06.
- **Documents to review** (Option C — grouped by purpose):
  - **Candidate verdict position (resolution doc):**
    - `ctl_pinn_resolution.md` §5.5–5.6 (lines 576–636) — metadata role for shape invariants; line 620 has `I3_in = 6*I3 - 1`.
  - **Candidate counter-position (issue doc):**
    - `pinn_instruction/issues/01-architecture-and-physics-foundations.md` §M5 — the contested `I3_norm = 2*I3 - 1` formula.
  - **Current framework spec (Phase 20 territory):**
    - `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — current `I_3` definition wherever the shape invariant is normalized.
  - **Phase 16 ledger and Phase 20 scope:**
    - `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` M5 row.
    - `.planning/ROADMAP.md` Phase 20 ARCH-03 success criterion.
- **Status**: **RESOLVED-WITH-INSTRUCTION**
- **Resolution note**: Auto-advance authorized 2026-05-19. Applied option (a): **M5 scope is reframed to metadata-only under the Jacobi-state IC contract**. Phase 20's ARCH-03 work narrows to applying the correct affine map (`I3_in = 6*I3 - 1` per resolution doc) to staging metadata; the formula no longer affects any network input. Phase 17's D-10 already records this reframe.

---

## Medium-impact gaps

### GAP-17-02: AC-IO-04 invention

- **Decision point**: Should IO-04 (obsolete-wording cleanup) have its own named acceptance check (`AC-IO-04`), or should the cleanup be enforced as a phase-exit gate without a named AC?
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-13
- **Task context**: Drafting `17-CONTEXT.md` D-13 (acceptance-check reservations) during discuss-phase write-up 2026-05-18.
- **Classification**: process-artifact schema
- **Source silence**:
  - `16-ISSUE-LEDGER.md` AC reservations — reserved `AC-IO-01` (B-03, M2), `AC-IO-02` (B-04, M1), `AC-IO-03` (B-06). Did NOT reserve `AC-IO-04`.
  - `.planning/REQUIREMENTS.md` IO-04 — phase-wide cleanup requirement, no finding ID.
  - `16-CONTEXT.md` D-13 — naming policy `AC-{REQ-ID}[-{NN}]` admits `AC-IO-04` syntactically; Phase 16 did not pre-reserve.
- **Mathematical / engineering grounding**:

  Verification-protocol design decision, not a physics/math question. Phase 16 D-09 established `VERIFIED` status requires a NAMED acceptance check. IO-04 is a phase-wide cleanup requirement with no corresponding finding ID, so it has no natural AC-ID slot. Two clean designs: (a) extend AC-naming to cover requirement-level checks (AC-IO-04 as Phase 17-local, no ledger row needed); (b) cleanup verified as part of `17-VERIFICATION.md` phase-exit gate without a named AC. Both preserve audit-trail soundness; (a) gives finer granularity, (b) keeps the AC list aligned with Phase 16 reservations.

- **Agent was tempted to**: Reserve `AC-IO-04` as a Phase 17-local check.
- **What the user needs to decide**:
  - (a) Approve `AC-IO-04` as a Phase 17-local AC (no Phase 16 ledger row)
  - (b) Skip the AC; treat IO-04 verification as part of standard phase-exit
  - (c) Retroactively add an `AC-IO-04` row to `16-ISSUE-LEDGER.md`
- **Confidence of impact**: **MEDIUM** — affects only verification protocol naming; cleanup happens regardless.
- **Documents to review** (Option C — grouped by purpose):
  - **AC reservation policy:**
    - `.planning/phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md` D-13 — AC-ID naming policy.
    - `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` — current AC reservation list.
  - **Requirement being verified:**
    - `.planning/REQUIREMENTS.md` IO-04 — cleanup requirement.
  - **Verification protocol context:**
    - `.planning/phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md` D-09 (`VERIFIED` status requires named AC) and D-12 (phase-exit gate).
- **Status**: **RESOLVED-WITH-INSTRUCTION**
- **Resolution note**: Auto-advance authorized 2026-05-19. Applied option (a): **`AC-IO-04` is reserved as a Phase 17-local AC** (no Phase 16 ledger row). Pass criterion: "no unqualified 11D / 12D / ambiguous 13D mentions remain except where labeled historical; `17-CODE-DIVERGENCE.md` exists and enumerates Phase 17's spec↔code gaps". Naming convention extension noted for future phases that may have similar requirement-level cleanups.

### GAP-17-03: AC-IO-01 / AC-IO-02 / AC-IO-03 pass-criteria wording

- **Decision point**: For each of `AC-IO-01`, `AC-IO-02`, `AC-IO-03` (names reserved by Phase 16 D-13), what is the *text/structural pass criterion* that gates the `VERIFIED` status transition for the underlying findings?
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-13
- **Task context**: Drafting `17-CONTEXT.md` D-13 acceptance-check pass criteria during discuss-phase write-up 2026-05-18.
- **Classification**: process-artifact schema
- **Source silence**:
  - `.planning/REQUIREMENTS.md` VER-01 — mandates numeric pass criteria for PHYS/FRAME-side checks; does NOT define the format for IO-side ACs.
  - `16-CONTEXT.md` D-13 — implies Phase 17 reserves names; criteria written elsewhere. For IO findings (likely not numericized), no upstream source for text/structural criteria.
- **Mathematical / engineering grounding**:

  IO contracts are linguistic-syntactic decisions about spec content, not numerical computations. These cannot be expressed as `relative_error < threshold` style numerical checks. They map naturally to **structural assertions** verifiable by: (i) grep-based existence/absence checks ("exactly one canonical contract per spec"); (ii) cross-file consistency checks (text equality of specific lines across files); (iii) presence-of-required-element checks (the evidence packet contains the required §). Either prose pass criteria or a small grep harness is a valid AC for IO findings — equivalent in soundness, differ in mechanizability.

  **Engineering implication:** pass criteria gate the `FIX_APPLIED → VERIFIED` transition for B-03/B-04/B-06/M1/M2.

- **Agent was tempted to**: Write specific text/structural pass criteria as drafted in `17-CONTEXT.md` D-13.
- **What the user needs to decide**:
  - (a) Approve agent-proposed text/structural criteria
  - (b) Defer all IO pass-criteria wording to Phase 21 VER-01
  - (c) User writes the criteria directly
- **Confidence of impact**: **MEDIUM** — gates VERIFIED transitions for all Phase 17 in-scope findings.
- **Documents to review** (Option C — grouped by purpose):
  - **VER-01 mandate (numeric form requirement):**
    - `.planning/REQUIREMENTS.md` VER-01.
  - **AC reservation in Phase 16:**
    - `.planning/phases/16-evidence-framework-and-issue-adjudication/16-CONTEXT.md` D-13 — pass criteria deferred to Phase 21.
  - **Findings that AC-IO-01/02/03 cover:**
    - `.planning/REQUIREMENTS.md` IO-01, IO-02, IO-03 — text of the requirements.
  - **17-CONTEXT.md proposed criteria:**
    - `.planning/phases/17-input-and-output-contracts/17-CONTEXT.md` D-13.
- **Status**: **RESOLVED-WITH-INSTRUCTION**
- **Resolution note**: Auto-advance authorized 2026-05-19. Applied option (a): **agent-proposed text/structural criteria are approved**. AC-IO-01 = "exactly one canonical input-contract definition per spec, total width 14, no contradiction across files"; AC-IO-02 = "IC₁₃ ordering matches across files, per-slot normalization named, B-04 EVID-05 record complete"; AC-IO-03 = "9D position output, COM head formula present, AD-derived v/a defined, `ctl_instruction.md:879–880` no longer claims direct velocity output". These are structural assertions; Phase 21 may add disposable numeric probes on top during VER-04 if useful.

### GAP-17-04: `17-CODE-DIVERGENCE.md` schema

- **Decision point**: What fields does `17-CODE-DIVERGENCE.md` contain per divergence entry, and how does it relate to the eventual `pinn/STATUS.md`?
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-14
- **Task context**: Drafting `17-CONTEXT.md` D-14 (code-divergence handling) during discuss-phase write-up 2026-05-18.
- **Classification**: process-artifact schema
- **Source silence**:
  - No source document specifies the schema for a divergence-register file.
  - `.planning/REQUIREMENTS.md` IO-02 success criterion 5 establishes that divergences are recorded, but not the schema.
  - SCOPE-01 (updated 2026-05-19) — establishes the divergence file is FUT-01 hand-off; doesn't specify format.
- **Mathematical / engineering grounding**:

  Process-artifact decision. The divergence record's job is to enable FUT-01 to consume spec-vs-code gaps efficiently. Considerations: (i) localization — each entry needs both sides (current code at file:line, target spec contract); (ii) ordering hints — priority HIGH/MEDIUM/LOW helps FUT-01 sequence rewrites; (iii) format — Markdown table is greppable, YAML/JSON is machine-consumable but less readable. Failure mode if schema is suboptimal: FUT-01 spends time re-organizing instead of reading. Not catastrophic.

- **Agent was tempted to**: Use 5-column Markdown table — Surface / Live code (file:line) / Spec target / FUT-01 item / FUT-01 priority (HIGH/MEDIUM/LOW).
- **What the user needs to decide**:
  - (a) Approve agent-proposed 5-column schema
  - (b) Lighter schema (drop priority column)
  - (c) Heavier schema (effort/risk/tests fields)
  - (d) Different format (YAML/JSON/per-divergence subsections)
- **Confidence of impact**: **MEDIUM** — schema affects FUT-01 ergonomics; locked here once and reused across Phases 18/19/20 divergence files.
- **Documents to review** (Option C — grouped by purpose):
  - **SCOPE-01 + 2026-05-19 directive:**
    - `.planning/REQUIREMENTS.md` SCOPE-01 (updated 2026-05-19) — establishes divergences are recorded.
    - `.planning/PROJECT.md` Key Decisions — "Live code in `pinn/` is NOT a grounding source during v1.4 (directive 2026-05-19)" with FUT-01 hand-off carve-out.
  - **FUT-01 context:**
    - `.planning/REQUIREMENTS.md` FUT-01.
  - **Proposed schema:**
    - `.planning/phases/17-input-and-output-contracts/17-CONTEXT.md` D-14.
- **Status**: **RESOLVED-WITH-INSTRUCTION**
- **Resolution note**: Auto-advance authorized 2026-05-19. Applied option (a): **5-column Markdown schema** — `Surface | Live code (file:line) | Spec target (Phase 17 decision) | FUT-01 item | FUT-01 priority (HIGH/MEDIUM/LOW)`. Schema reused in Phases 18/19/20 divergence files unless those phases surface their own GAP-NN-MM with a different requirement.

---

## Low / operational-impact gaps (promoted per user request 2026-05-19)

### GAP-17-06: Canonical-home topical split — specific topic→file assignment

- **Decision point**: User approved a topical split between `ctl_instruction.md` and `pinn_architecture.md`. Specific assignment: IC₁₃ composition + per-slot normalization → `ctl_instruction.md` primary; network input width + τ semantics + 9D output + COM head → `pinn_architecture.md` primary. Is this the right assignment?
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-04, D-05
- **Task context**: Drafting `17-CONTEXT.md` D-04/D-05 during discuss-phase write-up 2026-05-18 after the user approved the abstract topical split.
- **Classification**: operational coordination
- **Source silence**:
  - No source document specifies which spec file owns which content. The two current spec files both define overlapping (and contradictory) IO content — the natural topical split must be reasoned from the files' historical roles.
- **Mathematical / engineering grounding**:

  Information-architecture decision; no math content. Considerations: edit locality (which file is modified for a given change), drift risk (cross-file definitions can drift; current contradictions are the failure mode), ergonomics (where readers look). The proposed split maps to historical roles: `ctl_instruction.md` is data-preprocessing + curriculum-staging; `pinn_architecture.md` is model architecture + AD contract. Alternative single-file ownership concentrates the contract but breaks the data/model separation.

- **Agent was tempted to**: Apply the split above; secondary file carries a one-line summary + back-reference.
- **What the user needs to decide**:
  - (a) Confirm the proposed assignment
  - (b) Different assignment (e.g., all IO contract in `pinn_architecture.md`)
  - (c) No back-references — each file self-contained
- **Confidence of impact**: **LOW-MEDIUM** — affects spec edit locations.
- **Documents to review** (Option C — grouped by purpose):
  - **Current spec file structure:**
    - `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — section headers / TOC.
    - `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — section headers / TOC.
  - **Proposed assignment context:**
    - `.planning/phases/17-input-and-output-contracts/17-CONTEXT.md` D-04, D-05.
- **Status**: **RESOLVED-WITH-INSTRUCTION**
- **Resolution note**: Auto-advance authorized 2026-05-19. Applied option (a): **confirm proposed topical split**. IC₁₃ composition + per-slot normalization primary in `ctl_instruction.md` Step 4; network input width + τ semantics + 9D output + COM head primary in `pinn_architecture.md` §5.2–5.3. Secondary file carries one-line summary + back-reference.

### GAP-17-07: "Symbolic μ, σ until Phase 18"

- **Decision point**: Does Phase 17 lock per-slot normalization statistics μ_z, σ_z numerically, or leave them symbolic until Phase 18 (FRAME-01) finalizes preprocessing?
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-06
- **Task context**: Drafting `17-CONTEXT.md` D-06 (per-slot normalization table) during discuss-phase write-up 2026-05-18.
- **Classification**: operational coordination
- **Source silence**:
  - `ctl_pinn_resolution.md:533–572` — formula form locked; statistics described as "dataset statistics computed after the full frame/gauge/scale pipeline". The doc does not compute or provide numerical values.
  - `.planning/ROADMAP.md` Phase 18 — FRAME-01 locks preprocessing order; does not say Phase 18 also computes IC normalization statistics.
- **Mathematical / engineering grounding**:

  μ_z, σ_z are dataset-wide statistics computed over the preprocessed Jacobi state for each slot. Their values depend on: (a) which trajectories are in the training set; (b) the preprocessing pipeline (FRAME-01 in Phase 18). Computing numerical μ, σ now would bond the framework spec to the v1.3-era preprocessing pipeline; when Phase 18 locks FRAME-01, values may shift. Symbolic placeholders preserve correctness across Phase 18 finalization. No mathematical correctness concern.

- **Agent was tempted to**: Leave μ, σ symbolic; forward-ref to Phase 18 (or FUT-01) for actual numbers.
- **What the user needs to decide**:
  - (a) Symbolic in Phase 17; concrete values populated downstream
  - (b) Concrete now (run a disposable probe to compute over existing dataset)
  - (c) Softer forward-ref ("to be specified once preprocessing is finalized")
- **Confidence of impact**: **LOW** — text-spec choice; doesn't change semantic content.
- **Documents to review** (Option A):
  - `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:533–572` — symbolic statistics in formula form.
  - `.planning/ROADMAP.md` Phase 18 FRAME-01 — preprocessing order.
  - `.planning/phases/17-input-and-output-contracts/17-CONTEXT.md` D-06 — proposed handling.
- **Status**: **RESOLVED-WITH-INSTRUCTION**
- **Resolution note**: Auto-advance authorized 2026-05-19. Applied option (a): **μ, σ remain symbolic in Phase 17**; concrete values populated downstream (Phase 18 or FUT-01 when the data pipeline is rebuilt).

### GAP-17-08: Forward-reference wording — Phase 18 FRAME-01

- **Decision point**: Exact wording of `17-CONTEXT.md` D-08 forward reference, and of the sentence(s) inserted into `ctl_instruction.md` that say "IC₁₃ is computed from preprocessed trajectories".
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-08; future `ctl_instruction.md` Step 4 edit
- **Task context**: Drafting `17-CONTEXT.md` D-08 during discuss-phase write-up 2026-05-18.
- **Classification**: operational coordination
- **Source silence**:
  - Coordination point is grounded by `ctl_pinn_resolution.md` §5.4. Specific phrasing of "Phase 18 FRAME-01" inside the framework spec is agent invention.
  - Framework spec docs do NOT currently reference GSD phase numbers.
- **Mathematical / engineering grounding**:

  Spec-coupling decision; no math content. Framework specs predate GSD planning. Coupling spec text to GSD phase IDs means the spec needs editing whenever phase numbering changes. Neutral phrasing is more portable but less precise. Trade-off: precision vs durability.

- **Agent was tempted to**: Use "Phase 18 (FRAME-01)" inline in both planning artifact AND framework spec edit.
- **What the user needs to decide**:
  - (a) Inline "Phase 18 (FRAME-01)" everywhere
  - (b) Inline in planning artifacts only; spec text uses neutral phrasing
  - (c) No forward reference in spec — just state "preprocessed trajectories"
- **Confidence of impact**: **LOW** — wording choice only.
- **Documents to review** (Option A):
  - `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — current cross-section reference style.
  - `.planning/ROADMAP.md` Phase 18 FRAME-01 — coordination point.
  - `.planning/phases/17-input-and-output-contracts/17-CONTEXT.md` D-08 — proposed wording.
- **Status**: **RESOLVED-WITH-INSTRUCTION**
- **Resolution note**: Auto-advance authorized 2026-05-19. Applied option (a): use **"Phase 18 (FRAME-01)" inline** in both planning artifacts and framework spec text. Accept the spec-coupling cost; precision wins over durability here because the cross-phase dependency is structural (Phase 17's IC depends on Phase 18's preprocessing order).

### GAP-17-09: Forward-reference wording — Phase 19 PHYS-02

- **Decision point**: Same as GAP-17-08 but for the τ / autograd-leaf / chain-rule contract → Phase 19 PHYS-02.
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-09; future `pinn_architecture.md` §5.2 edit
- **Task context**: Drafting `17-CONTEXT.md` D-09 during discuss-phase write-up 2026-05-18.
- **Classification**: operational coordination
- **Source silence**:
  - `ctl_pinn_resolution.md:240–248` — chain-rule factors stated; doc does not name "PHYS-02" or "Phase 19".
  - Same spec-coupling concern as GAP-17-08.
- **Mathematical / engineering grounding**: Same as GAP-17-08 (spec-coupling decision; precision vs durability). No math content beyond the GAP-17-08 framing.
- **Agent was tempted to**: Inline "Phase 19 (PHYS-02)" in `pinn_architecture.md` §5.2.
- **What the user needs to decide**: Same A/B/C options as GAP-17-08.
- **Confidence of impact**: **LOW**.
- **Documents to review** (Option A):
  - `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — current cross-section reference style.
  - `.planning/ROADMAP.md` Phase 19 PHYS-02 — coordination point.
  - `.planning/phases/17-input-and-output-contracts/17-CONTEXT.md` D-09 — proposed wording.
- **Status**: **RESOLVED-WITH-INSTRUCTION**
- **Resolution note**: Auto-advance authorized 2026-05-19. Applied option (a): use **"Phase 19 (PHYS-02)" inline** in both planning artifacts and framework spec text. Same rationale as GAP-17-08.

### GAP-17-10: Forward-reference wording — Phase 21 VER-04

- **Decision point**: Does Phase 17 mention VER-04 in the framework spec, or only in planning artifacts?
- **Where in artifact**: `17-CONTEXT.md` §"Implementation Decisions" D-11
- **Task context**: Drafting `17-CONTEXT.md` D-11 during discuss-phase write-up 2026-05-18.
- **Classification**: operational coordination
- **Source silence**:
  - VER-04 is a planning artifact; framework spec docs do not currently reference VER-* numbering.
- **Mathematical / engineering grounding**: Same spec-coupling trade-off as GAP-17-08/09.
- **Agent was tempted to**: Mention VER-04 only in planning artifacts, NOT in framework spec edits.
- **What the user needs to decide**:
  - (a) Confirm the proposed split (planning artifacts name VER-04; framework specs do not)
  - (b) Mention in framework specs too
  - (c) Different split
- **Confidence of impact**: **LOW**.
- **Documents to review** (Option A):
  - `.planning/REQUIREMENTS.md` VER-04 — updated 2026-05-19 to remove live-code references; reflects current Phase 21 verification contract.
  - `.planning/phases/17-input-and-output-contracts/17-CONTEXT.md` D-11 — proposed wording.
- **Status**: **RESOLVED-WITH-INSTRUCTION**
- **Resolution note**: Auto-advance authorized 2026-05-19. Applied option (a): **confirm the split** — planning artifacts name VER-04; framework specs do not reference VER-* numbering. Keeps framework specs decoupled from GSD verification numbering.

---

## Operational choices NOT promoted to gaps (recorded here for audit)

The following are mechanical / presentation-only choices the agent is authorized to make without surfacing per the CRITICAL GOVERNANCE rule. They are recorded here for completeness:

| Choice | Decision the agent will make | Where in artifact |
|--------|------------------------------|-------------------|
| Section-break placement of IC₁₃ definition inside `ctl_instruction.md` Step 4 | Preserve existing section flow; IC₁₃ as natural sub-step | `17-CONTEXT.md` Claude's Discretion |
| Table vs enumerated list for per-slot normalization formula | Markdown table (matches `17-CONTEXT.md` D-06 style) | Future `ctl_instruction.md` edit |
| Evidence-packet subsection ordering for non-EVID-05 findings (B-03, B-06, M1, M2) | Per Phase 16 D-06 template; section 5/7/8/9 marked "Not contested"; section 4 (FUT-01 Hand-off Note, formerly Code Evidence) populated only if FUT-01 rewrite gap exists | `evidence/B-03.md` etc. |
| COM-projection-head placement in `pinn_architecture.md` §5.3 | Immediately after existing "Output Frame" subsection (lines 777–779) | Future `pinn_architecture.md` edit |

If any of these is actually a more substantial decision than I've classified it, promote it to a gap entry.

---

*Audit performed: 2026-05-19. Audit basis: `17-CONTEXT.md` decisions D-01 through D-16 classified against the CRITICAL GOVERNANCE rule (strengthened 2026-05-19 with STOP protocol + math/engineering grounding requirement + no-live-code directive).*
*Schema strengthened: 2026-05-19 — added `Task context`, `Mathematical / engineering grounding`, and `Documents to review` fields. Live-code citations removed from `Source silence` and `Mathematical / engineering grounding` per the 2026-05-19 no-live-code directive.*
*Resolution batch: 2026-05-19 — user auto-advance authorization applied all 10 gaps to their `Agent was tempted to` option; statuses updated to `RESOLVED-WITH-INSTRUCTION`.*
