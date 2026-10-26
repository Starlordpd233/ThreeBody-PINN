# Phase 64 Gap Register

This is the phase-local register under the STOP protocol, as applied to v2.4. A source-silent decision is recorded with every field. It may be resolved under the owner's delegation **unless** it would move a locked value, spend the evaluation or pre-empt the verdict; those go to the owner. Milestone index: `.planning/milestones/v2.4-GAPS.md`.

## In plain language

The milestone's requirement list still shows 12 requirements as "Pending". They belong to Phases 61–63, which never ran because Gate G2 stopped the ladder. Nothing says what they should be called when v2.4 closes, or whether the next milestone inherits them. Whether v2.5 inherits them is part of where the project goes next, which is the owner's call. It goes on checkpoint ① as one pre-filled line.

## GAP-64-01 — how the requirements of the skipped phases are labelled at close (OWNER-ROUTED)

- **Decision point.** At the v2.4 close, what status do the 12 requirements of Phases 61–63 get, and do they carry forward to v2.5? The 12 are CONF-10, CONF-11, INST-06, INST-07, SPEC-07, SPEC-08, SPEC-09, SPEC-10, GATE-05, FEAS-05, RUN-06 and DIAG-08.
- **Where in artifact.** `.planning/REQUIREMENTS.md:405-416`, the traceability rows, all `Pending`. The decision is applied by the Phase 64 close task that ticks FEAS-06, FEAS-10 and VER-22.
- **Task context.** Phase 64 planning. The researcher's VER-22 analysis (`64-RESEARCH.md`, Open Question 1) raised it.
- **Classification.** Process-artifact schema and cross-phase. Carrying requirements forward shapes the next milestone's scope.
- **Source silence.**
  - VER-22 (`REQUIREMENTS.md:313`) and ROADMAP Phase 64 criterion 6 require only that every requirement maps to exactly one phase. They do not say what status a skipped requirement takes.
  - `stop-handoff.json` records `phases_61_63` as "skipped at G2, not failed". It says nothing about requirement statuses.
  - FEAS-04 and FEAS-09 have pre-registered wording ("recorded as skipped: no rescue", `REQUIREMENTS.md:403-404`). The other 12 have none.
- **Grounding.**
  - The requirement table is the milestone's contract record.
  - `Pending` at close reads as unfinished work. "Skipped at G2" records that a pre-registered gate stopped them.
  - "Carried forward" commits v2.5 to them. But the verdict routes v2.5 to a research round that diagnoses the problem first (D-14), and its findings may make some of them moot. For example, Phase 61's spec amendments assume the current representation.
  - So the label changes what v2.5 inherits. Picking it here would pre-empt the owner's decision on the verdict's routing.
- **Agent was tempted to** label all 12 "Skipped at G2 (no rescue), not failed", mirroring FEAS-04 and FEAS-09, and leave the carry-forward to `/gsd-new-milestone`.
- **What the user needs to decide.**
  - **A (recommended):** "Skipped at G2 (no rescue), not failed; carried forward to v2.5 as candidates." v2.5's requirements step decides which survive. This keeps the record without binding v2.5.
  - **B:** "Skipped at G2 (no rescue), not failed; not carried forward." v2.5 writes its requirements fresh from the trainex-r5 findings.
  - **C:** leave them `Pending`, so the milestone closes with them open.
- **Confidence of impact.** MEDIUM. It is bookkeeping that shapes what v2.5 inherits, and it does not change any verdict number.
- **Status.** OPEN. It is owner-routed because it could pre-empt the verdict's routing.
  - It is dependency-scoped: only the close task's requirement-status edits wait for it.
  - It is presented as one pre-filled line at checkpoint ①, with A as the default.
- **Resolution note.** —

## GAP-64-02 — how the checkpoint ① answer is recorded and checked (RESOLVED UNDER DELEGATION)

### In plain language

