# Agent Instructions: 3-Body Problem Project

<!-- Canonical instruction file for all AI coding agents in this repository.
     CLAUDE.md and GEMINI.md symlink to this file. Edit here only. -->

**IMPORTANT**: Assist with authorized security testing, defensive security, CTF challenges, and educational contexts. Refuse requests for destructive techniques, DoS attacks, mass targeting, supply chain compromise, or detection evasion for malicious purposes. Dual-use security tools (C2 frameworks, credential testing, exploit development) require clear authorization context: pentesting engagements, CTF competitions, security research, or defensive use cases.

**Tooling:** Always use the MCP server Sequentialthinking for any task involving more than one step. When in doubt, use it.

## New Mac Migration Handoff

If this repository is being opened on the new Mac during the workstation migration, read `docs/runbooks/migration/exact-state-mac-migration.md` before doing any setup, cleanup, Git operations, or restore work. That document is the canonical restore runbook for recreating the old Mac's local repo state while excluding only the bulky simulation payloads that will be copied separately.

---

## CRITICAL GOVERNANCE: v1.4 and similar adjudication milestones

**For every phase in v1.4 (Phases 17, 18, 19, 20, 20.5, 21, 22), every phase in v1.5 (Phases 23–29), every phase in v1.6 (Phases 30–36) — and every future adjudication milestone where a "candidate verdict source" is designated — do NOT invent content where source materials are silent or ambiguous. STOP the affected work, surface the gap with full context, and wait for user instruction. The agent does NOT proceed past a non-grounded MUST-surface decision under any circumstance.**

### v1.5 applicability (2026-06-10)

v1.5 "Resolving 02 Data Pipeline and Validation" (Phases 23–29, branch `milestone/v1.5`) runs under this protocol. Read the grounding test below with these substitutions and extensions for v1.5 work:

- The issue doc is `pinn_instruction/issues/02-data-pipeline-and-validation.md` (non-authoritative; known to contain at least one suspect claim — the ratio-based SCS thresholds).
- The candidate verdict source is the **user-produced resolution doc** expected under `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/`. It does not exist until the user's external research delivers it; adjudication Phases 25–29 cannot start until it lands AND Phase 24 completes.
- Additional grounding (SCOPE-06/07 in `.planning/REQUIREMENTS.md`): the on-disk `simulation_data/` dataset (empirical facts verified by direct observation, recorded re-derivably) and `simulation_data/Scripts/` (`ic_generation/`, `metrics_calculation/`, `Validation/prescreening/`, `brutus_runners/`).
- Framework-spec sections revised during v1.4 or v1.5 are grounding; the `pinn/` live-code ban persists unchanged.
- Spec-edit targets are `ctl_instruction.md` and `pinn_architecture.md` ONLY; `sampling_method.md` is frozen by default (SCOPE-08); `data_quality_assessment.md` is read-only (SCOPE-09).
- The milestone-wide gap index for v1.5 phases is `.planning/milestones/v1.5-GAPS.md` (read step 4 of the STOP protocol accordingly).

### v1.6 applicability (2026-06-17)

v1.6 "Resolving 03 Curriculum and Training Loop" (Phases 30–36, branch `milestone/v1.6`) runs under this protocol. Read the grounding test below with these substitutions and extensions for v1.6 work:

- The issue doc is `pinn_instruction/issues/03-curriculum-and-training-loop.md` (non-authoritative; consolidates the 2026-04-27 audit Sections 6–7, the Causal Training Mismatch blueprint, the stage-assignment methodology, and `next steps.txt`; carries the `D = 6.694` claim that conflicts with the v1.5-locked raw-mass `D ≈ 4.6416`).
- The candidate verdict source is the **user-produced resolution doc** expected under `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/`. It does not exist until the user's external research (ERW) delivers it; adjudication Phases 32–36 cannot start until it lands AND Phase 31 (resolution-doc readiness verification) passes.
- Additional grounding (SCOPE-12 in `.planning/REQUIREMENTS.md`): the locked v1.4 (doc-01) and v1.5 (doc-02) framework-spec outcomes are hard constraints — 14D input `[τ, IC₁₃]`, Jacobi IC₁₃, mass-weighted COM projection head, PHYS-03 softening `eps_soft = 1e-5`, the post-v1.3 SCS gate (`ε_H > 10⁻⁵` / `SCS > −5`), the raw-mass `D ≈ 4.6416` convention (`D = 6.694` rejected by v1.5 Phase 25 EVID-10), and the v1.5 DataLoader/stage-query/validation-metric contracts (PIPE-01..10, VAL-01..04) — plus v1.5-verified dataset facts.
- Framework-spec sections revised during v1.4, v1.5, or v1.6 are grounding; the `pinn/` live-code ban persists unchanged.
- v1.6 is **specwork-only** (user-confirmed 2026-06-17): spec-edit targets are `ctl_instruction.md` and `pinn_architecture.md` ONLY (SCOPE-13); `sampling_method.md` is frozen (SCOPE-08); `data_quality_assessment.md`, `review-of-framework.md`, and `stage-strat-revision.md` are read-only (SCOPE-09). Training-loop code, the adaptive-stage-assignment EDA run, and the Stage-0 pilot are FUT-01/FUT-04 (SCOPE-14/15) — never implemented in v1.6; the verbatim audit "Section 6" pseudocode is transcribed as a normative spec contract, not executed.
- The milestone-wide gap index for v1.6 phases is `.planning/milestones/v1.6-GAPS.md` (created on the first v1.6 STOP gap, per the standing trigger; read step 4 of the STOP protocol accordingly).

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

