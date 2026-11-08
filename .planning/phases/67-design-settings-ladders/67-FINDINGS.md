# Phase 67 findings — EXP-02 through EXP-05 (bounded, evidence-cited)

This page records what the four Phase 67 diagnostic experiments established,
written only from committed evidence. Every quantitative claim is
machine-copied from a committed review, result page, budget or execution
summary; the digests below pin the cited bytes. It makes no Phase 68
pass-bar ruling and no Phase 69 redesign decision, and it adds no source
symbols, CLI flags, packages, thresholds or owner decisions.

## Committed sources cited by this page

| Cited artifact | sha256 |
|---|---|
| `evidence/exp02/review.json` | 853a41b748b7cbf6a30e8af3549006ab999ce820c94efcb218fc29a4a48ff0c4 |
| `evidence/exp03/review.json` | ccd236ef2d4299133b53972fa06ab44ec5df2315d0b3ac6c293f104a4930466c |
| `evidence/exp04/review.json` | 4a2a988389ed5eb063346519bb7f3c0cea36b95f3da67c72f9f0f3222d23892a |
| `evidence/exp05/review.json` | 2e3e5e4a7f6c86c76341239085c54df985b3cf052c0cce4cb2d116f439b1a1fe |
| `67-EXP02-RESULT.md` | eb15b210a1e62bd4e8eca6214d46dee8e94c4fcb9edd88e6de0588383cd81f1f |
| `67-EXP03-RESULT.md` | 63d9148bd25acc701d05cac033025c968a61ed11a72d34893f9dc3476869abb8 |
| `67-EXP04-RESULT.md` | 5bd076ecd69363f906d56489187f5beee24b5c642f73f2d40986734a280f0726 |
| `67-EXP05-RESULT.md` | dacb01271a8fe153439fd75a5981d54509148b3ead2ba68d8b8073d89cb7162d |
| `67-EXP03-RULING.md` | 2b6e8bd8672fd7513ef88b996120a1936cd24d87068b69f16554de10c7ef1a64 |
| `evidence/exp02/budget.json` | b7fa15884a33fd19ffd9bc60ab1ab43d8e0013aacd17514161fef72dd4794ab8 |
| `evidence/exp03/budget.json` | a23df471b0e1587ffa7a27e555ff9e4e2a9c97bbc6589b4c9a6343c318735941 |
| `evidence/exp04/budget.json` | e8000a4360caee1d780fc0c4e596cec7be75a0eb01cc6159f9f724d2e8d7e2ed |
| `evidence/exp05/budget.json` | 85e21beee27bb9486395d926fdc6ed4c62a703eb492f780afda20c41692387fc |
| `67-08-SUMMARY.md` (EXP-02 design/metadata/timing) | 19f120bac5011db6334020d9ac383d273cfb3294a06b5579ada6e3e29b9aa8d9 |
| `67-09-SUMMARY.md` (EXP-02 rows/review) | 2d4d6a0ee2d9ebc0f42190d2bbeeffdae711f3defab27b6d853d78f61c8b5331 |
| `67-10-SUMMARY.md` (EXP-03 design/metadata/timing) | 018672a00abc6199824ee29df4b562cdeb1e5604e02bfd5423b1c64e7760fdb6 |
| `67-11-SUMMARY.md` (EXP-03 rows/review) | 7da978e86f9cec9bd7b41dc3de85cef87589722ab334fdd3e5fd225e6613d400 |
| `67-12-SUMMARY.md` (EXP-04 design/metadata/timing) | d9d9d7ba6cbf629736d623f4a7dc4bca5d4d291eba768fe438ded0687ffc07a7 |
| `67-13-SUMMARY.md` (EXP-04 rows/review) | d134f4af01c1b4918c6ca70e60b1ffb103acc9914afa6783da8a03c7d9785e03 |
| `67-14-SUMMARY.md` (EXP-05 design/metadata/timing) | 2f11d6411a1b4a17c6d4e4f919e74346c9107462b09899b52d0cde9a371a6804 |
| `67-15-SUMMARY.md` (EXP-05 rows/review) | dba01320766b9fd81f599af4a84a4f0a58b20e5cdb61ae5a30a3e0d5c83de92e |
| `67-EXP04-PREDICTION.md` (fan-in confound) | bee1cddcfdbcc0938e62d60da2e7c760be980828651dae88d0077d8758bd360a |
| `../66-small-network-control/66-RESULT.md` | bf143995410ae48a57845b5cf7f5500dc059c4fd0af96486a1b43801b88d26a9 |
| `../59-read-only-baseline-scorecard/59-GAPS.md` | cca54c8c2dfae15def65f9345835223481b952a148605f2aede1c852c7a5bbe0 |
| `evidence/harness-freeze.json` | a84c93ba53937cc6c554b6f06c152815c00ba1c6cd00ccef5b383cdd4ac17a6e |

