# Phase 65 Findings: the probe on the record, and what a minute-scale fit costs

**Status.** Phase 65's two requirements are executed on the record. DIAG-09's
registered reproduction returned **`retained`** (every required historical
figure reproduced), and INST-08's harness is built, tested and proven by one
registered real fit. This page states what is now known, what the measured
cost is and on what basis, and the limitations retained at closeout. Every claim cites
committed evidence. Nothing here amends the roadmap, the framework specs, the
frozen scorecard or any owner pass bar.

**Closeout, 2026-10-31.** Phase 65 is complete under the owner's technical
delegation. The two reporting reviews are approved, the probe registration
is preserved as historical, and its runner defects have explicit dispositions
and reuse conditions in `65-CLOSEOUT.md`. The full suite now passes 204 tests.
The original predictions and evidence are unchanged.

## 1. The reproduction branch (DIAG-09): `retained`, association only

One registered read-only run of the seven-arm probe (plan 65-05, run commit
`22cee7d241f1` under registration `f469e003`) reproduced **all 144 required
historical fields exactly — 0 not_reproduced, 0 provenance limitations**
(`evidence/probe/reproduction.json`, verified by `verify-result`
(`VERIFY-RESULT-OK`, exit 0) and re-verified after this plan's edits; 64
preserved-only fields reported verbatim; 130 raw per-layer new-measurement
entries). The registered branch is **on-record (`retained`)**: the 2026-10-27
exploratory association — at the CPU64 seed-42 reconstruction, near-perfect
adjacent-time hidden-state correlation at initialization collapsing to
formatter-zero deep in every trained network, output movement collapsing to
~0.3% of the orbit's variation, the labelled rate comparator rising by
orders of magnitude — is now a reproduction of already-seen results, not an
independent discovery (D-02), and it **is not** information loss, a capacity
limit or the cause of the v2.4 failure (D-07). Those questions belong to
Phases 66–67 and 69. No SCOPE-49 pivot is proposed; the withdrawal branch was
never taken.

Provenance limitations: **none.** Every registered available historical
numeric field had its original source output.

## 2. Real-arm logger parity (INST-08(c))

The fit logger's DIAG-09 value is the probe's value by construction and by
receipt: the registered run's actual `diagnostic_fit.log_similarity` call on
the r1-1632 polish state (same admission/hash/data gates, same weights and
coordinates, CPU64, no updates) is materialized at
`evidence/probe/logger-parity.json`, byte-faithful to its publication commit,
and `verify-result` cross-checked it against the run's recorded entry with
exact agreement on all 13 measured layers. The smoke's admission required this
committed, successful receipt before its own training trace (D-10).

## 3. The registered smoke (INST-08(e)): mechanics complete

One registered attempt (plan 65-06; registration `ac4358cb` as re-pinned by
`b1dcacc4`, bytes `ba54e8124a33…`) ran the locked-12 variant on the Stage-0
training gold record of system 1632 and completed mechanically
(`evidence/fit/1632-smoke/record.json`, `status: complete`, verified
`VERIFY-RESULT-OK`, exit 0):

- **Variant/settings:** `locked-12` — 12 hidden layers × 256, raw `[tau,
  IC13]`, locked frequencies (30.0 / 1.0), constant-rate Adam at 1e-4 with
  the trainer's `OptConfig` betas/epsilon, no scheduler, clipping, physics
  term or polish; seed 42; **MPS float32**; physical window [0, 10];
  orbit `hierarchical/gold/1632`, split `train`, manifest stage 0, 1,001
  samples.
- **Steps:** exactly 20 finite updates — 2 warmup + 18 measured — within the
  registered 600-second whole-run cap (the whole supervised run took ~5 s).
