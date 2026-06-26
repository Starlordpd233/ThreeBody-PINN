# Git Guidelines

Date adopted: 2026-06-05
Last revised: 2026-06-11
Status: Canonical project Git policy

## Purpose

This guideline prevents hidden branch drift, destructive Git loss, low-signal
commits, mixed concurrent-agent commits, and agent bypass of project commit
policy. It is written for both humans and agents; when archived plans or older
snippets conflict with this document, this document wins.

## Plain-Language Git Vocabulary

- **Working tree**: the project files currently on disk.
- **Staged files**: the exact files selected for the next commit.
- **Commit**: a durable saved checkpoint in project history.
- **Branch**: a named timeline of commits, such as `milestone/v1.5`.
- **Tag or backup branch**: a named pointer to a known commit.
- **Stash**: a temporary shelf for unfinished file changes.
- **Worktree**: a separate checkout of the same repository, useful when multiple
  agents work at the same time.

## Trigger

Follow this guideline whenever a task may require a later Git commit, even if
the commit is not created in the current session.

## Session Start And Branch Awareness

At session start and before committing, run `git status --short --branch` and
surface the branch, ahead/behind state, and existing worktree changes. Treat
existing changes as user-owned unless you created them in the current task.

Pause and ask before proceeding when:

- You are on a red-flag branch such as `backup/*`, `recovery/*`, `wip/*`,
  `experiment/*`, or `tmp/*`.
- You are in a non-primary or unfamiliar worktree.
- You cannot fully enumerate what a Git operation will affect.
- The user reports lost work.

## Autonomy Matrix

Agents may do these without asking:

- Run read-only Git inspection commands.
- Stage explicit owned paths.
- Commit approved task work at logical boundaries.
- Create non-destructive recovery tags or backup branches.
- Push non-protected feature or backup branches when the task calls for it.

Agents must ask first:

- Any destructive operation.
- Any protected-branch push.
- Any history rewrite.
- Any operation affecting user-owned or unknown changes.
- Any hook bypass.

Agents must stop instead of guessing:

- The desired branch, remote, or affected files are ambiguous.
- Git reports conflicts or missing work.
- A required approval, owned-path declaration, or checkpoint marker is missing.

## Commit Cadence

Agents may auto-commit approved task work at logical boundaries unless the user
explicitly says not to commit. Keep commits atomic, reversible, and reviewable.
Avoid mixed commits that combine planning, implementation, verification, and
unrelated cleanup.

Good commit boundaries:

- One script or hook behavior change plus its tests.
- One documentation policy revision.
- One phase task or evidence packet.

Poor commit boundaries:

- A broad `wip` snapshot.
- A commit mixing generated outputs, policy text, and unrelated planning files.
- A commit that stages files outside the agent's declared ownership.

## Agent-Owned Paths

Every agent commit must use `scripts/agent-commit` and set:

- `GIT_AGENT_ID`: the active agent, tool, and model.
- `GIT_AGENT_OWNED_PATHS`: colon- or newline-separated repo-relative file or
  directory prefixes the agent is responsible for.

Example:

```bash
GIT_AGENT_ID="Codex GPT-5" \
GIT_AGENT_OWNED_PATHS='AGENTS.md:docs/git-guidelines.md:scripts/git_policy:tests/git_policy' \
scripts/agent-commit -m "docs(governance): clarify git autonomy policy" \
  -m "Explain the revised autonomy, checkpoint, and concurrent-agent rules."
```

Owned paths must be repo-relative. Do not use absolute paths, `.`, `..`, root,
or paths containing parent traversal. The commit validator rejects staged files
outside `GIT_AGENT_OWNED_PATHS`.

Use explicit staging only. Do not use broad staging commands such as
`git add .`, `git add -A`, `git add --all`, or `git add -u`.

## Concurrent Agent Work

For Claude Code CCP or any multi-agent setup, prefer separate worktrees and
branches for independent agents. If agents share one worktree, they must still
declare disjoint owned paths and commit through `scripts/agent-commit`.

Rules for concurrent agents:

- Prefer one agent per worktree/branch for independent work.
- Declare owned paths before editing and before committing.
- Stage only owned paths.
- Re-run `git status --short --branch`, `git diff --cached`, and relevant
  unstaged diffs immediately before commit.
