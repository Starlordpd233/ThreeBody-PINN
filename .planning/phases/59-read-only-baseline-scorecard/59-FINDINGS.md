# Phase 59 Findings: Read-Only Baseline and Scorecard

**Audience:** the project owner.
**Scorecard:** SHA-256 f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b (frozen before any result; commit order verified).

Every number below is copied from a committed evidence file named in the evidence index at the end. Prose rounds for readability; the exact value is in the named file.

## In plain language

1. **The ruler came first.** Before anything was measured, we froze the scorecard: the rules for scoring a network, in physical units. Every result in this phase was committed after that freeze, and the checker proves the order.
2. **Stage 0 is genuinely hard.** In a typical Stage-0 system the inner pair goes round about 18.6 times in the 10-unit window. To land within 10% of the right place at the end, a network has to time those laps to about 1 part in 1,169.
3. **The textbook formula does not already pass.** It treats the inner pair and the outer body as two separate textbook orbits. It reaches the Tier-1 line on 1 of 1,812 training systems and none of the 227 validation systems.
4. **Copying the most similar training system does worse.** Its median error is 2.14, against the formula's 0.94 on the validation systems.
5. **The hardest later stages are chaotic.** At Stage 6, a tiny starting error grows by a median factor of about 352 within the window; at Stage 4b, by about 29.
6. **Generation 7's saved checkpoints taught us three things.** The physics term had almost no say in how the network was updated. The run's own progress signal moved without any real accuracy behind it. And at the start the network's accelerations were about 6,600 times too large.
7. **Gate G1 did not fire.** The outcome is "proceed": Phase 61 goes ahead as planned.
8. **One decision waits for the owner (GAP-59-08).** The existing energy check fails even a perfect answer, so the project's final exam cannot be passed as it is written today. Nothing in Phase 59 changed it.

## Does the two-Kepler formula already reach Tier 1 on Stage 0?

**No.**

| Population | Reaches Tier 1 or better | Median E |
|---|---|---|
| Stage-0 training | 1 of 1812 | 0.989 |
| Stage-0 validation | 0 of 227 | 0.940 |

Source: `evidence/baselines/baselines.json`.

**What the formula is.** It treats the inner pair as one textbook orbit and the outer body's path around the pair as a second one. It starts exactly right, but the third body's pull slowly bends the real orbits away from it. A median E near 1 means its position error over the window is about as large as the scale of the inner orbit itself. The tiers are set in the frozen scorecard: Tier 1 needs E ≤ 0.1.

**The single exception.** The one training system where the formula reaches Tier 1 is id 2230, with E 0.0667 (`evidence/baselines/two_kepler_population.csv`).

**What this means for the counting rule.** A system counts only when the network reaches Tier 1 or better and its E is strictly below the formula's E on that same system. On Stage 0 the formula sits far above the Tier-1 line almost everywhere. In practice, then, a network that reaches Tier 1 on a Stage-0 system will nearly always also beat the formula there. The rule only bites on systems like id 2230.

## How hard Stage 0 is

These numbers cover the 1,812 Stage-0 training systems, from `evidence/census/census.json`. "Inner laps" (N_in) is the number of times the inner pair goes round by t = 10. "Outer laps" (N_out) is the number of times the outer body goes round the pair.

| Measure | 10th percentile | Median | 90th percentile | Max |
|---|---|---|---|---|
| Inner laps N_in | 10.47 | 18.61 | 39.35 | 101.74 |
| Outer laps N_out | 0.894 | 1.82 | 4.02 | 12.02 |

**Phase accuracy.** This is how precisely a network must time the inner laps.
- To keep the end-of-window miss under 10%, the median system needs a figure of 0.000855, about 1 part in 1169.
- To keep it under 1%, the figure is 8.55e-05, about 1 part in 11692.

**Under-sampling on the base grid.** The base grid is the coarse 0.08 time step on which the dataset is stored.
- 28 training systems have fewer than 2 samples per inner lap.
- 148 have fewer than 3.
- 545 have fewer than 5.

