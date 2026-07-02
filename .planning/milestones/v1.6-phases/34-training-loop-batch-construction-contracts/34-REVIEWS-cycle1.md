---
phase: 34
reviewers: [codex, opencode, claude, claude-minimax, claude-jiekou]
rerun_reviewers: [codex, opencode, claude, claude-minimax, claude-jiekou]
reviewed_at: 2026-06-25T03:25:10Z
generated_by: xreview
xreview_run_dir: /var/folders/kx/gq3tx75x04jf50z_d17fn1yc0000gn/T/xreview-20260625T032106Z-17770
---

# Cross-AI Plan Review — Phase 34

## codex Review

## 1. Summary

The Phase 34 plans are broadly executable and well-scoped for specwork. They cover LOOP-01..08 plus SI-PINN-003, preserve the no-live-code boundary, and include strong evidence-before-edit and final verification sequencing.

Main residual risk is not scope creep; it is execution semantics around deferred/owner-pending work and whether the final checks are strict enough to prove the single-canonical-home invariants.

## 2. Strengths

- Clear dependency shape: 34-01 creates evidence/ledger groundwork; 34-02/03/04 perform scoped spec edits; 34-05 verifies and closes ledger rows.
- Strong source discipline: the plans repeatedly avoid inventing source-silent policies and route GAP-34-01 through STOP handling.
- Scope boundaries are explicit: no `pinn/` live-code edits, no EDA/training/Stage-0 pilot, no frozen/read-only report edits.
- Good data-integrity guards: ledger freshness SHA, dirty-doc preservation, forbidden-path checks, and `.planning/STATE.md` protection are all planned.
- LOOP-04 receives appropriate special handling for cross-file canonical homes, `8.5` rejection, and re-verification after adjacent edits.

## 3. Concerns Tagged HIGH / MEDIUM / LOW

**HIGH:** None identified.

**MEDIUM:** Plan 34-05 is marked `autonomous: true` / `user_setup: []`, but also says Phase 34 closure is gated on user resolving or deferring OPEN `GAP-34-01`. That is correct under AGENTS.md, but it creates an execution ambiguity: an autonomous runner can produce artifacts and ledger updates, yet the phase still cannot close. This should be surfaced as an expected manual closure gate, not only inside verification text.

**MEDIUM:** LOOP-04 exactness is under-enforced by some automated checks. The spec requires the mechanism formula exactly once in `pinn_architecture.md` and zero times in `ctl_instruction.md`, with no duplicated schedule/value text. Plan 34-05’s command checks `pinn.count('clip_value = C_stage') >= 1`, not `== 1`, and is not section-scoped. Manual judgment is mentioned, but the automated gate could pass duplicate normative text.

**MEDIUM:** Ledger semantics for deferred findings are potentially confusing. The Phase 32 ledger header says closure is `VERIFIED` after an acceptance check, or `DEFERRED` with a written blocker and `defer-with-blocker` verdict. Plan 34-05 intentionally marks M16 and ALM as `VERIFIED` while preserving `defer-with-blocker`. That may be reasonable as “verified transcription of a deferral,” but downstream consumers that key only on `Status` could miss active blockers.

**LOW:** The plans depend on corrected 34-SPEC/RESEARCH over older ROADMAP/REQUIREMENTS preview wording for LOOP-03/04/06. The plans document this, but future executors reading broad context could still be confused by superseded `8.5`, “both sets,” or `n_col` formula language.

## 4. Suggestions

- Add a top-level note to 34-05 that execution is autonomous only up to “verification complete / closure blocked,” and list GAP-34-01 resolution or explicit deferral as required user input before phase closure.
- Strengthen LOOP-04 checks with section extraction and exact counts: formula exactly once in pinn §4.4, zero in ctl; `7-10` exactly once in ctl schedule; pointer-only in the non-canonical location.
- For M16/ALM, either use `DEFERRED` terminal status or add explicit ledger/header verification that `VERIFIED + defer-with-blocker` means “deferral transcription verified, downstream blocker still active.”
- Add a brief “superseded roadmap wording” warning near each relevant plan’s Source Audit to prevent accidental reversion to pre-adjudication criteria.

