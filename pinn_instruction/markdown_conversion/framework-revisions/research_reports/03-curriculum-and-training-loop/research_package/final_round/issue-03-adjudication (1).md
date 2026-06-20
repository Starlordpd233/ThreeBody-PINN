# Issue 03 — Final Adjudication: Curriculum and Training Loop (doc-03)

**Adjudicator posture.** An independent claim ledger was built from the canonical-sources bundle
*before* any report was read, then every report claim was mapped onto it. No voting, no averaging,
no majority-merge. Report agreement is not evidence; every disposition rests on a canonical source
section read and verified directly (hard constraints, claims register, verified-facts, and the
framework specs `ctl_instruction.md` / `pinn_architecture.md`). The model behind each R# is unknown
and irrelevant. Reports that claimed attached material was missing/truncated were checked against the
actual attachments (the material is present); their resulting gap/insufficiency claims were not
propagated.

Canonical sections are cited as **[S#/file §]**, report provenance as **[R#]**. The issue doc (S3)
is the non-authoritative subject; its live-code "Canonical" citations are overridden per
**[S2/scope-12 §2]**.

---

## PART 1 — Final Issue 03 Resolution

### Cross-cutting findings (apply to many verdicts)

- **XC-1. The issue doc was largely written against an *earlier* spec revision.** Stale premises:
  "global+ALM is current SOT," L1/MAE data loss, `lambda_E ~ 1000`, the dense-ALM `mu_p` machinery,
  and the `L_norm`->IC-vector mapping. Separating genuine open work from stale framing is the bulk
  of the task. Basis: **[S5/ctl Loss-Function-Formulation; S5/pinn 3.1, 4.1, 5.3.1; S3]**; surfaced
  by **[R2 C1/C2, R3, R4, R7]**.
- **XC-2. `review_of_framework.md` (S6) is a superseded baseline on specific contracts** (it carries
  an explicit critique mandate, so flagging this is in scope). Superseded: 2.2 softening (additive
  `(||r||+eps)` = the locked PHYS-03 anti-pattern; "1e-5 everywhere" superseded by dual-context),
  4.3 AD reference (all-ones-covector / `r.sum()` anti-pattern), 4.2 dense ALM (rejected), the <=1e3
  energy weight (superseded by PHYS-05's cap at 1). Surviving/usable: the `L_max` formula, the
  replay/lookahead + 50/50 batch protocol, the curriculum `C` schedule, ALM state-reset at stage
  boundaries, and the 2.2 *value* argument (1e-5) as one input to the epsilon decision. Basis:
  **[S5/ctl 2.5, Loss-Function-Formulation; S5/pinn 3.2, 4.1, 4.2, 5.3.1; S2/scope-12 2, item 4]**;
  **[R1 6, R2 C2, R3, R7]**.

### Section 2 — Three decisions reserved for the framework owner (options posed; none selected)

**D-04 / Causal-training-mode -- `surface_to_user`.** The issue doc's claim that **Option B (global
sampling + dense ALM) is the current SOT is factually wrong against the spec.** `ctl_instruction.md`
adopts **causal weighting** as the PHYS-05 default (`w_n = exp(-eta_c * sum_{m<n}
stopgrad(R_m))`, `eta_c=1`) and **explicitly rejects** the dense-residual pseudo-ALM
`L_data + lambda_p*L_phys + (mu_p/2)*L_phys^2 + lambda_E*L_energy`; ALM survives only as a P2
ablation on *scalar* constraints **[S5/ctl Loss-Function-Formulation; S5/pinn 3.2, 4.1, 4.2]**. So
the options map as: **A (causal weighting) ~ current baseline; B ~ the explicitly rejected
formulation (a reversion/departure from the spec, not preservation of SOT); C ~ a large un-specced
rewrite.** The `stopgrad` in the weights already partially mitigates the "causal firewall" risk
attributed to A. No dataset figure gates this; no A/B/C empirical comparison exists in the package.
Owner decides; the issue doc's Section-2 causal framing is annotated **obsolete -- superseded by
PHYS-05**. **[R1 1.1, R2, R3, R4, R5, R7]**.

**D-05 / s_min-frame -- `surface_to_user`.** The spec already implements **Option A**: unsoftened
geometric `s_min` from "true pairwise separations (no softening)" for the curriculum gate
**[S5/ctl Step 3 item 1]**, with softening confined to loss potentials (`eps_inv=1e-10` in `V` only;
`eps_train=1e-5` in residual/energy) **[S5/pinn 3.2, 3.4]**. **Critical correction:** the loss-side
softening is the **locked matched-Plummer** `sqrt(||dr'||^2 + eps^2)` **[S2/scope-12 item 4]**, *not*
the additive `max(s_min, eps)` the issue doc writes -- an additive `max(s_min, eps)` would itself be
the prohibited PHYS-03 anti-pattern. The issue doc therefore **conflates** (a) confirming the
existing gate (no training-loss collision term) with (b) implicitly proposing a *new* collision-loss
term. Owner chooses (a) ratify status quo, or (b) commission a genuinely new close-encounter loss
designed under PHYS-03. Distinct from D5. **[R1 1.2, R2, R3, R7]**.

**D-06 / Epsilon-strategy -- `surface_to_user` (open part only).** **LOCKED:** loss-side
`eps_train=1e-5` in both physics residual and energy regularizer **[S2/scope-12 item 4;
S4/claims-register CLM-19 companion / PHYS-03]** -- not re-openable. The spec baseline already
answers the open part as **Option B (dual-context)**: `eps_inv=1e-10` is "context-specific for
offline invariant computation and is distinct from the training-time softening `eps_train=1e-5`"
**[S5/ctl Step 3 item 1]**, with the dual-epsilon note in **[S5/pinn 3.4]**. Option A (collapse
offline to 1e-5) would coarsen `E`/`Q`/stage assignment; Option C (1e-10 everywhere) is incompatible
with the lock and argued against on float-precision grounds. `review_of_framework.md` 2.2's
"1e-5-everywhere" value argument is a legitimate input but its *additive form* is superseded
**[S6/review 2.2]**. Owner ratifies dual-context or chooses A. The issue doc's "truncated 1e-10
justification" is largely a transcription artifact resolvable from the same file **[R2]**.
**[R1 1.3, R2, R3, R4, R5, R7]**.

### Section 3 — Confirmed findings (BLOCKING / MAJOR)

**B-07 / Replay-lookahead batch construction -- `accepted` (contract) + `modified` (pseudocode).**
The spec already encodes the contract: replay `B_<=k=240`, lookahead `B_{k+1}=16` (batch 256),
`n_pts(traj)=min(n_pts_cap=32, n_snapshots)` without replacement, 50/50 acceleration-weighted
(Gumbel-top-k) + uniform **[S5/ctl Mini-Batch-Construction]**; the gap is the legacy flat `get_batch`
**[S5/pinn 3.1]**. **Required reconciliation:** the audit Section-6 pseudocode hard-codes a **fixed
32** (`np.random.choice(..., replace=False)`), which violates the locked M12 rule
`min(32, n_snapshots)` and will error/under-sample on low-snapshot trajectories (per-trajectory
minima can fall below 32 even though medians are 61/127/1003, **CLM-16**). Fix the pseudocode to
`min(32, n_snapshots)`. Counts 240/16/8192/4096 are **CLM-12 `claimed-unverified`** design constants
-- record as claimed, not fixed. Edge cases (final stage with no k+1; undersized/absent next-stage
pool; trajectory-level replacement; cross-pool dedup after relabeling; replay stage balance) are
**source-silent -> see Gap G-l**. **[R1 3.1, R2, R3, R5, R7]** (R4 asserted "no reconciliation
conflict," missing the fixed-32 bug).

**B-08 / Data-fidelity vs collocation separation -- `accepted` + `modified` (L1->Huber).** The two
roles already exist -- data-fidelity Huber term `N_data=256x32=8192` **[S5/pinn 3.1]** and
collocation physics residual `n_col=4096` **[S5/pinn 3.2]**; make the separate-set discipline
explicit in the batch constructor. **Correction:** the issue doc's data loss is **L1/MAE**, but the
current data term is **Huber (`delta_r=1`)** -- "the previous MAE/L1 data-loss prose is replaced by
this Huber contract" **[S5/pinn 3.1]**; adopt Huber on scaled positions. Counts **CLM-12 claimed**.
The collocation count per trajectory diverges (review 5.1 ~256/traj vs issue 16/traj) -> **Gap
G-e**; the issue doc's "both 50/50" is unproven for collocation (50/50 is defined for snapshot data
points, not a continuous-time collocation sampler) -> **Gap G-f**. **[R1 3.2, R2, R3, R4, R7]**.

**M6 / `L_norm` clamping -- `modified` (premise obsolete).** Under the locked 14D `[tau, IC13]`
contract **[S2/scope-12 item 1]**, `L_norm` is **metadata** (staging/diagnostics/loss-scaling), not
an IC slot **[S5/ctl Step 4]**; the "clip before `2x-1` IC mapping" rationale no longer applies, and
`L_norm>1` is physically valid. `compute_L_norm` returns `L/(L_max+eps)` **[S5/ctl Step 3 item 2]**.
The only residual concern is that stage-gating must not assume `L_norm in [0,1]`. Resolution: apply a
`[0,1]` clamp (or `>1` warning) **for staging/diagnostic use only**, never into any network input;
the safer contract persists the **raw** `L_norm` + a validity flag and derives any bounded feature
separately rather than silently overwriting **[R3]**. **[R1 3.3, R2, R3, R4, R5, R7]** (R6 endorsed
the obsolete clamp-into-IC framing -- overridden, see DR-7).

**M7 / `tau_L` excluded from IC vector -- `accepted`.** Concordant with the issue doc. `tau_L` is
returned in the invariant tuple and used in `(E,Q,s_min,L_norm,tau_L)` for default stage gating, but
excluded from `IC13` **[S5/ctl Step 3, Step 4]**, consistent with the locked 14D Jacobi-state input
**[S2/scope-12 items 1-2]**. Adding it would leak a full-trajectory-derived quantity into an
initial-state input. Spec already correct; only remove any lingering "tau_L is an input" text.
**[R1 3.4, R2, R3, R4, R5, R6, R7]**.

**M14 / Merged gradient clipping -- `accepted` (merge) + `modified` (8.5 not endorsed).** Merge as
`clip = C_stage * median(last 100 grad-norms)`. The two halves are not truly in conflict: the
`5.0 x median` in **[S5/pinn 4.4]** **is** the stages-2-3 value of the curriculum `C` schedule
(0-1: 7-10; 2-3: 5; 4-6: 3) in **[S5/ctl Adaptive-Median-Based-Gradient-Clipping]** -- replace the
standalone `5.0` with `C_stage`. Clipping is Adam-only, disabled in L-BFGS. The issue doc's `C_table`
value **8.5 (CLM-10 `claimed-unverified`)** is an arbitrary midpoint of the spec's **[7,10] range**;
the stages-0-1 value is an owner choice within `[7,10]` (8.5, 7, or 10 all defensible) and is **not**
spec-endorsed. Bootstrap-before-history-window and gradient-history reset at stage boundaries are
unspecified -> **Gap G-m**. **[R1 3.5, R2, R3, R4, R5, R7]**.

**M15 / Energy-loss weight schedule -- `rejected` (issue-doc fix) / spec stands.** The issue doc's
premise is **superseded**: PHYS-05 sets `lambda_E^max(k)=lambda_L^max(k)={0 for k in {0,1};
10^{k-4} for k in {2,3,4}; 1 for k in {5,6}}` with linear warmup `I_warm=min(2000, 0.1*N_Adam,k)`
**[S5/pinn 4.1]** -- energy is **off** at 0-1 and **capped at 1.0**, far below both the issue doc's
stale `1000` and its `cap_table` peak of 500. The `cap_table` **(CLM-11 `claimed-unverified`)** is
10x-500x larger at every stage; adopting it would **raise** late-stage energy weight against the
spec, the opposite of M15's stated safety intent. **Keep PHYS-05.** The dominance safeguard is
optional and low-value under a cap of 1. If a future ablation shows the cap is too low at 5-6, a
modest increase is a separate evidence-gated proposal -- not 500. **[R1 3.6, R2, R3, R7]**. *Minority
overridden:* R4 framed this as an open A/B/C choice with a hybrid raising stages 5-6 to 200/500; R6
endorsed the cap_table -- both miss the spec cap-at-1 (see DR-1).

**M16 / `dt_out`-aware collocation scaling -- `defer` (source-silent / spec defers).** The spec
**explicitly defers** the rule: `dt_out`/`n_snapshots` are exposed as forward-interface loader
metadata, "not used here" **[S5/ctl Mini-Batch-Construction / 2.6]**; `n_col=4096` is fixed
**[S5/pinn 3.2]**. Three live positions: review 5.3 (**no scaling needed** -- collocation samples
continuous `[0,T]`, resolution-independent) **[S6/review 5.3]**; issue `n_col ~ dt_base/dt_out`
**(CLM-20 `claimed-unverified`)**; spec defers. The `dt_base/dt_out` direction gives **fewer**
collocation points to lower-resolution trajectories (~0.059x standard) -- against the issue doc's own
stated motivation -- and `dt_base=0.01` is an unjustified assumption. Per-variant `dt_out` is
**verified (CLM-17)** but the scaling *rule* is not. Coupling `n_col` to `dt_out` is weakly motivated
since collocation is not at snapshot times; difficulty (close encounters) is the better driver.
**Keep the deferral; do not adopt either direction; FUT.** -> **Gap G-g**. **[R1 3.7, R3, R7]**.
*Minority preserved:* R2/R4 confirm/adopt the `dt_base/dt_out` direction; R5/R6 lean adopt (see DR-2).

**D5 / Stage-transition criteria -- `accepted` (dual-path structure + relaxation direction) / figures
`defer`.** The critique is well-founded and already half-conceded: the four strict criteria (plateau
`eps_plateau=1e-5` patience 200; **validation `<=min`**; physics `eps_phys=1e-4`; energy drift
`eps_energy=1e-4` using the **locked `eps_H=1e-4*S_H`**) carry the author's own attainability note
**[S5/ctl Stage-Transition-Criteria]**. The load-bearing change is relaxing criterion 2 from `<=min`
to `<=percentile_10` (sound for chaotic, non-monotonic validation loss). Adopt the **dual-path
structure** and the relaxation *direction*; per-stage thresholds **(CLM-08)** and `MAX_EPOCHS`
**(CLM-09)** are **`claimed-unverified` design hypotheses ("not fixed")** -> FUT-calibrate via a
Stage-0 pilot, not lock. -> **Gap G-h**. **[R1 3.8, R2, R4, R7]**. **Material owner sub-choice to
surface:** whether the fallback may *auto-advance*. R3 (partly R4) argue the fallback must separate
**ADVANCE / RECOVER / HALT-OWNER-REVIEW** -- max-epochs, stagnation, and NaN-rollback must **not**
automatically advance a stage; R7 offers graduated options. Preserved (see DR-3).

**NS-12 / Componentwise AD -- `accepted`.** The spec already satisfies NS-12: PHYS-02 requires all
nine `dr'_{i,a}/du`, **forbids** `torch.autograd.grad(r.sum(), u, ...)` (the summed-output proxy),
lists acceptable patterns (`jacrev`+`vmap`, per-component loop, full-Jacobian), and gives a worked
synthetic-trajectory test with a `<1e-6` acceptance check **[S5/pinn 5.3.1, 10.3]**. **Upstream
correction:** `review_of_framework.md 4.3`'s reference impl uses the forbidden all-ones-covector
`torch.autograd.grad(..., grad_outputs=torch.ones_like(r), ...)` -> must be replaced with the
PHYS-02 contract **[S6/review 4.3]** -> **Gap G-o**. Executable three-body batch impl is FUT/Phase-21
(VER-04). **[R1 3.9, R2, R3, R4, R5, R6, R7]**.

**NS-13 / Huber energy delta -- `modified` (direction) / value `defer`.** `delta=1.0` is **revisable**
(not locked) **[S5/pinn 3.4]**. Because the residual `dH_n` is *normalized* by `|H_eps(r_0)|+eps_H`
and is plausibly O(1e-4..1e-2), `delta=1.0` puts essentially all samples in the quadratic branch
(Huber -> L2), losing outlier robustness -- a sound critique shared by three sources. **Reduce delta
below 1.0**, but the **exact value is unverified**: no `|dH|` distribution is in the package.
FUT-calibrate per stage (review 4.4's `delta=0.1` is a reasonable starting hypothesis; quantile-tuned
0.01-0.1 per issue doc); whether delta becomes stage-dependent is open. -> **Gap G-i**. Note: the
same `delta=1.0` default also appears on the *data* Huber (3.1), where residuals are O(0.1-1) so
`delta_r=1` is more plausibly appropriate -- audit the two delta defaults jointly **[R7]**.
**[R1 3.10, R2, R3, R4, R7]**.

**NS-18 / Loss-component scaling contract -- `accepted` + `modified` (L1->Huber).** The units/scaling
contract is coherent: all terms dimensionless under `G=1`, `r'=r/D` (locked `D`, **CLM-19**); data =
Huber on scaled positions **[S5/pinn 3.1]**; physics residual `eps_train=1e-5` + causal weighting
**[3.2]**; energy regularizer same `eps_train` on the **same** collocation set **[3.4]**; PHYS-05
composition **[4.1]**. The one substantive change is the same L1/MAE->Huber data-term correction as
B-08. The chain-rule factor `d2r'/du2 = 4*d2r'/dtau2` applies **only** when differentiating w.r.t.
`tau`, not unconditionally **[R3, R7]**. **[R1 3.11, R2, R3, R4, R7]**.

### Section 6 — Data-driven adaptive stage assignment -- `modified` (constrained augmentation)

Adopt the adaptive methodology (EDA over invariants, `Q_norm=Q/s^3` virial correction, PCA, K-means,
quantile thresholds, population safeguard, PINN pilot) as an **augmentation** to the threshold-based
Step 5, **constrained to preserve the locked multi-fidelity stage topology**. The motivation is
grounded: the spec author's own note invites the data-scan because the virial ratio is not preserved
under quasi-random Sobol sampling, and `sampling_method.md` confirms the scale factor `s in [0.8,1.2]`
from Sobol `u4` makes `Q` scale as `s^3` **[S5/sampling Sampling-Time-Size-Variability; S5/ctl
Multi-Stage-Data-Stratification]**.

**Decisive structural constraint:** `stage_strat_revision.md` **Table 4 cannot be adopted
wholesale.** The spec places hierarchical in **Stages 0-2** (Stage 2 = high-resolution hierarchical
refinement, Set 2a) and quasi-random in **Stages 3-6** (Stage 5 = high-resolution chaotic, Set 2b)
**[S5/ctl Multi-Stage-Data-Stratification, Stages 0/1/2/5/6]**; Table 4 reorders purely by chaos
clustering (hierarchical->0-1, quasi-random->2-6) and **dissolves the gold-refinement roles of Stages
2 and 5** **[S6/stage_strat Part III/Table 4]**, conflicting with the multi-fidelity design and the
locked Stage-5 gold-counterpart obligation (every Stage-4-admitted ID owes a Stage-5 gold sample;
the **184** standard IDs without a gold counterpart are genuine Stage-5 holes -- **CLM-14 verified**)
**[S5/ctl Step 5; S4/verified-facts VF-3]**. **Reconciliation:** the adaptive criteria may set the
*within-fidelity* boundaries (quantiles/clustering) but must **preserve** the fidelity-stage roles
and the gold-counterpart/hole accounting. The PIPE-compatible posture is to **discover boundaries
offline (fixed seed, versioned normalization) then freeze them as fixed thresholds** producing a
stable seven-stage labeling per `record_key` -- **do not run K-means at training time**, since the
locked stage-query contracts (`sample_replay`, `sample_lookahead`, `has_stage`, PIPE-01..10) require
materialized integer labels **[S2/scope-12 item 7; R7]**.

Per-stage counts **CLM-02..07 are `claimed-unverified`** design outputs of the adaptive method -- not
facts; the `~2,565` gold count beside them is the **verified CLM-15** gold count, not a stage count.
Open owner/data gaps: population safeguard **5% (stage_strat) vs >10% (issue)**; clustering **k=5 vs
k=6-7**, with **k=6 yielding only six clusters for a seven-stage space** (R7); whether the scale
factor `s` is persisted per IC (if absent, `Q` must be excluded for the quasi-random set); the exact
gold-hole accounting (184 base-minus-gold vs the spec's Stage-5 dedup-prefer-gold hole count);
EDA/pilot results absent -> **Gap G-k**. **[R1 4, R2, R3, R4, R7]**. *R5 and R6 declined this finding
on the false premise that `stage_strat_revision.md` is not attached -- it is (S6); their
non-adjudication carries no weight (see DR-5, DR-6).*

### Section 7 — The `D` conflict and the `tau_L` / `L_max` formulas

**D = 6.694 vs D ~ 4.6416 -- `rejected`/`accepted` (LOCKED).** `D=(G*T^2)^(1/3)~4.6416` (raw-mass,
`G=1`, `T=10`) is the **SCOPE-12-locked** value **(CLM-19 verified)** **[S2/scope-12 item 6; S5/ctl
2.5; S4/verified-facts VF-5]**; the total-mass `D=6.694` (`M_tot=3`) **(CLM-01 `claimed-unverified`)**
was rejected by v1.5 Phase 25 EVID-10, and "no configuration parameter may select the mass-fraction
form" **[S5/ctl 2.5]**. Reconciliation under the locked value, not selection.

**Downstream consequence -- `accepted` core + logged gap.** In the issue doc's `compute_tau_L`, the
`D=cbrt(G*M_tot_ref*T_scale^2)=6.694` and `V=D/T_scale` lines are **assigned but never used** -- the
RHS uses raw masses with no `D`/`V` dependence and integration runs on already-scaled `r'`/`v'`
**[S3, "tau_L and L_max Formula Resolution"]**. `D` also does **not appear explicitly** in the
`L_max` or `tau_L` formulas, which consume already-scaled `(r',v',E)`; the locked `D` enters only
upstream at preprocessing `r'=r/D` **[S5/ctl 2.5, Step 3 item 2]**. Therefore, **under the locked
`D` no re-derivation of the formulas is required**; the edits are: delete/correct the dead
`D=6.694`/`V` lines, strike the line-305 "corrected B-02" comment, and **drop the issue doc's P4-1
"re-run stage assignment under corrected D=6.694" directive** (the existing locked-D invariants and
thresholds stand). **Logged gap:** the "dead code" reading is from the snapshot text; full
confirmation needs code inspection beyond the attachments -> **Gap G-d**. **[R1 2.1, R2, R7]**.
*Minority preserved:* R3/R4/R5 take a more cautious "recompute/verify thresholds under locked D" or
"re-derive" stance (R4 calls re-derivation needed; R5 flags the explicit equations as missing) -- see
DR-4. The caution is reasonable as verify-before-assuming but is not required by the sources, which
tie thresholds to the locked raw-mass scaling.

**`L_max` -- `accepted` + `modified` (interpretation narrowed).** `L_max=M_tot*r_char*v_char`,
`v_char=sqrt(2|E|/M_tot)`, `r_char=(1/3)*sum_{i<j}||r'_i-r'_j||`, `L_norm=L/L_max` is identical across
`ctl_instruction.md` Step 3 item 2, the issue doc, and review 1.1 **[S5/ctl Step 3 item 2; S6/review
1.1]**. **Narrowing:** it is a **characteristic ("circular-orbit") normalization scale**, not a
proven global maximum of arbitrary three-body angular momentum -- document it as such (the spec
already uses cautious wording), add degeneracy guards for `M_tot<=0`, `r_char~0`, `|E|~0`, non-finite
inputs, and do not hide degeneracy by unconditional clipping **[R3, R7]**.

**`tau_L` estimator -- `defer` (genuine method divergence + unit ambiguity).** Two estimator families
coexist and the spec does **not** state which is canonical: a **Rosenstein-style** estimator on the
Brutus time series (no re-integration, no softening) **[S5/ctl Step 3 item 5]** (also stage_strat
Phase I), versus a **Benettin/shadow-trajectory** estimator (`eps_pert=1e-8`, re-integrate
nominal+perturbed, `eps_soft=1e-10` static softening) **[S3; S6/review 1.1]**, plus an
under-specified "PCA+Rosenstein" batch approximation. These can give different `lambda_max`. The
split softening `eps_pert=1e-8`/`eps_soft=1e-10` is **distinct from the locked loss-side 1e-5 and
must not be collapsed** **[S2/scope-12 3]**, and applies only to the shadow method. **Plus a
unit-convention gap:** the spec returns `tau_L=1/lambda` while the issue doc returns
`tau_L=T_scale/lambda` (factor of 10), and the stage thresholds (`tau_L>5`; `2<tau_L<=5`) are not
pinned to a time axis -- must be resolved before locking any `tau_L` threshold **[R2 G2, R3, R7]**.
The issue doc's shadow code also uses a **non-Plummer** `||dr||^3+eps` softening **[R3]**. Owner picks
the canonical estimator; FUT cross-calibrates. -> **Gaps G-b, G-c**. **[R1 2.2, R2, R3, R7]**.

### Section 15 — ALM `mu_p` clamp -- `modified` (N/A to baseline; conditional on P2 ablation)

The clamp `mu_p=clip(mu_p, 1e-4, 100.0)` and its RMSprop-style `v_p`/`mu_p` update belong to the
**dense-residual pseudo-ALM that the spec rejects** **[S5/ctl Loss-Function-Formulation; S5/pinn 4.1:
"No dual variables are part of the default training loss"]**. In the baseline loss the clamp has
**nothing to attach to**. ALM survives only as the **P2 ablation on scalar conservation constraints**
(`c_E`, `c_{L,a}`; dual updates only between Adam epochs / refinement passes, never in L-BFGS;
default OFF) **[S5/pinn 4.2]**. The clamp lands **only if** that ablation is enabled and uses an
adaptive penalty parameter, applied at the 4.2 between-epoch cadence. The bounds `[1e-4,100]` are a
**non-dataset spec parameter** (claims-register exclusion), not a CLM figure; not adoptable as
validated, so any specific clamp follows a defined scalar-ALM update law -> **Gap G-n**. **[R1 5, R2,
R3, R4, R5, R7]**.


---

## PART 2 — Claim Matrix

`uncertainty_type` legend: **locked** (SCOPE-12, not re-openable) - **spec-grounded** (resolved by
the framework specs as source of truth) - **owner-decision** (genuine framework-owner choice) -
**figure-unverified** (CLM `claimed-unverified`, no v1.6 verification, FUT) - **source-silent**
(attachments do not settle it) - **method-divergence** (multiple un-reconciled methods).

| claim_id | issue_section | final_disposition | canonical_source_basis | supporting_R# | opposing_R# | uncertainty_type |
|---|---|---|---|---|---|---|
| C-CAUSAL | D-04 causal mode | surface_to_user (B-is-SOT rejected) | S2 scope-12; S5 ctl Loss-Formulation; S5 pinn 3.2/4.1/4.2 | R1,R2,R3,R4,R5,R7 | (R6 vague-concur) | owner-decision |
| C-SMIN | D-05 s_min frame | surface_to_user (spec=Option A; max != Plummer) | S5 ctl Step 3 item 1; S5 pinn 3.2/3.4; S2 item 4 | R1,R2,R3,R4,R5,R7 | none | owner-decision |
| C-EPS | D-06 epsilon | surface_to_user (open part); loss-side locked | S2 item 4; S5 ctl Step 3 item 1; S5 pinn 3.4; S4 CLM-19 | R1,R2,R3,R4,R5,R7 | none | locked + owner-decision |
| C-B07 | B-07 batch | accepted (contract) + modified (fixed-32 -> min) | S5 ctl Mini-Batch; S5 pinn 3.1; S4 CLM-12/16 | R1,R2,R3,R5,R7 | R4 (missed bug) | spec-grounded + figure-unverified |
| C-B08 | B-08 point sets | accepted + modified (L1 -> Huber) | S5 pinn 3.1/3.2; S4 CLM-12 | R1,R2,R3,R4,R7 | none | spec-grounded + figure-unverified |
| C-M6 | M6 L_norm clamp | modified (IC premise obsolete; metadata guard) | S2 item 1; S5 ctl Step 3 item 2/Step 4 | R1,R2,R3,R4,R5,R7 | R6 (endorsed obsolete) | spec-grounded |
| C-M7 | M7 tau_L exclusion | accepted | S2 items 1-2; S5 ctl Step 3/Step 4 | R1,R2,R3,R4,R5,R6,R7 | none | spec-grounded |
| C-M14 | M14 clip merge | accepted (merge) + modified (8.5 not endorsed) | S5 pinn 4.4; S5 ctl Adaptive-Median-Clipping; S4 CLM-10 | R1,R2,R3,R4,R5,R7 | none | spec-grounded + figure-unverified |
| C-M15 | M15 lambda_E schedule | rejected (cap_table); PHYS-05 stands | S5 pinn 4.1; S4 CLM-11 | R1,R2,R3,R7 | R4 (open A/B/C), R6 (adopt) | spec-grounded |
| C-M16 | M16 collocation scale | defer (spec defers; rule unverified) | S5 ctl Mini-Batch/2.6; S5 pinn 3.2; S6 review 5.3; S4 CLM-17/20 | R1,R3,R7 | R2,R4 (adopt); R5,R6 (lean adopt) | source-silent + figure-unverified |
| C-D5 | D5 transitions | accepted (structure+relax dir); figures defer | S5 ctl Stage-Transition-Criteria; S4 CLM-08/09 | R1,R2,R4,R7 | R3 (no auto-advance); R4 partial | spec-grounded + figure-unverified |
| C-NS12 | NS-12 componentwise AD | accepted | S5 pinn 5.3.1/10.3; S6 review 4.3 (anti-pattern) | R1,R2,R3,R4,R5,R6,R7 | none | spec-grounded |
| C-NS13 | NS-13 Huber delta | modified (delta<1.0 dir); value defer | S5 pinn 3.4 | R1,R2,R3,R4,R7 | none | figure-unverified |
| C-NS18 | NS-18 scaling | accepted + modified (L1 -> Huber) | S5 pinn 3.1/3.2/3.4/4.1; S4 CLM-19 | R1,R2,R3,R4,R7 | none | spec-grounded |
| C-ADAPT | Sec 6 adaptive staging | modified (constrained augmentation) | S5 ctl Multi-Stage-Strat/Step 5; S5 sampling; S6 stage_strat; S4 CLM-02..07/14/15 | R1,R2,R3,R4,R7 | R5,R6 (declined: false missing-file) | figure-unverified + owner-decision |
| C-DVAL | Sec 7 D conflict | rejected(6.694)/accepted(4.6416) -- LOCKED | S2 item 6; S5 ctl 2.5; S4 CLM-01/19, VF-5 | R1,R2,R3,R4,R5,R6,R7 | none | locked |
| C-DINERT | Sec 7 D downstream | accepted core (inert; drop P4-1) + gap | S3 compute_tau_L; S5 ctl 2.5/Step 3 | R1,R2,R7 | R3,R4,R5 (recompute/verify) | spec-grounded + source-silent |
| C-LMAX | Sec 7 L_max | accepted + modified (characteristic, not max) | S5 ctl Step 3 item 2; S6 review 1.1 | R1,R2,R3,R4,R5,R7 | none | spec-grounded |
| C-TAUL | Sec 7 tau_L estimator | defer (method divergence + unit gap) | S5 ctl Step 3 item 5; S3; S6 review 1.1; S2 3 | R1,R2,R3,R7 | R4,R5 (adopt/confirm) | method-divergence + source-silent |
| C-MUP | Sec 15 mu_p clamp | modified (N/A baseline; P2-conditional) | S5 ctl Loss-Formulation; S5 pinn 4.1/4.2 | R1,R2,R3,R4,R5,R7 | none | spec-grounded + source-silent |

---

## PART 3 — Disagreement Register

Every material conflict, including minority positions. Conflicts are resolved against the canonical
source, never by report count; minority positions are preserved.

- **DR-1 (M15 disposition).** *Majority/spec-grounded:* cap_table is obsolete; PHYS-05 caps lambda_E
  at 1; adopting cap_table would raise late-stage weights (R1,R2,R3,R7). *Minority:* R4 presents M15
  as an open A/B/C owner choice with a "hybrid" raising stages 5-6 to 200/500; R6 endorses the
  cap_table outright. *Adjudication:* **overridden by [S5/pinn 4.1]** -- the spec is the source of
  truth and caps lambda_E^max at 1; R6's position also rests on never reading pinn (it wrongly calls
  the file absent). Disposition: reject cap_table. R4's "if the cap proves too low, raise modestly"
  survives only as a future evidence-gated proposal, not as the cap_table.

- **DR-2 (M16 adopt vs defer).** *Defer camp:* R1,R3,R7 (insufficient evidence; spec defers; coupling
  weakly motivated; direction perverse). *Adopt camp:* R2,R4 adopt `dt_base/dt_out`; R5,R6 lean
  adopt. *Adjudication:* **defer** -- the spec itself defers the rule **[S5/ctl 2.6]**, CLM-20 is
  unverified, review 5.3 argues no scaling, and the direction is physically contested. The adopt
  positions make a design call the sources do not ground. Preserved as a live owner/FUT option; not
  adopted now.

- **DR-3 (D5 auto-advance).** *Confirm-dual-path camp:* R1,R2,R4,R7 (adopt structure + <=min ->
  percentile relaxation). *Safety-refinement camp:* R3 (and R4 partially) insist the fallback must
  separate **ADVANCE / RECOVER / HALT-OWNER-REVIEW** and must **not** auto-advance on
  max-epochs/stagnation/NaN; R7 offers graduated options. *Adjudication:* both are compatible with the
  sources; the dual-path *structure* and the relaxation *direction* are accepted, and the
  auto-advance-vs-halt question is **surfaced as a material owner sub-decision** (Gap G-h). No
  position forced.

- **DR-4 (D downstream consequence).** *Inert camp:* R1,R2,R7 (6.694 is dead code; under locked D the
  formulas are unchanged; drop P4-1's re-run directive). *Recompute camp:* R3,R4,R5 (verify/recompute
  thresholds under locked D; R4 says re-derivation needed; R5 says explicit equations are missing).
  *Adjudication:* the inert reading is grounded in the issue-doc code text + **[S5/ctl 2.5]** (inputs
  already scaled; D absent from the formulas) and is the **accepted core**, with explicit rejection
  of the issue doc's P4-1 re-run-under-6.694 directive. The recompute caution is preserved as a
  verify-before-assuming posture and is itself logged as **Gap G-d** (code-level confirmation is
  outside the attachments). All parties agree 4.6416 governs; the conflict is only on whether
  re-derivation work is needed.

- **DR-5 (R5 declines adaptive staging).** R5 logs a gap that `stage_strat_revision.md` "is not
  attached." *Adjudication:* **factually wrong** -- `stage_strat_revision.md` is attached at **[S6]**
  (sha256 d875cd66..., matching the wrapper). R5's gap and its refusal to adjudicate Section 6 are
  **retrieval errors**, not minority readings; not propagated. The Section-6 adjudication rests on
  R1/R2/R3/R4/R7 + direct reading of S6.

- **DR-6 (R6 multiple missing-file claims).** R6 declares `pinn_architecture.md`, `sampling_method.md`,
  `stage_strat_revision.md` absent and `framed-research-questions.md` truncated after the causal
  section, then returns "Insufficient Evidence" for architecture/sampling/stage_strat/epsilon.
  *Adjudication:* **all four are present and complete** (R6 even cites pinn's correct sha256
  `318f297a...` while calling it absent -- internally contradictory; the epsilon decision is fully
  present at S2). R6's insufficiency claims are retrieval failures and are not propagated.

- **DR-7 (R6 substantive errors on M6 and M15).** Because R6 never read pinn, it **endorses the
  issue-doc's obsolete `np.clip(L_norm,0,1)` before the `2x-1` IC mapping** (contradicting the locked
  14D contract that makes `L_norm` metadata) and **endorses the cap_table + the stale `lambda_E~1000`
  premise** (missing PHYS-05's cap at 1). *Adjudication:* both **overridden** by **[S2/scope-12 item
  1; S5/ctl Step 4; S5/pinn 4.1]**, verified directly. R6 also internally contradicts itself (correct
  14D framing for M7, IC-input framing for M6).

