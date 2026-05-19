---
title: "CTL-PINN Final Resolution Roadmap"
version: "final-resolved-v3.0"
date: "2026-05-16"
status: "implementation-ready after P0 patch pass"
author: "Consolidated for Starlordpd233"
source_files:
  - ctl_instruction(6).md
  - pinn_architecture(6).md
  - ctl_pinn_resolution.md
  - ctl_pinn_resolution_2.md
supersedes:
  - ctl_pinn_resolution.md
  - ctl_pinn_resolution_2.md
project: "Curriculum-trained SQR-SkipResNet-SIREN PINN for the Newtonian three-body problem"
---

# CTL-PINN Final Resolution Roadmap

## 0. Scope, Decision Standard, and Supersession Rule

This file is the single final resolution document for the CTL-PINN three-body framework. It consolidates the two prior resolution files against the two controlling specifications:

- `ctl_instruction(6).md`: data parsing, preprocessing, invariant calculation, curriculum staging, training loop, optimizer handoff, validation, and reproducibility workflow.
- `pinn_architecture(6).md`: SQR-SkipResNet-SIREN architecture, SIREN initialization, LayerNorm skip path, data/physics/conservation losses, automatic differentiation, output contract, and inference contract.

The goal is not to replace the project with a different model class. The SQR-SkipResNet-SIREN backbone, curriculum-learning structure, BRUTUS-supervised data loss, AD-derived velocity/acceleration, and physics-residual training are preserved. The resolution edits only the parts that are internally inconsistent, mathematically underdetermined, physically mismatched, or likely to fail under scientific-ML implementation practice.

This document supersedes both prior resolution files. Where the two drafts disagree, the final rule is:

1. Use the stricter mathematical correction from `ctl_pinn_resolution_2.md` when it repairs a genuine physics or dimensional-consistency issue.
2. Use the cleaner implementation organization from `ctl_pinn_resolution.md` when it gives a better source-edit roadmap.
3. Override both drafts where they leave a deterministic-trajectory identifiability problem unresolved.

The main override is the input-vector semantics. The final framework keeps the **14D input width** required by the existing architecture, but the 13D IC vector is no longer an invariant-only descriptor. It is a **reconstructive, gauge-fixed initial-state encoding**. The original invariant set remains essential for curriculum staging, diagnostics, sampling, and metadata, but it is not sufficient as the sole conditioning vector for a deterministic trajectory model.

---

## 1. Executive Decision Summary

The framework is not training-ready as written. It becomes implementation-ready after a focused P0 patch pass.

The final P0 contract is:

1. **Raw-mass nondimensionalization is retained.** Keep
   $$
   D=(GT^2)^{1/3},\qquad V=D/T.
   $$
   All residual, Hamiltonian, COM, and invariant formulas use ordered raw masses $m_i$. Do not switch to $D=(GM_{\rm tot}T^2)^{1/3}$ unless every force, energy, and angular-momentum formula is rewritten in mass fractions.

2. **All trajectories use one frame and gauge.** Every IC and every BRUTUS snapshot is transformed by the same deterministic pipeline:
   $$
   \text{parse}\rightarrow\text{mass check}\rightarrow\text{COM recenter}\rightarrow\text{zero-momentum boost}\rightarrow\text{canonical ordering}\rightarrow\text{canonical rotation}\rightarrow\text{global scaling}.
   $$

3. **The network input remains 14D, but the IC semantics are changed.** The final input is
   $$
   x=[\tau,IC_{13}]\in\mathbb R^{14},\qquad \tau=2u-1,\qquad u=t/T.
   $$
   The final `IC13` is a gauge-fixed Jacobi-state encoding:
   $$
   IC_{13}=
   [m_1^{in},m_2^{in},m_3^{in},
   \rho_x^{in},\lambda_x^{in},\lambda_y^{in},
   \dot\rho_x^{in},\dot\rho_y^{in},\dot\rho_z^{in},
   \dot\lambda_x^{in},\dot\lambda_y^{in},\dot\lambda_z^{in},
   E^{in}].
   $$
   This is the smallest correction that preserves the 14D architecture while giving the conditional network enough information to identify the initial-value problem in a fixed gauge.

4. **The original invariant-only 13D IC vector is rejected as the final model input.** It may be kept only as metadata or as a later ablation. A deterministic trajectory model cannot be conditioned only on non-injective invariants and a few scalar angle summaries.

5. **The network output is 9D position only.** The raw head emits three 3D positions. A hard mass-weighted COM projection is applied before any loss:
   $$
   r_i'=\tilde r_i'-\frac{1}{M}\sum_{k=1}^3m_k\tilde r_k',\qquad M=\sum_i m_i.
   $$
   Velocities and accelerations are derived by AD after this projection. The network does not output velocities.

6. **Use $u=t/T$ as the autograd leaf.** The model wrapper maps $u$ to $\tau=2u-1$ internally. If a code path differentiates directly with respect to $\tau$, it must apply
   $$
   \frac{dr'}{du}=2\frac{dr'}{d\tau},\qquad
   \frac{d^2r'}{du^2}=4\frac{d^2r'}{d\tau^2}.
   $$
   Componentwise derivatives are required; `grad(output.sum(), tau)` is not acceptable for production physics residuals.

7. **Use one matched softened Hamiltonian.** Replace every inconsistent $(r+\varepsilon)^{-1}$ / $(r+\varepsilon)^{-3}$ pair with the Plummer-matched pair
   $$
   r_{ij,\epsilon}=\sqrt{\|r_j'-r_i'\|^2+\epsilon^2},
   $$
   $$
   a_i'=\sum_{j\ne i}m_j\frac{r_j'-r_i'}{r_{ij,\epsilon}^3},
   \qquad
   H_\epsilon=\frac12\sum_im_i\|v_i'\|^2-
   \sum_{i<j}\frac{m_im_j}{r_{ij,\epsilon}}.
   $$

8. **Replace scalar pseudo-ALM on physics MSE.** The default loss is stationary during each optimizer phase:
   $$
   \mathcal L_{total}=
   \mathcal L_{data}+\lambda_{IC}\mathcal L_{IC}
   +\lambda_{phys}\mathcal L_{phys}^{causal}
   +\lambda_E\mathcal L_E+\lambda_L\mathcal L_L.
   $$
   Do not apply ALM to an already-squared physics loss. Optional true ALM is allowed only as a later deterministic/full-batch ablation on scalar conservation constraints, never on the dense ODE residual and never with dual updates inside L-BFGS.

