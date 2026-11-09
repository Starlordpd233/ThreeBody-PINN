# Milestones

## v2.5 Root-Cause Confirmation (Shipped: 2026-11-08)

**Phases completed:** 5 of 5 phases (65–69), 32 plans, 82 tasks; 325 commits (`dbc96887..ef76e00f`), 2026-10-27 → 2026-11-08

**Verdict & owner decisions:** Suspect 1 ("the network is too small") refuted for one Stage-0 orbit (`EXP-01` 1-layer 384-wide SIREN, `157,065` params vs `795,657` locked, reached settled Tier 1 on all three runs; `EXP-03` locked `12×256` control at `lr = 1e-4` also reached settled Tier 1 on all three runs: `E = 0.04069, 0.09550, 0.03492`); Suspect 2 ("the metrics are too harsh") confirmed in part on finite-difference energy measurement (`YARD-01`: Brutus exact answer fails FD energy gate `0.00109..0.02380` on gold and `0.047..0.38` on base while passing at `1.07e-14..2.09e-14` with exact velocities, and constant predictor passes energy gate at `eps_H = 0.0` / `SCS = -inf`); Suspect 3 ("the training pipeline is wrong") split into training settings (`lr = 1e-3` confirmed-worsening at `E = 1.4552, 1.2422, 1.1583` vs `lr = 1e-4` settled Tier 1 in `EXP-03`, while retrospective Phase 60 attribution remains open across co-varying recipe differences) and the physics-term half (carried into v2.6 by name). **Owner checkpoints:** Checkpoint ① (`66-CHECKPOINT-1-RULING.md`, 2026-11-01): `phase67-as-planned`; `EXP-03` `REFUTED-LEAD` continuation (`67-EXP03-RULING.md`, 2026-11-08): `proceed with option 1`; Checkpoint ② (`68-CHECKPOINT-2-RULING.md`, 2026-11-08): `C-7: A` (autograd velocities), closing `GAP-59-08`, `C-2, C-4, C-5, C-6` left open for separate discussion, `ROUT-68-01..05` routed to v2.6; Checkpoint ③ (`69-RULING.md`, 2026-11-08): selected **Direction A** (keep the current `12×256` architecture as the supervised fit control and prioritize the training recipe and physics pipeline in v2.6) and commissioned **`trainex-r5`** on the focused redesign question. Requirements: 13/13 Complete; scope boundaries `SCOPE-45..49` held throughout. No graded run, no held-out evaluation, no test-split file opened; `29.90` measured machine hours (`107,626.594706` UTC seconds across 129 published attempts and 1 yardstick capture) on this Mac.

**Key accomplishments:**

- Put the 2026-10-27 read-only probe on the record across all seven committed Phase 60 arms (`DIAG-09`: `144/144` required fields reproduced, verdict `retained`) and built and sealed the `INST-08` single-orbit fit harness with Stage-0 training-split guards, `inst08-diagnostic` checkpoint refusal across `evaluate.py` and `train.py`, and a 20-step MPS smoke run (`0.014265 s/step`, Phase 65).
- Ran the small-network control (`EXP-01`: 1-hidden-layer 384-wide SIREN, `157,065` params, `first_omega_0 = 1000`, `lr = 1e-4`, `N = 465,000` steps), reaching settled Tier 1 on all three runs (`1632/s42` `E = 0.01143`, `851/s42` `E = 0.01721`, `1632/s41` `E = 0.07898`) and refuting "too small" for single-orbit supervised fitting (Phase 66).
- Executed the four pre-registered design and settings ladders (`EXP-02` depth, `EXP-03` learning rate, `EXP-04` time-input design, `EXP-05` window length: 4 metadata captures, 60 blind timing rows and 60 single-look science rows over `28.30` machine hours). In `EXP-03`, `lr = 1e-3` was confirmed-worsening while the locked `12×256` (`first_omega_0 = 30`) control at `lr = 1e-4` reached settled Tier 1 on all three cases (`E = 0.04069, 0.09550, 0.03492` at `N = 155,100`), refuting the hypothesis that the locked 12-layer architecture cannot fit one Stage-0 orbit; `EXP-02`, `EXP-04` and `EXP-05` completed under the owner's `REFUTED-LEAD` continuation ruling and read `unsettled-continue` (Phase 67).
- Audited every production and feasibility metric against Brutus's exact trajectory and the constant predictor (`YARD-01..03`), proving that finite-difference velocities fail Brutus's exact answer on the energy gate while exact velocities pass at `1.07e-14..2.09e-14` and the constant predictor passes the standalone energy gate at `eps_H = 0.0` / `SCS = -inf`; closed `GAP-59-08` under `C-7: A` and routed `ROUT-68-01..05` to v2.6 (Phase 68).
- Published the plain-language findings (`69-FINDINGS.md`), retrospective recipe comparison (`69-EVIDENCE.md`), Mac compute and SCOPE-49 accounting (`69-ACCOUNTING.md`), fail-closed verifier (`verify_phase69.py`), owner Checkpoint ③ ruling (`69-RULING.md`), and v2.6 handoff (`69-HANDOFF.md`), with `VER-23` re-verified at 13/13/13 (Phase 69).

