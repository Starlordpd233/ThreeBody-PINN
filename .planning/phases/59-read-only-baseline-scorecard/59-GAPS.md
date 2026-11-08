# Phase 59 Gap Register

Phase-local register under the STOP protocol, as applied to v2.4. Under that
rule, a source-silent decision is recorded with every field and may be
resolved under the owner's delegation (2026-10-07, re-confirmed 2026-10-09)
**unless** it would move a locked value, spend the evaluation or pre-empt the
verdict. Those go to the owner. Milestone index:
`.planning/milestones/v2.4-GAPS.md`.

Every gap below surfaced in `59-RESEARCH.md` (2026-10-11) during Phase-59
planning and was recorded before any Phase-59 code ran. GAP-59-01..07 are
resolved under the delegation. **GAP-59-08 is RESOLVED-WITH-INSTRUCTION**
(2026-11-08, Owner Checkpoint 2 ruling in Phase 68). It did not block Phase 59.

## In plain language

| Gap | What it decides | Outcome |
|---|---|---|
| 01 | Which saved checkpoint is "step 900" | `best.pt` is step 900, so no stand-in is needed |
| 02 | Where the scorecard's velocities come from, for energy error | From the network's own derivative, not from differencing positions |
| 03 | How the survey labels Stages 2–6 | The spec's rules in ascending order, with Stage 6 as "everything left"; Stage 3 is empty |
| 04 | How the survey estimates chaos (`τ_L`) | The spec's estimator with stated settings and sensitivity columns; diagnostic only |
| 05 | The exact formula behind Gate G1 | Pre-registered before computing |
| 06 | How to normalize the starting-condition inputs without opening test files | Recover the production statistics from a saved checkpoint |
| 07 | Which time grid the scorecard measures on | The dense grid, so a fit that is right only at its training samples does not pass |
| 08 | **The existing energy check fails even a perfect answer** | **Resolved (Option A: autograd velocities in Checkpoint 2)** |
| 10 | The reader's IC13 values are one float32 rounding step over the frozen 1e-7 | Owner accepted it as a recorded deviation; the 1e-7 value is unchanged |
| 11 | Whether "within 1e-4" passes a difference of exactly one fourth-decimal step | Owner: compare the rounded copies in exact decimal units, so it passes |
| 12 | A JX-10 dev result goes stale when Task 2 edits the driver | Rerun JX-10 as a dev run after Task 2's code lands |
| 13 | The scorer's network scoring crashes on the GPU (MPS) runtime | The 59-09 driver scores through a byte-equivalent MPS-safe copy; the shared scorer is fixed before Phase 60 uses it on MPS |

---

## GAP-59-01 — the ruling's "checkpoint 900" exists as `best.pt`

- **Decision point.** D-22 makes `step-000931.pt` the stand-in for the
  ruling's checkpoint 900, on the belief that no step-900 file was retained.
- **Where in artifact.** `59-CONTEXT.md` D-22; `REQUIREMENTS.md` DIAG-07
  ("the retained set is … `best` and `latest`").
- **Task context.** Planning DIAG-07's checkpoint registry.
- **Classification.** Operational coordination: a factual correction.
- **Source silence.**
  - `trainex-r4-ruling.md:124-137` names checkpoints 0, 900 and 951 without
    a file name.
  - The retention manifest lists files, not their steps.
- **Grounding.** `best.pt` carries `counters.global_step = 900`, curriculum
  step 900 and Adam `step = 900`. It was written in the same second as
  `validation_gate/step-00000900.json` (59-RESEARCH C-1, verified by
  metadata). The Phase-58 replay already used `best.pt` as step 900. A
  stand-in 31 steps later measures a different parameter state.
- **Agent was tempted to** keep 931 for continuity with the text.
- **What the user needs to decide.** A: `best.pt` is checkpoint 900, with
  `global_step == 900` asserted in code. B: keep 931 as written.
- **Confidence of impact.** LOW: it corrects an input; no value moves.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-11, owner delegation).
- **Resolution note.** Option A. `step-000931.pt` and `step-000941.pt` stay as
  supplementary readings.

## GAP-59-02 — the scorecard's velocity source for `ε_H`

