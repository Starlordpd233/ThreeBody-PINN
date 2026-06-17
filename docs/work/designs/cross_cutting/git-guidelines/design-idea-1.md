---
status: consumed
purpose: other
created: unknown
milestone: untracked
phase: git-guidelines
retirement_trigger: milestone complete; superseded by subsequent work
Design: Git Workflow and Commit Guidelines
Placement: Expand the existing "Commit Message Conventions" section in .planning/codebase/CONVENTIONS.md (lines 266–301) into a comprehensive "Git Workflow and Commit Guidelines" section. Update AGENTS.md to reference these expanded conventions.
---

Section 1: Commit Message Format and Type Taxonomy

The project already uses Conventional Commits. I propose expanding the type definitions to cover the project-specific types that have emerged:

┌──────────┬───────────────────────────────────────────────────────────────────┬───────────────────────────────────────────────────────────────┐
│   Type   │                             Use When                              Example                            │
├──────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ docs     │ Any documentation, planning artifact, review repordd Phase 20 plan review report                     │
├──────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ spec     │ Framework spec edit that locks or changes a contralign I_3 range to M5 verdict (ARCH-03)             │
├──────────┼───────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────┤
│ evidence │ Evidence packet creation or adjudication record                   │ evidence(20): adjudicate M5 I_3 range/mapping; record verdict │
├──────────┼───────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────┤
│ verify   │ Acceptance check execution and audit verification  AC-ARCH-03 I_3 audits pass; M5 VERIFIED           │
├──────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ plan     │ Planning document edits (PLAN.md, wave assignments)               │ plan(20): remediate review findings before execution          │
├──────────┼───────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────┤
│ feat     │ New script, tool, or capability                                   │ feat(08-01): add verify_compile.py                            │
├──────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ fix      │ Bug fix or correction                             ): correct sampling method ambiguity               │
├──────────┼───────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────┤
│ refactor │ Code restructuring without behavior change                        │ refactor(latex): flatten nested directories                   │
├──────────┼───────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────┤
│ chore    │ Maintenance: gitignore, dependency, cleanup       prescreening_data to .gitignore                    │
├──────────┼───────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────┤
│ test     │ Test additions or test-only changes                               │ test(validator): add footer schema edge cases                 │
└──────────┴───────────────────────────────────────────────────────────────────┴───────────────────────────────────────────────────────────────┘

Scope rules:
- Phase work: docs(20), spec(20), evidence(20), verify(20) — use the phase number
- Sub-plans: docs(17-01), fix(15.1-03) — use plan identifier
- Functional areas: docs(planning), docs(arch), docs(governanceex)
- No scope for truly global changes: docs:, chore:

Subject line rules:
- Imperative mood: "add" not "added"
- Lowercase after colon
- No trailing period
- 50–72 characters preferred

Does this type taxonomy and scope convention look right?

---
Section 2: Atomic Commits and Workflow Patterns

Atomic commit principle: Each commit represents one logical, reversible unit of work. A commit should make sense in isolation.

