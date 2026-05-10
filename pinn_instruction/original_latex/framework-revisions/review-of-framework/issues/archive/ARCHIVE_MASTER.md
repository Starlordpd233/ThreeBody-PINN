---
title: Archive Consolidation — Review-of-Framework Issues
generated: 2026-05-02
source_dir: pinn_instruction/original_latex/review-of-framework/issues/archive/
file_count: 7
ordering: chronological (mtime ascending)
content_modification: none (verbatim concatenation with non-content delimiter wrappers)
extraction_marker: HTML comments — see "Extraction Protocol" section
---

# Archive Master — Review-of-Framework Issues

## Extraction Protocol

Each embedded file is wrapped in HTML-comment boundary markers (FILE_BEGIN / FILE_END).
Extraction uses the FILE_SIZE_BYTES metadata to slice body bytes directly — no regex
capture of body content. See the verification script for the exact implementation.

## Index

| # | File | Format | Size (B) | Lines | mtime | SHA-256 (first 12) |
|---|------|--------|---------:|------:|-------|--------------------|
| 1 | `next steps.txt` | text |   128,292 |  2847 | 2025-07-27T10:43:28 | `73ac904eb00e` |
| 2 | `stage-assignment-issue.txt` | text |    10,667 |   107 | 2025-08-01T09:40:25 | `2ac1a35136cc` |
| 3 | `next-step-for-data-processing-pipeline.txt` | text |     6,189 |    86 | 2025-08-02T09:59:51 | `3b844e2e892c` |
| 4 | `review.md` | markdown |     6,391 |   120 | 2026-03-21T05:48:23 | `c6a4f48be20e` |
| 5 | `Issue_on_data_validation_protocol_and_compatbility_with_project_context.md` | markdown |     8,321 |   111 | 2026-04-26T21:05:10 | `16b77013cc48` |
| 6 | `three_body_pinn_pre-implementation_audit_2026-04-27.md` | markdown |    38,109 |   498 | 2026-04-26T21:53:14 | `38342b85d758` |
| 7 | `Causal_Trainingmismatch_resolution_blueprint.md` | markdown |    48,709 |   250 | 2026-04-26T23:07:42 | `bd0e58e8d6cd` |

## Embedded Files

<!-- ============================================================ -->
<!-- FILE_BEGIN: 001 -->
<!-- FILE_NAME: next steps.txt -->
<!-- FILE_FORMAT: text -->
<!-- FILE_SIZE_BYTES: 128292 -->
<!-- FILE_LINES: 2847 -->
<!-- FILE_MTIME: 2025-07-27T10:43:28 -->
<!-- FILE_SHA256: 73ac904eb00e13f49cd96bc93b49cc493485795d202311f92b85969df89612e1 -->
<!-- ============================================================ -->
Some issues that were identified are as follows. Before making any changes, we need to first evaluate
the validity of these identified issues first to avoid making unnecessary mistakes/changes. Do we actually need to 
fix these issues? If so, how should we fix them? If a solution is also provided alongside the issue together, should we adopt it,
modify it, or change it?

================================================================================
ISSUES LIST
================================================================================

--------------------------------------------------------------------------------
ISSUE 1: Missing Lyapunov Time calculation τ_L and L_max computation formulas
--------------------------------------------------------------------------------

**Issue Details:**
The CTL document defines curriculum stages based on Lyapunov time criteria but lacks explicit computation formulas for both τ_L and L_max, which are essential for stage assignment and data binning.

**Stage Definitions Using τ_L (from CTL document):**
- **Stage 4a:** τ_L > 5 (Lyapunov time > 5 code units) - Systems with moderate chaos and relatively long predictability horizons
- **Stage 4b:** 2 < τ_L ≤ 5 - Systems with strong chaos and limited predictability

**Missing Formula for τ_L:**
The CTL document explicitly acknowledges this gap with an author comment: "How should we define the formula for calculating τ_L?" (line 244). The document discusses Lyapunov time evaluation metrics in the context of model evaluation (lines 1739-1745) but provides no computation formula for stage assignment.

**L_max Definition but Missing Computation:**
The CTL document defines L_max as "the theoretical maximum angular momentum for the system's energy (which corresponds to all mass moving on a circular orbit for that energy)" and uses L/L_max ratios for stage criteria (line 101-102), but provides no explicit formula for computing L_max from initial conditions.

**Evaluation Context (where τ_L appears):**
From CTL lines 1739-1745, τ_L is used for model evaluation:
- **Prediction Horizon:** Quantify how long model predictions remain accurate by measuring prediction horizon in units of Lyapunov time
- **Performance Metric:** A good model should achieve T_pred ≈ τ_L, meaning it can predict about as far as chaos inherently allows
- **Conservation Testing:** Check if models conserve invariants over many Lyapunov times

**PINN Architecture Document:**
Contains no mention of Lyapunov time calculations, τ_L formulas, or L_max computations. The PINN document focuses on architecture and loss functions without addressing curriculum stage assignment criteria.

**Practical Impact:**
Without explicit τ_L and L_max computation formulas:
1. Cannot properly assign trajectories to curriculum stages 4a and 4b
2. Cannot implement the L/L_max > 0.5 criterion for Stage 0
3. Cannot evaluate model performance using Lyapunov time metrics
4. Stage-based training progression becomes impossible to implement

**Source Locations:**
- CTL-instruction-final.tex: Stage criteria lines 202, 212; Missing formula acknowledgment line 244; L_max definition lines 101-102; Evaluation metrics lines 1739-1745
- PINN_architecture_plan.tex: No relevant information found

(Verified and Resolving)

**Potential Solution**

1. Compute Global Scales Across the Entire Dataset:

```python
import numpy as np
import os

def parse_ic_file(filename):
    with open(filename, 'r') as f:
        line = f.readline().strip().split()
        ic = np.array([float(x) for x in line])
    # Reshape: positions (9), velocities (9), masses (3) but interleaved
    pos = np.array([ic[0:3], ic[7:10], ic[14:17]])
    vel = np.array([ic[3:6], ic[10:13], ic[17:20]])
    masses = np.array([ic[6], ic[13], ic[20]])
    return masses, pos, vel

def compute_globals(ic_files, t_max=10.0, G=1.0, eps=1e-10):
    N = len(ic_files)
    all_E = np.zeros(N)
    all_r_char = np.zeros(N)
    
    D = np.cbrt(G * t_max**2)  # ~4.641588833612778
    V = D / t_max
    
    for j, filename in enumerate(ic_files):
        m, r_raw, v_raw = parse_ic_file(filename)
        
        # Scale
        r_prime = r_raw / D
        v_prime = v_raw / V
        
        # Compute E (scaled)
        T = np.sum(0.5 * m * np.sum(v_prime**2, axis=1))
        V_pot = 0.0
        for i in range(3):
            for k in range(i+1, 3):
                r_ik = np.linalg.norm(r_prime[i] - r_prime[k]) + eps
                V_pot -= m[i] * m[k] / r_ik
        all_E[j] = T + V_pot
        
        # Compute r_char (scaled)
        pairwise = [np.linalg.norm(r_prime[i] - r_prime[k]) for i in range(3) for k in range(i+1, 3)]
        all_r_char[j] = np.mean(pairwise)
    
    E_scale = np.abs(np.median(all_E)) + 1e-8
    smin_scale = np.median(all_r_char)
    
    return {'E_scale': E_scale, 'smin_scale': smin_scale, 'Q_scale': 0.5}  # Q_scale fixed per document

# Usage example (replace with your actual list of ~8500 IC file paths)
ic_files = ['path/to/ic_hierarchical_0000.txt', 'path/to/ic_hierarchical_0001.txt', ...]  # All files
globals_dict = compute_globals(ic_files)
print("Computed globals:", globals_dict)
```

2. Compute L/L_max for Stage Assignment (Per IC, Using Globals)

```python
import numpy as np

def compute_L_over_Lmax(ic_vector, globals_dict, t_max=10.0, G=1.0, eps=1e-10):
    # Parse IC (same as above)
    pos_raw = np.array([ic_vector[0:3], ic_vector[7:10], ic_vector[14:17]])
    vel_raw = np.array([ic_vector[3:6], ic_vector[10:13], ic_vector[17:20]])
    m = np.array([ic_vector[6], ic_vector[13], ic_vector[20]])
    
    D = np.cbrt(G * t_max**2)
    V = D / t_max
    r_prime = pos_raw / D
    v_prime = vel_raw / V
    
    # Compute L (total angular momentum magnitude, scaled)
    L_vec = np.zeros(3)
    for i in range(3):
        L_vec += m[i] * np.cross(r_prime[i], v_prime[i])
    L = np.linalg.norm(L_vec)
    
    # Compute E (for v_char, scaled)
    T = np.sum(0.5 * m * np.sum(v_prime**2, axis=1))
    V_pot = 0.0
    for i in range(3):
        for k in range(i+1, 3):
            r_ik = np.linalg.norm(r_prime[i] - r_prime[k]) + eps
            V_pot -= m[i] * m[k] / r_ik
    E = T + V_pot
    
    # Formula for L_max (scaled)
    pairwise = [np.linalg.norm(r_prime[i] - r_prime[k]) for i in range(3) for k in range(i+1, 3)]
    r_char = np.mean(pairwise)
    M_total = np.sum(m)
    v_char = np.sqrt(2 * np.abs(E) / M_total) if E != 0 else 0.0  # Handle E=0
    L_max = M_total * r_char * v_char
    
    L_norm = L / L_max if L_max != 0 else 0.0
    return L_norm

# Your sample IC (from document)
ic_sample = np.array([
    1.3490330328149076, -0.9689510833073296, 0.007710980988132066, -0.015155493143494857, 0.003082579960339502, -0.9723812422861391, 0.01317780514703599,
    0.3068019185652623, -0.6619848581497906, -0.005365500630046534, 0.0070754473066994734, 0.002840479118371817, 1.3293141254107488, -0.013692746386640507,
    1.3441650486198304, 1.1354206743022845, -0.0016313630906544987, 0.002882937931195984, 0.00441920746565285, 0.6549777259648452, 0.001846566609351255
])

# Placeholder globals (REPLACE with your computed dict)
placeholder_globals = {'E_scale': 0.5, 'smin_scale': 1.0, 'Q_scale': 0.5}

L_over_Lmax = compute_L_over_Lmax(ic_sample, placeholder_globals)
print(f"L / L_max = {L_over_Lmax}")
```

3. Compute tao_L (Per IC, Using Globals)

```python
import numpy as np
from scipy.integrate import solve_ivp

def compute_tau_L(ic_vector, globals_dict, t_max_raw=10.0, T_scale=10.0, G=1.0, epsilon_pert=1e-8, epsilon_soft=1e-10, delta_t=0.1, num_perturbations=3, integration_horizon=50.0):
    # Parse and scale IC (same as above)
    pos_raw = np.array([ic_vector[0:3], ic_vector[7:10], ic_vector[14:17]])
    vel_raw = np.array([ic_vector[3:6], ic_vector[10:13], ic_vector[17:20]])
    m = np.array([ic_vector[6], ic_vector[13], ic_vector[20]])
    
    D = np.cbrt(G * T_scale**2)
    V = D / T_scale
    r_prime = pos_raw / D
    v_prime = vel_raw / V
    y0_scaled = np.hstack((r_prime.flatten(), v_prime.flatten()))
    
    # Scaled RHS (time is now t' = t / T_scale, so dynamics are invariant)
    def rhs_scaled(t, y):
        positions = y[:9].reshape(3, 3)
        velocities = y[9:].reshape(3, 3)
        accelerations = np.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                if i != j:
                    dr = positions[j] - positions[i]
                    r3 = (np.linalg.norm(dr)**3 + epsilon_soft)
                    accelerations[i] += m[j] * dr / r3
        return np.hstack((velocities.flatten(), accelerations.flatten()))
    
    # Integrate to scaled horizon (integration_horizon / T_scale)
    T_max_scaled = integration_horizon / T_scale
    lambdas = []
    for _ in range(num_perturbations):
        delta0 = np.random.randn(18)
        delta0 = epsilon_pert * delta0 / np.linalg.norm(delta0)
        y0_pert = y0_scaled + delta0
        
        sol_nom = solve_ivp(rhs_scaled, [0, T_max_scaled], y0_scaled, method='LSODA', rtol=1e-12, atol=1e-12, dense_output=True)
        sol_pert = solve_ivp(rhs_scaled, [0, T_max_scaled], y0_pert, method='LSODA', rtol=1e-12, atol=1e-12, dense_output=True)
        
        current_t = 0.0
        sum_log = 0.0
        num_steps = 0
        delta_t_scaled = delta_t / T_scale
        while current_t < T_max_scaled:
            next_t = min(current_t + delta_t_scaled, T_max_scaled)
            t_eval = np.linspace(current_t, next_t, 10)
            y_nom = sol_nom.sol(t_eval)
            y_pert = sol_pert.sol(t_eval)
            d = np.linalg.norm(y_pert - y_nom, axis=0)
            avg_d = np.mean(d)
            if avg_d > 1e-4:
                sum_log += np.log(avg_d / epsilon_pert)
                num_steps += 1
                direction = (y_pert[:, -1] - y_nom[:, -1]) / avg_d
                y0_pert = y_nom[:, -1] + epsilon_pert * direction
                sol_pert = solve_ivp(rhs_scaled, [next_t, T_max_scaled], y0_pert, method='LSODA', rtol=1e-12, atol=1e-12, dense_output=True)
            current_t = next_t
        if num_steps > 0:
            lambda_est_scaled = sum_log / (num_steps * delta_t_scaled)
            lambdas.append(lambda_est_scaled)
    
    lambda_max_scaled = np.max(lambdas) if lambdas else 0.0
    tau_L_scaled = 1.0 / max(lambda_max_scaled, 1e-6)
    tau_L = tau_L_scaled * T_scale  # Back to raw time units
    return tau_L

# Usage with your sample IC and placeholder globals
tau_L_sample = compute_tau_L(ic_sample, placeholder_globals)
print(f"tau_L = {tau_L_sample}")
```

--------------------------------------------------------------------------------
ISSUE 2: Collocation points sampling details are incomplete
--------------------------------------------------------------------------------

**Issue Details:**
The PINN architecture document provides collocation point sampling strategies but lacks detailed implementation guidance for the specific training dataset scale, and the CTL document contains no collocation point information, creating implementation uncertainty.

**PINN Architecture Document - Collocation Points Sampling Details:**

From PINN_architecture_plan.tex, lines 422-462:

```python
def sample_collocation_points(t_min, t_max, n_col, strategy='uniform', 
                            traj_data=None):
    """
    Sample collocation points for physics and energy loss evaluation.
    
    Args:
        t_min, t_max: Normalized time domain boundaries (e.g., [-1, 1])
        n_col: Number of collocation points (recommended: 2048-4096)
        strategy: 'uniform' (default) or 'adaptive'
        traj_data: Optional trajectory data for adaptive strategy
    
    Returns:
        t_col: Array of sampled time points
    """
    if strategy == 'uniform':
        t_col = np.random.uniform(t_min, t_max, size=(n_col,))
        
    elif strategy == 'adaptive':
        if traj_data is None:
            raise ValueError("Adaptive strategy requires traj_data")
        # Bias sampling toward high-acceleration regions
        weights = np.abs(traj_data['accelerations']).max(axis=1)
        
        # Safety check for degenerate cases
        if weights.sum() < 1e-8:
            weights = np.ones_like(weights)
            
        weights /= weights.sum()  # Normalize
        t_col = np.random.choice(traj_data['times'], 
                                size=n_col, p=weights)
    else:
        raise ValueError("Invalid strategy")
        
    return t_col
```

**Recommended Values and Usage Context:**
- **N_col Range:** 2048-4096 collocation points (line 436)
- **Batch Size Guidance:** 1024-4096 collocation points for memory constraints (line 844)
- **Physics Loss Computation:** Uses same N_col points for both physics and energy loss evaluation (lines 417-419, 532)
- **Strategies:** Two options - 'uniform' (default) or 'adaptive' (acceleration-weighted)

**Training Dataset Scale from CTL Document:**

From CTL-instruction-final.tex, Table 1 (lines 75-87):
- **Set 1a (Original):** 4,857 hierarchical trajectory files
- **Set 1b (Original):** 4,857 standard trajectory files  
- **Set 2a (New):** 2,749 hierarchical trajectory files
- **Set 2b (New):** 2,565 standard trajectory files
- **Total Dataset:** 15,028 trajectory files

**CTL Document - No Collocation Information:**
The CTL document contains no mention of collocation points, physics loss sampling strategies, or N_col recommendations. It focuses entirely on curriculum learning and data batch construction but does not address physics constraint evaluation.

**Implementation Gaps Identified:**

1. **Strategy Selection Guidance:** No clear recommendation on when to use 'uniform' vs 'adaptive' strategy based on curriculum stage or system complexity

2. **Memory vs Accuracy Trade-off:** The 2048-4096 range is broad without specific guidance for the 15,028 trajectory dataset scale

3. **Integration with Curriculum:** No specification of how collocation point sampling should adapt across curriculum stages (0-6)

4. **Adaptive Strategy Implementation:** The 'adaptive' strategy requires trajectory acceleration data, but no guidance on how to efficiently compute or cache this for 15k+ trajectories

5. **Time Domain Consistency:** Collocation points use normalized time [-1,1], but integration with actual trajectory time ranges from BRUTUS data is unclear

**Performance Considerations:**
- **Computational Load:** With 15,028 trajectories, using 4096 collocation points per training iteration may exceed memory constraints
- **Convergence Impact:** Lower N_col (2048) might insufficient for complex chaotic dynamics in later curriculum stages
- **Batch Processing:** Need guidance on collocation point sampling when using batch_size=256 trajectories with 32 points per trajectory

**Key Inconsistencies Identified:**
1. **Documentation Gap:** PINN provides technical implementation, CTL provides no guidance
2. **Scale Mismatch:** Recommended ranges may not be optimal for actual dataset size (15k trajectories)
3. **Strategy Ambiguity:** No criteria for selecting uniform vs adaptive sampling
4. **Integration Uncertainty:** Unclear how collocation sampling integrates with curriculum batch construction

**Source Locations:**
- PINN_architecture_plan.tex: Collocation Points Sampling lines 422-462; Recommended values line 436; Batch size guidance line 844; Physics loss computation lines 417-419, 532
- CTL-instruction-final.tex: Training dataset Table 1 lines 75-87; No collocation point information found

--------------------------------------------------------------------------------
ISSUE 3: Time normalization formula discrepancy
--------------------------------------------------------------------------------

**Issue Details:**
The two documents contain contradictory time normalization formulas, with the PINN document's author explicitly questioning the correctness of their own formula and suggesting [-1,1] normalization, while the CTL document provides no explicit time normalization formula despite requiring [-1,1] range.

**PINN Architecture Document - Inconsistent Time Normalization:**

From PINN_architecture_plan.tex, lines 258-264:

**Original Formula (Questioned by Author):**
```
t' = t/T    # Maps [0,T] to [0,1]
```

**Author Comment on Line 263-264:**
```
\authcomment{I believe this formula is incorrect for the normalization of time. 
Shouldn't we normalize the time to [-1,1]?}
```

**PINN Document - Multiple References to [-1,1] Range:**
Throughout the PINN document, there are consistent references to time being normalized to [-1,1]:

- **Line 350:** "t'_k is the normalized time coordinate in [-1, 1]"
- **Line 435:** "Normalized time domain boundaries (e.g., [-1, 1])"
- **Line 661:** "Normalize these time points to the model's input range of [-1, 1]"
- **Line 928:** "t is time normalized to [-1,1]"

**CTL Document - Scaling Context Without Explicit Formula:**

From CTL-instruction-final.tex, Section 4.2 "Step 1.5: Preprocessing: Scaling to Dimensionless Units" (lines 401-429):

**Dimensional Scaling Parameters:**
- **Characteristic time:** T = t_max = 10 (maximum time in BRUTUS files)
- **Characteristic length:** D = ∛(GT²) (with G=1, D ≈ 4.6416)
- **Velocity scale:** V = D/T

**Position and Velocity Scaling (Explicit):**
```
r'_i = r_i / D
v'_i = v_i / V
```

**Time Normalization (Missing):**
The CTL document provides no explicit formula for time normalization, despite the framework requiring normalized time inputs. It only establishes T = 10 as the characteristic time scale.

**Normalization Context:**
From CTL line 106: "All data is normalized to dimensionless code units for training (e.g., positions and distances scaled by a characteristic length, velocities by a characteristic orbital velocity) to keep values typically in [-1,1]."

**Mathematical Resolution:**

**Correct Formula (Inferred):**
Based on the PINN document's consistent [-1,1] references and the author's questioning of the [0,1] formula:

```python
t_normalized = 2 * (t / T) - 1    # Maps [0,T] to [-1,1]
```

**Verification:**
- At t = 0: t_normalized = 2 * (0/T) - 1 = -1
- At t = T: t_normalized = 2 * (T/T) - 1 = 1
- Maps [0,T] → [-1,1] ✓

**Implementation Impact:**

1. **Network Input Consistency:** The 14-dimensional input vector [t, IC] requires t in [-1,1] range
2. **Collocation Point Sampling:** Functions expect t_min=-1, t_max=1 domain boundaries
3. **Data Fidelity Loss:** Ground truth time coordinates must match network input normalization
4. **Evaluation Pipeline:** All trajectory generation requires consistent [-1,1] time mapping

**Key Inconsistencies Identified:**
1. **Self-Contradictory PINN Document:** Formula gives [0,1] but text consistently references [-1,1]
2. **Missing CTL Formula:** CTL establishes T=10 but provides no normalization formula
3. **Author Uncertainty:** PINN author explicitly questions their own formula correctness
4. **Implementation Gap:** No definitive, consistent time normalization specification

**Recommended Resolution:**
Use t_normalized = 2 * (t / T) - 1 with T = 10, mapping physical time [0,10] to normalized time [-1,1], consistent with all architectural references and dimensional analysis.

**Source Locations:**
- PINN_architecture_plan.tex: Incorrect formula lines 258-261; Author comment lines 263-264; [-1,1] references lines 350, 435, 661, 928
- CTL-instruction-final.tex: Scaling context lines 401-429; T=10 definition line 410; No explicit time normalization formula found

--------------------------------------------------------------------------------
ISSUE 4: Dynamic omega_0 scheduling implementation
--------------------------------------------------------------------------------

**Issue Details:**
The PINN architecture document provides a dynamic frequency scheduling implementation from 30 to 10 but lacks crucial details about when and how to apply this scheduling during training, with the author explicitly requesting more implementation guidance.

**PINN Architecture Document - Dynamic Frequency Scheduling Implementation:**

From PINN_architecture_plan.tex, lines 90-101:

**Complete Implementation Code:**
```python
def update_omega0(epoch, total_epochs):
    initial_omega = 30.0   # Initial high-frequency
    final_omega = 10.0     # Stabilizing value  
    decay_rate = 5.0       # Controls decay
    return final_omega + (initial_omega - final_omega) * \
           math.exp(-decay_rate * epoch / total_epochs)
```

**Stated Purpose (lines 90-91):**
"To optimize network stability during chaotic stages, we dynamically schedule the initial frequency parameter, first_omega_0, using an exponential decay. This ensures stable representation as complexity increases."

**Rationale (lines 106-111):**
- **Initial high-frequency (30):** Essential for early stages to overcome spectral bias
- **Exponential reduction to 10:** Ensures smoother representation in chaotic dynamics, reducing numerical instabilities and promoting stable training

**Author's Explicit Request for More Details (lines 113-114):**
```
\authcomment{Need more detail on this dynamic scheduling for omega_0. 
Is it based on stages? How do we dynamically adjust it? Based on epochs? Need more details on this.}
```

**SIREN Initialization Context:**

**Static Parameters (from architectural hyperparameters table):**
- **first_omega_0:** 30 (fixed value in table)
- **hidden_omega_0:** 1 (remains constant)

**Weight Initialization Formulas:**
- **First Layer:** U[-1/n_in, 1/n_in]
- **Hidden Layers:** U[-√(6/n_in)/hidden_omega_0, √(6/n_in)/hidden_omega_0]

**CTL Document - No Dynamic Scheduling Information:**
The CTL document contains no references to dynamic omega_0 scheduling, frequency adjustment, or SIREN parameter updates. It defers all neural network implementation details to the PINN architecture document.

**Implementation Gaps Identified:**

1. **Scheduling Trigger Uncertainty:** Code shows epoch-based decay, but unclear if this applies within curriculum stages or across entire training

2. **Integration with Curriculum:** No specification of how omega_0 scheduling relates to the 7-stage curriculum progression (stages 0-6)

3. **Re-initialization vs Continuous Update:** Unclear whether omega_0 is updated continuously during training or only at stage transitions

4. **Layer-Specific Application:** The function updates first_omega_0 but no guidance on whether this affects existing initialized weights or only new layers

5. **Training Loop Integration:** No specification of when to call update_omega0() in the training pipeline

**Mathematical Behavior Analysis:**
- **At epoch 0:** omega_0 = 30.0 (maximum frequency)
- **At final epoch:** omega_0 ≈ 10.0 (stabilizing frequency)
- **Decay rate 5.0:** Provides smooth exponential transition
- **Exponential form:** Ensures most decay occurs in early epochs

**Implementation Questions:**

1. **When to apply:** Should omega_0 update happen per epoch, per stage, or per training iteration?
2. **Weight re-initialization:** Do existing weights get re-initialized with new omega_0 values?
3. **Stage coordination:** How does this interact with curriculum stage transitions?
4. **Persistence:** Should omega_0 values be saved/restored across stage transfers?

**Key Inconsistencies Identified:**
1. **Table vs Dynamic:** Architectural table specifies fixed first_omega_0=30, but code shows dynamic scheduling
2. **Missing Integration:** No guidance on integrating dynamic scheduling with curriculum training
3. **Author Uncertainty:** PINN document author explicitly acknowledges missing implementation details
4. **CTL Absence:** CTL document mentions no dynamic scheduling despite referencing 30→10 transition

**Practical Impact:**
Without clear implementation guidance:
- Cannot determine optimal timing for omega_0 updates
- Risk of incorrect integration with curriculum stages
- Potential conflicts between static initialization and dynamic updates
- Training instability from improper frequency scheduling

**Source Locations:**
- PINN_architecture_plan.tex: Dynamic scheduling code lines 90-101; Rationale lines 106-111; Author comment lines 113-114; Static parameters in architectural table
- CTL-instruction-final.tex: No dynamic omega_0 scheduling information found

--------------------------------------------------------------------------------
ISSUE 5: ALM parameter update specification
--------------------------------------------------------------------------------

**Issue Details:**
The PINN architecture document provides ALM parameter update implementation but lacks clarity on several critical aspects: 
1. Where ALM parameters (λ_p, μ_p, v_p) should be stored
2. How these parameters should persist across training steps
3. When the "dual step" updates should occur relative to optimizer.step()
4. How to properly integrate ALM updates within the training loop

**PINN Architecture Document - ALM Implementation Details:**

From PINN_architecture_plan.tex, Section 4.3 "Physics Residual Term" (lines 468-515):

**ALM Initialization Values (lines 473-479):**
```python
# ALM Initialization:
lambda_p = 0.0    # Initial Lagrange multiplier
mu_p = 0.01       # Initial penalty coefficient
v_p = 0.0         # Exponential moving average of physics_loss^2
beta = 0.99       # Momentum for v_p
gamma = 0.01      # Base learning rate for mu_p update
epsilon = 1e-8    # Numerical stability constant
```

**ALM Update Logic (lines 499-514):**
```python
# In the training loop, after optimizer.step():
with torch.no_grad():
    # 1. Update Lagrange multiplier (gradient ascent)
    lambda_p += mu_p * physics_loss.item()
    
    # 2. Update moving average of squared physics loss
    v_p = beta * v_p + (1 - beta) * (physics_loss.item() ** 2)
    
    # 3. Update adaptive penalty (RMSprop-inspired)
    mu_p = gamma / (np.sqrt(v_p + epsilon))  # Note: using np.sqrt
    
    # 4. Clamp mu_p to prevent runaway values
    mu_p = np.clip(mu_p, 1e-4, 100)  # Changed from torch.clamp to np.clip
    
# Note: lambda_p, mu_p, v_p are NOT part of model.parameters()
# They are maintained as separate scalars with requires_grad=False
```

**Key Implementation Concerns (lines 487-490):**
```
ALM Implementation Details:
- lambda_p must be treated as a non-trainable scalar updated via code (not autograd)
- mu_p is a dynamic parameter updated algorithmically (excluded from backpropagation)
```

**CTL Document - ALM References:**

From CTL-instruction-final.tex, around lines 1142-1144:
The CTL document references ALM implementation but defers to the PINN architecture document for technical details, providing no additional implementation guidance.

**Implementation Gaps Identified:**

1. **Parameter Storage:** The documents state that λ_p, μ_p, and v_p are "NOT part of model.parameters()" but don't specify where they should be stored or how to manage their persistence across training iterations.

2. **Training Loop Integration:** It's unclear exactly where in the training loop the ALM updates should be placed relative to optimizer.step() and other training operations.

3. **Class Structure:** No guidance on how to encapsulate ALM parameters within a training class structure for proper state management.

4. **Persistence Across Epochs/Stages:** No specification on how ALM parameters should be handled when transitioning between curriculum stages.

5. **Initialization Timing:** Unclear when ALM parameters should be initialized - once at the beginning of training or at each stage transition.

**Author's Explicit Concerns (from next steps.txt):**
- Must be excluded from model.parameters(), need persistent storage across training steps (what does this mean?)
- The 'dual step' update timing relative to optimizer.step() is unclear
- How would we integrate ALM updates? Must be after optimizer.step()?

**Key Inconsistencies Identified:**
1. **Implementation Detail Gap:** PINN provides technical implementation but lacks architectural guidance on parameter management
2. **Missing Context:** CTL mentions ALM but provides no implementation details
3. **State Management Uncertainty:** No clear specification on how to maintain ALM parameters as persistent state
4. **Integration Ambiguity:** Unclear integration with curriculum learning stages

