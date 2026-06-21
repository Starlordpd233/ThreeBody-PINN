---
phase: 32
reviewers: [agy, codex, claude, cursor, claude-glm, claude-deepseek, claude-minimax]
reviewed_at: 2026-06-21T06:33:40Z
generated_by: xreview
restored_note: reassembled from preserved first-run reviewer outputs after a --claude/--claude-glm rerun overwrote this file (dispatcher overwrites rather than merges). claude and claude-glm hung to the 240s watchdog (exit 143, 0 bytes); claude-minimax exceeded context.
---

# Cross-AI Plan Review — Phase 32

## agy Review

# Cross-AI Plan Review: Phase 32

This document provides a plan review for Phase 32 (Evidence Framework, Issue Ledger & Conflict Adjudication) of the **Three-Body Physics-Informed LLM** project.

## 1. Summary

The plans for Phase 32 ([32-01-PLAN.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-01-PLAN.md) through [32-04-PLAN.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-04-PLAN.md)) establish the curriculum-and-training-loop (`issue-03`) adjudication framework. The goal is to set up a protocol, schema, and ledger to resolve five headline conflicts: causal training mode (`D-04`), stage-gate frame (`D-05`), static epsilon strategy (`D-06`), gradient clipping (`M14`), and the scaling constant `D` conflict (`D = 6.694` vs `D ~= 4.6416`). The plan is structured across four wave-based execution steps:
*   **Plan 32-01 (Wave 1):** Scaffolding and machinery generation (protocol [README.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/README.md), [_TEMPLATE.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/_TEMPLATE.md), seeding 18 rows in [32-ISSUE-LEDGER.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md), and initializing [32-VERIFICATION.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-VERIFICATION.md)).
*   **Plan 32-02 (Wave 2):** Authoring factual and locked-convention-grounded packets ([d-6-694-conflict.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-6-694-conflict.md) and [m14-gradient-clipping.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/m14-gradient-clipping.md)).
*   **Plan 32-03 (Wave 3):** Authoring owner-routed packets ([d-04-causal-training-mode.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-04-causal-training-mode.md), [d-05-s-min-frame.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-05-s-min-frame.md), and [d-06-epsilon-strategy.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-06-epsilon-strategy.md)), defaulting to `defer-with-blocker` rather than choosing auto-defaults when user guidance is absent.
*   **Plan 32-04 (Wave 4):** Execution of structural validation checks, updating [32-VERIFICATION.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-VERIFICATION.md), and closeout.

---

## 2. Strengths

