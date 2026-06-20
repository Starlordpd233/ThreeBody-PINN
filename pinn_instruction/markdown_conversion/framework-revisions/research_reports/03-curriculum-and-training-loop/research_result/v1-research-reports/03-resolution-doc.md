---
title: doc-03 Resolution — Curriculum and Training Loop (CTL-PINN)
milestone: v1.6
role: adjudication of the framed-research-questions for doc-03
status: research output (informs the framework owner's resolution doc)
created: 2026-06-18
source_baseline: 522cea7182bf3d0e3206d8faa75150e705b174f0
spec_edit_targets: ctl_instruction.md, pinn_architecture.md
format_precedent: ctl_pinn_resolution.md (v1.4), 02-resolution-doc.md (v1.5) — non-binding
---

# doc-03 Resolution — Curriculum and Training Loop

## 0. Scope, method, and how to read the verdicts

This document adjudicates the eighteen questions in `framed-research-questions.md`, working
**only** from the attached package. Each verdict states a finding, names the attached files
and sections it relies on (bare filename + section anchor), and calls out conflicts and
uncertainty explicitly. Where the sources are silent or ambiguous, the gap is logged in §8
(the claims-register addendum) rather than filled by invention. "Insufficient evidence" is
used where the sources genuinely do not support a single resolution.

Three rules govern every verdict below, per the package contract:

- **The issue doc is non-authoritative.** `03-curriculum-and-training-loop.md` is a
  consolidated audit; its "Recommended Resolutions" are adjudicated, not transcribed.
- **The framework specs are the source of truth.** Where the issue doc cites live code as
  "Canonical," that citation is overridden (`scope-12-hard-constraints.md` §2); the
  spec-edit targets `ctl_instruction.md` and `pinn_architecture.md` govern.
- **The SCOPE-12 hard constraints (items 1–7) are fixed.** They are reconciled *to*, never
  re-opened. The *current* doc-03 positions in the specs (staging, batch construction,
  transitions, loss scaling, the `tau_L`/`L_max` formulas, clipping) are the **revisable
  baseline**.

Every figure is referenced by its `CLM-NN` ID from `claims-register.md`. A
`claimed-unverified` row is an input claim, not a fact; v1.6 has **no** in-milestone phase
that verifies these (`claims-register.md`, "no-in-milestone-verification boundary"), so any
verdict that would turn on such a figure records the figure as claimed and flags it for FUT.

The verdicts are ordered as in `framed-research-questions.md` / `resolution-doc-skeleton.md`
(issue-doc section order) to ease coverage-checking. Locked sub-parts are marked **LOCKED**.

---

## 1. Decisions requiring framework-owner approval (Section 2)

These three are **posed, not decided.** Options are stated; none is recommended. For each, the
most consequential research finding is that the issue doc's framing of the *current* baseline
is partly inaccurate, which changes what each option actually costs.

### 1.1 The causal-training-mode decision -> Phase 32 / Phase 34

**Options (state all three; recommend none).**
- **A — per-time-step causal weighting:** exponential weights $w_i \propto \exp\!\big(-\lambda
  \sum_{j<i} L_j\big)$ enforce a strict arrow of time. Issue-doc risk: a "causal firewall" — an
  early stiffness spike drives later weights to zero.
- **B — global sampling + ALM:** sample time points globally from $[0,T]$, no causal weighting;
  ALM sees the full constraint-violation field. Issue-doc risk: temporal-causality violation.
- **C — time-windowed causal-ALM hybrid:** overlapping causal windows with localized ALM, hard
  convergence gating, and state propagation; an end-to-end rewrite of the Adam phase.

**Finding — the issue doc mischaracterizes the current baseline, and this is decisive.** The
issue doc (`03-curriculum-and-training-loop.md` §"Decisions Requiring Human Approval" D-04, and
§"Open Decisions") calls Option B the "current SOT." The specs do **not** support this.
`ctl_instruction.md` §"Loss Function Formulation"/"Phase 2: Total Training Loss" makes **causal
weighting the PHYS-05 default**, $w_n = \exp\!\big(-\eta_c \sum_{m<n}
\operatorname{stopgrad}(\bar R_m)\big)$ with $\eta_c = 1$ and `stopgrad` in the weights; and it
**explicitly rejects** the dense-residual pseudo-ALM $L_{\text{data}} + \lambda_p L_{\text{phys}}
+ (\mu_p/2)L_{\text{phys}}^2 + \lambda_E L_{\text{energy}}$ "because squaring a nonnegative MSE
produces a quartic residual that does not represent a standard ... augmented Lagrangian."
`pinn_architecture.md` §3.2 and §4.1 carry the same causal-weighting default, and §4.2 confines
ALM to a **P2 ablation on scalar conservation constraints only** ($c_E$, $c_{L,\alpha}$),
default OFF, dual updates only between Adam epochs and never inside L-BFGS.

Three consequences follow, all of which the owner should weigh:

1. The spec baseline already *is* Option A's mechanism. Choosing **pure Option B** (drop causal
   weighting) is a **departure from the current spec**, not a preservation of it. The issue
   doc's request to "record Option B as an intentional departure from the blueprint"
   understates the change: it is also a departure from the *spec*.
2. Option B as described relies on ALM seeing the **dense** residual field. Dense-residual ALM
   is rejected. So "global + dense ALM" is **doubly non-baseline**: with ALM confined to scalar
   constraints, the dense residual is governed by causal weighting, not ALM, and the "ALM sees
   the full violation field" rationale does not transfer.
3. The "causal firewall" risk attributed to Option A is **partially mitigated already**: the
   `stopgrad` in the weights prevents the weighting from becoming an adversarial term
   (`pinn_architecture.md` §4.1). It does not eliminate the firewall — an early spike can still
   drive $w_n \to 0$ for later $n$ — but the standard mitigation is in place. Any adoption of A
   should keep `stopgrad`.

