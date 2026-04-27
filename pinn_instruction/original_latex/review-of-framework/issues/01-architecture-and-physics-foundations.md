# 01 — Architecture and Physics Foundations

## Executive Summary

This document consolidates all identified findings, critical issues, and open decisions related to the PINN network architecture, input vector design, and fundamental physics conventions across the three-body simulation framework. Source material is drawn from the 2026-04-27 comprehensive technical audit, the Causal Training Mismatch resolution blueprint, the scaling-contract review, and cherry-picked unique content from `next steps.txt` and `next-step-for-data-processing-pipeline.txt`.

The architecture baseline is an SQR-SkipResNet-SIREN hybrid: 12 hidden layers of 256 neurons with sinusoidal activations, power-enhanced skip connections (p=2), and LayerNorm stabilization on odd layers. The input vector is 14-dimensional — 1 normalized time coordinate plus a 13-component initial-condition descriptor. The network outputs 9-dimensional 3D positions for three gravitationally interacting bodies.

**Readiness assessment: NOT READY FOR IMPLEMENTATION.** Three blocking issues must be resolved before coding begins: the SIREN hidden-layer initialization formula inverts the Sitzmann et al. (2020) specification; the characteristic length D has two contradictory formulas (both wrong — correct value is 6.694); and the input vector composition is unresolved between a trigonometric encoding and a shape-invariants-plus-direction-cosines approach. Seven additional critical blockers are documented below.

---

## Confirmed Findings

### BLOCKING (Must resolve before implementation)

| ID | Severity | Finding | Location | Fix |
|----|----------|---------|----------|-----|
| B-01 | **BLOCKING** | SIREN hidden-layer init formula **multiplies** by omega0 instead of **dividing**. At hidden_omega0=1 the bug is latent; at omega0=30 variance explodes 810,000x → instant NaN across 12 layers. Contradicts Sitzmann et al. (2020) NeurIPS. | `basic_architecture.py:37`, `main_pinn.pdf` Table 1 | `bound = np.sqrt(6.0 / n_in) / hidden_omega0` (divide, not multiply) |
| B-02 | **BLOCKING** | Characteristic length D has two contradictory formulas. CTL: `D = cbrt(3GT^2) ≈ 4.64` (wrongly omits M_tot=3). PINN: `D = sqrt(3GT^2)` (dimensionally L^(3/2)/M^(1/2), not L). **Correct:** `D = (G * M_tot * T^2)^(1/3) = (3 * 100)^(1/3) = 6.694` | `main_CTL.pdf` Sec 4.2, `main_pinn.pdf` Table 2 | Adopt D = 6.694 everywhere. Recompute ALL scaled quantities and stage assignments. |
| B-03 | **BLOCKING** | Input vector dimensionality claimed as 12D, 13D, and 14D simultaneously across documents. No fixed n_in for the first Linear layer. | `main_CTL.pdf` Sec 4.5, `main_pinn.pdf` Table 2 | Adopt **14D** as canonical: t' (1D) + IC (13D). |
| B-04/B-05 | **BLOCKING** | Input vector composition is unresolved. Audit recommends 5 trig values for 3 angles. Causal_Trainingmismatch argues trig encodings suffer gimbal lock during chaotic scattering and proposes shape invariants + direction cosines. | Audit §5.3 vs Causal_Trainingmismatch §Input Vector | **Resolved:** shape invariants + direction cosines (see Open Decisions below). |
| B-05 | **BLOCKING** | COM frame violation in hierarchical ICs. |COM| ~ 9e-3 after Gaussian perturbation. PINN assumes COM-frame outputs but targets are not in COM frame. | `README.md` lines 328-335, `main_CTL.pdf` Sec 4.3 | Unified COM transformer: recenter + reboost FIRST, then scale. Assert mass consistency. |
| B-09 | **BLOCKING** | Softening parameter mismatch by 10^5×. CTL uses eps=1e-10 for invariant E (stage assignment). PINN uses eps_soft=1e-5 for physics residual and energy loss. Different physics for curriculum vs training. | `main_CTL.pdf` Sec 4.4, `main_pinn.pdf` Sec 3.2-3.3 | Adopt Dual-Context Epsilon Strategy: eps=1e-10 for static invariants (CPU/float64), eps_soft=1e-5 for dynamic loss (GPU/float32). See resolution below. |
| B-10 | **BLOCKING** | Dynamic omega0 scheduling has no runtime effect. `update_omega0()` decays first_omega0 from 30 to 10 over epochs, but omega0 is used ONLY at weight initialization. Changing it post-init does nothing. | `main_pinn.pdf` Sec 2.2, Listing 1 | **Remove the scheduling function.** Use fixed first_omega0=30, hidden_omega0=1. |