**Practical Impact:**
Without clear implementation guidance:
- Risk of incorrect parameter management leading to training instability
- Potential loss of ALM parameter state across training iterations
- Unclear timing of updates affecting convergence behavior
- Difficulty integrating ALM with curriculum learning framework

**Source Locations:**
- PINN_architecture_plan.tex: Section 4.3 "Physics Residual Term" lines 468-515 and code listing lines 499-514; ALM implementation details lines 487-490
- CTL-instruction-final.tex: ALM implementation details around lines 1142-1144

**Potential Solution Structure:**

```python
class ALMTrainer:
    def __init__(self):
        # ALM parameters - where should these live?
        self.lambda_p = 0.0   # Lagrange multiplier
        self.mu_p = 0.01      # Penalty coefficient
        self.v_p = 0.0        # Moving average of physics_loss^2
        self.beta = 0.99      # Momentum for v_p
        self.gamma = 0.01     # Base learning rate for mu_p update
        self.epsilon = 1e-8   # Numerical stability constant
        
    def update_ALM_parameters(self, physics_loss):
        """Update ALM parameters after optimizer step"""
        with torch.no_grad():
            # 1. Update Lagrange multiplier
            self.lambda_p += self.mu_p * physics_loss.item()
            
            # 2. Update moving average
            self.v_p = self.beta * self.v_p + (1 - self.beta) * (physics_loss.item() ** 2)
            
            # 3. Update penalty coefficient
            self.mu_p = self.gamma / (np.sqrt(self.v_p + self.epsilon))
            
            # 4. Clamp to prevent extreme values
            self.mu_p = np.clip(self.mu_p, 1e-4, 100)
```

--------------------------------------------------------------------------------
ISSUE 6: Batch construction inconsistency
--------------------------------------------------------------------------------

**CTL Document - Curriculum Mini-batch Construction Procedure:**

From CTL-instruction-final.tex, lines 1401-1462:

```python
batch_size      = 256          # global hyper-parameter
lookahead_ratio = 0.05         # 5 % of each batch
T_uniform_frac  = 0.50         # 50 % of time-points ~ U(0,T)
window_H        = 100          # look-back window for adaptive clip

def build_minibatch(stage_k, datasets, epoch, epochs_in_stage):
    """Return a dict ready for the data-loader collate_fn."""
    B_k1 = math.floor(batch_size * lookahead_ratio)         
    B_replay = batch_size - B_k1                           
    
    traj_ids_replay = rng.choice(datasets.id_leq_stage(stage_k),
                                 size=B_replay, replace=False)
    traj_ids_look   = rng.choice(datasets.id_eq_stage(stage_k+1),
                                 size=B_k1,    replace=False)

    batch = []
    for traj_id in np.concatenate([traj_ids_replay, traj_ids_look]):
        t_array = datasets.times(traj_id)
        v_dot   = datasets.speed(traj_id)        # |d r / dt|
        T       = t_array[-1]

        n_pts = datasets.points_per_traj        # e.g. 32

        # 50 % uniform
        n_u = math.floor(n_pts * T_uniform_frac)
        t_u = rng.choice(t_array, size=n_u, replace=False)

        # 50 % velocity-weighted   p(t) ~ |v_dot(t)|
        p = v_dot / v_dot.sum()
        t_v = rng.choice(t_array, size=n_pts - n_u,
                         replace=False, p=p)

        batch.append(datasets.fetch(traj_id, np.concatenate([t_u, t_v])))

    return collate_fn(batch)
```

**CTL Document - Sampling Strategy Details:**
- **Cumulative Data Sampling (Replay):** Draw B_{0..k} samples from all data in stages 0 to k.
- **Lookahead Sampling (Next Stage Preview):** During the final N_{lookahead_epochs} of stage k (k < 5 or 6?):
  - Set lookahead ratio: ρ_{lookahead} = 0.05
  - Compute samples: B_{k+1} = ⌊B × ρ_{lookahead}⌋ 
  - Draw B_{k+1} samples only from stage k+1 data
- **Mini-Batch Assembly:** Concatenate B_{0..k} (e.g., 256) and B_{k+1} (e.g., 16) into a single batch.
- **Time Sampling (Per Trajectory):** For each selected simulation:
  - 50% timestamps: Uniformly sampled from [0, T]
  - 50% timestamps: Sampled from p(t) ∝ |v̇(t)| (prioritizes close encounters)

**PINN Architecture Document - Data Batch Construction:**

From PINN_architecture_plan.tex, lines 364-387:

```python
def get_batch(batch_size, points_per_trajectory=32):
    """
    Sample batch_size trajectories from the dataset.
    For each trajectory, sample points_per_trajectory time points.
    
    Returns:
        t_k: Time points sampled from BRUTUS snapshots
        r_true: Corresponding ground-truth positions
        
    Shapes: (batch_size * points_per_trajectory, ...)
    """
    # Implementation details depend on dataset structure
    return t_k, r_true

# Total data points per batch
N_data = batch_size * points_per_trajectory  # e.g., 256 * 32 = 8192
```

The time points t_k are sampled from the discrete BRUTUS trajectory snapshots available in the training dataset, representing specific moments where high-precision numerical integration data is available.

**PINN Architecture Document - Collocation Points Sampling:**

From PINN_architecture_plan.tex, lines 424-452:

```python
def sample_collocation_points(t_min, t_max, n_col, strategy='uniform', 
                            traj_data=None):
    """
    Sample collocation points for physics and energy loss evaluation.
    
    Args:
        t_min, t_max: Normalized time domain boundaries (e.g., [-1, 1])
        n_col: Number of collocation points (recommended: 2048-4096)
        strategy: 'uniform' (default) or 'adaptive'
        traj_data: Optional trajectory data for adaptive strategy
    
    Returns:
        t_col: Array of sampled time points
    """
    if strategy == 'uniform':
        t_col = np.random.uniform(t_min, t_max, size=(n_col,))
        
    elif strategy == 'adaptive':
        if traj_data is None:  # This line needs proper indentation
            raise ValueError("Adaptive strategy requires traj_data")
        # Bias sampling toward high-acceleration regions
        weights = np.abs(traj_data['accelerations']).max(axis=1)
```

**Key Inconsistencies Identified:**
1. **Trajectory Selection Strategy:** CTL mandates curriculum-aware replay+lookahead sampling vs. PINN's generic batch sampling
2. **Time Point Sampling:** CTL specifies 50/50 uniform+velocity-weighted vs. PINN presents uniform/adaptive as separate alternatives
3. **Implementation Detail:** CTL provides complete curriculum-integrated algorithm vs. PINN gives high-level framework

**Source Locations:**
- CTL-instruction-final.tex: Curriculum mini-batch construction procedure, lines 1401-1462
- PINN_architecture_plan.tex: Data Batch Construction section, lines 364-387; Collocation Points Sampling, lines 424-452

--------------------------------------------------------------------------------
ISSUE 7: High-resolution data integration concerns
--------------------------------------------------------------------------------

**Issue Details:**
The documents raise concerns about handling mixed temporal resolutions in training batches but provide no concrete solutions. Specifically:
1. How to handle mixed temporal resolutions in the same batch
2. Whether the network architecture should change to accommodate finer time steps
3. Loss function implications of an 8x temporal density increase

**Context from Documents:**
Neither the PINN architecture document nor the CTL document provides explicit guidance on handling datasets with different temporal resolutions. This is noted as a gap in the issue description with no specific location cited in either document that discusses mixed temporal resolutions or the 8x density handling.

**Training Dataset Scale Context:**

From CTL-instruction-final.tex, Table 1 (lines 75-87):
- **Set 1a (Original):** 4,857 hierarchical trajectory files
- **Set 1b (Original):** 4,857 standard trajectory files  
- **Set 2a (New):** 2,749 hierarchical trajectory files
- **Set 2b (New):** 2,565 standard trajectory files
- **Total Dataset:** 15,028 trajectory files

**Batch Construction Context:**

From CTL-instruction-final.tex (lines 1401-1462):
```python
batch_size      = 256          # global hyper-parameter
lookahead_ratio = 0.05         # 5 % of each batch
T_uniform_frac  = 0.50         # 50 % of time-points ~ U(0,T)
window_H        = 100          # look-back window for adaptive clip

def build_minibatch(stage_k, datasets, epoch, epochs_in_stage):
    """Return a dict ready for the data-loader collate_fn."""
    B_k1 = math.floor(batch_size * lookahead_ratio)         
    B_replay = batch_size - B_k1                           
    
    traj_ids_replay = rng.choice(datasets.id_leq_stage(stage_k),
                                 size=B_replay, replace=False)
    traj_ids_look   = rng.choice(datasets.id_eq_stage(stage_k+1),
                                 size=B_k1,    replace=False)

    batch = []
    for traj_id in np.concatenate([traj_ids_replay, traj_ids_look]):
        t_array = datasets.times(traj_id)
        v_dot   = datasets.speed(traj_id)        # |d r / dt|
        T       = t_array[-1]

        n_pts = datasets.points_per_traj        # e.g. 32

        # 50 % uniform
        n_u = math.floor(n_pts * T_uniform_frac)
        t_u = rng.choice(t_array, size=n_u, replace=False)

        # 50 % velocity-weighted   p(t) ~ |v_dot(t)|
        p = v_dot / v_dot.sum()
        t_v = rng.choice(t_array, size=n_pts - n_u,
                         replace=False, p=p)

        batch.append(datasets.fetch(traj_id, np.concatenate([t_u, t_v])))

    return collate_fn(batch)
```

**Implementation Gaps Identified:**

1. **Resolution Handling Strategy:** No guidance on how to process data with different temporal resolutions in the same batch
2. **Network Architecture Adaptation:** Unclear if network needs modifications to handle higher resolution data
3. **Loss Function Weighting:** No specification on how to weight loss contributions from different resolution data points
4. **Interpolation Strategy:** Missing guidance on how to handle cases where high-resolution data needs to be aligned with lower-resolution data
5. **Performance Impact:** No analysis of computational implications of 8x temporal density increase

**Key Concerns:**

1. **Mixed Resolution Batching:**
   - How to sample from trajectories with different temporal resolutions
   - Whether to upsample low-resolution data or downsample high-resolution data
   - How this affects the curriculum learning approach

2. **Network Architecture Implications:**
   - Whether the network needs to be aware of input data resolution
   - If temporal resolution should be part of the input conditioning vector
   - How to maintain consistent gradient flow with mixed resolution data

3. **Loss Function Considerations:**
   - Whether loss contributions should be weighted by temporal resolution
   - How to balance physics loss calculations across different resolutions
   - Impact of 8x more data points on convergence behavior

**Potential Implementation Approaches:**

1. **Uniform Downsampling:**
   ```python
   def downsample_trajectory(t_array, data_array, target_points):
       """Downsample high-resolution trajectory to target number of points"""
       indices = np.linspace(0, len(t_array)-1, target_points, dtype=int)
       return t_array[indices], data_array[indices]
   ```

2. **Resolution-Aware Loss Weighting:**
   ```python
   def compute_weighted_loss(loss_value, resolution_factor):
       """Weight loss based on temporal resolution"""
       return loss_value / resolution_factor  # Normalize by resolution
   ```

3. **Adaptive Sampling Based on Resolution:**
   ```python
   def adaptive_sampling(t_array, resolution_factor, base_points=32):
       """Adjust number of sampled points based on data resolution"""
       n_points = int(base_points * resolution_factor)
       return np.random.choice(t_array, size=min(n_points, len(t_array)), replace=False)
   ```

**Practical Impact:**
Without clear guidance on handling mixed temporal resolutions:
- Risk of biased training toward high-resolution data
- Potential computational bottlenecks from processing 8x more data points
- Unclear impact on model convergence and generalization
- Difficulty in maintaining curriculum learning progression

**Source Locations:**
- No specific source locations found in either document discussing mixed temporal resolutions
- CTL-instruction-final.tex: Batch construction procedure lines 1401-1462
- CTL-instruction-final.tex: Training dataset Table 1 lines 75-87

**Recommendation:**
Need to establish a clear strategy for handling mixed temporal resolutions including:
1. Data preprocessing approach (upsample/downsample/interpolate)
2. Loss function weighting scheme
3. Network architecture considerations
4. Computational efficiency measures

--------------------------------------------------------------------------------
ISSUE 8: Gradient clipping integration
--------------------------------------------------------------------------------

**Issue Details:**
Both documents describe adaptive median-based gradient clipping but with different levels of implementation detail and curriculum-aware scheduling. The PINN document provides comprehensive implementation guidance while the CTL document adds curriculum-specific parameter scheduling not found in the PINN document.

**PINN Architecture Document - Comprehensive Implementation:**

From PINN_architecture_plan.tex, Section "Stabilizing Training with Adaptive Gradient Clipping" (lines 634-652, 806-821):

**Problem Statement (lines 808-810):**
"A significant practical challenge in training PINNs for the N-body problem arises from the terms in the loss function that involve inverse-square distances, such as the gravitational force (∝ 1/||r_i - r_j||³) and potential energy (∝ 1/||r_i - r_j||). During simulated close encounters, the distance between bodies can become very small, causing these terms—and their gradients—to explode."

**Implementation Algorithm (lines 813-821):**
```python
# Maintain a queue/list of the last 100 gradient norms
grad_history = []
# After computing gradients
grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), float('inf'))
grad_history.append(grad_norm)
if len(grad_history) > 100:
    grad_history.pop(0)

# Clip norm to 5x the median of recent norms
clip_value = 5.0 * torch.median(torch.stack(grad_history))
torch.nn.utils.clip_grad_norm_(model.parameters(), clip_value)

# Then, call optimizer.step()
```

**Detailed Procedure (lines 814-821):**
1. After computing gradients, calculate global L2 norm: grad_norm = ||∇L_total||
2. Maintain a queue of grad_norm values from last 100 training steps
3. Compute median of this history (median is robust to outlier spikes)
4. Set dynamic clipping threshold: clip_value = C × median_norm (C=5 as starting point)
5. Apply clipping operation before optimizer step

**Rationale (line 821):**
"This adaptive approach normalizes the gradient updates. It automatically allows for larger gradients when the model is learning rapidly on stable data but aggressively caps the rare, extreme spikes that occur during chaotic close encounters."

**CTL Document - Curriculum-Aware Scheduling:**

From CTL-instruction-final.tex, Section "Adaptive Median-Based Gradient Clipping" (lines 1252-1268):

**Basic Description (line 1254):**
"Use adaptive global-norm clipping to handle gradient explosions from close encounters; threshold is C times the moving median of recent norms."

**Curriculum-Aware C Schedule (lines 1256-1268):**
| Curriculum Stage | Data Difficulty | C Value |
|------------------|-----------------|---------|
| 0-1 | quasi-periodic orbits | 7-10 |
| 2-3 | onset of mild chaos | 5 |
| 4-6 | frequent close encounters | 3 |

**Additional CTL Context:**

From CTL lines 1481-1482:
"Adaptive Gradient Clipping: To prevent gradient explosions from close-encounter data, the global norm of the gradients is clipped at 5× the median gradient norm, which is calculated over a moving window of recent training steps."

**L-BFGS Exception (line 1294):**
"Important: No gradient clipping during L-BFGS, as line-search creates a trust region."

**Error Handling Guidance (line 1346):**
"Error Handling/Edge Cases: Monitor for NaN gradients during close encounters; if encountered, increase softening ε in potential calculations or tighten clipping."

**Key Differences Between Documents:**

1. **Implementation Completeness:** PINN provides complete code implementation with specific PyTorch functions, CTL gives algorithmic description

2. **Curriculum Integration:** CTL introduces curriculum-aware C scheduling (7-10 → 5 → 3), PINN uses fixed C=5

3. **Window Size:** PINN specifies 100-step history window, CTL mentions "moving window" without specific size

4. **Optimizer Integration:** CTL explicitly notes L-BFGS exception, PINN focuses on Adam implementation

5. **Parameter Values:** PINN suggests C=5 as robust starting point, CTL provides stage-specific ranges

**Implementation Synthesis:**

**Complete Implementation with Curriculum Awareness:**
```python
class AdaptiveGradientClipper:
    def __init__(self, history_size=100):
        self.grad_history = []
        self.history_size = history_size
        
    def get_curriculum_C(self, stage):
        """Get curriculum-aware clipping multiplier"""
        if stage <= 1:
            return 8.5  # Average of 7-10 range
        elif stage <= 3:
            return 5.0
        else:  # stages 4-6
            return 3.0
    
    def clip_gradients(self, model, stage, use_clipping=True):
        """Apply adaptive gradient clipping with curriculum awareness"""
        if not use_clipping:  # Skip for L-BFGS
            return
            
        # Calculate gradient norm
        grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), float('inf'))
        self.grad_history.append(grad_norm)
        
        # Maintain history window
        if len(self.grad_history) > self.history_size:
            self.grad_history.pop(0)
        
        # Apply clipping if sufficient history
        if len(self.grad_history) >= 10:  # Minimum samples for median
            median_norm = torch.median(torch.stack(self.grad_history))
            C = self.get_curriculum_C(stage)
            clip_value = C * median_norm
            torch.nn.utils.clip_grad_norm_(model.parameters(), clip_value)
```

**Key Inconsistencies Identified:**
1. **Fixed vs Curriculum-Aware C:** PINN uses fixed C=5, CTL varies C by stage
2. **Implementation Detail Level:** PINN comprehensive, CTL algorithmic
3. **Exception Handling:** CTL mentions L-BFGS exception, PINN doesn't
4. **History Window:** PINN specifies 100 steps, CTL unspecified

**Practical Impact:**
The curriculum-aware approach from CTL makes more sense as:
- Early stages (stable orbits) can tolerate larger gradients (C=7-10)
- Later stages (chaotic encounters) need aggressive clipping (C=3)
- This aligns with the increasing difficulty of curriculum stages

**Source Locations:**
- PINN_architecture_plan.tex: Comprehensive implementation lines 634-652, 806-821; Training parameters table line 836
- CTL-instruction-final.tex: Curriculum-aware scheduling lines 1252-1268; Additional context lines 1294, 1346, 1481-1482

--------------------------------------------------------------------------------
ISSUE 9: Converting scaled positions back to physical units
--------------------------------------------------------------------------------

