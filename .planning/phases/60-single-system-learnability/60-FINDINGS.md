# Phase 60 Findings: Single-System Learnability

**Audience: the project owner, a non-specialist.**
**Run protocol:** SHA-256 `93486d240f129bb5947cddb56d2eb18936ac0cbad7ac0bceeb0af0372b850383` (sealed before any arm ran; every record cites it).
**Scorecard:** SHA-256 `f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b` (frozen in Phase 59, before any result).

Every number below is copied from a committed file named on this page. Almost all come from the evidence files listed in the evidence index at the end; the plan's estimates and the launcher's clock times come from the planning documents named beside them. Prose rounds for readability; the exact value is in the named file. This page reports measurements. It does not state the project's verdict: Phase 64 owns that.

## In plain language

Think of the project's experiments as a ladder of exams, each harder than the last, where a failed exam stops the climb. Rung 1 is the easiest exam: the network is trained on a real Stage-0 orbit together with the correct answer, then asked to reproduce that same orbit. If it cannot, the harder exams (learning the orbit from the physics alone) are not worth running. Gate G2 is the rule, agreed before any result, that says when to stop.

1. **At the locked setting, the network did not reproduce any of the three orbits.** The orbits are systems 1632, 851 and 4658, the three Phase 59 chose to span the Stage-0 difficulty range (10.47, 18.61 and 39.35 inner-pair laps in the 10-unit window). Each was trained once, for 2.57 to 5.69 hours, and each ended at **Tier 0**. A *tier* is the scorecard's grade for a prediction, and Tier 1 is the lowest passing grade. Tier 1 needs **E**, the worst position error over the window as a fraction of the system's size, to be at most 0.1 (10%). The three runs ended with E of 1.1574, 1.2375 and 1.1432, about 11 to 12 times over the line. An E near 1 means the prediction is off by about as much as the scale of the inner orbit itself. The **valid horizon**, the fraction of the window before the error first exceeds 1% (or 10%), was 0.0 at both limits on all three: the prediction was already outside both at the first scored time.
2. **Gate G2 fired.** The rule fires when two or more of the three systems end below Tier 1. All three did.
3. **There was no rescue.** The rule then tries one pre-agreed fix: four other values (60, 120, 240 and 480) of the network's first-layer frequency setting, on one system, 1632. The project locked that setting at 30. All four also ended at Tier 0, with E between 1.1539 and 1.1575. The locked setting had given 1.1574 on the same system, so across a 16-fold range of the setting the error did not move. A rescue needed at least one setting to reach Tier 1. None did, so there was nothing to confirm on system 851, and the owner was not asked at checkpoint 4 (the stop that asks whether to continue at a new setting).
4. **Can the network learn the orbit from the physics alone? Not tested.** Rung 2, which would ask this, is recorded as "skipped at G2: no rescue". The project's readiness ladder calls this capability Level 3 ("learns one system"). It is recorded as "not tested (skipped at G2)". The wording is deliberate: it does not say the network failed this exam, because the exam was never given.
5. **What the hard-stage probes show: nothing.** The two probes (one Stage-4b and one Stage-6 system) were skipped for the same reason, "no rescue". This phase says nothing about the hard stages.
6. **What this does and does not decide.** It shows, from one training run per setting, that this network trained this way for hours on an orbit it is shown does not come within the Tier-1 line of that orbit. That holds for three orbits at the locked setting and for one orbit at four other settings. It does not say why. The records show how the runs ended, not whether the cause lies in the network's design, the training recipe or something else. It does not test learning from the physics. It does not decide what the project does next. The decision rule frozen in Phase 59, given only "G2 fired and the sweep rescued nothing", returns the label RETHINK-REPRESENTATION. That is the pre-registered rule's output on these inputs, recorded in the handoff file. It is not a Phase 60 verdict: Phase 64 states and confirms the verdict, and you decide what follows.
7. **What it cost.** 22.378 machine hours across the seven training arms: 11.108 hours for Rung 1 and 11.270 hours for the sweep. The plan's estimate for this path was about 30 hours (eight arms at 3.75 hours each, `60-CONTEXT.md`). Seven arms ran, because there was no confirmation run. Six took 2.57 to 3.05 hours each. The seventh, r1-4658, took 5.69 hours because it earned its one doubling.
8. **What comes next.** Phase 64, the feasibility verdict, is next. It reads `evidence/g2/stop-handoff.json`. Phases 61 to 63 were not run. They are marked "skipped at G2 (no rescue), not failed", and they are not next.
9. **How it was checked.** Every result was re-scored from its committed weights, never retrained, on all seven arms: on the CPU in double precision and on the GPU in single precision. Every re-score matched the record (RESCORE-OK): the CPU re-score to within 1e-12, the GPU re-score on tier and counts. The evidence verifier passes (PHASE60-EVIDENCE-OK). The check that does the re-scoring crashed on its first real use during the closeout, was repaired and then re-run. The details are under Limits.

