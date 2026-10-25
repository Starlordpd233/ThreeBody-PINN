# Phase 64: Feasibility Verdict - Context

**Gathered:** 2026-10-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 64 closes v2.4 on paper. It writes the feasibility verdict from the evidence that Phases 59 and 60 already committed, and drafts the one-page project charter for the owner. It trains nothing and does not spend the held-out exam.

It delivers:
- **The verdict document** (FEAS-06; ROADMAP Phase 64 criteria 1–4). The ladder stopped at Gate G2 with no rescue, so the frozen rule's output is RETHINK-REPRESENTATION. Phases 61–63 were skipped at G2, not failed.
- **The readiness-ladder placement** (levels 0–9), with the evidence for each level.
- **Cost:** the machine hours spent, plus cost estimates, on this Mac only.
- **The next milestone,** named.
- **The charter draft** (FEAS-10; criterion 5), presented at owner checkpoint ①. That checkpoint blocks the milestone's close.
- **VER-22,** re-verified against the final requirement count (criterion 6).

Out of scope:
- new training or tuning runs;
- the held-out exam;
- any change to the frozen scorer, the frozen decision rule or a pre-registered output;
- the trainex-r5 research itself (v2.5);
- resolving GAP-59-08 (the owner decides it at checkpoint ①);
- merging v2.4 into master;
- the GitHub backup.

</domain>

<decisions>
## Implementation Decisions

### Verdict wording
- **D-01: Side by side.**
  - The headline states the frozen rule's output exactly as pre-registered: RETHINK-REPRESENTATION, for "G2 fired and the sweep rescued nothing".
  - Directly beside it, a plain box states what the evidence shows. Source: `60-VERIFICATION.md`, "Independent observation for Phase 64".
    - Every trained network learned only each body's average position, so it is a time-constant predictor.
    - Its accuracy curves levelled off early. `E` fell 25–50-fold in the first ~5% of training, then settled at 1.14–1.24, about 11–12 times the Tier-1 limit (`64-RESEARCH.md`, finding 7). Do not call them "flat".
    - The sweep varied only `first_omega_0`.
    - So the records cannot yet tell a design limit from a limit of the fixed training recipe.
  - Nothing pre-registered changes and the label is not amended. Amending it after seeing the result would need a formal amendment with the owner's sign-off (SCOPE-42, SCOPE-43). The owner chose "Side by side".
- **D-02: Explain the qualifier field plainly.** This item comes from the agent reading the code. It is not an owner choice.
  - `stop-handoff.json` records `representation_limit_qualifier: false`. `decision_verdict` returns `false` on the G2 path without evaluating the qualifier, and it refuses a Rung 1 comparison input on that path (`pinn/verification/feasibility_scorecard.py:734-752`).
  - The amendment's text applies the qualifier "whatever the branch" (`docs/work/designs/cross_cutting/v2.4-milestone-proposal/2026-10-11-v2.4-feasibility-amendments.md:187-189`).
  - The two do not conflict in substance. On this branch the label already names the representation as the limit. On the committed numbers the qualifier's condition also holds: Rung 1 is Tier 0 on all three systems, and its E is lower than the formula's only on 4658.
  - The verdict reports the field exactly as recorded. It adds one plain sentence: here `false` means "not evaluated on this branch", not "the condition failed". The verdict does not recompute or change the field.
- **D-03: Candidate fixes for the next milestone, unranked.** The owner chose "Design and recipe".
  - The pre-registered design changes: time-windowed networks, a different output frame, new input features or architecture, a shorter window (REQUIREMENTS "On RETHINK-REPRESENTATION" routing).
  - The untested recipe suspects beside them: learning rate, optimizer, schedule, depth.
  - trainex-r5 ranks them, not this phase.
- **D-04: One figure.** It shows system 1632's real orbit beside the network's prediction.
  - It is drawn read-only from the committed weights and takes seconds on the CPU.
  - It is saved next to the verdict, with its source paths and SHA-256 hashes.
  - The owner chose "Yes, one figure".