- **Decision point.** Where the predicted velocities in `ε_H` come from.
- **Where in artifact.** `REQUIREMENTS.md` FEAS-01 (i) ("from the network's
  positions and autograd velocities"); `59-CONTEXT.md` D-01 and D-04 ("the
  gate's own definition").
- **Task context.** Designing the scorer.
- **Classification.** Semantic.
- **Source silence.**
  - `ctl_instruction.md:567` defines `ε_H` for admitted data, where the
    file's velocities exist.
  - `pinn_architecture.md` §10.6 reuses it for predictions without saying
    how velocities are obtained.
  - The production gate differentiates predicted positions by finite
    differences (`pinn/verification/gate_metrics.py:84-122`, `:211-222`).
- **Grounding.**
  - Central differences at the dataset's 0.08 cadence, with inner periods
    down to about 0.1, carry a truncation error of order `(ωΔt)²`.
  - Measured on three Stage-0 training references (IDs 1632, 851 and 4658),
    the finite-difference `ε_H` is 4.7e-2, 2.1e-1 and 3.8e-1, against
    1.1e-14 to 2.1e-14 with the file's velocities. This was independently
    re-run by the orchestrator, 2026-10-11.
  - So the finite-difference route would make Tiers 2 and 3 unreachable for
    any model.
  - The network is an analytic function of `u`, so `dr′/du` by autograd is
    its exact velocity. That is the trainer's own route
    (`controllers.py:1160-1163`).
- **Agent was tempted to** call the production gate function, "the gate's
  own definition", literally.
- **What the user needs to decide.**
  - A: autograd velocities for networks, analytic for the formula, and
    Brutus's for the copy. The finite-difference value is reported as a
    labelled context column.
  - B: the finite-difference route.
  - C: both, gating on finite differences.
- **Confidence of impact.** HIGH: it decides whether Tiers 2 and 3 are
  measurable at all.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-11, owner delegation; FEAS-01's
  own text names autograd).
- **Resolution note.** Option A. The scorer uses
  `matched_plummer_hamiltonian_series` and `trajectory_eps_h`, and never
  `compute_trajectory_gate_metrics`. A static test enforces this. The held-out
  evaluator's own use of finite differences is GAP-59-08.

## GAP-59-03 — stage labels beyond Stage 1: precedence, an empty Stage 3, Stage 6 as the residual

- **Decision point.** How the read-only survey labels Stages 2–6.
- **Where in artifact.** `59-CONTEXT.md` D-18; `REQUIREMENTS.md` FEAS-08.
- **Task context.** Designing the survey's stage assignment.
- **Classification.** Semantic. It is confined to a non-gating survey and the
  probe picks.
- **Source silence.** `ctl_instruction.md:138-264` lists each stage's
  criteria, but:
  - fixes no evaluation order;
  - leaves the mapping beyond Stages 0 and 1 "owner-pending the FUT
    admitted-set EDA run" (`:326-347`, `:1654-1665`);
  - production labels only Stages 0 and 1 (`pinn/data/stages.py:58-85`).
- **Grounding.** Measured over the 6,085 training-split base records:
  - **Stage 6's `s_min < 0.5`** holds for every record, so evaluated first it
    swallows the dataset.
  - **Stage 3's `0.9 ≤ Q ≤ 1.1`** holds for none of the 2,199 standard base
    records (Q is at most 0.119).
  - **Stage 1a** is empty.
  - **The spec's own Stage-6 wording** is "All remaining data", which reads as
    a residual.
- **Agent was tempted to** evaluate the stages in numeric order with no
  residual rule.
- **What the user needs to decide.**
  - A: ascending precedence, Stage 6 the residual; the Stage-3 percentile
    population is the training-split standard base records; Stage 3 reported
    empty, with its measured Q range.
  - B: Stage 6 first.
  - C: leave Stages 2–6 unlabelled.
- **Confidence of impact.** MEDIUM: it shapes the survey and the Stage-6 probe
  pick. Nothing gates on it.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-11, owner delegation).
- **Resolution note.** Option A. Every label records its rule and source. The
  survey states that the labels are diagnostic and that the official mapping
  stays owner-pending.

## GAP-59-04 — the `τ_L` estimator's parameters and fit window

- **Decision point.** The settings of the spec's Rosenstein-style
  revisable-baseline `τ_L`, used to label Stages 4a and 4b and to pick the
  Stage-4b probe.
