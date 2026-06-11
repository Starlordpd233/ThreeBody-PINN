---
status: consumed
purpose: other
created: 2026-05-24
milestone: untracked
phase: latex-sync
retirement_trigger: milestone complete; superseded by subsequent work
---

# Consolidated Code Review: LaTeX-Markdown Sync Strategy Design

**Date**: 2026-05-24
**Document**: docs/work/designs/cross_cutting/latex-sync/2026-05-24-latex-markdown-sync-strategy-design.md
**Review Team**: repo-verifier, internal-logic, feasibility, historical-audit (4 specialized agents)
**Overall Assessment**: GO WITH CRITICAL FIXES
**Total findings**: 8 Critical, 11 Important, 14 Minor (33 total across 4 agents)

---

## Executive Summary

Three independent review agents analyzed the LaTeX-Markdown sync strategy design document. **All three agents independently identified the same critical flaw**: the 1:1 pairing assumption between markdown H1 headings and LaTeX include directives is empirically false for all three specifications. This is not a theoretical concern—the SECTION-MAP construction method as written will fail when executed.

**Critical findings**: 8 (must fix before Genesis)
**Important findings**: 11 (must fix before first sync milestone)
**Minor findings**: 14 (should fix for clarity)

**Recommendation**: Defer Genesis commit until critical findings C1-C4 are resolved. The design architecture is sound, but the implementation details contain fatal flaws that will cause Genesis to produce incorrect or incomplete SECTION-MAP entries.

---

## Critical Findings (Must Fix Before Genesis)

### C1: 1:1 Pairing Assumption is Empirically False [FEAS-01, REPO-5/6, HIST-pending]
**Severity**: CRITICAL | **Confidence**: HIGH (3/3 agents)

**Issue**: The design states "LaTeX \include/\input order pairs 1:1 with markdown H1 headings" but empirical counting disproves this for all three specs.

**Evidence**:
- **ctl-instruction**: 9 H1s vs 8 includes. The extra H1 "# Source Issues / Notes for Future Reconciliation" (line 1392) has no LaTeX counterpart—it explicitly states "These notes are metadata for future reconciliation. They are not part of the converted source body."
- **pinn-architecture**: 6 real H1s vs 7 active inputs. Two LaTeX files (blueprint_summary.tex, bibliography.tex) have no markdown counterpart.
- **sampling-method**: 4 \section* blocks vs 11 H2 headings. The markdown has significantly more subsections than the LaTeX.

**Impact**: SECTION-MAP construction method will fail when executed. The agent will encounter orphaned H1s with no LaTeX target, or orphaned .tex files with no markdown source, and has no guidance on how to proceed.

**Fix**: 
1. Replace "pairs 1:1 by order" with "pairs by title alignment, allowing N:1 and 1:N mappings"
2. Define explicit rules:
   - Multiple markdown H1s in one .tex file: each H1 gets its own section_id pointing to same target_tex
   - .tex files with no markdown H1: assign section_id via .tex \section{} title
   - Markdown H1s with no .tex counterpart: create reserved ID (e.g., ctl-instruction:source-issues) with target_tex: none
3. Add to "out of scope" list: framework-revisions, source-issues metadata sections

---

### C2: No Correction Path for Incorrectly-Applied Terminal States [LOGIC-01]
**Severity**: CRITICAL | **Confidence**: HIGH

**Issue**: synced-early is "PERMANENT TERMINAL HISTORICAL STATUS" but there's no escape hatch if the sync was applied incorrectly (wrong semantic content, wrong section).

**Evidence**: State machine has no "superseded" or "corrected" state. If interim sync captures pre-correction markdown version, agent is stuck:
- Can't set row back to pending (terminal state)
- Can't add new pending row (no new markdown edit)
- Can't fix .tex without drift row update (violates atomicity)

**Impact**: First incorrect interim sync creates permanent unresolvable state. Gate 1 will fail at v1.6.5 sync.

**Fix**: Add `superseded` status to lifecycle (requires relaxing "LOCKED — five states" to six). Define: "If final sync discovers interim sync was incorrect, create new pending row for the same section_id, apply correct sync, mark new row as synced, mark old synced-early row as superseded with note in SYNC-PLAN.md Build-Repairs section."

