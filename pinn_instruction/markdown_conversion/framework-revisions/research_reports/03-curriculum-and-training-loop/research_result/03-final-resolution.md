# Issue 03 Final Resolution — Curriculum and Training Loop

**Status:** final adjudication from the attached bundles only  
**Date:** 2026-06-20  
**Spec-edit targets:** `ctl_instruction.md`, `pinn_architecture.md`  
**Evidence boundary:** outer canonical sections S1–S6 and outer report sections R1–R7; inner bundle markers were treated as ordinary content except when read inside their governing outer section.

## 0. Adjudication method

The canonical bundle was read first and an 81-claim independent ledger was frozen before the research-results bundle was opened. The frozen ledger is supplied separately as `issue03-independent-source-ledger.csv`. Report claims were then mapped to that ledger section by section in `issue03-report-claim-crosswalk.csv`.

No report was counted as a vote. Repetition, synthesis, and apparent textual overlap did not increase evidentiary weight. Final dispositions follow the source hierarchy: locked SCOPE-12 constraints, then the framework specs as revisable baseline, then verified grounding companions, then the non-authoritative issue document and baseline design reports. Claimed-unverified figures remain proposals, not facts. [Canonical: S1, “Source-Treatment Preamble” and “Bundle Reading Rule”; S2, `scope-12-hard-constraints.md` §§1–3; S4, `claims-register.md`, “no-in-milestone-verification boundary.” Reports: R1 §0; R2 opening/C1–C2; R3 §1; R7 “Method and posture.”]

Disposition meanings:

- **accepted** — supported by the governing canonical sources.
- **rejected** — contradicted by a lock, the current authoritative spec, or the attached evidence.
- **modified** — the core concern survives, but its framing or implementation must change.
- **surface_to_user** — the sources explicitly reserve the decision or materially conflict without a governing resolution.
- **defer** — evidence or specification is insufficient; no value or rule is invented.

## 1. Final Issue 03 resolutions

### 1.1 Causal-training mode — `surface_to_user`

The current spec baseline is per-time causal weighting with `stopgrad`, not global sampling plus dense-residual ALM. Dense-residual pseudo-ALM is rejected; ALM remains optional and scalar-only. The framework owner must still select the final training mode: retain the causal-weighting baseline, deliberately remove causal weighting while preserving the dense-ALM rejection unless that lock is explicitly reopened, or commission a fully specified time-windowed design. The numeric causal-exponent clipping bound remains unset. [Canonical: S2, framed causal decision; S5, `ctl_instruction.md` “Loss Function Formulation”; S5, `pinn_architecture.md` §§3.2, 4.1, 4.2. Reports: R1 §1.1; R2 C1 and causal decision; R3 §3.1; R4 Q1; R5 causal section; R6 D-04; R7 causal section.]

### 1.2 `s_min` frame — `surface_to_user`

The current baseline uses unsoftened geometric `s_min` for stage assignment and matched-Plummer pair distances in the training residual and energy. A scalar `max(s_min, ε)` is not the governing force or potential softening, and the current specs do not define a separate collision-loss term. The owner must ratify the geometric gate or define a softened gate, including which epsilon it uses. No option is selected here. [Canonical: S2, framed `s_min` decision; S2, hard constraint 4; S5, `ctl_instruction.md` Step 3 item 1; S5, `pinn_architecture.md` §§3.2, 3.4. Reports: R1 §1.2; R2 `s_min`; R3 §3.2; R7 `s_min`. Dissent selecting Option A: R4 Q2; R5 `s_min`; max-based wording also appears in R6 D-05.]

### 1.3 Epsilon strategy — `surface_to_user`

The loss-side value and form are locked: `ε_train = 1e-5`, matched-Plummer, identically in physics and energy. The open decision is only the offline static/invariant context: collapse it to `1e-5` or retain the current dual-context `ε_inv = 1e-10`. “`1e-10` everywhere” is preserved as a recorded alternative but is not selectable without reopening the locked loss contract. No attached sensitivity study resolves the static choice. [Canonical: S2, hard constraint 4 and framed epsilon decision; S5, `ctl_instruction.md` Step 3 item 1 and §2.5; S5, `pinn_architecture.md` §3.4; S6, `review_of_framework.md` §2.2 as opposing baseline argument. Reports: R1 §1.3; R2 epsilon; R3 §3.3; R4 Q3; R5 epsilon; R6 D-06; R7 epsilon.]

### 1.4 B-07 replay/lookahead batching — `modified`

Adopt stage-aware replay/lookahead selection through the locked query interfaces. Keep `240/16` for a 256-trajectory batch and `n_pts_cap = 32` as configurable provisional defaults, not verified optimums. Per-trajectory snapshot sampling is `min(n_pts_cap, n_snapshots)`, without replacement, with the current weighted/uniform split. Final-stage, undersized-next-stage, and replacement policies remain unspecified and must be made deterministic. [Canonical: S2, hard constraint 7; S4, CLM-12 and CLM-16; S5, `ctl_instruction.md` §2.6 and “Mini-Batch Construction”; S5, `pinn_architecture.md` §3.1/PIPE-04. Reports: R1 §3.1; R2 B-07; R3 §4.1; R7 B-07. Dissent treating exact values/pseudocode as settled: R4 B-07; R5 B-07; R6 B-07.]

### 1.5 B-08 data versus collocation points — `modified`

Make two independent logical point sets explicit: discrete BRUTUS snapshot points for Huber data loss, and continuous collocation points for physics; energy reuses the physics collocation set. A single concatenated forward pass is permitted but does not merge the loss roles. `8192/4096` are example or provisional budgets, and actual data count follows the per-trajectory cap. The current spec’s uniform/adaptive collocation choices remain; a mandatory 50/50 mixed continuous sampler is deferred. [Canonical: S4, CLM-12; S5, `pinn_architecture.md` §§3.1, 3.2, 3.4; S6, `review_of_framework.md` §§5.1–5.2. Reports: R1 §3.2; R2 B-08; R3 §4.2; R4 B-08; R7 B-08. Opposing exact-L1/exact-budget/mandatory-mix position: R6 B-08.]

### 1.6 M6 `L_norm` clamping — `modified`

Reject the original “clamp before IC mapping” rationale: `L_norm` is metadata, not an `IC13` slot. The attached sources conflict on whether the sole stored metadata value should be clipped. No global clamp is authorized by this adjudication; the current un-clipped baseline remains until the owner selects raw-only, raw-plus-derived-clipped, or global-clipped storage. Nonfinite and near-degenerate `L_max` behavior also requires an explicit guard. [Canonical: S2, hard constraints 1–2; S3, M6 and issue `compute_L_norm`; S5, `ctl_instruction.md` Steps 3–4. Reports: R1 §3.3; R2 M6; R3 §5.1; R4 M6; R5 M6; R7 M6. Opposing obsolete mandatory IC clamp: R6 “Normalized Angular Momentum and Matrix Clamping.”]

### 1.7 M7 `tau_L` exclusion from `IC13` — `accepted`