**Known gaps / routed obligations:** 0 unsatisfied v2.5 requirements. `ROUT-68-01..05` (autograd velocity wiring in `validation_gate.py`, `evaluate.py`, and `pinn_architecture.md` §10.6; pairing energy gate with position accuracy; `C-11` rewrite of `ctl_instruction.md` §2.4.5), open charter rows `C-2, C-4, C-5, C-6`, and the physics-half pipeline defects (`CONF-10` single-anchor physics, `CONF-11` IC reduction, `10⁴–10⁶×` IC-to-physics gradient imbalance, unreachable production L-BFGS stage) are routed to v2.6 (`69-HANDOFF.md`); `GAP-56-02` remains DEFERRED.

**Close type:** clean close (`tech_debt` with zero blockers). The milestone audit (`milestones/v2.5-MILESTONE-AUDIT.md`) verified 13/13 requirements Complete, 5/5 phases passed, and 5/5 cross-phase integration checks PASS. Known verification items: 4 carried-forward open-artifact items from earlier milestones (2 Phase-39 debug sessions and 2 pending todos) recorded in `STATE.md` Deferred Items.

**Archive:** [roadmap](milestones/v2.5-ROADMAP.md), [requirements](milestones/v2.5-REQUIREMENTS.md), [audit](milestones/v2.5-MILESTONE-AUDIT.md), [summary](reports/MILESTONE_SUMMARY-v2.5.md). Learnings: `65-`, `66-`, `67-`, `68-`, `69-LEARNINGS.md`. Phase folders 65–69 stay in `.planning/phases/` alongside 53–60 and 64 because `pinn/verification/` and `tests/phase65..69` hardcode their paths.

---

## v2.4 Stage-0 Feasibility Checkpoint (Closed on its pre-registered exit at Gate G2: 2026-10-26)

**Phases completed:** 3 of 6 phases (59, 60, 64), 40 plans, 103 tasks; Phases 61–63 skipped at Gate G2 (no rescue), not failed; 234 commits, 2026-10-09 → 2026-10-26

**Verdict:** `RETHINK-REPRESENTATION`, the frozen rule's output for "G2 fired and the sweep rescued nothing", stated unamended. **Owner decision:** `change-course` (checkpoint ①, 2026-10-26); all fourteen charter rows C-1..C-14 left open. Requirements: 12/24 Complete; the twelve requirements of Phases 61–63 stay Pending (their label is charter row C-14, open). No graded run, no held-out evaluation, no test-split file opened; all computation on this Mac.

**Key accomplishments:**

- Froze the feasibility scorecard, its comparison points and the census before any rung ran (Phase 59). The FEAS-01 scorer, one allowlisted reader that refuses held-out files, the Stage-0 panels and a read-only survey of all 12,023 training-split records. The two-Kepler formula reaches Tier 1 on 1 of 1,812 training and 0 of 227 validation systems. Gate G1 recorded "proceed": generation 7's physics term supplied 7.19e-07 of the Adam-preconditioned update.
- Built the INST-05 learnability harness on the trainer's own losses, with the L-BFGS polish, a CPU float64 cross-check and governed pause/resume, and sealed its run protocol (SHA-pinned to 33 modules and 5 inputs) before any real arm (Phase 60).
- Ran Rung 1 on systems 1632, 851 and 4658 and the four-setting `first_omega_0` sweep (60, 120, 240, 480): every arm ended at Tier 0 (E 1.14–1.24, valid horizon 0.0) after 22.378 machine hours. Gate G2 fired with no rescue; Rung 2 and the hard-stage probes were recorded as skipped, and Phases 61–63 were skipped, not failed.
- Found, in Phase 60's independent verification, that every trained network learned only each body's average position: its output varies by about 0.3% of the real orbit's variation and its error equals that of the constant mean predictor.
- Wrote the owner-facing verdict (Phase 64) with every number a labelled, re-derivable manifest entry (365 entries) and a regenerated figure: the frozen label beside the time-constant evidence, Level 1 on the readiness ladder, the cost on this Mac, and eight unranked candidate fixes for `trainex-r5`; plus the one-page charter. VER-22 re-verified at 24/24/24.

**Known gaps:** CONF-10, CONF-11, INST-06, INST-07, SPEC-07, SPEC-08, SPEC-09, SPEC-10 (Phase 61), GATE-05, FEAS-05 (Phase 62), RUN-06, DIAG-08 (Phase 63): skipped at G2 (no rescue), not failed. GAP-59-08 and GAP-64-01 OPEN (owner-routed); GAP-56-02 still DEFERRED.