On those systems the stored points barely trace the inner orbit.

**Census checks.**
- Pair-tracking failures: 0.
- Gold-to-base maximum deviation: 9.68e-07, within the 1e-06 tolerance.
- The census also scored the 227 validation systems for the agreement check.

## The panels

Every system below was chosen by the frozen panel rule, not by hand (`evidence/census/panels.json`).

**The three single systems.** Each is the eligible training system nearest the 10th, 50th and 90th percentile of inner laps. To be eligible, a system needs at least 3 base samples per inner lap, and a tie goes to the lower id.

| Percentile | id | Inner laps N_in | Base samples per inner lap |
|---|---|---|---|
| 10 | 1632 | 10.47 | 11.94 |
| 50 | 851 | 18.61 | 6.72 |
| 90 | 4658 | 39.35 | 3.18 |

**The 16-system family.** The 1,812 training systems are sorted by inner laps and split into 16 equal bins. Bins 0 to 3 hold 114 systems each and bins 4 to 15 hold 113. From each bin the rule takes the system nearest the bin's median, excluding the three singles. The family spans the whole census, from 8.9 to 52.5 inner laps.

| Bin | id | N_in | Bin | id | N_in |
|---|---|---|---|---|---|
| 0 | 3891 | 8.92 | 8 | 3589 | 19.49 |
| 1 | 4345 | 10.35 | 9 | 2021 | 21.13 |
| 2 | 1709 | 11.65 | 10 | 1610 | 23.17 |
| 3 | 4513 | 12.81 | 11 | 367 | 26.22 |
| 4 | 1250 | 14.02 | 12 | 4056 | 29.66 |
| 5 | 3970 | 15.21 | 13 | 2777 | 33.91 |
| 6 | 2270 | 16.42 | 14 | 2303 | 40.06 |
| 7 | 4189 | 17.89 | 15 | 1383 | 52.53 |

**The validation panel.** All 227 Stage-0 validation systems. No test-split file was opened anywhere in this phase.

## The comparison points

Both comparison points were scored with the same scorer that will score the networks (`evidence/baselines/baselines.json`).

| Comparison point | Panel | Tier 0 | Tier 1 | Tier 2 | Tier 3 | Median E |
|---|---|---|---|---|---|---|
| Two-Kepler formula | three singles | 3 | 0 | 0 | 0 | |
| Two-Kepler formula | 16-system family | 16 | 0 | 0 | 0 | |
| Two-Kepler formula | Stage-0 training (1,812) | 1811 | 1 | 0 | 0 | 0.989 |
| Two-Kepler formula | validation (227) | 227 | 0 | 0 | 0 | 0.940 |
| Nearest-neighbour copy | validation (227) | 227 | 0 | 0 | 0 | 2.135 |

**The nearest-neighbour copy.** For each validation system, it copies the real orbit of the training system with the closest starting state. A nearby starting point still drifts onto a different orbit within the window, so the copy does worse than the formula. With 1,812 training systems, Stage 0 is not covered densely enough for simple lookup to work.

**The FEAS-09 probes.** Both FEAS-09 probe systems are standard quasi-random records, not hierarchical ones: `standard/base/2279` (Stage 4b) and `standard/base/3418` (Stage 6). Such systems have no inner pair to split off. `evidence/survey/picks.json` and `baselines.json` both record "not applicable: no hierarchical split" for the formula on them. Phase 60 therefore has no formula comparison for those two probes.

## The whole-dataset survey

This is a read-only survey of all 12023 training-split records (`evidence/survey/survey.json`). The stage labels and the Lyapunov times are diagnostic only. The official stage mapping beyond Stages 0 and 1 is owner-pending, and nothing in the survey gates a result.

How to read the columns:
- **Closest approach** is the smallest distance between any two bodies.
- **Peak acceleration** is the largest acceleration in the window.
- **tau_L** is the Lyapunov time: how long it takes a small error to grow by a factor of e.
- **Error growth** is e^{10/tau_L}: how much a small starting error grows by t = 10.