## Rung 1

**What ran.** Each arm trains the project's production network on the hierarchical gold record of one system (output step 0.01, 1,001 points) with the data term only. It uses the locked first-layer setting 30, seed 42, on this Mac's GPU (MPS, single precision). Training has two parts. Adam runs for a step budget sized so that Adam takes about 3 hours (the frozen cap, from a 500-step timing run). Then a short full-batch L-BFGS polish runs. Both end states are scored on that same gold grid, and the better one by the scorecard's rule (lowest E, then lowest energy drift) is the arm's official result. The coarser 0.08 base-grid scores beside it are also Tier 0 on every arm. A second scoring in double precision on the CPU agreed with the GPU score on tier and counts for both states of every arm. Source: `evidence/arms/r1-1632/record.json`, `r1-851/record.json`, `r1-4658/record.json`.

**Result per arm** (official state, gold grid). eps_H is the largest relative energy drift along the predicted path (Tier 2 would need at most 0.001). Inner laps are from Phase 59's `panels.json`, and the formula's E from Phase 59's `two_kepler.json` (both are in the evidence index).

| Arm | System | Inner laps | Tier | E | eps_H | Valid horizon at 1% / 10% | Better state | Budget outcome | Counts against the formula |
|---|---|---|---|---|---|---|---|---|---|
| r1-1632 | 1632 | 10.47 | 0 | 1.1574 | 705.69 | 0.0 / 0.0 | polish | complete | no (Tier 0; formula E 0.9168) |
| r1-851 | 851 | 18.61 | 0 | 1.2375 | 165.5 | 0.0 / 0.0 | adam | complete | no (Tier 0; formula E 0.4312) |
| r1-4658 | 4658 | 39.35 | 0 | 1.1432 | 13128 | 0.0 / 0.0 | adam | complete | no (Tier 0; formula E 1.9697) |

**Both optimizer states** (gold grid; tier / E / eps_H).

| Arm | Adam | Polish | Polish outer calls | CPU double-precision cross-check |
|---|---|---|---|---|
| r1-1632 | 0 / 1.1606 / 30.295 | 0 / 1.1574 / 705.69 | 6 | agrees on tier and counts |
| r1-851 | 0 / 1.2375 / 165.5 | 0 / 1.2384 / 176.65 | 7 | agrees on tier and counts |
| r1-4658 | 0 / 1.1432 / 13128 | 0 / 1.1439 / 362.02 | 6 | agrees on tier and counts |

**Against the textbook formula.** The two-Kepler formula (Phase 59) scores E 0.9168, 0.4312 and 1.9697 on these three systems (`formula.E_formula` in each record). A system counts only if the network reaches Tier 1 and its E is strictly below the formula's. None did, so Rung 1 counts on 0 of 3 systems. On system 4658 the network's E (1.1432) is numerically below the formula's (1.9697), but at Tier 0 it does not count.

