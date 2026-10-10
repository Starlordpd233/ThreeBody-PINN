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

  It ends in a go / pivot-training / rethink-representation verdict on which the owner decides. 20 requirements (FEAS-01..06, DIAG-07/08, INST-05..07, CONF-10/11, SPEC-07..10, GATE-05, RUN-06, VER-22); scope boundaries SCOPE-39..44; no graded run and no held-out evaluation. Branch `milestone/v2.4`.
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

**Granularity:** standard. 6 phases, 20 requirements: FEAS-01..06, DIAG-07..08, INST-05..07, CONF-10..11, SPEC-07..10, GATE-05, RUN-06, VER-22.
**Coverage:** 20/20 v2.4 requirements mapped at roadmap creation. VER-22's binding check is at Phase 64 close, against the final requirement count.
**Branch:** work continues in `.worktrees/trainex` on `milestone/v2.4`, created 2026-10-09 from `milestone/v2.3` at `b8632832` (the commit that records the `trainex-r4` ruling).
- The ratified proposal is the branch's first commit (`0b400dfa`).
- Commits are per-plan and atomic, via `scripts/agent-commit` with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS` set.
- No push to protected branches. `master` stays governance-only, and integration is user-controlled.

**Source:** `docs/work/designs/cross_cutting/v2.4-milestone-proposal/2026-10-09-v2.4-roadmap-proposal.md`, ratified under owner delegation 2026-10-09 (`0b400dfa`). The roadmap is generated inline from it, following the v2.0–v2.3 precedent.

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
  1. the verdict (FEAS-06, Phase 64);
  2. a veto on each spec amendment (SPEC-07..10, Phase 61);
  3. any result outside a pre-registered branch.
- **Verification lesson.** Code is checked against the spec mechanically. A passing plan verification is not evidence of spec conformance: v2.0's pilot and generation 7 both passed their verifications while diverging.

## Phases

**Phase Numbering:** integer phases 59–64 continue from v2.3's Phase 58 (numbering does not reset). Decimal phases are reserved for urgent insertions. The v2.3 phase folders 53–58 stay in `.planning/phases/` beside them.

- [ ] **Phase 59: Read-Only Baseline & Scorecard** — Before anything trains:
  - freeze the feasibility scorecard and its scorer;
  - count how hard the Stage-0 target is, with a census of inner and outer revolutions per window from Brutus data, and choose the panels from it;
  - run the ruling's read-only experiments on generation 7's retained checkpoints.

  No training. Gate G1 governs Phase 61. (FEAS-01, FEAS-02, DIAG-07)
- [ ] **Phase 60: Single-System Learnability** — The project's first real answer to "can it learn?":
  - a diagnostic harness on the trainer's own loss functions;
  - Rung 1, data only (the representation ceiling);
  - Rung 2, physics + IC only, and the full ratified loss;
  - all on three census-spanning systems.

  It needs no conformance work: with one system, every slot is the same trajectory. Gate G2 can end the training phases with RETHINK-REPRESENTATION. (INST-05, FEAS-03, FEAS-04)
- [ ] **Phase 61: Conformance & Instrumentation** — The ruling's step 2:
  - per-slot physics, monitor and validation, proven by an identity-dependent assertion;
  - the IC term as a mean over the selected slots;
  - the full telemetry;
  - observe-only guard and plateau detector, and an explicit Adam-only switch, all refused by graded runs;
  - four clarifying amendments, including the inherited GAP-56-02.

  Owner veto on each amendment. (CONF-10, CONF-11, INST-06, INST-07, SPEC-07, SPEC-08, SPEC-09, SPEC-10)
- [ ] **Phase 62: Gates & the Small-Family Rung** — `R_ref` re-measured, GATE-04 re-run, the `OQ-1` check on the 256 training identities, and `JX-1`'s conformant half. Then Rung 3: the corrected trainer on a 16-system family, scored on it and on the validation panel. Gate G3. (GATE-05, FEAS-05)
- [ ] **Phase 63: Corrected Control** — The ruling's composed control at full Stage-0 scale:
  - seeds 42, then 41 and 43;
  - 1,000 Adam steps each;
  - observe-only;
  - full telemetry;
  - not graded.

  The pre-registered readout takes exactly one branch, (a)–(d). (RUN-06, DIAG-08)
- [ ] **Phase 64: Feasibility Verdict** — A plain-language verdict, by the pre-registered rule: GO, PIVOT-TRAINING or RETHINK-REPRESENTATION, with the distance to the locked bar and the next milestone named. The owner decides whether the project continues. Traceability is re-verified at close. **Owner checkpoint ①.** (FEAS-06, VER-22)

## Phase Details

### Phase 59: Read-Only Baseline & Scorecard

**Goal**: Before anything trains, the project knows three things: exactly what it will measure, how hard the target is, and whether generation 7's checkpoints contradict the plan.
**Depends on**: Nothing. This is the first v2.4 phase.
**Requirements**: FEAS-01, FEAS-02, DIAG-07
**Gate G1** (gates Phase 61, not Phase 60): if `JX-1` shows physics took a share of `10⁻²` or more of generation 7's Adam-preconditioned update, the reading that "physics was a passenger" weakens. The conformance-first premise of Phases 61–63 is then re-examined before Phase 61 opens. Otherwise, proceed.
**Success Criteria** (what must be TRUE):
  1. The scorecard and its scorer are committed: metrics, tiers 0–3, the budget rule and the decision rule. Scoring the Brutus reference against itself returns zero position error and the reference's own `ε_H`.
  2. The difficulty census over the 1,812 Stage-0 training systems is committed and re-derivable. The three panels are committed with their selection rule before any rung runs: 3 single systems, the 16-system family, and the validation panel.
  3. Each of `JX-1` (executed half), `JX-2`, `JX-3`, `JX-4`, `JX-5` (split) and `JX-10` has a recorded result with its command, its checkpoint provenance (including the stand-in for the ruling's checkpoint 900), and the reading it supports or falsifies. Gate G1's outcome is recorded.
  4. No training step ran, and no test-split file was opened. The tooling asserts this.
**Plans**: TBD

### Phase 60: Single-System Learnability

**Goal**: For the first time, the project learns whether the network can learn one Stage-0 system to physical accuracy: first when shown the answer, then from the physics.
**Depends on**: Phase 59 (the frozen scorecard and the panels). It does not depend on Phase 61, because with one system every slot is the same trajectory and the single-anchor defect cannot arise.
**Requirements**: INST-05, FEAS-03, FEAS-04
**Gate G2**: if Rung 1 (data only) is below Tier 1 on 2 or more of the 3 systems, the network cannot represent a Stage-0 trajectory even when shown the answer. The verdict is then RETHINK-REPRESENTATION, Phases 61–63 are skipped, and Phase 64 follows. Otherwise, continue. The Rung-2 pattern is carried to the verdict.
**Success Criteria** (what must be TRUE):
  1. The learnability harness is committed and tested. Its loss functions are the trainer's own (mutation-proven), it refuses test-split paths, and the graded-run and evaluator paths refuse its run records.
  2. Rung 1 has a scored result on each of the three panel systems, within the pre-registered budget rule: tier, valid-horizon fraction, `ε_H`, and trace.
  3. Rung 2 has scored results on the same systems for arm (a), physics + IC only, and arm (b), the full ratified loss, with the comparison against Rung 1 recorded.
  4. Gate G2 is evaluated against the pre-registered rule, and its outcome is recorded with the evidence.
**Plans**: TBD

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
  4. Rung 3 has scored results on its 16 training systems and on the validation panel, and the count at Tier 1 or above is compared with the decision rule.
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
  3. The readout takes exactly one branch, (a)–(d), with its evidence. It is read together with the scorecard's absolute measures on the validation panel.
**Plans**: TBD

### Phase 64: Feasibility Verdict

**Goal**: The owner gets a plain-language, evidence-backed answer to "can this work?" and decides whether the project continues, changes course or stops.
**Depends on**: Phase 63, or an early exit at gate G2 or G3.
**Requirements**: FEAS-06, VER-22
**Success Criteria** (what must be TRUE):
  1. The verdict document leads in plain language. It states:
     - the tier each rung reached, and where along the window each broke;
     - the control's readout branch, if the control ran;
     - the best `ε_H` against the locked bar;
     - the result under the pre-registered rule.
  2. It names the next milestone the result routes to.
  3. The owner's decision is recorded verbatim: continue, change course or stop, and whether the `10⁻⁵` bar stays the success criterion.
  4. Every v2.4 requirement maps to exactly one phase. This is re-verified against the final requirement count.
**Plans**: TBD

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 59. Read-Only Baseline & Scorecard | 0/TBD | Not started | - |
| 60. Single-System Learnability | 0/TBD | Not started | - |
| 61. Conformance & Instrumentation | 0/TBD | Not started | - |
| 62. Gates & the Small-Family Rung | 0/TBD | Not started | - |
| 63. Corrected Control | 0/TBD | Not started | - |
| 64. Feasibility Verdict | 0/TBD | Not started | - |

---
*v2.4 created 2026-10-09 (`/gsd-new-milestone`). The roadmap was generated inline from the v2.4 proposal, ratified under owner delegation at `0b400dfa`.*
- No GSD domain-research spawn, following the v2.0–v2.3 precedent; this milestone's research is the `trainex-r4` round.
- 6 phases (59–64), continuing from v2.3's Phase 58.
- 20/20 requirements mapped: FEAS-01, FEAS-02, DIAG-07→59; INST-05, FEAS-03, FEAS-04→60; CONF-10, CONF-11, INST-06, INST-07, SPEC-07..10→61; GATE-05, FEAS-05→62; RUN-06, DIAG-08→63; FEAS-06, VER-22→64.
- v2.3 is archived under [`milestones/v2.3-*`](milestones/). Its inherited obligations are discharged as the proposal records.
