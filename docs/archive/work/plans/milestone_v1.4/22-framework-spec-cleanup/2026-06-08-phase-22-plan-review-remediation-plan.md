---
title: "docs: Remediate Phase 22 planning artifacts from plan audits"
type: docs
status: archived
archived_at: 2026-06-09
date: 2026-06-08
purpose: implementation-plan
created: 2026-06-08
milestone: v1.4
phase: 22-framework-spec-cleanup
execution: knowledge-work
execution_status: first-pass-complete
executed_at: 2026-06-09T10:23:17+0800
review_status: reviewed
retirement_trigger: "Phase 22 planning artifacts are revised, review findings are closed out, and reference audit passes"
retirement_trigger_met: 2026-06-09
closeout_evidence: docs/work/reviews/milestone_v1.4/22-framework-spec-cleanup/review_of_plans/2026-06-09-phase22-review-closeout-matrix.md
---

# docs: Remediate Phase 22 planning artifacts from plan audits

## Summary

Revise the Phase 22 planning artifacts so the five-plan cleanup pipeline can execute without missing baseline evidence, ambiguous autonomous STOP behavior, fragile verification gates, shared-state races, or stale ROADMAP/validation metadata.

The work is planning-only. It edits `.planning/` Phase 22 artifacts and does not touch framework specs, detector code, generated execution outputs, or review report lifecycle state beyond recording this remediation plan as the consumer of the reports.

---

## Problem Frame

Two adversarial review reports found that the Phase 22 plan set is directionally sound but not ready for execution. The current artifacts already resolve the author-comment scope dispute and use an all-forms census basis, but they still leave several execution-critical details underspecified: no pre-WS-A baseline tag exists, the pre-census is deferred until after WS-A edits, STOP-halted conversions are not operationally defined for autonomous plans, verify blocks rely on brittle output parsing, and the ROADMAP still says Phase 22 has zero plans.

Because Phase 22 is part of v1.4, remediation must preserve the STOP protocol. Where a proposed edit would define a new process-artifact schema or make a semantic judgment not grounded in current artifacts, the implementer must surface the decision instead of inventing it.

---

## Review Findings Verified

| Finding source | Verification result | Plan handling |
|---|---|---|
| `2026-06-08-phase22-adversarial-plan-audit.md` C-01 and `phase-22-adversarial-audit-report.md` Finding 1 | Confirmed. `git tag -l "v1.4*"` has no `v1.4-pre-phase-22`; 22-04/22-05 need a defined pre-WS-A baseline. | U1 |
| C-01/H-01 | Confirmed. 22-04 currently creates `22-COMMENT-CENSUS-PRE.md` in Wave 2 by reconstructing a before-state; Wave 0 can capture it before WS-A edits. | U1 |
| H-02 | Confirmed. 22-02 and 22-03 tell autonomous tasks to surface and halt a conversion, but do not define the file state, record shape, or completion semantics. | U3 |
| H-03 and M-07 | Confirmed. Verify blocks should not depend on grep-like output filters or silently pass when a detector exits non-zero for STOP-halted findings. | U2, U3 |
| H-04 | Confirmed. 22-03 still permits autonomous removal of "strictly representation-preserving" duplicate fallbacks; redundant-fallback deletion can be semantic and must not happen without user grounding. | U3 |
| H-05 and earlier Finding 7 | Confirmed. 22-02/22-03 lack explicit commit cadence and non-destructive rollback procedure for high-risk spec edits. | U4 |
| Earlier Finding 2 | Not adopted as stated. Re-counting the current all-forms marker set gives 26 author-marker lines, matching `22-RESEARCH.md`; the older 22-count claim used a narrower search. | U1, U2 keep execution-time re-derivation and avoid hardcoded closure on a stale count |
| Earlier Finding 3 and M-02 | Partly confirmed. The detector contract names modes and report expectations, but census text hashes belong in the detector/census contract because 22-04 later requires them. | U2 |
| Earlier Finding 4 | Confirmed in substance. G3 remains too semantic unless 22-05 defines a mechanical evidence protocol and routes unclassified deltas through STOP. | U6 |
| Earlier Finding 5 | Confirmed in part. 22-02/22-03 edit different specs but both reference shared ledger transitions; the plan should keep the wave parallel by removing shared ledger writes from Wave 1. | U4 |
| Earlier Finding 6 and M-01 | Confirmed as dependency risk, not as an auto-task bug. 22-01 is a blocking-human plan and footnote review is human-gated, but 22-03 should not wait on a footnote policy it does not need. | U5 |
| Earlier Finding 8 | Confirmed as planning risk. D3 needs false-positive/suppression language and a clear single-letter-subscript boundary. | U2 |
| Earlier Finding 9 | Confirmed. The sanity gate currently tests inline math only; it should also test block math because `ctl_instruction.md` has block-math leakage. | U2 |
| Earlier Finding 10 | Confirmed. 22-02 needs per-construct evidence/checkpoints for lossy Pandoc-to-GFM conversions. | U5 |
| M-03 | Accepted as inherent limitation. No new conversion rule is invented; STOP/user resolution remains the safety mechanism. | U3 |
| M-04, M-05, M-06, L-01 through L-06 | Confirmed or cheap to harden. Add `.gitignore` verification, reuse existing ledger format, update ROADMAP and validation metadata, remove padding incentives, and fix artifact ownership text. | U2, U6, U7 |

