# Delete v1.3 Closure Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Retire the stale `docs/findings/reports_on_v1.3/closure_audit_2026-05-11/` reports after verifying their findings were resolved, and remove live references so no broken links or stale manifest entries remain.

**Architecture:** Treat this as a risk-elevated documentation cleanup with one atomic commit. Delete the tracked closure-audit reports, remove the ignored `.DS_Store` that would otherwise keep the parent `reports_on_v1.3/` directory around, and update only live references that would become stale. The historical v1.3 closure audit plan and its cross-AI review are also retired in this commit; their findings were verified as fully addressed before deletion.

**Tech Stack:** Markdown documentation, Python validation script, Git, ripgrep, shell filesystem checks.

---

## Pre-Execution Requirements

- Current working directory: `<home>/Desktop/3_body_problem`
- Expected branch: `milestone/v1.4`
- This task touches risk-elevated paths: `pinn_instruction/`, `.planning/`, and `docs/findings/`.
- Before any mutation, surface:

```bash
git status --short --branch
git branch --show-current
git worktree list
git stash list
```

- Stop before mutating if the branch is not `milestone/v1.4`, if the working tree is dirty for unrelated files, or if a new non-historical reference to `closure_audit_2026-05-11` appears outside the files listed below.

## Audit Findings To Preserve

The closure audit originally had future-attention findings, but later commits addressed the actionable items:

| Finding | Resolution evidence |
|---|---|
| CTL corrupted softening sentence | `ac6bbd0 fix(ctl_instruction): repair corrupted softening sentence (line 655)` |
| Stage strategy deleted authcomment | `0234385 fix(audit): resolve CRITICAL C-1 by restoring deleted authcomment` |
| Stage strategy I3 schema note missing from Source Issues | `0ee9652 docs(stage_strat_revision): add SI-SSR-001 documenting I3 schema gap` |
| Stage strategy heading/cross-reference cleanup | `0844b3a fix(stage_strat_revision): add Part I-IV labels to H1s and update TOC anchors`; `57de4e4 fix(stage_strat_revision): replace unresolvable Section 1.2 cross-reference` |
| PINN architecture deleted authcomments | `d91825f fix(pinn_architecture): restore 4 authcomments to converted body (D-58)` |
| PINN architecture stale author-comment note | `14ec962 fix(pinn_architecture): update SI-PINN-002 to reflect bold bracket format` |
| PINN architecture weight-init inconsistency | `8d5c9ed docs(pinn_architecture): label Formula A/B and quantify ~235x divergence in SI-PINN-001`; `0708a56 fix(pinn-arch): correct SIREN hidden-layer weight init formula in LaTeX Table 1` |
| PINN architecture missing author/date metadata | `a1dee9b fix(pinn_architecture): add YAML frontmatter with author/date metadata` |

## File Map

### Delete

- `docs/findings/reports_on_v1.3/closure_audit_2026-05-11/DELETION-DECISIONS-2026-05-11.md`
- `docs/findings/reports_on_v1.3/closure_audit_2026-05-11/MASTER-AUDIT-2026-05-11.md`
- `docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-ctl_instruction.md`
- `docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-data_quality_assessment.md`
- `docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-pinn_architecture.md`
- `docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-review_of_framework.md`
- `docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-sampling_method.md`
- `docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-stage_strat_revision.md`
- `docs/findings/reports_on_v1.3/.DS_Store` if present; it is ignored by `.gitignore` and is the only sibling that would keep `reports_on_v1.3/` on disk.

### Modify

