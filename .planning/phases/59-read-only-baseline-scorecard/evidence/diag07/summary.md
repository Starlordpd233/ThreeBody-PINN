## In plain language

JX-1 measured how strongly each part of the loss pushed generation 7's network and what share of the actual Adam update the physics term received: at step 900 the physics term supplied 7.187e-07 of the Adam-preconditioned update direction (supports: physics was a passenger (PC-2)); at step 951 the physics term supplied 2.605e-08 of the Adam-preconditioned update direction (supports: physics was a passenger (PC-2)). At step 0 no Adam moments are stored, so no share is computable there. A share of 1e-4 or less reads as physics being a passenger, and 1e-2 or more reads that claim as overstated.

The frozen monitor reproduces the recorded Phase 58 values, and the smoke front is 0 at steps 100, 200 and 300. That reading supports C-F14 and F-H2b.

Gate G1 did not fire. The physics term supplied 7.187e-07 at step 900 and 2.605e-08 at step 951 of the Adam update, below the 0.01 threshold at both checkpoints. Outcome: proceed.

## Readings

| Experiment | Reading outcome | Checkpoints |
| --- | --- | --- |
| JX-1 | 900: supports: physics was a passenger (PC-2); 951: supports: physics was a passenger (PC-2) | stage-0-init.pt, best.pt, step-000951.pt |
| JX-10 | supports | stage-0-init.pt, best.pt, step-000931.pt, step-000941.pt, step-000951.pt, step-000100.pt, step-000200.pt, step-000300.pt |
| G1 | proceed | 900, 951 |
