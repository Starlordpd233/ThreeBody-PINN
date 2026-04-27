# Phase 9: Issues Directory Consolidation - Context

**Gathered:** 2026-04-27
**Status:** Ready for planning

<domain>
## Phase Boundary

Reorganize the 7 scattered issue/audit files in `pinn_instruction/original_latex/review-of-framework/issues/` into 3 thematic Markdown documents grouped by system layer (architecture-and-physics, data-pipeline-and-validation, curriculum-and-training-loop). Originals are moved to a new `issues/archive/` subdirectory; a `MIGRATION.md` records section-level provenance; an `issues/README.md` provides navigation. No source code, no LaTeX templates, and no implementation of any audit finding is in scope — this phase produces consolidated documentation only.

</domain>

<decisions>
## Implementation Decisions

### Thematic split (output structure)
- **D-01:** Produce **3 thematic documents**, grouped by system layer that maps to likely future implementation phases:
  1. `01-architecture-and-physics-foundations.md` — Network architecture (SIREN init, omega0 scheduling, LayerNorm), input vector design (14-D), characteristic length D, softening dual-context, COM frame, AD chain-rule factor
  2. `02-data-pipeline-and-validation.md` — IC parsing, file format (h5 vs txt/json), non-contiguous IDs, blacklist enforcement, snapshot-completeness gates, validation metrics (SCS / SASD / IPR / PSC), Brutus footer/mass drift handling
  3. `03-curriculum-and-training-loop.md` — Data-driven stage assignment (PCA / K-means / quantiles), replay-and-lookahead batch construction, collocation vs data-fidelity points, ALM scheduling (μ, λ, energy weight), gradient clipping, causal vs global sampling, stage transition criteria
- **D-02:** Numbered filename prefix (`01-`, `02-`, `03-`) for ordering. All output is `.md` (the 4 currently `.txt` files convert to Markdown during synthesis).

### Merge style
- **D-03:** **Synthesized rewrite** — write fresh thematic docs that re-state findings clearly, deduplicate cross-source repetition, and cross-link between the 3 new docs. Verbatim concatenation rejected. The 2026-04-27 audit's structure (Executive Summary → Critical Issues → Inconsistencies → Ambiguities → Corrected Specs → Implementation Checklist) is the structural spine for each new doc, scaled down to its theme.
- **D-04:** Each thematic doc must have a consistent skeleton: Executive Summary, Confirmed Findings (with severity), Open Decisions (`[DECISION-NEEDED]` callouts), Recommended Resolutions, References to the other 2 thematic docs where topics overlap.

### Conflict-resolution policy
- **D-05:** When two source files give contradictory recommendations on the same topic, **pick the position with the stronger physical/mathematical justification and document the reasoning inline** in the consolidated doc. The losing position is not silently dropped — record it under "Considered Alternatives" so a future reader can re-open the question. Two known live conflicts that must be addressed by name in the new docs:
  - **Input vector orientation encoding:** the 2026-04-27 audit (B-04, §5.3) recommends 5 trig values `[sin(theta_L), cos(theta_L), sin(phi_L), cos(phi_L), sin(gamma_orb)]`; `Causal_Trainingmismatch_resolution_blueprint.md` argues trig encodings are physically flawed (gimbal lock during chaotic scattering) and proposes 3 shape invariants `(I_1, I_2, I_3)` plus 2 direction cosines `(cos θ, sin θ)` of the invariant plane normal. Both produce 14-D total but with different IC composition. → Document both, pick winner by physical/ML soundness, and explicitly flag for verification.
  - **Frame for `s_min` in collision criterion:** unsoftened raw separation vs `max(s_min, epsilon)` — see audit D8.

### `next steps.txt` (128 KB, oldest, mostly superseded)
- **D-06:** **Cherry-pick unique content only.** The 2026-04-27 audit subsumes ~80 % of `next steps.txt`. Pull only content that is NOT in the audit:
  - The "5 Orders of Magnitude Difference" softening analysis (unique deep dive)
  - "Issue 17: Global scale computation implementation" (`compute_globals` over all ICs — unique pseudo-code)
  - "Issue 19: Normalization formulas verification" comprehensive table
  - "Issue 1: Lyapunov time τ_L and L_max formula resolution" (the verified+resolving section)
  Verify each candidate is genuinely absent from the audit before extracting; if present in audit, archive only.

