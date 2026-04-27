---
phase: 9
reviewers: [claude-self-review]
reviewed_at: "2026-04-27T02:00:00.000Z"
plans_reviewed:
  - 09-01-PLAN.md
  - 09-02-PLAN.md
  - 09-03-PLAN.md
---

# Cross-AI Plan Review -- Phase 9

> **Note:** Codex CLI binary was not installed on this system (shell function wrapper present but underlying binary missing). Gemini CLI was unavailable due to Keychain access restrictions in the CLI context. This review was performed by Claude as a structured self-review applying adversarial analysis to the plans.

## Claude Review

### Summary

Phase 9's three plans provide a well-structured, thoroughly researched approach to consolidating 7 scattered issue/audit files into 3 thematic documents. The context gathering (CONTEXT.md, RESEARCH.md) is exceptional in depth, with explicit decisions (D-01 through D-12), a complete content inventory, cross-link dependency mapping, and a 7-point verification strategy. The plans decompose the work into sensible waves with clear dependency ordering. The main risks are metadata accuracy issues and a DECISION-NEEDED count discrepancy that should be resolved before execution.

### Strengths

- **Exceptional context preparation**: CONTEXT.md and RESEARCH.md together provide one of the most thorough planning artifacts in this project's history. The content inventory with per-file unique contributions, thematic mapping, and overlap/deduplication analysis means an executor has everything needed to perform the synthesis correctly.
- **Well-chosen thematic split (D-01)**: The 3-way split (architecture/physics, data pipeline, curriculum/training) maps cleanly to likely future implementation phases and avoids the temptation to combine distinct concerns.
- **Synthesized rewrite mandate (D-03)**: Requiring fresh prose rather than verbatim concatenation is the correct approach. The size budget (80-120 KB target vs 246 KB source) provides a quantitative check that real deduplication occurred.
- **Conflict resolution policy (D-05)**: Explicitly requiring both positions to be documented with physical/mathematical justification for the winner is mature. Recording the loser under "Considered Alternatives" preserves the audit trail.
- **Cherry-pick strategy for next steps.txt (D-06)**: The explicit 4-item checklist prevents the common mistake of either ignoring or over-including the 128 KB dump.
- **Per-section provenance tracking (D-09)**: MIGRATION.md as a per-file, per-section map makes it possible to verify completeness after consolidation.
- **Verification strategy is comprehensive**: The 7-check approach in RESEARCH.md (completeness, unique findings, conflict resolution, size, archive, no-duplicate, decision callouts) covers the key risks.
- **Threat model correctly scoped**: All 3 plans correctly identify that documentation-only work has no runtime trust boundaries.
- **Parallel wave design**: Plans 01 and 02 can run concurrently since they produce independent files, and Plan 03 correctly depends on both.

### Concerns

- **[MEDIUM] DECISION-NEEDED count discrepancy**: D-12 specifies 4 unresolved decisions, but the plans produce 5 callouts: Plan 01 has 2 in doc 01 + 1 in doc 02, Plan 02 has 2 in doc 03. The 5th item (frame for s_min in collision criterion, in Plan 02) is a valid conflict per D-05 but was not counted in D-12. The VALIDATION.md checklist item 4 still says "All 4 [DECISION-NEEDED] items from D-12 appear" which will fail if 5 exist. Either D-12 should be updated to 5 items, or VALIDATION.md should say "at least 4." This affects traceability.

- **[MEDIUM] Plan 01 files_modified metadata includes 03-curriculum-and-training-loop.md**: Plan 01's YAML frontmatter lists this file under `files_modified`, but it is created exclusively by Plan 02. This metadata inaccuracy could confuse execution tracking tools or cause false conflict detection.

- **[MEDIUM] Normalization formulas table has ambiguous ownership**: RESEARCH.md maps "Normalization formulas verification table" (from next steps.txt Issue 19) to both `01-architecture-and-physics-foundations.md` AND `02-data-pipeline-and-validation.md`. Having the same table in two docs violates CONSOL-03 (each doc has clear, distinct purpose with no overlapping coverage). One doc should own it and the other should cross-link.

