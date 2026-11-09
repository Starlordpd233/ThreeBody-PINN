# Phase 69 supporting evidence

The [checked inventory](evidence/69-evidence.json) is committed at `0f53ab64061a1998e2df2a082149f087ee6c4b03`. Its `sources.source_rows` entries record the full path, revision and SHA-256 for the source records below. The comparison baseline is `0f91709000a442507e0eb2b9616f474a81525333`. For later re-pins or local edits, read the cited Git revision.

The frozen FEAS-01 score E is the maximum normalized error in body position or inner-pair separation over the scored window. Lower is better. The Tier 1 position criterion is E ≤ 0.1. The tables carry the recorded tier labels. Diagnostic grades use the gold grid, the r_prime_u frame and autograd velocities. Energy drift ε_H from that route and the production finite-difference gate are distinct measurements. [Scorer](../../../pinn/verification/feasibility_scorer.py) · [Frozen scorecard](../../../pinn/verification/artifacts/feasibility_scorecard_v1.json)

## Historical failures and successful locked controls

The frozen v2.4 rule returned `RETHINK-REPRESENTATION` after all three Rung 1 cases and the first-frequency sweep ended at Tier 0. The matched controls below establish that the locked architecture can fit these supervised tasks under a different recipe. The historical rule’s outcome remains on record. [v2.4 verdict](../64-feasibility-verdict/64-VERDICT.md) at `67c31af61504c1b88024e0be251426a15fcb8a9e`

| System/seed | Historical record | Adam E | Polish E | Official E / tier | Control E / tier | Control record at publication |
|---|---|---|---|---|---|---|
| 1632/42 | [r1-1632](../60-single-system-learnability/evidence/arms/r1-1632/record.json) at `0f91709000a4` | 1.1606404574102112 | 1.157387378319295 | 1.157387378319295 / 0 (polish) | 0.040691019043637484 / 1 (settled) | [lr1e-4](../67-design-settings-ladders/evidence/exp03/science/main-1632-s42/lr1e-4/record.json) at `df40671e2e07` |
| 851/42 | [r1-851](../60-single-system-learnability/evidence/arms/r1-851/record.json) at `0f91709000a4` | 1.2375295559620059 | 1.2383540710834968 | 1.2375295559620059 / 0 (adam) | 0.09549573839491703 / 1 (settled) | [lr1e-4](../67-design-settings-ladders/evidence/exp03/science/repeat-851-s42/lr1e-4/record.json) at `23df087ccb13` |
| 1632/41 | No historical match | — | — | — | 0.03491785615016659 / 1 (settled) | [lr1e-4](../67-design-settings-ladders/evidence/exp03/science/repeat-1632-s41/lr1e-4/record.json) at `623f8df6641e` |

System 851 is the second physical system. Seed 41 repeats system 1632. Control energy drifts were 1.884224250407955, 4.801534852996827, 7.866109129043417 in table order. Those are supervised fits on the orbits used in training. Physics learning and generalization remain open. [Registered review](../67-design-settings-ladders/evidence/exp03/review.json) at `0f91709000a4`

## Recipe comparability

The historical records identify implementation revision `a686d26e00f7c1e8ba54bb2d3e1cd730a3404a69`. The diagnostic rows bind their registrations to their individual publication revisions. Later re-pins differ. The inventory’s `sources.recipe.aspects` entries carry the cited implementation lines and underlying fields.

| Aspect | Status | Evidence |
|---|---|---|
| Architecture | Verified equivalent | Same production class, 12 layers of width 256, first and hidden frequencies 30 and 1, raw time plus IC13. The 33-module digest maps agree. |
| Initialization | Verified equivalent construction | Same seeded production construction for the paired seed-42 cases. The diagnostic builder uses a local generator. |
| Archived initial tensors | Open | Exact tensor identity across the old and new runs is unproved. |
| Input, targets, body order and gauge | Verified equivalent | Same production transform and ordered raw masses, global characteristic time and float32 residency times. The selected time and target arrays have identical digests. |
| Normalization | Verified equivalent statistics | Historical recovery and diagnostic rehydration both resolve to `77526e53c394bbac4d4a0e8fdd5a7688f0bda108d41c56277b55ad426a7a79f6`. |
| Window, grid and sample selection | Equivalent samples, different bounds | Both select 1,001 gold points over [0, 10]. The historical mask allows an extra 1e-9 at the upper bound. The diagnostic uses the exact bound. Actual selected arrays agree. |
| Loss and reduction | Verified equivalent | Full-batch data-only Huber loss divided by 9 times the sample count. Every update sees all retained points. |
| Adam policy | Verified difference | Shared betas (0.9, 0.999) and epsilon 1e-8. Historical cosine Adam starts at 1e-3. The controls use constant Adam 1e-4. |
| Clipping and polish | Verified difference | The historical runs record 66 and 93 clipped steps and six and seven diagnostic polish outer calls respectively. The controls use neither clipping nor polish. |
| Precision and device | Verified equivalent settings | MPS float32 in both recipes. |
| Runtime state, kernels and determinism | Open | Exact historical equivalence remains unproved. |
| Update budget | Verified difference | 794,350 and 980,523 historical Adam updates versus 155,100 for each control. |
| Scored state | Verified difference | Historical official state is polish for 1632 and Adam for 851. Controls use their registered endpoint. The score route agrees. |

