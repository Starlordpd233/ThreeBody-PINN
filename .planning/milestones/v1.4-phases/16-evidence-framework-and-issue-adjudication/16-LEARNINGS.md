---
phase: 16
phase_name: "Evidence Framework and Issue Adjudication"
project: "3-body-problem"
generated: "2026-06-09"
counts:
  decisions: 11
  lessons: 7
  patterns: 5
  surprises: 5
missing_artifacts: []
---

# Phase 16 Learnings: Evidence Framework and Issue Adjudication

## Decisions

### D-01: Canonical Issue-Ledger Path Locked to Full Phase Slug
The canonical ledger path is `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md`, replacing the stale draft path `.planning/milestones/v1.4-phases/16-evidence-framework/16-ISSUE-LEDGER.md` in ROADMAP.md, REQUIREMENTS.md, and PROJECT.md only.

**Rationale:** Stale paths could send future agents to a nonexistent or duplicate ledger; only three planning docs were authorized for the reconciliation, leaving STATE.md to workflow-state handling.
**Source:** 16-03-PLAN.md

---

### D-05: Evidence Packet File Layout
Evidence packets live one file per finding under `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/evidence/{finding-id}.md`.

**Rationale:** A predictable per-finding layout lets downstream agents (Phases 17-21) start packets by copying the template without guessing where they belong.
**Source:** 16-01-PLAN.md

---

### D-06: Fixed 12-Section Evidence Packet Schema
`_TEMPLATE.md` uses a fixed 12-section schema: Header, Source Positions, Spec Evidence, Code Evidence, First-Principles Physics Check, Verdict, Root-Cause Framework Ambiguity, Locked Convention, Which Source Was Correct / Wrong, Before / After Spec Note, Named Acceptance Check, Status Transition Log.

**Rationale:** Greppable headings make omission of required evidence sections visible and machine-checkable; mitigates tampering and repudiation threats.
**Source:** 16-01-PLAN.md

---

### D-13: AC-ID Naming Convention
Acceptance check IDs use the format `AC-{REQ-ID}[-{NN}]`; runnable pass criteria are deferred to Phase 21 scope.

**Rationale:** Reserves stable identifiers early without over-committing to executable semantics before the acceptance-check suite exists.
**Source:** 16-01-PLAN.md

---

### D-15: REQUIREMENTS.md Is the Sole Traceability Source
No `TRACEABILITY.md` artifact is created; the ledger carries only a verification statement ("30/30 v1.4 requirements mapped exactly once") and REQUIREMENTS.md remains the source of truth.

**Rationale:** Duplicating the traceability table risks drift between two sources of truth; a single verification statement in the ledger is sufficient.
**Source:** 16-02-PLAN.md, 16-03-PLAN.md

---

### D-17: Both Primary Sources Must Be Cited Side by Side
The template has no primary-source field; both Issue 01 sources (`ctl_pinn_resolution.md` and `01-architecture-and-physics-foundations.md`) must be cited side by side with line-range citations before any verdict selection.

**Rationale:** Prevents source-authority spoofing — neither Issue 01 source is authoritative, so the template must force the agent to read both before choosing a verdict.
**Source:** 16-01-PLAN.md

---

### D-18: Master Consolidation Report Is Supporting Evidence Only
`master_consolidation_report.md` is supporting evidence only, never a substitute for the two primary sources.

**Rationale:** A consolidation report could silently override the primary-source balance if treated as authoritative.
**Source:** 16-01-PLAN.md

---

### D-19: Strict Phase 16 Scope Boundary
Phase 16 deliverables are limited to the ledger, evidence README/template, narrow path reconciliation, and standard GSD artifacts — no spec edits, no live-code edits, no adjudication packets, no acceptance-check executable suite, no ledger linter.

**Rationale:** Containment; Phase 16 operationalizes the protocol before any spec or code edit begins, preventing premature adjudication.
**Source:** 16-01-PLAN.md, 16-03-PLAN.md

---

### Verdict and Status Enums Fixed at Five Values Each
Verdict enum: `accept-resolution`, `accept-issue-doc`, `accept-third-position`, `reject-both-as-unsupported`, `defer-with-blocker`. Status enum: `PENDING`, `IN_PROGRESS`, `FIX_APPLIED`, `VERIFIED`, `DEFERRED`.

**Rationale:** Fixed enums make verdict and lifecycle states greppable, machine-checkable, and prevent uncontrolled expansion of outcome categories.
**Source:** 16-01-PLAN.md

