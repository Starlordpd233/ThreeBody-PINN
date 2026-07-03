<!-- generated-by: gsd-doc-writer -->
# Development

This document covers the day-to-day developer workflow for working on the CTL-PINN
three-body simulation and training stack. It is the operational companion to
`docs/ARCHITECTURE.md` (system structure) and `docs/CONFIGURATION.md` (config
layers). For first-run and prerequisite instructions, see `docs/README.md`; for
contribution and PR process, see `docs/git-guidelines.md` and the
governance section in `AGENTS.md`.

The repository is not a typical web-service project. There is no top-level
`package.json`, `Makefile`, or package manager. The "build" is the Brutus C++
integrator (its own `makefile` lives in `brutus_Newton-main/`). The "tests" are
the GSD phase verification artifacts and the Brutus CLI runs. Almost all
developer actions are governed by a small set of scripts, hooks, and planning
artifacts under `.planning/`. This file is the entry point for that workflow.

## Local Setup

A fresh checkout needs four things configured before any development work
proceeds safely.

1. **Working tree state.** Run `git status --short --branch` and confirm the
   branch and ahead/behind state. The current development branch is
   `milestone/v1.6` (in an isolated worktree); protected branches `master`, `main`, and `milestone/*`
   must not be pushed from directly.
2. **Hooks path.** Run `scripts/setup-git-hooks.sh` once after cloning so that
   `git config --get core.hooksPath` returns `.githooks`. Hooks enforce
   commit-message format, agent attribution, owned-path staging, and the
   destructive-operation guards described in `docs/git-guidelines.md`. Do
   **not** use `--no-verify` or any equivalent bypass.
3. **Environment variables and Brutus build.** Brutus depends on GMP and MPFR
   for arbitrary-precision arithmetic. The C++ build and the Python pipeline
   do not require a `.env` file; the project's "configuration" is distributed
   across framework specs, pipeline scripts, and the Brutus makefile (see
   `docs/CONFIGURATION.md`). Build the C++ side once with
   `brutus_Newton-main/makefile` before invoking any Brutus runner.
4. **Pre-existing changes.** Any uncommitted files at session start are
   user-owned unless you created them in the current task. Surface them in
   your session-start report and never fold them into your own commits.

The dataset under `simulation_data/` is large and gitignored. Restore it from
the workstation backup per `docs/runbooks/migration/exact-state-mac-migration.md`
if you are on a new machine; otherwise, expect the Python pipeline to discover
the expected directory layout but no payload.

## Project Commands

There is no central `scripts` block. Commands group by subsystem.

| Command | Description |
|---|---|
| `git status --short --branch` | Surface branch and working-tree state; mandatory at session start and before any commit. |
| `scripts/setup-git-hooks.sh` | One-time install of `.githooks/` paths. Run after cloning. |
| `scripts/agent-commit` | The only commit entry point agents may use. Wraps `git commit` with owned-path, attribution, and lock checks. Raw `git commit` is blocked by lifecycle hooks. |
| `brutus_Newton-main/makefile` (`make`) | Builds the C++ arbitrary-precision N-body integrator. The integrator is the ground-truth engine; every Brutus runner script depends on the built binary. |
| `python simulation_data/Scripts/ic_generation/generate_ics.py` | Generates initial conditions (ICs) for the dataset. |
| `python simulation_data/Validation/prescreening/stage2_prescreening_revised_auto.py` | Runs the Stage 2 prescreening pass. |
| `python simulation_data/Scripts/brutus_runners/run_brutus_both_type_simple.py` | Standard Brutus batch runner (hierarchical + flat). |
| `python simulation_data/Scripts/brutus_runners/run_brutus_hierarchical_only_mac_gold_standard.py` | Gold-standard hierarchical runner. |
| `python simulation_data/Scripts/metrics_calculation/calculate_metrics.py` | Computes validation metrics (SCS, SASD, IPR, PSC) over simulated trajectories. |

