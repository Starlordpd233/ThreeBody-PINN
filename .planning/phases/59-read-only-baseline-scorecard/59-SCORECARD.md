# Phase 59 Feasibility Scorecard (frozen)

**Audience:** the project owner, a non-specialist.
**This document is:** the plain-language twin of pinn/verification/artifacts/feasibility_scorecard_v1.json.
**This document is not:** a result. Nothing in it was computed on real data.

## In plain language

This scorecard is the ruler. Later work holds a predicted orbit up to the true one and reads the mark on this ruler. The ruler is being locked now, before any of those measurements, so a pass mark cannot be moved after a result is seen.

It measures three things. How far the predicted orbit drifts from the true one, both for the system as a whole and for the inner pair. How long the prediction stays inside 1 percent and inside 10 percent. How well energy is conserved along the prediction.

There are four tiers. Tier 3 is a tight orbit that also conserves energy tightly. Tier 2 is the same tight orbit with a looser energy mark. Tier 1 is a coarser orbit, with no energy mark. Tier 0 is everything else, including a position error that is not a real number.

Any later change to a value in this ruler goes to the owner (SCOPE-42). This phase does not reset a threshold after a census, a baseline, a survey, or a checkpoint experiment.

## The measurements

Two position errors are scored at each output time. `e_sys` is the worst body, divided by the largest reference radius in the centre-of-mass frame over the scoring times. `e_in` is the inner-pair separation error, divided by the true separation. The inner pair is bodies 1 and 2 of the initial-condition file, tracked through the preprocessing permutation.

The tier-defining error `E` is the worst of those two errors over the scoring times. The valid horizons `h_delta` use deltas 0.01 and 0.1: each is the first scoring time at which the worst of the two errors exceeds that delta, divided by `T`, or 1 if that never happens.

Energy error uses the gate's own formula from ctl_instruction.md:567:

`eps_H = max_t |(H(t) - H(0)) / H(0)|`

The Hamiltonian is `gate_metrics.matched_plummer_hamiltonian_series` together with `trajectory_eps_h`, with the gate's inverse-epsilon `eps_h_eps_inv = 1e-10`.

Velocity depends on the kind of prediction. A network uses autograd. The two-Kepler formula uses its analytic velocity. The nearest-neighbour copy uses Brutus velocities. A finite-difference velocity is reported only as a labelled context column. It is not the velocity the tier uses.

The tier-defining grid is the gold sibling, spacing `gold_dt = 0.01`, out to `t_max = 10`. The base grid, spacing `base_dt = 0.08`, is reported beside it and does not set the tier. Gold and base positions at shared times must agree to `gold_base_agreement_max = 1e-6` before panels are fixed. Samples per inner period are `T` over `N_in` over the measured base spacing.

A physics residual is context only. It is never a gate. It is the acceleration minus the trainer's softened force at softening `1e-5`, using the scored system's ordered masses, in the `r_prime` / `u` frame, then the mean and the max over scoring times of the body-averaged squared residual divided by the governed `R_ref` in `pinn/verification/artifacts/r_ref_stage0.json`. The acceleration source is autograd's second derivative for a network, analytic Kepler for the formula, and a neighbour Newtonian acceleration on the copy's own positions and masses at softening `1e-12`.

The frame is named `r_prime_u`: position `r_prime`, time `u = t/T`, velocity `dr_prime/du`, masses the ordered raw masses. `D = 4.641588833612778` and `T = 10`. The scores are ratios or a relative energy error, so they do not change just because the same orbit is written in the raw frame or the scaled frame.

## The tiers

A level passes when the value is less than or equal to the bound. A missing energy bound means that level has no energy condition. A non-finite `E` is Tier 0. A non-finite `eps_H` fails every level that has an energy bound.

| Tier | Position error `E` | Energy error `eps_H` |
|---|---|---|
| 3 | `E <= 0.01` | `eps_H <= 1e-5` |
| 2 | `E <= 0.01` | `eps_H <= 0.001` |
| 1 | `E <= 0.1` | no energy condition |
| 0 | otherwise | otherwise |

## When a result counts

A system counts only when its tier is at least 1 and its `E` is strictly below the two-Kepler formula's `E` on that same system. An equal `E` does not count. If the formula is not applicable on a counted system, the case goes to the owner. It is not scored as a quiet failure.

## How the verdict is decided

Gate G2 fires when at least 2 of the 3 single-system runs are below Tier 1. The settings sweep then runs. If the sweep rescues a system to Tier 1, the case stops at owner checkpoint 4. If it rescues nothing, the verdict is RETHINK-REPRESENTATION and the later rungs are not read.

