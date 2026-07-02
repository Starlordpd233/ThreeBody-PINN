# Phase 30: PKG-08 Reports Characterization

This file characterizes the **two curriculum-relevant research reports** that issue-03
(`03-curriculum-and-training-loop.md`) repeatedly cites: `review_of_framework.md` and
`stage_strat_revision.md`. It is the v1.6 analog of the v1.5 `23-DQA-CHARACTERIZATION.md`
(which covered one report; this covers two).

**Governance:** This is a **read-only** characterization (SCOPE-09, PKG-08). Both source
files are byte-for-byte unchanged after this work — verified by `git diff --quiet <file>`
(exit 0) and by content-SHA-256 lines in `30-SNAPSHOT-HASHES.txt`. Neither report is an
authoritative framework spec; both are research reports under `framework-revisions/`. This
characterization is a **standalone phase artifact — never uploaded** into the research package
(the package carries byte-for-byte snapshots of the reports themselves, annotated in the
manifest with the role recommendation derived here).

**Sequencing (D-19):** The characterization completes BEFORE the document list is finalized
(30-02/30-03), so the Package-Inclusion Recommendation column below locks each report's
manifest shipping annotation in advance.

**Characterized:** 2026-06-18
**Characterized by:** Phase 30 Plan 01 Task 2 (T-30-01-02)

---

## Report 1 — `review_of_framework.md`

**File:** `pinn_instruction/markdown_conversion/framework-revisions/review-of-framework/review_of_framework.md`
**Lines:** 529
**Location:** `framework-revisions/` (research report, NOT an authoritative spec; SCOPE-09)
**Title:** "A Technical Review and Resolution Blueprint for the CTL-PINN Framework for the Three-Body Problem"
**Governance:** Read-only — zero edits to the source file (SCOPE-09, CLAUDE.md Source of Truth)

### Provenance

Git history (`git log --follow --oneline`), recorded re-derivably:

| Commit | Phase / Event | Description |
|--------|---------------|-------------|
| `bf127b06` | pre-v1.3 | Consolidate PINN instruction LaTeX + markdown into `markdown_conversion/` |
| `b1d2c306` | Phase 13 Plan 02 | Audit and fix review-of-framework sections 1–4 |
| `84411d62` | Phase 13 Plan 02 | Audit and fix review-of-framework sections 5–7 |
| `4318cbfc` | Phase 13 Plan 03 | Promote review-of-framework markdown to authoritative path; finalize verification report |
| `1d4b4b18` | Phase 12 | wip: cross-phase markdown fixes in progress |
| `ef79bd02` | Phase 15.1 Plan 01 | Resolve 7 CRITICAL markdown conversion errors |
| `0f7a80e6` | Phase 15.1 Plan 02 | Resolve 19 MAJOR markdown conversion errors (Wave B) |
| `431567cd` | Phase 15.1 Plan 03 | Replace prose em-dashes with Unicode em-dash (4 files) |
| `efefff73` | Phase 15.1 Plan 03 | Unescape `\~` tildes in review_of_framework.md (Task 12) |
| `f98a1caf` | post-Phase 15.1 | Move core framework markdowns into `framework-specs/` |
| `6ab19ea3` | post-Phase 15.1 | Move revision markdowns into `framework-revisions/` (current path) |

**Design edits:** None during v1.4, v1.5, or v1.6. All commits are markdown-conversion audit/format
fixes (Phases 12–15.1) plus directory moves. The substantive content is the original blueprint
authored pre-v1.3; no design position has been re-litigated in-repo.

**Latest source commit (provenance pin):** `6ab19ea3f8f9248578296472f75b659a8e5b19a4`

### Section Map