---

## Requirements

- R1. Wave 0 must create or record a durable pre-WS-A baseline ref and pre-WS-A author-comment census before any WS-A spec edits execute.
- R2. The detector planning contract must state stable command assumptions, sanity gates, census hash fields, exit-code semantics, false-positive handling, and fixture-maintenance expectations without inventing ungrounded process schemas.
- R3. Autonomous STOP-halt behavior must be explicit: leave the affected source region unchanged, record the finding, update required gap registers when the STOP protocol applies, and keep the affected plan blocked unless the user resolves or defers it.
- R4. WS-A repair plans must avoid shared mutable writes during parallel Wave 1 execution and must include commit cadence plus recovery instructions that comply with the repo's destructive-operation policy.
- R5. G3 and VER-05 verification must use grounded, auditable evidence: baseline refs, per-comment hashes, allowed-delta categories, existing ledger status fields, and STOP routing for unclassified deltas.
- R6. ROADMAP, validation metadata, artifact ownership lists, and plan status text must reflect the actual five-plan Phase 22 pipeline.
- R7. Review report closeout remains finding-by-finding work after the amendments land; the review reports stay active until a separate closeout proves every material finding is addressed, superseded, or not applicable.

---

## Scope Boundaries

In scope:
- Edit `.planning/phases/22-framework-spec-cleanup/22-01-PLAN.md` through `22-05-PLAN.md`.
- Edit `.planning/phases/22-framework-spec-cleanup/22-CONTEXT.md`, `22-RESEARCH.md`, `22-VALIDATION.md`, and, only if a new STOP gap is discovered during amendment, `22-GAPS.md` plus `.planning/milestones/v1.4-GAPS.md`.
- Edit `.planning/ROADMAP.md` Phase 22 plan count/list and status.

Out of scope:
- Implement `tools/spec-render-check/`.
- Run Phase 22 execution plans or edit framework specs.
- Create Phase 22 generated outputs such as `22-COMMENT-CENSUS-PRE.md`, `22-COMMENT-HANDOFF.md`, or `22-RENDER-REVIEW.md`.
- Delete or archive review reports. Their lifecycle decision is "keep active until remediation execution and closeout review complete."

---

## Key Technical Decisions

- KTD1. Wave 0 owns baseline evidence: move the pre-WS-A ref and `22-COMMENT-CENSUS-PRE.md` responsibility into 22-01 so downstream plans consume evidence instead of reconstructing it.
- KTD2. Keep Wave 1 parallel by removing shared writes: 22-02 and 22-03 should write only their target spec and per-plan execution summaries; 22-05 remains the sole `16-ISSUE-LEDGER.md` writer.
- KTD3. Reuse existing schemas before adding new ones: census hashes reuse the `COMMENT_HASH <stable-comment-id> <text_hash>` shape already required by 22-04; VER-05 uses the existing Phase 16 ledger table and transition-log fields. If an implementer thinks a new process-artifact schema is required, they must STOP and surface it.
- KTD4. No autonomous semantic deletion: redundant fallback candidates in `ctl_instruction.md` are recorded for human/STOP disposition, not removed by 22-03's auto task.
- KTD5. Rollback must follow repo governance: prefer small commits and region-level restoration from recorded pre-images. Full-file restore, `git checkout --`, or equivalent destructive rollback requires explicit user confirmation.