- **Similarity trace** (shared `measure_time_signal`, cadence 0/5/10/15/20;
  first-layer frequency median in cycles, movement = centred output norm /
  centred gold norm, rate = the labelled autograd/gold-finite-difference
  comparator, both in normalized tau — D-05's labels):

  | step | freq median | movement | rate | h1 | h12 |
  |---|---|---|---|---|---|
  | 0 (init) | 0.325 | 2.7877 | 1.03e+02 | 1.0000 | 0.9225 |
  | 5 | 0.322 | 2.7542 | 1.02e+02 | 1.0000 | 0.9210 |
  | 10 | 0.322 | 2.7619 | 1.05e+02 | 1.0000 | 0.9192 |
  | 15 | 0.321 | 2.7215 | 1.02e+02 | 1.0000 | 0.9201 |
  | 20 | 0.320 | 2.4039 | 9.44e+01 | 1.0000 | 0.9225 |

  Reported as measured values, with no interpretation: 20 steps at 1e-4 is a
  mechanics check, not a training experiment.
- **Physical scores and comparators** (frozen FEAS-01 scorer and
  `score_trajectory`, identical times/masses/body order, gold grid, autograd
  velocities): network **E 24.80, tier 0** (`eps_h` 14.49); window-mean
  constant predictor **E 1.1538, tier 0**; two-Kepler **E 0.9168, tier 0**
  (the frozen Newton solver converged on this orbit). Loss (context only):
  final 0.0405. These are context for the mechanics, not a verdict: the run
  imposes no E/tier threshold, and a 20-step fit at 1e-4 is not an
  optimization attempt.
- **Access and isolation:** exactly one corpus open
  (`hierarchical/gold/1632/train/stage0`), zero validation or test opens,
  the process open attestation clean, all 33 pinned source digests matching
  the committed modules, and the weights published only inside the
  intrinsically marked `inst08-diagnostic-weights/v1` payload
  (`diagnostic.weights`). The synthetic suites prove the relocated
  production-entry refusals (`tests/phase65/test_isolation.py`,
  `tests/phase65/test_contracts.py`); the preserved held-out evaluation
  stays unspent.

## 4. The measured cost, and its exact basis

**Seconds per measured optimizer step: 0.014265 s** (record:
`timing.seconds_per_step`). The basis, so a budget for **this exact
configuration** (locked-12, MPS float32, seed 42, the full 1,001-sample
[0, 10] window of `hierarchical/gold/1632`, constant-rate Adam 1e-4, no
scheduler/clipping/physics/polish) can be computed from a chosen duration:

- numerator: the sum of the 18 measured synchronized update durations,
  0.25678 s — each segment wrapped in the MPS `_synchronize` helper before
  and after, so queued device work is attributed to the step that queued it;
- denominator: the 18 measured updates only. Warmup (2 updates, 0.13147 s),
  similarity logging (0.57212 s over five calls), frozen scoring
  (1.21599 s), setup (0.52892 s), data load (0.25356 s) and publication
  (0.01508 s) are excluded from the numerator and recorded in the record;
- the different label: end-to-end **0.13597 s per completed step** (whole
  fit-body wall 2.7194 s ÷ 20), for whole-run budgeting that must include
  scoring and logging;
- synchronization overhead is recorded (0.000120 s over 42 calls) and the
  sample is **18 steps — not steady-state throughput**. A budget for this
  configuration is `duration_seconds ÷ 0.014265` steps plus the fixed
  logging/scoring/data segments above, scaled by their own cadence.

**Do not extrapolate:** this rate says nothing about other depths, widths,
time features, learning rates, precisions, devices or window lengths, and it
selects no Phase 66–67 experiment. Longer diagnostics remain **refused** at
or above a one-hour whole-run cap until governed pause/resume and
power-compatibility is demonstrated (the smoke's cap refuses 3600 s before
data access), and Phase 60's wrappers are not claimed compatible — D-11
records that their compatibility is unverified.

## 5. Reporting reviews resolved under delegated authority

Codex approved both scientific-reporting constraints on 2026-10-31 under
D-01 and the owner's explicit closeout delegation, supported by independent
reviews. This is a prose judgment, not an assertion that a deterministic test
can decide scientific interpretation, or that the owner personally reviewed it.

The smoke remains a mechanics check with exact-configuration timing only.
The reproduced probe remains an association without discovery, information-loss,
capacity-limit or causal claims. `65-UAT.md` records both passes;
`65-CLOSEOUT.md` records their rationale. The original pre-run prediction
pages remain unchanged.

## 6. The energy-metric limitation, carried explicitly (GAP-59-08)

The frozen FEAS-01 scorer reports `E`/`eps_h` with autograd velocities on the
gold grid. The metric family's known limitation stays open: GAP-59-08
(`.planning/phases/59-read-only-baseline-scorecard/59-GAPS.md`,
OWNER-ROUTED) records that the production validation gate and held-out
evaluator compute `eps_h` from finite-difference velocities on the coarse
output grid, where even the exact Brutus answer scores 5–38%, so that route
could never certify the `1e-5` bar. This smoke **does not adjudicate**
GAP-59-08: it reports the frozen scorer's output as-is, changes no metric,
and leaves the velocity-source and pass-bar decisions to Phase 68. The smoke's
`eps_h` 14.49 is the frozen autograd-route value on the gold grid and is not
comparable to the finite-difference production figures without Phase 68's
adjudication.

## 7. Closeout decisions and retained limitations

- Preserve `evidence/probe/expectations.json` unchanged. Its result binds its
  exact hash and the code at the recorded run commit. The planned 65-06 edits
  changed two dependencies, `diagnostic_fit.py` and `diagnostic_guard.py`.
  Historical result verification passes; live admission correctly refuses.
  The content test now checks historical dependency bytes, registration
  identity and ancestry, while preserved-source/frozen/arm checks remain live.
  No production gate was relaxed. A future probe needs a new registration.
- Accept the probe's stdout-renderer failure and empty redundant summary as
  historical defects. All 130 new measurements remain in the top-level JSON;
  the regenerated stdout retains its provenance label. The actual logger
  receipt plus `verify-result --logger-parity` satisfies INST-08(c), despite
  the missing standalone command. Repair the renderer and summary, add
  regression tests and register the changed code before any new probe run.
- `65-CLOSEOUT.md` dispositions every warning and info item in `65-REVIEW.md`.
  WR-01's list-nested-marker limitation is live and requires repair and
  production-entry regression tests before any graded run or held-out
  evaluation. This is separate from accepting historical probe defects.
- Longer diagnostics remain refused at an hour or more until governed
  pause/resume/power compatibility is proven. No Phase 60 wrapper compatibility
  is asserted. GAP-59-08 remains open for Phase 68.
- No learnability, causal, representation or experiment-selection conclusion
  follows from these records. Phases 66-67 need their own pre-run predictions
  and registrations; yardstick and redesign decisions remain in Phases 68-69.

## 8. Evidence index

| Claim | Committed evidence |
|---|---|
| Reproduction `retained`, 144/144, 0 limitations | `evidence/probe/reproduction.json` (`7a943da5`), `65-PROBE-RESULT.md` (`484ea30c`) |
| Logger parity (INST-08c) | `evidence/probe/logger-parity.json` (`484ea30c`); `verify-result` exit 0 re-run this plan |
| Smoke settings frozen before the run | `65-SMOKE-PREDICTION.md` + `evidence/fit/smoke-registration.json` (`ac4358cb`, re-pinned `b1dcacc4`) |
| The registered smoke run | `evidence/fit/1632-smoke/record.json`, `diagnostic.weights`, `attempt.json` (`84128fe2`), record sha256 `f6faee77d527…` |
| Harness tests (TDD, 131 gate tests; 204/204 closeout discovery) | `f7007b5e` (RED), `59647328` (GREEN), `b1dcacc4` (receipt-check fix); historical dependency-test correction and fresh closeout checks in `65-CLOSEOUT.md` |
| 33 frozen source digests unchanged | `load_protocol()` revalidation, `PROTOCOL-OK`; `record.json#source_sha256` == committed modules |

*Phase: 65-probe-on-the-record-fit-harness · Written 2026-10-29 by
gsd-executor-65-06 (plan 65-06).*