**Close type:** override closeout. The milestone audit (`milestones/v2.4-MILESTONE-AUDIT.md`) is `gaps_found` only for the twelve skipped-phase requirements (integration 4/4 checks PASS, 0 blockers, 6 warnings), and the owner chose to close over them (2026-10-26). Phase 60 reads `stale` only because its covered `REQUIREMENTS.md` received Phase 64's edits; its verification is `passed`. Known verification overrides: 18 open-artifact items carried forward from the v2.3 close and recorded in STATE.md Deferred Items rather than acknowledged in the archived files (owner decision, 2026-10-26); 0 previously acknowledged.

**Archive:** [roadmap](milestones/v2.4-ROADMAP.md), [requirements](milestones/v2.4-REQUIREMENTS.md), [audit](milestones/v2.4-MILESTONE-AUDIT.md), [gaps](milestones/v2.4-GAPS.md). Learnings: `59-`, `60-`, `64-LEARNINGS.md`. Phase folders 59, 60 and 64 stay in `.planning/phases/` because 18 code and test files hardcode their paths (owner decision, 2026-10-26).

---

## v2.3 Causal-Weight/SIREN-Scale Recipe Adjudication (Closed on the declared terminal state: 2026-10-04)

**Phases completed:** 6 phases (53–58), 30 plans, 73 tasks (Phase 58 was an adapted closeout with no plans); 172 commits, 2026-08-18 → 2026-10-03

**Owner verdict:** `rethink` (checkpoint ⑤, 2026-10-03). Requirements: 12/15 Complete; RUN-04 and RUN-05 closed incomplete; EVAL-02 not attempted, with the held-out evaluation preserved unspent.

**Key accomplishments:**

- Codified the four VER-20 items that needed no research (Phase 53): the locked PHYS-05 `λ_phys^max` values, a locked-vs-default marker convention for tables, the `L_data` mean reduction, and the worst-case-max held-out gate statistic (SPEC-02..05).
- Took the causal-weight/SIREN-scale recalibration through the governed channel (Phase 54): a non-recommending packet, the `trainex-r3` ERW round with Rule-19 verification of both returned reports, and an owner-delegated ruling, `A1 + B2 (residual-wide) + C1 + D3 + E1` (`54-RULING.md`).
- Landed INST-04, the architecture-only characterization probe, as tested tooling that reproduces the 2026-08-17 audit's six-row table (Phase 55).
- Wrote the ruling into `pinn_architecture.md` §3.2 as a SCOPE-38 contract amendment, with the `first_omega_0` and clip contracts recorded as NOT AMENDED. Built GATE-04, the fail-closed train-free gate, which blocks the pre-amendment recipe and passes the amended one with a governed `R_ref = 1.9749775821244170e+10` (Phase 56).
- Wired the amended recipe into the production trainer (4096 rows in 16 bins, frozen-`R_ref` normalization, one frozen invariant-B monitor, frozen L-BFGS segments) and re-ran Stage-0 (Phase 57). Generations 1–6 produced no graded result and were each handled by an owner ruling. On generation 7, graded seed 42 tripped invariant B at step 951 (front stuck at 2 since step 450), which is the declared terminal state. Seeds 41/43 were not launched and the evaluation was not spent.
- Rendered the DIAG-06 verdict on a packet whose frozen-monitor replay showed the stall was not a near miss (bins 0–2 sum 1.189 against the 0.693 bar). Re-verified VER-21 at 15/15, and routed the next milestone to ERW round `trainex-r4` (Phase 58).

**Known gaps:** RUN-04 (the causal front did not keep advancing), RUN-05 (no three-seed band), EVAL-02 (not attempted; evaluation preserved). GAP-56-02 DEFERRED to the milestone after `trainex-r4`.

**Close type:** override closeout. Phases 55 and 56 were flagged stale only because closeout files were added after their verification. Phase 58 has no VERIFICATION.md because it used an adapted closeout. There is no milestone audit file (v2.2 precedent). Known verification overrides: 18 open-artifact items carried forward and recorded in STATE.md Deferred Items rather than acknowledged in the archived files (owner decision, 2026-10-04); 0 previously acknowledged.

**Archive:** [roadmap](milestones/v2.3-ROADMAP.md), [requirements](milestones/v2.3-REQUIREMENTS.md), [gaps](milestones/v2.3-GAPS.md). Phase folders 53–58 stay in `.planning/phases/` (owner decision, 2026-10-04).

---

## v2.2 Stage-0 Conformance Repair & Valid Re-Run (Closed incomplete: 2026-08-17)

**Phases:** 7 planned (46–52). Phases 46–49 are complete, Phase 50 closed incomplete, Phase 51 was not attempted, and Phase 52 was an adapted closeout. 38 plans, 34 executed. 211 commits, 2026-07-25 → 2026-08-17.

**Owner decision:** `stop-incomplete` at the Plan 50-08 checkpoint (2026-08-17).

**Requirements:** 20/24 Complete. RUN-01 and RUN-02 closed incomplete. RUN-03 and EVAL-01 were not attempted; the held-out evaluation was preserved unspent.

**Key accomplishments:**