Always surface the current Git state at session start, before committing, and before any operation that could discard work. Run `git status --short --branch`, report the branch plus ahead/behind state, and summarize existing modified/deleted/untracked files. Treat existing changes as user-owned unless you created them in the current task.

### Destructive-operation awareness

Before running any operation that can permanently discard commits, working-tree changes, branch refs, stashes, tags, or history, explain what will be affected and obtain exact user approval for the command or effect. Vague approval is not enough.

Common destructive operations include: `git reset --hard`, `git clean -f`, `git branch -D`, `git rebase`, `git push --force`, `git stash drop`, `rm -rf` on tracked paths, and similar.

Create or verify a recovery checkpoint before destructive operations. The command must include all three markers: `ALLOW_DESTRUCTIVE_GIT=1`, `GIT_DESTRUCTIVE_APPROVAL='<exact approved command or effect>'`, and `GIT_RECOVERY_CHECKPOINT='<backup branch, tag, stash, or commit ref>'`.

### Recovery from suspected loss

If the user reports lost work, perform read-only forensics first (`git reflog`, `git fsck`, `git stash list`, `git worktree list`). Present recovery options before taking action.

### Commit cadence

Agents may commit approved task work at logical boundaries unless the user explicitly says not to commit. Keep commits atomic, reversible, and reviewable. When touching files under `pinn_instruction/`, `.planning/`, or LaTeX framework specs, commit the task's changes as one atomic commit at task end.

Use the layered capture ladder: commits for completed logical work, backup branches or tags before risky history operations, and stashes or durable patch snapshots for dirty unfinished work.

### Concurrent agents

For Claude Code CCP or other multi-agent setups, prefer separate worktrees and branches for independent agents. If agents share one worktree, they still must declare disjoint owned paths and serialize commits through `scripts/agent-commit`.

Every agent commit must set `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS`. `GIT_AGENT_OWNED_PATHS` is a colon- or newline-separated list of repo-relative file or directory prefixes owned by the committing agent. Do not use broad staging (`git add .`, `git add -A`, `git add --all`, `git add -u`); stage explicit owned paths only. Re-check `git status --short --branch`, `git diff --cached`, and touched unstaged diffs immediately before committing.

Archived plans or old snippets that omit current Git-policy env vars are stale for execution purposes; adapt them to this policy instead of replaying them literally.

### Pause and ask

Pause and ask the user when:
- On a red-flag branch or non-primary worktree
- About to run a destructive operation without exact user confirmation and a recovery checkpoint
- The user reports lost work
- You cannot fully enumerate what an operation will affect
- Required Git policy markers or owned-path declarations are missing

### Why

On 2026-05-13, an agent checked out to a feature branch and worked there for five days without re-surfacing branch context, then discarded valid work via `git reset`. The cost of asking "we're on branch X — confirm?" is small; the cost of silently destroying days of work is irreparable.

---

## CRITICAL GOVERNANCE: Git Commit Protocol

Follow this protocol whenever a task may require a later Git commit, even if the commit is not created in the current session. The full policy lives in `docs/git-guidelines.md`.

### Mandatory start and pre-commit checks

- At session start and before committing, run `git status --short --branch` and surface branch, ahead/behind state, and existing worktree changes.
- Treat existing changes as user-owned unless you created them in the current task.
- Before committing, inspect `git diff --cached`, check unstaged changes for touched files, and run relevant verification plus `git diff --check`.
- Stage only explicit files covered by `GIT_AGENT_OWNED_PATHS`. Do not include unrelated user changes.

### Hook and bypass policy

- Run `scripts/setup-git-hooks.sh` if `git config --get core.hooksPath` is not `.githooks`.
- Agents must use `scripts/agent-commit`; do not run raw `git commit`. Set both `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS`.
- Do not use `--no-verify`, `core.hooksPath=/dev/null`, or equivalent bypasses without explicit user approval.

### Commit message policy

Use `<type>(<scope>): <lowercase imperative subject>`.

Allowed types: `spec`, `evidence`, `verify`, `plan`, `docs`, `feat`, `fix`, `refactor`, `test`, `chore`.

Allowed scopes: two-digit phase scopes such as `20`, task scopes such as `20-05`, and fixed domain scopes `governance`, `planning`, `pinn`, `brutus`, `pipeline`, `spec`, `docs`, `ref`. Inserted phases use task-style scope (`20-05`), not `20.5`, `20-5`, or `20_5`.