---

## Implementation Units

### U1. Move Baseline And Pre-Census Ownership To Wave 0

**Goal:** Make the baseline and pre-census evidence available before WS-A edits begin.

**Requirements:** R1, R5, R6

**Dependencies:** None

**Files:**
- `.planning/phases/22-framework-spec-cleanup/22-01-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-04-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-05-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-CONTEXT.md`
- `.planning/phases/22-framework-spec-cleanup/22-VALIDATION.md`

**Approach:**
- Add `22-COMMENT-CENSUS-PRE.md` and the pre-WS-A baseline ref to the 22-01 produced-artifacts list and Wave 0 task flow.
- In 22-01, specify that execution records the baseline ref using the existing tag pattern `v1.4-pre-phase-22` or a named pre-WS-A commit recorded in the plan summary before any WS-A edits. Do not create the tag during this remediation plan.
- Move pre-census creation out of 22-04. 22-04 should consume the already committed `22-COMMENT-CENSUS-PRE.md`, create only `22-COMMENT-CENSUS-POST.md` and `22-COMMENT-HANDOFF.md`, and STOP if the pre-census artifact is missing.
- Update 22-05 to use the recorded baseline ref and the committed PRE/POST census artifacts for G3 instead of vague "WS-A base" prose.
- Keep the census count as re-derived execution evidence. Do not replace the current all-forms 26-marker baseline with the older 22-count finding.

**Patterns to follow:**
- `.planning/phases/22-framework-spec-cleanup/22-RESEARCH.md` WS-B census basis and `COMMENT_HASH` preservation requirements.
- `.planning/phases/22-framework-spec-cleanup/22-CONTEXT.md` D-04 through D-06.

**Test scenarios:**
- Search `22-04-PLAN.md` after the edit and confirm it no longer instructs the executor to reconstruct PRE from a missing tag or unstated WS-A base.
- Confirm `22-01-PLAN.md` names `22-COMMENT-CENSUS-PRE.md` as a committed Wave 0 output and says it must exist before 22-02/22-03 begin.
- Confirm `22-05-PLAN.md` consumes the recorded baseline ref and PRE/POST census docs for G3.

**Verification:** A reader can trace baseline creation from 22-01 to 22-04 to 22-05 without using git archaeology or guessing which commit is the before-state.

### U2. Harden The Detector Contract In Planning Text

**Goal:** Make the detector expectations precise enough that downstream plans can verify behavior without fragile report scraping.

**Requirements:** R2, R5

**Dependencies:** U1

**Files:**
- `.planning/phases/22-framework-spec-cleanup/22-01-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-RESEARCH.md`
- `.planning/phases/22-framework-spec-cleanup/22-VALIDATION.md`

**Approach:**
- Add a repo-root CWD note for all `node tools/spec-render-check/detect.mjs ...` commands.
- Remove `min_lines: 200` from the detector artifact contract and replace it with behavioral acceptance criteria.
- Extend the sanity gate text so it renders and asserts both inline math and block math.
- Add census output requirements grounded in 22-04: each census record carries `form`, `file`, `section/anchor`, `matched-snippet`, `verbatim-text`, and `text_hash = SHA-256(verbatim-text)`, with machine-readable `COMMENT_HASH` lines where PRE/POST comparison needs them.
- Add exit-code conventions at the planning level: successful zero-finding runs exit 0; detector/tool failures use distinct non-zero exits; rendering findings are non-zero and cannot be masked as success. If STOP-halted findings remain, the owning plan is blocked or explicitly user-deferred, not "green with exceptions."
- Harden D3 planning text: exclude Markdown emphasis contexts, keep code spans/fences excluded, document false-positive suppression as a STOP/user-reviewed path, and state that single-letter subscripts are not D3 definitive findings by themselves.
- Add `.gitignore` verification after scoped `npm install`: `git check-ignore -v tools/spec-render-check/node_modules/` must identify the ignore rule or the plan must add one.
- Add regression fixture maintenance text: if detector layers change, update fixtures and re-run `--selftest`; `sampling_method.md` must remain the zero-finding negative control.
- Do not introduce a new JSON or ledger schema unless it is copied from an existing artifact. If implementation needs a new process-artifact schema, STOP and surface it as a process-artifact schema gap before editing.

