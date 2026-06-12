---
status: active
purpose: review-findings
created: 2026-06-12
milestone: v1.5
phase: 25-evidence-framework-and-issue-ledger
retirement_trigger: Phase 25 execution complete and findings addressed or dispositioned
---

# Phase 25 Planning Artifacts — Adversarial Review

**Reviewer:** Claude (compound-engineering specialist panel: correctness, maintainability, reliability)
**Date:** 2026-06-12
**Scope:** 25-01-PLAN.md, 25-02-PLAN.md, 25-CONTEXT.md, 25-RESEARCH.md, 25-PATTERNS.md, 25-VALIDATION.md, 25-DISCUSSION-LOG.md
**Governance cross-check:** REQUIREMENTS.md (EVID-06..10, VER-10, SCOPE-06..11), ROADMAP.md (Phase 25 goal + 5 success criteria), CLAUDE.md STOP protocol, v1.5-GAPS.md

---

## Executive Summary

Phase 25's planning artifacts are **structurally strong** — they demonstrate a deep understanding of the v1.4 precedent, the six requirements they must satisfy, and the STOP-protocol governance boundary. The decision trail from D-01 through D-18 is thorough, and the RESEARCH file's pitfall catalogue is unusually self-aware.

That said, the review identifies **15 findings** across three dimensions, of which **3 are CRITICAL** and **5 are HIGH**. The critical findings cluster around two root causes:

1. **A commit-granularity contradiction** between per-task "SAME COMMIT" ledger-wiring instructions and the plan-level "one atomic commit" success criterion. The autonomous executor cannot reconcile these without an explicit commit-strategy instruction.
2. **A section-count inconsistency** (12 vs 13 vs 14 "sections") across the plan set that could cause structural drift in the template, propagating to every downstream evidence packet.

A third systemic issue — the D-01 "split reading" flag — is correctly identified in the plans but lacks a user-confirmation gate before execution. If the user rejects the split reading post-execution, Phase 25 would require replanning.

### Quick Reference

| ID | Severity | Dimension | One-line summary |
|----|----------|-----------|------------------|
| F-01 | CRITICAL | Logical | One-atomic-commit vs per-task-same-commit contradiction in 25-02 |
| F-02 | CRITICAL | Clarity | Section-count inconsistency (12/13/14) across plan documents |
| F-03 | CRITICAL | Resilience | No directory-creation step for `evidence/` before first file write |
| F-04 | HIGH | Logical | D-01 split-reading flag lacks a user-confirmation gate before execution |
| F-05 | HIGH | Logical | PENDING→PENDING transition is a process-schema decision not formally gapped |
| F-06 | HIGH | Clarity | M11 GUARD threshold is subjective — "sufficient and unambiguous" undefined |
| F-07 | HIGH | Resilience | No rollback/recovery procedure for mid-plan failures |
| F-08 | HIGH | Resilience | STOP-gap git state ambiguous — partial work commit/discard unspecified |
| F-09 | MEDIUM | Logical | D-15 caveat-propagation scope ambiguous for non-Phase-25 findings |
| F-10 | MEDIUM | Logical | Framework-spec line ranges not mechanically verified (assumption A1) |
| F-11 | MEDIUM | Clarity | "Near-verbatim" copy instruction permits unintentional prose drift |
| F-12 | MEDIUM | Clarity | SHA placeholder in transition logs — no fill-in instruction |
| F-13 | MEDIUM | Resilience | Grep-based verify checks confirm string presence, not structural correctness |
| F-14 | MEDIUM | Resilience | No preflight check for scripts/agent-commit or GIT_AGENT_ID env vars |
| F-15 | LOW | Clarity | SUMMARY output files not in files_modified — commit tracking ambiguous |

---

## Dimension 1: Logical Integrity

### F-01 · CRITICAL · Commit-granularity contradiction in 25-02

**Location:** 25-02-PLAN.md Tasks 1–3 (per-task "LEDGER WIRING (D-06, SAME COMMIT)" at lines 144, 195, 245) vs. success criterion (line 317: "One atomic commit via scripts/agent-commit, scope 25-02")

**Problem:** Each of the three tasks creates an EVID-10 record AND performs ledger wiring with the instruction "SAME COMMIT." But the plan's success criteria require exactly one atomic commit. An autonomous executor faces an irreconcilable choice:

- **Interpretation A:** Commit after each task (3 commits). D-06 same-commit discipline holds per task, but the one-atomic-commit success criterion fails. Between commits, the ledger is in an inconsistent state (e.g., SCS linked but D=6.694 not yet linked).
- **Interpretation B:** Stage all changes and commit once after Task 3. One-atomic-commit succeeds, but the per-task "SAME COMMIT" instructions are structurally violated — the agent is deferring ledger writes to a batch, not committing them alongside each record.

**Impact:** This is the single highest-impact ambiguity. The executor's choice determines whether D-06 holds and whether the success criterion passes. No automated verify step counts commits, so the wrong choice passes grep checks silently.

**Recommended fix:** Add an explicit commit-strategy instruction: *"Do NOT commit between tasks. Stage each task's record + ledger edits incrementally (`git add` per task). After Task 3 completes and all verifications pass, execute a single `scripts/agent-commit` with `GIT_AGENT_OWNED_PATHS` covering all four files."*

---

### F-04 · HIGH · D-01 split-reading flag lacks a user-confirmation gate

**Location:** 25-01-PLAN.md objective (line 50, D-01 flag); 25-CONTEXT.md D-01 (lines 23–25); ROADMAP.md success criteria 1–3

**Problem:** The ROADMAP success criteria 1–3 say "each issue-02 finding selected for remediation" — a universal quantifier that literally means all 19 findings. CONTEXT D-01 adopts a "split reading" (3 conflicts only) and flags the tension for user review. But neither plan includes a blocking gate that waits for user confirmation before execution. An autonomous agent will note the flag, find no gate, and proceed with the split reading — correct per D-01 but unconfirmed.

**Impact:** If the user actually intended the literal reading (all 19 packets), Phase 25 exits with 16 missing packets and fails success criteria 1–3 at the ROADMAP level. Recovery requires replanning Phase 25 as a full-adjudication phase.

**Recommended fix:** Add an explicit user-confirmation step before Task 0 of Plan 25-01 (or as a pre-wave gate): *"Print the D-01 flag to the user and wait for confirmation of the split reading before any mutation. Do not proceed until the user responds."*

---

### F-05 · HIGH · PENDING→PENDING transition is a process-schema decision not formally gapped

**Location:** 25-02-PLAN.md objective (lines 75–76); Task 1 line 143, Task 2 line 193, Task 3 line 244

**Problem:** The plan keeps all three adjudicated rows at PENDING status with a `PENDING -> PENDING (Phase 25 P02 ...)` transition-log entry. The plan acknowledges the lifecycle is "source-silent on adjudicated-but-unfixed" and calls this a "candidate process-artifact-schema gap" but does NOT execute the STOP protocol for it — it proceeds without formally recording it in `25-GAPS.md`.

Per CLAUDE.md governance: *"Process-artifact schemas… MUST surface, never invent."* The PENDING→PENDING convention is an invention of a new pseudo-state ("adjudicated-but-unfixed") without user authorization.

