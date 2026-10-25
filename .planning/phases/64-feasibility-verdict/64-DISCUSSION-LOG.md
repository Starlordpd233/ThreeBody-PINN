# Phase 64: Feasibility Verdict - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-10-24 to 2026-10-25
**Phase:** 64-Feasibility Verdict
**Areas discussed:** Verdict wording, Cost estimates, Charter draft, Next milestone (the owner selected all four), plus one todo cross-reference

---

## Todo cross-reference

| Option | Description | Selected |
|--------|-------------|----------|
| Don't fold (Recommended) | It is about stage labels and validation gates, which Phase 64 doesn't set. You declined it for Phase 60 for the same reason. | ✓ |
| Fold it in | Phase 64 would also have to plan and record the D-06 check. | |

**User's choice:** Don't fold
**Notes:** The todo is `.planning/todos/pending/d-06-static-epsilon-sensitivity-check.md`.

---

## Verdict wording

**Q1. How should the verdict present the rule's label next to what the evidence actually shows?**

| Option | Description | Selected |
|--------|-------------|----------|
| Side by side (Recommended) | The headline states RETHINK-REPRESENTATION and the 'design is the limit' clause exactly as pre-registered. Right beside them, a plain box: the network learned only the average position, its curves stayed flat, and only one setting was varied, so design versus training recipe is still open. Nothing pre-registered changes. | ✓ |
| Label first, evidence later | The headline is only the rule's output. The average-position finding appears in a later section. | |
| Amend the label | Formally amend the rule's wording, for example to 'representation or recipe'. Changing a pre-registered output after seeing the result needs a formal amendment with your sign-off (SCOPE-42 and SCOPE-43). | |

**Q2. Which candidate fixes should the verdict list for the next milestone to test?**

| Option | Description | Selected |
|--------|-------------|----------|
| Design and recipe (Recommended) | The pre-registered design changes (time-windowed networks, a different output frame, new input features or architecture, a shorter window), plus the untested recipe suspects beside them (learning rate, optimizer, schedule, depth). Unranked; trainex-r5 ranks them. | ✓ |
| Design changes only | Exactly the pre-registered list. Recipe suspects are left for trainex-r5 to raise. | |
| Rank them now | I rank all candidates in the verdict with my reasoning, and trainex-r5 then challenges the ranking. | |

**Q3. Add one figure: system 1632's real orbit beside the network's prediction, drawn from the committed weights (read-only, seconds on the CPU)?**

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, one figure (Recommended) | Shows at a glance that the prediction sits near the orbit's average while the real bodies move. Saved next to the verdict with its source and hash. | ✓ |
| No figure | Numbers and tables only, as in the Phase 59 and 60 findings. | |

**User's choice:** Side by side; Design and recipe; Yes, one figure. Then "Next area".
**Correction (2026-10-25, from `64-RESEARCH.md` finding 7):** the curves were not flat, as this question and the cost question said. `E` fell 25–50-fold in the first ~5% of training, then levelled off at 1.14–1.24, about 11–12 times the Tier-1 limit. The owner's choices are unaffected. CONTEXT D-01 and D-05 carry the corrected wording.
**Notes:** While writing CONTEXT.md, the agent checked the code. The frozen rule records `representation_limit_qualifier: false` on the G2 path without evaluating it (`feasibility_scorecard.py:735-752`). CONTEXT D-02 records how the verdict explains this.

---

## Cost estimates

**Q1. The accuracy curves stayed flat, so they give no basis for 'hours to the next level'. What should the cost section estimate?**

| Option | Description | Selected |
|--------|-------------|----------|
| Measured + for-scale (Recommended) | Hours spent per rung (22.4 h in Phase 60), the measured cost of one single-orbit experiment here (about 2.6 to 3 h), a costed first step for v2.5, and a clearly labelled for-scale figure for the finish from published step counts. Every assumption stated. | ✓ |
| Scenario table | Optimistic, middle and pessimistic hours to each ladder level, on the Mac and on a GPU, with each row's assumptions stated. | |
| Spent + not estimable | Hours spent and the per-experiment cost only. Next level and finish are marked 'not estimable until a design learns one orbit'. | |