The subject starts lowercase, uses imperative voice, is 80 characters or fewer, has no trailing period, and contains no markdown ticks, quotes, or semicolon-chained changes.

A body is required for `spec`, `evidence`, `verify`, and `plan` commits; commits touching multiple files; commits touching `pinn_instruction/`, `.planning/`, framework specs, or governance instructions.

Agent-authored or materially agent-assisted commits must include `Agent-Assisted-By: <agent/tool/model>` or a valid `Co-Authored-By:` trailer.

Do not push directly from protected branches `master`, `main`, or `milestone/*`. Milestone branches are local integration branches; publish through feature/review branches or explicit user-controlled integration.

### Transformation and verification integrity

- Before a bulk transformation of a file that already has uncommitted changes (split, reformat, large find-replace), commit or stash those pre-existing changes first as their own atomic unit; never fold them into the transformation commit.
- When a commit asserts a verifiable invariant (byte-for-byte preservation, hash match, counts), record the supporting hashes or counts in committed state — not in `/tmp` — so the claim is re-derivable.

### Docs plan-review-fix lifecycle

Rules attach to the action, not the agent; file retention, naming, and archive follow `docs/README.md`. **Read `docs/README.md` in full before creating, moving, or deleting any file in `docs/`.**

#### Docs/ placement rules (mandatory)

**Where new files go** — purpose-based folders only:
- `docs/work/plans/milestone_v<m#>/<phase>/` or `cross_cutting/<topic>/` — implementation, remediation, execution plans
- `docs/work/reviews/milestone_v<m#>/<phase>/` or `cross_cutting/<topic>/` — reviews, audits, verification reports, findings
- `docs/work/designs/milestone_v<m#>/<phase>/` or `cross_cutting/<topic>/` — design docs, strategy alternatives, pre-implementation artifacts
- `docs/runbooks/<category>/` — operational procedures
- `docs/archive/` — only after explicit user approval

**Do NOT write to these legacy paths** (no new files unless completing already-started work in that exact path):
- `docs/superpowers/` · `docs/user_plans/` · `docs/plans/` · `docs/findings/` · `docs/migration/` · `docs/brainstorms/`

**Do NOT:**
- Nest plans inside designs (no `docs/work/designs/plans/`) or vice versa.
- Create folders named after an agent, skill, workflow, or tool.
- Use dash-encoded phase numbers — use `20.5`, not `20-5`.
- Use bare filenames like `review1.md`, `final.md`, `notes.md`, or filenames with spaces.

#### Frontmatter rules

All new files under `docs/work/` must have this frontmatter block:

```yaml
---
status: active | consumed | retirement-proposed | archived | retained
purpose: implementation-plan | review-findings | verification-report | design | runbook | governance | migration | other
created: YYYY-MM-DD
milestone: v#.# (or "untracked")
phase: <phase-topic-slug> (or "cross-cutting")
retirement_trigger: <free text describing when this file is no longer needed>
---
```

Allowed `status` values: `active`, `consumed`, `retirement-proposed`, `archived`, `retained`. Do NOT use: `complete`, `completed`, `draft`, `superseded`, or any qualified string.

#### Execution, review, and commit rules

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

**`sampling_method.md` status (user directive 2026-06-10):** This file is the completed
instruction document that generated the now-finished `simulation_data/` dataset. The generation
work is done and will not be re-run, so `sampling_method.md` is **frozen by default** — it is NOT
an active design-revision target for v1.5 or later milestones. It remains authoritative as the
historical record of how the existing training data was produced. It may be revised ONLY on
explicit user instruction, triggered by verified data-feasibility issues (dataset ↔ framework
incompatibilities that must be fixed to make the existing data trainable). Note that no dedicated
phase or milestone has yet verified dataset ↔ framework compatibility; `data_quality_assessment.md`
(in `framework-revisions/`, a research report — not an authoritative spec) may cover parts of that
ground and is to be characterized, not edited, during v1.5.

**v1.3-era live code is NOT a grounding source** (user directive 2026-05-19): `pinn/data-processing-pipeline-full.py`, `pinn/basic_architecture.py`. These files are NOT evidence, NOT source-of-truth for any v1.4 spec decision. They may be referenced ONLY in forward-pointing FUT-01 hand-off documents (`NN-CODE-DIVERGENCE.md`, eventual `pinn/STATUS.md`).

**SCOPE-05 data-generation carveout:** `simulation_data/Scripts/ic_generation/` is a permitted
grounding source for data-generation specs in
`pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`. This is a narrow
carveout from the `pinn/` no-live-code directive, not a general live-code exception. The
canonical rule lives in `.planning/REQUIREMENTS.md` SCOPE-05.

For repo layout, command reference, dataset internals, and PINN architecture details: see `.claude/rules/` (path-scoped rules loaded by Claude Code when working in relevant directories; also readable directly by any agent).
