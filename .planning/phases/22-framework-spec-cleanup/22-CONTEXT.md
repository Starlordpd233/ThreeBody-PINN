---
phase: 22
slug: framework-spec-cleanup
status: Ready for planning
created: 2026-06-08
governance: "v1.4 STOP protocol, no semantic changes, presentation preservation only"
---

# Phase 22: Framework-Spec Cleanup - Context

**Gathered:** 2026-06-08
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 22 is the final presentation-preserving framework-spec cleanup. It normalizes math rendering and dispositions author comments under human adjudication without autonomous semantic changes or deletions.

</domain>

<decisions>
## Implementation Decisions

### Math Normalization Style
- **D-01:** Normalize all intended math into valid KaTeX math contexts where rendering is currently broken. Use single-dollar (`$`) delimiters for inline math and double-dollar (`$$`) delimiters for block math.
- **D-02:** Preserve already-correct notation, environments, spacing, and layout. Do not perform cosmetic repository-wide restyling.
- **D-03:** Equivalence-check each conversion and surface ambiguous cases under the STOP protocol.

### Author Comments Disposition
- **D-04:** Preserve and defer all 28 `\authcomment` items. Keep every comment's substantive text in place; do not delete, extract, resolve, rewrite as ordinary prose, or reclassify all comments as warnings or TODOs during Phase 22.
- **D-05:** If an `\authcomment` wrapper itself prevents correct Markdown rendering, convert only the wrapper mechanically into a render-safe author-comment format while preserving the comment text, meaning, and location. Do not assess or alter the substance of the comment.
- **D-06:** Verify that all 28 comments remain present and that none were lost or semantically changed. Create an explicit future-phase or backlog handoff for reviewing and adjudicating the comments individually. (This was a user-directed scope decision removing individual author-comment adjudication from Phase 22's required work).

### Render Verification Method
- **D-07:** Use both automated validation and manual visual review. Do not rely on only one method.
- **D-08:** Automated validation: Create and commit a Node-based detector using `markdown-it`, `@vscode/markdown-it-katex`, and `katex`. The detector must match the KaTeX engine used by the Cursor or VS Code Markdown Preview. It must report parse errors (throwOnError), strict-mode warnings, detect unbalanced delimiters, raw LaTeX, math-like backtick fragments, and broken Markdown structures. It must pass known author-flagged regression fixtures and keep a known-clean negative control free of findings. It must finish with zero unresolved rendering findings across `ctl_instruction.md`, `pinn_architecture.md`, and `sampling_method.md`, and verify all 28 comments remain present.
- **D-09:** Manual visual review: Open all three complete framework specs in the actual Cursor or VS Code Markdown Preview and inspect the full rendered documents. Check every edited equation and its surroundings. Confirm no raw LaTeX, clipped math, broken layouts, accidental code formatting, or missing content.
- **D-10:** Record the exact detector command and output plus a per-file visual-review checklist. Render correctness is established only when both automated detector and manual review pass.

### Claude's Discretion
None — all presentation and verification decisions strictly defined.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase Scope and Requirements
- `.planning/ROADMAP.md` — Phase 22 goal and success criteria (final presentation-preserving framework-spec cleanup).
- `docs/superpowers/specs/2026-06-07-framework-spec-cleanup-design.md` — Phase 22 design approval (referenced in PROJECT.md).

### Active Framework Specs
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- The Node-based automated detector (D-08) is a new asset that will be created during this phase.

### Established Patterns
- **STOP Protocol** — Surface ambiguous cases during math equivalence-checking rather than assuming intent.
- **Strict presentation preservation** — No semantic changes. Framework specs are documentation, so edits focus on valid KaTeX/Markdown interoperability.

### Integration Points
- **Automated Detector Integration** — Will run against the three active framework specs in `pinn_instruction/markdown_conversion/framework-specs/`.

</code_context>

<specifics>
## Specific Ideas

- The automated detector must use `markdown-it`, `@vscode/markdown-it-katex`, and `katex` to ensure parity with Cursor/VS Code.
- A future-phase or backlog handoff document must be created to track the 28 deferred author comments.

</specifics>

<deferred>
## Deferred Ideas

- **Adjudication of `\authcomment` items** — Individual review and resolution of the 28 author comments is explicitly deferred to a future phase or backlog item. Phase 22 only mechanically repairs their wrappers if they break Markdown rendering.

</deferred>

---

*Phase: 22-Framework-Spec Cleanup*
*Context gathered: 2026-06-08*