## 5. Overall Risk

**MEDIUM.** The plans are strong on scope and grounding, but the open STOP gap, LOOP-04 exactness checks, and deferred-row ledger semantics should be tightened before execution if the goal is unambiguous autonomous closeout.

---

## opencode Review

Now I have all the information needed. Here is my review:

---

## Cross-AI Plan Review: Phase 34 — Training-Loop & Batch-Construction Contracts

### 1. Summary

5 plans (34-01 through 34-05) executing 9 requirements (LOOP-01..08 + SI-PINN-003) as deterministic specwork — evidence packets first, then spec edits to `ctl_instruction.md` and `pinn_architecture.md`, then final verification + ledger closure. The plans are exceptionally well-governed with rigorous attention to the STOP protocol, source hierarchy, and anti-duplication discipline. The primary execution risk is a missing dependency file that all plans load.

### 2. Strengths

- **Rigorous packet-before-edit sequencing** (D-34-10): B-07/B-08/M16/ALM packets authored in W1 before any spec edit in subsequent waves.
- **Anti-duplication guardrail** (D-34-04/05/06): single canonical home per value/formula + stable-anchor cross-reference + no-duplication verifier — directly addresses the SI-PINN-003 root cause rather than just patching symptoms.
- **Re-verify-after-every-batch** on LOOP-04 cross-file invariants (c)/(d)/(e) — enforced in 34-02 Task 3, 34-03 Task 4, 34-04 Task 3.
- **Scope guards throughout**: each plan's `files_modified` frontmatter, per-task `git diff --name-only` checks, and the final forbidden-path guard over tracked *and untracked* files.
- **Ledger concurrency guard** (34-05 Task 2): SHA-256 freshness check before writing — prevents silent overwrite of concurrent edits.
- **Dynamic dirty-doc baseline** in `34-BASELINE-CAPTURED` using SHA-256 of `git diff` output, with per-path hashes, rather than hardcoded filenames.
- **GAP-34-01 explicitly gates phase closure** — not marked complete over an unresolved STOP gap.

### 3. Concerns

**HIGH**

1. **`34-VALIDATION.md` does not exist** but is loaded in `<context>` by all 5 plans (34-01 line 94, 34-02 line 82, 34-03 line 99, 34-04 line 77, 34-05 line 102). If the GSD executor treats `@file` references as read-before-run requirements, every plan will error immediately. 34-05 Task 1 also states "Run and record PASS/FAIL for the FULL `34-VALIDATION.md` structural check set" — but without this file, the set is undefined. The RESEARCH.md and SPEC.md embed equivalent checks inline, so the plans are technically self-contained, but the cross-file dependency is unresolved and creates ambiguity about the canonical check-list.

**MEDIUM**

2. **ROADMAP success criteria conflict with the adjudicated SPEC** in 3 places (LOOP-03 line 187: "applied to **both** point sets"; LOOP-04 line 188: "stages 0–1: **8.5**"; LOOP-06 line 189: "`n_col ∝ dt_base / dt_out` verbatim direction"). The plans correctly follow the SPEC + resolution doc, but the stale ROADMAP text creates a cross-phase governance risk: a Phase-36 verifier reading only the ROADMAP would conclude Phase 34 failed. The plans flag this as a finding (34-RESEARCH.md:500–511) but do not reconcile it beyond noting "transcribe the SPEC, not these lines." This should be surfaced to the user or a Phase-36 pre-reconciliation item.

3. **`34-RESEARCH.md` is in the 34-01 Task 3 allowed-changed set** at line 242 (verify step's `allowed` set includes RESEARCH.md), but `34-01-PLAN.md` frontmatter `files_modified` does NOT list it. This is a scope guard mismatch — RESEARCH.md should be in the forbidden/protected set, not allowed. Low practical risk (the executor shouldn't touch it), but if a stray edit occurred it would pass the guard undetected.

**LOW**