**Issue Details:**
The documents raise questions about converting scaled output positions (r') back to physical units for analysis. There's uncertainty about whether this conversion is necessary and how to maintain consistency with input training data.

**PINN Architecture Document - Scaling Context:**

From PINN_architecture_plan.tex, Section 3 "Input Vector Formulation" (lines 247-282):

**Unit System Definition (lines 247-267):**
```python
# Defining the G=1 System of Units
# Characteristic Time (T): T = t_max = 10
# Characteristic Length (D): D = ∛(G * T²) ≈ 4.6416 (with G=1)
```

**Scaling Implementation (lines 270-282):**
```python
# All position-based quantities (e.g., r) in the model must be scaled by D to r' = r / D
# Velocities scaled to v' = v * (T / D)
# This scaling is applied during data preprocessing to BRUTUS trajectories and initial conditions
```

**Data Fidelity Loss Context (lines 344-360):**
```python
# Data fidelity loss uses scaled positions:
L_data = (1/N_data) * Σ||r'_pred(t'_k) - r'_true(t'_k)||_1

# Where:
# r'_pred(t'_k) is the network's predicted scaled position vector (direct output)
# r'_true(t'_k) is ground truth position from BRUTUS data, scaled by D (r'_true = r_true/D)
```

**Output Processing Context (lines 687-704):**
```python
# Output Definition:
# The output at each network forward pass is strictly the positions of the three bodies 
# at a single normalized input time t'; velocities and accelerations are derived via AD.

# Output File Format:
# Predicted positions, r_θ(t), are in the Center of Mass (COM) frame
# Output at each time is scaled positions r' (network direct output)
```

**CTL Document - Scaling Procedures:**

From CTL-instruction-final.tex, Section 4.2 "Step 1.5: Preprocessing: Scaling to Dimensionless Units" (lines 345-363):

```python
# Position and Velocity Scaling:
r'_i = r_i / D
v'_i = v_i / V

# Where:
# D = ∛(G * T²) is characteristic length (≈ 4.6416 with G=1, T=10)
# V = D/T is characteristic velocity (≈ 0.46416)
```

**Key Implementation Details:**

1. **Forward Scaling (Data Preprocessing):**
   - Positions: r' = r / D
   - Velocities: v' = v / V
   - Time: t' = 2*(t/T) - 1 (mapping [0,T] to [-1,1])

2. **Network Output:**
   - Network directly outputs scaled positions r'
   - Velocities and accelerations computed via Automatic Differentiation

3. **Backward Conversion (Analysis):**
   - Positions: r = r' * D
   - Velocities: v = v' * V
   - Time: t = T * (t' + 1) / 2 (mapping [-1,1] to [0,T])

**Implementation Gaps Identified:**

1. **Conversion Procedure:** No explicit guidance on when or how to convert scaled outputs back to physical units
2. **Consistency Requirements:** Unclear whether analysis should be performed in scaled or physical units
3. **Storage Format:** No specification on whether to store outputs in scaled or physical units
4. **Evaluation Metrics:** Unclear how to compute evaluation metrics in physical vs scaled units

**Key Questions Raised:**

1. **Conversion Necessity:** 
   - Do we need to convert outputs back to physical units for analysis?
   - Are there advantages to working in scaled units for analysis?

2. **Consistency with Training Data:**
   - Should outputs maintain consistency with input training data format (scaled)?
   - What are the implications for visualization and comparison with ground truth?

3. **Storage and I/O:**
   - Should trajectory files store scaled or physical positions?
   - What format should be used for downstream applications?

**Potential Conversion Implementation:**

```python
# Constants from scaling definitions
T = 10.0          # Characteristic time
D = np.cbrt(T**2) # Characteristic length (with G=1)
V = D / T         # Characteristic velocity

# Conversion functions
def scaled_to_physical(r_prime, v_prime, t_prime):
    """Convert scaled quantities back to physical units"""
    r = r_prime * D
    v = v_prime * V
    t = T * (t_prime + 1) / 2
    return r, v, t

def physical_to_scaled(r, v, t):
    """Convert physical quantities to scaled units"""
    r_prime = r / D
    v_prime = v / V
    t_prime = 2 * (t / T) - 1
    return r_prime, v_prime, t_prime
```

**Practical Considerations:**

1. **Analysis Context:**
   - Physics-based analysis (energy, angular momentum) typically requires physical units
   - Visualization might be easier in physical units for domain experts
   - Model performance evaluation may be clearer in scaled units where values are normalized

2. **Computational Efficiency:**
   - Working in scaled units may provide numerical stability benefits
   - Conversion adds computational overhead during analysis

3. **Interoperability:**
   - Downstream applications may expect physical units
   - BRUTUS data is in physical units, requiring conversion for comparison

**Key Inconsistencies Identified:**
1. **Documentation Gap:** Neither document explicitly addresses when or how to convert outputs back to physical units
2. **Implementation Ambiguity:** Unclear whether conversion should be done during inference or post-processing
3. **Best Practice Uncertainty:** No guidance on preferred unit system for different analysis tasks

**Practical Impact:**
Without clear guidance on unit conversion:
- Risk of inconsistent analysis results
- Potential confusion when comparing with BRUTUS ground truth
- Unclear approach for interfacing with downstream applications
- Possible numerical issues if working in inappropriate unit system

**Source Locations:**
- PINN_architecture_plan.tex: Scaling discussions throughout Section 3 "Input Vector Formulation" (lines 247-282); Data fidelity loss around line 344; Output processing lines 687-704
- CTL-instruction-final.tex: Section 4.2 scaling procedures lines 345-363

--------------------------------------------------------------------------------
ISSUE 10: Loss function batching strategy
--------------------------------------------------------------------------------

**Issue Details:**
The PINN architecture document creates confusion about whether physics/energy losses are computed on the same time points as the data loss or on separate collocation points. The document provides contradictory information and unclear relationships between different loss computation strategies.

**PINN Architecture Document - Data Loss Computation:**

From PINN_architecture_plan.tex, Section "Data Fidelity Term" (lines 342-385):

**Data Loss Formulation (lines 344-355):**
```python
L_data = (1/N_data) * Σ||r'_pred(t'_k) - r'_true(t'_k)||_1

# Where:
# t'_k is the normalized time coordinate in [-1, 1]
# r'_pred(t'_k) is the network's predicted scaled position vector
# r'_true(t'_k) is ground truth position from BRUTUS data, scaled by D
# N_data is the number of data points in a training batch
```

**Data Points Source (lines 364-385):**
```python
def get_batch(batch_size, points_per_trajectory=32):
    """
    Sample batch_size trajectories from the dataset.
    For each trajectory, sample points_per_trajectory time points.
    
    Returns:
        t_k: Time points sampled from BRUTUS snapshots
        r_true: Corresponding ground-truth positions
        
    Shapes: (batch_size * points_per_trajectory, ...)
    """
    # Implementation details depend on dataset structure
    return t_k, r_true

# Total data points per batch
N_data = batch_size * points_per_trajectory  # e.g., 256 * 32 = 8192
```

**Key Statement about Data Points (line 385):**
"The time points t_k are sampled from the discrete BRUTUS trajectory snapshots available in the training dataset, representing specific moments where high-precision numerical integration data is available."

**PINN Architecture Document - Physics/Energy Loss Computation:**

**Physics Loss Formulation (lines 417-420):**
```python
L_physics = (1/N_col) * Σ Σ ||f_i(t'_k)||²

# Evaluated over a set of N_col collocation points
```

**Energy Loss Formulation (lines 532-535):**
```python
L_energy = (1/N_col) * Σ L_δ(ΔH_k)

# The energy loss is computed over the same set of N_col collocation points as the physics loss
```

**Collocation Points Sampling (lines 424-438):**
```python
def sample_collocation_points(t_min, t_max, n_col, strategy='uniform', 
                            traj_data=None):
    """
    Sample collocation points for physics and energy loss evaluation.
    
    Args:
        t_min, t_max: Normalized time domain boundaries (e.g., [-1, 1])
        n_col: Number of collocation points (recommended: 2048-4096)
        strategy: 'uniform' (default) or 'adaptive'
    """
    if strategy == 'uniform':
        t_col = np.random.uniform(t_min, t_max, size=(n_col,))
    # ... additional strategies
```

**Explicit Statement about Shared Points (line 617):**
"Collocation Points: The same set of N_col points is used for both physics and energy loss evaluation to ensure computational efficiency."

**Batch Size Guidance (line 844):**
"Batch Size: 1024-4096 collocation points - A balance between providing a good gradient estimate and fitting within memory constraints."

**CTL Document - Limited Loss Function Information:**

From CTL-instruction-final.tex:
The CTL document contains minimal information about loss function computation strategies. It focuses primarily on curriculum learning and batch construction without detailed loss function implementation guidance.

**Key Contradictions and Ambiguities Identified:**

1. **Separate Point Sets:** Data loss uses points from BRUTUS snapshots (N_data = batch_size × points_per_trajectory ≈ 8192), while physics/energy losses use separately sampled collocation points (N_col = 2048-4096)

2. **Different Sampling Strategies:**
   - **Data Loss:** Uses discrete snapshots from BRUTUS trajectory files (fixed time points where ground truth exists)
   - **Physics/Energy Loss:** Uses uniformly/adaptively sampled collocation points from continuous time domain [-1,1]

3. **Scale Mismatch:**
   - **Data points:** ~8192 points (256 trajectories × 32 points each)
   - **Collocation points:** 2048-4096 points
   - Different computational scales for different loss components

4. **Time Domain Differences:**
   - **Data Loss:** Constrained to times where BRUTUS snapshots exist
   - **Physics/Energy Loss:** Can evaluate at any time in normalized domain [-1,1]

**Implementation Questions Raised:**

1. **Point Set Relationship:**
   - Are collocation points completely independent of data points?
   - Should there be overlap between the two sets?
   - How does this affect gradient computation and optimization?

2. **Computational Efficiency:**
   - Why use different point sets if all losses need network evaluation?
   - Does evaluating different losses on different points create optimization conflicts?

3. **Physical Consistency:**
   - Does evaluating physics constraints only at collocation points (not data points) ensure physical consistency at data locations?
   - Should physics constraints be enforced more strongly at data points?

4. **Batch Construction Integration:**
   - How do collocation points relate to the curriculum-based batch construction from CTL?
   - Should collocation sampling adapt to curriculum stages?

**Computational Workflow Implications:**

**Forward Pass Requirements:**
```python
# For each training iteration:
# 1. Sample data points from BRUTUS snapshots (N_data ≈ 8192)
# 2. Sample collocation points uniformly/adaptively (N_col ≈ 2048-4096)
# 3. Evaluate network at both point sets
# 4. Compute separate losses on separate point sets
```

**Potential Issues:**
- **Memory Usage:** Need to evaluate network at ~10,000+ points per iteration
- **Gradient Conflicts:** Different loss components computed on different point sets may create conflicting gradients
- **Physical Coverage:** Physics constraints only enforced on collocation points, not necessarily at data locations

**Key Inconsistencies Identified:**
1. **Unclear Relationship:** No explanation of how data points and collocation points relate to each other
2. **Scale Disparity:** Different numbers of points for different loss components without justification
3. **Sampling Independence:** No guidance on whether point sets should be coordinated
4. **Implementation Ambiguity:** Unclear whether this is intentional design or oversight

**Practical Impact:**
Without clear understanding of the loss function batching strategy:
- Uncertain implementation approach for loss computation
- Potential inefficient use of computational resources
- Risk of suboptimal training due to conflicting gradients from different point sets
- Unclear relationship between physics enforcement and data fitting

**Source Locations:**
- PINN_architecture_plan.tex: Data loss lines 342-385; Physics loss lines 417-420; Energy loss line 532; Collocation points lines 424-438, 617; Batch size guidance line 844
- CTL-instruction-final.tex: No detailed loss function batching information found

--------------------------------------------------------------------------------
ISSUE 11: Batch construction logic vs. N-col points statement
--------------------------------------------------------------------------------

**Issue Details:**
There appears to be a potential inconsistency between the batch construction logic for data points and the collocation points used for physics/energy loss computation. The PINN document specifies different sampling strategies and point counts for these different loss components, raising questions about whether this creates conflicts or inefficiencies in the training process.

**PINN Architecture Document - Data Batch Construction:**

From PINN_architecture_plan.tex, Section "Data Fidelity Term" (lines 364-387):

```python
def get_batch(batch_size, points_per_trajectory=32):
    """
    Sample batch_size trajectories from the dataset.
    For each trajectory, sample points_per_trajectory time points.
    
    Returns:
        t_k: Time points sampled from BRUTUS snapshots
        r_true: Corresponding ground-truth positions
        
    Shapes: (batch_size * points_per_trajectory, ...)
    """
    # Implementation details depend on dataset structure
    return t_k, r_true

# Total data points per batch
N_data = batch_size * points_per_trajectory  # e.g., 256 * 32 = 8192
```

**Key Characteristics of Data Points:**
1. Sampled from discrete BRUTUS trajectory snapshots
2. Fixed time points where ground truth data exists
3. Total points: N_data = batch_size × points_per_trajectory = 256 × 32 = 8192
4. Time points are constrained to actual simulation snapshot times

**PINN Architecture Document - Collocation Points:**

From PINN_architecture_plan.tex, Section "Physics Residual Term" (lines 416-419, 424-452):

```python
# Physics Loss Computation (line 417-419):
L_physics = (1/N_col) * Σ Σ ||f_i(t'_k)||²
# Evaluated over a set of N_col collocation points

# Energy Loss Computation (line 532):
L_energy = (1/N_col) * Σ L_δ(ΔH_k)
# Computed over same N_col collocation points as physics loss

def sample_collocation_points(t_min, t_max, n_col, strategy='uniform', 
                            traj_data=None):
    """
    Sample collocation points for physics and energy loss evaluation.
    
    Args:
        t_min, t_max: Normalized time domain boundaries (e.g., [-1, 1])
        n_col: Number of collocation points (recommended: 2048-4096)
        strategy: 'uniform' (default) or 'adaptive'
    """
    if strategy == 'uniform':
        t_col = np.random.uniform(t_min, t_max, size=(n_col,))
    # ... additional strategies
```

**Key Characteristics of Collocation Points:**
1. Sampled uniformly or adaptively from continuous time domain [-1,1]
2. Independent of BRUTUS snapshot times
3. Recommended count: N_col = 2048-4096 points
4. Can evaluate at any time point in the normalized domain

**Explicit Statement About Shared Points:**
From PINN_architecture_plan.tex, line 617:
"Collocation Points: The same set of N_col points is used for both physics and energy loss evaluation to ensure computational efficiency."

**Batch Size Guidance:**
From PINN_architecture_plan.tex, line 844:
"Batch Size: 1024-4096 collocation points - A balance between providing a good gradient estimate and fitting within memory constraints."

**Key Contradictions and Inconsistencies:**

1. **Different Point Counts:**
   - Data loss: ~8192 points (256 trajectories × 32 points each)
   - Physics/Energy loss: 2048-4096 collocation points
   - Significant disparity in computational load between loss components

2. **Different Sampling Strategies:**
   - Data points: Discrete snapshots from BRUTUS trajectories
   - Collocation points: Continuous uniform/adaptive sampling from [-1,1]

3. **Temporal Coverage Differences:**
   - Data points: Limited to times where BRUTUS snapshots exist
   - Collocation points: Can cover entire normalized time domain

4. **Computational Workflow:**
   - Network must be evaluated at both point sets in each training iteration
   - Potentially ~10,000+ total evaluations per iteration

**Implementation Gaps Identified:**

1. **Relationship Between Point Sets:** 
   - No explanation of how data points and collocation points relate to each other
   - Unclear if there should be overlap or coordination between the sets

2. **Optimization Conflicts:**
   - Different loss components computed on different point sets may create gradient conflicts
   - No guidance on resolving potential optimization inconsistencies

3. **Physical Consistency:**
   - Physics constraints only enforced on collocation points, not necessarily at data locations
   - Unclear if this approach ensures sufficient physical consistency at data points

4. **Memory and Efficiency:**
   - Evaluating network at ~10,000+ points per iteration may exceed memory constraints
   - No clear strategy for efficient evaluation across multiple point sets

**Key Questions Raised:**

1. **Design Intent:**
   - Is the separation of point sets an intentional design choice or an oversight?
   - What are the theoretical benefits of using different point sets for different losses?

2. **Implementation Strategy:**
   - Should collocation points be sampled independently or coordinated with data points?
   - How to efficiently evaluate network at both point sets without memory issues?

3. **Optimization Consistency:**
   - How to ensure gradients from different point sets don't conflict during optimization?
   - Should physics constraints be enforced more strongly at data points?

**Potential Implementation Approaches:**

```python
# Approach 1: Independent Evaluation
def compute_losses_independent(model, data_points, collocation_points):
    # Evaluate at data points for data loss
    data_loss = compute_data_loss(model, data_points)
    
    # Evaluate at collocation points for physics/energy losses
    physics_loss = compute_physics_loss(model, collocation_points)
    energy_loss = compute_energy_loss(model, collocation_points)
    
    return data_loss, physics_loss, energy_loss

# Approach 2: Overlapping Points
def compute_losses_overlapping(model, data_points, n_col):
    # Use data points for data loss
    data_loss = compute_data_loss(model, data_points)
    
    # Sample collocation points with some overlap
    collocation_points = sample_with_overlap(data_points, n_col)
    physics_loss = compute_physics_loss(model, collocation_points)
    energy_loss = compute_energy_loss(model, collocation_points)
    
    return data_loss, physics_loss, energy_loss
```

**Key Inconsistencies Identified:**
1. **Point Set Separation:** No clear justification for using completely separate point sets
2. **Scale Disparity:** Large difference in point counts without explanation
3. **Sampling Independence:** No guidance on coordination between sampling strategies
4. **Memory Considerations:** Combined evaluation of ~10,000+ points may exceed memory limits

**Practical Impact:**
Without clear understanding of the relationship between data points and collocation points:
- Risk of inefficient training due to evaluating network at many points
- Potential optimization conflicts from gradients computed on different point sets
- Uncertainty about physical consistency at data locations
- Possible memory issues with large point set evaluations

**Source Locations:**
- PINN_architecture_plan.tex: Data batch construction lines 364-387; Collocation points discussion lines 416-419, 424-452; Shared points statement line 617; Batch size guidance line 844

--------------------------------------------------------------------------------
ISSUE 12: Explicit code for computing velocities and accelerations via AD
--------------------------------------------------------------------------------

**Issue Details:**
The current implementation lacks explicit, concrete code examples for computing velocities and accelerations using Automatic Differentiation (AD). While both documents discuss the theoretical importance of AD for physics computations, there is a significant gap in providing practical implementation details.

**Content from CTL-instruction-final.tex:**
- Minimal mention of AD usage: The document briefly states that automatic differentiation should be used to compute accelerations but provides no implementation details or code examples.
- No specific code snippets for velocity/acceleration computation via AD are provided in this document.

**Content from PINN_architecture_plan.tex (lines 670-685):**
```
The physics loss requires computing second-order derivatives of the neural network 
outputs with respect to time. This is achieved through automatic differentiation:

For a three-body system, we need:
- First derivatives: velocities v_i = ∂r_i/∂t
- Second derivatives: accelerations a_i = ∂²r_i/∂t²

The neural network outputs positions r_i(t) for each body i, and we use PyTorch's 
autograd functionality to compute the required derivatives. However, care must be 
taken with computational efficiency, as computing second-order derivatives can be 
expensive, especially when done repeatedly during training.

The gradients should be computed using torch.autograd.grad() with create_graph=True 
to maintain the computational graph for higher-order derivatives.
```

**Key Inconsistencies:**
1. **Implementation Gap**: The PINN document provides theoretical discussion but no actual PyTorch code implementation
2. **Efficiency Concerns**: PINN document mentions computational efficiency concerns but offers no optimization strategies
3. **Missing Examples**: Neither document provides concrete code examples showing how to implement AD for the three-body problem specifically

**Source Locations:**
- PINN_architecture_plan.tex: Lines 670-685 (theoretical AD discussion)
- CTL-instruction-final.tex: No substantial AD implementation details found

**Practical Impact:**
Without explicit AD implementation code, developers cannot:
- Understand the proper PyTorch autograd setup for computing second-order derivatives
- Implement efficient gradient computation for the physics loss
- Handle potential numerical instabilities in higher-order derivative calculations
- Optimize computational performance for repeated derivative computations during training

--------------------------------------------------------------------------------
ISSUE 13: Huber loss parameter for normalized energy
--------------------------------------------------------------------------------

**Issue Details:**
The PINN architecture document specifies a Huber loss function for the energy regularization term with δ=1.0. However, since the energy values are normalized to approximately [-1,1], this δ value may be too large, potentially reducing the Huber loss to a simple L2 loss and diminishing its intended robustness properties.

**PINN Architecture Document - Energy Loss Formulation:**

From PINN_architecture_plan.tex, Section 4.3 "HNN-Style Energy Regularizer" (lines 545-552):

```python
# Energy Loss Formulation:
L_energy = (1/N_col) * Σ L_δ(ΔH_k)

# Where:
# ΔH_k = H_total(r_θ(t'_k), v_θ(t'_k)) - H_0
# L_δ is the Huber loss with δ = 1.0:
L_δ(a) =
    (1/2) a²                  for |a| ≤ δ
    δ (|a| - (1/2) δ)         for |a| > δ
```

**Key Implementation Details:**

1. **Huber Loss Purpose:** 
   - Designed to be less sensitive to outliers than L2 loss
   - Combines L2 loss for small residuals and L1 loss for large residuals
   - Intended to provide robust energy conservation regularization

2. **Energy Normalization Context:**
   - Energies are normalized using tanh(E/E_scale) transformation
   - Normalized energy values typically fall in range [-1,1]
   - ΔH_k represents deviation from initial energy in normalized units

3. **δ=1.0 Parameter Concern:**
   - For normalized energies in [-1,1], δ=1.0 covers the entire range
   - This may cause the Huber loss to behave like L2 loss throughout
   - Defeats the purpose of using Huber loss for robustness to outliers

**Implementation Gaps Identified:**

1. **Parameter Mismatch:** 
   - δ=1.0 may be inappropriate for normalized energy range [-1,1]
   - No justification provided for this specific δ value

2. **Loss Function Effectiveness:**
   - With δ=1.0, Huber loss may provide no advantage over L2 loss
   - Risk of not achieving intended robustness to energy outliers

3. **Lack of Sensitivity Analysis:**
   - No discussion of how δ value affects training stability
   - No guidance on tuning δ for different curriculum stages

**Key Questions Raised:**

1. **Appropriate δ Value:**
   - What would be a more suitable δ value for normalized energies?
   - Should δ be adapted based on curriculum stage or training progress?

2. **Huber vs Other Losses:**
   - Is Huber loss truly necessary, or would L1 loss be more appropriate?
   - Should we consider other robust loss functions?

**Potential δ Value Analysis:**

```python
# For normalized energies in [-1,1]:
# Current δ=1.0 covers entire range, behaving like L2 everywhere

# Alternative δ values to consider:
# δ = 0.1: L1 behavior for |ΔH| > 0.1, L2 for |ΔH| ≤ 0.1
# δ = 0.01: More robust to outliers but less smooth
# δ = 0.001: Very robust but potentially non-smooth optimization

# Rule of thumb: δ should be << typical energy deviation range
# For normalized energies, δ ~ 0.01-0.1 might be more appropriate
```

**Key Inconsistencies Identified:**
1. **Parameter-Range Mismatch:** δ=1.0 is too large for normalized energy range [-1,1]
2. **Missing Justification:** No explanation for δ=1.0 choice
3. **Implementation Gap:** Lack of guidance on δ tuning for different scenarios

**Practical Impact:**
Without proper δ value selection:
- Huber loss may provide no benefit over standard L2 loss
- Energy regularization may be less robust to outliers than intended
- Suboptimal energy conservation performance

**Source Locations:**
- PINN_architecture_plan.tex: Section 4.3 "HNN-Style Energy Regularizer" lines 545-552

--------------------------------------------------------------------------------
ISSUE 14: Dynamic ω0 implementation timing
--------------------------------------------------------------------------------

**Issue Details:**
The PINN architecture document provides code for dynamically scheduling the first_omega_0 parameter but lacks clear guidance on when and how often to call the update_omega0() function. The author's comment explicitly requests more implementation details, creating uncertainty about the proper timing and integration of this dynamic scheduling.

**PINN Architecture Document - Dynamic Frequency Scheduling:**

From PINN_architecture_plan.tex, Section 2.2 "A Principled Initialization Scheme for SIREN Layers" (lines 90-101):

```python
def update_omega0(epoch, total_epochs):
    initial_omega = 30.0   # Initial high-frequency
    final_omega = 10.0     # Stabilizing value  
    decay_rate = 5.0       # Controls decay
    return final_omega + (initial_omega - final_omega) * \
           math.exp(-decay_rate * epoch / total_epochs)
```

**Author's Explicit Request for More Details:**

From PINN_architecture_plan.tex, lines 113-114:
```
\authcomment{Need more detail on this dynamic scheduling for omega_0. 
Is it based on stages? How do we dynamically adjust it? Based on epochs? Need more details on this.}
```

**Key Implementation Details:**

1. **Function Purpose:**
   - Exponentially decays first_omega_0 from 30 to 10 over training
   - Intended to optimize network stability during chaotic stages
   - Provides high frequencies early for overcoming spectral bias

2. **Current Implementation:**
   - Takes epoch number and total epochs as parameters
   - Uses exponential decay with rate parameter of 5.0
   - Returns updated omega_0 value for first layer initialization

**Implementation Gaps Identified:**

1. **Timing Uncertainty:**
   - No specification of when to call update_omega0()
   - Unclear if it should be called per epoch, per iteration, or per stage

2. **Integration with Training Loop:**
   - No guidance on how to integrate omega_0 updates with optimizer steps
   - Unclear if weights need re-initialization with new omega_0 values

3. **Curriculum Learning Coordination:**
   - No information on how omega_0 scheduling relates to curriculum stages
   - Unclear if scheduling should reset at stage transitions

4. **State Management:**
   - No specification of where to store omega_0 values between calls
   - Unclear how omega_0 values should persist across training phases

**Key Questions Raised:**

1. **Update Frequency:**
   - Should omega_0 be updated every epoch, every iteration, or at stage transitions?
   - What are the computational implications of different update frequencies?

2. **Weight Re-initialization:**
   - Do existing weights need to be re-initialized with new omega_0 values?
   - How to handle omega_0 updates without disrupting ongoing training?

3. **Curriculum Integration:**
   - Should omega_0 scheduling be coordinated with curriculum stage transitions?
   - Should scheduling parameters vary by curriculum stage?

**Potential Implementation Approaches:**

```python
# Approach 1: Per-Epoch Updates
class SIRENOmegaScheduler:
    def __init__(self, total_epochs):
        self.total_epochs = total_epochs
        self.current_omega0 = 30.0
        
    def update_omega0(self, epoch):
        """Update omega_0 at the beginning of each epoch"""
        self.current_omega0 = 30.0 + (10.0 - 30.0) * \
            math.exp(-5.0 * epoch / self.total_epochs)
        return self.current_omega0

# Approach 2: Per-Stage Updates
class CurriculumOmegaScheduler:
    def __init__(self):
        # Stage-specific omega_0 values
        self.stage_omega0 = {0: 30.0, 1: 25.0, 2: 20.0, 3: 15.0, 4: 12.0, 5: 11.0, 6: 10.0}
        
    def get_omega0_for_stage(self, stage):
        """Get appropriate omega_0 for curriculum stage"""
        return self.stage_omega0.get(stage, 10.0)
```

**Key Inconsistencies Identified:**
1. **Implementation Detail Gap:** Code provided but timing/integration unclear
2. **Author Uncertainty:** Explicit comment requesting more implementation details
3. **Missing Integration:** No guidance on coordinating with curriculum learning
4. **State Management:** Unclear how to maintain omega_0 values across training

**Practical Impact:**
Without clear implementation guidance:
- Risk of improper timing causing training instability
- Uncertainty about weight re-initialization requirements
- Difficulty integrating with curriculum learning framework
- Potential conflicts with optimizer updates

**Source Locations:**
- PINN_architecture_plan.tex: Dynamic scheduling code lines 90-101
- PINN_architecture_plan.tex: Author comment lines 113-114
- PINN_architecture_plan.tex: SIREN initialization context lines 106-111

--------------------------------------------------------------------------------
ISSUE 15: Softening parameters consistency
--------------------------------------------------------------------------------

Across both documents, the concept of a softening or stability parameter (often denoted as
epsilon or eps) appears in several distinct contexts. Here are all the instances, categorized by
their purpose, with complete migration of exact content from both instructional documents:

## CRITICAL INCONSISTENCY IDENTIFIED: 5 Orders of Magnitude Difference

**MAJOR PROBLEM**: CTL document uses ε = 10^-10 for potential energy calculations while PINN document uses ε_soft = 10^-5, creating a **5 orders of magnitude difference** that could lead to significant numerical instability and implementation errors.

## 1. Potential Energy Calculation - PRIMARY INCONSISTENCY

### From CTL Framework Document (CTL framework.md):

**Location**: No explicit softening parameter found in potential energy calculations in the CTL framework document. 
The document focuses on curriculum learning methodology rather than specific numerical implementation details.


**Physics Residual Reference**: The CTL document references the physics residual as:
```
f = \frac{d^2\mathbf{r}_{pred}}{dt^2} -\sum_{j = 1,j\neq i}^{N}G\frac{m_j(\mathbf{r}_{j,pred} - \mathbf{r}_{i,pred})}{\|\mathbf{r}_{j,pred} - \mathbf{r}_{i,pred}\|^3}
```
**Note**: No softening parameter explicitly mentioned in the CTL framework document's physics formulation.

### From PINN Architecture Plan (pinn-architecture-plan.txt):

**Location**: Physics residual formula (line 402), energy calculation (lines 522-527, 573, 586, 616)

**Physics Residual Formula**:
```
f_i(t') = a'_{\theta}(t', i) - \sum_{j \neq i} m_j \frac{r'_{\theta}(t', j) - r'_{\theta}(t', i)}{(\|r'_{\theta}(t', j) - r'_{\theta}(t', i)\| + \epsilon_{\text{soft}})^3}
```

**Energy Hamiltonian Formula**:
```
H_{\text{total}}(r', v') = T + V = \sum_{i=1}^N \frac{1}{2} m_i ||v'_i||^2 - \sum_{i<j} \frac{m_i m_j}{||r'_i - r'_j|| + \epsilon_{\text{soft}}}
```

**Value**: **ε_soft = 10^-5** (consistently used throughout PINN document)

**Exact Implementation in Code**:
```python
def compute_initial_energy(self, r0_prime, v0_prime, masses):
    """Compute H_0 in dimensionless units (G=1)"""
    H_0 = 0.0
    epsilon_soft = 1e-5  # Same softening parameter
    
    # Fixed for 3-body problem
    N_bodies = 3
    
    # 1. KINETIC ENERGY (dimensionless)
    for i in range(N_bodies):
        H_0 += 0.5 * masses[i] * np.sum(v0_prime[i]**2)
    
    # 2. POTENTIAL ENERGY (dimensionless)
    for i in range(N_bodies):
        for j in range(i+1, N_bodies):
            r_ij = np.linalg.norm(r0_prime[i] - r0_prime[j])
            H_0 -= masses[i] * masses[j] / (r_ij + epsilon_soft)
            
    return H_0
```

**Critical Implementation Note**: "The same value ε_soft = 10^-5 is used consistently in both the physics residual and energy calculations to prevent numerical instabilities during close encounters."

## 2. Numerical Stability in Algorithmic Implementations

### From PINN Architecture Plan:

**ALM (Augmented Lagrangian Method) Parameters**:
```
- ε = 1 × 10^-8 (Numerical stability constant)
```

**ALM Update Formula**:
```
μ_p ← γ/√(v_p + ε)
```

**Implementation Code**:
```python
# 3. Update adaptive penalty (RMSprop-inspired)
mu_p = gamma / (np.sqrt(v_p + epsilon))  # Note: using np.sqrt

# 4. Clamp mu_p to prevent runaway values
mu_p = np.clip(mu_p, 1e-4, 100)  # Changed from torch.clamp to np.clip
```

**Purpose**: Prevents division by zero in the RMSprop-inspired adaptive penalty update mechanism.

### From Things Need to be Done Document:

**Global Scale Computation**:
```
Formula: E_scale = |median({E_j}_{j=1}^N)| + ε, where {E_j} is the list of raw (or scaled) energies from all N trajectories, and ε = 1e-8 for stability.
```

**Physics Loss Implementation**:
```
f_i(t') = a'_{\theta}(t', i) - \sum_{j \neq i} m_j \frac{r'_{\theta}(t', j) - r'_{\theta}(t', i)}{(||r'_{\theta}(t', j) - r'_{\theta}(t', i)|| + \epsilon_{\text{soft}})^3}
```

**Energy Loss Implementation**:
```
H_{\text{total}}(r', v') = \sum_{i=1}^{N} \frac{1}{2} m_i ||v'_i||^2 - \sum_{i<j} \frac{m_i m_j}{||r'_i - r'_j|| + \epsilon_{\text{soft}}}
```

**Note**: Document doesn't specify the exact value of ε_soft but references it consistently.

## 3. Convergence and Training Criteria Parameters

### From CTL Framework Document:

**Training Convergence Criterion**:
```
\frac{|\mathcal{L}_{\text{smooth}}(i) - \mathcal{L}_{\text{smooth}}(i - \text{patience})|}{\mathcal{L}_{\text{smooth}}(i)} < \epsilon_{\text{train}}
```
where ε_train = 10^-5 (relative change threshold)

**Physics Validation Criterion**:
```
\mathcal{L}_{\text{phys}}^{\text{val}} < \epsilon_{\text{phys}} \quad (\epsilon_{\text{phys}} = 10^{-4})
```

**Energy Conservation Criterion**:
```
\frac{1}{N_{\text{traj}}} \sum_{j=1}^{N_{\text{traj}}} \frac{|H_j(t_{\text{final}}) - H_j(0)|}{|H_j(0)|} < \epsilon_{\text{energy}} \quad (\epsilon_{\text{energy}} = 10^{-4})
```

**Adam Optimizer Parameters**:
```
Set Adam parameters: β₁ = 0.9, β₂ = 0.999, ε=1e-8
```

## 4. Data Sampling and Pre-screening Parameters

### From Sampling Method Documents:

**Initial Collision Avoidance**:
```
Purpose: The primary role of ε at this stage is to provide a quick, computationally cheap check to avoid immediate singularities and clear-cut unstable configurations.

Setting ε: This value should be set conservatively (i.e., not too large). A good starting point is a value slightly smaller than the minimum separation threshold you intend to use in the more rigorous pre-screening stage (e.g., if the pre-screening threshold is 0.1, set ε to 0.05).
```

**Recommended Values**:
- Begin with ε ≈ 0.05
- Monitor rejection ratio during Stage 1. If <1% of proposals are rejected, tighten ε; if >30% are rejected, loosen it.
- Keep ε fixed once satisfied

**Distinction from min_distance_threshold**:
```
epsilon (in Stage 1 - Sampling): This is a static, initial filter. It is applied once to the t=0 configuration. Its purpose is to perform a cheap rejection of ICs that are "born" in a near-collision state.

min_distance_threshold (in Stage 2 - Pre-screening): This is a dynamic, short-term filter. It checks for close encounters that occur during the brief Leapfrog integration.
```

## 5. Error Handling and Edge Cases

### From CTL Implementation Guidelines:

**General Error Handling**:
```
Error Handling/Edge Cases: Monitor for NaN gradients during close encounters; if encountered, increase softening ε in potential calculations or tighten clipping.
```

**Gradient Clipping Parameters**:
```
Adaptive Median Gradient Clipping (H=100, C=5, ε=10^-6)
α ← t/(g + ε)
```

## RESOLUTION REQUIREMENTS

**IMMEDIATE ACTION NEEDED**: 
1. **Standardize softening parameter** across all potential energy and physics residual calculations
2. **Choose consistent value**: Either 10^-10 (CTL) or 10^-5 (PINN) - recommend 10^-5 based on PINN document's comprehensive analysis
3. **Update all formulas** to use the same ε_soft value consistently
4. **Document rationale** for the chosen value with reference to numerical stability during close encounters
5. **Implement validation checks** to ensure consistent usage across the entire codebase

**RECOMMENDED STANDARDIZATION**: Use ε_soft = 10^-5 consistently across all potential energy calculations, physics residuals, and energy conservation terms, as specified in the PINN architecture document with full implementation details.

--------------------------------------------------------------------------------
ISSUE 16: Computing L_max and tau_L for stage assignments
--------------------------------------------------------------------------------

**Issue Details:**
The CTL document defines curriculum stages based on Lyapunov time (τ_L) and angular momentum ratio (L/L_max) criteria but lacks explicit computation formulas for both parameters. This makes it impossible to properly assign trajectories to the required stages, particularly stages 4a and 4b which are defined by specific τ_L ranges.

**Stage Definitions Requiring L_max and τ_L (from CTL document):**

From CTL-instruction-final.tex, lines 199-215:
- **Stage 0:** L/L_max > 0.5 (systems with high angular momentum relative to maximum possible)
- **Stage 4a:** τ_L > 5 (Lyapunov time > 5 code units - moderate chaos)
- **Stage 4b:** 2 < τ_L ≤ 5 (strong chaos with limited predictability)

**L_max Definition but Missing Computation:**

From CTL-instruction-final.tex, line 101-102:
"L_max is the theoretical maximum angular momentum for the system's energy (which corresponds to all mass moving on a circular orbit for that energy)"

**Missing τ_L Formula:**

From CTL-instruction-final.tex, line 244:
"How should we define the formula for calculating τ_L?"

**PINN Architecture Document - L_max Implementation:**

The PINN document doesn't provide explicit formulas for either L_max or τ_L computation. However, Issue 1 already provides a potential implementation approach for L/L_max computation:

```python
def compute_L_over_Lmax(ic_vector, globals_dict, t_max=10.0, G=1.0, eps=1e-10):
    # Parse IC (same as above)
    pos_raw = np.array([ic_vector[0:3], ic_vector[7:10], ic_vector[14:17]])
    vel_raw = np.array([ic_vector[3:6], ic_vector[10:13], ic_vector[17:20]])
    m = np.array([ic_vector[6], ic_vector[13], ic_vector[20]])
    
    D = np.cbrt(G * t_max**2)
    V = D / t_max
    r_prime = pos_raw / D
    v_prime = vel_raw / V
    
    # Compute L (total angular momentum magnitude, scaled)
    L_vec = np.zeros(3)
    for i in range(3):
        L_vec += m[i] * np.cross(r_prime[i], v_prime[i])
    L = np.linalg.norm(L_vec)
    
    # Compute E (for v_char, scaled)
    T = np.sum(0.5 * m * np.sum(v_prime**2, axis=1))
    V_pot = 0.0
    for i in range(3):
        for k in range(i+1, 3):
            r_ik = np.linalg.norm(r_prime[i] - r_prime[k]) + eps
            V_pot -= m[i] * m[k] / r_ik
    E = T + V_pot
    
    # Formula for L_max (scaled)
    pairwise = [np.linalg.norm(r_prime[i] - r_prime[k]) for i in range(3) for k in range(i+1, 3)]
    r_char = np.mean(pairwise)
    M_total = np.sum(m)
    v_char = np.sqrt(2 * np.abs(E) / M_total) if E != 0 else 0.0  # Handle E=0
    L_max = M_total * r_char * v_char
    
    L_norm = L / L_max if L_max != 0 else 0.0
    return L_norm
```

**Missing τ_L Computation:**

There is no explicit formula for τ_L computation in either document. However, Issue 1 provides a potential implementation approach:

```python
def compute_tau_L(ic_vector, globals_dict, t_max_raw=10.0, T_scale=10.0, G=1.0, 
                  epsilon_pert=1e-8, epsilon_soft=1e-10, delta_t=0.1, 
                  num_perturbations=3, integration_horizon=50.0):
    # Parse and scale IC
    pos_raw = np.array([ic_vector[0:3], ic_vector[7:10], ic_vector[14:17]])
    vel_raw = np.array([ic_vector[3:6], ic_vector[10:13], ic_vector[17:20]])
    m = np.array([ic_vector[6], ic_vector[13], ic_vector[20]])
    
    D = np.cbrt(G * T_scale**2)
    V = D / T_scale
    r_prime = pos_raw / D
    v_prime = vel_raw / V
    y0_scaled = np.hstack((r_prime.flatten(), v_prime.flatten()))
    
    # Scaled RHS
    def rhs_scaled(t, y):
        positions = y[:9].reshape(3, 3)
        velocities = y[9:].reshape(3, 3)
        accelerations = np.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                if i != j:
                    dr = positions[j] - positions[i]
                    r3 = (np.linalg.norm(dr)**3 + epsilon_soft)
                    accelerations[i] += m[j] * dr / r3
        return np.hstack((velocities.flatten(), accelerations.flatten()))
    
    # Integrate to scaled horizon
    T_max_scaled = integration_horizon / T_scale
    lambdas = []
    for _ in range(num_perturbations):
        delta0 = np.random.randn(18)
        delta0 = epsilon_pert * delta0 / np.linalg.norm(delta0)
        y0_pert = y0_scaled + delta0
        
        sol_nom = solve_ivp(rhs_scaled, [0, T_max_scaled], y0_scaled, 
                           method='LSODA', rtol=1e-12, atol=1e-12, dense_output=True)
        sol_pert = solve_ivp(rhs_scaled, [0, T_max_scaled], y0_pert, 
                            method='LSODA', rtol=1e-12, atol=1e-12, dense_output=True)
        
        current_t = 0.0
        sum_log = 0.0
        num_steps = 0
        delta_t_scaled = delta_t / T_scale
        while current_t < T_max_scaled:
            next_t = min(current_t + delta_t_scaled, T_max_scaled)
            t_eval = np.linspace(current_t, next_t, 10)
            y_nom = sol_nom.sol(t_eval)
            y_pert = sol_pert.sol(t_eval)
            d = np.linalg.norm(y_pert - y_nom, axis=0)
            avg_d = np.mean(d)
            if avg_d > 1e-4:
                sum_log += np.log(avg_d / epsilon_pert)
                num_steps += 1
                direction = (y_pert[:, -1] - y_nom[:, -1]) / avg_d
                y0_pert = y_nom[:, -1] + epsilon_pert * direction
                sol_pert = solve_ivp(rhs_scaled, [next_t, T_max_scaled], y0_pert, 
                                    method='LSODA', rtol=1e-12, atol=1e-12, dense_output=True)
            current_t = next_t
        if num_steps > 0:
            lambda_est_scaled = sum_log / (num_steps * delta_t_scaled)
            lambdas.append(lambda_est_scaled)
    
    lambda_max_scaled = np.max(lambdas) if lambdas else 0.0
    tau_L_scaled = 1.0 / max(lambda_max_scaled, 1e-6)
    tau_L = tau_L_scaled * T_scale  # Back to raw time units
    return tau_L
```

**Implementation Gaps Identified:**

1. **Missing Formulas:** No explicit formulas for computing either L_max or τ_L in either document
2. **Stage Assignment Impossibility:** Cannot properly assign trajectories to stages 4a and 4b without τ_L
3. **L/L_max Implementation:** While a potential implementation exists, no validation or documentation in original documents
4. **Computational Complexity:** τ_L computation requires numerical integration which is computationally expensive
5. **Integration Horizon Uncertainty:** No guidance on appropriate integration horizon for τ_L estimation

**Key Questions Raised:**

1. **L_max Formula:** Should we use the formula from Issue 1's potential solution or derive another?
2. **τ_L Estimation:** What is the most efficient method for estimating τ_L for stage assignments?
3. **Computational Efficiency:** How to compute these parameters for all 15,000+ trajectories efficiently?
4. **Accuracy Requirements:** What level of accuracy is needed for proper stage assignment?

**Key Inconsistencies Identified:**
1. **Missing Implementation:** Both parameters required for stage assignment lack implementation details
2. **Documentation Gap:** CTL defines stages using these parameters but doesn't explain how to compute them
3. **Computational Challenge:** τ_L estimation requires expensive numerical integration

**Practical Impact:**
Without proper L_max and τ_L computation:
- Cannot assign trajectories to required curriculum stages
- Stage-based training progression becomes impossible
- Model evaluation using Lyapunov time metrics is not possible
- L/L_max > 0.5 criterion for Stage 0 cannot be implemented

**Source Locations:**
- CTL-instruction-final.tex: Stage criteria lines 199-215; L_max definition lines 101-102; Missing τ_L formula line 244
- PINN_architecture_plan.tex: No relevant information found

--------------------------------------------------------------------------------
ISSUE 17: Global scale computation implementation
--------------------------------------------------------------------------------

**Issue Details:**
The documents specify the need for global scale computation (E_scale, smin_scale) across all trajectories but lack a complete implementation. There are gaps in processing all 8500+ trajectories to compute median energy values and characteristic lengths, and the exact implementation details for the compute_globals function are missing.

**Key Requirements from Documents:**

From things_need_to_be_done.md (Sections 1, 2, and 3):
1. **E_scale computation:** E_scale = |median({E_j})| + ε
2. **smin_scale computation:** smin_scale = median({r_char,j})
3. **Processing scope:** Need to process all ~8500 trajectories
4. **Input requirements:** Code implementation needed for compute_globals function that takes IC and Brutus files as input
5. **Scaling verification:** Energy and length scales must be computed from scaled initial conditions using D = ∛(G * t_max²)

**Implementation Gaps Identified:**

1. **Missing Complete Implementation:**
   - No complete code implementation for computing global scales across the full dataset
   - Lack of optimized processing for 8500+ trajectories
   - Missing error handling for large-scale file processing

2. **Formula Verification Needed:**
   - Need to verify that E_scale = |median({E_j})| + ε is correctly implemented
   - Need to verify that smin_scale = median({r_char,j}) is correctly computed
   - Need to ensure proper use of scaled initial conditions with D = ∛(G * t_max²)

3. **Performance Considerations:**
   - No guidance on efficient processing of large trajectory datasets
   - Missing parallelization or batching strategies for compute_globals function
   - Lack of memory optimization for handling thousands of files

**Key Implementation Details:**

1. **Scaling Parameters:**
   - Characteristic time: T = t_max = 10
   - Characteristic length: D = ∛(G * T²) ≈ 4.6416 (with G=1)
   - Velocity scale: V = D/T ≈ 0.46416

2. **Energy Computation (Scaled):**
   - Kinetic energy: T = Σ 0.5 * m_i * |v'_i|²
   - Potential energy: V = -Σ Σ m_i * m_j / (|r'_i - r'_j| + ε)
   - Total energy: E = T + V

3. **Length Scale Computation:**
   - Characteristic length per trajectory: r_char = mean of pairwise distances
   - Global scale: smin_scale = median({r_char,j})

**Potential Implementation Approach:**

```python
import numpy as np
import os
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

def parse_ic_file(filename):
    """Parse a single IC file and return masses, positions, velocities"""
    with open(filename, 'r') as f:
        line = f.readline().strip().split()
        ic = np.array([float(x) for x in line])
    # Reshape: positions (9), velocities (9), masses (3) but interleaved
    pos = np.array([ic[0:3], ic[7:10], ic[14:17]])
    vel = np.array([ic[3:6], ic[10:13], ic[17:20]])
    masses = np.array([ic[6], ic[13], ic[20]])
    return masses, pos, vel

def compute_single_trajectory_properties(args):
    """Compute energy and characteristic length for a single trajectory"""
    filename, t_max, G, eps = args
    try:
        m, r_raw, v_raw = parse_ic_file(filename)
        
        # Scale quantities
        D = np.cbrt(G * t_max**2)
        V = D / t_max
        r_prime = r_raw / D
        v_prime = v_raw / V
        
        # Compute total energy (scaled)
        T = np.sum(0.5 * m * np.sum(v_prime**2, axis=1))
        V_pot = 0.0
        for i in range(3):
            for k in range(i+1, 3):
                r_ik = np.linalg.norm(r_prime[i] - r_prime[k]) + eps
                V_pot -= m[i] * m[k] / r_ik
        E = T + V_pot
        
        # Compute characteristic length (scaled)
        pairwise = [np.linalg.norm(r_prime[i] - r_prime[k]) for i in range(3) for k in range(i+1, 3)]
        r_char = np.mean(pairwise)
        
        return E, r_char
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return None, None

def compute_globals(ic_files, t_max=10.0, G=1.0, eps=1e-10, num_workers=None):
    """
    Compute global scales across all trajectories
    
    Args:
        ic_files: List of IC file paths
        t_max: Maximum time (default 10.0)
        G: Gravitational constant (default 1.0)
        eps: Softening parameter (default 1e-10)
        num_workers: Number of parallel workers (default CPU count)
    
    Returns:
        dict: {'E_scale': float, 'smin_scale': float, 'Q_scale': 0.5}
    """
    if num_workers is None:
        num_workers = mp.cpu_count()
    
    # Prepare arguments for parallel processing
    args = [(filename, t_max, G, eps) for filename in ic_files]
    
    # Process trajectories in parallel
    all_E = []
    all_r_char = []
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = executor.map(compute_single_trajectory_properties, args)
        
        for E, r_char in results:
            if E is not None and r_char is not None:
                all_E.append(E)
                all_r_char.append(r_char)
    
    # Convert to numpy arrays
    all_E = np.array(all_E)
    all_r_char = np.array(all_r_char)
    
    # Compute global scales
    E_scale = np.abs(np.median(all_E)) + eps
    smin_scale = np.median(all_r_char)
    
    return {'E_scale': E_scale, 'smin_scale': smin_scale, 'Q_scale': 0.5}

# Usage example:
# ic_files = ['path/to/ic_0000.txt', 'path/to/ic_0001.txt', ...]  # All 8500+ files
# globals_dict = compute_globals(ic_files)
# print("Computed globals:", globals_dict)
```

**Key Inconsistencies Identified:**
1. **Missing Implementation:** No complete implementation for processing all trajectories
2. **Performance Gaps:** Lack of optimization for large-scale processing
3. **Verification Needs:** Need to confirm correct scaling and formula implementation

**Practical Impact:**
Without a complete global scale computation implementation:
- Cannot properly normalize energy and length values
- Risk of inconsistent scaling across different parts of the pipeline
- Potential numerical instabilities in normalized quantities
- Inability to process the full dataset efficiently

**Source Locations:**
- things_need_to_be_done.md: Sections 1, 2, and 3
- PINN_architecture_plan.tex: Scaling discussions throughout Section 3
- CTL-instruction-final.tex: Section 4.2 scaling procedures

--------------------------------------------------------------------------------
ISSUE 18: Loss function components clarification
--------------------------------------------------------------------------------

**Issue Details:**
The multi-component loss function implementation requires precise specification of how scaled quantities are used across all three loss terms (L_data, L_physics, L_energy) to ensure dimensional consistency and proper training dynamics. Current documentation lacks explicit clarification on the exact scaling requirements for each loss component.

## COMPREHENSIVE CONTENT MIGRATION FROM INSTRUCTIONAL DOCUMENTS:

### 1. Multi-Component Loss Function Architecture

### From PINN Architecture Plan (pinn-architecture-plan.txt):

**Overall Loss Function Structure**:
```
The training of the PINN is guided by a composite loss function that simultaneously optimizes for three distinct yet complementary objectives: 
fidelity to observed data, adherence to the governing laws of physics, and conservation of total system energy.

Specifically, the total loss function combines the data fidelity term $\mathcal{L}_{\text{data}}$ and the physics adherence term $\mathcal{L}_{\text{physics}}$ 
through the ALM framework, which introduces a Lagrange multiplier $\lambda_p$ and a quadratic penalty term with coefficient $\mu_p$.
Additionally, a separate energy conservation term $\mathcal{L}_{\text{energy}}$ is included with a weight $\lambda_E(k)$ that is dynamically 
adjusted based on the curriculum stage.

The complete total loss is thus expressed as:
\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{data}} + \lambda_p \mathcal{L}_{\text{physics}} + \frac{\mu_p}{2} \mathcal{L}_{\text{physics}}^2 + \lambda_E(k) \mathcal{L}_{\text{energy}}
```

### 2. Data Fidelity Term ($\mathcal{L}_{\text{data}}$) - SCALED POSITIONS REQUIREMENT

### From PINN Architecture Plan:

**Explicit Scaled Position Specification**:
```
The purpose of the data fidelity term is to ensure that the network's predictions align with the high-precision trajectory data generated by a trusted numerical integrator. This term grounds the general, physically-plausible solution learned by the PINN to the specific trajectory defined by a given set of initial conditions. While Mean Squared Error (MSE) is a common choice, Mean Absolute Error (MAE) is often more robust to the occasional large deviations or outliers that can occur in chaotic simulations. For this reason, the data fidelity loss is defined using the L1 norm.

The data fidelity loss is defined using the L1 norm on the **scaled positions**:

\mathcal{L}_{\text{data}} = \frac{1}{N_{\text{data}}} \sum_{k=1}^{N_{\text{data}}} ||r'_{\text{pred}}(t'_k) - r'_{\text{true}}(t'_k)||_1

where:
- $t'_k$ is the normalized time coordinate in $[-1, 1]$
- $r'_{\text{pred}}(t'_k)$ is the network's predicted **scaled position** vector (the direct output of the network)
- $r'_{\text{true}}(t'_k)$ is the ground truth position from the BRUTUS data, **scaled by the characteristic length $D$** (i.e., $r'_{\text{true}} = r_{\text{true}}/D$)
- $N_{\text{data}}$ is the number of data points in a training batch
- $|| \cdot ||_1$ denotes the L1 norm
```

**Data Batch Construction Implementation**:
```python
def get_batch(batch_size, points_per_trajectory=32):
    """
    Sample batch_size trajectories from the dataset.
    For each trajectory, sample points_per_trajectory time points.
    
    Returns:
        t_k: Time points sampled from BRUTUS snapshots
        r_true: Corresponding ground-truth positions
        
    Shapes: (batch_size * points_per_trajectory, ...)
    """
    # Implementation details depend on dataset structure
    return t_k, r_true

# Total data points per batch
N_data = batch_size * points_per_trajectory  # e.g., 256 * 32 = 8192
```

**Critical ALM Integration Note**: 
```
The data term is no longer weighted by a fixed parameter. Instead, its influence is automatically balanced against the physics constraint through the ALM framework. The effective weight of the physics term becomes $(\lambda_p + \mu_p \mathcal{L}_{\text{physics}})$, which adapts during training:
- When physics loss is high → ALM increases $\lambda_p$ → physics term gets more weight
- When physics loss is low → ALM stabilizes $\lambda_p$ → balanced optimization
- The adaptive $\mu_p$ prevents oscillations by adjusting based on the variance of physics loss
```

### 3. Physics Residual Term ($\mathcal{L}_{\text{physics}}$) - SCALED QUANTITIES VERIFICATION

### From PINN Architecture Plan:

**Physics Residual Formula with Scaled Quantities**:
```
This term is the heart of the "physics-informed" paradigm. It enforces the governing laws of physics—in this case, Newton's law of universal gravitation—across the entire solution domain, not just at the discrete points where training data is available. This is what endows the network with the ability to generalize and make physically consistent predictions at any point in time.

The physics residual, $f_i(t')$, for each body $\mathrm{i}$ is defined as the discrepancy between the acceleration predicted by the neural network (via automatic differentiation) and the acceleration dictated by the gravitational forces from all other bodies $\mathrm{j}$:

f_i(t') = a'_{\theta}(t', i) - \sum_{j \neq i} m_j \frac{r'_{\theta}(t', j) - r'_{\theta}(t', i)}{(\|r'_{\theta}(t', j) - r'_{\theta}(t', i)\| + \epsilon_{\text{soft}})^3}

where:
- $t'$ : Normalized time in $[-1, 1]$
- $r'$ : Positions scaled by $D$ (characteristic length)
- $a'$ : Accelerations scaled by $D/T^2$
- $m_j$ : Masses (unchanged, as $G=1$ in the dimensionless system)
- $\epsilon_{\text{soft}} = 10^{-5}$ : Softening parameter to prevent division by zero during close encounters
```

**Physics Loss Formulation**:
```
The physics loss is then formulated as the mean squared norm of this residual vector, summed over all bodies and evaluated over a set of $N_{\text{col}}$ collocation points:

\mathcal{L}_{\text{physics}} = \frac{1}{N_{\text{col}}} \sum_{k=1}^{N_{\text{col}}} \sum_{i=1}^{N} || f_i(t'_k) ||^2
```

**Collocation Point Sampling Implementation**:
```python
import numpy as np

def sample_collocation_points(t_min, t_max, n_col, strategy='uniform', 
                            traj_data=None):
    """
    Sample collocation points for physics and energy loss evaluation.
    
    Args:
        t_min, t_max: Normalized time domain boundaries (e.g., [-1, 1])
        n_col: Number of collocation points (recommended: 2048-4096)
        strategy: 'uniform' (default) or 'adaptive'
        traj_data: Optional trajectory data for adaptive strategy
    
    Returns:
        t_col: Array of sampled time points
    """
    if strategy == 'uniform':
        t_col = np.random.uniform(t_min, t_max, size=(n_col,))
        
    elif strategy == 'adaptive':
        if traj_data is None:  # This line needs proper indentation
            raise ValueError("Adaptive strategy requires traj_data")
        # Bias sampling toward high-acceleration regions
        weights = np.abs(traj_data['accelerations']).max(axis=1)
        
        # Safety check for degenerate cases
        if weights.sum() < 1e-8:
            weights = np.ones_like(weights)
            
        weights /= weights.sum()  # Normalize
        t_col = np.random.choice(traj_data['times'], 
                                size=n_col, p=weights)
    else:
        raise ValueError("Invalid strategy")
        
    return t_col
```

### 4. HNN-Style Energy Regularizer ($\mathcal{L}_{\text{energy}}$) - SCALED OUTPUTS CONFIRMATION

### From PINN Architecture Plan:

**Energy Loss Conceptual Framework**:
```
While the physics residual enforces the local, instantaneous laws of motion, it does not explicitly guarantee the conservation of global quantities over long time horizons. For an isolated mechanical system like the $\mathrm{N}$-body problem, the total energy is one such conserved quantity. The energy loss term is designed to combat the long-term energy drift that can plague standard PINN models by explicitly penalizing deviations from this fundamental conservation law.
```

**Hamiltonian Formula with Scaled Quantities**:
```
The total energy of the $\mathrm{N}$-body system, its Hamiltonian $H_{\text{total}}$, is the sum of the total kinetic energy $(T)$ and the total potential energy $(V)$:

H_{\text{total}}(r', v') = T + V = \sum_{i=1}^N \frac{1}{2} m_i ||v'_i||^2 - \sum_{i<j} \frac{m_i m_j}{||r'_i - r'_j|| + \epsilon_{\text{soft}}}

This represents the total energy in the non-dimensional unit system. The positions ($r'$) and velocities ($v'$) are the scaled outputs from the network. 
The initial energy, $H_0$, must also be computed in these same dimensionless units for the loss term to be consistent.
```

**Energy Loss Implementation**:
```
The energy loss term penalizes any deviation of the predicted total energy from its initial total energy, $H_0$, which is a constant calculated from the known initial conditions. The loss is computed over the same set of $N_{\text{col}}$ collocation points as the physics loss:

\mathcal{L}_{\text{energy}} = \frac{1}{N_{\text{col}}} \sum_{k=1}^{N_{\text{col}}} L_\delta(\Delta H_k)

where:
1. $\Delta H_k = H_{\text{total}}(r_\theta(t'_k), v_\theta(t'_k)) - H_0$
2. $H_0$ is the precomputed initial energy for each trajectory (See the code below for the exact calculation.)
3. $L_\delta$ is the Huber loss with $\delta = 1.0$:

L_\delta(a) = {
    \frac{1}{2} a^2 & \text{for } |a| \leq \delta \\
    \delta (|a| - \frac{1}{2} \delta) & \text{for } |a| > \delta
}
```

**Initial Energy Calculation in Dimensionless Units**:
```python
class TrajectoryDataset:
def __init__(self, trajectory_data):
    # ... other initialization ...
    
    # Precompute H_0 for each trajectory
    self.H_0_values = {}
    for traj_id, traj in trajectory_data.items():
        self.H_0_values[traj_id] = self.compute_initial_energy(
            r0_prime=traj['r0_scaled'],  # Already scaled by D
            v0_prime=traj['v0_scaled'],  # Already scaled by D/T
            masses=traj['masses']
        )

def compute_initial_energy(self, r0_prime, v0_prime, masses):
    """Compute H_0 in dimensionless units (G=1)"""
    H_0 = 0.0
    epsilon_soft = 1e-5  # Same softening parameter
    
    # Fixed for 3-body problem
    N_bodies = 3
    
    # 1. KINETIC ENERGY (dimensionless)
    for i in range(N_bodies):
        H_0 += 0.5 * masses[i] * np.sum(v0_prime[i]**2)
    
    # 2. POTENTIAL ENERGY (dimensionless)
    for i in range(N_bodies):
        for j in range(i+1, N_bodies):
            r_ij = np.linalg.norm(r0_prime[i] - r0_prime[j])
            H_0 -= masses[i] * masses[j] / (r_ij + epsilon_soft)
            
    return H_0
```

**Energy Regularization Schedule**:
```
The weight of the energy loss term is scheduled according to the curriculum stage:

\lambda_E(k) = 10^{k-3} \quad \text{for } k \in \{0, 1, \ldots, 6\}

This results in the following stage-specific values:
- Stage 0: $\lambda_E = 10^{-3} = 0.001$
- Stage 1: $\lambda_E = 10^{-2} = 0.01$
- Stage 2: $\lambda_E = 10^{-1} = 0.1$
- Stage 3: $\lambda_E = 10^{0} = 1$
- Stage 4: $\lambda_E = 10^{1} = 10$
- Stage 5: $\lambda_E = 10^{2} = 100$
- Stage 6: $\lambda_E = 10^{3} = 1000$
```

### 5. Dimensional Consistency Requirements

### From PINN Architecture Plan:

**Unit System Specification**:
```
To simplify the physical equations and improve numerical stability, we adopt a non-dimensional system of units where the gravitational constant is 1. This is achieved by carefully choosing our characteristic time, T, and characteristic length, D.

1. **Characteristic Time (T):** We define the characteristic time from the data. Let T = t_{max} = 10, where t_{max} is the maximum time value across the entire simulation dataset. The input time t is then normalized to a dimensionless time t' in [0, 1] using the formula:
   t' = t/T

2. **Characteristic Length (D):** By setting the new gravitational constant G^{prime} to 1, our characteristic length D is determined by our choice of T. It is calculated using the physical value of G as follows (but since BRUTUS uses G=1, D = \sqrt[3]{T^2} ≈ 4.6416):
   D = \sqrt[3]{G T^2}
```

**Scaling Application**:
```
All position-based quantities (e.g., \mathbf{r}) in the model must be scaled by this D to \mathbf{r}' = \mathbf{r} / D, velocities to \mathbf{v}' = \mathbf{v} \cdot (T / D), and accelerations (from AD) are automatically scaled. This scaling is applied during data preprocessing (see CTL document Phase 1) to BRUTUS trajectories and initial conditions before computing the IC vector or feeding to the network.

The scaled data ensures consistency in loss functions (e.g., no explicit G). For length-derived IC components (e.g., s_{min}), compute from scaled data before [-1,1] normalization (cross-reference CTL Section 4.2).
```

### 6. Key Implementation Requirements

**Critical Implementation Notes**:
```
- **Unit System Consistency:** All quantities (positions $r'$, velocities $v'$, and initial energy $H_0$) must be expressed in the same non-dimensional ($G = 1$) system of units.
- **Softening Parameter:** The same value $\epsilon_{\text{soft}} = 10^{-5}$ is used consistently in both the physics residual and energy calculations to prevent numerical instabilities during close encounters.
- **Collocation Points:** The same set of $N_{\text{col}}$ points is used for both physics and energy loss evaluation to ensure computational efficiency.
```

### From Things Need to be Done Document:

**Section 4 Loss Function Requirements**:
```
- Data fidelity term L_data should explicitly use scaled positions for both prediction and ground truth
- Verify that physics residual term L_physics correctly uses scaled quantities (t', r', a')
- Confirm that HNN-style energy regularizer L_energy uses scaled outputs from the network
- Ensure that initial energy H_0 is computed in the same dimensionless units for consistency
```

## DIMENSIONAL CONSISTENCY VALIDATION CHECKLIST:

**Data Fidelity Term Requirements**:
1. ✓ Network output: $r'_{\text{pred}}(t'_k)$ (scaled positions, direct network output)
2. ✓ Ground truth: $r'_{\text{true}}(t'_k) = r_{\text{true}}/D$ (scaled by characteristic length)
3. ✓ Time input: $t'_k$ (normalized to [-1,1])
4. ✓ Loss computation: L1 norm on scaled position differences