| System | Matched training and scoring window SHA-256 |
|---|---|
| 1632 | `9d9aa6c66259007aa99aa63c28c96294842daaa42e56869a0593d3b0b5537c63` |
| 851 | `de2d509b3389ba4cb69afd253329cce1b2e5c44aeefa3a2ca5204e10a6181751` |

This retrospective comparison changes several settings together. EXP-03 isolates constant-rate variation within the diagnostic harness. It leaves the historical effects of the cosine schedule, clipping, polish, update budget and runtime unresolved.

## DIAG-09 original probe lead

The registered prediction was to reproduce previously seen fields on seven historical networks at reconstructed initialization and after training. The result was `retained`: 144/144 required fields reproduced and 0 failed. There are 64 preserved-only fields and 130 supplemental per-layer measurements. The historical summary’s new-measurement field is empty, while the top-level array retains the supplemental measurements. [Committed prediction](../65-probe-on-the-record-fit-harness/65-PROBE-PREDICTION.md) at `0f91709000a4` · [Reproduction record](../65-probe-on-the-record-fit-harness/evidence/probe/reproduction.json) at `0f91709000a4`

| Arm | State | Deepest adjacent-time cosine | Relative output movement | Median first-layer frequency |
|---|---|---|---|---|
| g2s-1632-w060 | init | 0.7505207051138141 | 2.7740869806584505 | 0.7813737312448045 |
| g2s-1632-w060 | adam | 0.002861468359487634 | 0.0033621071499160124 | 7.754830582362674 |
| g2s-1632-w120 | init | 0.4134875303532734 | 2.8466606393951683 | 1.562747462489609 |
| g2s-1632-w120 | adam | 0.004263718941992801 | 0.003205822899410137 | 16.801547050003656 |
| g2s-1632-w240 | init | 0.10357193496344971 | 2.824651414968202 | 3.125494924979218 |
| g2s-1632-w240 | adam | 0.0038446421962455373 | 0.002999651205459768 | 33.5312131891821 |
| g2s-1632-w480 | init | 0.02033517355491443 | 2.846060573673386 | 6.250989849958436 |
| g2s-1632-w480 | adam | -0.004967691111750435 | 0.003046161860010531 | 66.38361941135109 |
| r1-1632 | init | 0.9247840401321666 | 2.872958741554662 | 0.39068686562240224 |
| r1-1632 | polish | 0.003249426338720477 | 0.0034418917001109717 | 4.246399185618351 |
| r1-4658 | init | 0.9205834354813007 | 7.039588303917579 | 0.39068686562240224 |
| r1-4658 | adam | -0.0009682228072291421 | 0.0030443613714751985 | 5.285795744578519 |
| r1-851 | init | 0.9318229316261353 | 2.3524703618496132 | 0.39068686562240224 |
| r1-851 | adam | 0.0008469900484679206 | 0.0030759157109364033 | 3.9824653081634254 |

Low adjacent-time similarity co-occurred with nearly constant output. The probe reconstructed initialization on CPU float64 and revisited the same trained networks. Information loss and a causal explanation remain open. The record preserves the remaining layers, predicted tokens and rate ratios. [Phase 65 accepted-use conditions](../65-probe-on-the-record-fit-harness/65-CLOSEOUT.md) at `0f91709000a4`

## EXP-01 small-network control

Parameter shortage predicted that the smaller network would fail to reach Tier 1. A settled near-constant result would have triggered a data-to-scorer review. The registered confirmation required a shared Tier 1 or near-constant branch across main, repeat-system and repeat-seed. The one-layer network used 157,065 parameters versus 795,657 for the locked network. Depth, width and first frequency all changed. All three cases reached Tier 1 and the registered route was `phase67-as-planned`. [Committed prediction](../66-small-network-control/66-PREDICTION.md) at `0f91709000a4` · [Registered review](../66-small-network-control/66-RESULT.md) at `0f91709000a4`

