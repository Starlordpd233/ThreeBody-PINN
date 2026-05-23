---
phase: "20.5"
slug: sampling-coordinate-allocation
milestone: v1.4
type: research
origin: "docs/superpowers/specs/2026-05-19-sobol-allocation-ambiguity-design.md"
date: 2026-05-19
status: complete
---

# Phase 20.5 Research — Sampling Coordinate Allocation

This document records the research findings that inform Phase 20.5 (Sampling Coordinate
Allocation). It is the GSD-native extraction of the design rationale originally authored at
`docs/superpowers/specs/2026-05-19-sobol-allocation-ambiguity-design.md` (571 lines).
The design doc is the historical artifact; this file is the authoritative research reference
for Phase 20.5 execution.

**Companion documents:**
- Design rationale (historical): `docs/superpowers/specs/2026-05-19-sobol-allocation-ambiguity-design.md`
- Implementation plan: `.planning/phases/20-5-sampling-coordinate-allocation/20-5-PLAN.md`
- Gap register: `.planning/phases/20-5-sampling-coordinate-allocation/20-5-GAPS.md`
- Origin finding: `docs/findings/addressing_sobol_sequence_suggestion.md`

---

## 1. Problem Diagnosis

`pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` double-books the
4th Sobol coordinate `u_4`:

- **§1.1 "Low-Discrepancy Engine"**: "A Sobol engine with base 6 dimensions (3 for position
  + 3 for velocity) is used, plus optional extras (e.g., 1 for global scaling if enabled via
  `scale_range`)."
- **"Global Scaling (Optional)"**: maps `u_4` to the scale factor
  `s = s_min + (s_max - s_min) u_4`.
- **"Velocity Sampling"**: assigns `(u_4, u_5, u_6)` to the velocity vector, with
  `v_i = Φ⁻¹(u_{3+i})`.

When scaling is enabled — which is the active standard quasi-random configuration
(`scale_range=(0.8, 1.2)`) — `u_4` is described as **both** the scale factor and the first
velocity component. The spec is internally contradictory. A FUT-01 implementer cannot
determine the intended allocation from the spec alone.

This was raised in `docs/findings/addressing_sobol_sequence_suggestion.md`. The finding's
structural diagnosis is correct; its recommended fix ("Option A") turned out to match
reality (see §4).

---

## 2. Code Analysis: Data-Generation Pipeline

### 2.1 Dimension computation

`simulation_data/Scripts/ic_generation/ic_generation_utils.py`, class
`EnhancedThreeBodySampler` (lines 89–99):

```python
self.use_scaling  = (scale_range[0] != scale_range[1])
self.use_velocity = (velocity_scale > 0)
self.sobol_dim = 3                          # base: position
if self.use_scaling:  self.sobol_dim += 1   # +1 scale
if self.use_velocity: self.sobol_dim += 3   # +3 velocity
if self.rotate:       self.sobol_dim += 3   # +3 rotation (non-functional stub; rotate=False default)
```

The dimension is **conditional**: `d = 3 + δ_s + 3δ_v` where `δ_s = 1` iff scaling is
enabled and `δ_v = 1` iff velocity sampling is enabled. The `rotate` flag adds 3 dimensions
but is a disabled-by-default, non-functional stub — excluded from the locked formula.

### 2.2 Allocation order

`_process_sobol_batch` (lines 120–164): insertion order — position, then scale, then
velocity. `idx` advances `0 → 3` (position), `3 → 4` (scale, if `use_scaling`), then
`idx:idx+3` (velocity, if `use_velocity`).

For the standard config (`scale_range=(0.8, 1.2)`, `velocity_scale=0.1`), both flags are
True, `sobol_dim = 7`, and the allocation is:

| Sobol column (0-based) | Math index (1-based) | Physical role |
|---|---|---|
| 0, 1, 2 | `u_1, u_2, u_3` | Position (θ, φ, r) |
| 3 | `u_4` | Scale factor `s` |
| 4, 5, 6 | `u_5, u_6, u_7` | Velocity components |

### 2.3 Provenance

Repository documentation identifies `ic_generation_utils.py` and `generate_ics.py` as the
standard quasi-random generator, but no in-repo generation manifest or commit hash
independently proves every existing IC was produced by this exact script revision. Locking
the convention matching this code means the v1.4 spec matches the documented/current
generator behavior for the data that already exists.

### 2.4 Hierarchical ICs are unaffected

`generate_stable_hierarchical_systems` (lines 290–443) uses `np.random.uniform` only — no
Sobol sequence. The Sobol-allocation convention applies solely to standard quasi-random ICs.

---

## 3. Mathematical Grounding

### 3.1 Virial ratio distortion under uniform rescaling