**Patterns to follow:**
- Existing 22-01 CLI mode list.
- Existing 22-04 `COMMENT_HASH` verification command.
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` status lifecycle.

**Test scenarios:**
- Confirm 22-01 no longer contains `min_lines: 200`.
- Confirm 22-01's sanity gate names inline and block math.
- Confirm census text in 22-01 includes `text_hash` and `COMMENT_HASH` expectations that match 22-04.
- Confirm 22-VALIDATION does not treat a STOP-halted detector finding as a passing zero-finding run.

**Verification:** The detector contract is clear enough for 22-02 through 22-05 to rely on exit status, documented records, and existing hash lines instead of output grep patterns.

### U3. Define STOP-Halt Semantics And Remove Autonomous Fallback Deletion

**Goal:** Make autonomous STOP behavior executable while preventing semantic deletion.

**Requirements:** R3, R4, R5

**Dependencies:** U2

**Files:**
- `.planning/phases/22-framework-spec-cleanup/22-02-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-03-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-VALIDATION.md`
- `.planning/phases/22-framework-spec-cleanup/22-GAPS.md` only if the amendment reveals a new unresolved gap
- `.planning/milestones/v1.4-GAPS.md` only if `22-GAPS.md` is updated

**Approach:**
- Add an "Autonomous STOP-halt procedure" paragraph to 22-02 and 22-03 task text:
  - Leave the affected source region unchanged.
  - Record the section/anchor, original text, proposed conversion/removal, consulted sources, and why the agent cannot proceed.
  - Continue only independent conversions that do not depend on the halted decision.
  - If the finding is semantic, process-schema, cross-phase, or otherwise governed by the STOP protocol, append a formal gap entry to `22-GAPS.md` and update `.planning/milestones/v1.4-GAPS.md`.
  - The affected task/plan is not done until the user resolves or explicitly defers the halted item.
- Rewrite 22-03 Task 2 so redundant plaintext/backtick fallback candidates are surfaced for human/STOP disposition and are not deleted by the auto task. Hard-break removal can remain automatic only where the plan already has mechanical evidence that the backslash is conversion noise; otherwise it follows the same checkpoint path.
- Update verify/acceptance text so "zero residual findings" means exit 0, while non-zero findings tied to unresolved STOP items mean blocked, not passed.

**Patterns to follow:**
- AGENTS.md STOP protocol required fields.
- Existing `22-GAPS.md` and `.planning/milestones/v1.4-GAPS.md` format.

**Test scenarios:**
- Search 22-03 after the edit and confirm no auto task tells the executor to remove redundant fallbacks autonomously.
- Confirm both WS-A plans state that STOP-halted regions stay unchanged and block completion unless resolved or deferred.
- Confirm any new gap entry, if required, has all STOP-protocol fields and is indexed milestone-wide.

**Verification:** An autonomous executor can tell exactly what to do when a conversion is ambiguous, and no Phase 22 plan authorizes ungrounded semantic deletion.

### U4. Remove Shared-State Races And Add Commit/Rollback Cadence

**Goal:** Keep WS-A parallel where safe while preventing shared ledger conflicts and unrecoverable edits.

**Requirements:** R4, R5

**Dependencies:** U3

**Files:**
- `.planning/phases/22-framework-spec-cleanup/22-02-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-03-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-05-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-VALIDATION.md`

**Approach:**
- Remove instructions for 22-02 and 22-03 to append directly to `16-ISSUE-LEDGER.md` during parallel Wave 1 execution.
- Have 22-02 and 22-03 record per-plan summaries with detector outputs, converted region IDs, STOP items, and commit SHAs. 22-05 then reconciles the shared ledger once, after Wave 1 and Wave 2 artifacts are stable.
- Add commit cadence to 22-02 and 22-03: commit after each structural construct conversion or tightly scoped math batch that leaves the detector in a known state. Use `scripts/agent-commit`, not raw `git commit`.
- Add recovery instructions that avoid destructive commands by default: restore a bad region from recorded pre-image/diff with a targeted edit, then re-run the detector. If full-file restore or `git checkout -- <file>` appears necessary, STOP and request explicit user confirmation before running it.
- Add `git diff --check`, detector re-run, and changed-file inspection before each task-boundary commit.

**Patterns to follow:**
- `docs/git-guidelines.md` commit and hook protocol.
- AGENTS.md destructive-operation awareness.

**Test scenarios:**
- Confirm 22-02 and 22-03 no longer list `16-ISSUE-LEDGER.md` as a file they mutate during Wave 1.
- Confirm 22-05 remains the sole plan responsible for final ledger reconciliation.
- Confirm both WS-A plans name `scripts/agent-commit` and require user confirmation before destructive full-file rollback.

**Verification:** Running 22-02 and 22-03 in parallel cannot create a ledger merge race, and a failed conversion has a documented non-destructive recovery path.

### U5. Split The Footnote Dependency And Add Per-Construct Checkpoints

**Goal:** Remove unnecessary blocking from 22-03 and make lossy structural conversions auditable.

**Requirements:** R2, R4, R5

**Dependencies:** U2, U4

**Files:**
- `.planning/phases/22-framework-spec-cleanup/22-01-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-02-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-03-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-VALIDATION.md`

**Approach:**
- Split 22-01 Task 3 into two readiness signals in the plan text:
  - Detector/regression/selftest readiness, which unblocks non-footnote WS-A work.
  - Cursor footnote policy readiness, which blocks only footnote classification/repair and any final `--all` closure that depends on footnote policy.
- Update 22-03 so it depends on detector/regression readiness, not on the human footnote policy.
- Keep 22-02 tied to the footnote policy only for `pinn_architecture.md` footnote repair/classification.
- Add per-construct checkpoints to 22-02 Task 1 for Pandoc tables/divs/captions: original block hash, row/cell association evidence, converted block hash, detector result, and commit SHA after each successful construct or construct group.
- If a GFM table conversion cannot preserve row/cell association mechanically, STOP-surface the mapping and leave the region unchanged.

**Patterns to follow:**
- 22-02 existing section-anchor approach for locating table/div/caption regions.
- 22-VALIDATION manual-only footnote verification language.

**Test scenarios:**
- Confirm 22-03 does not require `22-STAGE0-FOOTNOTE-PROBE.md` before starting non-footnote repairs.
- Confirm 22-02 retains the footnote policy dependency for `pinn_architecture.md`.
- Confirm 22-02 Task 1 requires per-construct evidence before marking a table/div/caption conversion complete.

**Verification:** `ctl_instruction.md` repairs can proceed after the detector is ready, while `pinn_architecture.md` footnote handling stays correctly human-gated.

### U6. Mechanize G3 And Reuse The Existing VER-05 Ledger Format

**Goal:** Turn final verification from semantic prose into auditable evidence without inventing new closure rules.

**Requirements:** R5

**Dependencies:** U1, U3, U4, U5

**Files:**
- `.planning/phases/22-framework-spec-cleanup/22-05-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-VALIDATION.md`
- `.planning/phases/22-framework-spec-cleanup/22-RESEARCH.md`

**Approach:**
- Replace broad "every changed line differs only..." language with an audit protocol:
  - Compute WS-A diffs against the recorded pre-WS-A baseline.
  - Classify each changed hunk into allowed categories: math delimiter/brace normalization, whitespace needed for block rendering, GFM table syntax preserving cell content, fenced-div/caption wrapper removal preserving content, literal-dollar escaping, or D-05 wrapper-only author-comment repair preserving comment text.
  - Require evidence per hunk: before/after snippet, allowed category, detector output, and link to the plan/commit that made the change.
  - Any hunk outside allowed categories is a G3 failure or STOP item until user-resolved.
- Use PRE/POST `COMMENT_HASH` comparison for author-comment preservation, with D-05 wrapper repairs allowed only when verbatim comment text hash remains stable.
- Reuse the existing Phase 16 ledger columns and per-finding transition-log format. Do not define new VER-05 fields unless a STOP-surfaced process-schema decision resolves them.

**Patterns to follow:**
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` status table and transition log.
- Current 22-04 census hash verification command.

