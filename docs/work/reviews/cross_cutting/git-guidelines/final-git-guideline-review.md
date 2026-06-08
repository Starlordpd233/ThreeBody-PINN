# Final Git Guideline Review and Consolidation

Date: 2026-06-05
Status: Draft for user review
Scope: Project-specific Git behavior for human users and AI coding agents

## Executive Recommendation

Use a layered enforcement model:

1. Root `AGENTS.md` contains the short mandatory Git protocol. In this repo,
   `CLAUDE.md` and `GEMINI.md` are symlinks to `AGENTS.md`, and Codex also
   discovers root `AGENTS.md`, so this is the strongest shared instruction
   surface.
2. A full reference document, recommended path `docs/git-guidelines.md`,
   contains examples, gray areas, hook behavior, and rationale. Do not make
   `.planning/codebase/CONVENTIONS.md` the canonical enforcement surface; it is
   useful historical analysis, but agents do not reliably load it.
3. A tracked Git hook directory, recommended path `.githooks/`, provides the
   commit-time checks. Add `scripts/setup-git-hooks.sh` to run:
   `git config core.hooksPath .githooks`.
4. Agent lifecycle hooks add a second guardrail for agent tool use:
   `.claude/settings.json` for Claude Code and `.codex/hooks.json` for Codex.
   These should block raw bypass patterns such as `git commit --no-verify`,
   `git -c core.hooksPath=/dev/null ...`, destructive Git commands without
   confirmation, and raw `git commit` if the project adopts an agent commit
   wrapper.
5. Optional GitHub Actions or branch protection should check commit policy on
   PRs and milestone merges, because local Git hooks can be bypassed.

The key design shift: instructions tell agents what to do; hooks make failure
harder at the moment of commit. The guideline should not claim that
instructions alone enforce anything.

## Official Documentation Notes

- Claude Code docs say `CLAUDE.md` files are loaded as context, not enforced
  configuration, and recommend hooks when an action must be blocked:
  <https://code.claude.com/docs/en/memory>.
- Claude Code docs support project `CLAUDE.md`, symlinking/importing
  `AGENTS.md`, `.claude/rules/`, and project settings/hooks:
  <https://code.claude.com/docs/en/memory>,
  <https://code.claude.com/docs/en/settings>,
  <https://code.claude.com/docs/en/hooks>.
- Codex official manual documents root-to-current-directory `AGENTS.md`
  discovery, a default combined instruction limit, project-local `.codex/`
  hooks, and hook trust review:
  <https://developers.openai.com/codex/codex-manual.md>.
- Git official docs support `pre-commit` and `commit-msg` hooks and explain
  that `core.hooksPath` can point Git to a tracked hook directory:
  <https://git-scm.com/docs/githooks>,
  <https://git-scm.com/docs/git-config#Documentation/git-config.txt-corehooksPath>.
- Git docs also note that `pre-commit` and `commit-msg` can be bypassed with
  `--no-verify`, so the project guideline must explicitly forbid bypassing
  hooks except with direct user approval.

## Review of Design Idea 1

Strong parts to keep:

- Good project-level lifecycle coverage: branch strategy, milestone branches,
  recovery checkpoints, generated artifact rules, and merge/PR conventions.
- Correct instinct that destructive operations require confirmation and a
  recoverable checkpoint.
- Good distinction between audit artifacts that belong in Git and bulky
  generated data/checkpoints/logs that do not.
- The branch model fits the current repo: `master` as stable history and
  `milestone/vX.Y` as the long-running milestone work branch.

Problems to fix:

- It places the main guideline in `.planning/codebase/CONVENTIONS.md`. That is
  too easy for agents to miss. Use `AGENTS.md` for mandatory rules and a
  regular docs reference for detail.
- It is still written like a brainstorm artifact, with unresolved questions.
  The final guideline should be imperative, not interrogative.
- Some text appears corrupted or typo-heavy, which would weaken the authority
  of the final policy.
- It has no machine enforcement layer.
- Its scope examples are inconsistent: `(17-01)` and `(15.1-03)` should be
  normalized to a single two-digit phase/subtask form such as `(20-05)`.

## Review of Commit Convention Design

Strong parts to keep:

- Strongest commit-message design: type taxonomy, restricted `docs`, fixed
  scope categories, body requirements, and prohibited patterns.
- Good agent-centered style: decision trees and fixed enumerations are easier
  for agents to follow than prose-only conventions.
- Good forensic motivation: scope fragmentation, overuse of `docs`, missing
  bodies, and inconsistent AI attribution are real auditability problems.