**Open gap inside the spec (not a decision, but adjacent):** the causal-exponent underflow clip
is deliberately unset (`pinn_architecture.md` §4.1: "do not choose a numeric clipping bound in
Phase 19; surface a gap"). Logged as G-09 (§8).

**Reconciliation note.** Whichever mode is chosen, it must state its relation to the PHYS-05
causal-weighting default and the dense-ALM rejection. No dataset figure gates this decision (the
dense residual is a design constant, not a dataset-derived figure).

*Files relied on:* `03-curriculum-and-training-loop.md` (D-04, Open Decisions, Causal Training
Mismatch); `ctl_instruction.md` (Loss Function Formulation / Phase 2 Total Loss);
`pinn_architecture.md` (§3.2, §4.1, §4.2); `review_of_framework.md` (§4.2, §5.1) as the source
the issue doc reads as "Option B," and which in fact addresses point-set unification (§5.1) and
the now-rejected dense ALM (§4.2), not the causal-weighting question.

### 1.2 The `s_min`-frame decision -> Phase 32 / Phase 33

**Options.** A (spec baseline): unsoftened geometric `s_min` for the curriculum stage gate;
softened treatment inside the training-loss collision criterion; always log the unsoftened
value. B: softened everywhere.

**Finding — the spec already implements Option A; confirm it, with one precision.** The spec
separates the two cleanly: `ctl_instruction.md` §"Step 3" item 1 defines $s_{\min}$ from "true
pairwise separations (**no softening**)" — an explicitly geometric quantity — while the
loss-side potentials soften, the static invariant with $\varepsilon_{\mathrm{inv}} = 10^{-10}$
(`ctl_instruction.md` §2.5 / Step 3) and the training residual/energy with
$\varepsilon_{\mathrm{train}} = 10^{-5}$ (`pinn_architecture.md` §3.2, §3.4). The issue doc
(`03-curriculum-and-training-loop.md` D-05) agrees Option A matches the SOT and frames it as
documentation cleanup.

**Precision the owner should note.** The loss-side softening is the **LOCKED** matched-Plummer
form $r_{\mathrm{safe}} = \sqrt{\lVert \Delta r' \rVert^2 + \varepsilon^2}$ (PHYS-03,
`scope-12-hard-constraints.md` item 4), **not** the additive clamp $\max(s_{\min}, \varepsilon)$
the issue doc writes. These differ: $\max(s_{\min}, \varepsilon)$ is a floor on a *detection
threshold*; the Plummer form smoothly softens the *force/energy denominator*. Option A is
therefore precise as: unsoftened geometric `s_min` for the gate; the close-encounter handling
inside the loss is realized through the locked Plummer softening of the residual and energy, and
`max(s_min, eps)` (if used at all) is only a diagnostic/gating floor on the criterion, never a
re-softening of the residual.

This is **distinct from D5** (§3.8 below), per the framed question. Recommend none; the spec is
internally consistent with A and only needs the documentation made explicit.

*Files relied on:* `03-curriculum-and-training-loop.md` (D-05, Considered Alternatives);
`ctl_instruction.md` (Step 3 item 1, §2.5); `pinn_architecture.md` (§3.2, §3.4);
`scope-12-hard-constraints.md` (item 4).

### 1.3 The epsilon-strategy decision -> Phase 32 / Phase 35

> **LOCKED:** the **loss-side** softening is $\varepsilon_{\mathrm{train}} = 10^{-5}$, applied
> identically in the physics residual and the energy regularizer (`scope-12-hard-constraints.md`
> item 4; `claims-register.md` CLM-19 companion / PHYS-03). Not re-openable. Do not frame any
> sub-question as "which loss-side epsilon is correct."

**Open part only.** Whether a distinct **static/invariant-computation** softening
($\varepsilon_{\mathrm{inv}} = 10^{-10}$, offline, for $E$, $Q$, stage assignment) legitimately
coexists with the locked loss-side $10^{-5}$ (dual-context, Option B), versus collapsing to
$10^{-5}$ everywhere (Option A) or unifying at $10^{-10}$ (Option C).

**Finding — the spec baseline is already dual-context with the loss side locked.**
`ctl_instruction.md` §"Step 3" item 1 states $\varepsilon_{\mathrm{inv}} = 10^{-10}$ is
"context-specific for offline invariant computation and is distinct from the training-time
softening $\varepsilon_{\mathrm{train}} = 10^{-5}$"; `pinn_architecture.md` §3.4 adds a
dual-epsilon visibility note separating the data-side $\varepsilon_{\mathrm{inv}} = 10^{-10}$
from the training-time $\varepsilon_{\mathrm{train}} = 10^{-5}$. So Option B is the current
state, with the loss side fixed.

**The decisive nuance for the owner.** The issue doc grounds Option A in `review_of_framework.md`
§2.2, which mandates $10^{-5}$ "for all relevant calculations" and argues that $10^{-10}$ "is
numerically indistinguishable from zero for standard double-precision." That **value argument**
is a legitimate input. But §2.2's concrete *implementation* uses the **additive** form
$1/(\lVert r \rVert + \varepsilon)$ and $1/(\lVert r \rVert + \varepsilon)^3$ — which is
precisely the **PHYS-03 anti-pattern that is LOCKED as prohibited** (`scope-12-hard-constraints.md`
item 4; matched-Plummer required). So §2.2's *form* is superseded by the locked constraint even
though its *value* argument stands. Logged as G-08 (§8).

Weighing: Option A's double-precision argument cuts against keeping $10^{-10}$; Option B's
rationale (offline invariants computed once in float64 at maximum precision vs. on-GPU
regularization of a live loss) cuts for keeping the split. Option C ($10^{-10}$ everywhere) is
argued against by the same §2.2 double-precision point and by the spec's deliberate separation.
Collapsing the static side into $10^{-5}$ (Option A) would slightly change the computed $E$, $Q$,
and therefore stage assignment — a real, if small, side effect. Pose all three as the
**static-context reconciliation under the locked loss-side value**; recommend none.

*Files relied on:* `03-curriculum-and-training-loop.md` (D-06); `ctl_instruction.md` (Step 3
item 1, §2.5); `pinn_architecture.md` (§3.2, §3.4); `review_of_framework.md` (§2.2);
`scope-12-hard-constraints.md` (item 4); `claims-register.md` (CLM-19 companion / PHYS-03).

---

## 2. The worked seed-conflict and the `tau_L` / `L_max` formulas (Section 7)

### 2.1 `D = 6.694` vs `D ≈ 4.6416` -> Phase 32

> **LOCKED:** $D = (G T^2)^{1/3} \approx 4.6416$ (raw-mass convention, $G=1$), `CLM-19`
> (`verified`), `scope-12-hard-constraints.md` item 6. The total-mass form $D = (G M_{\mathrm{tot}}
> T^2)^{1/3} \approx 6.694$ ($M_{\mathrm{tot}} = 3$) is `CLM-01` (`claimed-unverified`),
> **rejected by v1.5 Phase 25 EVID-10**. "Which `D` is correct" is settled; not re-openable.

**Reconciliation under the locked `D` — the key technical result.** Beyond being the rejected
value, the issue doc's `D = 6.694` is **functionally inert in its own derivation.** In
`03-curriculum-and-training-loop.md` §"tau_L and L_max Formula Resolution", `compute_tau_L`
assigns `D = np.cbrt(G * M_tot_ref * T_scale**2)` (= 6.694) and `V = D / T_scale`, but **neither
`D` nor `V` is referenced anywhere else in the routine** — the right-hand side and the integrator
consume `r_prime`, `v_prime`, `masses`, and `epsilon_soft` directly. Likewise the issue doc's
`compute_L_norm` consumes already-scaled `r_prime`/`v_prime` and never references `D`. Therefore
the `tau_L` and `L_max` **numbers are independent of the `D` label**; the `6.694` appears only in
a dead variable and in the line-305 comment ("Uses corrected B-02 formula: D ... = 6.694").

The locked $D \approx 4.6416$ enters **upstream**, at preprocessing (`ctl_instruction.md` §2.5:
$r' = r/D$, $v' = v/V$, $V = D/T$). All invariants ($E$, $s_{\min}$, $\tau_L$, $L_{\mathrm{norm}}$)
are computed from those correctly-scaled quantities. So **under the locked `D`, no re-derivation
of the `tau_L`/`L_max` formulas is required.** The fix is purely to delete the dead `D = 6.694` /
`V` lines from `compute_tau_L` and strike the line-305 comment.

**Downstream stage-threshold consequence.** The issue doc's checklist item **P4-1** ("Re-run
stage assignment for all ~15K trajectories with corrected D=6.694") is **rejected along with the
value.** Adopting $6.694$ would rescale every invariant and shift every stage boundary; under the
locked $4.6416$ there is **no such consequence** — the existing scaled invariants and the stage
thresholds defined on them stand. Independent corroboration inside the package:
`review_of_framework.md` §2.1 itself uses $D \approx 4.6416$ and $V \approx 0.46416$, agreeing
with the locked value and contradicting the issue doc — so within the source set the issue doc's
$6.694$ is the outlier, consistent with EVID-10.

**Conflict fully registered:** `CLM-01` ($6.694$, `claimed-unverified`, rejected) vs `CLM-19`
($4.6416$, `verified`, locked). Verdict: $4.6416$ governs; remove $6.694$ from `compute_tau_L`
and drop P4-1's re-derivation directive.

*Files relied on:* `03-curriculum-and-training-loop.md` (§"tau_L and L_max Formula Resolution",
lines ~261–306; P4-1); `ctl_instruction.md` (§2.5); `review_of_framework.md` (§2.1);
`claims-register.md` (CLM-01, CLM-19, Row Notes); `consolidated-context.md` (Fragment E);
`scope-12-hard-constraints.md` (item 6).

### 2.2 `tau_L` and `L_max` computation formulas -> Phase 33

**`L_max` — confirmed; all three sources agree.** `ctl_instruction.md` §"Step 3" item 2,
`review_of_framework.md` §1.1, and `03-curriculum-and-training-loop.md` all give

$$
L_{\max} = M_{\mathrm{tot}} \, r_{\mathrm{char}} \, v_{\mathrm{char}}, \qquad
v_{\mathrm{char}} = \sqrt{\frac{2\lvert E \rvert}{M_{\mathrm{tot}}}}, \qquad
r_{\mathrm{char}} = \tfrac{1}{3}\sum_{i<j}\lVert \mathbf r'_i - \mathbf r'_j \rVert,
\qquad L_{\mathrm{norm}} = \frac{L}{L_{\max}}.
$$

This lands in the spec as written (it is already `ctl_instruction.md`'s canonical
`compute_L_norm`). Clamping of $L_{\mathrm{norm}}$ is handled under M6 (§3.3).

**`tau_L` — a genuine method divergence; insufficient evidence to declare one canonical.** The
sources carry **two different estimators**:

- `ctl_instruction.md` §"Step 3" item 5 specifies a **Rosenstein-style** estimator operating
  directly on the BRUTUS trajectory time-series (uniform-cadence resample, delay-coordinate
  embedding, nearest neighbors with a Theiler window, divergence-curve regression);
  $\tau_L = 1/\lambda_{\max}$, $\infty$ if $\lambda_{\max} \le 0$. It **re-integrates nothing**
  and uses **no** potential softening (and no `D`). `stage_strat_revision.md` Phase I uses the
  same Rosenstein-style estimator.
- `03-curriculum-and-training-loop.md` and `review_of_framework.md` §1.1 specify a **Benettin /
  shadow-trajectory** estimator (perturb by $\varepsilon_{\mathrm{pert}} = 10^{-8}$, integrate
  nominal + perturbed, renormalize, average $\ln$ growth factors), with a static potential
  softening $\varepsilon_{\mathrm{soft}} = 10^{-10}$. The issue doc adds a faster **PCA +
  Rosenstein** batch approximation for the ~15K trajectories.

These can give different $\lambda_{\max}$ estimates, and the spec does **not** state which is
canonical when both are present, nor whether they are calibrated to agree. This is logged as
**G-01** (§8). The split softening here ($\varepsilon_{\mathrm{pert}} = 10^{-8}$ perturbation
magnitude; $\varepsilon_{\mathrm{soft}} = 10^{-10}$ static potential) is **distinct from the
locked loss-side $\varepsilon_{\mathrm{train}} = 10^{-5}$** and must not be collapsed into it (per
the framed question and `scope-12-hard-constraints.md`); it applies **only** to the
shadow/Benettin method, which re-integrates a softened potential — the Rosenstein method has no
integration potential, so the split is N/A there. These epsilon-values are non-dataset spec
parameters (`claims-register.md`, "Non-dataset figures ... excluded by design"), not CLM rows.

**Verdict.** Confirm `L_max` as the shared formula. For `tau_L`, the sources are split and not
reconciled — pose the choice rather than forcing it: either (i) keep the Rosenstein-style
trajectory estimator as canonical (matching `ctl_instruction.md` Step 3 and `stage_strat_revision.md`)
with the shadow/Benettin method as a calibration cross-check, or (ii) adopt the shadow/Benettin
estimator as canonical with PCA + Rosenstein as the fast batch approximation (matching the issue
doc and `review_of_framework.md`). Either way the $\varepsilon_{\mathrm{pert}} = 10^{-8}$ /
$\varepsilon_{\mathrm{soft}} = 10^{-10}$ split is spec'd only if the shadow method is adopted, and
the integration-based and PCA+Rosenstein estimates should be **FUT-cross-calibrated** on a
representative sample (the issue doc's own operational note). The Stage-4a/4b gates ($\tau_L > 5$;
$2 < \tau_L \le 5$; `ctl_instruction.md` stratification) are sensitive to the estimator choice —
flag this in the spec edit.

*Files relied on:* `ctl_instruction.md` (Step 3 items 2 & 5, stratification §);
`review_of_framework.md` (§1.1); `03-curriculum-and-training-loop.md` (tau_L/L_max section);
`stage_strat_revision.md` (Phase I); `claims-register.md` (Non-dataset-figures note).

---

## 3. Confirmed findings — BLOCKING and MAJOR (Section 3)

### 3.1 B-07 — replay/lookahead batch construction -> Phase 34

**Verdict — confirm the two-phase sampler; counts are claimed design constants (`CLM-12`).**
Three sources converge: `ctl_instruction.md` §"Mini-Batch Construction with Lookahead Sampling"
specifies replay $B_{\le k} = 240$ and lookahead $B_{k+1} = 16$ for batch size 256;
`review_of_framework.md` §5.2 adopts the CTL replay (~95%) + lookahead (~5%) with 50/50
uniform/acceleration-weighted point sampling; and `03-curriculum-and-training-loop.md` B-07
states 240 + 16 with 32 points/trajectory at 50/50. `pinn_architecture.md` §3.1 shows the
**legacy flat** `get_batch(batch_size, points_per_trajectory=32)` that B-07 flags as not yet
implementing replay/lookahead — and its own PIPE-04 note already says `points_per_trajectory=32`
"is a code default, not the spec contract." (SI-PINN-003 in `pinn_architecture.md` independently
records this inconsistency.)

**Reconciliation needed between the audit §6 pseudocode and the spec contract.** The issue doc's
§6 `training_step` hard-codes `n_pts = 32` and `np.tile(traj['ic_vector'], (32,1))`, but the
operative contract is `ctl_instruction.md`'s $n_{\text{pts}}(\text{traj}) =
\min(n_{\text{pts\_cap}}, n_{\text{snapshots}}(\text{traj}))$ **without replacement**, with the
50/50 split realized as `k_w = floor(n_pts/2)` acceleration-weighted draws (Gumbel-top-k) plus
the remainder uniform. The audit §6 pseudocode must adopt the $\min(\cdot)$ cap. In practice the
cap rarely binds — the verified median snapshot counts are **61 / 127 / 1003** (`CLM-16`,
`verified`; std / hier-base / gold; issue-doc `~59/~125/~1000` are `CLM-13`, superseded) — all
comfortably above 32, but the *contract* is $\min(\cdot)$, not a fixed 32.

**Figures.** Replay/lookahead/point counts 240 / 16 / 8192 / 4096 are `CLM-12`
(`claimed-unverified` design constants), and `n_pts_cap = 32` is a revisable code default
(PIPE-04). Adopt the contract; record the counts as claimed, not fixed.

*Files relied on:* `ctl_instruction.md` (Mini-Batch Construction, §2.6 stage-query interface);
`pinn_architecture.md` (§3.1, SI-PINN-003); `03-curriculum-and-training-loop.md` (B-07, §6);
`review_of_framework.md` (§5.2); `claims-register.md` (CLM-12, CLM-13, CLM-16);
`verified-facts-reference.md` (VF-2).

### 3.2 B-08 — data-fidelity vs collocation separation -> Phase 34

**Verdict — confirm the two-independent-point-set discipline; correct the data-loss function.**
The roles already exist in the spec — `pinn_architecture.md` §3.1 defines the data-fidelity term
($N_{\text{data}} = 256 \times 32 = 8192$) and §3.2 the physics residual on collocation points
($n_{\text{col}}$ default 4096); `ctl_instruction.md` §"Loss Function Formulation" composes them;
`review_of_framework.md` §5.1 explicitly defines the two distinct sets (data points where ground
truth exists; collocation from the continuous domain). B-08's contribution is to make the
**separate-set discipline explicit in the batch constructor**: data points from BRUTUS snapshots;
collocation from continuous $[0,T] \to \tau$. The single-forward-pass-on-the-union optimization
(`review_of_framework.md` §5.1) is compatible — the sets stay logically separate but may be
concatenated for one forward pass.

**Conflict to resolve (carried to NS-18).** The issue doc frames the data term as **L1/MAE**
(B-08: "8192 data-fidelity points, L1 loss"). The current spec data term is **Huber**:
`pinn_architecture.md` §3.1 states "The previous MAE/L1 data-loss prose is replaced by this Huber
contract," $\delta_r = 1$. So B-08's "L1 loss" must be updated to **Huber on scaled positions**.
Same issue resolved in §3.11 (NS-18).

**Figures and a residual gap.** The 8192 / 4096 totals are `CLM-12` (`claimed-unverified`). The
per-trajectory collocation count diverges between sources — `review_of_framework.md` §5.1 gives
~256/traj (illustrative) while the issue doc gives 16/traj (4096/256). Both are unverified;
logged as **G-02** (§8).

*Files relied on:* `pinn_architecture.md` (§3.1, §3.2); `ctl_instruction.md` (Loss Function
Formulation); `review_of_framework.md` (§5.1); `03-curriculum-and-training-loop.md` (B-08);
`claims-register.md` (CLM-12).

### 3.3 M6 — `L_norm` clamping -> Phase 33

**Verdict — M6's IC-vector rationale is obsolete; a `[0,1]` metadata guard remains reasonable.**
Under the **LOCKED** 14D $[\tau, IC_{13}]$ contract (`scope-12-hard-constraints.md` item 1),
$L_{\mathrm{norm}}$ is **no longer a network IC slot**: `ctl_instruction.md` §"Step 4" retains the
invariant-heavy descriptors (including $L_{\mathrm{norm}}$) as staging/diagnostic/loss-scaling
**metadata** only, "not final network IC slots under the Phase 17 input contract." So the issue
doc's M6 premise — that $L_{\mathrm{norm}}$ exceeding 1 yields a normalized IC component $>1$
after the $2x-1$ mapping — **no longer applies**; there is no $L_{\mathrm{norm}}$ IC slot to
overflow.

The clamp question relocates to the **staging/diagnostic** use. The Stage-0 gate uses $L/L_{\max}
> 0.5$ (`ctl_instruction.md` stratification). Physically $L_{\mathrm{norm}} \in [0,1]$ by
construction, but numerical $r_{\mathrm{char}}$/$v_{\mathrm{char}}$ estimates can push it slightly
above 1. The existing references already guard this: `ctl_instruction.md` Step 3 item 2 returns
$L/(L_{\max}+\text{eps})$, and the issue doc's `compute_L_norm` returns `np.clip(L/(L_max+eps), 0,
1)`. A $[0,1]$ clamp (or at minimum a $>1$ diagnostic warning) on the metadata keeps the Stage-0
threshold well-defined and is harmless. **No IC-range guard is needed**, since $L_{\mathrm{norm}}$
does not enter $IC_{13}$.

**Spec edit.** In `ctl_instruction.md` Step 3 / Step 4, note that $L_{\mathrm{norm}}$ metadata is
clamped to $[0,1]$ for staging/diagnostics; drop the "before the $2x-1$ IC mapping" framing. Do
**not** assume the IC-vector-mapping framing still holds (per the framed question).

*Files relied on:* `ctl_instruction.md` (Step 3 item 2, Step 4);
`03-curriculum-and-training-loop.md` (M6, compute_L_norm); `scope-12-hard-constraints.md` (item 1).

### 3.4 M7 — `tau_L` excluded from the IC vector -> Phase 33

**Verdict — confirm exclusion by design; the spec already encodes it.** `ctl_instruction.md`
§"Step 3" returns $\tau_L$ in the invariant tuple and uses $(E, Q, s_{\min}, L_{\mathrm{norm}},
\tau_L)$ for **default stage gating**; §"Step 4" **excludes** the invariant-heavy descriptors
(including $\tau_L$) from the final $IC_{13}$ slots, consistent with the **LOCKED** 14D
Jacobi-state contract (`scope-12-hard-constraints.md` items 1–2; $IC_{13} = [m_1,m_2,m_3, \rho_x,
\lambda_x, \lambda_y, \dot\rho_x, \dot\rho_y, \dot\rho_z, \dot\lambda_x, \dot\lambda_y,
\dot\lambda_z, E]$). The issue doc's M7 recommendation — exclude $\tau_L$ as a derived dynamical
property, retain it for staging/evaluation — is exactly this. The "no documented decision" gap M7
flags is closed by Step 4's explicit exclusion plus the Phase 17 contract. Low-risk confirmation;
no conflict.

*Files relied on:* `ctl_instruction.md` (Step 3, Step 4, network input contract);
`03-curriculum-and-training-loop.md` (M7); `scope-12-hard-constraints.md` (items 1–2).

### 3.5 M14 — merged gradient clipping -> Phase 35

**Verdict — confirm the merge $C_{\text{stage}} \cdot \mathrm{median}(\cdot)$.** The spec carries
the two halves M14 wants merged: `pinn_architecture.md` §4.4 specifies $5.0 \times \mathrm{median}$
of the last 100 gradient norms; `ctl_instruction.md` §"Adaptive Median-Based Gradient Clipping"
specifies the curriculum-aware $C$ schedule (stages 0–1: 7–10; 2–3: 5; 4–6: 3).
`review_of_framework.md` §5.4 already **synthesizes** them into $C \cdot \mathrm{median}(\text{last
}100)$. Clipping is Adam-only and disabled during L-BFGS (`ctl_instruction.md` Phase 2b;
`pinn_architecture.md` §4.4; `review_of_framework.md` §5.4 all agree). The fixed $5.0$ in §4.4 is
the stage-2–3 value of the CTL schedule; replacing it with $C_{\text{stage}}$ generalizes it.

**Conflict / uncertainty.** For stages 0–1 the spec gives a **range** 7–10; the issue doc's
`C_table` and `review_of_framework.md` §5.4 both instantiate the midpoint **8.5**. The 8.5 is
`CLM-10` (`claimed-unverified`); the spec range is 7–10. Adopt $C_{\text{stage}} \cdot
\mathrm{median}(\cdot)$; record the stages-0–1 value as the claimed 8.5 midpoint **or** keep the
7–10 range as a tunable — 8.5 is not locked.

*Files relied on:* `pinn_architecture.md` (§4.4); `ctl_instruction.md` (Adaptive Median-Based
Gradient Clipping, Phase 2b); `review_of_framework.md` (§5.4); `03-curriculum-and-training-loop.md`
(M14, Gradient Clipping — Merged Specification); `claims-register.md` (CLM-10).

### 3.6 M15 — energy-loss weight schedule -> Phase 35

**Verdict — the issue doc's premise is superseded by the current spec; the `cap_table` is
unnecessary.** M15 argues against $\lambda_E$ "up to 1000 at Stage 6" (from $\text{base} =
10^{k-3}$, so $10^3 = 1000$) and proposes a capped-hybrid `cap_table` $\{0{:}1, \dots, 6{:}500\}$
(`CLM-11`). But the **current** spec already replaced that schedule: `pinn_architecture.md` §4.1
(PHYS-05) sets

$$
\lambda_E^{\max}(k) = \lambda_L^{\max}(k) =
\begin{cases} 0 & k \in \{0,1\}\\ 10^{\,k-4} & k \in \{2,3,4\}\\ 1 & k \in \{5,6\}\end{cases}
$$

with linear warmup over $I_{\text{warm}} = \min(2000,\, 0.1\,N_{\text{Adam},k})$. This **caps
$\lambda_E^{\max}$ at 1** (stages 5–6) — far below both the issue doc's uncapped 1000 *and* its
capped 500. Numerically the spec schedule is $\{2{:}0.01,\,3{:}0.1,\,4{:}1,\,5{:}1,\,6{:}1\}$.

So M15's concern targets a **superseded** schedule. Under the current PHYS-05 schedule
$\lambda_E$ cannot overwhelm the data/physics terms — it is held at $\le 1$ with warmup, *more*
conservative than the proposed `cap_table`. The `cap_table` (`CLM-11`, `claimed-unverified`) is
therefore **not needed**. State the reconciliation plainly: **neither 1000 nor 500 is the spec
value — the spec is $\le 1$.**

**Open sub-part.** The dominance **safeguard** ("if $\lambda_E L_{\text{energy}} > 10
L_{\text{data}}$, reduce $\lambda_E$ by 0.5") is a separate idea not in the spec. It could be
adopted as a runtime diagnostic, but under $\lambda_E^{\max} \le 1$ it is largely redundant.
Recommendation: keep the PHYS-05 $\lambda_E^{\max}(k)$ warmup schedule (the recommended baseline
stands); do not adopt the `cap_table`; treat the dominance safeguard as optional and low-value
under the capped schedule.

*Files relied on:* `pinn_architecture.md` (§4.1 PHYS-05); `03-curriculum-and-training-loop.md`
(M15, §6.4); `claims-register.md` (CLM-11).

### 3.7 M16 — `dt_out`-aware collocation scaling -> Phase 33 / Phase 35

**Verdict — genuinely unsettled; a three-way conflict; keep the spec's deferral and FUT-flag the
rule.** Three positions are live:

- `review_of_framework.md` §5.3: **no scaling needed** — because collocation is sampled from the
  continuous $[0,T]$, the source trajectory's resolution is irrelevant; mixed resolution is
  handled "gracefully ... without ... up-sampling ... or down-sampling."
- `03-curriculum-and-training-loop.md` M16: scale $n_{\text{col}} \propto
  dt_{\text{base}}/dt_{\text{out}}$ (audit-verbatim direction); for $dt_{\text{base}} = 0.01$:
  gold $1\times$, hierarchical-base $\approx 0.125\times$, standard-base $\approx 0.059\times$
  (`CLM-20`). The issue doc explicitly flags that the **inverse** $dt_{\text{out}}/dt_{\text{base}}$
  "would be a separate methodology change."
- `ctl_instruction.md` §"Mini-Batch Construction" **defers** the question (SCOPE-11: the
  collocation-density rule is "not used here"), exposing $dt_{\text{out}}$ / $n_{\text{snapshots}}$
  as forward-interface metadata only.

**Nuance the owner should weigh.** The spec's collocation sampler (`pinn_architecture.md` §3.2
`sample_collocation_points`) draws the **uniform half** from `np.random.uniform(0,1)` —
resolution-independent, which supports `review_of_framework.md` §5.3 — but the
**acceleration-weighted half** weights by `traj['accelerations']` from the discrete BRUTUS
snapshots, so low-resolution trajectories (fewer snapshots) yield coarser importance sampling.
M16's concern therefore has force for the *weighted* half but not the *uniform* half. The
direction itself is physically ambiguous: $dt_{\text{base}}/dt_{\text{out}}$ gives high-resolution
trajectories more collocation (issue doc's choice), while the inverse would give low-resolution
trajectories more to compensate for sparser data constraints — both are defensible, which is
exactly why this is unsettled.

**Figures.** The per-variant $dt_{\text{out}}$ values are **verified** (`CLM-17`: std 0.17 /
hier-base 0.08 / gold 0.01; `verified-facts-reference.md` VF-1). The M16 scaling **factors**
(`CLM-20`) are `claimed-unverified` *derived* figures — they depend on the verified
$dt_{\text{out}}$ but the scaling *rule* is unverified. Do not adopt a scaling factor as fact.

**Recommendation.** Keep `ctl_instruction.md`'s deferral (forward interface) until FUT empirical
evidence resolves the direction. If a rule is adopted, the audit-verbatim
$dt_{\text{base}}/dt_{\text{out}}$ is the issue doc's committed direction but **conflicts with**
`review_of_framework.md` §5.3 (no scaling), and the inverse is a distinct methodology change.
Logged as **G-03** (§8).

*Files relied on:* `review_of_framework.md` (§5.3); `03-curriculum-and-training-loop.md` (M16,
P3-9); `ctl_instruction.md` (Mini-Batch Construction, §2.6 SCOPE-11); `pinn_architecture.md`
(§3.2); `claims-register.md` (CLM-17, CLM-20); `verified-facts-reference.md` (VF-1).

### 3.8 D5 — stage-transition dual-path -> Phase 33

**Verdict — confirm the critique and the dual-path structure; the fallback figures are
claimed-unverified hypotheses.** The spec baseline (`ctl_instruction.md` §"Stage Transition
Criteria") lists **four strict criteria**: training-loss plateau ($\varepsilon_{\text{plateau}} =
10^{-5}$, patience 200, $\beta = 0.98$); validation-loss stability $\mathcal{L}_{\text{val}}(i) \le
\min_{j \le i}\mathcal{L}_{\text{val}}(j)$; physics-residual $\varepsilon_{\text{phys}} = 10^{-4}$;
energy-drift $\varepsilon_{\text{energy}} = 10^{-4}$ using the **locked** $\varepsilon_H = 10^{-4}
\cdot S_H$ floor (PHYS-04). The spec **already carries the author note** questioning attainability
with limited data ("All of this transition criteria is theoretical now ... Because I only have a
limited amount of training data, maybe not even enough ...") — the same concern D5 raises — but it
does **not** yet encode the fallback path or the per-stage threshold table.

The issue doc's D5 proposes: PATH A (strict, with criterion 2 **relaxed** from strict-min to
$\le$ percentile-10 of validation history); PATH B (fallback: `MAX_EPOCHS` $\{0{:}500, \dots,
6{:}1200\}$ `CLM-09`; stagnation = no $>1\%$ validation improvement for 400 epochs; NaN rollback
with $\text{LR} \times 0.5$); per-stage $\varepsilon_{\text{phys}}/\varepsilon_{\text{energy}}$
thresholds ($5\times10^{-3} \dots 10^{-4}$, `CLM-08`, explicitly "not fixed"); and a Stage-0 pilot
to calibrate.

**Assessment.** The critique is well-founded and already acknowledged in the spec. The brittle
element is strict criterion 2 (monotonic $\mathcal{L}_{\text{val}} \le \min$); relaxing it to a
percentile plus adding a max-epochs fallback is a sound, low-risk robustness improvement that
touches **no locked constraint** (the energy criterion still uses the locked $\varepsilon_H =
10^{-4}\cdot S_H$). Adopt the dual-path **structure** and surface the substantive edit explicitly:
criterion 2 changes from strict-min to $\le$ percentile-10.

**Figures.** The per-stage thresholds (`CLM-08`) and `MAX_EPOCHS` (`CLM-09`) are
`claimed-unverified` design **hypotheses**, explicitly "not fixed," to be **FUT-calibrated** via
the Stage-0 pilot. Record the threshold/max-epochs tables as claimed design constants pending
Stage-0 calibration — not as fixed spec values.

*Files relied on:* `ctl_instruction.md` (Stage Transition Criteria, author note); `pinn_architecture.md`
(§3.4 for $\varepsilon_H = 10^{-4}\cdot S_H$); `03-curriculum-and-training-loop.md` (D5, §6.3);
`claims-register.md` (CLM-08, CLM-09).

### 3.9 NS-12 — componentwise AD -> Phase 34

**Verdict — confirm; the spec already satisfies NS-12, and a baseline-report reference
contradicts it.** `pinn_architecture.md` §5.3.1 (PHYS-02) is the canonical componentwise
normalized-time AD contract: it requires all nine $dr'_{i,\alpha}/du$; **forbids**
`torch.autograd.grad(r.sum(), u, ...)` (an all-ones-covector VJP, "not the nine individual
derivatives"); lists acceptable patterns (`jacrev` + `vmap`, explicit per-component loop,
full-Jacobian); gives a worked synthetic-trajectory test ($r'(u) = [\sin 2\pi u, \cos 2\pi u, u^2]$
with the symbolic $dr'/du$, $d^2r'/du^2$); and §10.3 adds an acceptance check (relative error
$< 10^{-6}$). This is exactly NS-12's requirement ("do not differentiate the summed 9D output as a
proxy"). Confirm NS-12 at the contract level.

**Conflict to flag for upstream correction.** `review_of_framework.md` §4.3's "reference
implementation" computes derivatives with `torch.autograd.grad(outputs=r, inputs=t,
grad_outputs=torch.ones_like(r), create_graph=True)` — the **ones-covector pattern**, equivalent
to differentiating `r.sum()`: it returns $\sum_k \partial r_k/\partial t$ (a summed proxy), **not**
the nine per-component derivatives. This directly **contradicts PHYS-02** and must be replaced by
the componentwise contract. NS-12's fix aligns with PHYS-02, against §4.3. Logged as **G-07** (§8).

**Residual open.** The concrete batched three-body PyTorch implementation is deferred to FUT-01 /
Phase 21 VER-04 (`pinn_architecture.md` §5.3.1: "Spec-illustrative AD pattern (not FUT-01
implementation prescription)"). NS-12 is confirmed at the contract level; the executable
implementation is FUT scope.

*Files relied on:* `pinn_architecture.md` (§5.3.1 PHYS-02, §10.3); `review_of_framework.md` (§4.3);
`03-curriculum-and-training-loop.md` (NS-12).

### 3.10 NS-13 — Huber energy $\delta$ -> Phase 35

**Verdict — the critique is valid; reduce $\delta$ from 1.0; the exact value is unverified and
FUT-calibrated.** Three positions: spec $\delta = 1.0$ (`pinn_architecture.md` §3.4, PHYS-04);
`review_of_framework.md` §4.4 $\delta = 0.1$ (fixed, with the "$<10\%$ deviation -> quadratic"
reasoning); issue-doc NS-13 $\delta \approx 0.01$–$0.1$, quantile-tuned per stage (`np.clip(
np.quantile(|ΔH|, 0.75), 0.01, 0.1)`).

$\delta = 1.0$ is the **revisable** baseline (not a locked constraint). The critique — shared by
two independent sources — is that normalized $|\Delta H|$ is expected $\ll 1$, so $\delta = 1.0$
makes Huber degenerate to L2 over the whole expected range, losing outlier robustness during
close encounters. This is a sound argument, and the **direction** ($\delta < 1.0$) is well
supported.

**But the exact value is unverified.** It depends on the observed $|\Delta H|$ distribution, which
**no in-milestone phase measures** (these are empirical quantiles, not in the claims register as
verified figures). So: recommend reducing $\delta$ from 1.0 and **calibrating from observed
$|\Delta H|$ quantiles** (per stage if the drift scale shifts across stages — plausible, since
chaotic stages have larger drift). The specific value (0.1 vs quantile-tuned 0.01–0.1) is a FUT
empirical calibration, not adoptable as fact now; use `review_of_framework.md` §4.4's $\delta =
0.1$ as a starting point pending calibration. Whether $\delta$ becomes stage-dependent is an open
design choice. Logged as **G-10** (§8).

*Files relied on:* `pinn_architecture.md` (§3.4 PHYS-04); `review_of_framework.md` (§4.4);
`03-curriculum-and-training-loop.md` (NS-13, Huber Delta for Normalized Energy).

### 3.11 NS-18 — loss-component scaling contract -> Phase 35

**Verdict — confirm the units contract; the only substantive change is L1/MAE -> Huber for the
data term.** The scaling/units contract is well-defined across the spec and consistent: all terms
operate in the dimensionless $G = 1$, $r' = r/D$ system (locked $D$, `CLM-19`).
`pinn_architecture.md` §3.1 fixes the data term (Huber on scaled positions), §3.2 the physics
residual on collocation points (componentwise AD; on the $\tau$-leaf path $a' = 4\,d^2r'/d\tau^2$;
$\varepsilon_{\text{train}} = 10^{-5}$; causal weighting), §3.4 the energy regularizer on the
**same** collocation set ($dr'/du$, same $\varepsilon_{\text{train}} = 10^{-5}$, floor
$\varepsilon_H = 10^{-4}\cdot S_H$), and §4.1 the PHYS-05 composition. Confirm this units contract.

**The reconciliation.** The issue doc's NS-18 (and its Loss Component Scaling Contract table)
frames $L_{\text{data}}$ as **L1/MAE**. The current spec data term is **Huber** ($\delta_r = 1$;
`pinn_architecture.md` §3.1: "The previous MAE/L1 data-loss prose is replaced by this Huber
contract"; §4.1 confirms "$L_{\text{data}}$: Huber loss on position predictions, $\delta_r = 1$
default"). So NS-18's "$L_{\text{data}}$ ... with L1/MAE" must be updated to **Huber on scaled
positions**. Otherwise the issue-doc contract matches the spec ($r' = r/D$; same
$\varepsilon_{\text{train}} = 10^{-5}$ in physics and energy; same collocation set for physics and
energy). Adopt the units contract as the spec defines it, with $L_{\text{data}} = $ Huber.

**Cross-links.** Same Huber-vs-L1 correction as B-08 (§3.2). The canonical chain-rule factors the
issue doc cross-references to "01" live in `pinn_architecture.md` §5.3.1 (PHYS-02): $a' =
4\,d^2r'/d\tau^2$ on the $\tau$-leaf, no factor on the $u$-leaf. Locked anchors: $D$ (`CLM-19`),
$\varepsilon_{\text{train}} = 10^{-5}$ (`scope-12-hard-constraints.md` item 4).

*Files relied on:* `pinn_architecture.md` (§3.1, §3.2, §3.4, §4.1, §5.3.1);
`03-curriculum-and-training-loop.md` (NS-18, Loss Component Scaling Contract);
`claims-register.md` (CLM-19); `scope-12-hard-constraints.md` (item 4).

---

## 4. Data-driven adaptive stage assignment (Section 6) -> Phase 33

**Verdict — adopt the methodology as an *augmentation* to the threshold-based Step 5, constrained
to preserve the locked data-side fidelity roles; the population figures are claimed-unverified.**

The proposal (`03-curriculum-and-training-loop.md` §"Data-Driven Adaptive Stage Assignment"; deep
dive in `stage_strat_revision.md` Parts I–IV) replaces fixed theoretical thresholds with
data-adaptive criteria: EDA over all trajectories' invariants; a $Q_{\text{norm}} =
Q_{\text{raw}}/s^3$ correction for the quasi-random virial distortion; correlation/PCA; K-means
clustering; quantile thresholds; a population safeguard; and a small PINN pilot. It **augments**
(not replaces) `assign_curriculum_stage()`.

The motivation is well grounded. The $Q \propto s^3$ distortion is real and documented:
`sampling_method.md` §"Sampling-Time Size Variability" sources the scale factor $s$ from Sobol
coordinate $u_4$ over $[0.8, 1.2]$ for quasi-random generation and states it "changes $Q = 2T/|U|$
by a factor of $s^3$." The `ctl_instruction.md` stratification author note **already** suggests
the data-scan approach for exactly this reason ("simply designing the criteria based on
theoretical values might not be the best way ... virial ratio is not preserved for quasi-random IC
sampling"). So adopting data-driven quantiles to refine the theoretical anchors matches the spec
author's own intent.

**Four constraints/conflicts the methodology must respect (these are the substance of the
adjudication):**

1. **Locked data-side contracts (`scope-12-hard-constraints.md` item 7, PIPE-01..10).** The
   stage-query interface (`sample_replay`, `sample_lookahead`, `has_stage`) and the
   trajectory-admission/quality contracts are fixed. The adaptive criteria still produce integer
   stage labels 0–6 keyed by `record_key` over the admitted set, so they remain consumable by
   these queries — compatible, provided the labels stay per-`record_key`.
2. **Locked Stage-5 gold obligation conflicts with `stage_strat_revision.md` Table 4.**
   `ctl_instruction.md` §"Step 5" and the GAP-26-01 ruling fix that "every Stage-4-admitted ID
   owes a Stage-5 gold sample," that Stage 5 is the **gold stratum** (Set 2b), and that the 184
   standard IDs are genuine Stage-5 gold holes pending re-simulation. But `stage_strat_revision.md`
   Table 4 reorganizes stages **purely by chaos clustering** (Stage 5 = "strongly chaotic
   quasi-random cluster") and **dissolves the fidelity-refinement roles** (Stage 2 = hierarchical
   gold refinement; Stage 5 = quasi-random gold). This **conflicts** with the locked obligation
   and the multi-fidelity curriculum design. Notably, the issue doc's own Stage Inventory (lines
   ~670–678) *does* preserve the fidelity roles (Stage 2 = hierarchical gold; Stage 5 =
   quasi-random gold minus 184) while using quantile/cluster criteria for stages 3–6 — so the
   issue-doc inventory is a constrained hybrid, but `stage_strat_revision.md` Table 4 is not.
   **Reconciliation:** the adaptive criteria may set the *within-fidelity ordering and boundaries*
   (via quantiles/clustering) but must **preserve the locked fidelity-stage roles** — Stage 2 and
   Stage 5 remain the high-resolution (gold) refinement stages tied to the gold strata, and the
   gold-counterpart contract + 184-hole accounting stay in force. Adopt the adaptive criteria
   *inside* the fidelity-constrained skeleton, not as a free re-clustering that erases the gold
   stages. Logged as **G-04** (§8).
3. **Population safeguard threshold discrepancy.** The issue doc says ">10% per stage";
   `stage_strat_revision.md` §"Population Control and Stage Merging" says merge below "5% of the
   total dataset." Both are `claimed-unverified` design choices — to be set with the owner (logged
   as **G-05**, §8). The per-stage counts (`CLM-02..CLM-07`: Stage 0 ~1,200; 1 ~2,000; 2 ~1,657;
   3 ~600; 4 ~1,600; 6 Unknown) are `claimed-unverified` design **outputs** of the adaptive method
   — **not facts**; no v1.6 phase verifies them; FUT-flagged. The ~2,565 count that appears
   alongside (Stage 5) is the v1.5-**verified** `CLM-15` (a **gold count**, not a stage count) —
   keep these distinct.
4. **The $Q_{\text{norm}}$ correction needs the scale factor $s$ per IC.** `stage_strat_revision.md`
   Phase I flags that if $s$ "is not explicitly stored with each IC, it must be recorded during ...
   generation or estimated post-hoc," and that without it "the virial ratio ... should be excluded
   ... for those simulations." `sampling_method.md` confirms $s \in [0.8, 1.2]$ from Sobol $u_4$.
   Whether $s$ is persisted in trajectory metadata is a **data-side gap** — logged as **G-06** (§8);
   if absent, $Q$ must be excluded for the quasi-random set per the report's own contingency.

**Minor.** `stage_strat_revision.md` carries its own SI-SSR-001 (the $I_1, I_2, I_3$ DataFrame
schema omits the $I_3$ column) — an upstream documentation fix, noted, no downstream figure impact.

**Verdict (consolidated).** Adopt the data-driven adaptive methodology as an augmentation to
`ctl_instruction.md` Step 5 (data-driven quantiles/clustering refine the theoretical anchors),
**constrained** to preserve the locked fidelity-stage roles (Stage 2/5 gold) and the
gold-counterpart/184-hole contracts; reconcile the population safeguard (5% vs 10%, owner's
choice); record the stage counts as `claimed-unverified` (`CLM-02..CLM-07`, FUT); resolve the
$s$-storage gap. Spec-edit target: `ctl_instruction.md` (Step 5 + the stratification section).

*Files relied on:* `03-curriculum-and-training-loop.md` (Data-Driven Adaptive Stage Assignment,
Stage Inventory Summary); `stage_strat_revision.md` (Parts I–IV, esp. Phase I virial correction,
Phase III/IV criteria & population balancing, SI-SSR-001); `ctl_instruction.md` (Step 5,
stratification §, §2.6 gold-counterpart contract); `sampling_method.md` (Sampling-Time Size
Variability); `claims-register.md` (CLM-02..CLM-07, CLM-15); `consolidated-context.md`
(Fragments C, D); `scope-12-hard-constraints.md` (item 7).

---

## 5. ALM `mu_p` clamp (Section 15) -> Phase 34 / Phase 35

**Verdict — the clamp's original target (dense-residual ALM) is rejected; it lands on the optional
P2 scalar-constraint ablation *only if* that ablation uses an adaptive penalty parameter, and not
on the baseline loss at all.**

The issue doc (§"ALM Parameter Update Specification", MINOR/INFO) observes that $\mu_p$ can diverge
without bounds and proposes `mu_p = np.clip(mu_p, 1e-4, 100.0)` in the ALM update — where the
update is the RMSprop-style $v_p = 0.99 v_p + 0.01\,L_{\text{phys}}^2$, $\mu_p = 0.01/\sqrt{v_p +
10^{-8}}$ (audit §6 `training_step`). Lower bound prevents physics enforcement decaying to zero;
upper bound prevents overwhelming the data term.

But the spec **rejects** the dense-residual pseudo-ALM that this $\mu_p$ belongs to
(`ctl_instruction.md` §"Loss Function Formulation"; `pinn_architecture.md` §3: "No dual variables
are part of the default training loss"). ALM survives **only** as a P2 ablation on **scalar**
conservation constraints (`pinn_architecture.md` §4.2: constraints $c_E = \mathrm{RMS}_n(\Delta
H_n)$, $c_{L,\alpha} = \mathrm{RMS}_n(\cdot)$; dual updates only between Adam epochs / refinement
passes, never inside L-BFGS; default OFF). That ablation uses a **different** update structure
(dual ascent on scalar constraint values) and the spec does **not** specify a divergent
RMSprop-style $\mu_p$ there.

So, stating both positions:

- **On the baseline loss:** the clamp does **not** apply — there is no $\mu_p$ (no dual variables
  in the default penalty-term loss).
- **On the P2 scalar-constraint ablation:** the clamp $[10^{-4}, 100.0]$ lands **only if** that
  ablation is implemented with an adaptive (RMSprop-style) penalty parameter that can diverge —
  which the current §4.2 does not mandate. If such a parameter is used, the clamp plus the
  per-stage **reset** of $\lambda_p/\mu_p/v_p$ (recommended for the now-superseded dense ALM in
  `review_of_framework.md` §4.2) are the natural guards. This is contingent on the ablation's
  design, not on the baseline.

The clamp bounds $[10^{-4}, 100.0]$ are a non-dataset spec parameter (`claims-register.md`,
"Non-dataset figures ... excluded by design"), not a CLM figure. **Spec edit (if adopted):** add
the clamp to the §4.2 ablation's penalty-parameter update *conditional* on that update being
adaptive; note it is N/A to the default loss. (`scope-12-hard-constraints.md` §4 confirms the
$\mu_p$-clamp finding retains a resolution path and is not out of scope.)

*Files relied on:* `03-curriculum-and-training-loop.md` (ALM Parameter Update Specification, §6
training_step); `pinn_architecture.md` (§3 intro, §4.2); `ctl_instruction.md` (Loss Function
Formulation); `review_of_framework.md` (§4.2); `claims-register.md` (Non-dataset-figures note);
`scope-12-hard-constraints.md` (§4).

---

## 6. Corrections flagged to the baseline reports

The two baseline reports carry the design intent and are mostly adopted, but cross-reading against
the locked constraints and the PHYS-02 contract surfaced two reference implementations that are
now wrong and must be corrected upstream before they propagate into the spec:

- **`review_of_framework.md` §4.3 (AD reference) uses the forbidden anti-pattern.** Its
  `torch.autograd.grad(outputs=r, inputs=t, grad_outputs=torch.ones_like(r), ...)` is the
  all-ones-covector / `r.sum()` proxy that `pinn_architecture.md` §5.3.1 (PHYS-02) explicitly
  forbids — it returns $\sum_k \partial r_k/\partial t$, not the nine per-component derivatives.
  Replace with the PHYS-02 componentwise contract. (G-07; see §3.9.)
- **`review_of_framework.md` §2.2 (softening) uses the additive form.** Its $1/(\lVert r\rVert +
  \varepsilon)$ / $1/(\lVert r\rVert + \varepsilon)^3$ is the PHYS-03 anti-pattern locked as
  prohibited (`scope-12-hard-constraints.md` item 4; matched-Plummer $\sqrt{\lVert\Delta r\rVert^2
  + \varepsilon^2}$ required). The §2.2 *value* argument ($10^{-5}$) is a legitimate input to the
  epsilon-strategy decision; its *form* is superseded. (G-08; see §1.3.)

Both reports otherwise remain the adopted design-intent sources (batch construction §5.2; clipping
§5.4; $L_{\max}$ §1.1; the adaptive methodology in `stage_strat_revision.md`).

---

## 7. Verdict ledger (locked vs revised vs deferred)

| # | Finding | Verdict type | Locked sub-part respected |
|---|---------|--------------|---------------------------|
| 1.1 | Causal-training mode | Owner decision (pose A/B/C; none recommended) — but spec is **not** Option B | PHYS-05 causal weighting; dense-ALM rejection |
| 1.2 | `s_min` frame | Owner decision; spec baseline = Option A; recommend none | PHYS-03 matched-Plummer (item 4) |
| 1.3 | Epsilon strategy | Owner decision on static side; loss side **LOCKED** at `1e-5` | item 4 / CLM-19 companion |
| 2.1 | `D` 6.694 vs 4.6416 | **LOCKED** 4.6416; 6.694 inert + rejected; strike from `compute_tau_L` + P4-1 | item 6 / CLM-19 |
| 2.2 | `tau_L`/`L_max` formulas | `L_max` confirmed; `tau_L` estimator **insufficient evidence** (pose two) | `1e-5` not collapsed with `1e-8`/`1e-10` split |
| 3.1 | B-07 replay/lookahead | Confirm contract; counts `CLM-12` claimed | locked stage-query interface (item 7) |
| 3.2 | B-08 two point sets | Confirm; correct L1->Huber; counts `CLM-12` claimed | — |
| 3.3 | M6 `L_norm` clamp | IC-vector framing obsolete; `[0,1]` metadata guard | 14D `[tau, IC13]` (item 1) |
| 3.4 | M7 `tau_L` excluded | Confirm exclusion by design | 14D Jacobi-state (items 1–2) |
| 3.5 | M14 merged clipping | Confirm `C_stage·median`; 8.5 is `CLM-10` claimed | — |
| 3.6 | M15 energy-loss weight | Premise superseded; spec `lambda_E^max <= 1`; cap_table unneeded | — |
| 3.7 | M16 collocation scaling | **Insufficient evidence** (three-way); keep deferral; FUT | `dt_out` verified (CLM-17); factors CLM-20 claimed |
| 3.8 | D5 stage transition | Confirm dual-path + percentile relaxation; thresholds `CLM-08/09` claimed | locked `eps_H = 1e-4·S_H` (PHYS-04) |
| 3.9 | NS-12 componentwise AD | Confirm (spec satisfies); flag §4.3 anti-pattern | PHYS-02 contract |
| 3.10 | NS-13 Huber `delta` | Reduce from 1.0; exact value **unverified** (FUT) | `delta` is revisable, not locked |
| 3.11 | NS-18 scaling contract | Confirm units; correct L1->Huber data term | locked `D` (CLM-19), `1e-5` (item 4) |
| 4 | Adaptive stage assignment | Adopt as augmentation; preserve gold-stage roles; counts `CLM-02..07` claimed | items 1, 7; gold-counterpart contract |
| 5 | ALM `mu_p` clamp | N/A to baseline; conditional on P2 ablation being adaptive | dense-ALM rejection |

---

## 8. Claims-register addendum — logged gaps (do not invent; resolve as noted)

These gaps were surfaced during adjudication. They are recorded here rather than filled. Each
notes what is missing and what would resolve it; figure-bearing gaps cite the relevant CLM row.

| Gap | What is missing | How it resolves | Related CLM / constraint |
|-----|-----------------|-----------------|--------------------------|
| G-01 | Canonical `tau_L` estimator is not fixed — Rosenstein-style (ctl Step 3, stage_strat) vs Benettin/shadow (issue-03, review §1.1) coexist, uncalibrated | Owner picks the canonical estimator; FUT cross-calibrates the two on a representative sample; the `eps_pert=1e-8`/`eps_soft=1e-10` split is spec'd only if shadow is adopted | non-CLM spec params; ties to CLM-01 context |
| G-02 | Collocation points-per-trajectory diverges: review §5.1 ~256/traj vs issue-03 16/traj (4096/256) | Owner sets the collocation count; FUT calibration | CLM-12 (claimed) |
| G-03 | M16 scaling-rule direction unsettled and conflicts with review §5.3 (no scaling) | Keep ctl deferral; FUT empirical evidence on whether/which direction to scale | CLM-20 (claimed); CLM-17 (verified inputs) |
| G-04 | `stage_strat_revision.md` Table 4 dissolves the locked fidelity-stage roles (Stage 2/5 gold) | Constrain adaptive criteria to preserve gold-stage roles + gold-counterpart contract; cluster only *within* fidelity strata | item 7; Step 5 gold-counterpart; CLM-15 |
| G-05 | Population safeguard threshold inconsistent: issue-03 ">10%" vs stage_strat "5%" | Owner sets the merge threshold | CLM-02..07 context (claimed) |
| G-06 | Scale factor `s` persistence for `Q_norm = Q_raw/s^3` is unclear (data-side) | Confirm `s` stored in trajectory metadata, else estimate post-hoc; if neither, exclude `Q` for the quasi-random set | sampling_method (s in [0.8,1.2], Sobol u4) |
| G-07 | `review_of_framework.md` §4.3 AD reference uses the forbidden ones-covector pattern | Replace with the PHYS-02 componentwise contract upstream | PHYS-02 (pinn §5.3.1) |
| G-08 | `review_of_framework.md` §2.2 softening uses the additive `(||r||+eps)` form | Use §2.2's *value* argument only; the additive *form* is superseded by the locked matched-Plummer | item 4 (PHYS-03) |
| G-09 | Causal-exponent underflow clip bound is unset in the spec | Owner/FUT sets the numeric clip (the spec itself asks to "surface a gap") | non-CLM spec param |
| G-10 | NS-13 Huber `delta` value depends on unmeasured `|ΔH|` quantiles | FUT-calibrate `delta` from observed `|ΔH|`; default 0.1 pending | `delta` revisable |

No `claimed-unverified` figure (`CLM-01`–`CLM-13`, `CLM-20`, and the stage counts) is treated as
fact anywhere above; each is recorded as a claim and, where verdict-relevant, FUT-flagged. The
`verified` anchors used as fact are `CLM-14`–`CLM-19` (and `VF-1`–`VF-5`).

---

## 9. Coverage map (finding -> adjudication phase -> primary spec-edit target)

Per `resolution-doc-skeleton.md` (non-binding); every framed question has a verdict slot above.

| Finding cluster | Findings | Phase | Primary spec-edit target |
|-----------------|----------|-------|--------------------------|
| Cross-source root-cause | 1.1, 1.2, 1.3, 2.1 (the `D` conflict; the three named decisions) | 32 | both targets, as adjudicated |
| Curriculum / staging / `tau_L` / `L_max` / transitions | 2.2, 3.3 (M6), 3.4 (M7), 3.8 (D5), 4 (adaptive) | 33 | `ctl_instruction.md` |
| Training-loop mechanics | 3.1 (B-07), 3.2 (B-08), 3.9 (NS-12), 5 (ALM clamp) | 34 | `ctl_instruction.md` + `pinn_architecture.md` |
| Loss scaling / weights / clipping / softening | 3.5 (M14), 3.6 (M15), 3.7 (M16), 3.10 (NS-13), 3.11 (NS-18) | 35 | `pinn_architecture.md` |
| Source-issue / cross-reference reconciliation | §6 baseline-report corrections; FUT hand-off (G-01..G-10) | 36 (FUT) | both targets / FUT |

*This document is research output informing the framework owner's resolution doc; it prescribes no
schema and adopts the v1.4/v1.5 resolution docs only as format precedents. Locked sub-parts are
not re-opened; unverified figures are recorded as claims, not facts.*