`tau_L` is deliberately excluded from the locked Jacobi-state input and retained only as staging/evaluation metadata. [Canonical: S2, hard constraints 1–2; S5, `ctl_instruction.md` Steps 3–4. Reports: R1 §3.4; R2 M7; R3 §5.2; R4 M7; R5 M7; R6 Lyapunov/M7; R7 M7.]

### 1.8 M14 gradient clipping — `modified`

Use `clip_value = C_stage × median(recent global gradient norms)` during Adam only; do not clip in L-BFGS. The PINN’s fixed `5.0` becomes the Stage-2/3 instance or fallback, not an additional multiplier. Preserve the CTL schedule `7–10 / 5 / 3`; do not canonize the claimed midpoint `8.5`. Bootstrap, lower-floor, and stage-history reset rules remain open. [Canonical: S4, CLM-10; S5, `ctl_instruction.md` “Adaptive Median-Based Gradient Clipping” and Phase 2b; S5, `pinn_architecture.md` §4.4; S6, `review_of_framework.md` §5.4. Reports: R1 §3.5; R2 M14; R3 §6.1; R7 M14. Reports adopting the midpoint or omitting execution gaps: R4 M14; R6 M14.]

### 1.9 M15 energy-loss weights — `rejected` as an issue-doc replacement

The issue premise of `lambda_E = 1000` is stale. Retain the current PHYS-05 warmup schedule, whose maximum is `1`, and reject CLM-11’s cap table up to `500`. Do not adopt automatic reweighting from the inconsistent issue safeguards; continue logging weighted losses, scheduled weights, and gradient statistics before designing any control law. [Canonical: S3, M15 and energy-schedule code; S4, CLM-11; S5, `pinn_architecture.md` §4.1; S5, `ctl_instruction.md` “Loss Function Formulation.” Reports: R1 §3.6; R2 M15; R3 §6.2; R7 M15. Opposing live-option/mandatory-cap positions: R4 M15; R5 M15; R6 M15.]

### 1.10 M16 `dt_out`-aware collocation scaling — `defer`

The verified `dt_out` values do not establish a collocation-density objective or direction. Keep `dt_out` and `n_snapshots` exposed as metadata and retain the present fixed/configurable collocation budget until a fixed-compute ablation compares constant and candidate policies. Do not adopt CLM-20’s `dt_base/dt_out` factors or the inverse. [Canonical: S4, CLM-17/20 and VF-1; S5, `ctl_instruction.md` forward-interface note; S5, `pinn_architecture.md` §3.2; S6, `review_of_framework.md` §5.3; S3, M16. Reports supporting deferral: R1 §3.7; R3 §6.3; R7 M16. Opposing adoption: R2 M16; R4 M16; R5 M16; R6 M16.]

### 1.11 D5 stage transitions — `modified`

Retain the four current success criteria as the baseline pending a Stage-0 pilot. Add an explicit operational state machine: **ADVANCE** only on an approved success gate; **RECOVER** for NaN/Inf rollback and bounded retry; **HALT/REVIEW** for max-epoch or stagnation unless the owner explicitly authorizes degraded advancement. The percentile-10 relaxation, per-stage thresholds, epoch table, stagnation window, and retry limits are not adopted; they remain claimed-unverified. The locked energy denominator contract is unchanged. [Canonical: S3, D5 and fallback proposal; S4, CLM-08/09; S5, `ctl_instruction.md` “Stage Transition Criteria”; S5, `pinn_architecture.md` §3.4. Reports supporting state separation: R3 §6.4; R7 D5. Reports treating failure triggers as advancement: R1 §3.8; R2 D5; R4 D5; R5 D5; R6 D5.]

### 1.12 NS-12 componentwise automatic differentiation — `accepted`

The PHYS-02 contract already requires all coordinatewise first and second derivatives and forbids the summed-output VJP. The `review_of_framework.md` all-ones-covector snippet is rejected. Executable batched implementation/performance details remain FUT work. [Canonical: S5, `pinn_architecture.md` §5.3.1 and §10.3; S6, `review_of_framework.md` §4.3. Reports: R1 §3.9; R2 NS-12; R3 §6.5; R4 NS-12; R5 NS-12; R6 NS-12; R7 NS-12.]

### 1.13 NS-13 energy Huber delta — `defer`

`delta_E = 1.0` remains the configurable current baseline, not a validated optimum. No attached normalized `|Delta H|` distribution supports an immediate change to `0.1` or `0.01–0.1`. Measure quantiles, linear-branch occupancy, validation energy drift, and weighted gradients before changing the value or making it stage-dependent. [Canonical: S3, NS-13; S5, `pinn_architecture.md` §3.4; S6, `review_of_framework.md` §4.4. Reports supporting defer/calibration: R2 NS-13; R3 §6.6; R5 NS-13; R7 NS-13. Reports directing immediate reduction: R1 §3.10; R4 NS-13; R6 NS-13.]

### 1.14 NS-18 loss scaling and units — `modified`

Confirm the current dimensionless contract: projected scaled positions for data, componentwise normalized-time derivatives for physics, matched `ε_train = 1e-5` in physics and energy, raw masses, the same physics/energy collocation set, the IC anchor, and angular-momentum regularization; there is no linear-momentum loss. Replace the issue document’s L1/MAE data term with the spec’s Huber contract. Chain factors `2` and `4` apply only when differentiating with respect to `tau`, not when `u` is already the autograd leaf. [Canonical: S2, hard constraints 1–4 and 6; S5, `pinn_architecture.md` §§3.1–3.5, 4.1, 5.3.1; S5, `ctl_instruction.md` “Data Flow” and total loss. Reports: R1 §3.11; R2 NS-18; R3 §6.7; R4 NS-18; R5 NS-18; R7 NS-18. Opposing L1 contract: R6 B-08.]

### 1.15 Data-driven adaptive stage assignment — `modified`

Permit admitted-set EDA, robust transforms, PCA, and clustering as offline diagnostics or boundary-calibration tools. Do not adopt `stage_strat_revision.md` Table 4 wholesale: it erases the existing Stage-2 hierarchical-gold and Stage-5 quasi-random-gold refinement roles and conflicts with the resolved gold-counterpart obligation. Materialize stable integer labels keyed by `record_key` before training. Use `Q_norm = Q_raw/s^3` only where per-record `s` is established; otherwise exclude that feature for affected quasi-random records. The 5% versus >10% population safeguard is surfaced to the owner, and CLM-02..07 remain unverified. [Canonical: S3, adaptive proposal; S4, CLM-02..07 and CLM-14/15; S5, `ctl_instruction.md` stratification/Step 5; S5, `sampling_method.md` “Sampling-Time Size Variability”; S6, `stage_strat_revision.md` Parts II–IV. Reports supporting constrained topology: R1 §4; R2 adaptive; R3 §7. Opposing wholesale topology/selected threshold: R4 adaptive. R5 incorrectly treated the source as absent; R7 supports offline freezing but leaves topology/threshold open.]

### 1.16 Locked `D` conflict — `accepted` for `4.6416`, `rejected` for `6.694`