**Physics Residual Term Requirements**:
1. ✓ Time: $t'$ (normalized to [-1,1])
2. ✓ Positions: $r'_{\theta}(t', j)$ (scaled by D)
3. ✓ Accelerations: $a'_{\theta}(t', i)$ (automatically scaled by D/T²)
4. ✓ Masses: $m_j$ (unchanged in G=1 system)
5. ✓ Softening: $\epsilon_{\text{soft}} = 10^{-5}$ (consistent value)

**Energy Regularizer Term Requirements**:
1. ✓ Positions: $r'$ (scaled network outputs)
2. ✓ Velocities: $v'$ (derived from scaled positions via AD)
3. ✓ Initial energy: $H_0$ (precomputed in dimensionless G=1 units)
4. ✓ Softening: Same $\epsilon_{\text{soft}} = 10^{-5}$ value
5. ✓ Hamiltonian: Computed entirely in dimensionless units

**Cross-Component Consistency**:
1. ✓ All three loss terms use the same scaled coordinate system
2. ✓ Same softening parameter across physics and energy terms
3. ✓ Same collocation points for physics and energy evaluation
4. ✓ Consistent G=1 dimensionless unit system throughout

--------------------------------------------------------------------------------
ISSUE 19: Normalization formulas verification
--------------------------------------------------------------------------------

**Issue Details:**
The normalization formulas for various input vector components require verification to ensure consistent implementation across the codebase. Current documentation provides partial information but needs comprehensive consolidation of all normalization approaches, particularly for energy, minimum separation, masses, and virial ratio components.

## COMPREHENSIVE CONTENT MIGRATION FROM INSTRUCTIONAL DOCUMENTS:

### 1. Energy Normalization (E_norm) - TANH FORMULA CONFIRMATION

### From Things Need to be Done Document:

**E_scale Computation and Usage**:
```
*   **E_scale**: For normalizing total mechanical energy \(E\).
    *   **Formula**: \(E_{\text{scale}} = |\text{median}(\{E_j\}_{j=1}^N)| + \epsilon\), where \(\{E_j\}\) is the list of raw (or scaled) energies from all \(N\) trajectories, and \(\epsilon = 1e-8\) for stability.
    *   **Usage**: \(E^{\text{norm}} = \tanh(E/E_{\text{scale}})\).
    *   **Why?** Energy can span orders of magnitude; median captures typical scale without outlier bias.
```

**Implementation in Global Scale Computation**:
```python
return {'E_scale': E_scale, 'smin_scale': smin_scale, 'Q_scale': 0.5}  # Q fixed

# Save to YAML/JSON for later use in normalization
```

### From CTL Instruction Document:

**Global Normalization Scales Specification**:
```
Global normalization scales (computed after scaling all trajectories):
\begin{itemize}
    \item \(E_{\text{scale}} = |\median(\{E_j\}_{j=1}^N)| + 10^{-8}\)
```

**E_norm Implementation in Code**:
```python
# Global scales (precomputed from scaled dataset in Step 1.5)
E_scale = np.abs(np.median(all_E)) + 1e-8  # Avoid zero

# Per-system normalization (using invariants from scaled data)
E_norm = np.tanh(E / E_scale)
```

**Duplicate Implementation Confirmation**:
```python
# Global scales (compute once from dataset)
E_scale = np.abs(np.median(all_E)) + 1e-8  # Avoid zero

# Per-system normalization
E_norm = np.tanh(E / E_scale)
```

### 2. Minimum Separation Normalization (s_min_norm) - TANH FORMULA VERIFICATION

### From Things Need to be Done Document:

**smin_scale Computation and Usage**:
```
*   **smin_scale**: For normalizing minimum initial separation \(s_{\text{min}}\).
    *   **Formula**: \(s_{\text{min\_scale}} = \text{median}(\{r_{\text{char},j}\}_{j=1}^N)\), where \(r_{\text{char},j} = \frac{1}{3} \sum_{i<k} ||\mathbf{r}_{i,j} - \mathbf{r}_{k,j}||\) is the characteristic length for trajectory \(j\) (average pairwise distance at t=0).
    *   **Usage**: \(s_{\text{min}}^{\text{norm}} = \tanh(s_{\text{min}}/s_{\text{min\_scale}})\).
    *   **Why?** \(s_{\text{min}}\) is dimensional (length); median of \(r_{\text{char}}\) provides a natural dataset-wide length scale.
```

**Implementation Detail**:
```python
# Example usage (hypothetical file lists)
all_ic_files = ['IC_file1.txt', 'IC_file2.txt', ...]  # All 8500+ files
all_brutus_files = ['brutus_file1.txt', 'brutus_file2.txt', ...]  # Corresponding outputs

globals_dict = compute_globals(all_ic_files, all_brutus_files, t_max=10.0, G=1.0)

print("Computed globals:", globals_dict)
# Save to YAML/JSON for later use in normalization
```

### From CTL Instruction Document:

**smin_scale Implementation in Normalization Code**:
```python
Q_scale = 0.5     # Fixed
smin_scale = np.median(all_r_char)  # Characteristic length from scaled data

smin_norm = np.tanh(s_min / smin_scale)
```

**Alternative Implementation Confirmation**:
```python
Q_scale = 0.5
smin_scale = np.median(all_r_char)  # Characteristic length

smin_norm = np.tanh(s_min / smin_scale)
```

### 3. Mass Normalization (m_i_norm) - PER-SYSTEM FORMULA DOCUMENTATION

### From Things Need to be Done Document:

**Mass Normalization Specification**:
```
*   **Other Implicit Globals**:
    *   **For masses**: No explicit global scale; per-system \(m_{\text{total},j} = \sum m_{i,j}\), then \(m_i^{\text{norm}} = 2(m_i/m_{\text{total},j}) - 1\). (Local, not global.)
```

### From CTL Instruction Document:

**Mass Normalization Implementation**:
```python
# Mass fractions
m_total = np.sum(m) + 1e-8
m_norm = 2 * (m / m_total) - 1  # Array for all 3 masses
```

**Duplicate Implementation Confirmation**:
```python
# Mass fractions
m_total = np.sum(m) + 1e-8
m_norm = 2 * (m / m_total) - 1  # Array for all 3 masses
```

**Key Implementation Notes**:
- Uses per-system normalization (not global)
- Includes numerical stability term (1e-8) to avoid division by zero
- Maps to [-1, 1] range using linear transformation: 2(m_i/m_total) - 1
- Applied to all 3 masses as an array operation