| System/seed | E / tier | ε_H | Constant E | Two-Kepler E | Record |
|---|---|---|---|---|---|
| 1632/42 | 0.011431234453278821 / 1 | 0.23059668730403904 | 1.1538408194255343 | 0.9168487091299374 | [record](../66-small-network-control/evidence/exp01/main-1632-s42/record.json) at `0f91709000a4` |
| 851/42 | 0.01720558902801923 / 1 | 0.3529082508657166 | 1.233696866477104 | 0.4312597209593449 | [record](../66-small-network-control/evidence/exp01/repeat-851-s42/record.json) at `0f91709000a4` |
| 1632/41 | 0.07898485527313073 / 1 | 0.4403488467986121 | 1.1538408194255343 | 0.9168487091299374 | [record](../66-small-network-control/evidence/exp01/repeat-1632-s41/record.json) at `0f91709000a4` |

## How to read the ladders

Each contrast uses a matched control. Confirmation requires all three cases to qualify in one direction with clean, settled endpoints. A matching tier change or at least 20% relative E effect qualifies a case. Improvement greater than 5% over the last quarter leaves an endpoint unsettled. I means improvement, W means worsening and ✓ marks a qualifying case effect. Per-case effects, checkpoints and failure reasons are in the registered reviews. [Phase 67 closeout](../67-design-settings-ladders/67-CLOSEOUT.md) at `0f91709000a4`

The Phase 67 narrative swaps the repeat-system and repeat-seed columns in some effect tables. The lr1e-3 relative effects are 15.376889578229147 for 851/42 and 39.16428044173176 for 1632/41. The raw keyed reviews and run records agree. Their registered labels are used below. [Historical narrative](../67-design-settings-ladders/67-FINDINGS.md) at `0f91709000a4` · [Raw EXP-03 review](../67-design-settings-ladders/evidence/exp03/review.json) at `0f91709000a4`

## EXP-02 depth ladder

The registered prediction was shallower depth improves the one-orbit fit: each shallower arm's E is below the d12 control's on all three registered cases under the registered effect rule. [Committed prediction](../67-design-settings-ladders/67-EXP02-PREDICTION.md) at `0f91709000a4` · [Registered review](../67-design-settings-ladders/evidence/exp02/review.json) at `0f91709000a4`

Each arm used 152,900 updates. All four shallower-depth contrasts were unsettled. The d2 arm had worse E in all three cases, with unsettled endpoints.

| Arm | Control | Main 1632/42 | Repeat system 851/42 | Repeat seed 1632/41 | Registered reading |
|---|---|---|---|---|---|
| d2 | d12 | W ✓ | W ✓ | W ✓ | `unsettled` |
| d4 | d12 | I | W ✓ | I | `unsettled` |
| d6 | d12 | W ✓ | I ✓ | I ✓ | `unsettled` |
| d8 | d12 | I | I ✓ | I ✓ | `unsettled` |

