# Phase 20.5 GSD Workflow Repair Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repair Phase 20.5 so the official GSD workflow recognizes it as Phase `20.5`, with complete pre-execution artifacts and canonical split plans, without executing Phase 20.5.

**Architecture:** This is a workflow repair pass, not the phase implementation. It preserves the existing `20-5` research/gaps/plan content as source material, moves Phase 20.5 to dot-decimal GSD identity, registers pending SAMP/SCOPE requirements, creates missing GSD artifacts, and rewrites the monolithic plan into canonical executable GSD plans. It must not edit `sampling_method.md`, create probes, run `$gsd-execute-phase`, or mark Phase 20.5 complete.

**Tech Stack:** Markdown GSD artifacts, `gsd-sdk` queries, shell validation, git commits with explicit path staging.

---

## Save Target

Save this plan as:

`<home>/Desktop/3_body_problem/docs/plans/2026-05-22-phase-20-5-gsd-workflow-repair-plan.md`

This current thread is still in Plan Mode, so no file mutation has been performed yet.

## Non-Execution Guard

Phase 20.5 execution remains blocked after this plan.

Allowed in this repair:
- Register Phase 20.5 in GSD root planning docs.
- Rename/copy planning artifacts into the correct dot-decimal phase directory.
- Create missing pre-execution artifacts: `SPEC`, `CONTEXT`, `DISCUSSION-LOG`, `PATTERNS`, `VALIDATION`.
- Create canonical split `20.5-XX-PLAN.md` files for later execution.

Forbidden in this repair:
- Do not run `gsd-sdk query init.execute-phase 20.5` except as read-only validation.
- Do not invoke `$gsd-execute-phase 20.5`.
- Do not edit `<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`.
- Do not create `20.5-SUMMARY.md`, `20.5-VERIFICATION.md`, probes, or `20.5-DATA-ALIGNMENT.md`.
- Do not mark SAMP requirements complete.
- Do not change current milestone focus away from Phase 19 unless the user explicitly authorizes sequencing changes.

## File Structure

Create:
- `<home>/Desktop/3_body_problem/docs/plans/2026-05-22-phase-20-5-gsd-workflow-repair-plan.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/20.5-SPEC.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/20.5-CONTEXT.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/20.5-DISCUSSION-LOG.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/20.5-PATTERNS.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/20.5-VALIDATION.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/20.5-01-PLAN.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/20.5-02-PLAN.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/20.5-03-PLAN.md`

Move or copy:
- `<home>/Desktop/3_body_problem/.planning/phases/20-5-sampling-coordinate-allocation/20-5-GAPS.md` to `20.5-GAPS.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20-5-sampling-coordinate-allocation/20-5-RESEARCH.md` to `20.5-RESEARCH.md`
- Archive `<home>/Desktop/3_body_problem/.planning/phases/20-5-sampling-coordinate-allocation/` outside `.planning/phases/` after the dot-decimal directory is complete.

Modify:
- `<home>/Desktop/3_body_problem/.planning/ROADMAP.md`
- `<home>/Desktop/3_body_problem/.planning/REQUIREMENTS.md`
- `<home>/Desktop/3_body_problem/.planning/STATE.md`
- `<home>/Desktop/3_body_problem/.planning/MILESTONES.md`
- `<home>/Desktop/3_body_problem/.planning/PROJECT.md` only if needed to replace stale `20-5` paths with `20.5` paths.

Do not modify:
- `<home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/20.5-SUMMARY.md`
- `<home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/20.5-VERIFICATION.md`

---

### Task 1: Preflight And Safety Checks

**Files:**
- Read only.

- [ ] **Step 1: Surface git state**

Run:

```bash
git status --short --branch
```

Expected:
- Branch is `milestone/v1.4`.
- Existing `.planning/phases/20-5-sampling-coordinate-allocation/` is untracked or locally modified.
- No destructive command is needed.

If the branch is not `milestone/v1.4`, stop and ask the user whether to continue.

- [ ] **Step 2: Confirm current parser failure**

Run:

```bash
gsd-sdk query init.plan-phase 20.5
gsd-sdk query init.plan-phase 20
gsd-sdk query phase-plan-index 20.5
```

Expected before repair:
- `init.plan-phase 20.5` returns `"phase_found": false`.
- `init.plan-phase 20` incorrectly resolves `.planning/phases/20-5-sampling-coordinate-allocation`.
- `phase-plan-index 20.5` returns `"Phase not found"`.

