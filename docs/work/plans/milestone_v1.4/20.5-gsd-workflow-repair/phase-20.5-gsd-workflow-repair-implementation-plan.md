---
status: consumed
purpose: other
created: unknown
milestone: v1.4
phase: 20.5-gsd-workflow-repair
retirement_trigger: milestone complete; superseded by subsequent work
---

# Phase 20.5 GSD Workflow Repair Implementation Plan

> **SUPERSEDED / NOT ACTIVE (2026-06-07).** This dot-decimal "GSD workflow repair" proposal is not the chosen path for Phase 20.5. The team elected to keep the hyphenated `.planning/phases/20-5-sampling-coordinate-allocation/` directory and reorganize `20-5-PLAN.md` in place into a thin index plus `20-5-PLAN-part1/2/3.md`. Do NOT execute this plan: do not migrate to a `20.5-` directory, do not rename or retire the monolith, and do not create `20.5-0N-PLAN.md` or the GSD artifact set. It is also stale (assumes `v1.4-GAPS` 17/17 and a 30-requirement baseline; live state is 21 and SAMP/SCOPE-05 are already registered). Retained in place as historical context / audit trail only.

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repair Phase 20.5 so the official GSD workflow recognizes it as Phase `20.5`, with complete pre-execution artifacts and canonical split plans, without executing Phase 20.5.

**Architecture:** This is a workflow repair pass, not the phase implementation. It preserves the existing `20-5` research/gaps/plan content as source material, moves Phase 20.5 to dot-decimal GSD identity, registers pending SAMP/SCOPE requirements, creates missing GSD artifacts, and rewrites the monolithic plan into canonical executable GSD plans. It must not edit `sampling_method.md`, create probes, run `$gsd-execute-phase`, or mark Phase 20.5 complete.

**Tech Stack:** Markdown GSD artifacts, `gsd-sdk` queries, shell validation, git commits with explicit path staging.

---

## Save Target

This plan lives at:

`docs/work/plans/milestone_v1.4/20.5-gsd-workflow-repair/phase-20.5-gsd-workflow-repair-implementation-plan.md`

The file already exists at this canonical path. Do **not** create a second dated/hyphenated copy (`2026-05-22-phase-20-5-gsd-workflow-repair-plan.md`) — that would (a) introduce a hyphenated `20-5` artifact into a dot-decimal migration and (b) duplicate the canonical plan.

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
- Do not edit `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`.
- Do not create `20.5-SUMMARY.md`, `20.5-VERIFICATION.md`, probes, or `20.5-DATA-ALIGNMENT.md`.
- Do not mark SAMP requirements complete.
- Do not change current milestone focus away from Phase 19 unless the user explicitly authorizes sequencing changes.

## File Structure

Create:
- `.planning/phases/20.5-sampling-coordinate-allocation/20.5-SPEC.md`
- `.planning/phases/20.5-sampling-coordinate-allocation/20.5-CONTEXT.md`
- `.planning/phases/20.5-sampling-coordinate-allocation/20.5-DISCUSSION-LOG.md`
- `.planning/phases/20.5-sampling-coordinate-allocation/20.5-PATTERNS.md`
- `.planning/phases/20.5-sampling-coordinate-allocation/20.5-VALIDATION.md`
- `.planning/phases/20.5-sampling-coordinate-allocation/20.5-01-PLAN.md`
- `.planning/phases/20.5-sampling-coordinate-allocation/20.5-02-PLAN.md`
- `.planning/phases/20.5-sampling-coordinate-allocation/20.5-03-PLAN.md`

Move (`git mv` — the source directory is **git-tracked**, not untracked; see Task 3):
- `.planning/phases/20-5-sampling-coordinate-allocation/20-5-GAPS.md` → `20.5-GAPS.md` in the new dir
- `.planning/phases/20-5-sampling-coordinate-allocation/20-5-RESEARCH.md` → `20.5-RESEARCH.md` in the new dir
- `.planning/phases/20-5-sampling-coordinate-allocation/20-5-PLAN.md` → `20.5-MONOLITHIC-SOURCE-PLAN.md` in the new dir (renamed; this is the historical source plan, NOT executed)

After the moves, the old `20-5-sampling-coordinate-allocation/` directory is empty and is removed with `rmdir`. Git's rename detection preserves history; no separate `.planning/archives/` copy is required.

Modify (these are **partially already done** by commit a9ecd51 from 2026-05-20 — verify presence, supplement where missing, never duplicate):
- `.planning/ROADMAP.md` (Phase 20.5 already inserted in `:9`; verify only)
- `.planning/REQUIREMENTS.md` (SAMP-01/02, SCOPE-05, SCOPE-02 amendment, ARCH-05 traceability rows, count bump 30 → 32 — **all still missing**)
- `.planning/STATE.md` (Phase 20.5 note already present at `:78`; verify only)
- `.planning/MILESTONES.md` (Phase 20.5 already present at `:26`, `:31`; verify only — no further edit required in this repair)
- `.planning/PROJECT.md` (Phase 20.5 row already present; only edit if stale `20-5-*` *paths* (not gap IDs) remain — see Task 4 Step 4)
- `.planning/milestones/v1.4-GAPS.md` (no Phase 20.5 section; counts 17/17 — **must be added** with the three RESOLVED-WITH-INSTRUCTION gaps, counts bumped to 20/20)
- `AGENTS.md` (SCOPE-05 cross-reference missing — **must be added** per DG-1; covers `CLAUDE.md`/`GEMINI.md` automatically since both are symlinks to `AGENTS.md`)
- `ANTIGRAVITY.md` (SCOPE-05 cross-reference missing — **must be added** per DG-1; this is a separate 15 KB file, not a symlink)

Do not modify:
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`
- `.planning/phases/20.5-sampling-coordinate-allocation/20.5-SUMMARY.md`
- `.planning/phases/20.5-sampling-coordinate-allocation/20.5-VERIFICATION.md`

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
- Existing `.planning/phases/20-5-sampling-coordinate-allocation/` is **git-tracked** (`git ls-files` returns all three files: `20-5-GAPS.md`, `20-5-PLAN.md`, `20-5-RESEARCH.md`). It may also have uncommitted local modifications. The repair therefore uses `git mv`, not `cp` + filesystem `mv`.
- No destructive command is needed.

Also confirm by running:

```bash
git ls-files .planning/phases/20-5-sampling-coordinate-allocation/
git check-ignore .planning/phases/20-5-sampling-coordinate-allocation/ || echo "not ignored"
```

Expected: `ls-files` lists 3 files; `check-ignore` reports the path is not ignored.

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
git diff -- pinn_instruction/markdown_conversion/framework-specs/sampling_method.md
```

Expected: no diff for `sampling_method.md`.

---

### Task 2: Verify This Plan File Exists at the Canonical Path

**Files:**
- Read only.

The plan already lives at the canonical path (see "Save Target" above). This task verifies it is present and contains the expected anchors; it does **not** create a second dated/hyphenated copy.