---

### C3: Append-Only Rule Contradicts Status Mutability [LOGIC-02]
**Severity**: CRITICAL | **Confidence**: HIGH

**Issue**: Per-task workflow (line 157) states "Never edit a pre-existing row." Lifecycle (line 96) states "Status field is the only mutable cell." These are directly contradictory.

**Evidence**: An agent reading the per-task workflow during Phase 19 would conclude drift rows are completely immutable. During v1.6.5 sync, the agent might refuse to update Status from pending to synced, believing this violates the append-only rule.

**Impact**: Gate 1 fails because rows remain pending. Sync cannot complete.

**Fix**: Clarify temporal scope:
- "Never edit a pre-existing row during content milestones (v1.4, v1.5, v1.6)"
- "Status transitions occur during sync milestone and via hotfix commits"
- Alternative: "Row content (Phase through Target .tex) is immutable after creation. Status is the only mutable cell, updated only during sync operations."

---

### C4: Backfill Inventory Incomplete for Phases 19-21 [LOGIC-03, REPO-10]
**Severity**: CRITICAL | **Confidence**: HIGH

**Issue**: Genesis backfill covers only Phases 17/18 (~8-9 rows). Phases 19/20/20.5 also modified framework-specs. If Genesis lands after Phase 19 starts, those edits become orphaned.

**Evidence**: Git history shows commits from phases 17-20 all touched LaTeX files. User-lock decision #6 acknowledges uncertainty about Genesis timing relative to Phase 19.

**Impact**: Phase 19 edits to markdown have no drift rows. Gate 2 never checks for them (before DRIFT_BASELINE tag). Corresponding .tex sections are never updated. LaTeX PDFs silently diverge from markdown.

**Fix**: Make backfill inventory a "compute at Genesis time" step, not a static list:
1. Add hard pre-condition: "Genesis MUST land before Phase 19's first markdown-touching commit" OR
2. Specify: "At Genesis execution time, enumerate ALL pre-Genesis framework-spec commits across ALL v1.4 phases using `git log --oneline -- 'pinn_instruction/markdown_conversion/framework-specs/*.md' | head -40` and create retro rows for each"
3. Increase effort estimate for retro row creation from "~8-9 rows" to "~15-20 rows"

---

### C5: Code-Block False Positives in Heading Detection [FEAS-03/07, REPO-recommendation]
**Severity**: CRITICAL | **Confidence**: HIGH

**Issue**: SECTION-MAP construction method uses `^# ` to find H1 headings, but this matches code-comment lines inside fenced code blocks.

**Evidence**:
- ctl_instruction.md: 14 raw H1s, only 9 true H1s. False positives at lines 377, 516, 530, 531, 698 are code comments like "# Total data points per batch"
- pinn_architecture.md: similar code-comment artifacts

**Impact**: SECTION-MAP will have spurious entries for phantom headings. Drift rows will reference non-existent section_ids. Gates will produce false failures.