`D = (G T^2)^(1/3) ≈ 4.6416` is mandatory. Remove the issue document’s `6.694` claim and reject its P4-1 rerun directive. In the attached `compute_tau_L` pseudocode, the assigned `D` and `V` are unused, so changing those two dead assignments alone does not change that routine; however, the attachments do not establish whether any external processed artifact or threshold was produced under `6.694`. Recompute only if provenance shows an affected artifact. [Canonical: S2, hard constraint 6; S3, `tau_L` code/P4-1; S4, CLM-01/19 and VF-5; S5, `ctl_instruction.md` §2.5. Reports identifying dead assignments: R1 §2.1; R2 D conflict; R7 D conflict. Reports emphasizing blanket rederivation: R3 §8.1; R4 D conflict; R5 D/tau; R6 characteristic-scale section.]

### 1.17 `L_max` and `tau_L` formulas — `modified` / `surface_to_user`

Retain `L_max = M_tot r_char sqrt(2|E|/M_tot)` as the current **characteristic angular-momentum scale**, not as a proven global maximum for arbitrary three-body states. The canonical `tau_L` estimator remains unresolved: the current spec uses a Rosenstein-style trajectory estimator, while the issue/baseline sources propose shadow/Benettin integration. The owner must select the method and time-unit convention before locking `tau_L` stage thresholds. Until then, retain Rosenstein as the current revisable baseline. Do not normatively adopt the issue shadow code because its force denominator is not matched-Plummer, and do not adopt the unspecified “PCA+Rosenstein” shortcut. The perturbation `1e-8` and static `1e-10` are shadow-method parameters only, distinct from training softening. [Canonical: S3, `tau_L`/`L_max` section; S5, `ctl_instruction.md` Step 3 items 2 and 5; S6, `review_of_framework.md` §1.1; S2, hard constraint 4. Reports supporting unresolved method: R1 §2.2; R2 tau/Lmax; R3 §§8.2–8.3; R7 tau/Lmax. Opposing canonization/complementary adoption: R4 tau/Lmax; R5 tau; R6 Lyapunov section.]

### 1.18 ALM `mu_p` clamp — `defer`

The default loss has no `mu_p`, because dense-residual ALM is rejected. A clamp could apply only to an optional scalar-conservation ALM after that ablation defines constraint normalization, penalty update law, state reset/persistence, and update cadence. The exact `[1e-4, 100]` bounds and RMSprop-style update are not adopted. [Canonical: S3, ALM update proposal; S5, `ctl_instruction.md` loss formulation; S5, `pinn_architecture.md` §§4.1–4.2; S4, non-dataset-figure note. Reports supporting conditional/deferred treatment: R1 §5; R3 §9; R7 ALM. Reports adopting exact bounds for P2: R2 ALM; R4 ALM; R5 ALM; R6 ALM.]

## 2. Claim matrix

The asterisk in a report cell denotes a mixed report position that is recorded on both sides. Full report-section-to-claim mapping is in `issue03-report-claim-crosswalk.csv`.