- [ ] **Step 1: Verify the plan file exists at the canonical path**

Run:

```bash
test -f "docs/work/plans/milestone_v1.4/20.5-gsd-workflow-repair/phase-20.5-gsd-workflow-repair-implementation-plan.md"
```

Expected: exit `0`.

- [ ] **Step 2: Verify the plan contains key anchors**

Run:

```bash
rg -n "Non-Execution Guard|Do not edit .*sampling_method.md|Validate GSD Recognition" "docs/work/plans/milestone_v1.4/20.5-gsd-workflow-repair/phase-20.5-gsd-workflow-repair-implementation-plan.md"
```

Expected: command exits `0` and prints matches for all three patterns. Grep the stable phrase `"Validate GSD Recognition"` (used by Task 7) rather than a task-number-prefixed string, so the check is robust to task renumbers.

- [ ] **Step 3: Confirm no dated/hyphenated duplicate exists**

Run:

```bash
test ! -f docs/plans/2026-05-22-phase-20-5-gsd-workflow-repair-plan.md
```

Expected: exit `0` (the stale-naming duplicate must not be created).

---

### Task 3: Repair Phase Directory Identity

**Files:**
- Create: `.planning/phases/20.5-sampling-coordinate-allocation/`
- `git mv` from: `.planning/phases/20-5-sampling-coordinate-allocation/`

**Rationale for `git mv` (not `cp` + filesystem `mv`):** the source directory is git-tracked (see Task 1 Step 1). Using `cp` would leave the deletions of the tracked old paths *unstaged*, breaking Task 8 Step 1's "status shows only repair docs" check and producing a dirty post-commit tree. `git mv` stages both rename sides atomically; git's rename detection preserves history without requiring a separate `.planning/archives/` copy.

- [ ] **Step 1: Create the canonical directory**

Run:

```bash
mkdir -p .planning/phases/20.5-sampling-coordinate-allocation
```

- [ ] **Step 2: `git mv` each tracked artifact into the dot-decimal directory with renames**

Run:

```bash
git mv .planning/phases/20-5-sampling-coordinate-allocation/20-5-GAPS.md     .planning/phases/20.5-sampling-coordinate-allocation/20.5-GAPS.md
git mv .planning/phases/20-5-sampling-coordinate-allocation/20-5-RESEARCH.md .planning/phases/20.5-sampling-coordinate-allocation/20.5-RESEARCH.md
git mv .planning/phases/20-5-sampling-coordinate-allocation/20-5-PLAN.md     .planning/phases/20.5-sampling-coordinate-allocation/20.5-MONOLITHIC-SOURCE-PLAN.md
```

Note the third rename also changes the basename to `20.5-MONOLITHIC-SOURCE-PLAN.md` — this signals the file is historical source material, not an executable phase plan.

- [ ] **Step 3: Normalize moved-file frontmatter and references**

Edit the moved files in place:
- In `20.5-GAPS.md`, ensure `phase: "20.5"` (or `20.5-sampling-coordinate-allocation`) in the frontmatter; rewrite any *path* references from `20-5-sampling-coordinate-allocation/20-5-*.md` → `20.5-sampling-coordinate-allocation/20.5-*.md`. **Per DG-2, do NOT rename the gap IDs `GAP-20-5-01/02/03` — they are `RESOLVED-WITH-INSTRUCTION` locked records from the 2026-05-19 audit trail and serve as permanent historical identifiers.** Only path identity is normalized.
- In `20.5-RESEARCH.md`, rewrite path references the same way; preserve any historical reference to the monolithic plan as `20.5-MONOLITHIC-SOURCE-PLAN.md` (historical/source context) rather than the new `20.5-0X-PLAN.md` files (executable plans).
- In `20.5-MONOLITHIC-SOURCE-PLAN.md`, add this first line after the title:

```markdown
> **SOURCE ONLY:** This monolithic plan is retained as historical source material for the canonical split `20.5-0X-PLAN.md` files. Do not execute this file. Path references within may still use the legacy `20-5-*` naming where they reflect the document's original 2026-05-19 state — normalize forward-pointing references only.
```

