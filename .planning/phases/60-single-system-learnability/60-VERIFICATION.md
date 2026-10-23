---
phase: 60-single-system-learnability
verified: 2026-10-23T22:50:15Z
status: passed
score: 5/5 success criteria met
verifier: gsd-verifier (independent pass)
head: 93cb1bcf66eb9be4c942aa7e117d022103e7642b
behavior_unverified: 0
overrides_applied: 0
human_verification: []
covered_files:
  - .planning/REQUIREMENTS.md
  - .planning/phases/60-single-system-learnability/60-01-PLAN.md
  - .planning/phases/60-single-system-learnability/60-01-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-02-PLAN.md
  - .planning/phases/60-single-system-learnability/60-02-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-03-PLAN.md
  - .planning/phases/60-single-system-learnability/60-03-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-04-PLAN.md
  - .planning/phases/60-single-system-learnability/60-04-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-05-PLAN.md
  - .planning/phases/60-single-system-learnability/60-05-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-06-PLAN.md
  - .planning/phases/60-single-system-learnability/60-06-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-07-PLAN.md
  - .planning/phases/60-single-system-learnability/60-07-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-08-PLAN.md
  - .planning/phases/60-single-system-learnability/60-08-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-09-PLAN.md
  - .planning/phases/60-single-system-learnability/60-09-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-10-PLAN.md
  - .planning/phases/60-single-system-learnability/60-10-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-11-PLAN.md
  - .planning/phases/60-single-system-learnability/60-11-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-12-PLAN.md
  - .planning/phases/60-single-system-learnability/60-12-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-13-PLAN.md
  - .planning/phases/60-single-system-learnability/60-13-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-14-PLAN.md
  - .planning/phases/60-single-system-learnability/60-14-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-15-PLAN.md
  - .planning/phases/60-single-system-learnability/60-15-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-16-PLAN.md
  - .planning/phases/60-single-system-learnability/60-16-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-17-PLAN.md
  - .planning/phases/60-single-system-learnability/60-17-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-18-PLAN.md
  - .planning/phases/60-single-system-learnability/60-18-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-19-PLAN.md
  - .planning/phases/60-single-system-learnability/60-19-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-20-PLAN.md
  - .planning/phases/60-single-system-learnability/60-20-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-21-PLAN.md
  - .planning/phases/60-single-system-learnability/60-21-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-22-PLAN.md
  - .planning/phases/60-single-system-learnability/60-22-SUMMARY.md
  - .planning/phases/60-single-system-learnability/60-23-PLAN.md
  - .planning/phases/60-single-system-learnability/60-23-SUMMARY.md
  - .planning/phases/60-single-system-learnability/evidence/launch_phase60_arm.py
  - .planning/phases/60-single-system-learnability/evidence/verify_phase60_evidence.py
  - pinn/verification/diagnostic_architecture.py
  - pinn/verification/feasibility_scorer.py
  - pinn/verification/gate04_omega_remeasure.py
  - pinn/verification/gate04_train_free.py
  - pinn/verification/learnability_arms.py
  - pinn/verification/learnability_data.py
  - pinn/verification/learnability_g2.py
  - pinn/verification/learnability_losses.py
  - pinn/verification/learnability_protocol.py
  - pinn/verification/learnability_ruling.py
  - pinn/verification/learnability_run.py
  - tests/phase60/__init__.py
  - tests/phase60/_fixtures.py
  - tests/phase60/test_admission.py
  - tests/phase60/test_amendment.py
  - tests/phase60/test_arm_spec.py
  - tests/phase60/test_budget_driver.py
  - tests/phase60/test_cli.py
  - tests/phase60/test_cross_check.py
  - tests/phase60/test_data_seam.py
  - tests/phase60/test_g2.py
  - tests/phase60/test_gate04_remeasure.py
  - tests/phase60/test_launcher.py
  - tests/phase60/test_losses_trainer_functions.py
  - tests/phase60/test_mps_lbfgs_smoke.py
  - tests/phase60/test_physics_arm.py
  - tests/phase60/test_preflight.py
  - tests/phase60/test_protocol.py
  - tests/phase60/test_protocol_records.py
  - tests/phase60/test_refusals.py
  - tests/phase60/test_resume.py
  - tests/phase60/test_ruling.py
  - tests/phase60/test_run_short.py
  - tests/phase60/test_schedule.py
  - tests/phase60/test_scorer_mps.py
  - tests/phase60/test_static_guards.py
  - tests/phase60/test_verifier_phase60.py
  - tests/phase60/test_verifier_successor.py
covered_digest: "v1:sha256:dee5c8ed36d9f018fd1f0788a69740e1d5c7285dc02b9d8a81fc51c5d0df42b9"
---

# Phase 60: Single-System Learnability — Verification Report

**Phase goal:** For the first time, the project learns whether the network can
learn one Stage-0 system to physical accuracy: first when shown the answer,
then from the physics.