Under uniform rescaling `r → s·r, v → s·v`:
- Kinetic energy `T = ½ Σ mᵢ|vᵢ|² → s²T`
- Newtonian potential `U = -G Σ mᵢmⱼ/|rᵢ-rⱼ| → s⁻¹U`
- Virial ratio `Q = 2T/|U| → s³Q`

This is derived from first principles and is uncontroversial.

### 3.2 Coordinate coupling risk

If a single Sobol coordinate were reused for both the scale factor `s` and the first
velocity component `v_1`, the two would be deterministically affine-coupled, collapsing an
independent sampling dimension and injecting a hidden correlation beyond the documented `s³`
virial distortion. The actual code uses distinct coordinates — no coupling.

### 3.3 Sobol low-discrepancy preservation

Sobol sequences preserve low-discrepancy under coordinate projection. The conditional
dimension count (`d = 3 + δ_s + 3δ_v`) does not degrade coverage of the coordinates actually
used. This is a standard property of Sobol sequences.

### 3.4 Preprocessing survival

The sampling-time scale factor `s` survives preprocessing: the characteristic time
`T = t_max` is a global constant, so `D, V` are per-milestone constants. The sampled `s`
manifests as variety in the dimensionless IC, propagating through the virial-ratio
distortion into `E` and other invariants.

---

## 4. Decision Analysis: Allocation Options

Three options were considered:

| Option | Convention | Pros | Cons |
|--------|-----------|------|------|
| **A** (LOCKED) | Conditional: `u_1–u_3` position, `u_4` scale (if enabled), `u_{4+δ_s}–u_{6+δ_s}` velocity | Matches existing data-generation code; preserves dataset compatibility | Velocity indices shift depending on `δ_s` |
| **B** | Fixed 7-dim: `u_1–u_3` position, `u_4–u_6` velocity, `u_7` scale | Clean QMC properties; fixed allocation | **Contradicts existing dataset** — code uses Option A |
| **C** | Decoupled scale stream: separate RNG for scale | Eliminates Sobol interaction entirely | Over-engineering; no dataset alignment benefit |

**Decision:** Option A, per user instruction 2026-05-19. Initially Option B was selected on
QMC-purity grounds; corrected after consulting `ic_generation_utils.py` showed the actual
convention is Option A. Data-spec alignment (SCOPE-05) takes priority over QMC aesthetics.

**Agent temptation note:** The agent was tempted to lock Option B on QMC-purity grounds.
The user surfaced the data-alignment requirement, and consulting the code confirmed Option A.

---

## 5. Governance Framework

### 5.1 SCOPE-05 — Data-spec alignment rule

The key governance innovation of Phase 20.5 is **SCOPE-05**: when v1.4 framework-spec edits
describe the data-generation pipeline, they MUST match the actual behavior of
`simulation_data/Scripts/ic_generation/`. The no-live-code directive (2026-05-19) targets
`pinn/` only; `simulation_data/Scripts/ic_generation/` is a **permitted grounding source**
for data-generation specs because the existing dataset is fixed and the framework must
remain compatible with it.

Spec divergences from data must be:
1. Reconciled to match data, or
2. Flagged in `docs/findings/` for separate handling, or
3. Explicitly authorized by the user as a data-regeneration directive for FUT-01.

### 5.2 Requirements introduced

- **SAMP-01**: `sampling_method.md` documents an explicit Sobol coordinate allocation
  convention with no coordinate reused for two independent physical quantities. Dimension
  formula `d = 3 + δ_s + 3δ_v`.
- **SAMP-02**: The §1.1 dimension claim, "Sampling-Time Size Variability" prose, and
  "Velocity Sampling" prose/formula are mutually consistent and agree with the locked
  allocation, matching `ic_generation_utils.py`.

### 5.3 Acceptance check: AC-SAMP-01

A new acceptance check `AC-SAMP-01` is introduced (approved per GAP-20-5-02) for Phase 21
execution under VER-04. It verifies that the spec's dimension formula and column allocation
match `ic_generation_utils.py` using a disposable Python probe with synthetic Sobol data.

**Pass criterion (finalized):** the probe exits 0 with all six PASS lines — four dimension
lines (`sobol_dim` ∈ {7, 6, 4, 3} for `(δ_s, δ_v)` ∈ {(1,1), (0,1), (1,0), (0,0)}) and two
allocation lines (scale ← Sobol column 3; velocity ← columns 4–6, verified by processing a
synthetic batch through `_process_sobol_batch` with `n_rows = 5`).

---

## 6. Cross-Milestone Consistency

### 6.1 Hard conflicts resolved