| System/seed | Arm | Samples | Window end | E | Tier | ε_H | Endpoint | Record |
|---|---|---|---|---|---|---|---|---|
| 1632/42 | d12 | 1001 | 9.999999999999831 | 0.03482590188705743 | 1 | 4.416877124406674 | unsettled | [record](../67-design-settings-ladders/evidence/exp02/science/main-1632-s42/d12/record.json) at `0f91709000a4` |
| 1632/42 | d2 | 1001 | 9.999999999999831 | 0.12158120320360874 | 0 | 0.2642484341123774 | settled | [record](../67-design-settings-ladders/evidence/exp02/science/main-1632-s42/d2/record.json) at `0f91709000a4` |
| 1632/42 | d4 | 1001 | 9.999999999999831 | 0.0343996498236197 | 1 | 0.10574600253161902 | settled | [record](../67-design-settings-ladders/evidence/exp02/science/main-1632-s42/d4/record.json) at `0f91709000a4` |
| 1632/42 | d6 | 1001 | 9.999999999999831 | 0.0588671343305699 | 1 | 0.11688786475535326 | settled | [record](../67-design-settings-ladders/evidence/exp02/science/main-1632-s42/d6/record.json) at `0f91709000a4` |
| 1632/42 | d8 | 1001 | 9.999999999999831 | 0.03344629454651585 | 1 | 0.1583505368867083 | settled | [record](../67-design-settings-ladders/evidence/exp02/science/main-1632-s42/d8/record.json) at `0f91709000a4` |
| 851/42 | d12 | 1001 | 9.999999999999831 | 0.06749088823348984 | 1 | 2.72791719958816 | unsettled | [record](../67-design-settings-ladders/evidence/exp02/science/repeat-851-s42/d12/record.json) at `0f91709000a4` |
| 851/42 | d2 | 1001 | 9.999999999999831 | 0.17043356151106176 | 0 | 0.5315043436535077 | unsettled | [record](../67-design-settings-ladders/evidence/exp02/science/repeat-851-s42/d2/record.json) at `0f91709000a4` |
| 851/42 | d4 | 1001 | 9.999999999999831 | 0.23328599364334615 | 0 | 0.4739514161119753 | settled | [record](../67-design-settings-ladders/evidence/exp02/science/repeat-851-s42/d4/record.json) at `0f91709000a4` |
| 851/42 | d6 | 1001 | 9.999999999999831 | 0.01731869678957498 | 1 | 0.10553654345352415 | unsettled | [record](../67-design-settings-ladders/evidence/exp02/science/repeat-851-s42/d6/record.json) at `0f91709000a4` |
| 851/42 | d8 | 1001 | 9.999999999999831 | 0.022799860938189802 | 1 | 0.38212731764290664 | unsettled | [record](../67-design-settings-ladders/evidence/exp02/science/repeat-851-s42/d8/record.json) at `0f91709000a4` |
| 1632/41 | d12 | 1001 | 9.999999999999831 | 0.08081264163459871 | 1 | 2.170905880839927 | settled | [record](../67-design-settings-ladders/evidence/exp02/science/repeat-1632-s41/d12/record.json) at `0f91709000a4` |
| 1632/41 | d2 | 1001 | 9.999999999999831 | 0.10048647826697461 | 0 | 0.2555525085391311 | unsettled | [record](../67-design-settings-ladders/evidence/exp02/science/repeat-1632-s41/d2/record.json) at `0f91709000a4` |
| 1632/41 | d4 | 1001 | 9.999999999999831 | 0.07386500305114937 | 1 | 0.13765341321298027 | settled | [record](../67-design-settings-ladders/evidence/exp02/science/repeat-1632-s41/d4/record.json) at `0f91709000a4` |
| 1632/41 | d6 | 1001 | 9.999999999999831 | 0.011827234768698413 | 1 | 0.11890223695663073 | unsettled | [record](../67-design-settings-ladders/evidence/exp02/science/repeat-1632-s41/d6/record.json) at `0f91709000a4` |
| 1632/41 | d8 | 1001 | 9.999999999999831 | 0.01715509046203649 | 1 | 0.1235521819128475 | settled | [record](../67-design-settings-ladders/evidence/exp02/science/repeat-1632-s41/d8/record.json) at `0f91709000a4` |

## EXP-03 learning-rate ladder

The registered prediction was learning-rate sensitivity: the fit's E changes across the rate ladder against the lr1e-4 control on the registered cases. [Committed prediction](../67-design-settings-ladders/67-EXP03-PREDICTION.md) at `0f91709000a4` · [Registered review](../67-design-settings-ladders/evidence/exp03/review.json) at `0f91709000a4`

Each arm used 155,100 updates. The registered rate-improvement hypothesis was refuted within this ladder. Constant 1e-3 confirmed worsening against 1e-4 on three settled pairs. The 1e-5 and 3e-4 contrasts were unsettled. The settled 3e-5 pairs disagreed by case and were ambiguous. The original DIAG-09 association remains retained.

| Arm | Control | Main 1632/42 | Repeat system 851/42 | Repeat seed 1632/41 | Registered reading |
|---|---|---|---|---|---|
| lr1e-3 | lr1e-4 | W ✓ | W ✓ | W ✓ | `confirmed-worsening` |
| lr1e-5 | lr1e-4 | W ✓ | W ✓ | W ✓ | `unsettled` |
| lr3e-4 | lr1e-4 | W ✓ | W ✓ | I ✓ | `unsettled` |
| lr3e-5 | lr1e-4 | W ✓ | W ✓ | I ✓ | `ambiguous` |