| Stage | Records | Median inner laps | Median closest approach (smallest) | Median peak acceleration | Median tau_L (finite / infinite) | Median error growth |
|---|---|---|---|---|---|---|
| 0 | 1812 | 18.61 | 0.03929 (0.005466) | 582.4 | 21.41 (1495 / 317) | 1.22 |
| 1 | 2074 | 25.02 | 0.03801 (0.008621) | 787.4 | 24.64 (1660 / 414) | 1.10 |
| 2 | 3886 | 21.53 | 0.03859 (0.003302) | 685.9 | 21.25 (3125 / 761) | 1.15 |
| 3 | 0 | (empty) | (empty) | (empty) | (empty) | (empty) |
| 4a | 1404 | not applicable | 0.01594 (0.001748) | 3966 | 10.74 (655 / 749) | 1.0 |
| 4b | 654 | not applicable | 0.01701 (0.002139) | 3504 | 2.984 (654 / 0) | 28.53 |
| 5 | 1923 | not applicable | 0.005793 (0.0002672) | 2.98e+04 | 5.02 (1225 / 698) | 2.144 |
| 6 | 269 | not applicable | 0.007083 (0.0007175) | 1.993e+04 | 1.706 (269 / 0) | 351.6 |

Notes on the table:
- **No inner-lap count.** Stages 4a to 6 are standard quasi-random records, so they have no inner pair to count laps for.
- **Stage 3 is empty.** It needs a virial ratio between 0.9 and 1.1, and the standard base records span only 0.0006319 to 0.1192.
- **One unlabelled record.** tau_L could not be computed for it, so it was not pushed into any stage.
- **No unreadable tau_L in the labelled stages.** "Not computable" is 0 for every labelled stage.

**Difficulty order against the curriculum order.** The curriculum order is 0, 1, 2, 4a, 4b, 5, 6. The table gives each measure's ranking from hardest to easiest and its Spearman rank agreement with that curriculum order.

| Measure | Hardest to easiest | Agreement with curriculum order |
|---|---|---|
| tau_L | 6, 4b, 5, 4a, 2, 0, 1 | 0.93 |
| Closest approach | 5, 6, 4a, 4b, 1, 2, 0 | 0.89 |
| Peak acceleration | 5, 6, 4a, 4b, 1, 2, 0 | 0.89 |
| Error growth | 6, 4b, 5, 0, 2, 1, 4a | 0.64 |
| Inner laps (Stages 0 to 2 only) | 1, 2, 0 | 0.5 |

Broadly, the later stages are harder, as the curriculum assumes. One exception: Stage 1 has more inner laps than Stage 2, and both have more than Stage 0.

**The FEAS-09 probe picks** (`evidence/survey/picks.json`):
- **Stage 4b: `standard/base/2279`.** Its tau_L is 2.984, at the stage median over 654 candidates.
- **Stage 6: `standard/base/3418`.** Its t = 0 minimum separation is 0.2657, at the stage median over 269 candidates.
- **Both picks are fragile.** Under each of the three sensitivity fit windows (1, 2 and 3 time units), both picks change.
  - Stage 4b: `standard/base/1916`, `standard/base/281`, `standard/base/73`.
  - Stage 6: `standard/base/512`, `standard/base/1074`, `standard/base/509`.

  So the Stage-4b pick is not robust to the tau_L estimator's fit window. These picks are the pre-declared rule's output, not a judgment about which system is most informative.

### Is a per-system energy bar of 1e-5 plausible at Stages 4b and 6?

Copied from `survey.json` per_stage.

