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

The verdict's evidence says the network's output barely varies in time while the real orbit varies, so the project cannot yet tell whether the limit is the design or the training recipe. The recommendation is to change course: v2.5 opens with the trainex-r5 research round (open-book, diagnosis first) and runs no new long training until it explains the time-constant output. Continuing on this path repeats the same design and recipe and spends the remaining budget on an answer the evidence already questions. Stopping here keeps the one-shot held-out evaluation unspent; it is a legitimate answer if the diagnosis round is not worth the computing time. You decide (D-14).

## C-1: Purpose

The purpose is recorded from your own words on 2026-10-25, so it is not asked again. You answered "1 and 2" to the two options offered first, Learning and Research paper; read together with the rest of the answer, this is a learning project whose research output is a proof of concept, a modest positive result rather than a polished paper (CONTEXT D-07).

```owner-quote
1 and 2. we're not aiming for a perfect research result. I think this project could be more for like a PoC because not many people have done training PINN for 3 body porblems in the past. does that make sense? also, i'm just a freshman in college, and all i have this macbook. so reasonably we wouldn't achieve somethign great here. but it's just good to see some positive results coming out.
```

## C-2: Definition of done

A positive result is a network that passes the one-shot Stage-0 held-out exam at the C-4 and C-5 bar (Level 6), not a network that merely learns one system (Level 3), and not every stage at its bar (Level 9). Level 6 is recommended because it can be stated without overselling: one network, one preserved exam, one pre-registered bar. Level 3 counts as Rung 2b when one system is learned on at least 2 of 3 seeds. Level 9 needs every stage at its bar, which the survey's empty Stage 3 makes impossible to demonstrate today.

## C-3: Current level

The current level is recorded: Level 1. The training code runs, but not yet to the specification. The ladder counts a level only when every level below it is reached, so Level 1 is the whole of the current position and nothing above it is claimed.

## C-4: Stage-0 pass bar, position criterion

The position criterion is the part of the Stage-0 bar that measures where the predicted bodies are. It is fixed before any held-out exam and set against the anchors below; it is a proposal for your approval.

| Comparison point | Median E |
|---|---|
| Formula, training panel | 0.989 |
| Formula, validation panel | 0.940 |
| Copy, validation panel | 2.135 |
| Constant time-mean predictor | 1.1396 to 1.2337 |
| Trained networks, final | 1.14 to 1.24 |

The tiers are Tier 1: E ≤ 0.1; Tier 2: E ≤ 0.01 and ε_H ≤ 10⁻³; Tier 3: E ≤ 0.01 and ε_H ≤ 10⁻⁵. Beating the formula or the copy means E strictly below its value; reaching Tier 1 means E ≤ 0.1, inclusive; the locked 10⁻⁵ held-out bar passes at equality (pinn_architecture.md:1087). The frozen decision rule counts Rung 2b on at least 2 of 3 seeds and Rung 3 on at least 12 of 16; the page's 75% is that same 12 of 16 proportion. The census puts the median Stage-0 orbit at 18.61 inner laps and lap timing at 1 part in 1,169.

## C-5: Stage-0 pass bar, energy criterion

The energy criterion is the other half of the Stage-0 bar, and it is never used alone. Published levels bracket it: Breen et al. report energy error of order 10⁻² on a two-parameter family, and the 2026 PINN study reports 0.02–3% on single periodic orbits. The tiers are Tier 1 at E ≤ 0.1, Tier 2 at E ≤ 0.01 and ε_H ≤ 10⁻³, and Tier 3 at E ≤ 0.01 and ε_H ≤ 10⁻⁵.

- **A:** ε_H ≤ 10⁻² from autograd velocities, conditional on C-7 being A; Tier 2's 10⁻³ is the stretch.
- **B:** ε_H ≤ 10⁻³, conditional on the C-7 answer.
- **C:** ε_H ≤ 10⁻⁵, conditional on the C-7 answer.