## Code Style

This repository has no JavaScript/TypeScript linter, formatter, or test
runner. Code style is enforced by:

- **Git policy** (`docs/git-guidelines.md`). All commits are checked by
  `.githooks/commit-msg` for message format, body requirements on
  `spec`/`evidence`/`verify`/`plan` types, and agent attribution. The
  `pre-commit` hook blocks generated, scratch, and oversized artifacts; the
  `pre-push` hook blocks direct pushes to protected branches. There is no
  `--no-verify` escape for agents.
- **Agent-owned paths.** Every commit must set `GIT_AGENT_ID` and
  `GIT_AGENT_OWNED_PATHS` env vars when invoking `scripts/agent-commit`.
  Broad staging (`git add .`, `git add -A`, `git add -u`) is forbidden. Stage
  only the paths your agent is responsible for.
- **Spec-edit discipline.** Framework-spec edits are limited to
  `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
  and `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
  (SCOPE-13 in v1.6). `sampling_method.md` is frozen by default
  (user directive 2026-06-10) and `data_quality_assessment.md` is read-only
  research-report material; both are not active design-revision targets. The
  Brutus C++ build (`brutus_Newton-main/`) and the on-disk dataset
  (`simulation_data/`) are also out of spec-edit scope.
- **Live-code ban in `pinn/`.** Files under `pinn/` (notably
  `pinn/basic_architecture.py` and `pinn/data-processing-pipeline-full.py`)
  are **not** a grounding source for any spec decision; they are v1.3-era
  reference material (user directive 2026-05-19). Forward-pointing
  references are permitted only in `pinn/STATUS.md` (future) and
  `NN-CODE-DIVERGENCE.md` handoff documents.

## Branch Conventions

The branch model is:

- **`master`** is the integration trunk. v1.0–v1.5 are merged here. Direct
  push to `master` is blocked by `pre-push` and is never the path a
  developer takes.
- **`milestone/vN.N`** is the local integration branch for a milestone
  (current: `milestone/v1.6`, in an isolated worktree). v1.6 was cut from the
  v1.5 deliverable tip `88aa1e4f` and rebased onto the completed `master`
  after v1.5 shipped. All v1.6 work lives here. The `pre-push` hook blocks
  direct pushes from any `milestone/*` branch.
- **Feature / review branches** carry work between agents and toward
  publication. PRs are opened from these branches, not from the milestone
  branch.

Tagging convention: a `v1.6-pre-phase-NN` tag is cut from `milestone/v1.6`
before each phase starts, so a phase's work can be retrieved in isolation.
The milestone closes with a `--no-ff` merge of `milestone/v1.6` into
`master` (user-owned final step).

Red-flag branches `backup/*`, `recovery/*`, `wip/*`, `experiment/*`, and
`tmp/*` are pause-and-ask territory: do not commit, push, or do destructive
work on them without first confirming with the user.

## PR Process

The repository does not currently host a `.github/PULL_REQUEST_TEMPLATE.md`.
The PR process is therefore governed by the project's own git policy
(`docs/git-guidelines.md`) plus the `CONTRIBUTING.md` guide. The summary:

1. **Surface git state first.** `git status --short --branch`, then
   `git diff --cached`, then any unstaged diffs for files you touched. Treat
   anything not created in this session as user-owned.
2. **Work on the right branch.** If the change is a v1.6 spec edit, you
   are on `milestone/v1.6`. If the change is documentation or runbook, you
   are on a feature branch off the milestone branch.
