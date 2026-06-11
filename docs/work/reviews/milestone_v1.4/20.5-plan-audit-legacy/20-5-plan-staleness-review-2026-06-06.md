---
status: consumed
purpose: other
created: unknown
milestone: v1.4
phase: 20.5-plan-audit-legacy
retirement_trigger: milestone complete; superseded by subsequent work
---

# Phase 20.5 Plan Staleness Review — 2026-06-06

**Review conducted:** 2026-06-06
**Plan authored:** 2026-05-19
**Plan path:** `.planning/milestones/v1.4-phases/20-5-sampling-coordinate-allocation/20-5-PLAN.md`
**Phases executed since plan was written:** 17 (completed), 18 (completed), 19 (completed), 20 (completed 2026-06-05)

---

## Executive Summary

The Phase 20.5 Sobol Coordinate Allocation plan is **not currently executable as written**. It has 3 CRITICAL blockers (FROM-text mismatches caused by Phase 18 edits), 3 HIGH-severity staleness issues (partially-redundant tasks, stale gap counts), and 2 pending cross-reference verifications (Phase 18/19 FLAG-10). All are fixable with targeted plan edits. Estimated remediation effort: 30-45 minutes.

**Side note:** The similarly-named `20-05-PLAN.md` (ARCH-04 I_norm naming in `20-architecture-and-normalization-cleanup/`) was already executed on 2026-06-05. The plan under review here is the separate `20-5-PLAN.md` (Sobol coordinate allocation).

---

## Dimension 1: Logical Integrity

### 🔴 CRITICAL: Task 5, Edit 5 — FROM text mismatch (momentum conservation sentence)

**What the plan says to match:**
```
The sampler then enforces total momentum conservation by adjusting the velocity of the fixed particle so that $\sum_i m_i \mathbf{v}_i = 0$.
```

**What the file actually contains (lines 129-131):**
```
The sampler then enforces total momentum conservation for the equal-mass case
by setting `v1 = -v2/2` and `v3 = -v2/2`, so
$\sum_i m_i \mathbf{v}_i = 0$.
```

**Root cause:** Phase 18 commit `34cd746` (`docs(18-02): align quasi-random momentum prose`) updated the momentum-conservation sentence to match the code's symmetric split. This was correct behavior for Phase 18, but invalidates the plan's FROM block.

**Impact:** The Edit tool will fail with "old_string not found." An autonomous agent will either:
- (a) Stop with an error (best case — surface the mismatch)
- (b) Try to manually locate and edit, potentially corrupting the file (worst case)

