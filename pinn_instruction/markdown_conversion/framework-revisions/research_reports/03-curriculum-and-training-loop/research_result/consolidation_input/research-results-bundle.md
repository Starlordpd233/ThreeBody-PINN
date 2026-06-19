===================================================================
DERIVED PACKAGING ARTIFACT — DO NOT EDIT BY HAND
Issue 03 final consolidation — research results
-------------------------------------------------------------------
Each file below is framed by OUTER markers that carry a per-build
nonce token  ISSUE03-SECTION-<nonce>.  ONLY those nonce-bearing
markers delimit sections; every byte between them is verbatim.
-------------------------------------------------------------------
Contents (tag | bytes | sha256/12 | self-bundle):
  R1   |    57819 | d696b601f0eb | no
  R2   |    47478 | c1a12efe49da | no
  R3   |    55221 | 7a877b20bf2d | no
  R4   |    42645 | 10ee26b34975 | no
  R5   |    11132 | ba2cbe8174e4 | no
  R6   |    48267 | 34e45c41d97d | no
  R7   |    26170 | bfecf583dffb | no
===================================================================

===== BEGIN ISSUE03-SECTION-f26fed61251ff665 REPORT R1 (57819 bytes, sha256 d696b601f0eb) =====
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

===== END ISSUE03-SECTION-f26fed61251ff665 REPORT R1 =====

===== BEGIN ISSUE03-SECTION-f26fed61251ff665 REPORT R2 (47478 bytes, sha256 c1a12efe49da) =====
---
title: doc-03 Curriculum and Training Loop — Research Adjudication
role: external-research adjudication output (feeds the v1.6 resolution doc, Phases 32–36)
status: draft for framework-owner review
created: 2026-06-18
scope: answers every question in framed-research-questions.md, under the SCOPE-12 hard constraints
sources_worked: RESEARCH-CONTEXT-MASTER.md; scope-12-hard-constraints.md; framed-research-questions.md;
  resolution-doc-skeleton.md; claims-register.md; verified-facts-reference.md; consolidated-context.md;
  03-curriculum-and-training-loop.md; ctl_instruction.md; pinn_architecture.md; sampling_method.md;
  review_of_framework.md; stage_strat_revision.md
---

# doc-03 Adjudication — Curriculum and Training Loop

This adjudicates the open questions in `framed-research-questions.md` against the framework
specs (`ctl_instruction.md`, `pinn_architecture.md`), under the locked SCOPE-12 constraints,
treating `03-curriculum-and-training-loop.md` (the issue doc) and the two baseline reports
(`review_of_framework.md`, `stage_strat_revision.md`) as non-authoritative subjects. Every
figure is referenced by its `CLM-NN` row. Where the sources are silent or ambiguous I say so
and log the gap (consolidated in the closing register addendum) rather than inventing a value.

Two findings cut across many questions and are stated once up front, because several
individual verdicts depend on them.

## Cross-cutting finding C1 — the issue doc's "global + ALM is the current SOT" is doubly wrong

The issue doc repeatedly treats Option B (global time sampling + dense ALM, no causal
weighting) as the standing state of truth — in `03-curriculum-and-training-loop.md` §"D-04",
§"Causal Training Mismatch", and §"Open Decisions". That framing fails on two independent
grounds:

First, it misreads its own cited source. `review_of_framework.md §5.1` ("Unifying Data and
Collocation Point Sampling") unifies the two *point sets* (data points ∪ collocation points)
into a single forward pass for efficiency; it says nothing about replacing causal weighting
with global ALM. The temporal-weighting decision and the point-set-unification decision are
orthogonal, and §5.1 settles only the latter. The issue doc's claim that §5.1 "describes a
single forward pass with global ALM, confirming Option B as the SOT default" reads a verdict
into §5.1 that is not there.

Second, and decisively, the *current* spec adopts causal weighting and rejects dense ALM.
`ctl_instruction.md` §"Loss Function Formulation" / "Phase 2: Total Training Loss" makes
causal weighting $w_n = \exp(-\eta_c \sum_{m<n}\mathrm{stopgrad}(\bar R_m))$, $\eta_c = 1$
the PHYS-05 default, and explicitly rejects the pseudo-ALM term
$L_{\mathrm{data}} + \lambda_p L_{\mathrm{phys}} + (\mu_p/2)L_{\mathrm{phys}}^2 + \lambda_E L_{\mathrm{energy}}$
as "not a standard equality-constrained augmented Lagrangian." `pinn_architecture.md §3.2`,
§4.1, and §4.2 carry the same causal-weighting default and confine ALM to an optional P2
scalar-constraint ablation (default OFF). So the spec baseline is *closer to a causal regime
than to Option B*, and the issue doc's "Option B is current SOT" premise is contradicted by
the spec-edit targets the adjudication is supposed to govern. This reframes the causal-mode,
M15, and μ_p-clamp questions below.

## Cross-cutting finding C2 — `review_of_framework.md` is a superseded baseline on several contracts

`review_of_framework.md` is the older "resolution blueprint." On several specific contracts
the current specs have already moved past its recommendations, and the issue doc sometimes
cites the blueprint as if it were live. Where they conflict, the specs govern
(`scope-12-hard-constraints.md §2`). The concrete supersessions, each used below:

- Softening (`review_of_framework.md §2.2`): recommends $\epsilon_{\mathrm{soft}} = 10^{-5}$
  *everywhere* and, worse, implements it in the **additive** form
  $1/(\lVert r\rVert + \epsilon)$ and $1/(\lVert r\rVert + \epsilon)^3$. Both are now wrong:
  the spec adopts a dual-context arrangement (offline $\epsilon_{\mathrm{inv}} = 10^{-10}$,
  loss-side $\epsilon_{\mathrm{train}} = 10^{-5}$), and the additive form is the **PHYS-03
  anti-pattern, explicitly prohibited** in favor of the matched-Plummer
  $r_{\mathrm{safe}} = \sqrt{\lVert\Delta r\rVert^2 + \epsilon^2}$
  (`scope-12-hard-constraints.md` item 4; `ctl_instruction.md` Step 3 item 1 / §2.5;
  `pinn_architecture.md §3.2`).
- Energy weight (`review_of_framework.md` consolidated table): $\lambda_E$ up to $10^3$ at
  chaotic stages — the very magnitude M15 objects to. The spec PHYS-05 schedule caps
  $\lambda_E^{\max}$ at $1$ (`pinn_architecture.md §4.1`).
- Componentwise AD (`review_of_framework.md §4.3`): its reference implementation calls
  `torch.autograd.grad(..., grad_outputs=torch.ones_like(...))`, which is exactly the
  summed-output VJP anti-pattern PHYS-02 forbids (`pinn_architecture.md §5.3.1`).
- Dense ALM (`review_of_framework.md §4.2`): documents the dense-residual pseudo-ALM that the
  spec rejects (`ctl_instruction.md` Loss Function Formulation; `pinn_architecture.md §4.2`).

The blueprint's surviving, still-correct contributions (the $L_{\max}$ formula, the
replay/lookahead and 50/50 batch protocol, the curriculum-aware $C$ schedule, ALM state-reset
at stage boundaries) are noted where relevant.

---

# Section 2 — Decisions requiring framework-owner approval

## The causal-training-mode decision — options posed, none recommended

**Verdict: unsettled; escalate to the framework owner.** I state all three options and do not
pick one, per the prompt. What the adjudication *can* settle is the framing the owner decides
under, which finding C1 corrects.

- **Option A — per-time-step causal weighting**, $w_i \propto \exp(-\lambda\sum_{j<i}L_j)$.
  Issue-doc risk: a "Causal Firewall," where an early stiffness spike zeros all later weights.
- **Option B — global sampling + dense ALM**, no causal weighting. Issue-doc risk:
  temporal-causality violation; late-time gradients propagate through unresolved early dynamics.
- **Option C — time-windowed causal-ALM hybrid**: overlapping causal windows, localized ALM,
  hard convergence gating, state propagation. Most complex; the issue doc presents it as
  resolving both failure modes but as an end-to-end rewrite of the Adam phase.

Reconciliation note the owner needs (finding C1): the current spec is **not** at Option B. It
already runs causal weighting as the PHYS-05 default and has rejected dense ALM
(`ctl_instruction.md` Loss Function Formulation; `pinn_architecture.md §3.2`, §4.1, §4.2).
Reading the options through that lens, the live baseline is essentially Option A's
causal-weighting mechanism *without* the dense-ALM machinery either A-as-issue-framed or B
would add. Therefore: choosing A is largely a *ratification + hardening* of the existing
default (it mainly needs the causal-exponent underflow-clip bound that Phase 19 explicitly
left open — see gap G1); choosing B is a **reversion** that would reintroduce the rejected
dense ALM and must be recorded as an intentional departure from PHYS-05, not as "keeping the
SOT"; choosing C is a genuine new architecture that supersedes both. The issue doc's request to
"record Option B as an intentional departure from the blueprint" is correct in spirit but
mislabeled — under the current spec, B departs from the *spec's causal default*, not merely
from the Causal-Training-Mismatch blueprint.

Sources: `framed-research-questions.md` §"causal-training-mode"; `03-curriculum-and-training-loop.md`
§"D-04" / §"Causal Training Mismatch" / §"Open Decisions"; `ctl_instruction.md` "Loss Function
Formulation"; `pinn_architecture.md §3.2`, §4.1, §4.2; `review_of_framework.md §5.1`.
No dataset figure gates this (`framed-research-questions.md` notes "Figures referenced: none").

## The s_min-frame decision — options posed; spec baseline is Option A

**Verdict: unsettled (owner approval required), but the spec baseline already implements
Option A and is internally consistent.** I state both options without forcing one.

- **Option A** (matches the spec): unsoftened geometric $s_{\min}$ for the curriculum stage
  gate; $\max(s_{\min}, \epsilon_{\mathrm{soft}} = 10^{-5})$ inside the training-loss collision
  criterion; always log the unsoftened value.
- **Option B**: softened $\max(s_{\min}, \epsilon)$ everywhere.

Grounding: `ctl_instruction.md` Step 3 item 1 defines $s_{\min}$ from "true pairwise
separations (no softening)" — an explicitly unsoftened geometric quantity — while the static
invariant potential uses the Plummer form with $\epsilon_{\mathrm{inv}} = 10^{-10}$ and the
training residual/energy use $\epsilon_{\mathrm{train}} = 10^{-5}$ (`pinn_architecture.md §3.2`,
§3.4). The spec therefore already separates the unsoftened geometric gate from the softened
loss potentials, exactly as Option A describes. The issue doc agrees this is "documentation
cleanup," and the choice is a ratification with zero methodology change if Option A is kept.
This decision is distinct from the D5 stage-transition finding (both legitimately appear).

Sources: `framed-research-questions.md` §"s_min-frame"; `03-curriculum-and-training-loop.md`
§"D-05" / §"Considered Alternatives"; `ctl_instruction.md` Step 3 item 1, Stage 6 gate;
`pinn_architecture.md §3.2`, §3.4.

## The epsilon-strategy decision — only the static-context reconciliation is open

**LOCKED (not re-opened):** the training-loss-side softening $\epsilon_{\mathrm{soft}} = 10^{-5}$,
applied identically in the physics residual and energy regularizer (`scope-12-hard-constraints.md`
item 4; `claims-register.md` CLM-19 companion / PHYS-03). I do not frame any sub-question as
"which loss-side epsilon is correct."

**Verdict on the OPEN part: the spec baseline is already Option B (dual-context), and it is the
defensible resolution; I pose Options A and C without forcing the owner.** The open question is
whether the offline static/invariant softening $\epsilon_{\mathrm{inv}} = 10^{-10}$ (used for
$E$, $Q$, stage assignment, in float64) legitimately coexists with the locked loss-side
$10^{-5}$.

- **Option A** — collapse static invariants to $10^{-5}$ too. Trade-off: changes the
  ground-truth invariant computation to softened physics. Its support comes from
  `review_of_framework.md §2.2`, which is superseded (finding C2): §2.2 both argues for
  "$10^{-5}$ everywhere" *and* writes the prohibited additive form, so it cannot be adopted as
  written.
- **Option B (dual-context)** — keep $\epsilon_{\mathrm{inv}} = 10^{-10}$ offline and the
  locked $10^{-5}$ in the loss. This is precisely the current spec: `ctl_instruction.md` Step 3
  item 1 states $\epsilon_{\mathrm{inv}} = 10^{-10}$ is "context-specific for offline invariant
  computation and is distinct from the training-time softening $\epsilon_{\mathrm{train}} = 10^{-5}$,"
  and `pinn_architecture.md §3.4` adds the dual-epsilon visibility note. The trade-off the issue
  doc flags (gate and loss operate on slightly different physics) is real but bounded: at
  scaled separations of order unity, $10^{-10}$ and $10^{-5}$ both affect only the deep
  close-encounter tail, and the offline value runs in float64 where $10^{-10}$ is not
  negligible — undercutting the double-precision argument that was aimed at the *loss* side.
- **Option C** — tighten everything to $10^{-10}$. The issue doc itself records the scientific
  argument against this (indistinguishable from zero in the GPU/float32 loss path). Not advisable.

The issue doc's "internal SOT contradiction" (one source says $10^{-5}$ for all, another uses
$10^{-10}$, with a truncated justification) is real *between the issue doc's cited sources* but
is **already resolved in the current spec**: the spec keeps the dual-context split with the loss
side locked. The truncated $10^{-10}$ justification in `ctl_instruction.md` §"Step 3"
"Numerical notes" ("…is a safe default in scaled units and does not [enter $s_{\min}$ or any
denominator besides $V$]") is in fact *completable from the same file* — the following clause
states it does not enter $s_{\min}$ or any denominator besides $V$ — so the apparent
incompleteness is a rendering/transcription artifact, not a missing decision.

Context note (not part of the decision): the framework actually carries *more* than two ε
contexts. `sampling_method.md §2.2` uses an IC-generation collision-avoidance threshold
$\epsilon \approx 0.05$, and §"Stage 3" uses `MIN_DISTANCE_THRESHOLD = 0.01`; the $\tau_L$
shadow-trajectory routine uses a split $\epsilon_{\mathrm{pert}} = 10^{-8}$ /
$\epsilon_{\mathrm{soft}} = 10^{-10}$. These are distinct generation-time and
diagnostic-time quantities and must not be folded into the loss-side $10^{-5}$.

Sources: `framed-research-questions.md` §"epsilon-strategy"; `scope-12-hard-constraints.md`
items 4, §3; `03-curriculum-and-training-loop.md` §"D-06"; `ctl_instruction.md` Step 3 item 1 +
"Numerical notes"; `pinn_architecture.md §3.2`, §3.4; `review_of_framework.md §2.2`;
`sampling_method.md §2.2`; `claims-register.md` CLM-19.

---

# Section 3 — Confirmed findings (BLOCKING and MAJOR)

## B-07 — replay/lookahead batch construction

**Verdict: confirmed; the spec already encodes the contract, and the gap is in the legacy
code, not the spec.** `ctl_instruction.md` §"Mini-Batch Construction with Lookahead Sampling"
specifies replay $B_{\leq k} = 240$ and lookahead $B_{k+1} = 16$ for batch size 256,
`n_pts(traj) = min(n_pts_cap, n_snapshots(traj))` with `n_pts_cap` default 32, and the 50/50
composition realized as $k_w = \lfloor n_{\mathrm{pts}}/2\rfloor$ acceleration-norm-weighted
draws (Gumbel-top-k) plus uniform draws, all without replacement. `pinn_architecture.md §3.1`
still shows the legacy `get_batch(batch_size, points_per_trajectory=32)` with the author note
that it "is not consistent with the CTL instruction plan" (also logged as SI-PINN-003). So B-07
is real, but it is a *code-vs-spec* gap that the spec resolves in its own favor: adopt the
`ctl_instruction.md` mini-batch contract; the `points_per_trajectory=32` literal in
`pinn_architecture.md §3.1` is a code default, not the contract (the file's PIPE-04 note says
so explicitly).

The replay/lookahead/point counts (240 / 16 / 8192 / 4096) are claimed design constants
(`CLM-12`, `claimed-unverified`); no v1.6 phase verifies them, so they enter the spec as design
choices to be FUT-calibrated, not as established facts. One reconciliation point: the
audit §6 pseudocode draws data points 50/50 over a *fixed* 32 (`n_u = n_w = 16`), while the
`ctl_instruction.md` contract caps at `min(32, n_snapshots)` — these agree only when a
trajectory has ≥32 snapshots, which is not guaranteed for the standard variant (verified median
61, but a population median, not a per-file floor — `CLM-16`). Prefer the `min(·)` form.

