# Phase 65 Smoke Prediction: the registered 20-step system-1632 fit

**Registered before the first real optimizer step** (D-02 discipline applied to
the fit harness; SCOPE-47's lightweight pre-registration). This page and
`evidence/fit/smoke-registration.json` are committed together and the run
admits only their committed-clean bytes. The registration pins the final
current fit implementation's bytes, the committed logger-parity receipt from
the probe run, the frozen scorer/scorecard and statistics evidence, and the
sealed 33-module run protocol.

## What this run is

One registered, bounded diagnostic fit of the locked-12 variant on the
Stage-0 training gold record of system 1632, on MPS float32, seed 42:

- variant `locked-12` — 12 hidden layers of width 256, raw `[tau, IC13]`
  inputs, locked first/hidden frequencies, constant Adam rate 1e-4 with the
  trainer's `OptConfig` betas and epsilon, no scheduler, no clipping, no
  physics objective, no polish;
- orbit `hierarchical/gold/1632`, split `train`, manifest stage 0 — the only
  record the guarded Stage-0 seam may open;
- physical window [0, 10], 1,001 retained samples;
- exactly 20 optimizer updates, the first 2 warmup and the remaining 18 the
  optimizer-rate measurement;
- similarity logged at steps 0, 5, 10, 15 and 20 only, by the one shared
  `measure_time_signal` implementation (D-05);
- a 600-second whole-run cap covering admission, data load, setup, updates,
  logging, scoring and publication, enforced by a supervised worker with
  graceful termination as well as by deadline checks between phases and
  updates;
- scoring by the frozen FEAS-01 `score_network`, beside the window-mean
  constant predictor and the two-Kepler comparison through the frozen
  `score_trajectory` on identical times, masses and body order;
- one exclusive attempt: repeated or parallel attempts refuse; an
  interruption, a non-finite update or a cap expiry leaves the attempt
  explicitly incomplete and publishes nothing; no failure retries, extends
  or resumes.

## Mechanical acceptance rule (the only rule)

The run **passes mechanically** if and only if the record shows:

1. `steps.completed == 20` with every update finite (a non-finite loss or
   gradient refuses before its update);
2. exactly five similarity entries, at steps 0, 5, 10, 15 and 20;
3. the frozen network score present with physical metrics and tier, and both
   comparison rows present on the same window (the two-Kepler row may record
   the frozen solver's own non-convergence as a non-applicable row — that is
   a recorded outcome, not a run failure);
4. access evidence showing Stage-0 TRAIN-only reads, zero validation or test
   opens, and the process open attestation;
5. all 20 updates and the scoring completed within the 600-second cap;
6. the intrinsically marked `inst08-diagnostic` record and weights payload
   published exclusively, with the 33 pinned source digests matching the
   committed modules.

**No E value, tier, similarity figure or improvement is predicted or
required.** A record with every mechanical box ticked is a pass regardless of
the numbers; a record failing any mechanical box is incomplete and is not a
result.

## Incomplete and error branches

- **Incomplete:** the attempt file records status `incomplete` with the
  reason (deadline expiry, interruption, non-finite update, admission
  refusal after the claim). The record is never written. The attempt is not
  retried by the tooling; any further attempt is a new decision.
- **Admission refusal:** a missing, untracked, staged-only or dirty
  registration or code dependency, a cap at or above 3600 seconds, missing
  MPS, or a receipt problem refuses before the claim and before any data
  access; nothing is created.
- **Out-of-branch outcome:** any outcome this page does not describe (a
  refusal the admission did not name, an output shape this page does not
  define) is reported to the orchestrator rather than interpreted here.

## What this run is not

The smoke demonstrates that the harness operates and what its work costs. It
supplies **no learnability verdict, no causal confirmation, no representation
claim** and selects no Phase 66-67 experiment (D-11). Its seconds-per-step
figure is 18 steps of this exact configuration on this Mac — a budget input,
not steady-state throughput for other depths, rates, time features or
devices. The historical reproduction branch of the probe (retained, plan
65-05) is recorded in the registration and is not a precondition of this run.
The two bespoke scientific-reporting prohibitions attached to D-11's
reporting intent remain flagged for review, not adjudicated here.