### Cost estimates
- **D-05: Measured + for-scale.** The owner chose "Measured + for-scale". The cost section gives:
  - the hours spent per rung, from `stop-handoff.json`: 22.378 h of arm wall time in Phase 60, plus each arm's wall hours and timed seconds per step (about 0.011–0.0136 s);
  - the measured cost of one single-orbit experiment on this Mac (about 2.6–3 h for most arms; the exact per-arm values are in `stop-handoff.json`);
  - a costed first step for v2.5;
  - a clearly labelled for-scale figure for the finish, from published step counts (amendments doc `:227-230`: generation 7 at 12.3 s per step × about 200,000 Adam steps ≈ a month of nonstop computing).

  Every assumption is stated. "Hours to the next level" is not projected, because the curves levelled off far above Tier 1.
- **D-06: This Mac only.** All computation runs on the owner's Mac (Apple M5 Pro, 24 GB). This is a standing owner rule (`.planning/PROJECT.md` Constraints; trainex-r1 design, 2026-06-10). The owner restated it twice in this discussion.
  - The verdict, the charter and the next-milestone proposal contain no GPU figures, prices, speed-up assumptions, tripwires or GPU-dependent routes.
  - The amendments doc's rented-GPU clause (`:222-225`) is superseded. ROADMAP criterion 3, FEAS-06 and the FEAS-10 budget item were corrected in `bb323a52`.
  - No claim that the Mac can or can't handle a workload is made without measured evidence. Where a projection is unknown, the verdict says so and names what would measure it.
  - The charter records the owner's words under its budget item. Latest statement, verbatim: "For now, the only device on which we will do the computation will be on this MacBook, so ignore any proposal or route where it requires a rented GPU, either that is a cloud GPU or some other thing. That will not be something that we should consider at this point, so right now treat every single computation that will be needed done on this Mac."
  - Earlier statement, verbatim: "We will not have access to a rented GPU unless that is absolutely necessary and it is proven to make a difference. I will not invest into buying or renting a separate GPU for speeding up the work. The training process should be done on this Mac. does that make sense? tell me if this mac cannot handle the computation. I doubt that's the case. but that statement also requires lots of proofing and actual evidence to support. so I would be careful making any statements toward that"

### Charter draft (FEAS-10)
- **D-07: Purpose.** The owner's answer, verbatim (2026-10-25): "1 and 2. we're not aiming for a perfect research result. I think this project could be more for like a PoC because not many people have done training PINN for 3 body porblems in the past. does that make sense? also, i'm just a freshman in college, and all i have this macbook. so reasonably we wouldn't achieve somethign great here. but it's just good to see some positive results coming out."
  - "1 and 2" are the first two options offered: Learning and Research paper.
  - Read together, this is a learning project whose research output is a proof of concept, a modest positive result rather than a polished paper.
  - The charter records the answer verbatim. The definition of done and the pass bars are drafted from it.
- **D-08: Pre-filled draft.**
  - Every charter item gets a few options and a recommended answer, already filled in, so the owner can approve the page as it stands or change single lines at checkpoint ①.
  - Items the owner leaves open are recorded as open.
  - This was the agent's default, stated to the owner on 2026-10-25 with no objection. The owner asked why so many questions were needed, so checkpoint ① should take as little of the owner's effort as possible.
- **D-09: Pass bars.** This was the agent's default, stated with no objection.
  - Stage 0 gets a concrete proposed bar, with a position criterion and an energy criterion (never energy alone), fixed before any held-out exam.
  - The bar aims at a reachable positive result for a proof of concept. It is set against the comparison points: the two-Kepler formula, the nearest-neighbour copy, Breen et al. (arXiv:1910.07291) and the 2026 PINN study (arXiv:2607.23501).
  - Stages 1–6 are listed and marked open.
  - On `10⁻⁵`, the draft recommends replacing it, by formal amendment, with a bar based on evidence. That follows the owner's recorded lean (amendments doc `:235`). Moving a locked value is outside the delegation, so the owner decides.
- **D-10: GAP-59-08 at the checkpoint.** This was the agent's default, stated with no objection.
  - Its options A, B and C (`59-GAPS.md`; A is recommended) sit beside the pass bars, because the energy criterion depends on how energy is measured.
  - Today's finite-difference check gives even the exact Brutus orbits 5–38% error.
  - Any proposed energy bar is written as conditional on the owner's answer.
