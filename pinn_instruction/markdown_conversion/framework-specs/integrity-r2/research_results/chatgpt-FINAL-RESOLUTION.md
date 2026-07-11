Project-source inventory received: `ctl_instruction.md`, `pinn_architecture.md`, `sampling_method.md`, `v2.0-build-plan.md`, `trainex-r1a-resolution-doc.md`, `RATIFICATION.md`, `DATASET-CONTEXT.md`; instruction prompt received: `RESEARCH-AGENT-PROMPT-STORM(1).md`.

# Part 1 — Verdict

**NO-GO — blocked on IR2-001, IR2-002, and IR2-003.** The foundation is mostly coherent, but the v2.0 build plan currently contradicts the locked loss contract, misstates the batch-construction contract, and leaves a validation/test leakage risk for base/gold duplicate physical systems.

# Part 2 — Pre-build punch-list

**PB-1. Decide how Phase 38 will implement the locked five-term loss before any training code is written.**
Option A: Change Phase 38 NET-04 to the full locked loss: Huber data + IC + causal physics + energy + angular momentum — aligns the build with the specs.
Option B: Keep Phase 38 as a three-term smoke-only probe, but explicitly prohibit using it as the training objective and require Phase 40 to add the missing terms before any real run — faster skeleton, higher drift risk.
Source problems: IR2-001.
Recommended: **A** — the build plan says Phase 38 is “rebuilt from specs,” so the spec-faithful loss should be present from the start.

**PB-2. Decide the authoritative v2.0 batch-construction wording before implementing the DataLoader.**
Option A: Replace Phase 39 DATA-05 with the `ctl_instruction.md` contract: 240 replay trajectories + 16 lookahead trajectories; data-fidelity snapshot points are capped per trajectory; collocation points are a separate continuous set; 50/50 acceleration-weighted sampling applies only to data-fidelity points.
Option B: Intentionally revise the science spec to make lookahead a collocation-only mechanism — requires a spec-unfreeze and new rationale.
Source problems: IR2-002.
Recommended: **A** — this is a direct build-plan transcription error, not a science choice.

**PB-3. Decide the split unit: `physical_key`, not `record_key`, unless the owner explicitly waives leakage risk.**
Option A: Split by `physical_key = (variant, id)` first, then place all base/gold realizations of that physical system in the same train/val/test split — avoids duplicate-IC leakage.
Option B: Split by `record_key` and report validation/test results as potentially optimistic — easier but weakens the acceptance gate.
Source problems: IR2-003.
Recommended: **A** — the dataset contains base/gold realizations of the same ICs, so split grouping is necessary for credible held-out metrics.

**PB-4. Decide which dataset inventory is authoritative in implementation: `DATASET-CONTEXT.md` must override the stale table in `ctl_instruction.md`.**
Option A: Patch/spec-note the `ctl_instruction.md` dataset table before build code uses set names or counts.
Option B: Leave the spec unchanged but add an explicit build rule that all variant counts and base/gold roles come from `DATASET-CONTEXT.md`.
Source problems: IR2-004, IR2-006.
Recommended: **A** — the locked science spec should not carry a wrong base/gold inventory into a build milestone.

# Part 3 — Proven problems

## IR2-001

**What's wrong** — The v2.0 model-build phase specifies a three-term L1/MAE loss, but the locked science specs require a five-term objective with Huber data loss plus energy and angular-momentum regularizers.

**Where** — `v2.0-build-plan.md`, Phase 38 NET-04; `pinn_architecture.md`, Sections 3.1–3.5 and 4.1; `ctl_instruction.md`, Loss Function Formulation.

**The proof** — The build plan says Phase 38 must implement “the three-term data+physics+IC loss” and later states “The three-term loss (data L1/MAE + physics + IC) evaluates…” . The locked architecture spec instead states the default objective is
`L_total = L_data + λ_IC L_IC + λ_phys L_phys^causal + λ_E L_E + λ_L L_L`, and Section 3.1 says the data fidelity term “uses a Huber contract on scaled projected positions,” not L1/MAE . The CTL training-loop spec repeats the same five loss terms: data, IC, causal physics, energy, and angular momentum .
**derived-math:** The build-plan loss set is `{data-L1/MAE, physics, IC}`. The locked-spec loss set is `{Huber data, IC, causal physics, energy, angular momentum}`. The symmetric difference is `{data loss form mismatch, energy missing, angular momentum missing}`. That is not an implementation detail; it changes the optimized objective.