Sources: `framed-research-questions.md` §"B-07"; `03-curriculum-and-training-loop.md` B-07,
§6.2; `ctl_instruction.md` Mini-Batch Construction; `pinn_architecture.md §3.1` + SI-PINN-003;
`claims-register.md` CLM-12, CLM-16.

## B-08 — data-fidelity vs collocation point separation

**Verdict: confirmed; make the two-independent-set discipline explicit in the batch
constructor, but reconcile two divergences.** The spec already carries distinct roles —
`pinn_architecture.md §3.1` (data-fidelity term, $N_{\mathrm{data}} = 256\times32 = 8192$) and
§3.2 (physics residual on collocation points) — but does not pin a *separate, independently
sampled* collocation set with its own count into the batch constructor. The B-08 fix (8192
data-fidelity + 4096 collocation, both 50/50) is a coherent way to make that explicit.

Two reconciliations the owner must note. (i) The *data loss* metric diverges: B-08/issue-doc
says L1 on the data-fidelity set, but `pinn_architecture.md §3.1` now specifies a **Huber**
data contract ($\delta_r = 1$, "the previous MAE/L1 data-loss prose is replaced by this Huber
contract"). The spec's Huber governs (this is the same conflict as NS-18 below). (ii) The
*collocation count per trajectory* diverges across sources: the issue-doc batch pseudocode uses
16/trajectory ($256\times16 = 4096$, `CLM-12`), whereas `review_of_framework.md §5.1` gives an
illustrative 256/trajectory. Both are example values; the 4096-total figure is
`claimed-unverified` (`CLM-12`), so adopt it as a design default to be FUT-calibrated, and
record the §5.1 figure as a non-binding illustration rather than a competing contract.

Sources: `framed-research-questions.md` §"B-08"; `03-curriculum-and-training-loop.md` B-08, §6.1;
`pinn_architecture.md §3.1`, §3.2; `review_of_framework.md §5.1`; `claims-register.md` CLM-12.

## M6 — `L_norm` clamping before IC-vector mapping

**Verdict: the M6 framing is obsolete; the clamp is no longer required for IC bounds and is at
most an optional staging-diagnostic guard.** M6 assumes $L_{\mathrm{norm}}$ is mapped into an IC
slot via $2x-1$, so a value $>1$ would push the IC component out of range. Under the locked 14D
$[\tau, IC_{13}]$ contract, $L_{\mathrm{norm}}$ is **not** an IC slot: `ctl_instruction.md`
Step 3 outputs it as metadata, and Step 4 / the Network input contract list the invariant-heavy
descriptors (including $L_{\mathrm{norm}}$) as "curriculum, diagnostics, loss-scaling, and
reporting metadata… not final network IC slots." So the out-of-range-IC failure mode M6 guards
against cannot occur.

What remains: $L_{\mathrm{norm}} = L/L_{\max} \ge 0$ always (both magnitudes are non-negative),
but can exceed 1 numerically because $L_{\max}$ is an approximate characteristic scale, not a
strict bound. The Stage-0 gate uses $L/L_{\max} > 0.5$, which a clamp at 1 does not affect; the
lower clamp at 0 is redundant given non-negativity. Note the two reference implementations
already disagree: the spec `compute_L_norm` returns $L/(L_{\max}+\epsilon)$ **without** a clip,
while the issue-doc `compute_L_norm` wraps it in `np.clip(..., 0, 1)`. Recommendation to pose:
keep the spec's unclamped metadata value as the stored quantity (so diagnostics see true
ratios, including $>1$ outliers), and apply any clamp only at the point of use if a downstream
consumer needs a bounded $[0,1]$ feature — not globally.

Sources: `framed-research-questions.md` §"M6"; `03-curriculum-and-training-loop.md` M6;
`ctl_instruction.md` Step 3 item 2, Step 4 / Network input contract.

## M7 — `τ_L` excluded from the IC vector

**Verdict: confirmed by design; no change needed.** `ctl_instruction.md` Step 3 returns
$\tau_L$ in the invariant tuple and uses $(E, Q, s_{\min}, L_{\mathrm{norm}}, \tau_L)$ for
default stage gating, while Step 4 / the Network input contract explicitly exclude the
invariant-heavy descriptors (including $\tau_L$) from the final $IC_{13}$ slots, consistent
with the locked 14D Jacobi-state contract (`scope-12-hard-constraints.md` items 1–2). The
issue-doc recommendation — exclude $\tau_L$ from the IC vector (a derived dynamical property,
not an IC invariant), retain it for staging/evaluation — matches the spec exactly. The only
spec action is to record that this exclusion is intentional (the issue doc notes no documented
decision existed); the verdict supplies it.

Sources: `framed-research-questions.md` §"M7"; `03-curriculum-and-training-loop.md` M7;
`ctl_instruction.md` Step 3, Step 4 / Network input contract; `scope-12-hard-constraints.md`
items 1–2.

## M14 — merged gradient clipping

**Verdict: confirmed; merge as $\text{clip} = C_{\mathrm{stage}}\cdot\mathrm{median}(\text{grad
norm history})$, with the per-stage $C$ schedule governing and the fixed $5.0$ retired to a
special case.** The two halves M14 wants merged exist in different files:
`pinn_architecture.md §4.4` clips at $5.0\times\mathrm{median}$ of the last 100 gradient norms
(a single fixed factor), while `ctl_instruction.md` §"Adaptive Median-Based Gradient Clipping"
gives the curriculum-aware schedule (stages 0–1: 7–10; 2–3: 5; 4–6: 3). The merge is the
issue-doc form, and it subsumes both: the per-stage $C$ replaces the fixed $5.0$, with $5.0$
recovered as the stage-2–3 value. So the reconciliation is to treat `pinn_architecture.md §4.4`'s
$5.0$ as the stage-2–3 instance of the `ctl_instruction.md` schedule and edit §4.4 to reference
$C_{\mathrm{stage}}$ rather than a constant.

The issue-doc $C\_table = \{0\!-\!1\!:8.5, 2\!-\!3\!:5.0, 4\!-\!6\!:3.0\}$ (`CLM-10`,
`claimed-unverified`) is a numeric *instantiation* of the spec's 7–10/5/3 schedule: 8.5 is the
midpoint of 7–10 (the same midpoint `review_of_framework.md §5.4` picks). The spec's stage 0–1
entry is a **range** (7–10), not a point; whether to lock a single value (8.5) or keep the range
is the open sub-question. The numeric $C\_table$ is unverified, so adopt the schedule shape from
the spec and treat 8.5 as a within-range default to be calibrated, not as a fact.

Sources: `framed-research-questions.md` §"M14"; `03-curriculum-and-training-loop.md` M14,
§"Gradient Clipping — Merged Specification"; `pinn_architecture.md §4.4`; `ctl_instruction.md`
Adaptive Median-Based Gradient Clipping; `review_of_framework.md §5.4`; `claims-register.md` CLM-10.

## M15 — energy-loss weight schedule (capped hybrid vs PHYS-05 warmup)

**Verdict: a genuine three-way divergence; the spec PHYS-05 schedule is the live baseline and
is already far below the magnitude M15 worries about, so the capped-hybrid table is not needed
as a safety measure — but the dominance safeguard is worth keeping.** The three positions:

- Spec (`pinn_architecture.md §4.1`, PHYS-05):
  $\lambda_E^{\max}(k) = \{0\ \text{for}\ k\in\{0,1\};\ 10^{k-4}\ \text{for}\ k\in\{2,3,4\};\ 1\ \text{for}\ k\in\{5,6\}\}$,
  i.e. max value $1$, with linear warmup over $I_{\mathrm{warm}} = \min(2000, 0.1 N_{\mathrm{Adam},k})$.
- Issue-doc (`CLM-11`): capped hybrid $\lambda_E(k) = \min(10^{k-3}, \text{cap}[k])$,
  $\text{cap} = \{0\!:1, 1\!:5, 2\!:20, 3\!:50, 4\!:100, 5\!:200, 6\!:500\}$, plus a safeguard
  that halves $\lambda_E$ when energy is already well-conserved.
- Baseline blueprint (`review_of_framework.md` consolidated table): $\lambda_E$ up to $10^3$.

The issue-doc cap_table is a *middle* position between the blueprint's $10^3$ and the spec's
$1$. M15's premise — "$\lambda_E = 1000$ at Stage 6 risks overwhelming the data/physics terms" —
is aimed at the blueprint magnitude (finding C2), which the spec has **already abandoned** by
capping $\lambda_E^{\max}$ at $1$. So the spec is not exposed to the failure M15 describes, and
adopting the cap_table (peaking at 500) would *raise* the late-stage energy weight relative to
the current spec, not lower it. The defensible resolution is to keep the PHYS-05 schedule and
**not** import the cap_table; the one issue-doc element worth porting is the runtime dominance
safeguard (reduce $\lambda_E$ when $\lambda_E L_{\mathrm{energy}}$ dominates $L_{\mathrm{data}}$),
which is orthogonal to the schedule values. The cap_table figures are `claimed-unverified`
(`CLM-11`); do not treat them as fact.

Sources: `framed-research-questions.md` §"M15"; `03-curriculum-and-training-loop.md` M15,
§"Energy Loss Weight Schedule"; `pinn_architecture.md §4.1`; `review_of_framework.md`
consolidated table; `claims-register.md` CLM-11.

## M16 — `dt_out`-aware collocation scaling

**Verdict: confirmed in the audit-verbatim direction $n_{\mathrm{col}} \propto dt_{\mathrm{base}}/dt_{\mathrm{out}}$;
the spec carries the hook but defers the rule to doc-03, so this is where it lands.**
`ctl_instruction.md` §"Mini-Batch Construction" exposes `n_snapshots(traj)` and `dt_out(traj)`
as loader metadata and labels the collocation-density question a "deferred, forward-interface"
item ("not used here"). The M16 fix supplies the deferred rule. The per-variant $dt_{\mathrm{out}}$
are **verified** (`CLM-17`: standard 0.17, hierarchical base 0.08, gold 0.01), so the *direction
and inputs* are grounded; the derived scaling factors (gold $1\times$, hierarchical-base
$\approx 0.125\times$, standard-base $\approx 0.059\times$ for $dt_{\mathrm{base}} = 0.01$) are
`claimed-unverified` (`CLM-20`) — the rule itself, not the $dt_{\mathrm{out}}$ values, is the
unverified part. Flag explicitly (as the issue doc does) that the *inverse* form
$dt_{\mathrm{out}}/dt_{\mathrm{base}}$ would be a separate methodology change, not a
residual-finding correction, and is out of scope unless the owner opens it. Note the stage-table
$dt_{\mathrm{out}}$ entries in the issue-doc Stage Inventory (Stage 0/1 = 0.08, Stage 3/4 = 0.17,
etc.) are consistent with `CLM-17`.

Sources: `framed-research-questions.md` §"M16"; `03-curriculum-and-training-loop.md` M16;
`ctl_instruction.md` Mini-Batch Construction; `verified-facts-reference.md` VF-1;
`claims-register.md` CLM-17, CLM-20.

## D5 — stage-transition criteria; dual-path fallback

**Verdict: confirmed direction (add a fallback path); the spec currently has only the strict
path, and the proposed thresholds are explicitly hypotheses.** `ctl_instruction.md` §"Stage
Transition Criteria" lists exactly four strict criteria — training-loss plateau
($\epsilon_{\mathrm{plateau}} = 10^{-5}$, patience 200, $\beta = 0.98$); validation-loss
stability; physics residual ($\epsilon_{\mathrm{phys}} = 10^{-4}$); energy drift
($\epsilon_{\mathrm{energy}} = 10^{-4}$, using the locked $\epsilon_H = 10^{-4} S_H$ floor) —
and carries the author note questioning their attainability with limited data, but encodes **no**
fallback path and **no** per-stage threshold table. D5's dual-path advance (strict + fallback on
max-epochs / stagnation / NaN rollback, with a Stage-0 pilot to calibrate) is a coherent
addition that the spec's own author note invites.

Two reconciliations. (i) D5 also *relaxes* the strict path's validation criterion: the spec
requires $\mathcal{L}_{\mathrm{val}}(i) \le \min_{j\le i}\mathcal{L}_{\mathrm{val}}(j)$ (true
minimum), while D5's Path A2 uses $\le \mathrm{percentile}_{10}$ ("relaxed from min"). That is a
change to a *revisable* criterion, in scope, but it should be called out as a relaxation of the
strict path, not only as a fallback addition. (ii) The per-stage thresholds
($\epsilon_{\mathrm{phys}}/\epsilon_{\mathrm{energy}}$, $5\times10^{-3}\!\to\!10^{-4}$,
`CLM-08`) and the `MAX_EPOCHS` table ($\{0\!:500\ldots 6\!:1200\}$, `CLM-09`) are
`claimed-unverified` design hypotheses the issue doc itself marks "not fixed." No v1.6 phase
verifies them; adopt the dual-path *structure* and flag the threshold tables for FUT calibration
via the Stage-0 pilot rather than locking the numbers.

Sources: `framed-research-questions.md` §"D5"; `03-curriculum-and-training-loop.md` D5, §6.3,
§"Stage Transition Criteria (D5)"; `ctl_instruction.md` Stage Transition Criteria;
`claims-register.md` CLM-08, CLM-09.

## NS-12 — componentwise AD for velocities/accelerations

