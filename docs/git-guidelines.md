# Git Guidelines

Date adopted: 2026-06-05
Status: Canonical project Git policy

## Purpose

This guideline prevents hidden branch drift, destructive Git loss, low-signal commits, and agent bypass of project commit policy.

## Trigger

Follow this guideline whenever a task may require a later Git commit, even if the commit is not created in the current session.

## Session Start And Branch Awareness

At session start and before committing, run `git status --short --branch` and surface the branch, ahead/behind state, and existing worktree changes. Treat existing changes as user-owned unless you created them in the current task.

## Destructive Operations

Do not run destructive Git operations without explicit user confirmation after explaining what will be affected. This includes `git reset --hard`, `git clean -f`, `git branch -D`, `git rebase`, `git push --force`, `git stash drop`, and disabling hooks.

## Commit Cadence

Commit at logical task boundaries. Keep commits atomic, reversible, and reviewable. Avoid mixed commits that combine planning, implementation, verification, and unrelated cleanup.

## Baseline Before Transformation

Before performing a bulk or mechanical transformation on a file that already carries uncommitted changes — splitting one file into several, reformatting, or large find-and-replace — first commit or stash the pre-existing changes as their own atomic unit. Do not fold unrelated prior edits into the transformation commit: conflating two logically distinct changes destroys the clean pre-transformation baseline that later content-preservation checks depend on.

## Pre-Commit Review Protocol

Before committing, inspect `git status --short`, `git diff --cached`, and the unstaged diff for touched files. Stage only intended files. Run relevant verification and `git diff --check`.

## Commit Message Format

Use `<type>(<scope>): <lowercase imperative subject>`.

Allowed types: `spec`, `evidence`, `verify`, `plan`, `docs`, `feat`, `fix`, `refactor`, `test`, `chore`.

Allowed scopes: two-digit phase scopes such as `20`, task scopes such as `20-05`, and fixed domain scopes `governance`, `planning`, `pinn`, `brutus`, `pipeline`, `spec`, `docs`, `ref`.

The subject starts lowercase, uses imperative voice, is 80 characters or fewer, has no trailing period, and does not contain markdown ticks, quotes, or semicolon-chained changes.

## Required Bodies

A body is required for `spec`, `evidence`, `verify`, and `plan` commits; commits touching multiple files; commits touching `pinn_instruction/`, `.planning/`, framework specs, or governance instructions.

## Auditable Verification Claims

When a commit asserts a verifiable invariant — byte-for-byte preservation, hash match, line or unit counts — record the supporting evidence durably, not in ephemeral locations such as `/tmp`. Commit the per-unit hashes or counts alongside the change, or reference them from a committed path, so a later reviewer can re-derive the claim from committed state instead of trusting the commit message alone.

## Agent Attribution

Agent-authored or materially agent-assisted commits must include `Agent-Assisted-By: <agent/tool/model>` or a valid `Co-Authored-By:` trailer. Agents must use `scripts/agent-commit`; raw agent `git commit` commands are blocked by lifecycle hooks.

## Hook Enforcement

Run `scripts/setup-git-hooks.sh` after cloning or after changing hook files. Do not use `--no-verify`, `core.hooksPath=/dev/null`, or equivalent bypasses without explicit user approval.

## Branches, Tags, And PRs

Do not push directly from protected branches `master`, `main`, or `milestone/*`. Prefer feature branches for PR work. Create recovery branches or tags before destructive operations when loss is possible.

## Recovery

If work appears lost, perform read-only forensics first: `git reflog`, `git fsck`, `git stash list`, and `git worktree list`. Present recovery options before changing state.

## Docs Plan-Review-Fix Lifecycle

These rules govern Git commit behavior for the iterative loop run on implementation plans and review reports under `docs/`: plan execution, independent review, fix-plan, remediation. Rules attach to the action performed, not to which agent performs it; one agent may perform several actions, but each follows its own rule and gets its own commit. File retention, naming, archive, and review closeout are governed by `docs/README.md`; this section governs only commit behavior and defers to `docs/README.md` wherever the two meet.

**Executing a plan.** Commit the executed work as normal typed commits by domain. Record execution provenance in the plan file's frontmatter per `docs/README.md` (`execution_status`, `executed_at` with date, time, and timezone, and `review_status`); legacy plans without frontmatter use the short top-note `docs/README.md` permits. Close each pass with a dedicated commit that updates those keys and carries the trailers `Plan-Execution: first-pass` and `Plan-Source: <plan path>` alongside the mandatory attribution trailer; keep this commit separate from the work commits. Re-executing after remediation uses `remediation-pass-N` in both the status and the trailer. Do not fold pre-existing uncommitted changes into execution commits.

**Reviewing an execution.** Commit a review report as `verify(<scope>)`, or `docs(<scope>)` for non-finding narrative; a body is required for `verify`. Naming and location follow `docs/README.md`. A report is kept, never deleted-and-recreated: superseding an older report sets its frontmatter `status: superseded` in an atomic commit, and the new report is its own commit. Archive or deletion follows the approval-gated lifecycle in `docs/README.md`. If the reviewing agent also finishes or fixes work, commit the report separately from the fixes — findings in one commit, changes in their own atomic commits. After review, update the reviewed plan's `review_status`.

**Authoring a fix or remediation plan.** Commit it as its own `plan(<scope>)` commit, separate from any execution or report commit. When later executed, it follows the Executing a plan rules with a `remediation-pass-N` marker.

**Applying fixes.** Commit fixes as normal typed commits by domain, separate from the report that identified them and the plan that scheduled them.
