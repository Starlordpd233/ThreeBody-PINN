# Phase 22: Framework-Spec Cleanup - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-08
**Phase:** 22-Framework-Spec Cleanup
**Areas discussed:** Math Normalization Style, Author Comments Disposition, Render Verification Method

---

## Math Normalization Style

| Option | Description | Selected |
|--------|-------------|----------|
| Strict Uniformity | Enforce strict, uniform usage (e.g., all block math must use `$$`, standard matrix environments) everywhere. | |
| Minimal Repair Only | Normalize only what breaks the markdown rendering; preserve the author's original style otherwise. | ✓ |

**User's choice:** Normalize all intended math into valid KaTeX math contexts where rendering is currently broken. Use single-dollar delimiters for inline math and double-dollar delimiters for block math. Preserve already-correct notation, environments, spacing, and layout. Do not perform cosmetic repository-wide restyling. Equivalence-check each conversion and surface ambiguous cases under the STOP protocol.
**Notes:** User chose a targeted minimal repair approach with strict rules for delimiters (`$` and `$$`) and explicit instructions against cosmetic restyling. Ambiguity must trigger the STOP protocol.

---

## Author Comments Disposition

| Option | Description | Selected |
|--------|-------------|----------|
| Rewrite to Prose | Remove if resolved, otherwise rewrite as clean descriptive prose. | |
| Extract and Remove | Extract all to a separate disposition log and remove from specs. | |
| Elevate to Warnings | Keep them as explicit project warnings/TODOs if unresolved. | |

**User's choice:** Preserve and defer all 28 authcomment items. Keep every comment's substantive text in place; do not delete, extract, resolve, rewrite as ordinary prose, or reclassify all comments as warnings or TODOs during Phase 22. If an authcomment wrapper itself prevents correct Markdown rendering, convert only the wrapper mechanically into a render-safe author-comment format while preserving the comment text, meaning, and location. Do not assess or alter the substance of the comment.
**Notes:** Explicitly recorded as a user-directed scope decision. The phase is no longer responsible for adjudicating comments. A future-phase handoff must be created instead. The option presented in conversational prompting were all rejected in favor of full deferral.

---

## Render Verification Method

| Option | Description | Selected |
|--------|-------------|----------|
| Manual Visual Check | Use a local markdown viewer to manually confirm all edited equations and comments render properly. | |
| Automated Script | Write an automated script (e.g., using remark or regex) to scan for unbalanced delimiters or broken tags. | |

**User's choice:** Do not select Option 1 or Option 2 alone. Use both automated validation and manual visual review. Automated validation: Create and commit a Node-based detector using markdown-it, @vscode/markdown-it-katex, and katex... Manual visual review: Open all three complete framework specs in the actual Cursor or VS Code Markdown Preview and inspect the full rendered documents...
**Notes:** The user mandated a dual approach. The automated script has strict library requirements (`markdown-it`, `@vscode/markdown-it-katex`, `katex`) to match Cursor/VS Code preview engine.

---

## Claude's Discretion

None.

## Deferred Ideas

Adjudication of the 28 `\authcomment` tags is deferred to a future phase.