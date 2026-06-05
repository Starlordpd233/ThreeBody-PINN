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

## Pre-Commit Review Protocol

Before committing, inspect `git status --short`, `git diff --cached`, and the unstaged diff for touched files. Stage only intended files. Run relevant verification and `git diff --check`.

## Commit Message Format

Use `<type>(<scope>): <lowercase imperative subject>`.

Allowed types: `spec`, `evidence`, `verify`, `plan`, `docs`, `feat`, `fix`, `refactor`, `test`, `chore`.

Allowed scopes: two-digit phase scopes such as `20`, task scopes such as `20-05`, and fixed domain scopes `governance`, `planning`, `pinn`, `brutus`, `pipeline`, `spec`, `docs`, `ref`.

The subject starts lowercase, uses imperative voice, is 80 characters or fewer, has no trailing period, and does not contain markdown ticks, quotes, or semicolon-chained changes.

## Required Bodies

A body is required for `spec`, `evidence`, `verify`, and `plan` commits; commits touching multiple files; commits touching `pinn_instruction/`, `.planning/`, framework specs, or governance instructions.

## Agent Attribution

Agent-authored or materially agent-assisted commits must include `Agent-Assisted-By: <agent/tool/model>` or a valid `Co-Authored-By:` trailer. Agents must use `scripts/agent-commit`; raw agent `git commit` commands are blocked by lifecycle hooks.

## Hook Enforcement

Run `scripts/setup-git-hooks.sh` after cloning or after changing hook files. Do not use `--no-verify`, `core.hooksPath=/dev/null`, or equivalent bypasses without explicit user approval.

## Branches, Tags, And PRs

Do not push directly from protected branches `master`, `main`, or `milestone/*`. Prefer feature branches for PR work. Create recovery branches or tags before destructive operations when loss is possible.

## Recovery

If work appears lost, perform read-only forensics first: `git reflog`, `git fsck`, `git stash list`, and `git worktree list`. Present recovery options before changing state.