### Disposition of originals
- **D-07:** Move all 7 originals to `pinn_instruction/original_latex/review-of-framework/issues/archive/` using `git mv` (preserves history). No deprecation header injection — the archive folder name and `MIGRATION.md` carry that signal.
- **D-08:** **Output location:** new thematic docs live at `pinn_instruction/original_latex/review-of-framework/issues/` (the same directory the originals came from). New layout after consolidation:
  ```
  issues/
    archive/                                       # all 7 originals, untouched
    01-architecture-and-physics-foundations.md     # NEW
    02-data-pipeline-and-validation.md             # NEW
    03-curriculum-and-training-loop.md             # NEW
    MIGRATION.md                                   # NEW
    README.md                                      # NEW (index/navigation)
  ```

### Migration manifest
- **D-09:** `MIGRATION.md` is a **per-file, per-section provenance map**. For each of the 7 originals it must list every major section heading and which new doc(s) absorbed each section, plus a "Unique findings preserved" checklist confirming nothing is lost. Format:
  ```
  ## next steps.txt (archived)
  | Original section | Destination doc(s) | Notes |
  |---|---|---|
  | Issue 1: Lyapunov τ_L / L_max | 03-curriculum-and-training-loop.md §Stage assignment | Resolved subsection extracted |
  | 5 Orders of Magnitude Difference | 01-architecture-and-physics-foundations.md §Softening | Unique to this file |
  | Issue 6: Batch construction | (covered by audit) | Not extracted; archived only |
  ...
  ```
- **D-10:** `MIGRATION.md` lives next to the 3 new docs (i.e., at `issues/MIGRATION.md`), not inside `archive/`. Archive folder gets only the 7 raw original files, no metadata files.

### `issues/README.md`
- **D-11:** Add a short README at `issues/README.md` (≤ 50 lines) that:
  1. States the consolidation date and rationale
  2. Lists the 3 thematic docs with one-sentence descriptions
  3. Points at `MIGRATION.md` for provenance and `archive/` for originals
  4. Links to the canonical refs (CTL doc, PINN doc, dataset README) so future agents land here first
  This is the navigation anchor; downstream agents read it before opening individual thematic docs.

### Substantive open decisions to surface in the consolidated docs
- **D-12:** The following items remain unresolved across the source set and **must be flagged with `[DECISION-NEEDED]` callouts** in the relevant thematic doc, not silently merged:
  1. **Input vector composition (14-D content):** trig encoding vs shape invariants + direction cosines (see D-05). → `01-architecture-and-physics-foundations.md`
  2. **File format for processed data:** keep `h5` or migrate to `txt/json`? → `02-data-pipeline-and-validation.md`
  3. **Causal training mode:** Option A (per-time-step causal weighting, validation-PDF style) vs Option B (global sampling + ALM, CTL-doc style). → `03-curriculum-and-training-loop.md`
  4. **`I_norm` definition:** text formula `tr(I) / (M r_char^2)` vs code listing `tanh(...)`. → `01-architecture-and-physics-foundations.md`