- **D-11: Budget.** The budget is how many months of computing on this Mac. The draft offers options and a recommendation. It states the measured per-experiment cost from D-05 so the owner can size it.
- **D-12: Stop rule.** FEAS-10's draft text is the recommended default: "a milestone that neither climbs a ladder level nor beats the best fixed-scorecard result means stop or change approach, with no third attempt at the same idea."
  - Today's best result is effectively a constant predictor, so "beats" needs a stated margin.
  - The draft proposes one as the default, and the owner decides (`64-RESEARCH.md`, Open Question 2).
- **D-13: Routed items the charter records.**
  - `ctl_instruction.md`'s evaluation section (`:2057`, `:2081`, `:2111`) describes results that do not exist. Its rewrite is routed to the milestone that sets the bars.
  - `PROJECT.md`'s "What This Is" and Core Value still describe the LLM project. A rewrite matching the charter is drafted and applied only on the owner's approval at checkpoint ①.
    - The title line and the Model constraint also still describe the LLM project.
    - One extra pre-filled line offers to rewrite those too (`64-RESEARCH.md`, Open Question 3).
  - GAP-64-01 (`64-GAPS.md`) asks how the 12 requirements of Phases 61–63 are labelled at close, and whether they carry forward to v2.5.
    - It appears as one pre-filled line, with option A as the default.
    - The close task applies it only as the owner approves.

### Next milestone
- **D-14: v2.5, committed only to its name and first phase.**
  - The first phase is the trainex-r5 research round: open-book (Route B), diagnosis first, on why every trained network predicts a time-constant position.
  - `/gsd-new-milestone` plans the later phases.
  - Work continues in `.worktrees/trainex`.
  - This was recommended on 2026-10-24 and the owner proceeded on that basis. It was restated as the default on 2026-10-25 with no objection.

### Claude's Discretion
- The verdict and charter documents: structure and file names. The v2.0 precedent keeps them in the phase directory: `.planning/milestones/v2.0-phases/43-verification-stage-0-pilot-acceptance/43-VERDICT.md`.
- The figure: its styling, and how its script loads the weights. Reuse the Phase 60 verifier's real-data loading path.
- The layout of the readiness-ladder evidence table.
- Plain-language wording throughout. The owner is a first-year student, so lead with what happened and define each term once.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase contract
- `.planning/ROADMAP.md`: Phase 64 (success criteria 1–6; criterion 3 corrected in `bb323a52`).
- `.planning/REQUIREMENTS.md`: FEAS-06 (`:143`), FEAS-10 (`:196`), VER-22, and the "On RETHINK-REPRESENTATION" future routing.
- `.planning/PROJECT.md`: Constraints (Hardware: this Mac only), "What This Is" and Core Value (to be rewritten on approval).

### Design sources
- `docs/work/designs/cross_cutting/v2.4-milestone-proposal/2026-10-11-v2.4-feasibility-amendments.md`:
  - the verdict branches and the qualifier (`:160-196`);
  - the readiness ladder (levels 0–9);
  - the cost model (`:217-231`), whose rented-GPU clause is superseded by D-06;
  - the owner's lean on `10⁻⁵` (`:235`);
  - the pass-bar rules (`:246` onward).
- `docs/work/designs/cross_cutting/v2.4-milestone-proposal/2026-10-09-v2.4-roadmap-proposal.md`: the original v2.4 proposal.

### Phase 60 evidence (the verdict's inputs)
- `.planning/phases/60-single-system-learnability/evidence/g2/stop-handoff.json`: the single handoff, holding:
  - the frozen rule's output;
  - per-arm wall hours and seconds per step;
  - the total of 22.378 h;
  - `level3` "not tested (skipped at G2)".
- `.planning/phases/60-single-system-learnability/evidence/g2/{g2-outcome.json,sweep-curve.json,skip-records.json}`.
- `.planning/phases/60-single-system-learnability/evidence/arms/*/{record.json,adam.weights,polish.weights}`: per-arm results, accuracy traces and the committed weights the figure uses.
- `.planning/phases/60-single-system-learnability/evidence/verify_phase60_evidence.py`.
- `.planning/phases/60-single-system-learnability/60-FINDINGS.md`.
- `.planning/phases/60-single-system-learnability/60-VERIFICATION.md`: see "Independent observation for Phase 64".