- **Settled the frame question (Phase 46).** The CONF-01 branch point fired `VERDICT_AMBIGUOUS` and was owner-settled under GAP-46-06. CONF-08 repaired the mass↔position permutation and the COM/boost gauge. INST-01 added per-trajectory `ε_H`/SCS validation metrics as a fail-closed receipt.
- **Completed the canonical frame and the `S_H` pipeline (Phase 47).** CONF-09 moved residency to `pre.r_gauge`/`pre.v_gauge` and re-ratified the validation frame. CONF-02 built `S_H = median_train(K0 + Uabs0)`. CONF-03 wired `ε_H = 1e-4 · S_H` and removed the additive fallback floor.
- **Made the executed loss math match the specs (Phase 48).** This covered `R̄ = (1/3)Σ‖f_i‖²`, the causal-exponent clip, `λ_E^max → 0`, and the `L_data` reduction (GAP-45-01 owner checkpoint). It also added per-term gradient statistics (CONF-04..07, INST-02, TEST-01/02).
- **Built the conformance gate (Phase 49).** The PHYS-05 table is asserted at run start and at stage boundaries. The phase added a placeholder census, runtime invariants A and B with invariant-B `N = 500` ratified 2026-08-05, and a divergence register (GATE-01..03, INST-03).
- **Re-ran Stage-0 under the corrected recipe (Phase 50).** Generation 3, seed 41, halted at invariant B at step 501, with `front_idx = 0` throughout. A same-day residual-frame conformance audit traced the halt to the SIREN `ω₀ = 30` second-derivative scale against an unnormalized `η_c = 1` causal-weight calibration. That is a property of the locked architecture at initialization, and v2.2 could not fix it (SCOPE-30).
- **Discharged DIAG-05, VER-19, and VER-20 in adapted form (Phase 52).** This superseded the Phase 44 diagnosis rankings and routed five spec-amendment items. The substantive one, the causal-weight/SIREN-scale calibration, went to v2.3.

**Known gaps:** RUN-01 and RUN-02 (no completed conformant band). RUN-03 and EVAL-01 (not attempted; the evaluation was preserved for v2.3).

**Archive:** [roadmap](milestones/v2.2-ROADMAP.md), [requirements](milestones/v2.2-REQUIREMENTS.md), [gaps](milestones/v2.2-GAPS.md), [phase archive](milestones/v2.2-phases/). The phase folders moved at the v2.3 start (`12e16d7b`). There is no `v2.2` tag. This entry was backfilled on 2026-10-04, because the v2.2 close recorded no MILESTONES.md entry.

---

## v2.1 Physics-Gate Investigation & trainex-r2 Research Package (Shipped: 2026-07-24)

**Phases completed:** 2 phases (44–45), 9 plans

**Key accomplishments:**

- Characterized the physics-gate FAIL from retained v2.0 evidence — the per-trajectory ε_H distribution over all 1,500 held-out trajectories (from the preserved `metrics.json`; the exhausted-budget evaluator was NOT re-run), the five-term loss decomposition with the ~3.7e9 warmup-spike attribution, and the three-seed 41/42/43 band — all re-derivably (pinned scripts + SHA-256 `manifest.json`)
- Delivered `44-DIAGNOSIS.md`: ≥4 hypothesis-ranked candidate causes, each with cited supporting AND contradicting evidence, explicitly abstaining from remedy selection (SCOPE-26)
- Assembled and delivered the trainex-r2 ERW package under `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/` — commit-pinned document snapshots, 5 neutrally framed research questions + an evaluation-policy question, a claims register ([FACT] vs [HYP]), and a delivery note — audited PASS (`45-AUDIT.md`, ten checks)
- A bounded Stage-0 conformance audit established that the v2.0 pilot diverged from the locked specs in five verified respects (C-01..C-08), so the physics-gate failure is not evidence about the design — this qualified `44-DIAGNOSIS.md` via `44-ERRATUM.md` (re-derivation obligation GAP-44-02)
- All five gap questions routed to the owner and resolved the same day (4 RESOLVED-WITH-INSTRUCTION, 1 DEFERRED); the returned report accepted Route B / open-book with repository-derived claims verified 6/6 per ERW Rule 19
- SCOPE-22..26 held throughout (no held-out evaluation, no new training, no spec edits, no PLAT-01..07, no remedy selection); owner set the next milestone conformance-first with six inherited obligations (`milestones/v2.1-GAPS.md §Obligations`)

## v2.0 CTL-PINN Training Viability Slice (Shipped: 2026-07-23)

**Phases completed:** 7 phases, 60 plans, 190 tasks

**Key accomplishments:**