3. **Run the verification gate that matches the change.** For a spec edit,
   the relevant Phase verification plan (the phase's `NN-VERIFICATION.md`). For a
   Brutus change, the C++ build + the relevant Brutus runner. For a docs
   change, the `docs/` lifecycle per `docs/README.md`.
4. **Commit atomically via `scripts/agent-commit`.** One commit per logical
   change. Set `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS`. Include
   `Agent-Assisted-By:` or `Co-Authored-By:` trailer for agent-authored
   commits. Required body for `spec`, `evidence`, `verify`, `plan`, and any
   commit touching `pinn_instruction/`, `.planning/`, framework specs, or
   governance instructions.
5. **Open the PR from a feature branch** (not the milestone branch). Wait
   for review. Do not push to `master` directly.

## GSD State Machine

Project work is organized by the GSD planning artifacts under `.planning/`.
The current state is at `.planning/STATE.md`; it lags reality after a phase
boundary and must be manually advanced.

Key artifacts:

- `.planning/PROJECT.md` — project identity, core value, and key decisions.
- `.planning/REQUIREMENTS.md` — the current-milestone requirements ledger
  (v1.6: 32 entries across PKG/EVID/CURR/LOOP/LOSS/VER; v1.5's 36-entry
  ledger is archived at `.planning/milestones/v1.5-REQUIREMENTS.md`).
- `.planning/ROADMAP.md` — milestone and phase plan.
- `.planning/STATE.md` — current position. **Manually advanced** after
  each phase; the three GSD query tools disagree on `current_phase`, so
  verify phase directories on disk rather than trust any single tool.
- `.planning/milestones/v1.6-GAPS.md` — milestone-wide gap index for the
  current milestone (created on the first v1.6 gap; none arose in Phases
  30–31). The v1.5 index (`v1.5-GAPS.md`, ten gaps all
  RESOLVED-WITH-INSTRUCTION) is archived.
- `.planning/research/edl/` — non-canonical Empirical Decision Loop
  research-support briefs for empirically consequential source-silent
  gaps. The phase-local gap register remains the authoritative blocking
  and resolution record; EDL briefs do not authorize a numeric default
  or a spec edit without user instruction.

The state machine is operated by hand. There is no automatic GSD runner
in this repository.

## STOP Protocol and the Gap Register

This is a "similar adjudication milestone" repository (v1.4, v1.5, and v1.6 per
`AGENTS.md` governance). Spec work, adjudication, and cross-phase
reframing are governed by the STOP protocol. A decision is "grounded" only
if it is explicitly answered by one of:

- A resolution doc under
  `pinn_instruction/markdown_conversion/framework-revisions/research_reports/`
  (e.g. `03-curriculum-and-training-loop/research_result/03-final-resolution.md`
  for v1.6).
- The corresponding issue doc (e.g.
  `pinn_instruction/issues/03-curriculum-and-training-loop.md`).
- A prior user decision in chat, a `RESOLVED-WITH-INSTRUCTION` gap entry,
  or an `NN-CONTEXT.md` decision marked `LOCKED`.
- A planning artifact: `.planning/REQUIREMENTS.md` requirement,
  `.planning/ROADMAP.md` success criterion, `.planning/PROJECT.md` Key
  Decision.
- A framework spec section **only when that section was revised during
  v1.4, v1.5, or v1.6** (i.e., touched by an applied plan in this milestone).
  Pre-v1.4 framework spec content is not a grounding source.
- First-principles physics or short uncontroversial math (long or
  contested derivations must be surfaced as a gap).

`pinn/` live code is explicitly not a grounding source. The on-disk
dataset (`simulation_data/`) and `simulation_data/Scripts/` are grounding
(SCOPE-06/07).

When a gap is detected:

1. **STOP the affected work immediately.** No exceptions.
2. **Verify the agent understands the decision space** (math/physics,
   downstream consequences, source silence). If understanding is
   insufficient, surface that as a question rather than recording a gap.
3. **Record the gap** in the phase-local register
   (`.planning/phases/NN-*/NN-GAPS.md`) with all required fields:
   decision point, where in artifact, task context, classification
   (semantic / operational coordination / process-artifact schema /
   cross-phase reframing), source silence, mathematical/engineering
   grounding, what the agent was tempted to decide, what the user needs
   to decide (concrete A/B/C options), confidence of impact, status
   `OPEN`, and a resolution note.
4. **Update the milestone-wide index** at
   `.planning/milestones/v1.6-GAPS.md`.
5. **Surface to the user** via the active workflow channel. Halted work
   stays halted until the user provides instruction. Update status to
   `RESOLVED-WITH-INSTRUCTION` (or `DEFERRED`) when instruction arrives.

Subagents do not write gap registers directly. They return findings to
the parent agent, which decides whether a finding rises to a gap and logs
it.

## Specwork and Trainex Tracks

Development splits into two user-defined tracks (per
`.claude/rules/repo-map.md`):

- **specwork** — the framework-specs design/editing stage: authoring and
  adjudicating `ctl_instruction.md` and `pinn_architecture.md`. This is
  the v1.4 / v1.5 / v1.6 (doc-03) scientific-backbone track. Spec edits
  land only on the two spec files above; all other spec content is
  frozen, read-only, or characterized-not-edited.
- **trainex** — the training-execution / reality-pipeline development:
  the user runbook, the PH-1..PH-10 research placeholders, and the
  future build of the training pipeline + PINN code (FUT-01 / FUT-04).
  Reference design at
  `docs/work/designs/cross_cutting/training-execution/2026-06-10-training-execution-design.md`.
  Research packages for trainex decisions live at
  `pinn_instruction/markdown_conversion/framework-specs/trainex-<id>/`,
  numbered as research rounds (`trainex-r1/` = foundational round,
  `trainex-r2/` = post-framework tuning round).

When the user says "specwork" or "trainex", they mean these tracks.

## External Research Workflow (ERW)

Both tracks delegate research-grade decisions to external AI research
agents via ERW, the canonical runbook at
`docs/runbooks/external-research/2026-06-11-external-research-workflow.md`.
Read that runbook before assembling any external research package.

The flow: **GATHER -> PACKAGE -> HANDOFF -> RESULTS -> USE**. Every round
creates a `DELIVERY-NOTE.md` (user-only, holds repo paths), a shared
`specs/` snapshot set at the round root, and one or more
`research_package[_a|_b]/` sub-packages, each with a
`RESEARCH-CONTEXT-MASTER.md` (uploaded entry point) and a
`RESEARCH-AGENT-PROMPT.md` (paste-ready prompt + attach list).

Critical rules:

- **Zero repo paths in any authored upload.** External agents have no
  codebase access; refer to companion files by bare filename only.
  Verbatim snapshot cross-references in `specs/` are exempt (snapshots
  are commit-pinned; scrubbing them breaks fidelity).
- **One shared `specs/` per round.** Never duplicated per sub-package;
  attach-lists in each prompt's header do the routing.
- **Pin snapshots to a commit hash** in the master frontmatter
  (`source_baseline`). Refresh snapshots if a source document is edited
  after packaging.
- **Channel separation is absolute.** specwork (spec adjudication) and
  build-design (e.g. trainex) packages do not share evidence. If
  evidence is needed in both, route it as a separate EDL-style support
  brief through the specwork channel.

Two channels with different report standing:

- **specwork** (issue-doc resolutions): package at
  `framework-revisions/research_reports/<NN-issue-slug>/`. The report is
  a **candidate verdict source** — transcribed unless evidence shows a
  position fails; never authoritative; full verification protocol
  applies.
- **build-design** (e.g. trainex): package at
  `framework-specs/<track>-<round>/` (e.g. `trainex-r1/`). The report
  delivers **options menus + findings, not verdicts** — the user fills
  a decision sheet; the picks (recorded as Key Decisions) are the
  decisions; the report is not a grounding source for spec
  adjudication.

## Phase Verification Discipline

Every v1.6 adjudication phase (Phases 32-36) follows the same loop:
**adjudicate -> fix -> verify -> re-verify after every batch -> close
only when the acceptance check passes**. The issue ledger lives at a
stable path under the Phase 32 (evidence-framework) directory, stood up
and operated through the protocol established in Phase 32.

Evidence-packet rules (EVID-11): Phase 32 authors the evidence packets
and verdicts for the headline conflicts (D-04 causal mode, D-05 s_min
frame, D-06 epsilon strategy, the M14 gradient-clipping divergence, and
the `D = 6.694` vs v1.5-locked `D ≈ 4.6416` reconciliation, EVID-15).
Packets for the remaining findings may be authored by the owning contract
phase (33-35) **immediately before** its spec edits, recorded as a
STOP-resolved split where the source materials do not pre-specify it.

Each spec-edit commit wires the affected ledger rows in the same commit.
Phase exit happens only at VERIFIED or DEFERRED status. (The v1.5 analog —
Phases 23-29, ledger seeded by Phase 24, EVID-10 conflict verdicts owned by
Phase 25 — is archived under `.planning/milestones/v1.5-*`.)

## Destructive Operations

Before any destructive Git command, do all of:

1. Explain what the operation will affect (commits, refs, working-tree
   files, stashes, tags).
2. Obtain exact user approval naming either the exact command or the
   exact effect. Vague approval is not enough.
3. Create or verify a recovery checkpoint (backup branch, tag, stash,
   or commit ref).
4. Include all three markers in the command:
   `ALLOW_DESTRUCTIVE_GIT=1`, `GIT_DESTRUCTIVE_APPROVAL='<exact
   approved command or effect>'`, `GIT_RECOVERY_CHECKPOINT='<ref>'`.
   `ALLOW_DESTRUCTIVE_GIT=1` is machine-readable; it does not replace
   the chat approval requirement.

Destructive operations include `git reset --hard`, `git clean -f`,
`git branch -D`, `git rebase`, `git push --force`, `git stash drop`,
disabling hooks, and `rm -rf` on tracked paths. If the user reports
lost work, perform read-only forensics first (`git reflog`, `git fsck`,
`git stash list`, `git worktree list`) and present recovery options
before changing state.

## Concurrent Agent Work

Multi-agent setups (Claude Code CCP or any worktree-shared model) must:

- Prefer separate worktrees and branches per independent agent.
- Declare disjoint owned paths per agent and set `GIT_AGENT_OWNED_PATHS`
  on every commit.
- Re-run `git status --short --branch`, `git diff --cached`, and
  relevant unstaged diffs immediately before commit.
- Serialize commits through `scripts/agent-commit` (it takes a
  repository-local lock). If the lock is held, wait or retry.
- Never alter another agent's staged or unstaged work unless explicitly
  assigned.

## Capture and Recovery Ladder

Use the lightest mechanism that preserves the right state:

1. **Completed logical work** -> commit it.
2. **Risky history or branch operations** -> create a backup branch or
   tag first.
3. **Dirty unfinished work** -> use a stash or durable patch snapshot
   when a commit is not appropriate.
4. **Suspected lost work** -> read-only forensics before changing
   state.

Do not rely on `/tmp` for evidence or recovery material that must
survive the task. When a commit asserts a verifiable invariant
(byte-for-byte preservation, hash match, count), record the
supporting hashes or counts in committed state, not `/tmp`, so the
claim is re-derivable.

## Next Steps

- First-run and prerequisites: `docs/README.md`.
- System structure: `docs/ARCHITECTURE.md`.
- Configuration layers: `docs/CONFIGURATION.md`.
- Spec-edit targets and frozen/read-only files: SCOPE-08 / SCOPE-09
  in `.planning/REQUIREMENTS.md`.
- External research packaging: `docs/runbooks/external-research/2026-06-11-external-research-workflow.md`.
- Git policy in full: `docs/git-guidelines.md`.
- Phase gap registers: `.planning/phases/NN-*/NN-GAPS.md`; current
  milestone index: `.planning/milestones/v1.6-GAPS.md`.
- New Mac migration restore: `docs/runbooks/migration/exact-state-mac-migration.md`.
