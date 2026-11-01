# Phase 66 Prediction: EXP-01, the small-network control

**Committed after the timing record and before every experiment registration.**
The frozen design of `66-TIMING-PREDICTION.md` applies unchanged, and this page
adds only the budget and the run table. Every experiment registration below
pins this page by SHA-256 and the seven frozen code digests; admission
re-checks the page bytes on every launch, so the page is never amended.

## The frozen design

## 1. The frozen design (applies to every Phase 66 run)

Per D-04, D-05 and D-06. The machine-checkable design block, exactly the
output of `-m pinn.verification.diagnostic_phase66 design`:

```json exp01-design
{
  "budget_rule": {
    "cadence_head": [
      0,
      100,
      300,
      1000,
      3000,
      10000,
      30000,
      100000
    ],
    "cadence_tail_entries": 6,
    "cap_seconds": 3300.0,
    "loss_entry_bytes": 32,
    "loss_trace_entries_max": 10000,
    "rate_margin": 0.25,
    "similarity_margin": 1.15,
    "size_fraction": 0.9,
    "size_limit_bytes": 10485760,
    "step_quantum": 1000,
    "time_fraction": 0.75,
    "timing_cadence": [
      0,
      1300,
      2600,
      3900,
      5200
    ],
    "timing_cap_seconds": 600,
    "timing_loss_trace_stride": 1,
    "timing_steps": 5200,
    "timing_warmup": 200,
    "warmup_steps": 200
  },
  "experiment": "EXP-01",
  "first_layer_frequency_bound": 22.736420441699334,
  "first_layer_inputs": 14,
  "locked_12_parameters": 795657,
  "loss": "data_only",
  "optimizer": {
    "kind": "adam_constant_rate",
    "lr": 0.0001
  },
  "parameters": 157065,
  "physical_window": [
    0.0,
    10.0
  ],
  "reading_rule": {
    "branches": [
      "tier1",
      "near",
      "between",
      "other",
      "unsettled"
    ],
    "confirmation": "confirmed only when all three runs share tier1 or near",
    "e_const_predicted": {
      "hierarchical/gold/1632": 1.1538408194255343,
      "hierarchical/gold/851": 1.233696866477104
    },
    "e_const_source": "comparisons[comparison=window_mean_constant].score.E",
    "e_const_tolerance": 1e-09,
    "frequency_check": [
      0.95,
      1.00001
    ],
    "improvement": {
      "min_growth": 0.01,
      "reference_fraction": 0.75,
      "signal": "similarity.entries[*].output_movement.value"
    },
    "near_band": 0.05,
    "routes": {
      "confirmed near": "propose-66.1",
      "confirmed tier1": "phase67-as-planned",
      "otherwise": "owner"
    },
    "tier1": "pinn/verification/artifacts/feasibility_scorecard_v1.json"
  },
  "runs": [
    {
      "orbit_key": "hierarchical/gold/1632",
      "role": "main",
      "seed": 42
    },
    {
      "orbit_key": "hierarchical/gold/851",
      "role": "repeat-system",
      "seed": 42
    },
    {
      "orbit_key": "hierarchical/gold/1632",
      "role": "repeat-seed",
      "seed": 41
    }
  ],
  "runtime": {
    "device": "mps",
    "dtype": "float32"
  },
  "variant": {
    "depth": 1,
    "first_omega_0": 1000.0,
    "hidden_omega_0": 1.0,
    "learning_rate": 0.0001,
    "name": "exp01-d1-w384-o1000",
    "time_features": "raw_tau_ic13",
    "width": 384,
    "window_length": 10.0
  },
  "variant_registry": "phase66"
}
```

The stack, in plain language: the production layer types
(`SQRSkipResNetSIREN` built through the INST-08 variant registry) with an
input SIREN layer from 14 inputs to 384 units at `first_omega_0 = 1000`; one
SQR-SkipResNet hidden block from 384 to 384 at `hidden_omega_0 = 1.0`, whose
LayerNorm carries no affine parameters; a linear head from 384 to 9; then the
mass-weighted COM projection.