**How serious** — Serious.

**Which file it points at** — the build plan.

**Stops the build?** — must-fix-first.

**Suggested fix** — Suggest changing Phase 38 NET-04 to: “the PHYS-05 five-term loss catalog: Huber data loss, IC anchor, causal physics residual, soft energy regularizer, and angular-momentum regularizer, with scheduled weights as defined in `pinn_architecture.md` and assembled by `ctl_instruction.md`.”

## IR2-002

**What's wrong** — The v2.0 data-ingestion phase misstates the replay/lookahead and collocation contract by treating 16 lookahead trajectories as the collocation set and applying 50/50 acceleration-weighted sampling to both point sets.

**Where** — `v2.0-build-plan.md`, Phase 39 DATA-05; `ctl_instruction.md`, Phase 2a Mini-Batch Construction.

**The proof** — The build plan says the batch constructor emits “data-fidelity (240 replay, 8192 pts) vs collocation (16 lookahead with the `has_stage(k+1)` guard, 4096 pts) — with 50/50 uniform + acceleration-weighted time sampling on both” . The CTL spec says the 240/16 numbers are trajectory counts: “Replay set `B_replay = 240` trajectories” and “Look-ahead set `B_lookahead = 16` trajectories” . It then defines two logically independent point sets: data-fidelity points from BRUTUS snapshots and collocation points from continuous samples; it states that 50/50 mixed sampling is retained for data-fidelity points, while “Collocation points — 50/50 deferred” and “Phase 34 does not mandate it” .
**derived-math:** Under the spec, a stage-k batch has up to `(240 + 16) × 32 = 8192` data-fidelity snapshot points, plus an independently configured collocation budget. Under the build-plan wording, the 16 lookahead trajectories are reinterpreted as a collocation bucket. That changes both the role of lookahead and the sampling distribution.

**How serious** — Serious.

**Which file it points at** — the build plan.

**Stops the build?** — must-fix-first.

**Suggested fix** — Suggest rewriting DATA-05 so that replay/lookahead selects trajectories, while data-fidelity and collocation are separate point sets; apply acceleration-weighted 50/50 only to the data-fidelity snapshot sampler unless a later spec explicitly commissions mixed continuous collocation.

## IR2-003

**What's wrong** — The split plan does not state that train/validation/test splits must be grouped by `physical_key`, creating a proven risk that base and gold realizations of the same physical system leak across splits.

**Where** — `v2.0-build-plan.md`, Phase 39 DATA-04; `DATASET-CONTEXT.md`, Dataset identity and variants; `ctl_instruction.md`, Step 1 ID resolution.

**The proof** — The dataset context states hierarchical gold trajectories are “Gold (high temporal resolution) reruns of the same hierarchical ICs,” and standard gold trajectories are “Gold reruns of a subset of the standard ICs” . The CTL spec defines both `record_key = (variant, fidelity, id)` and `physical_key = (variant, id)` . The v2.0 build plan only requires “a deterministic, stage-stratified split manifest (~80/10/10)” and says nothing about grouping all records under the same `physical_key` into the same split .
**derived-math:** If a splitter operates over `record_key`s, then `(hierarchical, base, 0123)` and `(hierarchical, gold, 0123)` are distinct records and can be assigned to different splits even though they share the same physical IC. Because the gold trajectory is a rerun of the same IC, this can put the same physical problem in train and validation/test, making held-out metrics optimistic.

**How serious** — Serious.

**Which file it points at** — the build plan / data.

**Stops the build?** — must-fix-first.

**Suggested fix** — Suggest adding a split invariant: first partition by `physical_key`, then expand to all associated `record_key`s; assert no `physical_key` appears in more than one split.

## IR2-004

**What's wrong** — `ctl_instruction.md`’s dataset table assigns the 4,857 and 2,749 counts to the wrong base/gold roles relative to the verified dataset facts.

