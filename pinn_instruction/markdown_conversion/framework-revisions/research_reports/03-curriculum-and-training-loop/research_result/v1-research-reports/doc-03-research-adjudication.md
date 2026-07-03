# doc-03 Research Adjudication — Curriculum and Training Loop

**Scope:** CTL-PINN framework revision, doc-03  
**Evidence boundary:** the six attached files only  
**Status:** research findings for framework-owner disposition

## 1. Source hierarchy and adjudication standard

This adjudication applies the source treatment prescribed by `RESEARCH-CONTEXT-MASTER.md` and `scope-12-hard-constraints.md`:

1. The seven SCOPE-12 hard constraints are fixed boundary conditions.
2. `ctl_instruction.md` and `pinn_architecture.md` are the authoritative framework specifications. Their doc-03 training-loop positions are the revisable baseline, not immutable law.
3. `03-curriculum-and-training-loop.md` is the non-authoritative issue document under review. Its findings and recommended resolutions are not decisions.
4. `review_of_framework.md` and `stage_strat_revision.md` are baseline design-intent reports. They supply arguments and candidate methods, but they do not override the specs or locked outcomes.
5. Every numerical figure is treated according to `claims-register.md`. A `claimed-unverified` value remains a proposal or input claim; it is not promoted to fact by this adjudication.
6. Citations to live implementation code inside the issue document are disregarded. No conclusion below depends on a file outside the attachment set.

The locked conventions that directly constrain this report are: the 14D `[τ, IC₁₃]` input; Jacobi-state `IC₁₃`; the mass-weighted COM projection head; matched-Plummer training softening `ε_train = 10⁻⁵`; the post-v1.3 SCS/energy-gate convention; raw-mass `D = (GT²)^(1/3) ≈ 4.6416`; and the locked data-side stage-query and validation contracts.

**Primary sources:** `RESEARCH-CONTEXT-MASTER.md`, “Source-Treatment Preamble”; `scope-12-hard-constraints.md`, §§1–3; `claims-register.md`, “The no-in-milestone-verification boundary” and “Claims Table.”

---

## 2. Executive disposition matrix

| Question | Disposition | Principal correction or outcome |
|---|---|---|
| Causal-training mode | **OWNER DECISION — unresolved** | The issue document misstates Option B as the current SOT. The current spec baseline is causal weighting with dense-residual ALM rejected. |
| `s_min` frame | **OWNER DECISION — unresolved** | Reframe the choice around an unsoftened versus softened *stage gate*. The training loss uses matched-Plummer pair distances, not `max(s_min, ε)`. |
| Epsilon strategy | **OWNER DECISION — unresolved open part** | `ε_train = 10⁻⁵` is locked. Only static/invariant `ε_inv` remains open. Unifying all contexts at `10⁻¹⁰` is out of bounds in this milestone. |
| B-07 replay/lookahead | **CONFIRM STRUCTURE; NUMBERS PROVISIONAL** | Use locked stage-query APIs and explicit replay/lookahead sampling. Do not treat 240/16 and 32 as empirically verified constants. |
| B-08 independent point sets | **CONFIRM, WITH CORRECTIONS** | Separate snapshot data points from continuous collocation points. Data loss is Huber, not L1; 8192 and 4096 are design defaults/examples, not facts. |
| M6 `L_norm` clamp | **REVISE ISSUE FINDING** | `L_norm` is metadata, not an `IC₁₃` slot. Preserve raw diagnostics; optionally expose a clipped feature rather than silently overwriting the physical ratio. |
| M7 `τ_L` exclusion | **CONFIRM** | `τ_L` remains staging/evaluation metadata and is excluded from the locked 14D input. |
| M14 gradient clipping | **CONFIRM MERGED FORM; CALIBRATE `C`** | Use `C_stage × rolling median`; interpret the PINN’s fixed 5.0 as a fallback/default, not a second multiplier. Do not canonize 8.5. |
| M15 energy-loss weights | **REJECT ISSUE FIX** | Current PHYS-05 weights peak at 1, not 1000. The cap table addresses a stale schedule and is unsupported. Retain PHYS-05 warmup pending evidence. |
| M16 `dt_out` scaling | **INSUFFICIENT EVIDENCE; DO NOT ADOPT** | `dt_base/dt_out` gives *fewer* collocation points to lower-resolution trajectories, contrary to the issue document’s stated motivation. `dt_out` heterogeneity alone does not determine a collocation law. |
| D5 stage transition | **REVISE** | Add calibrated operational fallbacks, but do not let max epochs, stagnation, or NaN automatically advance a stage. Separate ADVANCE, RECOVER, and HALT/REVIEW outcomes. |
| NS-12 componentwise AD | **CONFIRM RESOLVED** | The current PHYS-02 contract already requires componentwise first and second derivatives and forbids differentiating a summed 9D output. |
| NS-13 Huber `δ_E` | **INSUFFICIENT EVIDENCE TO CHANGE** | Keep `δ_E = 1.0` as configurable baseline; calibrate from training-split normalized energy-drift statistics before adopting another value. |
| NS-18 scaling contract | **CONFIRM, WITH CURRENT-SPEC TERMS** | All losses use scaled projected positions, raw masses, normalized time, matched softening, and componentwise AD. Use Huber data loss and include IC/angular-momentum terms. |
| Adaptive stage assignment | **REVISE SUBSTANTIALLY** | Use data-driven analysis to calibrate boundaries *within the multi-fidelity topology*; do not replace Stages 2 and 5 with undifferentiated quasi-random clusters. |
| `D` conflict | **LOCKED RESOLUTION** | `D ≈ 4.6416`; rederive dimensionless dynamics under raw masses. The issue’s 6.694-based code is invalid for this framework. |
| `τ_L` / `L_max` formulas | **PARTIAL CONFIRMATION; ESTIMATOR GAP** | Keep `L_max` as a characteristic normalization, not a proven global maximum. Current Rosenstein estimator is the baseline; shadow/PCA alternatives are not sufficiently specified or validated. |
| ALM `μ_p` clamp | **RELOCATE TO OPTIONAL ABLATION; BOUNDS UNRESOLVED** | Dense-residual ALM is rejected. A clamp can apply only to a future scalar-conservation ALM after its update law and scaling are specified. |

---

# 3. Decisions requiring framework-owner approval

## 3.1 Causal-training-mode decision

### Finding

**Unresolved by design; framework-owner approval remains required.** All three modes must remain on the decision record, but the issue document’s account of the baseline is materially wrong.

### Correct baseline

The current specifications already use per-time-ordered causal weighting:

\[
 w_n = \exp\!\left[-\eta_c \sum_{m<n}\operatorname{stopgrad}(\bar R_m)\right],
 \qquad w_1=1,\qquad \eta_c=1.
\]