The reasoning is sound (IN_PROGRESS is defined as "fix being worked," which isn't true in Phase 25; PENDING is the no-invention default). But the governance protocol requires either: (a) formally gap it and get user instruction, or (b) classify it as "operational coordination" and log it. The plan does neither formally.

**Impact:** Downstream Phases 26–28 will see PENDING rows with verdicts assigned. If they treat PENDING as "not yet touched," they may re-adjudicate or skip findings. The semantic gap propagates.

**Recommended fix:** Either formally record this as an operational-coordination gap in `25-GAPS.md` (classification: operational-coordination; agent was tempted to: invent PENDING→IN_PROGRESS; what the user needs to decide: confirm the PENDING→PENDING convention is acceptable), or classify it as "Claude's discretion" operational coordination and log it explicitly in the CONTEXT.

---

### F-09 · MEDIUM · D-15 caveat-propagation scope ambiguous

**Location:** 25-CONTEXT.md D-15 (line 54); 24.5-READINESS-REPORT.md caveat table; 25-02-PLAN.md must_haves (line 25)

**Problem:** D-15 says "each caveat is propagated into the affected finding's packet." The readiness report lists 7 caveats (OI-1, OI-3, OI-6, OI-7, OI-8, OI-11, OI-12). Phase 25 adjudicates only 3 findings. OI-7 (M13) and OI-12 (addendum erratum) are correctly NOT propagated because their affected findings aren't Phase 25's. But D-15's "each caveat" language could be read as requiring propagation of all 7 caveats into some Phase 25 artifact.

**Recommended fix:** Clarify D-15 text: *"each caveat whose affected finding is among the three Phase 25 EVID-10 conflicts is propagated into that finding's record; unaffected caveats are carried forward by their owning phases."*

---

### F-10 · MEDIUM · Framework-spec line ranges not mechanically verified

**Location:** 25-02-PLAN.md Task 2 read_first (line 175); 25-RESEARCH.md assumption A1

**Problem:** Framework-spec line numbers (e.g., `ctl_instruction.md` line ~598 rejecting 6.694) are resolution-doc self-cites flagged as "may have shifted." The plans instruct "RE-VERIFY all line numbers at authoring time" — but no acceptance criterion or automated verify step confirms re-verification occurred. If the executor skips it, records carry stale ranges. The VALIDATION section calls for manual checking, but all tasks are `type: auto`.

**Recommended fix:** Add guidance: *"If re-verification shows the line number has shifted but the content is unchanged, update the range and proceed. If the content itself has changed or is absent, STOP and surface as a gap — do not proceed with a stale citation."*

---

## Dimension 2: Execution Clarity

### F-02 · CRITICAL · Section-count inconsistency across the plan set

**Location:** 25-01-PLAN.md Task 1 action ("13-section structure"), 25-02-PLAN.md objective ("14-section structure"), CONTEXT D-04 ("12-section schema"), PATTERNS.md ("all 14 sections"), acceptance criteria ("all 14 sections present")

**Problem:** The actual v1.4 `_TEMPLATE.md` has 12 `##`-level sections plus the `#` Title heading (13 top-level headings). The new `### Dataset Evidence` is a sub-block, not a `##` section, so adding it keeps the `##` count at 12. But the plan documents cite 12, 13, and 14 at different points. An autonomous agent cannot determine which counting scheme applies and may produce:
- 12 `##` sections (matching v1.4, missing §3b as a `##`)
- 13 `##` sections (promoting §3b to `##`)
- 14 sections (counting Title + all `##` including a new one)

The grep-based verify checks for "Dataset Evidence" but not heading level or section count.

**Impact:** A structural error in the template propagates to all three EVID-10 records and every downstream Phase 26–28 packet. Fixing after the fact requires re-authoring 6+ files.

**Recommended fix:** Adopt one canonical count. The v1.4 template has 12 `##`-level sections. Adding `### Dataset Evidence` as a sub-block under `## Spec Evidence` keeps it at 12 `##` sections. State explicitly: *"12 `##`-level sections (unchanged) plus one new `###` sub-block."* Update all references in 25-01, 25-02, and PATTERNS to match. Add a verify step that counts `##` headings and asserts the exact number.

---

### F-06 · HIGH · M11 GUARD threshold is subjective

**Location:** 25-02-PLAN.md Task 3 M11 GUARD (lines 239–240)

**Problem:** The guard says "PROCEED… IF that data-integrity grounding is sufficient and unambiguous." The terms "sufficient" and "unambiguous" are subjective. The OI-8 caveat (M11 live-loader consumption `unverified — SCOPE-10`) is already known to be outside grounding — which means one of the two guard triggers is already partially true. Different agents will threshold differently, producing non-deterministic M11 outcomes.

**Recommended fix:** Replace the subjective threshold with concrete decision criteria: *"PROCEED if `24.5-RESOLUTION-MAP.md` maps M11 to a resolution-doc section that contains an explicit severity recommendation grounded on data-integrity evidence. DEFER if that section contains only the phrase 'EVID-10's call' without an accompanying data-grounded severity argument."* This makes the guard mechanical.

---

### F-11 · MEDIUM · "Near-verbatim" copy permits unintentional drift

**Location:** 25-01-PLAN.md Task 1 action (line 112)

**Problem:** "Copy the v1.4 `_TEMPLATE.md` 13-section structure near-verbatim" is ambiguous. Does "near-verbatim" mean "copy structure but adjust prose" or "copy everything exactly except the named substitutions"? An agent may rewrite prose for "clarity" while preserving headings, introducing v1.4-incompatible language.

**Recommended fix:** Replace with: *"Copy the markdown structure and prose EXACTLY. Apply ONLY the substitutions listed below. Any deviation from the v1.4 template beyond these substitutions is a defect."*

---

### F-12 · MEDIUM · SHA placeholder in transition logs

**Location:** 25-02-PLAN.md all task action blocks (Status Transition Log entries using `2026-MM-DD <SHA>`)

**Problem:** The plan uses `2026-MM-DD` and `<SHA>` placeholders but does not specify whether the agent should fill them at authoring time, or how to handle the SHA (which is unknown before the commit).

**Recommended fix:** Add explicit instruction: *"Use the current date in YYYY-MM-DD format. Write the literal placeholder `<SHA>`. After the commit succeeds, the agent MUST amend the record to replace `<SHA>` with the actual short SHA."*

---

## Dimension 3: Operational Resilience

### F-03 · CRITICAL · No directory-creation step for `evidence/`

**Location:** 25-01-PLAN.md Task 1 (first file write to `evidence/_TEMPLATE.md`)

**Problem:** The `evidence/` directory does not yet exist (confirmed via `ls`). No task in either plan explicitly creates it. Whether the Write tool auto-creates intermediate directories is tooling-dependent and unspecified. If it doesn't, Task 1 fails at the first write with a path-not-found error and the agent has no fallback instruction.

**Impact:** Hard block at the very first file-creation step. The agent cannot recover without a mkdir instruction that isn't in the plan.

**Recommended fix:** Add `mkdir -p .planning/phases/25-evidence-framework-and-issue-ledger/evidence/` as the first action in Task 1 (or as a new Task 0.5 between the tag and the template), with a verify step confirming the directory exists.

---

### F-07 · HIGH · No rollback/recovery procedure for mid-plan failures

**Location:** 25-01-PLAN.md Tasks 0–3; 25-02-PLAN.md Tasks 1–3

**Problem:** If a task fails mid-execution (e.g., Task 2 succeeds but Task 3 fails), the plan provides no recovery procedure. The recovery tag `v1.5-pre-phase-25` is cut at Task 0, but neither plan instructs the agent to USE it on failure. The agent is left with partially mutated files and no clear next step.

**Recommended fix:** Add a `<failure_recovery>` section to each plan: *"If a task fails before any commit, discard uncommitted work via `git checkout -- <files>` back to the tag. If a STOP gap fires on one task in 25-02, commit the completed records as a partial commit, create `25-GAPS.md` for the halted task. The tag `v1.5-pre-phase-25` is the full-rollback reset point."*

---

### F-08 · HIGH · STOP-gap git state ambiguous

**Location:** 25-02-PLAN.md Task 3 M11 GUARD (line 239)

**Problem:** If the M11 GUARD fires, the plan says to create `25-GAPS.md` and halt — but the `m11-m12-severity.md` file is in an indeterminate state (partially written, no verdict for M11). The plan doesn't specify whether to commit the partial record, discard it, or commit only the SCS + D=6.694 records.

**Recommended fix:** Add explicit guidance: *"If a STOP gap fires on Task 3, first commit Tasks 1–2 output as a partial commit with scope `25-02-partial`. Then create `25-GAPS.md` and halt Task 3. The `m11-m12-severity.md` file is NOT committed; it stays as an in-progress draft."*

---

### F-13 · MEDIUM · Grep-based verify checks confirm presence, not structure

**Location:** All task `<verify><automated>` blocks in both plans

**Problem:** Every verification step uses `grep -q` for string presence. These can produce false positives: `"Dataset Evidence"` could appear in a comment; `"accept-resolution"` could appear in the wrong section; `"Phases 26-28"` could appear in the Notes section rather than the Lifecycle Rules block. No verify step checks WHERE in the file a string appears or counts `##` headings.

**Recommended fix:** Supplement grep checks with structural verification:
- Count `##` headings and assert the expected number.
- For ledger edits, verify the changed line specifically (`grep -n "Phases 26-28" ... | grep -q "^79:"` or re-verified line).
- For verdicts, check the Header `Current Verdict` row specifically (`grep -A2 "Current Verdict" ... | grep -q "accept-resolution"`).

---

### F-14 · MEDIUM · No preflight check for scripts/agent-commit

**Location:** 25-01-PLAN.md, 25-02-PLAN.md (both mandate `scripts/agent-commit`)

**Problem:** Both plans mandate using `scripts/agent-commit` (requires `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS` env vars) but neither includes a Wave 0 / precondition check. If the env vars are unset, the script exits 1 — discovered only at commit time after all authoring work is done.

**Recommended fix:** Add to Task 0 of Plan 25-01: *"Verify `scripts/agent-commit` is executable and that `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS` are set. If any are missing, halt before any file mutation."*

---

### F-15 · LOW · SUMMARY output files not in files_modified

**Location:** 25-01-PLAN.md `<output>` (line 244), 25-02-PLAN.md `<output>` (line 321)

**Problem:** Both plans end with `<output>Create 25-NN-SUMMARY.md when done.</output>` but these files aren't in `files_modified` or `artifacts_this_phase_produces`. The agent-commit script stages only `GIT_AGENT_OWNED_PATHS` files. It's unclear whether SUMMARYs should be committed.

**Recommended fix:** Either add SUMMARYs to `files_modified` and `GIT_AGENT_OWNED_PATHS`, or add an explicit note that SUMMARYs are handled by the gsd-tools workflow handler and are NOT part of the plan's commit.

---

## Residual Risks

| Risk | Likelihood | Impact |
|------|-----------|--------|
| **Commit-granularity choice (F-01)** determines whether D-06 holds and whether the success criterion passes. No automated check catches the wrong choice. | HIGH | Ledger inconsistency between commits; success criterion failure |
| **D-01 user rejection** post-execution requires full Phase 25 replan as a 19-finding adjudication phase. | MEDIUM | All 25-02 work discarded; 16 additional packets required |
| **M11 GUARD non-determinism** — different agents reach different conclusions about whether the guard fires. | MEDIUM | M11 severity ruling flips between executions |
| **PENDING→PENDING convention** propagates to Phases 26–28, which may misinterpret PENDING rows with verdicts as "not yet touched." | MEDIUM | Duplicate adjudication or skipped findings downstream |
| **Template section-count error** propagates to 6+ files (3 EVID-10 records + Phase 26–28 packets). | HIGH | Structural inconsistency requiring multi-file re-authoring |

---

## Testing Gaps

1. **No section-count or heading-structure verify step** in any task. Grep checks content strings but not document structure.
2. **No cross-file consistency check** between `_TEMPLATE.md` and `README.md` after 25-01 completes (shared verdict enum, EVID-10 markers).
3. **No commit-count assertion** — the verify section does not confirm the number of commits matches the expected count.
4. **No path-resolution verify** for relative markdown links in the ledger (Evidence-Packet column).
5. **No freshness check** on `24-ISSUE-LEDGER.md` before editing (concurrent session risk).
6. **No 24.5 gate check** in Task 0 — the agent verifies the branch but not the phase gate status.

---

## Disposition Recommendation

| Finding | Recommended Action |
|---------|-------------------|
| F-01 (commit granularity) | **Fix before execution.** Add explicit commit-strategy instruction to 25-02. |
| F-02 (section count) | **Fix before execution.** Canonicalize to "12 `##` sections + 1 `###` sub-block" and update all references. |
| F-03 (mkdir) | **Fix before execution.** Add directory-creation step to 25-01 Task 1. |
| F-04 (D-01 gate) | **Fix before execution.** Add user-confirmation gate. |
| F-05 (PENDING gap) | **Decide:** formally gap it or classify as operational coordination with explicit logging. |
| F-06 (M11 GUARD) | **Fix before execution.** Make guard criteria mechanical. |
| F-07 (rollback) | **Fix before execution.** Add `<failure_recovery>` sections. |
| F-08 (STOP-gap state) | **Fix before execution.** Specify partial-commit behavior. |
| F-09–F-15 | **Address before execution if feasible; otherwise acknowledge as accepted risk.** |

---

*Review completed 2026-06-12. Findings derived from adversarial specialist panel covering logical integrity, execution clarity, and operational resilience.*