4. **D-34-15 ordering-skeleton insertion point is underspecified.** 34-03 Task 2 says "AUGMENT the existing Total-Loss / Data-Flow section" and "do NOT create a new separate subsection" but does not state whether the ordering skeleton goes before, after, or replaces the existing text in that section. The section currently spans ~1685-1745 and includes a pseudo-ALM rejection at ~1745. An executor could make a reasonable but non-deterministic placement choice, and the verification checks (positive token asserts only) would not catch a misplaced skeleton.

5. **34-01 Task 2/3 action descriptions truncated** (each ends with "line truncated to 2000 chars"). The full instructions for authoring four evidence packets and synchronizing the ledger may not be fully visible in a single tool read — the executor must scroll through the full file. This is a plan-navigation ergonomic concern, not a correctness issue.

### 4. Suggestions

- **Create `34-VALIDATION.md` before execution begins** — or remove it from all `<context>` load lists and annotate 34-05 Task 1 to use the inline checks from RESEARCH.md. Either way, resolve the dangling reference.
- **Surface the ROADMAP staleness to the user as a pre-verification item.** The research finding (34-RESEARCH.md:500–511) is thorough — the user just needs to know it blocks Phase-36 handoff unless the ROADMAP is reconciled. Recommend a brief finding note in `34-VERIFICATION.md`.
- **Tighten the 34-01 Task 3 scope guard** to exclude `34-RESEARCH.md` from the `allowed` set, matching the `files_modified` frontmatter.
- **For 34-03 Task 2, add one sentence specifying the insertion anchor**: e.g. "insert the ordering skeleton immediately after the existing '4-step per-training-step flow' at ~1716, before the Loss Function Formulation subsection" — or just "append as the second paragraph of the Data Flow section" — to make placement deterministic.

### 5. Overall Risk: **LOW**

Assuming `34-VALIDATION.md` is created or the cross-file references are removed, the plans are sound. The governance is the strongest I have seen in these phases — the anti-duplication guardrail, ledger concurrency check, re-verify-after-every-batch loop, and GAP-34-01 closure gate all demonstrate mature understanding of the failure modes. The ROADMAP staleness is the only significant unresolved governance issue, but it is disclosed, not hidden.

---

## claude Review

## Phase 34 Plan Review

### 1. Summary
Five sequential plans (waves 1–5) transcribe the training-loop/batch-construction contracts (LOOP-01..08 + SI-PINN-003) into `ctl_instruction.md` and `pinn_architecture.md` at their adjudicated verdict+status, then verify and close the Phase-32 ledger rows. The plans are unusually rigorous: packet-before-edit grounding, single-canonical-home discipline for LOOP-04, STOP-gap routing for source-silent edge cases, dynamic dirty-doc/STATE.md preservation, and per-batch re-verification of cross-file invariants. The structure faithfully serves the SPEC and the v1.6 STOP-protocol governance. The main issue is a literal contradiction between one task's authoring instruction and its own verification gate.

### 2. Strengths
- **Goal coverage is complete and traceable:** all 9 requirements map to authoring + verification tasks; Source Audit tables and AC-ID reservations (no new schema minted) are consistent across plans.
- **Governance fidelity:** source-silent batch edge cases are routed to `GAP-34-01` (OPEN, full STOP fields, closure-gated) rather than invented — exactly the directive in AGENTS.md. M14-deferred constants correctly distinguished as *source-routed* (body-deferred, not a gap).
- **Concurrency/integrity engineering:** dynamic dirty-doc capture (no hardcoded `STATE.md`), `ledger_post_34_01_sha256` pre-write freshness guard, tracked+untracked forbidden-path guards. Strong for a repo with known concurrent sessions.
- **Anti-duplication (no second SI-PINN-003):** mechanism canonical in pinn §4.4, C-schedule canonical in ctl, bidirectional `AC-LOOP-04` anchors, with a recoverable "one coherent rule, zero duplicated text" win condition.
- **Dependency ordering is sound:** 34-01→02→03→04→05 is strictly sequential; the two spec files are never edited concurrently within a wave.

### 3. Concerns

