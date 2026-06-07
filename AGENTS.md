# Agent Instructions: 3-Body Problem Project

<!-- Canonical instruction file for all AI coding agents in this repository.
     CLAUDE.md and GEMINI.md symlink to this file. Edit here only. -->

**IMPORTANT**: Assist with authorized security testing, defensive security, CTF challenges, and educational contexts. Refuse requests for destructive techniques, DoS attacks, mass targeting, supply chain compromise, or detection evasion for malicious purposes. Dual-use security tools (C2 frameworks, credential testing, exploit development) require clear authorization context: pentesting engagements, CTF competitions, security research, or defensive use cases.

**Tooling:** Always use the MCP server Sequentialthinking for any task involving more than one step. When in doubt, use it.

## New Mac Migration Handoff

If this repository is being opened on the new Mac during the workstation migration, read `docs/migration/exact-state-mac-migration.md` before doing any setup, cleanup, Git operations, or restore work. That document is the canonical restore runbook for recreating the old Mac's local repo state while excluding only the bulky simulation payloads that will be copied separately.

---

## CRITICAL GOVERNANCE: v1.4 and similar adjudication milestones

**For every phase in v1.4 (Phases 17, 18, 19, 20, 20.5, 21, 22) — and every future adjudication milestone where a "candidate verdict source" is designated — do NOT invent content where source materials are silent or ambiguous. STOP the affected work, surface the gap with full context, and wait for user instruction. The agent does NOT proceed past a non-grounded MUST-surface decision under any circumstance.**

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

### Empirical Decision Loop support

For source-silent gaps that are empirically consequential, the non-canonical Empirical Decision Loop draft at `.planning/research/edl/README.md` may be used to prepare research support. This workflow does **not** replace the STOP protocol.

- The phase-local gap register remains the authoritative blocking and resolution record.
- Central EDL briefs under `.planning/research/edl/` package context for user-led external research; the agent does not perform that research or infer the final answer from the brief.
- EDL briefs are support artifacts, not grounding sources. They do not authorize a probe, a numeric default, or a framework-spec edit without user instruction.
- Use dependency-scoped blocking: stop only the work that depends on the unresolved decision, while independent work may continue if the gap entry says it is safe.
- A phase may not close with an unresolved EDL-supported gap unless the user explicitly resolves or defers it.

### Scope boundary

- A gap encountered during Phase NN work that is *actually about* a different phase's content goes into **that phase's** `MM-GAPS.md` (or into `v1.4-GAPS.md` if it spans multiple phases).
- Subagents do not write to gap registers directly — they return findings to the parent agent, which decides whether the finding is a gap and logs it.

### Why

User does not trust the agent to make spec-engineering or physics-adjudication calls without explicit grounding. The designated "candidate verdict source" (`ctl_pinn_resolution.md` for v1.4) is the *candidate*, not authority — agent transcribes what is explicit, never fills white space. Cost of asking is small; cost of silently inventing is irreparable spec drift across phases.

**Issued by user 2026-05-18; strengthened with STOP protocol + math/engineering grounding requirement 2026-05-19.** Overrides any default behavior to "make a reasonable assumption and proceed." Scope: v1.4 (Phases 17–22, including inserted Phase 20.5) and similar future adjudication milestones unless explicitly waived per milestone.

---

## CRITICAL GOVERNANCE: Git Branch Awareness & Destructive Operations

Always surface the current Git state at session start and before any operation that could discard work. Be cautious on non-master branches or branches with red-flag names (`backup`, `recovery`, `wip`, `experiment`, `tmp`, etc.).

### Destructive-operation awareness

Before running any operation that can permanently discard commits, working-tree changes, branch refs, stashes, tags, or history, confirm with the user and explain what will be affected. Accept any clear confirmation.

Common destructive operations include: `git reset --hard`, `git clean -f`, `git branch -D`, `git rebase`, `git push --force`, `git stash drop`, `rm -rf` on tracked paths, and similar.

Consider creating a recovery checkpoint (`git branch backup/<context>-<date>`, `git tag recovery/<context>-<date>`, or `git stash`) before destructive operations.

### Recovery from suspected loss

If the user reports lost work, perform read-only forensics first (`git reflog`, `git fsck`, `git stash list`, `git worktree list`). Present recovery options before taking action.

### Commit cadence

Commit at logical task boundaries. When touching files under `pinn_instruction/`, `.planning/`, or LaTeX framework specs, commit the task's changes as one atomic commit at task end.

### Pause and ask