If G2 does not fire, the verdict is GO only when all three of these hold: Rung 2b counts on at least 2 of 3, Rung 3 counts on at least 12 of 16, and the control branch is `a`. Otherwise the verdict is PIVOT-TRAINING, and it names each clause that failed. The control branches on the menu are `a`, `b`, `c`, and `d`. Only `a` is a GO.

If Rung 1, shown the answer, beats the formula on fewer than 2 of 3 systems, the verdict adds a representation-limit qualifier, whatever the branch.

Reported, and not part of the verdict: Rung 2a, the validation panel against the baselines, the hard-stage probes, the survey, and the distance to `1e-5`.

## Fairness rules for every arm

Each arm's step budget comes from a timing run of at least 50 steps. Seconds per step are that run's wall time divided by its steps. A single-system arm is capped at 3.0 hours. Rung 3 is capped at 8.0 hours. The control keeps 1000 Adam steps.

"Still improving" compares the best `E`. The reference window is steps at or before 75 percent of the budget. The final window is the last 25 percent. Non-finite readings are ignored. No finite final reading means not improving. A finite final reading with no finite reference reading counts as improving. Otherwise the best final `E` must be at most 90 percent of the best reference `E` (a relative drop of at least 0.1).

One extension is allowed, and it doubles the budget (factor 2.0). If the arm is still improving after that extension, the outcome is inconclusive and the rate of improvement is reported. Otherwise the outcome is complete.

Scoring readings include the start and the end, and no gap may exceed 5 percent of the budget (`scoring_cadence_max_fraction = 0.05`).

Every single-system arm then takes a full-batch L-BFGS polish: history size 10, strong Wolfe line search, and at most 50 iterations per call. Arms with a physics term keep the freeze in 57-RULING.md:112-124. The polish stops at 5 outer calls without improvement, or at 25 percent of that arm's Adam wall time, whichever comes first. The kept state is the better of Adam and the polish, compared on `E` and then `eps_H`, with non-finite values last. An exact tie keeps Adam. Both states are reported.

## The settings sweep (G2)

The swept parameter is `first_omega_0`. The locked value is 30.0. The frozen grid is 60, 120, 240, 480. The sweep is data-only. It starts on the failing panel system with the fewest inner laps, then confirms on the next failing panel system by inner laps. Rescue means Tier 1. Rescue goes to owner checkpoint 4. No rescue is RETHINK-REPRESENTATION.

D-08 froze this grid because a higher first-layer frequency is the usual lever against spectral bias, against an estimate of up to about 80 inner laps in the Stage 0 window. The research's initial-edge table compares `omega_0/14` radians per unit `tau` with the required `pi*N`. It is a research estimate, to be re-derived by the census. It is not a second pass mark.

| `omega_0` | 30 (locked) | 60 | 120 | 240 | 480 |
|---|---|---|---|---|---|
| Initial edge `omega_0/14` (rad per unit tau) | 2.1 | 4.3 | 8.6 | 17.1 | 34.3 |

| Census quantile of `N_in` | p10 | p50 | p90 | p99 | max |
|---|---|---|---|---|---|
| Required `pi*N` (rad per unit tau) | 33 | 58 | 124 | 204 | 320 |

## Accuracy readings during training

Read the accuracy every 100 optimizer steps, and also at the initial state and the final state. Rung 3 is read on the 16-system family and on the 227-system validation panel. The control is read on the validation panel.

## Which systems are used

The single-system percentiles and the 16-system family are drawn from the Stage 0 training population, size 1812. Difficulty is `N_in`, estimated by an alias-safe unwrap of the inner separation on the gold grid for `t <= 10`, with an unwrap step no larger than pi (`3.141592653589793`). Percentiles use numpy's linear percentile. The singles are the 10th, 50th, and 90th percentiles of all Stage 0 training systems, and only among systems with at least 3.0 base-grid samples per inner period. Distance is the absolute gap in `N_in`. Ties go to the lowest id.

The family has 16 systems. Sort by `N_in`, then id, and split with numpy's array split into bins of sizes 114, 114, 114, 114, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113. From each bin, take the system nearest the numpy median of that bin, excluding the three singles, and break ties by the lowest id. The validation panel is every Stage 0 validation system, size 227.

## Census and survey rules