**Other facts from the records.**
- **Polish moved little.** It was the better state only for r1-1632 (E 1.1574 against Adam's 1.1606). On every arm, in Rung 1 and in the sweep, the polish ended on the frozen stop "5 outer calls in a row without a lower objective", within 4.4 to 5.4 seconds.
- **The third arm earned its one doubling and gained nothing.** The frozen "still improving" test granted r1-4658 one doubling of its budget (record: `extended` true, 980,623 steps doubled to 1,961,246). Its E was 1.1427 at step 980,623 and 1.1432 at step 1,961,246. The other two Rung-1 arms were not extended.
- **The error sits in a narrow band although the orbits differ.** E is 1.14 to 1.24 on three systems whose inner-lap counts differ by a factor of about 3.8. This is a measured fact only. What it implies is not decided here.

## Gate G2

**What the gate asks.** Whether one locked setting, rather than the network's design, is the bottleneck. The rule fires when two or more of the three Rung-1 systems end below Tier 1. If it fires, it tries four fixed values of the first-layer frequency setting on one failing system, and counts a setting only if its arm reaches Tier 1.

**What happened.** The tiers in panel order (1632, 851, 4658) were 0, 0, 0, so the gate fired (`evidence/g2/g2-outcome.json`: `g2_fired` true, trigger "below Tier 1"). The lap counts then fix the pair the rule uses: the sweep ran on 1632, the failing system with the fewest inner laps (10.47). A confirmation would have run once on 851, the next one. System 4658 is the "uncovered" system, which would have got one data-only run only if the owner had continued after a confirmed rescue.

**The sweep on system 1632.** One run per setting, in grid order, each with the same seed, budget rule and polish as Rung 1. The first row is Rung 1's own result at the locked setting, shown for comparison. The other four rows are `evidence/g2/sweep-curve.json` (outcome `no_rescue`), and each equals its arm's record.

| first_omega_0 | Arm | Tier | E | eps_H | Valid horizon at 1% / 10% | Better state | Budget outcome | Label in sweep-curve.json |
|---|---|---|---|---|---|---|---|---|
| 30 (locked) | r1-1632 | 0 | 1.1574 | 705.69 | 0.0 / 0.0 | polish | complete | Rung 1 result, not a sweep row |
| 60 | g2s-1632-w060 | 0 | 1.1569 | 4052.3 | 0.0 / 0.0 | adam | complete | below Tier 1 |
| 120 | g2s-1632-w120 | 0 | 1.1561 | 1342.9 | 0.0 / 0.0 | adam | complete | below Tier 1 |
| 240 | g2s-1632-w240 | 0 | 1.1539 | 123.62 | 0.0 / 0.0 | adam | complete | below Tier 1 |
| 480 | g2s-1632-w480 | 0 | 1.1575 | 4170.1 | 0.0 / 0.0 | adam | complete | below Tier 1 |

**Both optimizer states for the sweep arms** (gold grid; tier / E / eps_H).

| Arm | Adam | Polish | Polish outer calls | CPU double-precision cross-check |
|---|---|---|---|---|
| g2s-1632-w060 | 0 / 1.1569 / 4052.3 | 0 / 1.1587 / 293.17 | 7 | agrees on tier and counts |
| g2s-1632-w120 | 0 / 1.1561 / 1342.9 | 0 / 1.1580 / 2452.9 | 6 | agrees on tier and counts |
| g2s-1632-w240 | 0 / 1.1539 / 123.62 | 0 / 1.1588 / 117.99 | 6 | agrees on tier and counts |
| g2s-1632-w480 | 0 / 1.1575 / 4170.1 | 0 / 1.1576 / 431.61 | 6 | agrees on tier and counts |

**Reading.** No setting reached Tier 1, on any of the five values tried on system 1632 (30, 60, 120, 240, 480). The sweep's E spans 1.1539 to 1.1575, a spread of 0.0036, and the locked setting gave 1.1574. The energy drift differs by a factor of about 34 between settings (123.62 at 240, 4170.1 at 480) but is far above the Tier-2 line (0.001) in every arm. None of the four sweep arms counts against the formula (E 0.9168 on this system; the network's E is higher in all four, and all are Tier 0). No sweep arm was extended, and none diverged.

**No confirmation, no checkpoint 4.** The curve records `confirmation_arm` null and `confirmed_first_omega_0` null, so the confirmation run on system 851 was not run. With no rescue there was no checkpoint 4: the owner was not asked whether to continue, `learnability_g2 branch owner-decision` prints "BRANCH-NOT-TAKEN: owner-decision (no rescue: no sweep setting reached Tier 1)", and no ruling file exists. GAP-60-09, a confirmation that ends below Tier 1, did not arise.

**What the gate recorded.** `evidence/g2/skip-records.json` records Rung 2 (FEAS-04) and the probes (FEAS-09) as skipped, both with the reason "no rescue", and Level 3 as "not tested (skipped at G2)". `evidence/g2/stop-handoff.json` is the handoff to Phase 64. It holds the frozen rule's output for the inputs "G2 fired and the sweep rescued nothing" and no later-rung inputs: RETHINK-REPRESENTATION, with the reason "G2 fired and the sweep rescued nothing". It also records Phases 61 to 63 as "skipped at G2, not failed", the next phase as 64, and the per-arm hours below. That label is the pre-registered rule's output. It is not a Phase 60 verdict.

## Rung 2