**Where** — `ctl_instruction.md`, Existing Training Dataset; `DATASET-CONTEXT.md`, Dataset identity and variants.

**The proof** — The CTL table says Set 1b Standard has 4,857 files and Set 2a Hierarchical has 2,749 files . The verified dataset context says the live folders are: hierarchical base 4,857, hierarchical gold 4,857, standard base 2,749, standard gold 2,565 .
**derived-math:** The count attached to “standard base” in CTL is 4,857, but the verified standard base count is 2,749. The count attached to “hierarchical gold” in CTL is 2,749, but the verified hierarchical gold count is 4,857. These cannot both be true, and `DATASET-CONTEXT.md` is fixed Tier-1 empirical evidence under the audit prompt .

**How serious** — Serious.

**Which file it points at** — a spec / the data.

**Stops the build?** — handle-with-a-condition.

**Suggested fix** — Suggest correcting the CTL dataset table and all Set 1a/1b/2a/2b references so they map to the four verified folders in `DATASET-CONTEXT.md`; until then, require build code to ignore the stale table and use folder scans plus `DATASET-CONTEXT.md`.

## IR2-005

**What's wrong** — The `L_norm` code snippet silently floors the characteristic angular-momentum denominator even though the surrounding contract requires raw un-clipped storage and diagnostic flags for degenerate cases.

**Where** — `ctl_instruction.md`, Step 3: Necessary Calculations of Invariants.

**The proof** — The mathematical definition states `v_char = sqrt(2|E| / M_total)`, `L_max = M_total r_char v_char`, and `L_norm = L / L_max` . The same section says that when `L_max` is nonfinite or near-degenerate, the recorded `L_norm` “MUST carry a diagnostic flag rather than being silently clamped or stored as `inf` / `nan`,” and that no global clamp is authorized . The immediately following code instead computes `v_char = np.sqrt(2 * np.abs(E) / M_total + eps)` and returns `L / (L_max + eps)` .
**derived-math:** Adding `eps` inside `sqrt` changes the definition of `v_char` when `|E|` is small, exactly the Stage-6 regime the contract says must be diagnosed. Adding `eps` to `L_max` in the denominator converts an undefined or near-degenerate diagnostic into a finite number. That contradicts the stated guard semantics.

**How serious** — Minor.

**Which file it points at** — a spec.

**Suggested fix** — Suggest replacing the snippet with a version that implements the formula exactly, then branches: if `L_max` is nonfinite or below a named numerical floor, store a diagnostic flag and do not manufacture a finite `L_norm`.

## IR2-006

**What's wrong** — The CTL admission gate still describes the 70 DATA-05 hierarchical base files as quarantined, but the verified dataset context says the remediation is complete and all quarantines are lifted.

**Where** — `ctl_instruction.md`, Step 1A — Trajectory Admission Gate; `DATASET-CONTEXT.md`, Mass-consistency remediation.

**The proof** — CTL Step 1A states: “The 70 `brutus_hierarchical` base outputs flagged by DATA-05 … are quarantined from training, metrics, and PIPE-07 use until rerun validation from the current canonical ICs passes” . The dataset context states that remediation was executed and validated; the current state is “0 mismatches across all 15,028 pairs” and “All quarantines are lifted” .
**derived-math:** If an implementer treats the CTL sentence as active configuration, then 70 valid current files are excluded. If an implementer treats `DATASET-CONTEXT.md` as fixed empirical truth, they are included. The two states are mutually exclusive.

**How serious** — Minor.

**Which file it points at** — a spec / the data.

**Suggested fix** — Suggest changing the CTL clause from an active quarantine to a historical note: the quarantine list is empty in the verified baseline unless a future validation run reopens it.

# Part 4 — Spec check-everything table

## `ctl_instruction.md`