| § | Lines | Content |
|---|-------|---------|
| Title + Executive Summary | 1–19 | Framework-review overview; scope of the resolution blueprint |
| §1 Foundational Physical Metrics for Curriculum Design | 20–131 | — |
| — §1.1 `τ_L` and `L / L_max` computation | 24–82 | Lyapunov-time + max-angular-momentum definitions and implementation |
| — §1.2 Global Scale (`D`) Computation Pipeline | 83–131 | The characteristic-length-scale `D` derivation — the `D`-conflict ground |
| §2 Unifying Data Scaling and Normalization Protocols | 132–229 | — |
| — §2.1 Spatiotemporal normalization + unit conversion | 136–174 | Standardization of position/time scaling |
| — §2.2 Consistent Application of Numerical Softening Parameters | 175–192 | **Standardizes `ε_soft = 10⁻⁵` for ALL force/energy/loss calculations** — the D-06 epsilon anchor |
| — §2.3 Finalized IC-vector normalization schema | 193–229 | Input-vector normalization |
| §3 Architectural & Initialization Refinements (SIREN) | 230–261 | §3.1 curriculum-integrated `ω₀` schedule |
| §4 A Rigorous Multi-Component Loss Function Framework | 262–392 | — |
| — §4.1 Scaled quantities in all loss components | 266–285 | NS-18 loss-scaling contract |
| — §4.2 ALM parameter state management | 286–315 | ALM state mgmt (LOOP-05 / μ_p clamp context) |
| — §4.3 AD reference implementation (kinematics) | 316–376 | NS-12 component-wise AD |
| — §4.4 Huber-loss `δ` for normalized energy | 377–392 | NS-13 `δ` selection |
| §5 A Coherent Training & Data Sampling Strategy | 393–500 | — |
| — §5.1 Unifying data + collocation sampling | 397–432 | B-07 / B-08 unified sampling; the D-04 Option B (global+ALM) SOT anchor |
| — §5.2 Curriculum-aware batch construction protocol | 433–458 | Batch construction (240 replay / 16 lookahead context) |
| — §5.3 Mixed-resolution trajectory data integration | 459–476 | `dt_out`-aware data integration (M16 context) |
| — §5.4 Curriculum-aware gradient clipping | 477–500 | M14 gradient-clip context |
| Conclusion & Consolidated Recommendations | 501–524 | Synthesis |
| Source Issues / Notes for Future Reconciliation | 525–529 | SI notes |

### Relation to the doc-03 findings

`review_of_framework.md` is the **single most doc-03-relevant report**: it is the
"State Of Truth" (SOT) anchor issue-03 repeatedly cites. The findings it grounds:

| doc-03 finding | Grounded in | What it provides |
|----------------|-------------|------------------|
| **M7** (`τ_L` excluded from IC vector by design) | §1.1 | `τ_L` / `L/L_max` definitions |
| **`D` conflict / CURR-02** (`D = 6.694` vs locked `D ≈ 4.6416`) | §1.2 | The global-scale `D` computation pipeline |
| **D-06** (epsilon strategy) | §2.2 | `ε_soft = 10⁻⁵` standardization (see hard-constraint flag below) |
| **D-05** (s_min frame) | §2.2 (softening), §2.1 (normalization) | Softening + scaling context for the s_min gate |
| **NS-18** (loss-component scaling contract) | §4.1 | Scaled-quantities-in-loss contract |
| **NS-12** (AD velocities/accelerations) | §4.3 | Component-wise AD reference impl |
| **NS-13** (Huber `δ`) | §4.4 | `δ` selection from `|ΔH|` quantiles |
| **LOOP-05 / ALM μ_p clamp** (MINOR) | §4.2 | ALM parameter state management |
| **D-04** (causal training mode) | §5.1, §5.2 | Global+ALM unified sampling = the Option B SOT |
| **B-07** (batch construction not implemented) | §5.1, §5.2 | Unified data/collocation batch protocol |
| **B-08** (data-fidelity vs collocation conflation) | §5.1 | Point-type separation |
| **M16** (`dt_out`-aware collocation scaling) | §5.3 | Mixed-resolution data integration |
| **M14** (gradient-clip merge) | §5.4 | Curriculum-aware gradient clipping |

### Non-authoritative status

This is a research report under `framework-revisions/` (SCOPE-09), NOT an authoritative
framework spec. It is **baseline design intent** (ERW rule 6): its design positions are the
current SOT the external research starts from, but it is non-authoritative and may contain
positions the resolution doc revises. The authoritative spec-edit targets are
`ctl_instruction.md` and `pinn_architecture.md` (SCOPE-13); this report is never edited.

### Package-Inclusion Recommendation

**Recommendation: INCLUDE** (byte-for-byte intact snapshot).

**Shipping annotation (locks the 30-03 manifest entry):**
"baseline design intent (ERW rule 6) + **baseline-critique mandate**; curriculum-relevant
research report (SCOPE-09, non-authoritative); the external research may challenge its design
positions ONLY via explicit option-vs-baseline proposals."

**CRITICAL — locked-within-baseline hard constraints (F10).** The baseline-critique mandate
applies to this report's **revisable design positions only**, NEVER to SCOPE-12-locked
outcomes. The following values this report touches are **HARD CONSTRAINTS — exempt from the
critique mandate** (they were locked in v1.4/v1.5 and v1.6 does not re-open them absent new
first-principles evidence surfaced through EVID-15):