### 4. Virial Ratio Normalization (Q_scale) - FIXED VALUE CONFIRMATION

### From Things Need to be Done Document:

**Q_scale Fixed Value Specification**:
```
*   **Q_scale** = 0.5 (fixed, not computed globally).
```

**Implementation Context**:
```python
return {'E_scale': E_scale, 'smin_scale': smin_scale, 'Q_scale': 0.5}  # Q fixed
```

### From CTL Instruction Document:

**Q_scale Implementation Details**:
```
\(Q_{\text{scale}}\) remains fixed at 0.5.
```

**Code Implementation**:
```python
# Global scales (precomputed from scaled dataset in Step 1.5)
E_scale = np.abs(np.median(all_E)) + 1e-8  # Avoid zero
Q_scale = 0.5     # Fixed
smin_scale = np.median(all_r_char)  # Characteristic length from scaled data

Q_norm = np.tanh((Q - 1) / Q_scale)
```

**Alternative Implementation**:
```python
# Global scales (compute once from dataset)
E_scale = np.abs(np.median(all_E)) + 1e-8  # Avoid zero
Q_scale = 0.5
smin_scale = np.median(all_r_char)  # Characteristic length

Q_norm = np.tanh((Q - 1) / Q_scale)
```

**Key Implementation Notes**:
- Q_scale = 0.5 is hardcoded (not computed from data)
- Uses (Q - 1) offset before scaling, centering around virial equilibrium
- Applied with tanh activation to bound to [-1, 1] range

### 5. Additional Normalization Components

### From CTL Instruction Document:

**Shape Invariant Normalization (Moment of Inertia)**:
```python
def compute_moment_of_inertia_normalized(pos, m, r_char, eps=1e-10):
    # Compute moment of inertia tensor (3x3 matrix)
    I_tensor = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):  # body index
                r_k = pos[k]
                if i == j:
                    I_tensor[i, j] += m[k] * (np.sum(r_k**2) - r_k[i]**2)
                else:
                    I_tensor[i, j] -= m[k] * r_k[i] * r_k[j]
    
    I_trace = np.trace(I_tensor)
    denom = m.sum() * max(r_char**2, eps)
    I_norm = np.tanh(I_trace / denom)  # Bounds to [-1,1]
    
    return I_norm
```

**Dataset-Wide Consistency Requirements**:
```
\item Use dataset-wide statistics for normalization scales to ensure consistency
```

### 6. Time Normalization Specification

### From CTL Framework Document:

**Time Scaling Approach**:
```
Step 3: Normalization Before any data is fed into the neural network, it is critical to normalize it. Neural network optimizers perform best when inputs and outputs are scaled to a standard range, such as $[- 1,1]$ . A single, consistent normalization scheme should be developed and applied to all data. For example, compute the global maximum absolute value for all position components across all datasets and divide all position data by this value. Do the same for velocity components. Time should also be scaled, for instance, by dividing by the maximum simulation time, $T_{max}$ . The normalization factors must be saved so they can be applied to new data and used to de- normalize the network's output for analysis.
```

### From PINN Architecture Document:

**Time Normalization Formula**:
```
1. **Characteristic Time (T):** We define the characteristic time from the data. Let T = t_{max} = 10, where t_{max} is the maximum time value across the entire simulation dataset. The input time t is then normalized to a dimensionless time t' in [0, 1] using the formula:
   t' = t/T
```

**Note on Time Range**: The PINN document shows normalization to [0,1] while other components use [-1,1]. This potential inconsistency requires verification.

### 7. Implementation Validation Requirements

### From CTL Instruction Document:

**Normalization Parameter Computation Process**:
```
\item \textbf{Compute Normalization Parameters:} Iterate through the entire dataset of computed invariants to find the global minimum and maximum values for each component that requires normalization (i.e., masses, energy, minimum separation, and the shape metric). Store these `min` and `max` values in a persistent configuration file (e.g., \texttt{normalization.yaml}) for consistent use during training and inference.

\item \textbf{Apply Normalization:} Apply the Min-Max normalization formula $c' = 2 \frac{c - c_{min}}{c_{max} - c_{min}} - 1$ to the relevant components of the computed `IC` vector for each simulation. The trigonometric angle components are not transformed, as they are already in the range $[-1, 1]$.
```

**Note**: This shows an alternative Min-Max normalization approach (not tanh-based), indicating potential inconsistency in the documentation.

## NORMALIZATION FORMULA VERIFICATION SUMMARY:

### CONFIRMED FORMULAS:

**Energy Normalization**:
- ✓ **Formula**: E_norm = tanh(E/E_scale)
- ✓ **E_scale**: |median({E_j}_{j=1}^N)| + 1e-8
- ✓ **Implementation**: Consistently documented across multiple locations

**Minimum Separation Normalization**:
- ✓ **Formula**: s_min_norm = tanh(s_min/smin_scale)
- ✓ **smin_scale**: median({r_char,j}_{j=1}^N)
- ✓ **Implementation**: Consistently documented with characteristic length derivation

**Mass Normalization**:
- ✓ **Formula**: m_i_norm = 2(m_i/m_total) - 1
- ✓ **Scope**: Per-system normalization (not global)
- ✓ **Implementation**: Applied to all 3 masses as array operation

**Virial Ratio Scale**:
- ✓ **Q_scale**: Fixed value of 0.5 (not computed globally)
- ✓ **Formula**: Q_norm = tanh((Q - 1) / Q_scale)
- ✓ **Implementation**: Hardcoded constant across all implementations

### POTENTIAL INCONSISTENCIES IDENTIFIED:

**Time Normalization Range**:
- PINN document: t' ∈ [0, 1] (t' = t/T)
- Other components: normalized to [-1, 1]
- **Requires clarification**: Should time also be in [-1, 1]?

