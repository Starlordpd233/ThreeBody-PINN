# 25-GAPS.md - Phase 25 STOP-Protocol Gap Register

**Phase:** 25 - Evidence Framework and Issue Ledger
**Created:** 2026-06-12
**STOP-protocol authority:** `AGENTS.md` / `CLAUDE.md` "v1.5 applicability" + STOP-protocol field list.

## GAP-25-01 - D-01 phase-scope split confirmation

- **Decision point:** Should Phase 25 use the split reading already drafted in D-01 - machinery plus only the three known EVID-10 conflict adjudications - or should Phase 25 author packets/verdicts for all 19 issue-02 findings before Phases 26-28 proceed?
- **Where in artifact:** `.planning/phases/25-evidence-framework-and-issue-ledger/25-CONTEXT.md` D-01 and `.planning/phases/25-evidence-framework-and-issue-ledger/25-01-PLAN.md` objective D-01 flag.
- **Task context:** review-driven planning-artifact revision before Phase 25 execution; the review reports found the D-01 flag but no blocking execution gate.
- **Classification:** **cross-phase reframing** - this chooses whether Phases 26-28 author their own packets immediately before edits or consume a complete Phase 25 packet/verdict inventory.
- **Source silence:**
  - `.planning/ROADMAP.md:170-174` - says each selected finding needs packet/verdict evidence and separately names the three known conflicts, but does not explicitly say whether Phase 25 or the owning spec-edit phases author the non-conflict packets.
  - `.planning/REQUIREMENTS.md:39-43` - defines EVID-06..10 evidence and adjudication duties, but does not assign non-conflict packet authorship to a specific phase.
  - `.planning/phases/25-evidence-framework-and-issue-ledger/25-CONTEXT.md:23-25` - records the split-reading rationale and also admits the literal whole-inventory reading; it is the ambiguity, not an independent user confirmation.
  - `.planning/phases/25-evidence-framework-and-issue-ledger/25-DISCUSSION-LOG.md:22-24` - records an auto-selected recommendation and says the tension is flagged to the user; it is not a user decision resolving the flag.
- **Mathematical / engineering grounding:** This is a process-architecture dependency decision. Under the split reading, Phase 25 creates the reusable machinery and only the three cross-source conflict records; Phases 26-28 then preserve evidence-before-edit locality by writing each remaining packet next to the spec edit it gates. Under the literal reading, Phase 25 becomes a full 19-finding adjudication phase; Phases 26-28 consume already-authored packets and focus on edits/verification. The two choices produce different artifact counts, phase exit conditions, commit scope, and downstream responsibilities.
- **Agent was tempted to:** proceed with the split reading because the ROADMAP says the three known conflicts are Phase 25's center of gravity and Phases 27/28 say edits land "per the EVID-10 record." That is a plausible interpretation, but the universal wording in ROADMAP success criteria 1-3 makes it a user-level scope choice.
- **What the user needs to decide:**
  - **A.** Confirm the split reading: Phase 25 authors machinery plus the three known EVID-10 conflict records; Phases 26-28 author the remaining packets immediately before their edits.
  - **B.** Use the literal reading: Phase 25 authors packets/verdicts for all 19 issue-02 findings before Phases 26-28 proceed.
  - **C.** Define a hybrid scope, naming exactly which additional non-conflict findings Phase 25 must adjudicate now.
- **Confidence of impact:** HIGH - the answer changes Phase 25 deliverable count, downstream phase responsibilities, and whether the current two-plan structure is sufficient.
- **Status:** **RESOLVED-WITH-INSTRUCTION** (2026-06-12)
- **Resolution note:** User selected **Option A** (split reading) on 2026-06-12: Phase 25 delivers the machinery plus the three known EVID-10 conflict records (SCS thresholds, `D=6.694`, M11/M12); Phases 26-28 author the remaining packets/verdicts immediately before their spec edits, using the Phase 25 machinery (evidence-before-edit, EVID-06). The user additionally instructed a clarifying parenthetical on ROADMAP Phase 25 success criteria 1-3 so the goal-backward verifier reads them as milestone-wide guarantees enforced by the Phase 25 machinery rather than as Phase 25 deliverables (applied in the same commit as this resolution). Decision basis presented to the user: the literal all-19 reading would make step 1 of the adjudicate->fix->verify loop vacuous in Phases 26-28, and pre-authored packets citing spec line ranges would drift as Phase 26/27 edits land before Phase 28 consumes its packets; v1.4 precedent (Phase 16) shipped machinery with zero verdicts.

## GAP-25-02 - Ledger status for adjudicated-but-unfixed findings