**Skipped at G2: no rescue.** Rung 2 (learning the orbit from the physics, in two forms, on the three systems) runs only if the ladder continues past G2. It did not, so no Rung-2 arm was started. `evidence/g2/skip-records.json` holds FEAS-04 as skipped with the exact pre-registered reason "no rescue". There is therefore no Rung-2 comparison with Rung 1 or with the formula, and Level 3 ("learns one system") reads "not tested (skipped at G2)".

## Hard-stage probes

**Skipped at G2: no rescue.** The two probes (FEAS-09) run only if the ladder continues past G2. `evidence/g2/skip-records.json` holds FEAS-09 as skipped with the reason "no rescue". The probe systems that Phase 59's pre-declared rule picked (its `picks.json`, in the evidence index), `standard/base/2279` (Stage 4b) and `standard/base/3418` (Stage 6), were not trained or scored in this phase. Nothing is reported about the hard stages.

## Machine hours

Wall hours are each record's `wall.hours`: the whole arm, from start to finish. Adam and polish seconds are the record's `wall.adam_seconds` and `wall.polish_seconds`. The arm total exceeds their sum by 12 to 14 seconds, which is other work inside the arm that the record does not itemize. The timed seconds per step come from each arm's 500-step timing run (`timing.seconds_per_step`), which sizes the Adam budget. Every arm ran in one launch with no pause or governed stop (`launch.invocations` 1, `launch.stops` empty).

| Arm | Wall hours | Adam s + polish s | Timed seconds per step | Adam step budget | Budget outcome | Invocations / governed stops |
|---|---|---|---|---|---|---|
| r1-1632 | 2.573 | 9244.82 + 4.44 | 0.013596 | 794,350 | complete | 1 / 0 |
| r1-851 | 2.842 | 10215.56 + 4.79 | 0.011015 | 980,523 | complete | 1 / 0 |
| r1-4658 | 5.693 | 20475.93 + 4.50 | 0.011013 | 980,623, doubled once to 1,961,246 | complete | 1 / 0 |
| g2s-1632-w060 | 2.730 | 9808.86 + 4.96 | 0.011893 | 908,063 | complete | 1 / 0 |
| g2s-1632-w120 | 2.903 | 10435.62 + 4.40 | 0.011303 | 955,466 | complete | 1 / 0 |
| g2s-1632-w240 | 3.046 | 10946.28 + 5.44 | 0.010856 | 994,807 | complete | 1 / 0 |
| g2s-1632-w480 | 2.591 | 9311.03 + 4.49 | 0.012815 | 842,770 | complete | 1 / 0 |
| **Total** | **22.378** | | | | | 7 / 0 |

- **Totals.** Rung 1 took 11.108 hours, the sweep 11.270 hours, 22.37828873402778 in all (`evidence/g2/stop-handoff.json`, `total_wall_hours`; it equals the sum of the seven records).
- **Against the plan.** The plan expected about 3.75 hours per arm (3 hours of Adam plus up to 45 minutes of polish). Six arms took 2.57 to 3.05 hours, and the doubled arm took 5.69. Two reasons, both visible in the table. Each Adam budget is sized from a 500-step timing run, and the sustained rate (Adam seconds divided by steps run) came out between 0.0104 and 0.0116 seconds per step, faster than the timed rate on six of seven arms (slower only on g2s-1632-w240, 0.011003 against 0.010856). And each polish stopped in 4.4 to 5.4 seconds instead of running to its 25% cap. One arm, g2s-1632-w240, ran 1.4% over the 3-hour sizing target (Adam 10,946 s against 10,800 s), because its sustained rate was slower than its timed rate. The budget rule sizes the step count from the timing run and does not enforce wall time.
- **The timing runs themselves** (5.4 to 6.8 seconds each) are outside the arm totals.
- **Calendar time.** Rung 1 ran from 2026-10-21 21:29 to 2026-10-22 08:35 CDT, and the sweep from 2026-10-22 12:01 to 23:18 CDT, one arm at a time (launcher times in `60-14-SUMMARY.md` and `60-15-SUMMARY.md`).

## Limits

