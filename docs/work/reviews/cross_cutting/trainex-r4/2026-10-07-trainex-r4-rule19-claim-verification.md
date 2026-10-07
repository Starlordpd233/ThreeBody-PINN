---
status: active
purpose: verification-report
created: 2026-10-07
milestone: untracked
phase: cross-cutting
retirement_trigger: the trainex-r4 round is consumed — its reports are verified (Rule 19), consolidated, and the owner has ruled on the decision sheet
verifier: Claude Code (claude-opus-5-5), the in-repo agent
live_tree_pin: 296c6526fe49807f6e0267847c21f119aeac178a
reports_verified: research_results/codex-resolution.md (report_body_sha256 634c5fdd…); research_results/claude-resolution.md (report_body_sha256 58051ae1…)
---

# trainex-r4 — ERW Rule-19 verification of the returned reports' claims

## Status of this file

| Part | Covers | State |
|---|---|---|
| 1 | The premise-challenge findings: Codex §1 (P1–P6); Claude §2 (PC-1 to PC-12) and its §2.13 table of F-01 to F-18 | **complete in this commit** |
| 2 | The diagnoses, the facts each option rests on, the gaps, and the claims registers | pending; it will extend this file |

## Why this exists

Two reports came back for the trainex-r4 round: Codex on 2026-10-04 and Claude
on 2026-10-06. Both open with the same finding: the generation-7 run computed its
physics loss on one trajectory per step, not on every selected trajectory as the
ratified recipe requires.

The ERW runbook requires an in-repo, per-claim verification before any returned
claim informs a decision. If a verified claim contradicts a package premise, the
round must be re-framed before its answers are used
(`docs/runbooks/external-research/2026-06-11-external-research-workflow.md`,
"Handoff" step 6). The premise layer is verified first because the re-framing
depends on it.

This file verifies. It rules on nothing. Whether and how the round is re-framed is
a separate record.

**Independence.** Several of the challenged premises are statements the in-repo
agent wrote into the package. For that reason a second, independent check of the
same layer was commissioned in parallel on 2026-10-07. It works from a written
brief and blind to this file. This file was written without reading that check's
report.

## Scope of Part 1

| # | Source section | Extracted | Rows |
|---|---|---|---|
| 1 | `codex-resolution.md` §1, lines 29–80 | each finding split into separately checkable assertions | 6 findings → 26 rows |
| 2 | `claude-resolution.md` §2, lines 193–594 | the same | 12 findings → 74 rows |
| 3 | `claude-resolution.md` §2.13, lines 596–634 | each F-row note, plus the notes on Part G, the monitor recompute, code identity, and the bundle | 18 rows and 4 notes → 22 rows |

**Total ledger rows: 122.**

Paths in the ledger are repository-relative. `controllers.py` is
`pinn/training/controllers.py`, `batches.py` is `pinn/data/batches.py`, the
verifier is `pinn/verification/phase57_production_conformance.py`, and "the spec"
is `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`.
The master, prompt, and bundles are the files under
`pinn_instruction/markdown_conversion/framework-specs/trainex-r4/research_package/`.

## Method

**Pin and code identity.** The tree was read at
`296c6526fe49807f6e0267847c21f119aeac178a`. Each of these three commands
printed nothing, with valid refs:

```
git diff --stat 629b1a6ca4462915b6340a59b8d4e3ad8df75d8b HEAD -- pinn/ configs/ <ctl_instruction.md> <pinn_architecture.md>
git diff --stat 735e2ae8d5ec30b9915ec9172ac06965fbaa8afb HEAD -- pinn/ configs/ runs/ <both specs>
git diff --stat ef4764f9 629b1a6c -- pinn/
```

So the code and specs read here are byte-identical to the code that ran
generation 7 (commit `629b1a6c…`), to the package baseline (`735e2ae8…`), and to
generation 6's code (commit `ef4764f9…`). The run directories are unchanged
since the baseline. Line numbers below describe the code that ran.

**Read-only.**

- No training was run and no evaluation invoked.
- No model forward or backward pass was run. Claims that need one carry the
  verdict `NOT-VERIFIABLE-HERE`.
- Checkpoints were read as tensors only (`torch.load(..., weights_only=True)`).
- **No trajectory data file of any split was opened.** The per-step
  trajectory sequence was rebuilt from `splits.json` metadata alone. The rebuild
  is proved correct by matching the random-number state saved in every retained
  checkpoint (Appendix A.2).

**Content first.** A wrong line number is recorded separately from a wrong
claim, because a claim can be true at a line that has moved.

**Scripts.** All five scripts and their complete outputs are reproduced in
Appendix A with SHA-256 digests, so every number below can be re-derived. They
ran from the repository root:

- `r4v_logs.py`, `r4v_anchor_stats.py`, and `r4v_tb.py` under the system
  `python3` (standard library only);
- `r4v_anchor_replay.py` and `r4v_ckpt.py` under the project's `.venv/bin/python`
  (torch, numpy).

## Verdict vocabulary

The six verdicts of the trainex-r3 check, unchanged
(`docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/2026-09-02-trainex-r3-rule19-claim-verification.md`,
"The closed verdict vocabulary (D-13)"):

| Verdict | Meaning |
|---|---|
| `CONFIRMED` | Re-derived, and the tree says what the claim says. |
| `CONFIRMED-SHARPER` | Re-derived, and the evidence supports a stronger statement. The stronger statement is given. |
| `CONFIRMED-NARROWER` | Re-derived, but true only under a narrower reading. The narrower reading is given. |
| `REFUTED` | Re-derived, and the tree contradicts the claim. |
| `UNSUPPORTED` | The cited location exists but does not carry the claimed content. |
| `NOT-VERIFIABLE-HERE` | Cannot be re-derived within this pass's rules. What would settle it is named. |

A row with a part this pass can settle and a part it cannot carries two
verdicts separated by `·`.

## Ledger

### Group A — Codex §1 (P1–P6)