**Q2. Which rented GPU should the estimate price? (This Mac can't measure a GPU speed-up, so it is given as a range.)**

| Option | Description | Selected |
|--------|-------------|----------|
| Consumer + data-center (Recommended) | One RTX 4090-class card and one A100/H100-class card, with current prices from two providers, looked up and dated. | |
| Data-center only | A100/H100-class pricing only. | |
| Consumer only | RTX 4090-class pricing only, the cheapest realistic option. | |

**User's choice:** None of the options. The owner answered in free text: "We will not have access to a rented GPU unless that is absolutely necessary and it is proven to make a difference. I will not invest into buying or renting a separate GPU for speeding up the work. The training process should be done on this Mac. does that make sense? tell me if this mac cannot handle the computation. I doubt that's the case. but that statement also requires lots of proofing and actual evidence to support. so I would be careful making any statements toward that"

**Q3 (asked in prose; it should not have been asked).** The agent offered A, Mac-only estimates plus a GPU tripwire (recommended), or B, keeping one GPU reference line.

**User's choice:** Neither. The owner wrote (2026-10-25): "For now, the only device on which we will do the computation will be on this MacBook, so ignore any proposal or route where it requires a rented GPU, either that is a cloud GPU or some other thing. That will not be something that we should consider at this point, so right now treat every single computation that will be needed done on this Mac. does that make sense? I don't know why you're keep asking about where we're doing the computation and trainig. I already set this requirement down a LONG TIME AGO, where I said this Mac will be where all the training/computation happens."

**Notes:**
- The owner was right. The rule had been in the trainex-r1 design (2026-06-10) and in `PROJECT.md` Constraints all along.
- The v2.4 amendment (2026-10-11) had put rented-GPU wording into ROADMAP criterion 3, FEAS-06 and FEAS-10, and the agent followed that wording without checking it against the standing rule.
- Corrected in `bb323a52`, and saved as a standing agent memory.

---

## Charter draft

**Q1. What is the project mainly for? The charter sets its pass bars from this.**

| Option | Description | Selected |
|--------|-------------|----------|
| Learning | Understand PINNs and the three-body problem by building one. Bars could be set against the simple baselines, for example beating the textbook formula on Stage 0. | ✓ (with Research paper) |
| Research paper | A publishable result. Bars would need to beat the formula, the copy-the-nearest-orbit baseline and the published results, on a held-out exam. | ✓ (with Learning) |
| Fast predictor | A tool that predicts orbits faster than Brutus at a stated accuracy. Bars would add a speed target next to accuracy. | |
| Not sure yet | I draft bars for each purpose side by side, and you pick at the checkpoint. | |

**User's choice (free text):** "1 and 2. we're not aiming for a perfect research result. I think this project could be more for like a PoC because not many people have done training PINN for 3 body porblems in the past. does that make sense? also, i'm just a freshman in college, and all i have this macbook. so reasonably we wouldn't achieve somethign great here. but it's just good to see some positive results coming out. also, why are you even asking all this?"

**Notes:** Before asking, the agent checked the planning files. No purpose was recorded anywhere. The agent stated these defaults, and the owner raised no objection:
- each charter item is pre-filled with options and a recommended answer;
- Stage 0 gets a real bar, and Stages 1–6 are marked open;
- GAP-59-08 is decided at checkpoint ①, beside the pass bars.

---

## Next milestone

No question was asked. The agent stated the default from 2026-10-24: v2.5, beginning with the trainex-r5 research round (open-book, diagnosis first). The verdict commits only to the milestone's name and first phase. The owner raised no objection.

---

## Claude's Discretion

- The structure and file names of the verdict and charter documents.
- The figure's styling and loading path.
- The layout of the readiness-ladder table.
- The plain-language wording.

## Deferred Ideas

- The D-06 static-epsilon todo (not folded).
- After the phase: the milestone close, the merge into master with the owner's OK, and the GitHub backup (a separate agent).
- Optional Phase 60 follow-ups: code review, security and validation.