- **Where in artifact.** `59-CONTEXT.md` D-18 and D-20.
- **Task context.** Designing the survey.
- **Classification.** Semantic, diagnostic only.
- **Source silence.**
  - `ctl_instruction.md:1294-1363` defines the estimator as a revisable
    baseline whose final form is owner-pending (D-33-07).
  - Its snippet (`:1369-1435`) needs `scipy`, which `pinn-train` lacks.
  - The snippet's iteration bound collapses to 1 point on 4 of 6 sampled
    records.
  - Nothing fixes the fit window.
- **Grounding.** On 100 sampled standard base records, the share with `τ_L`
  in (2, 5] runs from 3% to 32% as the fit window goes from 0.5 to 3 time
  units. The class depends on the window, so the window must be fixed before
  the survey runs, and the sensitivity reported.
- **Agent was tempted to** pick a window after seeing the class fractions.
- **What the user needs to decide.**
  - A: the spec's defaults (resampled `dt = 0.01`, embedding `d = 5`, delay
    10, Theiler window 100). The fit runs over the "half-pairs" range. Fixed
    windows of 1, 2 and 3 time units are reported as sensitivity columns.
    Values are labelled diagnostic.
  - B: a single fixed window.
  - C: skip `τ_L`.
- **Confidence of impact.** LOW to MEDIUM: it is non-gating, but it decides
  the Stage-4b probe system.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-11, owner delegation).
- **Resolution note.**
  - Option A.
  - The vectorized estimator is tested against a literal transcription of
    the spec's loop.
  - Degenerate curves return "not computable" with a reason.
  - The survey reports whether the Stage-4b pick changes under the
    sensitivity windows.

## GAP-59-05 — Gate G1's share formula and checkpoint rule

- **Decision point.** What "physics' share of the Adam-preconditioned update"
  means, and at which checkpoints Gate G1 reads it.
- **Where in artifact.** `REQUIREMENTS.md` DIAG-07 (Gate G1); `ROADMAP.md`
  Phase 59 Gate G1; `59-CONTEXT.md` D-24.
- **Task context.** Planning `JX-1`.
- **Classification.** Semantic.
- **Source silence.**
  - `trainex-r4-resolution-doc.md:646` and the ruling give the threshold
    (`10⁻²`) and the phrase "from the stored moments", with no formula.
  - `stage-0-init.pt` has no optimizer state, so checkpoint 0 has no
    moments.
- **Grounding.** Adam's update is `−η m̂ / (√v̂ + ε)`. With the preconditioner
  `P = diag(1/(√v̂ + ε))` taken from the stored `exp_avg_sq`, bias-corrected
  by the stored step, physics' share of the preconditioned total gradient
  `g_tot = Σ λ_k g_k` is the projection `⟨P g_phys, P g_tot⟩ / ‖P g_tot‖²`.
  The shares of all terms sum to 1. Logged raw norms at step 900 (IC 3.0e6,
  physics 109) forecast a share near 1e-5 to 1e-4.
- **Agent was tempted to** use the raw gradient-norm ratio, which ignores
  preconditioning.
- **What the user needs to decide.**
  - A: the primary is the projection share above; the secondary uses `m̂` in
    place of `g_tot`. Both are reported. G1 fires if the primary is at least
    `10⁻²` at checkpoint 900 **or** 951, on the frozen monitor batch.
  - B: the raw-norm ratio.
  - C: the secondary alone.
- **Confidence of impact.** MEDIUM. G1 only triggers a re-examination of
  Phase 61's premise; it pre-empts nothing.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-11, owner delegation).
- **Resolution note.** Option A. Pre-registered in the scorecard before
  `JX-1` runs. A toy two-parameter test checks the formula.

## GAP-59-06 — the IC13 normalizer without opening test files

- **Decision point.** Where the production IC13 normalization statistics come
  from, for the nearest-neighbour distance and for `DIAG-07`.