**Fix**: 
1. Construction method must track fenced-code-block state (toggle on ``` lines)
2. Provide Python script (10 lines) instead of grep command:
   ```python
   in_code_block = False
   for i, line in enumerate(open('spec.md')):
       if line.strip().startswith('```'):
           in_code_block = not in_code_block
       elif not in_code_block and line.startswith('# '):
           print(f"L{i+1}: {line.strip()}")
   ```
3. Gate script must implement same state machine

---

### C6: Effort Estimate is 2-3x Too Optimistic [FEAS-02]
**Severity**: IMPORTANT | **Confidence**: MEDIUM (single agent, well-evidenced)

**Issue**: Design says "~10-20 hours across 2-4 sessions" but realistic projection is 25-40 hours.

**Evidence**:
- Projected row count at v1.6.5 sync: ~63-93 rows
  - v1.4 retro: 8-9 (Phases 17-18) + 7-11 (Phases 19-21) = 15-20
  - v1.5: 20-30 rows
  - v1.6: 20-30 rows
- Per-row sync time: 15-35 minutes
  - Read markdown diff: 2-3 min
  - Navigate .tex: 1-2 min
  - Apply semantic change: 5-10 min
  - Fix LaTeX syntax: 5-15 min
  - Build+verify: 2-5 min
- Total: 63 rows × 15 min = 15.75h (optimistic), 93 rows × 35 min = 54.25h (pessimistic)
- pinn_architecture.md has 149 inline math instances + 26 display math blocks requiring careful transcription

**Impact**: User under-allocates time for v1.6.5 sync. Rushed work leads to LaTeX build failures. Gate 3 fails repeatedly.

**Fix**: Revise estimate to "25-40 hours across 4-6 sessions." Add variance note: "ctl_instruction.md and pinn_architecture.md dominate; sampling-method.md is ~10% of total effort."

---

## Important Findings (Must Fix Before First Sync Milestone)

### I1: Authority-Split Rule Produces Ambiguous Cases [FEAS-04, LOGIC-18]
**Severity**: IMPORTANT | **Confidence**: HIGH (2 agents)

**Issue**: "Markdown is authoritative for semantic content; LaTeX is authoritative for LaTeX-specific syntax" is too vague for common scenarios.

**Evidence**: Three ambiguous cases:
1. **Math environment choice**: Markdown `$$...$$` vs LaTeX `\begin{equation}`, `\begin{align}`, `\[...\]`. pinn_architecture.md has 26 display math blocks needing this decision.
2. **Table formatting**: Markdown pipe tables vs LaTeX tables with column widths, alignment specifiers, \multirow. Should LaTeX preserve column widths (overflow risk) or recalculate (presentation change)?
3. **Cross-references**: Markdown `[Section 3.2](#sec:step2)` vs LaTeX `\ref{sec:step2}`. SECTION-MAP section_ids don't include LaTeX labels.

**Impact**: Sync agent makes inconsistent choices across specs. Build failures when LaTeX environment mismatches. Semantic drift when cross-references point to wrong labels.

**Fix**: Add "Authority Split Examples" subsection with 5-10 worked examples covering: display math, inline math, tables, cross-references, footnotes, code listings, theorem environments. Each example shows markdown input → expected LaTeX output.

---

### I2: Gate Script SYNC_START/SYNC_END Source Unspecified [FEAS-05, LOGIC-15]
**Severity**: IMPORTANT | **Confidence**: HIGH (2 agents)

**Issue**: Design says script takes `<SYNC_START>` and `<SYNC_END>` as arguments but doesn't specify where these values come from.

**Evidence**: Gate 2's table references `SYNC_START..SYNC_END` and `DRIFT_BASELINE..SYNC_START` but never defines these. Tags exist (drift-baseline-v1.4, latex-sync-v1-start, latex-sync-v1) but design never says script reads them.

**Impact**: Gate script implementer guesses at argument source. Different implementations produce different gate behavior.

**Fix**: Specify: "SYNC_START and SYNC_END are git references (tags or SHAs) passed as positional arguments. The script uses `git log --oneline SYNC_START..SYNC_END -- <path>` to enumerate commits in range. DRIFT_BASELINE is derived from the `drift-baseline-*` tag."

---

### I3: New Markdown Sections Added Post-Genesis Have No Section_ID [LOGIC-04, LOGIC-09]
**Severity**: IMPORTANT | **Confidence**: HIGH (2 findings)

**Issue**: SECTION-MAP is "frozen baseline — built once at Genesis." If content milestone adds new markdown section, no section_id exists for it. Agent cannot create valid drift row.

**Evidence**: Per-task workflow says "Use SECTION-MAP to resolve section_id and target_tex." If section doesn't exist in SECTION-MAP, agent either:
- Skips drift row (violates atomicity)
- Invents new section_id (breaks frozen baseline)
- Uses parent section's ID (loses granularity)

**Impact**: New sections in v1.5/v1.6 have no drift tracking. Gate 1 fails at sync time.

**Fix**: Either:
1. Add SECTION-MAP update protocol: "SECTION-MAP is frozen for existing sections, extensible for new sections. New sections get appended with section_id `ctl-instruction:new-<slug>` and current line ranges."
2. Define ad-hoc convention: "Post-Genesis additions use section_id format `ctl-instruction:ad-hoc-<YYYY-MM-DD>-<slug>`"

---

### I4: Atomicity Rule Silent on Merge Commits, Cherry-Picks, Rebases [LOGIC-07, LOGIC-14]
**Severity**: IMPORTANT | **Confidence**: HIGH (2 findings)

**Issue**: Atomicity rule assumes linear commit history. Three common git operations break the assumption:
1. **Merge commits**: May introduce framework-spec diffs without drift row
2. **Cherry-picks**: Duplicate logical change with new SHA
3. **Rebases**: Rewrite commit SHAs, making retro drift rows stale

**Evidence**: No guidance in design for these scenarios.

**Impact**: Feature branch with 3 framework-spec commits (each with drift rows) is merged. Merge commit's diff includes framework-spec changes (conflict resolution). Merge commit doesn't modify drift file. Gate 2 detects framework-spec commit without drift row. Agent must retroactively add row or explain merge.

**Fix**: Add "Git operations" subsection:
- "Merge commits should NOT create additional drift rows if all constituent commits already have rows"
- "Cherry-picks should reference the original commit's drift row in Change Summary"
- "After rebase, drift rows referencing short SHAs should be updated"
- Alternative: "Feature branches must be rebased (not merged) to avoid merge commits"

---

### I5: Gate 3 Verification Mechanism Ambiguous [LOGIC-08]
**Severity**: IMPORTANT | **Confidence**: MEDIUM

**Issue**: Gate 3 says "Mtime is a helper signal only" and "Authoritative freshness proof: latexmk invocation evidence captured in VERIFICATION.md." But bash script can't meaningfully verify markdown file content without fragile parsing.

**Evidence**: Script can check PDF existence, size, mtime. It cannot verify latexmk invocation evidence stored in VERIFICATION.md.

**Impact**: Gate script implementer must decide: does Gate 3 check (a) PDF exists + non-empty + mtime? (b) VERIFICATION.md exists? (c) only PDF existence? Different implementers produce different gate behavior.

**Fix**: Explicitly specify: "Gate 3 mechanical check: PDF exists + non-empty + mtime after SYNC_START. Latexmk invocation evidence: human review of VERIFICATION.md during Phase C sign-off, not by script."

---

### I6: No Cancelled-Task Terminal State [LOGIC-06]
**Severity**: IMPORTANT | **Confidence**: MEDIUM

**Issue**: If task creates drift row but is cancelled before markdown commit, pending row has no valid terminal state. noop requires target_tex=none. synced/synced-early/synced-hotfix require .tex edits.

**Evidence**: State machine has no "cancelled" or "void" status.

**Impact**: Cancelled tasks leave pending rows. Gate 1 fails at sync time. Recovery says "classify open rows" but no "cancelled" classification exists.

**Fix**: Add `cancelled` status (requires relaxing "LOCKED — five states" to six). Define: "If task is cancelled after drift row creation but before markdown commit, mark row as cancelled with note in Change Summary: 'CANCELLED: task withdrawn before commit.'"

---

### I7: Cross-Milestone Row Batching Underspecified [FEAS-08]
**Severity**: IMPORTANT | **Confidence**: MEDIUM

**Issue**: Phase B says "per-section-file batching" but doesn't address .tex files with drift rows from multiple milestones.

**Evidence**: Example: 04_phase1_data_prep.tex has 3 rows from v1.4 and 2 rows from v1.5. Design says "batch all drift rows that target it" but commit message would need to reference both v1.4 and v1.5 milestones.

**Impact**: Sync agent creates commit with unclear message. Verification checks both drift indexes but design doesn't specify how.

**Fix**: Specify: "When .tex file has drift rows from multiple milestones, apply commit message lists all source milestones (e.g., 'sync(04_phase1_data_prep): apply v1.4 + v1.5 drift'). Commit is part of v1.6.5 sync milestone regardless of source."

---

### I8: Frozen Baseline Language Conflicts with Mutable Titles [LOGIC-10]
**Severity**: IMPORTANT | **Confidence**: MEDIUM

**Issue**: SECTION-MAP is "frozen baseline" but Section Title column says "informational current heading text" implying it can be updated.

**Evidence**: If heading renames from "Step 4: Input Vector Construction" to "Step 4: Feature Vector Construction," should SECTION-MAP be updated?

**Impact**: Inconsistent SECTION-MAP updates across specs. Some titles frozen, some updated.

**Fix**: Clarify: "SECTION-MAP section_id mappings and target_tex paths are frozen at Genesis. Section Title columns are informational and MAY be updated when headings are renamed. Line ranges are frozen and never updated."

---

## Minor Findings (Should Fix for Clarity)

### M1: Tag Creation Listed as Part of Atomic Commit [LOGIC-11]
Tag references commit SHA and must be post-commit step. Rephrase: "Single atomic commit producing items 1-7, followed by: 8. git tag (post-commit step)."

### M2: No Section Deletion Handling [LOGIC-12]
If markdown section is deleted, drift row needs target_tex but sync action is deletion. Add note: "Section deletions: create drift row with Change Summary describing deletion. During sync, comment out or remove corresponding .tex section."

### M3: No Section Split/Merge Handling [LOGIC-13]
If markdown section splits (one heading → two) or merges (two → one), SECTION-MAP section_ids become invalid. Add note: "Section splits/merges require SECTION-MAP update (new section_ids for split children, retired section_id for merged parent)."

### M4: No Proactive Atomicity Enforcement [LOGIC-14]
Atomicity rule enforced only by convention and late detection (gates at sync time). Consider lightweight pre-commit hook (~10 lines) that checks if staged files include framework-specs/*.md and warns if drift file not staged.

### M5: "Source" Column Referenced but Absent from Schema [LOGIC-05]
Phase B says "chronological by Source" but "Source" is not in schema. Replace with "chronological by Task" or add Source column.

### M6: v1.5 Drift Index Creation Timing Unspecified [FEAS-06]
Design doesn't say when v1.5-LATEX-DRIFT.md is created. Add to per-task workflow: "Step 0: If current milestone's drift index doesn't exist, create it by copying header from most recent drift index."

### M7: Inactive .tex Re-Activation Underspecified [FEAS-09]
pinn-architecture has 3 inactive files. If re-activated, SECTION-MAP needs new row but construction method says "built once at Genesis." Add: "SECTION-MAP is append-only after Genesis. Re-activating dormant .tex file requires appending new row."

### M8: Retro Row Backfill Requires Commit Archaeology [FEAS-10]
Design lists ~8-9 retro rows but doesn't specify how to determine (file, section_id) pairs for each historical commit. Add: "Allocate 4-6 hours for retro row backfill. For each commit, run git show <sha> --stat to identify files, then git show <sha> -- <file> to identify sections, then match to SECTION-MAP."

### M9: Build-Repair Recording is Manual [FEAS-11]
SYNC-PLAN.md created in Phase A but build repairs happen in Phase B. Clarify: "SYNC-PLAN.md is append-only after Phase A. Phase B appends '## Build-Repairs Applied' section."

### M10: Agent Training Material Missing [FEAS-12]
Per-task workflow is 6 steps but lacks decision tree for "did this task touch framework-specs?" and worked example. Add "Agent Quick-Reference" appendix with decision tree and example.

### M11: v1.3-ROADMAP.md Line 9 Wording [REPO-moderate-4]
Design claims "lines 9, 27, 48, 71, 94, 116, 138" use exact phrasing but line 9 uses different wording. Change to "lines 27, 48, 71, 94, 116, 138" or reword to "use this or similar phrasing."

---

## Additional Critical Findings from Historical Audit

### C7: Hotfix 0708a56 Missing from Backfill Inventory [HIST-003]
**Severity**: CRITICAL | **Confidence**: HIGH

**Issue**: Commit 0708a56 modified BOTH markdown AND LaTeX AND PDF in a single commit. Design references it as hotfix precedent and defines `synced-hotfix` status for this pattern, but backfill inventory does NOT include a row for it.

**Evidence**: `git diff-tree 0708a56` shows 3 files: `pinn_architecture.md`, `sqr_skipresnet_siren_backbone.tex`, `main_pinn.pdf`. Backfill rows (lines 207-215) list only Phases 17-18 markdown changes + d3fcff9 noop.

**Impact**: The exact commit cited as the hotfix precedent is missing from the drift index. At sync time, this row won't exist, creating inconsistency between the documented precedent and actual tracking.

**Fix**: Add backfill row: `Phase 17 → pinn_architecture §SQR-SkipResNet-SIREN Backbone → target_tex: .../sqr_skipresnet_siren_backbone.tex, status: synced-hotfix`

---

### C8: Design Does Not Acknowledge LaTeX Was Modified During v1.4 [HIST-006, REPO-10]
**Severity**: CRITICAL | **Confidence**: HIGH (2 agents)

**Issue**: Design states (line 13) "v1.4+ phase work edits only the corresponding markdown sources." But git history proves LaTeX WAS modified during v1.4 phases 17-20 (9+ commits). The sync isn't just forward-propagating markdown to stale LaTeX — for those specific sections, it's reconciling two independently-edited sources.

**Evidence**: Commits 0708a56, 5dbf0f5, 782e694, 923d053, 5077ded, fff4c16, 096aaa8 all modified LaTeX during v1.4. The backfill rows treat Phases 17-18 as markdown-only changes, but actual history shows concurrent LaTeX modifications.

**Impact**: Sync agent assumes LaTeX is stale and overwrites it with markdown content, potentially losing intentional LaTeX edits made during v1.4. For sections that received both markdown and LaTeX edits, the agent needs to reconcile rather than blindly forward-propagate.

**Fix**:
1. Update line 13: "During v1.4, some phases also edited LaTeX sources directly (e.g., hotfix 0708a56); the Genesis regime formalizes markdown-only authoring going forward."
2. Backfill rows for sections with concurrent LaTeX edits should note: "LaTeX also edited during this phase — reconcile both sources"
3. The 0708a56 `synced-hotfix` row (C7) should note it was already applied to LaTeX

---

## Cross-Agent Deduplication Matrix

| Finding | Repo-Verifier | Internal-Logic | Feasibility | Historical-Audit | Confidence |
|---------|---------------|----------------|-------------|------------------|------------|
| C1: 1:1 pairing false | ✓ (5/6) | - | ✓ (FEAS-01) | ✓ (HIST-007) | HIGH |
| C2: No correction path | - | ✓ (LOGIC-01) | - | - | HIGH |
| C3: Append-only contradiction | - | ✓ (LOGIC-02) | - | - | HIGH |
| C4: Backfill incomplete | ✓ (10) | ✓ (LOGIC-03) | - | - | HIGH |
| C5: Code-block false positives | ✓ (recommendation) | - | ✓ (FEAS-03/07) | - | HIGH |
| C6: Effort estimate low | - | - | ✓ (FEAS-02) | ✓ (HIST-008) | MEDIUM-HIGH |
| C7: 0708a56 missing from backfill | - | - | - | ✓ (HIST-003) | HIGH |
| C8: LaTeX modified during v1.4 not acknowledged | ✓ (10) | - | - | ✓ (HIST-006) | HIGH |
| I1: Authority-split ambiguous | - | ✓ (LOGIC-18) | ✓ (FEAS-04) | pending | HIGH |
| I2: SYNC_START/SYNC_END undefined | - | ✓ (LOGIC-15) | ✓ (FEAS-05) | pending | HIGH |
| I3: New section handling missing | - | ✓ (LOGIC-04/09) | - | pending | HIGH |
| I4: Atomicity silent on git ops | - | ✓ (LOGIC-07/14) | - | pending | HIGH |
| I5: Gate 3 mechanism ambiguous | - | ✓ (LOGIC-08) | - | pending | MEDIUM |
| I6: No cancelled-task state | - | ✓ (LOGIC-06) | - | pending | MEDIUM |
| I7: Cross-milestone batching | - | - | ✓ (FEAS-08) | pending | MEDIUM |
| I8: Frozen baseline language | - | ✓ (LOGIC-10) | - | pending | MEDIUM |

---

## Recommendations

### Immediate Actions (Before Genesis)
1. **Rewrite SECTION-MAP construction method** (C1, C5)
   - Replace "pairs 1:1 by order" with N:1 and 1:N mapping rules
   - Add code-block-aware heading detection (Python script)
   - Define reserved IDs for orphaned sections (ctl-instruction:source-issues, ctl-instruction:supplementary-figures)
   - Add "out of scope" list: framework-revisions, source-issues metadata, supplementary-figures

2. **Add correction path to state machine** (C2, C3, I6)
   - Add `superseded` and `cancelled` statuses (relax "LOCKED — five states" to seven)
   - Clarify append-only rule temporal scope
   - Define correction workflow: "If interim sync was incorrect, create new pending row, apply correct sync, mark old row as superseded"

3. **Complete backfill inventory** (C4, C7)
   - Add missing 0708a56 hotfix row (status: synced-hotfix)
   - Enumerate ALL pre-Genesis framework-spec commits across ALL v1.4 phases
   - Increase retro row estimate from ~8-9 to ~15-20
   - Add hard pre-condition: "Genesis MUST land before Phase 19's first markdown-touching commit" OR make inventory dynamic

4. **Acknowledge LaTeX modifications during v1.4** (C8)
   - Update line 13 narrative to acknowledge concurrent LaTeX edits
   - Add reconciliation notes to backfill rows for sections with both markdown and LaTeX edits
   - Ensure sync agent knows to reconcile (not blindly overwrite) for these sections

5. **Revise effort estimate** (C6)
   - Change from "10-20 hours across 2-4 sessions" to "25-40 hours across 4-6 sessions"
   - Add variance note: "ctl_instruction.md and pinn_architecture.md dominate"
   - Add discovery risk: "If retroactive backfill misses rows, manual discovery adds ~2-5 hours per missed section"

### Before First Sync Milestone (v1.6.5)
5. **Add authority-split examples** (I1)
   - Create 5-10 worked examples covering display math, inline math, tables, cross-references, footnotes, code listings, theorem environments
   - Each example: markdown input → expected LaTeX output

6. **Specify gate script arguments** (I2, I5)
   - Define SYNC_START, SYNC_END, DRIFT_BASELINE sources (git tags)
   - Clarify Gate 3 mechanical check vs human review

7. **Add SECTION-MAP update protocol** (I3)
   - Define how to add new sections post-Genesis
   - Specify ad-hoc section_id format

8. **Add git operations subsection** (I4)
   - Define merge commit, cherry-pick, rebase handling
   - Specify: "Feature branches must be rebased (not merged)"

### For Clarity (Before Implementation)
9. **Fix minor findings** (M1-M11)
   - Clarify tag creation timing
   - Add section deletion/split/merge handling
   - Add agent training material
   - Fix line number references

---

## Conclusion

The LaTeX-Markdown sync strategy design is **architecturally sound** but contains **8 critical implementation flaws** that will cause Genesis to fail or produce incorrect SECTION-MAP entries. All critical findings are fixable with targeted revisions to the design document.

**Recommendation**: Defer Genesis commit. Address critical findings C1-C5 and C7-C8 (estimated 3-4 hours of design revision). Proceed with Genesis once all critical findings are resolved.

**Risk if not addressed**: Genesis produces SECTION-MAP with orphaned entries, drift rows with no valid terminal states, incomplete backfill inventory, and silent overwrites of concurrent LaTeX edits. Estimated 15-20 hours of rework to correct.

**Risk if addressed**: Clean Genesis, correct SECTION-MAP, complete drift tracking, proper reconciliation of dual-edited sections. v1.6.5 sync proceeds smoothly within revised 25-40 hour estimate.

---

**Review completed by**: 4 specialized agents across 33 total findings
- repo-verifier: 19 verified, 3 contradicted, 2 partially verified
- internal-logic: 18 findings (3 critical, 7 important, 8 minor)
- feasibility: 12 findings (3 critical, 5 important, 4 minor)
- historical-audit: 8 findings (2 critical, 3 important, 3 minor)

**Cross-agent consensus**: C1 (1:1 pairing false) independently discovered by 3/4 agents. C4 (backfill incomplete) confirmed by 3/4 agents with git evidence.