**Verdict: confirmed; `pinn_architecture.md §5.3.1` (PHYS-02) fully satisfies NS-12, and it is
the issue-doc's own cited fix that is partly outdated.** PHYS-02 is the canonical componentwise
normalized-time AD contract: it requires all nine $dr'_{i,\alpha}/du$, **forbids** the
`torch.autograd.grad(r.sum(), u, …)` summed-output VJP anti-pattern, lists acceptable patterns
(`jacrev`+`vmap`, explicit per-component loop, full-Jacobian), and gives a worked
synthetic-trajectory derivative test
($r'(u) = [\sin 2\pi u, \cos 2\pi u, u^2]$ with symbolic $dr'/du$, $d^2r'/du^2$). That is a
complete answer to "no concrete three-body implementation given." The catch worth recording:
the issue doc routes the fix to "the component-wise AD requirement in 01," and the older
`review_of_framework.md §4.3` reference implementation uses
`torch.autograd.grad(..., grad_outputs=torch.ones_like(network_output_r))` — which is exactly
the all-ones-covector VJP PHYS-02 forbids. So PHYS-02 governs and §4.3's snippet is superseded
(finding C2). No open three-body collocation-batch detail remains beyond the executable
tolerance/probe, which PHYS-02 defers to Phase 21 VER-04 / AC-PHYS-02.

Sources: `framed-research-questions.md` §"NS-12"; `03-curriculum-and-training-loop.md` NS-12;
`pinn_architecture.md §5.3.1`; `review_of_framework.md §4.3`.

## NS-13 — Huber energy δ

**Verdict: a real three-way split, posed; the shared argument is sound, and whether δ becomes
stage-dependent is the substantive open sub-question.** Positions:

- Spec (`pinn_architecture.md §3.4`, PHYS-04): Huber transition $\delta = 1.0$, on
  $\Delta H_n$ normalized by $|H_\epsilon(r_0)| + \epsilon_H$ with the locked
  $\epsilon_H = 10^{-4} S_H$ floor.
- Issue-doc (NS-13): tune $\delta$ from observed normalized $|\Delta H|$ quantiles, starting
  $\approx 0.01\!-\!0.1$, per stage (`delta = clip(quantile(|ΔH|, 0.75), 0.01, 0.1)`).
- Baseline blueprint (`review_of_framework.md §4.4`): a single fixed $\delta = 0.1$.

All three accept the same premise: with normalized residuals typically $\ll 1$, $\delta = 1.0$
makes Huber behave like L2 over the whole expected range, defeating its outlier robustness. The
disagreement is only the value and whether it is global, fixed-small, or stage/quantile-adaptive.
None of these is a dataset figure (the spec's $\delta = 1.0$ is a PHYS-04 design parameter, not
a CLM row — confirmed by `claims-register.md` "Non-dataset figures (excluded by design)"). So
this is a design call, not a verification question: pose $\delta = 1.0$ (spec) vs a calibrated
$\delta \in [0.01, 0.1]$ (issue-doc, possibly stage-dependent) vs fixed $0.1$ (blueprint), and
note that making $\delta$ stage-dependent couples it to the same per-stage calibration as D5's
thresholds. I do not force a value; the calibration target ($|\Delta H|$ quantiles) is only
observable from a pilot run.

Sources: `framed-research-questions.md` §"NS-13"; `03-curriculum-and-training-loop.md` NS-13,
§"Huber Delta for Normalized Energy"; `pinn_architecture.md §3.4`; `review_of_framework.md §4.4`;
`claims-register.md` Row Notes (non-dataset figures).

## NS-18 — loss-component scaling/units contract

**Verdict: confirm a single dimensionless scaling contract across the three terms; the one
substantive reconciliation is the data-loss metric (L1/MAE vs Huber), resolved in the spec's
favor.** The terms already share a units contract across `pinn_architecture.md §3.1` (data,
Huber on scaled positions $r' = r/D$), §3.2 (physics residual on collocation points,
$\epsilon_{\mathrm{train}} = 10^{-5}$, causal weighting), §3.4 (energy, same
$\epsilon_{\mathrm{train}}$), and §4.1 (PHYS-05 composition). The locked pieces — $D \approx 4.6416$
(`CLM-19`) and $\epsilon_{\mathrm{soft}} = 10^{-5}$ — fix the coordinate system, so NS-18 is
mostly a documentation consolidation. The genuine divergence: NS-18 (and the issue-doc Loss
Component Scaling Contract table) specify $L_{\mathrm{data}}$ with **L1/MAE**, whereas
`pinn_architecture.md §3.1` now uses a **Huber** data contract ($\delta_r = 1$, explicitly
replacing the earlier MAE/L1 prose). The spec governs (`scope-12-hard-constraints.md §2`): the
contract is Huber on scaled positions, not L1. (This is the same data-loss point that surfaces
under B-08.) Everything else in the issue-doc contract — scaled positions for data,
componentwise-AD accelerations with $d^2r'/du^2 = 4\,d^2r'/d\tau^2$ on the $\tau$-leaf path,
$dr'/du = 2\,dr'/d\tau$ for energy, shared collocation set and shared $\epsilon_{\mathrm{train}}$ —
matches the spec.

Sources: `framed-research-questions.md` §"NS-18"; `03-curriculum-and-training-loop.md` NS-18,
§"Loss Component Scaling Contract"; `pinn_architecture.md §3.1`, §3.2, §3.4, §4.1, §5.3.1;
`claims-register.md` CLM-19.

---

# Section 6 — data-driven adaptive stage assignment

**Verdict: the adaptive methodology can *augment* the threshold-based Step 5 as the issue doc
proposes, but `stage_strat_revision.md`'s Phase-IV table cannot be adopted wholesale — it
conflicts with the locked/spec stage structure on Stage 2 and disagrees with the issue doc on
the population safeguard.** Three things to reconcile.

First, the methodology itself (EDA over invariants, correlation/PCA, K-means $k = 6\!-\!7$,
quantile thresholds, a small PINN pilot, augmenting rather than replacing
`assign_curriculum_stage()`) is compatible with the locked stage-query contracts: PIPE-01..10
(`sample_replay`, `sample_lookahead`, `has_stage`) operate on the admitted set by integer stage
index and are agnostic to *how* stages are assigned, provided the result is non-empty stages
keyed 0–6 (`scope-12-hard-constraints.md` item 7; `ctl_instruction.md` §"Data-side stage-query
interface"). So adaptive assignment does not, by itself, violate the locked interface.

Second, there is a real structural conflict between the two non-authoritative sources.
`stage_strat_revision.md` Phase IV (Table 4) assigns **Stages 2–6 all to quasi-random clusters**
(Stage 2 = "cluster with highest median $\tau_L$"), whereas both the spec and the issue-doc Stage
Inventory keep **Stage 2 = high-resolution hierarchical refinement (Set 2a)**, with quasi-random
data not entering until Stage 3 (`ctl_instruction.md` §"Multi-Stage Data Stratification",
Stage 2; `03-curriculum-and-training-loop.md` Stage Inventory). Adopting Table 4 verbatim would
silently delete the spec's hierarchical-refinement stage and reassign its data source — a change
that also interacts with the locked Stage-5 gold-counterpart obligation (every Stage-4-admitted
ID owes a Stage-5 gold sample; the 184 standard IDs without a gold counterpart are genuine
Stage-5 holes — `ctl_instruction.md` Step 5 / GAP-26-01; `CLM-14`). So the adaptive method may
re-bin *within* the quasi-random block and refine quantile boundaries, but it must preserve the
hierarchical-refinement role of Stage 2 and the locked Stage-5 gold semantics. I flag Table 4's
Stage-2 reassignment as a conflict to be resolved *against* the spec, not adopted.

Third, the population safeguard diverges: the issue doc mandates ">10% per stage," while
`stage_strat_revision.md` Phase IV says "≥5% of the total dataset (e.g.)." These are different
thresholds for the same merge rule. Neither is locked; pose both and let the owner set it, noting
the merge must not drop any stage below the `has_stage(k)` requirement or violate the Stage-5
obligation.

The per-stage trajectory counts (Stage 0 ~1,200 … Stage 6 unknown) are issue-doc design outputs
of the *adaptive* method and are `claimed-unverified` (`CLM-02`..`CLM-07`); no v1.6 phase
verifies them, so they are inputs, not facts. The ~2,565 gold count that appears alongside them
*is* verified, but it is `CLM-15` (a gold count), not a stage count.

Sources: `framed-research-questions.md` §"Adaptive stage-assignment"; `03-curriculum-and-training-loop.md`
§"Data-Driven Adaptive Stage Assignment", Stage Inventory; `ctl_instruction.md` Multi-Stage Data
Stratification, Step 5, Data-side stage-query interface; `stage_strat_revision.md` Part III,
Phase IV / Table 4; `scope-12-hard-constraints.md` item 7; `claims-register.md` CLM-02..CLM-07,
CLM-14, CLM-15; `consolidated-context.md` Fragment C.

---

# Section 7 — `τ_L` / `L_max` formulas and the `D` conflict

## `D = 6.694` vs `D ≈ 4.6416` (the worked seed-conflict)

**LOCKED:** $D \approx 4.6416$, $D = (G T^2)^{1/3}$, raw-mass convention, with $G = 1$
(`scope-12-hard-constraints.md` item 6; `ctl_instruction.md §2.5`; `CLM-19`, verified). The
total-mass form $D = (G M_{\mathrm{tot}} T^2)^{1/3} \approx 6.694$ ($M_{\mathrm{tot}} = 3$) was
rejected by v1.5 Phase 25 EVID-10 and is a future-only rewrite. "Which $D$ is correct" is
settled; I do not re-open it.

**Verdict on the OPEN part (reconciliation under the locked $D$): the $D = 6.694$ in the
issue-doc `compute_tau_L` is both wrong *and* inert, so the formulas re-derive identically under
$D \approx 4.6416$ with no numerical change downstream.** This is the key technical observation.
Inspect `03-curriculum-and-training-loop.md` §"τ_L and L_max Formula Resolution": the
`compute_tau_L` routine computes `D = np.cbrt(G * M_tot_ref * T_scale**2)` $= 6.694$ and
`V = D / T_scale` at the top — but neither `D` nor `V` is ever referenced again in the function.
The `rhs` integrand uses the input `masses`, `pos`, `vel` directly, and the inputs `r_prime`,
`v_prime` arrive **already scaled** by the upstream pipeline (which scales by the locked
$D \approx 4.6416$, `ctl_instruction.md §2.5`). So `D = 6.694` is a dead, mislabeled annotation;
deleting it or correcting it to $4.6416$ changes no computed value in the routine.

More generally, $D$ does **not appear explicitly** in either the $L_{\max}$ or the $\tau_L$
formula. $L_{\max} = M_{\mathrm{tot}}\, r_{\mathrm{char}}\, v_{\mathrm{char}}$ with
$r_{\mathrm{char}} = \tfrac13\sum_{i<j}\lVert r'_i - r'_j\rVert$ and
$v_{\mathrm{char}} = \sqrt{2|E|/M_{\mathrm{tot}}}$ is computed entirely from already-scaled
$r', v', E$ (`ctl_instruction.md` Step 3 item 2). $\tau_L$ is computed from the divergence of
scaled trajectories. The locked $D$ enters only one place — upstream, in producing $r', v'$ —
and once that scaling is the locked $4.6416$, every invariant and stage threshold is in the
locked code units. Therefore the reconciliation is clean: remove/correct the inert `D = 6.694`
line, confirm inputs are scaled by the locked $D$, and $L_{\max}$, $L_{\mathrm{norm}}$, $\tau_L$,
and the stage thresholds ($L/L_{\max} > 0.5$, $\tau_L > 5$, $2 < \tau_L \le 5$,
$s_{\min}$/$E$ gates) re-derive **unchanged**. No downstream stage-threshold consequence follows
from the $D$ correction, *provided* no one re-derived thresholds under the 6.694 scaling — and
the spec confirms the thresholds are tied to the locked raw-mass scaling.

Both values are registered so the conflict is fully captured: $6.694$ is `CLM-01`
(`claimed-unverified`, verdict-gating), $4.6416$ is `CLM-19` (verified/locked).

Sources: `framed-research-questions.md` §"D = 6.694 vs D ≈ 4.6416"; `scope-12-hard-constraints.md`
item 6, §3; `03-curriculum-and-training-loop.md` §"τ_L and L_max Formula Resolution",
`compute_tau_L`; `ctl_instruction.md §2.5`, Step 3 item 2; `claims-register.md` CLM-01, CLM-19;
`consolidated-context.md` Fragment E.

## `τ_L` and `L_max` computation formulas

**Verdict: $L_{\max}$ is settled and consistent across all three sources; the $\tau_L$ *method*
is genuinely divergent (three estimators) and the time-unit convention is ambiguous — adopt
$L_{\max}$ now, and resolve the $\tau_L$ estimator choice and units before locking
$\tau_L$-keyed thresholds.**

$L_{\max} = M_{\mathrm{tot}}\, r_{\mathrm{char}}\, v_{\mathrm{char}}$,
$v_{\mathrm{char}} = \sqrt{2|E|/M_{\mathrm{tot}}}$, $L_{\mathrm{norm}} = L/L_{\max}$ is identical
in `ctl_instruction.md` Step 3 item 2, the issue-doc `compute_L_norm`, and
`review_of_framework.md §1.1`. No conflict; adopt it (the spec already calls it "canonical").

The $\tau_L$ estimator, by contrast, differs across the three sources, and the spec's own
estimator differs from the issue-doc's primary method:

- Spec (`ctl_instruction.md` Step 3 item 5): a **Rosenstein-style** estimator operating directly
  on the BRUTUS trajectory — uniform-cadence resampling, delay-coordinate embedding (e.g.
  $d = 5$), nearest neighbors with a Theiler window, divergence-curve slope $\Rightarrow$
  $\lambda_{\max}$, $\tau_L = 1/\lambda_{\max}$ (with $\tau_L = \infty$ if $\lambda_{\max} \le 0$).
- Issue-doc (`compute_tau_L`): a **shadow-trajectory / Benettin-style** integration — perturb by
  $\epsilon_{\mathrm{pert}} = 10^{-8}$, integrate nominal + perturbed, renormalize, with static
  potential softening $\epsilon_{\mathrm{soft}} = 10^{-10}$ — *plus* a faster "PCA+Rosenstein"
  batch approximation for ~15K trajectories.
- Baseline blueprint (`review_of_framework.md §1.1`): a **Benettin** single-perturbation-vector
  algorithm, $\epsilon_{\mathrm{pert}} \approx 10^{-8}$, $\tau_L = 1/\lambda$.

These are not interchangeable: the spec estimates $\lambda_{\max}$ from existing trajectory data
(no re-integration), while the issue-doc/blueprint re-integrate a perturbed shadow. The
issue-doc's "shadow-trajectory primary + Rosenstein batch approximation" inverts the spec's
"Rosenstein primary." This is a methodology choice the owner must make; both are defensible, but
they will give different $\tau_L$ distributions and therefore shift the Stage-4a/4b boundaries
($\tau_L > 5$, $2 < \tau_L \le 5$).

A unit ambiguity compounds it (gap G2): the spec returns $\tau_L = 1/\lambda_{\max}$, while the
issue-doc `compute_tau_L` returns $\tau_L = T_{\mathrm{scale}}/\lambda_{\max}$ with
$T_{\mathrm{scale}} = 10$ — an extra factor of 10. Whether the stage thresholds "$\tau_L > 5$ /
$2$–$5$ code units" are expressed in scaled time ($1/\lambda$) or rescaled time
($T_{\mathrm{scale}}/\lambda$) is not pinned anywhere in the attached set, so the two estimators
are not even on the same axis. This must be resolved before any $\tau_L$ threshold is locked;
I log it rather than guess a convention.

Finally, do **not** collapse the shadow-trajectory split softening
($\epsilon_{\mathrm{pert}} = 10^{-8}$, $\epsilon_{\mathrm{soft}} = 10^{-10}$) into the locked
loss-side $10^{-5}$ — these are distinct diagnostic-time contexts (`framed-research-questions.md`
§"τ_L"; `scope-12-hard-constraints.md §3`). They are also distinct from each other:
$\epsilon_{\mathrm{pert}}$ is a perturbation magnitude, $\epsilon_{\mathrm{soft}}$ a potential
softening.

Sources: `framed-research-questions.md` §"τ_L and L_max"; `03-curriculum-and-training-loop.md`
§"τ_L and L_max Formula Resolution"; `ctl_instruction.md` Step 3 items 2 and 5;
`review_of_framework.md §1.1`; `scope-12-hard-constraints.md §3`.

---

# Section 15 — the ALM `μ_p`-clamp finding

**Verdict: the clamp $[10^{-4}, 100.0]$ attaches to the surviving P2 scalar-constraint ALM
ablation if that ablation is used; in the default baseline (ALM OFF, dense-residual ALM
rejected) the clamp lands nowhere.** The issue doc's $\mu_p = \mathrm{np.clip}(\mu_p, 10^{-4},
100.0)$ lives inside the dense-residual ALM update
(`03-curriculum-and-training-loop.md` §"ALM Parameter Update Specification", §6.2) — the very
formulation the spec rejects (`ctl_instruction.md` Loss Function Formulation;
`pinn_architecture.md §4.2`). Because dense-residual ALM is not in the baseline, the clamp has no
home in the default loss. ALM survives only as a P2 ablation on **scalar** conservation
constraints ($c_E = \mathrm{RMS}_n(\Delta H_n)$, $c_{L,\alpha} = \mathrm{RMS}_n(\cdot)$), default
OFF, with dual updates only between Adam epochs or between refinement passes and never inside
L-BFGS (`pinn_architecture.md §4.2`). So:

- If the P2 ablation is enabled, the clamp's intent (lower bound prevents the penalty parameter
  decaying to zero and disabling constraint enforcement; upper bound prevents it overwhelming
  the data term) applies to that ablation's penalty parameter, and is a reasonable guard.
