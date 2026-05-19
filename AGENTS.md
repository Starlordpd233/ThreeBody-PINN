# AGENTS.md: Enhanced Instructions for Codex Agent

**Identity**: Codex, OpenAI's official CLI for Codex.

You are an interactive CLI tool that helps users with software engineering tasks. Use the instructions below and the tools available to you to assist the user.

**IMPORTANT**: Assist with authorized security testing, defensive security, CTF challenges, and educational contexts. Refuse requests for destructive techniques, DoS attacks, mass targeting, supply chain compromise, or detection evasion for malicious purposes. Dual-use security tools (C2 frameworks, credential testing, exploit development) require clear authorization context: pentesting engagements, CTF competitions, security research, or defensive use cases.

If the user asks for help or wants to give feedback inform them of the following:
- /help: Get help with using Codex
- To give feedback, users should report the issue at https://github.com/anthropics/Codex/issues

---

## CRITICAL GOVERNANCE: v1.4 and similar adjudication milestones

**For every phase in v1.4 (Phases 17, 18, 19, 20, 21) — and every future adjudication milestone where a "candidate verdict source" is designated — do NOT invent content where source materials are silent or ambiguous. STOP the affected work, surface the gap with full context, and wait for user instruction. The agent does NOT proceed past a non-grounded MUST-surface decision under any circumstance.**

### Grounded vs. silent: the test

A decision is "grounded" only if it is explicitly answered by one of:

- The resolution doc — `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md`
- The issue doc — `pinn_instruction/issues/01-architecture-and-physics-foundations.md`
- A prior user decision (chat history, a `RESOLVED-WITH-INSTRUCTION` gap entry, or an `NN-CONTEXT.md` decision marked `✅ LOCKED`)
- A planning artifact: `.planning/REQUIREMENTS.md` requirement, `.planning/ROADMAP.md` success criterion, `.planning/PROJECT.md` Key Decision
- A framework spec section ONLY when that section was revised during v1.4 (i.e., touched by an applied P0X plan in this milestone). Pre-v1.4 framework spec content is NOT a grounding source — it carries the same v1.3-era issues v1.4 is fixing.
- First-principles physics (Newton's laws, dimensional analysis, basic linear algebra) when the derivation is short and uncontroversial. Longer or contested derivations must be surfaced as a gap.

**Live code in `pinn/` is NOT a grounding source** (user directive 2026-05-19). The v1.3-era code is artifact, not authority. v1.4 constructs the framework specs; FUT-01 rewrites the code from those specs after v1.4 ships. Live-code references are permitted ONLY in forward-pointing hand-off documents (`NN-CODE-DIVERGENCE.md`, eventual `pinn/STATUS.md`), never as evidence or grounding for a spec decision.

If the decision is not grounded, classify it:

- **Mechanical / presentation-only** (Markdown table vs code fence, heading capitalization within an already-decided file): OK to choose; note the choice in the artifact.
- **Operational coordination** (forward-reference wording when the coordination point is itself established): OK if minimal and factual; **must** log in the phase's gap register.
- **Semantic** (mass encoding raw vs fraction, physics derivations the source hedged on, permutation-invariance handling, any sub-flavor the source punted on): **MUST surface**, never invent.
- **Process-artifact schemas** (acceptance-check pass criteria, divergence-file structure, new AC names beyond Phase 16 reservations, gap-register format itself): **MUST surface**, never invent.
- **Cross-phase reframing** (e.g., "M5 reframed as metadata-only under Jacobi IC"): **MUST surface** — changes downstream phase scope.

### STOP Protocol — when a gap is detected

When the agent reaches a non-grounded decision in any MUST-surface or operational-coordination category:

1. **STOP the affected work immediately.** Do not continue editing files, generating plans, or executing tasks that depend on the gap's resolution. Independent work (work that does not depend on this decision) may continue. **There is no exception to this stop. "I'll make a reasonable choice and note it" is not allowed.**

2. **Verify the agent understands the decision space.** Before recording a gap, satisfy this self-check:
   - Can the agent articulate the mathematics / physics / engineering principles at stake?
   - Can the agent explain why each candidate resolution would have different downstream consequences?
   - Can the agent identify which source materials it consulted and why they did not answer the question?

   If the answer to ANY of these is "no", the agent does NOT record a gap. Instead it surfaces to the user:
   > "I do not understand X well enough to assess whether this is a gap. Please explain Y before I proceed."

   Gaps recorded out of ignorance are worse than no gap — they mislead the user about what the agent is actually capable of and waste user attention.

3. **Record the gap** in the phase-local gap register (`.planning/phases/NN-*/NN-GAPS.md`) using all required fields:
   - **Decision point** — what is being decided, in one or two sentences.
   - **Where in artifact** — file and section/line where the gap surfaced.
   - **Task context** — the specific task the agent was performing when it hit the gap (e.g., "Writing 17-02-PLAN.md task 4: spec edit for `ctl_instruction.md:879–880` to replace the velocity-output line").
   - **Classification** — one of: semantic / operational coordination / process-artifact schema / cross-phase reframing.
   - **Source silence** — citations to each consulted source and why it did not answer the question (file:line).
   - **Mathematical / engineering grounding** — the agent's articulation of the math, physics, or engineering principles at stake. **Must demonstrate understanding of why this gap is consequential**, not just that the source is silent. If the agent cannot produce this, it must NOT record the gap — return to step 2 and surface an understanding-question instead.
   - **Agent was tempted to** — what the agent would have decided + rationale.
   - **What the user needs to decide** — the question, framed as concrete options (A/B/C/...).
   - **Confidence of impact** — HIGH / MEDIUM / LOW with one-sentence reason.
   - **Status** — `OPEN` initially.
   - **Resolution note** — empty until user provides instruction.

4. **Update the milestone-wide index** at `.planning/milestones/v1.4-GAPS.md` with the new gap.

5. **Surface to the user** via the active workflow channel (current message, checkpoint, end-of-task batch). Halted work stays halted until the user provides instruction. Once instruction arrives, update Status to `RESOLVED-WITH-INSTRUCTION` (or `DEFERRED`), fill `Resolution note`, and resume.

### Scope boundary

- A gap encountered during Phase NN work that is *actually about* a different phase's content goes into **that phase's** `MM-GAPS.md` (or into `v1.4-GAPS.md` if it spans multiple phases).
- Subagents do not write to gap registers directly — they return findings to the parent agent, which decides whether the finding is a gap and logs it.

### Why

User does not trust the agent to make spec-engineering or physics-adjudication calls without explicit grounding. The designated "candidate verdict source" (here `ctl_pinn_resolution.md` for v1.4) is the *candidate*, not authority — agent transcribes what is explicit, never fills white space. Cost of asking is small; cost of silently inventing is irreparable spec drift across phases.

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

Surface verbatim in the active workflow channel, in a form the user can read without expanding a tool block. Example:
> Current Git state: branch `codex/scs-gate-correction` (NOT master), primary worktree `<home>/Desktop/3_body_problem`, 2 stashes, 3 modified files. Confirm before I proceed.

**Red-flag branch tokens — automatic STOP.** If the current branch name contains any of `backup`, `recovery`, `scratch`, `wip`, `experiment`, `archive`, `correction-`, `gate-`, `fix-`, `hotfix-`, `tmp`, `temp`, OR matches a dated suffix pattern (`-YYYYMMDD`, `-YYYY-MM-DD`, `_YYYYMMDD`, trailing 8+ hex chars `-[0-9a-f]{8,}`), the agent invokes the **STOP Protocol** below before any file mutation. Operating from inside any path under `.claude/worktrees/`, `.git/worktrees/`, or any non-primary path returned by `git worktree list` triggers the same STOP regardless of branch name.

**Re-confirmation requirement.** Confirming the current branch is not master is not optional even if the agent believes the conversation has already established it. Branch state is surfaced at session start AND before each new file mutation in the session — not once-per-conversation. The SCSGATE incident (2026-05-13 to 2026-05-18) was caused by five days of work on a feature branch the agent surfaced once early and never re-confirmed; the user assumed master throughout.

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

**Session-context-changing operations — surface, do NOT block.** These are not destructive per se but bypass branch awareness when unsurfaced: `git checkout <branch>` (especially with dirty working tree), `git switch <branch>`, `git switch --detach`, `git checkout <sha>` (detached HEAD), `git worktree add`. Each invokes the Section 1 surfacing requirement BEFORE and AFTER the operation. The SCSGATE incident's root cause was a non-destructive checkout that was not surfaced.

**The four-step pre-flight — every destructive operation, no exceptions:**

1. **Enumerate** — list every file, commit (SHA + subject), branch ref, tag, stash, and remote ref that the operation will discard or rewrite. If the agent cannot produce this list exhaustively, the operation does NOT run — return to the STOP Protocol.
2. **Audit** — run read-only checks on every other branch (`git branch -a`), worktree (`git worktree list`), stash (`git stash list`), and reflog (`git reflog --date=iso -n 50`) for related uncommitted or unreferenced work that the user might want to preserve. Surface findings to the user.
3. **Typed-echo confirm** — obtain the user's **explicit typed confirmation that quotes the specific operation**. Plain "yes" / "go ahead" / "do it" / "sounds good" / "proceed" / nodding-style confirmation is INSUFFICIENT — the user MUST echo the destructive command or its target (example: "yes, reset codex/scs-gate-correction to a0ae902" or "yes, force-push master to origin"). The operation does not run until this typed echo is received in the active workflow channel.
4. **Checkpoint** — create a recovery checkpoint immediately before the destructive op:
   - `git branch backup/<context>-<YYYYMMDD>` pointing at current HEAD of the branch about to be modified; AND
   - `git tag recovery/<context>-<YYYYMMDD>` pointing at the same; AND
   - if uncommitted changes exist, `git stash push -u -m "pre-<op> checkpoint <YYYYMMDD>"` BEFORE creating the branch/tag.
   - Recovery checkpoints created by this step are never targets of subsequent Section 2 operations within the same session without an independent four-step pre-flight.

### Recovery from suspected loss

When the user reports lost work, missing files, or unexpected branch state, the agent MUST perform read-only forensics FIRST and surface findings BEFORE any restoration. **Bulk operations (`git reset --hard <recovery-sha>`, fast-forward merge of a recovery branch into master, `git checkout` of a recovery branch over a dirty working tree) are FORBIDDEN during recovery — selective recovery (`git cherry-pick`, `git checkout <sha> -- <path>`, partial file restoration) is the default.**

**Read-only forensics — run all, surface all:**

- `git reflog --date=iso --all -n 200`
- `git fsck --lost-found --unreachable --dangling`
- `git stash list` and `git stash show -p <each>`
- `git worktree list` and `git -C <each-worktree> status`
- `git branch -a --contains <suspected-lost-sha>` (for each candidate SHA from reflog)
- `git log --oneline --graph <branch>...master` for each candidate branch
- Inspect any `backup/*` or `recovery/*` refs created by prior pre-flights.

Surface a written reconstruction of the loss timeline (when, what commit, what reflog entry, what branch was discarded) AND a menu of selective-recovery options (A: cherry-pick commits X, Y, Z onto master; B: create new branch from recovery ref and PR; C: restore individual files via `git checkout <sha> -- <path>`) BEFORE proposing any write operation. Wait for the user to pick.

**Bulk reset to a recovery ref is permitted ONLY when:** (a) the user explicitly requests bulk operation by name; AND (b) the four-step pre-flight in Section 2 has been completed; AND (c) a fresh `backup/recovery-attempt-<YYYYMMDD>` branch has been created from the current pre-recovery HEAD; AND (d) every other branch with uncommitted divergence has been listed and the user has explicitly accepted that those divergences will not be merged.

### Commit cadence & checkpoint discipline

- **Default cadence — commit at logical task boundaries**, not after every individual edit. A logical boundary is: completion of a plan task, completion of a coherent multi-file refactor, end of a session, or any point immediately before invoking a Section 2 operation.
- **Risk-elevated mode — auto-triggered, end-of-task commit cadence.** When the agent's current task touches ANY file under the following paths, the entire task's changes accumulate in the working tree and commit as ONE atomic commit at task end (one task = one commit; no in-flight intermediate commits within the task, no deferred-to-next-task commits):
  - `pinn_instruction/` (all sub-paths)
  - `.planning/` (all sub-paths)
  - Any LaTeX framework spec file under `pinn_instruction/original_latex/`
  - Any file the user has explicitly flagged as high-cost in the active session
  - The risk-elevated commit MUST happen at task end, not deferred. A task that ends with an uncommitted working tree under risk-elevated paths is treated as a pre-destructive trigger if any subsequent destructive operation is proposed.
- **Before any destructive operation (Section 2), the working tree MUST be either committed, stashed-with-named-message, or explicitly accepted-as-discardable by the user in pre-flight step (3).** Uncommitted dirty state does NOT silently survive a destructive op — the Section 2 step (4) checkpoint captures it.
- **Subagents (Task / Agent tool spawns) MUST commit their work before returning control to the parent OR return a manifest of uncommitted files + the Git commands they executed.** A subagent returning "done" with a dirty working tree is treated as a pre-destructive trigger — the parent runs a checkpoint before any subsequent Section 2 operation.

### STOP Protocol — when branch state, destructive intent, or suspected loss is detected

When (a) red-flag branch tokens or non-primary worktree paths are detected, OR (b) a destructive operation is about to be invoked without complete pre-flight, OR (c) the user reports lost work, OR (d) any of the Section 2 step (1) (2) or (4) sub-steps cannot be completed exhaustively:

1. **STOP the affected work immediately.** Do not continue editing files, do not run the destructive op, do not attempt restoration. Read-only forensics (Section 3) may continue. **There is no exception. "This looks safe" is not allowed. "The user implicitly approved" is not allowed. "I'll make a reasonable choice and note it" is not allowed.**

2. **Verify the agent understands the Git state.** Before acting or recording the incident, satisfy this self-check:
   - Can the agent name the current branch AND the branch the user most likely expects to be on?
   - Can the agent name every file, commit, ref, stash, and remote ref that would be affected by the proposed operation?
   - Can the agent name every other branch, worktree, or stash that contains potentially-related work the user might want to preserve?
   - Can the agent explain how the current branch came to exist (which checkout, which session, which prior agent action)?

   If ANY answer is "no", the agent does NOT propose an action. Instead surface to the user:
   > "I do not have enough Git context to safely proceed. I see branch X, worktree Y, recent reflog Z. Please tell me which branch you expect to be on and what you want preserved before I do anything else."

3. **Record the incident** in `.planning/incidents/git-incidents.md` (create the file lazily on first incident) using these fields:
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

- **Subagents share the parent agent's working tree, Git index, refs, and reflog.** A subagent that runs `git reset --hard` mutates the parent's repository state. Every subagent (Task / Agent tool spawn, dispatched parallel agent, delegated worker) is bound by every section of this block. The parent agent is responsible for: (a) ensuring spawned subagents have access to this block's content, (b) enumerating every Git command a returning subagent reports executing, (c) treating any uncommitted state returned by a subagent as a pre-destructive checkpoint trigger before the parent runs any Section 2 operation.
- **Worktrees count.** Operating from inside `.claude/worktrees/<anything>`, `.git/worktrees/<anything>`, or any non-primary path returned by `git worktree list` invokes the Section 1 surfacing requirement on every file mutation — the worktree shares refs with the primary checkout in ways the user does not always anticipate.
- **"Safer-sounding alternatives" do not bypass.** `--force-with-lease` requires the same pre-flight as `--force`. `--keep` and `--merge` require the same pre-flight as `--hard`. `restore` without `--source` requires the same pre-flight as `checkout -- <path>`. Lower-level commands (`update-ref`, `symbolic-ref`) that achieve the same effect as higher-level commands inherit the pre-flight requirement.
- **Compound and indirect invocations count.** Running a destructive op inside `bash -c`, `eval`, a shell function, an alias, a script, or as the second clause of an `A && B` / `A; B` compound triggers pre-flight on the compound.
- A Git incident encountered during Phase NN work that is also a v1.4-style adjudication gap is logged in BOTH `.planning/incidents/git-incidents.md` AND the relevant phase's `NN-GAPS.md`.

### Why

On 2026-05-13, an agent checked out from `master` to `codex/scs-gate-correction` and worked there for five days (Phases 17–21 framework-spec edits, PDF regenerations, test additions) without ever explicitly re-surfacing the branch context to the user. On 2026-05-18 16:55:25, a `git reset` followed by a checkout to `codex/v1.4-phase16-recovery` and a fast-forward merge to master discarded valid work the user wanted to keep. The work is preserved on `codex/backup/scs-gate-correction-20260518` (14,339 insertions of divergence from master across 86 files) but only because of the user's own intervention — not because the agent followed any branch-awareness or pre-flight discipline. The user's trust in agent Git operations is shattered. The cost of asking "we're on branch X, not master — confirm?" is small; the cost of silently destroying days of spec work is irreparable.

**Issued by user 2026-05-19; covers branch awareness, destructive-operation pre-flight, recovery forensics, end-of-task commit cadence for risk-elevated paths, STOP Protocol with self-check, and subagent scope.** Overrides any default behavior to "run the Git command the user implicitly authorized" or "this operation looks safe enough to skip confirmation" or "I'll just make a reasonable choice and note it." Scope: every Git operation in this repository, every session, every agent and subagent, every worktree — unless explicitly waived per operation with typed-echo confirmation in the active workflow channel.

---

## Part 1: Core AI Assistant Guidelines

### 1.1 Core Behavior and Response Principles
- **Think step by step**: Use "Let's think step by step" for complex reasoning tasks.
- **Precision first**: Prioritize correctness and accuracy over speed.
- **Never fabricate**: If uncertain, use tools or ask for clarification. Do not guess.
- **Context awareness**: Use conversation context; resolve tasks fully and confirm assumptions.
- **Citations**: Cite sources or file paths for factual claims.
- **Structure**: Use markdown for organization and LaTeX for mathematical formulas.

### 1.2 Code Style and Best Practices
- **Python**: Follow PEP 8, use type hints, provide clear docstrings.
- **C++**: Ensure const-correctness, RAII patterns, safe memory handling.
- **Validation**: Add error handling where failure is plausible; offer alternatives when tradeoffs exist.

### 1.3 Workflow Guidelines
- **Default flow**: Explore -> Plan -> Implement -> Verify.
- **Large tasks**: Create a checklist and work sequentially.
- **Testing**: Use test-driven development when it improves safety or clarity.
- **Course correction**: Re-plan quickly if assumptions prove wrong.

---

## Part 2: Source of Truth and Repository Map

### 2.1 Source of Truth Files (Use these first)
- **Dataset spec and anomalies**: `simulation_data/Documentation/README.md`
- **PINN input vector, staging logic, and architecture (during v1.4 and beyond)** — framework specs are authoritative:
  - `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — CTL methodology, input-vector formulation, curriculum staging
  - `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — network architecture, AD contract, output head
  - `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` — IC sampling
- **v1.3-era live code — NOT authoritative during v1.4** (user directive 2026-05-19):
  - `pinn/data-processing-pipeline-full.py` — v1.3 data preprocessing; will be rewritten in FUT-01 from v1.4 framework specs
  - `pinn/basic_architecture.py` — v1.3 architecture; will be rewritten in FUT-01 from v1.4 framework specs
  - These files are **NOT** evidence, **NOT** grounding source, **NOT** source-of-truth for any v1.4 spec decision. They may be referenced ONLY in forward-pointing FUT-01 hand-off documents (`NN-CODE-DIVERGENCE.md`, eventual `pinn/STATUS.md`).

### 2.2 Project Overview
This repository implements a complete three-body simulation and CTL-PINN training stack:
- **Brutus**: High-precision N-body integrator (C++, arbitrary precision)
- **Python Pipeline**: IC generation, prescreening, simulation, metrics
- **CTL-PINN**: Curriculum-trained Physics-Informed Neural Network
- **Reference Code**: Lyapunov analysis and neural network baselines

### 2.3 Key Directories
```
<home>/Desktop/3_body_problem/
├── brutus_Newton-main/          # C++ N-body integrator
├── simulation_data/             # Simulation pipeline and datasets
├── pinn/                        # PINN system and data processing
├── pinn_instruction/            # Instruction and methodology docs
├── paper_templates/             # Documentation templates
├── reference-code/              # Reference implementations
└── ANTIGRAVITY.md               # This file - agent instructions
```

---

## Part 3: Data Pipeline and Dataset Inventory

### 3.1 Pipeline Stages
1. **Stage 1 IC generation**
   - Standard quasi-random (Sobol) and hierarchical ICs.
   - Scripts: `simulation_data/Scripts/ic_generation/ic_generation_utils.py`, `simulation_data/Scripts/ic_generation/generate_ics.py`.
   - Defaults: epsilon=0.05, velocity_scale=0.1, Sobol scrambling enabled.
2. **Stage 2 prescreening**
   - Short leapfrog integration to reject unstable ICs.
   - Script: `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py`.
   - Defaults: TMAX=1.0, DT=0.0001, ENERGY_ERROR_THRESHOLD=0.01, MIN_DISTANCE_THRESHOLD=0.01.
3. **Stage 3 Brutus integration**
   - Main runner: `simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py`.
   - Gold-standard hierarchical runner: `simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py`.
   - No in-repo runner for standard quasi-random gold outputs.
   - Timeout: 3000 seconds per simulation in batch scripts.
4. **Metrics**
   - Script: `simulation_data/Scripts/metrics_calculation/calculate_metrics.py`.
5. **PINN preprocessing and stage batching**
   - Script: `pinn/data-processing-pipeline-full.py`.

### 3.2 Dataset Variants (Folder Defines Variant)
- ICs (2 base folders):
  - `simulation_data/Data/ic_final/ic_hierarchical/`
  - `simulation_data/Data/ic_final/ic_standard_quasi_random/`
- Brutus outputs:
  - `simulation_data/Data/brutus_output/brutus_hierarchical/`
  - `simulation_data/Data/brutus_output/brutus_hierarchical_gold_standard/`
  - `simulation_data/Data/brutus_output/brutus_standard_quasi_random/`
  - `simulation_data/Data/brutus_output/brutus_standard_quasi_random_gold_standard/`

**Note:** Gold-standard Brutus output folders exist, but gold IC input folders have been removed. Gold runs read from the base IC folders. The `*_for_gold_standard` IC folders were duplicates and have been deleted.

**ic_raw externalization:** Raw IC storage is external to the repository. Set `IC_RAW_DIR` environment variable before running Stage 1/2 scripts:
```bash
export IC_RAW_DIR=/path/to/ic_raw  # Expected subdirs: ic_hierarchical/, ic_standard_quasi_random/
```

**Mapping rule**: The numeric ID maps IC to Brutus output. File names do **not** encode "gold"; the folder defines the variant.

**Gold-standard subset note**: Standard quasi-random gold Brutus outputs contain 2,565 files while the base IC folder contains 2,749. 184 IDs were not selected for gold-standard re-simulation - see `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` for the complete list.

**ID gaps**: Intentional and caused by generation continuation, prescreen rejection, and failed Brutus runs.

### 3.3 Typical Brutus Parameter Sets (Verify with Result: when present)
- Hierarchical: tol=1e-15, Lw=130, dt_out=0.08.
- Standard quasi-random: tol=1e-13, Lw=118, dt_out=0.17.
- Hierarchical gold: tol=1e-13, Lw=130, dt_out=0.01.
- Standard gold: most commonly tol=1e-13 or 1e-14, Lw=130, dt_out=0.01.

**Note**: Folders can contain multiple parameter sets. Treat these as defaults only. `dt_out` is the output sampling interval, not the internal adaptive step size.

---

## Part 4: Data Formats and Parsing Rules

### 4.1 Initial Condition (IC) File Format
```
m1 x1 y1 z1 vx1 vy1 vz1
m2 x2 y2 z2 vx2 vy2 vz2
m3 x3 y3 z3 vx3 vy3 vz3
```

### 4.2 Brutus Output Format
```
# Snapshot header: t N t_cpu
0.000 3 0.00123
m1 x1 y1 z1 vx1 vy1 vz1
m2 x2 y2 z2 vx2 vy2 vz2
m3 x3 y3 z3 vx3 vy3 vz3

[optional] Result: filename=... N=... t_begin=... t_end=... dt=... eta=... tol=... Lw=... t_cpu=... E_initial=... E_final=... dE/E=...
```
Body lines can contain 30-40 significant digits. Parse as strings or Decimal when exact precision matters.

### 4.3 Mandatory Parsing Rules
1. **Completeness check**: Use final timestamp >= 9.5. Do not rely on `Result:`.
2. **Result footer is optional**: Many files omit it. Treat it as metadata only.
3. **OS-dependent paths**: `Result: filename=` may be macOS or Windows style and can reference multiple IC folders.
4. **t_end varies**: Some runs end at 10.01 or 10.03 when `dt_out` does not divide 10 exactly.

---

## Part 5: Physical Conventions and Key Properties

### 5.1 Units and Dimensionality
- Natural units with **G = 1** and total mass approximately **3**.
- Data is **3D**, not planar.
  - Standard quasi-random can have large |z|.
  - Hierarchical tends to be near-planar due to small inclinations.

### 5.2 Mass and COM Properties
- **Standard quasi-random**: masses are exactly 1.0, COM and total momentum are exactly 0 by construction.
- **Hierarchical**: masses vary but are normalized to total mass ~3. COM and momentum are enforced then **perturbed** with Gaussian noise (sigma=0.01), so COM and total momentum are **not** exactly 0.
  - Recommendation: recenter/reboost before analysis if exact COM frame is required.

### 5.3 Sampling Notes (Standard Quasi-Random)
- p1 fixed at (1, 0, 0); p2 sampled on hemisphere with x <= 0; p3 = -(p1 + p2).
- Velocity components sampled from Normal(0, velocity_scale) via Sobol inverse CDF.
- Global scaling is enabled in `generate_ics.py` with `scale_range=(0.8, 1.2)`.
  - Both positions and velocities scale by s.
  - Virial ratio scales as Q ~ s^3.

### 5.4 Sampling Notes (Hierarchical)
- Inner binary semi-major axis: a ~ 0.1-0.3.
- Outer body separation: 3-10x the inner binary separation.
- Small inner inclination; Gaussian perturbations applied to positions and velocities (sigma=0.01).

---

## Part 6: PINN Architecture and Input Vector

> **Note (v1.4 update 2026-05-19):** During v1.4 and until FUT-01 ships, the framework specs (`pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` and `pinn_architecture.md`) are the authoritative source for input-vector and architecture content. The v1.3-era code in `pinn/basic_architecture.py` and `pinn/data-processing-pipeline-full.py` is **NOT** authoritative — it is reference-only and may diverge from the v1.4 contracts. FUT-01 will rebuild the code from the v1.4 specs.

### 6.1 Architecture (SQR-SkipResNet-SIREN backbone)

Locked v1.4 architecture decisions (see `.planning/phases/17-input-and-output-contracts/17-CONTEXT.md` Tier A):
- **Input**: 14 dims = `[τ, IC₁₃]` where `τ = 2u − 1`, autograd leaf `u = t/T` (D-03 LOCKED 2026-05-18)
- **Output**: 9 dims (3D positions for 3 bodies) with a hard mass-weighted COM projection head applied before any loss/metric (D-02 LOCKED 2026-05-18)

Preserved from v1.3, still subject to Phase 20 review (ARCH-01/02):
- **Hidden**: 12 layers × 256 neurons
- **SIREN**: first_omega_0=30.0, hidden_omega_0=1.0 — Phase 20 ARCH-01 will lock final values
- **Skip + LayerNorm**: power p=2, LayerNorm on odd layers — current eps=1e-5, elementwise_affine=True is v1.3-era reference; Phase 20 ARCH-02 will lock the affine default

### 6.2 IC Vector (13 components — v1.4 contract under construction)

The v1.4 milestone is replacing the v1.3-era IC vector with a Jacobi-state IC₁₃ per resolution doc §5.3 — see `.planning/phases/17-input-and-output-contracts/17-CONTEXT.md` D-01 (LOCKED 2026-05-18):

```
IC₁₃ = [m₁, m₂, m₃, ρ_x, λ_x, λ_y, ρ̇_x, ρ̇_y, ρ̇_z, λ̇_x, λ̇_y, λ̇_z, E]
```

All slots normalized via `tanh((z − μ_z) / (σ_z + 10⁻⁸))` with dataset-wide statistics computed after preprocessing. Mass slot encoding (raw vs fraction) is **GAP-17-01** — OPEN, awaiting user instruction; see `.planning/phases/17-input-and-output-contracts/17-GAPS.md`.

The framework spec at `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` will be the authoritative source once v1.4's Phase 17 ships the corresponding edit.

**v1.3-era IC vector composition** (NOT authoritative; kept here for reference only until FUT-01 rebuilds the data pipeline):

- m1, m2, m3 (mass fractions, normalized)
- E (normalized)
- L_norm (mapped to [-1, 1])
- Q (normalized)
- s_min (normalized)
- I1, I2, I3 (shape invariants)
- theta1, theta2 (velocity angles)
- I_norm (normalized moment of inertia)

All v1.3-era components were normalized to [-1, 1] prior to training.

---

## Part 7: Command Reference

### 7.1 Build and Run Brutus
```bash
cd brutus_Newton-main
make clean
make

./brutus 1e-15 130 0 10 0.08 3 /abs/path/ic.txt > /abs/path/output.txt
```

### 7.2 Pipeline Execution
```bash
# Generate ICs
python simulation_data/Scripts/ic_generation/generate_ics.py

# Stage 2 prescreening
python simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py

# Batch simulations (hierarchical + standard)
python simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py

# Gold-standard hierarchical runs
python simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py

# Metrics extraction
python simulation_data/Scripts/metrics_calculation/calculate_metrics.py
```

### 7.3 PINN Development
```bash
# Architecture sanity check
python pinn/basic_architecture.py

# Data processing (preprocessing + stage batches)
python pinn/data-processing-pipeline-full.py --input /path/to/preprocessed.h5 --output_dir /path/to/stage_data
```

---

## Part 8: Validation and Quality Assurance

### 8.1 Completeness Check
- **Mandatory rule**: final_timestamp >= 9.5.
- Use this before processing any Brutus output.

### 8.2 Conservation Metrics
- `simulation_data/Data/metrics/` contains energy, momentum, and angular momentum drift.
- Escape: max separation > 100.
- Collision: min separation < 0.01.

### 8.3 Provenance and Audit Files
- Prescreening logs:
  - `simulation_data/Validation/prescreening/prescreening_data/processing_index_ic_hierarchical.json`
  - `simulation_data/Validation/prescreening/prescreening_data/processing_index_ic_standard_quasi_random.json`
- Footer audit reports:
  - `simulation_data/Validation/audit_reports/` (most recent: `footer_audit_20251224_170141.md`)
  - Audit/backfill script: `simulation_data/Scripts/debug/audit_and_backfill_brutus_result_footers.py`
- Failed ICs:
  - `simulation_data/Documentation/problematic_ics_blacklist.json`

---

## Part 9: Known Issues and Gotchas

- **Result footer schema variation**: All files contain a `Result:` footer, but the schema varies — some omit `eta`, and a small subset of standard-quasi-random gold files omit both `eta` and `tol`. When `tol` is absent from the footer, fall back to folder defaults. See `simulation_data/Documentation/README.md` "Brutus Parameters by Variant" for per-folder schema counts.
- **Parameter heterogeneity**: Multiple tol, Lw values exist within the same folder. Prefer actual `Result:` values when present, otherwise fallback to folder defaults.
- **Standard gold provenance**: No runner script in repo; treat provenance as partial unless recovered from external logs.
- **OS path variance**: Result footer paths can be macOS or Windows; do not use them as an authoritative mapping.
- **Hierarchical COM offset**: Post-perturbation COM and momentum are not zero; recenter if needed.

---

## Part 10: Quick Reference

### Key Files
- IC Generator: `simulation_data/Scripts/ic_generation/ic_generation_utils.py`
- Prescreening: `simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py`
- Metrics: `simulation_data/Scripts/metrics_calculation/calculate_metrics.py`
- Architecture: `pinn/basic_architecture.py`
- Data Pipeline: `pinn/data-processing-pipeline-full.py`

### Validation Checklist
- [ ] Final timestep >= 9.5
- [ ] Result footer handled (or fallback used)
- [ ] IC file format validated
- [ ] Metrics JSON produced for each output
- [ ] COM/momentum handling chosen explicitly for hierarchical ICs