| claim_id | issue_section | final_disposition | canonical_source_basis | supporting_R# | opposing_R# | uncertainty_type |
|---|---|---|---|---|---|---|
| GOV-01 | governance | accepted | S1::Source-Treatment Preamble; S2::scope-12-hard-constraints.md §§1–3 | R1 §0; R2 Cross-cutting C1/C2; R3 §1; R5 Executive summary; R6 Epistemological baseline; R7 Method | — | none |
| GOV-02 | governance | accepted | S1::Source-Treatment Preamble; S2::scope-12-hard-constraints.md §2 | R1 §0; R2 Cross-cutting C1/C2; R3 §1; R5 Executive summary; R6 Epistemological baseline; R7 Method | R6 Source omissions | none |
| GOV-03 | governance | accepted | S4::claims-register.md, no-in-milestone-verification boundary | R1 §0; R3 §1; R5 Executive summary; R6 Epistemological baseline; R7 Method | R6 Dataset/stages | epistemic |
| GOV-04 | governance | accepted | S2::framed-research-questions.md, How to read these questions / Section 2 | R3 §1 | — | decision |
| CAU-01 | causal-training mode | accepted | S5::ctl_instruction.md, Loss Function Formulation; S5::pinn_architecture.md §§3.2,4.1 | R1 §1.1; R2 Cross-cutting C1/C2; R3 §3.1; R4 Q1; R5 Causal; R6 Causal; R7 Causal | — | none |
| CAU-02 | causal-training mode | accepted | S5::ctl_instruction.md, Loss Function Formulation; S5::pinn_architecture.md §4.2 | R1 §1.1; R2 Cross-cutting C1/C2; R3 §3.1; R4 Q1; R5 Causal; R6 Causal; R7 Causal | — | none |
| CAU-03 | causal-training mode | rejected | S3::D-04/Open Decisions versus S5::ctl_instruction.md, Loss Function Formulation and S5::pinn_architecture.md §§3.2,4.1,4.2 | R1 §1.1; R2 Cross-cutting C1/C2; R3 §3.1; R4 Q1; R5 Causal; R6 Causal; R7 Causal | — | source_conflict |
| CAU-04 | causal-training mode | surface_to_user | S2::framed-research-questions.md, causal-training-mode decision | R1 §1.1; R2 Causal decision; R3 §3.1; R4 Q1; R5 Causal; R6 Causal; R7 Causal | — | decision |
| CAU-05 | causal-training mode | defer | S5::ctl_instruction.md, Loss Function Formulation; S5::pinn_architecture.md §4.1 | R1 §1.1; R2 Causal decision; R3 §3.1; R4 Q1; R7 Causal | — | source_silent |
| SMIN-01 | s_min frame | accepted | S5::ctl_instruction.md, Step 3 item 1 / Stage 6 criteria | R1 §1.2; R2 s_min decision; R3 §3.2; R4 Q2; R5 s_min; R7 s_min | — | none |
| SMIN-02 | s_min frame | accepted | S2::scope-12-hard-constraints.md item 4; S5::pinn_architecture.md §§3.2,3.4 | R1 §1.2; R2 s_min decision; R3 §3.2; R4 Q2; R5 s_min; R7 s_min | R6 s_min | none |
| SMIN-03 | s_min frame | surface_to_user | S2::framed-research-questions.md, s_min-frame decision | R1 §1.2; R2 s_min decision; R3 §3.2; R6 s_min; R7 s_min | R4 Q2; R5 s_min | decision |
| EPS-01 | epsilon strategy | accepted | S2::scope-12-hard-constraints.md item 4; S5::pinn_architecture.md §§3.2,3.4 | R1 §1.3; R2 epsilon decision; R3 §3.3; R4 Q3; R5 epsilon; R6 epsilon; R7 epsilon | — | none |
| EPS-02 | epsilon strategy | accepted | S5::ctl_instruction.md Step 3 item 1 / §2.5; S5::pinn_architecture.md §3.4 dual-epsilon note | R1 §1.3; R2 epsilon decision; R3 §3.3; R4 Q3; R5 epsilon; R6 epsilon; R7 epsilon | — | none |
| EPS-03 | epsilon strategy | surface_to_user | S2::framed-research-questions.md, epsilon-strategy decision; S2::scope-12-hard-constraints.md item 4 | R1 §1.3; R2 epsilon decision; R3 §3.3; R4 Q3; R5 epsilon; R6 epsilon; R7 epsilon | — | decision |
| EPS-04 | epsilon strategy | modified | S6::review_of_framework.md §2.2 versus S2::scope-12-hard-constraints.md item 4 and S5::ctl_instruction.md Step 3 | R1 §1.3; R2 Cross-cutting C1/C2; R3 §3.3 | — | source_conflict |
| EPS-05 | epsilon strategy | defer | S2::framed-research-questions.md epsilon decision; S4::claims-register.md boundary | R1 §1.3; R2 epsilon decision; R3 §3.3; R4 Q3; R7 epsilon | — | missing_empirical_evidence |
| B07-01 | B-07 replay/lookahead | accepted | S5::ctl_instruction.md §2.6 stage-query interface / Mini-Batch Construction; S2::scope-12-hard-constraints.md item 7 | R1 §3.1; R2 B-07; R3 §4.1; R4 B-07; R5 B-07; R6 B-07; R7 B-07 | — | none |
| B07-02 | B-07 replay/lookahead | modified | S5::ctl_instruction.md Mini-Batch Construction; S4::claims-register.md CLM-12 | R1 §3.1; R2 B-07; R3 §4.1; R7 B-07 | R4 B-07; R5 B-07; R6 B-07 | claimed_unverified |
| B07-03 | B-07 replay/lookahead | accepted | S5::ctl_instruction.md Mini-Batch Construction | R1 §3.1; R2 B-07; R3 §4.1; R7 B-07 | R4 B-07; R5 B-07; R6 B-07 | none |
| B07-04 | B-07 replay/lookahead | rejected | S5::pinn_architecture.md §3.1 PIPE-04/SI-PINN-003; S2::scope-12-hard-constraints.md §2 | R1 §3.1; R2 B-07; R3 §4.1; R4 B-07; R5 B-07; R7 B-07 | — | none |
| B07-05 | B-07 replay/lookahead | defer | S5::ctl_instruction.md stage-query interface and Mini-Batch Construction | R3 §4.1 | R5 B-07 | source_silent |
| B08-01 | B-08 point-set separation | accepted | S5::pinn_architecture.md §§3.1,3.2; S6::review_of_framework.md §5.1 | R1 §3.2; R2 B-08; R3 §4.2; R4 B-08; R5 B-08; R6 B-08; R7 B-08 | — | none |
| B08-02 | B-08 point-set separation | accepted | S5::pinn_architecture.md §3.1 | R1 §3.2; R2 B-08; R3 §4.2; R4 B-08; R5 B-08; R7 B-08 | R6 B-08 | none |
| B08-03 | B-08 point-set separation | accepted | S5::pinn_architecture.md §3.4 Key Implementation Notes | R1 §3.2; R2 B-08; R3 §4.2; R4 B-08; R5 B-08; R7 B-08 | — | none |
| B08-04 | B-08 point-set separation | modified | S5::pinn_architecture.md §§3.1,3.2; S4::claims-register.md CLM-12 | R1 §3.2; R2 B-08; R3 §4.2; R7 B-08 | R4 B-08; R6 B-08 | claimed_unverified |
| B08-05 | B-08 point-set separation | defer | S5::pinn_architecture.md §3.2 versus S6::review_of_framework.md §5.2 and S3::Unified Batch Specification | R1 §3.2; R3 §4.2 | R4 B-08; R6 B-08 | source_conflict |
| M6-01 | M6 L_norm clamp | rejected | S2::scope-12-hard-constraints.md items 1–2; S5::ctl_instruction.md Step 4 | R1 §3.3; R2 M6; R3 §5.1; R4 M6; R5 M6; R7 M6 | R6 L_norm | none |
| M6-02 | M6 L_norm clamp | surface_to_user | S5::ctl_instruction.md Step 3 item 2 versus S3::L_max Computation/M6 | R2 M6; R3 §5.1; R4 M6; R5 M6; R7 M6* | R1 §3.3; R6 L_norm; R7 M6* | source_conflict |
| M6-03 | M6 L_norm clamp | defer | S5::ctl_instruction.md Step 3 item 2 | R3 §5.1; R3 §8.2 | — | source_silent |
| M7-01 | M7 tau_L input | accepted | S2::scope-12-hard-constraints.md items 1–2; S5::ctl_instruction.md Steps 3–4 | R1 §3.4; R2 M7; R3 §5.2; R4 M7; R5 M7; R6 Lyapunov/M7; R7 M7 | — | none |
| M7-02 | M7 tau_L input | accepted | S5::ctl_instruction.md Step 3 outputs and Step 4 | R1 §3.4; R2 M7; R3 §5.2; R4 M7; R5 M7; R6 Lyapunov/M7; R7 M7 | — | none |
| M14-01 | M14 gradient clipping | accepted | S5::pinn_architecture.md §4.4; S5::ctl_instruction.md Adaptive Median-Based Gradient Clipping; S6::review_of_framework.md §5.4 | R1 §3.5; R2 M14; R3 §6.1; R4 M14; R5 M14; R6 M14; R7 M14 | — | none |
| M14-02 | M14 gradient clipping | modified | S5::pinn_architecture.md §4.4; S5::ctl_instruction.md clipping schedule | R1 §3.5; R2 M14; R3 §6.1; R4 M14; R5 M14; R6 M14; R7 M14 | — | source_conflict |
| M14-03 | M14 gradient clipping | defer | S5::ctl_instruction.md clipping schedule; S4::claims-register.md CLM-10; S6::review_of_framework.md §5.4 | R1 §3.5; R2 M14; R3 §6.1; R7 M14 | R4 M14; R6 M14 | claimed_unverified |
| M14-04 | M14 gradient clipping | defer | S5::pinn_architecture.md §4.4; S5::ctl_instruction.md clipping section | R3 §6.1 | R4 M14; R6 M14 | source_silent |
| M14-05 | M14 gradient clipping | accepted | S5::ctl_instruction.md Phase 2b; S6::review_of_framework.md §5.4 | R1 §3.5; R2 M14; R3 §6.1; R4 M14; R7 M14 | — | none |
| M15-01 | M15 energy weights | rejected | S3::M15 versus S5::pinn_architecture.md §4.1 | R1 §3.6; R2 Cross-cutting C1/C2; R2 M15; R3 §6.2; R7 M15 | R4 M15; R5 M15; R6 M15 | source_conflict |
| M15-02 | M15 energy weights | accepted | S5::pinn_architecture.md §4.1; S5::ctl_instruction.md Loss Function Formulation | R1 §3.6; R2 M15; R3 §6.2; R7 M15 | R4 M15; R5 M15; R6 M15 | none |
| M15-03 | M15 energy weights | rejected | S3::M15/Energy Schedule; S4::claims-register.md CLM-11; S5::pinn_architecture.md §4.1 | R1 §3.6; R2 M15; R3 §6.2; R7 M15 | R4 M15; R5 M15; R6 M15 | claimed_unverified |
| M15-04 | M15 energy weights | defer | S3::M15 text versus get_lambda_E code; S5 specs silent | R1 §3.6; R3 §6.2 | R2 M15; R4 M15; R6 M15 | source_conflict |
| M16-01 | M16 dt_out scaling | accepted | S4::verified-facts-reference.md VF-1 / CLM-17 | R1 §3.7; R3 §6.3; R7 M16 | — | none |
| M16-02 | M16 dt_out scaling | defer | S5::ctl_instruction.md Mini-Batch forward-interface note; S6::review_of_framework.md §5.3; S3::M16 | R1 §3.7; R3 §6.3; R7 M16 | R2 M16; R4 M16; R5 M16; R6 M16 | source_conflict |
| M16-03 | M16 dt_out scaling | rejected | S4::claims-register.md CLM-20 | R1 §3.7; R3 §6.3; R7 M16 | R2 M16; R4 M16; R5 M16; R6 M16 | claimed_unverified |
| D5-01 | D5 stage transition | accepted | S5::ctl_instruction.md Stage Transition Criteria | R1 §3.8; R2 D5; R3 §6.4; R4 D5; R5 D5; R7 D5 | — | none |
| D5-02 | D5 stage transition | accepted | S5::ctl_instruction.md Stage Transition author note; S3::D5/Pilot | R1 §3.8; R2 D5; R3 §6.4; R4 D5; R5 D5; R7 D5 | — | none |
| D5-03 | D5 stage transition | modified | S3::D5 Path B versus S5::ctl_instruction.md “advance only when all four” | R3 §6.4 | R1 §3.8; R2 D5; R4 D5; R5 D5; R6 D5 | semantic_conflict |
| D5-04 | D5 stage transition | surface_to_user | S3::D5 versus S5::ctl_instruction.md Stage Transition Criteria | R3 §6.4; R7 D5 | R1 §3.8; R2 D5; R4 D5; R5 D5; R6 D5 | decision |
| D5-05 | D5 stage transition | defer | S3::D5; S4::claims-register.md CLM-08/09 | R1 §3.8; R2 D5; R3 §6.4; R4 D5; R5 D5; R7 D5 | R6 D5 | claimed_unverified |
| D5-06 | D5 stage transition | accepted | S5::pinn_architecture.md §3.4; S5::ctl_instruction.md Stage Transition criterion 4 | R1 §3.8; R2 D5; R3 §6.4; R4 D5; R7 D5 | — | none |
| NS12-01 | NS-12 componentwise AD | accepted | S5::pinn_architecture.md §5.3.1 / §10.3 | R1 §3.9; R2 NS-12; R3 §6.5; R4 NS-12; R5 NS-12; R6 NS-12; R7 NS-12 | — | none |
| NS12-02 | NS-12 componentwise AD | rejected | S6::review_of_framework.md §4.3 versus S5::pinn_architecture.md §5.3.1 | R1 §3.9; R2 Cross-cutting C1/C2; R2 NS-12; R3 §6.5; R4 NS-12; R7 NS-12 | — | source_conflict |
| NS12-03 | NS-12 componentwise AD | defer | S5::pinn_architecture.md §5.3.1 illustrative-pattern note | R1 §3.9; R2 NS-12; R3 §6.5 | — | implementation_gap |
| NS13-01 | NS-13 energy Huber delta | accepted | S5::pinn_architecture.md §3.4 | R1 §3.10; R2 NS-13; R3 §6.6; R5 NS-13; R7 NS-13 | — | none |
| NS13-02 | NS-13 energy Huber delta | defer | S3::NS-13; S6::review_of_framework.md §4.4; S4::claims-register.md boundary | R2 NS-13; R3 §6.6; R5 NS-13; R7 NS-13 | R1 §3.10; R4 NS-13; R6 NS-13 | missing_empirical_evidence |
| NS13-03 | NS-13 energy Huber delta | defer | S2::framed-research-questions.md NS-13; S5/S6/S3 divergent positions | R2 NS-13; R3 §6.6; R5 NS-13; R7 NS-13 | R1 §3.10; R4 NS-13; R6 NS-13 | decision |
| NS18-01 | NS-18 scaling contract | accepted | S2::scope-12-hard-constraints.md items 3,4,6; S5::pinn_architecture.md §§3.1–3.5,4.1 | R1 §3.11; R2 NS-18; R3 §6.7; R4 NS-18; R5 NS-18; R7 NS-18 | — | none |
| NS18-02 | NS-18 scaling contract | modified | S3::Loss Component Scaling Contract versus S5::pinn_architecture.md §3.1 | R1 §3.11; R2 NS-18; R3 §6.7; R4 NS-18; R5 NS-18; R7 NS-18 | — | source_conflict |
| NS18-03 | NS-18 scaling contract | accepted | S5::pinn_architecture.md §5.3.1 | R1 §3.11; R2 NS-18; R3 §6.5; R3 §6.7; R4 NS-18; R7 NS-18 | — | none |
| NS18-04 | NS-18 scaling contract | accepted | S2::scope-12-hard-constraints.md item 3; S5::pinn_architecture.md §4.1 | R1 §3.11; R2 NS-18; R3 §6.7; R4 NS-18; R7 NS-18 | — | none |
| ADAPT-01 | adaptive stage assignment | modified | S5::ctl_instruction.md stratification/Step 5; S6::stage_strat_revision.md Parts II–IV; S3::Adaptive Stage Assignment | R1 §4; R2 Adaptive assignment; R3 §7; R7 Adaptive | R5 Adaptive | source_conflict |
| ADAPT-02 | adaptive stage assignment | accepted | S5::ctl_instruction.md stratification and Step 5 gold-counterpart ruling | R1 §4; R2 Adaptive assignment; R3 §7 | R4 Adaptive; R5 Adaptive; R7 Adaptive | none |
| ADAPT-03 | adaptive stage assignment | rejected | S6::stage_strat_revision.md Phase IV Table 4 versus S5::ctl_instruction.md stratification/Step 5 | R1 §4; R2 Adaptive assignment; R3 §7; R7 Adaptive | R4 Adaptive; R5 Adaptive | source_conflict |
| ADAPT-04 | adaptive stage assignment | surface_to_user | S6::stage_strat_revision.md Population Control versus S3::Adaptive Stage Assignment | R1 §4; R2 Adaptive assignment; R3 §7 | R4 Adaptive; R5 Adaptive; R7 Adaptive | source_conflict |
| ADAPT-05 | adaptive stage assignment | defer | S5::sampling_method.md Sampling-Time Size Variability; S6::stage_strat_revision.md Normalized Virial Ratio | R1 §4; R2 Adaptive assignment; R3 §7; R4 Adaptive; R7 Adaptive | R5 Adaptive | data_availability_gap |
| ADAPT-06 | adaptive stage assignment | rejected | S4::claims-register.md CLM-02..07 | R1 §4; R2 Adaptive assignment; R3 §7; R4 Adaptive; R5 Adaptive; R7 Adaptive | R6 Dataset/stages | claimed_unverified |
| ADAPT-07 | adaptive stage assignment | defer | S6::stage_strat_revision.md Parts I–III and validation protocol | R1 §4; R2 Adaptive assignment; R3 §7; R4 Adaptive; R7 Adaptive | R5 Adaptive | missing_empirical_evidence |
| D-01 | D conflict | accepted | S2::scope-12-hard-constraints.md item 6; S4::CLM-19/VF-5; S5::ctl_instruction.md §2.5 | R1 §2.1; R2 D conflict; R3 §8.1; R4 D conflict; R5 D conflict; R6 Characteristic scale; R7 D conflict | — | none |
| D-02 | D conflict | rejected | S3::P4-1/D statement versus D-01 | R1 §2.1; R2 D conflict; R3 §8.1; R4 D conflict; R5 D conflict; R6 Characteristic scale; R7 D conflict | — | none |
| D-03 | D conflict | accepted | S3::tau_L Computation code | R1 §2.1; R2 D conflict; R3 §8.1*; R7 D conflict | R3 §8.1*; R4 D conflict; R5 tau/Lmax | code_inspection |
| D-04 | D conflict | defer | S1::self-contained access boundary; S3::claims only | R3 §8.1; R7 D conflict | R1 §2.1; R2 D conflict; R4 D conflict | unavailable_evidence |
| LMAX-01 | tau_L/L_max formulas | accepted | S5::ctl_instruction.md Step 3 item 2; S6::review_of_framework.md §1.1; S3::L_max section | R1 §2.2; R2 tau/Lmax; R3 §8.2; R4 tau/Lmax; R7 Lmax/tau | — | none |
| LMAX-02 | tau_L/L_max formulas | modified | S5::ctl_instruction.md “characteristic circular-orbit scale” versus S6/S3 “maximum” language | R3 §8.2 | — | epistemic |
| TAUL-01 | tau_L/L_max formulas | surface_to_user | S5::ctl_instruction.md Step 3 item 5 versus S3::tau_L section and S6::review_of_framework.md §1.1 | R1 §2.2; R2 tau/Lmax; R3 §8.3; R7 Lmax/tau | R4 tau/Lmax; R5 tau/Lmax; R6 Lyapunov/M7 | source_conflict |
| TAUL-02 | tau_L/L_max formulas | rejected | S3::tau_L operational note; S6::stage_strat_revision.md | R3 §8.3; R7 Lmax/tau* | R1 §2.2; R2 tau/Lmax; R4 tau/Lmax; R5 tau/Lmax; R7 Lmax/tau* | source_silent |
| TAUL-03 | tau_L/L_max formulas | defer | S5::ctl_instruction.md Step 3 item 5; S3::compute_tau_L | R1 §2.2; R2 tau/Lmax; R3 §8.3; R7 Lmax/tau | R4 tau/Lmax; R5 tau/Lmax | source_conflict |
| TAUL-04 | tau_L/L_max formulas | accepted | S3::tau_L code; S2::framed-research-questions.md tau_L formulas; S2::scope-12-hard-constraints.md item 4 | R1 §2.2; R2 tau/Lmax; R3 §8.3; R4 tau/Lmax; R7 Lmax/tau | — | none |
| TAUL-05 | tau_L/L_max formulas | rejected | S3::compute_tau_L code versus S5::ctl_instruction.md §2.5 PHYS-03 anti-pattern and S2::HC-4 | R3 §8.3; R7 Lmax/tau* | R4 tau/Lmax; R5 tau/Lmax; R6 Lyapunov/M7; R7 Lmax/tau* | source_conflict |
| ALM-01 | ALM mu_p clamp | accepted | S5::ctl_instruction.md Loss Function Formulation; S5::pinn_architecture.md §§4.1,4.2 | R1 §5; R2 ALM clamp; R3 §9; R4 ALM clamp; R5 ALM clamp; R6 ALM; R7 ALM | — | none |
| ALM-02 | ALM mu_p clamp | modified | S5::pinn_architecture.md §4.2; S3::ALM Parameter Update | R1 §5; R2 ALM clamp; R3 §9; R4 ALM clamp; R5 ALM clamp; R7 ALM | R6 ALM | design_contingency |
| ALM-03 | ALM mu_p clamp | defer | S3::ALM Parameter Update; S5::pinn_architecture.md §4.2; S4::claims-register.md non-dataset figures note | R1 §5; R3 §9; R7 ALM | R2 ALM clamp; R4 ALM clamp; R5 ALM clamp; R6 ALM | missing_specification |

