# Phase 20.5 Plan Remediation Implementation Plan
Created: 2026-06-06

## Purpose

Repair the current Phase 20.5 Sobol Coordinate Allocation plan so it can be executed safely after Phases 17-20 changed the repository state. This plan is a plan-update artifact: it tells an implementer how to revise `.planning/phases/20-5-sampling-coordinate-allocation/20-5-PLAN.md` and its immediately related companion references. It does not execute Phase 20.5, edit `sampling_method.md`, run the verification probe, or create the Phase 20.5 data-alignment hand-off.

Primary target:

- `.planning/phases/20-5-sampling-coordinate-allocation/20-5-PLAN.md`

Companion targets only if the plan repair needs them:

- `.planning/phases/20-5-sampling-coordinate-allocation/20-5-GAPS.md`
- `.planning/phases/20-5-sampling-coordinate-allocation/20-5-RESEARCH.md`

Do not treat `docs/plans/Phase 20.5 GSD Workflow Repair Implementation Plan.md` as the executable Phase 20.5 plan. It is a separate workflow-repair proposal and may be used only as context for review findings that discuss SCOPE-05 propagation, gap ID preservation, and the GSD phase-numbering hazard.

Also, do not confuse this plan with `.planning/phases/20-architecture-and-normalization-cleanup/20-05-PLAN.md` (which is Phase 20, Task 05). This remediation plan strictly targets `.planning/phases/20-5-sampling-coordinate-allocation/20-5-PLAN.md`.

## Source Inputs

Use these review reports as the evidence base:

| Source | Use in this remediation |
|--------|--------------------------|
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/2026-06-06-phase20-5-plan-adversarial-staleness-audit.md` | Primary stale-state audit for ROADMAP, v1.4 gap index, Task 5 Edit 5, preflight, rollback, and explicit-path warnings. |
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/2026-06-06-phase20.5-plan-execution-readiness-audit.md` | Primary execution-readiness audit for FROM-text mismatches, redundant tasks, Task 8 obsolescence, SCOPE-05 fallback, probe fragility, and execution-path recommendation. |
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/phase20.5-plan-pre-execution-audit-2026-06-06.md` | Governance and operations audit for raw commit commands, hook setup, worktree safety, symlink topology, requirements staleness, and companion-doc references. |
| `docs/findings/milestone_v1.4/reviewing_phase20.5_plan/phase_20.5_plan_critique_review.md` | Earlier critique review. Use only findings that still match the live repository; several sections refer to the separate workflow-repair plan rather than the current `20-5-PLAN.md`. |

When reports conflict, verify against the live repository before editing the plan. Known conflict already verified: commit `a9ecd51` exists and records Phase 20.5 status in planning docs; commit `b727b15` is the design/plan lock lineage. Do not blindly replace every `a9ecd51` reference with `b727b15`; update only references whose stated role is wrong.

## Current-State Snapshot

The remediation instructions should be based on these live-state facts:

- The authoritative Phase 20.5 directory is currently `.planning/phases/20-5-sampling-coordinate-allocation/`; no `.planning/phases/20.5-sampling-coordinate-allocation/` directory exists.
- `.planning/ROADMAP.md` already contains the Phase 20.5 top-level list item and progress-table row, but still shows `30/30 v1.4 requirements mapped` and lacks a `### Phase 20.5: Sampling Coordinate Allocation` details block.
- `.planning/REQUIREMENTS.md` still has `30 total`, has `| ARCH-05 | Phase 20 | Complete |`, and lacks SAMP-01, SAMP-02, and SCOPE-05.
- `.planning/milestones/v1.4-GAPS.md` already has `total_gaps: 21`, `resolved_gaps: 21`, and a Phase 20.5 section for GAP-20-5-01/02/03.
- `.planning/phases/20-5-sampling-coordinate-allocation/20-5-GAPS.md` already exists and records all three gaps as `RESOLVED-WITH-INSTRUCTION`.
- `CLAUDE.md` and `GEMINI.md` are symlinks to `AGENTS.md`; `ANTIGRAVITY.md` is a separate file.
- `AGENTS.md` and `ANTIGRAVITY.md` do not yet carry the SCOPE-05 data-generation carveout.
- `core.hooksPath` is `.githooks`, and both `scripts/agent-commit` and `scripts/setup-git-hooks.sh` exist.

## Non-Execution Guard

Start the revised `20-5-PLAN.md` with a guard stating that the plan is not executable until its own preflight passes. The guard must say:

- Use explicit file paths for all Phase 20.5 work. Do not rely on `find-phase 20`, `init.phase-op 20`, or other GSD phase-number tooling while the known Phase 20 / Phase 20.5 resolution hazard remains.
- Run the revised Task 0 before mutating any file.
- If any semantic or process-artifact decision is not already grounded by the existing gap register, milestone index, review reports, or user instruction, follow the STOP protocol instead of inventing a default.
- Do not rename `GAP-20-5-0X` IDs during this remediation. They are historical resolved gap IDs. Directory/path migration to dot-decimal `20.5-*` is out of scope for this plan update unless the user separately authorizes workflow repair.

## Implementation Sequence

### Task 0. Add plan-level preflight

Add a new Task 0 before current Task 1 in `20-5-PLAN.md`.

Task 0 must verify:

- `git status --short --branch`, with unrelated changes surfaced and excluded from Phase 20.5 staging.
- `git config --get core.hooksPath`; if the value is not `.githooks`, run `scripts/setup-git-hooks.sh` before any commit.
- `git cat-file -t a9ecd51` and `git cat-file -t b727b15`. Treat `a9ecd51` as the status-record commit and `b727b15` as the design/plan-lock commit.
- `ls -l AGENTS.md CLAUDE.md GEMINI.md ANTIGRAVITY.md` to confirm symlink topology before any SCOPE-05 propagation.
- The current target-state checks listed in "Current-State Snapshot". If any check has changed, update the relevant task instructions before proceeding.
- Every future plan task stages only its intended files with explicit paths.

Task 0 must also add the GSD tooling warning from `.planning/milestones/v1.4-GAPS.md`: `find-phase 20` and `init.phase-op 20` can resolve to the Phase 20.5 directory, so executors must use explicit paths.

### Task 1. Repair ROADMAP update instructions

Revise current Task 1 so it is state-aware:

- Convert the existing Phase 20.5 list-item insertion step into a verification-only step. The list item already exists in `.planning/ROADMAP.md`; do not duplicate it.
- Keep the coverage update, but make it update `30/30` to `32/32` only if `.planning/REQUIREMENTS.md` has also been updated to add SAMP-01 and SAMP-02.
- Keep the Phase 20.5 details-block insertion, because the details block is still absent. Insert it between the Phase 20 and Phase 21 details sections.
- Convert the Phase 20.5 progress-table row insertion into a verification-only step. The row already exists.
- Replace count-only verification with exact-row checks where feasible. For example, verify that ROADMAP has exactly one Phase 20.5 top-level list item, exactly one Phase 20.5 progress row, and exactly one Phase 20.5 details heading after the repair.

The revised task must not assume Phase 20 is unchecked or incomplete; Phase 20 is complete as of 2026-06-05.

### Task 2. Repair REQUIREMENTS update instructions

Revise current Task 2 so its FROM text matches the live requirements file and its verification is less fragile:

- Use `| ARCH-05 | Phase 20 | Complete |` as the traceability insertion anchor, not `Pending`.
- Keep adding SAMP-01 and SAMP-02. These remain missing and are still required.
- Keep amending SCOPE-02 so Phase 20.5 SAMP-01/SAMP-02 edits to `sampling_method.md` are explicitly in scope.
- Keep adding SCOPE-05 as the data-generation grounding carveout for `simulation_data/Scripts/ic_generation/`.
- Add SAMP-01 and SAMP-02 traceability rows after the ARCH-05 row.
- Update the coverage block from `30 total` to `32 total`, `Mapped to phases: 30` to `Mapped to phases: 32`, and the scope-annotation line from SCOPE-01/02/03/04 to SCOPE-01 through SCOPE-05.

Verification must check exact intended artifacts rather than broad counts:

- The SAMP-01 definition exists once.
- The SAMP-02 definition exists once.
- The SCOPE-02 row contains both FRAME-03 and SAMP-01/SAMP-02.
- The SCOPE-05 row exists once and mentions `simulation_data/Scripts/ic_generation/`.
- The traceability table contains `| SAMP-01 | Phase 20.5 | Pending |` and `| SAMP-02 | Phase 20.5 | Pending |`.
- The coverage block says `32 total` and `Mapped to phases: 32`.

### Task 3. Harden SCOPE-05 propagation

Keep SCOPE-05 propagation in the Phase 20.5 plan, but do not rely only on `gsd-docs-update`.

Revise Task 3 to:

- Run after Task 2, because the canonical SCOPE-05 row must exist in `.planning/REQUIREMENTS.md` before root instructions cite it.
- Verify `CLAUDE.md` and `GEMINI.md` are symlinks to `AGENTS.md`.
- Treat `AGENTS.md` and `ANTIGRAVITY.md` as the real edit targets. Explicitly instruct the executor to use tools or commands that do not blindly follow symlinks, avoiding duplicate edits across the linked files.
- Permit `gsd-docs-update` only if its output is reviewed before staging.
- Add a manual fallback clause: if the skill fails, is unavailable, or edits unexpected files, manually add a narrow SCOPE-05 note to `AGENTS.md` and `ANTIGRAVITY.md`.