All paths are relative to `.planning/phases/67-design-settings-ladders/`
except the two that begin with `../`. The four reviews carry schema
`phase67-review/v1` and each result page embeds its review byte-exactly.

## Reading rules this page applies (never re-set after results)

- Endpoint status applies the registered final-quarter rule: a relative E
  improvement over the last quarter strictly greater than 5% leaves the
  endpoint unsettled; no branch extends, retries or re-sizes any run after
  its score is read (the no-continuation policy, identical in all four
  committed designs).
- A case qualifies only if the E direction is nonzero and either the tier
  changes in the same direction or the relative E effect is at least the
  exact 20% line. A contrast confirms improvement or worsening only when
  all three registered cases qualify in the same direction and all six
  paired endpoints are settled and mechanically clean; otherwise it reads
  unsettled, ambiguous or inconclusive-mechanical. A favourable main run
  alone can never confirm.
- E is the frozen scorecard's position-error score. GAP-59-08 stays
  explicit: no energy bar or scorer definition is adjudicated here
  (each review's `gap_59_08` field; `59-GAPS.md` GAP-59-08 records that the
  production energy check fails even a perfect answer and is owner-routed).
- Adjacent-time hidden-state similarity (centred hidden-state cosine
  between adjacent times, per layer) is associated evidence only: no cosine
  threshold and no causal claim. Loss is context only.

## EXP-02 — depth ladder (15 science rows, common N = 152900)

**Registered prediction** (`evidence/exp02/design.json` via the review's
`predictions_comparison`): "shallower depth improves the one-orbit fit:
each shallower arm's E is below the d12 control's on all three registered
cases under the registered effect rule". Arms d2/d4/d6/d8/d12 at the locked
layer types, width 256, first omega 30, raw 14-dim `[tau, IC13]` input,
rate 1e-4, physical window [0,10]; cases main-1632-s42, repeat-851-s42,
repeat-1632-s41.

**Complete observed branch: unsettled continue.** `confirmed` is empty and
all four contrasts read unsettled (`evidence/exp02/review.json`,
`confirmation`).

Matched effects (relative E vs each case's d12 control; all values
machine-copied from `evidence/exp02/review.json` -> `confirmation` ->
`contrasts`):

| contrast | main | repeat-851-s42 | repeat-1632-s41 | label |
|---|---|---|---|---|
| d2 | worsening 2.491, tier worsened (arm settled / control unsettled) | worsening 0.243, tier worsened (arm unsettled / control settled) | worsening 1.525, tier worsened (both unsettled) | unsettled |
| d4 | improvement 0.012, below the 20% line | improvement 0.086, below the 20% line | worsening 2.457, tier worsened | unsettled |
| d6 | worsening 0.690 | improvement 0.854 | improvement 0.743 | unsettled |
| d8 | improvement 0.040, below the 20% line | improvement 0.788 | improvement 0.662 | unsettled |