---

### B-02, B-04, B-09, M5 Pre-Flagged for EVID-05 Adjudication
These four findings are pre-flagged `YES - EVID-05 required` in the ledger without their verdicts being decided in Phase 16.

**Rationale:** These are the contested findings where the two primary Issue 01 sources disagree; they require root-cause ambiguity, locked convention, first-principles check, and source-correctness fields before any framework-spec edit.
**Source:** 16-01-PLAN.md, 16-02-PLAN.md

---

### FIX_APPLIED Is Not Closure; VERIFIED Requires Passing Check
`FIX_APPLIED` is explicitly not closure; transition to `VERIFIED` requires a passing named acceptance check. A batch regression rule requires re-running verified dependent acceptance checks after later edit batches.

**Rationale:** Prevents agents from recording a fix and considering the finding closed without actually verifying it; closes the repudiation threat.
**Source:** 16-01-PLAN.md, 16-02-PLAN.md

---

## Lessons

### Concurrent Plan Execution Requires Path-Limited Commits
Concurrent Plan 16-01 commits advanced HEAD while Plan 16-02 was executing. The ledger work had to be recommitted on the current head using path-limited commits, leaving unrelated staged files untouched.

**Context:** Two plans ran in parallel against the same phase directory; git HEAD moved between plan start and commit time.
**Source:** 16-02-SUMMARY.md

---

### Pre-Staged Unrelated Files Can Contaminate Task Commits
Initial Task 1 commit in Plan 16-01 picked up pre-staged unrelated files. Corrected by soft-resetting only that commit and recommitting with `git commit --only`.

**Context:** The working tree had pre-existing staged files unrelated to the plan's scope.
**Source:** 16-01-SUMMARY.md

---

### Finding Count Evolved After Initial Plan Wrote 20 Rows
Plan 16-02 seeded 20 finding rows, but post-prep verification showed 26 total, 24 in-scope, and 2 deferred. The Tier-1 prep expanded traceability beyond the original 20-row count.

**Context:** The verification report supersedes earlier Phase 16 wording that counted 20 rows.
**Source:** 16-VERIFICATION.md

---

### gsd-sdk Key-Link Checker Returns False Negatives on Escaped Regex
The `gsd-sdk query verify.key-links` tool reported false negatives because the plan regex strings were escaped. Direct `rg` checks correctly found the target links in the source files.

**Context:** Verification had to fall back from the SDK tool to raw `rg` for reliable results.
**Source:** 16-VERIFICATION.md

---

### STATE.md Stale Path Is Intentionally Out of Scope
`.planning/STATE.md` also contained the stale ledger path, but Phase 16 context authorized only ROADMAP, REQUIREMENTS, and PROJECT edits. STATE.md is treated as a non-blocking workflow-state note to be handled by workflow-state sync.

**Context:** This was a deliberate scope boundary — editing STATE.md directly could conflict with GSD state handlers.
**Source:** 16-03-PLAN.md, 16-VERIFICATION.md

---

### Pre-Existing Dirty Edits Prevent Standalone Path-Replacement Hunks
PROJECT.md and REQUIREMENTS.md had broader pre-existing v1.4 planning edits in the working tree. The path replacement could not be isolated as a standalone hunk without dropping the surrounding v1.4 planning context. The reconciliation commit included those planning-document updates as they stood after path correction.

**Context:** A workflow-safe staging adjustment deviation was recorded.
**Source:** 16-03-SUMMARY.md

---

### SEED_SHA Used as Intentional Seed Marker in Transition Logs
The plan explicitly required `SEED_SHA` as a placeholder for initial transition log entries instead of a real commit short SHA. Future status transitions must use real commit short SHAs.

**Context:** Recorded as a known stub in 16-02-SUMMARY.md.
**Source:** 16-02-SUMMARY.md

---

## Patterns

### Evidence-Packet Template with Fixed Greppable Schema
A fixed 12-section template with required HTML comments and greppable headings (`## Source Positions`, `## Verdict`, `## Status Transition Log`, etc.) enforces completeness. Required sections are marked with HTML comments stating they are `REQUIRED for EVID-05`.

**When to use:** When building a protocol for adjudicating contested findings between multiple authoritative sources, where omission of any evidence category must be visible and machine-checkable.
**Source:** 16-01-PLAN.md, 16-VERIFICATION.md

---

