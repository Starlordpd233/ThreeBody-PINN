---
title: Issue-Fix Agent Team Design — ARCHIVE_MASTER Plan Patching
date: 2026-05-02
status: approved (design phase complete; awaiting implementation plan)
target_artifact: ~/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md
source_findings: docs/findings/critique_of_consolidating_archived_issue/3_synthesis_report.md
author: brainstorming session, 2026-05-02
---

# Issue-Fix Agent Team — Design

## 1. Problem Context

The synthesis report (`docs/findings/critique_of_consolidating_archived_issue/3_synthesis_report.md`)
identifies 15 distinct findings against the upstream plan
`~/.claude/plans/consolidate-all-archived-files-elegant-umbrella.md`. The plan, as written, will fail
its own SHA-256 round-trip verification on all 7 archive files (finding C-1).

The user wants an **agent team** to systematically address each finding, with a supervisor agent
overseeing each fix in real time to ensure the workers are addressing the right thing.

## 2. Locked-in Decisions

These were resolved through clarifying questions before the design walkthrough:

| Decision | Choice | Rationale |
|---|---|---|
| Work unit | One worker per finding (`C-1`, `M-1`, …) | Findings have explicit IDs and severity in the synthesis report — natural queue |
| Fix target | Patch the upstream plan file | Plan must become executable; the artifact (ARCHIVE_MASTER.md) is downstream |
| Topology | Sequential gate | One worker at a time, supervisor reviews diff before next worker starts. Truest "real time" oversight. No edit collisions on the plan file |
| Verdict criteria | Faithful match + cross-section regression check + final E2E SHA round-trip 7/7 | Strongest correctness guarantee |
| Roster | 13 workers (skip S-1 informational, S-2 critique-document defect) | Both meta-findings have no plan-level edit |

## 3. Architecture

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR (in-session, the harness)                  │
│  • Holds worker queue (13 finding IDs in dependency order)                 │
│  • Spawns one Worker subagent at a time                                    │
│  • Spawns the Supervisor subagent after each Worker finishes               │
│  • Manages plan-file snapshots and run journal                             │
│  • Escalates to user when rework limit hits                                │
│  • Runs final E2E integration test after last worker                       │
└────────────────────────────────────────────────────────────────────────────┘
              │ Agent.spawn (1 per worker)         │ Agent.spawn (review)
              ▼                                    ▼
┌──────────────────────────────┐    ┌────────────────────────────────────────┐
│  WORKER (fresh per finding)  │    │  SUPERVISOR (single conceptual role,    │
│                              │    │   fresh subagent per turn, fed ledger)  │
│  • Reads ONE finding         │    │                                         │
│  • Reads relevant plan slice │    │  • Sees full synthesis report           │
│  • Verifies premise          │    │  • Sees full current plan state         │
│  • Verifies prescription     │    │  • Reads Worker's structured output     │
│  • Returns structured        │    │  • Verdict: APPROVE / REWORK / ESCALATE │
│    proposal (no file write)  │    │  • Records ledger entry per turn        │
└──────────────────────────────┘    └────────────────────────────────────────┘
              │                                    │
              │  proposed diff + rationale         │  verdict + ledger entry
              └──────────────┬─────────────────────┘
                             ▼
                  ┌────────────────────────────────┐
                  │  ORCHESTRATOR applies/rolls    │
                  │  back the diff to the plan     │
                  │  file (with backup snapshots)  │
                  └────────────────────────────────┘
