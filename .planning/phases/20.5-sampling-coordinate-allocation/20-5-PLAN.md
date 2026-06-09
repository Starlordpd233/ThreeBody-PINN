# Phase 20.5: Sobol Coordinate Allocation — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. No other plan-execution skill (in particular, the worktree-based alternative) is supported for this plan.

## Plan Parts and Execution Order

This plan is split across four files. Execute them in order; each part file is dispatched
**with this index attached** so the executor has the full context.

| Tasks | File |
| --- | --- |
| Task 0 (preflight), Post-Completion Follow-ups, Self-Review | This index (`20-5-PLAN.md`) |
| Tasks 1–4 (Planning & Governance Scaffolding) | `20-5-PART1.md` |
| Tasks 5–8 (Spec Edits & Verification) | `20-5-PART2.md` |
| Task 9 (Closure & Status Synchronization) | `20-5-PART3.md` |

**Execution order:** run Task 0 to green first, then execute `part1` → `part2` → `part3` in
order. All four files are required to complete Phase 20.5. After Task 9, return to this index
for Post-Completion Follow-ups and the Self-Review.

**Plan-files-committed precondition:** all four plan files (`20-5-PLAN.md`,
`20-5-PART1.md`, `20-5-PART2.md`, `20-5-PART3.md`) must be committed and the
working tree clean with respect to them before Task 0 begins. Execution must never start from
an uncommitted or stale plan revision. Task 0 verifies this as its first step.

**Goal:** Lock the Sobol coordinate allocation convention in `sampling_method.md` so it is
explicit, non-overlapping, and matches `simulation_data/Scripts/ic_generation/ic_generation_utils.py`,
resolving the `u_4` double-booking between scaling and velocity sampling.

**Architecture:** This plan implements GSD Phase 20.5 (inserted between Phase 20 and
Phase 21 of v1.4). It is authored via `superpowers:writing-plans` per user directive
2026-05-19, made state-aware on 2026-06-06 after Phases 17–20 executed, and hardened
on 2026-06-07 after Phase 20.5 plan-review reports were verified against live repository
state. Task 0 runs a plan-level preflight that verifies live repository state before any
mutation. Tasks 1–2 make REQUIREMENTS and ROADMAP state-aware in dependency order: Task 1
creates SAMP-01, SAMP-02, and SCOPE-05 in `REQUIREMENTS.md` and bumps the coverage totals in
both `REQUIREMENTS.md` and `ROADMAP.md` (the Phase 20.5 list item and progress row already
exist from prior status work; only the requirements, scope rule, and coverage content are
new). Task 2 inserts the ROADMAP details block **after** those requirements exist, and
correctly declares dependencies on Phase 18's FRAME contract and Phase 19's
preprocessing-scaling contract. Task 3 propagates the SCOPE-05 governance rule after it
exists in REQUIREMENTS and before risk-elevated spec edits. Task 4 verifies the
already-existing gap registers (verification-only — they were created and resolved on
2026-05-19). Task 5 applies the five spec edits and runs the FLAG-10 cross-reference check
now that Phases 18–19 are complete. Task 6 runs a three-surface disposable verification
probe (static spec, entrypoint AST, sampler behavior). Task 7 creates the data-alignment
hand-off with an expanded AC-SAMP-01 that mirrors the three-surface probe and a scoped
provenance claim (alignment of spec, documented generator configuration, and current sampler
behavior — no in-repository manifest proves the exact script revision for every stored data
file; no regeneration is required to resolve this coordinate-allocation mismatch; this is
not a blanket historical-provenance certification). Task 8 verifies that no separate
velocity-momentum finding is needed (Phase 18 already reconciled the spec prose to the
code). Task 9 reruns the expanded AC-SAMP-01 probe, verifies the handoff contains both the
scoped no-regeneration conclusion and the historical-provenance caveat, and performs final
closure/status synchronization after all Phase 20.5 deliverables pass. Each part file ends
with a completion gate that the next part's precondition requires before it may start. The locked
convention is "Option A" — the conditional `(δ_s, δ_v)` allocation that the existing
standard quasi-random dataset was generated under. Full rationale:
`.planning/phases/20-5-sampling-coordinate-allocation/20-5-RESEARCH.md`.
Research extraction: `20-5-RESEARCH.md` (GSD-native rationale and source map for execution;
use the Non-Execution Guard above for grounding authority).
Gap register: `20-5-GAPS.md`.