| System/seed | Arm | Samples | Window end | E | Tier | ε_H | Endpoint | Record |
|---|---|---|---|---|---|---|---|---|
| 1632/42 | lr1e-3 | 1001 | 9.999999999999831 | 1.4551508979130539 | 0 | 2920.7290554588394 | settled | [record](../67-design-settings-ladders/evidence/exp03/science/main-1632-s42/lr1e-3/record.json) at `0f91709000a4` |
| 1632/42 | lr1e-4 | 1001 | 9.999999999999831 | 0.040691019043637484 | 1 | 1.884224250407955 | settled | [record](../67-design-settings-ladders/evidence/exp03/science/main-1632-s42/lr1e-4/record.json) at `0f91709000a4` |
| 1632/42 | lr1e-5 | 1001 | 9.999999999999831 | 0.2097428875427889 | 0 | 24.516796802897684 | settled | [record](../67-design-settings-ladders/evidence/exp03/science/main-1632-s42/lr1e-5/record.json) at `0f91709000a4` |
| 1632/42 | lr3e-4 | 1001 | 9.999999999999831 | 1.3814863535666753 | 0 | 38.71866239878142 | settled | [record](../67-design-settings-ladders/evidence/exp03/science/main-1632-s42/lr3e-4/record.json) at `0f91709000a4` |
| 1632/42 | lr3e-5 | 1001 | 9.999999999999831 | 0.07747289529864392 | 1 | 2.2198196566511315 | settled | [record](../67-design-settings-ladders/evidence/exp03/science/main-1632-s42/lr3e-5/record.json) at `0f91709000a4` |
| 851/42 | lr1e-3 | 1001 | 9.999999999999831 | 1.5639231628850137 | 0 | 177.42477145294563 | settled | [record](../67-design-settings-ladders/evidence/exp03/science/repeat-851-s42/lr1e-3/record.json) at `0f91709000a4` |
| 851/42 | lr1e-4 | 1001 | 9.999999999999831 | 0.09549573839491703 | 1 | 4.801534852996827 | settled | [record](../67-design-settings-ladders/evidence/exp03/science/repeat-851-s42/lr1e-4/record.json) at `0f91709000a4` |
| 851/42 | lr1e-5 | 1001 | 9.999999999999831 | 0.21207523896683939 | 0 | 12.467165297317097 | settled | [record](../67-design-settings-ladders/evidence/exp03/science/repeat-851-s42/lr1e-5/record.json) at `0f91709000a4` |
| 851/42 | lr3e-4 | 1001 | 9.999999999999831 | 1.9228096305533615 | 0 | 524.9238100289732 | settled | [record](../67-design-settings-ladders/evidence/exp03/science/repeat-851-s42/lr3e-4/record.json) at `0f91709000a4` |
| 851/42 | lr3e-5 | 1001 | 9.999999999999831 | 0.22019943911402998 | 0 | 1.6130511963131093 | settled | [record](../67-design-settings-ladders/evidence/exp03/science/repeat-851-s42/lr3e-5/record.json) at `0f91709000a4` |
| 1632/41 | lr1e-3 | 1001 | 9.999999999999831 | 1.4024505668393392 | 0 | 72.81422878169708 | settled | [record](../67-design-settings-ladders/evidence/exp03/science/repeat-1632-s41/lr1e-3/record.json) at `0f91709000a4` |
| 1632/41 | lr1e-4 | 1001 | 9.999999999999831 | 0.03491785615016659 | 1 | 7.866109129043417 | settled | [record](../67-design-settings-ladders/evidence/exp03/science/repeat-1632-s41/lr1e-4/record.json) at `0f91709000a4` |
| 1632/41 | lr1e-5 | 1001 | 9.999999999999831 | 0.18744816464300104 | 0 | 70.99439302662817 | unsettled | [record](../67-design-settings-ladders/evidence/exp03/science/repeat-1632-s41/lr1e-5/record.json) at `0f91709000a4` |
| 1632/41 | lr3e-4 | 1001 | 9.999999999999831 | 0.017057375824979466 | 1 | 6.061345685052845 | unsettled | [record](../67-design-settings-ladders/evidence/exp03/science/repeat-1632-s41/lr3e-4/record.json) at `0f91709000a4` |
| 1632/41 | lr3e-5 | 1001 | 9.999999999999831 | 0.018883270414925272 | 1 | 0.9810821444560512 | settled | [record](../67-design-settings-ladders/evidence/exp03/science/repeat-1632-s41/lr3e-5/record.json) at `0f91709000a4` |

## EXP-04 time-input ladder

The registered prediction was the encoded harmonic input improves the fit: each encoded arm's E is below its own backbone's raw control's on all three registered cases. [Committed prediction](../67-design-settings-ladders/67-EXP04-PREDICTION.md) at `0f91709000a4` · [Registered review](../67-design-settings-ladders/evidence/exp04/review.json) at `0f91709000a4`

Each arm used 112,700 updates. All four harmonic contrasts against their own backbones were unsettled. Both smaller-network harmonic arms were worse on all three cases. The locked backbone’s direction depended on the case.

| Arm | Control | Main 1632/42 | Repeat system 851/42 | Repeat seed 1632/41 | Registered reading |
|---|---|---|---|---|---|
| exp01-f1 | exp01-raw | W ✓ | W ✓ | W ✓ | `unsettled` |
| exp01-f12 | exp01-raw | W ✓ | W ✓ | W ✓ | `unsettled` |
| locked-f1 | locked-raw | W ✓ | W ✓ | I ✓ | `unsettled` |
| locked-f12 | locked-raw | W ✓ | W ✓ | I | `unsettled` |

