---
phase: "20.5"
slug: sampling-coordinate-allocation
milestone: v1.4
total_gaps: 3
open_gaps: 0
resolved_gaps: 3
deferred_gaps: 0
last_updated: 2026-05-19
governance: "Governed by CLAUDE.md/AGENTS.md/GEMINI.md 'CRITICAL GOVERNANCE' block and .planning/REQUIREMENTS.md SCOPE-05. GAP-20-5-01/02/03 are RESOLVED-WITH-INSTRUCTION per user approval of the Phase 20.5 design on 2026-05-19."
---

# Phase 20.5 Gap Register — Sampling Coordinate Allocation

This file records Phase 20.5 decisions where source materials were silent or ambiguous. It
follows the Phase 17 gap-register precedent, including curated **Documents to review** lists
for future re-verification.

## GAP-20-5-01 — Sobol coordinate allocation convention

- **Decision point:** Which Sobol coordinate allocation convention to lock in
  `sampling_method.md` when scaling and velocity sampling are both enabled, given the spec
  double-books `u_4`.
- **Where in artifact:** `sampling_method.md` §1.1 (dimension bullet), "Global Scaling
  (Optional)", and "Velocity Sampling".
- **Task context:** Resolving the ambiguity raised in
  `docs/findings/addressing_sobol_sequence_suggestion.md`.
- **Classification:** Semantic — which coordinate maps to which physical quantity — with a
  data-alignment dimension (the spec must describe the existing dataset).
- **Source silence:** `ctl_pinn_resolution.md` is silent — its §10.1–10.10 patches target
  `ctl_instruction.md` and `pinn_architecture.md`; none target `sampling_method.md`; all
  "scaling" mentions are preprocessing/raw-mass contexts.
  `01-architecture-and-physics-foundations.md` is silent. `sampling_method.md` itself is
  internally contradictory — the source of the gap.
- **Mathematical / engineering grounding:** Under uniform rescaling `r → s·r, v → s·v`,
  kinetic energy `T → s²T`, Newtonian potential `U → s⁻¹U`, so `Q = 2T/|U| → s³Q`. Reusing
  one Sobol coordinate for both `s` and `v_1` would deterministically affine-couple them,
  collapsing an independent sampling dimension and injecting a hidden correlation beyond
  the documented `s³` virial distortion. The actual code reads `s` from Sobol column 3 and
  velocity from columns 4–6 — distinct coordinates, no coupling. Sobol sequences preserve
  low-discrepancy under coordinate projection, so the conditional dimension count does not
  degrade coverage.
- **Agent was tempted to:** lock "Option B" (fixed 7-dim) on QMC-purity grounds. Corrected
  after the user surfaced the data-alignment requirement; consulting
  `ic_generation_utils.py` showed the actual convention is "Option A".
- **What the user needed to decide:** A — convention matching the code; B — fixed 7-dim
  alternative; C — decoupled scale stream.
- **Confidence of impact:** HIGH — the wrong choice creates a framework-data mismatch
  between the v1.4 spec and the existing standard quasi-random dataset.
- **Documents to review** (Option C — grouped by purpose):
  - **Design and execution contract:**
    - `.planning/phases/20-5-sampling-coordinate-allocation/20-5-RESEARCH.md` §3 — locked Option A convention.
    - `.planning/phases/20-5-sampling-coordinate-allocation/20-5-PLAN.md` Task 5 — spec edits.
    - `.planning/phases/20-5-sampling-coordinate-allocation/20-5-RESEARCH.md` — mathematical grounding and decision analysis.
  - **Data-generation grounding:**
    - `simulation_data/Scripts/ic_generation/ic_generation_utils.py` — Sobol dimension and allocation order.
    - `simulation_data/Scripts/ic_generation/generate_ics.py` — standard config enabling scaling and velocity sampling.
  - **Governance:**
    - `.planning/REQUIREMENTS.md` SCOPE-05 — permits `simulation_data/Scripts/ic_generation/` as data-generation grounding.
- **Status:** `RESOLVED-WITH-INSTRUCTION`
- **Resolution note:** User instruction 2026-05-19 — lock Option A, matching
  `simulation_data/Scripts/ic_generation/ic_generation_utils.py` (verified: `u_1`–`u_3`
  position, `u_4` scale, `u_5`–`u_7` velocity for the standard config). Generalized via the
  `(δ_s, δ_v)` flags: `d = 3 + δ_s + 3δ_v`.

## GAP-20-5-02 — New acceptance-check name `AC-SAMP-01`