- Six stdlib-only `tests/phase37/` modules encoding the executable ENV-01..04 / CTX-01..14 contracts before any host mutation, package install, or empirical MPS run
- Reviewed committed environment pair + fail-closed normal setup + re-derivable M5 Pro provenance, all gated by an explicit (non-circular) first-lock seed
- The narrow two-profile precision/device seam and the one §10.3 componentwise-AD worker both D1-p arms execute unchanged — no global default, no fallback, no D1-p pick
- One stdlib-only command that runs both D1-p profiles through isolated, sanitized subprocesses and writes append-only, provenance-bound, verdict-free evidence — no real MPS run yet (that is Plan 37-05)
- The one authorized M5 Pro dual-arm run is retained and validated; the owner explicitly DEFERRED D1-p (retracting an initial fp32-MPS pick); Phase 38 remains blocked
- Wave-1 substrate landed: one cited constants home and a frozen fail-closed ArchitectureSpec for every later Phase 38 module
- Wave-2 model core landed: a spec-faithful SQR-SkipResNet-SIREN backbone instantiated from an ArchitectureSpec, with a hard mass-weighted COM projection head wired so projected positions are the model's only public output.
- PHYS-02 componentwise-AD residual on the canonical `u = t/T` leaf (jacrev+vmap, no manual chain factor, gradcheck-clean under fp64-CPU and live under fp32-MPS) plus a read-only, sha256-provenanced, completeness-gated single-Brutus-trajectory loader with traversal-proof path resolution.
- 1. [Rule 2 - Missing Critical] Protect the read-only dataset boundary from probe output
- Nine-file dataset-free Nyquist Wave-0 unittest contract for DATA-01..06: a deterministic read-only TinyCorpus fixture, a self-testing mechanical boundary audit (green today), and deferred executable expectations that Plans 02-06 implement against — no production `pinn/data` code introduced.
- Sole float64 corpus parser + version seam, pure CTL preprocessing/invariants/IC13/normalization pipeline, the sole GAP-39-08 base-Set-1a Stage-0/1 classifier, and the seven-clause Step-1A admission gate with GAP-39-04/05 boundaries — all frozen Wave-0 tests green, zero real-corpus scanning.
- The production two-pass `AdmittedSetAdapter` integrates the Wave-1 pure contracts into one deterministic, read-only, fp32-resident admitted set with observable admission/provenance/memory state — fail-closed root resolution (git-common-dir default, typed missing/partial-corpus guards), the seven-clause admission gate, the sole base-Set-1a classifier with a hard zero-gold-numeric invariant, the GAP-39-07 deduplicated `resident_tensor_bytes` numerator plus a `mem_ballpark` lower-bound cross-check, and the sole-reader/sole-classifier containment gate — closing DATA-01/02/03.
- A persisted-label `StageIndex` and complete-signature Hamilton allocator now keep every physical base/gold group indivisible, expose a train-only batching seam, and atomically write a byte-stable, typed `splits.json`.
- The DATA-04 train-restricted `StageIndex` now builds deterministic replay/lookahead batches containing aligned observed snapshots and an independent, exactly balanced continuous physics-collocation set.
- DATA-06 now has a portable persisted-label population report and atomic CLI whose sole fatal operand is the admitted/full Stage-0 count, with canonical split bytes retained and hashed before either exit 0 or exit 2.
- Phase 39 closes train-ready: the read-only 6.3 GB Thrust-A scan reports `stage0_full_split_count=2265` (>= 240) with `gold_numeric_stage_count=0`, retained byte-identical evidence, and an exact-reader/source audit — after a green dataset-free + full-repository regression.
- Refreshed real-corpus evidence and the Phase-39 validation ledger for the 08/09 behavior changes, then closed the 39-10-03 authority checkpoint under the owner's Option-A resolution (the deployed gsd-core UAT hard-gate), unblocking the verification closeout.
- 1. [Rule 1 - Bug] Python bool capitalization in `evidence_byte_identity`
- PHYS-05 warmup/freeze/rewarm schedule + §4.4 Adam-only median grad clipper with single-mechanism non-finite flag -- the two pure numeric-machinery modules RunController (40-05) composes per Adam step.
- RunController.run_stage(k) — the real Adam→L-BFGS two-phase closure loop with per-epoch resampled batches, Adam-only median gradient clipping, the CTX-46 50-epoch plateau handoff (or budget-exhaustion fallback), a frozen-λ fixed-batch L-BFGS phase with chunked-accumulation gradients, and a real held-out validation pass wiring StageExitMachine's ADVANCE criteria 2–4.
- CurriculumController closes TRAIN-01 -- ADVANCE/RECOVER/HALT stage-progression dispatch over RunController.run_stage(k), a T-40-09-guarded forced-disposition injection seam, a cold-start RECOVER backstop against an empty CheckpointStore, CTX-38/45 run-start provisional-threshold logging, and the full pinn/training package barrel -- closing Phase 40 at 142/142 dataset-free tests.
- RECOVER restores rolled-back RunController state; zero-L-BFGS-headroom boundary polls stage-exit so ADVANCE is reachable when the gate holds
- Dtype-honest grad-clip resume, config-governed energy floor, reserved percentile-10 seam, and stagnation-HALT coverage
- Per-stage RunController swap via caller-supplied stage_factory so ADVANCE trains stage k+1 against that stage's lambda^max (PHYS-05), not stage 0's
- CTRL-01 library floor: keyed YAML ↔ frozen TrainingConfig with recursive fail-loud keys, atomic frozen copy, shared atomic_io, and ⚖ provisional cadence/guard/RNG-format seams
- Production CheckpointStore delivers atomic weights_only-clean writes, dual-trigger rolling/best/anchor retention, fallback scan, exact-path load_checkpoint, and an idempotent curriculum.jsonl promotion ledger behind the preserved CTX-43 Protocol
- Injectable StepGuards (Tier-1+2, per-family RECOVER/HALT, disk-floor-safe failure/) and four-stream RNG exact-continuation + strict-CPU RuntimeSpec return with statistical-equivalence honesty — CTRL-07/08 modules ready for 41-04/41-05 wiring
- RunController/CurriculumController additive mid-stage checkpoint + guard wiring — live Adam/RNG/global-step state, single CTX-53 composer, phase-specific guard placement, disposition ledger, and CTRL-06 Adam-reset init anchors — composition seam ready for 41-05 pinn.train
- Multi-module field-classified resume refuse + exact-anchor hold-stage routing + minimal runnable `python -m pinn.train` composition root delivering CTRL-01/05/08 end-to-end on the dataset-free Stage-0 floor
- 42-operator-runbook-surface-monitoring (Wave 1)
- A macOS-safe unattended wrapper, loadable Stage-0 configuration, and five-entry-point operator runbook with focused contract coverage.
- Graceful signal interruption and honest run-directory lifecycle wiring for the training composition root
- Realize E2/E4/must-NOT edge tests against the fully wired system (42-08)
- `python -m pinn.verify` — an ordered five-rung pre-flight that orchestrates the four existing probes as in-process library calls, names its first failure, and writes an atomic `runs/.verify/latest-marker.json` fingerprinted by device, dtype, Torch, Python and Git head so only a fresh green marker from the same code can authorize a long run.
- One-time `pinn.evaluate` CLI that reconstructs the persisted held-out test split from a checkpoint's frozen run provenance and renders the authoritative post-v1.3 binary gate (worst-case Hamiltonian drift, matched-Plummer `eps_inv=1e-10`) with a single-evaluation receipt.
- `pinn.train._check_duration_gate` — wired into the launch preflight before any run-directory/checkpoint/optimizer construction, forecasting from the persisted 43-03 Stage-0 timing calibration times the launch's own declared budget, and refusing both an absent calibration (unconditional on duration) and a >1800s forecast lacking a fresh green 43-01 verify marker.
- Completed-run summaries now project persisted validation, curriculum, held-out metrics, and prior-run evidence into one honest payload, with evaluation refreshing only an existing finished run after its one-time receipt is committed.
- Real ordinary Stage-0 smoke over the actual admitted corpus (32 trajectories, 300 gap-free steps, checkpoints 100/158/200/300, one SIGTERM interrupt + resume to finished, s_per_step≈0.1157) with B-5, R-1, and D4-a all owner-ratified — B-5 and R-1 via explicit instruction/delegation earlier in the plan, D4-a (wall_clock_ceiling_s=120) via the owner's explicit selection that resolved this continuation's blocking checkpoint.
- Three real admitted-data Stage-0 seeds produced a traceable calibration band, and the owner ratified the exact supported guard/recovery configuration: `100000000000.0`, `0.05`, `0.7`, and `0`.
- The sole held-out evaluation produced an unequivocal FAIL, and the owner rendered `adjust`: keep the proven mechanical Stage-0 slice, block full-platform expansion, and investigate the physics-gate failure and non-convergent behavior without claiming a known remedy.
- The long-run gate now binds calibration and verification authority to the effective strict-CPU runtime, and only a complete current-schema ordered marker can grant authorization.
- Each run now owns exactly one canonical evaluation path and durably consumes its held-out budget before admitted-corpus access, preventing redirected replay, crash erasure, and concurrent double evaluation.
- The owner verdict backstop now parses typed YAML and verifies its gate, metrics, and provenance digests against the cited receipt, closing the forged-go, quoted-YAML, and impossible-date bypasses.
- Legacy launch fixtures now satisfy the unchanged duration gate, the corpus-reader audit retains its prohibition without false-flagging diagnostic text writes, and all 1,036 repository tests authorize ACC-02/ACC-04 completion.

