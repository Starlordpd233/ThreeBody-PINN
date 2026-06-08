# Docs Reorganization Move Proposal

> Generated: 2026-06-07
> Depends on: `2026-06-07-docs-reorganization-inventory.md`
> Scope: within-`docs/` moves only. No deletions. Separate deletion proposals follow in `2026-06-07-docs-reorganization-deletion-proposals.md`.

## Proposed Moves

### Runbooks

| Current path | Proposed path | Reference updates | Reason |
| --- | --- | --- | --- |
| `docs/migration/exact-state-mac-migration.md` | `docs/runbooks/migration/exact-state-mac-migration.md` | `README.md:9` — update link target and display path. `AGENTS.md:12` — update backtick path. | Migration runbook; target structure places runbooks in `docs/runbooks/`. |
| `docs/migrating_to_macbookPro.txt` | `docs/runbooks/migration/migrating-to-macbook-pro.txt` | none (no external references) | Older plain-text migration notes; same topic; rename to URL/slug-safe form. |

### Work Plans — milestone_v1.4

| Current path | Proposed path | Reference updates | Reason |
| --- | --- | --- | --- |
| `docs/plans/2026-06-06-phase-20-5-plan-remediation-implementation-plan.md` | `docs/work/plans/milestone_v1.4/20.5-plan-remediation/2026-06-06-phase-20-5-plan-remediation-implementation-plan.md` | none external (internal references are historical audit-trail citations to `docs/findings/` which are intentionally left as-is) | Phase 20.5 plan. |
| `docs/plans/ADOPT_EDL_19_01_UPDATED_PLAN.md` | `docs/work/plans/milestone_v1.4/19-edl-adoption/ado-edl-19-01-updated-execution-plan.md` | none external | EDL-19-01 adoption plan. |
| `docs/plans/Phase 20.5 GSD Workflow Repair Implementation Plan.md` | `docs/work/plans/milestone_v1.4/20.5-gsd-workflow-repair/phase-20.5-gsd-workflow-repair-implementation-plan.md` | none external (self-references via absolute path are historical; see inventory notes) | Phase 20.5 plan; slugify filename. |
| `docs/superpowers/plans/2026-06-05-phase20-review-remediation.md` | `docs/work/plans/milestone_v1.4/20-review-remediation/2026-06-05-phase20-review-remediation.md` | none external | Phase 20 plan. |
| `docs/superpowers/plans/2026-06-06-phase20-completion-state-reverification.md` | `docs/work/plans/milestone_v1.4/20-completion-reverification/2026-06-06-phase20-completion-state-reverification.md` | none external | Phase 20 plan. |

### Work Plans — cross_cutting

| Current path | Proposed path | Reference updates | Reason |
| --- | --- | --- | --- |
| `docs/superpowers/plans/2026-06-05-enforce-git-guideline.md` | `docs/work/plans/cross_cutting/git-guidelines/2026-06-05-enforce-git-guideline.md` | none external | Cross-cutting (not phase-specific). |
| `docs/user_plans/plans/2026-03-19-remove-qwen-model-and-mlx.md` | `docs/work/plans/cross_cutting/cleanup/2026-03-19-remove-qwen-model-and-mlx.md` | none external | Cross-cutting cleanup plan. |

### Work Reviews — milestone_v1.4