| Line | Level | Heading                                                          | Verdict                                                                                 |
| ---: | ----- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
|    9 | H1    | Important Note                                                   | audited-clean                                                                           |
|   17 | H1    | Characterizing and Organizing the Multi-Fidelity Simulation Data | see problem IR2-004                                                                     |
|   19 | H2    | Existing Training Dataset                                        | see problem IR2-004                                                                     |
|   44 | H2    | Multi-Fidelity Dataset and Physical Invariants                   | audited-clean, except dataset-role inheritance from IR2-004                             |
|  107 | H2    | Multi-Stage Data Stratification by Difficulty                    | see problems IR2-004, IR2-005                                                           |
|  336 | H1    | A Glimpse at the Data                                            | audited-clean                                                                           |
|  408 | H1    | Phase 1 - Data Preparation and Stratification                    | see problem IR2-006                                                                     |
|  414 | H2    | Step 1: Parse Raw Simulation Data                                | audited-clean                                                                           |
|  526 | H2    | Step 1A — Trajectory Admission Gate                              | see problem IR2-006                                                                     |
|  772 | H2    | Step 2: Unified Preprocessing Pipeline                           | audited-clean                                                                           |
| 1097 | H2    | Step 3: Necessary Calculations of Invariants                     | see problem IR2-005                                                                     |
| 1444 | H2    | Step 4: Formulating the Input Vector                             | audited-clean                                                                           |
| 1580 | H2    | Step 5: Curriculum Stage Assignment                              | see problem IR2-004; missing-gold status noted but not a defect                         |
| 1647 | H1    | Phase 2 - The Definitive CTL-PINN Training Loop                  | audited-clean, except build-plan drift in IR2-001/IR2-002                               |
| 1677 | H2    | Overview: The Two-Phase Optimization Strategy                    | audited-clean                                                                           |
| 1722 | H2    | Loss Function Formulation                                        | audited-clean; build-plan contradicts it in IR2-001                                     |
| 1768 | H2    | Phase 2a: Adam-driven Exploration                                | audited-clean; build-plan contradicts batch semantics in IR2-002                        |
| 1877 | H2    | Phase 2b: High-Precision L-BFGS Refinement                       | audited-clean                                                                           |
| 1902 | H2    | Stage Transition Criteria                                        | audited-clean; numeric thresholds are owner-carved/provisional                          |
| 1979 | H2    | Consolidated Hyperparameter Schedule                             | audited-clean                                                                           |
| 1992 | H2    | Implementation Notes                                             | audited-clean; Hydra ambiguity already recorded in ratified decisions, not a new defect |
| 2021 | H1    | Advanced Considerations and Best Practices                       | audited-clean                                                                           |
| 2023 | H2    | Evaluation Metrics and Validation                                | audited-clean as conceptual guidance; Lyapunov final estimator remains owner-pending    |
| 2097 | H1    | Reproducibility Note                                             | audited-clean as non-operative note                                                     |
| 2130 | H1    | Supplementary Figures                                            | audited-clean                                                                           |
| 2136 | H1    | Source Issues / Notes for Future Reconciliation                  | audited-clean                                                                           |
| 2140 | H2    | SI-CTL-001                                                       | audited-clean; resolved by locked IC13 contract                                         |

## `pinn_architecture.md`