**Fix needed:** Update the FROM block in Edit 5 to match the current 3-line momentum sentence, AND update the corresponding TO block (the plan's replacement text) to preserve the Phase 18 wording rather than reverting it. Also update the plan's instruction "Note: the momentum-conservation sentence...is preserved verbatim — do NOT alter it here" since Phase 18 already altered it.

### 🔴 CRITICAL: Task 8 — Sub-conflict #1 is already resolved

The plan's Task 8 creates `docs/findings/velocity_momentum_sampling_discrepancy.md` documenting a contradiction between `sampling_method.md` ("adjusting the velocity of the fixed particle") and `ic_generation_utils.py` (symmetric `v1 = v3 = -v2/2` split).

**Phase 18 commit `34cd746` already resolved this.** The spec now says "by setting `v1 = -v2/2` and `v3 = -v2/2`" — matching the code. The discrepancy no longer exists.

**Impact:** Creating the finding file would document a phantom issue. The finding's claim "the spec's singular wording does not state" the symmetric split is now false.

**Fix needed:** Either remove Task 8 entirely, or repurpose it to document that Phase 18 resolved this (a brief note rather than a full discrepancy finding). The plan's "Post-Completion Follow-ups" should also be checked.

### 🔴 CRITICAL: Task 4, Step 2 — v1.4-GAPS.md frontmatter count is stale

**Plan assumes:** `total_gaps: 11` → change to `14`
**Current actual:** `total_gaps: 21`

The v1.4-GAPS.md frontmatter has accumulated 10 additional gaps from Phases 18, 19, and 20 since the plan was written.

**Impact:** The FROM text `total_gaps: 11` will not match. An Edit would fail. Even if manually corrected, the plan's math (`11 + 3 = 14`) doesn't account for the 10 gaps added by Phases 18-20.

**Fix needed:** Read the current frontmatter, compute `current_total + 3 = new_total` (likely 24), and update Step 2 accordingly.

### 🟡 HIGH: Task 1, Step 4 — Phase 20.5 details block insertion location

The ROADMAP.md already has Phase 20.5 references (6 total) including the phase list item and progress table row, but does NOT have the `### Phase 20.5: Sampling Coordinate Allocation` details block. The insertion point (`### Phase 21: Acceptance Checks...`) still exists at line 220.

**However**, the plan's Steps 1-3 are partially redundant:
- Step 1 (mkdir): harmless, will succeed (directory exists)
- Step 2 (phase list item): the item already exists at line 108 with slightly different wording
- Step 3 (coverage bump): the coverage line may have changed format — verify before editing
- Step 5 (progress table row): the row already exists at line 260

**Fix needed:** Add a pre-condition check at Task 1 start: verify which content already exists and skip/adapt steps accordingly. Convert Step 2 from "insert after Phase 20 line" to "verify existing and reconcile wording if needed."

### 🟡 HIGH: Task 2 — REQUIREMENTS.md FROM text blocks need verification

REQUIREMENTS.md has zero SAMP/SCOPE-05 references — so Task 2's substantive content is still needed. However, the FROM text blocks (e.g., SCOPE-02 table row, SCOPE-04 table row, Coverage block, ARCH-05 traceability row) may have shifted due to Phase 17-20 REQUIREMENTS.md edits.

**Fix needed:** Re-verify every FROM block in Task 2 against the current REQUIREMENTS.md before execution. The SCOPE-02 amendment and traceability row insertion are particularly at risk since Phase 20 added ARCH requirements.

### 🟡 HIGH: Post-completion FLAG-10 cross-reference verification is now DUE, not deferred

The plan's "Post-Completion Follow-ups" section says:
> "After Phases 18 and 19 complete, confirm that the cross-references in sampling_method.md to their scaling conventions remain accurate."

Phases 18 and 19 are now complete. This verification should be done **during** Phase 20.5 execution (after Task 5 applies the spec edits), not deferred to post-completion.

Specifically, Edit 3's Disambiguation note references:
- Phase 18 FRAME-04 (scaling order)
- Phase 19 PHYS-01 (`D = (G T^2)^{1/3}` convention)

And Edit 4 references preprocessing-time scaling. These references must be verified against what Phase 18 and 19 actually locked.

---

## Dimension 2: Execution Clarity

### 🟡 MEDIUM: Two "Phase 20.5" plans create naming ambiguity

The repository has:
- `.planning/milestones/v1.4-phases/20-architecture-and-normalization-cleanup/20-05-PLAN.md` — ARCH-04 I_norm naming (EXECUTED)
- `.planning/milestones/v1.4-phases/20-5-sampling-coordinate-allocation/20-5-PLAN.md` — Sobol allocation (PENDING)

The `v1.4-GAPS.md` heads-up note (line 78) warns about this: "GSD find-phase 20 / init.phase-op 20 resolves to the Phase 20.5 directory." An autonomous agent could execute the wrong plan.

**Fix needed:** Add an explicit path disambiguation at the top of 20-5-PLAN.md.

### 🟡 MEDIUM: Task 3 delegates to `gsd-docs-update` skill

The plan delegates SCOPE-05 propagation to an external skill with detailed instructions. This is reasonable but fragile:
- The skill's output format may have changed
- The skill may modify files the plan doesn't expect
- The review step (Step 2) relies on manual manifest comparison

**Current state:** CLAUDE.md has no SCOPE-05 reference, so Task 3 is still needed.

**Fix needed:** Add a fallback: if `gsd-docs-update` fails or produces unexpected output, manually add the SCOPE-05 cross-reference to CLAUDE.md.

### 🟢 LOW: Task 6 probe calls `_process_sobol_batch` (private method)

The probe accesses `EnhancedThreeBodySampler._process_sobol_batch`, a private method. If `ic_generation_utils.py` were refactored, the probe would break. Currently safe — the file hasn't materially changed since the plan was written (only renamed in `16d1b89`).

### 🟢 LOW: Phase 18 added FRAME-03 notes adjacent to edit targets

Phase 18 added two `FRAME-03 frame note` blocks to `sampling_method.md`:
- After the hierarchical generation section (lines 71-79)
- After the velocity sampling section (lines 133-138)

These sit adjacent to the plan's edit targets. They don't interfere with FROM text matching (verified above) but an agent should be aware they exist and not accidentally modify them.

---

## Dimension 3: Operational Resilience

### 🟡 MEDIUM: No pre-flight verification step

The plan has no initial checkpoint to verify that FROM text blocks still match. An agent will discover mismatches mid-execution (at Task 5), wasting work from Tasks 1-4.

**Fix needed:** Add a Task 0 (pre-flight): run all FROM text matches as dry-run `grep` checks. If any fail, surface the mismatch before any file is modified.

### 🟡 MEDIUM: Verification commands depend on specific line counts

Task 5 Step 6 checks:
```
grep -c "delta_s" "$SPEC"  # expect 3 or more
```

If Phase 18 edits added `delta_s` references (unlikely but possible), this count would be off. The check should be more structural — verify specific headings exist/non-exist rather than counting reference density.

### 🟢 LOW: Git staging uses explicit paths (good)

The plan consistently uses `git add <explicit paths>`. No `git add -A` or `git add .`. This is correct and follows the project's git guidelines.

### 🟢 LOW: One-commit-per-task with verification checkpoints (good)

Each task has its own commit with verification steps. If a task fails, the prior tasks' work is safely committed. Recovery is straightforward.

---

## Summary of Required Plan Edits

| Priority | Task | Issue | Fix |
|----------|------|-------|-----|
| **P0** | Task 5 Edit 5 | FROM text mismatch (momentum sentence changed by Phase 18) | Update FROM block to match current 3-line text; update TO block to preserve Phase 18 wording |
| **P0** | Task 8 | Sub-conflict #1 already resolved by Phase 18 | Remove or repurpose Task 8 |
| **P0** | Task 4 Step 2 | v1.4-GAPS.md total_gaps is 21, not 11 | Read current frontmatter; calculate `21 + 3 = 24` |
| **P1** | Task 1 Steps 2-3, 5 | ROADMAP.md already has partial Phase 20.5 content | Add pre-condition checks; skip/adapt redundant steps |
| **P1** | Task 2 | REQUIREMENTS.md FROM blocks unverified post-Phase 20 | Re-verify all FROM text against current file |
| **P1** | Post-completion | FLAG-10 cross-ref verification now due | Promote to in-execution verification after Task 5 |
| **P2** | Task 0 (new) | No pre-flight check | Add pre-flight dry-run of all FROM text matches |
| **P2** | Plan header | Naming ambiguity with 20-05-PLAN.md | Add path disambiguation note |

---

## Recommendation

**Do not execute the plan as-is.** Apply the P0 fixes first (Tasks 5, 8, 4), then the P1 fixes (Tasks 1, 2, FLAG-10). The plan's core architecture — 8 tasks, evidence-gated spec edits, verification probe — remains sound. The issues are entirely staleness-driven, not design flaws.

The quickest path:
1. Edit `20-5-PLAN.md` to fix the P0 and P1 issues identified above (~30 min)
2. Re-run all FROM text verification as a pre-flight
3. Execute the corrected plan