When the owner answers at checkpoint ①, the answer is saved word for word in one file. Next to it sits a small table that says, row by row, which choice the owner made. A program reads that table before it lets the later edits happen (rewriting `PROJECT.md`, relabelling the 12 skipped requirements, filling the verdict's decision field). Without the table, the program could only confirm that the owner's words exist, not that an edit matches them.

- **Decision point.** What does the checkpoint ① ruling record look like, and what may the `ruling` check read from it? The planner proposed the format in `64-05-PLAN.md` `<interfaces>` ("Ruling record format") and raised it as finding F-1 on return.
- **Where in artifact.** `64-05-PLAN.md` Task 1 (the reply rules on the page) and Task 3 (the `ruling` check); `64-06-PLAN.md` Tasks 2–3 (writing the record); `64-07-PLAN.md` Tasks 1 and 3 (applying and checking edits).
- **Task context.** Phase 64 planning, plan-phase run of 2026-10-25. The planner had to turn the `ruling` row of `64-VALIDATION.md` into a checkable format.
- **Classification.** Process-artifact schema. It has no cross-phase effect: the record is read only inside Phase 64.
- **Source silence.**
  - `64-VALIDATION.md:63` and `64-RESEARCH.md:741` require exactly one non-empty `owner-quote` block, a tracked and clean file, and approved edits applied "only if the record approves". They do not say how the owner's answers are laid out, or how "approves" is read mechanically.
  - `64-RESEARCH.md:353` names plan 60-17 as the template, with the owner's message stored byte for byte in an `owner-quote` fence. `60-17-PLAN.md:66` shows that precedent: one `phase60-ruling` block with `ruling:` and `answer:` lines, for a single either-or choice. Checkpoint ① has 15 items.
  - `64-RESEARCH.md:535` says an unclear reply is asked about again "for that item only", and items the owner does not address are recorded as open. So the answer may arrive in more than one message, which the one-block rule does not mention.
  - `REQUIREMENTS.md:159` and `:210-211` require the decision "recorded verbatim", open items "recorded as open", and `PROJECT.md` rewritten "on the owner's approval". They fix neither a layout nor an approval signal.
  - `64-PATTERNS.md:284` and `:320` say to copy the fence parser and that the ruling file has exactly one `owner-quote` block while the charter has several. They give no table schema.
  - `64-CONTEXT.md` D-08 (`:76-79`) says every charter item is pre-filled and open items are recorded as open. It is silent on the record's layout.
- **Grounding.**
  - The ruling record is the only control that gates three owner-dependent writes: the `PROJECT.md` rewrite, the 12 requirement labels (what v2.5 inherits) and the verdict's `owner_decision` field.
  - A verbatim quote is the evidence, but it is free text. A verifier must never parse, evaluate or format it into a path or command (the plan's own injection rule). So a mechanical "applied only if approved" check needs a machine-readable layer outside the quote, and that layer must use a closed vocabulary so it can only restate a choice the page offered, never extend it.
  - Option A keeps one verbatim block (k messages, in order, one blank line apart), so the copied fence parser and the one-block rule stay as validated. The table sits outside the fence, one row per item in page order, with tokens `continue`, `change-course`, `stop`, `recorded`, `open`, an option letter the page row offers, or `changed: <restatement>`.
  - Option B (one block per message) breaks the one-block rule and the copied parser, so a new rule would need its own proof. Option C (no table) leaves the check able to confirm only that the quote exists, so "applied only if approved" would rest on whoever reads the quote, not on a check.
  - The remaining risk in A is a transcription error in the table. It is bounded: the table may only restate the chosen option, the quote beside it is the evidence, and the page's reply rules (64-05 Task 1) say an unclear item is asked again or recorded `open`.
- **Agent was tempted to.** Accept the planner's proposal without logging it, because it follows the 60-17 precedent. This entry exists so the choice is recorded and the owner can veto it.
- **What the user needs to decide.** Nothing is required. The owner may veto before 64-05 Task 3 runs:
  - **A (resolved to this):** one `owner-quote` block holding every owner message verbatim, plus a 15-row "Recorded answers" table (V-1, C-1 to C-14) in the closed vocabulary above. "Approve all" on the page records V-1 as `change-course`, the pre-filled answer, and every other row as its pre-filled option, except C-6 and C-7, which stay `open` until the owner names an option (owner's decision, 2026-10-25).
  - **B:** one `owner-quote` block per owner message. This changes the one-block rule in `64-VALIDATION.md:63`.
  - **C:** no table. The `ruling` check could confirm only that the quote exists.
- **Confidence of impact.** LOW. It is a record format, and it changes no verdict number, bar or label. It is costly to change after the ruling is committed, because 64-07 applies edits from it. Before execution a change means revising 64-05, 64-06 and 64-07.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-25), under the owner's standing delegation of 2026-10-07, re-confirmed 2026-10-09 (ROADMAP "Delegation and gaps"). It does not move a locked value, spend the evaluation or pre-empt the verdict: the table accepts `continue`, `change-course` or `stop`, and the pre-filled `change-course` default comes from D-14 and D-08, not from this format.
- **Resolution note.** Option A, **confirmed by the owner directly on 2026-10-25** in the plan-phase session, when asked after the plan-checker's iteration-3 pass said a record format should be shown to the owner. The owner also decided that "approve all" does not cover C-6 (whether the `10⁻⁵` bar stays) or C-7 (how energy is measured, GAP-59-08): those two stay `open` until the owner names an option. The format is exactly as written in `64-05-PLAN.md` `<interfaces>` ("Ruling record format"), as revised for that change. Dependent tasks: 64-05 Tasks 1 and 3, 64-06 Tasks 2 and 3, 64-07 Tasks 1 and 3. Recorded by the orchestrating agent during plan-phase 64, citing the delegation and this rationale; the planner did not write to this register.

## GAP-64-03 — "estimated cost to the next level" against the owner's D-05 choice (RESOLVED UNDER DELEGATION)

### In plain language

The roadmap and FEAS-06 say the verdict must give "the estimated cost to the next level and to the finish". The owner chose, in discussion, a cost section that does not project hours to the next level, because the accuracy curves levelled off far above the passing level and give no rate to extrapolate. The two cannot both be met word for word. The verdict will say plainly that the next-level cost cannot be estimated from this evidence, say what would measure it, and give the measured and for-scale figures D-05 lists. The owner sees this at checkpoint ① before FEAS-06 is ticked.

- **Decision point.** How does the verdict satisfy ROADMAP Phase 64 criterion 3 and FEAS-06's cost item ("the estimated cost to the next level and to the finish") when D-05 says "Hours to the next level is not projected"?
- **Where in artifact.** `ROADMAP.md:377` (goal) and `:387` (criterion 3); `REQUIREMENTS.md:154` (FEAS-06 cost bullet); `64-CONTEXT.md` D-05 (`:57-63`) and D-06 (`:67`); `64-04-PLAN.md:26`.
- **Task context.** Phase 64 plan-phase, plan-checker iteration 1 (a WARNING). I confirmed the mismatch against the three files above.
- **Classification.** Semantic. A locked owner decision and the planning contract's wording disagree about what the verdict asserts.
- **Source silence.**
  - `ROADMAP.md:387` and `REQUIREMENTS.md:154` do not define "estimated", and do not say whether "not estimable, with what would measure it named" counts.
  - D-05 (`64-CONTEXT.md:57-63`) fixes the cost section's contents but does not say whether the roadmap wording is amended or treated as met.
  - `64-DISCUSSION-LOG.md:57-63` (Q1) offered "Measured + for-scale" and "Spent + not estimable", and the owner chose the first. It records the choice, not how the roadmap text is reconciled.
  - D-06 (`64-CONTEXT.md:67`) says where a projection is unknown, the verdict says so and names what would measure it. That covers the wording of the statement, not the contract text.
- **Grounding.**
  - A cost to the next ladder level needs a measured rate of improvement. The committed curves fell 25–50-fold in the first ~5% of training and then settled about 11–12 times above the Tier-1 limit, so there is no rate to extrapolate from. Any hours figure would be invented.
  - "Every assumption stated" is met by stating the assumption that no rate exists. A costed first step (the v2.5 diagnostic round) and the measured per-experiment cost bound what the next step costs without projecting the level.
  - Rewording the roadmap would change the milestone's contract text, which is a larger step than stating the reconciliation in the verdict.
- **Agent was tempted to.** Reword ROADMAP criterion 3 to the D-05 form, as `bb323a52` did for the rented-GPU clause. That edit followed an explicit owner statement about that sentence; D-05 does not address this sentence.
- **What the user needs to decide.** Nothing is required. The owner may veto at or before checkpoint ①:
  - **A (resolved to this):** follow D-05 and D-06. The verdict has an explicit "Cost to the next level" statement: not projected, why, and what would measure it. The roadmap text is unchanged. The reconciliation is checked in the verdict and in 64-07's final check, and the owner sees it at checkpoint ① before FEAS-06 is ticked.
  - **B:** reword ROADMAP criterion 3 and FEAS-06 to the D-05 form, with the owner's sign-off.
  - **C:** add a bounded next-level estimate with stated assumptions. This contradicts D-05 and needs a new owner decision.
- **Confidence of impact.** MEDIUM. No number changes, but it decides how the verdict meets a written success criterion.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-25), under the owner's standing delegation of 2026-10-07, re-confirmed 2026-10-09 (ROADMAP "Delegation and gaps"). It moves no locked value, spends no evaluation and pre-empts no verdict. Plans 64-04 and 64-07 apply it; the plan-checker confirmed both on 2026-10-25 (iteration 2).
- **Resolution note.** Option A, **confirmed by the owner directly on 2026-10-25** in the plan-phase session: keep the roadmap wording, and the verdict says plainly that the next-level cost is not estimable from this evidence. Recorded by the orchestrating agent; the planner did not write to this register.