| Current path | Proposed path | Reference updates | Reason |
| --- | --- | --- | --- |
| `docs/superpowers/reviews/reviewing_20260605-phase-20-review-remediation-plan.md` | `docs/work/reviews/milestone_v1.4/20-review-remediation/2026-06-05-phase-20-review-remediation-review.md` | none external | Phase 20 review. |
| `docs/findings/milestone_v1.4/phase20-completion-reverification-2026-06-06.md` | `docs/work/reviews/milestone_v1.4/20-completion-reverification/phase20-completion-reverification-2026-06-06.md` | none external | Phase 20 reverification report. |
| `docs/findings/milestone_v1.4/reviewing_19_context.md` | `docs/work/reviews/milestone_v1.4/19-context-verification/reviewing-19-context.md` | `.planning/phases/19-physics-and-loss-contracts/19-GAPS.md:26` references a different file in the same legacy dir (`reviewing_phase19_plans/2026-05-22-phase19-plan-repair-meta-plan.md`) — that file does not exist in the current tree and is not part of this move. No update needed for this specific move. | Phase 19 verification report. |
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/review1.md` | `docs/work/reviews/milestone_v1.4/20.5-plan-audit/2026-06-06-phase-20.5-audit-review1.md` | none external | Phase 20.5 audit. |
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/review2.md` | `docs/work/reviews/milestone_v1.4/20.5-plan-audit/2026-06-06-phase-20.5-audit-review2.md` | none external | Phase 20.5 audit. |
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/review3.md` | `docs/work/reviews/milestone_v1.4/20.5-plan-audit/2026-06-06-phase-20.5-audit-review3.md` | none external | Phase 20.5 adversarial audit. |
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/review4.md` | `docs/work/reviews/milestone_v1.4/20.5-plan-audit/2026-06-06-phase-20.5-audit-review4.md` | none external | Phase 20.5 audit. |

### Work Reviews — cross_cutting

| Current path | Proposed path | Reference updates | Reason |
| --- | --- | --- | --- |
| `docs/superpowers/specs/2026-05-24-latex-sync-strategy-consolidated-review.md` | `docs/work/reviews/cross_cutting/latex-sync/2026-05-24-latex-sync-strategy-consolidated-review.md` | `docs/superpowers/specs/2026-05-24-latex-markdown-sync-strategy-design.md:306` references this file by legacy path. That design doc is itself moving in this batch; the reference should be updated to the new review path in the same commit. | Review of a design (not a design itself). |

### Work Designs — milestone_v1.4

| Current path | Proposed path | Reference updates | Reason |
| --- | --- | --- | --- |
| `docs/superpowers/specs/2026-06-04-phase20-review-framework-design.md` | `docs/work/designs/milestone_v1.4/20-review-framework/2026-06-04-phase20-review-framework-design.md` | none external | Phase 20 design. |
| `docs/superpowers/specs/2026-06-07-framework-spec-cleanup-design.md` | `docs/work/designs/milestone_v1.4/framework-spec-cleanup/2026-06-07-framework-spec-cleanup-design.md` | `.planning/PROJECT.md:165` references this path. Update to new path in same commit. | v1.4-adjacent design. |

### Work Designs — cross_cutting

| Current path | Proposed path | Reference updates | Reason |
| --- | --- | --- | --- |
| `docs/superpowers/specs/2026-05-24-latex-markdown-sync-strategy-design.md` | `docs/work/designs/cross_cutting/latex-sync/2026-05-24-latex-markdown-sync-strategy-design.md` | internal reference to `2026-05-24-latex-sync-strategy-consolidated-review.md` at line 306 will be updated when the review moves (both in this batch). | Cross-cutting design. |
| `docs/user_plans/design_git_guideline/2026-06-05-git-commit-convention-design.md` | `docs/work/designs/cross_cutting/git-guidelines/2026-06-05-git-commit-convention-design.md` | none external (joins existing `docs/work/designs/cross_cutting/git-guidelines/` directory) | Design that produced `docs/git-guidelines.md`. |
| `docs/user_plans/design_git_guideline/design_idea_1.md` | `docs/work/designs/cross_cutting/git-guidelines/design-idea-1.md` | none external | Early design idea. |

### Work Reviews — cross_cutting (git guidelines)

| Current path | Proposed path | Reference updates | Reason |
| --- | --- | --- | --- |
| `docs/user_plans/design_git_guideline/final_git_guideline_review.md` | `docs/work/reviews/cross_cutting/git-guidelines/final-git-guideline-review.md` | none external (references to `docs/git-guidelines.md` remain valid — that file stays) | Review of git guidelines design. |

### Already in target structure (no move)

