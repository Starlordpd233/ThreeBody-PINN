# Phase 60: Single-System Learnability - Research

**Researched:** 2026-10-18
**Domain:** A diagnostic single-trajectory learnability harness for the CTL-PINN network (PyTorch 2.12.1, MPS float32), built from the trainer's own loss functions and scored by a frozen, pre-registered scorecard; long detached runs; owner-gated branching.
**Confidence:** MEDIUM-HIGH. Reuse points, hazards and frozen-rule behavior are HIGH (read in full or executed read-only this session). MPS L-BFGS behavior, per-step timing and several protocol choices are LOW and flagged in the Assumptions Log and Open Questions.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Learning-rate schedule**

- **D-01:** Physics arms use the ratified Adam schedule and do not change it. Initial rate `LR_k = 1e-3 × (0.7)^k`, cosine annealing to zero over that arm's step budget, Adam `β1 = 0.9`, `β2 = 0.999`, `ε = 1e-8`, and the PHYS-05 warmup. SCOPE-41 forbids a different schedule. Stage 0 uses `k = 0`. Stage 4b uses `k = 4`. Stage 6 uses `k = 6` (`1e-3 × 0.7^6 ≈ 1.18e-4`).
- **D-02:** The cosine's step count is the frozen 3-hour cap divided by that arm's timing-run seconds per step. The timing run is not part of the cosine.
- **D-03:** The one ×2 extension, if the frozen still-improving test grants it, is a second cosine of that same length. It starts again at that stage's initial rate, keeps Adam's state, and does not repeat the physics-weight ramp.
- **D-04:** Every data-only arm uses the Stage-0 cosine (`k = 0`), not the Phase 38 constant `1e-3`. The frozen still-improving test is unchanged. Its 75%–100% window is therefore the low-rate tail of the cosine, and the readout says so.
- **D-05:** Probe Rung-2b arms use that stage's `LR_k`, not Stage 0's rate. The readout names the confound: the 0.7 factor assumes weights carried forward from the previous stage, and these probes start from scratch.

**No self-halt**

- **D-06:** A physics arm never halts on invariant B or any other causal-front rule. On the budget-rule readings (both ends, and no gap larger than 5% of the step budget), it logs the frozen monitor's per-bin causal weights and front. It does not run a live 256-identity monitor every step. Phase 61 builds the observe-only guard. This phase does not.

**R_ref and GATE-04**

- **D-07:** If the owner continues at checkpoint ④, re-measure `R_ref` and re-run GATE-04 at the approved `first_omega_0` before any physics arm. Neither step trains. GATE-04 is the ratified complete-pass rule in `57-RULING.md` (GAP-56-01): non-anchor spread at least 2:1, then the fixed residual reduction. A fail stops for the owner. The checkpoint question says that continue includes this step.
- **D-08:** Probe physics arms reuse the committed Stage-0 `R_ref`. They do not re-measure it. `R_ref` is ratified for the whole of Stage 0. The probes are Stage 4b and Stage 6, and none of the invalidation triggers in `pinn_architecture.md` change for them: `T = 10`, and the six measurement cases use no real system. The run record says the value is the Stage-0 reference applied unchanged.

**Phase 59 verifier after the scorer fix**

- **D-09:** `verify_phase59_evidence.py` accepts exactly one successor SHA-256 for `pinn/verification/feasibility_scorer.py`, named in a committed Phase 60 record. Every other producer hash is still checked against the Phase 59 result files. Phase 59 evidence is not re-run, and Phase 59 is not reduced to "verifies only at `45f65228`".

**Weights in git**

- **D-10:** Both scored states of every real arm are committed in plain git, not Git LFS. That is about 2.8 MiB per state: about 45 MiB on the stop path (8 arms, counting one confirmation) and about 106 MiB on the continue path (19 arms). Resume checkpoints and timing-run weights stay out of git. Re-deriving a result re-scores the committed weights.

**Checkpoint ④ authorization**

- **D-11:** A continue-path arm is legal only when a committed ruling file quotes the owner's message and names the approved `first_omega_0`. The file is written only from the owner's words. Every continue-path arm record cites it. A physics arm refuses any other value.

### Claude's Discretion

- The data term uses every point of the assigned record on each Adam step (1,001 on a gold record with `T = 10` and step 0.01). The polish uses that same set.
- The timing run is a separate run of at least 50 steps of the exact arm configuration, immediately before the arm. Its weights are discarded. The arm then starts from the seed-42 initialization, and its cosine covers only the arm's budgeted steps.
- Launch and resume use the generation-7 launcher's safeguards. A handler saves a checkpoint when the run is terminated or its terminal closes. Resume uses the trainer's L-BFGS segment state and refuses a resume that lacks it (`pinn/training/controllers.py`, the amended-checkpoint check near line 846 and `_start_lbfgs_segment` near line 2213). Line 262 is the record-key parser, not this check.
- The footprint preflight is unreliable on this macOS. Before a long arm, ask the owner to close browsers. The arm needs 6 GiB free.
- Module layout, the shape of the INST-05 tests, the plan split, and the order of the three Rung-1 arms are the planner's.

### Deferred Ideas (OUT OF SCOPE)

- The observe-only invariant-B guard and plateau detector are INST-07 in Phase 61. This phase only logs the frozen monitor on the budget-rule readings.
- Closing the stale `trainex-r1` handoff todo is housekeeping outside Phase 60. The r1a and r1b results are already committed, and rounds r2–r4 followed. The todo still says R1b has not returned.
- Reviewed todos (not folded): the D-06 static-epsilon sensitivity check (Phase 60 sets neither softening; leave it for whichever work next sets stage labels or gates) and the trainex-r1 research handoff (finished; close the stale todo outside this phase).