Every contrast's observed cell values, endpoint statuses and reasons are in
the committed review; the per-row E/tier/endpoint/wall tables with row
commit hashes are in `67-EXP02-RESULT.md`.

**What this establishes, bounded:** the shallowest arm d2 worsens on all
three registered cases with qualifying effects, but unsettled endpoints
block confirmation in either direction (the main-case d12 control endpoint
is itself unsettled). d8 improves on all three cases without qualifying on
main; d4 and d6 disagree across cases. The registered depth hypothesis is
therefore not supported at confirmation grade, and no claim of a confirmed
improvement or worsening from depth is made.

**Uncertainty and limits preserved:** endpoint unsettles on the main-case
and repeat-system controls plus several arms (finite budgets ended with
arms still improving; the no-continuation policy extends nothing). The
D-03 confound is recorded, not controlled away: parameter counts rise with
depth (d2 137,737 / d4 269,321 / d6 400,905 / d8 532,489 / d12 795,657),
so any depth-ordered E pattern co-varies with network size
(`67-EXP02-RESULT.md`). The Phase 66 positive-control confounding (D-02)
also applies: see "Shared limits" below.

**SCOPE-49 disposition:** `scope49_disposition = none`,
`proposed_change = null`, `dependent_launch_allowed = true`
(`evidence/exp02/review.json`). No ruling file exists and none was required.

**Measured cost:** 15 science walls totalling 19,750.2 s (693.6–2135.6 s
per row) against the measured projection 25,466.9 s, every row inside its
3540 s cap and per-row projection, no failed attempts
(`67-09-SUMMARY.md`; `67-EXP02-RESULT.md`). The 15 timing rows ran at
N1200/warmup200 under the 900-second cap (`67-08-SUMMARY.md`).

## EXP-03 — learning-rate ladder (15 science rows, common N = 155100)

**Registered prediction** (`evidence/exp03/design.json` via the review's
`predictions_comparison`): "learning-rate sensitivity: the fit's E changes
across the rate ladder against the lr1e-4 control on the registered cases"
— under the hypothesis, learning-rate sensitivity improves the fit. Arms
lr1e-3 / lr3e-4 / lr1e-4 (locked control) / lr3e-5 / lr1e-5 on the locked
12-layer network, same three cases.

**Complete observed branch: refuted lead, owner-ruled.** `confirmed`
contains exactly one entry: `[{"arm": "lr1e-3",
"confirmation": "confirmed-worsening"}]`
(`evidence/exp03/review.json`, `confirmation`).

Matched effects (relative E vs each case's lr1e-4 control; all values
machine-copied from `evidence/exp03/review.json`):

| contrast | main | repeat-851-s42 | repeat-1632-s41 | label |
|---|---|---|---|---|
| lr1e-3 | worsening 34.761, tier worsened (both settled) | worsening 39.164, tier worsened (both settled) | worsening 15.377, tier worsened (both settled) | confirmed-worsening |
| lr1e-5 | worsening 4.155, tier worsened (both settled) | worsening 4.368, tier worsened (arm unsettled) | worsening 1.221, tier worsened (both settled) | unsettled |
| lr3e-4 | worsening 32.951, tier worsened (both settled) | improvement 0.511 (arm unsettled) | worsening 19.135, tier worsened (both settled) | unsettled |
| lr3e-5 | worsening 0.904 (tier unchanged) | improvement 0.459 (tier unchanged) | worsening 1.306, tier worsened | ambiguous |

**What this establishes, bounded:** the registered rate-sensitivity
hypothesis is refuted at confirmation grade — lr1e-3 worsens in all three
registered cases with matching tier change and qualifying effects, all six
endpoints settled. Nothing is confirmed-improving anywhere in the ladder.
lr3e-5 reads ambiguous (the registered cases disagree on the E direction);
the other two non-control arms read unsettled with worsening in most cells.
Endpoint E values for the confirmed contrast: main 1.455151 vs control
0.040691; repeat-seed 1.402451 vs 0.034918; repeat-system 1.563923 vs
0.095496 (`evidence/exp03/review.json`).