- **DR-8 (B-07 reconciliation).** R4 asserts "the spec and audit Section-6 pseudocode describe the
  same contract; no reconciliation conflict." R1,R2,R3,R5,R7 catch that the pseudocode hard-codes a
  fixed 32 (`np.random.choice`) violating the locked `min(32, n_snapshots)`. *Adjudication:* the
  fixed-32 bug is real **[S5/ctl Mini-Batch-Construction; locked M12 rule]**; the pseudocode must be
  corrected. R4's "no conflict" is an under-reading, not a defensible minority position.

- **DR-9 (tau_L estimator: confirm vs defer).** R4 (and R5) treat both estimators as "valid,
  complementary"; R1,R2,R3,R7 treat the choice as an un-reconciled method divergence the sources do
  not settle, compounded by the 1/lambda-vs-T_scale/lambda unit ambiguity. *Adjudication:* **defer**
  -- the spec does not designate a canonical estimator when both are present, and the unit axis for
  the tau_L thresholds is unpinned **[S5/ctl Step 3 item 5; S2 3]**. Owner picks; FUT cross-calibrates.


---

## PART 4 — Gap Register (source-silent / ambiguous -> require a user decision or FUT)

No `claimed-unverified` figure is treated as fact anywhere above. Verified anchors used as fact are
**CLM-14..CLM-19 / VF-1..VF-5** only. v1.6 has **no in-milestone verification phase** -- every figure
gap below is a FUT empirical check, not adoptable now **[S4/claims-register; S4/verified-facts]**.

