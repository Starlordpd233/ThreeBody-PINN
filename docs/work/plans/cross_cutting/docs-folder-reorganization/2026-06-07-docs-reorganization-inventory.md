---
status: consumed
purpose: other
created: 2026-06-07
milestone: untracked
phase: docs-folder-reorganization
retirement_trigger: milestone complete; superseded by subsequent work
---

# Docs Reorganization Inventory

> Generated: 2026-06-07
> Branch: `milestone/v1.4` (ahead 65 of origin)

## Git State

Pre-existing docs changes already in the worktree (treated as user-owned):

```
 D docs/findings/milestone_v1.4/phase_20.5_plan_critique_review.md
 D docs/findings/milestone_v1.4/reviewing_phase20_plans/phase20_review.md
 D docs/superpowers/specs/2026-06-05-git-commit-convention-design.md
?? docs/README.md
?? docs/findings/milestone_v1.4/reviewing_phase20.5_plan/
?? docs/plans/2026-06-06-phase-20-5-plan-remediation-implementation-plan.md
?? docs/superpowers/plans/
?? docs/superpowers/reviews/
?? docs/user_plans/design_git_guideline/
```

Note: Three tracked docs files already show `D` (deleted in worktree, not yet staged). These deletions are pre-existing and will not be restored or finalized without explicit approval.

## Active Root Docs

| Current path | Proposed action | Reason |
| --- | --- | --- |
| `docs/README.md` | retain | Target rules doc; defines the destination structure |
| `docs/git-guidelines.md` | retain | Referenced by `AGENTS.md` and `scripts/git_policy/validate_commit_msg.py`; out of scope for this move |

## Runbooks

| Current path | Proposed path | Reference updates needed | Reason |
| --- | --- | --- | --- |
| `docs/migration/exact-state-mac-migration.md` | `docs/runbooks/migration/exact-state-mac-migration.md` | `AGENTS.md` references old path | Active migration runbook; target structure places runbooks in `docs/runbooks/` |
| `docs/migrating_to_macbookPro.txt` | `docs/runbooks/migration/migrating-to-macbook-pro.txt` | none found | Older plain-text migration notes; same topic; rename to markdown-friendly slug |

## Work Plans

### `docs/work/plans/milestone_v1.4/`

| Current path | Proposed path | Proposed action | Reason |
| --- | --- | --- | --- |
| `docs/plans/2026-06-06-phase-20-5-plan-remediation-implementation-plan.md` | `docs/work/plans/milestone_v1.4/20.5-plan-remediation/2026-06-06-phase-20-5-plan-remediation-implementation-plan.md` | move | Phase 20.5 plan, belongs in milestone_v1.4 subtree with decimal phase dir |
| `docs/plans/ADOPT_EDL_19_01_UPDATED_PLAN.md` | `docs/work/plans/milestone_v1.4/19-edl-adoption/ado-edl-19-01-updated-execution-plan.md` | move | EDL-19-01 adoption plan; phase 19 is part of v1.4 milestone |
| `docs/plans/Phase 20.5 GSD Workflow Repair Implementation Plan.md` | `docs/work/plans/milestone_v1.4/20.5-gsd-workflow-repair/phase-20.5-gsd-workflow-repair-implementation-plan.md` | move + slugify (remove spaces) | Phase 20.5 plan; filename must be URL/slug-safe |
| `docs/superpowers/plans/2026-06-05-phase20-review-remediation.md` | `docs/work/plans/milestone_v1.4/20-review-remediation/2026-06-05-phase20-review-remediation.md` | move | Phase 20 plan |
| `docs/superpowers/plans/2026-06-06-phase20-completion-state-reverification.md` | `docs/work/plans/milestone_v1.4/20-completion-reverification/2026-06-06-phase20-completion-state-reverification.md` | move | Phase 20 plan |

### `docs/work/plans/cross_cutting/`

| Current path | Proposed path | Proposed action | Reason |
| --- | --- | --- | --- |
| `docs/superpowers/plans/2026-06-05-enforce-git-guideline.md` | `docs/work/plans/cross_cutting/git-guidelines/2026-06-05-enforce-git-guideline.md` | move | Cross-cutting (not phase-specific) |
| `docs/user_plans/plans/2026-03-19-remove-qwen-model-and-mlx.md` | `docs/work/plans/cross_cutting/cleanup/2026-03-19-remove-qwen-model-and-mlx.md` | move | Cross-cutting cleanup plan |