| Current path | Action | Reason |
| --- | --- | --- |
| `docs/work/designs/cross_cutting/git-guidelines/2026-06-07-docs-lifecycle-git-behavior-design.md` | retain | Already follows target structure. |
| `docs/README.md` | retain | Root guidelines. |
| `docs/git-guidelines.md` | retain | Referenced widely; governed by separate scope constraint. |

## Blocked Moves

| Current path | Blocker | Required decision |
| --- | --- | --- |
| `docs/user_plans/splitting_latex.md` | Content and purpose not classified without reading. Title "Proposed File Structure" is ambiguous — could be LaTeX framework split (historical, possibly archive-worthy) or early docs-layout proposal (possibly consumed by `docs/README.md`). | User to classify: move to `docs/work/designs/`, `docs/archive/`, or delete? |
| `docs/user_plans/verifying_review_documents_conversion.md` | Purpose unknown without reading; title is empty-string in inventory. | User to classify: move to `docs/work/reviews/`, `docs/archive/`, or delete? |
| `docs/superpowers/plans/` directory (after all files move out) | Cannot remove directory until every file inside is moved. | Auto-resolves when all contained files are moved; remove empty dir as final step. |
| `docs/plans/`, `docs/findings/`, `docs/user_plans/` directories (after all files move out) | Same as above. | Auto-resolves when all contained files are moved; remove empty dir as final step. |

## Absolute-Path Conversion Policy

The following files contain absolute paths (`/Users/.../docs/findings/...` or `/Users/.../docs/plans/...`) that will stale when their targets move:

- `docs/superpowers/plans/2026-06-06-phase20-completion-state-reverification.md`
- `docs/superpowers/plans/2026-06-05-phase20-review-remediation.md`
- `docs/superpowers/specs/2026-06-04-phase20-review-framework-design.md`
- `docs/plans/Phase 20.5 GSD Workflow Repair Implementation Plan.md` (self-references)

**Proposed policy:** For files that are themselves moving, convert absolute paths to **repository-relative paths** (e.g., `docs/work/reviews/milestone_v1.4/...`) in the same commit as the move. For historical audit-trail text that explicitly records "state at a point in time" (e.g., git-status snapshots), leave absolute paths unchanged and add a `[path obsolete — file moved to X]` annotation.

**Approval request includes this policy.**

## Reference Updates To Apply In Same Commit As Moves

| File to edit | Reference to update | From | To |
| --- | --- | --- | --- |
| `README.md` | migration runbook link | `docs/migration/exact-state-mac-migration.md` | `docs/runbooks/migration/exact-state-mac-migration.md` |
| `AGENTS.md` | migration runbook backtick path | `docs/migration/exact-state-mac-migration.md` | `docs/runbooks/migration/exact-state-mac-migration.md` |
| `.planning/PROJECT.md` | framework-spec cleanup design | `docs/superpowers/specs/2026-06-07-framework-spec-cleanup-design.md` | `docs/work/designs/milestone_v1.4/framework-spec-cleanup/2026-06-07-framework-spec-cleanup-design.md` |
| `docs/work/designs/cross_cutting/latex-sync/2026-05-24-latex-markdown-sync-strategy-design.md` | consolidated review | `docs/superpowers/specs/2026-05-24-latex-sync-strategy-consolidated-review.md` | `docs/work/reviews/cross_cutting/latex-sync/2026-05-24-latex-sync-strategy-consolidated-review.md` |

## Approval Request

**Approve only the moves and reference updates listed above. No deletions are included in this proposal.**

Specifically approve:

1. The 22 file moves listed in the Proposed Moves tables.
2. The 4 reference updates in the Reference Updates table.
3. The absolute-path conversion policy for the 4 files listed.
4. Removal of empty legacy directories (`docs/plans/`, `docs/superpowers/`, `docs/user_plans/`, `docs/findings/`, `docs/migration/`) after all moves complete.
5. Leave the 2 blocked files (`splitting_latex.md`, `verifying_review_documents_conversion.md`) in place pending user classification.

To approve: respond with approval. To revise: specify which moves to change, defer, or drop.