The fallback note should communicate only this grounded rule:

- `simulation_data/Scripts/ic_generation/` is a permitted grounding source for data-generation specs in `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`.
- This is a narrow carveout from the `pinn/` no-live-code directive, not a general live-code exception.
- The canonical rule lives in `.planning/REQUIREMENTS.md` SCOPE-05.

Do not stage `CLAUDE.md` or `GEMINI.md` separately if they are still symlinks to `AGENTS.md`.

### Task 4. Convert gap-register work to verification-only

Revise current Task 4 because both the phase-local register and milestone-wide index already exist.

The revised task should:

- Verify `.planning/phases/20-5-sampling-coordinate-allocation/20-5-GAPS.md` exists and contains GAP-20-5-01, GAP-20-5-02, and GAP-20-5-03.
- Verify all three Phase 20.5 gaps are `RESOLVED-WITH-INSTRUCTION`.
- Verify `.planning/milestones/v1.4-GAPS.md` already contains exactly one `## Phase 20.5: Sampling Coordinate Allocation` section.
- Verify `total_gaps` and `resolved_gaps` remain internally consistent with the current milestone index. Provide the exact hardcoded frontmatter replacements to avoid fragile bash-based YAML parsing. Since the baseline count is 21, the executor should use FROM: `total_gaps: 21` / `resolved_gaps: 21` and TO: `total_gaps: 24` / `resolved_gaps: 24` (and update `last_updated`).
- Preserve the GAP-20-5 IDs. Do not rename them to dot-decimal IDs.

If the verification fails, the revised plan must require STOP-protocol handling for any process-artifact schema decision before inventing a new gap-index structure.

### Task 5. Repair and guard the sampling_method.md edit task

Revise current Task 5 so a future executor cannot partially apply stale spec edits.

Required changes:

- Add a Task 5 Step 0 preflight that verifies every FROM block against `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md` before any edit is made.
- Require section-anchor lookup instead of line-number lookup.
- Keep Edits 1-4 if their FROM text still matches live `sampling_method.md`.
- Replace Edit 5's FROM and TO texts with exact, explicit Markdown blocks to prevent the executor from hallucinating physics terminology.
- **FROM block must include:** The current 3-line momentum sentence added by Phase 18: `The sampler then enforces total momentum conservation for the equal-mass case by setting v1 = -v2/2 and v3 = -v2/2, so...`
- **TO block must include:** The exact Sobol coordinate logic (`u_{4+\delta_s}, u_{5+\delta_s}, u_{6+\delta_s}`) and preserve the Phase 18 wording above. Do NOT ask the downstream agent to synthesize this physics text.
- Remove any instruction claiming the old momentum-conservation sentence is preserved verbatim if that sentence has already changed.
- Add a rollback rule: if any edit fails after the file has been mutated, stop immediately, inspect `git diff -- pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`, and remove only the partial Phase 20.5 edits via a targeted patch. Do not continue with later edits, and do not use broad reset/restore commands that could discard unrelated user changes.
- Promote FLAG-10 cross-reference verification into the execution flow immediately after Task 5, because Phases 18 and 19 are now complete.

Task 5 verification should include a post-edit check that the dimension formula, sampling-time scaling prose, and velocity-coordinate prose all agree on `d = 3 + delta_s + 3 delta_v` and the Option A allocation.

### Task 6. Harden the verification probe task

Revise current Task 6 so the probe is operationally robust but still disposable:

- Require the executor to run from the repo root, or to compute repo root before invoking the probe.
- Add a dependency check for Python plus `numpy` and `scipy` before running the probe. If dependencies are missing, explicitly instruct the executor to run `pip install numpy scipy` or source the correct virtual environment, rather than silently halting execution.
- Add a comment that `_process_sobol_batch` is a private method used only for disposable verification.
- Add a runtime assertion that the private method returns seven values before unpacking.
- Keep the synthetic Sobol-batch design that uses distinct column constants to prove allocation order.
- Keep the probe disposable and under `.planning/phases/20-5-sampling-coordinate-allocation/probes/`.

If the dependency check fails, the plan should surface the environment setup steps rather than just immediately blocking or changing the acceptance standard.

### Task 7. Repair the data-alignment hand-off instructions

Revise current Task 7 so the generated hand-off is stable across line-number drift:

- Do not cite live `sampling_method.md` line numbers in `20-5-DATA-ALIGNMENT.md`; cite section headings and stable text anchors instead.
- Keep the AC-SAMP-01 stub because it is grounded by GAP-20-5-02.
- Keep the provenance caveat for `simulation_data/Scripts/ic_generation/` as the data-generation source.
- Include a verification step that checks the generated hand-off references `AC-SAMP-01`, the Option A allocation, and the FUT-01 hand-off without depending on exact line numbers.