- If another agent commits first, re-check the branch and staged diff before
  committing.
- Never alter another agent's staged or unstaged work unless explicitly assigned.

`scripts/agent-commit` serializes commits with a repository-local lock shared by
all worktrees. Acquisition waits up to ~5 minutes for a held lock and reclaims it
only when the holder process is gone or the lock exceeds the stale floor (both
default 300s, overridable via `AGENT_COMMIT_LOCK_TIMEOUT` / `AGENT_COMMIT_LOCK_STALE`),
so a live commit is never interrupted and a crashed holder never blocks others.

### Per-track worktrees and overlap avoidance

- Long-running parallel tracks (e.g. `specwork`, `trainex`) each get a worktree
  under `.worktrees/<track>/`; the main repo folder stays on `master` for
  cross-cutting governance, planning, and CI. Tracks **merge** `master` into their
  branch and never rebase (history is never rewritten).
- Before overlapping on a file or folder, consult or declare it with
  `scripts/agent-claim <area>` (release with `scripts/agent-release <area>`;
  claims self-expire after ~2 hours). An on-edit hook warns automatically when a
  target overlaps another session's claim and auto-declares the editing session's
  claim, so the warning does not depend on remembering to check.
- The hard backstop is the commit-time owned-paths net: a commit may only stage
  paths under `GIT_AGENT_OWNED_PATHS` (enforced by the commit-msg validator,
  `scripts/git_policy/validate_commit_msg.py`, gated on `GIT_AGENT_COMMIT=1`).

## Capture And Recovery Ladder

Use the lightest recovery mechanism that preserves the right state:

1. Completed logical work: commit it.
2. Risky history or branch operations: create a backup branch or tag first.
3. Dirty unfinished work: use a stash or durable patch snapshot when a commit is
   not appropriate.
4. Suspected lost work: perform read-only forensics before changing state.

Do not rely on `/tmp` for evidence or recovery material that must survive the
task.

## Destructive Operations

Do not run destructive Git operations without exact user approval after
explaining what will be affected. Approval must name either the exact command or
the exact effect. Vague approval is not enough.

Destructive operations include `git reset --hard`, `git clean -f`,
`git branch -D`, `git rebase`, `git push --force`, `git stash drop`, disabling
hooks, and `rm -rf` on tracked paths.

Before a destructive operation, create or verify a recovery checkpoint. The
command must include all three markers:

```bash
ALLOW_DESTRUCTIVE_GIT=1
GIT_DESTRUCTIVE_APPROVAL='<exact approved command or effect>'
GIT_RECOVERY_CHECKPOINT='<backup branch, tag, stash, or commit ref>'
```

`ALLOW_DESTRUCTIVE_GIT=1` is a machine-readable marker; it does not replace the
chat approval requirement.

## Baseline Before Transformation

Before performing a bulk or mechanical transformation on a file that already
carries uncommitted changes, first commit or stash the pre-existing changes as
their own atomic unit. Examples include splitting one file into several,
reformatting, or large find-and-replace. Do not fold unrelated prior edits into
the transformation commit.

## Pre-Commit Review Protocol

Before committing:

1. Run `git status --short --branch`.
2. Inspect `git diff --cached`.
3. Inspect the unstaged diff for touched files.
4. Stage only explicit paths covered by `GIT_AGENT_OWNED_PATHS`.
5. Run relevant verification and `git diff --check`.
6. Confirm `git config --get core.hooksPath` is `.githooks`.

## Commit Message Format

Use:

```text
<type>(<scope>): <lowercase imperative subject>
```

Allowed types: `spec`, `evidence`, `verify`, `plan`, `docs`, `feat`, `fix`,
`refactor`, `test`, `chore`.

Allowed scopes:

- Two-digit phase scopes such as `20`.
- Task scopes such as `20-05`.
- Fixed domain scopes: `governance`, `planning`, `pinn`, `brutus`, `pipeline`,
  `spec`, `docs`, `ref`.

Inserted phases use task-style scope, for example `20-05`. Do not use `20.5`,
`20-5`, or `20_5` in commit scopes.

