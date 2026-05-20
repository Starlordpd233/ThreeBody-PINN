# Phase 20.5: Sobol Coordinate Allocation — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Lock the Sobol coordinate allocation convention in `sampling_method.md` so it is
explicit, non-overlapping, and matches `simulation_data/Scripts/ic_generation/ic_generation_utils.py`,
resolving the `u_4` double-booking between scaling and velocity sampling.

**Architecture:** This plan implements GSD Phase 20.5 (inserted between Phase 20 and
Phase 21 of v1.4). It is authored via `superpowers:writing-plans` per user directive
2026-05-19. Tasks 1–3 are GSD scaffolding (ROADMAP, REQUIREMENTS, gap registers); Task 4
applies the five spec edits; Task 5 runs a disposable verification probe; Tasks 6–7 create
the hand-off and findings artifacts; Task 8 propagates the new governance rule. The locked
convention is "Option A" — the conditional `(δ_s, δ_v)` allocation that the existing
standard quasi-random dataset was generated under. Full rationale:
`docs/superpowers/specs/2026-05-19-sobol-allocation-ambiguity-design.md`.

**Tech Stack:** Markdown framework specs; `.planning/` GSD artifacts; one Python
verification probe (`numpy`, `scipy.stats`).

---

## Git context

- **Branch:** `milestone/v1.4` (correct branch for v1.4 spec work — not a red-flag branch).
- **Commit cadence:** One atomic commit per task. `.planning/` and `pinn_instruction/` are
  risk-elevated paths (per `CLAUDE.md`) — each task commits its full change set at task end.
- **Staging:** `git add` with explicit file paths only — never `git add -A` or `git add .`.
- **No destructive operations** anywhere in this plan. No resets, rebases, force-pushes,
  branch deletions, or history rewrites. If any task appears to need one, STOP and surface.

## File Structure

**Created:**
- `.planning/phases/20-5-sampling-coordinate-allocation/20-5-GAPS.md` — phase-local gap
  register (GAP-20-5-01/02/03).
- `.planning/phases/20-5-sampling-coordinate-allocation/20-5-DATA-ALIGNMENT.md` — FUT-01
  hand-off documenting spec↔`simulation_data` alignment; contains the `AC-SAMP-01` stub.
- `.planning/phases/20-5-sampling-coordinate-allocation/probes/verify_sobol_allocation.py`
  — disposable verification probe (VER-01-style).
- `docs/findings/velocity_momentum_sampling_discrepancy.md` — sub-conflict #1 finding
  (out of Phase 20.5 scope; recorded for separate handling).

**Modified:**
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` — Edits 1–5.
- `.planning/ROADMAP.md` — insert Phase 20.5; bump coverage 30→32.
- `.planning/REQUIREMENTS.md` — add SAMP-01/02; amend SCOPE-02; add SCOPE-05; traceability.
- `.planning/milestones/v1.4-GAPS.md` — add Phase 20.5 section; frontmatter 11→14.
- `PROJECT.md` and/or `CLAUDE.md` — SCOPE-05 governance propagation (Task 8, via
  `gsd-docs-update`).

**Responsibility boundaries:** the spec file holds the convention; the gap register holds
the decision audit trail; the data-alignment doc holds the FUT-01 hand-off and acceptance
check; the findings file holds the deferred sub-conflict. Each is independently reviewable.

---

## Task 1: Insert Phase 20.5 into ROADMAP.md and create the phase directory

**Files:**
- Create: `.planning/phases/20-5-sampling-coordinate-allocation/` (directory)
- Create: `.planning/phases/20-5-sampling-coordinate-allocation/probes/` (directory)
- Modify: `.planning/ROADMAP.md`

- [ ] **Step 1: Create the phase directories**

Run:
```bash
mkdir -p ".planning/phases/20-5-sampling-coordinate-allocation/probes"
```

- [ ] **Step 2: Add the Phase 20.5 list item to the v1.4 phase list**

In `.planning/ROADMAP.md`, find this line (the Phase 20 list item):
```
- [ ] **Phase 20: Architecture and Normalization Cleanup** — Clean up SIREN frequency/init, LayerNorm attribution/defaults, inertia normalization, and realized dataset-support wording.
```
Insert immediately AFTER it:
```
- [ ] **Phase 20.5: Sampling Coordinate Allocation** — Lock the Sobol coordinate allocation convention in `sampling_method.md` so it is explicit, non-overlapping, and matches `simulation_data/Scripts/ic_generation/ic_generation_utils.py`. Narrow scope: Sobol allocation only.
```

- [ ] **Step 3: Bump the coverage line**

In `.planning/ROADMAP.md`, find:
```
**Coverage:** 30/30 v1.4 requirements mapped
```
Replace with:
```
**Coverage:** 32/32 v1.4 requirements mapped
```

- [ ] **Step 4: Add the Phase 20.5 details block**

In `.planning/ROADMAP.md`, find the line that begins the Phase 21 details section:
```
### Phase 21: Acceptance Checks, Validation Execution, and Handoff
```
Insert immediately BEFORE it (note the blank line after the block):
```
### Phase 20.5: Sampling Coordinate Allocation

**Goal**: `sampling_method.md` exposes one explicit, fixed, non-overlapping mapping from Sobol coordinates to physical sampling quantities; the §1.1 dimension claim, the "Sampling-Time Size Variability" section, and the "Velocity Sampling" section are mutually consistent and match `simulation_data/Scripts/ic_generation/ic_generation_utils.py`.
**Depends on**: Phase 16 (evidence framework). No content dependency on Phases 17–20; sequenced before Phase 21 so acceptance checks can cover it.
**Requirements**: SAMP-01, SAMP-02 (+ VER-05 applied throughout)
**Success Criteria** (what must be TRUE):

  1. Reader finds a "Sobol Coordinate Allocation Convention" subsection in `sampling_method.md` mapping `(u_1, …, u_7)` to physical quantities with no double-booking.
  2. Reader can verify the §1.1 dimension claim, "Sampling-Time Size Variability", and the Sobol coordinate allocation within "Velocity Sampling" are mutually consistent and agree with the locked `d = 3 + δ_s + 3δ_v` allocation. (The momentum-conservation procedure in "Velocity Sampling" remains a separate, flagged discrepancy — see `docs/findings/velocity_momentum_sampling_discrepancy.md` — and is excluded from this criterion.)
  3. The phase-local gap register records GAP-20-5-01/02/03 at `RESOLVED-WITH-INSTRUCTION`.
  4. `20-5-DATA-ALIGNMENT.md` records the alignment with `ic_generation_utils.py` and the FUT-01 hand-off, and defines `AC-SAMP-01` for Phase 21 execution.