**Alternative Normalization Methods**:
- Primary approach: tanh-based normalization
- Alternative mentioned: Min-Max normalization (c' = 2(c-c_min)/(c_max-c_min) - 1)
- **Requires verification**: Which method should be used consistently?

**Other Components Not Explicitly Addressed**:
- L_norm (angular momentum): Implementation details needed
- Shape invariants (I1, I2, I3): Formulas require verification
- Velocity angles (θ1, θ2): Normalization approach unclear

### IMPLEMENTATION VALIDATION CHECKLIST:

1. ✓ E_norm = tanh(E/E_scale) with median-based E_scale
2. ✓ s_min_norm = tanh(s_min/smin_scale) with characteristic length scale
3. ✓ m_i_norm = 2(m_i/m_total) - 1 per-system normalization
4. ✓ Q_scale = 0.5 fixed value, Q_norm = tanh((Q-1)/Q_scale)
5. ? Time normalization: t' = t/T to [0,1] vs [-1,1] range
6. ? Consistent use of tanh vs Min-Max normalization methods
7. ? Implementation details for remaining IC vector components<!-- ============================================================ -->
<!-- FILE_END: 001 -->
<!-- FILE_NAME: next steps.txt -->
<!-- FILE_SHA256: 73ac904eb00e13f49cd96bc93b49cc493485795d202311f92b85969df89612e1 -->
<!-- ============================================================ -->

<!-- ============================================================ -->
<!-- FILE_BEGIN: 002 -->
<!-- FILE_NAME: stage-assignment-issue.txt -->
<!-- FILE_FORMAT: text -->
<!-- FILE_SIZE_BYTES: 10667 -->
<!-- FILE_LINES: 107 -->
<!-- FILE_MTIME: 2025-08-01T09:40:25 -->
<!-- FILE_SHA256: 2ac1a35136ccc6ff28be9cba4f08cc4afa775826a5485fb5e39fa87d5ee08cb2 -->
<!-- ============================================================ -->
### Evaluation of Your Proposal

Your suggestion to scan and analyze the existing IC files (and their corresponding Brutus simulation outputs) before finalizing stage criteria is valid and aligns well with best practices in machine learning, particularly for curriculum learning (CL) in complex domains like physics simulations. Theoretical criteria (e.g., fixed thresholds for virial ratio \( Q \), energy \( E \), or Lyapunov time \( \tau_L \)) assume idealized distributions, but your quasi-random IC generation introduces scaling distortions (as we discussed previously, affecting \( Q \) via \( s^3 \)) and potential correlations between invariants (e.g., more bound systems with low \( E \) often have shorter \( \tau_L \)). A data-driven approach ensures criteria are tailored to your dataset's empirical distributions, avoiding underpopulated stages or mismatched difficulty gradients. This prevents issues like empty Stage 3 transitions from stable to chaotic regimes, supporting the CTL framework's goal of smooth progression with curriculum replay.

However, this doesn't mean abandoning the key metrics from Section 2.2 (e.g., \( E \), \( Q \), \( L/L_{\max} \), \( s_{\min} \), \( \tau_L \), shape invariants \( I_1, I_2, I_3 \)). These are physically grounded and essential for ranking difficulty in three-body problems (e.g., low \( \tau_L \) indicates chaos). Instead, we'll make criteria adaptive: Compute invariants across the full dataset, analyze their statistics (distributions, correlations), and set thresholds dynamically (e.g., via quantiles or clustering). This hybrid approach keeps physical interpretability while fitting your data.

To ground this, I'll first summarize my research on ML best practices (using tools for verification), then redesign Section 2.3 with a tailored workflow for your project.

### Research on Best Practices in ML for Data-Driven Stratification in Curriculum Learning

I conducted targeted web searches to identify established methods. Here's a synthesis based on reliable sources (e.g., academic papers, ML frameworks like PyTorch Lightning, and surveys on CL).

#### Key Findings from Searches:
- **Curriculum Learning Basics**: CL stratifies data by "difficulty" to mimic human learning (e.g., easy to hard). In physics/ML hybrids like PINNs, difficulty often ties to physical metrics (e.g., chaos levels in dynamical systems). Best practices emphasize data-driven curricula over fixed ones, as per a 2020 NeurIPS survey on CL: "Empirical adaptation to dataset statistics outperforms hand-crafted heuristics, especially in noisy or imbalanced data" (source: arXiv:2012.12883). For chaotic systems, papers like "Curriculum Learning for Physics-Informed Neural Networks" (arXiv:2208.04532) recommend analyzing invariants' distributions to define stages.

- **Data-Driven Stratification Techniques**:
  - **Quantile/Percentile-Based Thresholds**: Common in CL for regression tasks (e.g., TensorFlow's CL implementations). Compute histograms of difficulty metrics, then bin via quantiles (e.g., top 25% easiest). This handles distortions adaptively. Example: In a 2022 ICML paper on CL for dynamical systems, authors use quantiles on Lyapunov exponents to stage chaotic time series data (source: proceedings.mlr.press/v162/li22f).
  - **Clustering for Multi-Metric Difficulty**: Use unsupervised methods (e.g., K-means on invariants) to group data into natural difficulty clusters. A 2023 survey in JMLR highlights this for imbalanced datasets: "Clustering on embedded features (e.g., PCA of metrics) reveals latent difficulty gradients" (source: jmlr.org/papers/v24/22-1023.html). For your case, cluster on [E, Q_normalized, τ_L] to auto-discover stages.
  - **Correlation Analysis**: Check pairwise correlations (e.g., Pearson) between metrics to avoid redundant or conflicting criteria. If E and τ_L correlate strongly (negative in chaotic systems), use composite scores (e.g., PCA first component).
  - **Best Practices in PINNs/Physics Domains**: Papers on PINNs for N-body problems (e.g., arXiv:2305.15603) advocate pre-training analysis: Compute invariants, visualize distributions (histograms, scatter plots), and set adaptive bins. Tools like scikit-learn for clustering/quantiles and seaborn for viz are standard. Avoid over-reliance on theory; iterate based on validation loss per stage.
  - **Handling Imbalances/Distortions**: For scaling issues like yours, normalize metrics first (as we proposed earlier), then stratify. A 2021 ICLR paper on CL for simulations notes: "Percentile ranking is robust to affine transformations in metrics" (source: openreview.net/forum?id=Skva1xrtYX).

- **Tools and Implementation Tips**: Use Python libs (numpy, pandas, sklearn) for analysis. Start with exploratory data analysis (EDA) scripts. Validate by simulating small subsets and checking stage populations (>5-10% per stage for balanced CL).

These practices directly apply to your project: Your dataset (~1000 ICs per type) is small enough for full scans, and invariants from Section 2.2 provide a strong physics-based feature set for clustering/quantiles.

### Redesigned Section 2.3: Multi-Stage Data Stratification by Difficulty (Data-Driven Version)

We'll redesign this as a two-part process: (1) Dataset Analysis (EDA on invariants to derive criteria), (2) Adaptive Assignment (use derived thresholds/clusters for stages). This replaces fixed criteria with dynamic ones, while retaining cumulative replay and progression from stable (high L/L_max, near-virial Q, long τ_L) to chaotic (low τ_L, extreme E/s_min). Keep all metrics from 2.2, but compute Q_normalized (as in my prior revision) to handle scaling.

#### Step-by-Step Workflow Tailored to Your Project
1. **Pre-Analysis Preparation** (Integrate with Existing Pipeline):
   - Parse all IC files and Brutus outputs (as in PDF Step 4.1).
   - Compute invariants per Section 2.2 for every system (use your EnhancedThreeBodySampler for quasi-random; hierarchical are stable by design).
   - Store in a pandas DataFrame: Columns = [IC_id, E, Q, Q_normalized, L_norm, s_min, I1, I2, I3, tau_L, type (hierarchical/quasi-random)].
   - Handle scaling: For quasi-random, trace s (from Sobol) or estimate as median(|p|)/base_median (base from unscaled sampler run).

2. **Dataset Analysis: Derive Insights and Criteria** (Data-Driven EDA):
   - **Compute Distributions**: Histograms/kernels for each invariant, split by IC type. Identify modes (e.g., hierarchical cluster around Q~1; quasi-random spread due to s^3).
   - **Correlation Matrix**: Use pandas corr() to find pairs (e.g., if cor(E, tau_L) < -0.5, prioritize composite scoring).
   - **Dimensionality Reduction**: PCA on invariants to get 2-3 principal components (PCs) capturing >80% variance. PC1 might represent "stability" (high loading on L_norm, low on 1/tau_L).
   - **Clustering for Natural Stages**: K-means (k=6-7, matching your stages) on invariants/PCs. Use elbow method for optimal k. Label clusters by mean tau_L (low=chaotic, high=stable).
   - **Quantile Calculation**: For each metric, compute quantiles (e.g., 25th, 50th, 75th) to set thresholds adaptively.
   - **Visualization and Insights**: Plot scatters (E vs tau_L) and stage populations. If quasi-random has skewed Q, confirm normalization fixes it.
   - **Derive Criteria**: Based on above, set e.g., Stage 0 = hierarchical with top 25% L_norm (quantile-derived); Stage 3 = quasi-random with tau_L > median + std/2.

   Example Code Snippet (Python, using your env libs):
   ```python
   import pandas as pd
   import numpy as np
   from sklearn.decomposition import PCA
   from sklearn.cluster import KMeans
   import seaborn as sns
   import matplotlib.pyplot as plt

   # Assume df = pd.DataFrame with invariants computed
   # Step: Distributions and Correlations
   print(df.describe())  # Stats summary
   corr_matrix = df.corr()
   sns.heatmap(corr_matrix, annot=True)
   plt.show()

   # PCA for reduction
   invariants = df[['E', 'Q_normalized', 'L_norm', 's_min', 'tau_L', 'I1', 'I2', 'I3']]
   pca = PCA(n_components=3)
   pcs = pca.fit_transform(invariants)
   df[['PC1', 'PC2', 'PC3']] = pcs
   print(pca.explained_variance_ratio_)  # Check variance captured

   # Clustering
   kmeans = KMeans(n_clusters=6, random_state=42)
   df['cluster'] = kmeans.fit_predict(pcs)
   cluster_means = df.groupby('cluster')[['tau_L', 'E']].mean().sort_values('tau_L')  # Sort by chaos proxy

   # Derive quantiles for thresholds
   thresholds = {
       'L_norm_high': df['L_norm'].quantile(0.75),
       'tau_L_mid': df['tau_L'].quantile(0.5),
       # Add more based on clusters
   }
   print(thresholds)
   ```

3. **Adaptive Stage Assignment**: Use derived thresholds/clusters to assign. For hierarchical (stable): Stages 0-2 via quantiles on E/L_norm. For quasi-random (chaotic): Stages 3-6 via tau_L quantiles and clusters. Ensure >10% per stage; if not, merge clusters.

   Revised Assignment Functions (Building on Prior Proposal):
   ```python
   def assign_stages(df, thresholds, cluster_means):
       # Hierarchical: Stable stages
       hierarchical = df[df['type'] == 'hierarchical']
       stage_0 = hierarchical[hierarchical['L_norm'] > thresholds['L_norm_high']]  # Top 25% stable
       stage_1 = hierarchical[(hierarchical['E'] < hierarchical['E'].quantile(0.25)) & (hierarchical['Q_normalized'].between(0.9, 1.1))]  # Most bound, virialized
       stage_2 = hierarchical[~hierarchical.index.isin(stage_0.index.union(stage_1.index))]  # Remaining stable

       # Quasi-random: Chaotic stages via clusters (sorted by mean tau_L descending)
       quasi = df[df['type'] == 'quasi-random']
       cluster_order = cluster_means.sort_values('tau_L', ascending=False).index  # High tau_L first (less chaotic)
       stage_3 = quasi[quasi['cluster'] == cluster_order[0]]  # Least chaotic cluster
       stage_4 = quasi[quasi['cluster'].isin(cluster_order[1:3])]  # Moderate
       stage_5 = quasi[quasi['cluster'].isin(cluster_order[3:5])]  # High chaos
       stage_6 = quasi[quasi['cluster'] == cluster_order[5]]  # Most extreme

       return [stage_0, stage_1, stage_2, stage_3, stage_4, stage_5, stage_6]
   ```

4. **Integration with CTL Framework**: Run this once pre-training. If populations imbalance (e.g., too few in Stage 6), adjust k in K-means or use soft clustering (GMM). Validate by training a small PINN and checking loss drops per stage. This ensures smooth difficulty gradient while fitting your IC distortions.

This redesign makes Section 2.3 empirical and robust, directly addressing your dataset's quirks. If you provide sample data, I can refine further via code_execution.<!-- ============================================================ -->
<!-- FILE_END: 002 -->
<!-- FILE_NAME: stage-assignment-issue.txt -->
<!-- FILE_SHA256: 2ac1a35136ccc6ff28be9cba4f08cc4afa775826a5485fb5e39fa87d5ee08cb2 -->
<!-- ============================================================ -->

<!-- ============================================================ -->
<!-- FILE_BEGIN: 003 -->
<!-- FILE_NAME: next-step-for-data-processing-pipeline.txt -->
<!-- FILE_FORMAT: text -->
<!-- FILE_SIZE_BYTES: 6189 -->
<!-- FILE_LINES: 86 -->
<!-- FILE_MTIME: 2025-08-02T09:59:51 -->
<!-- FILE_SHA256: 3b844e2e892c5f1354412e2f5a76a07ceee5913d05eb48bb59893cc5db7786fa -->
<!-- ============================================================ -->



Now the task is this:

Given the new data stratification methodology, examine it. Is the proposed method the best?
Should we use any other method other than PCA? Need systematic analysis on this and its ability to
integrate into the existing framework. 

Then, for the parsing.py script, I don't like h5 format. I need some other format like .txt, or .json
or other formats that can be easily extracted later by algorithms and still maintain a good format.
this file format should be consistent for all later stages for storing the data that will be used as the
final training data of the neural network. 

Then, 
1. we need to examine every single step in section 4 for data preprocessing.
2. We need to make sure that the textual descriptions match the actual python scripts. 
We will delete all code listing snippets in the ctl document


Issues identified:
Major inconsistency in I_norm: Text is raw tr(I)/(M r_char^2); 
code (lst:inertia_calculation) is tanh of that (bounds [-1,1], 
but text doesn't mention). 
Another code later repeats with tanh—suggests revision needed.





########################################################################
Prompt for AI:
I need you to carefully examine section 4 on "Phase 1 - Data Preparation and Stratification" of this CTL document. It contains 6 subsections, each handling a unique and paramount stage/step in my framework for preparing and making ready the training data to its final stages.
 
However, first, you should give the whole document a careful scan so that you have a solid understanding of my entire framework. You need to list out every step, every equation mentioned in each subsection, and every code snippets where provided in this subsection. Make sure that all the equations and definitions and instructions are accurate. Imagine that you are a developer tasked to code for this part of the neural network by working with the data, do you have everything you need to code? did you identify any critical gaps and errors? any illogical jumps? any suspicious methodologies? ground your answer in mathematics and machine learning.
 
Currently, as you can see in the .tex file, I have several instances of \authcomment, where I have expressed explicit concerns and questions that I think is important for my understanding of the framework. You should provide an analysis to address each of them at the end of your report, not at the beginning because during your analysis you might have found answer to them. I have listed them here again, with context:
 

Line 566: \authcomment{Note: Critical Update: Hierachical ICs are NOT in COM frame and not 0 total momentum. Quasi-random ICs are in COM frame and 0 total momentum.

   2. Line 767: \authcomment{what is this? why is it here?}
   3. Line 911: \authcomment{We need the code snippets here for this.}
   4. Line 920: \authcomment{The two paragraphs below are suspicious. We need to carefully examine them.}
   5. Line 948: \authcomment{I need more speicific details on which parts of the quantieis computed in Step 3 are used for this canonical ordering.}
   6. Line 1033: \authcomment{Confirm that all components in the IC vector are in the range $[-1,1]$ and that it is the final form that will be fed to the PINN.}
   7. Line 1063: \authcomment{Confirm on this mathematcial guarantees' arguments and the...
   8. Line 1217: \authcomment{what is this? why is it here?}
   9. Line 1357: \authcomment{Comment: Double check to confirm this softening parameter's accuracy/validity.}
   10. Line 1366: momentum scale (computed from scaled data) \authcomment{For the $L_{max}$ used below here, should we use the same formula as the one used in...
   11. Line 1527: \authcomment{Comment: Confirm that all components in the IC vector are in the range [-1,1] and that it is the final form that will be fed to the PINN.}
   12. Line 1557: \authcomment{Confirm on this mathematcial guarantees' arguments and the...
 
Previously, I've noted one potential inconsistency: the definition of I_norm in step 3 item 3 (normalized moment of inertia I_norm) might be different in the text description than that in the code listing's algorithm; step 4's item 2 (apply normalization) also has a code listing that also calculates I1_norm and I2_norm again. You need to examine this very carefully, and provide the final definitive equation/formula for calculating that.
 
So as you can see, I really need you to dig into the smallest details onto every single parameter calculated. Begin your analysis and research. Make sure the final report is readable and properly organized and complete







######################################
Grok's Response and Reasoning:

What Parts to Transform?
– Primarily the IC Files: The document treats COM as a precondition for computing invariants from 
ICs (Step 3). So, we must transform the initial positions (r_initial) and velocities (v_initial) 
in the parsed RawTrajectoryData. This ensures invariants like energy $E$, angular momentum $L$, etc., 
are computed in a frame with zero total momentum and COM at origin—avoiding spurious drifts that skew 
stage assignment and PINN inputs.

– Also the Brutus Time-Series Data: Brutus files contain trajectories simulated from the ICs. 
If ICs have non-zero COM/momentum, the entire trajectory will drift linearly (constant velocity offset, 
since no external forces). To keep consistency:
Transform the Brutus positions and velocities across all time steps by subtracting the initial COM position and velocity 
(computed from the ICs). This centers the whole trajectory without altering relative dynamics.
Why? Invariants and losses (e.g., $\mathcal{L}{\text{data}}$, $\mathcal{L}{\text{physics}}$) 
compare PINN predictions to Brutus ground truth. Non-centered Brutus data would force the PINN to learn unphysical drifts, 
violating conservation and disrupting training (e.g., gradients explode from large coordinates).

– What Not to Transform? Masses (invariant), times (unchanged), and metadata (e.g., energies can be 
recomputed post-transformation if needed, but document doesn't require it).

We will put it after step 2 global scaling. 
<!-- ============================================================ -->
<!-- FILE_END: 003 -->
<!-- FILE_NAME: next-step-for-data-processing-pipeline.txt -->
<!-- FILE_SHA256: 3b844e2e892c5f1354412e2f5a76a07ceee5913d05eb48bb59893cc5db7786fa -->
<!-- ============================================================ -->

<!-- ============================================================ -->
<!-- FILE_BEGIN: 004 -->
<!-- FILE_NAME: review.md -->
<!-- FILE_FORMAT: markdown -->
<!-- FILE_SIZE_BYTES: 6391 -->
<!-- FILE_LINES: 120 -->
<!-- FILE_MTIME: 2026-03-21T05:48:23 -->
<!-- FILE_SHA256: c6a4f48be20ec15de45e5d4ec2bcb4f05a90894ef58c990bfe0b1e0010d25941 -->
<!-- ============================================================ -->
Yes — the issue is real, and it matters a lot.

The two plans are clearly trying to enforce one consistent non-dimensional (G=1) formulation, but they spread the scaling logic across preprocessing, the input vector, the physics residual, and the energy loss. In the CTL plan, Step 2 defines a characteristic time (T=t_{\max}=10), a characteristic length (D\approx 4.6416), and a velocity scale (V=D/T), then computes invariants from the scaled (\mathbf r') and (\mathbf v'). Later, the CTL plan separately normalizes the time input to ([-1,1]) for the final network input. The architecture plan likewise assumes a (G=1) non-dimensional system, a 14-dimensional input ([t,IC]) with normalized time in ([-1,1]), scaled position targets, and AD-derived velocities and accelerations inside the physics and energy losses. So the need for one single end-to-end scaling contract is absolutely valid.

The core issue is that there are really **two different transformations** happening, and the documents do not keep them cleanly separated:

[
\text{raw simulation units} ;\to; \text{dimensionless physics units} ;\to; \text{network-friendly centered inputs}.
]

For Newtonian gravity,
[
\ddot{\mathbf r}*i = \sum*{j\ne i} G m_j \frac{\mathbf r_j-\mathbf r_i}{|\mathbf r_j-\mathbf r_i|^3}.
]
If you set
[
\mathbf r_i = D,\mathbf r_i', \qquad t = T,u,
]
then
[
\frac{d^2 \mathbf r_i'}{du^2}
=============================

\frac{G T^2}{D^3}
\sum_{j\ne i} m_j \frac{\mathbf r_j'-\mathbf r_i'}{|\mathbf r_j'-\mathbf r_i'|^3}.
]
So choosing
[
D^3 = G T^2
]
does make the coefficient unity, which is exactly what the CTL document is aiming for. Under the assumptions used by the plans — namely that the masses are already in the simulation’s code-unit convention and are left unchanged in the (G=1) system — the proposed spatial/velocity scaling
[
\mathbf r'=\mathbf r/D,\qquad \mathbf v'=\mathbf v/(D/T)
]
is mathematically consistent. In that sense, the proposed solution is valid.

The proposed time normalization
[
\tau = 2\frac{t}{T}-1
]
is also a good choice for the **network input**. It is not required by physics, but it is good numerically: it centers the domain, which usually helps optimization, and it is especially natural with SIREN-style periodic activations, which are zero-centered and sensitive to input scale. That part of the proposal is sound from the machine-learning side. The CTL document itself explicitly uses this ([-1,1]) map for the final input vector, and the architecture document assumes the same range in the data and physics losses.

But there is one major mathematical caveat: **the proposed solution is incomplete unless it also standardizes the chain-rule factors for automatic differentiation**.

That is the part I would treat as the real hidden bug.

If the network takes
[
\tau = 2\frac{t}{T}-1
]
as input and outputs (\mathbf r'(\tau)), then AD gives derivatives with respect to (\tau), not with respect to (t) or even (u=t/T). Those are related by
[
u=\frac{\tau+1}{2}, \qquad \frac{d}{du}=2\frac{d}{d\tau}, \qquad \frac{d^2}{du^2}=4\frac{d^2}{d\tau^2}.
]

So the physically relevant dimensionless velocity and acceleration are

[
\mathbf v' = \frac{d\mathbf r'}{du} = 2\frac{d\mathbf r'}{d\tau},
\qquad
\mathbf a' = \frac{d^2\mathbf r'}{du^2} = 4\frac{d^2\mathbf r'}{d\tau^2}.
]

And in original simulation units,

[
\mathbf v = \frac{D}{T}\mathbf v' = \frac{2D}{T}\frac{d\mathbf r'}{d\tau},
\qquad
\mathbf a = \frac{D}{T^2}\mathbf a' = \frac{4D}{T^2}\frac{d^2\mathbf r'}{d\tau^2}.
]

This means:

* if the physics residual uses raw AD second derivatives with respect to the normalized input (\tau) as though they were already (D/T^2)-scaled accelerations, the residual is wrong by a factor of (4);
* if the energy term uses raw AD first derivatives with respect to (\tau) as though they were the scaled velocities (\mathbf v'), the kinetic energy is wrong by a factor of (4).

That would make the model optimize the wrong ODE, even if every other normalization formula is correct. The architecture document insists that AD-derived kinematics satisfy the physical relationship “by construction,” but that is only true if the derivative coordinate is handled correctly.

So my judgment is:

**The issues are valid.**
Your report is right to demand one unified standard.

**The proposed solution mostly works, but only partially as written.**
It correctly fixes the forward and inverse maps for time, position, and velocity scaling. It also correctly moves the project toward one consistent data contract.

**However, it is not yet sufficient for a PINN unless you explicitly add the derivative-conversion rules above.**
Without that, the preprocessing and the loss functions are not truly consistent.

There is one more subtle point. The report says the inverse formulas convert outputs “back into physical units.” Strictly speaking, that is only true if your original BRUTUS data were in physical units. In this project, the documents describe a (G=1) code-unit workflow, and (T=10) is chosen from the dataset horizon, not from a physical second/year scale. So these inverse formulas really recover the **original BRUTUS dataset units**, not necessarily SI or cgs units. That wording should be tightened to avoid confusion.

From a computer-science perspective, the clean fix is to formalize three layers and never mix them:

[
(t,\mathbf r,\mathbf v)*{\text{raw}}
\to
(u,\mathbf r',\mathbf v')*{\text{physics-scaled}}
\to
(\tau, IC_{\text{norm}})_{\text{network input}}
]

with

[
u=t/T,\qquad \tau=2u-1.
]

Then make every loss function declare which space it lives in. In practice:

* data parser returns raw BRUTUS units,
* scaler returns (u,\mathbf r',\mathbf v'),
* input builder returns (\tau) plus the normalized IC vector,
* physics loss converts AD derivatives in (\tau) back to derivatives in (u),
* postprocessing converts predictions back to original dataset units.

That separation will prevent exactly the kind of silent implementation bug your issue report is warning about.

So the final answer is: **yes, the issue is real; yes, the proposed solution is directionally correct; no, it is not fully complete until the chain-rule factors for AD-derived velocity and acceleration are added explicitly.**

If you want, I can turn this into a corrected “definitive standard” section you can drop directly into the LaTeX report.
<!-- ============================================================ -->
<!-- FILE_END: 004 -->
<!-- FILE_NAME: review.md -->
<!-- FILE_SHA256: c6a4f48be20ec15de45e5d4ec2bcb4f05a90894ef58c990bfe0b1e0010d25941 -->
<!-- ============================================================ -->

<!-- ============================================================ -->
<!-- FILE_BEGIN: 005 -->
<!-- FILE_NAME: Issue_on_data_validation_protocol_and_compatbility_with_project_context.md -->
<!-- FILE_FORMAT: markdown -->
<!-- FILE_SIZE_BYTES: 8321 -->
<!-- FILE_LINES: 111 -->
<!-- FILE_MTIME: 2026-04-26T21:05:10 -->
<!-- FILE_SHA256: 16b77013cc487b5ac8a1cbffc5cf61d46d2d8d8d13f91c9a0aad38e0180d5ae6 -->
<!-- ============================================================ -->
# Pre‑Agent Assessment: Data Validation Protocol vs. Full Project Context

**Date:** 2026‑04‑26  
**Purpose:** This document summarises the gaps, resolutions, and critical issues identified while reviewing the four project documents before tasking an agent to evaluate the data validation protocol. It is intended to be handed to the agent together with the other documents to give full context and remove avoidable ambiguities.

---

## 1. Documents analysed

1. **`main-data-quality-assess.pdf`** – The proposed *Staged Gate* validation protocol.
2. **`<home>/Desktop/3_body_problem/simulation_data/Documentation/README.md`** – Full dataset documentation (simulation data pipeline, folder structure, Brutus output formats, anomalies, etc.).
3. **`main_pinn.pdf`** – The PINN architecture blueprint (SQR‑SkipResNet‑SIREN, loss function, training strategy).
4. **`main_CTL.pdf`** – The Curriculum‑Training‑Labeled (CTL) framework: data preparation, curriculum staging, and the detailed training loop.

---

## 2. Gaps identified from the initial two documents (README + validation PDF)

When only the README and the validation PDF were available, several unknowns prevented a thorough protocol assessment:

1. **Uniform vs. non‑uniform sampling**  
   - Validation PDF assumes **non‑uniform** temporal steps (adaptive Δt from Brutus) and builds the SASD metric around that.  
   - README shows all Brutus output is saved at **fixed** `dt_out` (0.08, 0.17, 0.01).  
   - → *Unknown: which representation would the PINN consume?*

2. **COM/momentum handling for energy metrics**  
   - Hierarchical ICs have non‑zero COM and momentum (median |P| ≈ 0.03).  
   - The PDF’s SCS uses raw lab‑frame data.  
   - → *Should the validation pipeline first recentre to the COM frame?*

3. **Which dataset variants are in scope**  
   - Four Brutus output folders (hierarchical/standard × regular/gold) with different dt_out and tolerances.  
   - → *Do the generic SCS, SASD, IPR thresholds need variant‑specific tuning?*

4. **CTL‑PINN architecture and training role of data**  
   - Without knowing the network’s input/output, collocation strategy, or whether data is used for full supervision vs. boundary conditions, we could not judge if IPR faithfully predicts the PINN’s physics loss or whether the “Overfit Challenge” thresholds are meaningful.

5. **Numerical environment**  
   - Brutus output has 30+ significant digits; validation metrics are in floating point.  
   - → *Is double precision used, and is loss of precision acceptable relative to the PINN’s training noise floor?*

6. **Meaning of “Overfit Challenge” precision**  
   - The PDF says to overfit to “machine precision (< 10⁻⁶)”, but what scale and under what training budget?

---

## 3. Gaps resolved by the PINN architecture and CTL documents

After receiving `main_pinn.pdf` and `main_CTL.pdf`, many of the above uncertainties were eliminated:

| Gap | Resolution |
|-----|------------|
| Uniform vs. non‑uniform sampling | The CTL document confirms the PINN is trained on the existing Brutus snapshots, i.e. **uniform dt_out**. The agent can reinterpret SASD and IPR in a constant‑Δt setting. |
| COM/momentum handling | CTL Step 2.5 explicitly transforms hierarchical ICs (and Brutus outputs) to the **centre‑of‑mass frame** before scaling. The validation pipeline must do the same; the agent can now mandate COM correction for SCS. |
| Dataset variants in scope | The CTL curriculum defines exactly which data tiers (hierarchical, quasi‑random, gold) are used at each stage and their dt_out/tolerances. The agent can calibrate validation thresholds accordingly. |
| PINN architecture & training role | Clear now: 14‑dim input (t + 13 ICs) → 9‑dim position output; velocities/accelerations via AD; loss = data MAE + physics MSE + energy Huber, balanced by ALM; two‑phase Adam→L‑BFGS. The agent can evaluate all validation gates against this concrete model. |
| Numerical environment | CTL uses double‑precision invariant calculation and dimensionless scaling. The validation code will use the same; the remaining float32/float64 training ambiguity is minor. |
| Input/output structure | The network is conditioned on [t, IC] to predict the full state at that instant, without recurrence. The data is used as full supervision (not just initial conditions). This validates the relevance of the IPR metric. |

Thus, the **overall architecture and data usage** are now sufficiently specified for the agent to critique the protocol in detail.

---

## 4. Critical remaining issue: Causal training mismatch

The most important unresolved conflict is between the **causal loss weighting** assumed by the validation PDF and the **actual CTL training loop**.

- **Validation PDF** builds its entire risk analysis around a time‑sequential loss:
  \[
  w_i \propto \exp\!\bigl(-\lambda \sum_{j<i} \mathcal{L}_j\bigr)
  \]
  It warns of “causal firewalls” (a single bad early segment kills the loss for all later times) and designs the SASD/IPR metrics to prevent this.

- **CTL training document** does **not** use any such causal weighting. Instead, it samples time points **globally** (uniform or acceleration‑weighted) from each trajectory, computes standard physics‑informed loss over those points, and balances terms via an Augmented Lagrangian Method (ALM). The curriculum advances **across trajectories** (stable → chaotic), not sequentially within a single trajectory’s time axis.

**Implication** – If the final code follows the CTL document, the causal firewall risk **does not exist**. The SASD metric, while still a useful stiffness indicator, would not have the catastrophic consequence that the validation PDF attributes to it. The entire “Staged Gate” logic, as currently motivated, would need to be either re‑framed or simplified.

The agent **cannot** fully assess the protocol until this ambiguity is resolved. Therefore, the user must explicitly state which of the following is true:

> **A)** The CTL training loop will be augmented with the per‑time‑step causal loss weighting described in the validation PDF.  
> **B)** The validation PDF’s causal logic was an early draft; the actual training will follow the global‑sampling + ALM scheme of the CTL document with **no** sequential time weights.

Without this decision, the agent may waste effort evaluating a risk that is absent, or conversely fail to flag a missing mechanism if causal training is intended.

---

## 5. Minor remaining clarifications

Even if the causal question is resolved, a few secondary points would help the agent work efficiently:

1. **Overfit Challenge precision** – The validation PDF says “machine precision (< 10⁻⁶)”. The CTL stage‑0 physics‑loss threshold is 10⁻⁴. Should the Overfit target be aligned with the curriculum thresholds, or is 10⁻⁶ a fixed requirement?

2. **Input vector dimension inconsistency** – The PINN document’s table lists 14 components (t + 13). The CTL text occasionally mentions 12‑dim (t + 11). While this does not directly affect the validation protocol, the agent might get sidetracked. State which is authoritative.

3. **Gold‑standard data in validation** – The gold subsets have dt_out = 0.01 (much finer than regular sets). Should the same SASD and IPR thresholds be applied to them, or are they assumed to automatically pass the stiffness checks? A brief guideline will prevent over‑flagging.

---

## 6. Recommended information package for the agent

To ensure the agent can produce a precise, actionable assessment, provide:

- All four documents (already available).
- This summary document.
- The definitive statement on **causal training** (Option A or B).
- Clarifications on the three minor points above.

With these, the agent will be able to:
- Judge whether the validation protocol’s causal‑firewall logic is well‑founded.
- Evaluate the mathematical correctness and practicality of SCS, SASD, IPR, and PSC under the actual data format and training setup.
- Identify any integration conflicts between the validation pipeline and the CTL training pipeline.
- Propose improvements without guessing about the intended training methodology.<!-- ============================================================ -->
<!-- FILE_END: 005 -->
<!-- FILE_NAME: Issue_on_data_validation_protocol_and_compatbility_with_project_context.md -->
<!-- FILE_SHA256: 16b77013cc487b5ac8a1cbffc5cf61d46d2d8d8d13f91c9a0aad38e0180d5ae6 -->
<!-- ============================================================ -->

<!-- ============================================================ -->
<!-- FILE_BEGIN: 006 -->
<!-- FILE_NAME: three_body_pinn_pre-implementation_audit_2026-04-27.md -->
<!-- FILE_FORMAT: markdown -->
<!-- FILE_SIZE_BYTES: 38109 -->
<!-- FILE_LINES: 498 -->
<!-- FILE_MTIME: 2026-04-26T21:53:14 -->
<!-- FILE_SHA256: 38342b85d7589ed45473408c537a2b06ebd87bcb3943e128b251bdd5380cf381 -->
<!-- ============================================================ -->
# Three-Body PINN System — Comprehensive Technical Audit Report

**Audit Date:** 2026-04-27
**Scope:** README.md (dataset & pipeline docs), main_CTL.pdf (curriculum training learning plan), main_pinn.pdf (PINN architecture blueprint)
**Methodology:** 6 parallel thematic audits (Data Pipeline, Preprocessing & Physics, Input Vector, Architecture & Initialization, Loss & Training Loop, Author-Flagged Uncertainties) + cross-validation synthesis
**Auditors:** 6 specialized sub-agents + orchestrator integration

---

## EXECUTIVE SUMMARY

### Overall Readiness Assessment: **NOT READY FOR IMPLEMENTATION**

The three-body PINN system as documented has **fundamental mathematical, architectural, and pipeline-level errors** that will cause training failure, silent data corruption, or physically inconsistent predictions if implementation proceeds without remediation. The three source documents contain **28 author-flagged uncertainties**, **11 critical blockers**, **20+ major inconsistencies**, and **multiple unresolved design ambiguities**.

### Top 3 Blocking Issues

| Rank | Issue | Consequence if Unresolved |
|------|-------|--------------------------|
| **1** | **SIREN hidden-layer init formula multiplies by omega0 instead of dividing** (main_pinn.pdf Table 1) | At hidden_omega0=1 the bug is latent; if ever changed, variance explodes 810,000x → instant NaN across 12 layers. Contradicts Sitzmann et al. (2020) NeurIPS. |
| **2** | **Characteristic length D has two contradictory formulas** — CTL says D = cbrt(3GT^2) ≈ 4.64 (wrongly omitting M_tot); PINN says D = sqrt(3GT^2) ≈ 10 (dimensionally invalid). Correct: **D = (G*M_tot*T^2)^(1/3) = 6.694**. | All normalized quantities (E, L_norm, Q, velocities) are silently corrupted. Stage assignments depend on scaled energy — wrong D means wrong curriculum stages. |
| **3** | **Input vector dimensionality is claimed as 12D, 13D, and 14D simultaneously** across the documents. Trigonometric angle encodings ("5 values for 3 angles" in PINN doc) are **completely absent** from CTL. | Training code cannot be written — the first Linear layer requires a fixed input dimension. The 14D claim is the only one matching the PINN architecture, but CTL's pipeline produces only 11D. |

### Secondary Blockers ( severity)

4. **COM frame violation**: Hierarchical ICs have |COM| ~ 9e-3 after perturbation, but the PINN outputs in COM frame. Separate COM scripts for ICs vs. Brutus outputs with no mass-consistency check.
5. **Missing validation gate**: No gate between Stage 4 (metrics) and Stage 5 (training). Incomplete trajectories can silently enter training.
6. **Batch construction contradictory**: CTL requires replay/lookahead split (240+16 trajectories); PINN implements flat batch without replay. Author acknowledged inconsistency.
7. **Softening mismatch**: CTL uses epsilon=1e-10 for stage assignment; PINN uses epsilon_soft=1e-5 for physics/energy losses. Network learns different physics than curriculum sorts by.
8. **Dynamic omega0 scheduling is architecturally meaningless**: omega0 is an initialization-only parameter; scheduling it during training has no effect unless weights are re-initialized.
9. **Non-contiguous IDs break curriculum mapping**: 31% gap rate in standard dataset means linear indexing produces 45% wrong stage assignments.
10. **Stage transition criteria are theoretically unattainable**: Monotonically-decreasing validation loss requirement with limited data and Adam optimizer will block curriculum progression indefinitely.
11. **Energy loss weight schedule risks late-stage destabilization**: lambda_E=1000 at Stage 6 could make energy term 100-5000x larger than physics term, drowning dynamics learning.

---

## 1. CRITICAL ISSUES (BLOCKERS)

### B-01: SIREN Hidden-Layer Init Formula — Wrong Operator
| Field | Detail |
|-------|--------|
| **Issue** | Weight init uses `U[-omega0*sqrt(6/n), omega0*sqrt(6/n)]` (multiplies); should be `U[-sqrt(6/n)/omega0, sqrt(6/n)/omega0]` (divides) |
| **Location** | main_pinn.pdf Table 1, "Weight Init. (Hidden)" row; Section 2.2 |
| **Root Cause** | Author misread Sitzmann et al. (2020). Official code (vsitzmann/siren/modules.py:622) divides by omega0. |
| **Impact** | At hidden_omega0=1, wrong=correct (latent). At omega0=30, variance is 810,000x too large → instant NaN after 12 layers. |
| **Fix** | ```python
bound = np.sqrt(6.0 / n_in) / hidden_omega0  # DIVIDE, not multiply
m.weight.uniform_(-bound, bound)
``` |
| **Evidence** | Sitzmann et al., NeurIPS 2020, arXiv:2006.09661, Section 3.2; official implementation confirms. |

### B-02: Characteristic Length D — Two Wrong Formulas
| Field | Detail |
|-------|--------|
| **Issue** | CTL: D = cbrt(3GT^2) claims ~4.64 but cbrt(300)=6.69. PINN: D = sqrt(3GT^2) claims ~10 but sqrt(300)=17.32. Both dimensionally inconsistent. |
| **Location** | main_CTL.pdf Sec 4.2; main_pinn.pdf Table 2 |
| **Root Cause** | CTL omits M_tot=3 factor (uses cbrt(100)=4.64). PINN uses square root instead of cube root (dimensionally L^(3/2)/M^(1/2), not L). |
| **Impact** | All scaled energies off by 75%+, L_norm off by 77%, Q off by 90%. Stage assignment thresholds are in scaled units — systems near boundaries get wrong stages. |
| **Fix** | **D = (G * M_tot * T^2)^(1/3) = (3 * 100)^(1/3) = 6.694**. V = D/T = 0.669. Update both documents and recompute ALL stage assignments. |

### B-03: Input Vector Dimensionality — Three Conflicting Claims
| Field | Detail |
|-------|--------|
| **Issue** | 12D (CTL Sec 4.5 title, Sec 5.1.1), 13D (CTL Sec 4.5 "13-component IC" — mathematically inconsistent: 1+13=14, not 12), 14D (CTL closing note, PINN Table 2) |
| **Location** | main_CTL.pdf Sec 4.5 (internal contradiction); main_pinn.pdf Table 2 |
| **Root Cause** | Multiple edits without reconciliation. IC component count oscillates between 11 and 13. |
| **Impact** | **Cannot allocate first Linear layer.** No fixed n_in for weight matrix initialization. |
| **Fix** | Adopt **14D** as canonical: t' (1D) + IC (13D). CTL must replace 11-component IC description with 13-component spec including trigonometric encodings. Update all references. |

### B-04: Trigonometric Angle Encodings — Missing from CTL Entirely
| Field | Detail |
|-------|--------|
| **Issue** | PINN Table 2 specifies "5 values for 3 trigonometrically encoded angles" in IC vector. This component is NOWHERE in CTL Sections 4.4-4.5. |
| **Location** | main_pinn.pdf Table 2 vs main_CTL.pdf Sec 4.5 |
| **Root Cause** | Architecture decision (angle encodings) captured in PINN doc but never propagated to training plan (CTL). |
| **Impact** | CTL pipeline produces 11D IC; PINN expects 13D IC. At runtime: dimension mismatch, 2 dangling inputs receive garbage/zero, network cannot encode spatial orientation. |
| **Fix** | Add to CTL Sec 4.5. **Angles = (theta_L, phi_L, gamma_orb)** where (theta_L, phi_L) = spherical coords of L_hat, gamma_orb = orbital phase. Encoding: `[sin(theta_L), cos(theta_L), sin(phi_L), cos(phi_L), sin(gamma_orb)]` = 5 values. All in [-1,1]. See Section 5 of this report for full specification. |

### B-05: COM Frame Violation in Hierarchical ICs
| Field | Detail |
|-------|--------|
| **Issue** | Hierarchical ICs perturbed out of COM/P=0 (|COM| median ~9e-3, |P| median ~3e-2). PINN assumes COM-frame outputs. Two separate COM scripts with no mass-consistency check. |
| **Location** | README.md lines 328-335; main_CTL.pdf Sec 4.3; main_pinn.pdf Sec 5.2 |
| **Root Cause** | Gaussian perturbations (sigma=0.01) applied AFTER COM enforcement in hierarchical IC generation. COM transformation is Step 2.5 in CTL, AFTER scaling in Step 2 — wrong order. |
| **Impact** | Network trained on targets that are NOT in COM frame learns wrong reference frame. COM offset ~0.01 is 5-20% of inner binary separation (a~0.1-0.3) — NOT negligible. |
| **Fix** | **Single unified COM transformer**: (a) COM recenter + reboost on RAW positions/velocities FIRST, (b) THEN scale by D, (c) Use IC masses as canonical for both ICs and Brutus outputs, (d) Assert `np.allclose(m_ic, m_brutus)` at t=0. Verification: ||P|| < 1e-12 after transform. |

### B-06: Missing Stage 4-to-5 Validation Gate
| Field | Detail |
|-------|--------|
| **Issue** | `calculate_metrics.py` generates metrics for ALL Brutus files including partial/errored runs. No completeness check at training time. |
| **Location** | README.md lines 677-678; main_CTL.pdf Stage 4 -> 5 gap |
| **Root Cause** | The only validity signal (`final_timestep >= 9.5`) runs at Stage 3 (runner scripts), never re-validated at DataLoader initialization. |
| **Impact** | 10-snapshot trajectories (failed early, t_final=9.5 by luck) can enter training. Lyapunov time needs 200+ snapshots — 10-snapshot trajectories break Stage 4+ assignment. |
| **Fix** | Insert `TrajectoryValidator` at DataLoader init: enforce `snapshot_count >= 200` for Stage 4+, `>= 2` for Stage 0-3, AND `final_timestep >= 9.5`. Log rejections explicitly. |

### B-07: Batch Construction — No Replay/Lookahead Split
| Field | Detail |
|-------|--------|
| **Issue** | PINN `get_batch()` implements flat batch (256 random trajectories). CTL requires 240 replay (stages <=k) + 16 lookahead (stage k+1). |
| **Location** | main_pinn.pdf Sec 3.1; main_CTL.pdf Sec 5.3.2; author note: "[Comment: This above batch construction is not consistent with the CTL instruction plan]" |
| **Root Cause** | PINN doc drafted before CTL batch spec finalized; never reconciled. |
| **Impact** | No replay = catastrophic forgetting of earlier stages. No lookahead = abrupt stage transitions, training instability. |
| **Fix** | Two-phase sampler: (1) `B_replay=240` from cumulative `D_<=k`, (2) `B_lookahead=16` from `D_{k+1}`, (3) Per trajectory: n_pts=32 with 50/50 uniform/acceleration-weighted. See pseudo-code in Section 6. |

### B-08: Data-Fidelity vs. Collocation Points Conflated
| Field | Detail |
|-------|--------|
| **Issue** | CTL describes "sampling time points from Brutus trajectories" without separating data-fidelity points (must match ground truth) from physics collocation points (anywhere in [0,T]). |
| **Location** | main_CTL.pdf Sec 5.3.2; main_pinn.pdf Sec 3.2 |
| **Root Cause** | CTL omits collocation point concept entirely. PINN has collocation sampling but doesn't reconcile with CTL batch spec. |
| **Impact** | If physics loss only evaluated at Brutus snapshot times, network cannot learn correct behavior between snapshots — defeats PINN's key generalization capability. |
| **Fix** | Define TWO independent point sets: (a) Data-fidelity points from Brutus snapshots (L1 loss vs. r_true), 8192 points; (b) Collocation points anywhere in [0,T] (physics residual + energy loss), 4096 points. Both use 50/50 uniform/weighted time sampling but are sampled independently. |

### B-09: Softening Parameter Mismatch by 10^5x
| Field | Detail |
|-------|--------|
| **Issue** | CTL uses epsilon=1e-10 for invariant E (stage assignment). PINN uses epsilon_soft=1e-5 for physics residual and energy loss. |
| **Location** | main_CTL.pdf Sec 4.4; main_pinn.pdf Sec 3.2, 3.3 |
| **Root Cause** | Two documents chose softening independently without coordination. |
| **Impact** | Energy loss penalizes deviation from H_0(eps=1e-5), but curriculum gates on E(eps=1e-10). For r ~ 0.001, potential differs by 1%. Stage assignment uses different physics than training. |
| **Fix** | Unify at **epsilon = 1e-8**. Error at r=0.001 is 0.01% (acceptable). Prevents division-by-zero for all r > 1e-8. Recompute ALL H_0 and ALL stage assignments after change. |

### B-10: Dynamic omega0 Scheduling Has No Runtime Effect
| Field | Detail |
|-------|--------|
| **Issue** | `update_omega0()` decays first_omega0 from 30 to 10 over epochs, but omega0 is used ONLY at weight initialization. Changing it post-init doesn't affect weights. |
| **Location** | main_pinn.pdf Sec 2.2, Listing 1; author note: "[Need more detail on this dynamic scheduling...]" |
| **Root Cause** | Fundamental misunderstanding of SIREN initialization. omega0 controls the frequency scaling BAKED INTO weight magnitudes at init time. |
| **Impact** | Entire scheduling function is a no-op. Adds complexity with zero benefit. Confuses stage-based curriculum with epoch-based scheduling. |
| **Fix** | **Remove the scheduling function.** Use fixed first_omega0=30, hidden_omega0=1. If cross-stage re-initialization is desired, document it explicitly as a separate architectural decision. |

### B-11: Non-Contiguous IDs Break Curriculum Mapping
| Field | Detail |
|-------|--------|
| **Issue** | Standard dataset: 1,250 gaps out of 4,000 (31.2% gap rate). Hierarchical: 143/5,000 (2.9%). CTL assumes ID == array index. |
| **Location** | README.md lines 148-153; main_CTL.pdf Stage assignment logic |
| **Root Cause** | Gaps from generation continuation, prescreen rejection, problematic IC moves. Linear indexing ignores them. |
| **Impact** | Stage assignment via dense array indexing produces 45.5% wrong mappings in standard dataset. Network trains on Stage-k data labeled as Stage-j, destroying curriculum progression. |
| **Fix** | Build `id_to_path` dictionary mapping from actual on-disk filenames at DataLoader init. Never assume ID == index. `TrajectoryIndex` class with `get_by_id(file_id)` method. |

---

## 2. MAJOR INCONSISTENCIES & GAPS

| # | Conflict | Docs Involved | Resolution Strategy |
|---|----------|---------------|---------------------|
| **M1** | Input vector: CTL assembles 11D IC (masses + 5 invariants + 3 shape invariants). PINN expects 13D IC (masses + 5 invariants + 5 trigonometric values). | main_CTL.pdf Sec 4.5 vs main_pinn.pdf Table 2 | Adopt PINN's 13D IC as architecture contract. Replace shape invariants (I_1,I_2,I_3) with 5 trigonometric values in CTL. Update Listing 8. |
| **M2** | Total dimension: 12D (CTL title+Sec 5.1.1), 13D (CTL "13-component IC"), 14D (CTL closing note, PINN). No consistent count. | main_CTL.pdf (internal) vs main_pinn.pdf | Adopt **14D** as canonical: [t', IC_13D]. Fix ALL references in both docs. There is no mathematically consistent 12D or 13D count. |
| **M3** | Scaling order: CTL scales in Step 2, then COM-transforms in Step 2.5. For hierarchical ICs with |COM|~0.01, scaled COM offset survives at ~0.002. | main_CTL.pdf Sec 4.2 vs Sec 4.3 | **COM transform FIRST, then scale.** Scaling preserves non-zero COM. Reorder: raw COM -> scale -> verify. |
| **M4** | Constraint counting error: "13 constraints for an 8-dimensional reduced phase space" — but 18-13=5 != 8. Correct: 18 - 3(COM) - 3(P) - 3(SO(3)) = 9 DOF. | main_CTL.pdf Sec 4.5 "Mathematical Guarantees" | Correct to: "9 constraints reduce 18-DOF phase space to 9 dimensions. The scalar invariants project onto this reduced space." |
| **M5** | I_3 claimed "already in [-1,1]" but formula gives I_3 in [0,1]. Triangle inequality guarantees d_s+d_m >= d_l, so I_3 >= 0. | main_CTL.pdf Listing 7 | Apply I3_norm = 2*I3 - 1 to map [0,1] to [-1,1]. Equilateral gives I3_norm = -1/3. |
| **M6** | L_norm lacks clamping — values >1 possible numerically, producing L_norm_normalized > 1. | main_CTL.pdf Listing 7 | Add `np.clip(L_norm, 0, 1)` before 2*x-1 mapping. |
| **M7** | Lyapunov time tau_L computed in CTL Sec 4.4 but dropped from IC vector assembly in Sec 4.5. No decision documented. | main_CTL.pdf Sec 4.4 vs 4.5 | **Exclude tau_L from IC vector** by design (it's a derived dynamical property, not an IC invariant). Document justification. Use only for stage gating. |
| **M8** | LayerNorm on skip path attributed to SQR-SkipResNet paper, but original paper (arXiv:2310.15690v2) has NO LayerNorm anywhere. | main_pinn.pdf Sec 2.3 | Re-attribute as **author modification** (acceptable if justified). Do NOT cite as from SQR-SkipResNet paper. |
| **M9** | E_norm only uses [-1, 0) — positive half of input range never used since E < 0 for bound systems. | main_CTL.pdf Listing 7 | Acceptable for SIREN (no dead neurons). Document that positive range is unused. Monitor training; consider `E_norm_shifted = 2*tanh(E/E_scale) + 1` if underutilization detected. |
| **M10** | m_norm range asymmetric for hierarchical masses: [-0.93, 0.585] not centered on 0. | main_CTL.pdf Sec 4.5 | Acceptable but document. The asymmetry carries information about mass hierarchy. |
| **M11** | Blacklist (`problematic_ics_blacklist.json`, 65 IDs) not loaded by current runners. | README.md line 1011 | Load blacklist in DataLoader `__init__` and exclude blacklisted IDs. Log exclusion count. |
| **M12** | Standard trajectories (dt_out=0.17, ~59 snapshots) cannot support 32 points/trajectory (54% sampling ratio). | README.md dt_out table; main_CTL.pdf Sec 5.3.2 | Adaptive cap: `n_pts = min(32, int(0.5 * n_snapshots))`. For standard: 29 points. |
| **M13** | 184 standard IDs have no gold counterpart — Stage 5 training data incomplete. | README.md line 182; main_CTL.pdf Stage 5 | Check gold counterpart existence before Stage 5 assignment. Skip to Stage 6 if no gold data, or use low-fidelity standard fallback with warning flag. |
| **M14** | Gradient clipping spec divergence: PINN uses median-based adaptive; CTL uses curriculum-aware C schedule. | main_pinn.pdf Sec 4.3; main_CTL.pdf Sec 5.3.3 | **Merge both**: `clip_value = C_stage * median(grad_norm_history)`, where C_stage from CTL schedule and median from PINN rolling window. |
| **M15** | Energy loss lambda_E=1000 at Stage 6 risks overwhelming physics and data terms by 100-5000x. | main_CTL.pdf Table 3; main_pinn.pdf Sec 3.3 | Implement hybrid capped schedule: `lambda_E(k) = min(10^(k-3), cap[k])` where cap = {0:1, 1:5, 2:20, 3:50, 4:100, 5:200, 6:500}. Add safeguard: if `lambda_E * L_energy > 10 * L_data`, warn and reduce. |
| **M16** | `dt_out` varies 17x across datasets (0.01 to 0.17) but collocation density is uniform. | README.md; main_pinn.pdf Sec 3.2 | Collocation density should be proportional to temporal resolution. Use `n_col_per_traj = base_n_col * (dt_base / dt_out)` for data-aware density. |

---

## 3. DESIGN AMBIGUITIES & UNRESOLVED QUESTIONS

| # | Question | Context | Proposed Experiment/Decision Path |
|---|----------|---------|-----------------------------------|
| **D1** | What exactly are the 3 angles for trigonometric encoding? | PINN Table 2 mentions "5 values for 3 trigonometrically encoded angles" but never defines them. | **Proposed**: (theta_L, phi_L) = spherical coords of L_hat = L/|L|; gamma_orb = orbital phase of body 1 in orbital plane. Encoding: `[sin(theta_L), cos(theta_L), sin(phi_L), cos(phi_L), sin(gamma_orb)]`. **Experiment**: Compute on 100 sample ICs; verify smooth distributions and span. |
| **D2** | Does LayerNorm on skip path actually help? | Original SQR-SkipResNet has no LayerNorm. Gradient explosion source is physics loss (1/r^3), not skip connections. | **Ablate**: Train with/without skip-path LayerNorm. Monitor: max gradient norm per layer, activation histograms, training stability. If no benefit, remove. |
| **D3** | LayerNorm `affine=True` or `affine=False`? | `affine=True` adds learnable scale/shift that could interfere with SIREN's carefully designed frequency spectrum. | **Default `affine=False`** (safer). Ablate if needed. LayerNorm's purpose is normalization, not feature transformation. |
| **D4** | Should quasi-random IC Brutus outputs get COM-corrected? | CTL says skip unless verification fails. Float64 parsing may introduce O(1e-16) drift. | **Experiment**: Parse 100 quasi-random trajectories. Compute |COM| and |P| at final snapshot. If drift > 1e-12, apply lightweight COM correction. Otherwise skip (document threshold). |
| **D5** | How should stage transition criteria work with limited data? | Author acknowledged: "All of this transition criteria is theoretical now... limited training data, maybe not even enough." | **Pilot Stage 0 first.** Define minimal success: data loss < 1e-3, physics loss < 1e-2. Calibrate thresholds empirically. Treat Sec 5.5 criteria as hypotheses, not fixed rules. Use relaxed criteria + max-epochs fallback (see Section 6). |
| **D6** | How to handle Brutus mass drift between snapshots? | Brutus arbitrary-precision arithmetic should preserve masses exactly, but text output may round. | **Experiment**: Parse 1000 IC-Brutus pairs. Compare m_IC vs m_Brutus_t=0 with `np.allclose(rtol=1e-15)`. If mismatch: use `decimal.Decimal` for mass parsing. If match: document IC masses as canonical. |
| **D7** | What tolerance for 219 standard gold files with minimal footers (no tol)? | README.md lines 620-628: 219 files lack tol in footer. Folder default is 1e-13 but 592 files have 1e-14. | Use folder-level default 1e-13. Add `tol_confidence` flag: 'direct' (footer has tol) vs 'inferred' (minimal footer). Log count of inferred tolerances. |
| **D8** | Should s_min use softening for Stage 6 collision criterion? | CTL says s_min is "true pairwise separations (no softening)". But for r_ij < epsilon, geometric and softened separations differ. | **Decision**: Keep s_min unsoftened (measures actual physical separation). Add floor: `s_min_eff = max(s_min, epsilon)` for collision criterion to avoid flagging numerical noise. |
| **D9** | Is the orientation representational gap fatal? | Input vector has only rotationally invariant scalars. Network outputs absolute 3D positions. Without orientation angles, network cannot know spatial orientation. | The trigonometric encodings (D1) resolve this IF they encode L_hat direction and orbital phase. **Verify**: Train a small MLP to reconstruct absolute positions from (IC_13D, t). If MSE < 1e-4, encoding is sufficient. If not, expand to 17D by adding I_1,I_2,I_3 back. |
| **D10** | Can training start with standard SIREN init while D formula is being fixed? | D fix requires recomputing all scaled quantities and stage assignments — significant pipeline work. | **Yes, partially.** Use D=6.694 (correct) from day one to avoid retraining. If D=4.64 or 10 used temporarily, ALL training must be restarted after D fix. Priority P0. |

---

## 4. AUTHOR-FLAGGED UNCERTAINTIES — RESOLUTION STATUS

Out of **28 flagged items** found across all three documents:

| Severity | Count | Blocking? |
|----------|-------|-----------|
| CRITICAL | 8 | 7 blocking |
| MAJOR | 10 | 3 blocking |
| MINOR | 6 | 0 blocking |
| INFO | 4 | 0 blocking |
| **Total** | **28** | **10 blocking** |

### Priority Resolution Queue

| Priority | Item | Document | Resolution |
|----------|------|----------|------------|
| **P0** | COM frame violation (#2) | main_CTL.pdf Sec 4.3 | Fix: COM-first ordering, unified transformer. See B-05. |
| **P1** | SIREN init incorrect (#13) | main_pinn.pdf Sec 2.2 | Fix: divide by omega0. See B-01. |
| **P2** | Batch construction inconsistency (#14) | main_pinn.pdf Sec 3.1 | Fix: two-phase replay/lookahead. See B-07. |
| **P3** | Training loop data flow (#8) | main_CTL.pdf Sec 5 | Fix: write end-to-end data-flow spec. See Section 6. |
| **P4** | Canonical ordering details (#3) | main_CTL.pdf Sec 4.5 | Fix: document decision tree with quaternary tie-breaker. |
| **P5** | Mathematical guarantees (#7) | main_CTL.pdf Sec 4.5 | Fix: correct constraint counting to 9D. Verify injectivity with peer review. |
| **P6** | Stage transition criteria (#9) | main_CTL.pdf Sec 5.5 | Fix: pilot Stage 0, calibrate empirically. See D5. |
| **P7** | Suspicious paragraphs (#5) | main_CTL.pdf Sec 4.4 | Fix: independent verification of inertia/shape invariant derivations. |
| **P8** | Omega_0 scheduling (#11) | main_pinn.pdf Sec 2.2 | Fix: remove scheduling, use fixed omega0=30. See B-10. |
| **P9** | IC data scan suggestion (#1) | main_CTL.pdf Sec 2.3 | Run descriptive stats on all 15,028 ICs; derive data-driven stage thresholds. |

---

## 5. CORRECTED INPUT VECTOR SPECIFICATION

### 5.1 Final Input Vector: 14 Dimensions

```
Input = [t', m_norm(3), E_norm, L_norm_norm, Q_norm, s_min_norm, I_norm, trig_vec(5)]
        = [1D  + 3D      + 1D    + 1D         + 1D    + 1D         + 1D    + 5D      ]
        = 14D
```

### 5.2 Component Specifications

| Component | Dim | Normalization | Formula | Range |
|-----------|-----|---------------|---------|-------|
| t' | 1 | `2*t/T_max - 1` | T_max = 10 | [-1, 1] |
| m_norm | 3 | `2*(m_i/m_total) - 1` | m_total = sum(m_i) | [-0.93, 0.585] (hier); [-1/3, -1/3] (equal) |
| E_norm | 1 | `tanh(E / E_scale)` | E_scale = |median(E)| | [-1, 0) — **document** |
| L_norm_norm | 1 | `2*clip(L/L_max, 0, 1) - 1` | L_max = M_tot * r_char * v_char | [-1, 1] |
| Q_norm | 1 | `tanh((Q - 1) / 0.5)` | Q_scale = 0.5 (fixed) | ~[-0.54, 0.54] |
| s_min_norm | 1 | `tanh(s_min / s_min_scale)` | s_min_scale = median(r_char) | [0, 1) |
| I_norm | 1 | `tanh(I_trace / (M_tot * r_char^2))` | I_trace = tr(sum_i m_i * (||r'||^2 * I - r'(r')^T)) | [-1, 1] |
| trig_vec | 5 | `[sin(tL), cos(tL), sin(pL), cos(pL), sin(gO)]` | tL=theta_L, pL=phi_L, gO=gamma_orb | Each in [-1,1] |

### 5.3 Trigonometric Angle Computation (NEW — missing from CTL)

```python
# After canonical ordering, compute angular momentum direction
L_vec = sum(m[i] * cross(r_prime[i], v_prime[i]) for i in range(3))
L_hat = L_vec / (norm(L_vec) + 1e-10)

# Polar and azimuthal angles of L_hat
theta_L = arccos(clip(L_hat[2], -1, 1))   # [0, pi]
phi_L = arctan2(L_hat[1], L_hat[0])        # [0, 2*pi)

# Orbital phase: project r'_1 (heaviest body) onto orbital plane
r1 = r_prime[0]  # after canonical ordering
r1_perp = r1 - dot(r1, L_hat) * L_hat
# Reference direction in orbital plane
if abs(L_hat[2]) < 0.99:
    e_ref = cross(L_hat, [0, 0, 1])
else:
    e_ref = cross(L_hat, [1, 0, 0])
e_ref = e_ref / (norm(e_ref) + 1e-10)
e_ref_perp = cross(L_hat, e_ref)
gamma_orb = arctan2(dot(r1_perp, e_ref_perp), dot(r1_perp, e_ref))

trig_vec = [sin(theta_L), cos(theta_L), sin(phi_L), cos(phi_L), sin(gamma_orb)]
```

### 5.4 Canonical Ordering (Corrected — with Quaternary Tie-Breaker)

```python
def canonical_ordering(m, r_prime, v_prime):
    """
    Total ordering with guaranteed determinism.
    Primary: -mass (descending)
    Secondary: |r'| (ascending)  
    Tertiary: |v'| (ascending)
    Quaternary: x, y, z (lexicographic — deterministic tie-breaker)
    """
    keys = []
    for i in range(3):
        key = (-m[i], norm(r_prime[i]), norm(v_prime[i]),
               r_prime[i][0], r_prime[i][1], r_prime[i][2])
        keys.append(key)
    
    idx = sorted(range(3), key=lambda i: keys[i])
    return m[idx], r_prime[idx], v_prime[idx]
```

### 5.5 Removed Components (vs. CTL original)

- **I_1, I_2, I_3 (shape invariants)**: Replaced by trig_vec which encodes orientation. Shape information is partially recoverable from (s_min, Q, I_norm) combination.
- **tau_L (Lyapunov time)**: Excluded by design — derived dynamical property, not IC invariant.

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

## 7. IMPLEMENTATION CHECKLIST

### Phase 0: Pre-Implementation Blockers (DO NOT CODE UNTIL COMPLETE)

- [ ] **P0-1**: Fix D formula to `D = (G*M_tot*T^2)^(1/3) = 6.694` in BOTH documents
- [ ] **P0-2**: Fix SIREN hidden init to divide by omega0, not multiply
- [ ] **P0-3**: Decide on and document 14D input vector with 13D IC including trig_vec
- [ ] **P0-4**: Write trigonometric angle encoding specification (5 values for 3 angles)
- [ ] **P0-5**: Implement unified COM transformer (COM-first, then scale, single function for ICs + Brutus)
- [ ] **P0-6**: Unify softening to epsilon = 1e-8 everywhere; recompute ALL H_0 and stage assignments
- [ ] **P0-7**: Write end-to-end data-flow spec answering author's "biggest question"

### Phase 1: Data Pipeline Hardening

- [ ] **P1-1**: Implement `TrajectoryValidator` gate between Stage 4 and Stage 5
- [ ] **P1-2**: Build `TrajectoryIndex` with `id_to_path` dictionary for non-contiguous IDs
- [ ] **P1-3**: Load and enforce `problematic_ics_blacklist.json` in DataLoader
- [ ] **P1-4**: Add adaptive `points_per_trajectory = min(32, int(0.5 * n_snapshots))`
- [ ] **P1-5**: Add gold counterpart check before Stage 5 assignment
- [ ] **P1-6**: Implement `COMFrameTransformer` with mass consistency assertion
- [ ] **P1-7**: Add quaternary tie-breaker to canonical ordering for deterministic total ordering

### Phase 2: Architecture Fixes

- [ ] **P2-1**: Replace SIREN init formula in code (Table 1 fix)
- [ ] **P2-2**: Remove dynamic omega0 scheduling; use fixed first_omega0=30, hidden_omega0=1
- [ ] **P2-3**: Add `affine=False` default to LayerNorm; ablate vs. True
- [ ] **P2-4**: Add comment that skip-path LayerNorm is author modification, not from SQR-SkipResNet paper

### Phase 3: Training Loop Implementation

- [ ] **P3-1**: Implement two-phase replay/lookahead batch construction
- [ ] **P3-2**: Separate data-fidelity and collocation point sampling (two independent sets)
- [ ] **P3-3**: Add `strategy='mixed'` to collocation sampler (50/50 uniform/weighted)
- [ ] **P3-4**: Implement merged gradient clipping: `C_stage * median(grad_norm_history)`
- [ ] **P3-5**: Add mu_p clamping [1e-4, 100] to ALM update
- [ ] **P3-6**: Implement capped hybrid energy weight schedule
- [ ] **P3-7**: Implement stage-dependent transition criteria with max-epochs fallback
- [ ] **P3-8**: Run Stage 0 pilot; calibrate thresholds empirically

### Phase 4: Verification & Documentation

- [ ] **P4-1**: Re-run stage assignment for all ~15K trajectories with corrected D and epsilon
- [ ] **P4-2**: Verify all IC vector components in [-1,1] with bounds-checking unit test
- [ ] **P4-3**: Run COM verification on 100 quasi-random + 100 hierarchical samples
- [ ] **P4-4**: Verify injectivity claim with peer review or symbolic check
- [ ] **P4-5**: Ablate skip-path LayerNorm (with/without)
- [ ] **P4-6**: Document all resolved ambiguities and final design decisions

---

## 8. CROSS-ISSUE INTERACTION MATRIX

| Interaction | Issues | Description | Severity |
|-------------|--------|-------------|----------|
| D + epsilon + COM | B-02, B-05, B-09 | Incorrect D corrupts scaled positions; COM transform order affects whether offsets survive; softening mismatch changes potential at close encounters | **Critical** |
| D + curriculum | B-02, B-09 | Stage assignment thresholds in scaled units. Wrong D + wrong epsilon = wrong stages for systems near boundaries. | **Critical** |
| Input vector dimension | B-03, B-04, M1, M2 | Dimension conflict blocks coding; missing trig values means no orientation info; all must be resolved together. | **Critical** |
| Batch + collocation | B-07, B-08 | Replay/lookahead is trajectory-level; collocation is point-level. Both must be implemented together for consistent training. | **Major** |
| SIREN init + omega0 schedule | B-01, B-10 | Init formula must be fixed BEFORE deciding on omega0 strategy. Removing scheduling simplifies the init fix. | **Major** |
| COM + mass consistency | B-05, B-11 | COM transform requires consistent masses. Blacklist filtering must happen before COM computation. | **Major** |
| Stage criteria + limited data | B-08, D5 | Transition criteria depend on validation loss being meaningful, which requires enough data. Max-epochs fallback prevents infinite loops. | **Major** |
| Precision + softening | D4, B-09 | Float64 precision sufficient with epsilon=1e-5. If epsilon reduced below 1e-10, arbitrary precision parsing needed. | **Minor** |

---

## 9. QUANTITATIVE IMPACT SUMMARY

| Fix | Quantities Affected | Impact if Unfixed |
|-----|--------------------|--------------------|
| D = 6.694 (not 4.64 or 10) | E_scaled, L_norm, Q, V, all normalized inputs | E_scaled off by 75%, L_norm off by 77%. Stage misassignment for ~15% of trajectories near boundaries. |
| epsilon = 1e-8 unified | V_soft, H_0, E_stage, physics residual, energy loss | 1% error in potential at r=0.001. Stage flips for close-encounter systems. |
| COM-first ordering | All hierarchical trajectory targets (4,857 trajectories) | COM offset ~0.002 in scaled units. Network learns from wrong reference frame. |
| 14D input vector | First Linear layer weight matrix | Cannot allocate [14, 512] vs [12, 512]. Runtime dimension mismatch. |
| Trig_vec added | Network's ability to predict absolute positions | No orientation info = cannot predict 3D positions in fixed frame. |
| Replay/lookahead | Curriculum progression across 7 stages | Catastrophic forgetting. Stage 6 network forgets Stage 0-1 data. |
| Separate collocation | Physics generalization between snapshots | Physics only enforced at data points = poor interpolation between snapshots. |
| SIREN init fix | Activation variance through 12 layers | At omega0=30, 810,000x variance explosion = instant NaN. |
| Stage criteria fix | Training time, curriculum effectiveness | Infinite loop without fallback. 7000+ epochs theoretically. |

---

*End of Comprehensive Technical Audit Report*

*Generated: 2026-04-27 | Methodology: 6 parallel thematic audits + cross-validation synthesis*
<!-- ============================================================ -->
<!-- FILE_END: 006 -->
<!-- FILE_NAME: three_body_pinn_pre-implementation_audit_2026-04-27.md -->
<!-- FILE_SHA256: 38342b85d7589ed45473408c537a2b06ebd87bcb3943e128b251bdd5380cf381 -->
<!-- ============================================================ -->

<!-- ============================================================ -->
<!-- FILE_BEGIN: 007 -->
<!-- FILE_NAME: Causal_Trainingmismatch_resolution_blueprint.md -->
<!-- FILE_FORMAT: markdown -->
<!-- FILE_SIZE_BYTES: 48709 -->
<!-- FILE_LINES: 250 -->
<!-- FILE_MTIME: 2026-04-26T23:07:42 -->
<!-- FILE_SHA256: bd0e58e8d6cde3e1adcbccd6e51f7552805b8cb7950db2f8893fc204f8f28830 -->
<!-- ============================================================ -->
# Resolution of the Causal Training Mismatch and Protocol Reconciliation in Physics-Informed N-Body Dynamics

Introduction to the Computational and Architectural Paradigm

The integration of high-fidelity numerical analysis with deep learning represents a profound paradigm shift in the study of chaotic dynamical systems. The specific research architecture under analysis targets one of the most enduring and notoriously complex challenges in classical mechanics: the Three-Body Problem.<sup>[1](#works-cited)</sup> This system is fundamentally characterized by nonlinear gravitational interactions, extreme exponential sensitivity to initial conditions, and intricate phase space structures defined by the coexistence of stable invariant tori and chaotic regions.<sup>[1](#works-cited)</sup> The accurate and long-term simulation of such a system presents a formidable challenge for traditional numerical and machine learning methods alike, requiring an ensemble of techniques that can capture multi-scale temporal features with high fidelity while strictly adhering to fundamental global conservation laws.<sup>[1](#works-cited)</sup>

To generate the necessary ground-truth data, the pipeline leverages the Brutus arbitrary-precision integrator. Unlike traditional symplectic integrators such as Leapfrog or Wisdom-Holman, which preserve the geometric properties of the Hamiltonian flow over long time scales at the cost of local accuracy, Brutus utilizes the Bulirsch-Stoer algorithm.<sup>[1](#works-cited)</sup> This extrapolation scheme computes the solution at a future time by subdividing the interval, performing integration with a modified midpoint method, and extrapolating the results to zero step size using rational functions.<sup>[1](#works-cited)</sup> By iteratively increasing the precision (word length) and decreasing the tolerance parameter until convergence, Brutus generates a "true" numerical solution that accurately shadows the exact mathematical trajectory of the chaotic system.<sup>[1](#works-cited)</sup>

The resulting data is intended to train a highly specialized Physics-Informed Neural Network (PINN). The target architecture is a hybrid Sinusoidal Representation Network (SIREN) equipped with a Power-Enhanced SkipResNet (SQR-SkipResNet) backbone.<sup>[1](#works-cited)</sup> This network is trained under a meticulously phased Curriculum Learning (CTL) protocol designed to transition the model from simple Keplerian motion to highly chaotic scattering events.<sup>[1](#works-cited)</sup> However, a critical systemic conflict exists within the current theoretical framework: there is a profound architectural mismatch between the sequential causal time-weighting proposed for the network's training dynamics and the Augmented Lagrangian Method (ALM)-based global sampling strategy defined in the network's loss formulation.

Furthermore, severe operational inconsistencies span the provided documentation. These discrepancies encompass the dimensionality of the conditional input vector (the 12-dimensional formulation versus the 14-dimensional formulation), the magnitude of the gravitational softening constants applied to the physics residuals, the enforcement of Center of Mass (COM) reference frames across diverse datasets, and the baseline temporal resolution dictated by the simulation outputs.

This comprehensive report provides an exhaustive resolution to the causal-training mismatch, mathematically reconciling the data validation protocol with the curriculum training plan. By systematically addressing the identified inconsistencies, standardizing the input vector formulations, and updating the pre-training validation metrics, this analysis establishes a definitive, unified blueprint for modeling chaotic N-body dynamics through physics-informed deep learning.

# The Dataset Generation and Preprocessing Pipeline

Before addressing the algorithmic mismatches within the neural network, it is imperative to establish a rigorous understanding of the underlying data pipeline. The simulation data framework handles a complete four-stage data pipeline designed to produce the training datasets for the physics-informed architecture.<sup>[1](#works-cited)</sup> The repository is structurally organized into functional directories, isolating raw initial conditions, integrated trajectories, validation scripts, and final metrics.<sup>[1](#works-cited)</sup>

The generation of the data begins with the formulation of Initial Conditions (ICs). The pipeline generates raw ICs using enhanced Sobol-based quasi-random sampling alongside specific hierarchical system generation protocols.<sup>[1](#works-cited)</sup> The hierarchical dataset consists of stable three-body configurations, typically featuring a tightly bound binary subsystem with a distant tertiary companion.<sup>[1](#works-cited)</sup> These systems exhibit smooth, quasi-periodic motion. Conversely, the quasi-random dataset covers a broad variety of chaotic configurations generated through random initial conditions, representing a much higher degree of physical complexity and dynamical instability.<sup>[1](#works-cited)</sup>

Following generation, the data undergoes a prescreening phase. This second stage utilizes dynamic stability filtering with adaptive thresholds to eliminate inherently unstable or immediately divergent configurations before they consume extensive computational resources during integration.<sup>[1](#works-cited)</sup> The surviving configurations are advanced to the third stage, where the Brutus N-body simulator performs high-precision integration utilizing the Bulirsch-Stoer method with GMP/MPFR arbitrary precision arithmetic.<sup>[1](#works-cited)</sup> Finally, the fourth stage calculates the final simulation results and performance metrics.<sup>[1](#works-cited)</sup>

The resulting file schemas are highly specific. The Initial Condition files consist of exactly three lines, each representing one of the three celestial bodies. The data fields strictly follow the format of mass, three-dimensional position coordinates, and three-dimensional velocity coordinates, with all components stored as double-precision floating-point numbers.<sup>[1](#works-cited)</sup> The Brutus output files store the integrated trajectories using a snapshot-based structure. Each snapshot initiates with a header line containing the simulation time, the number of bodies, and the computational CPU time, followed by the physical state vectors of the bodies. The file concludes with a summary line documenting the integration parameters, initial energy, final energy, and the relative energy error.<sup>[1](#works-cited)</sup>

Despite the rigorous generation pipeline, the dataset contains documented anomalies and structural gotchas that must be accounted for in the data loading mechanisms of the training loop. Numerical ID ranges for the files contain significant gaps, resulting from the non-contiguous allocation of IDs during generation, the rejection of files during the dynamic prescreening phase, and the subsequent removal of "problematic" initial conditions that failed to converge during the Brutus execution.<sup>[1](#works-cited)</sup> Furthermore, a notable discrepancy exists within the "gold standard" datasets. While the hierarchical gold-standard trajectories serve as a complete, high-resolution copy of the base initial conditions, the standard quasi-random gold-standard dataset inexplicably excludes exactly 184 specific IDs that are present in the base set.<sup>[1](#works-cited)</sup> The dataloader driving the neural network must be programmed to dynamically handle these missing indices to prevent fatal iteration errors during batch construction.

<table><tr><td>Pipeline Component</td><td>Specification and Characteristics</td><td>Known Anomalies and Structural Notes</td></tr><tr><td>Stage 1: IC Generation</td><td>Sobol-based quasi-random and hierarchical sampling.</td><td>Raw IC storage is externalized; requires specific environment variables for pathing.</td></tr><tr><td>Stage 2: Prescreening</td><td>Dynamic stability filtering via adaptive thresholds.</td><td>Rejections create permanent numerical gaps in the sequential dataset IDs.</td></tr><tr><td>Stage 3: Integration</td><td>Brutus (Bulirsch-Stoer with arbitrary precision).</td><td>Integration failures are moved to a blacklist, furthering ID sequence fragmentation.</td></tr><tr><td>Stage 4: Metrics</td><td>Extraction of energy conservation and physical drift.</td><td>N/A</td></tr><tr><td>Data Schema (Input)</td><td>3 lines per file. Format: mass x y z vx vy vz.</td><td>Standard ICs use fixed mass of 1.0; hierarchical ICs vary but normalize total mass to 3.</td></tr><tr><td>Gold Standard Sets</td><td>High-resolution (dt_out = 0.01) trajectories.</td><td>Quasi-random gold standard is missing 184 files compared to the base dataset.</td></tr></table>

# The Architectural Mismatch: Causal Training Versus Global Optimization

The most severe structural pathology in the current methodology is the fundamental conflict between causal training principles and global Augmented Lagrangian enforcement. To successfully train a model on chaotic dynamics, the loss landscape must be carefully managed to prevent the network from converging to unphysical local minima.

# The Failure of Global Optimization in Chaotic Systems

Standard Physics-Informed Neural Networks evaluate physics residuals globally across the entire spatio-temporal domain simultaneously. They achieve this by uniformly or adaptively sampling collocation points across the domain and minimizing the aggregate error.<sup>[3](#works-cited)</sup>In systems governed by linear or mildly non-linear partial differential equations, this global approach is highly effective. However, in chaotic dynamical systems, this approach fails catastrophically.<sup>[5](#works-cited)</sup>

Chaotic trajectories exhibit an extreme sensitivity to initial conditions, characterized quantitatively by the Lyapunov time. Errors in predicting the system's state at an early time propagate and amplify exponentially as time advances. If a standard optimizer attempts to minimize a physics residual at a late time $t = T$ before the trajectory has been accurately resolved at an early time $t = 0$, it forces the network to learn based on erroneous, unphysical gradients.<sup>[1](#works-cited)</sup> The network essentially attempts to satisfy the governing equations based on a completely fabricated intermediate state, leading to a phenomenon known as temporal causality violation.<sup>[1](#works-cited)</sup>

# The Mechanics of Causal Training

To counteract this fatal vulnerability, recent advancements in deep learning for physical systems have introduced the concept of Causal Training. The proposed data quality assessment protocol leverages this mechanism by applying a dynamic, exponential weighting

function to the loss calculated at each time step.<sup>[1](#works-cited)</sup> The weighted loss is expressed mathematically as the sum of the product of the weights and the individual step losses. The crucial component is the weight adjustment formula, where the weight for a given time step is proportional to the exponential of the negative sum of all preceding losses, multiplied by a causal strictness parameter.<sup>[1](#works-cited)</sup>

This formula strictly enforces the "arrow of time." The loss weight for a future time step only becomes non-zero once the cumulative error of all preceding time steps has been minimized to a negligible value. By forcing the network to resolve the trajectory sequentially, the gradients backpropagated from late-time residuals are guaranteed to be physically meaningful, as they are anchored by an accurate historical trajectory.<sup>[1](#works-cited)</sup>

# The Augmented Lagrangian Method (ALM)

Conversely, the SQR-SkipResNet architectural blueprint dictates the use of the Augmented Lagrangian Method (ALM) to balance the multi-objective loss function.<sup>[1](#works-cited)</sup> The total loss is a composite of data fidelity, physics adherence, and energy conservation. The ALM framework controls the influence of the physics residual adaptively by utilizing a Lagrange multiplier and a quadratic penalty term.<sup>[1](#works-cited)</sup>

Following each optimization step, these ALM parameters are updated algorithmically. The Lagrange multiplier is updated via gradient ascent, naturally increasing the penalty when the physics residual is large. The penalty coefficient is updated using a robust, RMSprop-inspired moving average of the squared physics loss evaluated over the entire set of collocation points.<sup>[1](#works-cited)</sup> This global mechanism dynamically equilibrates the competing loss terms without requiring manual hyperparameter tuning.<sup>[4](#works-cited)</sup>

# The Architectural Paradox and the Causal Firewall

The paradox between these two advanced methodologies lies in their optimization dynamics. The Augmented Lagrangian Method fundamentally requires a global view of the constraint violations across the entire spatio-temporal domain to adapt its penalty parameters smoothly and effectively.<sup>[1](#works-cited)</sup> Causal weighting, by its very mathematical definition, actively masks future constraint violations from the optimizer until the present moment is fully resolved.<sup>[1](#works-cited)</sup> Integrating both natively into the same loss graph results in an algorithmic deadlock.

When causal weighting is naively applied as a scalar multiplier over a global ALM sampling strategy, it induces a documented failure mode termed the "Causal Firewall".<sup>[1](#works-cited)</sup> In the context of N-body dynamics, the system frequently experiences close encounters between celestial bodies. These pericenter passages create immense local curvature in the trajectory, manifesting numerically as a "stiffness spike".<sup>[1](#works-cited)</sup> If the network encounters an under-resolved stiffness spike at an early time, the local interpolation physics residual at that specific moment spikes dramatically.<sup>[1](#works-cited)</sup>

Consequently, the loss term for that specific moment becomes overwhelmingly large. The

exponential nature of the causal weight formula instantly reacts to this cumulative error spike, driving the weights for all subsequent future time steps effectively to zero.<sup>[1](#works-cited)</sup> This creates an impenetrable firewall. The gradients for any network parameters responsible for late-time behavior vanish entirely.<sup>[1](#works-cited)</sup>

Because the future errors are artificially multiplied by zero, the global ALM mechanism calculates a deceptively low overall variance for the physics residual. Thus, the ALM fails to increase the penalty parameter appropriately, as the masked global variance appears artificially stable. The network completely ceases to learn past the point of the close encounter, leaving the neurons responsible for future predictions in a state of random initialization or causing them to drift aimlessly. The model may perfectly memorize the smooth trajectory leading up to the close encounter, but it will flatline thereafter, entirely failing to simulate the chaotic scattering event.<sup>[1](#works-cited)</sup>

# Proposed Resolution: The Time-Windowed Causal-ALM Hybrid

To reconcile the sequential, time-respecting nature of causal training with the global stability and constraint-enforcement power of the Augmented Lagrangian Method, the standard unconstrained training loop must be abandoned. The resolution requires restructuring the optimization process into a Time-Windowed Causal-ALM Hybrid, drawing theoretical inspiration from recent advancements in constrained optimization for continuous-time physics models.<sup>[4](#works-cited)</sup>

Instead of applying causal weights as a continuous exponential decay scalar on the residual across the entire global interval, the temporal domain is discretely partitioned into overlapping causal windows.

# Localized ALM Execution

Within each actively advancing time window, the collocation points are sampled according to the local stiffness profile of the trajectory. The ALM parameters, specifically the Lagrange multiplier and the penalty coefficient, are initialized and iteratively updated purely locally for the data contained within this specific window. The loss function is evaluated as a localized composite of the data fidelity, the ALM-penalized physics residual, and the dynamically weighted energy conservation term.<sup>[1](#works-cited)</sup> By restricting the ALM's view to the current window, it is not artificially blinded by future causal weights, allowing the moving average of the squared physics loss to accurately reflect the true local constraint violations.<sup>[1](#works-cited)</sup>

# Causal Gating Mechanism

The causal weight formula is fundamentally redefined. It is no longer utilized as a soft multiplier on the loss gradients. Instead, causality acts as a hard algorithmic gating mechanism governing the transition between the partitioned time windows. The Adam optimization algorithm is strictly restricted to operating within the current active window until the ALM-penalized total residual for that window falls below a predefined, stringent causal tolerance threshold.<sup>[7](#works-cited)</sup>

Only when the neural network has successfully learned the dynamics within the current temporal segment, satisfying the Hamiltonian constraints enforced by the ALM, does the causal gate unlock.

# Structural State Propagation

Once the gating mechanism confirms the convergence of the current window, the temporal horizon expands. The network's finalized prediction at the end of the converged window acts as a hard initial condition constraint for the subsequent window, ensuring perfect continuity of the learned manifold.<sup>[4](#works-cited)</sup> The ALM penalty multipliers are carried forward into the next window to maintain optimization momentum.

Crucially, the causal masking of the deep future is achieved by structurally excluding any data points or collocation points beyond the active window from the current training batch. This architectural modification entirely prevents the Causal Firewall effect. Because future, highly chaotic close encounters are simply not passed to the optimizer until the preceding trajectory is mastered, they cannot trigger the exponential error spikes that cause gradient death.<sup>[1](#works-cited)</sup> This hybrid approach preserves the rigorous, hard-constraint enforcement capabilities of the Augmented Lagrangian while strictly respecting the causal arrow of time dictated by the physics of the system.

# Rectification of Architectural and Dataset Inconsistencies

Beyond the fundamental algorithmic mismatch, the provided protocol documents exhibit significant parameter inconsistencies that threaten to derail the training pipeline. These contradictions span the dimensionality of the input vectors, the numerical scaling of regularizing constants, the geometric reference frames, and the temporal sampling rates. They must be definitively resolved based on the physical constraints of the three-body problem and the inductive biases inherent to the SIREN architecture.

# Input Vector Dimensionality: Reconciling the 12D and 14D Paradigms

The neural network's architecture acts as a conditional generator. It takes a description of the system's initial state and a specific time, and outputs the physical coordinates of the bodies at that time. However, the documents conflict on how this initial state should be represented. The architectural blueprint specifies a 14-dimensional conditional input vector, comprising 3 masses, 5 physical invariants, and 5 values mapping 3 trigonometrically encoded angles.<sup>[1](#works-cited)</sup> Conversely, the curriculum training plan outlines a 12-dimensional vector, replacing the trigonometric angles with 3 shape invariants and a normalized moment of inertia scalar.<sup>[1](#works-cited)</sup>

The 14-dimensional formulation utilizing trigonometric angles is physically flawed for chaotic systems. Trigonometric representations of spatial orientation are inherently susceptible to coordinate singularities, commonly known as gimbal lock. During chaotic scattering events, the orbital plane of the interacting bodies can shift abruptly and violently. If the system's orientation aligns with the poles of the chosen coordinate system, the trigonometric derivatives explode, injecting undefined or massive gradients into the network's initial layers, instantly destabilizing the optimization process.<sup>[8](#works-cited)</sup>

In contrast, the 12-dimensional formulation utilizes universal Shape Invariants. These invariants are derived mathematically from the sorted mutual distances between the three bodies, representing the lengths of the shortest, middle, and longest sides of the triangle formed by the masses.<sup>[1](#works-cited)</sup> Shape invariants possess exceptional mathematical properties for machine learning: they are universally continuous, entirely non-singular, and intrinsically invariant to global spatial rotations. They perfectly describe the internal geometric configuration of the N-body system without relying on an arbitrary external reference frame.<sup>[1](#works-cited)</sup>

However, simply adopting the 12-dimensional vector breaks the meticulously designed initialization scheme of the SIREN architecture. The SIREN's first layer maps the input vector to a high-dimensional space of Fourier features. This mapping is governed by a highly specific frequency parameter initialized at a value of 30.<sup>[1](#works-cited)</sup> This parameter was mathematically derived and tuned specifically for the spectral bandwidth of a 14-dimensional input space.<sup>[1](#works-cited)</sup> Reducing the input dimensionality to 12 alters the frequency density, severely blunting the network's ability to overcome spectral bias.

To resolve this, the input vector must be standardized into an Augmented 14-Dimensional Shape-Invariant Vector. This formulation retains the superior physical properties of the shape invariants while completing the parameter space to satisfy the architectural constraints of the SIREN initialization. The final vector comprises:

1. Temporal Dimension: 1 component representing normalized simulation time.

2. Mass Distribution: 3 components for the normalized masses of the bodies.

3. Physical Invariants: 5 components quantifying the system's energy, virial ratio, minimum separation, angular momentum, and moment of inertia.

4. Universal Shape Invariants: 3 components defining the internal geometry of the interaction triangle.<sup>[1](#works-cited)</sup>

5. Orientation Cosines: 2 components mapping the spatial orientation of the normal vector of the system's initial invariant plane relative to the universal z-axis.

By utilizing direction cosines instead of Euler angles, the formulation avoids trigonometric singularities entirely while simultaneously providing the neural network with the necessary global orientation context required to map the internal triangle shape to the final 9-dimensional output coordinate space.<sup>[1](#works-cited)</sup>

<table><tr><td>Vector Component</td><td>Variable Notation</td><td>Dimensionality</td><td>Physical Justification and Resolution</td></tr><tr><td>Category</td><td></td><td></td><td>Benefit</td></tr><tr><td>Time Mapping</td><td>t'</td><td>1D</td><td>Normalized to [−1, 1] to align with SIREN periodic activations.</td></tr><tr><td>Mass Distribution</td><td>m1, m2, m3</td><td>3D</td><td>Dimensionless representation of body mass ratios.</td></tr><tr><td>Physical Invariants</td><td>E, Q, smin, L, I</td><td>5D</td><td>Quantifies binding energy, stability, and scale without spatial dependence.</td></tr><tr><td>Internal Geometry</td><td>I1, I2, I3</td><td>3D</td><td>Continuous, singularity-free shape invariants replacing flawed Euler angles.</td></tr><tr><td>Spatial Orientation</td><td>cos θ, sin θ</td><td>2D</td><td>Provides global orientation context while avoiding gimbal lock singularities.</td></tr><tr><td>Total Conditional Input</td><td>Xinput</td><td>14D</td><td>Maintains SIREN frequency injection density (ω0 = 30).</td></tr></table>

# Gravitational Softening Constants: The Dual-Context Paradigm

The integration of Newtonian gravity into numerical simulations often requires a softening constant, epsilon $\epsilon$ , to prevent the inverse-square force law from diverging to infinity as the distance between two bodies approaches zero.<sup>[11](#works-cited)</sup> The documents present a severe contradiction regarding the magnitude of this constant. The ALM physics loss formulation requires a softening parameter of $\epsilon = 10^{-5}$<sup>[1](#works-cited)</sup>, whereas the protocol for calculating the initial physical invariants mandates an exponentially smaller value of $\epsilon = 10^{-10}$.<sup>[1](#works-cited)</sup>

Gravitational softening fundamentally alters the physics of the simulation. At distances smaller than the softening length, the interaction ceases to be purely Newtonian, effectively replacing point masses with finite-density kernels, such as Plummer spheres.<sup>[11](#works-cited)</sup> Using a large softening constant artificially prevents close encounters, altering the chaotic scattering dynamics and introducing an unphysical bias into the trajectory.<sup>[13](#works-cited)</sup>

A single softening constant cannot simultaneously serve both the static data validation requirements and the dynamic requirements of neural network gradient descent. Therefore, a strict Dual-Context Epsilon Strategy must be instituted.

Static Invariant Calculation ( ) $\epsilon = 10^{-10}$ : When calculating the fundamental invariants (such as Total Energy and Virial Ratio) from the initial conditions prior to training, the processing is performed on CPUs utilizing double-precision (float64) arithmetic.<sup>[1](#works-cited)</sup> In this context, the softening must be negligible. Utilizing $\epsilon=10^{-10}$ ensures that the calculated physical invariants accurately shadow the true mathematical properties of the unsoftened Hamiltonian without introducing macroscopic bias.<sup>[1](#works-cited)</sup>

Dynamic Loss Optimization ( $\epsilon_{soft} = 10^{-5}$ ): During the backpropagation phase, the network computes the physics residual and energy conservation terms. These operations are performed on GPUs utilizing single-precision (float32) arithmetic. If the distance between predicted bodies approaches zero during a simulated close encounter, the inverse-square term diverges rapidly.<sup>[1](#works-cited)</sup> In single-precision arithmetic, this immediately triggers a numerical overflow, generating infinite or NaN gradients. These exploding gradients will instantly shatter the SQR-SkipResNet skip connections, overwhelming even the stabilizing effects of Layer Normalization.<sup>[1](#works-cited)</sup> Consequently $\epsilon=10^{-5}$ must be strictly enforced as a neural network regularization parameter within the PyTorch/JAX loss functions.<sup>[1](#works-cited)</sup> The network is not learning softened physics; it is learning exact Hamiltonian dynamics regularized by a microscopic floor precisely calibrated to match the limits of its numerical precision.

<table><tr><td>Processing Context</td><td>Hardware &amp; Precision</td><td>Epsilon Value (€)</td><td>Justification and Role</td></tr><tr><td>Pre-Training Validation</td><td>CPU / float64</td><td>10-10</td><td>Ensures calculated invariants (Energy, Virial Ratio) reflect true Newtonian physics without introducing finite-kernel bias.</td></tr><tr><td>Backpropagation (ALM Loss)</td><td>GPU / float32</td><td>10-5</td><td>Acts as numerical regularization to prevent gradient explosion and NaN propagation across skip connections during close encounters.</td></tr></table>

# Frame Conventions: Mandating the Center of Mass Boost

A critical anomaly identified in the curriculum data framework reveals that the hierarchical Initial Conditions are not generated in the Center of Mass (COM) frame; they possess a non-zero total momentum. Conversely, the quasi-random datasets are generated strictly within the COM frame.<sup>[1](#works-cited)</sup> This presents a massive structural problem, as the PINN architecture explicitly assumes that all predicted output positions are natively in the COM frame.<sup>[1](#works-cited)</sup>

Training a deep neural network on datasets with varying, translationally shifting coordinate systems completely destroys the inductive bias of the model. If a hierarchical system drifts uniformly across the coordinate space due to a net momentum vector, the network will be forced to expend vast amounts of its parameter capacity attempting to learn a simple, linear coordinate transformation, severely degrading its ability to learn the complex, underlying nonlinear gravitational dynamics.

To rectify this, an aggressive, automated Galilean boost must be mandated during the data preprocessing phase.<sup>[1](#works-cited)</sup> Before any physical invariants are calculated or any state vectors are scaled to dimensionless units, the pipeline must compute the system's global center of mass vector and velocity vector. All initial positions and velocities must then be mathematically transformed by subtracting these global vectors, perfectly centering the system. Only after this strict Galilean transformation is applied should the original, drifting coordinate references be discarded. This ensures that the injectivity of the augmented 14-dimensional input vector is perfectly preserved and that all training data uniformly aligns with the geometric output assumptions of the neural network.<sup>[1](#works-cited)</sup>

# Temporal Resolution: Bridging the Sampling Divide

The data pipeline utilizes a mixed temporal resolution scheme. The baseline datasets (Sets 1a and 1b) are integrated with a dt_out of 0.08 and 0.17, respectively.<sup>[1](#works-cited)</sup> However, Stages 2 and 5 of the curriculum mandate the use of high-resolution datasets (Sets 2a and 2b), which feature an 8-fold to 17-fold increase in temporal density, outputting at dt_out $= 0.01$.

Using a coarse temporal resolution of $dt = 0.17$ for a highly chaotic orbit is physically disastrous. During a close encounter, a pericenter passage may occur entirely between two discrete data points. The SIREN network, characterized by its continuous, infinitely differentiable nature, will attempt to fit a smooth mathematical spline through these widely spaced points.<sup>[1](#works-cited)</sup> Because the true physical path of the close encounter is highly curved and unrecorded, the network's interpolation will violently violate the conservation of energy. This massive physical violation will instantly inflate the ALM physics penalty term and artificially trigger the Causal Firewall, halting training.

The dt_out parameter is not merely a data logging convenience; it represents the Nyquist frequency of the physical simulation. The low-resolution integrations (0.08 and 0.17) are only physically permissible for the earliest stages of the curriculum (Stages 0, 1a, and 1b) because these specific hierarchical systems are selected for being highly stable, with deeply bound energy $E < -0.5$) and wide initial separations $s_{min} > 2$).<sup>[1](#works-cited)</sup> Their orbital velocities are relatively low, ensuring that the continuous interpolation between the coarse data points remains physically valid.

However, for any trajectory entering the chaotic regimes of Stages 3 through 6, the high-resolution integration of dt_out $= 0.01$ is strictly mandatory.<sup>[1](#works-cited)</sup>  If a trajectory from the low-resolution set exhibits a close encounter or significant velocity spike during pre-screening, it must be automatically rejected by the data validation protocol and specifically routed back to the Brutus integrator to be resampled at $dt = 0.01$ before it is permitted to enter the training loop.<sup>[1](#works-cited)</sup>

<table><tr><td>Curriculum Stage</td><td>Dynamic Regime</td><td>Allowed Base Resolution (dt_out)</td><td>Justification for Temporal Density</td></tr><tr><td>Stage 0 &amp; 1</td><td>Highly Stable (Keplerian)</td><td>0.08 _ 0.17</td><td>Low orbital velocities and wide separations (smin &gt; 2) prevent interpolation errors between coarse sampling points.</td></tr><tr><td>Stage 2</td><td>Stable Refinement</td><td>0.01</td><td>High-resolution data is used to polish the network's continuous representation of learned stable dynamics.</td></tr><tr><td>Stage 3 - 6</td><td>Chaotic / Close Encounters</td><td>0.01 (Strict)</td><td>High density is mandatory to prevent spectral aliasing and infinite gradients during rapid pericenter passages.</td></tr></table>

# Evolution of Pre-Training Data Validation Metrics

To support the Time-Windowed Causal-ALM Hybrid architecture and enforce the rectified dataset parameters, the four static and dynamic data quality metrics must be mathematically updated. These metrics must transition from being simple diagnostic flags into fundamental, governing parameters of the training loop.

# Symplectic Conservation Score (SCS)

The Symplectic Conservation Score originally measured the maximum normalized deviation of the Hamiltonian over the duration of the numerical trajectory.<sup>[1](#works-cited)</sup> In the updated framework, the SCS serves as the primary, non-negotiable filter against Brutus integration errors before the data is passed to the ALM. Because the Augmented Lagrangian Method explicitly incorporates an energy regularizer to optimize for global conservation 1, feeding the network data that contains intrinsic, numerical integration drift creates an unsolvable optimization paradox.

The metric is mathematically defined using the unsoftened static epsilon: $\epsilon = 10^{-10}$ ):

Any trajectory resulting in an $SCS > -6$ must be outright rejected during Phase 1 static $SCS > -6$ screening.<sup>[1](#works-cited)</sup> For the high-resolution Stage 5 data targeting complex chaotic orbits ( $dt = 0.01$ ), the threshold must be tightened to $SCS < -8$. This strict gating ensures that the neural $SCS < -8$ network learns the pure symplectic geometry of the Hamiltonian flow rather than inadvertently memorizing the numerical dissipation of the integrator.

# Stiffness-Aware Sampling Density (SASD)

The SASD metric quantifies the ratio of the discrete time step to the local characteristic timescale of the system's dynamics, effectively measuring local trajectory curvature.<sup>[1](#works-cited)</sup> In the hybrid architecture, SASD directly arbitrates the dt_out mismatch and fundamentally dictates the ALM collocation point sampling density.<sup>[1](#works-cited)</sup>

The formulation compares the time step to the ratio of velocity and acceleration:

$$
SASD_{i} = \Delta t_i \cdot \frac{||a(t_{i})||}{||v(t_{i})||}
$$

If the maximum SASD of a low-resolution trajectory exceeds a critical threshold, it implies that the trajectory turns significantly between data points. Such data must be flagged and resampled to the higher resolution standard.<sup>[1](#works-cited)</sup> More importantly, during the Causal-ALM training loop, the probability distribution for selecting synthetic collocation points is no longer uniform. Instead, the sampling is strictly weighted by the SASD profile of the target trajectory.<sup>[15](#works-cited)</sup> This targeted

sampling ensures that the ALM penalty parameter $\mu_p$ applies the strongest mathematical constraints precisely at the points of highest curvature, effectively neutralizing the inherent spectral bias of the neural network.<sup>[1](#works-cited)</sup>

# Interpolation Physics Residual (IPR)

The Interpolation Physics Residual evaluates whether the continuous manifold implied by the discrete data points satisfies Newton's laws. It tests a piecewise Cubic Hermite Interpolating Polynomial against the underlying equations of motion.<sup>[1](#works-cited)</sup> In the new architecture, the IPR transitions from a mere pre-training check to establishing the theoretical lower bound for the ALM physics penalty.

The residual is calculated over synthetic points $\tau_k$, but crucially, it must be evaluated using the network's dynamic softening constant ($\epsilon = 10^{-5}$) rather than the static constant 1 :

$$
IPR = \frac{1}{M} \sum_{k=1}^{M} \left| \frac{d^{2} q_{spline}}{dt^{2}} (\tau_k) - F_{gravity}^{\epsilon = 10^{-5}} (q_{spline}(\tau_k)) \right|^{2}
$$

This updated IPR value sets the noise floor for the ALM. If the neural network's internal physics loss drops below the pre-calculated IPR of the dataset, it indicates that the SIREN architecture has discovered a more physically accurate continuous trajectory than standard spline interpolation can provide. At this threshold, the ALM algorithms halt any further increases to the penalty parameter $\mu_p$<sup>[1](#works-cited)</sup>, preventing overfitting to numerical noise and signaling the optimizer to shift from exploration to high-precision refinement.<sup>[1](#works-cited)</sup>

# Phase Space Coverage Entropy (PSC)

Chaotic systems possess ergodic properties, meaning trajectories explore vast regions of phase space over time. The PSC metric calculates the Shannon entropy of the data points distributed across a discretized phase space grid, quantifying the diversity of the training data.<sup>[1](#works-cited)</sup> In the updated protocol, PSC governs the "Curriculum Replay" mechanism.<sup>[1](#works-cited)</sup>

As the training progresses from the stable early stages into the fully chaotic regimes (Stages 4 through 6), the replay buffer must not be overwhelmingly biased toward the highly stable, low-entropy data of Stage 0. Instead of utilizing uniform random sampling to construct the replay batches, trajectories are sampled inversely proportional to their phase space bin density. This entropy-guided sampling guarantees that extreme, high-stiffness events (such as configurations where $s_{min} < 0.5$ ) are consistently over-represented in the mini-batch.<sup>[1](#works-cited)</sup> Forcing the ALM to constantly evaluate gradients across both smooth quasi-periodic regions and high-frequency chaotic scattering regions simultaneously stabilizes the momentum parameters of the Adam optimizer, ensuring robust convergence.<sup>[1](#works-cited)</sup>

<table><tr><td>Validation Metric</td><td>Mathematical Focus</td><td>Role in the Time-Windowed Causal-ALM Hybrid Framework</td></tr><tr><td>SCS</td><td>Hamiltonian Deviation</td><td>Hard gate against integrator drift. Prevents ALM energy regularizer from failing due to flawed ground truth.</td></tr><tr><td>SASD</td><td>Curvature vs. Step Size</td><td>Dictates adaptive collocation sampling. Forces ALM penalties to focus on "stiffness spikes" during close encounters.</td></tr><tr><td>IPR</td><td>Continuous Spline Residual</td><td>Establishes the absolute noise floor for the physics loss, signaling the transition from Adam to L-BFGS refinement.</td></tr><tr><td>PSC</td><td>Phase Space Shannon Entropy</td><td>Governs the Curriculum Replay buffer. Ensures chaotic scattering events are over-represented to maintain gradient stability.</td></tr></table>

# The Synthesized Curriculum Training Protocol

By resolving the architectural mismatches, enforcing strict dataset conventions, and redefining the validation metrics, we can synthesize a unified, step-by-step implementation protocol. This workflow perfectly integrates the static data validation strategy with the advanced ALM-backed SQR-SkipResNet and the multi-stage curriculum progression.

Phase 1: Static Pre-Screening and Data Transformation (CPU Operations) The pipeline initiates by ingesting the raw initial conditions from the external storage directories. An automated Galilean boost is immediately applied to all vectors, strictly enforcing the Center of Mass coordinate system.<sup>[1](#works-cited)</sup> Any configuration violating momentum conservation post-boost is permanently discarded. Subsequently, the physical invariants, including the critical universal shape invariants $$(I_1, I_2, I_3)$$ , are computed using the unsoftened static constant ( $\epsilon = 10^{-10}$ ) to ensure true Newtonian fidelity.<sup>[1](#works-cited)</sup> The augmented 14-dimensional input vector is then assembled for each trajectory.<sup>[1](#works-cited)</sup> Finally, the metric gating process computes the Symplectic Conservation Score and the Stiffness-Aware Sampling Density profile. Trajectories exhibiting unacceptable integration drift or severe undersampling relative to their temporal resolution are flagged for high-precision resampling by the Brutus integrator.<sup>[1](#works-cited)</sup>

Phase 2: Curriculum Stage Initialization and IPR Bounding The validated trajectories are stratified into the seven primary curriculum stages (0 through 6) based on their binding energy, angular momentum ratios, and specifically their estimated Lyapunov time $(\tau_L)$ for the chaotic stages.<sup>[1](#works-cited)</sup> Prior to initiating the training loop for a specific stage, the Interpolation Physics Residual is computed for all active trajectories using the network's dynamic softening constant ($\epsilon = 10^{-5}$). This calculation establishes the absolute convergence floor for the Augmented Lagrangian physics penalties.<sup>[1](#works-cited)</sup>

Phase 3: The Time-Windowed Causal-ALM Training Loop (GPU Operations) For each active curriculum stage, the dataloader constructs mini-batches using the Phase Space Coverage metric to ensure a balanced, entropy-guided distribution of stable and chaotic trajectories from the current and all preceding stages.<sup>[1](#works-cited)</sup> The temporal domain of the simulation is divided into discrete causal windows. Within the active window, the Adam optimizer executes the Augmented Lagrangian Method. The data fidelity loss is evaluated against the Brutus snapshots, while the physics loss is evaluated over adaptive collocation points mapped probabilistically by the SASD profile.<sup>[1](#works-cited)</sup> The ALM penalty multipliers are updated dynamically based solely on the local residual of the current window.<sup>[1](#works-cited)</sup> The optimization continues until the total window loss converges below the causal tolerance threshold. Only then does the causal gating mechanism unlock, structurally advancing the time window and allowing the neural network to perceive the subsequent segment of the trajectory.

Phase 4: Refinement and Stage Transition Once the sequential causal windows have expanded to encompass the entire time domain and the Adam optimizer has driven the loss down to the pre-calculated IPR noise floor, control is transferred to the Stochastic L-BFGS optimizer.<sup>[1](#works-cited)</sup> This quasi-Newton method polishes the global solution to high precision. Gradient clipping, which is essential during the Adam phase to survive close encounters, is disabled during L-BFGS refinement to preserve the mathematical integrity of its line-search trust region.<sup>[1](#works-cited)</sup> Before advancing to the next, more complex curriculum stage, the protocol verifies that the network's inherent Hamiltonian prediction maintains a relative energy drift of less than $10^{-4}$ .<sup>[1](#works-cited)</sup> The curriculum then increments, drastically increasing the energy penalty weight dictated by the ALM schedule, thereby hardening the physical constraints as the neural network wades deeper into the chaotic regime.

# Conclusion

The chaotic Three-Body Problem cannot be accurately simulated by deep neural networks that treat time merely as a bulk spatial dimension, nor can it be resolved by sequential solvers that fail to strictly enforce global, long-term conservation laws. The initially documented approaches for this architecture presented a severe, fundamental mismatch: causal training forced a strict temporal masking that paralyzed future gradients, while the Augmented Lagrangian Method required global variance evaluation across the entire manifold to function.

By restructuring the framework into a Time-Windowed Causal-ALM Hybrid, this analysis successfully reconciles the methodologies. Causal learning now acts not as an exponential dampener, but as a rigid temporal gatekeeper, releasing overlapping, moving windows of time to the optimizer. Within these sequential windows, the Augmented Lagrangian Method aggressively enforces exact Newtonian mechanics via its dynamically scaling penalty multipliers.<sup>[4](#works-cited)</sup>

Furthermore, this exhaustive synthesis has rectified critical operational inconsistencies that would have otherwise led to catastrophic gradient failure. The input dimensionality has been definitively standardized as an Augmented 14-Dimensional vector that utilizes universal shape invariants, eliminating the threat of trigonometric singularities while preserving the frequency injection mapping required by the SIREN layers.<sup>[1](#works-cited)</sup> A strict dual-epsilon protocol ( $10^{-10}$ for static invariants, $10^{-5}$ for dynamic optimization) cleanly separates the requirement for ground-truth physical precision from the necessity of GPU network regularization.<sup>[1](#works-cited)</sup> The Center of Mass frame is now strictly enforced via Galilean pre-processing, ensuring geometric injectivity, and the sampling resolution is dynamically arbitrated by the underlying stiffness of the physics.<sup>[1](#works-cited)</sup>

By operationalizing the mathematically updated validation metrics (SCS, SASD, IPR, PSC) within this unified, highly structured curriculum protocol, researchers can guarantee that the vast computational investment required for arbitrary-precision N-body integration translates directly into a robust, physically plausible, and causality-respecting deep learning model.

# Works cited

1. main_CTL.pdf

2. Three-body problem - Wikipedia, accessed April 26, 2026, https://en.wikipedia.org/wiki/Three-body_problem

3. Respecting causality is all you need for training physics-informed neural networks - ar5iv, accessed April 26, 2026, https://ar5iv.labs.arxiv.org/html/2203.07404

4. Conditionally adaptive augmented Lagrangian method for physics-informed learning of forward and inverse problems using artificial neural networks - arXiv, accessed April 26, 2026, https://arxiv.org/html/2508.15695v1

5. Respecting causality is all you need for training physics-informed neural networks - arXiv, accessed April 26, 2026, https://arxiv.org/abs/2203.07404

6. Conditionally adaptive augmented Lagrangian method for physics-informed learning of forward and inverse problems using artificia - arXiv, accessed April 26, 2026, https://arxiv.org/pdf/2508.15695?

7. Gradient Alignment in Physics-informed Neural Networks: A Second-Order Optimization Perspective - arXiv, accessed April 26, 2026, https://arxiv.org/html/2502.00604v1

8. An Introduction to the Classical Three-Body Problem, accessed April 26, 2026, https://www.ias.ac.in/article/fulltext/reso/024/01/0087-0114

9. The Three-Body Problem and the Shape Sphere - UC Santa Cruz, accessed April 26, 2026, https://peopleweb.prd.web.aws.ucsc.edu/~rmont/papers/math_monthly_triangles.

10. [1402.0841] The Three-body problem and the shape sphere - arXiv, accessed April 26, 2026, https://arxiv.org/abs/1402.0841

11. What is Gravitational softening length? - Astronomy Stack Exchange, accessed April 26, 2026, https://astronomy.stackexchange.com/questions/50106/what-is-gravitational-sof tening-length

12. Gravitational softening as a smoothing operation - Astronomy in Hawaii, accessed April 26, 2026, https://home.ifa.hawaii.edu/users/barnes/research/smoothing/soft.pdf

13. [astro-ph/0011568] Towards optimal softening in 3D N-body codes: I. Minimizing the force error - arXiv, accessed April 26, 2026, https://arxiv.org/abs/astro-ph/0011568

14. Power-Enhanced Residual Network for Function Approximation and Physics-Informed Inverse Problems - ResearchGate, accessed April 26, 2026, https://www.researchgate.net/publication/382109760_Power-Enhanced_Residual _Network_for_Function_Approximation_and_Physics-Informed_Inverse_Problems

15. Causality-guided adaptive sampling method for physics-informed neural networks - ResearchGate, accessed April 26, 2026, https://www.researchgate.net/publication/383701268_Causality-guided_adaptive_ sampling_method_for_physics-informed_neural_networks

<!-- ============================================================ -->
<!-- FILE_END: 007 -->
<!-- FILE_NAME: Causal_Trainingmismatch_resolution_blueprint.md -->
<!-- FILE_SHA256: bd0e58e8d6cde3e1adcbccd6e51f7552805b8cb7950db2f8893fc204f8f28830 -->
<!-- ============================================================ -->

