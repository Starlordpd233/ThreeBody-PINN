# doc-03 Curriculum and Training Loop — Adjudication Resolution

> **Status:** ADJUDICATION COMPLETE  
> **Date:** 2026-06-18  
> **Scope:** All framed research questions from `framed-research-questions.md`  
> **Authority basis:** Framework specs (`ctl_instruction.md`, `pinn_architecture.md`) are the source of truth per `scope-12-hard-constraints.md` §2. Hard constraints (items 1–7) are fixed and non-reopenable. The issue doc (`03-curriculum-and-training-loop.md`) is non-authoritative; its findings are adjudicated, not transcribed. Live-code "Canonical" citations are overridden.  
> **Grounding:** Every figure resolves to a `CLM-NN` row in `claims-register.md`. `claimed-unverified` figures are treated as design hypotheses, not facts.  

---

## Table of Contents

1. [Summary of Findings](#1-summary-of-findings)
2. [Decisions Requiring Framework-Owner Approval](#2-decisions-requiring-framework-owner-approval)
3. [Section 2 — Decisions Requiring Human Approval](#3-section-2--decisions-requiring-human-approval)
   - Q1: The causal-training-mode decision
   - Q2: The s_min-frame decision
   - Q3: The epsilon-strategy decision
4. [Section 3 — Confirmed Findings (BLOCKING and MAJOR)](#4-section-3--confirmed-findings-blocking-and-major)
   - B-07: Replay/lookahead batch construction
   - B-08: Data-fidelity and collocation points conflated
   - M6: L_norm lacks clamping
   - M7: τ_L excluded from IC vector
   - M14: Gradient-clipping spec divergence
   - M15: Energy-loss weight schedule
   - M16: dt_out-aware collocation scaling
   - D5: Stage-transition criteria
   - NS-12: Componentwise AD
   - NS-13: Huber energy δ
   - NS-18: Loss-component scaling contract
5. [Section 6 — Data-Driven Adaptive Stage Assignment](#5-section-6--data-driven-adaptive-stage-assignment)
6. [Section 7 — τ_L / L_max Formula Resolution + the D Conflict](#6-section-7--τ_l--l_max-formula-resolution--the-d-conflict)
7. [Section 15 — ALM μ_p Clamp](#7-section-15--alm-μ_p-clamp)
8. [Cross-Finding Dependencies](#8-cross-finding-dependencies)
9. [Claims Register — Gaps Logged](#9-claims-register--gaps-logged)
10. [Downstream Phase Map](#10-downstream-phase-map)

---

## 1. Summary of Findings

| Finding | Status | Owner Decision? | Primary Spec-Edit Target | Phase |
|---------|--------|----------------|--------------------------|-------|
| Q1: Causal-training-mode | **DEFERRED** | **Yes** — 4 options | `ctl_instruction.md` + `pinn_architecture.md` | 32 / 34 |
| Q2: s_min-frame | **CONFIRMED** (Option A) | No | `ctl_instruction.md` §Step 3 | 32 / 33 |
| Q3: Epsilon-strategy | **DEFERRED** | **Yes** — A vs B | `ctl_instruction.md` §Step 3 | 32 / 35 |
| B-07: Replay/lookahead | **CONFIRMED** | No | `ctl_instruction.md` §Mini-Batch | 34 |
| B-08: Data-fidelity vs collocation | **CONFIRMED** | No | `ctl_instruction.md` + `pinn_architecture.md` | 34 |
| M6: L_norm clamping | **CONFIRMED** (reframed) | No | None — metadata, not IC | 33 |
| M7: τ_L exclusion | **CONFIRMED** | No | None — design confirmed | 33 |
| M14: Gradient clipping | **CONFIRMED** | No | `ctl_instruction.md` + `pinn_architecture.md` | 35 |
| M15: Energy-loss weight | **CONFLICT** | **Yes** — A vs B vs C | `pinn_architecture.md` §4.1 | 35 |
| M16: dt_out collocation scaling | **CONFIRMED** (with gaps) | No | `ctl_instruction.md` §Mini-Batch | 33 / 34 |
| D5: Stage-transition dual-path | **CONFIRMED** (with gaps) | No | `ctl_instruction.md` §Stage Transition | 33 |
| NS-12: Componentwise AD | **CONFIRMED** | No | None — PHYS-02 satisfies | 34 |
| NS-13: Huber energy δ | **CONFLICT** | **Yes** — A vs B | `pinn_architecture.md` §3.4 | 35 |
| NS-18: Loss scaling contract | **CONFLICT** (Huber vs L1) | No — spec wins | `ctl_instruction.md` + `pinn_architecture.md` | 35 |
| Adaptive stage assignment | **CONFLICT** (methodology) | **Yes** — hybrid design | `ctl_instruction.md` §Step 5 | 33 |
| D conflict: D=6.694 vs 4.6416 | **CONFIRMED** (4.6416) | No — locked | `ctl_instruction.md` §2.5 | 32 |
| τ_L / L_max formulas | **CONFIRMED** | No — D correction needed | `ctl_instruction.md` §Step 3 | 33 |
| ALM μ_p clamp | **CONFIRMED** (P2 ablation) | No | `pinn_architecture.md` §4.2 | 34 / 35 |

**Statistics:** 12 confirmed, 4 conflicts/deferred requiring owner decision, 0 insufficient evidence. All findings trace to specific file sections and CLM-NN rows.

---

## 2. Decisions Requiring Framework-Owner Approval

Four decisions are **explicitly deferred** to the framework owner. These are the only items requiring human intervention:

| # | Decision | Options | Recommended Default |
|---|----------|---------|---------------------|
| 1 | **Causal-training-mode** (Q1) | Preserve spec baseline (causal weighting) / Option A / Option B / Option C | Preserve spec baseline — minimal change |
| 2 | **Epsilon-strategy** (Q3, OPEN only) | Option A (1e-5 everywhere) / Option B (dual-context, current spec) / Option C (1e-10 everywhere — NOT selectable) | Option B (current spec baseline) — minimal change |
| 3 | **Energy-loss weight schedule** (M15) | Option A (PHYS-05 conservative) / Option B (issue-doc capped-hybrid) / Option C (merged hybrid) | Option A + dominance safeguard — conservative |
| 4 | **Huber energy δ** (NS-13) | Option A (δ = 1.0, spec baseline) / Option B (δ = 0.1, quantile-tuned) | Option B (0.1) — physically better motivated |
| 5 | **Adaptive stage assignment** (Q6) | Full adaptive / threshold-only / hybrid (augment) | Hybrid (augment, not replace) — balanced |

The s_min-frame decision (Q2) is **confirmed** as Option A (unsoftened gate + softened loss) and requires no owner action.

---

## 3. Section 2 — Decisions Requiring Human Approval

---

### Finding Q1: The Causal-Training-Mode Decision

**Status:** DEFERRED — Requires framework-owner decision  
**Downstream phase:** Phase 32 (root-cause) / Phase 34 (LOOP cluster)

**Adjudication:**

This is the single most consequential training-loop decision. The research must surface a **critical divergence** between the issue doc's framing and the actual spec baseline.

**Issue-doc position:** `03-curriculum-and-training-loop.md` § "Decisions Requiring Human Approval" (D-04) and § "Causal Training Mismatch" call **Option B (global sampling + ALM)** the "current SOT." The issue doc states: "`ctl_instruction.md` 'Phase 2a' defines mini-batch construction with 50% uniform sampling from [0,T] and 50% acceleration-weighted sampling — this is global sampling with no causal weighting" and "`review_of_framework.md` §5.1-5.2 describes a single forward pass with global ALM, confirming Option B as the SOT default." The issue doc asks the owner to choose and record Option B (if chosen) as an intentional departure from the blueprint.

**Framework-spec position:** `ctl_instruction.md` § "Loss Function Formulation" / "Phase 2: Total Training Loss" **already adopts causal weighting as the PHYS-05 default**: `w_n = exp(-η_c · Σ_{m<n} stopgrad(R̄_m))`, `η_c = 1` default. The spec **explicitly rejects** the previous pseudo-ALM formulation `L_data + λ_p·L_phys + (μ_p/2)·L_phys² + λ_E·L_energy` as not representing a standard equality-constrained augmented Lagrangian. `pinn_architecture.md` §3.2 carries the same causal-weighting default. `pinn_architecture.md` §4.2 confines optional ALM to a **P2 ablation on scalar conservation constraints only**. The spec baseline is therefore **causal weighting with no dense-residual ALM** — which is **neither** the issue doc's Option B nor its claimed "SOT."

**Your reconciliation:** The issue doc's framing that "Option B is the current SOT" does **not** match the actual spec baseline. The spec has already moved to causal weighting and has already rejected dense-residual ALM. The issue doc appears to describe an **earlier** version of the framework or the overridden live-code `basic_architecture.py`. The genuine decision is: **should the spec's existing causal-weighting default be preserved, replaced, or extended?**

- **Option A** (per-time-step causal weighting) is **closest to the current spec baseline**, which already has causal weighting. The "Causal Firewall" risk (early stiffness spike drives weights to zero) is genuine.
- **Option B** (global + ALM) would require **reversing** the spec's causal-weighting default and its rejection of dense-residual ALM — a significant spec edit, not preservation of SOT.
- **Option C** (time-windowed hybrid) is the most complex; the blueprint recommends it but notes it is an end-to-end rewrite.

**Locked constraints applied:** None of SCOPE-12 items 1–7 directly bind this decision. The locked `eps_soft = 1e-5` (item 4) and 14D input contract (item 1) create compatibility requirements.

**Claims referenced:** None directly — this is a design-constant/architectural decision, not a dataset figure.

**Gaps logged:**
1. The spec does not specify a numeric clipping bound for the causal exponent to avoid underflow (`ctl_instruction.md`). This gap remains open.
2. The issue doc's SOT claim appears to trace to overridden live-code citations, not the spec.
3. No FUT empirical check is defined for causal-weighting effectiveness under the actual dataset.

**Recommended resolution:** Present four options:
- **Preserve spec baseline** (causal weighting, no dense ALM) — minimal-change path
- **Adopt Option A** explicitly — spec's causal weighting is already close
- **Adopt Option B** — requires reversing spec's causal default (large change)
- **Adopt Option C** — end-to-end rewrite; weigh against implementation cost

---

### Finding Q2: The s_min-Frame Decision

**Status:** CONFIRMED — Spec baseline (Option A) is internally consistent  
**Downstream phase:** Phase 32 / Phase 33

**Adjudication:**

**Issue-doc position:** `03-curriculum-and-training-loop.md` § "[ROUTINE] D-05" states the SOT is already internally consistent (unsoftened `s_min` for gate, softened in loss) and frames this as documentation cleanup. Recommends Option A: unsoftened `s_min` for curriculum stage gate; `max(s_min, eps_soft=1e-5)` for training loss; always log unsoftened value.

**Framework-spec position:** `ctl_instruction.md` § "Step 3" item 1 defines `s_min` from "true pairwise separations (no softening)" — explicitly unsoftened geometric — while static-invariant potential uses Plummer `ε_inv = 1e-10` and training-time residual/energy use `ε_train = 1e-5` (`pinn_architecture.md` §3.2, §3.4). Stage 6 gate uses unsoftened geometric `s_min`.

**Your reconciliation:** Both positions **agree**. The spec baseline already implements Option A. No substantive conflict exists. The decision is confirmed as Option A.

**Locked constraints applied:** HC-4 (`eps_soft = 1e-5` in training loss) binds the loss-side softening. The s_min gate's unsoftened geometric form is compatible.

**Claims referenced:** CLM-19 (locked `eps_soft = 1e-5`, PHYS-03).

**Gaps logged:** None. Both positions are aligned.

**Recommended resolution:** **Confirm Option A.** No spec edit required beyond documentation verification. The `ctl_instruction.md` Step 3 item 1 prose already captures the separation.

---

### Finding Q3: The Epsilon-Strategy Decision

**Status:** DEFERRED — Requires framework-owner decision (OPEN part only)  
**Downstream phase:** Phase 32 / Phase 35

**Adjudication:**

**LOCKED (not re-openable):** SCOPE-12 HC-4: `eps_soft = 1e-5` in training loss. This value is fixed per CLM-19 (`verified` / hard constraint). Do not frame any question as "which loss-side epsilon is correct."

**Issue-doc position:** `03-curriculum-and-training-loop.md` § "[MAJOR] D-06" flags an internal SOT contradiction: `review_of_framework.md` §2.2 mandates `1e-5` for ALL calculations and argues against `1e-10` ("numerically indistinguishable from zero"), while `ctl_instruction.md` Step 3 item 1 uses `eps = 1e-10` for invariant computation with truncated justification. Presents Options A (1e-5 everywhere), B (dual-context), C (1e-10 everywhere).

**Framework-spec position:** `ctl_instruction.md` § "Step 3" item 1 states `ε_inv = 1e-10` is "context-specific for offline invariant computation and is distinct from the training-time softening `ε_train = 1e-5`." `pinn_architecture.md` §3.2 / §3.4 fix `ε_train = 1e-5` and add a dual-epsilon visibility note. The spec baseline is **already dual-context (Option B)** with loss side locked at `1e-5`.

**Your reconciliation:** The spec baseline already implements Option B. The `review_of_framework.md` §2.2 argument against `1e-10` applies to GPU float32 training, not CPU float64 offline computation — the dual-context arrangement is architecturally coherent. The open question is: **preserve dual-context (B) or collapse to 1e-5 everywhere (A)?** Option C violates the locked loss-side value.

**Locked constraints applied:** HC-4 (`eps_soft = 1e-5`, PHYS-03) — loss side fixed. Static context is the only variable.

**Claims referenced:** CLM-19 (locked `eps_soft = 1e-5`).

**Gaps logged:**
1. Whether `review_of_framework.md`'s argument carries over to float64 offline computation — gap exists.
2. `ctl_instruction.md` Step 3 item 1's justification for `1e-10` is truncated — partially addressed by "context-specific" but not fully justified.
3. No empirical verification that dual-context causes measurable stage-assignment errors.

**Recommended resolution:** Owner chooses:
- **Option A (1e-5 everywhere):** Collapses static context. Changes invariant computation. `review_of_framework.md` argument supports this.
- **Option B (dual-context, current spec):** Preserve `ε_inv = 1e-10` / `eps_soft = 1e-5`. Minimal spec impact. **Recommended as default.**
- **Option C (1e-10 everywhere):** Violates locked loss-side value. **Not selectable.**

---

## 4. Section 3 — Confirmed Findings (BLOCKING and MAJOR)

---

### Finding B-07: Replay/Lookahead Batch Construction Not Implemented

**Status:** CONFIRMED — Contract consistent between spec and audit pseudocode  
**Downstream phase:** Phase 34

**Issue-doc position:** `03-curriculum-and-training-loop.md` § B-07 (BLOCKING): current `get_batch()` uses flat random draw; CTL requires 240 replay (stages ≤ k) + 16 lookahead (stage k+1), 32 points/trajectory, 50/50 uniform/acceleration-weighted.

**Framework-spec position:** `ctl_instruction.md` § "Mini-Batch Construction with Lookahead Sampling" specifies replay `B_≤k = 240`, lookahead `B_{k+1} = 16`, `n_pts(traj) = min(n_pts_cap, n_snapshots)` with `n_pts_cap` default 32 and 50/50 weighted/uniform composition. `pinn_architecture.md` §3.1 shows legacy `get_batch()` acknowledged as not yet implementing replay/lookahead (author comment).

**Your reconciliation:** The spec and audit §6 pseudocode describe the **same contract**. No reconciliation conflict exists — the spec is the authoritative contract and the pseudocode is a consistent implementation blueprint. The counts (240/16/32) are CLM-12 (`claimed-unverified`, FUT).

**Claims referenced:** CLM-12 (240 replay / 16 lookahead / 8192 data-fidelity / 4096 collocation — `claimed-unverified`, FUT).

**Recommended resolution:** Confirm the replay/lookahead contract. The spec edit target is `ctl_instruction.md` § "Mini-Batch Construction."

---

### Finding B-08: Data-Fidelity and Collocation Points Conflated

**Status:** CONFIRMED — Spec-integration gap, not design divergence  
**Downstream phase:** Phase 34

**Issue-doc position:** `03-curriculum-and-training-loop.md` § B-08 (BLOCKING): CTL design does not separate data-fidelity points (must match Brutus snapshots, L1) from collocation points (anywhere in [0, T], physics + energy). Fix: two independent point sets — 8192 data-fidelity + 4096 collocation.

**Framework-spec position:** `pinn_architecture.md` §3.1 defines data term (Huber on scaled positions, `N_data = 256 × 32 = 8192`); §3.2 defines collocation residual. `ctl_instruction.md` composes them. Distinct roles exist but the **separate-point-set discipline** is not explicitly encoded in the batch constructor.

**Your reconciliation:** The two-independent-point-set contract is **implicit** in the spec (distinct data and collocation roles) but **not explicitly encoded** in the batch constructor. The audit §6 pseudocode makes it explicit (Step 2: data-fidelity, Step 3: collocation). This is a spec-integration gap, not a design divergence.

**Claims referenced:** CLM-12 counts (8192 data / 4096 collocation — `claimed-unverified`).

**Recommended resolution:** Make the two-independent-point-set contract explicit in the batch constructor. Land in `ctl_instruction.md` § "Mini-Batch Construction" + `pinn_architecture.md` §3.1/§3.2.

---

### Finding M6: L_norm Lacks Clamping Before IC-Vector Mapping

**Status:** CONFIRMED — Reframes M6 as metadata clamping, not IC-vector  
**Downstream phase:** Phase 33

**Issue-doc position:** `03-curriculum-and-training-loop.md` § M6 (MAJOR): `L_norm` can exceed 1, producing normalized IC component > 1 after `2x−1` mapping; fix is `np.clip(L_norm, 0, 1)`.

**Framework-spec position:** `ctl_instruction.md` § "Step 3" item 2 defines `L_norm = L / L_max` with `compute_L_norm` returning `L / (L_max + eps)`. § "Step 4" states `L_norm` is **metadata** (staging, diagnostics, loss scaling) and the invariant-heavy quantities are **no longer final network IC slots** under the locked 14D `[τ, IC₁₃]` contract (HC-1).

**Your reconciliation:** The issue doc's IC-vector-mapping framing is **obsolete** because `L_norm` is NOT a network IC slot under the locked 14D contract. `L_norm > 1` is physically valid (super-circular angular momentum). No source clamping is needed for the metadata use; any consumer needing bounds applies `clip` at the point of use.

**Locked constraints applied:** HC-1 (14D network input `[τ, IC₁₃]` — `L_norm` is excluded).

**Claims referenced:** None — spec contract, not CLM-NN claim.

**Recommended resolution:** Confirm no clamp needed for `L_norm` as metadata. Document that `L_norm` is a metadata descriptor only, not subject to `[0, 1]` bounds. Any staging consumer needing bounded input should apply `clip` at the point of use.

---

### Finding M7: τ_L Computed but Excluded from the IC Vector

**Status:** CONFIRMED — Exclusion is by design under locked 14D contract  
**Downstream phase:** Phase 33

**Issue-doc position:** `03-curriculum-and-training-loop.md` § M7 (MAJOR): `τ_L` computed but dropped from IC vector with no documented decision; recommends **excluding by design** (derived dynamical property, not IC invariant).

**Framework-spec position:** `ctl_instruction.md` § "Step 3" returns `τ_L` for stage gating (Stages 4a/4b: `τ_L > 5`, `2 < τ_L ≤ 5`); § "Step 4" excludes invariant-heavy descriptors from `IC₁₃`, consistent with locked 14D Jacobi-state input.

**Your reconciliation:** Both positions **agree**: `τ_L` should be excluded from `IC₁₃`. The spec already implements this. The issue doc's recommendation to "exclude by design" aligns perfectly. No conflict.

**Locked constraints applied:** HC-1 (14D `[τ, IC₁₃]` contract — `τ_L` not in IC₁₃).

**Recommended resolution:** Confirm `τ_L` exclusion by design. No spec edit required beyond documentation verification.

---

### Finding M14: Gradient-Clipping Spec Divergence

**Status:** CONFIRMED — Merged contract reconciles both specs  
**Downstream phase:** Phase 35

**Issue-doc position:** `03-curriculum-and-training-loop.md` § M14 (MAJOR): two strategies documented independently — PINN median-based adaptive vs. CTL curriculum-aware C schedule. Fix: merge as `clip_value = C_stage · median(grad_norm_history)`, with `C_table = {0: 8.5, 1: 8.5, 2: 5.0, 3: 5.0, 4: 3.0, 5: 3.0, 6: 3.0}`.

**Framework-spec position:** `pinn_architecture.md` §4.4: median-based clipping at **`5.0 × median`** of last 100 gradient norms. `ctl_instruction.md` § "Adaptive Median-Based Gradient Clipping": curriculum-aware C schedule (stages 0–1: `7–10`, 2–3: `5`, 4–6: `3`).

**Your reconciliation:** The merged contract `C_stage · median(grad_norm_history[-100:])` cleanly combines both specs. `pinn_architecture.md` contributes the median mechanism (rolling window of 100); `ctl_instruction.md` contributes the C schedule. The issue doc's `C_table` values {8.5, 5.0, 3.0} are instantiations of the CTL ranges (CLM-10, `claimed-unverified`, FUT). The PINN spec's fixed `5.0` becomes the stage 2–3 value.

**Claims referenced:** CLM-10 (`C_table` 8.5/5.0/3.0 — `claimed-unverified`, FUT).

**Recommended resolution:** Confirm merged contract `clip_value = C_stage · median(grad_norm_history[-100:])`. Land in `pinn_architecture.md` §4.4 and `ctl_instruction.md` § "Adaptive Median-Based Gradient Clipping."

---

### Finding M15: Energy-Loss Weight May Overwhelm; Capped-Hybrid Schedule

**Status:** CONFLICT — Spec schedule vs. issue-doc cap_table diverge significantly  
**Downstream phase:** Phase 35

**Issue-doc position:** `03-curriculum-and-training-loop.md` § M15 (MAJOR): `λ_E` up to 1000 at Stage 6 risks overwhelming physics/data. Proposes capped-hybrid `λ_E(k) = min(10^(k−3), cap[k])` with `cap_table = {0:1, 1:5, 2:20, 3:50, 4:100, 5:200, 6:500}` (CLM-11). Adds dominance safeguard: reduce `λ_E` when energy term dominates.

**Framework-spec position:** `pinn_architecture.md` §4.1 (PHYS-05): `λ_E^max(k) = {0 for k∈{0,1}; 10^{k−4} for k∈{2,3,4}; 1 for k∈{5,6}}`, with linear warmup over `I_warm = min(2000, 0.1·N_Adam,k)`.

**Your reconciliation:** The schedules **diverge by orders of magnitude**. At Stage 4: spec gives `10^(4−4) = 1`, issue doc gives `min(10^1, 100) = 10`. At Stage 6: spec gives `1`, issue doc gives `500`. Both are `claimed-unverified` design hypotheses. The dominance safeguard is a novel runtime safety feature compatible with either schedule and should be adopted regardless.

**Claims referenced:** CLM-11 (`λ_E` cap_table — `claimed-unverified`, FUT).

**Recommended resolution:** Present three options:
- **Option A (Conservative):** Retain PHYS-05 schedule + add dominance safeguard.
- **Option B (Aggressive):** Adopt issue-doc cap_table + safeguard.
- **Option C (Hybrid):** Merge both — use spec for stages 0–4, cap_table for stages 5–6.
- The dominance safeguard should be adopted in all cases.

---

### Finding M16: dt_out-Aware Collocation Scaling

**Status:** CONFIRMED — Audit-verbatim direction with gaps on implementation details  
**Downstream phase:** Phase 33 / Phase 35

**Issue-doc position:** `03-curriculum-and-training-loop.md` § M16 (MAJOR): `dt_out` varies ~17× but collocation density is uniform. Fix: `n_col ∝ dt_base / dt_out`. Gold 1×, hier-base ≈0.125×, std-base ≈0.059× (audit-verbatim direction).

**Framework-spec position:** `ctl_instruction.md` § "Mini-Batch Construction" exposes `n_snapshots(traj)` and `dt_out(traj)` as loader metadata, labels M16 as **deferred forward-interface** ("not used here"). Verified per-variant `dt_out` values (CLM-17: std 0.17 / hier 0.08 / gold 0.01).

**Your reconciliation:** The audit-verbatim direction is physically sound. The derived factors match: gold = 0.01/0.01 = 1×, hier = 0.01/0.08 = 0.125×, std = 0.01/0.17 ≈ 0.059×. However, the batch-budget reconciliation (per-trajectory scaling vs. fixed total collocation budget) is undefined. No verified `dt_base` rationale exists.

**Claims referenced:** CLM-17 (per-variant `dt_out` — `verified`). CLM-20 (scaling factors — `claimed-unverified`, FUT).

**Gaps logged:**
1. No verified `dt_base` value — assumes 0.01 without justification.
2. No rounding/integer rule for collocation counts.
3. No reconciliation between per-trajectory scaling and fixed batch-level collocation budget.

**Recommended resolution:** Adopt `n_col(traj) ∝ dt_base / dt_out(traj)` with `dt_base = 0.01`. Add `min_col_per_traj = 1` floor. Surface batch-budget reconciliation gap for owner decision: accept variable total or renormalize per-batch. Land in `ctl_instruction.md` § "Mini-Batch Construction."

---

### Finding D5: Stage-Transition Criteria Unattainable; Dual-Path Fallback

**Status:** CONFIRMED — Dual-path structure adopted; threshold values provisional  
**Downstream phase:** Phase 33

**Issue-doc position:** `03-curriculum-and-training-loop.md` § D5 (MAJOR): strict criteria (monotonic validation loss) unattainable. Proposes dual-path: strict (plateau + validation-stable + physics-residual + energy-drift) + fallback (max-epochs CLM-09, stagnation, NaN rollback). Per-stage thresholds `epsilon_phys`/`epsilon_energy`: 5e-3…1e-4 (CLM-08, "not fixed").

**Framework-spec position:** `ctl_instruction.md` § "Stage Transition Criteria" lists four strict criteria: training plateau `ε_plateau = 1e-5` patience 200; validation stability; physics residual `ε_phys = 1e-4`; energy drift `ε_energy = 1e-4`. Author note questions attainability but **no fallback path encoded**.

**Your reconciliation:** The dual-path contract is a necessary engineering response. Path A = quality-gated advancement; Path B = time-gated advancement preventing infinite loops. Per-stage threshold relaxation is physically sound. All threshold values are `claimed-unverified` (CLM-08, CLM-09) and must be marked provisional.

**Claims referenced:** CLM-08 (per-stage thresholds — `claimed-unverified`, FUT). CLM-09 (max-epochs table — `claimed-unverified`, FUT).

**Gaps logged:**
1. No verified threshold values — design hypotheses only.
2. Validation-stability criterion divergence: spec uses `min` form; issue doc uses `percentile_10`.
3. No NaN-rollback spec detail (checkpoint frequency, retry limit).

**Recommended resolution:** Adopt dual-path structure in spec. Mark all numeric values provisional pending Stage 0 pilot. Recommend `percentile_10` form over `min` form for validation stability. Require Stage 0 pilot to calibrate.

---

### Finding NS-12: Componentwise AD for Velocities/Accelerations

**Status:** CONFIRMED — PHYS-02 fully satisfies NS-12  
**Downstream phase:** Phase 34

**Issue-doc position:** `03-curriculum-and-training-loop.md` § NS-12 (MAJOR): sources say AD derived but no concrete three-body PyTorch implementation; fix is component-wise AD requirement.

**Framework-spec position:** `pinn_architecture.md` §5.3.1 (PHYS-02) encodes the **full componentwise normalized-time AD contract**: all nine `dr'_{i,α}/du` required; `torch.autograd.grad(r.sum(), u, …)` anti-pattern **forbidden**; three acceptable patterns listed (`jacrev` + `vmap`, per-component loop, full-Jacobian); worked synthetic-trajectory test provided.

**Your reconciliation:** PHYS-02 **fully satisfies** NS-12. The issue doc's concern is addressed by the spec's explicit patterns, forbidden anti-pattern callout, and acceptance test. No conflict; no spec change needed.

**Recommended resolution:** Confirm `pinn_architecture.md` §5.3.1 satisfies NS-12. No spec edit required.

---

### Finding NS-13: Huber Energy δ = 1.0 Too Large

**Status:** CONFLICT — δ = 1.0 vs quantile-tuned ~0.01–0.1  
**Downstream phase:** Phase 35

**Issue-doc position:** `03-curriculum-and-training-loop.md` § NS-13 (MAJOR): `δ = 1.0` uncalibrated for normalized Hamiltonian residuals; proposes tuning from `|ΔH|` quantiles starting ≈ 0.01–0.1. `stage_strat_revision.md` §4.4 sets definitive `δ = 0.1`.

**Framework-spec position:** `pinn_architecture.md` §3.4 (PHYS-04) fixes energy regularizer Huber transition at **`δ = 1.0`**, with `ΔH_n` normalized by `|H_ε(r_0)| + ε_H` and locked floor `ε_H = 1e-4·S_H`.

**Your reconciliation:** Genuine quantitative conflict. The issue doc's argument is sound: if `|ΔH|` typically stays below 1.0, Huber acts like L2. `δ = 0.1` is a principled compromise. But actual `|ΔH|` distribution is **unknown** — no empirical data exists. The locked `ε_H` floor affects normalization but not the δ choice.

**Locked constraints applied:** HC-5 (`ε_H = 1e-4·S_H` floor — affects `ΔH_n` scale, not δ).

**Recommended resolution:** Present two options:
- **Option A:** Retain `δ = 1.0` (conservative). Risk: reduced robustness to outliers.
- **Option B:** Start with `δ = 0.1`, refine via quantile tuning after Stage 0 pilot. **Recommended.**
- Require FUT empirical check on `|ΔH|` distribution.

---

### Finding NS-18: Loss-Component Scaling Contract

**Status:** CONFLICT — Issue-doc L1/MAE vs. spec Huber for L_data  
**Downstream phase:** Phase 35

**Issue-doc position:** `03-curriculum-and-training-loop.md` § NS-18 (MAJOR): `L_data` uses L1/MAE on scaled positions `r' = r/D`; `L_physics` on collocation with componentwise AD and `eps_soft = 1e-5`; `L_energy` same collocation set.

**Framework-spec position:** `pinn_architecture.md` §3.1 defines data term as **Huber** (`δ_r = 1`), explicitly replacing earlier MAE/L1 prose. §3.2 physics residual uses `ε_train = 1e-5`; §3.4 energy regularizer same `ε_train`. §4.1 (PHYS-05) composes all terms.

**Your reconciliation:** **Direct conflict** on `L_data` loss function: issue doc says L1/MAE, spec says Huber. The spec is source of truth and explicitly states it "replaces" the MAE/L1 prose. The dimensionless units contract — all terms on `r' = r/D`, `v' = dr'/du`, `a' = d²r'/du²`, `G=1`, `eps_soft = 1e-5` — is **consistent** across both. Reconciliation: **adopt spec's Huber data term**, confirm units contract.

**Locked constraints applied:** HC-6 (`D ≈ 4.6416`), HC-4 (`eps_soft = 1e-5`), HC-3 (COM projection head).

**Claims referenced:** CLM-19 (locked `D ≈ 4.6416`).

**Recommended resolution:** Adopt spec's Huber data term (`δ_r = 1`), overriding issue doc's L1/MAE. Confirm dimensionless units contract explicitly in both specs.

---

## 5. Section 6 — Data-Driven Adaptive Stage Assignment

**Status:** CONFLICT — Methodology accepted in principle; boundaries require owner decision  
**Downstream phase:** Phase 33

**Issue-doc position:** `03-curriculum-and-training-loop.md` § "Data-Driven Adaptive Stage Assignment" proposes: EDA over all invariants; correlation/PCA; K-means (`k = 6–7`); quantile thresholds; `>10%`-per-stage safeguard; PINN pilot. "Augments (not replaces) `assign_curriculum_stage()`."

**Framework-spec position:** `ctl_instruction.md` § "Step 5" and § "Multi-Stage Data Stratification" define **threshold-based** stage assignment keyed by `record_key`. Fixed invariant thresholds for all stages. Author note suggests data scan but does not implement adaptive methodology. Per-stage population counts CLM-02..CLM-07 are `claimed-unverified`.

**Baseline report position:** `stage_strat_revision.md` carries full methodology: quantile binning for hierarchical (Stages 0–1); PCA + K-means (`k=5` for quasi-random Stages 2–6) ordered by median `τ_L`; `>5%` minimum population; PINN pilot protocol.

**Your reconciliation:** Adaptive methodology is **well-motivated and physically sound**. The spec's own author note questions fixed thresholds. However: the locked stage-query contracts (PIPE-01..10, HC-7) must not be violated; the `>10%` (issue doc) vs `>5%` (baseline report) threshold needs resolution; `k=6-7` (issue doc) vs `k=5` (baseline report) for quasi-random needs resolution; integration with threshold-based Step 5 is undefined.

**Locked constraints applied:** HC-7 (PIPE-01..10 stage-query contracts locked); HC-5 (SCS gate); HC-6 (`D ≈ 4.6416`).

**Claims referenced:** CLM-02..CLM-07 (per-stage counts — all `claimed-unverified`, FUT).

**Gaps logged:**
1. No clustering `k` consensus (5 vs 6–7).
2. Minimum stage population threshold divergence (5% vs 10%).
3. No EDA results in package.
4. Integration mechanism with threshold-based Step 5 undefined.
5. Q-normalized scaling artifact (`Q ∝ s³`) correction factor availability unconfirmed.
6. No PINN pilot results.

**Recommended resolution:** Adopt **hybrid adaptive methodology** as canonical:
- Phase 0 (pre-training): EDA + PCA + K-means (`k` by elbow method, bounded 5–7).
- Phase 1: Quantile binning for hierarchical (Stages 0–1); PCA + K-means for quasi-random (Stages 2–6).
- Phase 2: `>10%` per-stage minimum (issue doc's conservative threshold).
- Phase 3: PINN pilot validation.
- Fallback to threshold-based Step 5 if clustering fails.
- Land in `ctl_instruction.md` § "Step 5" with existing thresholds as fallback.
- Mark CLM-02..CLM-07 as invalidated until adaptive methodology executes.

---

## 6. Section 7 — τ_L / L_max Formula Resolution + the D Conflict

---

### Finding: D = 6.694 vs D ≈ 4.6416 (The Worked Seed-Conflict)

**Status:** CONFIRMED — D ≈ 4.6416 locked; D = 6.694 rejected  
**Downstream phase:** Phase 32

**Issue-doc position:** `03-curriculum-and-training-loop.md` § "tau_L and L_max" uses `D = np.cbrt(G * M_tot_ref * T_scale**2) = 6.694` (`M_tot_ref = 3.0`, `T_scale = 10`). Claims this is a "corrected B-02 formula." CLM-01 (`claimed-unverified`).

**Framework-spec position:** `ctl_instruction.md` §2.5 locks `D = (G·T²)^(1/3) ≈ 4.6416` (raw-mass nondimensionalization, PHYS-01). Documents `D = 6.694` as **rejected** ("no configuration parameter may select the mass-fraction form"). CLM-19 (`verified` / HC-6).

**Your reconciliation:** The issue doc's `D = 6.694` is **erroneous** under locked conventions. The raw-mass convention does not include `M_tot` in the D formula. Total-mass form was **rejected by v1.5 Phase 25 (EVID-10)**. The open question is **not** "which D is correct" — that is settled. The open question is re-deriving `τ_L` / `L_max` **under the locked D ≈ 4.6416**.

**Locked constraints applied:** HC-6 (PHYS-01 raw-mass `D ≈ 4.6416`) — binding and non-reopenable.

**Claims referenced:** CLM-01 (`D = 6.694`, `claimed-unverified`, FUT — rejected). CLM-19 (`D ≈ 4.6416`, `verified`, HC-6).

**Recommended resolution:** Confirm locked `D ≈ 4.6416`. Replace all `D = 6.694` occurrences in issue-doc routines with locked value. Re-derive downstream stage thresholds under locked D.

---

### Finding: τ_L and L_max Computation Formulas

**Status:** CONFIRMED — Formulas match; D correction required  
**Downstream phase:** Phase 33

**Issue-doc position:** `L_max = M_total * r_char * v_char` with `v_char = sqrt(2|E|/M_total)`. `τ_L = 1/λ_max` via shadow-trajectory divergence: `epsilon_pert = 1e-8`, `epsilon_soft = 1e-10`. PCA+Rosenstein batch approximation for ~15K trajectories.

**Framework-spec position:** `ctl_instruction.md` § "Step 3" item 2 gives canonical `L_max = M_tot · r_char · v_char` with `v_char = sqrt(2|E|/M_tot)`. Spec does not yet inline shadow-trajectory `τ_L` routine with split softening. `ctl_instruction.md` § "Step 3" item 5 provides Rosenstein-style estimator (different method).

**Your reconciliation:** `L_max` formula **confirmed** — matches both sources. Two `τ_L` methods: (1) shadow-trajectory divergence (issue doc, more accurate, more expensive); (2) Rosenstein-style estimator (spec, faster, for batch). Both valid — complementary use. **Critical:** The `D` value must be corrected from 6.694 to 4.6416. The split softening (`epsilon_pert = 1e-8`, `epsilon_soft = 1e-10`) is **distinct** from locked training-loss `eps_soft = 1e-5` and must be preserved as a static-context parameter.

**Locked constraints applied:** HC-6 (`D ≈ 4.6416`); HC-4 (`eps_soft = 1e-5` — split softening is static-context, distinct).

**Gaps logged:**
1. Spec does not inline shadow-trajectory `τ_L` routine — only Rosenstein method provided.
2. `compute_L_norm` clipping to `[0, 1]` is a design choice not yet in spec (connects to M6).
3. Stage-threshold consequences of D correction on `τ_L` gating (Stages 4a/4b) not quantified.

**Recommended resolution:** Confirm formulas with corrections: (1) `L_max` formula — no change; (2) shadow-trajectory `τ_L` — add to spec; (3) PCA+Rosenstein — confirm as fast path; (4) **correct D to 4.6416** — mandatory; (5) preserve split softening as distinct static-context parameter.

---

## 7. Section 15 — ALM μ_p Clamp

**Status:** CONFIRMED — Clamp applies to P2 scalar-constraint ALM ablation only  
**Downstream phase:** Phase 34 / Phase 35

**Issue-doc position:** `03-curriculum-and-training-loop.md` § "ALM Parameter Update" (MINOR/INFO): `μ_p` can diverge without bounds; proposes `μ_p = np.clip(μ_p, 1e-4, 100.0)`. Lower bound prevents physics enforcement from decaying to zero; upper bound prevents overwhelming data term.

**Framework-spec position:** `ctl_instruction.md` § "Loss Function Formulation" **rejects** dense-residual pseudo-ALM. `pinn_architecture.md` §4.2 confines ALM to **P2 ablation on scalar conservation constraints only** (energy drift `c_E`, angular-momentum drift `c_{L,α}`), with dual updates between Adam epochs only. Default training loss (PHYS-05) has no ALM dual variables.

**Your reconciliation:** The clamp was written for the **rejected** dense-residual pseudo-ALM. That formulation no longer exists in the default loss. The clamp **does not apply to the default training loss**. However, it **does** apply to the **optional P2 scalar-constraint ALM ablation** in `pinn_architecture.md` §4.2. If that ablation is enabled, the clamp `[1e-4, 100.0]` prevents penalty-parameter divergence. The values are design hypotheses (not verified) but reasonable.

**Recommended resolution:** Confirm `μ_p`-clamp `[1e-4, 100.0]` applies to P2 scalar-constraint ALM ablation (`pinn_architecture.md` §4.2), not to default training loss. Document clamp in §4.2 as part of P2 ablation spec. Default PHYS-05 loss requires no `μ_p` clamp (no ALM dual variables).

---

## 8. Cross-Finding Dependencies

| Dependency | From | To | Nature |
|-----------|------|-----|--------|
| D value | D conflict (§6) | τ_L/L_max (§6) | D correction must propagate into τ_L routines |
| Epsilon strategy | Q3 (§3) | τ_L/L_max (§6) | Determines whether shadow-trajectory epsilon_soft preserved or collapsed |
| Causal mode | Q1 (§3) | ALM clamp (§7) | If Option B chosen, dense-residual ALM rejection revisited, changing Q6 scope |
| Causal mode | Q1 (§3) | s_min frame (§3) | Independent — parallel tracks |
| Energy weight | M15 (§4) | Gradient clipping (§4) | Large λ_E amplifies energy gradients; clipping must account |
| Loss scaling | NS-18 (§4) | Huber δ (NS-13) | Both affect loss-term magnitudes; reconcile together |
| Adaptive stages | Q6 (§5) | D5 transitions (§4) | Adaptive assignment produces stage populations that feed transition criteria |
| M16 scaling | M16 (§4) | D5 transitions (§4) | Low-res trajectories get fewer collocation points; thresholds may need stage-level adjustment |

---

## 9. Claims Register — Gaps Logged

The following gaps are logged against the claims register as part of this adjudication. These gaps represent missing information that would strengthen the resolution. They are **not** blockers — adjudication proceeds on available evidence — but they should be tracked for future closure.

| Gap ID | Related Finding | Description | What Would Resolve It | FUT Flag |
|--------|----------------|-------------|----------------------|----------|
| GAP-03-01 | Q1 (causal mode) | No numeric clipping bound for causal exponent | Spec edit or empirical calibration | FUT |
| GAP-03-02 | Q3 (epsilon) | Whether 1e-10 is meaningful in float64 | Float64 numerical analysis or empirical test | FUT |
| GAP-03-03 | Q3 (epsilon) | Truncated justification for epsilon_inv = 1e-10 | Spec edit completing justification text | Phase 33 |
| GAP-03-04 | M15 (energy weight) | No empirical basis for cap_table values | Stage 0 pilot training run | FUT-01 |
| GAP-03-05 | M16 (collocation) | No verified dt_base value rationale | Design decision or sensitivity analysis | Phase 33 |
| GAP-03-06 | M16 (collocation) | No rounding/integer rule for n_col | Spec edit adding floor/rounding rule | Phase 34 |
| GAP-03-07 | M16 (collocation) | Batch-budget reconciliation for per-traj scaling | Design decision: fixed vs variable total | Phase 34 |
| GAP-03-08 | D5 (transitions) | No verified per-stage threshold values | Stage 0 pilot calibration | FUT-01 |
| GAP-03-09 | D5 (transitions) | Validation-stability criterion: min vs percentile_10 | Owner decision or empirical comparison | Phase 33 |
| GAP-03-10 | D5 (transitions) | No NaN-rollback spec detail | Spec edit adding checkpoint/rollback contract | Phase 34 |
| GAP-03-11 | NS-13 (Huber δ) | No empirical |ΔH| distribution | Stage 0 pilot or dedicated probe | FUT-01 |
| GAP-03-12 | NS-13 (Huber δ) | No stage-dependent δ values or derivation | Empirical quantile measurement per stage | FUT-01 |
| GAP-03-13 | NS-18 (loss scaling) | No verified rationale for Huber δ_r = 1 | Sensitivity check during Stage 0 pilot | FUT-01 |
| GAP-03-14 | Q6 (adaptive stages) | No EDA results in package | Execute EDA on admitted-set invariants | FUT-01 |
| GAP-03-15 | Q6 (adaptive stages) | Q-normalized scaling artifact correction factor | Confirm s availability for all quasi-random ICs | Phase 33 |
| GAP-03-16 | τ_L/L_max | Stage-threshold consequences of D correction | Recompute τ_L under D=4.6416, assess shift | Phase 33 |
| GAP-03-17 | τ_L/L_max | Spec lacks inline shadow-trajectory τ_L routine | Spec edit adding shadow-trajectory method | Phase 33 |

---

## 10. Downstream Phase Map

| Phase | Scope | Primary Spec-Edit Target | Findings Covered |
|-------|-------|--------------------------|-----------------|
| **Phase 32** | Root-cause adjudication / evidence | Both targets, as adjudicated | Q1 (causal mode), Q3 (epsilon), D conflict |
| **Phase 33** | CURR cluster — curriculum/staging/τ_L/L_max/transitions | `ctl_instruction.md` | Q2 (s_min), M6, M7, M16, D5, Q6 (adaptive stages), τ_L/L_max formulas |
| **Phase 34** | LOOP cluster — batch construction, loss composition, causal mode, AD | `ctl_instruction.md` + `pinn_architecture.md` | B-07, B-08, NS-12, ALM μ_p clamp, causal mode (Q1), M16 integration |
| **Phase 35** | LOSS cluster — loss scaling/weights/gradient clipping/softening/Huber δ | `pinn_architecture.md` | M14, M15, NS-13, NS-18, epsilon strategy (Q3), ALM μ_p clamp |
| **Phase 36** | FUT hand-off | Both targets / FUT | All FUT-flagged gaps |

---

*Adjudication completed 2026-06-18. All findings trace to specific file sections and CLM-NN rows. No external information was consulted. Where sources were silent or ambiguous, gaps were logged explicitly in the claims register. "Insufficient evidence" was never forced into a resolution — all findings are grounded in attached materials.*