- **Where in artifact.** `59-CONTEXT.md` D-12, D-16 and D-26.
- **Task context.** Designing the allowlisted reader.
- **Classification.** Semantic, engineering.
- **Source silence.**
  - The production adapter computes the statistics over every admitted
    record of all four folders, test split included, and never persists
    them (`pinn/data/adapter.py:892-893`, `:938-942`).
  - It also opens every test file (`:814-820`). So D-12 ("the production
    data path") and D-26 ("no test file opened") conflict.
- **Grounding.** The normalizer is `tanh((z − μ)/(σ + 1e-8))`, which is
  invertible. A retained checkpoint stores normalized IC13 for 256 records
  whose raw values are recomputable from allowlisted files. That determines
  `μ` and `σ`. The research reproduced 256 × 13 slots to 5.5e-8.
- **Agent was tempted to** recompute the statistics from training and
  validation records only. That would not be the production normalizer.
- **What the user needs to decide.**
  - A: recover the statistics from the retained checkpoint, asserting a
    residual of at most 1e-6; if the assertion fails, fall back to option B
    and record it as a deviation.
  - B: recompute from training and validation records.
  - C: use the stock adapter. That opens test files and is refused.
- **Confidence of impact.** MEDIUM: it affects the nearest-neighbour baseline
  and the `DIAG-07` inputs.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-11, owner delegation).
- **Resolution note.** Option A. `AdmittedSetAdapter` and
  `_build_admitted_sources` are never instantiated by Phase-59 code. A static
  test enforces it.

## GAP-59-07 — the scoring grid

- **Decision point.** Which time grid defines `E`, `h_δ` and `ε_H`.
- **Where in artifact.** `59-CONTEXT.md` D-02 ("over the reference's output
  times"); `REQUIREMENTS.md` FEAS-01 (i) ("over the whole window").
- **Task context.** Designing the scorer and the census.
- **Classification.** Semantic. It is tier-defining and is fixed before the
  scorecard freezes.
- **Source silence.** Neither the proposal nor the requirements chose between
  the 0.08 base grid and the 0.01 gold grid of the same reference.
- **Grounding.**
  - The base grid has 126 samples. 1.5% of Stage-0 training systems have
    fewer than two samples per inner period, and 7.8% fewer than three.
  - A network trained on base-grid samples can match them while being wrong
    between them, so a base-grid score would measure the fit at its own
    training points, not the orbit.
  - The gold sibling agrees with the base trajectory at shared times to
    5.7e-9 on 300 sampled systems (59-RESEARCH C-4).
- **Agent was tempted to** keep the base grid, as written, and report the
  dense one.
- **What the user needs to decide.**
  - A: the dense gold grid (`t ≤ 10`) is tier-defining wherever a gold
    sibling exists, which covers every Stage-0 training and validation
    system; base-grid values are reported beside it.
  - B: base-grid tier-defining, dense reported.
  - C: base grid only.
- **Confidence of impact.** HIGH: it decides what "learned" means for every
  rung.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-11, owner delegation; chosen
  before any scorecard freeze, so SCOPE-42 holds).
- **Resolution note.**
  - Option A.
  - The census verifies gold-base agreement on every Stage-0 system before
    the panels are fixed.
  - The three single-system picks also require at least 3 base-grid samples
    per inner period, so the representation test is not confounded with
    aliased training data. The 16-system family and the validation panel are
    unrestricted, with the samples-per-period flag reported.

## GAP-59-08 — the production energy check fails even a perfect answer (OWNER-ROUTED)

- **Decision point.** The validation gate and the held-out evaluator compute
  `ε_H` from finite-difference velocities of predicted positions, on the
  dataset's coarse output grid. On that grid, the exact Brutus answer already
  scores 5–38%. Should the evaluation's velocity source change before the
  preserved held-out evaluation is ever spent?
- **Where in artifact.**
  - `pinn/verification/gate_metrics.py:84-122` and `:211-222`;
  - `pinn/evaluate.py:472`;
  - `pinn/training/validation_gate.py:257-259`;
  - `pinn_architecture.md` §10.6 (`:1087-1093`).
- **Task context.** Verifying GAP-59-02's measurement during Phase-59
  planning.
- **Classification.** Semantic and cross-phase. It touches the definition of
  the preserved evaluation.
- **Source silence.**
  - §10.6 reuses Step 1A's `ε_H` "as already defined", and Step 1A
    (`ctl_instruction.md:560-570`) is written for admitted data with
    recorded velocities.
  - No source states how velocities are obtained from a network's
    prediction.
  - The finite-difference choice was an implementation fix, recorded in the
    code comment as "review HIGH fix" so the forward pass needs no gradient.