**HIGH — 34-02 Task 2 action contradicts its own verify.** The authoring instruction tells the executor to write, in `ctl_instruction.md`, "*the mechanism `clip_value = C_stage · median(...)` is defined there*" — i.e. it literally includes the string `clip_value = C_stage`. The same task's verify asserts `'clip_value = C_stage' not in ctl` (and 34-03/34-04/34-05 re-assert this). I confirmed the string is currently absent from ctl, so a faithful executor following the action verbatim introduces the forbidden token and fails the gate (or is forced to silently deviate). Fix: instruct the cross-reference to name the mechanism *without* reproducing the formula literal (e.g. "the `C_stage·median` mechanism defined in §4.4 (AC-LOOP-04)").

**MEDIUM — `8.5` negative check is a bare substring (`'8.5' not in file`).** Safe today (I verified no incidental `8.5`/`18.5` in either file), but any future value containing `8.5` as a substring (`18.5`, `8.50`) would trip all four plans' guards. Low present risk, but the check should be word-boundary anchored to be durable.

**MEDIUM — dash-encoding inconsistency for the C-schedule.** The two current ctl locations use different encodings: `7--10` (prose ~1796) and `7-10` (table ~1911). Most checks correctly guard with `('7-10' in ctl) or ('7--10' in ctl)` or a dual `findall` count, but the SPEC/must-have prose asserts a literal "`7-10 / 5 / 3`". Ensure the retained canonical copy uses one consistent rendering; the count==1 collapse check is otherwise correct.

**LOW — scope guards weaken under per-plan commit cadence.** Several guards use `git diff --name-only HEAD` (or no-HEAD unstaged) over `pinn_instruction/`. If each wave commits, later waves' guards see only the current wave's uncommitted delta, so the "only two files changed across the phase" claim is enforced per-plan, not cumulatively. Acceptable, but the phase-wide invariant relies on 34-05's read-of-file-contents checks, not the diff guards.

**LOW — STATE.md preservation handles dirty→clean but not dirty→further-dirty.** Given concurrent sessions, the user could further modify `STATE.md` mid-execution; only the dirty→clean tracking-write divergence is documented as a non-violation. A second user edit would fail the hash check without a recorded escape. Minor, and arguably correct to surface.

### 4. Suggestions
- Reword 34-02 Task 2's cross-reference instruction to drop the literal `clip_value = C_stage` formula from ctl, resolving the HIGH contradiction; mirror the phrasing already used correctly in 34-03 Task 2 ("cross-reference … NOT restate the formula").
- Convert `'8.5' not in` and similar bare-substring negatives to anchored regex (`\b8\.5\b`) for durability.
- Verify the `5 / 3` portions of the C-schedule explicitly (current checks lean on `7-10` and `5.0` only).
- Optionally have 34-05's forbidden-path guard diff against the phase base commit, not `HEAD`, to assert the cumulative two-file invariant.

### 5. Overall Risk: **MEDIUM**
The plans are well-grounded and achieve the phase goal, but the 34-02 Task 2 action/verify contradiction is a concrete blocker that will surface during autonomous execution and should be corrected before the wave runs. The remaining items are brittleness hardening, not design faults.

---

## claude-minimax Review

# Cross-AI Plan Review: Phase 34 — Training-Loop & Batch-Construction Contracts

**Reviewer:** Independent review pass on the 5-plan Phase 34 set (34-01..34-05) + SPEC + CONTEXT, against `.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md`, AGENTS.md, and the Phase 32 ledger/packet corpus.
**Worktree:** `milestone/v1.6`; `STATE.md` dirty (user-owned, per D-34-18).
**Files read:** all 8 listed phase artifacts + git state. No files failed to read.

---

## 1. Summary

Phase 34's plan set is unusually disciplined for specwork: it inherits the Phase-33 blockquote-callout convention, the packet-before-edit rule (D-34-10), the single-canonical-home-per-half rule (D-34-04/05/06), and the re-verify-after-every-batch rule (ROADMAP). The SPEC is the result of two prompt-level corrections (LOOP-04 8.5 canonization and LOOP-06 M16 transcription), and the plans correctly enforce the post-correction verdicts at the source-token level. The wave structure (1→2→3→4→5) is conservative but executable. Phase goal is achievable.