The parameters: 157,065 = 5,376 (input weight 384x14) + 384 (input bias) +
147,456 (hidden weight 384x384) + 384 (hidden bias) + 3,456 (head weight
9x384) + 9 (head bias). That is 19.7 percent of locked-12's 795,657, with 1
hidden layer against 12.

The rest of the setup (D-03, D-06): a data-only fit of position against time
with no physics term; constant-rate Adam at the locked 1e-4 with the locked
betas and epsilon, no scheduler, no clipping, no polish; the full [0, 10]
window on MPS float32; the 1,001-sample Stage-0 training gold record; and the
production input design `[tau, IC13]` unchanged. One variant definition
(`exp01-d1-w384-o1000`) serves all three runs.

## 2. Why first_omega_0 = 1000

Per D-05. The production first layer initializes its weights in
`U[-1/n_in, 1/n_in]` with `n_in = 14` (`pinn/network.py`, `_SIRENLayer`), and
applies `first_omega_0`, so its fastest starting time frequency is
`first_omega_0 / (14 * pi)` rad per unit tau. The input tau is
`2t/10 - 1`, which maps the [0, 10] window to [-1, 1], so one inner lap of an
orbit is `pi` rad per unit tau.

The Phase 59 census gives the inner-lap counts: system 1632 has
N_in 10.471994061054543 laps, system 851 has N_in 18.612048388702. Their
fundamentals are therefore `pi * N_in` = 32.9 rad per unit tau for 1632 and
58.5 for 851. Covering a fundamental from the first layer needs
`first_omega_0 = 14 * pi * N_in`, which is 460.6 for 1632 and 818.6 for 851.

The chosen 1000 covers the faster of the two repeat systems, 851, with a 1.22
margin (22.736420441699334 cycles per window against 18.612), and 1632 with a
2.17 margin.

The in-run check this fixes: the step-0 logged first-layer maximum
(`first_layer_frequency.max` at cadence step 0, in cycles per window) must lie
between 0.95 B and 1.00001 B, with B = 22.736420441699334 cycles per window —
that is, about 21.5996 to 22.7366. A reading near 0.68 (the locked
`first_omega_0 = 30` value) would mean the setting never reached the network.

The research qualifications (66-RESEARCH.md Pattern 1): the fundamental is a
floor, not the full bandwidth the orbit needs (harmonics matter at these
eccentricities); overshooting degrades the initial features of the deeper
layers; the synthetic-proxy usable range is first_omega_0 819 to 1,200 for a
1-hidden-layer network; and the proxy is a prior, not a certificate (A1) —
the real-orbit capacity question is exactly what EXP-01 tests.

Finally, bandwidth alone does not explain v2.4: the locked deep network at
`first_omega_0 = 480` (about 34 rad per unit tau at the fastest) still ended
at E 1.1575.

## 3. What each suspect predicts

Per D-09. For the main run (orbit 1632, seed 42):

| Suspect | Predicts | Observable |
|---|---|---|
| "Too small" (the network lacks capacity for the real orbit) | No Tier 1 | `scores.network.E` above 0.1 |
| A working pipeline with the depth-linked lead | Tier 1, with output movement near 1 rather than about 0.003 | E <= 0.1; the movement figure is reported, not read |
| A pipeline defect (from the data to the scorer, or in the recipe) | The near band, with the output settled — its output movement not growing over the last quarter | E inside the band of section 4 |
| Under-training (the run is too short for this network) | A result above the Tier-1 line with the output movement still growing over the last quarter | Detected by the improvement check; the run reads unsettled and goes to the owner (checker blocker 1; A8) |
| "Metrics too harsh" | Not tested by E (Tier 1 uses E only) | `eps_h` is reported, not read |

The identifiability limit, in plain sentences: failure is predicted by both
"too small" and a pipeline defect, so EXP-01 can refute "too small" but
cannot confirm it. An unsettled run supports no suspect until it settles.

