# Requirements: v2.5 Root-Cause Confirmation

**Defined:** 2026-10-27
**Core value:** An evidence-backed, pre-registered answer at each milestone to whether the approach learns three-body motion, in physical units, against this charter's bars.
**Total:** 13 requirements (1 DIAG + 1 INST + 5 EXP + 3 YARD + 2 VERD + 1 VER) + scope boundaries SCOPE-45..49.

**Source:** the owner's direction in the 2026-10-27 `/gsd-new-milestone` session,
recorded in `.planning/PROJECT.md` "Current Milestone: v2.5" (`633f8eb4`). The
owner approved the milestone summary ("Looks good"), skipped the milestone-level
research step, and confirmed the scope ("No, that's the scope"). It builds on
the v2.4 close: `64-VERDICT.md`, `64-CHARTER.md` and
`64-CHECKPOINT-1-RULING.md` under `.planning/phases/64-feasibility-verdict/`.

## Why this milestone exists

Every network v2.4 trained learned only each body's average position. The
frozen rule returned `RETHINK-REPRESENTATION`, and the owner chose to change
course (2026-10-26). Before redesigning anything, the owner wants to know what
actually stopped it, and named three suspects:

1. **The network is too small** for the problem.
2. **The metrics are too harsh,** perhaps impossible to meet physically or
   mathematically.
3. **The training pipeline is wrong,** and would stay wrong after a redesign.

The v2.4 records cannot separate these. The G2 sweep varied only
`first_omega_0`, and Rung 1 trained on data alone, so the known defects in
the physics term cannot explain it.

An informal read-only probe of the seven committed Phase 60 networks
(2026-10-27) gave a concrete lead. After training, the network's hidden
states at two times 0.01 apart are unrelated from layer 2–3 onward (cosine
|·| ≤ 0.018, against ≥ 0.92 at initialization). The network has about 0.8M
parameters for about 9,000 target numbers per orbit, so size is an unlikely
limit. Separately, Phase 59 found that the production energy check fails even
Brutus's exact answer (GAP-59-08).

v2.5 tests each suspect with cheap experiments on this Mac. Each experiment's
predictions are committed before it runs. v2.6 then redesigns against a
confirmed cause, not a plausible one: v2.2–v2.4 each fixed a plausible cause,
and the next run failed for a different reason.

## Grounding (authoritative inputs)

1. **The approved milestone text:** `PROJECT.md` "Current Milestone: v2.5"
   (`633f8eb4`), including order A and the pivot rule.
2. **The v2.4 close record:** `64-VERDICT.md`, `64-CHARTER.md` (rows C-1..C-14)
   and `64-CHECKPOINT-1-RULING.md`; `milestones/v2.4-REQUIREMENTS.md`.
3. **The frozen v2.4 scorecard and its tooling:**
   - `pinn/verification/artifacts/feasibility_scorecard_v1.json`. Tier 1 is
     `E ≤ 0.1`. Tier 2 is `E ≤ 0.01` with `ε_H ≤ 10⁻³`. Tier 3 is `E ≤ 0.01`
     with `ε_H ≤ 10⁻⁵`.
   - `pinn/verification/feasibility_scorer.py`;
   - the comparison points: `two_kepler.py`, `nn_copy.py`, and the constant
     predictor that Phase 64 scored (E 1.1538, 1.2337 and 1.1396 on systems
     1632, 851 and 4658);
   - the INST-05 learnability harness (`pinn/verification/learnability_*.py`)
     and `split_allowlist.py`.
4. **The Phase 60 records:** the seven arms' committed weights under
   `.planning/phases/60-single-system-learnability/evidence/arms/`.
5. **The Phase 59 census and panels:** for example, system 1632 has 10.47
   inner laps per window and 1,001 gold samples
   (`.planning/phases/59-read-only-baseline-scorecard/evidence/census/`).
6. **GAP-59-08** (`.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md`): on the dataset's grid,
   finite-difference `ε_H` scores Brutus's exact answer at 4.7e-2, 2.1e-1 and
   3.8e-1 on systems 1632, 851 and 4658, against about 1e-14 with true
   velocities.

**Not reopened:** the locked framework specs as amended through v2.3, the
frozen v2.4 scorecard, its panels and comparison points, and every v2.4
record. v2.5 measures with them and does not re-freeze them. A defect that
YARD-01 finds is recorded and routed (see the pivot rule, SCOPE-49).

## v2.5 Requirements

### Diagnostics (DIAG)