- **Only one seed per arm.** Every arm ran once, with seed 42, and the first completed run is the result. One seed cannot separate luck from capability. This is a stated limit for the verdict, not a reason to add seeds: no second seed, second confirmation or restart was run, and none is proposed here.
- **D-04, the low-rate tail.** Every data-only arm uses the Stage-0 cosine learning-rate schedule (`k = 0`), so the 75%-100% window of the frozen "still improving" test is the low-rate tail of that cosine (the readout note stored in every record). The test that decided whether to extend an arm therefore looked at the part of training where the learning rate is smallest. Only r1-4658 earned the doubling, and it gained nothing.
- **D-05, the from-scratch confound.** This note applies to the probe Rung-2b arms. Their learning rate would use their own stage's value, and the 0.7-per-stage factor behind that value assumes weights carried forward from the previous stage, but the probes start from scratch. No probe arm ran, so the confound affected no result here. It stays on the record for any later probe.
- **The R_ref in force.** The governed Stage-0 reference, `pinn/verification/artifacts/r_ref_stage0.json` (value 19749775821.24417, SHA-256 `c3a14924524ec94ad633d7dabe1027d277ba2c1c94d74ad01af2c448b50d73ff`, as pinned in `evidence/run-protocol.json`), applied unchanged. It was not re-measured, because the re-measure happens only after an owner continue at checkpoint 4. No physics arm ran, so it played no part in any result.
- **Five settings only, on one system.** The first-layer setting was tried at 30 on all three systems and at 60, 120, 240 and 480 on system 1632 alone. No value between or beyond those was tried, and no other knob was varied.
- **The orbit is scored on the record it was trained on.** Rung 1 asks whether the network can fit an orbit it is shown, scored on that same orbit. It does not ask whether the network can predict an orbit it has not seen. A fail, as here, is a failure to fit the orbit it was given.
- **No validation or test data.** Every record's attestation shows zero test-split opens and zero validation opens (`attestation.test_split_opened` 0 and `attestation.opened.validation` 0 on all seven arms). Nothing in this phase was run on the validation or test splits.
- **Timing was measured under memory pressure.** The plan asked for 6 GiB of free memory before each long arm. The arms ran with about 3.9 to 5.3 GiB free and about 5 to 10 GB of swap in use, and the owner waived the figure (`60-14-SUMMARY.md`, `60-15-SUMMARY.md`). Whether swap use slowed the runs was not measured, so the seconds-per-step figures carry that caveat.
- **The closeout checks had two first-use failures, both repaired.** The evidence verifier is checking code that had never run on real artifacts.
  - Its sweep-curve check crashed on the first real curve (wave 15). It called a pinned function with the wrong argument shapes. Commit `e3841c73` fixed it with three regression tests.
  - Its re-scoring check, `rescore --all`, crashed on its first real use during this closeout, within a second, with the error "'DataContext' object does not support the context manager protocol". Three defects sat behind that one error: it used the data context as a context manager although it is a plain object; it read the test-split counter from the wrong attribute; and its GPU half called `.to()` on arrays that are NumPy arrays, not tensors. Its unit test had hidden all three by mocking the context. Commit `2ca6a821` fixed all three and rewrote that test to use real objects. It added three tests, and all four failed with the real error before the fix. The repaired check then passed on all seven arms (RESCORE-OK, 53 seconds).
  - The verifier is not one of the 33 files the sealed protocol pins, and neither repair changed a recorded number or any pinned file.
  - The verifier's rescue check, which runs only if a sweep setting reaches Tier 1, has still never run on a real rescue, because none occurred. That branch is covered by tests only.

## Evidence index

Every file below is committed. Paths are relative to `.planning/phases/60-single-system-learnability/` unless they start with `pinn/`. The commands are run from the project root with `python -B`; the verifier is `evidence/verify_phase60_evidence.py`.

**Sealed inputs.**

| What | Path | SHA-256 | Checked by |
|---|---|---|---|
| Run protocol | `evidence/run-protocol.json` | `93486d240f129bb5947cddb56d2eb18936ac0cbad7ac0bceeb0af0372b850383` | `verify_phase60_evidence.py protocol` |
| Plain-language twin of the protocol | `60-RUN-PROTOCOL.md` | `d5d4298ca380b84b46f03300d7b33f70d65e8f630a44eecd61a1e4b4dafa8cd4` | `verify_phase60_evidence.py protocol` (tracked, clean, cites the protocol SHA-256) |
| Preflight records | `evidence/preflight/records.json` | `7f4fffe8702da3da8307582310221ccc0d4b1abab1156dd48b2c6103c89892cd` | `verify_phase60_evidence.py protocol`, `preflight` |
| Scorer successor record | `evidence/scorer-successor.json` | `feee49e33f2fb975bab5ea929e01062e527bf3015454101e5a51f1fafe17c882` | `verify_phase60_evidence.py protocol`, `records` |
| Frozen scorecard | `pinn/verification/artifacts/feasibility_scorecard_v1.json` | `f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b` | `verify_phase60_evidence.py protocol` |
| Scorer | `pinn/verification/feasibility_scorer.py` | `00edf81d59396fe189d476dd3e69473c4291b71bc6af6171da758f68b61f2bc7` | `verify_phase60_evidence.py protocol`, `records` |
| Stage-0 reference R_ref | `pinn/verification/artifacts/r_ref_stage0.json` | `c3a14924524ec94ad633d7dabe1027d277ba2c1c94d74ad01af2c448b50d73ff` | `verify_phase60_evidence.py protocol` |

