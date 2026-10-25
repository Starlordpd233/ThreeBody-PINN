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