- [ ] **Step 3: Confirm forbidden files remain untouched**

Run:

```bash
git diff -- <home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/framework-specs/sampling_method.md
```

Expected: no diff for `sampling_method.md`.

---

### Task 2: Save This Plan File

**Files:**
- Create: `<home>/Desktop/3_body_problem/docs/plans/2026-05-22-phase-20-5-gsd-workflow-repair-plan.md`

- [ ] **Step 1: Create the plan file**

Write this full plan content to:

```bash
<home>/Desktop/3_body_problem/docs/plans/2026-05-22-phase-20-5-gsd-workflow-repair-plan.md
```

- [ ] **Step 2: Verify the plan file exists**

Run:

```bash
test -f <home>/Desktop/3_body_problem/docs/plans/2026-05-22-phase-20-5-gsd-workflow-repair-plan.md
rg -n "Non-Execution Guard|Do not edit .*sampling_method.md|Task 6: Validate GSD Recognition" <home>/Desktop/3_body_problem/docs/plans/2026-05-22-phase-20-5-gsd-workflow-repair-plan.md
```

Expected: command exits `0` and prints all three matches.

---

### Task 3: Repair Phase Directory Identity

**Files:**
- Create: `<home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/`
- Move/copy from: `<home>/Desktop/3_body_problem/.planning/phases/20-5-sampling-coordinate-allocation/`
- Archive to: `<home>/Desktop/3_body_problem/.planning/archives/20-5-sampling-coordinate-allocation-pre-repair/`

- [ ] **Step 1: Create canonical and archive directories**

Run:

```bash
mkdir -p <home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation
mkdir -p <home>/Desktop/3_body_problem/.planning/archives
```

- [ ] **Step 2: Copy existing artifacts into dot-decimal names**

Run:

```bash
cp <home>/Desktop/3_body_problem/.planning/phases/20-5-sampling-coordinate-allocation/20-5-GAPS.md <home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/20.5-GAPS.md
cp <home>/Desktop/3_body_problem/.planning/phases/20-5-sampling-coordinate-allocation/20-5-RESEARCH.md <home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/20.5-RESEARCH.md
cp <home>/Desktop/3_body_problem/.planning/phases/20-5-sampling-coordinate-allocation/20-5-PLAN.md <home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/20.5-MONOLITHIC-SOURCE-PLAN.md
```

- [ ] **Step 3: Normalize copied frontmatter and references**

Edit the copied files only:
- In `20.5-GAPS.md`, change `phase: "20.5"` if already correct; change any executable path references from `20-5-*` to `20.5-*`.
- In `20.5-RESEARCH.md`, change artifact paths from `.planning/phases/20-5-sampling-coordinate-allocation/` to `.planning/phases/20.5-sampling-coordinate-allocation/`.
- In `20.5-MONOLITHIC-SOURCE-PLAN.md`, add this first line after the title:

```markdown
> **SOURCE ONLY:** This monolithic plan is retained as source material for canonical `20.5-XX-PLAN.md` files. Do not execute this file.
```

- [ ] **Step 4: Archive the old misparsed directory**

Run:

```bash
mv <home>/Desktop/3_body_problem/.planning/phases/20-5-sampling-coordinate-allocation <home>/Desktop/3_body_problem/.planning/archives/20-5-sampling-coordinate-allocation-pre-repair
```

Expected: no directory named `<home>/Desktop/3_body_problem/.planning/phases/20-5-sampling-coordinate-allocation` remains.

---

### Task 4: Register Phase 20.5 Without Executing It

**Files:**
- Modify: `<home>/Desktop/3_body_problem/.planning/ROADMAP.md`
- Modify: `<home>/Desktop/3_body_problem/.planning/REQUIREMENTS.md`
- Modify: `<home>/Desktop/3_body_problem/.planning/STATE.md`
- Modify: `<home>/Desktop/3_body_problem/.planning/MILESTONES.md`
- Modify: `<home>/Desktop/3_body_problem/.planning/PROJECT.md` only for stale path cleanup.

- [ ] **Step 1: Add Phase 20.5 to ROADMAP**

Add Phase 20.5 as a pending phase between Phase 20 and Phase 21. Use this exact intent:

```markdown
**Phase 20.5: Sampling Coordinate Allocation** — Repair and later execute the Sobol coordinate allocation contract. Status: planning workflow repaired; execution pending. This phase remains sequenced after Phase 20 and before Phase 21 unless the user explicitly authorizes earlier execution.
```

Do not mark it complete.