They also reject the pseudo-ALM expression that squares a nonnegative dense physics MSE, and they permit ALM only as an optional P2 ablation on scalar energy and angular-momentum constraints. Thus:

- **Option A — per-time-step causal weighting:** closest to the current PHYS-05 baseline. Its unresolved implementation gap is the causal-exponent clipping bound and the behavior near early close-encounter stiffness.
- **Option B — global sampling + ALM:** not the current SOT as described by the issue document. Global *sampling* is compatible with later time-ordering and causal weights; removing causal weights is a separate change. Reintroducing ALM on the dense ODE residual would directly conflict with the current spec. An owner choosing B must define whether “ALM” means only the permitted scalar-constraint ablation or a deliberate reversal of the dense-residual rejection.
- **Option C — time-windowed causal-ALM hybrid:** not specified sufficiently for adoption. It needs a precise window schedule, overlap, advancement gate, state-transfer contract, checkpoint semantics, and a statement of whether ALM remains scalar-only. Calling it a resolution of both failure modes is an unverified architectural hypothesis.

### Conflict

`03-curriculum-and-training-loop.md` says Option B is the current CTL/PINN SOT. `ctl_instruction.md` and `pinn_architecture.md` instead make causal weighting the default and explicitly reject dense-residual pseudo-ALM. The issue document therefore cannot be used to characterize the status quo.

### Uncertainty / claims-register gap

No attached material reports an A/B/C ablation, a failure-rate comparison, a validated causal-exponent bound, or an executable Option-C window contract. The owner can choose a design direction, but the evidence package cannot establish which mode trains best.

### Source basis

- `framed-research-questions.md`, “The causal-training-mode decision.”
- `ctl_instruction.md`, “Data Flow During Training” and “Phase 2: Total Training Loss,” especially the PHYS-05 causal-weighting and pseudo-ALM-rejection paragraphs.
- `pinn_architecture.md`, §§3.2, 4.1, and 4.2.
- `03-curriculum-and-training-loop.md`, “Causal Training Mismatch” and “Open Decisions” — treated as the non-authoritative opposing position.

**Figure grounding:** no CLM figure determines this verdict.

---

## 3.2 `s_min`-frame decision

### Finding

**Unresolved owner decision, but the options require technical correction before approval.** The meaningful choice is whether the curriculum gate uses the true geometric separation or a softened separation. The current training loss does not contain a separate scalar “collision criterion” based on `max(s_min, ε)`.

### Correctly framed options

- **Option A:** compute and log unsoftened
  \[
  s_{\min}=\min_{i<j}\|r'_i-r'_j\|
  \]
  for stage assignment and diagnostics; independently use the locked matched-Plummer distance
  \[
  r_{\mathrm{safe},ij}=\sqrt{\|r'_i-r'_j\|^2+\varepsilon_{\mathrm{train}}^2}
  \]
  in the training force and energy terms.
- **Option B:** define a softened separation for the stage gate as well, while retaining matched-Plummer training losses. The owner must specify whether the gate uses the static `ε_inv` or the training `ε_train`; that choice interacts with the separate epsilon-strategy decision.

The expression `max(s_min, ε)` should not be inserted into the force or potential. It is neither the locked Plummer form nor a substitute for pairwise regularization.

### Conflict

The spec baseline is internally clear: `ctl_instruction.md` computes `s_min` from true pairwise separations, while `pinn_architecture.md` softens pairwise distances inside force and energy. The issue document reaches a similar qualitative split but describes a “training-loss collision criterion” and uses `max`, which is not the governing PHYS-03 form.

### Uncertainty / claims-register gap

The attachments contain no sensitivity study showing how a softened gate would change Stage-6 membership or whether the current `s_min` threshold remains meaningful under either softening convention.

### Source basis

- `framed-research-questions.md`, “The s_min-frame decision.”
- `ctl_instruction.md`, Step 3 item 1 and Stage 6 criteria.
- `pinn_architecture.md`, §§3.2 and 3.4.
- `scope-12-hard-constraints.md`, item 4.
- `03-curriculum-and-training-loop.md`, D-05 / “Open Decisions” — non-authoritative proposal.

**Figure grounding:** no CLM figure settles the frame choice.

---

## 3.3 Epsilon-strategy decision

### Finding

**The open part remains unresolved.** The loss-side value and form are not open:

\[
\varepsilon_{\mathrm{train}}=10^{-5},\qquad
r_{\mathrm{safe}}=\sqrt{r^2+\varepsilon_{\mathrm{train}}^2}
\]

must be used identically in the physics residual and energy regularizer. The owner is deciding only the static/invariant context.

### Options under the hard constraint

- **Option A — collapse static invariants to `10⁻⁵`:** changes offline `E`, `Q`, and any stage assignment depending on them. It requires invariant recomputation and stage recalibration.
- **Option B — dual context:** retain `ε_inv=10⁻¹⁰` for offline invariant computation and the locked `ε_train=10⁻⁵` for training. This is the current framework-spec baseline.
- **Option C — `10⁻¹⁰` everywhere:** cannot be adopted in this milestone because it contradicts locked hard constraint 4. It may be listed for historical completeness only.

### Conflict

`review_of_framework.md` argues for `10⁻⁵` in all calculations, while `ctl_instruction.md` explicitly distinguishes `ε_inv=10⁻¹⁰` from `ε_train=10⁻⁵`. The baseline report also uses additive distance softening in places, which is prohibited by PHYS-03. Its statement that `10⁻¹⁰` is “numerically indistinguishable from zero” is not established by the attached evidence and conflates numerical representation with the separate question of whether the regularization is physically effective at the dataset’s separation scale.

### Uncertainty / claims-register gap

No attached distribution of admitted minimum separations and no A/B invariant sensitivity table shows how often `ε_inv=10⁻¹⁰` versus `10⁻⁵` materially changes `E`, `Q`, or a stage label. That empirical comparison is what would resolve the open part.

### Source basis

- `scope-12-hard-constraints.md`, item 4 and §3.
- `framed-research-questions.md`, “The epsilon-strategy decision.”
- `ctl_instruction.md`, Step 3 item 1 and “Numerical notes and defaults.”
- `pinn_architecture.md`, §§3.2 and 3.4.
- `review_of_framework.md`, §2.2 — baseline argument, not authority.
- `03-curriculum-and-training-loop.md`, D-06 — non-authoritative statement of the conflict.

**Figure grounding:** the two epsilon values are framework parameters, not dataset CLM rows; `claims-register.md` explicitly classifies them as non-dataset figures.

---

# 4. Batch construction and point-set contracts

## 4.1 B-07 — replay/lookahead batch construction

### Finding

**Confirm the sampler architecture; retain the numerical split as a provisional default rather than an empirically grounded constant.**