The 9 requirement IDs (LOOP-01..08 + SI-PINN-003) appear across the plan set's `requirements` fields: LOOP-04 in 34-02; LOOP-01/02/03/06/07/08 in 34-03; SI-PINN-003 + LOOP-05 in 34-04; all 9 re-verified in 34-05. The packet-before-edit mandate is satisfied for B-07/B-08/M16/ALM in 34-01 (D-34-10/11), with M14 reused (D-34-12) and LOOP-07/08 carried forward as v1.5 with no packet (D-34-13). The source-silent batch edge cases are routed to GAP-34-01 rather than fabricated (D-34-16a), and phase closure is explicitly gated on the user resolving or deferring it (D-34-22 mitigation in 34-05 Task 3).

## 2. Strengths

- **Packet-before-edit discipline (HIGH value).** 34-01 Task 3 sets the four LOOP rows to `IN_PROGRESS` only after the packets exist and the ledger link is written, with `ledger_post_34_01_sha256` recorded for the Phase-36 freshness guard. This is the exact pattern that prevented the LOOP-04 8.5 trap from re-occurring.
- **Single canonical home per half (HIGH value).** 34-02 and 34-04 enforce "mechanism one home in pinn §4.4, schedule one home in ctl, the other carries a pointer" via the (a)-(e) cross-file suite with discriminating exact-phrase checks (e.g., `clip_value = C_stage` `>= 1` in pinn, `not in` ctl; `7-10` regex exactly once in ctl). The Consolidated Hyperparameter table copy is explicitly collapsed to a pointer, not a second normative copy — this is the discipline that prevents the second SI-PINN-003.
- **Re-verify after every batch.** 34-02 Task 3, 34-03 Task 4, 34-04 Task 3 each re-run the (a)-(e) suite + locked-convention guard after their batch. The ROADMAP's re-verify-after-every-batch is operationalized.
- **Discriminating exact-phrase checks.** Verifies assert tokens that did NOT exist pre-Phase-34 (`Phase 34 contract`, `AC-LOOP-04`, `B_replay`, `realized-as-deferred`, `RESOLVED` in SI-PINN-003 log), so the suite would fail against pre-Phase-34 content — this defeats token-level no-op edits.
- **Dynamic dirty-doc capture (D-34-18).** 34-01 Task 1 captures the dirty-doc set dynamically (not by hardcoding `STATE.md`) using `git diff --name-only`, with a per-path SHA-256 plus a combined `dirty_docs_sha256` — preserves the user-owned modification without naming it.
- **Concurrency guard (HIGH value).** 34-05 Task 2 refuses to overwrite the ledger if the SHA-256 has drifted from `ledger_post_34_01_sha256`. Halts rather than overwriting concurrent agent work.
- **Verdict + status + citation discipline.** Every transcribed contract carries an explicit status tag (locked/provisional/deferred/owner-pending) and a source citation (resolution-doc §1.x, packet, M14 GAP-08). No invented locks.
- **GAP-34-01 is a closure blocker, not silent override.** 34-05 Task 3 explicitly records that Phase-34 closure is gated on the user resolving or deferring GAP-34-01, citing AGENTS.md. This is the correct STOP-protocol behavior.
- **Protected-path guard is tight.** 34-05 checks BOTH tracked changes AND `git ls-files --others` over the SCOPE-08/09/13 + `pinn/` pathset, so a freshly created `pinn/` file cannot slip past.
- **Verdict preservation on closure.** B-07/B-08/M14 keep `accept-resolution`; M16/ALM keep `defer-with-blocker`. No re-litigation. The reserved AC IDs (AC-LOOP-01/02/04/05/06) are reused; no new status enum is minted (process-artifact-schema reuse per AGENTS.md).

## 3. Concerns

### HIGH

- **34-05 Task 1 dirty-doc relaxation is loose.** The verify allows the `dirty_docs_sha256` to mismatch if `34-VERIFICATION.md` records "divergence" and contains `STATE.md`. There is no per-path check to confirm STATE.md content is byte-for-byte unchanged vs the user-owned pre-edit state — only a hash over the captured set and a textual mention in the report. A real (non-tracking) edit to STATE.md could pass if the report also documents it. Recommend: re-derive per-path SHA-256 of STATE.md at verification time, compare against the per-path hash recorded in 34-BASELINE-CAPTURED, and explicitly require "per-path STATE.md hash unchanged" as a separate PASS criterion. The 33-VERIFICATION precedent is referenced but not enforced.