**Tech Stack:** Markdown framework specs; `.planning/` GSD artifacts; one Python
verification probe run with the project virtual environment (`.venv/bin/python3`, `numpy`,
`scipy.stats`).

---

## Non-Execution Guard

**This plan is not executable until its own Task 0 preflight passes.** Read and obey these
rules before touching any file:

- **Use explicit file paths for all Phase 20.5 work.** Do **not** rely on `find-phase 20`,
  `init.phase-op 20`, or any other GSD phase-number tooling: a known Phase 20 / Phase 20.5
  resolution hazard means `find-phase 20` and `init.phase-op 20` can resolve to the
  Phase 20.5 directory. This hazard is recorded in `.planning/milestones/v1.4-GAPS.md`.
- **Run Task 0 before mutating any file.** If any Task 0 check has drifted from the state this
  plan assumes, update the affected task instructions before proceeding.
- **STOP, do not invent.** If any semantic or process-artifact decision is not already
  grounded by the existing gap register (`20-5-GAPS.md`), the milestone index
  (`v1.4-GAPS.md`), `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`,
  `.planning/PROJECT.md`, the issue/resolution sources allowed by the root governance
  instructions, or a prior user instruction, follow the `CLAUDE.md` STOP protocol instead of
  choosing a default. Review reports under `docs/findings/` are audit inputs only; use them to
  identify hazards, not as authority for resolving source-silent semantic or process decisions.
- **Do not rename `GAP-20-5-0X` IDs.** They are historical resolved gap IDs. Directory/path
  migration to dot-decimal `20.5-*` is out of scope for this plan unless the user separately
  authorizes workflow repair.
- **Commits:** use `scripts/agent-commit` with `GIT_AGENT_ID` set; never raw `git commit`,
  never `--no-verify`. Commit scopes must pass `scripts/git_policy/validate_commit_msg.py`
  (`20-5` is **not** a valid scope — use `planning`, `governance`, or `spec`).

## Git context

- **Branch:** `milestone/v1.4` (correct branch for v1.4 spec work — not a red-flag branch).
- **Commit cadence:** One atomic commit per *mutating* task (Tasks 1, 2, 3, 5, 6, 7, 9).
  Tasks 0, 4, and 8 are verification-only and produce **no commit**. `.planning/` and
  `pinn_instruction/` are risk-elevated paths (per `CLAUDE.md`) — each mutating task commits
  its full change set at task end with a body.
- **Commit tool:** use `scripts/agent-commit` with the environment variable `GIT_AGENT_ID`
  set to the **executing agent's actual identity** (for example `claude-opus-4-5`,
  `codex-gpt-5`, `gemini-2.5-pro`, etc. — whatever tool is actually performing the commit).
  The commit script adds the `Agent-Assisted-By` trailer from this value. Never raw
  `git commit`, never `--no-verify`. Run
  `scripts/setup-git-hooks.sh` first if `git config --get core.hooksPath` is not `.githooks`.
- **Staging:** `git add` with explicit file paths only — never `git add -A` or `git add .`.
  Surface any pre-existing unrelated working-tree changes and exclude them from staging.
- **No destructive operations** anywhere in this plan. No resets, rebases, force-pushes,
  branch deletions, or history rewrites. If any task appears to need one, STOP and surface.

### Mandatory per-commit gate

Every mutating task (Tasks 1, 2, 3, 5, 6, 7, 9) must run this gate around each commit. The
gate is part of the task; skipping any sub-step invalidates the commit:

1. **Pre-stage index check:** `git diff --cached --name-only` must print nothing. If the
   staged index is non-empty, STOP — an earlier step left a stray staged file; resolve it
   without altering any pre-existing user staging.
2. **Unstaged diff review:** `git diff -- <file1> <file2> ...` for exactly the files this
   task owns. Confirm the changes match the task's declared edits. If unrelated changes
   appear in these files, STOP — they are user-owned and must not be bundled.
3. **Stage only the declared files:** `git add <file1> <file2> ...` using the exact paths
   listed in the task's commit step. Never use a directory path or `.`.
4. **Staged-list confirmation:** `git diff --cached --name-only` must equal the task's
   expected file set exactly — no more, no fewer.
5. **Cached-diff inspection and whitespace check:**
   `git diff --cached` must match the task's expected diff; `git diff --cached --check`
   must print no whitespace errors.
6. **Rerun task verification:** rerun the task's own verification checks (the bash blocks
   earlier in the task) against the staged content. They must still pass.
7. **Commit:** `GIT_AGENT_ID="$GIT_AGENT_ID" scripts/agent-commit -m "<type>(<scope>): <subject>" -m "<body>"`.
   Never use `--no-verify`.
8. **Post-commit confirmation:** `git diff --cached --name-only` must again print nothing
   (the commit drained the index); `git show --stat HEAD --name-only` must list exactly the
   expected file set. If a pre-commit hook rejected the commit, surface the rejection and
   do not proceed.

The gate's purpose is to guarantee that every Phase 20.5 commit contains only the files it
declares, that no pre-existing user staging is silently captured, and that every commit is
immediately verifiable against its task's checks.

## File Structure

**Created (this execution):**
- `.planning/phases/20-5-sampling-coordinate-allocation/20-5-DATA-ALIGNMENT.md` — FUT-01
  hand-off documenting spec↔`simulation_data` alignment; contains the `AC-SAMP-01` stub
  (Task 7).
- `.planning/phases/20-5-sampling-coordinate-allocation/probes/verify_sobol_allocation.py`
  — disposable verification probe (VER-01-style) (Task 6).

**Verified pre-existing (created/resolved 2026-05-19, not recreated):**
- `.planning/phases/20-5-sampling-coordinate-allocation/20-5-GAPS.md` — phase-local gap
  register (GAP-20-5-01/02/03 at `RESOLVED-WITH-INSTRUCTION`). Task 4 verifies it; it is not
  rewritten.
- `.planning/milestones/v1.4-GAPS.md` Phase 20.5 section — already present; `total_gaps` /
  `resolved_gaps` already equal 21 and already include the three Phase 20.5 gaps. Task 4
  verifies internal consistency and makes **no** frontmatter change.

**Not created (resolved by Phase 18):**
- `docs/findings/velocity_momentum_sampling_discrepancy.md` is **not** created. Phase 18
  (FRAME-03) already reconciled the momentum-conservation prose in `sampling_method.md` to
  the code's symmetric `v1 = v3 = -v2/2` split, so the May 2026 sub-conflict no longer
  exists. Task 8 verifies this rather than recording a stale open finding.