**Plans**: Authored via `superpowers:writing-plans` per user directive 2026-05-19 — see `docs/superpowers/plans/2026-05-19-phase-20-5-sampling-coordinate-allocation.md`.

```

- [ ] **Step 5: Add the progress-table row**

In `.planning/ROADMAP.md`, find the Phase 20 progress-table row:
```
| 20. Architecture and Normalization Cleanup | v1.4 | 0/TBD | Not started | - |
```
Insert immediately AFTER it:
```
| 20.5 Sampling Coordinate Allocation | v1.4 | 0/TBD | Not started | - |
```

- [ ] **Step 6: Verify the ROADMAP edits**

Run:
```bash
grep -cF "**Phase 20.5: Sampling Coordinate Allocation**" .planning/ROADMAP.md
grep -cF "### Phase 20.5: Sampling Coordinate Allocation" .planning/ROADMAP.md
grep -cF "32/32 v1.4 requirements" .planning/ROADMAP.md
```
Expected: first = 1 (the phase list item), second = 1 (the details heading), third = 1
(the coverage line). If any is 0, that edit did not apply.

- [ ] **Step 7: Commit**

```bash
git add .planning/ROADMAP.md
git commit -m "docs(roadmap): insert Phase 20.5 Sampling Coordinate Allocation"
```
Note: the empty `probes/` directory is not tracked by git until it has a file (added in
Task 5); this is expected.

---

## Task 2: Add SAMP requirements and the SCOPE-05 data-alignment rule to REQUIREMENTS.md

**Files:**
- Modify: `.planning/REQUIREMENTS.md`

- [ ] **Step 1: Add the Sampling Coordinate Allocation requirement section**

In `.planning/REQUIREMENTS.md`, find the start of the Verification section:
```
### Verification and Handoff
```
Insert immediately BEFORE it:
```
### Sampling Coordinate Allocation

- [ ] **SAMP-01**: `sampling_method.md` documents an explicit Sobol coordinate allocation convention with no coordinate reused for two independent physical quantities. Allocation order: position → optional scale → optional velocity. Dimension formula `d = 3 + δ_s + 3δ_v`, where `δ_s = 1` iff sampling-time scaling is enabled and `δ_v = 1` iff velocity sampling is enabled.
- [ ] **SAMP-02**: The §1.1 dimension claim, the "Sampling-Time Size Variability" prose, and the "Velocity Sampling" prose/formula in `sampling_method.md` are mutually consistent and agree with the locked allocation, matching `simulation_data/Scripts/ic_generation/ic_generation_utils.py` (the implementation that generated the existing standard quasi-random dataset).

```

- [ ] **Step 2: Amend SCOPE-02**

In `.planning/REQUIREMENTS.md`, find the SCOPE-02 table row:
```
| **SCOPE-02** `sampling_method.md` revisions | **In scope, limited to FRAME-03** — hierarchical post-perturbation COM offset wording and any cross-reference needed for the unified preprocessing contract. No sampling-method content unrelated to Issue 01 is rewritten. |
```
Replace it with:
```
| **SCOPE-02** `sampling_method.md` revisions | **In scope, limited to (a) FRAME-03** — hierarchical post-perturbation COM offset wording and any cross-reference needed for the unified preprocessing contract — **AND (b) SAMP-01/SAMP-02** — the Sobol coordinate allocation convention (Phase 20.5). No sampling-method content unrelated to (a) or (b) is rewritten. Other sampling-method discrepancies surfaced during Phase 20.5 (velocity-momentum reconciliation, §2.1 enhancement framing) are flagged to `docs/findings/` for separate handling and explicitly excluded from Phase 20.5 scope. |
```

- [ ] **Step 3: Add the SCOPE-05 data-alignment rule**

In `.planning/REQUIREMENTS.md`, find the SCOPE-04 table row:
```
| **SCOPE-04** Disposable validation probes | **In scope, limited** — probes may be created, recorded, or run only to test risky framework contracts and produce evidence for VER-04. They are not production framework code and are not packaged as reusable `pinn/` validation infrastructure during v1.4. |
```
Insert immediately AFTER it:
```
| **SCOPE-05** Data-spec alignment for sampling-method edits | When v1.4 framework-spec edits describe the data-generation pipeline, they MUST match the actual behavior of `simulation_data/Scripts/ic_generation/`. The no-live-code directive (2026-05-19) targets `pinn/` only; `simulation_data/Scripts/ic_generation/` is a permitted grounding source for data-generation specs because the existing dataset is fixed and the framework must remain compatible with it. Spec divergences from data must be (i) reconciled to match data, (ii) flagged in `docs/findings/` for separate handling, or (iii) explicitly authorized by the user as a data-regeneration directive for FUT-01. |
```

- [ ] **Step 4: Add SAMP traceability rows**

In `.planning/REQUIREMENTS.md`, find the ARCH-05 traceability row:
```
| ARCH-05 | Phase 20 | Pending |
```
Insert immediately AFTER it:
```
| SAMP-01 | Phase 20.5 | Pending |
| SAMP-02 | Phase 20.5 | Pending |
```

- [ ] **Step 5: Update the Coverage block**

In `.planning/REQUIREMENTS.md`, find:
```
**Coverage:**
- v1.4 requirements: 30 total (5 EVID + 4 IO + 4 FRAME + 6 PHYS + 5 ARCH + 6 VER)
- Mapped to phases: 30
- Unmapped: 0
- SCOPE-01/02/03/04 are scope-boundary annotations (see "Scope Boundaries" table above), not numbered requirements.
```
Replace with:
```
**Coverage:**
- v1.4 requirements: 32 total (5 EVID + 4 IO + 4 FRAME + 6 PHYS + 5 ARCH + 2 SAMP + 6 VER)
- Mapped to phases: 32
- Unmapped: 0
- SCOPE-01 through SCOPE-05 are scope-boundary annotations (see "Scope Boundaries" table above), not numbered requirements.
```

- [ ] **Step 6: Verify the REQUIREMENTS edits**

Run:
```bash
grep -cE "SAMP-01|SAMP-02" .planning/REQUIREMENTS.md
grep -cF "**SCOPE-05** Data-spec alignment" .planning/REQUIREMENTS.md
grep -cF "32 total" .planning/REQUIREMENTS.md
```
Expected: first ≥ 4 (SAMP-01/02 definition lines, 2 traceability rows, and the SCOPE-02
amendment mention), second = 1 (the SCOPE-05 row), third = 1 (the coverage line).

- [ ] **Step 7: Commit**

```bash
git add .planning/REQUIREMENTS.md
git commit -m "docs(20-5): add SAMP-01/02 requirements and SCOPE-05 data-alignment rule"
```

---

## Task 3: Create the phase gap register and update the milestone gap index

**Files:**
- Create: `.planning/phases/20-5-sampling-coordinate-allocation/20-5-GAPS.md`
- Modify: `.planning/milestones/v1.4-GAPS.md`

- [ ] **Step 1: Create `20-5-GAPS.md`**

Create `.planning/phases/20-5-sampling-coordinate-allocation/20-5-GAPS.md` with exactly:
```markdown
---
phase: "20.5"
milestone: v1.4
total_gaps: 3
open_gaps: 0
resolved_gaps: 3
deferred_gaps: 0
last_updated: 2026-05-19
---