| Gap | What is missing / unsettled | Resolution path | Related CLM / constraint |
|---|---|---|---|
| G-a | Causal-exponent underflow clip bound is deliberately unset ("Phase 19 does not choose a numeric clipping bound; surface a gap") | Owner/FUT sets the numeric clip if causal mode (A or C) is adopted | non-CLM spec param [S5 pinn 4.1; S5 ctl] |
| G-b | `tau_L` estimator not designated canonical (Rosenstein vs Benettin/shadow); "PCA+Rosenstein" under-specified; Rosenstein params (embedding dim, delay, Theiler window, fit window) not fully pinned | Owner picks canonical estimator; FUT cross-calibrates on a representative sample | non-CLM; ties to CLM-01 context |
| G-c | `tau_L` time-unit convention: spec `1/lambda` vs issue `T_scale/lambda` (x10); thresholds `tau_L>5`/`2-5` not tied to a time axis | Pin the convention before locking any tau_L threshold | non-CLM; couples to G-b |
| G-d | Code-level confirmation that `D=6.694` is dead in `compute_tau_L` (the read is from snapshot text only) | Code inspection + regression test that tau_L is unchanged after removing the dead lines | CLM-01 context |
| G-e | Collocation count per trajectory diverges: review 5.1 ~256/traj vs issue 16/traj (4096/256) | Owner sets the count; FUT calibration | CLM-12 (claimed) |
| G-f | Collocation "both 50/50" unproven -- 50/50 is defined for snapshot data points, not for a continuous-time collocation sampler | Define the collocation sampler explicitly, or drop the 50/50 claim for collocation | CLM-12 (claimed) |
| G-g | M16 scaling rule direction (`dt_base/dt_out` vs inverse vs none) unsettled; `dt_base=0.01` unjustified; objective undeclared; no ablation; conflicts with review 5.3 (no scaling) | Keep deferral; FUT ablation (constant vs cadence-proportional vs inverse at fixed compute) | CLM-20 (claimed); CLM-17 (verified inputs) |
| G-h | D5 attainability + per-stage thresholds (CLM-08) + MAX_EPOCHS (CLM-09) + `<=min` vs `percentile_10` + NaN-rollback detail + the ADVANCE/RECOVER/HALT-vs-auto-advance policy | Stage-0 pilot for metric traces; owner decides the fallback state machine | CLM-08/09 (claimed); locked eps_H=1e-4*S_H (PHYS-04) |
| G-i | NS-13 Huber delta: no normalized `|dH|` distribution in package; whether delta is stage-dependent | FUT-calibrate delta from observed `|dH|` quantiles (review's 0.1 a starting point) | delta is revisable, not a CLM figure |
| G-j | Epsilon: whether `eps_inv=1e-10` vs `1e-5` materially changes E/Q/stage labels is unverified | FUT: distribution of admitted separations + per-record dE/dQ/stage-label changes | non-CLM; couples to D-06 |
| G-k | Adaptive staging: population safeguard 5% vs >10%; clustering k=5 vs 6-7; k=6 -> only 6 clusters for 7 stages; scale factor `s` persistence per IC; exact gold-hole accounting (184 base-gap vs Stage-5 dedup-prefer-gold holes); EDA/pilot results absent | Owner sets thresholds/k; data-side audit of `s`; offline EDA + Stage-0 pilot; preserve gold-counterpart contract | CLM-02..07 (claimed); CLM-14/15 (verified) |
| G-l | B-07 edge cases: final stage with no k+1; undersized/absent next-stage pool; trajectory-level with/without replacement; cross-pool dedup after relabeling; replay stage balance | Spec must prohibit silent failure and require an explicit policy | CLM-12 context |
| G-m | M14: stages-0-1 value within `[7,10]`; bootstrap before the history window fills; whether gradient history resets at stage boundaries | Owner picks the 0-1 value / anneal rule; specify bootstrap + reset policy | CLM-10 (claimed) |
| G-n | ALM `mu_p` clamp: the scalar-ALM update law (constraints included, normalization, initial mu, monotone vs adaptive, cadence, checkpointing, bound sensitivity) is unspecified | Specify the P2 scalar-ALM update law before fixing any clamp; `[1e-4,100]` is non-dataset, unverified | non-CLM (claims-register exclusion) |
| G-o | Upstream baseline-report defects to fix before they propagate: review 4.3 AD ones-covector anti-pattern; review 2.2 additive `(||r||+eps)` softening form | Replace 4.3 with the PHYS-02 componentwise contract; use 2.2's value argument only, not its additive form | PHYS-02 (pinn 5.3.1); PHYS-03 / item 4 |

**Non-gaps recorded to prevent re-litigation.** The two false "missing-file" gaps raised by R5 (it is
attached at S6) and R6 (pinn/sampling/stage_strat attached at S5/S6; framed-questions complete at S2)
are **not** real gaps; they are retrieval errors and are excluded from this register.

---

## PART 5 — Source-Coverage Checklist

### Canonical sections (every section touched, or marked irrelevant)

| Section | File(s) | Role | Coverage in this adjudication |
|---|---|---|---|
| S1 | RESEARCH-CONTEXT-MASTER.md | Orientation / source-treatment preamble | Used for source hierarchy + bundle-reading rule. Not a figure source. |
| S2 | scope-12-hard-constraints.md; framed-research-questions.md; resolution-doc-skeleton.md | Locked constraints (items 1-7); the question backbone; non-binding skeleton / phase map | Fully used. The 7 hard constraints anchor every "locked" disposition; the framed questions define the claim ledger; the skeleton's phase map informs the resolution structure. |
| S3 | 03-curriculum-and-training-loop.md (issue doc) | Non-authoritative subject under adjudication | Fully read. Every finding (D-04/05/06, B-07/08, M6/M7/M14/M15/M16, D5, NS-12/13/18, adaptive, D-conflict, tau_L/L_max, mu_p) is adjudicated, not transcribed. The `compute_tau_L` dead-D read is from this file. |
| S4 | claims-register.md; verified-facts-reference.md; consolidated-context.md | Figure grounding (CLM-01..20); v1.5-verified anchors; minimal context | Fully used. CLM statuses governed every figure call; only CLM-14..19 / VF-1..5 used as fact. |
| S5 | ctl_instruction.md; pinn_architecture.md; sampling_method.md | Framework specs = source of truth + Sobol/`s` grounding | Fully used and **independently verified** (D-lock 2.5; causal/ALM rejection; clip C-schedule; 4 stage criteria; pinn 3.1/3.2/3.4/4.1/4.2/4.4/5.3.1; s_min/eps_inv/tau_L/L_norm Step 3-4; sampling s-in-[0.8,1.2]/Q~s^3). |
| S6 | review_of_framework.md; stage_strat_revision.md | Baseline design-intent reports (explicit critique mandate) | Fully read. review's superseded contracts (2.2, 4.2, 4.3, energy weight) flagged; its surviving parts used. stage_strat Table 4 / Phase IV / SI-SSR-001 adjudicated against locked topology. |

No canonical section is irrelevant; all six were used.

### Reports (every R# touched + reliability)

| R# | Bytes | Coverage | Reliability | Net contribution |
|---|---|---|---|---|
| R1 | 57819 | All 18 questions + 10-gap register + coverage map | High | Comprehensive, well-grounded; the D-inertness demonstration; treats M16 as insufficient evidence. |
| R2 | 47478 | All questions + C1/C2 cross-cutting + gap register | High | Comprehensive; **unique catch** of the tau_L unit ambiguity (1/lambda vs T_scale/lambda). |
| R3 | 55221 | All questions + conflict register + spec edits | High | Comprehensive; the D5 ADVANCE/RECOVER/HALT refinement; L_max "characteristic not maximum" narrowing; non-Plummer shadow-softening catch; cautious D-downstream stance. |
| R4 | 42645 | All questions + dependency map + 17-gap register | Medium-High | Thorough but less cautious: frames M15 as open (raise-hybrid), adopts M16, calls D re-derivation needed, misses the B-07 fixed-32 bug. Good catch: dt_base=0.01 unjustified. |
| R5 | 11132 | Partial; concordant on big items | Low | Short; **retrieval error** -- falsely declares stage_strat_revision.md missing and declines Section 6; over-flags tau_L equations as missing. |
| R6 | 48267 | Partial; verbose/low-precision | Low | **Unreliable** -- falsely declares pinn/sampling/stage_strat absent and framed-questions truncated; consequently gets M6 and M15 wrong (endorses obsolete fixes). Internally contradictory. |
| R7 | 26170 | All questions + consolidated owner view | High | Concise, sharp; the "issue doc written against earlier spec" meta-pattern; the k=6-vs-7-stage + discover-offline-then-freeze posture; the joint data/energy delta-audit point. |

---

## PART 6 — Non-Independent-Input Note

How apparent synthesis/overlap among reports was handled, without assuming model identity (identity
was not provided and was not inferred):

1. **Heavy overlap was neutralized, not rewarded.** All seven reports read the same six files, so they
   converge on the canonical-grounded findings (D-lock, causal-not-SOT, Huber-not-L1, M7 exclusion,
   PHYS-02 satisfies NS-12). Per the mandate, agreement is **not** evidence: every disposition in Part
   1 is anchored to a canonical section I read and verified (Part 5, S2/S4/S5/S6), and restatements
   across reports were given **no** additional weight. Where five or six reports said the same thing, I
   still re-derived the verdict from the spec, not from the count.

2. **Possible synthesis/merge was not given extra weight.** R1 reads like a consolidated resolution
   (numbered verdict ledger + gap register + coverage map) and R7 opens with "I now have a thorough
   panel analysis" -- suggesting one or both may post-date and synthesize the others. Some phrasing and
   structure recur across R1/R2/R3/R7 (e.g., the identical L_max rendering; the "8.5 is the midpoint of
   [7,10]" observation; near-identical gap IDs). I treated each report's claims as needing canonical
   grounding regardless of lineage, and a possibly-synthetic report earned no premium for restating
   others. No verdict rests on a chain of reports citing each other; each rests on S2/S4/S5/S6.

3. **Two reports' dissents trace to retrieval failure, not to a minority reading of the evidence.** R5
   declined the adaptive-staging question on the false claim that `stage_strat_revision.md` is missing;
   R6 declared four attached files absent/truncated and returned spurious "Insufficient Evidence." Both
   were checked against the attachments (the material is present and complete -- including R6's own
   correctly-quoted sha256 for the file it calls absent). Their gap/insufficiency claims and the
   downstream errors they caused (R6's endorsement of the obsolete M6 clamp and M15 cap_table) were
   **overridden by direct verification** against S5/S6, which I read in full, and were recorded in the
   Disagreement Register (DR-5, DR-6, DR-7) and excluded from the Gap Register. Critically, R5/R6's
   inability to read a file did **not** weaken the adaptive-staging, M6, or M15 verdicts that R1/R2/R3
   /R4/R7 plus my own reading support.

4. **Genuine minority positions among the reliable reports were preserved, not majority-voted.** Where
   high-reliability reports actually disagreed on substance -- M16 adopt (R2/R4) vs defer (R1/R3/R7);
   D-downstream inert (R1/R2/R7) vs recompute (R3/R4); D5 auto-advance (R1/R2/R4/R7) vs HALT-only (R3);
   tau_L confirm (R4) vs defer (R1/R2/R3/R7) -- I resolved each against the canonical source (the spec's
   own deferral, the issue-doc code text, the locked floors) and **kept the dissent on the record**
   (DR-2, DR-4, DR-3, DR-9), with several routed to the owner (surface_to_user) or to FUT (defer)
   rather than forced to a single answer.

---

*Adjudication worked only from the attached files. No external information was used. Locked SCOPE-12
outcomes were reconciled to, never re-opened. Every `claimed-unverified` figure is recorded as a
claim, not a fact; the only figures used as fact are the v1.5-verified anchors CLM-14..CLM-19 /
VF-1..VF-5. Material cited by a report but not attached was treated as unavailable; material a report
wrongly called unavailable was verified present and adjudicated on its merits.*
