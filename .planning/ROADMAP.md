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
- 🚧 **v2.4 Stage-0 Feasibility Checkpoint** — Phases 59–64 (started 2026-10-09; **in progress**). It answers the owner's question of whether the CTL-PINN approach can learn three-body motion at all, with a ladder of experiments scored in physical units against a scorecard frozen before any rung runs:
  - one Stage-0 system with data only (the representation ceiling);
  - the same systems from physics plus IC, and from the full ratified loss;
  - a 16-system family on the corrected trainer;
  - the `trainex-r4` corrected control (seeds 42, 41 and 43; observe-only; Adam-only).

  It ends in a go / pivot-training / rethink-representation verdict on which the owner decides. Amended 2026-10-11 after a re-examination, with owner approval. The amendment adds:
  - comparison points, against which every score is read;
  - a read-only survey of the whole dataset;
  - two probes on harder stages;
  - a readiness ladder and cost model in the verdict;
  - a project charter.

  24 requirements (FEAS-01..10, DIAG-07/08, INST-05..07, CONF-10/11, SPEC-07..10, GATE-05, RUN-06, VER-22); scope boundaries SCOPE-39..44; no graded run and no held-out evaluation. Branch `milestone/v2.4`.
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

## 🚧 v2.4 Stage-0 Feasibility Checkpoint (Planning)

**Milestone Goal:** Find out whether the CTL-PINN approach can learn three-body motion at all, with the cheapest experiments that can settle it. The ladder runs in order:

1. one Stage-0 system with the answer shown;
2. the same systems learned from the physics;
3. a 16-system family;
4. the full Stage-0 control.

The milestone ends with an evidence-backed go / pivot-training / rethink-representation verdict, on which the owner decides whether the project continues.

**What this milestone deliberately does not do:**
- spend a graded run or the preserved held-out evaluation;
- tune the recipe;
- open Stage-1+ or PLAT-01..07;
- re-litigate the `trainex-r4` picks it executes.