**Test scenarios:**
- Confirm 22-05 lists allowed G3 delta categories and says unclassified deltas fail or STOP.
- Confirm 22-05 does not allow a text-hash mismatch for author comments except a wrapper-only change with stable verbatim text.
- Confirm 22-VALIDATION references the existing ledger lifecycle rather than a new ungrounded ledger schema.

**Verification:** A reviewer can audit G3 from committed evidence and existing ledger mechanics, without trusting a freeform semantic assertion.

### U7. Update ROADMAP, Validation Metadata, And Artifact Ownership Text

**Goal:** Align project-level planning metadata with the actual Phase 22 plan set.

**Requirements:** R6, R7

**Dependencies:** U1 through U6

**Files:**
- `.planning/ROADMAP.md`
- `.planning/phases/22-framework-spec-cleanup/22-VALIDATION.md`
- `.planning/phases/22-framework-spec-cleanup/22-04-PLAN.md`
- `docs/work/reviews/milestone_v1.4/22-framework-spec-cleanup/review_of_plans/2026-06-08-phase22-adversarial-plan-audit.md` read-only
- `docs/work/reviews/milestone_v1.4/22-framework-spec-cleanup/review_of_plans/phase-22-adversarial-audit-report.md` read-only

**Approach:**
- Update `.planning/ROADMAP.md` Phase 22 row from `0/TBD | Not planned` to the correct five-plan planned state. Do not mark Phase 22 complete.
- Replace the Phase 22 `Plans:` TBD item with the five existing plan files and wave labels.
- Update `22-VALIDATION.md` frontmatter from draft to active after the amendment pass, while leaving execution fields such as `wave_0_complete` false.
- Replace placeholder task IDs in `22-VALIDATION.md` with plan-aware references where possible, or explicitly say they are execution-derived and not hardcoded.
- Fix 22-04 artifact ownership text after U1 so PRE is a consumed Wave 0 artifact and POST/HANDOFF are produced in Wave 2.
- Leave both review reports in `active` lifecycle state until a later closeout report classifies each finding as addressed, superseded, not applicable, or open.