### Side-by-Side Dual-Source Citation Without Primary-Source Field
Requiring both primary sources to be cited side by side (with line-range citations) and omitting any "primary source" field prevents agents from pre-selecting an authority. The verdict can only be chosen after both sources are on the record.

**When to use:** When two source documents conflict and neither is pre-declared authoritative — forces the adjudicator to read both before choosing a verdict.
**Source:** 16-01-PLAN.md

---

### Ledger-As-Index With Separate Source-of-Truth Traceability
The issue ledger carries a verification statement (`30/30 v1.4 requirements mapped exactly once`) and points to REQUIREMENTS.md as the traceability source of truth, rather than duplicating the traceability table.

**When to use:** When a status ledger needs to demonstrate requirements coverage but a canonical traceability table already exists elsewhere — avoids drift between two tables.
**Source:** 16-02-PLAN.md, 16-03-PLAN.md

---

### Per-Finding Subsections With Seed Transition Logs and Shared AC-ID Annotations
Each finding in the ledger gets a per-finding H3 subsection containing an evidence-packet path reference, a seed transition log entry (with date, commit short SHA, status transition, and actor / plan reference), and annotations for shared acceptance checks (e.g., `AC-ARCH-01 also covers B-01 and B-10`).

**When to use:** When managing a ledger of 20+ findings where some findings share an acceptance check and every finding needs an auditable status-transition trail from the moment of seeding.
**Source:** 16-02-PLAN.md

---

### Narrow Path Reconciliation With Authorized-File-Only Scope
When a stale artifact path exists in multiple planning docs, restrict reconciliation to a pre-authorized file list (ROADMAP, REQUIREMENTS, PROJECT) and explicitly leave other files (STATE.md) to their own workflow handlers. Verify the stale path is absent from the authorized files after.

**When to use:** When renaming/moving a shared artifact mid-milestone and some docs have the old path — limits the reconciliation surface to avoid unintended edits.
**Source:** 16-03-PLAN.md

---

## Surprises

### Finding Count Changed After Initial Plan Was Written
The plan seeded 20 finding rows, but the verification report recorded 26 total, 24 in-scope, and 2 deferred — the Tier-1 prep had expanded traceability beyond the original count. The verification report explicitly supersedes the earlier wording.

**Impact:** The ledger had to accommodate additional findings after initial seeding; plan documents still reference "20" in places while the actual ledger and verification reference "26/24/2".
**Source:** 16-VERIFICATION.md, 16-02-PLAN.md

---

### SDK Key-Link Checker False Negatives Required Manual Verification Fallback
The `gsd-sdk query verify.key-links` tool returned false negatives on escaped regex patterns used by the plan. Direct `rg` checks were needed to verify the same links successfully.

**Impact:** Verification had to include a disconfirmation note explaining the SDK false negatives; trust in the SDK tool for regex-heavy link checks was reduced.
**Source:** 16-VERIFICATION.md

---

### User Passed Phase 16 UAT But Raised Milestone-Level Concern
The user confirmed Phase 16 with "yes. looks like phase 16 is good to go now" but simultaneously raised a concern outside Phase 16 scope: whether the v1.4 milestone (Phases 16-21) as a whole would actually resolve Issue 01. This concern was captured separately and routed to a milestone-level adversarial review pass.

**Impact:** Local phase satisfaction does not guarantee milestone-level confidence; an adversarial review pass was spawned to address the broader concern.
**Source:** 16-UAT.md

---

### STALE PATH Survived in STATE.md Despite Reconciliation in Other Docs
`.planning/STATE.md` still contained the stale ledger path after Phase 16 path reconciliation completed successfully in ROADMAP, REQUIREMENTS, and PROJECT. This was not a gap — it was an intentional scope boundary — but it means the stale path persists in the repo.

**Impact:** Downstream agents referencing STATE.md for the ledger path would be misrouted unless they use the canonical path from ROADMAP/REQUIREMENTS/PROJECT.
**Source:** 16-VERIFICATION.md, 16-03-PLAN.md

---

### Plan 16-03 Deviated From Plan Due to Pre-Existing Dirty Edits
Plan 16-03 had to include pre-existing v1.4 planning edits in PROJECT.md and REQUIREMENTS.md because the path replacement could not be isolated as a standalone hunk. This was recorded as a workflow-safe staging adjustment deviation.

**Impact:** The commit contained more changes than the plan strictly required, though no spec, code, acceptance-check, or STATE.md changes were introduced.
**Source:** 16-03-SUMMARY.md
