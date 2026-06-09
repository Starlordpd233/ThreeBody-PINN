# Docs Deletion Proposals

> Generated: 2026-06-07
> Depends on: `2026-06-07-docs-reorganization-inventory.md`, `2026-06-07-docs-reorganization-move-proposal.md`
> Status: **PARTIALLY APPROVED** (2026-06-08) — #2 and #3 approved and executed; #1 rejected for deletion, file preserved.

## Summary

Three tracked files were in `D` state (deleted in worktree, not yet staged). Approval received 2026-06-08:

- **#1 (`phase_20.5_plan_critique_review.md`)**: DELETION REJECTED. File contains unique content (Part 3 false-negatives, Part 4 decision gates) not fully folded into review1-4. Restored and preserved at `docs/work/reviews/milestone_v1.4/20.5-plan-audit/2026-05-27-phase-20.5-plan-critique-review.md` alongside review1-4.
- **#2 (`reviewing_phase20_plans/phase20_review.md`)**: DELETION APPROVED. Duplicate preserved at `docs/work/reviews/milestone_v1.4/20-plan-audit-legacy/phase20-review.md`. Staged via `git rm`.
- **#3 (`2026-06-05-git-commit-convention-design.md`)**: DELETION APPROVED. Design fully consumed by `docs/git-guidelines.md`; design history preserved at `docs/work/designs/cross_cutting/git-guidelines/2026-06-05-git-commit-convention-design.md`. Staged via `git rm`.

---

## Deletion 1: `docs/findings/milestone_v1.4/phase_20.5_plan_critique_review.md` — **REJECTED, FILE PRESERVED**

**Decision (2026-06-08):** User rejected deletion. File contains unique content (Part 3 false-negatives, Part 4 decision gates) not fully captured in review1-4 audit reports. Restored from HEAD and moved to preserved location.

**Preserved at:** `docs/work/reviews/milestone_v1.4/20.5-plan-audit/2026-05-27-phase-20.5-plan-critique-review.md`

**Rationale:** Governance-aligned choice is to preserve unique audit content. All three files were recoverable from git history regardless, but #1 has substantive unique value.

<details>
<summary>Original proposal (for historical record)</summary>

```yaml
File: docs/findings/milestone_v1.4/phase_20.5_plan_critique_review.md
Type: review
Purpose served: Early critique review of Phase 20.5 plan; findings partially folded into later audit reviews (review1-4 in `reviewing_phase20.5_plan/`)
Replacement or consuming artifact: 
  - `docs/work/reviews/milestone_v1.4/20.5-plan-audit/2026-06-06-phase-20.5-audit-review1.md`
  - `docs/work/reviews/milestone_v1.4/20.5-plan-audit/2026-06-06-phase-20.5-audit-review2.md`
  - `docs/work/reviews/milestone_v1.4/20.5-plan-audit/2026-06-06-phase-20.5-audit-review3.md`
  - `docs/work/reviews/milestone_v1.4/20.5-plan-audit/2026-06-06-phase-20.5-audit-review4.md`
  - Final Phase 20.5 plan: `.planning/phases/20-5-sampling-coordinate-allocation/20-5-PLAN.md`
Reference audit:
  - Exact path references: 4 (all in historical audit-trail text)
  - Basename references: 5 (all in historical audit-trail text)
  - Stem references: 5 (all in historical audit-trail text)
  - Live dependencies: 0
  - Commands run:
    ```sh
    rg --hidden --glob '!.git/*' -n --fixed-strings "docs/findings/milestone_v1.4/phase_20.5_plan_critique_review.md" .
    rg --hidden --glob '!.git/*' -n --fixed-strings "phase_20.5_plan_critique_review.md" .
    rg --hidden --glob '!.git/*' -n --fixed-strings "phase_20.5_plan_critique_review" .
    ```
  - Result: all references are historical audit-trail citations in:
    - `docs/work/plans/milestone_v1.4/20.5-gsd-workflow-repair/phase-20.5-gsd-workflow-repair-implementation-plan.md:932, 940` (Decision Gate record)
    - `docs/work/plans/milestone_v1.4/20.5-plan-remediation/2026-06-06-phase-20-5-plan-remediation-implementation-plan.md:30` (as path variant)
    - `docs/work/plans/milestone_v1.4/20-completion-reverification/2026-06-06-phase20-completion-state-reverification.md:857` (in test command)
    - `docs/work/reviews/milestone_v1.4/20.5-plan-audit/2026-06-06-phase-20.5-audit-review3.md:13` (records deletion)
  - Assessment: references are historical context, not live dependencies. Safe to finalize deletion.
Review closeout:
  | Finding | Status | Evidence |
  | --- | --- | --- |
  | Early critique of Phase 20.5 plan structure | addressed | Folded into review1-4 audit reports; final plan reflects resolutions |
  | Decision Gate record citations | historical | Cited as historical source in GSD workflow repair plan; no action required |
Proposed action: delete (finalize `git rm` for already-deleted file)
Approval needed: yes
```

</details>

---

## Deletion 2: `docs/findings/milestone_v1.4/reviewing_phase20_plans/phase20_review.md` — **APPROVED, DELETED**

