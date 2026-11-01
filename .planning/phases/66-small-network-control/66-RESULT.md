# Phase 66 Result: EXP-01 read against the pre-registered rule

**Committed after the three runs and before owner checkpoint ①.** Every label,
the confirmation, the route and every number on this page comes from the output
of `pinn.verification.diagnostic_phase66` (`read-run` per run directory, one
`review` over the three, and `check-run` on the timing directory) over the
committed run directories; no number is re-derived by hand. Each run's numbers
cite its committed record by path and SHA-256, and the evidence index at the
end lists every cited file's digest. Loss is shown as context only.

## In plain language

1. We trained one small network — one hidden layer of 384 units, 157,065
   parameters, about one-fifth of the locked network's 795,657 — to reproduce
   orbit 1632 from its initial state and time alone (a data-only fit of
   position against time), and scored the result with the frozen FEAS-01
   scorecard; a *tier* is the scorecard's grade for a prediction, and Tier 1
   is the lowest passing grade, which needs *E* — the worst position error
   over the [0, 10] window as a fraction of the system's size — to be at most
   0.1.
2. All three runs ended at Tier 1: E of 0.011431234453278821 on the main run
   (1632, seed 42), 0.01720558902801923 on the second-system repeat (851,
   seed 42) and 0.07898485527313073 on the second-seed repeat (1632, seed 41),
   each far below the 0.1 line (66-PREDICTION.md section 4; E <= 0.1,
   inclusive).
3. The pre-registered reading for this label: a network one-fifth the size,
   with one hidden layer, fits the orbit, so size is not what stopped v2.4;
   the data and scoring path can produce a passing fit.
4. The result repeated on the second system and the second seed, so the branch
   is *confirmed* — the rule confirms only when all three runs share `tier1`
   or share `near` (66-PREDICTION.md section 5).