**Modified:**
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` — Edits 1–5
  (Task 5). Edits 1–4 FROM text still matches live; Edit 5's FROM/TO were re-grounded to the
  current Phase 18 momentum wording.
- `.planning/ROADMAP.md` — Phase 20.5 list item and progress row already exist (Task 2
  verifies them); **insert** the absent Phase 20.5 details block (Task 2) **after** SAMP-01/02
  and SCOPE-05 have been added to REQUIREMENTS by Task 1; the coverage bump 30/30→32/32 is
  made in Task 1 together with the SAMP-01/02 additions that justify it.
- `.planning/REQUIREMENTS.md` — add SAMP-01/02; amend SCOPE-02; add SCOPE-05; traceability
  rows; coverage 30→32 in both REQUIREMENTS.md and ROADMAP.md (Task 1), then final
  SAMP-01/02 traceability closure to `Complete` after the Phase 20.5 deliverables pass (Task 9).
- `.planning/STATE.md`, `.planning/MILESTONES.md`, and `.planning/PROJECT.md` — narrow
  execution-complete status synchronization only after Phase 20.5 passes (Task 9). Do not
  duplicate the older design/plan-lock status already recorded by `a9ecd51`.
- Root agent instructions — SCOPE-05 governance propagation (Task 3). `CLAUDE.md` and
  `GEMINI.md` are **symlinks to `AGENTS.md`**; the real edit targets are `AGENTS.md` and
  `ANTIGRAVITY.md` (a separate file). Do not edit or stage `CLAUDE.md`/`GEMINI.md` separately.

**Commit-lineage note:** commit `a9ecd51` recorded Phase 20.5 *status* in `.planning/PROJECT.md`,
`.planning/STATE.md`, and `.planning/MILESTONES.md` — do not duplicate those status updates.
Commit `b727b15` is the Phase 20.5 *design/plan-lock* lineage (referenced by the ROADMAP list
item). Treat the two by role; do not blindly rewrite one to the other.

**Responsibility boundaries:** the spec file holds the convention; the gap register holds
the decision audit trail; the data-alignment doc holds the FUT-01 hand-off and acceptance
check. Each is independently reviewable.

---

## Task 0: Plan-level preflight (run before mutating any file)

**Files:** none modified. This task is verification-only; it produces no commit.

Run every check below from the repository root. If any check has drifted from the state this
plan assumes, **stop and update the affected task instructions before proceeding** — do not
execute a downstream task against drifted state.

- [ ] **Step 0a: Plan-files-committed precondition**

Confirm all four plan files are committed and the working tree is clean with respect to them:
```bash
for f in \
  .planning/phases/20-5-sampling-coordinate-allocation/20-5-PLAN.md \
  .planning/phases/20-5-sampling-coordinate-allocation/20-5-PART1.md \
  .planning/phases/20-5-sampling-coordinate-allocation/20-5-PART2.md \
  .planning/phases/20-5-sampling-coordinate-allocation/20-5-PART3.md
do
  git diff --name-only HEAD -- "$f"
  git diff --cached --name-only -- "$f"