**Locked requirements (SPEC.md) that bound everything below:** 8 requirements in `60-SPEC.md`; out of scope there: editing the frozen scorecard, editing `pinn_architecture.md` or the other framework specs, conformance/telemetry/observe-only modes (Phase 61), Rung 3 and the 16-system family (Phase 62), the corrected control (Phase 63), the verdict and charter (Phase 64), a second seed, a second confirmation or a silent restart, graded runs / held-out evaluation / test-split files, curriculum training beyond Stage 0.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| INST-05 | The learnability harness under `pinn/verification/`: real normalized IC13; the trainer's own loss and residual functions; scorer at a fixed cadence; budget cap; Adam then full-batch L-BFGS polish with both states scored; diagnostic overrides for the G2 sweep's data-only arms only; run records marked diagnostic; test-split refusal. Tests (a)-(e): trainer functions by mutation, test-split refusal, graded-run/evaluator refusal incl. an override record, a short run through the polish with both states scored, override refused on a physics arm. | Findings H (function-by-function loss mapping), E (scorer), I (launch/resume), J (refusal paths), G (record reading); Pattern 1 (compose catalog functions + cross-check against a real RunController); Pitfall 1 (ArchitectureSpec locks omega); Validation Architecture rows INST-05(a)-(e). |
| FEAS-03 | Rung 1 on the three panel systems at the locked settings with the polish and the frozen budget rule; Gate G2 evaluated; the data-only sweep and confirmation if G2 fires; checkpoint ④ hold on a rescue. | Findings C (frozen rule signatures and cadence), G (gold records, 1,001 points), the sweep-pair rule (verified against the SPEC's four cases), Open Question OQ-5 (failed confirmation), Pattern 3 (budget driver), Pattern 7 (G2 pure rules, `OwnerRouted` propagation). |
| FEAS-04 | Rung 2 arms (a) physics + IC only and (b) full ratified loss on the same three systems, scored on gold; skipped with one of two exact reasons when the ladder stops at G2. | Finding H (2a uses a zero data tensor because `LossWeights` forces `lambda_data == 1.0`), Finding D (R_ref), Pattern 1 (microbatched physics step, frozen monitor), Pattern 7 (skip writer), Amendment finding A. |
| FEAS-09 | Two hard-stage probes (standard/base/2279, standard/base/3418): a Rung-1 arm and a Rung-2b arm each; run only if the ladder continues past G2; never counted; formula field "not applicable: no hierarchical split". | Finding G (probe records verified), Open Questions OQ-7 (S_H for the probe energy term), OQ-8 (probe normalizer), Finding D (R_ref in force), Pattern 7. |

**SPEC requirement to research mapping:** R1 amendment -> Finding A; R2 harness -> Findings B, H, I, J, Pattern 1-2; R3 scorer fix -> Finding E; R4 run protocol -> Findings C, I, Open Questions OQ-9/OQ-10; R5 Rung 1/G2 -> Findings C, G; R6 sweep -> Pattern 7, OQ-5; R7 Rung 2/probes/skips -> Findings D, H, Pattern 7; R8 records/resume/closeout -> Findings G, I, L.
</phase_requirements>

## Summary

Almost everything Phase 60 needs already exists in the repository and in the installed environment, so the phase needs no new packages. The harness should be a thin, separate loop that composes the trainer's own functions (`pinn.loss_catalog`, `pinn.physics_residual`, the 16-bin helpers in `pinn.training.controllers`, `ScheduledWeights`, `OptConfig`, `GradClipper`) and is proven against a real `RunController` on a stub source, exactly the pattern Phase 59's JX-1 driver used. Scoring, the budget rule, the polish stop, the G2 gate and the counting rule are frozen functions in `pinn/verification/feasibility_scorecard.py` and must be called, never re-implemented. Corpus access must go through `split_allowlist` plus `production_reference.load_reference`. All ten assigned records (hierarchical 1632, 851, 4658 in base and gold; standard 2279 and 3418 in base and gold) exist, are train-split, are admitted by the production gate, and carry bit-identical raw IC13 between base and gold siblings.

Research surfaced hazards that the SPEC and CONTEXT do not mention and that change the plan. (1) `ArchitectureSpec` raises on any `first_omega_0` other than 30, and `gate04_train_free` builds its networks through it, so both the G2 sweep and the D-07 re-measure need a new seam. (2) `network_trajectory` has three float64 widening sites, not one. (3) D-09 as written is incomplete: Phase 59's `baselines --check` re-derivation byte-compares output that embeds the scorer digest, and the verifier is itself hashed in `evidence/manifest.json`. (4) A second `CosineAnnealingLR` on the same optimizer without resetting the learning rate stays at zero forever, and continuing the first one climbs back up; D-03 needs an explicit reset. (5) The git ignore rules block `*.pt`, `*.npz`, `*.npy`, and the staged-path policy blocks any path under `runs/`, `tmp/`, `outputs/`; D-10's weights need a non-ignored extension under the phase evidence directory. (6) Gold records carry 1,002 snapshots (t reaches 10.01); training and scoring must window to t <= 10 (1,001 points). (7) The network has 795,657 parameters (3.04 MiB per float32 state), so D-10's sizes are about 8 percent low. (8) `tests.phase38.test_prohibitions` already has two unrelated failures at HEAD (stale spec byte checks); only its four other tests are a valid gate.

Several semantic choices are silent in every source and are listed under Open Questions with options and a recommendation, not decided here: gradient clipping in harness arms, what "improvement" means for the polish stop, what happens when a G2 confirmation run fails, the divergence rule, the energy-term scale `S_H` for the probes, and which `R_ref` the probe arms use on a continue path. Under the v2.4 delegation rule (ROADMAP "Delegation and gaps") each is recorded in `60-GAPS.md` and `.planning/milestones/v2.4-GAPS.md` with the STOP-protocol fields and may be resolved under the delegation unless it would move a locked value, spend the evaluation or pre-empt the verdict; OQ-5 is the one that could pre-empt the verdict and should default to an owner stop.

**Primary recommendation:** Lead with a thin tracer slice (one data-only arm end to end on a fixture: allowlisted record -> real network -> cosine Adam -> polish -> both states scored -> exclusive-create record -> refused by the evaluator), run the three small autonomous fixes (amendment text, scorer MPS fix with successor hash, harness omega seam) in parallel with it, then build physics arms, run control and the G2 rules, commit the run protocol, and only then launch the long Rung-1 arms as non-autonomous detached plans with owner memory prompts.

## Project Constraints (from CLAUDE.md)

Extracted from `./CLAUDE.md`, `./.claude/rules/*.md`, `~/.claude-max/CLAUDE.md`, `~/.claude/CLAUDE.md` and the v2.4 roadmap. Treat as locked.

- **Worktree and branch:** work only in `<home>/Desktop/3_body_problem/.worktrees/trainex` on `milestone/v2.4`; the corpus is read from the main checkout through the allowlist, never copied. Surface `git status --short --branch` before committing.
- **Commits:** agents use `scripts/agent-commit`, never raw `git commit`, with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS` set; stage explicit paths only; subject `<type>(<scope>): <lowercase imperative>` with types `spec evidence verify plan docs feat fix refactor test chore` and scopes such as `60`, `60-01`; a body is required for multi-file commits and anything under `.planning/`; add an `Agent-Assisted-By:` or `Co-Authored-By:` trailer; no push from `milestone/*`; no `--no-verify`. `scripts/agent-commit` rejects `-F`, so pass multiple `-m` paragraphs with the trailer last (memory note).
- **Staged-path policy** (`scripts/git_policy/validate_staged_paths.py:9-27`): blocked patterns include `runs/*`, `*/runs/*`, `tmp/*`, `*/tmp/*`, `outputs/*`, `*/outputs/*`, `scratch/*`, `wandb/*`, `__pycache__`, `.DS_Store`; blobs over 10 MiB are refused. Phase 60 evidence must live under `.planning/phases/60-single-system-learnability/` with no path segment named `runs`, `tmp`, `outputs` or `scratch`.
- **Source-silent semantic decisions (STOP protocol, v2.4 form):** record in `.planning/phases/60-single-system-learnability/60-GAPS.md` and `.planning/milestones/v2.4-GAPS.md` with every STOP field; may be resolved under the 2026-10-07/09 delegation unless the decision would move a locked value, spend the evaluation, or pre-empt the verdict; those go to the owner. Owner checkpoints: ③ any off-script result, ④ a G2 rescue.
- **Hard scope boundaries:** SCOPE-39 (Stage-0 only plus named exceptions), SCOPE-40 (no test-split file, no held-out evaluation), SCOPE-41 (every run diagnostic, ratified recipe unchanged), SCOPE-42 (pre-registration, no threshold re-set), SCOPE-43 (locked values move only by formal amendment), SCOPE-44 (one run at a time, detached, generation-7 safeguards).
- **Do not edit:** `pinn/verification/artifacts/feasibility_scorecard_v1.json`, `pinn/verification/feasibility_scorecard.py`, `59-SCORECARD.md`, `evidence/scorecard-freeze.json` (the four files `_frozen_rels` freezes), `59-CONTEXT.md`, `59-RESEARCH.md`, `pinn_architecture.md`, `ctl_instruction.md`, or any Phase 59 producer module except `feasibility_scorer.py` (12 other modules are hash-pinned in committed results; see Finding F).
- **Tests:** `python -B -m unittest tests.phaseNN.test_x -v` with `<home>/miniforge3/envs/pinn-train/bin/python`; pytest is not installed.
- **Tooling:** the project instructions require the Sequentialthinking MCP tool for multi-step work (executor concern). The `pinn/` live-code ban applies to the v1.4-v1.6 specwork milestones; in v2.4 `pinn/` is the code under construction.
- **User global rules:** formal concise tone, no emojis; expensive (over 60 s) validation commands must retain complete stdout, stderr, exit status and elapsed time in a session-specific temp file outside the repo and be reused rather than re-run when inputs are unchanged; no git write operations by research agents.
- **GSD tooling cautions (memory):** `gsd state.*` mutators regress `STATE.md` counters (snapshot, diff, restore, hand-edit); `gsd-planner` can leak stray tool-call closing tags into PLAN.md tails (verify plan files yourself); a `gsd-plan-checker` PASS is not evidence; the decision-coverage parser breaks on bullets lacking `:` or ` — ` right after the bold label, so write decision lines as `**D-NN:** text`.

## Architectural Responsibility Map

The template's web tiers do not apply; this phase has these ownership tiers.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Reading assigned train records | Data access (`split_allowlist.AllowlistedCorpusReader` + `production_reference.load_reference`) | Preflight (records manifest) | The only corpus choke point; refuses test-split keys before a path is built (`split_allowlist.py:188-194`). |
| Loss, residual, schedule, polish math | Training compute (harness process, MPS float32) | Trainer functions (`loss_catalog`, `physics_residual`, `controllers` helpers) | INST-05(a): the trainer's functions, composed not copied. |
| Tiering, budget rule, polish stop, G2, counting | Frozen rules (`feasibility_scorecard.py`) | Scorer (`feasibility_scorer.py`) | Pre-registered; may not be re-implemented or edited. |
| Long-run survival (detach, signals, resume) | Orchestration (launcher + supervisor) | Harness signal handlers | Generation 6 was lost silently without this. |
| Evidence (records, weights, protocol, verifier) | Evidence store (git, `.planning/phases/60-.../evidence/`) | Atomic writers (`atomic_io`, `evidence_io`) | Re-derivable; plain git per D-10. |
| Authorizing a non-locked `first_omega_0` | Governance (owner + committed ruling file D-11) | Harness ruling loader | A physics arm must refuse any value the file does not name. |
| Refusing harness records downstream | Production paths (`pinn.evaluate`, `pinn.training.checkpoint`) | Tests (INST-05(c)) | Structural refusal exists; the test proves it. |

## Standard Stack

No external package is installed. Everything below is already present in the `pinn-train` conda environment or in the repository.

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.11.15 | Runtime | `[VERIFIED: ran python in <home>/miniforge3/envs/pinn-train, 2026-10-18]` |
| torch | 2.12.1 | Autograd, `torch.func.vmap/jacrev`, `Adam`, `LBFGS`, `CosineAnnealingLR`, MPS | `[VERIFIED: ran, torch.backends.mps.is_available() True]`; the project's pinned runtime |
| numpy | 2.4.6 | float64 scoring arithmetic, RNG streams | `[VERIFIED: ran]` |
| unittest (stdlib) | - | Test framework | pytest, scipy and safetensors are absent `[VERIFIED: importlib.util.find_spec False]`; Phase 59 tests use unittest |

### In-repo building blocks (reuse, do not rewrite)
| Module | Provides | Used for |
|--------|----------|----------|
| `pinn.loss_catalog` | `data_huber_loss`, `ic_anchor_loss`, `causal_physics_loss`, `soft_energy_loss`, `angular_momentum_loss`, `compose_total`, `LossWeights`, `_matched_plummer_hamiltonian`, `_angular_momentum` | All loss terms (INST-05(a) mutation target) |
| `pinn.physics_residual` | `componentwise_du`, `softened_acceleration`, `physics_residual` | Velocity/acceleration and the residual; reverse-over-reverse (`jacrev`), MPS-safe |
| `pinn.training.controllers` | `accumulate_chunked_data_term`, `_bin_mean_residuals`, `_bin_index_for_times`, `_RATIFIED_N_BINS`, `RunController` (test oracle) | Chunked data term, 16-bin means, cross-check oracle |
| `pinn.training.scheduled_weights.ScheduledWeights` | PHYS-05 warmup, freeze, state_dict | Physics-arm lambda schedule |
| `pinn.training.config.OptConfig` | `lr_for_stage(k)`, betas, eps, microbatch 256, chunk 1024 | LR_k and Adam constants |
| `pinn.training.grad_clip.GradClipper` | Adam-only adaptive median clip, `state_dict` | Open Question OQ-3 |
| `pinn.network` / `pinn.architecture_spec` | `SQRSkipResNetSIREN`, `build_network`, `ArchitectureSpec` | The production network (795,657 parameters `[VERIFIED: built it]`) |
| `pinn.data.batches._stratified_full_slot_rows` | The 16-bin x 256 collocation draw | Physics collocation (single system repeated 256 times) |
| `pinn.verification.split_allowlist` | `SplitAllowlist`, `AllowlistedCorpusReader`, `install_open_attestation` | Corpus access, test-split refusal, files-opened attestation |
| `pinn.verification.production_reference` | `load_reference`, `recover_normalizer_from_checkpoint`, `stats_digest`, `resident_record` | References, real normalized IC13 |
| `pinn.verification.feasibility_scorecard` / `feasibility_scorer` | Frozen rules; `score_network`, `network_trajectory`, `score_trajectory` | Everything graded |
| `pinn.verification.evidence_io` | `write_json`, `canonical_json_bytes`, `module_hashes`, `memory_preflight`, `begin_long_step` | Atomic redacted evidence writes (import only; never edit) |
| `pinn.training.atomic_io` | `atomic_write_text`, `atomic_write_torch` | Atomic checkpoint writes |
| `pinn.training.determinism` | `capture_rng_state`, `restore_rng_state`, `REPRODUCIBILITY_SCOPE` | Exact-continuation resume |
| `pinn.training.signals` | `SignalState`, `install_signal_handlers` | Graceful stop |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Own thin loop composing catalog functions | Build a real `RunController` per arm and call its private step methods | Exact production math, but deep private coupling, a heavy constructor, and `_non_data_terms`/L-BFGS closure are monolithic over 4096 rows (memory). CONTEXT says the harness does not enter the production loop. Use a real controller only as the equivalence oracle in tests. |
| `CosineAnnealingLR` + explicit lr reset for the D-03 extension | `CosineAnnealingWarmRestarts(T_0=B, T_mult=1)` | Warm restarts is a closed form and restarts natively but is not bit-identical to the trainer's recursive `CosineAnnealingLR`. Keep the trainer's object. |
| Plain git for weights (D-10) | Git LFS, safetensors | Rejected by D-10; safetensors is not installed. |

**Installation:** none.

**Version verification:** `python -c "import torch, numpy"` in the pinn-train environment printed torch 2.12.1 and numpy 2.4.6 `[VERIFIED: ran 2026-10-18]`; no registry lookup is needed because nothing is installed.

## Package Legitimacy Audit

No external package is installed or recommended in this phase. All required packages are already present (see Standard Stack). Therefore no `package-legitimacy check` run and no `checkpoint:human-verify` install task is required.

| Package | Registry | Age | Downloads | Source Repo | Verdict | Disposition |
|---------|----------|-----|-----------|-------------|---------|-------------|
| (none) | - | - | - | - | - | No installs |

**Packages removed due to [SLOP] verdict:** none
**Packages flagged as suspicious [SUS]:** none

## Verified Findings by Research Question (A-L)

Lettering follows the orchestrator's research brief. Every claim carries a provenance tag. Quoted values are verbatim from the cited line range. Where a pre-verified brief fact was wrong or incomplete, the correction is marked CORRECTION.

### A. Scope amendment (SPEC Req 1): what makes the six paragraphs verbatim

Method: a script parsed the six labeled paragraphs from the `## Amendment text` block of `60-SPEC.md` and tested each sentence for containment in `REQUIREMENTS.md` and `ROADMAP.md` under four normalizations `[VERIFIED: ran this session]`. Result under whitespace collapse only (`' '.join(text.split())`):

| Amendment paragraph | Target file | Today | Location of near-matches | Edit needed |
|---|---|---|---|---|
| SCOPE-39 | `REQUIREMENTS.md` row at line 319 | 4 of 5 sentences; the 1st matches only if the `**` pair is deleted | Table cell opens `**Stage-0 only, with three read-only or diagnostic exceptions:**` | Delete the two `**` markers in that cell. Keep the trailing tag `[2026-10-17 spec amendment]`. |
| FEAS-04, last acceptance bullet | `REQUIREMENTS.md:135` | Verbatim, 2 of 2 | - | None |
| Roadmap success criterion 3, added sentence | `ROADMAP.md:234` (success criterion 3) | Verbatim ("If the ladder stopped at G2, Rung 2 is recorded as skipped."). The same sentence also ends the Gate G2 paragraph at `ROADMAP.md:225`. | - | None. Check it inside the success-criterion-3 item, not by whole-file count. |
| FEAS-09 | `REQUIREMENTS.md:187`, `:195` | 1 of 3 ("On a continue they use the approved setting.") | :187 reads "These run only if the ladder continues past G2: G2 passed, or the owner continued at checkpoint ④."; :195 reads "...with one of the pre-registered reasons: no rescue, or checkpoint ④ answered go to the verdict." | Make the three sentences one contiguous paragraph in the FEAS-09 body: "The probes run only if the ladder continues past G2. On a continue they use the approved setting. If the ladder stopped at G2, FEAS-09 is recorded as skipped, with one of the same two reasons." Keep any extra explanation as separate sentences outside that paragraph. |
| SCOPE-44 | `REQUIREMENTS.md:324` | 0 of 1 | Clause "...and the hard-stage probes run only if the ladder continues past G2 (four arms, about 12 hours)." | Add the stand-alone sentence "The hard-stage probes run only if the ladder continues past G2." (reword the clause so the arm count and hours do not repeat the condition). |
| Checkpoint ④ continue | `REQUIREMENTS.md:337-340` (Owner Checkpoint 4) | 1 of 3 ("Phase 60 does not edit `pinn_architecture.md`." is in the FEAS-03 rescue bullet, :126) | Content is spread and reworded across :126, :337-340, :351 | Insert the three sentences contiguously in Owner Checkpoint 4. The SPEC names no home for this paragraph; Owner Checkpoint 4 is the recommended one (planner's choice, mechanical). |

**Normalization (recommended):** `unicodedata.normalize("NFC", ...)` then `' '.join(text.split())` on both sides; containment must hold inside the paragraph's designated section (a requirement entry, a table row, an Owner Checkpoint item, or the success-criterion-3 item), not by whole-file count, because the Roadmap sentence legitimately appears twice (see the table). Do not strip markdown. The Checkpoint ④ paragraph contains literal backticks around `first_omega_0` and `pinn_architecture.md` and the circled digit U+2463, so a stripping rule would weaken the check, and the SPEC's own edge row says "Amendment equality is exact after collapsing whitespace" (`60-SPEC.md` Edge Coverage, encoding/R3). Make the files conform rather than loosening the rule. Fallback if the owner objects to losing the SCOPE-39 bold: tolerate deletion of the two-character token `**` only, documented in the test.

**Check design:** `tests/phase60/test_amendment.py` parses the SPEC block itself (single source of truth), asserts each paragraph is contained in its designated section of its designated file, asserts `hashlib.sha256(<scorecard bytes>) == SCORECARD_SHA256` (`f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b`, `feasibility_scorecard.py:44`), calls `load_scorecard()`, and proves the four frozen files (`_frozen_rels`: scorecard JSON, `feasibility_scorecard.py`, `59-SCORECARD.md`, `scorecard-freeze.json`, `verify_phase59_evidence.py:145-151`) are unchanged since the freeze commit (`python .planning/phases/59-.../evidence/verify_phase59_evidence.py scorecard-frozen` prints `SCORECARD-FROZEN-OK`, or `git diff --quiet <freeze> HEAD -- <four paths>`). The amendment commit must precede any real-arm record; record its SHA in the run protocol (Finding L, Req 4).

### B. Learning-rate schedule and warmup: reuse, do not re-implement (D-01..D-05)

- **LR_k:** `OptConfig().lr_for_stage(k)` returns `adam_lr_base * adam_lr_decay ** k` with `adam_lr_base: float = 1e-3` and `adam_lr_decay: float = 0.7` `[VERIFIED: pinn/training/config.py:664-667, 705-707]`. Spec text: `LR_k = 10^{-3} x (0.7)^k` and "Initialize a cosine annealing scheduler" `[VERIFIED: ctl_instruction.md:1803, 1805]`. Values: k=0 1e-3; k=4 2.401e-4; k=6 1.17649e-4.
- **Adam:** the trainer builds `torch.optim.Adam(model.parameters(), lr=cfg.opt.lr_for_stage(k), betas=cfg.opt.adam_betas, eps=cfg.opt.adam_eps)` and `CosineAnnealingLR(optimizer, T_max=max(n_adam_k, 1), last_epoch=scheduler_last_epoch)`, and calls `optimizer.step()` then `scheduler.step()` each epoch `[VERIFIED: controllers.py:2634-2639, 2658-2660, 2162-2163]`. `OptConfig.adam_betas == (0.9, 0.999)`, `adam_eps == 1e-8` `[VERIFIED: config.py:664-665]`.
- **Warmup:** `ScheduledWeights(n_adam_k, *, lambda_phys_max=1.0, lambda_e_max=0.0, lambda_l_max=0.0, lambda_ic=1.0, warmup_length=None)`; `I_warm = min(2000, int(0.1 * n_adam_k))`; `current(epoch)` returns `LossWeights` with `lambda_data` pinned at 1.0, `lambda_ic` unramped, others scaled by `min(1, epoch/I_warm)` `[VERIFIED: scheduled_weights.py:91-127, 191-212]`. Spec: `I_warm = min(2000, 0.1 * N_Adam,k)` `[VERIFIED: pinn_architecture.md:699]`. Per-stage maxima: `PHYS05_LAMBDA_PHYS_MAX = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)`, `PHYS05_LAMBDA_E_MAX = (0.0, 0.0, 1e-2, 1e-1, 1.0, 1.0, 1.0)`, `PHYS05_LAMBDA_L_MAX = (0.0, 0.0, 1e-2, 1e-1, 1.0, 1.0, 1.0)` `[VERIFIED: pinn/constants.py:92-94]` (CORRECTION: the brief cited pinn_architecture.md ~:669; the formula is at :699-704). So at k=0 (Stage 0) energy and angular-momentum weights are 0 and need not be computed; at k=4 and k=6 (probe Rung 2b) both are 1.0.
- **N_Adam,k for the ramp** is the arm's budget `B` (the cosine length), so `I_warm = min(2000, floor(0.1 B))`. On the extension (D-03) `current(epoch)` with epoch >= B is already at ramp 1, so "no repeat of the ramp" is automatic; do not call `rewarm()`.
- **Polish freeze:** the trainer calls `scheduled_weights.freeze()` then `current(0)` before L-BFGS `[VERIFIED: controllers.py:2435-2436]`, matching the ruling "freeze the segment's collocation samples and detached causal weights" at the Adam-to-L-BFGS handoff `[VERIFIED: 57-RULING.md:112-124]`.
- **D-03 second cosine, verified numerically** (torch 2.12.1, CPU, B=10) `[VERIFIED: ran this session]`: (A) continuing the same `CosineAnnealingLR` past `T_max` does not restart; the rate hits 0 at step B then climbs back through the second half-period (0, 2.45e-5, 9.55e-5, ...). (B) Constructing a new `CosineAnnealingLR` on the same optimizer without touching `group["lr"]` stays at 0 forever, because epoch 0 keeps the current (near-zero) rate and the recursion is multiplicative. (C) Setting `group["lr"] = group["initial_lr"]` for every param group and then constructing a new `CosineAnnealingLR(optimizer, T_max=B)` reproduces the first cosine exactly (max difference 0.0). The torch docs confirm this class has no periodic restart `[CITED: https://docs.pytorch.org/docs/2.12/generated/torch.optim.lr_scheduler.CosineAnnealingLR.html]`. Implement (C), keep the same optimizer object (Adam moments kept), and add a test that asserts the lr trace over [B, 2B) equals the trace over [0, B).
- **Resume:** the rate recursion uses the current `group["lr"]`, so a resumed scheduler needs `last_epoch=k-1` and an optimizer whose param groups carry `initial_lr` (restored by `optimizer.load_state_dict`) `[VERIFIED: torch source of LRScheduler.__init__ read this session; controllers.py:2648-2660 does the same]`. Checkpoint the scheduler `state_dict()`, the segment index (first or second cosine) and `B`.
- **Probe Rung 2b:** `LR_4`/`LR_6` and clip stage 4/6, `lambda_E = lambda_L = 1.0` (D-05). Data-only arms everywhere, including probe Rung 1, use k=0 (D-04).

### C. The frozen scorecard: exact signatures, behavior, and cadence (brief item C)

All functions live in `pinn/verification/feasibility_scorecard.py`, take `scorecard` keyword-only, and are the only legal source of tiers, budgets, G2 and counting `[VERIFIED: file read in full]`.

| Function | Signature | Behavior the harness depends on |
|---|---|---|
| `load_scorecard` | `(path=None, *, expected_sha256=SCORECARD_SHA256) -> Scorecard` (:558-592) | Canonical-bytes, key-set, value and SHA checks; raises `ScorecardError` |
| `tier_of` | `(E, eps_h, *, scorecard) -> int` (:595-617) | Inclusive cuts; non-finite `E` -> 0; non-finite `eps_h` fails every level with an energy bound, so `E <= 0.1` with non-finite `eps_h` is Tier 1 |
| `counts` | `(tier, E, E_formula, *, scorecard) -> bool` (:684-703) | `E_formula is None` raises `OwnerRouted("two-Kepler formula not applicable on a counted system")`; strict `position < formula`; `min_tier` 1 |
| `g2_fires` | `(rung1_tiers, *, scorecard) -> bool` (:706-715) | Requires a list or tuple of exactly 3 tiers; counts tiers `< 1`; fires at `>= 2` |
| `decision_verdict` | `(*, g2_fired, sweep_rescued, rung2b_counts, rung3_counts, control_branch, rung1_beats_formula, scorecard) -> dict` (:718-776) | `g2_fired and sweep_rescued` raises `OwnerRouted("owner checkpoint 4")`; `g2_fired` with any later-rung input not `None` raises `ValueError`; `g2_fired` alone returns `{"verdict": "RETHINK-REPRESENTATION", "representation_limit_qualifier": False, "reasons": [...]}` |
| `steps_budget` | `(cap_hours, timing_wall_seconds, timing_steps, *, scorecard) -> int` (:779-799) | `floor(cap*3600 / (wall/steps))`; `timing_steps >= 50` else `ValueError` |
| `still_improving` | `(readings, budget_steps, *, scorecard) -> bool` (:802-811) | `readings` are `(step, E)` pairs with integer `step` in `0..budget`; reference window `step <= 0.75*budget`, final window above it; non-finite `E` ignored; no finite final reading -> `False`; finite final and no finite reference -> `True`; else `best_final <= 0.9 * best_ref` |
| `budget_outcome` | `(readings, budget_steps, *, extended, scorecard) -> dict` (:814-839) | `{"outcome": "complete"}`, or `{"outcome": "extend", "new_budget_steps": 2*budget}` when not yet extended, or when `extended=True` and still improving `{"outcome": "inconclusive", "rate_per_step": (best_ref - best_final)/(best_ref*0.25*budget)}`; raises `OwnerRouted("improvement rate is not determinable without a finite reference-window reading")` if the rate cannot be formed |
| `scoring_cadence_ok` | `(reading_steps, budget_steps, *, scorecard) -> bool` (:842-865) | Readings must include step 0 and step `budget`; no gap above `scoring_cadence_max_fraction * budget` |
| `polish_should_stop` | `(outer_calls_without_improvement, polish_wall_seconds, adam_wall_seconds, *, scorecard) -> bool` (:868-888) | `calls >= 5` or `polish_wall >= 0.25 * adam_wall`; `adam_wall` must be finite and `> 0` |
| `better_state` | `(adam_state, polish_state, *, scorecard) -> str` (:894-906) | States are mappings with `E` and `eps_h`; returns `"polish"` only if strictly better on `(E, eps_h)` with non-finite last; an exact tie keeps `"adam"` |

Frozen values `[VERIFIED: feasibility_scorecard_v1.json]`: `budget_rule` (lines 14-28) `cap_hours_single_system: 3.0`, `extensions_max: 1`, `extension_factor: 2.0`, `after_extension: "inconclusive_with_rate"`, `scoring_cadence_max_fraction: 0.05`, `still_improving_reference_fraction: 0.75`, `still_improving_final_fraction: 0.25`, `still_improving_min_relative_drop: 0.1`, `still_improving_statistic: "best_E"`, `timing_run_min_steps: 50`; `lbfgs_polish` (398-409) `lbfgs_history_size: 10`, `lbfgs_line_search: "strong_wolfe"`, `lbfgs_max_iter: 50`, `physics_arm_freeze: "57-RULING.md:112-124"`, `report_both_states: true`, `stop_after_outer_calls_without_improvement: 5`, `stop_at_fraction_of_adam_wall_time: 0.25`; `gate_g2` (379-397) `grid: [60.0, 120.0, 240.0, 480.0]`, `locked_value: 30.0`, `parameter: "first_omega_0"`, `rescue_tier: 1`, `trigger_below_tier: 1`, `trigger_min_systems: 2`, `on_rescue: "owner_checkpoint_4"`, `on_no_rescue: "RETHINK-REPRESENTATION"`; `tiers` (613-634) `comparison: "inclusive_le"`, levels `3: E<=0.01, eps_h<=1e-05`, `2: E<=0.01, eps_h<=0.001`, `1: E<=0.1, no energy bound`, `non_finite_E_tier: 0`; `scoring_grid` (526-536) `tier_defining: "gold_sibling"`, `gold_dt: 0.01`, `base_dt: 0.08`, `reported_beside: ["base"]`, `t_max: 10.0`; `counting_rule` (49-53) `formula_comparison: "strictly_less"`, `formula_not_applicable: "owner_routed"`, `min_tier: 1`.

**Where the 5 percent cadence is defined (brief asked):** `budget_rule.scoring_cadence_max_fraction = 0.05` (JSON line 21), enforced by `scoring_cadence_ok`. D-06's "no gap larger than 5% of the step budget" is that field. `accuracy_cadence.every_steps = 100` (JSON line 6) is Rung 3 and the control only; it does not apply to single-system arms.

**How the harness must drive the rules:**
1. Timing run -> `B = steps_budget(3.0, wall, steps, scorecard=sc)`.
2. Reading steps: `0`, every `floor(0.05*B)` steps, and `B` (so `scoring_cadence_ok(steps, B)` holds). Readings are scored on the gold grid.
3. At step `B` call `budget_outcome(readings_so_far, B, extended=False)`. On `"extend"` run the second cosine to `2B` and call `budget_outcome(all_readings, 2B, extended=True)`; the windows are recomputed against `2B`. Readings taken every `0.05*B` already satisfy `scoring_cadence_ok(steps, 2B)` (limit `0.1*B`).
4. After the final Adam step score the Adam state; run the polish; score the polish state; `better_state(...)`; `tier_of` already inside the score; `counts(...)` for the three panel systems only.
5. Never wrap `counts`, `budget_outcome` or `decision_verdict` in a handler that swallows `OwnerRouted` (SPEC prohibition 6).

### D. R_ref and GATE-04 (D-07, D-08)

- **Artifact:** `pinn/verification/artifacts/r_ref_stage0.json`: `r_ref = 19749775821.24417`, `valid: true`, `statistic: "median"`, precision `float64`, device `cpu`, `eta_c 1.0`, `t_max 10.0`, 16 bins x 256 = 4096 points, six cases (labels `41`, `42`, `43`, `0`, `7`, `41-variable-mass`; `ic13_mode` `zero` for the first five, `random_tanh` for the last), so no real system `[VERIFIED: ran, read JSON this session]`. Loader: `pinn.training.config.load_frozen_r_ref_artifact(path)` takes any path and validates schema `phase56-r-ref-stage0/v1`, `valid is True`, the 16x256 configuration, six 16-entry rows and non-empty `git_sha`/`timestamp` `[VERIFIED: config.py:166-236]`.
- **Contract:** "Re-measure `R_ref` and re-run GATE-04 after any change to `first_omega_0`, depth, width, power-skip exponent, LayerNorm placement or stabilizer, initialization bounds, `D`, `T`, `epsilon_soft`, IC13 normalization, `n_col`, `M`, count unit, selected-slot semantics, or bin/allocation semantics." `[VERIFIED: pinn_architecture.md:454]`. GATE-04 complete-pass rule: non-anchor spread `max(w_1..w_15)/min(w_1..w_15) >= 2`, then multiply all 16 squared-residual bin means by `alpha = log(2)/(2*P_15)` and require the front to reach bin 15 with every perturbed weight `>= 0.70` `[VERIFIED: 57-RULING.md:32-90]`.
- **Producer:** `gate04_train_free.compute_r_ref(cases, *, precision, device)` (:757), `run_gate(cases=DEFAULT_CASES, *, precision="float64", device="cpu") -> Gate04Verdict` (:845), `write_r_ref_artifact(verdict, path=R_REF_ARTIFACT_PATH, *, gate_evidence_path=None, gate_evidence_sha256=None)` (:911), CLI `main` (:1205).
- **BLOCKER for D-07 (not in the brief):** `_measure_raw_bin_means` builds `build_network(ArchitectureSpec(seed=case.seed), ...)` `[VERIFIED: gate04_train_free.py:716]`, and `ArchitectureSpec.__post_init__` raises `ValueError("ArchitectureSpec.first_omega_0 must be 30.0 ...")` for any other value `[VERIFIED: architecture_spec.py:119-124; ran ArchitectureSpec(first_omega_0=60.0) -> ValueError]`. There is no parameter anywhere in `compute_r_ref`, `evaluate_case` or `run_gate` for omega. Re-measuring "at the approved `first_omega_0`" therefore needs a code seam: add a keyword `first_omega_0: float | None = None` to `_measure_raw_bin_means`, `compute_r_ref`, `evaluate_case` and `run_gate` (default `None` keeps today's path unchanged) that builds the network through the diagnostic builder (Pattern 2). Do not weaken `ArchitectureSpec` (SCOPE-43).
- **HAZARD:** the CLI's `--r-ref-path` defaults to the governed artifact, and on a canonical six-case complete PASS it overwrites it (`gate04_train_free.py:1205-1268`, `write_r_ref_artifact(verdict_obj, path=args.r_ref_path, ...)`); on a BLOCK it writes a Phase-57 `terminal-state.json`. Never run that CLI with default paths for a Phase 60 re-measure. Provide a separate Phase 60 entry that writes the re-measured artifact to a Phase 60 evidence path, never touches `R_REF_ARTIFACT_PATH`, never writes `terminal-state.json`, and returns PASS or BLOCK to the caller (BLOCK stops for the owner, D-07). `write_r_ref_artifact` accepts a `path`, so the artifact schema does not change; carry omega in the Phase 60 record that cites the artifact's SHA-256 (the frozen artifact key set has no omega field).
- **Which R_ref the probes use on a continue:** see Open Question OQ-2 (D-08's literal "committed Stage-0 R_ref" is the omega=30 value, which the spec's own invalidation list declares invalid once omega changes).
- **Scorer context column:** `score_network` always normalizes its context residual by the governed (omega=30) artifact via `load_governed_r_ref()` (`feasibility_scorer.py:327-330`). It is context only and never tiers; record which R_ref normalized the physics loss and which normalized the context column.
- **Cost:** the gate measures six cases twice (`compute_r_ref`, then `evaluate_case`) on CPU float64 at 4096 rows; expect minutes `[ASSUMED]`. Run it detached, not inline.
- **Entry sketch for the Phase 60 re-measure (D-07):** `python -B -m pinn.verification.gate04_omega_remeasure --ruling <60-CHECKPOINT-4-RULING.md> --evidence-root <.planning/phases/60-.../evidence/continue>`. It (1) loads and validates the D-11 ruling (tracked, clean, strict block) and reads `approved_first_omega_0`; (2) calls `run_gate(DEFAULT_CASES, precision="float64", device="cpu", first_omega_0=<value>)`; (3) writes the raw gate evidence under the Phase 60 evidence root; (4) on a complete PASS only, calls `write_r_ref_artifact(verdict, path=<evidence-root>/r_ref_omega_<value>.json, gate_evidence_path=..., gate_evidence_sha256=...)`; (5) on BLOCK exits non-zero and writes nothing else, so the continue plan stops for the owner. Test that the governed `pinn/verification/artifacts/r_ref_stage0.json` has the same SHA-256 before and after, and that the default-path (`first_omega_0=None`) run reproduces today's behavior.

### E. Scorer MPS fix (GAP-59-13, SPEC Req 3)

- **CORRECTION (three sites, not one):** `network_trajectory` widens at three places: positions, velocities, and (when `want_acceleration`) accelerations `[VERIFIED: feasibility_scorer.py:417, 420, 425]`, each `.detach().to(device="cpu", dtype=torch.float64).numpy().reshape(-1, 3, 3)`. A fix that patches two leaves `score_network` (which passes `want_acceleration=True`, :454-463) broken. The GAP entry itself says "the two ... lines" (`59-GAPS.md` GAP-59-13); the third was missed.
- **Reference:** Phase 59's driver copy `jx02_jx05.py::_network_trajectory` uses `_cpu64(t) = t.detach().to("cpu").to(torch.float64)` at all three sites `[VERIFIED: jx02_jx05.py:56-60, 346-388]`. The earlier flatten fix in 59-07 is commit `936f7f56`. Failure evidence: `TypeError: Cannot convert a MPS Tensor to float64 dtype`, reproduced 2026-10-16 `[CITED: 59-GAPS.md GAP-59-13]`.
- **Fix:** one module-private helper in `feasibility_scorer.py`, used at the three sites; no new imports; CPU float64 behavior unchanged (`.to("cpu")` and `.to(torch.float64)` are no-ops there).
- **Tests (new `tests/phase60/test_scorer_mps.py`):** (1) MPS integration: tiny float32 network on `torch.device("mps")`, `network_trajectory(..., dtype=torch.float32, device=mps, want_acceleration=True)` returns float64 numpy of shape `(N,3,3)` and agrees with the CPU float64 result within float32 tolerance; make a missing MPS a hard failure on this Mac (an env flag turns skip into fail). (2) Static: an AST/regex guard that the scorer contains no `.to(device="cpu", dtype=` pattern. (3) CPU equality: the existing `tests.phase59.test_diag07_panels.NetworkScoreTests` already pins the driver copy equal to `score_network` field for field on a CPU float64 network and passes at HEAD in 1.1 s `[VERIFIED: ran]`; it plus `tests.phase59.test_scorer_network` (9 tests, 1.8 s `[VERIFIED: ran]`) are the "unchanged on CPU float64" proof. (4) The "fails on the old widen" half is evidenced by the GAP record; a direct `assertRaises(TypeError)` on a raw old-idiom MPS call is a platform probe and should be a clearly named, non-gating test because a future torch could make it pass.
- **New SHA-256:** compute after the edit, record in `evidence/scorer-successor.json` (Finding F). Phase 59 evidence that pins the old digest is not re-run.
- **CPU float64 cross-check (Req 3):** after an MPS float32 arm, copy the scored weights into a CPU float64 network (the diagnostic builder with the same omega, `load_state_dict` with each tensor moved `.to("cpu").to(torch.float64)`), feed the same float32-rounded normalized IC13 widened to float64, call `score_network(..., dtype=torch.float64, device=cpu)`, and compare tier and the counts-boolean. Any difference raises a dedicated owner-routed exception (a fourth stop alongside the three frozen `OwnerRouted` cases) and the better score is never taken. Cross-check both scored states of every real arm; interim cadence readings are MPS only.

### F. Phase 59 verifier after the scorer change (D-09): the minimal change is larger than D-09 states

Facts `[VERIFIED: ran + read]`:
- Thirteen modules are hash-pinned across the committed Phase 59 results: `evidence/diag07/diag07_common.py`, `jx01_jx10.py`, `jx02_jx05.py`, and `pinn/verification/{baselines,dataset_survey,evidence_io,feasibility_scorecard,feasibility_scorer,nn_copy,production_reference,split_allowlist,stage0_census,two_kepler}.py`. Each has exactly one recorded digest and all match the current files. Ten result files cite the scorer (`cd5019a2ba5604f39d5c6e01763ff3f0e53547920a57bbf174ebc3bb0a73870b`, 17,626 bytes): `baselines/{baselines,nn_copy,two_kepler}.json` and `diag07/{g1,jx01,jx02,jx03,jx04,jx05,jx10}.json`. Only the scorer may change (D-09), so Phase 60 must not edit the other twelve.
- `_check_result` re-hashes every `producer_sha256` entry and fails on mismatch (`verify_phase59_evidence.py:434-440`: `current = sha256_file(repo_path(str(relative), ...)); if current != digest: fail(...)`). `_run_area` calls it for every result, then `_rederive(area)` unless `--skip-rederive` (`:731-744`); `cmd_final` runs every area with `skip_rederive=False` (`:911-943`).
- The scorer is not one of the four frozen files (`_frozen_rels`, :145-151), so editing it does not trip `scorecard-frozen`.

**Required work, in order:**
1. `_check_result`: read the committed successor record once; for exactly one path (`pinn/verification/feasibility_scorer.py`) accept `digest == record.predecessor_sha256 and current == record.successor_sha256`; every other module must match as today; a record naming more than one path or a list of successors is refused; an absent record keeps today's strict behavior. Require the record to be tracked and clean (as `is_tracked`/`is_clean` do for other inputs).
2. **Gap in D-09 (not in the brief):** `baselines --check` re-derivation fails after the fix. `_full_mode(check=True)` re-renders the payloads, whose `producer_sha256` embeds the live scorer digest (`PRODUCER_MODULES` includes `feasibility_scorer.py`, `baselines.py:82-91`), and byte-compares them with the committed files (`baselines.py:666-681`, prints `BASELINES-CHECK-DIFF: <name>` and returns 1). `_rederive` then fails with "baselines re-derivation exited 1". Editing `baselines.py` to avoid this would change its own pinned digest (a second successor, which D-09 forbids). Recommended resolution (OQ-1): in `_rederive("baselines")`, copy the committed `baselines/` directory to a temporary evidence root, replace the predecessor digest with the successor digest inside the copies (a same-length string substitution, so canonical JSON bytes are otherwise identical), and run `python -B -m pinn.verification.baselines --check --evidence-root <tmp>` (the CLI already has `--evidence-root`, `baselines.py:_parse_args`). This keeps all 13 other digests checked and Phase 59 verifiable at HEAD. Cost: one extra baselines run, about 66 s `[CITED: STATE.md line 57]`.
3. **Manifest self-hash (not in the brief):** `evidence/manifest.json` lists 49 files including `verify_phase59_evidence.py` itself and the three `diag07/*.py` drivers `[VERIFIED: ran]`; `_check_manifest("all")` fails with "changed file verify_phase59_evidence.py" after any edit. Rewrite it with `verify_phase59_evidence.py manifest --area all --write` after the verifier edit (`_write_manifest` stamps the current HEAD as `produced_at_head`); per-area manifests hash only files inside their own area directory, none of which change, so they are unaffected.
4. Re-run `verify_phase59_evidence.py final` detached; it printed `PHASE59-EVIDENCE-OK` in 644 s at Phase 59 close `[CITED: STATE.md line 40]`. Do not start another heavy job while it runs, and do not run it concurrently with a timing run or an arm (Pitfall 12).
5. New tests: a synthetic-repo test reusing the stub-producer fixtures in `tests/phase59/test_evidence_verifier.py` (the existing `test_result_producer_hash_must_match_current_bytes` at ~:921-937 is the template): successor accepted; same digest for a different path refused; a second successor refused; any other producer mismatch still refused; absent record strict; untracked or dirty record refused. `tests.phase59.test_evidence_verifier` takes about 70 s `[CITED: STATE.md line 41]`.
6. Keep the edit compatible with `tests.phase59.test_static_guards` (15 tests, 6.8 s, green at HEAD `[VERIFIED: ran]`): no new imports outside the allowed roots; the verifier is a scanned "evidence" file.

### G. Corpus records (SPEC Req 8 preflight content): all ten assigned records verified

Read-only run through `SplitAllowlist` + `AllowlistedCorpusReader` + `production_reference.load_reference` with the open-attestation hook installed `[VERIFIED: ran 2026-10-18, 0.14 s]`. The corpus lives in the main checkout; `resolve_data_root(None)` resolves to it. Folder names from `BRUTUS_FOLDER_TABLE`: `brutus_hierarchical` (hierarchical base), `brutus_hierarchical_gold_standard`, `brutus_standard_quasi_random` (standard base), `brutus_standard_quasi_random_gold_standard`.

| Record key | split | snapshots | within T (t <= 10 + 1e-9) | measured dt | inner pair | ordered raw masses | E (t=0) |
|---|---|---|---|---|---|---|---|
| hierarchical/base/1632 | train | 126 | 126 | 0.08 | (1,2) | 1.9505, 0.5885, 0.461 | -4.96846 |
| hierarchical/gold/1632 | train | 1002 | 1001 | 0.01 | (1,2) | same | same |
| hierarchical/base/851 | train | 126 | 126 | 0.08 | (1,2) | 1.797, 0.9001, 0.3029 | -5.48934 |
| hierarchical/gold/851 | train | 1002 | 1001 | 0.01 | (1,2) | same | same |
| hierarchical/base/4658 | train | 126 | 126 | 0.08 | (0,2) | 1.7451, 1.0415, 0.2134 | -11.83099 |
| hierarchical/gold/4658 | train | 1002 | 1001 | 0.01 | (0,2) | same | same |
| standard/base/2279 | train | 60 | 59 | 0.17 | (1,2) | 1.0, 1.0, 1.0 | -7.86021 |
| standard/gold/2279 | train | 1002 | 1001 | 0.01 | (1,2) | same | same |
| standard/base/3418 | train | 60 | 59 | 0.17 | (0,2) | 1.0, 1.0, 1.0 | -9.70997 |
| standard/gold/3418 | train | 1002 | 1001 | 0.01 | (0,2) | same | same |

Relative layout (no home path; the reader builds it, `split_allowlist.py:126-127, 266-268`): `<data_root>/brutus_output/<folder>/brutus_<variant>_<id:04d>.txt`, for example `brutus_hierarchical_gold_standard/brutus_hierarchical_1632.txt` and `brutus_standard_quasi_random/brutus_standard_2279.txt`. `<data_root>` is the main checkout's `simulation_data/Data` (directory named `Data`, parent `simulation_data`); base and gold siblings share the file name and differ by folder.

- Every key is in the train split and was admitted by the production admission gate (`NotAdmitted` was not raised). The attestation summary after the run was `{'train': 10, 'validation': 0, 'other_under_root': 0}`, `test_split_opened: 0`, `blocked_attempts: 0`, `refused_before_open: 0`.
- **Gold records have 1,002 snapshots; the last is at t = 10.01 (> T).** CONTEXT says 1,001 points, so every train and score path must window with the scorer's own rule `times <= t_max + 1e-9` (`baselines._window`, `baselines.py:~103-108`). Hierarchical base: 126 points (last time is 10.000000000000007, inside the tolerance). Standard base: 59 points inside T. Training on the 1,002nd point would put `u = 1.001` outside the network's `tau` domain.
- **Raw IC13 of base and gold siblings is bit-identical** (max absolute difference 0.0, equal canonical permutations) for all five systems `[VERIFIED: ran]`. So "which sibling supplies IC13" does not change the network input; record it anyway.
- **Normalizer (real normalized IC13):** `load_retained_checkpoint(repo_root, "stage0-v23g7-seed42", "stage-0-init.pt", expected_step=0)` then `recover_normalizer_from_checkpoint(reader, payload, tolerance=1e-6)`; the stats digest must equal `77526e53c394bbac4d4a0e8fdd5a7688f0bda108d41c56277b55ad426a7a79f6` (audit `reader_acceptance.json`, `normalizer.stats_sha256`, recovery residual `1.1920928955078125e-07`, source `recovered_from_checkpoint`) `[VERIFIED: read]`, as `baselines._recover_normalizer` does (`baselines.py:~315-333`). The network input is `tau_ic13 = [2u - 1, normalize_ic13(raw_ic13, stats)]`, float32 on MPS. Fail closed if the digest differs; the fallback normalizer in `production_reference` is a recorded deviation (GAP-59-06 option B) and must not be used silently.
- **Formula comparison inputs:** `evidence/baselines/two_kepler.json` `rows.singles` (applicable true): E_formula 1632 = 0.916813577071981, 851 = 0.4312413103776787, 4658 = 1.9697113677004474 `[VERIFIED: ran]`. A Tier >= 1 network (E <= 0.1) therefore beats the formula on all three, but the harness must still call `counts()`. Probe formula field: the string `"not applicable: no hierarchical split"` (`two_kepler.py:25`, `dataset_survey.py:73`); probes never call `counts()`.
- **Preflight (Req 8):** for each assigned key (train record and score record per arm, including Rung 2a's gold score record) require: key in train split, `reader.exists`, parse succeeds, snapshot count > 0, admitted, window count as above. Any miss -> that arm is blocked, no substitute fidelity or system, no fallback; a blocked Rung-1 arm makes G2 impossible. Commit a manifest of the results (key, split, snapshots, within-T count, measured dt, and a SHA-256 of the parsed float64 arrays so the read is re-derivable without storing a path). Never put the data root or home path in committed evidence (`evidence_io.guard_redaction`).

### H. Trainer functions the harness must call, per arm (INST-05(a))

All catalog signatures `[VERIFIED: loss_catalog.py read in full]`; trainer wiring `[VERIFIED: controllers.py:1148-1310, 1746-2017, 2361-2421]`.

| Arm | Terms and functions (all from the trainer) | Weights | Train record | Score record | Adam LR | Clip stage |
|---|---|---|---|---|---|---|
| Rung 1 data-only (incl. sweep, confirmation, uncovered, probe R1) | `data_huber_loss(pred.reshape(-1,3,3), targets.reshape(-1,3,3), dtype=, device=)` over every windowed point | `LossWeights(1,0,0,0,0)` | hierarchical gold (probe: standard gold), 1,001 pts | same gold (base beside) | k=0 cosine | 0 |
| Rung 2a physics + IC | `ic_anchor_loss(...)` + `causal_physics_loss(...)`; no data term | `lambda_ic=1`, `lambda_phys` ramped to 1 | hierarchical base (IC13 and t=0 anchor) | hierarchical gold | k=0 | 0 |
| Rung 2b full ratified | data + IC + physics (+ energy/angmom only when their weight > 0) | PHYS-05 at k=0: `lambda_E = lambda_L = 0` so energy and angmom are not evaluated | hierarchical base, 126 pts | hierarchical gold | k=0 | 0 |
| Probe 2279 Rung 2b | data (59 pts) + IC + physics + energy + angmom | k=4: `lambda_phys=1`, `lambda_E=lambda_L=1.0` | standard base | standard gold | k=4 (2.401e-4) | 4 |
| Probe 3418 Rung 2b | data (1,001 pts) + IC + physics + energy + angmom | k=6: all 1.0 | standard gold | standard gold | k=6 (1.17649e-4) | 6 |

Mechanics to mirror (the cross-check test proves equality against a real `RunController`):
- **Data term:** `_data_term`: `pred = model(tau_ic13, masses)` then `data_huber_loss` (Huber delta 1, mean over `(N,3,3)`). For the polish use `accumulate_chunked_data_term(model, data_points, *, weight, chunk_size, dtype, device)` (`controllers.py:577-621`; `chunk_size` 1024 from `OptConfig`), which `.backward()`s per chunk and returns a detached scalar.
- **Rung 2a has no data term but `LossWeights` forces it on:** `LossWeights.__post_init__` raises unless `lambda_data == 1.0` (`loss_catalog.py:169-173`). Implement "no data term" by not evaluating it (a zero tensor in `compose_total`'s `terms["data"]`), never by `lambda_data = 0`.
- **IC term:** `pred_r0 = traj(0)`, `pred_v0 = componentwise_du(traj, 0)[0].reshape(3,3)`, `ic_anchor_loss(pred_r0, true_r0, pred_v0, true_v0, dtype=, device=)` with `true_r0, true_v0 = r', dr'/du` at t=0 of the training record.
- **Physics term:** 4096 collocation rows = `_stratified_full_slot_rows([key]*256, rng=rng)` (one row per slot per bin; a single system repeated 256 times is exactly the "every slot is the same trajectory" case the roadmap describes), sorted ascending, redrawn every Adam step from the seed-42 numpy stream and frozen at the polish handoff (`57-RULING.md:112-124`: "Adam retains the already-ratified per-step sampling behavior"). Per chunk of 256: `first, second = componentwise_du(traj, u)`, positions by `vmap`, `force = softened_acceleration(positions, masses, dtype=, device=)`, `rbar = ((second - force)**2).sum(dim=(-2,-1)) / 3.0`. Pass 1 builds detached bin sums and counts with `_bin_index_for_times`; `causal_physics_loss(raw_bin_means, r_ref=r_ref, times=bin_centres, return_details=True)` gives the frozen `w_n`; pass 2 backwards each chunk with the constant row weight `w_n[bin] / (16 * r_ref * count[bin])` (`controllers.py:1772-1820, 1895-1951`). `causal_physics_loss` requires exactly 16 bin means when `r_ref` is supplied (`loss_catalog.py:378-383`).
- **Polish for physics arms:** the trainer's own L-BFGS closure calls `_weighted_non_data_terms` over all 4096 rows at once (`controllers.py:2385-2389`), the shape that produced the 1.5 -> 22.8 GB footprint spike on MPS (`:1724-1732`). The harness polish closure must use the pass-2 chunked backward with the frozen `w_n`, frozen rows and frozen lambdas (`scheduled_weights.freeze()`), plus `accumulate_chunked_data_term`.
- **Energy and angmom (probes only):** `soft_energy_loss(positions, velocities, h0, eps_h, *, masses, dtype, device)` and `angular_momentum_loss(positions, velocities, l0, *, masses, dtype, device)`, each scaled by `chunk_fraction` per chunk; `h0 = loss_catalog._matched_plummer_hamiltonian(r0.unsqueeze(0), v0.unsqueeze(0), masses, ...)[0]`, `l0 = loss_catalog._angular_momentum(...)[0]`; `eps_h = energy_floor_factor * S_H` with `energy_floor_factor = 1e-4` (provisional in `config.py` `_PROVISIONAL`). The `S_H` value is OQ-7.
- **Frozen monitor logging (D-06), physics arms only:** draw one 4096-row stratified set before step 1 (same seed stream, kept frozen), and at each reading run the chunked pass-1 (256 rows) to log `w_n` min/mean/max, `front_idx = max(n : w_n[n] > 0.5, default=-1)`, per-bin normalized and raw residuals, and `r_ref` (`controllers.py:1027-1073`). No halting, no guard (D-06).
- **Mutation proof (INST-05(a)):** import each function at module scope in the harness module that composes the step and call it by bare name, so `mock.patch.object(harness_module, "<name>", side_effect=scaled_wrapper)` changes the harness output. This is the INST-04 SC3 pattern (`tests/phase55/test_architecture_characterization.py:283-320`: `mock.patch.object(probe, "causal_physics_loss", ...)`, scale 2.0, assert the output scales by 2.0). Patch at least `data_huber_loss`, `ic_anchor_loss`, `causal_physics_loss`, `softened_acceleration`, `componentwise_du`, `soft_energy_loss`, `angular_momentum_loss`, `accumulate_chunked_data_term`. Add an identity test (`harness.data_huber_loss is controllers.data_huber_loss is loss_catalog.data_huber_loss`) and the equivalence test against `RunController._run_adam_step_microbatched` on the stub source from `tests/phase57/_fixtures.build_run_controller`, CPU float64, as Phase 59's `_trainer_cross_check` did (relative differences below 2e-7 on a tiny MPS controller, 59-07-SUMMARY).

### I. Long-run safety: launch, signals, resume, memory

- **Pattern to copy** (not import; the file lives in the Phase 57 evidence tree and its `RUN_NAMES` is closed): `launch_phase57_run.py` starts a supervisor with `subprocess.Popen(..., start_new_session=True, stdin=DEVNULL)` so closing a terminal or an agent session cannot signal the trainer; the supervisor runs `/usr/bin/caffeinate -is <pinned python> -m pinn.train ...`, writes `launch.json`, `process.json`, `output.log`, `exit.json`, `supervisor.err` under `runs/.launch/<run>/invocation-<n>/`, and a resume requires the previous `exit.json` to record exit code 130 (`INTERRUPTED_EXIT_CODE = 130`) `[VERIFIED: launch_phase57_run.py:36-47, 64-101]`. The supervisor itself installs no handlers; a deliberate stop goes to the trainer PID (memory: signal the real python PID, not `caffeinate`).
- **Handlers:** `pinn.training.signals.install_signal_handlers(state, on_escalate)` handles SIGINT (graceful; a second SIGINT after a 1.0 s debounce escalates and `os._exit(130)`) and SIGTERM (graceful, exit code 143); there is no SIGHUP handler `[VERIFIED: signals.py:44-75]`. CONTEXT asks the harness to save a checkpoint "when the run is terminated or its terminal closes", so install SIGHUP as a graceful stop too (exit 129). Generation 6 was lost silently for exactly this reason (memory: phase57-gen7-detached-launch). Governed stop codes to allow a resume: 129, 130, 143, each only when a valid resume checkpoint was written and a stop marker recorded; any other exit (including SIGKILL) means "an arm that cannot resume goes to the owner" (SPEC Req 8), never a silent restart.
- **Launch metadata cannot be committed from `runs/`:** the staged-path policy blocks `runs/*` except exact allowlisted generation-6/7 paths (`validate_staged_paths.py:11-27, 29-...`). Keep launch files untracked under the ignored `runs/` tree (`.gitignore:339 runs/`) and copy exit code, signal, wall seconds and invocation count into the committed arm record.
- **What a resume checkpoint must hold:** model, Adam state, scheduler `state_dict`, `ScheduledWeights.state_dict()`, `GradClipper.state_dict()` (if used), the four RNG streams via `determinism.capture_rng_state`, readings so far, budget `B`, extension flag and segment index, Adam wall seconds summed across segments, the frozen monitor and the frozen polish segment (rows, `w_n`, hashes; the trainer's schema is `phase57-lbfgs-segment/v1`), the L-BFGS `optimizer.state_dict()` (keys `H_diag, al, d, func_evals, n_iter, old_dirs, old_stps, prev_flat_grad, prev_loss, ro, t` `[VERIFIED: ran]`), outer-call and non-improving counters, and the SHA-256 of every harness module. The trainer rebuilds a fresh `LBFGS` on resume (`controllers.py:2443-2448`) and so loses curvature history; saving the optimizer state makes polish resume exact. Refuse a resume when module digests differ. Write with `atomic_write_torch`; load with `torch.load(..., weights_only=True)` (the Phase 59 static guard requires the literal keyword `[VERIFIED: test_static_guards.py torch_load_violations]`).
- **Mirror the trainer's refusals:** `RunController.load_state_dict` raises when an amended resume lacks `front_monitor` or `lbfgs_segment_state` (`controllers.py:845-850`) and `_start_lbfgs_segment` raises when `lbfgs_start > 0` without segment state (`:2213-2218`).
- **Memory and timing contamination:** `evidence_io.available_memory_bytes()` (the basis of `memory_preflight(required_bytes)`) sums free + inactive + speculative pages `[VERIFIED: evidence_io.py:462-498]` and reported 4.63 GiB available at research time `[VERIFIED: ran]`, below the 6 GiB bar, which is the situation CONTEXT's "ask the owner to close browsers" anticipates. Use it as advisory logging; the owner confirmation is the gate. Do not run any other heavy job (the Phase 59 `final` verifier, large test suites) during a timing run or an arm: the timing run's seconds-per-step sets the budget, so contention changes the experiment.
- **Do not reuse these Phase 59 helpers as-is:** `evidence_io.runtime_gate` returns exit code 5 above `RUNTIME_BUDGET_SECONDS = 600` (`evidence_io.py:35, 684-698`); `begin_long_step` defaults its lock to Phase 59's evidence tree (`:33, 566-570`), so pass `evidence_root=` pointing at the Phase 60 evidence directory.
- **MPS fallback env:** do not let `PYTORCH_ENABLE_MPS_FALLBACK` reach the process (project convention CTX-08) `[CITED: scripts/run_precision_probe.py:120-126]`; capture it before importing torch (as `overfit_probe.py:16-19` does) and record it in the run record.

### J. Refusal paths (SPEC prohibitions 1, 4, 8; INST-05(b),(c))

- **Test split:** `SplitAllowlist.require(key)` raises `SplitRefused` for any non-train/validation key before a path is built (`split_allowlist.py:188-194`); `install_open_attestation` also blocks withheld basenames at the audit-hook level and counts opens (`:357-414`). The harness takes a `RecordKey` from a closed arm catalog, never a path. Embed `attestation.summary()` in every record; the Phase 60 verifier asserts `test_split_opened == blocked_attempts == refused_before_open == 0`. Note `install_open_attestation` is process-global and raises if installed twice for different roots (`:366-371`); tests should reuse one root per process.
- **Evaluator:** `pinn.evaluate._resolve_owning_run` accepts a checkpoint only if its run directory (conventional `.../checkpoints/<file>.pt` parent's parent, or the file's own parent) holds both `config.yaml` and `splits.json`; otherwise `CheckpointOwnershipError` is raised before any claim file or corpus access (`evaluate.py:162-188`, claim happens later at `:225-262`). A harness arm directory must therefore never contain either file.
- **Graded-run / production load:** `TorchSaveCheckpointStore.load_checkpoint` uses `_is_structurally_valid`: required keys `model, optimizer, curriculum, rng, counters, config_identity, schema_version` and `schema_version == CHECKPOINT_SCHEMA_VERSION (2)` (`checkpoint.py:32-43, 170-200`); a harness payload with its own schema string and no `config_identity` is refused with `NoValidCheckpointError`. There is no `--init-from` in the trainer, so "a follow-on run that loads those weights is refused" holds structurally; the harness must not add one.
- **What to add:** tests that call `evaluate_run` and the production load/resume entry on the real files of the (d) fixture run (once with `first_omega_0` overridden) and assert the specific exception and that no `evaluation-attempt.json` appears; a writer invariant that arm directories contain no `config.yaml`/`splits.json`; a marker (`diagnostic: true`, schema `phase60-harness-run/v1`) in every record. Do not edit `pinn/evaluate.py` or `pinn/train.py` (no edit is needed, and `SurveyNonGatingTests` keeps training/evaluation free of verification imports).
- **`decision_verdict`** raises `ValueError` if any later-rung input is not `None` once `g2_fired` is true (`feasibility_scorecard.py:735-747`); on a stop pass `None` for all four, and `sweep_rescued=False`.
- **Scope guard:** INST-07 (Phase 61) later adds a generic "diagnostic-mode record" refusal to the graded-run path and the evaluator (`REQUIREMENTS.md` INST-07). Phase 60's INST-05(c) is satisfied by the structural refusals above plus tests; do not pre-empt INST-07's design by editing `pinn/evaluate.py` or `pinn/train.py`.

### K. Environment and gates that already exist

- Interpreter `<home>/miniforge3/envs/pinn-train/bin/python` (3.11.15); `python -B -m unittest tests.phaseNN.test_x -v`.
- **Prohibition suites on new `pinn/**/*.py` modules** (executable source with docstrings and comments stripped): `tests.phase38.test_prohibitions` forbids the tokens `set_default_dtype`, `is_available`, `add_argument("--precision", default=` and the v1.3 tokens `basic_architecture`, `data-processing-pipeline-full`, `data_processing_pipeline_full`, `data-handling`, `data_handling`; `tests.phase39.test_prohibitions` forbids corpus tokens (`brutus_hierarchical`, `brutus_standard`, `ic_hierarchical`, `ic_standard`, `glob/rglob(...*.txt)`) outside its four allowlisted readers (`pinn/data/adapter.py`, `fixture_loader.py`, `target_frame_probe.py`, `split_allowlist.py`, `test_prohibitions.py:49-54`). Consequences: harness code cannot probe MPS availability (hard-code `torch.device("mps")` from the protocol constants; an unavailable device fails at allocation), cannot name a corpus folder (use `split_allowlist`), and any `--precision` argument must be absent or required.
- **CORRECTION to the brief:** `tests.phase38.test_prohibitions` has 6 tests and two of them FAIL at HEAD for an unrelated reason: `test_spec_byte_identity_endpoint_sha256` (working-tree digest `f9a3aaf9...` vs the Phase 38 baseline `e629b2fc...`) and `test_spec_history_no_touch_since_phase_base` (the specs were legitimately amended in later phases) `[VERIFIED: ran 2026-10-18]`. The valid Phase 60 gate is the other four (`test_discovered_modules_superset_of_known_phase38`, `test_no_precision_default_in_discovered_modules`, `test_no_v1_3_era_imports_in_discovered_modules`, `test_write_spy_no_simulation_data_writes`). Report the two as pre-existing; do not fix them in this phase. `tests.phase39.test_prohibitions` passes (31 tests, 0.9 s).
- **Docstring marker trap:** `tests/phase59/test_static_guards.py` treats any `pinn/verification/*.py` whose first docstring line starts with "Phase 59" as a Phase 59 module (forbidden: `torch.optim`, `Optimizer`, trainer/evaluator imports, checkpoint saves; `_is_phase59_module`, :56-60, 74-79). Harness modules must begin "Phase 60 ...".
- **Green at HEAD (baseline for the scorer change)** `[VERIFIED: ran]`: `test_scorer_network` 9 tests 1.8 s; `test_scorer_known_errors` 11; `test_baselines` 4; `test_diag07` 27 tests 17 s; `test_diag07_panels` 16 tests 5 s; `test_two_kepler` 11; `test_nn_copy` 6; `test_scorecard_rules` 40; `test_static_guards` 15 tests 6.8 s.
- **Facts about the machine:** macOS 26.5.1 (build 25F80), model Mac17,9, 24 GiB RAM, 572 GiB free disk, MPS built and available, `caffeinate` present at `/usr/bin/caffeinate`, git 2.54.0 with `.githooks` configured `[VERIFIED: ran]`. CORRECTION: the network has 795,657 parameters, 3.04 MiB per float32 state, not about 730k and 2.8 MiB `[VERIFIED: built the network]`.

### L. Machine time, budgets, and storage

- Measured production throughput is 12.2-12.9 s/step for the 4096-row physics path on MPS float32 `[CITED: 57-05-SUMMARY.md:96]`. If the single-system physics step is comparable `[ASSUMED]`, a 3 h cap gives about 860 Adam steps (`I_warm = min(2000, floor(0.1*860)) = 86`), the extension about 1,720; each polish outer call may use up to `max_eval = max_iter*5//4 = 62` closure evaluations (about 13 minutes) `[VERIFIED: torch LBFGS source read]`, so the 25 percent cap (45 minutes at 3 h) allows about 3 outer calls. `polish_should_stop` is evaluated between outer calls, so the last call can overrun the cap by one call's duration. Data-only steps (1,001-point forward and backward) are expected to be tens of milliseconds, giving a budget in the 10^5 range `[ASSUMED]`; each cadence reading (gold-grid score, a few seconds) is negligible.
- CONTEXT's planning figures (about 30 h stop path, about 71 h continue path at 3.75 h per arm) stand. Arm counts: stop path 3 + 4 + 1 = 8 (7 with no confirmation); continue path 3 + 4 + 1 + 1 + 3 + 3 + 4 = 19; G2-passed path 3 + 3 + 3 + 4 = 13.
- **D-10 sizes, corrected for 795,657 parameters:** 3.04 MiB per state gives about 48.6 MiB (8 arms), 79.0 MiB (13 arms), 115.3 MiB (19 arms). Blobs are far below the 10 MiB per-file hook limit.

## Architecture Patterns

### System Architecture Diagram

```
 owner ruling file (D-11, only if continue)        run protocol (committed, SHA-pinned)
          |                                                  |
          v                                                  v
   arm catalog (closed ids) --> launcher (detached supervisor, caffeinate, one arm at a time)
          |                                  |  argv: arm id only, never a path
          v                                  v
   PREFLIGHT: protocol/scorecard/scorer SHAs, record keys readable+admitted+train, normalizer digest, free memory (advisory)
          |  any miss -> blocked arm, no fallback
          v
   allowlist reader (RecordKey only) --> load_reference(train record), load_reference(score record, gold)
          |                                         window t <= 10 ; real normalized IC13 ; masses ; inner pair
          v
   TIMING RUN (>=50 steps, discarded) --> B = steps_budget(3 h)
          |
          v
   ADAM LOOP  loss = trainer functions (data | IC+phys | +E,L), ScheduledWeights, cosine(B), [GradClipper?]
          |   readings 0, every floor(0.05 B), B  --> score_network(gold) --> trace ; physics arms: frozen monitor log
          |   at B: budget_outcome -> complete | extend (reset lr, new cosine, same Adam) | inconclusive(rate)
          |   non-finite -> divergence rule (OQ-6) ; SIGHUP/INT/TERM -> checkpoint, exit 129/130/143
          v
   score Adam state (MPS f32) + CPU f64 cross-check (tier/counts must match, else owner stop)
          v
   L-BFGS POLISH (full batch, strong Wolfe, max_iter 50, history 10; physics: frozen rows, w_n, lambdas, chunked)
          |   polish_should_stop between outer calls
          v
   score polish state + cross-check --> better_state --> counts(E_formula) (3 panel systems only)
          v
   record.json (exclusive create) + adam.weights + polish.weights --> git (plain), re-derive = re-score
          v
   G2: g2_fires(3 tiers) --> stop | sweep (60,120,240,480 data-only, then confirm) --> OwnerRouted (checkpoint 4) | G2 passed
```

### Recommended Project Structure

```
pinn/verification/
  learnability_arms.py        # ArmSpec, closed arm catalog and ids, omega provenance, override refusal, record keys
  learnability_data.py        # allowlist loading seam, windowing, normalizer digest check, ArmData (fixture-injectable)
  learnability_losses.py      # trainer-function composition (mutation target), chunked physics step, frozen monitor
  learnability_run.py         # budget driver, schedules, Adam, polish, scoring, cross-check, resume, signals, records
  learnability_g2.py          # pure rules: sweep pair, confirmation, uncovered system, skip writer, ruling loader
  diagnostic_architecture.py  # first_omega_0 override builder (does not touch ArchitectureSpec)
  gate04_train_free.py        # EDIT: optional first_omega_0 seam (default None = unchanged)
.planning/phases/60-single-system-learnability/
  60-RUN-PROTOCOL.md + evidence/run-protocol.json   # pre-registration, SHA-pinned
  evidence/scorer-successor.json                    # D-09 record
  evidence/preflight/records.json
  evidence/arms/<arm-id>/{record.json, adam.weights, polish.weights}
  evidence/g2/{g2-outcome.json, sweep-curve.json, skip-records.json}
  evidence/continue/{r_ref_omega.json, gate04-remeasure.json}
  60-CHECKPOINT-4-RULING.md                         # only if the owner answers
  evidence/verify_phase60_evidence.py               # records, g2, rescore, final
tests/phase60/  (new package; see Validation Architecture)
```
Path rules: no segment named `runs`, `tmp`, `outputs`, `scratch` under committed evidence (staged-path policy). Weights use a non-ignored extension (`.weights`): `*.pt`, `*.pth`, `*.npz`, `*.npy`, `*.ckpt`, `*.pkl` are git-ignored (`.gitignore:146-158`) and force-added ignored files are what the milestone-archive trap drops (memory). Resume checkpoints go under ignored `runs/phase60/<arm-id>/`.

### Pattern 1: Compose the trainer's functions; prove it against a real RunController
**What:** a thin loop that imports and calls the catalog and helper functions by bare name; a CPU float64 test builds a real `RunController` over the `tests/phase57/_fixtures` stub source and asserts per-term losses and `.grad` agree with `_run_adam_step_microbatched` (the Phase 59 JX-1 pattern, `diag07_common.per_term_gradients` mirrors the same method).
**When:** every physics arm; the data-only arm is the degenerate case.
**Source:** Finding H.

### Pattern 2: Closed arm catalog with refusal gates and a separate omega builder
**What:** arms are enumerated by a pure function (rung, system, record keys, loss arm, omega provenance in {locked, g2_sweep_override, confirmation_override, owner_approved}, LR stage, clip stage); free-form ids and paths are rejected. `first_omega_0` other than 30 is legal only for data-only arms with provenance `g2_sweep_override`/`confirmation_override`, or for any arm with provenance `owner_approved` whose value equals the value in the committed D-11 ruling file; a physics arm with an override is refused (INST-05(e)). The network for a non-30 omega comes from a builder that constructs `SQRSkipResNetSIREN(spec, dtype=, device=, generator=)` directly with a duck-typed spec copied from `ArchitectureSpec()` fields plus the overridden `first_omega_0`; `ArchitectureSpec` and `build_network` stay untouched. Same seed gives identical initial parameters at every omega because the first layer's init bound is `1/in_features` and independent of omega (`network.py:74-96`); a test asserts omega=30 through the builder is bitwise equal to `build_network(ArchitectureSpec(seed=42))`. This was run on CPU float64 and holds: omega=30 gives bitwise-identical parameters, omega=60 gives identical initial parameters with `input_layer.omega_0 == 60.0` and a different forward `[VERIFIED: ran this session]`.
**Source:** Findings D, J; `network.py:152-196`, `architecture_spec.py:119-124`.

### Pattern 3: Budget driver that only calls the frozen functions
**What:** a driver whose branches are exactly the return values of `steps_budget`, `scoring_cadence_ok`, `budget_outcome`, `polish_should_stop`, `better_state`, `tier_of`, `counts`; the extension is a second cosine from `LR_k` on the same optimizer (Finding B); `OwnerRouted` and the cross-check exception propagate. **Source:** Finding C.

### Pattern 4: Exclusive-create record, plain-git weights, re-derive by re-score
**What:** `record.json` is written with `evidence_io.write_json` (canonical, redacted, atomic) to a path that must not already exist (`O_EXCL` semantics: the first completed run is the result; a second invocation never replaces it), together with `adam.weights` and `polish.weights` (CPU float32 `OrderedDict`, `torch.save`, atomic). The record carries seed, runtime, torch/macOS/python/numpy versions (`platform.mac_ver()[0]`), `git_head` and a dirty-path list under `pinn/`, config hash, scorecard SHA-256, scorer SHA-256, protocol SHA-256, ruling-file SHA-256 when applicable, module digests (`evidence_io.module_hashes`), wall hours and seconds per step (timing run recorded separately), per-state weights digest (canonical: for each parameter in sorted-name order hash dtype, shape and bytes, as `controllers._tensor_hash` does per tensor), the files-opened attestation, the budget trail, the trace, `counts` and the formula field, and the `readout_notes` (D-04 low-rate-tail statement; D-05 from-scratch confound for probe 2b; D-08 reference applied unchanged). A validator rejects a record missing any required hash or version field (SPEC Req 4). **Source:** Findings F, G, L.

### Pattern 5: Detached supervisor, graceful stop, exact resume
**What:** Finding I. One arm at a time; the supervisor lives in its own session; exit codes 129/130/143 allow a governed resume; everything else goes to the owner.

### Pattern 6: G2 and sweep as pure functions
**What:** `sweep_plan(failing_ids)` sorts failing systems by the pinned inner-lap counts (1632: 10.47, 851: 18.61, 4658: 39.35) and returns (sweep system, confirmation system, uncovered system); `confirmed_omega(results)` returns the maximum `first_omega_0` whose arm result is Tier >= 1, or `None`. The four SPEC cases verified: failing {all three} or {1632, 851} -> sweep 1632, confirm 851, uncovered 4658; {1632, 4658} -> sweep 1632, confirm 4658, uncovered 851; {851, 4658} -> sweep 851, confirm 4658, uncovered 1632 `[VERIFIED: ran]`. A confirmed rescue calls `decision_verdict(g2_fired=True, sweep_rescued=True, ...)`, which raises `OwnerRouted("owner checkpoint 4")`; do not catch it. The skip writer accepts exactly the two reason strings `no rescue` and `checkpoint ④ answered go to the verdict` (circled digit U+2463; define both as module constants and test the exact bytes) and refuses once any Rung-2 arm has a state file; the handoff text for Level 3 is `not tested (skipped at G2)`, never "not reached".

### Pattern 7: Verifier extended with one successor digest
**What:** Finding F. Independent of Phase 60 code; reads one JSON record; pins one path and one predecessor/successor pair.

### Anti-Patterns to Avoid
- **Editing `ArchitectureSpec`, `feasibility_scorecard.py`, or any Phase 59 producer other than the scorer:** breaks pinned digests or violates SCOPE-43.
- **Using `AdmittedSetAdapter` or `_build_admitted_sources`:** they parse every file of every split, including the test split (`production_reference`/`split_allowlist` module docstrings; Phase 59 static guard forbids both names).
- **`lambda_data = 0` for Rung 2a:** raises in `LossWeights`.
- **Running the GATE-04 CLI with default paths for the D-07 re-measure:** overwrites the governed artifact.
- **Unchunked 4096-row backward or monitor on MPS:** the 22.8 GB failure mode.
- **Catching `OwnerRouted` or the cross-check exception to retry:** SPEC prohibition 6.
- **Restarting an arm after an unclean exit:** the first completed run is the result; an unrestorable arm goes to the owner.
- **Committing weights as `*.pt`:** ignored; force-adds are dropped by milestone archival.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Corpus path building, test-split refusal, open counting | A glob over `brutus_*` folders or your own reader | `split_allowlist.SplitAllowlist` + `AllowlistedCorpusReader` + `install_open_attestation` | Single choke point; refuses before any path exists; Phase 39 allowlist test forbids other readers |
| Reference trajectories and IC13 | Your own preprocessing | `production_reference.load_reference`, `recover_normalizer_from_checkpoint`, `resident_record` | Same chain the trainer sees; digest-checked normalizer |
| Tier, counting, budget, G2, polish stop, result state | Thresholds in harness code | The frozen functions in `feasibility_scorecard.py` | Pre-registered (SCOPE-42); frozen and hashed |
| Scoring | A second position-error or eps_H implementation | `feasibility_scorer.score_network` / `score_trajectory` | Known-error tested; same Hamiltonian as the gate |
| Loss terms and residuals | Re-typed Huber, IC, causal weights, force | `pinn.loss_catalog`, `pinn.physics_residual` | INST-05(a) |
| LR_k, warmup, optimizer constants | Literals `1e-3 * 0.7**k`, `min(2000, ...)` | `OptConfig`, `ScheduledWeights`, `PHYS05_*` constants | One home each |
| Second cosine | Manual lr arithmetic | Reset `initial_lr` then a fresh `CosineAnnealingLR` (verified) | Avoids the 0-forever and climb-back traps |
| Atomic writes, canonical JSON, redaction, module hashes | `open(..., "w")` | `atomic_io.atomic_write_torch/text`, `evidence_io.write_json`, `module_hashes` | Crash-safe; refuses home-directory and data-root text |
| RNG capture for exact continuation | `torch.manual_seed` | `determinism.capture_rng_state/restore_rng_state` | Four streams, weights_only-clean |
| Signals | Ad hoc handlers | `signals.SignalState` + `install_signal_handlers` (+ SIGHUP) | Debounce and escalation tested in `tests/phase41` |
| Detached launch | `nohup`/shell backgrounding | The generation-7 launcher pattern | Own session, retained log, recorded exit |
| L-BFGS and cosine | Custom optimizers | `torch.optim.LBFGS` (`strong_wolfe`), `CosineAnnealingLR` | The ratified recipe |

**Key insight:** the phase is composition and fail-closed plumbing. Every numerical definition already has a home; the risk is in the seams (omega lock, hash pins, memory shape, restart semantics), not in new math.

## Runtime State Inventory

Not a rename, rebrand or migration phase. The one in-place edit (the scorer) is an evidence-pinning change, inventoried here.

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| Stored data | 10 Phase 59 result JSONs embed the scorer digest `cd5019a2...870b` (`evidence/baselines/*.json` x3, `evidence/diag07/*.json` x7); `evidence/manifest.json` hashes the verifier and the three diag07 drivers | Successor record (D-09), verifier edit, manifest rewrite; do not re-run Phase 59 evidence |
| Live service config | None - no external service holds the string | None |
| OS-registered state | None - no launchd/cron entry; arms are launched per run | None |
| Secrets/env vars | `PYTORCH_ENABLE_MPS_FALLBACK` must be unset for MPS runs; `GSD_DATA_ROOT` optional corpus override | Record in protocol; capture before importing torch |
| Build artifacts / installed packages | `__pycache__` dirs (ignored); nothing installed | None |

## Common Pitfalls

### Pitfall 1: `ArchitectureSpec` rejects every omega except 30
**What goes wrong:** the G2 sweep, the confirmation, the uncovered Rung 1 and the whole D-07 re-measure cannot even build a network at another `first_omega_0`.
**Why:** `ArchitectureSpec.__post_init__` raises `ValueError("ArchitectureSpec.first_omega_0 must be 30.0 ...")` (`architecture_spec.py:119-124`); `build_network` requires an `ArchitectureSpec` instance (`network.py:~233-241`); `gate04_train_free._measure_raw_bin_means` goes through both.
**How to avoid:** the separate omega builder (Pattern 2) and the optional `first_omega_0` keyword in the GATE-04 helpers; never relax `ArchitectureSpec`.
**Warning signs:** `ValueError: ArchitectureSpec.first_omega_0 must be 30.0 (got 60.0)`.

### Pitfall 2: `network_trajectory` has three float64 widening sites
**What goes wrong:** fixing positions and velocities leaves the acceleration widening (`want_acceleration=True`, used by `score_network`) raising on MPS. **Avoid:** one helper at all three sites plus a static guard. **Warning:** `TypeError: Cannot convert a MPS Tensor to float64 dtype` only from `score_network`.

### Pitfall 3: D-09 as worded leaves Phase 59 red
**What goes wrong:** after the scorer edit and the `_check_result` change, `verify_phase59_evidence.py baselines` and `final` still fail on `baselines --check` (`BASELINES-CHECK-DIFF`) and on the manifest (`changed file verify_phase59_evidence.py`). **Avoid:** Finding F steps 2-3. **Warning:** `baselines re-derivation exited 1`.

### Pitfall 4: the "second cosine" silently does the wrong thing
**What goes wrong:** continuing the scheduler climbs back up; a fresh scheduler without resetting the learning rate stays at 0 forever (verified, Finding B). **Avoid:** reset `group["lr"] = group["initial_lr"]`, new `CosineAnnealingLR(optimizer, T_max=B)`, same optimizer; unit-test the rate trace.

### Pitfall 5: Rung 2a and `LossWeights`
**What goes wrong:** `LossWeights(lambda_data=0.0)` raises. **Avoid:** do not evaluate the data term; pass a zero tensor to `compose_total`.

### Pitfall 6: the 1,002nd gold snapshot
**What goes wrong:** training or scoring over all 1,002 gold snapshots includes t = 10.01 (> T), changes the point count from the pre-registered 1,001, and shifts the scorer's grid. **Avoid:** window every record with `times <= 10 + 1e-9`; assert the counts 1,001 (gold), 126 (hierarchical base), 59 (standard base).

### Pitfall 7: weights and evidence paths that git or the hooks drop
**What goes wrong:** `*.pt`/`*.npz`/`*.npy` are ignored and `runs/*`, `*/tmp/*`, `*/outputs/*` are blocked at commit; force-added ignored files are what milestone archival silently drops (memory). **Avoid:** `.weights` under `.planning/phases/60-.../evidence/arms/<arm-id>/`; after any phase archive run, compare `git ls-files` with `find` counts. **Warning:** `git policy: generated or scratch artifact is staged`.

### Pitfall 8: memory spike from an unchunked physics evaluation
**What goes wrong:** the frozen monitor or the L-BFGS closure over 4096 rows built every term's graph at once, 1.5 -> 22.8 GB on MPS (`controllers.py:1724-1732`). **Avoid:** 256-row chunks everywhere (monitor pass-1, Adam pass-2, polish closure). The footprint reader is unreliable on this macOS; the 6 GiB owner confirmation is the real gate.

### Pitfall 9: the GATE-04 CLI overwrites the governed `R_ref`
See Finding D. Use a separate Phase 60 entry and an explicit Phase 60 output path; assert the governed file's SHA-256 is unchanged after a re-measure.

### Pitfall 10: Phase 59 helpers with Phase 59 defaults
`runtime_gate` fails any step over 600 s; `begin_long_step` defaults to Phase 59's evidence tree; `require_frozen_scorecard` is wired to the Phase 59 freeze. Pass `evidence_root=` or write Phase 60 equivalents; never edit `evidence_io.py`.

### Pitfall 11: prohibition suites and the docstring marker
A harness module that mentions `is_available`, names a corpus folder, or defaults `--precision`, or whose docstring starts "Phase 59", will fail `tests.phase38/39.test_prohibitions` or be pulled into the Phase 59 scan (Finding K). Run both suites after every new module.

### Pitfall 12: timing-run contamination and warm-up inflation
**What goes wrong:** seconds per step sets `B` (`steps_budget`), so a concurrent job, a thermal dip, or MPS first-step compilation inside a 50-step timing run shrinks the experiment. For a fast data-only step the warm-up could dominate. **Avoid:** pre-register the timing-run length and what it includes (OQ-9); no other heavy job during timing; record the timing run separately. **Warning:** a data-only budget far below ~10^5 steps.

### Pitfall 13: process-global open attestation
`install_open_attestation` installs a permanent audit hook and raises if installed again for a different data root (`split_allowlist.py:366-371`). One data root per process; tests use one fixture root per process.

### Pitfall 14: polish defaults and resume
`OptConfig.lbfgs_max_iter` is 20 (`config.py:669`) but the frozen polish is 50 (`feasibility_scorecard_v1.json:403`): read the scorecard. A polish outer call can overrun the 25 percent cap. A fresh `LBFGS` on resume drops curvature history unless its state is saved.

### Pitfall 15: treating the two Phase 38 failures as regressions
They exist at HEAD (Finding K). Gate on the four relevant tests and say so in the plan.

### Pitfall 16: stepping on a non-finite gradient
The trainer checks the clip outcome (`clip_outcome.non_finite`) and the loss before `optimizer.step()` (`controllers.py:2131-2162`). Do the same; otherwise parameters become NaN and the last finite state is lost. What to record and score afterwards is OQ-6.

### Pitfall 17: reusing one arm's budget for another
D-02 sizes the cosine from "that arm's timing-run seconds per step". Every sweep arm, the confirmation and each probe arm has its own timing run.

## Code Examples

Sketches built from the verified sources named in each header. They are not drop-in files.

### MPS-safe widening at all three sites
```python
# Source: pinn/verification/feasibility_scorer.py:417,420,425 (current) and
# jx02_jx05.py:56-60 (_cpu64, the Phase 59 reference copy)
def _to_cpu_float64(tensor):
    """MPS has no float64: move to the CPU first, then widen (GAP-59-13)."""
    return tensor.detach().to("cpu").to(torch.float64)

position_chunks.append(_to_cpu_float64(positions).numpy().reshape(-1, 3, 3))
velocity_chunks.append(_to_cpu_float64(velocities).numpy().reshape(-1, 3, 3))
acceleration_chunks.append(_to_cpu_float64(second).numpy().reshape(-1, 3, 3))
```

### D-03 second cosine (verified: second trace equals the first, max difference 0.0)
```python
# Source: ran on torch 2.12.1; CosineAnnealingLR.get_lr read from the installed source
def start_second_cosine(optimizer, budget: int):
    for group in optimizer.param_groups:
        group["lr"] = group["initial_lr"]        # set by the first scheduler's setdefault
    return torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=budget)
```

### Budget driver using only the frozen functions
```python
# Source: feasibility_scorecard.py:779-865 signatures
B = steps_budget(3.0, timing_wall_seconds, timing_steps, scorecard=sc)
interval = max(1, int(0.05 * B))                      # gaps never exceed 0.05*B
reading_steps = sorted(set(list(range(0, B, interval)) + [B]))
assert scoring_cadence_ok(reading_steps, B, scorecard=sc)
# ... train to B, scoring (step, E) at each reading step ...
outcome = budget_outcome(readings, B, extended=False, scorecard=sc)
if outcome["outcome"] == "extend":
    B2 = int(outcome["new_budget_steps"])
    scheduler = start_second_cosine(optimizer, B)
    # ... train steps B..B2, readings keep the same interval ...
    outcome = budget_outcome(readings, B2, extended=True, scorecard=sc)   # may raise OwnerRouted
```

### INST-05(a) mutation test (INST-04 SC3 pattern)
```python
# Source: tests/phase55/test_architecture_characterization.py:283-320
original = harness_losses.data_huber_loss
def doubled(*args, **kwargs):
    return original(*args, **kwargs) * 2.0
base = harness_losses.data_only_loss(fixture_arm)
with mock.patch.object(harness_losses, "data_huber_loss", side_effect=doubled):
    mutated = harness_losses.data_only_loss(fixture_arm)
self.assertAlmostEqual(float(mutated) / float(base), 2.0, places=12)
# repeat for ic_anchor_loss, causal_physics_loss (scale details["w_n"]), softened_acceleration,
# componentwise_du, soft_energy_loss, angular_momentum_loss, accumulate_chunked_data_term
```

### Omega override builder (production `ArchitectureSpec` untouched)
```python
# Source: network.py:152-196 (constructor reads only spec attributes), architecture_spec.py:119-124
from dataclasses import asdict
from types import SimpleNamespace

def build_network_with_first_omega(first_omega_0: float, *, seed: int, dtype, device):
    fields = asdict(ArchitectureSpec(seed=seed))          # validated locked defaults
    fields["first_omega_0"] = float(first_omega_0)        # the only difference
    generator = torch.Generator(device=device)
    generator.manual_seed(int(seed))
    return SQRSkipResNetSIREN(SimpleNamespace(**fields), dtype=dtype, device=device, generator=generator)
```

### Override refusal (INST-05(e)) and sweep rule (verified against the SPEC's four cases)
```python
GRID = (60.0, 120.0, 240.0, 480.0)
LAPS = {1632: 10.47, 851: 18.61, 4658: 39.35}

def check_omega(spec, ruling=None):
    if spec.first_omega_0 == 30.0 and spec.omega_provenance == "locked":
        return
    if spec.omega_provenance in ("g2_sweep_override", "confirmation_override"):
        if spec.loss_arm != "data_only" or spec.first_omega_0 not in GRID:
            raise OverrideRefused("an override is legal only on a data-only sweep arm at a grid value")
        return
    if spec.omega_provenance == "owner_approved" and ruling is not None \
            and spec.first_omega_0 == ruling.approved_first_omega_0:
        return
    raise OverrideRefused("first_omega_0 not authorized for this arm")

def sweep_plan(failing_ids):                      # at least two failing systems
    order = sorted(failing_ids, key=lambda i: LAPS[i])
    sweep, confirm = order[0], order[1]
    uncovered = [i for i in LAPS if i not in (sweep, confirm)][0]
    return sweep, confirm, uncovered

def confirmed_omega(tier_by_omega):               # all four grid values already run
    ok = [w for w, tier in tier_by_omega.items() if tier >= 1]
    return max(ok) if ok else None
```

### Verifier: exactly one successor digest
```python
# Source: verify_phase59_evidence.py:434-440 (current loop)
for relative, digest in producers.items():
    current = sha256_file(repo_path(str(relative), what=str(relative)))
    if current == digest:
        continue
    record = _scorer_successor()          # committed, tracked, clean; None if absent
    if (record is not None and relative == record["path"]
            and digest == record["predecessor_sha256"] and current == record["successor_sha256"]):
        continue
    fail(f"{path.name} producer_sha256 does not match {relative}")
```

### Amendment containment (strict, whitespace only)
```python
import unicodedata
def collapse(text): return " ".join(unicodedata.normalize("NFC", text).split())
for label, body, section_text in amendment_paragraphs_from_spec():     # body parsed from 60-SPEC.md,
    self.assertIn(collapse(body), collapse(section_text), label)       # section_text = its designated section only
self.assertEqual(hashlib.sha256(scorecard_path.read_bytes()).hexdigest(), SCORECARD_SHA256)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Phase 38 probe: constant lr 1e-3, zero IC13, `torch.optim.Adam`, ratio gate (`overfit_probe.py:52-53, 139-146`) | Harness: real normalized IC13, trainer cosine and warmup, polish, physics-unit scoring | Phase 60 | The first evidence of learnability in physical units |
| Generation 7: physics term on one trajectory per step (single anchor) | One system makes every slot the same trajectory; no anchor defect | Roadmap statement for Phase 60 | Phase 60 needs no conformance work |
| Unchunked 4096-row monitor and L-BFGS closure | 256-row chunks | GAP-57-05 (2026-09-16) | Harness must chunk the monitor and the polish closure |
| Scorer evaluated only on CPU float64 in tests | MPS float32 official scores with CPU float64 cross-check | Phase 60 (GAP-59-13) | Fix before any network is scored |

**Deprecated or stale:** `tests.phase38.test_prohibitions` spec byte-identity checks (stale since later spec phases); v1.3-era `pinn/basic_architecture.py` and `data-processing-pipeline-full.py` (banned tokens).

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `torch.optim.LBFGS` with `strong_wolfe` runs correctly on MPS float32 for this network and a 1,001-point or chunked 4096-row closure. No repository test or committed run exercises it on MPS (the production runs were Adam-only). | Findings H, I | Polish fails or misbehaves; mitigated by a Wave-0 tiny MPS smoke before any real arm. SPEC fixes MPS float32 for the polish, so a failure goes to the owner. |
| A2 | Data-only step time is tens of milliseconds, so a 3 h cap gives a budget near 10^5 steps. | Finding L | Plan time estimates and the timing-run design (OQ-9) shift; no correctness effect. |
| A3 | The single-system physics step costs about the production 12.2-12.9 s/step (4096 rows), giving about 860 Adam steps per 3 h. | Finding L | Physics-arm hours and warmup length differ; the frozen rule sets the real budget. |
| A4 | The D-07 re-measure (six cases, two passes, CPU float64) takes minutes, not seconds. | Finding D | Task must run detached; harmless if faster. |
| A5 | The normalized-copy method for `baselines --check` reproduces committed bytes exactly after an old-to-new digest substitution. Not executed (it requires a changed scorer). | Finding F | A residual byte difference would fail `final`; fallback is a documented skip of baselines re-derivation only (OQ-1 option B). |
| A6 | `torch.func.jacrev` works under an outer `torch.no_grad()` on MPS, so the frozen-monitor pass needs no parameter graph. The Phase 59 scorer already runs `jacrev` without a backward call, and the trainer's pass-1 detaches `rbar`. | Finding H | Memory higher than planned; the monitor stays chunked either way. |
| A7 | Probe arms use the Stage-0-recovered IC13 normalizer unchanged (consistent with D-08's reasoning about R_ref). | OQ-8 | Probe inputs differ from a hypothetical full-curriculum normalizer; non-gating. |
| A8 | The optimizer-level choices in OQ-3 (clipper), OQ-4 (polish improvement and state), OQ-6 (divergence) are resolvable under the 2026-10-07/09 delegation. | Open Questions | If the owner considers any of them a recipe change, they escalate. |
| A9 | The protocol should fix timing-run length 500 steps for data-only arms and the 50-step minimum for physics arms. | OQ-9 | Smaller or larger budgets than intended; pre-registration makes it explicit. |
| A10 | Gold, base and standard record counts and the within-T windows are stable (the corpus is frozen). | Finding G | Preflight catches any change. |

## Open Questions (owner/planner) (RESOLVED)

All twelve were resolved on 2026-10-18 under the v2.4 delegation; each item below names the `60-GAPS.md` entry that holds its resolution.

Each item is NOT grounded in the SPEC, CONTEXT, ratified specs or code. Per the v2.4 delegation rule each is to be recorded in `60-GAPS.md` and `.planning/milestones/v2.4-GAPS.md` with the STOP fields, and resolved under the delegation unless it moves a locked value, spends the evaluation or pre-empts the verdict (then it goes to the owner). The recommendation is advice, not a decision.

1. **OQ-1: D-09 completeness (operational coordination).** RESOLVED: GAP-60-02.
   - Known: the verifier edit alone leaves `baselines --check` and the manifest red (Finding F).
   - Options: (A) normalized-copy re-derivation, keeping all other digests checked; (B) skip the baselines re-derivation inside `final` with a documented exception; (C) edit `baselines.py` (a second successor, contradicts D-09's "exactly one").
   - Recommendation: A, plus the manifest rewrite and a detached `final` run. Route: planner under delegation; mention in the closeout.

2. **OQ-2: D-07/D-08 on a continue path (semantic).** RESOLVED: GAP-60-10.
   - Known: D-08 says probes "reuse the committed Stage-0 `R_ref`"; the committed value is the omega=30 measurement; the ratified invalidation list names `first_omega_0`; D-07 re-measures before "any physics arm" at the approved omega. `gate04_train_free` cannot take an omega (Finding D).
   - Options: (i) probes on a continue use the committed omega=30 value (literal D-08; applies an invalidated reference); (ii) "the Stage-0 R_ref in force" = committed at omega=30, the D-07 re-measured value after a continue.
   - Recommendation: (ii), recorded in each probe record ("Stage-0 reference in force, applied unchanged", with the artifact path and SHA-256). Also add the omega seam to the GATE-04 helpers and write the re-measure to a Phase 60 path. Route: planner under delegation; state it in the checkpoint ④ question text.

3. **OQ-3: gradient clipping in harness arms (semantic).** RESOLVED: GAP-60-03.
   - Known: the trainer clips every Adam step with `GradClipper` (`controllers.py:2092`); table `{0: 8.5, 1: 8.5, 2: 5.0, 3: 5.0, 4: 3.0, 5: 3.0, 6: 3.0}` and median floor 1e-6, all marked provisional (`grad_clip.py:89-97`). D-01 lists the schedule constants but not clipping; the Phase 38 probe did not clip.
   - Options: (A) clip every Adam step in every arm with the trainer's `GradClipper` at the arm's stage (0 for data-only and Stage-0 arms, 4 and 6 for probe 2b); (B) clip physics arms only; (C) no clipping anywhere.
   - Recommendation: A (SCOPE-41: the ladder measures the ratified recipe; D-04's logic that data-only arms share the Rung 2 schedule applies equally here); checkpoint the clipper state. Route: planner under delegation; owner told because it affects Rung 1.

4. **OQ-4: polish semantics (semantic).** RESOLVED: GAP-60-05.
   - Known: the scorecard stops "after 5 outer calls without improvement" or at 25 percent of Adam wall time; it does not define improvement, the polish state, or which wall time counts (`feasibility_scorecard_v1.json:398-409`, `polish_should_stop`).
   - Options for improvement: (A) the full-batch objective the closure returns, strictly below the best so far (the Adam-final objective is the baseline); (B) the scored `E` after each outer call. Polish state: final iterate (recommended, literal) vs best iterate. Adam wall: all-inclusive monotonic time of the Adam phase summed across segments, excluding interruptions (recommended) vs step time only.
   - Recommendation: A; final iterate; all-inclusive wall; log `E` at each outer call for data-only arms. Pre-register in the protocol. Route: planner under delegation.

5. **OQ-5: what a failed confirmation means (semantic; could pre-empt the verdict).** RESOLVED: GAP-60-09.
   - Known: SPEC Req 6 says the confirmation is the highest Tier >= 1 setting and "a confirmed rescue raises the frozen `OwnerRouted`"; it never says what happens if the confirmation run is below Tier 1. `decision_verdict` raises only for `sweep_rescued=True`.
   - Options: (A) failed confirmation = no rescue -> RETHINK-REPRESENTATION; (B) any Tier >= 1 sweep result = rescue; (C) stop and route to the owner as an off-script result (SCOPE-42, Owner Checkpoint ③).
   - Recommendation: pre-register C. It neither declares RETHINK nor a rescue by itself. Route: owner if it ever occurs; the protocol rule can be committed under delegation because it decides nothing.

6. **OQ-6: divergence rule (semantic).** RESOLVED: GAP-60-06.
   - Known: the trainer checks finiteness before `optimizer.step()` and returns RECOVER (`controllers.py:2131-2160`); the harness has no recovery; SPEC says a silent restart is not a result.
   - Options: (A) stop Adam at the last finite state, score it as the Adam state, still run the polish if the weights are finite, and let `better_state` choose; (B) mark the arm Tier 0 without scoring; (C) stop for the owner.
   - Recommendation: A, recorded with `diverged_at_step`; no restart. Route: planner under delegation.

7. **OQ-7: energy-term scale for probe Rung 2b (semantic).** RESOLVED: GAP-60-12.
   - Known: `eps_H = 1e-4 * S_H`, `S_H = median_train(K0 + Uabs0)` over the training split (`pinn_architecture.md:567-575`); the only recorded value is the Stage-0 run's `s_h = 22.321729071058996`, `eps_h = 0.0022321729071058997` (`runs/stage0-v23g7-seed42/training_metadata.json` `[VERIFIED: read]`). Probe 2b at k=4 and k=6 has `lambda_E = lambda_L = 1`, so the term is active.
   - Options: reuse the Stage-0 `S_H` (recommended, parallel to D-08); recompute over a larger split (a new number with no ratified owner).
   - Recommendation: reuse, record it as applied unchanged. Route: planner under delegation; non-gating arm.

8. **OQ-8: probe IC13 normalizer (semantic, low).** RESOLVED: GAP-60-13. Reuse the Stage-0-recovered stats for all arms, including standard-variant probes (consistent with D-08; IC13 normalization is on the `R_ref` invalidation list, so changing it would force a re-measure). Route: planner; record the stats digest in every record.

9. **OQ-9: timing-run definition (process-artifact).** RESOLVED: GAP-60-04.
   - Known: at least 50 steps, discarded weights (CONTEXT); seconds per step is `wall/steps` of the whole run (`steps_budget`).
   - Choices to fix before the first arm: step count (recommend 500 for data-only arms so MPS first-step compilation is amortized, 50 for physics arms), what is timed (all steps, warm-up included; no exclusions), a throwaway RNG so the arm's seed-42 stream starts fresh, and no concurrent heavy jobs. Route: planner, in the run protocol.

10. **OQ-10: weights file format and hash (operational).** RESOLVED: GAP-60-08. `.weights` extension (not ignored), `torch.save` of a CPU float32 `OrderedDict`, canonical per-tensor digest in the record plus the file SHA-256. Route: planner.

11. **OQ-11: cross-check scope (operational).** RESOLVED: GAP-60-07. Cross-check both scored states of every real arm; stop on any tier or counts-boolean difference with a dedicated owner-routed exception. Route: planner.

12. **OQ-12: an approved omega outside the swept grid (low).** RESOLVED: GAP-60-11. The ruling file may name any positive finite value. Recommend accepting it, recording whether it equals the confirmed omega and whether it is in the grid, and running D-07 at that value. Route: planner.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `pinn-train` Python env | everything | yes | 3.11.15 | none |
| torch with MPS | arms, scorer MPS test | yes (`mps built True, available True`) | 2.12.1 | none: SPEC fixes MPS float32; CPU float64 is the cross-check only |
| numpy | scoring arithmetic | yes | 2.4.6 | none |
| `/usr/bin/caffeinate` | detached arms | yes | system | none; keep the machine awake and on AC |
| git and project hooks | commits | yes | 2.54.0, `core.hooksPath=.githooks` | none |
| Corpus (main checkout, read through the allowlist) | preflight, all arms | yes: 10 assigned records read and admitted | frozen | a missing or unreadable record blocks that arm; no substitute (SPEC Req 8) |
| Retained `stage-0-init.pt`, generation-7 `splits.json`, retention manifest | normalizer recovery, allowlist | yes (tracked under `runs/stage0-v23g7-seed42/`) | step 0 | the fallback normalizer is a recorded deviation; do not use silently |
| 6 GiB free memory | long arms | not at research time: `available_memory_bytes()` = 4.63 GiB | - | owner closes browsers (CONTEXT); advisory only |
| pytest, scipy, safetensors | - | no | - | not needed; use unittest |
| Disk | weights, resume checkpoints | yes, 572 GiB free | - | - |

**Missing dependencies with no fallback:** none for planning. **Blocking at launch time:** the owner's memory confirmation before each long arm.
**Missing dependencies with fallback:** none.

## Validation Architecture

`workflow.nyquist_validation` is `true` in `.planning/config.json`, so this section applies.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | `unittest` (stdlib); `pytest` is not installed |
| Config file | none; new package `tests/phase60/` (create `__init__.py` in the first plan that adds a test) |
| Quick run command | `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest tests.phase60.<module> -v` |
| Full suite command | `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase60 -t . -v` |

### Phase Requirements -> Test Map
| Req / Decision | Behavior | Test type | Automated command | Failure signal | Fixture or real | Cost |
|---|---|---|---|---|---|---|
| SPEC R1 | Six amendment paragraphs each contained in their designated section after whitespace collapse; scorecard SHA unchanged | unit | `...tests.phase60.test_amendment` | label of the missing paragraph; SHA mismatch | docs only | under 2 s |
| INST-05(a) | Harness output moves by the scale when each trainer function is mutated; function objects identical to the trainer's; per-term loss and `.grad` equal to `RunController._run_adam_step_microbatched` | unit | `...test_losses_trainer_functions` | ratio is not the scale; gradient mismatch | stub source, CPU float64 | about 5-20 s |
| INST-05(b) | Test-split key refused before any path; no raw-path input; attestation shows zero test opens | unit | `...test_arm_spec`, `...test_data_seam` | no `SplitRefused`; opens counted | tiny corpus fixture (`tests/phase59/_corpus_fixtures.py`) | under 5 s |
| INST-05(c) | `evaluate_run` and the production checkpoint load refuse harness artifacts, including an override record; no `evaluation-attempt.json` appears | integration | `...test_refusals` | wrong or no exception; attempt file exists | artifacts of the (d) run | about 10 s |
| INST-05(d) | Short run through the polish with both states scored, record valid, exclusive create, not a Rung-1 result | integration | `...test_run_short` | missing state, invalid record, overwrite allowed | real network, CPU float64, tiny fixture, temp evidence root | 10-40 s `[ASSUMED]` |
| INST-05(e) | Override refused on a physics arm; legal only on data-only grid arms or with the ruling value | unit | `...test_arm_spec` | no `OverrideRefused` | none | under 1 s |
| SPEC R3 | `network_trajectory` runs on MPS float32 and is unchanged on CPU float64; no one-call widen remains | unit | `...test_scorer_mps`, `tests.phase59.test_scorer_network`, `tests.phase59.test_diag07_panels.NetworkScoreTests` | `TypeError` on MPS; field mismatch | tiny network, MPS | under 10 s |
| D-09 | Verifier accepts exactly one successor digest for one path; other mismatches, a second successor, an untracked record still fail | unit | `...test_verifier_successor` | wrong accept or reject | synthetic repo (reuse `tests/phase59/test_evidence_verifier.py` fixtures) | about 70 s (sibling suite timing) |
| D-09 end to end | Phase 59 evidence verifies at HEAD after the scorer edit | e2e | `python .planning/phases/59-.../evidence/verify_phase59_evidence.py final` | non-zero exit or no `PHASE59-EVIDENCE-OK` | real | 644 s, run detached with retained output |
| D-01..D-05 | LR_k values, cosine length B, warmup length, no re-ramp past B, second cosine equals first, data-only k=0, probe LR_4 and LR_6 | unit | `...test_schedule` | trace mismatch | CPU | under 5 s |
| SPEC R4, R5 | Budget driver: B from the timing run, cadence, extend/complete/inconclusive, `OwnerRouted` propagation, tier boundaries (E = 0.1 is Tier 1; non-finite E is Tier 0; non-finite eps_H caps at Tier 1) | unit | `...test_budget_driver` | | fakes, no training | under 5 s |
| SPEC R6 | Four pair cases; confirmation is the highest Tier >= 1; none -> no confirmation; all four settings before the confirmation; rescue raises and is not caught | unit | `...test_g2` | | none | under 1 s |
| SPEC R7 | Skip writer accepts only the two exact reasons, refuses once a Rung-2 arm has a state file; probes never call `counts()`; `decision_verdict` not called with later inputs on a stop | unit | `...test_g2` | | none | under 1 s |
| SPEC R8 | Preflight blocks missing, empty, unreadable records with no fallback; resume keeps B, sums Adam time, refuses a missing segment state or changed module digest | unit | `...test_preflight`, `...test_resume` | | tiny corpus fixture; tiny CPU network | 5-30 s |
| D-06 | Physics arm never halts; monitor evaluated in chunks of at most 256 rows at readings only | unit | `...test_losses_trainer_functions` | | CPU | few s |
| D-07 | Omega seam: default path leaves the committed artifact and results unchanged; re-measure writes only to a Phase 60 path and never `terminal-state.json`; BLOCK stops | unit | `...test_gate04_remeasure` | governed file digest changed | small case set, CPU float64 | seam test cheap; the real re-measure is minutes `[ASSUMED]` |
| D-08, D-11 | Probe record states the reference in force; ruling loader accepts only a tracked, clean file with a strict machine block and a finite positive value; the quote is opaque | unit | `...test_protocol_records` | | fixtures | under 1 s |
| D-10, SPEC R4 | Weights use a non-ignored extension, digest recorded, record rejects any missing hash or version field; re-score of committed weights equals the recorded tier and E | unit, then real | `...test_protocol_records`; verifier `rescore` | | real weights | each state about 10-60 s `[ASSUMED]` |
| Static | Docstring marker, `torch.load(weights_only=True)`, no evaluator or trainer import, no corpus token, no `is_available`, no catch of `OwnerRouted` | unit | `...test_static_guards`, `tests.phase39.test_prohibitions`, four named tests of `tests.phase38.test_prohibitions` | | static | under 10 s |
| Real arms | Per arm: record complete, attestation zeros, seed 42, protocol SHA matches, scorer SHA matches, `g2_fires` reproduces the recorded outcome | verifier | `verify_phase60_evidence.py records`, `g2`, `rescore`, `final` | | real | minutes; arms themselves take hours |

### Sampling Rate
- **Per task commit:** the module's quick command (seconds). When a `pinn/` module changes, also `tests.phase39.test_prohibitions` (0.9 s).
- **Per wave merge:** the full `tests/phase60` suite, the scorer-dependent Phase 59 suites (about 35 s together: `test_scorer_network`, `test_scorer_known_errors`, `test_baselines`, `test_diag07`, `test_diag07_panels`, `test_two_kepler`, `test_nn_copy`, `test_scorecard_rules`, `test_static_guards`), and the four relevant `tests.phase38.test_prohibitions` tests.
- **Phase gate:** Phase 60 evidence verifier `final`, Phase 59 `final` (detached, 644 s, retained output), both prohibition suites.
- **Expensive (over 60 s) and therefore run once, detached, with full retained output and reused while inputs are unchanged:** Phase 59 `final`, `tests.phase59.test_evidence_verifier` (about 70 s), `baselines --check` (about 66 s), the D-07 re-measure, every real arm, every `rescore`.

### Wave 0 Gaps
- [ ] `tests/phase60/__init__.py` and the test modules named above.
- [ ] Reusable fixtures: tiny corpus (`tests/phase59/_corpus_fixtures.py::tiny_split_fixture`), stub `RunController` (`tests/phase57/_fixtures.py::build_run_controller`), rigid orbits (`tests/phase59/_fixtures.py::lagrange_rotation`).
- [ ] An MPS smoke for `torch.optim.LBFGS` (strong Wolfe) before any real arm (Assumption A1).
- [ ] No framework install needed.
- [ ] A fixture-vs-real marker in every record so a fixture run can never be mistaken for a Rung result.

## Security / Threat Notes

Security enforcement is on (config key absent). ASVS Level 1; items marked HIGH block the first real-arm launch until their tests pass.

### Applicable ASVS Categories
| ASVS Category | Applies | Standard control |
|---------------|---------|-----------------|
| V2 Authentication | no | - |
| V3 Session Management | no | - |
| V4 Access Control | yes (owner authorization of a non-locked omega, test-split access) | committed D-11 ruling file; allowlist `require`; closed arm catalog |
| V5 Input Validation | yes (ruling file text, arm ids, record schemas) | strict parsers; closed enums; size and type checks |
| V6 Cryptography | hashing only | `hashlib` SHA-256 (never hand-rolled) |
| V8 Data Protection | yes (home and data-root text in evidence) | `evidence_io.guard_redaction`, `reject_evidence_root` |
| V12 Files and Resources | yes (paths, atomic writes, deserialization) | `atomic_io`, `torch.load(weights_only=True)`, containment checks |
| V14 Configuration | yes (frozen scorecard, pinned digests) | `load_scorecard` SHA, single scorer successor |

### Known Threat Patterns
| Pattern | STRIDE | Severity | Standard mitigation |
|---------|--------|----------|---------------------|
| A test-split file is opened by a harness arm or its preflight (SCOPE-40, single preserved evaluation) | Information disclosure | HIGH | `SplitAllowlist.require` before any path; audit-hook attestation; arms take `RecordKey` only; records embed attestation zeros; verifier asserts them |
| Unsafe deserialization of a resume checkpoint or weights (`torch.load` of a pickle) | Tampering, Elevation | HIGH | literal `weights_only=True`; payloads are tensors and plain containers; static test |
| A harness record or weights accepted by `pinn.evaluate` or a production resume, or used to initialize a run | Spoofing, Tampering | HIGH | structural refusal (no `config.yaml`/`splits.json`; own schema string); tests on real artifacts incl. an override record; no init-from option; diagnostic marker |
| Prompt-injection or malformed text in the owner message copied into the D-11 ruling file | Tampering | MEDIUM | parse only a strict machine block (answer, finite positive `approved_first_omega_0`); quote stored as opaque text fenced with a fresh random delimiter per the untrusted-input boundary; never executed, formatted into paths, or evaluated; file must be tracked and clean; its SHA-256 is cited by every continue-path record |
| Evidence path injection or traversal through arm ids or a ruling-file field | Tampering | MEDIUM | closed catalog of ids; containment and symlink refusal as in the verifier's `repo_path`; deep path review is owned by `/gsd-secure-phase` and is not minted here |
| Home-directory or data-root text in committed evidence | Information disclosure | MEDIUM | `guard_redaction`; launch metadata (contains `cwd`) kept untracked |
| Silent second run, other seed, or restart replaces a result | Repudiation, Tampering | MEDIUM | exclusive-create records; module digests in checkpoints; refuse resume on drift; verifier requires one record per arm id with seed 42 |
| Scorecard or scorer drift | Tampering | MEDIUM | `load_scorecard` SHA; single scorer successor; `scorecard-frozen` check |
| Memory exhaustion on the owner's machine (22.8 GB failure mode) | Denial of service | MEDIUM | 256-row chunking; one arm at a time; owner confirmation; advisory preflight |
| Shell injection in the launcher | Tampering | LOW | argv lists, no `shell=True`; arm id from a closed enum |
| Package supply chain | Tampering | LOW | none installed |

## Recommended Plan and Wave Decomposition

Principles: tracer first (one thin end-to-end slice), independent small fixes in parallel with it, protocol committed before any real arm, long arms as non-autonomous detached plans, result-dependent work as gated branch plans that open with a fail-closed precondition task. Files of parallel plans must be disjoint. `tests/phase60/__init__.py` is created by 60-01; the repository has no `tests/__init__.py`, and a subpackage without `__init__.py` still imports as a namespace package `[VERIFIED: ran in a scratch directory]`, so parallel Wave-1 plans do not block on it.

| Plan | Wave | Autonomous | Depends on | Covers | Core content and files |
|------|------|------------|-----------|--------|------------------------|
| 60-01 Tracer: one data-only arm end to end on a fixture | 1 | yes | - | INST-05 (b)(d)(e) subset; SPEC R2 core | `learnability_arms.py`, `learnability_data.py`, minimal `learnability_run.py`, `diagnostic_architecture.py`, `tests/phase60/{__init__,test_arm_spec,test_data_seam,test_run_short,test_static_guards}.py`. Slice: closed arm id -> allowlisted record (fixture reader) -> real normalized IC13 -> cosine Adam -> polish -> both states scored -> exclusive-create record -> refused by the evaluator. Also fixes weights format and record schema. |
| 60-02 Scorer MPS fix and successor record | 1 | yes (short MPS test) | - | SPEC R3, D-09 part 1 | `pinn/verification/feasibility_scorer.py`, `tests/phase60/test_scorer_mps.py`, `evidence/scorer-successor.json` |
| 60-03 Amendment text and frozen-scorecard check | 1 | yes | - | SPEC R1 | `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `tests/phase60/test_amendment.py` |
| 60-04 Phase 59 verifier successor, baselines re-derivation, manifest | 2 | yes (launches a detached 644 s run) | 60-02 | D-09 | `verify_phase59_evidence.py`, `evidence/manifest.json`, `tests/phase60/test_verifier_successor.py` |
| 60-05 Physics arms and trainer-function proofs | 2 | yes | 60-01 | INST-05(a); D-06; D-08 reference selection | `learnability_losses.py`, `tests/phase60/{test_losses_trainer_functions,test_schedule}.py`; chunked physics step, frozen monitor, ScheduledWeights, polish closure |
| 60-06 GATE-04 omega seam and re-measure entry | 2 | yes | 60-01 | D-07 | `pinn/verification/gate04_train_free.py` (optional `first_omega_0` keyword, default `None` = unchanged), new `pinn/verification/gate04_omega_remeasure.py` (kept separate from `learnability_g2.py` so 60-06 and 60-08 own disjoint files), `tests/phase60/test_gate04_remeasure.py` |
| 60-07 Run control: timing, budget driver, extension, resume, signals, launcher, preflight | 3 | yes | 60-01, 60-05 | SPEC R4, R8; D-02, D-03 | `learnability_run.py`, launcher script, `tests/phase60/{test_budget_driver,test_resume,test_preflight,test_refusals}.py` |
| 60-08 G2 rules, skip writer, ruling loader, Phase 60 evidence verifier | 3 | yes | 60-01 | SPEC R5-R7; D-11 | `learnability_g2.py`, `evidence/verify_phase60_evidence.py`, `tests/phase60/{test_g2,test_protocol_records}.py` |
| 60-09 Run protocol, preflight evidence, pre-registration commit | 4 | yes (informs the owner) | 60-02..60-08 | SPEC R4, R8 | `60-RUN-PROTOCOL.md`, `evidence/run-protocol.json`, `evidence/preflight/records.json`, `60-GAPS.md` and `v2.4-GAPS.md` entries for OQ-1..OQ-12. Nothing real runs before this commit. |
| 60-10 Rung 1 on 1632, 851, 4658 | 5 | no (owner memory prompt, hours, detached) | 60-09 | FEAS-03, SPEC R5 | three arm launches, supervised, one at a time; records and weights committed per arm. Suggested order 1632, 851, 4658 (the pinned inner-lap order the sweep rule uses); the order is the planner's per CONTEXT. |
| 60-11 G2 evaluation and branch decision | 5 | yes | 60-10 | FEAS-03, SPEC R5 | `g2_fires` on the three recorded tiers; writes the outcome; selects exactly one branch |
| 60-12 STOP branch (no rescue or go to the verdict) | 6 | yes | 60-11 | FEAS-04, FEAS-09, SPEC R7, R8 | skip records with an exact reason, machine hours, Phase 64 handoff ("not tested (skipped at G2)"), mark Phases 61-63 skipped not failed |
| 60-13 SWEEP branch (G2 fired) | 6 | no (hours; ends at checkpoint ④) | 60-11 | FEAS-03, SPEC R6 | four data-only arms in grid order, confirmation, sweep curve; on a confirmed rescue the frozen `OwnerRouted` and a blocking human checkpoint; nothing of Rung 2 runs or is skipped while unanswered |
| 60-14 G2-PASSED branch | 6 | no (hours) | 60-11 | FEAS-04, FEAS-09 | Rung 2a and 2b on three systems and four probe arms at omega 30 |
| 60-15 CONTINUE branch (owner answered continue) | 7 | no (hours, owner prompts) | 60-13 plus the ruling | FEAS-04, FEAS-09, D-07, D-11 | ruling file, R_ref re-measure and GATE-04 at the approved omega (stop on BLOCK), uncovered-system Rung 1, Rung 2, probes |
| 60-16 Closeout | 8 | yes | the executed branch | all | summary, machine hours per arm, verification, requirement traceability, final Phase 59 and Phase 60 verifiers, gap register |

Branch discipline: plans 60-12 to 60-15 are mutually exclusive; each opens with a precondition task that reads the recorded G2 outcome and refuses to continue unless it matches; a skip is written only after the owner's "go to the verdict" or a no-rescue sweep, and never once any Rung-2 arm has a state file. The planner may instead leave 60-12..60-15 to a re-plan after Rung 1 (ROADMAP says planning of later phases may start while runs execute).

Execution shape for each long arm plan: (1) precondition task, (2) human-verify task: owner closes browsers, confirms 6 GiB free and no other heavy job, (3) launch task (detached, returns immediately; the executor must not hold a session for hours), (4) completion check in a later session (the cross-session watchdog skill under `.claude/skills/cross-session-watchdog` can wake a session when an arm ends), (5) verify and commit the record, weights and manifest, (6) update the gap register. Use `agent-commit` with explicit owned paths, scope `60-NN`.

Decision coverage for the planner: D-01, D-02, D-04, D-05 -> 60-05, 60-07 (schedule tests); D-03 -> 60-07; D-06 -> 60-05; D-07 -> 60-06, 60-15; D-08 -> 60-05, 60-15; D-09 -> 60-02, 60-04; D-10 -> 60-01 (format), arm plans; D-11 -> 60-08, 60-15. SPEC: R1 -> 60-03; R2 -> 60-01, 60-05; R3 -> 60-02; R4 -> 60-07, 60-09; R5 -> 60-10, 60-11; R6 -> 60-13; R7 -> 60-12, 60-14, 60-15; R8 -> 60-07, 60-09, 60-12, 60-15.

Non-autonomous flags: 60-10, 60-13, 60-14, 60-15 (owner memory prompt, hours of detached compute), the checkpoint ④ task inside 60-13 (blocking human decision), and any task that launches the Phase 59 `final` while an arm could run.

## Sources

### Primary (HIGH confidence): read in full or executed this session
- `.planning/phases/60-single-system-learnability/60-SPEC.md`, `60-CONTEXT.md`, `60-DISCUSSION-LOG.md`; `.planning/REQUIREMENTS.md`; `.planning/ROADMAP.md` (Phase 60 section, delegation rule); `.planning/STATE.md` (head, Phase 59 decisions); `.planning/milestones/v2.4-GAPS.md`.
- `pinn/verification/feasibility_scorecard.py`, `feasibility_scorer.py`, `artifacts/feasibility_scorecard_v1.json`, `split_allowlist.py`, `production_reference.py`, `overfit_probe.py`, `baselines.py`, `evidence_io.py`, `gate04_train_free.py`, `candidate_eligibility.py`, `two_kepler.py`, `artifacts/r_ref_stage0.json`.
- `pinn/loss_catalog.py`, `physics_residual.py`, `network.py`, `architecture_spec.py`, `constants.py`, `runtime.py`, `evaluate.py`, `data/batches.py`, `training/controllers.py`, `scheduled_weights.py`, `config.py`, `grad_clip.py`, `signals.py`, `determinism.py`, `checkpoint.py`, `atomic_io.py`.
- `.planning/phases/59-read-only-baseline-scorecard/` (`59-SCORECARD.md`, `59-GAPS.md` GAP-59-13, `evidence/verify_phase59_evidence.py`, `scorecard-freeze.json`, `manifest.json`, `diag07/{diag07_common,jx02_jx05}.py`, `baselines/*.json`, `audit/reader_acceptance.json`), `.planning/phases/57-.../57-RULING.md`, `57-05-SUMMARY.md`, `evidence/launch_phase57_run.py`.
- `tests/phase38/test_prohibitions.py`, `tests/phase39/test_prohibitions.py`, `tests/phase55/test_architecture_characterization.py`, `tests/phase57/_fixtures.py`, `tests/phase59/{test_static_guards,test_scorer_network,test_diag07_panels,_fixtures,_corpus_fixtures}.py`; `scripts/git_policy/validate_staged_paths.py`; `.gitignore`.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` (lines 1803, 1805, 1894-1912, 1999), `pinn_architecture.md` (lines 181, 454, 567-575, 699-704).
- Executed read-only: environment versions, parameter count, `ArchitectureSpec(first_omega_0=60.0)` failure, ten-record preflight, base/gold IC13 equality, amendment containment script, scheduler restart experiment, sweep-rule script, Phase 38/39/59 test timings, memory sample.
- Context7 `/websites/pytorch_2_12`: `CosineAnnealingLR` (no periodic restart), `CosineAnnealingWarmRestarts`, `Tensor.to` (https://docs.pytorch.org/docs/2.12/generated/torch.optim.lr_scheduler.CosineAnnealingLR.html).

### Secondary (MEDIUM)
- `scripts/run_precision_probe.py:120-126` (MPS fallback convention), `STATE.md` timing figures for the Phase 59 verifier and baselines.

### Tertiary (LOW)
- Per-step timing estimates for data-only arms and the harness physics step (Assumptions A2, A3); MPS L-BFGS behavior (A1).

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH, nothing new is installed and every module was read or executed.
- Architecture and reuse points: HIGH, with the omega seam, chunked polish closure and cross-check design verified against the code.
- Hazards: HIGH for the eight newly found items; each was reproduced or read at a line.
- Protocol choices (OQ-3, 4, 6, 7, 9): MEDIUM, unresolved by any source and routed.
- Runtime behavior on MPS (L-BFGS, timing): LOW until the Wave-0 smoke and the timing runs.

**Research date:** 2026-10-18
**Valid until:** 2026-11-17 for repository facts (the repo moves with each commit; re-check line numbers after any edit to the cited files); the PyTorch statements hold for torch 2.12.1.