- **Grounding.**
  - **The measurement floor.** Brutus references score finite-difference
    `ε_H` of 4.7e-2, 2.1e-1 and 3.8e-1 (IDs 1632, 851 and 4658, training
    split), against about 1e-14 with true velocities. Under the
    finite-difference route, **no model, not even a perfect one, can pass
    the `1e-5` bar on this data.**
  - **What it does not explain away.** v2.0's held-out 237.2 and generation
    7's validation values of 15.65 and 50.63 are 40 to 5,000 times above
    that floor, so those networks were genuinely far off.
  - **What it does mean.** As implemented, the gate could never certify
    success.
- **Agent was tempted to** fix the evaluator to autograd velocities. That is
  outside Phase 59's scope, and the evaluation is owner-held.
- **What the user needs to decide.**
  - A: the evaluator and validation gate use the network's autograd
    velocities, written into §10.6 by a formal clarifying amendment. This is
    the recommendation: it measures the network's actual motion, and matches
    the v2.4 scorecard.
  - B: keep finite differences on a dense grid. Even at the 0.01 gold
    cadence the floor is likely still above `1e-5` for the fastest
    binaries, so B probably remains unpassable.
  - C: keep the gate as is, knowing it cannot pass.
- **Confidence of impact.** HIGH. It decides whether the project's final exam
  is passable at all, and how every past `ε_H` figure reads.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-11-08, Owner Checkpoint 2 ruling in
  `.planning/phases/68-yardstick/68-CHECKPOINT-2-RULING.md`).
- **Resolution note.** Option A: The evaluator and validation gate use autograd
  velocities ($\mathbf{v}(t) = \partial \mathbf{r} / \partial t$) for neural
  network predictions, resolving the $O(\Delta t^2)$ finite-difference truncation
  floor that caused exact Brutus trajectories to fail the $10^{-5}$ line during the
  Phase 68 yardstick audit. Formal specification clarifying amendment to
  `pinn_architecture.md` §10.6 is routed to milestone v2.6 (`ROUT-68-01`).

## GAP-59-09 — parameters and reading rules the planner pre-registered in the 59-01 scorecard

- **Decision point.** Eight groups of choices that no source fixes, which plan
  59-01 writes into the frozen scorecard contract:
  1. JX-3's 20 trajectories (7 most-anchored, 7 never-anchored with seed
     59031, 6 validation with seed 59032), read by a factor-of-two comparison
     of group medians;
  2. JX-2 "parameter motion": the change from 900 to 951 exceeds the range
     of the 20 draws at both checkpoints (seeds 59020–59039);
  3. JX-4: fixtures are the three single systems plus the monitor anchor; the
     physical scale is the mean squared true acceleration; draw seed 59040;
  4. JX-5: "mixed derivatives" is read as d(dr′/du)/d(IC13), and "skip
     contributions" as each odd block's SIREN and skip branch scales;
  5. numeric limits: the DIAG-07 tolerances, gold-base agreement within 1e-6
     of system size, an unwrap step below π, and a 2% base-grid cross-check
     flag;
  6. the survey:
     - records whose `τ_L` cannot be computed go to "unlabelled", not to
       Stage 6;
     - Stage 1 carries 1a and 1b sub-labels;
     - `τ_L` uses COM-ordered positions in raw time;
     - ties between base and gold records go to base;
  7. panel singles: percentiles are taken over all 1,812 systems, then the
     pick is restricted to systems with at least 3 samples per inner period;
  8. the budget:
     - seconds per step is the timing run's wall time divided by its steps;
     - with no finite reading before the 75% mark, the arm counts as "still
       improving";
     - a formula that does not apply to a counted system goes to the owner.
- **Where in artifact.** `59-01-PLAN.md`, the scorecard contract; listed in
  the planner's return of 2026-10-11.
- **Task context.** Phase-59 planning, before any code runs.
- **Classification.** Process-artifact schema: acceptance-check and reading
  rules for diagnostics.
- **Source silence.**
  - `trainex-r4-resolution-doc.md:644-655` and `trainex-r4-ruling.md:124-137`
    give each experiment's purpose and cost, but no sample seeds, group
    sizes or reading thresholds.
  - FEAS-01 and D-06 give the budget rule's structure but not these edge
    cases.
  - D-31, D-32 and D-33 give the grid, the panel and the survey rules, but
    not these tolerances.