**SCOPE-49 disposition (factual):** the committed review reads
`scope49_disposition = proposal-pending` with
`dependent_launch_allowed = false` on the registered refuted-lead branch.
The owner resolved the reserved decision on 2026-11-05 with the verbatim
instruction "proceed with option 1", selecting `authorize-recorded-proposal`
(`67-EXP03-RULING.md`, digest-bound: `proposal_sha256` e949fffb…,
`review_sha256` ccd236ef… matching `evidence/exp03/review.json`,
`result_page_sha256` 63d9148b… matching `67-EXP03-RESULT.md`; introducing
commit bfd85916; `changed_by_ruling = false` for both reviewed artifacts).
The ruling authorizes EXP-04's dependent launch under its existing
committed registration and authorizes no plan amendment, scope change,
pass-bar change or registration change. The audit reads exp03 as
`proposal-ruled`.

**Measured cost:** all 15 science walls measured 2069–2385 s, total 32,185 s
against the 39,055.09 s experiment projection, every row inside its cap
(`67-11-SUMMARY.md`). The 15 timing rows measured segments 13.21–13.66 s per
row; the metadata capture and timing rows ran inside the owner amendment's
weekday window on 2026-11-04 (`67-10-SUMMARY.md`).

## EXP-04 — time-input design ladder (18 science rows, common N = 112700)

**Registered prediction** (`evidence/exp04/design.json` via the review's
`predictions_comparison`): "the encoded harmonic input improves the fit:
each encoded arm's E is below its own backbone's raw control's on all three
registered cases". Four contrasts on two backbones, each encoded arm
against its own backbone's raw control: exp01-f1 and exp01-f12 vs exp01-raw
(the actual EXP-01 network), locked-f1 and locked-f12 vs locked-raw (the
locked network); same three cases.

**Complete observed branch: unsettled continue.** `confirmed` is empty and
all four contrasts read unsettled (`evidence/exp04/review.json`,
`confirmation`).

Matched effects (relative E vs each case's own-backbone raw control; all
values machine-copied from `evidence/exp04/review.json`):

| contrast | main | repeat-851-s42 | repeat-1632-s41 | label |
|---|---|---|---|---|
| exp01-f1 | worsening 6.066 (tier unchanged) | worsening 1.664 (tier unchanged) | worsening 0.804 (tier worsened) | unsettled |
| exp01-f12 | worsening 3.477 (tier unchanged) | worsening 4.283 (tier unchanged) | worsening 0.965 (tier worsened) | unsettled |
| locked-f1 | worsening 0.341 (tier unchanged) | improvement 0.426 (tier unchanged) | worsening 0.444 (tier unchanged) | unsettled |
| locked-f12 | worsening 0.748 (tier unchanged) | improvement 0.056, below the 20% line | worsening 0.254 (tier unchanged) | unsettled |

**What this establishes, bounded:** the registered input-design hypothesis
is not supported at confirmation grade. The encoded harmonic arms worsen
against their own backbone's raw control in ten of the twelve registered
cells; the only improvement cells are the seed-41 repeat on the two locked
arms (one below the 20% line), so no case combination approaches
confirmation. No claim that encoded inputs help or hurt at confirmation
grade is made.

**Uncertainty and limits preserved:** endpoint unsettles are widespread
(including both main-case encoded-arm/control pairs and the exp01-raw
main control), so even the observed worsening directions are not
confirmation-grade. The input fan-in/dimension change is recorded as a
confound, not controlled away: the encoded arms change the input design,
not `first_omega_0` (D-05), with first-layer fan-in bound 1/16 for f1 and
1/18 for f12 (internal dimensions 16/18) on both backbones, and census
feature frequencies f = N_in/10 (1.0471994061 rad per unit time on 1632,
1.8612048389 on 851) with harmonics 1 (f1) or 1 and 2 (f12)
(`67-EXP04-PREDICTION.md` confounds; `evidence/exp04/design.json`
variants). The frequency diagnostic's input-weight-column-zero reading is
raw-input-only; encoded arms carry explicit nonapplicability with
registered feature metadata (committed record checks).