- [ ] **Step 2: Add SAMP requirements and SCOPE-05**

In `REQUIREMENTS.md`, add pending requirements:

```markdown
### Sampling Coordinate Allocation

- [ ] **SAMP-01**: `sampling_method.md` documents an explicit Sobol coordinate allocation convention with no coordinate reused for two independent physical quantities. Allocation order: position -> optional scale -> optional velocity. Dimension formula `d = 3 + delta_s + 3 delta_v`, where `delta_s = 1` iff sampling-time scaling is enabled and `delta_v = 1` iff velocity sampling is enabled.
- [ ] **SAMP-02**: The section 1.1 dimension claim, the "Sampling-Time Size Variability" prose, and the "Velocity Sampling" prose/formula in `sampling_method.md` are mutually consistent and agree with the locked allocation, matching `simulation_data/Scripts/ic_generation/ic_generation_utils.py`.
```

Add SCOPE-05:

```markdown
| **SCOPE-05** Data-spec alignment for sampling-method edits | When v1.4 framework-spec edits describe the data-generation pipeline, they MUST match the actual behavior of `simulation_data/Scripts/ic_generation/`. The no-live-code directive targets `pinn/` only; `simulation_data/Scripts/ic_generation/` is a permitted grounding source for data-generation specs because the existing dataset is fixed and the framework must remain compatible with it. Spec divergences from data must be reconciled to match data, flagged in `docs/findings/`, or explicitly authorized by the user as a data-regeneration directive for FUT-01. |
```

- [ ] **Step 3: Keep Phase 19 as current**

In `STATE.md`, keep Phase 19 as the current or next focus. Add only this Phase 20.5 status note:

```markdown
- Phase 20.5 workflow repair pending/underway: canonical GSD identity is `.planning/phases/20.5-sampling-coordinate-allocation/`; execution remains pending and must not begin before explicit user authorization or the normal post-Phase-20 sequence.
```

- [ ] **Step 4: Replace stale `20-5` paths in planning docs**

Run:

```bash
rg -n "20-5-sampling-coordinate-allocation|20-5-PLAN|20-5-RESEARCH|20-5-GAPS" <home>/Desktop/3_body_problem/.planning
```

Replace stale executable-path references with:
- `.planning/phases/20.5-sampling-coordinate-allocation/20.5-RESEARCH.md`
- `.planning/phases/20.5-sampling-coordinate-allocation/20.5-GAPS.md`
- `.planning/phases/20.5-sampling-coordinate-allocation/20.5-01-PLAN.md`

Historical references may remain only if explicitly labeled as archived or source-only.

---

### Task 5: Create Missing GSD Pre-Execution Artifacts

**Files:**
- Create: `20.5-SPEC.md`
- Create: `20.5-CONTEXT.md`
- Create: `20.5-DISCUSSION-LOG.md`
- Create: `20.5-PATTERNS.md`
- Create: `20.5-VALIDATION.md`

- [ ] **Step 1: Write `20.5-SPEC.md`**

Create `<home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/20.5-SPEC.md` with:
- Phase goal: lock Sobol coordinate allocation only.
- Explicit non-goals: do not solve velocity-momentum discrepancy, do not update `pinn/`, do not execute acceptance probes during workflow repair.
- Acceptance criteria: GSD recognizes Phase 20.5; SAMP-01/SAMP-02 pending; canonical plans exist; execution remains blocked.
- Ambiguity score statement: current workflow ambiguity is high until directory identity and artifacts are repaired; content design ambiguity is already reduced by prior design/review docs.

- [ ] **Step 2: Write `20.5-DISCUSSION-LOG.md`**

Create an audit-only discussion log with this opening notice:

```markdown
> **Audit trail only.** Do not use this file as the primary planning source. Decisions are captured in `20.5-CONTEXT.md`.

This log reconstructs the Phase 20.5 workflow-repair discussion from prior artifacts and user instructions. It does not claim that `$gsd-discuss-phase 20.5` was already run.
```

Record these discussion points:
- User noticed Phase 20.5 was being worked before Phase 19.
- User allowed considering Phase 20.5 independently, but asked not to execute unless justified.
- Repair decision: do not execute now.
- Repair decision: use dot-decimal `20.5`, not hyphen `20-5`.

- [ ] **Step 3: Write `20.5-CONTEXT.md`**