done
```
Both loops must print nothing. If any plan file has uncommitted or staged-but-not-committed
changes, STOP — execution must not start from an uncommitted or stale plan revision.

- [ ] **Step 0b: Export `GIT_AGENT_ID`**

The commit gate in every mutating task requires `GIT_AGENT_ID` to contain the executing
agent's actual identity (for example `claude-opus-4-5`, `codex-gpt-5`, `gemini-2.5-pro` —
whatever tool is performing the commit). Set and export it for the shell session before any
Task 1 work begins:
```bash
export GIT_AGENT_ID="<actual-agent-identity>"   # e.g. claude-opus-4-5
echo "GIT_AGENT_ID=$GIT_AGENT_ID"
```
If `GIT_AGENT_ID` is unset or empty at Task 1 entry, STOP. Every `scripts/agent-commit`
invocation in this plan reads this environment variable; no task may substitute a hardcoded
value.

- [ ] **Step 1: Working tree and branch**

```bash
git status --short --branch
```
Confirm the branch is `milestone/v1.4`. Note any pre-existing unrelated changes (the working
tree may already carry user-owned edits) — these MUST be excluded from every Phase 20.5
commit; each task stages only its own named files.

Two additional constraints at this step:

1. **The staged index must be globally empty.** Run:
   ```bash
   git diff --cached --name-only
   ```
   Expected: no output. If anything is staged, STOP and surface the staged files to the user.
   Do not reset, unstage, or otherwise alter any pre-existing user staging — the Phase 20.5
   execution halts until the user clears the index or authorizes a path forward. The
   per-commit gate in every mutating task re-checks this invariant before staging.

2. **Every Phase 20.5 target file must have no staged or unstaged diff.** Run:
   ```bash
   for f in \
     .planning/ROADMAP.md \
     .planning/REQUIREMENTS.md \
     AGENTS.md \
     ANTIGRAVITY.md \
     pinn_instruction/markdown_conversion/framework-specs/sampling_method.md \
     .planning/STATE.md \
     .planning/MILESTONES.md \
     .planning/PROJECT.md
   do
     git diff --cached --name-only -- "$f"
     git diff         --name-only -- "$f"
   done
   ```
   Expected: no output on either loop. If any target file has a staged or unstaged diff, STOP
   and surface it as pre-existing user-owned work; update the affected task instructions or get
   user guidance rather than silently bundling pre-existing edits into a Phase 20.5 commit. Do
   not reset or alter the pre-existing change.

As of the 2026-06-07 plan-review pass, these risk-elevated files had user-owned edits outside
Phase 20.5:
```text
pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
```
If they still appear in `git status`, leave them untouched and never stage them. Every `git add`
in this plan names exact files; never use `git add pinn_instruction/`, `git add .`, or
`git add -A`.

- [ ] **Step 2: Hook path**

```bash
git config --get core.hooksPath
```
Expected `.githooks`. If it is anything else, run `scripts/setup-git-hooks.sh` before any
commit. All commits in this plan use `scripts/agent-commit` with `GIT_AGENT_ID` set.

- [ ] **Step 3: Commit-lineage roles**

```bash
git cat-file -t a9ecd51
git cat-file -t b727b15
```
Both must print `commit`. Treat `a9ecd51` as the **status-record** commit (Phase 20.5 status
in `PROJECT.md`/`STATE.md`/`MILESTONES.md`) and `b727b15` as the **design/plan-lock** commit.
Do not rewrite references to one as the other.

- [ ] **Step 4: Root-instruction symlink topology**

```bash
ls -l AGENTS.md CLAUDE.md GEMINI.md ANTIGRAVITY.md
```
Confirm `CLAUDE.md` and `GEMINI.md` are symlinks to `AGENTS.md`, and `ANTIGRAVITY.md` is a
separate regular file. Task 3 edits `AGENTS.md` and `ANTIGRAVITY.md` only; it must not edit or
stage `CLAUDE.md`/`GEMINI.md` separately.

- [ ] **Step 5: Target-state checks (confirm the plan's assumptions still hold)**

```bash
# ROADMAP: list item + progress row exist; coverage still 30/30; no details block yet
grep -nF "Phase 20.5: Sampling Coordinate Allocation" .planning/ROADMAP.md
grep -nF "30/30 v1.4 requirements" .planning/ROADMAP.md
grep -cF "### Phase 20.5: Sampling Coordinate Allocation" .planning/ROADMAP.md   # expect 0

# REQUIREMENTS: ARCH-05 row is Complete; coverage still 30 total; no SAMP/SCOPE-05 yet
grep -nF "| ARCH-05 | Phase 20 | Complete |" .planning/REQUIREMENTS.md
grep -nF "30 total" .planning/REQUIREMENTS.md
grep -cE "SAMP-01|SCOPE-05" .planning/REQUIREMENTS.md                            # expect 0

# Gap index: already at 21 and already carries the Phase 20.5 section
grep -nE "total_gaps: 21|resolved_gaps: 21" .planning/milestones/v1.4-GAPS.md
grep -cF "## Phase 20.5: Sampling Coordinate Allocation" .planning/milestones/v1.4-GAPS.md  # expect 1