### MEDIUM

- **34-04 wave assignment is over-conservative.** Plan 34-04 modifies only `pinn_architecture.md` and depends on the B-08 and ALM packets (created in 34-01). It does not depend on 34-03's `ctl_instruction.md` edits. The `depends_on: [34-02, 34-03]` declaration means 34-04 cannot run until 34-03 completes; this is safe but unnecessarily serial. Not wrong, just slower than needed.
- **34-01 Task 3 scope-guard allowed-set logic is brittle.** The `set | {p for p in changed if p.startswith('.planning/phases/34-training-loop-batch-construction-contracts/34-0') and p.endswith('-PLAN.md')}` pattern duplicates the explicit allowlist below it and could miss sibling artifacts (e.g., a new evidence sub-folder). A positive allowlist would be more robust than the negative check + exception.
- **34-03 LOOP-07/08 gap-opening guidance is open-ended.** Plan 34-03 Task 3 says: "if the source is SILENT on a specific training-side role ... record a 34-GAPS.md STOP gap." If multiple roles are silent, multiple gaps could open without a single "halt and surface" threshold. The plan works for the known-good case (3 v1.5 roles already established per D-34-14) but lacks a worst-case branch.
- **No automation-level fallback if GAP-34-01 reveals sub-gaps.** 34-03 Task 1 opens GAP-34-01 as a single gap covering three edge cases (final-stage, undersized, replacement). If during 34-05 verification any of the three is observed to actually need its own decision, there is no template or guidance for splitting it into a GAP-34-01a/b/c. Recommend: a one-paragraph "sub-gap split" precedent in 34-05 Task 3 or in 34-GAPS.md.
- **34-05 Task 1 forbidden-path guard scope check has a small coverage hole.** The guard checks `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md` but the file name in some paths could be `data-quality-assessment.md` (dash) — verify the actual file name in the repo before relying on this exact path string. (Could not confirm without filesystem access; the path appears correct in current usage but should be sanity-checked at execution time.)
- **The "UI gate false positive is ignored" line appears in every plan's `must_haves.truths`.** It is harmless but template noise; it implies the UI gate fires here. Consider a one-line project-wide note that v1.6 specwork never trips the UI gate, instead of repeating it 5 times.

### LOW

- **34-02 anchor format for `AC-LOOP-04` is not specified.** The plans require the anchor to be present in both files but don't fix the format (e.g., HTML comment `<!-- AC-LOOP-04 -->` vs heading text vs fenced label). The exact-phrase check accepts any of these. Pick one in the plan to make the check deterministic for future phases.
- **STRIDE T-34-SC "package installs" threat is repeated in every plan with `accept` disposition.** This is template noise; the threat doesn't apply. Could be removed from all 5 plans' threat models.
- **34-02's C-schedule regex `r'7\s*-\s*10'` could match a date range or non-schedule use of "7-10".** In practice, ctl_instruction.md uses "7-10" only for the schedule, so this is fine — but a more specific anchor (e.g., the exact line in the canonical section) would be more robust.
- **34-01's `34-BASELINE-CAPTURED` is modified twice (Task 1 captures hashes, Task 3 appends `ledger_post_34_01_sha256`).** The two-write pattern is correct but the file is also referenced by name in many later verify commands. A "single write at end of 34-01" pattern would reduce read-then-write races if 34-01 is partially run.

## 4. Suggestions