| Line | Level | Heading                                         | Verdict                                                                         |
| ---: | ----- | ----------------------------------------------- | ------------------------------------------------------------------------------- |
|    6 | H1    | A Definitive Implementation Blueprint…          | audited-clean                                                                   |
|    8 | H1    | 1. Foundational Architectural Principles        | audited-clean                                                                   |
|  105 | H1    | 2. SQR-SkipResNet-SIREN Backbone                | audited-clean                                                                   |
|  113 | H2    | 2.1 Sinusoidal Activation                       | audited-clean                                                                   |
|  149 | H2    | 2.2 SIREN Initialization                        | audited-clean                                                                   |
|  190 | H2    | 2.3 SQR-SkipResNet Formulation                  | audited-clean                                                                   |
|  248 | H2    | 2.4 Finalized Architectural Hyperparameters     | audited-clean                                                                   |
|  268 | H1    | 3. Multi-Component Loss Function                | audited-clean; build-plan contradicts it in IR2-001                             |
|  292 | H2    | 3.1 Data Fidelity Term                          | audited-clean; build-plan contradicts Huber with L1/MAE in IR2-001              |
|  362 | H2    | 3.2 Physics Residual Term                       | audited-clean                                                                   |
|  473 | H2    | 3.3 Initial Condition Anchor Loss               | audited-clean                                                                   |
|  497 | H2    | 3.4 Soft Energy Conservation Regularizer        | audited-clean; missing from build-plan NET-04 in IR2-001                        |
|  611 | H2    | 3.5 Angular Momentum Conservation Loss          | audited-clean; missing from build-plan NET-04 in IR2-001                        |
|  627 | H1    | 4. Advanced Training and Optimization Strategy  | audited-clean                                                                   |
|  633 | H2    | 4.1 Loss Balancing via Warmup Schedule          | audited-clean                                                                   |
|  684 | H2    | 4.2 Optional ALM Ablation                       | audited-clean                                                                   |
|  707 | H2    | 4.3 Two-Phase Optimization                      | audited-clean                                                                   |
|  724 | H2    | 4.4 Adaptive Gradient Clipping                  | audited-clean                                                                   |
|  774 | H1    | 5. Inference and Trajectory Generation          | audited-clean                                                                   |
|  779 | H2    | 5.1 Generating a Trajectory                     | audited-clean                                                                   |
|  801 | H2    | 5.2 Output Layer and Kinematic Consistency      | audited-clean                                                                   |
|  847 | H2    | 5.3 Output Frame and File Format                | audited-clean                                                                   |
|  994 | H2    | References                                      | audited-clean for project use; external citations checked only where used below |
| 1014 | H1    | 10. Numerical Acceptance Checks                 | audited-clean; fp32/MPS achievability remains a side-list test                  |
| 1043 | H2    | Source Issues / Notes for Future Reconciliation | audited-clean                                                                   |

## `sampling_method.md`

| Line | Level | Heading                                      | Verdict       |
| ---: | ----- | -------------------------------------------- | ------------- |
|    1 | H1    | Unified Pipeline for Generating ICs          | audited-clean |
|    5 | H2    | Overview of the Data Generation Pipeline     | audited-clean |
|   20 | H2    | Stage 1: Hierarchical IC Generation          | audited-clean |
|   83 | H2    | Stage 2: Enhanced Quasi-Random Sampling      | audited-clean |
|   86 | H2    | 1. Core Sampling Methodology                 | audited-clean |
|  168 | H2    | 2. Enhancements to Sampling Algorithm        | audited-clean |
|  200 | H2    | Stage 3: Pre-Screening                       | audited-clean |
|  203 | H2    | 3. Pre-Screening Rationale                   | audited-clean |
|  224 | H2    | 4. Pre-Screening Criteria                    | audited-clean |
|  246 | H2    | 5. Coordinated Strategy for Minimum Distance | audited-clean |
|  264 | H2    | 6. Execution and Final Quality Control       | audited-clean |
|  279 | H2    | Source Issues / Notes                        | audited-clean |

# Part 5 — Numbers cross-check