- **"Global scaling" name collision**: The resolution doc §4.5 and `ctl_instruction.md`
  Step 2 define a preprocessing-time nondimensionalization ("global scaling" by `D, V, T`).
  `sampling_method.md` used "Global Scaling" for a sampling-time random scale. Phase 20.5
  renames the sampling-method section to "Sampling-Time Size Variability" with a
  disambiguation note.
- **`s_min` symbol collision**: `s_min` is the minimum pairwise separation invariant in the
  resolution doc. Phase 20.5 renames the scale bounds to `s_lo / s_hi`.

### 6.2 Cross-references

| Ref | Target | Status |
|-----|--------|--------|
| C | Phase 17 IC₁₃ | No conflict — sampled `s` enters via `s³` virial distortion in `E` |
| D | Phase 18 FRAME-04 | Sampling-time `s` precedes preprocessing; cross-linked in Edits 3–4 |
| E | Phase 21 | New `AC-SAMP-01` acceptance check |
| F | LaTeX original | Phase 20.5 edits Markdown only; LaTeX is v1.3-era source artifact |
| G | `20-5-DATA-ALIGNMENT.md` | FUT-01 hand-off document |

### 6.3 Post-completion re-verification (FLAG-10)

After Phases 18 and 19 complete, re-verify that `sampling_method.md` cross-references to
their scaling conventions (FRAME-04, PHYS-01) remain accurate. Update Edits 3–4 if those
phases rename or revise the conventions.

### 6.4 Confirmed non-conflicts

- Phase 17 GAP-17-01 (raw ordered masses): standard quasi-random is equal-mass; hierarchical
  mass sampling is not via Sobol.
- Phase 19 (raw-mass scaling, softening, energy regularizer, ALM): no interaction with
  sampling-time `s`.
- Phase 20 (SIREN, LayerNorm, inertia, dataset support): no interaction.
- Resolution doc: silent on sampling-time scaling and Sobol allocation; no §10.X patch
  targets `sampling_method.md`.

---

## 7. Out-of-Scope Findings

### 7.1 Sub-conflict #1 — Velocity-momentum reconciliation

`sampling_method.md` says momentum conservation is enforced "by adjusting the velocity of
the fixed particle." `ic_generation_utils.py` (lines 167–171) performs a symmetric split
`v1 = v3 = -v2/2`. For equal masses both yield total momentum zero, but they are
**contradictory in outcome distribution**: the `v1`/`v3` distributions differ. A literal
FUT-01 implementer following the spec would produce a statistically different dataset.

**Status:** Flagged to `docs/findings/velocity_momentum_sampling_discrepancy.md`; out of
Phase 20.5 scope. FUT-01 must follow the code's symmetric split until the spec is corrected.

### 7.2 Sub-conflict #2 — §2.1 enhancement framing

§2.1 discusses velocity-sampling alternatives ("6 additional Sobol dimensions" for two free
particles). Its hypothetical analysis holds only for `δ_s = 0`; under the standard
configuration (`δ_s = 1`) the total would be `d = 3 + 1 + 6 = 10`, not 9. Mild ambiguity,
out of Phase 20.5 scope. Unaffected by the Phase 20.5 edits.

---

## 8. Verification Summary

**Math (verified 2026-05-19):**
- `s³` virial-ratio scaling derived from first principles. ✓
- Sampled `s` survives preprocessing: `T = t_max` is a global constant. ✓
- Sobol projections preserve low-discrepancy. ✓

**Code (`ic_generation_utils.py`, verified 2026-05-19):**
- `sobol_dim = 3 + δ_s + 3δ_v` for `rotate=False` (lines 89–99). ✓
- Allocation order position → scale → velocity (lines 120–164). ✓
- Standard config `d = 7`, layout `u_1–u_3 / u_4 / u_5–u_7`. ✓
- Hierarchical path uses no Sobol (lines 290–443). ✓
- Positions and velocities both scale by `s` (lines 152–153, 174–176). ✓

**Spec cross-references (verified 2026-05-19):**
- `ctl_instruction.md` Step 2 is the preprocessing scaling section. ✓
- All FROM text in spec edits quoted verbatim from current `sampling_method.md`. ✓
- No resolution-doc §10.X patch targets `sampling_method.md`. ✓

**Adversarial review (2026-05-19):**
- 3 BLOCK findings in design doc (wrong gap count, weak probe, false arithmetic) — all
  resolved in commit b727b15.
- 10 FLAG findings — 7 resolved, 2 correctly skipped, 1 (dataset provenance) addressed via
  explicit provenance caveat in `20-5-DATA-ALIGNMENT.md`.
- 3 P1 cross-document inconsistencies (SCOPE-D→SCOPE-05 naming, success criteria count,
  AC-SAMP-01 timing) — resolved in this GSD document set by adopting the plan's corrected
  terminology as authoritative.