## 3. Disagreement register

Every material conflict and minority position is retained; agreement was not treated as evidence.

| conflict_id | topic | positions | final_handling | canonical_source_basis | report_sections |
|---|---|---|---|---|---|
| DGR-01 | Causal baseline | Issue doc/R6-style global+ALM framing versus current causal weighting and dense-ALM rejection. | Current baseline is causal weighting; final mode remains owner decision. | S2 framed causal question; S5 ctl Loss Formulation; S5 pinn §§3.2,4.1,4.2 | R1 §1.1; R2 C1/causal; R3 §3.1; R4 Q1; R5 causal; R6 causal; R7 causal |
| DGR-02 | s_min decision status | R1/R2/R3/R6/R7 preserve owner decision; R4 and R5 select Option A. | Surface to owner; current baseline is A but not adjudicated as owner-approved. | S2 framed s_min decision; S5 ctl Step 3; S5 pinn §§3.2,3.4 | R1 §1.2; R2 s_min; R3 §3.2; R4 Q2; R5 s_min; R6 D-05; R7 s_min |
| DGR-03 | s_min loss formulation | Issue/R4/R5/R6 use max(s_min,eps) language; R1/R3/R7 distinguish matched-Plummer and note no canonical collision-loss term. | Use unsoftened gate plus matched-Plummer residual/energy; do not encode max as force/potential. | S2 HC-4; S5 ctl Step 3; S5 pinn §§3.2,3.4 | R1 §1.2; R3 §3.2; R4 Q2; R5 s_min; R6 D-05; R7 s_min |
| DGR-04 | Static epsilon | Dual-context baseline versus collapse to 1e-5; Option C conflicts with locked loss value. | Surface A/B static-context choice; C preserved only as rejected alternative. | S2 HC-4/framed epsilon; S5 ctl Step 3; S5 pinn §3.4; S6 review §2.2 | R1 §1.3; R2 epsilon; R3 §3.3; R4 Q3; R5 epsilon; R6 D-06; R7 epsilon |
| DGR-05 | B-07 constants | Some reports treat 240/16/32 as mandatory; others treat them as claimed/configurable defaults and enforce min(cap,n_snapshots). | Retain structure and provisional defaults; min-cap governs. | S5 ctl Mini-Batch; S4 CLM-12/16 | R1 §3.1; R2 B-07; R3 §4.1; R4 B-07; R5 B-07; R6 B-07; R7 B-07 |
| DGR-06 | B-08 sampler/budgets | Reports differ on exact 8192/4096 and mandatory 50/50 collocation mix. | Sets/Huber accepted; budgets provisional; collocation mixed policy deferred. | S5 pinn §§3.1,3.2,3.4; S4 CLM-12; S6 review §§5.1,5.2 | R1 §3.2; R2 B-08; R3 §4.2; R4 B-08; R6 B-08; R7 B-08 |
| DGR-07 | L_norm clamp | R1/R7 favor staging clamp, R2/R3 preserve raw plus optional derived clip, R4 says no global clamp, R6 mandates obsolete IC clamp. | Reject IC rationale; defer metadata storage/clamp policy and preserve current raw baseline. | S5 ctl Steps 3–4; S2 HC-1/2; S3 M6 | R1 §3.3; R2 M6; R3 §5.1; R4 M6; R5 M6; R6 L_norm; R7 M6 |
| DGR-08 | Gradient C value | Structural merge is shared, but 8.5 versus 7–10 and bootstrap/reset differ. | Adopt C_stage×median; keep 7–10 range; defer exact early C and execution details. | S5 ctl clipping; S5 pinn §4.4; S4 CLM-10 | R1 §3.5; R2 M14; R3 §6.1; R4 M14; R6 M14; R7 M14 |
| DGR-09 | Energy-weight schedule | R1/R2/R3/R7 reject issue cap; R4/R5/R6 keep it as option or mandate it. | Reject CLM-11 cap table and retain PHYS-05 max≤1 schedule. | S5 pinn §4.1; S3 M15; S4 CLM-11 | R1 §3.6; R2 M15; R3 §6.2; R4 M15; R5 M15; R6 M15; R7 M15 |
| DGR-10 | Energy dominance safeguard | Some reports adopt/encourage automatic reduction; others find issue formulations inconsistent and unsupported. | Defer automatic reweighting; log weighted losses/gradients first. | S3 M15 text/code; S5 specs silent | R1 §3.6; R2 M15; R3 §6.2; R4 M15; R6 M15 |
| DGR-11 | dt_out collocation scaling | R1/R3/R7 defer; R2/R4/R5/R6 adopt or direct adoption of dt_base/dt_out. | Defer; verified dt_out does not establish a scaling objective or direction. | S5 ctl forward-interface note; S6 review §5.3; S3 M16; S4 CLM-17/20 | R1 §3.7; R2 M16; R3 §6.3; R4 M16; R5 M16; R6 M16; R7 M16 |
| DGR-12 | Stage fallback semantics | R1/R2/R4/R5/R6 treat max/stagnation/NaN as fallback advancement; R3 separates ADVANCE/RECOVER/HALT; R7 leaves choice open. | No automatic advancement on failure; surface degraded-advance policy. | S5 ctl Stage Transition; S3 D5 | R1 §3.8; R2 D5; R3 §6.4; R4 D5; R5 D5; R6 D5; R7 D5 |
| DGR-13 | Validation stability | Strict minimum versus percentile-10 relaxation. | Retain current baseline until pilot; surface relaxation decision. | S5 ctl Stage Transition criterion 2; S3 D5 | R1 §3.8; R2 D5; R3 §6.4; R4 D5; R7 D5 |
| DGR-14 | Energy Huber delta | R1/R4/R6 argue immediate reduction; R2 poses; R3/R7 defer pending data. | Defer change; retain configurable delta=1 baseline pending measured distribution. | S5 pinn §3.4; S6 review §4.4; S3 NS-13 | R1 §3.10; R2 NS-13; R3 §6.6; R4 NS-13; R5 NS-13; R6 NS-13; R7 NS-13 |
| DGR-15 | Adaptive topology | R1/R2/R3 preserve Stage 2/5 gold roles; R4 adopts 0–1 hierarchical/2–6 quasi topology; R5 incorrectly says source missing; R7 leaves topology open. | Use offline adaptive calibration within existing multi-fidelity topology; reject Table 4 wholesale. | S5 ctl stratification/Step 5; S6 stage_strat Table 4 | R1 §4; R2 adaptive; R3 §7; R4 adaptive; R5 adaptive; R7 adaptive |
| DGR-16 | Population safeguard | 5% in stage_strat versus >10% in issue/R4/R7. | Surface to owner; no value adopted. | S6 stage_strat Population Control; S3 adaptive method | R1 §4; R2 adaptive; R3 §7; R4 adaptive; R7 adaptive |
| DGR-17 | D correction consequence | R1/R2 say dead variable means no local numerical change; R3/R4/R5/R6 emphasize rederivation/recalibration; R7 identifies dead code but asks verification. | Attached pseudocode D/V are dead; external artifact provenance is unavailable, so no blanket claim about prior outputs. | S2 HC-6; S3 tau code; S5 ctl §2.5 | R1 §2.1; R2 D conflict; R3 §8.1; R4 D conflict; R5 D; R6 D; R7 D |
| DGR-18 | L_max interpretation | Several reports call it theoretical maximum; R3 narrows to characteristic normalization. | Retain formula but use characteristic-scale wording. | S5 ctl Step 3 item 2; S6 review §1.1 | R1 §2.2; R2 tau/Lmax; R3 §8.2; R4 tau/Lmax; R6 L_norm; R7 Lmax |
| DGR-19 | tau_L estimator | R1/R2/R3/R7 identify unresolved Rosenstein vs shadow; R4/R5/R6 canonize or add shadow/PCA paths. | Surface estimator choice; retain current Rosenstein baseline until decided; reject unspecified PCA shortcut and issue shadow code as normative. | S5 ctl Step 3 item 5; S3 tau code; S6 review §1.1 | R1 §2.2; R2 tau/Lmax; R3 §8.3; R4 tau/Lmax; R5 tau; R6 Lyapunov; R7 tau |
| DGR-20 | tau_L units | R2/R3 surface factor-of-T/time-axis ambiguity; other reports largely omit it. | Defer thresholds until estimator/time unit is explicit. | S5 ctl Step 3 item 5; S3 compute_tau_L | R2 tau/Lmax; R3 §8.1/8.3; R7 tau |
| DGR-21 | ALM clamp bounds | R1/R3/R7 defer exact bounds; R2/R4/R5/R6 adopt [1e-4,100] for P2. | No baseline clamp; optional only if update law exists; bounds deferred. | S5 pinn §4.2; S3 ALM update | R1 §5; R2 ALM; R3 §9; R4 ALM; R5 ALM; R6 ALM; R7 ALM |
| DGR-22 | Attachment availability | R5 says stage_strat missing; R6 says major S5/S6 material absent/truncated; both are false under the outer-section rule. | Reject missing-source claims; all outer S1–S6 sections were parsed and used. | S1 manifest/bundle rule; S5/S6 outer sections | R5 Registered Gaps; R6 Evidentiary Boundaries |