**Arm records** (each next to its two weights files).

| Arm | Record path | SHA-256 | Checked by |
|---|---|---|---|
| r1-1632 | `evidence/arms/r1-1632/record.json` | `a87273674785128714f5eae4981dcee31fe4c2332dbd84213b7aeaa0098da0b7` | `verify_phase60_evidence.py records`, `rescore --all` |
| r1-851 | `evidence/arms/r1-851/record.json` | `3152470de1b34f8e1aa4fe3c0a7f825c32da385eb7636db56a92da50a88baa8a` | `verify_phase60_evidence.py records`, `rescore --all` |
| r1-4658 | `evidence/arms/r1-4658/record.json` | `dbba558ab41b9b1ba080b8346fc4834dcd0987e046d151a4d443a8e5d94f1ab8` | `verify_phase60_evidence.py records`, `rescore --all` |
| g2s-1632-w060 | `evidence/arms/g2s-1632-w060/record.json` | `cf1bc1fac780c21e26c917f4573c4845ccd36ed88136e23658f5a0eb5c960c42` | `verify_phase60_evidence.py records`, `rescore --all` |
| g2s-1632-w120 | `evidence/arms/g2s-1632-w120/record.json` | `893cbcefbda4c8cb061071c6d12044620112750644d68987a3b57d55ea245900` | `verify_phase60_evidence.py records`, `rescore --all` |
| g2s-1632-w240 | `evidence/arms/g2s-1632-w240/record.json` | `391e3f1728b3de287849ca4a7e48ae17da92e8ca48c8f77562caf377d56e4ca1` | `verify_phase60_evidence.py records`, `rescore --all` |
| g2s-1632-w480 | `evidence/arms/g2s-1632-w480/record.json` | `b75905c954728001c27a4f9c649281feb7f404358d88a2cdd58822d94909639e` | `verify_phase60_evidence.py records`, `rescore --all` |

**Weights files** (SHA-256 of `adam.weights` and `polish.weights` in each arm directory, as stored in the record; `rescore --all` re-scores both).

| Arm | adam.weights | polish.weights |
|---|---|---|
| r1-1632 | `5bc35136eee394e8d8354a110f6c874349407e97d0bac5921d5cb52f449ce6f5` | `d0521ed6a09cf5125d52fdcbd08b50d19f4251bacab3a5bd4937976ca5a68a35` |
| r1-851 | `1bb833d36b0d8b28ff0935c37c31f1bff3885c678eee0cf36face6f97bff499d` | `8ca92cf5cf1a15a58c027bc8ce38ee0aad470fed330a1008a9e1bf570f52bdb5` |
| r1-4658 | `9c46d15b62e15f0ea31d09d652456f7a487243a5fcc3623ebc1b50ebccfbee89` | `526ab72a9ac08f34bb2801d005f064c83e4cac4c44dc965c8387fba9f457b19b` |
| g2s-1632-w060 | `495272c7d08db11d9e1d516bff9f86b3e3ad90213200dc5a73a41c2a7975907a` | `4ad5877a9c609e02718930943dcfaf51e96ab3833bb1aa58aa98f7240df34853` |
| g2s-1632-w120 | `2cb70b1595521f0d541ac5b308b954cf425a3e8f875a308c9390cf8008d58e92` | `dd82999cf2ff90cf76dec1f0b282760abd5f33f5de37bf348769a1156c45312d` |
| g2s-1632-w240 | `14f8530b4dca31d183c2890e9ca0ed4c012532c33e3526d505aa27018b630959` | `0628b1578f9fe8ff7b58dbde25aaba8b3793741104245d6b638d88b286b329cd` |
| g2s-1632-w480 | `22f132cd1585013846765f448da9d89d5d23bb4133ae9852fbf3a8594ae7be40` | `f74f1f30bcecd2e79faffb4057947a8980933e64e1d4006082698f1a62a3ed20` |