The training loop should consume the locked data-side interfaces:

- `sample_replay(n, max_stage=k)` from admitted trajectories in stages `0…k`;
- `sample_lookahead(n, stage=k+1)` only when the next stage exists;
- `has_stage(k)` before any stage-specific query.

For a configured trajectory batch `B`, define a configurable lookahead fraction `ρ_lookahead`, then derive the integer replay/lookahead counts deterministically. The current example `B=256`, `B_replay=240`, `B_lookahead=16` may remain the default configuration, but not a universal fixed law.

For each selected trajectory, the current spec’s snapshot-data rule is coherent:

\[
n_{\mathrm{pts}}(j)=\min(n_{\mathrm{pts,cap}},n_{\mathrm{snapshots}}(j)),
\]

with draws without replacement, split between acceleration-weighted and uniform snapshot times. The default cap `32` is explicitly labeled “not evidence-based” in the spec and must remain configurable.

### Required unresolved edge cases

The attached material does not settle:

- what to do at the final stage when no `k+1` exists;
- what to do when `has_stage(k+1)` is false or a next-stage pool is too small;
- whether trajectory sampling itself is with or without replacement;
- whether duplicate trajectories may appear across replay/lookahead pools after stage relabeling;
- how to preserve stage balance inside the cumulative replay pool.

The spec should prohibit silent failure and require an explicit policy, but this adjudication does not invent the policy.

### Conflict

The issue document bases B-07 partly on live-code behavior, which is excluded by SCOPE-12. The finding survives only as a spec-level need to make the existing replay/lookahead contract executable. The exact 240/16/32 values do not become verified merely because both the issue document and current spec contain them.

### Source basis

- `scope-12-hard-constraints.md`, item 7 and §2.
- `ctl_instruction.md`, “Data-side stage-query interface” and “Mini-Batch Construction with Lookahead Sampling.”
- `framed-research-questions.md`, B-07.
- `review_of_framework.md`, §5.2 — supporting design intent.
- `03-curriculum-and-training-loop.md`, B-07 / unified batch specification — non-authoritative candidate.

**Figure grounding:** CLM-12 (`240/16`, `8192/4096`) is `claimed-unverified`. CLM-16 verifies only median snapshot counts of 61 standard, 127 hierarchical, and 1003 gold; those medians do not prove a point cap or batch ratio.

---

## 4.2 B-08 — data-fidelity versus collocation separation

### Finding

**Confirm two independent point sets, with three corrections.**

1. **Data-fidelity points** are discrete BRUTUS snapshot times selected per trajectory. They supervise scaled, COM-projected positions using the current **Huber** data loss, not L1/MAE.
2. **Collocation points** are independently sampled continuous normalized times. They feed componentwise AD and the physics residual. The same collocation set should be reused for the energy regularizer to avoid an unnecessary second forward/AD graph unless an explicit ablation says otherwise.
3. The numerical totals are not hard facts. With `B=256` and every trajectory contributing 32 points, the maximum data count is 8192; the actual total is
   \[
   N_{\mathrm{data}}=\sum_{j=1}^{B}\min(32,n_{\mathrm{snapshots}}(j)),
   \]
   so it can be smaller. `N_col=4096` is a current design default/example, not a verified optimum.

### 50/50 ambiguity

The current CTL spec clearly defines a 50/50 acceleration-weighted/uniform composition for **snapshot data points**. The current PINN collocation contract allows uniform and adaptive sampling, but the attachment set does not define a canonical mixed continuous-time sampler or establish that collocation must also be 50/50. The issue document’s “both 50/50” statement therefore remains unproven and ambiguous.

### Conflict

The issue document says data loss is L1 and fixes exact 8192/4096 counts. `pinn_architecture.md` supersedes the L1 prose with Huber and presents the collocation count as a design setting. The spec-level separation is valid; the issue document’s exact implementation prescription is not fully valid.

### Source basis

- `pinn_architecture.md`, §§3.1, 3.2, and 3.4.
- `ctl_instruction.md`, “Mini-Batch Construction with Lookahead Sampling.”
- `framed-research-questions.md`, B-08.
- `review_of_framework.md`, §5.1.
- `03-curriculum-and-training-loop.md`, B-08 / unified batch specification — non-authoritative proposal.

**Figure grounding:** CLM-12 is `claimed-unverified`. CLM-16’s verified medians correct the issue document’s approximate snapshot counts (CLM-13), but they do not validate either batch total.

---

# 5. Invariant metadata and network-input questions

## 5.1 M6 — `L_norm` clamping

### Finding

**Revise the issue finding.** The alleged problem “before IC-vector mapping” is obsolete under the locked Jacobi-state `IC₁₃`: `L_norm` is no longer a network input component. It is staging/evaluation metadata.

A silent clamp of the sole stored value is not advisable because `L_norm>1`, a negative/nonfinite value, or a nearly zero `L_max` can reveal a bad energy convention, a degenerate denominator, or the fact that this `L_max` is only a characteristic scale. The safer contract is:

- persist `L_norm_raw = L/L_max` and a validity flag;
- reject or flag nonfinite inputs and near-zero denominators;
- where a bounded feature is explicitly required for clustering or visualization, derive a separate `L_norm_clipped = clip(L_norm_raw,0,1)` and record that transformation;
- do not overwrite the raw diagnostic.

### Conflict

The issue document assumes `L_norm` is still mapped into the IC vector and recommends clipping before `2x−1`. The locked input contract excludes it. The current `ctl_instruction.md` reference function also adds small epsilons inside the square root and denominator without a fully specified degeneracy policy; that implementation detail should be revised independently of the conceptual formula.

### Uncertainty / claims-register gap

No attached empirical distribution shows how often `L_norm_raw` lies outside `[0,1]`, how those cases relate to `E≈0`, or whether the existing stage thresholds are sensitive to clipping.

### Source basis

- `scope-12-hard-constraints.md`, items 1–2.
- `ctl_instruction.md`, Step 3 item 2 and Step 4 “Network input contract.”
- `framed-research-questions.md`, M6.
- `03-curriculum-and-training-loop.md`, M6 — stale issue framing.

**Figure grounding:** no CLM figure determines the clamp policy.

---

## 5.2 M7 — `τ_L` excluded from `IC₁₃`

### Finding

**Confirm exclusion by design.** The network input is exactly `[τ, IC₁₃]`, where `IC₁₃` is the locked fixed-gauge Jacobi-state encoding. `τ_L` is trajectory-derived difficulty metadata, not a member of that input vector.

It remains available for:

- stage assignment, subject to the estimator decision below;
- curriculum diagnostics;
- post-training evaluation and stratified reporting.

Adding it to the input would violate hard constraints 1 and 2 and would also leak a quantity computed from the full target trajectory into a model intended to condition on initial state.