| Measure | Stage 4b | Stage 6 |
|---|---|---|
| Records | 654 | 269 |
| tau_L, median (p10 to p90) | 2.984 (2.247 to 4.55) | 1.706 (1.05 to 1.926) |
| tau_L, infinite / not computable | 0 / 0 | 0 / 0 |
| Error growth e^{T/tau_L}, median (p10 to p90) | 28.53 (9.007 to 85.71) | 351.6 (179.7 to 1.367e+04) |
| Error growth, min to max | 7.453 to 141.4 | 150.5 to 3.731e+05 |
| Closest approach, minimum / median | 0.002139 / 0.01701 | 0.0007175 / 0.007083 |
| Acceleration range (smallest acc_min to largest acc_max) | 0.1324 to 2.185e+05 | 0.3258 to 1.942e+06 |

Judgment, not a gate: a per-system relative energy error of 1e-5 looks implausible for a network at Stage 6, and very doubtful at Stage 4b. In both stages every system is chaotic within the window: no tau_L is infinite. A starting error grows by a median of about 29 at Stage 4b and about 352 at Stage 6. Across each stage, accelerations span about six orders of magnitude. Within a typical system they span about three: the median smallest is 4.404 against a median peak of 3504 at Stage 4b, and 6.241 against 1.993e+04 at Stage 6. The median closest approaches are 0.01701 and 0.007083. Near such an approach the kinetic and potential energy are both very large and nearly cancel. Holding their sum to 1 part in 100,000 then needs the speed at the closest point to be right to much better than 1e-5 of the total. This is integrator-grade accuracy, and it must hold exactly where the motion changes fastest. For comparison, generation 7's own energy errors at step 951 on Stage-0 fixtures were between 4.0 and 53.9 (JX-4 below), and Stage 0 is the gentlest stage. This reading gates no phase and is not a verdict input. It rests on diagnostic stage labels whose official mapping is owner-pending.

## The checkpoint experiments (DIAG-07)

All six experiments read generation 7's saved checkpoints without training them (`evidence/diag07/`).
- Run: `stage0-v23g7-seed42`.
- Checkpoints: step 0 (`stage-0-init.pt`), checkpoint 900 (`best.pt`, which is checkpoint 900), and steps 931, 941 and 951.
- Device: MPS float32, with a CPU float64 cross-check where noted.

**JX-10 (does the monitor reproduce?)** Reading: supports (C-F14, F-H2b, C-07 numeric).
- The run's frozen "is the front advancing" monitor reproduces the values recorded in Phase 58. On seed 42 the front reads 0, 1, 2, 2 and 2 at steps 0, 900, 931, 941 and 951.
- The smoke run's front is 0 at steps 100, 200 and 300.
- The CPU float64 cross-check matched the MPS run on every front and prefix, and all 54 of JX-10's recorded tolerance checks passed.

**JX-1 (was physics a passenger?)** Reading: "900: supports: physics was a passenger (PC-2); 951: supports: physics was a passenger (PC-2)".
- The physics term supplied 7.187e-07 of Adam's actual update direction at step 900 and 2.605e-08 at step 951. Anything at or below 1e-4 reads as a passenger.
- The CPU float64 cross-check gave 6.94e-07 and 2.59e-08, with the same reading.
- The IC anchor term supplied almost all of the update.
- At step 0 no Adam moments are stored, so no share is computable there.

**JX-2 (did the monitor move by more than its own noise?)** Reading: "estimator noise not excluded".
- From step 900 to 951 the monitor's prefix through bin 2 changed by 0.1552.
- Twenty fresh draws of collocation times spread it by 0.1717 at step 900 and 0.1406 at step 951.
- The change is not larger than both ranges, so it cannot be called real progress.

**JX-3 (was the improvement global or specific?)** Reading: "mixed: exposure-specific / global".
- Replaying the run's batch random stream matched every retained checkpoint's state, so the anchors the run trained on are known: 40 distinct anchors over 951 steps.
- From step 0 to 951 the starting-condition (IC) loss fell by a median factor of:
  - 0.00517 on the 7 most-anchored training trajectories;
  - 0.331 on 7 never-anchored ones;
  - 0.274 on 6 validation ones.