## 4. Gap register

No source-silent or ambiguous point below has been filled by invention.

| gap_id | topic | missing_or_ambiguous | final_disposition | resolution_needed | related_claim_ids |
|---|---|---|---|---|---|
| GAP-01 | Causal exponent clip | Numeric underflow clipping bound is unset. | defer | Owner/FUT sets bound if causal weighting remains. | CAU-05 |
| GAP-02 | Causal mode | No attached A/B/C ablation or executable Option-C window contract. | surface_to_user | Owner selects mode; future controlled comparison. | CAU-04 |
| GAP-03 | s_min frame | No sensitivity analysis for geometric versus softened stage gate. | surface_to_user | Owner selects frame; recompute changed stage labels if revisited. | SMIN-03 |
| GAP-04 | Static epsilon | No per-record invariant/stage sensitivity between eps_inv=1e-10 and 1e-5. | surface_to_user | Owner selects A/B; future comparison. | EPS-03,EPS-05 |
| GAP-05 | Replay edge cases | Absent/undersized next-stage pool, replacement, and final-stage policies are incomplete. | defer | Specify deterministic sampling policy. | B07-05 |
| GAP-06 | Collocation budget/mix | No validated 4096 budget or canonical continuous 50/50 mixed sampler. | defer | Compute-budget and sampler ablation. | B08-04,B08-05 |
| GAP-07 | L_norm storage | Raw-versus-clipped metadata policy and degenerate L_max handling are unresolved. | surface_to_user | Owner selects storage contract; audit admitted distribution. | M6-02,M6-03 |
| GAP-08 | Gradient clipping execution | Early-stage C, bootstrap floor, and history reset policy are unset. | defer | Stage-0 gradient trace calibration. | M14-03,M14-04 |
| GAP-09 | Energy dominance control | No coherent automatic safeguard rule or evidence. | defer | Log weighted losses/gradients before designing control. | M15-04 |
| GAP-10 | dt_out scaling | Objective, direction, caps, rounding, and fixed-compute budget are undefined. | defer | Compare constant and candidate policies at fixed compute. | M16-02,M16-03 |
| GAP-11 | Stage advancement | Whether a degraded checkpoint may advance after max epochs/stagnation is an owner decision. | surface_to_user | Define ADVANCE/RECOVER/HALT state machine. | D5-04 |
| GAP-12 | Transition constants | Percentile rule, thresholds, epoch table, stagnation and retry limits are unverified. | defer | Stage-0 pilot. | D5-05 |
| GAP-13 | Executable AD | Batched implementation/memory strategy remains FUT. | defer | Implement and run PHYS-02 acceptance checks. | NS12-03 |
| GAP-14 | Energy Huber delta | No normalized \|Delta H\| distribution or branch occupancy. | defer | Pilot-based calibration; retain baseline meanwhile. | NS13-02,NS13-03 |
| GAP-15 | Adaptive population | 5% versus >10% and cluster-count/stage mapping unresolved. | surface_to_user | Owner sets policy after admitted-set EDA. | ADAPT-04,ADAPT-07 |
| GAP-16 | Sampling scale s | Per-record s persistence/reconstruction is not established. | defer | Audit metadata; exclude Q_norm when s unavailable. | ADAPT-05 |
| GAP-17 | Prior D artifacts | Attachments do not establish whether any processed stores or thresholds used 6.694. | defer | Provide provenance or recompute only affected artifacts. | D-04 |
| GAP-18 | tau_L method/units | Canonical estimator, time unit, fit parameters, uncertainty flags, and threshold calibration are unresolved. | surface_to_user | Owner selects method; cross-calibrate representative sample. | TAUL-01,TAUL-03 |
| GAP-19 | Optional ALM | Scalar-constraint update law, normalization, state reset, and clamp sensitivity are unspecified. | defer | Specify ablation before choosing bounds. | ALM-02,ALM-03 |