| System/seed | Arm | Samples | Window end | E | Tier | ε_H | Endpoint | Record |
|---|---|---|---|---|---|---|---|---|
| 1632/42 | exp01-f1 | 1001 | 9.999999999999831 | 0.07822251056763327 | 1 | 13.754342650396838 | settled | [record](../67-design-settings-ladders/evidence/exp04/science/main-1632-s42/exp01-f1/record.json) at `0f91709000a4` |
| 1632/42 | exp01-f12 | 1001 | 9.999999999999831 | 0.04955849067979028 | 1 | 6.7333592436844825 | unsettled | [record](../67-design-settings-ladders/evidence/exp04/science/main-1632-s42/exp01-f12/record.json) at `0f91709000a4` |
| 1632/42 | exp01-raw | 1001 | 9.999999999999831 | 0.011069594072166582 | 1 | 0.3856868153899165 | unsettled | [record](../67-design-settings-ladders/evidence/exp04/science/main-1632-s42/exp01-raw/record.json) at `0f91709000a4` |
| 1632/42 | locked-f1 | 1001 | 9.999999999999831 | 0.04615102941421912 | 1 | 99.96383776939349 | unsettled | [record](../67-design-settings-ladders/evidence/exp04/science/main-1632-s42/locked-f1/record.json) at `0f91709000a4` |
| 1632/42 | locked-f12 | 1001 | 9.999999999999831 | 0.06013616119727379 | 1 | 28.07713033949705 | settled | [record](../67-design-settings-ladders/evidence/exp04/science/main-1632-s42/locked-f12/record.json) at `0f91709000a4` |
| 1632/42 | locked-raw | 1001 | 9.999999999999831 | 0.0344080542047465 | 1 | 1.8464687298205864 | unsettled | [record](../67-design-settings-ladders/evidence/exp04/science/main-1632-s42/locked-raw/record.json) at `0f91709000a4` |
| 851/42 | exp01-f1 | 1001 | 9.999999999999831 | 0.14185020924126024 | 0 | 2.3000216403039033 | unsettled | [record](../67-design-settings-ladders/evidence/exp04/science/repeat-851-s42/exp01-f1/record.json) at `0f91709000a4` |
| 851/42 | exp01-f12 | 1001 | 9.999999999999831 | 0.15456749202685538 | 0 | 14.011953593667911 | settled | [record](../67-design-settings-ladders/evidence/exp04/science/repeat-851-s42/exp01-f12/record.json) at `0f91709000a4` |
| 851/42 | exp01-raw | 1001 | 9.999999999999831 | 0.07864043014323893 | 1 | 0.36457240999319457 | settled | [record](../67-design-settings-ladders/evidence/exp04/science/repeat-851-s42/exp01-raw/record.json) at `0f91709000a4` |
| 851/42 | locked-f1 | 1001 | 9.999999999999831 | 0.0710851362747344 | 1 | 28.105923557950906 | settled | [record](../67-design-settings-ladders/evidence/exp04/science/repeat-851-s42/locked-f1/record.json) at `0f91709000a4` |
| 851/42 | locked-f12 | 1001 | 9.999999999999831 | 0.061705123279830354 | 1 | 34.39525761361645 | settled | [record](../67-design-settings-ladders/evidence/exp04/science/repeat-851-s42/locked-f12/record.json) at `0f91709000a4` |
| 851/42 | locked-raw | 1001 | 9.999999999999831 | 0.04919948294071304 | 1 | 1.9098325862255108 | settled | [record](../67-design-settings-ladders/evidence/exp04/science/repeat-851-s42/locked-raw/record.json) at `0f91709000a4` |
| 1632/41 | exp01-f1 | 1001 | 9.999999999999831 | 0.04697019298545217 | 1 | 6.284006303612736 | unsettled | [record](../67-design-settings-ladders/evidence/exp04/science/repeat-1632-s41/exp01-f1/record.json) at `0f91709000a4` |
| 1632/41 | exp01-f12 | 1001 | 9.999999999999831 | 0.09316469672181629 | 1 | 6.190277329438445 | unsettled | [record](../67-design-settings-ladders/evidence/exp04/science/repeat-1632-s41/exp01-f12/record.json) at `0f91709000a4` |
| 1632/41 | exp01-raw | 1001 | 9.999999999999831 | 0.01763443846274973 | 1 | 0.19032648423519966 | settled | [record](../67-design-settings-ladders/evidence/exp04/science/repeat-1632-s41/exp01-raw/record.json) at `0f91709000a4` |
| 1632/41 | locked-f1 | 1001 | 9.999999999999831 | 0.023682017735151037 | 1 | 13.053754711807843 | settled | [record](../67-design-settings-ladders/evidence/exp04/science/repeat-1632-s41/locked-f1/record.json) at `0f91709000a4` |
| 1632/41 | locked-f12 | 1001 | 9.999999999999831 | 0.03895762366412014 | 1 | 8.775924940252512 | unsettled | [record](../67-design-settings-ladders/evidence/exp04/science/repeat-1632-s41/locked-f12/record.json) at `0f91709000a4` |
| 1632/41 | locked-raw | 1001 | 9.999999999999831 | 0.0412830122941967 | 1 | 15.243132763313138 | settled | [record](../67-design-settings-ladders/evidence/exp04/science/repeat-1632-s41/locked-raw/record.json) at `0f91709000a4` |