- **[LOW] Parallel wave has implicit dependency**: Plan 02's `read_first` references `archive/` paths, meaning it expects files to already be archived. But archival happens in Plan 01 Task 1. If both plans start simultaneously, Plan 02 may fail to find source files. The `depends_on: []` metadata for Plan 02 is technically correct (no plan-level dependency) but Task 1 of Plan 01 must complete first.

- **[LOW] Verbatim copy boundaries underspecified**: Both Plans 01 and 02 call for verbatim copying of audit sections (Section 5 and Section 6 respectively), but neither defines exact start/end markers. The executor must identify section boundaries by heading text, which is straightforward but could lead to including too much or too little.

- **[LOW] Size targets may be tight**: The verbatim copies of audit Sections 5 and 6 could consume 10-16 KB of the 80-120 KB budget before any synthesized content is added. The executor should monitor cumulative size and adjust synthesis depth if the budget is at risk.

- **[LOW] s_min conflict resolution reasoning not pre-specified**: CONTEXT.md provides detailed reasoning for the input vector conflict resolution (shape invariants win, with 3 specific arguments), but the s_min conflict (unsoftened raw separation vs max(s_min, epsilon)) has no pre-determined resolution rationale. The executor must develop this reasoning independently, increasing execution risk.

- **[LOW] Verification commands use relative paths**: Commands like `wc -c issues/01-*.md` assume execution from a specific directory. Should specify "from repo root" explicitly or use absolute paths.

### Suggestions

- Update D-12 to include the s_min frame decision as a 5th item, and update VALIDATION.md accordingly. This keeps the decision tracking consistent.
- Remove `03-curriculum-and-training-loop.md` from Plan 01's `files_modified` list. It belongs only in Plan 02's metadata.
- Assign the normalization formulas table to a single canonical owner (recommend `01-architecture-and-physics-foundations.md` since normalization is an architecture concern) and have `02-data-pipeline-and-validation.md` cross-link to it.
- Add a note to Plan 02 that it must wait for Plan 01 Task 1 to complete before starting, or change Plan 02's `depends_on` to `[09-01]` with a note that only Task 1 is the actual dependency.
- Add explicit start/end markers for verbatim copy sections (e.g., "Copy from `## 5. Corrected 14-D Input Vector Specification` through the line before `## 6.`").
- Pre-specify the s_min resolution rationale in CONTEXT.md or RESEARCH.md to reduce executor judgment risk.

### Risk Assessment

**Overall risk: LOW-MEDIUM**

This is a documentation-only phase with no code changes, no runtime dependencies, and no security surface. The plans are among the most thoroughly prepared in this project's history. The MEDIUM concerns (metadata accuracy, decision count, content ownership) are traceability issues that could cause confusion but won't break execution. The LOW concerns are edge cases a competent executor would handle naturally.

The primary execution risk is content loss during synthesis -- that a unique finding from one of the 7 sources gets dropped. This is mitigated by:
1. The detailed content inventory in RESEARCH.md
2. The MIGRATION.md provenance tracking
3. The 7-check verification strategy
4. The cherry-pick checklist for next steps.txt (D-06)

---

## Consensus Summary

(Single-reviewer session -- consensus is this review's findings.)

### Agreed Strengths

- Context preparation (CONTEXT.md + RESEARCH.md) is exceptional in depth and specificity
- The synthesized-rewrite approach with size budget prevents the common failure mode of verbatim concatenation
- Conflict resolution policy (D-05) with "Considered Alternatives" is mature and preserves audit trail
- Per-section provenance tracking (MIGRATION.md) enables post-hoc completeness verification
- Thematic 3-way split maps cleanly to future implementation phases

### Agreed Concerns

- DECISION-NEEDED count discrepancy (5 in plans vs 4 in D-12) affects validation checklist
- Plan 01 metadata claims ownership of file created by Plan 02
- Normalization formulas table ownership is ambiguous across docs 01 and 02

### Divergent Views

(Single reviewer -- no divergent views to report.)

---

*Review conducted: 2026-04-27*
*Reviewer: Claude (self-review, adversarial mode)*
*External CLIs unavailable: Codex (binary not installed), Gemini (Keychain access restricted)*