# Gap register already exists and is resolved
grep -cF "RESOLVED-WITH-INSTRUCTION" .planning/phases/20-5-sampling-coordinate-allocation/20-5-GAPS.md  # expect >= 3
```
If a check disagrees with the expected value, the live state has drifted since 2026-06-06 —
re-derive the affected task before running it.

- [ ] **Step 6: GSD phase-number tooling hazard (acknowledge)**

`find-phase 20` and `init.phase-op 20` can resolve to the Phase 20.5 directory (recorded in
`.planning/milestones/v1.4-GAPS.md`). For the rest of this plan, use **explicit file paths
only**; do not invoke phase-number tooling to locate Phase 20 or Phase 20.5 artifacts.

- [ ] **Step 7: Commit tooling and target-file cleanliness**

Verify the required commit tooling exists, then check every existing file this plan may mutate
for pre-existing diffs:
```bash
test -x scripts/agent-commit
test -f scripts/git_policy/validate_commit_msg.py

for f in \
  .planning/ROADMAP.md \
  .planning/REQUIREMENTS.md \
  AGENTS.md \
  ANTIGRAVITY.md \
  pinn_instruction/markdown_conversion/framework-specs/sampling_method.md \
  .planning/STATE.md \
  .planning/MILESTONES.md \
  .planning/PROJECT.md
do
  git diff --name-only -- "$f"