1. **Tighten 34-05 Task 1's STATE.md preservation check** to per-path SHA-256 comparison against the per-path hash recorded in 34-BASELINE-CAPTURED. Drop the textual-divergence relaxation in favor of: "STATE.md byte-unchanged OR recorded as a delegated tracking write (whitelisted path with documented user-tool action)". This makes the guard enforceable by a single `git diff` hash check rather than narrative documentation.
2. **Parallelize 34-04 with 34-03 in the wave declaration** (change 34-04 `depends_on: [34-02, 34-03]` to `[34-02]`). 34-04 only depends on the B-08 and ALM packets (Wave 1) and the locked pinn §4.4 region (Wave 2); the 34-03 ctl edits are not required for 34-04's pinn-only scope. This halves the wall-clock for the spec-edit phase with no semantic risk.
3. **Pick a fixed `AC-LOOP-04` anchor format** (suggest a single inline token like `<a id="ac-loop-04"></a>` or a fenced `> **AC-LOOP-04**` callout) and write the format into 34-02 Task 1's `action` block, so the exact-phrase check `AC-LOOP-04 in pinn` is a single token match with no false positives.
4. **Add a "split sub-gap" precedent** to 34-05 Task 3 (or to the 34-GAPS.md template header) covering what to do if verification reveals GAP-34-01 is actually 2-3 distinct decisions. Three sentences is enough.
5. **Refactor 34-01 Task 3's scope-guard to a positive allowlist** of Phase-34-owned paths. Drop the dynamic `dirty | {p for p in changed if ...}` exception logic — replace with a single explicit set.
6. **In 34-05 Task 1, add a pre-verify check that `34-GAPS.md` exists and is OPEN** (mirrors the GAP-34-01 STOP-completeness check in Task 3 but as a precondition for ledger closure in Task 2, not just a post-verification recording). This is a one-liner that catches the case where Plan 34-03's gap-writing was somehow skipped.
7. **Remove the per-plan "UI gate false positive" truth** in favor of a single global note in 34-SPEC.md or 34-CONTEXT.md that v1.6 specwork is not in scope for UI gate checks. Reduces noise and keeps the must_haves field focused on phase-specific truths.
8. **Make the `re.search(r'n_col\s*=\s*', ctl)` LOOP-06 negative check also probe a few specific candidates** that an executor might write (`n_col = `, `n_collocation = `, `collocation_count = `) to reduce the risk of a synonym sneaking through.

## 5. Overall Risk

**MEDIUM** — driven entirely by the HIGH concern (34-05 dirty-doc relaxation) and the MEDIUM concerns around sub-gap handling and over-conservative sequencing. The packet-before-edit discipline, single-canonical-home enforcement, re-verify-after-every-batch, and forbidden-path guards are strong. The phase goal is achievable and the source-token checks are well-designed. The main residual risk is governance/coordination: the dirty-doc STATE.md check and the GAP-34-01 split-precedent gap are the two places where the plans rely on narrative documentation rather than deterministic guards.

Recommend addressing the HIGH concern and the 34-04 wave parallelism before execution starts; the rest can be deferred to post-execution review.

---

## claude-jiekou Review

There's an issue with the selected model (opus-4-8-r). It may not exist or you may not have access to it. Run --model to pick a different model.

---

## Consensus Summary
_Synthesize shared concerns across reviewers above (2+ agreement = highest priority)._

## xreview Diagnostics

### codex
- reviewer=codex
- exit_code=0
- elapsed_seconds=243
- timeout_seconds=360
- watchdog=not_triggered
- command=codex exec --ephemeral --dangerously-bypass-hook-trust --model gpt-5.5 -c model_reasoning_effort=\"xhigh\" --skip-git-repo-check - 
- stdout_bytes=3888
- stderr_bytes=469070

### opencode
- reviewer=opencode
- exit_code=0
- elapsed_seconds=65
- timeout_seconds=360
- watchdog=not_triggered
- command=opencode run - 
- stdout_bytes=5887
- stderr_bytes=1087

### claude
- reviewer=claude
- exit_code=0
- elapsed_seconds=121
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp pro --model claude-opus-4-8 -p - 
- stdout_bytes=5171
- stderr_bytes=0

### claude-minimax
- reviewer=claude-minimax
- exit_code=0
- elapsed_seconds=135
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp claude-minimax -p - 
- stdout_bytes=11812
- stderr_bytes=192

### claude-jiekou
- reviewer=claude-jiekou
- exit_code=1
- elapsed_seconds=10
- timeout_seconds=360
- watchdog=not_triggered
- command=ccp claude-jiekou --model opus-4-8-r -p - 
- stdout_bytes=145
- stderr_bytes=192