Every option depends on how ε_H is measured (C-7): the same network can pass or fail on the measurement route alone.

## C-6: The 10⁻⁵ held-out bar

The 10⁻⁵ held-out bar is locked in pinn_architecture.md §10.6, where it passes at equality (:1087). Your recorded lean, quoted from the amendments document, is: "Relax the `10⁻⁵` bar, decided later, with evidence." The agent's recommendation, consistent with that lean, is to replace it by formal amendment with an evidence-based bar — the bar of C-4 and C-5 — in the milestone that sets the bars. Moving a locked value is outside the agent's delegation, so you decide. The amendment is routed, not made: Phase 64 edits no specification.

## C-7: GAP-59-08, how ε_H is measured

GAP-59-08 asks how ε_H, the energy-drift measure, is computed from a network's predicted positions. The current evaluator uses finite differences on the dataset's coarse output grid; on that grid the exact Brutus orbits already score 4.7e-2, 2.1e-1 and 3.8e-1 (5–38%), against a value near zero with true velocities. Under that route no model, not even a perfect one, can pass the 10⁻⁵ bar on this data.

- **A (recommended):** autograd velocities in the evaluator and the validation gate, written into §10.6 by a formal clarifying amendment. It measures the network's actual motion and matches the scorecard.
- **B:** keep finite differences on a dense grid. It is likely still above 10⁻⁵ for the fastest binaries.
- **C:** keep the gate as it is, knowing it cannot pass.

This decision blocks any held-out spend and the pass-bar choice, and nothing else in v2.4.

## C-8: Pass bars for Stages 1–6

Stages 1–6 are listed and left open until Stage 0 passes. The survey gives two cautions: Stage 3 is empty, and the stage mapping beyond Stages 0 and 1 is owner-pending. Option A is recommended because a bar set before the stage's data exists would be a guess.

## C-9: Budget