## EXP-05 window-length ladder

The registered prediction was a shorter window improves the fit: each shorter prefix arm's E is below the lap10 control's on all three registered cases. [Committed prediction](../67-design-settings-ladders/67-EXP05-PREDICTION.md) at `0f91709000a4` · [Registered review](../67-design-settings-ladders/evidence/exp05/review.json) at `0f91709000a4`

Each arm used 148,700 updates. The shorter signed-lap prefixes had lower E in all nine comparisons. Some endpoints remained unsettled and no contrast confirmed. A case can qualify through its tier change even when the relative E effect is below 20%.

| Arm | Control | Main 1632/42 | Repeat system 851/42 | Repeat seed 1632/41 | Registered reading |
|---|---|---|---|---|---|
| lap1 | lap10 | I ✓ | I ✓ | I ✓ | `unsettled` |
| lap2 | lap10 | I ✓ | I ✓ | I ✓ | `unsettled` |
| lap5 | lap10 | I ✓ | I ✓ | I ✓ | `unsettled` |

| System/seed | Arm | Samples | Window end | E | Tier | ε_H | Endpoint | Record |
|---|---|---|---|---|---|---|---|---|
| 1632/42 | lap1 | 96 | 0.9500000000000006 | 0.005407673830025773 | 1 | 0.72248822653622 | unsettled | [record](../67-design-settings-ladders/evidence/exp05/science/main-1632-s42/lap1/record.json) at `0f91709000a4` |
| 1632/42 | lap10 | 952 | 9.509999999999842 | 0.027243759954814768 | 1 | 2.779949963785304 | unsettled | [record](../67-design-settings-ladders/evidence/exp05/science/main-1632-s42/lap10/record.json) at `0f91709000a4` |
| 1632/42 | lap2 | 190 | 1.8900000000000015 | 0.015753288018634588 | 1 | 2.3401525358661597 | unsettled | [record](../67-design-settings-ladders/evidence/exp05/science/main-1632-s42/lap2/record.json) at `0f91709000a4` |
| 1632/42 | lap5 | 477 | 4.759999999999943 | 0.013948577928655764 | 1 | 10.146344851160096 | unsettled | [record](../67-design-settings-ladders/evidence/exp05/science/main-1632-s42/lap5/record.json) at `0f91709000a4` |
| 851/42 | lap1 | 55 | 0.5400000000000003 | 0.012315061236409686 | 1 | 0.7842946688789658 | settled | [record](../67-design-settings-ladders/evidence/exp05/science/repeat-851-s42/lap1/record.json) at `0f91709000a4` |
| 851/42 | lap10 | 538 | 5.36999999999993 | 0.03528830371107014 | 1 | 4.353531077264153 | unsettled | [record](../67-design-settings-ladders/evidence/exp05/science/repeat-851-s42/lap10/record.json) at `0f91709000a4` |
| 851/42 | lap2 | 109 | 1.0800000000000007 | 0.0041033828287498 | 1 | 0.7946819208473842 | unsettled | [record](../67-design-settings-ladders/evidence/exp05/science/repeat-851-s42/lap2/record.json) at `0f91709000a4` |
| 851/42 | lap5 | 269 | 2.679999999999987 | 0.01650364030491745 | 1 | 2.549706216490554 | unsettled | [record](../67-design-settings-ladders/evidence/exp05/science/repeat-851-s42/lap5/record.json) at `0f91709000a4` |
| 1632/41 | lap1 | 96 | 0.9500000000000006 | 0.015676362749794264 | 1 | 1.7745594867600087 | settled | [record](../67-design-settings-ladders/evidence/exp05/science/repeat-1632-s41/lap1/record.json) at `0f91709000a4` |
| 1632/41 | lap10 | 952 | 9.509999999999842 | 0.11465182676222399 | 0 | 16.82295313516749 | settled | [record](../67-design-settings-ladders/evidence/exp05/science/repeat-1632-s41/lap10/record.json) at `0f91709000a4` |
| 1632/41 | lap2 | 190 | 1.8900000000000015 | 0.09900171619123573 | 1 | 39.01542367416107 | settled | [record](../67-design-settings-ladders/evidence/exp05/science/repeat-1632-s41/lap2/record.json) at `0f91709000a4` |
| 1632/41 | lap5 | 477 | 4.759999999999943 | 0.036324687262097394 | 1 | 5.822916138548797 | settled | [record](../67-design-settings-ladders/evidence/exp05/science/repeat-1632-s41/lap5/record.json) at `0f91709000a4` |