The census population signature is hierarchical, stage 0, label UNASSIGNED. The inner normal is the unit cross of the initial separation and its derivative. The outer vector runs from the inner-pair centre of mass to the third body. A base-grid cross-check uses mean-motion-assisted unwrap and flags a relative disagreement above 0.02. Phase-accuracy deltas are 0.01 and 0.1. Acceleration in the census is the softened acceleration at `1e-5` in the `r_prime` frame. The tracked pair must be the closest pair at `t = 0` on all Stage 0 training and validation systems, and gold-base agreement is checked on that same population. A failed check stops before the panels are fixed and goes to the owner.

Survey labels are diagnostic. The official stage mapping stays owner-pending. Precedence is 0, then 1, then 2, then 3, then 4a, then 4b, then 5, then 6, and Stage 6 is the residual. Stages 0 and 1 come from the splits-manifest record stage. Substage 1a is energy from -0.5 inclusive up to but not including -0.1. Substage 1b is energy below -0.5 with an angular-momentum ratio from 0.1 inclusive up to but not including 0.5. Stage 2 is the hierarchical gold records. Stage 3 is standard-base training records at or below the 25th energy percentile and at or above the 75th angular-momentum-ratio percentile, with `Q` from 0.9 to 1.1. Stage 4 is the standard base that is not Stage 3: 4a has `tau_L` above 5.0, and 4b has `tau_L` above 2.0 and at most 5.0. Stage 5 is standard gold with `tau_L` above 2. Stage 6 keeps the recorded residual clause `s_min < 0.5` or absolute energy below 0.01. A `tau_L` that cannot be computed is unlabelled, with a reason, and is not forced into Stage 6.

`tau_L` uses centre-of-mass ordered positions and raw time, resampled linearly at `dt = 0.01` out to `t_max = 10`, embedding dimension 5, delay 10, Theiler window 100, and minimum distance `1e-9`. The primary fit is the half-pairs window. Sensitivity windows are 1.0, 2.0, and 3.0. A fit needs at least 2 points. A non-positive slope is recorded as infinite. Error growth is `exp(T / tau_L)` with `T = 10`, and 1 when `tau_L` is infinite. Ordering uses the stage median and Spearman rank with average ties. The Stage 4b pick is the median primary `tau_L`. The Stage 6 pick is the median `s_min` invariant at `t = 0`. Nearest means the absolute gap from the numpy median. Ties go to the lowest id, and base before gold. An empty stage is recorded with no substitute unless the owner says otherwise. The survey also reports whether the 4b pick changes under each sensitivity window.

## Checkpoint experiments and Gate G1

These experiments run against generation 7's code at commit `629b1a6ca4462915b6340a59b8d4e3ad8df75d8b`, on a snapshot whose `pinn` and `configs` blobs match that commit. The primary runtime is float32 on MPS. JX-1 and JX-10 are cross-checked in float64 on CPU. The microbatch size is 256. Memory high water is `ru_maxrss`. A checkpoint is loaded only after its SHA-256 matches the generation-7 retention record, and then weights only.

The retained steps are: for `stage0-v23g7-seed42`, `stage-0-init.pt` at 0, `best.pt` at 900, `step-000931.pt` at 931, `step-000941.pt` at 941, `step-000951.pt` at 951, `latest.pt` at 951, and `failure-stage-0-step-951.pt` at 951; for `stage0-v23g7-smoke`, steps 100, 200, and 300.

Gate G1 reads the primary share at checkpoint 900 (`best.pt`) or 951 (`step-000951.pt`), on the frozen monitor batch. The share is the projection of the preconditioned physics gradient on the preconditioned total gradient:

`primary = <P g_phys, P g_tot> / ||P g_tot||^2`

`P` is the inverse of `sqrt(v_hat) + eps`. `v_hat` is `exp_avg_sq` bias-corrected by `1 - beta2^step`. `m_hat` is `exp_avg` bias-corrected by `1 - beta1^step`. The physics vector is `lambda_phys` times the physics gradient. The total vector sums `lambda` times each term's gradient, at the scheduled weights restored for the current step. The secondary share is the same projection with `m_hat` as the total. G1 fires if either checkpoint's primary share is at least 0.01. Firing means the Phase 61 premise is re-examined before Phase 61 opens. Not firing means proceed. A non-finite share is not determinable and goes to the owner.

Tolerances, frozen before any of these runs: the Phase 58 packet front index matches exactly; rounded packet values within 0.0001 absolute; raw `rbar` bin 0 within 0.0001 relative; CPU versus MPS front index exactly, and the scaled residual, prefix, gradient norm, and share within 0.001 relative, with a share absolute floor of `1e-7`; the G1 outcome identical; driver versus trainer gradient norm within `1e-5` relative; monitor targets, times, and masses bitwise in float32; monitor IC13 within `1e-7` absolute; normalizer recovery within `1e-6` absolute. A miss stops and goes to the owner.