- **Decision point:** When Phase 25 assigns an EVID-10 verdict for a finding whose actual spec edit is owned by Phase 26, 27, or 28, what ledger status and transition-log convention should be used before the fix exists?
- **Where in artifact:** `.planning/phases/25-evidence-framework-and-issue-ledger/25-02-PLAN.md` objective ledger-status note and the task-level status-transition examples for SCS, D=6.694, M11, and M12.
- **Task context:** review-driven planning-artifact revision before Phase 25 execution; the review reports found that the draft plan acknowledged source silence but proceeded with a `PENDING -> PENDING` convention without a formal gap.
- **Classification:** **process-artifact schema** - this changes how the ledger state machine represents an adjudication outcome that is not yet a fix.
- **Source silence:**
  - `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md:73-81` - defines `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED`, `DEFERRED`, regression, and phase-exit rules, but does not define an "adjudicated but unfixed" state.
  - `.planning/phases/25-evidence-framework-and-issue-ledger/25-CONTEXT.md:39` - says Evidence Packet links and status transitions are ledger edits in the same commit as the underlying change, but not what status represents verdict-only work.
  - `.planning/phases/25-evidence-framework-and-issue-ledger/25-CONTEXT.md:48` - requires preserving the existing state machine during the lifecycle re-issue, so inventing a new state is not mechanically authorized.
  - `.planning/REQUIREMENTS.md:39-43` - requires packets and verdicts before edits, but does not specify the intermediate ledger status for pre-fix adjudication.
  - `.planning/phases/25-evidence-framework-and-issue-ledger/25-02-PLAN.md:75` - explicitly says the lifecycle is source-silent, then chooses a convention; that choice needs user instruction.
- **Mathematical / engineering grounding:** A ledger status is a state-machine invariant. `IN_PROGRESS` normally means a fix is being worked, which is false for Phase 25 records whose fixes are owned later; `FIX_APPLIED` and `VERIFIED` are also false because no spec edit or acceptance check has happened. Keeping `PENDING` preserves the existing enum, but `PENDING + verdict + evidence link` can be misread downstream as "not adjudicated." Adding `ADJUDICATED` or a sub-state would be clearer but changes the process schema and every phase verifier that reads the ledger.
- **Agent was tempted to:** keep the seeded `PENDING` status and add a `PENDING -> PENDING (Phase 25 P02 EVID-10 record authored + verdict assigned)` audit entry, because it avoids falsely claiming a fix is active or applied. That is operationally sensible but still a new convention requiring user confirmation.
- **What the user needs to decide:**
  - **A.** Confirm the `PENDING` status convention: Phase 25 may fill the verdict and Evidence Packet fields while leaving Status as `PENDING`, with a `PENDING -> PENDING` audit entry and a README note that `PENDING + Verdict` means adjudicated-but-unfixed.
  - **B.** Add a new explicit `ADJUDICATED` status or sub-state for verdict-assigned, fix-not-started rows.
  - **C.** Use another existing state and define exactly how downstream phases distinguish verdict-only work from fix work.
  - **D.** Do not update ledger verdict/status fields in Phase 25; leave the verdict solely inside evidence records until the owning spec-edit phase starts.
- **Confidence of impact:** HIGH - downstream Phases 26-28 will use the ledger to decide what has been adjudicated, what still needs work, and what blocks phase exit.
- **Status:** **RESOLVED-WITH-INSTRUCTION** (2026-06-12)
- **Resolution note:** User selected **Option A** (`PENDING` convention) on 2026-06-12: Phase 25 fills the verdict and Evidence-Packet fields while leaving Status `PENDING`; each such row gets a `PENDING -> PENDING (Phase 25 P02 EVID-10 record authored + verdict assigned)` audit entry with date + commit-audit label in the per-finding subsection; the protocol README documents the legend that `PENDING + Verdict` means adjudicated-but-unfixed (this legend requirement was added to 25-01-PLAN.md Task 2 in the same commit as this resolution). The state machine `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED` is preserved verbatim — no new state is introduced (consistent with ROADMAP Phase 25 criterion 5 and 25-CONTEXT D-11 keep-verbatim). 25-02-PLAN.md already encodes this convention conditionally in its objective ledger-status note; no further plan edit is required. **Addendum (user instruction, 2026-06-12):** the README legend must also state the exit-gate interaction — adjudicated-but-unfixed rows are NOT "in-scope findings" for Phase 25's phase-exit gate (Phase 25 owns records, not fixes; without this clarification a literal reading of "phase-exit permits only `VERIFIED`/`DEFERRED` for in-scope findings" would wrongly block Phase 25 exit with the three rows at `PENDING`); each such row becomes in-scope for the phase that owns its fix (26-28). Applied to 25-01-PLAN.md Task 2 (action bullet, acceptance criterion, automated grep for the literal phrase "owns records, not fixes").

## Milestone-wide index

Mirrored at `.planning/milestones/v1.5-GAPS.md` (updated 2026-06-12 with these entries).