**Granularity:** standard. 6 phases, 24 requirements: FEAS-01..10, DIAG-07..08, INST-05..07, CONF-10..11, SPEC-07..10, GATE-05, RUN-06, VER-22.
**Coverage:** 20/20 mapped at roadmap creation; 24/24 after the 2026-10-11 amendment. VER-22's binding check is at Phase 64 close, against the final requirement count.
**Branch:** work continues in `.worktrees/trainex` on `milestone/v2.4`, created 2026-10-09 from `milestone/v2.3` at `b8632832` (the commit that records the `trainex-r4` ruling).
- The ratified proposal is the branch's first commit (`0b400dfa`).
- Commits are per-plan and atomic, via `scripts/agent-commit` with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS` set.
- No push to protected branches. `master` stays governance-only, and integration is user-controlled.

**Source:** `docs/work/designs/cross_cutting/v2.4-milestone-proposal/2026-10-09-v2.4-roadmap-proposal.md`, ratified under owner delegation 2026-10-09 (`0b400dfa`). The roadmap is generated inline from it, following the v2.0–v2.3 precedent. It is amended by `docs/work/designs/cross_cutting/v2.4-milestone-proposal/2026-10-11-v2.4-feasibility-amendments.md` (owner-approved 2026-10-11), which governs where the two differ.

### Feasibility discipline (applies to all phases)

- **Hard boundaries (SCOPE-39..44):**
  - **Stage-0 only.**
  - **No graded run, no held-out evaluation, no test-split file.** The preserved evaluation stays unspent.
  - **Every training run is diagnostic.** It runs in a configuration the graded-run path refuses, and it never alters the ratified recipe.
  - **Pre-registration before every rung.** No threshold is re-set after a result is seen.
  - **Locked values move only by formal amendment.** v2.4's spec edits are the four clarifying amendments SPEC-07..10.
  - **Compute budgets are fixed from a measured seconds-per-step before launch.** Each arm gets at most one extension. Runs go one at a time, detached, with the generation-7 launcher's safeguards.
- **Measure in physical units.** Every rung is scored by FEAS-01's scorecard on the same metrics:
  - position error, including the inner pair's separation;
  - the valid-horizon fraction;
  - the gate's own `ε_H`.

  Loss values are context, not scores. Each result is read against the locked `10⁻⁵` bar.
- **Read every score against comparison points** (FEAS-07): the two-Kepler formula, which uses no learning; on validation, a copy of the nearest training system; and published results. A system counts toward the decision rule only if it is at Tier ≥ 1 **and** beats the formula.
- **Never fail an experiment for the wrong reason.**
  - Every single-system arm gets the spec's L-BFGS polish after Adam, and its result is the better of the two states.
  - Before any RETHINK-REPRESENTATION, the G2 settings sweep checks whether a locked setting, rather than the representation, is at fault.
- **Watch accuracy during training,** not only at the end: Rung 3's and the control's checkpoints are scored at a fixed cadence.
- **Gates and pivots.** Every phase ends at a gate with a pre-registered consequence.
  - A gate may skip, re-order or insert later phases when its condition fires. Later phases are provisional until their gate.
  - **Every exit path ends at Phase 64:** the normal path, the early exit at G2 (RETHINK-REPRESENTATION), and the early exit at G3 (an unfixable gate failure).
  - A result outside a pre-registered branch goes to the owner.
- **Delegation and gaps.**
  - The owner delegated judgment on 2026-10-07 and re-confirmed it on 2026-10-09. Decisions inside the pre-registered branches proceed, and are reported with their rationale at each gate.
  - A source-silent semantic decision is still recorded in the phase-local `NN-GAPS.md` and the milestone index `.planning/milestones/v2.4-GAPS.md` (created on the first gap), with every STOP-protocol field.
  - Such a decision may be resolved under the delegation (`RESOLVED-WITH-INSTRUCTION`, citing the delegation and the rationale), **except** where it would:
    - move a locked value;
    - spend the evaluation;
    - pre-empt the verdict.

    Those go to the owner.
- **Owner checkpoints:**
  1. the verdict and the project charter (FEAS-06, FEAS-10, Phase 64);
  2. a veto on each spec amendment (SPEC-07..10, Phase 61);
  3. any result outside a pre-registered branch;
  4. a G2 sweep rescue, which would move a locked setting (FEAS-03, Phase 60).
- **Verification lesson.** Code is checked against the spec mechanically. A passing plan verification is not evidence of spec conformance: v2.0's pilot and generation 7 both passed their verifications while diverging.

## Phases

**Phase Numbering:** integer phases 59–64 continue from v2.3's Phase 58 (numbering does not reset). Decimal phases are reserved for urgent insertions. The v2.3 phase folders 53–58 stay in `.planning/phases/` beside them.

- [x] **Phase 59: Read-Only Baseline & Scorecard** (completed 2026-10-17, Gate G1 proceed) — Before anything trains:
  - freeze the feasibility scorecard and its scorer, with known-error tests;
  - count how hard the Stage-0 target is, with a census of inner and outer revolutions per window from Brutus data, and choose the panels from it;
  - score the comparison points: the two-Kepler formula and the nearest-neighbour copy;
  - survey every stage read-only, with the predictability envelope;
  - run the ruling's read-only experiments on generation 7's retained checkpoints.

  No training. Gate G1 governs Phase 61. (FEAS-01, FEAS-02, FEAS-07, FEAS-08, DIAG-07)
- [x] **Phase 60: Single-System Learnability** (completed 2026-10-23, stopped at G2: no rescue) — The project's first real answer to "can it learn?":
  - a diagnostic harness on the trainer's own loss functions, with Adam then an L-BFGS polish;
  - Rung 1, data only (the representation ceiling);
  - Rung 2, physics + IC only, and the full ratified loss;
  - all on three census-spanning systems;
  - then, if the ladder continues past G2, two probes on a Stage-4b and a Stage-6 system.

  It needs no conformance work: with one system, every slot is the same trajectory. Gate G2 can end the training phases with RETHINK-REPRESENTATION, but only after a settings sweep finds no rescue. (INST-05, FEAS-03, FEAS-04, FEAS-09)
- [ ] **Phase 61: Conformance & Instrumentation** — **Skipped at G2 (no rescue), not failed.** The ruling's step 2:
  - per-slot physics, monitor and validation, proven by an identity-dependent assertion;
  - the IC term as a mean over the selected slots;
  - the full telemetry;
  - observe-only guard and plateau detector, and an explicit Adam-only switch, all refused by graded runs;
  - four clarifying amendments, including the inherited GAP-56-02.

  Owner veto on each amendment. (CONF-10, CONF-11, INST-06, INST-07, SPEC-07, SPEC-08, SPEC-09, SPEC-10)
- [ ] **Phase 62: Gates & the Small-Family Rung** — **Skipped at G2 (no rescue), not failed.** `R_ref` re-measured, GATE-04 re-run, the `OQ-1` check on the 256 training identities, and `JX-1`'s conformant half. Then Rung 3: the corrected trainer on a 16-system family, scored on it and on the validation panel. Gate G3. (GATE-05, FEAS-05)
- [ ] **Phase 63: Corrected Control** — **Skipped at G2 (no rescue), not failed.** The ruling's composed control at full Stage-0 scale:
  - seeds 42, then 41 and 43;
  - 1,000 Adam steps each;
  - observe-only;
  - full telemetry;
  - not graded.

  The pre-registered readout takes exactly one branch, (a)–(d). (RUN-06, DIAG-08)
- [x] **Phase 64: Feasibility Verdict** (completed 2026-10-26, verdict RETHINK-REPRESENTATION; owner decision: change-course) — A plain-language verdict, by the pre-registered rule: GO, PIVOT-TRAINING or RETHINK-REPRESENTATION. It states:
  - the level reached on the readiness ladder;
  - every result beside the comparison points;
  - the distance to the locked bar;
  - the cost so far, and to the next level and the finish;
  - the next milestone.

  With it comes a one-page project charter: purpose, definition of done, pass bars per stage, budget and stop rule. The owner decides whether the project continues. Traceability is re-verified at close. **Owner checkpoint ①.** (FEAS-06, FEAS-10, VER-22)

## Phase Details

### Phase 59: Read-Only Baseline & Scorecard

**Goal**: Before anything trains, the project knows five things:
- exactly what it will measure;
- what a no-learning formula and a copy of the nearest training system already score;
- how hard the Stage-0 target is;
- how hard every later stage is;
- whether generation 7's checkpoints contradict the plan.

**Depends on**: Nothing. This is the first v2.4 phase.
**Requirements**: FEAS-01, FEAS-02, FEAS-07, FEAS-08, DIAG-07
**Gate G1** (gates Phase 61, not Phase 60): if `JX-1` shows physics took a share of `10⁻²` or more of generation 7's Adam-preconditioned update, the reading that "physics was a passenger" weakens. The conformance-first premise of Phases 61–63 is then re-examined before Phase 61 opens. Otherwise, proceed.
**Success Criteria** (what must be TRUE):
  1. The scorecard and its scorer are committed, before any rung runs:
     - metrics and tiers 0–3;
     - the budget rule and the amended decision rule, including the counting rule;
     - the L-BFGS polish budget, the G2 settings-sweep grid and the accuracy-reading cadence.

     The known-error tests pass: the reference against itself, a known displacement, known velocity scaling, and an inner-pair-only error.
  2. The difficulty census over the 1,812 Stage-0 training systems is committed and re-derivable, with the phase-accuracy figure. The three panels are committed with their selection rule before any rung runs: 3 single systems, the 16-system family, and the validation panel.
  3. The two-Kepler formula is scored on every panel system, and the nearest-neighbour copy on the validation panel, before any rung runs.
  4. The whole-dataset survey, with its predictability envelope and stage difficulty ordering, is committed and re-derivable. The two hard-stage probe systems are selected by their pre-declared rule.
  5. Each of `JX-1` (executed half), `JX-2`, `JX-3`, `JX-4`, `JX-5` (split) and `JX-10` has a recorded result with its command, its checkpoint provenance (the ruling's checkpoint 900 is `best.pt`, `global_step` 900; GAP-59-01), and the reading it supports or falsifies. Gate G1's outcome is recorded.
  6. No training step ran, and no test-split file was opened. The tooling asserts this.
**Plans**: 10/10 plans executed in 5 waves — **closed 2026-10-17**. All six success criteria are met (`59-VERIFICATION.md`); Gate G1's outcome is proceed. GAP-59-08 stays open for the owner.

Plans:

**Wave 1**

- [x] 59-01-PLAN.md — Wave 1: freeze the feasibility scorecard (machine file, strict loader, rule functions, plain-language document, SHA-256 freeze record) before any real-data result (FEAS-01, SCOPE-42)

**Wave 2** *(Wave 1 complete)*

- [x] 59-02-PLAN.md — Wave 2: the scorer and its known-error tests; autograd velocities for networks, finite differences only as a labelled context column (FEAS-01)
- [x] 59-03-PLAN.md — Wave 2: the corpus choke point (hash-checked train/validation allowlist, refusal before any path, audit-hook attestation, production reference trajectories, normalizer recovery) and the static guards (FEAS-02, FEAS-07, FEAS-08, DIAG-07)
- [x] 59-04-PLAN.md — Wave 2: the evidence writer and the independent verifier, including the SCOPE-42 commit-order check (all five requirements)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 59-05-PLAN.md — Wave 3: reader acceptance, the Stage-0 difficulty census and the panels (FEAS-02)
- [x] 59-07-PLAN.md — Wave 3: the DIAG-07 harness on the generation-7 snapshot, JX-10, JX-1 (executed half) and Gate G1 (DIAG-07)

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 59-06-PLAN.md — Wave 4: the read-only whole-dataset survey with tau_L and the FEAS-09 picks (FEAS-08)
- [x] 59-08-PLAN.md — Wave 4: the two-Kepler formula and the nearest-neighbour copy (FEAS-07)
- [x] 59-09-PLAN.md — Wave 4: JX-5, JX-2, JX-4 and JX-3 (DIAG-07)

**Wave 5** *(blocked on Wave 4 completion)*

- [x] 59-10-PLAN.md — Wave 5: the plain-language findings (formula Tier-1 answer, census, panels, survey, Gate G1, GAP-59-08 reported and not fixed) and the final evidence check (all five requirements)

### Phase 60: Single-System Learnability

**Goal**: For the first time, the project learns whether the network can learn one Stage-0 system to physical accuracy: first when shown the answer, then from the physics.
**Depends on**: Phase 59 (the frozen scorecard and the panels). It does not depend on Phase 61, because with one system every slot is the same trajectory and the single-anchor defect cannot arise.
**Requirements**: INST-05, FEAS-03, FEAS-04, FEAS-09
**Gate G2**: Rung 1 runs at the locked settings, with the polish. If it is below Tier 1 on 2 or more of the 3 systems, the G2 settings sweep runs, data-only:
- **No configuration rescues it:** the network cannot represent a Stage-0 trajectory even when shown the answer. The verdict is RETHINK-REPRESENTATION, Phases 61–63 are skipped, and Phase 64 follows.
- **A non-locked configuration rescues it:** owner checkpoint ④. The phase holds until the owner answers. Continue runs the remaining Phase 60 arms at the approved setting, including one data-only Rung 1 on the panel system the sweep did not cover. Go to the verdict records Rung 2 and the probes as skipped.

Otherwise G2 did not fire: continue, run Rung 2, and run the hard-stage probes. The Rung-2 pattern is carried to the verdict. If the ladder stopped at G2, Rung 2 is recorded as skipped.
**Outcome:** the G2 settings sweep found no rescue (all four settings, 60, 120, 240 and 480, ended at Tier 0 on system 1632), so Rung 2 and the hard-stage probes are recorded as skipped with the reason "no rescue", and the handoff to Phase 64 is `.planning/phases/60-single-system-learnability/evidence/g2/stop-handoff.json`.
**Success Criteria** (what must be TRUE):
  1. The learnability harness is committed and tested:
     - its loss functions are the trainer's own (mutation-proven);
     - it runs Adam, then the L-BFGS polish, scoring both states;
     - it records settings overrides for the sweep's data-only arms only;
     - it refuses test-split paths;
     - the graded-run and evaluator paths refuse its run records.
  2. Rung 1 has a scored result on each of the three panel systems, within the pre-registered budget rule: tier, valid-horizon fraction, `ε_H`, trace, and the comparison with the formula.
  3. Rung 2 has scored results on the same systems for arm (a), physics + IC only, and arm (b), the full ratified loss. The comparison against Rung 1 and the formula is recorded, along with whether each system counts. If the ladder stopped at G2, Rung 2 is recorded as skipped.
  4. Gate G2 is evaluated against the pre-registered rule, including the settings sweep if it fires, and its outcome is recorded with the evidence.
  5. If the ladder continues past G2, the two hard-stage probes have scored Rung-1 and Rung-2b results at the setting the ladder is using. If the ladder stopped at G2, the probes are recorded as skipped.
**Plans**: 23 plans in 22 waves. Plans 60-15 to 60-21 are conditional branch plans: each opens with a read-only branch query and, off its path, records "branch not taken" and ends cleanly. Plans 60-13 to 60-17 and 60-20 to 60-21 are non-autonomous (the owner's two questions before the protocol is sealed, owner memory confirmations, checkpoint ④, and detached multi-hour arms whose end is confirmed by the owner in a later session). Only Wave 2 runs two plans at once. From Wave 3 on, plans run one at a time, because each one's checks scan files the others edit in the shared working tree, and because Wave 3's detached Phase 59 final run must not overlap another plan's test suites.

Plans:

**Wave 1**

- [x] 60-01-PLAN.md — Wave 1: tracer, one data-only fixture arm end to end, and the Phase 60 static guard (INST-05)

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 60-02-PLAN.md — Wave 2: the scorer's MPS fix at all three widening sites, the single successor digest (D-09), and the MPS L-BFGS smoke (INST-05, FEAS-03)
- [x] 60-03-PLAN.md — Wave 2: the 2026-10-17 scope amendment text and its SPEC-parsed containment test; the scorecard unchanged (FEAS-04, FEAS-09)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 60-04-PLAN.md — Wave 3: the Phase 59 verifier accepts the one scorer successor; digest-substituted baselines re-derivation; manifest; detached final (INST-05)

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 60-23-PLAN.md — Wave 4: the override record end to end, the closed arm catalog and override refusal, test-split refusal and the record preflight (INST-05)

**Wave 5** *(blocked on Wave 4 completion)*

- [x] 60-05-PLAN.md — Wave 5: the physics step composed from the trainer's functions, with oracle, mutation and identity proofs and the frozen-monitor log (INST-05, FEAS-04)

**Wave 6** *(blocked on Wave 5 completion)*

- [x] 60-06-PLAN.md — Wave 6: G2, the sweep pair, the confirmation, rescue and failed confirmation, the skip writer, the stop handoff, the D-11 rulings and the branch state (FEAS-03, FEAS-04, FEAS-09)

**Wave 7** *(blocked on Wave 6 completion)*

- [x] 60-07-PLAN.md — Wave 7: the detached one-at-a-time sequence launcher with the governed resume gate (INST-05, FEAS-03)

**Wave 8** *(blocked on Wave 7 completion)*

- [x] 60-08-PLAN.md — Wave 8: the frozen budget rule, the timing run, the ratified schedule, the second cosine, the clipper and divergence (INST-05, FEAS-03)

**Wave 9** *(blocked on Wave 8 completion)*

- [x] 60-09-PLAN.md — Wave 9: the GATE-04 omega seam and the D-07 re-measure entry (FEAS-04, FEAS-09)

**Wave 10** *(blocked on Wave 9 completion)*

- [x] 60-10-PLAN.md — Wave 10: the run-protocol builder and drift check, the preflight writer and real-arm admission (INST-05, FEAS-03, FEAS-04, FEAS-09)

**Wave 11** *(blocked on Wave 10 completion)*

- [x] 60-11-PLAN.md — Wave 11: physics arms in the runner, the CPU float64 cross-check, counting, and validated records with every result field (INST-05, FEAS-03, FEAS-04, FEAS-09)

**Wave 12** *(blocked on Wave 11 completion)*

- [x] 60-12-PLAN.md — Wave 12: the arm command line, the one-launch lock, graceful stop and exact resume (INST-05, FEAS-03)

**Wave 13** *(blocked on Wave 12 completion)*

- [x] 60-13-PLAN.md — Wave 13: the Phase 60 evidence verifier; the preflight; the owner's pre-seal answers on clipping (GAP-60-03) and a failed confirmation (GAP-60-09); the run protocol committed before any arm (INST-05, FEAS-03, FEAS-04, FEAS-09)

**Wave 14** *(blocked on Wave 13 completion)*

- [x] 60-14-PLAN.md — Wave 14: Rung 1 on 1632, 851 and 4658, and Gate G2 (FEAS-03)

**Wave 15** *(blocked on Wave 14 completion)*

- [x] 60-15-PLAN.md — Wave 15: branch G2 fired, the four-setting sweep (FEAS-03)

**Wave 16** *(blocked on Wave 15 completion)*

- [x] 60-16-PLAN.md — Wave 16: branch Tier-1 setting found, the single confirmation run (FEAS-03) — branch not taken (no rescue)

**Wave 17** *(blocked on Wave 16 completion)*

- [x] 60-17-PLAN.md — Wave 17: branch rescue or failed confirmation, owner checkpoint ④ and the ruling file (FEAS-03) — branch not taken (no rescue)

**Wave 18** *(blocked on Wave 17 completion)*

- [x] 60-18-PLAN.md — Wave 18: branch stop, skip records and the Phase 64 handoff (FEAS-04, FEAS-09) — branch taken (no rescue)

**Wave 19** *(blocked on Wave 18 completion)*

- [x] 60-19-PLAN.md — Wave 19: branch continue, the R_ref re-measure and GATE-04 at the approved setting (FEAS-04, FEAS-09) — branch not taken (no rescue)

**Wave 20** *(blocked on Wave 19 completion)*

- [x] 60-20-PLAN.md — Wave 20: branch ladder, Rung 2 (and the uncovered system's Rung 1 on a continue) (FEAS-04, FEAS-03) — branch not taken (no rescue)

**Wave 21** *(blocked on Wave 20 completion)*

- [x] 60-21-PLAN.md — Wave 21: branch ladder, the two hard-stage probes (FEAS-09) — branch not taken (no rescue)

**Wave 22** *(blocked on Wave 21 completion)*

- [x] 60-22-PLAN.md — Wave 22: closeout, final evidence checks, re-derivation by re-scoring, findings and progress records (INST-05, FEAS-03, FEAS-04, FEAS-09)

### Phase 61: Conformance & Instrumentation

**Goal**: The trainer executes the ratified recipe for every slot in the batch and records everything the readout needs. It can also run in observe-only diagnostic modes, which graded runs refuse.
**Depends on**: Phase 60's gate G2, which skips this phase on RETHINK-REPRESENTATION, and Phase 59's gate G1. Planning may start while Phase 60's runs execute.
**Requirements**: CONF-10, CONF-11, INST-06, INST-07, SPEC-07, SPEC-08, SPEC-09, SPEC-10
**Success Criteria** (what must be TRUE):
  1. Perturbing a non-anchor slot's IC13 changes both the physics loss and the IC loss. The assertion fails on the generation-7 code path and passes on the corrected one, and the production-conformance verifier records the IC and mass inputs it evaluated.
  2. The IC term equals the mean over the selected slots, with multiplicity preserved. The corrected code consumes the batch random stream unchanged, so the seed-42 pairing with generation 7 holds.
  3. A short synthetic run writes every `JD-10` telemetry field. The observe-only guard, the observe-only plateau detector and the explicit Adam-only switch each work and are recorded in the run configuration. The graded-run path and the evaluator refuse any run that used them.
  4. SPEC-07..10 are written as clarifying amendments with no value changed, and each has been shown to the owner for veto.
  5. A mechanical code-against-spec check of every changed contract passes.
**Plans**: TBD

### Phase 62: Gates & the Small-Family Rung

**Goal**: With conformant code, the causal weights are shown to respond on real training systems, and the recipe is tested on a 16-system family before the full control spends about ten hours.
**Depends on**: Phase 61.
**Requirements**: GATE-05, FEAS-05
**Gate G3**: a gate failure stops the line until it is fixed, or until the probe is amended per `OQ-1`. A failure that cannot be fixed within the milestone sends the milestone to Phase 64 on the ladder's evidence. Rung 3's result goes to the verdict. The control still runs: its readout branch names the next arm.
**Success Criteria** (what must be TRUE):
  1. `R_ref` is re-measured by the ratified six-case procedure on the corrected code, and GATE-04 re-runs to a complete PASS, with provenance-bound artifacts.
  2. The `OQ-1` check passes: at initialization, the frozen monitor's 256 training identities give neither floor-bound nor degenerate weights. If the check fails, the probe is amended to training-split ICs before any run.
  3. `JX-1`'s conformant half at initialization is recorded as structural evidence.
  4. Rung 3 has scored results on its 16 training systems and on the validation panel, both at the end and as an accuracy curve over its checkpoints. The count of systems that count (Tier ≥ 1 and beating the formula) is compared with the decision rule, and the validation scores are read beside the formula and the nearest-neighbour copy.
**Plans**: TBD

### Phase 63: Corrected Control

**Goal**: The corrected recipe runs at full Stage-0 scale on three seeds, and its pre-registered readout selects exactly one branch.
**Depends on**: Phase 62, with GATE-05 passed.
**Requirements**: RUN-06, DIAG-08
**Success Criteria** (what must be TRUE):
  1. Seeds 42, 41 and 43 each complete 1,000 Adam steps under the composed control:
     - observe-only guard and plateau detector;
     - Adam-only by an explicit switch;
     - full telemetry;
     - no graded slot and no evaluation.

     Alternatively, seed 42 exposes an implementation defect, which is recorded and fixed first.
  2. For every seed, the record shows the step at which the ratified invariant-B rule would have halted the run, and the steps at which the plateau detector would have fired.
  3. For every seed, the weights kept at the pre-registered cadence are scored offline on the validation panel, giving an accuracy curve. Keeping them changes nothing in the run.
  4. The readout takes exactly one branch, (a)–(d), with its evidence. It is read together with the scorecard's absolute measures and the accuracy curves on the validation panel.
**Plans**: TBD

### Phase 64: Feasibility Verdict

**Goal**: The owner gets a plain-language, evidence-backed answer to "can this work?", with where the project stands, what the next level costs, and a charter for the rest. The owner then decides whether the project continues, changes course or stops.
**Depends on**: Phase 63, or an early exit at gate G2 or G3.
**Requirements**: FEAS-06, FEAS-10, VER-22
**Success Criteria** (what must be TRUE):
  1. The verdict document leads in plain language. It states:
     - the tier each rung reached, and where along the window each broke;
     - the control's readout branch, if the control ran;
     - the best `ε_H` against the locked bar;
     - the result under the pre-registered rule.
  2. It places the project on the readiness ladder (levels 0–9) with the evidence for each level. It reads every result beside the comparison points, the accuracy curves, the survey and the hard-stage probes.
  3. It states the machine hours spent, and the estimated cost to the next level and to the finish, on this Mac, with every assumption stated. All computation runs on this Mac; no rented or cloud GPU route is costed or proposed (standing owner rule, `PROJECT.md` Constraints; reaffirmed 2026-10-25).
  4. It names the next milestone the result routes to.
  5. The one-page charter is drafted:
     - purpose and definition of done;
     - pass bars per stage, each with a position and an energy criterion, fixed before any held-out exam;
     - budget and stop rule.

     The owner's decision and choices are recorded verbatim, including whether the `10⁻⁵` bar stays. Items left open are recorded as open.
  6. Every v2.4 requirement maps to exactly one phase. This is re-verified against the final requirement count.
**Plans**: 7 plans in 7 waves, one at a time, because every plan extends the same verifier and test file. Only 64-06 is non-autonomous: it holds owner checkpoint ①, the phase's single owner question, after every automated check is green. 64-07 applies only what the owner approved there.

Plans:

**Wave 1**

- [x] 64-01-PLAN.md — Wave 1: tracer, the verifier's inputs check (the sealed handoff and the label re-derived by the frozen rule), the frozen-path check, and the traceability check for VER-22 (FEAS-06, VER-22)

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 64-02-PLAN.md — Wave 2: the number manifest, re-derived from the committed records and, on the CPU in float64, from the committed weights, including the time-constant evidence (FEAS-06, FEAS-10)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 64-03-PLAN.md — Wave 3: the one figure, system 1632's real orbit beside the network's prediction, with its provenance (FEAS-06)

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 64-04-PLAN.md — Wave 4: the feasibility verdict, plain language first, with its rules check (FEAS-06)

**Wave 5** *(blocked on Wave 4 completion)*

- [x] 64-05-PLAN.md — Wave 5: the pre-filled one-page charter with appendices, and the ruling check (FEAS-10, FEAS-06)

**Wave 6** *(blocked on Wave 5 completion)*

- [x] 64-06-PLAN.md — Wave 6: owner checkpoint ①, the decision and the charter in one reply, recorded verbatim (FEAS-06, FEAS-10)

**Wave 7** *(blocked on Wave 6 completion)*

- [x] 64-07-PLAN.md — Wave 7: apply what the owner approved, tick the requirements, VER-22's binding check and the final check (FEAS-06, FEAS-10, VER-22)

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 59. Read-Only Baseline & Scorecard | 10/10 | Complete | 2026-10-17 |
| 60. Single-System Learnability | 23/23 | Complete (stopped at G2: no rescue) | 2026-10-23 |
| 61. Conformance & Instrumentation | 0/TBD | Skipped at G2 (no rescue), not failed | - |
| 62. Gates & the Small-Family Rung | 0/TBD | Skipped at G2 (no rescue), not failed | - |
| 63. Corrected Control | 0/TBD | Skipped at G2 (no rescue), not failed | - |
| 64. Feasibility Verdict | 7/7 | Complete | 2026-10-26 |

---
*v2.4 created 2026-10-09 (`/gsd-new-milestone`). The roadmap was generated inline from the v2.4 proposal, ratified under owner delegation at `0b400dfa`.*
- No GSD domain-research spawn, following the v2.0–v2.3 precedent; this milestone's research is the `trainex-r4` round.
- 6 phases (59–64), continuing from v2.3's Phase 58.
- 20/20 requirements mapped at creation: FEAS-01, FEAS-02, DIAG-07→59; INST-05, FEAS-03, FEAS-04→60; CONF-10, CONF-11, INST-06, INST-07, SPEC-07..10→61; GATE-05, FEAS-05→62; RUN-06, DIAG-08→63; FEAS-06, VER-22→64.
- Amended 2026-10-11 with owner approval (`docs/work/designs/cross_cutting/v2.4-milestone-proposal/2026-10-11-v2.4-feasibility-amendments.md`): FEAS-07, FEAS-08→59; FEAS-09→60; FEAS-10→64. 24/24 mapped.
- v2.3 is archived under [`milestones/v2.3-*`](milestones/). Its inherited obligations are discharged as the proposal records.