# Phase 20.5 Gap Register — Sampling Coordinate Allocation

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
- **Mathematical / engineering grounding:** n/a — naming/schema decision, not a physics
  decision.
- **Agent was tempted to:** name it `AC-SAMP-01` and proceed.
- **What the user needed to decide:** approve the new AC name, or choose another.
- **Confidence of impact:** LOW — naming only; no behavioral consequence.
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
- **Mathematical / engineering grounding:** n/a — naming and coordination decision.
- **Agent was tempted to:** name the file `20-5-DATA-ALIGNMENT.md` and frame it as an
  alignment record rather than a divergence record.
- **What the user needed to decide:** approve the renamed/repurposed hand-off file, or
  require the `NN-CODE-DIVERGENCE.md` pattern.
- **Confidence of impact:** LOW — documentation naming only.
- **Status:** `RESOLVED-WITH-INSTRUCTION`
- **Resolution note:** User approved the Phase 20.5 design (containing
  `20-5-DATA-ALIGNMENT.md`) on 2026-05-19. The file documents spec↔`simulation_data`
  alignment and carries the `AC-SAMP-01` stub.
```

- [ ] **Step 2: Update the milestone gap index frontmatter**

In `.planning/milestones/v1.4-GAPS.md`, find the frontmatter:
```
---
milestone: v1.4
total_gaps: 11
open_gaps: 0
resolved_gaps: 11
deferred_gaps: 0
last_updated: 2026-05-19
---
```
Replace with:
```
---
milestone: v1.4
total_gaps: 14
open_gaps: 0
resolved_gaps: 14
deferred_gaps: 0
last_updated: 2026-05-19
---
```

- [ ] **Step 3: Append the Phase 20.5 section to the milestone gap index**

In `.planning/milestones/v1.4-GAPS.md`, after the final table row of the Phase 17 section
(the `GAP-17-11` row), append:
```

## Phase 20.5: Sampling Coordinate Allocation

**Register:** `.planning/phases/20-5-sampling-coordinate-allocation/20-5-GAPS.md`