### Claude's Discretion
- Exact section headings within each thematic doc (use audit subsections as a guide)
- Severity-classification scheme (recommend reusing audit's BLOCKER / MAJOR / MINOR labels for cross-doc consistency)
- Whether to include a top-level "Cross-doc Interaction Matrix" similar to audit §8 (recommend: yes, in `README.md`)
- Format choices for tables, callouts, and code snippets within new docs
- How to phrase the `[DECISION-NEEDED]` callouts (markdown blockquotes vs admonition syntax — pick whatever renders cleanest in plain Markdown)
- Whether to copy the audit's full corrected-spec sections verbatim or summarize and link (recommend: copy verbatim into `01-architecture-and-physics-foundations.md` because they are reference specs that downstream implementation phases will quote — preserving exact text avoids transcription bugs)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### The 7 source files being consolidated (read all 7 before drafting any of the 3 new docs)
- `pinn_instruction/original_latex/review-of-framework/issues/three_body_pinn_pre-implementation_audit_2026-04-27.md` — Comprehensive audit (38 KB); structural spine for the 3 new docs. Sections: Executive Summary, §1 Critical Issues B-01..B-11, §2 Major Inconsistencies M1..M16, §3 Design Ambiguities D1..D10, §4 Author-Flagged Uncertainties (28 items), §5 Corrected 14-D Input Vector Spec, §6 Unified Batch Construction, §7 Implementation Checklist P0..P4, §8 Cross-Issue Interaction Matrix, §9 Quantitative Impact Summary
- `pinn_instruction/original_latex/review-of-framework/issues/Causal_Trainingmismatch_resolution_blueprint.md` — Architecture+training reconciliation (48 KB). Key contributions: Time-Windowed Causal-ALM Hybrid; shape-invariants-vs-trig argument; SCS/SASD/IPR/PSC redesign as live training parameters; Synthesized Curriculum Training Protocol
- `pinn_instruction/original_latex/review-of-framework/issues/Issue_on_data_validation_protocol_and_compatbility_with_project_context.md` — Pre-agent validation gap analysis (8 KB). Surfaces the causal-training Option-A-vs-B decision
- `pinn_instruction/original_latex/review-of-framework/issues/review.md` — Scaling-contract review (6 KB). Unique finding: AD chain-rule factor missing → physics residual off by 4×, kinetic energy off by 4×
- `pinn_instruction/original_latex/review-of-framework/issues/stage-assignment-issue.txt` — Curriculum-stratification methodology (10 KB). Data-driven adaptive stage assignment via PCA + K-means + quantiles
- `pinn_instruction/original_latex/review-of-framework/issues/next-step-for-data-processing-pipeline.txt` — Mixed pipeline asks (6 KB). h5→txt/json question; I_norm text-vs-code inconsistency; 12 author-flagged comment line items in CTL
- `pinn_instruction/original_latex/review-of-framework/issues/next steps.txt` — Oldest dump (128 KB, mostly superseded). Cherry-pick per D-06: 5-OoM softening, global-scale computation, normalization verification, Issue 1 resolution

### Project planning (already-decided context)
- `.planning/PROJECT.md` — Milestone v1.2 goal (PINN Implementation Readiness); core value (data integrity); deferred requirements that explain why this consolidation matters
- `.planning/ROADMAP.md` §"Phase 9: Issues Directory Consolidation" — phase goal, 4 success criteria, requirements CONSOL-01..CONSOL-03
- `.planning/REQUIREMENTS.md` — currently lists v1.1 requirements only; downstream planner should note that v1.2 requirements (CONSOL-01..CONSOL-03) are referenced in ROADMAP.md but not yet expanded into REQUIREMENTS.md (this is a planning-phase concern, not a context-phase one)

### Project methodology (referenced by every source file; downstream agents need these to evaluate findings)
- `pinn_instruction/markdown_conversions/CTL-instruction-final.md` — Curriculum-Training-Labeled framework (the document being audited)
- `pinn_instruction/markdown_conversions/PINN_architecture_plan.md` — SQR-SkipResNet-SIREN architecture (the other document being audited)
- `pinn_instruction/markdown_conversions/sampling_method_instruction.md` — IC sampling methodology
- `simulation_data/Documentation/README.md` — Dataset spec, anomalies, dt_out per variant, completeness rules
- `pinn/data-processing-pipeline-full.py` — Source of truth for current 13-component IC vector and staging logic (audit findings reference this)
- `pinn/basic_architecture.py` — Current SIREN+SkipResNet implementation (audit findings reference this)

### Phase pattern reference (for documentation style)
- `.planning/phases/05-content-completeness-verification/05-CONTEXT.md` — example of prior CONTEXT.md style in this project
- `.planning/phases/08-compilability-verification/08-CONTEXT.md` — most recent prior phase context

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **Source files**: Markdown formatting in audit and Causal_Trainingmismatch is consistent (tables, code fences, `## H2` headers). Reuse those conventions verbatim in the 3 new docs.
- **Audit's Section 5 (Corrected Input Vector Specification)** and **Section 6 (Unified Batch Construction)** are reference-quality and should be copied verbatim into `01-...` and `03-...` respectively (per Claude's discretion note above) — they are formal specs that future implementation will quote.