The subject starts lowercase, uses imperative voice, is 80 characters or fewer,
has no trailing period, and does not contain markdown ticks, quotes, or
semicolon-chained changes.

## Required Bodies

A body is required for `spec`, `evidence`, `verify`, and `plan` commits;
commits touching multiple files; commits touching `pinn_instruction/`,
`.planning/`, framework specs, or governance instructions.

For spec or adjudication work, the body must cite grounding sources or user
decisions when relevant. The body should explain why the commit exists, not
repeat the diff.

## Auditable Verification Claims

When a commit asserts a verifiable invariant, record the supporting evidence
durably. Examples include byte-for-byte preservation, hash matches, line counts,
or unit counts. Commit the per-unit hashes or counts alongside the change, or
reference them from a committed path, so later reviewers can re-derive the
claim.

## Agent Attribution

Agent-authored or materially agent-assisted commits must include
`Agent-Assisted-By: <agent/tool/model>` or a valid `Co-Authored-By:` trailer.
Agents must use `scripts/agent-commit`; raw agent `git commit` commands are
blocked by lifecycle hooks.

## Hook Enforcement

Run `scripts/setup-git-hooks.sh` after cloning or after changing hook files.
Do not use `--no-verify`, `core.hooksPath=/dev/null`, or equivalent bypasses
without explicit user approval.

Current enforcement includes:

- `.githooks/commit-msg`: validates message format, body requirements, agent
  attribution, and agent-owned staged paths.
- `.githooks/pre-commit`: blocks generated, scratch, and oversized staged
  artifacts.
- `.githooks/pre-push`: blocks direct pushes to protected branches and preserves
  Git LFS pre-push behavior.
- `.githooks/pre-rebase`: requires destructive-operation approval markers.
- Agent lifecycle hooks: block raw commits, hook bypasses, broad staging, and
  unapproved destructive commands before shell execution.

## Branches, Tags, And PRs

Do not push directly from protected branches `master`, `main`, or
`milestone/*`. Milestone branches are local integration branches. Agents may
commit locally on a milestone branch when authorized by the task, but remote
publication should use feature/review branches or explicit user-controlled
integration.

Prefer feature branches for PR work. Create recovery branches or tags before
destructive operations when loss is possible.

## Recovery

If work appears lost, perform read-only forensics first:

- `git reflog`
- `git fsck`
- `git stash list`
- `git worktree list`

Present recovery options before changing state.

## Docs Plan-Review-Fix Lifecycle

These rules govern Git commit behavior for the iterative loop run on
implementation plans and review reports under `docs/`: plan execution,
independent review, fix-plan, and remediation. Rules attach to the action
performed, not to which agent performs it. One agent may perform several
actions, but each follows its own rule and gets its own commit.

File retention, naming, archive, and review closeout are governed by
`docs/README.md`; this section governs only commit behavior and defers to
`docs/README.md` wherever the two meet.

**Executing a plan.** Commit the executed work as normal typed commits by
domain. Record execution provenance in the plan file's frontmatter per
`docs/README.md` (`execution_status`, `executed_at` with date, time, and
timezone, and `review_status`). Close each pass with a dedicated commit that
updates those keys and carries the trailers `Plan-Execution: first-pass` and
`Plan-Source: <plan path>` alongside the mandatory attribution trailer. Keep
this commit separate from the work commits. Re-executing after remediation uses
`remediation-pass-N` in both the status and the trailer. Do not fold
pre-existing uncommitted changes into execution commits.

**Reviewing an execution.** Commit a review report as `verify(<scope>)`, or
`docs(<scope>)` for non-finding narrative. A body is required for `verify`.
Naming and location follow `docs/README.md`. A report is kept, never
deleted-and-recreated: superseding an older report sets its frontmatter
`status: superseded` in an atomic commit, and the new report is its own commit.
Archive or deletion follows the approval-gated lifecycle in `docs/README.md`.
If the reviewing agent also finishes or fixes work, commit the report separately
from the fixes. After review, update the reviewed plan's `review_status`.

**Authoring a fix or remediation plan.** Commit it as its own `plan(<scope>)`
commit, separate from any execution or report commit. When later executed, it
follows the Executing a plan rules with a `remediation-pass-N` marker.

