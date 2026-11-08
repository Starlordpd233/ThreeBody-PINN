# Roadmap: 3-Body Problem Physics-Inspired LLM

## Milestones

- ✅ **v1.0 Codebase Cleanup** — Phases 1–4 (shipped 2026-03-20; [archive](milestones/v1.0-ROADMAP.md))
- ✅ **v1.1 LaTeX Modularization Verification** — Phases 5–8 (shipped 2026-03-22)
- ✅ **v1.2 PINN Implementation Readiness** — Phase 9 (shipped 2026-05-08)
- ✅ **v1.3 Markdown Conversion Verification & Correction** — Phases 10–15, 15.1 (shipped 2026-05-08; [archive](milestones/v1.3-ROADMAP.md))
- ✅ **v1.4 Resolving 01 Architecture and Physics Foundations** — Phases 16–22, including 20.5 (shipped 2026-06-09; [roadmap archive](milestones/v1.4-ROADMAP.md), [requirements archive](milestones/v1.4-REQUIREMENTS.md), [phase archive](milestones/v1.4-phases/))
- ✅ **v1.5 Resolving 02 Data Pipeline and Validation** — Phases 23–29, including 24.5 (shipped 2026-06-17; archived under [`milestones/v1.5-*`](milestones/))
- ✅ **v1.6 Resolving 03 Curriculum and Training Loop** — Phases 30–36 (shipped 2026-07-02; 32/32 requirements, 26/26 acceptance probes PASS, ledger 18/18 VERIFIED; FUT-01/FUT-04 routed to the trainex track; archived under [`milestones/v1.6-*`](milestones/))
- ✅ **v2.0 CTL-PINN Training Viability Slice** — Phases 37–43 (shipped 2026-07-23; the project's first **build** milestone / trainex track — Stage-0-first end-to-end training slice from the ratified trainex-r1a decisions; 42/42 requirements Complete; audit `tech_debt` with zero blockers; the sole held-out physics gate rendered an honest **FAIL** (`ε_H = 237.21` vs ≤ 1e-5) and the owner signed **`adjust`** — Stage-0 mechanical slice retained, PLAT-01..07 blocked, physics-gate investigation routed to the next milestone; archived under [`milestones/v2.0-*`](milestones/))
- ✅ **v2.1 Physics-Gate Investigation & trainex-r2 Research Package** — Phases 44–45 (shipped 2026-07-24; the separately governed investigation routed by the v2.0 `adjust` verdict — read-only forensics over the retained v2.0 artifacts + trainex-r2 ERW package delivery; 7/7 requirements, package audited PASS; a bounded conformance audit found the v2.0 pilot diverged from the locked specs in five verified respects, qualifying the Phase 44 diagnosis and seeding a conformance-first next milestone; archived under [roadmap](milestones/v2.1-ROADMAP.md), [requirements](milestones/v2.1-REQUIREMENTS.md), [gaps](milestones/v2.1-GAPS.md), [phase archive](milestones/v2.1-phases/))
- ⚠️ **v2.2 Stage-0 Conformance Repair & Valid Re-Run** — Phases 46–52 (started 2026-07-25; **closed incomplete 2026-08-17**; repaired all nine verified Stage-0 conformance divergences (Phases 46–49, CONF/INST/GATE/TEST-01..09 Complete) and re-ran Stage-0 under the corrected recipe (Phase 50), but the conformant run HALTed at the invariant-B causal-front gate, step 501 — a bounded 2026-08-17 conformance audit found this is a property of the locked architecture at initialization (SIREN second-derivative scale vs. causal-weight calibration), not a further conformance defect, with no remedy available inside v2.2 (SCOPE-30); owner selected `stop-incomplete` (RUN-01/RUN-02 unsatisfied), the sole held-out evaluation was preserved unspent (RUN-03/EVAL-01 not attempted), and DIAG-05/VER-19/VER-20 were discharged in adapted form (Phase 52); 20/24 requirements Complete, 2 closed incomplete, 2 not attempted; archived under [`milestones/v2.2-*`](milestones/); routes to v2.3)
- ⚠️ **v2.3 Causal-Weight/SIREN-Scale Recipe Adjudication** — Phases 53–58 (started 2026-08-18; **closed 2026-10-04 on the declared terminal state**; codified the four research-free VER-20 items (Phase 53), obtained the owner-delegated recalibration ruling `A1 + B2 + C1 + D3 + E1` through the `trainex-r3` ERW round (Phase 54), landed the architecture characterization probe (Phase 55), and wrote the ruling into `pinn_architecture.md` as a SCOPE-38 contract amendment with the fail-closed train-free gate GATE-04 passing (Phase 56); the Stage-0 re-run (Phase 57) produced no graded result in generations 1–6, and generation-7 graded seed 42 tripped invariant B at step 951 (front stuck at 2 since step 450), so seeds 41/43 were not launched and the sole held-out evaluation stays preserved unspent; owner verdict **`rethink`** (2026-10-03): RUN-04/RUN-05 closed incomplete, EVAL-02 not attempted, Stage-1+/PLAT-01..07 still blocked; 12/15 requirements Complete; archived under [roadmap](milestones/v2.3-ROADMAP.md), [requirements](milestones/v2.3-REQUIREMENTS.md), [gaps](milestones/v2.3-GAPS.md), with the phase folders left in `phases/`; routes to ERW round `trainex-r4`)
- ⚠️ **v2.4 Stage-0 Feasibility Checkpoint** — Phases 59–64 (started 2026-10-09; **closed 2026-10-26 on its pre-registered exit at Gate G2**; froze the feasibility scorecard, its comparison points and the whole-dataset survey read-only (Phase 59, Gate G1 proceed); built and sealed the INST-05 learnability harness and ran Rung 1 on systems 1632, 851 and 4658 plus the four-setting `first_omega_0` sweep — every arm ended at Tier 0, so G2 fired with no rescue and Phases 61–63 were skipped, not failed (Phase 60); every trained network learned only each body's average position; the frozen rule's verdict **`RETHINK-REPRESENTATION`** was stated unamended with the one-page charter (Phase 64); owner decision **`change-course`** (2026-10-26) with all charter rows open; 12/24 requirements Complete, the 12 skipped-phase requirements Pending (C-14 open); milestone audit `gaps_found` for those twelve only, override closeout; no graded run and no held-out evaluation; archived under [roadmap](milestones/v2.4-ROADMAP.md), [requirements](milestones/v2.4-REQUIREMENTS.md), [audit](milestones/v2.4-MILESTONE-AUDIT.md), [gaps](milestones/v2.4-GAPS.md), with the phase folders left in `phases/`; routes to v2.5's `trainex-r5` research round)
- 🚧 **v2.5 Root-Cause Confirmation** — Phases 65–69 (started 2026-10-27; **in progress**). It finds out why every v2.4 network learned only each body's average position, before any redesign. Each of the owner's three suspects is tested by a cheap experiment on this Mac, with its predictions committed before it runs: the network is too small, the metrics are too harsh, or the training pipeline is wrong. The yardstick is also checked against known answers, and the owner sets the pass bars. The milestone ends with a findings page and the owner's choice of v2.6 redesign direction. 13 requirements (DIAG-09, INST-08, EXP-01..05, YARD-01..03, VERD-01..02, VER-23); scope boundaries SCOPE-45..49; no graded run and no held-out evaluation; phases after the first experiment are provisional (SCOPE-49). Branch `milestone/v2.5`.
- 🔮 **Final Publication LaTeX Sync** — deferred until implementation, network/training design, training, and research-result interpretation are complete

## Deferred: Final Publication LaTeX Sync

**Goal:** Refresh LaTeX/PDF publication sources from the final authoritative markdown framework specs.

**Preconditions:**

- Implementation complete (FUT-01 or successor milestone)
- Network design stable
- Training and research results complete
- No active framework-spec iteration expected

**Non-goal:** Maintaining `.tex` parity during active development milestones.

**Source of truth:** Markdown framework specs (`pinn_instruction/markdown_conversion/framework-specs/*.md`) at final sync start.

**Historical note:** This supersedes the earlier draft `v1.6.5-latex-sync` timing from the May 24, 2026 design document.

## 🚧 v2.5 Root-Cause Confirmation (Planning)

**Milestone Goal:** Find out why every v2.4 network learned only each body's average position, using cheap pre-registered experiments on this Mac, so that v2.6 redesigns against a confirmed cause. Each of the owner's three suspects gets a test:

1. **the network is too small:** a smaller, shallower network on the same orbit, and a depth ladder;
2. **the metrics are too harsh:** known-answer checks of every metric, then the owner sets the bars;
3. **the training pipeline is wrong:** a learning-rate ladder for the training settings; the physics half waits for v2.6, because it cannot be judged until a network fits one orbit.

The lead is the 2026-10-27 probe. It reported low neighbour similarity in deeper hidden states while the trained networks predicted average positions. Phase 65 reproduced that association; a cause has not been established.

**What this milestone deliberately does not do:**

- redesign or rebuild the network, or edit a framework spec (v2.6);
- fix the physics-term defects (carried into v2.6 by name);
- spend a graded run or the preserved held-out evaluation;
- assemble `trainex-r5` (the owner decides at the close whether to commission it).

**Granularity:** standard. 5 phases, 13 requirements: DIAG-09, INST-08, EXP-01..05, YARD-01..03, VERD-01..02, VER-23.
**Coverage:** 13/13 v2.5 requirements mapped at roadmap creation. VER-23's binding check is at the close, against the final requirement count, including anything added under SCOPE-49.
**Branch:** work continues in `.worktrees/trainex` on `milestone/v2.5`, created 2026-10-27 from `milestone/v2.4` at `dac9d9c1`.

- Its first commits repoint the Phase 64 verifier at the v2.4 project archive (`dbc96887`), start the milestone (`633f8eb4`) and define the requirements (`85c1a930`).
- Commits are per-plan and atomic, via `scripts/agent-commit` with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS` set.
- No push to protected branches. `master` stays governance-only, and integration is user-controlled.

**Source:** the owner's direction in the 2026-10-27 `/gsd-new-milestone` session, recorded in `PROJECT.md` "Current Milestone: v2.5" (`633f8eb4`) and `REQUIREMENTS.md` (`85c1a930`). The roadmap is generated inline, following the v2.0–v2.4 precedent.

### Diagnosis discipline (applies to all phases)

- **Hard boundaries (SCOPE-45..49):**
  - **Stage 0, training-split records only.** No graded run, no held-out evaluation, no test-split file. The preserved evaluation stays unspent.
  - **No spec edits, no locked value moves.** Settings vary only inside the INST-08 harness, whose records are diagnostic and refused by the graded-run path.
  - **One committed prediction page per experiment before its first run.** No reading rule is re-set after a result is seen.
  - **Compute on this Mac only.** Budgets come from a measured seconds-per-step. A run over an hour uses the governed pause, resume and power-guard tooling.
- **Measure in physical units.** Every experiment is scored by the frozen FEAS-01 scorer, beside the two-Kepler formula and the constant predictor. Loss values are context, not scores.
- **A result confirms only when it repeats.** It must hold on a second panel system and a second seed before the findings call it confirmed.
- **The plan may pivot (SCOPE-49).** After each experiment's result, the agent compares it with the prediction page and with this roadmap.
  - When a result refutes the lead or opens a new question, the agent proposes the change: an inserted phase such as 66.1, a dropped phase, re-aimed later phases, or a new requirement.
  - The owner decides. The roadmap is neither forced against the evidence nor changed without the owner.
  - Phases 67–69 are provisional until Phase 66's review.
- **Delegation and gaps.**
  - Technical rulings inside the pre-registered branches proceed under the owner's delegation, and are reported with their rationale at each phase gate.
  - A source-silent semantic decision is still recorded in the phase-local `NN-GAPS.md` and the milestone index `.planning/milestones/v2.5-GAPS.md` (created on the first gap), with every STOP-protocol field.
  - These go to the owner:
    - a plan change;
    - the yardstick choices (C-7, C-2, C-4..C-6);
    - the redesign direction;
    - anything that would move a locked value or spend the evaluation.
- **Owner checkpoints:**
  1. plan changes under SCOPE-49, including the review after Phase 66;
  2. the yardstick (YARD-02, YARD-03, Phase 68);
  3. the close (VERD-02, Phase 69).
- **Verification lesson.** Code is checked against what it claims mechanically. A passing plan verification is not evidence: v2.0's pilot and generation 7 both passed their verifications while diverging.

## Phases

**Phase Numbering:** integer phases 65–69 continue from v2.4's Phase 64 (numbering does not reset). Decimal phases, such as 66.1, are for insertions under SCOPE-49. The phase folders 53–60 and 64 stay in `.planning/phases/` beside them.

- [x] **Phase 65: Probe on the Record & Fit Harness** — The 2026-10-27 probe re-run as a committed, read-only step on the seven v2.4 networks, with its earlier figures as the predictions. Then the minute-scale harness that trains one named network variant, data-only, on one training orbit and logs, layer by layer, how alike the network's state is at neighbouring times. (DIAG-09, INST-08)
- [x] **Phase 66: Small-Network Control** — The cheapest, most decisive test first: does a smaller, shallower network fit orbit 1632 from time alone? Reaching Tier 1 refutes "too small" for one orbit. The result is reviewed against the plan before anything else runs. **Owner checkpoint ①.** (EXP-01) (completed 2026-11-01)
- [x] **Phase 67: Design & Settings Ladders** *(provisional until Phase 66's review)* — Four experiments on the locked layer types, each with its own prediction page: (completed 2026-11-08)
  - depth: 2, 4, 6, 8 and 12 layers;
  - learning rate: 10⁻³ down to 10⁻⁵;
  - time-input design: time features matched to the orbit's speed;
  - window length: 1, 2, 5 and 10 inner laps.

  They separate "the design" from "the training settings". (EXP-02, EXP-03, EXP-04, EXP-05)
- [x] **Phase 68: Yardstick** — Known-answer checks of every metric and gate, read-only. Brutus's exact answer must pass; the constant predictor must fail every accuracy bar. Then the owner decides how energy error is measured (GAP-59-08) and sets the definition of done and the Stage-0 bars, including whether the 10⁻⁵ bar stays. It does not depend on the experiments. **Owner checkpoint ②.** (YARD-01, YARD-02, YARD-03) (completed 2026-11-08)
- [ ] **Phase 69: Findings & Redesign Decision** — One page marks each suspect, and the probe's lead, as confirmed, refuted or open, with numbers. The owner picks the v2.6 redesign direction and decides whether to commission `trainex-r5`. Traceability is re-verified at close. **Owner checkpoint ③.** (VERD-01, VERD-02, VER-23)

## Phase Details

### Phase 65: Probe on the Record & Fit Harness

**Goal**: The probe's lead is either on the record or withdrawn, and a tested harness can train and score any named network variant on one orbit in minutes.
**Depends on**: Nothing. This is the first v2.5 phase.
**Requirements**: DIAG-09, INST-08
**Gate**: if the probe does not reproduce, the lead is withdrawn. The agent proposes re-aiming Phases 66–67 (owner checkpoint ①), and under order A `trainex-r5` would run on the diagnosis.
**Success Criteria** (what must be TRUE):

  1. The probe script and the 2026-10-27 figures, as predictions with a reproduction tolerance, are committed before it runs. Each figure is recorded as reproduced or not on all seven arms, at initialization and after training, with every weight file checked by SHA-256 before loading.
  2. The harness's tests pass:
     - its 12-layer locked variant gives the production network's forward pass at the same seed and weights;
     - it scores with the frozen FEAS-01 scorer;
     - its similarity logger reproduces the probe's value on one committed arm;
     - test-split paths are refused, and the graded-run and evaluator paths refuse its records.
  3. A short run on orbit 1632 completes and is scored. Its measured seconds per step is recorded, and sets the budgets for Phases 66–67.
  4. No training step ran in the probe, and no test-split file was opened. The tooling asserts this.

**Plans**: 6/6 complete. Closed 2026-10-31 under delegated technical review; see `65-CLOSEOUT.md` and `65-VERIFICATION.md`.
**Wave 1**

- [x] 65-01-PLAN.md

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 65-02-PLAN.md

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 65-03-PLAN.md

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 65-04-PLAN.md

**Wave 5** *(blocked on Wave 4 completion)*

- [x] 65-05-PLAN.md

**Wave 6** *(blocked on Wave 5 completion)*

- [x] 65-06-PLAN.md

### Phase 66: Small-Network Control

**Goal**: The project knows whether a network smaller than the locked one can fit one Stage-0 orbit, which settles whether "too small" can explain v2.4's failure.
**Depends on**: Phase 65 (the harness and its measured rate).
**Requirements**: EXP-01
**Gate (owner checkpoint ①)**: the result is reviewed against the plan before Phase 67 starts. These branches are pre-registered (`REQUIREMENTS.md`, "How the first results can reshape the plan"):

- **Tier 1 on 1632:** "too small" is refuted for one orbit, and Phase 67 runs as planned to find which part of the locked design fails.
- **Near the constant predictor's `E`:** the lead does not explain the failure on its own. The agent proposes an inserted phase that checks the path from the data to the scorer first.
- **Anything else:** it goes to the owner.

**Success Criteria** (what must be TRUE):

  1. A prediction page is committed before the first run. It gives the network's architecture and parameter count (fewer layers and parameters than the locked network), what each suspect predicts, the budget from the measured rate, and the reading rule.
  2. The result on orbit 1632 is scored: tier, `E` against the constant predictor and the two-Kepler formula, and the neighbour-similarity trace. A confirming result is repeated on a second panel system and a second seed.
  3. The review is recorded: the branch taken, the plain-language reading, and any plan change proposed under SCOPE-49 with the owner's answer.

**Plans**: 5 plans in 5 waves (planned 2026-10-31). 66-03 and 66-04 run only in the owner's weekend AC window.
**Wave 1**

- [x] 66-01-PLAN.md

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 66-02-PLAN.md

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 66-03-PLAN.md

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 66-04-PLAN.md

**Wave 5** *(blocked on Wave 4 completion)*

- [x] 66-05-PLAN.md

### Phase 67: Design & Settings Ladders

**Goal**: The project knows which part of the locked setup turns the network's view of time to noise: its depth, its training settings, its time input or the window length.
**Depends on**: Phase 66 and its review. The phase is provisional: the review may re-aim, reorder or drop its experiments.
**Requirements**: EXP-02, EXP-03, EXP-04, EXP-05
**Success Criteria** (what must be TRUE):

  1. Each experiment has its prediction page committed before its first run.
  2. The depth ladder records `E`, tier and per-layer neighbour similarity at 2, 4, 6, 8 and 12 layers. The learning-rate ladder records the same, with the similarity trace through training, at each rate.
  3. The time-input design and the window-length experiments each record `E`, tier and similarity for every variant, on the locked depth and, for time input, on the Phase 66 network.
  4. Every confirming result is repeated on a second panel system and a second seed, and every result is reviewed against the plan under SCOPE-49.

**Plans**: 16 plans in 15 waves (planned 2026-11-01). Waves 7-14 run only in the owner's weekend AC window.
**Wave 1**

- [x] 67-01-PLAN.md

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 67-02-PLAN.md
- [x] 67-03-PLAN.md

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 67-04-PLAN.md

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 67-05-PLAN.md

**Wave 5** *(blocked on Wave 4 completion)*

- [x] 67-06-PLAN.md

**Wave 6** *(blocked on Wave 5 completion)*

- [x] 67-07-PLAN.md

**Wave 7** *(blocked on Wave 6 completion)*

- [x] 67-08-PLAN.md

**Wave 8** *(blocked on Wave 7 completion)*

- [x] 67-09-PLAN.md

**Wave 9** *(blocked on Wave 8 completion)*

- [x] 67-10-PLAN.md

**Wave 10** *(blocked on Wave 9 completion)*

- [x] 67-11-PLAN.md

**Wave 11** *(blocked on Wave 10 completion)*

- [x] 67-12-PLAN.md

**Wave 12** *(blocked on Wave 11 completion)*

- [x] 67-13-PLAN.md

**Wave 13** *(blocked on Wave 12 completion)*

- [x] 67-14-PLAN.md

**Wave 14** *(blocked on Wave 13 completion)*

- [x] 67-15-PLAN.md

**Wave 15** *(blocked on Wave 14 completion)*

- [x] 67-16-PLAN.md

**Cross-cutting constraints:**

- All 15 arm/case timing rows measure this experiment's cost; no Phase65/66 rate determines its budget, per D-07/D-08/D-09.
- Every science row receives one common cost-only N with the exact cadence, controls and repeats frozen prospectively, per D-08/D-10.
- Every real attempt is serial, single-use, TRAIN-only, supervised below one hour and admitted on this Mac during weekend AC eligibility, per D-07/D-12/D-13.
- E, frozen tier, same-window comparisons and every-layer adjacent-time trace are reported against the committed prediction, per D-11/D-13.
- No main-only result, tie, opposed repeat, unsettled endpoint or small effect is presented as confirmation, per D-08/D-09.
- A result-driven scope/resource/out-of-rule change blocks dependent work until an actual owner ruling; registered in-scope branches proceed under D-01/SCOPE-47/SCOPE-49.
- Frozen scorer, pass bars, production settings and all historical evidence remain unchanged, per D-11/D-12.

### Phase 68: Yardstick

**Goal**: Every metric that judges a result is known to pass a perfect answer and fail a useless one, and the owner has set the bars that v2.6 will aim at.
**Depends on**: Nothing in v2.5's experiments. It uses only the frozen scorer, the gates and Brutus data, and may run at any point before Phase 69.
**Requirements**: YARD-01, YARD-02, YARD-03
**Success Criteria** (what must be TRUE):

  1. A committed, re-derivable table shows, for every metric and gate, the result for Brutus's exact answer and for the constant predictor on the three panel systems. Every metric that the constant predictor passes is named.
  2. The finite-difference `ε_H` floor at the 0.01 gold cadence on the Stage-0 training panel is measured, as the evidence for C-7 option B.
  3. The owner's C-7 choice is recorded verbatim, and GAP-59-08 is closed with it.
  4. The owner's C-2, C-4, C-5 and C-6 choices are recorded verbatim, with any row left open recorded as open. Every amendment they call for is routed to v2.6.
  5. No test-split file was opened and no held-out evaluation was spent.

**Plans**: 0/2 plans executed in 2 waves (planned 2026-11-08).
**Wave 1**

- [x] 68-01-PLAN.md

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 68-02-PLAN.md

**Cross-cutting constraints:**

- SCOPE-45 and SCOPE-46 govern all execution. The preserved evaluation remains unspent and the frozen scorer and production metric contracts remain intact.

### Phase 69: Findings & Redesign Decision

**Goal**: The owner gets a plain-language, evidence-backed answer to "what stopped v2.4?" and chooses how v2.6 redesigns.
**Depends on**: Phases 67 and 68, or an earlier exit the owner approves under SCOPE-49.
**Requirements**: VERD-01, VERD-02, VER-23
**Success Criteria** (what must be TRUE):

  1. The findings page leads in plain language. It marks each suspect, and the probe's lead, as confirmed, refuted or open, with the numbers beside each committed prediction. The pipeline suspect is reported in two halves, the physics half carried into v2.6 by name unless an experiment speaks to it.
  2. Every claim cites a committed run record or table. The page lists the machine hours spent on this Mac and every plan change made under SCOPE-49.
  3. The owner's decision is recorded verbatim: the v2.6 redesign direction, and whether to commission `trainex-r5`, and on which question.
  4. Every v2.5 requirement maps to exactly one phase. This is re-verified against the final requirement count, including anything added under SCOPE-49.

**Plans**: TBD

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 65. Probe on the Record & Fit Harness | 6/6 | Complete | 2026-10-31 |
| 66. Small-Network Control | 5/5 | Complete    | 2026-11-01 |
| 67. Design & Settings Ladders | 16/16 | Complete    | 2026-11-08 |
| 68. Yardstick | 2/2 | Complete    | 2026-11-08 |
| 69. Findings & Redesign Decision | 0/TBD | Not started | - |

---
*v2.5 created 2026-10-27 (`/gsd-new-milestone`). The roadmap was generated inline from the owner-approved milestone text and requirements.*

- No GSD domain-research spawn; the owner skipped it (2026-10-27).
- 5 phases (65–69), continuing from v2.4's Phase 64.
- 13/13 requirements mapped: DIAG-09, INST-08→65; EXP-01→66; EXP-02..05→67; YARD-01..03→68; VERD-01, VERD-02, VER-23→69.
- v2.4 is archived under [`milestones/v2.4-*`](milestones/).