9. **SIREN frequency parameters are fixed inside a model instance.** Use `first_omega_0=30`, `hidden_omega_0=1`, and the standard SIREN initialization. Remove epochwise `omega0` scheduling.

10. **Training claims are bounded-horizon claims.** The framework is a bounded-horizon neural trajectory surrogate. For chaotic stages, evaluate and report performance in Lyapunov-time units; do not claim indefinite trajectory identity.

---

## 2. Final Decision Matrix

| Issue family | Final classification | Final decision | Priority |
|---|---|---|---|
| Characteristic length and mass convention | Spec Error if changed incorrectly | Keep $D=(GT^2)^{1/3}$ and raw masses. Replace mass-fraction input channels. | P0 |
| Input width | Spec Error | Freeze input width at 14: one time scalar plus `IC13`. | P0 |
| Input semantics | Spec Error beyond both drafts | Use reconstructive gauge-fixed Jacobi-state `IC13`, not invariant-only `IC13`. | P0 |
| COM and Galilean frame | Spec Error | Apply universal COM recentering and zero-momentum boost to all ICs and targets. | P0 |
| Rotation/permutation gauge | Spec Error | Canonical body ordering plus deterministic initial-geometry rotation. | P0 |
| Output contract | Spec Error in CTL prose | 9D positions only; no velocity output head. Add hard COM projection. | P0 |
| AD derivatives | Spec Error | Differentiate componentwise with respect to $u=t/T$ or apply exact $\tau\to u$ chain factors. | P0 |
| Softening | Spec Error | Use matched Plummer acceleration and potential. Keep raw $s_{min}$ unsoftened. | P0 |
| Loss balancing | Spec Error | Replace pseudo-ALM-on-MSE with stationary causal residual plus IC/conservation penalties. | P0 |
| Optional ALM | Code Risk | Only optional on scalar conservation constraints in deterministic/full-batch refinement; freeze in L-BFGS. | P1/P2 |
| SIREN initialization | Documentation Drift | Keep first-layer and hidden-layer SIREN formulas; remove scheduler and author doubts. | P1 |
| LayerNorm | Documentation Drift / empirical default | Keep skip-path LayerNorm; default `elementwise_affine=False`, ablate if needed. | P1 |
| $I_3$ normalization | Spec Error | $I_3\in[0,1/3]$, so use $I_3^{in}=6I_3-1$ for metadata features. | P1 |
| Invariant use | Scope correction | Use invariants for curriculum, sampling, diagnostics, and optional metadata, not as sole IC encoding. | P0/P1 |
| BRUTUS provenance | External dependency | Record tolerance, word length, cadence, and trustworthy horizon per trajectory. | P1 |
| Capacity limits | Empirical risk | Keep 12x256 initially; widen only after P0 validation plateaus. | P2 |

---

## 3. Governing Mathematical Convention

### 3.1 Raw-mass nondimensionalization

Let

$$
r_i=D r_i',\qquad t=Tu,\qquad v_i=\frac{D}{T}v_i',\qquad a_i=\frac{D}{T^2}a_i'.
$$

The physical Newtonian equation is

$$
\frac{d^2 r_i}{dt^2}=G\sum_{j\ne i}m_j\frac{r_j-r_i}{\|r_j-r_i\|^3}.
$$

Substitute the scalings:

$$
\frac{D}{T^2}\frac{d^2 r_i'}{du^2}=G\sum_{j\ne i}m_j
\frac{D(r_j'-r_i')}{D^3\|r_j'-r_i'\|^3}.
$$

Therefore

$$
\frac{d^2 r_i'}{du^2}=\frac{GT^2}{D^3}\sum_{j\ne i}m_j
\frac{r_j'-r_i'}{\|r_j'-r_i'\|^3}.
$$

To obtain the exact raw-mass scaled equation

$$
\frac{d^2 r_i'}{du^2}=\sum_{j\ne i}m_j
\frac{r_j'-r_i'}{\|r_j'-r_i'\|^3},
$$

we require

$$
\boxed{D^3=GT^2},\qquad \boxed{D=(GT^2)^{1/3}}.
$$

This is the convention already implicit in the controlling specs: raw masses appear in the CTL energy/angular-momentum formulas and in the PINN residual/Hamiltonian formulas. The mass-fraction alternative is valid but is not this framework.

### 3.2 Rejected alternative: $D=(GM_{tot}T^2)^{1/3}$

If instead

$$
D=(GM_{tot}T^2)^{1/3},
$$

then

$$
\frac{GT^2}{D^3}=\frac1{M_{tot}},
$$

and the scaled equation becomes

$$
\frac{d^2 r_i'}{du^2}=\sum_{j\ne i}\frac{m_j}{M_{tot}}
\frac{r_j'-r_i'}{\|r_j'-r_i'\|^3}.
$$

That equation uses mass fractions

$$
\mu_j=m_j/M_{tot}.
$$

Using $D=(GM_{tot}T^2)^{1/3}$ while leaving raw masses in the residual would insert a false factor of $M_{tot}$. Therefore it is rejected for this project unless the full framework is deliberately rewritten in mass fractions.

### 3.3 Time spaces

The final implementation distinguishes three spaces:

$$
(t,r,v)_{raw}
\rightarrow
(u,r',v')_{physics}
\rightarrow
(\tau,IC_{13})_{network},
$$

with

$$
u=t/T,\qquad \tau=2u-1.
$$

The clean implementation is:

```python
# u is the autograd leaf.
u = torch.as_tensor(u, dtype=torch.float64).requires_grad_(True)
tau = 2.0 * u - 1.0
x = torch.cat([tau, ic13], dim=-1)
r_proj = model_projected(x, raw_masses)
```

Then

$$
v_\theta'=\frac{dr_\theta'}{du},\qquad
 a_\theta'=\frac{d^2r_\theta'}{du^2}.
$$

If implementation differentiates with respect to $\tau$ directly, then

$$
v_\theta'=2\frac{dr_\theta'}{d\tau},\qquad
 a_\theta'=4\frac{d^2r_\theta'}{d\tau^2}.
$$

---

## 4. Data Preprocessing, Frame, Gauge, and Stored Metadata

### 4.1 Parser contract

For every IC/BRUTUS pair:

1. Parse masses, positions, and velocities in float64.
2. Accept IC files in either one-line flattened format or three-line body format.
3. Parse BRUTUS outputs as time blocks: header `(t,N,t_cpu)` followed by three body rows.
4. Verify body count `N=3` for every block.
5. Verify mass invariance through the trajectory before any training use:

$$
\max_{t,i}|m_i(t)-m_i(0)| < 10^{-15}
$$

in float64 parse space. If this fails, reject the trajectory or quarantine it for parser debugging.

### 4.2 Universal COM and zero-momentum transform

Apply this to **all** datasets, hierarchical and quasi-random, regardless of whether they are believed to already be in COM frame.

For each trajectory, define

$$
M=\sum_i m_i,
$$

$$
R_{COM}(0)=\frac1M\sum_i m_i r_i(0),\qquad
V_{COM}=\frac1M\sum_i m_i v_i(0).
$$

For every snapshot time $t_n$:

$$
\bar r_i(t_n)=r_i(t_n)-R_{COM}(0)-V_{COM}t_n,
$$

$$
\bar v_i(t_n)=v_i(t_n)-V_{COM}.
$$

For the initial condition this gives

$$
\sum_i m_i\bar r_i(0)=0,
\qquad
\sum_i m_i\bar v_i(0)=0.
$$

For an isolated Newtonian system the transformed trajectory remains a valid solution in the COM frame.

### 4.3 Canonical ordering

After COM/boost correction, sort body labels deterministically:

1. descending raw mass $m_i$;
2. tie-break by descending $\|\bar r_i(0)\|$;
3. tie-break by descending $\|\bar v_i(0)\|$;
4. final tie-break by original file order.

The same permutation is applied to:

- masses;
- every initial-condition quantity;
- every BRUTUS target snapshot;
- every residual, Hamiltonian, COM projection, and evaluation output.

This removes permutation ambiguity without requiring a permutation-equivariant architecture.

### 4.4 Canonical rotation gauge

After canonical ordering, define the Jacobi position vectors

$$
\rho = \bar r_2(0)-\bar r_1(0),
$$

$$
\lambda = \bar r_3(0)-\frac{m_1\bar r_1(0)+m_2\bar r_2(0)}{m_1+m_2}.
$$

For non-collision ICs with $\|\rho\|>\varepsilon_\rho$, set

$$
e_x=\rho/\|\rho\|.
$$

Remove the $e_x$ component from $\lambda$:

$$
\lambda_\perp=\lambda-(\lambda\cdot e_x)e_x.
$$

If $\|\lambda_\perp\|>\varepsilon_\lambda$, set

$$
e_y=\lambda_\perp/\|\lambda_\perp\|.
$$

If the initial geometry is collinear, use the first nonzero projected vector from the ordered list

$$
\dot\rho,\quad \dot\lambda,\quad \bar v_1(0),\quad \bar v_2(0),\quad \bar v_3(0),
$$

where

$$
\dot\rho=\bar v_2(0)-\bar v_1(0),
$$

$$
\dot\lambda=\bar v_3(0)-\frac{m_1\bar v_1(0)+m_2\bar v_2(0)}{m_1+m_2}.
$$

Project the chosen vector perpendicular to $e_x$ and normalize it. If all candidates are degenerate, choose the fixed coordinate basis vector least aligned with $e_x$ and project it perpendicular to $e_x$.

Set

$$
e_z=e_x\times e_y,
$$

and define the rotation matrix

$$
R_0=
\begin{bmatrix}
e_x^\top\\
e_y^\top\\
e_z^\top
\end{bmatrix}.
$$

Apply the same rotation to every snapshot:

$$
r_i^{g}(t_n)=R_0\bar r_i(t_n),\qquad
v_i^{g}(t_n)=R_0\bar v_i(t_n).
$$

The canonical gauge ensures that, at $t=0$,

$$
\rho^g=(\rho_x,0,0),\qquad
\lambda^g=(\lambda_x,\lambda_y,0),\qquad \lambda_y\ge 0
$$

up to numerical tolerance.

### 4.5 Scaling order

After frame and gauge transforms, scale by the global constants:

$$
r_i'=r_i^g/D,
\qquad
v_i'=v_i^g/V,
\qquad V=D/T.
$$

Although global scaling commutes algebraically with COM subtraction, the documented order above is required for auditability and for avoiding mixed-frame intermediate files.

### 4.6 Stored metadata per trajectory

Each trajectory record must store:

```text
traj_id
raw_file_paths
ordered_raw_masses: (3,)
permutation: (3,)
R0: (3,3)
R_COM0: (3,)
V_COM: (3,)
D, T, V
r0_prime_ordered_gauge: (3,3)
v0_prime_ordered_gauge: (3,3)
times_raw: (Nt,)
u: (Nt,)
tau: (Nt,)
r_true_prime_ordered_gauge: (Nt,3,3)
v_true_prime_ordered_gauge: (Nt,3,3)  # optional but recommended
IC13: (13,)
invariants: E, Q, s_min, L_vec, L_norm, I_norm_raw, I1, I2, I3, tau_L
brutus_tolerance, word_length, dt_out, trustworthy_horizon
```

Raw masses are always available separately from the network-facing mass channels.

---

## 5. Final Input Contract

### 5.1 Why the invariant-only IC vector is rejected

The previous drafts correctly fix several input-width errors, but their proposed invariant-heavy 13D vector still does not fully identify the initial-value problem. For a deterministic direct-trajectory PINN,

$$
r_\theta(t,IC)
$$

must receive enough information to distinguish two different initial states. Otherwise two different BRUTUS trajectories may share one input vector but require different outputs, producing an irreducible supervised-learning contradiction.

The invariant-only vector

```text
[masses, E, L_norm, Q, s_min, I_norm, I1, I2, I3, c1, c2]
```

is useful as metadata but not a mathematically safe final conditioning state. It compresses away velocity-direction information and can admit multiple gauge-fixed initial states with the same scalar descriptors. The corrected spec therefore preserves the architecture's 14D width but replaces the IC semantics with a reconstructive gauge-fixed state.

### 5.2 Gauge-fixed Jacobi state

After preprocessing, define scaled Jacobi state variables:

$$
\rho'=r_2'(0)-r_1'(0),
$$

$$
\lambda'=r_3'(0)-\frac{m_1r_1'(0)+m_2r_2'(0)}{m_1+m_2},
$$

$$
\dot\rho'=v_2'(0)-v_1'(0),
$$

$$
\dot\lambda'=v_3'(0)-\frac{m_1v_1'(0)+m_2v_2'(0)}{m_1+m_2}.
$$

By construction of the rotation gauge,