|  # | Shared element                           | `ctl_instruction.md`                                                                       | `pinn_architecture.md`                                                                      | `sampling_method.md`                                      | Match verdict                                                         |
| -: | ---------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- | --------------------------------------------------------- | --------------------------------------------------------------------- |
|  1 | Network input `[τ, IC₁₃]`                | Exactly `[τ, IC13]`                                                                        | Exactly 14D `[τ, IC13]`                                                                     | absent                                                    | Match between CTL/PINN                                                |
|  2 | `τ = 2u − 1`, `u=t/T`                    | stated                                                                                     | stated with AD leaf `u`                                                                     | absent                                                    | Match                                                                 |
|  3 | IC₁₃ slot order/raw mass                 | slots listed; raw ordered masses before normalization                                      | same slots; normalized after preprocessing                                                  | masses normalized to sum 3 in generation for ICs          | Match for model; sampling is historical data-gen                      |
|  4 | Trajectory horizon `T`                   | `T=t_max=10`                                                                               | `T=t_max` implied; output examples use interval                                             | Brutus/pre-screening uses t_max/t_end conventions         | Match at framework level                                              |
|  5 | `G` convention                           | `G=1`, raw masses                                                                          | non-dimensional `G=1`                                                                       | generation formulas assume gravitational units            | Match                                                                 |
|  6 | Characteristic length `D`                | `D=(G*T^2)^(1/3)≈4.6416`; mass-fraction rejected                                           | same in summary/acceptance checks                                                           | distinguishes sampling-time scale from preprocessing `D`  | Match                                                                 |
|  7 | Input normalization                      | tanh per slot; energy tanh(E/E_scale)                                                      | same formula in Network Input Contract                                                      | absent                                                    | Match                                                                 |
|  8 | Output head & COM projection             | training data flow points to 9D output + COM projection                                    | 9D position output + hard mass-weighted COM projection                                      | absent                                                    | Match                                                                 |
|  9 | Softening `ε_train` / validation `ε_inv` | `epsilon_train=1e-5`, `epsilon_inv=1e-10` distinct                                         | same dual-epsilon separation                                                                | sampling collision threshold is separate                  | Match                                                                 |
| 10 | Energy-drift screening gate              | Step 1A rejects if SCS > −5 / eps_H > 1e-5                                                 | acceptance checks include force-energy consistency; training epsilon_H is denominator floor | absent                                                    | Match with glyph distinction                                          |
| 11 | Hidden architecture                      | cross-ref to PINN spec                                                                     | 12×256 SIREN, first ω0=30, hidden ω0=1, LayerNorm false, p=2                                | absent                                                    | Match                                                                 |
| 12 | Loss inventory                           | five-term total loss                                                                       | five-term total loss + Huber data                                                           | absent                                                    | Match between specs; v2 contradicts in IR2-001                        |
| 13 | Energy denominator floor                 | `epsilon_H=1e-4*S_H` for model energy criterion                                            | same in §3.4                                                                                | absent                                                    | Match                                                                 |
| 14 | Batch construction                       | 240 replay trajectories, 16 lookahead trajectories, per-traj cap 32; collocation separate  | points back to CTL as canonical                                                             | absent                                                    | Match between specs; v2 contradicts in IR2-002                        |
| 15 | Curriculum stage count                   | stages 0–6, no Stage 7+                                                                    | references CTL                                                                              | absent                                                    | Match                                                                 |
| 16 | Adam → L-BFGS boundary                   | plateau handoff; full batch early, sL-BFGS later                                           | two-phase optimization, no clip during L-BFGS                                               | absent                                                    | Match                                                                 |
| 17 | Per-variant `dt_out` / tolerance         | CTL table has stale count/role mapping; footer defaults mostly match                       | absent                                                                                      | data generation background                                | **Mismatch vs DATASET-CONTEXT: see IR2-004**                          |
| 18 | Output frame & file format               | COM/gauge-scaled training references                                                       | COM frame; CSV position output example                                                      | absent                                                    | Mostly match; inverse-to-raw export is not specified but not blocking |

# Part 6 — Build-plan problem-hunt

I examined `v2.0-build-plan.md` Phases 37–43, `trainex-r1a-resolution-doc.md` D1–D7 / B-1–B-11, `RATIFICATION.md`, and the first-run recipe for defects that would invalidate results, block the build, force a spec-unfreeze, or derail later phases. The instruction file explicitly required full spec coverage, problem-hunt depth for build decisions, and exclusion of owner-carved placeholders from the problem list .

## Found build-plan problems

| Area              | Finding                                                                |
| ----------------- | ---------------------------------------------------------------------- |
| Phase 38 NET-04   | Wrong loss contract: see IR2-001.                                      |
| Phase 39 DATA-05  | Wrong batch-construction semantics: see IR2-002.                       |
| Phase 39 DATA-04  | Split manifest lacks physical-key grouping: see IR2-003.               |
| Dataset grounding | CTL dataset inventory conflicts with fixed dataset facts: see IR2-004. |

## Checked this, found nothing register