The ladder evidence applies to the registered orbits and budgets. Each linked run record retains the same-window constant and two-Kepler baselines, where applicable, along with position horizons and similarity traces.

## Yardstick and current owner ruling

The known-answer expectation was for Brutus’s recorded trajectory to pass and for a static predictor to fail the accuracy checks. The frozen explicit-velocity position grades met that expectation. The production finite-difference energy gate rejected Brutus and accepted the static predictor. The two finite-difference routes use the same samples within each grid. [Committed yardstick audit](../68-yardstick/evidence/yardstick-audit.json) at `0f91709000a4` · [Committed audit interpretation](../68-yardstick/68-AUDIT.md) at `0f91709000a4`

| System | Grid | Prediction | Samples | Explicit E / tier | Explicit ε_H | FD native ε_H / verdict | FD float32-input ε_H / verdict |
|---|---|---|---|---|---|---|---|
| 1632 | base | brutus | 125 | 0.0 / 3 | 1.1440860870054439e-14 | 0.04707916601467425 / FAIL | 0.04707930493790348 / FAIL |
| 1632 | base | window_mean_constant | 125 | 1.151562120989809 / 0 | 0.0 | 0.0 / PASS | 0.0 / PASS |
| 1632 | gold | brutus | 1001 | 0.0 / 3 | 3.4352972396849396e-12 | 0.0010895525002158342 / FAIL | 0.0011350563563030777 / FAIL |
| 1632 | gold | window_mean_constant | 1001 | 1.1538408194255343 / 0 | 0.0 | 0.0 / PASS | 0.0 / PASS |
| 851 | base | brutus | 125 | 0.0 / 3 | 1.8768864216679452e-14 | 0.20458554440424515 / FAIL | 0.2045854124681413 / FAIL |
| 851 | base | window_mean_constant | 125 | 1.2381183188852325 / 0 | 0.0 | 0.0 / PASS | 0.0 / PASS |
| 851 | gold | brutus | 1001 | 0.0 / 3 | 2.170101384887484e-11 | 0.0034423088343345566 / FAIL | 0.003448819505592303 / FAIL |
| 851 | gold | window_mean_constant | 1001 | 1.233696866477104 / 0 | 0.0 | 0.0 / PASS | 0.0 / PASS |
| 4658 | base | brutus | 125 | 0.0 / 3 | 1.6215598050713573e-14 | 0.37899778680724633 / FAIL | 0.3790000386863116 / FAIL |
| 4658 | base | window_mean_constant | 125 | 1.1460238197509678 / 0 | 0.0 | 0.0 / PASS | 0.0 / PASS |
| 4658 | gold | brutus | 1001 | 0.0 / 3 | 9.150401922247111e-12 | 0.023797298497379084 / FAIL | 0.02379455667088198 / FAIL |
| 4658 | gold | window_mean_constant | 1001 | 1.1395956985717504 / 0 | 0.0 | 0.0 / PASS | 0.0 / PASS |

| Grid | Prediction | FD route | Panel ε_H | SCS | Gate |
|---|---|---|---|---|---|
| base | brutus | native_float64 | 0.37899778680724633 | -0.42136332612745997 | FAIL |
| base | brutus | float32_input | 0.3790000386863116 | -0.4213607457014506 | FAIL |
| base | window_mean_constant | native_float64 | 0.0 | -Infinity | PASS |
| base | window_mean_constant | float32_input | 0.0 | -Infinity | PASS |
| gold | brutus | native_float64 | 0.023797298497379084 | -1.6234723418625197 | FAIL |
| gold | brutus | float32_input | 0.02379455667088198 | -1.6235223823627327 | FAIL |
| gold | window_mean_constant | native_float64 | 0.0 | -Infinity | PASS |
| gold | window_mean_constant | float32_input | 0.0 | -Infinity | PASS |

The static predictor has constant potential energy and zero velocity. Its energy drift vanishes while its positions are wrong. The audit confirms the velocity measurement defect and the need for a separate position criterion. The defect concerns evaluation. The historical failed fits optimized only their position targets.

The later C-7 A ruling chooses autograd velocities in the validation gate and evaluator and closes GAP-59-08. The implementation and the architecture-spec amendment go to v2.6. C-2, C-4, C-5 and C-6 remain open. The C-11 evaluation-text rewrite also goes to v2.6. [Phase 68 owner ruling](../68-yardstick/68-CHECKPOINT-2-RULING.md) at `0f91709000a4`

[Findings](69-FINDINGS.md) · [Cost and scope decisions](69-ACCOUNTING.md) · [Owner packet](69-CHECKPOINT.md)