**Context-aware path normalization (replaces the critique's blanket rule):** when normalizing path references during this step or Task 4 Step 4, distinguish:
- "the (now-archived) source / historical / monolithic plan" → `20.5-MONOLITHIC-SOURCE-PLAN.md`
- "the (executable) phase plan" / "the split plan" → the appropriate `20.5-0X-PLAN.md`
- A blind global replace of `20-5-PLAN.md` → `20.5-MONOLITHIC-SOURCE-PLAN.md` will misdirect references that should now point at the split plans.

- [ ] **Step 4: Remove the now-empty old directory**

Run:

```bash
rmdir .planning/phases/20-5-sampling-coordinate-allocation
```

Expected: `rmdir` succeeds (the directory contains only the three files that were just `git mv`'d out). If `rmdir` fails because an untracked file remains, investigate before proceeding — do not `rm -rf`.

Verify no `20-5` directory remains under `.planning/phases/`:

```bash
test ! -d .planning/phases/20-5-sampling-coordinate-allocation
ls -d .planning/phases/20-5-* 2>/dev/null && echo "FAIL: hyphenated dir still present" || echo "OK"
```

---

### Task 4: Register Phase 20.5 Without Executing It

**Files:**
- Modify: `.planning/REQUIREMENTS.md` — add SAMP-01/02; **amend SCOPE-02**; add SCOPE-05; add **ARCH-05 traceability rows** for SAMP-01/02; **bump count 30 → 32**; update SCOPE-01–04 enumeration to SCOPE-01–05.
- Modify: `.planning/milestones/v1.4-GAPS.md` — append `## Phase 20.5` section with the three `RESOLVED-WITH-INSTRUCTION` gaps; bump `total_gaps` 17 → 20, `resolved_gaps` 17 → 20, `last_updated`.
- Modify: `AGENTS.md` — add the SCOPE-05 cross-reference after the existing `pinn/` no-live-code directive (covers `CLAUDE.md`/`GEMINI.md` automatically since both are symlinks → `AGENTS.md`).
- Modify: `ANTIGRAVITY.md` — add the SCOPE-05 cross-reference in §1.4 governance after the `Live PINN code is not v1.4 grounding` bullet.
- Verify-only (no edit unless missing/stale): `.planning/ROADMAP.md`, `.planning/STATE.md`, `.planning/MILESTONES.md`, `.planning/PROJECT.md`. Commit `a9ecd51` (2026-05-20) already inserted Phase 20.5 status into all four. Steps 1 and 3 are verification gates, not edits, and exist only to catch regressions.

**Governance decision record (resolves DG-1/2/3 from the critique review).** This repair applies these resolutions:
- **DG-1:** SCOPE-05 propagation to root agent-instruction files happens **during repair** (Steps 5 below), alongside the REQUIREMENTS.md SCOPE-05 row in Step 2. Splitting the two — REQUIREMENTS now, propagation later in `20.5-01` — would create a transient window in which the rule exists in `REQUIREMENTS.md` but not in agent instructions; doing both together is the consistent option already taken for the REQUIREMENTS.md edit.
- **DG-2:** Gap IDs `GAP-20-5-01/02/03` are **preserved as historical identifiers** (no rename to `GAP-20.5-*`). They are `RESOLVED-WITH-INSTRUCTION` locked records on the 2026-05-19 audit trail. Only directory identity and *path* references are normalized to dot-decimal — see Step 4. A partial rename is the worst outcome (dangling IDs).
- **DG-3:** Propagation targets = **`AGENTS.md` + `ANTIGRAVITY.md`** only. `CLAUDE.md` and `GEMINI.md` are symlinks → `AGENTS.md`, so editing `AGENTS.md` covers them automatically.

- [ ] **Step 1: Verify Phase 20.5 is present in ROADMAP.md (no edit unless missing)**

Run:

```bash
rg -n "Phase 20\.5|20\.5-sampling-coordinate-allocation" .planning/ROADMAP.md
```

Expected: at least one match describing Phase 20.5 as inserted before Phase 21 (commit `a9ecd51` placed it at `ROADMAP.md:9`). If missing, add this line near the v1.4 milestone block:

```markdown
- 🚧 **v1.4 Resolving 01 Architecture and Physics Foundations** — Phases 16–21, with Phase 20.5 inserted before Phase 21
```

Do not mark Phase 20.5 complete; the execution remains pending.

- [ ] **Step 2: Add SAMP requirements, amend SCOPE-02, add SCOPE-05, add ARCH-05 traceability rows, bump counts, update scope enumeration**

This step lands the **full monolithic Task 2 registration set** (`20-5-PLAN.md:156–238`). The earlier draft only added SAMP-01/02 and SCOPE-05; that left REQUIREMENTS.md internally inconsistent (SCOPE-02 still capping `sampling_method.md` to FRAME-03, no traceability rows, the "30 total" line and SCOPE-01–04 enumeration both unchanged).

**(2a) Add SAMP-01/02 requirements** under a new `### Sampling Coordinate Allocation` heading:

```markdown
### Sampling Coordinate Allocation

- [ ] **SAMP-01**: `sampling_method.md` documents an explicit Sobol coordinate allocation convention with no coordinate reused for two independent physical quantities. Allocation order: position → optional scale → optional velocity. Dimension formula `d = 3 + δ_s + 3δ_v`, where `δ_s = 1` iff sampling-time scaling is enabled and `δ_v = 1` iff velocity sampling is enabled.
- [ ] **SAMP-02**: The §1.1 dimension claim, the "Sampling-Time Size Variability" prose, and the "Velocity Sampling" prose/formula in `sampling_method.md` are mutually consistent and agree with the locked allocation, matching `simulation_data/Scripts/ic_generation/ic_generation_utils.py` (the implementation that generated the existing standard quasi-random dataset).
```

**(2b) Amend SCOPE-02** in the Scope Boundaries table at `REQUIREMENTS.md:74`. Replace the existing row:

```markdown
| **SCOPE-02** `sampling_method.md` revisions | **In scope, limited to FRAME-03** — hierarchical post-perturbation COM offset wording and any cross-reference needed for the unified preprocessing contract. No sampling-method content unrelated to Issue 01 is rewritten. |
```

with:

```markdown
| **SCOPE-02** `sampling_method.md` revisions | **In scope, limited to (a) FRAME-03** — hierarchical post-perturbation COM offset wording and any cross-reference needed for the unified preprocessing contract — **AND (b) SAMP-01/SAMP-02** — the Sobol coordinate allocation convention (Phase 20.5). No sampling-method content unrelated to (a) or (b) is rewritten. Other sampling-method discrepancies surfaced during Phase 20.5 (velocity-momentum reconciliation, §2.1 enhancement framing) are flagged to `docs/findings/` for separate handling and explicitly excluded from Phase 20.5 scope. |
```

This is the **highest-severity defect in the earlier draft**: without this amendment, the future `20.5-02` edit to `sampling_method.md` would violate SCOPE-02's own scope boundary — a live governance contradiction.

**(2c) Add SCOPE-05** as a new row in the same Scope Boundaries table:

```markdown
| **SCOPE-05** Data-spec alignment for sampling-method edits | When v1.4 framework-spec edits describe the data-generation pipeline, they MUST match the actual behavior of `simulation_data/Scripts/ic_generation/`. The no-live-code directive (2026-05-19) targets `pinn/` only; `simulation_data/Scripts/ic_generation/` is a permitted grounding source for data-generation specs because the existing dataset is fixed and the framework must remain compatible with it. Spec divergences from data must be (i) reconciled to match data, (ii) flagged in `docs/findings/` for separate handling, or (iii) explicitly authorized by the user as a data-regeneration directive for FUT-01. |
```

**(2d) Add ARCH-05 traceability rows** for SAMP-01/02. Find the traceability table that already contains `ARCH-05 | Phase 20 | Pending` near `REQUIREMENTS.md:117` and append:

```markdown
| SAMP-01 | Phase 20.5 | Pending |
| SAMP-02 | Phase 20.5 | Pending |
```

**(2e) Update the count line** at `REQUIREMENTS.md:126`. Replace:

```markdown
- v1.4 requirements: 30 total (5 EVID + 4 IO + 4 FRAME + 6 PHYS + 5 ARCH + 6 VER)
- Mapped to phases: 30
```

with:

```markdown
- v1.4 requirements: 32 total (5 EVID + 4 IO + 4 FRAME + 6 PHYS + 5 ARCH + 6 VER + 2 SAMP)
- Mapped to phases: 32
```

**(2f) Update the scope-annotations enumeration** in the same block. Replace:

```markdown
- SCOPE-01/02/03/04 are scope-boundary annotations (see "Scope Boundaries" table above), not numbered requirements.
```

with:

```markdown
- SCOPE-01 through SCOPE-05 are scope-boundary annotations (see "Scope Boundaries" table above), not numbered requirements.
```

**(2g) Verify the REQUIREMENTS.md edits** (mirrors monolithic Task 2 Step 6):

```bash
grep -cE "SAMP-01|SAMP-02" .planning/REQUIREMENTS.md
grep -cF "**SCOPE-05** Data-spec alignment" .planning/REQUIREMENTS.md
grep -cF "32 total" .planning/REQUIREMENTS.md
grep -cF "SAMP-01/SAMP-02" .planning/REQUIREMENTS.md
grep -cF "SCOPE-01 through SCOPE-05" .planning/REQUIREMENTS.md
```

Expected: first ≥ 4 (SAMP-01/02 definitions, 2 traceability rows, SCOPE-02 amendment mention); second = 1; third = 1; fourth ≥ 1 (the amended SCOPE-02 row); fifth = 1.

- [ ] **Step 3: Verify Phase 20.5 status is present in STATE.md (no edit unless missing)**

Run:

```bash
rg -n "Phase 20\.5|20\.5-sampling-coordinate-allocation" .planning/STATE.md
```

Expected: at least one match (commit `a9ecd51` placed the Phase 20.5 status note at `STATE.md:78`). If missing, append this note to the v1.4 status block (do not change current Phase 19 focus):

```markdown
- Phase 20.5 workflow repair complete (this commit): canonical GSD identity is `.planning/phases/20.5-sampling-coordinate-allocation/`; execution remains pending and must not begin before explicit user authorization or the normal post-Phase-20 sequence.
```

- [ ] **Step 4: Replace stale `20-5` paths in planning docs (paths only, not gap IDs)**

Per DG-2, **path identity** is normalized; **gap IDs** (`GAP-20-5-0X`) and **commit-message scopes** (e.g., `docs(20-5):`) are NOT touched.

Run:

```bash
rg -n "20-5-sampling-coordinate-allocation|20-5-PLAN|20-5-RESEARCH|20-5-GAPS" .planning docs/superpowers 2>/dev/null
```

Replace stale executable-path references with the appropriate dot-decimal path, applying the context-aware rule from Task 3 Step 3:
- Forward-pointing path references to the (current) phase content → `20.5-sampling-coordinate-allocation/20.5-{GAPS,RESEARCH,0X-PLAN}.md`.
- Historical/source references to the (now-archived) monolithic plan → `20.5-MONOLITHIC-SOURCE-PLAN.md`.
- **Explicit scope:** `.planning/**` IS in scope. `docs/work/designs/cross_cutting/latex-sync/2026-05-24-latex-markdown-sync-strategy-design.md` (the third file currently still carrying `20-5-*` refs) — include only if its references are forward-pointing path mentions; leave them alone if they are historical context. `docs/findings/**` and `docs/work/plans/milestone_v1.4/20.5-gsd-workflow-repair/phase-20.5-gsd-workflow-repair-implementation-plan.md` are OUT of scope (this plan and its critique review are *themselves* the audit trail; rewriting them would corrupt their own historical citations).

Quotes inside frontmatter (`origin: "..."`), commit-message bodies, and quoted historical evidence MUST remain as-is. Historical references to the original gap IDs (e.g., "GAP-20-5-01" in the 2026-05-19 audit trail in `20.5-GAPS.md`) MUST remain as-is — see DG-2.

- [ ] **Step 5: Propagate SCOPE-05 to root agent-instruction files (per DG-1)**

This step lands the monolithic Task 3 propagation that the earlier draft dropped. Targets are `AGENTS.md` (a regular file; `CLAUDE.md` and `GEMINI.md` are symlinks → `AGENTS.md`, so editing AGENTS.md covers all three) and `ANTIGRAVITY.md` (a separate 15 KB file).

**(5a) Verify the symlink topology** before editing (defensive check — fails loud if the topology changed):

```bash
test -L CLAUDE.md
test -L GEMINI.md
test ! -L AGENTS.md
test ! -L ANTIGRAVITY.md
readlink CLAUDE.md | grep -qx AGENTS.md
readlink GEMINI.md | grep -qx AGENTS.md
```

Expected: all six exit `0`. If any fail, **stop** and surface — the propagation strategy depends on the symlink topology and must be re-confirmed before editing.

**(5b) Edit `AGENTS.md`** immediately after the existing `pinn/` no-live-code directive (currently around `AGENTS.md:27`). Add a paragraph:

```markdown
**`simulation_data/Scripts/ic_generation/` IS a permitted grounding source for data-generation specs** (`.planning/REQUIREMENTS.md` SCOPE-05, added 2026-05-20). The existing standard-quasi-random dataset was generated by that code; the v1.4 sampling-method spec must remain compatible with it. SCOPE-05 is a narrow carveout from SCOPE-01's `pinn/` no-live-code directive and applies only to the data-generation pipeline. Other live-code categories remain off-limits. See `.planning/REQUIREMENTS.md` SCOPE-05 for the canonical rule.
```

Link to `.planning/REQUIREMENTS.md` SCOPE-05 as the canonical source rather than duplicating the full rule text. Do **not** widen the carveout beyond `simulation_data/Scripts/ic_generation/`.

**(5c) Edit `ANTIGRAVITY.md`** in the §1.4 governance block (around `ANTIGRAVITY.md:35`), immediately after the bullet `- **Live PINN code is not v1.4 grounding**: ...`. Add a parallel bullet:

```markdown
- **Data-generation script carveout (SCOPE-05)**: `simulation_data/Scripts/ic_generation/` IS a permitted grounding source for data-generation specs in `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`, distinct from the `pinn/` no-live-code directive above. The existing standard-quasi-random dataset was generated by that code, and v1.4 sampling-method content must remain compatible with the data. Spec divergences from data must be reconciled to match data, flagged to `docs/findings/`, or explicitly authorized by the user as a data-regeneration directive for FUT-01. See `.planning/REQUIREMENTS.md` SCOPE-05.
```

**(5d) Verify the propagation:**

```bash
grep -cF "SCOPE-05" AGENTS.md
grep -cF "SCOPE-05" ANTIGRAVITY.md
grep -cF "simulation_data/Scripts/ic_generation/" AGENTS.md
grep -cF "simulation_data/Scripts/ic_generation/" ANTIGRAVITY.md
```

Expected: each ≥ 1. Confirm the AGENTS.md addition does not contradict the existing `pinn/` directive (SCOPE-05 is narrower than, not a replacement for, SCOPE-01).

- [ ] **Step 6: Register Phase 20.5 in the milestone gap index `v1.4-GAPS.md`**

This step lands Gap 1.2 from the critique. The three Phase 20.5 gaps are **already** `RESOLVED-WITH-INSTRUCTION` (per user approval 2026-05-19, recorded in `20.5-GAPS.md` line 10 governance frontmatter and `:60`, `:89`, `:121` Status fields). They are not new/open gaps — they are pre-existing resolved entries that simply have not yet been mirrored to the milestone-wide index.

**(6a) Append a new `## Phase 20.5` section** to `.planning/milestones/v1.4-GAPS.md` after the existing `## Phase 19` block, mirroring the format used for Phases 17/18/19:

```markdown
## Phase 20.5: Sampling Coordinate Allocation

**Register:** `.planning/phases/20.5-sampling-coordinate-allocation/20.5-GAPS.md`

**Resolution batch:** On 2026-05-19, the user approved the Phase 20.5 design (commit b727b15 adversarial-review-fix lineage and the prior design-lock commit). That approval resolved `GAP-20-5-01`, `GAP-20-5-02`, and `GAP-20-5-03` together. The hyphenated `GAP-20-5-*` IDs are preserved as permanent historical identifiers (per repair DG-2); the directory and path identity have been normalized to dot-decimal `20.5-*`.

| Gap | Decision | Resolution |
|-----|----------|------------|
| GAP-20-5-01 | Sobol coordinate allocation convention | RESOLVED-WITH-INSTRUCTION: Option A — `u_4` = sampling-time scale, `u_5`–`u_7` = velocity components (for standard config, `rotate=False`); dimension `d = 3 + δ_s + 3δ_v` matches `simulation_data/Scripts/ic_generation/ic_generation_utils.py`. |
| GAP-20-5-02 | New acceptance-check name `AC-SAMP-01` | RESOLVED-WITH-INSTRUCTION: approved in Phase 20.5 design review 2026-05-19 (precedent: GAP-17-02). |
| GAP-20-5-03 | Hand-off file naming `20.5-DATA-ALIGNMENT.md` | RESOLVED-WITH-INSTRUCTION: use dot-decimal `20.5-DATA-ALIGNMENT.md` for the eventual hand-off file. |
```

**(6b) Bump the frontmatter** at the top of `v1.4-GAPS.md`. Replace:

```yaml
total_gaps: 17
open_gaps: 0
resolved_gaps: 17
deferred_gaps: 0
last_updated: 2026-05-26
```

with:

```yaml
total_gaps: 20
open_gaps: 0
resolved_gaps: 20
deferred_gaps: 0
last_updated: 2026-05-27
```

(Use the current date if executing on a later day.)

**(6c) Verify:**

```bash
grep -cF "## Phase 20.5" .planning/milestones/v1.4-GAPS.md
grep -cF "GAP-20-5-01" .planning/milestones/v1.4-GAPS.md
grep -cF "GAP-20-5-02" .planning/milestones/v1.4-GAPS.md
grep -cF "GAP-20-5-03" .planning/milestones/v1.4-GAPS.md
grep -cF "total_gaps: 20" .planning/milestones/v1.4-GAPS.md
grep -cF "resolved_gaps: 20" .planning/milestones/v1.4-GAPS.md
```

Expected: each = 1.

The split-plan `20.5-01-PLAN.md` and `20.5-03-PLAN.md` files (created in Task 6) list `v1.4-GAPS.md` as `files_modified` with a "verify and no-op" guard so future plan execution does not re-register an already-recorded resolution.

- [ ] **Step 7: Verify MILESTONES.md and PROJECT.md have Phase 20.5 status (no edit unless missing/stale)**

Run:

```bash
rg -n "Phase 20\.5|20\.5-sampling-coordinate-allocation" .planning/MILESTONES.md .planning/PROJECT.md
```

Expected: matches in both files (commit `a9ecd51` placed Phase 20.5 entries at `MILESTONES.md:26`, `:31`, and `PROJECT.md:99`, `:163`). If `PROJECT.md` still references the hyphenated `20-5-sampling-coordinate-allocation/` directory path, replace those *path* references with `20.5-sampling-coordinate-allocation/` (DG-2 path-normalization rule). Do not edit otherwise.

---

### Task 5: Create Missing GSD Pre-Execution Artifacts

**Files:**
- Create: `20.5-SPEC.md`
- Create: `20.5-CONTEXT.md`
- Create: `20.5-DISCUSSION-LOG.md`
- Create: `20.5-PATTERNS.md`
- Create: `20.5-VALIDATION.md`

- [ ] **Step 1: Write `20.5-SPEC.md`**

Create `.planning/phases/20.5-sampling-coordinate-allocation/20.5-SPEC.md` with:
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
- `D-02`: Canonical directory is `.planning/phases/20.5-sampling-coordinate-allocation/`; the old `20-5-sampling-coordinate-allocation/` is removed (its three files were `git mv`'d into the new dir, with the monolithic plan renamed to `20.5-MONOLITHIC-SOURCE-PLAN.md`). Git history preserves the rename audit trail.
- `D-03`: Root registry docs may be repaired now; `sampling_method.md` and probes remain execution work.
- `D-04`: `simulation_data/Scripts/ic_generation/` is allowed grounding for data-generation specs under SCOPE-05; `pinn/` remains disallowed as v1.4 grounding.
- `D-05`: `AC-SAMP-01` pass criteria and any FUT-01 velocity-momentum guidance must be treated as governance-sensitive and surfaced if not already grounded.
- `D-06`: After Phase 19 and Phase 20 complete, Phase 20.5 plans must be rechecked for stale cross-references before execution.
- `D-07` (DG-1, this repair): SCOPE-05 propagation to root agent instructions runs **during repair**, alongside the REQUIREMENTS.md SCOPE-05 row, not deferred to `20.5-01` execution. Splitting the two would leave a transient window where the rule lives in REQUIREMENTS.md but not in agent instructions.
- `D-08` (DG-2, this repair): The hyphenated gap IDs `GAP-20-5-01/02/03` are preserved as permanent historical identifiers. Only **path identity** is normalized from hyphen to dot-decimal. A partial rename of the IDs across the audit trail produces dangling references; a full rename destroys the 2026-05-19 audit-trail anchor.
- `D-09` (DG-3, this repair): SCOPE-05 propagation targets are `AGENTS.md` (covering `CLAUDE.md` and `GEMINI.md` automatically since both are symlinks) and `ANTIGRAVITY.md` (a separate 15 KB file). The symlink topology is verified defensively before editing.
- `D-10` (normalization scope, this repair): Path normalization in Task 4 Step 4 is scoped to `.planning/**` and `docs/superpowers/**` for forward-pointing path references. `docs/findings/**` (audit-trail documents including the critique-review) and the plan files in `docs/plans/` are out of scope — they are themselves part of the historical record and rewriting them would corrupt their own citations.

- [ ] **Step 4: Write `20.5-PATTERNS.md`**

Map artifacts to local analogs:
- `20.5-CONTEXT.md` follows `18-CONTEXT.md`.
- `20.5-DISCUSSION-LOG.md` follows `18-DISCUSSION-LOG.md`.
- `20.5-XX-PLAN.md` follows `18-01-PLAN.md`.
- `20.5-PATTERNS.md` follows `17-PATTERNS.md`.
- `20.5-VALIDATION.md` follows `17-VALIDATION.md` and `18-VALIDATION.md`.

- [ ] **Step 5: Write `20.5-VALIDATION.md`**

Create validation gates:
- **SDK gate:** `init.plan-phase 20.5` is true.
- **Misparse gate:** `init.plan-phase 20` does not resolve any `20-5`/`20.5` directory. (Returning `phase_found: false` is acceptable while the Phase 20 directory does not yet exist.)
- **Plan-index gate:** `phase-plan-index 20.5` returns canonical plan IDs `20.5-01`, `20.5-02`, `20.5-03`.
- **Non-execution gate:** no diff to `sampling_method.md`; no `probes/` directory; no `20.5-SUMMARY.md`, `20.5-VERIFICATION.md`, or `20.5-DATA-ALIGNMENT.md`.
- **REQUIREMENTS consistency gate (M-1/M-3):** `REQUIREMENTS.md` contains SAMP-01, SAMP-02, the SCOPE-02 amendment text mentioning `SAMP-01/SAMP-02`, the SCOPE-05 row, ARCH-05 traceability rows for SAMP-01 and SAMP-02, count line `32 total`, and SCOPE annotation `SCOPE-01 through SCOPE-05`.
- **Milestone-index gate (Gap 1.2/M-5):** `v1.4-GAPS.md` contains a `## Phase 20.5` section with the three `RESOLVED-WITH-INSTRUCTION` gaps, frontmatter `total_gaps: 20` and `resolved_gaps: 20`.
- **Propagation gate (Gap 1.1):** `AGENTS.md` and `ANTIGRAVITY.md` both contain `SCOPE-05` and the `simulation_data/Scripts/ic_generation/` carveout text; symlinks `CLAUDE.md` and `GEMINI.md` still target `AGENTS.md`.
- **Directory-cleanup gate:** `.planning/phases/20-5-sampling-coordinate-allocation/` no longer exists.

---

### Task 6: Create Canonical Split GSD Plans

**Files:**
- Create: `20.5-01-PLAN.md`
- Create: `20.5-02-PLAN.md`
- Create: `20.5-03-PLAN.md`

- [ ] **Step 1: Create `20.5-01-PLAN.md` for governance and registry completion**

Purpose: later execution plan for root registry and governance propagation, only if not already completed by repair. Since this repair already lands the full registration set in Task 4 (REQUIREMENTS.md amendments, SCOPE-05 propagation to AGENTS.md/ANTIGRAVITY.md, v1.4-GAPS.md Phase 20.5 section), this plan's primary content at execution time will be the "verify and no-op" sweep described below.

**Required frontmatter:**

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
  - "AGENTS.md"
  - "ANTIGRAVITY.md"
autonomous: false
requirements:
  - SAMP-01
  - SAMP-02
  - VER-05
---
```

**`depends_on: []` is correct** for this wave-1 first plan (verified convention: Phase 18-01 and Phase 19-01 both use `depends_on: []`). The repair review (and an earlier external critique) suggested adding a cross-phase entry like `"20-03"`; that suggestion is **rejected** because (a) `depends_on` in this project is **intra-phase only** across Phases 16–19, (b) cross-phase sequencing is owned by `ROADMAP.md` + `STATE.md`, and (c) no Phase 20 directory exists yet, making any cross-phase value unimplementable. Sequencing of Phase 20.5 after Phase 20 is already guarded four ways: ROADMAP intent, the Phase 20.5 status note in STATE.md, decisions `D-01`/`D-06` in `20.5-CONTEXT.md`, and the Non-Execution Guard at the head of this plan.

**Task body at execution time:** verify and no-op only. For each file in `files_modified`, confirm the repair-time edit is still present (SAMP-01/02 / SCOPE-05 row / SCOPE-02 amendment / count = 32 / `## Phase 20.5` section in v1.4-GAPS.md / SCOPE-05 cross-reference in AGENTS.md and ANTIGRAVITY.md). Do **not** re-append or duplicate any of these entries. If any verification grep fails, surface the regression and stop — do not silently re-add.

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

**`v1.4-GAPS.md` is a verify-and-no-op target for this plan.** Phase 20.5's three gaps are already registered in the milestone index by the repair (Task 4 Step 6); this plan's role at execution time is to confirm the section still exists and the counts still read `20/20`. Do not re-append. The line stays in `files_modified` for traceability and to allow re-validation runs.

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
- It does **not** resolve `.planning/phases/20.5-sampling-coordinate-allocation/`.
- It does **not** resolve any `20-5-*` directory.
- Since the Phase 20 directory does not yet exist, the response will be `"phase_found": false` (or equivalent). That is the correct post-repair state for Phase 20 itself; the only invariant this step enforces is that querying `20` never picks up Phase 20.5's directory. Earlier wording — "resolves the real Phase 20 directory" — was unsatisfiable because no Phase 20 directory has been created yet; loosen the check to the non-misroute invariant only.

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
test ! -f .planning/phases/20.5-sampling-coordinate-allocation/20.5-SUMMARY.md
test ! -f .planning/phases/20.5-sampling-coordinate-allocation/20.5-VERIFICATION.md
test ! -f .planning/phases/20.5-sampling-coordinate-allocation/20.5-DATA-ALIGNMENT.md
test ! -d .planning/phases/20.5-sampling-coordinate-allocation/probes
git diff -- pinn_instruction/markdown_conversion/framework-specs/sampling_method.md
```

Expected:
- All four `test` commands exit `0`.
- `sampling_method.md` diff is empty.

- [ ] **Step 5: Confirm REQUIREMENTS.md internal consistency (M-3 coverage)**

The Task 4 Step 2 edits must leave `REQUIREMENTS.md` self-consistent. Run:

```bash
rg -c "^\- \[ \] \*\*(SAMP-01|SAMP-02)\*\*" .planning/REQUIREMENTS.md
rg -nF "SAMP-01/SAMP-02" .planning/REQUIREMENTS.md
rg -nF "SAMP-01 | Phase 20.5 | Pending" .planning/REQUIREMENTS.md
rg -nF "SAMP-02 | Phase 20.5 | Pending" .planning/REQUIREMENTS.md
rg -nF "32 total" .planning/REQUIREMENTS.md
rg -nF "SCOPE-01 through SCOPE-05" .planning/REQUIREMENTS.md
rg -nF "**SCOPE-05** Data-spec alignment" .planning/REQUIREMENTS.md
```

Expected: first ≥ 2 (SAMP-01 and SAMP-02 definitions); rows 2–7 each return at least one match. If any returns 0, surface the regression — REQUIREMENTS.md is internally inconsistent and Task 4 Step 2 was not fully applied.

- [ ] **Step 6: Confirm SCOPE-05 propagation landed in root agent-instruction files (Gap 1.1 coverage)**

Run:

```bash
rg -nF "SCOPE-05" AGENTS.md
rg -nF "SCOPE-05" ANTIGRAVITY.md
rg -nF "simulation_data/Scripts/ic_generation/" AGENTS.md
rg -nF "simulation_data/Scripts/ic_generation/" ANTIGRAVITY.md
```

Expected: each ≥ 1 match.

- [ ] **Step 7: Confirm v1.4-GAPS.md Phase 20.5 registration landed (Gap 1.2 coverage)**

Run:

```bash
rg -nF "## Phase 20.5" .planning/milestones/v1.4-GAPS.md
rg -nF "GAP-20-5-01" .planning/milestones/v1.4-GAPS.md
rg -nF "GAP-20-5-02" .planning/milestones/v1.4-GAPS.md
rg -nF "GAP-20-5-03" .planning/milestones/v1.4-GAPS.md
rg -nF "total_gaps: 20" .planning/milestones/v1.4-GAPS.md
rg -nF "resolved_gaps: 20" .planning/milestones/v1.4-GAPS.md
```

Expected: each returns exactly 1.

---

### Task 8: Commit Workflow Repair

**Files:**
- Stage explicit paths only.

**Tracked-vs-untracked notes for this commit:**
- The Task 3 `git mv` operations have already staged both the *deletions* of `.planning/phases/20-5-sampling-coordinate-allocation/20-5-{GAPS,PLAN,RESEARCH}.md` and the *additions* of the moved/renamed files in `.planning/phases/20.5-sampling-coordinate-allocation/`. The Task 8 staging below MUST cover the new directory; the old-path deletions are already staged by `git mv`.
- The `docs/work/plans/milestone_v1.4/20.5-gsd-workflow-repair/phase-20.5-gsd-workflow-repair-implementation-plan.md` file (this plan) is already at its canonical path and was committed in an earlier change (b77358a); only stage it here if Task 2 had to repair its anchors. Do **not** create a dated/hyphenated duplicate.
- This repair commit must **not** contain unrelated Phase 19 work (`.planning/phases/18-frame-and-gauge-contracts/18-03-PLAN.md`, `18-VALIDATION.md`, `18-UAT.md`, EDL 19-01 resolution docs, ADOPT plans, the critique-review findings doc). The repair leaves those for their own commits.

- [ ] **Step 1: Check diff and inventory**

Run:

```bash
git diff --check
git status --short
git status --short | grep -E "^\s*(D|R|A|M)\s" | grep -E "20-5|20\.5|REQUIREMENTS|ROADMAP|STATE|MILESTONES|PROJECT|AGENTS|ANTIGRAVITY|v1\.4-GAPS"
```

Expected:
- `git diff --check` exits `0`.
- Status shows: (a) renamed `.planning/phases/20-5-…/20-5-*.md` → `.planning/phases/20.5-…/20.5-*.md` (and `20.5-MONOLITHIC-SOURCE-PLAN.md`), (b) added new artifact files under `20.5-sampling-coordinate-allocation/`, (c) modified `REQUIREMENTS.md` and `milestones/v1.4-GAPS.md`, (d) modified `AGENTS.md` and `ANTIGRAVITY.md`, (e) optionally modified `ROADMAP.md`/`STATE.md`/`MILESTONES.md`/`PROJECT.md` (only if a verify-step found something missing/stale).
- Unrelated working-tree changes (Phase 19 work, EDL docs, findings docs) are **not** part of this commit.

- [ ] **Step 2: Stage explicit files**

Run:

```bash
# Phase directory: covers the git-mv renames + new artifact files in 20.5-…/.
# Use -A so both the rename-side deletions in the old dir (if any remain) and
# the additions in the new dir are staged.
git add -A .planning/phases/20.5-sampling-coordinate-allocation
git add -A .planning/phases/20-5-sampling-coordinate-allocation 2>/dev/null || true

# Planning / milestone registry edits
git add .planning/REQUIREMENTS.md
git add .planning/milestones/v1.4-GAPS.md

# Optional: stage these only if Task 4 verification found them missing/stale
# and a step in this repair edited them. Otherwise, leave them out so the
# diff is empty for these paths.
[ -n "$(git diff --cached --name-only .planning/ROADMAP.md)" ] || \
  git diff --quiet .planning/ROADMAP.md || \
  git add .planning/ROADMAP.md
[ -n "$(git diff --cached --name-only .planning/STATE.md)" ] || \
  git diff --quiet .planning/STATE.md || \
  git add .planning/STATE.md
[ -n "$(git diff --cached --name-only .planning/MILESTONES.md)" ] || \
  git diff --quiet .planning/MILESTONES.md || \
  git add .planning/MILESTONES.md
[ -n "$(git diff --cached --name-only .planning/PROJECT.md)" ] || \
  git diff --quiet .planning/PROJECT.md || \
  git add .planning/PROJECT.md

# Root agent-instruction propagation (DG-1, DG-3). AGENTS.md covers CLAUDE.md
# and GEMINI.md via symlink; do NOT stage CLAUDE.md or GEMINI.md.
git add AGENTS.md
git add ANTIGRAVITY.md
```

After staging, confirm the staged set:

```bash
git diff --cached --name-only --diff-filter=ACMR | sort
```

Cross-check against every file appearing under "Modify" / "Create" / "Move" in this plan. Any file listed in the plan but absent from `--cached --name-only` means the step that edits it did not run, or the change was not staged — investigate before committing.

- [ ] **Step 3: Commit**

Run:

```bash
git commit -m "$(cat <<'EOF'
docs(20.5): repair GSD workflow identity and complete pre-execution registration

- Rename 20-5-sampling-coordinate-allocation/ → 20.5-sampling-coordinate-allocation/
  (git mv); rename 20-5-PLAN.md → 20.5-MONOLITHIC-SOURCE-PLAN.md (source-only).
- Create pre-execution artifacts (SPEC, CONTEXT, DISCUSSION-LOG, PATTERNS,
  VALIDATION) and split execute-plans (20.5-01/02/03) without executing them.
- REQUIREMENTS.md: add SAMP-01/02, amend SCOPE-02 to permit SAMP-01/02 sampling-
  method edits, add SCOPE-05 (data-spec alignment carveout), add ARCH-05
  traceability rows for SAMP-01/02, bump count 30 → 32, update SCOPE
  annotation to "SCOPE-01 through SCOPE-05".
- v1.4-GAPS.md: append Phase 20.5 section with GAP-20-5-01/02/03 as
  RESOLVED-WITH-INSTRUCTION (preserving historical hyphenated IDs per DG-2);
  bump counts 17 → 20.
- AGENTS.md + ANTIGRAVITY.md: propagate SCOPE-05 cross-reference per DG-1
  and DG-3. CLAUDE.md and GEMINI.md are covered automatically via symlink.
- Preserve historical GAP-20-5-* IDs; normalize only path identity.
- sampling_method.md is NOT edited; SUMMARY/VERIFICATION are NOT created.

Resolves the Phase 20.5 GSD-recognition failure and lands the full monolithic
Task 1–4 registration set the earlier draft had dropped. Phase 20.5 execution
remains pending (gated by Phase 19/20 completion and explicit user authorization).
EOF
)"
```

---

## Test Plan

Run these commands after the commit:

```bash
gsd-sdk query init.plan-phase 20.5
gsd-sdk query init.plan-phase 20
gsd-sdk query phase-plan-index 20.5

# Non-execution invariants
test ! -f .planning/phases/20.5-sampling-coordinate-allocation/20.5-SUMMARY.md
test ! -f .planning/phases/20.5-sampling-coordinate-allocation/20.5-VERIFICATION.md
test ! -f .planning/phases/20.5-sampling-coordinate-allocation/20.5-DATA-ALIGNMENT.md
test ! -d .planning/phases/20.5-sampling-coordinate-allocation/probes
git diff HEAD~1..HEAD -- pinn_instruction/markdown_conversion/framework-specs/sampling_method.md
test ! -d .planning/phases/20-5-sampling-coordinate-allocation

# REQUIREMENTS.md internal consistency (M-1 / M-3 coverage)
grep -cF "32 total" .planning/REQUIREMENTS.md           # expect 1
grep -cF "SAMP-01/SAMP-02" .planning/REQUIREMENTS.md    # expect ≥ 1 (SCOPE-02 amendment + others)
grep -cF "**SCOPE-05** Data-spec alignment" .planning/REQUIREMENTS.md  # expect 1
grep -cF "SCOPE-01 through SCOPE-05" .planning/REQUIREMENTS.md         # expect 1
grep -cF "SAMP-01 | Phase 20.5 | Pending" .planning/REQUIREMENTS.md    # expect 1
grep -cF "SAMP-02 | Phase 20.5 | Pending" .planning/REQUIREMENTS.md    # expect 1

# v1.4-GAPS.md registration (Gap 1.2 / M-5 coverage)
grep -cF "## Phase 20.5" .planning/milestones/v1.4-GAPS.md    # expect 1
grep -cF "total_gaps: 20" .planning/milestones/v1.4-GAPS.md   # expect 1
grep -cF "resolved_gaps: 20" .planning/milestones/v1.4-GAPS.md # expect 1
grep -cF "GAP-20-5-01" .planning/milestones/v1.4-GAPS.md      # expect 1 (historical ID preserved per DG-2)

# Propagation (Gap 1.1 coverage)
grep -cF "SCOPE-05" AGENTS.md       # expect ≥ 1
grep -cF "SCOPE-05" ANTIGRAVITY.md  # expect ≥ 1

git diff --check HEAD~1..HEAD
```

Acceptance:
- Phase `20.5` is recognized by `gsd-sdk`.
- Phase `20` no longer resolves any `20-5`/`20.5` directory (it may legitimately return `phase_found: false` because the Phase 20 directory does not yet exist).
- `20.5-01`, `20.5-02`, and `20.5-03` are indexable plans.
- No substantive Phase 20.5 execution artifact exists (`SUMMARY`, `VERIFICATION`, `DATA-ALIGNMENT`, `probes/`).
- `sampling_method.md` remains unchanged.
- REQUIREMENTS.md is internally consistent: count = 32; SCOPE-02 amended; SCOPE-05 row present; ARCH-05 traceability rows include SAMP-01 and SAMP-02; SCOPE annotation reads "SCOPE-01 through SCOPE-05".
- `v1.4-GAPS.md` carries a `## Phase 20.5` section with the three `RESOLVED-WITH-INSTRUCTION` gaps (historical hyphenated IDs preserved); counts read `total_gaps: 20`, `resolved_gaps: 20`.
- AGENTS.md and ANTIGRAVITY.md carry a SCOPE-05 cross-reference pointing at `.planning/REQUIREMENTS.md` and naming `simulation_data/Scripts/ic_generation/`.
- No old `20-5-sampling-coordinate-allocation/` directory remains under `.planning/phases/`.
- The commit contains only workflow repair artifacts (no Phase 19, EDL, or findings work bundled in).

## Assumptions and Decision Records

**Working assumptions:**
- Public phase label remains `20.5`; do not rename it to `20.1`.
- Root registry updates (REQUIREMENTS.md, milestone gap index, AGENTS.md, ANTIGRAVITY.md) are **workflow repair**, not Phase 20.5 execution: requirements remain pending; no spec/probe work runs; `sampling_method.md` is untouched.
- The existing `.planning/phases/20-5-sampling-coordinate-allocation/` directory is **git-tracked** (verified by `git ls-files`). It contains three files (`20-5-GAPS.md`, `20-5-PLAN.md`, `20-5-RESEARCH.md`), all moved by `git mv` in Task 3. Earlier draft assumption that these were "untracked source material" was wrong.
- ROADMAP.md, STATE.md, MILESTONES.md, and PROJECT.md already carry Phase 20.5 status from commit `a9ecd51` (2026-05-20). Task 4 Steps 1, 3, and 7 are verify-only; they edit only on a missing/stale match.
- `CLAUDE.md` and `GEMINI.md` are symlinks → `AGENTS.md`. Editing `AGENTS.md` automatically updates all three. `ANTIGRAVITY.md` is an independent 15 KB file and must be edited separately.
- Phase 20.5's three gaps (`GAP-20-5-01/02/03`) are pre-existing `RESOLVED-WITH-INSTRUCTION` entries (user approval 2026-05-19, recorded in the gap register frontmatter). Task 4 Step 6 mirrors them into the milestone index; it does not re-resolve or re-approve.

**Decision Gate record (resolutions adopted from `docs/findings/milestone_v1.4/phase_20.5_plan_critique_review.md` Part 4):**
- **DG-1 (SCOPE-05 propagation placement):** Propagate **during repair** (Task 4 Step 5), alongside the REQUIREMENTS.md SCOPE-05 row. Rationale: avoids a transient window where the rule exists in REQUIREMENTS.md but not in agent instructions.
- **DG-2 (gap-ID rename):** **Preserve historical hyphenated IDs** `GAP-20-5-01/02/03`. Only **path identity** is normalized to dot-decimal. Rationale: the IDs are on a `RESOLVED-WITH-INSTRUCTION` audit trail from 2026-05-19; a half-rename produces dangling references; a full rename across the audit trail destroys the precedent value of the original IDs.
- **DG-3 (propagation targets):** **`AGENTS.md` + `ANTIGRAVITY.md`** only. CLAUDE.md and GEMINI.md are symlinks → AGENTS.md and are covered automatically. The symlink topology is verified defensively in Task 4 Step 5(a) before editing.

These three decisions are also recorded in `20.5-CONTEXT.md` (Task 5 Step 3) so the choices are auditable from the phase artifacts themselves and not only from this implementation plan.

**Sources / verification basis for this revision:**
- Critique-review document: `docs/findings/milestone_v1.4/phase_20.5_plan_critique_review.md` (2026-05-27)
- Monolithic source plan: `.planning/phases/20-5-sampling-coordinate-allocation/20-5-PLAN.md` (lines 156–298 for the registration + propagation tasks)
- Verified live state at revision time: REQUIREMENTS.md:74/117/126; v1.4-GAPS.md frontmatter (17/17); AGENTS.md:27; ANTIGRAVITY.md:35; STATE.md:75–78; MILESTONES.md:26/31; ROADMAP.md:9; symlink topology for CLAUDE.md/GEMINI.md.
- GSD frontmatter convention for first-wave plans: `.planning/phases/18-frame-and-gauge-contracts/18-01-PLAN.md` and `.planning/phases/19-physics-and-loss-contracts/19-01-PLAN.md` (both `wave: 1`, `depends_on: []`).

**Recommended execution mode** after leaving Plan Mode: `superpowers:subagent-driven-development`, with one worker for directory/registry repair (Tasks 1–4) and one worker for artifact creation (Tasks 5–6), and a reviewer for SDK validation and the consistency checks (Task 7). Worker A must complete Task 4 before Worker B begins Task 6 because the split plans reference SAMP-01/02/SCOPE-05/v1.4-GAPS state landed in Task 4.