Create decisions:
- `D-01`: Phase 20.5 execution is blocked until GSD recognition and canonical plans pass validation.
- `D-02`: Canonical directory is `.planning/phases/20.5-sampling-coordinate-allocation/`; `20-5` is archived source material only.
- `D-03`: Root registry docs may be repaired now; `sampling_method.md` and probes remain execution work.
- `D-04`: `simulation_data/Scripts/ic_generation/` is allowed grounding for data-generation specs under SCOPE-05; `pinn/` remains disallowed as v1.4 grounding.
- `D-05`: `AC-SAMP-01` pass criteria and any FUT-01 velocity-momentum guidance must be treated as governance-sensitive and surfaced if not already grounded.
- `D-06`: After Phase 19 and Phase 20 complete, Phase 20.5 plans must be rechecked for stale cross-references before execution.

- [ ] **Step 4: Write `20.5-PATTERNS.md`**

Map artifacts to local analogs:
- `20.5-CONTEXT.md` follows `18-CONTEXT.md`.
- `20.5-DISCUSSION-LOG.md` follows `18-DISCUSSION-LOG.md`.
- `20.5-XX-PLAN.md` follows `18-01-PLAN.md`.
- `20.5-PATTERNS.md` follows `17-PATTERNS.md`.
- `20.5-VALIDATION.md` follows `17-VALIDATION.md` and `18-VALIDATION.md`.

- [ ] **Step 5: Write `20.5-VALIDATION.md`**

Create validation gates:
- SDK gate: `init.plan-phase 20.5` is true.
- Misparse gate: `init.plan-phase 20` does not resolve Phase 20.5.
- Plan-index gate: `phase-plan-index 20.5` returns canonical plan IDs.
- Non-execution gate: no diff to `sampling_method.md`; no probes; no `SUMMARY` or `VERIFICATION`.

---

### Task 6: Create Canonical Split GSD Plans

**Files:**
- Create: `20.5-01-PLAN.md`
- Create: `20.5-02-PLAN.md`
- Create: `20.5-03-PLAN.md`

- [ ] **Step 1: Create `20.5-01-PLAN.md` for governance and registry completion**

Purpose: later execution plan for root registry and governance propagation, only if not already completed by repair.

Required frontmatter:
```yaml
---
phase: 20.5-sampling-coordinate-allocation
plan: 01
type: execute
origin: ".planning/phases/20.5-sampling-coordinate-allocation/20.5-CONTEXT.md"
wave: 1
depends_on: []
files_modified:
  - ".planning/ROADMAP.md"
  - ".planning/REQUIREMENTS.md"
  - ".planning/STATE.md"
  - ".planning/milestones/v1.4-GAPS.md"
autonomous: false
requirements:
  - SAMP-01
  - SAMP-02
  - VER-05
---
```

Include an explicit task: if registry work was completed by workflow repair, verify and no-op; do not duplicate entries.

- [ ] **Step 2: Create `20.5-02-PLAN.md` for `sampling_method.md` edits**

Purpose: later execution plan for the actual Sobol coordinate allocation spec edit.

Required frontmatter:
```yaml
---
phase: 20.5-sampling-coordinate-allocation
plan: 02
type: execute
origin: ".planning/phases/20.5-sampling-coordinate-allocation/20.5-CONTEXT.md"
wave: 2
depends_on:
  - "20.5-01"
files_modified:
  - "pinn_instruction/markdown_conversion/framework-specs/sampling_method.md"
requirements:
  - SAMP-01
  - SAMP-02
  - VER-05
autonomous: false
---
```

Include read-first references to:
- `20.5-CONTEXT.md`
- `20.5-GAPS.md`
- `20.5-RESEARCH.md`
- `simulation_data/Scripts/ic_generation/ic_generation_utils.py`
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`

Add a hard precondition: this plan must not run during workflow repair.

- [ ] **Step 3: Create `20.5-03-PLAN.md` for handoff, findings, and verification artifacts**

Purpose: later execution plan for `20.5-DATA-ALIGNMENT.md`, disposable probe, gap index updates, and findings after the spec edit.

Required frontmatter:
```yaml
---
phase: 20.5-sampling-coordinate-allocation
plan: 03
type: execute
origin: ".planning/phases/20.5-sampling-coordinate-allocation/20.5-CONTEXT.md"
wave: 3
depends_on:
  - "20.5-02"
files_modified:
  - ".planning/phases/20.5-sampling-coordinate-allocation/20.5-DATA-ALIGNMENT.md"
  - ".planning/phases/20.5-sampling-coordinate-allocation/probes/verify_sobol_allocation.py"
  - "docs/findings/velocity_momentum_sampling_discrepancy.md"
  - ".planning/milestones/v1.4-GAPS.md"