This GAP-59-08 sentence applies to every eps_h figure this experiment
reports, verbatim:
eps_h here is the frozen scorer's autograd-velocity value on the gold grid; it is not the production gate's finite-difference value, GAP-59-08 (owner-routed, Phase 68) is open, and eps_h does not measure correctness for a near-constant predictor.

## 4. The reading rule (immutable after observation)

Per D-09 and the orchestrator ruling on checker blocker 1. The labels are
evaluated in this order, exactly as `classify_exp01` evaluates them:

1. A non-finite E is `other`.
2. `tier1` is E <= the scorecard's Tier-1 E_max, 0.1, inclusive. A Tier-1
   result counts whether or not the run was still improving.
3. `unsettled` is any other result from a run whose improvement check says
   still improving, or whose setting check failed (the table below).
4. `near` is 0.95 E_const <= E <= 1.05 E_const, where E_const is the record's
   own `comparisons[window_mean_constant].score.E` — never a hand-typed
   constant.
5. `between` is above 0.1 and below the band; `other` is above the band.

The improvement check, in plain words. Output movement is how much the
network's output moves over time, as a fraction of how much the real orbit
moves (the DIAG-09 logger records it at every cadence step). Take the last
cadence entry at or before three quarters of the run. If the output movement
grew by more than 0.01 from that entry to the final entry, the run was still
improving when its steps ran out.

Why output movement and not loss: loss values are context, not scores
(ROADMAP diagnosis discipline; D-10). A network cannot fall below the
constant predictor's E without making its output move with time, so growing
movement is the observable sign that a non-Tier-1 run had not settled.

Why 0.01: it is about three times the 0.0030 to 0.0034 at which every v2.4
network settled (64-VERDICT.md line 95). A settled near-constant output
therefore does not trip it, and any larger growth counts as still improving.
A false "still improving" costs one owner question at checkpoint 1. A false
"settled" would wrongly send a run that needed more steps to the 66.1
proposal.

What "near the constant predictor" means here: the run is settled by the
improvement check, its setting check passed, and its E is in the band. A run
with E in the band that is still improving, or whose setting check failed,
reads `unsettled`. So "stays near the constant predictor's E"
(REQUIREMENTS) is read only for runs that are not still improving, and a
result outside the page's branches goes to the owner (SCOPE-47).

The page's setting checks, one row per discretionary setting:

| Setting | The check, and when it runs | A failure means |
|---|---|---|
| `first_omega_0 = 1000` | The census arithmetic of section 2 before the run; on every run, the step-0 first-layer maximum within [0.95 B, 1.00001 B] with B = 22.736420441699334 | The page could not validate the bandwidth on that run. A non-Tier-1 run then reads unsettled, and a Tier-1 run reads out-of-branch, because its fit came from a network the run did not register. Either way it goes to the owner. |
| The step budget N | The improvement check, on every run | A run that fails it reads unsettled and goes to the owner. |
| Depth 1 and width 384 | Conformance to D-04 (1 hidden layer; 157,065 parameters, below 795,657), checked on every run by the variant block and the input and h1 similarity rows; the 157,065-parameter build is pinned by tests/phase66/test_catalog.py | Their capacity on the real orbit is not checked by the run. It rests on the research proxy readout, which is a prior and not a certificate (A1, A11). That capacity is the "too small" question itself, which the identifiability limit already leaves open. That is why the near reading proposes checking the path first, rather than claiming the fault lies there. |
| Every other setting | A locked value (D-06), part of the recipe that the pipeline-defect suspect covers | Routed through the pre-registered branches as recorded. |

No extension rule applies. N uses about three quarters of the one-hour cap,
so a rerun at more steps could not stay under the cap (D-08 makes such a rule
optional). An unsettled run goes to the owner instead, under 66-PREDICTION.md
"What a longer run would need".

The predicted band edges at full precision:

| System | E_const (predicted) | near band |
|---|---|---|
| 1632 | 1.1538408194255343 | from 1.0961487784542576 to 1.211532860396811 |
| 851 | 1.233696866477104 | from 1.1720120231532487 to 1.2953817098009592 |

The mechanical checks that route a run to the owner without reading a branch
(the 66-02-PLAN.md must_haves list): the record's status not complete; the
recorded scorecard grade disagreeing with the network error; the
constant-predictor score more than 1e-9 from its predicted value; similarity
rows other than input and h1; an improvement check that cannot be evaluated;
wrong variant-registry fields; any validation or test-split open; a receipt
that is missing, not AC Power, outside the weekend window or written after
the attempt started; an attempt not published, or whose record digest
disagrees with the record bytes.

The basis for plus or minus 5 percent: the 14 trained v2.4 states lie 0.005
to 0.586 percent above E_const, so the band is about eight times the largest
observed deviation, and the two-Kepler formula at 0.9168 lands in between.

No rule is re-set after a result is seen.

## 5. Repeats and confirmation

Per D-07. The repeat-system run is 851 at seed 42, and the repeat-seed run is
1632 at seed 41. Both run whichever branch the main run lands in. The only
pause is the setting-problem halt of section 7, which leaves them to the
owner.

A result is confirmed only when all three runs share `tier1` or share `near`
(66-RESEARCH.md Pattern 5 item 6). Three runs that agree on `between`,
`other` or `unsettled` stay unconfirmed, because those labels carry no
pre-registered consequence.

The route table:

| Outcome | Route |
|---|---|
| Confirmed tier1 (all three) | "Too small" is refuted for one orbit, and Phase 67 runs as planned, reviewed at checkpoint 1 |
| Confirmed near (all three settled and in the band) | The agent proposes an inserted Phase 66.1 that checks the path from the data to the scorer before the ladders |
| Anything else, including any unsettled run | The owner decides at checkpoint 1 |

The plain-language reading per label:

- `tier1`: a network one-fifth the size, with one hidden layer, fits the
  orbit, so size is not what stopped v2.4; the data and scoring path can
  produce a passing fit.
- Confirmed `near`: a small network whose bandwidth and training length this
  page checked still returns essentially the average position, so the
  depth-linked lead does not explain the failure on its own; the path from
  the data to the scorer is checked next, before the ladders.
  This does not show where the fault is, because a network too small for the
  real orbit predicts the same score. (This is the owner-registered wording,
  REQUIREMENTS "How the first results can reshape the plan"; it deliberately
  does not reuse the stronger research wording of 66-RESEARCH.md Pattern 5
  item 10, which named a location for the fault that the page cannot
  support.)
- `unsettled`: the run was still improving when its steps ran out, so its
  score is not final; the owner decides whether a longer run is worth its
  cost.
- Anything else: the result sits between the lines; the owner decides.

## Budget from the measured rate

The budget was computed once with
`-m pinn.verification.diagnostic_phase66 budget --timing-dir .planning/phases/66-small-network-control/evidence/timing/1632-s42`,
whose EXP01-BUDGET line reads
`EXP01-BUDGET steps=465000 loss_trace_stride=47 cap=3300.0`. The budget prints
no score, similarity value or loss value.

The timing evidence this budget is derived from:

- Record: `.planning/phases/66-small-network-control/evidence/timing/1632-s42/record.json`,
  sha256 `128fe093dac017e1b9c0da900d07db8d768ccfacb9d8f22088b97a938859d671`,
  564082 bytes.
