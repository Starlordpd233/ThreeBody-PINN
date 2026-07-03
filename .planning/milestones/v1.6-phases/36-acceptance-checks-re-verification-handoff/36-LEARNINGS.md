---
phase: 36
phase_name: "acceptance-checks-re-verification-handoff"
project: "3-body-problem"
generated: "2026-07-02T10:54:18+00:00"
counts:
  decisions: 6
  lessons: 4
  patterns: 5
  surprises: 3
missing_artifacts: []
---

# Phase 36 Learnings: Acceptance Checks, Re-verification & Handoff

## Decisions

### GAP-36-01 resolved: PKG-05..08 flipped Complete, terminal-anchor rule extended
**What was decided:** `PKG-05`..`PKG-08` were flipped `Pending` → `Complete` in `REQUIREMENTS.md`, anchored on the Phase 30 completion record (ROADMAP progress table, 5/5, 2026-06-18) rather than a Phase 32 ledger row (which doesn't exist for pre-ledger requirement families). The "terminal anchor" definition was explicitly extended to phase-completion records for such families.
**Rationale:** These four flags genuinely contradicted terminal state (Phase 30 was done) but the locked reconciliation rule only recognized ledger rows as anchors; the owner chose to extend the rule rather than leave a satisfied requirement permanently `Pending` or silently invent a completion.
**Source:** 36-GAPS.md GAP-36-01 (RESOLVED-WITH-INSTRUCTION 2026-07-01, via AskUserQuestion)

### GAP-36-02 resolved: LOOP-07/08 flipped Complete, D-36-17 amended
**What was decided:** `LOOP-07` and `LOOP-08` were flipped `Pending` → `Complete`, anchored on `34-VERIFICATION.md`'s SATISFIED/VERIFIED truths (rows 6-7) rather than a ledger row. Rule D-36-17 was amended to read "each flipped flag must match a terminal Phase 32 ledger row **OR** a terminal phase-VERIFICATION record."
**Rationale:** SPEC R6 explicitly named these two as stale flags needing a flip, but the literal ledger-row rule was unsatisfiable for them (Phase 34 deliberately carried them as provisional carry-forwards with no dedicated ledger row); amending the rule text keeps future reconciliation consistent rather than creating a silent one-off exception.
**Source:** 36-GAPS.md GAP-36-02 (RESOLVED-WITH-INSTRUCTION 2026-07-01, via AskUserQuestion)

### SI metadata reconciled by carrying forward prior precedent, not re-litigating
**What was decided:** All four `SI-*` framework-spec metadata IDs were disposed: `SI-CTL-001` and `SI-PINN-003` retire-with-back-reference (already resolved by earlier phases); `SI-PINN-002` and `SI-DQA-003` preserve-with-reason, citing the v1.5 Phase 29 D-08 human-approval precedent and SCOPE-12's locked SCS-gate citation respectively.
**Rationale:** The preserve dispositions are carry-forwards of dispositions already ratified by cross-AI review in v1.5, not freshly invented calls — each carries a written reason and owner rather than a bare status flip.
**Source:** 36-04-SUMMARY.md Task 1/2

### Probe-suite failures were fixed by widening probe patterns only, never the specs
**What was decided:** All 15 initial probe FAILs were resolved by correcting over-strict disposable probe patterns (whitespace tolerance, rejection-context awareness, LaTeX/Unicode variants, a genuine monotonicity-assertion bug fix) — zero edits were made to `ctl_instruction.md` or `pinn_architecture.md` during Phase 36.
**Rationale:** The underlying spec transcriptions from Phases 33/34/35 were already correct; the probes themselves were the defect. This was independently confirmed via `git diff --stat` across the entire Phase 36 commit range showing an empty diff on both spec files.
**Source:** 36-02-SUMMARY.md "Probe-Design Fixes Applied", 36-UAT.md Test #4

### D-05/D-06 ledger rows promoted to VERIFIED citing prior owner verdicts only
**What was decided:** The Phase 32 issue-ledger rows for D-05 and D-06 were promoted `PENDING` → `VERIFIED` after confirming their transcriptions were clean, citing the already-`RESOLVED-WITH-INSTRUCTION` GAP-32-02 (Option A) and GAP-32-03 (dual-context) verdicts as authority — no new verdict was proposed.
**Rationale:** Phase 36's role is closure verification, not re-adjudication; the promotion is a freshness-checked bookkeeping act, not a new decision.
**Source:** 36-03-SUMMARY.md Task 1/2

### Acceptance manifest + disposable probe suite built as the verification spine
**What was decided:** A 26-row acceptance manifest (one row per requirement-family contract, sorted by ID) and a matching 26-script disposable probe suite were built first, with a later companion `AC-TRACEABILITY` probe added to assert exactly 32 v1.6 traceability rows map bijectively to phases.
**Rationale:** Establishes a mechanically re-runnable, evidence-hashed closure gate rather than relying on narrative claims of "done."
**Source:** 36-01-SUMMARY.md, 36-05-SUMMARY.md Task 3

---

## Lessons

### A high initial probe-fail rate needs legitimacy scrutiny, not just a re-run to green
**What was learned:** The suite's initial 15/26 FAIL rate, followed by a commit titled "widen probe patterns" that brought it to 26/26 PASS, is exactly the shape of a suite that could have been loosened to mask a still-wrong spec. Trusting the final green run alone would not have ruled that out.
**Context:** Required an independent verifier to read the actual widening diff and confirm every loosened check still retains a real FAIL path, before accepting the PASS verdict as honest.
**Source:** 36-UAT.md "Verification approach", Test #2

### A probe's own assumption can be the bug, even when the spec is correct
**What was learned:** One probe asserted the gradient-clipping C-schedule must be monotonic by stage, but the actual contract is intentionally non-monotonic (`7-10 → 5 → 3`); the fix was removing the incorrect assertion, not the spec being wrong.
**Context:** A reminder that a failing check is evidence of *some* defect, but not necessarily in the artifact under test — the check itself needs to be validated against the actual contract before trusting its verdict.
**Source:** 36-02-SUMMARY.md item 8, 36-UAT.md Test #2

### A naive substring count and a precise anchored-pattern count can legitimately disagree
**What was learned:** A loose grep for traceability rows counted 33, while the properly anchored family-specific pattern (`^\|\s*(PKG|EVID|CURR|LOOP|LOSS|VER)-\d+\s*\|`) counted the correct 32 — the naive grep also matched an unrelated scope-rule row that merely contained similar-looking text.
**Context:** Confirmed the anchored probe was correct and the discrepancy was a loose-grep artifact, not a probe defect — worth remembering before trusting a quick manual grep over a purpose-built check.
**Source:** 36-UAT.md Test #8

### "Was this closure earned or gamed" is often decisively provable with one cheap check
**What was learned:** The entire "did they weaken the spec to pass" concern for this phase was conclusively settled by a single `git diff --stat` across the whole phase's commit range against just the two framework-spec files — an empty diff proves the fix direction was probe-only regardless of how the probes themselves were changed.
**Context:** A cheap, decisive check is more convincing than re-reading every individual probe fix, and should be reached for first when auditing a suspicious FAIL→PASS transition.
**Source:** 36-UAT.md Test #4

---

## Patterns

### Extend the anchor rule by amendment, not by silent exception
**Pattern:** When a locked reconciliation rule can't cover a real case (e.g. "must match a terminal ledger row" for requirements that never had one), resolve by explicitly amending the rule's text to a broader, still-precise definition — rather than granting a one-off silent exception that leaves the rule's written form inconsistent with actual practice.
**When to use:** Any milestone-closure reconciliation where a locked process rule turns out to be unsatisfiable for a legitimate subset of cases.
**Source:** 36-GAPS.md GAP-36-01/GAP-36-02 resolution notes

### Three-legged closure verification: reproduce, scrutinize the diff, audit scope
**Pattern:** To verify a suspicious "everything now passes" claim, run three independent legs: (1) re-execute the full suite independently into a separate evidence directory to confirm reproducibility, (2) read the actual diff that caused the transition and confirm every loosened check still has a real failure path, (3) audit that no out-of-scope or protected path was touched.
**When to use:** Any closure/handoff phase where a prior FAIL→PASS transition needs independent trust, not just re-confirmation.
**Source:** 36-UAT.md "Verification approach"

### Preserve-with-reason vs. retire-with-back-reference as the two legacy-metadata dispositions
**Pattern:** For legacy in-spec metadata markers (author comments, provenance notes) that a closure phase must dispose of, classify each as either "retire-with-back-reference" (the issue it tracked is resolved; point to the resolving phase) or "preserve-with-reason" (still relevant; cite the specific locked requirement or precedent that keeps it) — never a bare removal or a bare keep without citation.
**When to use:** Any milestone-closure phase reconciling legacy spec-metadata markers against the current state of the framework specs.
**Source:** 36-04-SUMMARY.md Task 1

### Sealed evidence plus a separate directory for every re-verification
**Pattern:** Never overwrite a prior evidence capture; write each new re-run's output (whether a "final rerun" task or an independent verifier's re-run) to its own directory, so every run's evidence remains independently inspectable and comparable.
**When to use:** Any phase where verification is expected to be re-run more than once (a fix-and-rerun cycle, or a second independent verifier).
**Source:** 36-05-SUMMARY.md "Final batch re-verify", 36-UAT.md Test #1