| Locked value (this report's location) | SCOPE-12 lock | Status |
|---------------------------------------|---------------|--------|
| `ε_soft = 10⁻⁵` (§2.2, lines 175–192) | PHYS-03 softening | **HARD CONSTRAINT — not re-opened.** The report's §2.2 standardization to `ε_soft = 10⁻⁵` AGREES with the lock; D-06's open question is the dual-context epsilon *strategy* (where `1e-10` vs `1e-5` apply), NOT the softening value `1e-5` itself |
| Raw-mass `D ≈ 4.6416` convention | PHYS-01 (`D = (G·T²)^(1/3) ≈ 4.6416`) | **HARD CONSTRAINT.** `D = 6.694` was rejected by v1.5 Phase 25 EVID-10. The §1.2 `D` pipeline is read against the locked raw-mass convention; see CLM Register CLM-01/CLM-19 |
| Post-v1.3 SCS gate (`ε_H > 10⁻⁵` / `SCS > −5`) | post-v1.3 SCS gate | **HARD CONSTRAINT** wherever the report's validation discussion touches it |
| 14D input `[τ, IC₁₃]`, Jacobi IC₁₃, mass-weighted COM projection head | v1.4 architecture locks | **HARD CONSTRAINTS** wherever §2.3 normalization references the IC vector |

So the critique mandate **cannot be read as inviting challenge to a hard constraint.** The
external research grades this report "baseline design intent, critique freely" — but the
SCOPE-12-locked values above are off the table.

*This characterization was produced with zero edits to `review_of_framework.md` (verified: `git diff --quiet` exits 0; content SHA-256 recorded in `30-SNAPSHOT-HASHES.txt`).*

---

## Report 2 — `stage_strat_revision.md`

**File:** `pinn_instruction/markdown_conversion/framework-revisions/stage-strat-revision/stage_strat_revision.md`
**Lines:** 427
**Location:** `framework-revisions/` (research report, NOT an authoritative spec; SCOPE-09)
**Title:** "A Data-Driven Stage Assignment Framework for Curriculum Transfer Learning in N-Body Dynamics"
**Governance:** Read-only — zero edits to the source file (SCOPE-09, CLAUDE.md Source of Truth)

### Provenance

Git history (`git log --follow --oneline`), recorded re-derivably:

| Commit | Phase / Event | Description |
|--------|---------------|-------------|
| `bf127b06` | pre-v1.3 | Consolidate PINN instruction LaTeX + markdown into `markdown_conversion/` |
| `5d0afd33` | Phase 14 Plan 02 | Audit and fix all 6 stage-strat-revision sections (3 critical defects, pandoc artifacts, heading fixes) |
| `d2d90ace` | Phase 14 Plan 03 | Promote stage-strat-revision markdown to authoritative path; finalize verification report |
| `ef79bd02` | Phase 15.1 Plan 01 | Resolve 7 CRITICAL markdown conversion errors |
| `0f7a80e6` | Phase 15.1 Plan 02 | Resolve 19 MAJOR markdown conversion errors (Wave B) |
| `431567cd` | Phase 15.1 Plan 03 | Replace prose em-dashes with Unicode em-dash (4 files) |
| `6a9fbd88` | Phase 15.1 Plan 03 | Add Source-Issues note for missing I3 column (Task 15) |
| `f98a1caf` | post-Phase 15.1 | Move core framework markdowns into `framework-specs/` |
| `6ab19ea3` | post-Phase 15.1 | Move revision markdowns into `framework-revisions/` (current path) |
| `c68cc406` | post-Phase 15.1 | Update stale LaTeX source path in conversion note |
| `02343852` | audit | Resolve CRITICAL C-1 by restoring deleted authcomment |
| `0ee9652f` | docs | Add SI-SSR-001 documenting I3 schema gap |
| `0844b3aa` | fix | Add Part I–IV labels to H1s and update TOC anchors |
| `57de4e4a` | fix | Replace unresolvable Section 1.2 cross-reference |
| `2f952cf0` | Phase 21 | Define/execute numerical acceptance checks and validation handoff (touched in batch) |

**Design edits:** None during v1.4, v1.5, or v1.6. All commits are markdown-conversion audit/format
fixes (Phases 14–21), heading/anchor repairs, a directory move, and the SI-SSR-001 Source-Issues
note (a documentation-of-a-gap, not a design change). The substantive methodology is the original
report authored pre-v1.3.

**Latest source commit (provenance pin):** `2f952cf0154b40e054287902716f16f8d50db576`

### Section Map

| Part / § | Lines | Content |
|----------|-------|---------|
| Title + Contents + Abstract | 1–27 | Title, TOC, abstract |
| Part I. Foundational Principles of Data-Driven Stratification | 28–107 | — |
| — Rationale for adaptive curricula | 32–41 | Why adaptive curricula for physics simulations |
| — Lexicon of difficulty metrics | 42–71 | Difficulty-metric vocabulary for the 3-body problem |
| — Core stratification techniques (PCA / clustering / quantile binning) | 72–107 | Composite stability score; dynamical-regime clustering; balanced quantile pacing |
| Part II. Revised Algorithmic Workflow for Stage Stratification | 108–180 | — |
| — Phase I: Invariant computation + feature engineering | 112–156 | Pre-computation, invariant calc, **normalized virial ratio** sampling-artifact correction, feature DataFrame |
| — Phase II: EDA + landscape mapping | 157–180 | Stratified distribution, correlation, low-dim visualization |
| Part III. Deriving Adaptive Stage Criteria — Hybrid Strategy | 181–239 | Stable subset (hierarchical → stages 0–1); complex subset (quasi-random → stages 2–6); population balancing |
| Part IV. Implementation & Validation Protocol | 240–420 | Python reference impl; advanced refinements; curriculum-validation protocol; conclusions |
| References | 399–420 | — |
| Source Issues / Notes for Future Reconciliation | 421–427 | SI-SSR-001 (I3 schema inconsistency) |

### Relation to the doc-03 findings

`stage_strat_revision.md` is the deep-dive companion to issue-03 §6
("Data-Driven Adaptive Stage Assignment"). The findings it grounds:

| doc-03 finding | Grounded in | What it provides |
|----------------|-------------|------------------|
| **CURR-01 / adaptive stage assignment** | Part II Phase I–II, Part III | The full EDA-driven stage-assignment methodology that issue-03 §6 pseudocode references |
| **EDA methodology** | Part II Phase II (lines 157–180) | Stratified distribution / correlation / PCA workflow |
| **Stage-assignment + the >10%-per-stage safeguard** | Part III (population balancing, lines 213–239) | Hybrid stratification + population control / stage merging (the per-stage population safeguard) |
| **Normalized virial ratio (sampling-artifact correction)** | Part II Phase I (lines 132–141) | Bias correction feeding the difficulty metric |
| **SI reconciliation (VER-18, downstream)** | Source Issues (SI-SSR-001) | I3 schema inconsistency flagged for later reconciliation |

### Non-authoritative status

This is a research report under `framework-revisions/` (SCOPE-09), NOT an authoritative
framework spec. It is **baseline design intent** (ERW rule 6) for the curriculum
stage-assignment methodology. The stage-assignment EDA run and any adaptive-stage-assignment
implementation are FUT-01/FUT-04 (SCOPE-14/15) — never executed in v1.6. This report supplies
the methodology baseline; it is never edited.

### Package-Inclusion Recommendation

**Recommendation: INCLUDE** (byte-for-byte intact snapshot).

**Shipping annotation (locks the 30-03 manifest entry):**
"baseline design intent (ERW rule 6) + **baseline-critique mandate**; data-driven
stage-assignment research report (SCOPE-09, non-authoritative); the external research may
challenge its methodology positions ONLY via explicit option-vs-baseline proposals."

**Locked-within-baseline note (F10).** This report is methodology-centric and touches fewer
SCOPE-12 hard constraints than `review_of_framework.md`. Where it references dataset facts
(per-variant counts, snapshot/`dt_out` distributions) those are the v1.5-verified anchors —
see the CLM Register `verified` rows (CLM-13..CLM-18). Where it references the stage-trajectory
population counts, those are **claimed-unverified** (CLM-02..CLM-07): the report proposes an
*adaptive* assignment methodology, and the concrete per-stage counts are design outputs that no
v1.6 phase verifies (D-17). The critique mandate applies to the methodology; it does not invite
re-opening the v1.5-verified dataset anchors.

*This characterization was produced with zero edits to `stage_strat_revision.md` (verified: `git diff --quiet` exits 0; content SHA-256 recorded in `30-SNAPSHOT-HASHES.txt`).*

---

## Cross-report summary (for the 30-03 manifest)

| Report | Lines | Package role (manifest annotation) | Primary doc-03 cluster |
|--------|-------|-------------------------------------|------------------------|
| `review_of_framework.md` | 529 | baseline design intent + baseline-critique mandate (locked-within-baseline values exempt, F10) | D-04 / D-05 / D-06 / NS-12 / NS-13 / NS-18 / B-07 / B-08 / M7 / M14 / M16 / the `D` conflict |
| `stage_strat_revision.md` | 427 | baseline design intent + baseline-critique mandate | CURR-01 / EDA methodology / stage assignment / >10%-per-stage safeguard |

Both shipping annotations are **confirmed by this characterization** before the document list is
finalized (D-19 sequencing). 30-03's manifest carries these annotations verbatim.