---

## v1.6 Resolving 03 Curriculum and Training Loop (Shipped: 2026-07-02)

**Phases completed:** 7 phases, 30 plans, 49 tasks

**Key accomplishments:**

- Read-only PKG-08 characterization of both curriculum-relevant reports plus a provisional PKG-07 claims register (CLM-01..CLM-19) carrying the D-17 no-in-milestone-verification boundary and the D=6.694 vs D≈4.6416 seed-conflict, with content-SHA + source-commit provenance seeded for byte-fidelity.
- Authored the PKG-05 document-list + consolidation plan (`30-CONSOLIDATION-PLAN.md`), locked the MULTI-COMPANION package form, classified the framework specs NEVER consolidated (D-04), assigned the standalone verified-facts reference to 30-03 Task 2 (F11), posed the three open inclusion calls, and FILLED the D-09 APPROVED record under the user's pre-authorized approve-as-proposed waiver — each decision cross-checked against the 30-RESEARCH Consolidation Map with zero conflicts. Assembly (30-03) is now unlocked.
- Authored the four upload companions for the doc-03 ERW package: 19 neutrally-framed research questions in issue-03 section order (three named decisions + the D conflict posed unsettled with locked/open delineation), the verbatim SCOPE-12 hard-constraints preamble, a non-binding per-finding resolution-doc skeleton, and the uploaded PKG-07 claims register — with the claims seed extended after the full issue-03 read.
- Delivered the complete repo-blind doc-03 ERW package (single-entry-point master + paste-ready prompt + round-root delivery note over the existing companions/snapshots), passed the F12 self-containment cross-check both directions, and opened the external resolution-doc gate via gsd-tools handlers with STATE progress counters verified unchanged.
- Gate verdict READY-WITH-CAVEATS on the landed issue-03 resolution doc — all 18 selected findings covered, zero v1.5-verified-fact contradictions, zero SCOPE-12 violations; 12 non-blocking caveats routed to Phase 32 EVID-15 / Phases 33–35 / FUT.
- Issue-03 adjudication machinery with first-write baselines, fixed verdict/status protocol, packet template, seeded 18-row ledger, and verification inventory
- Final Phase 32 evidence-framework closeout with packet coverage, ledger coverage, protected-path guards, owner-decision discipline, and baseline preservation verified
- Multi-Stage Data Stratification by Difficulty section
- Stage Transition Criteria section
- 1. Combined dirty-doc SHA-256 mismatch (Wave 1-3 STATE.md tracking-write artifact)
- Captured the Phase 34 baseline, stood up the evidence workspace, authored the four packet-before-edit evidence packets (B-07, B-08, M16, ALM), and synchronized their Phase 32 ledger links so the downstream spec-edit plans can proceed without inventing evidence or process schema.
- Transcribed the LOOP-04 merged adaptive median-based gradient-clipping contract with a single canonical home per half: mechanism in `pinn_architecture.md` §4.4 and per-stage C-schedule `7-10 / 5 / 3` in `ctl_instruction.md`, linked by bidirectional `AC-LOOP-04` anchors.
- Landed the LOOP-01/02/03 provisional batch-construction contract, the LOOP-06 realized-as-deferred collocation-scaling body, the LOOP-07/08 provisional training-side metric roles, and the opaque total-loss ordering skeleton in `ctl_instruction.md`, and opened GAP-34-01 for the source-silent batch edge cases.
- Reconciled the pinn_architecture.md batch-construction inconsistency with ctl_instruction.md as canonical and transcribed the LOOP-05 optional/deferred ALM contract, leaving the default training loop ALM-free and the LOOP-04 cross-file invariants intact.
- Durable Phase 34 goal-backward verification report and five LOOP-related Phase-32 ledger rows closed VERIFIED, with Phase-34 completion explicitly gated on OPEN GAP-34-01.
- Transcribed the owner-ratified Option A batch edge-case policy into the `ctl_instruction.md` Mini-Batch Construction LOOP-01 contract (provisional) and cleared the Phase-34 closure gate recorded in `34-VERIFICATION.md`, with the LOOP-04 cross-file and locked-convention guards re-verified intact.
- 1. [Rule 3 - Blocking verification anchor] Restored the plan's stable multi-component loss anchor
- Phase 35 loss-contract verification with dual-register D-04 closure and five VERIFIED issue-ledger rows.
- Build the Phase 36 acceptance-check spine (contract manifest + probe suite)
- Run AC suite and record evidence
- Drive the Phase 32 issue ledger to terminal state by verifying D-05/D-06 transcription and promoting those two PENDING rows.
- Write the v1.6 milestone-closure handoff: classify every ledger finding, reconcile all four framework-spec SI entries, and route implementation-shaped findings to FUT-01/FUT-04.
- Phase 36 verification + reconciliation + final batch re-verify.