The budget is months of computing on this Mac. The measured per-experiment cost is 2.573 to 3.046 h for an unextended arm, 5.693 h for the doubled arm, and 22.378 h in all. The figure is for scale only: generation 7's measured 12.3 s per step × 200,000 to 300,000 Adam steps is 28.5 to 42.8 days of nonstop computing; that rate comes from generation 7's run, which ended in a failed state (runs/stage0-v23g7-seed42/status.json), on device mps (that run's summary.json, header.device), a Mac measurement.

The costed first step for v2.5 is the trainex-r5 round. Its computing need is not yet measured: it depends on which arms the round commissions, and the harness times each arm before fixing its budget. A 100,000-step data-only diagnostic arm would take about 0.3 h at the median timed rate, a labelled illustration, not a plan. How many months to allow is your choice: A, about 1 month for the next milestone, re-set by you at each verdict; B, 3 months; C, 6 months.

Latest statement, verbatim:

```owner-quote
For now, the only device on which we will do the computation will be on this MacBook, so ignore any proposal or route where it requires a rented GPU, either that is a cloud GPU or some other thing. That will not be something that we should consider at this point, so right now treat every single computation that will be needed done on this Mac.
```

Earlier statement, verbatim:

```owner-quote
We will not have access to a rented GPU unless that is absolutely necessary and it is proven to make a difference. I will not invest into buying or renting a separate GPU for speeding up the work. The training process should be done on this Mac. does that make sense? tell me if this mac cannot handle the computation. I doubt that's the case. but that statement also requires lots of proofing and actual evidence to support. so I would be careful making any statements toward that
```

## C-10: Stop rule

FEAS-10's draft text is the recommended default: "a milestone that neither climbs a ladder level nor beats the best fixed-scorecard result means stop or change approach, with no third attempt at the same idea."

The baseline is Level 1, with every arm at Tier 0. The best official ε_H is 123.62, on arm g2s-1632-w240. A constant time-mean predictor scores E 1.1396 to 1.2337 on the panel systems, close to the trained networks' 1.14 to 1.24, so a rule that counts any lower E as progress would count almost any change.

- **A (recommended):** "beats" means at least one panel system reaches Tier 1 (E ≤ 0.1), which a constant predictor cannot do here.
- **B:** E below the constant predictor's by a margin you name.
- **C:** any lower E counts.

You choose what "beats" means; the rule itself is the default.

## C-11: The evaluation section of ctl_instruction.md

The evaluation section of ctl_instruction.md is written as if results exist. Three anchors, quoted verbatim from the frozen file:

- line 2057: "In our results, the final model shows minimal energy drift (e.g.,"
- line 2081: "much sooner than it should. In testing our model, we found that it can"
- line 2111: "our case, after the final active learning fine-tuning, the model passes"

No such results exist. The text is aspirational, left over from the original write-up, and is not evidence that the approach works. Its rewrite is routed to the milestone that sets the bars; Phase 64 makes no edit.

## C-12: Rewriting What This Is and Core Value in PROJECT.md

PROJECT.md's What This Is and Core Value still describe the earlier language-model project, so the project's stated purpose and this charter's would disagree. The drafts below are applied only on approval (C-12 A), by 64-07.

```project-draft-what-this-is
A learning project and a proof of concept by one student on one MacBook. It trains a curriculum-trained physics-informed neural network on high-precision Brutus three-body data to predict motion from starting conditions, stage by stage, and measures each stage against fixed comparison points. All computation runs on this Mac.
```

```project-draft-core-value
An evidence-backed, pre-registered answer at each milestone to whether the approach learns three-body motion, in physical units, against this charter's bars.
```

## C-13: The title line and the Model constraint in PROJECT.md

The title line and the Model constraint also still describe the earlier language-model project. The drafts below are applied only on approval (C-13 A), by 64-07.

```project-draft-title
# Three-Body Physics-Informed Neural Network (CTL-PINN)
```

```project-draft-model
- **Model**: the CTL-PINN network locked in pinn_architecture.md (SQR-SkipResNet-SIREN; input [τ, IC₁₃]; output the three bodies' positions through the mass-weighted centre-of-mass projection head), trained on this Mac
```

## C-14: The requirements of the skipped phases (GAP-64-01)

GAP-64-01 asks how the twelve requirements of Phases 61–63 are labelled at close, and whether they carry forward to v2.5. The twelve are CONF-10, CONF-11, INST-06, INST-07, SPEC-07, SPEC-08, SPEC-09, SPEC-10, GATE-05, FEAS-05, RUN-06 and DIAG-08. Their checkboxes stay unticked (`- [ ]`) under every option, and v2.5's requirements step decides which survive under A.

- **A (recommended):** "Skipped at G2 (no rescue), not failed; carried forward to v2.5 as candidates."
- **B:** "Skipped at G2 (no rescue), not failed; not carried forward."
- **C:** leave them Pending, so the milestone closes with them open.

## Sources

- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md`
- `.planning/phases/59-read-only-baseline-scorecard/evidence/baselines/baselines.json`
- `.planning/phases/59-read-only-baseline-scorecard/evidence/census/census.json`
- `.planning/phases/60-single-system-learnability/evidence/g2/stop-handoff.json`
- `.planning/phases/64-feasibility-verdict/64-CONTEXT.md`
- `.planning/phases/64-feasibility-verdict/64-GAPS.md`
- `.planning/phases/64-feasibility-verdict/64-RESEARCH.md`
- `.planning/phases/64-feasibility-verdict/64-VERDICT.md`
- `.planning/phases/64-feasibility-verdict/evidence/numbers.json`
- `docs/work/designs/cross_cutting/v2.4-milestone-proposal/2026-10-11-v2.4-feasibility-amendments.md`
- `pinn/verification/artifacts/feasibility_scorecard_v1.json`
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
- `runs/stage0-v23g7-seed42/status.json`
- `runs/stage0-v23g7-seed42/summary.json`