$$
\rho'=(\rho_x,0,0),\qquad
\lambda'=(\lambda_x,\lambda_y,0),\qquad \lambda_y\ge0.
$$

The velocities remain fully 3D:

$$
\dot\rho'=(\dot\rho_x,\dot\rho_y,\dot\rho_z),
$$

$$
\dot\lambda'=(\dot\lambda_x,\dot\lambda_y,\dot\lambda_z).
$$

The reconstructive state has:

- 3 ordered masses;
- 3 independent position-shape/scale coordinates;
- 6 independent velocity coordinates.

That gives 12 IC scalars. The 13th scalar is $E^{in}$, retained as redundant but useful optimization/curriculum information. This preserves the 14D first-layer contract without discarding the initial-value problem.

### 5.3 Final `IC13` formula

The final network-facing IC vector is

$$
\boxed{
IC_{13}=
[m_1^{in},m_2^{in},m_3^{in},
\rho_x^{in},\lambda_x^{in},\lambda_y^{in},
\dot\rho_x^{in},\dot\rho_y^{in},\dot\rho_z^{in},
\dot\lambda_x^{in},\dot\lambda_y^{in},\dot\lambda_z^{in},
E^{in}]
}.
$$

The full model input is

$$
\boxed{x=[\tau,IC_{13}]\in\mathbb R^{14}}.
$$

### 5.4 Normalization

Mass channels must preserve absolute mass scale. Do not use mass fractions as the final input representation under raw-mass dynamics.

For each ordered mass channel, compute dataset statistics after canonical ordering:

$$
\mu_{m,i}=\operatorname{mean}_{traj}(m_i),\qquad
\sigma_{m,i}=\operatorname{std}_{traj}(m_i),
$$

and encode

$$
\boxed{m_i^{in}=\tanh\left(\frac{m_i-\mu_{m,i}}{\sigma_{m,i}+10^{-8}}\right)}.
$$

For each Jacobi coordinate channel $z$ in

$$
z\in\{\rho_x,\lambda_x,\lambda_y,
\dot\rho_x,\dot\rho_y,\dot\rho_z,
\dot\lambda_x,\dot\lambda_y,\dot\lambda_z\},
$$

compute dataset statistics after the full frame/gauge/scale pipeline:

$$
z^{in}=\tanh\left(\frac{z-\mu_z}{\sigma_z+10^{-8}}\right).
$$

For energy,

$$
E^{in}=\tanh(E/E_{scale}),
\qquad
E_{scale}=|\operatorname{median}_{traj}(E)|+10^{-8}.
$$

Do not clip before the `tanh` except for NaN/Inf rejection. Hard clipping before a monotone map can destroy injectivity in extreme cases. Dataset statistics should report saturation rates, for example the fraction of channels with $|z^{in}|>0.99$.

### 5.5 Invariants remain required metadata

The following quantities remain mandatory, but they are not the final network IC vector:

```text
E, Q, s_min, L_vec, L_norm, I_norm_raw, I1, I2, I3, tau_L
```

They are used for:

- curriculum stage assignment;
- lookahead/replay sampling;
- diagnostics and validation;
- loss scaling and reporting;
- possible auxiliary-head or widened-input ablations.

### 5.6 Corrected invariant normalizations for metadata

For sorted side lengths

$$
d_{short}\le d_{mid}\le d_{long},
$$

keep

$$
I_1=d_{short}/d_{long},\qquad
I_2=d_{mid}/d_{long},
$$

and

$$
I_3=\frac{d_{short}+d_{mid}-d_{long}}{d_{short}+d_{mid}+d_{long}}.
$$

By the triangle inequality,

$$
I_3\in[0,1/3],
$$

so the correct metadata normalization is

$$
I_3^{in}=6I_3-1.
$$

For inertia, distinguish the raw descriptor from the bounded metadata channel:

```python
I_norm_raw = trace(I_tensor) / (M_total * r_char**2 + eps)
I_norm_in = tanh(I_norm_raw)
```

For angular momentum metadata,

$$
L^{in}=2\operatorname{clip}(L/L_{max},0,1)-1.
$$

Raw $L_{vec}$ must still be stored for angular-momentum conservation diagnostics.

---

## 6. Final Architecture Contract

### 6.1 Backbone

Keep the architecture class:

```text
SQR-SkipResNet-SIREN
```

Default hyperparameters:

| Hyperparameter | Final value |
|---|---:|
| Input width | 14 |
| Output head width | 9 |
| Hidden depth | 12 hidden layers |
| Hidden width | 256 |
| Activation | sine / SIREN |
| first_omega_0 | 30 |
| hidden_omega_0 | 1 |
| Skip cadence | alternating SQR-SkipResNet blocks |
| Power term | 2 |
| LayerNorm | skip path only on power branch |
| LayerNorm affine | `False` by default |
| Output activation | none / linear |

### 6.2 SIREN initialization

Use exactly one SIREN initialization statement.

First layer:

$$
W^{(0)}\sim U\left[-\frac1{n_{in}},\frac1{n_{in}}\right].
$$

Hidden layers:

$$
W^{(\ell\ge1)}\sim U\left[-\frac{\sqrt{6/n_{in}}}{\omega_0^{(\ell)}},
\frac{\sqrt{6/n_{in}}}{\omega_0^{(\ell)}}\right],
\qquad \omega_0^{(\ell\ge1)}=1.
$$

Remove all epochwise or optimizer-step `omega0` scheduling. If `omega0` is retuned, it is a stage-boundary ablation with fresh initialization, not a within-run mutation.

### 6.3 Output projection

Let the raw network head produce

$$
\tilde r_\theta'\in\mathbb R^{3\times3}.
$$

Before data loss, physics residual, IC loss, conservation loss, or metrics, project to the mass-weighted COM frame:

$$
R_\theta'=\frac1M\sum_{i=1}^3m_i\tilde r_{\theta,i}',
$$

$$
r_{\theta,i}'=\tilde r_{\theta,i}'-R_\theta'.
$$

This gives

$$
\sum_i m_i r_{\theta,i}'=0
$$

by construction. Since masses are constant metadata, AD through the projection also gives

$$
\sum_i m_i v_{\theta,i}'=0,
\qquad
\sum_i m_i a_{\theta,i}'=0
$$

up to floating-point error.

### 6.4 AD derivative implementation

Compute derivatives componentwise after COM projection.

Acceptable implementations:

- `torch.func.jacrev` + `vmap`;
- explicit loop over the 9 projected output components;
- equivalent full-Jacobian/Hessian method.