---

## v1.5 Resolving 02 Data Pipeline and Validation (Shipped: 2026-06-17)

**Delivered:** Evidence-verified data-pipeline and validation-metric design contracts for `ctl_instruction.md` / `pinn_architecture.md`, with every issue-02 finding adjudicated against the on-disk dataset and a user-produced resolution doc, plus a complete FUT-01 implementation handoff.

**Phases completed:** 8 phases, 27 plans

**Key accomplishments:**

- Assembled the framed research package (annotated document list, "claimed, unverified" dataset figures, read-only DQA characterization) that opened the external resolution-doc gate.
- Verified every empirical dataset claim (ID gaps, blacklist, gold-counterpart gap, footer variance, mass drift, snapshot/`dt_out` distributions) against `simulation_data/` with re-derivable probes; closed DATA-05 via a 70-file base-hierarchical rerun.
- Stood up the evidence-packet / EVID-10 root-cause adjudication machinery and the re-verification issue ledger; adjudicated the SCS-threshold, `D=6.694`, and M11/M12 conflicts at root cause.
- Locked the DataLoader ingestion/selection contracts (B-06 gate, B-11 ID-resolution, M11 blacklist, M13 gold-counterpart, D7 footer heterogeneity, D-03 HDF5 format) and the sampling/precision/global-scale contracts (M12 points, float64/Decimal, `dt_out`/stage-query, `compute_globals`).
- Defined canonical SCS/SASD/IPR/PSC validation-metric contracts threshold-aligned to the locked gate, with training-loop usage deferred to doc-03.
- Executed the 13-check acceptance suite (G1–G8 milestone-closure gate PASS), closed the 19-row ledger (18 VERIFIED + 1 DEFERRED), reconciled 3 SI dispositions, and produced the two-artifact FUT-01 handoff (gold: 117 validatable + 67 permanent-absent).