**Verified:** 2026-10-23 at HEAD `93cb1bcf` (branch `milestone/v2.4`)
**Status:** passed. All five ROADMAP success criteria are met on the path the
phase actually took: Gate G2 fired, the four-setting sweep found no rescue, and
the ladder stopped at G2 by its pre-registered rule.
**Re-verification:** No. This is the first verification (no earlier
`60-VERIFICATION.md` existed).
**Judged against:** `60-SPEC.md` Requirements 1-8 and acceptance criteria, the
five ROADMAP success criteria, every plan's `must_haves`, and the
`REQUIREMENTS.md` Exit Paths row "Early, at G2". A continue path that was never
taken is not held against the phase.

## In plain language

Phase 60 asked one question for the first time: can the network reproduce a
single Stage-0 orbit when it is shown the correct answer, and only if that
works, can it do so from the physics alone? The phase built and tested a
training rig, sealed its rules before any run, and ran the first experiments.
The network did not reproduce any of the three orbits it was shown: all three
graded Tier 0, with an error about 11 to 12 times the Tier-1 line. The
pre-agreed rescue attempt (four other values of the first-layer frequency
setting, on one orbit) also failed. By the rule written down in advance, the
climb stopped there. Learning from the physics and the two hard-stage probes
are recorded as skipped for the reason "no rescue", and the next phase is
Phase 64, the verdict.

I checked this from the code, the tests and the saved results, not from the
summaries. The rig really calls the trainer's own loss functions, refuses test
data, and cannot be fed to the graded-run or evaluation paths. The seven saved
results re-score to the same numbers from their saved weights (the GPU
re-score is identical to the last digit). The rules sealed before the runs
match the code that ran. Nothing that should not exist on this path (Rung 2,
probes, a confirmation run, an owner ruling) exists.

One fact the phase's own findings do not state, found by re-scoring the saved
weights: every trained network is, to within a fraction of a percent, a flat
line in time that predicts each body's average position. It scores the same
grade as a no-learning guess that does exactly that. The records show the
network did not learn; they do not show why. That is for Phase 64 (see
"Independent observation for Phase 64").

## Method note

This is an independent pass, not the executing agent. SUMMARY and FINDINGS
statements were treated as allegations. Every number below was recomputed from
the committed records, weights, code or test runs unless it says "retained".

- **Fresh at `93cb1bcf`, all exit 0:** the Phase 60 evidence verifier `final`;
  the six G2 branch queries; the CPU float64 `rescore` for all seven arms; an
  independent MPS float32 re-score of all 14 saved states; independent
  recomputation of tiers, the better-state rule, counting, G2, the verdict and
  the budget rule from the records; all 25 `tests/phase60` modules, run one at
  a time (992 tests, 0 failures); the nine scorer-dependent Phase 59 suites
  (139) and the prohibition suites (35); eight fast Phase 59 verifier
  subcommands; the gsd artifact and key-link checks for all 23 plans.
- **Reused, not re-run:** Phase 59 `final` (604 s) and the single
  `unittest discover` run (992 tests, 787.9 s). Both are valid at this HEAD
  because their inputs are unchanged (shown below).
- **Departure from the brief's guidance:** I ran the modules one by one instead
  of the single discovery command (about 9.8 minutes of test time in total), and
  three modules took longer than the one-minute guidance: `test_g2` 66.7 s,
  `test_admission` 114.6 s, `test_resume` 121.1 s. I ran them because they hold
  the prohibition and resume tests. The per-module counts sum to exactly the
  retained 992. Nothing was launched, trained (beyond the tiny CPU fixture runs
  inside the tests), committed or edited, and no gsd state, roadmap or
  requirements verb was run. `git status` at the end equals the session-start
  snapshot.

## Success criteria

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| SC1 | The learnability harness is committed and tested: the trainer's own loss functions (mutation-proven); Adam then the L-BFGS polish with both states scored; settings overrides recorded for the sweep's data-only arms only; test-split paths refused; graded-run and evaluator paths refuse its run records | **MET** | Five-bullet table below. 25 modules, 992 tests, all pass; the checks were repeated on the real committed weights and records, not only on fixtures |
| SC2 | Rung 1 has a scored result on each of the three panel systems, within the pre-registered budget rule: tier, valid-horizon fraction, `eps_H`, trace, formula comparison | **MET** | `evidence/arms/r1-1632`, `r1-851`, `r1-4658`: Tier 0 on all three (E 1.1574, 1.2375, 1.1432). Budget rule recomputed from each record's timing run and readings: matches 7/7 arms. Detail below |
| SC3 | Rung 2 has scored results for arms (a) and (b) with the comparison recorded; if the ladder stopped at G2, Rung 2 is recorded as skipped | **MET (stop clause)** | `evidence/g2/skip-records.json`: FEAS-04 `skipped: true`, reason exactly `no rescue`; `level3` = `not tested (skipped at G2)`. No r2a/r2b arm exists anywhere. `learnability_g2 branch ladder` prints `BRANCH-NOT-TAKEN: ladder (the ladder stopped at G2: no rescue)` |
| SC4 | Gate G2 is evaluated against the pre-registered rule, including the settings sweep if it fires, and its outcome is recorded with the evidence | **MET** | Tiers 0, 0, 0 give `g2_fires` true (recomputed with the frozen function). Sweep ran on 1632 (fewest laps, 10.47) at 60, 120, 240, 480 in that order; all Tier 0; `sweep-curve.json` outcome `no_rescue`, `confirmation_arm` null. Files: `g2-outcome.json`, `sweep-curve.json`, `skip-records.json`, `stop-handoff.json`; every hash they cite matches disk |
| SC5 | If the ladder continues past G2, the two probes have scored results; if it stopped at G2, the probes are recorded as skipped | **MET (stop clause)** | `skip-records.json`: FEAS-09 `skipped: true`, reason `no rescue`. No p1/p2b arm exists in evidence or in `runs/` |

