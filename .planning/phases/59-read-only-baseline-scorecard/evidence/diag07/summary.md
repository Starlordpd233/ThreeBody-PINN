## In plain language

JX-1 measured how strongly each part of the loss pushed generation 7's network and what share of the actual Adam update the physics term received: at step 900 the physics term supplied 7.187e-07 of the Adam-preconditioned update direction (supports: physics was a passenger (PC-2)); at step 951 the physics term supplied 2.605e-08 of the Adam-preconditioned update direction (supports: physics was a passenger (PC-2)). At step 0 no Adam moments are stored, so no share is computable there. A share of 1e-4 or less reads as physics being a passenger, and 1e-2 or more reads that claim as overstated.

JX-2 asked whether the run's progress monitor moved between steps 900 and 951 by more than its own sampling noise. On the monitor's own trajectory, the prefix through bin 2 changed by 1.552e-01, while 20 fresh draws of collocation times spread it over 1.717e-01 at step 900 and 1.406e-01 at step 951. Reading: estimator noise not excluded.

JX-3 asked whether generation 7 improved everywhere or only on the trajectories it kept anchoring on. The replay of the run's batch random stream matched every retained checkpoint's state, so the anchors are known: 40 distinct anchors over 951 steps. From step 0 to step 951 the IC loss changed by a median factor of 0.00517 on the 7 most-anchored training trajectories, 0.331 on 7 never-anchored ones and 0.274 on 6 validation ones; the residual sum changed by 0.369, 0.448 and 0.335. Reading: mixed: exposure-specific / global.

JX-4 compared the run's own relative progress signal with real orbit accuracy. The monitor's front moved from 0 at step 0 to 2 at step 951. At step 951 the fixtures score: panel_single_p10 tier 0, panel_single_p50 tier 0, panel_single_p90 tier 0, frozen_monitor_anchor tier 0. Reading: relative descent without useful accuracy. It informs the scale question of JD-3 only (R-2).

JX-5 recorded, at initialization and on the frozen monitor's trajectory, how large each quantity in the physics residual is. The network's acceleration a' has an RMS of 2.899e+05 against a softened force of 4.410e+01, so the residual's RMS is 2.899e+05. The IC position and velocity errors are 8.234e-01 and 2.113e+02. Among the six skip blocks, the largest du-derivative of the skip branch is 2.065e+02 at hidden layer 11 (SIREN branch 1.107e+02). This is structural evidence only and is not a decision input (R-2).

The frozen monitor reproduces the recorded Phase 58 values, and the smoke front is 0 at steps 100, 200 and 300. That reading supports C-F14 and F-H2b.

Gate G1 did not fire. The physics term supplied 7.187e-07 at step 900 and 2.605e-08 at step 951 of the Adam update, below the 0.01 threshold at both checkpoints. Outcome: proceed.

## Readings

| Experiment | Reading outcome | Checkpoints |
| --- | --- | --- |
| JX-1 | 900: supports: physics was a passenger (PC-2); 951: supports: physics was a passenger (PC-2) | stage-0-init.pt, best.pt, step-000951.pt |
| JX-2 | estimator noise not excluded | stage-0-init.pt, best.pt, step-000931.pt, step-000941.pt, step-000951.pt |
| JX-3 | mixed: exposure-specific / global | stage-0-init.pt, step-000951.pt |
| JX-4 | relative descent without useful accuracy | stage-0-init.pt, best.pt, step-000951.pt |
| JX-5 | recorded | stage-0-init.pt |
| JX-10 | supports | stage-0-init.pt, best.pt, step-000931.pt, step-000941.pt, step-000951.pt, step-000100.pt, step-000200.pt, step-000300.pt |
| G1 | proceed | 900, 951 |