### Source basis

- `scope-12-hard-constraints.md`, items 1–2.
- `ctl_instruction.md`, Step 3 outputs and Step 4 “Network input contract.”
- `framed-research-questions.md`, M7.
- `03-curriculum-and-training-loop.md`, M7 — its proposed exclusion is consistent with the locked contract.

**Figure grounding:** none.

---

# 6. Optimization and loss-scaling questions

## 6.1 M14 — gradient-clipping divergence

### Finding

**Confirm the merged functional form:**

\[
C_{\mathrm{clip}}(k,i)=C_k\,\operatorname{median}\{\|g\|_{i-h+1},\ldots,\|g\|_i\},
\]

followed by global-norm clipping during Adam only. The rolling window is currently 100 observations.

The fixed `5.0 × median` in `pinn_architecture.md` should be interpreted as the stage-agnostic default/fallback. It should not be multiplied again by the CTL factor. Once a stage schedule is active, `C_k` replaces the fixed 5.0.

### Numerical status

- The CTL baseline gives `C=7–10` for Stages 0–1, `5` for 2–3, and `3` for 4–6.
- The issue document converts the early-stage range to `8.5`. That midpoint is CLM-10 and is `claimed-unverified`; it should not be canonized.

The executable specification still needs a chosen early-stage value or calibration rule, a bootstrap rule before the history window is populated, a finite lower floor, and a decision on whether gradient history resets at stage boundaries. Those details are absent.

### Conflict

The two specs contain complementary rather than mutually exclusive mechanisms. The issue document is correct to merge them structurally but overreaches by presenting 8.5 as settled.

### Source basis

- `pinn_architecture.md`, §4.4.
- `ctl_instruction.md`, “Adaptive Median-Based Gradient Clipping.”
- `framed-research-questions.md`, M14.
- `review_of_framework.md`, §5.4 — candidate midpoint, not authority.
- `03-curriculum-and-training-loop.md`, “Gradient Clipping — Merged Specification.”

**Figure grounding:** CLM-10 (`8.5/5/3`) is `claimed-unverified`. The spec schedule `7–10/5/3` is a revisable framework parameter, not an empirical CLM fact.

---

## 6.2 M15 — energy-loss weight schedule

### Finding

**Reject the issue document’s capped-hybrid replacement.** Its premise is stale: the current PHYS-05 schedule does not set `λ_E=1000` at Stage 6.

The current maxima are:

\[
\lambda_E^{\max}(k)=
\begin{cases}
0, & k\in\{0,1\},\\
10^{k-4}, & k\in\{2,3,4\},\\
1, & k\in\{5,6\},
\end{cases}
\]

with linear warmup over `I_warm = min(2000, 0.1 N_Adam,k)`. Thus the maximum is 1, not 1000 or 500.

The issue cap table `{1,5,20,50,100,200,500}` would increase several current weights by orders of magnitude and has no attached empirical support. It should not replace PHYS-05.

### Dominance safeguard

A diagnostic for weighted loss or gradient dominance is reasonable, but the issue document does not supply a coherent settled rule: one passage compares `λ_E L_E` to `10 L_data`, while another halves the weight when `L_E<0.01`. Neither accounts for physics, IC, or angular-momentum terms. The spec may require logging per-component weighted losses and gradient norms; automatic reweighting requires calibration and should not be invented here.

### Source basis

- `pinn_architecture.md`, §4.1.
- `ctl_instruction.md`, “Phase 2: Total Training Loss.”
- `framed-research-questions.md`, M15.
- `03-curriculum-and-training-loop.md`, M15 / “Energy Loss Weight Schedule.”

**Figure grounding:** CLM-11, the cap table, is `claimed-unverified` and conflicts with the current PHYS-05 baseline.

---

## 6.3 M16 — `dt_out`-aware collocation scaling

### Finding

**Do not adopt `n_col ∝ dt_base/dt_out` on the present evidence.** Preserve `dt_out` and `n_snapshots` as loader metadata and leave the scaling hook open for a controlled experiment.

### Why the proposed direction is not justified

The verified output cadences are `0.17` standard base, `0.08` hierarchical base, and `0.01` gold. The proposed rule gives factors `0.059`, `0.125`, and `1` respectively. It therefore allocates *fewer* collocation points to lower-output-resolution trajectories. That is opposite to the issue document’s stated motivation that lower-resolution trajectories have fewer ground-truth snapshots and might need additional physics constraints.

Moreover, collocation points enforce the differential equation continuously and are independent of where BRUTUS snapshots occur. Heterogeneous `dt_out` proves heterogeneous data supervision; it does not by itself prove that physics-collocation density should be proportional to either `dt_out` or its inverse.

### What is missing

A valid rule first needs a declared objective, such as:

- equal collocation compute per trajectory;
- equal total supervision points per trajectory;
- compensation for sparse data labels;
- equal physical-time coverage;
- or prioritization of high-resolution/close-encounter trajectories.

It then needs caps, a compute budget, and an ablation against constant collocation. The inverse `dt_out/dt_base` is a different methodology and is not adopted here either.

### Conflict

`review_of_framework.md` says mixed-resolution data requires no special collocation handling; the issue document prescribes a scaling rule; the current specs intentionally defer the decision. The attachments do not resolve that disagreement empirically.

### Source basis

- `ctl_instruction.md`, “Data-side stage-query interface” and the forward-interface note in “Mini-Batch Construction.”
- `framed-research-questions.md`, M16.
- `review_of_framework.md`, §5.3.
- `03-curriculum-and-training-loop.md`, M16 / P3-9.
- `verified-facts-reference.md`, VF-1 and VF-2.

**Figure grounding:** CLM-17 `dt_out` values are `verified`; CLM-20’s scaling factors and the scaling law itself are `claimed-unverified`. CLM-16 verifies median snapshot counts 61/127/1003; it does not validate a collocation formula.

---

## 6.4 D5 — stage-transition criteria and fallback

### Finding

**Revise the current strict-only transition rule, but reject automatic fallback advancement.**

The current validation criterion `L_val(i) ≤ min_{j≤i} L_val(j)` effectively requires the current checkpoint to tie or set the stage’s best validation loss. It is brittle but not mathematically impossible. A percentile or patience-based stability condition is a reasonable candidate, yet the package contains no calibration.

The issue document’s Path B mixes three different events and labels all of them “advance” triggers. They must instead be separated:

- **ADVANCE:** only when a documented success gate is met.
- **RECOVER:** NaN/Inf causes rollback, learning-rate adjustment, and a bounded retry policy; it is not stage success.
- **HALT / OWNER REVIEW:** max epochs or prolonged stagnation stops the stage and records a non-convergence condition. Whether to advance with a degraded checkpoint is a separate owner decision, not an automatic branch.