### `docs/work/plans/unclassified/` (need user routing)

| Current path | Proposed path | Proposed action | Reason |
| --- | --- | --- | --- |
| `docs/user_plans/splitting_latex.md` | TBD | blocked | Title is "Proposed File Structure" — content unclear without reading; could be LaTeX framework split (historical) or early docs-layout proposal. Needs user classification before routing. |
| `docs/user_plans/verifying_review_documents_conversion.md` | TBD | blocked | Title empty; purpose unknown without reading. Needs user classification. |

## Work Reviews

### `docs/work/reviews/milestone_v1.4/`

| Current path | Proposed path | Proposed action | Finding closeout needed |
| --- | --- | --- | --- |
| `docs/superpowers/reviews/reviewing_20260605-phase-20-review-remediation-plan.md` | `docs/work/reviews/milestone_v1.4/20-review-remediation/2026-06-05-phase-20-review-remediation-review.md` | move | Verify all P1 findings from this review were addressed in the Phase 20 remediation work |
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/review1.md` | `docs/work/reviews/milestone_v1.4/20.5-plan-audit/2026-06-06-phase-20.5-audit-review1.md` | move | Audit report for 20.5 plan; verify findings closed |
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/review2.md` | `docs/work/reviews/milestone_v1.4/20.5-plan-audit/2026-06-06-phase-20.5-audit-review2.md` | move | Audit findings; verify closed |
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/review3.md` | `docs/work/reviews/milestone_v1.4/20.5-plan-audit/2026-06-06-phase-20.5-audit-review3.md` | move | Adversarial audit; verify closed |
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/review4.md` | `docs/work/reviews/milestone_v1.4/20.5-plan-audit/2026-06-06-phase-20.5-audit-review4.md` | move | Title empty; verify closed |
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/previous_reports/phase20_review.md` | `docs/work/reviews/milestone_v1.4/20-plan-audit-legacy/phase20-review.md` | move | Labeled "previous_reports" — candidate for archive rather than active reviews |
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/previous_reports/phase20-deep-adversarial-review-v2-2026-06-04.md` | `docs/work/reviews/milestone_v1.4/20-plan-audit-legacy/phase20-deep-adversarial-review-v2-2026-06-04.md` | move | Legacy Phase 20 review |
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/previous_reports/20-plan-review-comprehensive.md` | `docs/work/reviews/milestone_v1.4/20-plan-audit-legacy/20-plan-review-comprehensive.md` | move | Legacy |
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/previous_reports/20-plan-review-findings.md` | `docs/work/reviews/milestone_v1.4/20-plan-audit-legacy/20-plan-review-findings.md` | move | Legacy |
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/previous_reports/20-plan-deep-adversarial-review-2026-06-04.md` | `docs/work/reviews/milestone_v1.4/20-plan-audit-legacy/20-plan-deep-adversarial-review-2026-06-04.md` | move | Legacy |
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/previous_reports/2026-06-04-phase20-comprehensive-review.md` | `docs/work/reviews/milestone_v1.4/20-plan-audit-legacy/2026-06-04-phase20-comprehensive-review.md` | move | Legacy |
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/previous_reports/20-5-plan-staleness-review-2026-06-06.md` | `docs/work/reviews/milestone_v1.4/20.5-plan-audit-legacy/20-5-plan-staleness-review-2026-06-06.md` | move | Lives in `previous_reports/` but is about 20.5; route to 20.5 legacy subfolder |

### `docs/work/reviews/milestone_v1.4/` (standalone finding doc)

| Current path | Proposed path | Proposed action | Finding closeout needed |
| --- | --- | --- | --- |
| `docs/findings/milestone_v1.4/phase20-completion-reverification-2026-06-06.md` | `docs/work/reviews/milestone_v1.4/20-completion-reverification/phase20-completion-reverification-2026-06-06.md` | move | Reverification report; verify conclusions still hold |
| `docs/findings/milestone_v1.4/reviewing_19_context.md` | `docs/work/reviews/milestone_v1.4/19-context-verification/reviewing-19-context.md` | move | Verification report for 19-CONTEXT.md |

## Work Designs

| Current path | Proposed path | Proposed action | Reason |
| --- | --- | --- | --- |
| `docs/work/designs/cross_cutting/git-guidelines/2026-06-07-docs-lifecycle-git-behavior-design.md` | (already in correct location) | retain | Already follows target structure |
| `docs/superpowers/specs/2026-05-24-latex-markdown-sync-strategy-design.md` | `docs/work/designs/cross_cutting/latex-sync/2026-05-24-latex-markdown-sync-strategy-design.md` | move | Cross-cutting design |
| `docs/superpowers/specs/2026-05-24-latex-sync-strategy-consolidated-review.md` | `docs/work/reviews/cross_cutting/latex-sync/2026-05-24-latex-sync-strategy-consolidated-review.md` | move | Review of a design, not a design itself |
| `docs/superpowers/specs/2026-06-04-phase20-review-framework-design.md` | `docs/work/designs/milestone_v1.4/20-review-framework/2026-06-04-phase20-review-framework-design.md` | move | Phase 20 design |
| `docs/superpowers/specs/2026-06-07-framework-spec-cleanup-design.md` | `docs/work/designs/milestone_v1.4/framework-spec-cleanup/2026-06-07-framework-spec-cleanup-design.md` | move | v1.4-adjacent design |
| `docs/user_plans/design_git_guideline/2026-06-05-git-commit-convention-design.md` | `docs/work/designs/cross_cutting/git-guidelines/2026-06-05-git-commit-convention-design.md` | move | Design that produced git-guidelines |
| `docs/user_plans/design_git_guideline/design_idea_1.md` | `docs/work/designs/cross_cutting/git-guidelines/design-idea-1.md` | move | Early design idea |
| `docs/user_plans/design_git_guideline/final_git_guideline_review.md` | `docs/work/reviews/cross_cutting/git-guidelines/final-git-guideline-review.md` | move | Review, not design |

## Deletion Proposal Candidates

| Current path | Type | Why it may be consumed | Required proof before proposal |
| --- | --- | --- | --- |
| `docs/findings/milestone_v1.4/phase_20.5_plan_critique_review.md` | review | Already `D` in worktree (user deleted); likely findings folded into later reviews | Confirm no open findings; confirm no other file references it by path |
| `docs/findings/milestone_v1.4/reviewing_phase20_plans/phase20_review.md` | review | Already `D` in worktree; duplicate of file now in `reviewing_phase20.5_plan/previous_reports/phase20_review.md` | Confirm the surviving copy is byte-identical or intentionally different; confirm no references |
| `docs/superpowers/specs/2026-06-05-git-commit-convention-design.md` | design | Already `D` in worktree; design work consumed by `docs/user_plans/design_git_guideline/2026-06-05-git-commit-convention-design.md` and ultimately by `docs/git-guidelines.md` | Confirm design is fully consumed by final guideline; confirm no references |

## Do Not Touch Yet

| Current path | Reason |
| --- | --- |
| `docs/plans/`, `docs/superpowers/`, `docs/user_plans/`, `docs/findings/` as top-level folders | Will become empty only after all moves are applied; remove empty dirs as last step |
| `docs/superpowers/specs/2026-06-05-git-commit-convention-design.md` (tracked-deleted state) | Already in `D` state; do not stage deletion until deletion proposal approved |
| `docs/findings/milestone_v1.4/phase_20.5_plan_critique_review.md` (tracked-deleted state) | Same; deletion proposal required |
| `docs/findings/milestone_v1.4/reviewing_phase20_plans/phase20_review.md` (tracked-deleted state) | Same; deletion proposal required |
| `docs/user_plans/splitting_latex.md` | Content not classified; blocked on user routing decision |
| `docs/user_plans/verifying_review_documents_conversion.md` | Content not classified; blocked on user routing decision |
| Pre-existing modifications to `.planning/`, `pinn_instruction/`, `.claude/settings.json` | Out of scope for docs reorganization; user-owned |

## Reference Audit Notes

### Root/runbook references

- `docs/migration/exact-state-mac-migration.md`: referenced by `README.md:9` and `AGENTS.md:12`. **Move is blocked until both references are updated in the same commit as the move.**
- `docs/git-guidelines.md`: referenced by `AGENTS.md:128`, `ANTIGRAVITY.md:44`, `README.md:9`, `scripts/git_policy/validate_commit_msg.py:100`, and many plans/designs. **Retained at current path** per plan constraint; not in scope for this reorg.
- `docs/migrating_to_macbookPro.txt`: **no external references found** by exact path, basename, or stem. Eligible for move.

### Deletion candidate references

- `docs/findings/milestone_v1.4/phase_20.5_plan_critique_review.md`: already `D` in worktree. Active references by path in:
  - `docs/plans/Phase 20.5 GSD Workflow Repair Implementation Plan.md:932, 940` (Decision Gate record cites it as source)
  - `docs/plans/2026-06-06-phase-20-5-plan-remediation-implementation-plan.md:30` (as `reviewing_phase20.5_plan/phase_20.5_plan_critique_review.md` — path variant)
  - `docs/superpowers/plans/2026-06-06-phase20-completion-state-reverification.md:857` (in a `test -e` command)
  - `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/review3.md:13` (records its deletion)
  - **Assessment:** references are historical audit-trail citations, not live dependencies. Deletion is safe; references may be left as historical context or annotated.
- `docs/findings/milestone_v1.4/reviewing_phase20_plans/phase20_review.md`: already `D` in worktree. Active references by path in:
  - `docs/superpowers/specs/2026-06-04-phase20-review-framework-design.md:68`
  - `docs/superpowers/plans/2026-06-05-phase20-review-remediation.md:22`
  - `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/review3.md:14`
  - **Assessment:** all references are historical audit-trail citations. A duplicate now lives at `reviewing_phase20.5_plan/previous_reports/phase20_review.md`. Deletion of the `reviewing_phase20_plans/` copy is safe; references may point to the surviving copy.
- `docs/superpowers/specs/2026-06-05-git-commit-convention-design.md`: already `D` in worktree. Only reference is `docs/findings/milestone_v1.4/phase20-completion-reverification-2026-06-06.md:16` recording its deletion status. **Safe to finalize deletion.**

### Legacy folder references

- `.planning/tmp/docs-work-manifest.json`: references many legacy `docs/findings/`, `docs/plans/`, `docs/user_plans/` paths. This is a transient manifest; it will be regenerated or cleaned up separately and does **not** block moves.
- `.planning/phases/*/18-CONTEXT.md`, `19-GAPS.md`, `20-DISCUSSION-LOG.md`, `20-5-*.md`: historical planning-phase references to legacy docs paths. These are historical audit-trail references; they do not block moves but should not be silently updated either.
- `.planning/MILESTONES.md:52`, `.planning/PROJECT.md:164-165`: references to `docs/findings/addressing_sobol_sequence_suggestion.md` and `docs/superpowers/specs/2026-06-07-framework-spec-cleanup-design.md`. The first is a historical finding (file does not exist in current tree); the second is a live file proposed for move. **Move of the design spec will stale the PROJECT.md reference** — flag for update in the move proposal.
- `docs/README.md:50, 402, 408-411`: names the legacy folders as legacy. These references are intentional documentation of the legacy structure; **do not update**.
- `docs/user_plans/design_git_guideline/final_git_guideline_review.md:15, 445` and `docs/user_plans/design_git_guideline/design_idea_1.md:126`: references to `docs/git-guidelines.md` and `docs/findings/`. `docs/git-guidelines.md` stays; `docs/findings/` mentions are generic category mentions, not path-specific.
- Plan files in `docs/superpowers/plans/`, `docs/plans/`: many internal references to `docs/findings/` paths. These files will themselves move, carrying their internal references. **Internal references within moving files do not need separate update unless they are absolute paths.**

### Absolute-path references that will stale

Files containing absolute paths like `<home>/Desktop/3_body_problem/docs/findings/...` or `<home>/Desktop/3_body_problem/docs/plans/...` will stale when files move. Affected:

- `docs/superpowers/plans/2026-06-06-phase20-completion-state-reverification.md` — many absolute paths to `docs/findings/` files
- `docs/superpowers/plans/2026-06-05-phase20-review-remediation.md` — absolute paths to `docs/findings/milestone_v1.4/reviewing_phase20_plans/*`
- `docs/superpowers/specs/2026-06-04-phase20-review-framework-design.md` — absolute path to `docs/findings/.../phase20_review.md`
- `docs/plans/Phase 20.5 GSD Workflow Repair Implementation Plan.md` — absolute self-references to `docs/plans/Phase 20.5 GSD Workflow Repair Implementation Plan.md`

**Proposal:** convert absolute paths to relative paths in moving files where the target also moves; leave absolute paths in historical audit-trail text unchanged when they describe state at a point in time.