- `docs/superpowers/plans/2026-05-19-delete-v13-closure-audit.md` — this implementation plan; include it in the final cleanup commit.
- `pinn_instruction/markdown_conversion/README.md` — remove links to the deleted audit files and replace them with static verification status.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — remove dead audit-file path from Source Issues metadata note.
- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md` — remove dead audit-file path from Source Issues metadata note.
- `tests/test_phase12_validation.py` — remove stale skip-message path references to `audit-pinn_architecture.md`.
- `.planning/milestones/v1.3-MILESTONE-AUDIT.md` — update one historical note so it does not point readers to a retired folder.
- `.planning/tmp/docs-work-manifest.json` — remove four already-stale `reports_on_v1.3` review-queue entries.

### Leave Unchanged

None — all v1.3 closure audit artifacts, including the original implementation plan and its cross-AI review, are retired in this cleanup.

## Task 1: Reconfirm Git State And Reference Scope

**Files:**
- Read: repository Git metadata
- Read: all files that may reference `closure_audit_2026-05-11`

- [ ] **Step 1: Surface current Git state**

Run:

```bash
git status --short --branch
git branch --show-current
git worktree list
git stash list
```

Expected:

```text
## milestone/v1.4...origin/milestone/v1.4 [ahead 1]
milestone/v1.4
```

The worktree list should show `<home>/Desktop/3_body_problem` on `milestone/v1.4`. Existing stashes are allowed; do not alter them.

- [ ] **Step 2: Verify the tracked deletion manifest**

Run:

```bash
git ls-files docs/findings/reports_on_v1.3/closure_audit_2026-05-11
```

Expected: exactly these 8 tracked files:

```text
docs/findings/reports_on_v1.3/closure_audit_2026-05-11/DELETION-DECISIONS-2026-05-11.md
docs/findings/reports_on_v1.3/closure_audit_2026-05-11/MASTER-AUDIT-2026-05-11.md
docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-ctl_instruction.md
docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-data_quality_assessment.md
docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-pinn_architecture.md
docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-review_of_framework.md
docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-sampling_method.md
docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-stage_strat_revision.md
```

- [ ] **Step 3: Verify live references before edits**

Run:

```bash
rg --hidden -n "closure_audit_2026-05-11" \
  -g '!.git' \
  -g '!docs/findings/reports_on_v1.3/closure_audit_2026-05-11/**' \
  -g '!docs/superpowers/plans/**' \
  -g '!docs/superpowers/reviews/**' \
  -g '!.planning/tmp/**'
```

Expected live hits before edits:

```text
pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md:310:...
pinn_instruction/markdown_conversion/README.md:7:...
pinn_instruction/markdown_conversion/README.md:8:...
pinn_instruction/markdown_conversion/README.md:10:...
pinn_instruction/markdown_conversion/README.md:12:...
pinn_instruction/markdown_conversion/README.md:13:...
pinn_instruction/markdown_conversion/README.md:14:...
pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1212:...
.planning/milestones/v1.3-MILESTONE-AUDIT.md:27:...
tests/test_phase12_validation.py:21:...
tests/test_phase12_validation.py:60:...
tests/test_phase12_validation.py:89:...
tests/test_phase12_validation.py:105:...
tests/test_phase12_validation.py:127:...
tests/test_phase12_validation.py:142:...
```

Stop if any additional non-historical live file appears.

## Task 2: Update Live Markdown References

**Files:**
- Modify: `pinn_instruction/markdown_conversion/README.md`
- Modify: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
- Modify: `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md`
- Modify: `.planning/milestones/v1.3-MILESTONE-AUDIT.md`

- [ ] **Step 1: Replace the conversion index table**

In `pinn_instruction/markdown_conversion/README.md`, replace the current table with this content:

```markdown
# Markdown Conversion Index

This index tracks authoritative markdown conversions for the v1.3 verification milestone. The 2026-05-11 closure reports were retired after their remaining findings were fixed or carried forward in the converted markdown.

