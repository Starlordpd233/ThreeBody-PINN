# Research report — candidate dispositions for owner ratification

## 1. Premise-challenge findings

The supplied evidence supports the observed initialization saturation and the recorded halt. It does **not** establish a converged-network residual reference, prove that the failure is independent of every possible training budget, or quantify what changing `first_omega_0` would accomplish.

Following your revised access instruction, this report uses the attachments and published literature without live repository verification. Evidence labels are:

- **[P] Package-derived:** statements or repository excerpts supplied in the attachments.
- **[L] Literature:** published sources, with complete references below.
- **[A] Analysis:** independent derivations, interpretations, or proposed defaults.

No claim below is labeled repository-verified. Repository citations retain the original `file:line` anchors supplied by the bundles. `pinn_architecture.md` and `ctl_instruction.md` mean the authoritative files under `pinn_instruction/markdown_conversion/framework-specs/`, at the package’s pin `6a4f9b9902ab62e1d1f57bba0e521f38120c416d`; they do not mean the frozen copies. [P: `RESEARCH-CONTEXT-MASTER.md:90`, `RESEARCH-CONTEXT-MASTER.md:321`]

### Finding 1 — Gate B is misidentified as a trained-network result.

[P] The operative diagnosis says Gate B measured a **trained network** against ground truth. The audit instead says it finite-differenced a **stored Brutus trajectory** and compared that acceleration with the gravitational force calculation. Those descriptions contradict each other. [`52-DIAG-05-REDERIVATION.md:83`; `2026-08-17-residual-frame-conformance-audit.md:109`]

[A] Consequently, the reported relative error, approximately $0.00647$, does not establish that a converged PINN has $\bar R=O(1)$. Even for the reference trajectory, converting a relative acceleration error into $\bar R$ requires the absolute acceleration norm and compatible aggregation:

$$
\bar R=\frac{\Vert a-F\Vert ^2}{3}
      =\frac{e_{\mathrm{rel}}^2\Vert a\Vert ^2}{3}.
$$

The audit’s converged-network inference, subsequently transcribed as F-12, therefore cannot supply a normalization constant. [P: `2026-08-17-residual-frame-conformance-audit.md:167`; `RESEARCH-CONTEXT-MASTER.md:278`]

### Finding 2 — “Proven budget-independent” exceeds the evidence.

[P] The record establishes six initialization cases and a 502-step halted run. It also reports a fitted decline of $0.255$ decades over the 402 steps at full physics weight. The diagnosis nevertheless calls failure “proven budget-independent.” [`2026-08-17-residual-frame-conformance-audit.md:140`, `2026-08-17-residual-frame-conformance-audit.md:151`, `2026-08-17-residual-frame-conformance-audit.md:128`; `52-DIAG-05-REDERIVATION.md:84`]

[A] Initialization saturation proves suppression at initialization, not permanent inability to reduce the first residual. Because $w_1=1$, an effective physics gradient remains. The defensible conclusion is that the existing calibration failed throughout the observed budget—not that every larger budget or every IC must fail identically. The universal IC claim is similarly stronger than the sampled evidence. [P: `pinn_architecture.md:435`; `52-DIAG-05-REDERIVATION.md:80`]

