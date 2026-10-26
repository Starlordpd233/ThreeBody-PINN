---
schema_version: phase64-charter/v1
status: awaiting-owner
created: 2026-10-26
verdict_citation: .planning/phases/64-feasibility-verdict/64-VERDICT.md
numbers_sha256: 632e02b21d1ee132f844e5c9592578d5ce32bb31b9673ccb76dc84556511cafa
ruling_citation: pending
---

**Audience:** the project owner; reading about five minutes; replying takes one message.

## In plain language

This charter is the project's rulebook for what comes next: what the project is for, when it counts as done, what score counts as passing, how much computing time to spend, and when to stop.

Every line on the next page is already filled in with a recommendation, so you can approve the page as it stands or change a single line. The purpose (C-1) and the Mac-only rule (C-9) are recorded from your own words and are not asked again. You reply once, at checkpoint ①, in one message; the appendices hold the evidence, the options and the draft project text.

<!-- page:begin -->
## The charter on one page

Approve the page as it stands, or change single lines; C-6 and C-7 need their own answers.

| ID | Item | Recommended answer | Other options | Owner |
|---|---|---|---|---|
| V-1 | Your decision on the verdict | Change course: v2.5 opens with the trainex-r5 research round (open-book, diagnosis first) and runs no new long training until it explains the time-constant output | Continue on this path (the same design and recipe); Stop here (the held-out evaluation stays unspent) | |
| C-1 | Purpose | Recorded: learning, with a proof of concept as the research output (2026-10-25, your words in C-1) | none | |
| C-2 | Definition of done | A: Level 6 at Stage 0, one network passes the one-shot Stage-0 held-out exam at the C-4 and C-5 bar | B: Level 3: learns one system (Rung 2b counts on at least 2 of 3); C: Level 9, every stage at its bar | |
| C-3 | Current level | Recorded: Level 1, the training code runs but not yet to spec | none | |
| C-4 | Stage-0 bar, position | A: Tier 1 (E ≤ 0.1) and E strictly below both the formula's and the copy's on at least 75% of the Stage-0 validation panel (the frozen 12 of 16 proportion) | B: valid-horizon h at 10% of at least 0.5 on the same share; C: a position criterion you name | |
| C-5 | Stage-0 bar, energy | A: ε_H ≤ 10⁻² from autograd velocities, conditional on C-7 being A (Tier 2, 10⁻³, as the stretch) | B: ε_H ≤ 10⁻³, conditional on the C-7 answer; C: ε_H ≤ 10⁻⁵, conditional on the C-7 answer | |
| C-6 | The 10⁻⁵ held-out bar | A: replace it by formal amendment with the evidence-based bar of C-4 and C-5, in the milestone that sets the bars | B: keep 10⁻⁵ as the success criterion | |
| C-7 | GAP-59-08 | A: autograd velocities in the evaluator and validation gate, by a formal clarifying amendment to pinn_architecture.md §10.6 | B: finite differences on a dense grid; C: keep the gate as is, knowing it cannot pass | |
| C-8 | Stages 1–6 bars | A: listed and left open until Stage 0 passes | B: you name some now | |
| C-9 | Budget (months of computing on this Mac) | A: about 1 month for the next milestone, re-set by you at each verdict | B: 3 months; C: 6 months | |
| C-10 | Stop rule | A: the FEAS-10 rule, with "beats" meaning at least one panel system reaches Tier 1 (E ≤ 0.1) | B: E below the constant predictor's by a margin you name; C: any lower E counts | |
| C-11 | ctl_instruction.md evaluation section | Recorded: it describes results that do not exist; its rewrite goes to the milestone that sets the bars; no edit now | none | |
| C-12 | PROJECT.md What This Is and Core Value | A: apply the draft in C-12 | B: do not rewrite now | |
| C-13 | PROJECT.md title line and Model constraint | A: rewrite them too (draft in C-13) | B: leave them | |
| C-14 | Requirements of Phases 61–63 (GAP-64-01) | A: "Skipped at G2 (no rescue), not failed; carried forward to v2.5 as candidates" | B: "Skipped at G2 (no rescue), not failed; not carried forward"; C: leave them Pending | |