| Phase / decision            | What was checked                                                      | Why it is sound enough                                                                                                           |
| --------------------------- | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Phase 37 / D1-p             | Precision is left to the dual-arm probe, not decided in text.         | This matches RATIFICATION carve-outs; not a defect .                                                                             |
| Phase 38 architecture       | 14→256×12→9, SIREN ω0, LayerNorm, COM head.                           | Matches `pinn_architecture.md` architecture summary; only the loss wording is wrong .                                            |
| Phase 39 admission/loading  | Step-1A, NaN/Inf, `data_version_hash`, metadata exposure.             | Consistent with CTL loader/admission contracts and trainex D3; `data_version_hash` production remains known-open, not a defect . |
| Phase 40 loop               | Adam→L-BFGS, scheduled weights, clipping, ADVANCE/RECOVER/HALT.       | Matches ratified decisions and CTL transition model; thresholds are owner-carved placeholders .                                  |
| Phase 41 checkpoints/resume | Dual-trigger, atomic writes, anchors, resume diff, RNG state.         | Matches ratified D4/D6/D7 decisions; B-5 field list is deliberately owner-deferred .                                             |
| Phase 42 operator surface   | `caffeinate -is`, JSONL canonical, TensorBoard secondary, run folder. | Matches RATIFICATION summary and trainex D2/B10 choices .                                                                        |
| Phase 43 verification       | Verify ladder, smoke test, seed band, owner threshold calibration.    | Matches v2.0 verification protocol and known carve-outs; no invented thresholds .                                                |
| Trainex D1–D7 / B-1–B-11    | Checked for direct contradiction with locked specs.                   | No new defect beyond v2.0 transcription problems; owner-carved items correctly remain open .                                     |
| First-run recipe            | Checked composition of setup → verify → configure → launch → resume.  | Coherent, provided PB-1/PB-2/PB-3 are fixed first.                                                                               |

# Part 7 — Side-list: empirical doubts and their tests

**SL-1 — MPS second-order AD may be unsupported, inaccurate, or too slow for the actual model.**
Why paper cannot settle it: PyTorch and Apple document MPS acceleration generally, but kernel coverage and numerical behavior for this exact second-derivative SIREN workload must be measured on the target machine. The build plan already requires the right test: MPS fp32 with fallback unset plus fp64 CPU reference .
Quick test: Phase 37 §10.3 componentwise-AD dual-arm probe. Bad result: unsupported op, silent CPU fallback with fallback disabled, relative error outside the owner’s accepted tolerance, or runtime too slow for the smoke test.
Confidence note: medium-high risk; current primary docs support MPS as a backend but not this workload-specific guarantee ([docs.pytorch.org][1]).

**SL-2 — Stage-0 may be underpopulated after real admission, blacklist, and corrected dataset-role mapping.**
Why paper cannot settle it: Stage labels are owner-pending admitted-set EDA; the specs explicitly defer actual cluster counts and stage populations.
Quick test: Phase 39 Thrust-A scan. Bad result: Stage-0 count too small for train/val/test after `physical_key` grouping, or class imbalance makes validation meaningless.
Confidence note: medium.

**SL-3 — Multi-term PINN loss training may suffer term domination or causal-weight collapse.**
Why paper cannot settle it: the specs correctly require instrumentation, but convergence depends on data, initialization, weights, and hardware. PINN literature reports failure modes and training pathologies in more complex settings; this supports monitoring, not a proof of failure ([proceedings.neurips.cc][2]).
Quick test: Phase 43 smoke/pilot logs weighted losses, gradient norms per term, and `w_n` statistics. Bad result: one term dominates gradients, `w_n` collapses near zero over most time points, or validation physics loss does not decrease.
Confidence note: medium.

**SL-4 — Base-resolution stages may under-sample high-frequency close-encounter dynamics.**
Why paper cannot settle it: `DATASET-CONTEXT.md` gives medians of 61/127/1003 snapshots, but not per-stage SASD/IPR distributions.
Quick test: compute SASD/IPR distributions by stage during Phase 39 and compare against overfit residuals. Bad result: a large fraction of base-stage trajectories have high SASD/IPR flags or single-trajectory overfit cannot match between-snapshot dynamics.
Confidence note: medium; the CTL spec already recognizes endpoint metrics can miss between-snapshot encounters.

**SL-5 — Full-batch / accumulate-in-closure L-BFGS may exceed practical wall-time even if memory is acceptable.**
Why paper cannot settle it: no near-workload benchmark exists in the files. PyTorch’s official LBFGS is closure-based and constrained to one device, but workload cost is empirical ([docs.pytorch.org][3]).
Quick test: first L-BFGS smoke phase records wall-time, memory, and line-search iteration count. Bad result: swap pressure, out-of-memory, or per-step time too high for unattended operation.
Confidence note: medium.