- The physics residual changed by 0.369, 0.448 and 0.335 on the same three groups.
- So the starting-condition fit was specific to what the run saw, while the residual change was roughly global.

**JX-4 (did relative progress come with real accuracy?)** Reading: "relative descent without useful accuracy".
- The monitor's front rose from 0 at step 0 to 2 at step 951.
- At step 951 every fixture is still Tier 0:

| Fixture | E at step 0 | E at step 951 |
|---|---|---|
| Single 1632 | 38.8 | 13.5 |
| Single 851 | 58.7 | 19.9 |
| Single 4658 | 76.7 | 29.1 |
| Frozen monitor anchor | 149.0 | 61.7 |

- Energy errors at step 951 were 4.0, 26.5, 9.9 and 53.9 respectively.
- The front measured in physical units stayed at 0 at steps 0, 900 and 951, on the monitor and on every fixture.
- This informs the scale question of JD-3 only.

**JX-5 (where does the derivative scale come from at initialization?)** Reading: recorded (structural evidence only, not a decision input).
- At step 0, on the frozen monitor's trajectory, the network's acceleration has an RMS of 2.899e+05 against a softened gravitational force of 4.410e+01. That is about 6,600 times too large, so the physics residual (RMS 2.899e+05) is almost entirely the network's own curvature.
- The IC position and velocity errors are 0.8234 and 211.3.
- Among the six skip blocks, the largest skip-branch derivative is 206.5 at hidden layer 11 (SIREN branch 110.7).

## Gate G1

Source: `evidence/diag07/g1.json`.
- **Rule.** G1 fires if the physics term's primary share of the Adam update reaches the 1e-2 threshold.
- **Shares.**
  - Step 900: 7.187e-07.
  - Step 951: 2.605e-08.
  - CPU float64 cross-check: 6.94e-07 and 2.59e-08, with the identical outcome.
- **Fires:** false.
- **Outcome:** proceed

For Phase 61 this means proceed: the Phase 61 premise stands, and nothing here asks for it to be re-examined. Phase 59 itself would have been unaffected either way.

## GAP-59-08 (reported, not fixed)

**The finding in plain words.** The production validation gate and the held-out evaluator compute the energy error from finite-difference velocities, on the dataset's coarse output grid. On that grid, Brutus's exact answer already scores 4.7e-2 to 3.8e-1, roughly 5% to 38%. These were measured on training ids 1632, 851 and 4658; with true velocities the same answers score about 1e-14. So, as implemented, no model, not even a perfect one, can pass the 1e-5 exam.

**What it does not change.** Past values were genuinely bad. v2.0's held-out 237.2 and generation 7's validation 15.65 and 50.63 are 40 to 5,000 times above that floor.

**The owner's options, as recorded in the register:**
- **A.** The evaluator and validation gate use the network's autograd velocities, written into §10.6 by a formal clarifying amendment. This is the recommendation recorded there: it measures the network's actual motion, and it matches the v2.4 scorecard.
- **B.** Keep finite differences, on a dense grid. Even at the 0.01 gold cadence the floor is likely still above 1e-5 for the fastest binaries, so B probably remains unpassable.
- **C.** Keep the gate as is, knowing it cannot pass.

**What it blocks.**
- It blocks any spend of the held-out evaluation, and the FEAS-10 pass-bar choice.
- It blocks nothing in v2.4's ladder, which scores with the scorecard's autograd energy error.

**Status.** OPEN and owner-routed. Phase 59 changed nothing about the gate or the evaluator, and the register's GAP-59-08 entry is unchanged since the phase start. See [59-GAPS.md](59-GAPS.md).

## Evidence index

Every file below is hash-checked by its area manifest (`evidence/<area>/MANIFEST.json`), and the top-level `evidence/manifest.json` hashes every evidence file. `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py final` re-derives the audit, census, baselines and survey byte for byte, hash-checks the DIAG-07 results without re-running them, recomputes Gate G1, and checks the scorecard's commit order, the guardrails and this page.