- Receipt (`power-gate.json`) checked_utc `2026-11-01T17:57:03+00:00`
  (AC Power, Sunday 2026-11-01T11:57:02-06:00 America/Chicago, inside the
  owner's weekend window); attempt started_utc `2026-11-01T17:57:04+00:00`,
  ended_utc `2026-11-01T17:57:29+00:00`, status published.

Every input, exactly as the budget read it from the committed record:

- `seconds_per_step` 0.004238129693630617 (the measured 5,000-update sum over
  5,000, warmup, logging and scoring excluded);
- `warmup_seconds` 1.3444102415814996 (the 200 warmup updates);
- `measured_seconds` 21.190648468153086;
- `logging_seconds` 0.5760097929742187 for 5 cadence calls, so
  0.11520195859484374 seconds per call;
- the fixed cost `T_fixed` 4.888931497291196 seconds: the launch wall
  (`launch_wall_seconds` = receipt checked_utc to attempt ended_utc, 26 s,
  plus the 2 s timestamp margin = 28.0 s) minus the record's own warmup,
  measured and logging seconds; it covers process start, admission, data
  load, setup, scoring and publication;
- 56987.2 bytes per similarity entry (the timing record's similarity block
  over its 5 entries);
- 5200 loss-trace entries in the timing record (stride 1);
- record bytes 564082.

The time bound, which is the only bound (D-08): the target is 0.75 of the
3300.0-second cap, that is 2475 s. The projected wall for N steps is
T_fixed + warmup_seconds + (N − 200) x 0.004238129693630617 x 1.25 (the 25
percent rate margin) + (cadence entries) x 0.11520195859484374. N is the
largest multiple of the 1,000-step quantum whose projected wall stays within
the target: N = 465000, whose projected wall is 2470.1995211585886 s (about
41 minutes; the next quantum, 466000, would exceed 2475 s).

- optimizer_steps 465000; warmup_steps 200; measured_steps 464800;
- similarity_cadence [0, 100, 300, 1000, 3000, 10000, 30000, 100000, 160833, 221666, 282500, 343333, 404166, 465000] (the exp01_cadence schedule, 14 entries);
- loss_trace_stride 47 = ceil(465000 / 10000), so the record keeps at most
  10001 loss entries;
- whole_run_cap_seconds 3300.0 (strictly below the harness's 3,600-second
  refusal).

The projected worker record is 1304114 bytes, and the record-size ceiling —
which does not depend on N — is 1307538 bytes against 0.9 of the 10485760-byte
staged-blob limit of scripts/git_policy/validate_staged_paths.py, so the guard
is far from tripping and can refuse only a broken input, never a long run.

One plain sentence: time alone sets the run length (D-08, "as long as you
need"); the record size cannot limit it at any N, because the loss trace
keeps at most 10001 entries and the similarity log at most 14.

## The three runs

The three pre-registered runs of the frozen design, in this order, one at a
time, each detached through the launch wrapper and only inside the gate's
weekend window (Saturday, or Sunday before 22:00, America/Chicago; AC power):

| Role | Orbit key | Seed | Registration | Output directory |
|---|---|---|---|---|
| main | hierarchical/gold/1632 | 42 | `evidence/exp01/main-1632-s42-registration.json` | `evidence/exp01/main-1632-s42/` |
| repeat-system | hierarchical/gold/851 | 42 | `evidence/exp01/repeat-851-s42-registration.json` | `evidence/exp01/repeat-851-s42/` |
| repeat-seed | hierarchical/gold/1632 | 41 | `evidence/exp01/repeat-1632-s41-registration.json` | `evidence/exp01/repeat-1632-s41/` |

The exact launch command per run, from the trainex root (only the
registration and output paths change):

- main: `-m pinn.verification.diagnostic_power launch --registration .planning/phases/66-small-network-control/evidence/exp01/main-1632-s42-registration.json --output .planning/phases/66-small-network-control/evidence/exp01/main-1632-s42/record.json`
- repeat-system: `-m pinn.verification.diagnostic_power launch --registration .planning/phases/66-small-network-control/evidence/exp01/repeat-851-s42-registration.json --output .planning/phases/66-small-network-control/evidence/exp01/repeat-851-s42/record.json`
- repeat-seed: `-m pinn.verification.diagnostic_power launch --registration .planning/phases/66-small-network-control/evidence/exp01/repeat-1632-s41-registration.json --output .planning/phases/66-small-network-control/evidence/exp01/repeat-1632-s41/record.json`

All three use identical steps (465000), cadence, loss-trace stride (47) and
cap (3300.0). They run in the order above whichever branch the main run lands
in; the only pause is the setting-problem halt below.

## Mechanical failure and retry

## 7. Incomplete, retry and out-of-branch

An incomplete attempt is not a result, and neither is a published run that
fails verify-result or check-run's mechanical checks. An attempt whose launch
ended without marking it, a receipt with no attempt, and a directory the
launch created with neither a receipt nor an attempt all count as incomplete.

One retry per run role is allowed for any of these, with identical settings,
under a fresh committed registration named `<role>-retry1-registration.json`
and a new output directory `<role>-retry1`. For the three experiment runs,
`<role>` is main-1632-s42, repeat-851-s42 or repeat-1632-s41, in
`evidence/exp01/`. The timing run's first files are named differently, so its
retry is bound here by name: the registration
`evidence/timing/timing-registration-retry1.json` and the directory
`evidence/timing/1632-s42-retry1`.

A second failure, or a cap expiry, goes to the owner and is never re-sized.

A setting problem (the step-0 bandwidth check of section 4 failed, and no
mechanical check did) does not use the retry, because identical settings
rebuild the same initial network from the same seed. The run's files are
kept, and the runs halt for the owner before the next launch. This halt
chooses no repeat after a result is seen (D-07). check-run reports the
problem without showing any score, and the problem is fixed at step 0, before
training. The remaining runs are not dropped or replaced; the owner decides
when they run.

A battery refusal is a deferral to the next weekend AC window.

## Record readout

For each run, the fields 66-05 quotes from the record (66-RESEARCH.md Pattern
6), plus the improvement check and the band beside the label:

- `scores.network.tier`, `scores.network.E`, `scores.network.eps_h` (the
  frozen scorer's autograd-velocity value on the gold grid);
- the constant predictor: the `comparisons` row `window_mean_constant` and its
  `score.E` (the record's own E_const for the band and the reading rule);
- the two-Kepler row: its `score.E`, or `applicable: false` with its reason (a
  recorded outcome, never a score);
- the neighbour-similarity trace at the registered cadence:
  `similarity.entries[*].layers[*].adjacent_cosine_mean` (rows `input` and
  `h1`), `first_layer_frequency.{median,max}`, `output_movement.value` and
  `output_rate_ratio.value`;
- the improvement check beside the branch: `reference_step`,
  `reference_output_movement`, `final_step`, `final_output_movement`,
  `growth`, `min_growth` and `still_improving`, with `e_band` (the classify
  verdict on E alone) beside the run's `branch` label;
- training loss as context only: `loss.final` and `loss.trace`;
- timing: `timing.seconds_per_step`,
  `timing.end_to_end_seconds_per_completed_step`, `timing.phases.*`;
- access: `access.reads`, `access.attestation`, `access.stage0` (one train
  open, zero validation or test opens);
- variant identity: `variant` (name, fields, `registered`, `registry`),
  `seed`, `registration.sha256`.

The GAP-59-08 sentence, verbatim:
eps_h here is the frozen scorer's autograd-velocity value on the gold grid; it is not the production gate's finite-difference value, GAP-59-08 (owner-routed, Phase 68) is open, and eps_h does not measure correctness for a near-constant predictor.

## What a longer run would need

This is the route an unsettled result may lead to, and it is the owner's
choice at checkpoint 1. A run at or above one hour needs a proven governed
pause, resume and power path first (SCOPE-48; the 65-CLOSEOUT.md reuse
conditions; 66-RESEARCH.md Pattern 7 — the diagnostic fit has no checkpoint,
resume or SIGINT path, and the Phase 60 control scripts are hard-wired to the
Phase 60 launcher). The cap refusals are not loosened. The record size needs
nothing, because it is bounded at any length. None of this is planned.