**Stats:**

- 36/36 requirements satisfied; 8/8 phases verified; 10/10 STOP-protocol gaps RESOLVED-WITH-INSTRUCTION, 0 open.
- G1–G8 milestone-closure gate PASS (2026-06-17); milestone audit verdict `tech_debt` with 3 non-blocking items closed at archive.
- `milestone/v1.5` merged to master `--no-ff` as `fe9b3c92` (2026-06-17); branch tip `b8b39a4` preserved at tag `v1.5-pre-merge-backup`.

**What's next:** v1.6 (Issue-03 "Resolving CTL") starts fresh requirements; FUT-01 consumes the dataset-finalization handoff (FO-1: promote 117 validated gold + 184→67 cascade; then FO-2: PSC/SCR first-run sanity, SASD/IPR/PSC constant recalibration, AC-VAL-04 numeric run).

---

## v1.4 Resolving 01 Architecture and Physics Foundations (Shipped: 2026-06-09)

**Delivered:** Evidence-backed, physically coherent framework specifications with executable acceptance checks and a complete downstream implementation handoff.

**Phases completed:** 8 phases, 26 plans, 65 tasks

**Key accomplishments:**

- Established the evidence-packet, EVID-05 adjudication, STOP-gap, and re-verification protocols used across all eight phases.
- Locked coherent 14D input, 13-component IC, raw 9D position-output, COM projection, frame, gauge, and sampling-coordinate contracts.
- Defined physically consistent scaling, componentwise AD, matched softening, conservation regularizers, and loss-balancing semantics.
- Settled SIREN, LayerNorm, inertia, energy, mass, and normalization contracts while preserving explicit FUT-01 implementation divergences.
- Executed all five numerical acceptance probes and closed 32/32 requirements, 8/8 phase verifications, and all 25 STOP-protocol gaps.
- Completed presentation-preserving cleanup and archived the full phase history, including the FUT-05 author-comment handoff.

**Stats:**

- 258 files changed across the milestone branch range
- 40,357 additions and 5,177 deletions
- 8 phases, 26 plans, 65 tasks
- 22 days from branch baseline to ship

**Git range:** `dffc7a5` → `833930f`

**What's next:** Define the next milestone and fresh requirements; production PINN alignment remains a documented candidate rather than an assumed scope.

---

## v1.0 Codebase Cleanup (Shipped: 2026-03-20)

**Phases completed:** 4 phases, 10 plans, 9 tasks

**Key accomplishments:**

- (none recorded)

## v1.1 LaTeX Modularization Verification (Shipped: 2026-03-22)

**Phases completed:** 4 phases (5–8)

**Key accomplishments:**

- Verified content completeness across all 5 modular LaTeX structures (automated diff)
- Confirmed preamble parity (packages, macros, commands) between original and modular preambles
- Verified structure fidelity (section hierarchy, labels, references, citations, floats)
- Confirmed all 5 modular structures compile cleanly (0 errors, 0 new warnings)

## v1.2 PINN Implementation Readiness (Shipped: 2026-05-08)

**Phases completed:** 1 phase (9), 3 plans

**Key accomplishments:**

- Consolidated 7 scattered issue reports into 3 thematic documents (01-architecture, 02-data-pipeline, 03-curriculum)
- No unique findings lost; each thematic document has distinct, non-overlapping coverage
- Produced MIGRATION.md and README.md for migration tracking; VERIFICATION-REPORT.md (PASS) and VALIDATION.md (all checks PASS)

## v1.3 Markdown Conversion Verification & Correction (Shipped: 2026-05-08)

**Phases completed:** 7 phases (10–15, 15.1), 21 plans

**Key accomplishments:**

- Verified all 6 LaTeX→markdown conversions with one-to-one injection fidelity
- Corrected 7 critical, 19 major, and 17 minor conversion errors in Phase 15.1
- Archived unselected markdown candidates to `_archive/` directories
- Produced verification reports documenting all discrepancies and fixes
- Preserved inter-document inconsistencies faithfully (deferred reconciliation to v2)
- Cleaned up stale debug sessions and quick-task artifacts from prior milestones