- Good atomicity language: one logical change per commit, split unrelated
  concerns, and use body text for cross-domain causal links.

Problems to fix:

- "No hooks" conflicts with the user's explicit enforcement goal. Keep the
  docs, but add tracked Git hooks and agent lifecycle hooks.
- `.claude/rules/commit-convention.md` is useful for Claude Code, but it is
  not a shared enforcement surface for Codex/Gemini. The shared rule must live
  in `AGENTS.md`.
- It should not rely on an unspecified default Co-Authored-By trailer across
  all agents. The final rule should say not to remove tool-generated trailers,
  and should define an explicit project trailer policy for agents.
- Its capitalization rule conflicts with existing project history and
  Conventional Commits style used in this repo. Prefer lowercase imperative
  subjects after the colon unless the user intentionally wants a breaking
  style change.
- Phase checkpoint tags before every phase may be useful for v1.4-style
  adjudication work, but should not be mandatory for every future small task.
  Make them milestone/phase-run checkpoints, not generic commit policy.

## Consolidated Final Guideline

### 1. Trigger

These rules apply whenever an agent performs work that may need a Git commit,
including documentation, planning artifacts, framework specs, review reports,
code, tests, cleanup, or generated audit artifacts.

Agents must not wait until the final commit command to think about Git. They
must follow the Git protocol from task start through commit completion.

### 2. Session Start and Branch Awareness

At the start of any task that may produce a commit, run and surface:

```bash
git status --short --branch
```

The agent must explicitly report:

- current branch
- whether the branch is ahead/behind
- existing modified, deleted, or untracked files
- which existing changes appear unrelated to the requested task

Agents must treat existing changes as user-owned unless they created them in
the current task.

Pause and ask before proceeding when:

- the branch is a red-flag branch: `backup/*`, `recovery/*`, `wip/*`,
  `experiment/*`, `tmp/*`
- the branch is not `master`, `milestone/vX.Y`, or an explicitly requested
  feature/worktree branch
- the work requires switching branches, rebasing, resetting, cleaning, force
  pushing, deleting refs, dropping stashes, or removing tracked paths
- the agent cannot explain exactly what an operation will affect

### 3. Destructive Operations

Before any destructive operation, the agent must:

1. Stop.
2. Explain the exact command and what it can discard or rewrite.
3. Create a recovery checkpoint when appropriate:
   `backup/<context>-<YYYYMMDD>` branch or `recovery/<context>-<YYYYMMDD>` tag.
4. Wait for explicit user confirmation.

Destructive operations include:

- `git reset --hard`
- `git clean -f`, `git clean -fd`, or stronger variants
- `git branch -D`
- `git rebase`
- `git push --force` or `--force-with-lease`
- `git stash drop` or `git stash clear`
- `rm -rf` on tracked paths
- any command that changes branch refs, commit history, stashes, tags, or
  tracked worktree state in a way that may discard work

### 4. What Belongs in Git

Commit these when they are part of the task:

- `.planning/` state, plans, context, gap registers, ledgers, and roadmap
  updates
- `docs/findings/` review reports and analysis that form an audit trail
- framework spec edits under `pinn_instruction/`
- evidence packets, issue-ledger updates, and acceptance-check results
- source code, tests, scripts, and project documentation

Do not commit these without explicit user approval:

- `.h5`, `.npy`, `.npz`, `.mat`
- model checkpoints: `.pt`, `.pth`, `.ckpt`
- training logs, run outputs, and large simulation payloads
- LaTeX build products: `.aux`, `.pdf`, `.log`, `.out`, `.toc`
- scratchpads, temp files, personal notes, and transient agent outputs

Review report rule: commit reports that are part of the milestone or project
audit trail; do not commit private scratch analysis.

### 5. Atomic Commit Cadence

Each commit must represent one logical, reversible unit of work and leave the
project in a coherent state.

Split commits when:

- the subject cannot describe all changes clearly
- the staged set mixes unrelated features, fixes, docs, or review outputs
- the commit mixes refactoring with behavior changes
- files in unrelated domains are touched without a direct causal link

Combine changes only when they are meaningless or misleading apart, such as a
spec edit plus the directly corresponding planning-state update.

For v1.4-style adjudication flows, prefer this sequence when all three
artifacts exist:

1. `evidence(NN): ...`
2. `spec(NN): ...`
3. `verify(NN): ...`

No `wip` commits.

### 6. Pre-Commit Review Protocol

Before committing, the agent must:

1. Run `git status --short`.
2. Inspect unstaged and staged changes with `git diff` and `git diff --cached`
   or equivalent targeted commands.
3. Stage explicit paths for the task. Avoid broad `git add -A` unless the
   agent has just reviewed the complete status and every path belongs in the
   commit.
4. Run the relevant verification for the touched files, or state clearly why
   verification was not run.
5. Confirm `git config --get core.hooksPath` is `.githooks`, or run the project
   setup script before committing. If hooks are unavailable, stop and ask the
   user whether to proceed without hook enforcement.

### 7. Commit Message Format

Use:

```text
<type>(<scope>): <lowercase imperative subject>

[body when required]

[trailers]
```

Subject rules:

- 72 characters preferred, 80 hard maximum
- lowercase imperative verb after the colon, matching current project history:
  `add`, `fix`, `record`, `document`, `verify`
- no trailing period
- no Markdown, backticks, quotes, semicolon chains, or multiple unrelated
  clauses

Allowed types:

- `spec`: framework spec edits under `pinn_instruction/` or cross-phase spec
  artifacts
- `evidence`: evidence packets, issue-ledger adjudication, source-material
  analysis
- `verify`: acceptance checks, validation results, audit pass/fail evidence
- `plan`: phase plans, implementation plans, remediation plans
- `docs`: general docs, governance docs, README, cleanup/archive, or docs that
  do not fit the project-specific types above
- `feat`: new source behavior or user-facing capability
- `fix`: bug fix or correctness repair
- `refactor`: restructuring without behavior/spec change
- `test`: test-only additions or changes
- `chore`: mechanical maintenance, dependencies, config, ignore rules

Forbidden types:

- `wip`
- `phase`
- ad-hoc types not listed above

Allowed scopes:

- phase scope: two digits, e.g. `(17)`, `(20)`
- phase subtask scope: two digits plus two-digit task, e.g. `(20-05)`
- fixed domain scope:
  - `(governance)`: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/`,
    `.codex/`, `.githooks/`, governance policies
  - `(planning)`: cross-phase `.planning/` state
  - `(pinn)`: `pinn/`
  - `(brutus)`: `brutus_Newton-main/`
  - `(pipeline)`: `simulation_data/`
  - `(spec)`: cross-phase spec work not tied to one phase
  - `(docs)`: general `docs/` changes not tied to one phase
  - `(ref)`: `reference-code/`

Forbidden scopes:

- session names, model names, line numbers, math expressions, decision IDs,
  or ad-hoc phrases
- examples: `(quick-260320-ssi)`, `(phase-20)`, `(20.5)`, `(D-58)`,
  `(claude)`, `(line-655)`

Commit body is required for:

- `spec`, `evidence`, `verify`, and `plan`
- any multi-file commit
- any governance change
- any commit touching `pinn_instruction/`, `.planning/`, or framework LaTeX

Body content must explain why the commit exists and cite grounding sources or
user decisions for spec/adjudication work. The body should not repeat the diff.

AI attribution:

- Do not remove tool-generated `Co-Authored-By:` trailers.
- Agent-authored or agent-substantially-assisted commits must include either a
  valid `Co-Authored-By:` trailer supplied/configured by the tool or a project
  trailer such as `Agent-Assisted-By: <agent/tool/model>`.
- Do not fabricate a coauthor email. If no valid coauthor identity is
  configured, use the project trailer.

### 8. Branches, Tags, and PRs

Branch model:

- `master`: stable project history
- `milestone/vX.Y`: long-running milestone work
- feature/topic branches: short-lived, merge back to the active milestone
  branch unless the user says otherwise
- red-flag branches: `backup/*`, `recovery/*`, `wip/*`, `experiment/*`,
  `tmp/*`

Milestone completion:

- merge `milestone/vX.Y` into `master` with a merge commit, not squash, unless
  the user explicitly chooses otherwise
- tag milestone completion with an annotated tag such as `v1.4.0`
- preserve the milestone branch for reference unless the user approves deletion

Recovery tags:

- use `recovery/<context>-<YYYYMMDD>` before risky operations
- use backup branches only for short-lived recovery and convert to tags when
  the backup no longer needs active branch semantics

PR conventions when PRs are used:

- PR title follows the same type/scope convention
- preserve atomic commits for adjudication workflows
- squash only trivial fixup commits, with user approval when auditability
  matters

### 9. Hook Enforcement

Tracked hook directory:

- Create `.githooks/commit-msg` to validate message format, type, scope,
  subject length, body requirements, and prohibited patterns.
- Create `.githooks/pre-commit` to block staged bulky generated artifacts and
  obvious accidental scratch files.
- Create `.githooks/pre-rebase` or equivalent agent hook to block rebasing
  milestone/master without confirmation.
- Create `.githooks/pre-push` to preserve Git LFS pre-push behavior and block
  direct/force pushes to protected branches unless the user confirms.
- Add `scripts/setup-git-hooks.sh` to configure `core.hooksPath`.

Important: this repo currently has Git LFS hooks in `.git/hooks`. If the
project sets `core.hooksPath` to `.githooks`, the tracked hooks must call the
equivalent Git LFS hooks where needed, especially `git lfs pre-push "$@"`.

Agent lifecycle hooks:

- Claude Code: use project `.claude/settings.json` hooks for shared project
  behavior. A `PreToolUse` hook can deny dangerous Bash commands before they
  run.
- Codex: use project `.codex/hooks.json` or `.codex/config.toml` for
  project-local hooks. Codex requires project-local hooks to be reviewed and
  trusted before they run.
- Both agents should block or ask for confirmation on:
  - `git commit --no-verify`
  - `git -c core.hooksPath=/dev/null ...`
  - `git reset --hard`
  - `git clean -f`
  - `git branch -D`
  - `git rebase`
  - `git push --force`
  - raw `git commit` if the project adopts a required `scripts/agent-commit`
    wrapper

Git hooks are the cross-agent enforcement layer. Agent lifecycle hooks are
useful defense in depth, but should not be the only enforcement mechanism.

### 10. Recommended `AGENTS.md` Insert

Add this compact section after the existing "Git Branch Awareness &
Destructive Operations" section:

```markdown
## CRITICAL GOVERNANCE: Git Commit Protocol

These rules apply whenever a task may require a Git commit.

At task start, run and surface `git status --short --branch`. Report current
branch, ahead/behind state, and existing modified/deleted/untracked files.
Treat existing changes as user-owned unless you created them in the current
task.

Before committing, inspect `git diff` and `git diff --cached`, stage only
task-relevant paths, run relevant verification, and confirm
`git config --get core.hooksPath` is `.githooks`. If hooks are not installed,
run `scripts/setup-git-hooks.sh` or stop and ask the user whether to proceed.

Do not bypass hooks with `--no-verify` or `core.hooksPath=/dev/null` unless the
user explicitly approves that exact bypass.

Use one logical commit per reversible unit of work. No `wip` commits. Split
evidence, spec, and verification work when they are distinct artifacts.

Commit message format:

`<type>(<scope>): <lowercase imperative subject>`

Allowed types: `spec`, `evidence`, `verify`, `plan`, `docs`, `feat`, `fix`,
`refactor`, `test`, `chore`.

Allowed scopes: two-digit phase `(20)`, phase task `(20-05)`, or one of
`(governance)`, `(planning)`, `(pinn)`, `(brutus)`, `(pipeline)`, `(spec)`,
`(docs)`, `(ref)`.

Subject: lowercase imperative, 72 characters preferred, 80 maximum, no trailing
period, no Markdown/backticks/quotes, no semicolon chains.

Body required for `spec`, `evidence`, `verify`, `plan`, multi-file commits,
governance changes, and commits touching `pinn_instruction/`, `.planning/`, or
framework LaTeX. Body explains why and cites grounding/user decision sources
for spec/adjudication work.

Agent-authored or agent-assisted commits must keep valid tool-generated
`Co-Authored-By:` trailers or include `Agent-Assisted-By: <agent/tool/model>`.
Do not fabricate coauthor emails.
```

## Implementation Order

1. Add the compact protocol to `AGENTS.md`.
2. Add `docs/git-guidelines.md` as the full reference, using this document as
   the source.
3. Add `.githooks/commit-msg`, `.githooks/pre-commit`, and
   `.githooks/pre-push`, with Git LFS preservation.
4. Add `scripts/setup-git-hooks.sh`.
5. Add optional `.claude/settings.json` and `.codex/hooks.json` lifecycle hooks
   to block bypass/destructive agent commands.
6. Optionally add a GitHub Action for PR/milestone commit-message validation.

## One Open Policy Choice

The only choice I would ask the user to settle before implementation:

Should AI attribution be required for every commit in this repo after adoption,
or only for commits where an agent materially contributed?

Recommended answer: only require it for agent-authored or agent-assisted
commits, but configure agent lifecycle hooks/wrappers so agents cannot omit it.