If a future executor wants to mention the velocity-momentum wording, the revised plan must require live verification first. It must not create a new open discrepancy from a stale May 2026 premise.

### Task 8. Remove or reframe obsolete sub-conflict work

Revise current Task 8 so it no longer creates `docs/findings/velocity_momentum_sampling_discrepancy.md` as an open finding based on stale evidence.

Acceptable outcomes:

- Remove Task 8 entirely and move any still-useful traceability note into Task 7.
- Or replace Task 8 with a verification-only step that confirms no separate open velocity-momentum finding is needed.

If live verification shows a real unresolved semantic contradiction, do not write a finding immediately. Follow the STOP protocol: articulate the physics and downstream consequences, identify consulted sources and source silence, record a proper gap only if the gap criteria are met, and surface it for user instruction.

### Task 9. Repair commit and staging instructions

Replace every raw commit invocation in `20-5-PLAN.md` with `scripts/agent-commit`, and set `GIT_AGENT_ID` before committing.

Use commit subjects whose scopes pass `scripts/git_policy/validate_commit_msg.py`. Avoid `docs(20-5): ...`; `20-5` is not an allowed scope under the current validator. Prefer fixed scopes such as `planning`, `governance`, or `spec`.

Examples:

```bash
GIT_AGENT_ID="Codex GPT-5" scripts/agent-commit \
  -m "docs(planning): insert Phase 20.5 roadmap details" \
  -m "Add the Phase 20.5 details block and update v1.4 coverage after SAMP-01 and SAMP-02 are introduced."

GIT_AGENT_ID="Codex GPT-5" scripts/agent-commit \
  -m "docs(planning): add SAMP requirements and SCOPE-05" \
  -m "Add the Phase 20.5 sampling requirements, SCOPE-05 data-generation carveout, traceability rows, and updated coverage totals."

GIT_AGENT_ID="Codex GPT-5" scripts/agent-commit \
  -m "spec(spec): lock Sobol coordinate allocation" \
  -m "Apply the Phase 20.5 sampling-method edits after preflight verifies the current FROM blocks and Phase 18 wording is preserved."
```

Every task commit that touches `.planning/`, `pinn_instruction/`, root governance instructions, or multiple files must include a body. Stage only the files named by that task.

## Verification Before Declaring the Plan Repaired

After revising `20-5-PLAN.md`, run static verification against the plan text:

```bash
rg -n "git commit -m|docs\\(20-5\\)|total_gaps: 14|total_gaps: 11|ARCH-05 \\| Phase 20 \\| Pending|velocity_momentum_sampling_discrepancy.md" .planning/phases/20-5-sampling-coordinate-allocation/20-5-PLAN.md
rg -n "Task 0|scripts/agent-commit|SCOPE-05|find-phase 20|init.phase-op 20|preflight|rollback|FLAG-10|GAP-20-5-01" .planning/phases/20-5-sampling-coordinate-allocation/20-5-PLAN.md
```

Expected:

- The first command returns no stale executable instructions. If `velocity_momentum_sampling_discrepancy.md` remains, it must appear only in a note explaining that the stale open-finding task was removed or made verification-only.
- The second command returns the new safety and governance instructions.

Then run live-state spot checks:

```bash
git status --short --branch
git config --get core.hooksPath
git cat-file -t a9ecd51
git cat-file -t b727b15
ls -l AGENTS.md CLAUDE.md GEMINI.md ANTIGRAVITY.md
rg -n "Phase 20\\.5: Sampling Coordinate Allocation|30/30|32/32" .planning/ROADMAP.md
rg -n "SAMP-01|SAMP-02|SCOPE-05|ARCH-05" .planning/REQUIREMENTS.md
rg -n "Phase 20\\.5: Sampling Coordinate Allocation|GAP-20-5-0|total_gaps: 21" .planning/milestones/v1.4-GAPS.md
```

These checks are diagnostic. They should inform whether the plan instructions need more state-awareness; they should not execute Phase 20.5.

## Completion Criteria

The remediation is complete when:

- `20-5-PLAN.md` has a Task 0 preflight and explicit-path GSD warning.
- ROADMAP, REQUIREMENTS, gap-index, root-instruction, sampling-method, probe, data-alignment, Task 8, and commit instructions are all state-aware.
- The plan distinguishes `a9ecd51` and `b727b15` by role instead of treating either as universally wrong.
- The plan no longer duplicates existing ROADMAP or gap-index content.
- The plan no longer creates an open velocity-momentum finding from stale evidence.
- The plan uses `scripts/agent-commit` with valid commit scopes and required bodies.
- Any remaining semantic or process-artifact uncertainty is routed through the STOP protocol rather than resolved by assumption.