### MAJOR (Degrades correctness or blocks dependent work)

| ID | Severity | Finding | Resolution Strategy |
|----|----------|---------|---------------------|
| M1 | MAJOR | CTL assembles 11D IC (masses + 5 invariants + 3 shape invariants); PINN expects 13D IC. Dimension gap of 2 components. | Adopt PINN's 13D IC as architecture contract. |
| M2 | MAJOR | Total dimension claims: 12D (CTL title), 13D (CTL "13-component IC"), 14D (CTL closing note, PINN). No consistent count. | Adopt **14D** as canonical: [t', IC_13D]. |
| M3 | MAJOR | Scaling order: CTL scales in Step 2, COM-transforms in Step 2.5. For hierarchical ICs, scaled COM offset survives. | **COM transform FIRST, then scale.** |
| M4 | MAJOR | Constraint counting error: "13 constraints for 8-D reduced phase space" — but 18 - 3(COM) - 3(P) - 3(SO(3)) = 9 DOF, not 8. | Correct to: "9 constraints reduce 18-DOF to 9 dimensions." |
| M5 | MAJOR | I_3 claimed "already in [-1,1]" but formula gives I_3 in [0,1]. | Apply `I3_norm = 2*I3 - 1` to map [0,1] → [-1,1]. |
| M8 | MAJOR | LayerNorm on skip path attributed to SQR-SkipResNet paper, but the original paper (arXiv:2310.15690v2) has NO LayerNorm anywhere. | Re-attribute as author modification. |
| M9 | MAJOR | E_norm only uses [-1, 0) — positive input range never used since E < 0 for bound systems. | Acceptable for SIREN. Document that positive range is unused. |
| M10 | MAJOR | m_norm range asymmetric for hierarchical masses: [-0.93, 0.585], not centered on 0. | Acceptable — asymmetry carries mass hierarchy information. |

### MINOR / INFO (Design ambiguities and documentation gaps)

| ID | Severity | Question | Proposed Path |
|----|----------|----------|---------------|
| D1 | MINOR | What exactly are the 3 angles for trigonometric encoding? | Proposed: (theta_L, phi_L) = spherical coords of L_hat; gamma_orb = orbital phase. |
| D2 | MINOR | Does LayerNorm on skip path actually help? | Ablate: train with/without skip-path LayerNorm. |
| D3 | MINOR | LayerNorm affine=True or affine=False? | Default `affine=False` (safer). LayerNorm's purpose is normalization, not feature transformation. |
| D4 | MINOR | Should quasi-random IC Brutus outputs get COM-corrected? | Experiment: parse 100 trajectories. If COM drift > 1e-12, apply correction. |
| D6 | MINOR | How to handle Brutus mass drift between snapshots? | Compare m_IC vs m_Brutus_t=0 with np.allclose(rtol=1e-15). |
| D8 | MINOR | Should s_min use softening for Stage 6 collision criterion? | Keep s_min unsoftened for physical measurement. Use `max(s_min, epsilon)` as floor for criteria. |
| D9 | MINOR | Is the orientation representational gap fatal? | The direction-cosines encoding resolves this. Verify with small MLP: if MSE < 1e-4, sufficient. |
| D10 | MINOR | Can training start with standard SIREN init while D formula is being fixed? | Yes partially. Use D=6.694 from day one to avoid retraining. Priority P0. |

---

## AD Chain-Rule Factor — Missing Derivative Conversion

**Source:** `review.md` (scaling-contract review)

**Finding (MAJOR):** The PINN takes normalized time τ = 2t/T - 1 as input and outputs dimensionless positions r'(τ). Automatic differentiation computes derivatives with respect to τ, but the physics residual and energy loss require derivatives with respect to physical time t (or dimensionless time u = t/T). The chain-rule conversion factors are:

```
u = t/T
τ = 2u - 1

d/du = 2 * d/dτ        (first derivative: factor of 2)
d²/du² = 4 * d²/dτ²    (second derivative: factor of 4)
```

**Impact if unfixed:**
- Physics residual (uses d²/dτ² as though it were d²/du²): **off by factor of 4**
- Kinetic energy (uses d/dτ as though it were d/du): **off by factor of 4**

**Recommended three-layer separation formalism:**

```
(t, r, v)_raw  →  (u, r', v')_physics-scaled  →  (τ, IC_norm)_network-input
```

With explicit conversion rules:
- `r' = r / D`, `v' = v / (D/T)` (forward scaling)
- `dr'/du = 2 * dr'/dτ` (first derivative conversion)
- `d²r'/du² = 4 * d²r'/dτ²` (second derivative conversion)
- `v = (2D/T) * dr'/dτ`, `a = (4D/T²) * d²r'/dτ²` (back to original units)

Every loss function must declare which space it lives in. The physics loss converts AD derivatives in τ back to derivatives in u before computing the residual.

---

## Dual-Context Epsilon Strategy

**Source:** `Causal_Trainingmismatch_resolution_blueprint.md`

The softening parameter epsilon serves two fundamentally different roles that require two different values:

| Context | Hardware | Epsilon | Justification |
|---------|----------|---------|---------------|
| Static invariant calculation (E, Q, stage assignment) | CPU / float64 | **1e-10** | Negligible softening preserves true Newtonian fidelity. Calculated invariants accurately shadow the unsoftened Hamiltonian. |
| Dynamic loss optimization (physics residual, energy loss) | GPU / float32 | **1e-5** | Numerical regularization floor prevents gradient explosion and NaN propagation during close encounters in single-precision arithmetic. |

The dual-epsilon approach cleanly separates ground-truth physical precision from GPU numerical regularization. The network learns exact Hamiltonian dynamics regularized by a microscopic floor calibrated to GPU precision limits — it does NOT learn "softened physics."

### 5 Orders of Magnitude Difference — Softening Analysis

**Source:** `next steps.txt` (Issue 15, unique deep-dive analysis)

A five-order-of-magnitude gap between eps=1e-10 and eps_soft=1e-5 produces qualitatively different behavior at close encounters:

- **At r = 1.0 (wide separation):** Both epsilon values produce identical potentials to within 1e-8 relative error. The softening choice is irrelevant for quiescent phases.
- **At r = 0.01 (moderate close encounter):** eps=1e-5 softens the potential by ~0.1% relative to unsoftened Newtonian; eps=1e-10 is effectively exact.
- **At r = 0.001 (extreme close encounter):** eps=1e-5 softens by ~1%; eps=1e-10 softens by ~0.01%. The 1% difference in potential changes the local curvature of the loss landscape — gradient magnitudes differ by ~3% between the two epsilon values.
- **At r = 1e-4 (near-singularity):** eps=1e-5 is 100× larger than the separation — the softened potential is dominated by the softening kernel, not the 1/r² law. eps=1e-10 produces gradient norms ~10³× larger than eps=1e-5.

**Operational consequence:** Stage assignment (which uses eps=1e-10) correctly identifies systems that WILL experience close encounters at later times. But the training loss (which uses eps_soft=1e-5) evaluates those same encounters with softened dynamics. The curriculum gate and the loss function operate on different physics. For trajectories within ~15% of a stage boundary defined by s_min or E thresholds, this 1% potential difference can flip the stage label — making the network train on Stage-k data that the curriculum assigned to Stage-(k+1), or vice versa.

---

## Input Vector Normalization Formulas

**Source:** `next steps.txt` (Issue 19, canonical table)

| Component | Symbol | Normalization | Domain | Notes |
|-----------|--------|---------------|--------|-------|
| Time | t' | `2*t/T_max - 1` | [-1, 1] | T_max = 10 |
| Mass (×3) | m_norm,i | `2*(m_i/M_tot) - 1` | [-0.93, 0.585] (hier); [-1/3, -1/3] (equal mass) | Asymmetric for hierarchical |
| Energy | E_norm | `tanh(E / E_scale)` | [-1, 0) | E_scale = |median(E)|; positive range unused |
| Angular momentum | L_norm_norm | `2*clip(L/L_max, 0, 1) - 1` | [-1, 1] | L_max = M_tot * r_char * v_char |
| Virial ratio | Q_norm | `tanh((Q - 1) / 0.5)` | ~[-0.54, 0.54] | Q_scale = 0.5 fixed |
| Min separation | s_min_norm | `tanh(s_min / s_min_scale)` | [0, 1) | s_min_scale = median(r_char) |
| Moment of inertia | I_norm | **See Open Decision below** | [-1, 1] | Text vs code conflict |
| Shape invariants (×3) | I_1, I_2, I_3 | `2*(I_i / I_max) - 1` | [-1, 1] | I_3_norm needs 2*I3 - 1 mapping |
| Direction cosines (×2) | cos(θ), sin(θ) | Direct use | [-1, 1] | Orientation of invariant plane normal |
| **Total** | | | **14D** | t'(1) + IC(13) |

**Note on I_norm text-vs-code inconsistency (also from `next-step-for-data-processing-pipeline.txt`):**
The textual description defines `I_norm = tr(I) / (M_tot * r_char^2)`, while the code listing (`lst:inertia_calculation`) applies `tanh()` to that quantity. A later code listing repeats the `tanh` version. The `tanh` wrapper maps the result to [-1, 1] for neural network input but was never documented in the text. This is the canonical location for this table; `02-data-pipeline-and-validation.md` cross-links here.

---

## Frame Convention: Galilean Boost Mandate

**Source:** `Causal_Trainingmismatch_resolution_blueprint.md`

Hierarchical ICs are perturbed out of the COM frame (Gaussian noise σ=0.01 after COM enforcement). Quasi-random ICs are generated in the COM frame. The PINN architecture assumes all output positions are in the COM frame. Training on mixed-frame data destroys the model's geometric inductive bias — the network expends capacity learning linear coordinate transformations instead of nonlinear gravitational dynamics.

**Resolution:** Apply an aggressive automated Galilean boost during preprocessing, BEFORE any invariant calculation or scaling:

1. Compute COM position and velocity vectors from raw IC masses
2. Subtract COM position/velocity from all raw state vectors
3. Assert `||P_total|| < 1e-12` after transform
4. Only then proceed to scaling (r' = r/D, v' = v/(D/T))
5. Apply the same boost to Brutus output trajectories using the IC-derived COM

This ensures all training data uniformly aligns with the COM-frame output assumption.

**COM transform ordering (M3 fix):** COM transform FIRST, then scale. Scaling preserves non-zero COM; reordering eliminates this artifact.

---

## Dynamic Omega0 Scheduling — Removal

**Source:** Audit B-10

The `update_omega0()` function in the PINN architecture document decays first_omega0 from 30 to 10 over epochs. However, omega0 is an **initialization-only parameter** in the SIREN architecture — it controls the frequency scaling baked into weight magnitudes at init time. Changing it post-initialization has no effect on the weights.

**Fix:** Remove the scheduling function entirely. Use fixed `first_omega0=30`, `hidden_omega0=1`. If cross-stage re-initialization is desired for curriculum purposes, document it explicitly as a separate architectural decision with per-stage weight re-initialization — not epoch-based scheduling.

---

## Open Decisions

> **[DECISION-NEEDED]** Input vector composition (14-D IC content)
>
> Two competing proposals exist for the 5 orientation-encoding slots in the 13-component IC vector:
>
> **Option A — Trigonometric encoding (audit B-04, §5.3):**
> 5 values: `[sin(theta_L), cos(theta_L), sin(phi_L), cos(phi_L), sin(gamma_orb)]`
> where (theta_L, phi_L) are spherical coordinates of the angular momentum unit vector L_hat, and gamma_orb is the orbital phase of the heaviest body.
>
> **Option B — Shape invariants + direction cosines (Causal_Trainingmismatch):**
> 5 values: `[I_1, I_2, I_3, cos(theta), sin(theta)]`
> where (I_1, I_2, I_3) are the three shape invariants (sorted mutual distances), and (cos θ, sin θ) are direction cosines of the invariant plane normal relative to the z-axis.
>
> **Recommended resolution:** Adopt **Option B** (shape invariants + direction cosines) because:
> 1. Trigonometric encodings have known gimbal-lock pathologies during chaotic scattering events — the exact regime targeted by late curriculum stages. When L_hat aligns with a coordinate pole, trigonometric derivatives explode.
> 2. Shape invariants are universally rotation-invariant, continuous, and non-singular — they describe internal geometry without relying on arbitrary external reference frames.
> 3. Direction cosines provide global orientation without trigonometric singularities, giving the network the spatial context needed to map internal triangle shape to absolute 3D output positions.
> 4. The SIREN first layer (omega0=30) was tuned for 14-D spectral bandwidth — this composition preserves that dimensionality.
>
> Audit's trig encoding argument is well-reasoned but applies patterns from less-chaotic regimes. It is documented below under "Considered Alternatives."
>
> **Resolve before writing the first Linear layer.**

> **[DECISION-NEEDED]** `I_norm` definition — text formula vs code implementation
>
> Two conflicting definitions exist:
> - **Text:** `I_norm = tr(I) / (M_tot * r_char^2)` — a raw ratio, unbounded
> - **Code (lst:inertia_calculation):** `I_norm = tanh(tr(I) / (M_tot * r_char^2))` — same ratio passed through tanh to map to [-1, 1]
>
> The tanh version is consistent with all other IC vector components being in [-1, 1], but the text never mentions it. A second code listing independently repeats the tanh version, suggesting the text is stale rather than the code.
>
> **Recommended resolution:** Adopt the `tanh` version — it is consistent with the [-1, 1] normalization contract for all IC vector components. Update the textual description in CTL Sec 4.5 to explicitly state the tanh wrapper.
>
> **Resolve before finalizing the IC vector composition.**

---

## Recommended Resolutions

1. **P0 — Fix D formula:** Replace both D=4.64 and D=10 with D=6.694 everywhere. Recompute all scaled energies, L_norm values, Q values, and stage assignments.
2. **P0 — Fix SIREN init:** Change `bound = omega0 * sqrt(6/n)` to `bound = sqrt(6/n) / omega0` in `basic_architecture.py:37`.
3. **P0 — Adopt 14D input vector:** Canonicalize [t', IC_13D] with shape invariants + direction cosines per the recommended resolution above.
4. **P1 — Implement unified COM transformer:** COM-first ordering, single function for both ICs and Brutus outputs, mass-consistency assertion.
5. **P1 — Add AD chain-rule conversion:** Explicit `dr'/du = 2 * dr'/dτ` and `d²r'/du² = 4 * d²r'/dτ²` in physics loss and energy loss computations.
6. **P1 — Remove omega0 scheduling:** Delete `update_omega0()`, use fixed first_omega0=30, hidden_omega0=1.
7. **P2 — Resolve I_norm definition:** Adopt tanh-wrapped version; update CTL text.
8. **P2 — Ablate skip-path LayerNorm:** Train with/without to determine if author modification helps or hurts.

---

## Cross-Issue Interactions

Several issues interact non-trivially and must be resolved together, not independently:

| Interaction | Issues | Description | Severity |
|-------------|--------|-------------|----------|
| D + epsilon + COM | B-02, B-05, B-09 | Incorrect D corrupts scaled positions; COM transform order affects whether offsets survive; softening mismatch changes potential at close encounters | **Critical** |
| D + stage assignment | B-02, B-09 | Stage assignment thresholds are in scaled units. Wrong D + wrong epsilon = wrong stages for ~15% of systems near boundaries | **Critical** |
| Input vector dimension | B-03, B-04, M1, M2 | Dimension conflict blocks coding; missing orientation info means no absolute position prediction; all must be resolved together | **Critical** |
| SIREN init + omega0 schedule | B-01, B-10 | Init formula must be fixed BEFORE deciding on omega0 strategy. Removing scheduling simplifies the init fix | **Major** |
| COM + mass consistency | B-05, B-11 | COM transform requires consistent masses between IC and Brutus output | **Major** |
| Precision + softening | D4, B-09 | Float64 precision is sufficient with eps=1e-5. If epsilon reduced below 1e-10, arbitrary-precision parsing needed | **Minor** |

---

## Architecture Details: SIREN + SQR-SkipResNet

The target architecture (`SQRSkipResNetSIREN` in `basic_architecture.py`) combines three mechanisms:

1. **SIREN activations** — `φ(x) = sin(ω₀(Wx + b))`. First layer uses ω₀=30 for high-frequency injection; hidden layers use ω₀=1. The sine activation is periodic and infinitely differentiable, critical for computing physics residuals via automatic differentiation.

2. **Power-enhanced skip connections** — Odd layers fuse `f_sr(x) + LayerNorm(x)^p` where p=2. The element-wise square amplifies small features. LayerNorm precedes the power term (eps=1e-5, elementwise_affine=True in current code). **Caveat (M8):** The original SQR-SkipResNet paper (arXiv:2310.15690v2) does NOT use LayerNorm — this is an author modification. Whether it helps or hurts is unknown (D2, D3).

3. **DeepXDE compatibility** — The base `NN` class supports `apply_feature_transform` and `apply_output_transform` hooks, matching the DeepXDE pattern for input normalization and output constraint enforcement.

**Layer dimensions:** 14 → 256 × 12 hidden → 9. Total parameters: approximately 794,000.

**Known code issues in current implementation:**
- Hidden-layer init in `basic_architecture.py:37` multiplies by omega0 instead of dividing (B-01)
- `compute_derivatives` method computes derivatives w.r.t. the raw time coordinate, not the normalized τ — the chain-rule conversion factors (2×, 4×) described above are not applied
- Input vector comments in `basic_architecture.py` describe a different IC composition than what `data-processing-pipeline-full.py` produces

---

## LayerNorm Analysis

**Why LayerNorm on skip connections?** The physics residual involves 1/r³ terms. During close encounters (r → 0), gradient magnitudes spike by 3-4 orders of magnitude. These spikes propagate through skip connections — without normalization, the power term (element-wise square) amplifies already-large activations. LayerNorm normalizes the skip-path activations to zero mean and unit variance before the power operation, capping the maximum skip-contribution magnitude.

**affine=True vs affine=False (D3):** `affine=True` adds learnable scale (γ) and shift (β) parameters after normalization. For SIREN layers, which are carefully tuned for specific frequency spectra, learnable affine transforms on the skip path could interfere with the frequency-spreading design. **Default recommendation:** `affine=False` is safer. Ablate to confirm.

**Empirical ablation protocol (D2):**
1. Train a Stage 0 model with affine=True (baseline) and affine=False (comparison)
2. Monitor: max gradient norm per layer, activation histogram spread, training loss trajectory
3. Expected: if affine=True adds value, loss should converge faster; if not, both should reach similar final loss
4. If no benefit from affine=True, remove it to reduce parameter count and simplify the architecture

---

## Quantitative Impact of D Formula Error

Using D=4.64 (CTL's wrong formula) instead of D=6.694 (correct):

| Quantity | With D=4.64 | With D=6.694 | Relative Error |
|----------|-------------|--------------|----------------|
| Scaled positions r' = r/D | 44% too large | Correct | 44% overestimate |
| Scaled velocities v' = v/(D/T) | 44% too large | Correct | 44% overestimate |
| E_scaled (∝ v'², ∝ 1/r') | 44% too large (KE), 44% too small (PE) | Correct | Net ~75% error in total |
| L_norm (∝ r'×v') | 97% too large | Correct | 97% overestimate |
| Q (virial, ∝ v'²/r') | Net ~90% error | Correct | 90% error |

These errors propagate into every normalized IC vector component fed to the network and into every stage assignment threshold. Systems near curriculum boundaries get systematically wrong stage labels, destroying the curriculum's progressive-learning design.

---

## References

- [02-data-pipeline-and-validation.md](02-data-pipeline-and-validation.md) — Data pipeline produces the 13-component IC vector specified here; validation must apply the same COM transform; normalization formulas table lives canonically here.
- [03-curriculum-and-training-loop.md](03-curriculum-and-training-loop.md) — Training loop consumes the 14D input; omega0 scheduling interacts with stage initialization; D=6.694 drives stage thresholds; dual-epsilon strategy feeds into training loss epsilon_soft.
- [Canonical: PINN Architecture Plan](../../../markdown_conversions/PINN_architecture_plan.md) — Original architecture specification.
- [Canonical: CTL Instruction](../../../markdown_conversions/CTL-instruction-final.md) — Curriculum training framework.
- [Canonical: basic_architecture.py](../../../../pinn/basic_architecture.py) — Current SIREN implementation.
- [Canonical: data-processing-pipeline-full.py](../../../../pinn/data-processing-pipeline-full.py) — Current IC vector assembly.

---

## Considered Alternatives

### Trigonometric Encoding for Input Vector Orientation

**Source:** 2026-04-27 audit B-04, §5.3

The audit proposed encoding 3 angles (theta_L, phi_L, gamma_orb) as 5 trigonometric values: `[sin(theta_L), cos(theta_L), sin(phi_L), cos(phi_L), sin(gamma_orb)]`. This is a standard approach for representing spatial orientation in neural networks and has been used successfully in molecular dynamics and celestial mechanics contexts.

**Reason not chosen:** During chaotic scattering events — the exact regime targeted by curriculum stages 4-6 — the orbital plane can shift abruptly. When the angular momentum vector L_hat aligns with a coordinate pole (theta_L ≈ 0 or π), the azimuthal angle phi_L becomes undefined, and its trigonometric derivatives diverge. This injects undefined or massive gradients into the network's first layer, destabilizing the optimization precisely when the physics is most demanding.

The shape-invariants-plus-direction-cosines approach avoids this pathology entirely: shape invariants (I_1, I_2, I_3) are universally continuous and rotation-invariant, while direction cosines (cos θ, sin θ) of the invariant plane normal provide global orientation without singularities.

---

## Verbatim Reference Specification — Copied from 2026-04-27 Audit

The following section is copied verbatim from the comprehensive technical audit dated 2026-04-27. It serves as the authoritative 14-D input vector specification that downstream implementation phases should quote directly.

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

---

## Resolution Priority Queue (Implementation Order)

This queue orders all architecture/physics fixes by dependency, not just severity. Each item blocks the ones below it.

| Priority | Item | Blocks | Estimated Effort |
|----------|------|--------|------------------|
| **P0-1** | Fix D formula to 6.694; recompute scaled quantities | All stage assignments, all IC vectors | Pipeline re-run (~2 hrs compute) |
| **P0-2** | Fix SIREN init (divide by omega0) | Weight initialization validity | 1-line code change |
| **P0-3** | Adopt 14D input vector with shape invariants + dir cosines | First Linear layer allocation | ~50 lines of Python |
| **P0-4** | Implement unified COM transformer (COM-first, then scale) | All hierarchical trajectory targets | ~30 lines of Python |
| **P0-5** | Add AD chain-rule conversion factors to loss functions | Physics residual correctness | ~10 lines in loss.py |
| **P0-6** | Remove omega0 scheduling; use fixed values | Simplifies architecture | Delete ~15 lines |
| **P1-1** | Resolve I_norm definition (adopt tanh version) | IC vector finalization | 1-line change + doc update |
| **P1-2** | Resolve LayerNorm affine question (ablate) | Architecture finalization | 2 training runs to compare |
| **P2-1** | Re-attribute LayerNorm as author modification in docs | Citation accuracy | Doc edit only |

---

*End of 01-architecture-and-physics-foundations.md*

*This document synthesized from 7 source files archived in `archive/`. See `MIGRATION.md` for per-section provenance.*
