# 03 — Curriculum and Training Loop

## Executive Summary

This document consolidates all identified findings, critical issues, and open decisions related to curriculum stage stratification, training loop mechanics, batch construction, causal-training methodology, and stage-assignment criteria across the three-body PINN training stack. Source material is drawn from the 2026-04-27 comprehensive technical audit (Sections 6 and 7), the Causal Training Mismatch resolution blueprint, the Issue on Data Validation Protocol, the stage-assignment methodology, and cherry-picked unique content from `next steps.txt`.

The curriculum follows a seven-stage progression (Stages 0-6) from stable hierarchical Keplerian motion through increasingly chaotic quasi-random configurations, culminating in near-collision and extreme scattering events. Each stage builds on the replay buffer of all preceding stages plus a lookahead fraction of the next stage's data, implemented via a Unified Batch Construction specification (audit Section 6, reproduced verbatim below) that mandates two independent point sets (data-fidelity and collocation), 240+16 replay/lookahead trajectory splits, 50/50 uniform/acceleration-weighted time sampling, and a capped hybrid energy loss weight schedule.

**Readiness assessment:** Two critical blockers (B-07 batch construction; B-08 data-fidelity/collocation conflation) plus one unresolved architectural decision (causal training mode: per-time-step causal weighting vs. global ALM) must be addressed before implementation. An additional open decision on the `s_min` collision-criterion frame must be resolved for consistency between curriculum gating and training loss evaluation.

---

## Confirmed Findings

### BLOCKING (Must resolve before training loop code can be written)

| ID | Severity | Finding | Location | Fix |
|----|----------|---------|----------|-----|
| B-07 | **BLOCKING** | Batch construction not implemented. Current `get_batch()` uses flat 256 random trajectories. CTL requires 240 replay (stages ≤ k) + 16 lookahead (stage k+1). Author acknowledged: "[Comment: ...not consistent with the CTL instruction plan]." | `main_pinn.pdf` Sec 3.1; `main_CTL.pdf` Sec 5.3.2 | Two-phase sampler: B_replay=240 from D_≤k, B_lookahead=16 from D_{k+1}. n_pts=32 with 50/50 uniform/acceleration-weighted. See Section 6. |
| B-08 | **BLOCKING** | Data-fidelity and collocation points conflated. CTL doesn't separate data-fidelity (must match Brutus snapshots) from collocation (anywhere in [0,T]). PINN has collocation sampling but unreconciled with CTL. | `main_CTL.pdf` Sec 5.3.2; `main_pinn.pdf` Sec 3.2 | Two independent point sets: (a) Data-fidelity: 8192 points from snapshots, L1 loss; (b) Collocation: 4096 points from [0,T], physics+energy loss. Both 50/50 sampling. |
| — | **BLOCKING** | No replay = catastrophic forgetting. No lookahead = abrupt transitions. Flat-batch has neither. | `basic_architecture.py` get_batch(); CTL Sec 5.3.2 | Implement replay/lookahead per Section 6 spec below. |

### MAJOR (Degrades training effectiveness or blocks dependent decisions)