```

### Architectural principles

- **Worker proposes; Orchestrator writes.** Workers never touch the plan file directly. They return
  a structured proposal; the Orchestrator applies it after Supervisor approval. Trivializes
  rollback and prevents partial states.
- **Supervisor is one role, fresh subagent per turn, with a ledger.** Each Supervisor invocation
  receives the cumulative ledger of prior verdicts so it can detect cross-finding contradictions
  ("this fix undoes what we approved for finding X").
- **Plan file lives outside the repo** (`~/.claude/plans/`), so we use timestamped backup snapshots
  instead of git. The original plan is preserved as `*.bak.original` for diffing.

## 4. Worker Contract

### Inputs (provided by Orchestrator)

| Input | Source |
|---|---|
| `finding_id` | e.g. `C-1`, `M-2` |
| `finding_text` | Verbatim section from the synthesis report |
| `current_plan_text` | Live read of the plan file |
| `applied_findings_ledger` | Short list of prior approved ledger entries |

The Worker does NOT receive the full synthesis report or other findings. Tight scope = predictable
output.

### Worker rules

1. **Stay in your lane.** Touch only sections relevant to your finding. Cross-references in the
   synthesis report's "See also" notes define each finding's natural scope.
2. **Verify, don't transcribe.** Each Worker treats its finding as a *starting hypothesis*, not a
   directive:
   - **Verify the premise** — does the described problem actually exist in the current plan state?
   - **Verify the prescription** — would the recommended fix actually solve the root problem?
   - **Choose the best approach** based on verification, not on blind implementation.
3. **No invented requirements.** Worker only addresses what its finding says. Stretch fixes
   ("while I'm here, let me also…") are forbidden — those belong to a different finding's Worker.
4. **One edit per Worker per turn.** If a finding needs multiple disjoint section edits (rare),
   Worker returns a list of edits but they stand or fall together (atomic).

### Valid Worker outcomes

| Outcome | When to choose | Example |
|---|---|---|
| `implement_as_recommended` | Verification confirms both premise and prescription | C-1: regex is broken (verified), length-prefixed extraction is the right fix (verified) |
| `implement_modified` | Premise is real but the recommended fix isn't best | M-3: relative path issue is real, but argv default to env var is more brittle than `pathlib.Path(__file__).resolve()` |
| `no_change_needed` | Premise is moot (already fixed by prior worker, or not a real issue) | L-3: leading blank lines warning is moot once C-1's length-prefixed reader lands |
| `disagree_with_finding` | Worker concludes the finding itself is wrong (e.g., misreading) | Rare. Triggers Supervisor's `ESCALATE_TO_USER` path |

### Worker output shape

```
finding_id: C-1
edit_type: section_rewrite | targeted_replace | append | no_change_needed
target_locator:
  - section_heading: "Boundary Marker Design (machine-extractable)"
  - or line_range: "L62-L68"
  - or unique_anchor_string: "<!-- =+ -->\n\n(.*?)\n\n<!-- =+ -->"