| Source | Authoritative markdown | Verification status | Candidate archive |
|---|---|---|---|
| CTL instruction | [`framework-specs/ctl_instruction.md`](framework-specs/ctl_instruction.md) | Verified in v1.3; reconciliation notes retained inline | N/A -- single candidate |
| Data Quality Assessment | [`framework-revisions/data_quality_assessment.md`](framework-revisions/data_quality_assessment.md) | Verified in v1.3; reconciliation notes retained inline | N/A -- single candidate |
| PINN Architecture | [`framework-specs/pinn_architecture.md`](framework-specs/pinn_architecture.md) | Verified in v1.3; follow-up fixes applied to author comments, metadata, and SIREN initialization | N/A -- single candidate |
| Review of Framework | [`framework-revisions/review-of-framework/review_of_framework.md`](framework-revisions/review-of-framework/review_of_framework.md) | Verified in v1.3; accepted markdown-only equation-numbering limitations remain | N/A -- single candidate |
| Stage Strategy Revision | [`framework-revisions/stage-strat-revision/stage_strat_revision.md`](framework-revisions/stage-strat-revision/stage_strat_revision.md) | Verified in v1.3; I3 schema inconsistency retained as a source issue | N/A -- single candidate |
| Sampling Method | [`framework-specs/sampling_method.md`](framework-specs/sampling_method.md) | Verified in v1.3; accepted markdown-only authcomment color loss remains | N/A -- single candidate |
```

Use `apply_patch` for this edit.

- [ ] **Step 2: Reword CTL Source Issues provenance**

In `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`, replace:

```markdown
These notes are metadata for future reconciliation. They are not part of the converted source body and are excluded from fidelity comparison in `docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-ctl_instruction.md`.
```

with:

```markdown
These notes are metadata for future reconciliation. They are not part of the converted source body and were excluded from v1.3 fidelity comparisons.
```

- [ ] **Step 3: Reword DQA Source Issues provenance**

In `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md`, replace:

```markdown
These notes are metadata for future reconciliation. They are not part of the converted source body and are excluded from fidelity comparison in `docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-data_quality_assessment.md`.
```

with:

```markdown
These notes are metadata for future reconciliation. They are not part of the converted source body and were excluded from v1.3 fidelity comparisons.
```

- [ ] **Step 4: Reword v1.3 milestone audit historical note**

In `.planning/milestones/v1.3-MILESTONE-AUDIT.md`, replace the `phase: 14` `detail` line:

```yaml
    detail: "No 14-VERIFICATION.md exists. Phase 14 has only a verification_report.md in markdown_conversion/verification_reports/ (superseded by closure_audit_2026-05-11; 3 of 6 reports deleted 2026-05-12), not a standardized per-phase VERIFICATION.md."
```

with:

```yaml
    detail: "No 14-VERIFICATION.md exists. Phase 14 originally had only a verification_report.md in markdown_conversion/verification_reports/; that report trail was superseded during v1.3 closure work and later retired after follow-up fixes, not converted into a standardized per-phase VERIFICATION.md."