A Stage-0 pilot is appropriate to estimate attainable plateau, validation, physics, and energy metrics. Until that pilot exists, retain current thresholds as baseline configuration and mark candidate per-stage tables as provisional.

### Conflict

The issue document correctly identifies operational brittleness, but its “either strict or fallback means advance” logic can propagate an unconverged or numerically unstable model into a harder stage. The current spec acknowledges that its thresholds are theoretical but provides no failure-state machine.

### Source basis

- `ctl_instruction.md`, “Stage Transition Criteria.”
- `framed-research-questions.md`, D5.
- `03-curriculum-and-training-loop.md`, “Stage Transition Criteria (D5 — Practical Fallbacks).”

**Figure grounding:** CLM-08’s stage-dependent thresholds and CLM-09’s max-epoch table are `claimed-unverified` hypotheses. They cannot be adopted as fixed gates. The current spec constants are framework parameters, not empirical claims, and remain revisable.

---

## 6.5 NS-12 — componentwise automatic differentiation

### Finding

**Confirmed resolved in the authoritative spec.** PHYS-02 requires derivatives of every output coordinate with respect to the normalized-time autograd leaf, including second derivatives. It explicitly forbids differentiating `r.sum()` or any summed 9D output as a proxy for the coordinatewise Jacobian.

Essential chain rules are:

\[
\tau=2u-1,
\qquad
\frac{\partial r'}{\partial u}=2\frac{\partial r'}{\partial \tau},
\qquad
\frac{\partial^2 r'}{\partial u^2}=4\frac{\partial^2 r'}{\partial \tau^2},
\]

only when derivatives are actually taken with respect to `τ`. If the computation differentiates directly with respect to leaf `u`, those factors are already present and must not be applied again.

Remaining choices such as a loop versus `jacrev`/`vmap`, graph-retention policy, and memory optimization are implementation details. They do not reopen the mathematical contract.

### Source basis

- `pinn_architecture.md`, §5.3.1 and validation §10.3.
- `ctl_instruction.md`, “Data Flow During Training.”
- `framed-research-questions.md`, NS-12.
- `review_of_framework.md`, §4.3 — earlier implementation guidance, subordinate to PHYS-02.

**Figure grounding:** none.

---

## 6.6 NS-13 — Huber energy delta

### Finding

**Insufficient evidence to replace `δ_E=1.0`.** Keep it as a configurable baseline, not a scientifically validated final value.

The issue document’s `0.01–0.1` range is a plausible tuning suggestion, but no attached normalized `|ΔH|` distribution shows whether `δ=1` leaves almost all samples in the quadratic branch or whether the smaller range provides better robustness. A value cannot be adjudicated from scale intuition alone.

### Required calibration

Use only the training split to report, by stage or source stratum:

- quantiles of the normalized energy residual;
- the fraction of samples in the Huber linear branch for each candidate `δ`;
- weighted energy-gradient magnitude relative to other loss terms;
- sensitivity of validation energy drift and trajectory error.

A single global `δ` is preferable unless evidence supports stage-dependent values; changing `δ` by stage changes the loss geometry and should be explicit.

### Source basis

- `pinn_architecture.md`, §3.4.
- `framed-research-questions.md`, NS-13.
- `review_of_framework.md`, §4.4.
- `03-curriculum-and-training-loop.md`, NS-13 / Huber calibration recommendation.

**Figure grounding:** `δ=1.0` and the proposed `0.01–0.1` are framework-design parameters, not dataset CLM figures. The necessary empirical distribution is absent.

---

## 6.7 NS-18 — loss-component scaling contract

### Finding

**Confirm a unified dimensionless contract, using the current authoritative loss definitions rather than the issue document’s stale L1/ALM language.**

The required contract is:

- **Input/time:** `u=t/T` is the autograd leaf; `τ=2u−1` is the network time channel.
- **Output/frame:** apply the hard mass-weighted COM projection before any loss, residual, or metric.
- **Data:** compare projected predicted `r'` to BRUTUS `r/D` using Huber loss at discrete snapshot times.
- **Physics:** use componentwise `d²r'/du²`, raw masses, and the locked matched-Plummer force with `ε_train=10⁻⁵` at independent collocation times.
- **Energy:** evaluate normalized energy drift on the same projected predictions and collocation set, with the identical Plummer potential and raw masses.
- **Initial condition:** compare projected position and AD velocity at `u=0` in scaled units.
- **Angular momentum:** use componentwise AD velocity and scaled angular momentum with its documented denominator.
- **No linear-momentum loss:** momentum is structural through the projection head.

The issue document’s statement `d²r'/du² = 4 d²r'/dτ²` is correct only when the differentiation variable is `τ`; it must not become an unconditional extra factor.

### Source basis

- `scope-12-hard-constraints.md`, items 1–4.
- `pinn_architecture.md`, §§3.1–3.5, 4.1, and 5.3.1.
- `ctl_instruction.md`, “Data Flow During Training” and “Phase 2: Total Training Loss.”
- `framed-research-questions.md`, NS-18.
- `review_of_framework.md`, §4.1 — useful dimensional argument, but stale on some loss details.
- `03-curriculum-and-training-loop.md`, “Loss Component Scaling Contract.”

**Figure grounding:** `D≈4.6416` is verified/locked CLM-19. The loss-side `ε_train=10⁻⁵` is a hard constraint. No claimed-unverified dataset figure is needed.

---

# 7. Adaptive stage-assignment methodology

## 7.1 Finding

**Do not adopt the baseline report’s seven-stage PCA/K-means assignment as written. Adopt a constrained hybrid: data-driven calibration inside the existing multi-fidelity curriculum topology.**

### Decisive structural conflict

The current curriculum is not merely a ranking by chaos. It deliberately introduces temporal fidelity in stages:

- Stages 0–1: hierarchical base trajectories;
- Stage 2: high-resolution hierarchical counterparts of stable systems;
- Stages 3–4: quasi-random base trajectories from milder to stronger chaos;
- Stage 5: high-resolution quasi-random counterparts;
- Stage 6: extreme/near-collision or remaining cases.

`stage_strat_revision.md` instead assigns all hierarchical data to Stages 0–1 and all quasi-random data to Stages 2–6. That erases the high-resolution refinement role of Stages 2 and 5 and breaks the paired base/gold progression. This is not a boundary calibration; it is a different curriculum architecture.

### Admissible use of data-driven methods

The following is supportable:

1. Run EDA on admitted, blacklist-cleaned records, stratified by IC type and fidelity.
2. Use verified metadata and computed invariants to test whether existing fixed thresholds produce empty or severely imbalanced strata.
3. Use quantiles, robust transforms, and exploratory clustering to propose boundaries **within each source/fidelity block**.
4. Preserve paired-ID semantics when moving from base to gold. The verified quasi-random gold population is 2565 from a base population of 2749, with 184 base IDs lacking gold counterparts; the stage policy must state how those unmatched records are handled rather than pretending every base case has a gold pair.
5. Reserve a physically explicit extreme-case gate before or after clustering, but validate its effect and do not make K-means the sole safety detector.
6. Validate any ordering against actual curriculum difficulty: convergence rate, validation trajectory error, residual behavior, and close-encounter diagnostics—not PCA variance alone.

### Feature-specific adjudication

- `Q_norm = Q/s³` is physically motivated because `sampling_method.md` confirms that positions and velocities may both be scaled by sampling-time factor `s`, causing `Q` to scale as `s³`. However, the package does not establish that `s` is persisted or reconstructible for every admitted record. Until that is proved, `Q_norm` cannot be required universally.
- Use of `1/τ_L` requires explicit treatment of infinite, censored, nonpositive, and failed estimates. Replacing infinities with zero without a validity flag can conflate regular trajectories with estimator failures.
- PCA captures variance, not training difficulty. A principal component is not a difficulty score unless validated.
- K-means assumes Euclidean, roughly spherical clusters after scaling. Its cluster count and adjacency do not follow from the existence of seven curriculum stages.
- Sorting clusters by median `τ_L` reduces a multivariate clustering exercise to a single estimator whose own specification is unresolved.
- The report states hierarchical trajectories are “entirely stable”; the attachments do not verify that universal claim.
- The report proposes a 5% minimum stage population, while the issue document proposes more than 10%. Both are unverified design thresholds. Automatic merging can also destroy fidelity semantics and should not cross source/fidelity boundaries.
- The reference implementation uses synthetic dummy data and leaves population merging unimplemented. It is illustrative, not an executable stage contract.

### Population figures

The issue document’s per-stage counts (CLM-02 through CLM-07) are `claimed-unverified` and cannot validate the adaptive procedure. They must not be used to assert that the proposed clustering yields viable stages.

### Source basis

- `ctl_instruction.md`, “Multi-Stage Data Stratification by Difficulty” and Step 5.
- `stage_strat_revision.md`, Parts I–III, especially “Phase III,” “Population Control,” and the reference implementation.
- `sampling_method.md`, “Sampling-Time Size Variability.”
- `framed-research-questions.md`, “Adaptive stage-assignment methodology.”
- `03-curriculum-and-training-loop.md`, “Data-Driven Adaptive Stage Assignment.”
- `verified-facts-reference.md`, VF-3 and VF-4.

**Figure grounding:** CLM-02–CLM-07 are `claimed-unverified`; CLM-14 (184 missing gold counterparts) and CLM-15 (2565 gold from 2749 base) are `verified`.

---

# 8. The locked `D` conflict and formula reconciliation

## 8.1 `D=6.694` versus `D≈4.6416`

### Finding

**The conflict is already settled: `D≈4.6416` is mandatory.** The issue document’s `6.694` derivation and every downstream instruction that depends on it are rejected.

### Essential derivation under raw masses

Start from Newton’s equation in physical coordinates:

\[
\frac{d^2\mathbf r_i}{dt^2}
=G\sum_{j\ne i}m_j
\frac{\mathbf r_j-\mathbf r_i}{\|\mathbf r_j-\mathbf r_i\|^3}.
\]

Set

\[
\mathbf r_i=D\mathbf r'_i,\qquad t=Tu.
\]

Then