| ID | Severity | Finding | Resolution Strategy |
|----|----------|---------|---------------------|
| M6 | MAJOR | L_norm lacks clamping — values > 1 possible numerically, producing L_norm_normalized > 1 for IC vector assembly. | Add `np.clip(L_norm, 0, 1)` before 2*x-1 mapping in IC vector formulation. |
| M7 | MAJOR | Lyapunov time tau_L computed in CTL Sec 4.4 but dropped from IC vector assembly in Sec 4.5. No decision documented on whether to include it. | **Exclude tau_L from IC vector** by design (it's a derived dynamical property, not an IC invariant). Use only for stage gating and model evaluation. See tau_L/L_max resolution section below. |
| M14 | MAJOR | Gradient clipping spec divergence: PINN uses median-based adaptive clipping; CTL uses curriculum-aware C schedule. Two different clipping strategies documented independently. | **Merge both:** `clip_value = C_stage * median(grad_norm_history)`, where C_stage from CTL schedule and median from PINN rolling window. |
| M15 | MAJOR | Energy loss lambda_E=1000 at Stage 6 risks overwhelming physics and data terms by 100-5000×. Single large energy weight can drown dynamics learning. | Implement capped hybrid schedule: `lambda_E(k) = min(10^(k-3), cap[k])` where cap = {0:1, 1:5, 2:20, 3:50, 4:100, 5:200, 6:500}. Add safeguard: if `lambda_E * L_energy > 10 * L_data`, warn and reduce. |
| M16 | MAJOR | dt_out varies 17× (0.01 to 0.17) but collocation density is uniform. Low-res trajectories get same collocation count as high-res despite far fewer Brutus snapshots. | Scale supplemental collocation in proportion to `dt_base / dt_out`: `n_col = base * (dt_base/dt_out)`. For dt_base=0.01: gold=1×, hier≈0.125×, standard≈0.059×. <!-- Reverted to audit M16 line 163 verbatim. --> |
| D5 | MAJOR | Stage transition criteria theoretically unattainable. Monotonically-decreasing validation loss with limited data blocks progression. Author: "...theoretical now... limited data, maybe not even enough." | Pilot Stage 0 first. Dual-path: strict (all criteria) + fallback (max-epochs, stagnation, NaN rollback). Calibrate empirically. |
| NS-12 | MAJOR | `next steps.txt` Issue 12: source documents say velocities/accelerations are derived via AD but provide no concrete three-body PyTorch implementation. | Use the component-wise AD implementation requirement in `01-architecture-and-physics-foundations.md`; do not differentiate the summed 9D output as a proxy for per-coordinate acceleration. |
| NS-13 | MAJOR | `next steps.txt` Issue 13: Huber energy-loss δ=1.0 may be too large for normalized energy residuals and can behave like plain L2 over the whole expected range. | Tune δ from observed normalized `|ΔH|` quantiles or start with δ≈0.01-0.1; document the chosen value per stage. |
| NS-18 | MAJOR | `next steps.txt` Issue 18: loss components need an explicit scaling contract across `L_data`, `L_physics`, and `L_energy`. | Adopt the Loss Component Scaling Contract below and cross-link the AD chain-rule factors in 01. |

### MINOR / INFO (Design refinements and documentation clarifications)

| ID | Severity | Finding | Resolution |
|----|----------|---------|------------|
| — | MINOR | Constraint counting error (M4): see `01-architecture-and-physics-foundations.md` MAJOR table for canonical documentation. Cross-linked here for CTL awareness — no code impact. | Reference M4 in 01. |
| — | INFO | ALM mu_p parameter can diverge without clamping. The moving-average variance update has no upper bound. | Add `mu_p = np.clip(mu_p, 1e-4, 100.0)` in ALM update step. |

---

## Causal Training Mismatch: Option A vs Option B

**Source:** `Issue_on_data_validation_protocol_and_compatbility_with_project_context.md`

The most consequential architectural decision for the training loop is how to handle temporal causality. The validation protocol assumes per-time-step causal loss weighting; the CTL document specifies global-sampling with ALM. These two approaches are fundamentally incompatible.

### Option A — Per-Time-Step Causal Weighting

Applies exponential weights `w_i ∝ exp(-λ Σ_{j<i} L_j)` to each time step's loss, enforcing strict "arrow of time" — future errors contribute only after past is resolved. **Risk:** "Causal Firewall" — an early stiffness spike drives all subsequent weights to zero, ALM sees artificially low variance, penalty parameters don't increase, training stops.

### Option B — Global Sampling + ALM

Samples time points globally (uniform or acceleration-weighted), no causal weighting. ALM has complete view of constraint violations. **Risk:** Temporal causality violation — late-time gradients propagate through unresolved early dynamics.

### Resolution: Time-Windowed Causal-ALM Hybrid

**Source:** `Causal_Trainingmismatch_resolution_blueprint.md`

The hybrid partitions [0,T] into overlapping causal windows with localized ALM and hard gating:

1. **Localized ALM:** Within each active window, ALM parameters update locally for accurate variance estimates
2. **Hard causal gate:** Adam operates within current window until ALM-penalized residual falls below tolerance
3. **State propagation:** Converged window's prediction bootstraps next window's initial condition; ALM multipliers carry forward
4. **Firewall prevention:** Future time points beyond active window are EXCLUDED from batch

### Training Phases

1. **Static Pre-Screening (CPU):** Galilean boost, invariant computation (eps=1e-10), SCS/SASD screening, 14-D IC assembly
2. **Stage Init + IPR Bounding:** Stages 0-6 stratification. IPR (eps=1e-5) for ALM convergence floor
3. **Causal-ALM Training (GPU):** PSC mini-batches across current+preceding stages. Adam + ALM per causal window
4. **Refinement + Transition:** Full domain converged. L-BFGS at IPR noise floor. Stage advance gated by Hamiltonian drift < 1e-4

---

## Loss Component Scaling Contract

**Source:** `next steps.txt` Issue 18, `main_pinn.tex` physics-loss section, and `main_CTL.tex` training-loop section.

Every training loss term must operate in the same dimensionless coordinate system:

| Loss Term | Evaluation Points | Required Units | Contract |
|-----------|-------------------|----------------|----------|
| `L_data` | Brutus snapshot times sampled from each trajectory | `t_tau in [-1,1]`, positions `r' = r/D` | Compare network output directly to scaled Brutus positions with L1/MAE. No unscaled positions enter this term. |
| `L_physics` | Independent collocation points in `[0,T]` mapped to `tau in [-1,1]` | positions `r'`, accelerations `d2r'/du2`, masses unchanged with `G=1` | Compute component-wise AD accelerations, apply `d2r'/du2 = 4*d2r'/dtau2`, then evaluate Newton residual with `epsilon_soft=1e-5`. |
| `L_energy` | Same collocation point set as `L_physics` | positions `r'`, velocities `dr'/du`, initial energy `H_0` in the same dimensionless units | Compute `dr'/du = 2*dr'/dtau`; use the same `epsilon_soft=1e-5` as the physics residual. |

The AD implementation details and chain-rule factors live canonically in `01-architecture-and-physics-foundations.md`. The batch constructor must keep data-fidelity points and collocation points separate even if they share trajectory IDs.

### Huber Delta for Normalized Energy

**Source:** `next steps.txt` Issue 13, `main_pinn.tex`.

The spec'd `delta=1.0` for `L_energy` is uncalibrated for normalized Hamiltonian residuals. If most `|ΔH|` values stay below 1.0, Huber acts like L2, losing robustness to outliers during close encounters.

**Recommended:** tune `delta` from empirical `|ΔH|` quantiles:

```python
delta_energy = np.clip(np.quantile(abs_delta_H_train, 0.75), 0.01, 0.1)
```

Record in `loss.yaml`. Use 0.01–0.1 as starting point; verify some close-encounter residuals enter the linear Huber branch.

---

## Data-Driven Adaptive Stage Assignment

**Source:** `stage-assignment-issue.txt`

### Methodology

Transition from fixed theoretical thresholds to data-adaptive criteria based on empirical distributions of invariants. This prevents underpopulated stages and empty stage boundaries that block curriculum progression.

**Core insight:** Quasi-random ICs introduce scaling distortions (Q ~ s^3) and invariant correlations. Data-driven criteria tailor boundaries to the actual dataset while retaining physically-grounded metrics.

**Step 1 — Dataset Analysis (EDA):**
1. Parse all IC files and Brutus outputs, compute invariants for every system
2. Compute distributions (histograms, KDE) split by IC type
3. Correlation matrix between invariants; if cor(E, tau_L) < -0.5, use composite scoring
4. PCA on invariants to capture >80% variance in 2-3 components
5. K-means (k=6-7) on invariants/PCs for natural difficulty clustering
6. Compute quantiles for adaptive threshold setting

**Step 2 — Adaptive Assignment:**

```python
# PCA + K-means clustering for stage discovery
invariants = df[['E', 'Q_normalized', 'L_norm', 's_min', 'tau_L', 'I1', 'I2', 'I3']]
pcs = PCA(n_components=3).fit_transform(invariants)
clusters = KMeans(n_clusters=6, random_state=42).fit_predict(pcs)
cluster_means = df.groupby('cluster')[['tau_L', 'E']].mean().sort_values('tau_L')

# Hierarchical stages (stable → moderate)
stage_0 = df[(df['type']=='hierarchical') & (df['L_norm'] > df['L_norm'].quantile(0.75))]
stage_1 = df[(df['type']=='hierarchical') & (df['E'] < df['E'].quantile(0.25)) &
             (df['Q_normalized'].between(0.9, 1.1))]
# Quasi-random stages via clusters sorted by mean tau_L
cluster_order = cluster_means.sort_values('tau_L', ascending=False).index
stage_3 = df[(df['type']=='quasi-random') & (df['cluster']==cluster_order[0])]
stage_5 = df[(df['type']=='quasi-random') & (df['cluster'].isin(cluster_order[3:5]))]
stage_6 = df[(df['type']=='quasi-random') & (df['cluster']==cluster_order[5])]
```

**Safeguards:** Ensure >10% per stage (merge underpopulated clusters). Validate with small PINN pilot. Check invariant correlations before clustering — if E and tau_L correlate strongly, use PCA composite as difficulty score.

**Integration:** Augments (not replaces) `assign_curriculum_stage()` in `data-processing-pipeline-full.py`. Static thresholds serve as initial anchors; data-driven quantiles refine them.

---

## tau_L and L_max Formula Resolution

**Source:** `next steps.txt` (Issue 1, verified+resolving section)

### Problem Statement

The CTL document defines stage criteria using Lyapunov time (tau_L) and L/L_max ratio but provides no explicit computation formulas. Stages 4a/4b require tau_L ranges (>5 and 2-5), Stage 0 requires L/L_max > 0.5. Without formulas, chaotic-regime stage assignment is impossible.

### L_max Computation (Resolved)

L_max = M_total * r_char * v_char where r_char is mean pairwise separation and v_char = sqrt(2|E|/M_total):

```python
def compute_L_norm(masses, r_prime, v_prime, eps=1e-10):
    L_vec = sum(masses[i] * np.cross(r_prime[i], v_prime[i]) for i in range(3))
    L = np.linalg.norm(L_vec)
    r_char = np.mean([np.linalg.norm(r_prime[i]-r_prime[k]) for i in range(3) for k in range(i+1,3)])
    T = np.sum(0.5 * masses * np.sum(v_prime**2, axis=1))
    V = -sum(masses[i]*masses[k]/(np.linalg.norm(r_prime[i]-r_prime[k])+eps) for i in range(3) for k in range(i+1,3))
    E = T + V; M_total = np.sum(masses)
    v_char = np.sqrt(2*abs(E)/M_total) if abs(E)>eps else 0.0
    L_max = M_total * r_char * v_char
    return np.clip(L/(L_max+eps), 0, 1) if L_max>eps else 0.0
```

### tau_L Computation (Resolved)

tau_L = 1/λ_max where λ_max is the largest Lyapunov exponent. The recommended approach uses shadow trajectory divergence: perturb the initial state by epsilon_pert, integrate both trajectories, and track exponential separation growth.

<!-- Reverted: tau_L uses split epsilon_pert=1e-8 (perturbation magnitude) and epsilon_soft=1e-10 (potential softening) per next steps.txt Issue 1 / data-processing-pipeline-full.py line 167. The merged eps=1e-10 form lost the distinction. -->

```python
def compute_tau_L(masses, r_prime, v_prime, T_scale=10.0, G=1.0, M_tot_ref=3.0,
                  epsilon_pert=1e-8, epsilon_soft=1e-10, delta_t=0.1, n_pert=3, horizon=50.0):
    """Compute Lyapunov time via shadow trajectory divergence."""
    from scipy.integrate import solve_ivp
    D = np.cbrt(G * M_tot_ref * T_scale**2)  # = 6.694
    V = D / T_scale
    y0 = np.hstack((r_prime.flatten(), v_prime.flatten()))

    def rhs(t, y):
        pos, vel = y[:9].reshape(3,3), y[9:].reshape(3,3)
        acc = np.zeros((3,3))
        for i in range(3):
            for j in range(3):
                if i != j:
                    dr = pos[j] - pos[i]
                    acc[i] += masses[j] * dr / (np.linalg.norm(dr)**3 + epsilon_soft)
        return np.hstack((vel.flatten(), acc.flatten()))

    T_max = horizon / T_scale
    lambdas = []
    for _ in range(n_pert):
        delta0 = epsilon_pert * (d := np.random.randn(18)) / np.linalg.norm(d)
        sol_nom = solve_ivp(rhs, [0, T_max], y0, method='LSODA', rtol=1e-12, atol=1e-12, dense_output=True)
        sol_pert = solve_ivp(rhs, [0, T_max], y0 + delta0, method='LSODA', rtol=1e-12, atol=1e-12, dense_output=True)
        current_t, sum_log, num_steps = 0.0, 0.0, 0
        dt = delta_t / T_scale
        while current_t < T_max:
            t_eval = np.linspace(current_t, min(current_t + dt, T_max), 10)
            d = np.linalg.norm(sol_pert.sol(t_eval) - sol_nom.sol(t_eval), axis=0)
            avg_d = np.mean(d)
            if avg_d > 1e-4:
                sum_log += np.log(avg_d / epsilon_pert); num_steps += 1
                sol_pert = solve_ivp(rhs, [current_t, T_max],
                    sol_nom.sol(current_t) + epsilon_pert * (sol_pert.sol(current_t) - sol_nom.sol(current_t)) / avg_d,
                    method='LSODA', rtol=1e-12, atol=1e-12, dense_output=True)
            current_t += dt
        if num_steps > 0: lambdas.append(sum_log / (num_steps * dt))

    tau_L = T_scale / max(np.max(lambdas) if lambdas else 0.0, 1e-6)
    return tau_L
```

**Operational note:** For batch processing ~15K trajectories, use the faster PCA+Rosenstein approximation at `data-processing-pipeline-full.py:799` (`estimate_lyapunov_time()`). Calibrate thresholds against the integration-based method on a representative sample.

**D value:** Uses corrected B-02 formula: D = cbrt(G * M_tot_ref * T_scale^2) = 6.694. Original CTL D = cbrt(G * T_scale^2) ≈ 4.64 omitted M_tot.

---

## Implementation Checklist — Training Loop Items

**Source:** Audit Section 7 (P3-P4 items extracted)

### Phase 3: Training Loop Implementation

- [ ] **P3-1:** Implement two-phase replay/lookahead batch construction (240 replay + 16 lookahead)
- [ ] **P3-2:** Separate data-fidelity and collocation point sampling (two independent sets, 8192 + 4096 points)
- [ ] **P3-3:** Add `strategy='mixed'` to collocation sampler (50/50 uniform/acceleration-weighted)
- [ ] **P3-4:** Implement merged gradient clipping: `C_stage * median(grad_norm_history)`
- [ ] **P3-5:** Add mu_p clamping [1e-4, 100] to ALM update
- [ ] **P3-6:** Implement capped hybrid energy weight schedule (see M15 fix above)
- [ ] **P3-7:** Implement stage-dependent transition criteria with max-epochs fallback (see D5 fix below)
- [ ] **P3-8:** Run Stage 0 pilot; calibrate thresholds empirically

### Phase 4: Verification and Re-computation

- [ ] **P4-1:** Re-run stage assignment for all ~15K trajectories with corrected D=6.694 and unified epsilon
- [ ] **P4-2:** Verify all IC vector components in [-1,1] with bounds-checking unit test
- [ ] **P4-3:** Run COM verification on 100 quasi-random + 100 hierarchical samples
- [ ] **P4-4:** Verify injectivity claim with peer review or symbolic check
- [ ] **P4-5:** Ablate skip-path LayerNorm (with/without) — train two models, compare
- [ ] **P4-6:** Document all resolved ambiguities and final design decisions

### Stage Transition Criteria (D5 — Practical Fallbacks)

**Source:** Audit Section 6.3

The strict transition criteria require monotonically decreasing validation loss, which is unrealistic with finite data and Adam optimizer. Practical dual-path advancement:

```
ADVANCE when EITHER:

PATH A (Strict — all four met):
    A1. Training plateau: |L_smooth(i) - L_smooth(i-200)| / L_smooth(i) < 1e-5
    A2. Validation stable: L_val(i) <= percentile_10(val_history)  [relaxed from min]
    A3. Physics residual: L_val_phys < epsilon_phys[stage]  [stage-dependent]
    A4. Energy drift: avg |H(t_final) - H(0)| / |H(0)| < epsilon_energy[stage]

PATH B (Fallback — any trigger):
    B1. MAX_EPOCHS reached: {0:500, 1:600, 2:700, 3:800, 4:900, 5:1000, 6:1200}
    B2. Stagnation: no val improvement >1% for 400 epochs
    B3. NaN/Inf: rollback to last checkpoint, LR *= 0.5, retry

Stage-dependent thresholds:
    Stage | epsilon_phys | epsilon_energy
    ------|-------------|---------------
    0     | 5e-3        | 5e-3
    1     | 2e-3        | 2e-3
    2     | 1e-3        | 1e-3
    3     | 5e-4        | 5e-4
    4     | 2e-4        | 2e-4
    5-6   | 1e-4        | 1e-4
```

**Pilot strategy (D5):** Run Stage 0 with relaxed thresholds first. Measure actual convergence behavior. If the network reaches the strict-path thresholds within 500 epochs, the criteria are calibrated. If not, widen thresholds proportionally to the observed convergence rate. Do NOT treat the above thresholds as fixed — they are hypotheses to be empirically validated.

### Energy Loss Weight Schedule (M15 — Capped Hybrid)

```python
def get_lambda_E(stage, L_energy_current=None):
    """Stage-dependent energy weight with adaptive soft cap."""
    base = 10 ** (stage - 3)
    cap_table = {0: 1.0, 1: 5.0, 2: 20.0, 3: 50.0, 4: 100.0, 5: 200.0, 6: 500.0}
    lambda_E = min(base, cap_table[stage])
    if L_energy_current is not None and L_energy_current < 0.01:
        lambda_E *= 0.5  # Reduce if already well-conserved
    return lambda_E
```

The cap prevents energy loss from dominating the total loss at late stages. At Stage 6, lambda_E capped at 500 (vs uncapped 1000 in original spec). The adaptive reduction (factor 0.5) further reduces energy penalty when conservation is already well-maintained, shifting optimizer focus to dynamics accuracy.

---

## Open Decisions

> **[DECISION-NEEDED]** Causal training mode: Option A (per-time-step causal weighting) vs Option B (global sampling + ALM) vs Hybrid (Time-Windowed Causal-ALM)
>
> Three approaches exist for handling temporal causality in the training loop:
>
> **Option A — Per-time-step causal weighting (validation-PDF style):**
> - Applies exponential weights `w_i ∝ exp(-λ Σ_{j<i} L_j)` to each time step's loss
> - Enforces strict "arrow of time" — future errors contribute only after past is resolved
> - Risk: "Causal Firewall" — a single early stiffness spike kills all future gradients
> - Implemented in some PINN literature (Wang et al., arXiv:2203.07404)
>
> **Option B — Global sampling + ALM (CTL-doc style):**
> - Samples time points globally from each trajectory, no causal weighting
> - ALM has complete view of constraint violations across full temporal domain
> - Risk: Temporal causality violation — late-time gradients propagate through unresolved early-time dynamics
> - Simpler to implement, well-tested in standard PINN training loops
>
> **Option C — Time-Windowed Causal-ALM Hybrid (Causal_Trainingmismatch blueprint):**
> - Divides temporal domain into discrete overlapping causal windows
> - ALM operates locally within each window (avoids the causal firewall)
> - Hard gating mechanism advances windows only when local convergence achieved
> - Structural state propagation ensures continuity between windows
> - Most complex to implement but theoretically resolves both failure modes
>
> **Recommendation:** Keep this decision open. The current CTL/PINN LaTeX sources describe Option B (global sampling + ALM), while the Causal Training Mismatch blueprint explicitly recommends Option C (Time-Windowed Causal-ALM Hybrid) as the reconciliation. Phase 9 must preserve that stronger blueprint conclusion rather than silently downgrading it. If implementation simplicity is prioritized, a human reviewer may choose Option B, but that choice should be recorded as an intentional departure from the blueprint.
>
> **Resolve before finalizing the training loop implementation.**

> **[DECISION-NEEDED]** Frame for `s_min` in collision criterion: unsoftened raw separation vs `max(s_min, epsilon)`
>
> **Conflict (D-05):** CTL uses unsoftened s_min for the Stage 6 collision gate. Audit D8 notes that for r_ij < epsilon, geometric and softened values differ. The unsoftened value is physically honest but risks gradient explosion (1/r^3 divergence) during close encounters in single-precision arithmetic.
>
> **Recommended resolution:** Use `max(s_min, epsilon_soft)` (epsilon_soft=1e-5) for training loss collision criterion — matches the loss function's own softening floor. Use unsoftened s_min for the curriculum STAGE GATE (gate should detect true close encounters). Always log unsoftened value for diagnostics. Document unsoftened approach under "Considered Alternatives."
>
> **Resolve before implementing Stage 6 collision criterion.**

---

## Recommended Resolutions

1. **P3-1 — Implement replay/lookahead batch construction:** Two-phase sampler per the verbatim Section 6 specification below. 240 replay + 16 lookahead, 32 points/trajectory with 50/50 sampling. Highest-priority task — without it the curriculum does not function.

2. **P3-2 — Separate data-fidelity and collocation points:** Define two independent point sets. Data-fidelity: 8192 points from Brutus snapshots, L1 loss. Collocation: 4096 points from [0,T], physics + energy loss. Both use 50/50 sampling.

3. **P3-3 — Resolve causal training decision:** Choose between current CTL/PINN Option B and blueprint Option C before coding. If Option C is chosen, implement time-windowed causal ALM. If Option B is chosen, document the human decision to prioritize current LaTeX simplicity over the blueprint's hybrid recommendation.

4. **P3-4 — Implement merged gradient clipping:** `clip_value = C_stage * median(grad_norm_history)` with rolling window of last 100 gradient norms.

5. **P3-5 — Implement capped hybrid energy weight schedule:** `lambda_E(k) = min(10^(k-3), cap[k])` with safeguard when energy term dominates.

6. **P3-6 — Implement stage transition criteria with fallback:** Dual-path advancement (strict + fallback). Calibrate thresholds from Stage 0 pilot.

7. **P3-7 — Implement adaptive stage assignment:** Data-driven PCA + K-means + quantile methodology. Run once pre-training on the full dataset.

8. **P3-8 — Implement tau_L and L_max computation:** Per-trajectory computation using the resolved formulas above. Integrate into `compute_all_invariants()` in the data pipeline.

9. **P3-9 — Add dt_out-aware collocation scaling:** `n_col_per_traj = base_n_col * (dt_base / dt_out)`. For dt_base=0.01, gold gets 1×, hierarchical-base gets 0.125×, standard-base gets ~0.059×. <!-- Reverted to audit M16 line 163 verbatim. -->

10. **P3-10 — Resolve s_min frame:** Use `max(s_min, epsilon)` for training loss, log unsoftened value for diagnostics (per Open Decision above).

11. **P3-11 — Calibrate Huber energy δ:** Select `delta_energy` from normalized `|ΔH|` statistics, with an initial recommended range of 0.01-0.1.

---

## Cross-Issue Interactions (Training Loop)

Several issues interact non-trivially across the training loop and must be resolved together:

| Interaction | Issues | Description | Severity |
|-------------|--------|-------------|----------|
| Batch + collocation | B-07, B-08 | Replay/lookahead is trajectory-level; collocation is point-level. Both must be implemented together for consistent training. | **Major** |
| Stage criteria + limited data | B-08, D5 | Transition criteria depend on validation loss being meaningful, which requires enough data. Max-epochs fallback prevents infinite loops. | **Major** |
| Causal mode + ALM | Option A/B, M15 | Causal weighting masks future errors → ALM variance estimate artificially low → penalty parameters don't increase. Resolution choice affects ALM implementation. | **Critical** |
| Energy weight + gradient clipping | M15, M14 | Large lambda_E at late stages amplifies energy loss gradients. Curriculum-aware gradient clipping must account for these amplified gradients. | **Major** |
| dt_out heterogeneity + stage assignment | M16, D5 | Low-resolution trajectories get systematically fewer constraints. Stage transition criteria must be relaxed for stages dominated by low-resolution data. | **Minor** |
| s_min + softening + collision criterion | D8, B-09 | Softening choice affects whether Stage 6 correctly identifies close-encounter systems. Dual-epsilon strategy splits this: eps=1e-10 for gate, eps_soft=1e-5 for loss. | **Major** |

---

## Gradient Clipping — Merged Specification

**Source:** Audit M14

The PINN document specifies median-based adaptive clipping; the CTL document specifies a curriculum-aware C schedule. The merged specification combines both:

```python
# During training_step():
grad_norm_history = []  # Rolling window, max length 100

def get_clip_value(stage, grad_norms):
    """Merged adaptive + curriculum-aware clipping."""
    C_table = {0: 8.5, 1: 8.5, 2: 5.0, 3: 5.0, 4: 3.0, 5: 3.0, 6: 3.0}  # CTL schedule from next steps.txt Issue 8: stages 0-1 use 7-10 (midpoint 8.5), 2-3 use 5, 4-6 use 3.
    C_stage = C_table[stage]
    median_grad = np.median(grad_norms[-100:]) if len(grad_norms) >= 10 else 1.0
    return C_stage * max(median_grad, 1e-6)

# In training step, after backward():
clip_value = get_clip_value(stage, grad_norm_history)
torch.nn.utils.clip_grad_norm_(model.parameters(), clip_value)
```

C_stage decreases with stage: Stages 0-1 (quasi-periodic) use C=8.5 (midpoint of CTL's 7-10 range); Stages 2-3 use C=5.0; Stages 4-6 (chaotic encounters) use C=3.0. Early stages tolerate larger gradients; later chaotic stages need aggressive clipping. The median rolling window adapts to current training dynamics. <!-- Reverted descriptive prose to match next steps.txt Issue 8: early stages tolerate larger gradients, later chaotic stages need aggressive clipping. -->

---

## ALM Parameter Update Specification

**Source:** Audit Section 6, augmented with mu_p clamping per review findings

```python
# ALM parameter update (excluded from autograd, executed in torch.no_grad())
lambda_p += mu_p * L_physics.item()

# Robust RMSprop-inspired moving average of squared physics loss
v_p = 0.99 * v_p + 0.01 * (L_physics.item() ** 2)
mu_p = 0.01 / np.sqrt(v_p + 1e-8)

# Clamp mu_p to prevent divergence or vanishing
mu_p = np.clip(mu_p, 1e-4, 100.0)
```

The clamping bounds were added in response to the observation that mu_p can diverge without limits. Lower bound 1e-4 prevents the penalty parameter from decaying to zero (which would disable physics enforcement). Upper bound 100.0 prevents the penalty from overwhelming the data fidelity term.

---

## References

- [01-architecture-and-physics-foundations.md](01-architecture-and-physics-foundations.md) — 14-D input vector consumed by training loop; COM frame transform applied before training; D=6.694 drives stage thresholds; dual-epsilon strategy (eps=1e-10 for stage gating, eps_soft=1e-5 for training loss); normalization formulas table (canonical location); omega0 scheduling interacts with stage initialization.
- [02-data-pipeline-and-validation.md](02-data-pipeline-and-validation.md) — DataLoader must support stage queries (replay/lookahead sampling); SCS/SASD/IPR/PSC feed into training loop as live parameters; stage labels produced by data pipeline; TrajectoryValidator gate must be passed before training data enters loop; temporal resolution bridging feeds into dt_out-aware collocation scaling.
- [Canonical: CTL Instruction](../../../markdown_conversion/pandoc_conversion/CTL-instruction-final.md) — Original curriculum training framework specification.
- [Canonical: PINN Architecture Plan](../../../markdown_conversion/pandoc_conversion/PINN_architecture_plan.md) — Original architecture specification including training strategy.
- [Canonical: data-processing-pipeline-full.py](../../../../pinn/data-processing-pipeline-full.py) — Current IC vector assembly, stage assignment logic, and training data preparation.
- [Canonical: basic_architecture.py](../../../../pinn/basic_architecture.py) — Current SIREN implementation, get_batch(), and training utilities.

---

## Considered Alternatives

### Unsoftened s_min for Collision Criterion

**Source:** CTL document, Audit D8

The CTL document states that `s_min` is "true pairwise separations (no softening)" for the Stage 6 collision criterion. This is physically honest — it measures actual physical separation without introducing a softening kernel. In principle, a collision detection criterion should flag genuinely close encounters, not softened approximations.

**Reason not chosen:** During gradient-based optimization, the unsoftened `s_min` produces infinite gradients as separation approaches zero (1/r^3 divergence in the physics residual). In single-precision GPU arithmetic, these gradients immediately cause NaN propagation through skip connections. The softened value `max(s_min, epsilon)` provides a numerically stable floor that is consistent with the loss function's own softening — the network never sees unsoftened physics, so the collision criterion should match the physics the network actually learns.

The unsoftened value is still computed and logged for diagnostic purposes, and is still used for the curriculum stage gate (which identifies close-encounter systems BEFORE they enter the training loss). The softening is applied only in the training loss collision criterion, not in the stage assignment gate.

---

## Verbatim Reference Specification — Copied from 2026-04-27 Audit

The following section is copied verbatim from the comprehensive technical audit dated 2026-04-27. It serves as the authoritative batch construction specification that downstream implementation phases should implement directly — preserving exact text avoids transcription bugs in the formal training loop spec.

---

## 6. UNIFIED BATCH CONSTRUCTION SPECIFICATION

### 6.1 Design Principles

1. **Two independent point sets**: Data-fidelity (Brutus snapshots, L1 loss) and collocation (anywhere in [0,T], physics+energy loss)
2. **Replay/lookahead trajectory split**: 240 replay + 16 lookahead per CTL
3. **Mixed time sampling**: 50% uniform + 50% acceleration-weighted for BOTH data and collocation points
4. **Per-trajectory collocation**: Each of 256 trajectories gets 16 collocation points

### 6.2 Complete Training Step Pseudo-Code

```python
def training_step(dataset, model, stage, optimizer, lambda_p, mu_p, v_p):
    # ---- STEP 1: Trajectory batch (CTL Sec 5.3.2) ----
    B_replay, B_lookahead = 240, 16
    replay_trajs = dataset.sample_replay(n=B_replay, max_stage=stage)
    if dataset.has_stage(stage + 1):
        lookahead_trajs = dataset.sample_lookahead(n=B_lookahead, stage=stage+1)
        batch_trajs = replay_trajs + lookahead_trajs
    else:
        batch_trajs = replay_trajs

    # ---- STEP 2: Data-fidelity points (50/50 sampling) ----
    t_data, r_true, ic_data = [], [], []
    for traj in batch_trajs:
        times, positions = traj['times'], traj['positions']  # Brutus snapshots
        n_u, n_w = 16, 16  # 50/50 split of 32 points
        idx_u = np.random.choice(len(times), n_u, replace=False)
        acc_norms = np.abs(traj['accelerations']).max(axis=1)
        weights = acc_norms / acc_norms.sum()
        idx_w = np.random.choice(len(times), n_w, p=weights, replace=False)
        idx = np.concatenate([idx_u, idx_w])
        t_data.extend(2.0 * times[idx] / T_max - 1.0)  # normalize to [-1,1]
        r_true.extend(positions[idx].reshape(-1, 9))
        ic_data.extend(np.tile(traj['ic_vector'], (32, 1)))

    # ---- STEP 3: Collocation points (separate, 50/50) ----
    n_col_per_traj = 16  # 4096 / 256
    t_col, ic_col, H0_col = [], [], []
    for traj in batch_trajs:
        n_u, n_w = n_col_per_traj // 2, n_col_per_traj - n_col_per_traj // 2
        t_u = np.random.uniform(-1, 1, size=n_u)
        acc_norms = np.abs(traj['accelerations']).max(axis=1)
        weights = acc_norms / acc_norms.sum()
        t_w_phys = np.random.choice(traj['times'], size=n_w, p=weights)
        t_w = 2.0 * t_w_phys / T_max - 1.0
        t_col.extend(np.concatenate([t_u, t_w]))
        ic_col.extend(np.tile(traj['ic_vector'], (n_col_per_traj, 1)))
        H0_col.extend(np.full(n_col_per_traj, traj['H_0']))

    # ---- STEP 4: Forward passes ----
    # Data fidelity
    input_data = torch.cat([tensor(t_data).unsqueeze(-1), tensor(ic_data)], dim=-1)
    r_pred_data = model(input_data)
    L_data = torch.mean(torch.abs(r_pred_data - tensor(r_true)))

    # Physics + Energy (collocation)
    input_col = torch.cat([tensor(t_col).unsqueeze(-1), tensor(ic_col)], dim=-1)
    t_col_req = tensor(t_col, requires_grad=True)  # for autodiff
    r_pred_col = model(torch.cat([t_col_req.unsqueeze(-1), tensor(ic_col)], dim=-1))
    L_physics = compute_physics_residual(t_col_req, r_pred_col, tensor(ic_col))
    L_energy = compute_energy_loss(r_pred_col, tensor(H0_col))

    # ---- STEP 5: Total loss with ALM ----
    lambda_E = get_lambda_E(stage)  # capped hybrid schedule
    L_total = L_data + lambda_p * L_physics + (mu_p / 2.0) * L_physics**2 + lambda_E * L_energy

    # ---- STEP 6: Backprop + ALM update ----
    optimizer.zero_grad()
    L_total.backward()
    C = get_clip_c(stage)  # curriculum-aware C
    clip_grad_norm_(model.parameters(), C * median(grad_norm_history))
    optimizer.step()

    # ALM parameter update (excluded from autograd)
    with torch.no_grad():
        lambda_p += mu_p * L_physics.item()
        v_p = 0.99 * v_p + 0.01 * (L_physics.item() ** 2)
        mu_p = 0.01 / np.sqrt(v_p + 1e-8)
        mu_p = np.clip(mu_p, 1e-4, 100.0)
```

### 6.3 Stage Transition Criteria (Practical Fallbacks)

```
ADVANCE when EITHER:

PATH A (Strict — all four met):
    A1. Training plateau: |L_smooth(i) - L_smooth(i-200)| / L_smooth(i) < 1e-5
    A2. Validation stable: L_val(i) <= percentile_10(val_history)  [relaxed from min]
    A3. Physics residual: L_val_phys < epsilon_phys[stage]  [stage-dependent]
    A4. Energy drift: avg |H(t_final) - H(0)| / |H(0)| < epsilon_energy[stage]

PATH B (Fallback — any trigger):
    B1. MAX_EPOCHS reached: {0:500, 1:600, 2:700, 3:800, 4:900, 5:1000, 6:1200}
    B2. Stagnation: no val improvement >1% for 400 epochs
    B3. NaN/Inf: rollback to last checkpoint, LR *= 0.5, retry

Stage-dependent thresholds:
    Stage | epsilon_phys | epsilon_energy
    ------|-------------|---------------
    0     | 5e-3        | 5e-3
    1     | 2e-3        | 2e-3
    2     | 1e-3        | 1e-3
    3     | 5e-4        | 5e-4
    4     | 2e-4        | 2e-4
    5-6   | 1e-4        | 1e-4
```

### 6.4 Energy Loss Weight (Capped Hybrid Schedule)

```python
def get_lambda_E(stage, L_energy_current=None):
    """Stage-dependent energy weight with adaptive soft cap."""
    base = 10 ** (stage - 3)
    cap_table = {0: 1.0, 1: 5.0, 2: 20.0, 3: 50.0, 4: 100.0, 5: 200.0, 6: 500.0}
    lambda_E = min(base, cap_table[stage])
    if L_energy_current is not None and L_energy_current < 0.01:
        lambda_E *= 0.5  # Reduce if already well-conserved
    return lambda_E
```

---

*End of verbatim audit Section 6 *

---

## Stage Inventory Summary

| Stage | Name | Data Source | Key Criteria | Trajectory Count (approx.) | Temporal Resolution |
|-------|------|-------------|--------------|---------------------------|---------------------|
| 0 | Stable Keplerian | Hierarchical, low-fidelity | E < -0.5, L_norm > 0.5, Q in [0.7,1.3], s_min > 2 | ~1,200 | dt_out = 0.08 |
| 1 | Moderately Stable | Hierarchical, low-fidelity | Relaxed E or L_norm thresholds | ~2,000 | dt_out = 0.08 |
| 2 | High-Res Refinement | Hierarchical, high-fidelity | All hierarchical gold | ~1,657 | dt_out = 0.01 |
| 3 | Moderately Chaotic | Quasi-random, low-fidelity | E ≤ E_25, L_norm ≥ L_75, Q in [0.9,1.1] (quantile-derived) | ~600 | dt_out = 0.17 |
| 4 | Chaotic | Quasi-random, low-fidelity | tau_L > 2, remaining low-fidelity | ~1,600 | dt_out = 0.17 |
| 5 | High-Res Chaotic | Quasi-random, high-fidelity | All quasi-random gold (minus 184 missing IDs) | ~2,565 | dt_out = 0.01 |
| 6 | Near-Collision / Extreme | Any | s_min < 0.5 or |E| < 0.01 | Unknown | Any |

**Stage transition flow:** Stages progress cumulatively. Stage k's replay buffer includes all trajectories from Stages 0 through k-1, ensuring no catastrophic forgetting. Stage 6 is the catch-all for extreme cases and can be entered from any prior stage.

**DataLoader queries required:**
- `sample_replay(n=240, max_stage=k)` — sample n trajectories from cumulative D_≤k
- `sample_lookahead(n=16, stage=k+1)` — sample n trajectories from D_{k+1}
- `has_stage(k+1)` — check if next stage has data before attempting lookahead

---

## Decision Priority Queue (Training Loop)

| Priority | Item | Blocks | Estimated Effort |
|----------|------|--------|------------------|
| **P3-3** | Resolve causal training mode decision | Batch construction design | Decision only (no code) |
| **P3-1** | Implement replay/lookahead batch construction | All curriculum training | ~100 lines of Python |
| **P3-2** | Separate data-fidelity and collocation points | Physics loss correctness | ~50 lines in DataLoader + training_step |
| **P3-10** | Implement s_min frame resolution | Stage 6 collision criterion | Decision + 5 lines of code |
| **P3-5** | Implement capped hybrid energy weight schedule | Late-stage training stability | ~15 lines of Python |
| **P3-6** | Implement stage transition criteria with fallback | Curriculum progression | ~50 lines of Python |
| **P3-4** | Implement merged gradient clipping | Training stability | ~20 lines of Python |
| **P3-7** | Implement data-driven adaptive stage assignment | Stage population balance | ~100 lines of Python + EDA run |
| **P3-8** | Implement tau_L / L_max computation | Stage 0 and 4a/4b assignment | ~80 lines of Python |
| **P3-9** | Add dt_out-aware collocation scaling | Collocation density correctness | ~10 lines of Python |
| **P3-11** | Calibrate Huber energy δ | Stage 0 calibration | Tuning step (hours) |
| **P3-12** | Pilot Stage 0; calibrate all thresholds | All stage advancement | ~1 training run (hours) |
<!-- Renumbered Decision Priority Queue IDs to match Recommended Resolutions canonical numbering (P3-1..P3-11). Added P3-11 (Huber δ) and P3-12 (Stage 0 pilot) entries to align both lists. -->

---

*End of 03-curriculum-and-training-loop.md*

*This document synthesized from 7 source files archived in `archive/`. See `MIGRATION.md` for per-section provenance.*