```

## Task 3: Update Test Skip Text

**Files:**
- Modify: `tests/test_phase12_validation.py`

- [ ] **Step 1: Replace stale report-path comment**

In `tests/test_phase12_validation.py`, replace:

```python
# REPORT_MD was pinn_instruction/markdown_conversion/verification_reports/pinn_architecture_verification_report.md
# Superseded by v1.3 closure audit (2026-05-11); report deleted per DELETION-DECISIONS-2026-05-11.
# See: docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-pinn_architecture.md
```

with:

```python
# REPORT_MD was pinn_instruction/markdown_conversion/verification_reports/pinn_architecture_verification_report.md.
# The report artifact was retired after v1.3 closure; report-only checks remain skipped.
```

- [ ] **Step 2: Replace skipped report messages**

In `tests/test_phase12_validation.py`, replace each of these strings:

```python
"  SKIP: CLEAN-03 — verification report deleted; superseded by closure_audit_2026-05-11/audit-pinn_architecture.md"
"  SKIP: CAND-01 — verification report deleted; superseded by closure_audit_2026-05-11/audit-pinn_architecture.md"
"  SKIP: AUDIT-01 — verification report deleted; superseded by closure_audit_2026-05-11/audit-pinn_architecture.md"
"  SKIP: AUDIT-02 — verification report deleted; superseded by closure_audit_2026-05-11/audit-pinn_architecture.md"
"  SKIP: AUDIT-03 — verification report deleted; superseded by closure_audit_2026-05-11/audit-pinn_architecture.md"
```

with:

```python
"  SKIP: CLEAN-03 — verification report artifact retired after v1.3 closure"
"  SKIP: CAND-01 — verification report artifact retired after v1.3 closure"
"  SKIP: AUDIT-01 — verification report artifact retired after v1.3 closure"
"  SKIP: AUDIT-02 — verification report artifact retired after v1.3 closure"
"  SKIP: AUDIT-03 — verification report artifact retired after v1.3 closure"
```

## Task 4: Remove Stale Temporary Manifest Entries

**Files:**
- Modify: `.planning/tmp/docs-work-manifest.json`

- [ ] **Step 1: Remove four stale review queue entries**

In `.planning/tmp/docs-work-manifest.json`, remove exactly these four objects from `review_queue`:

```json
{"path": "docs/findings/reports_on_v1.3/pinn_architecture_verification_report_2.md", "type": "hand-written", "status": "pending_review"},
{"path": "docs/findings/reports_on_v1.3/pinn_architecture_verification_report.md", "type": "hand-written", "status": "pending_review"},
{"path": "docs/findings/reports_on_v1.3/stage_strat_revision.md", "type": "hand-written", "status": "pending_review"},
{"path": "docs/findings/reports_on_v1.3/verification_final_report.md", "type": "hand-written", "status": "pending_review"},
```

Do not modify any other `review_queue` entries.

- [ ] **Step 2: Validate JSON syntax**

Run:

```bash
python3 -m json.tool .planning/tmp/docs-work-manifest.json >/tmp/docs-work-manifest.json.check
```

Expected: exit code `0`.

## Task 5: Delete The Closure Audit Folder And Parent Leftovers

**Files:**
- Delete: 8 tracked markdown files under `docs/findings/reports_on_v1.3/closure_audit_2026-05-11/`
- Delete if present: ignored `docs/findings/reports_on_v1.3/.DS_Store`

- [ ] **Step 1: Delete tracked closure audit files with `apply_patch`**

Use `apply_patch` delete hunks for all 8 tracked files listed in the File Map. Do not use `git rm` because the repository governance treats deletion as risk-elevated and this plan should keep the file list explicit.

- [ ] **Step 2: Remove the now-empty closure directory**

Run:

```bash
rmdir docs/findings/reports_on_v1.3/closure_audit_2026-05-11
```

Expected: exit code `0`.

- [ ] **Step 3: Remove ignored `.DS_Store` parent leftover if present**

Run:

```bash
test ! -e docs/findings/reports_on_v1.3/.DS_Store || rm docs/findings/reports_on_v1.3/.DS_Store
```

Expected: exit code `0`.

- [ ] **Step 4: Remove the now-empty `reports_on_v1.3` directory**

Run:

```bash
rmdir docs/findings/reports_on_v1.3
```

Expected: exit code `0`. If this fails, run `find docs/findings/reports_on_v1.3 -maxdepth 2 -print` and stop to review the unexpected leftover before continuing.

## Task 6: Verify No Live Stale References Remain

**Files:**
- Read: repository

- [ ] **Step 1: Verify target folder and parent are gone**

Run:

```bash
test ! -e docs/findings/reports_on_v1.3
```

Expected: exit code `0`.

- [ ] **Step 2: Verify no non-historical slug references remain**

Run:

```bash
rg --hidden -n "closure_audit_2026-05-11" \
  -g '!.git' \
  -g '!docs/superpowers/plans/**' \
  -g '!docs/superpowers/reviews/**'
```

Expected: no hits outside historical superpowers plan/review files. If hits appear in `pinn_instruction/`, `.planning/milestones/`, `.planning/tmp/`, `tests/`, or active docs, stop and clean them before committing.

- [ ] **Step 3: Verify no active `reports_on_v1.3` references remain**

Run:

```bash
rg --hidden -n "docs/findings/reports_on_v1\\.3|reports_on_v1\\.3" \
  -g '!.git' \
  -g '!docs/superpowers/plans/**' \
  -g '!docs/superpowers/reviews/**'