### Pin interpreter/environment determinism before claiming reproducibility
**Pattern:** Export a fixed hash seed (`PYTHONHASHSEED=0`) and capture the interpreter version and git commit SHA alongside probe output, so a later re-run's result is comparable byte-for-byte rather than merely "probably the same."
**When to use:** Any disposable-probe or test suite whose PASS/FAIL claim needs to survive independent re-execution as evidence, not just a one-time log.
**Source:** 36-05-SUMMARY.md Task 3, 36-UAT.md Test #1

---

## Surprises

### The milestone's final phase itself opened two new STOP gaps
**What was surprising:** Even at Phase 36 — pure closure/verification, supposedly just checking that everything already decided is consistent — two genuine STOP-protocol gaps (GAP-36-01, GAP-36-02) surfaced and required fresh owner ratification, because the closure reconciliation rule itself turned out to be unsatisfiable for four PKG rows and two LOOP rows that had no ledger row to anchor on.
**Impact:** Shows that even a milestone's designated "closing" phase can still discover genuinely undecided process questions, not just execute a fully mechanical checklist.
**Source:** 36-GAPS.md GAP-36-01, GAP-36-02

### A "final verification" phase's own probe suite initially failed 58% of checks
**What was surprising:** The acceptance-check spine — built specifically to prove the milestone's contracts hold — itself started at 11/26 PASS (15 failures) before the probes were corrected, an alarming initial signal for what was meant to be the closing confidence-building step.
**Impact:** Required the full legitimacy-scrutiny exercise (see Patterns) rather than simply treating "we fixed it and now it's green" as sufficient evidence of closure.
**Source:** 36-02-SUMMARY.md "Run summary" (11 PASS / 15 FAIL initial run)

### A second agent was dispatched specifically to distrust the first agent's own passing verdict
**What was surprising:** Even after the executing agent (Agent A) produced a fully self-verified 27/27 PASS record with hashed evidence, a second independent agent (Agent B, "verifier") was separately tasked to re-derive the same conclusion from scratch — re-running probes into its own evidence directory and reading the actual widening diff — rather than accepting Agent A's self-report as sufficient for milestone closure.
**Impact:** The two-agent executor/verifier split caught and explicitly ruled out the "loosened probes to mask a wrong spec" failure mode that a single self-verifying agent's report alone could not rule out.
**Source:** 36-UAT.md frontmatter ("verifier: agent-b-verifier"), "Verification approach"