**SCOPE-49 disposition:** `scope49_disposition = none`,
`proposed_change = null`, `dependent_launch_allowed = true`
(`evidence/exp04/review.json`). No ruling file exists and none was required.

**Measured cost:** all 18 rows launched exactly once, walls 442–1987 s,
total 19,695 s against the 25,880.3 s projection, each a complete
112700-step attempt under the 3540-second cap (`67-13-SUMMARY.md`). The 18
timing rows ran at N1200 under the 900-second cap (`67-12-SUMMARY.md`).

## EXP-05 — window ladder (12 science rows, common N = 148700)

**Registered prediction** (`evidence/exp05/design.json` via the review's
`predictions_comparison`): "a shorter window improves the fit: each shorter
prefix arm's E is below the lap10 control's on all three registered cases".
Three contrasts (lap1, lap2, lap5 against each case's lap10 control) at the
locked settings, using exact signed first-crossing 1/2/5/10-lap prefixes
with the unchanged global tau normalization; same three cases.

**Complete observed branch: unsettled continue.** `confirmed` is empty and
all three contrasts read unsettled (`evidence/exp05/review.json`,
`confirmation`).

Matched effects (relative E vs each case's lap10 control; all values
machine-copied from `evidence/exp05/review.json`):

| contrast | main | repeat-851-s42 | repeat-1632-s41 | label |
|---|---|---|---|---|
| lap1 | improvement 0.802 (both unsettled) | improvement 0.863, tier improved (both settled) | improvement 0.651 (arm settled / control unsettled) | unsettled |
| lap2 | improvement 0.422 (both unsettled) | improvement 0.137, tier improved (both settled) | improvement 0.884 (arm settled / control unsettled) | unsettled |
| lap5 | improvement 0.488 (both unsettled) | improvement 0.683, tier improved (both settled) | improvement 0.532 (arm settled / control unsettled) | unsettled |

**What this establishes, bounded (per the committed review and
`67-15-SUMMARY.md`):** the improvement direction is present on all nine
case-contrast cells and every relative E effect qualifies (0.14–0.88, all
above the exact 20% line), with the frozen tier improving only on the
seed-41 repeat. But unsettled endpoints block confirmation in every
contrast: on the main case all six endpoints (three short arms and the
lap10 control) were still improving by more than the registered five
percent when their budgets ended, and on the repeat-system case the three
short arms settled while their lap10 control did not. Only the seed-41
repeat case is fully settled. Nothing is confirmed in either direction, and
neither a short-window success nor a full-window failure is declared.

**Exact short-window coverage preserved:** each arm uses its actual signed
first-crossing endpoint per system — 0.95/1.89/4.76/9.51 physical time
units on 1632 and 0.54/1.08/2.68/5.37 on 851 for 1/2/5/10 laps
(`evidence/exp05/budget.json` per-row window lengths; identical values in
`67-15-SUMMARY.md`). Per-row requested endpoint, last retained timestamp,
sample count and actual lap coverage are in each committed row record (for
example the main lap1 record attests `requested_window` [0, 0.95] with 96
of 1002 snapshots inside the window); same-window baselines were recomputed
by the committed metadata for every window, and the census mean period
remains only a labelled rough planning estimate.

**SCOPE-49 disposition:** `scope49_disposition = none`,
`proposed_change = null`, `dependent_launch_allowed = true` on the
registered unsettled branch (`evidence/exp05/review.json`). No ruling file
exists and none was required; the conditional task-03 owner checkpoint was
skipped by its own condition.

**Measured cost:** 12 whole-launch walls 2012/1957/2006/2226/2203/2629/
2791/2874/2593/2699/2899/2357 s, total 29,246 s (≈ 8.12 h) against the
30,305.5 s projection, every row inside the 3540 s cap and the
remaining-window allowance at its launch, no failed attempts
(`67-15-SUMMARY.md`). The 12 timing rows ran at N1200 under the 900-second
cap (`67-14-SUMMARY.md`).

## Actual machine cost of the phase (for the Phase 69 handoff)

The four science campaigns ran 19,750.2 + 32,185 + 19,695 + 29,246 =
100,876.2 s (≈ 28.0 h) of measured launch wall against projected totals of
25,466.9 + 39,055.1 + 25,880.3 + 30,305.5 = 120,707.8 s. Each figure cites
its committed per-experiment source above; the exp03/exp04/exp05 totals are
whole-launch supervision walls and the exp02 total is the committed
record-wall basis (the two bases differ by a few seconds per experiment).
Timing campaigns added 15/15/18/12 single 1200-step rows under 900-second
caps (per-row measured segments cited above), and the four metadata
captures are published read-only census captures whose committed attempt
receipts carry no wall-second field. No failed or partial attempt exists
anywhere in the phase evidence: the 124 committed attempt records
(60 timing + 60 science + 4 metadata) all read `published` with complete
records, and no successful-row count includes anything but published
complete attempts.

## Shared limits carried by every experiment

- **EXP-01 positive-control confounding (D-02).** Phase 66's confirmed
  Tier-1 fit (E = 0.0114312 on 1632/s42, 0.0172056 on 851/s42, 0.0789849 on
  1632/s41, `../66-small-network-control/66-RESULT.md`) came from a
  multi-setting change (depth 1, width 384, first omega 1000) against the
  locked variant (depth 12, width 256, first omega 30). It refutes "too
  small" for the tested one-orbit task but does not identify which changed
  setting enabled the fit. All four designs record this note
  (`positive_control_note` in each committed design).
- **Depth size confounding (D-03).** Parameter counts rise with depth
  (137,737 to 795,657 across the EXP-02 arms); depth is not isolated from
  network size in the observed patterns.
- **Input fan-in/dimension changes (D-05, EXP-04).** Encoded arms change
  the first layer's fan-in (1/16, 1/18) and input design, not
  `first_omega_0`; input-design effects and frequency-scale effects remain
  distinct in the committed declarations.
- **Finite-budget reading (D-08).** A failed finite-budget fit is not
  representational impossibility: an unsettled endpoint means the budget
  ended while the fit was still moving, and the no-continuation policy
  extends nothing. No result here labels a budget-limited run a
  representation failure.
- **Adjacent-time similarity is association only.** Low (or high) neighbour
  cosine remains an association to investigate, not proof of information
  loss, a causal mechanism, or an accurate fit; no cosine threshold is
  applied anywhere in the committed reviews.
- **No new-IC generalization.** Every fit is a single-orbit, TRAIN-only
  diagnostic fit on the Stage-0 training split; none of these results is
  evidence of generalization to new initial conditions.
- **GAP-59-08 energy caveat.** E is the frozen scorecard's position-error
  score; the production energy check fails even a perfect answer on the
  coarse output grid and stays owner-routed and unadjudicated
  (`59-GAPS.md` GAP-59-08).
- **Roadmap wording stays weaker than causal.** The experiments distinguish
  observed fits, replicated finite-budget effects and ambiguity under
  prospective rules; they do not establish a causal attribution of the
  locked setup's one-orbit failure to any single setting, and no finding
  here strengthens the roadmap's causal wording beyond that.

## What the phase did not decide

No Phase 68 pass-bar or energy adjudication, no Phase 69 redesign decision,
no framework-spec or locked-value change, and no scope amendment beyond the
one owner ruling recorded factually above. Those decisions belong to their
own phases and owners.