### Established Patterns (from this project)
- Documentation lives near the artifacts it describes (CTL doc next to CTL LaTeX, audit findings next to the framework being audited)
- Phases that touch documentation use plain Markdown with no extra tooling (no MkDocs, no Sphinx, no MDX) — keep this consolidation in plain Markdown
- Multi-file consolidations (Phase 1, Phase 2) used `git mv` to preserve history; do the same here for the 7 originals → archive/

### Integration Points
- The 3 new docs are leaf artifacts (read by humans + future agents, not imported by code) — no Python/C++ integration concerns
- `simulation_data/Documentation/README.md` is the existing dataset doc that some audit findings reference. The new `02-data-pipeline-and-validation.md` should cross-link to it but not duplicate it
- The 3 new docs are read by future planning phases (data pipeline implementation, architecture implementation, training loop implementation) — they are inputs to those phases, not implementations themselves

### Existing artifacts already in target directory
- The `issues/` folder currently contains only the 7 files. No README, no archive, no migration manifest. Empty slate apart from the 7 files.

</code_context>

<specifics>
## Specific Ideas

- **The `Causal_Trainingmismatch` recommendation conflicts with the 2026-04-27 audit on input vector orientation encoding.** This is the most consequential live disagreement across the 7 sources. Per D-05 it must be resolved by physical/mathematical reasoning and the losing position recorded under "Considered Alternatives" — not silently dropped. Recommended verdict: shape invariants + direction cosines (Causal_Trainingmismatch position) is more defensible because (a) trig representations have known gimbal-lock pathologies during the exact chaotic-scattering events the curriculum's late stages target, (b) shape invariants are universally rotation-invariant and continuous, (c) direction cosines provide global orientation without singularity. The audit's trig argument is well-reasoned but applies a pattern from less-chaotic regimes. Documenting both positions and the verdict satisfies D-05 and surfaces the decision for future review.

- **Severity hygiene:** the audit uses "BLOCKING / MAJOR / MINOR / INFO". Reuse exactly those four labels across all 3 new docs so cross-doc references resolve unambiguously.

- **Format consistency target:** each new thematic doc should be readable standalone (someone opening just `02-data-pipeline-and-validation.md` should not need to flip back to `01-...` to follow it) but cross-link liberally where topics genuinely overlap (e.g., COM frame is touched by all 3 docs but lives canonically in `01-...`).

- **Length budget:** the 3 new docs combined should be **smaller** than the 7 originals combined (sources total ~245 KB; target ~80–120 KB through deduplication and synthesis). If the new docs end up ≥ 80 % of the source size, the rewrite isn't actually rewriting — it's pasting.

</specifics>

<deferred>
## Deferred Ideas

These came up during analysis but belong to **future implementation phases**, not this consolidation:

- **Actually fixing the audit's findings.** Phase 9 produces the consolidated documentation only. Implementation of B-01 (SIREN init), B-02 (D = 6.694), B-05 (unified COM transformer), B-09 (epsilon = 1e-8), B-11 (TrajectoryIndex), and the entire Phase 0–4 implementation checklist from the audit are scope for future phases (likely v1.2 phases 10+).
- **Updating the LaTeX source documents** (`CTL-instruction-final.tex`, `PINN_architecture_plan.tex`) to reflect the consolidated findings. Future LaTeX-modification phase.
- **Resolving the 12 author-flagged `\authcomment` items** in `next-step-for-data-processing-pipeline.txt`. These are individual LaTeX comments that need answers — they belong in the LaTeX-revision phase, not consolidation.
- **File format conversion** of processed data from h5 → txt/json (the request inside `next-step-for-data-processing-pipeline.txt`). This is an implementation decision for the data-pipeline phase; we surface it as `[DECISION-NEEDED]` in `02-...` but do not make the decision here.
- **Re-running stage assignment for all ~15 K trajectories** with corrected D and epsilon (audit P4-1). Future data-pipeline phase.
- **Updating `.planning/REQUIREMENTS.md`** to expand v1.2 requirements CONSOL-01..CONSOL-03. This is a planning-phase concern, not a context-phase concern; flag it for the planner.
- **Adding a top-level dashboard / kanban view** of all open decisions across the 3 docs. Could be useful but adds scope; keep `[DECISION-NEEDED]` callouts inline for now.

### Reviewed Todos (not folded)
None — no project todos matched this phase's scope.

</deferred>

---

*Phase: 09-issues-directory-consolidation*
*Context gathered: 2026-04-27*