- [x] **DIAG-09**: **The 2026-10-27 probe, on the record.** The informal probe is committed as a read-only script and re-run on the seven Phase 60 arms' committed weights, at initialization and after training. For each layer it records:
  - how alike the centred hidden state is at times 0.01 apart (cosine similarity);
  - how much the output moves, as a share of the orbit's own variation;
  - the output's rate of change against the true orbit's;
  - how the first layer's time frequencies changed in training.

  **Acceptance:**
  - The 2026-10-27 figures are committed as the predictions, with a reproduction tolerance, before the script runs.
  - Each figure is recorded as reproduced or not.
  - Weights are checked by SHA-256 before loading.
  - No training runs, and no test-split file is opened, which is asserted. [`PROJECT.md` v2.5 "The probe on the record"; memory of the informal probe]

### Instrumentation (INST)

- [x] **INST-08**: **A minute-scale diagnostic fit harness.** Committed, tested tooling under `pinn/verification/` that builds on INST-05. It trains one named network variant, data-only, on one Stage-0 training orbit's gold record. It scores each run with the frozen FEAS-01 scorer, beside the two-Kepler formula and the constant predictor. It logs DIAG-09's per-layer neighbour similarity at a fixed cadence during training.
  - **Variants** are named entries in a registry, written into the run record: depth, width, time-input features, learning rate and window length.
  - **The locked variant** (12 layers, the locked settings) is the v2.4 network.
  - **Run records** are marked diagnostic and keep their budget and measured seconds per step.

  **Acceptance:** tests prove each of these:
  - **(a)** the locked variant's forward pass equals the production network's at the same seed and weights;
  - **(b)** the scorer is the frozen FEAS-01 scorer, not a re-implementation;
  - **(c)** the similarity logger reproduces DIAG-09's value on one committed arm;
  - **(d)** test-split paths are refused, and the graded-run and evaluator paths refuse a harness record;
  - **(e)** a short run on one orbit completes and is scored. [`PROJECT.md` v2.5 "A minute-scale test harness"; INST-05 lineage]

### Cause-Confirmation Experiments (EXP)

Each experiment has a committed prediction page before its first run (SCOPE-47). The page states:

- what each suspect predicts;
- the exact settings;
- the budget, from a measured seconds-per-step;
- the reading rule.

A result counts as confirming only if it repeats on a second panel system and a second seed. All five experiments use INST-08.

- [x] **EXP-01**: **The small-network control (tests "too small").** A network with fewer parameters than the locked one, and fewer layers, fits orbit 1632 from time alone. Its architecture is fixed on the prediction page.

  **Acceptance:**
  - Its tier, `E` against the constant predictor and the formula, and neighbour similarity are recorded.
  - Reaching Tier 1 (`E ≤ 0.1`) refutes "too small" for one orbit.
  - The result is reviewed against the plan before EXP-02..05 start (owner checkpoint ①). [`PROJECT.md` v2.5 experiments]
- [x] **EXP-02**: **The depth ladder.** The locked layer types at 2, 4, 6, 8 and 12 layers, with everything else locked, on orbit 1632.

  **Acceptance:** `E`, tier and per-layer neighbour similarity are recorded at each depth, so it shows whether accuracy falls and similarity collapses as depth grows. [`PROJECT.md` v2.5 experiments]
- [x] **EXP-03**: **The learning-rate ladder.** The locked network at learning rates from 10⁻³ down to 10⁻⁵. The exact points are on the prediction page.

  **Acceptance:** `E`, tier and the similarity trace through training are recorded at each rate. These separate "the design" from "the training settings". [`PROJECT.md` v2.5 experiments]
- [x] **EXP-04**: **Time-input design.** Time features matched to how fast the orbit moves, against the locked input, where time shares the first layer with 13 inputs that are constant on one orbit.

  **Acceptance:** `E`, tier and similarity are recorded for each input design, on the locked depth and on the EXP-01 network. [`PROJECT.md` v2.5 experiments]
- [x] **EXP-05**: **Window length.** Windows of 1, 2, 5 and 10 inner laps. On system 1632, 10 laps is about the whole window (10.47).

  **Acceptance:** `E` over each window, tier and similarity are recorded, so it shows whether a shorter window removes the failure. [`PROJECT.md` v2.5 experiments; `64-VERDICT.md` representation pivots]

### Yardstick (YARD)