JX-1, at steps 0, 900, and 951 on the frozen monitor batch, reads the data, IC, physics, energy, and angular-momentum terms, the cosines of IC with physics, IC with data, and physics with data, and splits the IC term into position and velocity. Shares need Adam moments. A physics share at or below `1e-4` supports "physics was a passenger". A share at or above 0.01 falsifies that claim, which is the same bar as Gate G1.

JX-2 follows the frozen monitor anchor at steps 0, 900, 931, 941, and 951. It draws 20 stratified collocation samples, 16 bins by 256, from seed base 59020. The statistic is the prefix through the bin, and the bin is the max of the frozen front at 900 and 951. Parameter motion is claimed only if the frozen change from 900 to 951 exceeds the draw range at both checkpoints. Otherwise estimator noise is not excluded.

JX-3 compares steps 0 and 951. It uses 7 high-exposure trajectories, 7 never-anchored trajectories from seed 59031, and 6 validation trajectories from seed 59032. Anchors are replayed at steps 1 and 951. Times are the frozen monitor collocation times. Statistics are `L_IC` and the sum of the scaled residual. The pattern is exposure-specific if group A's median ratio is below half of both B and C, global if B and C stay within a factor 2 of A, and otherwise inconclusive.

JX-4, at steps 0, 900, and 951, uses the three single-system picks and the frozen monitor anchor, with draw seed 59040. The physical scale is the mean, over gold snapshots at `t <= 10`, of the body-averaged squared true softened acceleration. The physical front replaces `R_ref` with that scale inside the causal physics loss. Relative descent without accuracy means the front rose from 0 to 951 and every fixture is still Tier 0 at 951. Accuracy with descent means the front rose and some fixture reached Tier 1 or better with `E` at 951 no worse than 0.9 times `E` at 0. Otherwise inconclusive. This informs the scale question only.

JX-5 reads `stage-0-init.pt` on the frozen monitor anchor and its collocation times, taking every 16th row of the time-sorted times. It describes position, velocity, acceleration, force, residual, residual bins, IC position and velocity error, the mixed derivative of velocity with respect to IC13, and the skip versus SIREN branch values. The reading is structural and descriptive. It is not a decision input.

JX-10 expects the smoke checkpoints at 100, 200, and 300 to keep front index 0. It reproduces `stage-0-init.pt`, `best.pt`, and steps 931, 941, and 951 against the Phase 58 packet below. Support means the smoke front is 0 at all three checkpoints and the seed-42 packet matches within the tolerances above. Otherwise the check falsifies the claim.

| Checkpoint | front | prefix through front | prefix to cross next | rtilde bins 0 to 5 | raw rbar bin 0 | rtilde median |
|---|---|---|---|---|---|---|
| stage-0-init.pt | 0 | 0.8754 | 1.6975 | 0.8754, 0.8221, 2.0538, 2.7849, 1.4951, 1.0632 | 17288675328.0 | 1.1058 |
| best.pt | 1 | 0.7277 | 1.3443 | 0.3099, 0.4178, 0.6166, 1.0578, 0.8126, 0.6346 | 6120390144.0 | 0.6363 |
| step-000931.pt | 2 | 1.1922 | 2.4369 | 0.2447, 0.3085, 0.639, 1.2448, 0.7146, 0.7053 | 4832969216.0 | 0.6473 |
| step-000941.pt | 2 | 1.1815 | 2.4272 | 0.2444, 0.3042, 0.6329, 1.2457, 0.7103, 0.7145 | 4827524608.0 | 0.6404 |
| step-000951.pt | 2 | 1.1891 | 2.452 | 0.2496, 0.3009, 0.6386, 1.263, 0.7274, 0.7032 | 4929262080.0 | 0.6578 |

## Not decided here

GAP-59-08 stays open. The existing validation gate and the held-out evaluator compute energy error by finite differences of predicted positions. On the coarse output grid, that check cannot pass even the exact answer. The question is owner-routed. This scorecard does not use that path. Phase 59 reports the gap and does not fix it.

## Frozen identity

The machine file is `pinn/verification/artifacts/feasibility_scorecard_v1.json`. Its schema version is `phase59-feasibility-scorecard/v1`. Its size is 17966 bytes. Its SHA-256, which is also `SCORECARD_SHA256` in `pinn/verification/feasibility_scorecard.py`, is `f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b`.