- **Grounding.**
  - Each choice is a measurement or reading convention for a non-gating
    diagnostic, or a conservative edge-case rule. Item 8's "still improving
    without readings" avoids calling an unmeasured arm failed.
  - JX-3's group sizes match the resolution doc's "about 40
    trajectory-checkpoints" (20 trajectories at checkpoints 0 and 951).
  - The 1e-6 agreement limit sits about 175 times above the largest
    measured disagreement (5.7e-9, 59-RESEARCH C-4).
  - The only gating rule in Phase 59 is Gate G1, whose formula is GAP-59-05.
    None of these choices changes it.
  - Fixing the choices before any result is seen is what SCOPE-42 requires.
- **Agent was tempted to** leave them to execution time, which would let a
  result shape its own reading rule.
- **What the user needs to decide.** A: accept all eight as written in 59-01.
  B: change specific items before 59-01 executes. C: drop the reading rules
  and report raw numbers only.
- **Confidence of impact.** LOW: none gates the milestone or moves a locked
  value. Item 7 shapes which three systems Rung 1 sees.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-11, owner delegation; reviewed
  by the orchestrator before 59-01 executes).
- **Governance basis.** In the trainex STOP protocol, a process-artifact
  schema is a MUST-surface class. For v2.4, the owner's delegation covers it:
  under ROADMAP "Feasibility discipline → Delegation and gaps", a
  source-silent decision may be resolved under the delegation unless it would
  move a locked value, spend the evaluation or pre-empt the verdict. None of
  the eight items does any of those, so no separate owner confirmation is
  required. The record above is the surfacing.
- **Resolution note.** Option A. Also accepted: dropping the legacy v1.3
  Rosenstein cross-check. D-18 and D-33 permit it but do not require it, and
  running it needs `sklearn` in an unpinned `.venv`; the spec's own loop is
  the test oracle.
- **Addendum (2026-10-11, after plan-check iteration 2).** The same
  disposition covers the operational parameters the revised plans fix:
  - the memory-preflight floors: 2 GiB before the detached survey pass (plan
    06) and 6 GiB before the DIAG-07 run (plan 07), checked with `vm_stat`;
  - the evidence schema names (`phase59-*/v1`) and the completion-marker
    token strings.

  None gates a result. The floors only refuse to launch on a memory-starved
  machine.
- **Addendum 2 (2026-10-12, after plan-check iteration 2's revision).** The
  same disposition covers:
  - the 600 s wall-time gate on inline steps (census and baselines; measured
    at seconds, 59-RESEARCH Q12);
  - the one-launch lock and the failure record (`phase59-launch-lock/v1`,
    `phase59-launch-failure/v1`), the `LAUNCH-REFUSED` token and exit code 6;
  - the two decision-source check modes in `scorecard-freeze.json`:
    59-CONTEXT.md and 59-RESEARCH.md are checked against their pinned
    blobs, and 59-GAPS.md and 59-VALIDATION.md only at the freeze commit,
    so that gaps recorded mid-phase stay possible.

  After the freeze, mid-phase rulings are recorded in 59-GAPS.md, never by
  editing 59-CONTEXT.md or 59-RESEARCH.md.

---

## GAP-59-10 — the reader acceptance's IC13 residual is one float32 step over 1e-7 (OWNER-ROUTED)

- **Decision point.** Plan 59-05's reader acceptance measured a monitor IC13
  max abs of `1.1920928955078125e-07` (`2**-23`) against the frozen
  `diag07.tolerances.monitor_reproduction_ic13_abs` of `1e-7`. Should the
  census proceed?
- **Where in artifact.** `pinn/verification/stage0_census.py` (`--acceptance`,
  around `:831-906`); the audit check in
  `evidence/verify_phase59_evidence.py:543-544`; `59-SCORECARD.md` (diag07
  tolerances).
- **Task context.** 59-05 Task 2, the first real acceptance run (2026-10-14).
- **Classification.** Semantic. Moving or reinterpreting a frozen value is
  owner-routed (SCOPE-42, `on_failure: stop_and_surface_owner_routed`).
- **Source silence.** The scorecard fixes the value but not how a residual at
  the float32 resolution floor is read. 59-03 had already recorded a
  normalizer residual of `1.192e-7` over 256 keys, after the 59-01 freeze set
  `1e-7`.
- **Grounding.**
  - Targets, times and masses matched bitwise on all 8,192 rows, with zero
    mismatches over 256 identities.
  - The IC13 residual equals the normalizer recovery residual. That one is
    inside its own `1e-6` tolerance, so the gap is the round-off of
    recovering the statistics, not a reader defect.
  - Normalized IC13 lies in (−1, 1), where one float32 step is `2**-24` or
    `2**-23`. So `1e-7` sits below two rounding steps.
- **Agent was tempted to** call it round-off and continue. It did not, because
  the value is frozen.
- **What the user needed to decide.**
  - A: accept the run as a recorded deviation, with the frozen value unchanged.
  - B: amend the tolerance and re-freeze.
  - C: stay halted and investigate first.
- **Confidence of impact.** HIGH for scheduling, since 59-06, 59-08, 59-09 and
  59-10 wait on the census. LOW for the physics.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-14, owner chose A).