- [ ] **YARD-01**: **Known-answer checks of every metric that judges a result.** This covers the FEAS-01 scorer's metrics and tiers, the production validation gate (`pinn/training/validation_gate.py`) and the held-out evaluator's `ε_H` (`pinn/evaluate.py`). Read-only, with no training. On the three panel systems, each metric is scored for:
  - **Brutus's exact answer,** which must pass every bar it should;
  - **the constant predictor,** which must fail every bar that judges accuracy.

  Every metric that a constant prediction passes is reported. From first principles, a perfectly constant prediction has zero velocity, so its energy never changes, and its `ε_H` is 0 when `H(0)` is the prediction's own. This is why FEAS-10 pairs every energy bar with a position bar. The check also measures the finite-difference `ε_H` floor at the 0.01 gold cadence on the Stage-0 training panel, which is the evidence for C-7 option B.

  **Acceptance:**
  - Each metric and gate has its pass or fail table for both answers, committed and re-derivable.
  - No test-split file is opened, and no held-out evaluation is spent. [`PROJECT.md` v2.5 "The yardstick"; GAP-59-08]
- [ ] **YARD-02**: **The owner decides GAP-59-08 (charter row C-7):** how the energy error is measured. The options are `64-CHARTER.md`'s A, B and C, with YARD-01's evidence.

  **Acceptance:**
  - The choice is recorded verbatim, and GAP-59-08 is closed with it.
  - Any amendment it calls for (A writes autograd velocities into `pinn_architecture.md` §10.6) is routed to v2.6 (SCOPE-46). [`64-CHARTER.md` C-7]
- [ ] **YARD-03**: **The owner sets the bars.** These are charter rows C-2 (the definition of done), C-4 and C-5 (the Stage-0 position and energy bars) and C-6 (the 10⁻⁵ held-out bar). They are set from the purpose (C-1), the comparison points, YARD-01 and the published results.

  **Acceptance:**
  - The choices are recorded verbatim. A row the owner leaves open is recorded as open.
  - Any amendment they call for, including the C-6 replacement and the `ctl_instruction.md` evaluation-section rewrite (C-11), is routed to v2.6. [`64-CHARTER.md` C-2, C-4..C-6; FEAS-10]

### Findings and Decision (VERD)

- [ ] **VERD-01**: **The findings page.** One page, plain language first. It marks each suspect, and the probe's lead, as confirmed, refuted or open, with the numbers beside each experiment's committed prediction.
  - **Suspect 3, the pipeline,** is reported in two halves. The training-settings half is tested by EXP-03. The physics-term half cannot be judged until a network fits one orbit, so it is marked open and carried into v2.6 by name, unless an experiment speaks to it.
  - **The page also lists:**
    - the redesign directions the evidence supports;
    - the machine hours spent on this Mac;
    - every plan change made under SCOPE-49.

  **Acceptance:** every claim cites a committed run record or table. [`PROJECT.md` v2.5 "Findings and decision"]
- [ ] **VERD-02**: **The owner's decision at the close.** The owner picks:
  - the v2.6 redesign direction;
  - whether to commission `trainex-r5` for it, and on which question. By order A, r5 is re-aimed at the redesign. If the lead was refuted, it runs on the diagnosis instead.

  **Acceptance:** the decision is recorded verbatim. A choice the owner leaves open is recorded as open. [`PROJECT.md` v2.5 Governance, order A]

### Traceability (VER)

- [ ] **VER-23**: **Traceability.** Every v2.5 requirement maps to exactly one phase, with no orphans and no duplicates. This includes any requirement or phase added by a plan change under SCOPE-49. It is re-verified at the close against the final requirement count, not carried forward from the roadmap-creation check. [VER-22 lineage]

## Scope Boundaries (owner direction 2026-10-27; hard constraints)

| ID | Boundary |
|---|---|
| SCOPE-45 | **Stage 0 only, on training-split records.** No graded run, no held-out evaluation, and no experiment opens a test-split file; each run asserts it. The single preserved evaluation stays unspent. |
| SCOPE-46 | **No framework-spec edits and no locked value moves.** Experiments vary settings only inside the INST-08 harness, and their records are diagnostic, which the graded-run path refuses. Spec amendments, the rebuild and the pipeline fixes belong to v2.6. |
| SCOPE-47 | **Lightweight pre-registration.** Each experiment has one committed prediction page before its first run, not the full sealed v2.4 protocol. A reading rule is never re-set after a result is seen. A result outside the page's branches goes to the owner. |
| SCOPE-48 | **Compute on this Mac only.** Budgets are set from a measured seconds-per-step. Any run over an hour uses the governed pause, resume and power-guard tooling (`scripts/phase60-pause.sh`, `phase60-resume.sh`, `phase60-power-guard.sh`). No rented or cloud GPU route is costed or proposed (`PROJECT.md` Constraints). |
| SCOPE-49 | **The plan may pivot on results.** After each experiment's result is recorded, the agent compares it with the prediction page and with the roadmap. When a result refutes the lead or opens a new question, the agent proposes the change: an inserted phase numbered like 66.1, a dropped phase, re-aimed later phases, or a new requirement continuing these ID sequences. The owner decides. The roadmap is neither forced against the evidence nor changed without the owner. Phases after the first experiment are provisional. |