```

Expected: no hits in active docs, `pinn_instruction/`, tests, or `.planning/tmp`. Historical superpowers plan/review hits are allowed only when the command is run without the two exclusion globs.

- [ ] **Step 4: Verify no deleted files remain tracked**

Run:

```bash
git ls-files docs/findings/reports_on_v1.3
```

Expected: no output.

- [ ] **Step 5: Review scoped diff**

Run:

```bash
git diff --stat
git diff --name-status
```

Expected paths:

```text
M	.planning/milestones/v1.3-MILESTONE-AUDIT.md
M	.planning/tmp/docs-work-manifest.json
D	docs/findings/reports_on_v1.3/closure_audit_2026-05-11/DELETION-DECISIONS-2026-05-11.md
D	docs/findings/reports_on_v1.3/closure_audit_2026-05-11/MASTER-AUDIT-2026-05-11.md
D	docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-ctl_instruction.md
D	docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-data_quality_assessment.md
D	docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-pinn_architecture.md
D	docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-review_of_framework.md
D	docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-sampling_method.md
D	docs/findings/reports_on_v1.3/closure_audit_2026-05-11/audit-stage_strat_revision.md
A	docs/superpowers/plans/2026-05-19-delete-v13-closure-audit.md
M	pinn_instruction/markdown_conversion/README.md
M	pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md
M	pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
M	tests/test_phase12_validation.py
```

No other paths should appear.

## Task 7: Run Focused Validation

**Files:**
- Test: `tests/test_phase12_validation.py`

- [ ] **Step 1: Run JSON validation**

Run:

```bash
python3 -m json.tool .planning/tmp/docs-work-manifest.json >/tmp/docs-work-manifest.json.check
```

Expected: exit code `0`.

- [ ] **Step 2: Run the repository's local validation script**

Run:

```bash
python3 tests/test_phase12_validation.py
```

Expected: script runs without Python import errors. Report-only checks print `SKIP` messages that no longer mention `closure_audit_2026-05-11`.

- [ ] **Step 3: Do not run `pytest` unless the environment has it**

Check:

```bash
python3 -m pytest tests/test_phase12_validation.py
```

Expected in the current environment: `No module named pytest`. This is acceptable because the file is an executable script and `pytest` is not installed.

## Task 8: Commit The Cleanup

**Files:**
- Stage: all modified and deleted paths from Task 6 Step 5

- [ ] **Step 1: Stage exact paths**

Run:

```bash
git add \
  .planning/milestones/v1.3-MILESTONE-AUDIT.md \
  .planning/tmp/docs-work-manifest.json \
  docs/findings/reports_on_v1.3/closure_audit_2026-05-11 \
  docs/superpowers/plans/2026-05-19-delete-v13-closure-audit.md \
  pinn_instruction/markdown_conversion/README.md \
  pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md \
  pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md \
  tests/test_phase12_validation.py
```

Expected: exit code `0`.

- [ ] **Step 2: Confirm staged diff is exact**

Run:

```bash
git diff --cached --name-status
```

Expected: same path list as Task 6 Step 5, with no extra files.

- [ ] **Step 3: Commit**

Run:

```bash
git commit -m "docs: retire stale v1.3 closure audit reports" -m "Delete the 2026-05-11 closure audit folder after follow-up fixes resolved or carried forward its remaining findings. Update live markdown conversion references, test skip text, and the docs work manifest so the retired reports_on_v1.3 path is not left behind."
```

Expected: commit succeeds with one focused documentation-cleanup commit.

## Task 9: Post-Commit Verification

**Files:**
- Read: Git metadata

- [ ] **Step 1: Confirm clean status**

Run:

```bash
git status --short --branch
```

Expected:

```text
## milestone/v1.4...origin/milestone/v1.4 [ahead 2]
```

No modified, deleted, or untracked files should appear.

- [ ] **Step 2: Confirm latest commit scope**

Run:

```bash
git log -1 --stat --oneline
```

Expected: latest commit is `docs: retire stale v1.3 closure audit reports` and includes the 8 audit file deletions, the 6 reference/manifest updates, and this implementation plan.

- [ ] **Step 3: Confirm ignored parent leftover is gone**

Run:

```bash
git status --short --ignored docs/findings/reports_on_v1.3
```

Expected: no output.

## Self-Review

- **Spec coverage:** The plan deletes the closure folder, cleans live references, removes the ignored parent leftover, updates the stale temporary manifest entries found during the second audit, validates syntax/tests, and commits atomically.
- **Placeholder scan:** No unspecified implementation steps remain.
- **Type/path consistency:** All referenced paths match the current repository paths found by `rg`, `find`, and `git ls-files`.
- **Scope control:** Historical superpowers plan/review files are intentionally excluded from edits. They are provenance documents, not live references.