```yaml
File: docs/findings/milestone_v1.4/reviewing_phase20_plans/phase20_review.md
Type: review
Purpose served: Initial Phase 20 plan review; superseded by more comprehensive reviews in `reviewing_phase20_plans/` directory
Replacement or consuming artifact:
  - `docs/work/reviews/milestone_v1.4/20-plan-audit-legacy/phase20-review.md` (duplicate, preserved during reorg)
  - `docs/work/reviews/milestone_v1.4/20-plan-audit-legacy/20-plan-review-comprehensive.md`
  - `docs/work/reviews/milestone_v1.4/20-plan-audit-legacy/20-plan-deep-adversarial-review-2026-06-04.md`
  - `docs/work/reviews/milestone_v1.4/20-plan-audit-legacy/phase20-deep-adversarial-review-v2-2026-06-04.md`
  - `docs/work/reviews/milestone_v1.4/20-plan-audit-legacy/20-plan-review-findings.md`
  - `docs/work/reviews/milestone_v1.4/20-plan-audit-legacy/2026-06-04-phase20-comprehensive-review.md`
Reference audit:
  - Exact path references: 3 (all in historical audit-trail text)
  - Basename references: 3 (all in historical audit-trail text)
  - Stem references: 3 (all in historical audit-trail text)
  - Live dependencies: 0
  - Commands run:
    ```sh
    rg --hidden --glob '!.git/*' -n --fixed-strings "docs/findings/milestone_v1.4/reviewing_phase20_plans/phase20_review.md" .
    rg --hidden --glob '!.git/*' -n --fixed-strings "phase20_review.md" .
    rg --hidden --glob '!.git/*' -n --fixed-strings "phase20_review" .
    ```
  - Result: all references are historical audit-trail citations in:
    - `docs/work/designs/milestone_v1.4/20-review-framework/2026-06-04-phase20-review-framework-design.md:68`
    - `docs/work/plans/milestone_v1.4/20-review-remediation/2026-06-05-phase20-review-remediation.md:22`
    - `docs/work/reviews/milestone_v1.4/20.5-plan-audit/2026-06-06-phase-20.5-audit-review3.md:14`
  - Assessment: references are historical context, not live dependencies. A duplicate now lives at `docs/work/reviews/milestone_v1.4/20-plan-audit-legacy/phase20-review.md`. Safe to finalize deletion of the `reviewing_phase20_plans/` copy.
Review closeout:
  | Finding | Status | Evidence |
  | --- | --- | --- |
  | Initial Phase 20 plan review findings | addressed | Comprehensive reviews in `20-plan-audit-legacy/` supersede this initial review |
  | Historical audit-trail value | preserved | Duplicate retained in `20-plan-audit-legacy/` for historical record |
Proposed action: delete (finalize `git rm` for already-deleted file)
Approval needed: yes
```

---

## Deletion 3: `docs/superpowers/specs/2026-06-05-git-commit-convention-design.md` — **APPROVED, DELETED**

```yaml
File: docs/superpowers/specs/2026-06-05-git-commit-convention-design.md
Type: design
Purpose served: Early design spec for git commit convention; fully consumed by `docs/git-guidelines.md`
Replacement or consuming artifact:
  - `docs/git-guidelines.md` (canonical reference)
  - `docs/work/designs/cross_cutting/git-guidelines/2026-06-05-git-commit-convention-design.md` (design history, preserved)
  - `docs/work/reviews/cross_cutting/git-guidelines/final-git-guideline-review.md` (review, preserved)
Reference audit:
  - Exact path references: 1 (in historical audit-trail text)
  - Basename references: 1 (in historical audit-trail text)
  - Stem references: 1 (in historical audit-trail text)
  - Live dependencies: 0
  - Commands run:
    ```sh
    rg --hidden --glob '!.git/*' -n --fixed-strings "docs/superpowers/specs/2026-06-05-git-commit-convention-design.md" .
    rg --hidden --glob '!.git/*' -n --fixed-strings "2026-06-05-git-commit-convention-design.md" .
    rg --hidden --glob '!.git/*' -n --fixed-strings "2026-06-05-git-commit-convention-design" .
    ```
  - Result: only reference is in:
    - `docs/work/reviews/milestone_v1.4/20-completion-reverification/phase20-completion-reverification-2026-06-06.md:16` (records deletion status)
  - Assessment: design is fully consumed by `docs/git-guidelines.md`. Design history is preserved in `docs/work/designs/cross_cutting/git-guidelines/2026-06-05-git-commit-convention-design.md`. Safe to finalize deletion.
Review closeout:
  | Finding | Status | Evidence |
  | --- | --- | --- |
  | Git commit convention design | addressed | Fully consumed by `docs/git-guidelines.md` |
  | Design history | preserved | Retained in `docs/work/designs/cross_cutting/git-guidelines/2026-06-05-git-commit-convention-design.md` |
Proposed action: delete (finalize `git rm` for already-deleted file)
Approval needed: yes
```

---

## Approval Request

**Approve finalization of the 3 deletions listed above.**

Specifically approve:

1. `git rm docs/findings/milestone_v1.4/phase_20.5_plan_critique_review.md`
2. `git rm docs/findings/milestone_v1.4/reviewing_phase20_plans/phase20_review.md`
3. `git rm docs/superpowers/specs/2026-06-05-git-commit-convention-design.md`

To approve: respond with "approved" or similar confirmation.
To reject: specify which deletion(s) to reject.