Unacceptable implementation:

```python
torch.autograd.grad(r.sum(), u, create_graph=True)
```

as a surrogate for all componentwise derivatives. That expression gives a vector-Jacobian product against an all-ones covector, not the nine derivatives required by the residual and Hamiltonian.

---

## 7. Final Dynamics and Hamiltonian Contract

### 7.1 Matched Plummer pair

Use a matched force/potential pair.

For training:

$$
\epsilon_{train}=10^{-5}
$$

unless ablated. Define

$$
r_{ij,\epsilon}=\sqrt{\|r_j'-r_i'\|^2+\epsilon_{train}^2}.
$$

Acceleration:

$$
A_i(r')=\sum_{j\ne i}m_j\frac{r_j'-r_i'}{r_{ij,\epsilon}^{3}}.
$$

Hamiltonian:

$$
H_{\epsilon}(r',v')=\frac12\sum_{i=1}^3m_i\|v_i'\|^2
-\sum_{1\le i<j\le3}\frac{m_im_j}{r_{ij,\epsilon}}.
$$

The acceleration is the mass-normalized force generated by this Hamiltonian potential. Do not mix

$$
(\|r\|+\epsilon)^{-3}
$$

with

$$
(\|r\|+\epsilon)^{-1}.
$$

Those are not a matched gradient pair.

### 7.2 Static invariant softening

For static invariant computation, use

$$
\epsilon_{inv}=10^{-10}
$$

in the energy potential only:

$$
V_{\epsilon_{inv}}=-\sum_{i<j}\frac{m_im_j}{\sqrt{\|r_i'-r_j'\|^2+\epsilon_{inv}^2}}.
$$

Do not soften the geometric quantity $s_{min}$:

$$
s_{min}=\min_{i<j}\|r_i'-r_j'\|.
$$

Softening never enters curriculum collision gates.

### 7.3 Physics residual

For temporally ordered collocation points $u_n$, define

$$
\mathcal R_i(u_n;\theta)=
\frac{d^2r_{\theta,i}'(u_n)}{du^2}-A_i(r_\theta'(u_n)).
$$

The pointwise residual magnitude is

$$
\bar R_n=\frac13\sum_{i=1}^3\|\mathcal R_i(u_n;\theta)\|_2^2.
$$

The residual is evaluated in the canonical COM frame with ordered raw masses.

---

## 8. Final Loss and Optimization Contract

### 8.1 Total loss

The default loss is

$$
\boxed{
\mathcal L_{total}=\mathcal L_{data}
+\lambda_{IC}\mathcal L_{IC}
+\lambda_{phys}\mathcal L_{phys}^{causal}
+\lambda_E\mathcal L_E
+\lambda_L\mathcal L_L
}.
$$

This is a stationary objective during each optimizer phase. Hyperparameters may be scheduled between epochs or stages, but no dual variables or penalty coefficients are updated inside an L-BFGS line search.

### 8.2 Data loss

Use scaled, projected, gauge-frame positions:

$$
\mathcal L_{data}=\frac1{N_{data}}
\sum_k \operatorname{Huber}_{\delta_r}
\left(r_\theta'(u_k,IC_k)-r_{true}'(u_k,IC_k)\right).
$$

`L1` remains acceptable, but Huber is the default because it is less brittle than pure L2 while smoother than pure L1.

Recommended default:

$$
\delta_r=1.
$$

### 8.3 Initial-condition anchor loss

The ODE problem must be anchored at $u=0$ for every trajectory sampled in a batch.

Position anchor:

$$
\mathcal L_{IC,r}=\frac13\sum_{i=1}^3\|r_{\theta,i}'(0)-r_i'(0)\|_2^2.
$$

Velocity anchor:

$$
\mathcal L_{IC,v}=\frac13\sum_{i=1}^3\|v_{\theta,i}'(0)-v_i'(0)\|_2^2.
$$

Total anchor:

$$
\mathcal L_{IC}=\mathcal L_{IC,r}+\beta_v\mathcal L_{IC,v},
\qquad \beta_v=1.
$$

This term is mandatory even if $t=0$ is present in BRUTUS snapshots, because random minibatch sampling does not guarantee consistent enforcement of the initial-value condition.

### 8.4 Causal physics residual

For sorted collocation times

$$
u_1<u_2<\cdots<u_{N_t},
$$

use

$$
w_1=1,
$$

$$
w_n=\exp\left(-\eta_c\sum_{m=1}^{n-1}\operatorname{stopgrad}(\bar R_m)\right),
\qquad n>1.
$$

Then

$$
\mathcal L_{phys}^{causal}=\frac1{N_t}\sum_{n=1}^{N_t}w_n\bar R_n.
$$

Use `stopgrad` in the weights by default to prevent the weight mechanism from becoming an unintended adversarial term.

Recommended default:

$$
\eta_c=1,
$$

with clipping of the exponent to avoid underflow.

### 8.5 Energy conservation penalty

Using the matched Hamiltonian,

$$
\Delta H_n=\frac{H_\epsilon(r_\theta'(u_n),v_\theta'(u_n))-H_\epsilon(r_0',v_0')}{|H_\epsilon(r_0',v_0')|+\epsilon_H}.
$$

Then

$$
\mathcal L_E=\frac1{N_t}\sum_{n=1}^{N_t}\operatorname{Huber}_{1.0}(\Delta H_n).
$$

### 8.6 Angular-momentum conservation penalty

Define

$$
L_\theta'(u_n)=\sum_{i=1}^3m_i\,r_{\theta,i}'(u_n)\times v_{\theta,i}'(u_n),
$$

$$
L_0'=\sum_{i=1}^3m_i\,r_i'(0)\times v_i'(0).
$$

Normalize componentwise by

$$
\epsilon_L=10^{-8},\qquad
L_{scale}=\|L_0'\|+\epsilon_L.
$$

Then

$$
\mathcal L_L=\frac1{3N_t}\sum_{n=1}^{N_t}\sum_{\alpha\in\{x,y,z\}}
\operatorname{Huber}_{1.0}
\left(\frac{L_{\theta,\alpha}'(u_n)-L_{0,\alpha}'}{L_{scale}}\right).
$$

### 8.7 Weight schedules

Warm up physics and conservation terms inside each curriculum stage:

$$
I_{warm}=\min(2000,0.1N_{Adam,k}),
$$

$$
\lambda_{phys}(k,i)=\lambda_{phys}^{max}(k)\min\left(1,\frac{i}{I_{warm}}\right).
$$

Default:

$$
\lambda_{phys}^{max}(k)=1.
$$

For conservation:

$$
\lambda_E^{max}(k)=\lambda_L^{max}(k)=
\begin{cases}
0, & k\in\{0,1\},\\
10^{k-4}, & k\in\{2,3,4\},\\
1, & k\in\{5,6\}.
\end{cases}
$$

and

$$
\lambda_E(k,i)=\lambda_E^{max}(k)\min\left(1,\frac{i}{I_{warm}}\right),
$$

$$
\lambda_L(k,i)=\lambda_L^{max}(k)\min\left(1,\frac{i}{I_{warm}}\right).
$$

Keep

$$
\lambda_{IC}=1
$$

by default, with an ablation range $[0.1,10]$ if IC anchoring dominates early training.

### 8.8 ALM policy

The current scalar pseudo-ALM objective is rejected:

$$
\mathcal L_{data}+\lambda_p\mathcal L_{physics}+\frac{\mu_p}{2}\mathcal L_{physics}^2.
$$

Reason: $\mathcal L_{physics}$ is already a nonnegative MSE. Squaring it produces a quartic residual term and does not represent a standard equality-constrained augmented Lagrangian.

Default final framework: **no ALM dual updates**.

Optional later ablation: ALM may be applied only to scalar conservation constraints on deterministic/full-batch refinement sets:

$$
c_E=\operatorname{RMS}_n(\Delta H_n),
$$

$$
c_{L,\alpha}=\operatorname{RMS}_n\left(\frac{L_{\theta,\alpha}'(u_n)-L_{0,\alpha}'}{L_{scale}}\right).
$$

If used:

- never apply ALM to the dense ODE residual;
- never update dual variables during L-BFGS;
- update dual variables only between Adam epochs or between deterministic refinement passes;
- log constraint values before and after each update;
- treat this as a P2 ablation, not the default training contract.

---

## 9. Curriculum and Data Contract

### 9.1 Stage criteria remain metadata-driven

Curriculum stage assignment still uses the invariant metadata:

```text
E, Q, s_min, L_norm, tau_L
```

with $I_{norm}$ and shape invariants available for diagnostics or secondary filters.

After P0 preprocessing changes, all invariant distributions must be recomputed. Do not reuse old thresholds without regenerating the post-gauge/post-scaling statistics.

### 9.2 Sampling policy

Stages 0-2:

- uniform time collocation is acceptable;
- include IC anchor at every batch;
- use replay from all previous stages.

Stages 3-6:

- use 50% uniform time sampling;
- use 50% proximity-biased or acceleration-biased sampling;
- keep lookahead sampling small, e.g. 5%;
- always include replay to prevent forgetting.

### 9.3 BRUTUS provenance

Every trajectory used for training must carry:

```text
BRUTUS tolerance
word length
dt_out
raw IC file hash
raw BRUTUS output hash
postprocessing version
trustworthy_horizon
```

For chaotic stages, evaluation claims are valid only up to

$$
\min(\text{stored trustworthy horizon},\;5\tau_L)
$$

unless a stronger reference-integration audit is supplied.

### 9.4 Bounded-horizon claim

The model is not specified as an indefinite replacement for BRUTUS. It is a neural trajectory surrogate with physically constrained short-to-medium horizon behavior. The primary trajectory-identity target is approximately

$$
1\text{--}3\,\tau_L
$$

for chaotic systems, together with bounded conservation drift and plausible statistical behavior beyond exact trajectory identity.

---

## 10. Exact Source Patch Requirements

### 10.1 Patch `ctl_instruction(6).md`: scaling convention

Replace the current scaling prose with:

```markdown
This framework uses raw masses in the scaled Newton equations. The global
scales are

T = t_max,
D = (G*T**2)**(1/3),
V = D/T.

The alternative D=(G*M_total*T**2)**(1/3) belongs to a mass-fraction
convention and is not used here. All residual, Hamiltonian, angular-momentum,
COM, and invariant calculations use ordered raw masses m_i.
```

### 10.2 Patch `ctl_instruction(6).md`: unified preprocessing

Replace Step 2.5 with a unified frame/gauge step:

```markdown
Apply one deterministic transform to every IC and every Brutus snapshot:
raw parse -> mass invariance check -> COM recenter -> zero-momentum boost ->
canonical ordering -> canonical rotation -> scaling.

After preprocessing, assert
||sum_i m_i*r_i'|| < 1e-12
and
||sum_i m_i*v_i'|| < 1e-12.
```

### 10.3 Patch `ctl_instruction(6).md`: input vector section

Replace the invariant-only Step 4 assembly with:

```markdown
The model input is x=[tau,IC13] in R^14.

tau = 2*(t/T)-1.

IC13 is the gauge-fixed Jacobi-state vector:
[m1_in,m2_in,m3_in,
 rho_x_in,lambda_x_in,lambda_y_in,
 drho_x_in,drho_y_in,drho_z_in,
 dlambda_x_in,dlambda_y_in,dlambda_z_in,
 E_in].

The former invariant vector is retained as metadata for curriculum staging and
diagnostics. It is not the final model-conditioning vector.
```

### 10.4 Patch `ctl_instruction(6).md`: remove false injectivity proof

Delete any statement equivalent to:

```text
13 constraints for an 8-dimensional reduced phase space ensure over-determination and uniqueness.
```

Replace with:

```markdown
The final IC13 is a redundant but reconstructive fixed-gauge initial-state
encoding. It is not justified by constraint counting. Its validity comes from
COM removal, zero-momentum boost, canonical ordering, canonical rotation, and
retention of the independent Jacobi position/velocity degrees of freedom.
```

### 10.5 Patch `pinn_architecture(6).md`: input/output contract

Replace the input/output rows with:

```markdown
Input: x=[tau,IC13] in R^14, where tau is normalized time and IC13 is the
reconstructive gauge-fixed Jacobi-state vector defined in the CTL spec.

Output: the raw head emits 9 unconstrained position coordinates. A hard
mass-weighted COM projection is applied before every loss and metric. The
network does not output velocities or accelerations.
```

### 10.6 Patch `pinn_architecture(6).md`: AD contract

Replace generic AD prose with:

```markdown
Training uses u=t/T as the autograd leaf. The model wrapper computes tau=2u-1.
Velocities and accelerations are componentwise derivatives of the projected
positions with respect to u. If differentiating with respect to tau directly,
use v'=2*dr'/dtau and a'=4*d2r'/dtau2.
```

### 10.7 Patch `pinn_architecture(6).md`: residual and Hamiltonian

Replace the residual and energy formulas with the matched Plummer pair:

```markdown
r_safe_ij = sqrt(||r_j' - r_i'||^2 + epsilon_train^2)

a_i' = sum_{j != i} m_j * (r_j' - r_i') / r_safe_ij^3

H = 0.5*sum_i m_i*||v_i'||^2 - sum_{i<j} m_i*m_j/r_safe_ij
```

### 10.8 Patch both files: loss

Replace scalar pseudo-ALM with:

```markdown
L_total = L_data + lambda_IC*L_IC + lambda_phys*L_phys_causal
          + lambda_E*L_E + lambda_L*L_L.

No ALM is applied to L_physics. Optional ALM may be tested only as a P2
full-batch conservation-constraint ablation, with no dual updates during L-BFGS.
```

### 10.9 Patch `pinn_architecture(6).md`: SIREN frequency

Delete the epochwise `update_omega0()` scheduler. Replace with:

```markdown
first_omega_0 = 30
hidden_omega_0 = 1

These frequency parameters are fixed for a given instantiated model. Retuning
omega0 is a stage-boundary ablation with fresh initialization, not an in-stage
schedule.
```

### 10.10 Patch both files: 3D disclosure

Add:

```markdown
All state vectors, residuals, losses, and outputs are fully 3D. Any cited
planar literature is motivational only and does not define this framework's
state contract.
```

---

## 11. Dependency-Ordered Implementation Roadmap

```mermaid
flowchart TD
    A[Raw parser and mass-invariance assertions] --> B[Universal COM and zero-momentum transform]
    B --> C[Canonical ordering and rotation gauge]
    C --> D[Global scaling with raw-mass D=(G*T^2)^(1/3)]
    D --> E[Build reconstructive Jacobi IC13]
    E --> F[Update dataset serializers and batch builders]
    F --> G[Set model n_in=14 and output head=9]
    G --> H[Add mass-weighted COM projection]
    H --> I[Implement componentwise AD with u=t/T leaf]
    I --> J[Replace force and energy with matched Plummer formulas]
    J --> K[Add IC anchor, causal residual, and conservation penalties]
    K --> L[Remove pseudo-ALM and omega0 scheduler]
    L --> M[Recompute curriculum statistics]
    M --> N[Run P0 validation suite]
    N --> O[Begin staged training]
```

P0 tasks must be completed before any serious training run.

P1 tasks clean documentation, metadata, and ablation hooks.

P2 tasks test capacity, alternative input features, ALM ablations, and wider networks.

---

## 12. Validation Test Suite

### 12.1 Tensor shape tests

```python
assert x.shape[-1] == 14
assert ic13.shape[-1] == 13
assert r_raw.shape[-1] == 9
assert r_proj.reshape(-1, 3, 3).shape[-2:] == (3, 3)
```

### 12.2 Raw-mass scaling test

Numerically verify that

$$
GT^2/D^3=1
$$

under the retained convention:

```python
coef = G * T**2 / D**3
assert abs(coef - 1.0) < 1e-12
```

If a future branch uses $D=(GM_{tot}T^2)^{1/3}$, assert that the residual uses $m_j/M_{tot}$ instead of $m_j$.

### 12.3 COM projection test

For random raw output and random positive masses:

```python
r_proj = project_com(r_raw, masses)
com = (masses[:, None] * r_proj).sum(axis=0) / masses.sum()
assert np.linalg.norm(com) < 1e-12
```

### 12.4 Gauge transform tests

Verify:

```python
assert np.allclose(R0 @ R0.T, np.eye(3), atol=1e-12)
assert abs(np.linalg.det(R0) - 1.0) < 1e-12
assert abs(rho_g[1]) < 1e-12
assert abs(rho_g[2]) < 1e-12
assert abs(lambda_g[2]) < 1e-12
assert lambda_g[1] >= -1e-12
```

### 12.5 IC reconstructivity test

Before bounded normalization, reconstruct the canonical initial state from masses, Jacobi positions, and Jacobi velocities. Assert equality to the stored gauge-frame initial state.

```python
r_rec, v_rec = reconstruct_from_jacobi(m, rho, lam, drho, dlam)
assert np.max(np.abs(r_rec - r0_prime)) < 1e-12
assert np.max(np.abs(v_rec - v0_prime)) < 1e-12
```

### 12.6 AD chain-rule test

For a known analytic test function, compare derivatives computed through `u` with derivatives computed through `tau` and chain factors.

```python
# r(tau) = tau**3. tau = 2u-1.
# dr/du = 6*tau**2.
# d2r/du2 = 24*tau.
```

Assert both implementations agree to numerical tolerance.

### 12.7 Force/potential consistency test

For random positions, verify the acceleration equals the negative mass-normalized gradient of the matched potential:

$$
a_i=-\frac1{m_i}\frac{\partial V}{\partial r_i}.
$$

Use finite differences or autograd on the potential.

### 12.8 Initial-condition anchor test

Before training, construct a tiny overfit batch with one trajectory and force inclusion of $u=0$. Confirm that $\mathcal L_{IC}$ can decrease and that AD-derived $v'(0)$ has the correct shape and scale.

### 12.9 Permutation and rotation invariance test

Take a raw IC, then generate a permuted and globally rotated copy. After preprocessing, the two records should produce the same canonical masses, same `IC13`, and same transformed target trajectory up to tolerance.

### 12.10 Loss stationarity test

During an L-BFGS closure, assert that no variable outside the model parameters changes:

```python
before = snapshot_loss_hyperparameters()
loss = closure()
after = snapshot_loss_hyperparameters()
assert before == after
```

This prevents silent ALM-style dual updates inside L-BFGS.

### 12.11 Two-body and symmetry sanity checks

- For $m_3\to0$, recover stable two-body-like behavior and finite conservation drift.
- For equal-mass symmetric configurations, verify that canonical ordering tie-breaks are deterministic and that tiny perturbations produce continuous IC changes except at explicitly documented symmetry boundaries.

---

## 13. Empirical Capacity and Ablation Triggers

Do not redesign the architecture before P0 fixes. The current 12-layer, width-256 SQR-SkipResNet-SIREN is a reasonable first corrected baseline.

After P0 validation:

1. If Stage 2 validation Huber/MAE on scaled COM-frame positions plateaus above $10^{-3}$ after 20,000 Adam steps, widen to 384 or 512 before advancing to chaotic stages.
2. If Stage 3 or higher underfits while conservation and residual losses remain high, run a stage-boundary `first_omega_0` sweep in `{20,30,40}` with fresh initialization. Do not schedule `omega0` inside a run.
3. If close-encounter residuals dominate, ablate $\epsilon_{train}\in\{10^{-6},10^{-5},10^{-4}\}$ and proximity-biased collocation ratios.
4. If the Jacobi-state IC13 outperforms the invariant-only IC13, retire the invariant-only vector permanently. If the invariant-only vector is kept for a paper comparison, label it as a non-reconstructive ablation.
5. If conservation drift remains high after matched Hamiltonian and AD fixes, increase $\lambda_E,\lambda_L$ mildly before trying optional ALM.

---

## 14. Final Open-Decision Closure

### D-01A: Input-vector composition

Closed.

Use:

```text
[tau,
 m1_in, m2_in, m3_in,
 rho_x_in, lambda_x_in, lambda_y_in,
 drho_x_in, drho_y_in, drho_z_in,
 dlambda_x_in, dlambda_y_in, dlambda_z_in,
 E_in]
```

Do not use the invariant-only IC vector as the final deterministic trajectory conditioning input.

### D-01B: Loss-balancing methodology

Closed.

Use:

```text
L_total = L_data + lambda_IC*L_IC + lambda_phys*L_phys_causal
          + lambda_E*L_E + lambda_L*L_L
```

No scalar ALM on physics MSE. Optional ALM is a later full-batch conservation-only ablation.

### D-02: `I_norm` definition

Closed.

Use:

```python
I_norm_raw = trace(I_tensor) / (M_total * r_char**2 + eps)
I_norm_in = tanh(I_norm_raw)
```

as metadata only unless a widened-input ablation is run.

### D-03: Mass normalization

Closed.

Use raw ordered mass statistics:

```python
m_i_in = tanh((m_i - mu_m_i) / (sigma_m_i + 1e-8))
```

Do not use mass fractions for the final input under the raw-mass dynamics convention.

### D-04: Softening

Closed.

Use matched Plummer softening in residual and Hamiltonian. Do not soften $s_{min}$.

### D-05: Output velocities

Closed.

No velocity output head. Velocities and accelerations come from AD after COM projection.

---

## 15. Final Readiness Call

The corrected framework is implementation-ready **only after** the P0 patch pass and validation suite are complete.

The final framework preserves the project's intended architecture and curriculum but changes three critical implementation contracts:

1. the final IC vector is reconstructive rather than invariant-only;
2. the loss is stationary and causal rather than pseudo-ALM-on-MSE;
3. the force and Hamiltonian use one matched softened potential.

After these changes, remaining concerns are empirical capacity questions, not internal mathematical contradictions.

Training should not begin from the unpatched CTL/PINN specs.

---

## 16. Minimal Code Skeletons

### 16.1 COM projection

```python
def project_com(r_raw, masses, eps=1e-12):
    """
    r_raw: (..., 3, 3)
    masses: (..., 3) or (3,)
    returns: (..., 3, 3), mass-weighted COM projected positions
    """
    m = masses[..., :, None]
    total = m.sum(axis=-2, keepdims=True)
    com = (m * r_raw).sum(axis=-2, keepdims=True) / (total + eps)
    return r_raw - com
```

### 16.2 Matched acceleration

```python
def acceleration_plummer(r, masses, eps_train=1e-5):
    """
    r: (..., 3, 3), scaled projected positions
    masses: (..., 3) or (3,), raw ordered masses
    returns: (..., 3, 3), scaled acceleration d2r'/du2
    """
    a = zeros_like(r)
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            delta = r[..., j, :] - r[..., i, :]
            rsafe = sqrt((delta * delta).sum(axis=-1, keepdims=True) + eps_train**2)
            a[..., i, :] += masses[..., j, None] * delta / (rsafe**3)
    return a
```

### 16.3 Hamiltonian

```python
def hamiltonian_plummer(r, v, masses, eps_train=1e-5):
    kinetic = 0.5 * (masses[..., :, None] * v**2).sum(axis=(-2, -1))
    potential = 0.0
    for i in range(3):
        for j in range(i + 1, 3):
            delta = r[..., i, :] - r[..., j, :]
            rsafe = sqrt((delta * delta).sum(axis=-1) + eps_train**2)
            potential -= masses[..., i] * masses[..., j] / rsafe
    return kinetic + potential
```

### 16.4 Jacobi IC construction

```python
def jacobi_state(m, r0, v0):
    """
    Inputs are ordered, COM-frame, rotation-gauge, scaled arrays.
    m: (3,)
    r0: (3,3)
    v0: (3,3)
    """
    m1, m2, m3 = m
    rho = r0[1] - r0[0]
    lam = r0[2] - (m1 * r0[0] + m2 * r0[1]) / (m1 + m2)
    drho = v0[1] - v0[0]
    dlam = v0[2] - (m1 * v0[0] + m2 * v0[1]) / (m1 + m2)
    return rho, lam, drho, dlam
```

### 16.5 IC13 assembly

```python
def build_ic13(m, rho, lam, drho, dlam, E, stats):
    channels = []
    for i in range(3):
        channels.append(tanh((m[i] - stats.mu_m[i]) / (stats.sigma_m[i] + 1e-8)))

    raw = {
        "rho_x": rho[0],
        "lambda_x": lam[0],
        "lambda_y": lam[1],
        "drho_x": drho[0],
        "drho_y": drho[1],
        "drho_z": drho[2],
        "dlambda_x": dlam[0],
        "dlambda_y": dlam[1],
        "dlambda_z": dlam[2],
    }

    for name in [
        "rho_x", "lambda_x", "lambda_y",
        "drho_x", "drho_y", "drho_z",
        "dlambda_x", "dlambda_y", "dlambda_z",
    ]:
        channels.append(tanh((raw[name] - stats.mu[name]) / (stats.sigma[name] + 1e-8)))

    channels.append(tanh(E / (stats.E_scale + 1e-8)))
    ic13 = array(channels)
    assert ic13.shape == (13,)
    return ic13
```

---

## 17. One-Sentence Final Rule

Use the final patched framework as a **raw-mass, COM/gauge-fixed, reconstructively conditioned, position-output PINN** trained with **componentwise AD, matched Hamiltonian physics, causal residual weighting, explicit IC anchoring, and bounded-horizon chaotic validation**.