## 5. Source-coverage checklist

All outer canonical sections and all reports were touched; no section was silently omitted.

| source_id | kind | contained_file_or_scope | status | use |
|---|---|---|---|---|
| S1 | canonical outer section | RESEARCH-CONTEXT-MASTER.md | touched | Authority hierarchy; bundle-reading rule; source-treatment preamble |
| S2 | canonical outer section | scope-12-hard-constraints.md | touched | Locked constraints; source override; revisable baseline |
| S2 | canonical outer section | framed-research-questions.md | touched | All 18 adjudication questions; explicit owner decisions |
| S2 | canonical outer section | resolution-doc-skeleton.md | touched | Coverage and downstream phase map only; non-binding |
| S3 | canonical outer section | 03-curriculum-and-training-loop.md | touched | Non-authoritative issue claims and candidate fixes |
| S4 | canonical outer section | claims-register.md | touched | Claim status and no-verification boundary |
| S4 | canonical outer section | verified-facts-reference.md | touched | Verified dt_out/snapshot/gold/D anchors |
| S4 | canonical outer section | consolidated-context.md | touched | Cross-check of verified and claimed dataset context |
| S5 | canonical outer section | ctl_instruction.md | touched | Primary curriculum/training-loop baseline |
| S5 | canonical outer section | pinn_architecture.md | touched | Primary loss/AD/optimization baseline |
| S5 | canonical outer section | sampling_method.md | touched | Sobol scale s and Q distortion for adaptive staging |
| S6 | canonical outer section | review_of_framework.md | touched | Baseline design intent; conflicts/anti-patterns assessed |
| S6 | canonical outer section | stage_strat_revision.md | touched | Adaptive-stage proposal; topology/population conflicts assessed |
| R1 | research report | all material sections | touched | Mapped in report_claim_crosswalk.csv |
| R2 | research report | all material sections | touched | Mapped in report_claim_crosswalk.csv |
| R3 | research report | all material sections | touched | Mapped in report_claim_crosswalk.csv |
| R4 | research report | all material sections | touched | Mapped in report_claim_crosswalk.csv |
| R5 | research report | all material sections | touched | Mapped in report_claim_crosswalk.csv; false missing-source claim registered |
| R6 | research report | all material sections | touched | Mapped in report_claim_crosswalk.csv; unsupported/missing-source claims registered |
| R7 | research report | all material sections | touched | Mapped in report_claim_crosswalk.csv |