**How to reply.** Start with V-1, then say "approve the rest" or write changes as "C-4: B" or "C-9: two months". "Approve all" accepts every recommended answer, including change course for V-1, except C-6 and C-7. C-6 and C-7 each need their own answer, written with the row's ID, for example "C-6: A"; "approve all" and "approve the rest" do not cover them, so each stays open until you answer it. An item you do not mention is recorded as open, unless you said "approve all" or "approve the rest".
<!-- page:end -->

## V-1: Your decision on the verdict

This is the one decision that shapes the next milestone: continue on this path, change course, or stop. The recommendation is to change course, because the evidence does not yet say whether the limit is the design or the recipe. The options and their consequences are set out below.

## C-1: Purpose

The purpose is recorded from your own words on 2026-10-25, so it is not asked again. In plain terms, this is a learning project whose research output is a proof of concept: a modest positive result, not a polished paper.

## C-2: Definition of done

The definition of done says what a positive result would be. The options map to the readiness ladder: Level 6 at Stage 0 (recommended), Level 3, or Level 9.

## C-3: Current level

The current level is recorded: Level 1. The training code runs, but not yet to the specification, and the ladder counts a level only when every level below it is reached.

## C-4: Stage-0 pass bar, position criterion

The position criterion is the part of the Stage-0 pass bar that measures where the predicted bodies are. It is fixed before any held-out exam and set against the formula, the copy and the published studies; the anchors are in the appendix.

## C-5: Stage-0 pass bar, energy criterion

The energy criterion is the other half of the Stage-0 pass bar. It is never used alone, and every option is conditional on how energy is measured (C-7).

## C-6: The 10⁻⁵ held-out bar

The locked 10⁻⁵ held-out bar is the strictest energy requirement in the specification. The draft follows your recorded lean: replace it by formal amendment with an evidence-based bar, in the milestone that sets the bars. Moving a locked value is outside the agent's delegation, so you decide.

## C-7: GAP-59-08, how ε_H is measured

GAP-59-08 asks how ε_H, the energy-drift measure, is computed. Today's finite-difference check fails even the exact Brutus orbits, so the pass bar depends on this answer. The options and the measured floor are in the appendix.

## C-8: Pass bars for Stages 1–6

The pass bars for Stages 1–6 are listed and left open until Stage 0 passes. The survey gives two cautions: Stage 3 is empty, and the stage mapping beyond Stages 0 and 1 is owner-pending.

## C-9: Budget

The budget is measured in months of computing on this Mac. The appendix gives the measured per-experiment cost, a for-scale figure and the costed first step for v2.5; how many months to allow is your choice.

## C-10: Stop rule

The stop rule says when a milestone should stop or change approach instead of trying the same idea again. The draft text is the recommended default, and "beats" needs a margin you choose.

## C-11: The evaluation section of ctl_instruction.md

The evaluation section of ctl_instruction.md describes results that do not exist. The charter records that fact and routes the rewrite to the milestone that sets the bars; no specification is edited now.

## C-12: Rewriting What This Is and Core Value in PROJECT.md

PROJECT.md's What This Is and Core Value still describe the earlier language-model project. The appendix holds a draft rewrite, applied only if you approve it.

## C-13: The title line and the Model constraint in PROJECT.md

The title line and the Model constraint also still describe the earlier language-model project. The appendix holds draft replacements, applied only if you approve them.

## C-14: The requirements of the skipped phases (GAP-64-01)

GAP-64-01 asks how the twelve requirements of Phases 61–63 are labelled at close, and whether they carry forward to v2.5. The options and the exact labels are in the appendix; their checkboxes stay unticked under every option.

## Sources

- `.planning/phases/64-feasibility-verdict/64-CONTEXT.md`
- `.planning/phases/64-feasibility-verdict/64-VERDICT.md`
- `.planning/phases/64-feasibility-verdict/evidence/numbers.json`
- `.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md`
- `.planning/phases/60-single-system-learnability/evidence/g2/stop-handoff.json`
- `.planning/PROJECT.md`
- `docs/work/designs/cross_cutting/v2.4-milestone-proposal/2026-10-11-v2.4-feasibility-amendments.md`
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
- `runs/stage0-v23g7-seed42/status.json`
