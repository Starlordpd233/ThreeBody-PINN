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