**SL-6 — Lyapunov-time evaluation remains scientifically underdetermined for later chaotic stages.**
Why paper cannot settle it: `ctl_instruction.md` explicitly leaves the final τ_L estimator, time-unit convention, fit window, and thresholds owner-pending. Prior Brutus-based neural three-body work used narrower initial-condition regimes, so it is not direct evidence that this broader CTL-PINN evaluation is calibrated .
Quick test: before Stage 4/5, compare Rosenstein-style τ_L against a shadow/Benettin estimator on a stratified subset. Bad result: stage labels change materially under estimator choice.
Confidence note: high that this is unresolved; low that it blocks Stage 0.

## Out of scope / no cheap test now

* Whether the frozen dataset would be scientifically better if regenerated with different quasi-random scaling. `sampling_method.md` documents that quasi-random sampling-time size scaling distorts virial ratio by `s^3`, but the audit prompt treats regeneration as a one-way door and out of punch-list scope .
* Whether the final multi-stage platform should replace PINN training with a symplectic or Hamiltonian architecture. The locked design uses soft conservation regularizers; a locked-decision challenge would need a stronger project-specific proof than the current files provide.

# Part 8 — Sources

## Attached project files

* `RESEARCH-AGENT-PROMPT-STORM(1).md` — audit protocol, source tiers, proof rule, deliverable shape, owner carve-outs. 
* `ctl_instruction.md` — locked CTL/PINN data, preprocessing, curriculum, training-loop, and evaluation spec. 
* `pinn_architecture.md` — locked architecture, loss, AD, output-head, and acceptance-check spec. 
* `sampling_method.md` — frozen data-generation methodology. 
* `v2.0-build-plan.md` — build plan under audit. 
* `trainex-r1a-resolution-doc.md` — ratified decision set and first-run recipe. 
* `RATIFICATION.md` — owner ratification and carve-out record. 
* `DATASET-CONTEXT.md` — fixed verified dataset facts. 

## External primary / scholarly sources used

* Breen, P. G., Foley, C. N., Boekholt, T., & Portegies Zwart, S. (2020). *Newton versus the machine: solving the chaotic three-body problem using deep neural networks*. MNRAS. Used for Brutus-generated three-body ML precedent and scope comparison. 
* Krishnapriyan, A. S., et al. (2021). *Characterizing possible failure modes in physics-informed neural networks*. NeurIPS. Used for PINN failure-mode and curriculum-regularization context. ([proceedings.neurips.cc][2])
* Wang, S., Sankaran, S., Wang, H., & Perdikaris, P. (2023/2024). *An Expert’s Guide to Training Physics-Informed Neural Networks*. arXiv. Used for PINN training pathology / best-practice context. ([arXiv][4])
* Sitzmann, V., et al. (2020). *Implicit Neural Representations with Periodic Activation Functions*. NeurIPS. Used for SIREN derivative/representation support. ([proceedings.neurips.cc][5])
* PyTorch official documentation, MPS backend. Used for MPS backend context. ([docs.pytorch.org][1])
* PyTorch official documentation, `torch.optim.LBFGS`. Used for LBFGS closure/device constraints context. ([docs.pytorch.org][3])

[1]: https://docs.pytorch.org/docs/stable/notes/mps.html?utm_source=chatgpt.com "MPS backend — PyTorch 2.12 documentation"
[2]: https://proceedings.neurips.cc/paper/2021/hash/df438e5206f31600e6ae4af72f2725f1-Abstract.html "Characterizing possible failure modes in physics-informed neural networks"
[3]: https://docs.pytorch.org/docs/stable/generated/torch.optim.LBFGS.html?utm_source=chatgpt.com "LBFGS — PyTorch 2.12 documentation"
[4]: https://arxiv.org/abs/2308.08468?utm_source=chatgpt.com "An Expert's Guide to Training Physics-informed Neural Networks"
[5]: https://proceedings.neurips.cc/paper/2020/hash/53c04118df112c13a8c34b38343b9c10-Abstract.html "Implicit Neural Representations with Periodic Activation Functions"