### Phase 59 evidence (comparison points, survey, open gap)
- `.planning/phases/59-read-only-baseline-scorecard/59-FINDINGS.md`.
- `.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md`: GAP-59-08, open and owner-routed.
- `.planning/phases/59-read-only-baseline-scorecard/evidence/baselines/{two_kepler_population.csv,two_kepler.json,nn_copy.json,baselines.json}`.
- `.planning/phases/59-read-only-baseline-scorecard/evidence/survey/` (FEAS-08).
- `.planning/phases/59-read-only-baseline-scorecard/evidence/scorecard-freeze.json`.
- `.planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py`.

### Frozen code (read only)
- `pinn/verification/feasibility_scorecard.py`: `decision_verdict` (`:718-776`); the G2 path is at `:734-752`.
- `pinn/verification/feasibility_scorer.py`.

### Spec section the charter routes
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`: `:2057`, `:2081`, `:2111` (evaluation section).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `verify_phase60_evidence.py` recomputes every Phase 60 number from committed files. Its `rescore` mode loads the committed weights through the real data context, so the figure script and the verdict's number checks can reuse that path.
- `verify_phase59_evidence.py` and `evidence/baselines/` give the comparison points per system.

### Established Patterns
- Evidence records cite the path and SHA-256 of every input. Verifiers re-derive numbers rather than trusting summaries.
- The tests under `tests/phase59/` and `tests/phase60/` use unittest. The phase-60 discovery takes about 13 minutes, so treat it as expensive and keep its full output outside the repo.
- Before a plan relies on a new verifier mode, smoke-test it read-only on the real committed files. Phase 60's verifier crashed on first real use twice.
- Planning files are edited by hand and committed as `docs(planning)`. All commits go through `scripts/agent-commit`.

### Integration Points
- The verdict reads `evidence/g2/stop-handoff.json`.
- Checkpoint ① is the owner decision near the end of execution, and it blocks `/gsd-complete-milestone`.
- On approval, `PROJECT.md` "What This Is" and Core Value are rewritten.
- VER-22 is checked against the final requirement count in `REQUIREMENTS.md`.

</code_context>

<specifics>
## Specific Ideas

- **Proof-of-concept framing.** The owner frames the project as a proof of concept by a first-year student with one MacBook: "it's just good to see some positive results coming out". The verdict and charter should say plainly what a positive result would look like at Stage 0, and should neither oversell nor undersell.
- **Prior work.** The owner believes few people have trained PINNs on the three-body problem. The verdict states briefly what the two published comparison points did, so any proof-of-concept claim is scoped accurately against them. The Phase 59 survey and the amendments doc hold what the repo knows about them.
- **Headline numbers.** These were checked against the committed records on 2026-10-25. The verdict re-derives each one rather than copying it.

  | System | Rung 1 E | Formula E | Rung 1 `ε_H` |
  |---|---|---|---|
  | 1632 | 1.1574 | 0.9168 | 705.69 |
  | 851 | 1.2375 | 0.4312 | 165.50 |
  | 4658 | 1.1432 | 1.9697 | 13127.5 |

  - Every result in the table is Tier 0.
  - The best `ε_H` is 123.62, from sweep arm `g2s-1632-w240`.
  - Total arm wall time is 22.378 h.

</specifics>

<deferred>
## Deferred Ideas

### Reviewed Todos (not folded)
- `.planning/todos/pending/d-06-static-epsilon-sensitivity-check.md` is about stage labels and validation gates, which Phase 64 doesn't set. The owner declined it for Phase 60 for the same reason. Its "D-06" is an earlier phase's decision number, not this file's D-06.

### After Phase 64
- `/gsd-complete-milestone` for v2.4.
- Merging v2.4 into master, only with the owner's explicit OK.
- The GitHub backup, handled by a separate agent.

### Optional Phase 60 follow-ups (user-invoked, not Phase 64 work)
- `/gsd-code-review 60`, `/gsd-secure-phase 60`, `/gsd-validate-phase 60`.
- `60-VALIDATION.md` is still `status: draft`.
- The `plan_head_before` in `60-13-SUMMARY.md` is malformed.

</deferred>

---

*Phase: 64-Feasibility Verdict*
*Context gathered: 2026-10-25*