**Patterns to follow:**
- `docs/README.md` lifecycle rules for plans and reviews.
- Existing ROADMAP table style.

**Test scenarios:**
- Confirm `.planning/ROADMAP.md` lists `22-01-PLAN.md` through `22-05-PLAN.md` and no longer says `0 plans`.
- Confirm `22-VALIDATION.md` no longer has `status: draft` after all amendments land.
- Confirm no review report is deleted, archived, or marked consumed before finding-by-finding closeout.

**Verification:** Project metadata accurately tells the next executor that Phase 22 has a five-plan pipeline ready for amended execution, not an unplanned placeholder.

---

## Execution Notes

Use a plan-edit-first posture. Apply amendments to planning artifacts, run markdown/link sanity checks, then commit the remediation as an atomic planning/docs commit because it touches `.planning/` and Phase 22 governance artifacts.

Before committing, run `git status --short --branch`, inspect staged and unstaged diffs for touched files, run `git diff --check`, and use `scripts/agent-commit` per repo protocol.

---

## Verification Plan

- Run `git diff --check` after the amendments.
- Run `rg -n "0/TBD|0 plans|TBD \\(run /gsd-plan-phase 22|v1\\.4-pre-phase-22 tag or the WS-A base commit|min_lines: 200|remove a duplicate plaintext/backtick fallback in this auto task" .planning/ROADMAP.md .planning/phases/22-framework-spec-cleanup` and confirm every hit is either gone or intentionally retained with new context.
- Run `rg -n "22-COMMENT-CENSUS-PRE|COMMENT_HASH|text_hash|Stage-0 footnote|scripts/agent-commit|STOP" .planning/phases/22-framework-spec-cleanup` and confirm the expected amended plan paths are covered.
- Run a read-only review closeout matrix against the two review reports and mark findings as addressed/superseded/not applicable/open in a follow-up review-closeout artifact before proposing report retirement.

---

## Sources

- `docs/work/reviews/milestone_v1.4/22-framework-spec-cleanup/review_of_plans/2026-06-08-phase22-adversarial-plan-audit.md`
- `docs/work/reviews/milestone_v1.4/22-framework-spec-cleanup/review_of_plans/phase-22-adversarial-audit-report.md`
- `.planning/phases/22-framework-spec-cleanup/22-01-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-02-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-03-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-04-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-05-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-CONTEXT.md`
- `.planning/phases/22-framework-spec-cleanup/22-RESEARCH.md`
- `.planning/phases/22-framework-spec-cleanup/22-VALIDATION.md`
- `.planning/phases/22-framework-spec-cleanup/22-GAPS.md`
- `.planning/milestones/v1.4-GAPS.md`
- `.planning/ROADMAP.md`
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md`
- `docs/README.md`