## 6. Non-independent-input note

Apparent report synthesis and overlap were handled by **claim collapsing, not weighting**. Each report section was mapped to the independently frozen canonical ledger. Restatements of another report, shared wording, or a report that appeared to synthesize several others produced only another provenance entry for the same claim; they did not increase confidence or alter disposition. No inference was made about model identity, generation lineage, or report independence.

Dissent was retained even when isolated. Examples include R2/R4/R5/R6 support for the proposed `dt_base/dt_out` rule against the source-grounded deferral; R3’s minority ADVANCE/RECOVER/HALT distinction against reports that treated failure triggers as advancement; R3’s characteristic-scale interpretation of `L_max`; and R5/R6’s false claims that bundled source material was missing. These positions remain visible in the opposing-report column and disagreement register.

The canonical bundle’s outer-marker rule controlled source availability. `stage_strat_revision.md`, `pinn_architecture.md`, `sampling_method.md`, and the complete framed questions were present inside S5/S6; R5/R6 assertions that they were absent or truncated were therefore rejected. [Canonical: S1, “Uploaded File Manifest” and “Bundle Reading Rule.” Reports: R5 “Registered Gaps”; R6 “Evidentiary Boundaries and Tracked System Omissions.”]

## 7. Deliverable index

- `issue03-final-resolution.md` — this document.
- `issue03-claim-matrix.csv` — machine-readable 81-claim matrix.
- `issue03-disagreement-register.csv` — machine-readable conflict register.
- `issue03-gap-register.csv` — machine-readable gap register.
- `issue03-source-coverage-checklist.csv` — canonical/report coverage.
- `issue03-report-claim-crosswalk.csv` — 167 report-claim mappings used to verify R1–R7 coverage.
- `issue03-independent-source-ledger.csv` — frozen source-only ledger created before report review.