| Gap | Decision | Resolution |
|-----|----------|------------|
| GAP-20-5-01 | Sobol coordinate allocation convention | RESOLVED-WITH-INSTRUCTION: lock Option A matching `ic_generation_utils.py` — `u_1`–`u_3` position, `u_4` scale, `u_5`–`u_7` velocity; `d = 3 + δ_s + 3δ_v` |
| GAP-20-5-02 | New acceptance-check name `AC-SAMP-01` | RESOLVED-WITH-INSTRUCTION: approved in Phase 20.5 design review 2026-05-19 (precedent: GAP-17-02) |
| GAP-20-5-03 | Hand-off file naming `20-5-DATA-ALIGNMENT.md` | RESOLVED-WITH-INSTRUCTION: approved in Phase 20.5 design review 2026-05-19; alignment record, not a `NN-CODE-DIVERGENCE.md` (no `pinn/` code performs Sobol allocation) |
```

- [ ] **Step 4: Verify the gap-register edits**

Run:
```bash
grep -cF "GAP-20-5-0" .planning/phases/20-5-sampling-coordinate-allocation/20-5-GAPS.md
grep -cF "GAP-20-5-0" .planning/milestones/v1.4-GAPS.md
grep -cF "total_gaps: 14" .planning/milestones/v1.4-GAPS.md
```
Expected: first = 3 (the three gap headings), second = 3 (the three index rows), third = 1.

- [ ] **Step 5: Commit**

```bash
git add .planning/phases/20-5-sampling-coordinate-allocation/20-5-GAPS.md .planning/milestones/v1.4-GAPS.md
git commit -m "docs(20-5): add gap register with GAP-20-5-01/02/03"
```

---

## Task 4: Apply the five Sobol-allocation edits to sampling_method.md

**Files:**
- Modify: `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`

All five edits must be applied together — a partial application leaves the file
internally inconsistent. One commit at task end.

- [ ] **Step 1: Edit 1 — Line 6 "Critical Update" preamble**

Replace this exact block:
```
**[Critical Update: The script preserves virial ratio in hierarchical ICs (masses normalized consistently with velocities). For quasi-random, scaling is **enabled** in the main block with range (0.8, 1.2), which distorts the virial ratio by $s^3$—see documented warning in "Global Scaling (Optional)". The default would preserve it, but scaling is explicitly enabled for variety.]**
```
With:
```
**[Critical Update: The script preserves virial ratio in hierarchical ICs (masses normalized consistently with velocities). For quasi-random, sampling-time size scaling is **enabled** in the main block with range `[s_lo, s_hi] = [0.8, 1.2]`, which distorts the virial ratio by $s^3$ — see "Sampling-Time Size Variability" below. The default would preserve it, but scaling is explicitly enabled for variety. The Sobol coordinate allocation convention (locked in v1.4 Phase 20.5, matching `simulation_data/Scripts/ic_generation/ic_generation_utils.py`) places this scale factor at coordinate $u_4$ ahead of velocity coordinates $u_5$–$u_7$ in the standard configuration.]**
```

- [ ] **Step 2: Edit 2 — §1.1 Dimension bullet**

Replace this exact line:
```
- **Dimension:** A Sobol engine with base 6 dimensions (3 for position + 3 for velocity) is used, plus optional extras (e.g., 1 for global scaling if enabled via `scale_range`).
```
With:
```
- **Dimension:** The Sobol engine dimension is determined by which sampling features are enabled. Let $\delta_s = 1$ if sampling-time scaling is enabled (`scale_range[0]` $\neq$ `scale_range[1]`) and $0$ otherwise; let $\delta_v = 1$ if velocity sampling is enabled (`velocity_scale > 0`) and $0$ otherwise. The Sobol dimension is then $d = 3 + \delta_s + 3\delta_v$. This formula assumes `rotate=False` (the standard configuration): `ic_generation_utils.py` also exposes an optional `rotate` flag that would add 3 dimensions, but it is disabled by default and is a non-functional placeholder for a future rotation feature, not exercised by the existing dataset. See "Sobol Coordinate Allocation Convention" below for the layout. For the standard quasi-random configuration in `generate_ics.py` (`scale_range=(0.8, 1.2)`, `velocity_scale=0.1`), $\delta_s = \delta_v = 1$ and $d = 7$.
```

- [ ] **Step 3: Edit 3 — Insert the "Sobol Coordinate Allocation Convention" subsection**

Replace this exact block (the §1.2 lead sentence followed by the first subsection heading):
```
The quasi-random numbers $(u_1, u_2, \dots) \in (0, 1)^d$ generated by the Sobol engine must be mapped to the desired physical coordinates.

#### Direction on the Unit Sphere
```
With:
```
The quasi-random numbers $(u_1, u_2, \dots) \in (0, 1)^d$ generated by the Sobol engine must be mapped to the desired physical coordinates.

#### Sobol Coordinate Allocation Convention

The Sobol coordinates $u_i$ use 1-based mathematical indexing throughout this document. Array indexing in implementation should be shifted accordingly.

The allocation order is **fixed**: position, then (optionally) scale, then (optionally) velocity. The dimension count $d = 3 + \delta_s + 3\delta_v$ (for `rotate=False`; see the §1.1 Dimension bullet) is conditional, but the order in which enabled features consume coordinates is invariant.

| Coordinate | Physical role | Drawn when |
|---|---|---|
| $u_1, u_2, u_3$ | Position of the free particle ($\theta, \phi, r$) | Always |
| $u_4$ | Sampling-time size scale factor $s$ | $\delta_s = 1$ only |
| $u_{4+\delta_s}, u_{5+\delta_s}, u_{6+\delta_s}$ | Velocity components of the free particle | $\delta_v = 1$ only |

For the standard configuration ($\delta_s = \delta_v = 1$): $u_1$–$u_3$ position, $u_4$ scale, $u_5$–$u_7$ velocity. When $\delta_s = 0$, no scale coordinate is drawn and velocity coordinates take indices $u_4$–$u_6$.

This convention prevents any Sobol coordinate from being reused for two independent physical quantities, and matches the implementation in `simulation_data/Scripts/ic_generation/ic_generation_utils.py` that generated the existing standard quasi-random dataset.

**Disambiguation note.** The sampling-time scale factor $s$ defined here is distinct from the preprocessing-time global scaling (by constants $D$, $V$, $T$) currently described in `ctl_instruction.md` Step 2 ("Preprocessing: Scaling to Dimensionless Units") and to be locked in v1.4 by Phase 18 (FRAME-04, scaling order) and Phase 19 (PHYS-01, the $D = (G T^2)^{1/3}$ convention) per resolution doc §4.5 and §10.1. They apply at different pipeline stages: this sampling-time $s$ is applied at IC generation; preprocessing scaling is applied after canonical rotation.

#### Direction on the Unit Sphere
```

- [ ] **Step 4: Edit 4 — Rename "Global Scaling (Optional)" → "Sampling-Time Size Variability"**

Replace this exact block:
```
#### Global Scaling (Optional)
An optional global scaling factor $s$ can be applied to all positions and velocities for added variety in system size. It uses an additional Sobol dimension, mapping $u_4$ to a user-defined range $[s_{\min}, s_{\max}]$ (default: $[1.0, 1.0]$, disabling it) via $s = s_{\min} + (s_{\max} - s_{\min})u_4$. For example, the script's main block enables it with $[0.8, 1.2]$ for quasi-random generation.

When enabled, positions scale by $s$ and velocities by $s$. **Impact on Virial Ratio:** This changes $Q = 2T / |U|$ by a factor of $s^3$ (kinetic energy scales as $s^2$, potential as $s^{-1}$). Disable if preserving virial equilibrium is required.
```
With:
```
#### Sampling-Time Size Variability
An optional sampling-time size scale factor $s$ can be applied to all positions and velocities for added variety in system size. The scale factor is sourced from the 4th Sobol coordinate (per the Sobol Coordinate Allocation Convention above) and maps to a user-defined range $[s_{\mathrm{lo}}, s_{\mathrm{hi}}]$ (default: $[1.0, 1.0]$, which disables it: $\delta_s = 0$) via

$$s = s_{\mathrm{lo}} + (s_{\mathrm{hi}} - s_{\mathrm{lo}})\,u_4.$$

