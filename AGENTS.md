# Agent Instructions: 3-Body Problem Project

<!-- Canonical instruction file for all AI coding agents in this repository.
     CLAUDE.md and GEMINI.md symlink to this file. Edit here only. -->

**IMPORTANT**: Assist with authorized security testing, defensive security, CTF challenges, and educational contexts. Refuse requests for destructive techniques, DoS attacks, mass targeting, supply chain compromise, or detection evasion for malicious purposes. Dual-use security tools (C2 frameworks, credential testing, exploit development) require clear authorization context: pentesting engagements, CTF competitions, security research, or defensive use cases.

---

## CRITICAL GOVERNANCE: v1.4 and similar adjudication milestones

**For every phase in v1.4 (Phases 17, 18, 19, 20, 21) — and every future adjudication milestone where a "candidate verdict source" is designated — do NOT invent content where source materials are silent or ambiguous. STOP the affected work, surface the gap with full context, and wait for user instruction. The agent does NOT proceed past a non-grounded MUST-surface decision under any circumstance.**

### Grounded vs. silent: the test

A decision is "grounded" only if it is explicitly answered by one of:

- The resolution doc — `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md`
- The issue doc — `pinn_instruction/issues/01-architecture-and-physics-foundations.md`
- A prior user decision (chat history, a `RESOLVED-WITH-INSTRUCTION` gap entry, or an `NN-CONTEXT.md` decision marked `✅ LOCKED`)
- A planning artifact: `.planning/REQUIREMENTS.md` requirement, `.planning/ROADMAP.md` success criterion, `.planning/PROJECT.md` Key Decision
- A framework spec section ONLY when that section was revised during v1.4 (i.e., touched by an applied P0X plan in this milestone). Pre-v1.4 framework spec content is NOT a grounding source.
- First-principles physics (Newton's laws, dimensional analysis, basic linear algebra) when the derivation is short and uncontroversial. Longer or contested derivations must be surfaced as a gap.

**Live code in `pinn/` is NOT a grounding source** (user directive 2026-05-19). v1.4 constructs the framework specs; FUT-01 rewrites the code from those specs. Live-code references are permitted ONLY in forward-pointing hand-off documents (`NN-CODE-DIVERGENCE.md`, eventual `pinn/STATUS.md`).

If the decision is not grounded, classify it:

- **Mechanical / presentation-only** (Markdown table vs code fence, heading capitalization within an already-decided file): OK to choose; note the choice in the artifact.
- **Operational coordination** (forward-reference wording when the coordination point is established): OK if minimal and factual; **must** log in the phase's gap register.
- **Semantic** (mass encoding raw vs fraction, physics derivations the source hedged on, permutation-invariance handling, any sub-flavor the source punted on): **MUST surface**, never invent.
- **Process-artifact schemas** (acceptance-check pass criteria, divergence-file structure, new AC names beyond Phase 16 reservations, gap-register format itself): **MUST surface**, never invent.
- **Cross-phase reframing** (e.g., "M5 reframed as metadata-only under Jacobi IC"): **MUST surface** — changes downstream phase scope.

### STOP Protocol — when a gap is detected

1. **STOP the affected work immediately.** Do not continue editing files, generating plans, or executing tasks that depend on the gap's resolution. Independent work may continue. **There is no exception. "I'll make a reasonable choice and note it" is not allowed.**

2. **Verify the agent understands the decision space.** Before recording a gap, confirm YES to all three:
   - Can the agent articulate the mathematics / physics / engineering principles at stake?
   - Can the agent explain why each candidate resolution would have different downstream consequences?
   - Can the agent identify which source materials it consulted and why they did not answer the question?

   If any answer is "no", do NOT record a gap. Surface instead: *"I do not understand X well enough to assess whether this is a gap. Please explain Y before I proceed."* Gaps recorded out of ignorance are worse than none — they mislead the user and waste attention.

3. **Record the gap** in the phase-local gap register (`.planning/phases/NN-*/NN-GAPS.md`) using all required fields:
   - **Decision point** — what is being decided, in one or two sentences.
   - **Where in artifact** — file and section/line where the gap surfaced.
   - **Task context** — specific task being performed when the gap was hit.
   - **Classification** — one of: semantic / operational coordination / process-artifact schema / cross-phase reframing.
   - **Source silence** — citations to each consulted source and why it did not answer the question (file:line).
   - **Mathematical / engineering grounding** — the agent's articulation of the math, physics, or engineering principles at stake. Must demonstrate understanding of why this gap is consequential, not just that the source is silent. If the agent cannot produce this, it must NOT record the gap — return to step 2 and surface an understanding-question instead.
   - **Agent was tempted to** — what the agent would have decided + rationale.
   - **What the user needs to decide** — the question, framed as concrete options (A/B/C/...).
   - **Confidence of impact** — HIGH / MEDIUM / LOW with one-sentence reason.
   - **Status** — `OPEN` initially.
   - **Resolution note** — empty until user provides instruction.

4. **Update the milestone-wide index** at `.planning/milestones/v1.4-GAPS.md` with the new gap.

5. **Surface to the user** via the active workflow channel. Halted work stays halted until the user provides instruction. Once instruction arrives, update Status to `RESOLVED-WITH-INSTRUCTION` (or `DEFERRED`), fill `Resolution note`, and resume.

### Scope boundary

- A gap encountered during Phase NN work that is *actually about* a different phase's content goes into **that phase's** `MM-GAPS.md` (or into `v1.4-GAPS.md` if it spans multiple phases).
- Subagents do not write to gap registers directly — they return findings to the parent agent, which decides whether the finding is a gap and logs it.

### Why

User does not trust the agent to make spec-engineering or physics-adjudication calls without explicit grounding. The designated "candidate verdict source" (`ctl_pinn_resolution.md` for v1.4) is the *candidate*, not authority — agent transcribes what is explicit, never fills white space. Cost of asking is small; cost of silently inventing is irreparable spec drift across phases.

**Issued by user 2026-05-18; strengthened with STOP protocol + math/engineering grounding requirement 2026-05-19.** Overrides any default behavior to "make a reasonable assumption and proceed." Scope: v1.4 (Phases 17–21) and similar future adjudication milestones unless explicitly waived per milestone.

---

## CRITICAL GOVERNANCE: Git Branch Awareness & Destructive-Operation Protocol

**Before any file mutation, before any Git operation that could discard work, and at every session start, the agent MUST surface the current Git state to the user in plain text and obtain explicit confirmation before proceeding on any non-master branch or any branch whose name signals risk. Destructive Git operations require a four-step pre-flight (enumerate → audit → typed-echo confirm → checkpoint) with no exceptions. The agent does NOT silently change branch context, silently discard work, or silently rewrite history under any circumstance.**

### Branch & worktree surfacing — always on

At every session start, AND before any file mutation, AND before any Git operation listed in the destructive-operation section below, the agent MUST run and surface in plain text:

- `git status --short --branch`
- `git branch --show-current`
- `git worktree list`
- `git stash list` (only if non-empty)

Surface verbatim in the active workflow channel so the user can read it without expanding a tool block. Example:
> Current Git state: branch `codex/scs-gate-correction` (NOT master), primary worktree `<home>/Desktop/3_body_problem`, 2 stashes, 3 modified files. Confirm before I proceed.

**Red-flag branch tokens — automatic STOP.** If the current branch name contains any of `backup`, `recovery`, `scratch`, `wip`, `experiment`, `archive`, `correction-`, `gate-`, `fix-`, `hotfix-`, `tmp`, `temp`, OR matches a dated suffix pattern (`-YYYYMMDD`, `-YYYY-MM-DD`, `_YYYYMMDD`, trailing 8+ hex chars `-[0-9a-f]{8,}`), the agent invokes the **STOP Protocol** before any file mutation. Operating from inside any path under `.claude/worktrees/`, `.git/worktrees/`, or any non-primary path returned by `git worktree list` triggers the same STOP regardless of branch name.

**Re-confirmation requirement.** Branch state is surfaced at session start AND before each new file mutation — not once-per-conversation. The SCSGATE incident (2026-05-13 to 2026-05-18) was caused by five days of work on a feature branch the agent surfaced once early and never re-confirmed; the user assumed master throughout.

### Destructive-operation pre-flight

**This list is illustrative, not exhaustive. ANY operation whose effect can permanently discard committed work, working-tree changes, branch refs, stashes, tags, remote refs, or reachable history triggers the pre-flight protocol — whether the specific command appears below or not.**

**Forbidden without four-step pre-flight:**

- **Reset / restore / discard:** `git reset --hard`, `git reset --keep`, `git reset --merge`, `git reset --soft` (when discarding subsequent commits), `git restore <path>` (when discarding working-tree changes), `git restore --source=<rev> --staged --worktree`, `git checkout .`, `git checkout -- <path>`, `git checkout-index --force`.
- **Clean:** `git clean -f`, `git clean -fd`, `git clean -fx`, `git clean -fX`.
- **Branch / ref deletion:** `git branch -D`, `git branch --delete --force`, `git update-ref -d <ref>`, `git symbolic-ref` reassignment of `HEAD`, `git switch -C <existing-branch>`, `git tag -d`, `git tag -f` (overwrite).
- **History rewrite:** `git rebase` of pushed history (any form), `git rebase -i`, `git rebase --onto`, `git commit --amend` of pushed commits, `git filter-branch`, `git filter-repo`, `git replace`, `git reflog delete`, `git reflog expire`, `git reflog expire --expire-unreachable --all`.
- **Force push / remote deletion:** `git push --force`, `git push -f`, `git push --force-with-lease` (safer but still triggers pre-flight), `git push --delete <branch>`, `git push origin :<branch>`, `git remote remove`.
- **Worktree / stash / submodule:** `git worktree remove`, `git worktree prune`, `git stash drop`, `git stash clear`, `git stash pop` when conflicts could discard the stash, `git submodule deinit -f`, `git submodule update --force`.
- **Merge variants that silently drop content:** `git merge -X theirs`, `git merge -s ours`, `git merge --squash` when discarding individual commits, `git merge --abort`, `git rebase --abort`, `git cherry-pick --abort` when partial progress would be lost.
- **GC / pruning:** `git gc --prune=now`, `git gc --aggressive --prune=now`, `git notes prune`, `git lfs prune`.
- **Sparse / view-altering:** `git sparse-checkout set`, `git sparse-checkout reapply` when tracked files would be hidden from subsequent operations.
- **File-level on tracked paths:** `rm -rf` on tracked paths, `find ... -delete` on tracked paths, `> tracked_file` truncation, `truncate -s 0 tracked_file`, `mv tracked_file <discard-location>`.
- **Compound commands:** `A && B`, `A || B`, `A; B`, shell functions, aliases, subshells, `eval`, heredocs, scripts where any reachable B is destructive — pre-flight triggers on the **compound**, not on B in isolation.

**Session-context-changing operations — surface, do NOT block.** Not destructive per se but bypass branch awareness when unsurfaced: `git checkout <branch>` (especially with dirty working tree), `git switch <branch>`, `git switch --detach`, `git checkout <sha>` (detached HEAD), `git worktree add`. Each invokes the Section 1 surfacing requirement BEFORE and AFTER the operation. The SCSGATE incident's root cause was a non-destructive checkout that was not surfaced.

**The four-step pre-flight — every destructive operation, no exceptions:**

1. **Enumerate** — list every file, commit (SHA + subject), branch ref, tag, stash, and remote ref that the operation will discard or rewrite. If the agent cannot produce this list exhaustively, the operation does NOT run — return to the STOP Protocol.
2. **Audit** — run read-only checks on every other branch (`git branch -a`), worktree (`git worktree list`), stash (`git stash list`), and reflog (`git reflog --date=iso -n 50`) for related uncommitted or unreferenced work to preserve. Surface findings to the user.
3. **Typed-echo confirm** — obtain the user's **explicit typed confirmation that quotes the specific operation**. Plain "yes" / "go ahead" / "do it" / "sounds good" / "proceed" is INSUFFICIENT — the user MUST echo the destructive command or its target (example: "yes, reset codex/scs-gate-correction to a0ae902"). The operation does not run until this typed echo is received in the active workflow channel.
4. **Checkpoint** — create a recovery checkpoint immediately before the destructive op:
   - `git branch backup/<context>-<YYYYMMDD>` pointing at current HEAD of the branch about to be modified; AND
   - `git tag recovery/<context>-<YYYYMMDD>` pointing at the same; AND
   - if uncommitted changes exist, `git stash push -u -m "pre-<op> checkpoint <YYYYMMDD>"` BEFORE creating the branch/tag.
   - Recovery checkpoints created by this step are never targets of subsequent Section 2 operations within the same session without an independent four-step pre-flight.

### Recovery from suspected loss

When the user reports lost work, missing files, or unexpected branch state, the agent MUST perform read-only forensics FIRST before any restoration. **Bulk operations (`git reset --hard <recovery-sha>`, fast-forward merge of a recovery branch into master, `git checkout` of a recovery branch over a dirty working tree) are FORBIDDEN during recovery — selective recovery (`git cherry-pick`, `git checkout <sha> -- <path>`, partial file restoration) is the default.**

**Read-only forensics — run all, surface all:**

- `git reflog --date=iso --all -n 200`
- `git fsck --lost-found --unreachable --dangling`
- `git stash list` and `git stash show -p <each>`
- `git worktree list` and `git -C <each-worktree> status`
- `git branch -a --contains <suspected-lost-sha>` (for each candidate SHA from reflog)
- `git log --oneline --graph <branch>...master` for each candidate branch
- Inspect any `backup/*` or `recovery/*` refs created by prior pre-flights.

Surface a written reconstruction of the loss timeline AND a menu of selective-recovery options (A: cherry-pick commits X, Y, Z onto master; B: create new branch from recovery ref and PR; C: restore individual files via `git checkout <sha> -- <path>`) BEFORE any write operation. Wait for the user to pick.

**Bulk reset to a recovery ref is permitted ONLY when:** (a) the user explicitly requests bulk operation by name; AND (b) four-step pre-flight in Section 2 has been completed; AND (c) a fresh `backup/recovery-attempt-<YYYYMMDD>` branch has been created from the current pre-recovery HEAD; AND (d) every other branch with uncommitted divergence has been listed and the user has explicitly accepted those divergences will not be merged.

### Commit cadence & checkpoint discipline

- **Default cadence — commit at logical task boundaries**, not after every individual edit. A logical boundary is: completion of a plan task, completion of a coherent multi-file refactor, end of a session, or any point immediately before invoking a destructive operation.
- **Risk-elevated mode — auto-triggered, end-of-task commit cadence.** When the agent's current task touches ANY file under:
  - `pinn_instruction/` (all sub-paths)
  - `.planning/` (all sub-paths)
  - Any LaTeX framework spec file under `pinn_instruction/original_latex/`
  - Any file the user has explicitly flagged as high-cost in the active session

  The entire task's changes accumulate and commit as ONE atomic commit at task end. The risk-elevated commit MUST happen at task end, not deferred. A task that ends with an uncommitted working tree under risk-elevated paths is treated as a pre-destructive trigger if any subsequent destructive operation is proposed.

- **Before any destructive operation (Section 2), the working tree MUST be either committed, stashed-with-named-message, or explicitly accepted-as-discardable by the user in pre-flight step (3).** Uncommitted dirty state does NOT silently survive a destructive op.
- **Subagents MUST commit their work before returning control to the parent OR return a manifest of uncommitted files + the Git commands they executed.** A subagent returning "done" with a dirty working tree is treated as a pre-destructive trigger — the parent runs a checkpoint before any subsequent Section 2 operation.

### STOP Protocol — when branch state, destructive intent, or suspected loss is detected

When (a) red-flag branch tokens or non-primary worktree paths are detected, OR (b) a destructive operation is about to be invoked without complete pre-flight, OR (c) the user reports lost work, OR (d) any pre-flight sub-step cannot be completed exhaustively:

1. **STOP the affected work immediately.** Do not continue editing files, do not run the destructive op, do not attempt restoration. Read-only forensics may continue. **There is no exception. "This looks safe" is not allowed. "The user implicitly approved" is not allowed.**

2. **Verify the agent understands the Git state.** Confirm YES to all four:
   - Can the agent name the current branch AND the branch the user most likely expects to be on?
   - Can the agent name every file, commit, ref, stash, and remote ref that would be affected by the proposed operation?
   - Can the agent name every other branch, worktree, or stash that contains potentially-related work to preserve?
   - Can the agent explain how the current branch came to exist (which checkout, which session, which prior agent action)?

   If any answer is "no", do NOT propose an action. Surface instead: *"I do not have enough Git context to safely proceed. I see branch X, worktree Y, recent reflog Z. Please tell me which branch you expect to be on and what you want preserved before I do anything else."*

3. **Record the incident** in `.planning/incidents/git-incidents.md` (create the file lazily on first incident) using:
   - **Trigger** — what tripped the STOP (red-flag token, attempted destructive op, suspected loss report, pre-flight failure).
   - **Current Git state** — branch, worktree path, dirty files, stashes, last 10 reflog entries.
   - **Operation that would have run** — exact command (or `n/a — surfacing-only`).
   - **What would have been discarded** — exhaustive enumeration from pre-flight step (1), or `unknown — agent failed self-check` if applicable.
   - **Other-branch audit** — findings from pre-flight step (2).
   - **Agent's understanding** — output of step-2 self-check (each of the four questions, answered).
   - **Outcome** — `BLOCKED-AWAITING-USER` initially.
   - **Resolution note** — empty until user provides instruction.

4. **Update the milestone-wide gap index** at `.planning/milestones/v1.4-GAPS.md` (if an active milestone has one) with a one-line reference to the incident. If no active milestone has a gap index, skip this step.

5. **Surface to the user** with full pre-flight enumeration, self-check output, and explicit request for typed confirmation of the next step. Halted work stays halted until the user replies. Once instruction arrives, update Outcome to `RESOLVED-WITH-INSTRUCTION` or `DEFERRED`, fill `Resolution note`, and resume — including running pre-flight step (4) checkpoint before any destructive op the user authorized.

### Scope boundary

- **Subagents share the parent agent's working tree, Git index, refs, and reflog.** Every subagent is bound by every section of this block. The parent agent is responsible for: (a) ensuring spawned subagents have access to this block's content; (b) enumerating every Git command a returning subagent executed; (c) treating any uncommitted state returned by a subagent as a pre-destructive checkpoint trigger before the parent runs any Section 2 operation.
- **Worktrees count.** Operating from inside `.claude/worktrees/<anything>`, `.git/worktrees/<anything>`, or any non-primary path returned by `git worktree list` invokes the Section 1 surfacing requirement on every file mutation.
- **"Safer-sounding alternatives" do not bypass.** `--force-with-lease` requires the same pre-flight as `--force`. `--keep` and `--merge` require the same pre-flight as `--hard`. `restore` without `--source` requires the same pre-flight as `checkout -- <path>`. Lower-level commands (`update-ref`, `symbolic-ref`) that achieve the same effect inherit the pre-flight requirement.
- **Compound and indirect invocations count.** Running a destructive op inside `bash -c`, `eval`, a shell function, an alias, a script, or as the second clause of `A && B` / `A; B` triggers pre-flight on the compound.
- A Git incident that is also a v1.4-style adjudication gap is logged in BOTH `.planning/incidents/git-incidents.md` AND the relevant phase's `NN-GAPS.md`.

### Why

On 2026-05-13, an agent checked out from `master` to `codex/scs-gate-correction` and worked there for five days without ever re-surfacing the branch context to the user. On 2026-05-18 16:55:25, a `git reset` followed by a checkout to `codex/v1.4-phase16-recovery` and a fast-forward merge to master discarded valid work the user wanted to keep. The work is preserved on `codex/backup/scs-gate-correction-20260518` (14,339 insertions of divergence from master across 86 files) only because of the user's own intervention — not because the agent followed any branch-awareness or pre-flight discipline. The cost of asking "we're on branch X, not master — confirm?" is small; the cost of silently destroying days of spec work is irreparable.

**Issued by user 2026-05-19; covers branch awareness, destructive-operation pre-flight, recovery forensics, end-of-task commit cadence for risk-elevated paths, STOP Protocol with self-check, and subagent scope.** Overrides any default behavior to "run the Git command the user implicitly authorized" or "this operation looks safe enough to skip confirmation" or "I'll just make a reasonable choice and note it." Scope: every Git operation in this repository, every session, every agent and subagent, every worktree — unless explicitly waived per operation with typed-echo confirmation in the active workflow channel.

---

## Source of Truth

**Dataset spec and anomalies**: `simulation_data/Documentation/README.md`

**PINN framework specs** (authoritative for v1.4 and beyond):
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — CTL methodology, input-vector formulation, curriculum staging
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — network architecture, AD contract, output head
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` — IC sampling

**v1.3-era live code is NOT a grounding source** (user directive 2026-05-19): `pinn/data-processing-pipeline-full.py`, `pinn/basic_architecture.py`. These files are NOT evidence, NOT source-of-truth for any v1.4 spec decision. They may be referenced ONLY in forward-pointing FUT-01 hand-off documents (`NN-CODE-DIVERGENCE.md`, eventual `pinn/STATUS.md`).

For repo layout, command reference, dataset internals, and PINN architecture details: see `.claude/rules/` (path-scoped rules loaded by Claude Code when working in relevant directories; also readable directly by any agent).