### SC1 in detail

| Bullet | What I checked and found |
|---|---|
| Loss functions are the trainer's own, mutation-proven | `pinn/verification/learnability_losses.py` imports the trainer's functions by bare name (`data_huber_loss`, `ic_anchor_loss`, `causal_physics_loss`, `soft_energy_loss`, `angular_momentum_loss`, `compose_total`, `LossWeights` from `pinn.loss_catalog`; `componentwise_du`, `softened_acceleration` from `pinn.physics_residual`; `accumulate_chunked_data_term` and the bin helpers from `pinn.training.controllers`) and defines no loss of its own: `data_only_loss` is one `data_huber_loss` call and `data_polish_objective` is one `accumulate_chunked_data_term` call. The runner calls them (`learnability_run.py` lines 492, 559, 1105, 1118). `IdentityTests` assert each is the trainer's own object; `MutationTests` patch each name and assert the output moves (doubled for data, IC, energy, angular momentum, causal weights and the polish objective); `test_budget_driver`, `test_schedule` and `test_run_short` patch the runner's own call sites. `test_losses_trainer_functions`: 64 tests OK |
| Adam then L-BFGS polish; both states scored | `run_arm`: `drive_adam`, score the Adam state (gold and base grids), CPU float64 cross-check, save `adam.weights`, `_polish` (a real `torch.optim.LBFGS` with the scorecard's settings: `max_iter` 50, history 10, strong Wolfe; stop after 5 outer calls without a lower objective or at 25% of summed Adam time), score the polish state, `better_state`, validated exclusive record write. All 7 records hold both states with `score_gold`, `score_base`, `cross_check` and weights SHA-256 plus tensor digest; polish outer calls 6 to 7. `better_state` recomputed with the frozen function equals the recorded one on 7/7. `test_run_short` (INST-05 d): 38 OK |
| Overrides recorded for the sweep's data-only arms only | Records: the three Rung-1 arms are `omega_provenance: locked`, `grid_omega: null`; the four sweep arms are `g2_sweep_override` with `grid_omega` equal to `first_omega_0` (60, 120, 240, 480) and `loss_arm: data_only`. The closed catalog (42 arms) carries a grid override on 16 data-only arms only and none on a physics arm. `test_arm_spec` (47) and `test_refusals.OverrideOrderTests` refuse an override on `physics_ic`/`full` arms before any network is built or any record is read |
| Refuses test-split paths | `test_data_seam.TestSplitRefusalTests` (10 OK) refuses a test key in every role (train, score, beside) with `open` spied to zero calls. On the real allowlist I probed 9,000 `hierarchical/gold` ids: 4,628 refused, 4,372 accepted (including the panel ids), attestation `test_split_opened` 0, `blocked_attempts` 0. All 7 records and the preflight carry `test_split_opened: 0`; the rescore asserts it too |
| Graded-run and evaluator paths refuse its run records | On the real committed files, `pinn.evaluate.evaluate_run` raises `CheckpointOwnershipError` and `TorchSaveCheckpointStore.load_checkpoint` raises `NoValidCheckpointError` for both weights files of `r1-1632`, `g2s-1632-w060` and `g2s-1632-w480` (six files) and for the `record.json` of `r1-1632` and `g2s-1632-w060`. The graded run's own resume route, `pinn.training.resume.load_resume_target`, raises `NoValidCheckpointError` for `r1-1632/adam.weights`, `g2s-1632-w060/polish.weights` and `r1-1632/record.json`. No evaluation output was created. The runner's command line takes only an arm id, `--resume` and `--admit-only` (`test_cli`: no runtime, precision or path argument), so no option can start a run from a weights file. `test_refusals` (11) proves the same on fixtures, with and without an override |

### SC2 in detail (official state, gold grid, from the records)

| Arm | System | Inner laps | Tier | E | eps_H | Valid horizon 1% / 10% | Better state | Counts vs formula | Formula E | Wall h |
|---|---|---|---|---|---|---|---|---|---|---|
| r1-1632 | 1632 | 10.47 | 0 | 1.1574 | 705.69 | 0.0 / 0.0 | polish | no | 0.9168 | 2.573 |
| r1-851 | 851 | 18.61 | 0 | 1.2375 | 165.50 | 0.0 / 0.0 | adam | no | 0.4312 | 2.842 |
| r1-4658 | 4658 | 39.35 | 0 | 1.1432 | 13127.5 | 0.0 / 0.0 | adam | no | 1.9697 | 5.693 |

- Each arm trains and is scored on `hierarchical/gold/<id>` (1,001 points,
  train split; train and score windowed hashes are equal), with
  `hierarchical/base/<id>` (126 points) as the beside column. Training inputs
  checked directly: tau spans -1 to 1 in steps of 0.002, IC13 rows are the real
  normalized vector (not zeros), and the targets equal the scoring reference to
  1.5e-8.
- Every tier was recomputed with the frozen `tier_of` from the stored `E` and
  `eps_H`, for all 14 gold scores and all 14 CPU float64 cross-check scores:
  all agree, and the cross-check tier equals the official tier on every state.
- Budget rule recomputed with the frozen `steps_budget`, `budget_outcome` and
  `scoring_cadence_ok` from each record's timing run and readings: budget steps
  794,350 / 980,523 / 980,623 (and 908,063 / 955,466 / 994,807 / 842,770 for
  the sweep) all match. `r1-4658` is the one arm the frozen test extends
  (outcome `extend` at the first budget, `complete` after one doubling to
  1,961,246); the rest are `complete`. The 3-hour sizing target is met by the
  step count, not enforced on wall time (Adam ran 0.86x to 1.01x of 10,800 s on
  the one-budget arms).
- Records carry every field SPEC Requirement 4 names: seed 42, MPS float32,
  torch 2.12.1, macOS 26.5.1, `code.git_head`, `config_sha256`, scorecard,
  scorer and protocol SHA-256, `wall.hours`, `timing.seconds_per_step`, and each
  state's weights SHA-256.

### SC4 in detail

- `g2_fires([0,0,0])` true; `[0,0,1]` true; `[0,1,1]` false; `[1,1,1]` false.
  `tier_of(0.1, inf)` is 1, `tier_of(inf, 0)` is 0, `tier_of(0.1000001, 0)` is 0.
- `sweep_plan` returns (sweep, confirmation, uncovered) = (1632, 851, 4658) for
  all three failing and for {1632, 851}; (1632, 4658, 851) for {1632, 4658};
  (851, 4658, 1632) for {851, 4658}; it refuses fewer than two failing systems.
  These are SPEC Requirement 6's four pinned cases, and `g2-outcome.json`
  matches the first.
- The launcher's per-arm records show the four sweep arms ran back to back in
  grid order (each start follows the previous end by under 3 ms), all exit
  code 0, one invocation, no stop. The Rung-1 sequence did the same for the
  three Rung-1 arms. Both sequences report `SEQUENCE-COMPLETE`; no learnability
  process is running.
- `decision_verdict(g2_fired=True, sweep_rescued=False, <four None>)` returns
  `RETHINK-REPRESENTATION`, "G2 fired and the sweep rescued nothing"; the frozen
  function raises `ValueError` if any later-rung input is supplied and
  `OwnerRouted("owner checkpoint 4")` if a rescue is claimed. `stop-handoff.json`
  holds exactly the first result, labelled as the rule's output, not a Phase 60
  verdict.

## Phase contract on the stop path (60-SPEC.md acceptance criteria)

| # | Acceptance criterion | Verdict | Evidence |
|---|---|---|---|
| 1 | Amendment text matches `REQUIREMENTS.md` and `ROADMAP.md` after collapsing whitespace; scorecard SHA-256 unchanged | MET | My containment check: the SCOPE-39, FEAS-04, FEAS-09, SCOPE-44 and checkpoint-4 paragraphs are in `REQUIREMENTS.md`, the roadmap SC3 sentence in `ROADMAP.md`. `test_amendment` 21 OK. Scorecard `f4b17688...9444b` equals the Phase 59 freeze (`SCORECARD-FROZEN-OK`); its only commit is `bae63f02` (2026-10-13) |
| 2 | INST-05 tests (a)-(e) pass | MET | See SC1 |
| 3 | MPS regression passes; a CPU float64 re-score that changes the tier or counts stops for the owner | MET | `test_scorer_mps` 15 OK, including the platform probe that skips by default (it passes with `PHASE60_PLATFORM_PROBES=1`); the scorer fix `57f48478` adds one helper `_to_cpu_float64` at three sites. `test_cross_check` 15 OK. On the real arms all 14 cross-checks agree on tier and counts |
| 4 | Protocol committed before the first real-arm record; every record cites it | MET | Protocol commit `52d98211` (2026-10-20 23:21 CDT) precedes the Rung-1 launch (2026-10-21 21:29 CDT) and the first record commit `0a135eca` (2026-10-22 10:48 CDT). All 7 records cite `93486d24...0383`, which equals the file on disk. The scope amendment `dc3edac0` (2026-10-19) also precedes every real rung |
| 5 | Rung 1 trains on hierarchical gold and is scored on that same gold grid | MET | SC2 detail |
| 6 | G2 matches `g2_fires`; sweep pair matches the pinned lap-count cases | MET | SC4 detail |
| 7 | All four sweep settings run before any confirmation; confirmation is the highest Tier >= 1 setting, or none | MET | Four arms in grid order; none reached Tier 1; no confirmation arm or record; `confirmed_first_omega_0` null |
| 8 | Unanswered checkpoint 4 leaves Rung 2 and the probes neither run nor skipped | NOT APPLICABLE | Checkpoint 4 never arose (`branch owner-decision`: `BRANCH-NOT-TAKEN ... no rescue`); no ruling file. The pending route is covered by `test_g2` and `test_ruling` |
| 9 | A stop at G2 records Rung 2 and FEAS-09 skipped with `no rescue` and does not call `decision_verdict` with later-rung inputs | MET | `skip-records.json`; the handoff writer passes `None` for all four later-rung inputs (`learnability_g2.py`), and `test_g2` has a test that every call passes `None` for each of them |
| 10 | A continue runs the uncovered system's Rung 1, Rung 2 and the probes at the approved setting | NOT APPLICABLE | Not taken. The 31 confirmation, Rung-2, probe and continue arms are in the closed catalog; none has an evidence or run directory |
| 11 | Probe arms never call `counts()`; formula field is `not applicable: no hierarchical split` | Covered by code and tests; not exercised | `_official_counts` returns `None` when the spec is not counted; `FORMULA_NOT_APPLICABLE` is written by the record builder and enforced by `validate_record`; `test_protocol_records`. No probe ran |
| 12 | Every assigned record checked before the first arm; no fallback | MET | `PREFLIGHT-OK`; `evidence/preflight/records.json` lists the ten assigned records (gold 1,001 points, hierarchical base 126, standard base 59) with zero test, blocked and refused counters; `test_preflight` 15 and `test_admission` 69 OK |
| 13 | Resume keeps the budget, sums Adam time, an unrestorable arm stops for the owner | Covered by tests; not exercised | `test_resume` 25 OK. All seven arms ran in one launch (`launch.invocations` 1, `stops` []) |
| 14 | The harness does not catch and retry the three owner-routed cases | MET | `test_static_guards.test_verification_modules_do_not_swallow_owner_stops`, `test_budget_driver`, `test_cross_check`, `test_cli` (exit 3, no retry). None occurred in a real arm |
| 15 | Phases 61-63 marked skipped by G2, not failed, when the ladder stops | MET | `ROADMAP.md` lines 135, 143, 144 and the Progress rows 404-406 read "Skipped at G2 (no rescue), not failed", boxes unticked; `stop-handoff.json` `phases_61_63` and `next_phase` 64 |

REQUIREMENTS.md Exit Paths row "Early, at G2" is satisfied item by item: Rung 1
below Tier 1 on 3 of 3 and the sweep rescued none; Rung 2 and FEAS-09 recorded
skipped with reason no rescue; Level 3 reads "not tested (skipped at G2)";
Phases 61-63 skipped, not failed; the handoff carries RETHINK-REPRESENTATION
with the ladder and sweep evidence for Phase 64.

## Requirements coverage

Every ID in the plans' `requirements` field is accounted for, and
`REQUIREMENTS.md` maps no other requirement to Phase 60 (no orphans).

| Requirement | Plans declaring it | REQUIREMENTS.md | Verdict |
|---|---|---|---|
| INST-05 | 60-01, 02, 04, 05, 07, 08, 10, 11, 12, 13, 22, 23 | `[x]`, Traceability "Complete" | SATISFIED. Harness committed and tested; all seven real arms were produced by it |
| FEAS-03 | 60-02, 06, 07, 08, 10, 11, 12, 13, 14, 15, 16, 17, 20, 22 | `[x]`, "Complete" | SATISFIED. Rung 1 on three systems, G2 evaluated, sweep run, no rescue |
| FEAS-04 | 60-03, 05, 06, 09, 10, 11, 13, 18, 19, 20, 22 | `[x]`, "Complete (recorded as skipped: no rescue)" | SATISFIED by its skip clause |
| FEAS-09 | 60-03, 06, 09, 10, 11, 13, 18, 19, 21, 22 | `[x]`, "Complete (recorded as skipped: no rescue)" | SATISFIED by its skip clause |

The closeout commit `00f7f1bc` changed only the four checkboxes and four
Traceability cells in `REQUIREMENTS.md` (I read the diff); no requirement text
moved.

## Plan must-haves

| Group | Result |
|---|---|
| 18 plans that ran (60-01 to 60-15, 60-18, 60-22, 60-23) | `verify.artifacts`: 57/57 declared artifacts exist and pass; `verify.key-links`: 38/38 verified. Every declared export name resolves to a top-level name in its module (AST check, 0 missing). The plans' truths are covered by the 992 tests plus the real-evidence checks in this report |
| 5 conditional plans that took "branch not taken" (60-16, 60-17, 60-19, 60-20, 60-21) | Each SUMMARY records its branch query output; each is `status: complete` with `requirements-completed: []`. Their five declared artifacts are absent by contract (`rescue.json`, `60-CHECKPOINT-4-RULING.md`, `evidence/continue/gate04-remeasure.json`, `evidence/arms/r2b-1632/record.json`, `evidence/arms/p2b-3418/record.json`); the five matching key links therefore read unverified. This is the correct state |
| 60-18 (stop branch) | `BRANCH-TAKEN: stop (no rescue)`; skip records written once (`9f67d687`), handoff written once (`8bfa9875`), ROADMAP marks (`d54627d8`) |
| All 23 SUMMARYs | `status: complete`. Every commit hash cited in the SUMMARYs and FINDINGS resolves in git except one malformed `plan_head_before` (60-13, under Known issues); the other unresolved 8-character strings are SHA-256 prefixes, session ids and one git blob id |

## Prohibitions (SPEC must-NOT list, all test-tier)

| Prohibition | Enforcement found | Verdict |
|---|---|---|
| No test-split open or held-out spend | `TestSplitRefusalTests`; evaluator refusal of harness files; attestation zeros on 7/7 records, the preflight and my rescore runs | Enforced |
| No other seed, silent restart or second fresh run replacing an arm | `test_second_run_is_refused_before_any_optimizer_step`, `ExclusiveWriterTests` (O_EXCL write), `ResumeRefused`/`ClaimExists`; each of the 7 records has exactly one commit | Enforced |
| Never take the better of the MPS score and the CPU cross-check | `test_the_cpu_score_never_reaches_the_better_state_rule`, disagreement stops before polish weights are written; protocol `take_the_better: false` | Enforced |
| No later-rung inputs to `decision_verdict` once G2 fired | Frozen function raises (I called it); the handoff writer passes `None`; `test_g2` asserts it for every call | Enforced |
| No substitute fidelity or system for a missing, empty or unreadable record | `test_preflight`, `test_admission` ("substitutes nothing"), the closed record-key catalog | Enforced |
| `OwnerRouted` never caught and retried | Static guard (`test_verification_modules_do_not_swallow_owner_stops`), `test_budget_driver`, `test_cross_check`, `test_cli` | Enforced |
| No skip after a Rung-2 arm started, or with another reason | `_write_skip` rejects any reason outside the two; `_refuse_started_ladder`; `test_g2` | Enforced |
| A data-only arm's weights never start another run; scorecard bytes unchanged | `run_arm` has no initial-weights parameter and the CLI no path option (`test_cli`); the graded resume route and the evaluator refuse the weights (checked on the real files); scorecard hash equals the freeze | Enforced |

None is left as an unverified prohibition.

## Absent by contract (checked, all absent)

`find` under the phase directory for `r2a*`, `r2b*`, `p1*`, `p2b*`, `c-*`,
`rescue.json`, `60-CHECKPOINT-4-RULING.md`, `*ruling*`, `confirmation*` and
`continue`: nothing. `evidence/arms/` holds exactly seven directories. Of the 42
catalog arms, exactly the seven executed ones have an evidence directory and a
`runs/phase60/` directory; the other 35 have neither. `evidence/g2/` holds the
four files the stop path implies and no `rescue.json`. `git status` for the
phase directory is clean; all 30 evidence files are tracked.

## Data-flow trace

| Artifact | Source | Check | Verdict |
|---|---|---|---|
| `evidence/arms/*/record.json` | Real runs by the pinned runner | Weights re-score to the recorded numbers (below); 33 pinned module hashes equal the sealed protocol | Flows |
| `g2-outcome.json`, `sweep-curve.json` | Derived from the records | Every cited record SHA-256 and every `E`, `eps_H`, tier, omega equals the record | Flows |
| `skip-records.json`, `stop-handoff.json` | Derived from the above | Cited hashes match; per-arm hours and seconds per step equal the records; total 22.37829 h equals the sum; verdict equals the frozen call | Flows |
| `60-FINDINGS.md` | Records and G2 files | Every per-arm number I compared matches; all 21 file hashes and 14 weights hashes in its evidence index match disk | Flows |

## Supporting checks

| Check | Result |
|---|---|
| `verify_phase60_evidence.py final` | `PROTOCOL-OK`, `PREFLIGHT-OK`, `RECORDS-OK`, `G2-OK`, `PHASE60-EVIDENCE-OK`; exit 0; 1.5 s |
| `python -m pinn.verification.learnability_g2 branch` sweep / stop / owner-decision / confirmation / continue-gate / ladder | TAKEN (sweep system 1632); TAKEN (stop, no rescue); NOT-TAKEN with the stated reasons for the other four; each exit 0 |
| `verify_phase60_evidence.py rescore --cpu-only --arm A`, A in all seven arms | `RESCORE-OK`, exit 0, 5.6 to 7 s each: weights SHA-256 and tensor digest match; CPU float64 score equals the recorded cross-check within 1e-12 |
| Independent MPS float32 re-score of all 14 saved states (my script, not the verifier's) | Tier equal; `E` and `eps_H` relative difference 0.0 on all 14; zero test-split opens; 11 s. The verifier itself checks only tier and counts here |
| Recomputed from records with the frozen scorecard functions | `tier_of` 28/28, `better_state` 7/7, `counts` 7/7, `steps_budget`/`budget_outcome`/`scoring_cadence_ok` 7/7, `g2_fires` cases, `decision_verdict` and its refusals, `sweep_plan` four cases: all match |
| 33 pinned modules | On-disk hash = protocol pin = each record's `module_sha256` (7 x 33, none different); no commit touches any of them after the seal `52d98211` |
| `tests/phase60`, 25 modules one at a time | 992 tests OK in about 586 s (sum of module wall times); the one default skip passes with `PHASE60_PLATFORM_PROBES=1`. Retained single run: 992 tests, 787.9 s, OK at `2ca6a821`; `git diff --quiet 2ca6a821 HEAD -- pinn tests .../evidence` exits 0 (only four docs commits since) |
| Nine scorer-dependent Phase 59 suites | Ran 139 tests, OK, 31 s |
| `tests.phase39.test_prohibitions` + four named `tests.phase38` tests | Ran 35 tests, OK, 1.7 s |
| Phase 59 fast subcommands (`scorecard-frozen`, `guardrails`, `manifest --area all`, `audit`, `census`, `survey`, `baselines`, `diag07`, with `--skip-rederive --require-committed` where taken) | All eight OK, exit 0 |
| Phase 59 `final` (reused) | `PHASE59-EVIDENCE-OK`, `ELAPSED=604`, `EXIT=0` at `4df5d4a8` (log in `$HOME/.cache/3bp-phase60-logs/`). `git diff --quiet 4df5d4a8 HEAD -- .planning/phases/59-read-only-baseline-scorecard` exits 0; the scorer last changed at `57f48478`, before that log; since then `pinn/` changed only in Phase 60 modules, `diagnostic_architecture.py`, `gate04_omega_remeasure.py` and `gate04_train_free.py`, none of which Phase 59's verifier or tests reference |
| `launch_phase60_arm.py --sequence rung1 --status` and `--sequence sweep-1632 --status` | `SEQUENCE-COMPLETE` both; no `learnability_run` or launcher process running |
| Commit hygiene | 107 commits since 2026-10-17 17:00: all match `type(scope): subject`, all carry an agent trailer |
| Anti-pattern scan (modules above plus the two evidence scripts and `tests/phase60`) | No `TBD`/`FIXME`/`XXX`, no `TODO`/`HACK`/`PLACEHOLDER`. One `NotImplementedError` in `gate04_train_free.py:451` is a deliberate Phase 57 compatibility refusal (commit `0ccfe855`, 2026-09-08), not a stub. One `except Exception: pass` in `learnability_losses.py` around `torch.mps.empty_cache` is intentional and tested |

## Known issues and accepted deviations

None of these changes a verdict.

1. **Verifier first-use crashes (accepted, repaired, tested).** The evidence
   verifier is not one of the 33 pinned files. Its sweep-curve check crashed on
   the first real curve and was fixed in `e3841c73` (3 regression tests); its
   `rescore` check crashed on first real use at closeout (three defects behind
   one error) and was fixed in `2ca6a821` with a test rewritten on real objects.
   Neither repair changed a recorded number or a pinned file. The verifier's
   rescue branch has never run on a real rescue (none occurred); it is covered
   by tests only.
2. **Stale runtime estimate.** `tests/phase60` takes about 13 minutes (retained
   787.9 s), not "under about 60 s". `60-VALIDATION.md` is still `status: draft`,
   `nyquist_compliant: false`, `wave_0_complete: false`, with every one of its 63
   task rows still marked pending and approval pending. This is an unsigned
   process artifact, not a goal gap (Phase 59's equivalent was signed off). It
   can be closed by the orchestrator or a validate-phase run.
3. **Literal acceptance clause.** Plan 60-22's `tail -n 1 ... | grep -qx 'EXIT=0'`
   does not hold: the retained log is `START=`, `RESCORE-OK`, `EXIT=0`, `END=`,
   so its last line is the END stamp. On substance the clause is met
   (`RESCORE-OK` and `EXIT=0` are present, and I reproduced `RESCORE-OK` for all
   seven arms myself).
4. **Memory figure waived by the owner.** The 6 GiB free-memory figure was
   waived in the owner's words (quoted in the 60-14 frontmatter and the 60-15
   SUMMARY). I cannot confirm free memory at launch from the repository; the
   effect (swap pressure) on seconds per step is not measured, as FINDINGS says.
5. **`STATE.md` frontmatter is stale.** It still reads `status: executing`,
   `completed_phases: 1` and an old `stopped_at`, while the body says Phase 60
   is complete. The closeout commit `00f7f1bc` states it left those fields to the
   orchestrator. Not part of Phase 60's acceptance.
6. **A malformed hash in a SUMMARY.** `60-13-SUMMARY.md` `plan_head_before` is
   `8df698864d420f86b406981cfb56c4d7ec59b56f`, which does not resolve; the true
   commit is `8df69886cb360ff0424eb8b830d4ba3042718a3e` (same first 8
   characters). Cosmetic. The other 11 `plan_head_before` values resolve.
7. **Plan text not implemented in the verifier.** Plan 60-13 says `rescore`
   reports the MPS `E` difference; the verifier checks only tier and counts on
   the MPS half. I measured the difference myself: exactly zero on all 14 states.
8. **Re-derivation needs the external data root.** The re-score reads the
   simulation records through the Phase 59 allowlist from the default data root
   outside git (present on this Mac). Re-deriving elsewhere needs that dataset.

## Independent observation for Phase 64 (not a gap)

This is my own read-only analysis of the committed weights. It is not a Phase 60
artifact and not part of any acceptance test. The scripts are in the verifier's
session scratchpad and are not committed.

**Every trained network is a time-constant predictor.** For all seven arms and
both states, the network output barely depends on time.

| System | Constant "time-mean" predictor, frozen scorer | Trained network, official | Final training objective (record) | Same objective for the mean predictor (`data_huber_loss`) | Trained network's time variation / target's |
|---|---|---|---|---|---|
| 1632 | Tier 0, E 1.1538 | Tier 0, E 1.1574 | 0.00711013 | 0.00711232 | 0.0034 |
| 851 | Tier 0, E 1.2337 | Tier 0, E 1.2375 | 0.00974306 | 0.00974632 | 0.0032 |
| 4658 | Tier 0, E 1.1396 | Tier 0, E 1.1432 | 0.00112847 | 0.00112877 | 0.0032 |

- The "constant predictor" holds each body at its average position over the
  window and learns nothing. The frozen scorer grades it Tier 0 with E within
  0.004 of the trained networks, which are slightly worse than it.
- The four sweep arms on 1632 end at objective 0.0071095 to 0.0071107 for
  omega 60, 120, 240 and 480, the same value as the locked setting to four
  digits and within 4e-4 (relative) of the mean predictor's, which is the size
  of the MPS-versus-CPU float32 difference (the same weights give 0.0071119 on
  the CPU against 0.0071101 recorded on MPS). Their RMS error equals the RMS of
  the target about its own time mean to four or five digits (ratio 0.9999 to
  1.0001). The trained networks vary in time by about 0.3% of the target's
  variation; the untrained seed-42 network varies 2.5 to 7 times more than the
  target does.
- The error is therefore the error of "predict the average", which also
  explains FINDINGS' observation that E sits in a narrow band (1.14 to 1.24)
  across orbits whose inner-lap counts differ by a factor of about 3.8.
- Training did move the weights a long way: in the `r1-1632` Adam state every
  input and hidden tensor is 5.3 to 14.0 times its initial norm away from the
  seed-42 initialization (the input layer 14.0 times), and the two output-layer
  tensors 1.2 and 1.5 times. The optimizer covers all parameters
  (`Adam(model.parameters())`).
- I found no harness defect that explains it. The loss is the trainer's, the
  inputs and targets are correct (above), the training-mode batch forward and
  the scorer's per-time trajectory are both time-constant (they differ by at most 3e-3 against a target variation of
  about 0.1), and the recorded objective reproduces on the CPU from the
  committed weights to 2.5e-4.

What this does and does not show. The records establish that, at all five
first-layer settings tried, the production network trained under the fixed
recipe ended as a (nearly) time-constant function, and that its Tier-0 grade is
the grade of a no-learning constant. They do not distinguish a representation
limit from an optimization outcome of the fixed recipe (Adam, rate 1e-3 on a
cosine, median clipping, 12 layers of 256), because the pre-registered sweep
varied only `first_omega_0` and the other knobs were held fixed on purpose.
`RETHINK-REPRESENTATION` is the frozen rule's mechanical label for "G2 fired and
no rescue". I recommend Phase 64 state this observation beside the formula and
nearest-neighbour comparison points before the owner reads that label.

I did not list this as a human-verification item because Phase 60's acceptance
does not depend on it; the owner decision it informs is checkpoint 1 at
Phase 64. It is recorded here so it is not lost.

## Carried forward

- **GAP-59-08 (OPEN, owner-routed, Phase 59 item).** Unchanged: the production
  energy check uses finite-difference velocities. It blocks any held-out spend
  and the FEAS-10 pass-bar choice, not Phase 60.
- **Phase 60 gaps.** `60-GAPS.md` and `.planning/milestones/v2.4-GAPS.md` list
  GAP-60-01 to GAP-60-13, all `RESOLVED-WITH-INSTRUCTION` (2026-10-18). GAP-60-09
  resolved only the procedure (owner-routed if it occurs); it did not occur. No
  unlogged source-silent decision turned up in the SUMMARY deviation sections.
- **Paths that exist as tested code and never ran on real data**, by contract:
  the confirmation, rescue and checkpoint-4 route, the continue gate, the
  re-measure of `R_ref` and GATE-04, the Rung-2 and probe physics arms, the
  resume path, and the verifier's rescue branch.
- **One seed per arm** is a stated limit for the verdict, not a reason to add
  seeds.

## What I did not verify, or assumed

- I did not retrain anything (not allowed) and did not run the single
  `unittest discover` or Phase 59 `final`; I relied on the retained results and
  the unchanged-input diffs shown above.
- "One arm at a time with no other heavy job" is established from the launcher's
  contiguous per-arm timestamps, not from process accounting.
- The owner's memory waiver and the owner's go-ahead quotes are taken from the
  SUMMARYs; no command can confirm them.
- I did not audit the external simulation data itself, only how the harness
  reads it.
- I did not judge whether the null result reflects a representation limit; see
  the observation above.

## Human verification required

None.

## Gaps summary

No gaps. All five success criteria, SPEC Requirements 1-8 as they apply to the
stop path, the four requirement IDs, and the eight prohibitions are verified
against the code, the tests and the committed evidence. The
non-blocking items are listed under Known issues; the observation for Phase 64
is listed above.

---

_Verified: 2026-10-23T22:50:15Z_
_Verifier: Claude (gsd-verifier, independent pass)_