The evidence→spec→verify pattern (observed in v1.4 adjudication
When a framework spec change requires adjudication, use three atomic commits in this order:

1. evidence(NN) — Create the evidence packet, record the verdict
2. spec(NN) — Apply the spec edit that implements the verdict
3. verify(NN) — Run acceptance checks and confirm the edit is correct

This pattern makes each step independently reviewable and rever

Commit body conventions:
- Add a body (blank line after subject) when the commit is non-
- Explain why, not just what
- For review/report commits, include key findings summary (SIGN
- Use Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com> wtantively

When to combine vs. split:
- Combine: A spec edit + its immediate typo fix in the same file
- Split: Evidence packet creation (new file) vs. spec edit (exiation (different concern)

Does this atomic commit guidance and the three-step adjudication pattern capture how you want to work?

---
Section 3: Branch Strategy

Main branches:
- master — Stable, default branch. Framework specs on master represent the current agreed-upon state.
- milestone/vX.Y — Long-running feature branch for a milestone.

Milestone branch lifecycle:
1. Create milestone/vX.Y from master at milestone start
2. Do all phase work on milestone/vX.Y (direct commits or PRs)
3. When milestone completes, merge milestone/vX.Y → master via merge commit
4. Tag the merge commit: vX.Y
5. Keep the milestone branch for reference (do not delete)

Feature/topic branches (short-lived):
- Use for experimental work, review remediation, or parallel streams
- Name pattern: <category>/<description>-<YYYYMMDD>
- Examples: docs/review-remediation-20260604, fix/sobol-ambiguity-20260520
- Merge back to the milestone branch, not directly to master

Red-flag branch names (require extra caution):
- backup/*, recovery/*, wip/*, experiment/*, tmp/* — confirm before any destructive operation

Does this branch strategy match your intent?

---
Section 4: Tags, Worktrees, and Recovery

Milestone tags:
- v1.0, v1.3, v1.4 — Ship tags marking milestone completion
- v1.4-pre-phase-17 — Pre-phase checkpoint tags
- Create lightweight tags for checkpoints: git tag v1.4-pre-pha
- Create annotated tags for releases: git tag -a v1.4 -m "Mileshysics Foundations"

Recovery tags:
- recovery/<context>-<YYYYMMDD> — Before destructive operations
- Example: recovery/delete-v13-closure-audit-20260521

Worktree conventions:
- Use worktrees for parallel agent sessions to avoid working tree conflicts
- Worktree name pattern: worktree-agent-<hash> or worktree-<description>
- Merge worktree changes with a dedicated commit: chore: merge gent-<hash>)
- Clean up worktrees after merge

Does this tagging and worktree convention look correct?

---
Section 5: Generated Artifacts and What to Commit

Commit these:
- .planning/ metadata files (PLAN.md, CONTEXT.md, GAPS.md, STATE.md, ROADMAP.md) — they track project state
- docs/findings/ review reports and analysis — they are audit artifacts
- Framework spec edits under pinn_instruction/
- Evidence packets and issue ledger updates

Do NOT commit these:
- Large data files (.h5, .npy, .npz, .mat) — already in .gitignore
- Model checkpoints (.pt, .pth, .ckpt)
- Training logs and results
- LaTeX build artifacts (.aux, .pdf, .log)
- Simulation outputs (brutus_Newton-main/output/)
- Work-in-progress temp files

Review artifacts rule:
- If a review report is part of the milestone audit trail → commit it
- If it's a personal scratchpad or transient analysis → keep it

Does this commit/ignore distinction for generated artifacts ali

---
Section 6: Merge and Pull Request Conventions

Milestone merge to master:
- Use a merge commit (not squash) to preserve phase-level history
- The merge commit message should reference the milestone: Merge milestone/v1.4 into master
- Tag the merge commit immediately with the milestone version

PR conventions (when used):
- PR title follows commit convention: docs(20): Phase 20 plan review remediation
- Squash only for trivial fixup commits; preserve atomic commits for adjudication workflows
- Include Closes #<issue> or Refs #<issue> in PR description when applicable

Before any destructive operation:
1. Create recovery checkpoint: git branch backup/<context>-<date> or git tag recovery/<context>-<date>
2. Confirm with user what will be affected
3. Proceed only with clear confirmation

Does this merge/PR convention match how you want to handle milestone completion?

---
Section 7: Agent Co-Authorship and Commit Authorship

When to use Co-Authored-By:
- Agent performed substantive research, analysis, or multi-file editing
- Agent authored an evidence packet, review report, or planning
- Agent executed a plan with multiple atomic commits

When NOT to use Co-Authored-By:
- Trivial single-file edits
- The user performed the work and the agent only assisted
- Automated formatting or mechanical changes

Commit author:
- Primary author is the human user
- Agent contributions are credited via Co-Authored-By trailer in commit body

---
Next Step

If these seven sections look good, I'll:
1. Write the expanded guidelines into .planning/codebase/CONVENTIONS.md
2. Update AGENTS.md to reference the expanded conventions
3. Commit the changes with an appropriate message

Please let me know which sections need adjustment, or if you're