**Gate G2 files.**

| File | Path | SHA-256 | Checked by |
|---|---|---|---|
| G2 outcome | `evidence/g2/g2-outcome.json` | `3e71568fe6d243f16dc930c7b8d49d028967b625e134cf5ba52d4c48b579c529` | `verify_phase60_evidence.py g2` |
| Sweep curve | `evidence/g2/sweep-curve.json` | `946c0bb9a658f287f074c8768c4cd4a54333df9c7303445fd5d64a5a347706bc` | `verify_phase60_evidence.py g2` |
| Skip records | `evidence/g2/skip-records.json` | `e15ad37d95e452637014f18c0eeb5d1795589717b6b82af14691bc3edd580bf8` | `verify_phase60_evidence.py g2` |
| Phase 64 handoff | `evidence/g2/stop-handoff.json` | `7ed8223c066e62bd55e527dc703565367a0f9764a253e086a3bc0b4e719d02d5` | `verify_phase60_evidence.py g2` |

**Phase 59 files cited by this page** (full paths from the project root; Phase 59 verifies them, see the last row below).

| What | Path | SHA-256 |
|---|---|---|
| Panels (inner laps of the three systems) | `.planning/phases/59-read-only-baseline-scorecard/evidence/census/panels.json` | `56ad5185148fca7e72b21f4fc1dbaaaf8eea7aa9ecdf498653af98ad88d6aa92` |
| Two-Kepler formula scores (source of `formula.E_formula`) | `.planning/phases/59-read-only-baseline-scorecard/evidence/baselines/two_kepler.json` | `05a347a65e01ea6a9cde1c6cff4b53d0d17333db9c3672a460931e2323b4c80e` |
| Hard-stage probe picks | `.planning/phases/59-read-only-baseline-scorecard/evidence/survey/picks.json` | `b6836d5095edc12b9b7af873bfd5b6cb82fdeeb2e5c34e1c75b608810cda7317` |

**Verifier and test results at close.** Logs are retained outside the repository and are not committed.

| Command | Result |
|---|---|
| `verify_phase60_evidence.py final` | PROTOCOL-OK, PREFLIGHT-OK, RECORDS-OK, G2-OK, PHASE60-EVIDENCE-OK; exit 0, 1.291 s, at commit `2ca6a821` |
| `verify_phase60_evidence.py rescore --all` (run once, detached) | RESCORE-OK, EXIT=0, 53 s (21:33:13Z to 21:34:06Z on 2026-10-23), after the repair. Both states of all seven arms: weights hashes and tensor digests match; the CPU double-precision re-score equals the recorded cross-check within 1e-12; the GPU single-precision re-score gives the recorded tier and counts. Nothing was retrained. Log: `$HOME/.cache/3bp-phase60-logs/phase60-rescore-60-22.log`. The first attempt, before the repair, failed within a second. |
| `python -B -m unittest discover -s tests/phase60 -t . -v` | At `2ca6a821`: Ran 992 tests in 787.906 s, OK (skipped=1, the platform probe that skips by design). Before the verifier repair, at `e6ff187d`: Ran 989 tests in 789.861 s, OK (skipped=1). About 13 minutes: the "under about 60 s" estimate in the plan and in `60-VALIDATION.md` is stale. |
| Nine scorer-dependent Phase 59 suites | Ran 139 tests in 29.819 s, OK, none skipped |
| `tests.phase39.test_prohibitions` and the four named `tests.phase38.test_prohibitions` tests | Ran 35 tests in 1.675 s, OK. The other two Phase 38 tests (`test_spec_byte_identity_endpoint_sha256`, `test_spec_history_no_touch_since_phase_base`) fail at this commit for an unrelated, pre-existing reason (stale spec byte checks) and are not part of the gate. |
| Phase 59 `verify_phase59_evidence.py final` | Reused, not re-run: PHASE59-EVIDENCE-OK, ELAPSED=604, EXIT=0 at commit `4df5d4a8` (`$HOME/.cache/3bp-phase60-logs/phase59-final-60-04.log`). Valid because `git diff --quiet 4df5d4a8 HEAD` over Phase 59's evidence, producer modules, scorer, scorecard and artifacts exits 0. |