| Row | Assertion | Evidence | Verdict | Note |
|---|---|---|---|---|
| A-P1a | The sampler builds each collocation row's IC, masses, and record key | `batches.py:488-507`: one `ic13`, `masses`, and key appended per assigned row | `CONFIRMED` | `:492` is the loop head |
| A-P1b | The controller selects the first replay identity | `controllers.py:1075-1079`: `_select_anchor_key` returns `keys[0]` of replay + lookahead | `CONFIRMED` | |
| A-P1c | It builds a trajectory callable around that identity and consumes only the collocation times | `controllers.py:1081-1095` (closure over the anchor's `ic13` and `masses`); `:1117-1128` (comment "Only the TIME dimension is consumed here"; times taken at `:1128`) | `CONFIRMED` | |
| A-P1d | Every physics microbatch evaluates that same callable and mass vector | `controllers.py:1746-1770`: `_collocation_chunk_raw` calls `anchor_ctx.traj` and `anchor_ctx.masses`; the monolithic path at `:1169-1181` does the same | `CONFIRMED` | `:1760` lies inside the cited function |
| A-P1e | Intended bin residual averages `R(u_s, IC_s, m_s)` over the bin's 256 rows; executed averages `R(u_s, IC_anchor, m_anchor)` | The spec's collocation-allocation block (`:456`: "one row per selected slot inside every bin"; "each bin residual is the mean of exactly 256 rows"); code as in A-P1c and A-P1d | `CONFIRMED` | |
| A-P1f | This conflicts with the locked selected-slot contract and the owner's instruction; it is not an open reading of "time allocation" | `57-GAPS.md:214-218` (Option A patch inventory "including replacing the current one-anchor physics-loss execution with contributions from all selected slots"); `57-02-PLAN.md:23`, `:84` (must-have "every selected slot contributes physics gradients"); the spec `:456` keeps "selected-slot multiplicity" and "near-even identity weighting" in force | `CONFIRMED` | The code's own justification (`controllers.py:1124-1127`) quotes the spec's "re-ratifies the time allocation only". The owner's Option A note and the 57-02 must-have exclude that reading. |
| A-P1g | F-12's counts, normalization, and prefix arithmetic are supported; its premise that the complete ratified recipe executed is contradicted | Every generation-7 record logs `n_collocation_rows` 4096, `n_bins` 16, and the frozen `r_ref`; A-P1a to A-P1d | `CONFIRMED` | |
| A-P1h | The production files and live specs match generation 7's run commit byte for byte | Method: the `git diff --stat 629b1a6c HEAD` output is empty | `CONFIRMED` | |
| A-P2a | The verifier checks that the emitted collocation keys hold more than one identity, then calls the single-anchor calculation | Verifier `:408-411` (the assertion), `:413-415` (`_build_anchor_context`, `_non_data_terms`) | `CONFIRMED` | |
| A-P2b | Its output `"anchor_only": false` is a literal constant | Verifier `:533` | `CONFIRMED` | |
| A-P2c | Finite, non-zero aggregate physics gradients cannot show that each row's IC reached the model | Of the verifier's 39 `_assert_condition` calls, the only identity-related one is `:408-411`. The identity-dependent synthetic IC and masses (`:251-254`) are never asserted on | `CONFIRMED` | |
| A-P3a | The frozen monitor holds 4096 rows, 256 distinct keys, 16 rows per key; its first identity is `('hierarchical', 'base', 28)` | A.5: `step-000951.pt` `front_monitor.record_keys` | `CONFIRMED` | |
| A-P3b | Monitor evaluation rebuilds the same single-anchor context | `controllers.py:1044-1046`: `_build_anchor_context(self._train_source, self._front_monitor_batch, None)` | `CONFIRMED` | `:931` serializes the monitor batch at construction; the evaluation is `:1044` |
| A-P3c | So its physics residuals describe one fixed identity at the frozen times, not the 256-identity population | A-P3a, A-P3b | `CONFIRMED` | |
| A-P3d | Replay keys are sorted and the controller takes the smallest, which favors low-ranked keys; this does not show those keys are easier or harder | `batches.py:76-78`; `controllers.py:1075-1079`; A.3: 74.7 % of steps used one of the 10 lowest-ID trajectories | `CONFIRMED` | |
| A-P4a | `n_adam` and `max_epochs` are both 1000 | `configs/stage0-v23g7-seed42.yaml:24-25` | `CONFIRMED` | |
| A-P4b | After Adam exhaustion the refinement budget is zero and the controller returns through the stage-exit path without L-BFGS | `controllers.py:2690-2707` | `CONFIRMED` | |
| A-P4c | An earlier plateau could have left budget, but the detector's longest qualifying streak was 6 against the required 50 | `controllers.py:134-135`, `:546-562`; A.1: longest run 6, resets 433 | `CONFIRMED` | |
| A-P4d | So F-05's hand-off description is incomplete in a consequential way | Master `:183` ("Handoff: to L-BFGS at budget exhaustion or at a physics-loss plateau"); A-P4b, A-P4c | `CONFIRMED` | |
| A-P5a | Generations 6 and 7's configurations differ only in run name | `diff configs/stage0-v23g6-seed42.yaml configs/stage0-v23g7-seed42.yaml`: the header comment and `run.run_name` only | `CONFIRMED` | |
| A-P5b | Their telemetry shares a substantial initial trajectory | F-13; A.2 and A.3 | `CONFIRMED-SHARPER` | The two runs drew identical batches, anchors, and validation draws for all 513 shared steps; the replay matches both runs' checkpoint RNG states |
| A-P5c | Generation 6 ended by process loss at step 513, 160 updates after its last front advance at 353, and never exhausted the window | `57-…/evidence/blocked-state-g6.json`: `blocked_reason` `unexpected-process-loss`, `invariant_b_state` `{2, 353}`; 513 completed log records | `CONFIRMED` | The high-water fields sit at `:14-16`; `:13` is `global_step` |
| A-P5d | The "two independent runs … stalled" wording overstates the evidence | Verdict packet `:105` | `CONFIRMED` | The package already listed this wording as challengeable analysis (`H-02`, "to be read against `F-13`") |
| A-P6a | "Applied" gradient = scheduled weight × raw norm, before Adam preconditioning | `controllers.py:2000-2009` | `CONFIRMED` | Cited at `:1993`, where the block begins |
| A-P6b | The "raw" physics gradient already includes the `R_ref` normalization | The physics term is the residual-wide normalized loss (F-12); logged `loss_phys` is 0.07–0.26 while raw bin residuals are about 10¹⁰ | `CONFIRMED` | |
| A-P6c | The logged weighted-sum identity holds to float32 rounding, maximum relative discrepancy about 1.14 × 10⁻⁷ | A.1: maximum 1.14 × 10⁻⁷, exact equality on 0 of 952 records | `CONFIRMED` | The maximum is at step 53 (log line 53). The cited line 57 carries 1.03 × 10⁻⁷ |

### Group B — Claude §2 (PC-1 to PC-12)

| Row | Assertion | Evidence | Verdict | Note |
|---|---|---|---|---|
| B-PC1a | The sampler is conformant: each of the 4096 rows carries its own slot's `tau_ic13`, `masses`, and key | `batches.py:488-507` | `CONFIRMED` | |
| B-PC1b | The loss keeps only the times: anchor `keys[0]`; trajectory from the anchor's `ic13` and `masses`; the comment says so | `controllers.py:1075-1079`, `:1081-1095`, `:1117-1128` | `CONFIRMED` | |
| B-PC1c | Every physics row is evaluated on the anchor's trajectory in the monolithic and microbatched paths, and production ran the microbatched one | `controllers.py:1169-1181`, `:1746-1770`; config `adam_microbatch_size: 256`; the diagnostic steps' provenance is `microbatch_pass2_diagnostic` | `CONFIRMED` | |
| B-PC1d | The IC term is the anchor's IC | `controllers.py:1857-1864` | `CONFIRMED` | This is pre-existing behavior that Phase 57 deliberately kept (`57-02-PLAN.md:87`: "Preserve IC … behavior outside this bounded seam"). The data term is not anchored: `_data_term(batch.data_points)` (`:1865`) fits all 256 selected slots' data points (`:603-612`, `:1149`) |
| B-PC1e | The per-row `tau_ic13` and `masses` are only serialized and hashed; no loss reads them | A search of `pinn/` finds the collocation `tau_ic13` and `masses` only at `controllers.py:320-321`, `:333-334`, `:391`, `:409-410` (serialize, hash, restore). The loss reads only `.times` (`:1128`) | `CONFIRMED` | |
| B-PC1f | The anchor is the lowest ID among the step's 240 replay draws | `batches.py:76-78` (sorted), `controllers.py:1075-1079` | `CONFIRMED` | |
| B-PC1g | With N₀ = 1,812: P(rank 1) = 13.25 %, mean rank 7.5, effective number of anchors 14.1 | N₀ from `splits.json` (train, stage 0) and `training_metadata.json` `n_train`; A.3: 0.1325, 7.523, 14.07 | `CONFIRMED` | |
| B-PC1h | The per-step anchor sequence can be rebuilt from metadata, reproduces the monitor batch's keys, and matches the RNG state in all seven retained checkpoints | A.2: the monitor batch's first keys are reproduced (`[28, 90, 104, 147, 167]`); the state after that draw equals `stage-0-init.pt`; `best.pt`, `step-000931/941/951.pt`, `latest.pt`, and the failure checkpoint (after the 952 draw) all match | `CONFIRMED` | Re-derived independently. No data file was needed: a uniform 126-snapshot count reproduces every state, which proves it for every drawn record |
| B-PC1i | Over the 951 completed steps: 40 distinct trajectories; 74.7 % of steps on the 10 lowest-ID; IDs 0 and 1 took 132 and 111 steps | A.3 | `CONFIRMED` | |
| B-PC1j | The monitor is its own batch's anchor, trajectory 28 (Stage-0 rank 13), and was the training anchor on 31 listed steps | A.3: the same 31 steps | `CONFIRMED` | |
| B-PC1k | A sub-agent rebuilt the monitor from checkpoint contents, reproduced the packet's values, and confirmed all 4096 monitor times are evaluated on trajectory 28's IC13 | Code: `controllers.py:1044-1046` with the monitor anchor 28 (A-P3a) | `CONFIRMED` (structure) · `NOT-VERIFIABLE-HERE` (numeric reproduction) | The numbers need a forward pass, which this pass did not run |
| B-PC1l | Phase-57 records required per-slot evaluation and called one-anchor execution nonconformant | `57-RESEARCH.md:70`, `:138`, `:188`; `57-02-PLAN.md:23`, `:84` | `CONFIRMED` | |
| B-PC1m | The summary records the anchor path as replaced; only the time source was replaced; the regression test proves only that poisoned times propagate | `57-02-SUMMARY.md:100`, `:106`; `tests/phase40/test_optimizer_phase.py:686-720` | `CONFIRMED` | |
| B-PC1n | The verifier's anchor check passes by construction | Verifier `:408-415`, `:533`, `:251-254`; none of its 39 assertions tests identity use | `CONFIRMED` | |
| B-PC1o | Validation is single-trajectory and single-point: `collocation_count=1`; the anchor is always ID 12; so `val_phys` (ADVANCE criterion 3) is one time on one fixed trajectory | `controllers.py:1384-1385`, `:2176`; `batches.py:135-157` (the validation pool, sorted); the lowest Stage-0 validation ID in `splits.json` is 12 | `CONFIRMED` | |
| B-PC1p | So invariant B tracked one training trajectory, not the 256 frozen identities 57-RULING describes | A-P3a to A-P3c | `CONFIRMED` | |
| B-PC1q | Anchor identity explains 51 / 28 / 21 % of the detrended variance of log R̃ in bins 0 / 1 / 2; resampling the times of one trajectory at fixed parameters moves S₁ and S₂ by about 4–8 % | A.4: 50–52 / 27 / 19–20 % across three detrending windows; step 901 S₁ 0.779 against the monitor's 0.728 at `best.pt` (7.0 %); step 943 S₂ 1.120 against 1.182 and 1.189 (5.3–5.8 %) | `CONFIRMED` | The report does not state its detrending method. Results agree within 1–2 points under rolling-median detrending |
| B-PC1r | The IC term's swings depend on exposure: ID 0 ended at IC loss 26–59; trajectory 28 at 2.3 × 10³ – 2.2 × 10⁴; the run minimum 25.7 (step 947) is ID 0 | A.3: ID 0's last five appearances 59.1, 40.0, 34.0, 27.4, 25.7; trajectory 28 at steps 892, 901, 908, 943: 22,083 / 2,342 / 12,180 / 5,870; minimum at step 947, anchor 0 | `CONFIRMED` | |
| B-PC1s | `R_ref` and GATE-04 were measured on single-trajectory cases, so a per-slot fix triggers re-measurement under the named invalidation list | `pinn/verification/gate04_train_free.py:703-754` (one network, one IC13, one mass vector per case); `pinn/verification/artifacts/r_ref_stage0.json` (six cases); the spec `:454` lists "count unit, selected-slot semantics" | `CONFIRMED` | |
| B-PC1t | This is an implementation non-conformance; the owner may still choose to ratify anchor semantics | A-P1f; `57-02-PLAN.md:87`; the spec §3.3 (`:509-515`) | `CONFIRMED-NARROWER` | Established for the physics term, and so for the monitor. The IC term's one-trajectory evaluation is kept by plan, and the spec's `L_IC` states no batch rule, so whether it must cover every slot is open, not a verified non-conformance. The second half of the assertion is an option, not a claim |
| B-PC2a | The applied IC gradient exceeded the applied physics gradient by 2.78 × 10⁴ – 2.62 × 10⁶ on every diagnostic step | A.1, over the 19 steps | `CONFIRMED` | |
| B-PC2b | Under Adam, a component 10⁻⁴ – 10⁻⁶ of the dominant one contributes the same tiny fraction of the update | Analysis | `CONFIRMED-NARROWER` | The logged ratio is between global norms. Adam normalizes per parameter, and the logs do not show per-parameter dominance. B-PC2e is the direct evidence |
| B-PC2c | At step 951, median \|m̂\|/√v̂ = 0.039 (p90 0.115); gradient clipping never bound (peak norm/threshold 0.73) | A.5: median 0.0389, p90 0.1147 over all 795,657 parameters; peak clip ratio 0.741 at step 941 | `CONFIRMED` | The peak differs in the second digit, within how the clip window was reconstructed. It never approaches 1 |
| B-PC2d | The imbalance was on record before the run: raw IC gradient 3.80 × 10⁸, physics 215, data 60.3 | `57-…/evidence/production-conformance.json:100-112` (`closure_gradient_stats`) | `CONFIRMED` | |
| B-PC2e | Natural experiment. Generation 7, 57 pairs: IC fell in 65 % (median Δlog₁₀ −0.144, about −28 %); physics fell in 42 % (median +0.002); S₂ fell in 49 % (median 0.000). Generation 6, 32 pairs: 69 / 41 / 38 % | A.3 and A.4 | `CONFIRMED` | Physics median +0.002 is the Δlog₁₀; S₂ median +0.0008 |
| B-PC2f | Output-layer weight norm 1.7525 → 1.1715 (×0.668); all 9 rows ≈0.59 → ≈0.39; hidden-layer norms rose 1–2 % | A.5 | `CONFIRMED-NARROWER` | Output layer exact. Hidden-layer norms changed by ×1.0000 – 1.0178. The input layer, not mentioned, grew ×1.080 |
| B-PC2g | For fixed hidden features, curvature scales with the head, so the squared residual scales by 0.668² ≈ 0.45 in every bin | Analysis; A.5 | `CONFIRMED-NARROWER` | The algebra holds for a linear head on fixed features. The features were not fixed: the input layer, which feeds `first_omega_0 = 30`, grew 8 % |
| B-PC2h | The population's median per-bin R̃ fell 2.3–5.6× from steps 1–100 to 852–951 in every bin, and bins 13–15 by 2.3–2.9× | A.4: 2.28–5.60; bins 13–15: 2.28, 2.90, 2.84 | `CONFIRMED` | |
| B-PC2i | At initialization ‖a′‖ ≈ 1.9–2.4 × 10⁵ against ‖F_grav‖ ≈ 3–6, and R̄ ≈ ‖a′‖²/3 to four figures | `.planning/phases/55-architecture-characterization-probe/evidence/probe/20260906T035209Z/raw.json`, six cases | `CONFIRMED-NARROWER` | ‖a′‖ medians 1.92–2.41 × 10⁵. ‖F_grav‖ medians 2.81–5.91 (one case below 3). R̄/(‖a′‖²/3) = 1.00002–1.00014. These are 16-point medians from the Phase-55 probe |
| B-PC2j | The validation gate covered all 227 validation trajectories at steps 100…900; median `eps_H` 0.983–0.990 with no trend; none below 0.5; threshold 10⁻⁵ | `runs/stage0-v23g7-seed42/validation_gate/step-00000{100…900}.json`: 227 rows each, medians 0.9827–0.9900, minimum 0.880, every verdict FAIL; `pinn/verification/gate_metrics.py:64`, `:180-200` | `CONFIRMED` | |
| B-PC2k | So generation 7 tested IC-plus-data training of about 40 anchors with a causally weighted physics diagnostic attached, not the causal-training recipe | B-PC1d, B-PC1i, B-PC2a to B-PC2e | `CONFIRMED-NARROWER` | The IC and physics terms ran on 40 anchors. The data term ran on all 256 selected slots every step, so the data fit is not limited to about 40 trajectories |
| B-PC3a | At budget exhaustion the remaining budget is `max(max_epochs − adam_epochs_used, 0)` = 0; the stage-exit machine is polled once; an unmet gate returns HALT | `controllers.py:2690-2707` | `CONFIRMED` | |
| B-PC3b | The plateau path needs 50 consecutive steps with Δlog₁₀ L_phys > −5 × 10⁻³; its input is the per-step, single-anchor physics loss | `controllers.py:134-135`, `:518-562`, `:2169` | `CONFIRMED` | |
| B-PC3c | Longest qualifying run: 6 in generation 7, 4 in generation 6, 4 in the smoke; 433 resets in generation 7 | A.1 | `CONFIRMED` | |
| B-PC3d | Had invariant B not tripped, the stage would have ended at step 1000 with the learning rate near 0, without L-BFGS, and halted unless the gate passed | B-PC3a; the cosine law (B-PC11c) gives zero rate at step 1000 | `CONFIRMED` | |
| B-PC4a | The batch RNG stream depends only on pool sizes and per-key snapshot counts, never on model outputs | `batches.py:76-78`, `:238`, `:292`, `:348-367`, `:409-482`; A.2 reproduces every saved state from pool sizes and one snapshot count | `CONFIRMED` | |
| B-PC4b | Generations 6 and 7 and the smoke drew identical batch and anchor sequences | A.2 (each run's own checkpoints match the same replay); A.3 (anchors equal on all shared steps) | `CONFIRMED` | |
| B-PC4c | The smoke and the graded run are bit-identical at steps 1–2 and first differ at step 3, after their learning-rate schedules diverge | A.1 and the check below this table | `CONFIRMED-NARROWER` | Every loss term, weight statistic, front, and gradient norm is bit-identical at steps 1–2 and first differs at step 3. Logged `total` already differs at step 2, because the warm-up ramps differ (λ_phys 0.0333 vs 0.01). Logged `lr` differs from step 1, because it is the next step's rate under T_max 300 vs 1000 |
| B-PC4d | All three runs score the same monitor trajectory, 28 | A.2: each run's checkpoint monitor batch begins with 28 | `CONFIRMED` | |
| B-PC4e | On the same batches, trajectory 28's S₁ was equal to three decimals through step 271, then 2.575 vs 1.856 at step 286 and 0.460 vs 1.296 at step 409 | A.4 | `CONFIRMED` | |
| B-PC4f | The correlation of log IC loss between the runs over steps 270–513 is 0.17, against 0.11 for a one-step-shifted control | A.1: 0.167 (n = 244) and 0.114 | `CONFIRMED` | |
| B-PC4g | Generation 6 never completed a window | A-P5c | `CONFIRMED` | |
| B-PC4h | One experiment was observed twice through floating-point noise; when the front advances is not reproducible (353 vs 450) | B-PC4b, B-PC4e; `blocked-state-g6.json` (353); `step-000951.pt` `invariant_b_state` (450) | `CONFIRMED` | |
| B-PC5a | The package says no measurement relates an `R_ref`-relative front state to absolute accuracy | Master `:379` | `CONFIRMED` | |
| B-PC5b | The validation gate scored all 227 trajectories every 100th step; medians 0.986 / 0.983 / 0.984 / 0.984 / 0.984 / 0.986 / 0.990 / 0.989 / 0.987; every verdict FAIL | B-PC2j | `CONFIRMED` | |
| B-PC5c | Over the same steps the front went from 0 to 2 and the population's median R̃ fell about 3× | A.4 and the check below this table: the per-step 16-bin median fell ×3.29 (steps 1–100 vs 852–951), ×2.87 (around step 100 vs around 900) | `CONFIRMED` | |
| B-PC5d | `eps_H` is a self-consistency metric (matched-Plummer H of the predicted trajectory, velocities by finite differences), not error against Brutus, and on the validation split | `pinn/verification/gate_metrics.py:180-200`, `:211-220` | `CONFIRMED` | |
| B-PC6a | The package says the front "then made no further progress", the end state is "flat over the last 20 steps (1.192 → 1.189)", and the front "oscillates; it does not creep" | Prompt `:84`; verdict packet `:88-89` (Part B, `H-02`) | `CONFIRMED` | |
| B-PC6b | Trajectory 28's S₂ was about 2.1–2.6 at steps 470–481 and 1.12–1.40 at steps 892–943 | A.4 | `CONFIRMED` | |
| B-PC6c | The population median S₂ fell 2.33 → 0.99 (blocks 401–500 → 901–951) and S₁ fell 1.24 → 0.48 | A.4 | `CONFIRMED` | |
| B-PC6d | The last 20 steps hold about 0.03 % of the run's cumulative learning rate | A.1: 0.035 % | `CONFIRMED` | |
| B-PC6e | The prefix sums crept steadily while the discrete front hovered; H-02's arithmetic is right but "does not creep" is not | B-PC6b, B-PC6c, B-PC11b | `CONFIRMED-NARROWER` | The decline holds between blocks. Step to step it is noisy: trajectory 28's S₂ rises and falls across its appearances (A.4) |
| B-PC7a | F-09 attributes the training-batch front's spread to resampled batches | Master F-09 and prompt `:91-93` | `CONFIRMED-NARROWER` | The package calls the batches "resampled", which is true: each step draws a new batch, anchor included. It does not single out time resampling |
| B-PC7b | The dominant source of the spread is which trajectory the step evaluates; time resampling is minor | B-PC1q | `CONFIRMED` | |
| B-PC7c | The training-batch front reached 3 only on anchors 1 and 9 (111 and 70 steps), plus once on anchor 22 (35 steps) | A.3: 34 completed front-3 steps: anchor 9 ×17, anchor 1 ×16, anchor 22 ×1 | `CONFIRMED` | |
| B-PC7d | The 54-RULING premise that a high-water mark over changing samples is biased upward holds in direction, but its implied mechanism does not match what ran | B-PC7b, B-PC7c | `CONFIRMED` | Analysis consistent with the evidence |
| B-PC8a | GATE-04's controlled-reduction condition holds by construction: α = ln(√2)/P₁₅ makes w′₁₅ = 1/√2 | `57-RULING.md:61`, `:74` | `CONFIRMED` | |
| B-PC8b | It confirms `exp(−prefix)` is computed without floor clamping; it cannot test whether training moves residuals | Analysis; B-PC8a | `CONFIRMED` | |
| B-PC8c | GATE-04 ran single-trajectory cases with six different network seeds, so it did not exercise per-slot semantics | `gate04_train_free.py:703-754`; `r_ref_stage0.json` | `CONFIRMED-NARROWER` | Six single-trajectory cases but five distinct network seeds (41 twice, 42, 43, 0, 7). Five of the six use a zero IC13 and unit masses |
| B-PC8d | The initialization gradient imbalance was on record, and no gate examined it | B-PC2d; GATE-04's conditions concern weights and fronts only | `CONFIRMED` | |
| B-PC9a | `_global_epoch` increments once per Adam step, and the logged `epoch` equals `step` | `controllers.py:2165-2167`; A.1: 951 of 951 | `CONFIRMED` | |
| B-PC9b | So `max_epochs`, the plateau's "50 consecutive epochs", and `validation_every` are all counted in steps | B-PC9a; `controllers.py:2169`, `:2171` | `CONFIRMED` | |
| B-PC9c | The specs never define "epoch" for a replay batch scheme; a replay-coverage reading would make one Stage-0 pass ≈ 1,812/240 ≈ 7.6 steps | Searched every "epoch" in both live specs | `CONFIRMED-NARROWER` | No explicit definition exists. But `ctl_instruction.md:1829` (Phase-34 contract, GAP-34-01 Option A) rules that the replay set is "sampled without replacement across the epoch (standard once-per-epoch coverage)", which presupposes the coverage reading. See "Found by this check" item 1. The arithmetic (7.55) holds |
| B-PC10a | After B2 the physics/data raw-gradient ratio is about 16–520×; raw physics 91–758 against applied data 1.45–5.78 | A.1 | `CONFIRMED-NARROWER` | Raw physics spans 88.8–758 (minimum 88.76 at step 650). Measured step by step, raw physics / applied data is 21.6–243×. The 16–520× figure pairs extremes from different steps. Physics still leads data |
| B-PC10b | IC exceeds physics by 2.8 × 10⁴ – 2.6 × 10⁶ and data by about 10⁷ – 10⁸ | A.1 | `CONFIRMED-NARROWER` | IC/physics as stated. IC/data step by step is 2.1 × 10⁶ – 2.1 × 10⁸ |
| B-PC10c | 54-RULING's conditioning analysis did not include the IC term, which was dominant at initialization by about 10⁶ | `54-RULING.md:131-134` speaks of the "physics/data conditioning mismatch", and the ruling nowhere discusses the IC term's gradient scale; B-PC2d (IC/physics 1.8 × 10⁶) | `CONFIRMED` | |
| B-PC11a | F-03 recomputed from Part B: bins 0–5 fell 3.51, 2.73, 3.22, 2.21, 2.06, 1.51×; the 16-bin median 1.1058 → 0.6578 (×1.68) | The verdict packet's raw replay output (Appendix A rows): 3.507, 2.732, 3.216, 2.205, 2.055, 1.512; 1.1058 → 0.6578 | `CONFIRMED` | |
| B-PC11b | H-02's arithmetic: 41.7 % reduction; 3.88/0.693 = 5.6; a full front needs a 15-bin mean below 0.0462, 21.6× below 1 and 23.9× below 1.1058; raw bound 9.13 × 10⁸ | Recomputed from the same rows and `R_ref` | `CONFIRMED` | |
| B-PC11c | The logged `lr` matches `10⁻³(1 + cos(πs/1000))/2` to 3.4 × 10⁻¹⁵, fits T_max = n_adam = 1000, and is logged after `scheduler.step()` | A.1: 3.41 × 10⁻¹⁵; `controllers.py:2162-2163`, `:2179-2181`, `:2658-2660` | `CONFIRMED` | |
| B-PC11d | λ_phys = min(1, (step − 1)/100) exactly | A.1: 951 of 951 | `CONFIRMED` | |
| B-PC12a | The guard reads only the frozen monitor | `pinn/train.py:192-202` prefers the monitor's statistics and falls back to the training batch's. `controllers.py:2049-2051` evaluates the monitor before every Adam batch, so the fallback cannot fire there | `CONFIRMED` | |
| B-PC12b | Its state is a monotone high-water mark; transient regressions never reset the age | `pinn/training/guards.py:597-631` (the comment at `:599`) | `CONFIRMED` | |
| B-PC12c | With one trajectory, the high-water mark is a record statistic of one noisy, discretized series; its advance timing differed by about 100 steps between two runs on identical data | B-PC1p, B-PC4h (97 steps) | `CONFIRMED-NARROWER` | "Its noise amplitude scales with the learning rate" was not tested here |
| B-PC12d | 57-RULING §2 adds "no new front margin, observation cadence, or persistence-count threshold"; nothing tests the statistic's variance | `57-RULING.md:105-106` | `CONFIRMED` | |

**Checks referred to in the table.** These were run as inline commands, not as
appendix scripts; their output is quoted here.

- **Smoke vs graded, loss terms only (B-PC4c).** The first step at which any of
  `loss_ic`, `loss_phys`, `loss_data`, `front_idx`, `w_min`, `w_mean`, `w_max`,
  `grad_norm` differs is step 3. `lambda_phys` at step 2 is 0.0333 in the smoke
  and 0.01 in the graded run.
- **Per-step 16-bin median R̃ (B-PC5c).** Steps 1–100: 1.716. Steps 852–951:
  0.521, so ×3.29. Around step 100 (steps 91–110): 1.732. Around step 900 (steps
  891–910): 0.604, so ×2.87.

### Group C — Claude §2.13 (the F-row table and its notes)

| Row | Assertion | Evidence | Verdict | Note |
|---|---|---|---|---|
| C-F01 | Record 952 is the halted iteration; the failure checkpoint's model equals step 951's, and its RNG is one batch further | A.5: all 28 model tensors equal; A.2: the failure checkpoint's RNG equals the state after the 952 draw | `CONFIRMED` | |
| C-F02 | Every replayed value is a single-trajectory quantity (trajectory 28) | B-PC1p | `CONFIRMED` | |
| C-F03 | Factors 3.507, 2.732, 3.216, 2.205, 2.055, 1.512; median 1.1058 → 0.6578 | B-PC11a | `CONFIRMED` | |
| C-F04 | `lr` at step s is the rate for update s + 1; "0.001 at step 1" is 9.999975 × 10⁻⁴ rounded | `controllers.py:2162-2181`; A.1 | `CONFIRMED` | |
| C-F05 | No L-BFGS at budget exhaustion; the plateau path is inert; `train.log:964` logs a "budget-exhausted" hand-off after the invariant-B halt | B-PC3a to B-PC3c; `runs/stage0-v23g7-seed42/logs/train.log:964` (`trigger=budget-exhausted adam_epochs_used=952`, then HALT at `:965`). The trigger is the default set at `controllers.py:2040` and returned unchanged at `:2160` when the guard trips; `:2684-2688` and `:2998-3012` record and log it | `CONFIRMED` | |
| C-F06 | λ_phys = min(1, (step − 1)/I_warm) exactly; tying the warm-up to the Adam budget is the spec's formula | A.1; the spec `:699` | `CONFIRMED` | |
| C-F07 | `loss_ic` and `loss_phys` are single-anchor, exposure-dependent quantities | B-PC1r | `CONFIRMED` | |
| C-F08 | `raw` is the true global norm of the λ-free (still causally weighted, `R_ref`-normalized) term, before clipping | `controllers.py:2000-2009` | `CONFIRMED` | |
| C-F09 | Values confirmed; the "resampled" framing is qualified | B-PC7a | `CONFIRMED-NARROWER` | As B-PC7a |
| C-F10 | The guard's fallback to training-batch statistics is unreachable on the Adam path; the spec's "the fixed-monitor boundary above" points at nothing in that file | B-PC12a; the spec `:452` holds the phrase, and no earlier text in the file describes a monitor boundary | `CONFIRMED` | |
| C-F11 | Corroborated by GATE-04's stored late-bin-only diagnostics: all front 0 | `57-…/evidence/gate04/20260908T093626Z/raw.json`: `late_bin_only_response_front_idx` is 0 in all 6 cases × 9 perturbations | `CONFIRMED` | |
| C-F12 | Single-trajectory evaluation; five of six `R_ref` cases are synthetic (`ic13_mode: zero`, masses (1, 1, 1)), CPU float64; training used dataset ICs in float32 on MPS | `r_ref_stage0.json` cases and `configuration` (`cpu`, `float64`); config `precision: float32`, `device: mps` | `CONFIRMED` | |
| C-F13 | Parameters bit-identical through about step 269 (earlier differences are evaluation noise); identical batch and validation sequences for all 513 steps; identical monitor | A.2, A.3; the package digest (F-13): `loss_ic`, `total`, `grad_norm` bit-identical through step 269 | `CONFIRMED` | |
| C-F14 | The generation-5/6/7 smokes are bit-exact reproductions; the smoke monitor's instantaneous front was 0 again at steps 100/200/300 | Inline check: across the three smokes, `loss_ic`, `total`, `grad_norm`, `lr`, `front_idx`, `loss_data` are bit-identical on all 300 steps; `w_min`, `w_mean`, `loss_phys` differ on 65 (g6 vs g7) and 73 (g5 vs g7) steps | `CONFIRMED-NARROWER` · `NOT-VERIFIABLE-HERE` | Bit-exact as a training trajectory, not in every logged field. The instantaneous monitor front needs a forward pass. A checkpoint-only CPU recompute on the smoke's `step-000100/200/300.pt`, of the same kind as Part B, would settle it |
| C-F15 | Confirmed | Package row; not challenged | `CONFIRMED` | |
| C-F16 | Confirmed | Package row; not challenged | `CONFIRMED` | |
| C-F17 | Confirmed | Package row; not challenged | `CONFIRMED` | |
| C-F18 | Confirmed | Package row; not challenged | `CONFIRMED` | |
| C-N1 | Part G re-derived: the script's SHA-256 `d28c7d92…` matches with one trailing newline; the output matches 180/180 lines | The package audit's addendum (commit `86958a65`) re-ran the embedded digest and reproduced its output | `CONFIRMED` | |
| C-N2 | The monitor recompute from checkpoint contents reproduced all 8 Part B rows to 4 decimal places | The verdict packet's raw output has 8 rows (5 generation-7, 3 generation-6) | `CONFIRMED` (row count) · `NOT-VERIFIABLE-HERE` (the values) | The values need a forward pass |
| C-N3 | `pinn/`, `configs/`, `runs/`, and both live specs are byte-identical between the baseline and the report's pin; `pinn/` is identical between the generation-6 and generation-7 run commits | Method: the `git diff --stat` outputs are empty | `CONFIRMED` | |
| C-N4 | Part G's lead-in says the replay scores the monitor "at four checkpoints"; the packet's Appendix A and Part G's own notes say five generation-7 and three generation-6 | `v2.3-closure-evidence-bundle.md:1117`; the packet's 8 raw rows | `CONFIRMED` | A residual error the pre-handoff correction pass missed. The delivered bundle is left as delivered (D-15) |

## Roll-up per finding

| Finding | Holds? | Narrower form, where one applies |
|---|---|---|
| P1 (Codex) — physics discards collocation identities | **Holds** | — |
| P2 — the conformance evidence misses it | **Holds** | — |
| P3 — the monitor scores one identity | **Holds** | — |
| P4 — L-BFGS unreachable at Adam exhaustion | **Holds** | — |
| P5 — generations 6 and 7 not independent | **Holds, sharper** | Identical batches, anchors, and validation draws for all 513 shared steps |
| P6 — two numeric interpretations need qualification | **Holds** | The maximum discrepancy is at log line 53, not 57 |
| PC-1 (Claude) — single trajectory per step; monitor likewise | **Holds, narrower** | The verified non-conformance is the physics term (and so the monitor). The IC term is also anchored, but by preserved design, with no spec batch rule. The data term is per-slot. The monitor's numeric reproduction was not re-run |
| PC-2 — the causal physics term was effectively not trained | **Holds, narrower** | The data term trained on all selected slots, so the run was "single-anchor IC, per-slot data". The amplitude-shrinkage account omits the input layer's 8 % growth. Norm dominance is global, not shown per parameter |
| PC-3 — L-BFGS unreachable | **Holds** | — |
| PC-4 — generations 6 and 7 not independent; generation 6 never ran a full window | **Holds** | The smoke differs from the graded run in logged `total` and `lr` from step 1–2; its loss terms first differ at step 3 |
| PC-5 — an in-run absolute measurement exists | **Holds** | — |
| PC-6 — "no further progress" applies to the guard statistic | **Holds, narrower** | The prefix sums declined between blocks; step to step they are noisy, not steady |
| PC-7 — "resampled" mislabels the variation source | **Holds, narrower** | The package's word is accurate but incomplete; the anchor identity dominates the variation |
| PC-8 — "proven healthy at initialization" is narrower than it sounds | **Holds, narrower** | Five distinct network seeds, not six; five of six cases are synthetic |
| PC-9 — "epoch" means one step | **Holds, narrower** | The spec does say something: the Phase-34 rule of once-per-epoch replay coverage presupposes a pass-over-the-pool epoch |
| PC-10 — the binding imbalance was always IC | **Holds, narrower** | Per-step physics/data ratio 21.6–243×, not 16–520×; IC/data 2.1 × 10⁶ – 2.1 × 10⁸ |
| PC-11 — the verbatim and arithmetic premises | **Holds** | — |
| PC-12 — monitor robustness was never tested | **Holds** | The learning-rate scaling of the noise was not tested here |
| §2.13 (F-01 to F-18 and notes) | **Holds** | F-14's smoke-monitor front values and the monitor recompute values need a forward pass |

No finding fails. No assertion was refuted.

## Verdict counts

| Verdict | Group A | Group B | Group C | Total |
|---|---|---|---|---|
| `CONFIRMED` | 25 | 59 | 19 | 103 |
| `CONFIRMED-SHARPER` | 1 | 0 | 0 | 1 |
| `CONFIRMED-NARROWER` | 0 | 14 | 1 | 15 |
| `CONFIRMED` · `NOT-VERIFIABLE-HERE` | 0 | 1 | 1 | 2 |
| `CONFIRMED-NARROWER` · `NOT-VERIFIABLE-HERE` | 0 | 0 | 1 | 1 |
| **Total** | 26 | 74 | 22 | 122 |

## Found by this check, not by either report

1. **The spec's replay-coverage rule.**
   - `ctl_instruction.md:1829`, in the Phase-34 batch contract (GAP-34-01, owner-ratified Option A), reads: "the replay set is **sampled without replacement** across the epoch (standard once-per-epoch coverage)".
   - The code draws every batch independently: `rng.choice(1812, 240, replace=False)` once per step (`batches.py:76-78`, A.2). Trajectories therefore repeat across steps with no coverage guarantee.
   - Under the code's one-step "epoch" (B-PC9a) the rule is satisfied trivially. Under the pass-over-the-pool reading its parenthesis suggests, it is not.
   - This bears on PC-9 (Claude's gap G-6) and on Q4. Neither report cites the line.
2. **The data term is per-slot.**
   - `_data_term(batch.data_points)` (`controllers.py:1865`) fits 32 observed snapshots from each of the 256 selected trajectories every step, Stage-1 lookahead included.
   - Only the IC and physics terms are anchored. The energy and angular-momentum terms are anchored too, but carry zero weight.
   - So the run is better described as "per-slot data fitting, single-anchor IC and physics" than as training on about 40 trajectories. Both reports describe the anchoring correctly; Claude's PC-2 consequence understates the data term's reach.
3. **The input layer grew while the output layer shrank.**
   - From `stage-0-init.pt` to step 951, the input-layer weight norm grew ×1.080 while the output layer shrank ×0.668 (A.5). Hidden layers changed ×1.000–1.018.
   - The first layer feeds the `first_omega_0 = 30` sinusoid. Its growth raises the input frequency, which raises curvature. That works against the "amplitude shrinkage" account in PC-2 item 3.
   - The account remains plausible, since the observed per-bin drop (×2.3–5.6) exceeds the 0.45 the head alone predicts. But it is not the whole mechanism. This bears on Q3.
4. **The IC term's anchoring is preserved design, not part of the verified defect.**
   - Phase 57's plan refactored the physics path to the complete batch and told the executor to "Preserve IC, angular-momentum, optimizer, and curriculum behavior outside this bounded seam per D-01/D-16" (`57-02-PLAN.md:87`).
   - The spec's `L_IC` (`pinn_architecture.md` §3.3, `:509-515`) is written for one trajectory: a sum over the three bodies with no batch average.
   - So the IC term's one-trajectory evaluation predates Phase 57 and is spec-silent. Whether the IC term should cover every selected slot (it carries the dominant gradient, PC-2) is an open decision, not part of the verified non-conformance. Claude's PC-1 and headline group it with the physics term.

## What the verified premise layer establishes

These are facts, not rulings.

1. **The ratified causal objective did not run.**
   - Generation 7 computed its physics term on one trajectory per step: the lowest-ID of that step's 240 replay draws. The run saw 40 distinct trajectories, and three-quarters of its steps used one of the 10 lowest IDs.
   - Only the collocation times came from the per-slot allocation. The owner's Phase-57 Option A instruction and the 57-02 must-have required every selected slot to contribute physics gradients.
   - The IC term also runs on that one trajectory. That is pre-existing behavior Phase 57 kept on purpose, and the spec gives `L_IC` no batch rule, so it is an open question rather than a verified defect.
2. **The invariant-B monitor scored one trajectory (ID 28)**, which was the training anchor on 31 of 951 steps. Validation physics is one time point on one trajectory (ID 12).
3. **The Phase-57 conformance verifier could not detect this.** Its anchor check tests the sampler's keys, and its `anchor_only` field is a constant.
4. **L-BFGS could not run in this configuration.** At budget exhaustion its budget is zero, and the plateau trigger's longest qualifying streak was 6 of the required 50.
5. **Generations 6 and 7 are one experiment.** They used identical batches, anchors, validation draws, and monitor. Floating-point nondeterminism made them diverge from about step 270, and the front-advance timing differs between them by about 100 steps.
6. **The physics term barely moved, while the IC term dominated.**
   - The IC gradient exceeded the physics gradient by 2.8 × 10⁴ – 2.6 × 10⁶.
   - On consecutive steps with the same anchor, one update lowered that anchor's IC loss 65 % of the time and its physics loss 42 % of the time.
   - The validation energy-drift metric stayed at about 0.98 throughout.
   - The imbalance was on record at initialization, in the production-conformance evidence.
7. **The baseline must be redone after any fix.** `R_ref` and GATE-04 were measured on single-trajectory cases, five of six of them synthetic. Any change to selected-slot semantics is a named trigger to re-measure `R_ref` and re-run GATE-04.

## Appendix A — scripts and outputs

Each script is reproduced byte for byte. Its SHA-256 is the digest of the code
block's content plus one trailing newline. Outputs are the complete standard
output of the run that produced the numbers above.

### A.1 `r4v_logs.py` — log-derived claims

SHA-256 `50d97d2aeefa11fae456a2f0211346c5921e74d9622ecde247983ef240eab64d`

```python
"""Rule-19 re-derivation of the log-derived premise claims in the trainex-r4 reports.

Read-only. Run from the repository root:  python3 -B r4v_logs.py
"""
import json
import math
from pathlib import Path

PLATEAU_SLOPE, PLATEAU_COUNT = -5e-3, 50  # controllers.py:134-135


def load(run):
    rows = [json.loads(l) for l in (Path("runs") / run / "logs" / "train.log.jsonl").read_text().splitlines() if l.strip()]
    return rows, [r for r in rows if r["lr"] is not None]


g7, g7c = load("stage0-v23g7-seed42")
g6, g6c = load("stage0-v23g6-seed42")
sm7, sm7c = load("stage0-v23g7-smoke")

print("== P6 / F-06: total vs sum(lambda_k * loss_k), all records")
for name, rows in (("g7", g7), ("g6", g6)):
    worst = max(((abs(r["total"] - (r["lambda_ic"] * r["loss_ic"] + r["lambda_data"] * r["loss_data"]
                                      + r["lambda_phys"] * r["loss_phys"] + r["lambda_e"] * r["loss_energy"]
                                      + r["lambda_l"] * r["loss_angmom"])) / abs(r["total"]), r["step"]) for r in rows))
    exact = sum(1 for r in rows if r["total"] == (r["lambda_ic"] * r["loss_ic"] + r["lambda_data"] * r["loss_data"]
                                                   + r["lambda_phys"] * r["loss_phys"] + r["lambda_e"] * r["loss_energy"]
                                                   + r["lambda_l"] * r["loss_angmom"]))
    print(f"  {name}: max relative discrepancy {worst[0]:.3g} at step {worst[1]}; exactly equal in {exact}/{len(rows)} records")

print("== PC-3 / P4: plateau detector replayed on logged loss_phys of completed steps")
for name, rows in (("g7", g7c), ("g6", g6c), ("g7-smoke", sm7c)):
    prev, cons, longest, resets = None, 0, 0, 0
    for r in rows:
        x = math.log10(r["loss_phys"])
        if prev is None:
            cons = 0
        elif x - prev > PLATEAU_SLOPE:
            cons += 1
        else:
            cons, resets = 0, resets + 1
        longest = max(longest, cons)
        prev = x
    print(f"  {name}: completed steps {len(rows)}; longest qualifying run {longest}; resets (slope <= -5e-3) {resets}")

print("== PC-9: logged epoch vs step on completed records")
for name, rows in (("g7", g7c), ("g6", g6c)):
    print(f"  {name}: epoch == step on {sum(r['epoch'] == r['step'] for r in rows)}/{len(rows)}")

print("== PC-11 / F-04: lr law and lambda_phys law")
for name, rows in (("g7", g7c), ("g6", g6c)):
    rel = max(abs(r["lr"] - 1e-3 * (1 + math.cos(math.pi * r["step"] / 1000)) / 2) / (1e-3 * (1 + math.cos(math.pi * r["step"] / 1000)) / 2) for r in rows)
    lp = sum(r["lambda_phys"] == min(1.0, (r["step"] - 1) / 100) for r in rows)
    lp_close = max(abs(r["lambda_phys"] - min(1.0, (r["step"] - 1) / 100)) for r in rows)
    print(f"  {name}: max rel |lr - 1e-3(1+cos(pi s/1000))/2| = {rel:.3g}; lambda_phys == min(1,(s-1)/100) exactly on {lp}/{len(rows)}, max abs diff {lp_close:.3g}")
print(f"  g7 lr at step 1 = {g7c[0]['lr']!r}")

print("== PC-6 / headline: cumulative learning-rate shares (g7 completed steps; lr logged at s is the rate for update s+1)")
# Rate actually used by update s: the rate logged at step s-1, with 1e-3 for s = 1.
used = {1: 1e-3}
for r in g7c:
    used[r["step"] + 1] = r["lr"]
total = sum(used[s] for s in range(1, 952))
share = lambda a, b: sum(used[s] for s in range(a, b + 1)) / total
print(f"  last 20 updates (932..951): {100 * share(932, 951):.3f} %;  updates 451..951: {100 * share(451, 951):.2f} %;  updates 452..951: {100 * share(452, 951):.2f} %")
logged_total = sum(r["lr"] for r in g7c)
print(f"  using the logged lr directly: last 20 records {100 * sum(r['lr'] for r in g7c[-20:]) / logged_total:.3f} %; records 451..951 {100 * sum(r['lr'] for r in g7c if r['step'] >= 451) / logged_total:.2f} %")
print(f"  lr(step 450) / lr(step 951) = {next(r['lr'] for r in g7c if r['step'] == 450) / g7c[-1]['lr']:.1f}")

print("== PC-10 / F-08: gradient norms on grad_stats_complete steps (g7)")
d = [r for r in g7 if r["grad_stats_complete"]]
rp = [r["grad_norm_raw_phys"] for r in d]
ad = [r["grad_norm_applied_data"] for r in d]
rd = [r["grad_norm_raw_data"] for r in d]
print(f"  steps {[r['step'] for r in d]}")
print(f"  raw_phys {min(rp):.3g}..{max(rp):.3g}; applied_data {min(ad):.3g}..{max(ad):.3g}; raw_data {min(rd):.3g}..{max(rd):.3g}")
print(f"  raw_phys/applied_data per step: {min(a / b for a, b in zip(rp, ad)):.3g}..{max(a / b for a, b in zip(rp, ad)):.3g}")
print(f"  applied_ic/applied_phys: {min(r['grad_norm_applied_ic'] / r['grad_norm_applied_phys'] for r in d if r['grad_norm_applied_phys']):.3g}..{max(r['grad_norm_applied_ic'] / r['grad_norm_applied_phys'] for r in d if r['grad_norm_applied_phys']):.3g}")
print(f"  applied_ic/applied_data: {min(r['grad_norm_applied_ic'] / r['grad_norm_applied_data'] for r in d):.3g}..{max(r['grad_norm_applied_ic'] / r['grad_norm_applied_data'] for r in d):.3g}")
print(f"  zero applied_phys steps: {[r['step'] for r in d if not r['grad_norm_applied_phys']]}")

print("== PC-4: smoke vs graded, g6 vs g7")
F = ["lr", "front_idx", "total", "loss_ic", "loss_phys", "loss_data", "w_min", "w_mean", "w_max", "grad_norm"]
first = next(a["step"] for a, b in zip(sm7, g7) if any(a[f] != b[f] for f in F))
print(f"  g7-smoke vs g7: identical on all compared fields through step {first - 1}; step {first} differs in {[f for f in F if sm7[first - 1][f] != g7[first - 1][f]]}")
print(f"  smoke records: {len(sm7)}; smoke lr at steps 1..3: {[r['lr'] for r in sm7c[:3]]}; graded: {[r['lr'] for r in g7c[:3]]}")
pairs = [(a["loss_ic"], b["loss_ic"]) for a, b in zip(g6c, g7c) if 270 <= a["step"] <= 513]
sh = [(a["loss_ic"], b["loss_ic"]) for a, b in zip(g6c, g7c[1:]) if 270 <= a["step"] <= 512]


def corr(p):
    xs, ys = [math.log(x) for x, _ in p], [math.log(y) for _, y in p]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return sxy / math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))


print(f"  corr(log loss_ic g6, g7) over steps 270..513: {corr(pairs):.3f} (n={len(pairs)}); g6[s] vs g7[s+1] control: {corr(sh):.3f}")
print(f"  g6 completed steps: {len(g6c)}, last completed step {g6c[-1]['step']}; g6 records {len(g6)}")
```

Output:

```
== P6 / F-06: total vs sum(lambda_k * loss_k), all records
  g7: max relative discrepancy 1.14e-07 at step 53; exactly equal in 0/952 records
  g6: max relative discrepancy 1.14e-07 at step 53; exactly equal in 0/513 records
== PC-3 / P4: plateau detector replayed on logged loss_phys of completed steps
  g7: completed steps 951; longest qualifying run 6; resets (slope <= -5e-3) 433
  g6: completed steps 513; longest qualifying run 4; resets (slope <= -5e-3) 249
  g7-smoke: completed steps 300; longest qualifying run 4; resets (slope <= -5e-3) 151
== PC-9: logged epoch vs step on completed records
  g7: epoch == step on 951/951
  g6: epoch == step on 513/513
== PC-11 / F-04: lr law and lambda_phys law
  g7: max rel |lr - 1e-3(1+cos(pi s/1000))/2| = 3.41e-15; lambda_phys == min(1,(s-1)/100) exactly on 951/951, max abs diff 0
  g6: max rel |lr - 1e-3(1+cos(pi s/1000))/2| = 1.84e-15; lambda_phys == min(1,(s-1)/100) exactly on 513/513, max abs diff 0
  g7 lr at step 1 = 0.0009999975326009292
== PC-6 / headline: cumulative learning-rate shares (g7 completed steps; lr logged at s is the rate for update s+1)
  last 20 updates (932..951): 0.035 %;  updates 451..951: 23.58 %;  updates 452..951: 23.46 %
  using the logged lr directly: last 20 records 0.034 %; records 451..951 23.51 %
  lr(step 450) / lr(step 951) = 97.8
== PC-10 / F-08: gradient norms on grad_stats_complete steps (g7)
  steps [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950]
  raw_phys 88.8..758; applied_data 1.45..5.78; raw_data 1.45..5.78
  raw_phys/applied_data per step: 21.6..243
  applied_ic/applied_phys: 2.78e+04..2.62e+06
  applied_ic/applied_data: 2.08e+06..2.05e+08
  zero applied_phys steps: []
== PC-4: smoke vs graded, g6 vs g7
  g7-smoke vs g7: identical on all compared fields through step 0; step 1 differs in ['lr']
  smoke records: 300; smoke lr at steps 1..3: [0.000999972584682756, 0.0009998903417374227, 0.0009997532801828658]; graded: [0.0009999975326009292, 0.0009999901304280684, 0.000999977793554475]
  corr(log loss_ic g6, g7) over steps 270..513: 0.167 (n=244); g6[s] vs g7[s+1] control: 0.114
  g6 completed steps: 513, last completed step 513; g6 records 513
```

### A.2 `r4v_anchor_replay.py` — the per-step trajectory sequence, proved against checkpoint RNG states

SHA-256 `67327a96813c4c864cc8b5757ba9a12cfa7a15b539271bb5bd966be5e254594d`

```python
"""Rule-19 independent replay of the Stage-0 batch RNG stream (trainex-r4 PC-1 item 4).

Metadata only: reads runs/<run>/splits.json and checkpoint RNG states. Opens no
trajectory file of any split. Assumes every drawn record has N_SNAP snapshots and
validates that assumption (and the whole replay) by comparing the replayed numpy
PCG64 state with the state saved in every retained checkpoint.

Mirrors, call for call, pinn/data/batches.py at the run commit:
  select_stage_records   -> rng.choice(N0, 240, replace=False); rng.choice(N1, 16, replace=False)
  sample_data_points     -> per key: rng.gumbel(size=n); rng.choice(n - 16 items, 16, replace=False)
  sample_collocation_points (4096, 256 slots) -> 16 bins x 256 slots of one rng.uniform each
  validation (collocation_count=1) -> data points over the pool, then
      allocate_collocation_quota: rng.permutation(V); per key rng.uniform(0, T, size=0 or 1)

Run from the repository root with the project venv:  .venv/bin/python -B r4v_anchor_replay.py <run>
Writes the per-step anchor sequence to <scratchpad>/r4v_anchors_<run>.json.
"""
import json
import sys
from pathlib import Path

import numpy as np
import torch

RUN = sys.argv[1] if len(sys.argv) > 1 else "stage0-v23g7-seed42"
N_SNAP = 126
T_MAX = 10.0
N_BINS = 16
OUT = Path(__file__).with_name(f"r4v_anchors_{RUN}.json")
run_dir = Path("runs") / RUN

manifest = json.loads((run_dir / "splits.json").read_text())


def pool(split, stage):
    keys = [r["id"] for g in manifest["groups"] if g["split"] == split for r in g["records"]
            if r["variant"] == "hierarchical" and r["fidelity"] == "base" and r["stage"] == stage]
    return sorted(keys)  # RecordKey(variant, fidelity, id) sorts by id within hierarchical/base


P0, P1, PV = pool("train", 0), pool("train", 1), pool("validation", 0)
print(f"pools: stage-0 train {len(P0)}, stage-1 train {len(P1)}, stage-0 validation {len(PV)}")


def gen_from(state):
    bg = np.random.PCG64()
    bg.state = state
    return np.random.Generator(bg)


def same(rng, state):
    a, b = rng.bit_generator.state, state
    return (a["state"]["state"] == b["state"]["state"] and a["state"]["inc"] == b["state"]["inc"]
            and int(a["has_uint32"]) == int(b["has_uint32"]))


def data_points(rng, n_keys):
    for _ in range(n_keys):
        rng.gumbel(size=N_SNAP)
        rng.choice(np.arange(N_SNAP - 16), size=16, replace=False)


def uniform_in_bin(rng, b):
    lo = (b / N_BINS) * T_MAX
    if b < N_BINS - 1:
        rng.uniform(lo, ((b + 1) / N_BINS) * T_MAX)
    else:
        rng.uniform(lo, np.nextafter(T_MAX, np.inf))


def train_batch(rng):
    replay = sorted(P0[int(i)] for i in np.atleast_1d(rng.choice(len(P0), size=240, replace=False)))
    lookahead = sorted(P1[int(i)] for i in np.atleast_1d(rng.choice(len(P1), size=16, replace=len(P1) < 16)))
    data_points(rng, 256)
    for b in range(N_BINS):
        for _ in range(256):
            uniform_in_bin(rng, b)
    return replay, lookahead


def validation_batch(rng):
    data_points(rng, len(PV))
    recipients = rng.permutation(len(PV))[:1]
    for i in range(len(PV)):
        rng.uniform(0.0, T_MAX, size=1 if i in recipients else 0)


ckpts = {}
for p in sorted((run_dir / "checkpoints").glob("*.pt")):
    ck = torch.load(p, map_location="cpu", weights_only=True)
    if not isinstance(ck, dict) or "rng" not in ck:
        print(f"  (skipping {p.name}: no rng block; top-level keys {list(ck)[:8] if isinstance(ck, dict) else type(ck).__name__})")
        continue
    ckpts[p.name] = {
        "rng": ck["rng"]["numpy"],
        "step": ck.get("counters", {}).get("global_step"),
        "monitor_replay": [k["id"] if isinstance(k, dict) else (k[2] if isinstance(k, (list, tuple)) else k) for k in ck.get("front_monitor", {}).get("batch", {}).get("replay_keys", [])][:5],
    }
print("checkpoints:", {k: v["step"] for k, v in ckpts.items()})

start = torch.load(run_dir / "run_start_rng.pt", map_location="cpu", weights_only=True)
start_np = start["numpy"] if "numpy" in start else start["rng"]["numpy"]
rng = gen_from(start_np)
mon_replay, mon_look = train_batch(rng)
print(f"monitor batch from run_start_rng: replay begins {mon_replay[:5]}; checkpoint says "
      f"{next(v['monitor_replay'] for v in ckpts.values() if v['monitor_replay'])}")
init = ckpts.get("stage-0-init.pt")
print(f"state after monitor draw == stage-0-init.pt state: {same(rng, init['rng'])}")

log = [json.loads(l) for l in (run_dir / "logs" / "train.log.jsonl").read_text().splitlines() if l.strip()]
last = log[-1]["step"]
states = {}
anchors = {}
for step in range(1, last + 1):
    replay, _ = train_batch(rng)
    anchors[step] = replay[0]
    completed = any(r["step"] == step and r["lr"] is not None for r in log[step - 1:step])
    if completed and step % 100 == 0:
        validation_batch(rng)
    states[step] = rng.bit_generator.state

for name, v in ckpts.items():
    hits = [s for s, st in states.items() if same(gen_from(st), v["rng"])]
    if name == "stage-0-init.pt":
        continue
    print(f"  {name:32s} saved step {v['step']}: replay state matches after step(s) {hits}")

OUT.write_text(json.dumps({"run": RUN, "monitor_replay_first": mon_replay[0], "monitor_replay": mon_replay,
                           "anchors": anchors, "pool0": P0, "poolv_min": PV[0]}))
print(f"wrote {OUT.name}: {len(anchors)} steps")
```

Output, generation 7:

```
pools: stage-0 train 1812, stage-1 train 2074, stage-0 validation 227
  (skipping ckpt-158375347798.pt: no rng block; top-level keys ['tag', 'stage', 'run_controller'])
checkpoints: {'best.pt': 900, 'failure-stage-0-step-951.pt': 951, 'latest.pt': 951, 'stage-0-init.pt': 0, 'step-000931.pt': 931, 'step-000941.pt': 941, 'step-000951.pt': 951}
monitor batch from run_start_rng: replay begins [28, 90, 104, 147, 167]; checkpoint says [28, 90, 104, 147, 167]
state after monitor draw == stage-0-init.pt state: True
  best.pt                          saved step 900: replay state matches after step(s) [900]
  failure-stage-0-step-951.pt      saved step 951: replay state matches after step(s) [952]
  latest.pt                        saved step 951: replay state matches after step(s) [951]
  step-000931.pt                   saved step 931: replay state matches after step(s) [931]
  step-000941.pt                   saved step 941: replay state matches after step(s) [941]
  step-000951.pt                   saved step 951: replay state matches after step(s) [951]
wrote r4v_anchors_stage0-v23g7-seed42.json: 952 steps
```

Output, generation 6:

```
pools: stage-0 train 1812, stage-1 train 2074, stage-0 validation 227
  (skipping ckpt-38043381130.pt: no rng block; top-level keys ['tag', 'stage', 'run_controller'])
checkpoints: {'best.pt': 500, 'latest.pt': 510, 'stage-0-init.pt': 0, 'step-000490.pt': 490, 'step-000500.pt': 500, 'step-000510.pt': 510}
monitor batch from run_start_rng: replay begins [28, 90, 104, 147, 167]; checkpoint says [28, 90, 104, 147, 167]
state after monitor draw == stage-0-init.pt state: True
  best.pt                          saved step 500: replay state matches after step(s) [500]
  latest.pt                        saved step 510: replay state matches after step(s) [510]
  step-000490.pt                   saved step 490: replay state matches after step(s) [490]
  step-000500.pt                   saved step 500: replay state matches after step(s) [500]
  step-000510.pt                   saved step 510: replay state matches after step(s) [510]
wrote r4v_anchors_stage0-v23g6-seed42.json: 513 steps
```

Output, generation-7 smoke:

```
pools: stage-0 train 1812, stage-1 train 2074, stage-0 validation 227
  (skipping ckpt-154400428230.pt: no rng block; top-level keys ['tag', 'stage', 'run_controller'])
checkpoints: {'best.pt': 300, 'latest.pt': 300, 'stage-0-init.pt': 0, 'step-000100.pt': 100, 'step-000200.pt': 200, 'step-000300.pt': 300}
monitor batch from run_start_rng: replay begins [28, 90, 104, 147, 167]; checkpoint says [28, 90, 104, 147, 167]
state after monitor draw == stage-0-init.pt state: True
  best.pt                          saved step 300: replay state matches after step(s) [300]
  latest.pt                        saved step 300: replay state matches after step(s) [300]
  step-000100.pt                   saved step 100: replay state matches after step(s) [100]
  step-000200.pt                   saved step 200: replay state matches after step(s) [200]
  step-000300.pt                   saved step 300: replay state matches after step(s) [300]
wrote r4v_anchors_stage0-v23g7-smoke.json: 300 steps
```

### A.3 `r4v_anchor_stats.py` — statistics over the replayed sequences

SHA-256 `12233c3e9d2898c885d36065bf7e13f8b6eac21f33a0e18dd8a906658f9be1b6`

```python
"""Rule-19 statistics over the replayed anchor sequences (trainex-r4 PC-1, PC-2, PC-4, PC-7).

Reads the r4v_anchors_<run>.json files written by r4v_anchor_replay.py and the runs'
train.log.jsonl. Read-only. Run from the repository root:  python3 -B r4v_anchor_stats.py
"""
import collections
import json
import math
import statistics
from pathlib import Path

HERE = Path(__file__).parent


def load(run):
    a = json.loads((HERE / f"r4v_anchors_{run}.json").read_text())
    a["anchors"] = {int(k): v for k, v in a["anchors"].items()}
    log = [json.loads(l) for l in (Path("runs") / run / "logs" / "train.log.jsonl").read_text().splitlines() if l.strip()]
    return a, {r["step"]: r for r in log if r["lr"] is not None}


g7, g7log = load("stage0-v23g7-seed42")
g6, g6log = load("stage0-v23g6-seed42")
sm, smlog = load("stage0-v23g7-smoke")
P0 = g7["pool0"]
rank = {k: i + 1 for i, k in enumerate(P0)}
N0, K = len(P0), 240

print("== identical sequences across runs")
print(f"  g6 == g7 anchors on steps 1..513: {all(g6['anchors'][s] == g7['anchors'][s] for s in range(1, 514))}")
print(f"  smoke == g7 anchors on steps 1..300: {all(sm['anchors'][s] == g7['anchors'][s] for s in range(1, 301))}")

steps = sorted(g7log)
anc = [g7["anchors"][s] for s in steps]
cnt = collections.Counter(anc)
low10 = set(P0[:10])
print("== PC-1 item 4: anchors over the 951 completed generation-7 steps")
print(f"  distinct anchors: {len(cnt)}; steps on the 10 lowest-ID Stage-0 trajectories {P0[:10]}: "
      f"{sum(cnt[k] for k in low10)} = {100 * sum(cnt[k] for k in low10) / len(anc):.1f} %")
print(f"  most frequent: {cnt.most_common(8)}")
print(f"  monitor anchor (frozen batch replay_keys[0]): {g7['monitor_replay_first']}, Stage-0 rank {rank[g7['monitor_replay_first']]}")
m_steps = [s for s in steps if g7["anchors"][s] == g7["monitor_replay_first"]]
print(f"  steps whose training anchor is the monitor trajectory: {len(m_steps)}: {m_steps}")
print(f"  validation anchor (lowest stage-0 validation id): {g7['poolv_min']}")

print("== analytic anchor-rank distribution (min of 240 draws without replacement from 1812)")
lc = lambda n, k: math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
p = [math.exp(lc(N0 - r, K - 1) - lc(N0, K)) for r in range(1, N0 - K + 2)]
print(f"  sum p = {sum(p):.12f}; P(rank 1) = {p[0]:.4f} (240/1812 = {240 / 1812:.4f}); "
      f"mean rank = {sum((i + 1) * q for i, q in enumerate(p)):.3f}; effective number 1/sum p^2 = {1 / sum(q * q for q in p):.2f}")
print(f"  expected share of steps on ranks 1..10 = {100 * sum(p[:10]):.1f} %")

print("== PC-2 item 2: natural experiment (consecutive completed steps with the same anchor)")
for name, A, L in (("g7", g7, g7log), ("g6", g6, g6log)):
    pairs = [(s, s + 1) for s in sorted(L) if s + 1 in L and A["anchors"][s] == A["anchors"][s + 1]]
    dic = [math.log10(L[b]["loss_ic"]) - math.log10(L[a]["loss_ic"]) for a, b in pairs]
    dph = [L[b]["loss_phys"] - L[a]["loss_phys"] for a, b in pairs]
    dphl = [math.log10(L[b]["loss_phys"]) - math.log10(L[a]["loss_phys"]) for a, b in pairs]
    print(f"  {name}: {len(pairs)} pairs; IC fell in {sum(d < 0 for d in dic)}/{len(pairs)} = {100 * sum(d < 0 for d in dic) / len(pairs):.0f} % "
          f"(median dlog10 {statistics.median(dic):+.3f} = {100 * (10 ** statistics.median(dic) - 1):+.0f} %); "
          f"phys fell in {sum(d < 0 for d in dph)}/{len(pairs)} = {100 * sum(d < 0 for d in dph) / len(pairs):.0f} % "
          f"(median d {statistics.median(dph):+.4f}; median dlog10 {statistics.median(dphl):+.4f})")

print("== PC-1 (c): IC loss by anchor")
for k in (P0[0], P0[1], g7["monitor_replay_first"]):
    ss = [s for s in steps if g7["anchors"][s] == k]
    tail = [(s, round(g7log[s]["loss_ic"], 1)) for s in ss if s >= 850]
    print(f"  id {k}: {len(ss)} steps; IC loss on its appearances from step 850: {tail}")
mn = min(steps, key=lambda s: g7log[s]["loss_ic"])
print(f"  run-minimum loss_ic {g7log[mn]['loss_ic']:.4g} at step {mn}, anchor {g7['anchors'][mn]}")

print("== PC-7: anchors on steps with training-batch front_idx == 3")
f3 = [s for s in steps if g7log[s]["front_idx"] == 3]
f3a = collections.Counter(g7["anchors"][s] for s in f3)
print(f"  {len(f3)} completed steps with front 3; by anchor (anchor: front-3 steps / its total steps): "
      f"{[(k, v, cnt[k]) for k, v in f3a.most_common()]}")
```

Output:

```
== identical sequences across runs
  g6 == g7 anchors on steps 1..513: True
  smoke == g7 anchors on steps 1..300: True
== PC-1 item 4: anchors over the 951 completed generation-7 steps
  distinct anchors: 40; steps on the 10 lowest-ID Stage-0 trajectories [0, 1, 3, 5, 8, 9, 11, 13, 18, 22]: 710 = 74.7 %
  most frequent: [(0, 132), (1, 111), (9, 70), (3, 70), (5, 69), (8, 68), (11, 60), (18, 53)]
  monitor anchor (frozen batch replay_keys[0]): 28, Stage-0 rank 13
  steps whose training anchor is the monitor trajectory: 31: [17, 179, 204, 232, 271, 286, 290, 296, 330, 334, 336, 350, 409, 470, 476, 477, 481, 551, 624, 642, 687, 704, 709, 738, 757, 785, 813, 892, 901, 908, 943]
  validation anchor (lowest stage-0 validation id): 12
== analytic anchor-rank distribution (min of 240 draws without replacement from 1812)
  sum p = 0.999999999999; P(rank 1) = 0.1325 (240/1812 = 0.1325); mean rank = 7.523; effective number 1/sum p^2 = 14.07
  expected share of steps on ranks 1..10 = 75.9 %
== PC-2 item 2: natural experiment (consecutive completed steps with the same anchor)
  g7: 57 pairs; IC fell in 37/57 = 65 % (median dlog10 -0.144 = -28 %); phys fell in 24/57 = 42 % (median d +0.0004; median dlog10 +0.0020)
  g6: 32 pairs; IC fell in 22/32 = 69 % (median dlog10 -0.106 = -22 %); phys fell in 13/32 = 41 % (median d +0.0019; median dlog10 +0.0076)
== PC-1 (c): IC loss by anchor
  id 0: 132 steps; IC loss on its appearances from step 850: [(854, 1528.0), (863, 1998.5), (871, 402.2), (884, 136.2), (900, 84.3), (909, 75.7), (913, 73.9), (915, 59.1), (923, 40.0), (927, 34.0), (929, 27.4), (947, 25.7)]
  id 1: 111 steps; IC loss on its appearances from step 850: [(852, 5905.1), (859, 4334.0), (867, 8479.7), (869, 9227.1), (881, 10358.6), (893, 7024.5), (898, 3053.7), (899, 2043.9), (905, 3501.3), (910, 1032.5), (911, 699.3), (918, 1851.0), (934, 1564.6), (935, 1121.8), (936, 508.1), (940, 621.4)]
  id 28: 31 steps; IC loss on its appearances from step 850: [(892, 22082.7), (901, 2341.9), (908, 12180.1), (943, 5869.5)]
  run-minimum loss_ic 25.71 at step 947, anchor 0
== PC-7: anchors on steps with training-batch front_idx == 3
  34 completed steps with front 3; by anchor (anchor: front-3 steps / its total steps): [(9, 17, 70), (1, 16, 111), (22, 1, 35)]
```

### A.4 `r4v_tb.py` — per-bin residuals from the TensorBoard event files

SHA-256 `b150a3ce15b00ba8c00bb332cde92a89a343525b975c868eba16eb661c9b773b`

```python
"""Rule-19 re-derivation of the TensorBoard-based premise claims (trainex-r4 PC-1(b), PC-2, PC-4, PC-6).

Reads runs/<run>/tb/events.out.tfevents.* with a minimal TFRecord + protobuf reader
(no tensorboard package is installed), joins the per-step normalized bin residuals
(tag residuals/bin_XX, the training batch's own anchor) with the replayed anchor
sequence (r4v_anchors_<run>.json). Read-only.  Run from the repository root:
    python3 -B r4v_tb.py
"""
import collections
import json
import math
import statistics
import struct
from pathlib import Path

HERE = Path(__file__).parent


def varint(b, i):
    shift = result = 0
    while True:
        c = b[i]
        i += 1
        result |= (c & 0x7F) << shift
        if not c & 0x80:
            return result, i
        shift += 7


def fields(b):
    i = 0
    while i < len(b):
        key, i = varint(b, i)
        num, wt = key >> 3, key & 7
        if wt == 0:
            v, i = varint(b, i)
        elif wt == 1:
            v, i = b[i:i + 8], i + 8
        elif wt == 2:
            n, i = varint(b, i)
            v, i = b[i:i + n], i + n
        elif wt == 5:
            v, i = b[i:i + 4], i + 4
        else:
            raise ValueError(f"wire type {wt}")
        yield num, wt, v


def scalars(run):
    out = collections.defaultdict(dict)
    for path in sorted((Path("runs") / run / "tb").glob("events.out.tfevents.*")):
        data = path.read_bytes()
        i = 0
        while i < len(data):
            (n,) = struct.unpack("<Q", data[i:i + 8])
            rec = data[i + 12:i + 12 + n]
            i += 12 + n + 4
            step, summary = None, None
            for num, wt, v in fields(rec):
                if num == 2 and wt == 0:
                    step = v
                elif num == 5 and wt == 2:
                    summary = v
            if summary is None:
                continue
            for num, wt, v in fields(summary):
                if num != 1:
                    continue
                tag, val = None, None
                for n2, w2, v2 in fields(v):
                    if n2 == 1:
                        tag = v2.decode()
                    elif n2 == 2 and w2 == 5:
                        (val,) = struct.unpack("<f", v2)
                if tag is not None and val is not None:
                    out[tag][step] = val
    return out


def anchors(run):
    return {int(k): v for k, v in json.loads((HERE / f"r4v_anchors_{run}.json").read_text())["anchors"].items()}


def bins(tb, step):
    return [tb[f"residuals/bin_{b:02d}"].get(step) for b in range(16)]


tb7, tb6 = scalars("stage0-v23g7-seed42"), scalars("stage0-v23g6-seed42")
a7, a6 = anchors("stage0-v23g7-seed42"), anchors("stage0-v23g6-seed42")
log7 = {r["step"]: r for r in (json.loads(l) for l in Path("runs/stage0-v23g7-seed42/logs/train.log.jsonl").read_text().splitlines() if l.strip())}
log6 = {r["step"]: r for r in (json.loads(l) for l in Path("runs/stage0-v23g6-seed42/logs/train.log.jsonl").read_text().splitlines() if l.strip())}
print(f"tags g7: {len(tb7)} (residual bins present: {sum(1 for t in tb7 if t.startswith('residuals/bin_'))}); "
      f"points per bin tag: {len(tb7['residuals/bin_00'])}; steps {min(tb7['residuals/bin_00'])}..{max(tb7['residuals/bin_00'])}")
fr = sum(1 for s, r in log7.items() if tb7["causal/front_idx"].get(s) == r["front_idx"])
print(f"causal/front_idx equals logged front_idx on {fr}/{len(log7)} records")
S = lambda tb, s, k: sum(bins(tb, s)[:k + 1])
done7 = sorted(s for s, r in log7.items() if r["lr"] is not None)
done6 = sorted(s for s, r in log6.items() if r["lr"] is not None)

print("== PC-2 item 2: S2 = R0+R1+R2 in the consecutive same-anchor pairs")
for name, tb, A, done in (("g7", tb7, a7, done7), ("g6", tb6, a6, done6)):
    ds = set(done)
    pairs = [(s, s + 1) for s in done if s + 1 in ds and A[s] == A[s + 1]]
    d = [S(tb, b, 2) - S(tb, a, 2) for a, b in pairs]
    print(f"  {name}: {len(pairs)} pairs; S2 fell in {sum(x < 0 for x in d)}/{len(pairs)} = {100 * sum(x < 0 for x in d) / len(pairs):.0f} %; median dS2 {statistics.median(d):+.4f}")

print("== PC-2 item 3: median per-bin R~ over steps 1-100 vs 852-951 (g7 completed steps)")
early = [s for s in done7 if s <= 100]
late = [s for s in done7 if 852 <= s <= 951]
ratios = []
for b in range(16):
    e = statistics.median(tb7[f"residuals/bin_{b:02d}"][s] for s in early)
    l = statistics.median(tb7[f"residuals/bin_{b:02d}"][s] for s in late)
    ratios.append(e / l)
print("  early/late ratio by bin: " + ", ".join(f"{b}:{r:.2f}" for b, r in enumerate(ratios)))
print(f"  min {min(ratios):.2f}, max {max(ratios):.2f}; bins 13-15: {[round(r, 2) for r in ratios[13:]]}")

print("== PC-6: trajectory 28 and population prefix sums (g7)")
m = [s for s in done7 if a7[s] == 28]
print("  trajectory-28 steps with S1, S2: " + ", ".join(f"{s}:{S(tb7, s, 1):.3f}/{S(tb7, s, 2):.3f}" for s in m))
blk = lambda lo, hi, k: statistics.median(S(tb7, s, k) for s in done7 if lo <= s <= hi)
print(f"  population median S2: steps 401-500 {blk(401, 500, 2):.3f}, 901-951 {blk(901, 951, 2):.3f}; "
      f"median S1: 401-500 {blk(401, 500, 1):.3f}, 901-951 {blk(901, 951, 1):.3f}")

print("== PC-4 item 2: trajectory-28 S1 in g6 vs g7 on the same steps (anchor 28 in both)")
both = [s for s in m if s <= 513 and a6.get(s) == 28 and s in log6]
print("  " + ", ".join(f"{s}: g6 {S(tb6, s, 1):.3f} / g7 {S(tb7, s, 1):.3f}" for s in both))

print("== PC-1 (b): time resampling at (nearly) fixed parameters, trajectory 28")
print(f"  step 901 S1 {S(tb7, 901, 1):.4f} (monitor at best.pt / step 900, F-02: 0.728); "
      f"step 943 S2 {S(tb7, 943, 2):.4f} (monitor at 941 / 951, F-02: 1.182 / 1.189)")

print("== PC-1 (b): share of detrended log R~ variance explained by anchor identity (g7, bins 0-2)")
for b in range(3):
    xs = [(s, math.log(tb7[f"residuals/bin_{b:02d}"][s])) for s in done7]
    for w in (25, 51, 101):
        trend = {}
        vals = [v for _, v in xs]
        for i, (s, _) in enumerate(xs):
            lo, hi = max(0, i - w // 2), min(len(xs), i + w // 2 + 1)
            trend[s] = statistics.median(vals[lo:hi])
        res = [(a7[s], v - trend[s]) for s, v in xs]
        mean = statistics.fmean(r for _, r in res)
        groups = collections.defaultdict(list)
        for k, r in res:
            groups[k].append(r)
        ss_tot = sum((r - mean) ** 2 for _, r in res)
        ss_between = sum(len(g) * (statistics.fmean(g) - mean) ** 2 for g in groups.values())
        print(f"  bin {b}, centered rolling-median window {w}: eta^2 = {100 * ss_between / ss_tot:.0f} %")
```

Output:

```
tags g7: 53 (residual bins present: 16); points per bin tag: 952; steps 1..952
causal/front_idx equals logged front_idx on 952/952 records
== PC-2 item 2: S2 = R0+R1+R2 in the consecutive same-anchor pairs
  g7: 57 pairs; S2 fell in 28/57 = 49 %; median dS2 +0.0008
  g6: 32 pairs; S2 fell in 12/32 = 38 %; median dS2 +0.1225
== PC-2 item 3: median per-bin R~ over steps 1-100 vs 852-951 (g7 completed steps)
  early/late ratio by bin: 0:5.60, 1:4.66, 2:3.75, 3:2.43, 4:2.91, 5:4.38, 6:2.76, 7:2.93, 8:3.81, 9:2.45, 10:3.03, 11:3.34, 12:3.13, 13:2.28, 14:2.90, 15:2.84
  min 2.28, max 5.60; bins 13-15: [2.28, 2.9, 2.84]
== PC-6: trajectory 28 and population prefix sums (g7)
  trajectory-28 steps with S1, S2: 17:3.075/3.869, 179:3.839/5.855, 204:2.806/4.758, 232:2.600/4.122, 271:1.300/2.687, 286:1.856/4.007, 290:2.185/4.763, 296:2.037/4.881, 330:1.105/2.479, 334:1.473/2.996, 336:2.048/4.033, 350:1.768/4.424, 409:1.296/2.216, 470:0.949/2.088, 476:0.950/2.530, 477:1.015/2.303, 481:1.169/2.605, 551:1.085/1.667, 624:0.758/2.431, 642:1.247/2.423, 687:1.056/1.687, 704:1.013/1.616, 709:1.265/1.695, 738:0.706/1.325, 757:0.679/1.293, 785:0.898/1.373, 813:0.943/1.362, 892:0.658/1.262, 901:0.779/1.401, 908:0.777/1.384, 943:0.533/1.120
  population median S2: steps 401-500 2.334, 901-951 0.991; median S1: 401-500 1.244, 901-951 0.482
== PC-4 item 2: trajectory-28 S1 in g6 vs g7 on the same steps (anchor 28 in both)
  17: g6 3.075 / g7 3.075, 179: g6 3.839 / g7 3.839, 204: g6 2.806 / g7 2.806, 232: g6 2.600 / g7 2.600, 271: g6 1.300 / g7 1.300, 286: g6 2.575 / g7 1.856, 290: g6 2.000 / g7 2.185, 296: g6 2.061 / g7 2.037, 330: g6 1.450 / g7 1.105, 334: g6 0.864 / g7 1.473, 336: g6 1.191 / g7 2.048, 350: g6 0.997 / g7 1.768, 409: g6 0.460 / g7 1.296, 470: g6 1.046 / g7 0.949, 476: g6 1.803 / g7 0.950, 477: g6 2.159 / g7 1.015, 481: g6 1.097 / g7 1.169
== PC-1 (b): time resampling at (nearly) fixed parameters, trajectory 28
  step 901 S1 0.7791 (monitor at best.pt / step 900, F-02: 0.728); step 943 S2 1.1197 (monitor at 941 / 951, F-02: 1.182 / 1.189)
== PC-1 (b): share of detrended log R~ variance explained by anchor identity (g7, bins 0-2)
  bin 0, centered rolling-median window 25: eta^2 = 50 %
  bin 0, centered rolling-median window 51: eta^2 = 52 %
  bin 0, centered rolling-median window 101: eta^2 = 52 %
  bin 1, centered rolling-median window 25: eta^2 = 27 %
  bin 1, centered rolling-median window 51: eta^2 = 27 %
  bin 1, centered rolling-median window 101: eta^2 = 27 %
  bin 2, centered rolling-median window 25: eta^2 = 19 %
  bin 2, centered rolling-median window 51: eta^2 = 20 %
  bin 2, centered rolling-median window 101: eta^2 = 20 %
```

### A.5 `r4v_ckpt.py` — checkpoint tensors

SHA-256 `538f437e802e6ea879f448144c747b5a748b510cc95c878f3f411d8d82480b86`

```python
"""Rule-19 re-derivation of the checkpoint-based premise claims (trainex-r4 P3, PC-2, F-01).

Tensor reads only (torch.load(..., weights_only=True)); no model is built and no forward
pass is run. Run from the repository root:  .venv/bin/python -B r4v_ckpt.py
"""
import collections
import json
import math
from pathlib import Path

import torch

R = Path("runs/stage0-v23g7-seed42")
ld = lambda name: torch.load(R / "checkpoints" / name, map_location="cpu", weights_only=True)
init, s951, fail = ld("stage-0-init.pt"), ld("step-000951.pt"), ld("failure-stage-0-step-951.pt")

print("== P3: frozen monitor record keys (step-000951.pt)")
keys = [tuple(k) for k in s951["front_monitor"]["record_keys"]]
c = collections.Counter(keys)
print(f"  rows {len(keys)}; distinct keys {len(c)}; rows per key {sorted(set(c.values()))}; first row key {keys[0]}")
b = s951["front_monitor"]["batch"]
print(f"  batch replay keys {len(b['replay_keys'])} (first {b['replay_keys'][0]}), lookahead {len(b['lookahead_keys'])}")

print("== PC-2 item 1: Adam moment ratio |m_hat| / sqrt(v_hat) at step 951")
opt = s951["optimizer"]
g = opt["param_groups"][0]
b1, b2 = g["betas"]
ratios = []
for st in opt["state"].values():
    t = float(st["step"])
    mh = st["exp_avg"] / (1 - b1 ** t)
    vh = st["exp_avg_sq"] / (1 - b2 ** t)
    ok = vh > 0
    ratios.append((mh[ok].abs() / vh[ok].sqrt()).reshape(-1))
r = torch.cat(ratios)
print(f"  betas {g['betas']}, eps {g['eps']}, lr {g['lr']:.4g}; elements {r.numel()}; median {r.median().item():.4f}; "
      f"p90 {torch.quantile(r[torch.randperm(r.numel(), generator=torch.Generator().manual_seed(0))[:2_000_000]], 0.9).item():.4f} (2M-element sample); "
      f"mean {r.mean().item():.4f}")

print("== PC-2 item 3: weight norms, stage-0-init vs step 951")
for name in ("output_layer.weight",):
    a, z = init["model"][name], s951["model"][name]
    print(f"  {name}: Frobenius {a.norm():.4f} -> {z.norm():.4f} (x{(z.norm() / a.norm()).item():.4f}); "
          f"row norms init {[round(x, 3) for x in a.norm(dim=1).tolist()]} -> 951 {[round(x, 3) for x in z.norm(dim=1).tolist()]}")
chg = {n: (s951["model"][n].norm() / init["model"][n].norm()).item() for n in init["model"] if n.endswith("weight") and n.startswith("hidden")}
print(f"  hidden-layer weight norm ratios 951/init: min {min(chg.values()):.4f}, max {max(chg.values()):.4f}")
print(f"  input_layer.weight ratio {(s951['model']['input_layer.weight'].norm() / init['model']['input_layer.weight'].norm()).item():.4f}")

print("== F-01: failure checkpoint model vs step-000951 model")
same = all(torch.equal(fail["model"][n], s951["model"][n]) for n in s951["model"])
print(f"  all {len(s951['model'])} model tensors identical: {same}; failure counters {fail['counters']}; curriculum {fail['curriculum']}")

print("== PC-2 item 1: gradient clipping, logged pre-clip norm / (8.5 x torch-median of the last <=100 norms incl. current)")
log = [json.loads(l) for l in (R / "logs" / "train.log.jsonl").read_text().splitlines() if l.strip()]
norms, peak = [], (0.0, None)
for row in log:
    if row["grad_norm"] is None or row["lr"] is None:
        continue
    norms.append(row["grad_norm"])
    window = torch.tensor(norms[-100:])
    thr = 8.5 * max(window.median().item(), 1e-6)
    if row["grad_norm"] / thr > peak[0]:
        peak = (row["grad_norm"] / thr, row["step"])
print(f"  peak ratio {peak[0]:.3f} at step {peak[1]} (clipping binds only above 1.0)")
```

Output:

```
== P3: frozen monitor record keys (step-000951.pt)
  rows 4096; distinct keys 256; rows per key [16]; first row key ('hierarchical', 'base', 28)
  batch replay keys 240 (first ['hierarchical', 'base', 28]), lookahead 16
== PC-2 item 1: Adam moment ratio |m_hat| / sqrt(v_hat) at step 951
  betas (0.9, 0.999), eps 1e-08, lr 5.913e-06; elements 795657; median 0.0389; p90 0.1147 (2M-element sample); mean 0.0522
== PC-2 item 3: weight norms, stage-0-init vs step 951
  output_layer.weight: Frobenius 1.7525 -> 1.1715 (x0.6685); row norms init [0.596, 0.613, 0.564, 0.59, 0.572, 0.627, 0.543, 0.583, 0.566] -> 951 [0.394, 0.402, 0.388, 0.381, 0.377, 0.411, 0.372, 0.402, 0.385]
  hidden-layer weight norm ratios 951/init: min 1.0000, max 1.0178
  input_layer.weight ratio 1.0798
== F-01: failure checkpoint model vs step-000951 model
  all 28 model tensors identical: True; failure counters {'global_step': 951, 'global_epoch': 951, 'wall_clock_baseline': 158362.682789208}; curriculum {'stage': 0, 'phase': '2a', 'epoch': 952, 'step': 951, 'disposition_log_pointer': None}
== PC-2 item 1: gradient clipping, logged pre-clip norm / (8.5 x torch-median of the last <=100 norms incl. current)
  peak ratio 0.741 at step 941 (clipping binds only above 1.0)
```