- **Resolution note.**
  - The scorecard byte stays `1e-7`. This is not a re-freeze.
  - The acceptance records `passed` against the frozen value exactly as
    measured. It adds an `owner_accepted_deviation` block:
    - `gap`: "GAP-59-10";
    - `frozen_tolerance`: `1e-7`;
    - `accepted_ic13_max_abs`: `1.1920928955078125e-07`;
    - `resolved`: "2026-10-14".
  - With that block, the acceptance continues instead of raising
    `CensusHalt`.
  - The accepted ceiling is exactly the observed `2**-23`. A larger IC13
    residual, any target, time or mass mismatch, or a normalizer residual over
    `1e-6` still halts.
  - The audit's `summary.md` states the deviation in plain words.
  - The verifier's audit check accepts an `ic13_max_abs` above the frozen
    value only when that block names GAP-59-10 and the residual is at most the
    accepted ceiling, and it prints the deviation line.
  - The five DIAG-07 overlay modules are not edited, including
    `production_reference.py`.

## GAP-59-11 — whether "within 1e-4" passes exactly one fourth-decimal step (OWNER-ROUTED)

- **Decision point.** JX-10 compares the Phase-58 packet's 4-decimal fields
  with the measured values rounded to 4 decimals, using
  `phase58_packet_rounded_abs = 1e-4`.
  - In doubles, `2.0539 - 2.0538` is `1.0000000000021103e-4`. So
    `stage-0-init.pt` bin 2 failed: measured 2.0538578 rounds to 2.0539,
    against the packet's 2.0538.
  - Four other cases exactly one step apart passed at `9.999999999998899e-05`.
- **Where in artifact.**
  `evidence/diag07/jx01_jx10.py::_compare_packet` (`:167-192`).
- **Task context.** The 59-07 Task 1 acceptance run (2026-10-14, exit 3,
  run_id `061eb7a1782e4fdba7b1ae3e3bc18282`).
- **Classification.** Semantic. It governs how a frozen tolerance is read.
- **Source silence.** The plan says "rounded fields within 1e-4". It does not
  say whether that difference is taken in exact decimal or binary floating
  point.
- **Grounding.**
  - The packet values are decimal strings to 4 places.
  - In exact decimal units the difference is `1e-4`, and "within" includes the
    bound.
  - The unrounded gap is `5.8e-5`, and CPU float64 measures exactly 2.0538.
  - The largest unrounded gap anywhere is `6.67e-5`.
- **What the user needed to decide.**
  - A: exact decimal units.
  - B: compare unrounded values.
  - C: count one step as a miss, so five checks fail and JX-10 reads
    "falsifies".
- **Confidence of impact.** HIGH. It flips the JX-10 reading.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-14, owner chose A).
- **Resolution note.**
  - `phase58_packet_rounded_abs` stays `1e-4`.
  - Every rounded-field packet comparison takes
    `|Decimal(repr(actual)) - Decimal(repr(expected))| <= Decimal(repr(1e-4))`
    on the 4-decimal rounded copies. Exactly one step passes, and two steps
    fail.
  - The `raw_rbar_bin0` relative check, the exact front-index check and the
    CPU-versus-MPS checks are unchanged.
  - A regression test pins the observed pair (2.0539 against 2.0538 passes,
    2.0540 against 2.0538 fails) and one of the `9.999999999998899e-05` pairs.
  - The same rule applies wherever the verifier recomputes a packet
    comparison.