- **Decision point:** Whether to introduce a new acceptance-check name (`AC-SAMP-01`)
  beyond the Phase 16 reservations.
- **Where in artifact:** `20-5-DATA-ALIGNMENT.md` (the AC stub) and Phase 21's eventual
  §10 acceptance-check suite.
- **Task context:** Phase 20.5 needs an acceptance check verifying the spec↔code Sobol
  allocation alignment.
- **Classification:** Process-artifact schema (new AC name) — MUST-surface per
  `CLAUDE.md` governance.
- **Source silence:** Phase 16 reserved `AC-IO-*` names; no reservation covers a
  sampling-allocation check. Precedent: `GAP-17-02` introduced `AC-IO-04` the same way.
- **Mathematical / engineering grounding:** Verification-protocol naming decision, not a
  physics/math question. AC names form a stable namespace used by Phase 21's verification
  suite; introducing a new prefix without surfacing it risks namespace collision or an
  orphaned check that future agents cannot connect to requirements.
- **Agent was tempted to:** name it `AC-SAMP-01` and proceed.
- **What the user needed to decide:** approve the new AC name, or choose another.
- **Confidence of impact:** LOW — naming only; no behavioral consequence.
- **Documents to review** (Option A):
  - `.planning/phases/17-input-and-output-contracts/17-GAPS.md` GAP-17-02 — precedent for a phase-local AC name.
  - `.planning/REQUIREMENTS.md` SAMP-01/SAMP-02 and VER-04/VER-05 — requirement and verification context.
  - `.planning/phases/20-5-sampling-coordinate-allocation/20-5-DATA-ALIGNMENT.md` — eventual AC-SAMP-01 stub.
- **Status:** `RESOLVED-WITH-INSTRUCTION`
- **Resolution note:** User approved the Phase 20.5 design (containing `AC-SAMP-01`) on
  2026-05-19. Consistent with the `GAP-17-02` precedent for `AC-IO-04`.

## GAP-20-5-03 — Hand-off file naming: `20-5-DATA-ALIGNMENT.md`

- **Decision point:** Whether Phase 20.5's FUT-01 hand-off file departs from the
  established `NN-CODE-DIVERGENCE.md` pattern.
- **Where in artifact:** `.planning/phases/20-5-sampling-coordinate-allocation/`.
- **Task context:** Phase 17 used `17-CODE-DIVERGENCE.md` (schema locked by `GAP-17-04`)
  to document divergence between v1.4 specs and v1.3-era `pinn/` code.
- **Classification:** Operational coordination — the choice of *name and framing* for an
  established hand-off file (an alignment record, since no `pinn/` code performs Sobol
  allocation); it is not a new gap-register or divergence-file *schema*. Logged here per
  the `CLAUDE.md` requirement to record operational-coordination decisions.
- **Source silence:** The `NN-CODE-DIVERGENCE.md` pattern assumes divergence from `pinn/`
  code. No `pinn/` code performs Sobol IC-sampling allocation — the relevant code is the
  `simulation_data/` data-generation pipeline, which the v1.4 spec now *matches*. There is
  no divergence to document; there is alignment.
- **Mathematical / engineering grounding:** FUT-01 hand-off records need stable names and
  clear semantics. Calling this a divergence file would falsely signal a code/spec conflict;
  calling it a data-alignment file tells future agents that the spec is intended to match the
  documented generator behavior while still carrying provenance caveats.
- **Agent was tempted to:** name the file `20-5-DATA-ALIGNMENT.md` and frame it as an
  alignment record rather than a divergence record.
- **What the user needed to decide:** approve the renamed/repurposed hand-off file, or
  require the `NN-CODE-DIVERGENCE.md` pattern.
- **Confidence of impact:** LOW — documentation naming only.
- **Documents to review** (Option A):
  - `.planning/phases/17-input-and-output-contracts/17-GAPS.md` GAP-17-04 — precedent for hand-off file schema decisions.
  - `.planning/PROJECT.md` Key Decision "Live code in `pinn/` is NOT a grounding source during v1.4" — FUT-01 hand-off carveout.
  - `.planning/phases/20-5-sampling-coordinate-allocation/20-5-RESEARCH.md` §5.6 — data-alignment hand-off purpose.
- **Status:** `RESOLVED-WITH-INSTRUCTION`
- **Resolution note:** User approved the Phase 20.5 design (containing
  `20-5-DATA-ALIGNMENT.md`) on 2026-05-19. The file documents spec↔`simulation_data`
  alignment and carries the `AC-SAMP-01` stub.