removed_content: |
  [literal text being removed — exact bytes for Edit tool's exact-match]
new_content: |
  [literal replacement text]
premise_check:
  finding_claims: "[paraphrase of the finding's claim]"
  verified_against_plan: true | false
  evidence: "[what Worker did to verify — e.g., re-ran Strategy A, got 7/7 SHA mismatches]"
prescription_check:
  recommended_fix: "[paraphrase of recommendation]"
  would_actually_solve_root_problem: true | false
  reasoning: "[why or why not]"
chosen_approach: implement_as_recommended | implement_modified | no_change_needed | disagree_with_finding
deviation_rationale: |
  [REQUIRED if chosen_approach != implement_as_recommended. Explains WHY.]
follow_up_findings_affected: [list of finding IDs this might invalidate or assist]
```

## 5. Supervisor Contract

### Inputs

| Input | Source |
|---|---|
| `finding_id` + `finding_text` | Same as Worker |
| `worker_output` | Full structured response |
| `current_plan_text` | Live read of the plan |
| `applied_findings_ledger` | Cumulative history of approved ledger entries |
| `full_synthesis_report` | All 15 findings (Supervisor needs cross-finding context) |

### Supervisor's 7-check review (in order)

| # | Check | REWORK trigger |
|:--:|---|---|
| 1 | Premise check is sound | Worker said "verified" without evidence, or evidence doesn't actually verify the claim |
| 2 | Prescription check is sound | Worker waved away the question of whether the fix solves the root problem |
| 3 | Chosen approach matches verification result | Worker claims "premise confirmed, prescription correct" but chose `implement_modified` (internal inconsistency) |
| 4 | Edit reflects the chosen approach | Diff doesn't match what Worker said it would do; sneaky scope creep |
| 5 | No regression on prior approved fixes | Diff undoes/contradicts a ledger entry |
| 6 | No invasion of another finding's lane | Diff touches a section that belongs to a not-yet-processed finding |
| 7 | Plan stays internally consistent | Dangling references to removed concepts (e.g., L-1 still cites the deleted regex) |

### Verdicts

| Verdict | Meaning | Orchestrator action |
|---|---|---|
| `APPROVE` | All 7 checks pass | Apply edit, snapshot, advance to next worker |
| `REWORK` | One or more checks failed | Increment attempt counter, spawn fresh Worker with prior attempt + specific Supervisor feedback |
| `ESCALATE_TO_USER` | Supervisor cannot confidently judge (e.g., Worker's `disagree_with_finding` is plausible but Supervisor is uncertain) | Pause loop, surface to user with both arguments |

### Supervisor output shape

```
verdict: APPROVE | REWORK | ESCALATE_TO_USER
checks_passed: [1, 2, 3, 4, 5, 6, 7]
checks_failed: [{check: 5, reason: "Diff modifies the SHA-256 expected value for next-step-..., contradicts M-1's read_bytes fix"}]
ledger_entry: |
  C-1: APPROVED. Replaced regex extraction with length-prefixed reader.
  Worker chose implement_as_recommended; verification re-ran Strategy-A and confirmed 7/7 SHA mismatches.
feedback_to_worker: |
  [Only if REWORK. Specific, actionable, references which check failed.]
```

The `ledger_entry` becomes part of `applied_findings_ledger` for the next Worker.

## 6. Worker Roster & Execution Order

13 workers in 4 dependency-driven phases. Sequential within and across phases.

```
PHASE 1 — Architectural foundation (must land first; all else depends)
  1.  C-1   Extraction protocol: regex → length-prefixed reader

PHASE 2 — Verification block (depends on C-1's rewritten verification code)
  2.  M-1   read_text() → read_bytes() in verification script
  3.  M-3   Relative path → absolute path (or argv) in verification script

PHASE 3 — Construction script (depends on C-1's writer protocol)
  4.  M-4   Provide full inline Python construction script
  5.  L-2   Add explicit "no globs — pinned 7-file allowlist" comment
  6.  N-3   Fix the "Why a script instead of Read/Write" rationale section

PHASE 4 — Prose & metadata (mostly independent of each other)
  7.  M-2   Tighten pre-flight collision wording (drop bare-60-equals claim)
  8.  L-1   FILE_LINES undercount note for 3 trailing-newline-less files
  9.  L-3   Leading blank lines in next-step-…txt          ← likely NO_CHANGE
 10.  L-4   Inject-vs-fixed YAML `generated:` date convention
 11.  L-5   Add interior `---` mention to Risks section
 12.  N-1   Visual vs text marker contradiction            ← likely NO_CHANGE
 13.  N-2   Update marker overhead estimate (~15 → ~17 lines per file)

FINAL INTEGRATION TEST (Orchestrator runs, no worker)
  • Extract patched plan's construction script → run → produces ARCHIVE_MASTER.md
  • Extract patched plan's verification script → run → must print "PASS: 7/7"
  • If FAIL → escalate to user with full E2E output
```

### Why this order

- **C-1 alone in Phase 1.** C-1 changes both writer protocol (no separator inserted) and reader
  protocol (length-prefixed). Every later finding either touches code C-1 already rewrote, or
  assumes the new architecture.
- **Phase 2 before Phase 3.** Phase 2 finishes the verification block C-1 already touched (single
  section). Phase 3 then provides the construction script that the verification block validates.
- **L-3 and N-1 likely `no_change_needed`.** Both findings warn about ambiguities created *by the
  regex approach*. C-1 deletes the regex. Worker's premise check should detect this and return
  `no_change_needed`; Supervisor should accept.
- **Phase 4 ordering is largely cosmetic.** Workers within Phase 4 touch disjoint sections; order
  doesn't matter much.

### Wall-clock estimate

13 workers × (Worker turn ~30-90s + Supervisor turn ~20-60s) + final E2E ≈ 15-40 minutes total.
Faster if `no_change_needed` short-circuits land (less Worker text to write).

## 7. Rework Loop

```
                       ┌────────────────────────────┐
                       │ Worker spawned for finding │
                       └─────────────┬──────────────┘
                                     ▼
                       ┌────────────────────────────┐
                       │ Worker proposes structured │
                       │ output                     │
                       └─────────────┬──────────────┘
                                     ▼
                       ┌────────────────────────────┐
                       │ Supervisor reviews         │
                       └──┬──────────┬──────────┬──┘
                          │APPROVE   │REWORK    │ESCALATE
                          ▼          │          ▼
                 ┌──────────────┐    │   ┌──────────────────┐
                 │ Apply edit.  │    │   │ Pause. Surface   │
                 │ Snapshot.    │    │   │ to user with     │
                 │ Next worker. │    │   │ full context.    │
                 └──────────────┘    │   └──────────────────┘
                                     ▼
                       ┌────────────────────────────┐
                       │ attempt_count++. If <= 3,  │
                       │ spawn FRESH Worker subagent│
                       │ with prior attempt +       │
                       │ Supervisor feedback as     │
                       │ context. Else ESCALATE.    │
                       └────────────────────────────┘
```

**Why fresh Worker subagent on rework.** A subagent that already invested in a wrong approach will
rationalize it. A fresh subagent reading "previous Worker tried X, Supervisor rejected because Y" is
more likely to take a different angle. Costs an extra spawn but protects against tunnel vision.

**Rework limit: 3 attempts** (configurable). After the 3rd `REWORK`, automatic escalation.

## 8. Escalation to User

When `ESCALATE` fires (Supervisor verdict OR 3-attempt limit), the Orchestrator pauses and presents:

```
ESCALATION — finding M-3 stuck after 3 attempts

Finding text:
  [verbatim from synthesis report]

Attempt 1: Worker proposed → ROOT_DIR = pathlib.Path(__file__).resolve().parent
  Supervisor REWORK: "parent" goes one level too few; need parents[N] tied to actual repo depth

Attempt 2: Worker proposed → parents[2]
  Supervisor REWORK: this script lives outside the repo at ~/.claude/plans; parents[N] won't work

Attempt 3: Worker proposed → accept argv[1], default to env var
  Supervisor REWORK: defaulting to env var is a new dependency the plan doesn't establish

Your options:
  [1] Approve attempt 3 as-is (override Supervisor)
  [2] Provide custom direction (free text → spawned as Worker hint)
  [3] Skip this finding (record as deferred, continue loop)
  [4] Abort entire run (latest snapshot preserved)
```

User selection drives the next Orchestrator action.

## 9. Snapshots & Rollback

| Snapshot | When written | Purpose |
|---|---|---|
| `consolidate-…md.bak.original` | Once, before any worker | Always-recoverable starting point |
| `consolidate-…md.bak.before-{ID}` | Before each apply | Restore point if Supervisor approves then we discover an issue |
| `consolidate-…md.bak.after-{ID}` | After each approval | Audit trail of incremental progress |
| `consolidate-…md` | Live, mutated in place | Current state seen by next Worker |

**Validation after each apply:** Orchestrator reads the file back and runs basic markdown structural
sanity (headings present, no unterminated code fences, file size > minimum). If validation fails,
auto-rollback to `.before-{ID}` and Supervisor verdict downgrades to `REWORK`.

## 10. Failure Modes

| Failure | Detection | Recovery |
|---|---|---|
| Plan file corrupted by Edit | Post-apply markdown validation | Auto-rollback to `.before-{ID}`, REWORK |
| Worker stuck in 3-attempt loop | Attempt counter | Auto-escalate to user |
| Worker `disagree_with_finding` is plausible but Supervisor uncertain | Supervisor verdict ESCALATE | User decides |
| Edit's `removed_content` doesn't match plan (file drifted) | `Edit` tool exact-match fails | Spawn fresh Worker with current state, attempt counter unchanged (system error, not Worker error) |
| Final E2E test fails (PASS not 7/7) | E2E exit code | Escalate to user with full E2E output; offer per-finding bisect |
| User aborts | User input | Plan stays at last `.after-{ID}` snapshot; print summary of completed findings |
| Orchestrator crashes mid-loop | Journal file exists on next startup | Offer to resume from journal |

## 11. Implementation Harness

**Where this runs:** In-session, with the orchestrating session acting as Orchestrator.

**Tools the Orchestrator uses:**
- `Agent` (general-purpose subagent_type) — spawns Workers and Supervisor with self-contained prompts
- `Read` — plan, finding text, prior snapshots, journal
- `Edit` — applies approved diffs (uses exact-match for safety)
- `Bash` — snapshots (`cp`), structural validation, final E2E test (`python3`)
- `AskUserQuestion` — escalations and resume prompts
- `TaskCreate` / `TaskUpdate` — tracks 13 worker tasks + 1 E2E task for visibility

**State the Orchestrator holds across the loop:**
- Worker queue (13 ordered finding IDs)
- Current finding being processed
- Attempt counter for current finding
- `applied_findings_ledger` (list of approved ledger entries)
- Snapshot paths
- Journal path (for resume after crash)

**Persistence (for resumability):**
- `~/.claude/plans/.consolidate-fix-run/journal.json` — completed findings, current finding,
  attempt count, ledger
- `~/.claude/plans/.consolidate-fix-run/run-log.md` — append-only log of every Worker prompt,
  Worker output, Supervisor verdict (post-hoc debugging)

On Orchestrator startup, check for existing journal and offer to resume.

**Why not GSD:** GSD's execute-phase pattern is built for project phases with persistent artifacts
and atomic commits per task. This is a one-shot task on a file outside the repo. A direct in-session
orchestrator is lighter and more transparent — the user sees each Worker's output and each
Supervisor verdict as they happen.

## 12. Open Defaults (Baked Into the Design)

These are sensible defaults chosen during design; the implementation plan can expose them as knobs
if desired:

| Default | Value | Knob? |
|---|---|---|
| Rework attempts before escalation | 3 | Yes |
| Worker subagent type | `general-purpose` | No |
| Supervisor subagent type | `general-purpose` | No |
| Snapshot directory | next to plan file (same dir) | Yes |
| Journal directory | `~/.claude/plans/.consolidate-fix-run/` | Yes |
| Final E2E required to PASS | 7/7 SHA round-trip | No (correctness gate) |
| Markdown sanity check after apply | Enabled | Yes |

## 13. Out of Scope

- **Meta-finding S-1** (informational only — captured indirectly via C-1 fix).
- **Meta-finding S-2** (critique #1 document defect — out of scope for plan patching). Critique #1
  remains as-is.
- **Re-running the team if the original plan changes upstream.** The design assumes a single
  consistent starting point.
- **Modifying the synthesis report.** The synthesis report is the contract; Workers read it but
  don't write to it.

## 14. Next Steps

1. Commit this design doc.
2. Invoke the `superpowers:writing-plans` skill to produce a step-by-step implementation plan
   (executable in this session or another).
3. On user approval of the implementation plan, run the harness.