**Applying fixes.** Commit fixes as normal typed commits by domain, separate
from the report that identified them and the plan that scheduled them.

## Presence & overlap awareness (advisory)

At session start you are shown a **roster** of other live sessions: each peer's
short id, worktree/branch, one-line task summary, derived write set, and
heartbeat age. After your first prompt, announce your own task so peers can see
it:

    scripts/agent-presence announce "<one-line task summary>" --areas path/a,path/b

`--areas` is your **intended write set** as explicit paths (never inferred from
the summary). Announcing declares those areas on the claims board; it respects
peers' existing claims and never seizes them. Read-only files need no area.

**Before working, classify overlap with live peers and resolve it yourself where you can. Escalating to a human is the fallback for genuine deadlock, not the default — if you can resolve it autonomously, do.**

- **HIGH — proceed autonomously.** Disjoint work, or a conflict you can dissolve
  yourself: narrow your own write set to dodge a peer's claimed areas, then go. No
  human, no waiting.
- **MEDIUM — self-mitigate, then proceed.** A real but workable interaction (you
  both touch one file in sequence, or your scopes are related). *Act on a
  mitigation yourself* — sequence your edits after the peer's, re-scope to a
  disjoint slice, or take a non-overlapping portion — and record what you did in
  your `announce` summary so the roster reflects it. There is no synchronous peer
  to "acknowledge"; do not idle waiting for one. Surface to a human only if no
  self-mitigation exists.
- **LOW — stand down autonomously; surface only if unresolved.** This is likely
  the *same task* as a live peer (S1). Do **not** proceed on the overlapping work.
  Prefer an autonomous resolution: defer to the peer and pick up the next
  unclaimed task, or re-scope to clearly different work. Surface to a human
  **only** when you cannot resolve it yourself — e.g. both efforts look canonical
  and choosing which proceeds is a priority call you don't own.

Two axes drive the call — **write-overlap** and **semantic relationship**.
Compute write-overlap against the live board, but **run the check under your own
session identity** so your own announced areas aren't mistaken for a peer's
(`agent_claims.find_conflict` excludes only the *caller's* `who`; a plain shell
resolves a different `who`, so it would flag your own claims):

    AGENT_CLAIM_WHO="session:$CLAUDE_CODE_SESSION_ID" python3 scripts/git_policy/agent_claims.py check <path>

The roster above already excludes your session, so it is the primary surface;
use `check` only for an authoritative per-path verdict. Mapping the two axes:

| Planned writes vs. live peers | Unrelated | Related (S2) | Same task (S1) |
|---|---|---|---|
| No write-overlap | proceed | MEDIUM — self-mitigate (re-scope), then proceed | LOW — stand down / re-scope; surface only if unresolved |
| Write-overlap | MEDIUM — sequence yourself (Class B) | MEDIUM → LOW — sequence or re-scope; surface only if stuck | LOW — stand down / re-scope; surface only if unresolved |

Conflict classes: **A1/A2** same-file contention (handled by the claim guard +
commit-time net); **B** shared-file-in-sequence; **C** branch/worktree
structural; **D** read-only sharing (always proceed); **S1** task duplication
(same task, possibly different files — the case this system exists to catch);
**S2** scope overlap (related tasks that may interfere).

**Conservative tie-breaks:** if you cannot *confidently* place a situation in
the proceed cell, treat it as at least MEDIUM (self-mitigate before proceeding).
**Any** whiff of S1 → treat as LOW and **stand down from the duplicate work**,
regardless of file overlap — duplicated effort is the failure to prevent.
Standing down means redirecting yourself to other useful work, not halting for a
human; escalate only when you cannot find a safe autonomous path.

**Cross-worktree weighting:** peers in other worktrees stay visible but marked.
Same-worktree/same-branch peers carry the highest weight for *file-collision*
risk; *semantic duplication* (S1/S2) is weighted across **all** peers, including
cross-worktree ones.

**Subagents:** the unit of presence is the top-level session. Agent-tool
subagents do not register, announce, or appear in the roster.

This layer is **advisory**. No verdict here blocks an edit or a commit; the
commit-time owned-paths net in `scripts/agent-commit` is the only hard backstop.