requirements:
  - SAMP-01
  - SAMP-02
  - VER-05
autonomous: false
---
```

Add a hard precondition: do not create `20.5-SUMMARY.md` or `20.5-VERIFICATION.md`; those are post-execution artifacts only.

---

### Task 7: Validate GSD Recognition

**Files:**
- Read only after edits.

- [ ] **Step 1: Confirm Phase 20.5 is recognized**

Run:

```bash
gsd-sdk query init.plan-phase 20.5
```

Expected:
- `"phase_found": true`
- `"phase_dir": ".planning/phases/20.5-sampling-coordinate-allocation"`
- `"has_context": true`
- `"has_research": true`
- `"has_plans": true`

- [ ] **Step 2: Confirm Phase 20 is no longer misrouted**

Run:

```bash
gsd-sdk query init.plan-phase 20
```

Expected:
- It resolves the real Phase 20 directory, or reports Phase 20 according to ROADMAP.
- It does not resolve `.planning/phases/20.5-sampling-coordinate-allocation`.
- It does not resolve any `20-5` directory.

- [ ] **Step 3: Confirm plan index is populated**

Run:

```bash
gsd-sdk query phase-plan-index 20.5
```

Expected:
- Plans include `20.5-01`, `20.5-02`, and `20.5-03`.
- Each plan has a non-null objective.
- `files_modified` is populated for every plan.

- [ ] **Step 4: Confirm no Phase 20.5 execution happened**

Run:

```bash
test ! -f <home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/20.5-SUMMARY.md
test ! -f <home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/20.5-VERIFICATION.md
git diff -- <home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/framework-specs/sampling_method.md
```

Expected:
- Both `test ! -f` commands exit `0`.
- `sampling_method.md` diff is empty.

---

### Task 8: Commit Workflow Repair

**Files:**
- Stage explicit paths only.

- [ ] **Step 1: Check diff**

Run:

```bash
git diff --check
git status --short
```

Expected:
- `git diff --check` exits `0`.
- Status shows only workflow repair docs and archived source artifacts.

- [ ] **Step 2: Stage explicit files**

Run:

```bash
git add <home>/Desktop/3_body_problem/docs/plans/2026-05-22-phase-20-5-gsd-workflow-repair-plan.md
git add <home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation
git add <home>/Desktop/3_body_problem/.planning/archives/20-5-sampling-coordinate-allocation-pre-repair
git add <home>/Desktop/3_body_problem/.planning/ROADMAP.md
git add <home>/Desktop/3_body_problem/.planning/REQUIREMENTS.md
git add <home>/Desktop/3_body_problem/.planning/STATE.md
git add <home>/Desktop/3_body_problem/.planning/MILESTONES.md
git add <home>/Desktop/3_body_problem/.planning/PROJECT.md
```

- [ ] **Step 3: Commit**

Run:

```bash
git commit -m "docs(20.5): repair GSD workflow identity and planning artifacts"
```

---

## Test Plan

Run these commands after the commit:

```bash
gsd-sdk query init.plan-phase 20.5
gsd-sdk query init.plan-phase 20
gsd-sdk query phase-plan-index 20.5
test ! -f <home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/20.5-SUMMARY.md
test ! -f <home>/Desktop/3_body_problem/.planning/phases/20.5-sampling-coordinate-allocation/20.5-VERIFICATION.md
git diff -- <home>/Desktop/3_body_problem/pinn_instruction/markdown_conversion/framework-specs/sampling_method.md
git diff --check HEAD~1..HEAD
```

Acceptance:
- Phase `20.5` is recognized by `gsd-sdk`.
- Phase `20` no longer resolves the old Phase 20.5 directory.
- `20.5-01`, `20.5-02`, and `20.5-03` are indexable plans.
- No substantive Phase 20.5 execution artifact exists.
- `sampling_method.md` remains unchanged.
- The commit contains only workflow repair artifacts.

## Assumptions

- Public phase label remains `20.5`; do not rename it to `20.1`.
- Root registry updates are workflow repair, not Phase 20.5 execution, as long as requirements remain pending and no spec/probe work runs.
- Existing `20-5` files are untracked source material and may be archived after copying into the canonical dot-decimal directory.
- Recommended execution mode after leaving Plan Mode is `superpowers:subagent-driven-development`, with one worker for directory/root registry repair and one reviewer for SDK validation.