[L] Initial suppression is not, by itself, contrary to the published causal-PINN method: its illustrated weights initially vanish except at the beginning, then activate during training. [L1, §3; [source](https://arxiv.org/pdf/2203.07404)]

### Finding 3 — The attribution to `first_omega_0` alone remains inconsistent, and the stack-gain argument is heuristic.

[P] Master F-02 still says `first_omega_0 = 30` “sets” the derivative magnitude, although M2 explicitly corrected that attribution to include the SQR-SkipResNet stack. [`RESEARCH-CONTEXT-MASTER.md:268`; `RESEARCH-CONTEXT-MASTER.md:129`]

[A] The audit’s scalar expression $2\,\mathrm{LN}(x)/\mathrm{std}(x)$ is not the complete Jacobian of a squared LayerNorm branch. Its second derivative also depends on Hessian terms. Thus, multiplying six approximate scalar gains is not a quantitative prediction for this network. The independent derivation appears in §2.3 below. [P: `2026-08-17-residual-frame-conformance-audit.md:165`]

[A] Furthermore, dividing the printed acceleration medians by the printed velocity medians gives approximately **655–993**, rather than 650–900. Those ratios are not necessarily medians of pointwise ratios, so this discrepancy limits the precision of the frequency interpretation; it does not overturn the large measured derivatives. [P: `2026-08-17-residual-frame-conformance-audit.md:142`]

### Finding 4 — The count discrepancy needs a unit, and “256×” is not the exact endpoint-prefix multiplier.

[P] The architecture listing defaults to 4096 and recommends 2048–4096. The curriculum document calls 4096 collocation points a **provisional/example budget**, in a section describing a 256-trajectory batch. The audit already records the executed count of 16 as an open recipe qualification. [`pinn_architecture.md:454`, `pinn_architecture.md:461`; `ctl_instruction.md:1815`, `ctl_instruction.md:1840`; `2026-08-17-residual-frame-conformance-audit.md:175`]

[A] Therefore:

- $4096/16=256$ is the cardinality ratio.
- For equal residuals, the **last exclusive prefix** changes by
  $$
  \frac{4096-1}{16-1}=273.
  $$
- The exponent at the second point has one preceding term, regardless of total count.
- “4096 per batch” and “4096 per trajectory” are materially different configurations. In particular, $256\times16=4096$.

The supplied excerpts do not settle that last unit consistently enough to infer the intended implementation shape. A ruling must specify it.

### Finding 5 — 87.34 is the float32 normal-number boundary, not a universal round-to-zero boundary.

[A] For binary32,

$$
-\log(\text{smallest normal})=126\log2=87.33654.
$$

Subnormal values extend to $149\log2\approx103.279$, with round-to-zero near $150\log2\approx103.972$ under gradual underflow and ordinary rounding. Device flush-to-zero behavior can change the practical boundary.

[P/A] The package’s 87.34 value is appropriate for its **smallest-normal floor guard**, but “the exponential underflows to zero at 87.34” is too broad. This terminology correction does not rescue the baseline: exponents around $10^{10}$ exceed either boundary enormously. [`2026-08-17-residual-frame-conformance-audit.md:127`; `RESEARCH-CONTEXT-MASTER.md:281`]

### Finding 6 — A global gradient-norm ratio does not prove that every data-gradient component rounds away.

[P] The audit reports a median physics/data gradient-norm ratio of $6.3\times10^{12}$, then concludes that the data term contributes nothing to the accumulated float32 gradient. [`2026-08-17-residual-frame-conformance-audit.md:132`, `2026-08-17-residual-frame-conformance-audit.md:134`]

[A] Floating-point addition acts componentwise. For example, $g_{\rm phys}=(A,0)$ and $g_{\rm data}=(0,1)$ preserve the data contribution regardless of their norm ratio. The observation strongly supports severe imbalance, but proving complete disappearance requires componentwise evidence, including alignment and actual accumulation behavior.

Similarly, positive floored causal weights give mathematically nonzero contributions. “Exactly one point receives gradient” should be read as **one effectively weighted point**, not a literal identity. [P: `2026-08-17-residual-frame-conformance-audit.md:169`]

### Finding 7 — Two smaller numerical claims need qualification.

[A/P] Squaring the printed acceleration medians and dividing by three agrees with the printed residual medians to roughly **0.4%**, not to three significant figures in every row. Rounded values and median aggregation limit this check. It remains a useful consistency check, not an exact reconstruction. [`RESEARCH-CONTEXT-MASTER.md:143`]

[P/A] The retained run’s $2.53\times10^{10}$ median covers **502 steps**; calling it “the initialization value” conflates two different summaries. [`2026-08-17-residual-frame-conformance-audit.md:125`, `2026-08-17-residual-frame-conformance-audit.md:159`]

[P] The prompt’s four-copy warning is also stale relative to the master’s five-copy table. This is an anchor-resolution issue, not a physical contradiction. [`RESEARCH-CONTEXT-MASTER.md:90`]

### Finding 8 — A conditional L-BFGS consistency risk must accompany any continuation proposal.

[P] The specifications combine detached causal weights with Adam followed by L-BFGS. They freeze loss multipliers during L-BFGS, but the supplied passages do not settle whether causal weights are recomputed inside its line searches. [`pinn_architecture.md:668`, `pinn_architecture.md:698`, `pinn_architecture.md:741`]

[A] If weights are recomputed as functions of the trial parameters while their derivatives are detached, the supplied gradient omits $\sum_n R_n\nabla w_n$. It is then not the derivative of the scalar objective being compared by a conventional line search. This is a **conditional risk, not a verified implementation defect**. The proposed recipe below freezes the relevant surrogate objective during L-BFGS.

These findings leave the central observation intact: the package reports a correctly scaled residual frame, very large initialization derivatives, floored later weights, and a halted causal front. They remove unjustified claims about convergence scales, universal impossibility, and single-parameter causation. [P: `2026-08-17-residual-frame-conformance-audit.md:109`, `2026-08-17-residual-frame-conformance-audit.md:140`; `52-DIAG-05-REDERIVATION.md:58`]

---

## 2. Answers to master §5.1–§5.6

Door classifications below describe practical reversibility, not authorization:

- **Two-way:** the configuration can be reversed using compatible model checkpoints and modest implementation changes.
- **One-way, practically:** adopting it requires fresh initialization, substantial controller requalification, or spending a significant experimental budget that cannot be recovered.

Even a two-way change to an owner-ratified contract still requires ratification. Every value marked **suggested default** remains a proposal.

### 2.1 — §5.1: Exponent coefficient and form

**Independent capacity calculation.**

[P] Write the specified mechanism as

$$
P_n=\sum_{m<n}\bar R_m,\qquad
z_n=\eta_cP_n,\qquad
w_n=e^{-z_n},\qquad
L_{\rm phys}=\frac1N\sum_nw_n\bar R_n.
$$

The residual is $\bar R_n=\frac13\sum_i\Vert f_i(u_n)\Vert ^2$, and the weights are detached. [`pinn_architecture.md:429`, `pinn_architecture.md:435`, `pinn_architecture.md:440`]

[A] For nonnegative residuals, the two relevant conditions are different:

$$
\begin{aligned}
\text{avoid the normal-number floor at point }n &: \eta_cP_n<B_{32},\\
w_n>0.5 &: \eta_cP_n<\log2,
\end{aligned}
\qquad B_{32}=87.33654.
$$

The second is **126 times stricter in exponent magnitude**. Avoiding underflow does not establish front advancement.

[P/A] Using the retained first-residual median $r=2.53\times10^{10}$ as a representative value gives

$$
\eta_c<3.45\times10^{-9}
\quad\text{to avoid flooring }w_2,
$$

$$
\eta_c<2.74\times10^{-11}
\quad\text{to obtain }w_2>0.5.
$$

These are reductions of 8.46 and 10.56 decades from $\eta_c=1$, respectively. They agree with the audit’s arithmetic. [`2026-08-17-residual-frame-conformance-audit.md:125`, `2026-08-17-residual-frame-conformance-audit.md:126`]

[A] For an explicitly hypothetical **flat residual profile** $\bar R_n=r$, the endpoint constraints are:

| Points in one causal sequence | Endpoint prefix $(N-1)r$ | $\eta_c$ below which no weight reaches the normal floor | $\eta_c$ below which every weight exceeds 0.5 |
|---:|---:|---:|---:|
| 16 | $3.795\times10^{11}$ | $2.30\times10^{-10}$ | $1.83\times10^{-12}$ |
| 2048 | $5.179\times10^{13}$ | $1.69\times10^{-12}$ | $1.34\times10^{-14}$ |
| 4096 | $1.036\times10^{14}$ | $8.43\times10^{-13}$ | $6.69\times10^{-15}$ |

This table is a capacity calculation, **not a reconstruction of an observed weight vector**.

**The published method and its calibration.**

[L] The matching published method is Wang, Sankaran and Perdikaris, *Respecting causality for training physics-informed neural networks*, **Computer Methods in Applied Mechanics and Engineering 421, 116813 (2024)** [L1]. Its public 2022 preprint, §3 and Algorithm 1, calls $\epsilon$ the “causality parameter” controlling the weights’ “slope.” It anneals through

$$
[10^{-2},10^{-1},1,10,100],
$$

allowing up to $S$ optimization steps per value and breaking the inner loop when $\min_iw_i>\delta=0.99$. It uses stop-gradient, an exclusive temporal **sum**, spatial averaging within each temporal residual, and outer loss averaging. There is no $1/N_t$ normalization inside that prefix. Sorted time samples may be redrawn. Its recommended IC weight is $10^3$; its prose treats initial loss as a special temporal residual, although Algorithm 1’s indexing of that term is ambiguous. [Journal record](https://doi.org/10.1016/j.cma.2024.116813); [public preprint, §3 and Algorithm 1](https://arxiv.org/pdf/2203.07404).

[L] The later *Expert’s Guide* [L2] describes choosing a “moderately large” causal coefficient such that all temporal weights approach one **by the end of training**, reducing it if that does not happen. It also groups residuals into temporal chunks, averaging within each chunk before summing earlier chunks. Consequently, a batch containing thousands of points need not create thousands of terms in its causal prefix. [Source, §5.1](https://arxiv.org/pdf/2308.08468).

[P/A] The identifiable project departures or added conventions are:

| Project convention | Consequence for transferring the method |
|---|---|
| Fixed $\eta_c=1$. [`pinn_architecture.md:445`] | The source’s coefficient-continuation procedure is absent. |
| Body-averaged squared vector residual. [`pinn_architecture.md:429`] | The numerical scale must be calibrated for this residual definition. |
| Separate IC term with $\lambda_{\rm IC}=1$. [`pinn_architecture.md:656`, `pinn_architecture.md:665`] | IC treatment cannot be assumed equivalent to the source configuration. |
| A 0.5-front condition and 500-step advancement window. [`2026-08-17-residual-frame-conformance-audit.md:126`; `52-DIAG-05-REDERIVATION.md:58`] | These are project-specific control conditions, distinct from the source’s convergence criterion. |
| Underflow guard, warmup, and Adam/L-BFGS protocol. [`pinn_architecture.md:668`, `pinn_architecture.md:681`, `pinn_architecture.md:730`] | Their interaction with changing causal weights needs an explicit project protocol. |

[A] Copying the source’s initial coefficient $0.01$ would not solve this case: it leaves $z_2\approx2.53\times10^8$. The source provides a calibration strategy, not a universal coefficient valid across arbitrary residual units and counts.

**Options menu D1.**

All three options below are [A].

| Rank / option | Mechanical effect and behavior across training | Cross-decision interactions | Door |
|---|---|---|---|
| **1. D1-A — Suggested default: count-normalized exponential with coefficient continuation** | Use $z_n=\frac{\gamma_j}{N-1}\sum_{m<n}\operatorname{stopgrad}(\bar R_m/C)$. Start at $\gamma_0=2$, then increase only after a level satisfies declared conditions. | Requires D2-A’s fixed reference, D4’s explicit sequence count, and revised controller semantics in D6-A. | **Two-way:** compatible network and checkpoint structure; controller state must be recorded. |
| 2. D1-B — Same formula, fixed $\gamma=2$ | Removes the initial scale mismatch under the representative profiles, but becomes nearly uniform long before residuals are small. Suitable as a bounded control, not a demonstrated full-range curriculum. | Same D2/D4 choices; needs an accuracy gate independent of weights. | **Two-way:** coefficient configuration only. |
| 3. D1-C — Log-compressed exponent | Use $z_n=\frac{0.04}{N-1}\sum_{m<n}\log(1+\bar R_m)$. Compression greatly expands numerical capacity, but weakens the meaning of the front. | Supersedes D2-A with a unit reference, D2-B. It is a new formula, not an implementation of L1. | **Two-way:** compatible model; formula and gate amendment required. |

**Quantified default and its limitations.**

[A] With $C=2.60\times10^{10}$, $N=4096$, and $\gamma_0=2$,

$$
\eta_{\rm effective,0}
=\frac{2}{4095C}
=1.8785\times10^{-14}.
$$

For the representative flat profile $r=2.53\times10^{10}$,

$$
z_N=1.9462,\qquad w_N=0.1428,\qquad w_2=0.999525.
$$

Thus this combination exceeds the capacity needed to avoid flooring and to move beyond the first point, while retaining later suppression. The fraction of points above 0.5 is approximately $0.356$ for that flat profile. Making **every** point exceed 0.5 at initialization is not the objective.

[A/P] Using the six reported medians as separate flat profiles gives endpoint weights approximately $0.135$–$0.382$. Using the largest retained $R_1$, $3.93\times10^{11}$, as a deliberately severe flat profile gives $z_N=30.23$, still below 87.34. These are useful stress calculations, but neither medians nor the largest recorded **first-point** residual bound the unseen full prefixes. [`2026-08-17-residual-frame-conformance-audit.md:125`, `2026-08-17-residual-frame-conformance-audit.md:147`, `2026-08-17-residual-frame-conformance-audit.md:148`]

**Behavior beyond initialization.**

[P] The evidence establishes initialization medians around $10^{10}$ and retained $R_1$ values from $6.46\times10^8$ to $3.93\times10^{11}$. It does not establish a converged-PINN endpoint or a post-recalibration trajectory. [`2026-08-17-residual-frame-conformance-audit.md:125`, `2026-08-17-residual-frame-conformance-audit.md:142`; `RESEARCH-CONTEXT-MASTER.md:309`]

[A] The following covers a proposed working range, not a measured training history:

| Flat residual $r$ | Endpoint exponent at fixed $\gamma=2$ | Endpoint weight |
|---:|---:|---:|
| $3.93\times10^{11}$ | 30.23 | $7.43\times10^{-14}$ |
| $2.53\times10^{10}$ | 1.946 | 0.1428 |
| $10^8$ | 0.007692 | 0.99234 |
| $10^4$ | $7.69\times10^{-7}$ | 0.99999923 |
| $1$ | $7.69\times10^{-11}$ | effectively 1 |
| $10^{-4}$ | $7.69\times10^{-15}$ | effectively 1 |

This is why D1-B is not the suggested default: its weights become nearly uniform while residuals remain enormous relative to any plausible accuracy target.

[A] For D1-A, propose a **training-control** tolerance

$$
\tau_{\rm ctrl}=10^{-4},\qquad \delta=0.99,
$$

$$
q_j=\frac{-C\log\delta}{\gamma_j},
\qquad
\gamma_{\max}=\frac{-C\log\delta}{\tau_{\rm ctrl}}
=2.6131\times10^{12}.
$$

Advance to $\min(10\gamma_j,\gamma_{\max})$ only when, on the designated training collocation sets,

$$
\min_nw_n>0.99
\quad\text{and}\quad
\max_n\bar R_n<q_j.
$$

The additional raw-residual condition prevents the last point—which is absent from its own exclusive prefix—from escaping the control criterion. It is deliberately stronger than a prefix-average condition.

[P/A] The numerical value $10^{-4}$ is borrowed only as a **candidate** from the specification’s provisional validation threshold. This proposed pointwise training condition is a new condition, not the existing validation metric and not authorization to evaluate held-out data. [`ctl_instruction.md:1966`, `ctl_instruction.md:1969`]

[A] Initially $q_0=1.3065\times10^8$; at the final level $q=\tau_{\rm ctrl}$. For unchanged residuals, a tenfold coefficient increase after $\min w>0.99$ gives

$$
\min w_{\rm next}>0.99^{10}=0.90438,
$$

so the scheduled transition itself does not recreate flooring. The final effective raw coefficient is approximately $0.02454$, not the locked value 1.

This establishes conditional numerical coherence across the proposed range. It does **not** establish that optimization can traverse that range within the existing budget. Residual spikes can still saturate a level; those require reporting and review, not an unannounced reference update.

[A] D1-C has a different capacity:

$$
z_N=0.04\log(1+r),\qquad w_N=(1+r)^{-0.04}.
$$

At the representative initialization scale, $w_N\approx0.384$. For any finite binary32 residual, its flat-profile exponent is at most approximately 3.55, safely below the normal floor. But $w_N>0.5$ already when $r<33{,}554{,}431$. Numerical robustness therefore does not make its front an accuracy certificate.

---

### 2.2 — §5.2: Residual normalization and reference

[P] The residual already lives in the specified dimensionless training frame. “Unnormalized” here means lacking a further numerical reference for causal control, not lacking nondimensionalization. [`ctl_instruction.md:1757`; `pinn_architecture.md:429`]

[A] With exponent-only normalization,

$$
z_n=\frac{\eta_c}{C}P_n.
$$

Multiplying $C$ by $a$ divides every exponent by $a$. Therefore $\eta_c$ and $C$ are not independent mechanisms: only their ratio affects the weights.

For $\eta_c=1$ and the representative flat profile:

$$
C>\frac{r}{\log2}=3.65\times10^{10}
$$

is required for the first advance, while at $N=4096$,

$$
C>\frac{4095r}{87.3365}=1.19\times10^{12}
$$

avoids endpoint flooring, and

$$
C>\frac{4095r}{\log2}=1.49\times10^{14}
$$

makes every weight exceed 0.5.

Thus $C=2.60\times10^{10}$ **alone**, leaving the raw coefficient and prefix unchanged, is insufficient: it gives $z_2=0.973$ and $z_N=3984.75$. It works in the suggested recipe only through its declared combination with $\gamma/(N-1)$.

**Options menu D2.**

All options are [A]; the provenance for D2-A’s numerical value is the maximum of the six reported initialization medians, not a measured maximum residual. [P: `2026-08-17-residual-frame-conformance-audit.md:142`]

| Rank / option | Mechanical effect and behavior across training | Cross-decision interactions | Door |
|---|---|---|---|
| **1. D2-A — Suggested default: fixed initialization reference, exponent only** | Freeze $C=2.60\times10^{10}$. As residuals decrease, $\bar R/C$ decreases; continuation can tighten the criterion without erasing measured progress. | Use D1-A. Keep the outer physics loss raw. Reassess the reference if architecture or initialization changes. | **Two-way:** reference and coefficient can be changed through a documented compatible checkpoint. |
| 2. D2-B — No explicit normalization | Set $C=1$, but replace every $\gamma_j$ by $\gamma_j/(2.60\times10^{10})$ to obtain exactly the same exponential weights as D2-A. | Mechanically equivalent for D1-A; less explicit scale provenance. Also supplies D1-C’s unit reference. | **Two-way:** algebraic reparameterization. |
| 3. D2-C — Normalize both exponent and outer physics loss | Replace the outer $\bar R$ by $\bar R/C$. This changes physics gradients by $1/C$, as well as controlling causal weights. | Changes total-loss balance and requires explicit loss-assembly ratification; printed $\lambda_{\rm phys}=1$ would no longer mean the same effective scale. | **Two-way mechanically:** compatible weights, but optimizer state and loss-balance interpretation need review. |
| 4. D2-D — Online mean/EMA reference without a fixed lower scale | If all residuals decrease by a common factor, numerator and reference decrease together. The weight profile can remain unchanged indefinitely. | Requires a separate progress controller or a declared reference floor; incompatible with interpreting weight opening as absolute residual reduction by itself. | **Two-way:** controller state must be checkpointed to reverse it faithfully. |

[A] D2-A is suggested for **traceability and separation of controls**, not because a fixed reference has proven superior performance. D2-B is mathematically tied with it on weight behavior.

[A] D2-C can address a different problem: raw loss-scale imbalance. For fixed weights,

$$
\nabla_\theta L_{\rm phys}^{\rm normalized}
=\frac1C\nabla_\theta L_{\rm phys}^{\rm raw}.
$$

Dividing the recorded $6.3\times10^{12}$ norm ratio by $C$ gives approximately 242, but that is only arithmetic holding the old gradients and weights fixed—not a prediction for the proposed run. [P: `2026-08-17-residual-frame-conformance-audit.md:132`]

[P/A] The suggested defaults deliberately do **not** adopt automatic loss reweighting. That control is deferred in the specification pending weighted-loss and gradient evidence. Consequently, repairing causal weights does not establish that data and IC learning will be adequately balanced. [`pinn_architecture.md:690`]

[A] A physical acceleration reference $a_{\rm ref}$, if later established, would normalize $\bar R$ by $a_{\rm ref}^2$, not $a_{\rm ref}$. Gate B supplies neither a converged-network reference nor the necessary absolute norm.

---

### 2.3 — §5.3: SIREN initialization scale

**Independent derivation before comparison with H-01.**

[A] Let the first activation be $h(u)=\sin(\omega z(u))$, where $z$ is affine in $u$. Then

$$
h'=\omega z'\cos(\omega z),\qquad
h''=-\omega^2(z')^2\sin(\omega z).
$$

For the remaining network $r=H(h)$,

$$
r''=J_Hh''+\mathcal H_H[h',h'].
$$

If downstream Jacobians, Hessians, amplitudes, and cancellations remain comparable, both contributions have a nominal $\omega^2$ scale. If acceleration dominates gravity, squaring the residual then gives the **conditional** scaling

$$
\bar R(\omega)\approx
\bar R(30)\left(\frac{\omega}{30}\right)^4.
$$

Changing $\omega$ also changes phases and downstream activations. This is therefore neither a measured law nor a guaranteed bound for the specified stack.

[A] For LayerNorm without affine parameters, define

$$
P=I-\frac{\mathbf1\mathbf1^\top}{d},\quad
s^2=\frac{\Vert Px\Vert ^2}{d}+\epsilon,\quad z=\frac{Px}{s}.
$$

Then

$$
J_{\rm LN}=\frac1s\left(P-\frac{zz^\top}{d}\right),
$$

$$
J_{(\rm LN)^2}
=2\,\operatorname{diag}(z)\,
  \frac1s\left(P-\frac{zz^\top}{d}\right).
$$

The projection, cross-coordinate terms, and second derivatives matter. Also, when $\epsilon$ is negligible, LayerNorm approximately cancels common positive amplitude scaling. Lowering an upstream amplitude need not lower every downstream derivative proportionally.

[P] These qualifications apply directly because the specified stack uses squared LayerNorm skip branches, affine-free LayerNorm, 12 layers, and a fixed first frequency of 30. [`pinn_architecture.md:221`, `pinn_architecture.md:250`, `pinn_architecture.md:270`, `pinn_architecture.md:273`, `pinn_architecture.md:274`]

[L] Sitzmann et al.’s SIREN paper [L3] supplies periodic activations and their initialization scheme; its reported usefulness of first-layer frequency 30 is empirical. It does not validate derivative magnitudes for this custom LayerNorm/power-residual stack. Its hidden-layer parameterization also couples frequency with inverse weight scaling: changing that frequency while correspondingly rescaling initialization can leave the effective input mapping unchanged, while changing parameter-gradient scales. [Source and supplement](https://arxiv.org/pdf/2006.09661).

**Capacity against both thresholds.**

[A] Applying the conditional fourth-power model to $2.53\times10^{10}$:

| First frequency | Nominal residual | Reduction | Standalone result with raw $\eta_c=1$ |
|---:|---:|---:|---|
| 30 | $2.53\times10^{10}$ | None | First later weight floored |
| 10 | $3.12\times10^8$ | 1.91 decades | Still exceeds both first-point thresholds |
| 1 | $3.12\times10^4$ | 5.91 decades | Still exceeds both first-point thresholds |

[A] Under that same unverified model, one would need approximately:

- $\omega<0.230$ to avoid flooring $w_2$;
- $\omega<0.0686$ to obtain $w_2>0.5$;
- $\omega<0.00858$ to make the entire 4096-point flat-profile vector exceed 0.5.

These are **not recommended settings**. At such changes, force dominance, LayerNorm behavior, representational capacity, and the scaling approximation itself can change.

**Options menu D3.**

| Rank / option | Capacity, later behavior, and interaction | Door |
|---|---|---|
| **1. D3-A — Suggested default: retain first frequency 30 and the existing stack** | [A] Avoids adding an unmeasured architecture change while D1/D2 address the observed exponent mismatch. Makes no promise that derivative optimization or IC fitting will succeed. | **Two-way:** preserves model compatibility and leaves future ablations available. |
| 2. D3-B — Fresh initialization with first frequency 10 | [A] Nominal 81-fold residual reduction is insufficient alone. Requires fresh residual characterization and a revised D2 reference; late-training behavior is unknown. | **One-way for run lineage:** the contract requires fresh initialization for retuning. |
| 3. D3-C — Fresh initialization with first frequency 1 | [A] Nominal $810{,}000$-fold reduction is still insufficient alone. Greater risk of changing temporal representation and IC fitting; no supplied measurements establish the actual scale. | **One-way for run lineage:** fresh initialization and renewed comparison are required. |

[P] The contract allows frequency retuning only through a stage-boundary ablation with fresh reinitialization, not scheduling within a run. [`pinn_architecture.md:181`, `pinn_architecture.md:184`]

[A] Near convergence, $a$ and $F$ must cancel. There is then no general fourth-power law for $\Vert a-F\Vert ^2$. Any changed-frequency option must be assessed at initialization **and** through residual reduction; an initialization-only improvement is not sufficient evidence.

**H-01 comparison.** [A/P] The derivation supports the summarized second-derivative mechanism, but not exclusive attribution to frequency 30 or a uniquely implied remedy. The actual Q3 of trainex-r2 was not attached, so its full interpretation cannot be adjudicated line by line. That round prohibited remedy recommendations and predates the repairs; its omission of a remedy is not evidence against alternatives. [r2-QUAL] [`RESEARCH-CONTEXT-MASTER.md:20`, `RESEARCH-CONTEXT-MASTER.md:29`, `RESEARCH-CONTEXT-MASTER.md:289`]

---

### 2.4 — §5.4: Collocation count

[A] For a flat profile,

$$
z_n=\eta_c(n-1)r.
$$

Increasing $N$ changes endpoint capacity, but does not change the one-term exponent at $n=2$ if $R_1$ is held fixed. Reducing count therefore cannot independently repair the first-point mismatch.

With the suggested normalization,

$$
z_n=\gamma\frac{n-1}{N-1}\frac rC.
$$

At the same fractional position $(n-1)/(N-1)$, the exponent is exactly count-independent for a flat profile. For smooth residual functions and uniform sampling, it approximates a cumulative integral; count changes then affect quadrature and sampling error rather than intentionally multiplying causal strength.

[A] The denominator must be the **fixed sequence length $N-1$**. Dividing each prefix by its own length $n-1$ would produce the same weight at every later point for a flat profile, removing the intended temporal gradient.

**Options menu D4.**

All numerical capacity statements here are [A].

| Rank / option | Effective initial raw coefficient with D1-A/D2-A | Trade-off and interaction | Door |
|---|---:|---|---|
| **1. D4-A — Suggested default: 4096 points per logical causal sequence/trajectory** | $1.8785\times10^{-14}$ | Explicitly resolves the unit and follows the architecture listing’s default. Highest cost of this menu; not established as optimal or necessary. | **Two-way:** sampling/count change with compatible weights; preserve normalized prefix semantics. |
| 2. D4-B — 2048 per sequence | $3.7578\times10^{-14}$ | Half the point count; within the stated recommended range. Same nominal causal strength, less sampling coverage. | **Two-way:** count and denominator change together. |
| 3. D4-C — 16 per sequence | $5.1282\times10^{-12}$ | Useful bounded diagnostic comparison with the reported probes. Coarse temporal sampling and no evidence of adequate trajectory accuracy. | **Two-way:** suitable as an explicitly qualified control, not a hidden production default. |

[P] The documentary grounds for 4096 and 2048 are the default listing and recommendation, not a demonstrated accuracy optimum. [`pinn_architecture.md:454`, `pinn_architecture.md:461`; `ctl_instruction.md:1840`]

[A/P] At 256 trajectories, D4-A implies **1,048,576 physics points per logical batch**, before accounting for derivative work. Feasibility is unmeasured. If microbatching is needed, it must preserve each trajectory’s full exclusive prefix, its $1/N$ loss normalization, and the intended batch reduction. Resetting the prefix at microbatch boundaries changes the method. [`ctl_instruction.md:1815`]

[A] The suggested sampler is uniform and sorted within each trajectory. A single causal prefix must not mix times from different ICs. Adaptive sampling changes the measure represented by a normalized sum unless an appropriate correction is included; that would be another declared choice.

[A] Across training, count normalization preserves the same scalar-residual response at corresponding time fractions. It does not guarantee identical weights on different random samples. In particular, denser sampling can discover residual spikes that the 16-point characterization missed. The default consequently remains conditional on the proposed full-prefix preflight.

---

### 2.5 — §5.5: Causal-exponent clip

[A] Represent the guard as

$$
w_n=\exp[-\min(z_n,B)].
$$

For $z_n<B$, it changes nothing. For $z_n\ge B$, it replaces further distinctions with a common floor $e^{-B}$. It is therefore a numerical guard, not a calibration mechanism.

[P] This preserves the declared underflow-only purpose. [`pinn_architecture.md:668`, `pinn_architecture.md:671`]

**Options menu D5.**

| Rank / option | Capacity and behavior across the residual range | Cross-decision interaction | Door |
|---|---|---|---|
| **1. D5-A — Suggested default: dtype/device normal-floor guard** | [A] $B=-\log(\mathrm{tiny}_{\rm dtype})$; for float32, $B=87.33654$. No effect below this boundary; no change to the $\log2$ front threshold. | Compute and log the normalized, unclipped exponent first. D1/D2/D4 must supply calibration. | **Two-way:** numerical implementation choice, with unchanged intended weights above the floor. |
| 2. D5-B — Float64 exponent/weight path | [A] Normal-floor boundary becomes $708.396$, only 8.11 times the exponent capacity, or 0.91 decades. Still nowhere near raw $10^{10}$; front threshold unchanged. | Helps accumulation/rounding diagnostics, with extra cost. Does not replace recalibration. | **Two-way:** dtype change, subject to consistent downstream casting. |
| 3. D5-C — Deliberately small cap, e.g. $B=0.5$ | [A] Every weight is at least $e^{-0.5}=0.6065$, so every point passes the 0.5 test regardless of residual. | Changes curriculum semantics and invalidates the existing front interpretation. It is not an underflow-only guard. | **Two-way mechanically:** but requires a substantive formula/gate amendment before use. |

[A] D5-A has no independent “decade-reduction” capacity: it masks large exponents after they occur. D5-B adds insufficient capacity to the baseline. D5-C crosses the front threshold by construction, without evidence of learning.

[A] Reject nonfinite residuals and prefixes **before** clipping; otherwise an overflow can be disguised as an ordinary floored weight. Device-specific exponent behavior and rounding at the bound belong in an owner-authorized numerical preflight. The package reports an existing dtype/device floor resolver, so this is not a proposal to repair an absent clip. [P: `RESEARCH-CONTEXT-MASTER.md:281`]

---

### 2.6 — §5.6: Joint disposition and mechanism redesign

[P] The routing authority expressly permits curriculum redesign that avoids requiring initialization and causal scales to agree. The current default’s exclusion of windowed mechanics is a contract requiring amendment, not a reason to omit this authorized research family. [`52-VER-20-ROUTING-HANDOFF.md:45`; `ctl_instruction.md:1823`; `pinn_architecture.md:692`]

**Options menu D6.**

| Rank / option | Mechanical surface and full-range behavior | Interaction with other menus | Door |
|---|---|---|---|
| **1. D6-A — Suggested default: continuation recipe assembled from D1-A through D5-A** | [A] Retains the exponential family and network; separates initial numerical calibration from progressively tighter residual control. Performance remains untested. | Activates all five menus. Requires explicit front-monitoring and optimizer-handoff amendments. | **Two-way mechanically:** compatible model; amended controller state and provenance must be preserved. |
| 2. D6-B — Growing physics-time prefix, without residual-exponential activation | [A] Train unweighted physics residuals on $[0,j/16]$, starting at $j=1$, retaining earlier intervals as $j$ grows. Advance using an explicit training-residual gate, proposed $\max\bar R<10^{-4}$. Initial active weights are 1 regardless of residual magnitude. | D1’s exponent and D2’s exponent reference become unnecessary. D4 remains a sampling decision. Requires new curriculum, sampling, and gate contracts. | **One-way practically:** substantial protocol requalification and a distinct training history. |
| 3. D6-C — Disable causal weighting, $w_n=1$ | [A] Removes suppression for every finite residual immediately. Provides a useful diagnostic of whether causal suppression drives the failure, but supplies no temporal pacing. | D1/D2/D5 causal controls become inapplicable; the front cannot serve as a progress metric. | **Two-way:** compatible-network control, with its diagnostic status explicit. |
| 4. D6-D — Adopt Causal R3 without modifying its gate update | [L/A] Offers a different sampling/gating system, but does not automatically remove residual-scale sensitivity. | Requires its own coefficient/loss-scale disposition; not a justified drop-in escape from this problem. | **One-way practically:** new sampler, controller, and acceptance semantics. |

[L] Penwarden et al. [L4] provide published support for causal sweeping through collocation strategies and temporal decompositions. That supports considering D6-B’s family; it does not validate this report’s proposed 16 prefixes or tolerance for three-body trajectories. [Source](https://arxiv.org/abs/2302.14227); [journal record](https://doi.org/10.1016/j.jcp.2023.112464).

[A] D6-B addresses the initialization mismatch directly: active-point exponents are effectively zero, so active weights are one at any finite $\bar R$. This clears both numerical thresholds without pretending residuals are small. The advancement gate can still be difficult or impossible to satisfy within budget, but its failure would not result from an exponential hiding all active physics points. Retain the original global coordinate $u=t/T$; do not silently rescale derivatives to each growing interval.

[L] Daw et al.’s Causal R3 [L5] uses a temporal gate

$$
g(t)=\frac{1-\tanh[\alpha(t/T-\gamma)]}{2}
$$

and a gate-motion term proportional to $\exp(-\epsilon L_g)$. [Source](https://proceedings.mlr.press/v202/daw23a/daw23a.pdf).

[A] That motion can itself freeze when $\epsilon L_g$ is large. Its normal-floor condition is $\epsilon L_g<B$, and obtaining more than half the maximum nominal motion requires $\epsilon L_g<\log2$. Thus importing a method labeled “causal” or “adaptive” does not establish independence from initialization scale. Actual $L_g$ values for this project are unavailable.

[A] I rank D6-A first because it permits a direct test of the diagnosed mismatch while retaining the architecture and residual objective. D6-B is the strongest alternative if continuation remains ineffective or proves too dependent on residual calibration. The evidence does not yet justify selecting between their eventual trajectory accuracy.

#### Composed first-run recipe — a cross-menu coherence check

Everything proposed in this table is [A]; inherited contracts are cited.

| Component | Candidate configuration for owner ratification |
|---|---|
| Scope and initialization | Fresh Stage-0 trial, seed 41, existing 12-layer architecture and `first_omega_0=30`. No frequency scheduling. [P: `pinn_architecture.md:181`, `pinn_architecture.md:270`] |
| Physics quantity | Preserve $\bar R=\frac13\sum_i\Vert f_i\Vert ^2$, the current nondimensional frame, and the raw outer physics loss. [P: `pinn_architecture.md:429`; `ctl_instruction.md:1757`] |
| Sampling | 4096 sorted uniform points **per trajectory/causal sequence**. No prefixes across ICs or accidental resets across microbatches. |
| Reference | Freeze $C=2.60\times10^{10}$, with provenance “largest of six reported initialization medians.” Do not update it online. |
| Causal weights | $z_n=\gamma_j\sum_{m<n}\operatorname{stopgrad}(\bar R_m/C)/(4095)$, $w_1=1$, $w_n=e^{-\min(z_n,B_{32})}$. |
| Continuation | $\gamma_0=2$; multiply by at most 10 after the conditions in §2.1; cap at $2.6131\times10^{12}$. Use $\delta=0.99$, $\tau_{\rm ctrl}=10^{-4}$, and the additional all-point raw-residual condition. |
| Loss multipliers | Keep $\lambda_{\rm IC}=1$, $\lambda_{\rm phys}^{\max}=1$, and Stage-0 $\lambda_E=\lambda_L=0$. Do not divide the outer loss by $C$. [P: `pinn_architecture.md:665`, `pinn_architecture.md:683`, `pinn_architecture.md:684`] |
| Budget and warmup | Retain the authorized run budget; do not allocate a new budget for every coefficient level. The recorded 1000-step Adam budget implies the existing 100-step warmup. [P: `2026-08-17-residual-frame-conformance-audit.md:136`] |
| Front monitoring | Report both time reached and normalized front fraction. Do not count a changed count, changed coefficient, or reference adjustment as learning. Retain advancement monitoring while the front is incomplete; after it reaches the horizon, use residual/continuation progress rather than requiring impossible further index advancement. |
| Adam/L-BFGS handoff | Proposed amendment: hand off only after the final continuation level qualifies **and** the approved plateau condition holds. A premature plateau or exhausted budget produces HALT/REVIEW, not a silent handoff or extra optimization budget. Existing plateau criterion: `ctl_instruction.md:1894`, `ctl_instruction.md:1895`. |
| L-BFGS objective | Freeze sampled data/collocation sets, causal weights, $\gamma$, $C$, and scheduled multipliers throughout the refinement subproblem. Preserve the existing Adam-only gradient-clipping rule. [P: `pinn_architecture.md:698`, `pinn_architecture.md:768`] |
| Acceptance | Weight opening is a control diagnostic, not trajectory accuracy. Existing owner-governed acceptance remains separate. This recipe contains no held-out evaluation step. |

[A] The combination is algebraically coherent: D4 removes the prefix-count multiplier; D2 records the reference; D1 controls residual-range progression; D5 supplies only a numerical guard; D3 avoids adding an unmeasured derivative-scale change.

It is **not yet empirically qualified**. In particular, it may leave physics/data/IC imbalance unresolved, and the proposed tolerance may be unattainable within the retained budget. Existing execution constants not reproduced in the attachments—such as the complete L-BFGS budget—must be inherited from the authorized run manifest, not invented.

#### Owner-gated discriminating experiments

These are proposals only. None was performed.

| Option | Discriminating purpose | Suggested standing | Door |
|---|---|---|---|
| **E1 — Full-prefix initialization characterization** | On the proposed count, dtype, and specified training IC cases, record every residual, exclusive prefix, unclipped exponent, weight, and front. Test whether the actual vector has neither floor saturation nor nearly uniform weights alongside large residuals. | **Suggested default next evidence step.** It directly tests the median-based calibration assumption. | **Two-way:** bounded diagnostic cost; no held-out data. |
| E2 — One bounded Stage-0 trial of the ratified composed recipe | Determine whether raw residuals and IC/data losses improve, whether the controller progresses, and whether gradient imbalance remains disabling. | Conditional on E1 and owner authorization. No automatic additional runs. | **One-way in budget:** training compute and the resulting lineage cannot be recovered. |
| E3 — Matched count or fresh-frequency comparison | Compare one declared uncertainty: e.g. 16/2048/4096 with count-normalized weights, or fresh $\omega=30/10/1$ with measured initialization profiles. | Alternative research expenditure requiring a predeclared comparison and stopping rule. | **One-way in budget:** multiple runs; frequency changes also require fresh initialization. |

[A] For E1, the intended signature in the reported high-residual regime is $w_2>0.5$, some later suppression, finite prefixes, and no floor saturation. Uniform weights are acceptable when residuals are already genuinely small; they are not evidence of learning when produced solely by a tiny coefficient or permissive cap.

[P] These proposals do not authorize post-amendment tuning loops. The master limits subsequent iteration to conformance work unless the owner separately commissions more research. [`RESEARCH-CONTEXT-MASTER.md:381`]

#### What the runbook inherits

[A/P] An implementer would need to carry forward:

1. **The owner’s signed disposition and exact amendments.** Record formula changes under LOSS-04, count units, the reference’s provenance, continuation/gate semantics, and the optimizer-handoff amendment. Retaining an architecture value does not authorize changing its initialization contract. [`pinn_architecture.md:445`, `pinn_architecture.md:184`; `RESEARCH-CONTEXT-MASTER.md:381`]
2. **The distinction between exponent normalization and loss normalization.** The suggested recipe changes the former only. Preserve the residual’s $1/3$ factor, frame, and locked multiplier schedule. [`pinn_architecture.md:429`, `pinn_architecture.md:656`, `pinn_architecture.md:683`]
3. **Complete controller state.** Checkpoint $C,\gamma_j,N$, continuation level, random-state information, front-monitoring state, optimizer phase, and consumed budget.
4. **Diagnostics before clipping or aggregation hides information.** Log raw residual distributions, full-prefix extrema, unclipped exponents, floor counts, front time/fraction, raw and weighted losses, and term-gradient statistics. The existing contract already requires weighted-loss/gradient evidence before automatic dominance control. [`pinn_architecture.md:690`]
5. **Four separate meanings of success:** numerical non-saturation; causal-front opening; satisfying a continuation level; and acceptable trajectory accuracy. None automatically implies the next.
6. **A stable L-BFGS surrogate and explicit halt rules.** Freeze its objective inputs and weights; do not interpret coefficient changes as optimizer progress.
7. **The preserved held-out boundary.** Training diagnostics must not draw on the single unspent evaluation. No automatic evaluation, advancement after failed gates, or uncommissioned experiment follows from this report. [`ctl_instruction.md:1987`; `RESEARCH-CONTEXT-MASTER.md:381`]

---

## 3. Fill-in decision sheet

All suggested defaults are [A], pending owner ratification. Selecting a different D6 mechanism can make some D1/D2/D5 choices inapplicable; the owner’s selections should be recorded as a compatible bundle.

| Decision | Options | Suggested default | Door type | Owner’s pick |
|---|---|---|---|---|
| D1 — Exponent control | A: normalized-prefix continuation; B: fixed coefficient; C: log compression | **A**, $\gamma_0=2$, declared continuation and terminal criterion | A/B/C: two-way; each needs its stated contract/gate treatment | _____ |
| D2 — Reference and normalization location | A: fixed $C$, exponent only; B: equivalent coefficient without explicit $C$; C: normalize outer loss too; D: online reference | **A**, $C=2.60\times10^{10}$, frozen | All two-way mechanically; C changes loss balance, D adds controller state | _____ |
| D3 — Initialization scale | A: retain 30; B: fresh 10; C: fresh 1 | **A** | A: two-way; B/C: one-way for run lineage | _____ |
| D4 — Count and unit | A: 4096/sequence; B: 2048/sequence; C: 16/sequence diagnostic | **A**, subject to resource and full-prefix qualification | All two-way; coefficient/count normalization must remain coupled | _____ |
| D5 — Clip semantics | A: dtype normal-floor guard; B: float64 path; C: semantic low cap | **A**, float32 $B=87.33654$ | All two-way mechanically; C invalidates the old front interpretation | _____ |
| D6 — Curriculum family | A: composed continuation; B: growing prefix; C: no causal weighting; D: unmodified Causal R3 | **A** | A/C: two-way; B/D: practically one-way protocol changes | _____ |
| E — Next research expenditure | E1: initialization characterization; E2: bounded trial; E3: matched alternatives | **E1 first**; E2 only after separate authorization | E1: two-way; E2/E3: one-way expenditure | _____ |

---

## 4. Gaps

1. **Full initialization profiles are missing.** Six medians cannot bound all residuals or cumulative prefixes at 4096 points. The proposed $C$ and $\gamma_0$ therefore have conditional numerical support, not empirical qualification. [P/A: `2026-08-17-residual-frame-conformance-audit.md:151`]
2. **No converged-PINN absolute residual reference is established.** Gate B is a reference-trajectory consistency check. It cannot fix a converged-scale normalizer or connect a residual tolerance to trajectory error. [P/A: `2026-08-17-residual-frame-conformance-audit.md:109`]
3. **There is no measured response to alternative initialization scales.** The frequency table above is conditional analysis; the stack’s Jacobian/Hessian contributions have not been separated. [P/A: `RESEARCH-CONTEXT-MASTER.md:301`, `RESEARCH-CONTEXT-MASTER.md:311`]
4. **The baseline has post-initialization evidence; the proposed recipe does not.** The 502-step record must not be confused with evidence about continuation, normalized prefixes, or a redesigned curriculum. [P: `2026-08-17-residual-frame-conformance-audit.md:125`; `RESEARCH-CONTEXT-MASTER.md:309`]
5. **No finite upper bound for future residuals is established.** Optimization can create derivative spikes or close encounters outside the sampled initialization cases. The range table is not a guarantee of monotonic decay or bounded maxima. [A]
6. **Count units, computational feasibility, and complete execution constants remain unresolved.** Per-batch versus per-sequence count matters; the attachments do not establish memory capacity for the proposed dense configuration or reproduce every authorized optimizer constant. [P/A: `ctl_instruction.md:1815`, `ctl_instruction.md:1840`]
7. **Exact runtime front aggregation and tie handling were not inspected.** The derivations use the audit’s $R_1<\log2$ implication. A future implementer must reconcile the proposed controller with actual gate definitions before claiming conformance. [P/A: `2026-08-17-residual-frame-conformance-audit.md:126`]
8. **Gradient disappearance and optimizer consistency remain empirical questions.** The global norm ratio does not show componentwise rounding, and the attachments do not establish L-BFGS weight-refresh behavior. [P/A: `2026-08-17-residual-frame-conformance-audit.md:134`; `pinn_architecture.md:698`]
9. **The proposed $10^{-4}$ training-control tolerance is not validated.** It borrows a provisional number while changing its aggregation and role. Achievability, appropriate IC requirements, and its relationship to trajectory accuracy remain open. [P/A: `ctl_instruction.md:1966`, `ctl_instruction.md:1969`]
10. **H-01 is only summarized.** A full adjudication of the earlier Q3 requires its actual text; this report assesses the interpretation supplied in the master. [P: `RESEARCH-CONTEXT-MASTER.md:289`] [r2-QUAL]
11. **Literature transfer is not project validation.** The causal formula matches L1, but the project supplies no attribution trail. Algorithm details were checked in the public preprint; no claim is made that this report inspected the journal’s complete implementation. L4 supports the redesign family, not the proposed prefix count or threshold. [L/A]
12. **Additional live implementation contradictions are outside this report’s verification claim.** Repository inspection was waived. That limits conformance claims; it does not prevent the calculations and candidate dispositions above.

---

## 5. Claims-and-uncertainty register

| Claim | Evidence base | Confidence and limit |
|---|---|---|
| The pinned formula combines a raw residual prefix, $\eta_c=1$, detached weights, and outer averaging. | **[P]** `pinn_architecture.md:435`, `pinn_architecture.md:440`, `pinn_architecture.md:445` | High confidence in the supplied contract; not live implementation verification. |
| The reported run halted with no front advancement across 502 logged steps. | **[P]** `52-DIAG-05-REDERIVATION.md:58` | Established within the closure record; does not prove failure for every budget. |
| Gate B is not a converged-network measurement. | **[P/A]** `2026-08-17-residual-frame-conformance-audit.md:109`; `52-DIAG-05-REDERIVATION.md:83` | Direct contradiction between supplied descriptions; the audit identifies the actual measured object. |
| The first-point floor and advancement thresholds differ by a factor of 126. | **[A]** $126\log2/\log2$ | Exact under the specified normal-floor and 0.5 conditions. |
| Endpoint prefixes change by 273 between 16 and 4096 equal-residual samples. | **[A]** $4095/15$ | Exact for the stated profile; arbitrary sampled profiles need their actual sums. |
| Fixed exponent normalization and inverse coefficient scaling are equivalent. | **[A]** $z=\eta P/C$ | Exact for weights; not equivalent to normalizing the outer loss. |
| Residual scale changes as $\omega^4$. | **[A]**, informed by **[L3]** | Conditional heuristic only; not validated for this stack or near force cancellation. |
| L1 supplies coefficient continuation and a weight-based stopping criterion. | **[L1]** §3, Algorithm 1 | Directly checked in the public preprint; not a universal numerical calibration. |
| The proposed defaults avoid both forms of initial saturation in the illustrated profiles. | **[A]**, using **[P]** residual summaries | Algebraically supported for those profiles; actual full vectors remain unmeasured. |
| The proposed defaults will train an accurate three-body predictor. | **No supporting outcome evidence** | Unknown. This report makes no such claim. |
| Growing-prefix training removes the need for residual-exponential activation at initialization. | **[A]**; family supported by **[L4]** | Mechanically true for active weights set to one; convergence and accuracy remain unproven. |
| Severe gradient imbalance is reported, but complete data-gradient loss is proven. | **[P/A]** `2026-08-17-residual-frame-conformance-audit.md:132`, `2026-08-17-residual-frame-conformance-audit.md:134` | First clause supported; second clause not established. |
| The held-out evaluation must remain owner-governed and unspent by this work. | **[P]** `RESEARCH-CONTEXT-MASTER.md:381` | Preserved throughout this report’s work and proposals. |

### Literature cited

- **[L1]** Sifan Wang, Shyam Sankaran, and Paris Perdikaris. **“Respecting causality for training physics-informed neural networks.”** *Computer Methods in Applied Mechanics and Engineering*, 421, 116813, **2024**. [DOI](https://doi.org/10.1016/j.cma.2024.116813). Protocol checked in the public **2022** preprint, **“Respecting causality is all you need for training physics-informed neural networks,”** §3 and Algorithm 1: [arXiv:2203.07404](https://arxiv.org/abs/2203.07404).
- **[L2]** Sifan Wang, Shyam Sankaran, Hanwen Wang, and Paris Perdikaris. **“An Expert’s Guide to Training Physics-informed Neural Networks.”** *CoRR/arXiv preprint*, **2023**, §5.1. [arXiv:2308.08468](https://arxiv.org/abs/2308.08468). This source is a preprint, not presented here as a peer-reviewed journal article.
- **[L3]** Vincent Sitzmann, Julien N. P. Martel, Alexander W. Bergman, David B. Lindell, and Gordon Wetzstein. **“Implicit Neural Representations with Periodic Activation Functions.”** *Advances in Neural Information Processing Systems*, 33, 7462–7473, **2020**. [Paper](https://arxiv.org/abs/2006.09661).
- **[L4]** Michael Penwarden, Ameya D. Jagtap, Shandian Zhe, George Em Karniadakis, and Robert M. Kirby. **“A unified scalable framework for causal sweeping strategies for Physics-Informed Neural Networks (PINNs) and their temporal decompositions.”** *Journal of Computational Physics*, 493, 112464, **2023**. [DOI](https://doi.org/10.1016/j.jcp.2023.112464). The claims used here are limited to its stated framework and research scope.
- **[L5]** Arka Daw, Jie Bu, Sifan Wang, Paris Perdikaris, and Anuj Karpatne. **“Mitigating Propagation Failures in Physics-informed Neural Networks using Retain-Resample-Release (R3) Sampling.”** *Proceedings of the 40th International Conference on Machine Learning*, PMLR 202, 7264–7302, **2023**. [Paper and proceedings record](https://proceedings.mlr.press/v202/daw23a.html).

No files were edited, no training or model evaluation was performed, no specification was amended, and no remedy was ratified.