done
```
The loop should print nothing before Phase 20.5 execution starts. If any target file already
has a diff, STOP and inspect it as user-owned work before proceeding; update the affected task
instructions or get user guidance rather than silently bundling pre-existing edits into a
Phase 20.5 commit.

- [ ] **Step 8: Project Python environment for the probe**

The disposable probe in Task 6 must run in the project virtual environment, not whichever
`python` happens to be first on `PATH`:
```bash
.venv/bin/python3 -c "import sys, numpy, scipy; print(sys.executable); print('numpy', numpy.__version__); print('scipy', scipy.__version__)"
```
Expected: the command exits `0` and prints `.venv/bin/python3` plus installed `numpy` and
`scipy` versions. If `.venv/bin/python3` is missing or cannot import both packages, STOP and
create/repair a project-local environment. Do not install packages into a system Python just to
make this probe run.

---

## Post-Completion Follow-ups

FLAG-10 (re-verify the Phase 18/19 cross-references in `sampling_method.md`) is no longer a
post-completion item: Phases 18 and 19 are complete, so it has been **promoted into the
execution flow as Task 5 Step 7** and runs during this plan. No other post-completion
follow-ups remain.

---

## Self-Review

Run after all tasks are written — checklist, not a subagent dispatch.

**0. State-awareness (re-grounded 2026-06-06)** — this plan was made state-aware after
Phases 17–20 executed. Task 0 verifies live state before any mutation; Tasks 1 and 4 are
verification-aware (the ROADMAP list item/progress row and both gap registers already exist);
Task 5 Edit 5 and Task 8 are re-grounded to the Phase 18 momentum wording; FLAG-10 is promoted
into the flow as Task 5 Step 7.

**1. Spec coverage** — every section of the design doc maps to a task:
- Design §4 Edits 1–5 → Task 5 (Edit 5 FROM/TO re-grounded to the Phase 18 wording). ✓
- Design §5.2 SAMP-01/02 + §5.3 SCOPE-02/SCOPE-05 → Task 1 (also bumps both REQUIREMENTS and ROADMAP coverage 30→32). ✓
- Design §5.1 ROADMAP → Task 2 (verify existing list item/progress row; insert details block after SAMP-01/02/SCOPE-05 exist; declares dependencies on Phase 18 FRAME and Phase 19 preprocessing-scaling contracts; the false "no content dependency on Phases 17–20" statement is removed). ✓
- Design §5.3 SCOPE-05 propagation → Task 3 (symlink-aware; manual fallback; path-scoped `AGENTS.md`/`ANTIGRAVITY.md`/symlink-topology checks). ✓
- Design §5.4 v1.4-GAPS + §5.5 GAP Records → Task 4 (verification-only; registers already exist; count stays 21). ✓
- Design §5.6 DATA-ALIGNMENT + §6 AC-SAMP-01 → Task 7 (stable anchors, no line numbers; expanded AC-SAMP-01 mirrors the three-surface probe; scoped provenance claim — alignment of spec, documented generator configuration, and current sampler behavior; no in-repo manifest proves the exact script revision for every stored file; no regeneration required; not a blanket historical-provenance certification). ✓
- Design §6 verification probe → Task 6 (three-surface probe: static spec, entrypoint AST parse of `generate_ics.py`, sampler behavior including a synthetic position test; each surface exits nonzero on missing source anchor, malformed configuration, or allocation mismatch). ✓
- Design §8 sub-conflict #1 → Task 8 (verification-only; Phase 18 already reconciled it; no finding created). ✓
- Phase 20.5 closure/status synchronization → Task 9 (reruns expanded AC-SAMP-01 probe; verifies handoff contains both scoped no-regeneration conclusion and historical-provenance caveat). ✓
- Live-state preflight → Task 0; FLAG-10 cross-reference check → Task 5 Step 7.

**1b. Chained part-completion gates** — each part file ends with a completion gate that the
next part's precondition requires:
- Part 1 completion gate → verifies Tasks 1–4, their expected commits (Tasks 1, 2, 3 only;
  Task 4 is verification-only), required artifacts, and empty staged index. Required by Part
  2 precondition before Task 5 starts.
- Part 2 completion gate → verifies spec edit, full probe, data-alignment handoff, Task 8
  verification, expected commits (Tasks 5, 6, 7), and empty staged index. Required by Part
  3 precondition before Task 9 starts.
- Part 3 completion gate → verifies Task 9 reran the expanded AC-SAMP-01 probe, the
  handoff contains both the scoped no-regeneration conclusion and the historical-provenance
  caveat, expected commit (Task 9), and empty staged index. Routes back to this index's
  Post-Completion and Self-Review.

**2. Placeholder scan** — no "TBD/TODO/implement later". Every applied edit shows verbatim
FROM/TO text; the data-alignment doc and probe show full content; the verification-only tasks
(0, 4, 8) state explicit checks, not placeholders. Task 3 delegates to `gsd-docs-update` with
exact rule text plus a manual fallback and explicit-path staging — not a placeholder.

**3. Type/identifier consistency** — `δ_s`, `δ_v`, `d = 3 + δ_s + 3δ_v` are identical across
Edits 2–5, the data-alignment doc, and the probe. `AC-SAMP-01`, `SAMP-01`, `SAMP-02`,
`SCOPE-05`, `GAP-20-5-01/02/03` are spelled consistently throughout. All commits use
`scripts/agent-commit` with `GIT_AGENT_ID` and validator-valid scopes (`docs(planning)`,
`docs(governance)`, `spec(spec)`, `test(planning)`); `20-5` is never used as a scope.

**4. GSD document set** — companion documents in this phase directory:
- `20-5-RESEARCH.md` — extracted research findings (mathematical grounding, code analysis, decision rationale)
- `20-5-GAPS.md` — pre-existing gap register (GAP-20-5-01/02/03 at RESOLVED-WITH-INSTRUCTION); verified by Task 4, not recreated

Cross-document inconsistencies from the adversarial review (P1-#1 SCOPE-D→SCOPE-05, P1-#2
success criteria count 4, P1-#3 AC-SAMP-01 finalized) are resolved by adopting the plan's
corrected terminology as authoritative.

**Verification note:** Task 5 FROM blocks were re-verified against the live
`sampling_method.md` on 2026-06-06 by section anchor (not line number): Edits 1–4 FROM text
still matches, and Edit 5's FROM/TO were re-grounded to the Phase 18 (FRAME-03) momentum
wording (`v1 = -v2/2`, `v3 = -v2/2`). The probe's
`EnhancedThreeBodySampler(scale_range=..., velocity_scale=..., seed=...)` signature matches
`ic_generation_utils.py`.