\[
\frac{d^2\mathbf r_i}{dt^2}
=\frac{D}{T^2}\frac{d^2\mathbf r'_i}{du^2},
\]

while

\[
Gm_j\frac{D(\mathbf r'_j-\mathbf r'_i)}{D^3\|\mathbf r'_j-\mathbf r'_i\|^3}
=\frac{Gm_j}{D^2}
\frac{\mathbf r'_j-\mathbf r'_i}{\|\mathbf r'_j-\mathbf r'_i\|^3}.
\]

Multiplying by `T²/D` gives

\[
\frac{d^2\mathbf r'_i}{du^2}
=\frac{GT^2}{D^3}
\sum_{j\ne i}m_j
\frac{\mathbf r'_j-\mathbf r'_i}{\|\mathbf r'_j-\mathbf r'_i\|^3}.
\]

The desired unit coefficient with **raw masses** requires

\[
D^3=GT^2,
\qquad
D=(GT^2)^{1/3}\approx4.6416
\]

for `G=1`, `T=10`. Multiplication by `M_tot` would be appropriate only after replacing raw masses by mass fractions throughout the framework, which is a rejected framework-wide rewrite.

### Consequences for the issue’s `τ_L` code

If the state is already `(r',v')` and the integrator variable is `u`, no numerical `D` is needed inside the dimensionless RHS. The code should use raw masses with unit gravitational coefficient. If a Lyapunov exponent `λ_u` is estimated per unit `u`, then

\[
\lambda_t=\lambda_u/T,
\qquad
\tau_{L,t}=1/\lambda_t=T/\lambda_u.
\]

If `λ` is estimated directly per physical time, `τ_L=1/λ`. The estimator must state which convention it uses. The issue code computes `D` and `V` but does not consistently use them, and its 6.694 value invalidates any reprocessed invariant or threshold under the locked convention.

### Stage-threshold consequence

Any thresholds calibrated using the rejected scaling cannot simply be retained. The attachments do not quantify the change in stage membership, so the required action is recomputation and calibration—not an invented conversion factor.

### Source basis

- `scope-12-hard-constraints.md`, item 6.
- `ctl_instruction.md`, §2.5.
- `claims-register.md`, CLM-01 and CLM-19 row notes.
- `verified-facts-reference.md`, VF-5.
- `framed-research-questions.md`, the worked `D` conflict.
- `03-curriculum-and-training-loop.md`, “τ_L and L_max Formula Resolution” — rejected 6.694 branch.

**Figure grounding:** CLM-19 is `verified` and locked; CLM-01 is `claimed-unverified` and explicitly rejected.

---

## 8.2 `L_max` formula

### Finding

**Retain the current formula as a characteristic normalization, but narrow its interpretation.**

\[
\mathbf L=\sum_i m_i(r'_i\times v'_i),\qquad
r_{\mathrm{char}}=\frac13\sum_{i<j}\|r'_i-r'_j\|,
\]

\[
v_{\mathrm{char}}=\sqrt{\frac{2|E|}{M_{\mathrm{tot}}}},\qquad
L_{\max}=M_{\mathrm{tot}}r_{\mathrm{char}}v_{\mathrm{char}},\qquad
L_{\mathrm{norm}}=L/L_{\max}.
\]

The attachments do not derive this as the rigorous maximum angular momentum of an arbitrary three-body configuration at fixed energy. `ctl_instruction.md` more cautiously calls it a “characteristic circular-orbit scale”; that wording should govern. Renaming the stored quantity `L_scale` would be clearer, but such a rename is a documentation/API decision.

The formula is evaluated after locked scaling with `D≈4.6416`. `D` does not appear explicitly once `(r',v',E)` are supplied, but those quantities must have been generated under the locked convention.

### Numerical guard

Do not hide degeneracy by unconditional clipping. Define behavior for `M_tot≤0`, `r_char≈0`, `|E|≈0`, or nonfinite inputs; retain a validity flag and raw ratio.

### Conflict

`review_of_framework.md` and the issue document overstate the formula as a definitive theoretical maximum, and issue pseudocode uses additive softening in energy, which is prohibited. The current spec formula is the better baseline, subject to the interpretation and guard revisions above.

### Source basis

- `ctl_instruction.md`, Step 3 item 2.
- `review_of_framework.md`, §1.1.
- `framed-research-questions.md`, “τ_L and L_max computation formulas.”
- `03-curriculum-and-training-loop.md`, “L_max Computation.”

**Figure grounding:** none beyond locked CLM-19 for the upstream scaling convention.

---

## 8.3 `τ_L` estimator

### Finding

**The package does not support a final estimator verdict. Retain the current Rosenstein-style trajectory estimator as the revisable baseline; do not adopt the issue’s shadow-trajectory code or an unspecified “PCA+Rosenstein” shortcut as canonical.**

### Current-spec baseline

`ctl_instruction.md` defines a Rosenstein-style estimator from BRUTUS position time series:

1. resample to uniform cadence;
2. construct delay coordinates;
3. choose nearest neighbors outside a Theiler window;
4. form the mean log-divergence curve;
5. fit a linear region for `λ_max`;
6. return `τ_L=1/λ_max`, with regular/nonpositive cases handled explicitly.

This is at least methodologically aligned with the data actually attached to each record and avoids integrating a second force model during preprocessing. However, key parameters remain examples or underspecified: resampling cadence, embedding dimension, delay selection, Theiler window, linear-fit interval, minimum trajectory length, and uncertainty/quality flags.

### Shadow/Benettin alternative

`review_of_framework.md` proposes a Benettin-style reference method. Such a method could serve as a calibration benchmark, but the issue document’s code is not an acceptable canonical implementation because it:

- uses rejected `D=6.694`;
- regularizes force as `||dr||³ + ε` rather than matched Plummer `(||dr||²+ε²)^(3/2)`;
- leaves time-unit semantics implicit;
- uses a thresholded/averaged divergence update that is not demonstrated to estimate the same exponent;
- relies on live-code references that are unavailable and overridden.

### “PCA+Rosenstein” claim

No attached file specifies the PCA projection, retained dimension, normalization, fit procedure, error bound, or calibration for the claimed fast approximation. It cannot enter the normative spec.

### Threshold coupling

Stage thresholds such as `τ_L>5` or `2<τ_L≤5` are estimator-dependent. They must be recalibrated if the estimator, cadence, or embedding changes. The package supplies no comparison table linking the Rosenstein and shadow methods on the admitted dataset.

### Epsilon interaction

A time-series Rosenstein estimator does not require a force-softening choice beyond the preprocessing that produced the trajectory. A shadow integrator would require the owner’s unresolved `ε_inv` choice and a matched-Plummer RHS. The perturbation `10⁻⁸` is a design parameter, not a verified optimum.

### Source basis

- `ctl_instruction.md`, Step 3 item 5 and “Numerical notes and defaults.”
- `review_of_framework.md`, §1.1.
- `framed-research-questions.md`, “τ_L and L_max computation formulas.”
- `03-curriculum-and-training-loop.md`, “τ_L Computation” — non-authoritative code and live-code reference.

**Figure grounding:** the stage `τ_L` cutoffs are current revisable spec parameters, not verified dataset figures. The issue’s numerical estimator settings are non-dataset design parameters and remain unverified.

---

# 9. ALM `μ_p` clamp

## Finding

**The issue finding is misplaced in the baseline training loop.** The default framework has no dense-residual ALM and therefore no baseline dense-physics `μ_p` to clamp.

If the optional P2 scalar-conservation ALM is implemented, a bounded penalty parameter may be a useful numerical safeguard. But `[10⁻⁴,100]` cannot be adopted from the attachments as a validated range. The update law must first define:

- which scalar constraints are included;
- normalization/units of each constraint;
- initial `μ` and whether it is shared or per constraint;
- monotone versus adaptive updates;
- dual-update cadence;
- behavior at stage boundaries;
- checkpoint persistence;
- sensitivity of the selected bounds.

Only then can a clamp be specified. It must apply outside autograd and outside L-BFGS line searches, consistent with the current optional-ALM contract.

## Conflict

`03-curriculum-and-training-loop.md` updates `λ_p` from the dense physics MSE and computes an RMSprop-like `μ_p`; this is incompatible with the authoritative rejection of dense-residual pseudo-ALM. `review_of_framework.md` likewise assumes ALM is central to the baseline, which is stale relative to PHYS-05.

## Source basis

- `pinn_architecture.md`, §§4.1–4.2.
- `ctl_instruction.md`, “Phase 2: Total Training Loss.”
- `framed-research-questions.md`, “ALM μ_p clamp.”
- `03-curriculum-and-training-loop.md`, “ALM Parameter Update Specification.”
- `review_of_framework.md`, §4.2 — earlier baseline, now subordinate.

**Figure grounding:** `[10⁻⁴,100]` is a non-dataset design parameter explicitly excluded from the CLM table; the evidence package provides no calibration.

---

# 10. Proposed specification edits

The following edits summarize the adjudicated changes without converting unverified constants into facts.

## `ctl_instruction.md`

1. Correct any prose implying global sampling means no causal weighting; cross-reference PHYS-05 explicitly.
2. Preserve the three owner-choice causal modes in a decision note, while stating that the current baseline is causal weighting and dense-residual ALM is rejected.
3. Reframe `s_min` as an unsoftened/softened gate decision; remove `max(s_min,ε)` from any loss language.
4. Keep `ε_inv` marked owner-pending if the dual-context decision is not approved; retain `ε_train=10⁻⁵` as locked.
5. Make replay/lookahead ratios and `n_pts_cap` configuration values, with 240/16/32 labeled provisional defaults. Add explicit unresolved edge-case requirements for absent/undersized next stages.
6. Distinguish snapshot sampling from collocation sampling. Do not state that both are 50/50 until a continuous-time mixed sampler is defined.
7. Store raw `L_norm`, a validity flag, and any bounded derived feature separately.
8. Replace automatic “fallback advancement” with ADVANCE / RECOVER / HALT-REVIEW states.
9. Preserve `dt_out` as metadata; do not add the proposed scaling law without an ablation.
10. Preserve multi-fidelity stage roles while allowing data-driven calibration inside source/fidelity strata.
11. State `L_max` is a characteristic normalization rather than a proved absolute maximum.
12. Retain Rosenstein-style `τ_L` as the baseline but mark all estimator parameters and quality checks requiring calibration.

## `pinn_architecture.md`

1. Retain PHYS-05 energy/angular-momentum warmup; do not add CLM-11’s cap table.
2. Merge gradient clipping by replacing the fixed factor with configurable `C_stage`; retain 5.0 as fallback and require a bootstrap/history-reset policy.
3. Keep `δ_E=1.0` configurable and add a calibration protocol rather than a guessed replacement.
4. Keep optional ALM scalar-only and OFF by default; do not add the issue’s dense-residual `μ_p` update.
5. Cross-link B-08’s independent data/collocation contract and state that energy normally reuses the physics collocation set.

---

# 11. Claims-register gap addendum

The following entries should be appended as **gap notes**, not as verified CLM figures. They record evidence missing from the attachment set and what would resolve each gap.

| Proposed gap ID | Related question / CLM | Missing evidence | What would resolve it |
|---|---|---|---|
| GAP-CTL-01 | Causal mode | No A/B/C training comparison; no causal exponent bound; no executable window contract | Controlled ablation on identical admitted splits; exact clipping/window/state-transfer specification |
| GAP-CTL-02 | `s_min` frame | No Stage-6 membership sensitivity under geometric versus softened gate | Recompute stage labels under both definitions and report changed IDs, counts, and validation behavior |
| GAP-CTL-03 | Epsilon strategy | No invariant/stage sensitivity for `ε_inv=10⁻¹⁰` versus `10⁻⁵` | Distribution of admitted separations plus per-record `ΔE`, `ΔQ`, and stage-label changes |
| GAP-CTL-04 | B-07 / CLM-12 | No empirical basis for 240/16, cap 32, or final-stage/undersized-stage behavior | Batch-ratio/cap ablation; explicit stage-availability and replacement policy |
| GAP-CTL-05 | B-08 / CLM-12 | No validated 4096 collocation budget or continuous 50/50 mixed sampler | Compute-budget ablation; exact adaptive-time density and de-duplication algorithm |
| GAP-CTL-06 | M6 | No `L_norm_raw` range, degeneracy incidence, or effect of clipping | Admitted-set histogram with nonfinite/near-zero-`L_max` audit and stage-label sensitivity |
| GAP-CTL-07 | M14 / CLM-10 | Early-stage `C` unresolved; bootstrap and history reset unspecified | Stage-0 gradient-norm traces and clipping-rate ablation across candidate `C` values |
| GAP-CTL-08 | M15 / CLM-11 | No weighted-loss or gradient dominance statistics | Per-component loss/gradient logs under PHYS-05; ablation before any automatic reweighting |
| GAP-CTL-09 | M16 / CLM-20 | Objective of `dt_out` scaling is undefined; no ablation | Compare constant, inverse-cadence, and cadence-proportional policies at fixed compute |
| GAP-CTL-10 | D5 / CLM-08–09 | Transition thresholds, epoch limits, retry limits, and degraded-checkpoint policy uncalibrated | Stage-0 pilot with full metric traces and explicit ADVANCE/RECOVER/HALT decision table |
| GAP-CTL-11 | NS-13 | No normalized `|ΔH|` distribution or Huber branch occupancy | Training-split quantiles and candidate-`δ` validation/gradient study |
| GAP-CTL-12 | Adaptive stages / CLM-02–07 | Stage populations unverified; `s` availability unclear; cluster difficulty and fidelity topology unvalidated | Admitted-set EDA, stored/reconstructed `s` audit, paired base/gold mapping, cluster stability and pilot-training validation |
| GAP-CTL-13 | `τ_L` | Rosenstein parameters, uncertainty, estimator agreement, and “PCA+Rosenstein” algorithm absent | Fully specified estimator; benchmark against a correct shadow/variational method on a representative sample; recalibrate cutoffs |
| GAP-CTL-14 | ALM clamp | Scalar-ALM update law and bound sensitivity absent | Formal scalar constraint normalization/update spec plus bound ablation |

Existing CLM statuses remain unchanged:

- CLM-01 remains rejected/`claimed-unverified`; CLM-19 remains verified and locked.
- CLM-02–CLM-13 and CLM-20 remain `claimed-unverified` where registered.
- CLM-14–CLM-19 retain their verified status.
- No unverified design figure in this report is promoted to `verified`.

---

# 12. Conflict register

1. **Causal baseline:** issue document says global+ALM; specs say causal weighting and no dense-residual ALM.
2. **Softening form:** several baseline/issue snippets use additive or `max` softening; locked PHYS-03 requires matched Plummer.
3. **Energy weights:** issue document assumes up to 1000; current PHYS-05 maximum is 1.
4. **`dt_out` rationale:** issue text argues sparse labels need attention but proposes fewer collocation points for sparse-label variants.
5. **Stage fallback:** issue labels failure/recovery events as advancement triggers.
6. **Adaptive topology:** baseline stage report removes the multi-fidelity refinement roles of Stages 2 and 5.
7. **`D`:** issue code uses 6.694; locked raw-mass convention is 4.6416.
8. **`τ_L` force:** issue shadow code uses a non-Plummer force denominator and unresolved time units.
9. **`L_max`:** reports describe a theoretical maximum without a derivation establishing that claim for arbitrary three-body states.
10. **ALM clamp:** issue applies it to dense physics loss; authoritative spec permits ALM only on optional scalar constraints.

---

# 13. Final adjudication

The framework is not blocked by a lack of candidate ideas; it is blocked by conflating current specifications, stale baseline proposals, and unverified design constants. The defensible doc-03 revision should:

- preserve all SCOPE-12 outcomes;
- correct the causal-mode baseline before the owner chooses among A/B/C;
- separate stage-gate geometry from matched-Plummer training regularization;
- make replay/lookahead and point-set separation normative while keeping their numerical budgets configurable and explicitly provisional;
- retain PHYS-05 rather than adopting the stale capped energy schedule;
- withhold the `dt_out` scaling rule and fixed stage-transition fallback tables pending empirical calibration;
- preserve the multi-fidelity curriculum topology while using EDA and clustering only as constrained calibration tools;
- rederive every formula under raw-mass `D≈4.6416`;
- treat `τ_L` estimation and optional scalar ALM as unresolved method contracts, not completed implementations.

The three owner decisions remain exactly the three designated by `framed-research-questions.md`: causal-training mode, `s_min` gate frame, and static/invariant epsilon strategy. This report does not select among those options.