*   **Strict Governance & Boundary Enforcement:** The plans enforce a zero-edit boundary on editable framework specs ([ctl_instruction.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md) and [pinn_architecture.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/pinn_architecture.md)) and the production code directory ([pinn/](file://<home>/Desktop/3_body_problem/.worktrees/specwork/pinn/)) during Phase 32.
*   **STOP-Gap Integrity:** The inclusion of the `defer-with-blocker` mechanism for owner-routed parameters (`D-04`, `D-05`, `D-06`) prevents auto-mode executors from silently resolving mathematical or physical design decisions without explicit user confirmation.
*   **Historical Continuity:** Directly adapts the v1.5 Phase 25 baseline, keeping the adjudication taxonomy and the non-terminal nature of `FIX_APPLIED` statuses consistent.
*   **Robust Dirty-Doc Protection:** Explicitly runs baseline checks on the unrelated dirty document ([2026-06-20-gsd-review-dispatch-resilience-plan.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/docs/work/plans/cross_cutting/gsd-cross-ai-review-resilience/2026-06-20-gsd-review-dispatch-resilience-plan.md)) to prevent accidental commits or changes during the branch's specwork execution.

---

## 3. Concerns

### `[MEDIUM]` Downstream Disconnect for the Remaining 13 Findings
*   **Description:** The ledger is seeded with all 18 selected findings, but Phase 32 only authors evidence packets for the 5 headline conflicts. The remaining 13 findings are left with `PENDING` statuses and placeholder verdicts. The plans rely on owning downstream contract phases (Phases 33–35) to author their respective packets immediately prior to making spec edits. However, if those phases' plans do not explicitly mandate authoring these packets before spec transcription, the ledger will remain incomplete.
*   **Impact:** Downstream phases might transcribe contract changes without the rigorous vetting provided by the evidence packets, leading to drift.

### `[MEDIUM]` Preemptive Gap File Creation Risk
*   **Description:** [32-03-PLAN.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-03-PLAN.md) specifies files modified to include [32-GAPS.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-GAPS.md) and [v1.6-GAPS.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/milestones/v1.6-GAPS.md) in the frontmatter, but states that they are "STOP-only" and "created only if a real STOP trigger fires." If an automated executor interprets the frontmatter as a directive to modify or create these files, it may preemptively create empty files, which violates the `AGENTS.md` and `32-SPEC.md` rules stating they must not exist unless a new, unrouted gap is encountered.
*   **Impact:** Inconsistent implementation of the STOP protocol and cluttering of workspace state with empty files.

### `[LOW]` Capturing the Dirty-Doc Baseline Out of Order
*   **Description:** In [32-01-PLAN.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-01-PLAN.md) Task 1, the action says: *"Before creating any Phase 32 artifact, compute and retain the dirty-doc baseline..."* however, the task's targets list [README.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/README.md) as a file modified. Since Task 1 modifies this file, the baseline must be calculated before Task 1 execution begins. If the execution sequence does not run the baseline calculation *first*, the verification checks in [32-04-PLAN.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-04-PLAN.md) will be comparing against a post-hoc baseline.
*   **Impact:** Weakens the protection guard for unrelated modified files.

---

## 4. Suggestions

*   **Pre-execution Baseline Step:** Explicitly place the dirty-doc baseline command execution at the very beginning of the Wave 1 plan as a standalone setup step (or Task 0), ensuring the baseline hash is stored before *any* write operations occur.
*   **Enforce Downstream Evidence Mandate:** Add a explicit instruction in [README.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/README.md) specifying that downstream phases (Phases 33–35) **MUST** author their assigned findings' evidence packets (e.g., using the `_TEMPLATE.md`) and transition their ledger status from `PENDING` to `IN_PROGRESS` or `FIX_APPLIED` *before* editing the framework specs.
*   **Frontmatter Modification Clarification:** Remove [32-GAPS.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-GAPS.md) and [v1.6-GAPS.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/milestones/v1.6-GAPS.md) from the standard `files_modified` frontmatter in [32-03-PLAN.md](file://<home>/Desktop/3_body_problem/.worktrees/specwork/.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-03-PLAN.md) to prevent automated executors from touching them during clean runs. Move them to a conditional section.

---

## 5. Overall Risk

**Overall Risk: LOW**

The implementation plans are highly detailed, follow established precedents, and contain strict boundary protections. The risk of scope creep or broken dependencies is low, provided the suggestions for strict sequencing and downstream packet-generation rules are enforced.

---

## codex Review

## Summary

The plans are mostly well-structured and should achieve Phase 32’s goal: they build the evidence machinery first, separate adjudicable conflicts from owner-routed decisions, preserve the no-spec-edit boundary, and close with structural verification before downstream phases consume the artifacts.

Overall, the main risks are not conceptual scope creep but execution ambiguity: STOP-only gap files are listed as modified artifacts, summary files are requested but not owned or verified, and several validation checks are substring-level guards that could pass the wrong thing.

## Strengths

- **HIGH:** Dependency ordering is sound: protocol/template/ledger first, then adjudicable packets, then owner-routed packets, then closeout verification.
- **HIGH:** The plans correctly preserve v1.6 governance: resolution doc as candidate source, `pinn/` not grounding, Phase 32 as specwork-only, no framework-spec edits.
- **HIGH:** D-04/D-05/D-06 are treated conservatively with `defer-with-blocker` unless explicit owner instruction exists.
- **MEDIUM:** The dirty-doc baseline and protected-path guards are a good response to the known dirty worktree.
- **MEDIUM:** The D conflict and M14 split are appropriately separated from the owner-routed semantic decisions.

## Concerns

- **MEDIUM:** Plan 32-03 lists `32-GAPS.md` and `.planning/milestones/v1.6-GAPS.md` under `files_modified` and artifacts even though the text says they are STOP-only and must not be pre-created. This may cause an executor or commit wrapper to treat empty gap registers as expected outputs.
- **MEDIUM:** Each plan’s `<output>` requires a `32-0X-SUMMARY.md`, but those files are not included in `files_modified`, ownership checks, closeout artifact checks, or verification scope. This creates a mismatch between required outputs and permitted/validated files.
- **MEDIUM:** Some closeout checks are too weak for the governance risk. For example, live `pinn/` references only need `NOT grounding` or `FUT` somewhere in the evidence directory, not in the same packet or paragraph. Similarly, D-04/D-05/D-06 checks can pass if `explicit user instruction` appears in cautionary prose.
- **MEDIUM:** The ledger terminal-state guard allows `| FIX_APPLIED |` if explanatory lifecycle prose exists anywhere. That may miss a row accidentally left at terminal `FIX_APPLIED`.
- **LOW:** The dirty-doc baseline capture is correct in intent but operationally fragile. Plan 32-01 says to compute and retain it before creating artifacts, but the durable recording happens in Task 3. If the executor loses the value, the plan correctly blocks, but a clearer first action would reduce avoidable failure.
- **LOW:** Plan 32-04 adapts the older “no `32-*-PLAN.md`” check to “exactly four expected plan files,” which is necessary, but the surrounding context still contains the older prohibition. Executors should not treat that older line as current closeout criteria.

## Suggestions

- Remove STOP-only gap files from Plan 32-03 `files_modified`; mention them only in conditional STOP handling and commit ownership instructions.
- Add the four `32-0X-SUMMARY.md` files to each plan’s `files_modified`, verification, and owned-path guidance, or drop the summary outputs.
- Strengthen verification with packet-scoped checks: verify each packet containing a `pinn/` reference also contains `NOT grounding` or `FUT` in the same packet section.
- Replace substring checks for D-04/D-05/D-06 with explicit verdict parsing: require `Verdict: defer-with-blocker` unless a dedicated “Explicit user instruction” field contains a concrete citation.
- Parse ledger table rows for status values instead of checking global text. Fail any row whose status is `FIX_APPLIED` at Phase 32 closeout.
- In Plan 32-01, record the dirty-doc baseline as the first write to `32-VERIFICATION.md`, or specify an exact command block whose output must be pasted before any other artifact edit.

## Overall Risk

**MEDIUM.** The plan set is directionally strong and likely to complete Phase 32, but the artifact ownership and validation weaknesses could undermine STOP discipline or create closeout ambiguity if not tightened before execution.

---

## claude Review

_claude failed: hung to the 240s watchdog and was killed (exit 143); 0 bytes stdout and stderr. command: ccp pro --model claude-opus-4-8 -p -_

---

## cursor Review

## Summary

The Phase 32 plan set is strong overall: it preserves the evidence-first workflow, keeps framework/spec edits out of scope, and handles D-04/D-05/D-06 conservatively. The main risks are in verification robustness and execution hygiene, not in the phase decomposition.

## Strengths

- The four-plan dependency chain is sensible: machinery, adjudicable headline packets, owner-routed packets, then closeout verification.
- The plans repeatedly preserve the key governance constraints: candidate-source-not-authority, no live `pinn/` grounding, no spec edits in Phase 32, and no autonomous semantic defaults for D-04/D-05/D-06.
- The dirty unrelated docs file is explicitly protected, which is important given the starting worktree state.
- The D conflict handling correctly treats v1.5 raw-mass `D ~= 4.6416` as the hard constraint unless a real first-principles contradiction is surfaced.

## Concerns

- **HIGH:** The dirty-doc baseline is not durably captured before Phase 32 artifact writes. `32-01-PLAN.md` computes it before Task 1 but records it only in Task 3, so an executor restart or task handoff can lose the only valid baseline. If missing, the plan stops after artifacts may already have been created, which defeats the guard’s purpose.

- **HIGH:** The `FIX_APPLIED` closeout guard can false-pass terminal rows. `32-04-PLAN.md` allows `| FIX_APPLIED |` whenever the ledger contains the explanatory phrase `FIX_APPLIED is not terminal`, which is also required. That means a real terminal `FIX_APPLIED` row would not fail verification.

- **MEDIUM:** `32-04-PLAN.md` declares only `32-VERIFICATION.md` and `32-ISSUE-LEDGER.md` as modified files, but its tasks allow fixing any incomplete Phase 32-owned artifact. If verification finds a packet/template/README issue, the executor either edits undeclared paths or records a blocker instead of fixing an in-scope problem.

- **MEDIUM:** The live-`pinn/` source-discipline check is too weak. The command only verifies that some `NOT grounding` or `FUT` text exists somewhere if a live-code reference exists somewhere; it does not prove the label is attached to the offending reference or even in the same file/paragraph.

- **MEDIUM:** Gap-file handling depends on knowing whether files were “created by Phase 32,” but the plans do not define a durable baseline for pre-existing `32-GAPS.md` or `.planning/milestones/v1.6-GAPS.md`. If either file exists before execution, closeout could blur old entries with new Phase 32 entries.

- **LOW:** M14’s split handling is conceptually good, but the ledger/status wording should make it unmistakable that `accept-resolution` covers only the structural merge, while bootstrap floor, exact early-stage `C`, lower floor, and reset mechanics remain unresolved downstream details.

## Suggestions

- Create or initialize `32-VERIFICATION.md` first in `32-01-PLAN.md`, and record the dirty-doc baseline before any other artifact write.
- Replace the `FIX_APPLIED` check with a parser that inspects the ledger table’s `Status` column, not a broad substring check.
- Either widen `32-04-PLAN.md` `files_modified` to include all Phase 32 artifacts it may repair, or state that failures outside ledger/verification become blockers handled by a follow-up remediation plan.
- Strengthen the live-code check to inspect each matching file/reference and require nearby `NOT grounding` or `FUT` wording.
- Add an initial gap-file existence/hash baseline, then verify only newly added Phase 32 entries at closeout.

## Overall Risk

**MEDIUM.** The plans are well-scoped and likely achieve the phase goal, but the verification weaknesses could allow a governance artifact to appear closed while preserving invalid lifecycle state or unverifiable dirty-file protection.

---

## claude-glm Review

_claude-glm failed: hung to the 240s watchdog and was killed (exit 143); 0 bytes stdout and stderr. command: ccp glm -p -_

---

## claude-deepseek Review

# Cross-AI Plan Review: Phase 32 — Evidence Framework, Issue Ledger & Conflict Adjudication

## 1. Summary

Phase 32 builds the v1.6 adjudication machinery — evidence-packet protocol, packet template, issue ledger, and five headline conflict packets — before any framework-spec edit may land in Phases 33–35. The four plans are:

| Plan | Purpose |
|------|---------|
| **32-01** | Create protocol (`evidence/README.md`), packet template (`_TEMPLATE.md`), seeded issue ledger (`32-ISSUE-LEDGER.md`), and verification skeleton (`32-VERIFICATION.md`). |
| **32-02** | Author two independently adjudicable packets: the `D = 6.694` conflict and the M14 gradient-clipping structural merge. |
| **32-03** | Author three STOP-safe owner-routed packets for D-04 (causal-training mode), D-05 (`s_min` frame), and D-06 (epsilon strategy) — all `defer-with-blocker` unless explicit owner instruction exists. |
| **32-04** | Run structural verification, closeout checks, forbidden-path guards, and dirty-doc baseline comparison. |

The phase produces process-local artifacts only, never touches framework specs, and is the mandatory gate between the Phase 31 READY-WITH-CAVEATS verdict and the Phase 33–35 contract transcription.

---

## 2. Strengths

1. **STOP-protocol discipline is consistently designed.** Every plan encodes the D-04/D-05/D-06 `defer-with-blocker` fallback; plan 32-03 explicitly forbids autonomous selection of causal-training mode, `s_min` gate frame, or static epsilon. The AGENTS.md step-2 understanding check is referenced before gap creation. This matches the project's most critical governance requirement.

2. **Lockstep ledger/packet update requirement (D-09).** Plans 32-02 and 32-03 both require that ledger rows mirror packet verdict/status changes in the same plan — the same-commit discipline from the v1.5 Phase 25 precedent is preserved. This prevents the common failure mode of out-of-sync ledger and packet states.

3. **Dirty-doc baseline guard.** Plan 32-01 captures a SHA-256 baseline of the pre-existing modified file (`2026-06-20-gsd-review-dispatch-resilience-plan.md`) before any Phase 32 artifact is created; Plan 32-04 compares the closeout hash against that baseline. This is a disciplined approach to preserving unrelated user-owned work.

4. **Wave dependency ordering is correct.** 32-01 (machinery) → 32-02 (low-STOP-risk packets) → 32-03 (high-STOP-risk owner-routed packets) → 32-04 (verification closeout). Wave 2 and 3 both depend on 32-01 but not on each other, which is architecturally sound.

5. **The D-conflict packet's SCOPE-12 guard is explicit.** Plan 32-02 Task 1 requires STOP before any first-principles contradiction can overturn `D ~= 4.6416`, and requires the v1.5 `compute-globals-D.md` precedent be reused rather than re-derived from scratch. This correctly enforces the hard-constraint grounding contract.

6. **Forbidden-path checks span the full protected set.** Plan 32-04 includes `.planning/STATE.md` in the forbidden-path status guard (in addition to the seven framework-spec, read-only report, resolution-doc, and `pinn/` paths), which catches a subtle class of accidental mutation that a narrower check would miss.

---

## 3. Concerns

### HIGH

**H-1: The dirty-doc baseline timing window is fragile (32-01 → 32-04).**

Plan 32-01 Task 1 says: "Before creating any Phase 32 artifact, compute and retain the dirty-doc baseline." Plan 32-04 Task 2 then asserts: "If the baseline is absent, record a blocker instead of treating the pre-existing dirty file as preserved."

The problem: nothing in the plans prevents the executor from creating Phase 32 artifacts *before* capturing the baseline, then capturing the post-edit baseline and passing closeout trivially. The guard relies entirely on executor discipline — there is no structural enforcement that the baseline was captured at the correct time. A single misordered `Write` call defeats the entire guard.

**Recommendation:** Add a structural check in Plan 32-04: the baseline `patch-sha256` must differ from the closeout `patch-sha256` if AND ONLY IF the user has modified the file independently during Phase 32 execution (which the plans already assert should not happen). More practically, require the baseline timestamp to precede all Phase 32 artifact file modification timestamps, or embed the baseline in a pre-artifact commit that the closeout verification references by SHA.

**H-2: No resolution-doc re-delivery check at plan-wave boundaries.**

The 32-RESEARCH.md lists "The resolution doc is re-delivered or line count/hash changes before packet authoring" as a STOP trigger. Plans 32-02 and 32-03 cite specific line ranges from `03-final-resolution.md` (anchored to commit `49fb7958`), but none of the four plans includes a pre-flight check that the doc's byte count or SHA still matches the Phase 31 baseline before using those line ranges to author packets.

If the user re-delivers a corrected resolution doc between waves 1 and 3, the D-04/D-05/D-06 packets could cite stale line ranges that land in wrong sections. The Phase 31 re-check protocol (§6 of `31-READINESS-REPORT.md`) covers this case but Phase 32 plans do not invoke it.

**Recommendation:** Add a resolution-doc hash check at the start of Plans 32-02 and 32-03 (at minimum 32-03, since D-04/D-05/D-06 are the most sensitive to line-range drift). If the hash has changed, STOP and refresh Phase 31 line ranges before proceeding.

### MEDIUM

**M-1: 13 non-headline ledger rows are unowned but declared as covered.**

Plan 32-01 seeds all 18 selected findings in the ledger. The five headline packets (D-04, D-05, D-06, M14, `D = 6.694`) are authored in Plans 32-02/32-03, leaving 13 rows (`B-07`, `B-08`, `M6`, `M7`, `M15`, `M16`, `D5`, `NS-12`, `NS-13`, `NS-18`, `adaptive stage assignment`, `L_max / tau_L`, `ALM mu_p clamp`) in `PENDING` with verdict `-` and no evidence packet path.

This matches the stated split-reading precedent (D-08: "remaining packets may be authored by owning contract phases immediately before their edits"), but creates a coverage gap: Phase 32 closes with 13/18 rows unadjudicated, and there is no plan-level check that verifies Phase 33–35 plans actually reference the ledger rows they own. A contract phase could transcribe a spec edit without ever creating its evidence packet, and no verification catches this.

**Recommendation:** Add a closeout note in 32-VERIFICATION.md listing which downstream phase owns each of the 13 unadjudicated rows, and add a forward-reference requirement that each contract phase (33–35) must verify its owned ledger rows are `VERIFIED` or `DEFERRED` before its own phase-exit.

**M-2: The M14 packet's "structural merge" vs. "execution details" split (D-07) has no definition of the boundary.**

Plan 32-02 Task 2 says Phase 32 can lock the structural merge (`clip_value = C_stage * median(recent global gradient norms)`) while deferring "bootstrap floor, exact early-stage `C`, lower floor, and history-reset mechanics" to downstream/FUT. But the plan does not enumerate *which* of these are genuinely source-silent vs. which have partial grounding in the resolution doc or current specs.

For example, the resolution doc §1.8 (lines 52–55) explicitly says the PINN's fixed `5.0` "becomes the Stage-2/3 instance or fallback" and that `7–10 / 5 / 3` is the CTL schedule. Is "exact early-stage `C`" (stages 0–1 at 7–10 range) source-silent, or is the 7–10 range itself a grounded convention? The packet author will need to make this call, and the plan doesn't provide criteria.

**Recommendation:** Add a brief decision guide in 32-02 Task 2's `<action>`: treat any numeric constant as grounded only if it appears in the current framework spec, the resolution doc's `accepted` or `modified` disposition with canonical-source basis, or a v1.5-verified fact; otherwise classify as `defer-with-blocker`.

**M-3: The plan count boundary check has a contradiction.**

The 32-CONTEXT.md D-11 says "No `32-*-PLAN.md` should exist at the end of this run." Plan 32-01 Task 1 says "Do not create `32-*-PLAN.md`" and its verification check (the old spec/discussion boundary check #6) asserts `find ... -name '32-*-PLAN.md'` returns nothing. But Plans 32-01 through 32-04 *are* `32-*-PLAN.md` files that are expected to exist during execution — the prohibition was written for the spec/discussion phase boundary (before planning started), not for the plan-execution phase. Plan 32-04 Task 2 correctly replaces this with a closeout check that exactly four expected plan files exist, but the earlier plan text and verification still carry the contradictory prohibition language.

This is a presentation artefact, not an execution bug, but could confuse a strict executor.

**Recommendation:** Strip the D-11 / old-boundary prohibition language from the executable plans and let Plan 32-04's closeout check (exactly four expected plan files, no extras) be the sole authority.

### LOW

**L-1: `git status --short --` uses whole-worktree paths for forbidden checks, but the dirty-doc baseline check uses a single file.**

Plan 32-04's closeout runs `git status --short --` over protected paths with a `test -z` assertion. If the worktree has other unrelated dirty files (e.g., an untracked file under `pinn/` from a parallel trainex session), the check fails and blocks closeout — even though Phase 32 didn't create or touch it. The plans acknowledge that whole-worktree diff output is not used to judge Phase 32 ownership, but the `test -z` assertion over protected *directories* (`pinn/`) catches untracked files, which could be false positives.

**Recommendation:** The closeout check for `pinn/` should distinguish modified/tracked files (Phase 32's responsibility) from untracked files (which may belong to other sessions). Use `git diff --name-only` for tracked changes + `git ls-files --others --exclude-standard` for untracked files under `pinn/`, and log (rather than fail on) untracked files that predate Phase 32.

**L-2: Template section names hardcoded in the Python verification script could drift.**

Plans 32-01 and 32-04 use Python one-liners that check for exact heading strings like `## Header`, `## Source Positions`, etc. If the `_TEMPLATE.md` is adapted and a section heading is reworded, the verification breaks silently because the template's required sections changed but the check was not updated.

**Recommendation:** Add a comment in `_TEMPLATE.md` noting that section heading changes must be synchronized with the verification checks in `32-VERIFICATION.md` and `32-RESEARCH.md`.

---

## 4. Suggestions

1. **Add a resolution-doc integrity pre-flight to Plans 32-02 and 32-03.** A single `python3 -c "import hashlib; print(hashlib.sha256(Path('.../03-final-resolution.md').read_bytes()).hexdigest())"` against the Phase 31 recorded hash prevents stale-citation packets.

2. **Add a ledger forward-reference completeness check to Plan 32-04.** After closeout, verify that every non-headline ledger row has an `Owner Phase` column that names exactly one of Phase 33, 34, 35, or 36. If any row has no owner or an ambiguous owner, flag it as a blocker.

3. **Add a "citation freshness" check to Plan 32-04.** For each of the five headline packets, verify the cited `03-final-resolution.md` line range actually lands in the expected section (e.g., `sed -n '24,27p' ...03-final-resolution.md` should contain `### 1.1 Causal-training mode`). This is a cheap sanity check against line-range drift.

4. **Make the dirty-doc baseline timing auditable.** In Plan 32-01 Task 1, after capturing the baseline, immediately write a sentinel file (e.g., `.planning/phases/32-.../32-BASELINE-CAPTURED`) with the baseline values and a timestamp. Plan 32-04 can then verify that all Phase 32 artifact files have modification timestamps after the sentinel's timestamp.

5. **Add an explicit "no committed Phase 32 plan files before Plan 32-01" check.** The old D-11 boundary prohibition should be converted into a Plan 32-01 pre-flight: confirm that no `32-*-PLAN.md` files are *already committed* (they should only exist as the executor's working copies), to catch cross-session contamination.

---

## 5. Overall Risk: **LOW**

The plans are unusually thorough for a process-artifact phase. The STOP protocol is correctly encoded at every decision point, the v1.5 Phase 25 precedent is faithfully adapted, and the five headline packets have clear adjudication strategies with explicit fallback routes. The primary risks are operational rather than design-level: the dirty-doc baseline timing window (H-1) and the missing resolution-doc re-delivery check (H-2) are both fixable with small additions to the plan task lists. The 13 unadjudicated ledger rows (M-1) are an intentional design choice with a documented precedent, not an oversight, though the forward-reference to owning phases could be more explicit.

The phase goal — stand up adjudication machinery and record root-cause evidence for the five headline conflicts without touching framework specs — is achievable with the four plans as written. The concerns above would make the execution more robust to timing issues and cross-phase coordination but do not threaten the fundamental architecture.

---

## claude-minimax Review

_claude-minimax failed: returned "Prompt is too long" — the ~37K-token prompt exceeded the M3 context window. Not transient; a plain retry recurs._

---

## Consensus Summary

Consensus across the successful reviewers was that the four-plan Phase 32 structure was sound: the evidence machinery comes first, the adjudicable headline packets are separated from owner-routed decisions, D-04/D-05/D-06 avoid autonomous semantic defaults, and Phase 32 preserves the no-framework-spec-edit boundary. Multiple reviewers also identified the same execution-hygiene risks: STOP-only gap files needed conditional handling, summary outputs needed explicit ownership/verification, dirty-doc baseline capture needed to be auditable, resolution-doc citation freshness needed a guard, and ledger/`FIX_APPLIED` checks needed row-level parsing rather than broad substring checks.

Those shared concerns were incorporated before execution in commit `ab5f6eae` (`plan(32): incorporate review feedback`), which updated the Phase 32 plans and validation artifact. The completed closeout then added the explicit deferred gap records (`GAP-32-01` through `GAP-32-03`), clarified the ledger `Owner Phase` column, and captured this review artifact.

Reviewer availability note: `claude` and `claude-glm` produced no output after the watchdog killed the commands; `claude-minimax` failed deterministically because the prompt exceeded its context window. Those failures are recorded as tool/runtime limitations, not model verdicts.