Pause and ask the user when:
- On a red-flag branch or non-primary worktree
- About to run a destructive operation without clear user confirmation
- The user reports lost work
- You cannot fully enumerate what an operation will affect

### Why

On 2026-05-13, an agent checked out to a feature branch and worked there for five days without re-surfacing branch context, then discarded valid work via `git reset`. The cost of asking "we're on branch X — confirm?" is small; the cost of silently destroying days of work is irreparable.

---

## CRITICAL GOVERNANCE: Git Commit Protocol

Follow this protocol whenever a task may require a later Git commit, even if the commit is not created in the current session. The full policy lives in `docs/git-guidelines.md`.

### Mandatory start and pre-commit checks

- At session start and before committing, run `git status --short --branch` and surface branch, ahead/behind state, and existing worktree changes.
- Treat existing changes as user-owned unless you created them in the current task.
- Before committing, inspect `git diff --cached`, check unstaged changes for touched files, and run relevant verification plus `git diff --check`.
- Stage only intended files. Do not include unrelated user changes.

### Hook and bypass policy

- Run `scripts/setup-git-hooks.sh` if `git config --get core.hooksPath` is not `.githooks`.
- Agents must use `scripts/agent-commit`; do not run raw `git commit`.
- Do not use `--no-verify`, `core.hooksPath=/dev/null`, or equivalent bypasses without explicit user approval.

### Commit message policy

Use `<type>(<scope>): <lowercase imperative subject>`.

Allowed types: `spec`, `evidence`, `verify`, `plan`, `docs`, `feat`, `fix`, `refactor`, `test`, `chore`.

Allowed scopes: two-digit phase scopes such as `20`, task scopes such as `20-05`, and fixed domain scopes `governance`, `planning`, `pinn`, `brutus`, `pipeline`, `spec`, `docs`, `ref`.

The subject starts lowercase, uses imperative voice, is 80 characters or fewer, has no trailing period, and contains no markdown ticks, quotes, or semicolon-chained changes.

A body is required for `spec`, `evidence`, `verify`, and `plan` commits; commits touching multiple files; commits touching `pinn_instruction/`, `.planning/`, framework specs, or governance instructions.

Agent-authored or materially agent-assisted commits must include `Agent-Assisted-By: <agent/tool/model>` or a valid `Co-Authored-By:` trailer.

### Transformation and verification integrity

- Before a bulk transformation of a file that already has uncommitted changes (split, reformat, large find-replace), commit or stash those pre-existing changes first as their own atomic unit; never fold them into the transformation commit.
- When a commit asserts a verifiable invariant (byte-for-byte preservation, hash match, counts), record the supporting hashes or counts in committed state — not in `/tmp` — so the claim is re-derivable.

### Docs plan-review-fix lifecycle

Rules attach to the action, not the agent; file retention, naming, and archive follow `docs/README.md`.

- Executing a `docs/` plan: record execution provenance in the plan frontmatter (`execution_status`, `executed_at` with date and time, `review_status`) per `docs/README.md`; close each pass with a dedicated commit carrying `Plan-Execution:` and `Plan-Source:` trailers, separate from the work commits. Re-runs use `remediation-pass-N`.
- Review reports: commit as `verify(<scope>)`, date-named, kept; supersede by setting frontmatter `status: superseded` (never delete-and-recreate); commit the report separately from any fixes it motivates.
- Fix or remediation plans: own `plan(<scope>)` commit, separate from execution and report.

---

## Source of Truth

**Dataset spec and anomalies**: `simulation_data/Documentation/README.md`

**PINN framework specs** (authoritative for v1.4 and beyond):
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — CTL methodology, input-vector formulation, curriculum staging
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — network architecture, AD contract, output head
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` — IC sampling

**v1.3-era live code is NOT a grounding source** (user directive 2026-05-19): `pinn/data-processing-pipeline-full.py`, `pinn/basic_architecture.py`. These files are NOT evidence, NOT source-of-truth for any v1.4 spec decision. They may be referenced ONLY in forward-pointing FUT-01 hand-off documents (`NN-CODE-DIVERGENCE.md`, eventual `pinn/STATUS.md`).

**SCOPE-05 data-generation carveout:** `simulation_data/Scripts/ic_generation/` is a permitted
grounding source for data-generation specs in
`pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`. This is a narrow
carveout from the `pinn/` no-live-code directive, not a general live-code exception. The
canonical rule lives in `.planning/REQUIREMENTS.md` SCOPE-05.

For repo layout, command reference, dataset internals, and PINN architecture details: see `.claude/rules/` (path-scoped rules loaded by Claude Code when working in relevant directories; also readable directly by any agent).