For example, the script's main block enables it with $[s_{\mathrm{lo}}, s_{\mathrm{hi}}] = [0.8, 1.2]$ for quasi-random generation.

When enabled, positions and velocities both scale by $s$. **Impact on virial ratio:** this changes $Q = 2T / |U|$ by a factor of $s^3$ (kinetic energy scales as $s^2$, potential as $s^{-1}$). Disable if preserving virial equilibrium is required. When $\delta_s = 0$, no Sobol coordinate is consumed for scaling and velocity coordinates take indices $u_4$–$u_6$ instead of $u_5$–$u_7$.

**Distinct from preprocessing-time scaling.** This sampling-time $s$ is applied at IC generation, **before** the preprocessing pipeline. The preprocessing pipeline subsequently nondimensionalizes the state by constants $D, V, T$ (see the Disambiguation note above). Because the characteristic time $T = t_{\max}$ is a global constant, the sampled $s$ survives preprocessing as variety in the dimensionless IC, manifesting through the virial-ratio distortion that propagates into $E$ and other invariants.

**Symbol note.** The bounds are $s_{\mathrm{lo}}$ (low) and $s_{\mathrm{hi}}$ (high). They are deliberately written `s_lo`/`s_hi` rather than `s_min`/`s_max` to avoid collision with the minimum pairwise separation invariant (denoted `s_min` in the resolution doc's invariant set).
```

- [ ] **Step 5: Edit 5 — §1.2 "Velocity Sampling"**

Replace this exact block:
```
#### Velocity Sampling

The next three Sobol coordinates $(u_4, u_5, u_6)$ are mapped to a 3D velocity vector $\mathbf{v}$ using inverse transform sampling from a normal distribution with mean 0 and standard deviation $\sigma = \text{velocity\_scale}$ (default 0.1):

$$v_i = \Phi^{-1}(u_{3+i};\,\mu=0,\,\sigma=\text{velocity\_scale}),\quad i=1,2,3.$$

The sampler then enforces total momentum conservation by adjusting the velocity of the fixed particle so that $\sum_i m_i \mathbf{v}_i = 0$.
```
With:
```
#### Velocity Sampling

Per the Sobol Coordinate Allocation Convention, the velocity coordinates $(u_{4+\delta_s}, u_{5+\delta_s}, u_{6+\delta_s})$ are mapped to a 3D velocity vector $\mathbf{v}$ for the free particle using inverse transform sampling from a normal distribution with mean 0 and standard deviation $\sigma = \text{velocity\_scale}$ (default 0.1):

$$v_i = \Phi^{-1}(u_{3+\delta_s+i};\,\mu=0,\,\sigma=\text{velocity\_scale}),\quad i=1,2,3.$$

For the standard configuration with $\delta_s = 1$, the velocity coordinates are $(u_5, u_6, u_7)$; when $\delta_s = 0$, they are $(u_4, u_5, u_6)$.

The sampler then enforces total momentum conservation by adjusting the velocity of the fixed particle so that $\sum_i m_i \mathbf{v}_i = 0$.

**Particle indexing note.** "Free particle" here refers to the sampled particle (particle 2 in the pre-canonical-ordering scheme of §1). Phase 18 (FRAME-02) applies canonical ordering that may permute particle indices in downstream artifacts; the velocity vector defined here still describes the same physical particle through the permutation.
```

Note: the momentum-conservation sentence ("...adjusting the velocity of the fixed
particle...") is preserved **verbatim**. Its spec/code discrepancy — a contradiction in
outcome distribution versus the code's symmetric `v1 = v3 = -v2/2` split — is sub-conflict
#1, recorded separately in Task 7 — do NOT alter it here.

- [ ] **Step 6: Verify the spec edits**

Run from the repository root:
```bash
SPEC=pinn_instruction/markdown_conversion/framework-specs/sampling_method.md
grep -c "^#### Sobol Coordinate Allocation Convention$" "$SPEC"   # expect 1
grep -c "^#### Global Scaling (Optional)$" "$SPEC"                # expect 0
grep -c "^#### Sampling-Time Size Variability$" "$SPEC"           # expect 1
grep -c "delta_s" "$SPEC"                                         # expect 3 or more
```
Expected: the new "Sobol Coordinate Allocation Convention" and "Sampling-Time Size
Variability" headings each return 1; the old "Global Scaling (Optional)" heading returns 0
(it was renamed); `delta_s` appears on 3+ lines (the notation propagated through Edits
2–5). If the old heading is non-zero or either new heading is zero, an edit did not apply —
STOP, do not commit, and re-check. (Note: the new "Symbol note" mentions `s_min` only as
an inline-code reference to the resolution-doc invariant — this is intentional, not a
rename failure.)

- [ ] **Step 7: Commit**

```bash
git add pinn_instruction/markdown_conversion/framework-specs/sampling_method.md
git commit -m "docs(20-5): lock Sobol coordinate allocation convention in sampling_method.md"
```

---

## Task 5: Create and run the verification probe

**Files:**
- Create: `.planning/phases/20-5-sampling-coordinate-allocation/probes/verify_sobol_allocation.py`

- [ ] **Step 1: Write the probe**

Create `.planning/phases/20-5-sampling-coordinate-allocation/probes/verify_sobol_allocation.py`
with exactly:
```python
#!/usr/bin/env python3
"""
Phase 20.5 disposable verification probe — Sobol dimension and allocation order.

Confirms two properties of EnhancedThreeBodySampler against
simulation_data/Scripts/ic_generation/ic_generation_utils.py — the implementation
that generated the existing standard quasi-random dataset:

  1. The Sobol dimension formula d = 3 + delta_s + 3*delta_v (rotate=False; the
     rotate flag is a disabled, non-functional stub).
  2. The Sobol coordinate ALLOCATION ORDER for the standard config
     (delta_s = delta_v = 1): column 3 -> scale factor, columns 4-6 -> velocity.

Run from the repository root:
    python .planning/phases/20-5-sampling-coordinate-allocation/probes/verify_sobol_allocation.py
"""
import sys

import numpy as np
from scipy.stats import norm

sys.path.append("simulation_data/Scripts/ic_generation")
from ic_generation_utils import EnhancedThreeBodySampler  # noqa: E402

# --- Test 1: dimension formula d = 3 + delta_s + 3*delta_v (rotate=False) ---
# (scale_range, velocity_scale, expected_d, label)
cases = [
    ((0.8, 1.2), 0.1, 7, "delta_s=1, delta_v=1 (standard config)"),
    ((1.0, 1.0), 0.1, 6, "delta_s=0, delta_v=1"),
    ((0.8, 1.2), 0.0, 4, "delta_s=1, delta_v=0"),
    ((1.0, 1.0), 0.0, 3, "delta_s=0, delta_v=0"),
]

for scale_range, velocity_scale, expected_d, label in cases:
    s = EnhancedThreeBodySampler(
        scale_range=scale_range, velocity_scale=velocity_scale, seed=42
    )
    assert s.sobol_dim == expected_d, (
        f"{label}: expected d={expected_d}, got {s.sobol_dim}"
    )
    print(f"PASS  dimension: {label}: sobol_dim = {s.sobol_dim}")

# --- Test 2: allocation order for the standard config (delta_s = delta_v = 1) ---
# A synthetic Sobol batch with a distinct constant per column lets us prove which
# column each physical quantity is drawn from: if scale read any column other than
# 3, or velocity any columns other than 4-6, the assertions below would fail
# because every column carries a different value.
s = EnhancedThreeBodySampler(scale_range=(0.8, 1.2), velocity_scale=0.1, seed=42)
assert s.sobol_dim == 7, f"standard config: expected d=7, got {s.sobol_dim}"

n_rows = 5
# column j carries the constant 0.1*(j+1) -> 0.1, 0.2, ..., 0.7 (all strictly in (0,1))
synthetic = np.tile(0.1 * (np.arange(7) + 1.0), (n_rows, 1))
p1 = np.array([1.0, 0.0, 0.0])

# _process_sobol_batch returns 7 arrays (its type hint understates this):
# p1_scaled, p2, p3, v1, v2, v3, sobol_batch
p1_scaled, _p2, _p3, _v1, v2_batch, _v3, _ = s._process_sobol_batch(synthetic, p1)

# Scale is drawn from column 3: s = lo + (hi - lo) * u_4, and p1_scaled = p1 * s.
expected_scale = 0.8 + (1.2 - 0.8) * synthetic[:, 3]
assert np.allclose(p1_scaled[:, 0], expected_scale), (
    f"scale not from column 3: p1_scaled[:,0]={p1_scaled[:, 0]}, "
    f"expected {expected_scale}"
)
print("PASS  allocation: scale factor s is drawn from Sobol column 3 (u_4)")

# Velocity is drawn from columns 4-6 via inverse-CDF, then scaled by s.
expected_v2 = norm.ppf(synthetic[:, 4:7], loc=0, scale=0.1) * expected_scale[:, None]
assert np.allclose(v2_batch, expected_v2), (
    f"velocity not from columns 4-6: v2_batch={v2_batch}, expected {expected_v2}"
)
print("PASS  allocation: free-particle velocity is drawn from Sobol columns 4-6 (u_5-u_7)")

print()
print("Sobol dimension formula d = 3 + delta_s + 3*delta_v (rotate=False) and the")
print("allocation order (u_1-u_3 position, u_4 scale, u_5-u_7 velocity) are verified")
print("against simulation_data/Scripts/ic_generation/ic_generation_utils.py.")
```

- [ ] **Step 2: Run the probe**

Run from the repository root:
```bash
python .planning/phases/20-5-sampling-coordinate-allocation/probes/verify_sobol_allocation.py
```
Expected output:
```
PASS  dimension: delta_s=1, delta_v=1 (standard config): sobol_dim = 7
PASS  dimension: delta_s=0, delta_v=1: sobol_dim = 6
PASS  dimension: delta_s=1, delta_v=0: sobol_dim = 4
PASS  dimension: delta_s=0, delta_v=0: sobol_dim = 3
PASS  allocation: scale factor s is drawn from Sobol column 3 (u_4)
PASS  allocation: free-particle velocity is drawn from Sobol columns 4-6 (u_5-u_7)

Sobol dimension formula d = 3 + delta_s + 3*delta_v (rotate=False) and the
allocation order (u_1-u_3 position, u_4 scale, u_5-u_7 velocity) are verified
against simulation_data/Scripts/ic_generation/ic_generation_utils.py.
```
If the probe raises `AssertionError`, the spec's `d = 3 + δ_s + 3δ_v` dimension formula or
its column allocation does not match the code — STOP, do not commit, and surface the
mismatch (this would be a GAP-20-5-01 regression).

- [ ] **Step 3: Commit**

```bash
git add .planning/phases/20-5-sampling-coordinate-allocation/probes/verify_sobol_allocation.py
git commit -m "docs(20-5): add Sobol allocation verification probe"
```

---

## Task 6: Create the data-alignment hand-off document

**Files:**
- Create: `.planning/phases/20-5-sampling-coordinate-allocation/20-5-DATA-ALIGNMENT.md`

- [ ] **Step 1: Write `20-5-DATA-ALIGNMENT.md`**

Create `.planning/phases/20-5-sampling-coordinate-allocation/20-5-DATA-ALIGNMENT.md` with
exactly:
```markdown
# Phase 20.5 — Data Alignment and FUT-01 Hand-off

**Phase:** 20.5 (Sampling Coordinate Allocation)
**Milestone:** v1.4
**Date:** 2026-05-19

## Purpose

This is a forward-pointing hand-off document. It records that the Sobol coordinate
allocation convention locked in `sampling_method.md` by Phase 20.5 **matches** the
data-generation code in `simulation_data/Scripts/ic_generation/ic_generation_utils.py`.
It is an *alignment* record, not a `NN-CODE-DIVERGENCE.md` — see GAP-20-5-03.

## Alignment statement

| Spec claim (`sampling_method.md`, v1.4 Phase 20.5) | Code (`ic_generation_utils.py`) | Status |
|---|---|---|
| `d = 3 + δ_s + 3δ_v` | `sobol_dim` computed at lines 89–99 | ALIGNED |
| `u_1`–`u_3` → position | `_process_sobol_batch` lines 120–145 (`idx 0→3`) | ALIGNED |
| `u_4` → scale `s` (when `δ_s = 1`) | lines 148–151 (`u_scale = sobol_batch[:, idx]`, `idx 3→4`) | ALIGNED |
| `u_{4+δ_s}`–`u_{6+δ_s}` → velocity (when `δ_v = 1`) | lines 162–165 (`u_vel = sobol_batch[:, idx:idx+3]`) | ALIGNED |
| Standard config `d = 7` | `generate_ics.py` lines 41–42 (`scale_range=(0.8,1.2)`, `velocity_scale=0.1`) | ALIGNED |

The existing standard quasi-random dataset in
`simulation_data/Data/ic_final/ic_standard_quasi_random/` was generated under this
convention. The v1.4 spec therefore describes the data that already exists — no
framework-data mismatch.

## FUT-01 hand-off

- FUT-01 implementers build PINN/data code from the v1.4 framework specs. For Sobol
  allocation, the v1.4 spec (`sampling_method.md`, "Sobol Coordinate Allocation
  Convention") is authoritative and is statistically equivalent to the existing
  `ic_generation_utils.py` behavior.
- The PINN code in `pinn/` remains non-authoritative (directive 2026-05-19). If `pinn/`
  data-handling code assumes a different Sobol layout, FUT-01 corrects the `pinn/` code to
  this spec — the spec is not changed to match `pinn/`.
- No data regeneration is required for Sobol-allocation reasons: the spec matches the data.

## AC-SAMP-01 (acceptance check, for Phase 21 execution under VER-04)

- **Name:** `AC-SAMP-01` — Sobol coordinate allocation alignment.
- **What it checks:** the `sampling_method.md` dimension formula `d = 3 + δ_s + 3δ_v` and
  the position/scale/velocity column allocation match
  `simulation_data/Scripts/ic_generation/ic_generation_utils.py`.
- **Data:** none required — instantiates `EnhancedThreeBodySampler` directly.
- **Probe:**
  `.planning/phases/20-5-sampling-coordinate-allocation/probes/verify_sobol_allocation.py`.
- **Pass criterion:** the probe exits 0 with all six `PASS` lines — the four `dimension`
  lines (`sobol_dim` ∈ {7, 6, 4, 3} for `(δ_s, δ_v)` ∈ {(1,1), (0,1), (1,0), (0,0)}) and
  the two `allocation` lines (scale ← Sobol column 3; velocity ← columns 4–6, verified by
  processing a synthetic batch through `_process_sobol_batch`).
- **On failure:** routes back to Phase 20.5 for spec correction per VER-04 / VER-05; v1.4
  does not ship while `AC-SAMP-01` fails.
```

- [ ] **Step 2: Verify the file**

Run:
```bash
grep -cF "AC-SAMP-01" .planning/phases/20-5-sampling-coordinate-allocation/20-5-DATA-ALIGNMENT.md
grep -cF "ALIGNED" .planning/phases/20-5-sampling-coordinate-allocation/20-5-DATA-ALIGNMENT.md
```
Expected: first ≥ 2 (the AC-SAMP-01 section heading and the **Name:** line), second = 5
(the five rows of the alignment table).

- [ ] **Step 3: Commit**

```bash
git add .planning/phases/20-5-sampling-coordinate-allocation/20-5-DATA-ALIGNMENT.md
git commit -m "docs(20-5): add data-alignment hand-off and AC-SAMP-01 stub"
```

---

## Task 7: Record sub-conflict #1 as a separate finding

**Files:**
- Create: `docs/findings/velocity_momentum_sampling_discrepancy.md`

This finding is **out of Phase 20.5 scope**. It is recorded for separate user handling, per
the `CLAUDE.md` directive to flag — not silently fix — source-level discrepancies.

- [ ] **Step 1: Write the finding**

Create `docs/findings/velocity_momentum_sampling_discrepancy.md` with exactly:
```markdown
# Finding: Velocity-momentum reconciliation — contradictory outcome distributions in sampling_method.md

**Date surfaced:** 2026-05-19
**Surfaced during:** Phase 20.5 (Sobol Coordinate Allocation) design work.
**Status:** OPEN — out of Phase 20.5 scope; awaiting user decision on handling.

## Summary

`sampling_method.md` and the data-generation code disagree on how velocities are assigned
to the non-sampled particles. They agree on momentum conservation (both yield zero total
momentum for equal masses) but are **contradictory in outcome distribution**: the code
makes a specific symmetric choice the spec's singular wording does not state, so the two
produce statistically different `v1`/`v3` velocity distributions.

## Detail

`sampling_method.md`, "Velocity Sampling": after the free particle's velocity is sampled,
"The sampler then enforces total momentum conservation by adjusting the velocity of the
fixed particle so that Σ mᵢ vᵢ = 0." This describes adjusting one particle (the fixed
particle) and is silent on the third particle's velocity.

`simulation_data/Scripts/ic_generation/ic_generation_utils.py`, lines 167–171:
```
# For equal masses, maintain zero total momentum
# v1 + v2 + v3 = 0, so we can set v1 = -v2/2, v3 = -v2/2
v1_batch = -v2_batch / 2
v3_batch = -v2_batch / 2
```
The code samples particle 2's velocity, then sets `v1 = v3 = -v2/2` — a symmetric split
across the two non-sampled particles, valid for the equal-mass standard quasi-random case.

## Why this matters

For equal masses, both the spec's "adjust the fixed particle" reading and the code's
symmetric split yield total momentum zero — so they agree on the *conservation* outcome.
But they imply different `v1` and `v3` distributions: this is a contradiction in outcome
distribution, not a mere under-specification. A FUT-01 implementer following the spec
literally ("adjust the fixed particle" only) would produce a statistically different
velocity distribution from the existing dataset.

**FUT-01 guidance:** until the spec prose is corrected, FUT-01 MUST follow the code's
symmetric `v1 = v3 = -v2/2` split — that is the procedure that generated the existing
standard quasi-random dataset.

## Recommended handling (for user decision)

- A: open a follow-up phase / errata to correct the spec prose to describe the symmetric
  `v1 = v3 = -v2/2` split.
- B: defer to FUT-01 as a known spec gap.
- C: judge the discrepancy acceptable for FUT-01 (which follows the code) and close with
  no spec change.

This finding does not block Phase 20.5; the Phase 20.5 spec edits preserve the
momentum-conservation sentence verbatim.
```

- [ ] **Step 2: Verify the file**

Run:
```bash
test -f docs/findings/velocity_momentum_sampling_discrepancy.md && echo "FILE EXISTS"
```
Expected: `FILE EXISTS`.

- [ ] **Step 3: Commit**

```bash
git add docs/findings/velocity_momentum_sampling_discrepancy.md
git commit -m "docs(findings): record velocity-momentum sampling discrepancy"
```

---

## Task 8: Propagate the SCOPE-05 governance principle via gsd-docs-update

**Files:**
- Modify (via skill): `PROJECT.md`, `CLAUDE.md` (the `gsd-docs-update` skill determines
  the precise targets and edits).

This task is performed by invoking the `gsd-docs-update` skill, per user directive
2026-05-19. It is the final, post-phase step.

- [ ] **Step 1: Invoke `gsd-docs-update`**

Invoke the `gsd-docs-update` skill with the following instruction:

> Propagate the new v1.4 governance rule **SCOPE-05** (data-spec alignment for
> sampling-method edits) into the project's core documentation. The rule, already added to
> `.planning/REQUIREMENTS.md` in Phase 20.5, states:
>
> *"When v1.4 framework-spec edits describe the data-generation pipeline, they MUST match
> the actual behavior of `simulation_data/Scripts/ic_generation/`. The no-live-code
> directive (2026-05-19) targets `pinn/` only; `simulation_data/Scripts/ic_generation/` is a permitted
> grounding source for data-generation specs because the existing dataset is fixed and the
> framework must remain compatible with it. Spec divergences from data must be (i)
> reconciled to match data, (ii) flagged in `docs/findings/` for separate handling, or
> (iii) explicitly authorized by the user as a data-regeneration directive for FUT-01."*
>
> Update `PROJECT.md` (Key Decisions / governance context) and, if appropriate, the
> "Source of Truth" / governance section of `CLAUDE.md`, so a future agent treats
> `simulation_data/Scripts/ic_generation/` as a permitted grounding source distinct from the `pinn/`
> no-live-code directive. Verify all claims against the codebase. Do not restate the full
> rule text in multiple files — link to `REQUIREMENTS.md` SCOPE-05 as the canonical source.

- [ ] **Step 2: Review and commit**

Review the `gsd-docs-update` output. Confirm it (a) adds the SCOPE-05 cross-reference, (b)
does not contradict the existing `pinn/` no-live-code directive (SCOPE-01), and (c) changes
nothing else. Then commit with the file paths the skill actually modified:
```bash
git add <files-modified-by-gsd-docs-update>
git commit -m "docs(governance): propagate SCOPE-05 data-spec alignment rule"
```

---

## Post-Completion Follow-ups

Items to revisit after Phase 20.5 and its sibling phases complete — not part of the
Task 1–8 execution.

- [ ] **Re-verify Phase 18/19 cross-references (adversarial review FLAG-10).** After
  Phases 18 and 19 complete, confirm that the cross-references in `sampling_method.md` to
  their scaling conventions remain accurate: Edit 3's Disambiguation note (Phase 18
  FRAME-04 scaling order; Phase 19 PHYS-01, the `D = (G T²)^(1/3)` convention) and Edit 4's
  preprocessing-scaling note. If Phase 18 or 19 renames or revises those conventions,
  update the Edit 3/4 cross-references in `sampling_method.md` accordingly.

---

## Self-Review

Run after all tasks are written — checklist, not a subagent dispatch.

**1. Spec coverage** — every section of the design doc maps to a task:
- Design §4 Edits 1–5 → Task 4. ✓
- Design §5.1 ROADMAP → Task 1. ✓
- Design §5.2 SAMP-01/02 + §5.3 SCOPE-02/SCOPE-05 → Task 2. ✓
- Design §5.4 v1.4-GAPS + §5.5 GAP record → Task 3. ✓
- Design §5.6 DATA-ALIGNMENT + §6 AC-SAMP-01 → Task 6. ✓
- Design §6 verification probe → Task 5. ✓
- Design §8 sub-conflict #1 → Task 7. ✓
- Design §5.3 SCOPE-05 propagation → Task 8. ✓
- Refinements beyond the design doc: `SCOPE-D`→`SCOPE-05` (numbering consistency);
  `GAP-20-5-02`/`GAP-20-5-03` added (Phase 17 precedent for recording process-artifact
  schema decisions). Both folded into Tasks 2 and 3.

**2. Placeholder scan** — no "TBD/TODO/implement later". Every edit shows verbatim
FROM/TO text; every new file shows full content; the probe is complete code. Task 8
delegates to `gsd-docs-update` by design (user directive) and supplies the exact rule text
and target files — not a placeholder.

**3. Type/identifier consistency** — `δ_s`, `δ_v`, `d = 3 + δ_s + 3δ_v` are identical
across Edits 2, 3, 4, 5, the gap register, the data-alignment doc, and the probe.
`AC-SAMP-01`, `SAMP-01`, `SAMP-02`, `SCOPE-05`, `GAP-20-5-01/02/03` are spelled
consistently throughout. Commit message prefix `docs(20-5):` is uniform.

**Verification note:** all FROM text in Task 4 was quoted verbatim from the current
`sampling_method.md` (lines 6, 90, 94–98, 108–119) and verified 2026-05-19. The probe's
`EnhancedThreeBodySampler(scale_range=..., velocity_scale=..., seed=...)` signature matches
`ic_generation_utils.py` lines 60–61.