| Area | File | SHA-256 | Checked by |
|---|---|---|---|
| audit | `evidence/audit/reader_acceptance.json` | `11a6cf7bc3342a5ccee5bb30bb85fc94429faeeb1bc9ea58e5ff51e9b12522c0` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py audit --require-committed` |
| census | `evidence/census/census.json` | `cf68e32d2a8b919dd1536a363aee2c6865b2841026263a3130e6edf8466dd034` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py census --require-committed` |
| census | `evidence/census/census.csv` | `f73c91b3803ff62606c8a4e97eeb76b6a461a5e0fff286e8d31f8627e321a175` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py census --require-committed` |
| census | `evidence/census/panels.json` | `56ad5185148fca7e72b21f4fc1dbaaaf8eea7aa9ecdf498653af98ad88d6aa92` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py census --require-committed` |
| baselines | `evidence/baselines/baselines.json` | `3d7b7a687091cf9b1b0d803849c227990e1d45aa82888bd3e91980e62fc92d9e` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py baselines --require-committed` |
| baselines | `evidence/baselines/two_kepler.json` | `05a347a65e01ea6a9cde1c6cff4b53d0d17333db9c3672a460931e2323b4c80e` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py baselines --require-committed` |
| baselines | `evidence/baselines/two_kepler_population.csv` | `4995d65a042993764ccf4f44a98807b8b42690674e5c8108a9809bf59a23b59a` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py baselines --require-committed` |
| baselines | `evidence/baselines/nn_copy.json` | `4334fc04c91cd5c8521f1d2805ac30f2a92fd498e6d3f5c9d6dad0ca22956deb` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py baselines --require-committed` |
| survey | `evidence/survey/survey.json` | `0e3295edff60c8e09c8e629b4b2a2d63a7e62d66d405e4c08db805120fa720a1` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py survey --require-committed` |
| survey | `evidence/survey/survey_records.csv` | `88bb2cb6d4cb915e631a0b39ac371d2d7c273e8f41526b4ccdb85cb696f015d0` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py survey --require-committed` |
| survey | `evidence/survey/picks.json` | `b6836d5095edc12b9b7af873bfd5b6cb82fdeeb2e5c34e1c75b608810cda7317` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py survey --require-committed` |
| diag07 | `evidence/diag07/jx10.json` | `1b895e8ae7415cf433f9d4e0e2b385ee8d4a61af417b9a191742e9447e9139c9` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py diag07 --require all --require-committed` |
| diag07 | `evidence/diag07/jx01.json` | `7b8fff8042e629096407d4d805ba39ffc16782d816fc8627acb5e3c2ec45af35` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py diag07 --require all --require-committed` |
| diag07 | `evidence/diag07/g1.json` | `3c94131ca4f205dedbe3a7d49b41251af27712cdf4da2af42890f4f24245b5e8` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py diag07 --require all --require-committed` |
| diag07 | `evidence/diag07/jx02.json` | `1853be8936a15b2bc9400f4c69b9746c59708032464a159fff9080c38e70c903` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py diag07 --require all --require-committed` |
| diag07 | `evidence/diag07/jx03.json` | `ec529371210d866c64cf38c4d6e496f7f33872d36c9382609510acee66059278` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py diag07 --require all --require-committed` |
| diag07 | `evidence/diag07/jx04.json` | `c3baae248567742ebddceaafe778652be38090af478bd06bdebe72d6d027ebec` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py diag07 --require all --require-committed` |
| diag07 | `evidence/diag07/jx05.json` | `c74ab3cb494d92ef17138d3880a3830f1cd8ea2544630fbe6df7437ec2dca343` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py diag07 --require all --require-committed` |
| scorecard | `evidence/scorecard-freeze.json` | `820b64b9986c116a5ed7f843854ce5f2f826aa6b560d2dfba24fb2e5fcac4042` | `python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py scorecard-frozen` |