5. For scale: the *constant predictor* — the baseline that returns each body's
   average position over the window and nothing that moves — scores E
   1.1538408194255343 on 1632 and 1.233696866477104 on 851 (each record's own
   `window_mean_constant` row), and the *two-Kepler formula* — a no-learning
   baseline that places each body on the two-body orbit implied by its initial
   state — scores 0.9168487091299374 on 1632 and 0.4312597209593449 on 851
   (each record's own `two_kepler` row); the trained networks beat both by a
   wide margin.
6. The evidence beside the grade: *neighbour similarity* — how alike a layer's
   response and its neighbour's response to the same inputs remain, measured
   as the mean cosine between adjacent units' activity — stayed near 0.99
   throughout, while *output movement* — how much the network's output moves
   over time, as a fraction of how much the real orbit moves about its mean —
   reached about 1.0 and was no longer growing when the steps ran out
   (improvement check, section Numbers): the output genuinely moves with time
   rather than sitting near the average position.
7. What is proposed: the pre-registered route for this branch is
   `phase67-as-planned` — no plan change is proposed; Phase 67's ladders run
   as planned once the owner answers checkpoint ① (SCOPE-49 keeps Phases 67
   to 69 provisional until this review, and the owner decides plan changes).
8. What it does not say: it does not say the pipeline is fully sound and it
   locates no fault — it is one orbit on each of two systems, the probe's
   depth-linked lead remains an association, and nothing graded ran (the
   held-out evaluation is unspent).

## Branch taken

The review invocation (once, from the trainex root, the plan 66-05 command):

```
<home>/miniforge3/envs/pinn-train/bin/python -B -m pinn.verification.diagnostic_phase66 review --main .planning/phases/66-small-network-control/evidence/exp01/main-1632-s42 --repeat-system .planning/phases/66-small-network-control/evidence/exp01/repeat-851-s42 --repeat-seed .planning/phases/66-small-network-control/evidence/exp01/repeat-1632-s41
```

The near-band edges are 0.95 x E_const and 1.05 x E_const computed from each
record's own E_const (`near_band: 0.05` in the frozen design block); E_const
is the record's own `comparisons[window_mean_constant].score.E`, never a
hand-typed constant. `e_band` is the review's classify verdict on E alone;
`branch` is the final label under the improvement check. No run carried a
mechanical or setting problem (`mechanical_problems` and `setting_problems`
empty on all three read-run outputs).

| Role | Orbit | Seed | E | E_const (the record's own) | Near band from that E_const | Tier | E-only band (e_band) | still_improving | Final label (branch) |
|---|---|---|---|---|---|---|---|---|---|
| main | hierarchical/gold/1632 | 42 | 0.011431234453278821 | 1.1538408194255343 | 1.0961487784542576 to 1.211532860396811 | 1 | tier1 | false | tier1 |
| repeat-system | hierarchical/gold/851 | 42 | 0.01720558902801923 | 1.233696866477104 | 1.1720120231532487 to 1.2953817098009592 | 1 | tier1 | false | tier1 |
| repeat-seed | hierarchical/gold/1632 | 41 | 0.07898485527313073 | 1.1538408194255343 | 1.0961487784542576 to 1.211532860396811 | 1 | tier1 | false | tier1 |

confirmation: confirmed
route: phase67-as-planned

(the review's printed line: `EXP01-REVIEW confirmation=confirmed route=phase67-as-planned`)

## Numbers

Per run, the fields of the record readout (66-PREDICTION.md "Record readout"),
copied from the `read-run` output over each committed directory. Each run's
record: `.planning/phases/66-small-network-control/evidence/exp01/<dir>/record.json`,
SHA-256 given in the run's heading and in the evidence index. Loss is context
only (D-10).

### main — orbit hierarchical/gold/1632, seed 42 (record sha256 774a5a451bda97c79e39e3e10d146bcde8a5a5551b19a0d3cf59022b4b301007)

- tier 1; E 0.011431234453278821; eps_h 0.23059668730403904.
- E_const 1.1538408194255343 (the record's own window-mean constant row);
  two-Kepler E 0.9168487091299374 (the record's own two_kepler row).
- Output movement at the final entry (step 465000): 0.9999971356891447.
  Improvement check: reference step 343333, reference output movement
  0.9997545117108192; final output movement 0.9999971356891447; growth
  0.00024262397832552907; threshold (min_growth) 0.01; still_improving false.
- Neighbour similarity, adjacent_cosine_mean at the registered cadence
  (input row from the record's `similarity.entries`; h1 row from the
  read-run output):

  | Step | input | h1 |
  |---|---|---|
  | 0 | 0.9964733123779297 | 0.9904256463050842 |
  | 100 | 0.9964532256126404 | 0.9903262853622437 |
  | 300 | 0.9964550733566284 | 0.9903621673583984 |
  | 1000 | 0.9964566826820374 | 0.9904374480247498 |
  | 3000 | 0.9964487552642822 | 0.9904808402061462 |
  | 10000 | 0.9964869618415833 | 0.9905203580856323 |
  | 30000 | 0.9964647889137268 | 0.9905785918235779 |
  | 100000 | 0.9960978031158447 | 0.9904708862304688 |
  | 160833 | 0.9957742691040039 | 0.9905353784561157 |
  | 221666 | 0.9954429864883423 | 0.9896153211593628 |
  | 282500 | 0.9951443076133728 | 0.9886237978935242 |
  | 343333 | 0.9949041604995728 | 0.9886840581893921 |
  | 404166 | 0.9946206212043762 | 0.9877328872680664 |
  | 465000 | 0.9943618178367615 | 0.9867252111434937 |

- First-layer frequency (cycles per window): step 0 median
  11.41991901397705, max 22.732187271118164; final entry (step 465000)
  median 11.99764633178711, max 39.93656539916992. The step-0 max sits
  inside the registered bandwidth check [0.95 B, 1.00001 B] with
  B = 22.736420441699334 (read-run reported no setting problem).
- Loss, context only: final loss 6.056427359624195e-09. The recorded loss
  trace holds 9894 entries at the registered stride 47; the entry at three
  quarters of the trace (index 7419) is 5.684837489638994e-09, so the change
  over the last quarter of the recorded trace is +3.715898699852005e-10
  (final minus that entry; context only, not a score).
- Completed steps 465000 (200 warmup, 464800 measured); seconds_per_step
  0.004202254948933541; wall time 1957 s (attempt started_utc
  2026-11-01T18:12:51+00:00, ended_utc 2026-11-01T18:45:28+00:00).

### repeat-system — orbit hierarchical/gold/851, seed 42 (record sha256 9166311284ea857ea835813ea74b5ea6a30323d0cb4036341b722dcf56add05b)

- tier 1; E 0.01720558902801923; eps_h 0.3529082508657166.
- E_const 1.233696866477104 (the record's own window-mean constant row);
  two-Kepler E 0.4312597209593449 (the record's own two_kepler row).
- Output movement at the final entry (step 465000): 1.000002590770897.
  Improvement check: reference step 343333, reference output movement
  0.9998582992251148; final output movement 1.000002590770897; growth
  0.0001442915457821048; threshold (min_growth) 0.01; still_improving false.
- Neighbour similarity, adjacent_cosine_mean at the registered cadence:

  | Step | input | h1 |
  |---|---|---|
  | 0 | 0.9964644908905029 | 0.9903100728988647 |
  | 100 | 0.9964316487312317 | 0.9902673959732056 |
  | 300 | 0.9964350461959839 | 0.9902997016906738 |
  | 1000 | 0.9964433908462524 | 0.9903730154037476 |
  | 3000 | 0.9964465498924255 | 0.9904448390007019 |
  | 10000 | 0.9964698553085327 | 0.9905937910079956 |
  | 30000 | 0.9964865446090698 | 0.9906818270683289 |
  | 100000 | 0.9959797859191895 | 0.9905427098274231 |
  | 160833 | 0.995553195476532 | 0.989930272102356 |
  | 221666 | 0.9951211214065552 | 0.9895293712615967 |
  | 282500 | 0.9945107698440552 | 0.9872108697891235 |
  | 343333 | 0.9940727353096008 | 0.986176609992981 |
  | 404166 | 0.9937701225280762 | 0.9849913120269775 |
  | 465000 | 0.9934597015380859 | 0.9851512312889099 |

- First-layer frequency (cycles per window): step 0 median
  11.41991901397705, max 22.732187271118164; final entry (step 465000)
  median 13.307440757751465, max 49.98491287231445. The step-0 max sits
  inside the registered bandwidth check (read-run reported no setting
  problem).
- Loss, context only: final loss 5.212864806480866e-09. The recorded loss
  trace holds 9894 entries at the registered stride 47; the entry at three
  quarters of the trace (index 7419) is 1.1520136844467288e-08, so the
  change over the last quarter of the recorded trace is -6.307272037986422e-09
  (final minus that entry; context only, not a score).
- Completed steps 465000 (200 warmup, 464800 measured); seconds_per_step
  0.003724428295332197; wall time 1734 s (attempt started_utc
  2026-11-01T18:51:17+00:00, ended_utc 2026-11-01T19:20:11+00:00).

### repeat-seed — orbit hierarchical/gold/1632, seed 41 (record sha256 4146675b56990ca145fa9db777f7922476b1d64ab4cf8f708acb1acec2137c2a)

- tier 1; E 0.07898485527313073; eps_h 0.4403488467986121.
- E_const 1.1538408194255343 (the record's own window-mean constant row);
  two-Kepler E 0.9168487091299374 (the record's own two_kepler row).
- Output movement at the final entry (step 465000): 0.9994221674071753.
  Improvement check: reference step 343333, reference output movement
  0.9999716096247584; final output movement 0.9994221674071753; growth
  -0.0005494422175831293; threshold (min_growth) 0.01; still_improving
  false.
- Neighbour similarity, adjacent_cosine_mean at the registered cadence:

  | Step | input | h1 |
  |---|---|---|
  | 0 | 0.9965821504592896 | 0.9906841516494751 |
  | 100 | 0.996577262878418 | 0.9906193614006042 |
  | 300 | 0.9965808987617493 | 0.9906479716300964 |
  | 1000 | 0.9965846538543701 | 0.9907295107841492 |
  | 3000 | 0.9965834021568298 | 0.9908110499382019 |
  | 10000 | 0.9965659379959106 | 0.9907703995704651 |
  | 30000 | 0.9966127872467041 | 0.9908838868141174 |
  | 100000 | 0.9961008429527283 | 0.9909906387329102 |
  | 160833 | 0.9957289099693298 | 0.9901160001754761 |
  | 221666 | 0.995296835899353 | 0.9891172051429749 |
  | 282500 | 0.9950850009918213 | 0.9891534447669983 |
  | 343333 | 0.9947737455368042 | 0.9885631799697876 |
  | 404166 | 0.9945456385612488 | 0.9873615503311157 |
  | 465000 | 0.9940922856330872 | 0.9867066144943237 |

- First-layer frequency (cycles per window): step 0 median
  11.317618370056152, max 22.64010238647461; final entry (step 465000)
  median 12.232267379760742, max 48.901611328125. The step-0 max sits inside
  the registered bandwidth check (read-run reported no setting problem).
- Loss, context only: final loss 8.372545039492252e-07. The recorded loss
  trace holds 9894 entries at the registered stride 47; the entry at three
  quarters of the trace (index 7419) is 7.401766310977109e-09, so the change
  over the last quarter of the recorded trace is +8.298527376382481e-07
  (final minus that entry; context only, not a score).
- Completed steps 465000 (200 warmup, 464800 measured); seconds_per_step
  0.004365704157405605; wall time 2034 s (attempt started_utc
  2026-11-01T19:30:40+00:00, ended_utc 2026-11-01T20:04:34+00:00).

The GAP-59-08 sentence, which applies to every eps_h figure above, verbatim:
eps_h here is the frozen scorer's autograd-velocity value on the gold grid; it is not the production gate's finite-difference value, GAP-59-08 (owner-routed, Phase 68) is open, and eps_h does not measure correctness for a near-constant predictor.

## SCOPE-49 proposal

The route is `phase67-as-planned`, so **no plan change is proposed**. "Too
small" is refuted for one orbit, and Phase 67 runs as planned once the owner
answers checkpoint ①. Phases 67 to 69 are provisional until this review
(SCOPE-49); the owner decides any plan change, and checkpoint ① asks only
whether to accept this recorded proposal (here: proceed unchanged), direct a
different plan change, or hold.

What this blocks and what it does not: proceeding-as-planned blocks nothing.
Under D-12 a proposal blocks only the work that depends on it, and Phase 68
(the yardstick) does not depend on the experiments; the held-out evaluation
stays unspent either way. If the owner instead directs a change under
SCOPE-49 (an inserted phase, a dropped phase, re-aimed later phases, or a new
requirement), that change is recorded at the checkpoint and set up by a
separate step after this phase.

## What this result does not say

- It does not settle the identifiability limit: failure was predicted by both
  "too small" and a pipeline defect, so EXP-01 can refute "too small" but
  cannot confirm the pipeline is sound (66-PREDICTION.md section 3). A Tier 1
  result shows the data-to-scorer path can produce a passing fit for this
  network on this orbit; it does not locate any fault, and none is claimed.
- A near result would not have located the fault either, and an unsettled
  result supports no suspect until it settles; no run took either label here,
  and these limits are stated as registered, not earned by this result.
- It is one orbit on each of two systems only: 1632 at two seeds and 851 at
  one seed, each on the 1,001-sample Stage-0 training gold record.
- The probe's lead (the depth-linked neighbour-similarity association) remains
  an association, not a cause (D-02, D-07); this result does not convert it.
- No graded run happened and the held-out evaluation is unspent (SCOPE-45):
  these records stay intrinsically marked `inst08-diagnostic`, and the
  graded and evaluator entry points refuse them.
- eps_h does not measure correctness (GAP-59-08, sentence above); the energy
  metric is adjudicated in Phase 68.

## Harness and provenance

- Phase 65 smoke registration historical status (as on the timing page,
  66-TIMING-PREDICTION.md section 8): the Phase 65 smoke registration
  (`.planning/phases/65-probe-on-the-record-fit-harness/evidence/fit/smoke-registration.json`,
  sha256 `ba54e8124a33bb8b172256c6c7150b1f37e3dde1c52c682635bc49e169140d8e`)
  is historical — its live check-registration and verify-result refuse,
  naming `pinn/verification/diagnostic_fit.py`; its evidence is byte-unchanged;
  `tests/phase66/test_historical.py` checks its identity at commit `84128fe2`
  (the commit that added the smoke record); its last live passes were at HEAD
  `c919194d5496847ad4b62e88cb0d75b3b0144580`. The probe registration
  (`evidence/probe/expectations.json`) was already historical before Phase 66.
- Reuse-condition stance (65-CLOSEOUT.md, "Defect dispositions and reuse
  conditions"): Phases 66-67 use the fit harness and shared logger, not the
  historical probe's execution path, and need their own committed predictions,
  registrations and measured budgets — which this phase used. Runs at or
  above a one-hour cap remain refused until governed pause/resume and power
  compatibility is proven. The WR-01 nested-marker limitation stays a
  precondition for graded use, not for this diagnostic phase (D-11).
- Frozen code digests (66-02-SUMMARY.md, at the freeze commit `734cb7da`;
  every registration pins these seven): `pinn/verification/diagnostic_fit.py`
  `4884a1a5a2d0f0356ff142b5bb2ba6b438bdf5e11dd8425f1ec73493c4e7b273`;
  `pinn/verification/diagnostic_guard.py`
  `8dd577a263c28bf7886a0795336ac613fe3fde7c8ebf424fcd6eaf2e80fef540`;
  `pinn/verification/diagnostic_data.py`
  `47b9d99dd991c2a899cb8a4308273643c1d98ea591b851546373e44bcf429836`;
  `pinn/verification/diagnostic_variants.py`
  `ad8ed66c43a8d6edbef15e794f4f06af194a99729acd103428c25bd6cd0c5dfb`;
  `pinn/verification/diagnostic_similarity.py`
  `e80079b62485f04c7c42a513913ef392d7201eea625ff496bae432d0c440d4b7`;
  `pinn/verification/diagnostic_phase66.py`
  `cb0577fe6e976f3ed75ecf95e01f235e0c3cc94289ce316c731fe42581bc4ec7`;
  `pinn/verification/diagnostic_power.py`
  `7e2f00e2c275bc6897bb971af06538ee561635bbabbf1b79c8b7bedfb05f4200`.
- Budget: N = 465000 was set by time alone (0.75 of the 3,300 s cap at the
  timing run's measured rate with a 25 percent margin, D-08); the loss-trace
  stride is 47, so each record keeps at most 10001 loss entries. The
  100,000-step sanity stop did not apply (N is far above it).
- Record sizes: main-1632-s42 1,250,910 bytes; repeat-851-s42 1,251,193
  bytes; repeat-1632-s41 1,251,013 bytes — each below the 10,485,760-byte
  staged-blob limit.
- Timing-run provenance only: `check-run` (never `read-run`) on
  `.planning/phases/66-small-network-control/evidence/timing/1632-s42`
  printed `EXP01-CHECK-OK` with empty mechanical and setting problem lists
  and no score value; the timing run's score stays unread (timing page
  section 6).
- Machine hours on this Mac: the timing run plus the three runs, from the
  four attempts' started/ended timestamps — timing 25 s (2026-11-01T17:57:04Z
  to 17:57:29Z) + main 1957 s + repeat-system 1734 s + repeat-seed 2034 s =
  5,750 s = 1.5972222222222223 hours, about 1.60 machine-hours.

## Evidence index

Every file cited by this page, with the SHA-256 of the committed bytes.

Pages:

- `.planning/phases/66-small-network-control/66-TIMING-PREDICTION.md` —
  `ec54a05e0c98e6b92d303516c4d19ec466064c296ad6227df0efab7ab3e2aaed`
- `.planning/phases/66-small-network-control/66-PREDICTION.md` —
  `7ec16fe90c34cd01406fe227217916754128a283bc6409ed77f4e1811058d8be`

Registrations:

- `.planning/phases/66-small-network-control/evidence/timing/timing-registration.json` —
  `794daa6e334e44c0f3c0c5a040c635614de20d8143629b9f020e71ac998421c6`
- `.planning/phases/66-small-network-control/evidence/exp01/main-1632-s42-registration.json` —
  `b0d79585131c198a4c09f9dea4f1667b57eed8e38fb0d0fd3b11e5071964dcce`
- `.planning/phases/66-small-network-control/evidence/exp01/repeat-851-s42-registration.json` —
  `40754fb93ac4b8a4aa70c580ec233b6fbf7f15fb95dad002a969215062646f36`
- `.planning/phases/66-small-network-control/evidence/exp01/repeat-1632-s41-registration.json` —
  `48a15ad60f4a018c17eab10211153a48df577a292f9853d68eccd4e38592a8f1`

Records, weights, attempts and receipts:

- `.planning/phases/66-small-network-control/evidence/exp01/main-1632-s42/record.json` —
  `774a5a451bda97c79e39e3e10d146bcde8a5a5551b19a0d3cf59022b4b301007`
- `.planning/phases/66-small-network-control/evidence/exp01/main-1632-s42/diagnostic.weights` —
  `bdf95cc1c8b0a148e415892eb2bf9f4ec2eee844f92479ccbd3df3afc0ce31c6`
- `.planning/phases/66-small-network-control/evidence/exp01/main-1632-s42/attempt.json` —
  `a3b9d57b354fb61ae35aba8ee33a4b6763aad018372ff1e587fe915f962205a8`
- `.planning/phases/66-small-network-control/evidence/exp01/main-1632-s42/power-gate.json` —
  `e39b87ca7974447e0b1800e9d43a9595962c751dd3c3868a261dc5c80de218ba`
- `.planning/phases/66-small-network-control/evidence/exp01/repeat-851-s42/record.json` —
  `9166311284ea857ea835813ea74b5ea6a30323d0cb4036341b722dcf56add05b`
- `.planning/phases/66-small-network-control/evidence/exp01/repeat-851-s42/diagnostic.weights` —
  `f73519dffd0e23fd6b8f029c8f38e787fdcd436eb60461e8352b409e9422c62c`
- `.planning/phases/66-small-network-control/evidence/exp01/repeat-851-s42/attempt.json` —
  `9175c53cda4b4a14b11c4eba0dde33b743757b7b7258f993edc6c8b5088a4f0d`
- `.planning/phases/66-small-network-control/evidence/exp01/repeat-851-s42/power-gate.json` —
  `5e2cdbac791cd474397180e540dfcf1b461c1d94010cc11c8e966cfd24954990`
- `.planning/phases/66-small-network-control/evidence/exp01/repeat-1632-s41/record.json` —
  `4146675b56990ca145fa9db777f7922476b1d64ab4cf8f708acb1acec2137c2a`
- `.planning/phases/66-small-network-control/evidence/exp01/repeat-1632-s41/diagnostic.weights` —
  `957af465d74fb55455cf44b9836f32b4ae566d9e942ee67fc65bf4ff8530aabb`
- `.planning/phases/66-small-network-control/evidence/exp01/repeat-1632-s41/attempt.json` —
  `f4c17dfc155fca6362d5420c4723dd4675eb1ccf7724cadcbf684388fbe1a233`
- `.planning/phases/66-small-network-control/evidence/exp01/repeat-1632-s41/power-gate.json` —
  `4464c41db8018b07d0fd54be9d7ed8e0ab6709f2d22e8c2081839a86b4528d2c`
- `.planning/phases/66-small-network-control/evidence/timing/1632-s42/record.json` —
  `128fe093dac017e1b9c0da900d07db8d768ccfacb9d8f22088b97a938859d671`
- `.planning/phases/66-small-network-control/evidence/timing/1632-s42/diagnostic.weights` —
  `68b6ac60987557e693fd22f1a062850a5d8f749b6bee8ad508af796f1712dcc7`
- `.planning/phases/66-small-network-control/evidence/timing/1632-s42/attempt.json` —
  `767b1b15dc08dcec9f73b61279e590b9fd86a9b43f79dadae338d0a67bf81fd6`
- `.planning/phases/66-small-network-control/evidence/timing/1632-s42/power-gate.json` —
  `4b0d150506c3ea7bbf9f67c7a705d070ad7462eaf1f85dbe009dc467684a757c`