- Its placement must follow the P2 update *cadence*, not the issue-doc's per-iteration dense-ALM
  loop: the clamp is applied at the between-epoch dual update, consistent with §4.2 (and with the
  ALM state-reset-at-stage-boundary discipline in `review_of_framework.md §4.2`, which survives
  even though that section's dense-ALM context does not).

State both positions as the framed question asks: the issue-doc places the clamp in the dense
update; the spec confines any ALM (and therefore the clamp) to the optional P2 scalar-constraint
ablation. Adopt the latter placement.

Sources: `framed-research-questions.md` §"ALM μ_p clamp"; `03-curriculum-and-training-loop.md`
§"ALM Parameter Update Specification", §6.2; `ctl_instruction.md` Loss Function Formulation;
`pinn_architecture.md §4.2`; `review_of_framework.md §4.2`.

---

# Claims-register addendum — gaps and FUT flags

Per the prompt, where the attached set is silent or ambiguous I record the gap against the
relevant register row rather than inventing. New gap entries and reaffirmed FUT flags:

- **G1 — causal-exponent underflow-clip bound (open by spec design).** `pinn_architecture.md
  §4.1` and `ctl_instruction.md` Loss Function Formulation both require clipping the causal
  exponent to avoid underflow but explicitly decline to choose the numeric bound ("Phase 19 does
  not choose a numeric clipping bound; surface a gap if execution requires one"). No CLM row;
  this is a spec parameter left open. Resolve only if the causal mode (Option A or C) is adopted.
- **G2 — `τ_L` time-unit convention unpinned.** The stage thresholds "$\tau_L > 5$ / $2$–$5$ code
  units" are not tied to a specific time axis; the spec returns $1/\lambda_{\max}$ while the
  issue-doc returns $T_{\mathrm{scale}}/\lambda_{\max}$ (factor of 10). No attached file resolves
  which axis the thresholds use. Must be fixed before locking any $\tau_L$-keyed boundary;
  FUT (couples to whichever $\tau_L$ estimator is chosen).
- **G3 — collocation count per trajectory divergent.** Issue-doc 16/trajectory (4096 total,
  `CLM-12`) vs `review_of_framework.md §5.1` 256/trajectory; both illustrative, neither verified.
  Adopt the `CLM-12` design default, FUT-calibrate.
- **G4 — Stage-2 data-source conflict.** Spec/issue Stage 2 = hierarchical-gold refinement vs
  `stage_strat_revision.md` Table 4 Stage 2 = quasi-random cluster. Resolve against the spec;
  relates to `CLM-02`..`CLM-07` (stage populations) and the locked Stage-5 gold obligation.
- **G5 — population safeguard threshold.** ">10%" (issue doc) vs "≥5%" (`stage_strat_revision.md`
  Phase IV). Owner sets; not locked.
- **Reaffirmed `claimed-unverified` (no v1.6 verification phase — `claims-register.md`):**
  `CLM-01` (6.694, rejected/registered only), `CLM-02`..`CLM-07` (stage counts),
  `CLM-08`/`CLM-09` (D5 thresholds / max-epochs), `CLM-10` (C_table), `CLM-11` (λ_E cap_table),
  `CLM-12` (replay/lookahead/point counts), `CLM-20` (M16 scaling factors). Treat all as
  design hypotheses to be FUT-calibrated, not facts.
- **Verified anchors used as fact:** `CLM-14` (184 gold-gap), `CLM-15` (~2,565 gold),
  `CLM-16` (median snapshots 61/127/1003), `CLM-17` (`dt_out` 0.17/0.08/0.01),
  `CLM-19` ($D \approx 4.6416$).

# What stands vs what is open — one-line summary

Settled under the constraints: M7 (τ_L excluded by design), NS-12 (PHYS-02 satisfies it),
the $L_{\max}$/$L_{\mathrm{norm}}$ formula, the data-loss-is-Huber resolution (B-08/NS-18), the
$D$ reconciliation (6.694 is wrong and inert; nothing changes under the locked $D$), and the
direction of B-07, M14, M16, D5 (spec carries the contract or the hook; adopt with the noted
reconciliations). Genuinely open for the owner: the causal-training-mode decision (A/B/C, with
B correctly relabeled as a departure from the spec's causal default), the s_min frame
(spec = Option A), the epsilon strategy (spec = dual-context Option B), the energy-weight
schedule (spec PHYS-05 vs issue cap_table vs blueprint $10^3$), the Huber δ (1.0 vs calibrated
0.01–0.1 vs 0.1), the τ_L estimator choice and its unit convention (gap G2), and the adaptive
stage-assignment boundaries with the Stage-2 conflict and population safeguard (gaps G4–G5).

===== END ISSUE03-SECTION-f26fed61251ff665 REPORT R2 =====

===== BEGIN ISSUE03-SECTION-f26fed61251ff665 REPORT R3 (55221 bytes, sha256 7a877b20bf2d) =====
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

===== END ISSUE03-SECTION-f26fed61251ff665 REPORT R3 =====

===== BEGIN ISSUE03-SECTION-f26fed61251ff665 REPORT R4 (42645 bytes, sha256 10ee26b34975) =====
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

===== END ISSUE03-SECTION-f26fed61251ff665 REPORT R4 =====

===== BEGIN ISSUE03-SECTION-f26fed61251ff665 REPORT R5 (11132 bytes, sha256 ba2cbe8174e4) =====
Based on the provided transport package, I have adjudicated the open questions for the doc-03 ("Curriculum and Training Loop") revision. This assessment strictly honors the SCOPE-12 hard constraints, treats the framework specs (`ctl_instruction.md`, `pinn_architecture.md`) as the source of truth, and evaluates the non-authoritative issue doc (`03-curriculum-and-training-loop.md`) against that baseline.

---

### Executive Summary & Hard Constraint Acknowledgment
All reconciliations below are bounded by the **SCOPE-12 Hard Constraints** (`scope-12-hard-constraints.md`). Crucially:
1.  **Network Input**: The 14D `[τ, IC₁₃]` vector is locked. Invariant-heavy descriptors are metadata, not network inputs.
2.  **Loss-Side Softening**: `eps_soft = 1e-5` is locked for the training loss (PHYS-03).
3.  **Characteristic Length**: `D ≈ 4.6416` (raw-mass convention) is locked (PHYS-01). The issue doc's `D = 6.694` is rejected.
4.  **Source of Truth**: Live-code citations in the issue doc are overridden; the framework specs govern.

---

### Section 2: Decisions Requiring Human Approval

#### 1. The Causal-Training-Mode Decision
*   **Issue-Doc Premise**: Frames a choice between Option A (causal), Option B (global + ALM), and Option C (hybrid), claiming Option B is the "current SOT."
*   **Framework-Spec Reality**: The issue doc's premise is **factually incorrect**. `ctl_instruction.md` ("Loss Function Formulation") explicitly *rejects* the dense-residual pseudo-ALM formulation and adopts **causal weighting** ($w_n = \exp(-\eta_c \sum \dots)$) as the PHYS-05 default. `pinn_architecture.md` (§3.2, §4.1) mirrors this. ALM is confined to a P2 ablation for *scalar* conservation constraints only.
*   **Adjudication**: The spec baseline is already **Option A** (Causal Weighting without dense ALM). The framework owner must decide whether to retain the spec's Option A, adopt the issue doc's Option C (Time-Windowed Hybrid, which requires an end-to-end rewrite of the Adam phase), or intentionally regress to Option B (Global + ALM).
*   **Spec-Edit Target**: `ctl_instruction.md` (Phase 2: Total Training Loss) and `pinn_architecture.md` (§3.2).

#### 2. The `s_min`-Frame Decision
*   **Issue-Doc Position**: Proposes Option A (unsoftened geometric gate, softened loss) vs. Option B (softened everywhere).
*   **Framework-Spec Reality**: `ctl_instruction.md` (Step 3) explicitly defines $s_{min}$ from "true pairwise separations (no softening)" for the geometric gate, while using $\varepsilon_{inv} = 10^{-10}$ for the static potential and the locked $\varepsilon_{train} = 10^{-5}$ for the training loss.
*   **Adjudication**: The spec **already implements Option A**. The geometric stage gate uses unsoftened $s_{min}$ to honestly flag close encounters, while the network only ever sees softened physics.
*   **Recommendation**: Confirm Option A as the locked spec baseline. No spec edit is required, only documentation reinforcement.

#### 3. The Epsilon-Strategy Decision
*   **Locked Constraint**: Loss-side `eps_soft = 1e-5` (PHYS-03).
*   **Open Question**: Reconcile the static/invariant-computation softening (`1e-10` vs `1e-5`).
*   **Framework-Spec Reality**: The specs already utilize a **Dual-Context** arrangement. `ctl_instruction.md` (Step 3) and `pinn_architecture.md` (§3.4) explicitly separate the offline static invariant softening ($\varepsilon_{inv} = 10^{-10}$) from the dynamic training loss ($\varepsilon_{train} = 10^{-5}$).
*   **Adjudication**: The spec baseline is **Option B (Dual-Context)**. The owner must decide if this scientific split is acceptable, or if the static invariant computation (which dictates stage assignment) should be collapsed to the locked `1e-5` (Option A), thereby altering the physics of the curriculum gates.

---

### Section 3: Confirmed Findings (BLOCKING and MAJOR)

| Finding | Adjudication & Reconciliation | Spec-Edit Target |
| :--- | :--- | :--- |
| **B-07** (Replay/Lookahead) | **Aligned.** `ctl_instruction.md` ("Mini-Batch Construction") already specifies 240 replay, 16 lookahead, and $n_{pts} = \min(cap, snapshots)$ with a 50/50 split. The issue doc's claim that this is "not implemented" applies to legacy code, which is overridden. | None required (Implementation must follow spec). |
| **B-08** (Data vs. Collocation) | **Aligned but needs explicit constructor contract.** `pinn_architecture.md` separates the data term (§3.1, $N=8192$) and physics residual (§3.2). The spec must explicitly mandate that the batch constructor draws these as *independent* point sets to prevent conflation. | `ctl_instruction.md` (Unified Batch Construction). |
| **M6** ($L_{norm}$ clamping) | **Obsolete.** The issue doc claims $L_{norm}$ needs clamping before IC-vector mapping. However, per the locked 14D input constraint, `ctl_instruction.md` (Step 4) explicitly removes $L_{norm}$ from the network input vector; it is now metadata. Clamping is irrelevant to the NN, though it may be retained for staging logic. | None. |
| **M7** ($\tau_L$ excluded) | **Aligned.** Both the issue doc and `ctl_instruction.md` (Step 4) exclude $\tau_L$ from the $IC_{13}$ vector, retaining it strictly for stage gating and evaluation metadata. | None. |
| **M14** (Gradient Clipping) | **Merge Required.** `pinn_architecture.md` (§4.4) uses a fixed `5.0 * median`, while `ctl_instruction.md` defines a per-stage `C` schedule (7-10 / 5 / 3). The spec must be edited to merge these: `clip_value = C_stage * median(grad_history)`. | `pinn_architecture.md` (§4.4). |
| **M15** (Energy Weight) | **Conflict.** Issue doc proposes a `cap_table` (**CLM-11**). Spec (`pinn_architecture.md` §4.1, PHYS-05) uses a linear warmup schedule $\lambda_E^{max}(k)$. Owner must select which schedule governs late-stage training. | `pinn_architecture.md` (§4.1). |
| **M16** ($dt_{out}$ Scaling) | **Hook exists, rule missing.** `ctl_instruction.md` exposes $dt_{out}$ as metadata but defers the scaling rule. Owner must adopt a rule (e.g., $n_{col} \propto dt_{base}/dt_{out}$ using verified **CLM-17** values) and encode it in the spec. | `ctl_instruction.md` (Mini-Batch Construction). |
| **D5** (Stage Transitions) | **Fallback Missing.** Spec lists 4 strict criteria but lacks the dual-path fallback and per-stage thresholds (**CLM-08**, **CLM-09**) proposed by the issue doc. The spec must be edited to include the fallback path to prevent infinite loops. | `ctl_instruction.md` (Stage Transition Criteria). |
| **NS-12** (Componentwise AD) | **Aligned.** `pinn_architecture.md` (§5.3.1, PHYS-02) already mandates componentwise AD and explicitly forbids the summed-output proxy anti-pattern. | None. |
| **NS-13** (Huber $\delta$) | **Conflict.** Issue doc suggests tuning $\delta$ to `0.01-0.1`. Spec (`pinn_architecture.md` §3.4) fixes $\delta = 1.0$. Owner must decide whether to keep the spec baseline or adopt quantile-tuning. | `pinn_architecture.md` (§3.4). |
| **NS-18** (Loss Scaling) | **Misframed by Issue Doc.** Issue doc demands an L1/MAE data-loss contract. Spec (`pinn_architecture.md` §3.1) already has a strict scaling contract but uses **Huber** for the data term. The spec's Huber contract stands under the locked $D$ and $\varepsilon_{train}$. | None. |

---

### Section 6: Data-Driven Adaptive Stage Assignment
*   **Issue-Doc Position**: Proposes replacing fixed thresholds with PCA/K-means clustering and quantile-based boundaries.
*   **Framework-Spec Reality**: `ctl_instruction.md` (Step 5) relies on fixed theoretical thresholds (e.g., $E < -0.5$, $s_{min} > 2$).
*   **Adjudication**: This is a fundamental methodology shift. The owner must decide whether to retain the deterministic threshold tables or replace them with the data-driven methodology.
*   **GAP LOGGED**: The deep-dive methodology report (`stage_strat_revision.md`) referenced in the prompt's master and the framed questions **is not attached** in the knowledge base. I cannot evaluate the exact clustering mechanics or population safeguards without it.

---

### Section 7: $\tau_L$, $L_{max}$, and the $D$ Conflict

#### The $D$ Conflict (Worked Seed-Conflict)
*   **Locked Constraint**: $D \approx 4.6416$ (raw-mass, PHYS-01, **CLM-19**).
*   **Issue-Doc Claim**: $D = 6.694$ (total-mass, **CLM-01**).
*   **Adjudication**: The issue doc's $D=6.694$ is definitively rejected. All downstream formulas must be reconciled under $D \approx 4.6416$.

#### $\tau_L$ and $L_{max}$ Computation Formulas
*   **Issue-Doc Position**: Provides a shadow-trajectory routine for $\tau_L$ utilizing split epsilons ($\varepsilon_{pert} = 10^{-8}$, $\varepsilon_{soft} = 10^{-10}$).
*   **Framework-Spec Reality**: `ctl_instruction.md` (Step 3) defines $L_{max}$ but lacks the shadow-trajectory $\tau_L$ routine.
*   **Adjudication**: The spec must be edited to inline the $\tau_L$ shadow-trajectory contract. Crucially, this routine must be mathematically re-derived to use the locked raw-mass scaling ($D \approx 4.6416$) rather than the issue doc's total-mass scaling. The split static-softening context ($\varepsilon_{soft} = 10^{-10}$) must be preserved and kept distinct from the locked loss-side $\varepsilon_{train} = 10^{-5}$.
*   **GAP LOGGED**: The attached texts state *that* the $\tau_L$ derivation must be reconciled under $D \approx 4.6416$, but they **do not provide the explicit re-derived mathematical equations or code block** for the shadow trajectory scaling under the raw-mass convention. This derivation is required from the framework owner.

---

### Section 15: ALM $\mu_p$ Clamp
*   **Issue-Doc Position**: Proposes clamping $\mu_p \in [10^{-4}, 100.0]$ to prevent divergence.
*   **Framework-Spec Reality**: The spec explicitly rejects dense-residual ALM. ALM survives *only* as a P2 ablation for scalar conservation constraints (`pinn_architecture.md` §4.2).
*   **Adjudication**: The $\mu_p$ clamp is irrelevant to the baseline training loop. It should be provisionally adopted **only** for the P2 scalar-constraint ALM ablation.
*   **Spec-Edit Target**: `pinn_architecture.md` (§4.2 Optional ALM Ablation).

---

### Registered Gaps & Missing Evidence
The following items are logged as gaps where the attached materials are silent or missing, preventing full autonomous resolution:

1.  **Missing Baseline Report**: `stage_strat_revision.md` is referenced in the `RESEARCH-CONTEXT-MASTER.md` and `framed-research-questions.md` but is **not included** in the attached knowledge base. The data-driven adaptive staging methodology (Section 6) cannot be fully adjudicated without it.
2.  **Missing Mathematical Derivation**: The exact transformed equations for the $\tau_L$ shadow-trajectory perturbation and integration under the locked raw-mass convention ($D \approx 4.6416$) are not present in the text (Section 7).
3.  **Unverified Design Hypotheses**: The per-stage threshold tables (**CLM-08**) and `MAX_EPOCHS` schedules (**CLM-09**) required for the D5 dual-path fallback are `claimed-unverified` design hypotheses in the issue doc. The spec currently lacks them entirely; they must be empirically calibrated by the owner during the Stage-0 pilot.
===== END ISSUE03-SECTION-f26fed61251ff665 REPORT R5 =====

===== BEGIN ISSUE03-SECTION-f26fed61251ff665 REPORT R6 (48267 bytes, sha256 34e45c41d97d) =====
# Adjudication Report: Curriculum and Training Loop (CTL) Revision for the Three-Body PINN Framework

## Adjudication Framework and Epistemological Baselines

The formulation of a Curriculum and Training Loop (CTL) for a Physics-Informed Neural Network (PINN) designed to model the extreme chaotic dynamics of the three-body problem necessitates absolute rigor in managing multi-fidelity data, physical invariants, and gradient optimization protocols.[1] The present adjudication targets the "doc-03" framework revision, addressing profound structural contradictions between diverse documentation branches.[1] To systematically isolate architectural truths from uncalibrated design hypotheses, this evaluation operates under a strict, non-negotiable hierarchy of evidentiary precedence.

The adjudication architecture strictly invalidates the authority of live implementation code and issue documentation when they conflict with finalized framework specifications or historically locked mathematical boundaries.[1] The overarching constraints dictate that the framework specifications—primarily encompassing `ctl_instruction.md` and `pinn_architecture.md`—function as the singular, unyielding source of truth.[1] The non-authoritative issue document (`03-curriculum-and-training-loop.md`) and its associated resolution proposals are treated strictly as auditing materials requiring rigorous adjudication, rather than serving as authoritative implementation manuals.[1] Consequently, any invocation of live implementation scripts, such as `data-processing-pipeline-full.py` or `basic_architecture.py`, is unilaterally overridden by the written specifications, reflecting the principle that live code often harbors technical debt or unverified experimental branches that have not survived formal peer scrutiny.[1]

Furthermore, all architectural reasoning operates entirely beneath the boundary conditions established by the "SCOPE-12" hard constraints.[1] These constraints define locked mathematical outcomes from previous v1.4 and v1.5 validation phases, which cannot be reopened, contradicted, or renegotiated.[1] Any findings, stage transitions, batch constructions, or loss-scaling dynamics that form the "revisable baseline" must be mapped strictly within these fixed boundaries.[1]

A critical component of this epistemological framework is the treatment of numerical figures, population metrics, and transition thresholds. To maintain empirical integrity, all figures are presumed to be unverified claims unless they are actively backed by a committed dataset verdict logged within the formal verification pipeline.[1]

| Data Classification Paradigm | Treatment Protocol | Evidentiary Requirement |
|---|---|---|
| **SCOPE-12 Hard Constraints** | Immutable. All derivations must reconcile under these parameters. | Explicitly codified in `scope-12-hard-constraints.md` (e.g., 14D input, raw-mass length scale). |
| **Framework Specifications** | Authoritative baseline. Subject to revision only via formal adjudication of open research questions. | Present within `ctl_instruction.md` or `pinn_architecture.md`. |
| **Claimed-Unverified Figures** | Treated as untested design hypotheses. Excluded from foundational mathematical derivations. | Labeled `claimed-unverified` in the claims register (e.g., specific epoch tables, stage trajectory populations). |
| **Verified Facts** | Foundation for downstream calculations and empirical metrics. | Grounded by v1.5 DATA verdicts and designated as `verified` (e.g., verified median trajectory snapshots). |
| **Issue Document Proposals** | Evaluated critically. Subordinate to specifications. Often containing known errors or theoretical mismatches. | Contained within `03-curriculum-and-training-loop.md` or associated baseline reports. |

Where the underlying authoritative specifications are silent, truncated, or ambiguous concerning a specific architectural configuration, the evidentiary gap is explicitly documented.[1] Under no circumstances are synthetic resolutions, fabricated variables, or approximated thresholds injected into the structural logic to force a localized resolution.[1]

## Kinematic Non-Dimensionalization and Dimensionality Constraints

The fundamental stability of the continuous neural representation is directly predicated upon the accurate non-dimensionalization of celestial kinematics. Raw physical trajectories of three-body interactions span immense numerical magnitudes, guaranteeing severe catastrophic gradient failures and vanishing activations if fed into standard network architectures without rigorous preprocessing. The framework standardizes these inputs via scaling relationships parameterized by a characteristic length scale and predefined structural projection vectors.

### The Characteristic Length Scale Dispute

A foundational theoretical dispute exists regarding the appropriate normalization constant utilized to convert dimensional astronomical unit ranges into well-behaved code units.[1] The non-authoritative issue documentation argues for a characteristic length scale of $D = 6.694$, an assumption registered as the unverified claim CLM-01.[1] The derivation supporting this figure stems from a total-mass scaling formulation defined mathematically as $D = (G \cdot M_{tot\_ref} \cdot T^2)^{1/3}$, inherently assuming a reference total mass of $M_{tot\_ref} = 3.0$ and an arbitrary temporal scaling constant of $T_{scale} = 10$.[1]

Rigorous adjudication invalidates this total-mass paradigm completely. As established by the locked SCOPE-12 hard constraints (Item 6), and corroborated by the v1.5 Phase 25 documentation (EVID-10), the total-mass formulation was explicitly examined and formally rejected as an invalid scaling parameter for the present architecture.[1] The framework instead enforces the raw-mass non-dimensionalization convention, which yields $D = (G \cdot T^2)^{1/3} \approx 4.6416$ under the assumption that the gravitational constant $G = 1$.[1]

| Normalization Parameter | Formulation | Computed Value | Epistemological Status | Adjudicated Ruling |
|---|---|---|---|---|
| **Total-Mass Derivation** | $D = (G \cdot M_{tot\_ref} \cdot T^2)^{1/3}$ | 6.694 | CLM-01 (`claimed-unverified`) | **Rejected.** Contradicts Phase 25 EVID-10 validation. |
| **Raw-Mass Derivation** | $D = (G \cdot T^2)^{1/3}$ | $\approx 4.6416$ | CLM-19 (`verified`) | **Locked.** SCOPE-12 Hard Constraint. Mandatory for all downstream scaling. |

This raw-mass length scale ($D \approx 4.6416$) operates as an immutable boundary.[1] Therefore, all subsequent curriculum calculations, including the normalization of angular momentum metrics, spatial separation boundaries, and the derivation of predictable predictability horizons, must be reconstructed utilizing the raw-mass length scale to maintain topological consistency.[1]

### Continuous Temporal Domain Mapping

Neural architectures employing periodic activation functions, such as the SIREN networks designated for this implementation, exhibit maximum phase stability and optimal frequency generalization when inputs are constrained to a symmetric numerical boundary.[1] Consequently, the framework mandates the standardization of spatiotemporal normalization, specifically targeting the temporal input array.[1]

The physical integration time $t$ spans the interval $[0, T]$, where the characteristic maximal simulation time equates to $T = t_{\max} = 10$ code units.[1] To align this interval with the optimal neural domain, the continuous physical time $t$ undergoes an affine transformation mapping it to the normalized continuous range $[-1, 1]$.[1] This mapping is executed via the formalized temporal equation $t' = 2(t/T) - 1$.[1] In the context of PyTorch Automatic Differentiation operations, the intermediate temporal ratio $u = t/T$ operates as the foundational autograd leaf, ensuring that derived velocities and accelerations cleanly propagate through the chain rule mechanisms linking the continuous time domain to the spatial coordinates.[1]

### Neural Input Architecture and Spatial Projection

The neural architecture strictly defines its input manifold to maintain physical determinism.[1] Under SCOPE-12 Constraint 1, the continuous PINN input is locked strictly to a 14-dimensional vector, encoded as $[ \tau, IC_{13} ]$.[1] The first dimension captures the scaled temporal coordinate $\tau$ (structurally equivalent to $t'$), establishing the continuous evaluation point for the network.[1] The subsequent 13 dimensions encapsulate the initial physical condition state, parameterized through a fixed-gauge Jacobi-state encoding.[1]

This $IC_{13}$ vector is synthesized through a highly regulated, locked preprocessing pipeline designed to eliminate redundant translational artifacts and rotational degrees of freedom.[1] The data undergoes rigorous center-of-mass (COM) removal, receives a zero-momentum inertial boost, and is organized into canonical spatial ordering under a canonical rotation gauge.[1] While this specific representation retains mathematically redundant elements relative to the minimal necessary phase-space coordinates, its reconstructive properties were explicitly locked during Phase 19 (PHYS-06) development.[1]

To complement the constrained input, the output spatial tensor is similarly governed by structural mechanics.[1] SCOPE-12 Constraint 3 mandates the application of a hard, mass-weighted center-of-mass projection head applied immediately to the raw 9D position output predicted by the network layers.[1] Crucially, this projection head is executed before the evaluation of any mathematical loss or gradient metric.[1] By forcing the spatial coordinates to satisfy barycentric equilibrium fundamentally, linear momentum conservation is structurally embedded into the manifold output itself.[1] This architectural design entirely bypasses the need for soft-penalty regularizations regarding linear momentum conservation, increasing the robustness of the residual physics loss.[1]

## Fundamental Physical Metrics and Parallel Scale Computations

The transition from dimensional celestial trajectories to a curriculum-ready tensor framework requires the global calculation of structural constraints across the entire dataset manifold.[1] To effectively stratify the curriculum, the architecture identifies defining physical invariants characterizing the initial system configuration at $t = 0$.[1] The processing of over 15,000 dense trajectory files demands significant computational throughput to extract the foundational constants without inducing hardware bottlenecks.[1]

The framework resolves this through a fully parallelized computational orchestrator leveraging native multi-processing.[1] The primary execution loop (`compute_globals`) distributes independent integration matrices across a process pool array.[1] Individual workers parse localized state vectors from designated flat-text initial condition records (e.g., `ic_hierarchical_*.txt`).[1] Each record contains exactly 21 floating-point dimensions corresponding to the flat sequence $[m_1, \mathbf{r}_1, \mathbf{v}_1, m_2, \mathbf{r}_2, \mathbf{v}_2, m_3, \mathbf{r}_3, \mathbf{v}_3]$.[1]

Once mapped to continuous dimensionless units utilizing the raw-mass $D$ scaling parameter, the workers isolate total mechanical energy matrices ($E$) and calculate characteristic interaction length boundaries ($r_{char}$) derived natively from mean pairwise distances.[1] The orchestrator subsequently aggregates the complete localized distributions, utilizing stable median calculations to bypass extreme chaotic outliers.[1] The derived global bounding parameters emerge as $E_{scale} = |\text{median}(\{E_j\})| + 10^{-8}$ and $s_{min\_scale} = \text{median}(\{r_{char,j}\})$.[1]

### Normalized Angular Momentum and Matrix Clamping Analysis

The dynamical stability of an arbitrary three-body configuration relies heavily on the distribution of angular momentum relative to the total bounding energy.[1] A system demonstrating maximum possible angular momentum for a given discrete energy state structurally collapses into highly predictable, near-circular planar orbits.[1] Conversely, a massive deficit in angular momentum forces the celestial masses into highly eccentric, plunging radial interactions that precipitate immediate chaotic breakdown and unpredictable scattering.[1]

To capture this property systematically, the framework computes the total angular momentum magnitude ($L$) utilizing standard cross-product mechanics applied to scaled coordinates: $\mathbf{L} = \sum m_i (\mathbf{r}'_i \times \mathbf{v}'_i) \rightarrow L = \|\mathbf{L}\|$.[1] This magnitude is subsequently mapped against the theoretical topological maximum ($L_{max}$), defined mathematically via total system properties: $L_{max} = M_{total} \cdot r_{char} \cdot v_{char}$.[1] The characteristic velocity limit is itself constrained by binding energy representations via $v_{char} = \sqrt{2|E|/M_{total}}$.[1]

The resulting scalar ratio $L_{norm} = L / L_{max}$ serves as a dominant heuristic determining curriculum staging, with high ratios mapping to initial stability phases.[1] However, Finding M6 within the technical documentation uncovers a critical numerical vulnerability in this sequence.[1] Due to floating-point truncation variances and minor precision overlaps during spatial scaling, the raw computation occasionally generates $L_{norm}$ configurations mathematically exceeding $1.0$.[1] If unchecked, executing the subsequent $2x-1$ mapping transformation upon a value exceeding unity pushes the resultant continuous variable out of bounds, destabilizing the initial condition vector structure.[1]

To rectify this data-side failure mode, an explicit algorithmic intervention is necessitated.[1] A hard threshold bounding protocol utilizing `np.clip(L_norm, 0, 1)` must be inserted into the processing chain directly following the ratio calculation, truncating errant boundaries before downstream vectorization algorithms ingest the values.[1]

### Lyapunov Time Divergence and State Vector Exclusion

To formally quantify the boundary separating predictable celestial motion from pure deterministic chaos, the framework calculates the Lyapunov Time ($\tau_L$).[1] This metric identifies the precise temporal horizon at which exponentially compounding chaotic interactions render continuous predictions fundamentally invalid.[1]

The evaluation array applies the classical Benettin numerical estimation approach to establish the maximal Lyapunov exponent ($\lambda$) across the trajectory space.[1] Initiating from the base state configuration $y_0$, a microscopic mathematical perturbation is introduced to generate a parallel phantom trajectory $y_0^{pert} = y_0 + \delta_0$, constrained strictly by an initialization magnitude of $\epsilon_{pert} = 10^{-8}$.[1] Both celestial configurations undergo synchronized forward integration across discrete intervals $\Delta t$.[1] Following evaluation, the continuous separation array $\delta_1 = y_1^{pert} - y_1$ is measured to extract a localized growth differential scalar $a_1 = \|\delta_1\| / \epsilon_{pert}$.[1]

Crucially, to prevent exponential overflow during integration, the phantom trajectory undergoes continuous structural renormalization mapping it backward to the perturbation limit while preserving its instantaneous directional gradient: $y_1^{pert} = y_1 + \epsilon_{pert} \cdot (\delta_1 / \|\delta_1\|)$.[1] Averaged continuously across a maximum temporal horizon, the exponent defines predictability: $\lambda \approx (1/T_{horizon}) \sum \ln(a_i)$, leading directly to the temporal metric $\tau_L = 1/\lambda$.[1]

Finding M7 exposes a structural ambiguity concerning the deployment of $\tau_L$.[1] The baseline specifications thoroughly document the calculation of $\tau_L$, yet paradoxically exclude the derived scalar from the final 13-dimensional initial condition state block.[1] The adjudication definitively resolves this finding: the omission is mathematically correct and must remain a fixed characteristic of the framework.[1] The Lyapunov timeframe is inherently a continuous dynamic outcome describing system evolution along a trajectory map; it is not an initial physical invariant inherent to the starting coordinates themselves.[1] Consequently, injecting $\tau_L$ into the $IC_{13}$ parameter space violates state-space definitions.[1] It must function exclusively as an external sorting heuristic utilized solely for mapping trajectories into appropriate chaotic curriculum stages.[1]

## Multi-Fidelity Dataset Architecture and Integration Parameters

The underlying trajectory database fueling the neural model represents a vast amalgamation of distinct celestial domains integrated using advanced N-body methodologies.[1] The structural complexity of chaotic interaction mandates a rigorous separation of input fidelity, balancing raw computational integration time against the necessity for hyper-dense temporal resolution during near-miss singularities.[1] The complete dataset represents a union of 15,028 individually verified physical combinations parsed directly from high-precision Brutus solver outputs.[1]

The trajectories are broadly classified across two dominant spatial paradigms [1]:

1. **High-Fidelity Hierarchical Domains:** These subsets represent mathematically stable celestial configurations, predominantly defined by tightly bound binary stars orbiting in resonance with a third, vastly distant companion body.[1] Their inherent stability permits extremely tight integration tolerances to capture long-term periodic smoothness.[1]
2. **Low-Fidelity Quasi-Random Domains:** Synthesized extensively via advanced Sobol quasi-random sequence sampling, this division forces bodies into chaotic, overlapping interaction geometries.[1] These sequences deliberately explore the unstable manifold space to map scattering dynamics and orbital breakdown.[1]

| Dataset Designation | Spatial Configuration Mode | File Count | Integrator Precision Tolerance | Word Length Parameter | Baseline Snapshot Frequency ($dt$) | Temporal Density Scaling |
|---|---|---|---|---|---|---|
| **Set 1a (Original)** | Hierarchical Structure | 4,857 | $1\text{e-}15$ | 130-bit | 0.08 | 1x Baseline Rate |
| **Set 1b (Original)** | Standard Quasi-Random | 4,857 | $1\text{e-}13$ | 118-bit | 0.17 | 1x Baseline Rate |
| **Set 2a (Resolution Upgrade)** | Hierarchical Structure | 2,749 | $1\text{e-}13$ | 130-bit | 0.01 | 8x Extreme Density |
| **Set 2b (Resolution Upgrade)** | Standard Quasi-Random | 2,565 | $1\text{e-}13$ | 130-bit | 0.01 | 17x Extreme Density |

The integration and verification pathways are mathematically constrained by SCOPE-12 Locked Contracts (Items 7).[1] These data-side pipeline limits govern precisely how trajectories bypass corruption logic.[1] Every validated phase utilizes explicit trajectory-admission gates mapped against robust blacklist-exclusion matrix filters to isolate systems manifesting immediate unrecoverable collapse outside the temporal bounds.[1] The validated trajectories then progress directly into the curriculum mapping schema.

## Curricular Stage Stratification and Evolutionary Progression

The foundational premise governing Curriculum-Transfer Learning (CTL) within PINNs states that neural models cannot adequately learn chaotic temporal boundaries without first internalizing foundational periodic truths.[1] The loss gradients originating from extreme close encounters generate chaotic gradient spikes that immediately corrupt early-stage generalized weight convergence.[1] Therefore, the framework dictates a rigorous seven-stage progression algorithm, evolving smoothly from highly predictable Keplerian mechanics toward entirely unbound scattering singularities.[1]

Because quasi-random Sobol sampling fundamentally strips away reliable preservation of the Virial ratio during initialization, an integrated stratification mechanism relying on dynamic bounds controls stage transitioning.[1] These parameters filter trajectories utilizing mechanical energy ($E$), angular momentum stability ($L/L_{max}$), Virial equilibrium defining gravitational collapse versus expansion ($Q = 2T / |V|$), and raw baseline body proximity ($s_{min}$).[1]

| Stage Identification | Fundamental Characterization | Staging Criteria Boundaries | Analytical Purpose within Architecture |
|---|---|---|---|
| **Stage 0** | Highest Stability | $E < -0.5$; $L/L_{max} > 0.5$; $0.7 \le Q \le 1.3$; $s_{min} > 2$ | Imprints baseline smooth-trajectory orbital mechanics. Filters solely tightly bound, wide-separated binaries in virial equilibrium.[1] |
| **Stage 1a** | Energy Relaxation | $-0.5 \le E < -0.1$; $L/L_{max} > 0.5$; $0.7 \le Q \le 1.3$; $s_{min} > 2$ | Introduces moderate gravitational well relaxation without sacrificing angular stability.[1] |
| **Stage 1b** | Angular Momentum Relaxation | $E < -0.5$; $0.1 \le L/L_{max} < 0.5$; $0.7 \le Q \le 1.3$; $s_{min} > 2$ | Plunges systems into severe eccentric modes while maintaining deep total binding energy.[1] |
| **Stage 2** | Temporal Refinement | Union matrix mapping Stage 0 + Stage 1 criteria constraints.[1] | Injects Set 2a ultra-high resolution temporal data to strictly evaluate temporal precision decoupled from novel topological chaos.[1] |
| **Stage 3** | Moderate Low-Fidelity Chaos | $E \le E^{LF}_{25\%}$; $L/L_{max} \ge L^{LF}_{75\%}$; $0.9 \le Q \le 1.1$ | Introduces quasi-random variables while protecting against severe divergence through strictly mapped percentage boundaries.[1] |
| **Stage 4a** | Chaos (Extended Horizon) | Predictability bound defined strictly by $\tau_L > 5$ code units. | Introduces fundamental chaotic drift possessing extensive predictable pathways before divergence.[1] |
| **Stage 4b** | Chaos (Terminal Horizon) | Highly restricted predictability matrix where $2 < \tau_L \le 5$ limits.[1] | Forces model to operate inside highly volatile regimes where deterministic divergence accelerates massively.[1] |
| **Stage 5** | Chaotic Temporal Refinement | Identical constraint matrix to combined Stage 4 boundaries.[1] | Pushes extreme snapshot-density Set 2b files through the system, testing resolution across chaotic fields.[1] |
| **Stage 6** | Extreme Collision / Scattering | $s_{min} < 0.5$ **OR** absolute energy limits measuring $\vert E\vert$ | |

### Empirical Validation Status of Demographic Trajectory Totals

A substantial documentation divergence exists regarding the empirical validation of the stage populations mapping across the stratification sequence.[1] The issue documentation asserts definitively modeled populations, notably dictating $\sim$1,200 trajectories assigned to Stage 0, scaling sequentially up through $\sim$1,600 trajectories terminating in Stage 4.[1] However, interrogation against the verification repository exposes all trajectory count approximations logged as CLM-02 through CLM-07 strictly as `claimed-unverified` parameters.[1]

These configurations represent speculative output boundaries designed by automated, uncalibrated stage-assignment systems that have not passed Phase-1 empirical verification thresholds.[1] Consequently, they remain entirely restricted by Future Empirical Check (FUT) gates and cannot function as foundational parameters determining maximum epoch allocations or mathematical loss plateau baselines.[1]

Equally critical, the generalized snapshot-per-trajectory estimations utilized in prior framework diagnostics (CLM-13: claiming $\sim$59 snapshots standard, $\sim$125 hierarchical, and $\sim$1000 gold) are explicitly overridden.[1] Computations must rely exclusively on the formally locked DATA-06 medians (CLM-16), validating the physical matrix boundaries at precisely **61 median standard outputs, 127 median hierarchical bounds, and exactly 1003 median high-density gold temporal snapshots**.[1]

### Unattainable Stage Transition Mechanics and Gating Triggers

Navigating across the predefined structural stages relies upon mathematical gating mechanics designed to evaluate network capability prior to escalating dynamical complexity.[1] Finding D5 outlines a debilitating theoretical failure originating from rigidly deterministic stage transition criteria.[1] The preceding specification dictated that the continuous neural architecture could only advance into a subsequent stage given an unbroken string of monotonically decreasing validation loss markers.[1]

Due to the stochastic nature of dense neural optimizations mapped across chaotic arrays experiencing constant micro-variations, enforcing strict monotonic loss reductions causes rapid evaluation stagnation.[1] In practice, models hit microscopic validation variance plateaus causing perpetual gating lockouts regardless of underlying generalizable convergence.[1] The adjudication dictates the implementation of dual-path progression matrices applied immediately from Stage 0.[1] A strict evaluation channel maintains primary validation authority based on complex mathematical tolerances. Simultaneously, a dynamic fallback architecture enforces transition escalations initiated via maximum computational epoch cutoffs or statistical stagnation quotas, alongside immediate mathematical rollback configurations if $NaN$ divergences are detected.[1]

## Tensor Batch Formulation and Dataloader Rectification

The optimization logic governing the ingestion of multi-fidelity datasets suffered massive procedural breakdown due to conflated dataloader designs. Two "BLOCKING" failures (B-07 and B-08) were definitively located within the core batch mechanisms.[1]

### The Replay Buffer Collapse and Lookahead Correction (B-07)

The core tenet of stable continuous learning mechanisms involves protecting foundational insights against catastrophic interference when processing novel chaotic inputs.[1] Finding B-07 exposes an operational reality where the underlying training loop bypassed completely the structured replay mechanisms detailed within the CTL manuals.[1] Instead, the dataloader executed a statistically flat, non-discriminatory fetch, populating batches using 256 random trajectories untethered to stage identity.[1]

A random batch matrix introduces dual catastrophic failure modes.[1] Firstly, the complete elimination of historical replay mechanics generates catastrophic forgetting; the network dynamically overwrites fundamental smooth-trajectory Keplerian physics parameters when abruptly swamped by chaotic scattering gradients.[1] Secondly, the lack of sequential lookahead exposure triggers violent and unpredictable loss explosions whenever arbitrary stage thresholds advance sequentially.[1]

The architectural fix mandates deploying a dual-phase tensor sampler.[1] The overall array structure must extract exactly 240 structured replay trajectories mathematically sourced from the total repository of current and completed historical archives (Stages $\le k$, mapped as $D_{\le k}$).[1] Furthermore, it necessitates the simultaneous extraction of 16 structured lookahead trajectories derived strictly from the immediate progressive threshold bounds (Stage $k+1$, mapped as $D_{k+1}$).[1] Each sampled path projects exactly 32 discrete internal time points, rigorously distributed through a 50/50 dual-matrix logic: half mapped across a perfectly uniform temporal spread bridging $[t_{min}, t_{max}]$, the other half dynamically distributed via acceleration-weighted parameters optimizing coordinate extraction near high-curvature periapsis zones.[1] (Parameters mapped under claimed-unverified classification CLM-12).[1]

### Isolation of Data-Fidelity and Collocation Matrices (B-08)

Finding B-08 uncovers an equally devastating dataloader collapse where physical reality constraints were fundamentally blended with mathematical interpolation constraints.[1] PINNs rely heavily on separate error topographies: data-fidelity vectors measure network accuracy mapped directly against discrete empirical simulation snapshots generated via the Brutus solver, while continuous collocation vectors track global compliance to overarching physical residual loss invariants extracted universally across the continuous coordinate plane.[1]

The prior iteration erroneously collapsed both requirements, evaluating them atop identical discrete trajectory points.[1] Such logic defeats continuous physics representations by tying differential solvers artificially to predefined output cadences.[1] To guarantee mathematically valid partial differential equation scaling, absolute detachment is required.[1]

| Point Generation Array | Discrete Temporal Volume | Extraction Methodology | Mathematical Validation Metric |
|---|---|---|---|
| **Data-Fidelity Architecture** | 8,192 Points per batch | Anchored rigorously to exact simulation time steps.[1] | Calculated via strict mathematical $L_1$ norm comparisons.[1] |
| **Global Collocation System** | 4,096 Points per batch | Floated dynamically across arbitrary temporal continuous domain mappings spanning $[t_{min}, t_{max}]$.[1] | Evaluated exclusively through physics constraint residuals and Hamiltonian energy conservation penalties.[1] |

Both disjointed arrays enforce identical 50/50 uniform and acceleration-weighted temporal distribution algorithms to ensure chaotic geometries are comprehensively enveloped.[1]

### Collocation Normalization Across Divergent Densities (M16)

Executing standardized global collocation parameters across datasets bearing vast variations in snapshot output densities introduces systemic bias into optimization gradients.[1] Finding M16 isolates a massive temporal imbalance wherein snapshot intervals mapping baseline hierarchical outputs ($dt \approx 0.08$) or quasi-random streams ($dt \approx 0.17$) exist alongside the radically dense gold standards ($dt = 0.01$) defining up to a 17-fold frequency disparity.[1]

Deploying static temporal point boundaries forces chaotic lower-resolution paths to bear massively inflated statistical relevance relative to their intrinsic spatial content, skewing physical residuals.[1] The mathematical resolution (mapped unverified under CLM-20 parameters) forces dynamic proportional constraints tracking temporal output scaling vectors.[1]

The calculation dictates evaluating density configurations relative to the benchmark $dt_{base} = 0.01$ output state via the formulated multiplier $n_{col} = base \cdot (dt_{base} / dt_{out})$.[1] Concurrently, this scales the standard baseline integrations to heavily diminished mathematical frequencies approximating $0.059$x normal volume, limits hierarchical domains to $\approx 0.125$x rates, and perfectly preserves gold pathways operating at $1.0$x saturation limits, neutralizing architectural imbalance entirely.[1]

## Structural Adjudications Governing Causal Regularization and Geometric Tolerances

The most complex challenges remaining for the framework require the definitive selection between competing conceptual paradigms regarding temporal causality enforcement and singularity geometric modeling.[1] These decisions remain officially unresolved pending framework-owner approval; the parameters, conflicts, and options are formally outlined to facilitate finalization.[1]

### The Causal-Training-Mode Discrepancy (D-04)

Modeling deeply chaotic trajectories utilizing physics-informed mechanisms routinely encounters catastrophic optimization failures stemming from temporal causality violations. If early portions of a celestial trajectory display minute positional deviations, the mathematically correct continuation along the phase space drives the simulation exponentially away from the expected future state. Standard neural networks inherently ignore causality, simultaneously penalizing minor late-stage deviances identically to early-stage structural errors, essentially pulling the coordinates toward physically impossible average pathways rather than true chaotic evolutions.[1]

Addressing this failure defines the single most consequential training-loop paradigm.[1] However, severe document contradictions obscure the official configuration.[1] The issue document claims that a methodology employing Global Sampling mapped to an Augmented Lagrangian Method (ALM) represents the current Source of Truth (SOT).[1] It cites sections outlining single forward passes mapped to total constraint-violation fields.[1]

Contradicting this directly, the unyielding authoritative framework specification (`ctl_instruction.md`) operates utilizing robust causal weighting matrices.[1] Operating as the PHYS-05 default mechanism, the formulation scales gradients explicitly via sequential loss progression arrays parameterized as $w_n = \exp(-\eta_c \cdot \sum_{m<n} \text{stopgrad}(\bar{R}_m))$ relying on exponent limits defining $\eta_c = 1$.[1] The mathematical specifications purposefully eliminate pseudo-ALM frameworks combining data loss, generic unscaled residual scalars, and unified energy vectors, retaining the ALM mechanism exclusively within specialized scalar Phase 2 ablations.[1] The overarching decision provides three distinct paradigms.

| Operational Design | Methodology | Optimization Dynamics and Risk Vectors |
|---|---|---|
| **Option A (Per-Time-Step Causal Weighting)** | Forces temporal sequences dictating $w_i \propto \exp(-\lambda \sum_{j<i} L_j)$ constraints.[1] | Maintains highly robust structural reality enforcing physical "arrows of time".[1] Vulnerable to "Causal Firewall" breakdowns where singular chaotic spikes occurring prematurely permanently collapse subsequent optimization gradients to zero.[1] |
| **Option B (Global Sampling / Dense ALM Array)** | Evaluates the complete time spectrum over continuous integration regions mapping $[t_{min}, t_{max}]$ simultaneously.[1] | Eliminates early gradient crashes allowing total topological evaluation across complex fields.[1] Highly susceptible to gross causality violations wherein volatile late-stage chaotic boundaries negatively corrupt smooth early-stage kinematic convergences.[1] |
| **Option C (Time-Windowed Causal-ALM Hybrid)** | Deploys advanced interlocking matrices partitioning continuous mapping limits into rigid overlapping sequence domains utilizing extreme local hard-gating.[1] | Provides optimal mathematical stabilization circumventing firewall events while preserving arrow metrics natively.[1] Implementation requires near-total reconstruction impacting Phase 2 dataloaders and stage gating systems.[1] |

### Geometric Coordinate Definitions for Collision Gating ($s_{min}$) (D-05)

Determining proximity bounds in gravitational structures necessitates extreme precision, particularly transitioning between macro-scale orbital measurements and microscopic numerical singular thresholds.[1] Minimum coordinate separation thresholds map to the scalar metric $s_{min}$ natively measuring initial interaction dimensions between bounded entities.[1]

Stage 6 configurations are governed purely by geometric proximity triggers established around measurements satisfying $s_{min} < 0.5$ boundaries to invoke severe scatter evaluations.[1] Standard implementation manuals invoke pure theoretical mathematical ranges mapping distances organically utilizing completely unsoftened metric variables for validation.[1] Contrastingly, the internal training loop specifications necessitate utilizing robust numerical dampening arrays enforcing constraints approximating $\epsilon_{soft} = 10^{-5}$ boundaries to eliminate unbounded division limits arising during coordinate intersection gradients.[1]

The pending framework-owner decision balances dual-resolution mechanisms [1]:

- **Option A:** Ensures strict adherence to source limits by running unsoftened pure measurements to govern macroscopic dataset transition gating logic to preserve initial ground truth, while isolating numerical limits measuring $\max(s_{min}, \text{eps\_soft} = 1\text{e-}5)$ universally mapping within discrete dynamic gradient networks to govern division safety loops.[1] Unsoftened coordinates are output securely into external analytical archives continuously.[1]
- **Option B:** Establishes mathematical unity forcing the $\max(s_{min}, \epsilon)$ transformation identically upon both data sorting protocols and neural network loss topographies equally.[1]

### The Epsilon Parameter Domain Discrepancy (D-06)

Compounding proximity logic disputes, the operational models currently harbor fatal order-of-magnitude divergences regarding applied softening parameter constants.[1] Computations governing underlying static potential energy derivations operate relying upon bounds restricted to exactly $\epsilon = 10^{-10}$.[1] However, the framework manuals highlight aggressively that such diminutive variables map identically to zero bounds inside baseline 32-bit GPU floating-point architecture fields, offering literally zero mathematical safety buffers.[1] Consequently, parallel internal limits restrict standard bounds to robust $\epsilon_{soft} = 10^{-5}$.[1]

Adjudication inherently forces alignment with SCOPE-12 Locked Item 4 metrics fixing loss-side physics-residual evaluations statically to $\epsilon_{train} = 1e-5$ incorporating standard matched-Plummer mathematical topology structured as $r_{safe} = \sqrt{\|\Delta r'\|^2 + \epsilon_{train}^2}$ while aggressively prohibiting generic linear additives.[1] The sole unresolved dynamic centers completely around how strictly static contexts integrate alongside the locked limit array.[1]

- **Option A:** Adopts universal $1e-5$ deployment models modifying pure static derivations entirely.
- **Option B:** Maintains a precise dual-context framework scaling static bounds parsed within complex 64-bit CPU configurations to exact $1e-10$ models while delegating all dynamic gradient operations inside GPU limits strictly to the protected $1e-5$ bounds.[1]
- **Option C:** Reverts models aggressively pushing generic $1e-10$ mappings over the full mathematical domain, openly discounting explicit documentation logic outlining severe convergence instability risks.[1]

## Continuous Physics Loss Regularizations and Gradient Telemetry

Ensuring accurate neural optimization inside chaotic domains relies upon sophisticated loss boundary scheduling matrices capable of limiting erratic spatial errors and suppressing catastrophic residual energy explosions natively.

### Energy Conservation Matrix Mitigation ($\lambda_E$) (M15)

The theoretical framework measures trajectory validity heavily based on absolute adherence to static Hamiltonian mechanical boundaries, particularly calculating mechanical binding loss over phase transitions.[1] The applied energy conservation limit ($\lambda_E$) serves to forcefully suppress predictions drifting structurally away from realistic limits.[1] Finding M15 identifies severe catastrophic failure configurations wherein standard late-stage parameters applying weights escalating upward toward limits approximating 1000 generate unmanageable optimization errors.[1] By scaling limits artificially high relative to native physical variances, the energy term swamps core coordinate positioning boundaries by factors expanding geometrically between 100x and 5000x margins.[1]

The solution requires mandatory hard-clamping models restricting variables via $\lambda_E(k) = \min(10^{k-3}, \text{cap}[k])$ distributions tracking progressively through sequence models mapping linearly across bounds starting at nominal 1 values up through hard terminal limits approximating 500.[1] (Metrics mapped unverified into CLM-11 parameters).[1] An active secondary heuristic requires runtime evaluation boundaries forcing real-time weight scaling compression whenever computed combinations violate basic scaling constraints defined via $(\lambda_E \cdot L_{energy}) > 10 \cdot L_{data}$ thresholds to prevent terminal run failures.[1]

### Continuous Adaptive Clipping Metrics (M14)

Optimization limits face conflicting array boundary definitions inside standard mathematical specifications.[1] Base PINN topologies define models capturing gradient normalizations utilizing strictly dynamic median historical rolling windows mapped inherently over discrete intervals.[1] Alternately, stage configuration models outline discrete static numerical step boundaries defining parameter array steps utilizing simple scalar integers.[1]

Finding M14 definitively forces unification combining both architectures continuously.[1] Parameters merge dynamically producing exact clipping targets evaluating constraints via $\text{clip\_value} = C_{stage} \cdot \text{median}(\text{grad\_norm\_history})$ boundaries.[1] The stage-aware parameter ($C_{stage}$ derived from `claimed-unverified` CLM-10 arrays) controls structural limits while native rolling windows govern immediate spatial tracking dynamics continuously.[1]

### ALM Variance Boundary Clamp Protocol

Integrating Augmented Lagrangian methodologies inside scalar Phase 2 bounds creates secondary optimization risks connected tightly to unbound structural variable drift tracking.[1] Specifically, formulas driving updating metrics for the parameter bounds defining moving-average limits managing $\mu_p$ scalar adjustments entirely lack limiting mathematical ceilings inherently.[1] Devoid of operational boundaries, volatile training runs precipitate immediate divergence pulling scalars asymptotically toward infinite bounds, breaking optimization loop geometries entirely.[1] To resolve structural deficiencies entirely, numerical clipping matrices utilizing standard mathematical array commands strictly evaluating limits constrained via `np.clip(mu_p, 1e-4, 100.0)` must insert fully inside operational update blocks natively.[1]

### Analytical Automatic Differentiation (AD) Fidelity and Topologies

Two critical optimization array components require fundamental architectural fixes concerning gradient tracking pathways.[1]

- **Component-Wise Kinematics (NS-12):** Initial theoretical outlines dictate velocity and acceleration tensor evaluations map cleanly utilizing strict PyTorch Automatic Differentiation matrices applied securely.[1] Live implementation parameters frequently circumvent strict chain-rule tracking formulas incorrectly utilizing total 9D state tensor summation properties representing generalized acceleration variables.[1] Finding NS-12 explicitly prohibits aggregated mapping derivatives.[1] Structural accuracy completely relies mapping pure discrete component-wise limits mapping temporal continuous fields mathematically onto corresponding unique geometric points strictly conforming identically against discrete continuous laws.[1]
- **Huber Parameter Calibration Dynamics (NS-13):** Evaluating relative performance boundaries applying energy differential scaling uses classical Huber models configured typically mapping values around generic $\delta = 1.0$ parameters.[1] Operating securely against fundamentally normalized input limits, broad limits entirely nullify Huber bounds reducing metrics functionally back mapping onto simplistic unbound $L_2$ properties failing entirely providing large-scale anomaly tracking.[1] Redefining bounds mandates initializing metrics securely across extremely tight $0.01$ parameters dynamically parsing measured quantile deviations directly extracted checking empirical bounds derived against absolute $|\Delta H|$ matrices mapped independently against specific curriculum sequences universally.[1]

## Evidentiary Boundaries and Tracked System Omissions

In strict adherence to the epistemological framework defined within the task adjudication sequence, analyzing theoretical constructs requires tracking transparent records detailing explicitly where fundamental material specifications suffer catastrophic missing boundary data configurations.[1]

Evaluations strictly bound against `doc-03` payload parameters expose massive source omissions invalidating deep parameter configurations.[1]

1. **Architecture Specifications:** Detailed continuous layer parameters, layer depth metrics, internal node frequency mapping, baseline loss limits defining topological initialization configurations referenced heavily relying upon standard target document matrices mapped globally as `pinn_architecture.md` (SHA-256 identifying `318f297a...`) exist entirely absent pulling through provided payload variables.[1]
2. **Sampling Framework Parameters:** Explicit programmatic boundary metrics defining pure theoretical Sobol generation patterns mapped against complex dataset integration mapping requirements existing naturally inside native `sampling_method.md` files structurally remain omitted from provided payloads.[1]
3. **Detailed Transition Modifications:** Deep metric evaluations detailing explicit transition alternative logic variables mapping natively inside `stage_strat_revision.md` specifications exist definitively outside the operational domain parsed through transport sequences.[1]
4. **Incomplete Interrogation Parameters:** Provided sequences determining core open research boundaries defining required decision thresholds display critical terminal truncation limits severing `framed-research-questions.md` text boundaries directly following causal limit mappings causing total analytical blackout measuring detailed option tracking regarding epsilon definitions independently.[1]

Any specific structural resolutions requested targeting these restricted bounds return formal "Insufficient Evidence" classifications registering directly mapping claims tracking limits effectively removing synthetic theoretical parameter generation variables universally.[1]

## Comprehensive Synthesis and Resolution Matrix

The adjudication of the multi-fidelity PINN framework targeting continuous complex three-body systems establishes a unified mathematical reality governed entirely underneath immutable fixed boundary constants restricting variables exactly against standard raw-mass non-dimensional mapping limits derived utilizing $D \approx 4.6416$ constraints while comprehensively overriding alternative total-mass theories structurally.[1]

Navigating dataset variables ranging structurally spanning deeply bound stable Keplerian dynamics advancing systematically toward unbounded hyper-dense terminal chaotic limits mapping 17-fold trajectory density variations relies comprehensively upon structural normalization bounds strictly utilizing derived empirical mapping constants fixing spatial matrices identically alongside $t' = 2(t/T) - 1$ mapping boundaries projecting temporal values into continuous variables efficiently.[1] Critical parameter logic fixes enforce absolute mathematical integrity isolating variables dynamically establishing clamping algorithms locking down derived angular limits neutralizing overflow arrays scaling above $1.0$ boundary limitations natively while aggressively excluding derived temporal matrices mapping Lyapunov parameters defining $\tau_L$ outside fixed $IC_{13}$ arrays universally.[1]

Optimization metrics advance structurally bypassing catastrophic replay collapse frameworks rebuilding dataloaders distributing purely defined 240+16 boundaries incorporating 50/50 temporal weighting formulas seamlessly isolating pure coordinate fidelity configurations capturing exactly 8192 parameters decoupled cleanly away targeting continuous collocation maps applying exactly 4096 separate nodes bounded strictly scaled proportionally correcting heavy matrix densities tracking explicit $n_{col} = base \cdot (dt_{base} / dt_{out})$ bounds cleanly maintaining accurate tensor normalization structures universally.[1]

Terminal framework finalization pathways require direct resolution determining final topology mapping configurations isolating critical conflict limits detailing ALM boundaries versus strictly mapped temporal causal weighting constraints definitively resolving conflicting parameter strategies spanning geometric unsoftened boundaries tracking exactly tracking analytical epsilon mapping variations restricting matrices accurately isolating operational boundaries safely inside formal double-precision configurations scaling matrices perfectly.[1]

## Works cited

1. 03-curriculum-and-training-loop.md

===== END ISSUE03-SECTION-f26fed61251ff665 REPORT R6 =====

===== BEGIN ISSUE03-SECTION-f26fed61251ff665 REPORT R7 (26170 bytes, sha256 bfecf583dffb) =====
I now have a thorough panel analysis. Below is my adjudication, written as evidence assessment and decision preparation.

# doc-03 Curriculum and Training Loop — Adjudication

## Method and posture

I adjudicate each framed question against the authoritative specs (`ctl_instruction.md`, `pinn_architecture.md`), under the locked SCOPE-12 constraints (items 1–7), treating the issue doc as non-authoritative. I separate **locked** from **revisable baseline**, **confirmed** from **gap**, and flag where the issue doc's premises are **stale/obsolete** relative to the current spec. Spec-edit directions are offered only as candidate resolutions with the owner decision identified — nothing here is an adopted change. Every figure is referenced by its CLM-NN status.

A recurring pattern, which should itself be recorded: the issue doc was largely written against an *earlier* spec revision. Several of its premises (the "global+ALM is current SOT" claim, the L1/MAE data loss, the `λ_E≈1000` energy weight, the dense-ALM `μ_p` machinery, the `L_norm`→IC-mapping framing) no longer match the current PHYS-05 / Phase-17–19 spec state. Distinguishing genuine open work from stale framing is the bulk of the task.

---

## Section 2 — Decisions requiring framework-owner approval

### The causal-training-mode decision

**Finding.** The issue doc's framing that "global sampling + ALM is the current SOT" is **factually wrong against the current spec** and should be corrected before being put to the owner. `ctl_instruction.md` ("Loss Function Formulation" / "Phase 2: Total Training Loss") and `pinn_architecture.md` §3.2/§4.1 (PHYS-05) **already** adopt causal weighting as the default — `w_n = exp(−η_c·Σ_{m<n} stopgrad(R̄_m))`, `w_1=1`, `η_c=1` — and **explicitly reject** the dense-residual pseudo-ALM `L_data + λ_p·L_phys + (μ_p/2)·L_phys² + λ_E·L_energy`. ALM survives only as a P2 ablation on *scalar* conservation constraints (`pinn_architecture.md §4.2`).

So the live options map onto the spec as: Option A (causal weighting) ≈ the **current baseline**; Option B (global + dense ALM) ≈ the **explicitly rejected** formulation; Option C (time-windowed causal-ALM hybrid) ≈ a large, un-specced rewrite. Notably, the spec's `stopgrad` in the causal weight is precisely the mechanism that mitigates the "causal firewall" risk attributed to Option A: gradients do not flow through the exponential weights, so an early stiffness spike depresses later weights without making the weight term adversarial.

**Conflict / uncertainty.** The issue doc's premise is stale. No empirical comparison of A vs B vs C is in the attached materials — the "causal firewall" and "temporal-causality violation" risks are asserted, not measured. v1.6 has no verification phase for them.

**Candidate resolution (owner decision).** *Target:* `ctl_instruction.md` loss formulation + `pinn_architecture.md §3.2/§4.1`. The honest finding is that **the A/B/C choice is largely already settled by the spec baseline (causal weighting; dense ALM rejected)**, not genuinely open. The owner's real decision is narrower: (i) confirm the causal-weighting baseline stands as written, and optionally (ii) decide whether `η_c` should become stage-dependent, and (iii) decide whether the Option-C windowed-hybrid is worth scoping as future work. I record this as evidence for the owner; I do not select among A/B/C. The issue doc's Section-2 causal framing should be annotated **obsolete — superseded by PHYS-05**.

### The s_min-frame decision

**Finding.** The spec is already internally consistent and dual-context: `ctl_instruction.md` Step 3 item 1 defines `s_min` from "true pairwise separations (no softening)" — an unsoftened geometric quantity used for stage gating; static invariants use Plummer `ε_inv=1e-10` (in `V` only); training losses use the locked `ε_train=1e-5` (PHYS-03). Option A (unsoftened gate + softened loss) matches this baseline; Option B (softened everywhere) contradicts it.

**Conflict to surface (important).** The issue doc's Option A references a *training-loss collision criterion* using `max(s_min, eps_soft)`. **No such term exists in the current spec.** Stage 6 (`s_min < 0.5 OR |E| < 0.01`) is a **curriculum gate**, not a loss component, and the locked PHYS-03 softening is the matched-Plummer `sqrt(‖Δr′‖²+ε²)` form — an *additive* `max(s_min, ε)` would itself be the prohibited PHYS-03 anti-pattern. So the issue doc is not "cleaning up" an existing criterion; it is implicitly proposing a *new* collision-loss term.

**Candidate resolution (owner decision).** *Target:* `ctl_instruction.md` Step 3 / Stage-6 gate. Recommended framing for the owner: **(a) confirm status quo** — unsoftened `s_min` for the gate, no training-loss collision term, always log the unsoftened value (this is what the spec already does); or **(b)** commission a genuinely new close-encounter loss term, which would have to be designed from scratch under PHYS-03 (matched-Plummer, `ε_train=1e-5`), with its own weight schedule and an explicit interaction analysis with the causal weighting. I do not pick; I flag that the issue doc conflates (a) and (b).

### The epsilon-strategy decision

**Finding.** The genuinely-open part is *only* whether a distinct static/invariant softening coexists with the locked loss-side `ε_train=1e-5`. The spec **already answers this as Option B (dual-context)**: `ctl_instruction.md` Step 3 item 1 states `ε_inv=1e-10` is "context-specific for offline invariant computation and is distinct from the training-time softening `ε_train=1e-5`," and `pinn_architecture.md §3.4` carries the dual-epsilon visibility note. Option A (collapse offline to `1e-5`) would coarsen offline invariants/stage assignment; Option C (unify at `1e-10`) is incompatible with the locked loss side (item 4) and is argued against on double-precision grounds.

**Candidate resolution (owner decision).** *Target:* `ctl_instruction.md` Step 3 / `pinn_architecture.md §3.4`. The baseline is already dual-context; the owner's decision reduces to **ratify the existing dual-context arrangement** (recommended posture, since the alternatives either contradict the lock or coarsen invariants) — annotate the issue doc's "five-order-of-magnitude contradiction / truncated justification" framing as resolved by the current spec text. Whether `ε_inv=1e-10` materially changes stage assignments vs `1e-5` is **unverified** in the attached materials; log that as a FUT empirical check if the owner wants to revisit.

---

## Section 3 — Confirmed findings

### B-07 — replay/lookahead batch construction
**Confirmed (already in spec); one pseudocode bug.** `ctl_instruction.md` "Mini-Batch Construction with Lookahead Sampling" already specifies `B_≤k=240`, `B_{k+1}=16` (batch 256), `n_pts(traj)=min(n_pts_cap=32, n_snapshots)`, and the 50/50 split (`k_w=floor(n_pts/2)` Gumbel-top-k acceleration-weighted + remainder uniform, without replacement, seeded). B-07 correctly flags the legacy flat `get_batch` in `pinn_architecture.md §3.1` as superseded. The reconciliation item: the audit §6 pseudocode draws a **fixed 32** via `np.random.choice(..., replace=False)`, which conflicts with locked M12 `min(32, n_snapshots)` and will error/under-sample on low-snapshot trajectories (verified base medians are 61/127/1003 per CLM-16 — but per-trajectory minima can fall below 32). Counts are claimed design constants (CLM-12), not verified facts. *Candidate edit:* correct the §6 pseudocode to `min(32, n_snapshots)`; no owner decision needed.

### B-08 — data-fidelity vs collocation separation
**Confirmed (already separated).** `pinn_architecture.md §3.1` (Huber data term on scaled positions, `N_data=256×32=8192`) and `§3.2` (collocation residual, `sample_collocation_points`, `n_col=4096`) are already two independent point sets with distinct sampling and loss roles. The issue doc's "conflation" claim is stale. CLM-12 counts are claimed-unverified. *Candidate edit:* state the two-independent-set discipline explicitly in the batch-constructor section to close the documentation gap; no design change.

### M6 — `L_norm` clamping
**Issue-doc framing obsolete.** Under the locked 14D `[τ, IC₁₃]` Jacobi-state contract, `L_norm` is **metadata** (staging/diagnostics/loss-scaling), not an IC slot (`ctl_instruction.md` Step 4). The "clip before `2x−1` IC mapping" rationale no longer applies. `compute_L_norm` returns `L/(L_max+eps)` and can exceed 1. The residual valid concern is narrow: stage-gating logic should not assume `L_norm∈[0,1]`. *Candidate edit (minor):* apply `clip(L_norm, 0, 1)` (or `min(·,1)`) for staging/diagnostic use only — never reintroduced into any network input. Owner decision is minor (clamp-for-staging vs guard the gate boundaries).

### M7 — `τ_L` excluded from IC vector
**Confirmed; matches spec.** `ctl_instruction.md` Step 4 excludes the invariant-heavy descriptors (including `τ_L`) from `IC₁₃`, and uses `(E, Q, s_min, L_norm, τ_L)` for default stage gating only — consistent with the locked 14D contract. No change beyond removing any lingering text implying `τ_L` is an input.

### M14 — gradient-clipping merge
**Reconcilable; issue-doc `8.5` is unjustified.** `pinn_architecture.md §4.4` gives `clip = 5.0 × median(last 100 norms)`; `ctl_instruction.md` "Adaptive Median-Based Gradient Clipping" gives the curriculum-aware `C` schedule (0–1: **7–10**; 2–3: **5**; 4–6: **3**). Crucially, the `§4.4` factor of `5.0` **is** the stages-2–3 value of the same schedule, so the two specs are not truly in conflict — `§4.4` is just the mid-curriculum instance presented as a standalone. The natural merge is `clip = C_stage · median(·)`, which is exactly what the issue doc proposes. The issue doc's `C_table` (CLM-10, claimed-unverified) sets stages 0–1 to `8.5`, an arbitrary midpoint of the spec's `[7,10]` **range** — not spec-endorsed. *Candidate edit:* update `§4.4` to reference the per-stage `C` schedule rather than a standalone `5.0`. **Owner decision:** choose a concrete value (or anneal rule) for stages 0–1 within `[7,10]`; `8.5` is one option but `10`/`7` are equally defensible.

### M15 — energy-loss weight schedule
**Severe conflict; issue-doc schedule is obsolete.** The spec PHYS-05 (`pinn_architecture.md §4.1`) sets `λ_E^max(k)=λ_L^max(k) = {0 for k∈{0,1}; 10^{k−4} for k∈{2,3,4}; 1 for k∈{5,6}}` with linear warmup `I_warm=min(2000, 0.1·N_Adam)` — i.e. the energy term is **off** at stages 0–1 and **capped at 1.0**. The issue doc's capped-hybrid `cap_table={0:1,1:5,2:20,3:50,4:100,5:200,6:500}` (CLM-11, claimed-unverified) is 10×–500× larger at every stage, and its premise (`λ_E=1000` overwhelming) comes from an even older schedule. Adopting it would massively over-weight energy conservation against data/physics. *Candidate resolution:* annotate M15/CLM-11 **obsolete — superseded by PHYS-05 §4.1**; the spec schedule stands. If a future ablation shows the `1.0` cap is too low at stages 5–6, a modest increase is a separate, evidence-gated proposal — not the `500` figure.

### M16 — `dt_out`-aware collocation scaling
**Insufficient evidence; spec correctly defers.** `ctl_instruction.md §2.6` exposes `n_snapshots`/`dt_out` as loader metadata but explicitly labels the M16 scaling rule a deferred forward-interface item ("not used here"); `pinn_architecture.md §3.2` uses a fixed `n_col=4096`. Per-variant `dt_out` is **verified** (CLM-17: std 0.17 / hier-base 0.08 / gold 0.01), but the scaling-factor rule itself is claimed-unverified (CLM-20). The direction is genuinely debatable:
- The audit-verbatim `n_col ∝ dt_base/dt_out` gives high-resolution gold trajectories **more** collocation and low-resolution standard trajectories **fewer** (≈0.059×) — a "match collocation to data density" logic, but arguably a perverse incentive (the sparsest trajectories, which most need physics-informed interpolation between snapshots, get the least enforcement).
- The inverse `dt_out/dt_base` is the "compensate sparse coverage" logic.
- A deeper point: collocation residuals are evaluated at points sampled from the **continuous** `[0,T]` domain (`§3.2`), not at snapshot times, so coupling `n_col` to `dt_out` at all is not strongly physically motivated — difficulty (close encounters) is the better driver.

*Candidate resolution:* **log a gap** against CLM-20. Recommended owner posture is to keep the deferral (fixed `n_col`) until an ablation studies collocation-density × resolution. Do not adopt either direction provisionally; "insufficient evidence" is the honest finding.

### D5 — stage-transition criteria / dual-path fallback
**Genuine gap + a substantive relaxation that needs justification.** `ctl_instruction.md` "Stage Transition Criteria" encodes four strict criteria (plateau `ε_plateau=1e-5`, patience 200; **validation stability `≤ min`** (monotonic); physics `ε_phys=1e-4`; energy drift `ε_energy=1e-4` with the locked `ε_H=1e-4·S_H` floor) and carries the author's own note questioning their attainability with limited data. It does **not** encode the fallback path or per-stage threshold table the issue doc proposes. The issue doc's fallback (max-epochs `{0:500…6:1200}` CLM-09, stagnation, NaN rollback), per-stage `ε_phys/ε_energy` table (`5e-3…1e-4` CLM-08, "not fixed"), and Stage-0 pilot are claimed-unverified design hypotheses. The most consequential single change is relaxing criterion 2 from `≤ min` to `percentile_10` — that shifts the gate from "never regress" to "mostly don't regress," and for chaotic systems where validation loss is inherently noisy (Lyapunov divergence makes long-horizon val loss non-monotonic), the author's attainability worry is well-founded.

*Candidate resolution (owner decision).* *Target:* `ctl_instruction.md` Stage Transition Criteria. Three graduated options for the owner: (a) keep strict-only, add a max-epochs safety cap + NaN rollback only (minimal, preserves strictness); (b) full issue-doc dual-path with `percentile_10` + per-stage tables (CLM-08/09 — but these are unverified and should be calibrated by the Stage-0 pilot before adoption); (c) intermediate. The materials contain **no empirical data on attainability**, so the per-stage thresholds and max-epochs values should be treated as hypotheses to validate via the Stage-0 pilot, not constants to lock. I do not select; I flag the `≤min`→`percentile_10` change as the load-bearing decision.

### NS-12 — componentwise AD
**Confirmed; fully satisfied.** `pinn_architecture.md §5.3.1` (PHYS-02) is the canonical componentwise normalized-time AD contract: it requires all nine `dr'_{i,α}/du`, **forbids** the `torch.autograd.grad(r.sum(), u, …)` summed-output anti-pattern that NS-12 warns against, lists acceptable patterns (`jacrev`+`vmap`, per-component loop, full-Jacobian), and gives a worked synthetic-trajectory derivative test. No gap; no change needed.

### NS-13 — Huber energy δ
**Valid concern; empirical/FUT.** `pinn_architecture.md §3.4` fixes the energy Huber transition at `δ=1.0`, applied to the *relative* drift `ΔH_n = (H_ε − H_ε(r_0))/(|H_ε(r_0)|+ε_H)`. Because this residual is normalized (and `|H_ε(r_0)|` is O(1) for bound systems), `|ΔH|` is plausibly O(1e-4…1e-2), so `δ=1.0` places essentially all samples in the quadratic branch — the Huber loss degenerates to L2 and its outlier robustness is lost. This matches the issue doc's NS-13 critique and is corroborated by PINN literature noting δ=1 Huber ≈ MSE. However, the *actual* `|ΔH|` distribution is **not in the attached materials**. *Candidate resolution:* **log a gap** — measure normalized `|ΔH|` per stage in the Stage-0 pilot, then set `δ` near a high quantile (issue-doc range 0.01–0.1 is a reasonable starting hypothesis), possibly stage-dependent. Do not change `δ` speculatively; flag as a known limitation. Owner decision: whether `δ` becomes a tuned/stage-dependent parameter.

### NS-18 — loss-component scaling contract
**Issue-doc L1/MAE premise is stale.** The spec's units/scaling contract is already coherent: `§3.1` data term is **Huber** (`δ_r=1`) on scaled positions `r'=r/D` with the locked `D≈4.6416` (CLM-19); `§3.2` physics residual with `ε_train=1e-5` and causal weighting; `§3.4` energy regularizer with the same `ε_train=1e-5`; `§4.1` composes them. The issue doc's "L_data uses L1/MAE" is the obsolete pre-Huber prose. *Candidate edit:* update the issue-doc/loss-table references from L1/MAE to the Huber `δ_r=1` data contract; confirm all terms operate in dimensionless `G=1` units under locked `D` and `ε_train`. Worth noting as a secondary item: the same `δ=1.0` question applies to the *data* Huber, but here residuals are in scaled-position units (O(0.1–1)), so `δ_r=1` is plausibly more appropriate than the energy case — a diagnostic check, not a clear defect. The double-default `δ=1.0` across data and energy should be audited jointly rather than treated as two unrelated tuning knobs.

---

## Section 6 — Data-driven adaptive stage assignment

**Major divergence; reconcile under locked PIPE contracts; do not adopt runtime clustering.** The spec baseline (`ctl_instruction.md` Step 5 + "Multi-Stage Data Stratification") is **threshold-based**, keyed by `record_key` over the admitted set, with hierarchical in stages **0–2** and quasi-random in **3–6**. The spec author's own note explicitly *invites* a data-driven scan because the virial ratio is not preserved under quasi-random Sobol sampling (`Q ∝ s³` distortion — confirmed in `sampling_method.md`, which documents `scale_range=[0.8,1.2]` enabled at coordinate `u₄`). So the *motivation* for the adaptive approach is grounded. But `stage_strat_revision.md` diverges from the spec in two concrete ways the owner must resolve:

1. **Stage mapping conflict.** `stage_strat_revision.md` puts hierarchical in **0–1** and quasi-random in **2–6** (via PCA+K-means clusters sorted by median `τ_L`); the spec puts hierarchical in **0–2**. These cannot be silently merged.
2. **Method conflict + a PIPE-contract failure mode.** K-means with `k=6` yields only six clusters, which cannot directly populate the **seven**-stage (0–6) curriculum label space without splitting a cluster or defining an extra stage. Runtime clustering also threatens the locked deterministic stage-query contracts (`sample_replay(n, max_stage)`, `sample_lookahead(n, stage)`, `has_stage(k)`, PIPE-01..10), which require stable, materialized integer stage labels per `record_key`.

Per-stage counts (CLM-02..07) are **claimed-unverified** design outputs and must not be treated as facts; the `~2,565` gold count that appears alongside them is the verified figure (CLM-15), not a stage count. `stage_strat_revision.md` also carries an internal `I3` schema inconsistency (noted in its own source-issues block, SI-SSR-001), reducing confidence in its DataFrame schema.

*Candidate resolution (owner decision).* *Target:* `ctl_instruction.md` Step 5. The reconciliation that respects the locked PIPE contracts is a **hybrid**: use EDA/PCA/clustering *offline, for boundary discovery only* (with a fixed seed, versioned feature normalization, and the `>10%`-per-stage / merge-underpopulated safeguard), then **encode the discovered boundaries as fixed thresholds** that produce a stable seven-stage labeling per `record_key`. Do **not** run K-means at training time. The hierarchical 0–2 vs 0–1 boundary and the cluster-count→stage mapping should be decided from the Stage-0/pilot EDA, not pre-committed. I record the divergence and the PIPE-compatibility constraint; the owner chooses retain-threshold vs hybrid-discover-then-freeze.

---

## Section 7 — The `D` conflict and `τ_L` / `L_max`

### `D = 6.694` vs `D ≈ 4.6416` (the worked seed-conflict)
**`D ≈ 4.6416` is locked; the question is reconciliation, not selection.** Per item 6 / CLM-19 / PHYS-01, `D=(G·T²)^(1/3)≈4.6416` (raw-mass; `G=1`, and consistently `T=10` since `4.6416³≈100=T²`). The total-mass `D=6.694` (`M_tot=3`) was rejected by v1.5 EVID-10 and "no configuration parameter may select the mass-fraction form" (`ctl_instruction.md §2.5`). CLM-01 (`6.694`) is claimed-unverified; CLM-19 (`4.6416`) is verified/locked.

**The genuinely useful finding on `compute_tau_L`:** in the issue doc's `compute_tau_L`, the `D = cbrt(G·M_tot_ref·T_scale²) = 6.694` and `V = D/T_scale` lines are computed but appear **unused** — the `rhs()` acceleration uses raw masses with no `D`/`V` dependence, and integration runs on `y0` assembled directly from `r_prime`/`v_prime`. If that reading is correct (it should be **verified by code inspection**, which is outside the attached materials, so I log it as a gap), the `D=6.694` error is **dead code with no numerical effect on `τ_L`** — a hygiene defect, not a results defect. *Candidate edit:* remove the dead `D`/`V` (or set to the locked `4.6416`) and add a regression test confirming `τ_L` is unchanged; purge the `6.694` reference regardless to prevent contamination if the variable is ever activated.

### `L_max` and `τ_L` formulas
- **`L_max`: confirmed consistent.** The issue doc's `L_max = M_total·r_char·v_char` with `v_char=sqrt(2|E|/M_total)` matches `ctl_instruction.md` Step 3 item 2 (the canonical `compute_L_norm`). No conflict.
- **`τ_L` method: divergence to resolve.** The spec designates a **Rosenstein-style** estimator operating on the Brutus time series (`ctl_instruction.md` Step 3 item 5: delay embedding, nearest neighbors with Theiler window, divergence-curve slope), and the spec's own pipeline note recommends the faster batch approximation for ~15K trajectories. The issue doc instead inlines a **shadow-trajectory** routine (perturb by `epsilon_pert=1e-8`, re-integrate nominal + perturbed, track divergence; potential softening `epsilon_soft=1e-10`), while *also* mentioning "PCA+Rosenstein batch approximation." These are different families: Rosenstein works from existing trajectory data and is cheaper/robust for batch use; shadow-trajectory requires re-integration and introduces extra softening hyperparameters. If the code is a hybrid (Rosenstein estimation applied to shadow-divergence data) it could be spec-compatible, but this is unclear from the materials — **log a gap**. On softening: `epsilon_soft=1e-10` here is *numerically equal to* `ε_inv` but is an independent offline parameter; it is **not** the locked loss-side `1e-5` and must not be collapsed into it. *Candidate resolution (owner decision):* clarify the implemented method, then either align the code to the spec's Rosenstein-style designation (recommended for batch cost/robustness, retaining shadow-trajectory only as a calibration diagnostic) or update the spec — and specify the missing Rosenstein parameters (embedding dim, delay, Theiler window, fit window) which are not fully pinned in the attached spec.

---

## Section 15 — ALM `μ_p` clamp

**Misattributed to a rejected formulation.** The issue doc's `μ_p = clip(μ_p, 1e-4, 100.0)` and the surrounding RMSprop-style `v_p`/`μ_p` machinery belong to the **dense-residual pseudo-ALM** that the spec **explicitly rejects** (`ctl_instruction.md` loss formulation; `pinn_architecture.md §4.1`). The only surviving ALM is the **P2 ablation on scalar conservation constraints** (`§4.2`), whose penalty/multiplier variables would be per-constraint (e.g. for energy/angular-momentum drift), not the dense-residual `μ_p`, with dual updates only between Adam epochs / refinement passes and never inside L-BFGS. So in the baseline loss the clamp has **nothing to attach to**. *Candidate resolution:* annotate the finding **misattributed — belongs to rejected dense ALM**. If and when the P2 ablation is activated, a clamp on *its* scalar-constraint multipliers is a reasonable safety measure to add then; it is a conditional/FUT item, not a baseline edit. The spec's `μ_p` clamp `[1e-4,100]` is listed in the claims-register's non-dataset spec-parameter exclusions, consistent with this.

---

## Consolidated view for the owner

**Already settled by the current spec (issue-doc framing stale) — ratify and annotate obsolete:** causal-training mode (PHYS-05 causal weighting; dense ALM rejected); epsilon strategy (dual-context already chosen); B-08 (point sets already separate); M7 (`τ_L` already excluded); NS-12 (PHYS-02 already satisfies); NS-18 (Huber already replaces L1/MAE); M15 (PHYS-05 schedule stands; CLM-11 obsolete); `μ_p` clamp (attaches to rejected dense ALM).

**Confirmed with small reconciliations:** B-07 (fix `min(32, n_snapshots)` pseudocode bug); M14 (merge as `C_stage·median`; owner picks stages-0–1 value in `[7,10]`, `8.5` not endorsed); M6 (clamp only for staging/diagnostics, IC-mapping framing dead).

**Genuine open decisions requiring owner input + empirical data:** D5 stage-transition fallback and the `≤min`→`percentile_10` relaxation (calibrate via Stage-0 pilot; CLM-08/09 unverified); adaptive stage assignment (hybrid discover-offline-then-freeze, reconcile the 0–2 vs 0–1 boundary and `k=6`→7-stage mapping, preserve PIPE contracts); s_min — confirm no collision loss vs commission a new one; `τ_L` method (Rosenstein vs shadow-trajectory).

**Logged gaps (do not invent):** code-level confirmation that `D=6.694` is dead in `compute_tau_L`; the normalized `|ΔH|` distribution (NS-13 δ); collocation-density × resolution evidence (M16/CLM-20); strict-criteria attainability (D5); per-stage population counts (CLM-02..07); missing Rosenstein estimator parameters. All are FUT/empirical — v1.6 has no in-milestone phase to verify them, so they remain unverified inputs, not facts.

Where the issue doc's "Recommended Resolutions" assert adopted values (e.g. CLM-10/11 tables, `D=6.694`, L1 data loss, dense-ALM `μ_p`), those are not transcribed as decisions; the spec baseline governs, and proposed changes to the revisable contracts are framed above as owner-authorizable options.
===== END ISSUE03-SECTION-f26fed61251ff665 REPORT R7 =====