## GAP-59-12 — a JX-10 development result goes stale when Task 2 edits the driver

- **Decision point.** `verify_phase59_evidence.py diag07` checks each result's
  `producer_sha256` against the current driver files. 59-07 Task 2 edits
  both driver files, so Task 1's development `jx10.json` would fail Task 2's
  `--require jx01,jx10,g1` verify.
- **Where in artifact.** 59-07-PLAN.md Task 2 `<verify>`.
- **Classification.** Operational coordination, resolved by the orchestrator
  under the delegation.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-14).
- **Resolution note.**
  - After Task 2's GREEN commit, run `--experiment jx1` and then
    `--experiment jx10` as development runs. Each is detached, holds the
    launch lock, and is accepted only on `EXIT=0`.
  - Then run Task 2's verify.
  - Task 3's single `--experiment all` run still produces the committed files,
    as planned.

## GAP-59-13 — the scorer's network scoring crashes on the MPS runtime

- **Decision point.** `feasibility_scorer.network_trajectory` (used by
  `score_network`) widens each chunk with one
  `.to(device="cpu", dtype=torch.float64)` call. On an MPS tensor that call
  raises `TypeError: Cannot convert a MPS Tensor to float64 dtype`, the same
  defect 59-07 fixed in its own flatten helper (`936f7f56`). JX-4 must score
  the network on the run's own MPS float32 runtime (D-36), so it cannot call
  `score_network` as written.
- **Where in artifact.** `pinn/verification/feasibility_scorer.py::network_trajectory`
  (the two `.detach().to(device="cpu", dtype=torch.float64)` lines). Found
  while writing 59-09 Task 2. Reproduced on 2026-10-16 with a one-line probe.
- **Task context.** 59-09 Task 2 (JX-4 trajectory errors through
  `score_network`).
- **Classification.** Operational coordination. It is a code defect with one
  correct numeric answer, not a semantic choice, and it is resolved under the
  delegation.
- **Source silence.** The 59-09 plan names `score_network` for JX-4 and the
  MPS runtime for every JX run. It does not anticipate that the scorer cannot
  run on MPS: the scorer's tests run on the CPU only.
- **Grounding.**
  - Fixing the scorer in place would change its SHA-256. That hash is pinned
    as `producer_sha256` in the committed Plan-07 `jx01.json`, `jx10.json`
    and `g1.json`, so `verify_phase59_evidence.py diag07` would fail until
    those were re-run. 59-09's I-2 requires those files to stay byte-unchanged.
  - Moving to the CPU before widening gives the same float64 numbers as the
    one-call form on a CPU tensor, so a copy differing only there scores
    identically.
- **Agent was tempted to.** Fix the scorer in place and re-run JX-1 and
  JX-10. Rejected because it rewrites committed Plan-07 evidence.
- **Options.**
  - A: an MPS-safe copy of `network_trajectory` in the 59-09 driver.
    `network_score` calls the scorer's own `score_trajectory` and
    `physics_residual_context`.
  - B: fix the scorer and re-run 59-07's JX-1 and JX-10.
  - C: score JX-4 on a CPU copy of the model.
- **Confidence of impact.** MEDIUM. JX-4 cannot run without one of these.
  Phase 60 will hit the same defect when it scores networks on MPS.
- **Status.** RESOLVED-WITH-INSTRUCTION (2026-10-16, delegation; option A).
- **Resolution note.**
  - `jx02_jx05.py::network_score` and `_network_trajectory` mirror the scorer
    line for line, except that each chunk is moved to the CPU before it is
    widened.
  - `NetworkScoreTests` pins `network_score` equal to `score_network` field
    for field on a CPU float64 network.
  - The shared scorer stays byte-unchanged in Phase 59.
  - **Forward item for Phase 60:** fix `network_trajectory` in place, with an
    MPS regression test, before the first rung scores a network on MPS. That
    fix changes the scorer's SHA-256, so Phase 60 records the change and does
    not re-run the Phase-59 evidence that pins the old hash.