## Owner Checkpoints

1. **Plan changes (SCOPE-49),** including the review after EXP-01. A
   proposal blocks only the work that depends on it.
2. **The yardstick (YARD-02, YARD-03):** C-7, then C-2 and C-4..C-6.
3. **The close (VERD-02):** the v2.6 direction and `trainex-r5`.

Everything else proceeds under the owner's delegation of technical rulings and
is reported at each phase gate.

## How the first results can reshape the plan

These are the pre-registered branches. A result outside them goes to the owner.

| Result | What happens |
|---|---|
| DIAG-09 does not reproduce the probe | The lead is withdrawn. The agent proposes re-aiming EXP-02..05, and under order A `trainex-r5` would run on the diagnosis. |
| EXP-01 reaches Tier 1 on 1632 | "Too small" is refuted for one orbit. EXP-02..05 run as planned, to find which part of the locked design fails. |
| EXP-01 stays near the constant predictor's `E` | The lead does not explain the failure on its own. The agent proposes an inserted phase that checks the path from the data to the scorer before the ladders run. |

## Future Requirements (v2.6 and beyond)

- **The redesign:** spec amendments, the rebuild, and re-climbing the ladder
  against the same frozen scorecard. That means one orbit with the answer
  shown, then one orbit from physics alone, then the 16-system family, then
  all of Stage 0.
- **Known pipeline defects, carried by name:**
  - physics computed on one trajectory per step (the single-anchor finding;
    formerly CONF-10);
  - the IC term not averaged over the selected slots (formerly CONF-11);
  - an IC gradient 10⁴–10⁶× the physics gradient;
  - the unreachable L-BFGS stage.
- **The amendments that YARD-02 and YARD-03 call for,** including the
  `ctl_instruction.md` evaluation-section rewrite (C-11).
- **`trainex-r5`,** if the owner commissions it at VERD-02.
- **PLAT-01..07 and Stage 1+:** still blocked.

## Out of Scope

| Exclusion | Reason |
|---|---|
| The redesign, spec amendments and the rebuild | v2.6 (SCOPE-46). v2.5 finds the cause first. |
| The twelve skipped v2.4 requirements (CONF-10, CONF-11, INST-06, INST-07, SPEC-07..10, GATE-05, FEAS-05, RUN-06, DIAG-08) | Charter row C-14 B (owner, 2026-10-27): not carried forward. v2.6 writes fresh ones, and the defects are carried by name above. |
| A graded run or any held-out evaluation | SCOPE-45. The preserved evaluation stays unspent. |
| Physics-term arms | The physics half of suspect 3 cannot be judged until a network fits one orbit (VERD-01). |
| Assembling the `trainex-r5` package | Order A. The owner decides at VERD-02 whether to commission it, and if so it opens v2.6. |
| The GSD 4-agent domain-research pass | Skipped by the owner (2026-10-27). Each phase still gets its own planning research. |
| Charter rows C-8 (Stages 1–6 bars), C-9 (budget) and C-10 (stop rule) | They stay open unless the owner raises them. C-1 and C-3 are recorded rows. |
| Moving phase folders 53–60 and 64 | Code and tests hardcode their paths (owner decisions 2026-10-04 and 2026-10-26). |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| DIAG-09 | Phase 65 | Complete |
| INST-08 | Phase 65 | Complete |
| EXP-01 | Phase 66 | Complete |
| EXP-02 | Phase 67 | Complete |
| EXP-03 | Phase 67 | Complete |
| EXP-04 | Phase 67 | Complete |
| EXP-05 | Phase 67 | Complete |
| YARD-01 | Phase 68 | Pending |
| YARD-02 | Phase 68 | Pending |
| YARD-03 | Phase 68 | Pending |
| VERD-01 | Phase 69 | Pending |
| VERD-02 | Phase 69 | Pending |
| VER-23 | Phase 69 | Pending |

**Coverage:**

- v2.5 requirements: 13 total
- Mapped to phases: 13
- Unmapped: 0 ✓

---
*Requirements defined: 2026-10-27*
*Last updated: 2026-10-31 at Phase 65 closeout: DIAG-09 and INST-08 Complete; 2/13 requirements complete. Traceability mappings unchanged.*
